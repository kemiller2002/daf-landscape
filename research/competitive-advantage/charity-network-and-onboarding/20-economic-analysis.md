# 20 - Economic analysis: charity network and institutional onboarding

Status: research draft (2026-11-26). Not legal advice. Evidence classes per 01-research-methodology.md.

Agent: ECO. Model: `scripts/economic_model.py` (Python 3 stdlib, functional, deterministic). Inputs: `data/economic-parameters.csv` (106 parameters, each with an evidence class: 66 ASSUMPTION, 28 INFERENCE, 8 VERIFIED-FACT, 2 VENDOR-CLAIM, 1 RECOMMENDATION, 1 HYPOTHESIS). Output: `data/economic-scenarios-output.csv` (long format, about 42,000 rows; 672 sponsor scenarios plus unit-cost, platform and network rows).

**Revision 2 (2026-11-26), after adversarial review B.** This revision responds to `data/adversarial-findings-B.csv` (ADVB-05, 06, 07, 10, 11, 13; also 01, 04, 12). Changes:

- Added onboarding cost lines that were missing: rehearsals, Unbound legal work, a failed-migration reserve, and CAC.
- Added a buyer switching-TCO model: sponsor effort with a floor of at least 0.5 FTE, consultants, incumbent tail fees, auditor uplift, legal and communications.
- Added a history-depth dimension: 33 months, 7 years, and full history.
- Calibrated time to production against case evidence.
- Restated the termination recommendation and lowered confidence.

Section 0 records what changed and what survived. Sources: `data/sources-ECO.csv`. To reproduce, run `python3 scripts/economic_model.py`, then `--check` (recomputes and diffs; currently OK) and `--report` (prints the tables in section 6).

## Summary

- **Track A, the charity registry, is cheap in money and expensive in engineering.** Establishment costs about **$319k** ($113k-$1.07M), of which 2,600 engineering hours are 96%. Running it costs about **$75k a year** ($24k-$219k), and 63% of that is connector maintenance. IRS and OFAC data are free [ECO-006][ECO-007]. Spread over a network's grants, that is **$0.20 per grant at 700k grants a year** and $1.98 at 70k. (INFERENCE from ASSUMPTION hour estimates; Medium.)
- **Unit costs (base case).** One exception costs **$34**. Verifying a charity the first time costs **$1.35** and monitoring it costs **$1.46 a year**. Enrolling a charity for e-payment directly costs **$24**, of which about $3.00 is vendor fees [ECO-003]. A check costs **$4.66 more than an ACH payment**, all-in [ECO-001][ECO-002][ECO-004]. Unbound's cost per grant falls from $2.29 to $1.80 when the check share drops from 33% to 10%. (INFERENCE; Medium.)
- **The network is mainly a sales and switching asset, not a margin lever.** Moving a grant from check to e-payment saves about $1.07: about $0.59 is the sponsor's pass-through rail fee (CNV-PAY-001) and about $0.48 is Unbound labour. (INFERENCE; Medium.)
- **The 10k-account entry sponsor still absorbs onboarding, but the result comes from the revenue assumption.**
  - Unbound's onboarding cost is **$438k**: $43.76 per account, including rehearsals, legal and a 10% failure reserve.
  - CAC adds **$125k**.
  - Payback is **about 2 months at 20 bps**, 4.3 months at 10 bps, and **13 months at a $100 per-account price**.
  - Time to production is **33 weeks** (24-45). That is consistent with AEF's ~8.5 months from selection to live.
  - The conclusion depends on a fee of about $400 per account. With 66 of 106 parameters ASSUMPTION, **confidence is Low** (ADVB-13).
- **Small sponsors are worse than revision 1 showed (strengthened).**
  - At 1,000 accounts, acquisition plus onboarding costs $259k-$456k. Payback is 10.5-20 months at 20 bps and 37 months at 10 bps.
  - Low balance, poor data or high grant volume each push the sponsor out of INCLUDE_IN_FEE: 18 of 27 combinations include at 20 bps, 9 of 27 at 10 bps.
  - In the stress case payback is **149 months**.
  - The break-even price including CAC and onboarding is **about $142 per account a year**, so a 1k-account sponsor needs a **minimum annual fee of about $140k**. Servicing-economics put this at $100-110k, but it excluded CAC. (INFERENCE; Medium.)
- **Processor-like mass books are uneconomic at any fee from 10 to 30 bps.** At about $7k average balance, account-based cost exceeds asset revenue. (INFERENCE; High for direction.)
- **History depth and data quality are the onboarding cost drivers (strengthened).**
  - Per-transaction migration is the share of onboarding cost at 100k-1M accounts:
    - 46-58% with 20 years of ramped history;
    - 32-43% with 7 years;
    - 18-27% with 33 months.
  - Data quality alone moves onboarding cost **2.5x at 1k accounts and 6.2x at 1M**.
  - A fixed price is safe only behind a data-quality and history-availability gate. (INFERENCE; Medium.)
- **The buyer bears a switching cost comparable to Unbound's onboarding cost, and it is not in Unbound's P&L.** Base: **$170k (1k accounts), $280k (10k) and $846k (1M)**. High cost case with poor data: $0.9M-$6.2M. It includes:
  - sponsor staff of at least 0.5 FTE over the project;
  - consultants;
  - an incumbent tail fee (JCF paid Ren $417,742, the high case);
  - auditor uplift, legal and communications.

  Absorbing Unbound's own onboarding cost does not remove this barrier. Reducing it is where onboarding design creates competitive advantage. (INFERENCE; Medium.)
- **Commercial terms (RECOMMENDATION; Medium).**
  - Include standard onboarding in the fee only behind gates: modelled payback including CAC of 24 months or less; a pre-contract data profile; history available at source; at most 1 custom integration.
  - For sponsors outside the gates, charge onboarding **up front**. Do not recover it through exit penalties.
  - Any recovery on early exit is limited to straight-line unamortised onboarding that Unbound actually absorbed, published up front. There is **no** export fee, export is never conditioned on payment, and nothing is owed when the exit is caused by an Unbound breach.
- **Faster sales and earlier go-live are worth about $0.9M per 10k sponsor (HYPOTHESIS).** This value is still unmeasured.

## 0. Adversarial review B: dispositions and what changed

| Challenge | Verdict here | Change made |
|---|---|---|
| ADVB-05: omitted onboarding costs | **Accepted** | Unbound side: rehearsals (3 runs, 40 h each at 1k scale), Unbound legal ($15k), failure reserve (10% of direct cost; FFTC's $654.5k abandoned implementation, INFERENCE; akoyaGO 85% on time, VENDOR-CLAIM), CAC ($125k; servicing-economics ADV-005). Buyer side: incumbent tail fee (base $50k ASSUMPTION; high $417,742, the JCF payment to Ren for "previous donor portal support", VERIFIED-FACT via 10), auditor uplift, legal, communications. Service credits are folded into the reserve. Paid export from the incumbent is in the tail fee. The pre-contract assessment is part of implementation hours. |
| ADVB-06: sponsor effort undercounted | **Accepted** | Sponsor hours are now at least 0.5 FTE (scaled +50% per 10x accounts) over the whole time to production, plus controller approval per rehearsal, data clean-up and IT per custom integration. Result: 584 h at 1k accounts, 934 h at 10k, 9,016 h at 1M (was 338-8,205). Consultants: $115k base (990 VII-B lines $115k-$724k; high $362k). Scaled to 25% at 1k accounts. The $724k JCF SF Salesforce build is excluded as wider in scope than a DAF platform switch. A duty-by-duty model is left to the first measured migration. |
| ADVB-07: history depth | **Accepted** | History is now a dimension: short = 2.75 years (AEF pulled 33 months), mid = 7 (GWCF), full = 20 (15-26, Arizona 26) with a volume ramp of 8%/yr growth. Full is the default (R16). |
| ADVB-10: auditor uplift | **Partly accepted** | Added as buyer cost ($5k-$60k ASSUMPTION). Timing SOC 1 is outside this model. |
| ADVB-11: termination fee against exit symmetry | **Accepted** | The termination-fee recommendation is withdrawn. Replaced by up-front onboarding fees for out-of-gate sponsors, and at most a published straight-line unamortised recovery with no export conditionality (section 4, ECO-RC-5). |
| ADVB-13: confidence and time-to-production calibration | **Accepted** | Confidence on payback is lowered to Low. Payback is now also reported at $100 and $400 per-account prices. Time to production now includes rehearsal weeks and is calibrated to case evidence (section 3). |
| ADVB-01: R1 "no migration" against CNV-EXP-002 / CNV-ECO-003 | Noted (outside the model) | The economics assume migration is in scope, as ratified clauses require. A Release 1 without migration would leave the entry segment unaddressable. |
| ADVB-04: private-label programs | Noted | These are fund-by-fund transfers (CNV-ENT-002) and are not modelled. Their onboarding is not a platform migration. |
| ADVB-12: migration is not unique | Accepted for interpretation | Section 5 no longer implies that "having onboarding" differentiates. The value lies in a lower buyer TCO and verifiable outcomes. Ren markets set-up at "around $50,000" and "90-120 days" (VENDOR-CLAIM, ADVB-007), which is the price anchor for any onboarding fee. |

**Rejected or not changed, with reasons.** The challenge that the 10k INCLUDE_IN_FEE result is wrong is not upheld *as arithmetic*. Even with all added lines, onboarding plus CAC ($563k) is about 15% of one year's revenue at 20 bps. It is upheld *as to dependence*: the result rests on the revenue assumption. So confidence is lowered rather than the conclusion reversed.

**What survives, and at what confidence.**

| Conclusion | Status |
|---|---|
| Registry cost structure | Survives, Medium |
| Unit costs | Survive, Medium |
| Network value is modest per grant | Survives, Medium |
| Entry segment absorbs onboarding | Survives only conditional on price; Low |
| Small sponsors need minimum fees | Survives and strengthened: about $140k, Medium |
| Processor books uneconomic | Survives, High for direction |
| History and data quality dominate onboarding cost | Survives and strengthened, Medium |
| Termination-fee recommendation | Withdrawn |

## 1. Model structure and evidence discipline

**Cost classes.**

| Class | What it covers | Driver in the model |
|---|---|---|
| Platform fixed (Track A) | Registry establishment; annual ingestion, storage and DB; state data fees; sanctions vendor; connector maintenance | Not allocated to sponsors; reported per grant across the network (R2, R15) |
| Sponsor fixed (recurring) | Close/controller support, configuration, audit support, reporting. Base 324 h/yr at 1k accounts [ACT, servicing-economics 04], +50% per 10x accounts; plus maintenance of custom integrations | Per sponsor |
| Account-based | Statements, contacts, contributions, infra share: $15/$25/$45 per account-year (SPN placeholder; servicing-economics `cost-to-serve-parameters.csv`) | Accounts |
| Transaction-based | Per-grant screening, exceptions and payment operations labour, plus recipient monitoring and first-time verification | Grants and recipients |
| Pass-through (not Unbound cost) | ACH and check rail fees, positive pay. Under CNV-PAY-001 the sponsor is Originator, so these are sponsor costs; reported separately | Grants |
| One-time onboarding (Unbound) | Implementation, engineering config, standard and custom integrations, per-account and per-transaction migration (volume-ramped history), reconciliation, rehearsals, donor re-onboarding, charity e-pay enrolment, third-party set-up, legal, failure reserve; plus CAC per sponsor | Accounts, history, data quality, integrations |
| Buyer switching TCO (not Unbound) | Sponsor staff (at least 0.5 FTE over the project), consultants, incumbent tail fee, auditor uplift, legal, communications | Time to production, size, data quality |
| Revenue | Asset-based: AUA x bps (10/15/20/30; **20 bps is a working scenario only**) | Accounts x average balance |

**Scenario grid (672 scenarios).** The base cost case runs 432 scenarios across five dimensions, all with full history:

- size: 1k, 10k, 100k or 1M accounts;
- grants per account:
  - low 5.6 (MS GIFT);
  - base 7.0 (median of 10 sponsors' published counts over Schedule D accounts, `summary-stats.json`; NPT FY2025 is 159,543 / 20,561 = 7.76, from `data/expanded-sponsor-activity-benchmarks-2026.csv`);
  - high 12.3 (Fidelity, `research/mission-2026-11-14/`);
- data quality: clean, typical or poor;
- average balance per size segment: low, base or high, taken from `data/commercial-opportunity/servicing-economics/segment-summary.csv` (sources are listed in the parameter file);
- fee: 10, 15, 20 or 30 bps.

The low and high cost cases add 216 scenarios at 20 bps. A history family adds 24 more: short and mid history x 4 sizes x 3 data qualities, at base values and 20 bps.

**Recipients.** A sponsor's distinct recipients are grants divided by grants per recipient. Grants per recipient is 2.5 x (accounts/1000)^0.24, kept between 2.5 and 13.2, so it reproduces the Fidelity end-point of 13.2 at 1M accounts (A-ACT-005).

**Classification rule (RECOMMENDATION).**

| Class | Rule |
|---|---|
| INCLUDE_IN_FEE | Payback of onboarding **plus CAC** of 24 months or less |
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

R4, R5, R16 and R17 give the figures.

**Fixed versus scaling cost.** Implementation, engineering configuration and integrations stay roughly fixed at **$118k-$154k** (800 engineering hours in the typical case). Rehearsals add $8k-$20k, Unbound legal $15k, and the failure reserve 10% of direct cost. CAC ($125k, ASSUMPTION) is reported separately and included in payback. Per-account and per-transaction work dominates above 10k accounts.

**History depth (ADVB-07).** Default history is 20 years, ramped for 8% a year growth. That is about 10.6 full-volume years, at (7 grants + 2 contributions) per account a year.

| Accounts | Migrated transactions | Per-transaction migration cost |
|---|---|---|
| 1k | about 95k | $10k |
| 10k | about 954k | $105k |
| 1M | about 95M | $10.5M |

The share of onboarding cost that is per-transaction work depends on how much history the predecessor holds (R16):

| Accounts | 33 months (AEF) | 7 years | 20 years |
|---|---|---|---|
| 10k | 7% | 14% | 24% |
| 1M | 27% | 43% | 58% |

Where the predecessor holds less than full history (AEF's platform yielded 33 months), the gap has to be documented, not invented.

**Charity enrolment at onboarding.** This is unchanged: $97k at 10k accounts and $3.2M at 1M. It assumes 50% partner coverage (CNV-EXP-002) and enrols 50% of the remainder in year 1.

**Customer employee effort (ADVB-06).** Sponsor hours are now 584 at 1k accounts, 934 at 10k, 1,922 at 100k and 9,016 at 1M. Sponsor staff cost $41k-$631k. They are built from:

- an FTE floor of at least 0.5 over the project;
- controller approval for each rehearsal;
- data clean-up;
- IT work per custom integration.

**Buyer switching TCO (R17).** This excludes the fee paid to Unbound.

| Accounts | Base case | High cost, poor data |
|---|---|---|
| 1k | $170k | $0.9M |
| 10k | $280k | $1.4M |
| 1M | $846k | $6.2M |

At 10k accounts the buyer's own switching cost is about 64% of Unbound's onboarding cost. The case evidence in 10 (Hartford: 4 months of clean-up plus 2 months of dual run; consultant lines of $115k-$724k a year) shows this cost is real and is borne by the buyer.

**Time to production (ADVB-13).** It is now base weeks + custom integrations + 3 rehearsals x 2 weeks + parallel cycles x 4.35 + size.

| Case | Weeks |
|---|---|
| Clean 1k-account sponsor | 22 (about 5 months) |
| Typical 10k-100k sponsor | 33-35 (about 8 months) |
| Poor-data 1M sponsor | 49 |

Case evidence in 10:

- CF single-vendor conversions took 3-6 months from contract to system of record.
- AEF took about 8.5 months from selection to go-live.
- Arizona's multi-system rebuild took 18 months or more.
- NPT's 14-16 weeks and Ren's 90-120 days (VENDOR-CLAIM) cover new programs, not migrations.

The model now sits inside the observed range, and its low end is no longer below every case. Remaining caveat: no case reports elapsed time with full-history reconciliation.

**Ongoing sponsor-specific maintenance.** $31k-$62k a year in recurring sponsor hours, plus $9.4k a year per custom integration.

**Cross-check.**

- SPN placeholders ($100k + $15 per account) give $250k at 10k accounts. The model now gives $438k, higher because of full history, rehearsals and the reserve.
- Unbound's flat `sponsor_onboarding_cost` of $60k (`parameters.json`) understates onboarding above about 3k accounts.
- Ren markets program set-up at "around $50,000" (VENDOR-CLAIM, ADVB-007). That is a new-program price, not a migration price, but it anchors buyer expectations for any onboarding fee.

## 4. Can onboarding be fixed-price or included in the fee?

R6, R7, R8, R10, R11, R14 and R16 answer this. All paybacks include CAC. Summary rule (RECOMMENDATION; Low-Medium):

| Condition | Include in servicing fee | Separate up-front onboarding fee (fixed for scope, plus overage) | Uneconomic or reprice |
|---|---|---|---|
| Accounts and fee | 10k or more at 15 bps or above (26-27 of 27 combinations); 10k at 10 bps (21/27) | 1k at 20 bps with low balance, or any 1k sponsor at 10 bps | 1k with low balance and poor data, or high grants; processor-like books at any bps |
| Per-account price equivalent | About $250 or more per account at 10k+ accounts (payback 13 months at $100) | $100-250 | At or below cost (about $142 at 1k accounts, $45-60 at 10k+) |
| Data quality (pre-contract profile) | Account exceptions 3% or less; transaction breaks 1% or less | Up to 10% / 3%, with per-exception overage | Unprofiled data plus a fixed price |
| History availability | Source holds the required history, or gaps are documented | Reconstruction needed from secondary sources (priced as overage) | n/a |
| Custom integrations | 1 or fewer | 2-3, priced per integration ($47k build; $9k a year to maintain) | Many custom integrations at a small sponsor |
| Term and exit | Any term of 36 months or more, **no exit charge** | Onboarding paid up front, so no exit recovery is needed | n/a |

**Fixed price needs a gate.** Data quality alone moves the onboarding bill $134k-$331k at 1k accounts and $7.0M-$43.3M at 1M. History depth adds up to 1.9x at 1M. That variance is safe to absorb only when it is measured before signing. The fee needed to restore a 24-month payback for uneconomic small sponsors is $229k-$491k (R14). That is more than their first-year revenue, so a **minimum annual fee of about $140k** is cleaner.

**Exit symmetry (ADVB-11).** Revision 1 recommended a termination fee that recovered onboarding. That **contradicts** the exit-symmetry position in 10 and 11 and is withdrawn. Replacement conditions:

1. Onboarding that Unbound absorbs is recovered only through the servicing fee over time.
2. If any early-exit recovery is contracted, it is limited to the straight-line unamortised balance of the onboarding Unbound absorbed. The model reports it at 12 months ($450k for a 10k sponsor on a 60-month term) and at 36 months ($225k). The schedule is published in the proposal.
3. Export of all sponsor data in documented schemas is never conditioned on payment, carries no export fee, and starts within the same SLA whatever the payment status.
4. Nothing is owed when the exit follows an Unbound breach or SLA failure.

Where recovery at exit would be material, charging onboarding up front is the more honest structure. Unbound should not market "no lock-in" while contracting for it.

**Large sponsors.** A 20 bps fee on $19-194B is unrealistic. The break-even price including onboarding and CAC is **$46-59 per account** at 10k+ accounts, against Ren-like anchors of about $737 per account (A-ADV-001). The binding constraints are capacity, risk and the buyer's switching TCO, not Unbound's unit cost.

## 5. Economic value of each track to Unbound

| Value lever | Mechanism | Base magnitude (10k-account sponsor, 20 bps) | Evidence |
|---|---|---|---|
| E-payment adoption: sponsor saving | Check share falls from 33% to 10% (Fidelity is 67% electronic [ECO-005]) at $2.56 a grant in rail savings | $41k/yr (sponsor benefit) | INFERENCE |
| E-payment adoption: Unbound labour | 2.1 minutes saved per check avoided | $34k/yr | INFERENCE |
| Unbound cost per grant | From $2.29 to $1.80 | 21% lower | INFERENCE |
| Network reuse at onboarding | A mature registry already holds 50% of the direct-enrol recipients | $48k once ($1.6M at 1M accounts) | ASSUMPTION |
| Registry scale economy | Fixed cost per grant: $1.98 at 70k grants, $0.20 at 700k (R15) | Favours a shared multi-sponsor registry | INFERENCE |
| Lower buyer switching TCO | Each 100 sponsor hours or $50k of consultant spend avoided | Buyer TCO is $280k at base | INFERENCE |
| Sales-cycle / time-to-revenue reduction | 3 months saved x monthly contribution | $0.9M | HYPOTHESIS |
| Data-quality tooling | Moving a sponsor from poor to typical data | $358k at 10k accounts; $25M at 1M | INFERENCE |

**Interpretation.** Migration services are already sold by Ren, Give, akoyaGO, Foundant and others (ADVB-12). So "having onboarding" does not differentiate. Two things can:

- a **lower and more predictable buyer switching TCO**: gated fixed price, fewer sponsor hours, partner enrolments reused so charities are not re-enrolled;
- **verifiable outcomes**: a reconciliation proof, documented history gaps, freeze length and exit schemas.

Direct e-payment savings are modest. Investment in data profiling and automated history reconciliation pays back faster than investment in registry breadth.

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
| onb_total_unbound | $200k | $438k | $2.26M | $18.16M |
| cac_per_sponsor | $125k | $125k | $125k | $125k |
| acquisition_and_onboarding_total | $325k | $563k | $2.39M | $18.28M |
| onb_per_account | $200 | $43.76 | $22.61 | $18.16 |
| onb_per_migrated_txn | $2.09 | $0.46 | $0.24 | $0.19 |
| onb_engineering_hours | 800 | 800 | 800 | 800 |
| onb_charity_enrolment | $17k | $97k | $558k | $3.21M |
| onb_sponsor_hours | 584 | 934 | 1,922 | 9,016 |
| onb_sponsor_cost | $41k | $65k | $135k | $631k |
| buyer_switching_tco | $170k | $280k | $350k | $846k |
| time_to_production_weeks | 31 | 33 | 35 | 37 |
| payback_months | 13.6 | 1.9 | 0.8 | 0.6 |
| payback_months_onboarding_only | 8.3 | 1.4 | 0.8 | 0.6 |
| payback_months_at_100_per_account | 168.6 | 13.0 | 5.0 | 3.8 |
| payback_months_at_400_per_account | 12.1 | 1.9 | 0.8 | 0.6 |
| breakeven_bps_recurring | 4.2 | 2.3 | 2.2 | 2.2 |
| breakeven_bps_incl_onboarding_amortised | 7.8 | 2.9 | 2.5 | 2.4 |
| breakeven_balance_at_fee | $71k | $30k | $24k | $23k |
| revenue_per_account | $364 | $413 | $388 | $388 |
| breakeven_price_per_account_incl_onboarding | $142 | $59.41 | $48.04 | $45.73 |
| classification | INCLUDE_IN_FEE | INCLUDE_IN_FEE | INCLUDE_IN_FEE | INCLUDE_IN_FEE |


### R5 Onboarding components (base case, typical data)

| Component | 1,000 | 10,000 | 100,000 | 1,000,000 |
|---|---|---|---|---|
| onb_implementation | $24k | $36k | $48k | $60k |
| onb_engineering_config | $19k | $19k | $19k | $19k |
| onb_integration_standard | $28k | $28k | $28k | $28k |
| onb_integration_custom | $47k | $47k | $47k | $47k |
| onb_per_account_migration | $704 | $7,045 | $70k | $704k |
| onb_per_transaction_migration | $10k | $105k | $1.05M | $10.46M |
| onb_reconciliation | $5,454 | $10k | $32k | $231k |
| onb_donor_reonboarding | $1,711 | $17k | $171k | $1.71M |
| onb_charity_enrolment | $17k | $97k | $558k | $3.21M |
| onb_third_party | $5,000 | $5,000 | $5,000 | $5,000 |
| onb_rehearsals | $7,854 | $12k | $16k | $20k |
| onb_unbound_legal | $15k | $15k | $15k | $15k |
| onb_failure_reserve | $18k | $40k | $206k | $1.65M |
| onb_total_unbound | $200k | $438k | $2.26M | $18.16M |
| cac_per_sponsor | $125k | $125k | $125k | $125k |
| acquisition_and_onboarding_total | $325k | $563k | $2.39M | $18.28M |


### R6 Fee sensitivity: payback months (base grants, typical data, base balance)

| Accounts | 10 bps | 15 bps | 20 bps | 30 bps |
|---|---|---|---|---|
| 1,000 | 37.1 (SEPARATE_ONBOARDING_FEE) | 19.9 (INCLUDE_IN_FEE) | 13.6 (INCLUDE_IN_FEE) | 8.3 (INCLUDE_IN_FEE) |
| 10,000 | 4.3 (INCLUDE_IN_FEE) | 2.6 (INCLUDE_IN_FEE) | 1.9 (INCLUDE_IN_FEE) | 1.2 (INCLUDE_IN_FEE) |
| 100,000 | 1.9 (INCLUDE_IN_FEE) | 1.2 (INCLUDE_IN_FEE) | 0.8 (INCLUDE_IN_FEE) | 0.5 (INCLUDE_IN_FEE) |
| 1,000,000 | 1.4 (INCLUDE_IN_FEE) | 0.9 (INCLUDE_IN_FEE) | 0.6 (INCLUDE_IN_FEE) | 0.4 (INCLUDE_IN_FEE) |


### R7 Data quality: onboarding cost / payback months / time to production (20 bps, base)

| Accounts | Clean | Typical | Poor |
|---|---|---|---|
| 1,000 | $134k / 10.5 mo / 22 wk | $200k / 13.6 mo / 31 wk | $331k / 20.4 mo / 43 wk |
| 10,000 | $270k / 1.3 mo / 24 wk | $438k / 1.9 mo / 33 wk | $796k / 3.0 mo / 45 wk |
| 100,000 | $1.09M / 0.4 mo / 26 wk | $2.26M / 0.8 mo / 35 wk | $4.88M / 1.7 mo / 47 wk |
| 1,000,000 | $7.00M / 0.2 mo / 28 wk | $18.16M / 0.6 mo / 37 wk | $43.33M / 1.5 mo / 49 wk |


### R8 Balance case: contribution and payback (20 bps, typical, base grants)

| Accounts | Low balance | Base balance | High balance |
|---|---|---|---|
| 1,000 | $76k: $74k / 52.3 mo | $182k: $287k / 13.6 mo | $390k: $703k / 5.5 mo |
| 10,000 | $76k: $1.03M / 6.5 mo | $206k: $3.65M / 1.9 mo | $423k: $7.97M / 0.8 mo |
| 100,000 | $161k: $27.79M / 1.0 mo | $194k: $34.47M / 0.8 mo | $423k: $80.19M / 0.4 mo |
| 1,000,000 | $6,939: -$28.20M / never mo | $194k: $345.89M / 0.6 mo | $323k: $603.93M / 0.4 mo |


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
| 1,000 | 4.2 ($67k) | 13.6 ($200k) | 132.9 ($711k) |
| 10,000 | 0.5 ($122k) | 1.9 ($438k) | 10.7 ($1.81M) |
| 100,000 | 0.2 ($599k) | 0.8 ($2.26M) | 4.9 ($8.98M) |
| 1,000,000 | 0.2 ($5.12M) | 0.6 ($18.16M) | 3.7 ($70.76M) |


### R11 Classification counts across 27 grants x quality x balance combinations (base cost)

| Accounts | Fee bps | INCLUDE_IN_FEE | SEPARATE_ONBOARDING_FEE | UNECONOMIC |
|---|---|---|---|---|
| 1,000 | 10 | 9 | 7 | 11 |
| 1,000 | 15 | 15 | 3 | 9 |
| 1,000 | 20 | 18 | 5 | 4 |
| 1,000 | 30 | 21 | 6 | 0 |
| 10,000 | 10 | 21 | 4 | 2 |
| 10,000 | 15 | 26 | 1 | 0 |
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
| term_contribution_after_onboarding | $1.11M | $17.67M | $169.96M | $1.71B |


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
| onb_total_unbound | $366k |
| cac_per_sponsor | $125k |
| acquisition_and_onboarding_total | $491k |
| onb_per_account | $366 |
| onb_per_migrated_txn | $2.41 |
| onb_engineering_hours | 1,600 |
| onb_charity_enrolment | $30k |
| onb_sponsor_hours | 951 |
| onb_sponsor_cost | $67k |
| buyer_switching_tco | $195k |
| time_to_production_weeks | 43 |
| payback_months | 149.2 |
| payback_months_onboarding_only | 111.2 |
| payback_months_at_100_per_account | never |
| payback_months_at_400_per_account | 20.4 |
| breakeven_bps_recurring | 14.8 |
| breakeven_bps_incl_onboarding_amortised | 27.8 |
| breakeven_balance_at_fee | $105k |
| revenue_per_account | $151 |
| breakeven_price_per_account_incl_onboarding | $210 |
| classification | UNECONOMIC |


### R14 Non-included combinations for small sponsors (1,000 accounts, base cost)

| Fee bps | Grants | Data | Balance | Contribution/yr | Onboarding (excl. CAC) | Payback mo (incl. CAC) | Fee to reach 24 mo (incl. CAC) | Class |
|---|---|---|---|---|---|---|---|---|
| 10 | low | clean | low | $12k | $130k | 245.0 | $230k | UNECONOMIC |
| 20 | low | clean | low | $88k | $130k | 34.7 | $78k | SEPARATE_ONBOARDING_FEE |
| 10 | low | clean | base | $119k | $130k | 25.8 | $17k | SEPARATE_ONBOARDING_FEE |
| 10 | low | typical | low | $3,028 | $194k | 1264.5 | $313k | UNECONOMIC |
| 20 | low | typical | low | $79k | $194k | 48.6 | $162k | SEPARATE_ONBOARDING_FEE |
| 10 | low | typical | base | $109k | $194k | 35.0 | $101k | SEPARATE_ONBOARDING_FEE |
| 10 | low | poor | low | -$16k | $322k | never | $447k | UNECONOMIC |
| 20 | low | poor | low | $60k | $322k | 89.7 | $328k | UNECONOMIC |
| 10 | low | poor | base | $90k | $322k | 59.4 | $267k | SEPARATE_ONBOARDING_FEE |
| 10 | base | clean | low | $8,225 | $134k | 377.3 | $242k | UNECONOMIC |
| 20 | base | clean | low | $84k | $134k | 37.0 | $91k | SEPARATE_ONBOARDING_FEE |
| 10 | base | clean | base | $114k | $134k | 27.1 | $30k | SEPARATE_ONBOARDING_FEE |
| 10 | base | typical | low | -$1,223 | $200k | never | $325k | UNECONOMIC |
| 20 | base | typical | low | $74k | $200k | 52.3 | $176k | SEPARATE_ONBOARDING_FEE |
| 10 | base | typical | base | $105k | $200k | 37.1 | $115k | SEPARATE_ONBOARDING_FEE |
| 10 | base | poor | low | -$20k | $331k | never | $456k | UNECONOMIC |
| 20 | base | poor | low | $56k | $331k | 98.6 | $345k | UNECONOMIC |
| 10 | base | poor | base | $86k | $331k | 63.6 | $284k | UNECONOMIC |
| 10 | high | clean | low | -$7,867 | $148k | never | $273k | UNECONOMIC |
| 20 | high | clean | low | $68k | $148k | 48.4 | $138k | SEPARATE_ONBOARDING_FEE |
| 10 | high | clean | base | $98k | $148k | 33.4 | $77k | SEPARATE_ONBOARDING_FEE |
| 10 | high | typical | low | -$17k | $220k | never | $345k | UNECONOMIC |
| 20 | high | typical | low | $58k | $220k | 71.0 | $229k | UNECONOMIC |
| 10 | high | typical | base | $89k | $220k | 46.6 | $168k | SEPARATE_ONBOARDING_FEE |
| 10 | high | poor | low | -$36k | $366k | never | $491k | UNECONOMIC |
| 20 | high | poor | low | $39k | $366k | 149.2 | $412k | UNECONOMIC |
| 10 | high | poor | base | $70k | $366k | 84.1 | $351k | UNECONOMIC |


### R16 History depth: onboarding cost / per-transaction share / payback (20 bps, base, typical data)

| Accounts | Short (33 months, AEF) | Mid (7 years, GWCF) | Full (20 years ramped) |
|---|---|---|---|
| 1,000 | $191k / 1% / 13.2 mo | $194k / 3% / 13.3 mo | $200k / 5% / 13.6 mo |
| 10,000 | $350k / 7% / 1.6 mo | $384k / 14% / 1.7 mo | $438k / 24% / 1.9 mo |
| 100,000 | $1.39M / 18% / 0.5 mo | $1.72M / 32% / 0.6 mo | $2.26M / 46% / 0.8 mo |
| 1,000,000 | $9.44M / 27% / 0.3 mo | $12.76M / 43% / 0.4 mo | $18.16M / 58% / 0.6 mo |


### R17 Buyer switching TCO, outside Unbound's P&L (base, typical data, full history)

| Item | 1,000 | 10,000 | 100,000 | 1,000,000 |
|---|---|---|---|---|
| onb_sponsor_hours | 584 | 934 | 1,922 | 9,016 |
| onb_sponsor_cost | $41k | $65k | $135k | $631k |
| buyer_consultant | $29k | $115k | $115k | $115k |
| buyer_incumbent_tail_fee | $50k | $50k | $50k | $50k |
| buyer_auditor_uplift | $20k | $20k | $20k | $20k |
| buyer_legal | $20k | $20k | $20k | $20k |
| buyer_comms | $10k | $10k | $10k | $10k |
| buyer_switching_tco | $170k | $280k | $350k | $846k |


High cost case, poor data: buyer switching TCO 1,000: $913k; 10,000: $1.38M; 100,000: $1.96M; 1,000,000: $6.18M.



### R15 Registry fixed cost per grant by network grant volume (annual fixed + establishment over 5 yrs)

| Network grants/yr | Low | Base | High |
|---|---|---|---|
| 70,000 | $0.67 | $1.98 | $6.20 |
| 700,000 | $0.07 | $0.20 | $0.62 |
| 3,000,000 | $0.02 | $0.05 | $0.14 |
| 7,000,000 | $0.01 | $0.02 | $0.06 |

## 7. Conflicts and tensions with ratified decisions and existing models

None of these is a conflict that requires a change. Each is flagged for the coordinator.

- **CNV-EXP-002 (full fund history at migration)** is the largest driver of onboarding cost: 46-58% at 100k+ accounts with 20 years of ramped history (R16). It is not a conflict. But the cost depends on how reconciliation is designed (see ECO-RC-2). Predecessors may also hold less than full history; AEF's held 33 months. A 'history available at source, gaps disclosed' clarification is needed (ECO-RC-7).
- **Release-1 scope (ADVB-01).** A proposed R1 with 'no migration' conflicts with CNV-EXP-002 (initial-implementation) and the CNV-ECO-003 shadow-replay amendment. These economics assume migration is in scope. Without it, the CNV-ECO-004 entry segment cannot be served.
- **CNV-PAY-001 / CNV-LEG-001 (sponsor originates; Unbound holds no funds).** E-payment rail savings accrue to the sponsor, not to Unbound's P&L. Unbound captures only labour savings (about $0.48 per grant shifted) and a stronger sales argument. Stripe and other facilitator payout products are cited only for price benchmarks. Using them as a rail would need a partner acting as the sponsor's agent.
- **The Unbound `parameters.json` value `sponsor_onboarding_cost` of $60k** (flat, amortised over 5 years) and the 05a "sponsor onboarding and exit" line understate onboarding above about 3k accounts. This model gives $43.76 per account at 10k and $22.61 at 100k, one-time, excluding CAC. Recommend reconciling the two models.
- **CNV-ECO-004 entry segment (about 5k-50k funds) is supported on cost, at Low confidence.** At 15 bps or above, 26-27 of 27 combinations are INCLUDE_IN_FEE, but this depends on the price assumption (ADVB-13). The segment also requires migration (see ADVB-01 above). The 1k sponsor is where the fee structure has to change.
- **Exit symmetry (ADVB-11).** Revision 1's termination-fee recommendation conflicted with the exit-symmetry position in 10 and 11. It is withdrawn (section 4).

## Implications for Unbound

1. **Price onboarding by gate, not by hope.**
   - Require a paid or free pre-contract **data-quality profile** that measures:
     - account mapping exception rate;
     - historical transaction break rate;
     - number of custom integrations;
     - the share of the sponsor's recipients covered by networked partners.
   - Include onboarding in the fee only inside the thresholds in section 4.
2. **Set a minimum annual fee of about $140k** (or per-account floors) for sponsors under about 3-5k accounts. Servicing-economics' $100-110k excluded CAC. Do not rely on onboarding fees for small sponsors, because those fees exceed first-year revenue.
3. **Invest in Track B automation and in reducing buyer effort before registry breadth.** Each percentage point of transaction-exception rate costs about $104k per 10k-account sponsor (ramped 20-year history at 10 minutes per exception). The buyer's own switching TCO is about $280k. The registry costs about $75k a year in total.
4. **Use the network as a switching-cost neutraliser.**
   - Reuse partner enrolments (CNV-EXP-002) and registry evidence (CNV-GRT-003). Each one halves the direct-enrolment bill at onboarding.
   - Quote the e-payment saving (about $1.07 per grant shifted, roughly half to the sponsor) in proposals as a sponsor benefit.
5. **Do not bid bps-only on processor-like books** (average balance under about $20k). Account-based cost exceeds asset revenue at any fee from 10 to 30 bps.
6. **Large sponsors will negotiate to a per-account price.** The cost floor of $46-59 per account leaves wide room under Ren-like anchors of about $737 per account. The constraints there are capacity, risk and the buyer's switching TCO, not unit cost.
7. **Never trade exit symmetry for onboarding recovery.** Charge out-of-gate onboarding up front. Any unamortised-recovery schedule must be straight-line and published, and export must never be conditional on payment.

## Candidate requirements (one line each)

- **ECO-RC-1 (refines CNV-EXP-002):** Before contract, the onboarding process SHALL produce a sponsor data-quality profile: account exception rate, historical transaction break rate, custom integration count, and partner-enrolment coverage of the sponsor's recipients. The profile SHALL feed a deterministic onboarding price and an estimated time to production.
- **ECO-RC-2 (refines CNV-EXP-002):** History migration SHALL reconcile aggregates per period and per fund first. Transaction-level exceptions SHALL be opened only where an aggregate breaks. Every imported transaction SHALL still be retained, append-only.
- **ECO-RC-3 (refines CNV-PAY-002 / UNB-CHAR):** The registry SHALL record verification method and cost class per destination (partner enrolment reused, instant ownership API, micro-deposit, bank letter) so that enrolment cost and reuse can be metered.
- **ECO-RC-4 (refines CNV-GRT-003):** The platform SHALL meter registry fixed and variable cost per grant and per charity in use, and SHALL report exception minutes per case, to replace ASSUMPTION parameters.
- **ECO-RC-5 (commercial; refines servicing-economics RC list):** Commercial terms SHALL support a minimum annual fee, an up-front onboarding fee for sponsors outside the gates, and overage per exception and per custom integration. Any early-exit recovery SHALL be limited to a published straight-line unamortised balance. Data export SHALL never be conditioned on payment or carry a fee.
- **ECO-RC-7 (clarifies CNV-EXP-002):** 'Full history' SHALL mean all history the sponsor can lawfully obtain from any source. Gaps SHALL be disclosed as HistoryGap records with the source's retention evidence, and history depth SHALL be an input to the onboarding price.
- **ECO-RC-6 (refines CNV-EXP-002):** Migration SHALL measure the sponsor's check share at baseline and track it monthly against a target, so that e-payment value is evidenced.

## Open questions / evidence gaps

1. **Migration exception rates and minutes.** Account and transaction exception rates, and the minutes to resolve them, have no public benchmark. All are ASSUMPTION, and they are the most sensitive inputs. An NDA time study on one real migration is needed.
2. **Time to production** is calibrated to self-reported cases in 10 (3-6 months for CF conversions, about 8.5 months for AEF, 18+ months for Arizona). No case reports elapsed time *with* full-history reconciliation.
2a. **Buyer TCO.** Incumbent tail fees (base $50k is ASSUMPTION; JCF $417,742 is the observed high), auditor uplift, and the sponsor's real FTE draw all need measuring in the first migration (CNV-ECO-003 evidence obligations).
3. **Plaid Auth and Identity Match prices** are not public [ECO-012]. The sponsor-side price of Chariot Disbursements is not published: the page says only "at no cost" to nonprofits [ECO-005]. PayPal Grant Payments economics are not public.
4. **Check economics specific to DAF sponsors** (uncashed and escheat rates, positive-pay exception rates) are not published. The AFP survey is from 2022 and covers B2B payers [ECO-001].
5. **Partner coverage.** The share of a migrating sponsor's recipients already enrolled with a networked partner is unknown. 50% is ASSUMPTION, anchored on Fidelity's 67% electronic grant share [ECO-005].
6. **Size of the 990 XML corpus and paid state-data prices** were not measured. Storage is immaterial at any plausible size. State data prices (Indiana $9,500+) need reconfirmation.
7. **Sales-cycle reduction** (HYPOTHESIS) needs pipeline data: the months from first meeting to signature, and from signature to go-live, with and without network coverage.
8. **Company-level viability.** Contribution here excludes organisation fixed costs and build capex. Company-level break-even remains as in `research/commercial-opportunity/servicing-economics/` and `ai-native-capital-minimization/`.
