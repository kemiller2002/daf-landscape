# DAF Administration Core: Master Requirements v0.1

Status: proposed, not implemented or legally approved. This is a requirements baseline for a US donor-advised fund sponsoring-organization platform, not a legal conclusion. Integrates financial core v0.5, enterprise UI catalog, UI vertical slices, and UX system v0.2.

## Mission and boundaries
Administer the entire sponsor-fund-donor-advisor relationship from prospect to closure, with accurate legal authority, policy enforcement, financial integration, human service, evidence and audit. The sponsoring organization retains legal control of contributed assets; donor/advisor recommendations are advisory, not instructions binding the sponsor. Avoid treating a DAF as a donor-owned brokerage account.

Platform model: multi-sponsor, multi-tenant, multiple legal entities, fund types, brands and custodians. F# modular monolith, API-first, Limen WASM, Forma components, Folio documents, managed data services, no required Kubernetes/Terraform. External charity facts are ingested with provenance into an internally owned registry; no dependency on Candid for canonical identity. Payment execution is a later gated capability, but its lifecycle and integration contracts are requirements now.

## Administration domains and priorities
| ID | Domain | P | Fundamental objects | Main outcomes |
|---|---|---|---|---|
| ADM-01 | Sponsor/legal entity setup | 0 | Sponsor, LegalEntity, Jurisdiction, Brand, PolicyBundle | legally scoped operation |
| ADM-02 | Prospect and relationship intake | 1 | Prospect, Household, Organization, Contact, Relationship | qualified onboarding |
| ADM-03 | Fund establishment | 0 | FundApplication, Fund, FundType, Agreement, Checklist | approved activated fund |
| ADM-04 | Agreements and amendments | 0 | AgreementTemplate, Execution, Amendment, Consent, Version | effective governing terms |
| ADM-05 | Parties and roles | 0 | Party, PartyIdentity, FundRelationship, Capacity | distinguish donor/advisor/beneficiary |
| ADM-06 | Authority and succession | 0 | AuthorityGrant, Delegation, SuccessorPlan, Trigger | enforce effective rights |
| ADM-07 | Sponsor policies | 0 | PolicyBundle, Rule, EffectiveWindow, Exception | versioned consistent decisions |
| ADM-08 | Fund restrictions and purpose | 0 | Restriction, Purpose, BeneficiaryClass, Consent | enforce lawful scope |
| ADM-09 | Contributions and acceptance | 0 | ContributionIntent, Asset, Diligence, Acceptance | accepted and received assets |
| ADM-10 | Fund accounting interface | 0 | FundBook, Allocation, LedgerLink, Period | reconciled fund activity |
| ADM-11 | Investments and custody | 1 | CustodyAccount, Mandate, PoolInterest, Authorization | managed assets |
| ADM-12 | Grant administration | 0 | Recommendation, Review, Decision, Grant | sponsor-approved grant |
| ADM-13 | Charity eligibility | 0 | Charity, Evidence, EligibilityDecision, Review | verified recipient |
| ADM-14 | Fees and billing | 0 | FeeSchedule, Tier, Accrual, Waiver, Invoice | accurate fee assessment |
| ADM-15 | Fund spending and distribution | 0 | SpendingPolicy, Capacity, Reserve, Allocation | controlled recommendations |
| ADM-16 | Donor/advisor service | 1 | ServiceCase, Preference, ContactEvent, SLA | traceable service |
| ADM-17 | Communications | 1 | Template, Notice, Consent, DeliveryReceipt | accurate notifications |
| ADM-18 | Documents and records | 0 | Document, Classification, Retention, LegalHold | authoritative records |
| ADM-19 | Reporting and statements | 0 | Statement, Disclosure, TaxAcknowledgment, Export | timely correct reporting |
| ADM-20 | Compliance and oversight | 0 | Control, Review, Conflict, Escalation, Evidence | accountable decisions |
| ADM-21 | Fund lifecycle changes | 0 | Suspension, Merge, Split, Transfer, Closure | controlled transitions |
| ADM-22 | Sponsor governance | 1 | BoardApproval, Committee, Minutes, Resolution | governed institution |
| ADM-23 | Partner and white-label service | 1 | Partner, Agreement, SLA, Configuration | safe delegated operations |
| ADM-24 | Financial sustainability | 1 | Revenue, Cost, Subsidy, ProfitabilityMeasure | sponsor economics |
| ADM-25 | Data migrations and corrections | 0 | ImportBatch, SourceMap, Reconciliation, Correction | trustworthy transition |
| ADM-26 | Operational resilience | 0 | Incident, Runbook, Recovery, ContinuityTest | reliable service |
| ADM-27 | AI-native operations | 1 | DecisionPackage, EvidenceGraph, Suggestion, Review | fewer manual steps |
| ADM-28 | Security and privacy | 0 | Principal, Scope, Session, AuditEvent | least-privilege isolation |
| ADM-29 | Institutional analytics | 1 | KPI, Cohort, Benchmark, Attribution | measured effectiveness |
| ADM-30 | External integration management | 0 | Provider, Capability, Credential, Sync, Observation | reliable data movement |

## Critical domain distinctions
1. Sponsor owns/controls contributed assets; donors and advisors may have recommendation privileges under governing terms.
2. Fund is a sponsor-administered accounting/administrative arrangement; a fund may map to multiple investment accounts and pools.
3. Party is a person or organization; relationship is role-specific, fund-specific, legally scoped and effective-dated.
4. Establishment is not activation: applications, agreement execution, identity checks, sponsor acceptance, initial contribution, and custodian provisioning can occur independently.
5. Recommendation, sponsor approval, payment preparation, provider acceptance, settlement and reconciliation are distinct.
6. Donor acknowledgment of a contribution is distinct from fund statements, valuation opinions, and tax advice.
7. Fee schedule, fee assessment, waiver and ledger posting are independently versioned and auditable.
8. Restrictions can arise from sponsor policy, governing agreements, law, donor intent accepted by sponsor, or grant conditions; hierarchy and conflicts need explicit resolution.
9. Sponsor policy exceptions require an authority and evidence trail; AI cannot grant exceptions.
10. Sponsor organizational structure may contain chapters, brands, service partners and investment managers, but legal control boundaries cannot be erased by UI branding.

## Full lifecycle
Prospect -> application -> due diligence -> agreement proposal -> sponsor acceptance -> executed terms -> activation -> funding -> ongoing administration -> advisory changes -> restrictions/amendments -> possible suspension -> merge/split/transfer/termination -> final reconciliation -> closure -> retention/archival. Every transition has preconditions, actor authority, effective date, evidence, ledger/custody impact, external notifications, reversibility policy and idempotency.

## Nonfunctional mandatory requirements
- Trusted command boundary derives principal, tenant, legal entity and authority; no caller-asserted identity.
- Bitemporal effective and recorded dates for legal authority, agreements, restrictions and decisions.
- Event/audit evidence with immutable source references, control owner, execution outcome, and retention classification.
- Configurable policy bundles with deterministic evaluation and version pinning; human-readable rationale.
- State machines with invalid transition rejection, concurrency/version checks and safe replay.
- No direct editing of posted financial entries; corrections use controlled reversing/adjustment processes.
- WCAG 2.2 AA target, mobile-first, meaningful loading, recovery and Folio accessible exports.
- Multi-currency only with explicit FX valuation, fee and accounting policies; no implicit conversion.
- Data provenance and freshness for external custody, charity, identity, payment and compliance sources.
- AI produces prepared cases, draft communications and suggestions; never self-authorizes a financial action.
- SOC 2 control claims must have actual execution evidence; documentation alone does not establish compliance.

## Immediate release focus
P0 includes sponsor/legal scope, establishment, agreements, parties/authority, policy/restrictions, contribution acceptance, grants/eligibility, fee engine, lifecycle, records, finance interfaces, security, migration and resilience. A donor portal without these cannot replace a DAF administrator.

## Open decisions
Sponsor types and jurisdictions; fund product taxonomy; minimums; advisory privileges; successor triggers; policy exceptions; investment manager authorities; tax acknowledgment practices; fees and revenue sharing; grant recipient classes; fund transfers and closures; state charitable solicitation requirements; regulatory and tax obligations. All require sponsor/legal/compliance validation, not assumed universal rules.
