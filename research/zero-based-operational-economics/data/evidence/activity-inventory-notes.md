# Operational activity inventory and requirement economic impact: method notes

Last reviewed: 2026-11-27. Outputs:

- [`../registers/operational-activities.csv`](../registers/operational-activities.csv): 180 activities (`OA-*`), 35 columns.
- [`../registers/requirement-economic-impact.csv`](../registers/requirement-economic-impact.csv): 51 requirement rows (`REI-*`), 19 columns.

Both files follow [`../CONVENTIONS.md`](../CONVENTIONS.md). They parse with the Python `csv` module, every row has the
header's field count, line endings are LF, and every enumerated field holds an allowed value. This work does not
modify Unbound.

## 1. Sources and versions

| Repository | Commit | Used for |
|---|---|---|
| `kemiller2002/unbound` (local clone) | `79b9258caa28861ae0a01df8b4608c50ab1dad79` | Requirement IDs, text, convergence clauses, Unbound's own work inventory |
| `daf-landscape` | `10b92f476fe9e9091880dd30224895cec3b74576` | Frequency, exception and minute baselines |

**Unbound files read.** `requirements/PRINCIPLES.md` and `requirements/AUTHORITATIVE-BASELINE.md` (index and precedence
rules). `requirements/baseline/baseline.jsonl` gave all 1,653 baseline rows (1,176 requirements, 395 records, 82
convergence clauses), with full text read for all 82 `CNV-*` clauses. I extracted ID and statement lists from the
domain files: `FULL-ACCOUNTING-SYSTEM.md`, `accounting/CANONICAL-CHART-AND-POSTING-RULES.md`,
`MULTI-PARTICIPANT-AND-SUCCESSOR-ACCOUNTS.md`, `PARTNER-SEGREGATION-AND-TENANCY.md`,
`grants/END-TO-END-GRANT-LIFECYCLE-AND-OPERATING-MODEL.md`, `grants/GRANT-EVENT-CATALOG-AND-EXCEPTION-RESOLUTION.md`,
`grants/MULTI-INVESTMENT-FUNDING-AND-PERCENTAGE-GRANTS.md`, `investments/*`,
`integrations/CUSTODIAN-AND-INVESTMENT-MANAGEMENT.md`, `charities/*`, `administration/*` (capability matrix ADM-001..048),
`governance/*` (GOV-AUTH, MON, OPS and SOC2 families), `ai/AI-NATIVE-INTERACTION-REQUIREMENTS.csv`,
`DEFERRED-PAYMENTS-AND-REMAINING-GAPS.md`, `ENTERPRISE-GAP-REGISTER-AND-CROSS-DOMAIN-SCENARIOS.md`, `BASELINE-001.md`,
`PLATFORM-UX-API-AND-ASSURANCE-STANDARDS.md` and the wave files (through the baseline). I also read the gap and
refinement records (`UNB-RCN-*`, `UNB-XIN-*`, `UNB-SMP-*`), the REQ-X canonical proposals and the TVR register
(`research/daf-theoretical-enterprise-validation/16-registers` and `19-questions`). Proposed records *outside* the
baseline were also used: `discovery/2026-11-25-availability-architecture` (UNB-AVL),
`2026-11-26-charity-network-and-onboarding` (UNB-CNET, UNB-ONB), `2026-11-26-file-ingestion` (UNB-ING) and
`2026-11-26-transitus-integration` (UNB-TRN). These are **proposed, not adopted**. The rows that cite them say so through
those ID prefixes. From `discovery/2026-11-24-simplification-economics/data/work-inventory.jsonl` I used Unbound's own
143-activity work inventory (SPW-001..143), which gives conventional and minimum-touch minutes at 100k accounts. Other
inputs: `requirements/open-questions.csv` (365 rows; open questions that bear on cost) and the names in `architecture/`.

**Every requirement ID cited in `unbound_requirements` exists** in the baseline or in those four proposed JSONL files.
This was checked by script, with zero misses. The only `none-found` is OA-COM-012 (training).

**daf-landscape baselines used.** `data/commercial-opportunity/servicing-economics/activities.csv` (ACT-A01..A26,
S01..S07). `research/competitive-displacement/data/model-inputs/events.csv` and `registers/operational-events.csv`
(EV-E01..E25). `research/file-ingestion-and-straight-through-processing/03` and `09` (FIE).
`research/competitive-advantage/charity-network-and-onboarding/06-continuous-vetting.md` (human vetting cases: 2.2 / 5.1
/ 14.9 per 1,000 grants) and `20-economic-analysis.md` (onboarding hours, destination verification fallback, charity
support desk). The decision records in `docs/` (automated charity assurance 180-day, financial core control spec v0.5,
recurring contributions, grant scheduling and fees).

Evidence-source shorthand in the CSVs: `dl:` means daf-landscape (ACT-*, EV-*, FIE, charity-network NN) and `ub:` means
unbound (requirement IDs, SPW-* work inventory rows).

## 2. Method

1. **Zero-based inventory.** Each activity was derived from what Unbound's requirements make necessary, not from
   incumbent org charts. It was then cross-checked against ACT/EV (daf-landscape), SPW (Unbound) and the FIE workflow
   inventory to find missed activities. ID prefixes: ACN = ACCOUNT, CON = CONTRIB, GRT = GRANT, CHR = CHARITY,
   INV = INVEST, ACG = ACCOUNTING, CMP = COMPLIANCE, TEC = TECHOPS, COM = COMMERCIAL.
2. **Anchoring.** Where an ACT or EV row exists, its frequency and touch rate were used as given. For EV-derived minutes,
   `minutes = d_native / 0.6`, which removes the embedded AI factor (for example EV-E10: 25.2 / 0.6 = 42). ACT
   `minutes_ai_native` values are *expected minutes over all occurrences*, so touched minutes were inferred as
   expected minutes ÷ touch rate, and those rows say so. Where only Unbound SPW data exists, SPW conventional and
   minimum-touch minutes bound the range, and the row is marked ASSUMPTION. Everything else is ASSUMPTION with wide
   ranges.
3. **Expected human minutes** = units(driver) × freq × exception × minutes. Reference scenario: 10,000 accounts;
   1,200 new accounts/yr (ACT-A01 base 0.12); 90,000 grants (ACT-A07 base 9.0); 25,000 contributions (EV-E03 base
   2.5); 5 sponsors; **1 sponsor onboarding per year (ASSUMPTION)**; 13,500 active recipient charities. The charity
   count is an INFERENCE: ACT-A09 gives 2.7 renewals per account-year, and two 180-day renewals per charity-year gives
   1.35 charities per account.
4. **External cost** is the cost per *occurrence of the activity* (the frequency unit), not per touched event. Annual
   external cost = units × freq × cost. `UNKNOWN` marks costs not established; no placeholder price was invented.
5. **Consolidation.** The first draft had 198 rows. Eighteen sub-steps that share the same driver were merged into their
   parent (listed in each kept row's description and evidence). Where the merged row had human minutes, the kept row's
   minutes were rescaled so the combined base expected minutes are preserved (noted `merge:` in `evidence_sources`).
   IDs were then renumbered once. This is the first publication, so no published ID was reused.
6. **REI register.** For each requirement with material recurring cost, minutes per 1k accounts = the scenario minutes
   of its linked activities ÷ 10. Activities are shared between requirements, so **REI minutes are not additive**.
   Per-sponsor activities assume 2,000 accounts per sponsor and do not scale linearly.

## 3. Results at the reference scenario

**Total expected human time: 23,358 hours/yr (base).** At 1,600 productive hours per FTE (FIE parameter) that is about
14.6 FTE. The low-to-high envelope is 3.7 to 67.5 FTE, from multiplying all lows or all highs. That envelope is not a
confidence interval, because the lows and highs are not jointly likely. External pass-through cost is about $317k/yr,
mostly check printing and mail ($119k), securities receive fees ($100k) and ACH ($18k). Most of it is borne by the
sponsor.

| Classification | Activities | Hours/yr |
|---|---|---|
| HUMAN-JUDGMENT | 24 | 7,702 |
| AI-ASSISTED | 18 | 5,115 |
| AUTO-EXCEPTION | 54 | 4,249 |
| SHARED-ECHELON | 20 | 2,152 |
| SPONSOR-OWNED | 19 | 1,420 |
| INDEPENDENT-AUTHORIZATION | 13 | 1,236 |
| EXTERNAL-PROVIDER | 7 | 836 |
| DETERMINISTIC | 22 | 647 |
| ELIMINATED (deferred scope: cards, foreign/ER grants, UBIT) | 3 | 0 |
| PREVENTED | 0 | — |

By responsible entity: sponsor 11,811 h; administrator 4,920 h; shared Echelon 4,736 h; bank/payment provider 868 h;
software provider 548 h; custodian 440 h. Fifteen activities require an independent second human.

### Top 15 activities by expected human minutes

| Rank | Activity | Classification | Responsible | Units × freq × exception × minutes | Minutes/yr | Hours/yr | Share |
|---|---|---|---|---|---|---|---|
| 1 | OA-GRT-005 Exception grant review and decision (Tier 2 / reserved A4) | HUMAN-JUDGMENT | sponsor | 90,000 grants × 1.0 × 0.09 × 42 | 340,200 | 5,670 | 24.3% |
| 2 | OA-ACG-007 Monthly close, financial reporting and controller sign-off | AI-ASSISTED | sponsor | 5 sponsors × 12 × 1.0 × 1,250 | 75,000 | 1,250 | 5.4% |
| 3 | OA-ACN-008 Human-handled donor and advisor service contacts | AI-ASSISTED | administrator | 10,000 accounts × 0.5 × 0.8 × 17 | 68,000 | 1,133 | 4.9% |
| 4 | OA-ACG-004 Reconciliation break investigation | AUTO-EXCEPTION | administrator | 10,000 × 12.5 × 0.02 × 17 | 42,500 | 708 | 3.0% |
| 5 | OA-ACG-011 Year-end external audit support | AI-ASSISTED | sponsor | 5 × 1 × 1.0 × 7,200 | 36,000 | 600 | 2.6% |
| 6 | OA-CON-004 Unidentified receipt attribution | AUTO-EXCEPTION | administrator | 25,000 contributions × 1.0 × 0.04 × 33 | 33,000 | 550 | 2.4% |
| 7 | OA-COM-007 Sponsor implementation and configuration | AI-ASSISTED | shared_echelon | 1 onboarding × 1 × 1.0 × 30,000 | 30,000 | 500 | 2.1% |
| 8 | OA-GRT-013 Paper check grants with positive pay and mailing | EXTERNAL-PROVIDER | bank/payment provider | 90,000 × 0.33 × 0.06 × 14.4 | 25,661 | 428 | 1.8% |
| 9 | OA-CON-005 Publicly traded securities gift receipt and valuation | AUTO-EXCEPTION | custodian | 25,000 × 0.4 × 0.08 × 30.6 | 24,480 | 408 | 1.7% |
| 10 | OA-ACN-023 Major-donor stewardship (optional sponsor service) | SPONSOR-OWNED | sponsor | 10,000 × 0.02 × 1.0 × 120 | 24,000 | 400 | 1.7% |
| 11 | OA-TEC-021 AI agent configuration, evaluation and change control | SHARED-ECHELON | shared_echelon | 1 platform × 12 × 1.0 × 1,920 | 23,040 | 384 | 1.6% |
| 12 | OA-COM-009 Data migration execution | AI-ASSISTED | shared_echelon | 1 × 1 × 1.0 × 22,000 | 22,000 | 367 | 1.6% |
| 13 | OA-GRT-012 Electronic grant payment execution | EXTERNAL-PROVIDER | bank/payment provider | 90,000 × 0.67 × 0.03 × 10.4 | 18,814 | 314 | 1.3% |
| 14 | OA-GRT-016 Uncashed/voided check outreach, reissue, escheat | AUTO-EXCEPTION | administrator | 90,000 × 1.0 × 0.01 × 19 | 17,100 | 285 | 1.2% |
| 15 | OA-GRT-001 Grant recommendation intake and affirmation | DETERMINISTIC | software_provider | 90,000 × 1.0 × 0.01 × 17.3 | 15,570 | 260 | 1.1% |

The top 15 make up 57% of base minutes. Exception grant review alone is a quarter of the total. It depends on the
EV-E10 touch rate (9%) times 42 unaided minutes, and both numbers are unmeasured for Unbound. The decisive measurement is
therefore Tier-2 trigger incidence and minutes per review in the CNV-ECO-003 shadow replay and time study.

## 4. Coverage gaps (not modelled, or modelled only as zero)

- **Deferred scope** is shown as ELIMINATED rows with zero base frequency: card contributions (CNV-PAY-008); foreign,
  ER and equivalency grants (CNV-GRT-002/007/008); UBIT accrual (CNV-FIN-010). Workplace/payroll giving is modelled at
  2% of contributions (REQ-X-070) because CNV-ECO-004 says it is not the entry segment.
- **Grant agreements, milestones, conditional grants and grantee impact reports** (UNB-GRANT-024, UNB-GRANT-042,
  EXC-11, EXC-16) have no activity row. There is no frequency baseline, and release-1 scope for conditional grants is
  unclear.
- **DAF-to-DAF inbound contributions** are folded into OA-CON-002/004.
- **Sponsor enterprise overhead** is excluded as not DAF-administration activity: board meetings beyond delegations,
  enterprise risk register, internal audit plan, metrics reviews, HR and payroll (SPW-120, 122, 123, 125, 130, 132,
  133). SPW-133 alone puts internal audit at 4,800-9,600 minutes per sponsor-year. Add it if the model needs full
  sponsor cost.
- **Echelon corporate functions** (finance, legal, hiring) are excluded except billing (OA-ACG-017), cost attribution
  (OA-ACG-018) and assurance.
- **The staffing floor is not an activity.** Reserved-authority coverage (CNV-GOV-004; the DecisionTeam default of 0.5
  FTE per holder, UNB-SMP-ORG-003#Q3), the three-distinct-person release (CNV-GOV-003) and the out-of-chain reconciler
  set a minimum headcount per sponsor regardless of minutes. They appear in the REI register (REI-002, REI-004), not as
  activity minutes. A per-sponsor floor of about 2.5 FTE could exceed the activity-driven minutes for small sponsors.
- **No row is classified PREVENTED.** Prevention appears as levers inside rows (EV prevention fields). There is no
  separate zero-minute row for each prevented activity.

## 5. Activities with no requirement that creates them

| Activity | Requirement status |
|---|---|
| OA-COM-012 training | `none-found`. CNV-GOV-004 requires only acknowledgment of §4958/§4966 manager status |
| OA-COM-001 sales | CNV-ECO-003/004 govern claims and segment, not the activity |
| OA-COM-002 procurement/DDQ | Only SOC2-020/036 (claims must match scope) |
| OA-COM-003 annual DDQ renewal | Same as OA-COM-002 |
| OA-COM-014 account management | Only ADM-033 SLA governance |
| OA-ACN-023 major-donor stewardship | Optional; CNV-LEG-001 bars operator-authored recommendations, so it can only be sponsor-owned |
| OA-TEC-011 software maintenance | CNV-ARC-005 governs how, not that |
| OA-TEC-019 support escalations | Only the generic case kernel |
| OA-ACN-012 mandatory-delivery retry | No baseline rate (UNB-RCN-WF-008 creates the duty) |

## 6. Requirements that create avoidable or overlapping recurring work

1. **Three sampling regimes over the same decisions.** UNB-XIN-CLM-005 (monthly stratified sample), CNV-GRT-011
   (decision-quality sampling) and CNV-GOV-008 (sampled reviews in the quarterly board report) overlap. One error-bound
   sampling plan could serve all three (REI-032, REI-033).
2. **Reconciliation assurance layered three times.** CNV-FIN-004 (independent attestation sample plus monthly controller
   sign-off) and CNV-GOV-003 (at least monthly independent review) overlap. The control objective is met by one
   independent attestation feeding the controller's sign-off.
3. **Daily next-day NAV sample (CNV-FIN-005).** CNV-FIN-005 itself (OD-M-07) says values come from the external
   manager's or custodian's positions and unit values. A daily independent sample of a figure Unbound does not compute
   is likely excessive. Weekly or risk-triggered sampling preserves the objective.
4. **Annual affiliation attestation (UNB-XIN-CRM-002).** The event-driven prefilled confirmation (SPD-ENT-004) removes
   a 10,000-form annual cycle.
5. **72-hour hold applied to all non-recurring recommendations when the sponsor sets no threshold (CNV-PLT-011).** This
   default will generate December holds and contacts. A platform default threshold is preferable.
6. **Monthly cost-attribution reconciliation (CNV-ECO-001).** This is Echelon-internal finance work; quarterly with
   automated monthly residual checks would suffice.
7. **One-sponsor-per-person reserved authority (SPD-ADV-001 via CNV-GOV-004).** This prevents pooling reviewers across
   sponsors, which turns reviewer capacity into a per-sponsor fixed cost. The rule is not unnecessary: it is an
   independence safeguard. It is the costliest governance choice, and its time-share default (0.5 FTE) is unvalidated.
8. **The pre-delegation phase (CNV-GRT-001, CNV-ECO-005)** makes every grant a human batch decision until a board
   resolution exists (OA-GRT-006, high case 90,000 decisions/yr). Making the delegation an activation gate removes this.
9. **The three-distinct-person release (CNV-GOV-003)** is necessary until the auditor and board accept the deterministic
   release design. Pursuing that acceptance at onboarding is the redesign, not removing the control.

No mandatory control is proposed for removal. Each alternative in the REI register states the control objective it
preserves.

## 7. Data problems and caveats

- **Nothing here is measured for Unbound.** 93 rows are ASSUMPTION, 80 INFERENCE, 4 VERIFIED-FACT (scope facts from
  CNV clauses) and 3 UNKNOWN. Confidence: 92 low, 84 medium, 4 high. CNV-EVB-001 requires exactly the measurements
  that would replace these numbers.
- **EV-E03 and EV-E10 have `d_native` greater than `d_conv`** (14 vs 8; 25.2 vs 12.4). This is plausible: fewer, harder
  residual cases. But it means "unaided" minutes after dividing by 0.6 (23 and 42) exceed conventional minutes per
  touch. I kept the anchor and flag it here.
- **ACT-S01 and ACT-S05 units are ambiguous.** The frequency column says sponsor-months or sponsor-quarters, but EV-E13
  and EV-E21 treat the minutes as per sponsor-year. I followed the EV interpretation (per sponsor-year), which is the
  smaller reading.
- **SPW complex-gift volume is 13 times ACT-A05.** SPW-026 has 4,000 per 100k accounts (0.04 per account); ACT-A05 has
  0.003. I anchored to ACT-A05 as instructed. The SPW figure would make complex gifts a top-5 driver.
- **Per-sponsor rows** (close, audit, release batches) are sensitive to the 5-sponsor / 2,000-accounts-per-sponsor
  split. At 1 sponsor with 10,000 accounts they fall by roughly 80%.
- **One sponsor onboarding per year is an assumption.** Onboarding and migration rows are one-off per sponsor and are
  shown as an annual run-rate only under that assumption.
- **REI minutes are not additive** (shared activities).
- **External costs marked UNKNOWN:** SOC examination fees, Nacha TPSP audit, penetration test, CA/HI registration fees,
  MDR/security tooling, sales cost, contract legal. Obtain quotes. Do not fill these from memory.
- **Policy questions still open:** RCD-005 (board delegation of routine approval), SPD-GRT-001 (deterministic renewal
  without sign-off) and UNB-XIN-TRS-004#Q1 (can POA agents exercise privileges). The rows that depend on them are
  marked `uncertain`.

## 8. Open questions

1. What are the measured Tier-2 trigger incidence and minutes per exception review (OA-GRT-005)? This one number
   carries 24% of the base.
2. Will auditors and boards accept the deterministic release gate (CNV-GOV-003), and how long does that take?
3. What time share per reserved-authority holder is actually needed (RR-UNB-ECO-003-r1#Q1)? Can contracted reviewers
   form a shared bench while each is appointed by only one sponsor?
4. How many sponsors get a board delegation before go-live, and how long is the pre-delegation phase (CNV-ECO-005)?
5. What are the real unidentified-receipt and securities orphan-delivery rates once intent capture is live
   (UNB-XIN-PAY-007, UNB-ING-DAF-001)?
6. What is the check share of grants after networked-rail reuse (CNV-EXP-002)? Checks drive OA-GRT-013, OA-GRT-016 and
   most external cost.
7. Can the three sampling regimes be consolidated into one plan acceptable to auditors (Section 6, item 1)?
8. What do SOC 1 type 2 plus SOC 2 type 2 examinations and the Nacha TPSP audit cost?
9. Does California or Hawaii platform registration apply to sponsor-direct deployments (CNV-LEG-002 interpretation)?
10. What are the December interval arrivals by activity (CNV-EVB-001), which size the surge bench in CNV-SVC-002?
11. Should sponsor enterprise overhead (internal audit, board meetings) be added to the activity model or kept in a
    separate overhead register?

## 9. Memory

The memory snapshot held no notes for this repository, and no memory content was used.
