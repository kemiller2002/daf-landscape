# Sponsor White Label, Grant Terminology and Donor Affirmations: Decision Record v0.1
Date: 2026-11-22
Status: PROPOSED; legal validation required

## Core architecture
Separate (1) sponsor branding/theme, (2) typed localization/terminology, (3) sponsor policy and legal disclosures, and (4) affirmation evidence. Branding and aliases must not modify financial, legal, authorization or accounting semantics. Scope each configuration to sponsoring legal entity, brand, channel, locale, product, grant purpose, donor class and effective date as appropriate. Support sponsor-approved templates with constrained overrides, preview, test, publish and rollback.

## Requirements
WL-01 Sponsor-scoped logo, color, typography, domain, emails, documents, widget and app shell; preserve accessibility, security and compliance.
WL-02 Typed terminology dictionary: Grant, GrantRecommendation, GrantDistribution, Grantee, Advisor, Fund, Contribution, Sponsor and relevant verbs; use stable canonical IDs and context-specific inflection, plural, accessibility labels and translations.
WL-03 Terminology cannot change legal semantics, ledger types, API schema identifiers or cross-sponsor audit evidence.
WL-04 Versioned sponsor policy engine for allowed grant purposes, prohibited benefits, special classes, jurisdiction and sponsor-specific restrictions, with stricter applicable law taking precedence.
WL-05 Sponsor-approved legal disclosures and donor representations, versioned with locale, applicability, effective date and legal reviewer.
WL-06 Explicit affirmative action for each required representation or an approved grouped acknowledgment; do not infer consent from prechecked boxes, silence, AI, or past unrelated activity.
WL-07 Bind affirmation evidence to actor, authority, sponsor, fund, draft/transaction, exact disclosure version/hash, presented language, time, channel, and submission idempotency key; tamper-evident audit.
WL-08 Distinguish statutory/legal prohibitions from sponsor-specific prohibitions, advisory guidance and conditional exceptions; display accurate explanations.
WL-09 Include prohibited private benefits, quid-pro-quo purchases (tickets, tables, auction items, memberships with material benefits), personal goods/services, binding pledges where prohibited, political campaign contributions, grants to individuals unless through a legally permitted sponsor program, and other prohibited uses as validated by sponsor counsel. Do not state all memberships, event sponsorships, or pledge arrangements are universally prohibited: evaluate benefit, commitment and governing rules.
WL-10 Donation/grant recipient and purpose attestation, including whether donor/advisor or related party receives goods, services, reimbursement, tuition, travel, event admission or other benefit; conditional follow-up rather than indiscriminate blanket prohibition.
WL-11 Sponsor policy may add restrictions but cannot override law, required sponsor control, or shared security invariants; validate rule conflicts before publication.
WL-12 Require policy/disclosure re-evaluation and potentially fresh affirmation after material edits, grant amount/purpose/recipient changes, policy version change, schedule execution, authority change or time expiry according to sponsor-approved policy.
WL-13 Recurring/future grant schedules: capture initial schedule consent and define bounded standing affirmation policy; re-check eligibility and grant-specific rules for each occurrence; fresh consent where required. Do not silently auto-affirm.
WL-14 API and embedded widgets must render and enforce the same sponsor-specific disclosures, policy and affirmation evidence as native UI; server rejects bypassed acknowledgments.
WL-15 Document and notification generation uses sponsor branding and terminology, but preserves legally mandated sponsor identification and accurate grantmaker identity.
WL-16 Sponsor configuration console with policy simulation, preview by persona, localization, approvals, dual control for sensitive policy edits, version comparison and rollback.
WL-17 Sponsor-specific terminology must support search synonyms and internal support tooling; audit displays canonical plus displayed term/version.
WL-18 Accessibility: screen-reader labels, 320px reflow, 400% zoom, WCAG 2.2 AA, contrast and readable legal text; no dark patterns or forced scroll-as-consent.
WL-19 Compliance exception queue for ambiguous benefits and policy conflicts, with evidence and reason codes; straight-through processing for passing cases.
WL-20 Record acceptance metrics and safety metrics: drop-off, time to affirm, exception rate, false-clearance, false-hold, policy publication errors and sponsor-specific support burden.
WL-21 Contributions, fund transfers, scheduled plans and fee consent have their own scoped disclosures; never reuse grant-purpose affirmation for a bank debit mandate.
WL-22 Provide safe default legal template library as illustrative starting points, not legally approved universal language; sponsor counsel approves final text.

## Challenge log
D1 **Separate presentation from policy.** Reason: brand flexibility without unsafe semantics. Objection: extra configuration layers. Resolution: one sponsor admin UI backed by distinct typed services.
D2 **Canonical term is GrantRecommendation, aliases only in presentation.** Reason: interoperable APIs and audits. Objection: partners may require alternate field names. Resolution: explicit versioned API adapters; never mutate canonical ledger model.
D3 **No universal blanket disclaimer.** Reason: donor benefits and permissible grant structures can be nuanced. Objection: complex policy. Resolution: counsel-approved common baseline plus conditional questions.
D4 **Explicit affirmations.** Reason: evidence and donor accountability. Objection: click fatigue. Resolution: concise grouped disclosures, progressive explanation and approved standing attestations.
D5 **Standing affirmation not indefinite.** Reason: facts and rules change. Objection: recurring grants become high friction. Resolution: event-triggered refresh and sponsor-approved validity windows.
D6 **Sponsor overrides are constrained.** Reason: client autonomy cannot bypass law or audit. Objection: less white-label freedom. Resolution: configurable presentation and stricter policy with protected invariants.
D7 **Sponsor is legal grantmaker even when UI says distribution.** Reason: donor advisor is not personally making sponsor grant. Objection: confusing copy. Resolution: context-specific legal explanation.
D8 **AI may classify purpose and suggest questions, not self-certify donor statements.** Reason: only authorized human can make personal representations. Objection: manual step. Resolution: one minimal donor interaction at meaningful authorization boundary.
D9 **Do not use a single affirmation for all actions.** Reason: recurring debit mandate, grant purpose, and fee consent differ. Objection: more forms. Resolution: consolidate UX but retain distinct evidence records.
D10 **Versioned publication and rollback.** Reason: policy mistakes can affect many sponsors. Objection: operational burden. Resolution: automated validation, simulations, staged rollout, only exceptions for human reviewers.

## Example donor statements (not final legal text)
- I am recommending this distribution for a charitable purpose and understand the sponsoring organization retains final authority.
- Neither I nor any related person will receive an impermissible personal benefit from this distribution.
- This recommendation is not intended to purchase tickets, goods, services, or other benefits for me or a related person.
- This recommendation will not satisfy a personal legally enforceable pledge or obligation where prohibited under applicable law and sponsor policy.
- I have disclosed any potential benefits or commitments connected with this recommendation.

## Test cases
1. Sponsor A displays 'Recommend a Grant'; Sponsor B displays 'Recommend a Distribution' for identical canonical command.
2. Widget cannot submit without required affirmation token/version; prechecked client-side boxes do not count.
3. Material recipient or purpose change invalidates affected affirmation.
4. Recurring schedule executes only under currently valid standing attestation and applicable sponsor rules; otherwise requests renewed confirmation.
5. Sponsor policy attempts to allow prohibited personal benefit: publication rejected.
6. Legal wording changes mid-draft: show current text and require renewed affirmation.
7. Different sponsor tenants have isolated branding, policy and consent records.
8. Donor discloses event ticket benefit: conditional review/block per validated rule, not blanket assertion that all event gifts are identical.
9. Accessibility and localized terminology preserve legal meaning.
10. Audit reconstructs exactly which statement the donor saw and affirmed.
11. AI-originated grant suggestion cannot attest on donor's behalf.
12. Paper check mailed to donor does not alter sponsor grantmaker identity or benefit restrictions.

## Dependencies
Sponsor counsel must validate precise legal prohibitions and exceptions under IRC 4967, 4966, 170 and applicable IRS guidance and state law; no legal conclusion is asserted by this document. Link OD-01, OD-14, OD-19, OD-21, donor UI D06/D14, charity assurance, recurring plans, fee consent, widgets and financial core. Status remains proposed.
