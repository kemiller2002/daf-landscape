# Validation wave 42C: routing realization and correlated realization (g0403-0105-04)

*Validator: independent-validation-agent-wave42c. Validated 2026-11-20. Nothing committed or pushed; no outreach; crt.sh, certspotter and sec.gov not used.*

**Validated:** [g0403-0105-04-routing-realization-and-correlation.md](g0403-0105-04-routing-realization-and-correlation.md), `data/mission-2026-11-14/ai-ranking-realized-correlated-2026-11-20.csv`, `scripts/mission_ai_realized_correlated.py`. Register: [`validation-register-wave42c.csv`](../../data/mission-2026-11-14/validation-register-wave42c.csv).

## Counts

20 claims: **14 confirmed, 5 partially confirmed, 1 contradicted, 0 unverifiable.**

## What was checked

- **Re-run (V42C-01).** NAT_LARGE re-run to scratch (`--archetypes NAT_LARGE --draws 10000`) in 4 min 12 s. All 14,873 NAT_LARGE model and meta rows are byte-identical to the repo CSV; only the two replication rows differ (3,830 compared, 0 mismatched at NAT_LARGE alone).
- **Replication (V42C-02).** Recomputed independently against `ai-ranking-a-calibrated-2026-11-20.csv`: 7,150 C_V1 / rank-correlation-0 values (main and absorption), all matched, 0 unmatched, 0 mismatches, max relative difference 0. Minor: the replication row note says `cell=main`, but absorption cells are included.
- **Headline values (V42C-03 to -06, -09, -13, -17, -18).** Every quoted P(rank first), modal string, count, value and absorption share for C_UPPER_FIELD at m = 1.77 and 1.56, the r_C sweep, hybrid, the rank-correlation 0.5 and 1.0 cells, set ABCD and the absorption shares matches the CSV. Ranges in §3.3 (B −0.031 to −0.066, C +0.009 to +0.057, A and D ranges) also reproduce from unrounded values.
- **Copula (V42C-11).** 2·sin(π·0.5/6) = 0.517638 and the inverse gives 0.500. Empirical Spearman at 0.5 is r_A–r_B 0.4975, r_B–r_D 0.5004, r_A–r_D 0.5179 and r_C–r_B 0.5088, all 1.000 at 1.0. U = u exactly at 0. r_A–r_D sits above 0.5 because the existing recut stream already has 0.023 at independence (disclosed in §5).
- **h cut (V42C-12).** The code matches the formula (h_eff(0.8, 0.33) = 0.599; h below 0.50 is untouched). H_SPLIT = 0.50 and the RPA mapping are labelled [I] in §0, §1.3 and §5. 0.50 is also the top of the lower-half evidence (E19 0.21–0.49; CB-04 0.494), which supports the split. The RPA audits measure bot labour hours, not classifier auto-close shares, so the [I] label is needed and correct.

## Findings

1. **Item 4 is contradicted (V42C-07).** The sample mean of r_C is 0.470, with 59% of draws below 0.5. C_UPPER_FIELD at m = 1.77 (0.168, 2 modal processes) lies between fixed r_C = 0.5 (0.170, 3) and 0.33 (0.159, 1), so the cut acts about as its mean implies, not "milder". "Most of routing's advantage comes from the lower half of h" holds only for mean P(C first): at r_C = 0, 0.137 of 0.200 remains. It fails in modal and value terms: 1 of 5 modal processes remains, and $43k of $133k of median value beyond the best other option.
2. **C_ALL_FIELD wording (V42C-08).** C is modal in 0 in every A_V1 and A_FIELD cell, as stated. However, "A modal in 6" is false under A_V1 × V1_PRIORS, where A is modal in 1.
3. **Scope of modal changes (V42C-14).** "At most 2 in any A_FIELD cell at NAT_LARGE" holds for set ABD only. Set ABCD changes 4 (Route A01 m = 1.77 at ρ_s = 1). "Up to 4" applies only to NAT_MID; the community-foundation archetypes change at most 2. At CF_1BN, P01 comes from B, not A.
4. **Claim 7 and wave 37C (V42C-15).** The numbers hold. Under A_FIELD, correlation moves rank-first probability from B (−0.031 to −0.066) to A and C, and the B and D levels move further from V1. Wave 37C's sentence, however, is a conditional about one *identical* factor on A, B, C and D. In that case the gross ranking is V1 by construction, and the study never ran it. What the study contradicts is g0403-01 §5 item 6's paraphrase ("revert towards V1 priors"), not wave 37C's conditional. The comonotone max-of-two mechanism is sound (E[max] is smallest under comonotonicity) but is unlabelled inference, so it should carry [I]. Cosmetic: the item numbers in §0 repeat (7 appears in both lists).
5. **Claim 8 (V42C-16).** Under A_RPA_ANALOGY the mean order D > B > A already held at rank correlation 0 (0.454 / 0.227 / 0.048), so nothing "reverts". A falls to 0.018, further below V1's 0.054.
6. **"Assistance is modal nowhere" is fair (V42C-19)** and is the study's most robust result: no ASSIST modal string contains C; the maximum is 0.065 at NAT_LARGE and 0.080 across archetypes. "Both studies" is loose, because assistance (no h) is run only in study B.
7. **Repo propagation (V42C-20).** Seven documents state "A01 routing modal in 5, A in 1" under A_FIELD × BD_FIELD without the upper-half h cut. These figures are correct as the uncut (C_V1) case, but under the [I] cut they become 2 and 4 (m = 1.77) and 3 and 3 (m = 1.56). Corrections below add the cut figures rather than replacing the uncut ones, because the cut is an [I] mapping.

## Exact corrections

### `research/mission-2026-11-14/g0403-0105-04-routing-realization-and-correlation.md`

- **Find:** "4. **The cut on the upper half is milder than its mean suggests.** r_C's mean is 0.47, but even r_C = 0 (h capped at 0.50) leaves A01 routing modal in P07 and hybrid modal in 5 processes (§3.2). Most of routing's advantage comes from the lower half of h."
- **Replace with:** "4. **The cut on the upper half acts about as its mean implies.** r_C's mean is 0.47 (sample mean 0.470; 59% of draws below 0.5), and C_UPPER_FIELD at m = 1.77 (0.168, 2 modal processes) sits between fixed r_C = 0.5 (0.170, 3) and 0.33 (0.159, 1). Even r_C = 0 (h capped at 0.50) leaves A01 routing modal in P07 and hybrid modal in 5 processes (§3.2). The lower half of h keeps 0.137 of routing’s 0.200 rank-first probability, but only 1 of its 5 modal processes and $43k of its $133k median value beyond the best of A, B and D, so most of routing’s modal and value advantage rests on the upper half [S] [V wave 42C]"
- **Find:** "removes routing and hybrid as modal winners** in every A_V1 and A_FIELD cell (A modal in 6, C in 0)."
- **Replace with:** "removes routing and hybrid as modal winners** in every A_V1 and A_FIELD cell (C modal in 0; A modal in 6, except under A_V1 × V1_PRIORS, where A is modal in 1 and B and D keep the rest) [V wave 42C]"
- **Find:** "and changes at most 2 modal winners in any A_FIELD cell at NAT_LARGE.** At the other archetypes it changes up to 4, and there A01 routing gains modal processes from A: at NAT_MID (m = 1.77) C goes from 2 to 5 modal processes (P03, P13, P14 from A), and at the community-foundation archetypes from 6 to 7 (P01 from A)."
- **Replace with:** "and changes at most 2 modal winners in any A_FIELD cell of set ABD at NAT_LARGE** (set ABCD: up to 4, Route A01 m = 1.77 at rank correlation 1, P11, P13 and P14 to C and P15 to D). It changes up to 4 at NAT_MID and up to 2 at the community-foundation archetypes, and there A01 routing gains modal processes: at NAT_MID (m = 1.77) C goes from 2 to 5 modal processes (P03, P13, P14 from A), and at the community-foundation archetypes from 6 to 7 (P01, from A at CF_250M and CF_SMALL and from B at CF_1BN) [V wave 42C]"
- **Find:** "7. **Why B loses.**"
- **Replace with:** "7. **Why B loses** (a mechanism inferred from the results, not decomposed [I]; the finding contradicts g0403-01 §5 item 6’s paraphrase of wave 37C, while wave 37C’s identical-factor case for A, B, C and D was not run) [V wave 42C]"
- **Find:** "Then the ordering among A, B and D does revert to V1 (A falls to 0.018), and C, which carries no factor, gains: A01 routing at m = 1.77 goes from 0.270 and 5 modal processes to **0.321 and 6** [S]."
- **Replace with:** "Then the mean ordering among A, B and D is V1’s (D > B > A), but it already was at rank correlation 0 (0.454 / 0.227 / 0.048), and the levels move away from V1, not back (A 0.018 against 0.054 under V1 priors; B 0.196 against 0.287). C, which carries no factor, gains: A01 routing at m = 1.77 goes from 0.270 and 5 modal processes to **0.321 and 6** [S] [V wave 42C]"
- **Find:** "10. **Assistance remains modal nowhere** in every cell of both studies at every archetype (maximum P(C first) 0.065 at NAT_LARGE and 0.080 across archetypes, both A_RPA_ANALOGY × BD_FIELD at rank correlation 1)."
- **Replace with:** "10. **Assistance remains modal nowhere** in every cell of study B at every archetype (assistance has no h, so it is not run in study A; maximum P(C first) 0.065 at NAT_LARGE and 0.080 across archetypes, both A_RPA_ANALOGY × BD_FIELD at rank correlation 1) [V wave 42C]"
- **Find:** "At NAT_MID and the community-foundation archetypes up to 4 change, mostly from A to C (e.g. NAT_MID A01 m = 1.77: P03, P13, P14 A→C)"
- **Replace with:** "Up to 4 change at NAT_MID and up to 2 at the community-foundation archetypes, mostly from A to C (e.g. NAT_MID A01 m = 1.77: P03, P13, P14 A→C; hybrid at CF_1BN and CF_250M: P05 D→C) [V wave 42C]"

### `research/mission-2026-11-14/g0403-01-manual-improvement-calibration.md`

- **Find:** "At m = 9.28 (wave-39B high), C is modal nowhere and A is back to 6 processes."
- **Replace with:** "At m = 9.28 (wave-39B high), C is modal nowhere and A is back to 6 processes. With the upper half of h (above 0.50) held to the RPA realization range [I] (g0403-0105-04, C_UPPER_FIELD), A01 routing at m = 1.77 falls to 0.168 and 2 modal processes (P03, P07) with A in 4; at m = 1.56, 0.172 with C and A in 3 each; hybrid stays modal in 5 [S] [V wave 42C]"
- **Find:** "The h-asymmetry caveat (wave 37C) still applies: routing's h upper half is not haircut"
- **Replace with:** "The h-asymmetry caveat (wave 37C) is tested in g0403-0105-04: with routing’s h upper half held to the RPA range [I], C is modal in P03 and P07 at m = 1.77 and in P03, P07 and P14 at m = 1.56 [S] [V wave 42C]"
- **Find:** "With a common factor, ranks among A, B and D revert towards V1 priors (wave 37C)."
- **Replace with:** "g0403-0105-04 tested a common factor (Gaussian copula, rank correlation 0.5 and 1): under A_FIELD it does not revert ranks towards V1 priors but moves rank-first probability from B (and slightly D) to A and C, changing at most 2 large-national modal winners [S] [V wave 42C]"

### `research/mission-2026-11-14/g0401-0103-ai-bd-recut.md`

- **Find:** "A01 routing modal in P03 only, and assistance and routing-note routing in none [C]. [V wave 37C]"
- **Replace with:** "A01 routing modal in P03 only, and assistance and routing-note routing in none [C]. [V wave 37C] g0403-0105-04 tested correlated, not identical, factors: with A at A_FIELD the ranking does not revert to V1 (B loses most, A and C gain), and with the upper half of h held to the RPA range [I], A01 routing at m = 1.77 is modal in 2 large-national processes under A_FIELD × BD_FIELD [S] [V wave 42C]"
- **Find:** "With A01 routing at m = 1.77, C is modal in 5 processes and A in 1."
- **Replace with:** "With A01 routing at m = 1.77, C is modal in 5 processes and A in 1; with the upper half of h held to the RPA range [I], 2 and 4 (g0403-0105-04) [S] [V wave 42C]"

### `research/mission-2026-11-14/g0401-g0502-ai-routing-and-per-grant.md`

- **Find:** "A01 routing is modal in 5 processes (P03, P07, P11, P13, P14) and A in 1 (P08); assistance is still modal nowhere [S] [V wave 41C]"
- **Replace with:** "A01 routing is modal in 5 processes (P03, P07, P11, P13, P14) and A in 1 (P08); assistance is still modal nowhere [S] [V wave 41C] With the upper half of h held to the RPA realization range [I] (g0403-0105-04), routing keeps P03 and P07 and A has 4 [S] [V wave 42C]"

### `research/mission-2026-11-14/g0403-04-escaped-error-cost.md`

- **Find:** "is modal in 5 of 15 large-national processes [S] [V wave 41C]"
- **Replace with:** "is modal in 5 of 15 large-national processes [S] [V wave 41C] With the upper half of h held to the RPA realization range [I] (g0403-0105-04), it is 0.168 and 2 processes [S] [V wave 42C]"

### `research/mission-2026-11-14/g0403-0104-m-detection-ofac.md`

- **Find:** "A01 routing at m = 1.56–1.77 reaches 0.200–0.204 and is modal in 5 large-national processes, while assistance stays modal nowhere [S] [V wave 41C]"
- **Replace with:** "A01 routing at m = 1.56–1.77 reaches 0.200–0.204 and is modal in 5 large-national processes, while assistance stays modal nowhere [S] [V wave 41C] With the upper half of h held to the RPA realization range [I] (g0403-0105-04), routing reaches 0.168–0.172 and is modal in 2–3 [S] [V wave 42C]"

### `research/mission-2026-11-14/strategic-synthesis.md`

- **Find:** "but at the current m = 1.77 A01 routing is then modal in 5 processes and A in 1 (g0403-01) [S] [V wave 41C]"
- **Replace with:** "but at the current m = 1.77 A01 routing is then modal in 5 processes and A in 1 (g0403-01) [S] [V wave 41C] Holding the upper half of h to the same RPA range [I] cuts routing to 2 processes and A to 4 (hybrid 5), and correlated realization moves probability from B to A and C rather than back to V1 priors (g0403-0105-04) [S] [V wave 42C]"

### `research/mission-2026-11-14/FINAL-STATUS.md`

- **Find:** "Under A01 routing at m ≈ 1.8, AI is modal in 5 processes and A in 1."
- **Replace with:** "Under A01 routing at m ≈ 1.8, AI is modal in 5 processes and A in 1; with the upper half of h held to the RPA realization range [I], 2 and 4 (g0403-0105-04) [S] [V wave 42C]"
- **Find:** "with A01 routing at m = 1.77, C is modal in 5 and A in 1."
- **Replace with:** "with A01 routing at m = 1.77, C is modal in 5 and A in 1; with the upper half of h held to the RPA range [I], 2 and 4, and correlated realization moves probability from B to A and C, not back to V1 priors (g0403-0105-04) [S] [V wave 42C]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

- **Find:** "\n---\n\n## Source register"
- **Replace with:** "\n### 11.59 AI economics: realization for routing and correlated execution (validated, wave 42C)\n\n**AI economics: realization for routing and correlated execution** (validated, wave 42C). A new study holds the upper half of A01 routing’s auto-close share h (above 0.50, resting on E15’s retrospective 0.78 and State’s self-reported 80%) to the HUD and GSA RPA realization range, r_C ~ tri(0.07, 0.33, 1.00), an [I] mapping. The validator re-ran the large national (14,873 identical rows) and confirmed the replication of the calibrated model (7,150 values, 0 mismatches). At m = 1.77, with A, B, C and D all carrying a realization factor, routing’s P(rank first) falls from 0.200 to 0.168 and its modal processes from 5 to 2 (A 4); hybrid keeps 5; cutting all of h removes both. Correlating realization (Gaussian copula, latent ρ 0.5176 for rank correlation 0.5) does not revert the ranking to V1 priors: it moves probability from B to A and C. Assistance is modal nowhere (maximum 0.080). The cut acts about as its mean implies: the lower half of h keeps 1 of routing’s 5 modal processes and $43k of $133k in median value [S]. [V wave 42C]\n\n---\n\n## Source register"
