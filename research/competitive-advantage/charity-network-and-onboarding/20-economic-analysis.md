# 20 - Economic analysis: charity network and institutional onboarding

Status: research draft (2026-11-26). Not legal advice. Evidence classes per 01-research-methodology.md.

Agent: ECO. Model: `scripts/economic_model.py` (Python 3 stdlib, functional, deterministic). Inputs: `data/economic-parameters.csv` (91 parameters, each with an evidence class: 59 ASSUMPTION, 22 INFERENCE, 6 VERIFIED-FACT, 2 VENDOR-CLAIM, 1 RECOMMENDATION, 1 HYPOTHESIS). Output: `data/economic-scenarios-output.csv` (long format, about 30,000 rows; 648 sponsor scenarios plus unit-cost, platform and network rows). Sources: `data/sources-ECO.csv`. To reproduce, run `python3 scripts/economic_model.py`, then `--check` (recomputes and diffs; currently OK) and `--report` (prints the tables in section 6).

## Summary

- **Track A, the charity registry, is cheap in money and expensive in engineering.** Establishment costs about **$319k** ($113k-$1.07M), of which 2,600 engineering hours are 96%. Running it costs about **$75k a year** ($24k-$219k), and 63% of that is connector maintenance. Storage and compute cost about $10k a year, because IRS and OFAC data are free [ECO-006][ECO-007]. Spread over a network's grants, that is **$0.20 per grant at 700k grants a year** and $1.98 at 70k. The registry does not cost much to run. What makes it hard to copy is time, data rights and the evidence it builds up. (INFERENCE from ASSUMPTION hour estimates; Medium.)
- **Unit costs (base case).** One exception costs **$34** ($13-$124). Verifying a charity the first time costs **$1.35** and monitoring it costs **$1.46 a year**. Enrolling a charity for e-payment directly costs **$24** ($6-$91), which includes **$3.00** in instant-verification fees [ECO-003]. A check costs **$4.66 more than an ACH payment** ($1.41-$14.88) once bank fees and labour are both counted [ECO-001][ECO-002][ECO-004]. Unbound's own cost per grant is **$2.29 at a 33% check share and $1.80 at 10%**. The all-in cost per grant, including the sponsor's pass-through rail fees, falls from **$3.66 to $2.59**. (INFERENCE; Medium.)
- **For a sponsor, each grant moved from check to e-payment saves about $1.07.** About $0.59 is the sponsor's rail fee, a pass-through under CNV-PAY-001. About $0.48 is Unbound labour. For a 10k-account sponsor that is about $75k a year. It is real but small next to servicing revenue. **The economic value of the charity network is mainly a sales and onboarding asset, not a margin lever.** (INFERENCE; Medium.)
- **Onboarding at the entry segment fits inside a 20 bps fee.** A 10,000-account sponsor costs about **$335k** to onboard ($33.55 per account; $0.53 per migrated transaction). Payback is **about 1 month** and time to production is about **27 weeks** (18-39 depending on data quality). The fee could fall to 10 bps and payback would stay under 3 months, as long as balances are near the segment median of about $206k. (INFERENCE; Medium.)
- **Small sponsors are where onboarding stops paying for itself.** At 1,000 accounts, onboarding costs $98k-$268k (clean to poor data) and payback is 4-12 months at 20 bps. A low average balance of $76k, poor data, high grant volume, a 10 bps fee or the high cost case each push payback past 24 months, and together they make the sponsor uneconomic. In the stress case payback is **89 months** and the sponsor needs about $85k average balance just to break even. To recover cost, a 1k-account sponsor needs a **minimum annual fee of about $108k**. That matches the $100-110k "minimum fee for zero contribution" in `data/commercial-opportunity/servicing-economics/sponsor-model-economics.csv`. (INFERENCE; Medium.)
- **Processor-like mass books are uneconomic at any fee from 10 to 30 bps.** With 1M accounts at about $7k average balance, contribution is negative ($-28M at 20 bps) because account-based cost exceeds asset-based revenue. A bps fee does not work for these books. They need per-account pricing. (INFERENCE; High for direction.)
- **The biggest migration cost driver is importing full history.** CNV-EXP-002 requires each fund's full history to be imported. Exceptions in migrated transactions make up 41-53% of onboarding cost at 100k+ accounts, and that one rate (0.1%/1%/3%, ASSUMPTION) moves total onboarding cost by **2.7x-4.8x** between clean and poor data. **A fixed price is safe only behind a data-quality gate.** (INFERENCE; Medium.)
- **Recommendation (RECOMMENDATION; Medium).**
  - Include standard onboarding in the servicing fee when all of these hold:
    - at least about 5k accounts (or a contracted minimum annual fee);
    - modelled payback of 24 months or less;
    - a pre-contract data profile with at most 3% account exceptions and at most 1% transaction breaks;
    - no more than 1 custom integration;
    - an initial term of at least 36 months (base 60).
  - Charge a separate fixed fee, plus overage per exception and per custom integration, when the sponsor falls outside those bounds.
  - Decline, or price per account, for low-balance processor-like books.
- **Faster sales and earlier go-live are the largest modelled benefit, but they are a HYPOTHESIS.** If a proven network and a low-risk migration shorten time to revenue by 3 months, that is worth about **$0.9M for a 10k-account sponsor at 20 bps**. That is 10 times the direct e-payment savings. It is untested and should be measured in the pipeline.

## 1. Model structure and evidence discipline

**Cost classes.**

| Class | What it covers | Driver in the model |
|---|---|---|
| Platform fixed (Track A) | Registry establishment; annual ingestion, storage and DB; state data fees; sanctions vendor; connector maintenance | Not allocated to sponsors; reported per grant across the network (R2, R15) |
| Sponsor fixed (recurring) | Close/controller support, configuration, audit support, reporting. Base 324 h/yr at 1k accounts [ACT, servicing-economics 04], +50% per 10x accounts; plus maintenance of custom integrations | Per sponsor |
| Account-based | Statements, contacts, contributions, infra share: $15/$25/$45 per account-year (SPN placeholder; servicing-economics `cost-to-serve-parameters.csv`) | Accounts |
| Transaction-based | Per-grant screening, exceptions and payment operations labour, plus recipient monitoring and first-time verification | Grants and recipients |
| Pass-through (not Unbound cost) | ACH and check rail fees, positive pay. Under CNV-PAY-001 the sponsor is Originator, so these are sponsor costs; reported separately | Grants |
| One-time onboarding | Implementation, engineering config, standard and custom integrations, per-account and per-transaction migration, reconciliation, donor re-onboarding, charity e-pay enrolment, third-party set-up | Accounts, history, data quality, integrations |
| Revenue | Asset-based: AUA x bps (10/15/20/30; **20 bps is a working scenario only**) | Accounts x average balance |

**Scenario grid (648 scenarios).** The base cost case runs 432 scenarios across five dimensions:

- size: 1k, 10k, 100k or 1M accounts;
- grants per account:
  - low 5.6 (MS GIFT);
  - base 7.0 (median of 10 sponsors' published counts over Schedule D accounts, `summary-stats.json`; NPT FY2025 is 159,543 / 20,561 = 7.76, from `data/expanded-sponsor-activity-benchmarks-2026.csv`);
  - high 12.3 (Fidelity, `research/mission-2026-11-14/`);
- data quality: clean, typical or poor;
- average balance per size segment: low, base or high, taken from `data/commercial-opportunity/servicing-economics/segment-summary.csv` (sources are listed in the parameter file);
- fee: 10, 15, 20 or 30 bps.

The low and high cost cases add 216 scenarios at 20 bps.

**Recipients.** A sponsor's distinct recipients are grants divided by grants per recipient. Grants per recipient is 2.5 x (accounts/1000)^0.24, kept between 2.5 and 13.2, so it reproduces the Fidelity end-point of 13.2 at 1M accounts (A-ACT-005).

**Classification rule (RECOMMENDATION).**

| Class | Rule |
|---|---|
| INCLUDE_IN_FEE | Payback of 24 months or less |
| SEPARATE_ONBOARDING_FEE | Payback over 24 months but within the 60-month term |
| UNECONOMIC | Contribution of 0 or less, or payback longer than the term |

**What "contribution" means here.** It is the sponsor's direct contribution *before* Unbound's organisation fixed cost: $1.66-1.74M a year in `servicing-economics/03-organization-and-budget.md`. It is also before build capex and sales cost. So a high contribution margin does not mean the company is profitable. Break-even at the company level is in servicing-economics: about $1.1-1.5B AUA on operating costs alone.

**Reused parameters (not invented).**

| Parameter | Value | Source |
|---|---|---|
| Labour rate | $65.45/h | servicing-economics |
| Engineering rate | $118/h | CST-R03 |
| Implementation rate | $80/h | CST-R11 |
| Exception rate, with determination reuse | 4% | A-ACT-006 |
| Minutes per exception | 30 | A-ACT-007; Unbound uses 45, range 30-135 |
| AI-native activity minutes | ACH 0.1, check 1.2, status check 0.03 | `activity-minutes-typical.csv` |
| Return, break and contact parameters | see file | Unbound `requirements/discovery/2026-11-24-simplification-economics/model/parameters.json` |
| Database storage and instance costs | see file | CST-T01, CST-T03, CST-T04 |
| Onboarding hours | about 300 h | ACT |

**Reuse note.** The coordinator named `cost-register.csv` and `assumptions-register.csv` under `research/commercial-opportunity/servicing-economics/`. They are actually in `data/commercial-opportunity/servicing-economics/`, and they were used from there.

## 2. Track A: charity infrastructure costs

**Establishment (R2).** The registry needs connectors for the IRS EO BMF (free CSV by state and region, posted 2026-11-10) [ECO-007], TEOS/Pub78, auto-revocation and 990 XML (71 bulk ZIPs for 2019-2026) [ECO-006], plus OFAC (free; CST-D02) and 3-10 state registries. Indiana's paid SOS bulk data is noted at "$9,500+" in `unbound/research/charity-sources/INDIANA-SOURCE-PILOT.md` and needs to be reconfirmed. The work also covers entity resolution (UNB-KNOW-008/032) and tooling for the exception and hold queue (CNV-GRT-003/004). Base estimate: 2,600 engineering hours, $307k.

**Ongoing ingestion.**

| Item | Annual cost | Basis |
|---|---|---|
| Object storage (1 TB raw, append-only versions) | about $276 | $0.023/GB-month [ECO-008] |
| Registry database storage and backup (150 GB) | about $378 | Cost register |
| Dedicated HA registry database | $6.2k | CST-T01 |
| Batch compute | $3.6k | ASSUMPTION |
| Paid state data and optional commercial sanctions screening | $18k | ASSUMPTION |
| Connector maintenance for source drift (UNB-KNOW-026) | $47k (400 h) | ASSUMPTION |

The cost of running the registry is dominated by people, not cloud spend.

**Verification, exceptions and monitoring.**

| Item | Calculation | Base cost |
|---|---|---|
| First-time verification of a charity | compute + 4% x $34 exception | $1.35 |
| Exception | 30 min x $65.45 + $0.90 AI dossier | $34 |
| Monitoring per charity-year | 4% status events x exception cost | $1.46 |

Monitoring is event-driven, consistent with servicing-economics' about $1 per account-year for 180-day re-verification done by continuous monitoring.

**E-payment enrolment (direct, for charities not covered by a networked partner).**

- **Instant path:** account verification $1.50 plus ownership check $1.50 [ECO-003]. Plaid does not publish prices and bills Auth as a one-time fee per Item [ECO-012]. Third-party estimates of $1-2 are not used.
- **Fallback path:** micro-deposits ($0 at Stripe; about $1.50 for 3 ACH entries at Increase [ECO-002]) plus 10 minutes to review a charity-signed bank letter and call back (CNV-PAY-002).
- **Outreach:** 15 minutes in all cases.
- **Result:** $24 base ($6-$91). Labour dominates; vendor fees are 6-12%.
- **Bank changes:** re-verification costs $0.70 per enrolled charity-year.

**Payment rails (sponsor pass-through).**

| Rail | Unit cost | Source |
|---|---|---|
| ACH | $0.50 (AFP median $0.26-0.50) | [ECO-001][ECO-002][ECO-003] |
| Check print and mail | $1.04 (Lob) to $3.00 (Increase) | [ECO-004][ECO-002] |
| Check issue, AFP median | $2.01-4.00 | [ECO-001] |
| Postage | Forever stamp $0.82 since 2026-07-12 | [ECO-009] |
| Positive pay | $10-50 per account-month | [ECO-010][ECO-011] |

Uncashed checks (assumed 3%) add a reissue and 30 minutes of handling. Escheat handling is part of that 30-minute decision; no public per-item cost was found.

As a cross-check, Corpay's illustrative "not a benchmark" model gives $5.71 for a check and $1.67 for an ACH payment [ECO-013]. Our gap of $4.66 is close to its gap of $4.04.

**Network growth (R3).** Variable cost scales with the charities actually in use, not with the 1.9M rows in the BMF. At 50k charities in use it is about $193k a year. At 600k charities (Fidelity-scale breadth) it is $2.3M a year, plus a one-time $3.6M to enrol the charities not covered by partners. Two cost-reducing facts:

- Ratified CNV-EXP-002 reuses existing partner enrolments.
- CNV-GRT-003 allows cross-sponsor evidence reuse.

Without those, the direct-enrolment bill roughly doubles at 50% partner coverage.

## 3. Track B: onboarding costs

R4 and R5 give the per-sponsor figures. Patterns:

- **Fixed versus scaling cost.** Implementation, engineering configuration and integrations stay roughly fixed at **$118k-$154k** (800 engineering hours in the typical case: config 160 + 3 standard x 80 + 1 custom x 400). Per-account and per-transaction work dominates above 10k accounts.
- **Per-transaction migration.** It covers 7 years of history at (7 grants + 2 contributions) per account a year:

  | Accounts | Migrated transactions | Cost |
  |---|---|---|
  | 1k | 63k | $6.9k |
  | 10k | 630k | $69k |
  | 1M | 63M | $6.9M |

  Cost per migrated transaction falls from $2.46 (1k) to $0.21 (1M).
- **Charity enrolment at onboarding.** It is the second-largest scaling item: $97k at 10k accounts and $3.2M at 1M. It assumes 50% partner coverage and enrols 50% of the remainder in year 1. A mature registry with 50% reuse avoids half of it (R12).
- **Reconciliation.** Parallel month-end cycles (1/2/3 by data quality) plus 1% cutover breaks at 20 minutes each cost $5k-$231k. This is cheaper than expected because the per-transaction exceptions already carry most of the reconciliation burden.
- **Customer employee hours.** About 340 h at 1k accounts, 530 at 10k, 1,330 at 100k and 8,200 at 1M. The sponsor's cost is $24k-$574k. This cost is invisible in Unbound's P&L but decides buyer friction.
- **Time to production.** The base case is 25-31 weeks: 12 base weeks + 4 per custom integration + 4.35 per parallel cycle + 2 per decade of size. The range is 16-43 weeks (R7). No public benchmark was found; all inputs are ASSUMPTION.
- **Ongoing sponsor-specific maintenance.** It is $31k-$62k a year in recurring sponsor hours, plus $9.4k a year per custom integration.
- **Cross-check against earlier internal estimates.**
  - SPN placeholders in `cost-to-serve-parameters.csv` ($100k fixed + $15 per account) give $250k at 10k accounts and $1.6M at 100k. The model gives $335k and $1.67M, so they agree.
  - Unbound `parameters.json` uses `sponsor_onboarding_cost` $60k ($20k-$250k), flat across sizes. That **understates onboarding above about 5k accounts once the full-history import is costed**. The difference is flagged in section 7, not changed.

## 4. Can onboarding be fixed-price or included in the fee?

R6, R7, R8, R10, R11 and R14 answer this. Summary rule (RECOMMENDATION; Medium):

| Condition | Include in servicing fee | Separate fixed fee + overage | Uneconomic or reprice |
|---|---|---|---|
| Accounts | 10k or more (100% of 27 combinations at 15-30 bps; 23/27 at 10 bps) | 1k-5k with typical or poor data | 1k with low balance at 10 bps; processor-like books |
| Average balance at 20 bps | Above about $100k (small sponsor) | $76k-$100k | Below about $85k at 1k accounts with poor data and high grants; about $7k mass books at any bps |
| Data quality (pre-contract profile) | Account exceptions 3% or less; transaction breaks 1% or less | Up to 10% / 3%, with per-exception overage | Unknown or unprofiled data plus a fixed price |
| Custom integrations | 1 or fewer | 2-3, priced per integration ($47k build at 400 h; $9k a year to maintain) | Many custom integrations at a small sponsor |
| Term | 36 months or more (base 60) | 36 months or more, with a termination fee covering unrecovered onboarding | Under 24 months at a small sponsor |
| Cost case | Base | High-cost 1k sponsor: payback 72.5 months | n/a |

**Why a fixed price needs a gate.** The 1k-sponsor onboarding bill moves from $98k to $268k on data quality alone. The 1M sponsor's moves from $6.0M to $28.7M. Variance like that is safe to absorb only when it is measured before signing. The fee needed to bring payback back to 24 months is computed per scenario (`onboarding_fee_to_meet_include_threshold`). For uneconomic small sponsors it is $70k-$293k (R14). That is comparable to their entire first-year revenue, which is why a minimum annual fee is cleaner than an onboarding fee.

**Large sponsors.** A 20 bps fee on $19-194B is unrealistic. The model reports revenue per account ($388-413) against a break-even price of **$45-55 per account including amortised onboarding** at 10k accounts and above. The bargaining range at scale is therefore wide. The binding constraint is the buyer's price anchor: Ren at MS GIFT is about $737 per account, or 18.5 bps (A-ADV-001). Unbound's cost is not the constraint.

## 5. Economic value of each track to Unbound

| Value lever | Mechanism | Base magnitude (10k-account sponsor, 20 bps) | Evidence |
|---|---|---|---|
| E-payment adoption: sponsor saving | Check share falls from 33% to 10% (Fidelity is 67% electronic [ECO-005]) at $2.56 a grant in rail savings | $41k/yr, a pass-through benefit to the sponsor and a selling point | INFERENCE |
| E-payment adoption: Unbound labour | 2.1 minutes saved per check avoided | $34k/yr (about $0.48 per grant across the book) | INFERENCE |
| Unbound cost per grant | From $2.29 to $1.80 | 21% lower | INFERENCE |
| Network reuse at onboarding | A mature registry already holds 50% of the direct-enrol recipients | $48k once ($1.6M at 1M accounts) | ASSUMPTION |
| Registry scale economy | Fixed cost per grant: $1.98 at 70k grants, $0.20 at 700k, $0.02 at 7M (R15) | Favours being a shared multi-sponsor registry | INFERENCE |
| Sales-cycle / time-to-revenue reduction | 3 months saved x monthly contribution | $0.9M; $72k for a 1k sponsor | HYPOTHESIS |
| Lower onboarding cost through data-quality tooling | Moving a sponsor from poor to typical data | $256k at 10k accounts; $15.8M at 1M | INFERENCE |

**Interpretation.** Track A (the network) matters economically mainly because it removes switching friction. Charities do not have to re-enrol and sponsors do not lose e-payment coverage. That shortens the sale. Its direct savings per grant are modest. Track B (onboarding) is where costs vary most and where pricing risk lives. Investment in data profiling and automated history reconciliation pays back faster than investment in the registry itself.

## 6. Result tables (generated by `scripts/economic_model.py --report`)

All tables use the base cost case unless labelled. Dollar figures are rounded. "never" means contribution of 0 or less.

### R1 Unit costs (low / base / high cost case)

| Unit cost | Low | Base | High |
|---|---|---|---|
| cost_per_exception | $12.95 | $33.62 | $124 |
| verification_cost_per_new_charity | $0.26 | $1.35 | $9.97 |
| monitoring_cost_per_charity_year | $0.28 | $1.46 | $10.52 |
| epay_enrollment_cost_per_charity | $6.47 | $24.07 | $91.30 |
| bank_change_reverification_per_enrolled_year | $0.11 | $0.70 | $4.38 |
| ach_rail_cost_per_grant_passthrough | $0.26 | $0.53 | $0.80 |
| check_rail_cost_per_grant_passthrough | $1.05 | $3.09 | $8.48 |
| ach_labour_cost_per_grant | $0.04 | $0.19 | $0.93 |
| check_labour_cost_per_grant | $0.67 | $2.29 | $8.13 |
| screening_cost_per_grant | $0.27 | $1.40 | $10.19 |
| unbound_cost_per_grant_at_initial_check_share | $0.37 | $2.29 | $14.73 |
| unbound_cost_per_grant_at_target_check_share | $0.40 | $1.80 | $11.34 |
| allin_cost_per_grant_at_initial_check_share | $0.71 | $3.66 | $19.37 |
| allin_cost_per_grant_at_target_check_share | $0.79 | $2.59 | $12.37 |
| check_minus_ach_allin_per_grant | $1.41 | $4.66 | $14.88 |


### R2 Registry establishment and annual fixed cost

| Item | Low | Base | High |
|---|---|---|---|
| establish_engineering_hours | 1,140 | 2,600 | 7,600 |
| establish_engineering_usd | $113k | $307k | $1.04M |
| establish_state_data_usd | $0.00 | $9,500 | $25k |
| establish_backfill_compute_usd | $500 | $2,000 | $8,000 |
| establish_total_usd | $113k | $319k | $1.07M |
| annual_storage_usd | $202 | $654 | $2,508 |
| annual_infra_total_usd | $4,521 | $10k | $27k |
| annual_third_party_data_usd | $0.00 | $18k | $55k |
| annual_connector_maintenance_usd | $20k | $47k | $137k |
| annual_fixed_total_usd | $24k | $75k | $219k |


### R3 Network growth (base cost case): variable cost by charities in use

| Charities in use | Monitoring/yr | New verification/yr | New enrolment/yr | Bank-change/yr | Variable total/yr | One-time enrol of existing |
|---|---|---|---|---|---|---|
| 10,000 | $15k | $4,065 | $18k | $1,739 | $39k | $60k |
| 50,000 | $73k | $20k | $90k | $8,693 | $193k | $301k |
| 200,000 | $293k | $81k | $361k | $35k | $770k | $1.20M |
| 600,000 | $879k | $244k | $1.08M | $104k | $2.31M | $3.61M |


### R4 Representative sponsors at 20 bps (base grants, typical data, base balance, base cost)

| Metric | 1,000 accts | 10,000 accts | 100,000 accts | 1,000,000 accts |
|---|---|---|---|---|
| avg_balance | $182k | $206k | $194k | $194k |
| aua | $181.90M | $2.06B | $19.40B | $193.98B |
| grants_per_year | 7,000 | 70,000 | 700,000 | 7,000,000 |
| recipients | 2,800 | 16,112 | 92,717 | 533,529 |
| revenue | $364k | $4.13M | $38.80M | $387.96M |
| cost_account_based | $25k | $250k | $2.50M | $25.00M |
| cost_transaction_based | $21k | $190k | $1.77M | $17.01M |
| cost_sponsor_fixed | $31k | $41k | $52k | $62k |
| contribution | $287k | $3.65M | $34.47M | $345.89M |
| contribution_margin | 79% | 88% | 89% | 89% |
| cost_per_account | $76.91 | $48.15 | $43.27 | $42.07 |
| cost_per_grant_unbound | $10.99 | $6.88 | $6.18 | $6.01 |
| sponsor_passthrough_rail_cost | $10k | $96k | $960k | $9.60M |
| onb_total_unbound | $155k | $335k | $1.67M | $12.92M |
| onb_per_account | $155 | $33.55 | $16.69 | $12.92 |
| onb_per_migrated_txn | $2.46 | $0.53 | $0.26 | $0.21 |
| onb_engineering_hours | 800 | 800 | 800 | 800 |
| onb_charity_enrolment | $17k | $97k | $558k | $3.21M |
| onb_sponsor_hours | 338 | 530 | 1,330 | 8,205 |
| onb_sponsor_cost | $24k | $37k | $93k | $574k |
| time_to_production_weeks | 25 | 27 | 29 | 31 |
| payback_months | 6.5 | 1.1 | 0.6 | 0.4 |
| breakeven_bps_recurring | 4.2 | 2.3 | 2.2 | 2.2 |
| breakeven_bps_incl_onboarding_amortised | 5.9 | 2.7 | 2.4 | 2.3 |
| breakeven_balance_at_fee | $54k | $27k | $23k | $22k |
| revenue_per_account | $364 | $413 | $388 | $388 |
| breakeven_price_per_account_incl_onboarding | $108 | $54.86 | $46.61 | $44.66 |
| classification | INCLUDE_IN_FEE | INCLUDE_IN_FEE | INCLUDE_IN_FEE | INCLUDE_IN_FEE |


### R5 Onboarding components (base case, typical data)

| Component | 1,000 | 10,000 | 100,000 | 1,000,000 |
|---|---|---|---|---|
| onb_implementation | $24k | $36k | $48k | $60k |
| onb_engineering_config | $19k | $19k | $19k | $19k |
| onb_integration_standard | $28k | $28k | $28k | $28k |
| onb_integration_custom | $47k | $47k | $47k | $47k |
| onb_per_account_migration | $704 | $7,045 | $70k | $704k |
| onb_per_transaction_migration | $6,904 | $69k | $690k | $6.90M |
| onb_reconciliation | $5,454 | $10k | $32k | $231k |
| onb_donor_reonboarding | $1,711 | $17k | $171k | $1.71M |
| onb_charity_enrolment | $17k | $97k | $558k | $3.21M |
| onb_third_party | $5,000 | $5,000 | $5,000 | $5,000 |
| onb_total_unbound | $155k | $335k | $1.67M | $12.92M |


### R6 Fee sensitivity: payback months (base grants, typical data, base balance)

| Accounts | 10 bps | 15 bps | 20 bps | 30 bps |
|---|---|---|---|---|
| 1,000 | 17.7 (INCLUDE_IN_FEE) | 9.5 (INCLUDE_IN_FEE) | 6.5 (INCLUDE_IN_FEE) | 4.0 (INCLUDE_IN_FEE) |
| 10,000 | 2.5 (INCLUDE_IN_FEE) | 1.5 (INCLUDE_IN_FEE) | 1.1 (INCLUDE_IN_FEE) | 0.7 (INCLUDE_IN_FEE) |
| 100,000 | 1.3 (INCLUDE_IN_FEE) | 0.8 (INCLUDE_IN_FEE) | 0.6 (INCLUDE_IN_FEE) | 0.4 (INCLUDE_IN_FEE) |
| 1,000,000 | 1.0 (INCLUDE_IN_FEE) | 0.6 (INCLUDE_IN_FEE) | 0.4 (INCLUDE_IN_FEE) | 0.3 (INCLUDE_IN_FEE) |


### R7 Data quality: onboarding cost / payback months / time to production (20 bps, base)

| Accounts | Clean | Typical | Poor |
|---|---|---|---|
| 1,000 | $98k / 4.0 mo / 16 wk | $155k / 6.5 mo / 25 wk | $268k / 12.0 mo / 37 wk |
| 10,000 | $215k / 0.7 mo / 18 wk | $335k / 1.1 mo / 27 wk | $591k / 2.0 mo / 39 wk |
| 100,000 | $926k / 0.3 mo / 20 wk | $1.67M / 0.6 mo / 29 wk | $3.34M / 1.2 mo / 41 wk |
| 1,000,000 | $5.96M / 0.2 mo / 22 wk | $12.92M / 0.4 mo / 31 wk | $28.73M / 1.0 mo / 43 wk |


### R8 Balance case: contribution and payback (20 bps, typical, base grants)

| Accounts | Low balance | Base balance | High balance |
|---|---|---|---|
| 1,000 | $76k: $74k / 25.0 mo | $182k: $287k / 6.5 mo | $390k: $703k / 2.6 mo |
| 10,000 | $76k: $1.03M / 3.9 mo | $206k: $3.65M / 1.1 mo | $423k: $7.97M / 0.5 mo |
| 100,000 | $161k: $27.79M / 0.7 mo | $194k: $34.47M / 0.6 mo | $423k: $80.19M / 0.2 mo |
| 1,000,000 | $6,939: -$28.20M / never mo | $194k: $345.89M / 0.4 mo | $323k: $603.93M / 0.3 mo |


### R9 Grant volume: Unbound cost per account and contribution (20 bps, typical, base balance)

| Accounts | Low grants (5.6) | Base (7.0) | High (12.3) |
|---|---|---|---|
| 1,000 | $72.66/acct; $291k | $76.91/acct; $287k | $93.00/acct; $271k |
| 10,000 | $44.35/acct; $3.69M | $48.15/acct; $3.65M | $62.56/acct; $3.50M |
| 100,000 | $39.72/acct; $34.82M | $43.27/acct; $34.47M | $56.70/acct; $33.13M |
| 1,000,000 | $38.67/acct; $349.29M | $42.07/acct; $345.89M | $54.95/acct; $333.01M |


### R10 Cost case at 20 bps (typical data, base grants/balance): payback months

| Accounts | Low cost | Base cost | High cost |
|---|---|---|---|
| 1,000 | 1.9 ($54k) | 6.5 ($155k) | 72.5 ($524k) |
| 10,000 | 0.3 ($88k) | 1.1 ($335k) | 7.5 ($1.44M) |
| 100,000 | 0.1 ($365k) | 0.6 ($1.67M) | 4.1 ($7.70M) |
| 1,000,000 | 0.1 ($2.90M) | 0.4 ($12.92M) | 3.2 ($62.24M) |


### R11 Classification counts across 27 grants x quality x balance combinations (base cost)

| Accounts | Fee bps | INCLUDE_IN_FEE | SEPARATE_ONBOARDING_FEE | UNECONOMIC |
|---|---|---|---|---|
| 1,000 | 10 | 15 | 3 | 9 |
| 1,000 | 15 | 19 | 4 | 4 |
| 1,000 | 20 | 22 | 4 | 1 |
| 1,000 | 30 | 25 | 2 | 0 |
| 10,000 | 10 | 23 | 3 | 1 |
| 10,000 | 15 | 27 | 0 | 0 |
| 10,000 | 20 | 27 | 0 | 0 |
| 10,000 | 30 | 27 | 0 | 0 |
| 100,000 | 10 | 27 | 0 | 0 |
| 100,000 | 15 | 27 | 0 | 0 |
| 100,000 | 20 | 27 | 0 | 0 |
| 100,000 | 30 | 27 | 0 | 0 |
| 1,000,000 | 10 | 18 | 0 | 9 |
| 1,000,000 | 15 | 18 | 0 | 9 |
| 1,000,000 | 20 | 18 | 0 | 9 |
| 1,000,000 | 30 | 18 | 0 | 9 |


### R12 Value of the two tracks to Unbound (20 bps, base case, typical data)

| Value item | 1,000 | 10,000 | 100,000 | 1,000,000 |
|---|---|---|---|---|
| value_epay_sponsor_passthrough_saving_yr | $4,130 | $41k | $413k | $4.13M |
| value_epay_unbound_labour_saving_yr | $3,381 | $34k | $338k | $3.38M |
| value_network_enrolment_avoided_at_onboarding | $8,423 | $48k | $279k | $1.61M |
| value_sales_cycle_reduction | $72k | $912k | $8.62M | $86.47M |
| onboarding_fee_to_meet_include_threshold | $0.00 | $0.00 | $0.00 | $0.00 |
| term_contribution_after_onboarding | $1.28M | $17.90M | $170.68M | $1.72B |


### R13 Stress case: 1,000 accounts, high grants, poor data, low balance, 20 bps

| Metric | Value |
|---|---|
| avg_balance | $76k |
| aua | $75.68M |
| grants_per_year | 12,300 |
| recipients | 4,920 |
| revenue | $151k |
| cost_account_based | $25k |
| cost_transaction_based | $37k |
| cost_sponsor_fixed | $50k |
| contribution | $39k |
| contribution_margin | 26% |
| cost_per_account | $112 |
| cost_per_grant_unbound | $9.10 |
| sponsor_passthrough_rail_cost | $17k |
| onb_total_unbound | $293k |
| onb_per_account | $293 |
| onb_per_migrated_txn | $2.92 |
| onb_engineering_hours | 1,600 |
| onb_charity_enrolment | $30k |
| onb_sponsor_hours | 515 |
| onb_sponsor_cost | $36k |
| time_to_production_weeks | 37 |
| payback_months | 89.0 |
| breakeven_bps_recurring | 14.8 |
| breakeven_bps_incl_onboarding_amortised | 22.5 |
| breakeven_balance_at_fee | $85k |
| revenue_per_account | $151 |
| breakeven_price_per_account_incl_onboarding | $170 |
| classification | UNECONOMIC |


### R14 Non-included combinations for small sponsors (1,000 accounts, base cost)

| Fee bps | Grants | Data | Balance | Contribution/yr | Onboarding | Payback mo | Fee to reach 24 mo | Class |
|---|---|---|---|---|---|---|---|---|
| 10 | low | clean | low | $12k | $95k | 91.1 | $70k | UNECONOMIC |
| 10 | low | typical | low | $3,028 | $151k | 596.7 | $144k | UNECONOMIC |
| 10 | low | poor | low | -$16k | $261k | never | $261k | UNECONOMIC |
| 20 | low | poor | low | $60k | $261k | 52.4 | $142k | SEPARATE_ONBOARDING_FEE |
| 10 | low | poor | base | $90k | $261k | 34.7 | $81k | SEPARATE_ONBOARDING_FEE |
| 10 | base | clean | low | $8,225 | $98k | 143.3 | $82k | UNECONOMIC |
| 10 | base | typical | low | -$1,223 | $155k | never | $155k | UNECONOMIC |
| 20 | base | typical | low | $74k | $155k | 25.0 | $6,073 | SEPARATE_ONBOARDING_FEE |
| 10 | base | poor | low | -$20k | $268k | never | $268k | UNECONOMIC |
| 20 | base | poor | low | $56k | $268k | 57.8 | $157k | SEPARATE_ONBOARDING_FEE |
| 10 | base | poor | base | $86k | $268k | 37.3 | $96k | SEPARATE_ONBOARDING_FEE |
| 10 | high | clean | low | -$7,867 | $111k | never | $111k | UNECONOMIC |
| 10 | high | typical | low | -$17k | $172k | never | $172k | UNECONOMIC |
| 20 | high | typical | low | $58k | $172k | 35.3 | $55k | SEPARATE_ONBOARDING_FEE |
| 10 | high | poor | low | -$36k | $293k | never | $293k | UNECONOMIC |
| 20 | high | poor | low | $39k | $293k | 89.0 | $214k | UNECONOMIC |
| 10 | high | poor | base | $70k | $293k | 50.2 | $153k | SEPARATE_ONBOARDING_FEE |


### R15 Registry fixed cost per grant by network grant volume (annual fixed + establishment over 5 yrs)

| Network grants/yr | Low | Base | High |
|---|---|---|---|
| 70,000 | $0.67 | $1.98 | $6.20 |
| 700,000 | $0.07 | $0.20 | $0.62 |
| 3,000,000 | $0.02 | $0.05 | $0.14 |
| 7,000,000 | $0.01 | $0.02 | $0.06 |

## 7. Conflicts and tensions with ratified decisions and existing models

None of these is a conflict that requires a change. Each is flagged for the coordinator.

- **CNV-EXP-002 (full fund history at migration)** is the largest driver of onboarding cost: 41-53% at 100k+ accounts. It is not a conflict. But the cost depends on how the reconciliation is designed. Per-transaction exception handling is costly. Reconciling aggregates per period, with drill-down only where an aggregate breaks, is cheap. See requirement candidate ECO-RC-2.
- **CNV-PAY-001 / CNV-LEG-001 (sponsor originates; Unbound holds no funds).** E-payment rail savings accrue to the sponsor, not to Unbound's P&L. Unbound captures only labour savings (about $0.48 per grant shifted) and a stronger sales argument. Stripe and other facilitator payout products are cited only for price benchmarks. Using them as a rail would need a partner acting as the sponsor's agent.
- **The Unbound `parameters.json` value `sponsor_onboarding_cost` of $60k** (flat, amortised over 5 years) and the 05a "sponsor onboarding and exit" line ($3-117 per fund) understate onboarding for sponsors above about 5k accounts once full history and charity enrolment are costed. This model gives $33.55 per account at 10k and $16.69 at 100k, one-time. Recommend reconciling the two models.
- **CNV-ECO-004 entry segment (about 5k-50k funds) is supported.** In every grant, data and balance combination at 15 bps or above, the 10k-account sponsor is INCLUDE_IN_FEE. The 1k sponsor is where the fee structure has to change.

## Implications for Unbound

1. **Price onboarding by gate, not by hope.**
   - Require a paid or free pre-contract **data-quality profile** that measures:
     - account mapping exception rate;
     - historical transaction break rate;
     - number of custom integrations;
     - the share of the sponsor's recipients covered by networked partners.
   - Include onboarding in the fee only inside the thresholds in section 4.
2. **Set a minimum annual fee of about $100-110k** (or per-account floors) for sponsors under about 3-5k accounts. This model's break-even of $108k for a 1k sponsor agrees with servicing-economics. Do not rely on onboarding fees for small sponsors, because those fees exceed first-year revenue.
3. **Invest in Track B automation before registry breadth.** Each percentage point of transaction-exception rate costs about $69k per 10k-account sponsor (7 years of history at 10 minutes per exception). The registry costs about $75k a year in total.
4. **Use the network as a switching-cost neutraliser.**
   - Reuse partner enrolments (CNV-EXP-002) and registry evidence (CNV-GRT-003). Each one halves the direct-enrolment bill at onboarding.
   - Quote the e-payment saving (about $1.07 per grant shifted, roughly half to the sponsor) in proposals as a sponsor benefit.
5. **Do not bid bps-only on processor-like books** (average balance under about $20k). Account-based cost exceeds asset revenue at any fee from 10 to 30 bps.
6. **Large sponsors will negotiate to a per-account price.** The cost floor of $45-55 per account leaves wide room under Ren-like anchors of about $737 per account. The constraint there is capacity and risk, not unit cost.

## Candidate requirements (one line each)

- **ECO-RC-1 (refines CNV-EXP-002):** Before contract, the onboarding process SHALL produce a sponsor data-quality profile: account exception rate, historical transaction break rate, custom integration count, and partner-enrolment coverage of the sponsor's recipients. The profile SHALL feed a deterministic onboarding price and an estimated time to production.
- **ECO-RC-2 (refines CNV-EXP-002):** History migration SHALL reconcile aggregates per period and per fund first. Transaction-level exceptions SHALL be opened only where an aggregate breaks. Every imported transaction SHALL still be retained, append-only.
- **ECO-RC-3 (refines CNV-PAY-002 / UNB-CHAR):** The registry SHALL record verification method and cost class per destination (partner enrolment reused, instant ownership API, micro-deposit, bank letter) so that enrolment cost and reuse can be metered.
- **ECO-RC-4 (refines CNV-GRT-003):** The platform SHALL meter registry fixed and variable cost per grant and per charity in use, and SHALL report exception minutes per case, to replace ASSUMPTION parameters.
- **ECO-RC-5 (commercial; refines servicing-economics RC list):** Commercial terms SHALL support a minimum annual fee, overage per exception and per custom integration, and a termination fee covering unrecovered onboarding.
- **ECO-RC-6 (refines CNV-EXP-002):** Migration SHALL measure the sponsor's check share at baseline and track it monthly against a target, so that e-payment value is evidenced.

## Open questions / evidence gaps

1. **Migration exception rates and minutes.** Account and transaction exception rates, and the minutes to resolve them, have no public benchmark. All are ASSUMPTION, and they are the most sensitive inputs. An NDA time study on one real migration is needed.
2. **Time to production.** No public DAF migration timelines were found with scope stated. Runbook-based estimates are ASSUMPTION.
3. **Plaid Auth and Identity Match prices** are not public [ECO-012]. The sponsor-side price of Chariot Disbursements is not published: the page says only "at no cost" to nonprofits [ECO-005]. PayPal Grant Payments economics are not public.
4. **Check economics specific to DAF sponsors** (uncashed and escheat rates, positive-pay exception rates) are not published. The AFP survey is from 2022 and covers B2B payers [ECO-001].
5. **Partner coverage.** The share of a migrating sponsor's recipients already enrolled with a networked partner is unknown. 50% is ASSUMPTION, anchored on Fidelity's 67% electronic grant share [ECO-005].
6. **Size of the 990 XML corpus and paid state-data prices** were not measured. Storage is immaterial at any plausible size. State data prices (Indiana $9,500+) need reconfirmation.
7. **Sales-cycle reduction** (HYPOTHESIS) needs pipeline data: the months from first meeting to signature, and from signature to go-live, with and without network coverage.
8. **Company-level viability.** Contribution here excludes organisation fixed costs and build capex. Company-level break-even remains as in `research/commercial-opportunity/servicing-economics/` and `ai-native-capital-minimization/`.
