# 05: Financial model and sensitivity

**Date:** 2026-11-25.

**Model:** [`model/`](model/), F# on .NET 10. It is research tooling, not product code.

**Full generated results:** [`model/out/results.md`](model/out/results.md) (sha256 `b8328e3b…`). Per-sponsor re-costing is in [`sponsor-model-economics.csv`](../../../data/commercial-opportunity/servicing-economics/sponsor-model-economics.csv).

**Status:** theoretical. Every output follows from labelled parameters in [`Parameters.fs`](model/src/ServicingEconomics/Parameters.fs) and the [assumptions register](../../../data/commercial-opportunity/servicing-economics/assumptions-register.csv). There is no time study, no signed contract and no measured operation. Nothing here is a forecast or a demonstration of commercial profitability.

## 1. What the model computes

| Element | Definition |
|---|---|
| Revenue | Asset fee: average billable assets x bps / 10,000, per account archetype. Optional per-account floor, flat per-account fee, sponsor minimum and buyer cap on the average per account. |
| Account archetypes | Six archetypes (inactive, small recurring, typical, high-frequency, high-value, complex-asset) with their own balances, minutes, vendor cost, payment cost and December share. Source: ACT pass, AI-native base. |
| Archetype rescaling | The mix is rescaled to each sponsor's observed average balance. Workload scales with balance^0.34, derived from the archetypes (ADV-009). |
| Human hours | Account workload plus sponsor-level work (close, configuration, incidents, audit support, governance: 324 h per sponsor-year AI-native), x complexity multiplier x stress factor. |
| Capacity | Core roles' servicing share x 1,520 productive hours x 90% utilisation. Added ops staff = whole FTEs above capacity (step), with a minimum for separation of duties (Model A 2, Model B 1). |
| December | Archetype December shares (about 0.18-0.33 of annual minutes). Demand above one month's capacity is bought at the loaded rate. |
| Fixed and step costs | Core payroll at economic cost; non-personnel and contracted lines from the cost register; step rules (operations manager, integration engineer, implementation analyst, fund accountant, compliance officer) triggered by added FTE, live sponsors or accounts, never by assets. |
| Boundary | Payment rails pass through at cost and complex-asset intermediary fees are fund-borne (base). Sponsor-retained reserved decisions ($42-43 per account) are excluded. |
| Profit | Operating profit = revenue - all costs. Contribution margin excludes core payroll, fixed non-personnel and step costs. |
| Fully loaded variant | Adds $1.0M a year of platform build amortisation (Unbound's $5M base over five years) and $250k a year of sales and acquisition. |
| Searches | Break-even and target-margin assets on a $10M grid to $20B, reporting the sustained crossing; minimum bps (0.1 bp steps); minimum contractual fee per sponsor. |
| Cash flow | Monthly, 60 months: staged hiring, build spend, startup costs, onboarding, implementation fees (half at signing, half at go-live), fees billed quarterly in arrears and collected one month later, 10% financing cost on negative cash, 12-month AI-enhanced lag before redesign applies. |

**Tests.** `dotnet test tests/ServicingEconomics.Tests` passed 28/28 on 2026-11-25. They cover:
- exact reproduction of the prior memo's table, its 30%-shock loss and its closed-form break-even;
- linearity, minimum-fee, floor and buyer-cap semantics;
- capacity steps, utilisation and the December premium;
- costs that do not fall when only assets fall;
- workload elasticity, effective bps and the pass-through boundary;
- billing timing, implementation-fee timing and the redesign lag.

**Determinism.** Two consecutive runs produce byte-identical output.

## 2. The prior model reproduced, then replaced

The prior memo's H0 (F = $1,177,750 and v = $75 per account, uncapped capacity) reproduces exactly: at $1B and B = $200k, revenue is $2.0M, cost $1.553M and profit $0.447M. Its break-even of $725M ($200k balance) rests on four assumptions this mission overturned:

1. **Fixed cost is too low.** It is $1.66M base for the same roles, or $1.74M with the second operations person that dual control needs (report 03).
2. **Labour is $65.45/h, not $50.** Variable cost by archetype ranges from $9 to $790 per account-year (report 04).
3. **Capacity was unlimited.** In reality it is stepped and seasonal.
4. **There was no build or sales cost.**

## 3. Break-even and target-margin assets

**Basis:** Model B lean (5 core), AI-native, average billable assets, 20 bps; five equal sponsors unless noted. Each cell gives the asset level at which the margin is first sustained; ranges span $150k / $250k / $500k average balances.

| Scenario | Break-even | 10% | 20% | 25% | 30% |
|---|---|---|---|---|---|
| Model B, one sponsor | $0.90-1.09B | $1.00-1.21B | $1.13-1.68B | $1.27-1.81B | $1.37-2.02B |
| Model B, five sponsors | $1.14-1.46B | $1.32-1.76B | $1.49-2.06B | $1.59-2.21B | $1.71-2.45B |
| Model A founder-led, five sponsors (economic cost) | $1.01-1.28B | $1.13-1.49B | $1.27-1.83B | $1.36-1.96B | $1.53-2.19B |
| Model C established, five sponsors | $1.47-1.67B | $1.64-1.87B | $1.85-2.18B | $1.98-2.48B | $2.19-2.75B |
| Model B fully loaded (build + sales), five sponsors | $1.83-2.29B | $2.09-2.61B | $2.36-3.16B | $2.60-3.57B | $2.97-3.91B |
| Model B, one sponsor, AI-enhanced only (redesign not achieved) | $1.02-1.95B | $1.19-2.52B | $1.51-3.53B | $1.61-4.27B | $1.81-5.83B |
| *Prior memo H0 (B = $200k)* | *$0.725B* | | | *$1.047B* | |

**Readings:**
- **Break-even at 20 bps is about $1.1-1.5B** of average billable assets for a lean organization. It rises to **about $1.8-2.3B** once build amortisation and sales are carried. That is 1.6-3x the prior memo's figure.
- **Sustainable profitability at 20 bps** (20-25% fully loaded margin) **needs about $2.4-3.6B**.
- **Scale is not the only lever.** The account balance is roughly as important: books averaging $500k reach every margin about $0.3-0.8B sooner than $150k books.
- **More sponsors cost more.** Every additional sponsor adds about 324 hours a year of sponsor-level work and per-sponsor step costs (about $40k a year), plus about $105k of onboarding. At the same assets, 20 sponsors break even only at about $3B, against about $1.5B for five ([results](model/out/results.md), Scale tables).

## 4. Price sensitivity

**Minimum viable price** (Model B, AI-native, five sponsors; ranges span $100-250k average balances; Model A founder-led, at economic cost, in brackets):

| Average assets | Break-even bps | bps for 20% margin | bps for 30% margin |
|---|---|---|---|
| $0.5B | 45-48 (40-43) | 56-59 (50-53) | 64-68 (57-61) |
| $1B | 24-29 (21-26) | 30-36 (27-32) | 34-41 (31-37) |
| $2B | 15-17 (13-16) | 18-22 (17-20) | 21-25 (19-23) |
| $5B | 8-11 (8-10) | 10-14 (9-13) | 11-16 (11-15) |

**Break-even assets by price** (Model B, five sponsors, $150-500k balance, operating basis):

| Price | Break-even assets |
|---|---|
| 5 bps | Never at $150k balances; $8-15B at $250-500k. **A software price, not a staffed-administration price.** |
| 10 bps | $2.9-4.5B |
| 15 bps | $1.6-2.2B |
| 20 bps | $1.1-1.5B |
| 25 bps | $0.9-1.05B |
| 30 bps | $0.75-0.84B |
| 35 bps | $0.64-0.68B |

Fully loaded figures (build amortisation and sales) are about 50-60% higher at 15-25 bps.

**Pricing structures** (Model B, five sponsors, $1.5B, $150k average balance):

| Structure | Effective bps | Operating profit | Margin | Profit after a 30% asset fall |
|---|---:|---:|---:|---:|
| Flat 15 bps | 15.0 | -$0.67M | -29.6% | -$1.34M |
| Flat 20 bps | 20.0 | $0.08M | 2.8% | -$0.82M |
| Flat 25 bps | 25.0 | $0.83M | 22.2% | -$0.29M |
| 20 bps, $250 per-account floor | 30.3 | $1.63M | 35.9% | $0.91M |
| 15 bps, $250 per-account floor | 26.3 | $1.03M | 26.1% | $0.50M |
| 10 bps + $150 per account | 20.0 | $0.08M | 2.8% | **-$0.37M** |
| 15 bps + $100 per account | 21.7 | $0.33M | 10.2% | -$0.34M |
| 20 bps, servicer pays payment rails | 20.0 | -$0.10M | -3.2% | -$1.00M |
| Buyer cap: lesser of 20 bps or $737 per account | 20.0 | $0.08M | 2.8% | -$0.82M (cap does not bind below about $370k balance) |
| 20 bps with a $150k sponsor minimum | 20.0 | $0.08M | 2.8% | inert: every sponsor here exceeds it (ADV-024) |

**Readings on structure:**
- **The floor is a disguised price increase.** At $75k balances the "$250 floor" is 44.7 bps effective (ADV-018). It also charges small funds 7-18% of balance a year, which is not acceptable for charitable assets (report 08).
- **A per-account component halves the damage of a market fall.** "10 bps + $150 per account" earns the same as 20 bps at a $150k balance, but loses $0.37M rather than $0.82M after a 30% fall, because servicer cost is driven by accounts and activity, not assets.
- **High-balance books need the opposite protection.** For them (the community-foundation and national targets averaging $0.6-2.5M per account), a flat 20 bps is $1,200-5,000 per account. That is 2-7x Ren's $737 at MS GIFT. Buyers there will price per account (ADV-001), so a cap or per-account tariff is needed to win them.

**The practical conclusion:** the cost-reflective tariff is a **per-account fee plus a low asset fee**, roughly $100-200 per account plus 5-10 bps. The per-account and bps levels can be set to equal 20 bps on a target book, and activity fees cover genuinely exceptional work: complex gifts, international grants, wires. That tariff is fairer at both ends of the balance range and more resilient to markets. It must be tested with buyers (report 07).

## 5. Stress tests (Model B, AI-native, 20 bps)

### Five equal $150k-balance sponsors at $1.5B (margin 2.8% base)

**Market falls:**
- 10%: -$0.22M
- 30%: -$0.82M
- 50%: -$1.42M

**Losing the largest sponsor:** -$0.04M.

**Operational stresses, each -$0.12M to -$0.42M:**
- automation 50% worse;
- exceptions x1.5;
- wages +15%;
- vendors +25%;
- a $500k security incident.

**Combined:** -$1.59M. **Severe:** -$1.88M.

### Anchor portfolio ($1.5B anchor at $300k + two $500M at $200k = $2.5B; margin 47.9% base)

| Stress | Margin |
|---|---:|
| Market -30% | 25.6% |
| Market -40% | 13.2% |
| Market -50% | -4.2% |
| Lose the anchor | 2.8% (profit $57k) |
| Combined (-30%, minutes x1.5, wages +10%, vendors +25%) | 4.0% |
| Severe | -121% |

### Starting assets needed to stay at break-even (or 10% margin) after a stress

Five sponsors, $150k balance:

| Stress | Model B | Model A |
|---|---|---|
| Market -30% (exploratory design objective) | $2.45B ($2.83B) | $2.19B ($2.53B) |
| Market -50% | $4.48B | $3.99B |
| Combined | $4.27B | |
| Severe | $6.65B | |
| Fully loaded, market -30% | $3.91B ($4.55B) | |
| Fully loaded, market -50% | $6.92B ($8.72B) | |
| Fully loaded, combined | $6.82B | |
| Fully loaded, severe | $9.84B | |

**Contractual minimums.** A sponsor minimum protects only small sponsors, because every sponsor in the tables already exceeds any reasonable minimum. A per-sponsor break-even minimum fee is about $100-135k a year for sponsors below about $50-75M. Below that a sponsor is unprofitable at 20 bps.

## 6. Scale and hiring thresholds (Model B, AI-native, 20 bps, $150k balance)

| Assets | One sponsor | Five sponsors |
|---|---|---|
| $1.0B | 3 added ops FTE | 4 |
| $1.5B | 4 | 5 |
| $3.0B | 8 | 9 |
| $5.0B | 14 | 15 |
| $10B | 28 | 29 |

These are with 6,667-66,667 accounts. Step costs ($0.1-1.7M) reflect:
- an operations manager per 6 added staff beyond 4;
- an integration engineer and an implementation analyst per 8 live sponsors;
- a fund accountant per 15,000 accounts beyond 5,000;
- a compliance officer above 10,000 accounts.

December demand above monthly capacity is the earliest bottleneck: about 3x average daily load. The ACT pass estimates about 10 ops FTE-equivalents in December at 5,000 accounts at year-round service levels, or 5.7 with a deferral policy (no December 31 legal deadline applies to DAF grants).

## 7. Sponsor-level results (the whole market through the model)

Of the 1,430 addressable, non-captive active sponsors ($151B average-asset proxy):

| Measure | Sponsors |
|---|---:|
| Positive contribution at 20 bps, AI-native base | 224 |
| Positive at high minutes | 141 |
| Positive, AI-enhanced only | 182 |
| Positive under the Ren per-account cap | 171 |

**By size:**

| Average assets | Sponsors | Result at 20 bps |
|---|---:|---|
| Under $50M | 1,179 | None positive (median -$65k to -$99k) |
| $50-100M | 95 | Median +$17k |
| $100-250M | 76 | Median +$157k |
| $250-500M | 39 | Median +$0.56M |
| $500M-1B | 23 | Median +$1.1M |
| Over $1B | 18 | Median +$4.0M |

**Covering Model B's $1.74M fixed cost alone:**
- 19 sponsors by arithmetic;
- 10 once build and sales are carried;
- 5 under the Ren per-account cap.

The realistic decision units are fewer still (report 02 and report 08 ADV-002):
- NPT is a competitor;
- AEF migrated to Ren in 2026;
- Dechomai is a processor;
- Greater Kansas City Community Foundation and Greater Horizons are one group;
- Silicon Valley, Chicago, the Carolinas, Boston and Marin are community foundations needing non-DAF fund support.

## 8. Model limitations

- Every handling minute is an assumption: there is no time study. Low and high minutes span 0.35-3.33x.
- Average assets are a (start + end) / 2 proxy.
- One archetype mix is used for all sponsors. It is rescaled with a derived elasticity, but real fund distributions are unknown.
- There is no revenue ramp, attrition, churn or renegotiation (ADV-015). Implementation fees are assumed. Financing cost is included in the capital figure (ADV-016).
- The December cost treatment is conservative, about $0.1M high (ADV-007).
- The sponsor CSV's "covers fixed" test slightly double-counts the minimum operations person (ADV-025).
- Same-model passes throughout; not independent validation (ADV-036).
