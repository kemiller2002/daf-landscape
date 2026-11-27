# Infrastructure cost evidence: Unbound (zero-based)

Reviewed 2026-11-27. Prices: [`../registers/infrastructure-prices.csv`](../registers/infrastructure-prices.csv) (88 rows; Azure Retail Prices API, AWS Price List API bulk CSVs for us-east-1, vendor pages, all read 2026-11-27). Consumption drivers: [`../registers/infrastructure-consumption-assumptions.csv`](../registers/infrastructure-consumption-assumptions.csv) (44 rows, low/base/high). The arithmetic is reproducible with [`infrastructure_cost_model_crosscheck.py`](../../model/infrastructure_cost_model.py). Hours per month = 730. Unless stated, figures are pay-as-you-go (PAYG) list prices in East US / us-east-1.

## 1. Which cloud is intended

**No cloud has been chosen. Azure is used as the primary price reference (INFERENCE, low-medium confidence) and AWS as the alternative.** Both are fully priced, because the choice is still open.

What the repositories say:

| Evidence | What it states | Class |
|---|---|---|
| `echelon-organization-administration/.../availability-architecture/19-UNRESOLVED-DECISIONS.md` U-09 | "Managed hosting platform (container platform, managed PostgreSQL provider, region): **Not chosen anywhere in Unbound**. Owner decision." | VERIFIED-FACT |
| `unbound/requirements/discovery/2026-11-26-file-ingestion/14-QUESTIONS-AND-OWNER-DECISIONS.md` FIL-OD-01 | Open owner decision. Recommends a cloud with native on-upload scanning (AWS GuardDuty S3 or Microsoft Defender for Storage); GCP would need a licensed engine. | VERIFIED-FACT |
| `unbound/requirements/PLATFORM-UX-API-AND-ASSURANCE-STANDARDS.md` CNV-ARC-001 | Mandates a **modular monolith on one managed PostgreSQL cluster**, with a schema and role per sponsor, RLS, an outbox and in-database state machines. A dedicated database is used only when risk or contract requires it. | VERIFIED-FACT |
| Same, CNV-PLT-004 | Transaction records are retained **10 years** after the transaction date. | VERIFIED-FACT |
| `availability-architecture/02-ALTERNATIVES-ASSESSMENT.md`, MISSION-BRIEF | No Kubernetes, Terraform, Redis, Kafka, RabbitMQ, distributed locks, sharding or read replicas. | VERIFIED-FACT |
| `kemiller2002/echelon-foundry` (about page) | The owner's background includes "Cloud migration strategy: AWS and Azure". There are no deployment manifests. | VERIFIED-FACT |
| `daf-landscape` servicing-economics cost register CST-T01..T04 | Earlier pricing work used Azure Database for PostgreSQL Flexible Server. | VERIFIED-FACT (of prior choice) |
| F# / .NET stack, WebAssembly UI | Azure has the closest first-party fit for .NET (Container Apps, Entra External ID). This is a tie-breaker, not a decision. | INFERENCE |

Grep result: in the four named trees, `Azure`, `AWS`, `Container Apps`, `App Service`, `Cosmos` and `Static Web` appear only in the open-decision text and in vendor price comparisons. Hits for `rds` came from words like "words" and "records". `PostgreSQL` appears dozens of times, so **managed PostgreSQL is the only infrastructure commitment**. `SQL Server` does not appear.

Implications:
- **AWS is cheaper at the floor in this design (about 47% lower at 1k accounts).** Almost all of the gap is Azure Front Door Premium ($330/month), which the design uses to get managed WAF rules. AWS WAF on CloudFront or an ALB costs about $15/month. Azure Front Door Standard with custom rules ($35 + $5) closes most of the gap.
- AWS also has two capability advantages that FIL-OD-01 already noted: S3 presigned uploads can bind a SHA-256 checksum, and malware scanning is cheaper per GB ($0.09 vs $0.15) with no $9.78 per-account monthly fee.
- Azure has cheaper 1-year reserved PostgreSQL (-40% vs RDS -23%) and a larger free identity tier (50k MAU vs 10k).

## 2. Unit prices used (summary; full register in CSV)

| Resource | Azure (primary) | AWS (alternative) |
|---|---|---|
| HA PostgreSQL, 2 vCPU | Flexible Server D2ds_v5 $0.178/h ×2 (zone-redundant standby) = **$259.88/mo**; 1-yr reserved $468/vCore-yr → $156/mo | RDS db.m7g.large Multi-AZ **$0.337/h = $246.01/mo**; 1-yr RI $0.2595/h → $189.44/mo; db.t4g.medium Multi-AZ $0.129/h (burstable) |
| DB storage | $0.115/GB-mo, doubled for HA ($0.23) | gp3 Multi-AZ $0.23/GB-mo (Single-AZ $0.115) |
| DB backup | $0.095/GB-mo above provisioned size | $0.095/GB-mo above allocation |
| DR replica (C2) | 2 vCore single $0.178/h = $129.94/mo + $0.115/GB; inter-region $0.02/GB | m7g.large Single-AZ $0.168/h = $122.64/mo + $0.115/GB; us-east-1→us-east-2 $0.01/GB |
| App compute | Container Apps $0.000024/vCPU-s + $0.000003/GiB-s; grant 180k vCPU-s + 360k GiB-s/mo | Fargate ARM $0.03238/vCPU-h + $0.00356/GB-h; ALB $0.0225/h + $0.008/LCU-h |
| Object storage | Hot ZRS $0.026, Hot LRS $0.0208, Cool ZRS $0.019, Cold $0.0036, Archive $0.00099 /GB-mo | S3 Standard $0.023, Std-IA $0.0125, Glacier IR $0.004 /GB-mo |
| Malware scanning | Defender $9.78/storage account-mo + $0.15/GB | GuardDuty S3 $0.09/GB + $0.215/1k objects (first 1 GB and 1k objects free) |
| Egress | Front Door $0.0825/GB (first 10 TB); bandwidth $0.087 after 100 GB free | $0.09/GB after 100 GB free |
| Edge/WAF | Front Door Premium $330/mo (Standard $35 + $5 WAF policy); $0.009/10k requests | WAF $5/ACL + $1/rule + $0.60/M requests; CloudFront flat-rate Pro $15 incl. WAF |
| Logs | Log Analytics $2.30/GB (5 GB free); Basic $0.50; Auxiliary $0.05; archive $0.02/GB-mo | CloudWatch $0.50/GB (IA $0.25); storage $0.03/GB-mo |
| Email | ACS $0.25/1k + $0.00012/MB | SES $0.10/1k |
| SMS (MFA) | Entra phone auth $0.03 (low tier; US tier unconfirmed); ACS $0.0075 + $0.0025 surcharge | Twilio $0.0083 + ~$0.0045 used as proxy (AWS SMS UNKNOWN) |
| External identity | Entra External ID: 50k MAU free, then $0.03/MAU (Core meter $0.01625 also listed) | Cognito Essentials: 10k free, then $0.015/MAU (Lite $0.0055) |
| Keys/secrets | Key Vault $0.03/10k ops; HSM key $1/mo | KMS $1/key-mo; Secrets Manager $0.40/secret-mo |
| DNS | $0.50/zone-mo | $0.50/zone-mo |
| AI (first-party, same on Foundry) | Opus 5.5 $4/$20; Sonnet 5.5 $2/$10; Haiku 5.5 $0.10/$0.50 per MTok; batch -50%; cache hits 0.05× (Opus/Sonnet 5.5) | same if called directly; Bedrock price not retrieved |
| CI | GitHub Actions Linux $0.006/min; Team includes $18/mo (~3,000 min) | same |
| Identity/bank checks | Stripe Identity $1.50; SSN lookup $0.50; Financial Connections instant bank verification $1.50 (micro-deposits free); Persona $250/mo for 500, then $1.50; Plaid **UNKNOWN** (unpublished, $1.50 placeholder) | same |

## 3. Deployment configurations: monthly bill of materials at minimum provisioned capacity

All three are single shared F# monoliths with database-backed queues: no broker, no cache, no Kubernetes.

### C1: minimal shared, single region, zone-redundant HA (Azure, PAYG)

| Item | Sizing | Arithmetic | $/month |
|---|---|---|---:|
| PostgreSQL Flexible Server, zone-redundant HA | D2ds_v5 primary + standby | 2 vCore × $0.089 × 2 × 730 | 259.88 |
| PostgreSQL storage (HA) | 128 GB × 2 copies | 128 × $0.115 × 2 | 29.44 |
| PostgreSQL backup | ≤ provisioned size | free allocation | 0.00 |
| Container Apps, 2 replicas always on | 0.5 vCPU / 1 GiB each | 2 × (0.5 × 0.000024 + 1 × 0.000003) × 2,628,000 s − $5.40 grant | 73.44 |
| Blob storage + Defender for Storage | 1 scanned account | $0.0134 × 730 | 9.78 |
| Front Door Premium (managed WAF, CDN for WASM bundle) | 1 profile | base fee | 330.00 |
| DNS | 1 zone | | 0.50 |
| Log Analytics | 15 GB/mo, 5 free; 7-yr archive | (15−5) × 2.30 + 15 × 12 × 7 × $0.02 | 48.20 |
| Key Vault | ops only | | 1.00 |
| **Production fixed** | | | **752.24** |
| Non-production (35% of prod fixed, INF-ENV-001) | dev/test/staging on burstable, scale-to-zero | 0.35 × 752.24 | 263.28 |
| CI (GitHub Team allowance-sized) | | | 18.00 |
| **C1 fixed monthly floor** | | | **≈ $1,034/mo ≈ $12.4k/yr** |

Variants:
- Front Door Standard + custom WAF rules ($35 + $5) instead of Premium: prod $462, nonprod $162, floor **≈ $642/mo**.
- 1-yr reserved DB (4 vCores × $468 / 12 = $156): floor **≈ $894/mo** with Premium, **≈ $502/mo** with Standard.

AWS C1 equivalent: RDS m7g.large Multi-AZ $246.01 + gp3 128 GB × $0.23 = $29.44 + 2 Fargate ARM tasks $28.84 + ALB/LCU $22.27 + WAF $15 + DNS $0.50 + CloudWatch $5 (10 GB × $0.50) + log storage $37.80 (15 × 84 × $0.03) + KMS/Secrets $6. Prod ≈ $391, nonprod $137, CI $18, floor **≈ $546/mo ≈ $6.6k/yr** (RI: ≈ $470/mo).

### C2: shared + warm DR region

C1 plus the following.

| Item | Azure arithmetic | $/month |
|---|---|---:|
| Cross-region read replica, same size | 2 × $0.089 × 730 + 128 × $0.115 | 144.66 |
| Replication transfer | WAL ≈ 3× logical bytes × $0.02/GB (≈ $0 at 1k; $1.39 at 1M) | ~0 |
| Warm app replica in DR region (idle-billed) | (0.5 × 0.000003 + 1 × 0.000003) × 2,628,000 | 11.83 |
| Geo-redundant blobs | (GRS $0.0458 − ZRS $0.026) × stored GB | ~0.24 |
| DR Key Vault + 5 GB logs | 1 + 5 × 2.30 | 12.50 |
| **Added** | | **≈ $169** |

C2 floor: **≈ $1,203/mo** with Azure Front Door Premium. AWS: +$173 (replica $137.36, warm Fargate task + ALB $30.84, KMS + logs $4.50), giving **≈ $719/mo**. Front Door or Route 53 handles failover routing, so no second edge is needed. Nonprod is not duplicated.

### C3: C2 + isolated databases for large sponsors

Each isolated large sponsor adds an HA primary, a DR replica, a customer-managed key, a separately scanned storage account and logs:
- **Azure: $456.26/mo** = 259.88 + 29.44 + 129.94 + 14.72 + 1.00 (HSM key) + 9.78 (Defender) + 11.50 (5 GB logs).
- **AWS: $416.31/mo** = 246.01 + 29.44 + 122.64 + 14.72 + 1.00 + 2.50.

That is about $5.5k / $5.0k per isolated sponsor per year. With the base 2 sponsors (INF-ISO-001): Azure floor **≈ $2,116/mo**, AWS **≈ $1,552/mo**. At small total scale the isolation cost dominates, so it should be priced into the large sponsor's contract rather than spread across all accounts.

## 4. What scales with what

| Driver | Resources | Behaviour |
|---|---|---|
| **Fixed per environment** | HA DB minimum, 2 app replicas, edge/WAF, scanning account, DNS, keys, base logs, nonprod, CI | ≈ $1.0k/mo (Azure) or $0.55k/mo (AWS). This floor dominates below ~100k accounts. |
| **Data volume (accounts × years retained)** | DB storage (×2 for HA, ×3 with DR), backups, object storage, log archive | Grows every year even with flat accounts, because retention is 10 years. Base 278.6 KB DB/account-year × 1.25 overhead × 7 years ≈ 2.44 MB per account online. At 1M accounts: 2,438 GB → 4 TB provisioned × $0.23 = $942/mo. Documents are 1.7 MB/account-year; at 1M accounts that is 11.9 TB of blobs ≈ $244/mo. |
| **Transactions/events** | DB vCPU (step function), app CPU bursts, log ingestion, AI, email | Linear but small. DB compute steps 2→4→8 vCores. |
| **Accounts / users** | Identity MAU above the free tier, SMS MFA, email | **The largest variable lines at scale.** At 1M accounts (Azure): MAU $4,350/mo, SMS $3,000/mo, email $427/mo. |
| **Per new account (not infra)** | Identity verification + bank account verification | $0.05 / $0.45 / $0.75+ per account-year (0.10–0.25 new-account share × $0.50–$3.00). This is larger than all variable infrastructure at scale. Kept out of the infra totals. |

### When bigger tiers are needed (base drivers)

The rule (INF-DB-010..012): DB vCores = peak events/s × 0.004 vCPU-s × 2 (read amplification) / 0.5 (target utilisation) = peak eps × 0.016.
- Peak eps = accounts × 150 events/yr / 365 × 10 (December peak day) × 0.15 (peak-hour share) / 3600 = accounts × 1.712e-4.
- So required vCores = accounts × 2.74e-6.

Thresholds:
- **2 vCores** (D2ds_v5 / m7g.large) cover up to about **730k accounts**. That equals about **125 peak events/s**, a peak day of **3.0M events**, or **about 300k events/day on average**.
- **4 vCores** from about 730k accounts and **8 vCores** from about 1.46M.
- The memory rule (hot set ≤ 4 GB per vCore) does not bind at base. The hot set at 1M is 9.1 GB, slightly above the 8 GB of a 2-vCore server, so 4 vCores (16 GB) at 1M is also the memory-safe choice.
- With all high-case drivers (400 events/account, 10 ms/event, 3× reads, 40% utilisation, 15× peak), 2 vCores bind at **about 23k accounts**, 16 vCores are needed at 100k, and about 86 vCores at 1M. That is above a sensible single shared cluster (Ddsv5 tops out at 96 vCores) and is the point where CNV-ARC-001's dedicated per-sponsor databases (C3) become a capacity tool as well as an isolation tool. The 128-vCore figures in the high case should be read as "split the cluster", not as a real SKU.
- **Storage tier**: 128 GB is enough until about 44k accounts (DB 2.44 MB/account × 1.2 headroom). Then 512 GB covers up to ~175k accounts, 4 TB up to ~1.4M. Premium SSD IOPS (about 5,000 at 1 TB) exceed the base peak of about 860 IOPS at 1M (INF-DB-013), so IOPS is not a separate driver.
- **App replicas**: 2 × 0.5 vCPU cover base load to ~100k accounts. The model doubles replica size at 1M (quarterly statement runs: 1M × 12 docs/yr × 1 vCPU-s ≈ 3M vCPU-s per quarter, burst-billed at about $0.03 per 1k PDFs).

## 5. Infrastructure cost per account-year (independent estimate)

Total = 12 × (production + nonproduction + CI + AI) / accounts. AI is included (base 1 call × $0.026); identity and bank verification APIs are excluded. Bold = base PAYG; "RI" = 1-yr reserved DB; range = all-low to all-high drivers. The low and high cases compound every driver, so they are bounds, not confidence intervals.

| Provider | Config | 1k | 10k | 100k | 1M |
|---|---|---|---|---|---|
| Azure | C1 | **12.49** (RI 10.80; 10.38-20.10) | **1.32** (RI 1.15; 1.05-3.52) | **0.22** (RI 0.20; 0.11-2.33) | **0.17** (RI 0.16; 0.02-2.27) |
| Azure | C2 | **14.52** (RI 12.21; 12.41-22.17) | **1.53** (RI 1.30; 1.25-3.82) | **0.25** (RI 0.23; 0.13-2.57) | **0.18** (RI 0.18; 0.03-2.46) |
| Azure | C3 | **25.47** (RI 19.42; 17.88-49.55) | **2.62** (RI 2.02; 1.80-6.56) | **0.36** (RI 0.30; 0.19-2.84) | **0.19** (RI 0.18; 0.03-2.49) |
| AWS | C1 | **6.60** (RI 5.69; 5.26-12.27) | **0.71** (RI 0.62; 0.53-2.56) | **0.15** (RI 0.14; 0.06-2.06) | **0.12** (RI 0.11; 0.02-1.92) |
| AWS | C2 | **8.68** (RI 7.76; 7.33-14.38) | **0.92** (RI 0.83; 0.74-2.85) | **0.18** (RI 0.17; 0.08-2.27) | **0.13** (RI 0.12; 0.02-2.09) |
| AWS | C3 | **18.67** (RI 16.40; 12.33-39.36) | **1.92** (RI 1.69; 1.24-5.35) | **0.28** (RI 0.26; 0.13-2.52) | **0.14** (RI 0.13; 0.03-2.12) |

Base monthly totals:

| Provider | Config | 1k | 10k | 100k | 1M |
|---|---|---|---|---|---|
| Azure | C1 | $1,040 | $1,103 | $1,844 | $13,984 |
| Azure | C2 | $1,210 | $1,274 | $2,081 | $14,976 |
| Azure | C3 | $2,122 | $2,187 | $2,993 | $15,889 |
| AWS | C1 | $550 | $593 | $1,279 | $9,642 |
| AWS | C2 | $723 | $767 | $1,513 | $10,566 |
| AWS | C3 | $1,556 | $1,600 | $2,346 | $11,399 |

Base line items, C1, $/month:

| Line | Azure 1k | 10k | 100k | 1M | AWS 1k | 10k | 100k | 1M |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| DB compute (HA) | 260 | 260 | 260 | 520 | 246 | 246 | 246 | 492 |
| DB storage (HA) | 29 | 29 | 118 | 942 | 29 | 29 | 118 | 942 |
| DB long-term archive | 0 | 0 | 2 | 16 | 0 | 1 | 6 | 64 |
| App compute (+ALB on AWS) | 73 | 74 | 78 | 199 | 51 | 51 | 53 | 97 |
| Object storage | 0 | 2 | 24 | 244 | 0 | 2 | 17 | 172 |
| Malware scanning | 10 | 10 | 10 | 16 | 0 | 0 | 4 | 40 |
| Edge/WAF/egress | 330 | 331 | 343 | 457 | 15 | 16 | 28 | 144 |
| Logs (ingest + archive) | 49 | 54 | 109 | 652 | 43 | 47 | 89 | 501 |
| Keys/secrets + DNS | 2 | 2 | 2 | 2 | 7 | 7 | 7 | 7 |
| Email | 0 | 4 | 43 | 427 | 0 | 2 | 17 | 167 |
| SMS MFA | 3 | 30 | 300 | 3,000 | 1 | 13 | 128 | 1,280 |
| Identity MAU | 0 | 0 | 0 | 4,350 | 0 | 0 | 142 | 2,775 |
| Non-production | 264 | 266 | 322 | 976 | 137 | 139 | 190 | 778 |
| CI | 18 | 18 | 18 | 18 | 18 | 18 | 18 | 18 |
| AI inference | 2 | 22 | 217 | 2,167 | 2 | 22 | 217 | 2,167 |
| **Total** | **1,040** | **1,103** | **1,844** | **13,984** | **550** | **593** | **1,279** | **9,642** |
| DB vCores / provisioned GB / data GB | 2/128/2 | 2/128/24 | 2/512/244 | 4/4096/2438 | same | | | |

Worked examples:
- **Azure C1, 1M accounts.** SMS = 1M × 4 logins × 0.3 / 12 × $0.03 = $3,000/mo. MAU = (1M × 0.195 − 50,000) × $0.03 = $4,350/mo. AI = 1M × 1 / 12 × (8,000 × $2 + 1,000 × $10)/1e6 = $2,167/mo. DB storage = 1M × 278.6 KB × 1.25 × 7 = 2,438 GB → 4,096 GB × $0.23 = $942/mo. Total $13,984 × 12 / 1M = **$0.168/account-year**.
- **Azure C1, 1k accounts.** $1,040 × 12 / 1,000 = **$12.49/account-year**, of which $12.40 is the fixed floor.

### Comparison with prior assumptions

| Prior figure | Value | Zero-based finding |
|---|---|---|
| competitive-displacement PAR-011 `infra_per_account_owned` | $15 / **$25** / $45 per account-year (ASSUMPTION, servicing-economics placeholder) | Matches only at **~1k accounts** (Azure C1 $12.49, C3 $25.47). At ≥10k accounts the base estimate is **$0.15–$2.62**, 10–150× below $25. Even the compounded high case (≤ $6.56 at 10k, ≤ $2.84 at 100k) stays below the PAR-011 low of $15. **Recommend replacing PAR-011 with a fixed + variable form: fixed ≈ $12–25k/yr per platform (plus ≈ $5.5k/yr per isolated sponsor) + variable ≈ $0.10–0.20 per account-year (base), $1–2.5 (high).** |
| servicing-economics CST-T01..T06 | DB HA $6,237 + DR $3,119 + cloud $24,000 + nonprod $8,000 ≈ **$41.4k/yr** fixed (base), plus Datadog CST-T07..T10 | The line-by-line floor is **$12.4k/yr (C1 Azure) / $14.4k (C2)**. CST-T05's unitemised $24k "hosting, networking, WAF, KMS, object storage, egress" is about 5× the priced equivalent (Container Apps + Front Door Premium + blobs + keys ≈ $5k/yr). CST-T01 (D2/D4/D8 HA) matches the DB prices read today. |
| Unbound simplification-economics `infra_base` / `infra_per_account` | $250k/yr base + $3.00/account (MC 0.5–6) | The base is consistent only if it includes non-cloud items (observability SaaS, security tooling, SOC 2 evidence tooling, pen tests, support). The variable $3/account is ~15–20× the base estimate; even the high case at ≥100k ($1.9–2.8) is below it. |
| file-ingestion research | Object storage ≈ $305/yr and scanning ≈ $30/yr at 100k funds | Consistent: $24/mo (= $288/yr) object storage and $10–14/mo scanning at 100k in this model. |

## 6. Exclusions and open risks

- **Excluded from these totals:**
  - Observability SaaS (Datadog $15–31/host-month; CST-T07/T08).
  - Security tooling, SIEM, SOC 2 audit and pen tests.
  - Cloud support plans (UNK-001, UNKNOWN; ~$100+/mo).
  - Paid DDoS protection beyond what Front Door/Shield Standard include.
  - Payment rails, data subscriptions, people.
  - Identity and bank verification APIs (§4).
- **UNKNOWN prices with conservative placeholders:** AWS End User Messaging SMS (Twilio proxy $0.0128), Plaid (unpublished; $1.50), CloudFront PAYG per-GB (EC2 egress $0.09 used), Azure Static Web Apps (not used), Entra phone-auth US tier (low tier $0.03 assumed), and whether Entra's $0.03 Basic or $0.01625 Core MAU meter applies (conservative $0.03 used).
- **Unverified documentation facts relied on:**
  - Burstable PostgreSQL has no zone-redundant HA.
  - Backup storage is free up to 100% of provisioned storage (Azure and AWS).
  - Front Door managed WAF rules require Premium.
  - Log Analytics includes 31-day retention.
  - These were not re-verified on 2026-11-27.
- **Biggest uncertainties in per-account cost:** SMS share of MFA and MAU share, not compute. Moving MFA to passkeys/TOTP and keeping MAU within free tiers changes the 1M-account figure more than any DB decision. The biggest uncertainty in the floor is Front Door Premium vs Standard ($280/mo).
- All consumption drivers are ASSUMPTION/INFERENCE until the RM-05 PostgreSQL benchmark and a pilot measure them. Validation methods are listed per row in the assumptions register.
