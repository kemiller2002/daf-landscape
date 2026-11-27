# 10 — Workload and capacity model

Outputs: [`scale-grid-accounts.csv`](data/model-outputs/scale-grid-accounts.csv), [`scale-grid-aua-balance.csv`](data/model-outputs/scale-grid-aua-balance.csv), [`programmes-and-mixes.csv`](data/model-outputs/programmes-and-mixes.csv), [`headline-scenarios.csv`](data/model-outputs/headline-scenarios.csv). Programmes: [`programmes.csv`](data/model-inputs/programmes.csv) (heterogeneous tier mixes, not uniform balances).

## 1. Productive human hours by scale (PG-HNW, 1 sponsor, full administration CFG-5)

| Accounts | AUA at $250k | Vendor hours | Sponsor hours | Dedicated FTE | View 1 cash | View 1 per account |
|---:|---:|---:|---:|---:|---:|---:|
| 100 | $25M | 5,079 | 518 | 5 | $1.81M | $18,053 |
| 1,000 | $250M | 6,107 | 911 | 6 | $2.00M | $2,003 |
| 2,500 | $625M | 7,739 | 1,560 | 8 | $2.23M | $891 |
| 5,000 | $1.25B | 10,391 | 2,636 | 12 | $2.72M | $545 |
| 10,000 | $2.5B | 15,592 | 4,779 | 19 | $3.60M | $360 |
| 25,000 | $6.25B | 30,874 | 11,181 | 35 | $5.80M | $232 |
| 100,000 | $25B | 105,359 | 43,037 | 113 | $16.5M | $165 |
| 1,000,000 | $250B | 971,018 | 422,985 | 1,026 | $141.7M | $142 |

Licensing with support (CFG-2) for comparison: $1.40M at 100 accounts, $1.42M at 1,000, $1.80M at 10,000, $4.33M at 100,000 — with the sponsor carrying 13,604 and 118,472 hours respectively.

**Two regimes.** Below ~2,500 accounts, cost is a platform floor of about $1.8-2.2M (engineering, compliance, assurance, insurance, control seats). Above ~10,000 accounts, it converges on about **58 vendor minutes and $142 per account-year** — almost exactly the original model's 52.8 minutes and $146.77. The independent inventory therefore corroborates the original's *variable* economics; the difference lies in the fixed floor and in per-sponsor work.

## 2. Assets are not a sufficient predictor of workload

Same $1B, full administration, two sponsors:

| Programme | Accounts | View 1 cash | View 1 as bps |
|---|---:|---:|---:|
| Concentrated institutional ($1M mean, 25 grants/acct) | 1,000 | $2.45M | 24.5 |
| National HNW ($250k mean) | 4,000 | $2.71M | 27.1 |
| Community-foundation style ($100k) | 10,000 | $3.37M | 33.7 |
| Dormant-heavy legacy book ($50k; 60% dormant) | 20,000 | $3.37M | 33.7 |
| High-volume retail ($10k; monthly contributions) | 100,000 | $22.0M | 220 |
| Payroll workplace giving ($5k; biweekly) | 200,000 | $56.0M | 560 |

At 20 bps ($2M revenue) none of these programmes covers full administration at $1B with two sponsors. Retail and payroll programmes cost 10-28× their AUA fee: they need per-account or per-transaction pricing, or a licensing configuration where the sponsor operates.

## 3. The same assets at different balances (full administration, View 1 as bps of AUA)

| AUA | $5k | $25k | $100k | $250k | $1M |
|---|---:|---:|---:|---:|---:|
| $100M | 494 | 255 | 200 | 195 | 181 |
| $500M | 330 | 99 | 54.5 | 44.0 | 39.1 |
| $1B | 308 | 81 | 36.9 | 27.1 | 22.9 |
| $2B | 294 | 70 | 27.0 | 18.6 | 12.9 |
| $5B | 286 | 64 | 21.7 | 13.1 | 8.5 |

## 4. Sponsor count is a first-order driver

At $1B and 4,000 accounts: one sponsor $2.55M; four large sponsors $3.17M; twenty small sponsors $5.49M; fifty small sponsors $10.7M. Each sponsor adds about **760 vendor hours of its own work** (monthly close preparation, audit support, Schedule D package, payment release batches, integration certification, sponsor-attributable incidents, policy changes) plus ~1,320 hours per onboarding — roughly **$145k a year of recurring marginal cost for a small sponsor** ([`sponsor-unit-economics.csv`](data/model-outputs/sponsor-unit-economics.csv)).

## 5. Activity level

Low-activity accounts (×0.6) save about $0.22M at $1B; high-activity (×2.06) adds $0.43M. Dormant accounts cut workload but also tend to hold balances below average, so revenue falls too.

## 6. Peaks and capacity

December year-end giving and month-end close produce the peaks. Under full administration, operations needs about 2.65 simulated FTE against 0.97 average at the reference scale; compliance needs about twice its average at 4,000 accounts. Surge contractors halve the operations premium; compliance cannot use them. The scarce capacity is not processing but **engineering (4,131 h at 2,000 accounts, 90% utilised)** and **founder time**.
