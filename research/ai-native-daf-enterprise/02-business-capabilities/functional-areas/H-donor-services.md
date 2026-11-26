# H. Donor services

**Capabilities:** C1.4 Donor and advisor servicing (primary), C1.1, C1.2, C5.3, C1.5 · **Outcomes:** O-09, O-16, O-17, O-02 · **Accountable:** Head of Client and Partner Operations ([accountability matrix](../accountability-matrix.csv))

## 1. Existing industry operating model

The conventional model is a phone, email and web-form contact center in front of a recordkeeping system. Representatives look up status, process changes and explain policy.

What the repository shows about it:
- **No published service promise.** Among the top-20 sponsors, the 13 readable sites publish no response-time promise, no public chat channel and no WCAG conformance claim. Three publish phone hours; AEF's accessibility statement is placeholder text; FFTC relies on an overlay. Automated axe-core checks found critical WCAG failures on 7 of 37 pages ([industry report §11.22](../../../DAF-INDUSTRY-REPORT-2026-11.md); [`direction-sponsor-accessibility-service.md`](../../../mission-2026-11-14/direction-sponsor-accessibility-service.md)).
- **Complaint data does not measure quality.** Among the 15 largest sponsors only Fidelity Charitable and RCF have review-venue records. Fidelity's rate is 1.32 per 10,000 accounts, and rankings flip with the denominator ([`gap19-complaints-with-denominators.md`](../../../mission-2026-11-14/gap19-complaints-with-denominators.md); strategic synthesis §0 A).
- **Processor complaints center on payout rules** (check thresholds, lost checks, EFT vetting). Written rules explain only two of seven named complaints ([`g1913-processor-disbursement-rules.md`](../../../mission-2026-11-14/g1913-processor-disbursement-rules.md)).
- **Donor-side AI is search or assistant only at incumbents.** Fidelity's assistant is search only; NCF has AI site search; TIFIN Louise and Daffy's MCP server are the only products that move DAF money, and both end in sponsor review ([industry report §11.25](../../../DAF-INDUSTRY-REPORT-2026-11.md); [`direction-ai-product-census.md`](../../../mission-2026-11-14/direction-ai-product-census.md)).
- **Donor protection.** Login MFA or a one-time code is published at 3 sponsors holding 52.0% of assets ([`b49-04-fraud-diversion-controls.md`](../../../mission-2026-11-14/b49-04-fraud-diversion-controls.md)).
- **Portability is thin.** NPT's Excel export is the one documented top-10 donor export, and no top-12 sponsor publishes an outbound transfer policy (strategic synthesis §0 A).

[I] Because no sponsor publishes contact volumes or reasons, the conventional contact mix (status, how-to, changes, documents) is an inference from feature and complaint evidence, not a measurement (GAP: no sponsor contact-reason data).

## 2. Actual required business outcomes

- Donors and advisors get correct answers about their account, grants and policies, grounded in authoritative state (O-09).
- Changes to profile, instructions, successors and privileges are executed safely, with the donor's verified intent (O-02, O-17).
- Documents are available on demand: acknowledgments, statements, grant history, tax-year summaries (O-01, O-12).
- Donors have real human recourse for disputes, harm and complex life events such as death, incapacity, divorce or business sale (O-16).
- No individualized tax advice is given; general information is cited (O-09). The DAF is not presented as tax-superior: [`direction-donor-tax-scenarios-2026.md`](../../../mission-2026-11-14/direction-donor-tax-scenarios-2026.md).

## 3. Legal and risk constraints

| Constraint | Source | Implication |
|---|---|---|
| Exclusive legal control: servicing cannot imply that donors direct assets | §4966(d)(2); O-03 | Service language says "recommend", and service agents create *requests*, never instructions (DD-003) |
| Acknowledgments must be accurate, including the §170(f)(18) exclusive-control statement | IRC §170(f)(8), (18) | Reissued documents are generated deterministically, never AI-drafted |
| Unfair or deceptive practice exposure for misleading statements | State UDAP; FTC Act jurisdiction over nonprofits is limited (see [regulatory map](../../08-governance-and-compliance/)) | Grounded answers with citations; QA sampling |
| Privacy and confidentiality of donor identity and anonymity choices | State privacy and breach laws; program agreement; Schedule B confidentiality | Authorization on every read; anonymity preserved in every channel |
| Accessibility | ADA Title III applicability to websites is contested in case law [I]; best practice is WCAG 2.2 AA | Design target WCAG 2.2 AA; automated plus manual audits |
| Account takeover and authorized-push fraud | O-08 | Step-up authentication for payout-relevant changes; cooling-off; notification via the prior channel |
| Tax-advice boundary | Professional regulation; liability | The service agent refuses individualized tax conclusions and refers to the donor's advisor or CPA |

## 4. Proposed AI-native operating model

Service is redesigned around three facts:

1. **Most contacts disappear when state is shared.** Grant status, contribution receipt and "did the charity get it" questions are answered by the shared grant and contribution state machines. Donors, advisors and recipients see the same correlation-ID timeline (ACT-030 eliminated).
2. **Remaining questions are answered from two governed sources only:**
   - authoritative account state, through read models with field-level authorization;
   - the approved policy and answer corpus, with clause IDs approved by the GC (see [canonical data model §5](../../06-data-and-knowledge/canonical-data-model.md)).

   The **service answer agent** composes the answer and must cite each fact's state field or clause ID. Ungrounded claims are blocked by an output validator.
3. **People handle what requires judgment, empathy or authority:** disputes, bereavement and successor matters, harm remediation, complex asset questions, vulnerable donors, and anything the donor asks to escalate. Requesting a human is always available and never gated behind the agent.

Service tiers:

| Tier | Handled by | Examples | Authority |
|---|---|---|---|
| T0 Self-service | Portal, app, API, advisor platforms | Status timeline, documents, profile edits with step-up | Donor's own privileges |
| T1 Agent-resolved | Service answer agent (AGT-S, read-only plus drafting) | Policy questions, how-to, "why is my grant pending" (explains which gate, without disclosing screening details) | Read only; it can *prepare* a request (for example a draft recommendation) that the donor confirms in an authenticated step |
| T2 Specialist | Client operations specialist | Disputes, successor activation, error remediation, goodwill credits within limit | Delegated limits (DEC-056) |
| T3 Leadership / counsel | Head of Client and Partner Operations, GC | Litigation threats, regulator or AG complaints, material harm | Per delegation register |

## 5. Eliminated activities

- ACT-030: grant status inquiries, removed by the shared state machine.
- ACT-052: statement production and mailing, reduced to on demand.
- ACT-053: address and profile change processing, now self-service with step-up.
- ACT-009: welcome kit mailing.
- ACT-051: transformed from routine phone and email handling to grounded self-service and the agent.
- Manual document reprinting: documents are regenerated from the ledger on request.

## 6. New workflows

- **WF-H1 Grounded answer.** A question is classified (P), then:
  - if it is about account facts → read model;
  - if it is about policy → retrieval over the approved corpus;
  - the answer is drafted with citations, passes the validator (every claim cites a field or clause), and is delivered.
  - If validation fails, the agent says it cannot answer and offers a human.
- **WF-H2 Request preparation.** The donor states an intent in conversation, for example "give $5k to the food bank in my town". The agent resolves candidate recipients and shows structured options. The donor confirms in the authenticated UI, which emits `RecommendationSubmitted`. The agent never submits.
- **WF-H3 Service recovery.** Triggered by complaint signals (sentiment flag P, explicit complaint, or an SLA breach on a donor-visible item). `ExceptionCaseOpened` (type: service recovery) goes to a specialist with the full event timeline. The resolution may include a remediation decision (H) and a root-cause tag that feeds C6.4.
- **WF-H4 Bereavement and successor.** `DonorDeceased` (documented) suspends privileges and holds pending recommendations. Successor document verification is D; a dispute is H with counsel. Then `PrivilegeGranted` to the successor.
- **WF-H5 Documentation on demand.** `DocumentationRequested` → deterministic generation → `DocumentationDelivered`, with a hash and a delivery receipt.
- **WF-H6 Outbound transfer.** `TransferOutRequested` → eligibility of the receiving sponsor is checked (D) → liquidation, if needed, under policy → grant to the receiving sponsor, plus a full-history export in the open grant record format (DD-006, O-16).

## 7. Required data

Read models: account summary, positions in units and value, contribution and grant timelines with state and reason codes, documents index, privileges, fee history. Policy corpus with clause IDs and versions. Conversation records: question, retrieval citations, state snapshot hash, answer, validator result, and escalation if any. Complaint taxonomy and outcomes. Consent and preference records.

## 8. Required APIs

`/v1/accounts/{id}` (read), `/v1/grants?account=` (timeline), `/v1/contributions`, `/v1/documents` (generate and fetch), `/v1/recommendations` (draft and confirm), `/v1/privileges` (successor and advisor grants), `/v1/cases` (service recovery), `/v1/events?correlation=` (timeline feed), `/v1/parties/{id}` (profile with step-up). See the [API catalog](../../04-enterprise-apis/).

## 9. Event triggers

| Event | Service action |
|---|---|
| `ContributionSettled`, `AcknowledgmentIssued` | Proactive notifications |
| `GrantApproved`, `PaymentSettled`, `PaymentReturned`, `GrantDeclined` | Proactive status with reason codes, so the donor does not need to call |
| `CharityEligibilityChanged` affecting a donor's pending or recurring grants | Notify with options |
| `DonorInstructionChanged` | Confirmation via the *prior* contact channel (anti-takeover) |
| `DonorDeceased`, `AccountInactivityThresholdReached` | Continuity workflows |
| `ExceptionCaseOpened` / `Resolved` | Service-recovery tracking |
| `CustodianUnavailable` | Status banner and adjusted expectations |

## 10. AI agent responsibilities

- **Service answer agent** (Category 3, supervised execution of *communications only*).
  - Tools: read-model queries scoped to the authenticated principal; corpus retrieval; draft-request creation.
  - Prohibited: any write to authoritative state, fee waivers, revealing screening logic or other donors' data, tax advice.
  - Escalates on: complaint, distress, bereavement, legal threat, a repeated failure to answer, or a request for a human.
- **Request preparation** (inside the same agent): recipient candidate resolution (P). The donor confirms.
- **Sentiment and complaint classifier** (Category 2): flags service-recovery cases; may add, never clear.
- **QA sampler** (Category 2): scores a sample of conversations against a rubric; humans review the disagreements.

## 11. Deterministic automation responsibilities

Notifications from events; document generation; step-up authentication rules (DEC-049); cooling-off timers; SLA timers on cases; routing of escalations by type and authority; anonymity enforcement in every rendered output; the output validator (claim-to-citation check).

## 12. Human oversight requirements

- Goodwill credits and remediation above the limit (DEC-056).
- Successor disputes (DEC-072).
- All complaints labeled regulatory or legal.
- Weekly review of QA disagreements and validator blocks by the agent owner.
- A monthly corpus review by GC for new clauses arising from unanswered questions.

## 13. Exception management

Every service exception is an `ExceptionCase` in the single queue (C5.3), typed `service.recovery`, `service.successor`, `service.document` or `service.complaint.regulatory`. SLA clocks are visible to the donor in the timeline. Root-cause tags are required on closure, and recurring causes create improvement hypotheses in C6.4, for example "returned payments due to a stale recipient bank profile".

## 14. Security and compliance controls

- Phishing-resistant MFA for donors (passkeys preferred), with step-up for payout-relevant changes.
- No "agent asks for codes": published anti-social-engineering notices, a practice documented by Fidelity per b49-04.
- Prompt-injection defences: tool access is scoped to the authenticated principal, retrieved content is treated as data, and outputs are validated.
- Conversation retention under a records schedule; PII redaction in telemetry.
- Service agent credentials cannot call payment, ledger-write or privilege-grant APIs (architecture invariant test).

## 15. Estimated staffing implications

**Drivers:** contacts per account per year that remain after T0 and T1; the share that are T2-eligible; handle time; bereavement events (mortality rates in the donor base); complaint rate.

**Direction:** the conventional tier-1 call-center function largely disappears (ACT-071); a small specialist recovery team remains. Numeric FTE by scale is computed in [`../../09-financial-models/`](../../09-financial-models/) from labeled [A] parameters. No sponsor publishes contact volumes, so these parameters are assumptions pending GAP validation.

## 16. Cost and performance model

| Metric | Target [A] | Note |
|---|---|---|
| T0+T1 resolution share of contacts | ≥ 85% | Validate in Phase 5 pilot |
| Grounded-answer validator pass rate | ≥ 98% | Failures route to a human |
| QA accuracy of agent answers (rubric) | ≥ 99% on facts, ≥ 97% on policy explanations | Measured on stratified samples |
| Median human response, T2 | < 1 business day | Published as a commitment, unlike any top-20 sponsor today |
| Cost per resolved contact | Inference cost is immaterial relative to labor (about $0.45 per heavy review vs about $83 of reviewer time, [industry report §7](../../../DAF-INDUSTRY-REPORT-2026-11.md)); cost is dominated by T2 minutes | Model in 09- |

## 17. Implementation dependencies

Shared state machines for contributions and grants (03-, 06-); the read models and authorization service (C1.2); the approved policy corpus (GC); identity and step-up (K); case management (C5.3); notification channels; the accessibility design system (Forma is evaluate-later only, DD-014).

## 18. Measurable success criteria

- Status-type contacts per 1,000 accounts fall by ≥ 70% vs the pre-launch baseline [A].
- 0 instances of an agent writing authoritative state (invariant test plus audit).
- 0 individualized tax-advice findings in QA samples.
- Published response-time commitment met at ≥ 95%.
- WCAG 2.2 AA conformance on all donor flows (automated plus manual audit).
- Service-recovery cases closed with a root cause at 100%.
- Donor-reported effort score improves versus baseline.
