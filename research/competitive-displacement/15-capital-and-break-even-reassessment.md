# 15 - Capital and break-even reassessment

Status: research (2026-11-26). Model: [model/](model/README.md); outputs [break-even-grid.csv](data/model-outputs/break-even-grid.csv), [entry-route-capital.csv](data/model-outputs/entry-route-capital.csv), [results.md](model/out/results.md) §2-4 and §12. Assumptions: [economic-assumptions.csv](data/registers/economic-assumptions.csv). Not an investment recommendation. Monte Carlo: 2,000 seeded triangular draws per item; parameters independent (ASSUMPTION; correlated draws would widen the tails).

## 1. Break-even assets at 5-30 bps (AI-native administration, MD-5)

| Fee | Base ($250k balance, 5 sponsors) | MC P10 | MC P50 | MC P90 | Draws where fee never covers variable cost |
|---|---|---|---|---|---|
| 5 bps | $15.1B | $11.6B | $54.3B | never | 40% |
| 10 bps | $3.68B | $3.59B | $4.87B | $10.9B | 3% |
| 15 bps | $2.10B | $2.11B | $2.57B | $3.65B | 0.2% |
| 20 bps | $1.46B | $1.48B | $1.74B | $2.21B | 0% |
| 25 bps | $1.13B | $1.14B | $1.31B | $1.59B | 0% |
| 30 bps | $0.91B | $0.92B | $1.06B | $1.25B | 0% |

Conventional administration (MD-1) for comparison: 20 bps base $2.11B (P50 $2.44B; never in 16% of draws); 10 bps never covers cost in 79% of draws. Licensing (MD-6) in bps-equivalent: 20 bps $0.85B; 10 bps $1.80B; 5 bps $4.08B.

**Reconciliation with prior packages.** PR #86 found $1.1-1.5B (lean) and $1.8-2.3B fully loaded at 20 bps; PR #87 found a lower bound of about $1.0B operating and $1.3B with the MSP platform. This model's $1.46B base / $1.74B P50 sits inside that range from an independent bottom-up event build, so the order of magnitude is now supported by three methods. All three share the same unmeasured inputs (touch rates, minutes, fixed costs), so agreement is not validation.

## 2. Capital by entry route (60-month horizon)

Capital = deepest cumulative cash deficit. Where a route never turns cash-positive within 60 months, the figure is the 60-month deficit, i.e. **a floor, not a total**.

| Route | Favourable | Base | Adverse | MC P10 | MC P50 | MC P90 | Never cash-positive in 60 months | Base first positive month |
|---|---|---|---|---|---|---|---|---|
| ER-1 Charity intelligence service | $0.68M | $1.98M* | $4.36M* | $1.57M | $2.16M | $2.95M | 68% | — |
| ER-2 Migration assessment and tooling | $0.28M | $1.87M* | $3.55M* | $1.23M | $1.80M | $2.42M | >99% | — |
| ER-3 Compliance evidence and reconciliation service | $0.92M | $2.73M* | $5.13M* | $2.03M | $2.73M | $3.58M | 77% | — |
| ER-4 White-label licensing, direct | $2.75M | $6.17M | $13.8M* | $5.15M | $6.53M | $8.61M | 18% | 49 |
| ER-5 Full administration (market pay) | $4.22M | $8.82M | $17.2M* | $7.42M | $9.22M | $11.8M | 37% | 55 |
| ER-6 Staged non-custodial services | $1.14M | $3.66M* | $7.73M* | $2.61M | $3.67M | $5.07M | 61% | — |
| ER-7 Licensing via channel partner | $2.13M | $4.84M | $11.4M* | $4.03M | $5.06M | $6.78M | 13% | 43 |

\* never cash-positive within 60 months in that case; figure is the 60-month deficit.

PR #87's **$4.5M founder-led** full-administration figure assumes founders at below-market pay and a $0.5-1.0B anchor from month 15-18; ER-5 at market pay needs about $8.8M base (CLM-030). Both are kept: the difference is a choice about founder compensation and anchor timing, not a modelling disagreement.

## 3. Lowest defensible capital requirement

There are three different questions:

| Question | Answer | Basis |
|---|---|---|
| Capital to reach a **commercial decision on evidence** (gates G0-G2) | **about $0.35-0.75M** | Validation plan [22](22-commercial-validation-plan.md) (V-1..V-7) plus PR #87 gates 1-2 ($0.6-0.75M incl. some build) |
| Capital to **first recurring revenue** from a non-custodial service | **about $0.7-1.2M** cumulative | ER-1/ER-6 build + 9-12 months of burn (favourable-to-base) |
| Capital to a **self-sustaining business** | **about $5M (P50; P10 $4.0M, P90 $6.8M)** via channel-partner licensing; $6.5M direct licensing; $4.5M founder-led / $8.8M market-pay full administration | ER-7, ER-4, ER-5 |

**The lowest defensible capital for a business that can stand on its own is about $4-5M, not lower** (Low confidence; channel partner unverified). Non-custodial services alone do not become self-sustaining at assumed prices and volumes (CLM-028); they are evidence-buying spend, and should be budgeted as such.

## 4. What moves capital most

1. **Customer acquisition speed** (customers per year) and **time to first revenue**: distribution, not technology (HYP-001).
2. **Fixed burn** (team size and pay).
3. **Price per customer** (licence $81-150 per account; service $15-120k a year).
4. **Build cost** (MSP $1.1-2.4M; PR #87). Agent-assisted development multiples remain unmeasured (PR #87 RC-AN-015).

## 5. Conditions under which the numbers fail

- Average balances below about $150k at a bps price (administration never breaks even below about $100k at ≤30 bps in MD-1, and needs $2.1B in MD-5 at 20 bps).
- Fees compressing toward 5-10 bps for staffed administration (MD-5 P50 $4.9B at 10 bps).
- No channel partner and direct CAC near the $125k assumption with 1 customer a year (ER-4 adverse: $13.8M).
- AI and prevention effects absent (prevention scale 0: +$0.1B break-even; touch rates ×2: +$0.1B) — material but not decisive; fixed cost and balance dominate.
