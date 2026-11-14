# AI economics v2: the 16-process model re-anchored to observed sponsor costs

*Queue item P-COST-06, plus related items P-COST-01 and P-COST-02 as context. Prepared 2026-11-14.*

- **Rebuilds:** the scenario model in [ai-economics-replacement-analysis.md](ai-economics-replacement-analysis.md) ("v1"), including its governing sections "Red-team corrections (wave 2A)" and "Update from observed cost data".
- **Observed inputs:** [sponsor-cost-structure-and-sensitivities.md](sponsor-cost-structure-and-sensitivities.md) and its CSVs.
- **Script:** `scripts/mission_ai_economics_v2.py` (stdlib only, functional style, seeded `random.Random(42)`).
- **Output:** `data/mission-2026-11-14/ai-economics-v2-results.csv` (8,078 rows).
- **Queue proposals:** `data/mission-2026-11-14/queue-proposals-ai-econ-v2.csv`.

**Notation.**
- **[F]** filed or published fact.
- **[C]** computed only from observed data.
- **[S]** scenario output. It depends on at least one assumption in §3.2, so it describes the model, not the world.
- **[I]** inference.

**v2 does not observe process costs.** It replaces v1's invented totals with observed Part IX totals. The way those totals divide into processes, and how each intervention performs, are still assumed. Every probability below is a probability **under the stated assumption distributions**. None is a measured likelihood.

---

## 1. Bottom line

1. **The gross ranking from v1 survives, and so does C's weak position. Both are still assumption-driven.**
   - [S] For each of the 16 processes, the intervention most likely to rank first by gross capture is the one v1 ranked first. The probability ranges from 0.44 (P03, manual improvement A) to 0.94 (P06, redesign D).
   - [S] C (AI on the existing workflow) ranks first by gross in at most 17% of draws in any process or archetype (P07 0.15–0.17, P03 0.14–0.16). It is less than 1% in 9 processes.
   - [S] v1's "C ranks last in all 16" does **not** survive. C is last in 39–96% of draws, and in fewer than half of draws for P03 (0.48) and P07 (0.41).
   - Gross rankings barely differ between archetypes (no cell differs by more than 0.10), because gross capture is proportional to the pool (§4.2). They are set by the assumed d, b, β, a and s, not by the observed costs.
2. **Anchoring to Part IX makes pools much larger per grant at small sponsors and somewhat larger at large ones.** Medians [S]:
   - Large nationals: **$7.9 per grant**, against v1's $4.32.
   - Mid nationals: **$37 per grant**.
   - Community foundations with $1bn and $250m of DAF assets: **$180–186 per grant**.
   - Community foundations with $10–100m: **$323 per grant**.
   - v1's linear scaling would have put the $250m community-foundation pool at about **$10k a year**. The anchored median is about **$446k**, 44 times higher. The v1 pool scaled by elasticity is still only about $27k. Observed cost per grant does not follow a single grant-volume curve; it differs by business model ([cost-structure §4.4, §4.6](sponsor-cost-structure-and-sensitivities.md)).
3. **Per-process business cases survive only at large-national scale. Below that, the observed IT budgets make even the cheapest intervention marginal.**
   - [S] At a large national (1–3M grants), C clears its own fixed cost in **59%** of draws for P07, **29%** for P11, **32%** for P16 and **18%** for P03. It clears in 15% or fewer for every other process.
   - [S] At a mid national, or at any community foundation, C clears its fixed cost in **5% or fewer of draws in every process**.
   - [S] At community foundations under $250m of DAF assets, the most likely net "winner" is **do nothing** in 87–100% of draws for every process.
   - [C+S] One AI project's assumed fixed cost ($150k–$750k) is a median **5.4×** the observed median IT line at a $10–100m community foundation. It is **1.3×** at $250m, and the project exceeds the whole IT line in 67% of draws ([IT medians: cost-structure §4.2](sponsor-cost-structure-and-sensitivities.md)).
4. **"AI pays as a shared platform" survives only if the network includes large sponsors. That shrinks the addressable market for network-scale AI.** [S] A vendor's platform breaks even at a median of:
   - about **8** large-national equivalents (only 5 nationals over $10bn exist);
   - about **59** mid-national or $1bn community-foundation equivalents (10 and 20 exist in those windows);
   - about **236** community foundations at $250m, and break-even is finite in only 24% of draws (58 exist).

   On the **observed FY2024 population**, with the vendor signing the most valuable sponsors first, break-even is reachable in:
   - **43%** of draws with all community foundations and standard nationals;
   - **26%** without the five giants;
   - **0.4%** with community foundations under $250m only.
5. **The largest remaining unknowns are now different. In order of influence on conclusions (§6):**
   - φ, the share of labour cost that is process handling. It sets pool size and platform break-even.
   - d and β, the redesign and conventional-automation shares. They set the gross ranking.
   - a and s, AI amenability and time saving. They matter only in P03, P07 and, weakly, P11, P13 and P14.
   - Fixed costs, which set the net ranking.

   The QA rate q, which v1 called "the single most important AI parameter" before the red-team correction, moves aggregate rankings by at most 2–3 points.

---

## 2. What v2 changes in the method

| v1 (governing text in [v1 §2](ai-economics-replacement-analysis.md)) | v2 |
|---|---|
| One illustrative sponsor with 1M grants. Pools built bottom-up as V × e × m × rate, then scaled linearly to other sizes | **Five archetypes** built by bootstrapping real FY2024 Part IX rows (§3.1), plus a v1 reference archetype for comparison |
| Pool totals invented ($4.32m base) | Pool = **observed DAF-allocated operating cost** × **observed labour share** (Part IX staff lines 5–10 plus outside services excluding 11f) × **assumed φ**. It is split across P01–P15 using v1's process mix, with e and m sampled |
| Linear scaling with grant volume | **Elasticity scaling** from each bootstrapped sponsor to the archetype's size. Nationals use ε 0.41–0.48 on DAF assets, applied to grants as a proxy; community foundations use 0.84–0.86 on total assets ([cost-structure §4.6](sponsor-cost-structure-and-sensitivities.md)). IT scales at 0.44 and 0.83 |
| Point values with optimistic and pessimistic cases | **Monte Carlo** of 10,000 draws over every unsourced parameter (§3.2). Parameter draws are common to all archetypes, so differences between archetypes come only from the cost anchors |
| Gross capture only. Fixed-cost ranges compared informally | Gross **and net** (gross minus a per-process fixed cost), with "none" as a fifth option. Fixed cost is also expressed as a multiple of the archetype's **observed median IT spend** |
| "AI pays as a shared platform" stated, not modelled | **Platform break-even**: number of homogeneous sponsors, and a greedy build-out over the observed FY2024 population |
| P16 (recipient side) at 1M grants received | Still v1's bottom-up pool, scaled **linearly** with the archetype's grants. It has no observed anchor; see proposal P-AIV2-06 |

The core formulas are unchanged from v1, so the two versions are comparable:
- A = α·L
- B = β·b·L
- C = s·a·L − 0.5·q·L − inference
- D = d·L
- Inference = cases × tokens × Sonnet 5.5 list price × 3 ([Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing), via v1)

The script recomputes v1's 64 base gross values to within $1 of rounding (`record_type=meta`).

---

## 3. Which inputs are observed and which remain assumptions

### 3.1 Observed (FY2024 Part IX unless stated; `sponsor-cost-structure.csv`)

| Archetype | Bootstrap pool | Observed anchors used |
|---|---|---|
| **NAT_LARGE**: national, 1–3M grants | 2 grant-count anchors | **Fidelity Charitable**: $203.1m operating cost at 3.0M grants, **$67.70 per grant**, labour share 0.895 ([2026 Giving Report](https://www.fidelitycharitable.org/insights/2026-giving-report.html); [FY2025 990 XML via cost-structure CSV](sponsor-cost-structure-and-sensitivities.md)). **DAFgiving360**: $87.4m at 1.6M grants, **$54.59 per grant**, labour share 0.517 ([FY2026 release](https://www.dafgiving360.org/press-release/fiscal-year-2026-results)). IT hurdle: median line 14 among nationals over $10bn with IT > 0, **$8.99m** ($3.65m including Fidelity's $0) |
| **NAT_MID**: national, $1–10bn DAF assets | 10 sponsors | Median operating cost $16.5m; IT > 0 median **$533k** (n = 5) |
| **CF_1BN**: community foundation, $1bn | 20 sponsors at $0.5–2bn, scaled to $1bn | IT > 0 median $694k, scaled to **$913k** |
| **CF_250M**: community foundation, $250m | 58 sponsors at $125–500m, scaled to $250m | IT > 0 median **$255k** |
| **CF_SMALL**: community foundation, $10–100m | 268 sponsors, used as filed | IT > 0 median **$62k** |

- DAF allocation for community foundations is drawn at random as either the assets basis (A) or the grants basis (G), both observed per row.
- v1's pool implies φ = **0.07** at Fidelity and **0.15** at DAFgiving360 (`record_type=grant_anchor`). v1's invented total therefore sits inside the φ range used below, but it is not evidence for any value in that range.

### 3.2 Still assumptions (all in `record_type=assumption`)

| Parameter | Distribution | Comment |
|---|---|---|
| s, AI time saving | triangular(0.15, 0.40, 0.70), one draw per iteration | v1 used 0.20 / 0.40 / 0.60 |
| q, QA re-review share | triangular(0.03, 0.10, 0.30) | v1 used 0.05 / 0.10 / 0.25 |
| a_p, AI-amenability | triangular(0.5a₁, a₁, min(0.9, a₁ + 0.35)) | Right-skewed to remove v1's cap at 0.45, which forced C below A (red-team #1) |
| d_p, redesign share | triangular(0.3d₁, d₁, min(0.95, d₁ + 0.10)) | Multiplied by adoption ~U(0.3, 1) for P07, P09, P10 and P16 |
| α, manual saving | U(0.05, 0.25) | v1 fixed it at 0.15 |
| β, conventional efficiency, and b_p | β ~ U(0.3, 0.7); b_p ~ triangular(0.7b₁, b₁, min(0.95, 1.2b₁)) | v1 fixed β at 0.5 |
| **φ**, process share of labour cost | triangular(0.05, 0.15, 0.35) | The main remaining scale assumption |
| e_p, m_p | triangular(v1 low, base, high) | Now set only the process **mix** |
| Fixed costs per process project | Log-uniform over v1's ranges: A $25–100k, B $100–500k, C $150–750k, D $0.2–2m | Same in every archetype |
| Average grant size (non-NAT_LARGE) | Log-uniform $5–40k | Bounded by observed anchors: Fidelity about $5.1k, DAFgiving360 $5.5k, Vanguard $11.4k, NPT $40k. Only affects inference cost |
| Platform cost | $1.5–6m a year | |
| Per-sponsor vendor cost | $10–100k a year | |
| Vendor fee share τ | U(0.2, 0.5) | |

What the elasticity scaling covers, and what it does not:
- Applying the national asset elasticity to grant volume treats grants as proportional to assets. That is an approximation.
- The community-foundation elasticity is measured on whole-organisation cost against total assets.

---

## 4. Results

### 4.1 Pools (`record_type=archetype_anchor`) [S]

| Archetype | Grants/yr (p50) | P01–P15 pool p50 (p5–p95 in CSV) | Pool per grant p50 | v1 linear at the same grants | v1 × elasticity | Inference share of pool |
|---|---:|---:|---:|---:|---:|---:|
| NAT_LARGE | 1.73M | $13.7m | $7.9 | $7.5m | $5.5m | 1.2% |
| NAT_MID | 40k | $1.60m | $37 | $0.17m | $1.04m | 0.2% |
| CF_1BN | 9.9k | $1.77m | $180 | $43k | $90k | 0.05% |
| CF_250M | 2.3k | $446k | $186 | $10k | $27k | 0.05% |
| CF_SMALL | 210 | $65k | $323 | $0.9k | $3.5k | 0.03% |
| REF_V1_1M | 1.0M | $5.8m | $5.8 | $4.3m | $4.3m | 1.6% |

The REF_V1_1M median sits above v1's $4.32m because the triangular e and m ranges are right-skewed.

**[I]** v1's finding that inference is immaterial survives: inference is at most 1–2% of the pool at nationals. The finding is not sensitive to model choice.

### 4.2 Probability each intervention ranks first (`record_type=process_intervention`) [S]

The gross column is shown for NAT_LARGE. The other archetypes differ by at most 0.10 per cell, because gross capture is proportional to the pool. The net columns show the most likely winner, with "none" meaning no intervention clears its fixed cost, followed by P(C first by net).

| Process | v1 base rank | P(first, gross): A / B / C / D | P(C last, gross) | Net: NAT_LARGE | Net: NAT_MID | Net: CF_1BN | Net: CF_250M | Net: CF_SMALL |
|---|---|---|---:|---|---|---|---|---|
| P01 KYC | B>D>A>C | .02 / **.57** / .00 / .41 | .79 | none .80 | none 1.0 | none 1.0 | none 1.0 | none 1.0 |
| P02 Cash/securities intake | D>B>A>C | .00 / .26 / .00 / **.73** | .90 | none .82 | none 1.0 | none 1.0 | none 1.0 | none 1.0 |
| P03 Complex assets | A>D>B>C | **.44** / .03 / .15 / .38 | .48 | A .85 (C .04) | none .79 | none .76 | none .99 | none 1.0 |
| P04 Rebalancing | B>D>A>C | .00 / **.83** / .00 / .17 | .96 | none 1.0 | none 1.0 | none 1.0 | none 1.0 | none 1.0 |
| P05 Recommendation intake | D>B>A>C | .00 / .16 / .00 / **.84** | .84 | A .41 | none .97 | none .96 | none 1.0 | none 1.0 |
| P06 Routine eligibility | D>B>A>C | .00 / .06 / .00 / **.94** | .89 | none .34 (A .25, B .22, D .19) | none .97 | none .96 | none 1.0 | none 1.0 |
| P07 Non-standard due diligence | D>A>B>C | .20 / .04 / .16 / **.60** | .41 | A .58 (C .11) | A .50 | A .59 | none .87 | none 1.0 |
| P08 Benefit review | D>B>A>C | .07 / .17 / .01 / **.76** | .86 | A .59 | none .75 | none .71 | none .98 | none 1.0 |
| P09 Disbursement | D>B>A>C | .00 / .35 / .00 / **.64** | .96 | A .36 | none .97 | none .96 | none 1.0 | none 1.0 |
| P10 Returned checks | D>B>A>C | .01 / .12 / .00 / **.86** | .78 | A .43 | none .83 | none .81 | none .99 | none 1.0 |
| P11 Service inquiries | D>A>B>C | .03 / .01 / .03 / **.93** | .52 | A .58 (C .04) | none .74 | none .70 | none .99 | none 1.0 |
| P12 Receipts | B>D>A>C | .00 / **.61** / .00 / .38 | .93 | none .92 | none 1.0 | none 1.0 | none 1.0 | none 1.0 |
| P13 Succession | D>A>B>C | .09 / .04 / .03 / **.84** | .64 | A .62 | none .97 | none .95 | none 1.0 | none 1.0 |
| P14 Fraud/AML alerts | B>D>A>C | .10 / **.65** / .04 / .21 | .67 | A .50 | none .95 | none .94 | none 1.0 | none 1.0 |
| P15 Schedule D data | D>B>A>C | .00 / .47 / .00 / **.52** | .90 | none .59 | none 1.0 | none .99 | none 1.0 | none 1.0 |
| P16 Recipient attribution (linear, unanchored) | D>B>A>C | .01 / .15 / .02 / **.82** | .65 | D .37 | none .96 | none 1.0 | none 1.0 | none 1.0 |

**How to read the net columns.** A wins net at large nationals because it is *assumed* to be the cheapest to implement ($25–100k). The net ranking measures the fixed-cost assumptions as much as the processes. D's high gross value is offset by its assumed $0.2–2m fixed cost and, in P07, P09, P10 and P16, by the adoption haircut.

### 4.3 Net-value distributions (selected; full p5 / p25 / p50 / p75 / p95 / mean in the CSV) [S]

| Archetype, process | A: p5 / p50 / p95 (P > 0) | C: p5 / p50 / p95 (P > 0) | D: p5 / p50 / p95 (P > 0) |
|---|---|---|---|
| NAT_LARGE P07 (pool p50 $4.0m) | $68k / $499k / $2.25m (.99) | −$486k / $99k / $1.91m (.59) | −$1.19m / $148k / $2.75m (.58) |
| NAT_LARGE P11 (pool $1.7m) | $0 / $183k / $902k (.95) | −$571k / −$148k / $589k (.29) | −$1.28m / −$60k / $1.39m (.46) |
| CF_1BN P07 (pool $501k) | −$55k / $18k / $244k (.62) | −$631k / −$257k / $3k (.05) | −$1.67m / −$508k / −$10k (.05) |
| REF_V1_1M P07 (pool $1.7m) | $12k / $179k / $587k (.97) | −$555k / −$140k / $336k (.27) | −$1.45m / −$281k / $451k (.26) |

### 4.4 Fixed-cost hurdle against observed IT budgets (`fixed_cost_over_it_median_*`) [C+S]

The numerator is an assumed fixed cost; the denominator is observed IT spend. Values are the median multiple, with P(a single project exceeds the whole annual IT line) in brackets.

| Archetype | A | B | C | D |
|---|---|---|---|---|
| NAT_LARGE (IT $9.0m) | 0.01 (0) | 0.02 (0) | 0.04 (0) | 0.07 (0) |
| NAT_MID (IT $533k) | 0.09 (0) | 0.41 (0) | 0.63 (0.21) | 1.20 (0.58) |
| CF_1BN (IT $913k scaled) | 0.05 (0) | 0.24 (0) | 0.37 (0) | 0.70 (0.34) |
| CF_250M (IT $255k) | 0.20 (0) | 0.86 (0.41) | **1.31 (0.67)** | 2.52 (0.90) |
| CF_SMALL (IT $62k) | 0.81 (0.35) | 3.6 (1.0) | **5.4 (1.0)** | 10.4 (1.0) |

The governing v1 update ("the $150k–$750k AI fixed-cost hurdle is prohibitive below about $250m of DAF assets") is **confirmed and refined**:
- The boundary sits at about $250m.
- At $250m, a C project exceeds the whole IT line in two-thirds of draws.
- At $1bn, it uses about a third of the IT line.

### 4.5 Shared vendor AI platform (`record_type=platform`, `platform_network`) [S]

Sponsor AI value is the sum of positive C gross across P01–P15. "After redesign" applies C only to the (1 − d) residual.

| Archetype | Sponsor AI value p50 (p25–p75) | P(self-built platform pays) | Vendor break-even N, p50 among finite (p10–p90) | P(finite) | Sponsors available | P(break-even ≤ available) |
|---|---|---|---|---|---|---|
| NAT_LARGE | $1.18m ($0.56–2.38m) | 0.20 | 8 (2–46) | 0.95 | 5 | 0.34 |
| NAT_MID | $131k ($44–289k) | 0.00 | 59 (16–410) | 0.57 | 10 | 0.02 |
| CF_1BN | $164k ($82–315k) | 0.00 | 59 (15–396) | 0.66 | 20 | 0.12 |
| CF_250M | $42k ($21–76k) | 0.00 | 236 (60–1,717) | 0.24 | 58 | 0.02 |
| CF_SMALL | $5.9k ($2.6–13k) | 0.00 | 626 (151–4,228) | 0.02 | 268 | 0.005 |
| REF_V1_1M | $515k | 0.00 | 21 (8–95) | 0.91 | – | – |

- **Break-even in grant volume.** The p50 break-even network is about **14M grants a year** of NAT_LARGE-type sponsors. That is nearly three times the combined self-reported volume of Fidelity Charitable, DAFgiving360, Vanguard Charitable and NPT (about 5M). For CF_1BN-type sponsors it is about **0.64M grants a year**. In the CSV these are `vendor_breakeven_grants_*`.
- **After redesign**, every break-even rises by 25–45% and P(finite) falls. If redesign happens first, there is less AI work left to sell.
- **Observed-population build-out.** A vendor signs sponsors in descending order of value until marginal sponsors lose money, using 2,000 draws.

  | Segment | Sponsors (FY2024) | P(reachable) | N at break-even (p50) |
  |---|---:|---:|---:|
  | CF < $250m | 741 | 0.004 | 51 |
  | All CF | 794 | 0.16 | 16 |
  | Nationals < $10bn | 71 | 0.035 | 8 |
  | CF + nationals < $10bn | 865 | 0.26 | 16 |
  | CF + all nationals | 870 | 0.43 | 7 |

---

## 5. What survives from v1 and what flips

| v1 statement (as governed by red-team and the cost update) | v2 verdict | Evidence |
|---|---|---|
| Inference cost is not the constraint (<1% of labour displaced) | **Survives.** It is ≤ 1.6% of the pool in every archetype | §4.1 [S] |
| D or B usually beats C; C ranks last in all 16 processes at base | **Partly survives.** The modal gross winner matches v1 in 16 of 16 processes. C is first in ≤ 17% of draws, but it is *not* reliably last: P(C last) is 0.41 for P07 and 0.48 for P03 | §4.2 [S] |
| C ranks first only for P03 under optimistic AI assumptions | **Refined.** P03 and P07 are the two processes where C can rank first (0.33–0.35 in the top tercile of a or s). P11, P13 and P14 reach 0.08–0.11 | §6 [S] |
| P07: B and C tied (red-team #3) | **Superseded.** With widened parameters C beats B in 51% of P07 draws, a coin flip, and both trail D and A on gross | `p_C_beats_B_gross` [S] |
| Ranking is invariant to pool size (a consequence of linear scaling) | **Holds for gross. Flips for net.** With fixed costs, scale decides whether any intervention is worth doing: "none" is first in 41% of process-draws at NAT_LARGE (0–100% by process) but in 87–100% of draws for every process at CF_250M and below | §4.2 [S] |
| $4.32m base pool at 1M grants is "consistent" with observed cost | **Survives, but anchoring gives about 1.8× per grant at large nationals** ($7.9 against $4.32). The gap is driven by φ (assumed) and Fidelity's 0.895 labour share (observed, mostly line 11a) | §3.1, §4.1 |
| Linear scaling (×3 for Fidelity, ×0.16 for NPT) | **Refuted, as the cost update already noted.** Anchored pools per grant run from $7.9 to $323, a 40× spread | §4.1 [C+S] |
| Per-process AI cases fail at sub-Fidelity scale | **Survives and sharpens.** P(C net > 0) is ≤ 5% everywhere below NAT_LARGE. At NAT_LARGE it is 59% for P07 | §4.3 [S] |
| $150–750k AI hurdle prohibitive below about $250m | **Confirmed.** The C cost exceeds the whole IT line in 67% of draws at $250m and in 100% at $10–100m | §4.4 [C+S] |
| AI pays as a shared platform; this favours vendors serving many sponsors | **Partly flips.** A platform pays when the network includes large sponsors. A network of small community foundations does not break even on sponsor-side process savings (P(reachable) 0.4% for CFs under $250m) | §4.5 [S] |
| QA intensity decides whether AI value is positive (red-team #2) | **Survives in direction, small in magnitude.** Moving q from its bottom to its top tercile shifts C-first shares by only 1–3 points in aggregate | §6 [S] |

---

## 6. Sensitivity of rankings (`record_type=sensitivity`, `sensitivity_process`) [S]

Values are shares of (draw, process) pairs across P01–P15 where each intervention ranks first, in the bottom versus top tercile of each parameter. The results are near-identical across archetypes for gross; NAT_LARGE is shown for net.

| Parameter | Gross: D first (low → high) | Gross: B first | Gross: C first | Net (NAT_LARGE): "none" | Net: A first |
|---|---|---|---|---|---|
| d (redesign) | **0.36 → 0.81** | 0.47 → 0.15 | 0.05 → 0.01 | 0.41 → 0.40 | 0.42 → 0.36 |
| β (conventional) | 0.77 → 0.46 | **0.12 → 0.47** | 0.03 → 0.02 | 0.41 → 0.40 | 0.44 → 0.34 |
| α (manual) | 0.65 → 0.56 | 0.31 → 0.27 | 0.04 → 0.02 | **0.50 → 0.32** | **0.20 → 0.56** |
| a (AI-amenability) | 0.63 → 0.59 | 0.29 → 0.29 | **0.00 → 0.07** | 0.41 → 0.41 | 0.40 → 0.38 |
| s (AI time saving) | 0.62 → 0.60 | 0.30 → 0.28 | **0.00 → 0.07** | 0.41 → 0.41 | 0.40 → 0.38 |
| q (QA) | 0.60 → 0.62 | 0.29 → 0.30 | 0.04 → 0.02 | 0.40 → 0.41 | 0.39 → 0.39 |
| φ (process labour share) | 0.61 → 0.61 | 0.29 → 0.30 | 0.03 → 0.03 | **0.51 → 0.31** | 0.36 → 0.40 |
| C fixed cost | unchanged | unchanged | unchanged | 0.41 → 0.40 | 0.38 → 0.40 |

**Per process: C first by gross, bottom → top tercile of a.** The pattern is nearly the same for s.
- P07: 0.03 → 0.32
- P03: 0.02 → 0.33
- P14: 0.00 → 0.11
- P13: 0.00 → 0.09
- P11: 0.00 → 0.08
- In every tercile of a, s or d, P(C first) stays below 0.01 for 8 processes: P02, P04, P05, P06, P09, P10, P12 and P15.

**[I]** Measured AI performance can change the ranking only for document-heavy, judgment-heavy work (P03, P07). For the rule-friendly processes no plausible AI result changes it. Measuring d (redesign and adoption) and φ (process share of cost) would change more conclusions than any AI benchmark.

---

## 7. Implications for the entrant strategy (vendor or network-scale AI)

These are [I] readings of [S] outputs. They build on [ai-native-entrant-simulation.md](ai-native-entrant-simulation.md) (Strategy 3, "AI-native operating layer", base price $120k a year, a SCENARIO) and [entry-strategy-comparison.csv](../../data/mission-2026-11-14/entry-strategy-comparison.csv).

1. **The buyers whose savings could fund a $120k-a-year product are national sponsors with $1bn or more and community foundations with about $1bn or more of DAF assets.**
   - Median sponsor-side AI gross value is $131k (mid national) and $164k (CF_1BN). At a fee share of 0.2–0.5 that supports roughly $26–82k of fees.
   - At CF_250M the median is $42k, and the p95 is $162k.
   - **[I]** Under these assumptions, Strategy 3 cannot be priced on AI process savings for the roughly 740 community foundations under $250m. This agrees with the simulation's own warning that "S3 must be priced and scoped on the whole operating burden" ([ai-native-entrant-simulation.md §5](ai-native-entrant-simulation.md)).
2. **The five giants decide whether network-scale AI pays.** P(break-even is reachable) on the observed population falls from 0.43 to 0.26 without them. The giants are also the only archetype where a self-built platform pays in more than 10% of draws (0.20). Their labour sits largely with affiliated administrators, for example Fidelity's $139.7m in line 11a ([cost-structure §1.3](sponsor-cost-structure-and-sensitivities.md)). **[I]** An entrant's realistic AI customer at scale is an *administrator or platform vendor* (Ren, TIFIN Give, Foundation Source) embedding the capability, not a sponsor. This is consistent with v1 §4.4 and the cost update, but it is now conditional on landing large clients.
3. **Small-sponsor value has to come from somewhere other than sponsor-side AI.** Candidates:
   - Redesign utilities that remove work: shared eligibility status, electronic payment, a remittance standard.
   - Recipient-side value: P16, still unanchored.
   - Donor-side revenue.

   These are where v2's gross rankings point (D first in 11 of 16 processes). They are also where the evidence is thinnest (d and adoption are assumed).
4. **Sequencing.** AI-after-redesign raises break-even by 25–45%. **[I]** An entrant selling both redesign and AI cannibalises its own AI revenue. Pricing should rest on the residual exception tail, not on today's workflow.

---

## 8. Limitations

- **Part IX gives totals, not processes.** φ and the v1 process mix are assumed. Anchoring constrains the *scale* of pools, not their *composition*.
- **CF_SMALL covers $10–100m only.** The 427 community foundations under $10m (median IT $17k, [cost-structure §4.2](sponsor-cost-structure-and-sensitivities.md)) are excluded. Every hurdle would be steeper for them.
- **Bootstrap windows are small for nationals:** n = 2 grant anchors for NAT_LARGE and n = 10 for NAT_MID. The NAT_MID IT median uses 5 positive rows.
- **The grant elasticity is borrowed** from operating cost against DAF assets. No grant-count elasticity can be estimated from six anchors.
- **Fixed-cost ranges are v1's, unchanged and size-invariant.** A small sponsor might buy A or B as a SaaS feature at lower cost. That would favour A and B at small sponsors and leave the C conclusions largely intact, since C's cost is mainly governance.
- **Parameters are independent.** In reality s and q are probably negatively correlated, because better models save more time and need less re-review. That would widen C's tails.
- **QA follows v1's convention:** a share q of *all* touched cases is re-reviewed at half the minutes.
- **The network build-out ignores inference** (≤ 1.6% of pool) and assumes the same φ and AI parameters for every sponsor in a draw.
- **The CSV mixes denominators.** The `social_breakeven_*` quantiles include never-breaks-even draws, coded as 1e9. The `vendor_breakeven_*_finite` quantiles are taken among finite draws only.

---

## 9. Data dictionary

### `data/mission-2026-11-14/ai-economics-v2-results.csv` (long format; one metric per row)

| Column | Meaning |
|---|---|
| `record_type` | `assumption` (one row per assumed distribution); `meta` (draws, seed, v1 replication check); `grant_anchor` (observed cost per grant, labour share and v1-implied φ for Fidelity and DAFgiving360); `archetype_anchor` (observed window statistics, scaled cost, pools, v1 comparisons); `process_intervention` (per archetype × process × intervention); `sensitivity` (tercile shares across P01–P15); `sensitivity_process` (P(C first by gross) by tercile of a, s, d per process); `platform` (homogeneous-network break-even); `platform_network` (greedy build-out over the observed FY2024 population) |
| `archetype` | NAT_LARGE, NAT_MID, CF_1BN, CF_250M, CF_SMALL, REF_V1_1M (v1 bottom-up, linear, for comparison), ALL, OBSERVED_POPULATION |
| `process_id`, `process` | P01–P16 as in v1 |
| `intervention` | A, B, C, D, or `none` (no intervention clears its fixed cost) |
| `parameter` | For `sensitivity*`: s, q, a_p, d_p, alpha, beta, phi, F_C. For `platform*`: `ai_on_workflow` or `ai_after_redesign`. For `assumption`: the parameter name |
| `bucket` | Tercile (`low`, `mid`, `high`) of the parameter's sampling quantile, or the network segment (`cf_lt_250m`, `cf_all`, `national_lt_10bn`, `cf_and_national_lt_10bn`, `cf_and_national_all`) |
| `metric` | See below |
| `value`, `unit` | Value and unit |
| `basis` | `observed`, `computed`, `v1 assumption`, `assumption-driven` (depends on §3.2 distributions), or a mixed label such as `assumed fixed cost / observed IT median` |
| `note` | Definition notes and sources |

Main metrics:
- `p_rank_first_net`: P(first by gross minus fixed cost, with "none" = 0).
- `p_rank_first_gross` and `p_rank_last_gross`: rank among A–D before fixed costs.
- `p_net_positive`.
- `net_value_{p05,p25,p50,p75,p95,mean}`.
- `gross_p50`, `pool_p50`.
- `fixed_cost_over_it_median_p50` and `p_fixed_cost_gt_it_median`.
- `p_C_beats_B_gross`.
- `v1_gross_base_1m` and `v1_rank_base`: v1 values for comparison.
- Archetype anchors: `daf_opex_scaled_*`, `it_hurdle_denominator_*`, `grants_per_year_*`, `sponsor_pool_P01_P15_*`, `sponsor_pool_per_grant_*`, `v1_linear_pool_at_median_grants`, `v1_elasticity_pool_at_median_grants`, `inference_share_of_pool_p50`, `available_sponsors_fy2024`.
- Platform: `sponsor_ai_gross_value_*`, `p_self_build_platform_pays`, `p_vendor_breakeven_finite`, `vendor_breakeven_sponsors_{p10,p50,p90}_finite`, `social_breakeven_sponsors_*` (τ = 1; 1e9 = never), `vendor_breakeven_grants_*`, `p_vendor_breakeven_le_{10,50,200,1000,available}`, `vendor_fee_over_it_median_p50`.
- Network: `segment_sponsors_fy2024`, `p_breakeven_reachable`, `breakeven_sponsors_{p10,p50,p90}_reachable`.

### `data/mission-2026-11-14/queue-proposals-ai-econ-v2.csv`

Six proposals, P-AIV2-01 to P-AIV2-06, in the format of `queue-proposals-README.md`.

### Reproduce

```
python3 scripts/mission_ai_economics_v2.py            # 10,000 draws, about 1 minute; network build-out uses 2,000
python3 scripts/mission_ai_economics_v2.py --draws 2000 --out /path/test.csv
```

Inputs are read only: `ai-process-economics.csv`, `sponsor-cost-structure.csv` and `sponsor-cost-structure-summary.csv`. No network access is needed.
