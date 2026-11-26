# 05 - Independent charity registry: identity, provenance and distribution

Status: research draft (2026-11-26). Not legal advice. Evidence classes per 01-research-methodology.md.

Track A3. Owner: REG. Companion files: [06-continuous-vetting.md](06-continuous-vetting.md), [data/identity-resolution-cases.csv](data/identity-resolution-cases.csv) (38 synthetic cases), [data/vetting-state-model.json](data/vetting-state-model.json), [scripts/reg_source_change_volumes.py](scripts/reg_source_change_volumes.py) (stdlib, reproduces every computed number below), [data/sources-REG.csv](data/sources-REG.csv).

## Summary

- **Most of this registry is already specified.** UNB-CHAR-001..042, UNB-EXT-001..038, UNB-KNOW-001..040 and the adopted refinements (RR-REQ-X-007-r1, UNB-RCN-GRT-013/014, RR-UNB-CHAR-013-r1, RR-UNB-EXT-028-r2) already require an immutable charity ID, effective-dated claims with provenance, no silent last-write-wins, reversible merges and a shared-public / sponsor-private split. This file maps each element to those IDs (section 2) and proposes only 11 new requirements (section 9). RECOMMENDATION, High.
- **The hard identity cases are a large share of the population, not edge cases.** In the 2026-11-10 EO BMF: 237,380 501(c)(3) rows are group-exemption subordinates, and **every one of them is absent from Pub 78**; 235,926 c3 organizations share a normalized name with at least one other (Toastmasters 6,143; Parent Booster USA 6,218); 317,386 share a street address (2,159 addresses hold 10 or more). On the revocation list, 19,351 EINs have more than one revocation episode. VERIFIED-FACT (computed from IRS files), High.
- **IRS rules make the EIN a strong, but not sufficient, key.** An EIN is "that entity's permanent federal taxpayer ID number" [REG-004]; a merger survivor and a renamed organization keep their EIN, but a new corporation after a statutory merger or a new charter needs a new one [REG-005]. Reliance on Pub 78/BMF covers only the "official name, recognized popular name, or a contraction" and **does not apply to group subordinates at all** [REG-002 §6.01, §6.03]. VERIFIED-FACT, High.
- **A third time axis is needed.** Bitemporal (valid time vs recorded time) is not enough: IRS reliance rules key on the **public posting date**, which lags the revocation's effective date by a median of 89 days (p90 119) for 2025 postings. The median is an artefact of the single August batch (in 2026, 39,415 of 53,120 postings sat at exactly 88 days, ADVA-16); outside that batch the lag varies. Grants made before posting by unaware grantors stay protected [REG-002 §4.02]. The claim model must carry valid time, source-publication time and recorded time. VERIFIED-FACT (rule and lag), High; RECOMMENDATION (model).
- **Claim precedence must be per predicate, not per source.** The IRS outranks a charity on exempt status; the charity outranks the IRS on its website and contacts; a central organization outranks both on whether a subordinate is in its group [REG-001]. Lower tiers may *dispute* but never *replace* a higher-tier claim. RECOMMENDATION, High.
- **The public directory is already commoditized.** IRS bulk files are public-domain government works [REG-020], ProPublica offers a free API over the same BMF [REG-022], and Ren's claimed "1.8M+" directory is about the size of the whole EO BMF (1,984,891 EINs) (data/ren-network-metrics.csv). Incumbent advantage lies elsewhere: accumulated **resolution of messy recipients** (22,269 top-50 recipient EINs, $4.18bn, are not in the BMF and 85% appear in no IRS bulk file at all; research/mission-2026-11-14/b40n1202-b43n26-03-non-bmf-recipients.md), **enrolled payment destinations**, **authorized charity contacts** and **decision history accepted by auditors**. INFERENCE, Medium-High.
- **Distribution recommendation.** Do not run a commercial charity-data service in release 1. Do design the shared public layer so it can later be published as an open, reliance-grade (Rev. Proc. 2018-32 §8.01) status and identity-crosswalk dataset. Publish only verbatim public-source facts with posting dates, never Unbound judgments, to keep defamation exposure close to that of republishing government records. RECOMMENDATION, Medium.
- **SharedStoreRegister.** Six proposed shared stores (section 7). One inference risk is new: per-sponsor monitoring watchlists and identity-resolution request logs would reveal sponsors' grantee portfolios and donors' intentions. The fix is to monitor the **whole public universe** and keep requester identity in the sponsor cell. RECOMMENDATION, High.

## 1. What the registry must hold: twelve separated layers

Each row is a distinct store or partition with its own writer, authority and sharing rule. "Shared" means a store listed in the CNV-TEN-001 SharedStoreRegister (section 7).

| # | Layer | Contents (examples) | Writers | Authority | Scope | Existing IDs |
|---|---|---|---|---|---|---|
| L1 | Organization identity | Unbound Charity ID, entity kind (legal entity, program/project, chapter, disregarded entity, government unit, foreign org), lifecycle | Platform resolution service; steward for merges | Resolution decisions (L1 only changes via ResolutionDecision) | Shared | UNB-CHAR-001, -003, UNB-KNOW-001, -007 |
| L2 | Legal identity | Identifier assertions (EIN, state entity no., foreign reg. no.), legal name, alternative/popular names, former names, each with valid interval | Ingestion from primary sources; steward | Issuing authority per identifier | Shared | UNB-CHAR-002, -004, UNB-KNOW-006 |
| L3 | Regulatory classification | Subsection, foundation code, deductibility, SO type, group exemption number (GEN) and affiliation, revocation/reinstatement episodes | Ingestion only (IRS, state) | Government source | Shared | UNB-EXT-001, RR-REQ-X-007-r1 |
| L4 | Publicly reported facts | 990/990-N filings, addresses, officers as filed, website as published | Ingestion | The publishing source, as self-report to government | Shared, subject to rights (UNB-EXT-025) | UNB-EXT-006, -011, UNB-KNOW-009 |
| L5 | Independently verified facts | Facts Unbound re-verified from a primary source (e.g. "Pub 78 posting 2026-11-11 lists EIN X as PC") | Verification service | Policy version that performed verification | Shared | UNB-EXT-022, UNB-KNOW-030, CNV-GRT-004 |
| L6 | User-submitted claims | Charity portal submissions, sponsor-submitted corrections, migrated legacy labels | Charity representatives, sponsors, migration | None until verified ("submissions are claims") | Charity-private or sponsor-private until verified; only re-verified **public** facts promote to L5 | UNB-CHAR-014, -041, SPD-GRT-002 |
| L7 | Verification evidence | Immutable artifacts: source payload, hash, retrieval time, posting date, parser version, rights policy | Ingestion; uploads | Source | Public evidence shared; private uploads stay in owning cell | UNB-CHAR-008, UNB-EXT-020 |
| L8 | Sponsor-specific eligibility | Sponsor policy overlay result, reliance snapshot, discretionary holds, exclusions, investigations | Sponsor cell only | Sponsor board via DoA (CNV-GRT-001) | Sponsor cell | UNB-CHAR-018..023, -031, CNV-GRT-004/005 |
| L9 | Grant-specific eligibility | Per-grant approval and release checks, purpose, amount, payee binding | Sponsor cell | Sponsor policy version + delegate | Sponsor cell | UNB-CHAR-019, -021, RR-REQ-X-007-r1 |
| L10 | Authorized representatives | Charity users, roles, proofing level, authority evidence | Charity portal; steward | Charity governance evidence | **Charity cell** (proposed, section 7) | UNB-CHAR-007, -014, CHAR-ADR-006 |
| L11 | Payment destinations | Destination evidence, rail enrolment reference, bank-change history | Rail partner; sponsor treasury; charity | CNV-PAY-002 evidence | Sponsor cell or rail partner; never shared store | UNB-CHAR-029, -032, CNV-PAY-002, CNV-EXP-002 |
| L12 | Historical decisions | Resolution decisions, verification results, eligibility evaluations with exact evidence versions | Each layer's decision service | As recorded | Shared for L1/L5 decisions; sponsor cell for L8/L9 | UNB-CHAR-025, UNB-KNOW-014, KNOW-T15 |

Two rules bind the layers (RECOMMENDATION):

1. **Downward only.** L8/L9 may read L1-L5 and L7 (public). L1-L5 never read L6, L8-L11. A sponsor's private evidence reaches L5 only when the platform re-fetches the same fact from the public source (SPD-GRT-002, CNV-GRT-004).
2. **Identity is not eligibility is not payability.** Passing L1 resolution says nothing about L3/L5 status, and neither says anything about L11 (UNB-CHAR-006, -026).

## 2. Mapping to the existing requirement baseline

| Design element in this file | Already covered by | What this file adds |
|---|---|---|
| Immutable ID, aliases, history, merges/splits | UNB-CHAR-001/002/004/005/009, UNB-KNOW-008/017-020 | Concrete resolution pipeline and outcome codes (section 4); gold-set cases (CSV) |
| Claims with provenance, conflicts kept | UNB-CHAR-008/012, UNB-EXT-020/030, UNB-KNOW-003/004 | Per-predicate authority lattice (section 5.3) |
| Bitemporal | UNB-KNOW-002, UNB-CHAR-040, KNOW-T05/T15 | Third axis, source-publication time, needed for Rev. Proc. 2018-32 reliance (section 5.2) |
| Entity-type evidence (churches, subordinates, government) | UNB-RCN-GRT-013, UNB-CHAR-003/016, CHAR-T04 | Group resolution algorithm via central org; measured population sizes |
| Shared vs private | UNB-CHAR-036/037, UNB-KNOW-012, CNV-GRT-004, CNV-TEN-001 | SharedStoreRegister entries and inference risks (section 7) |
| Stewardship only for unresolvable cases | RR-UNB-CHAR-013-r1, UNB-EXT-023 | Outcome taxonomy that decides when a case opens |
| Charity portal and disputes | UNB-CHAR-014/017, XID-CLM-001, CHAR-ADR-006 | Charity cell for representatives (L10) |
| Search binding to canonical ID | UNB-RCN-PLT-014 | Lookalike/fraud checks at binding (section 4.3) |
| External publication | UNB-EXT-035, UNB-KNOW-040, CHAR-ADR-008, KNOW-ADR-010 | Option evaluation (section 8) |
| Merger successor | XID-NPG-005, UNB-XIN-NPG-005, CNV-GRT-010 | Identity side: survivor vs new-EIN successor (section 3) |

## 3. Identity facts the design must respect

| Case | Rule or measured fact | Evidence class, confidence | Design consequence |
|---|---|---|---|
| EIN permanence | "Once we assign an EIN to a business entity, it becomes that entity's permanent federal taxpayer ID number." The IRS deactivates but cannot cancel an EIN [REG-004] | VERIFIED-FACT, High | An EIN never legitimately moves to another legal entity. An EIN whose observed name changes completely, with no name-change evidence, is a data error or fraud signal, not reuse |
| New EIN required | After "a new corporation after a statutory merger", "a new corporate charter", or becoming a subsidiary using the parent's EIN [REG-005] | VERIFIED-FACT, High | A successor can have a new EIN: model `SuccessorOf` edges between L1 identities; never re-key the old identity |
| No new EIN | Name change; survivor of a corporate merger; reorganization that only changes "identity, form, or place of organization" [REG-005] | VERIFIED-FACT, High | Name change = new L2 name claim on the same identity (Material-Neutral, 06) |
| Group exemptions | Central organization, not the IRS, "determines which organizations are included as subordinates"; verify via the "official subordinate listing approved by the central organization or by contacting the central organization directly"; subordinates "are not listed separately" in Pub 78 [REG-001] | VERIFIED-FACT, High | Subordinate status = central's current IRS status AND central-approved inclusion evidence |
| Subordinates in the data | 237,380 c3 BMF rows have affiliation code 9 (subordinate); 100% are absent from Pub 78; 2,622 distinct GENs among c3 rows; largest group 16,914 rows | VERIFIED-FACT (computed, BMF posted 2026-11-10 [REG-010], Pub 78 file 2026-11-11 [REG-009]), High | A Pub 78-only check falsely rejects about 14% of c3 organizations; the BMF lists subordinates even though [REG-001] says most are not |
| No reliance for subordinates | Reliance provisions "do not apply to a subordinate organization covered by a group exemption letter regardless of whether the subordinate organization appears in the EO BMF Extract" [REG-002 §6.03] | VERIFIED-FACT, High | CNV-GRT-003's "flag subordinates for additional verification" is legally grounded. The additional verification is central-org evidence, cacheable per group (06) |
| Churches | Churches "are automatically considered tax exempt and are not required to apply" [REG-006]; non-applying churches are not in the BMF [REG-011] | VERIFIED-FACT, High | Absence from every IRS file is expected for many churches (UNB-CHAR-016); entity-type evidence path (UNB-RCN-GRT-013) |
| Church scale | 293,661 c3 BMF rows have foundation code 10 (church); 125,381 of them are not in Pub 78. In top-50 DAF grants, 14,772 recipient EINs with religious-pattern names ($1.35bn) appear in no IRS file | VERIFIED-FACT (computed; internal non-BMF study), High | Church resolution is a volume problem, not an exception |
| Names | Reliance covers "official name, its recognized popular name, or a contraction of either ... reasonably identifiable or widely known" [REG-002 §6.01]; Pub 78 excludes DBA names (research/mission-2026-11-14/direction-data-standards-interoperability.md) | VERIFIED-FACT, High | Keep legal, popular, DBA and former names as separate typed L2 claims; payee name = listed legal name (CNV-GRT-003) |
| Name collisions | 36,932 normalized c3 names are shared by 235,926 organizations | VERIFIED-FACT (computed), High | Name match is never a resolution; EIN plus location plus GEN context are required |
| Shared addresses | 102,050 street+ZIP keys are shared by 317,386 c3 organizations; 2,159 keys host 10 or more | VERIFIED-FACT (computed), High | Address is weak evidence; registered-agent and accountant addresses must not create relationship edges (UNB-KNOW-018) |
| Duplicate rows | 5,060 EINs appear twice across the IRS regional files (region 4 overlaps the PR and international files), always with identical names | VERIFIED-FACT (computed), High | Ingestion must dedupe by EIN across files; idempotency test (CHAR-T19) |
| Repeat revocations | 1,228,742 EINs on the Auto-Revocation List; 19,351 with more than one row | VERIFIED-FACT (computed, list file dated 2026-11-17 [REG-008]), High | Revocation is an episode list per identity, not a flag |
| Cross-source conflict | 31,614 EINs still on the BMF have an unreinstated latest revocation row (definition: the EIN's latest Auto-Revocation List row, tie-break latest posting date then latest revocation date, has no reinstatement date; `revocation-conflicts` in the script); 19,688 of them are also in Pub 78 (19,698 Pub 78 EINs in all). For 22,402 (71%) the BMF ruling month is later than the revocation date, which points to re-recognition under a new determination; 9,212 remain unexplained. Other drafts' figures differ by 1-11 because of tie-break rules (ADVA-05) | VERIFIED-FACT (computed), High; re-recognition reading INFERENCE, Medium | Re-recognised group: deterministic reliance on the later listing [REG-002 §4.06]. Remaining ~9,200: deterministic hold-free status from the current listing, plus counsel question below; see 06 section 7 |
| Mergers / termination | Terminating organizations file a final return by the 15th day of the 5th month after termination [REG-019]; succession effects are already decided (XID-NPG-005, CNV-GRT-010) | VERIFIED-FACT, High | Final-return flag in the e-file index is an early dissolution signal; at top-50 sponsors, 884 recipient EINs ($220m) had filed final returns (internal non-BMF study) |
| Fiscal sponsorship | No IRS registry of fiscal sponsor/project relationships; CNV-GRT-008 accepts a published project list or signed attestation for a §170(b)(1)(A) sponsor that keeps discretion and control | VERIFIED-FACT (absence of an IRS list) Medium; ratified rule High | Project is an L1 node with no legal identity; payee = fiscal sponsor's L2; relationship edge carries attestation evidence |
| Proposed group-exemption overhaul | Notice 2020-36 proposed replacing Rev. Proc. 80-27 (e.g. all subordinates under the same §501(c) paragraph) [REG-018] | VERIFIED-FACT that it was proposed; finalization status not verified in this pass | Keep group rules versioned in the rule watch list |

## 4. Identity resolution design

### 4.1 Pipeline (deterministic first, probabilistic only to propose)

Input: an `IdentityQuery` from search binding (UNB-RCN-PLT-014), migration import (UNB-CHAR-041), charity self-registration or an ingested source row. The requester's sponsor and donor context stay in the sponsor cell. The shared resolver receives only the query fields (section 7).

| Stage | Rule | Outcome if it decides |
|---|---|---|
| R0 Normalize | Unicode NFKC, case-fold, strip punctuation and legal suffixes for comparison only; keep the original string as evidence | none |
| R1 Identifier syntax | EIN must be 9 digits. Format failure leads to R5 with `IdentifierInvalid` | none |
| R2 Identifier lookup | Exact EIN against L2 identifier index, all episodes (current, revoked, terminated) | candidate set |
| R3 Name agreement | Compare query name with the candidate's legal, popular, DBA and former names valid at the query's as-of date. Agreement classes: Exact, Contraction/Popular, FormerName, Mismatch | `Resolved` if EIN hit plus Exact/Contraction/FormerName |
| R4 Context | If the candidate is a subordinate (affiliation 9 or GEN present), attach the central identity and require group evidence (06). If the candidate has a `SuccessorOf` edge or a termination flag, attach the successor | `ResolvedWithConditions` |
| R5 No/invalid EIN or Mismatch | Probabilistic candidate generation: name tokens with TF-IDF over legal and alias names, city/state, ZIP3, website domain, GEN membership. Scores are calibrated on the gold set (UNB-KNOW-019) | `Ambiguous` (more than one above threshold), `ProposedMatch` (one above threshold) or `Unresolved` |
| R6 Risk screen | Lookalike and impersonation checks (section 4.3) on every outcome | may add `Suspicious` |

Outcome codes (each is a typed `IdentityResolutionDecision`, UNB-CHAR-005):

| Code | Meaning | Auto-bind a grant? | Case opened? (RR-UNB-CHAR-013-r1) |
|---|---|---|---|
| Resolved | EIN hit plus name agreement | Yes | No |
| ResolvedWithConditions | Subordinate, former name, successor or disregarded-entity link | Yes, with the condition passed to eligibility | No, unless the condition's evidence fails |
| ProposedMatch | Single probabilistic candidate | Donor confirms on screen (search UX); migration requires steward sampling | No for donor-confirmed; sampled for migration |
| Ambiguous | Two or more candidates | No | Yes, unless the donor disambiguates in search |
| Unresolved | No candidate | No (UNB-RCN-PLT-014 AC-3) | Yes; automated evidence request first |
| Conflict | EIN hit with name Mismatch and no former-name evidence | No | Yes; this is the hijack/typo signal |
| Suspicious | R6 fired | No | Yes, fraud-trained reviewer |

### 4.2 Relationship edges

Typed, time-bounded, evidence-backed edges (UNB-CHAR-009, UNB-EXT-012): `SubordinateOf(GEN)`, `FiscallySponsoredBy`, `SuccessorOf(merger|consolidation|asset-transfer)`, `DisregardedEntityOf`, `ChapterOf` (non-group affiliation), `AmericanFriendsOf` (US charity supporting a foreign one), `SharesOfficerWith` (observed only, never inferred control), `RenamedFrom` (same identity, recorded as an L2 name episode, not an edge). Each edge records whether it was **observed** in a source or **inferred**; inferred edges never affect eligibility.

Real example in the data: Further Future Foundation was renamed Navigation Charitable Fund under the same EIN 92-1117448 in the BMF from the 2024-07 snapshot (research/mission-2026-11-14/g0503-0501-exception-proxy-refinements.md). The model records an L2 name episode, not a new identity. The disregarded-entity case is also real: four Chan Zuckerberg LLC EINs received $1.59bn of top-50 grants and are disregarded entities of a BMF-listed c3 (internal non-BMF study §3.2). Without a `DisregardedEntityOf` edge these grants would be "not in BMF".

### 4.3 Fraudulent lookalikes and impersonation

Signals (UNB-CHAR-028; flags, not verdicts):

- **Name proximity to high-volume grantees.** Edit distance or token overlap of 0.9 or more with one of the platform's top-N grantees, but a different EIN, a ruling date in the last 24 months and a different state.
- **New EIN with a famous name.** Ruling date within 12 months and a name collision with a large organization outside the same GEN.
- **EIN-name mismatch** (`Conflict` above). The typo case and the hijack case look identical at intake.
- **Website and contact drift.** Charity-portal claims that change the website domain or contact email to a domain registered recently. Domain age is collected only if lawful and proportionate; this is HYPOTHESIS-level value, to test on the gold set.
- **Payment-destination change after a representative change** is an L11 control (CNV-PAY-002, CNV-PLT-011), not an identity signal. Identity resolution must not be weakened to make payment changes easier.

### 4.4 Confidence model

Two separate numbers, never combined into one "trust score" (UNB-KNOW-005, UNB-CHAR-033):

- **Match confidence** (L1): calibrated probability that a query refers to the candidate identity, from the gold set. Thresholds are chosen per outcome by false-merge cost (RR-UNB-CHAR-013-r1#Q1). Deterministic `Resolved` is recorded as `method=deterministic` with no probability.
- **Claim confidence** (L2-L5): an ordinal, not a probability: `{authority tier (5.3), currency (current publication | prior publication | stale), corroboration (1 source | 2+ independent), verification (observed | verified | disputed)}`. Policies test these components directly (e.g. "tier 1, current publication").

## 5. Provenance, time and precedence

### 5.1 Claim record

`Claim{claimId, subjectId, predicate (versioned ontology, UNB-KNOW-006), value, validFrom, validTo, sourcePublishedAt, recordedAt, supersededAt, sourceId, sourceVersion (posting date or file hash), evidenceIds, extractionMethod (structured | parser vN | AI-extracted | human-entered), authorityTier, status (observed | verified | disputed | stale | superseded | withdrawn), rightsPolicyId, scope (shared | sponsor:<id> | charity:<id>)}`. This extends the UNB-CHAR claim fields with `sourcePublishedAt`, `authorityTier` and `scope`.

### 5.2 Three time axes

| Axis | Question it answers | Example: automatic revocation |
|---|---|---|
| Valid time | When was it true in the world? | Revocation effective 2026-05-15 (filing due date) |
| Source-publication time | When did the authoritative source make it public? | Posted on the Auto-Revocation List about 89 days later (2025 median; p90 119 days) |
| Recorded time | When did Unbound learn it? | Ingested within 24 hours of posting (CNV-GRT-003 operational target) |

Why three: Rev. Proc. 2018-32 §4.02 protects grants "made on or before the date its name is posted on the Auto-Revocation List" by unaware grantors [REG-002]. In an illustrative case, a grant released on 2026-06-20 to an organization revoked effective 2026-05-15 but posted 2026-08-12 was protected, even though valid-time says "revoked". A bitemporal model that recomputes eligibility "as of" valid time would wrongly label that grant a violation. The §4.04 exception also matters: a grantor that "had knowledge" before posting loses reliance. So when Unbound records an adverse fact before the IRS posts it (e.g. a final return), the knowledge timestamp is in the sponsor's reliance record. VERIFIED-FACT (rule), High; INFERENCE (model need), High.

Queries the store must answer (KNOW-T15 extended): (a) what was true at T (valid); (b) what had the IRS published at T (publication); (c) what did Unbound know at T (recorded); (d) what did sponsor S rely on for grant G (its reliance snapshot).

### 5.3 Claim precedence lattice (per predicate)

Tiers: **T1** government primary record (IRS BMF/Pub 78/revocation list, OFAC, state registry of record); **T2** filed-with-government self-report (990 series, determination letter held by the charity); **T3** accountable counterparty record (central organization's subordinate listing, fiscal sponsor attestation, bank or rail account-ownership verification); **T4** authenticated charity representative submission; **T5** sponsor submission or migrated legacy label; **T6** third-party or web content; **T7** AI extraction not yet verified against its source.

| Predicate class | Highest authority | May a lower tier replace it? | Lower-tier contradiction does |
|---|---|---|---|
| Exempt status, subsection, foundation code, deductibility, revocation | T1 | Never | Opens a dispute record. A case only if it changes an eligibility or payee outcome |
| Subordinate inclusion in a group | T3 (central organization) [REG-001] over T1 BMF GEN | T1 GEN is corroboration only | A central listing that omits a BMF subordinate makes the claim `disputed`, and eligibility holds |
| Legal name | T1 (IRS name) for payee binding; T2 for state-of-incorporation name | No | A charity-submitted new name stays a claim until T1 shows it; the payee name stays the listed name (CNV-GRT-003) |
| Popular/DBA name, website, mission text, logo, public contact | T4 (the charity speaks for itself) over T6 | T6 cannot replace T4 | T6 adds an alias candidate only |
| Address | T1 for mailing of record; T4 for operating locations | No | Address change is Material-Neutral (06) |
| Officers | T2 as filed | No | Informational |
| Fiscal sponsor-project relation | T3 (fiscal sponsor) | No | Project-side claims cannot create the edge |
| Payment destination | T3 (account-ownership verification or charity-signed bank letter, CNV-PAY-002) | Never by T4-T7 | Triggers L11 change control, not an identity update |
| Merger succession | T1/T2 (final return, Schedule N, state filing) plus T3 successor confirmation | No | Steward case (human), because payee substitution follows (CNV-GRT-010) |

Projection rule (deterministic, rebuildable, UNB-KNOW-037): `current(subject, predicate, asOf) = the claim with the highest tier among status ∈ {verified, observed}` whose publication is current for its source. Ties inside one tier with different values give `Conflict`. A newer lower-tier claim never wins. AI-extracted claims (T7) cannot enter the projection until the extraction is re-verified against its quoted source span (CNV-AIO-002, UNB-KNOW-030, KNOW-T07).

## 6. Sponsor-specific and grant-specific layers, representatives, destinations

- **Sponsor eligibility (L8)** = `f(L5 verified facts at the reliance snapshot, sponsor policy overlay version)`, written in the sponsor cell (RR-REQ-X-007-r1). The overlay can only tighten the platform floor (UNB-RCN-GRT-014 AC-2).
- **Grant eligibility (L9)** adds purpose, amount, recipient class (CNV-GRT-002), fund-level conflicts and the payee binding: legal name plus EIN plus, for subordinates and fiscal sponsorship, the payee identity, which differs from the beneficiary identity (KNOW-T03, CHAR-T05).
- **Authorized representatives (L10).** A charity relates to many sponsors, so its representatives belong neither to a sponsor cell nor to the shared public store. A charity cell keyed by Unbound Charity ID holds representative identity, role and proofing (CNV-PLT-003), and contact-change holds (CNV-PLT-011). Sponsor cells see only `representativeVerified: true/false, level, asOf`.
- **Payment destinations (L11)** stay with the rail partner or the sponsor (CNV-PAY-001/002). The registry stores at most an opaque enrolment reference per sponsor cell. A destination verified for sponsor A is not reused for sponsor B unless the rail partner's own enrolment is the shared fact (CNV-EXP-002).
- **Historical decisions (L12)** are append-only. A later correction links to, and never edits, the decision it corrects (UNB-KNOW-013).

## 7. Shared public evidence versus sponsor-private data (CNV-TEN-001)

Proposed SharedStoreRegister entries. "Inference risk" is what a reader could deduce beyond the fields.

| Store | Permitted fields | Writers | Readers | Classification | Inference risks and mitigations |
|---|---|---|---|---|---|
| SS-REG-01 PublicSourceEvidence | Raw public files, hashes, posting dates, parsed T1/T2 claims | Ingestion service | All cells (read-only) | Public; rights-tagged | None beyond rights. Restricted-rights sources (UNB-EXT-025) are tagged and filtered on export |
| SS-REG-02 CanonicalIdentity | L1 identities, L2 identifiers and names, typed edges, resolution decisions | Resolver; steward (dual control for merges) | All cells | Public-derived | A resolution created *because* sponsor S asked about an unlisted church reveals S's interest. Mitigation: no requester field; creation time rounded to the day; resolutions also seeded from bulk sources |
| SS-REG-03 VerifiedPublicFacts | L5 facts with verifying policy version | Verification service | All cells | Public-derived | None if only public sources feed it (SPD-GRT-002) |
| SS-REG-04 PublicHoldPublications | Holds derived from verified public facts (revocation, Pub 78 removal, OFAC listing), with source and timestamp; versioned (CNV-ARC-003) | Monitoring service | All cells; dispatch fencing | Public-derived | Release 1: **no** neutral "enhanced review" flag (CNV-GRT-004 as amended by OD-P-GRT cut F) |
| SS-REG-05 MonitoringUniverse | List of monitored identities = **the entire ingested public universe**, not per-sponsor watchlists | Monitoring service | Monitoring service | Public-derived | A per-sponsor watchlist would reveal each sponsor's grantee book. Monitoring everything costs little: the IRS publishes whole-universe files monthly. Impact matching (which grants are affected) runs inside each sponsor cell |
| SS-REG-06 CharityPublicProfile | Charity-authored public claims (mission, website, logo, public contact) that the charity consented to share platform-wide | Charity cell, on explicit publish | All cells; donor search | Charity-consented public | Representatives' PII never enters; only the organization's role contact |

Not shared, ever: sponsor eligibility and reliance snapshots, investigations and discretionary holds (CNV-GRT-004/005), sanctions dispositions in release 1 (CNV-GRT-006 as amended), destination evidence, donor/advisor data (only keyed tokens, CNV-TEN-001), identity-resolution *requests* (they carry the requester), charity-private uploads (charity cell).

## 8. Distributing the public portion: options

Context first: public charity status data is already commoditized. The IRS files are free and public domain (17 U.S.C. §105 [REG-020]). ProPublica's Nonprofit Explorer API serves BMF and 990 data under its Data Terms of Use [REG-022]. Charity Navigator and Candid terms restrict AI and model use (research/mission-2026-11-14/b43n26-03-charity-data-terms-ai.md). Ren's claimed directory is about the size of the EO BMF (data/ren-network-metrics.csv). Publishing a directory therefore removes almost nothing from incumbents. INFERENCE, High.

**What incumbents actually accumulate** (INFERENCE from cited facts, Medium-High):

1. **The resolution crosswalk for messy recipients.** At the top-50 sponsors, 19.3% of grant lines went to recipients absent from Pub 78 (research/mission-2026-11-14/gap19-exception-load-proxy.md), and 22,269 recipient EINs ($4.18bn) were not in the BMF at all. Each incumbent has resolved these one grant at a time, and the knowledge sits in their history.
2. **Enrolled, verified payment destinations.** Fidelity pays 67% of grants by EFT through its own enrolment (data/payment-provider-matrix.csv). That reach is built by charities enrolling, not by data.
3. **Charity-side relationships:** authorized contacts, central organizations that answer subordinate queries, fiscal sponsors that attest to projects.
4. **Decision history and auditor familiarity.** Sponsors' auditors accept an incumbent's vetting packs; a new vetting regime must earn that.

| Option | Input licensing | Liability / defamation | Cost (order of magnitude) | Effect on incumbents | Verdict |
|---|---|---|---|---|---|
| Open dataset (identity crosswalk, group-subordinate resolution, change events, all with source and posting date) | IRS and OFAC public domain; 990 XML public; state data varies; aggregator data excluded | Low if limited to verbatim public facts with source. Unbound-authored judgments ("held", "risk") are Unbound's own content, and 47 U.S.C. §230 protects only information "provided by another information content provider" [REG-021] | Low marginal (data exists internally); support and correction-handling cost is the real one | Erodes item 1 above modestly; zero effect on 2-4 | **Later (post-R1)**, after CHAR-ADR-008 and counsel on RCD-029 |
| Public API (status lookup, reliance-grade report per Rev. Proc. 2018-32 §8.01) | Same | Same, plus availability expectations; a §8.01 report must state BMF revision date and time of report [REG-002 §8.01] | Moderate (SLA, abuse controls) | Commoditizes "Charity Check"-style lookups already near-free | Optional; only if it helps charity or sponsor acquisition |
| Searchable public directory | Same | Same; plus charity right-of-response duties (UNB-CHAR-017) | Moderate (accessibility, SEO, corrections) | Negligible; ProPublica and the IRS already provide it | **No**: not differentiating |
| Reusable Echelon component (bitemporal claim and provenance store, precedence lattice, resolution pipeline, no charity data) | n/a | n/a | Engineering only; shares cost with Strata (UNB-CHAR-040) | None directly | **Yes**: the generic engine is reusable; the data is not the asset |
| Independent commercial data service | Same, plus contract and warranty exposure | Highest: paying customers rely on Unbound judgments; E&O exposure; status statements about named charities | High (sales, support, SLA, legal) | Competes with Candid and Chariot verification; distracts from DAF servicing (CNV-ECO-004 entry segment) | **No** in R1; revisit only if registry quality becomes measurably better than public sources |

**Recommendation (RECOMMENDATION, Medium):** treat registry quality as a cost and reliability advantage inside Unbound, not as a product. Prepare the shared layer to be publishable (rights tags, verbatim-fact discipline, correction workflow) so an open crosswalk can be released later if it helps charity onboarding or regulators.

## Implications for Unbound

1. The registry's differentiator is **resolution coverage and change semantics**, not breadth. Build the group-subordinate, church, disregarded-entity and successor paths before any "more data" waves (UNB-EXT Wave 2-4).
2. Add the **source-publication time** axis now; retrofitting it after Strata schemas exist would require replaying all reliance snapshots (KNOW-ADR-001).
3. A **per-predicate precedence lattice** gives the charity real authority over its own self-description and none over its status. This makes the charity portal useful without opening a hijack channel.
4. **Monitor the whole public universe.** It is cheaper than it sounds: full-file monthly diffs (06) and no cross-tenant watchlist.
5. A charity cell (L10) is a new partition type in CNV-TEN-001 terms; architecture must confirm it.
6. Do not plan revenue from charity data. Plan to **reduce** the identity-resolution cost that incumbents carry implicitly.

## Release 1 versus later

Response to ADVA-20: the proposals are tiered so that Release 1 carries only what release-time eligibility and payee binding need.

| Tier | Items |
|---|---|
| Release 1 minimum | L1-L3, L5, L7 and L12 for IRS and OFAC sources; resolution outcomes (REG-P-04, REG-P-05); subordinate and church rules (REG-P-03, UNB-RCN-GRT-013); three time axes (REG-P-01); EIN dedupe and revocation episodes (REG-P-11); whole-universe monitoring and requester-free shared stores (REG-P-07, REG-P-08); shared stores SS-REG-01..05 |
| Release 1, minimal form | Precedence lattice (REG-P-02) for the predicates R1 uses: status, legal name, subordinate inclusion, payee. Typed edges (REG-P-06) only for SubordinateOf, SuccessorOf, FiscallySponsoredBy, DisregardedEntityOf |
| Later | Charity cell and SS-REG-06 charity public profile (REG-P-09), pending the architecture decision; lookalike domain-age signals (HYPOTHESIS); any external publication (REG-P-10), open dataset, public API, commercial service; Wave 2-4 acquisition (UNB-EXT) |
| Not proposed | Any cross-sponsor sharing of private verification evidence beyond re-verified public facts (ADVA-13); see below |

## Adversarial review response

| Finding | Verdict here | Change made |
|---|---|---|
| ADVA-04: BMF identity counts double-counted the 5,060 EINs repeated in eo_pr/eo_xx | Accepted | `bmf-profile` now counts each EIN once. Corrected figures: 1,659,108 c3; 237,380 subordinates; 36,932 shared names covering 235,926 organizations; 102,050 shared addresses covering 317,386; 2,159 addresses with 10 or more; largest group 16,914; Toastmasters 6,143; FC10 churches 293,661 (125,381 not in Pub 78). Updated in 05, the cases CSV and sources-REG.csv. The 06 BMF diff already keyed by EIN and is unchanged |
| ADVA-05: three different counts of revoked organizations still listed | Accepted | One definition and tie-break (latest posting date, then latest revocation date), implemented as `revocation-conflicts`: 31,614 on the BMF, 19,688 also in Pub 78. The remaining 1-11 differences from other drafts come from tie-break and are noted |
| ADVA-06: most of the 31,616 look re-recognized, not stale | Accepted | 22,402 (71%) have a BMF ruling month after the revocation: deterministic §4.06 reliance. Only ~9,200 go to the counsel question |
| ADVA-16: the 88-89 day median lag is an August-batch artefact | Accepted | Caveat added in the summary and in 06 section 2.2. The three-time-axis argument does not depend on the median |
| ADVA-13: shared verification adds correlated risk for small benefit | Accepted for this file | Shared stores hold only public facts, identity and resolution outcomes. Destination evidence (L11) stays per sponsor or with the rail partner. Cross-sponsor reuse of private verification evidence, and the neutral flag, are not proposed for Release 1 (consistent with CNV-GRT-004/006 as amended by OD-P-GRT cut F) |
| ADVA-14: no build/buy comparison | Partially accepted | Table below |
| ADVA-20: too many new requirements for a requirements-phase product | Accepted | Tiering above; REG-P-09 and REG-P-10 are later |
| Round-2 amendments (c10 CNV-PAY-002, c11 CNV-PLT-011) | Noted | Destination evidence combinations, 30-day callback-contact rule, CAL3 for charity contact and bank changes, and the charity contact/signatory hold are already ratified. L10/L11 here rely on them and add no requirement of their own |

Build/buy/hybrid (ADVA-14; ECO costs as reported by the reviewer, not re-derived here):

| Option | Cost signal | Covers | Does not cover | View |
|---|---|---|---|---|
| Build (this design) | ~$319k setup ($113k-$1.07M), ~$75k/yr (ECO) | IRS/OFAC status, §8.01-style report, subordinates, non-BMF resolution, three time axes | Auditor familiarity, until earned | Keep (UNB-CHAR-DEC-001) |
| Buy Candid as decision source | From $2,750/yr list API (VENDOR-CLAIM); platform/resale licence unknown | Same IRS/OFAC files | Subordinate rosters (§6.03), non-BMF recipients, payee verification; AI/ML and retention restrictions | Rejected; conflicts with UNB-CHAR-DEC-001 |
| Hybrid: non-runtime cross-check | Licence-dependent | Reconciliation QA and auditor comfort | Never a decision input | Evaluate only if the licence permits; pair with auditor interviews on Unbound §8.01 reports |

## Open questions / evidence gaps

- Does a continued BMF/Pub 78 row posted after an unreinstated revocation count as a "subsequent listing" under Rev. Proc. 2018-32 §4.06? This decides the ~9,200 BMF-listed EINs whose ruling date does not post-date the revocation; the 22,402 re-recognised ones fall under §4.06 directly. Counsel.
- Can the central organization's published directory (web page or PDF) stand as the "official subordinate listing" without a letter? Pub 4573 says either method works; how current must it be? Counsel and sponsor compliance.
- Gold-set precision and recall for R5. No labelled set exists yet (UNB-KNOW-019); build it from the 38 synthetic cases plus a stratified sample of top-50 non-BMF recipients.
- Status of the Notice 2020-36 proposed group-exemption procedure: not verified in this pass.
- Defamation exposure of publishing *public-fact* holds platform-wide (RCD-029 still "awaiting confirmation").
- Charity cell: does CNV-TEN-001's per-sponsor cell model allow a third, charity-keyed partition? Architecture owner.
- Whether a §8.01-compliant report generated by Unbound satisfies sponsors' auditors without Candid-branded output: needs auditor interviews (no evidence either way).

## Candidate requirements (proposed; refine existing IDs)

| ID (proposed) | Requirement | Refines |
|---|---|---|
| REG-P-01 | Every claim SHALL carry valid time, source-publication time and recorded time; reliance evaluation SHALL use publication time | UNB-KNOW-002, UNB-CHAR-040, RR-REQ-X-007-r1 |
| REG-P-02 | A versioned, counsel-approved PredicateAuthorityTable SHALL rank sources per predicate; lower tiers can dispute but never supersede | UNB-CHAR-012, UNB-EXT-030, UNB-KNOW-003 |
| REG-P-03 | Subordinate eligibility SHALL require the central's current status AND central-approved inclusion evidence, cached per GEN with its own validity | UNB-RCN-GRT-013, CNV-GRT-003 |
| REG-P-04 | Identity resolution SHALL emit one of seven typed outcomes (4.1); only Resolved/ResolvedWithConditions bind a grant without confirmation | UNB-CHAR-005, RR-UNB-CHAR-013-r1, UNB-RCN-PLT-014 |
| REG-P-05 | An EIN observed with a wholly different legal name and no rename evidence SHALL be treated as Conflict (EINs are never reassigned) | UNB-KNOW-017, UNB-CHAR-028 |
| REG-P-06 | Successor, disregarded-entity, subordinate and fiscal-sponsor relations SHALL be typed edges with observed/inferred flag; inferred edges never affect eligibility | UNB-CHAR-009, UNB-EXT-012 |
| REG-P-07 | Monitoring SHALL cover the entire ingested public universe; per-sponsor impact matching SHALL run in sponsor cells | CNV-TEN-001, RR-UNB-EXT-028-r2 |
| REG-P-08 | Identity-resolution requests SHALL keep requester context in the sponsor cell; the shared store records outcomes without requester and with day-rounded time | CNV-TEN-001, UNB-CHAR-037 |
| REG-P-09 | Charity representatives and charity-private uploads SHALL live in a charity-scoped partition; sponsor cells see only verification flags | UNB-CHAR-007/014, CNV-TEN-001 |
| REG-P-10 | Any external publication SHALL be limited to verbatim public-source facts with source and posting date; Unbound judgments are never published | UNB-KNOW-040, UNB-EXT-035, CHAR-ADR-008 |
| REG-P-11 | Ingestion SHALL dedupe EINs across IRS regional files and treat repeated revocations as separate episodes | UNB-KNOW-027, CHAR-T19 |
