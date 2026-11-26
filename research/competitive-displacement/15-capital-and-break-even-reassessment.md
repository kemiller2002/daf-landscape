# 15 - Capital and break-even reassessment

Status: research (2026-11-26), **revision 2** after the adversarial review. Model: [model/](model/README.md); outputs [break-even-grid.csv](data/model-outputs/break-even-grid.csv), [entry-route-capital.csv](data/model-outputs/entry-route-capital.csv), [stress.csv](data/model-outputs/stress.csv), [results.md](model/out/results.md) §2-4, §12. Assumptions: [economic-assumptions.csv](data/registers/economic-assumptions.csv). Not an investment recommendation. Monte Carlo: 2,000 seeded triangular draws, reported independent and correlated (ρ=0.5: half the parameters share one adverse quantile).

## 1. Break-even assets at 5-30 bps (AI-native administration, MD-5; $250k balance; 5 sponsors)

| Fee | Operating base | Fully loaded base | MC P10 | MC P50 | MC P90 | Correlated P90 | Never covers variable cost (ind. / corr.) |
|---|---|---|---|---|---|---|---|
| 5 bps | never | never | $31.2B | never | never | never | 77% / 70% |
| 10 bps | $6.58B | $8.00B | $5.23B | $10.2B | never | never | 20% / 25% |
| 15 bps | $2.98B | $3.60B | $2.76B | $4.01B | $12.1B | never | 4% / 10% |
| 20 bps | $1.92B | $2.33B | $1.87B | $2.48B | $4.25B | $7.26B | 1% / 4% |
| 25 bps | $1.42B | $1.72B | $1.41B | $1.80B | $2.67B | $3.54B | 0% / 2% |
| 30 bps | $1.13B | $1.36B | $1.13B | $1.41B | $1.94B | $2.38B | 0% / 1% |

Comparators at 20 bps (operating base / MC P50): conventional administration MD-1 $3.86B / $4.42B (never in 29% of draws); exception-driven MD-4 $1.84B; licensing MD-6 $0.96B / $1.15B (bps-equivalent); hybrid MD-7 $1.45B / $1.77B.

**Reconciliation with prior packages.** PR #86 found $1.1-1.5B (lean) and $1.8-2.3B (fully loaded) at 20 bps; PR #87 a lower bound near $1.0-1.3B. Revision 1 of this model ($1.46B) sat inside that range. **Revision 2 is higher ($1.92B operating, $2.33B fully loaded, P50 $2.48B)** because it adds AI oversight, labour utilisation, field-evidence AI productivity, no automation failure benefit and half-efficacy prevention. The prior packages' lower bounds now look optimistic; the agreement in revision 1 was agreement on shared assumptions, not validation.

## 2. Capital by entry route (120-month horizon; 8% annual churn; go-live lag)

Capital = deepest cumulative cash deficit. Where a route never pays back within 120 months, the figure is a floor.

| Route | Favourable | Base | Adverse | MC P10 / P50 / P90 | No payback within 120 months | Base first cash-positive month | Base payback month | Base ARR at month 60 |
|---|---|---|---|---|---|---|---|---|
| ER-1 Charity intelligence service | $0.79M | $2.33M* | $7.76M* | $1.76M / $2.67M / $4.36M | 93% | 87 | none | $0.41M |
| ER-2 Migration assessment and tooling | $0.31M | never self-funding: ~$0.33M a year net cost | — | — | 100% | none | none | $0.20M |
| ER-3 Compliance evidence and reconciliation | $1.08M | $3.61M* | $8.95M* | $2.33M / $3.42M / $5.28M | 96% | none | none | $0.38M |
| ER-4 White-label licensing, direct | $3.48M | $7.20M* | $23.1M* | $5.98M / $7.64M / $10.2M | 44% | 58 | none (≈ month 116 at P50) | $2.17M |
| ER-5 Full administration (market pay) | $5.21M | $10.3M* | $29.3M* | $8.66M / $10.9M / $14.7M | 78% | 66 | none | $3.21M |
| ER-6 Staged non-custodial services | $1.31M | $4.40M* | $13.4M* | $2.94M / $4.38M / $7.15M | 91% | 95 | none | $0.79M |
| ER-7 Licensing via channel partner | $2.72M | **$5.66M** | $19.3M* | **$4.70M / $5.96M / $8.00M** (corr. $4.34M / $5.83M / $8.69M) | 37% | 52 | 111 | $2.58M |

\* no payback within 120 months in that case; figure is the 120-month floor.

Revision 1 reported a 60-month horizon with no churn or go-live lag; the investor and CFO reviewers showed that understated capital and mixed censored draws into percentiles (CHL-025, CHL-079, CHL-089). Revision 2 corrects both.

PR #87's **$4.5M founder-led** full-administration figure assumes below-market founder pay and an anchor from month 15-18. ER-5 at market pay with revision 2 assumptions needs about **$10.3M base**, and pays back within ten years in only 22% of draws.

## 3. Lowest defensible capital requirement

| Question | Answer | Basis |
|---|---|---|
| Capital to reach a **commercial decision on evidence** (G0) | **about $0.15-0.35M** | [22](22-commercial-validation-plan.md) (V-1..V-9, with a buyer-access line) |
| Capital to **first referenceable paying customer** of a non-custodial wedge (G1) | **about $1.0-1.5M** cumulative, over 12-24 months | Sales cycles of 9-24 months in the target segments (CHL-013); SOC 2 Type 1 and privacy programme (CHL-014, CHL-040) |
| Capital to a **self-sustaining business** | **about $6.5M P50 for the staged path** ($1.0M G0-G1 + ER-7 $6.0M P50 less ~$0.5M build reuse); P90 about $9M; 37% chance of no payback within 10 years | ER-7 with the G0-G1 spend added (CHL-085) |
| Full administration | $4.5M founder-led (PR #87) to $10.3M market pay | ER-5 |

**The lowest defensible capital for a self-sustaining business is about $6-7M (P50), with a P90 near $9M, and only if a channel partner exists** (Low confidence). Non-custodial services alone never become self-funding at the modelled prices; they are evidence-buying spend and should be budgeted as such. The migration assessment is best treated as customer-acquisition cost, not a product (CHL-068, CHL-080).

## 4. Outcome scale

Even when it works, the base channel-licensing route reaches about **$2.6M of annual revenue at month 60** and pays back in month 111. That is a sustainable niche software business, not a venture-scale outcome (CHL-081). The serviceable population is also limited: about 36k licensed accounts are needed to break even at $81, and sponsors with 3-10k accounts sit largely in the segment that switches least (CHL-082). Exit paths are acquisition by an incumbent (Ren, TIFIN, Foundation Source, Foundant), which historically buy small DAF technology firms rather than license them (CLM-025, CHL-087).

## 5. What moves capital most

1. Existence and terms of a channel partner (ER-7 vs ER-4: about $1.7M at P50; partner share 30% assumed, 40-50% plausible, CHL-084).
2. Customer acquisition speed and sales-cycle length (no published CAC in any segment).
3. Fixed burn (team size and pay).
4. Price per customer.
5. Build cost (MSP $1.1-2.4M; full scope $3.6M+; CHL-057).

## 6. Conditions under which the numbers fail

- Average balances near the industry mean of about $141k for any bps-priced administration (CHL-083).
- Fees compressing to 10 bps or less for staffed administration (MD-5 P50 $10.2B).
- No channel partner and direct acquisition near one customer a year (ER-4 adverse $23M).
- Correlated adverse productivity (stress: MD-5 $2.79B at 20 bps).
- Vendor-viability objections from buyers to an undercapitalised vendor (CHL-015, CHL-094), which lengthen every sales cycle.
