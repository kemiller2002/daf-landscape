# 14 - Canonical migration model (B5)

Status: research draft (2026-11-26). Not legal advice. Evidence classes per 01-research-methodology.md.

Scope: a conceptual canonical model for heterogeneous legacy DAF exports, and a mechanism for imported history to coexist with Unbound's append-only, bitemporal financial architecture. Entity-level detail is in `data/canonical-migration-entities.csv`. The proposed interchange fields in `research/migration-runbook-2026.md` ("Data portability schema") are absorbed here. Notation: `(CLASS, confidence)`.

## Summary

- **Four layers with different trust levels.** L0 Source Vault (immutable bytes and hashes) → L1 Source-shaped staging (lossless parse, source IDs) → L2 Canonical Migration Model (CMM, with provenance and knowledge state) → L3 Unbound import commands into a tenant. Nothing skips a layer, and every L2/L3 record points back to an L0 byte range (RECOMMENDATION, High).
- **Unknown is never zero.** Every attribute is `Known(v) | NotProvided | Unknown(reason) | NotApplicable | Withheld(privacy)`. `Known(0.00)` and `NotProvided` are different facts. Missing history is never fabricated, consistent with REQ-X-061 ("unknown legacy details remain Unknown") and the WFM-26 guard `no-fabricated-history`.
- **Recommended ledger approach: an Opening-Balance Epoch plus a Legacy History Partition.** Legacy transactions are imported as **non-posting historical facts** (provenance=legacy) that never feed the GL. At epoch E, one balanced opening journal per (entity, fund, net-asset class) is posted **in the first open Unbound period** against `3090 Opening balance/control` (`unbound:requirements/accounting/CANONICAL-CHART-AND-POSTING-RULES.md`). There are no backdated postings into periods closed on the legacy system (ACC-MDL-010, UNB-ACC-003).
- **This pattern has vendor precedent.** Foundant migrates balances "as of a given date" without transaction history [MIG-001] and imports history with a flag so that it "will not impact the general ledger" [MIG-003] (VENDOR-CLAIM, Medium). Unbound's difference is a **roll-forward proof** that links the two layers: earliest legacy balance + Σ imported history = opening balance. Where history is incomplete, the gap is disclosed as an explicit `HistoryGap` amount rather than hidden.
- **Bitemporal honesty.** Imported facts have an effective time in the past and a recorded time equal to the import time (UNB-DATA-003, UNB-IMM-004). Unbound never claims to have known a legacy fact before it imported it.
- **In-flight items are live objects, not history.** Approved-unpaid grants, outstanding checks, recurring schedules and pending contributions become live Unbound objects at E, with lineage to their legacy IDs and `verification_status=imported_unverified` (RR-REQ-X-061-r1). Duplicate prevention is designed in 17.
- **Platform migration and sponsor-to-sponsor transfer are different and must not be conflated.** CNV-EXP-002 (same sponsor, new platform) imports history into the sponsor's own books. UNB-XIN-EVA-009 (new legal sponsor) leaves history in the source sponsor's books and gives the destination only a non-authoritative reference package. Both are correct for their case. The CMM labels each import with `migration_kind`. Advisor or bank programs hosted on a vendor's own sponsoring charity are `ProgramTransfer`, which follows the sponsor-transfer rules and has no full-history import (13 §2b).
- **The legacy history vault is held by Unbound for the sponsor.** Incumbents may allow as little as 10-15 days of post-termination access [ADVB-002]. The L0 vault plus the History Partition therefore replaces read-only legacy access as the durable home for history. Unbound holds it as processor and the sponsor remains records custodian (CNV-ENT-002) (RECOMMENDATION, High).

## 1. Layers and the provenance envelope

| Layer | Content | Mutability | Requirement anchors |
|---|---|---|---|
| L0 Source Vault | Original files, DB backups, PDFs, **report exports and statement PDFs captured before incumbent access ends**; SHA-256 per file; Merkle root per bundle; chain-of-custody record. The sponsor's durable legacy archive | Write-once, retained per CNV-PLT-004 and legal holds | UNB-CUST-012, UNB-DATA-008, UNB-IMM-007 |
| L1 Staging | One row per source record, all source columns kept (including unmapped), `row_locator` | Rebuildable from L0 (deterministic parser) | UNB-DATA-010 |
| L2 CMM | Canonical entities (CSV), typed values with knowledge state | Rebuildable from L1 + pinned mapping version (see 15) | REQ-X-061, RR-REQ-X-061-r1 |
| L3 Import commands | `ImportHistoricalFact`, `PostOpeningBalance`, `AdoptInFlightItem`, `RegisterCrosswalk` | Append-only domain events inside the tenant | UNB-IMM-001, UNB-XIN-SAS-005 |

**Provenance envelope** (on every L2/L3 record):
`{ migration_run_id, migration_kind: PlatformReplacement|SponsorTransferIn|ProgramTransfer|TenantRelocation, source_system, source_platform_version?, export_id, file_sha256, row_locator, source_record_ids[], mapping_version_hash, transform_version, import_batch_id, verification_status: imported_unverified|verified|rejected, knowledge_class: legacy_asserted|legacy_reconciled|unbound_verified, source_effective_at?, source_recorded_at?, imported_at }`

`knowledge_class` moves forward only. `legacy_asserted` means the legacy system said so. `legacy_reconciled` means the fact ties to an independent source (custodian, bank, as-issued statement). `unbound_verified` means re-verified under Unbound controls, for example payee destination evidence under CNV-PAY-002.

## 2. Value semantics

| State | Meaning | Example | UI rendering |
|---|---|---|---|
| `Known(v)` | Source provides v | fee = 0.00 explicitly | the value |
| `NotProvided` | Source schema lacks the field, or the export omitted it | DonorCentral grants-paid list has no purpose field | "Not provided by previous system" |
| `Unknown(reason)` | Field exists but is empty, contradictory or unparseable | gift completion date blank | "Unknown: <reason>" plus an evidence request |
| `NotApplicable` | Semantically void | tax lot for a cash contribution | hidden |
| `Withheld(privacy)` | Exists, but is not transferred (sponsor transfer-in under UNB-XIN-EVA-009, or anonymity) | donor identity for an anonymous grant | "Withheld" |

Rules: arithmetic over a non-`Known` amount is a type error. Reports aggregate `Known` values only, with counts of excluded items printed next to the totals. CNV-FIN-003 dates (GiftCompletionDate, AcceptanceDate, AvailabilityDate, AcknowledgmentDate) are typically `NotProvided` for older history. Acknowledgment re-issuance is blocked where AcknowledgmentDate is `Known`, which prevents duplicate receipts (runbook M18).

## 3. How imported history coexists with the append-only ledger

### Options considered

| Option | Description | Verdict |
|---|---|---|
| A. Replay history as live GL postings | Post every legacy transaction into Unbound periods dated in the past | **Rejected.** It needs backdated postings into periods closed and audited on the legacy system (ACC-MDL-010). Re-performing legacy fee or unit logic would create differences that look like errors (ASC 250 restatement territory [MIG-017]). It also doubles audit scope. |
| B. Opening balances only | Foundant-style beginning balance [MIG-001] | **Insufficient alone.** It fails CNV-EXP-002 (donor history must not degrade). |
| C. **Epoch + Legacy History Partition** | Non-posting historical facts + opening journals at E + roll-forward proof | **Recommended** |
| D. Shadow book | Unbound ingests legacy/ERP books without posting (UNB-XIN-ACC-010 `Shadow`) | Complementary. Used during parallel run and when the sponsor keeps an external GL (CNV-FIN-012) |

### Option C mechanics

1. **Epoch E** = the first instant of the first Unbound accounting period, normally a month start (see 17 for calendar). Legacy is the book of record for all periods before E. Unbound is the book of record from E onward, per function, under the BookOfRecord map (UNB-XIN-ACC-010).
2. **Legacy History Partition**: one store per tenant holding the `HistoricalContribution`, `HistoricalGrant`, `HistoricalFee`, `HistoricalInvestmentActivity`, `HistoricalJournal`, `HistoricalStatement` and `HistoricalUnitTransaction` facts. These are append-only, carry provenance=legacy, are **excluded from posting rules** (ACC-MDL-006 lets an event map to zero journals), and are visible in donor history, statements, Schedule D/990 support and acknowledgment deduplication.
3. **Opening journals** are posted once (WFM-26-T09 guard `opening-balances-posted-once`; idempotency key = `migration_run_id + entity + fund + class`). Their effective date is E and their posting period is the first open period. The legacy TB at E-1 is loaded as balanced lines, and `3090` must **net to zero** after the full TB loads. If it does not, the run is blocked and there is no plug (see 16).
4. **Roll-forward proof** per fund: `Opening(E) = B(earliest) + Σ Historical(earliest..E-1)`. If equality fails, or the earliest balance is unknown, the fund gets `HistoryGap{from, to, amount_unexplained}`. That is a disclosed attribute shown to staff and, with plain wording, to donors. It is not a ledger entry.
5. **Corrections after import**:
   - A wrong historical fact gets an appended `HistoricalCorrection`, linked to the original (UNB-IMM-002), with no GL effect.
   - A wrong opening balance gets a current-period correcting journal with `relates_to_period=E` and a correction class (CNV-FIN-011). If the error is material to statements already issued, the CFO decides on restatement (CNV-FIN-011, ASC 250 [MIG-017]).
   - A mapping defect found after archive uses the WFM-26 `MigrationCorrection` state.
6. **Grant recognition point (CNV-FIN-007; ADVB-08).**
   - The legacy convention is captured at T0 (13). Examples: recognize at approval, at communication, or at payment.
   - Each `HistoricalGrant` carries `legacy_recognition_point`.
   - The opening grants-payable balance at E is the legacy book's balance under the legacy convention. It is never recomputed silently.
   - The sponsor book's `GrantRecognitionPoint` is effective-dated. By default it continues the legacy convention to the next fiscal year-end, unless the external auditor concurs earlier with a written policy change. That auditor acceptance is the CNV-FIN-007 activation gate.
   - At E-1 the CNV-FIN-007 cutoff register is built from legacy data: approved-uncommunicated, communicated-unpaid and conditional grants. Each grant's communication evidence is `Known` or `NotProvided`.
   - Where the convention changes at a fiscal year-end, the difference in grants payable is computed per grant and posted as a policy-change entry under ASC 250 treatment [MIG-017], approved by the CFO. It is never posted as a migration correction.
7. **Statements**: legacy as-issued statements are stored as L0 evidence (hash, issue date) and are **never regenerated** to replace them. Unbound can produce an "as-recomputed" view from history for comparison (gate in 16), and it is labelled as such (UNB-NAV-010, UNB-ACC-025).

### Bitemporal coordinates

| Time | Source | Use |
|---|---|---|
| `effective_at` | Legacy transaction date (or `Unknown`) | Donor history, period attribution, retention clock |
| `source_recorded_at` | Legacy entry timestamp, if exported | Forensics ("when did the old system learn this") |
| `recorded_at` | Unbound append time (= import) | As-known queries; Unbound never "knew" earlier |
| `epoch` | E | Book-of-record boundary |

The retention clock runs from **source transaction date**, not import date, so a 2017 grant imported in 2027 keeps its CNV-PLT-004 10-year floor running from 2017 (RECOMMENDATION; avoids over-retention and under-retention). Records must also keep supporting what was reported on the sponsor's annual returns [MIG-024].

## 4. Entity-specific design notes

(The full list is in `data/canonical-migration-entities.csv`.)

- **Parties, households and roles.** Legacy "households" are relationship groupings, not owners. They map to party relationships (UNB-PART-001..004). Role vocabularies differ between platforms: AEF publishes that its role names differ from Ren's (Grant Advisor / Donor / Money Manager) [MIG-014] (VERIFIED-FACT, High). Role mapping is therefore a sponsor-approved table, and advisory authority derives from **signed agreements, not from the export** (WFM-26-T02 guard `roles-derived-from-signed-agreements`). Imported authorities are `imported_unverified`. View access is granted at go-live. Changes to authority, successor or contact follow CNV-PLT-011 holds, and credentials are re-enrolled under CNV-PLT-003. Password hashes are never migrated (RECOMMENDATION).
- **Successors.** Plans import as versioned succession plans (UNB-SUCC-001). An activated succession imports as history plus current successor relationships. Contested or unknown states stay `Unknown` and route to a case (UNB-SUCC-007).
- **DAF accounts.** The legacy fund ID is kept as an alias (REQ-X-025: preserve leading zeros, legacy aliases), and Unbound fund IDs are never reused legacy keys. Status is mapped to canonical lifecycle states, and a closed fund is imported if it has history (as Foundant also recommends for retired funds [MIG-001]).
- **Restrictions and variance power.** Free text maps to structured restriction records through the A4-approved mapping. Fund agreement evidence feeds RR-UNB-ACC-033-r1. Where evidence is missing, the fund's opening net-asset class posts to suspense classification with an exception that must close before the first period close.
- **Holdings, lots, units.** Custodian positions are the reconciling source (UNB-CUST-023, UNB-INV-008). Tax lots are imported where the custodian provides them, otherwise `NotProvided`. Unit balances are imported at **source precision** (no rescaling). Conversion is allowed only under UNB-NAV-031 (see 16).
- **Charities.** Imported records match the first-party registry by EIN. Legacy status labels are kept as `legacy_asserted` evidence only (UNB-CHAR-041). Bank details are `imported_unverified` until CNV-PAY-002 evidence exists or the charity is enrolled with a supported networked rail (CNV-EXP-002).
- **Recurring grants.** These are live schedule versions. AEF carried recurring recommendations over and warned of delays for a two-week window [MIG-013] (VERIFIED-FACT, High). Unbound should carry them over as `imported_unverified` schedules that release only after the payee is verified and the donor has been notified (RECOMMENDATION).
- **Audit records and delegated-authority logs.** These are imported as historical facts with their original actor strings. They are not linked to Unbound principals unless a verified identity match exists.
- **Documents.** Imported as L0 objects with hash, as-issued date and retention class. Foundant treats document migration as a separate workstream [MIG-006] (VENDOR-CLAIM, Low).

## 5. Crosswalk

`Crosswalk(tenant, entity_type, unbound_id, source_system, source_id, source_id_scope, valid_from, valid_to, relation: same|split_from|merged_into|replaces)` is many-to-many and append-only. It covers grant IDs, payment attempt IDs, check numbers, ACH trace numbers, rail-partner references, custodian account numbers, fund IDs and party IDs. It is the basis for cross-system idempotency in 17 and for the M10 case ("single canonical grant per recommendation, old/new IDs cross-referenced") in `research/migration-runbook-2026.md`.

## Implications for Unbound

- Option C turns CNV-EXP-002 into an engineering contract: the full history the predecessor holds is visible, reconciled to the opening balance, and kept out of the GL. That is a stronger donor-continuity promise than the public AEF/Ren outcome (33 months imported, 2 years visible) [MIG-012], and stronger than balances-only conversions [MIG-001]. (INFERENCE, Medium)
- It needs one new persistence concept, the non-posting historical-fact partition. Everything else reuses existing requirements.

Candidate requirements:
- **UNB-MIG-010** Five-state value semantics (Known/NotProvided/Unknown/NotApplicable/Withheld), with arithmetic on non-Known values rejected (refines REQ-X-061).
- **UNB-MIG-011** Legacy History Partition: imported history as non-posting, append-only historical facts with provenance=legacy, excluded from posting rules and included in donor history and acknowledgment deduplication (refines CNV-EXP-002, ACC-MDL-006).
- **UNB-MIG-012** Opening-Balance Epoch: opening journals at E in the first open period, posted once, `3090` nets to zero; no backdated posting before E (refines UNB-RCN-WF-009, ACC-MDL-010, WFM-26-T09).
- **UNB-MIG-013** Per-fund roll-forward proof with a disclosed `HistoryGap`; no plug (refines CNV-EXP-002 "reconciliation report").
- **UNB-MIG-014** Migration retention clocks start from the source transaction date (refines CNV-PLT-004).
- **UNB-MIG-015** A many-to-many, append-only crosswalk covering grant, payment, check, trace, rail and custody references (refines RR-REQ-X-061-r1, REQ-X-025).
- **UNB-MIG-016** Recognition-point continuity at the epoch: legacy convention carried until auditor-accepted change; cutoff register built at E-1; policy-change difference computed per grant (refines CNV-FIN-007, UNB-XIN-ACC-002).
- **UNB-MIG-017** The L0 vault and History Partition are the sponsor's durable legacy archive. All history and as-issued documents are captured before incumbent access ends, without relying on post-termination incumbent access (refines CNV-ENT-002, REQ-X-061).
- **Clarification**: amend CNV-EXP-002 so that "full fund history" reads "full history available from any source the sponsor can lawfully obtain (predecessor platform, prior predecessors, custodian, sponsor archives), with shortfalls disclosed per fund as HistoryGap together with the source's retention evidence". State that it applies to `PlatformReplacement`, while UNB-XIN-EVA-009 / CNV-ENT-002 govern `SponsorTransferIn` and `ProgramTransfer`. Older national sponsors may have decades of history, so the history-depth volume is a sizing driver for draft 20 (ADVB-07).

## Open questions / evidence gaps

- Does the sponsor's auditor accept non-posting history plus an opening-balance epoch, or require legacy GL detail inside the new system for the comparative year? This is an AU-C 510 practice question [MIG-016], and auditor interviews are needed.
- Field-level completeness of real Ren, FIMS and DonorCentral exports is unknown (L06, L15). The CMM is a hypothesis until rehearsed on authorized data.
- Whether donors should see `HistoryGap` amounts or only a "history before <date> not available" notice is a UX and legal-wording decision.

## Adversarial review response

| ID | Response |
|---|---|
| ADVB-02 | **Accepted.** Unbound's L0 vault replaces read-only incumbent access as the durable history store (UNB-MIG-017). |
| ADVB-04 | **Accepted.** Added `ProgramTransfer` as a migration_kind; it gets no full-history import. |
| ADVB-07 | **Accepted.** CNV-EXP-002 clarification extended to "any source the sponsor can lawfully obtain" plus retention evidence. Volume sizing is draft 20's. |
| ADVB-08 | **Accepted.** Added a recognition-point epoch design (mechanics item 6; UNB-MIG-016). I keep the position that a standardised epoch remains practical. |

