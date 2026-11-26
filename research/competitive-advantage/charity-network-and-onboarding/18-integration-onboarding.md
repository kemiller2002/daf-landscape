# 18 - Integration onboarding and automated certification (B9)

Status: research draft (2026-11-26). Not legal advice. Evidence classes per 01-research-methodology.md.

Scope: a standard onboarding and certification path for every external integration a sponsor needs (custodians, banks/ODFIs, grant-rail
partners and payment processors, identity providers, professional-advisor firms, sponsor websites/widgets, external accounting/ERP, payroll
contribution systems, file and API integrations), with automated certification and a self-service readiness assessment. The machine-readable
test catalogue is [`data/integration-certification-suite.csv`](data/integration-certification-suite.csv); sources in [`data/sources-CFG.csv`](data/sources-CFG.csv).
The sponsor configuration package that *references* certified integrations is in [`12-declarative-sponsor-configuration.md`](12-declarative-sponsor-configuration.md).

## Summary

- **Requirements already demand certification before production but do not define it.** UNB-CUST-024 (synthetic fixtures, sandboxes, contract tests, negative authorization, replay/idempotency, reconciliation, recovery drills "before production authorization"), UNB-PAY-007 (simulated payment adapter and deterministic contract tests), UNB-API-STD-003/005, UNB-XIN-SAS-006 ("certification status" on app registration), CNV-ECO-005 (integration register; readiness false while a mandatory dependency lacks contract or fallback) and RR-UNB-TEN-011-r1 ("provider integrations passing contract tests" to go Live). Missing: lifecycle states, scope-limited certificates, expiry/recertification, and a per-type test catalogue. This document supplies them (89 tests: 76 type-specific across 10 integration types plus 13 common). (INFERENCE, High)
- **External precedent shows three distinct things that are often conflated**: (1) *provider-run conformance programs* where implementers self-test with free tools and a body validates and publishes certificates (UK Open Banking functional conformance; OpenID Foundation self-certification) [CFG-012, CFG-013, CFG-014]; (2) *provider sandboxes* with simulated events and time (Plaid Sandbox `fire_webhook`, `reset_login`; Stripe sandboxes, test clocks, stripe-mock) [CFG-008, CFG-009, CFG-010]; (3) *counterparty message validation* against usage guidelines (Swift MyStandards Readiness Portal; ODFI test files) [CFG-018, CFG-020]. Unbound needs all three, from both sides: certify inbound adapters against counterparties' sandboxes, and offer counterparties a readiness portal against Unbound's contracts. (VERIFIED-FACT for each program, Medium-High)
- **Certification passed in test does not equal production authorization.** OBIE certifies against production unless agreed otherwise, and notes regulators may require more evidence [CFG-012]. Unbound should issue a **scoped certificate** (integration type, direction, scopes, file/API version) and require a **shadow-live** phase (read-only or parallel run on production) before write scopes activate. (RECOMMENDATION, High)
- **US wealth custodians mostly do not offer self-service certification.** Schwab publishes that daily data files and APIs exist (APIs via Schwab OpenView Gateway provided by PTI) and that not all listed third parties have integration agreements; a 2021 announced developer portal had sample data and test integrations, current status unverified [CFG-023, CFG-024, CFG-025]. Aggregators (BridgeFT) market normalized multi-custodial APIs, but their public custodian list excerpt did not confirm Schwab/Pershing coverage [CFG-026]. Custodian onboarding will remain contract-gated with a long lead time; certification must work from recorded file samples. (VERIFIED-FACT/VENDOR-CLAIM, Medium)
- **US open-finance certification is immature.** FDX publicly stated it did not yet offer a certification program and planned one; CFPB recognised FDX as a standard setter (Jan 2025) [CFG-015, CFG-016]. Do not plan around an FDX certificate. (VERIFIED-FACT, Medium; current status not confirmed)
- **ACH file certification is ODFI-specific.** Nacha publishes a developer guide; ODFIs add their own header/format requirements and require sample test files [CFG-019, CFG-020]. Nacha fraud-monitoring Phase 2 (rule date 19 June 2026, a federal holiday, so effectively the next banking day, 22 June, matching CNV-PAY-001) applies to TPSPs [CFG-022]. Certification must be per ODFI, and fraud-monitoring evidence is part of it. (VERIFIED-FACT, High)
- **Echelon gives little of the harness.** Strata's deterministic mock interactions (STRATA-DIV-001) are requirements only; Limen has no IdP/session capability and cannot mount as an embedded widget; Fides is GitHub-only; Vigila is an untagged task-organizer pilot (07-ECHELON-CAPABILITY-ASSESSMENT.md). Unbound must own provider mock contracts, the certification runner and the readiness portal (already the recorded position under CNV-ARC-004 and STRATA-GAP-01). (VERIFIED-FACT from repo, High)

## 1. Integration taxonomy and authority boundary

| Type | Examples | Direction | Authority boundary (never crossed by an integration) | Requirement IDs |
|---|---|---|---|---|
| CUST custodian / investment manager | Custodian daily files, manager positions/units/valuations | Inbound read; outbound instructions only where contract and sponsor authority permit | Unbound never selects investments or routes orders for others (CNV-LEG-001) | UNB-CUST-001..028, CNV-FIN-013, CNV-LEG-001 |
| BANK sponsor bank / ODFI | BAI2/camt.053 activity, positive pay issue files, ACH origination files | Both | Sponsor is Originator; Unbound is TPSP (CNV-PAY-001) | CNV-PAY-001/002/005/007, UNB-PAY-008 |
| RAIL networked grant-rail partner | Charity disbursement networks acting as sponsor's agent | Outbound instruction; inbound status | Partner acts as sponsor agent; exposure limits; status queries (CNV-PLT-012) | CNV-PAY-001, CNV-PAY-004, CNV-PLT-012, CNV-EXP-002 |
| PROC contribution processor | ACH debit, DAF-to-DAF, stock transfer intake | Inbound | Settles into sponsor-owned accounts only (CNV-LEG-001) | CNV-FIN-003, UNB-XIN-REG-001 |
| IDP identity provider | Sponsor workforce IdP (OIDC/SAML+SCIM), partner federation, proofing vendor | Inbound assertions | Step-up by sponsor-controlled verifier, not partner IdP (UNB-XIN-IAM-003) | CNV-PLT-003, UNB-XIN-IAM-001..005, AUTH-I8 |
| ADV professional-advisor firm | Firm roster/HR via SCIM, advisor entitlements | Inbound | Firm cannot grant advisory privilege; holder consent required (UNB-XIN-CRM-007) | UNB-WF-012, UNB-XIN-CRM-007, UNB-PART-003 |
| WEB sponsor website / widget | Embedded giving/status widgets, hosted pages | Outbound UI + API | Scoped read-only defaults, origin checks (INT-015); no money scopes (UNB-XIN-SAS-006) | ADM-037, INT-015, WG-2, WG-9, UNB-RCN-GRT-012 |
| ERP external accounting | Entity GL journal export, vendor master import | Outbound journals; inbound balances | One authoritative book per entity; stale balance fails safe (CNV-FIN-012) | CNV-FIN-012, UNB-ACC-022 |
| PAY payroll contribution | Employer payroll deduction files | Inbound | High-volume workplace giving not offered in release 1 without funding commitment (CNV-ECO-004) | CNV-ECO-004, CNV-FIN-003 |
| API third-party application | Partner apps using public APIs, webhooks | Both | No scopes to approve grants, move money, change payees (UNB-XIN-SAS-006) | UNB-XIN-SAS-004/006, UNB-API-STD-001..006 |

## 2. Real-world certification and testing programs

| Program | What it certifies / provides | Mechanism worth copying | Limits noted by the source | Source / class |
|---|---|---|---|---|
| UK Open Banking conformance (OBL/OBIE) | Functional, security-profile and DCR conformance of ASPSP APIs; customer-experience checklist | Free open-source tools (MIT), self-attestation, central validation and published certificate per base URL; certification against production unless agreed | Running tools is evidence, but a regulator may require more | [CFG-012], [CFG-013] VERIFIED-FACT, Medium (some pages on consultation site) |
| OpenID Foundation certification | OIDC/FAPI implementations | Free conformance suite; self-certification; listed certified implementations | Fee schedule separate | [CFG-014] VERIFIED-FACT, High |
| FDX (US) | Planned voluntary certification of FDX API implementations | Standard-setter recognition by CFPB | Program not confirmed live | [CFG-015], [CFG-016] VERIFIED-FACT, Medium |
| Plaid Sandbox | Test institutions, credentials, Sandbox-only endpoints to fire webhooks and force error states; Limited Production then full Production access application | Fault injection endpoints; staged production access | Sandbox data may be inconsistent across calls | [CFG-010] VERIFIED-FACT, High |
| Plaid Identity Match | Per-field match scores of user-provided name/address/phone/email against bank account-holder data; documented threshold 70 | Account-owner match as a certifiable capability of the funding-verification integration | Scores vendor-defined | [CFG-011] VERIFIED-FACT, High |
| Stripe sandboxes / test clocks / stripe-mock | Isolated sandboxes per team/CI; simulated time advance; mock server | Separate sandboxes for CI; **virtual time** for lifecycle tests | Some features unavailable in sandboxes | [CFG-008], [CFG-009] VERIFIED-FACT, High |
| Pact | Consumer-driven contract testing by example; each contract entry a concrete request/response pair | Adapter-side consumer contracts verified against provider sandboxes and against Unbound's own published APIs | Not a schema; covers only used interactions | [CFG-017] VERIFIED-FACT, High |
| Swift MyStandards Readiness Portal | Counterparties validate ISO 20022/MT message instances against an institution's usage guidelines; portals per customer or category | **Unbound-hosted readiness portal** validating counterparty files against Unbound's usage guidelines | Premium+ licence for publishers | [CFG-018] VERIFIED-FACT, Medium |
| Nacha developer guide / ODFI test files | ACH file layout; ODFIs require sample test files and run record-level validation | Per-ODFI file profile; sample-file certification | ODFI-specific variations | [CFG-019], [CFG-020] VERIFIED-FACT, Medium |
| Nacha WEB debit account validation | First-use account validation, method-neutral (prenote, micro-entries, third-party validation) | Funding-account validation test in PROC certification | Applies to WEB debits | [CFG-021] VERIFIED-FACT, High |
| Schwab daily data files / OpenView Gateway | Custody data files and APIs for advisor tech; SSO via PTI; announced developer portal with sample data (2021) | Treat as contract-gated; certify on recorded sample files | Not all listed providers have agreements; portal status unverified | [CFG-023], [CFG-024], [CFG-025] VENDOR-CLAIM, Medium |
| BridgeFT WealthTech API | Normalized multi-custodial data API | Possible aggregator path to reduce per-custodian adapters | Custodian coverage list not confirmed for Schwab/Pershing | [CFG-026] VENDOR-CLAIM, Low-Medium |

Fidelity (Fidelity Institutional/Wealthscape) and Pershing (NetX360/data feeds) feed specifications were **not publicly documented** in sources reached in this pass; treat as contract-gated (not evidence of absence).

## 3. Integration lifecycle

`Proposed -> Registered -> ContractCleared -> SandboxConnected -> Certifying -> Certified(scope, expiry) -> ShadowLive -> Live -> (Degraded <-> Live) -> Suspended -> Recertifying -> Retired`

| State | Entry guard | Exit / failure behaviour | IDs |
|---|---|---|---|
| Registered | Integration register row: counterparty, contract status, cost bearer, lead time, fallback, operational owner, data classes | Missing fallback for a mandatory dependency => sponsor readiness false | CNV-ECO-005, UNB-CUST-018 |
| ContractCleared | Executed contract (or sandbox terms) recorded; perimeter check that no flow routes money through Unbound | `FUNDS_FLOW_NONCONFORMANT` blocks permanently until redesign | CNV-LEG-001, UNB-XIN-REG-001, CNV-PAY-001 |
| SandboxConnected | Credentials in vault (rotation date set); sandbox/mock endpoint; tenant is Sandbox tenant only | Sandbox tenant cannot resolve production endpoints | UNB-XIN-SAS-010, UNB-CUST-017 |
| Certifying | Automated suite for the type runs; manual items recorded with evidence | Any `blocking` test failure => stays Certifying | UNB-CUST-024, UNB-API-STD-003 |
| Certified | Certificate = {integrationId, type, direction, scopes, contract/schema versions, ODFI profile, test-suite version, evidence hash, expiry} | Expiry (candidate 12 months), counterparty version change, or contract change => Recertifying | UNB-XIN-SAS-006 |
| ShadowLive | Production credentials; read-only or parallel-run: inbound data reconciled against existing source; outbound instructions generated but not sent (or sent via existing channel) | Reconciliation breaks above tolerance => back to Certifying | UNB-CUST-010, RR-UNB-ACC-018-r1 |
| Live | Sponsor A4 approval for write scopes (payments, instructions); sponsor configuration package references certificate | — | UNB-RCN-WF-009, CNV-GOV-005 |
| Degraded | Freshness SLO breached, malformed file, outage | Defined degraded mode: fail safe on stale balances, no invented balances, unknown outcomes to CNV-PAY-004 | UNB-CUST-022, CNV-FIN-012, CNV-PAY-004, UNB-RES-001 |
| Suspended | Revoked permission, security incident, sponsor disable | Tokens revoked within 5 min for apps; in-flight instructions to unknown-outcome process | UNB-XIN-SAS-006, CNV-PLT-012 |

## 4. Automated certification harness (design)

Components (all Unbound-owned until upstream equivalents exist):

1. **Provider mock contracts** (F#): deterministic simulators per counterparty type with virtual time, fault injection (timeouts, 5xx, partial files, duplicates, out-of-order, late corrections, returns/NOCs), recorded-sample replay. Adopt Strata DIV contracts when implemented (STRATA-GAP-01; CNV-ARC-004 says deterministic mocks are Unbound-owned provider contracts until then).
2. **Contract tests**: consumer-driven contracts for each adapter, verified (a) against the mock, (b) against the counterparty sandbox where one exists, (c) against recorded production samples in ShadowLive. Unbound's own public APIs publish provider contracts that third-party apps verify against (UNB-API-STD-003/006).
3. **Synthetic transaction packs**: per type, a fixed scenario set reusing the migration-runbook universal fixture (`research/migration-runbook-2026.md`) plus payment state dimensions (RR-REQ-X-083-r1).
4. **Validators**: schema (JSON Schema/XSD/Nacha layout), semantic (control totals, hash totals, balancing), usage-guideline validation per ODFI/custodian profile (MyStandards-style).
5. **Security/auth probes**: credential scope minimality, rotation, webhook signature verification, replay defence, tenant binding (forged tenant hints ignored, RR-UNB-TEN-004-r1).
6. **Invariant checker**: after each scenario, ledger balanced, no duplicate external effect, reconciliation zero-difference or classified, hold version recorded at dispatch (CNV-ARC-003).
7. **Evidence packager**: certificate plus evidence bundle hashed into the service-organization evidence class (CNV-PLT-009); rendered as accessible HTML first (Folio markup; PDF pipeline Unbound-owned per CNV-EXP-001).

Test categories (each row in the CSV carries one): `schema`, `contract`, `auth`, `synthetic-transaction`, `failure-simulation`, `replay`, `idempotency`, `reconciliation`, `security`, `accessibility`, `operational`, `legal-perimeter`. Automation levels: `full` (runs unattended in CI), `partial` (automated run, human evidence review), `manual` (document or counterparty attestation). Of 89 tests, the CSV marks 69 full, 13 partial, 7 manual (computed from the CSV; INFERENCE about achievable automation, Medium).

### Certification scoring and failure behaviour

- Tests are `blocking` (any failure prevents Certified) or `advisory`. All `legal-perimeter`, `idempotency`, `reconciliation` and `auth` tests are blocking.
- Certificate scope is the intersection of requested scopes and scopes whose tests passed (e.g. a custodian certified for positions/transactions but not for instructions stays read-only; UNB-CUST-005).
- A test that cannot run because the counterparty has no sandbox is recorded `not_executed` with the compensating evidence (recorded sample, counterparty attestation), never as passed (same discipline as `research/migration-runbook-2026.md`).

## 5. Self-service integration readiness assessment

Audience: sponsor operations staff and counterparties (custodian ops, ODFI treasury management, rail partner, IdP admin, firm IT). Output is a readiness report, not an approval.

| Step | Input | Automated probe | Output |
|---|---|---|---|
| 1 Classify | Pick integration type(s), direction, scopes | Maps to suite profile and required contract documents | Required evidence list, lead-time estimate from register history |
| 2 Contract & perimeter | Upload executed agreement metadata (not content unless needed), funds-flow diagram answers | Perimeter rules (PER-01..03 in doc 12) on declared flows | Blocking issues with explanation (AssistanceContract text) |
| 3 Connectivity | Endpoint/SFTP host, auth method | TLS, auth handshake, scope introspection, IP/origin allowlist check (sandbox) | Pass/fail per probe |
| 4 Sample validation | Upload sample files/messages (synthetic or de-identified) | Schema + usage-guideline validation; control totals | Line-level errors (MyStandards-style fix-and-revalidate) |
| 5 Behavioural | Run self-service subset in sandbox | Idempotency, replay, error-code mapping | Score per category |
| 6 Report | — | — | Readiness tier: `Not ready` / `Ready for certification` / `Certification-scheduled`; gaps with owners; never "Certified" |

Rules: samples containing real PII are rejected unless the uploader is in the sponsor tenant with a de-identification attestation (UNB-XIN-SAS-010 forbids production data in sandboxes); the assessment can never change integration state beyond `Registered` (AI and self-service are A1/A2 only; CNV-AIO-001).

## 6. Echelon capability review: dependencies and gaps

Source: `requirements/convergence/2026-11-24-master/07-ECHELON-CAPABILITY-ASSESSMENT.md` and `data/echelon-inventory.jsonl` (2026-11-24 read-only inspection).

| Component | Version/state | Role in integration onboarding | Dependency | Gap / Unbound position |
|---|---|---|---|---|
| Strata | v0.1.1 pilot, PostgreSQL 16 only | Schema governance for integration register and certificate tables | Schema migrations | **STRATA-DIV-001 (virtual time, fault injection, replay, Scenario Studio) is requirements only**; Unbound builds provider mocks; adopt DIV when implemented (STRATA-GAP-01) |
| Limen | 0.9.1, TS kernel, F# seam | Hosts readiness-portal and certification-console engines | Routing, forms (source-only) | No IdP/session/tenant token (LIMEN-GAP-02); no element/shadow-root mount, so sponsor-website widgets need Unbound embed profile (LIMEN-GAP-01, ADR-M-03) |
| Forma | 1.1.0 (channel pins 1.0.1) | UI for readiness wizard, certification results, task lists | form, task-list, work-queue, status-lozenge, data-grid | No money component, no status track, no chart primitives (FORMA-GAP-05/08/09); conformance evidence is Unbound's job (FORMA-GAP-29) |
| Folio | 0.4.1 tagged; markup only | Certificate and evidence-pack documents | print markup | No PDF renderer, no PDF/UA (FOLIO-GAP-14/15); accessible HTML is primary artifact |
| Vigila | untagged pilot "task organizer" | None | none | No release-1 dependency; do not use for certification workflow (CNV case kernel instead) |
| Conditor | tag 0.10.25; registry manifests to 0.10.19 | Installs pinned harness components reproducibly | Lock files | Registry lag; pin by manifest digest (FORMA-GAP-27 analogue) |
| Praxis | v3.25.0 mature | Requirement catalog and verification manifests linking tests (CSV `requirement_ids`) to requirements | Verification manifest compile | Needs conversion of Unbound CSV/MD to Praxis catalog (PRAXIS-GAP-01) |
| Dokimos | 0.11.1 | Records certification evidence against requirement IDs | Manifest-driven verification | No scenario/financial-invariant runner (DOKIMOS-GAP-01); F# tests feed it |
| Fides | 0.2.0, GitHub-only IdP | None | — | Managed OIDC IdP required (DG-05) |
| Licence | PolyForm Noncommercial across stack | — | — | Commercial licence before launch (CNV-GOV-009) |

INFERENCE (High): the certification harness is an Unbound build item with no upstream shortcut in release 1; it should be planned as product scope, not implementation services.

## Implications for Unbound

1. RECOMMENDATION: add an **IntegrationCertification** requirement defining the lifecycle above, scoped certificates with expiry, `not_executed` discipline, and ShadowLive before write scopes (refines UNB-CUST-024, UNB-PAY-007, UNB-XIN-SAS-006; binds CNV-ECO-005 readiness).
2. RECOMMENDATION: add a **Counterparty Readiness Portal** requirement (Unbound-published usage guidelines and validators for files/APIs Unbound consumes; MyStandards-style) so custodians, ODFIs and rail partners self-test before engineering time is spent.
3. RECOMMENDATION: **per-ODFI ACH profile** and Nacha fraud-monitoring evidence as part of BANK certification (refines CNV-PAY-001 TPSP obligations).
4. RECOMMENDATION: evaluate an aggregator (BridgeFT-type) adapter as a cost lever for advisor-distributed sponsors, subject to CNV-LEG-001 (read-only data, no advice) and data-rights review; INFERENCE, Low-Medium until custodian coverage verified.
5. Competitive point (INFERENCE, Medium): incumbents with integrated administration (Ren) hold integrations as a switching cost; a published certification catalogue plus readiness portal converts "integration risk" into a scheduled checklist for a switching sponsor. Bounded: it does not shorten custodian or bank contracting.

## Open questions / evidence gaps

- Current status of Schwab's developer portal and whether DAF sponsors (charities) are eligible data recipients vs only RIAs; Fidelity and Pershing feed specifications and eligibility.
- Which networked grant-rail partners offer sandboxes and status-query APIs (needed for CNV-PLT-012 contract terms); cross-reference Track A docs.
- Whether FDX certification has launched; whether any US bank offers OBIE-like conformance for corporate file channels.
- Certificate expiry period (candidate 12 months) and recertification triggers need owner decision.
- Whether payroll contribution integrations are in release-1 scope (CNV-ECO-004 suggests only with an employer funding commitment).
- Legal: whether Unbound's readiness portal holding counterparty sample files creates data-processing obligations; default to synthetic-only.
