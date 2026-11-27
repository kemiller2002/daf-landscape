# 10. Sensitivity, capital and stress

## Monte Carlo
The run uses 2,000 draws with seed 20261127 and triangular ranges. It is run twice: with independent draws, and with a common adverse shock taken with probability 0.5 (about 0.28 pairwise correlation). Volumes are held at base; the factor grid covers volume separately.

| Metric | Base (mode) | P10 | P50 | P90 | P90 (correlated) |
|---|---|---|---|---|---|
| L zero-customer annual cash | $7k | $8k | $24k | $70k | $94k |
| L first-customer annual cash | $202k | $228k | $275k | $346k | $422k |
| F first-customer annual cash | $325k | $356k | $410k | $490k | $586k |
| L marginal per customer (10→25) | $37k | $37k | $47k | $59k | $68k |
| F marginal per customer (10→25) | $89k | $106k | $122k | $141k | $175k |
| L first employee (customers) | 5 | 1 | 1 | 4 | 5 |
| F first employee (customers) | 4 | 1 | 1 | 2 | 3 |
| F cash break-even bps at 10 customers | 7.0 | 8.1 | 9.1 | 10.3 | 13.2 |
| L break-even price per customer at 10 | $57k | $63k | $76k | $90k | $111k |

**The base case sits below the P10 for most metrics** (review findings ADV-A-04 and ADV-P-13). Every range is right-skewed, so the most-likely value of each input combines into an optimistic corner. **Plan on P50; budget for P90.**

## Tornado (largest swings)
**L first-customer annual cash:**
- operating maintenance hours: ±$84k;
- founder hours available: ±$78k;
- keep-qualified maintenance: ±$72k;
- engineering contract rate: ±$70k;
- SOC 2 audit fee: ±$38k;
- security operations: ±$36k;
- founder fixed hours: ±$30k.

**F break-even bps at 10 customers:** operations loaded cost and the grant-exception human share each swing about ±0.7 bps.

Full table: [`tornado.csv`](data/outputs/tornado.csv).

## Capital to self-sustaining operation
The growth path ([`capital.csv`](data/outputs/capital.csv)) runs as follows:
1. **Pre-revenue:** the zero-customer platform for 6/12/24 months.
2. **Go-live:**
   - first-customer onboarding, hypercare and acquisition;
   - prepaid assurance and insurance;
   - 3/6/12 months of first-customer run-rate before the first invoice (SOC 2 observation, coverage, evidence).
3. **Growth:** two customers added a year, each charged onboarding.

| Model, mix (base, 2 customers a year) | Build cash | Go-live | Deepest cumulative deficit | Self-sustaining |
|---|---|---|---|---|
| L, anchor first | $108k | $172k | **$0.20M** | Year 2 (4 customers) |
| F 20 bps, mixed | $108k | $269k | **$0.28M** | Year 1 (2 customers) |
| F 20 bps, anchor first | $108k | $376k | $0.38M | Year 1 |
| L, mixed | $108k | $170k | **$0.76M** | Year 4 (8 customers) |
| W, mixed | $108k | $160k | $0.96M | Year 6 |
| T, mixed | $108k | $214k | $1.24M | Year 6 |
| L, all mid-size | $108k | $170k | $1.34M | Year 8 (16 customers) |
| F 20 bps, all mid-size | $108k | $269k | $0.64M | Year 3 |
| L, all small | $108k | $170k | $2.35M | Year 14 |
| F 20 bps, all small | $108k | $265k | never within 15 years | — |
| C, mixed | $52k | $121k | $1.12M | Year 15 (30 subscribers) |
| M, mixed | $25k | $23k | $27k | Year 1 |

**Corners.**
- **Every input favourable:** most routes need under $0.1M.
- **Every input adverse at once** (highest costs, lowest prices, fewest founder hours): no route becomes self-sustaining within 15 years. Licensing accumulates about $8.6M by year 5 and full service about $13M.

The adverse corner is a joint worst case, not a forecast; the probability of every input sitting at its worst end together is negligible. It shows that the business only works if prices are well above the tested low end. The growth rate is held at two customers a year in the corners because faster growth helps when customers are profitable and hurts when they are not.

## Stress: correlated failure
These events cluster in practice: a December surge (19.5% of grants; 3× load), a severity-1 incident, and the founder unavailable at the same time. The tier-1 configuration covers them as follows:
- **Incident command:** the secondary on-call (a regular contractor or a retainer) takes over.
- **Approvals:** two non-author reviewers can approve control-module changes without the founder.
- **Break-glass:** two holders are available without the founder.
- **Not covered:** a 24×7 bench of three or more non-founder people. That is the tier-2 rule COV-ONC24, about +$80–160k a year, which bank-grade contracts may demand.

Regional loss is recovered from cross-region backups within about 24 h. A one-hour regional recovery needs the tier-2 warm standby (+$1.3k a year), which Unbound does not require (CNV-ARC-001 declares a nonzero cross-region RPO).

**Correlated cost risk** (the ρ = 0.5 run) widens first-customer P90 by about $76–96k a year.
