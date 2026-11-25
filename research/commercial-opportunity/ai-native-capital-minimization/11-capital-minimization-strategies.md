# 11: Capital minimization strategies

**Sources:**
- model sections 9, 9b and 10 ([`results.md`](model/out/results.md); [`sequences.csv`](model/out/sequences.csv); [`failure-costs.csv`](model/out/failure-costs.csv));
- sequence definitions in [`Sequences.fs`](model/src/CapitalMinimization/Sequences.fs);
- gates in [`commercial-milestones.csv`](../../../data/commercial-opportunity/ai-native-capital-minimization/commercial-milestones.csv);
- LYR failure catalogue ([15](15-failure-and-resilience-analysis.md)).

Every timing and amount is an assumption.

## Common settings
- 60 months; 20 bps; sponsors at a $250k average balance.
- Fees billed quarterly in arrears and collected one month later.
- Each sponsor starts in pre-delegation, at AI-enhanced minutes (about 100), for 12 months after its own go-live; then 50 minutes.
- Recurring platform cost:
  - Echelon share and licence from formation;
  - non-production, servicing-specific platform and the maintenance gap from go-live.
- The minimum safe product is built at 1.5x ($1.94M) over 12 months.
- A deferred-scope tranche follows the second go-live.
- Startup legal, money-transmission opinion, SOC readiness, brand and migration tooling as in the previous study; recruiting per hire.

## Sequences A-G (cash view, three $500M sponsors = $1.5B)

| Sequence | Equity need | Debt-financed trough | Month profitable | Year-5 profit | NPV 15% | With growth to $3.0B: equity / NPV |
|---|---|---|---|---|---|---|
| A conventional: F5 staged, $5M contracted build over 24 months | $10.07M | $14.18M | 46 | $0.19M | -$7.67M | $10.30M / -$4.56M |
| B product-first: F2 builds, F5 from first go-live | $6.52M | $8.84M | 42 | $0.31M | -$4.27M | $6.73M / -$1.19M |
| C customer-funded: design partner prepays $250k + $150k minimum fee; F3 then F5 | $6.36M | $8.63M | 39 | $0.31M | -$4.18M | $6.56M / -$1.10M |
| D narrow entry: non-custodial service at $40k per sponsor, administration from month 24 | $7.04M | $9.18M | 48 | $0.39M | -$4.20M | $7.25M / -$1.09M |
| E provider partnership: partner carries money movement and SOC 1, keeps 30% (14 bps net); F3 | $7.15M | $10.06M | never in 60 | -$0.26M | -$6.64M | $7.49M / -$5.67M |
| **F founder-led: F1 builds, F3 from the anchor's go-live; $1.0B anchor + $500M** | **$4.54M** | **$6.03M** | **30** | **$0.70M** | **-$1.66M** | **$4.74M / +$1.44M** |
| G hybrid: narrow service + design partner + staged F2/F3/F5 | $6.88M | $9.16M | 45 | $0.35M | -$4.33M | $7.12M / -$1.24M |

Economic view, with founders paid at market:
- founder-led F needs $5.11M equity ($6.84M debt-financed) and is profitable from month 36;
- B, C, D and G need $6.6-7.5M;
- E needs $8.0M.

## Findings

1. **Minimum credible startup capital is about $4.5-7.2M equity**, plus financing if the deficit is borrowed.
   - The lowest is a founder-led path with one large anchor: $4.5M. That path depends on the anchor. If it withdraws, capital rises by $3.8M and there is no profit within 60 months.
   - The other AI-native paths cluster at $6.4-7.2M.
   - This **corrects** the previous study's $2.7-3.6M minimum, which assumed a $0.72M build. It lands inside the previous conservative $5-8M range.
2. **The conventional reference** (A, $5M contracted build, staged team) needs $10.1M equity. That is consistent with the previous study's $8.5-11.4M Unbound-scale case.
3. **At $1.5B under administration no AI-native path earns its cost of capital** (NPV at 15% is negative). Growth to $3.0B is needed. Even then only the founder-led path has positive NPV. The business is a scale business; capital minimization lowers the entry ticket, not the scale required.
4. **Customer funding helps at the margin.** A $250k prepaid implementation and a $150k minimum fee save about $0.16M of equity (C vs B) and bring profitability forward by 3 months. It does not fund the build (COM part 3).
5. **Narrow entry costs capital rather than saving it** (D, G). A non-custodial service carries SOC 2, insurance, compliance and support from its own launch, and at $40k per sponsor it does not cover them. Use it to buy **evidence** (price, charity-match recall, buyer behaviour), and keep it small.
6. **Provider partnership is the worst at 14 bps net.** Unless the partner also brings sponsors much faster than modelled, the fee share outweighs the assurance and staffing it removes.
7. **Incremental capital if Unbound already exists** (model section 9c). The servicing company alone needs about **$1.35-2.8M** of equity:
   - founder-led $1.35M, profitable from month 18, NPV +$3.0M;
   - B, C, D and G $2.2-2.7M, with positive NPV;
   - partnership E $2.8M, with negative NPV.

   **The capital problem is mostly the platform, not the servicing company.** This view assumes no build, engineers in Layer B and only the servicing-specific platform cost charged. Group-level capital still includes Unbound's build ($1.9-4.6M) and its recurring cost, which with one customer falls on servicing (report 03).

## Staged investment

Gate 1, about $0.12-0.15M:
- buyer price test;
- Echelon licence terms;
- payments counsel opinion;
- auditor conversation.

Gate 2, about $0.6-0.75M cumulative:
- design-partner LOI;
- instrumented shadow replay;
- 3-5 capabilities built under the measurement protocol.

Each gate has stop conditions ([`commercial-milestones.csv`](../../../data/commercial-opportunity/ai-native-capital-minimization/commercial-milestones.csv)). A failed go-live, by contrast, sinks $2-3M or more. **The option value is in not building until gates 1-2 pass.** The recommended path is founder-led (F) with a design partner (C's terms), entered only through the gates.
