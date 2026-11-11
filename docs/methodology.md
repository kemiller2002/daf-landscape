# Evidence and assurance methodology

**As of:** 2026-11-11. This repository tracks *public claims and their supporting evidence*, not a binary certification registry.

## Claim taxonomy

| Code | Meaning | What can be concluded |
|---|---|---|
| `report-reviewed` | The applicable independent auditor's report was accessed and its scope, dates, and findings reviewed | Findings limited to the named entity/system, trust criteria and report period |
| `vendor-claim-type-ii` | Official vendor/source explicitly asserts SOC 2 Type II | Only that an assertion is publicly documented; no independent verification of report contents |
| `vendor-claim-type-i` | Official vendor/source explicitly asserts SOC 2 Type I | Same; cannot infer tested operating effectiveness |
| `vendor-claim-unspecified` | Official source asserts SOC 2 without type | Type, report period and scope unknown |
| `technology-dependency` | Sponsor publicly names a third-party provider | Relationship established; no automatic extension of vendor attestation |
| `not-publicly-verified` | Scoped research did not locate applicable, credible public evidence | Neither compliant nor noncompliant is established |
| `conflicting` | Credible sources materially disagree on same entity/scope/timeframe | Needs reconciliation, do not select convenient interpretation |

**As of this baseline, zero third-party SOC 2 reports have been reviewed.** Do not relabel public claims as independently attested results or assert that a vendor is “certified.”

## What to collect before a diligence-grade decision

1. Legal entity and product/system name within **System Description**.
2. Report type (Type I as-of date versus Type II observation period); whether current, any bridge letters.
3. Independent CPA firm, opinion (unmodified/qualified/adverse/disclaimer) and exceptions/test results.
4. Trust Services Criteria actually covered (Security and, where applicable, Availability, Processing Integrity, Confidentiality, Privacy).
5. Hosting, subcontractors, processors, identity providers, custodian and payment systems; inclusive versus carve-out method.
6. **Complementary user entity controls (CUECs)** and **complementary subservice organization controls (CSOCs)**, especially sponsor approvals and financial access.
7. Known incidents, remediation, vulnerability/pentest summary, disaster recovery testing and change-management evidence.
8. **SOC 1 Type II where fund accounting and financial reporting controls are material**; SOC 2 alone cannot substitute for financial reporting assurance.
9. Application-specific evidence: access provisioning/deprovisioning, MFA/SSO, admin approval, transaction idempotency, payment reversals, ledger/reconciliation integrity, audit logs and retention.
10. Explicit confirmation of whether a DAF sponsor's systems and outsourced operator are in or out of scope.

## Source ranking

- **A: Report inspected** — independent report and applicable scope, date, and opinion established (none currently).
- **B: Primary public** — official provider, sponsor, regulator, or standards body states a specific fact. Confirms *what was published*, not the truth of performance claims.
- **C: Credible secondary** — named journalist/industry analysis, useful context requiring corroboration.
- **D: Hypothesis/inference** — interpretive assessment, never presented as observed fact.
- **U: Unknown/unassessed** — lack of evidence must not be encoded as a feature absence or failed control.

For every significant claim record the exact source URL, source date if known, retrieval/review date, and claim limitations in [sources.csv](../data/sources.csv). A recent page can contain old information; publication date and review date are different.

## How comparisons are scored

Maintain **separate** capability and security/assurance scorecards. A feature is *documented* only when a public source describes it. Otherwise mark *not assessed*, not *no*. No numeric overall ranking until products are evaluated against a shared use case, verified test scope, and weighted selection requirements.

## Important entity disambiguation

- **Ren — `reninc.com`:** philanthropic technology and administration provider.
- **Ren — `tryren.com`:** unrelated AI coaching/software company, with a separate SOC 2 Type II claim. **Never cite it as evidence for reninc.com.**

## Standards reference

[AICPA SOC suite](https://www.aicpa-cima.com/resources/landing/system-and-organization-controls-soc-suite-of-services): SOC 2 addresses trust services controls; Type I describes design at a point in time and Type II examines operating effectiveness over a defined period. [NAIC examination guidance](https://content.naic.org/sites/default/files/inline-files/Att%20A_Combined.pdf) provides a useful plain-language Type I/Type II distinction. (This repository does not independently audit those standards.)
