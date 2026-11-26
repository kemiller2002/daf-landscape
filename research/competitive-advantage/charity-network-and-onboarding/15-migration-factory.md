# 15 - Migration factory (B6)

Status: research draft (2026-11-26). Not legal advice. Evidence classes per 01-research-methodology.md.

Scope: a repeatable, productized migration process ("migration is a product, not a one-off professional services script", `unbound:research/daf-theoretical-enterprise-validation/19-questions/LEGACY-MIGRATION-PORTABILITY-AND-SPONSOR-EXIT-2026-11-23.md`). The factory refines the WFM-26 `MigrationRun` state machine (RR-REQ-X-061-r1) into operational stages, adds a determinism contract and rehearsal isolation, and surveys public evidence on legacy export formats. Notation: `(CLASS, confidence)`.

## Summary

- **The factory must not assume incumbent cooperation (ADVB-02).** Public terms allow direct-login access only, paid export services, deletion 10 business days after hosting ends (NPact [ADVB-002]), returns "as stored" (Foundant [ADVB-001]), and bans on downloading (TIFIN, draft 10). Every stage therefore has a **single-extract degraded path** (§1a). Parallel operations run on whatever extract cadence the contract allows, and Unbound's own L0 vault, not the incumbent, holds read-only legacy history (RECOMMENDATION, High).
- **Sixteen stages map onto the existing ten WFM-26 states**, so no new top-level states are needed. The additions are sub-stage evidence artefacts and gates (RECOMMENDATION, High).
- **Determinism contract.** `RunManifest = H(source bundle Merkle root, adapter@version, mapping_version_hash, transform code commit, reference-data snapshot IDs, config hash, as_of)`. The same manifest must produce a byte-identical canonical output hash. The transform may not read the wall clock or the network, use binary floating point (UNB-NAV-022), depend on locale, or call AI. AI is used only before a mapping is approved (see 13).
- **Rehearsals run in isolated rehearsal cells** with provider mocks and no outbox to real banks, rails or custodians. Production import always re-runs from the L0 vault with an approved manifest. **Rehearsal output is never promoted** (RECOMMENDATION, High).
- **Public export documentation is thin and uneven** (VERIFIED-FACT for what was found, Medium):
  - Foundant documents per-source migration tooling (FIMS, Pearl, CSData field translations, beginning-balance templates, a historical-import flag) [MIG-001..006].
  - Blackbaud documents Financial Edge/RE exports and database backups, but routes FIMS extraction through a Knowledgebase article [MIG-008].
  - FIMS and DonorCentral moved to NPact in 2022 [MIG-009].
  - **No sponsor-side Ren export or migration documentation is public**. Only a charity-side grants export is documented [MIG-015].
- **Adapters are plugins behind one contract** (`detect / parse / map / conformance`), validated against the synthetic fixture in `research/migration-runbook-2026.md` (M01-M20). Partner-built adapters are allowed under Unbound-controlled validation (REQ-X-061 decision challenge).
- **Exceptions follow an eight-class taxonomy (E1-E8)** with fixed owners and dispositions. Only **fix-in-source**, **fix-in-mapping**, **accept-as-Unknown-with-disclosure** or **block** are allowed, never "adjust to fit".
- **Timeline guidance from practitioners**: finish at least 3 months before the legacy contract ends [MIG-007]. Expect slippage: one FIMS replacement was planned at 18 months and took more than 2 years [MIG-025] (VENDOR-CLAIM, Low-Medium).

## 1. Stages

| # | Stage | WFM-26 state | Key output (evidence artefact) | Gate to next | Anchors |
|---|---|---|---|---|---|
| 1 | Secure ingestion | Contracted→Inventoried | Transfer receipt; malware scan; LegalBasis ref | Basis covers tier; scan clean | UNB-MIG-001, CNV-ARC-002 |
| 2 | Immutable source preservation | Inventoried | L0 manifest (SHA-256 per file, Merkle root), chain of custody | Hashes recorded before any parse | UNB-DATA-008, UNB-CUST-012 |
| 3 | Profiling | Inventoried | Profile (13 §2 T1/T3 schema) | Profile signed | UNB-MIG-004 |
| 4 | Format identification | Inventoried | Adapter selection + fingerprint score | Single adapter ≥ threshold, or human choice | §3 below |
| 5 | Inventory of in-flight items | Inventoried | In-flight register (17) | Every open item classified | WFM-26-T01, UNB-XIN-EVA-009 |
| 6 | Mapping | Mapped | Mapping version (Approved) | Round-trip `Tested` + A4 approval | UNB-MIG-003, WFM-26-T02 |
| 7 | Transformation | ImportedToStaging | L1/L2 outputs + output hash | Deterministic re-run equals output hash | UNB-MIG-020 |
| 8 | Validation | ImportedToStaging | Rule results per rule version | No E1/E2 open | UNB-ACC-030 |
| 9 | Exception classification | ImportedToStaging / ReconciliationBreak | Exception register (E1-E8) | All BLOCK classes resolved | §4 |
| 10 | Customer confirmation | ImportedToStaging | Signed confirmation per mapping version, per disposition class, per HistoryGap list | Sponsor A4 sign-off | WFM-26-T05 |
| 11 | Trial migration (rehearsal ≥2) | ImportedToStaging (rehearsal cell) | Rehearsal reports incl. timing | Two consecutive clean rehearsals on the same manifest family | UNB-MIG-021 |
| 12 | Financial reconciliation | Reconciled | Gate results `data/reconciliation-gates.csv` | All blocking gates pass | 16; WFM-26-T04 |
| 13 | Parallel operations | ParallelRunning→ParallelValidated | Shadow comparison at the cadence the Extraction Plan allows (daily feed / periodic report re-exports / month-end statements only); ProvisionalCalibration results | ≥1 full close cycle within tolerance at the available cadence | CNV-FIN-004, WFM-26-T07 |
| 14 | Final delta | CutoverAuthorized | Delta manifest at legacy high-water mark | Delta reconciled | UNB-TEN-013 |
| 15 | Cutover | SingleWriterActive | Fence confirmation, opening journals, routing switch | Fence confirmed (not Unknown) | 17; UNB-RCN-WF-020 |
| 16 | Post-cutover validation and legacy retirement | PostCutoverVerified→Archived | Independent sign-off; legacy archive receipt; retirement certificate | Reconciler ≠ operator (GOV-AUTH-014) | WFM-26-T15/T16, CNV-ENT-002 |

### 1a. Extraction-cadence variants (ADVB-02)

| Variant | When | Rehearsals | Parallel run | Final delta | Legacy history after cutover |
|---|---|---|---|---|---|
| **Full cooperation** | Sponsor-hosted system, or a contract grants unlimited exports/API | Fresh extract per rehearsal allowed | Daily or weekly deltas | Re-export diff (below) | L0 vault (plus legacy read-only if the contract allows) |
| **Periodic reports** | Direct-login reports only, no automation (NPact §2.4, TIFIN) | All rehearsals re-run on **one** baseline extract; determinism makes that sufficient | Sponsor downloads standard month-end reports (fund balances, TB, grant/contribution listings); comparison only at those points | Second report set after legacy close at E-1 | L0 vault only |
| **Single extract** | Export is a paid one-off PS deliverable, or termination is imminent | Same baseline extract | **No continuous shadow.** Unbound replays the baseline period and compares to as-issued month-end statements and custody/bank statements already in L0 (a retrospective parallel). The 12-month shadow replay that CNV-ECO-003 requires for the first sponsor is satisfied by this replay | Freeze-bounded: legacy close at E-1 → one final paid extract, or report-level delta only for the freeze window. The baseline extract is taken as late as possible | L0 vault only |

Rules:
- Before contract signature, the Extraction Plan (13 §2a) must show how many extracts are allowed, what they cost, and the post-termination window.
- Every report, statement PDF and document is captured into L0 **before** incumbent access ends, because Unbound never relies on post-termination incumbent access.
- Where the deletion window is short (e.g. 10 business days), cutover is scheduled at least one final-delta cycle before the hosting end date.
- Incumbent professional-services, remaining-term and tail fees are budgeted in draft 20.

**Final delta design.** Legacy "modified since" timestamps are unreliable as a change feed (INFERENCE, Medium). Instead, take a full re-export at the frozen high-water mark and diff it against the prior export by `(source_id, content_hash)`. That yields three sets: new, changed and disappeared. *Disappeared* records are an E5 or E6 exception, because legacy systems that hard-delete are a red flag.

## 2. Determinism and reproducibility contract

```
RunManifest {
  run_id, migration_run_id, purpose: Assessment|Rehearsal|Production,
  source_bundle_root: sha256,               // L0 Merkle root
  adapter: {id, version, code_commit},
  mapping: {version_id, content_hash, state: Approved|Proposed},
  transform: {code_commit, build_hash},
  reference_snapshots: {charity_registry_snapshot_id, price_snapshot_id?, fx_snapshot_id?, calendar_id},
  config_hash, as_of: date,                 // pinned, never wall clock
  output_hash: sha256                       // over canonical sorted serialization of L2
}
```

Rules (proposed UNB-MIG-020):
- **Purity.** A transform is a pure function `(L1 rows, mapping, snapshots, config, as_of) → L2 rows + exceptions`.
  - Banned in transform code: wall clock, random, network, environment-dependent locale or timezone, unordered map iteration in output, binary floats (decimal with declared scale only, UNB-NAV-022).
  - Static checks in CI enforce the ban, and a double-run test enforces purity.
- **Equivalence.** "Equivalent output" means identical `output_hash` over a canonical serialization: sorted by `(entity_type, canonical_key)`, normalized decimals, UTC ISO-8601 instants, NFC strings.
- **Pinned versions.** A Production run requires `mapping.state=Approved` and a manifest whose adapter, mapping and transform hashes match the ones used in the last clean rehearsal.
- **Re-performance.** An auditor or the sponsor can re-run any manifest from the vault and obtain the same output hash. This is an audit-evidence asset for opening balances (AU-C 510 [MIG-016]) (INFERENCE, Medium).
- **Upcasting.** If a later Unbound release changes the canonical schema, earlier runs are re-interpreted by versioned upcasters, and their outputs are never rewritten (UNB-DATA-010, UNB-XIN-WFA-002).

## 3. Adapter catalogue: what is publicly documented

| Legacy platform | Publicly documented export/migration material found | What is not public | Adapter implication | Evidence |
|---|---|---|---|---|
| Ren (sponsor side) | None for sponsors. Charity-side grants report exportable for GL/CRM; third-party DAF grants labelled "Legacy" [MIG-015]. AEF move from DonorCentral to Ren kept 2 years visible; pilot pulled 33 months [MIG-012] | Sponsor data export format, API, history depth, fee for export | Contractual: the sponsor must obtain a full export (L16-L18 pattern). Adapter built only against authorized samples. Expect report-style CSV/XLSX plus PDF statements | VENDOR-CLAIM / VERIFIED-FACT, Medium |
| Blackbaud FIMS (now NPact) | Blackbaud decommissioning page: follow a Knowledgebase article to extract critical data [MIG-008]. NPact acquired FIMS and DonorCentral NXT in 2022 [MIG-009]. Foundant publishes FIMS field-to-field translations and FIMS migration validation [MIG-004] | Native schema and file layout (not public) | Mature third-party knowledge exists (Foundant). Prefer a database backup or full export via NPact. Validate with the legacy TB and fund balance reports | VERIFIED-FACT (existence), Medium |
| Blackbaud Financial Edge / FE NXT | Export module, Create Import File, database backup request [MIG-008]; NXT import requires header records and field mapping [MIG-010]; JE Excel add-in [MIG-011] | Full field list in fetched material | Usually the sponsor's entity GL. Often stays as the external book (CNV-FIN-012), so Unbound posts DAF program data and reconciles in Shadow | VERIFIED-FACT/VENDOR-CLAIM, Medium |
| Blackbaud Raiser's Edge / RE NXT | Export of every field, query export, DB backup, NXT APIs [MIG-008] | n/a | Donor CRM source; party and contact data only | VERIFIED-FACT, High |
| Foundant CommunitySuite | Beginning balance: CoA, Funds Listing, Fund Balance Import "as of a given date" [MIG-001]; historical import flag not affecting GL [MIG-003]; grant-history export added 2024-08-27 (repo: `research/DAF-INDUSTRY-REPORT-2026-11.md`); "API Connections" add-on (Oct 2025) with objects documented only inside the product (repo: `research/mission-2026-11-14/queue-batch36-agent-terms-controls.md`) | Outbound bulk export spec | Mostly community foundations, outside the entry segment (CNV-ECO-004). Adapter lower priority | VENDOR-CLAIM, Medium |
| DonorCentral (NPact) | Legacy DonorCentral grants-paid list export (repo: `research/DAF-INDUSTRY-REPORT-2026-11.md` l.575) | Full fund-history export | Donor-portal layer, not the book of record. Pair with the FIMS/GL adapter | VERIFIED-FACT (repo), Medium |
| Spreadsheets / bespoke | Sponsor-specific | Everything | Highest variance. Schema inference + AI mapping proposal (13) + strict E1-E4 rules | INFERENCE |
| Custodian / bank statements | Custodian-neutral normalized schemas (UNB-CUST-004) | Provider-specific | Independent reconciliation sources, never migration sources of truth for fund attribution | Requirement |

**Adapter contract** (proposed UNB-MIG-022): `detect(bundle) → FingerprintScore`, `parse(file) → L1 rows (lossless)`, `map(L1, mapping) → L2 + exceptions`. Conformance suite:
1. Synthetic fixture covering every account state in the runbook universal fixture: pooled, separately managed, restricted, pending in-kind gift, recurring grant, approved-unpaid grant, uncashed check, returned ACH, corrected grant, successor change, deceased donor, hold, anonymization request.
2. Round-trip totals.
3. Determinism double run.
4. Malformed-file fuzz cases (encoding, delimiter, truncated file).
5. **Semantic invariants and mutation tests** (13 §4; ADVB-09). Total-preserving swaps (advisor↔successor, restricted↔unrestricted, status at the same amount, acknowledgment flags, payee swap on equal-amount grants) must all be detected. An adapter that lets any swap through fails conformance.

## 4. Exception taxonomy

| Class | Examples | Default owner | Allowed dispositions | Blocks cutover? |
|---|---|---|---|---|
| E1 Structural | Unparseable row, encoding, truncated file | Migration operator | Re-export (fix-in-source), adapter fix | Yes |
| E2 Referential | Grant references unknown fund; orphan transaction | Operator + sponsor ops | Fix-in-source, fix-in-mapping, accept-as-Unknown (history only) | Yes if live object; no if history-only with disclosure |
| E3 Identity | Duplicate fund IDs (REQ-X-061 adversarial case), same person twice, EIN collision | Sponsor ops | Merge/split decision recorded in crosswalk | Yes for funds and payees |
| E4 Domain validation | Negative fund balance, future dates, grant to revoked EIN | Sponsor ops / compliance | Fix-in-source or accept with explanation | Yes for balances; charity status rechecked anyway (CNV-GRT-003) |
| E5 Financial break | Fund balance ≠ legacy statement; unit totals ≠ pool | Controller | Explain with evidence or fix; never plug | Yes (16) |
| E6 Legal/authority | Advisor without signed agreement; successor contested; legal hold | Sponsor legal / ops | Import as `imported_unverified`; restrict authority | Per item: authority-dependent actions blocked |
| E7 Unsupported behaviour | 13 §5 catalogue | Product + sponsor | Remediate, drop with disclosure, keep reference-only | Depends on decision |
| E8 Privacy/retention | Anonymization request pending; data past retention | Privacy owner | Withheld state; disposition per CNV-PLT-004 | No, unless a hold conflict |

Each exception has `{id, class, rule_id@version, source_locator, amount?, owner, disposition, evidence_ref, decided_by, decided_at}`. Dispositions affecting money require segregation of duties (WFM-26-T05 guards).

## 5. Rehearsal isolation (proposed UNB-MIG-021)

- **Rehearsal cell**: a separate schema or database with `cell_purpose=Rehearsal`. Tenant IDs are distinct from production, so they cannot collide in envelopes (UNB-XIN-SAS-005).
- **No external side effects**: the outbox dispatcher is bound to deterministic provider mocks (STRATA-GAP-01 notes that Unbound must own these mocks; `unbound:requirements/convergence/2026-11-24-master/07-ECHELON-CAPABILITY-ASSESSMENT.md`). Notification channels are routed to sinks.
- **Same PII controls as production**: rehearsal data is real donor data.
- **Expiry**: a rehearsal cell is destroyed after the next rehearsal or 30 days after cutover, with a certificate, subject to legal holds.
- **No promotion path exists**: there is no API to copy rehearsal records into production. Production is built only from L0 plus an Approved manifest.

## 6. Parallel operations and legacy retirement

- During the parallel run, legacy stays the sole writer (WFM-26-T06). Unbound ingests legacy data at the cadence in §1a (daily deltas only where permitted) and recomputes balances, fees and, where in scope, units in Shadow.
- Variances follow CNV-FIN-004 `ProvisionalCalibration`: zero tolerance, with every non-exact item sent to the human queue for at least one full close cycle.
- Practitioner evidence varies: one month in parallel, no dual entry at all, or legacy kept in read-only for months [MIG-007]. Unbound should require **one full monthly close in parallel** for the entry segment (RECOMMENDATION, Medium).
- **Retirement** (proposed UNB-MIG-025):
  - The L0 vault plus History Partition are the sponsor's legacy archive (14, UNB-MIG-017). Before access ends, a final completeness check confirms that every as-issued statement, document and report listed in the inventory is in L0.
  - If the incumbent contract allows it, legacy may also stay read-only. The practitioner advice is to keep the legacy contract at least 3 months past go-live [MIG-007]. This is a **preference, not a dependency**.
  - Legacy credentials and API tokens are revoked (runbook M14).
  - The retirement certificate lists residual open items and legal holds (UNB-XIN-REC-001).

## Implications for Unbound

- The factory's moat is **reproducibility plus evidence**, not adapter count. A sponsor CFO and auditor can re-run the conversion and get the same hash. Nothing comparable is publicly documented by incumbents (not publicly documented, which does not mean absent).
- Prioritize adapters by entry segment (CNV-ECO-004): Ren-hosted and bespoke or spreadsheet national sponsors first; FIMS and CommunitySuite later.
- Ren adapter feasibility depends on the sponsor's contract export rights. Make "full export in documented format" a pre-signature checklist item, per the runbook's commercial checklist.

Candidate requirements: **UNB-MIG-020** deterministic run manifest and purity rules; **UNB-MIG-021** rehearsal isolation with no promotion; **UNB-MIG-022** adapter contract and conformance suite (refines UNB-CUST-024 pattern); **UNB-MIG-023** E1-E8 exception taxonomy with allowed dispositions; **UNB-MIG-024** final delta by full re-export diff at the high-water mark (refines UNB-TEN-013); **UNB-MIG-025** legacy retirement certificate, with the L0 completeness check before incumbent access ends; legacy read-only access is optional (refines CNV-ENT-002 for inbound); **UNB-MIG-026** extraction-cadence variants: rehearsals on one baseline extract, a retrospective parallel when there is only a single extract, and cutover scheduled before the incumbent's deletion window (refines UNB-TEN-013, RR-REQ-X-061-r1).

## Open questions / evidence gaps

- Real export samples from Ren, FIMS/NPact and DonorCentral under authorization. None have been seen, and every adapter claim here is design, not test.
- Whether NPact offers a supported FIMS database extract for migrations away from NPact products.
- Calibration of rehearsal count and duration once two or more real migrations exist (CNV-EVB-002).

## Adversarial review response

| ID | Response |
|---|---|
| ADVB-02 | **Accepted.** Added §1a cadence variants, a single-extract degraded path, the L0 vault as legacy archive, and legacy read-only demoted to optional (UNB-MIG-026). Determinism makes repeated extracts unnecessary for rehearsals. |
| ADVB-06 | **Accepted in part.** Controller approval is required on the final rehearsal and the production run only. Intermediate rehearsal gate results are system-generated. Hour modelling is draft 20's. |
| ADVB-09 | **Accepted.** Mutation tests and semantic invariants are added to adapter conformance. |

