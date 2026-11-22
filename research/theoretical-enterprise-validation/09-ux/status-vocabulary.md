# Status vocabulary (proposal resolving TVC-008)

**Status:** proposal [T]. Copy is illustrative; legal and plain-language review are required (the UX v0.2 content-governance rule).

## 1. Principle

A grant has **five independent dimensions**. The baseline already says this in two places: D07 "approval, funding, payment as separate states" and vertical slices "independent recommendation/approval/funding/payment states". But the design-system label list collapses them into one linear sequence. A single label cannot show "approved, held for eligibility, funding complete", or "paid, return received". Proposal: show one **headline** derived from the dimensions, plus the dimensions themselves on demand.

| Dimension | Values (internal) | Donor/advisor label | Must never be called |
|---|---|---|---|
| Request | Draft, AwaitingConfirmation, Submitted, Withdrawn, Superseded, Expired | Draft · Waiting for your confirmation · Recommendation submitted · Withdrawn · Replaced · Expired | "Accepted", "Approved" |
| Decision | UnderReview, AwaitingHumanDecision, Approved, Declined, Canceled | In sponsor review · Additional review · Approved by [Sponsor] · Not approved · Canceled | "Pending" alone (ambiguous) |
| Funding | NotStarted, Reserved, Funding, Funded, FundingShortfall | — (hidden unless delayed) · Funds set aside · Selling investments to fund grant · Ready to pay · Funding delayed | "Paid", "Processing" |
| Payment | None, Prepared, Submitted, Unknown, Accepted, Disbursed, Returned, Recalled, Voided | — · Payment being prepared · Payment sent to bank · **Confirming payment status** · Payment in progress · Paid to [Recipient] on D · Returned by recipient's bank · Payment stopped · Check voided | "Failed" for Unknown; "Complete" before Final |
| Finality / reconciliation | Final, Reconciled, PostPaymentReview | (not shown; "Paid" remains) · — · Under post-payment review (staff only unless policy discloses) | — |
| Hold (orthogonal) | Held(reason class) | On hold – [non-sensitive reason class]: eligibility review · verification · sponsor review | Specific sanctions or fraud reasons (UX-F19) |

## 2. Headline derivation (priority order)

1. Hold present → "On hold – …"
2. Payment `Unknown` → "Confirming payment status" (with the W02 copy: "We cannot confirm … check its status before trying again")
3. Payment `Returned` → "Returned – updating payment details"
4. Payment `Disbursed` → "Paid to [Recipient] on [date]"
5. Payment `Submitted/Accepted` → "Payment in progress"
6. Funding `FundingShortfall` → "Funding delayed"
7. Decision `Approved` → "Approved by [Sponsor]"
8. Decision `Declined/Canceled` → that
9. Request state otherwise

## 3. Mapping of baseline vocabularies

| Baseline term (source) | Maps to |
|---|---|
| Received (core command) | Internal only: command receipt. Not shown. |
| Authorized (core) | Decision = Approved |
| Reserved (core) | Funding = Reserved |
| Submitted (core) | Payment = Submitted |
| Observed (core) | Payment = Accepted or Disbursed, by observation type |
| Settled (core) | Payment = Disbursed |
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
