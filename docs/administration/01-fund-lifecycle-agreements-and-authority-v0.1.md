# DAF Administration: Fund Lifecycle, Agreements, Relationships and Authority v0.1

Status: proposed domain contract, not implementation or legal advice.

## Fund establishment requirements
EST-01 Prospect intake from donor, advisor, sponsor staff or API partner with source attribution and consent.
EST-02 Person and organization identity resolution; support households, trusts, estates, companies and authorized representatives without conflating them.
EST-03 Fund type catalog: standard, endowed, designated, field-of-interest, memorial, scholarship or other sponsor-specific programs. Do not assume every product qualifies as a DAF; classification is a legal/policy determination.
EST-04 Sponsor/legal entity selection and applicable jurisdiction, governing agreement template, minimum contribution, restrictions, fee plan and investment options.
EST-05 Application draft and document intake with structured field provenance, saved progress and accessibility.
EST-06 Conflict/duplicate screening for existing funds, relationships and records.
EST-07 AML/sanctions/identity checks where applicable; distinguish legally mandated controls from sponsor risk policies and record their basis.
EST-08 Gift acceptance and source-of-funds review as required by asset and risk type.
EST-09 Review of proposed fund name, purpose, advisory rights, privacy and successor instructions.
EST-10 Sponsor acceptance and authorized sign-off, distinct from electronic agreement execution.
EST-11 Fund activation gates: executed effective terms, sponsor approval, required checks, financial book setup, authorized parties, custody configuration as needed.
EST-12 Activation receipt, unique fund ID, effective date, document package, service owner and donor notification.
EST-13 Exception and abandonment states: withdrawn, expired, rejected, pending evidence, approved-not-funded, funded-not-active, suspended.
EST-14 No automatic assumption that an initial contribution or signature alone activates a fund.

## Agreement model
AG-01 Versioned templates with legal owner, sponsor entity, jurisdiction, effective window, language, disclosure attachments and supersession chain.
AG-02 Executed document stored as immutable content-addressed artifact with signer identity, signing capacity, time, consent and proof; distinguish electronic signature provider evidence from legal sufficiency.
AG-03 Terms expressed as structured constraints where possible, with source clause references. Legal text remains authoritative; structured interpretation requires approval.
AG-04 Amendment proposal -> review -> consent/signature if required -> effective date -> policy recomputation -> notices.
AG-05 Conflicting terms between agreement, sponsor policy and law create a review case; never silently select favorable interpretation.
AG-06 Historic decisions preserve policy and agreement versions used when decided.
AG-07 Support donor-advisor letters of wishes as nonbinding where applicable, distinct from legally effective agreement changes.
AG-08 Retention and legal hold survive fund closure; signed originals remain traceable.

## Party/relationship graph
PARTY-01 Canonical person/organization records with alias, address, contact, tax and privacy attributes independently classified.
PARTY-02 Relationships: original contributor, subsequent contributor, primary advisor, co-advisor, successor advisor, investment advisor, authorized agent, service contact, sponsor officer, beneficiary organization, committee member.
PARTY-03 Relationship edge stores fund, sponsor/legal scope, capacity, start/end effective time, recorded time, evidence, constraints and authority grant reference.
PARTY-04 One person can hold multiple capacities; do not merge privileges or identity evidence.
PARTY-05 Households and family groups are presentation/relationship structures, not automatic legal authority.
PARTY-06 An advisor may service multiple funds and sponsors; every cross-fund query must be authorized independently.
PARTY-07 Identity corrections and merges retain provenance, previous IDs and audit trail.

## Authority and delegation
AUTH-01 Capability-based grants (view, recommend grant, propose investment, edit contact, manage advisor, access documents, approve sponsor decision, prepare payment, authorize payment, close books).
AUTH-02 Scope by tenant, sponsor, legal entity, fund, asset/account, amount, purpose, effective date and policy.
AUTH-03 Delegation can only grant a subset of the delegator's effective rights and requires sponsor rules.
AUTH-04 Separation of duties: originator, reviewer, approver, executor, reconciler can be distinct as policy requires.
AUTH-05 Expiration, revocation, suspension, emergency access and audit with precise effective and recorded times.
AUTH-06 Authority rechecked at command execution, not only at UI rendering.
AUTH-07 Successor rights activate only after verified trigger and sponsor review under governing terms; nomination is not activation.
AUTH-08 Death, incapacity, divorce, dissolution, trust changes and disputes are distinct events with evidence and privacy controls.
AUTH-09 Disputed authority places affected actions on hold without necessarily freezing unrelated fund activity.
AUTH-10 Platform support access is separately granted, time-limited, logged and reviewed; no silent superuser cross-tenant access.

## Succession
SUCC-01 Named successors, ordering, contingencies, multiple successors, shared decision rules, age/eligibility restrictions and expiry.
SUCC-02 Trigger types: death, incapacity, resignation, loss of eligibility, term expiry, other agreement-specific trigger.
SUCC-03 Evidence intake and independent verification; protect sensitive medical/estate information.
SUCC-04 Interim authority and restricted hold policy during verification.
SUCC-05 Transition notice to authorized parties and review of current grant drafts, recurring recommendations and pending actions.
SUCC-06 If no valid successor, sponsor policy and agreement determine disposition; do not invent automatic family inheritance.
SUCC-07 Revocation/reinstatement and dispute handling with legal escalation.

## Lifecycle transitions
| From | To | Guard | Evidence |
|---|---|---|---|
| Prospect | Application | required contact and consent | intake source |
| Application | UnderReview | application complete for selected product | checklist snapshot |
| UnderReview | Approved | sponsor authority and policy satisfied | decision record |
| Approved | Active | effective agreement and activation conditions | activation package |
| Active | Suspended | authorized legal/compliance/risk trigger | reason and scope |
| Suspended | Active | documented remediation and authority | release decision |
| Active | AmendmentPending | proposed terms and appropriate parties | amendment proposal |
| AmendmentPending | Active | valid approval/consent and effective date | executed amendment |
| Active | ClosurePending | sponsor policy and outstanding obligations reviewed | closure plan |
| ClosurePending | Closed | no unresolved obligations, final reconciliation and notices | final close packet |
| Any eligible | Terminated/Rejected | policy-specific lawful decision | documented reason |

## Complex lifecycle cases
- Fund rename without changing immutable ID.
- Fund type conversion where legally allowed and approved.
- Consolidation/merger with explicit historical lineage, donor intent, fee implications and reconciliation.
- Split of fund interests with allocation rules and conservation proof.
- Transfer to/from another sponsor, with legal review, asset/custody movement, grant obligations, records and donor notices.
- Dormant or inactive fund, spending policy and sponsor intervention.
- Closure after donor death or loss of valid advisor.
- Restrictions, disputes, legal holds, and pending grants during closure.
- Reopening closed fund requires a new authorized process; no simple state toggle.

## Required UI workspaces
Fund onboarding wizard, agreement review/signature tracking, party relationship graph, advisory rights matrix, succession plan editor, lifecycle timeline, fund amendment case, transfer/closure workbench. Each has accessible mobile and desktop representations, draft persistence and evidence-linked decisions.

## Required tests
Double application submit; agreement revised while signing; fund activated before prerequisites (must reject); advisor revoked mid-submission; successor nominated but not triggered; two successors conflict; fund merge with pending grants; closure with unresolved external payment; legal hold on records; cross-tenant household search leakage; stale client cache after authority change; backdated agreement effective date with recorded-date audit.
