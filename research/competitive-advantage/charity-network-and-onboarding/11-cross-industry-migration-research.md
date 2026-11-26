# 11 - Cross-industry migration and onboarding research

Status: research draft (2026-11-26). Not legal advice. Evidence classes per 01-research-methodology.md.

Agent: XIN (Track B2). Data: [`data/cross-industry-migration-techniques.csv`](data/cross-industry-migration-techniques.csv) (24 techniques), [`data/migration-failure-cases.csv`](data/migration-failure-cases.csv) (7 cases), [`data/sources-XIN.csv`](data/sources-XIN.csv) (37 sources).

## Summary

- **Industries that made switching routine did it with a standard plus a guarantee plus a clock, not with better consultants.** ACATS (FINRA Rule 11870) requires validation within 1 business day, completion within 3 business days of validation, and allows exceptions only from a closed list [XIN-005]. The UK Current Account Switch Service (CASS) guarantees a 7-working-day switch with automatic redirection of misdirected payments. It completed 99.7% of 1.19m switches in 2024 within 7 working days and has redirected 160.5m payments since launch [XIN-009, XIN-010]. VERIFIED-FACT, High.
- **The most expensive public failures were operational and governance failures, not data-copy failures.** TSB's 2018 data "migrated successfully" [XIN-001], yet the bank paid £48.65m in penalties and £32.7m in redress and received 225,492 complaints. Testing "only concluded the day before the decision to migrate" [XIN-002]. Revlon's ERP go-live cost about $64m of unshipped sales and $53.6m of charges, and produced a material weakness in internal control [XIN-016]. VERIFIED-FACT, High.
- **Scale alone does not make a migration risky; rehearsal discipline does.** Schwab converted about $1.9T and more than 17m accounts in five transition groups, with attrition below its initial estimates [XIN-007]. CBA reports five dress rehearsals and a three-hour full outage for 16m accounts [XIN-024, VENDOR-CLAIM]. Unbound's entry sponsors hold 5,000–50,000 funds (CNV-ECO-004), three to four orders of magnitude fewer accounts than these banks. In DAF migration the hard part is heterogeneous legacy data and in-flight grant payments, not volume. INFERENCE, Medium.
- **Root causes, classified (§3):** the strongest public evidence points to *governance and schedule pressure* (an added category) and *weak tooling and testing*. Next come *domain-model mismatch* (Lidl), *inconsistent data*, and *vendor or consulting dependence* (Cover Oregon). Evidence for "poor software architecture" as a root cause is mostly vendor claims. INFERENCE, Medium.
- **Aggregate overrun statistics are directional only.** McKinsey and Oxford: large IT projects average 45% over budget and 7% over time, and deliver 56% less value than predicted [XIN-020]. Flyvbjerg and Budzier: average overrun 27%, with a fat tail [XIN-021]. Gartner predicts that more than 70% of recent ERP initiatives will miss their business-case goals by 2027 [XIN-023]. Standish CHAOS percentages are not used, because of documented methodology problems [XIN-022]. INFERENCE, Medium.
- **Three verified analogues upgrade existing Unbound proposals:**
  - ERISA blackout notice: 30–60 days' notice for any freeze longer than 3 business days [XIN-013]. UNB-XIN-OTH-002 had cited this as an unverified practice.
  - IRS Rev. Proc. 2004-53: one successor issues the whole year's W-2s, combining the predecessor's data [XIN-014]. The analogue is that one system issues a sponsor's cutover-year donor statements.
  - ONC EHI export: complete, self-service export in a published format, with no developer assistance [XIN-029]. The analogue is symmetric exit.
  VERIFIED-FACT, High (analogy: INFERENCE).
- **The ACATS and CASS mechanisms do not exist in DAF (§5.0; revised after adversarial review).** Both rest on regulatory compulsion, a central utility and obligations binding *both* counterparties. DAF has none of these:
  - Public incumbent terms limit extraction to direct-login reports or paid professional services, with deletion soon after exit (ADVB-02).
  - Donors have no legally enforceable right to a recommended grant (ADVB-03).
  VERIFIED-FACT, High.
- **Proposed competitive move (RECOMMENDATION): an *Unbound Migration Service Commitment* (§5), renamed from "Switching Guarantee".**
  - It covers **only the steps Unbound controls**, and its clock starts when a usable source extract is received.
  - It combines:
    - a published Migration Package schema that other vendors may adopt;
    - a closed intake-exception list;
    - timed rehearsals;
    - a legacy-reference crosswalk kept for at least 36 months;
    - a bounded Unbound-side freeze;
    - a single issuer of statements for the cutover year;
    - contractual exit terms that Unbound offers its own customers.
  - It makes no promise about the incumbent's behaviour or about donor-level sponsor-to-sponsor transfers. Unbound redirects references and instructions, never funds (CNV-LEG-001).
- **DAF-specific failure mode.** AEF's move to Ren is the only *national-sponsor* platform-change case found here. Draft 10 documents community-foundation cases. AEF imported 33 months of history, but its new portal shows two years; older records require a staff request (`research/revenue-retention-and-switching-2026-11-11.md`; adversarial verification ADVB-005).
  - CNV-EXP-002 (full history import with a reconciliation report) is a differentiator only as a *published, verifiable* outcome. Incumbents and adjacent vendors already sell migration services (ADVB-12).
  - VERIFIED-FACT, High (AEF); INFERENCE, Medium (differentiation).

## 1. Scope and relation to prior work

This file adds external, cross-industry evidence on migration and onboarding practice. It deliberately does not repeat:

- **The Unbound cross-industry discovery** (`unbound/requirements/discovery/2026-11-23-cross-industry/`; summarised in `daf-landscape/research/cross-industry-daf-operating-model-findings-2026-11-23.md`). It already proposes:
  - partner exit as per-fund transfer grants (UNB-XIN-SAS-007 and UNB-XIN-EVA-009, citing bulk ACATS transfers as an analogue);
  - a TransitionWindow notice (UNB-XIN-OTH-002);
  - versioned state machines for in-flight processes (UNB-XIN-WFA-002).
  That study rests on same-model research without primary-source verification. Here, several of its analogues are verified against primary sources.
- **The MigrationRun state machine** (`unbound/requirements/reconciliation/2026-11-23/07-REFINEMENT-RECORDS.md`, RR-REQ-X-061-r1). It runs Contracted > Inventoried > Mapped > ImportedToStaging > Reconciled > ParallelValidated > CutoverAuthorized > SingleWriterActive > PostCutoverVerified > Archived, and it fences the legacy writer and marks imported payees `imported_unverified`. Related rules: CNV-ARC-005 (per-tenant migration state) and UNB-CUST-023 (custodian migration history).
- **The DAF migration runbook** (`research/migration-runbook-2026.md`, acceptance tests M01–M20 and the portability schema) and the switching-cost control matrix (`data/switching-cost-control-matrix-2026.csv`).
- **Sibling deliverables in this package.** ONB (10) covers DAF-industry onboarding. MIG (13–17) covers DAF financial migration entities, reconciliation gates and cutover strategy. CFG (12) covers configuration and integration certification. Here, gates and cutover appear only at the level of cross-industry technique.

## 2. Evidence by industry

| Industry | Case or mechanism | What the evidence shows | Class / conf. | Source |
|---|---|---|---|---|
| Core banking | TSB 2018 (Proteo4UK) | ~5.2m customers. The platform was "not yet proven". Testing ran in parallel and was descoped to meet dates, concluding the day before the go decision. The outsourcer had 85 fourth parties. BAU returned 10 Dec 2018. £48.65m fines, £32.7m redress. | VERIFIED-FACT, High | XIN-001, XIN-002 |
| Core banking | TSB: Slaughter and May review (2019) | Coverage quotes the platform as "neither stable nor complete" and a "largely single event migration" adopted without sufficient consideration. TSB's board disputes parts. | VERIFIED-FACT (secondary), Medium | XIN-003, XIN-004 |
| Core banking | CBA SAP-on-AWS (2025–26) | Planned 3 dress rehearsals, ran 5. 8-hour cutover target; fully offline 3 hours. 18-month programme. The earlier 2008 programme was contracted at A$580m. | VENDOR-CLAIM, Medium | XIN-024, XIN-037 |
| Core banking | Nordea (Temenos) | EUR344m legacy impairment at the start. Product- and country-phased moves, e.g. ~250k Finnish savings accounts in 2018. Reported slow progress (2021). | VERIFIED-FACT (press), Low | XIN-025 |
| Core banking | Thought Machine / AWS (2026); Lloyds | Claims AI extraction of legacy product logic, "multi-year processes into days", with human sign-off gates. No figures. Lloyds planned 500k accounts. No primary evidence found for 10x or Mambu migration-cost claims. | VENDOR-CLAIM, Low | XIN-026, XIN-027 |
| Brokerage | ACATS / FINRA 11870 | Standard forms, 1+3 business-day clocks, closed exception list, clearing-agency processing. DTCC reports more than 70% of full transfers settling in 4 days after 2020 changes. | VERIFIED-FACT, High (DTCC figure: VENDOR-CLAIM) | XIN-005, XIN-006 |
| Custody / RIA | Schwab–TD Ameritrade (2023–24) | 5 transition groups; ~$1.9T; >17m accounts incl. 7,000 RIAs. Attrition below initial estimates. Total integration cost and capex expected at $2.4–2.5bn (whole acquisition). The advisor wave (Labor Day 2023) had minor position and pricing issues. | VERIFIED-FACT, High | XIN-007, XIN-008 |
| Payroll | Mid-year switching; IRS successor rules | New provider needs year-to-date and quarter-to-date history and proof of tax payments. The prior provider files completed quarters. Only one provider should issue W-2s. Rev. Proc. 2004-53 lets the successor assume the full W-2 obligation, combining both employers' wages. | VERIFIED-FACT, High (Gusto: Medium) | XIN-014, XIN-015 |
| Accounting / ERP | Revlon (2018) | $64m unshipped sales, $53.6m charges, material weakness tied to ERP implementation. | VERIFIED-FACT, High | XIN-016 |
| Accounting / ERP | Lidl eLWIS (2011–18) | Purchase-price vs retail-price inventory valuation mismatch; halted; ~€500m (unconfirmed). | press, Low | XIN-017 |
| Public sector | Queensland Health payroll (2010) | Vendor-recommended parallel pay run largely ignored (Auditor-General, per press); ~A$1.25bn (press). Primary report could not be fetched (HTTP 403). | press, Low | XIN-018 |
| Public sector | Cover Oregon (2014) | No independent systems integrator; state "largely dependent on the vendor"; contested blame. | press, Low | XIN-019 |
| Insurance | Closed-block administration | Legacy platforms kept alive 20–40 years; outsourcing or rule extraction before conversion (consultancy material). | VENDOR-CLAIM, Low | XIN-035 |
| Payments | Card-data portability between processors | The receiving processor provides its PCI AOC and PGP key; the sender encrypts and uploads by SFTP. Exports take "a few days to several months". An old→new ID mapping file is returned. A new MID may raise declines, so volume should be ramped. Stripe exports to "any PCI-compliant processor". | VERIFIED-FACT, High | XIN-028 |
| Healthcare | ONC §170.315(b)(10) EHI export; FHIR Bulk Data | Single-patient and population export of all EHI, computable, with a public format link, "without subsequent developer assistance". FHIR offers async NDJSON bulk export with `_since` deltas and SMART backend auth. | VERIFIED-FACT, High | XIN-029, XIN-030 |
| CRM | Salesforce loading guidance | Legacy IDs kept in indexed External ID fields; parent-before-child load order; deferred sharing recalculation. | VERIFIED-FACT, Medium | XIN-033 |
| Identity | SCIM (RFC 7644), SAML/OIDC | Standard cross-domain provisioning with bulk operations, intended "to reduce the cost and complexity of user management". | VERIFIED-FACT, High | XIN-031 |
| Cloud | AWS assess–mobilize–migrate | The landing zone is built in mobilize, and the migrate phase reuses patterns already tested. | VERIFIED-FACT, Medium | XIN-032 |
| Managed SaaS | Workday deployment | Foundation-tenant baseline; "configuration, not customization"; initial solution then expand. | VENDOR-CLAIM, Medium | XIN-034 |
| Open banking | UK CMA Order 2017; US CFPB §1033 | 9 largest UK providers mandated to adopt common APIs, roadmap completed Sept 2024. The §1033 rule was finalised in Oct 2024 and is under reconsideration (ANPR Aug 2025); its current status was not verified. | VERIFIED-FACT, Medium | XIN-011, XIN-012 |
| UK current accounts | CASS | 7-day guarantee, redirection plus sender notification, refund of interest and charges on failure; 99.7% within 7 days. | VERIFIED-FACT, High | XIN-009, XIN-010 |
| Retirement plans | ERISA blackout notice | 30–60 days' notice before restrictions longer than 3 business days; content rules. | VERIFIED-FACT, High | XIN-013 |

The per-technique implications for Unbound are in the techniques CSV. Each case's root causes and lesson are in the failure-cases CSV.

## 3. Why enterprise migrations become expensive and unpredictable

The brief's five categories are kept. A sixth, *governance and schedule pressure*, is added because it is the best-evidenced cause in the primary sources (TSB). Each assignment is INFERENCE from the cited facts.

| Cause | Evidence | Strength | Avoidable by product design? |
|---|---|---|---|
| **Unavoidable domain complexity** | Life policies administered for 20–40 years [XIN-035]. Payroll year-to-date and tax-quarter continuity [XIN-014, XIN-015]. For DAFs: pending in-kind gifts, approved-but-unpaid grants, uncashed checks, successor rights, tax-receipt history (runbook fixture). | Medium | No. It can only be modelled once, in the product, rather than per project. |
| **Domain-model mismatch** (customer semantics differ from product semantics) | Lidl: purchase-price vs retail-price valuation turned standard software into a customization [XIN-017]. | Low–Medium (press) | Partly. Declare supported accounting semantics up front and screen sponsors at sales time. |
| **Poor software architecture** | Thought Machine says legacy product logic sits inside databases [XIN-026] (vendor claim). TSB's data centres were configured inconsistently despite being specified as identical [XIN-003]; this is closer to configuration management than architecture. | Low | Yes, for the target system: declarative provisioning (CNV-ARC-005) and logic as versioned policy (CNV-GOV-005). Legacy source architecture cannot be fixed. |
| **Inconsistent data** | Processors take days to months to export [XIN-028]. Payroll requires per-quarter history [XIN-015]. IBM blamed state data-migration issues at Queensland Health (disputed) [XIN-018]. AEF's history truncation (internal). | Medium | Partly. Closed exception list, golden datasets and deterministic re-runs make data problems visible and cheap to iterate, but do not remove them. |
| **Weak tooling and testing** | TSB: testing compressed, run in parallel, descoped, with no performance environment [XIN-002, XIN-004]. Queensland Health: parallel run not followed [XIN-018]. Counter-example: CBA's 5 rehearsals [XIN-024]. | High (TSB primary) | Yes. This is the main lever for a new entrant. |
| **Consulting- or vendor-dependent business models** | Cover Oregon depended on its vendor and had no independent integrator [XIN-019]. IDC (Salesforce-commissioned) projects $6.19 of ecosystem revenue per $1 of Salesforce revenue by 2026 [XIN-036], an indicator of services intensity rather than waste. Thought Machine's accelerator relies on vendor engineers [XIN-026]. | Low | Yes, commercially: price migration as a product with fixed scope, and make results verifiable by the sponsor. |
| **Governance and schedule pressure** (added) | TSB: aim to migrate by end-2017, a delayed programme, testing compressed to meet dates, readiness attestations unchallenged [XIN-002]. McKinsey: each additional year of a project raises overruns by 15% [XIN-020]. | High (TSB primary) | Partly. Hard, machine-evidenced go/no-go criteria remove discretion at the end. |

**Interpretation (INFERENCE, Medium).** For an AI-native DAF platform, three categories are largely within Unbound's control: tooling, architecture of the target, and the consulting-dependent business model. Two are only partly addressable: inconsistent source data and domain-model mismatch. The cost those two impose can be made visible early, with a closed exception list and a semantic-fit screen, instead of surfacing late. Nothing in the evidence suggests DAF migrations carry less inherent complexity than payroll. Year-to-date continuity, single-issuer tax reporting and in-flight payments recur in both.

## 4. Quantitative evidence and its limits

| Statistic | Population and method | Limits | Class |
|---|---|---|---|
| Large IT projects: +45% budget, +7% time, −56% value; 17% "black swans" threatening the company; +15% overrun per extra year [XIN-020] | >5,400 projects; "large" means initial budget over $15m; McKinsey with Oxford, 2012 | Consultancy publication; sample and value measure not public; dated | industry-report, Medium |
| Average cost overrun 27%, fat-tail distribution [XIN-021] | 1,471 IT projects (Flyvbjerg & Budzier, HBR 2011) | Abstract read only; tail statistics not verified, so not used | academic, Medium |
| >70% of recent ERP initiatives will miss business-case goals by 2027; up to 25% catastrophically [XIN-023] | Gartner prediction, May 2024 | Prediction, paywalled, method unknown | industry-report, Low |
| Standish CHAOS success and failure rates | Not used | Success is defined by estimate accuracy alone, which is one-sided; data not public [XIN-022] | — |
| TSB: £48.65m penalties, £32.7m redress, 225,492 complaints, ~7.5 months to BAU [XIN-002] | Regulatory final notice | Single case | VERIFIED-FACT, High |
| Revlon: ~$64m unshipped sales, $53.6m charges [XIN-016] | 10-K | Company estimate | VERIFIED-FACT, High |
| Schwab–TDA: 5 waves, ~$1.9T, >17m accounts, $2.4–2.5bn total integration cost and capex [XIN-007] | 10-Q | Cost covers the whole acquisition integration | VERIFIED-FACT, High |
| CASS: 1,190,676 switches (2024), 99.7% within 7 working days, 160.5m payments redirected [XIN-010] | Operator report | Operator's own KPIs; method not stated | VERIFIED-FACT, High |
| CBA: 5 rehearsals, 3h fully offline, 16m accounts [XIN-024] | Company newsroom | Self-report | VENDOR-CLAIM, Medium |

No public source gives a cost per migrated account or fund that transfers to DAF sponsors. A dollar migration-cost figure for Unbound would be ASSUMPTION. The ECO model (20) should treat it that way.

## 5. Proposed design: the Unbound Migration Service Commitment (RECOMMENDATION)

The aim is to turn part of the incumbent's switching-cost barrier into a published, bounded, verifiable promise. The promise covers only what Unbound controls. It borrows techniques from ACATS and CASS but makes no claim to equivalent authority (§5.0). It builds on RR-REQ-X-061-r1 and does not replace it.

### 5.0 What ACATS and CASS have that DAF migration lacks

| Enabler | ACATS / CASS | DAF today | What Unbound can do instead |
|---|---|---|---|
| Regulatory compulsion of the losing party | FINRA 11870 obliges the carrying member to validate in 1 business day and complete in 3 [XIN-005]. CASS participants are bound by scheme rules [XIN-009]. | No DAF rule obliges a platform vendor or sponsor to export on any clock. Public terms limit it: NPact allows direct-login access only, charges professional services for export and deletes data 10 business days after hosting ends; Foundant returns data "as stored" at termination; TIFIN bars downloading (ADVB-02). | Use the **sponsor's contractual data-ownership rights** (Foundant §6.1, NPact §6.2 per ADVB-02) through a per-source Extraction Plan: notice deadline, permitted export method, cost and number of extracts (owned by drafts 13 and 15). Start the clock only on receipt of a usable extract. |
| Central utility and standard format | NSCC runs ACATS on standard forms. Pay.UK runs CASS. | None. Each platform exports in its own format, if at all. | **Publish an open Migration Package schema** (§5.2) under a permissive licence, and invite other vendors and sponsors to adopt it. Adoption is HYPOTHESIS; with no regulator, take-up depends on the schema's value to buyers. |
| Obligations on both counterparties, liability allocation | Both members must expedite. The new bank stands behind the guarantee and the old bank must cooperate. | The incumbent has no obligation. Sponsor-to-sponsor transfers are discretionary grants; Fidelity Charitable says donors have "no legally enforceable right" to a recommended grant (ADVB-03). | Commit only on Unbound-side intervals. Offer **Unbound's own exit terms** to its customers, which is the obligation Unbound can impose on itself: unassisted export, no export fee, export never conditional on payment, published onboarding-cost recovery schedule (ADVB-11). |
| Network redirection | Bacs and Faster Payments redirect at scheme level [XIN-009]. | No rail-level redirection exists for checks or ACH to a sponsor's legacy platform. | Redirect only through Unbound's own **old→new crosswalk**: lookups by legacy fund, grant, check and payee IDs. Legacy logins cannot be redirected on the incumbent's systems. |
| Scale economics funding the utility | Millions of transfers a year | Few platform changes a year | Fund the tooling as product, amortized across sponsors. That cost belongs in ECO (20). |

**Where I disagree with the review.** The *techniques* still transfer without compulsion: a closed exception list, deterministic re-runs, a crosswalk, freeze notice and single-issuer reporting all run on Unbound's side. On repeated extracts, a sponsor that owns its data can normally pull direct-login reports more than once during its remaining term, so the limit is cadence and format, not prohibition. Rehearsal value also comes mainly from re-running Unbound's own transform, which can reuse one extract plus synthetic deltas. So the rehearsal gate stays, with its extract count made source-dependent. INFERENCE, Medium.

### 5.1 Commitment terms (sponsor-facing contract schedule; Unbound-controlled steps only)

The numeric values here are illustrative. Canonical parameters (freeze length, rehearsal count, blackout calendar) live in draft 17's parameter table (ADVB-15), and that table governs where the two differ.

**Clock start:** the commitment clock starts when Unbound receives a *conforming* extract, meaning one that passes manifest and schema checks or has only closed-list exceptions.

**Explicit exclusions:**
- late, partial or non-conforming source extracts;
- incumbent refusal, fees or deletion;
- incumbent-side outages;
- sponsor approvals not given within the agreed turnaround;
- any distributor program whose legal sponsor is the vendor's own charity (ADVB-04). Such a program moves fund-by-fund under CNV-ENT-002 and is outside the commitment;
- any donor-level sponsor-to-sponsor transfer.

| Term | Proposed value | Analogue | Failure behaviour |
|---|---|---|---|
| Cutover date | Chosen by the sponsor from published slots, avoiding the year-end surge (canonical calendar in draft 17) unless the sponsor accepts the risk in writing | CASS switch date; December surge (UNB-ACC-036) | No slot, or no conforming extract, means no commitment clock |
| Advance notice | TransitionWindow published 30–60 days before freeze to donors, advisors and charities with pending grants | ERISA 29 CFR 2520.101-3 [XIN-013]; UNB-XIN-OTH-002 | Overrun of the maximum end triggers a re-notice and sponsor escalation |
| Donor-facing freeze | Target ≤3 business days. Grant recommendations are accepted and queued throughout; no new contributions are booked to legacy | ERISA ">3 consecutive business days" threshold | If exceeded, a service credit applies and a notice goes out |
| Rehearsals | ≥3 full mock conversions of Unbound's transform. They use as many fresh source extracts as the Extraction Plan permits, at least one; otherwise the last extract plus synthetic deltas. The last 2 must reconcile with zero unexplained breaks and finish within 70% of the window | CBA (5 rehearsals) [XIN-024]; TSB counter-example [XIN-002] | Gate fails, so the date moves; there is no discretionary override |
| Decision quiet period | ≥5 business days between the last passing rehearsal and CutoverAuthorized | TSB "testing concluded the day before" [XIN-002] | Gate fails |
| History | All history the source can supply, per CNV-EXP-002; as-issued legacy statements kept as documents; legacy read-only archive held in Unbound's vault, not on the incumbent's servers | AEF (33 months imported, 2 years visible) | History the source cannot supply is recorded as `HISTORY_GAP` and disclosed to donors. It is never silently truncated and is not a commitment breach |
| Reference crosswalk | Legacy fund, grant, check and payee identifiers resolve to new records in Unbound for ≥36 months, extended until 13 consecutive months without a hit | CASS redirection (≥3 years per Pay.UK; 36 months per bank guides) [XIN-009] | An unresolvable legacy reference opens a sponsor case; it is never auto-matched by fuzzy logic |
| Remediation | Contractual service credit to the sponsor for detriment caused by Unbound-side failures (late grant, duplicate acknowledgment). The cost of credits must be modelled in ECO (20) | CASS refund of interest and charges | Unbound pays credits as fee reductions. It never holds or moves donor funds (CNV-LEG-001) |
| Exit symmetry (Unbound's own exit terms) | Unassisted self-service export of the whole sponsor in the same published package format; no export fee; export never conditional on payment; any onboarding-cost recovery published as a declining schedule (ADVB-11) | ONC EHI export [XIN-029]; Stripe export to any PCI-compliant processor [XIN-028] | Export failure is a P1 incident |

The specific numbers (70%, 5 business days, 36/13 months) are ASSUMPTIONS to be validated in pilots. They are not industry requirements.

### 5.2 Unbound Migration Package (data contract)

This extends the runbook's proposed schema (`research/migration-runbook-2026.md`, "Data portability schema"). MIG (13–17) owns the entity detail.

```
MigrationPackage {
  package_id, schema_version (semver), source_system {vendor, product, version},
  sponsor_legal_id, as_of (timestamp, source clock), extracted_at,
  extract_kind: Full | Delta(since: timestamp, base_package_id),   // FHIR _since pattern [XIN-030]
  manifest: [ { entity, file, record_count, control_totals{amount_by_year, count_by_status}, sha256 } ],
  signature (sponsor key; the source vendor will usually not sign), encryption (recipient public key)   // PCI-style handoff [XIN-028]
  extraction_method: DirectLoginReport | VendorProfessionalService | DatabaseBackup | Api   // per Extraction Plan (drafts 13/15)
}
StagingRecord { entity, source_system, source_record_id (immutable alt key), package_id,
  mapping_version, policy_version, lineage_hash, verification_status: imported_unverified|verified|n/a }
IntakeException { code ∈ ClosedSet, entity, source_record_id, detail, resolution_path, owner, state: Open|Resolved|AcceptedBySponsor }
```

- **Determinism.** `stage(package_hash, mapping_version, policy_version)` is a pure function. A re-run must produce a byte-identical staging snapshot hash. Rehearsal N+1 consumes `Delta(since = rehearsal N as_of)`.
- **Closed exception set** (ACATS pattern). Initial codes: `DUPLICATE_SOURCE_ID`, `MANIFEST_COUNT_MISMATCH`, `CONTROL_TOTAL_MISMATCH`, `FUND_BALANCE_UNRECONCILED`, `ORPHAN_GRANT`, `ORPHAN_CONTRIBUTION`, `UNKNOWN_RECIPIENT_EIN`, `RECIPIENT_NAME_MISMATCH`, `MISSING_ADVISOR_AUTHORITY`, `SUCCESSOR_CONFLICT`, `UNSUPPORTED_ASSET_TYPE`, `PENDING_ITEM_UNOWNED`, `UNSUPPORTED_ACCOUNTING_SEMANTICS`, `HISTORY_GAP`.
  - Each code has one deterministic resolution path.
  - An observed problem that fits no code is logged as a tooling defect, which drives product work rather than consulting hours.
  - `AcceptedBySponsor` needs A4 approval (RR-REQ-X-061-r1). AI may explain but never accept (CNV-AIO-001).
- **Mapping artifact.** For every entity Unbound returns `old_id → new_id`, the same pattern as the Stripe and Salesforce mapping files [XIN-028, XIN-033]. It backs §5.1 redirection.

### 5.3 Charity-side continuity (the "redirection" analogue)

CASS's insight is that the payer, not the switcher, should not notice the switch. Its DAF counterpart is that charities should not notice a sponsor's platform change.

1. **Networked-rail charities.** These are paid through their existing partner enrolment (CNV-EXP-002), with no new Unbound enrolment. The first post-cutover grants should go to these charities where the sponsor's queue allows (INFERENCE, from the Stripe MID-ramp guidance [XIN-028]).
2. **ACH-fallback charities.** Imported bank details stay `imported_unverified` (RR-REQ-X-061-r1) until CNV-PAY-002 evidence exists.
   - Verification of payees expected in the next 90 days runs *during rehearsals*, so the verified share is known before cutover.
   - Cutover gate: the sponsor sets a minimum verified share or accepts the risk explicitly.
   - Unverified payees fall back to check with positive pay (CNV-PAY-002).
3. **Originator identity.** The sponsor stays Originator (CNV-PAY-001). Where the ODFI allows, keep the sponsor's ACH company name and ID stable across the platform change, and notify charities in advance through their verified channels. This is INFERENCE: no public evidence was found that charities reject unfamiliar originators.
4. **Legacy check numbers and grant IDs** presented by charities, such as remittance queries or returned checks, resolve through Unbound's legacy-reference crosswalk. A returned check addressed to the legacy platform's lockbox is a sponsor case, not an Unbound receipt (CNV-LEG-001).

**Tension to flag (not a conflict).** CNV-EXP-002 and TVF-244 say charities should not re-enrol or resubmit data. CNV-PAY-002 requires destination evidence before the first electronic payment. They can be reconciled through partner-rail evidence where CNV-EXP-002's equivalence conditions hold, plus account-ownership verification that needs no charity action. A charity whose account cannot be verified without its own action will face friction. The owner should decide whether checks are an acceptable interim rail for that group.

### 5.4 Cutover-year tax and statement continuity

This follows Rev. Proc. 2004-53 [XIN-014] and payroll practice [XIN-015].

- One system is designated issuer for the year's donor statements and annual giving summaries. The default is Unbound, using imported year-to-date history.
- Contribution acknowledgments issued by the legacy system before cutover are imported as `as_issued` and are never re-issued (runbook M18).
- Schedule D (Form 990) aggregates for the cutover year are computed from pre- and post-cutover ledgers, as RR-REQ-X-061-r1 already notes (TVS-307).

### 5.5 Waves

- Wave by sponsor, not by fund within a sponsor's book of record, so that one sponsor ledger has one writer.
- Start with small, simple sponsors. Schwab and Nordea show that waves reduce blast radius [XIN-007, XIN-025]. Nordea also shows that open-ended phasing can stretch programmes for years, so each sponsor needs a fixed end condition: legacy decommissioned or archived read-only.
- For a partner-exit sponsor-to-sponsor move, use per-fund transfer grants (CNV-ENT-002, UNB-XIN-EVA-009). ACATS validation clocks are the model for service levels on the receiving side.

## 6. Ranked transferable lessons for a DAF platform

Ranked by (evidence strength × relevance to Unbound's entry segment × degree to which Unbound controls it).

| Rank | Lesson | Evidence | Unbound mechanism |
|---|---|---|---|
| 1 | Make migration readiness a machine-evidenced gate with rehearsals and a quiet period. Schedule pressure is the leading failure cause. | TSB [XIN-002]; CBA [XIN-024]; McKinsey +15% per year [XIN-020] | §5.1 rehearsal and quiet-period gates; no discretionary override |
| 2 | Publish a commitment with a clock, a crosswalk and remediation, covering only the steps you control. CASS turns fear into a bounded promise, but it can because the scheme binds both sides; Unbound can bind only itself. | CASS [XIN-009, XIN-010]; ADVB-02/03 | §5.0–5.1 Migration Service Commitment; clock starts at a conforming extract; Unbound's own exit terms |
| 3 | Standardize the intake with a closed exception list and deterministic re-runs, so bespoke work becomes product defects. | ACATS [XIN-005]; Stripe validation summary [XIN-028] | §5.2 Migration Package and IntakeException |
| 4 | Preserve full history and legacy identifiers; the DAF failure mode is degraded donor history. | AEF (internal); Stripe/Salesforce ID maps [XIN-028, XIN-033] | CNV-EXP-002; mapping artifact; legacy-reference crosswalk; `HISTORY_GAP` disclosure |
| 5 | Treat financial controls as migration deliverables: reconcile and evidence controls from day one. | Revlon material weakness [XIN-016] | Reconciliation gates (MIG 13–17); SOC 2 control evidence at cutover |
| 6 | Keep charities unaware of the switch: reuse enrolments, verify payees before cutover, keep the originator stable. | CASS; Stripe MID ramp [XIN-028] | §5.3 |
| 7 | Use one issuer and one year-to-date for tax-facing outputs in the cutover year. | Rev. Proc. 2004-53 [XIN-014]; Gusto [XIN-015] | §5.4 |
| 8 | Give notice 30–60 days ahead and keep freezes at 3 business days or less. | ERISA [XIN-013] | UNB-XIN-OTH-002 refined |
| 9 | Make exit symmetric and self-service; it lowers the buyer's perceived lock-in risk and is a sales weapon against incumbents. | ONC EHI export [XIN-029]; Stripe [XIN-028] | Same package format outbound; P1 if export fails |
| 10 | Screen semantic fit at sales time; refuse sponsors whose accounting semantics would need customization. | Lidl [XIN-017]; Workday "configuration, not customization" [XIN-034] | `UNSUPPORTED_ACCOUNTING_SEMANTICS` raised in a pre-contract assessment |
| 11 | Federate identity and do not migrate credentials. | SCIM/OIDC [XIN-031] | Advisor SSO plus SCIM/JIT; donor re-enrolment under CNV-PLT-003 |
| 12 | Let the buyer verify the results; do not depend on vendor assurance. | Cover Oregon [XIN-019] | Sponsor-reproducible reconciliation reports; open schema |
| 13 | Use AI for logic and mapping extraction only behind human sign-off. Vendor speed claims are unproven. | Thought Machine/AWS [XIN-026] | CNV-AIO-001/002; AI proposes mappings and policy-pack drafts |

## Implications for Unbound

- **Competitive.** Incumbents' switching barrier is mostly *uncertainty* about history loss, payment disruption and duration, not unavoidable work (INFERENCE, Medium). A commitment backed by rehearsal evidence attacks the Unbound-side part of that uncertainty. The incumbent-side part (extraction rights, cadence, deletion, tail fees) can only be managed, through the sponsor's contract rights and an Extraction Plan, not guaranteed (ADVB-02). Incumbents already sell migration services (ADVB-12). Differentiation must therefore rest on *published, verifiable* outcomes: history depth, reconciliation proof, freeze length and exit terms. Its buyer value is HYPOTHESIS until tested in interviews. Entry-segment sponsors (5k–50k funds) are small enough that a full-volume rehearsal is cheap compared with bank-scale programmes. HYPOTHESIS: three rehearsals of a 50k-fund sponsor fit inside one calendar week of compute and review. Test this with the MIG fixtures.
- **Commercial.** Price migration as a fixed-scope product, with service credits, rather than as time and materials. Cross-check against the ECO model (20) and the 20 bps working scenario (`research/commercial-opportunity/daf-servicing-20bps-market-entry-2026-11-25.md`). A migration price is ASSUMPTION until pilots produce actual effort data.
- **Requirements candidates.** All are proposed; none is ratified.
  1. *Migration Service Commitment.* Published terms per §5.1, covering Unbound-controlled steps only, with the clock starting at a conforming extract and explicit source-side exclusions. Excludes vendor-sponsored distributor programs and donor-level transfers. Refines UNB-XIN-OTH-002 and CNV-EXP-002.
  1a. *Unbound customer exit terms.* No export fee, export never conditional on payment, published declining onboarding-recovery schedule. Refines UNB-TEN-016; resolves the ADVB-11 inconsistency with draft 20.
  2. *Migration Package schema with closed IntakeException set* and deterministic, hash-verified staging. Refines RR-REQ-X-061-r1 (Mapped, ImportedToStaging, Reconciled).
  3. *Rehearsal gate.* At least 3 mock conversions, the last 2 clean, finishing inside the window, plus a quiet period before CutoverAuthorized. Refines RR-REQ-X-061-r1 (ParallelValidated, CutoverAuthorized).
  4. *Legacy-reference crosswalk.* At least 36 months, with the 13-months-without-a-hit extension rule. New; links to CNV-EXP-002.
  5. *Pre-cutover payee verification campaign and verified-share gate.* Refines RR-REQ-X-061-r1 and CNV-PAY-002 application.
  6. *Cutover-year single issuer* for donor statements and summaries; imported acknowledgments stay `as_issued`. Refines REQ-X-060 (RR-REQ-X-060-r1) and runbook M18.
  7. *Unassisted full-sponsor export* in the same package format. Refines UNB-TEN-016 and the CNV-ENT-002 context.
  8. *Pre-contract semantic-fit assessment* covering supported accounting semantics (unitization, fee base, valuation timing). New; links to UNB-XIN-ERP-001.
- **No conflicts** with ratified CNV clauses were found. One tension is flagged in §5.3: CNV-EXP-002's "no new enrolment" versus CNV-PAY-002 destination evidence for ACH-fallback charities.

## Adversarial review response

This responds to the Track B review (`data/adversarial-findings-B.csv`).

| Finding | Verdict | Change made |
|---|---|---|
| ADVB-02: designs assume the incumbent will cooperate | **Accepted** for vendor-signed packages, redirection of legacy logins and fixed extract counts. **Partly refuted** for rehearsals: the sponsor owns its data and can normally pull reports repeatedly, and rehearsal value comes mainly from re-running Unbound's own transform (§5.0). | §5.0 added. Package signed by the sponsor, with `extraction_method`. Rehearsal extract count tied to the Extraction Plan. Login redirection dropped. Legacy archive held in Unbound's vault. |
| ADVB-03: guarantee credible only for Unbound steps | **Accepted.** | Renamed Migration Service Commitment. Clock starts at a conforming extract. Explicit exclusions. No donor-level or cross-sponsor promises. CASS/ACATS equivalence claim withdrawn; the techniques are kept. |
| ADVB-04: vendor-sponsored programs | **Accepted.** | Excluded from the commitment (§5.1); they move fund-by-fund under CNV-ENT-002. |
| ADVB-11: lock-in inconsistency | **Accepted.** | Unbound's own exit terms added (§5.0, §5.1, candidate 1a). |
| ADVB-12: differentiation | **Accepted.** | The implication now rests on published, verifiable outcomes and is HYPOTHESIS until buyer interviews. |
| ADVB-15: parameter drift | **Accepted.** | Draft 17's parameter table is canonical. The values here are illustrative. |
| ADVB-16: "only" AEF case | **Accepted.** | Reworded to "only national-sponsor case found". AEF stated as 33 months imported, 2 years visible. |
| ADVB-19: anchors misquoted | Rejected by the reviewer, and I agree. | None. |

## Open questions / evidence gaps

1. Primary text of the Slaughter and May TSB report: the PDF is image-only, so OCR is needed. The Queensland Health Commission report: Parliament site returned HTTP 403.
2. The current status of the CFPB §1033 rule after the August 2025 ANPR, and whether any DAF account could fall within it. This was not verified for 2026, and applicability to DAFs is unlikely but not established.
3. No public source quantifies DAF platform migration effort, such as hours per fund or exception rates. Pilot data or sponsor interviews (ONB, 10) are needed before any price or cost claim.
4. Whether charities or their banks actually reject or query ACH credits from an unfamiliar originator after a platform change (§5.3 item 3). Test via Nacha return-reason data (R-codes) on early pilots.
5. The ACATS annual volume and exception rate (DTCC does not publish them in the sources found), and the CASS 99.7% methodology.
6. Independent evidence for cloud-native core vendors' migration claims (Thought Machine, 10x, Mambu): none found. Treat them as VENDOR-CLAIM only.
7. Whether legacy DAF platforms (Ren, iPhi/Stellar, NPact FIMS/DonorCentral) provide complete exports on request, and in what time. Their contracts may oblige release; compare Stripe's note on processors' contractual duty [XIN-028] and `research/ren-legal-entities-public-msa-contract-portability-audit-2026-11-12.md`.
