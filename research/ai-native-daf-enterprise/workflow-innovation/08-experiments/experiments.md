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

**Independent audit (governing).** An agent that did not write the experiments audited them in [`../07-adversarial-reviews/adversarial-review.md`](../07-adversarial-reviews/adversarial-review.md) §5. Its central finding stands: **most results follow from the chosen parameters rather than from the mechanism tested.** This document was revised in response (2026-11-20). Fixes were applied where the audit found modeling errors. Where a result is parameter-driven, it is labeled as such, and the sensitivity run that removes it is shown.

| Exp. | Audit status after revision | What it can support |
|---|---|---|
| E1 | internal-demonstration; network arm removed | Source-latency floor and diff-driven work count (arithmetic); no accuracy advantage |
| E2 | internal-demonstration; ranking parameter-driven | Flag-only bounds AI downside; canaries detect a silent rule failure; sampling-only is worse. *Not* that AI-native beats manual on both cost and control |
| E3 | netting count mechanistic; registry arm = parameters | Netting reduces payment count by recipient-day concentration; grant-ID value depends on assumed minutes |
| E4 | hours = one assumption; detection age mechanical | Continuous detection is earlier; the hours saving is not evidenced |
| E5 | **not an experiment** (assumption table) | Nothing beyond L1 |
| E6 | smoothing arm fixed (deferral to January) | Correlated surges limit pooling; deferral reduces peak FTE, *if* donors accept execution windows |
| E7 | public data; the one external evidence | Overlap of recipient pairs (mostly cheap-to-check large charities); costly-work overlap unmeasured |
| E8 | specification plus illustration | Replay preserves history *by construction*; shows the loss from balance-forward |
| E9 | specification of required semantics | Exactly-once needs outbox *and* counterparty dedupe; ACH has no end-to-end key, so dedupe depends on the originating bank's API |
| E10 | flag-only arm fixed (human misses modeled) | Auto-close adds escapes beyond human misses, more after distribution shift |


**Baseline principle:** every experiment includes the conventional baseline as a deterministic comparator. It also includes at least one adversarial or negative case.

---

## E1: Recipient verification architectures (W1; INN-01, INN-03, INN-34)

**Design.**
- 100,000 grants over 12,000 recipients with Zipf(1.0) popularity.
- 0.1% of recipients become ineligible per year [A], revised from 0.5% after the audit. The revocation-share evidence is 0.082% of dollars.
- IRS data visible at monthly publication [A]; manual lookups take 3 minutes with a 1% miss rate [A].

**Results** ([`results/e1-verification.csv`](results/e1-verification.csv)):

| Architecture | Verification ops | Human min | Escaped / ineligible grants |
|---|---|---|---|
| Manual per grant (baseline) | 100,000 | 300,000 | 2 / 23 |
| Automated per grant | 100,000 | 0 | 2 / 23 |
| Passport, naive full refresh | 117,883 | 0 | 2 / 23 |
| Passport, diff-driven | 9,701 | 0 | 2 / 23 |
| Passport refreshed quarterly | 39,294 | 0 | 8 / 23 |

**What this supports (audit-adjusted):**
- Automated designs share the same escapes *by construction*, so the "source-latency floor" is a definitional point. It is still an important design point: accuracy depends on the source's publication cadence, and refresh cadence is a governed parameter.
- "Ops" are machine reads, so diff-driven versus per-grant is a pricing artifact. Automated lookups are already cheap.
- **The passport's value lies in latency, consistent dated evidence and fewer human lookups, not in compute.**
- The planned adversarial cases (poisoned refresh, name collision) were **not built**.
- **The network arm was removed.** It applied the measured 51.3% as a constant, while reuse per joiner is order-dependent (4–81%). Network value is computed from the measured curve in [`../09-economic-validation/`](../09-economic-validation/).

## E2: Approval architectures with seeded defects (W1/W2; INN-05, INN-06, INN-35; DD-005)

**Design.**
- 200,000 grants; 8% need review (EV-081). Seeded defects [A]:

  | Defect | Rate |
  |---|---|
  | Revoked recipient | 0.1% |
  | Sanctions | 0.005% |
  | Undeclared related party | 0.2% |
  | Benefit | 0.3% |
  | Account takeover | 0.05% |

- Detection probabilities are assumptions in code.
- Adversarial runs: a silently disabled revocation rule (days 100–199), and prompt injection (AI recall on benefit text falls to 0.2).
- Sensitivity runs added after the audit: AI recall set equal to human catch rates, and a 1-minute routine manual review.
- A cost bug in the pay-first arm was fixed: sampling is now charged on every sampled grant.

**Results** ([`results/e2-approval-architectures.csv`](results/e2-approval-architectures.csv); 1,359 seeded defects):

| Architecture | Hours (base) | Escaped (base) | Escaped (AI recall = human) | Hours (1-min manual review) | Escaped (rule disabled) | Escaped (injection) |
|---|---|---|---|---|---|---|
| Manual review all | 31,972 | 704 | 704 | 15,306 | 704 | 704 |
| Rules + manual all | 31,972 | 646 | 646 | 15,306 | 651 | 646 |
| Rules + AI flags → exceptions (flag-only) | 15,383 | 404 | **651** | **15,383** | 450 | 696 |
| Flag-only + daily canaries | 15,389 | 404 | 651 | 15,389 | **404** | 696 |
| Rules + 2% sampling, no AI | 12,532 | **1,069** | 1,069 | 12,227 | 1,115 | 1,069 |
| Flag-only + shared determinations | 10,219 | 404 | 651 | 10,219 | 450 | 696 |
| AI auto-clear (violates DD-005) | 13,789 | 729 | 866 | 13,789 | 775 | 870 |
| Pay-first (INN-35) | 15,750 | 1,277 | 1,293 | 15,444 | 1,277 | 1,286 |

**What this supports (audit-adjusted):**
1. **The AI-native advantage is parameter-driven.**
   - When AI recall equals human catch, control is the same as rules plus manual review of everything (651 against 646), at about half the hours.
   - When manual review takes only 1 minute, hours are the same and control is better.

   It wins on *one* criterion in each sensitivity, but **does not dominate on both independently of assumptions**. Which side holds depends on unmeasured human catch rates and review minutes (GAP-001, GAP-004).
2. **Flag-only bounds the AI's downside.** Under prompt injection, escapes rise to 696, about the level of manual review of everything (704). Auto-clear goes beyond that, to 870.
3. **Sampling-only is the worst safe design** (1,069 against 704 for manual review of everything). INN-06 does not survive as stated (audit verdict).
4. **A silently disabled rule is invisible to flag-only AI. Daily canary test cases detect it on day 1** and restore escapes. The detection day is set by construction, and the fix lag of 1 day is assumed. The *control requirement* is the finding: every deterministic rule needs known-answer canaries.
5. **Shared determinations save hours at unchanged escapes** *by construction*, because reuse is applied only to clean reviews. The 50% reuse share is assumed.
6. **Pay-first and auto-clear are rejected.** Pay-first is a partial straw man: it ignores the passport lookup INN-35 assumed. It is rejected primarily on law, because a sponsor decision must precede payment, not because of E2.
7. **Not modeled:** an adaptive fraudster, correlated AI misses, and reviewer automation bias.

## E3: Disbursement: netting, remittance key, payee registry (W3; INN-07/08/09)

**Results** ([`results/e3-disbursement.csv`](results/e3-disbursement.csv)): see the CSV.

**What this supports (audit-adjusted):**
- **Netting** cuts payments from 100,000 to 61,367 at this concentration. That is mechanistic (distinct recipient-days) and the one robust result.
- **Grant ID in remittance** cuts recipient matching from 8,333 to 833 hours *by assumption* (5 against 0.5 minutes).
- **Registry fraud and check-share gains are pure parameters.** They vanish at parity, so they are **not evidence**.
- The total number of grants affected by returns is identical across designs, so "netting widens impact" is definitional. Only the grants per incident change, from 1 to 1.63.
- **Not built:** a registry-compromise blast-radius model, and the case where a bank strips addenda.

## E4: Reconciliation, continuous versus month-end (W11; INN-22)

The rounded-uniform break generator was replaced by a Poisson generator.

| Mode | Mean age at detection | Hours (2 min/day age penalty [A]) | Hours (no age penalty) |
|---|---|---|---|
| Continuous | 0 | 370.5 | 370.5 |
| Month-end | 15.5 | 1,136.8 | **370.5** |

**What this supports (audit-adjusted):**
- **The entire hours saving comes from one unsourced assumption.** Without it the two modes cost the same.
- Earlier detection (0 against 15.5 days) is mechanical and is the only supported claim.
- The missing-feed alarm arm assumes a manual fallback within a day, which is not modeled explicitly.
- **E4 is not evidence for INN-22's cost benefit.**

## E5: Onboarding design table (W12; INN-24, INN-25): not an experiment

The audit is correct: `(1 − abandonment)^steps` over a hand-entered table returns its inputs. [`results/e5-onboarding.csv`](results/e5-onboarding.csv) is retained only as a **scenario table** documenting the assumptions a field test would need to measure. It supports nothing beyond L1.

## E6: Specialist pooling and surge smoothing (W2/W4; INN-28, INN-37)

The smoothing arm was corrected. It previously moved December demand into November, which is a causality error. **Execution windows now defer half of the December excess into January**, which is the only direction a donor-accepted window allows. Pre-clearing known recipients in November (the INN-37 narrative) is not modeled.

| Design | Minimum FTE meeting a 2-day SLA every day |
|---|---|
| Separate pools | 35 |
| Shared pool | 34 |
| Separate pools + deferral windows | 25 |
| Shared pool + deferral windows | 23 |

**What this supports (audit-adjusted):**
- Pooling across sponsors gains little when surges are correlated. The audit notes the remaining gain is mostly integer-FTE granularity, so pooling matters mainly for *small* sponsors that cannot staff even one specialist.
- **Deferral windows cut peak FTE by about 29% *if* donors accept that December recommendations may execute in January.** Grant timing has no donor tax effect (the deduction occurred at contribution), but acceptance is untested. INN-37 remains **insufficient evidence** pending donor research.

## E7: Cross-sponsor recipient overlap from public filings (W1/W2; INN-02)

See the [evidence note](recipient-overlap-evidence.md).

**Results:**
- 71.3% of lines (77.2% of dollars) go to recipients another top-50 sponsor also funds.
- A shared record would avoid 51.3% of sponsor-recipient verifications.
- The second joiner's reuse is 69.4% if large sponsors join first, 4.3% if small sponsors join first, and 10.0% in random order.

**Audit-adjusted reading:**
- **The overlap is concentrated in large, well-documented charities.** These are exactly the recipients that are cheapest to verify from free IRS and OFAC files.
- **The costly work is not in the data:** bank verification, foreign equivalency (Schedule F), and fiscal-sponsor review.
- So E7 shows that *pairs* recur. It **does not show that costly verification recurs**. INN-02 is **insufficient evidence** (audit), kept at L1 with the overlap premise documented.

## E7b: Does costly verification recur? (run after the audit; tests its central objection to INN-02)

**Data:** the same FY2023 edges, restricted to recipients needing human work rather than a free lookup. Script: [`scripts/workflow_innovation_costly_overlap.py`](../../../../scripts/workflow_innovation_costly_overlap.py). Output: [`data/workflow-innovation/costly-recipient-overlap.csv`](../../../../data/workflow-innovation/costly-recipient-overlap.csv).

Foreign recipients **cannot be tested**: Schedule F Part II reports regions, not recipient names.

| Recipient class | Recipients | Sponsor-recipient pairs | Funded by ≥2 top-50 sponsors | Pair verifications a shared record would avoid |
|---|---|---|---|---|
| All recipients | 133,763 | 274,929 | 40.1% | 51.3% |
| **Fiscal sponsors** (repository 433-EIN list) | 183 | 1,024 | **73.8%** | **82.1%** |
| **Recipients absent from the IRS EO BMF** (identity or status needs a person) | 17,114 | 24,377 | 24.7% | **29.8%** |

**Finding:**
- **Host-level fiscal-sponsor diligence recurs heavily** across sponsors. That is costly work, and it is reusable.
- **Unlisted-recipient resolution recurs much less** (30%).
- **Project-level review of a fiscal-sponsor grant** (what the hosted project is; whether it is earmarked to a non-charity) varies per grant, so it is not reusable by this measure.
- **INN-02 is supported narrowly:** a shared network has evidence for *fiscal-sponsor host diligence* and partial evidence for *unlisted-recipient resolution*. It has no evidence for foreign equivalency.
- The overlap premise for those classes moves to **L2**. Value per reuse remains assumed.

## E7c: Do sponsors outside the top 50 gain more? (OUTSTANDING B2, run 2026-11-23)

**Data.** The public FY2023 Schedule I returns (FY2024 as fallback) of every FY2024 DAF sponsor outside the top 50 that files a Form 990.
- Universe: 1,464 sponsors.
- **1,285 itemise Schedule I**, giving 224,271 sponsor–recipient pairs and 146,838 distinct recipients.
- 308 have no itemised lines and 54 file Schedule I only as an attachment. These are mostly the smallest sponsors, so the results describe *itemising* small sponsors.

**Script and outputs.**
- Script: [`scripts/workflow_innovation_small_sponsor_overlap.py`](../../../../scripts/workflow_innovation_small_sponsor_overlap.py). It uses the same exclusions and keys as E7.
- Data: [`data/workflow-innovation/small-sponsor-overlap-summary.csv`](../../../../data/workflow-innovation/small-sponsor-overlap-summary.csv) and the pair file `sponsor-recipient-edges-small-fy2023.csv`.
- Economics: [`../09-economic-validation/results/small-sponsor-network.csv`](../09-economic-validation/results/small-sponsor-network.csv).

**Share of a sponsor's distinct recipients already on another sponsor's Schedule I** (pooled across sponsors / median sponsor):

| Group | Sponsors | Median recipients | On a top-50 record | On any other sponsor's record | On another *small* sponsor's record |
|---|---|---|---|---|---|
| Top 50 (reference, against the other top 50) | 48 | n/a | 71% / 76% | n/a | n/a |
| Rank 51–200 | 141 | 362 | 62% / 64% | 71% / 73% | 56% / 57% |
| Rank 201–500 | 292 | 118 | 42% / 55% | 51% / 65% | 40% / 48% |
| Rank 501+ | 852 | 18 | 50% / 38% | 61% / 50% | 52% / 40% |
| All small | 1,285 | 37 | 54% / 48% | 63% / 59% | 50% / 45% |

**Costly classes (E7b repeated on small sponsors' recipients):**
- **Fiscal sponsors** (433-EIN list): 1,051 small-sponsor pairs, of which **92% are already on a top-50 record**. Host diligence is highly reusable for the long tail.
- **Recipients whose EIN is absent from the current IRS EO BMF**: 16,346 small-sponsor pairs, of which **only 25% are already on a top-50 record**.
  - The BMF extract postdates the FY2023 returns, so some of these absences are later revocations, not unresolvable identities.
  - The hard identity cases of small sponsors are mostly local and not shared.

**Findings**
1. **The hypothesis that small sponsors gain most per member is not supported in reuse share.** The median sponsor ranked 501+ finds 38% of its recipients on a top-50 record, against 76% for the median top-50 sponsor. Small sponsors fund more local recipients that no one else has verified.
2. **Their gain may still matter more to them, but the data cannot show that.** They have the least verification capacity. That is a statement about the value of a reuse, which public data cannot measure.
3. **In aggregate the long tail roughly doubles the network's work avoided** (09 §4b). However, the median small member saves only $370–$1,800 a year. Membership must therefore be near-free, or bundled into a platform, rather than sold.
4. **Seeding from the top 50 matters.** Small sponsors reuse about 1.7× more joining a network the top 50 seeded than joining one of small sponsors only.

## E8: Migration, replay versus balance-forward (W8; INN-18): specification plus illustration

Replay equality is determinism of one engine: a specification, not a test of migration across heterogeneous systems. The balance-forward comparison illustrates history loss (0.38 completeness, $185k of grant history not visible) against the pattern AEF donors experienced (EV-037). The baseline omits "history delivered as documents", a fairer comparator. INN-18 stays at **L2**: premise evidenced, prototype only by construction.

## E9: Failure recovery after interrupted payments: specification

The result is the hand-coded table. It is valid as a **specification of required semantics**: exactly-once needs a durable outbox *and* counterparty deduplication.

**Load-bearing caveat (audit):** ACH has no end-to-end idempotency key, so deduplication depends on the originating bank's API. Banks without it need a pre-release duplicate check, which makes this a counterparty-selection criterion. Key expiry, netted-batch recomposition and partial acceptance are not modeled.

## E10: AI exception triage, flag-only versus auto-close (DD-005)

Flag-only previously hard-coded zero escapes. Human reviewers now miss 5%, consistent with E2.

| Policy | Hours | Escaped (base, of 967) | Escaped (30% new weak-signal pattern) |
|---|---|---|---|
| Flag-only | 10,000 | 57 (human misses) | 57 |
| Auto-close below −1.0 | 8,438 | 57 | **73** |
| Auto-close below 0 | 5,243 | 80 | 171 |
| Auto-close below +1.0 | 1,981 | 209 | 365 |

**What this supports.** Auto-close adds escapes beyond human misses. A threshold that adds none on today's distribution (−1.0) adds 16 after a shift. This supports DD-005 **directionally**. Dossier minutes (45 → 30) and automation bias are assumed or not modeled.

## E11: Cost comparison

There is no separate E11 code. The cost comparison is [`../09-economic-validation/economic-validation.md`](../09-economic-validation/economic-validation.md), using `NetworkEconomics.fs` and the parent cost model. The audit found about 10 documents citing "E11" as if it were a built experiment; read those citations as pointing to 09.

## Experiments cited in design documents but NOT built

The audit, §6 item 3, lists these. Where the design catalogs and workflow files cite them, they are **planned, not executed**:

| Citation | Planned experiment | Status |
|---|---|---|
| "E5 complex-asset queue" (INN-11, W4, XW-14) | Queue model of pre-underwritten acceptance against bespoke review | not built |
| "E6 contact model" (INN-14, W5, XW-23) | Contact-volume model of shared-state servicing | not built; needs contact-centre logs |
| "E6 liquidity" (INN-27, D-INV-3, XW-16, XW-31) | Pipeline forecast against buffer | not built; the parent twin covers a buffer, not a forecast |
| "E2 back-test" (INN-21, XW-24) | Policy compiler back-test on a historical decision corpus | not built; needs partner history |
| "E2 evidence completeness" (D-W10-3) | Evidence coverage test | parent PoC asserts evidence records only |
| E1, E2, E3 adversarial extensions (W1–W3 §7) | Poisoned refresh; stale determination; registry hijack blast radius | not built |

## Summary: what the experiments changed, after audit

| Before | After experiments and independent audit |
|---|---|
| Passport (INN-01) reduces work | Only if diff-driven; the value is latency and evidence, not compute |
| Sampling can replace per-item review (INN-06) | **Does not survive**; canaries required for rule health |
| Pooling across sponsors smooths surge (INN-28) | Weak when surges are correlated; matters for small sponsors' indivisibility |
| Surge smoothing (INN-37) | Deferral cuts peak FTE ~29% in the model; donor acceptance unknown, so insufficient evidence |
| Verification network (INN-02) | Pair overlap real; costly-work overlap unmeasured, so insufficient evidence; economics thin for routine checks |
| AI-native approval dominates manual | **Not robust:** equal control at half the hours, or equal hours with better control, depending on unmeasured parameters |
| Flag-only AI (DD-005) | Supported directionally (E2 injection, E10 shift) |
| Exactly-once payments | A specification: requires counterparty dedupe, which ACH lacks natively |
| Continuous close saves labor | Not evidenced; only earlier detection is |
