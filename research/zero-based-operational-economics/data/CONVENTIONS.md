# Data conventions (zero-based operational economics)

- CSV: UTF-8, comma-delimited, one header row, LF endings, RFC 4180 quoting (quote any field containing a comma, quote or newline). Multi-valued fields use `|`.
- Stable IDs, never reused. Dates `YYYY-MM-DD`. "Last reviewed" date for this initiative: 2026-11-27.
- Evidence classes (exactly one per row):
  - `MEASURED-FACT` — measured by us (e.g., bounded HTTP HEAD sample, row count of a file we inspected).
  - `PUBLISHED-PRICE` — vendor's current public price page, with URL and access date.
  - `VERIFIED-FACT` — primary source (statute, regulation, filing, official docs) directly states it.
  - `INFERENCE` — derived from cited facts by stated reasoning.
  - `ASSUMPTION` — judgement with no direct evidence; must say so.
  - `UNKNOWN` — not established; give the conservative placeholder used.
- Confidence: `high` | `medium` | `low`.
- Mandate classes for obligations: `LEGAL-MANDATE` | `REGULATORY-GUIDANCE` | `CONTRACTUAL` | `INDUSTRY-PRACTICE` | `AUDITOR-EXPECTATION` | `RISK-BASED` | `ECHELON-POLICY` | `UNCERTAIN`.
- Activity classification (exactly one): `ELIMINATED` | `PREVENTED` | `DETERMINISTIC` | `AUTO-EXCEPTION` | `AI-ASSISTED` | `HUMAN-JUDGMENT` | `INDEPENDENT-AUTHORIZATION` | `SPONSOR-OWNED` | `EXTERNAL-PROVIDER` | `SHARED-ECHELON`.
- Every material numeric assumption carries: id, definition, unit, low, base, high, source, evidence_class, confidence, rationale, dependencies, validation_method, last_reviewed.
- Never invent legal requirements, prices, measurements. When unsure, say UNKNOWN and give a conservative range.
- No paid services, logins, outreach, bulk downloads of production-scale datasets, or production deployment.
