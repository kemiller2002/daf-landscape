# Status vocabulary (proposal resolving TVC-008)

**Status:** proposal [T]. Copy is illustrative; legal and plain-language review are required (the UX v0.2 content-governance rule). Read with [revision 3 amendments](../06-state-models/revision-3-amendments.md), which supersede conflicting text.

## 1. Principle

A grant has **five independent dimensions**. The baseline already says this in two places: D07 "approval, funding, payment as separate states" and vertical slices "independent recommendation/approval/funding/payment states". But the design-system label list collapses them into one linear sequence. A single label cannot show "approved, held for eligibility, funding complete", or "paid, return received". Proposal: show one **headline** derived from the dimensions, plus the dimensions themselves on demand.

| Dimension | Values (internal) | Donor/advisor label | Must never be called |
|---|---|---|---|
| Request | Draft, AwaitingConfirmation, Submitted, Withdrawn, Superseded, Expired | Draft · Waiting for your confirmation · Recommendation submitted · Withdrawn · Replaced · Expired | "Accepted", "Approved" |
| Decision | UnderReview, AwaitingHumanDecision, Approved, Declined, Canceled | In sponsor review · Additional review · Approved by [Sponsor] · Not approved · Canceled | "Pending" alone (ambiguous) |
| Funding | NotStarted, Reserved, Funding, Funded, FundingShortfall | — (hidden unless delayed) · Funds set aside · Selling investments to fund grant · Ready to pay · Funding delayed | "Paid", "Processing" |
| Payment | None, Prepared, Submitted, Unknown, Accepted, Settled, Final, Returned, StopRequested, Voided | — · Payment being prepared · Payment in progress · **Confirming payment status** · Payment in progress · Payment sent on D · Paid to [Recipient] on D · Returned – arranging payment again · Stop requested · Check voided | "Failed" for Unknown; "Paid" or "Complete" before Final (GR-5) |
| Finality / reconciliation | Final, Reconciled, PostPaymentReview | (not shown; "Paid" remains) · — · Under post-payment review (staff only unless policy discloses) | — |
| Hold (orthogonal) | Held(reason class) | On hold – [non-sensitive reason class]: eligibility review · verification · sponsor review | Specific sanctions or fraud reasons (UX-F19) |

## 2. Headline derivation (priority order, rev 2)

Revision 2 follows the UX review (A1–A4) and round 2 (G-24, G-25). Revision 1 let a hold hide money already in flight, showed canceled grants as "Returned" forever, and reused receipt copy for payment Unknown.

1. Grant `Declined`, `Withdrawn` or `Canceled` → that label. Terminal decisions outrank every payment label.
2. Payment `Unknown` → "Confirming payment status". Body: "Your grant may already be on its way. **Please do not send a new recommendation for this grant**; we will update you." **Not** the W02 receipt copy ("check its status before trying again"), which applies only to an unconfirmed *recommendation submission*. While a payment is Unknown, a new recommendation to the same recipient from the same fund routes to a human.
3. Payment in flight (`Submitted`/`Accepted`) → "Payment in progress". If a hold was added after submission, add "– under review", but never replace the in-flight fact.
4. Payment settled, before `Final` → "Payment sent on [date]". After `Final` → "Paid to [Recipient] on [date]" (GR-5).
5. Payment `Returned` (grant not canceled) → "Returned – we are arranging payment again".
6. Hold present (no attempt in flight) → "On hold – [reason class]".
7. Funding `FundingShortfall` → "Funding delayed". `ApprovedAwaitingCapacity` → "Approved – waiting for funds".
8. Decision `Approved` → "Approved by [Sponsor]".
9. Request state otherwise.

**Charity-facing copy (UX review A14):** returns must never say "updating payment details" to a charity, because that primes a bank-detail phishing request. Say: "A payment was returned. To update your details, sign in at [sponsor domain]. We will never ask for bank details by email or phone."

**Notification volume (UX review A6):** professional advisors (P5) receive a digest by default, not a push per status change. Push is reserved for items needing action: confirmation requests, holds needing information, Unknown resolved.

## 3. Mapping of baseline vocabularies

| Baseline term (source) | Maps to |
|---|---|
| Received (core command) | Internal only: command receipt. Not shown. |
| Authorized (core) | Decision = Approved |
| Reserved (core) | Funding = Reserved |
| Submitted (core) | Payment = Submitted |
| Observed (core) | Payment = Accepted or Disbursed, by observation type |
| Settled (core) | Payment = Settled ("Payment sent"); "Paid" only at Final |
| Reconciled (core) | Finality = Reconciled |
| Denied (core) / decline (O03) / Rejected (W02 receipt) | Decision = Declined (sponsor) **or** command rejected (validation). Two different facts: the receipt's "Rejected" means *not recorded*, not *declined* |
| Held (core) / On hold / held | Hold flag |
| Unknown (core) / Status unknown / UnknownExternalOutcome | Payment = Unknown (or command-receipt Unknown, a different object) |
| Failed (core) | Payment attempt Rejected/Failed/NotReceived. Grant returns to Funded. Donor sees "Payment being prepared" again or a delay notice, not "failed" |
| Compensating (core) | Child correction record; not a grant status |
| Accepted (W02 receipt) | Request = Submitted ("Recommendation submitted – reference R-…") |
| "sponsor-accepted recommendation ID" (W02 step 5) | **Wrong.** Replace with "recommendation reference" |
| Processing / Succeeded (widget platform receipt) | Command-level only; Succeeded for a recommendation = Request Submitted (TVC-009) |
| pending / approved / paid / rejected / canceled / returned (open record) | Lossy external projection; "rejected" = Declined |
| Funding in progress (design system) | Funding = Funding |

## 4. Contributions

| Internal | Label |
|---|---|
| Observed | "Received by [custodian/bank] – being matched" |
| Provisional | "Received – available for grants on [date]" |
| Final | "Available" |
| Proposed / Accepted (non-cash) | "Gift under review" / "Gift accepted – awaiting transfer" |
| Valued | "Valued at $X on D (method)" |
| Reversed | "Contribution returned by your bank" |
| Acknowledged | "Acknowledgment issued [date]" |

## 5. Screen-state set (resolves the 12 vs 13 vs 12 drift)

One union set for every surface: Loading, Ready, Empty, Partial, Stale, Offline, ValidationError, Conflict, Unauthorized, Restricted, ReauthRequired, ContextChanged, Held, UnknownExternalOutcome, RecoverableError, FatalError, Success, Maintenance. Each surface declares which apply. A state that cannot occur on a surface is listed as N/A with a reason. Each applicable state has a heading, body, announcement and primary action, which the W01 contract already requires but does not provide for Restricted, ReauthRequired or ContextChanged.
