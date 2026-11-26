# 13 - Pre-contract migration assessment (B4)

Status: research draft (2026-11-26). Not legal advice. Evidence classes per 01-research-methodology.md.

Scope: a capability that lets a prospective sponsor learn, *before signing*, how hard its migration to Unbound will be, without handing over raw donor data unless and until a lawful basis exists. Builds on `research/migration-runbook-2026.md` (M01-M20 synthetic acceptance cases), `data/switching-cost-control-matrix-2026.csv` (L01-L30) and the Unbound workflow WFM-26 (`unbound:requirements/reconciliation/2026-11-23/workflows/WFM-26-sponsor-migration.json`). Notation: `(CLASS, confidence)`.

## Summary

- **Switching cost is driven by unknowns, so assessment should come before the contract.** No public source gives migration TCO for a DAF platform (L27, `data/switching-cost-control-matrix-2026.csv`). The public cases that do exist show history loss and long timelines. AEF's Ren pilot imported 33 months of grant history and shows 2 years to donors [MIG-012] (VERIFIED-FACT, High). Foundant's beginning-balance path carries balances only, with history as a separate non-GL import [MIG-001][MIG-003] (VENDOR-CLAIM, Medium). One FIMS replacement planned at 18 months ran past two years [MIG-025] (VENDOR-CLAIM, Low). A sponsor that can see its migration risk in advance is easier to win (INFERENCE, Medium).
- **Use a five-tier exposure ladder (T0-T4).** The tiers run from a questionnaire up to a full trial conversion. Most go/no-go questions can be answered at **T1**: a profile the customer runs on its own premises that emits only the schema and suppressed aggregate statistics, so no record-level personal data leaves the sponsor (RECOMMENDATION, Medium).
- **Format-preserving tokenization (FF1) is useful but does not anonymize.** It keeps joins and formats intact, so mappings and referential checks still work. However, the tokens are deterministic, and amounts and dates remain quasi-identifiers, so tokenized samples stay personal data under state laws that cover nonprofits [MIG-020]. Use FF1, not FF3: NIST's 2nd draft of SP 800-38G Rev. 1 drops FF3 [MIG-018] (VERIFIED-FACT, Medium).
- **Differential privacy suits benchmarking, not reconciliation.** DP noise breaks the exact control totals that the financial gates need (see 16). Use DP only for cross-prospect benchmark statistics, and evaluate it against the hazards in NIST SP 800-226 [MIG-019] (INFERENCE, High).
- **The legal basis is tiered.** T0-T1 need a mutual NDA. T2-T4 need a processor/service-provider agreement (DPA) with purpose limitation, deletion and a no-training clause. They also need a check that the sponsor's own donor privacy notice permits disclosure to a service provider. GLBA most likely does not bind a 501(c)(3) sponsor directly. Even so, Unbound should adopt Safeguards-Rule-equivalent controls by contract [MIG-021] (INFERENCE, Medium).
- **AI-generated mappings are proposals and are never authoritative.** A mapping version becomes usable only after two things happen. First, a deterministic **round-trip reconciliation** passes: source control totals = re-projected canonical totals. Second, the sponsor confirms it under WFM-26-T02 (A4, segregation of duties). This follows CNV-AIO-001/002.
- **Hosted incumbents control what the sponsor can extract, and the assessment has to start there.** Before any profiling, the sponsor must obtain its own data. Public terms make that slow or costly:
  - NPact allows access "only by direct login", makes export a paid Professional Service, and deletes data 10 business days after hosting ends [ADVB-002].
  - Foundant returns data "as stored" through its reporting tools [ADVB-001].
  - TIFIN group terms bar downloading (`10-institutional-onboarding-landscape.md` contract table).

  So **T0 now outputs an Extraction Plan**, and T1 runs only on standard reports the sponsor can download through direct login (§2a) (RECOMMENDATION, High).
- **Legal sponsor of record is a T0 question.** An advisor or bank "program" hosted on a vendor's own charity (e.g. RCF, NPT, Charityvest-administered programs [ADVB-008][ADVB-012]) is not a platform migration. It is a **ProgramTransfer**: fund-by-fund sponsor-authorized grants (CNV-ENT-002, UNB-XIN-EVA-009) with no full-history import. It is assessed separately (§2b).
- **The output is a Readiness Report.** It contains RAG status per domain, blocking findings, available history depth, a list of unsupported legacy behaviours, the customer decisions required, and an effort model stated as driver counts × labelled assumptions. It does not quote a dollar figure.

## 1. Why pre-contract assessment is a competitive lever

| Observed friction | Evidence | What assessment answers early |
|---|---|---|
| Truncated donor history after platform change | AEF/Ren: 2 years visible; pilot 33 months [MIG-012]; L05 | How many years exist in the predecessor, and in what form (transactions, statements, PDFs only) |
| Balances-only conversions | Foundant beginning balance excludes transaction history [MIG-001]; history imported as non-GL "historical" [MIG-003] | Whether full history (CNV-EXP-002) is achievable or must be disclosed as `HistoryIncomplete` |
| Opaque exports | FIMS extraction is through a Knowledgebase article and the format is not public [MIG-008]; Ren publishes no sponsor-side export documentation (not publicly documented) | Which adapter applies, and whether a database backup or report exports are needed |
| Long timelines | 18 months planned, more than 2 years actual [MIG-025]; forum users advise finishing ≥3 months before the legacy contract ends [MIG-007] | A critical path that accounts for legacy contract end, fiscal calendar and the December peak (see 17) |

## 2. Exposure ladder

| Tier | What leaves the sponsor | Typical artefacts | Legal basis (minimum) | Answers | Cannot answer |
|---|---|---|---|---|---|
| T0 Questionnaire | Nothing record-level | Platform/version, **legal sponsor of record**, fund count, pools, custodians, rails, fiscal year, history years, **grant recognition convention (CNV-FIN-007)**, contract end date and notice deadline, **export rights, permitted export method, cost and allowed cadence** | NDA | Migration class (§2b), Extraction Plan (§2a), adapter choice, segment fit (CNV-ECO-004), calendar window | Data quality |
| T1 Schema + statistics profile | Schema, row counts, null/distinct ratios, value-pattern classes, date ranges, **control totals per fund bucket**; cells with fewer than k (default 10) contributors suppressed | Profiler kit run by the sponsor; signed JSON profile | NDA (and confirmation that no personal data is in the profile) | Structural complexity, missing fields, referential gaps, history depth, a first tie-out of totals | Record-level matching, duplicate persons |
| T2 Tokenized sample | Stratified sample (e.g. 500 funds incl. edge states) with FF1-tokenized identifiers and names; free text dropped; amounts and dates kept | Sample + token-domain manifest; key held by the sponsor | NDA + DPA | Mapping validation, identity-collision rates, restriction encoding | Contacting donors, and anything needing the clear text |
| T3 Authorized representative export | Full export, in a per-prospect isolated assessment enclave | Export bundle + hash manifest | NDA + DPA + documented sponsor authority + privacy-notice check | Full profiling, exception inventory, effort model | Live comparisons with the running legacy system |
| T4 Trial conversion | T3 data through the factory (15) into a rehearsal cell | Simulation run, reconciliation report | As T3 + statement of work | Conversion simulation, reconciliation gate results (16) | Cutover behaviour under live traffic |

Rules (RECOMMENDATION):
- Tiers are monotonic per engagement. Moving up a tier requires a recorded `LegalBasis` reference for that tier. An upload whose tier does not match its basis is rejected **before** it is persisted.
- A T1 profile is scanned on receipt for anything that looks like a direct identifier (email, phone, SSN/EIN patterns, personal names in free text). If any is found, the profile is quarantined, purged within 24h and recorded on a deletion certificate, and the sponsor is notified.
- T2 tokens use FF1 under a **sponsor-held key** (or a key escrowed in the sponsor's tenant), so Unbound cannot detokenize during assessment. Per CNV-TEN-001, tokens never enter a cross-tenant store.
- All tiers ≥T2 are treated as production-class PII for access, logging and retention. Each has a fixed **assessment retention deadline** (default 90 days after report delivery or no-decision), after which it is destroyed with a certificate, unless a legal hold applies (UNB-XIN-REC-001).

### 2a. Getting data out of a hosted incumbent (Extraction Plan)

`ExtractionPlan { incumbent, hosting: SponsorHosted|VendorHosted, contract_end, notice_deadline, export_rights_clause, methods[{DirectLoginReports|PaidProfessionalService|DatabaseBackup|API}], cost_basis, allowed_extracts: One|Periodic(n)|Unlimited, post_termination_access_days, deletion_after_days, automation_permitted: bool }`

| Incumbent (public terms) | Likely path for the sponsor | Constraint that shapes the plan |
|---|---|---|
| NPact (FIMS hosted, DonorCentral, Foundation Cloud) [ADVB-002] | Direct-login reports for T1; a paid Professional Services export or backup for T3+ | Direct login only; paid PS; data deleted 10 business days after hosting ends; 3-year term with 90-day non-renewal notice |
| Foundant CommunitySuite [ADVB-001] | Reporting-tool CSV exports | Returned "as stored" at termination; no duty to keep data afterwards |
| Ren / iPhi (2023 MSA draft, draft 10) | Contractual export request; the Data Migration add-on is sold as a service | 15 days of "industry-standard format" access after termination |
| TIFIN (group terms, draft 10) | Only what the signed agreement grants | Downloading and archiving barred by default terms |
| Self-hosted FIMS / Financial Edge [MIG-008] | Sponsor-run export or database backup | Sponsor controls; few limits |

Pre-contract pathway and timeline (ASSUMPTION ranges, to calibrate):
- **Week 0-1, T0.** The questionnaire and contract review produce the Extraction Plan.
- **Week 1-3, T1.** The sponsor runs standard reports it already runs: fund balance, trial balance, grant and contribution listings, year-end statements. The offline profiler reads them on the sponsor's desktop. Because these are routine reports, the request does **not** signal switching intent to the incumbent.
- **Week 3-8+, T2/T3.** These tiers usually need a full export. If that requires a paid PS order or a backup request, it reveals intent, so it follows a signed LOI or contract.
- **Week 4-12.** A full export arrives where it is paid PS; the timing is incumbent-dependent and has no public SLA.

When only **one extract** is permitted or affordable, the factory's single-extract path applies (15 §1a).

### 2b. Migration class

| Class | Who owns the books | Mechanism | History |
|---|---|---|---|
| PlatformReplacement | The sponsor (owns Client/Customer Data under Foundant §6.1 and NPact §6.2 templates [ADVB-001][ADVB-002]) | WFM-26 MigrationRun | Full import per CNV-EXP-002 |
| ProgramTransfer (distributor on a vendor-sponsored charity) | The incumbent sponsor; the distributor may not control donor records | Fund-by-fund grants under CNV-ENT-002 / UNB-XIN-EVA-009, needing incumbent-sponsor cooperation and each advisor's recommendation | Reference package only; whatever donors or the distributor lawfully hold |
| TenantRelocation | Unbound tenant moves between isolation profiles | UNB-TEN-011..013 | Lossless |

### Why tokenization is not anonymization (INFERENCE, High)
- Deterministic FPE preserves equality, which is the point: joins still work. But it also preserves frequency distributions, so the largest donors and rare ZIP codes can be singled out.
- DAF data is sparse and high-value. A single "$2.4m appreciated stock contribution on 2019-12-27" is enough to identify the donor. Amount banding or date shifting would break reconciliation, so T2 keeps exact amounts and dates and **treats the sample as personal data**.
- Schema-only profiles with k-suppression (T1) are the real privacy boundary.
- Differential privacy adds calibrated noise, which is incompatible with exact tie-outs. Use it only where Unbound publishes cross-prospect benchmarks, for example "median % of funds with missing successor data", with a recorded privacy budget and the NIST SP 800-226 hazard review [MIG-019].

## 3. Legal basis and confirmations

| Question | Default position | Evidence class |
|---|---|---|
| Is GLBA binding? | Probably not for a 501(c)(3) sponsor, because the Safeguards Rule reaches "financial institutions" under FTC jurisdiction [MIG-021]. Contractually adopt an equivalent written security program anyway. | INFERENCE, Medium; counsel to confirm |
| State comprehensive privacy laws | CO, DE, MD, MN, NJ, OR apply generally to nonprofits [MIG-020]. Unbound acts as processor and needs a contract with the required processor terms. | VERIFIED-FACT (summary), Medium |
| Sponsor's donor privacy notice | It must permit disclosure to service providers for administration. If it does not, stay at T0-T1 until the notice is amended. | RECOMMENDATION |
| Donor anonymity flags | Carried through even into T2 samples as a structural flag, never as clear names | RECOMMENDATION (consistent with CNV-TEN-001) |
| Use for AI training | Prohibited by the DPA. AI inference over T2/T3 runs only inside the prospect's enclave, with no retention by the model provider | RECOMMENDATION (CNV-AIO-001) |
| Predecessor-vendor contract | Export rights, fees, and any benchmark or "competitive evaluation" restrictions (L20-L21) are checked before T3 | VERIFIED-FACT that such clauses exist in some generic terms (`data/switching-cost-control-matrix-2026.csv` L20, L21) |

## 4. Assessment pipeline (deterministic core, AI at the edges)

```
Intake(T,LegalBasis) -> FormatIdentify -> StructuralProfile -> SemanticClassify(AI-proposed)
 -> QualityRules(deterministic) -> MappingProposal(AI draft) -> RoundTripTest(deterministic)
 -> SimulateConversion(T>=3) -> ReconciliationDryRun -> ReadinessReport
```

| Step | Automatic | Needs customer confirmation |
|---|---|---|
| Format identification: encoding, delimiter, header row, platform fingerprint (column-set signature vs. adapter catalog in 15) | Yes | Only when confidence is below threshold or several adapters match |
| Structural profile (types, keys, cardinalities, orphan foreign keys) | Yes | No |
| Semantic classification (column → canonical concept, see 14) | Proposed by AI with a confidence score | Yes, every column the mapping uses |
| Quality rules (dates in future, negative balances, duplicate fund IDs, EIN checksum/format, missing successor for deceased advisor, grants to payees without EIN) | Yes; the rule set is versioned | Disposition of each rule class |
| Unsupported-behaviour detection (§5) | Yes (pattern rules) + AI explanation | Yes. The sponsor chooses whether to remediate, drop, or keep as reference-only |
| Mapping proposal | AI draft | Yes, approved under WFM-26-T02 (A4) |
| Round-trip test | Yes | No (a failure blocks progress) |
| Simulation and reconciliation dry run | Yes | Sign-off of the dry-run report |

**Mapping state machine** (proposed UNB-MIG-003):
`Proposed(by=AI|human)` → `Tested` (round-trip passes on full T3 data or every T2 stratum) → `CustomerConfirmed` (named sponsor role) → `Approved` (A4, a different principal from the confirmer) → `Superseded`.
- `Tested` requires all three of the following, because aggregate totals alone miss **total-preserving** mis-mappings (ADVB-09):
  1. **Totals**: for every mapped financial measure, Σsource = Σcanonical exactly per fund and per period, and record counts match per entity class or every difference is itemized.
  2. **Semantic invariants per entity**, each a deterministic rule:
     - role cardinality (each active fund has ≥1 advisor; successors are not active advisors before activation);
     - status-transition legality (a paid grant has a release reference; a voided grant has no settlement);
     - restriction class consistent with the sampled fund-agreement evidence;
     - every acknowledgment links to exactly one contribution;
     - anonymous grants carry no donor-identity fields to the grantee view.
  3. **Mutation tests**: the conformance harness injects total-preserving swaps into a copy of the data and the mapping must catch every one. Swaps include advisor↔successor, restricted↔unrestricted, approved↔paid at the same amount, acknowledgment flags, and the payee on two equal-amount grants.
- `CustomerConfirmed` requires a **stratified record-level sample** (default: every record type × status × restriction class, at least 5 records per stratum), traced from source report → canonical → rendered Unbound view. A named sponsor role attests it.
- Each mapping decision records AI provenance: model, prompt hash, proposal, and the human decision. That record goes in the auditor pack (16).
- A `Proposed` mapping can be used only in a rehearsal cell and never for a production import. AI narrative explaining a mapping is labelled and rendered separately from the deterministic test results (CNV-AIO-002).

## 5. Unsupported or divergent legacy behaviours (detection catalogue)

| Pattern detected | Why it matters for Unbound | Default disposition |
|---|---|---|
| In-platform unit register with daily unitization | CNV-FIN-005: values come from the external manager or custodian, so the unit register may need `BookOfRecord=Shadow` (UNB-XIN-ACC-010) | Sponsor decision: Unbound becomes the unit register (UNB-NAV-031 conversion) or stays in shadow |
| Donor ACH debit origination by the platform | Not in release 1 (CNV-FIN-003 note) | Move to the sponsor's processor, and disclose |
| Agency / pass-through / scholarship funds | Need an AgencyLiability treatment (UNB-XIN-ACC-001); community-foundation features are outside the entry segment (CNV-ECO-004) | Flag; may be out of scope |
| Retroactive fee rebates, tiered breakpoints recomputed over history | Fee schedules are versioned and prospective (CNV-FIN-002) | Import the historical fees as facts; new schedule effective from the epoch |
| Grants to individuals, or expenditure-responsibility grants | Not standard DAF grant flows | Block or route to the sponsor |
| Free-text restrictions | Must be structured (WFM-26-T02 guard) | AI proposes a structure; the sponsor confirms each class |
| Checks printed in-house from the legacy system | Positive pay continuity (CNV-PAY-002; see 17) | Plan the check-number range partition |
| Legacy "approved" charity labels | UNB-CHAR-041: not authoritative | Re-verify under CNV-GRT-003 before first grant |
| Missing variance-power evidence in fund agreements | RR-UNB-ACC-033-r1 suspense classification | Collect evidence before the first close |

## 6. Effort model (no fabricated dollars)

`EffortHours = Σ_c (count_c × minutes_c / 60) + Σ_d decisions_d × hours_d + fixed_adapter_hours(platform)`

`count_c` comes from the profile (counts of exceptions per class in 15). `minutes_c`, `hours_d` and adapter hours are **labelled ASSUMPTIONS** that the coordinator should calibrate from rehearsals. The report shows the drivers, so the sponsor can see that, for example, "4,112 payees without verified bank evidence" dominates. That number matters because of RR-REQ-X-061-r1, under which imported payees are blocked until verified, and payees already enrolled with a supported networked rail partner are exempt (CNV-EXP-002).

## 7. Readiness report (contract)

`ReadinessReport { engagement_id, tier_reached, adapter_id@version, profile_hash, mapping_version_hash?, history_depth{entity→(earliest_date, completeness: Full|Partial|BalancesOnly|NotProvided)}, domain_status[{domain, RAG, blocking_findings[], non_blocking[]}], unsupported_behaviours[], required_customer_decisions[], reconciliation_dry_run{gate_id→pass|fail|not_run}, effort_drivers[], assumptions[], calendar_constraints, legal_basis_refs[], deletion_deadline }`

Every RED status cites a rule ID and a count. A domain can never be GREEN when its reconciliation gate shows `not_run`.

## 6a. Sponsor-side work is moved, not removed (ADVB-06)

The sponsor's duties are:
- run the T1 reports;
- confirm mappings and restriction classes;
- attest the record-level sample;
- fix-in-source exceptions;
- prepare explained differences;
- obtain the CFO/finance approvals of the reconciliation report;
- decide remediation for unsupported behaviours;
- sign the cutover decision.

Unbound should present migration as reducing consultant spend, not as removing customer work. It should offer a priced, Unbound-staffed sponsor-side analyst. That analyst may prepare the work but may not give the A4 approvals (segregation of duties). Sponsor hours are measured in the first migration (CNV-ECO-003 evidence obligations); the modelling is draft 20's.

## Implications for Unbound

1. Ship the **T1 profiler kit** as a free, offline, open-format tool. It shortens sales cycles without data-protection negotiation, and the competitor practices documented above offer nothing comparable publicly (not publicly documented, which does not mean absent).
2. Treat the readiness report as the **seed of the migration contract**. Its gates and exception classes become the acceptance criteria in 15 and 16.
3. Make the history-depth disclosure honest. "Full history" (CNV-EXP-002) has to mean "everything the predecessor holds and can export", with explicit `HistoryIncomplete` where it does not.

Candidate requirements (new namespace UNB-MIG; none exists in `baseline.jsonl` as of 2026-11-26):
- **UNB-MIG-001** Assessment exposure tiers T0-T4, with an upload rejected unless a tier-matching LegalBasis exists (refines REQ-X-061, UNB-REM-008).
- **UNB-MIG-002** T1 profiles with k-suppression and a direct-identifier scan, quarantine and deletion certificate. Assessment data has a fixed destruction deadline, subject to legal holds (UNB-XIN-REC-001).
- **UNB-MIG-003** Mapping state machine Proposed→Tested→CustomerConfirmed→Approved. AI-proposed mappings cannot be used for production import (refines WFM-26-T02, CNV-AIO-001/002).
- **UNB-MIG-004** Readiness report schema, including per-entity history depth, gate dry-run status, **Extraction Plan** and **migration class**.
- **UNB-MIG-005** The `Tested` mapping state requires semantic invariants and mutation-test coverage of total-preserving swaps. `CustomerConfirmed` requires a sponsor-attested stratified record-level sample (ADVB-09).

## Open questions / evidence gaps

- Sponsor appetite for running an on-premises profiler (HYPOTHESIS). Test with design-partner interviews (CNV-EVB-002 requires implementation cost from ≥3 migrations).
- Whether state-law processor terms require specific DPA clauses for pre-contract evaluation. Needs counsel.
- Whether SP 800-38G Rev. 1 has been finalized. Only the 2nd draft was seen [MIG-018].
- No sponsor-side Ren export documentation was found. Assessment for Ren-hosted sponsors depends on what the sponsor obtains contractually (L16-L18 pattern).

## Adversarial review response

| ID | Response |
|---|---|
| ADVB-02 | **Accepted.** T0 now produces an Extraction Plan (§2a). Later stages depend on the extract cadence the contract allows (15 §1a). |
| ADVB-04 | **Accepted for distributor-on-vendor-sponsor programs.** Added the §2b migration class and the T0 "legal sponsor of record" question. Self-sponsored books on SaaS stay PlatformReplacement. |
| ADVB-06 | **Accepted.** Added §6a: duty list, analyst option, and measurement. Hour modelling belongs to draft 20. |
| ADVB-09 | **Accepted.** Semantic invariants, mutation tests, a stratified attested sample and AI provenance added (§4; UNB-MIG-005). |
| ADVB-14 | **Accepted.** T1 is defined on direct-login standard reports; added the pathway and timeline and the intent-signalling point. Timeline ranges are labelled ASSUMPTION. |
| ADVB-15 | **Accepted.** AEF stated as "33 months imported, 2 years visible". Numeric parameters are owned by 17 §0. |

