# 05 - Challenging the charity registry economics

Status: research (2026-11-26). Model: [model/](model/README.md), registry inputs [registry-components.csv](data/model-inputs/registry-components.csv), [registry-alternatives.csv](data/model-inputs/registry-alternatives.csv), [registry-parameters.csv](data/model-inputs/registry-parameters.csv); outputs [results.md](model/out/results.md) §9-11 and [registry-alternatives-grid.csv](data/model-outputs/registry-alternatives-grid.csv) (672 scenarios). Monte Carlo: 2,000 seeded triangular draws.

## Answer in brief

- The ~$316k a year estimate (PR #88, rev 3) reconstructs exactly from ten components ($316,093; CLM-002).
- **39% of it is one staffing-ratio assumption**: a 1 FTE steward ($122k) not derived from workload (CLM-003). Sized by workload with a named accountable owner floor, the steward line falls to about $30-57k for one sponsor.
- **The lowest defensible run cost is about $90-120k a year for one sponsor** (5k-20k charities in use, change-driven monitoring, public data only), MC P50 $127-132k, P90 about $150-160k (CLM-004).
- **At 10 sponsors sharing public evidence the cost per sponsor is about $14-27k**; at 30 sponsors $7-14k.
- **Full periodic re-review is the dominant cost driver**: a 180-day full re-review costs about 4x change-driven monitoring at 20k charities (CLM-005).
- None of this removes human accountability: every alternative keeps a named owner (≥0.25 FTE), counsel review and an exception queue.

## 1. Reconstruction and classification

| Component | Annual (base) | Classification | Removable when |
|---|---|---|---|
| RC-01 Object storage | $276 | architecture-dependent | Never; immaterial |
| RC-02 Registry DB storage | $378 | architecture-dependent | Never; immaterial |
| RC-03 Dedicated HA registry DB | $6.2k | architecture-dependent | Shared instance acceptable unless sold as a standalone SLA service |
| RC-04 Batch compute | $3.6k | volume-dependent | Never; immaterial |
| RC-05 Paid state data, commercial sanctions | $18.0k | **optional** | Free federal data and free CSL/OFAC suffice for federal eligibility |
| RC-06 Connector maintenance (400 h) | $47.2k | volume-dependent | Scales with connector count (~40 h per connector-year) |
| RC-07 Stewardship (1 FTE) | $121.8k | **historically inherited** | Size by exception workload with a 0.25 FTE accountable-owner floor |
| RC-08 Charity support desk (0.5 FTE) | $38.6k | architecture-dependent | Removable if charities are never required to be software users |
| RC-09 Counsel (80 h) | $36.0k | legally required (establishment) | Recurring refresh ~30-40 h |
| RC-10 TPSP audit, vendor minimums, rider | $44.0k | contractually required **if** | Only if Unbound is a Nacha TPSP (OQ-009), uses bank verification vendors, or publishes facts |
| **Total** | **$316.1k** | | |

By the requested taxonomy: legally required $36k; contractually required (conditional) $44k; operationally necessary (owner floor, connectors, infra) about $60-70k; architecture-dependent $45k; volume-dependent $51k; historically inherited $122k; optional $18k; unsupported by evidence: the 1 FTE level itself (no workload derivation) and the $44k bundle (ASSUMPTION, no quotes).

## 2. Alternatives (one sponsor; 20k charities in use; 4% change rate; change-driven; 70k grants)

| Alternative | Run cost | Per grant | Human hours | Establishment (one-time) | MC P10-P90 |
|---|---|---|---|---|---|
| RA-0 Baseline reconstruction | $316k | $4.52 | 1,007 | $366k | $304-356k |
| RA-1 Public-data-only | **$115k** | $1.65 | 839 | $306k | $107-149k |
| RA-2 Fully automated evidence collection | $150k | $2.15 | 587 | $424k | $139-198k |
| RA-3 Exception-driven | $120k | $1.72 | 755 | $344k | $111-157k |
| RA-4 Shared multi-sponsor (1 sponsor) | $140k | $1.99 | 775 | $362k | $131-182k |
| RA-5 Commercially enriched | $179k | $2.56 | 671 | $348k | $171-256k |
| RA-6 Standalone service | $415k | $5.92 | 775 | $466k | $404-457k |
| RA-7 On Echelon infrastructure | $131k | $1.87 | 755 | $306k | $123-163k |

Observations:
- **Automation (RA-2) lowers human hours by ~30% but raises cost**, because it adds connectors (state registries, websites) whose maintenance outweighs the labour saved at this volume. Automation pays only when the charity population and change rate are larger.
- **Commercial enrichment (RA-5) is the most expensive single-sponsor option** apart from the standalone service, and its licence prevents sharing ([03](03-charity-data-licensing-and-access.md)).
- **Echelon infrastructure (RA-7)** saves connector hours but adds reliance cost; net it is slightly dearer than RA-3 until reuse is measured (consistent with PR #87 report 05).
- **Running the registry as a standalone service (RA-6)** costs more than the baseline because it carries its own SOC 2, sales, on-call and support.

## 3. Populations, sponsors and refresh policy

Cheapest alternative per cell at a 4% change rate (from §11 of results):

| Charities per sponsor | Sponsors | Change-driven run cost (per sponsor) | 180-day full re-review (per sponsor) |
|---|---|---|---|
| 5k | 1 | $89k (RA-1) | $198k |
| 20k | 1 | $115k (RA-1) | $482k |
| 50k | 1 | $205k (RA-3) | $1.05M |
| 20k | 3 | $184k ($61k) shared | $996k ($332k) |
| 20k | 10 | $274k ($27k) shared | $1.76M ($176k) |
| 20k | 30 | $431k ($14k) shared | $3.00M ($100k) |

Per grant, a shared change-driven registry falls from $1.65 (one sponsor) to about $0.21 at 30 sponsors. Change rate matters linearly: at 8% the human-hour line roughly doubles.

## 4. One-time versus ongoing

Establishment is $306-466k (connectors ×160 h, exception tooling 400 h, entity resolution 800 h, counsel; productisation 600 h if standalone). It is a development cost, separate from the run costs above. PR #88's $319k sits inside this range.

## 5. Lowest defensible operating cost and what must be demonstrated

**About $90-120k a year for a single sponsor, and about $15-30k per sponsor once ten sponsors share public evidence** (RECOMMENDATION, Medium for direction, Low for levels). To claim it, Unbound must demonstrate:

1. eligibility-relevant change rate at or below ~4% of charities a year (HYP-006; replay harness, OQ-003);
2. exception handling at or below ~45 minutes with 20-30% auto-resolution by deterministic rules;
3. auditor and counsel acceptance that change-driven monitoring with evidence expiry satisfies the 180-day policy (HYP-005; OQ-004);
4. that Unbound is not a Nacha TPSP in its architecture, or that the TPSP audit is carried elsewhere (OQ-009);
5. that charities are never required to use a portal (removes RC-08);
6. contractual terms that let public evidence be shared across sponsors while decisions stay per sponsor (OQ-010).

## 6. Implication

The registry is **not** a meaningful cost barrier at any realistic scale; it is a few cents to a few dollars per grant. This strengthens PR #88's conclusion that the directory is not a moat, and weakens any plan that prices charity intelligence as a premium standalone product ([16](16-commercial-entry-strategy.md)).
