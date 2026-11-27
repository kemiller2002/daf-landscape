# 07 — Minimum viable organisation

Built from responsibilities, authority, independence, expertise, workload, availability and continuity — not from departments. Inputs: [`operational-activities.csv`](data/registers/operational-activities.csv), [`control-obligations.csv`](data/registers/control-obligations.csv), [`roles.csv`](data/model-inputs/roles.csv), [`configurations.csv`](data/model-inputs/configurations.csv). Outputs: [`headline-staffing.csv`](data/model-outputs/headline-staffing.csv), [`simulation-reference.csv`](data/model-outputs/simulation-reference.csv). All figures are model results after two adversarial correction rounds; nothing is measured.

## 1. Responsibility pools and combination rules

| Pool | Roles combined | May not be combined with | Why |
|---|---|---|---|
| OPS | operations, support, implementation | AUTH, FINANCE (on the same transaction) | prepares payments and handles exceptions |
| FINANCE | accounting and reconciliation | OPS release rights | reconciler must hold no payment rights (functional independence) |
| CONTROL | controller (close and sign-off) | AUTH | separated after review (ADV-OA-010): the person who releases payments must not sign off the reconciliation |
| AUTH | independent authorizer (payment release, manual journals, bank-detail changes) | OPS, FINANCE, CONTROL | second-person release |
| COMPLIANCE | compliance owner, sanctions officer, Nacha TPSP owner, policy | testing of its own controls (external) | OFAC guidance allows one person across compliance-owner roles |
| ENG | engineering, security/on-call owner | — | author + two non-author approvers (CNV-PLT-010) |
| COMM | executive, sales, account management, contracts | — | founder covers first |
| EXT | counsel, auditors | — | never employed |

One person may hold several compliance-owner roles; no one may hold two incompatible duties on the same transaction (prepare/release; release/reconcile; author/approve).

## 2. Operating configurations (each produced by the model)

| Config | Vendor does | Sponsor keeps | Annual cash cost (View 1) at $100M / $500M / $1B (PG-HNW, $250k) | Dedicated FTE at $500M | Activation condition |
|---|---|---|---|---:|---|
| CFG-1 Technology licensing only | platform, engineering, assurance, tier-2 support | all administration | $1.40M / $1.40M / $1.46M | 4 | sponsor has staffed operations |
| CFG-2 Licensing with support | + support desk | all administration and decisions | $1.40M / $1.44M / $1.62M | 4 | sponsor wants vendor support but keeps operations |
| CFG-3 Exception administration | + operational exceptions; prepares reserved cases (30%) | judgment, authorization | $1.50M / $1.78M / $2.02M | 6 | sponsor lacks exception capacity |
| CFG-4 Hybrid administration | + delegated judgment, 50% of delegable sponsor work | independent authorization | $1.54M / $1.93M / $2.27M | 7 | sponsor supplies releaser and sign-off |
| CFG-5 Full administration (existing sponsor) | + independent authorization (80%), close preparation and audit support (80%), reserved-case preparation (50%) | reserved legal decisions, board delegations, sign-offs | $1.83M / $2.22M / $2.86M | 8 | sponsor outsources administration |
| CFG-6 Through a channel partner | platform; 30% of commercial; 20% of support | partner sells and supports; 30% revenue share | $1.37M / $1.37M / $1.40M (before 30% revenue share) | 4 | distributor exists |
| CFG-7 Standalone DAF administrator | as CFG-5, replacing every shared capability | as CFG-5 | ≈ CFG-5 cash; standalone view +$1.0M | 8 | Unbound spun out |

CFG-7 is an administrator, **not a sponsoring organisation**. Becoming a sponsor (holding exclusive legal control, filing Schedule D, bearing 4966 taxes) is a different business that this research does not model.

## 3. The reference organisation (full administration, $500M, 1 sponsor, 2,000 accounts)

| Pool | Hours/yr | Arrangement | Named persons | Cash cost |
|---|---:|---|---:|---:|
| ENG | 4,131 | 4 dedicated engineers | 4 | $920k |
| COMPLIANCE | 1,719 | 2 dedicated | 2 | $244k |
| OPS | 1,414 | 2 dedicated + 36 h December surge | 2 | $224k |
| COMM | 935 | founder 400 h + 535 h fractional | 2 | $94k |
| CONTROL | 315 | fractional controller | 2 | $78k |
| FINANCE | 509 | fractional accountant | 2 | $53k |
| AUTH | 38 (+ floor) | fractional independent authorizer | 2 | $12k |
| EXT | 6 | counsel/auditor hours | 1 | $2k |

Plus fixed lines (insurance, SOC 1/SOC 2, pen test, Nacha audit, counsel, MDR, on-call, escrow, key-person continuity, bookkeeping, observability) and resource-based infrastructure. **About 8 employees plus fractional and retained people; 17 named persons in all** (simulation-reference.csv). Simulated SLA breaches stay within the 1% tolerance in every pool.

## 4. Minimum independent control coverage

Segregated pools (OPS initiation, AUTH release, FINANCE reconciliation, CONTROL sign-off) each need **two named, trained persons** (primary and backup); engineering needs **three** for author-plus-two approval; compliance needs **two** (sanctions dispositions within 10 business days need a backup). Many of these seats can be sponsor personnel, fractional professionals or external firms ([06](06-human-control-obligations.md) §3). In CFG-1/2 the vendor holds only engineering, compliance (its own programme) and commercial seats; in CFG-5 it holds every delegable seat.

## 5. Escalation, absence and incident coverage

- **Escalation:** OPS → COMPLIANCE (eligibility, sanctions) or CONTROL (financial) → sponsor reserved authority (Tier-2 grants, delegations) → counsel.
- **Absence:** every critical pool has a retained, access-provisioned backup (80 h/yr readiness retainer each). The simulation applies 25 absence days per person; discrete one-person absences are not simulated (limitation).
- **Incidents:** on-call rotation across the engineering team (FC-017), managed detection (FC-016), incident-response retainer (FC-013), breach counsel; operational recovery and automation mass-remediation events seeded in the simulation.

## 6. Outsourcing dependencies

Custodian and external investment manager (valuation, OD-M-07); bank/ODFI and payment partners (Chariot, PayPal adapters, OD-P-PAY); identity and bank-account verification APIs; cloud provider; SOC auditor; external Nacha auditor; counsel; MDR provider; fractional controller, accountant and authorizer. Each is a single point of failure until a second provider is contracted.

## 7. Failure modes

| Failure | Consequence | Mitigation in the design |
|---|---|---|
| Founder unavailable | commercial and leadership gap; no Unbound board | FC-022 key-person continuity; documented delegations |
| Sponsor cannot staff release/sign-off seats | vendor must add two independent people plus a fractional controller | CFG-5 pricing includes AUTH/CONTROL pools |
| December peak plus short SLAs | compliance and operations queues breach | surge contractors (OPS/FINANCE only); compliance staffed to peak; SLA redesign ([21](21-requirement-economic-impact.md)) |
| Automation defect affecting many records | mass remediation | seeded remediation events; independent sampling; kill switch |
| Shared Echelon components immature | Unbound pays to build or replace them | transfer-not-elimination ([08](08-shared-echelon-resource-economics.md)) |
| Fractional professional unavailable at peak | SLA breach in control pools | named backups; engagement floors |

## 8. What the organisation is not

It is not "zero humans", and it is not the original three-executive salaried structure. It is a **workload-sized engineering team plus a small compliance function, with fractional control seats** — most of whose recurring cost is set by platform engineering and assurance, not by account volume, until about 5,000 accounts.
