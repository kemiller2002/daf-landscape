# 17 — Revenue models

Model: `Revenue.fs`; outputs [`revenue-models.csv`](data/model-outputs/revenue-models.csv), [`licensing-per-account.csv`](data/model-outputs/licensing-per-account.csv), [`sponsor-unit-economics.csv`](data/model-outputs/sponsor-unit-economics.csv), [`capital-required.csv`](data/model-outputs/capital-required.csv). 20 bps is a working comparison, not a market entitlement. **Assets administered are neither revenue nor assets owned by Echelon.**

## 1. Market reference points held in the repository

| Arrangement | Observed | Source |
|---|---|---|
| Ren → MS GIFT administration (CY2024) | $14.93M = **18.46 bps** = $737/account (21,800 accounts, $9.1B, 0 employees at sponsor) | servicing-economics PRC-O-* |
| Ren → U.S. Charitable Gift Trust | 39-40 bps; $389-429/account | same |
| Ren → RCF (FY2024) | $19.2M; 38.7 bps of admin revenue | same |
| Ren/Stellar software-only | $118k-$2.50M; 0.5-9 bps; $34-611/account; floor ~$120-175k | same |
| TIFIN Give → GiveClear | $815/account; ADV 30 bps to $1M | same |
| Ren NCF software price | ≈ $81/account | competitive-displacement PAR-012 |

## 2. Revenue structures compared (full administration, $1B, 4 sponsors, 4,000 accounts; View 1 cost $3.17M)

| Structure | Revenue | Margin after View 1 | Revenue per account |
|---|---:|---:|---:|
| AUA 20 bps | $2.00M | −$1.17M | $500 |
| AUA 10 bps | $1.00M | −$2.17M | $250 |
| Per-account $81 | $0.32M | −$2.84M | $81 |
| Per-account $150 | $0.60M | −$2.57M | $150 |
| Per-sponsor $150k | $0.60M | −$2.57M | $150 |
| $5/grant + $2/contribution | $0.19M | −$2.98M | $46 |
| 20 bps with $150k minimum per sponsor | $2.00M | −$1.17M | $500 |
| $75k per sponsor + 10 bps | $1.30M | −$1.87M | $325 |
| Tiered (25 bps to $250M, 15 to $1B, 8 above, per sponsor) | $2.50M | −$0.67M | $625 |
| 15 bps + $25 per human exception | $1.99M | −$1.18M | $498 |

Four $250M sponsors under full administration lose money at every structure tested at $1B. The same $1B as one or two sponsors is close to break-even at 20-25 bps ([18](18-break-even-analysis.md)). **Sponsor count, not fee structure, decides.**

## 3. Licensing must be priced per account, not as bps

Licensing with support (CFG-2), accounts needed to break even on View 1 (one sponsor per $250M):

| Price per account | Break-even accounts | Equivalent at $250k balance |
|---:|---:|---:|
| $40 | never | 1.6 bps |
| $81 (Ren NCF reference) | never | 3.2 bps |
| $120 | ≈ 98,000 | 4.8 bps |
| $150 | ≈ 41,500 | 6 bps |
| $250 | ≈ 13,200 | 10 bps |

Charging 20 bps for licensing (≈ $500/account at $250k) would be about six times market software pricing; break-even figures for licensing at 20 bps in [`break-even.csv`](data/model-outputs/break-even.csv) are therefore boundary cases, not plans (review ADV-BI-001).

## 4. Sponsor unit economics (full administration; marginal cost averaged over adding four sponsors to a $1B book)

| Sponsor assets | Revenue at 20 bps | Marginal recurring cost | Onboarding (hours / cost) | Acquisition cash | Payback | Minimum annual fee over a 5-year term |
|---:|---:|---:|---:|---:|---:|---:|
| $25M | $50k | $144k | 1,319 h / $158k | $30k | never | $181k |
| $50M | $100k | $145k | 1,319 h / $158k | $30k | never | $182k |
| $100M | $200k | $147k | 1,319 h / $158k | $30k | 43 months | $185k |
| $250M | $500k | $291k | 1,319 h / $158k | $30k | 11 months | $329k |
| $500M | $1.0M | $395k | 1,319 h / $158k | $30k | 4 months | $433k |
| $1B | $2.0M | $695k | 1,319 h / $158k | $30k | 2 months | $732k |

- **Minimum viable contract (incremental, on an established platform): about $185k a year**, i.e. ≈ $93M at 20 bps or a minimum-fee clause.
- **Minimum viable first customer** (who must carry the platform alone): fees of about $1.8-2.5M a year under full administration — **not reachable at 20 bps by a single $1-1.25B sponsor at $250k balances** (see §5: $0.55M gap at $1B), so a minimum-fee contract is required; or $1.4M a year under licensing with support.
- Implementation and migration fees (not in the break-even) should recover the ≈ $160-190k onboarding cost per sponsor; institutional buyers routinely pay them (ADV-BI-021).

## 5. Working capital and capital required (first sponsor, year one)

| First sponsor | Config | One-time cash | Pre-revenue operating cash (12 months) | Receivables | Annual gap after go-live | Capital required |
|---:|---|---:|---:|---:|---:|---:|
| $100M | CFG-2 | $0.57M | $1.40M | $0.03M | $1.20M | **$3.2M** |
| $100M | CFG-5 | $0.57M | $1.95M | $0.03M | $1.75M | **$4.3M** |
| $500M | CFG-2 | $0.57M | $1.44M | $0.13M | $0.44M | **$2.6M** |
| $500M | CFG-5 | $0.57M | $2.20M | $0.13M | $1.20M | **$4.1M** |
| $1B | CFG-5 | $0.57M | $2.55M | $0.25M | $0.55M | **$3.9M** |

These exclude development already sunk and the economic value of founder time.

## 6. Exposure to asset values

Revenue scales with assets; cost scales with accounts and sponsors. At $1B with four sponsors: a 30% market decline cuts revenue from $2.0M to $1.4M with no cost relief; net withdrawals of 15% cut it to $1.7M; losing the largest sponsor (40% of assets) cuts revenue to $1.2M while cost falls only to $2.56M. **Per-account floors or minimum fees protect against market declines; per-sponsor minimums protect against small sponsors.**

## 7. Recommended structure

Tiered AUA fee with a per-sponsor annual minimum of about $185k for full administration, separate implementation/migration fees, and per-account licensing ($150-250) for licensing configurations. Exception fees are not recommended as primary revenue: they price the residual 3% of events and create an incentive mismatch with prevention.
