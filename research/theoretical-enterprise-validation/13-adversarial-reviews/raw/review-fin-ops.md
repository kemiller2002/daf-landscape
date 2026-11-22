# Role-separated review: financial controls and operations

**Scope:** `research/theoretical-enterprise-validation/` files 05, 06, 07, 08, 12, 14, 15, 16, checked against `docs/financial-core-control-spec-v0.5.md` and `wf-investments-treasury.md` (WF-17/18).
**Nature:** This is a critique by the same model family that wrote the artifacts, split into two roles. It is **not** independent validation. No code was run and no simulations were done. Statements of law, accounting or industry practice that I am not certain of are marked **[unverified]**. Every accounting point below needs review by a CPA who knows ASC 958 nonprofit fund accounting.
Severity: 5 = could cause irreversible loss, legal exposure or unauthorized money movement; 3 = material misstatement or build defect; 1 = editorial.

---

## (A) Financial controls reviewer

### A-1. The check lifecycle contradicts itself, and the void path is unsafe. Severity 4
- **Claims challenged:**
  - state-models §3 transition `Settled → Voided: check only, before presentment`;
  - PA-4: "A check is `Settled` … only when presented and cleared. 'Issued' is `Accepted`";
  - PA-1 lets a new attempt start once the earlier one is `Voided`.
- **Why it is wrong:** By PA-4, a check that has not been presented cannot be `Settled`, so `Settled → Voided` cannot happen. The void must come from `Accepted`. There is a second problem. A void is internal bookkeeping. A stop-payment or positive-pay void only works if the bank applies it, and a bank can still pay a stopped item by mistake [unverified as to each bank's liability rules]. PA-1 then allows a reissue the moment the check is marked `Voided`. That opens the double-payment path that FT-1 lists ("check cashed after void + reissue paid").
- **Correction:**
  - change the transition to `Accepted → VoidRequested → Voided`;
  - `Voided` requires bank confirmation that the stop or positive-pay exception is in force;
  - reissue is allowed only after that confirmation;
  - if the voided item is presented later, open a recovery case.

### A-2. Check and in-transit cash are counted twice. The ledger "cash" diverges from the bank every day. Severity 4
- **Claims challenged:**
  - FI-21: "issued-not-presented amounts stay as a liability, not as fund cash";
  - GR-4 / FI-07 / FI-17: the reservation is consumed only at `Disbursed` (Settled, which for a check means presentment);
  - FI-03 cash equation.
- **Why it is wrong:**
  - **Checks.** If issuance moves the amount out of fund cash into an outstanding-check liability (FI-21) and the reservation stays `Active` until presentment (GR-4), then capacity `C` is reduced twice for months.
  - **ACH and wires.** The bank debits the sponsor at file transmission or settlement. Prefunded ACH can debit earlier [unverified per bank]. In both cases the debit comes before the platform observes "Settled". Meanwhile FI-17 says "reduce confirmed cash" only on confirmed settlement. FI-03's daily equality (legal-owner cash = Σ fund cash claims + operating + suspense) therefore breaks every day for in-transit items.
  - Ordinary book-cash practice credits cash when the check is issued and treats outstanding checks as a reconciling item [unverified as the sponsor's chosen policy].
- **Correction:**
  - add explicit clearing buckets (disbursements in transit, outstanding checks, returned items pending) to FI-03;
  - at issuance or transmission, move the reservation into an "issued/in-transit" obligation state instead of keeping it `Active` alongside a liability;
  - state which of book cash or bank cash `C` is computed on. [C]

### A-3. "Per-grant liquidation" confuses unit redemption with security sales at the custodian. Severity 4
- **Claims challenged:**
  - invariants §1 facts 5–6 ("Liquidation order … trade instruction to custodian"; "Liquidation settlement: custodian observation");
  - FI-14; FI-17 ("reduce the matching reservation");
  - state `Funding → Funded: cash settled and allocated to this grant`;
  - alternatives §1 B/C ("per-grant liquidation").
- **Why it is wrong:**
  - In a unitized pool, the fund redeems units internally at the struck NAV. The pool sells securities at the custodian on a **netted** basis across all subscriptions and redemptions, or does not sell at all if pool cash covers the outflow.
  - At about 3,200 grants a day, or roughly 10k on peak days (economics §5), per-grant trade instructions are not a real custodian workflow [unverified for any specific custodian].
  - A custodian settlement observation cannot be matched one-to-one to a grant reservation. The match is an internal allocation.
  - WF-18 step 3 already redeems units for "released grants" at the struck NAV. That implies the pool fronts the cash. It contradicts the program's Reserved → Funding → Funded order, and the contradiction register does not record it.
- **Correction:**
  - split fact 5 into "unit redemption (internal, at NAV)" and "pool trade (external, netted)";
  - FI-17 should match grant reservations to *pool cash allocations*;
  - pool trade settlement is reconciled separately at pool level;
  - add WF-18 step 3 vs the Funding state to the contradiction register.

### A-4. Approval, reservation and funding order are three different orderings. Severity 4
- **Claims challenged:**
  - FI-05 (on failure the grant "stays `Approved` and held 'insufficient capacity'");
  - FI-08 ("cannot both be approved if together they exceed `C`"; "approval order is the serialization order of reservations");
  - FI-12 ("unfunded grants are funded in approval order");
  - WF-17 step 5 ("first-in-first-out");
  - CW-03 ("order by reservation time").
- **Why it is wrong:**
  - FI-05's first branch allows an approved but unreserved grant. FI-08 forbids exactly that.
  - Once approved-without-reservation exists, approval order and reservation order differ. FI-12, WF-17 and CW-03 each then fund grants in a different order.
  - Fact 2 says approval "commits" the sponsor. Approving with no capacity is a commitment backed by nothing.
  - If approval is communicated to the grantee, the sponsor may have to recognize an unconditional promise to give, as a liability and expense, when it is made [unverified; C].
- **Correction:** resolve OD-06 in favor of making approval and reservation atomic. If capacity fails, the result is not an approval ("pending capacity" is a pre-decision state). Then define one ordering key, the reservation sequence, used by FI-12, WF-17 and CW-03.

### A-5. Reversing a provisional contribution after units were issued shifts gains and losses onto other donors. Severity 4
- **Claims challenged:**
  - FI-22 / CW-07 ("Units issued at Provisional … so investment exposure starts");
  - FI-23 ("Units issued against it are cancelled");
  - CON-3.
- **Why it is wrong:**
  - The pool received cash X and issued units at NAV₀. On reversal X leaves the pool, but the cancelled units are worth units × NAV₁.
  - If NAV fell, the pool is short by X − units·NAV₁, and every other unitholder absorbs that loss. If NAV rose, the donor's fund keeps a windfall.
  - Neither invariant attributes this difference.
  - CON-3's "sponsor receivable from the donor" may not be enforceable or collectible, and it does not say **which net assets** absorb the loss. Charging it to the pool or to other funds would be improper.
  - Fees charged on provisional value (FI-22) are not addressed when the contribution reverses.
- **Correction:**
  - on reversal, the pool is made whole at the original cash amount;
  - the NAV difference and any uncollectible receivable go to sponsor operating net assets (or a named loss reserve);
  - fees on reversed value are refunded or kept per a stated policy. [C]

### A-6. The ACH return window is applied to the wrong direction. Severity 3
- **Claims challenged:**
  - state-models §2 `Final → Returned: late return (rail allows, e.g. unauthorized-debit class)`;
  - GR-5; CW-06 ("including after `Final` where the rail allows").
- **Why it is wrong:**
  - Grant payments to charities are ACH **credits**. The R10 60-day unauthorized-return window (compliance §1) applies to **debits**, which here means donor contributions. Credit returns are mostly two banking days. Late or dishonored returns and originator reversals are separate mechanisms [unverified detail].
  - The grant `Final` timing is therefore mis-parameterized. If `Final` is set to 60 days, `Reconciled` (which requires `Final`) is delayed for two months.
  - The model also lacks ACH originator **reversals** of a settled credit (wrong amount, duplicate, wrong receiver; short time limit; the receiving bank may not recover the funds [unverified]). These are the main real tool against a double payment.
  - `Accepted → RecallRequested` is unrealistic for ACH once the file has been transmitted.
- **Correction:**
  - give the parameter table per rail and direction (contribution debit vs grant credit; wire; check; card);
  - add `Settled → ReversalRequested → Reversed | ReversalFailed`;
  - split `Accepted` into accepted-not-transmitted (cancellable) and transmitted.

### A-7. Reconciliation is tied to finality. Severity 3
- **Claim challenged:** state-models §2 `Final → Reconciled`; CW-01 Success = "`Reconciled` after `Final`".
- **Why it is wrong:** Reconciliation is matching, and TVCTL-02/07 require it daily. Finality is the passing of time. Putting `Reconciled` after `Final` leaves every disbursement looking unreconciled during its return window. It also hides real breaks among the normal pending items.
- **Correction:** make reconciliation status an orthogonal attribute of the attempt (matched / break). Let `Final` and `Reconciled` be independent, with termination needing both.

### A-8. Reservation residuals have no legal way to be released, so they become "Stranded" by design. Severity 3
- **Claims challenged:**
  - FI-07 / GR-4: release happens only by cancellation, decline or consumption;
  - FI-31: the FX buffer is included in the reservation;
  - FI-14: the liquidation buffer;
  - bank fees deducted from the payment.
- **Why it is wrong:** A foreign-currency grant settles at an amount X that differs from the reservation (amount plus buffer). FI-17 reduces the reservation by X, which leaves a residual. No permitted release event covers it, so it becomes `Stranded`, the state defined as a defect.
- **Correction:** add "residual release on final settlement" as a permitted, journalled event. Record realized FX gain or loss to a named account. State who bears wire and FX fees (fund or sponsor).

### A-9. Money with no owner: float income, rounding, credit-line interest, fees. Severity 3
- **Claims challenged:** FI-02 ("within tolerance"); FI-03; WF-17 step 4 (line of credit); alternatives 1E (sponsor fronts cash).
- **Why it is wrong:**
  - Interest earned on cash in transit, on outstanding checks, on liquidation proceeds awaiting payment, and on suspense has no attribution.
  - Accumulated unit-rounding residuals inside the FI-02 tolerance have no owner.
  - Interest on a credit line drawn to pay grants has no attribution. Debt in the pool may also raise debt-financed income (UBTI) questions [unverified].
  - Return and wire fees have no attribution.
- **Correction:** add an invariant: every income and expense item resolves to exactly one of {fund, pool (pro rata), sponsor operating}, under a stated rule, with a zero-unattributed daily check.

### A-10. The fund-accounting framing is not ASC 958 framing. Severity 3 (needs CPA review)
- **Claims challenged:** FI-03 "fund cash claims"; CON-3 "fund deficit case"; FI-25/26 fee "revenue" priority; FI-19/20 return and refund treatment.
- **Why it is wrong:**
  - DAF assets are the sponsor's assets under exclusive legal control. In GAAP statements, the funds are internal designations within net assets, often presented as with or without donor restrictions per variance power [unverified; C].
  - Sponsor fees from its own DAFs are then intra-entity transfers, not external revenue [unverified; C].
  - "Claims" language risks implying donor ownership.
  - None of the documents states **when grant expense and grant payable are recognized**: at approval, at communication to the grantee, or at payment. A post-settlement return (FI-19) or a recipient refund (FI-20) cannot be booked correctly without that.
  - FI-23's "effective date = original" must not become a GL posting into a closed period (FI-01).
- **Correction:**
  - add an explicit mapping from the 12 facts to GL events, recognizing that reservations are encumbrances with no GAAP effect;
  - label the fund sub-ledger as management accounting;
  - get a CPA opinion on expense recognition and on presenting fees.

### A-11. A single break blocks reservations across the whole sponsor. Severity 4 (also an operations issue)
- **Claims challenged:**
  - FI-03 ("no new reservations against the affected account until classified");
  - FI-29 ("blocks new reservations on the affected resource when its amount exceeds a threshold");
  - FI-05 (all constrained ancestors).
- **Why it is wrong:** Almost every fund draws on the same legal entity, custodial account and operating bank account. An unclassified break on that account, including routine timing differences, therefore halts every reservation for every donor. In December that halts the business. FI-03 has no threshold at all.
- **Correction:**
  - scope a hold to the amount at risk: reduce the ancestor's capacity by the break amount, with a haircut, instead of setting it to zero;
  - put a materiality threshold on FI-03;
  - define a timing-difference class that never blocks.

### A-12. The ancestor-lock design creates one global hot lock. Severity 2
- **Claim challenged:** FI-05 (serialize check and creation per ancestor, fixed lock order).
- **Why it is wrong:** Every reservation would serialize on the same legal-entity and custodial-account locks, with peak bursts of about 10× (economics §3/tech-arch). That is feasible but fragile. On a $bn ancestor the constraint almost never binds.
- **Correction:** state that ancestor constraints may be enforced by pre-allocated quota or escrow partitions, with exact checking only when headroom is low. Keep the invariant and leave the mechanism open.

### A-13. Frozen funds and OFAC blocking are under-specified. Severity 3
- **Claims challenged:** GR-7 ("Grants already in `PaymentInProgress` follow the attempt to resolution"); fund `Frozen` ("nothing moves, including fees"); SM-4 ("a hold never blocks … cancellation").
- **Why it is wrong:**
  - Under a sanctions block, a payment that is `Authorized` or `Submitted` but not yet accepted should be stopped, and a blocked transaction may have to be rejected or blocked and reported rather than allowed to complete [unverified; legal].
  - Blocked property may have to be held in a separate interest-bearing blocked account [unverified]. Units in a commingled pool cannot be "frozen" while the NAV keeps moving.
- **Correction:**
  - `Frozen` should trigger an attempt-level withdrawal wherever the rail still allows it;
  - add a legal-review step on whether blocked interests must be segregated out of the pool. [C]

### A-14. Smaller points. Severity 2 each
- **FI-15:** the residual sweep needs fees "through the closing date", but the closing date depends on when the sweep settles. Define a fee cut-off.
- **FI-25 vs WF-18 NAV:** if pool-level expenses are already in the NAV, V must subtract only fund-level fees. Otherwise fees are subtracted twice.
- **Haircut (TVC-022 recommendation):** a 100%-equity fund can never recommend its full balance. That product consequence is not costed or disclosed.
- **Economics §5:** the §4966 manager tax requires the manager's knowledge and has a per-distribution cap [unverified: I believe $10,000]. The exposure framing overstates manager liability.
- **FI-22:** donor-initiated ACH **credits** are not reversible like debits. Check returns and card chargebacks have different, and partly open-ended, windows (forged or altered-item claims) [unverified]. "Final" is not final for every rail.
- **Alternatives 1D:** the sleeve is said to make grants "cash-only", but sleeve cash is typically in a money-market vehicle that itself needs redemption [unverified]. Market risk moves to sleeve replenishment; it is not removed. Sizing a sleeve to one fund's grant forecast is statistically meaningless, because individual funds' grants are lumpy.
- **Broken link:** FI §4 and the register point to `16-registers/owner-decisions.md`, which does not exist. The OD-01..OD-12 definitions cannot be checked.

### A — Checked and could not fault
- The economics arithmetic: FTE cases (10.5 / 30 / 219), peak/average 2.5 at k = 3, backlog 9,600, $16m/day, $4/dossier break-even, ~21 reconciliation FTE, and 10 bps / $300 cash drag.
- FI-07 / GR-4: no release on Unknown or timeout.
- PA-3: idempotency key per attempt.
- SM-3: Unknown is not failure.
- SM-0: corrections are child records.
- FI-11: largest remainder with a deterministic tie-break.
- FI-24: the four non-cash values.
- FI-30: a feed is an observation.
- FI-09: per-instance reservation.
- FI-28: bitemporal corrections with a NAV-error case.
- FI-12 does accept over-commitment rather than pretend it cannot happen.
- CON-1 default of zero is conservative and coherent.
- The contradiction-register severity counts (7/12/10/5) add up to 34.
- The register honestly marks everything open.
- The R10 60-day statement matches my understanding [unverified].

---

## (B) Operations reviewer

### B-1. Staffing at the annual average is a critically loaded queue. The December backlog never drains. Severity 4
- **Claim challenged:** economics §3 ("backlog … ~9,600 cases, about 37 working days of capacity").
- **Why it is wrong:**
  - Staffing at the average makes annual capacity equal annual arrivals: 64,000 = 256/day × 250.
  - After December, the base arrival rate is 64,000 / 300 ≈ 213 a day. Capacity has a surplus of only about 43 a day, so clearing 9,600 cases takes about 223 working days.
  - So the backlog effectively carries into the next December. Any randomness in arrivals makes it grow without bound.
  - "37 days" understates the problem by a factor of about 6.
  - December demand also clusters in the last 3–5 business days, so k for that week is likely well above 3 [unverified; no data].
- **Correction:**
  - require staffing at a target utilization (for example ≤ 80–85%) **plus** a surge plan sized to clear the year-end backlog by a stated date;
  - model k by week, not by month.

### B-2. Coverage over the holiday cannot satisfy the separation-of-duties chain. Severity 4
- **Claims challenged:**
  - organization §4 (floor ~6–8 people);
  - TVCTL-02 ("PA-2 human decision requires two approvers (releaser excluded)");
  - SoD-1 (profile approver ≠ releaser);
  - TVR-ORG-003 (releaser ≠ reconciler);
  - CTL-013 (sanctions officer ≠ grant approver);
  - failure-analysis §4 ("payment-ops staff are at minimum (holiday)").
- **Why it is wrong:** On a single day, payment operations need a profile approver, a releaser, an independent reconciler, two PA-2 approvers who are not the releaser, and a sanctions decider who is not the approver. Covering absence two-deep needs about 10 or more people on rota from Dec 24 to Jan 2. That contradicts the 6–8 floor. The documents contain no rota, on-call or holiday model.
- **Correction:** add a requirement for a minimum staffed roster per role and per day (holiday calendar, on-call, backup delegates pre-authorized in the DoA), and derive the headcount floor from it.

### B-3. A batch timeout turns PA-2 into thousands of two-approver decisions, and failover to another provider is blocked. Severity 4
- **Claims challenged:** PA-1, PA-2, TVCTL-02; failure-analysis §4 step 3; TVC-024 recommendation (a).
- **Why it is wrong:**
  - One batch timeout can create thousands of `Unknown` attempts. PA-2 is designed per attempt and requires two humans.
  - No provider-level resolution procedure exists (for example, reconciling the provider's acknowledgment or return file in bulk), and there is no time limit.
  - PA-1 forbids a new attempt while one is `Unknown`, so switching to a secondary rail provider is **impossible** for every in-flight grant. Vendor redundancy does not help exactly when it is needed.
  - TVC-024 option (a), "only providers with idempotent APIs", may leave too few ACH providers to choose from [unverified].
- **Correction:**
  - define a batch-level Unknown runbook: bulk query, provider file reconciliation, a decision at batch level by named roles, and a time limit;
  - contract for provider-attested non-receipt at batch level;
  - state the resulting failover latency explicitly as a service-level fact donors and charities are told.

### B-4. Fail-closed controls have no degraded mode, so a stale feed stops all grants. Severity 4
- **Claims challenged:**
  - TVCTL-04 (Exceptions: "None"; failure response: hold);
  - CTL-011 (stale feed blocks);
  - TVCTL-05 (hold if the fallback cannot run);
  - FLAG-1 (flags never expire).
- **Why it is wrong:**
  - A late IRS data file, a delayed OFAC list fetch, or an outage of the benefit-check agent together with its fallback holds every payment. That can happen on Dec 30.
  - Failing closed is right for sanctions. But no document says who may authorize a degraded mode for the non-strict-liability checks (for example, the previous day's eligibility snapshot for already-approved grants), how long it may last, or what residual risk is recorded.
  - Incident response (CW-32) is ~6/18 specified. The kill switch's two-person rule is only "proposed". No RTO or RPO exists for the custodian, the payment provider, the IRS feed or the OFAC feed.
- **Correction:**
  - write a degraded-mode matrix per control: strict-liability items fail closed with no exception; other items get a bounded, pre-authorized degraded mode with an expiry and a mandatory look-back;
  - set RTO and RPO per dependency;
  - make TVR-OPS-003 drills a release gate, not a plan.

### B-5. Over-commitment decisions after a market drop cannot be handled case by case. Severity 3
- **Claims challenged:** FI-12 ("remaining shortfall is a sponsor decision case"); TVCTL-01 ("case decisions by CFO above threshold"); failure-analysis §4 step 2.
- **Why it is wrong:**
  - A 4% drop on a peak day can put hundreds of funds into over-commitment at once. A CFO cannot decide each one before the year-end cut-off.
  - FI-26 correctly says fee priority must be decided in advance. FI-12 leaves grant priority to incident-time cases.
- **Correction:** make the OD-08 rule a pre-approved deterministic playbook, as WF-17 does for the market playbook. Only cases outside the rule go to a human, with a stated limit on volume.

### B-6. NAV and reconciliation need evening and daily coverage that no one is assigned to. Severity 3
- **Claims challenged:** WF-18 ("NAV published by market close + 3 hours"; a price exception creates a controller case that blocks publication); TVCTL-07 (daily independent reconciliation); TVCTL-07 exception ("outside accountant monthly" at small scale).
- **Why it is wrong:**
  - A controller must be on call every trading evening.
  - The small-scale compensating control is monthly, but TVCTL-02 depends on **daily** independent matching to catch double payments. A monthly review would leave about 30 days of exposure.
  - Using internal audit as the operator of the reconciliation (TVCTL-07 "or internal audit"), while also making it the tester (TVCTL-01, -04, -11), weakens its independence [unverified as to the IIA standards wording].
- **Correction:**
  - name on-call coverage for NAV;
  - keep daily matching at every scale, even if it is outsourced;
  - never make internal audit the operator of a control it tests.

### B-7. The supply of specialists and time to train them are treated as unlimited. Severity 3
- **Claim challenged:** economics §3 ("Seasonal specialists: Linear").
- **Why it is wrong:** The peak demand is 75 FTE (expected) to 548 (high) of legally competent reviewers for about 5 weeks. Such reviewers cannot be hired seasonally, and onboarding includes DoA delegation and SoD set-up. The effect is not linear: new staff increase automation bias and error (FM-04).
- **Correction:** cap the seasonal share. Require that the levers (lower e, giving plan, deferral windows) are proven in a pilot before a scale target is set.

### B-8. Year-end timing for the rails and the calendar is not modelled. Severity 3
- **Claims challenged:** failure-analysis §4 (Dec 30 scenario); CW-01; FI-10.
- **Why it is wrong:**
  - Dec 25 and Jan 1 are Federal Reserve and market holidays.
  - Equity and fund liquidation settles T+1 [unverified as to each holding].
  - Under Reserved → Funding → Funded, a grant approved on Dec 30–31 cannot be paid in the calendar year. That matters to charities that expect receipt by Dec 31, and to the sponsor's 990 timing [unverified materiality].
  - Under CON-1 (default 0), December ACH contributions cannot be granted until about February, and CON-2 delays their acknowledgments to February as well.
  - None of this appears in donor-facing cut-off dates or staffing.
- **Correction:**
  - publish a year-end calendar: last approval, funding and payment cut-offs per rail;
  - plan the February acknowledgment surge;
  - decide OD-04 before the first December.

### B-9. Human time limits are missing throughout. Severity 3
- **Claims challenged:** PA-2; CW-11 (death verification); CW-06 ("H after N days"); FLAG-1 (SLA escalation); TVCTL-07 (breaks aged > threshold → Audit Committee).
- **Why it is wrong:**
  - Almost no human step states a time limit, a backup decider or an escalation target that is available.
  - Escalating to the Audit Committee or the CFO during the holidays is not an execution path.
- **Correction:** for each human decision in the critical workflows, record the time limit, the primary and backup role, and the action taken if the limit is missed. The action must never be "approve".

### B-10. Vendor dependence and evidence. Severity 3
- **Claims challenged:** alternatives 7D; TVCTL-* "Independent verification: auditor"; PA-2 [C: provider contracts].
- **Why it is wrong:** Several key controls rest on provider capabilities that are unverified (GAP-002, GAP-025). No exit plan, dual-provider design or contingency for losing a custodian or provider exists. A custodian conversion takes many months [unverified].
- **Correction:**
  - set provider-capability acceptance criteria as G6 gate evidence;
  - require a documented exit or contingency plan per critical vendor;
  - do not count controls that depend on vendor reports until the SOC 1 reports have been obtained.

### B — Checked and could not fault
- Failure-analysis §4 correctly identifies that the failures happen together and share the same staff.
- FT-1's finding that the main double-payment paths are organizational.
- TVR-ECON-002: deterministic list refreshes, not agents.
- The counterfactual "remove AI → D path unaffected" is consistent with DD-002 and TVCTL-05.
- Moving controls earlier with the giving plan (2D) and pre-verified succession (5C) is operationally sound.
- GR-8 / CW-11 immediate actions (Interim state, revoke sessions, suspend templates) are executable.
- The interim succession states do not grant authority before verification.
