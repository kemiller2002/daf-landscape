# Market validation plan

**Status:** plan, 2026-11-20.

**Guardrails:**
- No outreach is made without the owner's approval.
- No contacts are fabricated.
- Public research is not proof of willingness to pay.

This plan follows the [commercial-opportunity agenda](../../commercial-opportunity/2026-11-20-research-agenda.md) and the falsifiers in the [A–D comparison](models-A-B-C-D-comparison.md).

## 1. Interview hypotheses

| ID | Hypothesis | Segment | Supports | Disconfirming answer |
|---|---|---|---|---|
| H1 | Independent sponsors would grant read access to grant queues and ledgers to a third party under a DPA | Independent nationals, mid-size CFs | C | "Our vendor contract does not allow it" or "our vendor will not provide it" (Q-N04) |
| H2 | Sponsors cannot state their exception rate, minutes per exception or reconciliation break rate today | All sponsors | C (the evidence product has value) | Sponsors can produce these measures readily |
| H3 | Sponsor counsel would accept deterministic auto-approval of routine grants with AI limited to flagging | Sponsor GCs and compliance | C, D | Counsel requires human review of every grant |
| H4 | Reconciliation, servicing and payee maintenance cost more than grant review | Sponsor operations and finance | C (scope beyond review) | Grant review is the dominant cost |
| H5 | Wealth platforms want multi-sponsor flexibility rather than one bundled sponsor | Platforms, broker-dealers | D, P9 | They prefer a single bundled sponsor (the SEI pattern) |
| H6 | Advisors will adopt a program that publishes all-in cost and enforces fee caps, if it preserves their AUM relationship | RIAs, advisors | D, DD-010 | Advisors avoid transparency on fees |
| H7 | A partner sponsor-of-record would let an administrator run a new program end to end on an event-sourced ledger | Sponsors with white-label programs | D | Partners require system-of-record ownership or liability transfer |
| H8 | Nonprofits would pay for cross-sponsor DAF grant reconciliation | Mid-size nonprofits' development operations | P7 (nonprofit side) | Nonprofits will not pay; their CRM or Chariot bundles it |
| H9 | Community foundations under the cost gap would outsource administration rather than modernize in-house | Top-100 CFs outside Foundant | D | They stay on suites |
| H10 | Donors value transparency and recipient-side speed more than investment menus | Donors (via surveys run by sponsors) | B, D (philanthropic outcomes) | Donors primarily value investment options or brand |
| H11 | Sponsors would let the provider retain bitemporal eligibility evidence for reuse across clients | Sponsors' compliance teams | P1 differentiation | Data-sharing restrictions prevent pooling |
| H12 | Auditors would rely on a continuous evidence ledger and reduce sample testing | Audit firms serving sponsors | P5 | Auditors require the same procedures regardless |
| H13 | Consolidators (Ren, Foundation Source, TIFIN) would partner with or acquire, rather than block, a policy-as-code layer | Vendor executives | Exit path | They build it themselves or close access |
| H14 | Donor-side AI agents need a sanctioned delegated-authority channel, and sponsors would offer one | Sponsors, agent product companies | DD-017 | Sponsors refuse all agent access |

## 2. Evidence that would falsify each model

| Model | Falsifying evidence (any one is enough to deprioritize) |
|---|---|
| A | A credible measurement showing that the AI enhancements a new sponsor could add produce a cost or experience gap incumbents cannot match within 12 months. *This would rescue A*; absent it, A is not pursued |
| B | A distribution channel offering low-cost donor access to a new independent sponsor; or public consumer-DAF CAC and retention data showing payback (reconsideration criterion for P3). *These would rescue B* |
| C | No data access after 12 months (H1 false); or measured cost pools below price (H2/H4); or counsel rejects deterministic auto-approval (H3 false) |
| D | No partner sponsor accepts an external administrator on a new ledger (H7 false); or a partner demands liability or fund custody |

## 3. Pilots (each gated on owner approval and on legal review)

| Pilot | Scope | Success criteria (proposed thresholds, not market data) | Duration |
|---|---|---|---|
| PL-1, shadow decisioning | Run the policy engine and flag agents in shadow mode on a sponsor's exported historical grants, then on live recommendations | On ≥10,000 grants: **zero false clears** on a sponsor-audited stratified sample (with AI only flagging, no false clear can come from AI); ≥98% agreement on the routine tier; measured exception rate and minutes published to the sponsor (adapted from entrant simulation S3 as corrected by red team wave 2A) | 3–6 months |
| PL-2, reconciliation | Read-only custodian, bank and rail data → continuous three-way reconciliation | Break detection within T+1; ≥95% auto-match on an audited sample; time-to-close reduction measured against the sponsor baseline | 3 months |
| PL-3, nonprofit-side matching | Cross-sponsor DAF grant matching for 3–5 nonprofits | ≥3 paying customers renewing after 6 months (entrant S2 test [S]) | 6 months |
| PL-4, partner program (Stage D) | One new advisor-channel program for a partner sponsor-of-record | ≥500 live funds or ≥$50m; zero unexplained breaks older than T+1 for 90 days; clean auditor walkthrough (entrant S1 MVP test [S]) | 12 months |

## 4. Sequencing

The pilots run in this order:

1. **PL-1 and PL-2.** Cheapest, reversible, and they generate the missing Q-N03 data.
2. **PL-3.** Run in parallel as a low-cost demand test.
3. **PL-4.** Run only after PL-1 or PL-2 succeeds with a sponsor willing to become a partner.

Each step's result updates the scores in [`model-scores.csv`](model-scores.csv), after which [`scoring.py`](scoring.py) is re-run.
