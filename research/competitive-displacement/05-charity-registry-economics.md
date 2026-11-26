# 05 - Challenging the charity registry economics

Status: research (2026-11-26; revision 2 after adversarial review, see [20](20-adversarial-review.md)). Model: [model/](model/README.md), registry inputs [registry-components.csv](data/model-inputs/registry-components.csv), [registry-alternatives.csv](data/model-inputs/registry-alternatives.csv), [registry-parameters.csv](data/model-inputs/registry-parameters.csv); outputs [results.md](model/out/results.md) §9-11 and [registry-alternatives-grid.csv](data/model-outputs/registry-alternatives-grid.csv) (672 scenarios). Monte Carlo: 2,000 seeded triangular draws.

## Answer in brief

- The ~$316k a year estimate (PR #88, rev 3) reconstructs exactly from ten components ($316,093; CLM-002).
- **39% of it is one staffing-ratio assumption**: a 1 FTE steward ($122k) not derived from workload (CLM-003). Sized by workload with a named accountable owner floor, the steward line falls to about $30-57k for one sponsor.
- **Revision 2** (CHL-047, CHL-048, CHL-052): evidence expiry now runs at 0.5 refreshes per charity-year (was 0.1, inconsistent with the expiry rules in [04](04-charity-intelligence-architecture.md)); name-match alerts from CSL, SAM and FAC feeds are added; the commercial licence is anchored to Candid's $2,750 list price.
- **The lowest defensible run cost is about $90k a year for a 5k-charity sponsor and about $160-170k for 20k charities** (change-driven monitoring, public data only). MC P50 for 20k charities is about $202k, P90 about $276k (CLM-004, revised). This is a **marginal** cost that relies on platform-wide security, SOC and insurance; a standalone-equivalent figure is about $175k+ before SOC and sales (CHL-030).
- **At 10 sponsors sharing public evidence the cost per sponsor is about $18-42k**; at 30 sponsors $9-23k. Per-sponsor sharing economics depend on an untested overlap exponent (0.3-0.8; CHL-032).
- **Full periodic re-review is the dominant avoidable driver**: a 180-day full re-review costs about 3x change-driven monitoring at 20k charities (CLM-005). The 180-day cycle is a sponsor policy, not law (CHL-035).
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
| RA-0 Baseline reconstruction (components as published) | $316k | $4.52 | 1,707 | $366k | $316-432k |
| RA-1 Public-data-only | **$162k** | $2.32 | 1,532 | $306k | $151-276k |
| RA-2 Fully automated evidence collection | $196k | $2.81 | 1,270 | $424k | $186-317k |
| RA-3 Exception-driven | $167k | $2.38 | 1,445 | $344k | $156-284k |
| RA-4 Shared multi-sponsor (1 sponsor) | $186k | $2.66 | 1,465 | $362k | $178-306k |
| RA-5 Commercially enriched (Candid-anchored licence) | $181k | $2.58 | 1,357 | $348k | $180-308k |
| RA-6 Standalone service | $453k | $6.47 | 1,465 | $466k | $443-575k |
| RA-7 On Echelon infrastructure | $177k | $2.53 | 1,445 | $306k | $167-291k |

Observations:
- **Automation (RA-2) lowers human hours by ~30% but raises cost**, because it adds connectors (state registries, websites) whose maintenance outweighs the labour saved at this volume. Automation pays only when the charity population and change rate are larger.
- **Commercial enrichment (RA-5) is now close to the public-data options** once anchored to Candid's list price; its licence still prevents sharing ([03](03-charity-data-licensing-and-access.md)), and it shows that paid eligibility evidence is cheap, which undercuts any standalone charity-intelligence product.
- **Echelon infrastructure (RA-7)** saves connector hours but adds reliance cost; net it is slightly dearer than RA-3 until reuse is measured (consistent with PR #87 report 05).
- **Running the registry as a standalone service (RA-6)** costs more than the baseline because it carries its own SOC 2, sales, on-call and support.

## 3. Populations, sponsors and refresh policy

Cheapest alternative per cell at a 4% change rate (from §11 of results):

| Charities per sponsor | Sponsors | Change-driven run cost (per sponsor) | 180-day full re-review (per sponsor) |
|---|---|---|---|
| 5k | 1 | $89k (RA-1) | $199k |
| 20k | 1 | $162k (RA-1) | $483k |
| 50k | 1 | $321k (RA-3) | $1.05M |
| 5k | 10 | $178k ($18k) shared | $513k ($51k) |
| 20k | 10 | $421k ($42k) shared | $1.76M ($176k) |
| 20k | 30 | $687k ($23k) shared | $3.01M ($100k) |

Per grant, a shared change-driven registry falls from $2.32 (one sponsor) to about $0.33 at 30 sponsors. Change rate matters linearly: at 8% the human-hour line roughly doubles.

## 4. One-time versus ongoing

Establishment is $306-466k (connectors ×160 h, exception tooling 400 h, entity resolution 800 h, counsel; productisation 600 h if standalone). It is a development cost, separate from the run costs above. PR #88's $319k sits inside this range.

## 5. Lowest defensible operating cost and what must be demonstrated

**About $90-170k a year for a single sponsor (5k-20k charities), and about $18-42k per sponsor once ten sponsors share public evidence**, as a marginal cost on a platform that already carries security, SOC and insurance (RECOMMENDATION; Medium for direction, Low for levels; conditional on V-3/V-7 measurements, CHL-110). To claim it, Unbound must demonstrate:

1. eligibility-relevant change rate at or below ~4% of charities a year (HYP-006; replay harness, OQ-003);
2. exception handling at or below ~45 minutes with 20-30% auto-resolution by deterministic rules;
3. that sponsors will adopt change-driven monitoring with evidence expiry in place of a 180-day full re-review policy (HYP-005; OQ-004);
4. that the Nacha TPSP audit sits with the payments platform, not the registry: a platform that creates ACH files is almost certainly a TPSP (CHL-037), so the cost moves to platform fixed cost, it does not disappear;
5. that charities are never required to use a portal (removes RC-08);
6. contractual terms that let public evidence be shared across sponsors while decisions stay per sponsor (OQ-010).

## 6. Implication

The registry is **not** a meaningful cost barrier at any realistic scale; it is a few cents to a few dollars per grant, and paid alternatives start at $2,750 a year. This strengthens PR #88's conclusion that the directory is not a moat, and weakens any plan that prices charity intelligence as a premium standalone product ([16](16-commercial-entry-strategy.md)).
