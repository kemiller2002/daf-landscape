# P-B45N33-02: operating cost per DAF dollar and per DAF account in the long tail

**Date:** 2026-11-19 · **Queue item:** P-B45N33-02 (from `direction-long-tail-sponsors.md`, P-NEW-TAIL-01)

**Outputs**
- [`data/mission-2026-11-14/long-tail-operating-cost-2026-11-19.csv`](../../data/mission-2026-11-14/long-tail-operating-cost-2026-11-19.csv): 1,290 rows, one per sponsor (the 1,240 FY2024 sponsors under $50m of corrected DAF assets, plus the top 50).
- [`scripts/mission_long_tail_cost.py`](../../scripts/mission_long_tail_cost.py): stdlib only, functional style, no network. Run `python3 scripts/mission_long_tail_cost.py .`; it writes the CSV and prints every table in this note (the full print-out is the Appendix).
- [`data/mission-2026-11-14/queue-proposals-b45n33-02.csv`](../../data/mission-2026-11-14/queue-proposals-b45n33-02.csv): 5 follow-ups.

**Labels:** **[F]** filed value · **[C]** script computation · **[I]** inference. **Every DAF-allocated cost is [I]**; its rule is in §1.3 and in the column name (`_alloc_A`, `_alloc_G`, `_alloc_AM`). This is research, not legal, tax or accounting advice.

---

## 0. Answers in brief

| Question | Answer (FY2024 returns; sponsor medians with IQR) | Confidence |
|---|---|---|
| **Usable data** | **1,220 of 1,240 tail sponsors** have a usable FY2024 Part IX [C]: 635 of 641 community foundations (CFs), 539 of 547 single-issue sponsors, 46 of 52 nationals/processors. Per-account figures need a screened account count (CF n = 549, single-issue n = 428); per-dollar figures need non-imputed DAF assets (CF n = 603, single-issue n = 499). Top 50: 49 of 50 (Bank of America CGF excluded: $70.8k of operating cost on $4.73bn). | High [C] |
| **What tail CFs spend in total** | Median operating cost (Part IX line 25 less grants, line 4 and line 11f) **$630k** ($282k–$1.46m), **5 employees** (2–9), **205 bps of total assets** (127–367) [C]. DAFs are a minority of the balance sheet: **17.7%** of total assets (7.4–34.7%) and **27.6%** of grants (9.2–51.9%) [C]. | High [C] |
| **Per DAF account, tail CFs** | **[I]** Rule A (assets share): **$2,859** ($1,458–$6,119). Rule G (grants share): **$4,106** ($1,827–$9,821). Admin-only floor AM: **$1,179** ($617–$2,418). Column C often holds line 11f investment fees (69% of column C at Community Foundation of the Fox); with 11f removed from column C, the lower bound is $829 per account and 61 bps (medians) [V wave 33A] Unallocated ceiling: $19,413 [C]. | Medium [I] |
| **Per DAF dollar, tail CFs** | **[I]** Rule A: **205 bps** (127–359). Rule G: **285 bps** (136–602). AM floor: **90 bps** (52–147). Rule G per grant dollar: **32.8 cents** (19.5–56.1). | Medium [I] |
| **Per account / per dollar, single-issue tail (ex universities and hospitals, n = 351 / 394)** | **[I]** Rule A **$4,864** ($1,029–$19,160) and **708 bps** (143–2,273). Rule G **$7,402** and **578 bps**. AM floor **$1,293** and **178 bps** (62–390). Their Part IX is mostly mission delivery, so A and G overstate DAF cost; AM is the better guide here. | Low–medium [I] |
| **Top 50** | **[I]** Top-50 CFs: rule A **$12,036 per account** ($7,220–$23,987) and **102 bps** (58–156); rule G $16,840 and 131 bps. Top-50 nationals: **$1,425 per account** and **24 bps** (18–48); costs at affiliated firms are outside Part IX. | Medium [I]; High [C] on whole-org figures |
| **Tail vs top 50** | **Per dollar, tail CFs cost about twice top-50 CFs under rules A and G (205 vs 102 bps, 2.0×; 285 vs 131 bps, 2.2×), but 1.6× on the AM floor and 1.75× for the closest band ($10–50m, 178 vs 102 bps). Rule A per dollar is whole-org opex ÷ total assets, so this compares whole organisations, not DAF administration. Tail CFs are about 8.5 times top-50 nationals (24 bps) [V wave 33A] Per account they look cheaper ($2.9k vs $12.0k), but only because tail accounts are smaller**: median average account $144k at tail CFs against $1.14m at top-50 CFs [C]. Under rule A, cost per account = whole-org cost ratio × average account, an identity [C]. | High [C] on the identity; Medium [I] on the levels |
| **What DAF administration plausibly carries** | **[I] For a tail CF: about $1.2k–$4.1k per DAF account a year (central $2.9k), or about 90–285 bps of DAF assets (central about 205 bps).** Against published tail fees (P-B45N33-01: 6 CF schedules, 0–200 bps at $100k, median 150), each applied to every usable tail CF at its own average account, the median share across the six schedules is 66.7% of tail CFs below rule-A cost (n = 603), 73.1% below rule-G cost (n = 579) and 24.9% below the AM floor. Across the five non-zero schedules the rule-A share runs 51.7–74.8%. At the medians, a 150 bps fee covers about 73% (150 ÷ 205) of rule-A cost. The earlier comparison used the top-100 median of 100 bps, at or below which sit 15.3% (A) and 18.0% (G) of tail CFs ([b4501-04-tail-fee-pool-revision.md](b4501-04-tail-fee-pool-revision.md)) [b4501-04] [V wave 35A] | [I] |
| **Stable over time?** | Yes. Tail-CF rule-A medians on each year's own Schedule D: **211 / 198 / 205 / 184 bps** and **$2,462 / $2,583 / $2,783 / $2,709 per account** in FY2022 / 23 / 24 / 25 (FY2025 partial, n = 302–303) [C]. | High [C] |

---

## 1. Method

### 1.1 Data and the Part IX question
1. **The Schedule D harvest does not carry full Part IX.** `form990-returns-schedule-d-harvest-full.csv` (5,416 returns) has only four Part IX totals: `part_ix_it_total` (line 14), `part_ix_fees_mgmt_total` (11a), `part_ix_fees_other_total` (11g) and `part_ix_fees_invest_total` (11f). **It has no line 25 (total functional expenses), no grant lines and no employee count** [F, column check].
2. **Where full Part IX is cached.** `scripts/mission_sponsor_cost_structure.py` (P-99F-04) re-read all 5,272 parsed returns of that harvest with an extended extractor (Part IX lines 1–25 in all four columns, Part I including `TotalEmployeeCnt`). Its raw extracts were cached outside the repository (`--cache-dir …/extract990cost/{object_id}.json`); its per-return output is **`data/mission-2026-11-14/sponsor-cost-structure.csv`** (5,272 rows, FY2022 1,494 / FY2023 1,513 / FY2024 1,507 / FY2025 758). This note reads that file. The XML is the IRS e-file, via the GivingTuesday mirror (§6).
3. **Universe:** `daf-long-tail-sponsors-fy2021-2024.csv` (P-NEW-TAIL-01). Tail = `size_band_fy2024` in `t10_50`, `t1_10`, `t0_1`, `zero` (1,240). Top 50 = `top50` (50). Corrected FY2024 DAF assets, DAF grants, screened accounts and the DAFRC-based `sponsor_category` come from this file.
4. **Join:** EIN × FY2024 (FY = calendar year in which the tax period ends; this matches the DAFRC panel, e.g. Fidelity's FY2024 return is tax period 2024-06). 1,233 tail sponsors have an FY2024 return in the cost file. Where an EIN-FY has two returns (15 cases in the file), the one with the latest return timestamp is used.

### 1.2 Segments
| Segment | Rule | Tail sponsors |
|---|---|---|
| **Community foundations** (`tail_cf`) | `sponsor_category = community_foundation` | 641 |
| **Single-issue** (`tail_si`) | `single_issue_other` (283) + `religious` (149) + `university_or_hospital` (115) | 547 |
| Single-issue ex universities and hospitals (`tail_si_ex_univ`) | other + religious | 432 |
| Nationals and processors in the tail (context only) | `national_standard`, `donation_processor` | 52 |
| Top 50 | split into nationals (20), CFs (21), single-issue (9) | 50 |

Sub-bands for CFs and single-issue: $10–50m, $1–10m, and under $1m (which includes the 35 zero-asset sponsors; they have no per-dollar figure).

### 1.3 Measures and allocation rules
- **Operating cost (opex)** [C] = Part IX line 25(A) − lines 1–3 (grants) − line 4 (member benefits) − line 11f (investment-management fees). This is `operating_cost_ex_invest_mgmt`, the repository's standard definition (cost-structure note, as corrected in validation wave 5).
- **Whole-organisation ratios** [C]: opex ÷ DAF accounts and opex ÷ DAF assets. **These are ceilings**, because they put every non-DAF activity on the DAFs.
- **Allocation rules [I]:**

  | Rule | DAF cost = | Per account | Per DAF dollar | What it assumes |
  |---|---|---|---|---|
  | **A** (assets) | opex × min(1, corrected DAF assets ÷ total assets EOY) | ÷ screened accounts | ÷ DAF assets, in bps | A DAF dollar costs the same as any other dollar on the balance sheet. **Its per-dollar figure is then just the whole-org cost ratio** (except where the share is clipped). |
  | **G** (grants) | opex × min(1, corrected DAF grants ÷ Part IX grants, lines 1–3) | ÷ screened accounts | ÷ DAF assets; also ÷ DAF grants (cents per grant dollar) | Cost follows grantmaking activity. DAFs pay out faster than endowed funds, so G gives DAFs more cost than A. |
  | **AM** (admin floor) | Part IX line 25 column C (management and general) × the rule-A share | ÷ screened accounts | ÷ DAF assets | Only overhead is shared; program-service cost is not DAF cost. Right for single-issue sponsors (libraries, hospitals, congregations); **understates CFs**, which book grantmaking and donor services in column B. Column C may include part of 11f. |

- **Staffing** [C/I]: employees = Part I line 5 (`TotalEmployeeCnt`) [F]; accounts per employee [C]; DAF FTE = employees × rule-A share [I].
- **Statistics:** sponsor-level medians and IQRs (linear interpolation), with n per cell. Pooled ratios (Σ allocated cost ÷ Σ accounts or assets) are also printed in the Appendix.

### 1.4 Exclusions and data rules
- **Excluded from all statistics** (20 tail sponsors, 1 top-50) [C]: no FY2024 return in the cost file (7), opex ≤ 0 or line 25 missing (9), opex below 1 bp of DAF assets (2 tail: Kirkland & Ellis Foundation, Youngstown Area Jewish Foundation; 1 top-50: Bank of America CGF), and the two structural outliers of P-NEW-TAIL-01 (Givinga, undefined account unit; BNY Mellon CGF, terminated December 2024).
- **DAF assets** used only where not DAFRC-imputed and above 0; **DAF grants** only where not imputed; **accounts** only where `accounts_fy2024_screened` is set (non-imputed and passing the league-table plausibility screen).
- **Flags among the 1,220 usable tail sponsors** [C]: 314 report zero employees; 201 lack a screened account count; 76 have imputed or non-positive DAF assets; 91 imputed DAF grants; 15 have DAF assets above total assets and 33 DAF grants above Part IX grants (both clipped to a share of 1).

---

## 2. Results

### 2.1 Community foundations: DAFs are one fund type among several

| Tail CF segment | Usable | DAF share of total assets | DAF share of grants | Opex (whole org) | Employees | Median avg account |
|---|---|---|---|---|---|---|
| All tail CFs | 635 / 641 | 17.7% (7.4–34.7%) | 27.6% (9.2–51.9%) | $630k ($282k–$1.46m) | 5 (2–9) | $144k ($79k–$249k) |
| $10–50m | 207 / 207 | 28.3% (16.6–43.2%) | 43.7% (28.6–64.8%) | $1.55m | 9 (6–13.5) | $242k |
| $1–10m | 267 / 272 | 17.6% (8.4–28.8%) | 22.9% (9.3–46.0%) | $490k | 5 (2–7) | $130k |
| Under $1m | 161 / 162 | 3.7% (1.5–11.8%) | 5.4% (1.5–23.6%) | $281k | 2 (0–4) | $44k |
| *Top-50 CFs* | 21 / 21 | 65.3% (45.8–76.0%) | 75.7% (67.0–89.7%) | $26.7m | 97 (68–141) | $1.14m |

**Cost per DAF account and per DAF dollar, tail CFs [I unless marked]**

| Segment | Ceiling: whole org per account [C] | Rule A per account | Rule G per account | AM floor per account | Rule A bps | Rule G bps | AM bps | Rule G cents per grant $ |
|---|---|---|---|---|---|---|---|---|
| All tail CFs | $19,413 | **$2,859** ($1,458–$6,119; n=549) | **$4,106** ($1,827–$9,821; n=536) | $1,179 ($617–$2,418) | **205** (127–359; n=603) | **285** (136–602; n=579) | 90 (52–147) | 32.8 (19.5–56.1) |
| $10–50m | $18,228 | $4,689 ($2,574–$7,818) | $7,504 ($3,770–$13,396) | $1,711 | 178 (122–285) | 271 (161–481) | 67 | 27.1 |
| $1–10m | $18,093 | $2,523 ($1,567–$5,638) | $3,459 ($1,794–$7,510) | $1,169 | 220 (131–362) | 289 (127–569) | 100 | 34.2 |
| Under $1m | $31,493 | $1,012 ($420–$2,707) | $1,079 ($456–$3,378) | $499 | 248 (137–495) | 345 (101–966) | 120 | 41.1 |
| *Top-50 CFs* | $20,245 | $12,036 ($7,220–$23,987) | $16,840 ($10,035–$32,197) | $5,752 | 102 (58–156) | 131 (87–223) | 57 | 10.6 |

**Reading**
- **[C] The whole-org cost per account is about the same at tail and top-50 CFs ($18k–$31k against $20k).** The difference is in what the money buys: top-50 CFs hold 65% of their assets in DAFs; the smallest tail CFs hold 3.7%.
- **[C] Per dollar, cost rises as the CF shrinks** (rule A 178 → 220 → 248 bps down the tail, against 102 bps at top-50 CFs). **Per account, it falls** ($4,689 → $2,523 → $1,012), because the accounts shrink faster ($242k → $130k → $44k).
- **[I] Rules A and G both scale cost with dollars, so they assume a $44k DAF costs about a sixth of a $242k DAF to run.** If DAF administration is mostly a fixed cost per fund (statements, grant checks, donor contact), the true per-account cost at the smallest CFs is above the rule-A figure, and the per-dollar cost well above 248 bps. Fund counts now test this. On 34 tail CFs whose 990 narratives state an all-funds total, the fund-count rule F gives a median of $4,500 per DAF account and 258 bps, against rule A’s $3,518 and 203 bps on the same CFs. F exceeds A at 24 of 34 CFs, the expected direction. The set leans to larger-opex CFs, so the frame-level value is probably nearer $3.2k [I] (b45n33-02-01-01). The earlier 15-CF web sample gave $2,108 and 276 bps (b45n33-02-01). [V wave 48B]
- **[C] IT is small:** median line 14 is $26.9k at tail CFs (3.2% of opex; n = 403 reporting the line), and rule-A IT per DAF account is **$99** ($37–$212), against $362 at top-50 CFs. Staff (lines 5–10) are 53.3% of opex; 11a + 11g outside services are 3.5%.
- **[I] Staffing:** rule-A DAF FTE is 0.9 (0.2–1.9) per tail CF, serving a median 42 accounts per DAF FTE (24–76), against 16 at top-50 CFs (whose accounts are eight times larger).

### 2.2 Single-issue sponsors

| Segment | Usable | DAF share of assets | Ceiling per account [C] | Rule A per account | Rule G per account | AM per account | Rule A bps | Rule G bps | AM bps |
|---|---|---|---|---|---|---|---|---|---|
| All single-issue | 539 / 547 | 7.9% (1.1–32.8%) | $86,566 | $5,525 ($1,303–$22,400; n=428) | $7,402 ($907–$36,289; n=391) | $1,544 ($445–$5,652) | 610 (147–2,241; n=499) | 552 (113–3,503; n=441) | 168 (63–363) |
| Ex univ/hospital | 425 / 432 | 12.5% (2.4–38.9%) | $67,405 | **$4,864** ($1,029–$19,160; n=351) | **$7,402** ($909–$34,655; n=321) | **$1,293** ($410–$5,337) | **708** (143–2,273; n=394) | **578** (126–3,627; n=349) | **178** (62–390) |
| – Other single-issue | 278 / 283 | 12.7% | $88,391 | $8,356 | $8,178 | $1,791 | 1,033 | 633 | 249 |
| – Religious | 147 / 149 | 12.0% | $40,458 | $2,029 | $6,840 | $797 | 206 | 492 | 79 |
| – University or hospital | 114 / 115 | 0.7% (0.1–7.3%) | $1,210,656 | $8,052 | $7,409 | $2,352 | 390 | 341 | 130 |
| $10–50m (all SI) | 68 / 69 | 28.6% | $19,458 | $6,840 | $9,421 | $2,101 | 267 | 415 | 108 |
| $1–10m | 229 / 234 | 13.6% | $88,008 | $8,052 | $9,385 | $2,187 | 526 | 613 | 138 |
| Under $1m | 242 / 244 | 2.0% | $128,838 | $2,871 | $2,426 | $821 | 939 | 613 | 242 |
| *Top-50 single-issue* | 9 / 9 | 63.5% | $9,152 | $8,127 | $8,400 | $5,631 | 133 | 134 | 79 |

**Reading**
- **[C] Single-issue sponsors are not DAF businesses.** The median one has 7.9% of its assets in DAFs, and 0.7% at universities and hospitals. Its Part IX is a library, a school, a hospital or a congregation.
- **[I] Rules A and G therefore load mission-delivery cost onto DAFs.** Example: Friends of the Pamlico County Public Library has $1.64m of opex, 70% of its assets in 5 DAFs, and a rule-A cost of $230k per account (7,277 bps) (`long-tail-operating-cost-2026-11-19.csv`, EIN 611592352). The **AM floor (178 bps, $1,293 per account)** is the more plausible order of magnitude for the DAF administration itself.
- **[C] Religious sponsors are the exception**: rule A 206 bps and $2,029 per account, close to tail CFs, with 32% of them at or below 100 bps (rule A).
- **[C] Staffing is thin:** median 1.2 accounts per employee (ex univ/hospital) and 0.2 rule-A DAF FTE; IT median $25.2k (1.9% of opex).

### 2.3 Comparison with the top 50

| Measure (medians) | Tail CFs | Tail single-issue ex univ | Top-50 CFs | Top-50 nationals | Top 50, all |
|---|---|---|---|---|---|
| Usable / sponsors | 635 / 641 | 425 / 432 | 21 / 21 | 19 / 20 | 49 / 50 |
| DAF share of total assets [C] | 17.7% | 12.5% | 65.3% | 99.1% | 77.3% |
| Avg DAF account [C] | $144k | $104k | $1.14m | $387k | $843k |
| Whole-org opex per account (ceiling) [C] | $19,413 | $67,405 | $20,245 | $1,436 | $10,449 |
| Rule A per account [I] | $2,859 | $4,864 | $12,036 | $1,425 | $6,554 |
| Rule G per account [I] | $4,106 | $7,402 | $16,840 | $1,436 | $7,712 |
| Rule A bps of DAF assets [I] | 205 | 708 | 102 | 24 | 60 |
| Rule G bps [I] | 285 | 578 | 131 | 24 | 76 |
| AM floor bps [I] | 90 | 178 | 57 | 22 | 50 |
| Rule G cents per DAF grant $ [I] | 32.8 | 51.7 | 10.6 | 1.2 | 4.8 |
| IT per account, rule A [I] | $99 | $99 | $362 | $117 | $254 |
| Share with rule-A cost ≤ 100 bps [I] | 15.3% | 18.8% | 47.6% | 94.7% | 65.3% |

- **[C] The identity behind the per-account comparison.** Under rule A, cost per account = (opex ÷ total assets) × average account. Tail CFs have twice the cost ratio of top-50 CFs (205 vs 102 bps) but an eighth of the account size, so their per-account figure is a quarter as large. **Neither the per-dollar nor the per-account figure alone describes the tail; the pair does.**
- **[C] Nationals** report $1,425 per account and 24 bps (Fidelity: $161.6m opex, 204,614 accounts, $66.2bn, so about $783 per account and 24 bps; object 202521349349310887). Much national cost sits at affiliated firms and in fund expense ratios outside Part IX (cost-structure note §8), so these are floors for the all-in cost.
- **[I] Scale.** Moving from the tail to the top-50 CF halves the per-dollar cost but does not lower the cost of serving an account; it raises it. The economies at top-50 CFs come from account size, not from serving each account more cheaply.

### 2.4 What DAF administration plausibly carries (inference)
**[I] For a tail community foundation, DAF administration plausibly costs $1.2k–$4.1k per DAF account a year (AM floor to rule-G median; rule A, the central case, $2.9k), equal to about 90–285 bps of DAF assets (central about 205 bps).** For single-issue sponsors (excluding universities and hospitals), the plausible range is the AM floor, **about $1.3k per account and about 180 bps**, up to rule A or G (**$4.9k–$7.4k and 580–710 bps**), with the low end more credible because their Part IX is mostly program delivery.

The allocation rule behind each figure is in §1.3. Three cross-checks:
- **[C] Against the fee side.** The fee census (P-B45N33-01) found 6 published 2021+ tail-CF schedules: 0–200 bps at $100k, median 150 bps, against the top-100 CF median of 100 bps. Each applied to every usable tail CF at its own average account, the median share across the six schedules is **66.7%** of tail CFs below rule-A cost (n = 603; 51.7–74.8% across the five non-zero schedules), **73.1%** below rule-G cost (n = 579) and **24.9%** below the AM floor. In aggregate the fee recovers a median 0.58 of rule-A and 0.36 of rule-G cost. At the medians, 150 bps covers about 73% (150 ÷ 205) of rule-A cost and 53% (150 ÷ 285) of rule-G cost. At each publisher's own average account, the fee covers rule-A cost at 1 of 7, rule-G cost at 0 of 5 and the AM floor at 4 of 7 (P-B45N33-02-03). **[I] At observed tail prices, most tail CFs still run DAFs below fully allocated cost under either rule, covered by unrestricted, endowment or agency-fund income, while about three quarters cover the admin-only floor.** The fee level rests on n = 6 ([b4501-04-tail-fee-pool-revision.md](b4501-04-tail-fee-pool-revision.md)) [b4501-04] [V wave 35A]
- **[C] Against the market cost pool.** The cost-structure note's FY2024 CF pool is 127 bps (A) and 177 bps (G) on pooled DAF assets, across all CF sizes. The tail-CF pooled figures here are 255 bps (A) and 406 bps (G); tail CFs are about twice as costly per dollar as the CF average, which itself includes the tail. This is consistent with the scale elasticity of 0.84 reported there: median total assets are $28.8m (tail CFs) and $1.62bn (top-50 CFs), a 56× gap, and 56^0.16 ≈ 1.9 [V wave 33A]
- **[C] Over time.** The tail-CF medians barely move across FY2022–25 (§2.5).

### 2.5 Robustness: FY2022–25 on each year's own Schedule D
Same sponsors (FY2024 band membership), each year's return, DAF assets and accounts from that year's Schedule D (DAFRC value where blank), same exclusions and account screen.

| Group | FY2022 | FY2023 | FY2024 | FY2025 (partial) |
|---|---|---|---|---|
| Tail CFs, rule A per account [I] | $2,462 (n=626) | $2,583 (n=631) | $2,783 (n=629) | $2,709 (n=302) |
| Tail CFs, rule A bps [I] | 211 | 198 | 205 | 184 |
| Tail single-issue, rule A per account [I] | $4,904 (n=489) | $5,599 (n=516) | $6,092 (n=530) | $6,591 (n=246) |
| Tail single-issue, rule A bps [I] | 608 | 661 | 671 | 705 |
| Top-50 CFs, rule A per account [I] | $10,725 (n=21) | $11,874 | $12,036 | $10,805 (n=9) |
| Top-50 CFs, rule A bps [I] | 108 | 104 | 102 | 138 |

---

## 3. What this means [I]
- The tail's DAF cost problem is a **fixed-cost-per-account problem expressed as a high per-dollar ratio**. Tail CFs spend about the same per account as top-50 CFs on the whole organisation, on accounts an eighth of the size.
- **IT is not where the money goes**: about $100 per account (rule A) against $2,900 of allocated operating cost; staff are over half. A cheaper platform alone moves a few percent of cost; a change in how staff time per account is spent moves the rest.
- **Single-issue sponsors** run DAFs as a side line: a median 12.5% of assets in DAFs and about one DAF account per employee. Their DAF cost cannot be read from Part IX without an admin-only rule, and part of it may sit with an outside administrator.

---

## 4. Limits
- **Every DAF cost is an allocation [I].** Part IX reports cost by line and function, not by fund type. A, G and AM bracket a plausible range; none is observed. A fund-count rule has since been tested: rule F puts 0.245 of cost on DAFs, or $4,500 per account and 258 bps, on 34 CFs (b45n33-02-01-01). Audited notes by fund type (P-B45N33-02-02) have not yet been used as a test. [V wave 48B]
- **Rule A's per-dollar figure is not independent evidence**: it equals the whole-org cost ratio by construction (except for the 15 clipped sponsors).
- **Costs outside Part IX** (affiliated administrators, fund expense ratios, investment fees netted in returns) are invisible. This mainly affects top-50 nationals; three sponsors under 1 bp were excluded.
- **Account counts:** 201 usable tail sponsors have no screened count; 314 report zero employees (volunteer-run or staffed by an affiliate), so accounts-per-employee figures cover 781 tail sponsors.
- **FY2025** is partial (758 returns in the cost file) and used only as a robustness row.
- **University and hospital foundations**: DAF shares under 1% of nine- and ten-figure budgets make every allocated figure fragile; they are shown but excluded from the single-issue headline.
- **Tail fee data are thin**: the fee comparison uses 6 published tail-CF schedules (P-B45N33-01) from a sample in which 11.7% of sponsors publish a rate; the 100 bps top-100 median is kept only as a reference [b4501-04] [V wave 35A]
- **No network requests** were made for this item; no robots check was needed. All inputs are repository files built from cited primary sources.

---

## 5. Data dictionary: `long-tail-operating-cost-2026-11-19.csv`

| Column | Meaning | Label |
|---|---|---|
| ein, name | Sponsor EIN and name (long-tail file) | [F] |
| group | `tail_cf`, `tail_si`, `tail_national`, `top50_cf`, `top50_si`, `top50_national` | [C] |
| sponsor_category, size_band_fy2024, fy2024_rank_assets | From `daf-long-tail-sponsors-fy2021-2024.csv` | [C] |
| daf_assets_fy2024, daf_grants_fy2024 | Corrected FY2024 DAF assets and grants; blank if DAFRC-imputed (assets also blank if ≤ 0) | [F/C] |
| daf_accounts_fy2024_screened | Screened account count (non-imputed, plausible) | [F/C] |
| return_object_id, tax_period | FY2024 990 used (latest return timestamp if two) | [F] |
| total_functional_expenses | Part IX line 25(A) | [F] |
| part_ix_grants_l1_3 | Part IX lines 1–3 | [F] |
| opex_ex_11f | Line 25 − lines 1–4 − line 11f | [C] |
| staff_cost_l5_10, fees_mgmt_l11a, fees_other_l11g, it_l14 | Part IX lines | [F] |
| employees | Part I line 5 | [F] |
| total_assets_eoy | Part I / balance sheet EOY total assets | [F] |
| mgmt_col_l25c | Part IX line 25 column C (management and general) | [F] |
| usable, exclusion_reason | 1 if used in statistics; else the reason(s) (§1.4) | [C] |
| data_flags | Missing/imputed inputs and clipping flags (§1.4) | [C] |
| daf_share_assets, daf_share_grants | Rule A and rule G shares, clipped to [0, 1] | [C] |
| opex_bps_total_assets | Opex ÷ total assets EOY × 10,000 | [C] |
| opex_per_account_whole_org, opex_bps_daf_assets_whole_org | Unallocated ceilings | [C] |
| daf_cost_alloc_A / _G / _AM | Allocated DAF cost under each rule ($) | **[I]** |
| daf_cost_per_account_alloc_A / _G / _AM | Allocated cost ÷ screened accounts | **[I]** |
| daf_cost_bps_daf_assets_alloc_A / _G / _AM | Allocated cost ÷ DAF assets × 10,000 | **[I]** |
| daf_cost_cents_per_grant_dollar_alloc_G | Rule-G cost ÷ DAF grants × 100 | **[I]** |
| it_share_opex, staff_share_opex, fees_11a_11g_share_opex | Line shares of opex | [C] |
| it_per_account_alloc_A | Line 14 × rule-A share ÷ accounts | **[I]** |
| accounts_per_employee | Screened accounts ÷ employees (employees > 0) | [C] |
| daf_fte_alloc_A, accounts_per_daf_fte_alloc_A | Employees × rule-A share; accounts ÷ that | **[I]** |

Metric columns are blank where `usable = 0` or an input is missing.

---

## 6. Source register

| # | Source | Primary URL | Used for |
|---|---|---|---|
| S1 | IRS Form 990 e-file XML (GivingTuesday mirror of the IRS e-file data); every return is listed by `return_object_id` in the CSV | `https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml`, e.g. [Fidelity FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202521349349310887_public.xml), [Community Foundation of the Fox FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202512389349301101_public.xml), [Henry County CF FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543099349300029_public.xml), [Bank of America CGF FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503219349318170_public.xml) | Part IX, Part I, Schedule D (via `sponsor-cost-structure.csv`) |
| S2 | IRS e-file index | [index_2026.csv](https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv) | Return location (harvest) |
| S3 | ProPublica Nonprofit Explorer return pages (human-readable copies) | e.g. [Community Foundation of the Fox](https://projects.propublica.org/nonprofits/organizations/366086742/202512389349301101/full) | Spot checks |
| S4 | IRS, Instructions for Form 990 (Part IX functional columns, line 25, Part I line 5) | [i990.pdf](https://www.irs.gov/pub/irs-pdf/i990.pdf) | Definitions |
| S5 | DAF Research Collaborative sponsor dataset (types, published values) | [Annual DAF Report 2025 dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx) | Sponsor type; corrected values via P-NEW-TAIL-01 |
| R1 | Repo: `daf-long-tail-sponsors-fy2021-2024.csv`, `direction-long-tail-sponsors.md` | – | Universe, bands, corrected FY2024 values, 100 bps census median (as the fee benchmark, superseded by `long-tail-fee-census-2026-11-19.csv` and `tail-fee-pool-revision-2026-11-19.csv`) [b4501-04] [V wave 35A] |
| R2 | Repo: `sponsor-cost-structure.csv`, `scripts/mission_sponsor_cost_structure.py`, `sponsor-cost-structure-and-sensitivities.md` (with validation-wave-5 corrections) | – | Full Part IX per return; opex definition; CF pool comparison |
| R3 | Repo: `form990-returns-schedule-d-harvest-full.csv` | – | Column check (no line 25, no employees) |

**Spot check [C]:** Community Foundation of the Fox (EIN 366086742): opex $1,550,739 × (22,777,440 ÷ 148,593,728 = 0.1533) ÷ 99 accounts = **$2,401** per account and **104 bps** under rule A, as in the CSV.

---

## Appendix: full script print-out (`python3 scripts/mission_long_tail_cost.py .`)

Tables: (1) shares, opex, staff; (2) per account; (3) per DAF dollar; (4) IT and staffing; (5) FY2022–25 robustness; (6) average account and share at or below 100 bps; (7) exclusions. Each cell is median (p25–p75; n).

| Segment | Sponsors | Usable | DAF share of assets | DAF share of grants | Opex (whole org) | Employees | Opex bps of total assets |
|---|---|---|---|---|---|---|---|
| tail_cf | 641 | 635 | 17.7% (7.4%–34.7%; n=603) | 27.6% (9.2%–51.9%; n=590) | $629,935 ($281,556–$1,458,774; n=635) | 5.0 (2.0–9.0; n=635) | 205 (127–367; n=634) |
| tail_cf_10_50m | 207 | 207 | 28.3% (16.6%–43.2%; n=205) | 43.7% (28.6%–64.8%; n=205) | $1,545,473 ($814,436–$2,467,631; n=207) | 9.0 (6.0–13.5; n=207) | 178 (120–289; n=207) |
| tail_cf_1_10m | 272 | 267 | 17.6% (8.4%–28.8%; n=254) | 22.9% (9.3%–46.0%; n=253) | $489,972 ($270,118–$1,001,125; n=267) | 5.0 (2.0–7.0; n=267) | 219 (131–356; n=266) |
| tail_cf_lt1m | 162 | 161 | 3.7% (1.5%–11.8%; n=144) | 5.4% (1.5%–23.6%; n=132) | $281,108 ($72,308–$549,935; n=161) | 2.0 (0.0–4.0; n=161) | 248 (139–537; n=161) |
| tail_si | 547 | 539 | 7.9% (1.1%–32.8%; n=499) | 12.6% (0.8%–53.1%; n=456) | $1,208,131 ($213,874–$6,694,263; n=539) | 5.0 (0.0–34.5; n=539) | 681 (153–2,384; n=538) |
| tail_si_ex_univ | 432 | 425 | 12.5% (2.4%–38.9%; n=394) | 24.0% (2.7%–67.2%; n=361) | $917,108 ($157,557–$4,064,083; n=425) | 5.0 (0.0–23.0; n=425) | 724 (148–2,403; n=424) |
| tail_si_other | 283 | 278 | 12.7% (2.2%–45.5%; n=256) | 12.7% (1.3%–51.3%; n=229) | $851,898 ($106,037–$5,066,924; n=278) | 4.0 (0.0–23.8; n=278) | 1,172 (329–3,379; n=277) |
| tail_si_religious | 149 | 147 | 12.0% (2.5%–34.7%; n=138) | 37.7% (10.2%–78.9%; n=132) | $1,011,456 ($330,946–$3,439,896; n=147) | 6.0 (0.0–22.0; n=147) | 215 (87–846; n=147) |
| tail_si_univ_hosp | 115 | 114 | 0.7% (0.1%–7.3%; n=105) | 0.5% (0.0%–4.6%; n=95) | $4,495,205 ($511,494–$70,622,316; n=114) | 8.5 (0.0–742; n=114) | 403 (171–2,161; n=114) |
| tail_si_10_50m | 69 | 68 | 28.6% (12.6%–54.7%; n=66) | 44.9% (22.0%–93.2%; n=65) | $1,438,077 ($781,975–$10,783,726; n=68) | 8.5 (2.8–67.0; n=68) | 267 (89–856; n=68) |
| tail_si_1_10m | 234 | 229 | 13.6% (2.8%–41.1%; n=220) | 27.9% (3.1%–59.8%; n=201) | $1,560,771 ($275,735–$8,382,658; n=229) | 7.0 (0.0–46.0; n=229) | 562 (143–1,838; n=228) |
| tail_si_lt1m | 244 | 242 | 2.0% (0.4%–13.6%; n=213) | 2.6% (0.0%–18.6%; n=190) | $654,888 ($114,362–$4,227,853; n=242) | 3.0 (0.0–22.8; n=242) | 1,153 (257–3,373; n=242) |
| tail_national | 52 | 46 | 53.9% (12.3%–97.9%; n=41) | 100.0% (51.1%–100.0%; n=40) | $348,958 ($88,192–$1,282,314; n=46) | 0.0 (0.0–0.0; n=46) | 639 (113–1,607; n=45) |
| tail_all | 1240 | 1220 | 14.8% (3.8%–35.7%; n=1143) | 24.6% (4.6%–55.4%; n=1086) | $748,100 ($252,763–$2,371,336; n=1220) | 5.0 (0.0–13.0; n=1220) | 271 (131–885; n=1217) |
| top50_all | 50 | 49 | 77.3% (59.2%–98.2%; n=49) | 93.9% (75.4%–99.9%; n=48) | $18,443,509 ($9,140,988–$31,805,385; n=49) | 68.0 (0.0–137; n=49) | 60 (27–133; n=49) |
| top50_national | 20 | 19 | 99.1% (97.6%–99.6%; n=19) | 99.9% (99.2%–100.0%; n=19) | $14,533,321 ($4,498,148–$30,949,116; n=19) | 0.0 (0.0–71.5; n=19) | 24 (18–48; n=19) |
| top50_cf | 21 | 21 | 65.3% (45.8%–76.0%; n=21) | 75.7% (67.0%–89.7%; n=21) | $26,725,408 ($16,018,398–$30,054,626; n=21) | 97.0 (68.0–141; n=21) | 102 (58–156; n=21) |
| top50_si | 9 | 9 | 63.5% (59.6%–88.8%; n=9) | 88.6% (79.9%–99.8%; n=8) | $15,859,329 ($9,140,988–$32,114,039; n=9) | 34.0 (18.0–183; n=9) | 133 (39–152; n=9) |

| Segment | Whole-org opex per account [C] | Per account, rule A [I] | Per account, rule G [I] | Per account, rule AM [I] | Pooled per account A / G [I] |
|---|---|---|---|---|---|
| tail_cf | $19,413 ($9,857–$39,561; n=553) | $2,859 ($1,458–$6,119; n=549) | $4,106 ($1,827–$9,821; n=536) | $1,179 ($617–$2,418; n=549) | $4,757 / $7,611 |
| tail_cf_10_50m | $18,228 ($9,441–$31,445; n=203) | $4,689 ($2,574–$7,818; n=203) | $7,504 ($3,770–$13,396; n=203) | $1,711 ($969–$3,150; n=203) | $5,091 / $8,197 |
| tail_cf_1_10m | $18,093 ($9,909–$37,061; n=238) | $2,523 ($1,567–$5,638; n=237) | $3,459 ($1,794–$7,510; n=233) | $1,169 ($680–$2,355; n=237) | $4,150 / $6,411 |
| tail_cf_lt1m | $31,493 ($11,273–$71,194; n=112) | $1,012 ($420–$2,707; n=109) | $1,079 ($456–$3,378; n=100) | $499 ($195–$1,064; n=109) | $2,574 / $5,016 |
| tail_si | $86,566 ($11,469–$537,027; n=429) | $5,525 ($1,303–$22,400; n=428) | $7,402 ($907–$36,289; n=391) | $1,544 ($445–$5,652; n=428) | $3,560 / $10,079 |
| tail_si_ex_univ | $67,405 ($8,779–$261,234; n=352) | $4,864 ($1,029–$19,160; n=351) | $7,402 ($909–$34,655; n=321) | $1,293 ($410–$5,337; n=351) | $2,752 / $6,620 |
| tail_si_other | $88,391 ($16,074–$398,337; n=226) | $8,356 ($1,823–$35,819; n=226) | $8,178 ($540–$46,969; n=202) | $1,791 ($574–$7,730; n=226) | $2,509 / $5,813 |
| tail_si_religious | $40,458 ($4,024–$125,579; n=126) | $2,029 ($709–$7,427; n=125) | $6,840 ($1,680–$27,384; n=119) | $797 ($295–$2,228; n=125) | $3,384 / $8,710 |
| tail_si_univ_hosp | $1,210,656 ($90,993–$23,411,928; n=77) | $8,052 ($2,204–$34,776; n=77) | $7,409 ($912–$86,440; n=70) | $2,352 ($707–$8,808; n=77) | $44,683 / $203,797 |
| tail_si_10_50m | $19,458 ($4,539–$90,480; n=63) | $6,840 ($1,557–$21,309; n=63) | $9,421 ($3,332–$32,486; n=61) | $2,101 ($801–$6,264; n=63) | $6,631 / $16,694 |
| tail_si_1_10m | $88,008 ($10,311–$475,168; n=189) | $8,052 ($1,982–$36,670; n=189) | $9,385 ($2,079–$53,132; n=176) | $2,187 ($597–$8,808; n=189) | $2,234 / $6,513 |
| tail_si_lt1m | $128,838 ($27,142–$1,350,004; n=177) | $2,871 ($708–$12,776; n=176) | $2,426 ($80–$23,289; n=154) | $821 ($289–$2,874; n=176) | $8,762 / $44,821 |
| tail_national | $16,183 ($2,709–$42,834; n=37) | $6,569 ($1,252–$18,135; n=36) | $5,821 ($1,136–$30,236; n=34) | $1,503 ($531–$12,148; n=36) | $1,324 / $3,951 |
| tail_all | $27,359 ($9,847–$101,632; n=1019) | $3,512 ($1,415–$9,839; n=1013) | $4,991 ($1,536–$14,417; n=961) | $1,283 ($548–$3,172; n=1013) | $3,547 / $8,362 |
| top50_all | $10,449 ($1,641–$23,047; n=49) | $6,554 ($1,443–$18,055; n=49) | $7,712 ($1,513–$20,721; n=48) | $3,203 ($1,695–$8,314; n=49) | $2,114 / $3,685 |
| top50_national | $1,436 ($772–$2,781; n=19) | $1,425 ($744–$2,769; n=19) | $1,436 ($771–$2,776; n=19) | $1,206 ($275–$2,408; n=19) | $1,342 / $1,349 |
| top50_cf | $20,245 ($15,579–$36,618; n=21) | $12,036 ($7,220–$23,987; n=21) | $16,840 ($10,035–$32,197; n=21) | $5,752 ($3,203–$9,570; n=21) | $12,165 / $15,605 |
| top50_si | $9,152 ($2,529–$41,014; n=9) | $8,127 ($2,370–$34,087; n=9) | $8,400 ($2,181–$21,642; n=8) | $5,631 ($2,826–$7,968; n=9) | $4,776 / $20,645 |

| Segment | Whole-org opex, bps of DAF assets [C] | Rule A, bps of DAF assets [I] | Rule G, bps of DAF assets [I] | Rule AM, bps [I] | Pooled bps A / G [I] | Rule G, cents per DAF grant dollar [I] |
|---|---|---|---|---|---|---|
| tail_cf | 1,284 (559–3,913; n=604) | 205 (127–359; n=603) | 285 (136–602; n=579) | 90 (52–147; n=603) | 255 / 406 | 32.8 (19.5–56.1; n=568) |
| tail_cf_10_50m | 633 (399–1,183; n=205) | 178 (122–285; n=205) | 271 (161–481; n=205) | 67 (45–103; n=205) | 235 / 373 | 27.1 (17.3–43.5; n=205) |
| tail_cf_1_10m | 1,345 (668–2,648; n=255) | 220 (131–362; n=254) | 289 (127–569; n=250) | 100 (60–157; n=254) | 326 / 513 | 34.2 (20.7–58.8; n=244) |
| tail_cf_lt1m | 7,831 (3,071–22,250; n=144) | 248 (137–495; n=144) | 345 (101–966; n=124) | 120 (61–227; n=144) | 615 / 1,240 | 41.1 (24.0–79.1; n=119) |
| tail_si | 10,134 (1,156–84,868; n=499) | 610 (147–2,241; n=499) | 552 (113–3,503; n=441) | 168 (63–363; n=499) | 936 / 2,736 | 55.8 (18.0–167.9; n=403) |
| tail_si_ex_univ | 7,174 (795–50,892; n=394) | 708 (143–2,273; n=394) | 578 (126–3,627; n=349) | 178 (62–390; n=394) | 816 / 1,926 | 51.7 (15.2–145.8; n=321) |
| tail_si_other | 10,232 (1,421–80,790; n=256) | 1,033 (284–3,093; n=256) | 633 (105–4,756; n=220) | 249 (112–526; n=256) | 1,384 / 3,377 | 59.1 (21.5–150.5; n=199) |
| tail_si_religious | 3,017 (437–21,762; n=138) | 206 (88–806; n=138) | 492 (167–2,177; n=129) | 79 (40–196; n=138) | 466 / 1,096 | 31.8 (11.7–131.9; n=122) |
| tail_si_univ_hosp | 69,570 (4,745–887,344; n=105) | 390 (165–1,769; n=105) | 341 (99–2,542; n=92) | 130 (76–280; n=105) | 1,682 / 8,195 | 86.0 (29.3–298.8; n=82) |
| tail_si_10_50m | 798 (320–4,581; n=66) | 267 (89–864; n=66) | 415 (164–916; n=64) | 108 (44–178; n=66) | 656 / 1,630 | 25.7 (9.7–60.5; n=64) |
| tail_si_1_10m | 5,433 (718–32,150; n=220) | 526 (140–1,576; n=220) | 613 (140–2,625; n=197) | 138 (57–314; n=220) | 1,412 / 4,566 | 58.4 (18.1–179.6; n=189) |
| tail_si_lt1m | 50,054 (6,705–362,185; n=213) | 939 (252–3,191; n=213) | 613 (43–9,248; n=180) | 242 (97–521; n=213) | 2,222 / 11,054 | 72.7 (26.6–184.0; n=150) |
| tail_national | 1,330 (328–13,241; n=41) | 639 (118–1,607; n=41) | 415 (95–5,706; n=38) | 122 (54–395; n=41) | 686 / 1,878 | 9.8 (4.0–40.8; n=37) |
| tail_all | 2,293 (624–14,774; n=1144) | 267 (130–852; n=1143) | 344 (131–1,007; n=1058) | 107 (56–232; n=1143) | 462 / 1,095 | 35.3 (18.2–77.8; n=1008) |
| top50_all | 122 (33–242; n=49) | 60 (27–133; n=49) | 76 (32–153; n=48) | 50 (22–77; n=49) | 43 / 74 | 4.8 (1.3–12.2; n=48) |
| top50_national | 24 (19–50; n=19) | 24 (18–48; n=19) | 24 (19–50; n=19) | 22 (10–52; n=19) | 29 / 29 | 1.2 (1.1–2.3; n=19) |
| top50_cf | 162 (130–290; n=21) | 102 (58–156; n=21) | 131 (87–223; n=21) | 57 (37–80; n=21) | 84 / 108 | 10.6 (5.4–14.8; n=21) |
| top50_si | 166 (129–242; n=9) | 133 (39–152; n=9) | 134 (108–189; n=8) | 79 (47–131; n=9) | 153 / 687 | 7.9 (2.8–15.8; n=8) |

| Segment | IT line 14 ($) | IT share of opex | Staff share of opex | 11a+11g share of opex | IT per account, rule A [I] | Accounts per employee (whole org) | DAF FTE, rule A [I] | Accounts per DAF FTE, rule A [I] |
|---|---|---|---|---|---|---|---|---|
| tail_cf | $26,941 ($7,854–$54,286; n=403) | 3.2% (1.4%–5.2%; n=403) | 53.3% (37.1%–63.7%; n=569) | 3.5% (0.0%–14.8%; n=635) | $99 ($37–$212; n=362) | 6.6 (3.2–12.0; n=489) | 0.9 (0.2–1.9; n=603) | 42.3 (24.2–75.6; n=485) |
| tail_cf_10_50m | $54,739 ($29,865–$82,714; n=161) | 3.3% (1.8%–5.1%; n=161) | 56.6% (39.9%–65.7%; n=201) | 3.9% (0.2%–13.7%; n=207) | $146 ($71–$250; n=158) | 9.7 (5.4–16.4; n=195) | 2.3 (1.5–3.7; n=205) | 38.7 (22.5–57.6; n=195) |
| tail_cf_1_10m | $22,112 ($7,179–$35,272; n=161) | 3.3% (1.3%–5.4%; n=161) | 53.9% (39.3%–63.3%; n=243) | 3.9% (0.0%–14.3%; n=267) | $91 ($42–$184; n=148) | 6.0 (3.5–10.3; n=211) | 0.7 (0.3–1.2; n=254) | 40.0 (23.8–70.8; n=210) |
| tail_cf_lt1m | $6,097 ($360–$20,787; n=81) | 2.8% (0.4%–4.9%; n=81) | 47.9% (28.6%–59.9%; n=125) | 0.4% (0.0%–19.3%; n=161) | $29 ($11–$72; n=56) | 2.2 (1.2–5.0; n=83) | 0.1 (0.0–0.2; n=144) | 92.4 (39.6–191; n=80) |
| tail_si | $35,440 ($3,612–$237,062; n=352) | 1.9% (0.7%–3.8%; n=352) | 54.7% (39.8%–66.4%; n=416) | 4.1% (0.0%–13.9%; n=539) | $130 ($19–$607; n=285) | 0.7 (0.1–3.5; n=283) | 0.2 (0.0–2.1; n=499) | 14.2 (3.5–60.0; n=282) |
| tail_si_ex_univ | $25,200 ($2,183–$115,379; n=272) | 1.9% (0.6%–4.0%; n=272) | 54.6% (36.7%–66.6%; n=329) | 3.3% (0.0%–14.2%; n=425) | $99 ($15–$505; n=231) | 1.2 (0.2–4.0; n=244) | 0.2 (0.0–2.1; n=394) | 15.6 (4.7–63.9; n=243) |
| tail_si_other | $22,180 ($2,304–$115,379; n=172) | 1.7% (0.6%–3.8%; n=172) | 52.9% (35.5%–66.0%; n=211) | 4.1% (0.0%–17.2%; n=278) | $156 ($24–$921; n=144) | 0.6 (0.1–2.5; n=150) | 0.2 (0.0–1.9; n=256) | 10.3 (3.3–31.6; n=150) |
| tail_si_religious | $29,188 ($1,794–$115,493; n=100) | 2.3% (0.6%–4.8%; n=100) | 57.6% (42.7%–67.1%; n=118) | 2.3% (0.0%–9.1%; n=147) | $65 ($10–$188; n=87) | 2.0 (0.6–8.3; n=94) | 0.3 (0.0–2.6; n=138) | 50.3 (9.7–155; n=93) |
| tail_si_univ_hosp | $305,630 ($27,192–$3,078,198; n=80) | 1.8% (1.0%–3.2%; n=80) | 55.1% (42.6%–63.1%; n=87) | 6.1% (1.5%–12.5%; n=114) | $200 ($44–$921; n=54) | 0.0 (0.0–0.1; n=39) | 0.0 (0.0–2.2; n=105) | 3.7 (1.0–16.1; n=39) |
| tail_si_10_50m | $63,508 ($19,108–$277,248; n=42) | 2.2% (1.0%–3.8%; n=42) | 56.8% (48.4%–66.2%; n=53) | 5.9% (0.5%–13.4%; n=68) | $200 ($68–$1,066; n=39) | 4.4 (0.8–19.9; n=50) | 2.7 (0.6–11.0; n=66) | 18.4 (4.2–57.3; n=50) |
| tail_si_1_10m | $56,076 ($6,289–$268,310; n=153) | 2.1% (0.8%–3.9%; n=153) | 55.1% (40.7%–67.4%; n=179) | 4.0% (0.0%–11.8%; n=229) | $189 ($32–$975; n=129) | 0.9 (0.1–3.2; n=124) | 0.7 (0.0–3.0; n=220) | 10.8 (1.8–45.9; n=124) |
| tail_si_lt1m | $23,791 ($1,482–$114,994; n=157) | 1.5% (0.5%–3.6%; n=157) | 52.7% (33.9%–64.2%; n=184) | 4.0% (0.0%–15.5%; n=242) | $72 ($13–$252; n=117) | 0.3 (0.1–1.5; n=109) | 0.0 (0.0–0.3; n=213) | 18.9 (5.3–73.3; n=108) |
| tail_national | $5,135 ($0–$95,371; n=23) | 1.1% (0.0%–4.4%; n=23) | 5.1% (0.0%–46.8%; n=25) | 33.5% (1.0%–61.0%; n=46) | $99 ($8–$557; n=16) | 3.7 (0.6–8.3; n=9) | 0.0 (0.0–0.0; n=41) | 25.0 (6.3–69.0; n=9) |
| tail_all | $29,370 ($5,781–$82,605; n=778) | 2.6% (0.9%–4.8%; n=778) | 53.6% (36.6%–64.5%; n=1010) | 3.9% (0.0%–15.2%; n=1220) | $104 ($29–$266; n=663) | 4.1 (1.1–10.0; n=781) | 0.5 (0.0–1.9; n=1143) | 34.2 (13.4–71.6; n=776) |
| top50_all | $748,944 ($283,687–$1,636,568; n=42) | 4.3% (1.8%–6.2%; n=42) | 54.9% (35.0%–62.4%; n=46) | 9.9% (4.9%–21.6%; n=49) | $254 ($124–$536; n=42) | 15.3 (7.5–44.9; n=35) | 34.0 (0.0–87.5; n=49) | 28.9 (11.7–60.9; n=35) |
| top50_national | $533,200 ($2,280–$2,815,788; n=13) | 5.9% (0.0%–21.0%; n=13) | 5.1% (0.8%–43.7%; n=16) | 19.4% (4.6%–85.4%; n=19) | $117 ($0–$203; n=13) | 84.9 (46.2–201; n=6) | 0.0 (0.0–69.8; n=19) | 85.2 (47.4–203; n=6) |
| top50_cf | $894,070 ($395,938–$1,224,309; n=20) | 4.0% (3.2%–6.0%; n=20) | 61.3% (49.0%–65.1%; n=21) | 9.9% (6.0%–15.7%; n=21) | $362 ($240–$612; n=20) | 9.2 (7.4–15.6; n=21) | 48.0 (31.9–85.7; n=21) | 16.3 (11.3–29.3; n=21) |
| top50_si | $664,716 ($478,777–$1,417,939; n=9) | 4.4% (1.3%–5.7%; n=9) | 60.0% (54.9%–63.0%; n=9) | 7.6% (4.6%–9.7%; n=9) | $260 ($103–$827; n=9) | 33.6 (6.6–137; n=8) | 22.4 (16.0–152; n=9) | 47.5 (10.0–144; n=8) |

| Group | FY | Whole-org per account [C] | Per account, rule A [I] | bps of DAF assets, rule A [I] |
|---|---|---|---|---|
| tail_cf | 2022 | $17,292 ($8,515–$37,322; n=626) | $2,462 ($1,218–$5,361; n=626) | 211 (130–378; n=627) |
| tail_cf | 2023 | $17,815 ($9,002–$38,240; n=631) | $2,583 ($1,216–$5,584; n=631) | 198 (128–353; n=632) |
| tail_cf | 2024 | $20,012 ($9,842–$42,359; n=630) | $2,783 ($1,345–$6,128; n=629) | 205 (127–365; n=630) |
| tail_cf | 2025 | $22,099 ($10,764–$40,224; n=302) | $2,709 ($1,327–$6,287; n=302) | 184 (116–302; n=303) |
| tail_si | 2022 | $99,293 ($11,852–$968,444; n=489) | $4,904 ($1,211–$24,247; n=489) | 608 (147–2,157; n=492) |
| tail_si | 2023 | $102,788 ($13,313–$977,513; n=516) | $5,599 ($1,362–$30,465; n=516) | 661 (150–2,250; n=519) |
| tail_si | 2024 | $106,566 ($13,460–$1,131,068; n=531) | $6,092 ($1,392–$32,209; n=530) | 671 (150–2,369; n=533) |
| tail_si | 2025 | $131,052 ($23,042–$1,411,530; n=246) | $6,591 ($1,314–$30,445; n=246) | 705 (136–2,221; n=252) |
| top50_cf | 2022 | $17,347 ($14,410–$36,631; n=21) | $10,725 ($5,679–$19,788; n=21) | 108 (80–144; n=21) |
| top50_cf | 2023 | $20,332 ($14,453–$37,941; n=21) | $11,874 ($6,208–$20,792; n=21) | 104 (75–158; n=21) |
| top50_cf | 2024 | $20,245 ($15,579–$36,618; n=21) | $12,036 ($7,220–$23,987; n=21) | 102 (58–156; n=21) |
| top50_cf | 2025 | $24,925 ($16,414–$49,382; n=9) | $10,805 ($9,419–$18,842; n=9) | 138 (62–173; n=9) |
| top50_all | 2022 | $9,466 ($1,950–$36,155; n=49) | $5,679 ($1,863–$16,436; n=49) | 81 (34–135; n=49) |
| top50_all | 2023 | $11,355 ($1,827–$26,045; n=49) | $6,208 ($1,711–$18,510; n=49) | 75 (29–130; n=49) |
| top50_all | 2024 | $10,449 ($1,641–$23,047; n=49) | $6,554 ($1,443–$18,055; n=49) | 60 (27–133; n=49) |
| top50_all | 2025 | $16,414 ($1,798–$43,197; n=19) | $9,419 ($1,425–$22,316; n=19) | 111 (29–164; n=19) |

| Segment | Median average account (IQR; n) | Share with rule-A cost <= 100 bps [I] | Share with rule-G cost <= 100 bps [I] |
|---|---|---|---|
| tail_cf | $143,987 ($79,110–$249,088; n=550) | 15.3% (n=603) | 18.0% (n=579) |
| tail_cf_10_50m | $242,026 ($173,117–$371,859; n=203) | 16.1% (n=205) | 10.7% (n=205) |
| tail_cf_1_10m | $129,916 ($90,704–$187,413; n=238) | 15.7% (n=254) | 20.4% (n=250) |
| tail_cf_lt1m | $43,771 ($23,054–$66,088; n=109) | 13.2% (n=144) | 25.0% (n=124) |
| tail_si | $112,281 ($37,805–$262,717; n=428) | 17.2% (n=499) | 22.4% (n=441) |
| tail_si_ex_univ | $103,548 ($33,544–$229,639; n=351) | 18.8% (n=394) | 21.8% (n=349) |
| tail_si_other | $92,484 ($22,180–$249,203; n=226) | 11.7% (n=256) | 23.6% (n=220) |
| tail_si_religious | $120,780 ($55,720–$212,550; n=125) | 31.9% (n=138) | 18.6% (n=129) |
| tail_si_univ_hosp | $191,116 ($76,498–$631,888; n=77) | 11.4% (n=105) | 25.0% (n=92) |
| tail_si_10_50m | $225,943 ($130,430–$450,920; n=63) | 28.8% (n=66) | 14.1% (n=64) |
| tail_si_1_10m | $180,736 ($82,530–$420,168; n=189) | 16.8% (n=220) | 20.8% (n=197) |
| tail_si_lt1m | $34,996 ($13,568–$90,480; n=176) | 14.1% (n=213) | 27.2% (n=180) |
| tail_national | $139,292 ($36,631–$587,218; n=36) | 22.0% (n=41) | 26.3% (n=38) |
| tail_all | $133,061 ($61,087–$262,183; n=1014) | 16.4% (n=1143) | 20.1% (n=1058) |
| top50_all | $843,385 ($386,852–$1,399,112; n=49) | 65.3% (n=49) | 52.1% (n=48) |
| top50_national | $386,852 ($269,884–$955,132; n=19) | 94.7% (n=19) | 89.5% (n=19) |
| top50_cf | $1,141,560 ($803,860–$1,399,112; n=21) | 47.6% (n=21) | 28.6% (n=21) |
| top50_si | $964,778 ($592,848–$2,464,446; n=9) | 44.4% (n=9) | 25.0% (n=8) |

| Segment | Exclusions |
|---|---|
| tail_cf | {"opex_nonpositive": 2, "no_fy2024_return_in_cost_file": 4} |
| tail_cf_10_50m | {} |
| tail_cf_1_10m | {"opex_nonpositive": 2, "no_fy2024_return_in_cost_file": 3} |
| tail_cf_lt1m | {"no_fy2024_return_in_cost_file": 1} |
| tail_si | {"opex_nonpositive": 4, "opex_lt_1bp_daf_assets": 2, "no_fy2024_return_in_cost_file": 2} |
| tail_si_ex_univ | {"opex_nonpositive": 3, "opex_lt_1bp_daf_assets": 2, "no_fy2024_return_in_cost_file": 2} |
| tail_si_other | {"opex_nonpositive": 3, "opex_lt_1bp_daf_assets": 1, "no_fy2024_return_in_cost_file": 1} |
| tail_si_religious | {"opex_lt_1bp_daf_assets": 1, "no_fy2024_return_in_cost_file": 1} |
| tail_si_univ_hosp | {"opex_nonpositive": 1} |
| tail_si_10_50m | {"opex_lt_1bp_daf_assets": 1} |
| tail_si_1_10m | {"opex_lt_1bp_daf_assets": 1, "no_fy2024_return_in_cost_file": 2, "opex_nonpositive": 2} |
| tail_si_lt1m | {"opex_nonpositive": 2} |
| tail_national | {"opex_nonpositive": 3, "structural_outlier": 2, "no_fy2024_return_in_cost_file": 1} |
| tail_all | {"opex_nonpositive": 9, "no_fy2024_return_in_cost_file": 7, "structural_outlier": 2, "opex_lt_1bp_daf_assets": 2} |
| top50_all | {"opex_lt_1bp_daf_assets": 1} |
| top50_national | {"opex_lt_1bp_daf_assets": 1} |
| top50_cf | {} |
| top50_si | {} |

<!-- counts --> {"universe": 1290, "tail": 1240, "top50": 50, "tail_flags": {"employees_zero": 314, "accounts_unscreened_or_imputed": 201, "daf_assets_imputed_or_nonpositive": 76, "daf_grants_imputed": 91, "daf_grants_gt_part_ix_grants_clipped": 33, "daf_assets_gt_total_assets_clipped": 15}}
