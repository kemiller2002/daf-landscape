# DAF servicing economics, commercial viability and market entry

**Date:** 2026-11-25.

**Mission:** [2026-11-25-servicing-economics-agent-mission.md](../2026-11-25-servicing-economics-agent-mission.md), plus the owner's expanded brief.

**Status:** theoretical research.
- No outreach, paid data, consultations or confidential information.
- Unbound is read-only; proposed requirement changes are in report 09.
- **Not evidence of commercial profitability, and not a launch authorization.**

**Start here:** [10-executive-findings.md](10-executive-findings.md).

## Reports

| # | Report | Content |
|---|---|---|
| 00 | [Source baseline](00-source-baseline.md) | Revisions, passes, evidence rules, corrections |
| 01 | [Pricing and scope](01-pricing-and-scope.md) | 59 price observations; 5-35 bps positioning; Ren at MS GIFT 18.5 bps / $737 per account |
| 02 | [Sponsor market analysis](02-sponsor-market-analysis.md) | 1,597 sponsors; attractiveness; top-25 hypotheses; whole market re-costed |
| 03 | [Organization and budget](03-organization-and-budget.md) | Models A/B/C; BLS-based compensation; cost register; Echelon Foundry effect |
| 04 | [Activity cost and capacity](04-activity-cost-and-capacity.md) | 33 activities, 6 archetypes x 4 approaches; $75 / 48-minute test; 180-day verification |
| 05 | [Financial model and sensitivity](05-financial-model-and-sensitivity.md) | Break-even, margins, price, stress, scale, sponsor-level results |
| 06 | [Capital and runway](06-capital-and-runway.md) | 60-month cash plans; capital ranges; staging |
| 07 | [Market-entry strategy](07-market-entry-strategy.md) | Strategies A-F; recommendation; competitive response; safeguards |
| 08 | [Adversarial review](08-adversarial-review.md) | 38 findings and dispositions; 9 perspectives; Clarity-structured challenge |
| 09 | [Requirements transfer candidates](09-requirements-transfer-candidates.md) | 17 candidates for Unbound governance |
| 10 | [Executive findings](10-executive-findings.md) | The 15 questions answered with conditional ranges |
| — | [Research ledger](research-ledger.md) | Checkpoints and test runs |

## Data (`data/commercial-opportunity/servicing-economics/`)

| File | Rows | Content |
|---|---:|---|
| `sponsor-economics.csv` | 1,597 | Sponsor economics by EIN (SPN pass) |
| `sponsor-model-economics.csv` | 1,540 | Every sponsor re-costed by the F# model |
| `customer-attractiveness.csv`, `attractiveness-weights.csv` | 1,448 / 15 | Attractiveness scores and weights |
| `top25-hypotheses.csv`, `self-sustaining-candidates.csv`, `unattractive-large.csv`, `segment-summary.csv` | 25 / 43 / 19 / 26 | Hypothesis lists (not sales leads) |
| `price-observations.csv` | 59 | Normalized price observations |
| `cost-register.csv`, `role-compensation.csv`, `staffing-models.csv` | 109 / 15 / 67 | Costs, compensation, organization models |
| `activities.csv`, `approaches.csv`, `capacity-model.csv`, `staffing-steps.csv`, `verification-180.csv`, `workload-tails.csv` | 33 / 15 / 28 / 176 / 36 / 24 | Activity-based costing and capacity |
| `echelon-capabilities.csv` | 22 | Echelon Foundry capability verification |
| `framework-procedure.jsonl`, `assumption-challenge-template.csv`, `assumption-challenge-adv.csv` | 29 / 9 / 13 | Clarity/EDF procedure and challenges |
| `adversarial-findings.csv` | 38 | Adversarial findings |
| `evidence-register.csv`, `assumptions-register.csv`, `decision-register.csv` | 293 / 88 / 10 | Registers |
| `requirements-candidates-act.jsonl` | 9 | Requirement transfer candidates from the ACT pass |
| `pass-reports/*.jsonl` | 6 | Verbatim research-pass reports |

## Reproduce

```bash
cd research/commercial-opportunity/servicing-economics/model
dotnet test tests/ServicingEconomics.Tests          # 28 tests
dotnet run --project src/ServicingEconomics -c Release -- out ../../../../data/commercial-opportunity/servicing-economics/sponsor-economics.csv
cd ../../../.. && python3 -I -B research/commercial-opportunity/servicing-economics/scripts/assemble_reports.py .
```

Pass scripts are in [`scripts/`](scripts/): `sponsors/`, `pricing/`, `costs/`, `activities/`, `frameworks/` and `adversarial/`. Downloaded primary files are not committed because of their size; their URLs are in the evidence register.
