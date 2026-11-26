# 11 - Continuous charity intelligence

Status: research (2026-11-26). Track I. Agent HI. Builds on Phase II [02](../competitive-displacement/02-charity-intelligence-sources.md), [03](../competitive-displacement/03-charity-data-licensing-and-access.md), [04](../competitive-displacement/04-charity-intelligence-architecture.md), [05](../competitive-displacement/05-charity-registry-economics.md), the registry model (`model/src/CompetitiveDisplacement/Registry.fs`, [registry-components.csv](../competitive-displacement/data/model-inputs/registry-components.csv), [registry-parameters.csv](../competitive-displacement/data/model-inputs/registry-parameters.csv)), the source register [charity-data-sources.csv](../competitive-displacement/data/registers/charity-data-sources.csv) (68 sources), and the charity-network package ([06](../competitive-advantage/charity-network-and-onboarding/06-continuous-vetting.md)). Unbound inputs (cited by path, not linked): `requirements/grants/END-TO-END-GRANT-LIFECYCLE-AND-OPERATING-MODEL.md` (CNV-GRT-003), `requirements/discovery/2026-11-26-charity-network-and-onboarding/02-REQUIREMENTS.md` (UNB-CNET-001..026), `architecture/CHARITY-KNOWLEDGE-MODEL-AND-ACQUISITION-PIPELINE.md`, `requirements/convergence/2026-11-24-master/14-PUBLIC-DATA-REPLAY.md`. Cost components for the model agent: `data/fragments/HI/model-registry-components.csv`. Licence readings are research findings, not legal advice (Phase II OQ-007/008).

## Answer in brief

1. **Every eligibility-relevant federal source can be monitored automatically**, but the IRS files, the auto-revocation list and the SAM exclusions extract are **full snapshots that must be diffed** (the IRS overwrites history), OFAC offers public delta files but a full reload is safer (UNB-CNET-009), the trade.gov CSL is a daily full file, and the 990 XML series is the only naturally incremental federal source. State charity registries are the weak point: no national dataset, California is a per-organisation lookup, New York is FOIL (P3-CLM-HI009, P3-CLM-HI010).
2. **Only adverse changes to eligibility fields invalidate eligibility evidence** (status, subsection, foundation code, deductibility, revocation, group exit, sanctions hit). Name, address and financial changes never do. Mergers, dissolutions with successors, fiscal-sponsorship relationships, impersonation and unresolved identifier conflicts need a person; the rest resolve deterministically (section 3).
3. **The binding detection latency is IRS posting lag (median 89 days for revocations), not the review cycle.** A 180-day periodic review adds nothing for facts the release-time check already sees; it matters only for non-monitorable evidence (P3-CLM-HI011).
4. **Who bears the deep review decides the cost (Revision 3, P3-DEC-MOD005).** Under licensing (DEC-006) the deep review can be performed by the sponsor in Unbound. The ~$768k M1 cost at 20k charities is then sponsor labour, not Echelon's cost. If Echelon performs it on demand, the vendor addition is about $469k a year at 20k charities for one sponsor (`key-figures.md`). Earlier text, kept as history: **Governing registry run cost (Revision 2): about $768k a year at 20k charities for one sponsor** under M1, the periodic human deep review that the ratified CNV-GRT-003 wording requires until OD-CDD-02 ($215k favourable, $1.97M adverse; `registry-modes.md`). **Conditional on OD-CDD-02**, the hybrid M5 costs about $124k. **The hybrid estimate (one sponsor, monitoring within the 180-day ceiling, conditional on OD-CDD-02): about $98k a year at 5k charities and $124k at 20k charities (base), $44k all-low, $139-224k under workload stress, $330-530k if every input is at its high value simultaneously.** Phase II's $90-170k survives at the low end but its composition is wrong: workload was overstated (a 4% human-exception change rate and 833 hours of manual expiry refresh), while it omitted machine-renewal failures, tier-3 human reviews, the sample audit and ingest operations. At ≤20k charities the cost is **fixed-cost dominated** (connectors ~$35k, owner floor ~$30k, counsel ~$13.5k, ingest operations ~$8.5k) (P3-CLM-HI012).
5. **Public-intelligence maintenance is ~96% of the single-sponsor cost; sponsor-specific eligibility decisions are about $4.3k per sponsor-year (range $0.6-27k).** The **marginal cost of an added sponsor is about $3-24k a year (base)**, driven by how many new charities it adds to the shared union (overlap exponent), not by its own decisions (P3-CLM-HI013).
6. **The governing mode today is M1, a human 180-day full review, at ~$768k at 20k charities** (~$767k in this report's own arithmetic; $768k in model revision 2). Under licensing that cost is not Echelon's if the sponsor performs the review (P3-DEC-MOD005). An Echelon-performed, demand-driven review adds about $469k a year for one sponsor at 20k charities (revision 3). **A hybrid of continuous monitoring, evidence expiry, automated 180-day renewal, risk-tiered human review and a statistical sample audit costs ~$124k, conditional on OD-CDD-02.** It stays inside the DEC-003 180-day ceiling **only if** automated renewal is allowed to count as the deep review. Continuous monitoring alone does not meet the ceiling (section 5).
   - **Revision 2 (P3-CHL-REV3010, P3-CHL-REV3020).** This item previously said the hybrid "stays inside DEC-003 / CNV-GRT-003". That overstated the position. UNB-CDD-CIV-008 retains the deep review at the CNV-GRT-003 interval under the ratified wording until the owner decides OD-CDD-02. The owner has not authorized removal of a mandatory control (BRIEF). M5 (~$124k) is therefore **conditional** on OD-CDD-02, SPD-GRT-001, V-3 and V-9. Until those are met, the compliance-bound base is M1 (~$767k at 20k charities). Model revision 2 adopts M1 as the governing mode (P3-ASM-MOD049) and shows M5 as conditional ([16](16-capital-efficient-market-entry.md)).
7. **A sample audit of 149 verifications per stratum a year (zero-acceptance, 95% confidence, 2% tolerable rate) costs about $7.6k for three strata.** It detects systematic blind spots of 2% or more; it cannot demonstrate rates below 0.1% (2,995 samples), so rare-event safety must come from deterministic release-time controls (P3-CLM-HI014).
8. **Charity intelligence is not, on current evidence, an independent commercial asset.** The relevant comparator is Candid's **Charity Check API**, from $2,750 a year. Candid describes it as helping users "ensure the nonprofits you support are IRS and state compliant", and it offers "time-stamped documentation for auditing records" (accessed 2026-11-26). Phase II's V-8 gate (≥3 of 10 prospects at ≥$15k) sits at about 5.5× that list price, and a standalone service adds ~$197k of overhead (RA-6). It is a cost advantage inside Unbound and a possible low-price partner add-on (P3-CLM-HI015, P3-DEC-HI003).
   - **Revision 2 (P3-CHL-REV3013).** This item previously cited Candid's "Nonprofit Eligibility API ... 'real-time eligibility updates' from $5,000" as a DAF eligibility comparator. That was a misreading. Candid describes that API as "For donation platforms to enable Apple Pay" (mobile-payment eligibility). It is not a DAF eligibility monitor, and the "1.5-5.5×" range relied on it. State compliance coverage and time-stamped audit evidence are therefore **not** differentiators for Unbound: Charity Check already claims both.

## 1. Sources: monitoring, refresh, cadence, licence, sharing

Verified 2026-11-26 where marked; other rows rely on Phase II's register (SRC-001, SRC-064).

| Source | Automatic monitoring | Incremental or full refresh | Cadence (evidence) | Licence / redistribution | Shared or segregated | Eligibility role |
|---|---|---|---|---|---|---|
| IRS EO BMF | Yes | **Full snapshot, diff by EIN** (no deltas, no history; replay-grade history for Unbound starts on the date its own archive starts, and earlier NCCS archive files are irregular, so replay before that is of uncertain completeness, Revision 2, P3-CHL-REV3017) | Data posting 11/10/2026; page reviewed 2026-11-16 (P3-SRC-HI001); monthly in practice | US government work (17 USC 105) | Shared | Status, subsection, foundation code, GEN, deductibility |
| Pub 78 data (TEOS) | Yes | Full file, diff | "The data set files are updated monthly"; last update Nov 11, 2026 (P3-SRC-HI002) | Public domain | Shared | Reliance list (Rev. Proc. 2018-32) |
| Auto-revocation list | Yes | Full cumulative file, diff; reinstatement columns | Monthly; Nov 11, 2026; ~70% of postings in an August batch | Public domain | Shared | Revocation, reinstatement |
| Form 990-N | Yes | Full file | Latest posting Nov 9, 2026 (TEOS page says monthly; Phase II found weekly per Pub 5891: unresolved, P3-GAP-HI006) | Public domain | Shared | Filing presence (early warning) |
| Form 990 e-file XML | Yes | **Incremental by batch** (index plus monthly batches) | Latest XML posting Oct 21, 2026; ~month-long outage Nov 2025 (Phase II) | Public domain | Shared | Final return, Schedule N (merger/dissolution), financials (informational) |
| IRS 501(p), for-cause revocations (IRB) | Partly (ad hoc pages) | Full page check | Ad hoc | Public domain | Shared | Suspension, revocation |
| OFAC SDN and consolidated lists | Yes | Delta files are public (FAQ 90); full reload on any digest change recommended (UNB-CNET-009) | No schedule; 112-132 action dates a year; OFAC leaves download frequency to each institution's risk assessment | Public domain | List shared; **match results sponsor-scoped** (CHL-044) | Mandatory screening |
| trade.gov Consolidated Screening List | Yes | Full daily file (CSV/TSV/JSON) and API | "Updated automatically every day at 5:00 AM" (P3-SRC-HI004); an aid only: users must check official publications | US government data | List shared; results sponsor-scoped | Screening beyond OFAC |
| UK Sanctions List (FCDO) | Yes | Full file (XML/CSV), event-driven; e-mail alerts | Last updated 26 Nov 2026; OFSI list closed 28 Jan 2026 (P3-SRC-HI005) | OGL v3 | List shared; results sponsor-scoped | Screening |
| UN, EU lists | Yes | Full file | Event-driven | Open (EU registration) | As above | Screening |
| SAM.gov exclusions | Yes | **Daily full active-set extract** (Julian-dated ZIP); API 10 requests/day on a personal key (P3-SRC-HI006) | Daily, after 7 AM ET | Public; D&B fields restricted | Exclusion facts shared only after counsel confirms the reading (Revision 2, P3-CHL-REV3018); D&B fields not | Informs (federal exclusion is not by itself DAF ineligibility) |
| Federal Audit Clearinghouse | Yes | API (free data.gov key) and CSV | Continuous; cadence not stated (P3-SRC-HI007) | Federal public data (terms to review) | Segregated until counsel confirms the terms (Revision 2, P3-CHL-REV3018; previously "Shared") | Informs (going concern, material weakness); EIN-UEI bridge |
| State AG registries | **Mostly no** | Per-organisation lookup; NY by FOIL; a few open-data portals | CA page updated 2026-11-05 shows delinquency only via the Registry Search Tool (P3-SRC-HI008) | Per state; unclear (CHL-055) | Shared only where licence permits | Sponsor discretionary policy; state registration deferred (SPD-GRT-005). **Excluded from the ~$124k.** A sponsor whose policy requires state good standing must buy it (for example Charity Check), or the registry needs a priced line for the top 5-10 states. This weakens EK006 (Revision 2, P3-CHL-REV3016) |
| State corporate status (CO, NY open data) | Yes for CO/NY | Full file | Weekly/monthly | CO public domain; NY open | Shared | Dissolution signal (no EIN; candidate links) |
| Census of Governments, NCES CCD | Yes | Full annual file | Annual / quinquennial | Public domain | Shared | **Deterministic government-unit and school-district evidence** (automates ~0.5% of rows) |
| Candid APIs | Yes (vendor) | Vendor API | Vendor-managed (Charity Check: IRS and state compliance; the "Nonprofit Eligibility API" is for Apple Pay enablement, not DAF eligibility; Revision 2) | **Licensed, no sublicensing** | **Segregated per licensing sponsor**. For each channel model, record who holds the licence. A partner's existing Candid licence may not extend to use inside the module or to each sponsor, so a duplicate-licence cost may arise (Revision 2, P3-CHL-REV3036) | Optional enrichment |
| Charity Navigator, ProPublica, GivingTuesday, OpenSanctions | Possible | Varies | Varies | Restricted, NC-ND, ODbL share-alike, NC | **Excluded from shared/resold layers** (DEC-004) | Informs only |
| Charity-provided (bank letters, rosters, attestations) | No (request/response) | Per item | Expiry-driven | Charity data, may contain PII/bank data | **Charity cell, never shared** | Evidence for a decision |

Unacceptable licensing for a shared or resold layer: ProPublica (CC BY-NC-ND), OpenSanctions without a paid licence, GivingTuesday (ODbL share-alike, if any public derivative is published), MSRB EMMA feeds, Candid and Charity Navigator content, BBB WGA, ECFA, Fiscal Sponsor Directory and the Official Catholic Directory (no licence found). These are usable only as per-sponsor licensed evidence or link-outs (UNB-CNET-011).

## 2. What is shareable and what is segregated

| Evidence | Shareable across sponsors | Why |
|---|---|---|
| Source releases, hashes, three time axes (UNB-CNET-001) | Yes | Public-domain facts |
| Normalised status timeline, materiality classification of public fields | Yes | Deterministic function of public facts |
| Common verification built from public evidence only (churches via public evidence, GEN-based subordinate rosters, Census/NCES government units) | The **source-attributed public facts** are shareable, as input to each sponsor's own rule (CNV-GRT-003). **Identity confirmations and eligibility decisions are not**: they live in the sponsor's cell (UNB-CDD-CIV-010). Rev. Proc. 2018-32 gives grantors reliance on a central organization's listing, but its §6.03 gives no comparable reliance for subordinates, so first-time human verification of a non-listed recipient is sponsor-specific work | Reuse of public facts is the main eliminator (64-72% measured). **Revision 2 (P3-CHL-REV3011):** this row previously said the common verification itself was shareable. Moving first-time human verification to the sponsor layer raises the marginal sponsor cost in §8 above $3-24k; model revision 2 scales the registry with live sponsors but does not yet move first-time verification to the sponsor layer, so this remains open |
| Identity candidate links | As candidates only | Never auto-merged (UNB-KNOW-017) |
| Sanctions match scores and dispositions | **No** | Sponsor threshold and judgement; defamation and privacy exposure (CHL-044, CHL-063) |
| Sponsor watchlists, searches, grantee portfolios | **No** | Cross-tenant inference (UNB-CNET-010) |
| Charity-provided documents, bank destinations, contacts | **No** | Charity cell (UNB-CNET-020) |
| Licensed enrichment | **No** | Licence (DEC-004) |
| Sponsor decisions, overlays, holds on discretionary grounds | **No** | Sponsor authority |

## 3. Change types: invalidation and decision class

D = deterministic; H = human; AI may prepare documents but never decides (DEC-005).

| Change | Detected from | Automatic detection | Invalidates eligibility evidence? | Decision |
|---|---|---|---|---|
| Exempt status change (subsection exit, PC→PF, deductibility) | BMF monthly diff | Yes | **Yes, adverse direction only** (~35 PC→PF and ~16 subsection/deductibility a month in the c3 universe) | D; H only where a sponsor enables a class (e.g. supporting-organisation type) |
| Revocation (auto, for cause, 501(p)) | Auto-revocation list, IRB, 501(p) page | Yes | **Yes** for grants released after posting; reliance before posting (Rev. Proc. 2018-32) | D (hold); H for successor or name variance; reinstatement releases only on subsequent listing or letter (UNB-CNET-008) |
| Removal from Pub 78 or BMF without a revocation row | Diffs | Yes | Suspends pending re-check | D |
| Group exit, central organisation revoked | BMF GROUP field; central status | Yes | **Yes** (group evidence void; cascade) | D; H if independence asserted without a letter |
| State registration change ("not in good standing", delinquency) | State AG lookups | Mostly no | Not for federal eligibility; sponsor policy may hold | H (sponsor discretionary) |
| Name change, same EIN | BMF | Yes | No (update legal name on unreleased instructions) | D |
| Address change | BMF | Yes | No; re-verify destination only if the destination changed | D |
| Merger | No structured source; BMF removal, 990 Schedule N, charity notice | Partly | **Yes** for payee substitution | H (sponsor approval and donor notice, CNV-GRT-010) |
| Dissolution | BMF removal, final-return flag (990 XML), CO/NY corporate status | Mostly | Yes (suspend) | D to suspend; H for successor |
| Fiscal sponsorship relationship | Fiscal sponsor attestation (no licensed directory) | No | Yes when the sponsor drops the project or loses status | D on the fiscal sponsor's status; H for new relationships |
| Sanctions designation | OFAC, CSL, UK, UN, EU | Yes | **Release blocked** for a potential match | Mandatory H disposition; false-positive reuse within validity (CNV-GRT-006) |
| SAM exclusion | SAM extract | Yes | No by itself | H (sponsor discretionary) |
| Financial reporting (990 figures, FAC going concern, missed filings) | 990 XML, FAC, 990-N | Yes | **Never** (informational); third missed filing is an early warning | D (no task) |
| Payment information change | Charity request | n/a | Not an eligibility change; destination evidence voided | H on exception; partner verification (CNV-PAY-002) |
| Charity impersonation (lookalike, fraudulent destination change) | Destination evidence, aged contacts, EIN binding | Partly | Destination evidence voided; eligibility unchanged | Mandatory H investigation |
| Conflicting identifiers (revoked but listed; one organisation many EINs; one EIN many units) | Cross-file reconciliation | Yes | NeedsReview (never auto-cleared) | D for counsel-approved classes (re-recognised), else H (~9,200 genuinely ambiguous EINs universe-wide, UNB-CNET-005) |

Measured scale (charity-network 06): in one monthly BMF cycle 236,750 c3 organisations changed something; 405 (0.17%) changed an eligibility-relevant field and about 90 adversely. Among grantees, revocations run at about 1.7 per 1,000 Schedule I rows a year (Unbound replay) to ~0.3% of grantees (charity-network 06).

**Replay bias (Revision 2, P3-CHL-REV3014).** The exception, reuse, first-time and revocation rates come from Schedule I grants above $5k, with a one- to two-year e-file lag. Small DAF grants to churches, PTAs and local chapters are under-represented, which biases exceptions down and reuse up. Treat the rates as bounds, not base values. Sensitivity runs should use 1.5-2× the first-time incidence and 0.5× the reuse rate. These were not run in model revision 2; its tornado varies charities in use per account instead. A sample below $5k can come only through V-4 or V-6.

### 3a. Group exemptions: Rev. Proc. 2026-8 (added in Revision 2, P3-CHL-REV3012)

Rev. Proc. 2026-8 (P3-SRC-HI013) took effect on 2026-01-20. It modifies and supersedes Rev. Proc. 80-27 on group exemption letters (GENs). Its transition period for pre-existing GENs ends on **22 January 2027** (§12.02(2)). Before then, through SGRI submissions, each central organization must:
- keep at most one group exemption letter, terminating any others (§12.02(2)(c));
- remove any subordinate it cannot show to be affiliated with it and under its general supervision or control (§12.02(2)(d));
- remove subordinates described in a different paragraph of §501(c) from the one its group application specifies (§12.02(2)(e));
- add at least one subordinate or terminate a GEN with none (§12.02(2)(b)).

**Effect on this report.** Expect a wave of GEN terminations, consolidations and subordinate removals in BMF releases around and after January 2027. Each is an adverse, eligibility-relevant change for the affected subordinates: group exit voids group evidence (§3). It also generates identity work where a subordinate moves to another GEN or applies on its own. The low tier-2 renewal-failure rate (§5), the group-exit change rate in P3-EV-HI012 ([10](10-structural-cost-elimination.md)) and the identity-dispute rate (0.3% of charities a year, §7) are steady-state assumptions that do not hold for 2027. Stress all three several-fold for the 2027 releases (P3-GAP-HI011). This is also one more reason to archive monthly BMF releases now (P3-DEC-HI004). Reliance on a central organization's listing under Rev. Proc. 2018-32 is unchanged, but a subordinate's removal ends the basis for relying on its GEN.

## 4. Detection latency

Revocations post a median 89 days after their effective date (n = 369,247; Unbound replay); the August batch posts at a uniform ~88 days. No monitoring design detects a revocation before the IRS posts it, and reliance attaches to posting. Daily or monthly monitoring therefore reaches the floor (publication + ingestion within 24 hours, CNV-GRT-003) for every monitorable fact. A periodic review adds detection only for non-monitorable evidence (church status, fiscal sponsorship, subordinate inclusion, websites), at an average latency of half the cycle (~90 days for 180-day reviews). Expiry-driven refresh of that evidence gives the same or better latency at a fraction of the cost.

## 5. Monitoring modes within the 180-day ceiling

All modes keep transaction-time status checks at approval and release (CNV-GRT-003). Base, one sponsor, 20,000 charities in use; costs include the shared layer and sponsor-specific lines (model in `data/fragments/HI/model-registry-components.csv`; formulas in §7).

| Mode | Human hours a year | Run cost (base) | 180-day ceiling met? | Notes |
|---|---|---|---|---|
| M1 Periodic full human review every 180 days | ~10,300 | **~$767k** ($215k all-low) | Yes | Phase II's $483k applied 20% auto-resolution to periodic reviews; a human review at 15 min each costs more |
| M2 Continuous monitoring only | ~330 (owner floor binds: 450) | ~$99k | **No**: deep review would expire | Not compliant alone |
| M3 Evidence expiration + automated 180-day renewal | ~500 (floor 450) | ~$102k | Yes, if automatic renewal is approved (RR-REQ-X-007-r2(1); SPD-GRT-001) | Human only on renewal or refresh failure |
| M4 Risk-tiered (M3 + human deep review of tier 3, 2% of charities) | ~700 | ~$115k | Yes | Tier 3 = conflict classes, adverse history, discretionary flags |
| **M5 Hybrid (M4 + statistical sample audit)** | **~810** | **~$124k** | Only if OD-CDD-02 lets automated renewal count as the deep review (Revision 2; previously "Yes") | Recommended design, conditional on OD-CDD-02, SPD-GRT-001, V-3 and V-9; the audit adds ~$7.6k and supplies the evidence auditors will ask for (V-9). Until those conditions are met, M1 is the compliance-bound base |

Tiers for M4/M5 (proposal, P3-XRI-HI003): tier 1, Pub 78-listed public charities with no open conflict (automated renewal); tier 2, recipients relying on non-IRS evidence (churches, government units, subordinates, fiscal-sponsor projects; evidence expiry 12 months within the 180-day deep-review clock; automated requests to the central organisation or fiscal sponsor first); tier 3, conflicts, adverse history or sponsor-flagged (human review every 180 days or sooner).

## 6. Sample-audit sizing

Purpose: detect a systematic failure of automated renewal or monitoring (a blind spot), not individual rare errors. Population per stratum per year: all auto-renewed or auto-cleared verifications.

- **Zero-acceptance (discovery) sample**: smallest n such that, if the true error rate is at least the tolerable rate p_t, at least one error is found with confidence C: **n = ⌈ln(1 − C) / ln(1 − p_t)⌉**.
- **Acceptance number c**: smallest n with **Σ_{k=0..c} C(n,k) p_t^k (1 − p_t)^{n−k} ≤ 1 − C** (binomial; hypergeometric for small populations).
- **Upper bound when zero errors are found**: **p_U = 1 − (1 − C)^{1/n}** (≈ 3/n at 95%, the rule of three).
- **Finite population**: n_f = n / (1 + (n − 1)/N).
- **False alarm (producer's risk) with c = 0**: P(≥1 error | true rate p_0) = 1 − (1 − p_0)^n. A found error therefore triggers root-cause analysis, not automatic suspension of the programme.

| Confidence | p_t | n (c = 0) | n (c = 1) | n (c = 2) | p_U if 0 found | False alarm at p_0 = 0.2% |
|---|---|---|---|---|---|---|
| 95% | 5% | 59 | 93 | 124 | 4.95% | 11% |
| 95% | 2% | **149** | 236 | 313 | 1.99% | 26% |
| 95% | 1% | 299 | 473 | 628 | 1.0% | 45% |
| 95% | 0.5% | 598 | | | | |
| 95% | 0.1% | 2,995 | | | | |
| 90% | 2% | 114 | | | | |

Finite-population effect is small above ~5,000 items (149 → 145 at N = 5,000; 130 at N = 1,000). Recommended default (P3-DEC-HI002): three strata (tier-1 automated renewals; tier-2 expiry refreshes; monitoring "no change" clears), 149 each a year at 15 minutes per full review: ~112 hours, ~$7.6k. A sponsor whose auditor wants sponsor-specific assurance adds its own 59-149 sample (~$1-6k). Stratification should over-sample tier 2 (higher error propensity); sequential designs (Wald SPRT) can lower expected sample size but complicate auditor review. These are standard attribute-sampling results; acceptance by the sponsor's auditor is untested (V-9).

## 7. Challenging the $90-170k registry run cost, component by component

Phase II RA-1 at 20,000 charities, one sponsor: $162k. Decomposed from `Registry.fs`:

| Phase II line | Phase II | Challenge | Revised base (range) |
|---|---|---|---|
| Storage, compute (RC-01/02/04) | $4.3k, scaled by in-use charities | Universe-wide monitoring (UNB-CNET-010) means the shared layer ingests the full universe (~1 GB a monthly cycle) whatever the sponsor uses; immaterial either way | $7.5k incl. DB share ($4-20k), fixed |
| DB share (RC-03) | $3.1k | Kept (inside the line above) | — |
| Connectors (RC-06) 8 × 40 h | $37.8k | The minimal eligibility set is ~10 connectors (BMF, Pub 78, revocation, 990-N, 990 XML, OFAC, CSL, UK, SAM, FAC); 40 h/connector-year is unevidenced but drift is real (UK list replacement Jan 2026; OFAC retired PIP/DEL/SDALL formats; IRS 990 bulk outage Nov 2025). Federal fixed-layout files suggest ~30 h | **$35.4k** (10 × 30 h × $118; $16-99k) |
| (not modelled) Ingest operations | — | Quarantine reviews, failed runs, source silence alerts | **$8.5k** (24 × 3 h; $2-40k) |
| Counsel (RC-09) 30 h | $13.5k | Kept: materiality and reliance rule refresh | **$13.5k** ($6-48k) |
| Stewardship (RC-07): 1,532 h | $103.7k | Decomposed below | **$54.7k** (808 h) |
| — change exceptions: 800 × 0.8 × 45 min | 480 h | 4% a year is not the measured rate: material changes are ~0.3% a year universe-wide, revocations 0.17-0.3% of grantees, and most adverse changes resolve deterministically. Human monitoring cases ~0.05% of charities a year | **8 h** (1-50) |
| — new-charity exceptions: 320 × 0.8 × 45 min | 192 h | Replay measures first-time incidence at 3.1-4.0% of recipients a year (higher count) at "verify once" effort (25 min, charity-network 06) | **292 h** (0.035 × 25 min) |
| — evidence expiry: 10,000 × 5 min | **833 h** | Contradicted by the evidence rules: IRS status is current while it is the latest release; destination verification has no time expiry; renewals are automated (RR-REQ-X-007-r2). Human time arises only when automated renewal fails (0.5-3%) | **167 h** renewal failures (2 × 1% × 25 min) |
| — name-match alerts | 27 h | Moved to sponsor-specific lines (results are sponsor-scoped) | sponsor line |
| (not modelled) tier-3 human reviews | — | 2% of charities reviewed by a person every 180 days | **200 h** |
| (not modelled) sample audit | — | §6 | **112 h** |
| (not modelled) identity disputes | — | 0.3% of charities a year at 30 min | **30 h** |
| Owner floor 0.25 FTE (450 h) | binds at 5k | Kept; 0.15 FTE possible if the owner also holds other compliance duties on shared Echelon operations | $30.5k ($15-74k) |
| Sponsor-specific: policy 20 h, sanctions alerts, review cases on pending grants, sponsor audit sample | (policy only in RA-4) | Explicit per-sponsor lines | **$4.3k** per sponsor ($0.6-27k) |
| Support desk, TPSP audit, licence (RC-08, RC-10, RP-12) | $0 in RA-1 | Kept at zero in the registry: no charity portal (UNB-CNET-019); licensed enrichment is optional (+$0-9.9k per sponsor). The TPSP audit is not a contingency. Unbound is a TPSP under ratified CNV-PAY-001, and the annual Nacha Rules compliance audit is a **base obligation of the platform's** recurring compliance line ([02](02-existing-unbound-economics.md) §2), not of the registry (Revision 2, P3-CHL-REV3019; previously "TPSP audit belongs to the payments platform (CHL-037)") | $0 in the registry |
| **Total (M5 hybrid)** | **$162k** | | **$124k** ($44k all-low; $224k workload stress; $526k all-high) |

At 5,000 charities: **$98k** base (owner floor binds; Phase II $89k), stress $139k. At 50,000: $198k (Phase II $321k). One-at-a-time sensitivity at 20k charities: connector hours ($112-159k), renewal failure rate ($118-146k), tier-3 share ($117-144k), compliance rate ($112-136k), first-time minutes ($116-140k). Across sponsors the overlap exponent dominates (at 10 sponsors: $210k at 0.3 to $413k at 0.8).

**Revised range: about $95-125k a year base for one sponsor with 5k-20k charities; $45-225k across low and stress cases.** It remains a marginal cost on a platform that carries SOC 2, security and insurance (Phase II CHL-030).

## 8. Public-intelligence maintenance versus sponsor-specific decisions; marginal sponsor

| Layer | Contents | Scales with | Base at 20k, 1 sponsor | At 20k × 10 sponsors |
|---|---|---|---|---|
| Public-intelligence maintenance (shared) | Infra, connectors, ingest operations, counsel, owner floor, first-time verification from public evidence, renewal failures, monitoring cases, identity disputes, tier-3 reviews, sample audit | Universe (fixed), connectors, union of charities in use | $119.6k (96%) | $221k (union 63k charities at exponent 0.5) |
| Sponsor-specific eligibility decisions (segregated) | Policy overlay, sanctions dispositions, review cases on pending grants, sponsor audit sample, licensed enrichment | Sponsor count and its own charities | $4.3k | $43k |
| Total / average per sponsor | | | $124k | $265k / **$26k** (Phase II $18-42k) |

**Marginal cost of one more sponsor (base, M5):** $24k going from 1 to 2 sponsors with 20k charities each (the second sponsor adds ~8,300 new charities to the union at exponent 0.5); $11.6k from 10 to 11; $8.6k from 30 to 31. For 5k-charity sponsors: $2.8k, $4.7k, $3.9k. All-low $0.6-1.5k; all-high $50-220k (exponent 0.8 makes the union nearly additive). **Drivers**: overlap exponent (untested, CHL-032), first-time verification rate and minutes, renewal failure rate, sanctions alert rate, and whether the sponsor licenses enrichment.

## 9. Can charity intelligence be an independent commercial asset?

Evidence:
- **Incumbent prices (accessed 2026-11-26, P3-SRC-HI003)**: Candid Charity Check API from $2,750 ("ensure the nonprofits you support are IRS and state compliant"; "time-stamped documentation for auditing records"); Essentials API $4,800; Premier API $9,900; News API $3,300. Candid therefore already sells IRS and state compliance checks with audit documentation at list prices well under Phase II's V-8 threshold. **Revision 2 (P3-CHL-REV3013):** this bullet previously listed the "Nonprofit Eligibility API from $5,000 ('Receive real-time eligibility updates')" as an eligibility-monitoring comparator. Candid describes that API as "For donation platforms to enable Apple Pay", so it is not a comparator for DAF eligibility.
- **Free alternatives**: Treasury Do Not Pay monitors Pub 78 for federal agencies; Pactman has a free tier; the underlying IRS, OFAC and CSL data are free (Phase II 02 §6; CHL-051).
- **Buyers who built their own**: PayPal Giving Fund, Chariot, Benevity (Phase II 02).
- **Phase II V-8** (≥3 of 10 prospects at ≥$15k a year) has not been run; HYP-007 remains hypothesised.
- **Cost to stand alone**: Phase II RA-6 adds ~$197k a year (SOC 2 share, 0.5 sales FTE, on-call, support, rider). With the revised public layer (~$80-120k) a standalone service needs roughly $280-320k of revenue: 30-60 customers at $5-10k, competing with Candid at list.
- **Redistribution**: only the public-domain layer can be sold or shared (DEC-004), which is exactly what is free or cheap elsewhere; the differentiated content (charity-supplied, analytical) is licence-restricted.

What could differ: bitemporal reliance evidence (publication-time replay of what a grantor could rely on, UNB-CNET-001), the materiality table that suppresses ~99.8% of changes, verified government-unit and subordinate evidence, and a measured sanctions-matcher acceptance harness. These are audit-grade features; whether anyone pays separately for them is untested. Candid's Charity Check already advertises time-stamped documentation for auditing and state compliance, so neither counts as a differentiator. Only publication-time replay and the materiality table remain candidates, and replay-grade history starts only when Unbound's own archive starts.

**Conclusion (P3-CLM-HI015; INFERENCE, Medium):** not an independent commercial asset on present evidence. It is a cost advantage inside Unbound (shared reuse lowers the marginal sponsor cost to ~$3-24k) and could be offered as a low-price add-on through partners. Publishing the public-domain layer openly (UNB-CNET-024, gated) is a credibility option with liability limits (only source-attributed facts; CHL-044). Revisit if a $0 desk test of buyer categories and a later V-8 show willingness to pay above ~$10k.

## 10. Gaps and cheap tests

- Eligibility-relevant change rate among in-use charities over 12 releases (HYP-006 says 4%; evidence here says ~0.3-0.5% human-relevant): **start archiving monthly IRS releases now** at zero cost, because the IRS overwrites history (P3-VAL-HI001, P3-DEC-HI004).
- Automated renewal failure rate for tier-2 evidence (central rosters, attestations) (P3-GAP-HI004).
- Connector maintenance hours: desk reconstruction of format and schema changes for the ten federal sources over three years (P3-VAL-HI004).
- Overlap exponent: replay of Schedule I recipient overlap across the 20 sponsors already parsed (P3-VAL-HI002).
- Auditor acceptance of machine renewal plus sample audit (V-9; P3-GAP-HI003).
- California and other state delinquency data: whether any bulk list exists (Phase II recorded a CA "may not operate" list; today's CA page shows lookup only) (P3-GAP-HI005).
