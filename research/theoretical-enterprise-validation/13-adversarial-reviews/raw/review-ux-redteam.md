# Role-separated review: UX reviewer and adversarial red team

Scope: `research/theoretical-enterprise-validation/` folders 06, 07, 08, 09, 10, 12, 14, plus baseline `docs/ui/workflow-content-and-failure-contracts-v0.2.md` and `docs/ui/widgets/03-grant-recommendation-widget-contract-v0.2.md`. I also grepped 05-workflows, 11-scenarios and 16-registers to avoid raising points they already answer. No files under `/home/user/daf-landscape` were modified.

**Caveat:** a model from the same family as the authors wrote this critique. It is role-separated, not independent validation. Severities (1 = cosmetic, 5 = can cause irreversible financial loss or legal exposure at scale) are judgments. Statements about ACH and check law are marked [I] (my inference) where I did not check the primary text.

Paths below are relative to `research/theoretical-enterprise-validation/` unless stated otherwise.

---

## Part A: User experience review

### A1. Headline copy for payment Unknown tells the donor to "try again" (sev 4)
- **Claim:** `09-ux/status-vocabulary.md` §2, item 2. When payment is Unknown, the headline is "Confirming payment status" plus the W02 copy "We cannot confirm … check its status before trying again".
- **Problem:** The W02 sentence (baseline W02 "Unknown status message") was written for the *command receipt* Unknown: "was my recommendation received?". Section 3 of the same file says the two Unknowns are different objects. On a grant, "before trying again" tells the donor that recommending again is the expected next step, while the money may already be at the charity. This is the FMEA-13 path (the status label leads to a duplicate grant). REC-4 and WG-5 only *flag* duplicates. Under assurance-bound auto-approval, the second grant to a known recipient goes through the routine path.
- **Correction:** Give payment Unknown its own copy, for example: "Your grant was approved. We are confirming the payment with the bank. You do not need to do anything. Do not send a new recommendation for this grant." Add a deterministic rule: a new recommendation to the same recipient, at an amount within ±X, while a sibling grant is in payment Unknown, is referred to a human and never routine-approved.

### A2. Hold at priority 1 hides that money has left (sev 4)
- **Claim:** `status-vocabulary.md` §2 puts "Hold present → On hold" above every payment state. `state-models.md` SM-4 lets any authorized rule, person or model add a hold to any object at any time.
- **Problem:** Two cases.
  - A hold added while the payment attempt is Submitted, Unknown or Accepted. GR-7 says a fund Frozen or Suspended does not stop such an attempt ("cannot be un-sent"). The donor reads "On hold – verification" and believes no money moved.
  - A hold added on a Disbursed grant (for example during post-payment review, GR-6). The donor sees "On hold" and not "Paid".

  Both lead to a false belief that the grant was not paid. Likely results: re-recommendation, a complaint to the charity, or a wrong tax position. GR-6 says post-payment review "does not change the grant's state", yet the headline effectively changes.
- **Correction:** Rank holds below any payment state from Submitted onwards. Show the hold as a secondary line ("Payment in progress · Under review"). On a Disbursed grant, never show a hold to the donor unless policy discloses post-payment review.

### A3. "Returned" outranks "Canceled" for good (sev 3)
- **Claim:** In `status-vocabulary.md` §2, Payment Returned (priority 3) ranks above Decision Canceled (priority 8). `state-models.md` §2 allows `Returned → Canceled` ("funds back to fund").
- **Problem:** The payment dimension keeps the value Returned after the grant is canceled. The donor then sees "Returned – updating payment details" forever, while the grant is actually canceled and the money is back in the fund. The derivation also never says *which* attempt's payment value it reads when there are several attempts (PA-1).
- **Correction:** Derive the headline from the grant's lifecycle state first (Canceled and Declined are terminal and win). Read payment values from the *current* attempt only, and define "current attempt".

### A4. "Paid" at Disbursed contradicts GR-5 and the baseline glossary (sev 3)
- **Claim:** `status-vocabulary.md` uses the label "Paid to [Recipient] on D" at Disbursed. `state-models.md` GR-5 says the UI must not say "complete" or "**paid**" before `Final` without a qualifier. The baseline glossary in `workflow-content…v0.2` says "Paid/settled: supported by verified settlement evidence and reconciliation policy".
- **Problem:** These are direct contradictions. The vocabulary also forbids only "Complete before Final", not "Paid".
- **Correction:** Pick one rule. Suggestion: "Sent to [Recipient]'s bank on D" at Disbursed, and "Paid" only at Final or Reconciled. Alternatively, amend GR-5 and the glossary explicitly.

### A5. The headline drops states the vocabulary promises (sev 2)
- **Claim:** In `status-vocabulary.md` §3, Failed → "Payment being prepared again or a delay notice". Funding → "Selling investments to fund grant".
- **Problem:** The §2 derivation never reaches Funding, Funded or Prepared. Once a grant is Approved, the headline stays "Approved by [Sponsor]" through liquidation, a failed attempt and re-preparation. The promised delay notice can never be the headline. "Selling investments" also alarms P2 and P4 users, and it is false under the cash sleeve (alternative 1D).
- **Correction:** Either add these states to the derivation or remove the promises. Replace "Selling investments" with "Preparing funds".

### A6. Proactive push "at each change" makes the five-dimension model noisy (sev 3)
- **Claim:** `alternatives.md` §6C says the five-dimension status with a push at each change removes "where is my grant" contacts.
- **Problem:**
  - One grant can produce 8 to 12 transitions across the five dimensions. An advisor with 200 clients would receive thousands of pushes in December.
  - The content rule allows no amounts or names in previews, so every push reads like "A grant status changed", which is a reason to log in or call.
  - For P2 and P4, "Confirming payment status" or "Funding delayed" arriving as a push is exactly the anxiety trigger named in §8.
  - For a deceased donor, pushes keep going to the decedent's devices while the fund is paused.
- **Correction:** Send pushes only on donor-meaningful milestones (approved, declined, sent, returned, action needed). Let advisors receive digests. Never push transient states (Unknown, Funding). Stop all notifications to the decedent's channels when a death notice arrives.

### A7. Accessible step-up conflicts with assurance binding (sev 4)
- **Claim:**
  - P2 needs a "phone fallback" (`personas…md` §1).
  - UXA-3 says hardware keys may not suit P2 and P4.
  - TVCTL-06 requires step-up for new recipients from phishable sessions. OD-14 requires confirmation of new recipients always.
- **Problem:** The artifacts never say what assurance a phone or agent-assisted confirmation carries. Two outcomes are possible.
  - If phone confirmation counts as high assurance, it becomes the social-engineering bypass of TVCTL-06. FT-3 already lists "staff acting on email instruction".
  - If it does not count, users who cannot use passkeys can never recommend a new charity: an accessibility exclusion (WCAG 3.3.8 aims at the inverse).
- **Correction:** Define a phone confirmation protocol: an outbound call to a number on file for more than N days, with no inbound-call confirmation. Record it as its own `amr` class. State in policy which grant classes it can confirm.

### A8. A 60-second ContextChanged poll can wipe a screen-reader user's review (sev 3)
- **Claim:** `widget-integration-model.md` WG-1 / TVR-WID-001: on an authority-revision change, the widget clears its data within ≤60 s.
- **Problem:** Any revision change, including benign ones (an unrelated co-advisor added, a policy version bump), clears the view mid-review. This is an unexpected change of context (WCAG 3.2.x). It also contradicts UXA-4 / 3.3.7 Redundant Entry, which says not to lose entered data. "Authority revision" is not filtered to changes that reduce the user's rights.
- **Correction:** Clear the view only on a *reduction* of rights affecting this fund and capability. Otherwise mark the view stale and revalidate at submit. Announce the change once, move focus to a stated target, and keep the draft where policy permits.

### A9. Time limits with no WCAG 2.2.1 treatment (sev 3)
- **Claim:**
  - Preview hash expiry (GRW-06; personas §2.1).
  - `AwaitingRequesterConfirmation → Expired` (state-models §1).
  - Draft TTL `Abandoned`.
  - Session expiry (UXA-4).
- **Problem:** Only session expiry has an extension rule. For an agent-originated recommendation, the "confirm window" silently becomes Expired. Nothing requires a warning, an extension, or a notification that it expired. P4 users (bereaved, stressed) are the ones who miss windows.
- **Correction:** List every timed step against WCAG 2.2.1. Regenerate the preview silently. Notify before expiry. Make Expired recoverable as "resume this recommendation".

### A10. The command-Unknown dead end has no exit (sev 3)
- **Claim:** `personas…md` §2.1: "no resubmit button until resolved".
- **Problem:** No bound and no fallback is defined if the receipt lookup itself stays Unknown (for example during the outage that caused the timeout). An older donor will phone, or recommend through another channel (partner widget, advisor). WG-5 treats that as a flag only.
- **Correction:** Set an SLA after which a human-owned case opens and the donor gets a named contact. The phone agent must see the same command record.

### A11. A percentage grant is confirmed as "about $X" but fixed later (sev 3)
- **Claim:** `personas…md` §2.1 (review shows "about $X"); FI-10 fixes at approval; FI-16 allows `C` (reservable capacity) as a denominator.
- **Problem:** The donor consents to an estimate. Approval can be days later, for example under AwaitingHumanDecision during a December drawdown (event storm §4). A percentage of `C` depends on other people's reservations and on haircuts the donor cannot see, so the donor cannot verify it. P2's "misreads % grant" error is designed in, not mitigated.
- **Correction:** Remove `C` from the donor-selectable denominators. Show a fixing date and a range. Add a donor-set ceiling ("not more than $Y"). If the fixed amount differs from the preview by more than a tolerance, the grant needs reconfirmation.

### A12. Interaction models C and E conflict with the agent principal P9 (sev 4)
- **Claim:** §3.1 model C: "AI never submits from free text; conversation must end in the B review screen". P9 "Recommend within caps". OD-14: confirmation is required for new recipients plus caps.
- **Problem:** A donor's own conversational assistant *is* a P9 agent. Below the cap and to a known recipient, it submits with no review screen (TVF-017 is still open). So the "C is only an entry point into B" conclusion holds only for the sponsor's own chatbot. Model E scores + on every criterion, including cost, but the "donor confirms" step assumes the donor confirms in their own session (§3.2C). For an advisor with 200 clients in December, that means 200 separate donor sessions, so either the confirmation is rubber-stamped or many are abandoned.
- **Correction:** State that the model C rule applies to every natural-language origin, including third-party agents: agent recommendations from free text need a confirmation, cap or no cap. Rescore E's cost and error prevention with confirmation fatigue and abandonment as variables.

### A13. P5 at scale: drafts invalidated on context switch (sev 3)
- **Claim:** P5 "context switch invalidates drafts (TVC-011)".
- **Problem:** A year-end advisor works across many clients at once. Losing drafts on every switch pushes the work into spreadsheets and then into bulk entry, which is where wrong-client errors happen. The cross-client dashboard named as an information need is specified nowhere.
- **Correction:** Scope drafts per client. Revalidate at submit instead of deleting. Require a client-identity confirmation on review (name plus fund) that cannot be skipped. Add a cross-client batch review with per-item identity.

### A14. P17 (charity) copy invites a phishing pattern (sev 3)
- **Claim:** The donor headline is "Returned – updating payment details" (`status-vocabulary.md`, `05-workflows` line 117). UXA-6 says the charity re-enrolment flows are not designed.
- **Problem:** The donor, or the donor's advisor, tells the charity "they're updating your bank details". This primes the charity clerk to accept an emailed "update your bank details" request, the exact P17 fraud vector. The donor also gains nothing actionable.
- **Correction:** Donor copy: "Returned by the charity's bank. We will contact the charity through verified channels." Charity-facing copy must state that the sponsor never requests bank changes by email.

### A15. The screen-state set is too large to govern (sev 2)
- **Claim:** `status-vocabulary.md` §5: an 18-state union with heading, body, announcement and action per state per surface.
- **Problem:** That means hundreds of governed strings (content-governance rule), most of them never tested. Untested copy is where the misleading labels in A1 to A4 come from.
- **Correction:** Group the states into fewer families with shared copy patterns. Require usability testing only for the families on financial surfaces.

### A16. The automation-bias canary can reach the money path (sev 3)
- **Claim:** `personas…md` §2.4: seeded cases (CTL-046) indistinguishable from real ones. TVCTL-04 uses canaries "in a production-like environment".
- **Problem:** If a canary is indistinguishable in the production queue, an approval must still never create a reservation, a payment or a 990/Schedule D record. That guard is not stated anywhere. A canary also skews the reviewer metrics used for staffing.
- **Correction:** Canaries carry a server-side marker invisible to the reviewer that hard-stops before reservation. Count them out of all reporting.

---

## Part B: Adversarial red team

### B1. Most dangerous chain: grooming a recipient through the giving plan (sev 5)
- **Claim:**
  - Alternative 2D: the giving plan in Q3, then deterministic execution in December.
  - Alternative 1D: the cash sleeve pays at once.
  - TVCTL-06 / OD-14: step-up applies to *new* recipients only.
  - CON-1 / alternative 3C: provisional credit.
  - FMEA-03: a sham charity passes Pub 78.
  - Content rule: no amounts or names in pushes.
- **Scenario:**
  1. The attacker sets up a real, Pub 78-listed 501(c)(3).
  2. In Q3 the attacker takes over donor accounts. Older donors on phishable factors are the target. Passkey or credential enrollment after takeover is not gated by step-up anywhere I could find: only passkeys are promoted (UXA-3).
  3. The attacker adds the charity to each donor's giving plan and passes the new-recipient step-up with the newly enrolled passkey.
  4. The sponsor pre-clears the recipient during quiet-season review. It is a real charity.
  5. In December the plan executes "deterministically". The recipient is no longer new, so no step-up applies. No fresh session exists, so session assurance cannot be checked.
  6. The cash sleeve pays at once, which removes the T+1/T+2 liquidation delay that was a natural detection window.
  7. Optional ACH top-ups under the per-donor provisional limit add capacity. The R10 return lands 60 days later as a donor receivable.
  8. The detective controls are muted. Push notifications are deliberately uninformative, the attacker may have changed the contact channels, and specialists are in surge. Post-payment review is all that is left.
- **Controls defeated at once:** TVCTL-06, the velocity control (the payments are spread across many accounts and look like plan execution), TVCTL-04 (the recipient is eligible), notification as a detective control, and the timing benefit of review.
- **Correction:**
  - Plan items to a recipient first added within N months of execution re-confirm at execution with step-up.
  - Credential or factor enrollment, and contact-channel changes, need step-up, notify the *old* channel, and start a cooling-off period that blocks new-recipient additions.
  - Run cross-fund concentration analytics on recipients first added in Q3 plans.
  - Any sleeve-paid grant to a recipient that this fund has used for less than N days waits for a minimum hold period.

### B2. Check void and reissue: the diagram contradicts PA-4 and enables double payment (sev 4)
- **Claim:** `state-models.md` §3 has "Settled → Voided: check only, before presentment". PA-4 says "Issued is Accepted"; Settled means presented and cleared. PA-1 allows a new attempt once an earlier one is Voided.
- **Problem:** By PA-4's own definition, an unpresented check is Accepted, so the drawn transition can never apply. Implementers will either mark issued checks Settled to make Void possible, or void from Accepted with no defined path. In either case, Voided is terminal, so PA-1 permits a reissue. The original paper may still be honoured: a bank can pay a stale-dated check in good faith, and stop-payment orders lapse [I: UCC 4-403/4-404]. That is FT-1's "check cashed after void + reissue" with no structural block.
- **Correction:** Use `Accepted(Issued) → StopRequested → Voided` only after the bank or positive-pay confirms. Treat Voided as non-terminal for PA-1 until the stop is confirmed and positive-pay is active. Track the original paper to stale date before releasing the reservation.

### B3. "Late return, unauthorized-debit class" applied to outbound grants (sev 2)
- **Claim:** `state-models.md` §2 has "Final → Returned: late return (rail allows, e.g. unauthorized-debit class)".
- **Problem:** Grant payments are ACH *credits*. R10 and the 60-day window apply to *debits*. The contribution-side fact (`08-compliance` §1) has been carried over to the payment side [I]. This makes "Final" either meaningless or mis-sized.
- **Correction:** Define finality per rail and per direction from Nacha rules (credit returns and reversals), and verify it.

### B4. The cash sleeve's relation to FI-05 is unstated (sev 4)
- **Claim:** `alternatives.md` 1D, recommended in OD-13 as a hybrid: "Grants paid from the sleeve … combined with C for amounts above the sleeve."
- **Problem:** Nothing says whether sleeve-paid grants still pass FI-05 reservation against `C` (haircut, provisional exclusion, ancestors, over-commitment refusal from FI-12). If "cash-only transitions" skip reservation:
  - provisional ACH cash that lands in the sleeve is spendable at once, defeating CON-1 and TVCTL-03;
  - an over-committed fund (FI-12) still pays new grants from the sleeve, defeating "new reservations are refused";
  - grants could be paid twice from one sleeve balance, defeating FI-08.
- **Correction:** State that every grant, sleeve-funded or not, reserves under FI-05. The sleeve changes only the liquidation step. Provisional cash must be tagged inside the sleeve.

### B5. FI-15 residual sweep contradicts GR-1 and FI-10 (sev 3)
- **Claim:** GR-1 says Approved records a fixed currency amount. FI-15 says a 100% closing grant is fixed after the last settlement, not at approval.
- **Problem:** The rules cannot both hold. FUND-1 also needs zero active reservations at closure, but a sweep grant's reservation amount is unknown until fixed.
- **Correction:** Add a separate `ResidualSweep` grant type that is approved without an amount, has its own fixing event and reservation rule, and comes before FUND-1 closure.

### B6. A model can effectively release its own flag (sev 3)
- **Claim:** SM-5 says "A model never releases". §8 Flag: Raised → Superseded when "a rule re-ran on new data and no longer fires".
- **Problem:** If the flag came from a model (a P-flag), a model re-run that no longer fires supersedes it with no human involved. An attacker who controls a charity's description or uploads (prompt injection, GRW-17) can change the "new data" so the flag disappears. FLAG-1's "never expires by time" does not cover this.
- **Correction:** Allow Superseded only for deterministic-rule flags. Model-raised flags clear only by a human.

### B7. An unauthenticated death notice is a denial-of-service (sev 4)
- **Claim:** `personas…md` §2.2: the notice form needs no login, and grant activity is paused while verifying. `05-workflows` line 148: a notice from any channel is the trigger.
- **Problem:** Anyone (an estranged relative, a hostile party in a dispute, a prankster) can submit a notice on December 28 and freeze a living donor's year-end grants. The flow does not say who notifies the living donor, or how fast the pause is lifted. It also conflicts with AUTH-I3 (death-index signals are "a flag only") and GR-8 (approved grants continue).
- **Correction:** An unverified notice triggers an immediate out-of-band contact to the principal on file and a *review* flag. A pause happens only with corroborating evidence or no answer within N days. Approved grants follow GR-8.

### B8. TVCTL-02 relies on TVCTL-07's daily reconciler, which may be monthly (sev 3)
- **Claim:** TVCTL-02's independent verification is a "Reconciler (≠ releaser) matches bank debits to attempts daily". TVCTL-07's exception is "At very small scale, a compensating monthly review by an outside accountant".
- **Problem:** At launch scale, the double-payment detective control quietly becomes monthly, while FMEA-01 relies on fast detection for recall. "Exceptions: None" in TVCTL-02 is false in practice.
- **Correction:** Make the daily bank-to-attempt match a separate automated control with the alert going to someone outside payments. The monthly review covers only the remainder.

### B9. GR-3 and PA-2 can leave a grant stuck forever (sev 3)
- **Claim:** GR-3 says no cancel while an attempt is Unknown. PA-2 says Unknown resolves only by provider proof, observation, or a two-approver duplicate-risk decision.
- **Problem:** With an ACH provider that cannot prove non-receipt (TVC-024), Unknown has no timer. The grant, its reservation (FI-07 forbids release) and the fund's closure (FUND-1) are blocked indefinitely. The donor sees "Confirming payment status" for weeks (A1, A10).
- **Correction:** Set an aging SLA that forces the PA-2 human decision. Define a bank-statement non-observation window as acceptable evidence for each rail.

### B10. Non-atomic approval shows "Approved" before capacity fails (sev 3)
- **Claim:** FI-05 / FI-08 / OD-06: approval and reservation may be non-atomic. The later grant then "fails capacity; requester told approved-pending-capacity or declined".
- **Problem:** The vocabulary has no "approved pending capacity". The headline shows "Approved by [Sponsor]" (priority 7), then flips to "Funding delayed" or "Canceled". On December 30 (event storm §4) this produces a wave of confirmed-then-reversed approvals and re-recommendations.
- **Correction:** Decide OD-06 in favour of atomic approval and reservation for donor-visible states. Alternatively, do not show "Approved" until Reserved.

### B11. P9 policy errors give an attacker an oracle (sev 2)
- **Claim:** P9 information need: "Machine-readable status, policy errors".
- **Problem:** Detailed policy errors let an attacker who has compromised an agent binary-search the confirmation caps and velocity limits, then stay just below them (TVF-017).
- **Correction:** Return coarse error classes to agents. Log and rate-limit near-threshold probing.

---

## Checked and could not fault

- SM-0: corrections create child records, and terminal records are never reopened.
- SM-3 / FI-07 / GR-4: timeout never maps to failure, and reservations are never released on Unknown.
- PA-3: one provider key per attempt, reused on retry and never reused across attempts.
- §2.3 of the personas file: no "Retry" button in payment-Unknown resolution.
- FI-11: largest-remainder rounding with a deterministic tie-break, where the line amounts sum exactly to the grant amount.
- REC-4 / WG-5: duplicates are never silently merged. My objection is to severity, not principle.
- The trust-boundary table in the widget model, and consistency rules 1 to 4.
- The status vocabulary's distinction between receipt "Rejected" and sponsor "Declined".
- The content rule keeping sensitive data out of push previews and subjects. Sound for privacy; A6 and B1 note what it costs as a detective control.
- FI-24: four distinct non-cash values, and only sale proceeds fund grants.
- TVCTL-11: evidence integrity is held outside the function it evidences.
- FT-1's finding that the size-1 cut sets are organizational, not software.
