# Financial and staffing models

**Model code:** [`../models/Daf.Enterprise/Economics.fs`](../models/Daf.Enterprise/Economics.fs) and [`Report.fs`](../models/Daf.Enterprise/Report.fs), with tests in `EconomicsTwinCensusTests.fs`. To regenerate every table below:

```
cd research/ai-native-daf-enterprise/models
dotnet run --project Daf.Enterprise.Cli -- ..
```

The outputs are written to [`outputs/`](outputs/). **All numbers in this document come from those files.**

**Status:** a decision-support model, not a forecast. Of 30 parameters, 7 are sourced from repository evidence and 23 are labeled assumptions **[A]** ([`outputs/parameter-register.csv`](outputs/parameter-register.csv)). The repository has no measured sponsor time-and-motion data (GAP-001), no break-cost data (GAP-005) and no contact volumes (GAP-006). Those three gaps are the model's largest uncertainties, and Phase 1 of the roadmap exists to close them.

## 1. Structure

- **Accounts and AUM are separate inputs** (brief §11). AUM = accounts × average balance. Revenue depends on AUM; cost depends mostly on accounts, grants and exceptions. The test `accounts and AUM are independent` checks this.
- **Volume drivers:**
  - grants per account: 8, inside the FY2024 observed range of 6.2 (RCF) to 13.0 (Fidelity) computed from [`sponsor-operating-efficiency-2026-11-20.csv`](../../../data/mission-2026-11-14/sponsor-operating-efficiency-2026-11-20.csv);
  - contributions per account: 2 [A];
  - complex-asset share of contributions: 2% [A];
  - human exception rate: 8% of grants, at the per-grant core review-need proxy of about 7–8.5% (EV-079). That proxy measures recipients needing review, not observed review, so it is conservative in one way: it counts recipients cleared by standing rule. It is unconservative in another: it misses donor-controlled supporting organizations.
- **Staffing:** FTE by role = max(structural floor, volume × handling time ÷ productive hours). The floors encode accountability and segregation-of-duties minimums from the [organization model](../02-business-capabilities/organization-model.md).
- **Revenue:** Fidelity Charitable's published admin-fee tiers (0.60% / 0.30% / 0.20% / 0.15%; $100 minimum), applied to the average balance. The schedule is concave, so this **overstates** revenue for skewed balance distributions.
- **Conventional comparators**, all sourced from FY2024 Form 990s in the repository dataset:
  - *Efficient conventional:* Vanguard Charitable, 232.44 accounts per employee, $124,507 staff cost per employee, $766 non-staff opex per account.
  - *Typical conventional:* AEF, 107.03 accounts per employee.
  - *Frontier:* Fidelity Charitable all-in, about **$790 per account** (24.41 bps × $66.20bn ÷ 204,614 accounts). Fidelity is affiliate-staffed, so its staff sit at FMR and are paid through fees.

## 2. Results at four scales ($300k average balance)

From [`outputs/scale-results.csv`](outputs/scale-results.csv):

| Accounts | AUM | Grants per year | Human exceptions per year | AI-native FTE | Conventional FTE (efficient / typical) | AI-native cost | AI-native $/account | Frontier $/account (Fidelity) | AI-native cost bps | Revenue at published tiers |
|---|---|---|---|---|---|---|---|---|---|---|
| 1,000 | $0.3bn | 8,000 | 640 | **21** | 8 (floor) / 10 | $4.37m | $4,370 | $790 | 145.7 | $1.8m |
| 10,000 | $3bn | 80,000 | 6,400 | **30** | 44 / 94 | $6.97m | $697 | $790 | 23.2 | $18m |
| 100,000 | $30bn | 800,000 | 64,000 | **104** | 431 / 935 | $27.2m | $272 | $790 | 9.1 | $180m |
| 1,000,000 | $300bn | 8,000,000 | 640,000 | **765** | 4,303 / 9,344 | $213.3m | $213 | $790 | 7.1 | $1.8bn |

**Findings:**
1. **At 1,000 accounts the AI-native design costs more than a conventional sponsor**: $4.37m against $1.76m. The accountability floor (leadership, segregation of duties, engineering, agent ownership and evaluation) is fixed. A self-operated AI-native sponsor at 1k accounts cannot cover it on published fees: revenue is $1.8m. This favors *buying* the operating infrastructure at small scale, which is Model C's customer.
2. **Break-even** ([`outputs/break-even.csv`](outputs/break-even.csv)):

   | Case | Break-even accounts |
   |---|---|
   | $300k average balance | about **3,000** |
   | $150k average balance | about 8,000 |
   | $50k average balance | about **56,000** |
   | $800k average balance | about 2,000 |
   | Loaded cost $250k per FTE | about 5,000 |

   Balance size matters more than account count.
3. **Between 10k and 100k accounts the AI-native cost per account falls below the frontier** ($697 → $272, against Fidelity's $790). That is the modeled crossing point, not a ratio to rely on: the Clarity review rates the cost comparison internal-demonstration, Low confidence, until handling times are measured. Against the *efficient conventional* calibration the gap is 4–6×. Against the frontier it is smaller, and the frontier comparison is the honest one.
4. **Accounts per FTE:**

   | Accounts | AI-native accounts per FTE |
   |---|---|
   | 10k | 333 |
   | 100k | 962 |
   | 1m | 1,307 |

   Observed FY2024 figures are 62.7 (NPT), 107 (AEF) and 232 (Vanguard). DAFgiving360's 5,670 *grants* per employee (EV-136) shows that affiliate-staffed models already push some ratios far out, so per-account ratios should not be compared across staffing models without care.

## 3. Staffing by role

From [`outputs/fte-by-role.csv`](outputs/fte-by-role.csv):

| Role | 1k | 10k | 100k | 1m | Driver |
|---|---|---|---|---|---|
| Leadership | 5 | 8 | 10 | 10 | Accountability (fixed) |
| Grants compliance | 1 | 3 | 30 | 300 | Exceptions × 45 min [A] |
| Complex assets | 1 | 3 | 30 | 300 | Complex gifts × 12 h [A] |
| Finance and payments ops | 2 | 2 | 4 | 22 | SoD floor 2; breaks × 20 min [A] |
| Service recovery | 1 | 1 | 7 | 63 | 0.3 human contacts per account [A] |
| Engineering | 4 | 6 | 8 | 10 | log scale [A] |
| Agent ownership and evaluation | 4 | 4 | 4 | 4 | 18 agent families ÷ 6 + lead |
| Security | 1 | 1 | 3 | 3 | Step at 100k |
| Partnerships | 1 | 1 | 5 | 50 | 1 per 20k accounts [A] |
| Philanthropic intelligence | 1 | 1 | 3 | 3 | Step at 100k |
| **Total** | **21** | **30** | **104** | **765** | |

**What the table shows:** at scale, the human organization becomes two specialist pools: grants compliance and complex assets. Every other function stays small. The two pools scale *linearly* with exception volume, so **the economic lever is the exception rate and the reuse of determinations, not headcount**. Exceptions cluster by recipient: about 12.5 grants per recipient at Fidelity ([FINAL-STATUS.md](../../mission-2026-11-14/FINAL-STATUS.md), PR #73 additions). A recipient-level determination (equivalency, expenditure-responsibility pre-qualification, fiscal-sponsor review) reused across accounts would cut per-grant exception work well below the 8% per-grant rate. The model does not yet include reuse; it is the first parameter to measure in Phase 1. At 1m accounts the complex-asset pool would in practice be largely outsourced to non-cash processors (the repository's non-cash vendor research, b40n14-03).

## 4. Cost composition and sensitivity

From [`outputs/cost-lines.csv`](outputs/cost-lines.csv) at 100k accounts:

| Cost line | $m per year | Share of total ($27.2m) |
|---|---|---|
| Staff | 17.2 | 63% |
| Customer acquisition | 6.0 | 22% |
| Custody and pool administration | 1.5 | |
| Payments | 0.54 | |
| Legal and filings | 0.6 | |
| Infrastructure | 0.55 | |
| **AI inference** | **0.078** | **0.3%** |

Inference cost is immaterial, consistent with the repository's validated $0.45 per heavy review finding (EV-106).

**Sensitivity at 100k accounts** ([`outputs/sensitivity-100k.csv`](outputs/sensitivity-100k.csv)). Each factor is halved and doubled; inference cost is halved and multiplied by 10:

| Factor | Cost swing (% of base) |
|---|---|
| Loaded cost per FTE | 94.6% |
| Customer acquisition cost | 33.1% |
| Grants per account | 31.8% |
| Exception rate | 27.6% |
| Minutes per exception | 27.3% |
| Complex-asset share | 27.3% |
| Human contacts per account | 5.5% |
| Infrastructure | 3.0% |
| Inference cost ×10 | 2.7% |

**Reading:** the model is a *people* model. Whether AI-native operations are cheaper depends on how few people the exception and complex-asset pools need. That is precisely what no public source measures (GAP-001), so the headline cost ratios are design hypotheses until a shadow-mode pilot measures exception rates and handling times (roadmap Phase 3).

## 5. Accounts versus AUM

Same account counts, different balances (in [`outputs/scale-results.csv`](outputs/scale-results.csv)):

| Accounts | Average balance | AI-native cost bps | Margin at published tiers |
|---|---|---|---|
| 100k | $50k | 51.8 | 13.7% |
| 100k | $300k | 9.1 | 84.9% |
| 100k | $800k | 3.7 | 92.4% |
| 10k | $50k | 136.8 | −128% |

A mass-market, small-balance book needs very large account counts. The repository shows that most "DAF accounts" by count sit in donation processors holding 0.9% of assets (EV-008), so account count is the wrong growth metric.

## 6. Models A, B, C and D on one grid

From [`outputs/models-abcd.csv`](outputs/models-abcd.csv), with the assumptions in the `note` column:

| Accounts | A: traditional + AI | B: AI-native sponsor | C: infrastructure at $150/account | D: hybrid, 50% fee share |
|---|---|---|---|---|
| 1k | −6% | −143% | −2,803% | −397% |
| 10k | 30% | 61% | −318% | 22% |
| 100k | 32% | 85% | −33% | 71% |
| 1m | 32% | 88% | 6% | 77% |

**Model C pricing:** the cost per account served at $150/account is $4,355 (1k), $628 (10k), $200 (100k) and $141 (1m). So **C needs ≥100k accounts served at ≥$200–300 per account**. The only observed price reference is RCF's audited FY2024 payment to Ren: $19,225,546 for 25,824 accounts, about $745 per account, roughly 98% of RCF's fundholder fee (EV-044). That is one related-party contract, not a market price, but it shows administrators can be paid several hundred dollars per account.

**Steady-state margins favor B.** Steady state is the wrong lens, because the models reach scale differently.

## 7. Time to scale and capital need (the decisive economics)

From [`outputs/ramp-5yr.csv`](outputs/ramp-5yr.csv) and [`outputs/peak-capital.csv`](outputs/peak-capital.csv):

| Path [A] | Year-5 book | Peak capital need | Cumulative result at year 5 |
|---|---|---|---|
| B optimistic: $300k average, 49.5k accounts (~$15bn) by year 5 | 49,500 accounts | $2.5m | +$115.5m |
| **B calibrated: $100k average, ~$2bn by year 5** (the scale Daffy reports after about five years; company-reported, EV) | 20,000 accounts | **$12.8m** | −$11.5m |
| **C at $300/account, clients bringing 20k-account books** (1, 1, 2, 2, 3 clients signed) | 180,000 accounts served | **$6.4m** | +$16.7m |
| C at $150/account, 20k-account clients | 180,000 | $35.8m | −$35.8m |
| C at $300/account, 5k-account clients | 45,000 | $15.2m | −$15.2m |

**Reading:**
- **B's economics depend almost entirely on how fast it can acquire donor assets.** On the optimistic path it is the best business in the repository. On a path calibrated to the fastest observed challenger, it needs about twice C's capital and is still cumulatively negative at year 5. No new sponsor in the repository's 2021–2026 cohort shows the optimistic path (EV, gap19-startup-cohort).
- **C's economics depend on price per account and on client size.** It works only with mid-size or larger sponsors (≥~20k accounts each) at a few hundred dollars per account. The long tail of small sponsors cannot carry it (the 1,240 sponsors under $50m hold 2.84% of assets; strategic synthesis §0 D). This matches the earlier entrant simulation's conclusion that a probe needs large customers.
- **D's economics combine both.** It earns C revenue on institutional books and admin-fee share on its own book. The fee share (50% [A]) and the partner sponsor-of-record terms (GAP-027) are the unmeasured determinants.

These results feed the decision matrix in [`../10-market-and-business-model/models-A-B-C-D-comparison.md`](../10-market-and-business-model/models-A-B-C-D-comparison.md) and the executive synthesis.

## 8. Validation plan for the model

| Parameter | How to measure | Phase |
|---|---|---|
| Exception rate and minutes per exception | Shadow-mode replay of a design partner's historical grants through the policy engine, plus timed reviews | 1–3 |
| Determination reuse factor | Recipient clustering on partner grant history | 1 |
| Complex-asset hours | Partner non-cash case logs | 1 |
| Human contacts per account | Partner contact-center logs before and after shared-state rollout | 3–5 |
| Break rate and minutes | Partner custodian and bank reconciliation history | 1 |
| CAC (B and D) | Advisor-channel pilot | 4–6 |
| Price per account (C) | Design-partner commercial terms, three or more partners | 4 |

Until these are measured, every AI-native cost figure above remains an **[S]** scenario.
