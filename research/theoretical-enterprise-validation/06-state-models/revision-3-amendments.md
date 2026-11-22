# Revision 3: consolidated amendments

**Status:** proposals [T]. Each amendment **supersedes** any conflicting text in [state models](state-models.md), [financial invariants](../07-financial-invariants/financial-invariants.md), [status vocabulary](../09-ux/status-vocabulary.md), the [organization and authority model](../03-organization/organization-and-authority.md) and the [owner decisions](../16-registers/owner-decisions.md).

Source: round 3 (TVS-501..556 grants and lifecycle; TVS-601..656 security and cross-domain). Finding IDs are TVF-177..200 (H-n) and TVF-201..225 (K-n).

The round-3 grant pass found that 16 of its 24 findings were **revision-2 rules applied in one section but not carried through the others**. This file is that carry-through. A future editorial pass should fold these amendments into the base documents. Until then, read the base documents together with this file.

## A. Grant, payment and lifecycle consistency

| # | Amends | Amendment | Finding |
|---|---|---|---|
| A1 | Grant §2, PA-1 | `Disbursing` has sub-state **PartlyDisbursed** (Σ settled < amount). The next part's attempt is allowed under cumulative PA-1. A return of one part reduces the settled total. Label: "Partly paid – $x of $y sent". | TVF-177 |
| A2 | GR-3, GR-9, §3 | A cancellation requested while an attempt is Submitted or Unknown **waits** for the attempt outcome, then is re-decided. A check in Unknown may receive a positive-pay stop (`Unknown → StopRequested` for checks only). | TVF-178 |
| A3 | Status §2 | The headline considers **open child cases**. "Paid to X" is replaced by "Payment under review" while a misdirection or recovery case is open. A canceled-but-settled grant shows "Canceled – payment had already been sent; we are recovering it". Replacement grants (GR-12) link to the original. | TVF-179 |
| A4 | Status §2 rule 2 | Human routing during payment Unknown covers recurring instances and co-advisors' recommendations for the **same fund and same recipient**. It does not cover the donor's other funds. | TVF-180 |
| A5 | Status §2 rule 3 | "– under review" is shown only where sponsor policy discloses reviews. It is **never shown for sanctions or fraud holds**, for which a neutral "Payment in progress" remains. | TVF-181 |
| A6 | FI-15, GR-1 | A residual sweep is fixed only when every other grant from the fund is Final, no contribution is Provisional, and fees are assessed through the closing date. Before fixing, the label is "Amount will be set after [sale/closure]". Proceeds-linked grants (FI-39) define multi-lot sales (sum of lots) and use net proceeds after transaction costs [P]. | TVF-182, TVF-191 |
| A7 | GR-11 | The over-commitment exemption for re-payment covers the returned cash **plus** a top-up up to the recorded fee or FX difference. Anything beyond that is a new reservation. | TVF-183 |
| A8 | PA-4, FI-21 | A **bank-confirmed void restores the commitment**: the outstanding-check liability reverses into an Active reservation for the same grant. Then a reissue, re-plan or cancellation follows. | TVF-184 |
| A9 | PA-6 | Contradicting evidence after `Lost` or `Rejected` also opens a double-payment case. | TVF-185 |
| A10 | PA-2 | Each provider adapter contract declares, **per rail**, which evidence sources can observe an individual payment. Where the bank sees only net or batch totals (pre-funded providers, netted ACH files, checks before presentment), the bank's half of the two-source proof is the provider's per-item ledger reconciled to the net bank total. If no per-item source exists, only `ResolvedByDecision` is available. | TVF-186, TVF-219 |
| A11 | Contribution §5 | Standing contribution debits are suspended only on a **verified** death notice, not an unverified one. | TVF-187, TVF-202 |
| A12 | TIME-2 | Fail-closed on clock skew applies to money-moving and authority-changing commands only. **Protective actions** (stop, recall, void, hold, cancellation request, recording external observations) remain available. | TVF-188 |
| A13 | GR-10, FI-05, FI-09 | `ApprovedAwaitingCapacity` grants take their sequence number **at approval** and are funded first when capacity frees. Displayed availability subtracts them. Expiry is paused while the fund is Frozen. A **routine** grant that fails capacity is not approved: its recommendation stays `Submitted` with the label "Waiting for available funds" up to a time limit [P], then expires with notice. A recurring instance that fails capacity is held, and the series continues. This replaces the revision-1 "Approved and held" wording in FI-05 and FI-09. | TVF-189, TVF-200 |
| A14 | FUND-1, FUND-3, FI-15 | Closure, merge routing and the residual sweep also require: no grant in UnderReview, AwaitingHumanDecision or ApprovedAwaitingCapacity; no open cancellation request; no open post-payment review or recovery case. | TVF-190 |
| A15 | OD-10 | Fee priority is extended to **charges and commitments** (FI-37: capital calls, UBIT) against reserved grants. | TVF-192 |
| A16 | REC-5 | A supersession withdraws the original **only when the replacement is Submitted**. An unconfirmed agent edit does not withdraw anything. | TVF-193 |
| A17 | AUTH-I5 | Undecided recommendations from a person named in an unverified notice go to human review (REC-3). They are neither auto-approved nor dropped. | TVF-194 |
| A18 | Grant §2 | An open **post-payment review** blocks re-payment after a return. | TVF-195 |
| A19 | FI-17 | A settlement larger than the reservation posts the excess to **error-cost suspense** (OD-20), never to the donor's fund, and opens a case. | TVF-196 |
| A20 | §3 | `ResolvedByDecision` has two outcomes. `DeemedSettled`: the reservation is consumed and recovery is monitored. `DeemedNotReceived`: a new attempt is allowed, with the duplicate-risk acceptance recorded. | TVF-197 |
| A21 | Status §2 rule 5 | After a return, the label stays "Payment returned – under review" until re-payment is decided and no hold applies. Only then does it read "Arranging payment again". | TVF-198 |
| A22 | §3 diagram, FUND-1 | `Accepted (check) → Escheated` on dormancy, per the unclaimed-property process [C]. At fund closure, outstanding-check liabilities transfer to a **sponsor-level** liability, so an uncashed check cannot block closure for years. | TVF-199; TVS-222 |
| A23 | Grant §2, PA-8 | After a return where the cash is at a provider or intermediary, the grant shows "Recovering funds". It goes back to `Funded` only when the cash is back in the sponsor account. | TVS-217 |

## B. Security, external registers and third parties

| # | Amends | Amendment | Finding |
|---|---|---|---|
| B1 | AUTH-I5 | Person-level holds from an unverified notice **exempt protective requests**: cancellation requests, fraud reports, contact updates through the verified channel. A fraud report from the verified channel holds that person's approved, unpaid grants. | TVF-201 |
| B2 | REC-7, AUTH-I7 | Recipient novelty is measured **from the last confirmation through a channel that existed before the most recent credential change**, not by clock time alone. Waiting out the window does not make a recipient "known". | TVF-203 |
| B3 | TVCTL-06 | **Cross-donor monitor:** many unrelated donors adding the same recipient within a period raises a recipient-level flag. | TVF-204 |
| B4 | AUTH-I8 | **Bulk identifier remap** after a partner changes identity provider or is acquired: dual control, mapping attested by the partner, donor notice, and a temporary assurance downgrade (step-up on first use). | TVF-205 |
| B5 | Authorization formula | A cross-tenant **warning** (fraud or sanctions intelligence) may raise flags and holds in another tenant. It never clears anything, decides anything or supplies verification evidence. | TVF-206 |
| B6 | OD-22, DR | **Restore rules.** One consistent restore point across payment, decisioning, authority and evidence stores. **Security state** (revocations, holds, cooling-off clocks, flags) has zero-loss replication, or is re-derived from external sources before money moves. Blocking after a restore is per record, until each record is reconciled with providers. A predefined break-glass procedure, with dual control, covers the period when the command service is down. | TVF-207, TVF-216 |
| B7 | Migration | Each record is imported as its own domain command. **Imported payees start Unverified.** A recipient is "added" (REC-7) at import. An **account-claim protocol** (identity proofing plus cooling-off) applies before a migrated user controls a fund. Email ownership alone is insufficient. | TVF-208, TVF-217 |
| B8 | SM-6, TVCTL-09 | At release, the payment gate verifies the grant's **decision input snapshot** against the policy version history and the standing-data change history. A decision made under a policy or payee version that was later reverted opens a case. This catches edit-then-revert. | TVF-209 |
| B9 | §3 | **Third-party `Blocked`** (intermediary bank or provider blocks funds): a blocked receivable, no re-payment, sanctions officer case. | TVF-210 |
| B10 | Alternative 2D | Plan items are confirmed **when they are cleared**. Re-confirmation at execution is risk-based (B2 novelty, amount). Plan expiry is visible to the donor ahead of time, which avoids re-creating a December confirmation surge. | TVF-211 |
| B11 | Vendor | The sponsor holds the **verified bank data itself** and can move it, in addition to provider tokens. Exit from a provider must not require collecting every charity's details again. | TVF-212 |
| B12 | New CW-45 | **Sponsor bank failure** workflow: limits on uninsured balances, at least two banks, contingency for outstanding checks. | TVF-213 |
| B13 | INV-A, TVCTL-05 | **Typed agent outcomes:** only `Result(valid)` counts. Refusal, filtered output, timeout, schema failure and cost-ceiling stop all invoke the deterministic fallback. None of them means "no risk found". | TVF-214 |
| B14 | Vendor | Model-provider contracts include a **version availability horizon** and change-freeze windows covering year-end. | TVF-215 |
| B15 | PA-6 | Evidence sources are graded. Unauthenticated or single-source settlement claims open a **triage** queue, not an automatic block. A bulk triage procedure (dual control, sampling) covers provider-wide anomalies. | TVF-218 |
| B16 | PA-8 | An **in-transit exposure cap per provider**, tied to reserves and insurance (OD-20). | TVF-220 |
| B17 | TVCTL-09 | Delegation resolutions are attested by the corporate secretary, with a signed copy held outside the platform's administrative domain. | TVF-221 |
| B18 | §3, WF-10 | **Per-payment destination confirmation.** Where the destination is a provider-held token, the provider returns a destination fingerprint (account fingerprint or name-match result) with each payment. It is compared against the sponsor-held verified data (B11). A mismatch blocks the payment. Provider-side account changes are otherwise invisible to the sponsor. | TVF-222 (sev 5) |
| B19 | OD-22 | **External registers** are in scope: custodian asset movements are matched daily to authorized trade or transfer commands; identity-provider administrative actions (factor enrolment, admin grants) are matched to authorized changes; bank-portal entitlements are reviewed. An unmatched movement is an incident. | TVF-223 (sev 5) |
| B20 | AUTH-I7 | A **synced passkey** alone is not sufficient for new-recipient confirmation. A device-bound factor, or confirmation through a sponsor-direct channel, is required. Cloud-account takeover creates no credential-change event. | TVF-224 |
| B21 | SoD | **Agents never fill either side of a separation-of-duties pair.** An agent draft does not count as the "author". The human who accepts the draft is the author, so they cannot also publish. | TVF-225 |

## C. What remains after revision 3 (round-3 judgement)

- **Grant and payment lifecycle.** Round 3 found no new severity-4 or 5 issue. The remaining work is editorial: fold A1–A23 into the base documents. This lifecycle is classified as **approaching saturation**, pending a confirmation round after the fold-in.
- **Security and cross-domain chains.** **Not saturated.** Round 3 produced two severity-5 paths (B18, B19). The new findings come from:
  - restore and recovery;
  - external registers;
  - third parties' own failures;
  - control parameters an attacker can wait out.

  A targeted round 4 was run on these areas ([scenario library §4](../11-scenarios/scenario-library.md#4-saturation-tracking)).

## D. Round-4 findings: open, revision 4 not drafted

Round 4 (TVS-701..747; findings TVF-226..254; 1 at severity 5, 12 at severity 4) found new paths in **seven revision-3 amendments**:

| Amendment | Problem found | Finding |
|---|---|---|
| B6 | Its break-glass conflicts with OD-22 | M-3 |
| B6 | The consistent restore point can erase evidence | M-5 |
| B6 | Re-derivation breaks B19 matching | M-1 |
| B18 | A provider-computed fingerprint fails when the provider itself is compromised | M-9 |
| B18 | Resolving a mismatch with the provider's value undoes the control | M-25 |
| A12 | Observations recorded under an untrusted clock | M-17 |
| B5 | Year-end cross-tenant hold flooding | M-23 |
| B7 + B11 | Re-enrolment phishing recreated | M-19 |
| B13 | A requester can steer the agent into the weaker fallback | M-20 |
| A6 | Fixed-later amounts skip their thresholds | M-27 |

The severity-5 finding is **M-8 (TVF-233)**: B19 matching must compare the **destination**, not only amount and date. Custodian and bank settlement instructions, and pending custodian instructions, are registers in their own right.

These are **not** converted into amendments. [Scenario library §3.3](../11-scenarios/scenario-library.md#33-security-and-external-dependencies-not-saturated-and-not-converging-under-theoretical-rounds) explains why theoretical expansion stops here. The proposed requirements are in each finding's `evidence` field in the [findings register](../16-registers/findings.csv). They should be drafted **together with** real provider, custodian and bank capability evidence.
