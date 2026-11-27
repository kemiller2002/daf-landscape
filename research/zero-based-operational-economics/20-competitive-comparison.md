# 20 — Competitive comparison

The preserved competitive-displacement models (MD-1..MD-7) are compared with the zero-based model at **equal accounts and sponsors**, on equivalent scope. Output: [`baseline-comparison.csv`](data/model-outputs/baseline-comparison.csv). Mapping: MD-1/2/4/5 (vendor bears all administration) → CFG-5 full administration; MD-6 (licensing) → CFG-1; MD-7 (hybrid) → CFG-4. The original's "vendor opex" is compared with zero-based View 1 cash, View 2 allocated and View 3 standalone.

## 1. Like-for-like annual vendor cost (zero-based figures use analytic staffing, within ~6% of simulated)

| Accounts / sponsors | Original MD-5 (AI-native) | Zero-based CFG-5 View 1 / 2 / 3 | Original MD-1 (conventional) | Original MD-6 (licensing) | Zero-based CFG-1 View 1 |
|---|---:|---|---:|---:|---:|
| 2,000 / 1 | $2.84M | $2.20M / $2.39M / $3.18M | $2.05M | $1.86M | $1.40M |
| 4,000 / 2 | $3.17M | $2.71M / $2.90M / $3.69M | $2.93M | $1.93M | $1.46M |
| **7,695 / 5** (original break-even point) | **$3.85M** | **$3.89M** / $4.08M / $4.87M | $4.65M | $2.04M | $2.06M |
| 20,000 / 5 | $5.65M | $5.68M / $5.88M / $6.66M | $9.53M | $2.42M | $2.06M |
| 40,000 / 5 | $8.59M | $8.61M / $8.80M / $9.59M | $17.47M | $3.04M | $2.18M |

**At the original's own operating point the two models agree within 1%.** The zero-based model is about $0.6M cheaper at small scale (no salaried three-executive structure; fractional control seats) and identical at scale (variable cost converges on ~$142 per account).

## 2. Why the totals agree while the compositions differ

| Component | Original MD-5 | Zero-based CFG-5 |
|---|---|---|
| Executives on salary | founder, CTO, controller in fixed ($606k) | founder hours; fractional controller; no CTO line |
| Engineering | in CTO + two contracted approvers ($90k) | **4 dedicated engineers ($920k)** from workload (4,100 h) |
| Compliance | 0.25 FTE floor + event minutes | 2 dedicated (SLA- and backup-driven) |
| AI oversight | $0.3M flat | 384 h of change control + tokens |
| Build amortisation | inside fixed ($388k) | excluded (one-time) |
| Infrastructure | $25 per account | resource-based (~$13k/yr at small scale) |
| Per-sponsor work | 24,240 min/sponsor | ≈ 870-1,190 vendor h per small sponsor + ~1,320 h per onboarding |
| Insurance, assurance, counsel | $254k in non-personnel lines | ≈ $330k incremental lines, higher limits |

## 3. Like-for-like discipline

- Licensing is not compared with full administration without adjusting for transferred responsibility: CFG-1/2 leave 2,800-13,600 sponsor hours a year at 1,000-10,000 accounts; [`headline-scenarios.csv`](data/model-outputs/headline-scenarios.csv) reports a "system cost" (View 1 + sponsor labour at $70/h).
- Development is excluded from operating cost in both models in this comparison.
- The original MD-1 conventional comparator uses a superseded $1.18M memo (the re-priced figure is $1.66-1.74M), which flatters MD-1 at small scale.

## 4. Conventional administrators (repository benchmarks)

Ren's staffed administration of MS GIFT is paid ~18.5 bps ($737 per account) at $9.1B and 21,800 accounts; captive administrators are paid 24-67 bps (FMR 23.7 bps; BofA trustee 56 bps bundled). These are prices, not costs, and include profit. Run through the zero-based model as one sponsor with 21,800 accounts and a $417k mean balance (full administration, PG-HNW activity), an MS GIFT-sized book costs **$5.1M (analytic) to $5.8M (simulated) a year in cash — about 5.6-6.4 bps** — with 30-34 dedicated staff ([`benchmark-incumbent-sized-book.csv`](data/model-outputs/benchmark-incumbent-sized-book.csv)). Against Ren's $14.93M fee, that suggests either a large incumbent margin or scope the model does not carry (investment management, advisor channel support, enterprise overhead). It does not suggest an order-of-magnitude AI-native cost advantage over a well-run incumbent.

## 5. Where Unbound's advantage comes from (quantified where possible)

| Source | Evidence | Effect |
|---|---|---|
| Eliminated work | 3 scope exclusions only; prevention levers unmeasured | small (modelled) |
| Better workflow design | 96.7% of events complete without a person (modelled) | variable minutes ≈ 58 per account vs conventional 183 (MD-1) |
| Deterministic automation | 22 deterministic and 54 auto-exception activities | most of the variable saving vs conventional |
| AI assistance | factor 0.85 on 18 activities | ≈ $30k at $500M; net negative at small scale |
| Shared infrastructure | cloud < 1% of cost | negligible |
| Reusable components | most absent or immature | **none yet** (transfer, not elimination) |
| Lower organisational overhead | fractional control seats; no executive salaries in fixed | ≈ $0.6M at small scale vs MD-5 |
| Better data quality / fewer exceptions | unmeasured | potential −$0.1-0.4M (exceptions −40%) |
| Reduced migration friction | onboarding ~1,320 h per sponsor (modelled) | unmeasured |

**Against conventional administration (MD-1), the zero-based design is 2-3× cheaper per account at scale** ($142 vs ~$400). **Against the previous AI-native estimate (MD-5), it is not materially cheaper** except below ~4,000 accounts.
