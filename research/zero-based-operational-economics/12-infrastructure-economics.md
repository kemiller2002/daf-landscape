# 12 — Infrastructure economics

Prices: [`infrastructure-prices.csv`](data/registers/infrastructure-prices.csv) (88 rows; Azure Retail Prices API, AWS Price List API, vendor pages; all read 2026-11-27). Consumption: [`infrastructure-consumption-assumptions.csv`](data/registers/infrastructure-consumption-assumptions.csv) (44 rows). Model parameters: [`infrastructure-parameters.csv`](data/model-inputs/infrastructure-parameters.csv). Notes and bill of materials: [infrastructure-notes.md](data/evidence/infrastructure-notes.md); an independent Python cross-check is kept at [`infrastructure_cost_model_crosscheck.py`](data/evidence/infrastructure_cost_model_crosscheck.py). Model output: [`infrastructure.csv`](data/model-outputs/infrastructure.csv).

## 1. Architecture priced

F# component monolith; WebAssembly UI served through an edge/CDN; **one managed PostgreSQL cluster**, schema plus role per sponsor (OD-P-PLT cut M, CNV-ARC-001); database-backed queues and outbox; append-only ledger; object storage for documents and evidence with on-upload malware scanning; no Kubernetes, message broker or Terraform estate. **No cloud provider has been chosen** (U-09; FIL-OD-01). Azure is priced as base (the earlier cost register used Azure; .NET stack — an inference); AWS is priced as the low case.

## 2. Deployment configurations (fixed monthly floor: production + non-production + CI)

| Config | Description | Azure | AWS |
|---|---|---:|---:|
| C1 | Shared, single region, zone-redundant HA (D2ds_v5 PostgreSQL primary+standby, 2 always-on app replicas, Front Door Premium WAF, Defender for Storage, Log Analytics, Key Vault) | ≈ $1,034/mo ($12.4k/yr) | ≈ $546/mo |
| C2 | C1 + warm DR region (cross-region replica, idle app replica) | ≈ $1,203/mo | ≈ $719/mo |
| C3 | C2 + isolated HA database, DR replica, customer-managed key and scanned storage per large sponsor | + $456/mo per sponsor | + $416/mo |

Floor choices that matter: Front Door Premium vs Standard (−$280/mo) and one-year reserved database pricing take Azure C1 to ≈ $502/mo.

## 3. Annual infrastructure cost by scale (model, base, PG-HNW activity)

| Accounts | C1 total | C1 per account | C2 per account | C3 per account (1 isolated sponsor) | Stored GB (7 yrs online) | Peak DB vCPU needed |
|---:|---:|---:|---:|---:|---:|---:|
| 1,000 | $12.6k | **$12.56** | $14.60 | $20.07 | 14 | 0.00 |
| 10,000 | $13.3k | **$1.33** | $1.53 | $2.08 | 137 | 0.03 |
| 100,000 | $20.1k | **$0.20** | $0.22 | $0.28 | 1,371 | 0.27 |
| 1,000,000 | $140.9k | **$0.14** | $0.15 | $0.15 | 13,710 | 2.74 |

The independent arithmetic in the notes gives Azure C1 $12.49, $1.32, $0.22, $0.17 per account-year — within a few percent (the test suite checks the 1k figure).

## 4. What scales with what

| Driver | Components | Behaviour |
|---|---|---|
| Fixed per environment | HA DB minimum, 2 app replicas, edge/WAF, scanning, DNS, keys, base logs, non-production, CI | ≈ $12.4k/yr; **dominates below ~100k accounts** |
| Data volume (accounts × retained years) | DB storage (×2 HA, ×3 with DR), backups, object storage, log archive | grows every year at flat accounts because retention is 7-10 years |
| Transaction volume (durable events) | DB/app CPU above the base tier, log ingestion | 2 vCores carry ~730k accounts in the base case; with every driver high, only ~23k |
| Accounts / users | identity MAU above the free tier, SMS MFA, email | **the largest variable costs at scale** (identity + SMS ≈ $88k of $141k at 1M accounts) |
| Exceptions | AI inference (Claude Sonnet 5.5 $2/$10 per MTok; ~8k in / 1k out tokens) | ≈ $0.026 per AI-assisted exception; $16k/yr at 1M accounts |
| Sponsors | isolated databases (C3 only) | ≈ $5.5k per isolated sponsor-year; price into that sponsor's contract |
| One-time | environment build, deployment pipelines | engineering time (TECHOPS activities), not cloud spend |

Identity and bank-account verification APIs (≈ $0.50-3.00 per new account) are larger than all variable infrastructure but are external per-event costs (activity `external_cost_per_event`), not infrastructure.

## 5. Against the prior $25 per account

The previous model's $25/account-year (PAR-011) holds only at about 1,000 accounts. From 10k accounts the resource-based estimate is **10-150× lower**, and even the compounded high case (≤ $6.56 at 10k, ≤ $2.84 at 100k) stays below the old $15 low. The $25 was never infrastructure ([03](03-cost-assumption-audit.md) §1 item 5). Replacement form: **fixed ≈ $12-25k a year per platform + ≈ $5.5k per isolated sponsor + ≈ $0.10-0.20 per account-year** (high case $1-2.5).

Servicing-economics' fixed infrastructure ($41.4k/yr: DB HA $6.2k + DR $3.1k + an unitemised $24k "hosting, networking, WAF, KMS, storage, egress" + $8k non-production) is about 3× the priced equivalent for the unitemised line.

## 6. When more expensive infrastructure becomes necessary

1. **A sponsor contract demands isolation** (separate database, keys, region): C3 per sponsor, typically at large institutional sponsors — a contractual, not a volume, trigger.
2. **A DR objective tighter than restore-from-backup** (RPO minutes, RTO hours): C2 warm region (+$2k/yr).
3. **Peak write volume exceeds ~2 vCores**: ~730k accounts base, ~23k with every driver high (heavy statement runs, large December peaks, chatty event design). Steps to 4 then 8 vCores; beyond that, split the shared cluster per sponsor.
4. **Identity beyond free tiers**: above 50k MAU on Entra (10k on Cognito). Passkeys/TOTP instead of SMS cuts the largest per-account line.

## 7. Excluded or unknown

Observability SaaS (Datadog-class $15-31/host-month — monitoring is absent in Echelon today; a paging/uptime line is in fixed costs FC-009), SIEM and security tooling (FC-010), cloud support plans (~$100+/mo, UNKNOWN), paid DDoS protection, payment rails and data subscriptions. Placeholders: AWS SMS (Twilio proxy), Plaid ($1.50, unpublished), CloudFront per-GB, Entra US SMS tier. All consumption drivers stay ASSUMPTION/INFERENCE until a PostgreSQL benchmark (RM-05) and a pilot measure them.

**Conclusion.** Infrastructure is not a material driver of Unbound's economics at any scale modelled: **under 1% of incremental cash cost** at $500M AUA (≈ $13k of $2.2M). Decisions should be made on control, isolation and resilience grounds, not to save infrastructure cost.
