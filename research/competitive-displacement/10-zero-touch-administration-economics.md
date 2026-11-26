# 10 - Zero-touch administration economics

Status: research (2026-11-26), **revision 2** after the adversarial review ([20](20-adversarial-review.md)). Model results: [results.md](model/out/results.md) §1-8; [saving-decomposition.csv](data/model-outputs/saving-decomposition.csv); [prevention-vs-speed.csv](data/model-outputs/prevention-vs-speed.csv); [tornado.csv](data/model-outputs/tornado.csv); [stress.csv](data/model-outputs/stress.csv). Every figure is conditional on labelled inputs; none is measured. Monte Carlo P50 and P90 are given beside base values, as the CFO reviewer asked (CHL-028).

## Answer in brief

1. **Unbound can run at a much lower variable cost than conventional administration, but not at a fundamentally lower total cost at entry scale.** Human time falls from about 183 to about 53 minutes per account-year and vendor variable cost from about $397 to $147 (incl. $25 infrastructure, labour at 75% utilisation). Owning a controlled platform roughly doubles fixed cost, so break-even at 20 bps is about **$1.9B base / $2.5B P50 / $4.3B P90** for AI-native administration against $3.9B base / $4.4B P50 (never in 29% of draws) for conventional administration on licensed software.
2. **Against an automated incumbent the gap is small.** Mature incumbents already run deterministic workflow and automated vetting (Ren's own release; CHL-003). Against workflow automation (MD-3) the AI-native vendor-variable gap is about $71 per account-year; against exception-driven administration (MD-4) it is **about $11, and MD-4 breaks even lower ($1.84B) than MD-5 ($1.92B)** once AI oversight cost is included.
3. **AI is a small part of the saving.** Of the ~$194 per account-year event-cost reduction from conventional to AI-native, deterministic workflow gives ~$124, exception-only design ~$39, prevention ~$20 (at half efficacy) and AI on residual exceptions ~$11 (**about 6%**) (CLM-011, revised).
4. **Prevention still beats speed** wherever an upstream lever exists, but its value depends on bank, custodian and sponsor cooperation, so the base case assumes half efficacy.
5. **The structurally cheaper position for the vendor is not to carry the event labour**: technology-only licensing (MD-6) breaks even at about $0.96B of 20 bps-equivalent revenue (P50 $1.15B), or about **36k accounts at $81 per account**. The sponsor then carries the labour at lower efficiency, so the *system* cost is higher than AI-native administration ($197 vs $167 variable per account).

## 1. Seven operating modes (base; 5 sponsors)

| Mode | Human min/acct-yr | Vendor variable $/acct | System variable $/acct | Vendor fixed | Build | System $/acct @10k accts | @40k accts |
|---|---|---|---|---|---|---|---|
| MD-1 Conventional manual | 183 | 397 | 417 | $1.18M | $0 | 576 | 457 |
| MD-2 Conventional + AI assistance | 156 | 370 | 390 | $1.35M | $0.1M | 558 | 432 |
| MD-3 Workflow automation | 100 | 217 | 238 | $2.20M | $1.94M | 491 | 301 |
| MD-4 Exception-driven (no AI) | 62 | 158 | 178 | $2.20M | $1.94M | 430 | 241 |
| MD-5 AI-native with deterministic controls | 53 | 147 | 167 | $2.50M | $1.94M | 439 | 235 |
| MD-6 Technology-only licensing | 53 (sponsor-borne, ×1.4) | 31 | 197 | $1.80M | $1.60M | 399 | 248 |
| MD-7 Hybrid licensing + exception administration | 53 (60% vendor) | 99 | 179 | $2.20M | $1.75M | 421 | 240 |

System variable cost adds sponsor-borne labour (×1.4 efficiency penalty in licensing modes; CHL-058), sponsor-reserved decisions and pass-through rails. In licensing modes the vendor carries all AI compute.

## 2. Break-even average billable assets

**Operating break-even (base; $250k balance; 5 sponsors)**

| Mode | 5 bps | 10 bps | 15 bps | 20 bps | 25 bps | 30 bps |
|---|---|---|---|---|---|---|
| MD-1 | never | never | never | $3.86B | $1.75B | $1.13B |
| MD-3 | never | $19.4B | $4.02B | $2.24B | $1.55B | $1.19B |
| MD-4 | never | $6.85B | $2.90B | $1.84B | $1.35B | $1.06B |
| MD-5 | never | $6.58B | $2.98B | $1.92B | $1.42B | $1.13B |
| MD-6 | $4.80B | $2.06B | $1.31B | $0.96B | $0.76B | $0.63B |
| MD-7 | $22.4B | $3.86B | $2.11B | $1.45B | $1.11B | $0.90B |

**Fully loaded** (build, $125k CAC per sponsor and onboarding amortised over 5 years; CHL-024): MD-5 at 20 bps **$2.33B**; MD-6 $1.23B; MD-1 $4.49B. Full grid in [results.md](model/out/results.md) §2a.

**Monte Carlo, MD-5** (independent draws / correlated ρ=0.5): at 10 bps P50 $10.2B, and the fee never covers variable cost in 20% / 25% of draws; at 20 bps P10-P50-P90 $1.87B-$2.48B-$4.25B (correlated P90 **$7.26B**); at 30 bps $1.13B-$1.41B-$1.94B. Plan against the correlated tails (CHL-026, CHL-108).

**Balance.** At a $100k average balance MD-5 needs $5.1B at 20 bps; at $500k, $1.59B. The industry-wide average is about $141k (CHL-083), below the comfortable zone for any bps-priced administration.

## 3. Where the saving comes from

| Step | Saving $/acct | Minutes saved |
|---|---|---|
| AI assistance on conventional touches (MD-1→MD-2; alternative path) | 27 | 28 |
| Deterministic workflow on structured events (MD-1→MD-3) | 124 | 84 |
| Exception-only design for all events, no AI, no prevention (MD-3→MD-4) | 39 | 26 |
| Prevention mechanisms at half efficacy | 20 | 11 |
| AI on residual exceptions (MD-4→MD-5) | 11 | 9 |

Two caveats from the economist stand. MD-3's touch rates are AI-native-column targets, not demonstrated deterministic rates (CHL-103), and an entry-year ramp would raise every touch rate. Both are covered only by the touch-multiplier range (0.6-2.0) and the stress below.

## 4. Correlated pessimistic stress (20 bps)

Stress settings: AI factor 0.88, touches ×1.5, minutes ×1.3, no automation failure benefit, fixed cost ×1.15.

| Mode | Base break-even | Stress break-even | Minutes base → stress |
|---|---|---|---|
| MD-1 | $3.86B | $4.29B | 183 → 183 |
| MD-4 | $1.84B | $2.74B | 62 → 117 |
| MD-5 | $1.92B | $2.79B | 53 → 103 |
| MD-6 | $0.96B | $1.11B | 53 → 103 |
| MD-7 | $1.45B | $1.87B | 53 → 103 |

Under stress AI-native still beats conventional administration, but it loses its edge over exception-driven administration. **Licensing is the least sensitive mode**, because the vendor's economics do not depend on handling minutes.

## 5. Prevention versus faster processing (MD-5, $ per account-year, half efficacy)

| Event | Prevention value | AI speed value |
|---|---|---|
| Grant approval (pre-validated policy rules) | 5.96 | 6.05 |
| Charity vetting (change-driven monitoring with expiry) | 3.15 | 0.72 |
| Reconciliation (single ledger; internal breaks only, CHL-059) | 2.29 | 0.46 |
| Contribution attribution (notification-first intent) | 1.67 | 0.43 |
| Customer communication (self-service status) | 1.43 | 0.93 |
| Payment processing (e-payment enrolment) | 1.27 | 0.94 |

## 6. Sensitivity (tornado, MD-5, 20 bps)

| Driver | Break-even range |
|---|---|
| Average balance | $1.59-5.11B |
| Activity frequency (includes the rebound from cheaper grants, CHL-106) | $1.69-3.03B |
| **Fixed cost** | $1.57-2.81B |
| Native touch rate | $1.76-2.41B |

Then minutes per touch, sponsor count, utilisation and prevention. **Fixed cost and balance dominate; labour efficiency is second-order.**

## 7. The economist's check on AI productivity claims

- The base AI factor is now 0.85, from field evidence (~14% faster in customer support; ~3% of hours in administrative data), not the 0.6 lab figure (CHL-101). At 0.97 the AI step is worth close to nothing per account-year (the economist measured about −$0.2 under the revision-1 structure).
- AI oversight and model-risk management ($0.1-0.2M a year) are now in fixed cost (CHL-104). At entry scale they cost more than the AI saves; AI pays for itself only above roughly 26k accounts.
- Human accountability is unchanged in every mode: sponsor-reserved decisions, a named compliance owner, three-person release and independent reconciliation.
- Not modelled:
  - FTE step functions by expertise pool beyond the utilisation factor (CHL-109, partly accepted);
  - per-tenant infrastructure floors by isolation profile (CHL-064, recorded);
  - systemic batch failures (CHL-061, recorded as a risk).

## 8. What this means

AI-native administration is a **cost-structure improvement over conventional administration and roughly at parity with a well-automated incumbent**. Its advantage comes from deterministic design and prevention, which incumbents can adopt too. The economically robust position for an entrant is **licensing**, which is insensitive to handling minutes. That turns the question into one of distribution, not technology ([11](11-institutional-distribution.md), [14](14-alternative-enterprise-models.md)).
