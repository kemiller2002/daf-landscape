# Experiments: specifications and results

**Code:** [`../../models/Daf.Experiments/`](../../models/Daf.Experiments/) (F#), with tests in [`ExperimentTests.fs`](../../models/Daf.Enterprise.Tests/ExperimentTests.fs). The full suite (75 tests, parent plus experiments) passes.

**Regenerate every result:**

```
cd research/ai-native-daf-enterprise/models
dotnet run --project Daf.Enterprise.Cli -- ..
```

The fixed seed is `20261120`, and results are written to [`results/`](results/).

**What these are:**
- **[X] results about models.** Synthetic, seeded, deterministic simulations whose parameters are mostly **assumptions [A]**, listed in each module's `defaults`.
- **E7 is the exception.** It uses **public data**: FY2023 Schedule I filings of 48 of the top-50 sponsors ([evidence note](recipient-overlap-evidence.md)).

An experiment can raise an innovation to **L3 (tested prototype)**. It cannot show that anything works in a real DAF (L4).

**Independent audit:** the experiments were audited in [`../07-adversarial-reviews/adversarial-review.md`](../07-adversarial-reviews/adversarial-review.md) by an agent that did not write them. Its findings are reflected in §12.

**Baseline principle:** every experiment includes the conventional baseline as a deterministic comparator. It also includes at least one adversarial or negative case.

---

## E1: Recipient verification architectures (W1; INN-01, INN-03, INN-34, INN-02)

**Question.** Does a reusable recipient record ("passport") beat per-grant verification, and on which metric?

**Design.**
- 100,000 grants over 12,000 recipients with Zipf(1.0) popularity.
- 0.5% of recipients become ineligible during the year [A].
- IRS data visible at monthly publication [A].
- Manual lookups take 3 minutes with a 1% miss rate [A].

**Metrics:** verification operations, human minutes, escaped ineligible grants, latency.

**Results** ([`results/e1-verification.csv`](results/e1-verification.csv)):

| Architecture | Verification ops | Human min | Escaped (of 491 ineligible grants) | Median latency |
|---|---|---|---|---|
| Manual per grant (baseline) | 100,000 | 300,000 | 23 | 1 day |
| Automated per grant (automation-first) | 100,000 | 0 | 21 | 2 s |
| Passport, naive full refresh each publication | **117,883** | 0 | 21 | ~0 |
| **Passport, diff-driven** (verify once, then process source changes) | **9,759** | 0 | 21 | ~0 |
| Passport refreshed quarterly | 39,294 | 0 | **125** | ~0 |
| Network passport (diff-driven, measured 51.3% overlap) | 4,753 | 0 | 21 | ~0 |

**Findings:**
1. **Accuracy is bounded by the source, not the architecture.** All monthly-refreshed automated designs escape the same 21 grants. These are the *source-latency floor*: changes not yet published by the IRS. No verification design can beat the floor. Only a faster source can.
2. **A naive passport does more work than per-grant lookups.** Most recipients receive less than one grant per refresh period. *The passport idea survives only in its diff-driven form*, which cuts operations by about 90%. INN-01 is amended accordingly.
3. **Slower refresh multiplies escapes.** Quarterly refresh escapes 6× as many grants. Refresh cadence is a governed control parameter.
4. **The passport's value is latency, consistency of evidence and human minutes.** It is not compute; automated lookups are already cheap.

**Maturity:** INN-01/03/34 → **L3** for the work and latency claims. There is no accuracy claim beyond automated lookup.

## E2: Approval architectures with seeded defects (W1/W2; INN-05, INN-06, INN-35; DD-005)

**Design.**
- 200,000 grants; 8% need review (foreign, fiscal sponsor, new organization), per the core proxy (EV-081).
- Seeded defects [A]:

  | Defect | Rate |
  |---|---|
  | Revoked recipient | 0.1% |
  | Sanctions | 0.005% |
  | Undeclared related party | 0.2% |
  | Pledge or ticket benefit | 0.3% |
  | Account takeover | 0.05% |

- Detection probabilities per component (rules, AI flagger, human with and without a dossier) are assumptions shown in code.
- **Adversarial runs:** (a) the revocation rule is silently disabled on days 100–199; (b) prompt injection lowers AI recall on benefit text from 0.7 to 0.2.

**Results** ([`results/e2-approval-architectures.csv`](results/e2-approval-architectures.csv); 1,359 seeded defects):

| Architecture | Human hours | Human cases | Escaped (base) | Escaped (rule disabled) | Escaped (injection) | Rule failure detected |
|---|---|---|---|---|---|---|
| Manual review of all grants (baseline) | 31,972 | 200,000 | 704 | 704 | 704 | day 105 |
| Rules + manual review of all (automation-first) | 31,972 | 200,000 | 646 | 651 | 646 | day 105 |
| **Rules + AI flags → exceptions only (AI-native, flag-only)** | **15,383** | 20,511 | **404** | 450 | **696** | **never** |
| **AI-native + daily canary test cases** | 15,389 | 20,511 | 404 | **404** | 696 | **day 100** |
| Rules only + 2% acceptance sampling, no AI (radical) | 12,532 | 16,221 | 1,069 | 1,115 | 1,069 | never (no sample hit in window) |
| AI-native + shared determinations (ecosystem) | **10,219** | 20,511 | 404 | 450 | 696 | never |
| AI auto-clears 50% of AI-only flags (violates DD-005) | 13,789 | 18,385 | 729 | 775 | 870 | never |
| Pay-first for routine tier, sample after (INN-35) | 15,385 | 20,511 | **1,277** | 1,277 | 1,286 | — |

**Findings:**
1. **Under these assumptions, flag-only AI-native escapes fewer defects than manual review of everything, with half the human hours.** The reason is that per-item human review has low catch rates on related-party and benefit defects [A]. *This depends on assumed human catch rates (0.3, 0.5), which no public data measure (GAP-004).*
2. **Removing per-item review without an AI flagger (radical sampling) is the worst safe design on control effectiveness.** Acceptance sampling at 2% had **no statistical power** against a rare-defect rule failure in a 100-day window. *Contrarian hypothesis INN-06 is weakened:* sampling complements; it does not replace.
3. **A silently broken rule is invisible to flag-only AI.** AI watches the patterns it was given, not rule health. **Daily canaries** (known-bad synthetic grants pushed through the live rules; CTL-046) detect it on the first day and restore escapes to baseline. *New required control:* canary test cases for every deterministic rule.
4. **Prompt injection against the AI flagger raises escapes to manual-review levels** (696 against 704). Flag-only *bounds* AI's downside at "as if the AI were absent". It cannot do worse, because the AI never clears.
5. **Pay-first and AI auto-clear are rejected.** Pay-first escapes 3× more; auto-clear adds about 325 escapes for a 10% saving in hours.
6. **Shared determinations save another 34% of human hours** with no change in escapes.

## E3: Disbursement: netting, remittance key, payee registry (W3; INN-07/08/09)

**Design.**
- 100,000 grants to 12,000 recipients over 250 business days.
- Check share: 33% (from Fidelity's 67% EFT, industry report §2.5) versus 10% with a registry [A].
- ACH $0.30, check $4 [A].
- Recipient matching: 5 minutes without a grant ID, 0.5 minutes with one [A].
- Payee-change fraud: 0.2 changes per recipient per year, of which 2% are fraudulent [A].
- Catch rate: 0.7 for a per-sponsor callback against 0.95 for registry out-of-band checks [A].
- Return rate: 0.5% [A].

**Results** ([`results/e3-disbursement.csv`](results/e3-disbursement.csv)):

| Design | Payments | Payment cost | Recipient hours | Uncaught fraudulent payee changes | Grants per return incident |
|---|---|---|---|---|---|
| Per grant, no key (baseline) | 100,000 | $152,100 | 8,333 | 14.4 | 1.0 |
| Per grant + grant ID in remittance | 100,000 | $152,100 | **833** | 14.4 | 1.0 |
| Daily netting + key | 61,367 | $93,339 | 833 | 14.4 | **1.63** |
| Registry + netting + key | 61,367 | **$41,116** | 833 | **2.4** | 1.63 |

**Findings:**
1. The **grant ID in remittance** cuts recipient-side reconciliation by about 90% [A]. It is the cheapest high-value change, and it moves cost *off* the nonprofit.
2. **Netting cuts payments by 39%** at this concentration. In exchange, each return or failure affects 1.63 grants on average, and more for popular recipients. The total number of grants affected by returns is unchanged.
3. **The payee registry dominates on fraud** (2.4 against 14.4 uncaught changes). It requires two-sided adoption and a neutral operator (see 09), and it must never hold funds (money transmission, regulatory map §14).

## E4: Reconciliation, continuous versus month-end (W11; INN-22)

**Design.** About 4 breaks per day [A]. Investigation takes 15 minutes plus 2 minutes per day of age (evidence decays [A], a stated assumption). A 10-day custodian feed outage is run with and without a missing-feed alarm.

**Results** ([`results/e4-reconciliation.csv`](results/e4-reconciliation.csv)):

| Mode | Mean age at detection | Max age | Human hours |
|---|---|---|---|
| Continuous | 0 days | 0 | 367 |
| Month-end | 15.3 days | 30 | 1,117 |
| Continuous, outage, with missing-feed alarm | 0.03 | 1 | 369 |
| Continuous, outage, no alarm (masked) | 0.2 | **10** | 377 |

**Findings:**
- **Continuous reconciliation cuts break age to zero** and cuts hours by about two-thirds. *The hours effect is entirely driven by the age-cost assumption*; the detection-age effect is mechanical.
- **A silent feed outage silently turns continuous reconciliation back into periodic reconciliation.** A missing-feed alarm is a mandatory companion control.

## E5: Onboarding designs (W12; INN-24, INN-25)

**Assumption-dominated; low confidence.** There are no public abandonment or fraud data.

| Design | Completion [A-derived] | Donor minutes [A] | Synthetic identities reaching first grant per 10k [A] | Data complete when needed [A] |
|---|---|---|---|---|
| Upfront application | 0.69 | 35 | 2.0 | 0.95 |
| Automation-first form with prefill | 0.83 | 15 | 2.0 | 0.95 |
| AI conversational progressive intake | 0.90 | 8 | 2.4 | 0.90 |
| Account at first intent + step-up before first grant | **0.96** | 3 | 2.0 | 0.85 |
| Upstream KYC attestation reuse | **0.96** | **2** | 3.0 | 0.92 |

**Finding.** The radical designs win on completion only because fewer steps compound into fewer drop-offs. Step-up before the first grant keeps fraud exposure at the baseline, because money only moves at the grant. Attestation reuse trades a little fraud detection for speed. **This needs field data; no claim beyond L1.**

## E6: Specialist pooling across sponsors and surge smoothing (W2/W4; INN-28, INN-37)

**Design.** Five sponsors at 20 exception cases per day each, with a December surge of ×3 [A]. Each FTE handles about 8.5 cases per day [A]. The SLA is 2 days.

**Results** ([`results/e6-specialist-pooling.csv`](results/e6-specialist-pooling.csv)):

| Design | Minimum FTE meeting the SLA every day |
|---|---|
| Separate pools per sponsor (baseline) | 35 |
| Shared pool across sponsors (ecosystem) | 33 |
| Separate pools + execution-window smoothing | 25 |
| Shared pool + smoothing | **23** |

**Finding.**
- **Pooling across sponsors barely helps (−6%)** because the surge is *correlated*: everyone's December. Pooling diversifies only noise.
- **Time-shifting demand helps far more (−29%).** Execution windows spread December grants over November and December, and known recipients are pre-cleared in November.
- *INN-28's rationale is weakened; INN-37 is strengthened.* This is a counter-intuitive result worth keeping.

## E7: Cross-sponsor recipient overlap from public filings (W1/W2; INN-02)

Full method in [recipient-overlap-evidence.md](recipient-overlap-evidence.md).

**Coverage:**
- 48 of the top-50 sponsors (Renaissance and BofA file Schedule I as attachments only).
- 279,337 lines and $37.27bn; 133,763 recipients.
- Schedule I lists only domestic recipients over $5,000.

**Results:**
- **71.3% of lines (77.2% of dollars)** go to recipients that another top-50 sponsor also funds.
- A shared record would avoid **51.3%** of sponsor-recipient verifications.
- **Reuse is order-dependent.** The second joiner's reuse is 69.4% if large sponsors join first, 4.3% if small sponsors join first, and 10.0% in random order.

**Finding:** the *mechanism* for network reuse is real (INN-02 → **L2**). Its *cold start* requires the largest sponsors to join first, and those are the sponsors with the least need. Economic value is evaluated in [`../09-economic-validation/`](../09-economic-validation/).

## E8: System-of-record migration, replay versus balance-forward (W8; INN-18, INN-17)

**Design.** Five years of activity in the parent journey model (quarterly contributions, monthly grants). The source system is migrated (a) by replaying the full command/event log and (b) by an opening balance plus the last two years of activity, the pattern AEF's donors experienced (EV-037).

**Results** ([`results/e8-migration.csv`](results/e8-migration.csv)):

| Method | Grants visible | Fund balance | Grants paid visible | History completeness |
|---|---|---|---|---|
| Source | 60 | $300,000 | $300,000 | 1.00 |
| **Replay** | 60 | $300,000 | $300,000 | **1.00** |
| Balance-forward (2 years) | 23 | $300,000 | $115,000 | **0.38** |

**Finding.**
- Replay reproduces every projection exactly (tested).
- Balance-forward preserves the balance but **loses 62% of grant history and $185k of reportable grant history**.
- **INN-18 → L3** within the model. Real systems add schema-semantics risk, which is not tested here.

## E9: Failure recovery after interrupted payment transactions (event catalog §2)

**Design.** Exhaustive: 4 designs × 6 crash points (none; before commit; after commit before send; after send, lost in transit; after the bank executes, acknowledgment lost; duplicate delivery).

**Results** ([`results/e9-crash-recovery.csv`](results/e9-crash-recovery.csv)):

| Design | Correct of 6 | Failures |
|---|---|---|
| Send to bank, then commit | 3 | paid-but-unrecorded ×2; double payment ×1 |
| Commit, then send (no durable outbox) | 3 | lost payment ×2; double payment ×1 |
| Durable outbox, bank does not deduplicate | 4 | double payment ×2 |
| **Outbox + idempotency key at the bank** | **6** | none |

**Finding.** Exactly-once payment needs **both** a durable outbox *and* rail-level idempotency. This makes bank-side idempotency support a **counterparty selection criterion**: banks or rails without it need a reconciliation-based duplicate check before release. *The model is a logical enumeration, not a concurrency test (Phase 2).*

## E10: AI exception triage, flag-only versus auto-close, with distribution shift (DD-005)

**Design.**
- 20,000 exceptions, 5% true defects [A].
- Model score separation is 2 noise units [A].
- Shift case: 30% of defects are a new pattern with weak signal (0.3).
- Human review takes 30 minutes with an AI dossier [A].

**Results** ([`results/e10-ai-triage.csv`](results/e10-ai-triage.csv)):

| Policy | Hours | Escaped defects, base (of 967) | Escaped defects, after shift (of 967) |
|---|---|---|---|
| **Flag-only** | 10,000 | **0** | **0** |
| Auto-close below −1.0 | 8,438 | 0 | **16** |
| Auto-close below 0 | 5,243 | 23 | 118 |
| Auto-close below +1.0 | 1,981 | 159 | 320 |

**Finding.** Any auto-close threshold that saves meaningful time escapes defects, and **a threshold that is "safe" on today's distribution is unsafe after a shift**. That is exactly when nobody knows the model is wrong. **DD-005 (flag-only) is supported at L3.** Its cost is human hours, which the economics must carry.

## E11: Cost comparison across architectures and business models

See [`../09-economic-validation/economic-validation.md`](../09-economic-validation/economic-validation.md).

---

## 12. Summary: what the experiments changed

| Before | After experiments |
|---|---|
| Passport (INN-01) reduces work | Only if **diff-driven**; naive refresh increases work (E1) |
| Acceptance sampling can replace per-item review (INN-06) | Too little statistical power against rare-defect failures; **canaries** are needed (E2) |
| Pooling specialists across sponsors smooths surge (INN-28) | Barely, because surges are correlated; **time-shifting** works (E6) |
| A verification network is a strong business (INN-02) | Mechanism real (E7); economics thin for routine checks, viable for costly determinations (09) |
| Flag-only AI is a governance principle (DD-005) | Also the economically rational choice under shift risk (E10, E2 injection) |
| Exactly-once payments via outbox (parent design) | Needs rail idempotency too (E9) |
