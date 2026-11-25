# 06: Workload-driven staffing and handling-time targets

**Pass:** OPS (parts 3-4), integrated in model sections 4-6. **Data:**
- [`handling-targets.csv`](../../../data/commercial-opportunity/ai-native-capital-minimization/handling-targets.csv);
- [`workload-tails.csv`](../../../data/commercial-opportunity/ai-native-capital-minimization/workload-tails.csv);
- [`staffing-capacity.csv`](../../../data/commercial-opportunity/ai-native-capital-minimization/staffing-capacity.csv) (11 roles).

**Integrator conclusions**
- **Handling time is a small cost.** At 50.7 minutes, labour is about $55 of $877 revenue per account-year (6%).
- **Handling-time targets:**
  - The servicer floor is about **11.7 minutes** per account-year. About 9 of those minutes are legal, independence or control work.
  - 10 minutes is infeasible without weakening control.
  - 20 is reachable only with every lever plus transfers.
  - About 30 is a plausible steady state.
  - 45-75 is realistic in each sponsor's first year, before board delegation.
  - In the model, F5 at $1B goes from 1.7% loss at 10 minutes to 17.9% loss at 50 and 43.1% loss at 100 (section 4). At $1.5B, F5 standalone break-even moves from $1.49B at 30 minutes to $1.67B at 50 (section 3).
- **December, not the annual average, sets headcount above about 5,000 accounts** [OPS].
  - Temporary staff cannot release payments.
  - The integrated model now makes year-round release-capable employees carry half the December excess (ADV2-003).
- **Ratio-based and workload-driven staffing compared (model section 6).** Workload-driven staffing does **not** save money once December release capacity is respected.
  - F5 costs $0.06M less than the previous ratio model at 2,500 accounts.
  - It costs $0.1M more at 5,000-10,000 accounts and $0.5-1.9M more at 20,000-40,000.
  - **This corrects the previous study:** its ratio triggers understated December headcount.
- **Real drivers replace the ratios:**
  - Accounting scales with sponsor books, feed sources and break rates, not accounts.
  - Integration scales with distinct counterparties and their change rate.
  - Implementation scales with new sponsors on a learning curve.
  - Compliance needs a named owner from go-live (modelled as a 0.25 FTE floor).
  - Platform change control needs three engineers able to approve (author plus two), employees or contracted (CNV-PLT-010).
- **Tails** (model section 5, $1.5B):
  - A tail-heavy book (minutes ×2) moves F5 break-even to $2.10B.
  - December plus an incident plus an absence moves it to $1.77B.
  - The severe combined stress has no break-even below $20B.

> The research-pass content below was produced by a role-separated agent pass from the same model family as the integrator; it is not independent validation. Labels: [S] sourced, [A] assumption, [D] derived, [E] estimate, [M] measured (the pass ran it). Figures quoted inside pass sections are the pass's own; where the integrated model differs, the preface says so and the model ([`model/out/results.md`](model/out/results.md)) governs.

## Part 3: Handling-time targets, lower bound, tails and peaks

Each target below uses Model B fixed cost and a simplified break-even sensitivity.

| target min/acct-yr | feasibility | FTE per 10k accts | labour $/acct-yr | break-even (simplified) |
|---|---|---|---|---|
| 10 | infeasible at market mix without weakening control | 1.22 | 10.91 | $0.93B |
| 20 | theoretically reachable, not demonstrable; needs every lever plus transfers | 2.44 | 21.82 | $0.94B |
| 30 | plausible steady-state design point after redesign (this pass) | 3.65 | 32.72 | $0.96B |
| 50 | prior AI-native base (50.7); achievable without most transfers | 6.09 | 54.54 | $0.98B |
| 75 | realistic during pre-delegation (year 1 of each sponsor) | 9.14 | 81.81 | $1.02B |
| 100 | failure case: redesign not achieved (AI-enhanced is 124) | 12.18 | 109.08 | $1.06B |

**Theoretical lower bound (servicer):** about **11.7 minutes per account-year at market mix** [D from A], plus sponsor-level work of 1.3-3.2 at 10,000-4,000 accounts per sponsor, and **2.7 sponsor-appointed minutes**.
- **Irreducible on legal, independence or control grounds:** about 9.0. This covers exception dossiers and decisions, flag clearing, sanctions dispositions, ER/ED review, complex-gift packets, dual authorization, break resolution, independent sampling and controller sign-off.
- **Irreducible because of uncertainty or service by right:** fraud, succession, complaints and requested human service, accessibility accommodations, residual paper.
- **Excluded:** engineering, sales, management and onboarding, which are fixed or per-event.

**Segments and tails (after redesign):**
- routine accounts: 15.59 minutes;
- high-frequency grantmakers: 80 (7% of accounts carry about 18% of minutes);
- high-value: 64;
- complex contribution: 150 minutes per gift, of which 90 are irreducible;
- international/ER grant: 25 minutes per grant;
- accessibility accommodation: 30 minutes per case, **deliberately not reduced**;
- fraud/compliance investigation: 120 minutes per case, not reduced (monitoring raises detection volume).

**Workload percentiles:**
- **p50 account:** 23 minutes;
- **p90:** 64 (within-archetype high 227);
- **p99:** 188 (high 482).

The archetype step distribution is assumed; no account-level distribution has been observed.

**December stress** (10,000 accounts, 4 sponsors, core 5 FTE sized on annual minutes x 1.15):

| scenario | Dec minutes | peak-day minutes | core FTE needed (clear in 10 Jan days) | outcome at core 5 |
|---|---|---|---|---|
| average working day (annual sizing) |  | 1408.0 | 4.29 | none |
| December, no disruption | 83867.3 | 5903.3 | 10 | backlog 51,035 min at 31 Dec; 107.3 January working days to clear |
| December with 2 prep-only surge | 83867.3 | 5903.3 | 9 | backlog 37,902 min at 31 Dec; 79.7 January working days to clear |
| December + 2-day AI outage in peak week | 90707.03 | 9323.17 | 10 | backlog 44,742 min at 31 Dec; 94.0 January working days to clear |
| December + AI outage + one core ops absent for peak week | 90707.03 | 9323.17 | 11 | backlog 47,040 min at 31 Dec; 98.9 January working days to clear |
| December + AI outage + absence + 5-day feed incident | 94707.03 | 10123.17 | 12 | backlog 51,040 min at 31 Dec; 107.3 January working days to clear |

**Annual-average sizing cannot absorb December.** The 31 December backlog would take months of January spare capacity to clear.

**Sensitivity at 10,000 accounts (core FTE needed):**

| Surge FTE | Clear in 10 days | Clear in 20 days | Clear in 40 days |
|---|---|---|---|
| 2 | 9 | 8 | 6 |
| 4 | 8 | 7 | 6 |
| 6 | 8 | 6 | 5 |

**What is legally time-critical:**
- sanctions reports (10 business days);
- complaint acknowledgment (2 business days);
- contemporaneous acknowledgments, which only need to precede the donor's filing.

Year-end grant payment is a service expectation, not a legal deadline. **A sponsor-agreed deferral policy** (for example, non-urgent exceptions and statements shifted into January) is therefore the main peak lever, and it is a service-level transfer that must be disclosed.

**Combined stress:** AI outage, absence and a vendor incident together raise December minutes by about 13% and break dual control unless a second releaser is pre-appointed.

## Part 4: Workload-driven staffing (replacing prior triggers)

How each prior trigger is replaced:

| Prior trigger | Replacement |
|---|---|
| Ops manager after 4 added ops staff | Dedicated manager when human headcount across ops, accounting and compliance reaches 7 or more, or founder coordination time exceeds 0.3 FTE (span 6-8 [A]). Self-coordinating case workflows (assignment, clocks and escalation in the case kernel, CNV-SVC-001) remove status-chasing, **not** people management, rostering or the December readiness gate. |
| Integration engineer per 8 sponsors | Driven by **distinct counterparties** (banks, custodians, ERPs) and their change rate: FTE = (new adapters x 280 h + live adapters x 30 h) / 1,520 [A]. Integration work declines with reuse only when new sponsors share counterparties; a sponsor with a new bank resets the curve. |
| Implementation analyst per 8 sponsors | Driven by **new** sponsors per year with an 85% learning curve [A]: onboarding(n) = 9,000 + 9,000 x n^-0.234, plus 7,000 migration minutes. Live sponsors add little. |
| Fund accountant per 15,000 accounts | **Accounting scales with a combination:** sponsor books (monthly close and sign-off), new feed sources (100% calibration for one close cycle) and transactions x break rate. It does not scale with accounts. Break work is under 0.4 FTE even at 50,000 accounts [D from A]; the controller constraint is sponsor books (roughly 60-75 per controller-year [E]). |
| Compliance officer above 10,000 accounts | A **named fractional owner from go-live** (OFAC obligations do not wait for scale); employ when compliance minutes exceed 0.5 FTE or a contract requires it. |

**New lines the prior model lacked:**
- **independent reviewer:** S x 1888 minutes per year at n=59;
- **three-person engineering change-control floor** (CNV-PLT-010);
- **pre-contracted December surge;**
- **sponsor-side appointees:** at least 2 per sponsor, exclusive, not servicer staff.

**Servicing FTE (all queue roles) by scale:**

| accounts | sponsors | min/acct | annual sizing | December sizing | recon breaks FTE | independent review FTE | implementation FTE |
|---|---|---|---|---|---|---|---|
| 3000 | 2 | 30.11 | 2 | 3 | 0.02 | 0.05 | 0.3 |
| 5000 | 3 | 30.11 | 3 | 5 | 0.04 | 0.07 | 0.3 |
| 10000 | 4 | 30.11 | 5 | 9 | 0.07 | 0.09 | 0.3 |
| 20000 | 6 | 30.11 | 10 | 18 | 0.14 | 0.14 | 0.59 |
| 50000 | 10 | 30.11 | 23 | 46 | 0.35 | 0.23 | 0.87 |
| 5000 | 3 | 50.72 | 5 | 8 | 0.04 | 0.07 | 0.3 |
| 10000 | 4 | 50.72 | 8 | 15 | 0.07 | 0.09 | 0.3 |
| 20000 | 6 | 50.72 | 16 | 31 | 0.14 | 0.14 | 0.59 |

**Reading.**
- Below about 3,000 accounts, floors bind.
- From about 5,000 accounts, December sizing roughly doubles servicing headcount over annual sizing.
- The redesign (30 vs 50.7 minutes) saves about 3-13 servicing FTE between 5,000 and 20,000 accounts on December sizing. That is where minutes genuinely matter, but only well above the prior break-even scale (about 2,200-3,000 accounts).
