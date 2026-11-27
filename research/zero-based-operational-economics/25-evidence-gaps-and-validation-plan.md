# 25 — Evidence gaps and validation plan

## 1. Evidence status

| Class | Where | Comment |
|---|---|---|
| MEASURED-FACT | public-data sizes and change rates (one month); git and telemetry counts | small, bounded samples |
| PUBLISHED-PRICE | cloud, AI, messaging, identity, some data licences | list prices read 2026-11-27 |
| VERIFIED-FACT | statutes, regulations, Nacha rules, OFAC guidance; requirement texts | legal interpretation still needs counsel |
| INFERENCE | loaded labour rates; most frequencies; sizing | from cited baselines |
| ASSUMPTION | 93 of 183 activity rows; most fixed-cost lines; founder time; insurance; SOC fees (vendor claims) | no quotes, no time study |
| UNKNOWN | SAM extract sizes; bank-verification price; religious directories; some state fees | conservative placeholders |

**Nothing in this research is measured operational performance.**

## 2. Gaps ranked by economic leverage

| # | Gap | Leverage | Validation method | Earliest source |
|---|---|---|---|---|
| 1 | Handling minutes and exception rates, top 15 activities | ±$0.5M at $500M | timed synthetic operating year (OD-M-14), then pilot logs by activity ID | internal time study |
| 2 | Tier-2 trigger incidence and review minutes | 24% of inventory minutes | CNV-ECO-003 shadow replay on a sponsor's grant history | first sponsor data |
| 3 | Engineering hours per accepted change; maintenance load | ~$0.9M line | Praxis telemetry with human time and tokens per work item for 3 months | now |
| 4 | Per-sponsor close and audit-support hours by sponsor size | decides minimum viable sponsor | time study; sponsor finance interviews | first sponsor |
| 5 | Compliance alert rates and SLA distribution in December | compliance staffing | screening replay on real donor/charity names | pilot |
| 6 | Auditor reliance (SOC 1; deterministic release) | AUTH/CONTROL staffing, SOC scope | auditor walkthrough | first sponsor onboarding |
| 7 | Insurance limits and premiums | $45-145k | broker indication | owner decision OD-ZB-02 |
| 8 | Achievable fee for full administration; sponsor size distribution of buyers | break-even | sales conversations; RFPs | commercial pipeline |
| 9 | Stale-source share and connector drift | vetting false negatives, upkeep | run Beneficium connectors for 6 months | Beneficium build |
| 10 | December peak shape (daily) | operations and compliance peaks | sponsor daily contribution histories | first sponsor |

## 3. What to measure first when production operations exist (answer to Q25)

1. **Minutes and exception counts per activity ID** for the 15 activities in [04](04-operational-activity-inventory.md) §3 — instrumented at the case kernel.
2. **Tier-2 trigger rate and decision minutes** per trigger.
3. **Engineering hours per accepted change, review hours per change, defect escape rate.**
4. **Per-sponsor close, reconciliation and audit-support hours.**
5. **Queue age versus SLA in December**, by pool.
6. **Unidentified receipts and payment returns per 1,000 transactions** (prevention effectiveness).

Each measurement replaces a register value, changes its evidence class to MEASURED-FACT with sample size and period, and triggers an economic regression report ([22](22-continuous-economic-validation.md)).

## 4. Professional confirmations required (none commissioned)

Fourteen legal and audit matters in [06](06-human-control-obligations.md) §6, plus insurance (broker) and SOC fee quotes. Blocked by owner direction DF-ASR-2026-0D0F until OD-ZB-02 is decided.
