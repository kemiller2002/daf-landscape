# 09 - Event-level operating model

Status: research (2026-11-26; revision 2 after adversarial review). The business is modelled as **25 operational events**, not departments. Inputs: [events.csv](data/model-inputs/events.csv) (anchored to the existing activity register ACT-A01..S07, SRC-003) and [parameters.csv](data/model-inputs/parameters.csv). Register: [operational-events.csv](data/registers/operational-events.csv). Outputs: [event-costs-by-mode.csv](data/model-outputs/event-costs-by-mode.csv), [event-pareto.csv](data/model-outputs/event-pareto.csv), [results.md](model/out/results.md).

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
- **minutes per touch**: lowered by AI preparation (factor 0.85, range 0.6-0.97; field evidence, REV2; HYP-008).
- **utilisation**: loaded rates are divided by 0.75 (range 0.65-1.0) because staffed labour is not perfectly divisible (REV2).

**Revision 2 (adversarial review).** The `d_native` inputs were calibrated assuming AI preparation at 0.6; they are converted once to exception minutes without AI (÷0.6) and the AI factor then scales them down. A weaker AI therefore makes AI-native dearer rather than making exception-driven cheaper (CHL-100). Native touch rates for vetting (E08) and reconciliation (E13) were rebased to pre-prevention values so prevention is not counted twice (CHL-056/102); audit preparation is held at conventional minutes (CHL-105); automation is no longer assumed to reduce failures (fail multiplier 1.0, CHL-061/107); prevention runs at half efficacy until bank and custodian partners exist (CHL-060).

## 2. Events (base values; MD-1 conventional vs MD-5 AI-native)

| Event | Freq/acct-yr | Expertise | Human min MD-1 | Human min MD-5 | $/acct MD-1 | $/acct MD-5 | Failure lifecycle cost (MD-5) |
|---|---|---|---|---|---|---|---|
| E01 Account opening (agreement and fund set-up) | 0.12 | ops | 2.52 | 0.31 | 3.82 | 0.64 | $70 |
| E02 Identity verification | 0.12 | ops | 0.48 | 0.13 | 1.16 | 0.66 | $179 |
| E03 Contribution receipt and posting (cash ACH check securities) | 2.5 | ops | 12.00 | 1.26 | 28.73 | 13.22 | $92 |
| E04 Contribution attribution (pooled receipt to fund) | 2.5 | ops | 6.00 | 1.98 | 10.92 | 4.74 | $177 |
| E05 Asset liquidation and complex noncash assets | 0.003 | accounting | 2.16 | 1.27 | 4.42 | 3.22 | $3,751 |
| E06 Investment allocation | 1 | ops | 1.50 | 0.28 | 2.46 | 0.71 | $138 |
| E07 Charity discovery (assisted search) | 9 | ops | 2.70 | 1.02 | 5.89 | 3.55 | $22 |
| E08 Charity vetting (transaction-time check 180-day renewal and event monitoring) | 9 | compliance | 49.95 | 3.36 | 82.98 | 11.64 | $1,423 |
| E09 Grant recommendation intake | 9 | ops | 9.00 | 0.96 | 14.40 | 2.45 | $29 |
| E10 Grant approval (eligibility purpose and nonstandard grantee review) | 9 | compliance | 55.80 | 25.30 | 88.26 | 42.63 | $465 |
| E11 Payment processing (ACH check wire) | 9.045 | ops | 12.66 | 5.36 | 20.27 | 10.25 (+$14.92 rails) | $105 |
| E12 Payment failures (returns uncashed voids reissue) | 9.045 | ops | 2.70 | 1.44 | 4.83 | 3.84 | $92 |
| E13 Reconciliation (bank custodian ledger; monthly close) | 12.5 | accounting | 10.00 | 2.66 | 17.76 | 6.88 | $328 |
| E14 Statement generation and acknowledgments (incl. fee billing) | 1 | ops | 4.00 | 0.35 | 7.40 | 2.12 | $46 |
| E15 Customer communication (human-handled contacts) | 0.5 | ops | 5.00 | 4.82 | 8.46 | 8.37 | $59 |
| E16 Advisor administration (advisor onboarding fee schedules rep codes) | 0.1 | ops | 0.90 | 0.34 | 1.48 | 0.69 | $92 |
| E17 Account changes (address advisor bank contact) | 0.3 | ops | 1.80 | 0.36 | 2.88 | 0.78 | $89 |
| E18 Successor administration (death succession) | 0.02 | ops | 1.20 | 0.99 | 2.39 | 2.11 | $722 |
| E19 Fraud investigation (account takeover payment redirection) | 0.002 | compliance | 0.36 | 0.22 | 3.12 | 2.43 | $23,669 |
| E20 Compliance exceptions (sanctions alerts incidents) | 12.5 | compliance | 2.00 | 0.18 | 3.30 | 0.53 | $1,361 |
| E21 Regulatory and governance reporting | per sponsor | controller | 4800 / 2640 min per sponsor-year | | | | |
| E22 Audit preparation (sponsor audit SOC bridge) | per sponsor | controller | 7200 / 7200 min per sponsor-year | | | | |
| E23 Sponsor onboarding and configuration upkeep | per sponsor | implementation | 7200 / 3600 min per sponsor-year; one-time 36000 / 18000 min | | | | |
| E24 Data migration | per sponsor | implementation | one-time 18000 / 9000 min + 6 / 2 min per account | | | | |
| E25 Account closure (final grants transfers residual) | 0.02 | ops | 0.60 | 0.17 | 0.94 | 0.32 | $187 |

(Generated from `data/model-outputs/event-costs-by-mode.csv`; sponsor-level rows show conventional / AI-native minutes.) Totals: **183 human minutes per account-year conventional vs 53 AI-native** (revision 1 said 26; PR #87 found ~30 at steady state with a floor near 12, so this revision is more conservative than both).

## 3. Expertise, controls and external costs

Required expertise and controls per event are in the register. External costs that do not fall with automation: identity checks ($3 per new account), securities transfer costs (~$10 per transfer), complex-asset appraisal ($350), fraud investigation costs ($600 per attempt), rails ($14.92 per account at 9 payments; sponsor pass-through). Infrastructure is $25 per account-year owned (range $15-45) or $81 licensed software for conventional administrators.

## 4. Where the cost concentrates

| Rank | Conventional (MD-1) | Share | AI-native (MD-5) | Share |
|---|---|---|---|---|
| 1 | Grant approval | 24% | Grant approval | 27% |
| 2 | Charity vetting | 22% | Payment processing incl. rails | 16% |
| 3 | Reconciliation + close | 10% | Contribution posting | 8% |
| 4 | Payment processing | 9% | Reconciliation + close | 8% |
| 5 | Contribution posting | 8% | Charity vetting | 7% |
| | Top five | **73%** | Top five | **67%** |

**A small number of events drives cost.** Conventionally, two judgement events (approval and vetting) are 46% (CLM-012). After redesign, the residual is dominated by the irreducible judgement in grant approval (sponsor-reserved and 4967 cases), rails and securities transfer costs that automation does not touch.

## 5. Successful versus failed events

The lifecycle cost of a failed event dwarfs the cost of a successful one: a successful grant approval costs about $4.33 in AI-native mode, a failed one about $465; a successful vetting check about $0.76, a payment to an ineligible recipient about $1,423 (counsel, recovery, 4966 exposure); a fraud attempt that succeeds about $23,700. **Expected failure cost is about 19% of AI-native event cost against about 9% conventionally** (base): as routine work disappears, failures become the larger share, so prevention matters more than throughput ([10](10-zero-touch-administration-economics.md)).

## 6. Can input design eliminate whole categories?

| Category | Mechanism | Effect in model | Evidence |
|---|---|---|---|
| Unidentified contributions | Notification-first structured intents; unique fund reference or virtual account | −60% attribution touches and failures | INFERENCE (FIE: attribution is the main exception, SRC-004) |
| Vetting rework | Change-driven monitoring with evidence expiry | −50% | INFERENCE ([05](05-charity-registry-economics.md)) |
| Approval exceptions | Closed charity picker; purpose taxonomy; policy rules evaluated at recommendation time | −40-50% | ASSUMPTION |
| Payment failures | Verified destinations; e-payment enrolment; positive pay | −30-50% | INFERENCE (PR #88) |
| Fraud loss | Callback to aged contacts; bank-change holds | −70% of losses (×0.5 base prevention scale) | INFERENCE. Note: Nacha's 2026 risk-management rules make fraud monitoring **mandatory** for Originators and TPSPs (CHL-038); the lever here is effectiveness, not whether to do it |
| Paper | In-app agreement acceptance; IRS data instead of determination letters | eliminated (14 of 115 ingestion workflows, SRC-004) | INFERENCE |

Customer incentives (e.g. no fee for e-payment enrolment; faster grants for structured contributions) and upstream integrations (custodian feeds with fund keys) are the levers; they require sponsor and partner cooperation, which is a commercial dependency, not a technical one.
