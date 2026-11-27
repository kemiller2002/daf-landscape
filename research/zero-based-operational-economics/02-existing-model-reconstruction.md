# 02 — Existing model reconstruction

The original model is preserved unchanged as the comparison baseline: `research/competitive-displacement/model` (revision 2). The zero-based model reproduces it **by calling the original F# code** (`Baseline.fs`); the test `original model is reproduced` fails if any headline drifts by more than 0.5%. Generated: [`baseline-reconstruction.csv`](data/model-outputs/baseline-reconstruction.csv). Full trace: [`original-cost-trace.csv`](data/registers/original-cost-trace.csv) (132 rows) and [notes](data/evidence/original-cost-trace-notes.md).

## 1. The formula

For MD-5 "AI-native administration with deterministic controls" at 20 bps, $250k mean balance and 5 sponsors:

```
break-even assets A = (F + n·S) / (r − v/B)
                    = (2,500,000 + 5 × 43,679) / (0.0020 − 146.766/250,000)
                    = 2,718,396 / 0.0014129
                    = $1.924B   (7,696 accounts)
opex at break-even  = 2,500,000 + 218,396 + 7,696 × 146.766 = $3.85M
```

Assets and accounts are tied by a single average balance; workload scales with accounts, revenue with assets.

## 2. Reconstructed figures

| Mission figure | Reproduced | Where it comes from |
|---|---|---|
| ~$1.9B operating break-even | **$1.924B** | formula above |
| ~$2.3B fully loaded | **$2.326B** | adds build/5, CAC $125k and onboarding $48k per sponsor amortised over 5 years |
| $2.3M AI-native fixed cost | **$2.5M today** | $2.3M was revision 1 (F3 $1.46M + MSP platform $0.68M + $0.1M AI governance, rounded up). Revision 2 added $0.2M AI oversight (CHL-104). The assumptions register still shows $2.3M (stale; OCT-130). |
| $147 variable per account | **$146.77** | labour $77.84 (of which $19.46 is the 0.75 utilisation divisor) + external $16.14 + AI $2.30 + prevention $2.09 + expected failures $23.39 + "infrastructure" $25.00 |
| 53 human minutes per account | **52.76** | grant approval 25.30 (48%); payment exceptions 5.36; contacts 4.82; vetting 3.36; breaks 2.66; 20 others 11.27 |
| $25 infrastructure per account | **$25 (PAR-011)** | a servicing-economics account-maintenance placeholder chosen to reconcile to a superseded $75/fund memo, which itself allotted only **$5** to cloud. Relabelled "infrastructure" later. |
| ~$1.94M initial development | **$1,940,117** | 30% non-compressible of a $2.21M MSP scope ($663k) + 70% construction ÷ 1.5 ($1.031M) + agent compute ($26k) + safety floor ($220k) |
| $316k charity registry | **$316,093** | RC-01..RC-10; a 1.0 FTE steward ($121.8k, 39%) is a staffing ratio, not a workload |
| $90-170k registry minimum | **$89.1k-$162.3k** | RA-1 public-data registry at 5k and 20k charities, 1 sponsor, change-driven. Note: charity-network report 20's own low bound is $107k; the $90k comes from competitive-displacement report 05. |

## 3. Composition of the $2.5M fixed cost

| Block | Amount | Content |
|---|---:|---|
| F3 core | $1,460,771 | founder $200k, CTO $222k, controller $183k (loaded); reviewer $40k; two contracted code approvers $90k; compliance floor $46k; overhead $33k; 31 non-personnel lines + 7.5% contingency $646k |
| MSP platform charge | $680,162 | **build amortisation $388k**, Echelon share $135k, Echelon licence $60k, non-production $24k, maintenance gap $43k, servicing platform $30k |
| AI governance (REV1) | $100,000 | flat |
| AI oversight (REV2) | $200,000 | flat, citing SR 11-7 (bank model-risk guidance) |
| Unexplained residual | $59,067 | rounding "1.46 + 0.68" up to "2.2" |
| **Total** | **$2,500,000** | |

## 4. Composition of the $43.7k per sponsor

24,240 sponsor-level minutes a year at loaded rates ÷ 0.75 utilisation: close and sign-off 9,000 min; audit preparation 7,200 (held at conventional, CHL-105); configuration upkeep 3,600; governance and regulatory reporting 2,640; incidents 1,800.

## 5. Lineage

```
BLS/vendor pages → servicing-economics cost register (CST-*) → PAR-001..006 rates
superseded $75/fund memo → $25 per-account placeholder → charity-network ECO → PAR-011 "infrastructure"
servicing-economics ACT-A01..S07 → events.csv EV-E01..E25 → 52.76 min, $43.7k/sponsor
PR #87 (ai-native-capital-minimization): F3 $1.46M + MSP platform $0.68M → $2.2M (+$0.1M AI) = $2.3M → REV2 +$0.2M = $2.5M
PR #87 DEV pass (132 person-months, agent estimate) → $1.94M build
charity-network report 20 → RC-01..RC-10 = $316k → RA-1/RA-3 = $89-167k
```

## 6. Reconstruction verdict

The arithmetic reproduces exactly. Section 3 of [03](03-cost-assumption-audit.md) shows that the result is **not derived from its components**: errors in opposite directions roughly offset. Removing the double counts and adding the evidenced omissions gives roughly $1.6-1.8B within the original framework. The zero-based model ([18](18-break-even-analysis.md)) goes further, because it rebuilds fixed cost from workload and control obligations instead of from a three-executive staffing design.
