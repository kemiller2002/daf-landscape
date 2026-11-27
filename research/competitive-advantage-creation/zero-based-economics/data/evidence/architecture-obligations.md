# Architecture and operating obligations extracted from Unbound, Echelon Foundry and prior models

Read-only extraction, 2026-11-27. Prefixes: `U/` = kemiller2002/unbound, `EF/` = kemiller2002/echelon-foundry, `DL/` = this repository. Line numbers are at the Stage I heads (`unbound` edbcd0d, `echelon-foundry` c0ed458). Source register entries: SRC-ZB-001 (Unbound), SRC-ZB-002 (Echelon Foundry), SRC-ZB-003 (prior DL models).

**Headline:** almost every operational number in Unbound is a proposal, candidate or policy default. Nothing is benchmarked in production, deployed or audited (U/execution/README.md:7-8; U/requirements/governance/MASTER-CONTROL-MATRIX-GOVERNANCE.md:33). Echelon Foundry has **no** hosting, security, SOC or penetration-test standard. Its two draft standards are ENG-6BEA (reproducible F# research models) and MTH-48F0 (event-level costing: minutes = frequency × P(touch) × minutes per touch; every parameter ranged and sourced).

## 1. Stack
| Item | Obligation | Citation |
|---|---|---|
| Database | Modular monolith on **one managed PostgreSQL cluster**; schema and role per sponsor tenant, row-level security; dedicated DB only on risk or contract | U/requirements/PLATFORM-UX-API-AND-ASSURANCE-STANDARDS.md:257 (CNV-ARC-001) |
| Ledger | Append-only ledger on managed PostgreSQL; daily external digest anchoring | same :305 (CNV-ARC-004), :312 (CNV-PLT-010) |
| Broker/cache | None in release 1. A slice benchmarked at 2,100-3,900 tx/s, against about 200 needed | U/requirements/discovery/2026-11-25-availability-architecture/04:98-105, README:19 |
| Replicas | Batch, reporting and AI read from replicas or snapshots | CNV-ARC-001 |
| Region | RPO 0 in-region (synchronous standby); cross-region recovery declares a nonzero RPO; no active-active | CNV-ARC-001:257 |
| Cloud provider | **Not chosen** (FIL-OD-01, FIL-OD-02 open). Prior budget priced Azure: cloud line ~$35k/yr | U/…/2026-11-26-file-ingestion/14:19-20; DL/research/commercial-opportunity/servicing-economics/03-organization-and-budget.md:283-320 |

## 2. Availability and recovery
- **SLOs:** none ratified. Numeric SLA commitments come only after benchmark and pilot evidence; the candidate is 99.5-99.9% (CNV-ARC-001; U/requirements/OPEN-QUESTIONS.md:210).
- **RPO/RTO candidates by data class** (RR-UNB-RES-003-r1):
  - C0 ledger, holds and approvals: RPO 0, RTO ≤4 h.
  - C1 documents: RPO 0, RTO ≤24 h.
  - C2 cases: RPO ≤15 min, RTO ≤24 h.
  - C3 projections: rebuild.
  - C4 telemetry: best effort.
- **Restore tests:** at least annually per class, and per tenant with key-rotation evidence (CNV-ARC-005:343). The work inventory says semi-annual DR drills (SPW-137) — **contradiction**.
- **Immutability:** immutable backup (UNB-GAP-034) and immutable audit records in protected storage (SOC2-006). No numeric backup retention is stated.
- **Degraded operation:**
  - DB down: refuse new work with a retryable response and keep an independent status page (UNB-AVL-011).
  - Holds and revocation are never queued (UNB-AVL-006).
  - AI outage must not stop deterministic paths (CNV-AIO-001).
- **December:** surge of about 3×; December is 19.5% of grants; load test before each December (UNB-AVL-013).

## 3. Controls requiring distinct humans (drive the coverage register)
| Control | People | Citation |
|---|---|---|
| Changes to control-relevant modules (gate, ledger, reservations, holds, authority, dispatch) | **2 approvers, neither the author** | CNV-PLT-010, PLATFORM:312 |
| Production DB admin | Break-glass only, two-person activation | same |
| Operator emergency access (hold publication, revocation, read) | Two-person break-glass; sponsor notified | CNV-PLT-007 |
| Degraded mode / kill switch | Two persons | TVR-OPS-002; roles.jsonl:2 |
| Platform operator / incident commander | **On-call two-deep** | roles.jsonl:14 (ORG-R14) |
| Payment release | 3 distinct persons until the deterministic gate is auditor- and board-accepted, then 2. **Sponsor side.** | CNV-GOV-003; OPEN-QUESTIONS:112 |
| Treasury authority | ≥2 distinct holders. **Sponsor side.** | roles.jsonl:4 |
| Unobtainable payment outcome (30 days) | Two independent approvers | CNV-PAY-004 |
| Vendor staff authority | **May not hold A3+ authority**; a reserved-authority holder serves one sponsor | CNV-GOV-004:110 |
| Release 1 | Runs with **no Unbound staff in sponsor workflows** | UNB-CDD-CMF-002 |

## 4. Assurance
- **SOC 1 (AT-C 320) and SOC 2 evidence engineering from inception.** SOC 1 Type 2 applies when a user auditor relies on Unbound's controls.
- **For the staffed administration offer (OD-M-08), SOC 1 Type 2 readiness and the first observation period start before the first staffed client goes live.** Each party bears its own auditor costs (CNV-GOV-001).
- Pen testing is a recorded program, but no cadence is set (SOC2-016).
- Vendor assurance review is annual (CNV-GOV-002).
- **Retention:**
  - Transaction records: 10 years (31 CFR 501.601). Other financial records: 7 years.
  - Service-organization evidence: SOC period + 3 years (CNV-PLT-004, CNV-PLT-009).

## 5. Human work (work inventory, U/requirements/discovery/2026-11-24-simplification-economics)
- **143 activities:** 57 deterministic, 63 mixed, 19 human, 4 AI-assisted. At 100k accounts the minimum-touch design needs 55,220 h, against 379,240 h conventional.
- **Exception roles** are about 82% of minimum-touch workload. Exception grant decisions are 0.9 min per grant at minimum touch, against 3.6 conventional.
- **Decisions are reserved to the sponsor.** The sponsor board adopts the deterministic grant policy, and AI is prohibited from every decision (CNV-GRT-001; 10-ORGANIZATIONAL-AND-STAFFING-MODELS.md:77).
- **Event touch rates** (DL/research/competitive-displacement/data/model-inputs/events.csv), native design:
  - Vetting: 0.0234 × 15 min.
  - Grant approval: 0.09 × 25.2 min.
  - Payment processing: 0.06 × 8.2 min.
  - Reconciliation: 0.02 × 10 min.
  - Human contacts: 0.5/account-yr × 0.8 × 10 min.
  - Sponsor-reserved time: 2.7/4.85/7.0 min per account-year in every mode.
- **Internal time study:** 10.9% of grants routed to a person (16-SYNTHETIC…:40-48).

## 6. Charity data
- **IRS EO BMF, Pub 78, auto-revocation, 990-N, 990 e-file indexes and OFAC: all free/public domain**, about 1 GB per month (UNB-CNET-003).
- **Freshness:**
  - BMF/Pub 78/revocation: 45 days. 990-N: 14 days. OFAC: 24 h, polled every 6 h.
  - Deep review defaults to 180 days, kept as a ceiling under change-driven re-vetting (CNV-GRT-003; UNB-CDD-CIV-007/008).
  - Only 405 of 236,750 monthly BMF changes were eligibility-relevant (charity-network 02:139).
- **Optional licensed data:** Candid Charity Check $2,750-9,900; commercial sanctions screening $3k-25k (servicing-economics 03:298-300).

## 7. Money
- **Unbound never receives or holds money and cannot execute a payment.** The sponsor is the Originator; Unbound is a TPSP by contract. Investments sit with the sponsor's RIA or custodian (CNV-LEG-001, CNV-PAY-001).
- **EF may not be sponsor, Originator or operator** (UNB-CDD-CMF-005).
- **Rail fees are sponsor pass-through**, about $14.92 per account-year (DL competitive-displacement 09:60).

## 8. Support and incidents
- **No contractual SLAs** until benchmark and pilot.
- **Complaints:** acknowledge within 2 business days, respond within 15 (CNV-PLT-005).
- **Unmatched bank debit:** high-severity incident within 1 h.
- **Exit package** within 30 days.
- **Not stated:** breach-notification timeline and support hours.

## 9. Volume parameters (contradictions)
- **Grants per account-year:** 8 (work inventory), 9 (events.csv; observed 5.6-18.5), 10 (servicing-economics), 7.1 (synthetic year).
- **Contributions per account-year:** 2-2.5 (1-8).
- **Exception rate:** 8% (2.8-17%) in policy defaults; 10.9% measured in the synthetic year.
- **Assets per account:** $250k base (parameters.csv), industry mean ~$141k (report 15:65), "typical" segment $60k.
- **Infrastructure per account:** $25 per account-year (PAR-011, ~$250k at 10k accounts) vs ~$35k/yr total cloud in servicing-economics — **a 7× contradiction** that this package resolves bottom-up.

## Gaps
- No numeric SLOs.
- No backup retention period.
- No access-review cadence.
- No pen-test cadence.
- No log retention period.
- No breach-notification timeline.
- No cloud provider.
- No active-passive statement.
