# 08 - Organic Network Growth: Enrollment as a By-product of Grant Processing

Status: research draft (2026-11-26). Not legal advice. Evidence classes per 01-research-methodology.md.

Track A6. Agent PAY. Model: [scripts/pay_enrollment_growth_model.py](scripts/pay_enrollment_growth_model.py) (stdlib, deterministic), output [data/pay-enrollment-growth-model.csv](data/pay-enrollment-growth-model.csv) (2,430 rows). Sources: [data/sources-PAY.csv](data/sources-PAY.csv). The rails and verification options are in [07-payment-network-landscape.md](07-payment-network-landscape.md). Fraud is covered here only at design level; the security track covers it in depth.

## Summary

- **Grant-triggered enrolment already exists, so it is not a differentiator by itself** (VERIFIED-FACT, High).
  - **Chariot.** Holds each grant to an unclaimed charity for 5 business days and sends three emails, then mails a check [PAY-008, PAY-009].
  - **Ren for Charities.** Lets a charity claim its profile with a registration code printed on a grant check. AEF announced QR codes on checks from Q2 2026 (repo: `research/mission-2026-11-14/b49-04-fraud-diversion-controls.md`, `queue-ren-iphi-attrition.md`).
  - **Fidelity.** Reached 67% of grants by EFT with sponsor-owned enrolment, without a hard mandate (repo).
- **Mostly parity, with a narrow differentiator** (revised after ADVA-15; RECOMMENDATION, Medium):
  1. *No software use for the charity* is **parity**: Fidelity's ACH pays the charity's own bank with no portal (repo).
  2. *One enrolment reused by many payers* is **parity**: Chariot ("claim ... one time" for all Disbursement partners), Ren ("validated once, trusted across the entire platform") and CAF America (validation reused for 1-3 years) all do it.
  3. *Partner-neutral routing* (honour an existing Chariot or PayPal enrolment, never force a partner account) is **parity-plus**. Nobody documents doing it across rails.
  - **Residual differentiator (HYPOTHESIS):** sponsor-held, rail-neutral, re-verifiable destination evidence plus deterministic decision replay, so that a sponsor can change rail or administrator without its charities noticing. Test it with sponsors before ranking it as an advantage.
- **Step counts** (INFERENCE from documented flows, Medium):
  - **Check, every grant:** about 7 charity steps and 1-3 weeks of mail and deposit delay.
  - **Partner deposit-account enrolment** (Chariot-style): about 8 one-time steps, including the officer's SSN identity verification, and 1-2 steps per grant (sweep and reconcile in the partner's dashboard).
  - **Proposed Unbound enrolment:** 5 one-time steps when an owner-match vendor confirms the bank account with no charity effort, 6-7 when a bank login or document is needed, and **0 steps per grant**.
  - **Charity already enrolled with a contracted partner:** 0 steps.
- **Growth model** (INFERENCE on ASSUMPTION parameters, Low-Medium). Inputs: the real FY2023 Schedule I recipient distribution of three advisor-distributed sponsors (AEF, Raymond James, T. Rowe Price) and AEF's 109,708 grants in 2024. Each grant to a non-enrolled charity carries one invitation.
  - **Dollars go electronic much faster than grant counts.** At 25% conversion per invitation, 69-92% of dollars are electronic after 12 months (range over the β and tail-share sensitivity grid), against 43-73% of grants.
  - **Time to 67% of grants electronic:** 9-26 months at p = 0.25; 23-65 months at p = 0.10; 6-17 months at p = 0.40 (ranges over the sensitivity grid).
  - **Partner pre-enrolment gives a head start, not a different endpoint.** At go-live it gives 8-21% of grants and 12-32% of dollars, and saves about 2-3 months at p = 0.25 (about 6 at p = 0.10). After 24-36 months the conversion rate dominates.
  - So the levers that matter are **friction per invitation** and **targeted outreach to the top ~1,000 recipients**. For AEF those recipients took 67% of itemised FY2023 dollars [computed from repo edges].
- **Calibration warning** (INFERENCE, Medium). Fidelity has offered EFT for years and is at 67% of grants. That implies a low effective conversion in practice, about p ≤ 0.10 per grant, or many charities that never convert. Plan on the p = 0.10 path and treat p = 0.25 as a target that must be earned by friction reduction and measured in a pilot.
- **The design must stay consistent with ratified controls.**
  - Bank-detail submission needs CAL3 authentication (CNV-PAY-002 amendment).
  - Callbacks go only to registry-sourced or long-verified contacts.
  - A cooling-off period applies before first use (UNB-RCN-WF-028; floor of 1 business day).
  - Bank details are sponsor-scoped and never in a shared store except as a keyed token (CNV-TEN-001).
  - "Passwordless" applies to *reading* and *acknowledging*. Changing where money goes always gets step-up.

## 1. Step-count comparison (charity's view)

The counts are of distinct actions a charity staff member must take. Waiting time is shown separately.

| Flow | One-time steps | Per-grant steps | Typical delay to usable funds | Source |
|---|---|---|---|---|
| **A. Mailed check** | 0 | 7: receive mail → open and match letter to donor/fund → endorse → deposit (mobile/branch/lockbox) → record in CRM → acknowledge donor if named → chase if lost or stale | Mail 3-5 days plus processing; check-paying DAFs averaged 7-162 days from initiation to payment in Chariot's one-recipient study | repo `queue-payment-rails-cluster.md` |
| **B. Partner deposit account (Chariot)** | ~8: open email → create login → claim org → control person identity verification incl. SSN → accept Column account terms → link external bank (owner-only; documents if the name does not match) → set auto-transfer (weekly only on paid plans) → add team users | 1-2: (sweep, unless automatic) → reconcile against Chariot, not the bank | In-network instant; to own bank 2-3 business days | [PAY-005, PAY-006, PAY-012] |
| **C. Partner PayPal Grant Payments** | ~4-6 if not already a confirmed charity: PayPal business account → charity confirmation (EIN, documents) → link bank | 2: accept grant in dashboard → withdraw | Within 1 day of acceptance; grants expire | [PAY-016] |
| **D. Sponsor-proprietary EFT (Fidelity ACH form)** | ~4: download form → attach voided check → board/officer signature → submit; queue up to 4 weeks | 0-1 (read notice) | 1-2 days after processing | repo |
| **E. Proposed Unbound grant-triggered enrolment** | **5** if EWS-class match is Positive: scan QR / open link → confirm org (prefilled) → passkey or emailed code to a registry-sourced contact → enter routing/account → sign authorisation (also the authorised-representative attestation). **+1-2** if a bank login (Plaid-class) or an officer identity check is needed for CAL3 | **0** (remittance by email/CSV; optional 1-click acknowledgement) | ACH 1-2 days after the cooling-off clears | design below |
| **F. Charity already enrolled with a contracted partner** | 0 | as B or C | as B or C | CNV-EXP-002 |

**Reading (INFERENCE).**
- Flow E beats B on one-time effort mainly because the charity keeps its own bank account: no SSN-based KYC of the officer, no second account, no sweep.
- E is roughly equal to Ren's code-on-check flow. The advantage is mostly per-grant (zero) and cross-sponsor (a second sponsor's request becomes one consent click, section 3.4).
- CAL3 identity proofing can erase the advantage if it always requires document-plus-selfie. Route most charities through the bank-originated owner match plus a registry-sourced contact. Use a document check only when that path fails.

## 2. Design: states, data, rules

### 2.1 Invitation

`EnrollmentInvitation`:
```
{ invitation_id (opaque, 128-bit),
  charity_registry_id, ein,
  sponsor_id, triggering_grant_id?,
  channel: Email | CheckStubQR | CheckStubCode | GrantLetterPDF | Outreach,
  contact_source: RegistryPublic(990|BMF|website, retrieved_at) | PriorVerified(record_id, verified_at),
  issued_at, expires_at (default 60 days), max_redemptions = 1,
  status: Issued | Opened | Redeemed | Expired | Revoked }
```

Rules:
1. **What the token is.** The QR or code encodes only `https://<sponsor-or-unbound-domain>/e/<invitation_id>`. There is no EIN, no amount and no donor in the URL.
2. **What the landing page shows before verification.** Only the charity's registry legal name and "a grant from <sponsor> is ready to be paid". It shows no amount and no donor. This limits phishing value and protects donor privacy (UNB-REM-013).
3. **The same code also works when typed in** at a published, stable URL. Correspondence tells charities never to follow a link to enter bank credentials. Bank login happens only inside the vetted aggregator widget.
4. **Email invitations go only to `contact_source` addresses** that are registry-public, or prior-verified at least 30 days before (CNV-PAY-002 amendment). They are never sent to an address supplied in a change request.
5. **One open invitation per charity per sponsor.** Further grants attach to the open invitation instead of creating new ones, so the charity is not spammed. Two sponsors on Unbound send one combined invitation per charity, listing both.

### 2.2 Enrolment state machine (per charity, sponsor-scoped evidence)

```
Invited → Opened → ControlAsserted → DestinationSubmitted → OwnershipChecked
      → CoolingOff → Active
Active → ChangeRequested → (OwnershipChecked → CoolingOff) → Active
any → Suspended (eligibility hold, sanctions, fraud signal) → prior state or Revoked
```

| State | Entry condition | Exit rule | Failure behaviour |
|---|---|---|---|
| ControlAsserted | Passwordless auth to a registry-sourced contact (magic link or OTP), then passkey enrolment | Representative attests authority (signature, title) | If no registry-sourced contact responds → `OfficerVerification` path (IDV vendor) or check fallback |
| DestinationSubmitted | Routing and account entered, or bank-login token | Raises CAL3 requirement (CNV-PAY-002 amendment) | Charity can save and return; the grant pays by check after the sponsor's hold window |
| OwnershipChecked | `OwnershipSignalPort` result vs registry legal name | Positive → CoolingOff. Conditional → bank-login or document plus callback. Negative → manual review | Never auto-reject on Conditional; never auto-accept on reachability (micro-deposit or prenote) alone |
| CoolingOff | Evidence complete | ≥ sponsor cooling-off (≥ 1 business day); notice sent to verified channels | Any contact or signatory change during cooling-off restarts it |
| Active | Cooling-off elapsed with no objection | Destination usable for this sponsor's releases | NOC C01-C03 → updated under CNV-PAY-002 NOC rule; R03/R04 return → Suspended + outreach |

### 2.3 Data structures

```
PaymentProfile            -- charity-controlled; lives in a charity-scoped store, not the cross-tenant registry
{ profile_id, charity_registry_id,
  representatives: [ {rep_id, name, title, auth_level (CAL2|CAL3), passkeys[], verified_via, verified_at, status} ],
  destinations:   [ {dest_id, kind: BankAccount | PartnerAccount(partner, partner_org_id),
                     bank_token (vault reference; no cleartext outside vault),
                     owner_evidence: [DestinationEvidence], status, created_at, superseded_by?} ],
  preferences: { preferred_rail: Direct | Partner(name) | Check, remittance: Email | CSV | API | None,
                 remittance_recipients[], acknowledge_mode: None | OneClick },
  sponsor_authorisations: [ {sponsor_id, dest_id, granted_by rep_id, granted_at, scope: payments,
                             revoked_at?} ] }

DestinationEvidence       -- append-only (Strata-style), per check
{ evidence_id, dest_id, method: OwnerMatch(vendor) | BankLogin(vendor) | PartnerCIP(partner)
                                | DocumentPlusCallback | NOC | LegacyImported(predecessor),
  request_hash, response_code, matched_fields, raw_response_ref, performed_at,
  performed_for_sponsor_id }

SponsorDestinationAcceptance   -- what CNV-PAY-002 actually tests at release
{ sponsor_id, dest_id, evidence_ids[], reliance_policy_version, cooling_off_until,
  notices_sent[], accepted_at, status }
```

Rules:
- **R-1. Destination evidence is per sponsor in Release 1 (revised after ADVA-13).**
  - Each sponsor's acceptance rests on evidence produced *for that sponsor*. When sponsor B is authorised by the charity to pay a destination first verified for sponsor A, B re-runs the owner-match call. The call costs the charity nothing.
  - The only things reused across sponsors in Release 1 are the charity's representative and control evidence and public facts: the authenticated representative, its passkeys, and registry data.
  - Reuse of *destination* evidence by sponsor B, as CNV-PAY-002 permits under a written reliance policy, is deferred. It needs three things first:
    - a measured friction benefit (the saving is small where the owner match needs no charity effort);
    - a written allocation of losses when B relies on A's evidence;
    - counsel's view on imputed awareness. Per the reviewer, Rev. Proc. 2018-32 §4.04(3) and §5.02(2) remove reliance where a grantor "was aware of" deficiencies. Shared evidence could widen awareness. This was not verified here.
- **R-2. Storage of bank numbers.** They are held only in a vault, with per-sponsor keyed access. The shared charity registry holds at most a keyed token, never the number (CNV-TEN-001, UNB-CHAR-029, UNB-CHAR-036).
- **R-3. Partner enrolment is recorded as `PartnerAccount`.** The status is mirrored from the partner, and no bank data is held. The routing rules are in 07 R2.
- **R-4. AI's role.** AI may draft outreach text. It never changes a destination, approves evidence or chooses a rail (CNV-AIO-001).

### 2.4 Self-service corrections and authorised representatives

- **Add a representative.** Invited by an existing CAL3 representative, or proven independently (officer identity check plus a registry-sourced callback). Every representative change notifies all other representatives and the registry-sourced contacts, and starts the CNV-PLT-011 72-hour contact-channel hold.
- **Bank change.** Always a step-up to CAL3. It creates a new `dest_id` and never edits the old one. It needs new evidence and cooling-off (CNV-PAY-002 AC-1, AC-6), and notice goes to the old and new verified channels. The old destination stays usable until the new one is Active, unless the charity reports compromise.
- **Address and contact correction.** Low-risk fields such as remittance email and mailing address for letters can change at CAL2, with notice. Any change used for a *callback* disqualifies that contact for 30 days.

### 2.5 Without a portal

- **Remittance.** Per payment: an email with grant ID, sponsor, fund name or "anonymous", purpose or restriction, amount and trace number. A signed CSV is available. The charity's CRM can pull via API at its own option.
- **Acknowledgement (optional).** A one-click signed link, "received and attributed", logged as `RecipientAcknowledgement`. Settlement evidence remains the system of record for payment completion (UNB-PAY-010).
- **Re-verification.** Every 24 months or on any registry event (name change, revocation, merger), the charity gets one email asking it to confirm. Silence never suspends a payment; only a verified negative fact does. This follows CNV-GRT-003: informational changes must not block payment.

## 3. Interaction with partners

| Situation at release | Action | Charity sees |
|---|---|---|
| Active partner enrolment, sponsor has partner contract meeting CNV-EXP-002 controls | Route to partner | Nothing new |
| Active Unbound destination authorised for this sponsor | Sponsor-originated ACH | Remittance email |
| Unbound destination exists but not authorised for this sponsor | One-click consent request ("allow <sponsor> to pay you at account ••1234?"). Release 1: a new owner match for this sponsor, then cooling-off and notice; evidence reuse deferred (R-1) | 1 step |
| Neither, and the sponsor prefers the partner's claim window | Partner invites (e.g. Chariot 5 days); Unbound sends no parallel invite | Partner email |
| Neither, and the sponsor prefers direct | Unbound invitation on the email and on the check stub; the check goes out on the sponsor's normal schedule (no hold by default) | QR on check |

**Enrol once with a partner, or with Unbound?**
- **Partner enrolment.** Reaches every grantmaker on that partner's network. It locks the charity into the partner's account and does not help sponsors outside the network.
- **Unbound-held evidence.** Reaches every Unbound sponsor the charity authorises (in Release 1 each sponsor re-runs the owner match), and any rail that pays a bank account, including a sponsor that later drops its partner (07 R5).
- **Recommendation.** Offer both and let the charity choose through `preferred_rail`. Default to the charity's existing partner enrolment where one exists.

## 4. Growth model

### 4.1 Method

- **Per-recipient enrolment probability.** For recipient r with grant rate λ_r, pre-enrolment probability e0_r and conversion probability p per invitation-bearing grant:
  - P_r(t) = 1 − (1 − e0_r)·exp(−p·λ_r·t).
  - Grant share electronic = Σλ_r·P_r / Σλ_r. Dollar share uses dollars in place of λ_r.
  - The model is closed-form and deterministic.
- **Recipients.** The real FY2023 Schedule I recipients of each sponsor, taken from the repo edges file (`data/workflow-innovation/sponsor-recipient-edges-fy2023.csv`).
- **Grant volume.** Total grants scaled from AEF's 109,708 grants (2024) per 12,491 itemised recipients [PAY-038].
- **Tail recipients** (un-itemised, ≤ $5k per sponsor) are added as an ASSUMPTION: 40/60/80% of grants go to itemised recipients, with 1.5 grants of $1,000 per tail recipient.
- **Grants per itemised recipient** ∝ dollars^β, with β ∈ {0.3, 0.5, 0.7} (ASSUMPTION).
- **Pre-enrolment** by the number of top-50 sponsors funding the recipient (ASSUMPTION, illustrative):
  - `one_partner`: 20% / 8% / 3% / 2% for ≥6 sponsors / 2-5 / 1 / tail;
  - `two_partners`: 45% / 20% / 8% / 5%.
- **Conversion p** ∈ {0.10, 0.25, 0.40} (ASSUMPTION; no published claim rates).

### 4.2 Results (AEF, base case: β = 0.5, 60% of grants to itemised recipients)

| Partner coverage | p | Grants elec. at go-live | At 12 mo (grants / $) | At 36 mo (grants / $) | Months to 50% / 67% / 80% of grants | Grants processed before 67% |
|---|---|---|---|---|---|---|
| none | 0.10 | 0% | 36% / 72% | 63% / 90% | 23 / 43 / 73 | ~393k |
| none | 0.25 | 0% | 58% / 88% | 85% / 97% | 9 / 18 / 30 | ~165k |
| none | 0.40 | 0% | 70% / 93% | 93% / 99% | 6 / 11 / 19 | ~101k |
| one_partner | 0.25 | 8% | 60% / 89% | 85% / 97% | 8 / 17 / 29 | ~155k |
| two_partners | 0.10 | 19% | 45% / 79% | 67% / 92% | 16 / 37 / 67 | ~338k |
| two_partners | 0.25 | 19% | 63% / 90% | 86% / 98% | 7 / 15 / 27 | ~137k |

- **Other sponsors.** Raymond James and T. Rowe Price follow almost the same grant-share paths. Their dollar shares are lower at 12 months: 61-83% at p = 0.10-0.25 with no partner, against AEF's 72-88%, because their dollars are less concentrated at the very top.
- **Sensitivity.** Across the full grid, months to 67% are 9-26 at p = 0.25 and 23-65 at p = 0.10 (CSV `row_type=threshold`).

### 4.3 What the model says to do (INFERENCE)

1. **Optimise conversion per invitation first.** Moving p from 0.10 to 0.25 cuts time-to-67% by about 25 months. Adding a second partner's pre-enrolled base cuts it by about 3-6. This supports the zero-portal, owner-match-first design (section 1).
2. **Do targeted outreach before go-live.** For AEF the top 1,000 recipients took 67% of itemised FY2023 dollars (Raymond James 68%, T. Rowe Price 88%). Recipients funded by ≥ 6 top-50 sponsors took 51-63% of these sponsors' dollars. A pre-launch outreach to the largest few hundred recipients moves the *dollar* share before any organic conversion. Many of them will also already be partner-enrolled (CNV-EXP-002).
3. **Checks never disappear.** At p = 0.10-0.25, about 15-37% of grant *count* is still paper after 3 years: tail recipients receive about one grant a year. Positive pay and CNV-PAY-002/003 check controls stay permanent.
4. **Measure p in the first sponsor's shadow period** (CNV-ECO-003) and re-run the model with the observed value. Do not market speed-to-electronic claims before that.
5. **Model p by mechanism, not as one number (ADVA-08).**
   - An opt-in form with a queue (Fidelity) supports p ≈ 0.10, the conservative planning case.
   - Hold-and-claim (Chariot's 5-day hold) is likely higher. Chariot's and TIFIN's vendor figures (94.57% of payments electronic; 82% of dollars electronic in TIFIN's first 4 months, reported in 03) are an upper bound with undisclosed bases.
   - Zero-effort owner match plus a code on the check is untested.
   - CNV-ECO-003's shadow replay should record conversion per mechanism.

## Implications for Unbound

- Building the invitation, the payment profile and the evidence registry is the right scope: thin, partner-neutral, and owned under the sponsor's data authority. Money movement stays with partners and banks (07).
- Parity features are required just to match Ren and Chariot: a code or QR on the check, an email claim window, address sourcing. Zero per-grant steps and no second bank account are also parity with Fidelity's ACH. Partner-neutral routing is parity-plus. The only candidate differentiator is sponsor-held, rail-neutral, re-verifiable evidence with decision replay, and that is a HYPOTHESIS (ADVA-15).
- **Candidate requirement refinements:**
  - (a) **CNV-PAY-002.** Separate `DestinationEvidence` from `SponsorDestinationAcceptance`. Both are per sponsor in Release 1; cross-sponsor reuse of destination evidence is deferred (R-1).
  - (b) **CNV-EXP-002.** Add the charity's `preferred_rail` and a no-parallel-invitation rule.
  - (c) **UNB-REM-013/UNB-REM-002.** Add zero-portal remittance and acknowledgement.
  - (d) **UNB-CHAR-029/CNV-TEN-001.** Keep the payment profile in a charity-scoped vault, outside the shared registry.

## Release 1 versus later (ADVA-20)

| Release 1 minimum | Later, each behind a stated gate |
|---|---|
| Registration code and QR on the check stub and in the email (parity with Ren and AEF) | Combined multi-sponsor invitations |
| Enrolment flow E with CAL3, an owner-match port (at least one vendor), cooling-off and notice per CNV-PAY-002 (c10) | A second owner-match vendor; bank-login fallback if the no-data rate is high |
| `DestinationEvidence` and `SponsorDestinationAcceptance`, per sponsor | Cross-sponsor reuse of destination evidence (R-1 gates) |
| Partner enrolment mirrored (Chariot), honoured only if the owner admits evidence class (c) (07 C1) | Charity `preferred_rail`; PayPal mirroring |
| Email and CSV remittance | One-click acknowledgement; CRM API; VC-shaped export of evidence |
| Targeted pre-launch outreach to the top few hundred recipients by dollars | Organic-growth optimisation beyond codes on checks; growth-model recalibration |

## Adversarial review response

| Finding | Verdict here | Change made |
|---|---|---|
| ADVA-15: "differentiators" are mostly parity | **Accepted** | Summary rewritten into parity, parity-plus and one residual HYPOTHESIS. The Implications bullet amended |
| ADVA-13: cross-sponsor destination evidence adds risk for little benefit | **Accepted for Release 1** | R-1 and the routing table revised. Reuse deferred behind three gates (benefit, loss allocation, counsel on Rev. Proc. 2018-32 imputation) |
| ADVA-20: no Release 1 split | **Accepted** | Release 1 versus later table added |
| ADVA-08: one p across mechanisms | **Partly accepted** | Per-mechanism modelling added to 4.3. p = 0.10 kept as the conservative case. The script is unchanged; a mechanism-specific rerun waits on measured inputs |
| ADVA-07: ECO's partner coverage (0.3-0.7) conflicts with this model (2-45% tiers) | **Agree with reviewer.** Fidelity's EFT is proprietary and not reusable under CNV-EXP-002. Under 07 C1, even Chariot and PayPal enrolments may not count until the owner admits class (c) | None here. The correction belongs in 20 (ECO) |

## Open questions / evidence gaps

- **Conversion rates.** Real claim rates for Chariot's 5-day window, Ren's check codes and Fidelity's outreach are not public. They are the model's dominant parameter.
- **Grant-count distribution per recipient** for any entry-segment sponsor. Schedule I gives dollars per recipient, not grant counts, so β and the tail share are assumptions.
- **CAL3 cost.** Can a bank-originated owner match plus a registry-sourced contact satisfy CAL3 for a charity representative, or is officer document identity proofing always required? This is a security-track question, and it decides whether flow E takes 5 steps or 7.
- **Charity attitudes.** Willingness to grant cross-sponsor reliance, and board policies that forbid EFT (Fidelity asks charities to change such policies; repo). A charity interview round is needed.
- **QR-on-check phishing.** Fake QR codes on stolen or forged checks are a known pattern. Mitigation design (a domain shown in the letter, typed codes, no credentials on the landing page) needs security-track review.
