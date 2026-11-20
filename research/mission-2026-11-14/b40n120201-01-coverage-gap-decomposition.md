# What the 15.1% coverage gap is made of, and a bounded replacement for the 1/0.849 scaling (P-B40N120201-01)

**Date:** 2026-11-20 · **Task ID:** b40n120201-01 · **Queue item:** P-B40N120201-01 (from [queue-proposals-b40n1202-01.csv](../../data/mission-2026-11-14/queue-proposals-b40n1202-01.csv)) · **Builds on:** [b40n1202-01-non-top50-numerator.md](b40n1202-01-non-top50-numerator.md) and its wave 40B corrections ([validation-wave40b-report.md](validation-wave40b-report.md), V40B-01 to V40B-16)

**Outputs**
- Script: [`scripts/mission_coverage_gap.py`](../../scripts/mission_coverage_gap.py). It is new. It imports `mission_non_top50_numerator.py` (and through it the committed recipient-share modules) and modifies nothing.
- Data: [`data/mission-2026-11-14/coverage-gap-decomposition-2026-11-20.csv`](../../data/mission-2026-11-14/coverage-gap-decomposition-2026-11-20.csv). 3,454 rows: 52 component, 24 bound, 360 recipient-share, 58 allocation, 2,705 itemising sponsor-year and 255 non-itemising sponsor-year rows. Data dictionary in §6.
- Queue proposals: [`data/mission-2026-11-14/queue-proposals-b40n120201-01.csv`](../../data/mission-2026-11-14/queue-proposals-b40n120201-01.csv)

Tags: [F] computed from filings by the script · [P] quoted primary source · [I] inference or allocation assumption.

## 0. Answer in brief

- **The 15.1-point gap, FY2024, in points of netted DAF grants ($58.41bn) [F].** It reconciles exactly (residual $0) against DAFRC corrected grants, R5 netting and Part IX of every panel return:

  | Component | USD | Points | Reaches domestic frame recipients? |
  |---|---|---|---|
  | Schedule F foreign grants (Part IX line 3 × DAF weight) | $1.76bn | **3.0** | No |
  | Non-itemised domestic grants (Part IX line 1 − Schedule I total, × DAF weight) | $2.78bn | **4.8** | Yes |
  | · of which sponsors itemising ≥50% of line 1 (small gifts) | $1.97bn | 3.4 | Yes, spread toward small recipients |
  | · of which 89 sponsor-years itemising <50% (suspected partial itemisation) | $0.81bn | 1.4 | Yes, spread pro rata |
  | Non-itemising sponsors (corrected DAFRC DAF grants) | $2.60bn | **4.4** | Mostly |
  | · BofA CGF / RCF / The Donors Fund / Stifel (raw: $1.04bn / $0.72bn / $0 / $0.05bn) | $0.97bn / $0.77bn / $0.55bn / $0.05bn | 4.0 | |
  | DAF-weighting haircut, net (corrections +2.3, haircut −2.9, Part IX line 2 +1.1) | $0.26bn | **0.4** | Mostly removed by re-weighting |
  | DAF-to-DAF residual (weighted DAF-to-DAF lines dropped − R5 netting) | $1.42bn | **2.4** | No (goes to panel sponsors) |
  | **Total** | **$8.81bn** | **15.1** | |

  So 5.4 points (foreign plus DAF-to-DAF) can never reach a frame recipient. The scaling credited them pro rata.
- **Replacement for the scaling [F/I].** Each component is put back into the recipient numerator with an explicit key. The DAF weight is first re-based on the same DAFRC figures as the denominator: w2 = min(1, corrected DAF grants ÷ (Part IX line 1 + line 3)). Committed frame, pooled:

  | Basis | Floor (no gap assigned) | **Bounded allocation, central** | Range over 8 allocation choices | 95% CI (central) | Pro rata per FY (residual-scaling equivalent) | ÷ 0.849 (wave 40B upper) |
  |---|---|---|---|---|---|---|
  | 1h | 8.4% | **9.2%** | 9.1–9.2% | 8.3–10.2% | 9.8% | 9.9% |
  | 1h − 1d − 1e | 12.6% | **13.7%** | 13.7–13.8% | 12.3–15.2% | 14.6% | 14.8% |

- **The range tightens [F/I].** Wave 40B gave 8.4–9.9% on 1h and 12.6–14.8% on 1h − 1d − 1e. The bounded allocation narrows that to **9.1–9.2%** and **13.7–13.8%** (point ranges over allocation choices). That grid varies only the keys, whose frame shares are all 0.68–0.69. The assumption envelope, from dropping the sub-$5,000 component (about 8.8% / 13.2%) to allocating the DAF-to-DAF residual (9.39% / 14.05%), is about 8.8–9.4% and 13.2–14.1%. That envelope, not 0.1 point, is the comparison with wave 40B's range [V wave 41B] The sampling interval (about ±1 point) now dominates. The effective scale factor is **1.09**, against 1/0.849 = 1.18; the gap adds about half of what the scaling assumed.
- **Expanded frame [F/I].** With the 70,008 recipients that get only non-top-50 grants, the central share is **8.0%** on 1h (8.0–8.1%; CI 7.3–9.1%), up from 7.3%, and **13.2%** on 1h − 1d − 1e (13.2–13.3%; CI 12.0–14.6%), up from 12.1%.
- **What the allocation choice does move: medians and small bands [F/I].** Pooled shares hardly depend on the key, because the small-gift key and the pro rata key send almost the same share of dollars to frame recipients (0.69 against 0.68 in FY2024). Medians do depend on it. The committed-frame median on 1h is **11.9%** with the small-gift key (CI 10.4–13.5%) and 10.2% pro rata, against the 9.3% floor. Pooled by revenue band (1h, committed): <$1m 23.3% (range 22.1–23.3%), $1–5m 14.3%, $5–25m 11.5%, $25–100m 7.8%, ≥$100m **4.7%** (4.7–4.8%). The floors are 20.5%, 12.7%, 10.7%, 7.3% and 4.4%.
- **Recommendation [I].** Report 9.2% (allocation range 9.1–9.2%, sampling CI 8.3–10.2%) on 1h and 13.7% (13.7–13.8%; 12.3–15.2%) on 1h − 1d − 1e for the committed frame, instead of the residual-scaled 9.9% / 14.8% or the 8.4–9.9% / 12.6–14.8% ranges. Keep the floor (8.4% / 12.6%) as the measured-only figure.

## 1. Method

### 1.1 Inputs
- **Unchanged from b40n1202-01.** The sponsor universe, return choice, line caches, totals-row drop, DAF-to-DAF annotation, weights, frames, samples, recipient returns and statistics all come from the b40n1202-01 helpers with the same seeds, read from caches only (`rcp/lines`, `q120201/lines`, `q1226/f990p8`, `q120201/f990p8`, BMF and IRS index). The floor reproduces b40n1202-01 exactly: 8.39% and 12.56% on the committed frame, 7.35% and 12.07% expanded; 84.92% coverage [F].
- **New: Part IX and Schedule F for every panel sponsor-year.** The script read the same chosen returns (3,097 FY2023–24 panel sponsor-years in the netpayout990 cache) from the GivingTuesday mirror of IRS TEOS. From each it took:
  - Part IX column A lines 1 (`GrantsToDomesticOrgsGrp`), 2 (`GrantsToDomesticIndividualsGrp`), 3 (`ForeignGrantsGrp`) and 25;
  - Schedule F Part II and Part III row sums;
  - Schedule I Part II row count and sum.

  All 3,097 returned status `ok` (new cache `q12011/p9`) [F]. Absent Part IX elements count as zero (190 returns have no line 1 element).
- **DAFRC figures.**
  - Raw DAF grants come from [dafrc-sponsor-schedule-d-fy2019-2024.csv](../../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv).
  - Corrected grants add the applied R1–R4 deltas in [dafrc-corrections-itemized.csv](../../data/mission-2026-11-14/dafrc-corrections-itemized.csv). Summed over the panel, these reproduce the corrected market totals ($54.83bn FY2023, $66.44bn FY2024) to the dollar [F].
  - Netted grants and R5 netting come from [dafrc-market-totals-netted.csv](../../data/mission-2026-11-14/dafrc-market-totals-netted.csv) (central tier).

### 1.2 Decomposition identity
For each itemising sponsor-year, with w the b40n1202-01 DAF weight, D and Dc the raw and corrected DAFRC DAF grants, L1–L3 the Part IX lines and SI the Schedule I lines (DAF-to-DAF and other):

Dc − w·SI_other = (Dc − D) + (D − w·(L1+L2+L3)) + w·L2 + w·L3 + w·(L1 − SI) + w·SI_d2d

- **Netted market.** The netted market is N = Σ Dc (all panel sponsors) − R5 netting. Therefore N − covered = Σ_itemising(the terms above) + Σ_non-itemising Dc − R5.
- **The DAF-to-DAF terms** are reported as one residual: Σ w·SI_d2d − R5.
- **Exactness.** The identity is exact. The unreconciled remainder is $0 in both years [F].

**Definitions of the four requested components**
- **Foreign grants.** w·L3, Part IX line 3, which Schedule F Parts II and III itemise. The cross-check: FY2024 raw L3 is $4.74bn and Schedule F Part II rows are $4.34bn; the difference is grants to foreign individuals (Part III) and sub-threshold amounts [F].
- **Non-itemised grants under $5,000.** w·(L1 − Schedule I total), as specified.
  - Of this, 29 sponsor-years are negative (Schedule I exceeds line 1; −$0.05bn in total). They are kept in the net.
  - **Split.** 89 sponsor-years itemise less than half of line 1. They hold $0.81bn of the $2.78bn, led by Blackbaud Giving Fund (line 1 $542m, Schedule I $41m), Omaha CF and Nevada CF. They are reported separately as suspected partial itemisation, because a shortfall of that size is unlikely to be all sub-$5,000 gifts.
- **Non-itemising sponsors.** The corrected DAF grants of panel sponsor-years with no itemised FY lines:
  - 25 attachment-only sponsor-years ($2.56bn);
  - 95 with no Schedule I lines ($0.03bn);
  - 5 with no cached return ($0.01bn).
- **DAF-weighting haircut.** Dc − w·(L1+L3) = corrections + (D − w·G) + w·L2. Part IX line 2 belongs here, because DAF grants cannot go to individuals: a pro rata weight that includes line 2 understates the DAF share of organisational grants.

### 1.3 Re-weighting (decomposition B)
- **The new weight.** w2 = min(1, Dc ÷ (L1 + L3)) puts numerator and denominator on the same DAFRC basis and leaves out line 2.
- **What it does.**
  - It removes the weighting haircut except for a cap residual: 63 sponsor-years where Dc > L1 + L3, $0.08bn in FY2024 [F].
  - It zeroes FY2024 sponsor-years that DAFRC records with no DAF grants, such as Campanile Foundation and Give2Asia. 129 sponsor-years carry the default weight; 122 itemising sponsor-years have zero corrected DAF grants, 99 of them at w = 1 [V wave 41B]
  - It raises sponsors whose cost-structure weight was near zero: UCLA Foundation (w 0 → 0.38, corrected DAF grants $170m), Stanford (0.105 → 0.947) and CF for Southeast Michigan (0 → 0.67).
- **Coverage on w2.** Itemised coverage becomes 85.3% (FY2024) and 87.2% (FY2023) [F].
- **This addresses P-B40N120201-02** (default weight of 1) with a filing-based rule.

### 1.4 Allocation to recipients
Each component's FY dollars are spread over recipient-years as USD × key(r, fy) ÷ total key(fy). The total includes blank-EIN and out-of-frame destinations, so only the in-frame share lands on sampled recipients.

| Key | Definition (DAF-weighted, positive, non-DAF-to-DAF Schedule I lines) | FY2024 total (w2) | Share to committed-frame EINs |
|---|---|---|---|
| `all` | All itemising sponsors' lines (the residual-scaling assumption) | $49.80bn | 0.679 |
| `top50` | Top-50 sponsors' lines | $39.56bn | 0.692 |
| `small10` | Lines under $10,000: the nearest observed analogue of sub-$5,000 gifts, which weights small recipients | $0.80bn | 0.694 |
| `small5` | Lines under $5,000 itemised voluntarily (sensitivity; tiny base) | $0.005bn | 0.755 |

**Rules [I]**
- **Never allocated.** Foreign grants, the DAF-to-DAF residual and the foreign share of non-itemising sponsors go to no recipient.
  - The DAF-to-DAF residual is grants that reach other panel sponsors. Those are excluded from the frame, and their onward grants are already counted.
- **Small gifts.** `small10` (central) or `all` (bound).
- **Partial itemisation.** Always `all`.
- **Weight-cap residual.** `all` (central) or none (bound).
- **Non-itemising sponsors.**
  - Their dollars are first cut to their domestic-organisation share, L1 ÷ (L1 + L3) from their own return. This is 99.7% in FY2024, because BofA CGF and RCF report almost no line 3.
  - That domestic part is then split like the full itemisers' line 1 dollars: 81.3% itemised-like, 3.2% small-gift-like and 15.4% DAF-to-DAF-like, which goes nowhere.
  - The itemised-like part uses `top50` (central; both are top-50 national sponsors) or `all`. The small-gift-like part uses `small10` or `all`.
- **Grid.** 2 (cap) × 2 (small-gift key) × 2 (non-itemiser keys) = 8 allocations. The bounds are the minimum and maximum pooled shares over the grid. The central case is `rw_capall_s10_ni50`.
- **Statistics.** Recipient statistics use the b40n1202-01 estimator (`summary_a`; weights N_h ÷ (n_h − xml_not_read)) with a 500-replicate stratified bootstrap for the floor, the residual-scaling equivalent, re-weighted-only and all 8 grid scenarios.

### 1.5 Robots and requests
- **Robots.** `gt990datalake-rawdata.s3.amazonaws.com/robots.txt` returned 404 at 2026-11-20 00:18 and 00:22 UTC, which places no restriction. Both checks are logged in scratchpad `q12011/robots/log.tsv`.
- **Requests.** 3,097 sponsor XML files were read with user agent `research-script/1.0`. No other host was contacted. sec.gov, crt.sh and certspotter were not used.

## 2. Results

### 2.1 Decomposition, both years and both weightings [F]

Points of netted DAF grants (central tier):

| Component | A: b40n1202-01 weights, FY2024 | A: FY2023 | B: re-weighted, FY2024 | B: FY2023 |
|---|---|---|---|---|
| Corrections R1–R4 (Dc − D) | 2.26 | 0.09 | — | — |
| DAF-weighting haircut (D − w·G) | −2.95 | −1.37 | — | — |
| Part IX line 2 (individuals) | 1.13 | 1.59 | — | — |
| Weight-cap residual | — | — | 0.13 | 0.29 |
| Foreign grants (line 3) | **3.01** | 2.96 | 2.99 | 2.92 |
| Non-itemised domestic (line 1 − Schedule I) | **4.76** | 3.37 | 4.74 | 3.31 |
| · full itemisers | (3.38) | | 3.38 | 2.95 |
| · partial itemisers | (1.38) | | 1.36 | 0.36 |
| Non-itemising sponsors | **4.44** | 4.10 | 4.44 | 4.10 |
| DAF-to-DAF residual | 2.42 | 2.16 | 2.43 | 2.19 |
| **Gap** | **15.08** | 12.89 | 14.74 | 12.80 |
| Coverage | 84.92% | 87.11% | 85.26% | 87.20% |

- **Net DAF-weighting haircut (A).** 2.26 − 2.95 + 1.13 = **+0.44** points.
  - The FY2024 corrections are large because R1 replaced 2,324 imputed DAFRC values with filed ones. The cost-structure weights already use filed values, so the corrections and the haircut mostly cancel.
- **Foreign, FY2024 [F].**
  - Top-50 sponsors account for $1.01bn of the $1.76bn and the others for $0.75bn.
  - The largest are National Philanthropic Trust ($411m), CAF America ($300m DAF-weighted), Silicon Valley CF ($147m), GS DAPF ($103m) and Fidelity Charitable ($72m).
- **Non-itemised domestic, FY2024 [F].**
  - Top-50 sponsors account for $1.25bn and the others for $1.53bn.
  - The largest are Blackbaud Giving Fund ($500m), Morgan Stanley GIFT ($408m: line 1 $1.63bn, Schedule I $1.22bn), DAFgiving360 ($197m), Foundation for the Carolinas ($175m), AOGF ($147m) and Fidelity Charitable ($106m, 0.8% of its line 1).
  - Only $6.7m of panel Schedule I lines are under $5,000, so the panel shows almost no small gifts directly.
- **Non-itemising sponsors, FY2024 [F].**
  - BofA CGF: raw $1.04bn, corrected $0.97bn; line 1 $0.97bn; no line 3.
  - RCF: raw $0.72bn, corrected $0.77bn; line 3 $0.09m.
  - The Donors Fund: raw $0, corrected $0.55bn (R1); line 1 $0.55bn.
  - Stifel Charitable: $0.05bn.
  - The task's $1.04bn and $0.72bn are the raw figures. The gap uses the corrected ones because the netted denominator does.
- **DAF-to-DAF residual [F/I].** The numerator drops $9.45bn of DAF-weighted DAF-to-DAF lines in FY2024. R5 (central) nets $8.03bn from the denominator. The $1.42bn difference is money that went to other panel sponsors and is not netted, for example grants into sponsors' non-DAF funds. R5 central weights each line by the recipient's DAF share of assets, while the numerator drops whole lines. Against the upper tier (weight 1, $9.42bn) the residual is about $0.03bn, so the 2.4 points is a netting-tier choice. It does not affect recipient shares, because it is never allocated [V wave 41B] It is the largest component that is neither foreign nor unitemised (P-B40N12020101-02).

### 2.2 Recipient DAF share: bounded allocation, all in-scope recipients

Pooled share with 95% bootstrap interval; median in the last columns. All figures are [F] on the stated allocation assumptions [I].

| Scenario | Committed 1h | Committed 1h − 1d − 1e | Expanded 1h | Expanded 1h − 1d − 1e | Median, committed 1h |
|---|---|---|---|---|---|
| Floor (b40n1202-01) | 8.39 (7.48–9.37) | 12.56 (11.33–14.09) | 7.35 (6.56–8.25) | 12.07 (10.86–13.46) | 9.32 |
| Re-weighted only (w2, nothing allocated) | 8.42 | 12.60 | 7.38 | 12.13 | 9.25 |
| **Central** (`rw_capall_s10_ni50`) | **9.16 (8.30–10.15)** | **13.71 (12.26–15.22)** | **8.05 (7.25–9.05)** | **13.23 (12.02–14.63)** | **11.88** (10.35–13.50) |
| Grid lower bound | 9.13 (`rw_cap0_s10_niall`) | 13.67 | 8.04 | 13.20 | 10.16 |
| Grid upper bound | 9.21 (`rw_capall_sall_ni50`) | 13.79 | 8.07 | 13.25 | 11.88 |
| Residual-scaling equivalent (whole gap pro rata, per FY) | 9.76 (8.67–10.81) | 14.62 (12.98–16.58) | 8.55 | 14.05 | 10.85 |
| b40n1202-01 residual scaling (pooled ÷ 0.849) [I] | 9.9 | 14.8 | 8.7 | 14.2 | — |

- **Interval reproduction.** The floor intervals differ slightly from b40n1202-01's (7.6–9.2%) because the bootstrap seed differs. The point estimates are identical.
- **Pro rata per FY against ÷ 0.849.** The per-FY pro rata figure (9.76%) is below 9.9% because FY2023 coverage is 87.1%, not 84.9%; the ÷ 0.849 shortcut applies FY2024 coverage to both years.
- **Grid lower and upper bounds of the expanded-frame 1h−1d−1e and median columns** come from different grid members. The CSV `bound` rows give each one.

**Contributions, committed 1h [F/I]**
- Small gifts alone (`only_sub5k_small10`): 8.77%.
- Non-itemising sponsors alone (`only_non_itemising_top50`): 8.79%.
- Together with the cap residual: 9.16%.

**Sensitivities, committed 1h (no bootstrap) [I]**
- Allocating the DAF-to-DAF residual pro rata as well: 9.39%. This is an outer bound that would double-count onward grants.
- The `small5` key: 9.15%. On the expanded frame it gives 8.28%, because voluntarily itemised sub-$5,000 lines go disproportionately to new-only recipients.

### 2.3 By revenue band, committed frame, 1h [F/I]

| Band | Floor | Central | Grid range | Residual-scaling equivalent | Central median |
|---|---|---|---|---|---|
| <$1m | 20.5 | **23.3** | 22.1–23.3 | 23.8 | 17.7 |
| $1–5m | 12.7 | **14.3** | 14.0–14.3 | 14.8 | 8.2 |
| $5–25m | 10.7 | **11.5** | 11.5–11.7 | 12.4 | 6.4 |
| $25–100m | 7.3 | **7.8** | 7.8–8.0 | 8.4 | 4.6 |
| ≥$100m | 4.4 | **4.7** | 4.7–4.8 | 5.1 | 1.9 |

- **The 1h − 1d − 1e basis, central:** 27.5%, 17.5%, 16.5%, 13.7% and **7.4%** (≥$100m; range 7.4–7.6%).
- **Expanded frame, 1h, central:** 20.7%, 12.1%, 10.0%, 7.0% and 4.0%.
- **Effect of the small-gift key.** It lifts the smallest band most: <$1m moves from 22.1% with the pro rata key to 23.3%. The largest bands sit at the bottom of their grid range.
- **Against Chariot.** Wave 34B found Chariot's 12.6% about twice the size-matched ≥$100m figure. That still holds: the bounded ≥$100m figure on 1h − 1d − 1e is 7.4%.

## 3. How this replaces the 1/0.849 scaling
- **What the scaling assumed.** It assumed that all 15.1 points reach frame recipients in the measured proportion.
- **What the allocation finds.**
  - 3.0 points are foreign and 2.4 points are DAF-to-DAF accounting.
  - Another 0.7 point is the foreign and DAF-to-DAF-like share of the non-itemising sponsors.
  - The re-weighting removes the net haircut.
  - What remains, 8.6 points of FY2024 netted grants, is allocated. It reaches frame EINs at about the itemised rate (0.68–0.69).
- **The result.** The effective scale factor is 1.09 rather than 1.18 (or 1.16 per FY), so 9.2% replaces 9.9%.
- **The remaining uncertainty is not the allocation key.** The pooled range over keys is 0.1 point. The open questions are:
  - whether the DAF-to-DAF residual is really non-recipient money (+0.2 point if not; P-B40N12020101-02);
  - the sampling error (±1 point);
  - the definitional limits carried over from b40n1202-01.

## 4. Limits
1. **Allocation keys are assumptions [I].**
   - `small10` treats sub-$5,000 gifts as distributed like $5,000–$9,999 lines. The panel itemises only $6.7m under $5,000, so the key cannot be checked against the panel itself (P-B40N12020101-05).
   - The key matters for medians (10.2–11.9%) and the smallest band, not for pooled shares.
2. **Partial itemisation.** The 50%-of-line-1 threshold is a rule of thumb. The 89 flagged sponsor-years ($0.81bn) are spread pro rata. If they are really attachment-only lists, the same pro rata treatment applies; if they are small gifts, the central figure is slightly low for small bands (P-B40N12020101-01).
3. **Part IX line 1 − Schedule I mixes several things.**
   - It includes timing differences between Part IX (accrual) and Schedule I.
   - It includes noncash valuation differences.
   - It includes Schedule I lines lost by the parser (b40n1202-01 found none: all line counts matched).
   - The 29 negative sponsor-years are netted in.
4. **The re-weighting uses DAFRC corrected DAF grants over Part IX lines 1 + 3.** A sponsor whose DAF grants go disproportionately to some recipients is still misallocated pro rata within its own lines. Where DAFRC records DAF grants but Part IX lines 1 and 3 are zero, the dollars sit in the cap residual. This applies to $0.25m in FY2024.
5. **The DAF-to-DAF residual's treatment depends on R5.** If R5 under-nets because of caps, the netted denominator is too high and all coverage figures are understated slightly.
6. **Carried over from b40n1202-01 (§4 there):**
   - blank-EIN lines (spread here like every key's other out-of-frame destinations);
   - non-panel DAF sponsors in the frame;
   - name-based exclusions;
   - timing and pledges;
   - EZ filers;
   - bootstrap intervals that cover sampling only.
7. **FY2023 and FY2024 are allocated with their own components.** Recipients matched on FY2023 get FY2023 gap dollars. The FY2023 gap is smaller (12.9 points).

## 5. Reproduction
```
S=<scratchpad>; Q=$S/q12011
python3 scripts/mission_coverage_gap.py . --np-cache $S/npcache --lines-cache-top50 $S/rcp/lines \
    --lines-cache $S/q120201/lines --bmf-dir $S/rcp/bmf --index-dir $S/irs --p8-cache $S/q1226/f990p8 \
    --p8-cache-new $S/q120201/f990p8 --p9-cache $Q/p9 [--fetch] [--boot 500]
```
- **First run.** `--fetch --fetch-only` read the 3,097 sponsor returns' Part IX and Schedule F in a few minutes (16 workers).
- **Cache-only run.** With 500 replicates it takes about 6 minutes.
- **Reproducibility.** Two cache-only runs produced byte-identical CSVs (md5 `6f8e65af…`).
- **stdout** is a JSON diagnostic:
  - the decomposition in USD and in points;
  - shares and splits;
  - key totals and frame shares;
  - the largest sponsors per component;
  - the non-itemising sponsors by status;
  - the headline for every scenario;
  - bounds.

## 6. Data dictionary: `coverage-gap-decomposition-2026-11-20.csv`

Shares are fractions. `row_type` decides which columns apply. Every row has `source`.

**`component` (52)**

| Column | Meaning |
|---|---|
| decomposition | `A` (b40n1202-01 weights), `B` (re-weighted w2) or `split` (shares used for non-itemising sponsors) |
| fiscal_year | 2023 or 2024 |
| component | A: `corrections_r1_r4`, `daf_weighting_haircut`, `individual_grants_l2`, `foreign_grants_l3`, `non_itemised_domestic_l1_minus_sched_i`, `non_itemising_sponsors`, `d2d_netting_residual`. B: `weight_cap_residual`, `foreign_grants_l3`, `sub5k_full_itemisers`, `sub5k_partial_itemisers`, `non_itemising_sponsors`, `d2d_netting_residual`. Both: `netted_daf_grants_central`, `covered_itemised_daf_weighted`, `gap`, `unreconciled`. split: `non_itemisers_domestic_share`, `itemisers_domestic_share`, `itemised_like`, `sub5k_like`, `d2d_like` (value in share_of_netted) |
| usd | USD |
| share_of_netted | usd ÷ netted DAF grants of that FY (points ÷ 100) |
| share_of_gap | usd ÷ gap of that decomposition and FY |

**`bound` (24):** one per frame × basis × scope (all, five revenue bands).

| Column | Meaning |
|---|---|
| frame, basis, scope_type, scope | As in the recipient-share rows |
| scenario | The central scenario (`rw_capall_s10_ni50`) |
| pooled_share, median_share | Central values |
| bound_lower_pooled / bound_lower_scenario | Lowest pooled share over the 8-scenario grid, and the scenario that gives it |
| bound_upper_pooled / bound_upper_scenario | Highest pooled share over the grid, and its scenario |
| bound_lower_ci95, bound_upper_ci95 | 2.5th percentile of the lowest scenario and 97.5th of the highest (all-scope rows only) |
| median_lower, median_upper | Lowest and highest median over the grid |

**`recipient_share` (360):** 15 scenarios × 2 frames × 2 bases × 6 scopes.

| Column | Meaning |
|---|---|
| scenario | `measured_floor`, `residual_scaling_equivalent`, `reweighted_only`, the eight `rw_{cap0\|capall}_{s10\|sall}_{ni50\|niall}`, `only_sub5k_small10`, `only_non_itemising_top50`, `sens_plus_d2d_residual_all`, `sens_small5_key` |
| frame | `committed` or `expanded` |
| basis | `b1_1h` or `b3_1abcf` (1h − 1d − 1e) |
| scope_type / scope | `all`/`all_ex_excluded` or `revenue_band`/`a_lt_1m` … `e_ge_100m` |
| respondents, weighted_recipients | As in b40n1202-01 |
| median_share, pooled_share | Weighted median and ratio estimator |
| *_ci95_lo / *_hi | 500-replicate stratified bootstrap (all-scope rows of the floor, residual, re-weighted-only and grid scenarios; blank otherwise) |
| implied_scaling_factor | pooled_share ÷ floor pooled_share for the same frame, basis and scope |

**`allocation` (58)**

| Column | Meaning |
|---|---|
| scenario, decomposition, fiscal_year | Scenario, the decomposition it draws on, and the FY |
| key | `all`, `top50`, `small10` or `small5` |
| allocated_usd | Dollars spread by that key |
| share_of_netted | allocated_usd ÷ netted DAF grants of that FY |
| key_share_to_committed_frame | Share of the key's dollars held by committed-frame EINs |

**`sponsor_itemised` (2,705)**

| Column | Meaning |
|---|---|
| ein, sponsor_name, tier, fiscal_year, status | Sponsor-year identity; status is `itemised` |
| w, w2 | b40n1202-01 weight; re-weighted DAF share |
| d_raw, d_corr | DAFRC raw and corrected DAF grants |
| l1, l2, l3 | Part IX lines 1–3, column A |
| si_non_d2d, si_d2d | Schedule I Part II, other lines and DAF-to-DAF lines |
| sf_org_usd | Schedule F Part II row sum |
| si_lines_lt5k_non_d2d | Schedule I lines under $5,000 (non-DAF-to-DAF) |
| A_* | Decomposition A terms in USD (`A_d2d_lines` = w·SI_d2d; `A_covered` = w·SI_other) |
| B_* | Decomposition B terms in USD |
| partial | Schedule I < 50% of line 1 |
| p9_status | Part IX extract status |

**`sponsor_non_itemising` (255):** FY2023–24 panel sponsor-years with non-zero corrected DAF grants and no itemised lines.

| Column | Meaning |
|---|---|
| status | `not_itemised` (attachment), `no_sched_i_lines` or `not_in_cache` |
| d_raw, d_corr | DAFRC raw and corrected DAF grants |
| w | Cost-structure weight where present |
| l1, l2, l3, sf_org_usd | From the return where cached |
| dom_share | L1 ÷ (L1 + L3) |

## 7. Source register

| ID | Source | URL | Accessed / version | Use |
|---|---|---|---|---|
| S1 | IRS Form 990 e-file XML, GivingTuesday mirror of IRS TEOS | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml | 2026-11-20 (robots.txt 404) | Part IX lines 1–3 and 25, Schedule F Parts II–III, Schedule I Part II sums for 3,097 sponsor-years |
| S2 | IRS Instructions for Form 990 (Part IX lines 1–3) and Schedule F / Schedule I instructions | https://www.irs.gov/instructions/i990 ; https://www.irs.gov/pub/irs-pdf/i990sf.pdf ; https://www.irs.gov/pub/irs-pdf/i990si.pdf | Current editions | Line definitions; Schedule I $5,000-per-recipient threshold; Schedule F foreign grants |
| S3 | IRS TEOS e-file index | https://apps.irs.gov/pub/epostcard/990/xml/2024/index_2024.csv (and 2023, 2025, 2026) | Cached 2026-11-14/15 | Recipient returns (via b40n1202-01 helpers) |
| S4 | IRS EO Business Master File | https://www.irs.gov/pub/irs-soi/eo1.csv (eo1–eo4, eo_pr, eo_xx) | Cached; Last-Modified 2026-11-09 | Frames, bands, exclusions |
| S5 | DAFRC Annual DAF Report 2025 updated dataset (repo copy) | https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx ; [dafrc-sponsor-schedule-d-fy2019-2024.csv](../../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv) | Repo | Panel; raw DAF grants per sponsor |
| S6 | Repo corrections and netted totals | [dafrc-corrections-itemized.csv](../../data/mission-2026-11-14/dafrc-corrections-itemized.csv); [dafrc-market-totals-netted.csv](../../data/mission-2026-11-14/dafrc-market-totals-netted.csv) | Repo | Corrected DAF grants; R5 netting; netted totals |
| S7 | Repo weights and whitelist | [sponsor-cost-structure.csv](../../data/mission-2026-11-14/sponsor-cost-structure.csv); [daf-to-daf-recipient-whitelist.csv](../../data/mission-2026-11-14/daf-to-daf-recipient-whitelist.csv) | Repo | b40n1202-01 weights; DAF-to-DAF lines |
| S8 | Prior studies and validation | [b40n1202-01-non-top50-numerator.md](b40n1202-01-non-top50-numerator.md); [validation-wave40b-report.md](validation-wave40b-report.md); [b40n1202-b43n26-recipient-basis-and-rating-eligibility.md](b40n1202-b43n26-recipient-basis-and-rating-eligibility.md) | Repo | Method, floor, 8.4–9.9% / 12.6–14.8% range, Chariot comparison |
