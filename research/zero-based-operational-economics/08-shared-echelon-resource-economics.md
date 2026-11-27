# 08 — Shared Echelon resource economics

Register: [`shared-capabilities.csv`](data/registers/shared-capabilities.csv) (SC-001..032). Notes: [echelon-shared-and-development-notes.md](data/evidence/echelon-shared-and-development-notes.md). Allocation lines: FC-101..FC-105 (View 2), FC-201..FC-208 (View 3) in [`fixed-costs.csv`](data/model-inputs/fixed-costs.csv).

## 1. What actually exists (verified by reading code, not names)

| Component | Verified responsibility | Status for Unbound |
|---|---|---|
| Praxis | repository operating system: work protocol, provenance, registries, validation | production for governance; **not installed in Unbound** |
| Strata | schema governance | pilot |
| Forma / Limen | UI framework / TypeScript browser kernel (**no identity**) | in development |
| Folio | print markup (**no PDF engine**) | in development |
| Conditor | build/packaging | production for Echelon repos |
| Arca | records stored in GitHub — **unsuitable for a regulated ledger** | not usable for Unbound's ledger |
| Fides | sign-in through GitHub only | not donor identity |
| Aegis | fault handling (not security) | — |
| Transitus | data integration | **phase 0, no code** |
| Echelon.Execution (durable queue) | incubated inside Unbound | Unbound is its only user |
| echelon-assurance | SOC 1/SOC 2 research and control design | design stage |
| Monitoring/logging, hosting, donor identity, support, CRM, incident paging, deployment | — | **absent** (monitoring deferred by owner 2026-11-25) |
| Static analysis / dependency scanning | — | absent in all 11 CI configurations inspected |

Most components are licensed PolyForm Noncommercial. No cloud provider has been chosen.

## 2. Three economic views (model)

| View | $100M (CFG-5) | $500M (CFG-5) | $1B (CFG-5) | $500M (CFG-2) |
|---|---:|---:|---:|---:|
| 1 Incremental cash | $1.83M | $2.22M | $2.86M | $1.44M |
| 2 Allocated economic | $2.02M | $2.41M | $3.05M | $1.64M |
| 3 Standalone replacement | $2.81M | $3.20M | $3.84M | $2.42M |

- **View 2 − View 1 ≈ $0.19M:** founder hours at $200/h (400 h) plus Unbound's share of shared component maintenance (35% of $150k), development tooling (35% of $24k), legal/corporate (25% of $20k) and the assurance programme (50% of $90k). Echelon accounting is not allocated because none exists; Unbound's own bookkeeping is incremental cash (FC-020).
- **View 3 − View 1 ≈ $1.0M:** own maintainers for components Unbound depends on (1.5 FTE base), own finance, legal, tooling, leadership beyond activity workload, G&A, full assurance programme, standalone sales.

## 3. Allocation methodology (proposed)

| Shared cost | Driver (measurable) | Proxy until measured |
|---|---|---|
| Founder time | Praxis work-item hours by initiative tag | none: 400 h/yr is an assumption (owner decision OD-ZB-01) |
| Shared component maintenance | work items tagged by requesting product; consumer counts in Registry/Conditor manifests | Unbound's share of non-merge commits: 43% (31 days) to 65% (6 days); 35% used |
| Development tooling and agent usage | Praxis token telemetry per work item (fields exist, unpopulated) | same 35% |
| Assurance programme | echelon-assurance scaling: 1 + (N−1) × scaling per product | 50% until a second product is in scope |
| Infrastructure | metered resources tagged by product/sponsor | resource model ([12](12-infrastructure-economics.md)) |
| Legal/corporate | initiative share | 25% |

Rules applied: no reusable component is charged wholly to Unbound; shared capacity is finite (founder ~1,800 h/yr across 30 initiatives, 16 active); founder labour is never treated as free.

## 4. Transfer, not elimination

The "shared organisation" argument is real only where a capability exists and has more than one consumer. Today:

- Transitus and Echelon.Execution have **Unbound as their only consumer** — their cost is Unbound's cost under any honest allocation.
- Monitoring, hosting, donor identity, support and deployment **do not exist** — Unbound must fund them (they appear as View 1 cash: FC-009, FC-010, FC-016, infrastructure, TECHOPS activities).
- Echelon's productivity advantage is unmeasured: 5,609 commits with one human identity, no effort or cost telemetry ([16](16-software-development-economics.md)).

**Where sharing materially changes the result:** if platform engineering (≈ $0.9M of the ≈ $2.2M reference) were genuinely shared with two or more other products in production, Unbound's View 1 could fall by roughly $0.3-0.5M (inference; not modelled as base because no second product exists). That is the single largest available structural saving, and it depends on Echelon portfolio decisions, not on Unbound design.

## 5. Opportunity cost

Founder time at $200/h is a wage proxy. For an owner with 30 initiatives, the true opportunity cost is the value forgone elsewhere, which cannot be measured from records (ADV-BI-017). The founder-sensitivity output shows View 1 falls by about $330k if the founder supplies 1,200 hours instead of 400, but View 2 barely moves because the time is valued at a similar rate.

## 6. Capacity constraint

Unbound alone wants 935 hours of commercial and executive work at the reference scale, more than twice the 400-hour base allocation, before any engineering. Echelon-assurance's proposed cap on assurance labour (25% of founder capacity, ~450 h) is exceeded by its own recommended package even at one product. **Capacity, not cash, binds first.**
