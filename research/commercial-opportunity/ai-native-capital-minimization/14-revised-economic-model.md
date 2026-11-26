# 14: Revised economic model

**Model:** [`model/`](model/), an F# extension project (`CapitalMinimization`) that references the previous study's model **unchanged**. Results: [`model/out/results.md`](model/out/results.md) (sha256 `efa363cd34bc…`). CSVs:
- [`design-breakeven.csv`](model/out/design-breakeven.csv);
- [`sequences.csv`](model/out/sequences.csv);
- [`failure-costs.csv`](model/out/failure-costs.csv);
- [`development-scenarios-model.csv`](model/out/development-scenarios-model.csv).

**Tests:** 23 pass, including a regression that the previous anchor plan still needs $3.56M.

```bash
cd research/commercial-opportunity/ai-native-capital-minimization/model
dotnet test tests/CapitalMinimization.Tests
dotnet run --project src/CapitalMinimization -c Release -- out
```

## What the model adds

| Module | Content |
|---|---|
| `Design.fs` | Outcome-designed organizations with skill pools, a 0.75 FTE hiring threshold, fractional premium capacity, December release capacity, coordination beyond six pairs, and a CNV-GOV-003 control check |
| `Layers.fs` | Layers A (Echelon), B (Unbound) and C (servicing). Standalone, incremental, fully allocated and consolidated views; engineering embedded in a design is not double counted; cost-plus transfer |
| `Development.fs` | Amdahl-bounded productivity: construction share, compute share, safety floor; deliverable scope and safety by investment |
| `Designs.fs` | Parameters: rates from the previous cost register, itemised non-personnel, designs F1-F8+, outcome-designed variant, steady-state adjustments, MSP and full-scope platform bases, DEV-calibrated development baseline |
| `Sequences.fs` | Sequences A-G as monthly cash plans, with recurring platform cost, per-sponsor pre-delegation, a deferred-scope tranche, equity vs debt-financed capital, NPV, ROIC, and eleven failure modifiers including correlated failures |
| `Program.fs` | Sections 1-14: baseline, designs, break-even, targets, tails, ratio vs workload, layers, development, sequences (with growth and existing-Unbound variants), failures, pricing, cost bridge, scenario matrix, CAC |

## Cost bridge first (ADV2-011)

At $1.5B, 5 sponsors and a $250k balance:

| Step | Annual cost | Change | Nature |
|---|---|---|---|
| Previous Model B, AI-native, fully loaded ($1.0M build amortisation + $250k sales) | $3.88M | | baseline |
| Remove the fully loaded lines | $2.63M | -$1.25M | presentation |
| F5 workload-driven design, same minutes | $2.63M | ~$0 | structural. Ratio steps are replaced, but December release capacity, coordination, integration and relationship hours become explicit |
| Add standalone MSP platform charge (build at 1.5x over 5 years, Echelon share and licence, maintenance gap) | $3.26M | +$0.64M | assumption: development model, not measured |
| *(not in the bridge)* steady-state adjustments: sales to $250k, reconciler, turnover, replacement onboarding | about $3.58M | +$0.32M | ADV2-001 |
| Outcome-designed variant: 30.1 minutes, sponsor-level 12,720 minutes, +3% capacity [unproven] | $2.90M (before adjustments) | -$0.36M | hypothesis |

**Like for like, the redesigned company costs about $0.3M a year less than the previous fully loaded case** at this scale: $3.58M against $3.88M, about 8%.
- Almost all of the saving comes from a **cheaper build assumption**: a minimum product at about $1.9M instead of $5M.
- None of it comes from the organization.
- The outcome-designed variant could save another $0.36M, but it is unproven and depends on sponsor delegation and auditor reliance.

## Scenario matrix (model section 13; 20 bps unless stated; 5 sponsors)

| Scenario | Fixed cost | Marginal cost per account-year | Break-even at $250k | at $100k | at $500k | 15 bps | 25 bps | Market -30% |
|---|---|---|---|---|---|---|---|---|
| Conventional (previous Model B, conventional minutes, fully loaded) | $2.99M | $423 | $7.84B | >$20B | $3.50B | >$20B | $3.83B | >$20B |
| AI-assisted conventional (previous, AI-enhanced, fully loaded) | $2.99M | $218 | $2.99B | $6.25B | $2.24B | $4.82B | $2.05B | $5.79B |
| Previous AI-native (fully loaded, $5M build) | $2.99M | $132 | $2.09B | $2.67B | $1.83B | $3.04B | $1.56B | $3.34B |
| AI-native independent (F5, standalone, build at 1.5x, no Echelon) | $2.24M | $135 | $1.58B | $2.31B | $1.41B | $2.39B | $1.19B | $2.66B |
| Echelon-supported AI-native (F5, fully allocated, build at 3x) | $2.09M | $132 | $1.57B | $2.20B | $1.39B | $2.36B | $1.18B | $2.62B |
| Founder-led staged (F3, standalone) | $2.14M | $133 | $1.62B | $2.32B | $1.43B | $2.43B | $1.20B | $2.72B |
| F5 standalone + steady-state adjustments | $2.64M | $135 | **$1.85B** | $2.71B | $1.65B | $2.83B | $1.40B | $3.12B |
| F5 standalone, full-scope platform base (LYR) | $3.54M | $135 | $2.46B | $3.64B | $2.20B | $3.75B | $1.84B | $4.23B |
| F5 + adjustments, full-scope platform base (LYR) | $3.81M | $135 | **$2.65B** | $3.96B | $2.35B | $4.01B | $1.99B | $4.51B |
| Combined software + administration (licences net of their cost) | $2.07M | $132 | $1.56B | $2.18B | $1.39B | $2.34B | $1.17B | $2.61B |
| Outcome-designed F5 [unproven], fully allocated | $2.09M | $62 | $1.37B | $1.59B | $1.29B | $1.90B | $1.06B | $2.08B |

## Findings

1. **Sustainable profitability at 20 bps needs about $1.4-1.9B (MSP platform) to $2.5-2.7B (full-scope platform) of assets**, with 5 sponsors at a $250k balance.
   - Break-even is $1.44-1.85B on the MSP platform. A 20% margin needs $1.9-2.3B.
   - The range overlaps the previous study's fully loaded $1.8-2.3B. **No fundamentally different cost curve emerges.**
2. **The decisive variables, in order:**
   - buyer price at high balances (7 bps → break-even above $3.8B);
   - platform scope and engineering staffing (a $0.6-1.0B swing);
   - December capacity;
   - the build productivity multiple;
   - handling minutes. Halving minutes moves break-even by only about $0.2B.
3. **Marginal cost per account-year is about $135** for AI-native designs against $423 conventional; outcome-designed would be $62.
   - The difference is real but concerns variable cost, which is a small share of the cost.
   - **Fixed costs decide the economics.** These are controls, platform, assurance, insurance and sales.
4. **Average balance matters as much as design.** At a $100k balance, break-even rises by 40-50%. Per-account pricing (report 10) is the remedy, not lower cost.
5. **Downturn resilience is weak at the entry scale.** A 30% market fall moves break-even from $1.6-1.9B to $2.6-3.1B. A staffed servicer should not go live without a path to well above break-even.
6. **ROIC and NPV.** At $1.5B no AI-native path has a positive NPV at 15%. At $3.0B only the founder-led path does (+$1.4M). Year-5 ROIC is 3-9% at $1.5B and 13-23% at $3.0B (a single-year snapshot).
7. **The $5-8M conservative capital case is still the right reference** for building the platform and the servicer together. The $1.35-2.8M servicing-only case applies only if Unbound's build is paid elsewhere (report 11).

## What is measured, derived or assumed

- **Measured:** nothing about the company.
- **Derived from sources:** rates (BLS-based, previous register) and non-personnel lines (vendor price lists in the previous cost register).
- **Assumed:** everything that matters most. That includes minutes, exception rates, December arrivals, productivity, platform staffing, buyer price, sales timing and the steady-state adjustments.

The falsification conditions are in [16](16-adversarial-review.md) and the cheapest tests in [18](18-executive-findings.md).
