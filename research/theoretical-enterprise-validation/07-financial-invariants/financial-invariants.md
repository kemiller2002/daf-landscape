# Financial invariants catalog

**Status:** theoretical [T]. Accounting treatment marked [C] needs review by a CPA familiar with nonprofit (ASC 958) fund accounting. Nothing here is an accounting conclusion.

Baseline: [financial core v0.5](../../docs/financial-core-control-spec-v0.5.md) invariants 1–10, settlement conservation, SPEND-01..06, FEE-01..12, WF-17/WF-18 ([treasury](../ai-native-daf-enterprise/03-workflow-redesign/wf-investments-treasury.md)), and the grant machine in WF-01. This catalog keeps those rules and adds what is missing. Each invariant states what must hold, when it is checked, and what happens on violation.

## 1. Twelve distinct financial facts

The baseline vocabulary is close to this, but no single document separates all twelve. Several documents collapse adjacent facts ([TVF-007](../16-registers/findings.csv)).

| # | Fact | Created by | Moves money? | Legal effect | Reversible? |
|---|---|---|---|---|---|
| 1 | Recommendation | Donor, advisor, agent principal | No | None: a request (DD-003, §4966(d)(2) [V via REG-001]) | Withdraw before decision |
| 2 | Authorization (approval) | Sponsor rule or human | No | Sponsor commits to a grant | Cancel before payment (sponsor) |
| 3 | Fixing | Approval, or a defined later event for % grants | No | Converts a % into a currency amount | No; correct by new grant or cancel |
| 4 | Reservation | Ledger, atomically with or after approval | No (encumbrance) | None externally | Release on cancel |
| 5 | Liquidation order | Treasury rule | Yes (internal: units → cash) | Trade instruction to custodian | Until executed |
| 6 | Liquidation settlement | Custodian observation | Yes | Cash available to the legal owner | No (a new trade reverses) |
| 7 | Funding | Ledger | Internal allocation of settled cash to a grant | None externally | Until payment submitted |
| 8 | Payment instruction | Payment gate | Not yet | Sponsor order | Until submitted |
| 9 | Provider acceptance | Provider | Yes (committed) | Provider obligation | Recall only, uncertain |
| 10 | Settlement | Provider observation | Yes | Funds at recipient's bank | Return or recovery only |
| 11 | Finality | Time after settlement per rail | — | Return risk ended (mostly) | Recovery only |
| 12 | Reconciliation | Matching of ledger, custodian, bank | No | Evidence | Break reopened by later facts |

## 2. Invariants

### 2.1 Conservation and ledger

| ID | Invariant | Checked | On violation |
|---|---|---|---|
| FI-01 | Every journal balances in each currency. No posting into a closed period through any write path. Corrections are reversals or adjustments. | Every posting | Reject (baseline invariant 3) |
| FI-02 | Σ account units × NAV = pool NAV within tolerance; Σ pool positions = custodian positions after known in-transit items. | Each NAV strike; daily | Block NAV publication (WF-18; CTL-017) |
| FI-03 | Legal-owner cash (sponsor entity) = Σ fund cash claims + sponsor operating cash + suspense, per custodial and bank account. | Daily | Break case; no new reservations against the affected account until classified |
| FI-04 | Suspense and unapplied cash have an owner and an age. Nothing ages out of suspense into a fund or into revenue without a human decision. | Daily | Escalate by age |

### 2.2 Capacity and reservation

Definitions per fund *f* at time *t*:
- `V(f,t)` = Σ units × latest struck NAV, plus fund cash, less accrued unpaid fees.
- `R(f,t)` = Σ active reservations (currency).
- `H(f,t)` = valuation haircut = Σ over sources of value × haircut rate for that asset class [P, sponsor policy; OD-05].
- `P(f,t)` = provisional contribution value (reversible rails) not covered by the provisional credit limit.
- **Reservable capacity** `C(f,t) = V − R − H − P − policy minimum balance`.

| ID | Invariant | Checked | On violation |
|---|---|---|---|
| FI-05 | A reservation of amount *a* is created only if *a* ≤ `C(x,t)` for the fund **and every constrained ancestor x** (pool cash buffer if paying ahead of liquidation, custodial account, legal entity, restricted sub-balance). Check and creation are one serialized operation per ancestor, with locks taken in a fixed order. | Reservation | Reject; grant stays `Approved` and held "insufficient capacity" (or approval and reservation are atomic, so approval fails) |
| FI-06 | Displayed "available to recommend" = `C(f,t)` minus soft pending claims, labelled as an estimate with its as-of time. It is never shown as cash. | Each render | Content rule |
| FI-07 | A reservation is released only by cancellation, decline or consumption at settlement. Never by timeout, Unknown, a projection rebuild, or a UI action. | Each release | Reject release |
| FI-08 | Two recommendations, from one or many advisors, cannot both be approved if together they exceed `C` at the moment of the later reservation. Approval order is the serialization order of reservations, not the submission order. | Reservation | The later one fails capacity; the requester is told it was approved-pending-capacity or declined, per OD-06 |
| FI-09 | Recurring grants reserve **per instance**, at the instance's due date, never for the series. | Each instance | Instance held |

### 2.3 Fixed and percentage grants across several investments

The baseline requires a defined denominator and as-of time (SPEND-03, W02, D-GR-02). It leaves DEC-UI-08 pending. It does not say **when** a percentage becomes money, or what happens to the plan when values move ([TVF-008](../16-registers/findings.csv)).

| ID | Invariant |
|---|---|
| FI-10 | **Single fixing.** A percentage grant is converted to a currency amount exactly once, at a defined fixing event, with a recorded valuation snapshot ID. Proposed default: fix at approval, using the latest struck NAV [P; OD-07]. The donor-visible preview is an *estimate at preview time*. After fixing, the grant is an ordinary fixed-amount grant. |
| FI-11 | **Allocation is a funding plan, not a set of grants.** Lines `{source_i, share_i}` say where the cash comes from. The sponsor controls investments (DD-007), so a donor allocation is itself a recommendation. Line amounts = fixed amount × share, rounded to minor units by largest remainder with deterministic tie-break on source ID. Σ line amounts = grant amount exactly. |
| FI-12 | **Over-commitment.** If market moves make `R(f,t) > V(f,t) − H`, the fund is over-committed. New reservations are refused. Already-approved grants keep their fixed amounts. Unfunded grants are funded in approval order. Any remaining shortfall is a sponsor decision case (cancel newest, top-up policy, or partial) [P; OD-08]. The fund never goes negative silently. |
| FI-13 | **Source shortfall.** If one source cannot deliver its line (illiquid, restricted, gated, custodian outage), the grant enters `FundingShortfall`. Policy decides: re-plan to other permitted sources (allowed when the donor's allocation was a preference) or hold. No partial payment unless sponsor policy explicitly allows split disbursement [P]. |
| FI-14 | **Liquidation sizing.** Units redeemed per source = line amount ÷ forward NAV at strike. Because forward NAV is unknown at order time, the order must either sell by amount (cash-amount redemption) or sell units with a buffer and return the excess to the fund. The choice is a treasury policy [P]. Either way, the realised proceeds and the excess or shortfall are recorded, and the grant receives exactly its fixed amount. |
| FI-15 | **"100% of fund" or closing grant** is a distinct type: a *residual sweep*. Its amount is not known until all fees through closing date, all other obligations and all liquidations have settled. It is fixed after the last settlement, not at approval. A 100% grant fixed at approval is guaranteed to be wrong in one direction or the other. |
| FI-16 | **Percentage of what.** Allowed denominators are an enumerated set, each with a definition: fund `V`, reservable capacity `C`, a named portfolio's value, or a sponsor spendable base (endowed funds). "Percent of account" without a type is invalid. |

### 2.4 Settlement, payment and return

| ID | Invariant |
|---|---|
| FI-17 | Settlement conservation (baseline): on confirmed settlement of *X*, in one transaction, record unique external evidence, reduce confirmed cash by *X*, reduce the matching reservation by *X*, post the journal, write the outbox. Failure leaves the prior state plus an exception. |
| FI-18 | Double-payment invariant PA-1 ([state models §3](../06-state-models/state-models.md#3-payment-attempt)). |
| FI-19 | A return after settlement **re-credits the fund in cash** (the units were already redeemed). Reinvestment of returned cash follows the fund's allocation policy at the next cycle. The grant goes to `Returned` and its new reservation is re-established from that cash, not from new units. |
| FI-20 | A recipient refund (charity sends money back, for example a canceled event or excess benefit discovered) is **not** a return. It is a new inbound receipt linked to the grant. Whether it goes back to the fund or elsewhere, and whether it reverses the grant for Schedule D, are [C] questions (OD-09). |
| FI-21 | Uncashed checks: issued-not-presented amounts stay as a liability, not as fund cash. Void → re-credit or reissue per policy. Dormancy → unclaimed-property process [C: REG-045 is UNVERIFIED]. |

### 2.5 Contributions

| ID | Invariant |
|---|---|
| FI-22 | Contribution value on a reversible rail is `Provisional` until the reversal window passes. Provisional value counts toward `V` for display and fees but is excluded from `C` except up to the provisional credit limit (CON-1). |
| FI-23 | A reversed contribution produces a reversal entry dated when the reversal is recorded, with effective date = original. Units issued against it are cancelled. If the units no longer exist (already redeemed for a disbursed grant), the shortfall becomes a donor receivable and sponsor exposure, never a silent negative balance (CON-3). |
| FI-24 | Non-cash gift value: acceptance value, custody receipt value, gift-date valuation for acknowledgment, and sale proceeds are four different numbers. Only sale proceeds fund grants. |

### 2.6 Fees

| ID | Invariant |
|---|---|
| FI-25 | Fee accrual reduces `V` and `C` when accrued, not when collected. Otherwise a fund can reserve its whole balance and leave nothing for the fee. |
| FI-26 | If accrued fees exceed `V − R` (an over-committed fund), the order of priority between the fee and approved grants is a sponsor policy decision [P; OD-10]. It must be decided before it occurs, not during an incident. |
| FI-27 | Fees computed on a stale or later-restated NAV are recalculated by an adjustment entry in the current period, with an effective date. The fee basis records the NAV version used (FEE-03, FEE-11). |

### 2.7 Corrections and external disagreement

| ID | Invariant |
|---|---|
| FI-28 | **Custodian historical correction.** A correction to positions or cash effective in a past period is recorded bitemporally. If it changes a struck NAV beyond the materiality tolerance, a NAV-error case decides between restatement (re-processing unit transactions at the corrected NAV) and current-period adjustment [P/C; industry practice for pooled vehicles is a materiality threshold, I]. Fund-level effects on already-redeemed units are computed and shown, not ignored. |
| FI-29 | When the ledger, custodian and bank disagree, no source wins by default. Each field has a declared authoritative source (DATA-07). A disagreement creates a break that blocks new reservations on the affected resource when its amount exceeds a threshold [P]. |
| FI-30 | An external balance feed is an observation. It never makes cash spendable on its own (baseline). |

### 2.8 Multi-currency and restricted assets

| ID | Invariant |
|---|---|
| FI-31 | A foreign-currency grant is fixed in exactly one currency. If fixed in USD, the recipient bears FX at payment. If fixed in the foreign currency, the fund bears FX and the reservation includes an FX buffer. The choice is recorded per grant [P]. No implicit conversion (baseline nonfunctional rule). |
| FI-32 | Restricted balances (sponsor policy, agreement, donor intent accepted by sponsor) are separate capacity constraints. A grant line drawing on a restricted balance must satisfy the restriction at approval and again at funding. |

### 2.9 Closure, merge, split and transfer

| ID | Invariant |
|---|---|
| FI-33 | Merge or split conserves value: Σ outputs = input at one valuation point, by source and restriction. Pending reservations move with an explicit rule. |
| FI-34 | Transfer-out to another sponsor is a grant (the receiving sponsor is a public charity), subject to every grant invariant. Plus: provisional contributions and unresolved payment attempts block it. |
| FI-35 | After closure, trailing receipts (dividends, class actions, late returns) go to a defined destination per sponsor policy [P; OD-11]. They never re-open the fund as `Active`. |

## 3. Concurrency checks (theoretical)

| Overlap | Invariant that decides | Permitted outcome | Prohibited outcome |
|---|---|---|---|
| Two advisors recommend against the same balance | FI-05, FI-08 | One reserves; the other fails capacity or waits, with a truthful status | Both approved and both paid from one balance |
| Valuation drops after a % recommendation | FI-10 | Preview estimate differs from fixed amount; donor sees both | Grant amount silently moves after approval |
| Valuation drops after approval, before liquidation | FI-12, FI-14 | Grant paid at its fixed amount; fund absorbs loss; over-commitment case if needed | Recipient paid less than approved; fund silently negative |
| Recurring grant and an extraordinary grant on the same day | FI-09, FI-05 | Order by reservation time; the loser is held | Series pre-reserves the whole year |
| Cancel and payment release race | GR-3 | One wins by revision; if payment submitted, cancel becomes recall request | Both "canceled" and "paid" |
| Provider accepts but does not acknowledge | FI-18, PA-2 | Unknown; query; no retry | New attempt with a new key |
| Custodian corrects a past position | FI-28 | Bitemporal correction; NAV-error case | Silent overwrite of history |
| ACH contribution returns after it funded a grant | FI-23 | Donor receivable, sponsor exposure, case | Negative fund balance with no owner |

## 4. What the baseline does not let us decide (owner decisions)

OD-04 provisional credit limit; OD-05 haircut rates; OD-06 approval vs reservation atomicity; OD-07 fixing time; OD-08 over-commitment priority; OD-09 recipient refund destination; OD-10 fees vs grants priority; OD-11 trailing receipts. See [owner decisions](../16-registers/owner-decisions.md).
