# Phase A: requirements inventory

**Date:** 2026-11-22. **Method:** the author read the financial core, administration core, UX failure contracts and widget W01/W02 contracts in full, plus WF-01, WF-05..WF-11, the canonical data model and the event catalog. Three read-only inventory passes ran in separate contexts over:
- the remaining UI and widget documents;
- governance, regulatory and security;
- reviews, economics, organization and experiments.

Their reports were checked against the source text for every item used below. Counts were verified by the passes, or by `wc -l` on the CSV registers.

## 1. Corpus

| Body | Files | Requirement families (counts) | Evidence posture |
|---|---|---|---|
| Financial core v0.5 | 1 | 10 architecture invariants; command envelope; settlement conservation; gates G0–G9 | Self-declared NO-GO; no implementation verified |
| Administration core v0.1 | 6 | ADM-01..30; EST-01..14; AG-01..08; PARTY-01..07; AUTH-01..10; SUCC-01..07; POL-01..10; SPEND-01..06; FEE-01..12; SVC-01..10; GOV-01..10; ECON-01..06; OPS-01..10; INT-01..10; DATA-01..10; MIG-01..09; AI-01..14; SLO-01..07; 25 adversarial scenarios; DEC-ADM-01..10 | Proposed; no legal sign-off |
| UI v0.1 catalog and slices | 2 | D01–D16, O01–O18, E01–E20 (54 capabilities); F01–F16; UI-001..020; J01–J20; D-GR-01..09; O-CASE-01..09; E-FIN-01..10; DEC-UI-01..10; gates UX0–UX5 | Proposed |
| UX v0.2 | 4 | FC-01..24; UX-F01..F20; T01–T36; A1–A12; UX-G0..G8; journeys J-ADV..J-RES | Proposed |
| Widgets | 6 | W01–W16; EW-T01..T30; FS-01..16; GRW-01..20; GRW-F01..F20; P-01..14; H1–H5; SEC/UX/FIN-01..20, OPS-01..10 | Proposed; "no code, security assessment, browser test" |
| AI-native enterprise | ~80 | 18 outcomes; 81 decision types (37 D / 11 P / 33 H); 30 capabilities; 24 workflows; 35 entities; 58 events; 36 API domains; 19 agents; INV-A1..A8; SoD-1..9; 65 REG rows; 54 controls; 22 scenarios; 25 failure modes; 19 assumption challenges; 40 gaps (9 P0); DD-001..021 | Mostly [S]/[A]; E7/E7b is the only measured experiment |
| Workflow innovation | ~60 | 48 innovations; 105 designs; 31 cross-enterprise workflows; E1–E10; 77 adversarial verdicts | Experiments mostly restate parameters, per the authors' own adversarial review |

## 2. What the baseline does well (kept, not re-litigated)

These positions recur across bodies, have legal or control grounding, and survived this program's challenge. They are inputs here, not findings.
- Requests are not instructions (DD-003; ADM distinction 1; W02 "recommend").
- AI flags but never clears, and has no financial authority (DD-002/005; core invariant 9; AI-14; INV-A1..A5).
- External timeout means unknown (core invariant 7; UX-F14; GRW-F14).
- Ledger, custody, legal ownership and portfolio are different records (core invariant 1).
- Bitemporal authority and eligibility (AUTH-05; DATA-03; data model principle 3).
- Never self-custody, never build rails (DD-008).
- SOC 2 claims require execution evidence (core invariant 10; GOV-06; assurance methodology).

## 3. Structural problems found in discovery

| # | Problem | Finding |
|---|---|---|
| 1 | **Two parallel requirement bodies.** `docs/` (ADM/EST/AUTH… and UI) and `research/ai-native-daf-enterprise/` (WF/DD/CTL/REG) specify the same enterprise. Neither cites the other's IDs, except that the admin master cites financial core v0.5. Examples: OPS-03 vs WF-01; AUTH-07/SUCC vs WF-13; INT-04 vs DD-020; ADM-27 vs the agent catalog. | [TVF-030](../16-registers/findings.csv) |
| 2 | **At least seven grant lifecycle vocabularies**: financial core; WF-01; data-model open record; design-system label list; D-GR-08; widget platform receipt; W02 receipt; admin OPS-03. | [TVC-008](../16-registers/contradiction-register.md) |
| 3 | **Three gate schemes** (UX0–5, UX-G0–8, ADMIN-G*), plus financial G0–G9 and roadmap Gates 1–5, with no mapping. Test-ID collisions: `OPS-01..10` exists in both widgets/05 and administration/03. | TVF-031 |
| 4 | **Technology commitment in requirements.** UI and admin headers commit to F#, Limen WASM, Forma and Folio. The research workstream's DD-014 says do not depend on them, and found that Limen ships no WASM engine. | TVC-002 |
| 5 | **Coverage claims exceed evidence.** "Obligation coverage is 100%" (control-framework) while OUTSTANDING A1 (REG→CTL mapping) is open. CTL-037 checks only `current_law` and `sponsor=yes` rows. | TVC-015 |
| 6 | **Controls lack audit-grade fields.** No evidence retention, failure response, independent verification or escalation fields; no REG link; no designed-vs-operating status. | TVF-040 |
| 7 | **Personas.** No persona for users with disabilities, external auditors, charities as users, executors or trustees, or board members. Successors appear only as a field. | TVF-050 |
| 8 | **Economics.** The staffing model uses annual average volume. The December surge exists only in the twin (×3), while the technology architecture assumes 10–30× peaks. Incident and correlated-failure costs are unmodelled. | TVC-017; TVF-060 |
| 9 | **Experiments.** By the authors' own adversarial review, E2, E4, E5, E8 and E9 encode their conclusions in their parameters. E9 assumes bank-side ACH deduplication that ACH does not provide. | TVF-061; TVC-024 |

## 4. Coverage of the directive's domains in the baseline

| Directive domain | Baseline coverage | Gap severity |
|---|---|---|
| Ontology | 35 entities (data model) + ADM objects; no merged ontology | Medium: two partial ontologies |
| Organization | Org model, accountability matrix, functional areas A–N | Medium: SoD concentration in the Controller |
| Workflows | 24 WF + 31 XW + OPS-01..10 | Medium: missing workflows ([workflow catalog](../05-workflows/workflow-catalog.md)) |
| State machines | Grant (WF-01), payment profile (WF-10), foreign case (WF-06), fund lifecycle table, widget session | **High**: grant machine lacks reservation, funding, Unknown, post-settlement return and cancel |
| Financial invariants | Core v0.5 (strong); SPEND (thin) | **High**: no fixing rule for % grants; no over-commitment rule; ACH contribution finality |
| Compliance | 65 REG with honest labels; 54 CTL | High: control fields; unmapped legal rows |
| UX | Strong failure catalog; weak status semantics | High: status vocabulary |
| Widgets | Strong trust contract | Medium: idle-revocation display; partner liability |
| Adversarial | 25 admin scenarios; 22 SC; 77 verdicts | Medium: cross-domain chains missing |
| Economics | Detailed but average-volume | High: surge, incidents, correlated failure |

## 5. Not inspected

- `clarity-framework` (private).
- The local financial core v0.1–v0.4 ZIP packages (not committed, per the core spec's provenance note).
- Most of `research/mission-2026-11-14/` (328 files). It was used only through the AI-native workstream's citations.
- `data/`.
- The F# models were not run. The directive forbids executable simulation, and their results are taken as reported, labelled [X] by their authors.
