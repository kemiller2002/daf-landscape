# 18 — Break-even analysis

Outputs: [`break-even.csv`](data/model-outputs/break-even.csv) (7 configurations × 8 balances × 3 views × 7 fees, with and without investment recovery), [`break-even-by-sponsor-size.csv`](data/model-outputs/break-even-by-sponsor-size.csv), [`monte-carlo-break-even.csv`](data/model-outputs/monte-carlo-break-even.csv), [`policy-levers.csv`](data/model-outputs/policy-levers.csv). Break-even is the smallest account count from which profit stays non-negative for every larger grid point (step costs make "first crossing" misleading). Grid resolution ≈ 15%; repeated values are grid points.

## 1. Definitions

| Break-even | Cost covered |
|---|---|
| Cash | View 1 incremental cash, recurring |
| Operating (allocated) | View 2: adds founder time and allocated shared Echelon resources |
| Standalone | View 3: replaces every shared capability |
| With investment recovery | adds one-time investment amortised over 5 years (cash: $0.57M; economic: $1.94M build + readiness + legal) |

## 2. Full administration (CFG-5) at 20 bps — by balance (one sponsor per $500M)

| Mean balance | Cash | Allocated | Standalone | Allocated + investment |
|---:|---:|---:|---:|---:|
| ≤ $50k | never (≤ $5B) | never | never | never |
| $100k | $9.8B | $9.8B | $11.3B | $11.3B |
| **$250k** | **$1.85B** | **$1.85B** | **$2.85B** | **$2.47B** |
| $500k | $1.36B | $1.57B | $2.09B | $2.09B |
| $1M | $1.32B | $1.32B | $1.76B | $1.53B |

## 3. Full administration at 20 bps — by sponsor size ($250k balance)

| Sponsor size | Cash | Allocated | Standalone |
|---:|---:|---:|---:|
| $25M-$100M | never | never | never |
| $250M | $2.85B | $2.85B | $4.38B |
| $500M | $1.85B | $1.85B | $2.85B |
| $1B | $1.61B | $1.85B | $2.47B |

**Break-even depends more on sponsor size than on anything else in the model.** Below about $100M per sponsor, each sponsor's own recurring cost (~$145k) consumes most of its fee and the platform never covers its floor at 20 bps.

## 4. Fee sensitivity (full administration, $250k balance, cash view)

| Fee | 10 bps | 15 bps | 20 bps | 25 bps | 30 bps | 40 bps |
|---|---:|---:|---:|---:|---:|---:|
| Break-even AUA | $13.8B | $3.3B | $1.85B | $1.20B | $0.90B | $0.59B |

## 5. Licensing with support (CFG-2) — for completeness

At 20 bps (an unrealistic price for software; [17](17-revenue-models.md) §3): $0.90B cash at $250k. Priced per account at $150: ≈ 41,500 accounts; at $250: ≈ 13,200 accounts. With $100M sponsors: $1.6B; $50M sponsors: $5.1B.

## 6. Uncertainty (Monte Carlo, 200 draws, one sponsor, balance $100k-$500k)

| Config | View | P10 | P50 | P90 |
|---|---|---:|---:|---:|
| CFG-5 | Cash | $1.44B | **$2.04B** | $4.10B |
| CFG-5 | Allocated | $1.62B | $2.23B | $4.37B |
| CFG-5 | Standalone | $2.26B | $2.99B | $5.40B |
| CFG-5 | Cash, correlated (ρ 0.5) | $1.37B | $2.14B | $3.85B |
| CFG-2 | Cash | $0.87B | $1.11B | $1.39B |

## 7. Answers

**Q13. What is the break-even at 20 bps?** For full administration with a $250k mean balance and $500M sponsors: **≈ $1.85B cash, $1.85B allocated, $2.85B standalone** (MC P50 $2.0B cash; P10-P90 $1.4-4.1B). That is essentially the original $1.92B.

**Q14. How does it change with average balance?** Strongly: $1.3B at $1M balances, $1.85B at $250k, ~$10B at $100k, never below ~$50k — because cost follows accounts and revenue follows assets.

**Cash break-even versus investment recovery.** Investment recovery adds roughly 0-35% depending on view and grid step. Payback of the $0.57M one-time cash takes under a year once above break-even; recovery of the $1.94M economic build value needs a margin the model reaches only above ~$2.5B.

## 8. What would move break-even materially

| Lever | Effect on CFG-5 cash break-even ($500M sponsors) |
|---|---|
| Measured exceptions 40% lower after prevention | $1.85B → $1.61B |
| Combined levers (author + one approver, founder 1,200 h, low-end quotes, cheaper infrastructure, exceptions −40%) | → **$1.39B** |
| Platform engineering shared with other Echelon products in production (inference, not modelled) | roughly −$0.3B |
| Fee 25 bps instead of 20 | → $1.20B |
| Mean balance $500k instead of $250k | → $1.36B |
| $1B sponsors instead of $500M | → $1.61B |

The author-plus-two change-approval rule alone has no effect: engineering workload already requires four engineers.
