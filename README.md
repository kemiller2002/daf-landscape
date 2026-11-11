# DAF Technology Landscape

An evidence-led research repository for understanding the U.S. donor-advised fund (DAF) technology market: the legal sponsors that control charitable assets, the administrators that operate DAF programs, and the software and infrastructure vendors that support contributions, investment accounting, grant review, disbursement, and nonprofit reconciliation.

**Baseline date:** 2026-11-11<br>
**Research status:** initial foundation; directional, not exhaustive<br>
**Geographic scope:** United States unless a record explicitly says otherwise

## Goals

1. Build a durable map of the DAF operating and technology stack.
2. Distinguish legal sponsorship from administration, software, custody, payment, and fundraising roles.
3. Compare offerings without turning vendor marketing into unqualified fact.
4. Preserve claim-level evidence with source dates, access dates, and confidence.
5. Identify the questions and testable hypotheses that should drive interviews, demos, filings review, and later market sizing.

## Scope

### Included

- National, community-foundation, and mission-oriented DAF sponsor models.
- Sponsor program administration and business-process outsourcing.
- Donor, advisor, staff, and nonprofit-facing DAF software.
- Contribution intake, complex-asset handling, custody/investment interfaces, subaccounting, compliance, grant workflow, disbursement, and reconciliation.
- White-label and private-label DAF programs for financial institutions, employers, nonprofits, and advisors.
- Publicly supportable relationships among sponsors, administrators, platforms, and infrastructure providers.

### Not yet included

- An exhaustive sponsor census or global market map.
- Market share, revenue, pricing, or assets-under-administration estimates without comparable primary evidence.
- Product-quality rankings, security conclusions, or implementation recommendations without testing and customer evidence.
- Legal, tax, investment, or charitable-giving advice.

## Core distinction

The IRS describes a DAF as a separately identified fund or account maintained by a sponsoring organization. The sponsor has legal control of contributed assets; the donor or donor advisor retains advisory privileges over distributions or investments. This means a consumer brand, software vendor, custodian, and legal sponsor may be different entities. The repository records them separately.

## Method

1. **Define the claim.** Record one bounded, falsifiable statement rather than a general impression.
2. **Prefer primary evidence.** Use statutes and regulators first, then filings, audited reports, contracts/policies, official product documentation, and dated first-party announcements.
3. **Label vendor assertions.** An official product page can verify that a vendor represents a capability; it does not independently prove performance, adoption, security, or market leadership.
4. **Link every populated fact.** Landscape and matrix rows cite source IDs from `data/source-register.csv`.
5. **Date the evidence.** Keep both the source's publication/effective date and the date it was checked.
6. **Score confidence.** `high` means direct and specific primary evidence; `medium` means current first-party evidence that still needs corroboration or testing; `low` is not allowed in the verified-fact fields.
7. **Keep unknowns honest.** In the matrix, `unknown` means not yet established; it does not mean the capability is absent.
8. **Separate hypotheses.** Unverified ideas live in `docs/research-questions.md`, never in a verified-fact field.

See [the full methodology](docs/methodology.md) for evidence grades, confidence rules, freshness, and change control.

## Repository map

| Path | Purpose |
| --- | --- |
| `data/landscape.csv` | Initial entity map and verified role/relationship facts |
| `data/competitive-matrix.csv` | Evidence-backed comparison framework; deliberately contains unknowns |
| `data/source-register.csv` | Source/evidence register with dates, grades, confidence, and supported claims |
| `docs/classification-framework.md` | Vendor taxonomy, unit of analysis, and matrix field definitions |
| `docs/workflow.md` | End-to-end DAF operating and technology workflow |
| `docs/research-questions.md` | Research questions and explicitly unverified hypotheses |
| `docs/methodology.md` | Research, verification, freshness, and contribution rules |
| `CONTRIBUTING.md` | How to add or change a claim |

## Initial coverage

The first pass includes representative national sponsors and purpose-built DAF administrators/platforms. Inclusion signals relevance to the workflow, not endorsement, quality, or market position. The baseline intentionally avoids vendor rankings and most quantitative claims until comparable filings and customer evidence are collected.

## How to use the data

- Start with `data/landscape.csv` to see who plays which role.
- Use `data/competitive-matrix.csv` to identify verified capabilities and research gaps.
- Resolve each `source_ids` value against `data/source-register.csv` before repeating a claim.
- Treat `unknown` as a research assignment.
- Re-check any web source before a consequential decision, even if its freshness window has not expired.

## Near-term research sequence

1. Validate sponsor legal names, EINs, public-charity status, and latest Form 990 data in IRS TEOS.
2. Normalize audited sponsor scale metrics for a single fiscal year and definition set.
3. Conduct product demos against one scripted workflow and evidence checklist.
4. Interview sponsors, advisors, nonprofit finance teams, and implementation partners.
5. Map custody, banking, charity-data, identity, sanctions, and payment dependencies that vendors do not prominently disclose.
6. Add pricing and contracting evidence only when the unit, tier, and effective date are comparable.
7. Monitor the IRS priority-guidance project under sections 4966 and 6033; do not treat the 2023 proposed regulations as final guidance.

## Disclaimer

This project is market research, not legal, tax, investment, cybersecurity, or procurement advice. A cited official source may be accurate as to what an organization states while still requiring independent validation.
