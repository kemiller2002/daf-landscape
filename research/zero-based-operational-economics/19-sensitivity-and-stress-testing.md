# 19 — Sensitivity and stress testing

Outputs: [`sensitivity-tornado.csv`](data/model-outputs/sensitivity-tornado.csv), [`named-scenarios.csv`](data/model-outputs/named-scenarios.csv), [`monte-carlo-cost.csv`](data/model-outputs/monte-carlo-cost.csv), [`monte-carlo-break-even.csv`](data/model-outputs/monte-carlo-break-even.csv), [`stress.csv`](data/model-outputs/stress.csv), [`founder-sensitivity.csv`](data/model-outputs/founder-sensitivity.csv), [`policy-levers.csv`](data/model-outputs/policy-levers.csv). Reference: full administration, $500M, 1 sponsor (View 1 base $2.20M with analytic staffing; $2.22M simulated).

## 1. Largest drivers (one at a time, View 1 at $500M)

| Parameter | Low → high | View 1 at low / high |
|---|---|---:|
| Handling minutes multiplier | 0.7 → 1.6 | $1.78M / $2.84M |
| Exception-rate multiplier | 0.6 → 2.0 | $2.07M / $2.52M |
| Fixed-cost quotes multiplier | 0.8 → 1.5 | $2.12M / $2.42M |
| Activity (grants, contributions per account) | 0.6 → 2.06 | $2.17M / $2.42M |
| Max dedicated utilisation; productive hours | | $2.20M / $1.96M |
| Hire step (0.5 vs 1 FTE) | | $2.02M / $2.20M |
| Management ratio | 5% → 15% | $2.13M / $2.27M |
| Founder hours | 0 → 800 | $2.27M / $2.13M |
| AI handling factor | 0.6 → 0.97 | $2.18M / $2.21M |
| Infrastructure multiplier | 0.7 → 1.5 | negligible |

Handling time and exception rates — both unmeasured — dominate. AI and infrastructure do not matter at this scale.

## 2. Scenarios (all parameters at one level simultaneously; corner cases are deliberately implausible bounds)

| Scenario | Vendor hours | View 1 | View 2 | View 3 |
|---|---:|---:|---:|---:|
| Optimistic (all low; founder 800 h) | 1,372 | $0.29M | $0.45M | $0.90M |
| Expected | 7,200 | $2.20M | $2.39M | $3.18M |
| Conservative (activities base, parameters high) | 19,626 | $6.42M | $6.53M | $7.32M |
| Severe (all high; founder 0 h) | 73,469 | $23.5M | $23.7M | $25.0M |

## 3. Monte Carlo (300 draws; independent and correlated ρ = 0.5)

| AUA | View 1 P10 / P50 / P90 | View 2 P50 | View 3 P50 | Correlated View 1 P90 |
|---|---|---:|---:|---:|
| $100M | $1.73M / $1.99M / $2.34M | $2.19M | $2.98M | $2.56M |
| $500M | $2.06M / $2.43M / $2.89M | $2.63M | $3.41M | $3.25M |
| $1B | $2.63M / $3.17M / $3.81M | $3.37M | $4.16M | $4.29M |

The MC median sits above the base case (asymmetric ranges: handling and exception multipliers have long upper tails). Break-even P50 $2.04B (P10 $1.44B, P90 $4.10B) for full administration.

**What the Monte Carlo does not vary** (review ADV-BI-019): fee level, sponsor count and size, CAC, churn, time to revenue. These are covered by the deterministic grids and stresses, not by distributions — there is no defensible distribution for them.

## 4. Stress at $1B with four sponsors (full administration, 20 bps)

| Case | Revenue | View 1 | Margin |
|---|---:|---:|---:|
| Base | $2.00M | $3.17M | −$1.17M |
| Market decline 30% | $1.40M | $3.17M | −$1.77M |
| Loss of largest sponsor (40% of assets) | $1.20M | $2.56M | −$1.36M |
| Net withdrawals 15% | $1.70M | $3.17M | −$1.47M |
| Inactive accounts double | $2.00M | $2.74M | −$0.74M |

With four $250M sponsors, $1B is not viable under full administration at 20 bps in any case.

## 5. Founder availability

| Founder hours | View 1 at $500M | Break-even (cash, $250M sponsors) |
|---:|---:|---:|
| 0 | $2.27M | $2.85B |
| 400 (base) | $2.20M | $2.85B |
| 1,200 | $1.87M | $2.47B |

## 6. Answers

- **Largest economic drivers:** sponsor size and count; mean balance; handling minutes; exception rates; the fixed engineering and assurance floor.
- **Assumptions most capable of invalidating the model:** (1) exception rates and handling minutes (unmeasured; ±$0.5M); (2) engineering workload (a 4-engineer floor is a judgement from the inventory and review); (3) small sponsors at the same per-sponsor workload as large ones; (4) 20 bps being achievable for full administration.
- **Operational bottlenecks:** engineering at 90% utilisation; compliance in December (24-48 h SLAs); founder commercial capacity.
- **Minimum viable scale under adverse conditions:** conservative parameters at $500M already cost $6.4M — above 20 bps revenue on any plausible book under $3B.
- **When full administration is uneconomic:** sponsors under ~$100M; mean balances under ~$100k; retail and payroll programmes at AUA fees; any book below ~$1.3B at 20 bps.
- **When licensing is preferable:** whenever the sponsor already has operations staff, sponsors are small, or balances are low — priced per account ($150-250).
- **When shared infrastructure changes the result:** shared *engineering* across Echelon products would (≈ −$0.3-0.5M); shared *cloud* infrastructure would not (infrastructure is under 1% of cost).
