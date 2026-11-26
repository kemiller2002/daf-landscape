# 07 - Architectural competitive advantages

Status: research (2026-11-26). Track E. Public sources only; web pages accessed 2026-11-26. Register fragments: [competitive-advantages.csv](data/fragments/EK/competitive-advantages.csv) (P3-ADV-EK001..022), [competitors.csv](data/fragments/EK/competitors.csv), [claims.csv](data/fragments/EK/claims.csv), [sources.csv](data/fragments/EK/sources.csv), [hypotheses.csv](data/fragments/EK/hypotheses.csv), [evidence-gaps.csv](data/fragments/EK/evidence-gaps.csv), [decisions.csv](data/fragments/EK/decisions.csv). Builds on Phase II [13](../competitive-displacement/13-compounding-competitive-advantages.md) (ADV-001..014) and [06](../competitive-displacement/06-competitive-displacement.md); incumbent responses are in [13](13-incumbent-response-model.md).

**Absence rule.** A capability missing from a vendor's public pages is recorded as UNKNOWN, never as a weakness. **Sophistication is not defensibility**: an advantage counts only if customers value it, it can be measured, and a funded incumbent cannot copy it quickly.

## Answer

**Unbound has no demonstrated architectural advantage today, and no Track E candidate is built.** Of 22 candidates (the 16 named in the brief plus 6 found in Unbound's requirements and Phase II), the classification is:

| Classification | Count | Candidates |
|---|---|---|
| ordinary product capability | 8 | EK001 append-only history, EK002 deterministic controls, EK004 configuration onboarding, EK005 sponsor segregation, EK007 API-mediated operations, EK009 AI-readable docs, EK012 event-level cost measurement, EK022 durable command execution |
| unproven hypothesis | 6 | EK003 continuous compliance evidence, EK011 unified accounting and operational events, EK016 continuous requirements validation, EK018 sponsor-held payee evidence, EK019 neutral licence model, EK020 low-overhead agent-assisted organization |
| temporary execution advantage | 3 | EK010 reproducible migration, EK017 replayable eligibility decisions, EK021 published migration/exit commitments |
| cost advantage | 3 | EK013 shared Echelon infrastructure, EK014 component monolith, EK015 minimal deployment complexity |
| scale economy | 1 | EK006 shared public charity intelligence |
| learning economy | 1 | EK008 automated exception prevention |
| architectural, organizational or distribution advantage; genuine network effect | 0 | none |

(P3-CLM-EK006.) The 3-5 strongest candidates are in section 5. All of them can be copied by a funded incumbent within roughly 6-30 months, and none is yet built (P3-CLM-EK017).

**Revision 2 (P3-CHL-REV1017, P3-CHL-REV1045).** No measured benefit yet exists that would make any buyer type choose Unbound over existing private-label or turnkey offers that already have SOC 2 Type II reports and references:
- for sponsors, the modelled saving against a well-automated incumbent is $11-71 per account-year, unmeasured;
- for host sponsors and institutions, the benefit of hosted programmes is unmeasured;
- for channel partners, the benefit is filling a capability gap, still to be tested in V-6.

Completing Unbound to S3 does not create customer preference. It removes build cost from the vendor's clock. Buyers weigh SOC history, references and vendor viability, which the entrant lacks (CLM-040).

## 1. What Unbound's architecture actually is (maturity)

Unbound at baseline 79b9258 is a **requirements baseline plus repository tooling**, not a product (P3-CLM-EK005; P3-SRC-EK022..025).

| Element | What the requirement says | Maturity |
|---|---|---|
| CNV-ARC-001 modular monolith | One managed PostgreSQL cluster; schema and database role per sponsor tenant; row-level security on every tenant table with negative isolation tests; dedicated database only by risk or contract; transactional outbox; in-database state machines; brokers only on measured need; RPO 0 in region for authoritative financial data; benchmark before acceptance | Accepted requirement; **benchmark not run** |
| Append-only records | TENANT-AWARE-PERSISTENCE-DESIGN: authoritative business record append-only; corrections as new events; projections rebuildable. FULL-ACCOUNTING-SYSTEM: immutable posting, correction links, bitemporal queries, integrity checkpoints; Strata only for schema management and must refuse destructive changes | Design specification, "NOT implemented or validated" |
| Tenant isolation | Three isolation profiles (schema, database, dedicated) without branching domain logic; tenant resolved from verified principal, never from user input | Design specification |
| Continuous control monitoring | EXECUTABLE-ASSURANCE-ARCHITECTURE: ControlRegistry, EvidenceCollector, EvidenceIntegrity, ExpectedEvidenceMonitor, deterministic ControlEvaluator, NegativeTestHarness, Folio audit packages; 46 specific controls. CONTINUOUS-CONTROL-MONITORING: missing evidence raises a deficiency; Pass never inferred from silence | "Design only, no implemented evidence producers, executed tests or SOC 2 attestation"; "No controls have advanced beyond specification" |
| AI-readable interfaces | AssistanceContract per API operation (side effects, authority class, reversibility, prohibited AI actions) | Requirement |
| Durable execution | Echelon.Execution: idempotency with fingerprint, per-key ordering, leases, retries, quarantine, outbox | **Implemented first slice**; 25 unit and 10 PostgreSQL tests per README; not benchmarked on a managed instance, not deployed |
| Reproducible migration | Transitus phase 1 pipeline (immutable raw evidence, deterministic mapping, rehearsal, reconciliation) | Transitus phase 0: "No production code exists yet" |
| Requirements validation | F# validators, convergence baseline, byte-identical regeneration, public-data replay harness | **Implemented as tooling** (not product functionality) |

Nothing in this report credits Unbound with an operating capability. Every customer-value measure is a design target (P3-GAP-EK008).

## 2. Method

Each candidate was assessed on the brief's eight questions: (1) customer value, (2) measurable, (3) incumbents already provide, (4) reproducible by configuration, (5) requires architectural replacement, (6) requires organizational change, (7) persistent, (8) would customers pay. Each received one class from the controlled vocabulary and a resilience rating against the responses in [13](13-incumbent-response-model.md). Evidence for (3) comes from public product pages, trust pages, API documentation, job postings, press releases and filings; restricted SOC reports were not available (P3-GAP-EK002).

## 3. What incumbents already provide (public evidence)

| Incumbent | Relevant public evidence | Class |
|---|---|---|
| Ren (CMP-001) | Automated vetting, "once a charity is validated, it's trusted across the entire platform"; "over half of grants are instantaneously approved"; ACH with positive pay; 140,000+ charities paid; no API or SOC named on the platform page (SRC-019, fetched; P3-CLM-EK002). Giving Compass impact metrics added 2026-03-05 (P3-SRC-EK008). Engineering posting: C#/.NET Core microservices, multi-tenanted systems, Snowflake (P3-SRC-EK011; P3-CLM-EK013). SOC 2 Type 1 stated in 2023 (P3-SRC-EK010) and 2026 (SRC-017). iPhi CoreEnterprise with GL and subaccounting acquired with Stellar, 2023 (P3-SRC-EK009) | VENDOR-CLAIM |
| Foundant CommunitySuite ("CSuite"; CMP-006) | SOC 2 Type II by Linford & Co. covering security, availability, processing integrity, confidentiality, privacy; AWS; daily backups, RPO 24h, RTO 8h; RBAC, MFA, SSO; no API claims on the trust page (P3-SRC-EK007). Donor portal "tied directly to your accounting system"; 700+ CFs (SRC-075; P3-CLM-EK018) | VENDOR-CLAIM |
| Blackbaud / FIMS lineage (CMP-012, CMP-005) | Trust center: SOC 1 Type II and SOC 2 Type II; incident update 2026-09-02 (P3-SRC-EK014). SKY API over Financial Edge NXT (P3-SRC-EK015). Native change-tracking for RE NXT is supplied by third-party add-ons per community threads (search index, Low). FIMS now owned by NPact, which offered a migration path to Foundation Cloud (SRC-028) | VENDOR-CLAIM / VERIFIED-FACT |
| Chariot (CMP-007) | Versioned public API; Create Grant must be idempotent with an Idempotency-Key; signed webhooks; events retained 30 days; MCP server and llms.txt; SOC 2 Type II claim (P3-SRC-EK012) | VERIFIED-FACT (docs) |
| Daffy (CMP-014) | Public API (public.daffy.org/v1), MCP server, CLI (P3-SRC-EK013) | VERIFIED-FACT (docs) |
| TIFIN Give (CMP-002) | White label for SEI; Louise AI assistant; postings show Python/React/PostgreSQL and AI engineering hiring (SRC-021, SRC-022, P3-SRC-EK021) | VENDOR-CLAIM |
| Fidelity Charitable (P3-CMP-EK001) | Advisor access through GivingCentral; document upload; no public developer API found: UNKNOWN, not absent (P3-SRC-EK017; P3-CLM-EK015) | VERIFIED-FACT |
| DAFgiving360, Vanguard Charitable | Technology vendors and internals not published (Vanguard on Salesforce + Give Interactive per SRC-065) | UNKNOWN |
| NPT (P3-CMP-EK004) | Private-label programs under a joint SLA where NPT carries administrative, legal and technical work; customised dashboards (P3-SRC-EK016); ~14-16 week onboarding (SRC-001) | VERIFIED-FACT |
| Foundation Source (CMP-003) | Vennfi acquisition with a planned white-label RIA/BD platform (P3-SRC-EK018); multi-custodial advisor-branded DAFs via BridgeFT API (SRC-023) | VERIFIED-FACT |
| Give Interactive, Chariot | SOC 2 Type 2 / SOC 3 (SRC-031); SOC 2 Type II claim | VENDOR-CLAIM |
| GivingTech, Givinga | 8-week launch claim; llms.txt; $12.5k base and 30-45 day launch (SRC-029, SRC-030) | VENDOR-CLAIM |

**Not publicly documented by any incumbent** (UNKNOWN, carried from SRC-001 and rechecked): replayable eligibility decisions with source snapshots, versioned policy packs with shadow replay, published migration outcome metrics (CLM-020), and append-only bitemporal financial history (P3-CLM-EK014). These are the only places an entrant can look for a technical edge, and the absence of documentation is not evidence that incumbents lack them.

## 4. Assessment of every candidate

Q1-Q8 as in section 2. Y = yes, N = no, P = partly. Full text per cell is in the register.

| ID | Candidate (Phase II map) | Q1 value | Q2 | Q3 incumbents provide | Q4 config | Q5 arch. replacement | Q6 org | Q7 persistent | Q8 pay | Class | Resilience |
|---|---|---|---|---|---|---|---|---|---|---|---|
| EK001 | Append-only financial history (part ADV-014) | Audit trail | Y | Reversing entries are standard; SOC 1/2 Type II at Blackbaud, Foundant; internals UNKNOWN | P | N (Y only for full replay across multi-lineage books) | N | Low | Low | ordinary | Low |
| EK002 | Deterministic domain controls (MD-3) | Largest modelled saving | Y | Y: Ren automated vetting, >50% instant approvals (VENDOR-CLAIM) | Y | N | N | Low | Low | ordinary | Low |
| EK003 | Continuous compliance evidence (ADV-007) | Lower audit and diligence cost | Y | Incumbents hold SOC history; entrant has none | P | P | Y | Medium after auditor acceptance | Unknown | unproven | Low-Med |
| EK004 | Configuration-driven onboarding (ADV-005) | Faster launch | Y | Y: 8 weeks (GivingTech), 14-16 weeks (NPT), 30-45 days (Givinga) | Y | N | N | Low | Low-Med | ordinary | Low |
| EK005 | Sponsor segregation | Infosec comfort | Y | Multi-tenant platforms; isolation depth UNKNOWN | P | N | N | Low | Low | ordinary | Low |
| EK006 | Shared public charity intelligence (ADV-001/002/003) | Fewer first-time exceptions | Y | Y: Ren, Chariot, CAF America reuse; Candid from $2,750 | Y | N | N | Low | Low | scale economy | Low |
| EK007 | API-mediated operations (ADV-009) | Partner integration | Y | P: Chariot, Daffy, Blackbaud SKY; Ren specs unreviewed; Fidelity UNKNOWN | P | N | N | Low | Low-Med | ordinary | Low |
| EK008 | Automated exception prevention (ADV-006) | Fewer exceptions (~$20/acct at half efficacy) | Y | Incumbents have more repetitions | Y | N | P | Medium with volume | Low | learning economy | Low-Med |
| EK009 | AI-readable API docs (ADV-012) | Safer agent use | Y | Y: Daffy and Chariot MCP/llms.txt; GivingTech llms.txt | Y | N | N | Low | Low | ordinary | Low |
| EK010 | Reproducible migration (ADV-004, ADV-013) | Lower switching risk | Y | Incumbents migrate at volume; none publishes outcomes | P | N | Y | Medium if concentrated (DEC-007) | Low as product | temporary execution | Low-Med |
| EK011 | Unified accounting and operational events (ADV-014) | No internal re-keying | Y | Foundant sells it to CFs; Ren unification UNKNOWN (W06) | N | Y for multi-lineage stacks if W06 holds | Y | Medium if W06 holds | Medium (CFs) | unproven | Medium if W06 |
| EK012 | Event-level cost measurement | Cost-based pricing | Y | UNKNOWN; standard ABC practice | Y | N | P | Low | Low | ordinary | Low |
| EK013 | Shared Echelon infrastructure | Lower fixed cost per product | Y | Incumbents share larger platforms | N | N | Y | Medium only if other products earn | None | cost advantage | Low-Med |
| EK014 | Component monolith (CNV-ARC-001) | Lower ops cost | P | Ren uses microservices; its cost UNKNOWN | n/a | N | N | Low-Med | None | cost advantage | Medium |
| EK015 | Minimal deployment complexity | Lower release cost | P | UNKNOWN | Y | N | N | Low | None | cost advantage | Medium |
| EK016 | Continuous requirements validation (implemented tooling) | Cheaper traceable change | Y | UNKNOWN | n/a | N | Y | Unknown | None | unproven | Medium |
| EK017 | Replayable provenance-bound eligibility decisions (ADV-002 narrowed) | Audit defence | Y | Not publicly documented; inputs commodity (NCCS, Candid) | P | N (P for multi-lineage) | N | Medium-Low | Unknown | temporary execution | Low-Med |
| EK018 | Sponsor-held rail-portable payee evidence | Rail independence | P | Enrolments rail-bound (INFERENCE) | N | N | N | Medium | Unknown | unproven | Medium |
| EK019 | Neutral licence model | Distributor keeps economics | P | Y: GivingTech licence, NPT private label, TIFIN, Foundation Source | Y | N | P for RCF-type models | Low | Medium (distributors) | unproven | Low-Med |
| EK020 | Low-overhead agent-assisted organization | Lower price floor | Y | Incumbents adopt AI too | n/a | N | Y | Unknown | None | unproven | Low |
| EK021 | Published migration/exit commitments (ADV-013) | Lower perceived risk | Y | Not published; matchable by clause | Y | N | N | Very low | Low | temporary execution | Very low |
| EK022 | Durable command execution (implemented slice) | No duplicate grants | Y | Y at API boundary (Chariot idempotency) | N | N | N | Low | None | ordinary | Low |

### Notes on the classifications that matter

- **EK002 deterministic controls** is the most valuable item economically (Phase II: ~$124 of the ~$194 per account-year saving, SRC-063) and the least defensible: Ren already claims it (CHL-003). The modelled gap to a well-automated incumbent is ~$11-71 per account-year ([13](13-incumbent-response-model.md) §4).
- **EK001 append-only history** is the core of the "architecture" story, but customers buy audit trails and SOC opinions, not storage models. An incumbent can add immutability triggers, audit tables and correction lineage to an existing ledger without replacement. Only point-in-time **replay across every book** might need replacement in a multi-lineage stack, and that rests on hypothesis W06 (P3-HYP-EK005).
- **EK003 continuous compliance evidence** inverts in the short run: the entrant's real position is a **disadvantage** (no SOC history; CLM-040), and incumbents can buy compliance-automation tooling (category not sourced, P3-GAP-EK010). It becomes an advantage only if a CPA accepts generated evidence and it lowers audit cost (P3-HYP-EK004).
- **EK011 unified ledger** is already what Foundant sells to community foundations, the segment that does switch (CLM-016, P3-CLM-EK018). It is an advantage only against multi-lineage national/advisor stacks, where switching is rare.
- **EK014/EK015 monolith and minimal deployment** are real cost choices for a small team (infrastructure $15-45 per account-year in Phase II ASM-011), but customers do not pay for topology and an incumbent can answer with price without copying it.
- **EK016 continuous requirements validation** is the one candidate whose tooling is built. Its value is the unproven Echelon Foundry demonstration hypothesis (PRINCIPLES.md: "not yet established").

## 5. The strongest candidates and why

1. **EK017 Replayable, provenance-bound eligibility decisions.** No competitor documents it (UNKNOWN, not absent), it uses append-only storage for a purpose a compliance buyer can see ("show why this grant was approved on that date, with the sources as they stood"), and it is testable for $0 with the existing replay harness (V-3). Weakness: inputs are commodity and an incumbent can add snapshot logging in 6-18 months. Willingness to pay is untested (P3-HYP-EK001).
2. **EK010 Reproducible, reconciliation-proved migration.** No vendor publishes outcomes (CLM-020) and freezes and truncated history recur (CLM-019). It is strongest when migrations cluster on one source (DEC-007) and becomes a learning economy there. Weakness: the incumbent controls the export (CHL-005), the promise is matchable in 0-3 months (CHL-004), and Transitus has no code.
3. **EK011 Unified accounting and operational events.** Integration is the only switch reason stated more than once in the public record (n=3; CLM-016). It needs architectural replacement only for multi-lineage stacks, if W06 holds. Weakness: parity with Foundant at CFs; unverified elsewhere.
4. **EK003 Continuous compliance evidence**, conditional on auditor acceptance. It could lower the licensor's own SOC 1/SOC 2/Nacha TPSP cost (CLM-043), which matters for capital-light licensing more than for customers.
5. **EK014 + EK013 cost position** (monolith on managed PostgreSQL plus shared Echelon components). It lowers the vendor's fixed cost and therefore the price floor in a price war. It does not stop an incumbent from cutting price.

What makes these strongest is that they are **combinations** an incumbent would have to rebuild across products (provenance + replay + reconciliation + one ledger), not single features. Even so, the bundle is defensible only for the time it takes a funded incumbent to notice and build it (about 6-30 months, P3-ASM-EK003..005), which is about the length of one institutional sales cycle (9-24 months, CHL-013). **The window is shorter than the evidence needed to exploit it.**

## 6. Ordinary software capabilities (Executive question 8)

EK001, EK002, EK004, EK005, EK007, EK009, EK012 and EK022 are ordinary product capabilities: needed to compete, already present at incumbents or adjacent vendors, and copyable by configuration or ordinary engineering. Add EK006 (shared charity intelligence, a parity scale economy) and EK021 (a contract clause). They should be built to hygiene level and **not marketed as differentiators** (proposed P3-DEC-EK003; consistent with SRC-001 recommendation 4).

## 7. Implications

- Phase II's conclusion stands and is sharpened: technology does not create a moat; at best it creates a **short execution window** and a **lower cost floor**. Distribution and incentive alignment remain the binding barrier (HYP-001).
- The defensible-looking items are those buyers can audit: replay, reconciliation proofs, generated control evidence. Their value must be tested with auditors and stayers (V-1, V-3) before any build is prioritised for differentiation.
- Network effects: none. Shared intelligence is limited to public facts, and sponsor data cannot be pooled (CLM-035). The only compounding route remains an industry standard others adopt (CHL-011), which is not in sight.

## 8. Main evidence gaps

Incumbent ledger internals (P3-GAP-EK001); SOC scopes uninspected (P3-GAP-EK002); Ren and Fidelity Charitable API documentation not found (P3-GAP-EK007); auditor acceptance untested (P3-GAP-EK006); compliance-automation tooling not sourced (P3-GAP-EK010); no Unbound capability measured because none is built (P3-GAP-EK008, blocking for any superiority claim). Several sources were read through search-index summaries rather than fetched pages; each is marked in [sources.csv](data/fragments/EK/sources.csv).
