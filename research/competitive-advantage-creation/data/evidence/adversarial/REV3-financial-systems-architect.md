# REV3 - Financial systems architect review

Status: adversarial review, round 1 (2026-11-26). Reviewer panel REV3, perspective 1 of 5. Independent of the authoring agents; same model family, so not independent validation. Challenges are registered as P3-CHL-REV3001..REV3009 in `data/fragments/REV3/adversarial-challenges.csv`. "Fact" marks a checkable error; "Judgment" marks a disputed estimate.

## Position

I have built and run ledgers, reconciliation and conversion tooling for regulated money. The Phase III package is more candid than most about architecture: report 07 calls most candidates ordinary and says nothing is built (07:9-21, 07:38). The economic reports then quietly use the opposite premise. They assume an Unbound that is "functionally complete" (S3), that costs $40-250k to harden, and that one founder plus contracted reviewers can maintain it for $120k a year. That premise carries the headline (A3 ranked first, 14:40; key figures, 16:18-24), and nothing in the repository supports it.

## Challenges

**1. S3 is a hypothetical state that carries the conclusion (high; judgment plus circularity).** The package says today's state is S2: "no production code for the ledger, payments or the portals" (02:38). Report 07:23-36 says the only implemented product code is the first Echelon.Execution slice (25 unit and 10 PostgreSQL tests) and the CNV-ARC-001 benchmark has not been run (07:29, 07:34). A3 starts from S3 and excludes the remaining build, so it is the only sequence that both pays back and passes the kill rule (14:40, 14:264). S3 has no acceptance definition: no scope list, no test set, no reconciliation proof. That lets anyone declare it reached. The ranking measures how much cost the start state leaves out, not commercial merit. **Proposed change:** define S3 by testable exit criteria (MSP scope list, CNV-ARC-001 benchmark passed, tenant-isolation negative tests, a ledger replay proof, a migration rehearsal on synthetic data) and report A3 only as conditional on those criteria.

**2. Remaining build cash of $0.25-1.2M (base $0.6M) from S2 is not credible for this scope (high; judgment).** The base assumes a founder with agents and contracted approvers builds the ledger, payments role table, grant lifecycle, eligibility gates, portals, canonical import and rehearsal cell in 12-24 months (capital-states.csv S2 dev; P3-ASM-AB002; sequence-values TPL-UNB-S2 dev_cash). The scope includes CNV-PLT-010 (two approvers, external daily digest anchoring, break-glass DBA; `unbound/requirements/PLATFORM-UX-API-AND-ASSURANCE-STANDARDS.md:312`), bitemporal append-only accounting, schema-per-tenant RLS with negative tests, and an owner-mandated rehearsal (UNB-TRN, `requirements/discovery/2026-11-26-transitus-integration/02-REQUIREMENTS.md:208`). PR #87's market valuation is $1.35-2.43M MSP, plus $3.6M+ for full scope (03:18). The cash figure rests on an untested agent-productivity multiple. Report 04:20 calls the M-07 engineering spike that would measure it "moot once Unbound is built", which assumes the answer. **Proposed change:** keep M-07, or ledger actual build hours now (P3-GAP-AB002), before quoting any S2-to-S3 cash. Until then, treat S2 cash as unknown with a $1.35M+ economic floor.

**3. Hardening at 15-30% of MSP ($40-250k cash) understates production readiness for a financial system of record (high; judgment).** P3-ASM-AB003 covers security review, a DR test, observability, accessibility and pen-test remediation. It leaves out work that usually dominates hardening for ledgers:
- performance and soak tests against the CNV-ARC-001 benchmark;
- year-end volume (December peak) load;
- idempotency and replay under failure injection;
- schema-migration rehearsal across every tenant schema;
- backup restore to a point in time with ledger digest re-verification;
- operating control evidence producers, since echelon-assurance has "no control above Designed" (09:33).

In my experience readiness for regulated money movement costs a third or more of the build, not a sixth. **Proposed change:** itemize hardening against named CNV/UNB controls and widen the range to at least 30-60% of MSP economic cost.

**4. $120k a year of maintenance cannot fund CNV-PLT-010's two-person controls (high; unfunded obligation).** CNV-PLT-010 requires two approvers on every control-relevant change, neither the author, plus two-person break-glass production access. With a single founder as author, that means at least two other qualified people available for every release and incident, all year. P3-ASM-AB010 ($40-250k, base $120k) includes agent compute ($24k base, P3-ASM-AB011) and only a "partial" second maintainer. Report 02:104 concedes the second maintainer "stays", but the line does not cost two independent approvers plus on-call cover. SOC 2 segregation-of-duties testing will also fail with a one-person operations team. **Proposed change:** cost at least 2 × 0.3-0.5 FTE of contracted senior reviewers with on-call ($150-350k a year) and run A3 on that base.

**5. "Component monolith" and "minimal deployment" are presented as a cost advantage that survives product parity (medium; unsupported advantage).** EK014 and EK015 are rated "Medium" resilience (13:44-45). Report 16:11 claims "the lean structure survives price responses that would sink the Phase II cost base". The lean base, however, is mostly organizational: the founder at $0-60k cash and no staff (02:83-85; walk-away price $21.51 includes only a $60k founder draw, 16:235). Topology contributes infrastructure of $45k a year (02:74). An incumbent's per-account infrastructure is already $15-45 (07:98). The "survives price war" result is founder subsidy relabelled as architecture. **Proposed change:** split the walk-away price into an infrastructure component and an organizational component, and report both with the founder at market cash.

**6. Append-only plus bitemporal history is costed as free storage, but it carries ongoing engineering and legal cost (medium; omission).**
- Corrections-as-events, projection rebuilds, external digest anchoring (CNV-PLT-010) and multi-year retention mean projection-rebuild time grows with history.
- Every schema change needs an upcaster or a migration of historical events.
- Erasure requests (state privacy statutes that reach nonprofits; Unbound's own file-ingestion package discusses erasure) require crypto-shredding or tombstoning designs in an append-only store.

None of this appears in maintenance or infrastructure (02:70-74). **Proposed change:** add an event-store lifecycle line (projection rebuild, upcasting, retention and erasure) to maintenance, and a P3-GAP for its size.

**7. Schema-per-tenant on a pilot schema tool is a scaling liability, not a neutral choice (medium; judgment).** CNV-ARC-001 gives each sponsor a schema and role with RLS (07:29). Strata, the schema tool Unbound relies on, is a v0.1.1 pilot that supports only PG16 (09:17). A3's base reaches about 18 sponsors (14:73), and each hosted programme in Sequence E may need segregation (06:67). Every release must then migrate N schemas atomically, with negative isolation tests per tenant, which multiplies release time and failure modes. Infrastructure $20-110k (P3-ASM-AB014) assumes one cluster. **Proposed change:** add per-tenant release cost and a Strata maturity gate (multi-major PG support, multi-schema migration rehearsal) as preconditions for S4.

**8. Reconciliation "eliminations" ignore that external breaks are the expensive part (medium; double counting risk).** E13 reconciliation keeps 2.7 residual minutes per account-year (10:59). Sponsor-level close falls from 28,800 to 9,000 minutes (10:70), credited to a single ledger and continuous reconciliation. Report 10:175 itself notes that E13 prevention is applied on a p_native already rebased once. A single internal ledger does not reduce custodian, bank and rail breaks, which are the ones that take controller time; they increase in a multi-rail design (CNV-PAY-001 networked rail plus ACH plus check fallback). **Proposed change:** model close effort per external counterparty feed, not per account, and remove the second prevention credit on E13 (P3-VAL-HI007).

**9. Inconsistent cost bases make the kill signals unusable (medium; internal inconsistency).**
- Report 13 sets kill signals on the Phase II MD-6 base: "net price below ~$73" and break-even about 36-43k accounts (13:7, 13:114).
- Report 02:87 says the lean base breaks even at about 13k accounts.
- Report 16 says 8.5k accounts and a walk-away price of $21.51 (16:193-194, 16:235).

The package therefore carries three different viability thresholds for the same channel-licensing business, and the kill signal in 13 has not been recomputed. **Proposed change:** one walk-away table, with the founder at market and the costed maintainer team of challenge 4, used in 13, 16 and 19.

## Factual points checked

- CNV-PAY-001 makes Unbound a Nacha TPSP by contract and requires it to accept the fraud-monitoring obligations (`unbound/requirements/DEFERRED-PAYMENTS-AND-REMAINING-GAPS.md:129`). The architect consequence is a monitoring capability Unbound must build and operate; the cost is taken up in the compliance review (REV3 compliance, challenge 1).
- Nacha's Phase 2 fraud-monitoring effective date is 19 June 2026, with 22 June as the practical date because 19 June is a federal holiday (https://www.nacha.org/rules/risk-management-topics-fraud-monitoring-phase-2, accessed 2026-11-26). Unbound's "22 June 2026" is therefore acceptable.

## Verdict

The structural cost work (sequential savings, entity separation, no summing across models) is sound and better than Phase II. The build, hardening and maintenance lines are not. Everything ranked "first" depends on an undefined S3 and on a maintenance budget that cannot staff the two-person controls Unbound's own requirements mandate.
