# 24 — Cross-repository implications

Register: [`cross-repository-implications.csv`](data/registers/cross-repository-implications.csv) (XRI-ZB-01..15). **All are proposals.** No file outside `daf-landscape/research/zero-based-operational-economics/` was changed; no ratified requirement or owner decision was modified.

## Repository verification (2026-11-27)

| Repository | Access | Notes |
|---|---|---|
| kemiller2002/daf-landscape | push | primary; branch `claude/zero-based-unbound-economics-kia9lj` |
| kemiller2002/unbound | read (public) | read at `79b9258`; no Praxis, no CI |
| kemiller2002/transitus | read | phase 0, no code |
| kemiller2002/beneficium | **not accessible / not found** | blocker recorded; research held here |
| kemiller2002/echelon-organization-administration | read (private, attached) | business plan finance sections empty |
| kemiller2002/echelon-foundry, echelon-registry, praxis, strata, forma, limen, folio, conditor, arca, fides, echelon-assurance and others | read | verified responsibilities in [08](08-shared-echelon-resource-economics.md) |

## Unbound (requirement refinements, traceable)

XRI-ZB-01..09: economic impact records on material requirements; board delegation as activation gate (CNV-GRT-001); determination reuse and trigger calibration for Tier-2 review (CNV-GRT-011); continuous close with a shared workbench (UNB-ACC-017/020); tiered December compliance SLAs; notification-first contributions (UNB-GAP-013); single sampling plan, single reconciliation attestation, weekly NAV sample; an explicit sponsor-retained responsibilities list; Praxis, CI and operational measurement hooks. Each preserves the underlying control objective ([21](21-requirement-economic-impact.md)).

## Beneficium (held here; repository absent)

XRI-ZB-10: automated acquisition (5 connectors for the directory, 13 for continuous monitoring), temporal history, change events consumed by Unbound, evidence reuse across sponsors, reproducible snapshots, drift alarms, operational measurement of connector hours and stale-source share. **Production-scale datasets must not be stored in GitHub** (≈ 190 GB over 10 years belongs in object storage).

## Transitus

XRI-ZB-11: low-cost recurring ingestion; connector maintenance measured per connector; incremental processing; data-quality automation; mappings certified once per counterparty and reused across sponsors; resource metering.

## Echelon Organization Administration

XRI-ZB-12: the allocation method in [08](08-shared-echelon-resource-economics.md) §3; cost-centre activation criteria (shared platform engineering once two products are in production; shared assurance once N ≥ 2); responsibility models per configuration ([07](07-minimum-viable-organization.md)). Existing owner decisions are preserved: OD-M-08 (software first, staffed administration second), OD-P-GOV (SOC 1 readiness before first staffed client), OD-M-14 (no design partner), DF-ASR-2026-0D0F (no consulting spend — flagged as conflicting, OD-ZB-02).

## Praxis

XRI-ZB-13: optional `economic_impact` front matter; validator for requirement-activity links; economic regression report as work-item evidence; populated token and human-time telemetry. Requires owner approval (OD-ZB-05) before any enforcement.

## Echelon Foundry and Registry

XRI-ZB-14: record maturity and ownership boundaries (Transitus phase 0; monitoring, hosting and donor identity absent; Limen does no identity; Folio has no PDF engine; Arca unsuitable for a regulated ledger; PolyForm Noncommercial licensing) so other initiatives do not assume them.

## DAF Landscape (preserved baseline)

XRI-ZB-15: correct register drift in `research/competitive-displacement/data/registers/economic-assumptions.csv` and annotate the double counts in [03](03-cost-assumption-audit.md). The baseline itself is left unchanged by this initiative so the comparison remains reproducible.

## Architecture risks recorded for Unbound

Connection pooling under role-per-sponsor; tenant-scoped restore in a shared cluster (whole-server PITR); isolated-database operational overhead in C3; the compute change point (~730k accounts base, ~23k accounts high case).
