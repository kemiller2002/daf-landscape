# Competitive displacement and structural economic advantage (Phase II)

Date: 2026-11-26. Status: research from public sources and the owner's repositories. **Not legal, tax or investment advice; not a launch authorisation.** Every economic figure is conditional on labelled inputs; nothing is measured. Research agents, adversarial reviewers and integrator are the same model family, so nothing here is independent validation.

**Start with [00-executive-summary.md](00-executive-summary.md); final answers in [24-final-recommendations.md](24-final-recommendations.md).**

## Reports

| # | Report | Track |
|---|---|---|
| 00 | [Executive summary](00-executive-summary.md) | — |
| 01 | [Existing research synthesis and initialization](01-existing-research-synthesis.md) | — |
| 02 | [Charity intelligence sources](02-charity-intelligence-sources.md) | A |
| 03 | [Charity data licensing and access](03-charity-data-licensing-and-access.md) | A |
| 04 | [Charity intelligence architecture](04-charity-intelligence-architecture.md) | A |
| 05 | [Charity registry economics](05-charity-registry-economics.md) | B |
| 06 | [Competitive displacement](06-competitive-displacement.md) | C |
| 07 | [Institutional switching incentives](07-institutional-switching-incentives.md) | C |
| 08 | [Frictionless onboarding](08-frictionless-onboarding.md) | D |
| 09 | [Event-level operating model](09-event-level-operating-model.md) | E |
| 10 | [Zero-touch administration economics](10-zero-touch-administration-economics.md) | E |
| 11 | [Institutional distribution](11-institutional-distribution.md) | F |
| 12 | [Market entry segments](12-market-entry-segments.md) | F |
| 13 | [Compounding competitive advantages](13-compounding-competitive-advantages.md) | G |
| 14 | [Alternative enterprise models](14-alternative-enterprise-models.md) | H |
| 15 | [Capital and break-even reassessment](15-capital-and-break-even-reassessment.md) | E/H |
| 16 | [Commercial entry strategy](16-commercial-entry-strategy.md) | F/H |
| 17 | [Unbound implications](17-unbound-implications.md) | — |
| 18 | [Transitus implications](18-transitus-implications.md) | — |
| 19 | [Echelon Foundry implications](19-echelon-foundry-implications.md) | — |
| 20 | [Adversarial review](20-adversarial-review.md) | — |
| 21 | [Evidence gaps](21-evidence-gaps.md) | — |
| 22 | [Commercial validation plan](22-commercial-validation-plan.md) | — |
| 23 | [Executive decision register](23-executive-decision-register.md) | — |
| 24 | [Final recommendations](24-final-recommendations.md) | — |

Ledger: [research-ledger.md](research-ledger.md).

## Machine-readable registers (`data/registers/`)

| Register | Rows | Content |
|---|---|---|
| [sources.csv](data/registers/sources.csv) | SRC-001.. | Sources with dates, limitations, evidence class |
| [claims.csv](data/registers/claims.csv) | CLM-001.. | Claims: confirmed / inferred / hypothesized / contradicted / unknown |
| [hypotheses.csv](data/registers/hypotheses.csv) | HYP-001.. | Testable hypotheses with falsifiers |
| [competitors.csv](data/registers/competitors.csv) | CMP-001..016 | Competitor register |
| [charity-data-sources.csv](data/registers/charity-data-sources.csv) | 68 | Charity data sources (30 prior + 38 new) |
| [operational-events.csv](data/registers/operational-events.csv) | EV-E01..25 | Operational events with costs per mode |
| [economic-assumptions.csv](data/registers/economic-assumptions.csv) | ASM-001.. | Every model assumption with range and basis |
| [market-segments.csv](data/registers/market-segments.csv) | SEG-001..014 | Market segments |
| [competitive-advantages.csv](data/registers/competitive-advantages.csv) | ADV-001..014 | Candidate advantages classified |
| [adversarial-challenges.csv](data/registers/adversarial-challenges.csv) | CHL-001.. | Challenges, dispositions, changes |
| [decisions.csv](data/registers/decisions.csv) | DEC-001..012 | Proposed decisions (none approved) |
| [open-questions.csv](data/registers/open-questions.csv) | OQ-001..020 | Open questions |
| [cross-repository-implications.csv](data/registers/cross-repository-implications.csv) | XRI-001..018 | Proposals for Unbound, Transitus, Echelon Foundry, Praxis |

Agent evidence: `data/evidence/` (Tracks A, C, D, F). Model inputs and outputs: `data/model-inputs/`, `data/model-outputs/`.

## Reproduce and validate

```bash
cd model
dotnet test tests/CompetitiveDisplacement.Tests
dotnet run --project src/CompetitiveDisplacement -c Release -- check ../data/model-inputs ../data/model-outputs
dotnet run --project src/CompetitiveDisplacement -c Release -- validate ..
```

## Rules followed

Public sources only; no logins, outreach or representation of Echelon Foundry; no paid services or infrastructure; no production functionality; no change to Unbound or Transitus files (proposals only); absence of public evidence is never treated as proof of absence; incomparable economic units are never divided into one another.
