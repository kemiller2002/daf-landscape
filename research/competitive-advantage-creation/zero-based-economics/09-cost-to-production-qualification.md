# 09. Cost of reaching production qualification (kept separate)

The operating model assumes Unbound is complete and production-qualified. This report estimates what reaching that state costs ([`qualification.csv`](data/inputs/qualification.csv)). It is shown separately from operating cost and enters only the fully loaded view, amortised over 3/5/7 years. Each item is amortised only to the models that need it (review finding ADV-A-15).

**Current state:** a PostgreSQL slice exists (`unbound/execution/README.md`), but nothing is deployed or audited.

| Item | Founder hours (low/base/high) | Cash (low/base/high) | Models |
|---|---|---|---|
| Ledger, fund accounting and continuous reconciliation | 1,200 / 2,200 / 3,800 | — | L W T F |
| Grant lifecycle, policy gate, holds, payment-rail integration | 1,000 / 1,900 / 3,400 | — | L W T F |
| Charity intelligence pipeline and sanctions screening | 300 / 600 / 1,100 | — | L W T F C |
| Donor, advisor and sponsor experiences; partner API | 900 / 1,700 / 3,000 | — | L W T F |
| Tenancy, keys, evidence engineering, hardening | 300 / 600 / 1,100 | — | L W T F C |
| Independent review of control modules | 40 / 80 / 160 | $15k / $30k / $60k | L W T F |
| Pre-launch pen test and remediation | 40 / 80 / 160 | $8k / $15k / $30k | L W T F C |
| SOC 2 Type I readiness and audit | 80 / 160 / 320 | $5k / $12k / $25k | L W T F C |
| CPA review of the ledger design | 20 / 40 / 80 | $5k / $15k / $30k | L W T F |
| Counsel: MSA, DPA, TPSP role, data rights | 20 / 40 / 80 | $10k / $25k / $60k | all |
| Benchmark, load and DR rehearsal | 80 / 160 / 320 | $2k / $5k / $10k | L W T F |
| AI development tooling during the build | — | $2k / $6k / $15k | L W T F |
| **Total (platform models)** | **3,980 / 7,560 / 13,520** | **$47k / $108k / $230k** | |
| Commercial validation (G0), modelled and not authorised | 200 / 400 / 800 | $0 / $5k / $20k | |
| Partner pilot parallel run (G1), modelled and not authorised | 200 / 400 / 800 | $0 / $10k / $30k | |

## Findings
1. **Cash is small and time is large.** At the $123/h market rate, 7,560 founder hours are worth about $0.93M, giving a fully loaded build of **$1.04M** against Phase II's $1.94M.
2. **At 1,200 h a year this is over six years of founder time.** Even at 1,800 h a year it is four years. The real decision is how many founder-years to commit, or whether to buy part of the build. A contracted build at $120/h would turn the 7,560 hours into about $0.9M of cash.
3. **Uncertainty is wide.** The hours are workload estimates for an AI-assisted build. No productivity measurement exists. The 3,980–13,520 h range spans the PR #87 range when converted at market rates.
4. **Charity intelligence alone needs about 1,480 founder hours and $52k of cash.** Migration services depend on Transitus, whose build is outside this package.
