# File ingestion, information exchange and straight-through processing in DAF administration (2026-11-26)

How information enters, moves through and is processed by donor-advised fund sponsors; which of those flows can be
eliminated, prevented, processed deterministically or assisted by AI; and what it costs. Industry research only — no
product requirements.

| # | Chapter |
|---|---|
| 00 | [Executive findings](00-EXECUTIVE-FINDINGS.md) |
| 01 | [Research methodology](01-METHODOLOGY.md) |
| 02 | [Industry evidence catalog (per organization)](02-INDUSTRY-EVIDENCE-CATALOG.md) |
| 03 | [DAF ingestion workflow inventory](03-DAF-INGESTION-WORKFLOW-INVENTORY.md) (115 workflows, generated) |
| 04 | [Adjacent industry analysis](04-ADJACENT-INDUSTRY-ANALYSIS.md) |
| 05 | [File format inventory](05-FILE-FORMAT-INVENTORY.md) |
| 06 | [Delivery mechanism analysis](06-DELIVERY-MECHANISMS.md) |
| 07 | [Institutional integration research](07-INSTITUTIONAL-INTEGRATION.md) |
| 08 | [Straight-through processing opportunities](08-STP-OPPORTUNITIES.md) |
| 09 | [Economic analysis](09-ECONOMIC-ANALYSIS.md) (model outputs generated) |
| 10 | [Competitor capability comparison](10-COMPETITOR-CAPABILITY-COMPARISON.md) |
| 11 | [Evidence gaps](11-EVIDENCE-GAPS.md) |
| 12 | [Source register](12-SOURCE-REGISTER.md) (generated) |
| 13 | [Security, storage and AI evidence](13-SECURITY-STORAGE-AND-AI-EVIDENCE.md) |
| — | [Research ledger: provenance, checkpoints, disagreements, decisions](RESEARCH-LEDGER.md) |

**Data** ([`data/file-ingestion-2026-11/`](../../data/file-ingestion-2026-11/)): `evidence.csv` (263 rows), `sources.csv`,
`workflow-inventory.csv`, `formats.csv`, `economics-parameters.csv`, `economics-results.csv`, `economics-onboarding.csv`.
**Scripts**: [`scripts/fie_economics.py`](../../scripts/fie_economics.py), [`scripts/fie_validate.py`](../../scripts/fie_validate.py).

Cross-repository links (product requirements are deliberately kept out of this repository):
[product requirements derived from this research](https://github.com/kemiller2002/unbound/tree/main/requirements/discovery/2026-11-26-file-ingestion)
and [reusable engineering requirements](https://github.com/kemiller2002/echelon-organization-administration/tree/main/application-governance/file-ingestion).
