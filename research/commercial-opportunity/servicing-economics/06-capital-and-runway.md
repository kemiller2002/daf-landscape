# 06: Capital and runway

**Date:** 2026-11-25.

**Source:** [`Strategies.fs`](model/src/ServicingEconomics/Strategies.fs) and [`CashFlow.fs`](model/src/ServicingEconomics/CashFlow.fs). The table "Market-entry strategies" in [`model/out/results.md`](model/out/results.md) has every row.

**Status:** theoretical cash plans. Timings, customer sizes and signing dates are assumptions [A]. **No customer, pipeline or signed business exists.**

## 1. How a plan is built

**Formation (month 0).** Founder, CTO and senior engineer start.

**Product build.**
- Base: $60k a month of contract engineering for 12 months ($0.72M), for a narrow, servicing-only scope.
- Variants:
  - x2.5 over 18 months ($1.8M);
  - Unbound-scale build, $5M over 24 months (Unbound's own base; ECH: no DAF application exists today).

**Startup one-time costs: $272k** (CST):
- legal formation and contracts: $80k;
- money-transmission / agent-of-payee opinion: $40k;
- SOC readiness: $20k;
- brand: $15k;
- migration tooling: $40k;
- recruiting: $75k;
- incorporation: $2k.

**Staged hiring.** Controller at month 9; operations specialist at month 12 (Model B). Non-personnel fixed cost runs at 40% before the first go-live.

**First signing at month 12.** Onboarding takes 6 months, at a one-time cost of $105k per sponsor (range $35-325k). Implementation fees are collected half at signing and half at go-live.

**Revenue and cash collection.**
- Fees are billed quarterly in arrears and collected one month later. Cash therefore arrives about four months after go-live, and that working capital is part of the capital figure.
- Handling runs AI-enhanced for the first 12 live months. Delegations and activation gates (Unbound EV-08) take time; the AI-native redesign applies after that.

**Financing and capital.**
- 10% annual cost on negative cash.
- Capital required = the deepest cumulative cash trough, shown with a 25% buffer.

**Cost basis.** Cash costs; founder below-market pay appears only in the Model A plans. An economic-cost variant is shown for comparison.

## 2. Results (20 bps unless stated, payments passed through)

| Plan | Capital (trough) | With 25% buffer | Cumulative cash m6 / m12 / m18 / m24 / m36 | Profitable from month | Run-rate profit at m60 |
|---|---:|---:|---|---:|---:|
| **C anchor:** $1.5B anchor ($300k balance) + two $500M sponsors; Model B | $3.56M | $4.45M | -1.05 / -2.05 / -2.82 / -3.49 / -3.17M | 18 | $2.40M |
| C anchor, founder-led Model A (cash) | $2.67M | $3.34M | -0.85 / -1.64 / -2.13 / -2.51 / -1.67M | 18 | $2.82M |
| Same, at economic cost (founders at market) | $3.01M | $3.77M | | 18 | $2.64M |
| C anchor, signings +6 months | $4.39M | $5.49M | | 24 | $2.40M |
| C anchor, build x2.5 | $4.82M | $6.03M | | 18 | $2.40M |
| C anchor, Unbound-scale build ($5M) | **$8.51M** | $10.64M | | 18 | $2.40M |
| C anchor, AI-enhanced only (redesign never achieved) | $3.68M | $4.60M | | 18 | $1.34M |
| C anchor, AI-native from first go-live | $3.35M | $4.19M | | 18 | $2.40M |
| C anchor, servicer pays payment rails | $3.68M | $4.60M | | 18 | $2.19M |
| **D multiple smaller:** six $300M sponsors ($200k balance) | $5.36M | $6.70M | -1.05 / -2.05 / -2.87 / -3.97 / -5.27M | 30 | $0.67M |
| D, signings +6 months | $6.25M | $7.82M | | 36 | $0.67M |
| D, AI-enhanced only | $7.63M | $9.53M | | not by month 60 | -$0.27M |
| D, Unbound-scale build | $11.41M | $14.26M | | 30 | $0.67M |
| D, 20 bps + $250 per-account floor (about 30 bps effective) | $4.57M | $5.71M | | 30 | $1.93M |
| D, 10 bps + $150 per account | $6.39M | $7.98M | | 38 | $0.22M |
| **B administration first:** three $500M sponsors over 3 years | $5.42M | $6.78M | | 30 | $0.70M |
| **A software first:** eight licences at 4 bps, $80k minimum, 4-person software organization | $5.95M | $7.44M | -1.00 / -1.92 / -2.51 / -3.18 / -4.22M | not by month 60 | -$0.09M |
| A software first, build x2.5 | $7.57M | $9.46M | | not by month 60 | -$0.09M |
| **E partnership:** three $400M partner programs at 14 bps net | $8.54M | $10.67M | | not by month 60 | -$0.60M |

**Normalized comparison** (every plan reaches $1.5B at a $250k balance; ADV-013):

| Plan | Capital | Profitable from month | Run-rate profit at m60 |
|---|---:|---:|---:|
| N-C anchor ($1.0B + $0.5B) | $4.21M | 30 | $0.83M |
| N-B three $500M | $4.69M | 30 | $0.81M |
| N-D five $300M | $5.61M | 33 | $0.38M |
| N-E partnership, 14 bps net | $6.86M | never | -$0.09M |

## 3. Findings

1. **The minimum credible capital is about $2.7-3.6M of cash at the trough** ($3.3-4.5M with a 25% buffer). That assumes all of the following:
   - one anchor-scale customer of about $1.5B signs within 12 months of formation and goes live 6 months later;
   - the product can be built for under $1M;
   - founders accept below-market cash pay (lower end of the range).
2. **The conservative requirement is about $5-8M.** It covers slower sales (+6 months), a portfolio of smaller sponsors instead of an anchor, or a build of $1.8M or more. If the platform build approaches Unbound's own $5M estimate, the requirement is **about $8.5-11.4M**. Build scope is the single largest swing in capital.
3. **Time to revenue is driven by the sales cycle and onboarding, not by the build.** With a 12-month build and a 6-month onboarding, the earliest go-live is month 18 and the first cash is month 21-22. Every 6 months of sales delay adds about $0.8-0.9M.
4. **An anchor customer could fund part of the implementation.** The plans assume a $100k implementation fee. Unbound-scale builds would need far more than any implementation fee observed (TIFIN discloses one-time implementation fees without amounts). A design-partner contract that prepays implementation, or commits to a minimum annual fee from signing, shortens the trough by roughly the prepaid amount.
5. **Software licensing is not an early revenue source at realistic licence prices.** Eight licences at 4 bps with an $80k minimum do not reach profit within 60 months. Unbound's own EV-01 shows break-even needs about 50-100k platform funds, and only about 20 US sponsors hold 5,000 or more accounts. Licensing is a later extension, not the funding engine.
6. **What to staff before each milestone:**

   | Milestone | Required before it |
   |---|---|
   | Product development | Founder, CTO, senior engineer, contract engineering; legal formation |
   | Customer acquisition | Founder-led selling, SOC readiness, insurance binding, sample contracts, money-transmission opinion |
   | First signature | Controller and named compliance arrangements (vCISO, compliance consultant); SOC 2 Type 1 in progress |
   | Onboarding | Operations specialist; migration tooling; parallel-run reconciliation |
   | Commercial activation | Second operations person (dual control), SOC 1/SOC 2 Type 2 windows started, December surge plan, sponsor board delegation |
   | Operational expansion | Step hires per report 05 §6 (operations manager after 4 added staff; integration engineer and implementation analyst per 8 sponsors; fund accountant per 15,000 accounts) |
7. **The separation of development and operations is visible in the cash curve.** About 60% of pre-revenue burn is the development organization (founder, CTO, engineer, build). The operations organization (controller, operations staff, assurance) is hired 3-9 months before the first go-live.
8. **Financing.** The trough includes about $0.1-0.4M of financing cost at 10%. With equity instead of debt the trough is correspondingly lower (ADV-016).
