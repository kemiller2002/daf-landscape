# 09 - Event-level operating model

Status: research (2026-11-26). The business is modelled as **25 operational events**, not departments. Inputs: [events.csv](data/model-inputs/events.csv) (anchored to the existing activity register ACT-A01..S07, SRC-003) and [parameters.csv](data/model-inputs/parameters.csv). Register: [operational-events.csv](data/registers/operational-events.csv). Outputs: [event-costs-by-mode.csv](data/model-outputs/event-costs-by-mode.csv), [event-pareto.csv](data/model-outputs/event-pareto.csv), [results.md](model/out/results.md).

## 1. Method

For each event *e* and operating mode *m*, per account-year:

```
human minutes = frequency(e) × P(touch | m) × minutes per touch(m)
labour        = human minutes / 60 × rate(expertise(e))
expected failure cost = frequency × P(fail) × failure multiplier(m) × (1 − prevention)
                        × (failure minutes × rate + failure external cost + expected loss)
event cost    = labour + vendor external cost + AI cost + prevention cost + expected failure cost
```

Sponsor-level events (close, audit, reporting, configuration) are minutes per sponsor-year; onboarding and migration are one-time. Rail fees (ACH, check, wire) are **sponsor pass-through** (CNV-PAY-001) and are reported separately.

The decomposition separates the two things AI-productivity claims usually mix:
- **P(touch)**: how often a person is involved. Lowered by deterministic rules, exception design and prevention.
- **minutes per touch**: lowered by AI preparation (factor 0.6, range 0.4-0.9; ASSUMPTION; HYP-008).

Exception handling without AI is modelled as AI-native minutes divided by the AI factor, so the difference between exception-driven (MD-4) and AI-native (MD-5) is the AI effect alone.

## 2. Events (base values; MD-1 conventional vs MD-5 AI-native)

| Event | Freq/acct-yr | Expertise | Human min MD-1 | Human min MD-5 | $/acct MD-1 | $/acct MD-5 | Failure lifecycle cost (MD-5) |
|---|---|---|---|---|---|---|---|
| E01 Account opening (agreement and fund set-up) | 0.12 | ops | 2.52 | 0.16 | 2.87 | 0.30 | $51 |
| E02 Identity verification | 0.12 | ops | 0.48 | 0.09 | 0.96 | 0.53 | $135 |
| E03 Contribution receipt and posting (cash ACH check securities) | 2.5 | ops | 12.00 | 0.73 | 24.21 | 11.89 | $70 |
| E04 Contribution attribution (pooled receipt to fund) | 2.5 | ops | 6.00 | 0.80 | 8.19 | 1.70 | $132 |
| E05 Asset liquidation and complex noncash assets | 0.003 | accounting | 2.16 | 0.90 | 3.66 | 2.29 | $3,273 |
| E06 Investment allocation | 1 | ops | 1.50 | 0.20 | 1.87 | 0.42 | $116 |
| E07 Charity discovery (assisted search) | 9 | ops | 2.70 | 0.72 | 4.42 | 2.06 | $16 |
| E08 Charity vetting (transaction-time check 180-day renewal and event monitoring) | 9 | compliance | 49.95 | 0.79 | 63.38 | 4.82 | $1,242 |
| E09 Grant recommendation intake | 9 | ops | 9.00 | 0.45 | 10.80 | 0.94 | $22 |
| E10 Grant approval (eligibility purpose and nonstandard grantee review) | 9 | compliance | 55.80 | 12.25 | 66.47 | 16.15 | $372 |
| E11 Payment processing (ACH check wire) | 9.045 | ops | 12.66 | 3.12 | 15.27 | 5.03 (+$14.92 rails) | $83 |
| E12 Payment failures (returns uncashed voids reissue) | 9.045 | ops | 2.70 | 0.68 | 3.72 | 2.22 | $70 |
| E13 Reconciliation (bank custodian ledger; monthly close) | 12.5 | accounting | 10.00 | 0.62 | 13.32 | 1.94 | $246 |
| E14 Statement generation and acknowledgments (incl. fee billing) | 1 | ops | 4.00 | 0.25 | 5.73 | 1.53 | $34 |
| E15 Customer communication (human-handled contacts) | 0.5 | ops | 5.00 | 2.80 | 6.37 | 3.89 | $40 |
| E16 Advisor administration (advisor onboarding fee schedules rep codes) | 0.1 | ops | 0.90 | 0.24 | 1.11 | 0.38 | $68 |
| E17 Account changes (address advisor bank contact) | 0.3 | ops | 1.80 | 0.21 | 2.16 | 0.37 | $66 |
| E18 Successor administration (death succession) | 0.02 | ops | 1.20 | 0.70 | 1.87 | 1.23 | $601 |
| E19 Fraud investigation (account takeover payment redirection) | 0.002 | compliance | 0.36 | 0.07 | 2.97 | 1.61 | $23,318 |
| E20 Compliance exceptions (sanctions alerts incidents) | 12.5 | compliance | 2.00 | 0.08 | 2.54 | 0.29 | $1,271 |
| E21 Regulatory and governance reporting | per sponsor | controller | 4800 / 2640 min per sponsor-year | | | | |
| E22 Audit preparation (sponsor audit SOC bridge) | per sponsor | controller | 7200 / 3600 min per sponsor-year | | | | |
| E23 Sponsor onboarding and configuration upkeep | per sponsor | implementation | 7200 / 3600 min per sponsor-year; one-time 36000 / 18000 min | | | | |
| E24 Data migration | per sponsor | implementation | one-time 18000 / 9000 min + 6 / 2 min per account | | | | |
| E25 Account closure (final grants transfers residual) | 0.02 | ops | 0.60 | 0.12 | 0.71 | 0.18 | $138 |

(Generated from `data/model-outputs/event-costs-by-mode.csv`; sponsor-level rows show conventional / AI-native minutes.) Totals: **183 human minutes per account-year conventional vs 26 AI-native** (PR #87 found ~30 at steady state with a floor near 12; consistent).

## 3. Expertise, controls and external costs

Required expertise and controls per event are in the register. External costs that do not fall with automation: identity checks ($3 per new account), securities transfer costs (~$10 per transfer), complex-asset appraisal ($350), fraud investigation costs ($600 per attempt), rails ($14.92 per account at 9 payments; sponsor pass-through). Infrastructure is $25 per account-year owned (range $15-45) or $81 licensed software for conventional administrators.

## 4. Where the cost concentrates

| Rank | Conventional (MD-1) | Share | AI-native (MD-5) | Share |
|---|---|---|---|---|
| 1 | Grant approval | 23% | Payment processing incl. rails | 23% |
| 2 | Charity vetting | 22% | Grant approval | 18% |
| 3 | Payment processing | 10% | Contribution posting | 14% |
| 4 | Reconciliation + close | 10% | Reconciliation + close | 7% |
| 5 | Contribution posting | 8% | Charity vetting | 5% |
| | Top five | **74%** | Top five | **67%** |

**A small number of events drives cost.** Conventionally, two judgement events (approval and vetting) are 45% (CLM-012). After redesign, the residual is dominated by things automation does not touch: rails, securities transfer costs and the irreducible judgement in grant approval (sponsor-reserved and 4967 cases).

## 5. Successful versus failed events

The lifecycle cost of a failed event dwarfs the cost of a successful one: a successful grant approval costs about $1.62 in AI-native mode, a failed one about $372; a successful vetting check about $0.29, a payment to an ineligible recipient about $1,242 (counsel, recovery, 4966 exposure); a fraud attempt that succeeds about $23,300. **Expected failure cost is about 19% of AI-native event cost against about 10% conventionally** (base): as routine work disappears, failures become the larger share, so prevention matters more than throughput ([10](10-zero-touch-administration-economics.md)).

## 6. Can input design eliminate whole categories?

| Category | Mechanism | Effect in model | Evidence |
|---|---|---|---|
| Unidentified contributions | Notification-first structured intents; unique fund reference or virtual account | −60% attribution touches and failures | INFERENCE (FIE: attribution is the main exception, SRC-004) |
| Vetting rework | Change-driven monitoring with evidence expiry | −50% | INFERENCE ([05](05-charity-registry-economics.md)) |
| Approval exceptions | Closed charity picker; purpose taxonomy; policy rules evaluated at recommendation time | −40-50% | ASSUMPTION |
| Payment failures | Verified destinations; e-payment enrolment; positive pay | −30-50% | INFERENCE (PR #88) |
| Fraud loss | Callback to aged contacts; bank-change holds | −70% of losses | INFERENCE (Nacha false-pretenses) |
| Paper | In-app agreement acceptance; IRS data instead of determination letters | eliminated (14 of 115 ingestion workflows, SRC-004) | INFERENCE |

Customer incentives (e.g. no fee for e-payment enrolment; faster grants for structured contributions) and upstream integrations (custodian feeds with fund keys) are the levers; they require sponsor and partner cooperation, which is a commercial dependency, not a technical one.
