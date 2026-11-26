# 10 - Zero-touch administration economics

Status: research (2026-11-26). Model results: [results.md](model/out/results.md) §1-8; [saving-decomposition.csv](data/model-outputs/saving-decomposition.csv); [prevention-vs-speed.csv](data/model-outputs/prevention-vs-speed.csv); [tornado.csv](data/model-outputs/tornado.csv). Every figure is conditional on labelled inputs (ASSUMPTION / INFERENCE); none is measured.

## Answer in brief

1. **Unbound can operate at a fundamentally lower variable cost** than conventional administration: about 26 human minutes and **$85 vendor variable cost per account-year** (incl. $25 infrastructure) against 183 minutes and $324 (incl. $81 licensed software) (CLM-037).
2. **But it does not have a fundamentally lower total cost at entry scale.** Owning the platform raises fixed cost (about $2.3M a year against $1.2M for a conventional administrator on licensed software). Break-even at 20 bps falls only from about $2.1B to $1.5B (base) and the Monte Carlo P50 from $2.4B to $1.7B (CLM-013).
3. **Most of the saving does not come from AI.** Of the ~$183 per account-year event-cost saving, deterministic workflow gives ~$102, exception-only design ~$29, prevention ~$34 and AI on residual exceptions ~$17 (≈10%) (CLM-011).
4. **Preventing exceptions is worth more than processing them faster** wherever an upstream lever exists; AI speed matters only in judgement-heavy events (grant approval, complex assets, succession).
5. The **cheapest mode for the vendor is not administration at all**: technology-only licensing (MD-6) breaks even at about $0.85B at 20 bps-equivalent, or ~30k accounts at $81 per account (CLM-014), because the sponsor carries the event labour.

## 1. Seven operating modes (base; 5 sponsors)

| Mode | Human min/acct-yr | Vendor variable $/acct | System variable $/acct | Vendor fixed | Build | System $/acct @10k accts | @40k accts |
|---|---|---|---|---|---|---|---|
| MD-1 Conventional manual | 183 | 324 | 344 | $1.18M | $0 | 493 | 381 |
| MD-2 Conventional + AI assistance | 110 | 256 | 276 | $1.25M | $0.1M | 426 | 313 |
| MD-3 Workflow automation | 95 | 165 | 185 | $2.20M | $1.94M | 430 | 247 |
| MD-4 Exception-driven | 43 | 102 | 122 | $2.20M | $1.94M | 365 | 183 |
| MD-5 AI-native with deterministic controls | 26 | 85 | 105 | $2.30M | $1.94M | 348 | 166 |
| MD-6 Technology-only licensing | 26 (sponsor-borne) | 27 | 105 | $1.60M | $1.60M | 278 | 148 |
| MD-7 Hybrid licensing + exception administration | 26 (60% vendor) | 61 | 105 | $1.95M | $1.75M | 313 | 157 |

System variable cost adds sponsor-borne labour, sponsor-reserved decisions (2.7-7 min/account) and pass-through rails. MD-5, MD-6 and MD-7 have the same system cost: they differ only in who carries it.

## 2. Break-even average billable assets (base; $250k balance; 5 sponsors)

| Mode | 5 bps | 10 bps | 15 bps | 20 bps | 25 bps | 30 bps |
|---|---|---|---|---|---|---|
| MD-1 | never | never | $7.24B | $2.11B | $1.23B | $0.87B |
| MD-2 | never | never | $3.14B | $1.53B | $1.01B | $0.76B |
| MD-3 | never | $7.22B | $2.92B | $1.83B | $1.33B | $1.05B |
| MD-4 | $26.6B | $4.10B | $2.22B | $1.52B | $1.16B | $0.93B |
| MD-5 | $15.1B | $3.68B | $2.10B | $1.46B | $1.13B | $0.91B |
| MD-6 | $4.08B | $1.80B | $1.15B | $0.85B | $0.67B | $0.55B |
| MD-7 | $7.91B | $2.68B | $1.62B | $1.16B | $0.90B | $0.74B |

Monte Carlo (balance, sponsors, rates, touch rates, AI factor, prevention, fixed costs sampled), MD-5: 10 bps P10/P50/P90 $3.6B / $4.9B / $10.9B; 20 bps $1.48B / $1.74B / $2.21B; 30 bps $0.92B / $1.06B / $1.25B. At 5 bps the fee fails to cover variable cost in 40% of draws. Full grid in [break-even-grid.csv](data/model-outputs/break-even-grid.csv) and [15](15-capital-and-break-even-reassessment.md).

**Balance dominates.** At a $100k average balance MD-5 needs $2.11B at 20 bps; at $500k it needs $1.33B. Conventional administration (MD-1) never breaks even on $100k balances at any fee up to 30 bps. This reproduces PR #86's finding that a flat bps fee is wrong for low-balance books.

## 3. Where the saving comes from

| Step | Saving $/acct | Minutes saved |
|---|---|---|
| AI assistance on conventional touches (MD-1→MD-2; alternative path) | 67.9 | 73.3 |
| Deterministic workflow on structured events (MD-1→MD-3) | 102.4 | 88.4 |
| Exception-only design for all events, no AI, no prevention (MD-3→MD-4) | 29.4 | 26.3 |
| Prevention mechanisms (upstream input design) | 33.5 | 25.3 |
| AI on residual exceptions (MD-4→MD-5) | 17.5 | 17.3 |

The AI-assistance path (MD-2) is real but smaller than redesign, and it is the step most exposed to the unmeasured AI factor (HYP-008). Its value lies in deployment speed for an incumbent, which is why incumbents can copy it quickly (TIFIN's assistant, SRC-022).

## 4. Prevention versus faster processing (MD-5, $ per account-year)

| Event | Prevention value | AI speed value |
|---|---|---|
| Grant approval (pre-validated policy rules at recommendation time) | 10.48 | 8.75 |
| Charity vetting (change-driven monitoring with expiry) | 2.99 | 0.52 |
| Reconciliation (single ledger, continuous) | 1.93 | 0.36 |
| Contribution attribution (notification-first intent) | 1.90 | 0.53 |
| Customer communication (self-service status) | 1.59 | 1.78 |
| Payment processing (e-payment enrolment) | 1.50 | 1.91 |
| Fraud (callback to aged contacts; bank-change holds) | 0.95 | 0.05 |

Prevention dominates except where the residual work is judgement (succession, complex assets) or contact handling. If prevention fails entirely (prevention scale 0), MD-5 break-even rises from $1.46B to $1.56B: important, but not decisive.

## 5. Sensitivity

The tornado (break-even at 20 bps, per-unit parameters) ranks: average balance ($1.33-2.11B), activity frequency ($1.39-1.73B), sponsor count, native touch-rate multiplier ($1.42-1.56B), infrastructure per account, prevention, minutes per touch, labour rates. Labour-rate and AI-cost parameters barely move break-even: **in an AI-native design, fixed cost and balance, not labour efficiency, set viability.** Fixed-cost uncertainty is sampled in the Monte Carlo, not the tornado.

## 6. Economist's check on AI productivity claims

- The model assumes AI cuts minutes per touch by 40% (0.6 factor). No DAF time study exists (PR #87 RC-AN-015). At the pessimistic 0.9, the AI step is worth about $4 per account-year.
- Touch rates in AI-native mode (e.g. 9% of grant approvals, 1.2% of vetting checks) are calibrated to replay proxies (PR #88: 7.4-11.2% of lines routed to a person) but are not measured in production.
- Human accountability is not removed: sponsor-reserved decisions, a named compliance owner, three-person release and independent reconciliation sit in fixed cost and in sponsor-borne minutes in every mode.
- No double counting: rails are pass-through in every mode; prevention costs are charged per event; failure costs are counted once per event.

## 7. What this means

AI-native administration is a **cost-structure improvement, not a new cost structure**: it trades variable labour for fixed platform cost. It wins against conventional administrators only above roughly $1.5-2B of assets at 20 bps and $250k balances. The structurally cheaper position is to **not carry the event labour at all** (licensing) or to carry only exceptions (hybrid), which is a distribution question, not a technology question ([14](14-alternative-enterprise-models.md)).
