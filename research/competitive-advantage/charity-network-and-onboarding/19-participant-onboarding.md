# 19 - Low-friction participant onboarding (B10)

Status: research draft (2026-11-26). Not legal advice. Evidence classes per 01-research-methodology.md.

Scope: onboarding of donors, joint and professional advisors, viewers/successors and (briefly) charities, with federated identity, sponsor- or
partner-provided identity assertions, progressive collection, reuse of facts already held, prefill and risk-proportional verification, without
removing any required identity, legal, financial or fraud control. Charity organic network growth is covered in `08` (another agent); this
document only covers the charity's first touch when a grant arrives. Sponsor-side parameters come from the sponsor configuration package
([`12-declarative-sponsor-configuration.md`](12-declarative-sponsor-configuration.md)); identity-provider and firm integrations are certified per
[`18-integration-onboarding.md`](18-integration-onboarding.md). Sources: [`data/sources-CFG.csv`](data/sources-CFG.csv).

## Summary

- **Incumbent online opening is already short; the friction is elsewhere.** Fidelity Charitable states opening takes "about 5 minutes" in 3 steps (your information, name the account, review/submit), asks for SSN, contact information and an account name, and pre-fills some fields for existing Fidelity logins [CFG-027]. DAFgiving360 advertises "as little as 15 minutes" and lists SSN, date of birth and a US permanent address, with contact details and signature per holder, funding details and Program Policies acceptance [CFG-028]. Daffy advertises opening "in minutes" with $0 to open, though its own FAQ also cites a $100 one-time sign-up contribution [CFG-029]. (VENDOR-CLAIM, Medium) **INFERENCE (Medium):** a challenger cannot win on raw account-opening time; differentiation must come from (a) advisor- and sponsor-originated journeys where facts are already held, (b) adding participants, successors and advisors without paper, and (c) charities receiving grants without enrolment.
- **Field-level counts for incumbents are not publicly documented.** The sources give information groups, not field lists; DAFgiving360's application page returned 403 to direct fetch and was read via search excerpts. Current-vs-proposed counts below are therefore a modelled comparison on a stated field model (ASSUMPTION), not measured incumbent counts.
- **The requirement base is unusually complete and mostly favours low friction**: RR-ADM-002-r2 (collect only facts required by role checks, program terms and first funding method; prefill held/IdP facts for confirmation; click-accept agreement, no wet signature; view-only participants need no proofing), RR-AIN-007-r1 (query held, retrievable and inferable facts before asking), UNB-XIN-CLM-003 (never request a Fresh fact), UNB-SMP-CXP-001 (Interaction Register: every input needs a necessity basis), RR-UNB-PART-007-r1 (four separately classified checks; no "KYC" label without applicability record). RR-ADM-002-r2, RR-AIN-007-r1 and UNB-SMP-CXP-001 are **proposed**, not adopted. (VERIFIED-FACT from repo, High)
- **The controls that must stay are equally explicit**: CNV-PLT-003 (validate core attributes against authoritative sources, match funding-account owner, validated address or phone; step-up to document+selfie or non-biometric live video; no KBV for proofing; prefill never substitutes for proofing and never silently overwrites verified data), CNV-GRT-006 (sanctions screening at onboarding), CNV-PLT-011 (72h contact-change hold and accessible assurance path), CNV-PAY-002 and its ADV-R2 amendment (charity bank changes need CAL3 and ratified evidence combinations). NIST SP 800-63A-4 also says KBV "SHALL NOT be used for identity verification" and that a government identifier SHALL be a core attribute [CFG-030]. (VERIFIED-FACT, High)
- **Sponsor/partner identity assertions can reduce typing but not proofing by themselves.** NIST 800-63A-4 recognises "authentication and federation protocols" as a verification method under a trust agreement (800-63C) [CFG-030]; CNV-PLT-003 forbids prefill from substituting for proofing. Design: a federated assertion from an IdP with a recorded trust agreement and declared assurance is **evidence** in the proofing decision (it can satisfy attribute presence and, where the agreement states the IdP validated attributes at a declared level, attribute validation), while account-owner match and sanctions screening still run. Whether a reliance agreement can fully satisfy CNV-PLT-003 proofing is an **open interpretation** for counsel/owner; default is conservative. (INFERENCE, Medium)
- **Cross-sponsor reuse of donor facts is prohibited by design.** UNB-XIN-IAM-001 (one Customer principal per tenant; same person at two sponsors has two principals) and CNV-TEN-001 (no donor PII in shared stores except keyed token) mean "existing information reuse" is within the sponsor tenant, from the sponsor's or partner's own authorized feeds, or donor-initiated portability (e.g. migration CNV-EXP-002). Charity public facts, by contrast, are shared (RR-AIN-007-r1, CNV-GRT-004). (VERIFIED-FACT from repo, High)
- **Biggest friction reduction is in multi-party and advisor journeys**, where incumbents publicly rely on forms (DAFgiving360 lists donor forms and advisor forms; Fidelity Charitable offers a paper Donor Application) [CFG-027, CFG-028]. Firm-managed advisor access via SCIM with the (advisor, firm) pair rule (UNB-XIN-CRM-007) and holder consent replaces per-advisor paperwork. (INFERENCE, Medium)

## 1. Current-state evidence (public)

| Provider | Stated time | Steps | Information named publicly | Prefill / reuse | Paper/alt path | Source / class |
|---|---|---|---|---|---|---|
| Fidelity Charitable (individual Giving Account) | about 5 minutes | 3 | Account holder SSN; contact information; account name | "If you already have a Fidelity login, some fields may be pre-filled" | Paper Donor Application by mail | [CFG-027] VENDOR-CLAIM, Medium-High (page fetched) |
| DAFgiving360 (Schwab) | as little as 15 minutes | not stated | US permanent address; SSN; date of birth; contact info and signature per holder; funding details; Program Policies acceptance | Assets at Schwab movable via schwab.com | Mail or fax application; advisor forms | [CFG-028] VENDOR-CLAIM, Medium (search excerpts; direct fetch 403) |
| Daffy | "in minutes" | not stated | Not retrieved (requirements page did not render) | not documented | App-first | [CFG-029] VENDOR-CLAIM, Low-Medium |

No public source states field counts, abandonment rates or identity-verification step-up rates for these providers. Absence is not evidence that they lack prefill or risk-based proofing.

## 2. Hard constraints (never removed)

| Control | Applies to | IDs |
|---|---|---|
| Sanctions screening at onboarding, delta on list update, before each release | Donors, advisors, successors, payors, grantees | CNV-GRT-006, RR-UNB-EXT-004-r1 |
| Risk-based proofing: validate core attributes vs authoritative sources; funding account owner match; validated address or phone; step-up on failure/elevated risk | Advisory-privilege holders and contributors | CNV-PLT-003, RR-UNB-PART-007-r1 |
| No KBV for proofing; KBV ≤ CAL1 | All | CNV-PLT-003 |
| Prefill marked, confirmed, never silently overwrites verified data, never substitutes for proofing | All | CNV-PLT-003, RR-ADM-002-r2 |
| Entities verified by registration and signatory authority | Organizational donors, firms, charities | CNV-PLT-003, UNB-WF-012 |
| Contact-channel change notice and 72h hold on sensitive changes | All verified channels | CNV-PLT-011 |
| Destination evidence before first electronic payment and after bank change; CAL3 for charity bank/contact changes | Charities | CNV-PAY-002 (+ADV-R2-010/067), UNB-RCN-WF-028 |
| Instruction authority from fund agreement; joint approvals where no any-one clause | Multi-advisor funds | CNV-GRT-016, UNB-PART-008 |
| Affiliation capture for advisory-privilege holders | Advisors | UNB-XIN-CRM-002 |
| Agreement version, timestamp, principal, channel recorded | Fund opening | RR-ADM-002-r2, ADM-014 |
| Accessibility WCAG 2.2 AA; accessible assurance path to CAL3 | All | CNV-EXP-001, CNV-PLT-011, CNV-GOV-006 |
| CIP-style data only when counsel records applicability | All | RR-UNB-PART-007-r1, CNV-LEG-001 |

## 3. Fact-sourcing model

Every input on every journey is resolved in this order before the UI renders a blank field (RR-AIN-007-r1, UNB-XIN-CLM-003, UNB-SMP-CXP-001):

| Order | Source class | Examples | Use | Constraint |
|---|---|---|---|---|
| 1 | Held fact, same tenant, Fresh for purpose | Existing donor adding a second fund | Prefill for confirmation, or skip | Freshness per purpose; consent scope |
| 2 | Sponsor/partner federated assertion (OIDC/SAML claims) | Wealth-platform client arriving via partner SSO | Prefill; proofing evidence only under recorded trust agreement | Stable key issuer+subject (AUTH-I8); assurance declared; sponsor-direct factor offered at first login (UNB-XIN-IAM-001) |
| 3 | Authorized feed | Firm SCIM roster; custodian account title; payroll file | Prefill / role proposal | Certified integration (doc 18); firm cannot grant privilege (UNB-XIN-CRM-007) |
| 4 | Verification provider result | Bank account-owner match (e.g. per-field match scores [CFG-011]); identity-data validation | Validate, not prefill PII from vendor | Vendor result stored as evidence with retrieval time |
| 5 | Public registry (charities) | IRS TEOS/BMF, state registries, Unbound charity registry | Prefill charity identity | Cross-sponsor public facts reusable as input (CNV-GRT-003/004) |
| 6 | Inference/default rule | Fund name from donor name; statement delivery default | Suggest | Registered rule in Interaction Register |
| 7 | Ask | Anything still missing or expired | Progressive: only when the step needs it | Necessity basis recorded (law/consent/donor-control/security/convention) |

Prefill record (data structure): `{factType, value, sourceClass, sourceRef, retrievedAt, purpose, consentRef, freshnessUntil, confirmationState (Unconfirmed|Confirmed|Declined), verificationState (Unverified|Validated|Verified)}`. A declined prefill reverts to Ask plus normal verification (RR-ADM-002-r2). Conflict with a verified value opens a confirmation step showing both values and sources (CNV-PLT-003).

## 4. Risk-proportional verification matrix

| Role / action | Proofing required | Funding-account check | Contact assurance | Screening | Notes / IDs |
|---|---|---|---|---|---|
| View-only participant (authorized viewer, admin contact) | None (RCD-023) | n/a | Verified email | Name screening only if sponsor ScreeningScope says so | RR-ADM-002-r2, RR-UNB-PART-007-r1 |
| Successor-designate (not yet active) | None until activation | n/a | Contact recorded, unverified | At activation | UNB-SUCC-006, CNV-ENT-001 |
| Contributor without advisory privilege (e.g. family member gifting) | Payment-instrument level only | Account validation / owner match on first debit | n/a | Payor screening | CNV-PLT-003, CNV-GRT-006, Nacha first-use account validation [CFG-021] |
| Advisory-privilege holder (donor/advisor) | Risk-based proofing at sponsor-configured level | Owner match where they fund | CAL2+ for routine; CAL3 for bank/authority/contact changes | Onboarding + delta | CNV-PLT-003, UNB-XIN-IAM-003 |
| Professional advisor (firm-managed) | Individual proofing via firm IdP evidence + firm registration | n/a | AAL2 phishing-resistant | Onboarding + delta | UNB-WF-012, UNB-XIN-CRM-007 |
| Organizational donor | Entity registration + signatory authority | Owner match to entity | Signatory at CAL2+ | Entity and signatories | CNV-PLT-003 |
| Charity user (grant-initiated) | Not required to receive a routine grant | Destination evidence per CNV-PAY-002 | CAL3 for contact/bank changes | Recipient screening | RR-UNB-GRANT-026-r1, CNV-PAY-002 |

Step-up triggers (deterministic, recorded): attribute validation failure; owner-match score below threshold; device/channel risk signals; recent contact change (CNV-PLT-011 window); sponsor risk profile. Step-up paths: document + selfie, non-biometric live video, mailed one-time code, outbound call to verified number, in-person/notarized (CNV-PLT-003, CNV-PLT-011 AccessibleAssurancePath).

## 5. Journeys: current-state model vs proposed

**Field model (ASSUMPTION, stated so the comparison is reproducible):** typed inputs for a new individual advisory-privilege holder without any prior relationship: first, middle, last name (3), DOB (1), SSN (1), residential address (street, unit, city, state, ZIP = 5), email (1), mobile (1), fund name (1), funding bank routing/account/type (3), successor name and relationship (2), agreement acceptance (1), communication consent (1) = **21 inputs**. This matches the information groups the incumbents name but not any measured incumbent form.

| Journey | Current-state model (typed / confirm) | Proposed (typed / confirm) | How | Controls retained |
|---|---|---|---|---|
| J1 New donor, no relationship, direct | 21 / 0 | ~13 / 3 | Address lookup (5->1 typed + confirm); bank linked via account-owner-match provider (3->0 typed, 1 action); successor deferred to post-funding prompt (2->0 at opening); fund name suggested (1->confirm) | Proofing, owner match, screening |
| J2 Donor arriving via sponsor/partner SSO (advisor-distributed segment) | 21 / 0 | ~3 / 7 | Name, DOB, address, email, phone from assertion -> confirm; SSN typed if not asserted (government identifier SHALL be a core attribute [CFG-030]); bank via owner match or custodian-held account title | Assertion is evidence; owner match + screening still run; sponsor-direct factor offered |
| J3 Existing donor opening second fund at same sponsor | 21 / 0 (if re-keyed) | ~1 / 3 | Held Fresh facts reused (UNB-XIN-CLM-003); only fund name and agreement | No re-proofing while Fresh; screening per list version |
| J4 Add joint advisor | paper/online form, both parties | invitee: ~6 / 2; inviter: 2 | Invitation -> invitee identity -> scoped role -> holder consent (WF-02); instruction authority clause chosen explicitly | CNV-GRT-016 joint approval; proofing of invitee |
| J5 Add authorized viewer | form | ~3 / 0 | Name, email, accept | No proofing (view-only) |
| J6 Professional advisor access (firm-managed) | per-advisor form + firm agreement | 0 typed identity; 1-3 affiliation answers | Firm SCIM provisions principal; donor (holder) grants scoped access; departure ends access | UNB-XIN-CRM-007; AUTH-I8; affiliations UNB-XIN-CRM-002 |
| J7 Migrated donor first login after sponsor switch | re-register | ~0 / confirm migrated facts | Imported facts `imported_unverified` (RR-REQ-X-061-r1); confirm; verification before any payment to imported destination | Imported payees blocked until verified |

Counts are INFERENCE on the model above (Medium); they should be validated by moderated usability testing (CNV-GOV-005 ADV-R2-064 pattern; UNB-UX-006) before any external claim.

### Progressive collection plan (J1)

1. Intent and eligibility (role, individual vs entity) - 1 decision.
2. Identity (prefill/ask; validation runs in background) - proofing decision `Pass | StepUp | Fail | Pending(provider unavailable)`; on `Pending` the fund can be drafted but no role activates (RR-UNB-PART-007-r1 AC-2).
3. Agreement click-accept (version, timestamp, principal, channel).
4. Funding (link bank / custodian transfer / DAF-to-DAF); four contribution dates tracked (CNV-FIN-003).
5. After first contribution accepted: successors, additional participants, statement preferences (deferred, not dropped).

Failure behaviours: proofing Fail after contribution received -> capacity not grantable, case per policy (RR-UNB-PART-007-r1 AC-3); abandoned intake -> save-and-resume token with expiry, no partial account; duplicate person detection within tenant -> merge proposal to staff, never auto-merge (A4 for identity merges, cf. GOV decision matrix).

## 6. Delegated authority and organization-managed advisor access

- **Realms**: firm staff are Customer-realm principals linked to a firm record, not PartnerWorkforce unless the firm is a distribution partner (UNB-XIN-IAM-001). Staff endpoints reject them.
- **Provisioning**: SCIM (RFC 7644 [CFG-031]) from the firm's IdP creates/deactivates advisor principals; identity key is issuer+subject or SCIM externalId (AUTH-I8). End-to-end revocation latency is bounded by the firm's deprovisioning SLA, which must be contractual (WG-2).
- **Grant**: an advisory-privilege holder grants the (advisor, firm) pair a scoped role (view, prepare recommendations, recommend within limit); the firm cannot self-grant (UNB-XIN-CRM-007). Delegated customer roles expire on events and are recertified at least annually (CNV-GOV-006, UNB-XIN-IAM-004).
- **Representatives** (POA, guardian) act only within recorded scope; protective suspension available (UNB-XIN-CLM-006).
- **AI assistants** can prepare onboarding answers and explain fields (AssistanceContract), never submit attestations or consents for the principal (CNV-AIO-001).

## 7. Charity first touch (brief; see 08)

- A routine grant MUST NOT require charity enrolment when a verified destination, check or approved disbursement-partner path exists (RR-UNB-GRANT-026-r1, status unvalidated); charities already enrolled with a supported networked rail partner are paid through that enrolment (CNV-EXP-002).
- Charity identity is prefilled from the registry (RR-AIN-007-r1); the charity is asked only for what electronic payment needs: destination evidence by one of the two ratified combinations (CNV-PAY-002 amendment), with CAL3 for whoever submits bank or contact changes.
- Acknowledgment is optional and never payment proof (RR-UNB-GRANT-026-r1).
- Organic network growth, claim-your-profile and cross-sponsor evidence reuse are covered in 08.

## 8. Accessibility and contextual assistance

- WCAG 2.2 AA with reflow, mobile-first (CNV-EXP-001, UNB-PLAT-004); accessible assurance path reaching CAL3 without a smartphone (CNV-PLT-011); relay calls accepted.
- Every field shows AssistanceContract text: purpose, why needed (necessity basis from Interaction Register), what happens if declined, who sees it (CNV-AIO-001, UNB-SMP-CXP-001).
- Status of proofing and funding shown as domain state, including Pending/Unknown, never as success before verification (RR-UNB-UX-003-r1).

## Implications for Unbound

1. RECOMMENDATION: adopt RR-ADM-002-r2, RR-AIN-007-r1 and UNB-SMP-CXP-001 (currently proposed); they are the core of the low-friction claim and are consistent with CNV-PLT-003.
2. RECOMMENDATION: add a **FederatedAssertionReliance** requirement: per IdP, a recorded trust agreement, declared assurance level and attribute list; assertions are proofing evidence, never a substitute for account-owner match or screening; reliance status visible in the proofing decision record (refines CNV-PLT-003, UNB-XIN-IAM-001). Needs counsel/owner interpretation.
3. RECOMMENDATION: add **firm-managed advisor provisioning** (SCIM, pair-scoped grants, contractual deprovisioning latency) as a release-1 requirement for the advisor-distributed entry segment (refines UNB-WF-012, UNB-XIN-CRM-007; CNV-ECO-004 segment).
4. RECOMMENDATION: specify **deferred (not dropped) collection** for successors and secondary participants after first funding, with reminders via InformationRequest (UNB-XIN-CLM-003).
5. RECOMMENDATION: instrument onboarding per UNB-RCN-PLT-006 / ADM-047 (typed inputs, confirmations, step-up rate, abandonment by step) so claims are measured, not modelled.
6. Competitive framing (INFERENCE, Medium): sell "no re-keying for advisor-originated and migrated donors" and "add people without paper", not "faster account opening".

## Open questions / evidence gaps

- Can a sponsor/partner IdP's proofing, under a written trust agreement, satisfy CNV-PLT-003 proofing for advisory-privilege holders, or only contribute evidence? (counsel/owner; potential tension with "prefill never substitutes for proofing").
- Incumbent field-level forms, step-up rates and abandonment are not public; moderated walkthroughs of public flows (no account creation, per brief rules) or consented user studies are needed.
- Daffy's sign-up requirements and minimum ($0 vs $100 sign-up contribution) conflict across its own pages; not resolved.
- Sponsor appetite for SSN-optional opening (e.g. defer SSN until first contribution) is unknown; NIST requires a government identifier as a core attribute for proofing, so deferral only works if roles stay inactive until proofing.
- Whether view-only participants need any screening is a ScreeningScope (UNB-RCN-GRT-007) counsel decision.
