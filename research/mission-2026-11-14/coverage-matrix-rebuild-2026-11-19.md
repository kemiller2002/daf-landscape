# Coverage-matrix rebuild from post-baseline evidence (P-GAP19-02), 2026-11-19

**Outputs**
- `data/mission-2026-11-14/coverage-matrix-entities-2026-11-19.csv`: the new matrix (396 cells). Each cell has a pointer, a validation status and its old status.
- `data/mission-2026-11-14/coverage-summary-2026-11-19.json`: the summary, with baseline comparison and the cells still empty.
- `scripts/mission_coverage_rebuild.py`: new script. It holds the curated evidence tables and rules R1–R6.
- `scripts/mission_coverage.py`: additive `--summarize` mode only. Without the flag it behaves as before.

**Unchanged:** the old `coverage-matrix-entities.csv` and `coverage-summary.json`. Their md5 checksums were identical before and after the run.

**Reproduce**
```
python3 scripts/mission_coverage_rebuild.py .
python3 scripts/mission_coverage.py . --summarize data/mission-2026-11-14/coverage-matrix-entities-2026-11-19.csv data/mission-2026-11-14/coverage-summary-2026-11-19.json
```

## 1. Headline

| Measure | 2026-11-14 matrix | 2026-11-19 rebuild |
|---|---|---|
| Cells investigated (status other than NI) | 248 (62.6%) | 302 (76.3%) |
| Cells partially validated or better (PV, IC or RC) | 57 (14.4%) | 148 (37.4%) |
| Not investigated (NI) | 148 | 94 |
| Discovery started (DS) | 58 | 30 |
| Evidence collected (EC) | 113 | 97 |
| Partially validated (PV) | 20 | 34 |
| Independently corroborated (IC) | 37 | 114 |
| Contradictory evidence (CE) | 3 | 3 |
| Insufficient public information (IP) | 17 | 24 |

**Entities where most cells are NI**
- Before (12): Candid, DAF Direct, Foundant, Goldman Sachs, JCF, NPact, NCF, OneAscent, Pave, SEI, SVCF, TIAA.
- After (5): Candid / IRS BMF, OneAscent, Pave, SEI, TIAA.

**Cell changes**
- 137 cells were upgraded.
- 9 were relabelled to IP: 6 from NI and 3 from DS.
- 1 was corrected (see §2).
- 249 are unchanged.

**Main transitions**
- EC→IC: 28
- DS→IC: 23
- NI→IC: 17
- NI→EC: 13
- EC→PV: 12
- NI→DS: 12
- DS→EC: 10
- PV→IC: 9

### By segment

| Segment | Investigated, before → after | PV or better, before → after |
|---|---|---|
| National / FI-affiliated sponsors | 88.9% → 94.4% | 33.3% → 61.1% |
| Independent / white-label sponsors | 81.7% → 90.0% | 16.7% → 41.7% |
| Technology / administration vendors | 69.8% → 81.2% | 12.5% → 37.5% |
| Digital challengers | 75.0% → 77.8% | 16.7% → 25.0% |
| Payments / verification infrastructure | 54.2% → 68.8% | 8.3% → 39.6% |
| Wealth channels | 41.7% → 63.1% | 14.3% → 28.6% |
| Community / faith / affinity | 33.3% → 61.1% | 2.8% → 36.1% |

### NI cells by checklist item, before → after

| Item | Before | After |
|---|---|---|
| ai | 25 | 20 |
| custody_invest | 19 | 13 |
| assurance | 17 | 11 |
| ownership_funding | 14 | 9 |
| grant_workflow | 10 | 9 |
| timeline | 16 | 8 |
| operating_evidence | 16 | 8 |
| financials | 11 | 6 |
| fees | 12 | 6 |
| distribution | 6 | 2 |
| tech_admin | 2 | 2 |
| legal_role | 0 | 0 |

**How to read IC.** IC keeps the meaning the 2026-11-14 script gave it: at least one validation-register row confirms a claim that addresses this item for this entity. It does not mean the item is exhausted. No cell is RC.

## 2. Method and rules

### Evidence considered

- **Validation registers.** All 33 registers were read: `validation-register.csv`, waves 2a/2b, and waves 3–30 including 24a/b and 25a/b. Of their 859 rows, 348 name a matrix entity. Each of those rows was classified by hand to an (entity, checklist item) cell.
- **Datasets.** 69 post-baseline datasets were mapped to checklist items, searching on their entity key columns. The candidate rows were then reviewed by hand. The baseline inventory (`repo-inventory-baseline.json`) lists no mission datasets, so all of them post-date the baseline.
- **Documents.** Queue-batch, direction and earlier queue documents were used where a dataset or register row was absent: `queue-batch33-market-structure.md` §4.1 for Edward Jones, `queue-batch35-access-owners-faith.md` §3 for SEI, and `queue-cf-vendor-map.md` §3 for Foundant.

### Rules (in `mission_coverage_rebuild.py`)

- **R1 (IC).** A cell becomes IC only where a register row confirms a claim on that item.
- **R2 (PV).** A cell becomes PV where a register row confirms only partially, or confirms only a narrow part of the item. Examples: one web page, one product line, or a search-index capture only.
- **R3 (EC or DS).** A cell becomes EC where a dataset or document holds entity-specific evidence on the item. It becomes DS where the evidence is only a fragment:
  - one or two dated events for `timeline`;
  - a complaint scan with zero records;
  - a 990-derived revenue floor for a private vendor's `financials`.
- **R4 (IP).** A cell becomes IP where a recorded check shows the item is not public:
  - sponsor SOC reports: `sponsor-audit-notes.csv` `soc_report_reference=none`;
  - vendor SOC scope: `vendor-assurance-scope-2026.csv`.
- **R5 (no downgrade).** No cell is downgraded, except where its only support does not address the item.
- **R6 (CE kept).** CE stays unless a later register row resolves the conflict.

### Why the old matrix under-counted

`mission_coverage.py` assigns IC only when a register row's `entity` and `checklist_item` strings equal the matrix strings exactly. Most register rows fail that test:
- About three-quarters use other item labels, such as `filing`, `computation` or `primary_page`.
- Entity names vary. "DAFgiving360" never matches "DAFgiving360 (Schwab Charitable)", and "Edward Jones; Morgan Stanley" never matches either entity.

So confirmed claims were missed. Examples:
- DAFgiving360 operating_evidence (V2A-08);
- MS GIFT tech_admin (V2B-15);
- NPact legal_role (V10-02 and V16-27/28);
- JCF grant workflow (V26-06).

P-G02-02 proposes columns that would make this mapping mechanical.

### Corrections and judgement calls

- **Corrected: RCF `assurance`, IC → IP.** Its only support, V2A-23, is RCF's Charity Check vetting policy, not a SOC report. That claim now supports RCF `grant_workflow` (EC → IC). The IP pointer is `sponsor-audit-notes.csv`: statements read, no SOC reference.
- **Give Interactive `ownership_funding`, PV → IC.** V3-10 is marked "contradicted", but what it contradicts is the repo's "ownership unknown". The validator found primary evidence: Signatry's Schedule R names Give Interactive LLC as a controlled partnership.
- **Goldman Sachs `grant_workflow`, NI → IC.** The support is V15-09, the 2024-ratio program circular. V18-01 is listed in the validation column because it resolves the batch-33C conflict in favour of V15-09.
- **JCF.** Only rows for JCF New York (EIN 23-7174183) were used. V12-07 concerns JCF San Diego and was excluded.
- **Rows not mapped to any item:**
  - SEI vendor-footprint rows: SEI Investments as a CF investment manager, not the SEI Charitable Fund;
  - TIAA Kaspick and Morgan Stanley security incidents: not SOC scope;
  - `delegated-access-routes`, `agent-delegation-terms` and `daf-agent-wrappers` rows: donor-access terms, not distribution channels or AI claims;
  - `announced-vs-delivered` rows that are not about AI: Charityvest AVD29 and Vanguard AVD37.
- **Contradicted rows that do not change a cell:**
  - V29-05: MS GIFT, a repo recompute error, not the filing;
  - V22-25: Fidelity callback;
  - V21-17: Endaoment terms;
  - V14-20: Candid citation, substance confirmed.
  
  They are noted in `validation_status` or `rebuild_notes`.
- **Vendor assurance.** Where the type is stated (Chariot, Foundant, Give Interactive, Benevity), the old EC stays. `vendor-assurance-scope-2026.csv` shows that no vendor publishes a scoped report, so a stricter reading would be IP throughout. That stricter reading was applied only to cells that had no investigated status yet (TIFIN, DS → IP), so no investigated cell was downgraded.

## 3. Pointer format

The pointer is in `evidence_pointer`:
- **Register:** `validation-register-waveN.csv#CLAIM-ID`.
- **Dataset:** `data/mission-2026-11-14/<file>.csv [row key or filter]`.
- **Document:** `research/... §section`.
- **No new evidence:** `baseline only: <2026-11-14 evidence_files>`.

The validation status is in `validation_status`:
- `validated: wave N CLAIM (result)` or `partially validated: …`;
- `validated (2026-11-14 exact-name match): …` for ICs carried over from the old matrix;
- `not validated` otherwise.

The old status, the change type, and the old evidence files and notes are kept in their own columns.

## 4. Cells still Not investigated (94), by entity

| Entity | NI cells |
|---|---|
| Candid / IRS BMF | financials, fees, tech_admin, custody_invest, ownership_funding, timeline, operating_evidence (several are probably not applicable to a data vendor; the vocabulary has no n/a code) |
| OneAscent (OneGive) | financials, custody_invest, grant_workflow, assurance, timeline, ai, operating_evidence |
| Pave Finance | financials, tech_admin, grant_workflow, assurance, timeline, ai, operating_evidence |
| SEI (SEI Charitable Fund) | financials, fees, custody_invest, grant_workflow, assurance, ai, operating_evidence |
| TIAA (Charityvest program) | financials, custody_invest, grant_workflow, assurance, ownership_funding, ai, operating_evidence |
| Jewish Communal Fund | fees, distribution, assurance, ownership_funding, timeline, ai |
| DAF Direct | financials, custody_invest, assurance, ai, operating_evidence |
| NPact | fees, custody_invest, grant_workflow, ai, operating_evidence |
| Edward Jones | assurance, ownership_funding, timeline, ai |
| Foundant (CommunitySuite) | fees, custody_invest, grant_workflow, operating_evidence |
| Give Interactive | fees, custody_invest, grant_workflow, ai |
| National Christian Foundation | distribution, ownership_funding, timeline, ai |
| Silicon Valley CF | assurance, ownership_funding, timeline, ai |
| Bank of America CGF | ownership_funding, timeline, ai |
| Stellar / iPhi | custody_invest, assurance, ai |
| Benevity / workplace processors | custody_invest, grant_workflow |
| DAFgiving360 | assurance (`sponsor-audit-notes.csv`: audit not retrieved), ai |
| GiveClear Foundation | assurance, ownership_funding |
| Givinga | custody_invest, grant_workflow |
| Morgan Stanley GIFT | ownership_funding, ai |
| AEF, Charityvest, Chariot, Endaoment, Goldman Sachs, NPT, RCF | one each: ai (AEF, Charityvest, GS, NPT, RCF); custody_invest (Chariot, Endaoment) |

**Patterns**
- `ai` is the largest remaining gap: 20 of 33 entities. P-G02-01 proposes a cheap public check for it.
- The four thin wealth channels (OneAscent, Pave, SEI, TIAA) hold 28 of the 94 NI cells. They are already queued as P-GAP19-08.
- Edward Jones is queued as P-GAP19-07.
- Several `custody_invest` NI cells sit on vendors or processors where the item may not apply: Chariot, Give Interactive, Foundant, NPact, Stellar, Givinga and Benevity.

## 5. Limits

- The classification of register rows to cells is a coordinator judgement recorded in the REG table, not a new validation. Each row can be audited from its claim id.
- Dataset upgrades rest on matches in entity-key columns that were then reviewed by hand. EC means the dataset holds entity-specific rows on the item, not that the rows were re-checked.
- The share figures now overstate completeness less than they understate validation. Even so, IC ≠ complete. Read the 37.4% "PV or better" as "at least one validated claim on the item".
- Queue proposals: `data/mission-2026-11-14/queue-proposals-g02.csv` (P-G02-01, P-G02-02).
