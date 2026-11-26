# 07 - Payment Network Landscape: Build, Buy or Partner

Status: research draft (2026-11-26). Not legal advice. Evidence classes per 01-research-methodology.md.

Track A5. Agent PAY. Data: [data/payment-provider-matrix.csv](data/payment-provider-matrix.csv) (29 providers × 19 attributes), sources [data/sources-PAY.csv](data/sources-PAY.csv) (PAY-001..039). This note builds on [research/daf-grant-tracking-payment-rails-comparison-2026-11-11.md](../../daf-grant-tracking-payment-rails-comparison-2026-11-11.md), [research/ren-tifin-chariot-deep-dive-2026-11-11.md](../../ren-tifin-chariot-deep-dive-2026-11-11.md), [research/challenger-economics-daffy-chariot-charityvest-2026-11-12.md](../../challenger-economics-daffy-chariot-charityvest-2026-11-12.md) and the payment-rails queue work in `research/mission-2026-11-14/` (queue-payment-rails-cluster.md, queue-infrastructure-nonprofit-costs-emerging.md, b49-04-fraud-diversion-controls.md). It does not repeat their findings.

## Summary

- **The Release 1 decision holds, with one change to how it is worded.** CNV-PAY-001 chose networked rail partners acting as the sponsor's agent, with sponsor-originated ACH as fallback. That fits CNV-LEG-001: no option reviewed needs Unbound to hold funds. The change: the market's "networked partners" are three structurally different things, and only one of them can act as the sponsor's agent for a DAF grant (RECOMMENDATION, High):
  - **Partner-account rails.** The charity holds a receiving account at the partner: a Chariot Deposit Account at Column N.A., or a PayPal Confirmed Charity account. These are usable as agent rails.
  - **Pass-through intermediary charities.** PayPal Giving Fund, Benevity's foundations, Bonterra CGDS/CAF America, For Good, Every.org, Pledge and Goodstack's foundations. Legally, the grant is made to the intermediary, which then regrants. That breaks CNV-GRT-003 (grant to the listed legal name). These are **not** agent rails. CAF America stays relevant only for deferred international grants (CNV-GRT-008).
  - **Money-movement infrastructure with no charity network.** Bank APIs, Modern Treasury, Increase, Column, Dwolla, Moov. These are the substrate for the sponsor-originated ACH fallback, not a network.
- **Which partners.** Chariot Disbursements first, then PayPal Grant Payments, matching the order in CNV-PAY-007 (RECOMMENDATION, Medium-High).
  - **Chariot** is the only partner with a public, implementation-grade grantmaker API [PAY-001, PAY-002]. That API covers bulk create, approve, cancel, stop-payment, verification requests, webhooks, just-in-time funding with earmarks, and a sandbox.
  - **Chariot keeps funds in transit in the sponsor's own deposit account.** The grantmaker opens and funds a Chariot Deposit Account at Column N.A. [PAY-001, PAY-010, PAY-014]. This meets CNV-PLT-012's "segregated holding of sponsor funds in transit" without Unbound touching money (INFERENCE, High).
  - **PayPal Grant Payments** has the larger claimed charity base: more than 200,000 confirmed charities, a 2022 claim [PAY-017]. Vanguard Charitable and NPT use it. But it has no public grantmaker API, and its funding and holding terms are not public. It cannot pass the CNV-PLT-012 activation gate until those terms are seen (INFERENCE, High).
- **Nobody publishes verified-destination coverage.** Chariot does not publish its number of claimed accounts. PayPal's 200,000 figure is from 2022. Fidelity publishes only its own EFT share (67% of grants) [repo]. Do not read "supports ACH" or "has a nonprofit directory" as "has a reusable verified-destination network" (VERIFIED-FACT on absence from public sources, High).
- **Lock-in sits on the charity side, and it is strong.**
  - A Chariot recipient *must* receive into a Chariot Deposit Account ("you cannot 'bring your own' bank account") [PAY-006]. It reconciles inside Chariot, and sweeps to its own bank in 2-3 business days [PAY-012].
  - Chariot verifies the officer's identity, not the charity's external bank account, as the basis for electronic payment [PAY-003, PAY-007]. The enrolment is therefore not a portable verified-destination asset.
  - The same applies to PayPal accounts and to Ren for Charities enrolments, which are tied to Ren's own rail (RDE) [repo b49-04].
- **One lock-in exit for sponsors.** A claimed Chariot account has a non-debitable account and routing number. Chariot says the account exists so that payers who require a bank account legally owned by the nonprofit can pay it [PAY-006, PAY-007]. So a sponsor can pay a Chariot-enrolled charity by its *own* sponsor-originated ACH, to that charity's Chariot account, without a Chariot contract. The cost: the grant data does not reach the charity's Chariot dashboard (INFERENCE, Medium). This caps Chariot's pricing power over sponsors. It does not reduce the charity's lock-in.
- **Bank-account verification is cheap and plentiful, but it is per-inquirer.**
  - Plaid Identity Match [PAY-025], EWS Account Ownership Authentication [PAY-028, PAY-029] and Phixius by Nacha [PAY-027] all return per-inquiry results.
  - None of them offers a credential that the charity holds and can reuse across independent sponsors. W3C VC 2.0 [PAY-034] makes such a credential *possible*, but no bank or verifier issues one for charity accounts (VERIFIED-FACT on what is documented, Medium).
  - Unbound's portable asset is therefore **sponsor-scoped destination evidence that the charity authorizes for reuse**. Doc 08 designs it.
- **Nacha 2026 fraud monitoring raises the bar on every rail.** Phase 2 took effect June 19, 2026 (operationally Monday June 22, 2026). It requires Originators, TPSPs and Third-Party Senders to run risk-based processes to identify entries "authorized under False Pretenses" [PAY-026]. Nacha defines this to include misrepresenting ownership of the account to be credited (paraphrase of the rule page). So destination verification on grant *credits* is now a TPSP rule obligation, not only good practice. The WEB debit account-validation rule [PAY-039] covers consumer debits, not grant credits, and does not apply to release 1 (CNV-PAY-005: no donor debits) (VERIFIED-FACT for Phase 2, High).
- **Recommended shape: build the evidence and routing layer, buy verification signals, partner for rails.**
  - Build: a provider-neutral PaymentInstruction contract (UNB-PAY-002), a sponsor-scoped DestinationRegistry, and a routing policy.
  - Buy: owner-match signals from EWS, Plaid or Phixius, with two or more vendors behind one port.
  - Partner: Chariot and later PayPal, under the sponsor's agreement, plus the sponsor's ODFI for fallback ACH.
  - Building a proprietary money-moving network is excluded by CNV-LEG-001. It also has no economic case at the entry segment's scale (INFERENCE, Medium).

## 1. What "network" means here: five layers that vendors bundle

Each claim of "N nonprofits in our network" needs to be split into these layers. A vendor can be strong in one and absent in another.

| Layer | Question | Who can own it under CNV-LEG-001 |
|---|---|---|
| L1 Eligibility | Is the organisation an eligible grantee right now? (BMF, Pub 78, revocation, OFAC) | Unbound (UNB-CHAR-DEC-001 first-party registry); partners run their own checks too [PAY-011] |
| L2 Organisation control | Is the person acting entitled to act for the charity? | Unbound (identity proofing at CAL3, CNV-PLT-003), or the partner |
| L3 Destination ownership | Does this account belong to this charity? | A bank-originated owner match, or the partner's bank (a CIP-opened account) |
| L4 Money movement | Who originates, who holds funds in transit, who settles? | The sponsor's ODFI, or the partner and its bank. **Never Unbound** |
| L5 Remittance and reconciliation | Can the charity match money to grant, fund and restriction? | Shared: Unbound produces the advice (UNB-PAY-009); the partner or bank carries it |

Chariot bundles L1-L5 inside its own account. PayPal bundles L2-L5. Bank-verification vendors provide L3 only. Modern Treasury-type tools provide L4 and L5 over the sponsor's bank. A sponsor-agent design lets Unbound own L1, L2 and L5 and the *evidence* for L3, while L4 always belongs to a regulated party chosen by the sponsor (INFERENCE, High).

## 2. Landscape by category

Full attributes are in the matrix CSV. The decision-relevant points:

### 2.1 Partner-account rails (usable as sponsor's agent)

**Chariot Disbursements** (VERIFIED-FACT from vendor docs, High unless noted)

- **Funding and holding.** The grantmaker "open[s] a Chariot Deposit Account" and funds it by ACH credit, or by on-demand or just-in-time ACH debit of a linked account [PAY-001, PAY-002, PAY-010].
  - **Earmarks.** Without earmarks the balance is "one shared pool". Earmarks reserve each JIT transfer for its own disbursement [PAY-002].
  - **Partner choice.** Column N.A. holds the deposit, and Chariot is "Servicer". The bank may "refuse or restrict withdrawals and transfers ... in our sole discretion" [PAY-014].
  - **Deposit insurance.** Chariot says Chariot Deposit Accounts are "eligible for FDIC insurance up to $250,000 per depositor, for each insurance capacity in which the account is held" [PAY-006].
  - **Implication for CNV-PLT-012 [INFERENCE]:** a sponsor's balance at Column above $250k is uninsured bank exposure. The exposure limit should be set with that in mind, and JIT with earmarks keeps float near zero.
- **Lifecycle.** Statuses run `pending_approval → awaiting_verification → validating_organization → awaiting_account_claim → awaiting_balance → submitted → completed | failed`, plus `canceled`, `rejected` and `stopped` [PAY-002].
  - These map one-to-one onto the separate events required by UNB-PAY-001.
  - Once `submitted`, a disbursement can no longer be cancelled, only stopped where the rail allows. Unbound's dispatch fence must treat `submitted` as "acknowledged by partner" for CNV-PLT-012 failover (INFERENCE).
- **Delivery.**
  - In-network transfers "settle instantly", 24x7. ACH is "typically 1-2 days" [PAY-002].
  - An unclaimed charity gets an email and has 5 business days to claim, with three reminder emails. After that it gets a check to "the most current validated address" with the sponsor's grant letter [PAY-008, PAY-009]. Check delays run "~2-3 week[s]" [PAY-005].
  - Chariot handles address sourcing, returned checks and positive pay on the check path [PAY-003, PAY-009].
- **Verification.**
  - Eligibility requires BMF and Pub 78 listing. Private non-operating foundation codes are excluded. OFAC screening and continuous monitoring apply [PAY-011].
  - A Control Person verifies identity, including SSN, through Footprint [PAY-005, PAY-007].
  - Chariot states the design choice plainly: "Instead of simply validating payment pointers ... Chariot focuses on validating officer identities" [PAY-003].
- **API controls a sponsor needs.**
  - Approve and bulk-approve. This keeps the sponsor's release authority with the sponsor, per CNV-LEG-001.
  - `bypass_chariot_organization_verification`. This lets Unbound's L1 decision govern; use it only under sponsor policy [PAY-001].
  - Verification-request webhooks [PAY-004].
  - Idempotency keys and a status query for unknown outcomes (CNV-PAY-004): **not confirmed in the pages read**. Treat as an activation-gate question.
- **Price.** The grantmaker pays "a transaction fee"; the nonprofit pays nothing to receive [PAY-004]. The amount is not public: the deposit agreement's fee exhibit is an image that could not be read [PAY-014].
- **Charity-side lock-in.**
  - The charity cannot bring its own account [PAY-006] and is told to reconcile against Chariot, not its bank [PAY-012].
  - Moving funds to its own bank takes 2-3 business days, and weekly auto-transfer is a paid feature [PAY-012].
  - "Instant" therefore means in-network availability, not arrival in the operating account. This repeats the repo's earlier caution.
- **Channel conflict (INFERENCE, Medium).** Chariot also sells to nonprofits: DAFpay at a default 2.9% (challenger-economics file) and gift-processing subscriptions. Its claim emails create a nonprofit relationship that Chariot can monetise. That gives it no reason to make enrolments portable.

**PayPal Grant Payments** (VENDOR-CLAIM / VERIFIED-FACT on help page, Medium)

- **Eligibility.** Any PayPal-confirmed US charity can receive; acceptance is per grant [PAY-016]. The grantmaker sets each grant's expiry; NPT uses 14 days, then a check (repo).
- **No public grantmaker API.** Grantmakers onboard by contacting PayPal [PAY-016, PAY-017].
- **Unknown terms that matter to Unbound:**
  - where sponsor funds sit between release and acceptance;
  - whether PayPal is the sponsor's agent or the payer;
  - who the Originator is;
  - what status query exists;
  - PayPal's controls on changes to a charity's PayPal account. The repo found these pages returned 403; this session hit bot protection on the confirmed-charity terms [PAY-019].
- **Use.** Second adapter, gated on contract review. Its value is reach into charities already enrolled for Vanguard and NPT. That reach is the basis of CNV-EXP-002's promise not to ask such charities to re-enrol.

### 2.2 Pass-through intermediaries (not agent rails)

PayPal Giving Fund [PAY-018], Benevity's foundations [PAY-020], Bonterra CGDS with CAF and CAF America [PAY-021], For Good [PAY-022], Every.org, Pledge [PAY-035] and Goodstack's foundations (repo) all share the same model: **the money is a grant to the intermediary charity**, which then regrants. Some are described as able to redirect funds to an alternate cause [PAY-020].

For a DAF sponsor:
- the grantee of record becomes the intermediary;
- the sponsor's Schedule I, its CNV-GRT-003 checks and the donor's recommendation stop describing the actual end recipient;
- the intermediary's variance power interposes a second charity's discretion.

These platforms are fundraising and corporate-giving rails. They are not ways to deliver a DAF grant as the sponsor's agent (INFERENCE, High). Exclude them from the release-1 rail list. Treat CAF America-type intermediaries only under the deferred CNV-GRT-008 framework.

### 2.3 Money movement without a network (fallback substrate)

- **Sponsor-originated ACH through the sponsor's own ODFI.** This is the CNV-PAY-001 fallback. An orchestration layer such as Modern Treasury sits "on top of your existing bank accounts". Its terms say it "is not a bank and does not hold funds" [PAY-024].
  - Its counterparty verification uses prenotes, micro-deposits or Plaid, and is "purely for informational purposes" [PAY-023].
  - So it gives no owner-name match. CNV-PAY-002(a) still needs a separate owner-match vendor (VERIFIED-FACT, Medium).
  - The site also advertises an application for a national trust bank charter [PAY-024]. If granted, that would change its role; re-check it at selection.
- **BaaS platforms.**
  - Increase offers accounts at partner banks [PAY-030]. Column is a bank. Dwolla holds balances in "pooled holding accounts" at Veridian Credit Union, or in a KeyBank FBO subaccount [PAY-031]. Moov uses a Veridian concentration account [PAY-032].
  - Any of them would put sponsor money into a new account structure. Pooled or FBO balances conflict with CNV-PLT-012's segregation requirement unless the accounts are sponsor-titled (INFERENCE, Medium).
  - They add nothing that a sponsor's own bank does not, except API ergonomics. **Not recommended for release 1** beyond what Chariot already uses (Column).
- **Custodian disbursement.** Paying directly from sponsor custody accounts at Fidelity, Schwab or Pershing under standing letters of authorization is mechanically possible. It is governed by custodian procedures and, for advisers, by the SEC's 2017 SLOA no-action conditions [PAY-033].
  - Custodians verify the *instruction*, not the charity's account ownership. There is no charity network.
  - Use it only as a sponsor treasury choice for funding, not as a grant rail (INFERENCE, Medium). See also `unbound/requirements/integrations/CUSTODIAN-AND-INVESTMENT-MANAGEMENT.md`.

### 2.4 Destination-verification signals (buy, behind one port)

| Signal | Charity effort | Business names | Reuse across sponsors | Fit to CNV-PAY-002(a) "bank-originated account-owner match" |
|---|---|---|---|---|
| EWS Account Ownership Authentication / Verify Account (direct or via resellers) | None: the payer submits account, routing and business name | Yes; Positive/Conditional/Negative [PAY-028] | No (per inquiry) | **Best fit.** Bank-contributed data; coverage by participating bank not public |
| Phixius by Nacha (multi-responder incl. Kinexys, ValidiFI) | None | Not documented [PAY-027] | No | Possible; owner-match semantics not public. Validate before reliance |
| Plaid Auth + Identity Match | Charity logs into its bank | Yes [PAY-025] | No (per client/Item) | Good. Bank-held owner data; adds a login step |
| Mastercard/Finicity AOV, MX, Trustly | Bank login | Not checked | No | Comparable to Plaid; not assessed in depth [PAY-037] |
| Micro-deposits / prenote | Charity reads amounts / none | No | No | **Not** owner evidence; proves reachability only [PAY-023] |
| Partner CIP-opened account (Chariot/Column) | Full KYC of the officer | n/a | Within that partner only | Not literally "bank-originated owner match". **See conflict C1** |

**RECOMMENDATION.**
- Implement an `OwnershipSignalPort` with at least two adapters: an EWS-family adapter (no charity effort) and a bank-login adapter (Plaid-class) as fallback for Conditional or No-data results.
- Record the vendor, the response code, the match fields and the request hash as `DestinationEvidence`. Never record a pass/fail boolean alone.
- This keeps Unbound off any single verification vendor and satisfies the Nacha false-pretenses expectation as a documented, risk-based process [PAY-026].

### 2.5 Portable credentials

W3C VC 2.0 is a Recommendation family, including Bitstring Status List for revocation [PAY-034].

- **What a credential could carry.** A "bank-account-ownership" VC issued by the charity's bank, or by a verifier the sponsors trust, would let a charity show one credential to many sponsors.
- **What is missing.** No US bank or verification network was found issuing such credentials for nonprofits (absence of evidence, Medium).
- **Recommendation.** Design `DestinationEvidence` so it *can* be exported as a VC-shaped, signed, revocable attestation, with Unbound as the attesting verifier. Do not depend on one. Reliance by another sponsor stays governed by CNV-PAY-002's written reliance policy and CNV-GRT-004 (cross-sponsor evidence used as input only).

## 3. Customer-authorised migration of existing payment information

This is the CNV-EXP-002 "no re-enrolment" question, extended to sponsor-held bank records.

| Source of record | Who controls the data | Can it move to Unbound? | Evidence status on arrival |
|---|---|---|---|
| Sponsor's own ACH vendor-master (forms, voided checks, callbacks) kept by the sponsor or in its administrator's database as sponsor records | Sponsor (data owner) | Yes, under the sponsor's instruction. Predecessor contract data-return terms decide the mechanics; Ren's public MSA returns only "Customer Materials" and does not expressly require export of bank confirmations or payment instructions (`research/ren-legal-entities-public-msa-contract-portability-audit-2026-11-12.md`) | `LegacyImported`: provenance known, verification method often unknown |
| Ren for Charities enrolment (charity-provided via Ren's portal, Plaid link or manual review) | Probably Ren under its charity terms (ASSUMPTION; terms not read) | Only with the charity's authorisation or Ren's cooperation | Ren's checks are documented (postcard, 990 phone call, officer ID, check code) but are not Unbound evidence |
| Partner enrolments (Chariot, PayPal) | Charity plus partner | **No need to move.** Route through the partner if the sponsor contracts it (CNV-EXP-002) | Partner-held |

Nacha has no rule against a sponsor carrying its payees' account numbers to a new TPSP. The Originator remains responsible, and the new fraud-monitoring rule applies to the first entry after migration [PAY-026] (INFERENCE, Medium). Proposed handling:

1. **Import as `LegacyImported`.** Fields: `predecessor`, `predecessor_record_id`, `last_successful_credit_date`, `returns_history`, `predecessor_evidence_type` (if exported), `imported_at`, `sponsor_attestation_ref`.
2. **Bulk re-validate before the first Unbound-instructed payment.**
   - Run an EWS-class owner match against the BMF legal name, with no charity effort.
   - Positive → `Verified(owner_match)`, with the CNV-PAY-002 dual-channel notice. Cooling-off is waived only if the sponsor's reliance policy says a continuing, unchanged destination is not a "change" (**conflict C2**).
   - Conditional or no data → invite the charity through the doc 08 flow while paying by the predecessor's rail, or by check, in the meantime.
3. **Supporting evidence only.** A history of credits with no returns proves reachability, not ownership. Never treat it as sufficient alone.

## 4. Build vs buy vs partner

| Option | CNV-LEG-001 | Coverage on day 1 | Unit cost to sponsor | Lock-in | Verdict |
|---|---|---|---|---|---|
| A. Proprietary money-moving charity network (Unbound-held accounts or FBO) | **Violates** (holds funds) | 0 | High (licensing, BSA/AML, MTL) | n/a | Excluded |
| B. Single partner (Chariot only) | OK: sponsor-titled Column DDA | Chariot claimed base (unknown) plus check fallback | Partner fee (unknown) | Sponsor medium; charity high | Fast start, but recreates the Ren-style dependency one layer down |
| C. Sponsor-originated ACH only, with Unbound evidence layer | OK: sponsor ODFI | 0 enrolled; grows per doc 08 | Bank per-item plus verification calls; sponsor bears fraud loss | Low | Necessary fallback; slow alone |
| **D. Multi-rail abstraction: Unbound evidence/routing layer + Chariot (first) + PayPal (second) + sponsor ACH + check** | OK | Union of partner bases plus Unbound-verified destinations | Mixed; routing can choose the cheapest eligible rail | Low for sponsor; per-rail for charity | **Recommended** |

**Option D design rules (RECOMMENDATION).**

- **R1. One instruction, many rails.** A `PaymentInstruction` (UNB-PAY-002) carries `rail_candidates[]`, ordered by sponsor routing policy. `RailAdapter` implementations: `ChariotAdapter`, `PayPalGrantAdapter`, `SponsorAchAdapter` (bank API or NACHA file), `CheckAdapter` (positive pay), `SimulatedAdapter` (UNB-PAY-007).
- **R2. Rail selection at release, deterministic and recorded.**
  1. A partner where the charity has an *active* enrolment, the sponsor has an executed agreement, and the partner contract meets the CNV-EXP-002 equivalent-control amendment.
  2. Else, an Unbound-held destination with `Verified` evidence authorised for this sponsor → `SponsorAchAdapter`.
  3. Else, a partner with a claim window, if the sponsor opts in (the charity is invited by the partner), *or* an Unbound invitation (doc 08). Never both for the same grant.
  4. Else, a check.
  Record the decision trace with its inputs, and keep AI out of this decision (CNV-AIO-001).
- **R3. Partner-status mirroring.** Store a `PartnerEnrolment {partner, partner_org_id, status, last_event_at, control_change_events[]}` per charity, refreshed by webhook or poll. Never store a partner's charity bank details; partners do not expose them.
- **R4. Exit test per partner.** Before activation, run a drill: disable the partner and confirm that every affected charity routes to rule 2 or 4 within one release cycle. Instructions with partner acknowledgment stay in CNV-PAY-004 handling (CNV-PLT-012 AC-2).
- **R5. Chariot-account-as-ACH-destination.** With charity authorisation, a Chariot Deposit Account number can be stored as an ordinary Unbound destination. Owner evidence comes from an EWS match against Column's data, or from the charity's attestation plus callback. This lets a sponsor leave Chariot without stranding Chariot-only charities (INFERENCE, Medium; confirm Column participates in an owner-match network).

**Where Unbound can actually compete (INFERENCE, Medium).** Incumbents hold enrolments inside their own rails: Ren's RDE, Fidelity's Stripe and ACH, Chariot's accounts. Unbound cannot win by owning money movement. It can win by:
- holding sponsor-scoped, *charity-authorised, re-verifiable* destination evidence that any rail can use;
- making enrolment a by-product of receiving a grant (doc 08);
- letting the sponsor change rails without the charity noticing.
That is a switching-cost advantage the sponsor keeps, not a network Unbound keeps.

## Implications for Unbound

1. **Keep CNV-PAY-001 and CNV-PAY-007 (Chariot first, PayPal second).** Add the partner-account / pass-through distinction so a pass-through intermediary can never be configured as a grant rail.
2. **Contract checklist for partner activation**, extending the CNV-PLT-012 gate:
   - funds in the sponsor-titled account, with the insurance ceiling stated;
   - an idempotency key and status query;
   - stop and cancel semantics;
   - control-person or owner-change events delivered to the sponsor before the next release;
   - fee schedule in text;
   - data export on termination;
   - Nacha role mapping (who is Originator, ODFI and TPS for each payment path, in-network book transfer included).
3. **Implement two or more owner-match vendors** behind one port, and log raw responses as evidence.
4. **Treat migration as re-verification,** not trust transfer (section 3).
5. **The economics are unknown.** No partner fee is public, so per-grant rail cost against the 20 bps working scenario cannot be computed yet. Obtain quotes under NDA outside this public corpus.

### Conflicts and refinements with ratified clauses (flagged, not resolved)

- **C1 - CNV-PAY-002 and its round-2 amendment** require "bank-originated account-owner match" or "charity document plus registry-sourced callback".
  - Partner-account rails (Chariot, PayPal) provide neither: the destination is an account the partner's bank opened under CIP.
  - The CNV-EXP-002 amendment lists the equivalent controls as owner verification, cooling-off and notice, and a destination-change event. These are written for bank-detail changes. For partner accounts the risk event is an *account-control* change (for example Chariot's "Transfer ownership" [PAY-013]), not a change of bank details.
  - **Proposed refinement:** add evidence class (c), "destination is an account at the partner bank opened in the charity's legal name under that bank's CIP". The equivalent-control test then maps "bank-detail change" to "account owner/admin change at the partner".
- **C2 - CNV-PAY-002 cooling-off "after any bank change".** It is ambiguous whether importing a predecessor's unchanged destination is a "change". Recommend that the sponsor reliance policy decide this explicitly.
- **C3 - CNV-PLT-012 "segregated holding of sponsor funds in transit".** Chariot meets it through a sponsor-titled DDA. Partners with pooled or FBO models would not. PayPal's model is unknown.

## Open questions / evidence gaps

- Chariot: the grantmaker fee schedule; idempotency and status-query guarantees; the number of claimed accounts; whether grantmakers receive owner or control change events; who is the Originator for ACH out of a grantmaker's Column account; SOC 1 scope.
- PayPal Grant Payments: grantmaker agreement, funding and holding, API availability, current confirmed-charity count, change controls (pages blocked).
- EWS AOA and Phixius: participating-bank coverage for *business* accounts at small banks and credit unions; whether Column is a responder.
- Measured claim and conversion rates for grant-triggered invitations: Chariot's 5-day window, Ren's check codes. None are published, and doc 08's model depends on them.
- Ren for Charities terms: who controls charity-provided bank data, and whether it can be ported with charity consent.
- Counsel: whether paying a Chariot account by sponsor ACH without a Chariot contract raises any Column or Chariot terms issue for the payer (none found; the deposit agreement binds the account holder).
