# 02. Minimum operating configuration

The question here is the smallest set of infrastructure and organisational obligations that lets a production-qualified Unbound serve one paying institutional customer. Each element below is tied to an Unbound requirement ([obligations extract](data/evidence/architecture-obligations.md)) and priced from public sources ([infrastructure survey](data/evidence/prices-infra.csv), [operations survey](data/evidence/prices-ops.csv)).

## Infrastructure (Echelon Foundry, entity E1)
| Element | Obligation | Cheapest credible option (annual) | Mainstream option |
|---|---|---|---|
| One managed PostgreSQL cluster: synchronous standby in-region, PITR, cross-region backup copy | CNV-ARC-001/004 (one cluster, schema per tenant; RPO 0 in region) | AWS RDS t4g.small Multi-AZ: **$660** | Azure Flexible D2ds_v5 zone-redundant HA: $3,300 (Burstable has no zone-redundant HA) |
| Two application containers and a load balancer | Modular monolith; workers as roles of the same build | AWS Fargate ×2 + ALB + IPv4: **$790** | Azure Container Apps + Front Door: ~$1,300 |
| Write-once object storage | UNB-ING-STO-005, UNB-GAP-034 (immutable backup and evidence) | S3 with Object Lock, 100 GB: **$40** | Azure immutable Blob: ~$40 |
| WAF, DNS, TLS | Public endpoints | AWS WAF + Route 53: **$140** | Cloudflare Pro $240; Front Door $440 |
| Logs and monitoring | Incident detection; SOC evidence | CloudWatch 20 GB: **$130** (Grafana Cloud Free: $0) | Azure Log Analytics: $414 |
| Status page, uptime checks, paging | UNB-AVL-011 (independent status page); two responders | Better Stack: **$700** (Grafana Free: $0) | — |
| Keys and secrets | CNV-ARC-005 (key-rotation evidence); payment-signing keys in KMS | **$150** | — |
| Staging and CI | Rehearsed, reproducible releases | **$600** | — |
| Transactional email | Notifications, acknowledgments, statements | SES: about **$0.005 per account per year** | Resend from $240 |
| AI inference | Dossier preparation, extraction, grounded answers. AI never decides (CNV-AIO-001/002) | Haiku 5.5 at $0.10/$0.50 per M tokens; Sonnet 5.5 at $2/$10. Blended **$0.006 per transaction** | — |

**Infrastructure with no customers is about $5k a year. With one customer it is about $6k.** Scale-up is linear in accounts above 5,000 (database, workers, logs), plus a read replica above 20,000 accounts. At 100 mixed customers (about 118,000 accounts) infrastructure is still under $60k a year. The Phase II placeholder of $25 per account would have been about $3M.

The extraction found a contradiction. Phase II's $25 per account and the servicing-economics cloud line of about $35k a year differ about seven-fold. Bottom-up pricing resolves it: infrastructure is about $0.3–0.6 per account per year at scale.

## Organisational obligations
| Obligation | Basis | Minimum mechanism | Trigger |
|---|---|---|---|
| Two non-author approvers for control-module changes | CNV-PLT-010 | Founder or employee as author; contracted independent reviewers on retainer (~40 h a year each plus an emergency-availability clause) | First customer |
| Two-person break-glass for production DB and operator access | CNV-PLT-010, CNV-PLT-007 | The secondary on-call holds the second key | First customer |
| Two-deep on-call (incident commander and backup) | ORG-R14; typical contract response objectives | Founder plus a regular contractor (≥ 400 h a year) or a contracted secondary on-call (~$28k a year) | First customer, typical contract |
| SOC 2 Type II | Institutional due diligence (contract-typical) | Annual audit ($7–40k) + compliance platform ($4–15k) + ~100 h of evidence | First customer |
| SOC 1 Type II | CNV-GOV-001 (mandatory before the first staffed client); user-auditor reliance under licensing | Annual audit ($20–50k) | Full service: customer 1. Limited operations: customer 2. Licensing: customer 3 |
| Pen test | SOC2-016 (recorded program) | Annual test and retest ($6–30k) | First customer |
| Tech E&O and cyber insurance | Liability once customer data is held | $1M ($2–10k) + uplift to $2M ($2–9k) | First customer |
| Crime insurance (incl. third-party and social engineering) | Echelon Foundry staff prepare payments | $1M ($1.6–5.5k) | Limited operations and full service only |
| Business-day operations continuity | CNV-PLT-005 (complaints acknowledged in 2 business days); exception queues | Two distinct operations people, or a contracted backup analyst | Limited operations and full service only |
| Retention: 10 years for transactions, 7 for financial records, SOC period + 3 years | CNV-PLT-004/009 | Write-once storage lifecycle | Always |
| Counsel | Open legal questions (TPSP role, source rights, IP mechanics) | $3–25k a year + $2–15k per new contract | First customer |

## Mandatory versus contractual
At one licensing customer:
- **Mandatory obligations (tier 0)** cost about **$162k a year**.
- **Typical institutional contracts (tier 1)** add about **$40k**: SOC 2 Type II, pen test, compliance platform, the $2M insurance uplift and two-deep on-call.
- **Demanding bank-grade contracts (tier 2)** add another about **$123k**: SOC 1 under licensing, $5M limits, a 24×7 rotation, a vCISO, a warm standby region and escrow.

Full tier table: [`results.md` §3](data/outputs/results.md).

## What is deliberately absent
- **No salaried CEO, CTO, CFO or salesperson.** The founder holds management, and residual work goes to contractors or workload-derived hires (gate V6).
- **No D&O insurance or fractional CFO.** Both are discretionary while there are no outside investors or directors.
- **No licensed charity data.** The IRS and OFAC sources are authoritative and free.
- **No commercial sanctions screening.** The validated in-house matcher runs over free lists.
- **No separate Unbound legal entity.** It is deferred until there is a demonstrated need (owner direction, 2026-11-27).
