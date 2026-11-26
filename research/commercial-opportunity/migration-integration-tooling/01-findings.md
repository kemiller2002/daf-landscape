# Migration and integration tooling: findings for the DAF market

Date: 2026-11-26. Evidence IDs (EV-MIT-NNN) are in `data/commercial-opportunity/migration-integration-tooling/evidence-register.csv`. EV-COM IDs are in the capital-minimization register.

## F1. The generic data integration market is cheap per unit, consolidating, and aimed at warehouses

- **Consolidation.** The generic market consolidated through 2025–2026:
  - Salesforce closed its acquisition of Informatica on 2025-11-18 (EV-MIT-001).
  - Fivetran acquired Tobiko/SQLMesh in 2025 and completed its merger with dbt Labs on 2026-06-01 (EV-MIT-002).
  - Prefect announced the acquisition of Dagster in 2026-07; closing was not confirmed (EV-MIT-003).
  - Qlik retired Talend Open Studio on 2024-01-31 (EV-MIT-004).
- **Price per unit is low at sponsor volumes.** Some examples:
  - Fivetran gives 500k monthly active rows free, with a $5 minimum per connection from 2026-01 (EV-MIT-005).
  - Airbyte Cloud starts at $20 for 5 credits (EV-MIT-006).
  - AWS Glue costs $0.44 per DPU-hour (EV-MIT-007).
  - Azure Data Factory costs $1 per 1,000 activity runs (EV-MIT-008).

  For one sponsor's recurring feeds (IRS BMF weekly, custodian files daily), cash tool cost is plausibly hundreds to low thousands of dollars a year. Price is therefore **not** the barrier to migration.
- **None of the surveyed products loads data into an application through its business rules** with blocking reconciliation gates and an evidence package. They load into warehouses, lakes or SaaS APIs (EV-MIT-009). A DAF migration has to post opening balances, grants and contributions under fund-accounting invariants. That is domain work which generic ELT does not do.

## F2. DAF migrations need things the tools do not supply

The repository's own evidence:

- **Ren** sells data migration onto DFX as a paid add-on (EV-COM-023).
- **AEF** kept only 2 years of self-service history after migrating to Ren (EV-COM-024).
- **8 community-foundation vendor migrations** happened in 2022–2026, 6 of them to Foundant (EV-COM-018).
- **Foundant** offers a no-cost proof-of-concept migration before a contract is signed (EV-COM-031, search snippet, quality C).
- **No public export schemas** exist for Ren/iPhi DFX, TIFIN Give, GiftingNetwork, DAFtech or the NPact FIMS/DonorCentral systems. Among top-10 sponsors, no donor-facing machine-readable export exists beyond grants-paid exports (see `research/ren-iphi-platform-contract-architecture-integration-audit-2026-11-12.md` and `research/revenue-retention-and-switching-2026-11-11.md`).

What is therefore hard is not moving rows. It is:

1. mapping each source system's data model, which means a separate mapping per vendor (report 12 warning);
2. proving completeness and balance per fund, so that opening balance plus movements equals the closing balance;
3. preserving history and lineage;
4. fencing the legacy writer during cutover.

Generic tools address only parts of (1).

## F3. Implications for OPP-10

| Hypothesis | Assessment | Confidence |
|---|---|---|
| OPP-10 can be served by licensing a generic ELT tool plus services | Weak. The tool solves transport. Reconciliation, evidence and domain loading remain bespoke on every engagement. | Medium |
| A reusable importer with per-vendor mapping packages lowers the marginal cost of each migration | Plausible **only after** the first customer-authorized sample per vendor. Packages for undocumented vendors cannot be built from public sources (D-MIT-002). | Low–medium |
| A canonical historical import (target-side package) plus migration rehearsal lowers migration risk for every sponsor regardless of vendor | **Adopted by owner direction (2026-11-26):** canonical import and rehearsal are required in Unbound release 1, and basic packages are not conditioned on a signed customer (D-MIT-002 revised). Vendor-specific turnkey packages follow later. | Medium (no real export rehearsed yet; OD-M-14) |
| Reconciliation evidence ("independent assurance") is a sellable differentiator | Consistent with AEF's lost history and with Foundant pre-sale PoCs signalling buyer anxiety. Untested with buyers. | Low |
| Building an in-house engine is justified by licence savings | **Rejected.** Licence costs are small (F1). Any justification must rest on domain loading, evidence, data residency and reuse across products (D-MIT-001). | High |

## F4. Open questions for the market-validation programme

- Would sponsors pay for an independent reconciliation report on a migration performed by another vendor? This would extend the interview guide in `../market-validation/interview-program.md`.
- How many history years do sponsors require after migration? AEF kept 2.
- Will a vendor release an export sample under NDA for package development, and on what confidentiality terms?
