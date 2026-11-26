# 12 - Declarative sponsor configuration package (B3)

Status: research draft (2026-11-26). Not legal advice. Evidence classes per 01-research-methodology.md.

Scope: turn institutional sponsor onboarding from a services project into a native product capability. Onboarding ends in one
machine-readable, versioned **Sponsor Configuration Package (SCP)** that is validated, simulated, approved and deployed
reproducibly into the sponsor's tenant cell on the single Unbound release. No custom software fork. Companion files:
[`18-integration-onboarding.md`](18-integration-onboarding.md) (integrations the package references),
[`19-participant-onboarding.md`](19-participant-onboarding.md) (donor/advisor/charity journeys the package parameterises),
[`data/sponsor-config-schema-outline.json`](data/sponsor-config-schema-outline.json) (schema outline). Sources: [`data/sources-CFG.csv`](data/sources-CFG.csv).

## Summary

- **The requirement base already exists but is scattered over ~40 IDs.** CNV-GOV-005 (versioned, effective-dated policy with independent approval and shadow replay), REQ-X-045 (declarative validated configuration), RR-REQ-X-057-r1 ("operating models MUST differ only by declarative configuration, role assignments, adapters and view composition"), UNB-SMP-CFG-001..003 (outcome questionnaire, policy packs, configuration register), RR-UNB-TEN-011-r1 (tenant lifecycle with `ReadinessValidated` gate) and CNV-ECO-005 (integration register blocks readiness). What is missing is **one artifact that binds them**: a single package with a hash, a dependency graph and a deterministic validation pipeline. (INFERENCE, High)
- **Release 1 scope is narrower than the brief's vocabulary.** Owner decision OD-P-GOV cut I (appended to CNV-GOV-005 in `clauses/c8_owner_decisions.json`) says release 1 uses *one sponsor-adopted configuration per sponsor*; platform-published policy packs and cross-sponsor shadow evaluation are deferred, and replay uses *that sponsor's own history*. The SCP is therefore designed as a per-sponsor package with platform **defaults** (not adoptable cross-sponsor packs); UNB-SMP-CFG-002 and RR-UNB-RULE-019-r2 should be read as post-release-1. (VERIFIED-FACT from repo, High)
- **New sponsors have no "own history" to replay.** Because CNV-EXP-002 obliges migration of each donor's full predecessor history with a reconciliation report, the migrated history is the natural shadow-replay corpus; for greenfield sponsors the synthetic operating year (`requirements/convergence/2026-11-24-master/16-SYNTHETIC-OPERATING-YEAR-AND-INTERNAL-TIME-STUDY.md`) is the fallback. This turns migration (a switching cost) into simulation evidence (a differentiator). (RECOMMENDATION, Medium)
- **Comparable practice converges on four mechanisms**: declarative desired state with immutable version history (OpenGitOps [CFG-001]); a reviewable plan/diff before apply (Terraform plan [CFG-002], Workday Object Transporter pre-migration diff and prerequisite checks [CFG-004]); validate-without-deploy with tests (Salesforce `checkOnly` and quick deploy within 10 days [CFG-003]); product behaviour as versioned configuration or code with simulation (Mambu Configuration-as-Code YAML [CFG-005], Thought Machine smart contracts with simulation [CFG-006]). None of these covers legal-perimeter checks; that layer is Unbound-specific. (VERIFIED-FACT / VENDOR-CLAIM per source, Medium-High)
- **The legal-perimeter layer is the moat-relevant part.** Funds-flow conformance (CNV-LEG-001, UNB-XIN-REG-001), payment role table (CNV-PAY-001), operator status register (UNB-XIN-REG-002), non-removable capabilities (CNV-GOV-006) and the precedence lattice (CNV-EXP-003) are machine-checkable. Incumbents' onboarding evidence (implementation fees, multi-stage migrations) suggests these checks are performed by people today (see `research/revenue-retention-and-switching-2026-11-11.md`, H1/H2). (INFERENCE, Medium)
- **Approval is not one click.** CNV-GOV-003/005 and CNV-PLT-010 require author ≠ approver, independent approval of material changes regardless of direction, and A4 sponsor-officer adoption; CNV-GOV-004 bars Unbound staff from A3+ authority. The SCP lifecycle encodes these as state-transition guards. (VERIFIED-FACT from repo, High)
- **"No fork" needs an enforcement mechanism, not a promise.** Recommendation: a closed extension-point catalogue (configuration items in the Configuration Register, adapters behind versioned contracts, template slots, Brand Kit tokens, view composition); anything outside it is a product backlog item for all sponsors. Feature flags may not vary financial/legal semantics per tenant (UNB-XIN-SAS-002). (RECOMMENDATION, High)
- **Several brief items need narrowing to stay inside ratified decisions**: "investment options" can only list options made available by the sponsor's external manager (CNV-LEG-001 baseline text, OD-M-07: no sponsor-maintained pools); "SLAs" can only be declared as candidate SLO targets until benchmark and pilot evidence (CNV-ARC-001, UNB-XIN-SAS-008); "custodian/payment integrations" are references to certified integrations, never credentials (UNB-API-STD-005).

## 1. Why native onboarding matters competitively

| Observation | Evidence class | Source |
|---|---|---|
| TIFIN/GiveClear disclose SaaS implementation fees plus subscription; AEF's Ren migration was multi-stage | VERIFIED-FACT (filings summarised in prior work), Medium | `research/revenue-retention-and-switching-2026-11-11.md` (R04-R06, R10) |
| Sponsor-kept platform swap is possible but requires recreating portal, identities, reports, historical access | VERIFIED-FACT, Medium | `data/switching-cost-control-matrix-2026.csv` row L04 |
| Entry segment is mid-size national/single-issue and advisor-distributed sponsors (5,000-50,000 funds) | VERIFIED-FACT (ratified) | CNV-ECO-004 |
| Onboarding plans must schedule every activation gate (board delegation, auditor approach, ODFI and rail agreements, controller policies) | VERIFIED-FACT (ratified) | CNV-ECO-005 |

INFERENCE (Medium): for the entry segment the binding constraint on time-to-live is *governance and contracts* (board delegation, ODFI agreement, rail partner, auditor), not software setup. A declarative package does not shorten counterparties' lead times, but it (a) makes every gate visible from day one, (b) lets configuration, validation and simulation run in parallel with contracting, and (c) removes Unbound implementation labour from the critical path. The competitive claim must stay bounded (CNV-GOV-007: competitive claims carry dated evidence). No public data on incumbent implementation durations was found; see open questions.

## 2. Requirement map (existing IDs the design binds)

| Design element | Existing requirement IDs |
|---|---|
| One codebase, operating models differ only by configuration/adapters/view composition | RR-REQ-X-057-r1, RR-UNB-PLAT-008-r1 (AC-4 same release), CNV-ARC-001 ("one codebase SHALL serve all operating models"), UNB-TEN-002 |
| Declarative, validated, versioned sponsor configuration | REQ-X-045, ADM-027, ADM-048, UNB-TEN-010, UNB-GAP-025, `research/daf-theoretical-enterprise-validation/19-questions/SPONSOR-CONFIGURATION-POLICY-LIFECYCLE-AND-ISOLATION-2026-11-23.md` |
| Policy versioning, effective dating, material-change approval, emergency path, shadow replay, activation dependencies | CNV-GOV-005 (+ OD-P-GOV cut I; ADV-R2-064 usability wording), UNB-GEX-024, GOV-AUTH-018 |
| Outcome questionnaire (≤15 questions) with derivation trace; configuration register; defaults | UNB-SMP-CFG-001, UNB-SMP-CFG-003, UNB-SMP-CFG-002 (defaults only in release 1) |
| Precedence lattice and static checks at adoption | CNV-EXP-003 (as amended by ADV-R2-051) |
| Non-removable capabilities; justified human steps | CNV-GOV-006, UNB-XIN-SAS-001 (NonRemovable catalogue) |
| Entitlements per tenant/program | UNB-XIN-SAS-001 |
| Funds-flow and perimeter | CNV-LEG-001, UNB-XIN-REG-001, UNB-XIN-REG-002, CNV-PAY-001 |
| Payment destination evidence, rail exposure | CNV-PAY-002, RR-REQ-X-005-r1, UNB-RCN-GRT-017, CNV-PLT-012 |
| Fees | CNV-FIN-002, UNB-XIN-ERP-001, ADM-028 |
| Accounting / book-of-record | CNV-FIN-012, CNV-FIN-007, ACC-MDL-001 |
| Custodian / investment | CNV-FIN-013, UNB-CUST-001..028, CNV-LEG-001 (external manager only) |
| Identity, SSO, realms, step-up | CNV-PLT-003, UNB-XIN-IAM-001..005, AUTH-I8, RR-UNB-TEN-004-r1 |
| Roles, delegated authority, SoD | CNV-GOV-003, CNV-GOV-004, CNV-GOV-010, UNB-RCN-PLT-005, GOV-AUTH-001..026, CNV-GOV-007 (cumulative limits) |
| Approval workflows / case kernel | CNV-GRT-001, CNV-GRT-011, CNV-SVC-001, RR-REQ-X-048-r1 |
| Brand, terminology, templates | REQ-X-030, UNB-RCN-PLT-007 (protected terms), RR-REQ-X-029-r1, CNV-EXP-001, CNV-PLT-001, UNB-XIN-CRM-003 |
| Retention | CNV-PLT-004, CNV-PLT-009, UNB-TEN-008 |
| SLOs / service levels | UNB-XIN-SAS-008, CNV-ARC-001, CNV-SVC-002, ADM-033 |
| Tenant lifecycle and activation | RR-UNB-TEN-011-r1, UNB-RCN-WF-009, UNB-TEN-011, UNB-RCN-PLT-012, CNV-ECO-005 |
| Assistance metadata for every configuration field | CNV-AIO-001, RR-REQ-X-051-r1 |
| Process versioning, rollout, change control | CNV-ARC-005, UNB-XIN-SAS-002, UNB-XIN-SAS-003, CNV-PLT-010 |
| Sandbox tenants | UNB-XIN-SAS-010 |

## 3. Comparable practice

| System | Mechanism relevant to SCP | What Unbound should copy | What it does not cover | Source / class |
|---|---|---|---|---|
| OpenGitOps | Desired state declarative; stored immutable, versioned with complete history; pulled and continuously reconciled by agents | Package as immutable versioned desired state; drift detection between active package and tenant config records | Approval, legal checks | [CFG-001] VERIFIED-FACT, High |
| Terraform `plan` | Execution plan previews changes without applying; saved plan files can be applied later and are "potentially-sensitive" | `plan` artifact (diff + impact) hashed and the *approved plan* (not the package) is what deploys | Domain simulation | [CFG-002] VERIFIED-FACT, High |
| Salesforce Metadata API | `checkOnly` deploy validates without changing the org; tests run at chosen level; validated set can be quick-deployed within 10 days | Validate-only mode; approval bound to a validation result with expiry | Legal perimeter | [CFG-003] VERIFIED-FACT (via doc search summary; direct page fetch returned 403), Medium |
| Workday Object Transporter | Moves configuration between tenants; checks source for blocking errors, then prerequisites in target; pre-migration diff; post-migration tenant compare; packages limited to 300 instances with dependencies | Dependency closure, prerequisite check against target cell, post-deploy compare report | Simulation of financial outcomes | [CFG-004] VERIFIED-FACT, High |
| Mambu Configuration as Code | Loan/deposit product configuration via YAML GET/PUT; PUT deletes products absent from YAML (deactivates if used) | Whole-module replace semantics; **never delete used items, deactivate prospectively** | Approval, perimeter | [CFG-005] VERIFIED-FACT (doc search summary), Medium |
| Thought Machine Vault | Products defined as Python smart contracts from a product library, simulated before launch | Treat policy behaviour as versioned, testable artifacts; library of defaults | Unbound deliberately rejects sponsor-authored code (no fork) | [CFG-006] VENDOR-CLAIM, Medium |
| Stripe Accounts v2 | Role-based "configurations" (merchant/customer/recipient) enable capability sets; adding a configuration reuses identity data already collected; close requires listing all applied configurations | Capability-set modules; reuse collected facts; destructive actions must restate full current state | Sponsor governance | [CFG-007] VERIFIED-FACT, High |

INFERENCE (Medium): Unbound's differentiator is not configuration-as-code (commodity) but **configuration-as-evidence**: each value carries derivation, authority, legal basis, simulation result and approver, and the package cannot activate while a mandatory dependency (contract, delegation, certified integration) is unresolved (CNV-GOV-005 last sentences; CNV-ECO-005).

## 4. Design

### 4.1 Package structure

```
SponsorConfigurationPackage
  manifest        : packageId, tenantId, legalSponsorId, version (semver), parentVersion, hash (SHA-256 over canonical JSON),
                    schemaVersion, platformReleaseRange, effectiveFrom, authoredBy, derivation (questionnaireRunId)
  modules[]       : one per domain (Section 4.2); each = { moduleId, version, items[], materiality, owners }
  items[]         : { itemId (Configuration Register key, UNB-SMP-CFG-003), value, source (derived|default|sponsorChoice|counselDeviation),
                    derivationRuleId?, legalBasis?, overrideDirection (tightenOnly|lengthenOnly|sponsorChoice|none),
                    nonRemovable: bool, assistanceContractId (RR-REQ-X-051-r1) }
  references[]    : external artefacts by id+hash only: contracts (ODFI, rail partner, custodian, MSA), board resolutions,
                    appointments (CNV-GOV-004), integration certifications (doc 18), counsel determinations (UNB-XIN-REG-002)
  dependencies    : derived DAG item -> {decisionId | referenceId | integrationId}; unresolved mandatory edge blocks activation
```

Hard rules: no secrets or credentials in a package (credential *references* to the vault only, UNB-API-STD-005, UNB-CUST-017); no PII except named
officer principal IDs; no executable code; no free-form HTML (RR-REQ-X-029-r1).

### 4.2 Modules (brief scope -> design and constraints)

| Module | Content (examples) | Release-1 constraint / mapped IDs | Materiality default |
|---|---|---|---|
| `identity.legalEntities` | Legal sponsor, EIN, program(s), distribution partners, fund types, isolation profile | UNB-RCN-PLT-001 distinct entities; Profile B default (RR-UNB-PLAT-008-r1) | Material |
| `brand` | Brand Kit ref, colours (contrast-checked), logos, domains | REQ-X-030, CNV-EXP-001 (compile fails on contrast) | Non-material unless disclosures touched |
| `terminology` | Label overrides | UNB-RCN-PLT-007 protected-term registry | Material if touches protected term (then rejected) |
| `policies.grants` | Eligible recipient classes, minimums, deep-review interval (≤180 d, tighten only), tier-2 triggers, pledges policy, international (entitlement) | CNV-GRT-002/003/010/011, UNB-XIN-SAS-001 | Material |
| `policies.contributions` | Accepted asset types/rails, completed-gift rule table refs, minimums | CNV-FIN-003, UNB-RCN-FIN-012, CNV-PAY-008 (cards deferred) | Material |
| `restrictions` | Mission/charity restrictions, prohibited benefits affirmations | CNV-GRT-009, CNV-EXP-003 precedence | Material |
| `fees` | Fee schedule versions (basis, day count, minimums, payer) | CNV-FIN-002, UNB-XIN-ERP-001 | Material (customer rights) |
| `accounting` | Book-of-record function map, grant recognition point, chart mapping, ERP integration ref | CNV-FIN-012, CNV-FIN-007, ACC-MDL-001 | Material |
| `investments` | Option menu *published by the sponsor's external manager*; manager agreement ref; custodian integration refs | CNV-LEG-001 (no sponsor-maintained pools, no Unbound selection), UNB-XIN-REG-002 | Material |
| `payments` | Role table (Originator = sponsor), ODFI ref, rail partners + exposure limits, fallback, destination evidence table, positive pay | CNV-PAY-001/002, CNV-PLT-012, UNB-RCN-GRT-017 | Material |
| `integrations` | References to certified integrations (doc 18) with scope | CNV-ECO-005, UNB-CUST-018, UNB-XIN-SAS-006 | Material when write-scoped |
| `identity.providers` | Workforce IdP (OIDC/SAML), SCIM, partner federation, customer realm settings, step-up matrix overrides (tighten only) | UNB-XIN-IAM-001..005, CNV-PLT-003, AUTH-I8 | Material |
| `network` | Allowed origins for widgets, IP allowlists for sponsor workforce, webhook endpoints | INT-015, UNB-XIN-SAS-004 | Material (security) |
| `authority` | Roles, appointments (refs), approval thresholds, quorum, cumulative limits | CNV-GOV-003/004/010, CNV-GOV-007, CNV-GRT-001 | Material |
| `workflows` | Case routing, clocks, assignment modes, timing defaults | CNV-SVC-001, CNV-GOV-005 (timing defaults are candidates) | Material if deadlines change |
| `communications` | Template slot texts, classification, sender entity, channels | RR-REQ-X-029-r1, CNV-PLT-001, UNB-XIN-CRM-003 | Non-material unless classification/sender changes |
| `reporting` | Statement cadence, board report, exports | CNV-PLT-005, CNV-GOV-008 | Non-material |
| `retention` | Schedule (≥ floors), legal holds config | CNV-PLT-004 (sponsor compliance owner approves) | Material; lengthen only |
| `regulatory` | Jurisdiction gates, state registrations, screening scope ref | CNV-LEG-002, CNV-GRT-006/015, UNB-RCN-GRT-007 | Material |
| `serviceLevels` | Candidate SLO targets, servicing class, surge plan ref | UNB-XIN-SAS-008, CNV-SVC-002, UNB-XIN-ADV-001 | Non-material (but cannot be published as SLA before evidence) |
| `entitlements` | Optional capabilities with contract ref | UNB-XIN-SAS-001 | Material |

### 4.3 Lifecycle (package version state machine)

`Draft -> SchemaValid -> SemanticallyValid -> PerimeterCleared -> Simulated -> ApprovalPending -> Approved -> Scheduled -> Active -> Superseded`,
with side exits `Rejected` (from any validation state, with rule IDs), `Withdrawn` (author, before Approved), `Expired` (approval older than
validity window; analogous to Salesforce's 10-day quick-deploy window [CFG-003]; candidate 30 days) and `RolledBack` (Active -> prior version re-activated
prospectively).

| Transition | Guard | Failure behaviour |
|---|---|---|
| Draft->SchemaValid | JSON Schema (data/sponsor-config-schema-outline.json) passes; every item has a Configuration Register entry and an AssistanceContract | `SCHEMA_INVALID` with JSON pointer; no partial acceptance |
| ->SemanticallyValid | All rules S-* in Section 5 pass | `SEMANTIC_INVALID`, list of rule IDs |
| ->PerimeterCleared | All rules P-* pass, including funds-flow conformance | `PERIMETER_BLOCKED`; cannot be overridden by any sponsor or Unbound role; only a counsel determination reference can clear rules that name one |
| ->Simulated | Replay criteria met (4.5) | `SIMULATION_INSUFFICIENT` (coverage) or `SIMULATION_DIVERGENCE` (unexplained outcome change) |
| ->Approved | SoD guards (4.4) | stays ApprovalPending; approvals invalidated if package hash changes (GOV-AUTH-009) |
| ->Scheduled | effectiveFrom ≥ now; not inside a sponsor close window or platform peak freeze unless emergency path (UNB-XIN-SAS-003) | `FREEZE_WINDOW` |
| ->Active (first activation) | Tenant `ReadinessValidated` (RR-UNB-TEN-011-r1); UNB-RCN-WF-009 program activation A4 command; every mandatory dependency resolved (CNV-GOV-005, CNV-ECO-005) | `DEPENDENCY_UNRESOLVED` naming the decision/contract/integration |
| Active->RolledBack | single versioned action; in-flight process instances keep the version they started with (CNV-ARC-005) | Rollback itself is a new effective-dated version; never rewrites issued decisions |

### 4.4 Approval and segregation of duties

| Change class | Required approvals | Source |
|---|---|---|
| Any change | Author ≠ approver; author self-approval impossible | CNV-GOV-005 |
| Material (financial controls, eligibility, permissions, customer rights; ambiguous or mixed = material) | Independent approver *plus* affirmative adoption by an A4 sponsor officer appointed by board resolution | CNV-GOV-005, CNV-GOV-004, UNB-SMP-CFG-002 (attestation pattern) |
| Changes to deterministic release-gate policy | Approvers must have no authoring/publish/deploy rights over the gate, else third distinct person | CNV-GOV-003 |
| Touches a non-removable or perimeter item | Rejected (no approval path) | CNV-GOV-006, CNV-LEG-001 |
| Counsel deviation from a default with `overrideDirection` violation | Counsel deviation record + sponsor A4 | UNB-SMP-CFG-002 |
| Emergency mandatory change (statute, bank instruction) | Separately authorized path, impact analysis, independent retrospective review | CNV-GOV-005 |
| Unbound staff | May author drafts on sponsor's behalf under ServiceDelegation; may never approve or adopt (no A3+) | CNV-GOV-004, CNV-TEN-001, UNB-XIN-IAM-002 |
| AI agents | May prepare drafts and explanations (A1); cannot approve or publish | CNV-AIO-001, GOV-AUTH-003 |

### 4.5 Simulation (shadow replay)

Per CNV-GOV-005 and OD-P-GOV cut I, release-1 replay uses the sponsor's own history:

1. **Corpus**: (a) migrated predecessor history imported under CNV-EXP-002 / RR-REQ-X-061-r1 (`ImportedToStaging` or later), (b) after go-live, the sponsor's own decisions, (c) greenfield: the synthetic operating year fixture. Evidence pinned per decision (RR-UNB-RULE-019-r2 pattern).
2. **Run**: evaluate both the predecessor rules (as reconstructed, or prior SCP version) and the candidate SCP over the corpus; produce a per-decision diff of outcomes (approve/hold/decline, fee amount, recognition date, routing, deadline).
3. **Pass criteria** (CNV-GOV-005: volume, risk coverage, rollback readiness, not elapsed time): declared minimum decision volume; every risk stratum touched by changed items has ≥ N replayed decisions (N declared per stratum, candidate); every changed outcome is classified *expected* (traceable to an intended item change) or *unexplained*; zero unexplained changes in financial-integrity outcomes; rollback rehearsed in the sandbox tenant (UNB-XIN-SAS-010).
4. **Output**: hashed simulation report bound to the package hash; approvers approve the report, not just the package.

### 4.6 Reproducible deployment and "no fork"

- Deploy = compile approved package to effective-dated configuration records inside the tenant cell in one transaction per module, idempotent on (packageHash, moduleId). Post-deploy, a compare report (actual config records vs package, cf. Workday tenant compare [CFG-004]) must show zero drift; drift later raises an incident.
- Same package hash + same platform release => same configuration state; the package records the `platformReleaseRange` it was validated against; a release outside the range forces re-validation (cf. CNV-ARC-004 version precondition).
- **Extension-point catalogue** (exhaustive): Configuration Register items; adapter implementations behind versioned contracts certified per doc 18; template slots and tokens; Brand Kit tokens; view composition; entitlements. Anything else is a product change for all sponsors under CNV-PLT-010 change control. Feature flags are ReleaseToggle/KillSwitch only and may not vary semantics by tenant (UNB-XIN-SAS-002).

### 4.7 Illustrative package skeleton (YAML, abbreviated, synthetic values)

```yaml
manifest:
  packageId: scp-0001
  tenantId: tnt-7f3c            # immutable, independent of DB/schema name (UNB-TEN-001)
  legalSponsorId: ls-example-foundation
  version: 1.0.0
  parentVersion: null
  schemaVersion: scp/0.1
  platformReleaseRange: ">=1.0.0 <1.1.0"
  effectiveFrom: 2027-03-01T00:00:00-05:00
  derivation: { questionnaireRunId: oq-2027-001 }   # UNB-SMP-CFG-001
modules:
  identity.legalEntities:
    legalSponsor: { name: "Example Charitable Fund", ein: "00-0000000", isolationProfile: B }
    programs: [ { programId: prg-core, distributionPartnerId: null } ]
  terminology:
    overrides: { "fund": "Giving Account" }        # 'grant recommendation' is protected (UNB-RCN-PLT-007)
  policies.grants:
    eligibleRecipientClasses: [ PublicCharity509a1_a2, PrivateOperatingFoundation, Government170c1 ]
    minimumGrantUsd: 50
    deepReviewIntervalDays: { value: 180, overrideDirection: tightenOnly }   # CNV-GRT-003
    pledgePolicy: NonBindingOnly                                             # CNV-GRT-010
  fees:
    schedules:
      - scheduleId: fee-std-v1
        basis: AverageDailyBalance
        dayCount: Actual365
        tiers: [ { upToUsd: 500000, annualBps: 60 }, { aboveUsd: 500000, annualBps: 40 } ]
        minimumAnnualUsd: null
        payerSource: Fund
  accounting:
    functionMap: { programLedger: Unbound, entityGL: External, payroll: External }   # CNV-FIN-012
    grantRecognitionPoint: SponsorApproval                                          # CNV-FIN-007 sponsor policy
  investments:
    externalManagerAgreementRef: { refId: doc-ima-01, sha256: "<hash>" }
    optionMenuSource: integration:custodian-01     # options published by the manager; Unbound does not select
  payments:
    roleTable: { originator: legalSponsor, odfiAgreementRef: doc-odfi-01, tpsp: Unbound }   # CNV-PAY-001
    railPartners: [ { integrationId: rail-01, maxFundsInTransitUsd: 2000000, fallback: SponsorOriginatedACH } ]
    destinationEvidenceTableRef: det-v1            # UNB-RCN-GRT-017
  identity.providers:
    sponsorWorkforce: { protocol: OIDC, issuer: "https://idp.example.org", scim: true, privilegedAuthenticator: AAL3 }
    customerRealm: { federations: [ { partnerId: null } ], proofingProfile: risk-based-v1 }  # CNV-PLT-003
  authority:
    appointments: [ { appointmentRef: board-res-2027-02, decisionClasses: [GrantApproval], limitUsd: 250000, expires: 2028-02-28 } ]
    cumulativeLimitWindowDays: 30                  # CNV-GOV-007 candidate
  communications:
    templates: [ { eventType: GrantPaid, slotOverrides: { intro: "..." }, classification: TransactionalOrRelationship } ]
  retention: { scheduleRef: ret-v1, approvedBy: officer:compliance-owner }   # CNV-PLT-004
  serviceLevels: { sloTargets: candidate, publishedSla: false }               # CNV-ARC-001
references:
  - { refId: doc-odfi-01, kind: OdfiAgreement, status: Executed, sha256: "<hash>" }
  - { refId: board-res-2027-02, kind: BoardResolution, sha256: "<hash>" }
```

## 5. Validation rule catalogue

Layer key: SCH schema; SEM semantic/referential; PER legal perimeter; NRM non-removable and precedence; DEP readiness dependencies; SIM simulation; APR approval.

| Rule | Layer | Check | Failure code | Requirement IDs |
|---|---|---|---|---|
| SCH-01 | SCH | Package validates against schema version declared in manifest | SCHEMA_INVALID | REQ-X-045 |
| SCH-02 | SCH | Every item key exists in Configuration Register with approved disposition (not `eliminate`/`platform-owned`) | ITEM_NOT_REGISTERED | UNB-SMP-CFG-003 |
| SCH-03 | SCH | Every item has a published AssistanceContract | ASSISTANCE_MISSING | CNV-AIO-001, RR-REQ-X-051-r1 |
| SCH-04 | SCH | No secret-shaped values (keys, tokens, account numbers in clear) | SECRET_IN_PACKAGE | UNB-API-STD-005, UNB-CUST-017 |
| SCH-05 | SCH | Canonical hash recomputes to manifest hash | HASH_MISMATCH | UNB-DOC-001 (integrity pattern) |
| SEM-01 | SEM | All references resolve to stored artefacts with matching hash | REFERENCE_UNRESOLVED | CNV-GOV-005 |
| SEM-02 | SEM | Fee schedule declares basis, day count, accrual/settlement cadence, minimum, payer | FEE_SCHEDULE_INCOMPLETE | CNV-FIN-002, UNB-XIN-ERP-001 |
| SEM-03 | SEM | Book-of-record function map names exactly one authoritative book per entity and basis | DUPLICATE_BOOK | CNV-FIN-012 |
| SEM-04 | SEM | Every role referenced in workflows exists in authority module; every command class in AuthorityMatrix | UNCLASSIFIED_COMMAND | CNV-GOV-010 |
| SEM-05 | SEM | Appointments have expiry, scope, independence attestation; no person appointed for reserved authority at another sponsor | APPOINTMENT_INVALID | CNV-GOV-004 |
| SEM-06 | SEM | Approval routes satisfy three-distinct-person rule until deterministic-release preconditions recorded | SOD_ROUTE_INVALID | CNV-GOV-003 |
| SEM-07 | SEM | Templates: tokens in event allowlist; mandatory clauses locked; each template classified; Commercial has postal address | TOKEN_NOT_ALLOWED / UNCLASSIFIED_TEMPLATE / MISSING_POSTAL_ADDRESS | RR-REQ-X-029-r1, CNV-PLT-001, UNB-XIN-CRM-003 |
| SEM-08 | SEM | Brand compiles; every colour pair meets contrast | CONTRAST_FAIL (pair named) | CNV-EXP-001 |
| SEM-09 | SEM | Terminology overrides do not alter protected terms | PROTECTED_TERM | UNB-RCN-PLT-007, REQ-X-030 |
| SEM-10 | SEM | Identity mapping uses issuer+subject or SCIM externalId, never email | IDENTITY_KEY_UNSTABLE | AUTH-I8 |
| SEM-11 | SEM | Step-up policy overrides only increase assurance or reduce max auth age | STEPUP_WEAKENED | UNB-XIN-IAM-003 |
| SEM-12 | SEM | Privileged sponsor roles bound to AAL3 authenticators | AAL_INSUFFICIENT | CNV-PLT-003 |
| SEM-13 | SEM | Timing defaults do not shorten statutory/contractual deadlines | DEADLINE_SHORTENED | CNV-GOV-005, CNV-ARC-005 |
| SEM-14 | SEM | Rail partners each have approved funds-in-transit limit, status-query and segregated-holding contract terms | RAIL_TERMS_MISSING | CNV-PLT-012 (+ ADV-R2-059) |
| SEM-15 | SEM | Destination evidence combinations equal the ratified set; cooling-off ≥ 1 business day | DESTINATION_EVIDENCE_WEAK | CNV-PAY-002 (+ ADV-R2-010/067), UNB-RCN-WF-028 |
| SEM-16 | SEM | Check void days ≤ shortest applicable state window | VOID_WINDOW_INVALID | CNV-PAY-002 |
| SEM-17 | SEM | Entitlements reference contract; NonRemovable capabilities not NotEntitled | ENTITLEMENT_INVALID | UNB-XIN-SAS-001 |
| SEM-18 | SEM | Each WorkItem-creating rule declares expected volume and the human decision | WORKITEM_UNJUSTIFIED | UNB-RCN-PLT-006, CNV-GOV-006 |
| PER-01 | PER | FundsFlow: every money-holding account titled to sponsor or its custodian; Unbound instruction-only | FUNDS_FLOW_NONCONFORMANT | CNV-LEG-001, UNB-XIN-REG-001 |
| PER-02 | PER | Payment role table: Originator = sponsor; Unbound never Originator; ODFI agreement executed for activation | ProhibitedRole / ODFI_AGREEMENT_MISSING | CNV-PAY-001 |
| PER-03 | PER | No configuration lets Unbound execute or indefinitely block a payment other than CNV-PLT-007 protective hold | UNILATERAL_CONTROL | CNV-LEG-001, CNV-PLT-007 |
| PER-04 | PER | Investment module: no sponsor-maintained pool; options sourced from external manager; no Unbound selection or asset-varying compensation | INVESTMENT_PERIMETER | CNV-LEG-001, UNB-XIN-REG-002 |
| PER-05 | PER | Each status-relevant feature enabled has a counsel determination for this deployment and jurisdiction set | STATUS_DETERMINATION_REQUIRED | UNB-XIN-REG-002 |
| PER-06 | PER | Jurisdiction-gated capabilities (e.g. California D2C) off until opinion recorded | JURISDICTION_GATED | UNB-XIN-SAS-001, CNV-LEG-002 |
| PER-07 | PER | No per-donation compensation to solicitors in fee/partner module | SOLICITOR_COMP_PROHIBITED | CNV-LEG-001 |
| PER-08 | PER | Card contributions off in release 1 | FEATURE_DEFERRED | CNV-PAY-008 |
| NRM-01 | NRM | Retention ≥ floors; legal hold overrides disposition; sponsor compliance owner approval present | RETENTION_BELOW_FLOOR | CNV-PLT-004 |
| NRM-02 | NRM | Accessibility, audit, tenant isolation, financial integrity, mandatory compliance not disabled | NON_REMOVABLE | CNV-GOV-006 |
| NRM-03 | NRM | Rules checked against precedence lattice (law > platform non-removable > board policy > program terms > fund agreement > donor preference); same-level conflicting rules rejected | POLICY_CONFLICT | CNV-EXP-003 (+ ADV-R2-051) |
| NRM-04 | NRM | Deep review interval ≤ 180 days; refresh 30 days before expiry; fail-safe when stale cannot be disabled | GRT003_WEAKENED | CNV-GRT-003 |
| NRM-05 | NRM | Sanctions screening at onboarding, approval and release cannot be disabled | SCREENING_REQUIRED | CNV-GRT-006 |
| NRM-06 | NRM | Shared-store participation (charity registry, holds) limited to SharedStoreRegister fields; no PII | SHARED_STORE_VIOLATION | CNV-TEN-001, CNV-GRT-004 |
| NRM-07 | NRM | Feature flags not used for tenant semantic variation | FLAG_SEMANTICS | UNB-XIN-SAS-002 |
| DEP-01 | DEP | Every activation element maps to decision IDs and evidence; unresolved mandatory dependency blocks | DEPENDENCY_UNRESOLVED | CNV-GOV-005 |
| DEP-02 | DEP | Each external dependency in integration register with contract status, cost bearer, lead time, fallback | INTEGRATION_NOT_READY | CNV-ECO-005, UNB-CUST-018 |
| DEP-03 | DEP | Referenced integrations hold a current certification covering requested scopes (doc 18) | CERTIFICATION_MISSING | UNB-CUST-024, UNB-XIN-SAS-006 |
| DEP-04 | DEP | Tenant isolation decision and passing isolation suite for chosen profile | ISOLATION_UNVERIFIED | UNB-RCN-PLT-012, RR-UNB-PLAT-008-r1 |
| DEP-05 | DEP | Board delegation, contract, legal-sponsor disclosure, opening balances tied out, finance readiness certified by different principal | PROGRAM_ACTIVATION_BLOCKED | UNB-RCN-WF-009, RR-UNB-TEN-011-r1 |
| DEP-06 | DEP | Capacity forecast acknowledged when onboarding adds >10% accounts in 60 business days | CAPACITY_ACK_REQUIRED | UNB-SMP-ECN-002 (proposed) |
| DEP-07 | DEP | December readiness: surge plan present if go-live within the surge window | SURGE_PLAN_MISSING | CNV-SVC-002 |
| SIM-01 | SIM | Replay volume and stratum coverage meet declared minimums | SIMULATION_INSUFFICIENT | CNV-GOV-005 |
| SIM-02 | SIM | Zero unexplained changed outcomes in financial-integrity classes | SIMULATION_DIVERGENCE | CNV-GOV-005, UNB-GEX-024 |
| SIM-03 | SIM | Rollback rehearsed in sandbox tenant | ROLLBACK_UNREHEARSED | CNV-GOV-005, UNB-XIN-SAS-010 |
| APR-01 | APR | Author cannot approve; approvals bound to package hash and simulation report hash | SELF_APPROVAL / APPROVAL_STALE | CNV-GOV-005, GOV-AUTH-009 |
| APR-02 | APR | Material change has independent approval + A4 adoption | ADOPTION_REQUIRED | CNV-GOV-005, CNV-GOV-004 |
| APR-03 | APR | No Unbound principal or AI agent in approver set | PROHIBITED_APPROVER | CNV-GOV-004, CNV-AIO-001 |

## Implications for Unbound

1. RECOMMENDATION: add a normative requirement for the **SCP as the single activation artefact** (manifest, hash, modules, references, dependency DAG) that subsumes REQ-X-045 and binds CNV-GOV-005, RR-UNB-TEN-011-r1 and UNB-RCN-WF-009 to one hash.
2. RECOMMENDATION: make the **validation rule catalogue normative and versioned**, with each rule a golden-fixture test (CNV-GOV-007 golden fixtures first for highest decision risk: PER-*, NRM-*).
3. RECOMMENDATION: specify **migrated predecessor history as the replay corpus** for new sponsors (refines CNV-GOV-005 release-1 cut; uses CNV-EXP-002 output).
4. RECOMMENDATION: publish an **extension-point catalogue** and a release check that fails if tenant-specific code paths appear (refines RR-REQ-X-057-r1).
5. INFERENCE: the outcome questionnaire (UNB-SMP-CFG-001) plus derivation trace is the sales-facing surface of this capability; CNV-GOV-005 (ADV-R2-064) already requires moderated usability testing with a recorded task-success criterion.
6. Competitive messaging must stay bounded: "configuration and validation in parallel with contracting" is defensible; "go live in N weeks" is not until pilot evidence exists (CNV-ECO-003, CNV-GOV-007).

## Open questions / evidence gaps

- No public data on incumbent sponsor implementation duration or effort (Ren, TIFIN Give, Chariot, Blackbaud/Foundant for comparison); only fee-type disclosures. Evidence task: ADV/contract disclosures, RFP responses, customer interviews (with consent).
- Package validity window for approved-but-not-deployed versions (candidate 30 days) needs owner decision.
- Stratum definitions and minimum N per stratum for replay are undefined (CNV-GOV-005 "representative").
- Whether UNB-SMP-CFG-001/002/003 (status: proposed) will be adopted; this design assumes CFG-003 (register) and treats CFG-002 as defaults only in release 1.
- Who authors the reconstructed "predecessor rules" for diffing migrated history (Unbound under ServiceDelegation vs sponsor), and the liability allocation (CNV-GOV-005 responsibility matrix).
- Salesforce and Mambu details were taken from documentation search summaries because direct fetches were blocked (403) or partial; Thought Machine claims are vendor blog statements; Workday docs may change.
