# W10: compliance evidence, audit, filings and state registration

**Outcome:** every legal obligation is owned, operating and provable on demand. Filings are correct and on time. The board, auditors and regulators can see the evidence (BO-34–37, BO-45, BO-49–50, BO-63).

**Evidence:**
- No sponsor publishes operating metrics (EV-076).
- State charitable solicitation registration covers about 40 states plus DC (REG-053).
- Audit thresholds are state-specific (REG-054).
- §6033(k) requires Schedule D Part I (REG-013).
- OFAC record-keeping runs 10 years (REG-037).
- The parent workstream maps 65 requirements to 50 controls; the CTL→REG mapping is an open item.

## 1. First principles

| Necessary | Not necessary |
|---|---|
| Each obligation mapped to a control with an owner | Prose manuals as the operative control |
| Evidence that the control operated, for each instance | Annual staff attestations as primary evidence |
| Accurate filings derived from the books | Re-keying into tax software |
| Human sign-off where law requires an officer (990, 8283, 4720, state filings) | Humans assembling the content |
| Independent assurance (external audit; internal audit) | Sampled document hunts (PBC lists) |

## 2. Inversion
- **What if evidence were never assembled?** It is produced by the operation itself (INN-20).
- **What if compliance were evaluated continuously?** An obligation→control coverage test runs on every change (parent CTL-037 concept).
- **What if the auditor never asked for a sample?** Read access to the evidence ledger, plus reproducible queries.
- **What if an external partner maintained the policies?** Shared policy packs (INN-36, D-W10-5).

## 3. Competing designs

| ID | Type | Mechanism | Decides / when | Authoritative data | Humans | Controls | Cost | Experience | INN | Maturity |
|---|---|---|---|---|---|---|---|---|---|---|
| D-W10-1 | Conventional | Policy manuals; annual attestations; auditors' PBC lists; 990 prepared from trial balance by a tax preparer; state registrations tracked in a spreadsheet | Staff per cycle | Scattered systems | Compliance, finance, tax preparer | Manual reviews | Recurring staff and fees | Reactive | — | Inferred |
| D-W10-2 | Automation-first | GRC tool with control library, reminders, document repository; 990 data export | Same | GRC plus ledger | Fewer | Tool workflows | Tool licence | Less chasing | — | L1 |
| D-W10-3 | AI-native | Evidence ledger: each control emits evidence when it operates; obligation register machine-readable; coverage test on every policy change; filings generated from the ledger; agents draft narratives (990 Part III, board pack), officers sign | Officers sign; coverage test deterministic | Event and evidence ledger | CRCO, CFO, GC | CTL-037 coverage; evidence completeness 100% | Low marginal | On-demand audit packages | INN-20, INN-21 | L3 (partial: PoC emits evidence records and Schedule D aggregates; coverage test not yet built) |
| D-W10-4 | **Radical: continuous external assurance (auditor-in-the-loop)** | Instead of an annual audit cycle, the external auditor (or an assurance provider) holds standing read access, runs its own queries continuously, and issues ongoing assurance with an annual opinion as a checkpoint. The regulator-facing view is a pre-agreed query set. Changes the *performing organization* and the *timing* of assurance | Auditor continuously; board receives a running assurance report | Evidence ledger (shared read) | Auditor; CRCO | Read-only, logged auditor access; independence safeguards | Auditor fee structure changes | No audit season | INN-20, INN-32 | L0 |
| D-W10-5 | Ecosystem: shared compliance policy packs and registration utility | A provider maintains cited, back-tested policy packs (§4966/4967, OFAC, state rules) and a state-registration filing utility for many sponsors; each board adopts and parameterizes | Each sponsor's board and counsel | Provider library plus sponsor parameters | Sponsor counsel review | Version pinning; diff review | Subscription | Lower cost for small sponsors | INN-36 | L1 |
| D-W10-6 | Contrarian: publish operating metrics | Sponsor publishes P50/P90 grant latency, exception rates and evidence coverage (none do today, EV-076). Transparency becomes a control (external scrutiny) and a market signal | Board policy | Telemetry | CRCO | Metric definitions audited | Low | Donors and nonprofits see performance | INN-30 | L1 |

## 4. Constraint ledger

| Constraint | D-W10-3 | D-W10-4 radical | D-W10-5 | D-W10-6 |
|---|---|---|---|---|
| Legal (officer signatures; record retention; OFAC records) | Survives; humans sign | Survives. The annual opinion still required where state thresholds apply (REG-054) | Each board remains responsible | Survives |
| Fiduciary | Survives | Auditor independence must be preserved: auditor reads, never designs controls | Correlated error across sponsors if a pack is wrong | Survives |
| Accounting (audit standards) | Survives | Requires auditing-standard acceptance of continuous procedures; feasible in principle, firm methodology dependent | Survives | Survives |
| Privacy / security | Evidence contains PII; minimize, pseudonymize | Auditor access is broad; scope it | Packs contain no donor data | Aggregates only |
| Economic | Low | Audit firm pricing uncertain | Subscription viable for the long tail (1,240 sponsors under $50m hold 2.84% of assets) | Low |
| Operational | Needs evidence by construction | Needs auditor willingness | Needs a provider | Needs telemetry |
| Human acceptance | High internally | Audit firms conservative | Sponsors want autonomy | Incumbents will not follow, so it is a differentiator |

**Survivors:** D-W10-3, D-W10-5 (for Model C), D-W10-6. D-W10-4 is held pending auditor engagement (design-partner auditor interview in Phase 1).

## 5. Analogies
- **Continuous auditing / continuous controls monitoring** in large enterprises. It exists in practice. Breaks: small nonprofits' auditors may lack tooling.
- **Aviation safety management systems.** Continuous reporting with a regulator. Breaks: the FAA has a direct mandate.
- **Tax-software rule libraries.** D-W10-5. Works: law is common, parameters vary.

## 6. Seven perspectives

| Perspective | Position |
|---|---|
| Inventor | D-W10-4: the audit becomes a stream |
| Architect | Evidence by construction is already the parent design; add coverage tests |
| Economist | Large savings come from removing reconstruction effort (unmeasured). Packs have scale economies |
| Regulatory | Officers must sign; the auditor must stay independent; a shared pack must not become an outsourced legal judgment, since each board adopts it |
| Adversarial | "Green dashboards" can hide gaps where evidence is produced but not meaningful. Coverage tests check existence, not effectiveness; seeded-defect tests (CTL-046) are needed. Shared packs create correlated failure (FM in 13-) |
| Customer advocate | Published metrics help donors and nonprofits |
| Commercial | Audit evidence was one of the top-scoring product candidates (10-: 3.55). Packs suit Model C |

**Disagreement:** the adversarial reviewer vs the inventor on whether continuous assurance changes auditor behavior or just volume.

## 7. Experiments and recommendation
- **E2:** includes evidence completeness of every decision as a metric.
- **E4:** reconciliation evidence.
- **Coverage test** (desk/prototype): the obligation→control mapping is in the open items.
- **Recommendation:** adopt D-W10-3 and D-W10-6; offer D-W10-5 in Model C; hold D-W10-4 pending auditor interest.
