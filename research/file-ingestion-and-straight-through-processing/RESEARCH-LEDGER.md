# Research ledger — file ingestion and straight-through processing (2026-11-26)

Provenance, checkpoints, decisions and disagreements for this package. Evidence ids resolve in
[`evidence.csv`](../../data/file-ingestion-2026-11/evidence.csv).

## Checkpoints

| # | Checkpoint | Output |
|---|---|---|
| 1 | Repository survey: existing DAF research and economics models read before new research | Cited by path rather than repeated |
| 2 | Stream A — DAF sponsor intake (≈48 organizations) | 142 rows FIE-A-001..142 (125 confirmed, 9 inferred, 8 proposed) |
| 3 | Stream B — formats, delivery, adjacent industries | 66 rows FIE-B-001..066; 33-format inventory |
| 4 | Stream C — security, storage and AI costs (prices read from AWS Price List and Azure Retail Prices APIs) | 55 rows FIE-C-001..055 |
| 5 | Synthesis — 115-workflow inventory, STP opportunities, competitor comparison, economics model v1 | Chapters 03, 08, 09, 10 |
| 6 | Independent adversarial review R3 (economics, regulation, evidence spot checks) | 20 findings (6 material) |
| 7 | Revision — economics model v2, evidence corrections, wording corrections | This ledger §3 |

## Method decisions

- **D1** Industry research holds no product requirements; product names appear only in cross-repository links (gate F4).
- **D2** A workflow is *confirmed* only when a mapped evidence row is itself confirmed (gate F3).
- **D3** The economics model is deterministic (three explicit cases) so every number reproduces exactly.
- **D4** Volume drivers and handling minutes are labelled assumptions; no ingestion handling time is measured anywhere
  public (gaps G1, G2).

## Adversarial review R3 and resulting revisions

| Finding | Severity | Disposition | Revision |
|---|---|---|---|
| R3-01 free cost cliff above 1 − investigation share | material | accepted | Prevention modelled as a scenario with its own cost; routine STP excludes investigations |
| R3-02 99% STP unsupported | material | partially accepted | Planning targets 75–85% → 90% → 95% stretch; dashboard STP reported; 99% kept as a labelled sensitivity point |
| R3-03 balance confounded with cost case | material | accepted | Shares reported for $50k/$150k/$300k books in every row |
| R3-04 small-sponsor fixed costs omitted | material | accepted | Run cost, amortised onboarding, standalone staffing floor; pooled vs standalone |
| R3-05 document rows counted as zero | material | accepted | Documents count files plus per-fund records |
| R3-06 unlabelled volume drivers; grant rows mis-set | material | partially accepted | Basis columns; grant-driven rows; small-sponsor monthly-feed scenario not modelled (gap) |
| R3-07 file exceptions used record STP | moderate | accepted | Separate file-exception share |
| R3-08 uniform investigation share | moderate | accepted | Class-specific shares aligned with reconciliation-break rate; productive hours aligned |
| R3-09 double counting with staffing models | moderate | accepted | Stated as a slice of operating cost |
| R3-10 advisor-managed and migration volumes | moderate | accepted | Advisor-managed funds drive custody rows; migration excluded from annual model |
| R3-11 onboarding parameters vs anchor | moderate | accepted | Bespoke 15/30/50 days |
| R3-12 "platform" cost mislabelled | moderate | accepted | metered_cloud_usd plus run cost |
| R3-13 measured vs assumed lost downstream | moderate | accepted | input_basis column; wording corrected |
| R3-14 unverifiable or mis-cited evidence | moderate | accepted | FIE-B-013 marked unverified; FIE-B-012, B-066, A-016, B-043 notes corrected |
| R3-15 Nacha 2026 overstated | moderate | accepted | Chapter 04 wording corrected |
| R3-16..20 | minor | accepted | Thresholds, metric hygiene; no change needed for 17a-4 and OFAC |

Recorded disagreement: the reviewer would drop 99% from the grid; it is kept as a sensitivity point and labelled.

## Disagreements between streams

- Stream B recommended a managed inbound SFTP endpoint per sponsor from the start; the synthesis treats it as conditional
  because pull covers documented custodians (06).
- Stream B rated XLSX, generic ZIP and generic XML "initial"; the synthesis narrows them (values-only XLSX for migration,
  ZIP only for trusted public datasets, XML only for named schemas).

## Handoff

Next evidence to collect, in order of decision value: measured touches and minutes per exception type (G1, G2); the
launch bank's reporting and lockbox specifications (G3); the first custodian's feed specification (G4).
