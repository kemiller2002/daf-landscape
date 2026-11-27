# 01 — Methodology

Date: 2026-11-27. Status: research. **Not legal, tax, accounting or investment advice; not a launch or expenditure authorisation.** Research agents, adversarial reviewers and the integrator are the same model family: nothing here is independent professional assurance.

## 1. Question

What is the minimum economically sustainable operating model for Unbound (DAF administration), Beneficium (charity intelligence) and the Echelon Foundry capabilities they depend on, when the business, workflows, controls and organisation are designed together from first principles? Specifically, should the previous estimate stand: an operating break-even of about $1.92B assets under administration (AUA) at 20 bps, implying about $3.85M a year of operating expense?

## 2. Principles applied

The mission's fourteen principles were applied as model rules, not only as prose:

| Principle | How it is enforced |
|---|---|
| Start with zero employees and departments | No role exists unless an activity in [`operational-activities.csv`](data/registers/operational-activities.csv) produces hours for it, or a documented control obligation sets a floor ([`control-obligations.csv`](data/registers/control-obligations.csv)). |
| Responsibilities before roles | 180 activities are classified (10 classes) and assigned a responsible entity before any staffing is computed. |
| Roles only when automation, sharing, outsourcing or sponsor ownership cannot satisfy the work | `Staffing.fs` applies, in order: automation (exception rates) → sponsor/external (configuration shares) → founder capacity → fractional professionals → dedicated employees. |
| Staffing from workload, authority, availability, segregation, service obligations | Queue simulation with SLAs and absences (`Simulation.fs`); named-person minimums per segregated pool; hires decided on average load, headcount on peak. |
| Necessary controls vs conventional practice | Every obligation carries a mandate class (legal, regulatory guidance, contractual, industry practice, auditor expectation, risk-based, Echelon policy, uncertain). |
| Never weaken correctness, security, compliance or donor protection | No control was removed to reduce cost. Alternatives preserve the control objective ([21](21-requirement-economic-impact.md)). |
| Eliminate before automating; deterministic before AI | Classes `ELIMINATED`/`PREVENTED`/`DETERMINISTIC` precede `AI-ASSISTED`; the AI factor applies only to `AI-ASSISTED` activities. |
| Separate operations from development | One-time lines (`one_time=Y`) never enter annual opex; investment recovery is reported separately. |
| Echelon as a shared organisation | Three cost views (below); no reusable component is charged wholly to Unbound. |
| No invented requirements, prices or measurements | Evidence classes on every number: `MEASURED-FACT`, `PUBLISHED-PRICE`, `VERIFIED-FACT`, `INFERENCE`, `ASSUMPTION`, `UNKNOWN` ([conventions](data/CONVENTIONS.md)). |
| Preserve unfavourable findings | See [00](00-executive-findings.md) §"What did not improve" and [23](23-adversarial-review.md). |
| No production implementation | Research code only; nothing deployed or purchased. |

## 3. Work plan and dependency order

1. **Reconstruct** the original model by calling its code (not re-implementing it) and trace every material cost to source ([02](02-existing-model-reconstruction.md), [03](03-cost-assumption-audit.md)).
2. **Six parallel research tracks** in independent agent contexts, each writing machine-readable registers and evidence notes:
   activity inventory from Unbound requirements; human control obligations (primary legal sources); Echelon shared capabilities and development records; infrastructure prices (Azure Retail Prices API, AWS Price List API); Beneficium public data (bounded sampling); original cost trace.
3. **Zero-based model** in F# (`model/src/ZeroBased`), referencing the original `CompetitiveDisplacement` project so the baseline is reproduced inside the same run.
4. **Ten adversarial perspectives** in five independent contexts; dispositions recorded; corrections applied; final synthesis ([23](23-adversarial-review.md)).
5. Reports, registers, cross-repository proposals and validation.

The persistent ledger is [`research-ledger.md`](research-ledger.md).

## 4. The model

### 4.1 Workload

For each activity *a* and scenario:

```
events_a        = frequency_a × driver_units_a          (accounts, new accounts, contributions, grants,
                                                         sponsors, onboardings, platform, active charities)
human_events_a  = events_a × exception_rate_a × exception_mult (rates < 1 only)
minutes_a       = human_events_a × minutes_a × duration_mult × (AI factor if AI-ASSISTED)
auth_minutes_a  = human_events_a × minutes_a × independent_review_share   (if independent authorization)
vendor_share_a  = configuration share of the activity's bucket
```

Buckets: Tech, Commercial, Support, AdminException, AdminJudgment, IndependentAuth, SponsorOwned, External, Shared, Eliminated. Seven operating configurations (licensing only → full administration → standalone administrator) assign vendor shares ([`configurations.csv`](data/model-inputs/configurations.csv)). Sponsor-owned work is never vendor labour; it is valued separately at sponsor rates so licensing is not made to look cheap by moving work out of sight ([20](20-competitive-comparison.md)).

### 4.2 Operating-year simulation

`Simulation.fs` spreads each activity's vendor hours over 365 days by seasonality (year-end, month-end, quarter-end, tax season, Q1), adds seeded incidents (security, integration, operational failure), and runs FIFO queues per pool with business-day SLA ageing, absences and urgent-first incidents. The minimum staffing meeting an SLA breach tolerance (1% of hours) is found by doubling and bisection. Outputs: events, automatically completed share, human-assisted and authorised events, queue depth and age, breached hours, utilisation, peak week.

### 4.3 Staffing

Per pool (OPS, FINANCE, AUTH, COMPLIANCE, ENG, COMM, EXT):

- founder hours offset commercial then engineering work (never segregated control pools);
- average load < 0.6 FTE → fractional professionals at fractional rates;
- otherwise dedicated hires = max(average ÷ 0.85, simulated peak), with a least-cost alternative of average-sized staff plus priced surge contractors (OPS and FINANCE only);
- minimum named persons: 2 in each segregated control pool, 3 engineers (author + two non-author approvers, Unbound CNV-PLT-010); missing persons carry a readiness retainer.

### 4.4 Three economic views

| View | Contents |
|---|---|
| **1 Incremental cash** | Labour cash, retainers, infrastructure (resource-based), Beneficium public-dataset upkeep, external per-event costs, incremental fixed lines |
| **2 Allocated economic** | View 1 + founder hours at opportunity cost + Unbound's share of shared Echelon resources (allocation shares in [`fixed-costs.csv`](data/model-inputs/fixed-costs.csv)) |
| **3 Standalone replacement** | View 1 + founder hours at market cost + full replacement of every shared capability + standalone leadership and G&A |

Development is one-time and excluded from all three; investment recovery is computed separately.

### 4.5 Break-even

Costs are step functions, so break-even is the smallest account count from which profit stays non-negative for every larger grid point (70-point log grid, 100 to 2M accounts), not the first crossing. Assets = accounts × mean balance. Assets and accounts are varied independently (balance $5k-$1M).

### 4.6 Uncertainty

- Named scenarios: optimistic (all low), expected, conservative, severe (all high). The corner cases are deliberately implausible bounds.
- Monte Carlo: 300 seeded triangular draws (independent, and correlated with ρ = 0.5 adverse common shock) on 46 zero-based parameters; 200 draws for break-even.
- One-at-a-time tornado on View 1.
- Analytic staffing (average × calibrated peak factor) is used for grids and Monte Carlo; simulated staffing for headline scenarios and step functions. Calibration is reported ([`simulation-calibration.csv`](data/model-outputs/simulation-calibration.csv)).

## 5. Evidence standards

- Every material numeric assumption has id, definition, unit, low/base/high, source, evidence class, confidence, rationale, dependencies, validation method and review date.
- **Nothing is measured operational performance.** Unbound has no production operations, no time study (owner decision OD-M-14 planned one; it has not run) and no design-partner sponsor.
- Public-data sizes are measured from bounded samples (~185 MB downloaded and deleted). Cloud and AI prices are published list prices read 2026-11-27. Legal statements cite primary sources and are classified by mandate.
- Matters needing professional confirmation are listed but no paid consultation was commissioned (owner decision DF-ASR-2026-0D0F authorises no consulting spend).

## 6. Reproduce

```bash
cd model
dotnet test tests/ZeroBased.Tests
dotnet run --project src/ZeroBased -c Release -- run   ../data ../../competitive-displacement/data/model-inputs ../data/model-outputs
dotnet run --project src/ZeroBased -c Release -- check ../data ../../competitive-displacement/data/model-inputs ../data/model-outputs
```

Requires .NET 10 SDK. A run takes under a minute and is byte-identical.

## 7. Limits

- Activity frequencies, exception rates and minutes are anchored to earlier repository estimates and agent judgement; 93 of 180 rows are `ASSUMPTION`, 92 are low confidence.
- The simulation is a fluid FIFO model with deterministic arrivals and seeded incidents; it does not model individual skills, interruptions or learning curves.
- Revenue assumes equal-sized sponsors unless stated; concentration is a stress case.
- The cloud provider is undecided (U-09, FIL-OD-01); Azure is priced as base and AWS as the low case.
