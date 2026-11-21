# W11: reconciliation and close (watch-list)

**Outcome (BO-18, BO-19):** fund balances are correct daily, and the books agree with the custodian and the bank.
**Evidence: Low.** No public data exists on break rates or close effort (GAP-005). The batch-file custody integration is inferred.

| ID | Type | Mechanism | Decides / when | Authoritative data | Humans | Maturity | INN |
|---|---|---|---|---|---|---|---|
| D-W11-1 | Conventional | Daily or periodic recordkeeper reconciliation; month-end close as a multi-day project; manual break research | Accountants at period end | Recordkeeper vs custodian statements | Fund accountants | Inferred | — |
| D-W11-2 | Automation-first | Rules-based matching tool; break queue; faster close | Accountants | Same | Fewer | L1 | — |
| D-W11-3 | AI-native | Continuous three-way reconciliation as invariants on events (ledger ↔ custodian ↔ bank); break-triage agent proposes causes; controller attests monthly (CTL-048) | Rules continuously; controller monthly | Event ledger plus feeds | Controller | L2 (PoC `reconcile`; E4 forthcoming) | INN-22 |
| D-W11-4 | **Radical: reconciliation by construction (unique keys end-to-end)** | Every external movement is *initiated* with a unique key the counterparty echoes back: contribution references or virtual accounts (INN-23), payment idempotency keys in addenda (INN-08), trade IDs. Matching becomes equality, so the break class "can't match" disappears. What remains is "counterparty didn't do what we instructed" | No matching decision exists; only exception decisions | Keys in our instructions | Controller on genuine exceptions | L1 | INN-23, INN-08 |
| D-W11-5 | Ecosystem: custodian- or bank-provided sub-ledgers | The custodian maintains per-account sub-ledgers and the sponsor consumes them; or a fund-administration provider does the reconciliation | Provider | Provider's books | Oversight | L1 | — |

**Constraint pass:**
- Independent verification (accounting) kills any design where one system both records and confirms. External statements must remain the independent source, so D-W11-4 still reconciles; it just has far fewer ambiguous breaks.
- D-W11-5 dies for Model C if it introduces a second system of record. It is held.

**Perspectives:**
- **Architect:** D-W11-4 is a design rule, not a project.
- **Adversarial:** feed outages hide breaks, so a "no feed" condition must itself be a break.
- **Economist:** the value is unmeasured until GAP-005 is closed.
- **Unresolved:** custodian support for references or sub-accounts.

**Experiments:** E4 compares (a) periodic reconciliation, (b) continuous reconciliation and (c) keyed-by-construction under injected breaks. Metrics: detection latency, human minutes, undetected breaks.
**Recommendation:** adopt D-W11-3 plus D-W11-4 as design rules.
