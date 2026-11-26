# 09 - Charity network security: adversarial analysis and controls

Status: research draft (2026-11-26). Not legal advice. Evidence classes per 01-research-methodology.md.

Scope: Track A7 (security of a shared charity directory, shared vetting and electronic charity payment network) and the security parts of Track B (onboarding, migration, insider risk). Companion data: [`data/charity-network-threat-model.csv`](data/charity-network-threat-model.csv) (22 threats, T01-T22) and [`data/sources-SEC.csv`](data/sources-SEC.csv) (SEC-001 to SEC-019).

## Summary

- **The dominant loss mechanism is bank-detail substitution, not fake charities.** Documented grant losses follow one pattern: someone gets into a real grantee's email or portal login and changes the bank account. Two examples are the Margaret A. Cargill Foundation's $1m first payment in 2023 [SEC-010] and the One Treasure Island $650k wire [SEC-011]. The Commerce OIG alert of July 2026 describes the same pattern against federal grantees [SEC-009]. VERIFIED-FACT, High. Fake-charity fraud also exists but is smaller in the federal data: IC3 counts 662 "Charity" complaints and $7.9m in 2025, against $3.05bn of BEC losses [SEC-006, SEC-018]. VERIFIED-FACT, High.
- **The 2026 Nacha rules now cover an Unbound-type TPSP.** Phase 2 took effect on 19 June 2026 (practical date 22 June). It requires "each Third-Party Service Provider" to run risk-based processes that identify entries "authorized under False Pretenses", and to review them at least annually [SEC-001]. The definition of False Pretenses explicitly includes misrepresenting "the ownership of an account to be credited" [SEC-002]. The rule facts are VERIFIED-FACT, High. That they apply to Unbound is an INFERENCE from CNV-PAY-001, Medium, and needs counsel review. Destination-change controls are therefore a compliance duty, not only a product feature.
- **Shared verification creates correlated, systemic risk.** If one verified destination is reused by k sponsors, one successful deception exposes the pending grants of all k sponsors. Without sharing, an attacker must defeat k separate checks. INFERENCE, High. Sharing can be bounded (§5) with five controls: per-sponsor opt-in, reuse as input only (CNV-GRT-003), a network-wide exposure cap while a new destination is on probation, a first-payment cap per sponsor, and confirmation of receipt by the charity before the probation ends.
- **The callback is only as strong as the contact it dials, and the shared registry is where that contact lives.** UNB-UI-P-005 already requires the callback to use a contact from the registry, never one supplied in the change request. However, nothing stops an attacker from first changing the registry contact (by takeover, a directory submission or an IRS-of-record change) and then requesting the bank change. **Gap.** RECOMMENDATION: apply contact-age and contact-change holds to charity principals, extending CNV-PLT-011, which today covers donors only (PROP-SEC-02).
- **No verification method proves both ownership and authority.**
  - Micro-entries prove that the *submitter can see* an account, which a mule account also passes [SEC-003].
  - Instant account verification proves the submitter holds the bank login.
  - A bank-originated owner match (e.g. EWS Verify Account, which returns an "ownership match result" [SEC-005]) proves *whose* account it is, but not that the requester is authorized to act.
  - INFERENCE, High. Destination evidence must therefore combine ownership evidence, authority evidence (a callback to an independently sourced, aged contact), time (a cooling period plus notice to the old channel) and an exposure limit. The existing UNB-RCN-GRT-017 table supports this. The tiering in §4 makes it concrete.
- **Existing requirements are strong on single-sponsor destination change and weak at network level.** WFM-13, RR-REQ-X-005-r1, UNB-RCN-GRT-017, UNB-UI-P-005 and UNB-UI-S-056 already cover these controls:
  - requester ≠ verifier;
  - a callback to a registry-sourced contact;
  - a 3-business-day pending activation;
  - payments continuing to the old destination while a change is pending;
  - no bulk verification of imported payees.

  Missing: network exposure caps, receipt confirmation, provenance rules for writing payment-relevant fields in the shared registry, integrity gates for source feeds, chain of custody for migration files, and attestation of controls at partner enrolments. INFERENCE, High.
- **Conflict to resolve: CNV-EXP-002 against RR-REQ-X-005-r1.** CNV-EXP-002 requires paying through an existing rail-partner enrolment "without new Unbound enrolment". RR-REQ-X-005-r1 makes rails that cannot meet the DestinationEvidence minimum ineligible for automated release. The public documentation of Ren and Chariot states no callback or cooling-off period for later bank changes [SEC-019; b49-04 §3.3]. Partner due diligence must establish the evidence class of the partner's change controls before CNV-EXP-002 applies (PROP-SEC-07). VERIFIED-FACT (documentation gap) / RECOMMENDATION.
- **Competitive angle.** No FY2024 top-20 sponsor publishes a mandatory callback to a known contact before a charity bank change, and no sponsor page addressed to charities warns about bank-change fraud [SEC-018]. Evidence-backed network controls can therefore be a selling point to sponsors' treasurers and auditors, provided they do not add friction for the roughly 80-90% of grants that go to stable destinations (a HYPOTHESIS to measure). INFERENCE, Medium.

## 1. System under analysis

The design assumed here follows the ratified clauses:

- **Shared public layer.** The registry holds public facts (UNB-CHAR-036, UNB-KNOW-012) and propagates holds derived only from public facts (CNV-GRT-004).
- **Sponsor-private layer.** Each sponsor keeps its own eligibility decisions, investigations, banking details and grant relationships, in its own tenant cell (CNV-TEN-001).
- **Destinations.** Destination versions are pinned at authorization (RR-REQ-X-005-r1) and governed by WFM-13. Payments go out on rail partners acting as the sponsor's agent, with sponsor ACH as fallback (CNV-PAY-001).
- **Unbound's role.** Unbound holds no money and cannot unilaterally prevent a payment indefinitely (CNV-LEG-001). Its security holds must therefore be sponsor-policy holds with time bounds and an escalation path.

Assets ranked by attacker value:

1. payment destinations and the contacts used to verify them;
2. representative authority (who may act for a charity);
3. eligibility status and source feeds;
4. sponsor-confidential relationships and investigations;
5. migration extracts.

## 2. Real-world evidence

### 2.1 Regulatory baseline (Nacha 2026)

| Item | Fact | Class |
|---|---|---|
| Phase 1 | 20 March 2026. Covers ODFIs and Originators, TPSPs and TPSs whose 2023 volume exceeded 6m entries, and RDFIs whose 2023 receipts exceeded 10m [SEC-002] | VERIFIED-FACT, High |
| Phase 2 | 19 June 2026 (practical date 22 June). Covers "each ODFI, each non-consumer Originator, each Third-Party Sender, and each Third-Party Service Provider", plus all remaining RDFIs [SEC-001] | VERIFIED-FACT, High |
| Obligation | Risk-based processes "reasonably intended to identify Entries that are suspected of being unauthorized or authorized under False Pretenses". Reviewed "at least annually". Monitoring is not required before processing [SEC-001] | VERIFIED-FACT, High |
| False Pretenses | Misrepresenting (a) identity, (b) authority to act for another, or (c) "the ownership of an account to be credited". The definition "covers common fraud scenarios such as Business Email Compromise (BEC)" [SEC-001, SEC-002] | VERIFIED-FACT, High |
| Micro-entries | Credits under $1 used to verify a Receiver's account, with the description "ACCTVERIFY". Phase 2 took effect 17 March 2023 [SEC-003] | VERIFIED-FACT, High |
| WEB-debit account validation | Account validation is part of a "commercially reasonable" fraud-detection system (debits only) [SEC-004] | VERIFIED-FACT, Medium |

INFERENCE (Medium): grants are credit-push payments, so the 2021 WEB-debit validation rule does not bind them. The 2026 False Pretenses monitoring rule does, through clause (c). Unbound's monitoring program should be documented "relevant to the role it plays" and made available to each sponsor's ODFI (PROP-SEC-13).

### 2.2 Incidents and statistics

| Evidence | What it shows | Class |
|---|---|---|
| Cargill Foundation, 2023: the grantee employee's email and grants-system login were compromised and the bank number changed; $1m first payment of a $2m grant lost [SEC-010] | A bank change inside the grants portal is the attack. The *first* payment to the changed account is the loss event | VERIFIED-FACT (secondary press summary), Medium |
| One Treasure Island, 2020: thread hijack and new wire instructions; $650k lost [SEC-011] | A sponsor-staff BEC path | VERIFIED-FACT (press), Medium |
| Commerce OIG alert, July 2026: hijacked email; "changed banks"; fraudulent W-9 or bank documents; control is to call "a known contact … not a number contained in the request"; dual approval; check "domain spelling" [SEC-009] | Current federal benchmark | VERIFIED-FACT, High |
| IC3 2025: BEC losses $3,046,598,558; Financial Fraud Kill Chain freezes succeeded 58% of the time ($679m frozen of $1.16bn attempted); BEC losses involving AI over $30m [SEC-006] | Speed of recall matters; AI makes lures more fluent | VERIFIED-FACT, High |
| FinCEN: 15,417 reports, >$688m in 6 months; 44% of stolen checks altered and deposited, 26% used as templates [SEC-007, SEC-008] | Check grants remain exposed; positive pay (CNV-PAY-002) is necessary | VERIFIED-FACT, High |
| UK Charity Commission: verify bank changes "using contact information held separately", and "check that a sample of payments has been received by the legitimate organisation after the change" [SEC-012]; warnings about spoofed or similar email addresses [SEC-013] | Source for the receipt-confirmation control | VERIFIED-FACT, High (page withdrawn 2023; advice is standard) |
| California AG: lookalike URLs and email addresses [SEC-015]; cease-and-desist to a fundraising platform that "delayed transferring donated funds to nonprofits" [SEC-014] | Impersonation risk; concentration risk at intermediaries | VERIFIED-FACT, Medium |
| DOJ press-release screen, 2021-2026 (118,050 releases): 0 DAF grant diversions [SEC-018] | Absence from press releases, **not** absence of the threat | VERIFIED-FACT (screen); INFERENCE on meaning |

No CRA (Canada) alert specific to impersonation of registered charities was found in this pass. Not publicly documented, Low.

### 2.3 What incumbents publish

These points are carried from b49-04 and the PR01-PR25 file [SEC-018, SEC-019]:

- **Fidelity Charitable.** Uses a document check plus a *discretionary* callback to a public number.
- **Ren.** A charity claims its record by postcard to the IRS address, by a call to the phone number on its latest e-filed 990, or by an officer ID check. Ren rejects bank links it cannot tie to the organisation, but states no callback or cooling-off period for later changes.
- **Chariot.** Only account owners can change bank details, and two-factor authentication is mandatory. No callback or cooling-off period is stated. Chariot Disbursements validates officer identity against IRS master files.
- **PayPal (NPT, Vanguard).** Bank details are concentrated at PayPal.

INFERENCE: every incumbent network already concentrates bank-change risk at a single verification point. That is the systemic exposure analysed in §5.

## 3. Threat analysis (adversarial)

The full register is in the CSV. This section covers the threats where network design changes the answer.

### 3.1 Contact poisoning: the precursor attack (T04, T10, T14)

The attack chain:

1. Take over the charity's email, or submit a directory correction.
2. Change the registry phone number or add a portal admin.
3. Wait.
4. Request a bank change. The independent callback now rings the attacker.

UNB-UI-P-005 shows the callback contact's source and last-verified date, but no rule blocks a contact changed recently. An IRS-of-record address change (e.g. a Form 8822-B filing) could similarly poison the postcard-claim route. That is a HYPOTHESIS: this pass did not establish how hard it is to change an IRS address fraudulently. Controls are in PROP-SEC-02.

### 3.2 Shared-registry data poisoning (T10, T13, T22)

- **Write paths.** A shared registry has five: platform fetches from primary sources, charity self-service, sponsor corrections, AI extraction and migration imports.
- **Existing controls.** CNV-GRT-004 already requires sponsor corrections to be re-verified, and UNB-KNOW-026 quarantines implausible deltas.
- **Missing.** No requirement says which provenance tiers may write *payment-relevant and callback-relevant* fields.
- **Feed integrity.** The IRS EO BMF is published as CSVs with a posting date (11/10/2026; 1,984,891 records), and the page mentions no checksum or signature [SEC-016].
- **Feed tampering.** A spoofed or MITM'd feed could reinstate a revoked organisation, which is a favourable change and dangerous. It could also mass-revoke organisations, which is an availability attack that could collide with CNV-LEG-001 if holds become indefinite.

### 3.3 Prompt injection (T11, T12)

OWASP ranks indirect injection from "websites or files" first and says it is "unclear if there are fool-proof methods of prevention" [SEC-017].

- **Covered.** CNV-AIO-002 handles the decision dossier.
- **Remaining gap.** AI *extraction* of contact or bank fields from untrusted pages and PDFs into the registry or the destination form. Those values must be provenance tier T6. They must never be usable for callbacks or autofill of destinations, and they can only open a stewardship case (PROP-SEC-14). RECOMMENDATION, High.

### 3.4 Cross-sponsor leakage and evidence reuse (T15, T16)

Leaks can come through side channels as well as direct access:

- "last verified" timestamps on shared destinations;
- event-triggered re-checks started by sponsor A becoming visible to sponsor B;
- search ranking shaped by grant volume;
- embeddings.

Silent reuse of sponsor A's bank letter to meet sponsor B's evidence minimum would breach both A's confidentiality and B's control assurance. CNV-GRT-003 allows reuse "only as input", and UNB-CHAR-037 requires governance of the reuse. PROP-SEC-10 and PROP-SEC-11 make both testable.

### 3.5 Migration and insider risk (T19, T20)

- **Imported payees are already blocked until verified one by one** (UNB-UI-S-056; 07-REFINEMENT AC-1).
- **Remaining risks:**
  - a destination changed in the legacy system just before extraction, then "verified" against legacy evidence;
  - an extract altered in transit;
  - an Unbound Administrator, whose delegation spans several sponsors, touching destinations or shared contacts at more than one sponsor. This is the only cross-sponsor insider position in the design.

## 4. Control design: risk-tiered destination verification

These are RECOMMENDATIONS, refining CNV-PAY-002, RR-REQ-X-005-r1 and UNB-RCN-GRT-017. All numbers are ASSUMPTIONS, to be set as PK-TIMING and policy-pack parameters under CNV-GOV-005 and tighten-only for sponsors.

### 4.1 Provenance tiers (applies to every registry claim)

| Tier | Source | May set payment-relevant or callback fields? |
|---|---|---|
| T1 | Primary government source fetched by the platform (IRS EO BMF/TEOS/Pub78, latest e-filed 990, state registry) | Yes, but a contact changed within the last 60 days cannot be the *sole* callback channel |
| T2 | Bank-originated data (owner match, NOC through an authenticated rail callback, positive-pay clearing) | Yes, for destination ownership only |
| T3 | Contracted independent verifier or rail partner with an attested evidence class | Yes, as input; the sponsor's tier minimum still applies |
| T4 | Verified charity principal (authority proven, phishing-resistant MFA) | Requests only: creates a Pending version subject to the tier rules |
| T5 | Sponsor-submitted correction | No. Opens a re-verification case (CNV-GRT-004) |
| T6 | Web or AI extraction, uploaded documents, email | No. Stewardship case only |

### 4.2 Change risk tiers

**D0: informational change** (remittance address, contact name, no destination change).
- Activation: no payment hold (CNV-GRT-003 AC-3).
- Exposure limits: none.

**D1: first destination for a charity with no risk signals.**
- Minimum evidence (all of):
  - a T2 owner match on the exact legal name or a recorded DBA, *or* a bank letter confirmed by calling the bank on an independently sourced number;
  - plus a prenote, or IAV with the owner name returned;
  - plus a callback to an aged T1 contact.
- Activation: 3 business days pending (existing UNB-UI-P-005 AC-4).
- Exposure limits:
  - first payment per sponsor ≤ $25k;
  - network exposure on this destination version ≤ $50k until receipt is confirmed or 30 days of clean history.

**D2: change to an existing verified destination.**
- Minimum evidence: as D1, plus notice to the previous destination's contacts and to all charity admins. The callback contact must have been unchanged for 30 days or more and must not have been touched in this case.
- Activation: 5 business days pending. Payments continue to the old version meanwhile (UNB-UI-S-012 AC-2).
- Exposure limits:
  - first payment ≤ $25k per sponsor;
  - network exposure ≤ $50k;
  - 60-day probation.

**D3: elevated.** Any one signal puts the change in D3:
- a contact or admin changed within 30 days;
- a new representative (less than 30 days);
- an owner match of No or Partial, or an individual owner;
- the same account linked to another EIN;
- a requester email domain less than 90 days old or a lookalike domain;
- urgency language;
- pending grants above $100k;
- a migration late change (≤ 90 days before cutover);
- a foreign or non-bank account.

Requirements for D3:
- Minimum evidence: security review (`DestFraudSuspected`) by two independent verifiers, plus officer verification by assisted video, notarization or a bank-confirmed letter. No automated release.
- Activation: 10 business days pending.
- Exposure limits: release only after receipt of the first payment is confirmed; the sponsor can tighten further.

**NOC correction** (WFM-13 T03).
- Minimum evidence: the authenticated NOC creates a Pending version. If the owner name changes, the change is promoted to D3.
- Activation: per WFM-13 (new releases are held).
- Exposure limits: as D2.

### 4.3 Verification method trade-offs

| Method | Proves | Does not prove | Friction and cost | Use |
|---|---|---|---|---|
| Micro-entries [SEC-003] | The submitter can see the account; the account is open | That the *charity* owns it (a mule passes) | 1-3 days; charity effort | Supporting evidence only; never sufficient alone |
| Prenote | Account number is valid (absence of a return) | Ownership or authority | Several days; low cost | Supporting evidence |
| IAV (bank login) | The submitter holds the online-banking credentials; may return the owner name | Authority to change; owner-name similarity can be gamed by a shell with a similar name | Instant; charity must use bank credentials | Ownership evidence when the returned owner equals the legal name exactly |
| Bank-originated owner match (EWS-type) [SEC-005] | Owner name or business match from bank-contributed data, independent of the submitter | Requester authority; coverage of business accounts is not published | Instant; per-query fee | Preferred ownership evidence (T2) |
| Bank letter | Bank attests ownership | Genuineness (forgeable) unless the bank is called on an independent number | Days | D1 alternative; D3 with a bank call |
| Callback to an aged T1 contact | Authority (someone at the real organisation agrees) | Ownership; fails if the contact is poisoned | Minutes; staff time | Required at D1-D3 |
| Receipt confirmation [SEC-012] | The money actually arrived at the real charity | Nothing before the first payment | Charity effort after payment | Ends probation; required at D3 |

### 4.4 Failure behaviour

- **Callback denied** → `DestFraudSuspected` (WFM-13). Notify the charity on every verified channel, and recall any in-flight payment immediately. IC3's 58% freeze success is the reason to act within hours [SEC-006].
- **Evidence service unavailable** → the change stays Pending. Release continues to the previous version. An outage never activates a change.
- **Hold duration** → every security hold carries an SLA and sponsor escalation, never an indefinite hold by Unbound alone (CNV-LEG-001).

## 5. Bounding systemic risk from shared verification

**Model** (INFERENCE). Charity *c* has a destination version *v* that is shared with *k* opted-in sponsors, which have pending releases *P₁…Pₖ*. Without controls, the loss from one successful deception is ΣPᵢ released before detection. With controls, the loss is ≤ min(ΣPᵢ, E_net), where E_net is the network probation cap, and each sponsor's own loss is ≤ min(Pᵢ, F_first). Receipt confirmation ends probation, which usually limits the loss to one payment.

**Rules** (PROP-SEC-03, -04, -11):

1. **Opt-in on both sides.**
   - A sponsor may *consume* shared destination evidence only by affirmatively adopting a policy pack setting (CNV-GOV-005).
   - A sponsor's evidence is *offered* to others only with that sponsor's opt-in *and* the charity's consent.
   - What is shared is a derived assertion (evidence type, date, verifier class, destination fingerprint), never the document or the account number.
2. **Input, not decision.** The consuming sponsor's tier minimum still applies (CNV-GRT-003). Shared evidence can satisfy only the ownership component, never the authority component: each sponsor makes its own callback, or relies on a partner-attested T3 callback it has adopted.
3. **Asymmetry.**
   - Facts that make other sponsors *stricter*: public-fact holds propagate (CNV-GRT-004); destination-integrity signals propagate only as a neutral "re-verify destination" flag under the written inter-sponsor agreement.
   - Facts that make other sponsors *looser* (a destination being verified) propagate only to opted-in consumers, and only after the probation period.
4. **Velocity tripwire.** When more than *n* sponsors (default 3) release to a destination version less than 60 days old within 7 days, automated release pauses for every sponsor pending receipt confirmation. The pause is time-bounded.
5. **Destination uniqueness.** One account and routing pair linked to two EINs blocks both until resolved. Exception: a fiscal sponsor recorded as an edge under UNB-KNOW-021.

Is the net effect positive? HYPOTHESIS. With these bounds, sharing *reduces* expected loss compared with each sponsor verifying alone, for three reasons:
- shared T2 ownership evidence is stronger than the voided-check practice common today (PR01);
- network-wide velocity and return signals detect fraud faster;
- caps limit the downside.

This is testable with the replay and shadow tooling of CNV-GOV-005. The tension with CNV-GRT-004 is that a *destination-integrity* signal (the charity is the victim) is not a charity-misconduct investigation. Counsel should confirm whether it may be shared outside the written agreement. Flagged, not assumed.

## 6. Other controls (mapped)

| Area | Control | Existing IDs | Proposed |
|---|---|---|---|
| Representative authority | Officer on latest 990 or state registry plus callback to the organisation's number; new representative cannot change the destination for 30 days; annual re-attestation of admins | UNB-CHAR-014, CNV-PLT-003 | PROP-SEC-15 |
| Charity contact changes | Notify the old channel with a revert link; 72-hour hold on destination and admin changes after any contact change (mirrors CNV-PLT-011) | CNV-PLT-011 (donors only) | PROP-SEC-02 |
| Feed integrity | Allowlisted irs.gov hosts, TLS verification, raw hash and posting date stored, delta plausibility, cross-source consistency, favourable changes need corroboration, circuit breaker with time bound | UNB-CHAR-008, UNB-CHAR-011, UNB-KNOW-026, UNB-KNOW-032, CNV-GRT-003 | PROP-SEC-06 |
| AI ingestion | T6 provenance for extracted contacts and bank fields; no autofill; extraction shown beside the source image | CNV-AIO-002, UNB-KNOW-030, UNB-CHAR-022 | PROP-SEC-14 |
| Outbound authenticity | DMARC p=reject on Unbound and sponsor white-label domains; no action links in bank-related email; lookalike-domain monitoring; published "how to verify us" page for charities | — | PROP-SEC-09 |
| Partner enrolments | Partner change-control evidence class recorded; change-event feed and fingerprint; mismatch blocks; exposure limits | CNV-EXP-002, CNV-PLT-012, RR-REQ-X-005-r1 AC-1 | PROP-SEC-07 |
| Migration | Hashed and signed extract manifest; two independent extracts diffed; late-change window → D3; legacy payment-history corroboration (a destination paid without return for at least 12 months is pre-assembled evidence, still verified one record at a time); independent reconciler | UNB-CHAR-041, UNB-TEN-011, UNB-TEN-013, UNB-UI-S-056, UNB-UI-S-057 | PROP-SEC-08 |
| Insider | Unbound staff never verify or activate a sponsor destination; ServiceDelegation excludes destination authority; two-person rule on payment-relevant registry writes; alert on actions across more than one sponsor | CNV-TEN-001, UNB-RULE-020, UNB-UI-S-056 AC-1 | PROP-SEC-12 |
| Leakage | No per-sponsor timestamps or "verified by" in shared fields; re-checks not attributable across tenants; negative tests | CNV-TEN-001, UNB-TEN-009, UNB-KNOW-012, CHAR-T10/T17 | PROP-SEC-10 |
| Nacha program | A documented False Pretenses monitoring program, annual review, case feed to the sponsor's ODFI, a recall playbook | CNV-PAY-001 | PROP-SEC-13 |
| Checks | Payee-name positive pay, void files, stop-payment, preference for electronic payment for repeat grantees | CNV-PAY-002, RR-REQ-X-083-r1 | — |

## Implications for Unbound

1. **Treat bank-change security as a regulated, auditable product surface.** The Nacha Phase 2 TPSP duty means a sponsor's ODFI will ask for the monitoring program. A documented, tiered design is a sales asset with treasurers, while incumbents publish only discretionary callbacks (INFERENCE, Medium).
2. **Share ownership evidence, never authority.** This captures the network benefit (one strong owner match reused) without inheriting a single point of deception.
3. **Protect the contacts used for callbacks as carefully as the bank account.** Contact poisoning is the cheapest way to defeat every callback control on the network.
4. **Friction is the cost.**
   - First-payment caps and receipt confirmation slow a charity's *first* large grant. Measure the share of grants affected; HYPOTHESIS: under 10% are first or changed-destination payments.
   - Where caps would split a large first grant, offer an expedited D1 path: video officer verification plus a bank call.
5. **CNV-EXP-002 needs a security precondition.** Without one, Unbound inherits the weakest partner's change controls across every sponsor.

## Proposed requirements (only where missing)

- **PROP-SEC-01.** Risk-tiered destination verification D0-D3 with evidence minimums, pending periods and exposure caps (refines CNV-PAY-002, UNB-RCN-GRT-017).
- **PROP-SEC-02.** Rules on the age and change history of charity callback contacts, plus contact-change holds for charity principals (extends CNV-PLT-011, UNB-UI-P-005).
- **PROP-SEC-03.** Network exposure cap and velocity tripwire for new or changed destination versions; per-sponsor opt-in to shared destination evidence (refines CNV-GRT-003, UNB-CHAR-037).
- **PROP-SEC-04.** Receipt confirmation through an independent channel ends probation (new).
- **PROP-SEC-05.** Provenance tiers T1-T6 decide which sources may write payment-relevant and callback fields; corroboration quorum (refines UNB-CHAR-012, UNB-KNOW-030).
- **PROP-SEC-06.** Source-feed integrity gates, plus a mass-change circuit breaker with time-bounded holds (refines UNB-KNOW-026, CNV-GRT-003).
- **PROP-SEC-07.** Partner-enrolment change-control attestation before CNV-EXP-002 applies (resolves the conflict with RR-REQ-X-005-r1).
- **PROP-SEC-08.** Migration chain of custody and late-change window (refines UNB-CHAR-041, UNB-TEN-011).
- **PROP-SEC-09.** Outbound email authenticity and lookalike-domain monitoring (new).
- **PROP-SEC-10.** Shared-store inference tests: non-attributable re-checks, no per-sponsor timestamps (refines CNV-TEN-001).
- **PROP-SEC-11.** Reuse of private evidence needs charity consent and the providing sponsor's opt-in; only derived assertions are shared (refines UNB-CHAR-037).
- **PROP-SEC-12.** Unbound personnel excluded from destination authority; two-person rule on registry payment-relevant fields (refines CNV-TEN-001).
- **PROP-SEC-13.** Nacha False Pretenses monitoring program and recall playbook (new; counsel review).
- **PROP-SEC-14.** AI-extracted contact and bank values are T6 and never auto-applied (refines CNV-AIO-002).
- **PROP-SEC-15.** Proof of representative authority and a probation period for new representatives (refines UNB-CHAR-014, CNV-PLT-003).

## Open questions / evidence gaps

1. **Nacha applicability.** Counsel must confirm how the Phase 2 TPSP duties apply when the rail partner, not Unbound, transmits entries (CNV-PAY-001).
2. **Account-owner match coverage.** Not publicly documented for business and nonprofit accounts (EWS gives no rate). A bank or provider POC is needed before T2 can be the default.
3. **Partner change controls.** The bank-change controls of Ren, Chariot and PayPal after enrolment (callback, cooling period, notification) are not publicly documented. Due diligence is required.
4. **IRS address changes.** The difficulty of fraudulently changing an IRS-of-record address or phone number is unverified (HYPOTHESIS for T14).
5. **Destination-integrity signals.** May they be shared outside the CNV-GRT-004 written agreement, given the charity is the victim? Counsel question.
6. **Prevalence.** There is no public prevalence data for diversion of DAF grants specifically (the DOJ screen found 0). Calibrate caps from sponsor loss history, Form 990 Part VI line 5 data and a design-partner replay.
7. **Sources not readable this pass.** The Star Tribune original (403/429), the LSC OIG BEC advisory (connection reset) and the full FinCEN alert PDF. Their figures rest on secondary or earlier-repo reads.
