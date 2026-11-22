# Workflow catalog

**Status:** theoretical [T].

## 1. Inventory and gaps

Baseline workflows:
- WF-01..WF-24 ([workflows.csv](../ai-native-daf-enterprise/03-workflow-redesign/workflows.csv));
- OPS-01..OPS-10 ([administration/03](../../docs/administration/03-operations-integrations-data-and-ai-v0.1.md));
- XW cross-enterprise workflows ([workflow-innovation/04](../ai-native-daf-enterprise/workflow-innovation/04-cross-enterprise-workflows/)).

| Ref | Workflow | Baseline | Spec completeness (of the 18 directive fields) | Critical? |
|---|---|---|---|---|
| CW-01 | Grant lifecycle, routine domestic | WF-01, OPS-03 | ~11/18: missing funding, recovery, termination, unknown-state, financial effects per step | **Yes** (§2.1) |
| CW-02 | Grant, % or multi-source funded | SPEND-03, W02, D-GR-02 | ~6/18; fixing rule absent | **Yes** (§2.2) |
| CW-03 | Recurring grant instance | WF-05 | ~8/18 | **Yes** (§2.3) |
| CW-04 | Foreign / ER / fiscal-sponsor grant | WF-06/07/08 | ~12/18 | Yes (baseline adequate for theory; ER control gap TVF-044) |
| CW-05 | Eligibility change mid-flight | WF-09, OPS-09 | ~14/18 | Yes |
| CW-06 | Payment return / payee change | WF-10 | ~13/18; post-settlement return missing | **Yes** (§2.4) |
| CW-07 | Cash contribution | WF-01 leg, OPS-02 | ~10/18; finality missing | **Yes** (§2.5) |
| CW-08 | Securities / complex / crypto contribution | WF-02/03/04 | ~12/18 | Yes |
| CW-09 | Fund establishment → activation | EST-01..14; lifecycle table | ~10/18; **no WF counterpart** | **Yes** (§2.6) |
| CW-10 | Advisor onboarding / delegation | WF-12, AUTH | ~12/18 | Yes |
| CW-11 | Death / incapacity / succession | WF-13, SUCC, OPS-06 | ~11/18; pending-grant rule absent | **Yes** (§2.7) |
| CW-12 | Transfer out to another sponsor | WF-14 | ~11/18 | Yes |
| CW-13 | Inactive fund | WF-15 | ~10/18 | No |
| CW-14 | Liquidity management | WF-17 | ~11/18 | Yes |
| CW-15 | NAV, unitization, fees | WF-18, FEE | ~12/18; restatement absent | **Yes** (§2.8) |
| CW-16 | Reconciliation / break resolution | WF-19 | ~12/18 | Yes |
| CW-17 | Close, statements, 990/Schedule D | WF-20 | ~9/18 | Yes |
| CW-18 | Policy change → deployment | WF-22, OPS-08 | ~13/18 | Yes |
| CW-19 | Agent permission change | WF-23 | ~13/18 | Yes |
| CW-20 | Partner widget transaction | W02 | ~14/18 | Yes ([widget model](../10-widgets/widget-integration-model.md)) |
| **CW-21** | **Fund closure** (incl. residual sweep, trailing receipts) | Lifecycle table; Experiment E | ~5/18; **no WF** | **Yes** (§2.9) |
| **CW-22** | **Fund merge / split** | Complex lifecycle cases | ~3/18; **no WF** | Yes |
| **CW-23** | **Fund suspension / freeze** (legal order, sanctions) | Lifecycle table | ~4/18; **no WF** | Yes |
| **CW-24** | **Grant cancellation and recall** | `GrantCanceled` event only | ~2/18 | **Yes** (in §2.1) |
| **CW-25** | **Recipient refund / recovery of paid grant** | WF-09 step 4 mentions recovery | ~2/18 | Yes |
| **CW-26** | **Custodian historical correction / NAV error** | — | 0/18 | **Yes** (§2.8) |
| **CW-27** | **Contribution reversal (returned debit, failed delivery)** | — | 0/18 | **Yes** (§2.5) |
| **CW-28** | **Acknowledgment correction** | ADM scenario 15 | ~2/18 | Yes |
| **CW-29** | **Uncashed check → void → reissue / escheat** | CTL-044, `CheckAged` | ~4/18 | Yes |
| **CW-30** | **Authority dispute** | AUTH-09, SUCC-07 | ~4/18 | Yes |
| **CW-31** | **Partner onboarding / offboarding** | widgets/04 lifecycle | ~7/18 | Yes |
| **CW-32** | **Incident response and kill switch** | CTL-028, `KillSwitchActivated` | ~6/18 | Yes |
| **CW-33** | **Regulatory inquiry / legal hold** | SC-13 | ~6/18 | Yes |
| **CW-34** | **Donor complaint and appeal of grant decline** | SVC-07, SC-15 | ~5/18 | No |
| **CW-35** | **Privacy request (access/deletion) against retention and holds** | SVC-04, DATA-06 | ~3/18 | Yes (conflict with R-TAX/R-OFAC) |
| **CW-36** | **Migration cutover** | MIG-01..09, WF-08 design | ~12/18 | Yes |
| **CW-37** | **Fee correction / refund** | FEE-11 | ~5/18 | No |
| **CW-38** | **Board delegation (DoA) change** | GOV-01 | ~3/18 | Yes (TVC-003) |

Bold rows are the 18 workflows the baseline does not define as workflows. **14** of them are below one-third specified (corrected in review; [TVF-020](../16-registers/findings.csv)).

Added after round 2 cross-domain (not yet specified):
- **CW-39** transfer-in from another sponsor (TVF-121);
- **CW-40** investment-structure transition: custodian conversion, custodian or processor insolvency, pool merger or liquidation (TVF-122);
- **CW-41** inter-fund error correction (TVF-124);
- **CW-42** sponsor succession: sponsor merger, dissolution or revocation (TVF-130);
- **CW-43** migrated-fund validation and in-flight import (TVF-110/111);
- **CW-44** acceptance invalidated after the fact (TVF-113).

## 2. Critical workflow specifications

Field order follows the directive. "Auth" = authorization; "Fin" = financial effects.

### 2.1 CW-01 / CW-24 Grant lifecycle (routine, domestic, fixed amount)

| Field | Specification |
|---|---|
| Trigger | `RecommendationSubmitted` (portal, widget, API, agent, staff on behalf with evidence) |
| Preconditions | Fund `Active`, not `Frozen`; requester relationship effective; capability `recommend_grant`; session assurance ≥ required (TVC-025); no fund-level hold for the requester |
| Participants | Requester; sponsor rules; specialist (if referred); payment gate; provider; reconciler |
| Authoritative data | Authorization service; registry eligibility facts (versioned); sanctions list (pinned); policy version; ledger capacity |
| Inputs | Fund, recipient candidate, amount, currency, purpose, anonymity, allocation preference, idempotency key, preview hash |
| Decisions | Recipient resolution (D; ambiguity → H); eligibility (D); screening (D; potential match → H); benefit risk (P flag); routing (D); approval (D or H); capacity (D); release (D gate + DoA) |
| Business rules | DD-003, DD-004 (hypothesis, TVC-003), FI-05..09, GR-1..8, PA-1..4, REC-1..4 |
| State transitions | [Recommendation §1](../06-state-models/state-models.md#1-grant-recommendation-donoradvisor-side) → [Grant §2](../06-state-models/state-models.md#2-grant-sponsor-side) → [Attempt §3](../06-state-models/state-models.md#3-payment-attempt) |
| Outputs | Decision record; grant; reservation; payment attempt; remittance; journal entries; donor and recipient notices |
| Events | Baseline events **plus** `GrantReserved`, `GrantFundingOrdered`, `GrantFunded`, `GrantFundingShortfall`, `PaymentSubmitted`, `PaymentStatusUnknown`, `PaymentAccepted`, `PaymentFinal`, `GrantCancellationRequested` (TVR-EVT-001) |
| Fin | Reservation (encumbrance) → liquidation (units → cash) → funding allocation → disbursement (cash out) → finality. Each is a distinct ledger fact ([§1 of invariants](../07-financial-invariants/financial-invariants.md#1-twelve-distinct-financial-facts)) |
| Auth | Requester capability at submit **and** at decision; DoA for approver; release authority ≠ profile approver; re-check at payment submission (SM-6) |
| Audit | Inputs snapshot hash; policy version; list versions; actor kinds; evidence links; provider references |
| External deps | IRS data (freshness SLO); OFAC list; custodian (liquidation); bank/rail provider |
| Success | `Reconciled` after `Final` |
| Failure | Declined; Canceled; FundingShortfall unresolved; Returned unresolved; Unknown unresolved > SLA |
| Recovery | Unknown → query → (observe or human decision PA-2); Returned → re-pay or cancel; post-payment review → recovery case (CW-25) |
| Termination | Declined, Canceled, Reconciled (SM-0: later corrections are child records) |
| User-visible | Separate request / decision / funding / payment / finality statuses ([status vocabulary](../09-ux/status-vocabulary.md)); never "paid" before Disbursed; never "failed" for Unknown |

**Cancellation (CW-24).** Baseline WF-01 lets the *donor* cancel an approved grant before release (`Approved → Canceled`); review correction to TVF-005. Proposed: requester asks → if `UnderReview`, it is a withdrawal (REC-2). If `Approved`..`Funded`, the sponsor decides (normally grants it; [P]). If an attempt is in `Submitted/Unknown/Accepted`, cancellation becomes a recall request (GR-3), and the donor sees "cancellation requested – payment may already be on its way".

### 2.2 CW-02 Percentage or multi-source grant

Differences from CW-01 only:

| Field | Specification |
|---|---|
| Inputs | Mode (FixedMoney / Percent); denominator type from the enumerated set (FI-16); allocation lines |
| Decisions | Fixing (D) at the fixing event (FI-10; OD-07); source permission per line (D); re-plan on shortfall (D within policy, else H) |
| Rules | FI-10..16 |
| Fin | Fixing creates the currency amount; lines split by largest remainder; per-line liquidation; excess or shortfall from unit redemption at forward NAV returned to or drawn from the fund (FI-14) |
| Failure | One line's source unavailable → `FundingShortfall` (FI-13) |
| User-visible | Preview: "about $X (estimate as of T, based on [denominator])". After approval: "fixed at $Y on D". Donor never sees the amount silently change after approval. |

### 2.3 CW-03 Recurring grant instance

| Field | Specification |
|---|---|
| Trigger | `ScheduledGrantDue` from a standing recommendation template |
| Preconditions | Template active; **authority of the template's author still effective** (TVC-033); fund not held |
| Decisions | Full CW-01 decision set per instance (no decision reuse for authority, eligibility, sanctions); capacity per instance (FI-09) |
| Failure | Capacity short → instance held, donor notified, series continues; authority lapsed → series suspended |
| Termination | Template end date; withdrawal; authority end; recipient ineligible (series suspended, not just instance) |
| Collision | Same-day extraordinary grant: order by reservation time (FI-08); no priority for recurring unless policy says so [P] |

### 2.4 CW-06 Payment return (including after settlement)

| Field | Specification |
|---|---|
| Trigger | `PaymentReturned` (any time after `Accepted`, including after `Final` where the rail allows) |
| Decisions | Return code class (D); profile invalidation (D); re-pay vs cancel (D within policy; H after N days) |
| Fin | FI-19: fund re-credited **in cash**; reservation re-established; reinvestment at next cycle |
| Failure | Return arrives for a grant already `Reconciled` → reopen as a child `ReturnCase` (SM-0), reconciliation break opened |
| User-visible | Donor: "Returned by the recipient's bank – we are updating payment details". Charity: request to re-enroll through verified channel only |

### 2.5 CW-07 / CW-27 Cash contribution and reversal

| Field | Specification |
|---|---|
| Trigger | Intent; bank/custodian observation |
| States | Observed → Provisional (reversible rail) → Final ([§5](../06-state-models/state-models.md#5-contribution)) |
| Rules | CON-1..3; FI-22..23 |
| Fin | Units issued at Provisional (proposal) so investment exposure starts. Capacity excludes provisional value beyond the credit limit. |
| Reversal | Units cancelled. If redeemed already: donor receivable + sponsor exposure + case. Acknowledgment correction (CW-28) [C]. |
| Auth | Donor identity verified for debit authorization; Nacha fraud monitoring (REG-044, [S]) |
| User-visible | "Received – available for grants on D" (not "available now") |

### 2.6 CW-09 Fund establishment → activation

| Field | Specification |
|---|---|
| Trigger | Application (donor, advisor, partner, staff) |
| Preconditions | Product exists for the legal entity and jurisdiction; agreement template effective |
| Decisions | Identity and screening (D + H on match); duplicate/conflict (D flag → H); product eligibility (D; legal classification of non-standard products is H [C], EST-03); sponsor acceptance (H or delegated D [P]); activation gate (D: EST-11) |
| States | Prospect → Application → UnderReview → Approved → Active-Unfunded → Active (funded) |
| Fin | Book set-up; no capacity until first Final contribution |
| Failure | Expired application; rejection; approved-not-funded beyond TTL |
| Concurrency | Signature during an agreement revision → executed version pinned; re-sign if materially different (admin test "agreement revised while signing") |
| User-visible | "Agreement signed – sponsor review pending" ≠ "Fund active" |

### 2.7 CW-11 Death of the sole advisor

| Field | Specification |
|---|---|
| Trigger | Notice of death (any channel), or a data signal (e.g. a death-index match), which is a flag only |
| Immediate (D) | Fund `AuthorityState = Interim`; recommendations from the deceased held; recurring templates suspended; sessions and agent privileges of the deceased revoked; partner notified to revoke launch grants |
| Decisions | Evidence verification (H); effective date of death (H; bitemporal); actions taken between death and notice reviewed (AUTH-I3); approved-not-paid grants: complete per GR-8 [P][C]; successor activation (H, AUTH-07) |
| Failure | No valid successor → SUCC-06 sponsor disposition; disputed succession → CW-30 |
| Privacy | Medical and estate documents in a restricted evidence class |
| User-visible | Successor sees no fund data until `Active`; estate representatives see only what the instrument permits |

### 2.8 CW-15 / CW-26 NAV strike, fees and custodian correction

| Field | Specification |
|---|---|
| Trigger | Daily strike; `PositionChanged` with past effective date (correction) |
| Decisions | Invariant check FI-02 (D blocks publication); NAV error materiality (D threshold [P]); restate vs adjust (H, Controller + independent reviewer) |
| Fin | FI-27, FI-28 |
| External | Custodian; pricing vendor |
| Failure | Correction after period close → current-period adjustment with effective date; prior statements flagged "corrected" if restated |
| User-visible | Statements show a correction notice; donors whose units were redeemed at a wrong NAV get an explanation if the policy compensates |

### 2.9 CW-21 Fund closure

| Field | Specification |
|---|---|
| Trigger | Donor request; sponsor policy (inactivity, no valid advisor); transfer out completion |
| Preconditions | FUND-1 |
| Decisions | Residual disposition (per agreement or sponsor policy, SUCC-06); final residual sweep grant (FI-15) |
| Fin | Final fees through closure date; all reservations consumed or released; residual swept |
| Recovery | Trailing receipts → `ClosedWithResidualRecovery` destination (FI-35; OD-11) |
| Termination | `Closed`; records retained (AG-08) |
| User-visible | Closure statement with final reconciliation |
