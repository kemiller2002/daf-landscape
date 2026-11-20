# W8: system-of-record migration

**Outcome (BO-59, BO-60):** when a sponsor changes its platform or administrator, or winds down, every account's full history and balances carry over exactly. Donors lose no records, and the sponsor's books stay continuous.

**Evidence:**
- AEF's move onto Ren left donors two years of directly accessible history (EV-037).
- Ren's iPhi lost 6 of 57 sponsors in 2023–Nov 2026 (industry report §11.2).
- Six of six documented DAF-tech exits went to consolidators (EV-119).
- Give Interactive's Vanguard mandate is a vendor claim (EV-057).
- Community-foundation exits exist (cf-exits data).

## 1. First principles

| Necessary | Not necessary |
|---|---|
| Every economic event and decision with its evidence, in a form the next system can interpret | Schema-to-schema conversion in one weekend |
| Opening balances that reconcile to custody and bank | Freezing operations for weeks |
| Continuity of identifiers (account, grant, recipient) | Re-issuing account numbers |
| Proof that nothing was lost (reconciliation report) | Sampling-based migration sign-off only |

## 2. Inversion
- **What if migration never happened as a project?** The record is *always* exportable as an event log, and any system can replay it (INN-18).
- **What if the sponsor never owned a "system" at all?** The record lives in a neutral substrate and administrators are swappable operators (D-W8-4).
- **What if a partner did it?** Migration as a service, with verification (D-W8-5).

## 3. Competing designs

| ID | Type | Mechanism | Decides / when | Authoritative data | Humans | Controls | Cost | Experience | INN | Maturity |
|---|---|---|---|---|---|---|---|---|---|---|
| D-W8-1 | Conventional | Vendor-led project: map tables, convert, cut over at a weekend, keep N years online, archive the rest | Project steering; at cutover | Old system until cutover, then new | Large project team | Parallel run; sampled reconciliation | Months of staff and vendor fees | History truncated (AEF: 2 years); portal change | — | Observed (EV-037) |
| D-W8-2 | Automation-first | Automated ETL with full reconciliation reports; all history loaded as static documents | Same | Same | Smaller team | Full reconciliation | Lower | Old history as PDFs | — | L1 |
| D-W8-3 | AI-native | Continuous open-format export (open grant record plus event log). Migration = replay into the new system, then verify invariants (balances, counts, Schedule D aggregates). Agents map exotic legacy fields; deterministic validators confirm | Controller signs off replay invariants | Event log | Controller; agent owner for mapping | Invariant tests (balances, Schedule D, grant counts); hash chain | Low marginal | No visible change; full history | INN-18 | L2 (PoC: ledger and Schedule D derive from events; replay property tested in E8) |
| D-W8-4 | **Radical: no migration ever: neutral record substrate, swappable operators** | The sponsor's books live in a neutral, sponsor-owned record substrate (escrowed data trust or sponsor-controlled database). Administrators and vendors are *operators* with scoped write access via events. Changing administrator = revoking one operator's keys and granting another's | Sponsor (owner of the record) at any time | Sponsor-owned substrate | Sponsor data steward | Operator key rotation; append-only log; independent hash attestations | Substrate cost; operators compete | Invisible | INN-18 | L0 |
| D-W8-5 | Ecosystem: migration-as-a-service with certification | An independent party certifies migrations: full-history replay plus reconciliation certificate published to the sponsor's board and auditor | Board accepts certificate | Old and new systems | Certifier | Independent attestation | Certification fee | Full history assured | INN-18 | L1 |
| D-W8-6 | Contractual: exit-readiness as a procurement term | Sponsors require vendors to provide full-fidelity event export quarterly, with restore drills (CTL vendor exit-readiness in 08) | Sponsor procurement | Vendor system plus quarterly exports | Vendor manager | Restore drill evidence | Negotiation leverage | — | INN-18 | L1 (Q-N04: executed contracts unseen, GAP-002) |

## 4. Constraint ledger

| Constraint | D-W8-3 | D-W8-4 radical | D-W8-6 |
|---|---|---|---|
| Legal (record retention REG-026; donor records) | Survives | Survives | Survives |
| Fiduciary (vendor oversight) | Survives | Strengthened: sponsor owns its data | Strengthened |
| Accounting (continuity; auditor acceptance) | Replay invariants give evidence | Requires auditors to accept a substrate with multiple writers | Survives |
| Privacy / security | Export files are sensitive: encrypt, minimize | The substrate is a concentration target | Survives |
| Economic | Low | Vendors lose lock-in and resist. Sponsors pay substrate cost | Leverage only at renewal |
| Operational | Needs event-native source; legacy sources need one-time conversion | Requires operators to write events in a common schema | Needs negotiation |
| Human acceptance | High | Vendors resist; sponsors unfamiliar | Medium |

**Survivors:**
- D-W8-3 inside our platform (native).
- D-W8-6 as a recommendation to any sponsor, and as Model C's sales promise: "we make leaving us easy".
- D-W8-4 is held. It is attractive to sponsors and is a credible *product position* for Model C ("your data, our operations"), but it depends on a common event schema.

## 5. Analogies
- **Database replication and log shipping.** D-W8-3. Breaks only on semantic mapping from legacy systems.
- **Data escrow** (software escrow; personal data stores). D-W8-4. Breaks on adoption.
- **Bank core conversions.** Famously painful. They show that conversion risk lies in semantics, not in moving data.

## 6. Seven perspectives

| Perspective | Position |
|---|---|
| Inventor | D-W8-4: decouple record ownership from operations |
| Architect | Event-native from day one makes D-W8-3 trivial. D-W8-4 needs a published schema (open grant record v0.1 is a start) |
| Economist | Lower switching costs hurt incumbents and help challengers. A challenger should *lead* with portability |
| Regulatory | No conflict. Retention must be preserved across moves |
| Adversarial | A full export is a data-exfiltration path. Access to exports must be dual-controlled. Replay can import corrupted history faithfully, so it needs independent source reconciliation |
| Customer advocate | History loss is a real donor harm (tax substantiation) |
| Commercial | "Leave anytime with everything" builds trust, and it is hard for lock-in businesses to match |

**Disagreement:** the commercial strategist vs the economist on whether making exit easy reduces Model C's own retention. Resolution proposed: compete on operations, not lock-in, consistent with DD-006 and R8 in the parent report.

## 7. Experiments and recommendation
- **E8:** replay an exported event log into a fresh state; assert identical balances, grant states and Schedule D aggregates. Includes adversarial cases: truncated log, duplicated events, reordered events.
- **Recommendation:** adopt D-W8-3 and D-W8-6; hold D-W8-4 as a product thesis for Model C.
