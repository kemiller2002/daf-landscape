# 11. Adversarial review and reconciliation

Three independent reviewers challenged the committed pre-review baseline (`92c0aff`). Each worked from the files alone, without the author's conclusions:

| Reviewer | Perspective | Findings | Material |
|---|---|---|---|
| Pessimist | Former regulated-fintech operations head and SOC auditor: hidden founder labour, mandatory controls, coverage, support, DR, correlated failures | 25 | 13 |
| Anti-conventional optimist | Bootstrapped regulated-software founder: expenses introduced without necessity, automation, wrong-party costs; told explicitly not to remove necessary controls | 29 | 15 |
| Model auditor | Investment-committee model auditor: mechanics, double counting, attribution, break-even, capital, like-for-like comparisons | 25 | 16 |

**Every finding is recorded with its disposition, rationale and resulting change** in [`adversarial-findings.csv`](data/registers/adversarial-findings.csv). The raw reviews are in [`data/evidence/adversarial/`](data/evidence/adversarial/).

| Disposition | All | Material |
|---|---|---|
| Accepted | 33 | 21 |
| Partially accepted | 34 | 18 |
| Rejected | 12 | 4 |

## Engine defects found and fixed
Several were found independently by two or three reviewers.

| Defect | Found by | Effect | Fix |
|---|---|---|---|
| Founder counted as a qualified person in every role, even with zero hours in it | ADV-P-03, ADV-A-07 | Understated limited-operations and full-service coverage by ~$40k | Founder counts only where the founder works |
| Contractors never counted toward coverage | ADV-O-02 | Overstated retainers by ~$65–100k at one customer | A regular contractor (≥ 400 h) counts as one person |
| One new customer forced every year at every count | ADV-O-11, ADV-A-05 | Put ~$59k of onboarding into steady state at one customer | Expected-value onboarding; growth costed in the capital path |
| Forced hires did not take work from the founder | ADV-A-06 | Overstated limited-operations and full-service cost by ~$51k | Forced employees absorb work first |
| Break-even was first crossing, on one customer order | ADV-A-02, ADV-A-03 | "L breaks even at 7" held only for one mix | Persistent break-even for every mix |
| Capital stopped at the first invoice | ADV-A-01, ADV-A-08, ADV-P-06 | Understated capital about six-fold | Growth path to self-sustaining operation, with go-live costs |
| Whole build amortised to charity intelligence and migration | ADV-A-15 | Overstated their fully loaded cost | Per-model qualification |
| Base case reported as if central | ADV-A-04, ADV-P-13 | Base sits below P10 | Answers headline P50 and P90 |

## Where the two opposed reviewers met
**Platform maintenance.**
- The pessimist cited a maintenance norm of 15–25% of build effort and proposed 1,500 h.
- The optimist cited AI-assisted maintenance and the absence of any automation credit for engineering, and proposed 400 h.
- **Reconciled at 500/900/1,800 h**, split into keep-qualified work (which runs with no customers) and operating work. This is the largest remaining uncertainty.

**On-call.**
- The pessimist proposed $70k.
- The optimist proposed $9k, triggered only when a response objective is contracted.
- **Reconciled on the incident.io standby benchmark at $28k**, at the typical-contract tier.

**Change review.**
- The pessimist proposed $40k per reviewer, for emergency availability.
- The optimist proposed $8k, on ~40 h of workload.
- **Reconciled at $12k** (workload plus an availability clause).

**Year-one SOC 2.** The optimist proposed a Type I plus a bridge letter. **Rejected:** institutional buyers commonly require a current Type II, and a bridge letter only covers gaps after an existing report. Run-rate keeps the annual Type II.

## Reviewers who introduced conventional expense
Per the mission, proposals that added conventional organisational cost without established necessity were challenged:
- **ADV-P-08** (a 3–4-person non-founder 24×7 bench at tier 1): **rejected**. Tier 1 already gives non-founder cover for incidents and approvals. The bench is the tier-2 rule COV-ONC24.
- **ADV-P-12** (800 h of product enhancement): **rejected as an obligation** and reported as discretionary (~$96k a year).
- **ADV-P-18** (a warm standby region at tier 1): **rejected**. CNV-ARC-001 declares a nonzero cross-region RPO.
- **ADV-A-19** (a financial-statement audit): **rejected**. No lender or investor requires one.

## Reviewer claims checked against primary sources and rejected
- **ADV-O-22** (no phone at release 1): Unbound decision XID-SVC-005 reads "support live phone integration, callback and async; activation by sponsor". The phone line stays as a typical contractual cost under full service.

## Net effect (licensing, base)
| | Pre-review | Reconciled |
|---|---|---|
| Zero-customer cash | $44.6k | $7.1k (P50 $24k) |
| First-customer cash | $306k | $202k (P50 $275k) |
| First employee | 4 customers | 5 (median: the first customer) |
| Capital (mixed) | $118k excluding build (incomplete) | $0.76M deepest deficit, plus $108k build cash |
| Break-even (mixed) | 7 customers | 7 (anchor-first: 1; all mid-size: 211) |
