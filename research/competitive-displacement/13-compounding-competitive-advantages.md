# 13 - Compounding competitive advantages

Status: research (2026-11-26; revision 2 after adversarial review, see [20](20-adversarial-review.md)). Register: [competitive-advantages.csv](data/registers/competitive-advantages.csv) (ADV-001..014). Answers research question 8: can the technology create an advantage that compounds with each additional customer?

## Answer

**Mostly no, in the network-effect sense; partly yes, as learning and time.** None of the candidate assets is a genuine network effect where each customer makes the product more valuable to the others, because (a) customer data may not be pooled across sponsors without contractual rights (CLM-035) and (b) the public data that can be pooled is available to everyone. What can compound:

- **Time-based (revised: weak)**: revision 1 called the temporal archive unbuyable. It is not: the Urban Institute's NCCS publishes raw monthly BMF releases from June 2023 and harmonised vintages back to 1989, Candid keeps revocation and reinstatement history, and the IRS revocation file is cumulative (CHL-001, CHL-046; CLM-010 now contradicted). Only Pub 78 snapshots and hash-level provenance are scarce.
- **Learning economies**: migration adapters per incumbent source (ADV-004), identity resolutions (ADV-003) and exception-prevention rules (ADV-006) get cheaper and better with repetition.
- **Scale economies**: shared public evidence lowers registry cost per sponsor from about $162k (1 sponsor) to about $23k (30 sponsors) ([05](05-charity-registry-economics.md)).

These are modest and replicable by any well-funded entrant or incumbent within 6-24 months, and **incumbents are ahead on repetition today** (Foundant 700+ foundations; Ren's absorbed books; CHL-002).

## 1. Classification

| Advantage | Type | Marginal cost | Marginal customer value | Replicable in | Rights / privacy | Verdict |
|---|---|---|---|---|---|---|
| ADV-001 Shared public charity intelligence | Scale economy | ~0 | Fewer first-time exceptions | 6-12 months | Public/open only | **Parity** |
| ADV-002 Temporal archive with provenance | Time-based asset | Storage | Replay, audit defence, reinstatement semantics | Weeks (NCCS archive; Candid history) | Public | **Parity / hygiene**; narrow edge only for Pub 78 snapshots and provenance (revised) |
| ADV-003 Historical identity resolution | Learning | Low | Fewer conflicts and holds | 12-24 | Sponsor confirmations confidential | Modest |
| ADV-004 Migration adapters per source | Learning | High first, low after | Lower migration cost and risk | Incumbents ahead today | Under NDA; no personal data in adapters | Advantage only if sales cluster on one source (DEC-007); adapters drift with incumbent report changes |
| ADV-005 Reusable institutional configurations | Reusable capability | Low | Faster onboarding | 6-12 | Sponsor policies confidential | Ordinary capability |
| ADV-006 Exception-prevention rules | Learning | Low | Fewer exceptions | 12-18 | De-identified aggregates only | Modest, if measured |
| ADV-007 Audit-ready control library and generated evidence | Reusable capability | Low | Lower audit cost | 12-24 | — | Advantage only after auditor acceptance |
| ADV-008 Payment connectivity / verified destinations | Scale economy; weak indirect network | $24 per enrolment | Fewer failures | 24-60 | Bank data; sharing deferred (correlated fraud risk) | **Incumbent advantage today** |
| ADV-009 Integration library | Reusable capability | Medium | Shorter implementation | 6-18 | Partner contracts | Parity; key slots taken |
| ADV-010 Operational benchmarks | Learning | Low | Benchmarking | 12 | Consent; k-suppression | Not an advantage below ~10 sponsors |
| ADV-011 Anonymised aggregate insights | Data product | Low | Market intelligence | 12 | De-identification | Not an advantage (public 990 data widely used) |
| ADV-012 AI assistance documentation | Reusable capability | Low | Faster governance approval | 6 | — | Ordinary capability |
| ADV-013 Published migration and exit commitments | Commercial term | Contingent liability | Lower perceived switching risk | 0-3 months (a contract clause) | — | **Not an advantage**: incumbents can match it and back it with balance sheet; credible from an entrant only with escrow, insurance or a partner's backing (CHL-004) |
| ADV-014 Single operational ledger with deterministic controls | Architecture | — | Removes internal re-keying; custodian, bank and GL reconciliation remain (CHL-059) | 18-30 if W06 holds; parity with Foundant in CFs | Tenant per sponsor | **Unverified**: rests on W06, a hypothesis (CHL-009) |

## 2. Sponsor segregation and data rights

- **Shareable**: public facts and their history; screening results against public lists; the fact that a public-data conflict exists.
- **Not shareable without explicit contract**: sponsor decisions, charity-provided bank evidence, donor and grant data, sponsor-confirmed identity resolutions (OQ-010).
- **Shareable only as de-identified aggregates with consent**: exception rates, cycle times, prevention rule performance. With fewer than ~10 sponsors, k-suppression makes most benchmarks useless or identifying.

## 3. Negative externalities

- **Correlated error**: a wrong shared fact (bad merge, misread revocation) propagates to every sponsor at once; shared evidence needs stronger change control than a single-sponsor registry.
- **Correlated fraud**: shared bank destinations concentrate the payoff of a single account takeover; PR #88 deferred cross-sponsor bank evidence for this reason.
- **Regulatory concentration**: a shared registry that sponsors rely on becomes a de facto service provider in their audits (SOC 1 scope).

## 4. What would make an advantage compound for real

Only a **standard** others adopt (e.g. a published canonical DAF migration package and open eligibility-evidence schema that incumbents export to) would create a network effect. Incumbents with the largest installed bases have no reason to adopt an entrant's schema; a standard would need a regulator, an industry body or a dominant sponsor coalition to drive it, and none is in sight (CHL-011). That is a strategic option, not an asset: it would lower everyone's switching costs, which helps an entrant more than an incumbent. It is recorded as a hypothesis for the commercial plan ([16](16-commercial-entry-strategy.md)), not as an advantage.
