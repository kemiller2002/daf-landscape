# 07: Minimum viable organization

**Sources:** the integrated model (sections 2-6 of [`model/out/results.md`](model/out/results.md); designs in [`Designs.fs`](model/src/CapitalMinimization/Designs.fs)); OPS ([06](06-workload-driven-staffing.md), [`responsibility-matrix.csv`](../../../data/commercial-opportunity/ai-native-capital-minimization/responsibility-matrix.csv)); ADV2-004/-005/-021 ([16](16-adversarial-review.md)). All parameters are labelled assumptions. No organization has been observed.

## Designs evaluated

Six designs of 1, 2, 3, 5, 6 and 9 core people. Each has:
- skill pools: operations, accounting, compliance, donor service, engineering;
- a hiring threshold: an employee is hired once residual need reaches 0.75 FTE, and residual need below that is bought fractionally at a 50% premium;
- coordination cost beyond six pairs;
- a named compliance owner floor of 0.25 FTE;
- December release capacity: half of the operations December excess is carried by year-round staff;
- an itemised non-personnel floor.

| Design | Core | Fixed annual cost | At $1B (5 sponsors, 4,000 accounts, 50 min): employees / contracted FTE / total cost / margin | Live money (CNV-GOV-003) |
|---|---|---|---|---|
| F1 one founder + agents + contractors | 1 | $1.14M | 1 / 5.3 / $2.07M / -3.7% | **No**: one authorised person |
| F2 two founders | 2 | $1.27M | 2 / 5.1 / $2.13M / -6.3% | **No**: one authorised person (the technical founder has no bank access) |
| F3 three core: founder, CTO, controller | 3 | $1.46M | 6 / 1.7 / $2.22M / -10.8% | **Yes**, once operations hires exist, with a contracted independent reconciler |
| F5 five core: + engineer, operations specialist | 5 | $1.73M | 7 / 1.8 / $2.36M / -17.9% | Yes |
| F6 six core: + compliance and service specialist | 6 | $1.83M | 8 / 1.5 / $2.51M / -22.6% | Yes |
| F8+ nine core, specialised | 9 | $2.22M | 10 / 1.4 / $2.66M / -33.2% | Yes |

Break-even at 20 bps, 5 sponsors, $250k average balance (model section 3):

| Design | Operating (30 / 50 min) | Standalone with MSP platform (30 / 50 min) | Standalone + steady-state adjustments (30 / 50 min) |
|---|---|---|---|
| F3 | $1.05B / $1.15B | $1.44B / $1.62B | $1.59B / $1.78B |
| F5 | $1.12B / $1.26B | $1.49B / $1.67B | $1.64B / $1.85B |
| F8+ | $1.30B / $1.43B | $1.67B / $1.84B | $1.82B / $2.03B |

## Findings

1. **Smallest safe live servicing organization: three core people plus workload hires.**
   - The three core are a founder or managing director, a technical lead with no bank access, and a controller or head of financial operations.
   - Operations hires come as soon as accounts exist: at $1-1.5B, three to four. A contracted independent reconciler sits outside the payment chain.
   - Two code approvers are contracted (CNV-PLT-010).
   - At $1.5B that is about 7 employees and 1-2 contracted FTE. It is **not** a three-person company in operation.
   - Before the auditor and sponsor boards accept the deterministic release gate, CNV-GOV-003 requires three distinct people per payment. A sponsor-provided third person counts as transferred work.
2. **One or two founders cannot run live money.** F1 and F2 are admissible only as **pre-launch build organizations**: product build, buyer and auditor evidence, design-partner preparation.
   - Their low reported break-evens ($0.94-1.09B operating) are not achievable operations.
   - They depend on 5 FTE of contractors, on sponsors approving releases, and on a single point of failure.
3. **The non-personnel floor is about $0.65M a year whatever the headcount.** It covers:
   - audit, tax, SOC 2, SOC 1 and penetration testing;
   - cyber, E&O, D&O and crime insurance;
   - vCISO, compliance consultant, counsel and bookkeeping;
   - cloud and data;
   - sales events and marketing.

   AI does not remove it. A narrow non-custodial service avoids only SOC 1 and crime cover.
4. **Larger core teams cost more than they save until about $3B.** Specialisation (F8+) adds about $0.5M of fixed cost over F3 and raises break-even by about $0.2B. Its benefit is resilience and absence cover, not cost.
5. **What happens before hiring employees.** F1 or F2 with agents and contractors can do the following:
   - build the minimum servicing product: about $1.94M at 1.5x, $1.1-2.4M range;
   - run gates 1-2: buyer price test, licence terms, counsel opinion, auditor conversation, design partner, shadow replay and engineering spike;
   - operate a **non-custodial** service: charity verification or migration tooling.

   They cannot hold, release or reconcile charitable money.

## Conditions

These results hold at:
- 20 bps;
- $250k average balances;
- five equal sponsors;
- no time-study evidence for minutes.

Under a value-based price at high balances (about 7 bps; report 10), no design breaks even below about $3.8B.
