# DAF Administration: Adversarial Review and Implementation Roadmap v0.1

Status: proposed analysis. No production software or regulatory compliance is verified.

## 25 adversarial scenarios and safeguards
| # | Scenario | Risk | Required safeguard |
|---|---|---|---|
| 1 | Donor labeled as fund owner | Misstates legal control | sponsor/fund/party authority separation |
| 2 | Signature before sponsor approval | premature activation | separate acceptance and execution gates |
| 3 | Successor nominated but trigger unverified | unauthorized access | contingent authority state |
| 4 | Donor dies with recurring grants | unauthorized continuation | reevaluate advisory rights and pending instructions |
| 5 | Two advisors disagree | contested recommendation | policy-defined quorum/priority and dispute hold |
| 6 | Trust representative changes | invalid delegation | effective-dated evidence and role recheck |
| 7 | Fund transferred with pending payment | duplicate/stranded obligation | settlement unknown-state reconciliation before transfer |
| 8 | Fund split with shared pooled cash | double allocation | conservation at all shared constraints |
| 9 | Fee tier misread as flat rate | overbilling | tested marginal tiers and reproducible calculation |
| 10 | Backdated fee waiver | hidden historical correction | versioned adjustment with audit |
| 11 | Fee assessed against stale NAV | incorrect charge | freshness gate and review |
| 12 | Grant to charity with changed identity | wrong recipient | canonical identity and effective-dated eligibility |
| 13 | Charity bank account changed | diversion risk | independent destination verification |
| 14 | Gift asset accepted with hidden liability | sponsor loss | asset-specific diligence and approval |
| 15 | Receipt issued before gift accepted | incorrect tax communication | acknowledgment state machine |
| 16 | Sponsor policy change conflicts with agreement | breach of terms | legal precedence case, no silent override |
| 17 | Restricted fund pays unrelated grant | misuse | constraint engine at approval and funding |
| 18 | Cross-sponsor advisor search leaks donors | privacy violation | scoped search, tenant isolation, negative tests |
| 19 | Legacy migration imports stale rights | unauthorized access | verify executed authority evidence |
| 20 | Opening fund balance omits payable | financial misstatement | reconciliation of liabilities and obligations |
| 21 | AI hallucinates agreement clause | unauthorized action | source-linked clause verification and human review |
| 22 | White label hides disclosures | compliance exposure | non-overridable disclosure component |
| 23 | SOC 2 control logged but never performed | false assurance | control execution evidence and reviewer |
| 24 | Closed fund has pending provider unknown | untracked cash movement | closure gate blocks unresolved external state |
| 25 | Board conflict not recorded | governance failure | disclosure, recusal and decision evidence |

## Policy versus law distinction
Do not assume every best practice is a legal requirement. Requirements must carry an authority classification: federal statute/regulation, state law, sponsor governing instrument, sponsor policy, provider contract, control framework, or design recommendation. Legal review is needed for sponsor type, jurisdiction, tax treatment, eligible grant categories, donor advisory rights, excise-tax restrictions, private benefit, scholarships and expenditure responsibility where applicable. Do not generalize across all sponsors.

## AI-native organizational redesign experiments
Experiment A: Fund opening. Compare conventional 20-field form with evidence-led prefill and progressive questions. Measure steps eliminated, missing evidence, staff review and error rate.
Experiment B: Charity review. Compare manual web research with internally sourced evidence graph and contradiction-first review. Measure time, false positive/negative decisions and source traceability.
Experiment C: Fee servicing. Compare invoice dispute case with explainable calculation and self-service fee trace. Measure support contacts and corrections.
Experiment D: Advisor succession. Compare manual documents and role toggles with event-triggered, evidence-verified activation. Measure incorrect rights and cycle time.
Experiment E: Fund closure. Compare checklist-driven manual coordination with dependency graph and automatically prepared closure packet. Measure stranded obligations and reopens.
Experiment F: Board approvals. Compare agenda email chains with role-aware decision packages, recusals and recorded votes. Measure elapsed time and missing evidence.
Experiment G: Migration. Compare CSV import with provenance-aware entity resolution and reconciliation-first cutover. Measure unidentified conflicts and financial variance.

Each experiment must define baseline, intervention, measurable success, failure cost, human review, and rollback. Do not use AI where deterministic computation or direct source integration is more reliable.

## Dependencies and build order
1. Legal ontology: sponsor, legal entity, fund classification, party, relationship, authority, agreement, restrictions.
2. Versioned policy evaluation, sponsor-specific terms, evidence and authorization decision.
3. Fund application and activation state machines, identity, document and audit primitives.
4. Fees, lifecycle transitions and service cases on top of canonical domain objects.
5. Integration with independently verified financial core, custody and charity registry.
6. Three administrative vertical slices: onboarding, succession/rights, fee assessment/closure.
7. Data migration with realistic legacy fixtures and independent reconciliation.
8. Mobile UI and Folio document validation with assistive technology and user testing.
9. AI automation experiments with measured reduction of human work and no control regression.
10. Sponsor-specific legal and production safety signoffs.

## What not to build first
- Generic CRM unrelated to fund authority and servicing.
- Fully configurable workflow scripting without typed policy boundaries.
- Live payment execution before provider idempotency, reconciliation and double-spend controls.
- Auto-approval of grants or asset acceptance from AI-generated conclusions.
- A dashboard with no operational decision paths.
- A universal 'fund owner' field.
- An all-purpose administrator superuser with unlogged tenant access.
- A tax-deduction calculator presented as legal advice.
- Unverified 'SOC 2 compliant' branding.

## Decision register
DEC-ADM-01 Fund is not donor-owned account: required architectural distinction.
DEC-ADM-02 Party/relationship/authority modeled separately: required.
DEC-ADM-03 Agreement clauses are source-of-truth; structured interpretations approved: required.
DEC-ADM-04 Policy precedence and exceptions must be explicit: required.
DEC-ADM-05 Fee assessment is deterministic and reproducible: required.
DEC-ADM-06 Successor nomination not automatic activation: required.
DEC-ADM-07 Fund closure requires external obligation resolution: required.
DEC-ADM-08 Sponsor product types and tax rules need counsel review: pending.
DEC-ADM-09 Custodian/provider capabilities need contract verification: pending.
DEC-ADM-10 AI workflow redesign must demonstrate measurable advantage: pending experiments.

## Exit criteria for requirements phase
Every P0 domain has owner, entity schema, event/state machine, command permissions, UI states, legal/policy authority, failure modes, API contracts, accounting integration, test fixtures and release gate. Unresolved questions are tracked explicitly rather than replaced with invented defaults.
