# Realised admin fees across the whole tail: all 641 tail CFs and the 29 non-CF census sponsors (P-B4427B4501-04 / -05)

**Date:** 2026-11-20 · **Task id:** b4427b-0405 · **Labels:** **[F]** filed figure; **[C]** computed by the script; **[I]** inference. This is research, not legal, tax or accounting advice.

**Outputs**
- [`scripts/mission_tail_realised_fees_all.py`](../../scripts/mission_tail_realised_fees_all.py): stdlib only, functional style. It imports `scripts/mission_npt_screen_fees.py` (the b4427b-b4501 fee-line method) and does not change it. Tasks `fetch` (IRS index selection and XML fetch into a cache outside the repo) and `run` (CSV and the tables below, which are its stdout).
- [`data/mission-2026-11-14/tail-realised-fees-all-2026-11-20.csv`](../../data/mission-2026-11-14/tail-realised-fees-all-2026-11-20.csv): 670 rows. There are 641 tail CFs (`part = B_tail_cf`) and 29 non-CF census sponsors (`part = A_noncf_sample`). The data dictionary is in §7.
- [`data/mission-2026-11-14/queue-proposals-b4427b-0405.csv`](../../data/mission-2026-11-14/queue-proposals-b4427b-0405.csv): 5 follow-ups.
- No existing file was edited.

**Governing inputs.** Method: [`b4427b-b4501-npt-screen-and-realised-fees.md`](b4427b-b4501-npt-screen-and-realised-fees.md) §1.3, applied as corrected by [validation wave 41B](validation-wave41b-report.md):
- Greene County's EITC grant fee is a pass-through and is excluded.
- Licking County publishes its schedule (audit note 1N), so it counts as a publisher.
- The publisher vs non-publisher comparison is confounded by size, so rates are reported by size band.

The pool being replaced is [`b4501-04-tail-fee-pool-revision.md`](b4501-04-tail-fee-pool-revision.md) as corrected by wave 35A: whole-tail central $138m, CFs-only central $89.9m, tail CF DAF assets $6.10bn, non-CF tail $3.08bn.

---

## 0. Answers in brief

| Question | Answer | Confidence |
|---|---|---|
| **(B) Share of tail CFs that show a fee on the 990** | All 641 tail CFs have at least one FY2022–24 Form 990 read (2,657 returns FY2021–24, none missing from the mirror). **292 (46%) show some administrative or management fee item. 47 (7%) are classed as disclosing an internal fee charged to their own funds.** 245 show only agency-worded (21) or unstated-base (224) lines, and 349 show none [C]. Visible fees become more common with size: 39% under $1m of DAF assets, 45% at $1m–10m, 54% at $10m–50m. The internal share is flat at 7–8% [C]. | High on counts; medium on the internal/other split (wording rules) |
| **Realised internal-fee rates and size** | Internal fee ÷ average total assets, pooled FY2022–24, median 102 bps (IQR 71–136; n = 47). **Rates fall with size.** By DAF band, the medians of complete-capture CFs are **134 bps (under $1m DAF; n = 10), 112 bps ($1m–10m; n = 18) and 73 bps ($10m–50m; n = 13)**. By total assets: 122, 132, 92, 83 and 53 bps from under $10m to $100m and over. Spearman ρ (total assets vs rate) = −0.43, n = 47 [C]. | Medium (small n per band) |
| **Publisher vs non-publisher, size-controlled** | The two internal-fee publishers, Hutchinson (83.2 bps) and Licking (69.7 bps), are both in the $10m–50m DAF band, whose median is 72.7 bps. **They charge what their size band charges.** The census-level gap (publishers 76 bps vs non-publishers 103) is a size effect, as wave 41B suspected [C; I on the reading]. | Medium (n = 2 publishers) |
| **Realised-rate CF pool (replaces the schedule-based pool)** | Method: each CF at its own internal rate where observed with complete capture, otherwise its band median, applied to FY2024 DAF assets. **Central $49.4m (81 bps on $6.10bn).** Range **$38.5m–$61.5m** (band Q1–Q3); seeded bootstrap 90% interval $42.9m–$58.0m [C on that assumption]. Hard floor (only the 47 internal disclosers, at their own rate): $3.2m. The schedule-based CFs-only central ($89.9m, 147 bps) is 1.8× the realised central. | Low–medium: all-fund rates applied to DAF assets (§5) |
| **(A) Do non-CF tail sponsors charge like CFs?** | **Not on the 990 evidence.** 6 of the 29 non-CF census sponsors (21%) show any fee line, against 22 of the 31 census CFs (71%). **None of the six can be classed as an internal fund fee from its wording** [C]. The visible lines are large where they exist: National Boy Scouts of America Foundation "Admin Fees" $5.15m (184 bps of total assets); United Methodist Foundation of Louisiana "Trustee Management Fees" $3.11m (214 bps); United Way of the Mid-Willamette Valley $428k (202 bps). Their bases (trusts, council endowments) are not stated. 23 of 29 show no fee line, including both colleges, the University of Florida Foundation, and Cal Poly Pomona (which publishes a 2% schedule). On Schedule D Part V, 13 non-CFs charge endowments a median 95 bps of administrative expense, against 116 bps at 16 census CFs [C]. | Low–medium (n = 29; $173m of $3.08bn) |
| **Whole-tail realised pool** | **$49.4m if non-CFs charge nothing, $74.3m if they realise the CF central rate** (81 bps). Adjusting the second figure by the disclosure ratio (21% / 71% = 0.29) gives **$56.7m [I]**. Whole-tail range: $38.5m–$92.5m. The schedule-based whole-tail central ($138m) is not supported: its CF half is about 1.8× the realised CF rate, and its non-CF half has no realised evidence of CF-type charging [C; I]. | Low |

---

## 1. Method

### 1.1 Sponsors and returns [C]
- **(B) Tail CFs:** every `community_foundation` row in `daf-long-tail-sponsors-fy2021-2024.csv` with FY2024 band `t10_50`, `t1_10`, `t0_1` or `zero`. That is 641 CFs (207 / 272 / 150 / 12) holding $6,101.3m of corrected FY2024 DAF assets.
- **(A) Non-CFs:** the 29 sponsors in `long-tail-fee-census-2026-11-19.csv` with `type4` ≠ `cf`:
  - 13 single-issue and other;
  - 8 religious;
  - 7 university or hospital;
  - 1 national.
  - Their categories come from the tail CSV. All 60 census rows match it.
- **Returns.** The rule is the b4427b-b4501 rule (base `fy_candidates`):
  - Fiscal year = the calendar year in which the tax period ends.
  - Use the newest Form 990 per year; a higher object id supersedes.
  - Index sources are the IRS TEOS indexes 2019–2025 (copies of 2026-11-14) plus `index_2026.csv` of 2026-11-19 (516,019 rows).
  - FY2021 returns are read only for the opening DAF and funds balances.
- **Fetch.** 2,657 sponsor-year returns were selected:
  - 124 were reused from the b4427b-b4501 cache;
  - 2,533 were fetched from the GivingTuesday mirror of IRS TEOS;
  - 0 were missing; 0 failed to parse; 0 needed a next-newest fallback.

### 1.2 Fee lines (imported unchanged from `mission_npt_screen_fees.py`) [C]
1. **Part VIII revenue lines.** Program service revenue and other revenue lines whose description names an administrative, management, philanthropic or fund fee, or "fee income" (`FEE_DESC`).
2. **Schedule D Part XI line 2d.** Administrative-fee items: revenue in the audited statements that is not on Part VIII (`RECON_FEE`).
3. **Schedule D Part V line 1f.** Administrative expenses on endowment funds, divided by the average of lines 1a and 1g.
4. **Licking County audit fee income.** FY2023 $957,643 and FY2024 $1,058,361 (base `FEE_AUDIT`). Both quotes were re-verified against the cached audit text ("verified").

**Additions** (new script only):
- **Pass-through exclusion.** Lines naming EITC or a tax credit are reported in `fee_passthrough_fy22_24` and excluded from fee income. Only Greene County has one ($68,310, FY2022–24).
- **Part IX expense lines.** Part IX line 24 "other expenses" lines naming an administrative or fund fee are read. They feed the matched-expense rule below.

### 1.3 Capture classification, from the filer's wording [C on rules; I on each class]
First match wins. The quoted wording is in `capture_basis`.

| Rule | Class | Tail CFs |
|---|---|---|
| 1. b4427b-b4501 hand reading (base `SCOPE`; Pikes Peak and Jasper Newton → agency) | as read | 10 (8 internal) |
| 2. Fee item worded as charged to own funds: internal, interfund, component, endowment, nonoperating funds, from funds, fund admin, funds held, designated, donor advised / DAF | internal | 9 |
| 3. Schedule D Part XI 2d fee item not worded as agency (in audited revenue, not on Part VIII: an eliminated interfund fee) | internal | 11 |
| 4. A Part VIII fee line matched in the same year by a Part IX line 24 fee expense within 10%, where the expense is not agency-worded (an interfund gross-up) | internal | 19 |
| 5. Agency, external, charged to others, third party, other organisations, fiscal sponsorship/"sponsored", property, rental | agency | 21 |
| 6. A fee line whose base is not stated | unknown | 224 |
| 7. No fee item FY2022–24 | none visible | 349 |

`capture2` collapses these to internal / agency_or_unknown / none visible.

**Partial-capture flag.** An internal rate under half of the CF's own Part V endowment admin rate gets the flag. This is the test b4427b-b4501 applied to Central Florida. 6 of the 47 internal-fee CFs are flagged:
- Central Florida (17.5 vs 187.8 bps);
- Lehigh Valley (4.5 vs 102.9);
- Door County (25.4 vs 429.0);
- Howard County (36.0 vs 96.6);
- Keokuk (83.5 vs 185.8);
- one "Community Foundation of the …" (154.6 vs 979.5).

The pool's central case sets their own rates aside and gives them their band median instead.

### 1.4 Rates [C]
- **Pooling.** Rates are pooled over the FY2022–24 years in which the fee is visible. A blank year at a CF that discloses in other years counts as non-disclosure, not as zero (as in b4427b-b4501).
- **Internal rate** = internal fee income ÷ average (BOY, EOY) Part X total assets.
  - Also computed against net assets and against "funds held" (Schedule D Part I line 4, columns (a)+(b)).
  - The funds-held version is in the CSV only. Column (b) is often blank or small, so that denominator overstates the rate; medians of 350 bps and more are not credible.
- **Ceiling** = fee income ÷ average DAF balance (Schedule D I-4(a)), as in b4427b-b4501.

### 1.5 Pool [C on the stated assumption]
- **Base.** Each tail CF's FY2024 DAF assets.
- **Central rate.** Its own complete-capture internal rate where one exists (41 CFs); otherwise the median complete-capture rate of its DAF size band.
- **Low / high.** The band's lower or upper quartile in place of the median.
- **Bootstrap.** CFs are resampled within each band (seed 20261120, 2,000 draws), and the 5th and 95th percentiles of the central are reported.
- **Floors.**
  - Internal disclosers only, at their own rate; everyone else zero.
  - Any visible fee, at the CF's own visible rate.
- **Proxy.** The band median Part V rate.
- **Non-CF scenarios** on $3,079.4m:
  - zero;
  - a non-CF realised rate (not estimable: n = 0 internal);
  - the CF central implied rate (the whole-tail assumption);
  - that rate × the disclosure ratio of non-CFs to census CFs [I].

---

## 2. Reproduction check [C]
On its 31 census CFs, the new script reproduces every b4427b-b4501 realised rate to 0.05 bps, except **Greene County: 124.2 → 97.6 bps**. That is the wave-41B EITC correction, applied by rule rather than by hand.

---

## 3. Results, part B: all 641 tail CFs

### 3.1 Disclosure and rates by DAF size band (bps; median (IQR; n)) [C]

| DAF band (FY2024) | CFs | Any fee visible | Internal fee disclosed | Agency/unknown only | Visible fee ÷ avg TA | Internal ÷ avg TA | Part V admin ÷ endowment | DAF assets $m |
|---|---|---|---|---|---|---|---|---|
| $10m–50m | 207 | 111 (54%) | 16 (8%) | 95 (46%) | 21 (8–87; 111) | 71 (20–87; 16) | 111 (83–149; 117) | 4,858 |
| $1m–10m | 272 | 122 (45%) | 20 (7%) | 102 (38%) | 30 (7–102; 122) | 103 (80–142; 20) | 125 (93–156; 157) | 1,185 |
| under $1m | 150 | 59 (39%) | 11 (7%) | 48 (32%) | 59 (20–136; 59) | 137 (124–162; 11) | 136 (88–192; 83) | 58 |
| zero | 12 | 0 | 0 | 0 | – | – | 123 (97–146; 5) | 0 |
| **All tail CFs** | **641** | **292 (46%)** | **47 (7%)** | **245 (38%)** | 33 (8–103; 292) | **102 (71–136; 47)** | 124 (88–164; 362) | 6,101 |

### 3.2 By total-asset band (average FY2022–24 Part X total assets) [C]

| Total assets | CFs | Any fee visible | Internal disclosed | Visible ÷ TA | Internal ÷ TA | Part V admin | DAF assets $m |
|---|---|---|---|---|---|---|---|
| < $10m | 164 | 46 (28%) | 6 (4%) | 63 (20–116; 46) | 122 (103–149; 6) | 113 (79–189; 76) | 245 |
| $10m–25m | 152 | 72 (47%) | 14 (9%) | 82 (8–131; 72) | 132 (89–166; 14) | 142 (101–181; 89) | 641 |
| $25m–50m | 143 | 73 (51%) | 14 (10%) | 28 (8–106; 73) | 92 (37–128; 14) | 126 (97–158; 91) | 1,423 |
| $50m–100m | 107 | 59 (55%) | 9 (8%) | 16 (6–85; 59) | 83 (9–129; 9) | 111 (88–140; 60) | 1,831 |
| ≥ $100m | 75 | 42 (56%) | 4 (5%) | 14 (7–24; 42) | 53 (31–74; 4) | 107 (59–143; 46) | 1,961 |

The size gradient shows in every measure of the fee itself:
- the internal rate;
- the Part V endowment rate, whose medians fall from 142 bps to 107 bps above $10m of total assets;
- the visible-fee rate, which also shifts towards small agency lines as CFs grow.

The internal rate against total assets has Spearman ρ = −0.43 (n = 47) [C].

### 3.3 Census CFs: publishers vs non-publishers, with size [C]

| Group | CFs | Any fee | Internal | Internal ÷ TA | Part V admin |
|---|---|---|---|---|---|
| Publishers (6 with a 2021+ rate, plus Licking) | 7 | 5 | 2 | 76 (73–80; n=2) | 91 (n=2) |
| Non-publishers | 24 | 17 | 6 | 103 (99–115; n=6) | 116 (n=14) |

- The publishers are Hutchinson ($99.6m of average total assets, 83.2 bps) and Licking ($142.5m, 69.7 bps).
- Both are in the $10m–50m DAF band, whose complete-capture median is 72.7 bps (IQR 56–88; n = 13).
- Five of the six non-publishers with internal fees have total assets of $31.6m or less (Greene $8.6m to Clinton $31.6m). The three in the $1m–10m band (Four Way, Clinton, Decatur) realise 101.6–118.9 bps against that band's median of 111.7. Greene and Monroe, in the under-$1m band, realise 97.6 and 129.4 against 134.2.
- The sixth, Central Florida ($112.2m, $10m–50m band), carries the partial-capture flag (17.5 bps). It is in the non-publisher median of 103 shown above.
- **[I] Within size bands, publication status does not separate realised rates.** The census gap is a size gap.

### 3.4 Capture and the unknown class [C]
- **Agency lines are small.** The 21 agency-classed CFs show visible fees with a median of 8 bps of total assets; 19 of the 21 are under 20 bps.
- **The 224 "unknown" lines are bimodal.** Median 26 bps:
  - 103 are under 20 bps, consistent with agency or service fees;
  - 94 are at 50 bps or more, and 78 at 70 bps or more, consistent with an internal fee whose wording does not say so.
- **[I] Consequence.** The 7% internal-disclosure share is a floor on how many tail CFs charge their own funds. Up to about a further 15% (94 of 641) probably do too. Not showing a fee is not evidence of a zero fee (P-B4427B0405-01).

Examples of internal classification [F]:
- Wabash Valley CF, Schedule D Part XI 2d: "ADMINISTRATIVE FEES 1,221,891" (FY2024, object 202501269349303080). Its rate is 130.6 bps.
- Coastal Bend CF: Part VIII "ADMINISTRATIVE FEE INCOME" $1,165,161, matched by a Part IX line 24 expense "ADMINISTRATIVE FEES" $1,058,267 (FY2023). Its rate is 88.3 bps.
- Montrose CF: Part VIII "Donor Advised Admin Fee" (117.6 bps all-fund).

### 3.5 Realised-rate CF pool [C on the stated assumption]

Band rates (complete-capture internal-fee CFs):

| DAF band | n | Median | Q1 | Q3 |
|---|---|---|---|---|
| $10m–50m | 13 | 72.7 | 56.4 | 88.3 |
| $1m–10m | 18 | 111.7 | 81.3 | 154.5 |
| under $1m | 10 | 134.2 | 120.5 | 165.3 |
| all (used for `zero`, which has no DAF assets) | 41 | 108.9 | 77.5 | 137.4 |

Including the 6 partial captures gives 70.6 / 103.0 / 137.4 bps, with a much lower Q1 in the top band (20.4).

| Scenario (tail CF DAF assets $6,101.3m) | Pool $m | bps on DAF assets |
|---|---|---|
| **Central: own complete-capture rate, else band median** | **49.4** | **81.0** |
| **Low: own rate, else band Q1** | **38.5** | 63.1 |
| **High: own rate, else band Q3** | **61.5** | 100.7 |
| Bootstrap 90% interval of central (seed 20261120, 2,000 draws) | 42.9–58.0 | |
| Sensitivity: partial captures kept, band median | 47.0 | 77.1 |
| Sensitivity: partial captures kept, band Q1 | 21.8 | 35.7 |
| Flat all-tail median (no size control) | 66.4 | 108.9 |
| Floor: the 47 internal disclosers at their own rate, others zero | 3.2 | 5.3 |
| Floor: any visible fee at own visible rate, others zero | 15.9 | 26.0 |
| Proxy: band median Part V endowment admin rate | 69.7 | 114.2 |
| *Schedule-based CFs-only central (b4501-04, wave 35A)* | *89.9* | *147.3* |
| *b4427b-b4501 floor-type figure (8 CFs, flat 103 bps)* | *62.9* | *103.1* |

**[I] Reading.**
- Size control matters because tail CF DAF assets sit mostly in the $10m–50m band (80%), which realises the lowest rates. The flat 8-CF figure ($62.9m) and the flat 41-CF median ($66.4m) both overstate the size-banded central by about a third.
- The realised central replaces the schedule-based $89.9m as the evidence-based figure for what tail CFs actually collect at all-fund rates. The schedule figure remains a ceiling-type reference for DAF list prices (§5).

---

## 4. Results, part A: the 29 non-CF census sponsors

### 4.1 By category [C]

| Category | Sponsors | Any fee visible | Internal | Visible ÷ TA | Part V admin ÷ endowment | DAF assets $m |
|---|---|---|---|---|---|---|
| single-issue / other | 13 | 3 (23%) | 0 | 184 (105–193; 3) | 52 (24–162; 5) | 54 |
| religious | 8 | 2 (25%) | 0 | 108 (54–161; 2) | 96 (83–104; 4) | 72 |
| university / hospital | 7 | 1 (14%) | 0 | 59 (n=1) | 88 (47–132; 4) | 14 |
| national | 1 | 0 | 0 | – | – | 33 |
| **All non-CFs** | **29** | **6 (21%)** | **0** | 122 (34–197; 6) | **95 (49–123; 13)** | 173 |
| *All 31 census CFs, same basis* | *31* | *22 (71%)* | *8 (26%)* | *14 (4–101; 22)* | *116 (80–155; 16)* | *354* |

### 4.2 The six non-CFs with a fee line [F lines; C rates]

| Sponsor | Category | Fee line(s) FY2022–24 | ÷ avg TA | Why not classed internal |
|---|---|---|---|---|
| National Boy Scouts of America Foundation | single-issue | "Admin Fees" $1,459,026 / $3,010,049 / $676,349 | 184.5 | Base not stated (council endowments and trusts possible); Part V 162 bps |
| United Methodist Foundation of Louisiana | religious | "Trustee Management Fees" $1,098,101 / $1,120,165 / $887,808 | 214.4 | Trustee fees on trusts or church funds; base not stated |
| United Way of the Mid-Willamette Valley | single-issue | "Administrative Fees" $117,062 / $211,824 / $99,325 | 201.8 | Base not stated; holds no DAF assets in FY2024 |
| Educational Foundation of … | university | "FEE INCOME" $120,145 / $121,681 / $129,852 | 59.2 | Base not stated |
| The Astraea Foundation | single-issue | "ADMINISTRATIVE FEES" $172,666 / $37,412 / $550 | 25.5 | The matching expense is "SPONSORED ADMIN FEES", i.e. fiscal sponsorship |
| Jewish Federation Foundation of Greater … | religious | "MANAGEMENT FEE INCOME" $2,797 / $6,549 / $6,843 | 0.7 | Tiny; base not stated |

### 4.3 What the test shows [I]
1. **Non-CFs are far less likely to show any fee revenue.** The figures are 21% against 71% for CFs drawn by the same census.
   - The difference is not a filing-format artefact: the same parser reads both groups.
   - It is consistent with many non-CF sponsors running DAFs as a donor-relations service, with costs absorbed or recovered through investment spreads. That reading is not proven.
2. **Where non-CFs show fees, the lines are large but their base is not stated.** No line can be tied to DAFs, so none supports the claim that non-CFs charge CF-type DAF fees.
3. **Non-CFs with endowments charge them administrative expenses near CF levels.** The Part V median is 95 bps against 116. This is indirect evidence that some can and do charge funds. It is not a DAF fee.
4. **The whole-tail pool's assumption (non-CFs priced like CFs) is not supported.** The realised evidence fits a non-CF contribution between zero and a disclosure-discounted CF rate, not a full CF rate. The sample is small (29 sponsors, $173m of $3.08bn), so this is a test result, not a measurement (P-B4427B0405-03).

### 4.4 Whole-tail realised pool [C on each assumption]

| Non-CF assumption (non-CF tail DAF assets $3,079.4m) | Central $m | Low $m | High $m |
|---|---|---|---|
| Non-CFs charge nothing | 49.4 | 38.5 | 61.5 |
| Non-CFs at a non-CF realised internal rate | not estimable (n = 0) | | |
| [I] Non-CFs at the CF implied rate × disclosure ratio (0.21 / 0.71 = 0.29) | 56.7 | 44.2 | 70.5 |
| Non-CFs at the CF central implied rate (81.0 bps; the whole-tail assumption) | 74.3 | 57.9 | 92.5 |
| *Schedule-based whole-tail central (b4501-04)* | *138.0* | | |

**Suggested replacement figure [I]:**
- **Tail admin-fee pool on realised rates:** about **$50m–$57m** central. $49.4m is CFs only; $56.7m adds non-CFs on a disclosure discount.
- **Range:** about $38m–$93m. The range spans the CF band quartiles and non-CF charging from none to full CF rates.
- **Basis:** all-fund realised rates. A DAF-specific rate would raise the CF part by an unknown factor (P-B4427B0405-02).

---

## 5. Limits
1. **All-fund, not DAF-only.**
   - The realised rate is fee income ÷ total assets for all funds, so it understates a DAF rate if DAFs are priced above endowed and agency funds, as published schedules usually are.
   - The pool applies all-fund rates to DAF assets. It measures what the tail would collect at the rates it realises across its books, not DAF fee revenue as such.
   - The fee ÷ DAF balance ceiling (CSV) is far higher. The truth lies between the two.
2. **Classification by wording.**
   - 47 internal CFs is a floor; 94 high-rate "unknown" CFs probably also charge internal fees (§3.4).
   - The matched-expense rule (19 CFs) treats an equal fee expense as an interfund gross-up. A pass-through, such as Greene's EITC fee, would look the same unless named; only EITC/tax-credit wording is screened.
   - Rule 3 treats non-agency Part XI fee items as interfund.
3. **Partial capture.** The flag needs a Part V figure, and only 32 of the 47 internal CFs report one. Captures that are partial but unflagged remain in the band rates, which biases them down.
4. **Small bands.** n = 13, 18 and 10 complete-capture CFs per band. The bootstrap interval ($42.9m–$58.0m) reflects that sampling only, not classification error.
5. **Total assets include operating assets**, real estate and split-interest assets, which lowers rates at CFs with large non-fund balances.
6. **Part A sample.** 29 sponsors, 5.6% of non-CF tail DAF assets, drawn by the census strata. Two (IDACORP, GlobalTrust) are near-zero DAF hosts, and GlobalTrust has only one FY2022–24 return read.
7. **Year coverage.** FY2024 returns filed late may be missing from the 2026-11-19 index. Every sponsor had at least one FY2022–24 return, and 1 non-CF had only one.
8. **No audits were read beyond Licking.** This task used Form 990 alone, as asked. The b4427b-b4501 audit crawl covered the 30 census CF sites.

---

## 6. Robots and access log (2026-11-20, UA `research-script/1.0`, unchanged)

| Host | robots.txt | Use |
|---|---|---|
| gt990datalake-rawdata.s3.amazonaws.com | 404, so no robots file (checked 2026-11-20T01:10:54Z) | 2,533 Form 990 XMLs; 0 objects missing |
| apps.irs.gov | 302 to www.irs.gov/404, so no robots file (checked 2026-11-20T01:10:55Z) | Index CSVs (local copies of 2026-11-14 and 2026-11-19; not re-downloaded) |

No logins, forms or outreach were used. sec.gov, crt.sh and certspotter were not used. No other host was contacted.

---

## 7. Data dictionary: `tail-realised-fees-all-2026-11-20.csv` (one row per sponsor; 670 rows)

| Column | Meaning |
|---|---|
| ein, name | Tail CSV identifiers |
| part | `B_tail_cf` (641 tail CFs) or `A_noncf_sample` (29 non-CF census sponsors) |
| sponsor_category, size_band_fy2024, daf_assets_fy2024 | From `daf-long-tail-sponsors-fy2021-2024.csv` (corrected FY2024 DAF assets) |
| census_type4, in_census_sample, census_fee_status | From the fee census, where the sponsor is in it |
| publisher, publisher_basis | Census CFs: `yes` for a 2021+ rate in the census distribution, or Licking (wave 41B); blank outside the census |
| published_bps_100k | Census admin bps at $100k |
| years_read, years_with_fee, fee_years | FY2022–24 returns read; years with any visible fee; which years |
| fee_visible_fy22_24 | All fee items (Part VIII + Part XI + audit), less pass-through, FY2022–24 |
| fee_rev_990_fy22_24, fee_recon_990_fy22_24, fee_audit_fy22_24 | The three components |
| fee_passthrough_fy22_24 | EITC / tax-credit fee lines excluded |
| fee_internal_fy22_24 | Internal fee income summed over years with an internal fee (internal-capture sponsors only; agency-worded items excluded) |
| capture, capture2, capture_basis | Class from §1.3; two-way split; the rule and the wording behind it |
| avg_total_assets, ta_band | Mean FY2022–24 average total assets; band of §3.2 |
| visible_bps_ta | Visible fee ÷ average total assets, pooled over fee years |
| internal_bps_ta, internal_bps_na, internal_bps_funds | Internal fee ÷ average total assets / net assets / Sch D Part I line 4 (a)+(b). The funds version is not credible (§1.4) |
| fee_per_daf_bps_upper | Fee ÷ average Sch D line 4(a): a ceiling on a DAF-only rate |
| endow_admin_bps, endow_years | Sch D Part V line 1f ÷ average of lines 1a and 1g, pooled; years with data |
| partial_flag | 1 if internal_bps_ta < half of endow_admin_bps |
| pool_rate_bps, pool_rate_basis, pool_central_usd | Tail CFs: the rate used in the central pool (own complete-capture rate or band median) and the resulting $ |
| fallback_returns | Returns where the next-newest stood in (0 throughout) |
| fee_lines_seen, fee_expense_lines_seen | Fee items as filed (source: description amount); Part IX line 24 fee expenses |
| return_object_ids | IRS object ids of the FY2022–24 returns read (XML at the S2 URL) |

The queue-proposals CSV uses the header and format of `queue-proposals-gap19-13.csv`.

---

## 8. Source register

| ID | Source | URL | Accessed | Used in |
|---|---|---|---|---|
| S1 | IRS TEOS e-file indexes 2019–2026 | https://apps.irs.gov/pub/epostcard/990/xml/{YYYY}/index_{YYYY}.csv | copies 2026-11-14 and 2026-11-19 | §1.1 |
| S2 | Form 990 XMLs, all 2,657 selected returns (object ids in the CSV) | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{object_id}_public.xml | 2026-11-20 | §2–§4 |
| S3 | Wabash Valley CF Form 990 CY2024 (Sch D Part XI 2d) | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202501269349303080_public.xml | 2026-11-20 | §3.4 |
| S4 | Coastal Bend CF Form 990 FY2022–24 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202303199349307615_public.xml ; …/202443269349301469_public.xml ; …/202523219349325087_public.xml | 2026-11-20 | §3.4 |
| S5 | National Boy Scouts of America Foundation Form 990 FY2022–24 | …/202313199349306656_public.xml ; …/202413199349306191_public.xml ; …/202503219349326470_public.xml | 2026-11-20 | §4.2 |
| S6 | United Methodist Foundation of Louisiana Form 990 FY2022–24 | …/202341179349301514_public.xml ; …/202401099349300815_public.xml ; …/202540709349300234_public.xml | 2026-11-20 | §4.2 |
| S7 | The Astraea Foundation Form 990 FY2022–24 | …/202321359349313797_public.xml ; …/202431369349308438_public.xml ; …/202531349349308503_public.xml | 2026-11-20 | §4.2 |
| S8 | United Way of the Mid-Willamette Valley; Educational Foundation; Jewish Federation Foundation Form 990s | object ids in CSV `return_object_ids` (e.g. …/202423199349312292_public.xml ; …/202421349349305272_public.xml ; …/202421369349319482_public.xml) | 2026-11-20 | §4.2 |
| S9 | Licking County Foundation audited statements 2024 and 2023 (via b4427b-b4501 cache; quotes re-verified) | https://www.thelcfoundation.org/file_download/inline/9bb96e42-95b4-48f2-8b7a-cd7a4c2a0c28 | b4427b-b4501 / wave 41B | §1.2 |
| R1 | Repo | `daf-long-tail-sponsors-fy2021-2024.csv`; `long-tail-fee-census-2026-11-19.csv`; `tail-realised-fee-rates-2026-11-20.csv` (reproduction check); `b4427b-b4501-npt-screen-and-realised-fees.md`; `b4501-04-tail-fee-pool-revision.md`; validation waves 35A and 41B | repo | throughout |

**Reproduce** (the cache paths are outside the repo):
```
python3 -I scripts/mission_tail_realised_fees_all.py . --task fetch --irs-dir IRS --irs-dir IRS_2026_11_19 --xml-dir XMLDIR --reuse-dir OLDXML --fetch --log FETCH.tsv
python3 -I scripts/mission_tail_realised_fees_all.py . --task run   --irs-dir IRS --irs-dir IRS_2026_11_19 --xml-dir XMLDIR --reuse-dir OLDXML --text-dir FEEDIR
```
`FEEDIR/audit_txt/` holds the Licking audit text used by the quote check (as in b4427b-b4501).
