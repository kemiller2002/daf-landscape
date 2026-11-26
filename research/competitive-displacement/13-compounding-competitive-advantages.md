# 13 - Compounding competitive advantages

Status: research (2026-11-26). Register: [competitive-advantages.csv](data/registers/competitive-advantages.csv) (ADV-001..014). Answers research question 8: can the technology create an advantage that compounds with each additional customer?

## Answer

**Mostly no, in the network-effect sense; partly yes, as learning and time.** None of the candidate assets is a genuine network effect where each customer makes the product more valuable to the others, because (a) customer data may not be pooled across sponsors without contractual rights (CLM-035) and (b) the public data that can be pooled is available to everyone. What can compound:

- **Time-based**: a provenance-bound temporal archive of IRS and sanctions releases cannot be recreated retroactively (ADV-002; CLM-010).
- **Learning economies**: migration adapters per incumbent source (ADV-004), identity resolutions (ADV-003) and exception-prevention rules (ADV-006) get cheaper and better with repetition.
- **Scale economies**: shared public evidence lowers registry cost per sponsor from about $115k (1 sponsor) to about $14k (30 sponsors) ([05](05-charity-registry-economics.md)).

These are modest and replicable by any well-funded entrant or incumbent within 6-24 months; the archive is the only one that strictly cannot be bought later.

## 1. Classification

| Advantage | Type | Marginal cost | Marginal customer value | Replicable in | Rights / privacy | Verdict |
|---|---|---|---|---|---|---|
| ADV-001 Shared public charity intelligence | Scale economy | ~0 | Fewer first-time exceptions | 6-12 months | Public/open only | **Parity** |
| ADV-002 Temporal archive with provenance | Time-based asset | Storage | Replay, audit defence, reinstatement semantics | Never retroactively (others may already archive) | Public | **Moderate advantage if started now** |
| ADV-003 Historical identity resolution | Learning | Low | Fewer conflicts and holds | 12-24 | Sponsor confirmations confidential | Modest |
| ADV-004 Migration adapters per source | Learning | High first, low after | Lower migration cost and risk | 12-24 | Under NDA; no personal data in adapters | Advantage only if sales cluster on one source (DEC-007) |
| ADV-005 Reusable institutional configurations | Reusable capability | Low | Faster onboarding | 6-12 | Sponsor policies confidential | Ordinary capability |
| ADV-006 Exception-prevention rules | Learning | Low | Fewer exceptions | 12-18 | De-identified aggregates only | Modest, if measured |
| ADV-007 Audit-ready control library and generated evidence | Reusable capability | Low | Lower audit cost | 12-24 | — | Advantage only after auditor acceptance |
| ADV-008 Payment connectivity / verified destinations | Scale economy; weak indirect network | $24 per enrolment | Fewer failures | 24-60 | Bank data; sharing deferred (correlated fraud risk) | **Incumbent advantage today** |
| ADV-009 Integration library | Reusable capability | Medium | Shorter implementation | 6-18 | Partner contracts | Parity; key slots taken |
| ADV-010 Operational benchmarks | Learning | Low | Benchmarking | 12 | Consent; k-suppression | Not an advantage below ~10 sponsors |
| ADV-011 Anonymised aggregate insights | Data product | Low | Market intelligence | 12 | De-identification | Not an advantage (public 990 data widely used) |
| ADV-012 AI assistance documentation | Reusable capability | Low | Faster governance approval | 6 | — | Ordinary capability |
| ADV-013 Published migration and exit commitments | Commercial term | Contingent liability | Lower perceived switching risk | 6-12 | — | Differentiator until copied (HYP-003, HYP-013) |
| ADV-014 Single ledger with deterministic controls | Architecture | — | Removes reconciliation and re-keying | 18-30 for multi-lineage incumbents | Tenant per sponsor | Real; replicable by a greenfield sub-brand |

## 2. Sponsor segregation and data rights

- **Shareable**: public facts and their history; screening results against public lists; the fact that a public-data conflict exists.
- **Not shareable without explicit contract**: sponsor decisions, charity-provided bank evidence, donor and grant data, sponsor-confirmed identity resolutions (OQ-010).
- **Shareable only as de-identified aggregates with consent**: exception rates, cycle times, prevention rule performance. With fewer than ~10 sponsors, k-suppression makes most benchmarks useless or identifying.

## 3. Negative externalities

- **Correlated error**: a wrong shared fact (bad merge, misread revocation) propagates to every sponsor at once; shared evidence needs stronger change control than a single-sponsor registry.
- **Correlated fraud**: shared bank destinations concentrate the payoff of a single account takeover; PR #88 deferred cross-sponsor bank evidence for this reason.
- **Regulatory concentration**: a shared registry that sponsors rely on becomes a de facto service provider in their audits (SOC 1 scope).

## 4. What would make an advantage compound for real

Only a **standard** others adopt (e.g. a published canonical DAF migration package and open eligibility-evidence schema that incumbents export to) would create a network effect. That is a strategic option, not an asset: it would lower everyone's switching costs, which helps an entrant more than an incumbent. It is recorded as a hypothesis for the commercial plan ([16](16-commercial-entry-strategy.md)), not as an advantage.
