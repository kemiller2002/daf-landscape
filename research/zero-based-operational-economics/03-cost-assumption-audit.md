# 03 — Cost assumption audit

Register: [`original-cost-trace.csv`](data/registers/original-cost-trace.csv) (OCT-001..132), each component flagged on eleven audit tests (double counted; inherited conventional staffing; inconsistent allocation; unverified staffing ratio; actually one-time; actually sponsor responsibility; covered by another Echelon capability; unnecessary organisational separation; enterprise-scale inappropriate initially; unnecessary commercial licence; inconsistent with Echelon development method) plus "possibly underestimated". Evidence notes: [original-cost-trace-notes.md](data/evidence/original-cost-trace-notes.md).

Sensitivity rule of thumb in the original model: **$100k of fixed cost ≈ $71M of break-even assets; $1 per account ≈ $5.3M.**

## 1. Overstatements (ranked by effect on the original operating break-even)

| # | Problem | Audit tests failed | Δ break-even | Disposition |
|---|---|---|---:|---|
| 1 | Build amortisation ($388k) inside fixed **and** again in fully loaded | double counted; actually one-time | −$0.27B (op.) | **Reject** from opex; one-time investment |
| 2 | $0.3M flat AI governance/oversight with no workload basis; leans on SR 11-7 (bank guidance); overlaps agent-compute and evaluation lines | unverified staffing ratio; inconsistent allocation | −$0.16 to −$0.21B | **Revise**: AI cost follows exceptions (tokens) plus an AI change-control activity (OA-TEC-021, 384 h) |
| 3 | Echelon share $135k and Echelon licence $60k charged to servicing as standalone cost | covered by Echelon; inconsistent allocation | −$0.14B | **Reclassify-shared** (View 2/3 only) |
| 4 | Controller (60%), founder (15%) and compliance floor paid in fixed **and** priced as event/sponsor minutes | double counted | −$0.13B | **Revise**: workload-derived pools only |
| 5 | $25 "infrastructure" is an account-maintenance placeholder | mislabelled; double counted with EV-E02/E14/E15 and the cloud line | −$0.10B | **Reject**; resource-based infrastructure ([12](12-infrastructure-economics.md)) |
| 6 | Utilisation divisor 0.75 on top of 1,520-1,800 productive hours and on top of fixed segregation staff | double counted slack | −$0.09B | **Revise**: utilisation applies once, to dedicated staff (0.85) |
| 7 | Securities receipt and rail fees ($10.6/acct) borne by custodian or sponsor | actually sponsor responsibility | −$0.05B | **Reclassify-sponsor** (pass-through) |
| 8 | $59k unexplained residual | — | −$0.04B | **Reject** |
| 9 | Small overlaps: three independent-review lines, vCISO vs CTO, compliance consultant, Persona vs EV-E02, GRC licence vs continuous control monitoring, Candid vs free federal data | double counted; unnecessary commercial licence | −$0.02 to −$0.05B | **Revise** |
| 10 | MD-1 comparator uses the superseded $1.18M memo | inconsistent | flatters MD-1 | Noted ([20](20-competitive-comparison.md)) |

Items 1-8 overstate about **$0.95-1.0M a year of fixed cost plus ~$43 per account**.

## 2. Understatements and omissions

| Item | Placeholder | Δ break-even | Zero-based treatment |
|---|---:|---:|---|
| PR #87's own steady-state adjustments omitted (sales to $250k, turnover, replacement onboarding) | $268k | +$0.19B | Sales as COMMERCIAL activity hours; turnover/recruiting added after review ([23](23-adversarial-review.md)) |
| December peak capacity; integer staffing | $50-300k | +$0.04-0.21B | Queue simulation with SLAs; surge option |
| Per-tenant infrastructure floors | $0-250k | ≤ +$0.18B | Deployment C3 ($5.5k per isolated sponsor-year) |
| Registry run cost not in MD-5 | $51-162k | +$0.04-0.11B | Beneficium zero-customer upkeep in View 1 |
| 24x7 on-call for payment release | $30-150k | +$0.02-0.11B | Engineering monitoring/on-call activity; 3 named engineers |
| Nacha TPSP audit missing from MD-5 (present in MD-6/7) | $50k | +$0.035B | FC-007 when the platform originates ACH |
| Insurance limits; fidelity bond | +$20-100k | +$0.01-0.07B | FC-001..003 (no quotes) |
| SOC evidence time; counsel in years 1-3 | not costed | — | OA-TEC-020, FC-008, FC-304 |
| Onboarding $48k vs $757k for a 10k-account sponsor in charity-network 20 | — | fully loaded only | Activity-based onboarding (~790 h) |
| Deferred build tranche (~$0.6M); startup legal (~$0.12M); MSP-vs-MD-5 scope gap | — | build only | [16](16-software-development-economics.md) |

Omissions total about **$0.65-1.1M a year**.

## 3. Classification of the original costs

| Original component | Defensible? | Why |
|---|---|---|
| Loaded labour rates (BLS/O*NET-based) | **Yes** | Sourced (CST-R*, CST-V01); reused in [`roles.csv`](data/model-inputs/roles.csv) |
| Event frequencies (ACT-A*) | **Partly** | Reasonable anchors but unmeasured; reused by the inventory with ranges |
| Grant-approval touch rate ~7.9-9% × ~36-42 min | **Contested** | About twice PR #87's effective rate with determination reuse; sponsor-owned in Unbound's own requirements |
| Three executives on salary in fixed cost (F3) | **No (as structure)** | A staffing design, not a workload derivation |
| SOC 1, SOC 2, pen test, insurance lines | **Yes, with lower bounds** | Vendor claims; echelon-assurance carries the same ranges |
| Sponsor-level 24,240 minutes on top of a fixed controller | **No** | Double counts controller capacity |
| $25 infra | **No** | Mislabelled placeholder |
| AI oversight $0.3M flat | **No** | No workload basis |
| Build $1.94M | **Unsupported either way** | Scaled from a $5M figure with no derivation; Echelon development records show output, not effort ([16](16-software-development-economics.md)) |
| Registry $316k | **No (structure)** | 1.0 FTE steward is a ratio; measured change rates support far less ([13](13-beneficium-public-data-economics.md)) |
| Registry $90-170k | **Partly** | Close to the measured zero-customer upkeep plus recipient work at 20k charities |
| CAC $125k per sponsor | **Untested** | No sales evidence (CLM-026) |

## 4. What would have to be true for $1.92B to stand

1. About **$2.5M a year of recurring fixed cost** really exists, excluding build amortisation. The itemised recurring content is about $1.6-1.8M, so roughly $0.7-0.9M of currently unlisted recurring cost would have to exist (sales staff, December capacity, on-call, TPSP audit, registry operation, coordination overhead, adequate insurance). Plausible in part; none of it is evidenced.
2. **$147 variable per account** holds: the 0.75 utilisation is real slack; per-tenant floors justify $25 of infrastructure; grant approval touches stay near 8% at 36 minutes, and are vendor-borne.
3. **24,240 sponsor-level minutes** are consumed on top of a salaried controller.
4. A **$250k mean balance**, 20 bps realised and 5 equal sponsors.

## 5. Register drift found (documentation only)

`research/competitive-displacement/data/registers/economic-assumptions.csv` still shows MD-5 fixed $2.3M, build high $2.43M and prevention 1.0. Proposed correction is recorded in [24](24-cross-repository-implications.md); this initiative does not edit the preserved baseline.
