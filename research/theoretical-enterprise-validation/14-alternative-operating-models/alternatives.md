# Alternative operating models

**Status:** comparative judgment [I]. Uses parameters from the [economic model](../15-economics/economic-model.md). The baseline already compares *business models* A–D ([models comparison](../ai-native-daf-enterprise/10-market-and-business-model/models-A-B-C-D-comparison.md)) and *workflow designs* ([design catalog](../ai-native-daf-enterprise/workflow-innovation/03-alternative-designs/)). This document compares **operating mechanisms** for the outcomes where this program found the most fragility, and does not repeat those comparisons.

Scale: ++ / + / 0 / − / −− relative to the baseline AI-native design (column B). The scores are reasoned judgments, not measurements. Each row names the parameter that would flip the ranking.

Criteria abbreviations: FC financial correctness · RD regulatory defensibility · UX · Acc accessibility · Sec security · OR operational resilience · Cx complexity (+ = simpler) · Cost · Sc scalability · Au auditability · Ex explainability · Rv reversibility · IR implementation risk (+ = lower).

## 1. Grant funding: how cash meets an approved grant

| Design | Mechanism | FC | RD | UX | OR | Cx | Cost | Au | Rv | IR | Flips if |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A. Traditional batch | Approve in batches; liquidate at batch points; pay weekly | 0 | 0 | − | + | + | + | 0 | + | + | — |
| B. Baseline: earmark at approval, liquidate, then pay | Units earmarked (WF-05); per-grant liquidation | − (TVC-022) | 0 | + | − | − | 0 | 0 | 0 | − | — |
| C. Currency reservation with haircut (this program's FI-05/10/12) | Reserve currency; haircut by asset class; per-grant liquidation | + | 0 | + | 0 | − | 0 | + | 0 | − | Haircut too small for a drawdown → over-commitment cases |
| **D. Policy cash sleeve per fund** | Each fund keeps cash = max(policy floor, forecast grants for N days). Grants paid from the sleeve. The sleeve is replenished asynchronously by liquidation. | ++ | 0 | ++ | + | + | − (cash drag) | + | + | + | Cash drag cost > value of faster, simpler funding. Donors reject a cash allocation. |
| E. Pool-level liquidity buffer (sponsor fronts cash) | Pool cash pays grants; units redeemed at next strike | + | 0 | ++ | − (outage exhausts buffer, FM-17) | 0 | 0 | − (intra-pool funding must be accounted, TVF-073) | + | 0 | Outage length > buffer days |

**Rev 2:** the architecture and economics reviews dispute this recommendation, and the dispute is **preserved**:
- a sleeve plus currency reservation still needs every reservation state;
- the sleeve depletes in December, exactly when it is needed;
- its drag (~10 bps of AUM) is ~20× custody and is borne by funds;
- sleeve sizing is an Investment Committee decision.

The reviewers prefer **E (pool-level buffer) + C (currency reservation)**. This is now open as OD-13 with no program recommendation.

Rev 1 text, kept for the record: **Recommendation [I]:** D for the routine path, combined with C for amounts above the sleeve. D turns most grants into cash-only transitions: no `FundingShortfall`, no market risk between approval and payment, fewer states. The cost is cash drag. At a 2% cash-vs-pool return gap on a sleeve of 5% of AUM, drag ≈ 10 bps of AUM [A]. That is comparable to the custody and admin fees in the baseline. **Minority view preserved:** D changes every donor's investment allocation and may conflict with advisor-managed mandates (DD-010). Investment-advisor partners may oppose it. E is cheaper but concentrates outage risk.

## 2. Grant review: where human judgment sits

| Design | Mechanism | RD | FC | UX | Cost | Au | Flips if |
|---|---|---|---|---|---|---|---|
| A. Human reviews every grant | Traditional | + (simple story) | 0 | − | −− | 0 | — |
| B. Baseline: D routine + P flags + H exceptions (DD-004) | Policy approves | ? (TVC-003, needs counsel) | 0 | ++ | ++ | + | Counsel rejects delegation reading |
| C. Board-approved recipient catalog + D | Donors choose from pre-reviewed recipients; others go to H | + | 0 | − (choice limited) | + | + | Donor demand for free choice |
| **D. Giving plan (move controls earlier)** | Donor submits an annual or seasonal plan in Q3. The sponsor reviews new recipients ahead of time. December executes pre-cleared items deterministically. | + | + | + (for planners) | + (flattens surge) | + | Share of donors who plan ahead (unmeasured, TVA-030) |
| E. Exception-only, no queue for "missing info" | Requester resolves gaps through self-service | 0 | 0 | 0/− | ++ | 0 | Requester abandonment |

**Recommendation [I]:** B, kept as a hypothesis until OD-01, plus D as a surge-flattening overlay. D reduces December specialist demand without asking donors to accept deferred execution (INN-37, untested). It is not the only lever (review A19): see economics §3.

**Rev 2 red-team warning:** D creates the TVF-153 grooming chain. A recipient pre-cleared in Q3 by an attacker who controls the donor account auto-executes in December. D is acceptable only with REC-7 (re-confirmation at execution for recently added recipients), AUTH-I7 (step-up and cooling-off on credential changes) and a cross-fund recipient-addition flag.

## 3. Contribution finality

| Design | Mechanism | FC | UX | Cost | Flips if |
|---|---|---|---|---|---|
| A. Baseline: units and capacity on bank settlement | Fast | −− (TVC-023) | ++ | 0 | — |
| B. Hold capacity until R10 window (≈60 days) | Safe | ++ | −− | 0 | — |
| **C. Provisional credit limit (CON-1)** | Units issued; capacity up to a per-donor limit; remainder after window | + | + | 0 | Return rate × exposure > tolerance |
| D. Prefer irrevocable rails (wire, in-kind) for large gifts | Policy | + | 0 | − (donor cost) | — |

**Recommendation:** C with D above a size threshold [P].

## 4. Reconciliation

| Design | Mechanism | Notes |
|---|---|---|
| A. Month-end manual | Traditional | Breaks age ~15 days (E4 [X]) |
| B. Baseline continuous with break-triage agent | Detects at 0 days | E4's cost saving rests entirely on an assumed 2 min/day aging penalty (authors' own review). The detection-latency benefit is real; the labour benefit is unproven. |
| **C. Continuous + independent reconciler role (TVCTL-07)** | B plus SoD | Adds ~1 FTE at small scale [A]. Removes TVC-028. |
| D. Provider-attested reconciliation (custodian sends signed position snapshots) | Fewer breaks | Depends on custodian capability (DD-020; GAP-002) |

## 5. Succession and authority

| Design | Mechanism | Notes |
|---|---|---|
| A. Paper notice, manual role toggle | Traditional | Incorrect-rights risk (admin experiment D) |
| B. Baseline event-triggered, evidence-verified | WF-13 | Needs AUTH-I1..I4 |
| C. Pre-verified succession (donor re-confirms successors yearly; successor identity verified in advance) | Moves the control earlier | Shortens activation; the death event still needs evidence. Low cost; strong UX for bereaved users (P4/P7). |

## 6. Service

| Design | Notes |
|---|---|
| A. Contact centre | Status calls dominate (legacy [I]) |
| B. Baseline: grounded AI service + humans | Accuracy depends on the status vocabulary (TVC-008). A grounded answer is only as clear as the states it reads. |
| **C. Proactive status (no contact needed)** | The five-dimension status with push at each change removes "where is my grant" contacts. It needs the [status vocabulary](../09-ux/status-vocabulary.md) first. Contact volume baseline is unmeasured (GAP-006). |

## 7. Enterprise shape

| Design | Mechanism | Main risk |
|---|---|---|
| A. Traditional sponsor | Departments | Cost |
| B. Baseline AI-native single sponsor | Outcomes + one queue | SoD concentration (TVC-028); surge (TVC-017) |
| C. Infrastructure for many sponsors (Model C/D) | Shared platform | Correlated error across sponsors (INN-36, FM-03); liability allocation (adversarial objection 5); TVR-CMP-003 controls conditioned on model |
| D. "Thin sponsor": sponsor keeps only judgment, governance and legal control; contracts every deterministic function to providers with attested controls (SOC 1/2) | Smallest headcount; inherits providers' controls | Vendor concentration; evidence dependence on vendors' reports, which none of the 13 vendors studied publishes (GAP-025) |

**Unresolved disagreement (preserved):** the baseline recommends starting as C and staging toward D (executive report R1, Low-Medium confidence). This program found that C's main extra risk is *correlated* error, which neither the cost model nor the experiments quantify (TVF-062). Until a blast-radius analysis exists, the C-first recommendation rests on economics that exclude the risk most specific to C.

## 8. What would make the preferred designs wrong

| Preferred | Wrong if |
|---|---|
| Cash sleeve (1D) | Donors or advisors reject a mandatory cash allocation; cash drag at scale exceeds the operational savings |
| Giving plan (2D) | Few donors plan ahead, so surge is not flattened |
| Provisional credit (3C) | Return or fraud rate on contributions is high in the target segment |
| Independent reconciler (4C) | At very small scale the extra role costs more than an outsourced monthly review |
| Proactive status (6C) | Notifications create anxiety or contacts instead of reducing them (unmeasured) |
