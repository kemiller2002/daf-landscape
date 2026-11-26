# 16 - Financial reconciliation as the primary migration acceptance gate (B7)

Status: research draft (2026-11-26). Not legal advice. Evidence classes per 01-research-methodology.md.

Scope: what must reconcile, how exactly, under what tolerance, and which discrepancies block cutover. The gate register is in `data/reconciliation-gates.csv` (G01-G29). It builds on WFM-26-T04/T07/T15, CNV-FIN-004 (continuous reconciliation, ProvisionalCalibration), CNV-FIN-011 (no numeric materiality default), UNB-NAV-012/022 (no unexplained plug; decimal arithmetic) and UNB-RCN-WF-009 (activation requires tied-out opening balances). Notation: `(CLASS, confidence)`.

## Summary

- **Financial correctness is the acceptance gate, and UI parity is not.** A migration passes when every blocking gate in `data/reconciliation-gates.csv` passes on the final-delta manifest and an independent reconciler signs off (GOV-AUTH-014, WFM-26-T15). It does not pass because screens look right (RECOMMENDATION, High).
- **Three kinds of comparison, which must never be mixed:**
  - **Exact**: counts, cash and fund ledgers in cents, unit balances at source precision, open payables, check registers. Tolerance is zero.
  - **Declared rounding**: unitized values and fee accrual recomputation. Tolerance is a deterministic bound derived from precision, and the residual is allocated by an approved deterministic rule.
  - **Explained difference**: valuation source or timing differences, legacy statement errors, `HistoryGap`. Each difference is itemized with evidence and approved. There is no numeric "materiality" threshold, because the CFO decides materiality qualitatively per CNV-FIN-011.
- **No plugs.** `3090 Opening balance/control` must be exactly zero after the opening TB loads. Any unexplained residual blocks cutover. A rounding account may receive only amounts produced by the declared residual algorithm, each itemized to a fund (UNB-NAV-012) (RECOMMENDATION, High).
- **Unitized pools are the hardest case.** Units are imported **exactly at source precision**. Pool outstanding units must equal the sum of fund units exactly. The dollar value of each fund = units × price, with residual cents allocated by largest-remainder and a deterministic tiebreak (worked example in §3). Changing unit precision is a governed conversion under UNB-NAV-031, never a side effect of import.
- **Book of record decides what "reconcile to GL" means.** When the sponsor keeps its entity GL in an ERP (CNV-FIN-012; UNB-XIN-ACC-010 `Shadow`), the GL gates compare Unbound's program ledger to the sponsor GL control accounts. They do not compare to an Unbound GL that is not authoritative.
- **Gates that block cutover**: all exact gates, unit integrity, external custody and bank ties at the epoch, open liabilities (grants payable, outstanding checks), in-flight ownership completeness, and opening-balance control. **Non-blocking but must clear before first close**: historical statement recomputation differences, `HistoryGap` disclosures, classification suspense (RR-UNB-ACC-033-r1).
- **The auditor is a primary consumer.** AU-C 510 says reviewing predecessor working papers cannot be the only evidence for opening balances [MIG-016]. The migration's reproducible manifest, roll-forward proofs and custody/bank ties are designed to be that additional evidence (INFERENCE, Medium).
- **Aggregate tie-outs cannot see total-preserving mis-mappings (ADVB-09).** Two gates are added for that. G28 is a stratified, sponsor-attested record-level sample. G29 covers semantic invariants plus mutation-test detection. Both block cutover.
- **Grant recognition point (CNV-FIN-007) is an epoch gate (ADVB-08).** G27 has four parts:
  - the legacy convention is identified;
  - the cutoff register is built at E-1;
  - grants payable is reconciled under the legacy convention and shown, for information, under the target convention;
  - any change of convention waits for the auditor's acceptance (default: next fiscal year-end).
- **Unbound will not yet have a SOC 1 Type II report (ADVB-10).** No SOC 1 Type II report will cover the first sponsor's first audited period. The sponsor's auditor is therefore likely to do more substantive testing at the sponsor's cost, and that uplift belongs in the buyer TCO (draft 20). Mitigation: a Type I at go-live, a Type II window that overlaps the first sponsor's fiscal year (Type II periods are typically ≥6 months [ADVB-018]), and an evidence pack built for direct substantive use (§6a) (INFERENCE, Medium).

## 1. Reconciliation levels

| Level | What is compared | Sources | Comparison kind | Gate IDs |
|---|---|---|---|---|
| L1 Completeness | Record counts and control totals per entity, file and period | L0 manifest vs L1 vs L2 | Exact | G01-G03 |
| L2 Fund | Each DAF balance at E-1 (cash ledger), contributions, grants, fees YTD | Legacy fund balance report vs CMM opening | Exact | G04-G05 |
| L3 Sponsor | Σ funds = sponsor DAF program total; TB balances; `3090` = 0 | Legacy TB vs opening journals | Exact | G07-G09 |
| L4 External | Custodian positions (quantity) and cash; bank balances | Custodian statement / feed at E-1; bank statement | Exact on quantity and cash; explained on timing | G10-G13 |
| L5 Liabilities | Grants payable (approved unpaid), outstanding checks, accrued fees, payables to rails | Legacy registers, bank paid-item file, rail partner reports | Exact + itemized | G14-G17 |
| L6 In-flight | Pending contributions, reservations, unknown payments, open returns | In-flight register (17) | Exact count; ownership assigned 100%; payee verification status | G18-G19, G25 |
| L7 Units/NAV | Fund units, pool outstanding units, unit price, value | Legacy unit register, manager/custodian | Exact units; declared rounding on value | G20-G21 |
| L8 Restrictions | Restricted balances, restriction records, net-asset class | Legacy restriction data; fund agreements | Exact amounts; classification evidence | G22 |
| L9 History | Roll-forward proof; recomputed vs as-issued statements; acknowledgment dedup | History partition vs opening; L0 statements | Exact or explained | G06, G23-G24 |
| L10 Parallel | Shadow vs legacy at the extract cadence allowed (15 §1a) | Both systems / as-issued statements | ProvisionalCalibration zero tolerance | G26 |
| L11 Semantics | Record-level sample; semantic invariants; mutation-test detection | Source reports vs Unbound views | Exact per sampled attribute; 100% detection | G28-G29 |
| L12 Recognition | Grant recognition convention and cutoff register at E-1 | Legacy grants payable vs cutoff register | Exact under legacy convention | G27 |

## 2. Tolerance philosophy

1. **Exact where the representation permits.** Money is decimal cents in both systems, and units are decimals at declared scale. If both sides represent a quantity at the same precision, the tolerance is **zero**. A "small" difference there means a missing or duplicated item, and that is exactly what reconciliation exists to find (INFERENCE, High).
2. **Declared rounding where representation differs.** The bound is computed, not chosen. For n funds valued at price p with cent rounding, the maximum aggregate absolute residual is `n × $0.005`, and after largest-remainder allocation the pool total matches exactly. A per-fund difference above $0.005 against an independent recompute is a failure.
3. **Explained differences** for timing and valuation:
   - Each needs an itemized reconciling item: deposit in transit, outstanding check, unsettled trade, pending corporate action, price-source difference.
   - Each item carries source IDs and evidence and is approved by the controller.
   - Unattributable breaks go to a controller decision (CNV-FIN-004) and **block cutover**. That is stricter than steady state, where they block only the affected statements.
4. **No silent discard, no unauthorized plug.** Every reconciling item and every residual cent is itemized, owned and evidenced. A suspense account is permitted **only** for the RR-UNB-ACC-033-r1 classification case. Amount differences never go to suspense.
5. **Materiality.** No numeric materiality default ships (CNV-FIN-011). Where the CFO decides a historical statement difference is immaterial, the decision record states the qualitative assessment. ASC 250 governs how errors found in previously issued statements are treated [MIG-017].

## 3. Unitized NAV pools: worked rounding example

Synthetic pool. Legacy unit precision is 4 dp, the price is 1.004 per unit, and there are 1,000,000.0000 units outstanding, so the pool value is $1,004,000.00.

| Fund | Units (exact) | Units × price | Half-even cents | Floor cents | Remainder | Largest-remainder allocation |
|---|---:|---:|---:|---:|---:|---:|
| F1 | 1.0000 | 1.004 | 1.00 | 1.00 | 0.004 | 1.01 (tiebreak: lowest fund ID) |
| F2 | 1.0000 | 1.004 | 1.00 | 1.00 | 0.004 | 1.00 |
| F3 | 1.0000 | 1.004 | 1.00 | 1.00 | 0.004 | 1.00 |
| F4 | 999,997.0000 | 1,003,996.988 | 1,003,996.99 | 1,003,996.98 | 0.008 | 1,003,996.99 |
| **Σ** | 1,000,000.0000 | 1,004,000.000 | **1,003,999.99** (-0.01) | 1,003,999.98 | | **1,004,000.00** |

Independent per-fund half-even rounding leaves a **$0.01** pool-level difference. That is real and explainable, not an error. The rule (proposed UNB-MIG-031) is:
- Fund **units** must match the legacy register exactly.
- Fund **values** are computed by the declared allocation algorithm (here largest remainder, tiebreak by fund ID, which is deterministic).
- Each fund's value may differ from the legacy-reported value by at most $0.01, and only where legacy used a different rounding algorithm. Every such fund is listed.
- The pool total must equal the custodian/manager pool value at E-1 exactly, or itemized reconciling items must explain the difference.

Where CNV-FIN-005 applies (the external manager publishes unit values), Unbound may not be the unit register. The BookOfRecord for `UnitRegister` is then `Shadow` (UNB-XIN-ACC-010), and G20/G21 compare Unbound's imported units to the manager's register rather than create a new one.

## 4. Timing and cutoff alignment

At E-1, close of business, the following must share one as-of definition: the legacy fund balance report, the custodian position and cash statements, the bank statements, the rail-partner pending reports and the check register. A cutoff matrix records each source's actual cutoff, for example custodian T+1 settlement or bank statement close. Differences are bridged by itemized reconciling items in standard bank-reconciliation form. Foundant's own guidance is to compare a legacy Fund Balance or Trial Balance report "as of your migration date" [MIG-002] (VENDOR-CLAIM, Medium). Unbound extends this to external evidence, because legacy-to-new agreement alone proves only that the copy is faithful, not that the legacy books were right (INFERENCE, High).

## 5. Historical statements (non-blocking, disclosed)

For each fund and each as-issued legacy statement available in L0, Unbound recomputes the statement balance from the history partition and classifies the result:
- `Match`
- `LegacyStatementError` (the legacy statement disagrees with its own transactions)
- `HistoryIncomplete` (transactions missing)
- `MethodDifference` (fee or unit methodology).

As-issued statements remain the donor-facing record of what was issued (UNB-NAV-010). Differences are disclosed to the sponsor and resolved under CNV-FIN-011. They do not block cutover unless they reveal a break at E-1, which G04 would catch anyway.

## 6. Who signs what

| Artefact | Preparer | Approver | Independent check |
|---|---|---|---|
| Gate results (per run) | Migration operator (system-generated) | Controller | Rehearsal re-run reproduces the output hash |
| Explained-difference items | Sponsor finance | Controller (A4) | Sample tested by the sponsor's auditor (optional) |
| Reconciliation report (CNV-EXP-002) | System | Sponsor CFO + finance (WFM-26-T08 dual approval) | Post-cutover reconciler ≠ operator (GOV-AUTH-014) |
| Auditor opening-balance pack | System | Controller | External auditor (AU-C 510 [MIG-016]) |

**Auditor opening-balance pack** (proposed UNB-MIG-033): the legacy TB at E-1, the L0 manifest and hashes, the mapping version, the run manifest, the roll-forward proofs, custody and bank ties at E-1, the itemized reconciling items, the rounding allocation listing, and a sample of traces from opening journal → L2 → L1 → L0 byte range.

### 6a. Audit evidence without a Type II report (ADVB-10)

| Period | Assurance available from Unbound | What the sponsor's auditor will likely need | Design response |
|---|---|---|---|
| Pre-epoch (legacy) | None (legacy vendor's SOC report, if any) | Predecessor evidence + AU-C 510 opening-balance procedures [MIG-016] | Opening-balance pack (UNB-MIG-033) with re-performable manifests |
| Epoch to first Type II report | SOC 1 Type I (design only) at best | Substantive tests of transactions processed by Unbound; walkthroughs | Pack items: control-evidence exports (approvals, SoD, reconciliations) per transaction; read-only auditor access; sample-pull tooling |
| After the Type II window | SOC 1 Type II covering ≥6 months overlapping the sponsor FY [ADVB-018] | Reliance on controls + complementary user-entity controls | Publish CUECs mapped to sponsor duties |

Timing rule (proposed UNB-MIG-035): choose the first sponsor's epoch so that the Type II observation window can cover most of the sponsor's first fiscal year on Unbound. A fiscal-year-start epoch fits this best, which is in tension with 17's calendar preference; 17 §0 resolves the tension. The design-partner contract discloses the expected audit-fee uplift. CNV-ECO-003 evidence obligations measure it.

## Implications for Unbound

- The gate register is a sellable artefact. It turns "will our books survive the move?" from a vendor promise into a checklist the CFO and auditor can verify. The public evidence contains no comparable incumbent artefact (not publicly documented).
- The strict blocking rules (zero tolerance on exact gates, unattributable break = no cutover) will lengthen the first migrations. The rehearsal cadence in 15 is the mitigation.
- Requiring custody and bank ties will surface **pre-existing legacy errors**. The sponsor needs a decision path (fix in legacy before E, or carry as an explained difference) so that Unbound is not blamed for them. This is a customer-success and contract item.

Candidate requirements:
- **UNB-MIG-030** A migration gate register with three comparison kinds (exact / declared-rounding / explained); an unattributable break blocks cutover (refines CNV-FIN-004, WFM-26-T04).
- **UNB-MIG-031** Unit import at source precision; deterministic largest-remainder value allocation with itemized residuals; precision change only via UNB-NAV-031 (refines UNB-NAV-012/022/031).
- **UNB-MIG-032** `3090` opening control must be exactly zero; suspense is allowed only for the RR-UNB-ACC-033-r1 classification case (refines UNB-RCN-WF-009).
- **UNB-MIG-033** Auditor opening-balance pack (refines UNB-ACC-025).
- **UNB-MIG-034** Historical statement recompute and classification, with as-issued statements preserved (refines UNB-NAV-010, CNV-EXP-002).
- **UNB-MIG-035** SOC 1 timing plan: Type I at first go-live; Type II window overlapping the first sponsor's fiscal year; audit-fee uplift disclosed (refines RCD-031 SOC 1 design).
- **UNB-MIG-036** Epoch recognition gate G27 and semantic gates G28/G29 are blocking (refines CNV-FIN-007, UNB-MIG-005).

## Open questions / evidence gaps

- Whether sponsors' auditors accept migration evidence packs in lieu of extended substantive testing of opening balances. Needs auditor interviews.
- Real legacy rounding behaviours (Ren, FIMS) are unknown. The §3 example is synthetic.
- How rail partners report pending items at a point in time (L11, L13): whether a dated pending-grant register is available from each partner.

## Adversarial review response

| ID | Response |
|---|---|
| ADVB-06 | **Accepted in part.** Gate results on intermediate rehearsals are system-generated. The controller approves only the final rehearsal, the production run, and the explained differences. |
| ADVB-08 | **Accepted.** G27 added and L12 level added. Convention changes wait for the auditor (default fiscal year-end). The unit and fee design is unchanged, as the reviewer agreed. |
| ADVB-09 | **Accepted.** G28 (attested record-level sample) and G29 (invariants and mutation detection) added, both blocking. |
| ADVB-10 | **Accepted.** §6a and UNB-MIG-035 added. I am not claiming the evidence pack substitutes for a Type II report; it only reduces the auditor's substantive effort, and how much is unproven. |

