# Governance architecture

**Outcome served:** O-10, governance and fiduciary oversight. It also governs everything else. Controls are referenced by CTL id ([`controls.csv`](controls.csv)), and legal duties by the REG map ([`regulatory-applicability-map.md`](regulatory-applicability-map.md)).

## 1. Why governance is the hard core of an AI-native sponsor

Automation moves most *operations* out of human hands ([decision census](../01-enterprise-outcomes/activity-classification.md): 33 of 81 decision types are human, all low-volume). The *authority* that sets the rules for the automated decisions concentrates as a result. A threshold, a fuzzy-match cutoff or an agent's tool scope is a policy decision made once and applied at scale. If governance does not treat those parameters as governed objects, the enterprise's real policy is set by whoever edits configuration. The architecture's answer is to make every such parameter a versioned **Policy** with an approval record (CTL-009, CTL-010, CTL-024).

## 2. Board and committees

| Body | Composition | Core responsibilities | Evidence it receives |
|---|---|---|---|
| **Board** | ≥5 directors. Independent majority; **no director paid by, or holding equity in, a material vendor** (policy, stricter than law) | Mission, strategy, risk appetite, delegations of authority, CEO oversight, fee schedule, discretionary-hold policy, variance-power policy | Board evidence pack (§6) |
| **Audit and Risk Committee** | ≥3 independent directors; at least one with financial expertise and one with technology or model-risk expertise | External auditor appointment; internal audit plan; control health; model risk (AI); related-party transactions (CTL-042); incidents; regulatory inquiries | Control-health dashboard, internal audit reports, incident register, agent inventory changes |
| **Investment Committee** | ≥3, majority independent; may include non-director experts without vote on related-party matters | IPS, pools and menus, managers, rebalancing parameters (CTL-024), liquidity buffer parameters, advisor-program mandates and fee caps (CTL-025) | Daily compliance-to-IPS evidence, liquidity forecast versus actual, manager reports |
| **Governance and Nominating Committee** | Independent directors | Board composition, conflict register (CTL-041), delegation register review, policy on donor and advisor influence | Conflict register, recusal log |

**Why the vendor-independence rule.** The repository documents two patterns that a new sponsor should not copy, even though both were disclosed:
- **Charityvest and Foundation Source.** Charityvest's president and director is paid by its technology provider ($163,944 via Vennfi, 2024), and a Foundation Source executive sits on Charityvest's board ([industry report §2.3](../../DAF-INDUSTRY-REPORT-2026-11.md); [`sponsor-governance-and-fee-transparency-2026-11-11.md`](../../sponsor-governance-and-fee-transparency-2026-11-11.md)).
- **RCF and Ren.** RCF's 2024 Schedule L reports a $19,225,546 related-party administration transaction with Renaissance Administration LLC, with an officer overlap ([`rcf-ren-governance-related-party-controls-institutional-comparison-2026-11-12.md`](../../rcf-ren-governance-related-party-controls-institutional-comparison-2026-11-12.md)).

The repository is explicit that disclosure is not proof of wrongdoing, nor of arm's-length economics. The design simply removes the question.

**Special case: Model C or the hybrid.** If the infrastructure company and the sponsor are related (for example, the infrastructure company founds a sponsor as its anchor customer), the sponsor board needs:
- an independent majority with no equity in the infrastructure company;
- annual market-testing of the services agreement;
- disinterested approval of all pricing (CTL-042).

This is the structural risk of the hybrid model. It is evaluated in [`../10-market-and-business-model/`](../10-market-and-business-model/).

## 3. Delegation of authority (machine-enforced)

The delegation register is a Policy object. The authorization service reads it: a person whose delegated limit is below the item is *unable* to approve, so there is no warning to override. Initial values are assumptions **[A]**.

| Decision | Board | Committee | CEO | Officer (CFO/CRCO/GC) | Specialist | Deterministic policy |
|---|---|---|---|---|---|---|
| Strategy, risk appetite, delegations, fee schedule | **A** | recommends | proposes | — | — | — |
| IPS, pools, managers | approves material | **A** (Investment) | — | C | — | — |
| Rebalancing within bands | — | sets bands | — | — | — | **executes** |
| Routine grant ≤$250k [A], no flags | — | — | — | — | — | **approves** |
| Routine grant >$250k [A] | — | — | — | second approver | first approver | gates |
| Exception grant (ER, foreign, benefit flag, new org) | — | — | above $1m [A] | above $250k [A] | **A** ≤$250k [A] | gates |
| Discretionary hold on a recipient | sets policy | — | **A** per hold (CTL-045) | GC consulted | — | enforces |
| Sanctions potential true-match clearance | — | — | — | **CRCO / sanctions officer only** (CTL-013) | — | — |
| Complex asset acceptance | above $5m [A] | Gift acceptance above $1m [A] | — | CFO ≤$1m [A] | specialist recommends | — |
| Write-off or adjustment | — | Audit above $250k [A] | — | Controller ≤$25k [A]; CFO above | — | rounding ≤$500 [A] |
| Policy publish (non-loosening) | — | — | — | policy owner plus GC | — | back-test gate |
| Policy loosening (CTL-010) | material ones | Audit and Risk informed | — | Change Board plus CRCO | — | blocked otherwise |
| Agent permission expansion (CTL-026) | — | Audit and Risk informed | — | CRCO plus CTO | — | evaluation gate |
| Vendor selection or termination | material | Audit and Risk | **A** | COO | — | — |
| Filings | — | — | — | officer signs | — | generates |
| Variance power | **A** (or delegated committee) | — | — | GC | — | — |

## 4. Three lines adapted to AI

| Line | Who | AI-specific duties |
|---|---|---|
| **1st: own and operate** | Capability owners (accountable roles in the [accountability matrix](../02-business-capabilities/accountability-matrix.csv)) and **agent owners**: one named person per agent family | Maintain the agent's evaluation set; monitor drift (CTL-027); answer for incidents; propose permission changes |
| **2nd: oversee and challenge** | CRCO function, including a **model-risk lead** (dotted line from the CTO's evaluation lead) | Independent validation before deployment (CTL-026); model inventory; review of policy loosening (CTL-010); sanctions and fraud oversight; obligation coverage (CTL-037) |
| **3rd: independent assurance** | Internal audit, outsourced at small scale, reporting to Audit and Risk | Tests controls using the evidence ledger, including sampling decision records end to end; audits the agent inventory against actual tool grants; audits that no flag was cleared by a model |

## 5. Executive management through continuous evidence

Executives manage from the same operational evidence that runs the enterprise ([telemetry](continuous-improvement-system.md)), not from manually assembled reports. Each executive has a standing view:

| Executive | Standing view |
|---|---|
| CEO | Outcome scorecard O-01 to O-18: cycle times, exception rates, cost per outcome, control health, open H decisions past SLA |
| CFO | Reconciliation status and break aging, NAV checks, liquidity versus forecast, fee revenue, filing calendar |
| CRCO | Alert volumes and closure reasons, sanctions queue, agent flag rates and drift, obligation coverage, SoD conflicts (expect empty) |
| COO | Exception queue by type and age, bottleneck analysis from the digital twin, vendor SLA telemetry |
| CTO | Error budgets, deployment and evaluation results, security posture |

Weekly management reviews are *exception reviews*: what crossed a threshold, and why.

## 6. Board evidence pack

The pack is generated from the evidence ledger, frozen as an approved snapshot (hash recorded in the minutes), with drill-down to underlying records. Contents:

1. **Outcome scorecard,** with trends and the measured-versus-modeled label.
2. **Control health:** % of controls operating with evidence; failed tests; overdue remediations.
3. **Delegation use:** decisions made at each level; any near-threshold clustering, a gaming signal.
4. **Policy changes since last meeting,** with back-test diffs; loosening changes highlighted.
5. **AI oversight:**
   - agent inventory (agent, version, model, tool scope, owner);
   - permission changes;
   - evaluation results versus thresholds;
   - incidents and kill-switch use;
   - flags raised and closed by humans with outcome;
   - an **assertion that no flag was cleared by a model** (query result).
6. **Financial:** statements, reconciliation, liquidity, fees.
7. **Risk:** incidents, vendor concentration, open regulatory items, discretionary holds in force (CTL-045).
8. **Philanthropic outcomes:** payout distribution across accounts (not just aggregate), dormant capital, recipient-side metrics, with evidence-grade labels.

## 7. Concentration-of-authority analysis

| Concentration | Why it arises in an AI-native design | Mitigation |
|---|---|---|
| **Policy engineer or GC** shaping the deterministic rules that decide most grants | One rule change affects every grant | CTL-009 (back-test plus independent test plus approval); SoD-2; board sees loosening changes |
| **CTO / platform team** controls the code that enforces every control | Code is the control | Separation of deploy from parameter changes (SoD-5); independent evaluation (2nd line); internal audit of deploy logs; reproducible builds |
| **Sanctions officer** as the sole clearer | Legal and risk requirement | Named deputy; SLA; escalation to GC; all clearances sampled by internal audit |
| **CEO** for discretionary holds | Reputational holds are judgments | Board-approved hold policy; monthly review; holds visible to the board (CTL-045) |
| **Outsourced CIO** | Fiduciary expertise is concentrated | Committee approval of parameters; manager due diligence on file; periodic market test |
| **Single agent family** used across many decisions (for example a resolution agent) | Correlated error | Flag-only design limits harm; diversity in evaluation sets; deterministic fallback |
| **Key vendors** (custodian, bank, rail, IRS data) | Outsourcing | Concentration metrics; exit-readiness (CTL-035); dual rails where economic (see scenarios) |
| **Infrastructure company over the sponsor** (Model C or hybrid) | Commercial dependence | §2 special case |

Unacceptable concentrations, and the scenario evidence behind them, are listed in [`../11-scenarios-and-validation/scenarios.md`](../11-scenarios-and-validation/scenarios.md) §SPOF register.
