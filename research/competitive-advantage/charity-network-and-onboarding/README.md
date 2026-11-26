# Charity networks and frictionless onboarding: competitive-advantage research (2026-11-26)

This package asks two questions about Unbound's competitors:

- **Track A:** how can Unbound neutralise incumbents' charity-network advantages (directories, shared vetting, electronic payment networks)?
- **Track B:** how can Unbound make institutional onboarding and migration predictable?

The package is research and requirements discovery only. It contains no production implementation. It is not legal advice and not independent assurance.

Start with [00-executive-summary.md](00-executive-summary.md).

| # | File | Agent |
|---|---|---|
| 00 | [Executive summary](00-executive-summary.md) | Coordinator |
| 01 | [Research methodology and evidence classes](01-research-methodology.md) | Coordinator |
| 02 | [Ren network decomposition](02-ren-network-decomposition.md) | REN |
| 03 | [Competitor capability matrix](03-competitor-capability-matrix.md) | CMP |
| 04 | [Authoritative charity data inventory](04-authoritative-charity-data-inventory.md) | DAT |
| 05 | [Charity registry design](05-charity-registry-design.md) | REG |
| 06 | [Continuous vetting](06-continuous-vetting.md) | REG |
| 07 | [Payment network landscape](07-payment-network-landscape.md) | PAY |
| 08 | [Organic network growth](08-organic-network-growth.md) | PAY |
| 09 | [Charity network security](09-charity-network-security.md) | SEC |
| 10 | [Institutional onboarding landscape](10-institutional-onboarding-landscape.md) | ONB |
| 11 | [Cross-industry migration research](11-cross-industry-migration-research.md) | XIN |
| 12 | [Declarative sponsor configuration](12-declarative-sponsor-configuration.md) | CFG |
| 13 | [Pre-contract migration assessment](13-pre-contract-migration-assessment.md) | MIG |
| 14 | [Canonical migration model](14-canonical-migration-model.md) | MIG |
| 15 | [Migration factory](15-migration-factory.md) | MIG |
| 16 | [Financial reconciliation](16-financial-reconciliation.md) | MIG |
| 17 | [Cutover and recovery](17-cutover-and-recovery.md) | MIG |
| 18 | [Integration onboarding](18-integration-onboarding.md) | CFG |
| 19 | [Participant onboarding](19-participant-onboarding.md) | CFG |
| 20 | [Economic analysis](20-economic-analysis.md) | ECO |
| 21 | [Competitive performance targets](21-competitive-performance-targets.md) | Coordinator |
| 22 | [Adversarial review](22-adversarial-review.md) | ADVA, ADVB, ADVX + coordinator |
| 23 | [Strategic recommendations](23-strategic-recommendations.md) | Coordinator |
| 24 | [Unresolved questions](24-unresolved-questions.md) | Coordinator |
| 25 | [Source register](25-source-register.md) | Coordinator |

## Data and scripts

`data/` holds the machine-readable registers:

- source fragments and the merged `source-register.csv`;
- competitor, provider, onboarding and threat matrices;
- the vetting state model (JSON);
- identity-resolution and migration test cases;
- reconciliation gates;
- economic parameters and outputs;
- adversarial findings.

`scripts/` holds stdlib-only Python 3 in functional style:

| Command | What it does |
|---|---|
| `python3 -I scripts/economic_model.py --check` | Recomputes the economic scenarios and diffs them against the committed output |
| `python3 -I scripts/merge_source_register.py --check` | Validates and merges the sources and fails on an unresolved citation |
| `python3 -I scripts/pay_enrollment_growth_model.py <repo root>` | Network growth model |
| `scripts/advx_sensitivity.py` | Adversarial sensitivity runs |
| `scripts/ren_*.py`, `scripts/reg_source_change_volumes.py`, `scripts/dat_irs_*.py`, `scripts/adva_*.py` | Rebuild the IRS counts. They need the IRS bulk files, which are not committed; download URLs are in `data/charity-data-sources.csv` |

## Requirements

The proposed requirements derived from this research are in `kemiller2002/unbound`, `requirements/discovery/2026-11-26-charity-network-and-onboarding/`:

- 26 UNB-CNET and 33 UNB-ONB records;
- 13 owner decisions (OD-CNO-01..13), registered in Unbound's open-question register.

None is adopted, implemented or validated.
