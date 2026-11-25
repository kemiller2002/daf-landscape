# 00: Source baseline

**Date:** 2026-11-25.

**Mission:** [2026-11-25-servicing-economics-agent-mission.md](../2026-11-25-servicing-economics-agent-mission.md), plus the owner's expanded brief of the same day:
- assume 20 bps on average assets under administration;
- work backward to viable assets, organization, capital and customers;
- challenge the existing models.

**Status:** theoretical research. No outreach, paid data, consultations or confidential information were used.

## Repositories and revisions

| Source | Revision | Role |
|---|---|---|
| `kemiller2002/daf-landscape` | `main` @ `e1a3633`; work on branch `claude/daf-economics-event-architecture-v1zdti` | Research repository; all results are recorded here |
| `kemiller2002/unbound` | `main` @ `9b38de4` (read-only) | Economic validation (reports 05, 05a), evidence backlog (13), public-data replay (14), savings claims (15), authoritative baseline, simplification mission |
| Echelon-AI-Native-Enterprise-Design-Framework | `763ff8c` | Echelon Foundry capability evidence |
| AI-Engineering | `1bc519b` | Agent-engineering evidence (no capability trial claimed there) |
| clarity-framework | `200a9eb` | Clarity procedure |
| echelon-diagnostic-framework | `710d54c` (EDF v0.3) | EDF procedure |

The Clarity and EDF clones are single-commit, so the older pins in `research/mission-2026-11-14/clarity-edf-application-guide.md` (Clarity `8cd48019`, EDF `41fea6f`) could not be compared.

## Starting hypotheses under test

| Hypothesis | Source | Outcome |
|---|---|---|
| 20 bps on average billable AUA | Owner working assumption | A market price for books averaging $250k+ per account; below cost for $100-150k books unless floored (reports 01, 05) |
| 5 core FTE, $1,177,750 fixed | [Bottom-up budget memo](../daf-servicer-bottom-up-operating-budget-2026-11-25.md) | A low case: $1.66M base for the same roles; $1.74M once dual control adds a second operations person (report 03) |
| $75 per account-year incremental, $40 of it labour (48 min at $50/h) | Same memo | Labour rate is $65.45/h; the split is wrong (payments about $26, not $10); about $89 per account under AI-native handling (report 04) |
| Break-even about $725M at $200k average balance | [20 bps market-entry memo](../daf-servicing-20bps-market-entry-2026-11-25.md) | About $1.1-2.0B for a lean organization at realistic balances and handling (report 05) |
| Unbound staffed offer $150-299 per fund-year against Ren's $413-745 | Unbound reports 05, 05a | Ren comparator corrected: 18.5 bps or $737 per account at MS GIFT; 38-40 bps on average assets at USCGT and RCF (report 01) |

## Research passes

Each pass was a role-separated agent from the same model family as the integrator. Its output is kept verbatim in [`pass-reports/`](../../../data/commercial-opportunity/servicing-economics/pass-reports/), and its scripts are in [`scripts/`](scripts/).

| Pass | Scope | Main outputs |
|---|---|---|
| PRC | Pricing and competitor economics | 59 price observations; IRS 990 XML, ADV brochures and the MS GIFT donor circular read directly |
| SPN | Whole-market sponsor dataset and attractiveness | 1,597 EINs, attractiveness scores, top 25, self-sustaining and unattractive lists |
| CST | Cost register, labour, staffing models A/B/C | 109 cost lines, 15 roles, 3 organization models |
| ACT | Activity-based costing and capacity | 33 activities, 6 archetypes x 4 approaches, capacity steps, 180-day verification |
| ECH | Echelon Foundry capabilities; Clarity and EDF procedure | 22 capabilities, 29 framework steps, challenge template for 9 assumptions |
| ADV | Adversarial review (model audit, nine perspectives) | Report 08 |

## Evidence handling

**Registers.** The merged [evidence register](../../../data/commercial-opportunity/servicing-economics/evidence-register.csv) has 270 items and the [assumptions register](../../../data/commercial-opportunity/servicing-economics/assumptions-register.csv) has 80. Each row records:
- source URL or repository path;
- source type;
- filing period;
- access date (2026-11-25);
- quality grade: A primary and read, B primary with unclear scope, C secondary, D inference.

**Labels.** Every number in the reports is labelled [S] sourced, [A] assumption, [D] derived or [E] estimate.

**Rules applied throughout:**
- Donor-facing fees are never treated as servicer revenue.
- Schedule I recipient rows are never treated as grant counts.
- Average assets are a proxy, (beginning + end of year) / 2, and are labelled as such.
- Year-end run-rates are shown separately.

**Downloaded primary files** (990 XML, ADV PDFs, the donor circular, BLS/O*NET extracts) were used in scratch space and are not committed, because of size. Their URLs are in the evidence register.

**Blocked sources:**
- bls.gov returned 403 and its API was throttled, so OEWS was read through O*NET OnLine (grade B).
- philanthropy.org, ProPublica PDF downloads, NAPA and PSCA returned 403.
- FY2025 returns for MS GIFT, USCGT and RCF were not yet in the IRS index.

## Tooling

**F# model.** The research model is in [`model/`](model/): .NET 10 SDK, xUnit tests, deterministic output. F# matches the language Unbound's replay tool uses, and the model is research tooling, not product code. Pass scripts are Python, standard library only, functional style.

**Commands:**
- `cd model && dotnet test tests/ServicingEconomics.Tests`
- `dotnet run --project src/ServicingEconomics -c Release -- out ../../../../data/commercial-opportunity/servicing-economics/sponsor-economics.csv`
- `python3 -I -B research/commercial-opportunity/servicing-economics/scripts/assemble_reports.py .`

## Corrections to earlier repository work (recorded, originals preserved)

| Earlier statement | Location | Correction |
|---|---|---|
| Outsourced administration "approximately 33-37 bps" | Unbound report 13 / 05 §3a; prior 20 bps memo | Year-end denominators and two clients only. 38-40 bps on average assets for USCGT/RCF; 18.5 bps at MS GIFT (report 01) |
| No TIFIN Give payment found | Repository notes cited by PRC | GiveClear FY2024 990 paid Tifin Give LLC $185,921 (EV-PRC) |
| $1,177,750 fixed budget as the lean base | Bottom-up memo | A low case; base $1.66M for the same roles (report 03) |
| $40 = 48 minutes | Bottom-up memo | $40 = about 37 minutes at the evidence-based $65.45/h (report 04) |
| Break-even $725M (B = $200k) | Bottom-up memo | Depends on omitted costs and the uncapped capacity assumption; see report 05 |
| SPN cost-to-serve parameters | Pass SPN | Placeholders; superseded by the F# re-costing in `sponsor-model-economics.csv` |
