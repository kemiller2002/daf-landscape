# 17 - Cutover strategy, irreversibility and recovery (B8)

Status: research draft (2026-11-26). Not legal advice. Evidence classes per 01-research-methodology.md.

Scope: choosing a cutover strategy for DAF administration; separating reversible technical deployment from irreversible financial execution; preventing duplicate grants, contributions, payments and entries across the legacy-to-Unbound boundary. The comparison table is in `data/cutover-strategy-comparison.csv` (S01-S10). This refines WFM-26-T08..T15, UNB-TEN-013 (never two authoritative writers), UNB-XIN-OTH-002 (TransitionWindow) and the resolved decision XID-OTH-001 ("30-day notice; max 3 business days freeze; no Dec 15-Jan 5", `unbound:requirements/open-questions.csv`). Notation: `(CLASS, confidence)`.

## Summary

- **Recommended default for the entry segment** (CNV-ECO-004, roughly 5,000-50,000 funds):
  - a **per-sponsor single-writer switch** with ≥1 full monthly close of shadow parallel run;
  - a **controlled freeze of ≤3 business days**, announced ≥30 days ahead;
  - legacy kept **read-only** for ≥90 days.
  - Fund-cohort ("account-by-account") cutover inside one sponsor is **rejected**. Shared bank accounts, positive-pay files, pools and GL control accounts would have two writers (UNB-TEN-013) (RECOMMENDATION, High).
- **Account-by-account is right for sponsor-to-sponsor moves and partner exits.** Those run fund by fund as separate sponsor-authorized grants (CNV-ENT-002, UNB-XIN-EVA-009, UNB-XIN-SAS-007). They are a different process from platform migration.
- **Calendar.** No freeze Dec 15-Jan 5 (XID-OTH-001). Avoid Q4 generally: December is the contribution and grant peak (CNV-FIN-001), and sponsors publish asset-specific contribution cutoffs from Nov 10 to Dec 31 [MIG-023]. Avoid January statement and acknowledgment season, and the month before fiscal year-end close. **Preferred epoch: a month start between March and September** for calendar-year sponsors, after the prior month has closed in legacy (RECOMMENDATION, Medium). Practitioners have both gone live at fiscal-year start with one month of parallel running and gone live mid-year with no dual entry [MIG-007] (VENDOR-CLAIM, Medium). One vendor case study instead ran its parallel period across fiscal year-end as an audit safety net [MIG-026] (VENDOR-CLAIM, Low). That trade-off is possible, but it collides with the December peak for calendar-year DAF sponsors.
- **The rollback boundary should be the first irreversible external effect, not only the first live posting.** WFM-26 sets the boundary at "first live posting". That needs refining, because payment release, check printing, positive-pay issue files, donor notifications and acknowledgments are irreversible even when no ledger posting has happened yet (RECOMMENDATION, High).
- **Duplicate prevention rests on three mechanisms:**
  1. an **in-flight ownership register**, which assigns every open item to exactly one system with a fencing epoch;
  2. a **cross-system idempotency crosswalk**, which checks legacy payment attempts, check numbers, ACH trace numbers and rail references before any Unbound release;
  3. **partitioned check-number ranges with positive-pay continuity**.
  These extend CNV-ARC-003 fencing and CNV-PAY-004 (no automatic retry; stop or void before reissue).
- **ACH returns and NOCs arriving after cutover** for legacy-originated credits must route to Unbound via imported trace numbers. Most returns arrive within 2 banking days of settlement, but some classes allow 60 days [MIG-022] (VERIFIED-FACT, Medium). NOC corrections still apply within six banking days (CNV-PAY-002).
- **Unknown fence = no posting** (UNB-RCN-WF-020). An unknown payment outcome on the legacy side means the item is **not** adopted as payable. It is traced (CNV-PAY-004) and owned by legacy until resolved.

## 1. Strategy comparison (summary; detail in CSV)

| Strategy | Fit for DAF platform replacement | Why |
|---|---|---|
| S01 Big-bang (no parallel) | Poor | No independent verification before irreversible effects |
| S02 Big-bang writer switch + parallel shadow (recommended) | **Good** | One writer at a time; evidence before the switch; short freeze |
| S03 Phased by function (e.g. portal first, ledger later) | Conditional | Works only along BookOfRecord seams (UNB-XIN-ACC-010). For example, the donor portal goes first in read-only, or Unbound starts with the GL in Shadow. Payment release cannot be split from grant approval |
| S04 Long parallel with dual entry | Poor for entry segment | Staff double-keying causes divergence and duplicate payment risk; practitioners often skip it [MIG-007] |
| S05 Read-only legacy after cutover | **Required complement** | History access, audit, and returns lookup |
| S06 Bi-directional incremental sync | Rejected | Two authoritative writers (UNB-TEN-013) |
| S07 One-way incremental sync legacy→Unbound (shadow feed) | **Good as enabler** of S02 | Feeds the parallel run and the final delta |
| S08 Controlled freeze | **Required** (≤3 business days) | Quiesces in-flight work |
| S09 Sponsor-by-sponsor (multi-sponsor administrator) | **Good** | Tenant = legal sponsor (CNV-ARC-002) is the natural unit |
| S10 Account/fund-by-fund within one sponsor | Rejected for platform change; required for sponsor transfers | Shared bank, pools and positive pay in one case; legal form in the other (CNV-ENT-002) |

## 2. Reversible vs irreversible

| Class | Examples | Undo mechanism | Inside rollback window? |
|---|---|---|---|
| R1 Reversible technical | Routing binding, UI exposure, projections, staging, rehearsal cells | Re-route / rebuild (TENANT-AWARE-PERSISTENCE-DESIGN "Migration A→B→C", step 7) | Yes |
| R2 Compensable internal | Opening journals, live postings, reservations | Linked reversal entries (UNB-ACC-003); never delete | Until the first R3 effect; afterwards compensation only |
| R3 Irreversible external | Payment release to rail/ODFI, check print, positive-pay issue file, custodian trade or transfer instruction, donor/charity notification, tax acknowledgment, grant letter | None. Only a new compensating process (stop/void, recovery request, corrected acknowledgment, apology notice) | **Defines the boundary** |
| R4 Legal/authority | Legacy writer fence; credential revocation; partner token revocation | Re-grant through a new decision record | Fence release allowed before the first R2 posting (WFM-26-T11) |

**Rule (proposed UNB-MIG-045, refines RR-REQ-X-061-r1).** `RollbackBoundary = min(first live posting, first R3 effect)`.
- Before the boundary: WFM-26-T11 rollback (release the fence, legacy resumes, staging retained as evidence).
- After the boundary: forward compensation only (WFM-26-T13/T14). In addition, every R3 effect must be recorded in an **Effects Ledger** with its external reference, so that a reverse migration (exporting Unbound-era items back into legacy as a delta) is possible as a last resort and is itself a governed MigrationRun.
- For the first 5 business days after cutover, R3 dispatch is **rate-limited and dual-approved** (CNV-ECO-005 pre-delegation phase applies).

## 3. Duplicate-prevention design

### 3.1 In-flight ownership register (proposed UNB-MIG-040)

`InFlightItem { item_type, legacy_ids[], unbound_id?, state_at_freeze, owner: Legacy|Unbound|Frozen|Traced, fencing_epoch, assignment_rule_id, evidence_ref, resolved_at? }`

| Item at freeze | Default owner after cutover | Rule |
|---|---|---|
| Recommendation submitted, not approved | Unbound | Re-queued for sponsor review; charity re-checked (CNV-GRT-003) |
| Approved, not released | Unbound | Reservation re-created at E. Release blocked until payee verified (RR-REQ-X-061-r1) or networked enrolment reused (CNV-EXP-002) |
| Released, outcome known (settled) | Legacy history | Imported as a historical paid grant. No payable |
| Released, outcome **Unknown** | **Traced** (legacy-owned) | CNV-PAY-004 trace before any action. Not adopted as payable. Fund flagged (cf. UNB-XIN-EVA-009 "a fund with an Unknown payment must not transfer") |
| Check issued, uncleared | Unbound (liability), legacy check number preserved | In the Unbound positive-pay issue file from day 1 (§3.3). Reissue only after a confirmed stop/void (CNV-PAY-004) |
| ACH credit settled, return window open | Unbound (returns handling) | Trace number in crosswalk; returns route to the Unbound exception queue |
| Recurring schedule | Unbound (new schedule version, `imported_unverified`) | The next instance date must be ≥ E + freeze end. Instances dated inside the freeze are released once by Unbound, idempotent on `(legacy_schedule_id, instance_date)`. AEF processed in-window recurring items with possible delays [MIG-013] |
| Contribution in transit (stock transfer, wire, check in lockbox) | Unbound | Matched by custodian or bank feed. GiftCompletionDate from evidence (CNV-FIN-003); `Unknown` if absent |
| Acknowledgment due | The system that recorded the contribution's AcceptanceDate | Prevents duplicate receipts (runbook M18). Ownership token checked before issuing |
| Fee accrual period spanning E | Split: legacy to E-1, Unbound from E | Segment rule as UNB-XIN-ERP-001 ("migration cutover" segment) |

Completeness is gate G18/G19: 100% of items open at the high-water mark have exactly one owner.

### 3.2 Cross-system idempotency (proposed UNB-MIG-041)

- **Canonical grant key**: `(sponsor_legal_id, canonical_grant_id)`. Legacy grant IDs map to it through the crosswalk (14 §5).
- **Pre-release check.** Before any R3 dispatch, Unbound checks four sources, inside the same transaction as the release and with the CNV-ARC-003 fencing token:
  1. the imported legacy payment-attempt table;
  2. the rail partner's report of submitted references;
  3. the check register;
  4. the ACH originated-entries file from the ODFI (where the sponsor provides it).
  Any match → `DuplicateSuspected` → block plus a human case.
- **External idempotency keys** sent to rail partners include the canonical grant ID. Where a partner already holds a legacy reference, Unbound **re-uses the legacy reference** as the partner idempotency key, so that a replay is rejected by the partner as well. This needs confirmation per partner contract (HYPOTHESIS).
- **Contributions**: dedupe on `(custodian/bank reference, amount, value date)` against imported history and in-transit items. A match requires a human decision, so there is never an auto-merge on amount and date alone (consistent with `research/daf-cross-institution-reconciliation-evidence-2026-11-11.md` "do not use amount/date alone as a unique identifier").
- **Journals**: opening journals are idempotent per `(migration_run_id, entity, fund, class)`. Live journals are idempotent per event and posting-rule version (ACC-MDL-007).

### 3.3 Checks and positive pay (proposed UNB-MIG-042)

- **Partition check-number ranges** per disbursement account. Legacy keeps its last used range closed, and Unbound starts at a fresh, non-overlapping range recorded in the cutover plan.
- **Positive-pay continuity.** Whether a bank's issue file is incremental or full-replacement varies by bank (INFERENCE; confirm with each bank). Unbound's first issue file must therefore either be incremental or include **all outstanding legacy checks**, so that the bank does not reject legitimate legacy checks. Voids follow CNV-PAY-002 (daily issue files including voids).
- Stale and uncashed legacy checks keep their escheat clocks from the **original issue date**.

### 3.4 ACH and rails (proposed UNB-MIG-043)

- Import the legacy originated-entry trace numbers, the company ID and the effective dates for the return window. The return window is at least 2 banking days for most codes and up to 60 days for some unauthorized classes [MIG-022]. Use a conservative 60 days plus the bank's posting lag.
- Returns or NOCs that arrive at the ODFI for legacy entries are matched by trace number to the crosswalk and handled as Unbound exceptions against the imported grant.
- If the **ODFI or company ID changes at cutover**, the legacy ODFI channel must keep delivering returns for the window. This is a bank agreement item (HYPOTHESIS; not covered by the fetched sources).
- Rail-partner enrolments of charities are reused (CNV-EXP-002). Partner funds-in-transit limits (CNV-PLT-012) are measured across legacy plus Unbound submissions during the window.

## 4. Cutover runbook timeline (default)

| When | Activity | Evidence |
|---|---|---|
| T-60 | Calendar check (no Dec 15-Jan 5; not within 30 days of FY-end close; outside January statement season); rail, custodian and bank notices drafted | Cutover plan v1 |
| T-30 | TransitionWindow published to donors, advisors and active grant recipients (UNB-XIN-OTH-002) | Notice receipts |
| T-30..T-1 | Parallel shadow run ≥1 full close (CNV-FIN-004 ProvisionalCalibration); payee verification campaign to shrink `imported_unverified` | G26 results |
| T-3 BD | Freeze starts: new releases, payee changes, succession and authority changes frozen; recommendations accepted and queued; contributions accepted | TRANSITION_WINDOW responses |
| T-1 | Legacy close at E-1; final export at high-water mark; final delta run; gates G01-G25 | Gate report |
| T0 | Dual authorization (WFM-26-T08); fence legacy writer; confirm fence (not Unknown); post opening journals once; route switch | Fence confirmation, decision record |
| T0..T+5 BD | R3 effects dual-approved and rate-limited; first positive-pay file reviewed manually | Effects Ledger |
| T+30 | Independent post-cutover reconciliation (WFM-26-T15) | Sign-off |
| T+90 or later | Legacy retirement (15 §6); archive to sponsor | Retirement certificate |

## 5. Recovery playbooks

| Failure | Detection | Response | Anchors |
|---|---|---|---|
| Fence status Unknown | Fence call timeout | No posting; query until confirmed; roll back if still unknown at the freeze maximum end and notify within 1 BD | WFM-26-T10/T11; UNB-RCN-WF-020; UNB-XIN-OTH-002 |
| Legacy writes after fence | Legacy delta shows new postings | Incident; pause posting for affected funds; reconcile; compensate under sponsor approval | DKS-ENT-019; WFM-26-T13/T14 |
| Provider outage during cutover | Rail, custodian or bank API failure | Hold R3 effects; no blind retry; idempotent replay after recovery | Runbook M13; CNV-PAY-004; UNB-IMM-006 |
| Duplicate suspected | Pre-release crosswalk hit | Block; case; trace legacy attempt | UNB-MIG-041 |
| Post-cutover balance break | Daily reconciliation | Compensating entries (A4); statements for affected funds marked provisional | CNV-FIN-004; WFM-26-T13 |
| Freeze overruns maximum end | Timer | Notify affected parties within 1 BD with a new estimate | UNB-XIN-OTH-002 |
| Need to abandon after the boundary | Sponsor decision | No rollback. Either forward fix, or a governed reverse MigrationRun using the Effects Ledger | UNB-MIG-045 |

## Implications for Unbound

- A **short, scheduled, evidence-backed cutover** is a sales argument against the "two-year project" pattern seen in public FIMS-replacement stories [MIG-025] and the history truncation seen at AEF [MIG-012]. The binding constraint is payee re-verification (RR-REQ-X-061-r1). Reusing networked enrolments (CNV-EXP-002) and running a verification campaign during the parallel run are what keep it short (INFERENCE, Medium).
- The ownership register and crosswalk are the same machinery needed for partner exits and sponsor transfers (CNV-ENT-002), so building them once covers inbound and outbound.

Candidate requirements: **UNB-MIG-040** in-flight ownership register with 100% single-owner completeness; **UNB-MIG-041** cross-system pre-release duplicate check in the release transaction (refines CNV-ARC-003, RR-REQ-X-061-r1); **UNB-MIG-042** check-range partition and positive-pay continuity (refines CNV-PAY-002); **UNB-MIG-043** ACH return/NOC routing via imported trace numbers for ≥60 days (refines CNV-PAY-002/004); **UNB-MIG-044** epoch calendar policy (refines XID-OTH-001, UNB-XIN-OTH-002); **UNB-MIG-045** rollback boundary = min(first posting, first irreversible external effect) plus an Effects Ledger (refines RR-REQ-X-061-r1, WFM-26-T11); **UNB-MIG-046** acknowledgment ownership token (refines CNV-FIN-003, runbook M18).

## Open questions / evidence gaps

- Bank-specific positive-pay file semantics (incremental vs full replacement) and ODFI return routing after an originator change. These need bank documentation.
- Whether rail partners (PayPal Grant Payments, Chariot/DAFpay and others) accept a caller-supplied idempotency key that equals a legacy reference.
- Fiscal-year distribution of entry-segment sponsors (calendar vs June 30), which affects the preferred epoch window. Form 990 data could answer this.
- No public account of an entry-segment national sponsor's platform cutover was found. The AEF/Ren materials cover only portal-level effects [MIG-012..014].
