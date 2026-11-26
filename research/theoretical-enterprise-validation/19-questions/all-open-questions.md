# All open questions and data

Every unanswered question from the program is in one place: **[open-questions.csv](open-questions.csv)**, 183 rows, generated from the registers.

Each row has:
- the question;
- what it blocks;
- who decides;
- the options or the validation route;
- this program's recommendation, where one exists;
- its priority or severity;
- the source register.

The program decided none of these.

## 1. Questions by type

| Type | Count | Who answers | Where the detail lives |
|---|---|---|---|
| Owner decisions (OD-01..22) | 22 | Board, GC, CFO, CRCO, product owner (named per row) | [owner-decisions.md](../16-registers/owner-decisions.md) |
| Contradictions: which requirement prevails (TVC-001..044) | 44 | Named per row | [contradiction-register.md](../16-registers/contradiction-register.md) |
| Assumptions to validate (TVA-001..030) | 30 | Evidence: interviews, sponsor data, counsel | [assumption-register.csv](../16-registers/assumption-register.csv) |
| Open questions inside requirements | 33 | Owning domain | [requirements.csv](../16-registers/requirements.csv) |
| Severity-5 findings (design answer needed) | 16 | Product owner + domain owner | [findings.csv](../16-registers/findings.csv) |
| Round-4 findings, no amendment drafted (TVF-226..254) | 29 | Product owner, together with counterparty evidence | [revision 3 §D](../06-state-models/revision-3-amendments.md) |
| External evidence needed (EXT-01..09) | 9 | Vendors, custodians, banks, sponsor data, users | [ledger §4](../LEDGER.md) |
| **Total** | **183** | | |

## 2. If you only answer five

These block the most work. Full rows are in the CSV.

| ID | Question | Authority |
|---|---|---|
| OD-01 | Can a board-delegated, version-pinned policy be the sponsor's approval of each routine grant? This is the basis of the whole no-touch model. | Board + GC |
| OD-04 | How much reversible (ACH) contribution value may fund grants before the return window closes, and when is the acknowledgment issued? | CFO + GC |
| OD-13 | How do approved grants meet cash: currency reservation with haircut, cash sleeve, or pool buffer? | CFO + Investment Committee |
| OD-19 | When is a grant recognised in the accounts, and in which tax year are late or cross-year items reported? | CFO + external CPA |
| OD-22 | Is any human ever allowed to edit payee, authority, ledger or policy data directly, including at custodians, bank portals and identity providers? | CTO + CRCO + Audit Committee |

## 3. Questions for professional review [C]

These need counsel or a CPA, not a product decision:
- OD-01 delegated approval;
- OD-03 grants after a donor's death;
- OD-04 acknowledgment timing;
- OD-09 recipient refunds;
- OD-12 retention schedule;
- OD-19 grant recognition;
- TVC-003;
- TVC-016;
- TVC-023;
- TVA-001;
- TVA-020 reliance on other sponsors' determinations;
- TVCTL-13 OFAC blocking as applied to DAFs;
- TVCTL-14 supporting-organization classes.

## 4. Data inventory

| Dataset | Rows | Contents |
|---|---|---|
| [open-questions.csv](open-questions.csv) | 183 | This file's questions |
| [scenarios.csv](../11-scenarios/scenarios.csv) | 513 | Every scenario: round, workflow, category, permitted and prohibited outcomes, governing rules, result, linked finding, severity |
| [findings.csv](../16-registers/findings.csv) | 242 | Every finding: severity, domain, source scenarios, evidence, linked contradiction, proposed requirement |
| [requirements.csv](../16-registers/requirements.csv) | 61 | Requirements graph with 21 traceability fields |
| [assumption-register.csv](../16-registers/assumption-register.csv) | 30 | Assumptions with confidence, evidence quality, impact, reversibility, falsification and validation path |
| [contradiction-register.md](../16-registers/contradiction-register.md) | 44 | Contradictions with options, recommendation and authority |
| [owner-decisions.md](../16-registers/owner-decisions.md) | 22 | Decisions with options and what each blocks |
| [raw reviews](../13-adversarial-reviews/raw/) | 4 files | Verbatim role-separated review records, including objections the author did not accept |

Baseline datasets that the program read but did not change are in [`research/ai-native-daf-enterprise/`](../../ai-native-daf-enterprise/): evidence register, gap register, controls, regulatory matrix, events, workflows.

**Regenerating the CSV.** It was produced by a one-off script from the registers listed above. If you edit a register, the CSV does not update by itself. Either regenerate it, or treat the register as authoritative.
