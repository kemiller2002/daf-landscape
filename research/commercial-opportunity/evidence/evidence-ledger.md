# Commercial-opportunity evidence ledger

**Date:** 2026-11-20. This ledger indexes every evidence series used by the commercial-opportunity package. It lists where each series' records live and how far each has been verified. Nothing here has passed a numbered validation wave yet.

| Prefix | Records | Location | Content | Verification |
|---|---|---|---|---|
| INV001–INV120 | 120 | [`data/commercial-opportunity/inventory.csv`](../../../data/commercial-opportunity/inventory.csv); narrative in [phase0-repository-inventory.md](phase0-repository-inventory.md) | Repository facts relevant to commercial questions, each with its validation status and evidence date | Carries the repository's own validation status per row |
| PS01–PS23, PW01–PW24, PV01–PV31 | 78 | [`data/commercial-opportunity/`](../../../data/commercial-opportunity/) `prospects-*.csv` | Prospect hypotheses with sources, supporting and contradictory evidence, confidence and next validation action | Agent research. The lead removed names not verified on an official page |
| DS01–DS45 | 45 | [demand-signals-and-process-economics.md](../market-validation/demand-signals-and-process-economics.md) §4 | Demand signals, spend distribution, process economics | Spend tables reproduced by the lead with [`scripts/commercial_sponsor_spend_distribution.py`](../../../scripts/commercial_sponsor_spend_distribution.py) |
| CP01–CP60 | 60 | [competition-and-pricing.md](../competitive-landscape/competition-and-pricing.md) §6; [`competitors.csv`](../../../data/commercial-opportunity/competitors.csv) (40 rows) | Competitors, failed firms, price benchmarks | Fidelity Charitable–McKinsey ($11,805,000, FY ending 2025-06-30, "PHIL. CONSULTING") re-checked by the lead in `form990-contractors-harvest-full.csv` and `form990-contractors-fy2025-refresh.csv` |
| DE001–DE073 | 73 | [DAFCP evidence register](../../../data/dafcp-investigation-2026-11-20/evidence-register.csv) | DAFCP programme, issuer, relationships, curriculum and adoption | Lead re-checked the decisive sources |
| SS01–SS13 | 13 | [education study-source register](../../education/dafcp-study-source-register.md) | Syllabus and textbook status | Textbook ISBNs read on AbeBooks. Syllabus not read (robots); owner-fetch OF-525 |
| OF1–OF10 | 10 | [`opportunity-scores.csv`](../../../data/commercial-opportunity/opportunity-scores.csv) | Scored opportunities, with a basis per row | Judgements, recorded so they can be disputed |

## Reliability classes used

| Class | Meaning | Examples |
|---|---|---|
| Filing fact | IRS Form 990 XML, audited statements | Vendor payments, IT spend, McKinsey fee |
| First-party statement | Organisation's own page or release | Mercer launch, SEI release, College trademark guidelines |
| Vendor marketing | Self-reported claims | Daffy $2bn; Ren market-share claims |
| Secondary or snippet | Trade press, search snippets, LinkedIn | Pricing reports, some job postings |
| Scenario or model | Repository model outputs | AI value pools |
| Inference | Analyst reasoning | Exit windows; buyer roles |

## Stale evidence flags

These sources predate 2024 and are used only for context:
- Datos Insights (2021);
- Celent (2003);
- the 2018 TPI conversation data;
- the 2009 Chronicle community-foundation fee survey.

See [phase0-repository-inventory.md](phase0-repository-inventory.md) §(c).

## Inaccessible sources

| Source | Reason | Route |
|---|---|---|
| DAFCP 200 syllabus | robots.txt disallows the path | Owner fetch, OF-525 |
| Job boards (Indeed, LinkedIn Jobs, Glassdoor, ZipRecruiter) | Login or robots | Snippets only |
| Business Wire releases | 403 | Republications |
| Foundant site | robots disallows Claude agents | Not fetched |
| Blackbaud investor site | 403 | Not fetched |
| Paid analyst reports (Cerulli, Datos) | Paywall | Prices only |
