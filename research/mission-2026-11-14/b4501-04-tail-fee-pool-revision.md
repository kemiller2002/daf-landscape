# P-B4501-04 and P-B45N33-02-03: the long-tail admin-fee pool and fee coverage, on published tail schedules

**Date:** 2026-11-19 · **Queue items:** P-B4501-04 (revise the $92m / 100 bps hypothetical) and P-B45N33-02-03 (fee coverage in the tail) · **Task id:** b4501-04

**Outputs**
- [`scripts/mission_tail_fee_pool.py`](../../scripts/mission_tail_fee_pool.py): stdlib only, functional style, no network. `python3 scripts/mission_tail_fee_pool.py . --task pool` prints every table below and writes the CSV. `python3 scripts/mission_tail_fee_pool.py . --task check-corrections` verifies the Find/Replace list in "Exact corrections" against the files as they stand. It reads them and never writes them.
- [`data/mission-2026-11-14/tail-fee-pool-revision-2026-11-19.csv`](../../data/mission-2026-11-14/tail-fee-pool-revision-2026-11-19.csv): 109 rows (data dictionary in §6).
- [`data/mission-2026-11-14/queue-proposals-b4501-04.csv`](../../data/mission-2026-11-14/queue-proposals-b4501-04.csv): 4 follow-ups.

**Labels:** **[F]** transcribed from a sponsor document (via the fee census, which verified each quote); **[C]** script computation; **[I]** inference. Every pool figure is **[C] on a stated assumption**: what non-publishing sponsors charge is not observed. Allocated operating costs are **[I]** by construction (rules A, G, AM; cost study §1.3). This is research, not legal, tax or accounting advice.

**Governing inputs.** These are the fee census ([`b45n33-01-long-tail-fee-census.md`](b45n33-01-long-tail-fee-census.md)) as corrected by validation wave 34B ([`validation-wave34b-report.md`](validation-wave34b-report.md)), and the cost study ([`b45n33-long-tail-operating-cost.md`](b45n33-long-tail-operating-cost.md)). Wave 34B confirmed six of the seven 2021+ schedules (V34B-25 to 30) and partially confirmed Whatcom's (V34B-24: the live fee page returned a bot-verification page, so the scale rests on the census's 2026-11-19 cache), plus the T7 coverage arithmetic (V34B-32, 33, 38) [V wave 35A] It changed no rate. Its one reclassification, Columbus Medical Association Foundation to `partial`, publishes an unquantified fee ("a quarterly administration fee, based on the size of the fund"), so it adds no rate to this analysis. The census CSV now shows CMAF as `partial` (no `admin_tiers`; `in_2021plus_distribution` = no), so it is outside the schedule set; re-running `--task pool` on the corrected CSV reproduces all 109 rows unchanged [V wave 35A]

---

## 0. Answers in brief

| Question | Answer | Confidence |
|---|---|---|
| **Tail admin-fee pool** | **Central about $138m a year; range about $76m–$184m** [C on the assumptions in §1.3]. *Superseded 2026-11-20 as a fee estimate:* on realised all-fund rates the tail CF pool is $49.4m ($38.5m–$61.5m) and the whole tail $49.4m–$74.3m central ($38.5m–$92.5m) depending on non-CF charging; the published-schedule figures here remain list-price ceilings ([b4427b-0405-realised-tail-fees-all.md](b4427b-0405-realised-tail-fees-all.md)) [V wave 42A] The central case applies the median of the 6 published tail-CF schedules to every tail sponsor's DAF assets ($9.18bn) at its own average account ($137.6m; a flat 150 bps gives $137.7m). Low: only CFs charge ($6.10bn), at the lowest non-zero published schedule (Hutchinson, 125 bps): $76.3m. High: the whole tail at the highest published rate (2%, Cal Poly Pomona): $183.6m. **If only CFs charge, the central case is about $90m**, close to the old $92m but for a different reason. | **Low.** The range rests on **6 CF schedules (7 with one non-CF)** from a 60-sponsor sample in which only 11.7% publish a rate. One of the six publishers charges no admin fee, so the data do not bound the pool away from zero. A seeded bootstrap of the 6-schedule median gives $72m–$155m (90%); with seeds 1, 2, 3 and 42 the endpoints run $65.4m–$72.2m and $155.2m–$162.0m, because a median of six resampled values takes few distinct values [V wave 35A] |
| **What replaces $92m / 100 bps** | Not a single number. On published tail schedules the whole-tail pool is **$127m–$184m** (lowest to highest non-zero schedule). It is $76m–$122m if non-CFs charge nothing. The old $92m is the whole tail at 100 bps, the top-100 CF median. No standard 2021+ tail schedule is that low except ATC's 0%, but Pikes Peak's endowed-DAF column in the same 2025 document (1.00% on the first $3m) is exactly 100 bps at $100k; CF of West Texas's 1.0% is dated 2016 [V wave 35A] | Low (n = 6–7) |
| **Per-sponsor coverage** (P-B45N33-02-03) | At each publisher's own schedule and FY2024 average account, fee revenue covers **rule-A cost at 1 of 7** (Hutchinson: $419.7k against $337.6k), **rule-G cost at 0 of 5** and the **AM floor at 4 of 7**. Median fee ÷ cost: 0.52 / 0.22 / 1.18. Pooled over the publishers, fee revenue ($1.46m) is 0.70 of rule-A cost, 0.23 of rule-G cost and 1.28 of the AM floor [C on the arithmetic; I on the costs]. These reproduce census T7 exactly | Low–medium (n = 5–7) |
| **Tail CFs at a loss** (population) | Each CF schedule was applied to all 603 usable tail CFs at their own average account. At the median schedule, **66.7% of tail CFs run DAFs below rule-A cost, 73.1% below rule-G cost (n = 579) and 24.9% below the AM floor.** Across the five non-zero schedules: A 51.7–74.8%, G 63.6–77.9%, AM 15.3–32.0%. In aggregate the fee recovers a median 0.58 of rule-A cost, 0.36 of rule-G cost and 1.67 of the AM floor [C; I on costs] | Medium on the direction; low on the levels |
| **Reading** | **[I]** At the tail's own published prices, about two thirds of tail CFs still do not recover fully allocated DAF cost from the admin fee, and about three quarters do recover the admin-only floor. The cost study's "most run DAFs at a loss under either rule" survives with the observed fee in place of the hypothetical. The pool stays small: the central $138m is 1.5% a year of $9.18bn of tail DAF assets, and about 0.04% of the $323bn market | [I] |

---

## 1. Method

### 1.1 Fee engine [C]
- **Schedules.** The script re-parses each schedule from the census CSV's `admin_tiers` text, `fee_basis` and `min_annual_fee_usd`. It uses the seven rows with `in_2021plus_distribution = yes`:
  - six CFs: Whatcom, Hutchinson, Pikes Peak, Homer, Athens and Adirondack Trust Company (0%);
  - one non-CF: Cal Poly Pomona.
- **Formula.** Marginal schedules apply each rate to its slice. `flat_on_total` schedules apply the band's rate to the whole balance. The result is max(fee, minimum annual fee) plus any flat fee. This is the census formula.
- **Check.** The recomputed bps at $25k, $100k and $500k must equal the census columns. They do for all 8 schedules, including CF of West Texas (pre-2021). The script stops if any differ.
- **Sensitivity schedules** (the census's own alternative readings, §2.2 there):
  - Whatcom at 1.50% on the first $500k (endowed and long-term-pool funds);
  - Athens read as marginal;
  - Pikes Peak's endowed-DAF column (1.00% on the first $3m).

  Upper tiers that the census did not transcribe for these columns are kept from the standard column. They affect only average accounts above the first tier's ceiling. CF of West Texas (1.0%, "Revised 12/01/16") is shown, but it is outside the 2021+ evidence rule.

### 1.2 Frame [C]
- **Sponsors.** The 1,240 FY2024 tail sponsors (bands `t10_50`, `t1_10`, `t0_1`, `zero`) in `daf-long-tail-sponsors-fy2021-2024.csv`. Corrected DAF assets total **$9,180.1m**, of which CFs hold $6,101.3m (66.5%).
- **Average account.** Each sponsor's own FY2024 screened average account is used where present (1,023 sponsors, 93.8% of assets). Otherwise the sponsor gets the median average account of its `sponsor_category`. Givinga (1.42m "accounts" on $1.95m) has no screened count, so it gets the category median, not a $1 average account.

### 1.3 Pool [C on assumptions]
- **Formula.** For a schedule s and a charge set, pool = Σ DAF assets × fee bps(s, the sponsor's average account) ÷ 10⁴. That is the fee per account at the average account times the implied number of accounts.
- **Assumptions** (none observed):
  1. Every sponsor in the charge set charges schedule s on all of its DAF assets.
  2. All of a sponsor's accounts are at its average size. Account dispersion is not in the data. With a minimum fee, dispersion raises the true fee; with a declining marginal scale, it lowers it.
  3. The fee is charged on year-end assets.
  4. Gift, grant and investment fees are excluded, as in the census.
- **Charge sets:**
  - `whole_tail`: all 1,240 sponsors.
  - `cf_only`: only the 641 CFs charge; non-CFs are at zero. This is a bracketing assumption. It rests on 1 of 29 sampled non-CFs publishing a rate, and on the census's [I] reading that outside CFs \
- **Central figure.** The median of the six CF schedule pools, whole tail. The all-type median (n = 7) is also reported.
- **Range.** Low is the lowest non-zero schedule with CFs only charging. High is the highest schedule with the whole tail charging. The zero-fee schedule (ATC) is reported separately: it is a real observation, so the data do not exclude a pool near zero.
- **Bootstrap.** 20,000 resamples, with replacement, of the 6 (or 7) schedule pools; the median of each resample; 5th and 95th percentiles; seeded with `random.Random(20261119 + i)`. It shows how fragile a median of six is. It is not a population interval.

### 1.4 Coverage [C on arithmetic; I on costs]
- **Per sponsor (P-B45N33-02-03).** Fee revenue = fee at the publisher's own FY2024 average account × screened accounts. It is compared with that sponsor's allocated DAF cost (`daf_cost_alloc_A/G/AM`) in the cost CSV. Coverage = fee per account ÷ allocated cost per account, which is the same as revenue ÷ cost. Rule G is blank where the cost is missing (Homer) or zero (Cal Poly Pomona: DAF grant share 0).
- **Population.** The 604 usable tail CFs with DAF assets in the cost study, of which 603 have a rule-A and AM cost and 579 a rule-G cost. [V wave 35A] For each CF schedule, the fee bps at the CF's own average account (or the tail-CF median, $144.2k ($144,232, over the 551 tail CFs with their own average account), where it is missing) [V wave 35A] is compared with its allocated cost bps. The table counts the CFs whose fee falls below cost, and gives Σ fee ÷ Σ allocated cost.

### 1.5 Corrections check [C]
`--task check-corrections` parses the "Exact corrections" section of this note: each `### \`path\`` heading, then each **Find** / **Replace with** pair in `text` fences. It requires that:
- each Find occurs exactly once in its file;
- each Replace ends with `[b4501-04]`;
- applying the whole list in order, in memory only, succeeds (no Find is consumed by an earlier Replace).

Result on 2026-11-19: **12/12 pass across 5 files**.

---

## 2. Results: the pool

### 2.1 Flat rates on $9.18bn (P1)

| Rate | bps | Whole tail | CFs only |
|---|---|---|---|
| Old hypothetical: top-100 CF median at $100k | 100 | $91.8m | $61.0m |
| Tail-CF published p25 at $100k (n=6) | 131 | $120.5m | $80.1m |
| Tail-CF published median at $100k (n=6; also all-type n=7, and p75) | 150 | $137.7m | $91.5m |
| Highest published rate (Whatcom at $100k; Cal Poly Pomona) | 200 | $183.6m | $122.0m |

Published bps at $100k: CFs 0, 125, 150, 150, 150, 200; plus Cal Poly Pomona 200 [C]. The p75 equals the median because three of the six are 150.

### 2.2 Each schedule applied at every sponsor's own average account (P2)

| Schedule | Kind | Whole tail | bps | Whole tail, no minimum fee | CFs only | CFs-only bps |
|---|---|---|---|---|---|---|
| Whatcom CF | published | $179.6m | 195.6 | $179.6m | $120.9m | 198.2 |
| Hutchinson CF | published | $127.1m | 138.5 | $113.6m | $76.3m | 125.0 |
| Pikes Peak CF | published | $149.9m | 163.2 | $136.6m | $91.5m | 150.0 |
| Homer Foundation | published | $144.4m | 157.3 | $137.0m | $91.4m | 149.9 |
| Adirondack Trust Co. Community Fund | published | $0.0m | 0.0 | $0.0m | $0.0m | 0.0 |
| Athens County Foundation | published | $130.9m | 142.6 | $130.9m | $88.3m | 144.8 |
| Cal Poly Pomona Philanthropic Fdn | published | $183.6m | 200.0 | $183.6m | $122.0m | 200.0 |
| CF of West Texas | pre-2021 | $91.8m | 100.0 | $91.8m | $61.0m | 100.0 |
| Whatcom at 1.50% | alternative | $136.7m | 149.0 | $136.7m | $91.4m | 149.9 |
| Athens, marginal | alternative | $134.6m | 146.6 | $134.6m | $90.5m | 148.4 |
| Pikes Peak, endowed column | alternative | $105.0m | 114.4 | $91.2m | $61.1m | 100.1 |

- **[C] Minimum fees matter only at the small end.** The $150–$250 minimums add $7–14m to the whole-tail pool (Hutchinson, Pikes Peak, Homer). Almost all of that comes from small-account non-CF sponsors, so the CFs-only figures barely move.
- **[C] The interpretation choices move single schedules by up to $45m** (Pikes Peak endowed column, −$44.9m), but the central figure hardly. With the three alternative readings substituted, the six CF pools are 0, 105.0, 127.1, 134.6, 136.7 and 144.4, so the median is $130.9m, about $7m below the central figure [C, from the table].

### 2.3 Range (P3; 2021+ schedules with minimum fees)

| Schedule set | Charge set | n | Central (median) | Lowest non-zero | Highest | Bootstrap 90% of the median | Zero-fee schedule |
|---|---|---|---|---|---|---|---|
| CF schedules | whole tail | 6 | **$137.6m** | $127.1m | $179.6m | $72.2m–$155.2m | $0 |
| CF schedules | CFs only | 6 | **$89.9m** | **$76.3m** | $120.9m | $45.7m–$104.6m | $0 |
| All 7 schedules | whole tail | 7 | $144.4m | $127.1m | **$183.6m** | $127.1m–$179.6m | $0 |
| All 7 schedules | CFs only | 7 | $91.4m | $76.3m | $122.0m | $76.3m–$120.9m | $0 |

**Headline: central about $138m; range about $76m–$184m** (bold cells). These are list-price figures; realised all-fund rates give $49.4m for CFs and $49.4m–$74.3m for the whole tail (b4427b-0405) [V wave 42A] The central and high figures have the whole tail charging CF-type (or Cal Poly Pomona's) prices; the low figure has non-CFs charging nothing. The range therefore spans the charge-set assumption as well as the schedule spread, and the CFs-only central ($89.9m) is as defensible a central figure as the whole-tail one. [V wave 35A] As a share of tail DAF assets that is 0.83–2.0%, central 1.5%.

**Small sample, stated plainly.** The range is built from 6 CF schedules and one non-CF schedule. They come from a stratified sample of 60 tail sponsors, of whom 7 (11.7%; Wilson 5.8–22.2%) publish a 2021+ rate. The publishers lean to the $10–50m band (3 of 6 CFs). The sample's non-publishers may charge more, less or nothing. The bootstrap interval of the 6-schedule median ($72m–$155m) is wider than the gap between the old figure and the new central figure. The central figure should be cited only with its range.

---

## 3. Results: coverage (P-B45N33-02-03)

### 3.1 Each publisher at its own schedule and average account (C1)

| Sponsor | Avg account | Accounts | Fee bps | Fee revenue | Allocated cost A / G / AM | Coverage A / G / AM | Covers A/G/AM |
|---|---|---|---|---|---|---|---|
| Whatcom CF | $133,370 | 96 | 200.0 | $256,070 | $490,108 / $2,913,023 / $144,647 | 0.52 / 0.09 / 1.77 | no/no/yes |
| Hutchinson CF | $409,491 | 82 | 125.0 | $419,728 | $337,599 / $1,184,894 / $183,823 | 1.24 / 0.35 / 2.28 | yes/no/yes |
| Pikes Peak CF | $262,074 | 179 | 150.0 | $703,669 | $1,019,362 / $1,758,872 / $594,357 | 0.69 / 0.40 / 1.18 | no/no/yes |
| Homer Foundation | $110,443 | 18 | 150.0 | $29,820 | $77,277 / – / $76,237 | 0.39 / – / 0.39 | no/–/no |
| Adirondack Trust Co. CF | $198,266 | 28 | 0.0 | $0 | $23,010 / $24,427 / $38,786 | 0.00 / 0.00 / 0.00 | no/no/no |
| Athens County Fdn | $173,340 | 18 | 150.0 | $46,802 | $143,599 / $216,516 / $97,681 | 0.33 / 0.22 / 0.48 | no/no/no |
| Cal Poly Pomona | $28,302 | 1 | 200.0 | $566 | $910 / $0 / $217 | 0.62 / – / 2.61 | no/–/yes |
| *Whatcom at 1.50%* | | | 150.0 | $192,053 | as above | 0.39 / 0.07 / 1.33 | no/no/yes |
| *Athens, marginal* | | | 150.0 | $46,802 | as above | 0.33 / 0.22 / 0.48 | no/no/no |
| *Pikes Peak, endowed column* | | | 100.0 | $469,112 | as above | 0.46 / 0.27 / 0.79 | no/no/**no** |

| Rule | Fee ≥ cost | Median fee ÷ cost | Σ fee revenue ÷ Σ cost |
|---|---|---|---|
| A | 1 of 7 | 0.52 | 0.70 |
| G | 0 of 5 | 0.22 | 0.23 |
| AM | 4 of 7 | 1.18 | 1.28 |

- **[C] These reproduce census T7.** They were computed independently from the parsed schedules and the cost CSV, not copied from it.
- **[C] One reading changes a count.** On the endowed-DAF column, Pikes Peak no longer covers the AM floor, so AM drops to 3 of 7.
- **[C] CF of West Texas** (pre-2021, 1.0%) has no screened account count, so its fee revenue cannot be formed. On a per-dollar basis, its 100 bps sits below its allocated cost under rules A (151 bps) and G (125 bps), and above the AM floor (43 bps) (cost CSV).
- **[C] Pooled ratios are driven by Pikes Peak and Hutchinson**, the two largest publishers. That is why Σ revenue ÷ Σ cost (0.70 for A) is above the median ratio (0.52).

### 3.2 All usable tail CFs at each CF schedule (C2)

| Rule | CFs below cost at the median schedule | Range over the 5 non-zero schedules | At the zero-fee schedule | Aggregate fee ÷ cost (median schedule) |
|---|---|---|---|---|
| A (n = 603) | **66.7%** | 51.7% (Whatcom) – 74.8% (Hutchinson) | 100.0% | 0.58 |
| G (n = 579) | **73.1%** | 63.6% – 77.9% | 97.4% | 0.36 |
| AM (n = 603) | **24.9%** | 15.3% – 32.0% | 98.0% | 1.67 |

The full 18-row table (each schedule × rule) is in the CSV (`section = population_coverage`). The median of six is the mean of the 3rd and 4th values. Under rule A the six shares sort to 51.7, 66.0, 66.2, 67.3, 74.8 and 100.0%, so the median is (66.2 + 67.3) ÷ 2 = 66.7%, with ATC's zero fee included.

- **[C] Consistency with census T9.** T9 counts CFs with cost ≤ 150 bps under rule A: 33.7%, so 66.3% are above it. The schedule-based 66.0–67.3% at the three 150 bps schedules agrees. The small gap comes from minimum fees and Athens's band.
- **[I] Reading.** Replacing the 100 bps hypothetical with published tail prices narrows the loss share under rule A from about 85% to about two thirds. It does not reverse it. Under the admin-only floor, about three quarters of tail CFs cover cost. As the census said, the tail fee is priced nearer to overhead than to fully allocated cost. Rules A and G load non-DAF activity onto DAFs (cost study §1.3), so these "loss" shares are upper-leaning.

---

## 4. Every repository passage that uses the 100 bps / $92m hypothetical

Found with `grep -rn` over `research/` and `data/` for `$92m`, `100 bps`, `100bps` and `fee pool`, then read in context. The list also includes passages that say the tail has no published fee, because they rest on the same gap.

| # | File | Line (2026-11-19) | Passage | Action |
|---|---|---|---|---|
| 1 | `direction-long-tail-sponsors.md` | 38 | §0 "Published fee": none of the 1,240 has a published fee | Correction 1 (related) |
| 2 | `direction-long-tail-sponsors.md` | 39 | §0: "about $92m a year if the whole tail charged the 100 bps CF median" | Correction 2 |
| 3 | `direction-long-tail-sponsors.md` | 241 | §3.6: "the repo has no tail fee observation" | Correction 3 (related) |
| 4 | `direction-long-tail-sponsors.md` | 277 | §5.1: "Not yet shown: the tail's actual fees … and its cost base" | Correction 4 (related) |
| 5 | `direction-long-tail-sponsors.md` | 293 | §5.7: "At the 100 bps median CF admin rate … about $92m a year" | Correction 5 |
| 6 | `strategic-synthesis.md` | 558 | D: "At the 100 bps CF median … about $92m a year" | Correction 6 |
| 7 | `b45n33-long-tail-operating-cost.md` | 25 | §0: "Only 15.3% (rule A) and 18.0% (rule G) … at or below 100 bps … hypothetical fee" | Correction 7 |
| 8 | `b45n33-long-tail-operating-cost.md` | 144 | §2.4: "Against the fee side … top-100 CF census median of 100 bps" | Correction 8 |
| 9 | `b45n33-long-tail-operating-cost.md` | 176 | §4: "No fee data for the tail; the 100 bps comparison is a hypothetical" | Correction 9 |
| 10 | `b45n33-long-tail-operating-cost.md` | 225 | §6 R1: "100 bps census median" | Correction 10 |
| 11 | `consolidation-changelog-wave30.md` | 41 | "N33: tail fee pool about $92m a year" | Correction 11: a superseded note is appended and the history kept |
| 12 | `DAF-INDUSTRY-REPORT-2026-11.md` | 924 | §11.27: "No tail sponsor has a published fee in the repo." The report has no `$92m` passage | Correction 12 (related) |
| – | `data/…/validation-register-wave30.csv` | V30-38 | Records that wave 30 confirmed the $92m arithmetic | **Not changed.** It is a validation record of what was checked then |
| – | `data/…/research-priority-inputs.csv`, `research-priority-queue.csv`, `queue-proposals-b45n33-01.csv` | P-B4501-04 rows | The queue item's own text | Not changed (queue state is managed elsewhere) |
| – | `b45n33-01-long-tail-fee-census.md` | 24, 167–168, 175, 177, 388 | Uses 100 bps only as the named top-100 comparator; §3 item 2 already flags the $92m | No change needed: consistent with this note |
| – | `b45n33-long-tail-operating-cost.md` | 134, 340 (tables) | "Share with rule-A cost ≤ 100 bps": script output at a fixed threshold | No change: a threshold statistic, not a fee claim |
| – | `direction-cf-consolidation-fees.md` | 193 | Top-100 CF median 100 bps at $100k | No change: the top-100 figure itself |
| – | `sponsor-cost-structure-and-sensitivities.md` | 149 | "$92m / 456 bps" (National-Processor cost) | Unrelated |

---

## Exact corrections

Apply in order. Each Find is verbatim, occurs exactly once in its file as it stands on 2026-11-19, and is checked by `python3 scripts/mission_tail_fee_pool.py . --task check-corrections` (12/12 pass). Each Replace ends with `[b4501-04]`. Inside table rows, each Find stops before the cell's closing pipe, so the table structure is kept.

### `research/mission-2026-11-14/direction-long-tail-sponsors.md`

1. **§0 "Published fee" row** (related).
   - **Find:**
```text
**None of the 1,240 tail sponsors has a published fee in the repository** [C]:<br>- the CF fee census stops at the 100th-largest CF ($101.4m);<br>- the national schedules cover 11 sponsors, all above $50m.<br>For comparison, 16 of the top 50 have a published schedule in the repository. **This is the largest gap in this profile** (P-B45N33-01). | High on the absence
```
   - **Replace with:**
```text
**When this profile was written, no tail sponsor had a published fee in the repository; the fee census (P-B45N33-01) has since sampled 60.** 7 of them (11.7%; Wilson 5.8–22.2%) publish a 2021+ admin rate and 16 (26.7%) some fee term; 6 of 31 sampled CFs publish a rate. At $100k the published rates run 0–200 bps, with a CF median of 150 bps (n = 6), against 100 bps for top-100 CFs ([b45n33-01-long-tail-fee-census.md](b45n33-01-long-tail-fee-census.md); [b4501-04-tail-fee-pool-revision.md](b4501-04-tail-fee-pool-revision.md)). | High on the publication count; low on the fee level (n = 6–7) [b4501-04]
```
2. **§0 "What an AI-native platform could offer": revenue pool.**
   - **Find:**
```text
Its revenue pool is small: about $92m a year if the whole tail charged the 100 bps CF median [C on that assumption].
```
   - **Replace with:**
```text
Its admin-fee pool is small: about $138m a year if the whole tail charged like the median published tail CF, within about $76m–$184m (CFs only at the lowest non-zero published schedule, up to the whole tail at the highest). The earlier $92m used the top-100 CF median of 100 bps. Only 11.7% of sampled tail sponsors publish a rate, so the range rests on 6–7 schedules [C on those assumptions] [b4501-04]
```
3. **§3.6 "Fee" bullet** (related).
   - **Find:**
```text
- **Fee:** the repo has no tail fee observation. P-B45N33-01 fills this.
```
   - **Replace with:**
```text
- **Fee:** P-B45N33-01 found a 2021+ admin rate at 7 of 60 sampled tail sponsors (6 of 31 CFs): 0–200 bps at $100k, CF median 150 bps ([b45n33-01-long-tail-fee-census.md](b45n33-01-long-tail-fee-census.md)) [b4501-04]
```
4. **§5 item 1 "Not yet shown"** (related).
   - **Find:**
```text
   - **Not yet shown:** the tail's actual fees (P-B45N33-01) and its cost base (P-B45N33-02).
```
   - **Replace with:**
```text
   - **Since shown:** 7 of 60 sampled tail sponsors publish a 2021+ admin rate (P-B45N33-01). At its own average account, the published fee covers rule-A allocated DAF cost at 1 of 7 publishers and the admin-only floor at 4 of 7 (P-B45N33-02, P-B45N33-02-03; [b4501-04-tail-fee-pool-revision.md](b4501-04-tail-fee-pool-revision.md)) [b4501-04]
```
5. **§5 item 7 "Size the prize honestly": the pool.**
   - **Find:**
```text
   - At the 100 bps median CF admin rate (top-100 census, $100k–$1m), the tail's entire admin-fee pool would be about **$92m a year** [C on that assumption].
```
   - **Replace with:**
```text
   - The tail's entire admin-fee pool is about **$138m a year** if every tail sponsor applied the median published tail-CF schedule at its own average account, within about **$76m–$184m**. The low end has only CFs charging, at the lowest non-zero published schedule (Hutchinson, 125 bps); the high end has the whole tail at the highest (2%). If only CFs charge, the central figure is about $90m. The earlier $92m applied the top-100 CF median (100 bps). The range rests on 6 CF schedules (7 with Cal Poly Pomona) from a 60-sponsor sample in which 11.7% publish a rate, and one publisher charges no admin fee ([b4501-04-tail-fee-pool-revision.md](b4501-04-tail-fee-pool-revision.md)) [C on those assumptions] [b4501-04]. Non-publishing tail CFs do charge: 7 of 25 sampled disclose internal fees at a realised 70–129 bps of total assets (FY2022–24). Those all-fund rates applied to tail CF DAF assets give about $63m ($10.7m–$79.0m), a floor-type figure that bounds the CF pool away from zero. The non-CF part ($3.08bn) is untested (b4427b-b4501 §3) [V wave 41B]
```

### `research/mission-2026-11-14/strategic-synthesis.md`

6. **D. "Do not enter the long tail as a standalone business".**
   - **Find:**
```text
At the 100 bps CF median, their whole admin-fee pool would be about $92m a year [C on that assumption] (wave 30).
```
   - **Replace with:**
```text
Their whole admin-fee pool is about $138m a year if every tail sponsor charged like the median published tail CF (150 bps at $100k), within about $76m–$184m, or about $90m if only CFs charge. That rests on 6–7 published schedules: only 11.7% of 60 sampled tail sponsors publish a rate (wave 30; [b4501-04-tail-fee-pool-revision.md](b4501-04-tail-fee-pool-revision.md)) [C on those assumptions] [b4501-04]. Realised internal fees at 8 tail CFs (70–129 bps of total assets, FY2022–24) give about $63m on tail CF DAF assets as a floor-type figure; the whole-tail $138m still rests on untested non-CF charging (b4427b-b4501 §3) [V wave 41B]
```

### `research/mission-2026-11-14/b45n33-long-tail-operating-cost.md`

7. **§0 "What DAF administration plausibly carries": fee comparison.**
   - **Find:**
```text
Only 15.3% (rule A) and 18.0% (rule G) of tail CFs have allocated cost at or below 100 bps, the top-100 CF census median admin fee (a hypothetical fee for the tail, which has no fee in the repo). At the median, a 100 bps fee would cover about half (100 ÷ 205) of rule-A cost.
```
   - **Replace with:**
```text
Against published tail fees (P-B45N33-01: 6 CF schedules, 0–200 bps at $100k, median 150), each applied to every usable tail CF at its own average account, the median schedule leaves 66.7% of tail CFs below rule-A cost (n = 603), 73.1% below rule-G cost (n = 579) and 24.9% below the AM floor. Across the five non-zero schedules the rule-A share runs 51.7–74.8%. At the medians, a 150 bps fee covers about 73% (150 ÷ 205) of rule-A cost. The earlier comparison used the top-100 median of 100 bps, at or below which sit 15.3% (A) and 18.0% (G) of tail CFs ([b4501-04-tail-fee-pool-revision.md](b4501-04-tail-fee-pool-revision.md)) [b4501-04]
```
8. **§2.4 "Against the fee side".**
   - **Find:**
```text
- **[C] Against the fee side.** The repo's only CF fee benchmark is the top-100 CF census median of 100 bps (`direction-long-tail-sponsors.md` §0; no tail sponsor has a published fee). Only **15.3%** of tail CFs (rule A, n = 603) and **18.0%** (rule G, n = 579) have DAF cost at or below 100 bps. At the median, a 100 bps fee would cover about 49% (100 ÷ 205) of rule-A cost and 35% (100 ÷ 285) of rule-G cost. **[I] If tail CFs charge near the census median, most run DAFs at a loss under either rule, covered by unrestricted, endowment or agency-fund income.** This needs tail fee data (P-B45N33-01, P-B45N33-02-03).
```
   - **Replace with:**
```text
- **[C] Against the fee side.** The fee census (P-B45N33-01) found 6 published 2021+ tail-CF schedules: 0–200 bps at $100k, median 150 bps, against the top-100 CF median of 100 bps. Each applied to every usable tail CF at its own average account, the median schedule leaves **66.7%** of tail CFs below rule-A cost (n = 603; 51.7–74.8% across the five non-zero schedules), **73.1%** below rule-G cost (n = 579) and **24.9%** below the AM floor. In aggregate the fee recovers a median 0.58 of rule-A and 0.36 of rule-G cost. At the medians, 150 bps covers about 73% (150 ÷ 205) of rule-A cost and 53% (150 ÷ 285) of rule-G cost. At each publisher's own average account, the fee covers rule-A cost at 1 of 7, rule-G cost at 0 of 5 and the AM floor at 4 of 7 (P-B45N33-02-03). **[I] At observed tail prices, most tail CFs still run DAFs below fully allocated cost under either rule, covered by unrestricted, endowment or agency-fund income, while about three quarters cover the admin-only floor.** The fee level rests on n = 6 ([b4501-04-tail-fee-pool-revision.md](b4501-04-tail-fee-pool-revision.md)) [b4501-04]
```
9. **§4 Limits: fee data.**
   - **Find:**
```text
- **No fee data for the tail**; the 100 bps comparison is a hypothetical benchmark from the top-100 census.
```
   - **Replace with:**
```text
- **Tail fee data are thin**: the fee comparison uses 6 published tail-CF schedules (P-B45N33-01) from a sample in which 11.7% of sponsors publish a rate; the 100 bps top-100 median is kept only as a reference [b4501-04]
```
10. **§6 source register R1.**
    - **Find:**
```text
| Universe, bands, corrected FY2024 values, 100 bps census median
```
    - **Replace with:**
```text
| Universe, bands, corrected FY2024 values, 100 bps census median (as the fee benchmark, superseded by `long-tail-fee-census-2026-11-19.csv` and `tail-fee-pool-revision-2026-11-19.csv`) [b4501-04]
```

### `research/mission-2026-11-14/consolidation-changelog-wave30.md`

11. **Row 10 (history kept; superseded note appended).**
    - **Find:**
```text
N33: tail fee pool about $92m a year [C on assumption]
```
    - **Replace with:**
```text
N33: tail fee pool about $92m a year [C on assumption] (superseded 2026-11-19: about $138m central, $76m–$184m range on published tail schedules, n = 6–7; b4501-04-tail-fee-pool-revision.md) [b4501-04]
```

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

12. **§11.27 long-tail bullet** (related; the report has no `$92m` passage).
    - **Find:**
```text
No tail sponsor has a published fee in the repo. AI-native implications are inference only.
```
    - **Replace with:**
```text
When this section was validated, no tail sponsor had a published fee in the repo; §11.35 now reports 7 of 60 sampled tail sponsors with a 2021+ rate. On those schedules the tail admin-fee pool is about $138m a year central, $76m–$184m in range, resting on 6–7 schedules ([b4501-04-tail-fee-pool-revision.md](mission-2026-11-14/b4501-04-tail-fee-pool-revision.md)). AI-native implications are inference only [b4501-04]
```

---

## 5. Limits
1. **Small n.** The pool range and every coverage count rest on 6 CF schedules and 1 non-CF schedule. A single extra schedule at 100 bps or 250 bps would move the median. The bootstrap ($72m–$155m for the 6-schedule median) shows this. P-B4501-01 (60 more tail CFs) is the fix.
2. **Non-publishers are not observed.** 53 of the 60 sampled sponsors publish no rate. The pool assumes they charge like publishers (whole tail) or that non-CFs charge nothing (CFs only). Neither is evidenced. P-B4501-02, realised fee revenue from 990s and audits, would test this.
3. **The average-account approximation.** Each sponsor's accounts are treated as equal in size. Minimum fees bite harder, and marginal scales less, with real dispersion.
4. **Year-end assets** stand in for the fee base (average daily or quarterly balances in the schedules). Gift fees (Whatcom's short-term-pool fee, CFCW's 3% card fee), grant fees and investment fees are excluded, so the admin pool understates total sponsor revenue.
5. **Interpretation choices** (Whatcom, Athens, Pikes Peak) move single schedules by up to $45m and the central figure by about $7m (§2.2). Upper tiers in the alternative columns were not transcribed by the census and are carried from the standard column.
6. **Allocated cost is [I].** Rules A and G load non-DAF cost onto DAFs; AM understates CFs (cost study §1.3). The loss shares are only as good as the allocation.
7. **Dates.** Fees come from 2021–2026 documents (three undated live pages); costs and accounts are FY2024. CF of West Texas (2016) is excluded from the range under the 2021+ rule.
8. **The CMAF reclassification** (wave 34B) is now reflected in the census CSV (`fee_status` = `partial`). It does not affect this note, which uses only rows with a rate; the re-run on the corrected CSV is identical [V wave 35A]
9. **No network requests** were made. All inputs are repository files; the primary sources are those of the fee census and the cost study (§7).

---

## 6. Data dictionary: `tail-fee-pool-revision-2026-11-19.csv`

One table in long format. `section` says which columns are filled.

| Column | Meaning |
|---|---|
| `section` | `pool_flat_rate` (P1), `pool_schedule` (P2), `pool_summary` (P3), `sponsor_coverage` (C1), `population_coverage` (C2) |
| `scenario_id` | Row key: e.g. `flat_cf_median`, `sched_published_841339670_whole_tail_min`, `summary_cf6_whole_tail_central`, `cov_published_481076910`, `pop_A_911726410` |
| `description` | Plain-language label (schedule or scenario) |
| `schedule_kind` | `published` (2021+), `pre2021`, `alternative` (census sensitivity reading) |
| `ein`, `name`, `type4`, `fee_status` | Schedule owner (fee census) |
| `charge_set` | `whole_tail` (1,240 sponsors) or `cf_only` (641 CFs; non-CFs at zero) |
| `use_min_fee` | `yes` if the minimum annual fee is applied at the average account |
| `rate_bps` | Flat rate used (P1 only) |
| `n_basis` | Sponsors in the charge set (P1, P2) or schedules summarised (P3) |
| `daf_assets_charged_usd` | Corrected FY2024 DAF assets of the charge set |
| `fee_pool_usd` | Annual admin-fee pool [C on §1.3 assumptions] |
| `implied_bps` | `fee_pool_usd` ÷ assets charged × 10⁴ |
| `avg_account_usd`, `accounts`, `daf_assets_usd` | Publisher's FY2024 average account, screened accounts and DAF assets (C1) |
| `fee_per_account_usd`, `fee_bps_at_avg` | Published fee at that average account [C] |
| `fee_revenue_usd` | Fee per account × screened accounts [C] |
| `cost_alloc_A_usd` / `_G_` / `_AM_` | Allocated DAF operating cost from the cost CSV [I] |
| `cost_bps_A` / `_G` / `_AM` | The same per DAF dollar, bps [I] |
| `coverage_A` / `_G` / `_AM` | Fee revenue ÷ allocated cost (= fee per account ÷ cost per account) |
| `covers_A` / `_G` / `_AM` | `yes` if coverage ≥ 1; blank if cost is missing or zero |
| `rule`, `share_k`, `share_n`, `share_value` | C2: allocation rule; tail CFs with fee below cost; CFs with that rule's cost; share |
| `cost_pool_usd`, `aggregate_coverage` | C2: Σ allocated cost over those CFs; Σ fee ÷ Σ cost |
| `notes` | Bootstrap note on P3 rows |

---

## 7. Source register

All schedule figures come through the fee census, which fetched each document after a robots.txt check with `research-script/1.0` on 2026-11-19 and verified every quote (15/15). Wave 34B re-fetched them (V34B-24 to 31). This note made no requests.

| # | Source | Primary URL | Used for |
|---|---|---|---|
| S1 | Whatcom CF fee page; Non-Endowed T&C (12/31/2025) | https://whatcomcf.org/financial-oversight/investment-approach-fees/ ; https://whatcomcf.org/wp-content/uploads/2025/12/Non-Endowed-Funds-Terms-and-Conditions-12.2025.pdf | 2.00/1.50/1.25/1.00% scale; 1.50% alternative |
| S2 | Hutchinson CF DAF fee schedule | https://hutchcf.org/wp-content/uploads/2025/02/2023-fee-schedules_DAF.pdf | 1.25% to $2m, $250 minimum |
| S3 | Pikes Peak CF fund types and fees | https://www.ppcf.org/wp-content/uploads/2025/01/Fund-Types-Fee-Structure.pdf | Non-endowed and endowed DAF columns; $250 minimum |
| S4 | Homer Foundation Funds Policy (Jan 2021) | https://www.cityofhomer-ak.gov/sites/default/files/fileattachments/memo/72719/01-01_funds_policy_v.1.28.21.pdf | 1.5%, $150 minimum |
| S5 | Athens County Foundation | https://www.athensfoundation.org/create-a-fund ; https://www.athensfoundation.org/daf | 1.5% / 1% |
| S6 | Adirondack Trust Co. Community Fund | https://atccf.org/Donor-Options/donor-advised-fund | No admin charge |
| S7 | Cal Poly Pomona Philanthropic Fdn DAF policy | https://www.cpp.edu/philanthropy/policies/504philanthropic-donorsadvisedfundpolicy.pdf | 2% |
| S8 | CF of West Texas (Revised 12/01/16) | https://www.cfwtx.org/_files/ugd/416dfb_6eb9ed0847e14a06b62f37087d507867.pdf | 1.0%, pre-2021 sensitivity only |
| S9 | Columbus Medical Association Fdn (wave 34B) | https://cmafohio.org/create-a-personalized-charitable-fund | Unquantified fee; no rate used |
| S10 | IRS Form 990 e-file XML (GivingTuesday mirror), per `return_object_id` in the cost CSV | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml | Part IX and Schedule D behind the allocated costs and accounts |
| S11 | DAF Research Collaborative dataset | https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx | Sponsor universe and types (via the long-tail file) |
| R1 | Repo: `long-tail-fee-census-2026-11-19.csv`, `b45n33-01-long-tail-fee-census.md`, `validation-wave34b-report.md` | – | Schedules, sample, corrections |
| R2 | Repo: `long-tail-operating-cost-2026-11-19.csv`, `b45n33-long-tail-operating-cost.md` | – | Allocated DAF cost, rules A / G / AM |
| R3 | Repo: `daf-long-tail-sponsors-fy2021-2024.csv` | – | 1,240 tail sponsors, assets, average accounts |
