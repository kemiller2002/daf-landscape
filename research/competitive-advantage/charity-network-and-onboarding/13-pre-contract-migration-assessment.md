# 13 - Pre-contract migration assessment (B4)

Status: research draft (2026-11-26). Not legal advice. Evidence classes per 01-research-methodology.md.

Scope: a capability that lets a prospective sponsor learn, *before signing*, how hard its migration to Unbound will be, without handing over raw donor data unless and until a lawful basis exists. Builds on `research/migration-runbook-2026.md` (M01-M20 synthetic acceptance cases), `data/switching-cost-control-matrix-2026.csv` (L01-L30) and the Unbound workflow WFM-26 (`unbound:requirements/reconciliation/2026-11-23/workflows/WFM-26-sponsor-migration.json`). Notation: `(CLASS, confidence)`.

## Summary

- **Switching cost is driven by unknowns, so assessment should come before the contract.** No public source gives migration TCO for a DAF platform (L27, `data/switching-cost-control-matrix-2026.csv`). The public cases that do exist show history loss and long timelines. AEF's Ren pilot pulls only 33 months of grant history [MIG-012] (VERIFIED-FACT, High). Foundant's beginning-balance path carries balances only, with history as a separate non-GL import [MIG-001][MIG-003] (VENDOR-CLAIM, Medium). One FIMS replacement planned at 18 months ran past two years [MIG-025] (VENDOR-CLAIM, Low). A sponsor that can see its migration risk in advance is easier to win (INFERENCE, Medium).
- **Use a five-tier exposure ladder (T0-T4).** The tiers run from a questionnaire up to a full trial conversion. Most go/no-go questions can be answered at **T1**: a profile the customer runs on its own premises that emits only the schema and suppressed aggregate statistics, so no record-level personal data leaves the sponsor (RECOMMENDATION, Medium).
- **Format-preserving tokenization (FF1) is useful but does not anonymize.** It keeps joins and formats intact, so mappings and referential checks still work. However, the tokens are deterministic, and amounts and dates remain quasi-identifiers, so tokenized samples stay personal data under state laws that cover nonprofits [MIG-020]. Use FF1, not FF3: NIST's 2nd draft of SP 800-38G Rev. 1 drops FF3 [MIG-018] (VERIFIED-FACT, Medium).
- **Differential privacy suits benchmarking, not reconciliation.** DP noise breaks the exact control totals that the financial gates need (see 16). Use DP only for cross-prospect benchmark statistics, and evaluate it against the hazards in NIST SP 800-226 [MIG-019] (INFERENCE, High).
- **The legal basis is tiered.** T0-T1 need a mutual NDA. T2-T4 need a processor/service-provider agreement (DPA) with purpose limitation, deletion and a no-training clause. They also need a check that the sponsor's own donor privacy notice permits disclosure to a service provider. GLBA most likely does not bind a 501(c)(3) sponsor directly. Even so, Unbound should adopt Safeguards-Rule-equivalent controls by contract [MIG-021] (INFERENCE, Medium).
- **AI-generated mappings are proposals and are never authoritative.** A mapping version becomes usable only after two things happen. First, a deterministic **round-trip reconciliation** passes: source control totals = re-projected canonical totals. Second, the sponsor confirms it under WFM-26-T02 (A4, segregation of duties). This follows CNV-AIO-001/002.
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
| T0 Questionnaire | Nothing record-level | Platform/version, fund count, pools, custodians, rails, fiscal year, history years, contract end date | NDA | Adapter choice, segment fit (CNV-ECO-004), calendar window | Data quality |
| T1 Schema + statistics profile | Schema, row counts, null/distinct ratios, value-pattern classes, date ranges, **control totals per fund bucket**; cells with fewer than k (default 10) contributors suppressed | Profiler kit run by the sponsor; signed JSON profile | NDA (and confirmation that no personal data is in the profile) | Structural complexity, missing fields, referential gaps, history depth, a first tie-out of totals | Record-level matching, duplicate persons |
| T2 Tokenized sample | Stratified sample (e.g. 500 funds incl. edge states) with FF1-tokenized identifiers and names; free text dropped; amounts and dates kept | Sample + token-domain manifest; key held by the sponsor | NDA + DPA | Mapping validation, identity-collision rates, restriction encoding | Contacting donors, and anything needing the clear text |
| T3 Authorized representative export | Full export, in a per-prospect isolated assessment enclave | Export bundle + hash manifest | NDA + DPA + documented sponsor authority + privacy-notice check | Full profiling, exception inventory, effort model | Live comparisons with the running legacy system |
| T4 Trial conversion | T3 data through the factory (15) into a rehearsal cell | Simulation run, reconciliation report | As T3 + statement of work | Conversion simulation, reconciliation gate results (16) | Cutover behaviour under live traffic |

Rules (RECOMMENDATION):
- Tiers are monotonic per engagement. Moving up a tier requires a recorded `LegalBasis` reference for that tier. An upload whose tier does not match its basis is rejected **before** it is persisted.
- A T1 profile is scanned on receipt for anything that looks like a direct identifier (email, phone, SSN/EIN patterns, personal names in free text). If any is found, the profile is quarantined, purged within 24h and recorded on a deletion certificate, and the sponsor is notified.
- T2 tokens use FF1 under a **sponsor-held key** (or a key escrowed in the sponsor's tenant), so Unbound cannot detokenize during assessment. Per CNV-TEN-001, tokens never enter a cross-tenant store.
- All tiers ≥T2 are treated as production-class PII for access, logging and retention. Each has a fixed **assessment retention deadline** (default 90 days after report delivery or no-decision), after which it is destroyed with a certificate, unless a legal hold applies (UNB-XIN-REC-001).

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
- `Tested` requires that, for every mapped financial measure, Σsource = Σcanonical exactly per fund and per period, and that record counts match per entity class or that every difference is itemized.
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

## Implications for Unbound

1. Ship the **T1 profiler kit** as a free, offline, open-format tool. It shortens sales cycles without data-protection negotiation, and the competitor practices documented above offer nothing comparable publicly (not publicly documented, which does not mean absent).
2. Treat the readiness report as the **seed of the migration contract**. Its gates and exception classes become the acceptance criteria in 15 and 16.
3. Make the history-depth disclosure honest. "Full history" (CNV-EXP-002) has to mean "everything the predecessor holds and can export", with explicit `HistoryIncomplete` where it does not.

Candidate requirements (new namespace UNB-MIG; none exists in `baseline.jsonl` as of 2026-11-26):
- **UNB-MIG-001** Assessment exposure tiers T0-T4, with an upload rejected unless a tier-matching LegalBasis exists (refines REQ-X-061, UNB-REM-008).
- **UNB-MIG-002** T1 profiles with k-suppression and a direct-identifier scan, quarantine and deletion certificate. Assessment data has a fixed destruction deadline, subject to legal holds (UNB-XIN-REC-001).
- **UNB-MIG-003** Mapping state machine Proposed→Tested→CustomerConfirmed→Approved. AI-proposed mappings cannot be used for production import (refines WFM-26-T02, CNV-AIO-001/002).
- **UNB-MIG-004** Readiness report schema, including per-entity history depth and gate dry-run status.

## Open questions / evidence gaps

- Sponsor appetite for running an on-premises profiler (HYPOTHESIS). Test with design-partner interviews (CNV-EVB-002 requires implementation cost from ≥3 migrations).
- Whether state-law processor terms require specific DPA clauses for pre-contract evaluation. Needs counsel.
- Whether SP 800-38G Rev. 1 has been finalized. Only the 2nd draft was seen [MIG-018].
- No sponsor-side Ren export documentation was found. Assessment for Ren-hosted sponsors depends on what the sponsor obtains contractually (L16-L18 pattern).
