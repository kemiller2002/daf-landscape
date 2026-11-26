# 20 - Economic analysis: charity network and institutional onboarding

Status: research draft (2026-11-26). Not legal advice. Evidence classes per 01-research-methodology.md.

Agent: ECO. Model: `scripts/economic_model.py` (Python 3 stdlib, functional, deterministic). Inputs: `data/economic-parameters.csv` (136 parameters, each with an evidence class). Output: `data/economic-scenarios-output.csv`, long format, about 66,000 rows. It holds 876 deterministic sponsor scenarios, 16 Monte Carlo summaries (2,000 seeded draws each), and unit-cost, platform and network rows.

**Revision 3 (2026-11-26), after adversarial review X.** This revision responds to `data/adversarial-findings-X.csv`. Changes:

- The no-lever C0 case is now the base (CNV-ECO-003). The AI-native lever case C is shown as a lever.
- Added Monte Carlo P10/P50/P90 and the CNV-ECO-005 stresses, including pre-delegation.
- Added a first-sponsor view that carries organisation fixed cost and build amortisation, and a four-equal-sponsor view for the 25% concentration cap.
- Added registry operating and compliance costs.
- Added observed price benchmarks.
- Adopted the partner-coverage and conversion assumptions from 08.

`scripts/advx_sensitivity.py` (the reviewer's script) still runs against this model; its output is in `data/advx-sensitivity-output.csv`.

**Revision 2 (2026-11-26), after adversarial review B.** This revision responds to `data/adversarial-findings-B.csv` (ADVB-05, 06, 07, 10, 11, 13; also 01, 04, 12). Changes:

- Added onboarding cost lines that were missing: rehearsals, Unbound legal work, a failed-migration reserve, and CAC.
- Added a buyer switching-TCO model: sponsor effort with a floor of at least 0.5 FTE, consultants, incumbent tail fees, auditor uplift, legal and communications.
- Added a history-depth dimension: 33 months, 7 years, and full history.
- Calibrated time to production against case evidence.
- Restated the termination recommendation and lowered confidence.

Section 0 records what changed and what survived. Sources: `data/sources-ECO.csv`. To reproduce, run `python3 scripts/economic_model.py`, then `--check` (recomputes and diffs; currently OK) and `--report` (prints the tables in section 6).

## Summary

Base case throughout: C0 (no unmeasured levers), 20 bps working fee, typical data, full ramped history. Monte Carlo ranges are P10-P90 over 2,000 draws.

- **Track A, the registry, is a mandated cost of doing business, not a value lever (ADVX-15 accepted).**
  - Establishment: about **$319k** ($113k-$1.07M).
  - Running cost: **$316k a year** ($107k-$673k). That includes stewardship and disputes, counsel review, the Nacha TPSP audit, verification-vendor minimums, a charity support desk and an insurance rider.
  - Per grant: **$5.42 at one entry sponsor's 70k grants**, $0.54 at 700k.
  - Storage and compute stay immaterial. People and compliance are the cost. (INFERENCE from ASSUMPTION; Medium.)
- **Network economic value is small and conditional (ADVX-13/14 accepted).**
  - With 08's partner coverage (8% base) and its planning conversion path (p = 0.10, so 37% of grants are still checks at 36 months), e-payment savings against a 33%-check sponsor are **$0** in base.
  - Savings appear only if conversion beats p = 0.10 or the sponsor starts check-heavy. For example, a 50%-check sponsor saves about $148k a year at 10k accounts in the high cost case.
  - Charity enrolment at onboarding rises to **$178k** at 10k accounts. A mature registry would avoid about half.
  - The sales-cycle value (about $0.8M) stays a quarantined HYPOTHESIS until there is win/loss evidence. (INFERENCE; Medium.)
- **Onboarding in the fee works only for added sponsors, not the first (ADVX-03 accepted).**
  - *Marginal (added-sponsor) view* at 10k accounts:
    - Onboarding $757k, including $212k of pre-delegation labour. CAC adds $125k.
    - Payback is **3.4 months** at 20 bps (P10-P90 **3.9-6.6**; 100% of draws INCLUDE_IN_FEE).
    - At 10 bps it is 10.2 months (P10-P90 12.3-49).
  - *First-sponsor view* at 10k accounts: the sponsor must carry $3.04M a year of platform fixed cost (organisation $1.66M, build $1.0M, registry $0.38M).
    - Net is only **$63k at 20 bps**, so payback is **about 184 months**. At P50/P90 cost it never pays back.
    - At 10 bps net is -$2.0M.
  - With **four equal sponsors** (the CNV-ECO-004 25% cap), payback is 4.5 months at 20 bps (P90 11.0) and 38 months at 10 bps.
  - **INCLUDE_IN_FEE is therefore a rule for added sponsors once fixed costs are covered.** The first one to three sponsors need design-partner terms: onboarding charged up front or co-funded. (INFERENCE; Medium for direction, Low for levels.)
- **Small sponsors are uneconomic under C0.**
  - 1k accounts at 20 bps: marginal payback **20 months** (P10-P90 24-45). Only 11% of draws INCLUDE.
  - 9 of 27 deterministic combinations are UNECONOMIC.
  - Break-even price **$220 per account**. A minimum annual fee of about **$220k** is needed at C0, or about $160k if the levers are proven (C).
- **Price benchmarks cut the addressable buyers (ADVX-05/06/07 partly accepted).**
  - Unbound's C0 break-even is **$101-120 per account at 10k+ accounts** ($57-72 with levers).
  - Payback **never** occurs at Ren's software price of $81 per account (NCF).
  - At Ren's staffed take of 18.5 bps (MS GIFT), payback is 3.8 months base and never in the high cost case.
  - At $737 per account (staffed) it is 1.7 months.
  - So Unbound can compete for **outsourced-staffed** buyers. It cannot compete at C0 for **self-staffed software** buyers.
  - Donors ultimately fund the fee from sponsor admin-fee schedules, so 20 bps is a price *increase* against an 18.5 bps incumbent. (INFERENCE; Medium.)
- **The CNV-ECO-005 stresses keep the marginal case positive.** Applied together (15% AUA decline, 20% price pressure and a December surge), 10k-account contribution falls from $3.10M to $1.73M and payback to 6.1 months. At 1k accounts contribution falls to $96k, payback 46 months, and the sponsor is negative after its fixed-cost share. The 25% concentration cap is breached by any single-sponsor start, however large that sponsor is. (INFERENCE.)
- **History depth and data quality still drive variance.**
  - At 1M accounts, onboarding cost runs from $32M (clean) to $68M (poor).
  - Per-transaction migration is 14-24% of onboarding cost at 10k-1M accounts with full history.
  - Pre-delegation labour is now the largest scaling line.
- **The buyer's switching TCO of $170k-$846k (base) is unchanged.** Exit-symmetry terms from revision 2 stand.
- **CNV-ECO-003 conformance is partial.** Done: C0 base, P10-P90, viability at P90 cost, pre-delegation and stresses. Missing:
  - adverse licence scale (this model has no licence term);
  - correlated draws (independence is an ASSUMPTION);
  - measured lever values.

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

| ADVX-01: Track A run costs omitted | **Accepted** | Added stewardship (0.5-1 FTE, CST-R10), charity support desk (0.25-1 FTE, CST-R13), counsel review (40-130 h at CST-C06 rates), Nacha TPSP audit, verification-vendor minimums and an insurance rider. Registry run cost goes from $75k to $316k a year ($5.42 per grant at 70k grants). These are not in servicing-economics Model B. Model C's compliance officer would overlap stewardship, so do not add both. |
| ADVX-02: international grants | Noted | Excluded from Release-1 economics. Equivalency determination and intermediary routing are pass-through when CNV-GRT-008 activates. |
| ADVX-03: first-sponsor view | **Accepted** | Added first-sponsor and four-equal-sponsor views (R18, R22). INCLUDE_IN_FEE is restated as an added-sponsor rule. |
| ADVX-04: CNV-ECO-003/005 conformance | **Accepted, partially met** | C0 is now base (ai_enhanced activity minutes; 8% exceptions at 45 minutes; no determination reuse), with lever case C shown separately (R21). Monte Carlo P10/P50/P90 added (R22); "P90 cost" means contribution at P10. Pre-delegation (6-18 months, review and release labour at 1.5-3x, manual NAV checks) is in onboarding. CNV-ECO-005 stresses are in R19 and the 25% cap in R18. **Still missing:** adverse licence scale; correlated sampling; measured levers. |
| ADVX-05/06/07: price benchmarks and payer | **Partly accepted** | Added 18.5 bps to the fee grid and per-account price paybacks at $81, $150, $250 and $737 (R20). Added `sponsor_saving_vs_incumbent_18_5bps`. A full payer model (donor fee schedule minus servicer take) is not built. It is stated qualitatively. |
| ADVX-13: partner coverage | **Accepted** | 0.03/0.08/0.20 from 08. The Fidelity anchor is removed. |
| ADVX-14: check-share target | **Accepted** | 0.15/0.37/0.37 at 36 months (08: p = 0.25 target path; p = 0.10 planning path). E-payment value is restated as conditional. |
| ADVX-15: network value overstated | **Accepted** | The registry is reframed as a mandated cost. Sales-cycle value is quarantined. |
| ADVX-16: pre-delegation, replay, hypercare | **Accepted** | Pre-delegation applies to all sponsors. The first-sponsor replay and time study ($40k-$160k) apply in the first-sponsor view. Hypercare donor contact rises to 20% (10-35%). |
| ADVX-17: inputs misquoted | Rejection confirmed | No change. |

**Rejected or not changed, with reasons.** The challenge that the 10k INCLUDE_IN_FEE result is wrong is not upheld *as arithmetic*. Even with all added lines, onboarding plus CAC ($563k) is about 15% of one year's revenue at 20 bps. It is upheld *as to dependence*: the result rests on the revenue assumption. So confidence is lowered rather than the conclusion reversed.

**What survives, and at what confidence.**

**What survives revision 3.**

| Conclusion | Status |
|---|---|
| Registry cost structure | Revised: run cost is about 4x higher; still small against servicing revenue; Medium |
| Unit costs | Revised: C0 base roughly doubles labour cost per grant; Medium |
| Network value | Revised down to about $0 in base; mandated cost, not a lever; Medium |
| Entry segment absorbs onboarding | Survives **only for added sponsors** at roughly 15 bps or more, or about $250+ per account; Low |
| First-sponsor viability | New: not viable without design-partner terms; Medium |
| Small sponsors need minimum fees | Strengthened: about $220k at C0; Medium |
| Processor books uneconomic | Survives, High for direction |
| Self-staffed software buyers ($81 per account) | New: uncompetitive at C0; Medium |
| Termination-fee recommendation | Remains withdrawn |

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
| Revenue | Asset-based: AUA x bps (10/15/18.5/20/30; **20 bps is a working scenario only**). Per-account price paybacks at $81/$150/$250/$737 | Accounts x average balance |
| Platform fixed, first-sponsor view only | Organisation fixed ($1.09-2.77M), build amortisation ($0.6-3.0M a year), registry run cost and establishment over 5 years. Carried entirely by the first sponsor, or split four ways under the 25% cap | Per company |

**Lever case.** Base is **C0** (CNV-ECO-003). Its parameters use the `_c0` columns: ai_enhanced activity minutes, an 8% exception rate at 45 minutes with no determination reuse, $40 per account, and 560 sponsor hours. **C** (AI-native levers) appears in R21 and R22 only.

**Scenario grid (876 deterministic scenarios).** The base cost case runs 540 scenarios across five dimensions, all C0 with full history:

- size: 1k, 10k, 100k or 1M accounts;
- grants per account:
  - low 5.6 (MS GIFT);
  - base 7.0 (median of 10 sponsors' published counts over Schedule D accounts, `summary-stats.json`; NPT FY2025 is 159,543 / 20,561 = 7.76, from `data/expanded-sponsor-activity-benchmarks-2026.csv`);
  - high 12.3 (Fidelity, `research/mission-2026-11-14/`);
- data quality: clean, typical or poor;
- average balance per size segment: low, base or high, taken from `data/commercial-opportunity/servicing-economics/segment-summary.csv` (sources are listed in the parameter file);
- fee: 10, 15, 18.5, 20 or 30 bps.

The low and high cost cases add 216 scenarios at 20 bps. A history family adds 24 more: short and mid history x 4 sizes x 3 data qualities, at base values and 20 bps. A lever-C family adds 60 more.

**Monte Carlo.**

- Draws: 2,000 per scenario, with a fixed seed.
- Distribution: each non-dimension parameter is drawn from an independent triangular(low, base, high) distribution. Independence is an ASSUMPTION.
- Scenarios covered: 4 sizes x 10/20 bps x C0/C.
- Output: P10/P50/P90 (R22). For costs and payback, P90 is the adverse end.

**Stresses (CNV-ECO-005).** A 15% AUA decline, 20% price pressure, a December surge (30% of grants at a 1.3x labour premium), and all three combined (R19). Loss of the largest sponsor is the first-sponsor view (R18).

**Recipients.** A sponsor's distinct recipients are grants divided by grants per recipient. Grants per recipient is 2.5 x (accounts/1000)^0.24, kept between 2.5 and 13.2, so it reproduces the Fidelity end-point of 13.2 at 1M accounts (A-ACT-005).

**Classification rule (RECOMMENDATION).**

| Class | Rule |
|---|---|
| INCLUDE_IN_FEE | Payback of onboarding **plus CAC** of 24 months or less |
| SEPARATE_ONBOARDING_FEE | Payback over 24 months but within the 60-month term |
| UNECONOMIC | Contribution of 0 or less, or payback longer than the term |

**What "contribution" means here.** It is the sponsor's direct (marginal) contribution before platform fixed cost. **The first-sponsor and four-sponsor views (R18) carry that fixed cost**, and payback in those views includes CAC. Company-level break-even is still in servicing-economics: about $1.1-1.5B AUA operating, $1.8-2.3B fully loaded.

**Reused parameters (not invented).**

| Parameter | Value | Source |
|---|---|---|
| Labour rate | $65.45/h | servicing-economics |
| Engineering rate | $118/h | CST-R03 |
| Implementation rate | $80/h | CST-R11 |
| Exception rate | C0 8% with no reuse (Unbound); C 4% with reuse (A-ACT-006) | as stated |
| Minutes per exception | C0 45 (Unbound); C 30 (A-ACT-007) | as stated |
| Activity minutes | C0 = ai_enhanced (ACH 0.3, check 2, status 0.3, review 1.46); C = ai_native (0.1, 1.2, 0.03, 0.97) | `activity-minutes-typical.csv` |
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
| Stewardship and compliance, 1 FTE (disputes and appeals, CHAR-ADR-002/006/007) | $122k | CST-R10; ADVX-01 |
| Charity support desk, 0.5 FTE | $39k | CST-R13 |
| Counsel review of eligibility rules (CHAR-ADR-010), 80 h | $36k | CST-C06 rate |
| Nacha TPSP annual Rules compliance audit, vendor minimums, insurance rider | $44k | ADVX-001/002; ASSUMPTION |
| **Total** | **$316k** ($107k-$673k) | |

The registry's run cost is dominated by people and compliance, not cloud spend. Per grant (R15) it is **$5.42 at 70k grants, $1.81 at 210k and $0.54 at 700k**.

**Staging (ADVX-08, RECOMMENDATION).** In Release 1, build federal sources plus resolution of the first sponsor's actual recipients. Defer state connectors outside the first sponsor's states.

**Verification, exceptions and monitoring.**

| Item | Calculation | Base cost |
|---|---|---|
| First-time verification of a charity | compute + 8% x $50 exception | $4.01 (C: $1.35) |
| Exception | 45 min x $65.45 + $0.90 AI dossier | $50 (C: $34) |
| Monitoring per charity-year | 4% status events x exception cost | $2.12 (C: $1.46) |
| Unbound cost per grant at a 33% check share | review, screening, exceptions, payment labour | $7.26 (C: $3.35) |

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

As a cross-check, Corpay's illustrative "not a benchmark" model gives $5.71 for a check and $1.67 for an ACH payment [ECO-013]. Our gap is $5.32 at C0 ($4.66 at C), against its $4.04.

**Network growth (R3).** Variable cost scales with the charities actually in use, not with the 1.9M rows in the BMF. At 50k charities in use it is about $348k a year. At 600k it is $4.2M a year, plus a one-time $6.6M to enrol charities not covered by partners. Partner coverage is now 08's 8% base, so CNV-EXP-002 partner reuse saves less than revision 1 assumed. The material lever is per-invitation conversion (08 §4.3), not partner coverage.

## 3. Track B: onboarding costs

R4, R5, R16 and R17 give the figures.

**Fixed versus scaling cost.** Implementation, engineering configuration and integrations stay roughly fixed at **$118k-$154k** (800 engineering hours in the typical case). Rehearsals add $8k-$20k, Unbound legal $15k, and the failure reserve 10% of direct cost. CAC ($125k, ASSUMPTION) is reported separately and included in payback. Per-account and per-transaction work dominates above 10k accounts. **Pre-delegation (CNV-ECO-005)** is now the largest scaling line: about 12 months of human approval and three-person release before sponsor delegations allow deterministic approval. It costs $28k at 1k accounts, $212k at 10k and $20M at 1M (ASSUMPTION; borne by Unbound in this model; it may sit partly with the sponsor).

**History depth (ADVB-07).** Default history is 20 years, ramped for 8% a year growth. That is about 10.6 full-volume years, at (7 grants + 2 contributions) per account a year.

| Accounts | Migrated transactions | Per-transaction migration cost |
|---|---|---|
| 1k | about 95k | $10k |
| 10k | about 954k | $105k |
| 1M | about 95M | $10.5M |

The share of onboarding cost that is per-transaction work depends on how much history the predecessor holds (R16). Shares fell in revision 3 because C0 pre-delegation and enrolment enlarged the total:

| Accounts | 33 months (AEF) | 7 years | 20 years |
|---|---|---|---|
| 10k | 4% | 8% | 14% |
| 1M | 7% | 15% | 24% |

Where the predecessor holds less than full history (AEF's platform yielded 33 months), the gap has to be documented, not invented.

**Charity enrolment at onboarding.** It is $178k at 10k accounts and $5.9M at 1M, using 08's 8% partner coverage (was 50%) and enrolling 50% of the remainder in year 1. Donor hypercare after a universal credential reset (20% contact) costs $33k at 10k accounts.

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

- SPN placeholders ($100k + $15 per account) give $250k at 10k accounts. The model now gives $757k at C0 ($689k at C), higher because of full history, rehearsals, the reserve, pre-delegation and lower partner coverage.
- Unbound's flat `sponsor_onboarding_cost` of $60k (`parameters.json`) understates onboarding above about 3k accounts.
- Ren markets program set-up at "around $50,000" (VENDOR-CLAIM, ADVB-007). That is a new-program price, not a migration price, but it anchors buyer expectations for any onboarding fee.

## 4. Can onboarding be fixed-price or included in the fee?

R6, R7, R8, R10, R11, R14, R16, R18, R20 and R22 answer this. All paybacks include CAC. **Every rule below is for an added sponsor, once platform fixed cost is covered (ADVX-03).** For the first one to three sponsors, see the design-partner terms after the table. Summary rule (RECOMMENDATION; Low):

| Condition | Include in servicing fee | Separate up-front onboarding fee (fixed for scope, plus overage) | Uneconomic or reprice |
|---|---|---|---|
| Accounts and fee | 100k+ at 15 bps or above (27/27); 10k at 18.5-20 bps (21-23 of 27); 10k at 10-15 bps (16-18 of 27) | 1k at 15-20 bps with base or high balance | 1k at 10 bps (18/27 UNECONOMIC), or with low balance at any bps; processor-like books at any bps |
| Per-account price equivalent | About $250 or more per account at 10k+ accounts (payback 3-7 months; 22 months at $150) | $150-250 | Below C0 break-even ($220 at 1k accounts, $101-120 at 10k+). This includes Ren's $81 software price |
| Data quality (pre-contract profile) | Account exceptions 3% or less; transaction breaks 1% or less | Up to 10% / 3%, with per-exception overage | Unprofiled data plus a fixed price |
| History availability | Source holds the required history, or gaps are documented | Reconstruction needed from secondary sources (priced as overage) | n/a |
| Custom integrations | 1 or fewer | 2-3, priced per integration ($47k build; $9k a year to maintain) | Many custom integrations at a small sponsor |
| Term and exit | Any term of 36 months or more, **no exit charge** | Onboarding paid up front, so no exit recovery is needed | n/a |

**First one to three sponsors (design partners).** With platform fixed cost of about $3.04M a year, a 10k-account first sponsor nets $63k at 20 bps, and never pays back at P50 or P90. Viable structures:

- onboarding charged up front, or co-funded by the sponsor;
- a minimum annual fee;
- a higher introductory bps with a published step-down once four or more sponsors are live (the 25% cap);
- or sponsors of 100k+ accounts, whose first-sponsor payback is 2.4 months.

In every case Unbound needs capital for the fixed base until about four 10k-account sponsors are live (four-sponsor payback 4.5 months; P90 11).

**Fixed price needs a gate.** Data quality alone moves the onboarding bill $179k-$377k at 1k accounts and $32M-$68M at 1M. History depth adds up to 1.25x at 1M. That variance is safe to absorb only when it is measured before signing. The fee needed to restore a 24-month payback for uneconomic small sponsors is $229k-$491k (R14). That is more than their first-year revenue, so a **minimum annual fee of about $140k** is cleaner.

**Exit symmetry (ADVB-11).** Revision 1 recommended a termination fee that recovered onboarding. That **contradicts** the exit-symmetry position in 10 and 11 and is withdrawn. Replacement conditions:

1. Onboarding that Unbound absorbs is recovered only through the servicing fee over time.
2. If any early-exit recovery is contracted, it is limited to the straight-line unamortised balance of the onboarding Unbound absorbed. The model reports it at 12 months ($706k for a 10k sponsor on a 60-month term, onboarding plus CAC) and at 36 months ($353k). The schedule is published in the proposal.
3. Export of all sponsor data in documented schemas is never conditioned on payment, carries no export fee, and starts within the same SLA whatever the payment status.
4. Nothing is owed when the exit follows an Unbound breach or SLA failure.

Where recovery at exit would be material, charging onboarding up front is the more honest structure. Unbound should not market "no lock-in" while contracting for it.

**Prices and payer (ADVX-05/06).**

- Observed comparators (servicing-economics `price-observations.csv`):
  - staffed outsourced administration 13-19 bps (Ren at MS GIFT 18.5 bps, about $737 per account);
  - self-staffed software 3-9 bps, or about $34-326 per account (Ren at NCF 4.67 bps, $81).
- Unbound's C0 break-even is $101-120 per account at 10k+ accounts ($57-72 with levers).
  - It can serve the staffed segment, with margin, at or below 18.5 bps.
  - It cannot serve the self-staffed software segment at C0. At $81 per account no size pays back. That segment is reachable only if the levers are proven, and even then only above about $72.
- **Who pays.** At comparable sponsors the servicer fee is carved from donor-paid admin fees (RCF pays Ren 98% of fundholder admin-fee revenue). Unbound at 20 bps against an 18.5 bps incumbent is a price *increase* to the sponsor's retained margin (`sponsor_saving_vs_incumbent_18_5bps` is negative). The pitch must rest on service and risk, not price, unless Unbound bids at or below the incumbent's realised take.

**Large sponsors.** A 20 bps fee on $19-194B is unrealistic. The binding constraints are capacity, risk and the buyer's switching TCO.

## 5. Economic value of each track to Unbound

| Value lever | Mechanism | Base magnitude (10k-account sponsor, 20 bps, C0) | Evidence |
|---|---|---|---|
| E-payment adoption | Check share at 36 months under 08's planning path (p = 0.10) is 37%, against a 33% sponsor status quo | **$0** in base. About $148k/yr only where the sponsor starts at 50% checks (high case) or conversion reaches p = 0.25 | INFERENCE (ADVX-14) |
| Network reuse at onboarding | A mature registry already holds 50% of the direct-enrol recipients | $89k once ($3.0M at 1M accounts) | ASSUMPTION |
| Registry scale economy | Run cost per grant $5.42 at 70k grants, $0.54 at 700k (R15) | A shared multi-sponsor registry is needed to make the mandated cost small | INFERENCE |
| Lower buyer switching TCO | Fewer sponsor hours and consultants | Buyer TCO is $280k at base | INFERENCE |
| Levers (C vs C0) | Determination reuse, AI-native redesign | $470k/yr more contribution at 10k accounts; break-even price from $120 to $72 per account | HYPOTHESIS until measured (CNV-ECO-003) |
| Sales-cycle reduction | 3 months saved x monthly contribution | About $0.8M; **quarantined** | HYPOTHESIS |
| Data-quality tooling | Moving a sponsor from poor to typical data | $363k at 10k accounts; $25M at 1M | INFERENCE |

**Interpretation (revised).** The charity registry and network are **mandated costs of doing business** (CNV-GRT-003, UNB-CHAR-DEC-001). They remove an objection to buying from Unbound; they are not a source of margin. Their per-sponsor run cost ($316k a year, about $5 per grant at entry scale) exceeds their measured savings until three or more sponsors share them. The commercially decisive variables are the **price segment** (staffed vs self-staffed), **getting past the first sponsor's fixed-cost burden**, and **proving the levers**.

## 6. Result tables (generated by `scripts/economic_model.py --report`)

All tables use the base cost case unless labelled. Dollar figures are rounded. "never" means contribution of 0 or less.

### R1 Unit costs (low / base / high cost case)

| Unit cost | Low | Base | High |
|---|---|---|---|
| cost_per_exception | $25.45 | $49.99 | $184 |
| verification_cost_per_new_charity | $0.71 | $4.01 | $31.33 |
| monitoring_cost_per_charity_year | $0.53 | $2.12 | $15.32 |
| epay_enrollment_cost_per_charity | $6.47 | $24.07 | $91.30 |
| bank_change_reverification_per_enrolled_year | $0.11 | $0.70 | $4.38 |
| ach_rail_cost_per_grant_passthrough | $0.26 | $0.53 | $0.80 |
| check_rail_cost_per_grant_passthrough | $1.05 | $3.09 | $8.48 |
| ach_labour_cost_per_grant | $0.10 | $0.41 | $1.60 |
| check_labour_cost_per_grant | $1.00 | $3.16 | $10.13 |
| screening_cost_per_grant | $1.46 | $5.94 | $36.49 |
| unbound_cost_per_grant_at_initial_check_share | $1.65 | $7.26 | $42.35 |
| unbound_cost_per_grant_at_target_check_share | $1.70 | $7.37 | $41.24 |
| allin_cost_per_grant_at_initial_check_share | $2.00 | $8.63 | $46.99 |
| allin_cost_per_grant_at_target_check_share | $2.08 | $8.85 | $44.89 |
| check_minus_ach_allin_per_grant | $1.69 | $5.32 | $16.21 |


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
| annual_steward_compliance_fte_usd | $49k | $122k | $148k |
| annual_charity_support_usd | $14k | $39k | $97k |
| annual_counsel_review_usd | $12k | $36k | $104k |
| annual_nacha_audit_vendor_min_insurance_usd | $8,000 | $44k | $105k |
| annual_registry_ops_compliance_usd | $83k | $240k | $454k |
| annual_fixed_total_usd | $107k | $316k | $673k |


### R3 Network growth (base cost case): variable cost by charities in use

| Charities in use | Monitoring/yr | New verification/yr | New enrolment/yr | Bank-change/yr | Variable total/yr | One-time enrol of existing |
|---|---|---|---|---|---|---|
| 10,000 | $21k | $12k | $33k | $3,199 | $70k | $111k |
| 50,000 | $106k | $60k | $166k | $16k | $348k | $554k |
| 200,000 | $424k | $241k | $664k | $64k | $1.39M | $2.21M |
| 600,000 | $1.27M | $722k | $1.99M | $192k | $4.18M | $6.64M |


### R4 Representative sponsors at 20 bps (base grants, typical data, base balance, base cost)

| Metric | 1,000 accts | 10,000 accts | 100,000 accts | 1,000,000 accts |
|---|---|---|---|---|
| avg_balance | $182k | $206k | $194k | $194k |
| aua | $181.90M | $2.06B | $19.40B | $193.98B |
| grants_per_year | 7,000 | 70,000 | 700,000 | 7,000,000 |
| recipients | 2,800 | 16,112 | 92,717 | 533,529 |
| revenue | $364k | $4.13M | $38.80M | $387.96M |
| cost_account_based | $40k | $400k | $4.00M | $40.00M |
| cost_transaction_based | $60k | $562k | $5.39M | $52.61M |
| cost_sponsor_fixed | $46k | $64k | $83k | $101k |
| contribution | $218k | $3.10M | $29.32M | $295.25M |
| contribution_margin | 60% | 75% | 76% | 76% |
| cost_per_account | $146 | $103 | $94.75 | $92.71 |
| cost_per_grant_unbound | $20.89 | $14.66 | $13.54 | $13.24 |
| sponsor_passthrough_rail_cost | $10k | $96k | $960k | $9.60M |
| onb_total_unbound | $245k | $757k | $5.00M | $43.31M |
| cac_per_sponsor | $125k | $125k | $125k | $125k |
| acquisition_and_onboarding_total | $370k | $882k | $5.13M | $43.43M |
| onb_per_account | $245 | $75.68 | $50.02 | $43.31 |
| onb_per_migrated_txn | $2.57 | $0.79 | $0.52 | $0.45 |
| onb_engineering_hours | 800 | 800 | 800 | 800 |
| onb_charity_enrolment | $31k | $178k | $1.03M | $5.91M |
| onb_sponsor_hours | 584 | 934 | 1,922 | 9,016 |
| onb_sponsor_cost | $41k | $65k | $135k | $631k |
| buyer_switching_tco | $170k | $280k | $350k | $846k |
| time_to_production_weeks | 31 | 33 | 35 | 37 |
| payback_months | 20.4 | 3.4 | 2.1 | 1.8 |
| payback_months_onboarding_only | 13.5 | 2.9 | 2.0 | 1.8 |
| payback_months_at_81_per_account | never | never | never | never |
| payback_months_at_250_per_account | 42.8 | 7.2 | 4.0 | 3.3 |
| payback_months_at_737_per_account | 7.5 | 1.7 | 1.0 | 0.8 |
| first_sponsor_net_contribution | -$2.82M | $63k | $26.28M | $292.21M |
| first_sponsor_payback_months | never | 183.8 | 2.4 | 1.8 |
| four_sponsor_payback_months | never | 4.5 | 2.2 | 1.8 |
| sponsors_of_this_size_to_cover_fixed | 13.97 | 0.98 | 0.10 | 0.01 |
| breakeven_bps_recurring | 8.0 | 5.0 | 4.9 | 4.8 |
| breakeven_bps_incl_onboarding_amortised | 12.1 | 5.8 | 5.4 | 5.2 |
| breakeven_balance_at_fee | $110k | $60k | $53k | $51k |
| revenue_per_account | $364 | $413 | $388 | $388 |
| breakeven_price_per_account_incl_onboarding | $220 | $120 | $105 | $101 |
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
| onb_donor_reonboarding | $3,348 | $33k | $335k | $3.35M |
| onb_charity_enrolment | $31k | $178k | $1.03M | $5.91M |
| onb_third_party | $5,000 | $5,000 | $5,000 | $5,000 |
| onb_rehearsals | $7,854 | $12k | $16k | $20k |
| onb_unbound_legal | $15k | $15k | $15k | $15k |
| onb_failure_reserve | $20k | $50k | $269k | $2.08M |
| onb_predelegation | $28k | $212k | $2.05M | $20.38M |
| onb_total_unbound | $245k | $757k | $5.00M | $43.31M |
| cac_per_sponsor | $125k | $125k | $125k | $125k |
| acquisition_and_onboarding_total | $370k | $882k | $5.13M | $43.43M |


### R6 Fee sensitivity: payback months (base grants, typical data, base balance)

| Accounts | 10 bps | 15 bps | 18.5 bps | 20 bps | 30 bps |
|---|---|---|---|---|---|
| 1,000 | 124.6 (UNECONOMIC) | 35.1 (SEPARATE_ONBOARDING_FEE) | 23.3 (INCLUDE_IN_FEE) | 20.4 (INCLUDE_IN_FEE) | 11.1 (INCLUDE_IN_FEE) |
| 10,000 | 10.2 (INCLUDE_IN_FEE) | 5.1 (INCLUDE_IN_FEE) | 3.8 (INCLUDE_IN_FEE) | 3.4 (INCLUDE_IN_FEE) | 2.0 (INCLUDE_IN_FEE) |
| 100,000 | 6.2 (INCLUDE_IN_FEE) | 3.1 (INCLUDE_IN_FEE) | 2.3 (INCLUDE_IN_FEE) | 2.1 (INCLUDE_IN_FEE) | 1.3 (INCLUDE_IN_FEE) |
| 1,000,000 | 5.1 (INCLUDE_IN_FEE) | 2.6 (INCLUDE_IN_FEE) | 2.0 (INCLUDE_IN_FEE) | 1.8 (INCLUDE_IN_FEE) | 1.1 (INCLUDE_IN_FEE) |


### R7 Data quality: onboarding cost / payback months / time to production (20 bps, base)

| Accounts | Clean | Typical | Poor |
|---|---|---|---|
| 1,000 | $179k / 16.1 mo / 22 wk | $245k / 20.4 mo / 31 wk | $377k / 30.3 mo / 43 wk |
| 10,000 | $590k / 2.8 mo / 24 wk | $757k / 3.4 mo / 33 wk | $1.12M / 4.8 mo / 45 wk |
| 100,000 | $3.83M / 1.6 mo / 26 wk | $5.00M / 2.1 mo / 35 wk | $7.62M / 3.2 mo / 47 wk |
| 1,000,000 | $32.15M / 1.3 mo / 28 wk | $43.31M / 1.8 mo / 37 wk | $68.48M / 2.8 mo / 49 wk |


### R8 Balance case: contribution and payback (20 bps, typical, base grants)

| Accounts | Low balance | Base balance | High balance |
|---|---|---|---|
| 1,000 | $76k: $5,126 / 866.5 mo | $182k: $218k / 20.4 mo | $390k: $634k / 7.0 mo |
| 10,000 | $76k: $487k / 21.7 mo | $206k: $3.10M / 3.4 mo | $423k: $7.43M / 1.4 mo |
| 100,000 | $161k: $22.64M / 2.7 mo | $194k: $29.32M / 2.1 mo | $423k: $75.04M / 0.8 mo |
| 1,000,000 | $6,939: -$78.84M / never mo | $194k: $295.25M / 1.8 mo | $323k: $553.29M / 0.9 mo |


### R9 Grant volume: Unbound cost per account and contribution (20 bps, typical, base balance)

| Accounts | Low grants (5.6) | Base (7.0) | High (12.3) |
|---|---|---|---|
| 1,000 | $134/acct; $230k | $146/acct; $218k | $192/acct; $172k |
| 10,000 | $91.40/acct; $3.21M | $103/acct; $3.10M | $145/acct; $2.68M |
| 100,000 | $83.96/acct; $30.40M | $94.75/acct; $29.32M | $136/acct; $25.24M |
| 1,000,000 | $82.19/acct; $305.77M | $92.71/acct; $295.25M | $133/acct; $255.41M |


### R10 Cost case at 20 bps (typical data, base grants/balance): payback months

| Accounts | Low cost | Base cost | High cost |
|---|---|---|---|
| 1,000 | 4.9 ($73k) | 20.4 ($245k) | never ($1.01M) |
| 10,000 | 0.7 ($160k) | 3.4 ($757k) | 3305.6 ($4.26M) |
| 100,000 | 0.3 ($908k) | 2.1 ($5.00M) | 473.1 ($31.80M) |
| 1,000,000 | 0.3 ($7.78M) | 1.8 ($43.31M) | 214.1 ($293.77M) |


### R11 Classification counts across 27 grants x quality x balance combinations (base cost)

| Accounts | Fee bps | INCLUDE_IN_FEE | SEPARATE_ONBOARDING_FEE | UNECONOMIC |
|---|---|---|---|---|
| 1,000 | 10 | 5 | 4 | 18 |
| 1,000 | 15 | 10 | 6 | 11 |
| 1,000 | 18.5 | 13 | 5 | 9 |
| 1,000 | 20 | 14 | 4 | 9 |
| 1,000 | 30 | 18 | 4 | 5 |
| 10,000 | 10 | 16 | 2 | 9 |
| 10,000 | 15 | 18 | 2 | 7 |
| 10,000 | 18.5 | 21 | 3 | 3 |
| 10,000 | 20 | 23 | 1 | 3 |
| 10,000 | 30 | 26 | 1 | 0 |
| 100,000 | 10 | 23 | 4 | 0 |
| 100,000 | 15 | 27 | 0 | 0 |
| 100,000 | 18.5 | 27 | 0 | 0 |
| 100,000 | 20 | 27 | 0 | 0 |
| 100,000 | 30 | 27 | 0 | 0 |
| 1,000,000 | 10 | 18 | 0 | 9 |
| 1,000,000 | 15 | 18 | 0 | 9 |
| 1,000,000 | 18.5 | 18 | 0 | 9 |
| 1,000,000 | 20 | 18 | 0 | 9 |
| 1,000,000 | 30 | 18 | 0 | 9 |


### R12 Value of the two tracks to Unbound (20 bps, base case, typical data)

| Value item | 1,000 | 10,000 | 100,000 | 1,000,000 |
|---|---|---|---|---|
| value_epay_sponsor_passthrough_saving_yr | $0.00 | $0.00 | $0.00 | $0.00 |
| value_epay_unbound_labour_saving_yr | $0.00 | $0.00 | $0.00 | $0.00 |
| value_network_enrolment_avoided_at_onboarding | $15k | $89k | $513k | $2.95M |
| value_sales_cycle_reduction | $54k | $776k | $7.33M | $73.81M |
| onboarding_fee_to_meet_include_threshold | $0.00 | $0.00 | $0.00 | $0.00 |
| term_contribution_after_onboarding | $718k | $14.63M | $141.48M | $1.43B |


### R13 Stress case: 1,000 accounts, high grants, poor data, low balance, 20 bps

| Metric | Value |
|---|---|
| avg_balance | $76k |
| aua | $75.68M |
| grants_per_year | 12,300 |
| recipients | 4,920 |
| revenue | $151k |
| cost_account_based | $40k |
| cost_transaction_based | $106k |
| cost_sponsor_fixed | $65k |
| contribution | -$59k |
| contribution_margin | -39% |
| cost_per_account | $211 |
| cost_per_grant_unbound | $17.13 |
| sponsor_passthrough_rail_cost | $17k |
| onb_total_unbound | $439k |
| cac_per_sponsor | $125k |
| acquisition_and_onboarding_total | $564k |
| onb_per_account | $439 |
| onb_per_migrated_txn | $2.89 |
| onb_engineering_hours | 1,600 |
| onb_charity_enrolment | $54k |
| onb_sponsor_hours | 951 |
| onb_sponsor_cost | $67k |
| buyer_switching_tco | $195k |
| time_to_production_weeks | 43 |
| payback_months | never |
| payback_months_onboarding_only | never |
| payback_months_at_81_per_account | never |
| payback_months_at_250_per_account | 172.0 |
| payback_months_at_737_per_account | 12.8 |
| first_sponsor_net_contribution | -$3.10M |
| first_sponsor_payback_months | never |
| four_sponsor_payback_months | never |
| sponsors_of_this_size_to_cover_fixed | n/a |
| breakeven_bps_recurring | 27.8 |
| breakeven_bps_incl_onboarding_amortised | 42.7 |
| breakeven_balance_at_fee | $162k |
| revenue_per_account | $151 |
| breakeven_price_per_account_incl_onboarding | $323 |
| classification | UNECONOMIC |


### R14 Non-included combinations for small sponsors (1,000 accounts, base cost)

| Fee bps | Grants | Data | Balance | Contribution/yr | Onboarding (excl. CAC) | Payback mo (incl. CAC) | Fee to reach 24 mo (incl. CAC) | Class |
|---|---|---|---|---|---|---|---|---|
| 10 | low | clean | low | -$49k | $168k | never | $293k | UNECONOMIC |
| 20 | low | clean | low | $27k | $168k | 132.2 | $240k | UNECONOMIC |
| 10 | low | clean | base | $57k | $168k | 61.6 | $179k | UNECONOMIC |
| 10 | low | typical | low | -$59k | $232k | never | $357k | UNECONOMIC |
| 20 | low | typical | low | $17k | $232k | 250.1 | $323k | UNECONOMIC |
| 10 | low | typical | base | $48k | $232k | 90.0 | $262k | UNECONOMIC |
| 10 | low | poor | low | -$77k | $361k | never | $486k | UNECONOMIC |
| 20 | low | poor | low | -$1,742 | $361k | never | $486k | UNECONOMIC |
| 10 | low | poor | base | $29k | $361k | 202.5 | $428k | UNECONOMIC |
| 20 | low | poor | base | $211k | $361k | 27.7 | $64k | SEPARATE_ONBOARDING_FEE |
| 10 | low | poor | high | $237k | $361k | 24.6 | $12k | SEPARATE_ONBOARDING_FEE |
| 10 | base | clean | low | -$61k | $179k | never | $304k | UNECONOMIC |
| 20 | base | clean | low | $15k | $179k | 250.5 | $275k | UNECONOMIC |
| 10 | base | clean | base | $45k | $179k | 80.9 | $214k | UNECONOMIC |
| 10 | base | typical | low | -$71k | $245k | never | $370k | UNECONOMIC |
| 20 | base | typical | low | $5,126 | $245k | 866.5 | $360k | UNECONOMIC |
| 10 | base | typical | base | $36k | $245k | 124.6 | $299k | UNECONOMIC |
| 10 | base | poor | low | -$89k | $377k | never | $502k | UNECONOMIC |
| 20 | base | poor | low | -$14k | $377k | never | $502k | UNECONOMIC |
| 10 | base | poor | base | $17k | $377k | 359.5 | $468k | UNECONOMIC |
| 20 | base | poor | base | $199k | $377k | 30.3 | $105k | SEPARATE_ONBOARDING_FEE |
| 10 | base | poor | high | $225k | $377k | 26.8 | $52k | SEPARATE_ONBOARDING_FEE |
| 10 | high | clean | low | -$107k | $221k | never | $346k | UNECONOMIC |
| 20 | high | clean | low | -$31k | $221k | never | $346k | UNECONOMIC |
| 10 | high | clean | base | -$434 | $221k | never | $346k | UNECONOMIC |
| 10 | high | typical | low | -$116k | $293k | never | $418k | UNECONOMIC |
| 20 | high | typical | low | -$40k | $293k | never | $418k | UNECONOMIC |
| 10 | high | typical | base | -$9,882 | $293k | never | $418k | UNECONOMIC |
| 20 | high | typical | base | $172k | $293k | 29.2 | $74k | SEPARATE_ONBOARDING_FEE |
| 10 | high | typical | high | $198k | $293k | 25.3 | $22k | SEPARATE_ONBOARDING_FEE |
| 10 | high | poor | low | -$135k | $439k | never | $564k | UNECONOMIC |
| 20 | high | poor | low | -$59k | $439k | never | $564k | UNECONOMIC |
| 10 | high | poor | base | -$29k | $439k | never | $564k | UNECONOMIC |
| 20 | high | poor | base | $153k | $439k | 44.2 | $257k | SEPARATE_ONBOARDING_FEE |
| 10 | high | poor | high | $179k | $439k | 37.7 | $205k | SEPARATE_ONBOARDING_FEE |


### R16 History depth: onboarding cost / per-transaction share / payback (20 bps, base, typical data)

| Accounts | Short (33 months, AEF) | Mid (7 years, GWCF) | Full (20 years ramped) |
|---|---|---|---|
| 1,000 | $236k / 1% / 19.9 mo | $240k / 2% / 20.1 mo | $245k / 4% / 20.4 mo |
| 10,000 | $670k / 4% / 3.1 mo | $703k / 8% / 3.2 mo | $757k / 14% / 3.4 mo |
| 100,000 | $4.13M / 6% / 1.7 mo | $4.46M / 12% / 1.9 mo | $5.00M / 21% / 2.1 mo |
| 1,000,000 | $34.59M / 7% / 1.4 mo | $37.90M / 15% / 1.5 mo | $43.31M / 24% / 1.8 mo |


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



### R18 Marginal vs first-sponsor vs four-equal-sponsor view (20 bps and 10 bps, C0, base cost, typical data)

| Accounts | bps | Marginal contribution | Marginal payback mo | Platform fixed/yr | First-sponsor net | First-sponsor payback mo | 4-sponsor payback mo | Sponsors to cover fixed |
|---|---|---|---|---|---|---|---|---|
| 1,000 | 20 | $218k | 20.4 | $3.04M | -$2.82M | never | never | 13.97 |
| 10,000 | 20 | $3.10M | 3.4 | $3.04M | $63k | 183.8 | 4.5 | 0.98 |
| 100,000 | 20 | $29.32M | 2.1 | $3.04M | $26.28M | 2.4 | 2.2 | 0.10 |
| 1,000,000 | 20 | $295.25M | 1.8 | $3.04M | $292.21M | 1.8 | 1.8 | 0.01 |
| 1,000 | 10 | $36k | 124.6 | $3.04M | -$3.00M | never | never | 85.25 |
| 10,000 | 10 | $1.04M | 10.2 | $3.04M | -$2.00M | never | 38.1 | 2.93 |
| 100,000 | 10 | $9.92M | 6.2 | $3.04M | $6.88M | 9.1 | 6.7 | 0.31 |
| 1,000,000 | 10 | $101.27M | 5.1 | $3.04M | $98.23M | 5.3 | 5.2 | 0.03 |


High cost case at 20 bps: first-sponsor net 1,000: -$6.82M; 10,000: -$6.64M.



### R19 CNV-ECO-005 stresses on marginal contribution (20 bps, C0, base cost, typical data)

| Metric | 1,000 | 10,000 | 100,000 | 1,000,000 |
|---|---|---|---|---|
| contribution | $218k | $3.10M | $29.32M | $295.25M |
| stress_aua_decline_contribution | $163k | $2.48M | $23.50M | $237.05M |
| stress_price_pressure_contribution | $145k | $2.28M | $21.56M | $217.66M |
| stress_december_surge_contribution | $212k | $3.05M | $28.84M | $290.51M |
| stress_combined_contribution | $96k | $1.73M | $16.42M | $166.37M |
| stress_combined_payback_months | 46.4 | 6.1 | 3.7 | 3.1 |
| stress_combined_four_sponsor_net_each | -$664k | $971k | $15.66M | $165.61M |


### R20 Price benchmarks: payback months (incl. CAC) at observed price points (C0, typical data, base balance)

| Accounts | Cost case | 18.5 bps (Ren at MS GIFT) | $81/acct (Ren software, NCF) | $150/acct | $250/acct | $737/acct (Ren staffed, MS GIFT) | Break-even $/acct |
|---|---|---|---|---|---|---|---|
| 1,000 | base | 23.3 | never | 1182.0 | 42.8 | 7.5 | $220 |
| 1,000 | high | never | never | never | never | 70.6 | $775 |
| 10,000 | base | 3.8 | never | 22.3 | 7.2 | 1.7 | $120 |
| 10,000 | high | never | never | never | never | 16.6 | $501 |
| 100,000 | base | 2.3 | never | 11.1 | 4.0 | 1.0 | $105 |
| 100,000 | high | never | never | never | never | 10.8 | $444 |
| 1,000,000 | base | 2.0 | never | 9.1 | 3.3 | 0.8 | $101 |
| 1,000,000 | high | never | never | never | never | 9.7 | $430 |


### R21 Lever case: C0 (no levers, base) vs C (AI-native levers) at 20 bps, base cost, typical data

| Metric | 1,000 C0 | 1,000 C | 10,000 C0 | 10,000 C | 100,000 C0 | 100,000 C | 1,000,000 C0 | 1,000,000 C |
|---|---|---|---|---|---|---|---|---|
| cost_per_account | $146 | $84.31 | $103 | $55.56 | $94.75 | $50.67 | $92.71 | $49.48 |
| cost_per_grant_unbound | $20.89 | $12.04 | $14.66 | $7.94 | $13.54 | $7.24 | $13.24 | $7.07 |
| contribution | $218k | $279k | $3.10M | $3.57M | $29.32M | $33.73M | $295.25M | $338.48M |
| onb_total_unbound | $245k | $238k | $757k | $689k | $5.00M | $4.32M | $43.31M | $36.53M |
| payback_months | 20.4 | 15.6 | 3.4 | 2.7 | 2.1 | 1.6 | 1.8 | 1.3 |
| first_sponsor_payback_months | never | never | 183.8 | 20.1 | 2.4 | 1.8 | 1.8 | 1.3 |
| breakeven_price_per_account_incl_onboarding | $220 | $157 | $120 | $71.84 | $105 | $59.57 | $101 | $56.81 |


### R22 Monte Carlo (2,000 seeded draws, independent triangular(low, base, high) per parameter): P10 / P50 / P90

| Accounts | bps | Levers | Contribution | Onboarding+CAC | Marginal payback mo | First-sponsor payback mo | 4-sponsor payback mo | Draws contribution>0 | Draws INCLUDE |
|---|---|---|---|---|---|---|---|---|---|
| 1,000 | 10 | C0 | -$49k / -$585 / $32k | $392k / $459k / $539k | 174.0 / never / never | never / never / never | never / never / never | 50% | 0% |
| 10,000 | 10 | C0 | $289k / $719k / $1.00M | $922k / $1.12M / $1.38M | 12.3 / 19.0 / 49.2 | never / never / never | 104.1 / never / never | 98% | 69% |
| 100,000 | 10 | C0 | $2.83M / $7.03M / $9.68M | $5.09M / $6.64M / $8.71M | 7.1 / 11.8 / 31.5 | 12.0 / 26.0 / never | 8.0 / 13.6 / 47.1 | 98% | 86% |
| 1,000,000 | 10 | C0 | $34.13M / $72.85M / $99.25M | $41.54M / $56.08M / $76.28M | 5.8 / 9.5 / 22.2 | 6.0 / 10.0 / 25.0 | 5.8 / 9.6 / 22.7 | 98% | 91% |
| 1,000 | 20 | C0 | $131k / $181k / $214k | $388k / $458k / $537k | 23.9 / 30.9 / 44.6 | never / never / never | never / never / never | 100% | 11% |
| 10,000 | 20 | C0 | $2.35M / $2.80M / $3.07M | $934k / $1.14M / $1.38M | 3.9 / 4.9 / 6.6 | never / never / never | 5.6 / 7.5 / 11.0 | 100% | 100% |
| 100,000 | 20 | C0 | $22.10M / $26.36M / $29.04M | $5.07M / $6.64M / $8.92M | 2.2 / 3.1 / 4.4 | 2.6 / 3.7 / 5.4 | 2.3 / 3.2 / 4.6 | 100% | 100% |
| 1,000,000 | 20 | C0 | $225.59M / $266.30M / $293.53M | $41.58M / $55.97M / $75.48M | 1.8 / 2.6 / 3.7 | 1.9 / 2.6 / 3.7 | 1.8 / 2.6 / 3.7 | 100% | 100% |
| 1,000 | 10 | C | $49k / $72k / $92k | $379k / $450k / $530k | 54.7 / 74.8 / 115.4 | never / never / never | never / never / never | 100% | 0% |
| 10,000 | 10 | C | $1.17M / $1.34M / $1.48M | $868k / $1.04M / $1.25M | 7.4 / 9.3 / 11.9 | never / never / never | 18.8 / 31.9 / 115.0 | 100% | 100% |
| 100,000 | 10 | C | $11.32M / $12.86M / $14.19M | $4.46M / $5.77M / $7.35M | 4.1 / 5.4 / 7.3 | 5.7 / 7.8 / 11.1 | 4.4 / 5.8 / 7.9 | 100% | 100% |
| 1,000,000 | 10 | C | $114.99M / $131.41M / $143.36M | $36.56M / $47.83M / $62.56M | 3.3 / 4.4 / 6.1 | 3.4 / 4.6 / 6.3 | 3.3 / 4.4 / 6.1 | 100% | 100% |
| 1,000 | 20 | C | $231k / $255k / $274k | $381k / $449k / $527k | 17.5 / 21.3 / 25.8 | never / never / never | never / never / never | 100% | 78% |
| 10,000 | 20 | C | $3.24M / $3.42M / $3.54M | $864k / $1.04M / $1.25M | 3.0 / 3.7 / 4.5 | 35.0 / never / never | 4.1 / 5.1 / 6.4 | 100% | 100% |
| 100,000 | 20 | C | $30.68M / $32.26M / $33.53M | $4.44M / $5.73M / $7.32M | 1.6 / 2.1 / 2.8 | 1.9 / 2.5 / 3.2 | 1.7 / 2.2 / 2.9 | 100% | 100% |
| 1,000,000 | 20 | C | $309.11M / $324.87M / $337.22M | $36.05M / $47.28M / $62.36M | 1.3 / 1.7 / 2.4 | 1.3 / 1.8 / 2.4 | 1.3 / 1.8 / 2.4 | 100% | 100% |


### R15 Registry fixed cost per grant by network grant volume (annual fixed + establishment over 5 yrs)

| Network grants/yr | Low | Base | High |
|---|---|---|---|
| 70,000 | $1.86 | $5.42 | $12.68 |
| 700,000 | $0.19 | $0.54 | $1.27 |
| 3,000,000 | $0.04 | $0.13 | $0.30 |
| 7,000,000 | $0.02 | $0.05 | $0.13 |

## 7. Conflicts and tensions with ratified decisions and existing models

None of these is a conflict that requires a change. Each is flagged for the coordinator.

- **CNV-EXP-002 (full fund history at migration)** is a major onboarding cost driver: 14-24% of C0 onboarding cost at 10k-1M accounts with 20 years of ramped history (R16). It is second to pre-delegation and charity enrolment. It is not a conflict. But the cost depends on how reconciliation is designed (see ECO-RC-2). Predecessors may also hold less than full history; AEF's held 33 months. A 'history available at source, gaps disclosed' clarification is needed (ECO-RC-7).
- **Release-1 scope (ADVB-01).** A proposed R1 with 'no migration' conflicts with CNV-EXP-002 (initial-implementation) and the CNV-ECO-003 shadow-replay amendment. These economics assume migration is in scope. Without it, the CNV-ECO-004 entry segment cannot be served.
- **CNV-PAY-001 / CNV-LEG-001 (sponsor originates; Unbound holds no funds).** E-payment rail savings accrue to the sponsor, not to Unbound's P&L. Unbound captures only labour savings (about $0.48 per grant shifted) and a stronger sales argument. Stripe and other facilitator payout products are cited only for price benchmarks. Using them as a rail would need a partner acting as the sponsor's agent.
- **The Unbound `parameters.json` value `sponsor_onboarding_cost` of $60k** (flat, amortised over 5 years) and the 05a "sponsor onboarding and exit" line understate onboarding above about 3k accounts. This model gives $43.76 per account at 10k and $22.61 at 100k, one-time, excluding CAC. Recommend reconciling the two models.
- **CNV-ECO-004 entry segment (about 5k-50k funds) is supported only as an added-sponsor result (ADVX-03).** At C0, a 10k-account sponsor is INCLUDE_IN_FEE in 21-23 of 27 combinations at 18.5-20 bps, at Low confidence. As a first sponsor it nets about $63k a year after platform fixed cost. The segment also requires migration (ADVB-01).
- **CNV-ECO-003 / CNV-ECO-005 (ADVX-04).** Revision 3 meets: C0 base, P10/P50/P90, viability at P90 cost (marginal contribution is positive in 100% of draws at 10k+ accounts and 20 bps), the stresses, pre-delegation, and the 25% concentration cap as a view. **Not met:** adverse licence scale (no licence term in this model); correlated parameter draws; levers measured rather than assumed. These are flagged, not hidden.
- **CNV-ECO-004 concentration cap.** Any start with one sponsor exceeds the 25% cap. The four-equal-sponsor view is the earliest cap-conformant state.
- **Exit symmetry (ADVB-11).** Revision 1's termination-fee recommendation conflicted with the exit-symmetry position in 10 and 11. It is withdrawn (section 4).

## Implications for Unbound

1. **Price onboarding by gate, not by hope.**
   - Require a paid or free pre-contract **data-quality profile** that measures:
     - account mapping exception rate;
     - historical transaction break rate;
     - number of custom integrations;
     - the share of the sponsor's recipients covered by networked partners.
   - Include onboarding in the fee only inside the thresholds in section 4.
2. **Set a minimum annual fee of about $220k at C0** (about $160k if the levers are proven), or per-account floors, for sponsors under about 3-5k accounts. Servicing-economics' $100-110k excluded CAC and used AI-native minutes. Do not rely on onboarding fees for small sponsors, because those fees exceed first-year revenue.
3. **Invest in Track B automation and in reducing buyer effort before registry breadth.** Each percentage point of transaction-exception rate costs about $104k per 10k-account sponsor (ramped 20-year history at 10 minutes per exception). The buyer's own switching TCO is about $280k. The registry costs about $75k a year in total.
4. **Use the network as a switching-cost neutraliser.**
   - Reuse partner enrolments (CNV-EXP-002) and registry evidence (CNV-GRT-003). Each one halves the direct-enrolment bill at onboarding.
   - Quote the e-payment saving (about $1.07 per grant shifted, roughly half to the sponsor) in proposals as a sponsor benefit.
5. **Do not bid bps-only on processor-like books** (average balance under about $20k). Account-based cost exceeds asset revenue at any fee from 10 to 30 bps.
6. **Price by segment.** Staffed outsourced buyers (13-19 bps, about $737 per account) are serviceable at C0. Self-staffed software buyers ($34-326 per account; Ren at NCF $81) are not, until the levers are measured. The C0 cost floor of $101-120 per account leaves wide room under Ren-like anchors of about $737 per account. The constraints there are capacity, risk and the buyer's switching TCO, not unit cost.
7. **Treat the first one to three sponsors as design partners.** Use up-front or co-funded onboarding, a minimum fee, or a published introductory price step-down. Plan capital to carry about $3M a year of platform fixed cost until four sponsors are live.
8. **Fund the registry as a mandated cost**, staged to the first sponsor's recipients (ADVX-08). Do not market network savings before the CNV-ECO-003 shadow period has measured them.
9. **Never trade exit symmetry for onboarding recovery.** Charge out-of-gate onboarding up front. Any unamortised-recovery schedule must be straight-line and published, and export must never be conditional on payment.

## Candidate requirements (one line each)

- **ECO-RC-1 (refines CNV-EXP-002):** Before contract, the onboarding process SHALL produce a sponsor data-quality profile: account exception rate, historical transaction break rate, custom integration count, and partner-enrolment coverage of the sponsor's recipients. The profile SHALL feed a deterministic onboarding price and an estimated time to production.
- **ECO-RC-2 (refines CNV-EXP-002):** History migration SHALL reconcile aggregates per period and per fund first. Transaction-level exceptions SHALL be opened only where an aggregate breaks. Every imported transaction SHALL still be retained, append-only.
- **ECO-RC-3 (refines CNV-PAY-002 / UNB-CHAR):** The registry SHALL record verification method and cost class per destination (partner enrolment reused, instant ownership API, micro-deposit, bank letter) so that enrolment cost and reuse can be metered.
- **ECO-RC-4 (refines CNV-GRT-003):** The platform SHALL meter registry fixed and variable cost per grant and per charity in use, and SHALL report exception minutes per case, to replace ASSUMPTION parameters.
- **ECO-RC-5 (commercial; refines servicing-economics RC list):** Commercial terms SHALL support a minimum annual fee, an up-front onboarding fee for sponsors outside the gates, and overage per exception and per custom integration. Any early-exit recovery SHALL be limited to a published straight-line unamortised balance. Data export SHALL never be conditioned on payment or carry a fee.
- **ECO-RC-8 (refines CNV-ECO-003):** Sponsor economics SHALL be reported on the C0 base, with a marginal view, a first-sponsor (fixed-cost-bearing) view and a 25%-cap view, as P10/P50/P90, and with the CNV-ECO-005 stresses.
- **ECO-RC-9 (refines UNB-CHAR-DEC-001):** Registry scope SHALL be staged to recipients actually paid by contracted sponsors (federal sources and first-sponsor recipient resolution first). Registry run cost SHALL be metered per grant.
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
8. **Company-level viability.** The first-sponsor and four-sponsor views (R18) carry organisation fixed cost ($1.66M base) and build amortisation ($1.0M a year). These come from servicing-economics and Unbound and are not re-derived here. A full multi-year cash plan remains in `research/commercial-opportunity/servicing-economics/06-capital-and-runway.md` and `ai-native-capital-minimization/`.
9. **Lever measurement.** C0 vs C differ by about $470k a year of contribution per 10k-account sponsor, and by $48 per account in break-even price. Only the CNV-ECO-003 time study can resolve this.
10. **Payer economics.** A donor fee schedule minus the incumbent's realised take, per target sponsor, is not modelled quantitatively (ADVX-06).
11. **Correlation.** The Monte Carlo draws are independent. Correlated adverse draws (for example labour rate with minutes) would widen P90.
