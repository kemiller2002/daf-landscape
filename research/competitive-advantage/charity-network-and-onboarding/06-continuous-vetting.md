# 06 - Change-driven continuous vetting

Status: research draft (2026-11-26). Not legal advice. Evidence classes per 01-research-methodology.md.

Track A4. Owner: REG. Machine-readable model: [data/vetting-state-model.json](data/vetting-state-model.json). Computations: [scripts/reg_source_change_volumes.py](scripts/reg_source_change_volumes.py) (`bmf-diff`, `revocations`, `bmf-profile`, `review-load`). Registry design: [05-charity-registry-design.md](05-charity-registry-design.md).

## Summary

- **The policy frame is already ratified.** CNV-GRT-003 sets status checks at approval and release against the latest IRS postings, a 180-day default deep review with 30-day refresh lead time, event-triggered invalidation, and fail-safe when stale; informational changes must not block payment. RR-REQ-X-007-r2 adds automatic renewal with no human sign-off. RR-UNB-EXT-028-r2 sets a three-class MaterialityTable, and RR-UNB-GRT-003-r1 sets tiered diligence. This file supplies what those clauses leave open: measured change volumes, a field-level materiality table, evidence-expiry rules per type, retroactive-reinstatement semantics and an explicit state model. RECOMMENDATION, High.
- **Monthly source churn is large; material churn is tiny.** Between the 2026-06 and 2026-07 EO BMF snapshots, 236,750 501(c)(3) organizations changed at least one field. 189,577 (80%) changed only financial or filing fields (informational), and 46,768 changed only address or name (material-neutral). Only 405 (0.17% of changed organizations, 0.024% of all c3 organizations) changed a field that can affect eligibility, and on inspection about 90 of those were truly adverse (e.g. 35 public charities reclassified as private foundations, 25 group exits). 3,617 c3 organizations dropped out. VERIFIED-FACT (computed), High.
- **Auto-revocations arrive in one big batch a year.** About 53,000-66,000 revocations were posted per year in 2022-2026 (45,696-54,221 of them 501(c)(3)). About 70% landed in August (40,453 of 58,831 in 2025). Posting lags the effective date by a median of 89 days. VERIFIED-FACT (computed from the IRS list), High.
- **Two thirds of reinstatements are retroactive.** Of 184,830 reinstated rows, 122,787 (66%) carry a reinstatement date equal to (or before) the revocation date. 62,043 are prospective, with a median gap of 944 days. Retroactive reinstatement must reopen held grants, never rewrite what was known when they were held. The revocation list's reinstatement date alone should trigger re-checks, not releases: reliance attaches to a later Pub 78/BMF listing or a determination letter [REG-002 §4.06]. VERIFIED-FACT (counts, rule), High; RECOMMENDATION (semantics).
- **OFAC changes the SDN list on about 110-130 days a year** (114 in 2023, 132 in 2024, 114 in 2025, 112 in 2026 through 23 November). Each update must trigger an automatic delta rescreen (UNB-RCN-GRT-007). US-address additions are rare (about 6 in 2023 by heuristic parse). VERIFIED-FACT (dates), Medium (parse heuristic).
- **"Stale" must mean behind the latest publication, not old.** If the IRS has not posted since the last cycle, the last posting is still current. A wall-clock reading of CNV-GRT-003's fail-safe rule would hold every payment whenever the IRS publishes late. RECOMMENDATION, High; flagged as a clarification of a ratified clause.
- **Expected human review is small and comes mostly from renewals and onboarding, not monitoring.** Central scenario: about 2,000 human cases a year for 60,000 monitored charities and 400,000 grants. That is about 5 per 1,000 grants and about 1.6% of the 130,000 review events a conventional 180-day cycle implies (range 0.7%-4.6%). Monitoring-driven cases (revocations, adverse BMF changes, sanctions matches) are under 10% of the total. Renewal failures and new-charity onboarding dominate. INFERENCE over ASSUMPTION-heavy parameters, Low-Medium; no measured exception rate exists (research/daf-grant-exception-unit-economics-evidence-and-sensitivity-2026-11-12.md).
- **AI boundary.** AI may extract, match and propose (unstructured adverse records, central-org directories, merger documents). It never publishes or clears a hold, never moves a state on its own, and is never the only basis for an adverse outcome (CNV-AIO-001/002, RR-UNB-EXT-028-r2). Every transition in the JSON model carries a decision class.

## 1. Ratified baseline this design must keep

| Clause | What it fixes | Constraint on this design |
|---|---|---|
| CNV-GRT-003 | Approval and release checks against latest TEOS/Pub 78, BMF, auto-revocation with posting dates; legal name; subordinates flagged; deep review 180 days default, sponsor may tighten; refresh 30 days before expiry; event invalidation; cross-sponsor evidence as input only; fail safe when stale; informational changes do not block | All numbers live in FreshnessPolicy (UNB-RCN-GRT-014), not in the state model |
| RR-REQ-X-007-r1 | Per-sponsor reliance snapshot with Rev. Proc. 2018-32 §8.01 fields; an expired deep review holds **new approvals** but not release when release-time checks pass | Two separate clocks: deep review and status currency |
| RR-REQ-X-007-r2 | Passing scheduled renewal renews automatically with the policy version as approving authority; event revalidation resets the clock only if it is a full review; reuse by a second sponsor triggers no new routine vetting; stratified after-the-fact sampling | Automatic transitions are `deterministic` with `authority=policyVersion` |
| RR-UNB-EXT-028-r2 | MaterialityTable: Material-Adverse, Material-Neutral, Informational; AI proposals cannot publish or clear holds; SLAs relative to publication | Field-level table in section 3 |
| RR-UNB-GRT-003-r1 | Tiers A-D; humans only for rule-defined holds, non-standard classes and suspected fraud, deduplicated per charity | Case deduplication key = (charity, reason) |
| RR-UNB-CHAR-013-r1 | Stewardship only for unresolvable identity, outcome-changing conflicts, suspect documents, unmatched grantees; staleness case only if automated refresh fails | `NeedsEvidence` entered only after automated gathering is exhausted |
| UNB-XIN-NPG-005, CNV-GRT-010 | OrganizationChangeEffect table, including ReinstatementRetroactive and successor substitution with sponsor approval and donor notice | Section 5 |
| CNV-GRT-004 (+ OD-P-GRT cut F) | Only verified public facts propagate; R1 has no neutral flag | Shared holds only from public facts |
| CNV-GRT-005 | Discretionary holds under a board policy, 90-day maximum | Sponsor-cell state, never shared |
| CNV-GRT-006 (+ cut F) | Screening at onboarding, list update and release; human dispositions; FP reuse 12 months, within sponsor only in R1 | Sanctions machine |
| CNV-ARC-003 | Hold version checked atomically at dispatch; unknown hold state fails closed | Release transition guard |
| CA-180-01..18 | 180-day assurance decision record | Mapped in section 9 |

## 2. Measured change volumes

### 2.1 EO BMF month over month (NCCS mirror of IRS monthly files, 2026-06 to 2026-07 [REG-012])

| Measure | All subsections | 501(c)(3) |
|---|---|---|
| Rows (old, new) | 1,966,267 / 1,974,830 | |
| Added | 12,690 | 11,702 |
| Removed | 4,127 | 3,617 |
| Organizations with any field change | 285,710 | 236,750 |
| ... only informational fields | 228,813 | 189,577 (80.1%) |
| ... at most name/address (material-neutral) | 56,336 | 46,768 (19.8%) |
| ... any material-adverse-candidate field | 561 | 405 (0.17%) |

Field-level c3 counts: TAX_PERIOD 229,017; ASSET_AMT 140,197; INCOME_AMT 139,970; REVENUE_AMT 105,144; STREET 44,728; CITY 16,432; ICO 9,088; NAME 1,311; FOUNDATION 305; RULING 209; AFFILIATION 63; GROUP 55; DEDUCTIBILITY 53; SUBSECTION 42; STATUS 20. VERIFIED-FACT (computed), High for this month; one month is not a seasonal profile (Medium for annualization).

Direction matters. Of the 305 foundation-code changes: 148 were private foundation to public charity (04 to 15/16, favourable), 36 were switches between public-support tests (15/16, neutral for a DAF), 29+6 were public charity to private foundation (adverse), and a handful were supporting-organization type changes (adverse candidates under RR-UNB-EXT-028-r1). Group changes: 30 joined a group, 25 left one. A naive "any change opens a review" rule would create about 585 times more work than a direction-aware table.

### 2.2 Auto-Revocation List (file dated 2026-11-17 [REG-008]; the IRS "updates the list monthly" [REG-007])

| Year posted | All | 501(c)(3) | August share |
|---|---|---|---|
| 2023 | 60,101 | 49,845 | 70.7% |
| 2024 | 66,286 | 54,221 | 70.3% |
| 2025 | 58,831 | 50,119 | 68.8% |
| 2026 (to Nov) | 53,120 | 45,696 | 73.1% |

The other months carry 0 to 8,565 postings each. Posting lag after the effective date (2025 postings): p10 89, median 89, p90 119 days. Reinstated rows: 184,830, of which 122,787 are retroactive and 62,043 prospective. VERIFIED-FACT (computed), High.

Incidence among actual DAF grantees is far lower than in the population, because revoked organizations are mostly non-filers. Of 170,569 top-50 recipient EINs in FY2023-24, 141 were already revoked before the sponsor's fiscal year, 272 were revoked during it and 1,092 afterwards (to November 2026). That is about 0.3% of grantees a year. INFERENCE from research/mission-2026-11-14/b40n1202-b43n26-03-non-bmf-recipients.md and direction-recipient-lobbying.md, Medium.

### 2.3 OFAC SDN list

Distinct action dates in OFAC's annual "SDN Changes" publications [REG-013..017]: 2023: 114; 2024: 132; 2025: 114; 2026 to 11-23: 112. VERIFIED-FACT, Medium-High: the dates were counted by pattern match on the PDF/text, so a stray date string in an entry could inflate the count slightly. A heuristic parse of the 2023 text file found about 5,600 added entries (including vessels, aircraft and a.k.a. cross-references), of which about 6 carried a US address. VERIFIED-FACT on the source, Low on the parsed counts.

## 3. Materiality table (field- and direction-level refinement of RR-UNB-EXT-028-r2)

Decision class: **D** deterministic; **AI** AI-assisted (AI prepares, a deterministic rule or human executes); **H** human-required.

| Event (source) | Class | Effect | Decision | Measured frequency |
|---|---|---|---|---|
| Revocation posted, no reinstatement (Auto-Revocation List) | Material-Adverse | Publish shared hold; CommonVerification to Ineligible; re-evaluate impacted grants only (UNB-GEX-019) | D | ~0.3% of grantees/yr; 70% in one August batch |
| Removed from Pub 78 posting without a revocation row | Material-Adverse candidate | Suspended; hold release (CNV-GRT-003 AC-1); re-check next posting and the revocation list | D | subset of 3,617 c3 removals/month |
| Removed from BMF | Material-Adverse candidate | As above; look for a final return or successor (termination signal) | D, AI for successor documents | 3,617 c3/month |
| FOUNDATION public charity to PF, or SO type change | Material-Adverse | Ineligible for R1 recipient class (CNV-GRT-002) unless the sponsor enables the class | D | ~35/month in c3 population |
| FOUNDATION between public-support tests (15/16), or PF to public charity | Material-Neutral | Update; no hold | D | ~184/month |
| SUBSECTION leaves 501(c)(3); DEDUCTIBILITY to not deductible | Material-Adverse | Ineligible | D | ~16/month |
| GROUP exit (subordinate leaves group) | Material-Adverse candidate | Group evidence void; needs own determination or new group evidence; hold new approvals | D, H if the organization asserts independence without a letter | ~25/month |
| GROUP entry | Material-Neutral | Attach central; group evidence required | D | ~30/month |
| Central organization of a group revoked | Material-Adverse | Cascade to all subordinates in the GEN | D | rare |
| NAME change, same EIN | Material-Neutral | Update the payee legal name on unreleased instructions; no hold (UNB-XIN-NPG-005) | D | 1,311 c3/month (0.08%) |
| Address change | Material-Neutral | No hold; re-verify the destination only if the destination changed | D | ~45,000 c3/month (2.7%) |
| Financial fields, tax period, ICO, NTEE, filing codes | Informational | Evidence update; no hold, case or task (CNV-GRT-003 AC-3) | D | ~190,000 c3/month |
| Third missed annual filing becoming due (990-N/990 history) | Informational (early warning) | Proactively ask the charity to file before revocation; never a hold | D | derivable from the e-file index; not measured here |
| Final return or termination report | Material-Adverse candidate | Suspended; open succession check | AI (document extraction), H (successor designation) | 884 top-50 grantee EINs filed final returns (2023-24 cohort) |
| Merger, successor designated | Material-Adverse | Hold; sponsor approval of payee substitution plus donor notice (CNV-GRT-010) | H | rare |
| SDN list update | Trigger | Delta rescreen of all unreleased chains and outstanding checks | D; H for potential matches | ~120 update days/yr |
| Court judgment, AG action, news (unstructured) | Evidence only at platform level | AI may propose a match to the sponsor's DiscretionaryGrantPolicy criteria; the sponsor decides (CNV-GRT-005) | AI then H | not measured |
| Destination change, return code, rail enrolment change | Payment-material | L11 control (CNV-PAY-002); never an identity or eligibility change | D, H for destination exceptions | out of scope here |

## 4. Evidence types and expiry

Validity rules are proposed FreshnessPolicy entries (UNB-RCN-GRT-014); numbers are policy, not law, unless marked.

| Evidence type | Validity rule | On expiry or invalidation | Shared? |
|---|---|---|---|
| IRS status observation (Pub 78, BMF, Auto-Revocation List) | **Current while it is the latest published version**; retrieval target 24 h after publication (CNV-GRT-003). If the source misses its expected cadence by more than a grace period, raise a source-silence alert, **not** a hold | If a newer version is published but not ingested: Stale, release fails safe | Yes (SS-REG-01) |
| Deep review result | 180 days default (sponsor may shorten); renewal starts 30 days before expiry, with jitter | Expired: new approvals held; release still allowed on current release-time checks (RR-REQ-X-007-r1) | Yes (common verification); sponsor overlay private |
| Group subordinate inclusion (central listing or letter) | 12 months, aligned to the central's annual update duty [REG-001] (ASSUMPTION); void on GROUP exit or central revocation | Automated request to the central first; human only if the central does not answer before expiry | Yes, per GEN |
| Church / government unit evidence (entity-type matrix, UNB-RCN-GRT-013) | Until the next deep review; void on contradicting T1 data | Automated re-attestation request | Yes if public evidence; private uploads stay in the charity cell |
| Fiscal sponsor project list or attestation (CNV-GRT-008) | 12 months (ASSUMPTION); void if the sponsor drops the project or loses status | Request a fresh attestation | Public list yes; signed attestation in the charity cell |
| Determination letter for a new organization not yet listed | Until the organization appears in the BMF/Pub 78 posting; reliance provisions do not apply before listing [REG-002 §6.02] | VerifiedWithConditions; sponsor policy decides acceptance | Yes |
| Sanctions screening result | Valid only for the list version screened; release needs the current version | Rescreen | No (sponsor cell) |
| Sanctions false-positive disposition | 12 months, voided by subject or entry change (CNV-GRT-006); R1 within the deciding sponsor only | New review | No |
| Destination verification (CNV-PAY-002) | No time expiry; voided by bank change, account-validation return, rail enrolment change or contact-channel change hold | L11 re-verification | No |
| Authorized representative | 12 months re-confirmation (ASSUMPTION) or on role/contact change (CNV-PLT-011 72 h hold) | Representative actions suspended; charity status unaffected | Charity cell |
| Form 990 filings and financials | Informational; never expire eligibility | n/a | Yes |
| State registration | Deferred (SPD-GRT-005) | n/a | n/a |

## 5. Revocation, reinstatement and reliance semantics

Let E be the revocation effective date (valid time), P the posting date, K the time Unbound records the fact, R the reinstatement effective date and L the date of the next Pub 78/BMF listing or determination letter.

| Grant timing | Outcome | Basis |
|---|---|---|
| Approved and released before P, Unbound unaware | Valid; no remediation; history unchanged | Rev. Proc. 2018-32 §4.02 [REG-002] |
| Released between K and P where Unbound already had the adverse fact (e.g. a final return) | Not protected: the knowledge exception may apply | §4.04 [REG-002]. Shared public facts must therefore reach every sponsor quickly (CNV-GRT-004) |
| Approved before P, release after P | Held at release (EligibilityChanged) | CNV-GRT-003 AC-1 |
| Recurring occurrence due after P | Held for the sponsor's hold window, then Skipped; not re-created later | unbound requirements/grants/END-TO-END-GRANT-LIFECYCLE-AND-OPERATING-MODEL.md:240 (AC-2) |
| Retroactive reinstatement (R = E) observed on the revocation list | Trigger an immediate re-check; held grants become releasable **when L exists** (listing posted after P, or a determination letter effective on or before the grant date), and all other checks pass | §4.06 [REG-002]; retroactive reinstatement procedures [REG-003]; UNB-XIN-NPG-005 ReinstatementRetroactive |
| Prospective reinstatement (R > E) | Grants dated in [E, R) stay refused; ask the donor to re-recommend; grants dated after R follow normal rules | UNB-XIN-NPG-005 |
| Held grant whose hold window expired before reinstatement | Stays Skipped/Cancelled; no automatic recreation | same file :195, :240 |

Recording rule (KNOW-T05): a retroactive reinstatement adds a valid-time correction (exempt throughout) while the recorded-time history keeps that, at decision time, the organization was revoked. Holds placed then were correct decisions on the facts known; they are not re-labelled as errors. Metrics count them as "correct hold, later lifted", not false positives.

Why not release on the revocation list's reinstatement column alone: §4.06 names a subsequent Pub 78/BMF listing or a determination letter as the reliance basis, not the list. In the current files, 19,695 Pub 78 EINs still show an unreinstated revocation row, so the list is an imperfect signal. INFERENCE, Medium; counsel question in 05.

## 6. State model

Full definitions are in [data/vetting-state-model.json](data/vetting-state-model.json): 6 machines and 63 transitions (49 deterministic, 2 AI-assisted, 12 human-required), each with trigger, guards, effects, decision class, AI role and the requirement IDs it refines. AI also prepares dossiers inside several human-required transitions; that role is recorded in `ai_role`. Summary:

| Machine | Scope (store) | States |
|---|---|---|
| CommonVerification | Shared (SS-REG-03/04) | NotAssessed, Gathering, Verified, VerifiedWithConditions, RenewalDue, NeedsEvidence, Suspended, Ineligible, Expired, Superseded |
| SponsorEligibility | Sponsor cell | NotEvaluated, Eligible, EligibleWithConditions, NeedsReview, InsufficientEvidence, Ineligible, DiscretionaryHold, Excluded |
| GrantCheck (approval and release) | Sponsor cell | Pending, Passed, Held, Refused, Released, Cancelled |
| RecurringOccurrence | Sponsor cell | Scheduled, Checked, HeldInWindow, Released, Skipped |
| SanctionsScreening | Sponsor cell | Unscreened, Clear, PotentialMatch, FalsePositive, TrueMatch, Blocked, Rejected, ProceedLicensed |
| EvidenceItem | Owning store | Observed, Quarantined, Current, Expiring, Expired, Superseded, Disputed, Withdrawn |

Invariants enforced across machines:

1. Only `deterministic` transitions run without a named human. Their authority is the policy version (RR-REQ-X-007-r2).
2. No AI output is a trigger by itself. AI outputs are `proposal` artifacts that a deterministic guard or a human must accept.
3. A shared state can only become more restrictive from public facts. Sponsor-private information never moves CommonVerification.
4. Release requires current hold version, current status publication, current sanctions list version and verified destination, checked atomically at dispatch (CNV-ARC-003).
5. Any unknown (hold registry unreachable, status not ingested after publication) fails closed for release and never produces Ineligible.

## 7. Specific situations

**Pending and recurring grants.** An impact index inside each sponsor cell maps charity ID to open approvals, unreleased instructions and schedules. A shared hold publication or state change fans out only to the matching items (UNB-GEX-019), deduplicated into one case per charity and reason (UNB-GEX-021).

**Sponsor-specific policy.** Sponsor overlays can shorten validity windows, exclude classes, require extra evidence or add discretionary criteria. They can never loosen platform floors (UNB-RCN-GRT-014 AC-2). A change to the overlay re-evaluates SponsorEligibility for that sponsor only. CNV-GOV-005 governs adoption; in release 1 it is one versioned configuration per sponsor (OD-P-GOV cut I).

**Shared verification evidence.** One CommonVerification serves every sponsor. Each sponsor writes its own reliance snapshot (RR-REQ-X-007-r1). A second sponsor's first grant to a charity costs one overlay evaluation, not a review (RR-REQ-X-007-r2(4)).

**False positives.**
- Sanctions: CNV-GRT-006 reuse rules.
- Identity: a wrong merge is reversed by unmerge with dual control (UNB-KNOW-020). Grants stay bound to the identity they were bound to.
- Materiality: every Suspended state that clears without adverse confirmation is counted as a materiality false positive. Its rate per rule is a KPI, and rules that exceed a threshold are revised through the governed policy change, not by ad hoc overrides.

**Stale and unavailable sources.** States: `current` (latest publication ingested); `late-publication` (source past expected cadence: alert only); `ingest-failed` (a publication exists but is not ingested: release fails safe, approvals may continue only on evidence still current); `quarantined` (schema drift or implausible delta, UNB-KNOW-026: treated as ingest-failed). Implausibility test: a monthly delta far outside the historical range, e.g. a 40,000-row revocation posting outside August, routes to quarantine review before propagation.

**Conflicting authoritative records.** Resolve deterministically by publication order where the reliance rule supplies it: a Pub 78/BMF listing posted after a revocation posting may be relied on (§4.05-4.06). Equal-date T1 conflicts (e.g. BMF still lists an organization that the same cycle's Pub 78 dropped) give Suspended and a next-cycle re-check. A case opens only if two cycles disagree and a grant is affected (RR-UNB-CHAR-013-r1).

## 8. Expected human-review rates

Model: `review-load` in the script; parameters carry evidence classes. Base: 60,000 monitored charities and 400,000 grants a year, from the 100,000-account inventory in unbound requirements/discovery/2026-11-24-simplification-economics/04-MINIMUM-TOUCH-OPERATING-MODEL.md (SPW-049..051, ASSUMPTION there).

| Source of human cases per year | Low | Central | High | Main parameter (class) |
|---|---|---|---|---|
| Revocations needing judgment (successor, name variance) | 0 | 9 | 45 | 0.2-0.5% grantees/yr revoked (INFERENCE) x 0-15% needing judgment (ASSUMPTION) |
| Adverse BMF field changes | 4 | 12 | 105 | measured 0.0054-0.024%/month (VERIFIED-FACT) x 10-60% judgment (ASSUMPTION) |
| Sanctions potential matches | 30 | 120 | 600 | 0.05-1% per charity-year (ASSUMPTION: no public false-positive rate) |
| New charities not resolvable by matrix | 200 | 500 | 1,000 | 2-10% of 10,000 new/yr (ASSUMPTION anchored on the 7.4% core exception proxy, of which recent rulings are deterministic) |
| Renewal failures after automated gathering | 600 | 1,200 | 3,600 | 0.5-3% of 120,000 renewals (ASSUMPTION) |
| Identity disputes and corrections | 60 | 180 | 600 | 0.1-1% per charity-year (ASSUMPTION; SPW-058 used 300) |
| **Total** | **894** | **2,021** | **5,950** | |
| Per 1,000 grants | 2.2 | 5.1 | 14.9 | |
| Share of a conventional cycle (130,000 reviews/yr) | 0.7% | 1.6% | 4.6% | |

Reading (INFERENCE):
- Monitoring adds few human cases at any plausible rate. Capacity planning should focus on one predictable August revocation batch and about 120 sanctions rescreen days, all automated.
- **Renewal-failure rate is the controlling parameter.** Engineering effort belongs in automated evidence gathering for renewals (central-org listings, church attestations, determination letters), not in better monitoring.
- These are cases, not hours. At 25 minutes a case the central scenario is about 840 reviewer hours a year, inside the 7,350 hour minimum-touch residual in the unbound inventory, which is dominated by legally human equivalency and expenditure-responsibility work disabled in release 1.
- The figures do not cover grant-level exceptions (donor benefit, purpose, payments), which the 90-day study in the exception unit-economics file must measure.

## 9. Decision classes

| Deterministic (no human) | AI-assisted (AI proposes, rule or human executes) | Human-required |
|---|---|---|
| Status currency checks; posting-order conflict rules; materiality classification of structured fields; automatic renewal; hold publication from public facts; impact fan-out; release fencing; informational updates; name/address effects; sanctions delta rescreen; FP disposition reuse within its validity; expiry and refresh scheduling; donor-facing neutral codes (XID-CLM-003) | Extracting determination letters, central-org subordinate directories, final returns, merger documents; proposing duplicate candidates; matching unstructured adverse records to sponsor DiscretionaryGrantPolicy criteria; drafting the dossier narrative (CNV-AIO-002) | Identity merge/unmerge; successor designation and payee substitution (CNV-GRT-010); sanctions potential-match disposition, block/reject/proceed (CNV-GRT-006); discretionary holds (CNV-GRT-005); non-standard recipient classes; suspected fraud; disputes by a charity; overrides within lawful bounds with expiry (UNB-CHAR-023); policy changes (CNV-GOV-005) |

AI never overrides a deterministic prohibition, never grants itself authority, and AI unavailability never stops deterministic paths (CNV-AIO-001).

CA-180 mapping: 01/02/06/08/18 map to CommonVerification renewal transitions; 03/04 to 05; 05/12 to section 3; 07 to GrantCheck; 09 to NeedsEvidence entry guards; 10 to SponsorEligibility; 11 to L11; 13 to section 7 (stale); 14 to decision records; 15/16 to KPIs below; 17 to sponsor overlays.

KPIs (refining RR-REQ-X-007-r2(6), CA-180-16), each with an explicit denominator: renewal success rate; human cases per 1,000 grants by reason code; materiality false-positive rate per rule; time from source publication to hold (p50/p95); evidence reuse ratio; correct-hold-later-lifted count (reinstatements), kept separate from false holds.

## Implications for Unbound

1. The 180-day window can be kept at its maximum with near-zero routine human touch, because the material event rate among real grantees is very low. The cost driver is evidence that expires and cannot be refreshed automatically.
2. Encode direction-aware materiality. Field-level "changed" flags would bury reviewers.
3. Define "stale" as behind the latest publication, in the FreshnessPolicy schema, before any rail partner integration builds on it.
4. Implement reinstatement as re-check, not release, until a qualifying listing or letter exists.
5. Plan an annual August surge test: about 40,000-47,000 revocation rows in one posting, delta-applied and fanned out within the detection SLA.

## Open questions / evidence gaps

- Real renewal-failure and new-charity human shares: only a pilot can measure them (RR-UNB-GRT-003-r1#Q1, 90-day study).
- Sanctions potential-match rate for charity names with EIN/country-aware matching: no public data.
- One month of BMF diffs is not a seasonal profile. Run `bmf-diff` across the 37 NCCS monthly files to get annual distributions.
- Counsel: the §4.06 "subsequent listing" reading (05); whether the Auto-Revocation List reinstatement column can itself support release.
- Expected IRS posting cadence and grace period for the source-silence alert (the October 2025 posting carried only 64 rows; it is unclear whether that was a short cycle or a late one).
- Clarify CNV-GRT-003 "fail safe when stale" (currency vs age), and whether CNV-GRT-004's "published judgments" produce platform holds or only shared evidence for sponsor discretionary policies (CNV-GRT-005). Both are flagged for owner resolution.

## Candidate requirements (proposed; refine existing IDs)

| ID (proposed) | Requirement | Refines |
|---|---|---|
| REG-P-12 | FreshnessPolicy SHALL define currency against the latest publication of each source, with a separate source-silence alert that never holds by itself | UNB-RCN-GRT-014, CNV-GRT-003, RR-UNB-EXT-028-r2 |
| REG-P-13 | The MaterialityTable SHALL classify by field and direction of change (e.g. foundation code 15 to 16 neutral, 15 to 04 adverse) | RR-UNB-EXT-028-r2 |
| REG-P-14 | A revocation-list reinstatement SHALL trigger re-checks; held grants release only on a later Pub 78/BMF listing or a determination letter covering the grant date | UNB-XIN-NPG-005, CHAR-T14, KNOW-T05 |
| REG-P-15 | Holds lifted after retroactive reinstatement SHALL be recorded as correct-then-lifted, not as false holds | RR-REQ-X-007-r2(6), CA-180-16 |
| REG-P-16 | Each evidence type SHALL declare its validity and invalidation events (section 4) in the FreshnessPolicy | UNB-RCN-GRT-014, CA-180-01 |
| REG-P-17 | Monthly deltas outside a source's historical range SHALL be quarantined before propagation | UNB-KNOW-026, UNB-EXT-032 |
| REG-P-18 | Missed-filing history SHALL produce an informational early-warning request to the charity, never a hold | UNB-EXT-028 |
| REG-P-19 | Human-review KPIs SHALL be reported per reason code per 1,000 grants, with renewal-failure rate as a release-gate metric for straight-through vetting | RR-REQ-X-007-r2, CA-180-16 |
