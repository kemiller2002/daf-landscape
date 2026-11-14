# Queue Q-N15, P-LND-03 and P-PRC-01: BDC period fix, observed labour rates in AI-economics v2, and AOGF's Benevity payments

**Date:** 2026-11-14 · **Queue items:** Q-N15 (BDC schedule periods), P-LND-03 (observed labour rates in AI-economics v2), P-PRC-01 (AOGF / Benevity fee reconciliation) · **Recency:** 2021+ filings only

**Data written:**
- [`bdc-loans-daf-ecosystem.csv`](../../data/mission-2026-11-14/bdc-loans-daf-ecosystem.csv) (regenerated, 600 rows)
- [`bdc-loans-daf-ecosystem-v1.csv`](../../data/mission-2026-11-14/bdc-loans-daf-ecosystem-v1.csv) (the old 650-row file, kept unchanged)
- [`bdc-loans-latest-marks.csv`](../../data/mission-2026-11-14/bdc-loans-latest-marks.csv) (231 rows)
- [`ai-economics-v2b-results.csv`](../../data/mission-2026-11-14/ai-economics-v2b-results.csv) (12,916 rows)
- [`aogf-benevity-reconciliation.csv`](../../data/mission-2026-11-14/aogf-benevity-reconciliation.csv) (160 rows)
- [`queue-proposals-bdc-labour.csv`](../../data/mission-2026-11-14/queue-proposals-bdc-labour.csv) (4 proposals)

**Scripts:**
- [`scripts/mission_bdc_loans.py`](../../scripts/mission_bdc_loans.py) (fixed)
- [`scripts/mission_ai_economics_v2b.py`](../../scripts/mission_ai_economics_v2b.py) (new; imports v2 unchanged)
- [`scripts/mission_aogf_benevity_reconcile.py`](../../scripts/mission_aogf_benevity_reconcile.py) (new)

**Builds on:** [validation-wave8-report.md](validation-wave8-report.md) (bug report) · [queue-pe-lenders-labour-rates.md](queue-pe-lenders-labour-rates.md) · [ai-economics-v2-observed-costs.md](ai-economics-v2-observed-costs.md) · [queue-processor-economics-vendor-profiles.md](queue-processor-economics-vendor-profiles.md)

**Evidence tags:**
- **[F]**: read from a filing or a published document.
- **[S]**: computed by a script from filed data.
- **[I]**: inference.

---

## 1. Key findings

1. **Q-N15: fixed. Prior-period comparative rows now carry their own date.** [S] Of the 650 parsed schedule lines, **247 belong to a period other than the filing's own period**. This is the bug the wave-8 validation found. Each row now takes its date from the inline-XBRL context in the row (415 rows), else from the nearest "Schedule of Investments … *date*" heading (193), else from the filing period, which is flagged (16 table rows in documents with no XBRL and no dated heading, plus 14 text-only hits).
   - **Deduplication: 650 rows became 600.**
     - 21 rows were the same filing row matched by two search phrases ("Bonterra" and "CyberGrants").
     - 29 rows repeated, in a later filing's comparative schedule, a line already reported for the same period.
   - **Comparatives that remain: 206.** These are periods that appear only as comparatives in the filings that were searched.
2. **Bonterra: the 9/8/2027 loan's last marks are 2024, and the 3/5/2032 facility is the live one.** [S]
   - **The 2027 loan.** Its latest-mark rows are now dated as follows:
     - Golub Capital BDC: 2024-09-30, facility 98.5%.
     - Golub Capital Direct Lending: 2024-09-30, 98.5%.
     - BlackRock TCP: 2024-12-31, 99.3%.
     - BlackRock Direct Lending: 2024-12-31, 99.3%.
     - Monroe Capital: 2024-12-31, 99.4%.

     Each of these is flagged `not_in_schedule_at_<2025 period-end>`.
   - **The S+4.75–5.00% facility due 3/5/2032** is held at **2026-09-30** at 99.0–99.5%:
     - AB Private Credit Investors and AB Private Lending Fund: S+5.00%, 99.0%;
     - CCS IX: S+5.00%, 99.0%;
     - Crescent: S+4.75%, 99.0%;
     - FS KKR: SF+4.8 (as printed), $133.4m par, 99.5%;
     - KKR FS Income Trust and KKR FS Income Trust Select: 99.4%.
   - The `identity_note` now reads "probable: 2025 refinancing of Apax Bonterra".
3. **Audax / Foundation Source marks are correct and dated.** [S]
   - **Latest (2026-09-30).** Term loan $13,365,065, DDTL $4,208,879 and revolver $343,575 (revolver due 9/6/2029). All are at S+5.00%, due 9/6/2030 except the revolver, and all at 100% of par. Class A and Class B LP interests are at **1.38× cost**.
   - **2025-12-31.** The comparatives in the same 10-Q carry this date ($13,468,138 term loan, LP interests at 1.44× cost), so they no longer overstate the latest period.
4. **P-LND-03: in v2, swapping in observed labour rates changes almost nothing, by construction.** [S]
   - **Why.** v2 sets each archetype's pool as *observed opex × observed labour share × φ*. The loaded rate only sets the mix across P01–P15.
   - **Scaling every rate to the sponsor's observed rate (V2B_SCALED)** reproduces v2 exactly: the maximum relative difference is 3×10⁻¹⁵.
   - **Putting every process at the sponsor's single observed all-staff rate (V2B_UNIFORM)** moves the mean P(rank first) by at most 1.0 point (net of fixed cost) and 0.03 points (gross). Platform break-even p50 moves by 0–2 sponsors for nationals and CF_1BN, and by up to 41 sponsors for CF_250M and CF_SMALL, from bases of 236–718. The modal winner changes in 1 of 75 archetype × process cells (NAT_MID P07: A to none).
   - **The "+8–55% at large nationals" premise of P-LND-03 does not apply to v2.**
5. **The observed rate matters only if pools are rebuilt bottom-up, and then φ is what breaks.** [S] V2B_BOTTOMUP sets the pool = v1 touch rates × minutes × archetype grants × each sponsor's own observed rate, capped at observed labour cost.
   - **NAT_LARGE.** The pool rises from **$13.7m to $16.0m (p50)**. Implied φ is 0.20, inside v2's assumed 0.05–0.35. Vendor break-even falls from 8 to 7 sponsors.
   - **Everywhere else, implied φ collapses:**
     - NAT_MID: 0.027;
     - CF_1BN: 0.008;
     - CF_250M: 0.006;
     - CF_SMALL: 0.003.

     As a result, vendor break-even becomes unreachable in almost every draw.
   - [I] v1's per-grant minutes ($5–9 of handling per grant at observed rates) describe a high-volume national. v2's φ-anchored pools for community foundations are about $180–320 per grant. **φ (the share of labour cost that is grant-processing work), not the hourly rate, decides the CF and NAT_MID results.** See P-BLB-01.
6. **P-PRC-01: the queue's premise misreads the fee schedule.** [F] The [Benevity Foundations Fees Schedule](https://go.benevity.com/hubfs/website/en/Benevity-Fees-Schedule.pdf) (updated 2026-10-01, p.2) says "The Cause Support Fee **Caps** … do not apply to matching transactions or gift of securities donations."
   - **Matches and securities therefore pay the full, uncapped 2.99%.** They cannot explain a rate below 2.99%.
   - **AOGF reports no noncash contributions** in any year FY3/2022–FY3/2025: there is no `NoncashContributionsAmt` and no Schedule M.
   - The same misreading appears in [queue-processor-economics-vendor-profiles.md](queue-processor-economics-vendor-profiles.md) line 19, and should be corrected.
7. **On the published schedule, only two levers can lower the effective rate.** [S]/[I] They are the $500 cap on cash gifts above **$16,722**, and client master-agreement rates, which the schedule allows.
   - **If the whole Benevity payment were funded by fees deducted from contributions:** the share of contributions bearing the full 2.99% rose from **54% (FY3/2022) to 90% (FY3/2025)**.
   - **What that requires at minimum:** that 46% of FY2022 volume, falling to 10% in FY2025, was capped or discounted. Schedule I cannot rule this out: up to 80% of grant dollars went to recipients large enough to have received capped gifts.
   - **Two other things grew alongside the payment** (+$25.2m):
     - AOGF's "administrative service fee" revenue: $22.3m → $27.5m;
     - its investment income: $0.01m → $11.0m.

     If those revenue lines fund part of the payment, the fee deducted from donations is 0.4–1.3% of contributions.
   - **The 990 cannot separate these.** The answer is "mix shift or rate change, not identifiable from the 990". The historical fee schedules (Wayback was blocked) and AOGF's audited statements would settle it (P-BLB-02, P-BLB-03).

---

## 2. Q-N15: BDC schedule period fix

### 2.1 Method (changes to `mission_bdc_loans.py`)

1. **Row period.** The script keeps each `<tr>` match's position and does three things with it:
   - It reads every inline-XBRL `contextRef` inside the row and maps it to its `<xbrli:instant>` (or `endDate`) through the document's `<xbrli:context>` blocks.
   - It finds the nearest preceding "Schedule(s) of Investments" heading whose plain text gives exactly one date within 60 characters. Headings that list two dates, such as tables of contents and notes, are skipped.
   - It sets `period_ending` from the XBRL date if there is one, else the heading date, else the filing period. The filing's own period moves to `filing_period_ending`.
2. **Rows with two XBRL periods.** Some unfunded-commitment notes print the current and prior columns in one row. These rows take the later date and are flagged `multi_xbrl_dates`. They are excluded from the latest-marks table, because their parsed par and fair value come from different periods.
3. **Deduplication, stage 1.** The same `(adsh, table_row_index)` matched by two EDGAR phrases is kept once, with the first target winning. The other phrase is recorded in `also_matched_phrases`.
4. **Deduplication, stage 2.** The key is (lender, borrower, instrument, period). Instrument identity is the label plus reference rate, spread, PIK flag, maturity, par, fair value and row type, because a label such as "One stop" does not distinguish tranches.
   - All rows of one filing are kept for each key.
   - The filing kept is the one whose own period equals the row period; ties go to the earliest filing.
   - `dup_count` and `dup_filings` record the collapsed filings.
5. **Latest marks.** A facility is (lender, company group, maturity month). The "legacy CyberGrants/EveryAction" phrases fold into their company group.
   - Each facility's tranche rows are kept at its latest period, with facility par, FV and FV % of par.
   - `status` = `held_at_lender_latest_period` if the facility appears in the lender's latest searched schedule, else `not_in_schedule_at_<date>`.
6. **Identity note.** The 3/5/2032 Bonterra `identity_note` was updated per wave-8 correction 13.

The script still re-creates the same 650 parsed rows from the cached EDGAR documents. The unchanged v1 script reproduced the old CSV byte-for-byte before the fix.

### 2.2 Before and after

| | v1 (`-v1.csv`) | v2 (regenerated) |
|---|---|---|
| Rows | 650 | 600 |
| Rows whose own period ≠ filing period | 0 detected (all stamped with filing period) | 247 found; 206 kept after dedupe |
| `debt` rows | 374 | 334 |
| Period from XBRL / heading / fallback (kept rows) | n/a | 372 / 186 / 30 (16 table rows plus 14 text-only hits; 12 no-hit rows have none) |
| Rows flagged `row_period_conflict` | n/a | 30 (XBRL vs heading disagree, or two XBRL dates; XBRL governs) |
| Latest 10-K (`which_filing=latest`) table rows that are comparatives | n/a | 57 of 71 |
| 10-Q table rows that are comparatives (prior year-end) | n/a | 135 of 437 |

The rows named in wave-8 correction 12 are now dated as below [S]:
- Golub Capital BDC (rows 4047–4050) and Golub Capital Direct Lending (rows 2478–2481): **2024-09-30**.
- BlackRock TCP (rows 1164–1167), BlackRock Direct Lending (rows 868–871) and Monroe Capital (rows 1299–1301): **2024-12-31**.
- BlackRock rows 1573 and 1112 are commitment-note rows with two periods ("NA" in 2025, the value in 2024). They are flagged `multi_xbrl_dates` and excluded from the latest marks.

The BKCC FY2023 10-K repeats its 12/31/2022 Bonterra rows, as wave 8 suspected. Those rows are now dated 2022-12-31 and deduplicated against the FY2022 10-K.

### 2.3 Verification: Bonterra and Foundation Source (`bdc-loans-latest-marks.csv`)

| Lender | Facility (maturity) | Latest row period | Terms | Facility FV % par | Status |
|---|---|---|---|---|---|
| Golub Capital BDC | 09/2027 one-stop | 2024-09-30 | SF+7.00% (+7.75% PIK tranche) | 98.5 | not in schedule at 2025-09-30 |
| Golub Capital Direct Lending | 09/2027 | 2024-09-30 | SF+7.00% / 7.75% PIK | 98.5 | not in schedule at 2025-09-30 |
| BlackRock TCP | 9/8/2027 + 9/27/2027 increment | 2024-12-31 | SOFR+7.00%; increment PIK | 99.3 | not in schedule at 2025-12-31 |
| BlackRock Direct Lending | same | 2024-12-31 | SOFR+7.00%; 7.75% increment | 99.3 | not in schedule at 2025-12-31 |
| Monroe Capital | 9/8/2027 | 2024-12-31 | SF+7.00%; 7.75% PIK | 99.4 | not in schedule at 2025-12-31 |
| AB Private Credit Investors | 3/5/2032 | 2026-09-30 | S+5.00% (S+4.75% at 2025-12-31) | 99.0 | held |
| AB Private Lending Fund | 3/5/2032 | 2026-09-30 | S+5.00% | 99.0 | held; its 9/8/2027 S+7.25% loan was last seen at 2024-06-30 |
| CCS IX | 3/5/2032 | 2026-09-30 | S+5.00% | 99.0 | held |
| Crescent Private Credit Income | 03/2032 | 2026-09-30 | S+4.75% | 99.0 | held |
| FS KKR Capital | 03/2032 | 2026-09-30 | SF+4.8 (printed), $133.4m + $5.4m + $11.6m (millions) | 99.5 | held |
| KKR FS Income Trust / Select | (maturity not parsed) | 2026-09-30 | SF+4.8 | 99.4 | held |
| Audax Private Credit Fund (Foundation Source) | 9/6/2030 TL + DDTL; 9/6/2029 revolver | 2026-09-30 | S+5.00% | 100.0 | held; LP interests at 1.38× cost |

Sources:
- Each row's `filing_url`, for example [Golub BDC FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1476765/000147676525000096/gbdc-20250930.htm), [FS KKR 10-Q filed 2026-11-05](https://www.sec.gov/Archives/edgar/data/1422183/000162828026070499/fsk-20260930.htm) and [Audax Private Credit Fund 10-Q filed 2026-11-12](https://www.sec.gov/Archives/edgar/data/2033362/000119312526458521/ck0002033362-20260930.htm).
- The XBRL context dates are in `row_period_xbrl`.

### 2.4 Limitations

- **Periods taken from the filing (16 table rows).** These come from exhibit documents (Blue Owl SLF exhibits) and early Owl Rock / SLR filings with no XBRL and no dated heading. They are flagged `filing_period_fallback`, and they could still be comparatives.
- **Equal lines across filings.** Stage-2 dedupe treats two lines as equal only if par and fair value match exactly. A later amended figure for the same period survives as a separate row.
- **Parsing quirks kept from v1.** Examples: the KKR FS Income Trust maturity is not parsed, and the T. Rowe/OHA revolvers are on a commitment basis. Use `parse_check` and `row_cells_raw` to read these rows.
- **Facility FV %.** This is the sum over `debt` rows only. Partly drawn revolvers can pull it down.
- **What the status flag can and cannot say.** `not_in_schedule` means "absent from the latest filing found by the name search", not a confirmed repayment. For Golub BDC 3 and BlackRock Capital Investment, the latest schedule predates their 2024 mergers.

---

## 3. P-LND-03: AI-economics v2 with observed labour cost (v2b)

### 3.1 Method

`mission_ai_economics_v2b.py` imports v2 unchanged.
- **Same random streams as v2:** `random.Random(42)` for parameters and `42×1000+archetype` for the sponsor bootstrap. Every v2b draw is therefore the same draw as in v2 (common random numbers), and differences come only from the rate.
- **The observed rate.** For each draw it is the **bootstrapped sponsor's own** loaded labour cost per employee: Part IX lines 5–10 ÷ Part I line 5 ÷ 2,080 h ([`sponsor-salary-per-employee.csv`](../../data/mission-2026-11-14/sponsor-salary-per-employee.csv), `record_type=return`).
  - Only valid returns are used, meaning no flag `employees_lt_5`, `no_line7`, `wage_lt_20k_parttime_heavy` or `wage_gt_300k_outlier`. FY2024 is preferred, else the nearest year.
  - The fallback is the median valid rate of the archetype's window.
  - Coverage is 870 EINs with a valid rate.

| Archetype | Window sponsors with a valid rate | Window median rate | Draw p50 rate | Draws using own return |
|---|---|---|---|---|
| NAT_LARGE (Fidelity or DAFgiving360 anchor) | 3 of 5 nationals > $10bn | $60.47/h | $84.60/h (DAFgiving360 FY2024) | 50% (Fidelity has 0 employees and uses the fallback) |
| NAT_MID | 3 of 10 | $49.21/h | $49.21/h | 30% |
| CF_1BN | 20 of 20 | $61.01/h | $61.35/h | 100% |
| CF_250M | 58 of 58 | $53.30/h | $53.07/h | 100% |
| CF_SMALL | 229 of 268 | $41.21/h | $41.21/h | 85% |

The v1 hours-weighted mean rate over P01–P15 is **$45.14/h**. The variants are:
- **V2B_SCALED.** Each v1 process rate is multiplied by (observed ÷ $45.14), so occupation relativities are kept. It is checked against `v2.evaluate_draw` and written as a single `meta` row.
- **V2B_UNIFORM.** All processes are at the sponsor's single observed rate. This is the literal swap, and it changes only the mix.
- **V2B_BOTTOMUP.** The pool = Σ v1 (volume × touch rate × minutes) × archetype grants ÷ 1m × v1 rate × observed ÷ $45.14, capped at observed DAF-allocated labour cost. φ is not used, and implied φ = pool ÷ labour cost is reported.
  - The network break-even uses each FY2024 sponsor's own DAF grant dollars ÷ the drawn average grant size, at its own rate.
- P16 (recipient-side) and REF_V1_1M are left as in v2.

### 3.2 Results versus v2 (`record_type=compare_v2` rows; the note column carries the v2 value)

**Rank probabilities** are the mean over P01–P15 of P(option ranks first, net of fixed cost).

| Archetype | v2: none / C | UNIFORM: none / C | BOTTOMUP: none / C | Modal winners changed (UNIFORM / BOTTOMUP) |
|---|---|---|---|---|
| NAT_LARGE | 0.408 / 0.014 | 0.408 / 0.014 | 0.366 / 0.015 | 0 / 1 (P06: none → A) |
| NAT_MID | 0.893 / 0.001 | 0.889 / 0.001 | 0.993 / 0.000 | 1 (P07: A → none) / 1 |
| CF_1BN | 0.873 / 0.001 | 0.870 / 0.001 | 1.000 / 0.000 | 0 / 1 (P07: A → none) |
| CF_250M | 0.988 / 0.000 | 0.988 / 0.000 | 1.000 / 0.000 | 0 / 0 |
| CF_SMALL | 1.000 / 0.000 | 1.000 / 0.000 | 1.000 / 0.000 | 0 / 0 |

Mean P(C ranks first by gross, before fixed cost) is 0.028–0.032 in v2. It moves by no more than 0.0003 in UNIFORM and 0.0043 in BOTTOMUP.

**Break-evens** (AI on current workflow; vendor break-even p50 among finite draws; P = probability break-even is finite):

| Archetype | Pool p50: v2 → BOTTOMUP | Vendor N\* p50: v2 / UNIFORM / BOTTOMUP | P(finite): v2 / UNIFORM / BOTTOMUP | Implied φ p50 (BOTTOMUP) |
|---|---|---|---|---|
| NAT_LARGE | $13.67m → $16.03m | 8 / 8 / 7 | 0.95 / 0.95 / 0.97 | 0.200 |
| NAT_MID | $1.60m → $0.22m | 59 / 59 / 262 | 0.57 / 0.56 / 0.11 | 0.027 |
| CF_1BN | $1.77m → $0.08m | 59 / 60 / 627 | 0.66 / 0.66 / 0.02 | 0.008 |
| CF_250M | $0.45m → $0.015m | 236 / 229 / 2,172 | 0.24 / 0.24 / 0.0004 | 0.006 |
| CF_SMALL | $65k → $1.1k | 626 / 585 / none | 0.017 / 0.016 / 0 | 0.003 |

Network build-out over the observed FY2024 population, P(break-even reachable), AI on workflow:

| Segment | v2 | UNIFORM | BOTTOMUP |
|---|---|---|---|
| CF and national, all | 0.433 (p50 7 sponsors) | 0.431 (7) | 0.040 (4) |
| CF and national < $10bn | 0.263 (16) | 0.260 (16.5) | 0 |
| CF all | 0.160 (16) | 0.160 (17) | 0 |

### 3.3 Reading [I]

- **The v2 conclusions do not depend on the BLS-versus-observed rate question.** v2 anchors cost in dollars, so the rate cancels. The P-COST-02 observation that large sponsors pay $57–86/h is true, but it does not change any v2 number.
- **The bottom-up variant shows something else.** v1's process times, valued at observed rates, account for under 1% of community-foundation labour cost and about 3% at NAT_MID, against the 5–35% assumed for φ. Either CF staff spend most of their time on work outside P01–P15 (donor service, development, community programmes), or v1's touch rates and minutes are far too low for low-volume sponsors.
  - v2's CF and NAT_MID AI value rests on that assumed φ. NAT_LARGE is consistent in both framings.
- **Reading this for the entrant case.** Network-scale AI break-even is robust to the rate. It is not robust to φ.

### 3.4 Limitations

- **Per-head, not per-FTE.** Per-head rates count part-time staff, which biases them down (P-LND-04). Officer pay biases them up.
- **NAT_MID.** Only 3 of 10 sponsors have a valid rate.
- **Fidelity.** It always uses the nationals' median, because it reports no W-2 staff and buys its labour through line 11a.
- **BOTTOMUP and grant counts.** For non-NAT_LARGE archetypes, BOTTOMUP inherits v2's assumed average grant size ($5–40k, log-uniform) as its grant-count driver, and the implied φ scales inversely with it.
- **Outside-services labour.** The cap uses the observed labour cost including outside services (v2's labour share). Outside-services labour has no observed hourly rate.

---

## 4. P-PRC-01: AOGF's Benevity payments versus the 2.99% Cause Support Fee

### 4.1 Method

[`mission_aogf_benevity_reconcile.py`](../../scripts/mission_aogf_benevity_reconcile.py) reads two sources:
- the AOGF rows (EIN 81-0739440) of [`processor-vendor-economics-990.csv`](../../data/mission-2026-11-14/processor-vendor-economics-990.csv);
- the four 990 XML returns:
  - FY3/2022 [202340469349301209](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202340469349301209_public.xml);
  - FY3/2023 [202410469349300741](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202410469349300741_public.xml);
  - FY3/2024 [202530159349302758](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202530159349302758_public.xml);
  - FY3/2025 [202641969349302754](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202641969349302754_public.xml) (an amended return; the amendment corrects only Schedule I allocations).

From the XML it reads Part VIII (contributions, noncash contributions, program-service revenue and investment income) and Part IX lines 1, 3 and 11a. It also reads Schedule D (DAF counts), the presence of Schedule M, Schedule I recipient amounts and the Schedule A five-year series. The schedule parameters, 2.99%, the $500 cap and the 2.95% card fee, are taken from the [fee schedule PDF](https://go.benevity.com/hubfs/website/en/Benevity-Fees-Schedule.pdf), retrieved on 2026-11-14 (SHA-256 76fe1631…a345d7) [F]:
- the Cause Support Fee is "2.99% of each donation", capped at $500, and "may be different based on a Benevity client's master agreement";
- the caps "do not apply to matching transactions or gift of securities donations";
- the fee "is donated to and legally owned by the applicable Foundation, regardless of whether it is paid to an intermediary as an agent";
- AOGF deducts a "2.95% payment processing fee for credit and debit card donations".

### 4.2 Results [S] (`aogf-benevity-reconciliation.csv`)

| FYE March | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| Benevity, Inc. (Part VII-B) | $29.27m | $33.49m | $45.97m | $54.45m |
| Contributions (Part VIII 1h) | $1,801.3m | $1,731.0m | $2,035.4m | $2,027.0m |
| Grants paid (Part I 13) | $1,675.5m | $1,721.5m | $1,953.6m | $2,125.7m |
| Noncash contributions / Schedule M | none / not filed | none / not filed | none / not filed | none / not filed |
| "Administrative service fee" revenue (Part VIII 2a) | $22.31m | $21.24m | $24.93m | $27.46m |
| Investment income | $0.01m | $3.43m | $10.67m | $11.04m |
| Merchant fees (Part IX 24) | $5.95m | $5.13m | $5.79m | $6.48m |
| Benevity ÷ grants | 1.75% | 1.95% | 2.35% | 2.56% |
| Benevity ÷ contributions | 1.63% | 1.93% | 2.26% | 2.69% |
| Full-rate-equivalent share of contributions (÷ 2.99%) | 54% | 65% | 76% | 90% |
| Minimum share capped or discounted | 46% | 35% | 24% | 10% |
| Same, if admin-fee revenue funds part of the payment: (Benevity − admin fee) ÷ contributions | 0.39% | 0.71% | 1.03% | 1.33% |
| Upper bound on capped-gift volume (Sched I $ at recipients ≥ $16,722, plus foreign grants, ÷ grants) | 80% | 80% | 81% | 81% |
| Minimum card share of grants (merchant fees ÷ grants ÷ 2.95%) | 12.0% | 10.1% | 10.1% | 10.3% |
| DAF accounts (Sched D) / contributions per account | 763,149 / $2,384 | 678,086 / $2,583 | 720,545 / $2,855 | 710,352 / $2,890 |

### 4.3 What grant mix explains the effective rate [I]

- **Matches and securities do not explain it.** Under the schedule they pay 2.99% uncapped. AOGF reports no securities at all, and securities gifts are not in its contributions as noncash.
- **Mix-only explanation.** The only mix lever is the cap. At the cap a donation pays $500 whatever its size, so a capped gift of $50k pays 1.0% and one of $100k pays 0.5%.
  - Reproducing 2.56% of grants needs at least **14% of grant volume in capped cash gifts**. That is the limit as gifts grow very large; at an average capped gift of $50k, it rises to about 22%.
  - FY3/2022 needs at least **41%** (about 62% at $50k).
  - That is a fall of about two-thirds in the large-gift share over three years. It is possible (for example, large corporate disaster gifts in FY3/2022, which includes February–March 2022), but nothing in the 990 shows it.
  - Contributions per account rose only 21%. Schedule I cannot test the cap, because it reports recipient totals, not donations.
- **Rate-or-recognition explanation.** The schedule lets client master agreements set other rates. AOGF also has two revenue lines besides contributions that rose with the payment:
  - administrative service fees, +$5.1m;
  - investment income on float, +$11.0m, as interest rates rose.

  Together they cover 64% of the +$25.2m rise in the Benevity payment. The return also says Benevity performs "management duties … pursuant to a management services agreement" (FY3/2025 Schedule O). If the payment includes pass-through of these revenues, the fee actually deducted from donations was 0.4–1.3% of contributions, and its rise is a change in the contract or the rate, not a shift in mix.
- **Conclusion.** The 990 shows that the rise is not caused by matches or securities. It cannot separate a cap-driven mix shift from client-rate or contract changes.
  - The cheapest test is the historical fee schedule: earlier versions of the same PDF. web.archive.org was blocked from this environment (proxy reset).
  - The decisive test is AOGF's audited statements: the revenue-recognition and related-party notes, filed with state charity regulators.
- **Card-funded volume.** Merchant fees imply at least about 10% of volume came by card, stable over FY2022–25. Payroll and corporate rails carry the rest.

### 4.4 Limitations

- **Gross versus net contributions.** The ratio uses contributions, which per the schedule include the fee "donated to … the Foundation". Grants are lower than contributions in three of the four years, so ratios on grants and on contributions differ by up to 0.13 points.
- **Funding of the Benevity payment.** Whether the admin-service-fee revenue or the investment income pays Benevity is not stated in the 990.
- **Fiscal-year mismatch.** Benevity's fiscal year and the fee schedule's effective dates are not aligned with AOGF's March year-end.
- **Line 11a versus Part VII-B.** Line 11a (management fees) is $32.4m in FY3/2022, against $29.3m to Benevity in Part VII-B. The difference is not itemised.

---

## 5. Data sources

- **SEC EDGAR filings.** Full-text search hits and filing documents, cached from `efts.sec.gov/LATEST/search-index` and `www.sec.gov/Archives`. Each row's `filing_url` and `efts_query_url` are in the BDC CSVs.
- **IRS Form 990 e-file XML.** These are the four AOGF returns above. The sponsor returns are those behind `sponsor-cost-structure.csv` and `sponsor-salary-per-employee.csv`, with ProPublica page URLs in `source_url`.
- **Benevity Foundations Fees Schedule** (last updated 2026-10-01): https://go.benevity.com/hubfs/website/en/Benevity-Fees-Schedule.pdf
- **AI-economics inputs (v2):** `ai-process-economics.csv`, `sponsor-cost-structure.csv`, `sponsor-cost-structure-summary.csv` and `ai-economics-v2-results.csv` (comparison).

---

## 6. Data dictionary

### `bdc-loans-daf-ecosystem.csv` (new or changed columns; the others are as in [queue-pe-lenders-labour-rates.md](queue-pe-lenders-labour-rates.md))

| Column | Meaning |
|---|---|
| `period_ending` | **Changed.** The row's own schedule date: XBRL, else heading, else filing period |
| `filing_period_ending` | The filing's period of report (the old `period_ending`) |
| `adsh` | EDGAR accession number |
| `is_comparative` | "yes" if `period_ending` ≠ `filing_period_ending` |
| `row_period_source` | `xbrl_context`, `schedule_heading` or `filing_period_fallback` |
| `row_period_xbrl`, `row_period_heading` | The two candidate dates (blank if none) |
| `row_period_conflict` | `xbrl_vs_heading` and/or `multi_xbrl_dates:<d1>\|<d2>` |
| `dup_count`, `dup_filings` | Number of filings and the list of accession numbers that reported this line for this period. The kept row comes from one of them |
| `also_matched_phrases` | Other EDGAR phrases that matched the same filing row (dropped duplicates) |

### `bdc-loans-latest-marks.csv`

| Column | Meaning |
|---|---|
| `company_group` | Target company with the legacy-name phrases folded in |
| `maturity_month` | YYYY-MM from `maturity`. Part of the facility key (lender, company group, maturity month; instrument for undated rows) |
| `lender_latest_schedule_period` | Latest `filing_period_ending` among this lender's filings found for the group |
| `status` | `held_at_lender_latest_period` or `not_in_schedule_at_<date>` |
| `facility_debt_par`, `facility_debt_fv`, `facility_fv_pct_of_par` | Sums and ratio over the facility's `debt` rows at that period (units as in `units_hint`) |
| Other columns | As in the main CSV. For equity rows, `par_or_principal` is units or shares |

### `ai-economics-v2b-results.csv`

The columns are v2's (`record_type`, `archetype`, `process_id`, `process`, `intervention`, `parameter`, `bucket`, `metric`, `value`, `unit`, `basis`, `note`) plus a leading `variant`, which takes the values `V2B_UNIFORM`, `V2B_BOTTOMUP`, `V2B_SCALED` (meta only) or `ALL`. The new record types are:
- **`labour_rate`.** Window rate quartiles, the share of draws using the sponsor's own return, draw-rate distribution, implied-φ distribution and the share of draws where the cap binds.
- **`compare_v2`.** `value` is the v2b figure; `note` = "v2=…; diff=…". Metrics include `mean_p_rank_first_net_P01_P15`, `mean_p_rank_first_gross_P01_P15`, `processes_modal_winner_changed_*`, `sponsor_pool_P01_P15_p50`, platform break-even metrics and network `p_breakeven_reachable` / `breakeven_sponsors_p50_reachable`.
- **`platform_network`.** BOTTOMUP adds `segment_implied_phi_*`.

### `aogf-benevity-reconciliation.csv`

| Column | Meaning |
|---|---|
| `fiscal_year_end`, `fiscal_year` | AOGF fiscal year (March year-end); `ALL` for schedule parameters |
| `metric` | See the table in §4.2. The `sched_a_admin_service_fee_tax_year_YYYY` rows hold the Schedule A five-year series (tax year YYYY = FYE March YYYY+1) |
| `value`, `unit` | usd, ratio or count. A blank value means the item is absent from the return |
| `basis` | XML return id and URL, the source CSV, "computed", or the fee-schedule citation |
| `note` | Formula or caveat |

### `queue-proposals-bdc-labour.csv`

The format follows [queue-proposals-README.md](../../data/mission-2026-11-14/queue-proposals-README.md). IDs are P-BLB-01 to P-BLB-04: φ measurement, archived Benevity fee schedules, AOGF audited statements, and the commitment-note parser.

## Validation corrections (wave 9, 2026-11-14) — governing
Source: [validation-wave9-report.md](validation-wave9-report.md). Where these conflict with the text above, these govern.

1. **§1 item 2, Golub bullets.**
   - Replace "Golub Capital BDC: 2024-09-30, facility 98.5%." with "Golub Capital BDC: 2024-12-31, 100.0% of par ($104.7m; 10-Q 0001476765-25-000016)."
   - Replace "Golub Capital Direct Lending: 2024-09-30, 98.5%." with "Golub Capital Direct Lending: 2024-12-31, 100.0% of par ($9.55m; 10-Q 0001868878-25-000011)."
2. **§1 item 2, 2032 facility.**
   - Replace "is held at **2026-09-30** at 99.0–99.5%:" with "is held at **2026-09-30** at 98.2–99.5%:".
   - Add a bullet: "New Mountain Finance, NM Guardian IV BDC, NM Guardian IV Income Fund, NM Private Credit Fund and NMF SLF I: SOFR(Q)+5.00%, 03/2032, 98.25% (e.g. NMFC 14,876 par / 14,615 FV, $000). Not captured by the parser (borrower printed on its own row)."
   - Change "FS KKR: SF+4.8 (as printed)" to keep "(as printed; rounded, 4.75 not confirmed from FSK)".
3. **§2.2 (line "Golub Capital BDC (rows 4047–4050) and Golub Capital Direct Lending (rows 2478–2481): **2024-09-30**.")** Append: "These are the latest marks *in the filings the script selected*. The 12/31/2024 10-Qs carry current-period rows at par (see wave-9 V9-07)."
4. **§2.3 table, Golub rows.**
   - Change `| Golub Capital BDC | 09/2027 one-stop | 2024-09-30 | ... | 98.5 | not in schedule at 2025-09-30 |` to period `2024-12-31` and mark `100.0`.
   - Make the same change for Golub Capital Direct Lending.
   - Add a row: `| New Mountain family (5 BDCs) | 03/2032 | 2026-09-30 | SOFR+5.00% | 98.25 | held; missed by parser |`.
