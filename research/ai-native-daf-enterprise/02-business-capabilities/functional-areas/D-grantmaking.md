# D. Grantmaking

**Capabilities:**
- C3.1 Recipient registry and eligibility
- C3.2 Recommendation intake
- C3.3 Grant decisioning
- C3.4 Disbursement and remittance
- C3.5 Post-grant obligations
- C5.2 Screening and fraud
- C5.3 Exception management

**Outcomes:** O-06, O-08, O-15, O-07, O-13.

**Accountable:**
- Head of Grants Compliance: eligibility, decisioning, post-grant.
- Controller: disbursement.

## 1 Existing industry operating model

**Legal frame.** §4966 taxes taxable distributions at 20% on the sponsor and 5% (capped at $10k) on knowing managers. §4967 taxes prohibited benefits at 125% on the donor or advisor and 10% on managers. Grants to listed §170(b)(1)(A) public charities are excepted from §4966, and grantors may rely on IRS listings ([industry report §4](../../../DAF-INDUSTRY-REPORT-2026-11.md)).

**How many grants need judgment** (strategic synthesis §0 A, "Grant approval is the bottleneck"; [`g0503-0501-exception-proxy-refinements.md`](../../../mission-2026-11-14/g0503-0501-exception-proxy-refinements.md)):

| Measure | Value |
|---|---|
| Like-for-like non-standard share, four largest nationals, FY2023–24 dollars | about 3.6% |
| Same, with the EIN-keyed fiscal-sponsor list | about 4.2% (3.9% without 50CAN, Global Impact, NEO Philanthropy and Myriad USA) |
| Top-50 core review-need proxy | **7.76% of recipient lines and 11.61% of dollars** (6.80% / 11.00% counting only true new organisations) |
| Same proxy, per grant, at Fidelity, NPT and Vanguard | about 7–8.5% of grants |
| Grants to EINs under IRS revocation | **0.082%** of top-50 Schedule I dollars ([`direction-recipient-compliance-screen.md`](../../../mission-2026-11-14/direction-recipient-compliance-screen.md)) |

The proxy measures *recipients that could need review*, not observed review. **No sponsor publishes exception rates, reviewer minutes or turnaround P50/P90.** Only 5 of 28 published turnaround statements are measured, and all of those are vendor figures (industry report §4; [`queue-batch36-metrics-rails.md`](../../../mission-2026-11-14/queue-batch36-metrics-rails.md)).

**Volume and size.**
- NPT processed 159,543 grants in FY2025. The governing FY2024 figure is 129,575 (FINAL-STATUS, PR #74).
- Published average grants are about $4.5–6k at Fidelity, RCF and DAFgiving360, and $11–15k at the mid-size nationals.
- Small recipients receive many grants, about 12.5 per recipient at Fidelity (industry report §11.77; FINAL-STATUS PR #73).

**Payment rails come in four camps** (industry report §2.5):

| Camp | Users and notes |
|---|---|
| Fidelity EFT/Stripe | 67% of Fidelity's grants via EFT |
| PayPal Grant Payments | NPT, Vanguard |
| Ren Rapid Disbursement Engine | |
| Chariot Disbursements | TIFIN/GiveClear, Daffy, Founders Pledge, Groundswell, Charityvest (transitioning) |

**Payment and remittance mechanics.**
- No rule requires paper checks (strategic synthesis A7).
- No top-10 sponsor page read states a grant ID in ACH addenda.
- Grant detail travels out of band ([`b4013-02-b4222-02-remittance-and-portal-features.md`](../../../mission-2026-11-14/b4013-02-b4222-02-remittance-and-portal-features.md)).

**Sponsor discretion.** After the SPLC indictment in April 2026, Fidelity Charitable, Vanguard Charitable and DAFgiving360 restricted grants, and 16 AGs wrote to them (industry report §4).

**AI in this function.**
- No public evidence of AI in sponsor-side approval or eligibility (industry report §7).
- Agentic products are donor-side: TIFIN Louise; Daffy MCP `make_donation` with no documented limits.

## 2 Actual required business outcomes

1. Every grant goes to an eligible recipient for a charitable purpose, or meets the expenditure-responsibility (ER) or equivalency requirements (O-06, O-07).
2. No grant confers more than an incidental benefit on a donor, advisor or related party (O-08).
3. No grant reaches a sanctioned party (O-07).
4. Funds arrive at the right entity quickly, with machine-readable identification of the grant (O-15).
5. Donors, advisors and recipients can see the status of every grant at any time without asking (O-09).
6. Post-grant obligations are tracked to closure: ER reports, restricted-grant conditions, returns (O-06).
7. Sponsor discretionary policy is applied consistently and is board-approved (O-10).

## 3 Legal and risk constraints

**Legal mandates.** Map each to the [regulatory map](../../08-governance-and-compliance/regulatory-applicability-map.md):
- §4966: charitable purpose, and ER for grants to non-§170(b)(1)(A) organizations via §4945(h).
- §4967.
- §4958(c)(2): no grants to donors or advisors.
- Notice 2017-73: pledges and event tickets.
- Rev. Proc. 2018-32: reliance on IRS data.
- OFAC.
- State AG oversight.

**Internal policy, not law:**
- reputational and discretionary holds;
- the dollar thresholds for human review;
- a minimum grant amount;
- a check threshold;
- the anonymity default.

**Risk:**
- name ambiguity, leading to the wrong entity being paid;
- payee bank hijack;
- sham charities;
- circular flows to donor-controlled entities;
- AI agents manipulated into recommending fraudulent payees;
- mass simultaneous recommendations, such as a disaster or a viral campaign.

## 4 Proposed AI-native operating model

**Grantmaking is a continuous, event-driven state machine, not a sequence of forms and departmental handoffs.**

```
Submitted → Resolving → Evaluating ─┬─(all D-pass)──────────────→ Approved → Released → Settled → Reconciled
                                    ├─(flag/refer)→ AwaitingHumanDecision ─┬→ Approved
                                    │                                       └→ Declined
                                    └─(deny rule)→ Declined
Approved/Released → (CharityEligibilityChanged | PaymentReturned) → Held / Returned
```

1. **Recipient identification.**
   - Exact EIN, or selection from the registry: D.
   - Free text ("the food bank in Dayton"): the recipient-resolution agent proposes candidates and the **donor confirms** (P → D by confirmation).
   - The registry includes non-BMF recipients: churches without e-filed 990s take about 8.3% of top-50 DAF dollars (strategic synthesis §0 G4). For them the registry uses denomination group rulings and other recognized evidence.
2. **Charity eligibility verification is continuous, not per grant (DD-012).**
   - The registry ingests BMF, Pub 78, the auto-revocation list and OFAC on each publication.
   - Diffs produce `CharityEligibilityChanged` / `SanctionsListUpdated`.
   - At grant time, eligibility is a lookup against a fresh, versioned snapshot (D).
   - Stale data, past its freshness SLO, means *refer*, never pass.
3. **Organizational due diligence** applies only where the class requires it: non-public-charity, foreign, new ruling (<24 months), fiscal sponsor, Type III supporting organization. The exception dossier preparer assembles the evidence; a human decides.
4. **Restricted grant review.** Purpose and restriction text is classified (P). Restrictions implying donor benefit, scholarships to named individuals, or ER-triggering purposes raise flags. **AI may add a flag, never clear one** (DD-005).
5. **Prohibited-benefit detection.**
   - Deterministic rules: recipient equals a related party, or a §4958 disqualified person via the relationship graph; pledge language; ticket or membership terms.
   - The benefit-risk flagger (P): purpose text, event-related grants, timing against galas, tuition patterns.
   - Flags go to a human.
6. **Recommendation assessment and risk-based approval:**

| Path | Criteria (policy `grant-routing@vN`) | Decision | Expected share |
|---|---|---|---|
| **Routine** | Listed §170(b)(1)(A) public charity; not revoked; no sanctions hit; no flags; amount ≤ routine threshold; account balance sufficient; within velocity limits | **D: policy engine approves** (DD-004) | The large majority by count. The repo's core per-grant proxy implies about 7–8.5% of grants fall *outside* routine on recipient characteristics alone at the big nationals; flag rates add to that and are unmeasured (GAP) |
| **Enhanced** | Routine recipient, but amount above threshold, or a velocity or fraud-score band | D gates plus H confirmation by a payments or grants specialist | Small |
| **Specialist** | Foreign (equivalency or ER), non-charity (ER), fiscal sponsor, new ruling, Type III, flagged benefit or purpose | **H**, a grants compliance specialist with a P dossier | ~4–12% of dollars per the proxies above |
| **Sanctions** | Potential true match | **H**, the sanctions officer only | Very rare |
| **Policy hold** | Recipient on a board-approved discretionary list | **H**, the policy owner, under a board policy | Rare |

7. **Payment execution.** `GrantApproved` → payment gate (D):
   - verified payment profile, not in a change cooling-off;
   - limits;
   - dual control above the threshold;
   - sufficient funds.

   Then `PaymentInstructed` with an idempotency key. Rails: ACH with a CCD+/CTX addendum carrying the grant ID [A design choice; the industry does not do this today]; RTP or FedNow where the recipient bank supports it [A]; check only as a residual.
8. **Confirmation and reconciliation.** `PaymentSettled` is matched on the idempotency key. Remittance is delivered to the recipient: grant ID, donor information per the anonymity choice, purpose. Reconciled to the ledger.
9. **Grant status tracking.** One state machine read by the donor, advisor, sponsor and recipient (ACT-030 eliminated).
10. **Post-grant monitoring when appropriate.** ER report tracking; restricted-grant follow-up; and re-checks of eligibility after payment, where a revocation with an effective date before the grant date opens a review case.

**Mass simultaneous recommendations** (disaster, viral campaign):
- The routine path scales horizontally.
- Velocity limits per account and per recipient hold the excess, not reject it.
- Recipient-level surges trigger a fraud check on that recipient's payment profile.
- Liquidity checks run against the pool cash buffer (see areas E and F).

## 5 Eliminated activities

| Activity | Disposition |
|---|---|
| ACT-017: manual review of every grant | Eliminated |
| ACT-018: per-grant IRS lookup by a person | Eliminated |
| ACT-019: per-grant OFAC search by a person | Automated |
| ACT-023: calling charities to confirm acceptance | Transformed into one-time recipient enrollment |
| ACT-024: check printing | Reduced |
| ACT-025: cover letters | Transformed into machine-readable remittance |
| ACT-028: batched payment runs | Eliminated |
| ACT-030: status inquiries | Eliminated |
| ACT-031: data entry from emails | Eliminated |
| ACT-075: purpose-text review of every grant | Eliminated; flags only |

## 6 New workflows

- **WF-D1 Routine grant, no human.** `RecommendationSubmitted` → `RecipientResolved` → `EligibilityEvaluated` (pass) → `ScreeningCompleted` (pass) → policy → `GrantApproved` → `PaymentInstructed` → `PaymentSettled` → remittance → reconciled.
- **WF-D2 Flagged grant.** As WF-D1, then `GrantFlagged` → `ExceptionCaseOpened` with the dossier → `ExceptionCaseResolved` (H) → resumes or `GrantDeclined` with a reason code.
- **WF-D3 Foreign grant.** Equivalency determination reuse: one determination per foreign recipient per validity period, shared across accounts. Otherwise the ER path: the post-grant ER tracker drafts the agreement and tracks reports.
- **WF-D4 Eligibility change mid-flight.** `CharityEligibilityChanged` → in-flight grants re-evaluated → unreleased payments held → donors notified → released payments go to post-payment review.
- **WF-D5 Payee bank change.** `PaymentProfileChanged` → out-of-band verification → cooling-off → fraud screen → profile active.
- **WF-D6 Recurring grants.** A standing recommendation creates `RecommendationSubmitted` on schedule; each instance passes through the gates afresh.
- **WF-D7 Donor-agent recommendation.** An agent principal submits within its delegated scope (DD-017). Above the scope's confirmation threshold the donor confirms. The sponsor's gates are identical to those for a human recommendation.

## 7 Required data

- Recommendation: recipient candidate, amount, purpose, restriction, recognition, channel, requesting principal.
- Recipient registry: EIN or foreign ID, aliases, BMF and Pub 78 status history, revocation, Type III status, rulings, church and group-ruling evidence.
- OFAC index with version.
- Relationship graph.
- Payment profiles with verification evidence.
- Policy versions.
- Equivalency determinations and ER agreements.
- Prior grants.
- Liquidity position.

## 8 Required APIs

- `/v1/recommendations`
- `/v1/recipients`: search, resolve
- `/v1/eligibility`: evaluate, with snapshot versions
- `/v1/grants`: state, history
- `/v1/payments`
- `/v1/decisions`
- `/v1/cases`
- `/v1/policies`
- `/v1/evidence`
- `/v1/events` (webhooks to donors, advisors and recipients)

## 9 Event triggers

`RecommendationSubmitted`, `RecipientResolved`, `EligibilityEvaluated`, `ScreeningCompleted`, `GrantFlagged`, `GrantApproved`, `GrantDeclined`, `GrantCanceled`, `PaymentInstructed`, `PaymentSettled`, `PaymentReturned`, `PaymentProfileChanged`, `CheckAged`, `CharityEligibilityChanged`, `SanctionsListUpdated`, `ExceptionCaseOpened` / `Resolved`, `PolicyPublished`.

## 10 AI agent responsibilities

| Agent | Category | Responsibility | Prohibited |
|---|---|---|---|
| Recipient-resolution agent | 2 | Propose candidate entities with evidence | Binding a recipient without donor confirmation or an exact ID |
| Benefit-risk flagger | 2 | Flag prohibited- or private-benefit indicators with reasons | Clearing flags; approving |
| Sanctions near-match triage | 2 | Rank and explain near-matches | Clearing |
| Exception dossier preparer | 2 | Assemble the evidence pack for the specialist | Recommending approval as a decision; it may summarise |
| Post-grant ER tracker | 3 | Draft ER agreements and report requests; track deadlines; send reminders | Accepting an ER report as sufficient (H) |
| Related-party detector | 2 | Detect undeclared links between donor and recipient | Writing relationships |

## 11 Deterministic automation responsibilities

- Eligibility evaluation against snapshots.
- Sanctions screening.
- Routing policy.
- Routine approval.
- Velocity and fan-out limits.
- Payment gate checks.
- Idempotent instruction.
- Settlement matching.
- Remittance generation.
- Eligibility re-checks.
- Check aging and escheat timing.

## 12 Human oversight requirements

- Specialist-path decisions.
- Sanctions true match.
- Discretionary holds under board policy.
- Changes to routing thresholds: policy owner plus CRCO, back-tested before publication (DD-011).
- Sampled QA of routine D approvals: a statistically sized monthly sample reviewed by a specialist, with findings feeding the improvement loop. This is the falsification check on DD-004.

## 13 Exception management

| Case type | SLA [A] | Notes |
|---|---|---|
| Specialist grants | 2 business days for domestic flags; published clock for foreign and ER | Skill-routed, with the dossier attached |
| Donor clarification (ambiguous recipient) | — | Goes to the donor, not staff |
| Returns | — | Profile invalidated, donor notified, re-grant offered |
| Discretionary hold | — | Recorded decision and donor notice |

## 14 Security and compliance controls

- Requests are not instructions (DD-003).
- The approver cannot be related to the donor or recipient.
- The person who creates a payee profile cannot approve a payment to it.
- Cooling-off on bank changes.
- Idempotency keys at the rail.
- Fan-out caps.
- Every decision recorded with policy and data snapshot versions.
- Agent outputs cannot reach the payment gate except through the D policy engine.

## 15 Estimated staffing implications

**Drivers:**
- specialist-path grants per year × minutes per case [A: a domestic flag about 20–45 minutes; foreign or ER several hours];
- the QA sample size;
- the return and exception rate on payments.

The routine path has **no headcount driver** beyond its supervision. The repository's labor pool estimate for grant review is thin: about $16k a year at a 48,744-grant sponsor and about $975k a year at Fidelity scale [S] (strategic synthesis A5). Specialist staffing therefore scales with the *complex* share, not with total grants.

Numeric FTE is in [`../../09-financial-models/`](../../09-financial-models/).

## 16 Cost and performance model

**Cost drivers:**
- rail fees per payment [A; Chariot/PayPal/ACH pricing varies; see the repository's rails files];
- eligibility data costs (IRS data free; commercial enrichment optional);
- specialist time;
- inference (immaterial: about $0.45 per heavy review against about $83 of reviewer time [V]).

**Design targets [A]:**

| Measure | Target |
|---|---|
| Routine path, recommendation to `PaymentInstructed` | P50 under 1 minute; P99 under 1 hour (excluding bank cut-offs) |
| Specialist path | P50 under 2 business days for domestic |
| Electronic share of payments | Over 95% |
| Remittance with grant ID | 100% |

## 17 Implementation dependencies

- IRS bulk data ingestion.
- OFAC list ingestion.
- Policy engine and routing policy approved by the board.
- Payment bank or rail partner supporting addenda and webhooks (DD-008).
- Recipient enrollment portal.
- Relationship graph (area B).
- Liquidity service (area E/F).

## 18 Measurable success criteria

1. Share of grants on the D path, and its QA error rate (the falsifier for DD-004).
2. Latency distributions per path, published.
3. Grants to entities ineligible at grant time. Target: zero; measured against the bitemporal snapshot.
4. Prohibited-benefit or sanctions misses found by audit. Target: zero.
5. Electronic payment share; returns rate; time to remittance.
6. Recipient-reported reconciliation effort, surveyed.
7. Status inquiries per 1,000 grants. Target: near zero.
