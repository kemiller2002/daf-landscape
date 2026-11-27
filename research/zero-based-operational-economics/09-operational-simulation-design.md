# 09 — Operational simulation design

Code: `model/src/ZeroBased/Simulation.fs` (queue simulation), `Staffing.fs` (staffing decisions), `Workload.fs` (event generation). The model references and reuses the original `CompetitiveDisplacement` project (CSV, sampling, baseline reproduction) instead of creating a competing framework. **This is a theoretical capacity model. Nothing it produces is production performance.**

## 1. What is simulated

A full operating year (365 days; weekends have no capacity) with:

| Element | Implementation |
|---|---|
| Routine events | 182 activities × driver units (accounts, new accounts, contributions, grants, sponsors, onboardings, platform, active charities) |
| Seasonality | `flat`, `year_end` (Nov ×1.5, Dec ×3.5 with 55% of December arrivals in the last 10 days), `month_end` (last 3 days ×6), `quarter_end` (×20), `tax_season` (Jan-Apr ×2), `annual_q1` |
| Exceptions | exception rate × handling minutes; AI factor only on AI-assisted work |
| Human approvals | independent-authorization second-person minutes routed to the pool of the reviewed work |
| Operational failures | seeded operational-recovery events (FINANCE, 3-day SLA) |
| Automation failures | seeded mass-remediation events (OPS 10-day SLA, ENG 5-day SLA) |
| Security incidents, integration failures, recovery | TECHOPS activities (OA-TEC-002/004/006/023) — not double counted in the simulation |
| Staffing absences | 25 days per person per year as a daily capacity haircut |
| New sponsor onboarding | per-onboarding activities at the configured onboarding rate |
| Period-end accounting, year-end giving, audit preparation | month-end, year-end and Q1 profiles |

## 2. Queue mechanics

- Daily arrivals per pool are grouped by SLA class (SLA hours ÷ 24, minimum one business day).
- FIFO service with short-SLA work at the head; capacity = staff × 6.5 productive hours × (1 − absence share).
- SLA age counts **business days**; weekend arrivals start their clock on the next business day (a defect found and fixed during the build: calendar ageing inflated staffing 400-fold).
- Measured per pool: arrived hours, completed hours, peak queue depth (hours), peak queue age (business days), breached hours, utilisation, peak week.
- **Minimum staffing** is the smallest headcount (0.05 FTE resolution) at which breached hours ≤ 1% of arrivals. Search: start at average load, double until feasible, bisect.

## 3. Staffing decision layered on the simulation

1. Founder hours offset COMM then ENG work.
2. Fractional professionals while average load is below 0.6 FTE **and** fractional is cheaper than dedicated; minimum engagement 50 h per pool.
3. Otherwise dedicated hires = max(average ÷ 0.85, simulated peak), or, for OPS and FINANCE only, average-sized staff plus surge contractors for the hours that would breach (1.5× fractional rate plus $15k readiness) when cheaper.
4. Named-person minimums (2 per segregated pool, 3 engineers, 2 compliance) with readiness retainers for any person not otherwise employed.
5. Management overhead (10% of other staffed hours) added to the executive pool.

## 4. Analytic mode and calibration

Break-even grids and Monte Carlo use **analytic staffing**: hours × peak factor ÷ productive hours (1.5 for OPS, FINANCE and COMPLIANCE; 1.1 for steady pools). Calibration against the simulation at the headline points: analytic View 1 is within **−5% to +6%** of simulated ([`simulation-calibration.csv`](data/model-outputs/simulation-calibration.csv), and the headline comparison in the ledger). Compliance is peak-driven (simulated/average ≈ 2 at 4,000 accounts) because its 24-48 h SLAs fall in the December peak and surge staff cannot hold its authority.

## 5. Reference run ($500M AUA, 2,000 accounts, 1 sponsor, CFG-5)

| Measure | Value |
|---|---:|
| Events | 304,128 |
| Completed without a person | 96.7% |
| Human-handled events | 9,953 |
| Independently authorized events | 1,222 |
| Human hours (vendor / sponsor) | 8,545 (7,200 / 1,344) |
| Peak queue (ENG / OPS / COMPLIANCE) | 132 h / 86 h / 49 h |
| Peak queue age | 2-6 business days |
| Breached hours | within 1% tolerance in every pool |
| Engineering utilisation | 90% |
| Cost per account / grant / contribution / sponsor / human exception (View 1) | $448 / $16.65 / $12.48 / $206k / $178 |

Unit costs allocate each activity's labour (at the effective hourly cost of the staffed organisation) and external cost to its driver; fixed and infrastructure costs are spread per account. At this scale the per-account figure is dominated by fixed engineering and assurance.

## 6. Theoretical versus validated capacity

| Quantity | Status |
|---|---|
| Event frequencies | anchored to repository estimates (ACT-*, EV-*); unmeasured for Unbound |
| Exception rates and handling minutes | unmeasured; 93 of 182 activity rows are ASSUMPTION |
| SLAs | from Unbound requirements where stated; otherwise assumed |
| Productive hours, absences, utilisation | assumptions |
| Queue behaviour | deterministic fluid model; real queues are lumpier |

**Validated capacity: none.** The first production quarter, or the synthetic operating-year time study already planned under OD-M-14, should replace these inputs ([25](25-evidence-gaps-and-validation-plan.md)).

## 7. Limitations

No individual skills or learning curves; no discrete absences; sub-day SLAs approximated as next business day (24×7 paged response is costed separately); implementation projects spread evenly rather than lumpy; incidents seeded with a fixed seed (reproducible, not a distribution of years).
