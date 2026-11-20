# Validation wave 41C: manual improvement (A) held to the evidence standard (g0403-01)

**Validator:** independent-validation-agent-wave41c · **Date:** 2026-11-20 · **Register:** [`validation-register-wave41c.csv`](../../data/mission-2026-11-14/validation-register-wave41c.csv) (20 claims)

**Checked:** [g0403-01-manual-improvement-calibration.md](g0403-01-manual-improvement-calibration.md), `data/mission-2026-11-14/manual-improvement-evidence-2026-11-20.csv`, `data/mission-2026-11-14/ai-ranking-a-calibrated-2026-11-20.csv` and `scripts/mission_ai_a_calibrated.py`. Nothing was committed or pushed, and no repo file other than these two outputs was written.

## Counts

| Result | Re-run and evidence (V41C-01 to -10) | Results, framing and repo passages (V41C-11 to -20) | Total |
|---|---|---|---|
| confirmed | 8 | 5 | 13 |
| partially_confirmed | 2 | 4 | 6 |
| contradicted | 0 | 1 | 1 |
| unverifiable | 0 | 0 | 0 |
| **Total** | **10** | **10** | **20** |

There are 19 exact corrections: 10 to g0403-01, 9 to other files (including §11.56 of the industry report).

## Method

- **Re-run.** `python3 scripts/mission_ai_a_calibrated.py . --draws 10000 --archetypes NAT_LARGE` wrote its output to scratch (`--out`, `--evidence-out`). It produced 17,168 rows (spec, meta and NAT_LARGE), identical row for row to the NAT_LARGE and ALL rows of the repo CSV. The evidence CSV is byte-identical (`cmp`). The idx passed to `cal.simulate` is the full-list index, so a single-archetype run reproduces the same draws.
- **Replication against the recut.** Filtered to scenario CAL_CENTRAL, 250 values (mean P(first) for each option and the modal strings, for ASSIST and ROUTE_A01_M1, at all five archetypes) were compared. A_V1 against the recut's same B/D spec, and A_RPA_ANALOGY × BD_FIELD against ABD_FIELD, gave **0 mismatches**. Without the scenario filter there appear to be 45 "mismatches", because the recut CSV also holds three other framings.
- **Sources.** These were fetched with user agent `research-script/1.0` after robots.txt was read with `urllib.robotparser`. All four were allowed and returned 200:
  - NAO HC 1336 (22 Oct 2025);
  - NAO HC 1375 (16 Jun 2023);
  - the NAO guide *Improving operational delivery in government* (Mar 2021);
  - the Econometrica abstract page.
- **Results.** Every number in the tables in §0 and §3.1–3.5, every modal string and every summary count was recomputed from the CSV by script.
- **Not used:** sec.gov, crt.sh and certspotter. There was no outreach and no change of user agent.

## Findings

### Confirmed
- **Reproducibility.** Both the model and the evidence table reproduce exactly (V41C-01, -02).
- **DWP TCR (HC 1336, Figure 9 and paras 3.27–3.28).**
  - Productivity: 0.57 against 1.20 expected (2023-24) and 1.07 against 0.89 (2024-25).
  - Cases: 1,151,000 against 1,104,000 (104%).
  - Savings: £581m against £525m (11% above).
  - Hit rate: 20% against 24%.
  - The by-year rows are as transcribed (V41C-03, -04).
- **Home Office PACE (HC 1375).**
  - Figure 9 gives the plan as 1.4 to 2.5 decisions a week.
  - Para 3.9: "the 640 active caseworkers (those making decisions) achieved the 2.5 decisions weekly"; the consultancy contract was £24m.
  - Para 3.12: 72% of decisions were administrative (84% for Albanian claimants, footnote 33) (V41C-06, -07).
- **IOPC.** The guide says productivity "may have increased by 33%" (V41C-08).
- **Fenizia.** The abstract states 10% (driven by the exit of retiring older workers) and "at least 6.9%" (V41C-09).
- **Model results.**
  - The P(rank first) tables, all 24 modal strings, the sweep table and thresholds, the pools, the median and p25–p75 C increments, and the net-first values all match (V41C-11, -12, -14, -15).
  - A or "none" wins on net in all 168 NAT_LARGE cells. The maximum net P(C first) is 0.108.
  - The archetype claims match (V41C-18).

### Discrepancies
1. **Contradicted (V41C-16).** "Assistance … at most 0.140 (A_LEVEL_A_FIELD × BD_PROGRAM)" (§0 item 4 and §4) is wrong. The maximum is **0.167027** (A_RPA_ANALOGY × BD_PROGRAM); 0.140 is the maximum only if the RPA-analogy spec is left out. Assistance is still modal nowhere.
2. **Absorption rounding (V41C-13).** The hybrid A_RPA_ANALOGY share_A is 0.124522. That rounds to 0.12, but the table prints 0.13.
3. **BD_PROGRAM range (V41C-17).** "C is modal in 5 (A_FIELD) to 12" leaves out A_V1, which gives 2 at m = 1.56–1.77 (3 at m = 1), and m = 9.28, which gives 0–6.
4. **The DWP caveat "The agents are outsourced" is only partly right (V41C-05).**
   - Agents were in-house through 2023-24. TP was contracted in June 2024, delivery became hybrid from September 2024, and TP had about 2,600 FTE by January 2025.
   - Footnote 23: outsourced agents hand entitlement decisions to DWP staff. Part of the 2024-25 cases-per-agent figure (1.07) therefore leaves some labour per case uncounted.

### Interpretation challenges (r_A and framing)
- **The r_A mapping is correctly labelled [I], but it is not the standard applied to B (V41C-10).**
  - B's r is realized ÷ estimated *savings*. The DWP bounds are ratios of productivity *levels*, which compress towards 1. Illustration [C]: a planned 20% gain realized at 10% is 1.10/1.20 = 0.92 as a level ratio but 0.50 as a gain ratio.
  - The top value, 1.20, comes from a 2024-25 expectation (0.89) that was lower than the 2023-24 one (1.20). Against 1.20, the 2024-25 actual is 0.89 [C]. NAO does not explain the change.
  - The mode, 1.0, rests on PACE's headline, which applies only to the active caseworkers. At workforce level, about 1,310 decisions a week against the 1,350 × 62% × 2.5 ≈ 2,090 the business case implies is about 0.63 [C], although that shortfall comes from headcount. NAO also does not reconcile 640 × 2.5 = 1,600 with the 1,310 total.
  - The range probably favours A.
- **Framing (V41C-19).** The bold "Yes, under the only audited realization evidence" is fair for assistance: A takes 94% of what B and D lose and is modal in 6 processes. It is overstated in general:
  - with A01 routing at the current m = 1.77, C is modal in 5 processes and A in 1, even though A still takes 58% of the lost probability;
  - the evidence is audited *throughput*, mapped by inference, not audited labour-savings realization.
  The body (§0 items 2–3, §5) does say this. The headline and §4 should say it too.
- **Sweep wording.** §4 says A's role "no longer holds" at r_A ≤ 0.5 with assistance. At 0.5, A is still modal in P03 (V41C-14). This is minor and is left as is.
- **Other docs (V41C-20).** The rankings in g0403-04 and g0403-0104 (≤ 0.032–0.043 and ≤ 0.035) use v1 priors for A, B and D: their scripts do not import the recut. They remain true for that setting but need a qualifier.

## Exact corrections

All values are on one line; `\n` stands for a newline. A script checked that each Find occurs exactly once in the current file.

### `research/mission-2026-11-14/g0403-01-manual-improvement-calibration.md`
- **Find:** "**Does A still absorb what B and D lose? Yes, under the only audited realization evidence for manual work. The answer turns on r_A.**"
- **Replace with:** "**Does A still absorb what B and D lose? With assistance as C, yes, under an [I] mapping of audited manual-casework throughput realization (not realized labour savings, the standard applied to B) onto r_A. With A01 routing at the current m = 1.56–1.77, A still takes 58% of what B and D lose, but C is modal in 5 processes and A in 1–2. The answer turns on r_A.** [V wave 41C]"
- **Find:** "4. **Assistance remains modal nowhere** in any A × B/D cell at a large national. Its rank-first probability is at most **0.140** (A_LEVEL_A_FIELD × BD_PROGRAM)."
- **Replace with:** "4. **Assistance remains modal nowhere** in any A × B/D cell at a large national. Its rank-first probability is at most **0.167** (A_RPA_ANALOGY × BD_PROGRAM); excluding the RPA-analogy stress spec it is at most 0.140 (A_LEVEL_A_FIELD × BD_PROGRAM) [V wave 41C]"
- **Find:** "- **Mapping [I]:** realized A = r_A·α·L. Here r_A is drawn from triangular(0.475, 1.00, 1.20):"
- **Replace with:** "- **Mapping [I]:** realized A = r_A·α·L. Here r_A is drawn from triangular(0.475, 1.00, 1.20). The DWP bounds are ratios of productivity levels (actual ÷ expected cases per agent per day), not of realized ÷ planned gains or savings, so they compress towards 1: a planned 20% gain realized at 10% gives a level ratio of 1.10/1.20 = 0.92 but a gain ratio of 0.50 [C, illustrative]. The range is therefore likely to favour A relative to the realized-÷-estimated-savings standard applied to B [V wave 41C]"
- **Find:** "  - top: TCR 2024-25 productivity, 1.07/0.89."
- **Replace with:** "  - top: TCR 2024-25 productivity, 1.07/0.89. The 2024-25 expectation (0.89) is lower than the 2023-24 expectation (1.20), and NAO does not explain the change; against the earlier 1.20 expectation, the 2024-25 actual is 0.89 [C] [V wave 41C]"
- **Find:** "Case selection uses analytics-built rules. The savings are benefit outcomes, not administrative cost. The agents are outsourced."
- **Replace with:** "Case selection uses analytics-built rules. The savings are benefit outcomes, not administrative cost. Agents were DWP staff until 2023-24; DWP contracted TP in June 2024, moved to a hybrid model from September 2024 (TP had about 2,600 FTE agents by January 2025), and outsourced agents hand any entitlement decision to DWP staff (paras 3.22–3.24, footnote 23) [V wave 41C]"
- **Find:** "  - Only about 50% of caseworkers were deciding claims."
- **Replace with:** "  - Only about 50% of caseworkers were deciding claims (about 640 of 1,270 at the end of April 2023, against a business-case assumption of 62% of 1,350; para 3.8, Figure 9). At workforce level, about 1,310 decisions a week in April 2023 (para 3.12) against the 1,350 × 62% × 2.5 ≈ 2,090 the business case implies is a ratio of about 0.63 [C], although that shortfall is headcount, not handling speed [V wave 41C]"
- **Find:** "With A01 routing, C is modal in 5 (A_FIELD) to 12 (RPA analogy) processes."
- **Replace with:** "With A01 routing at m = 1.56–1.77, C is modal in 2 (A_V1), 5 (A_FIELD), 6 (A_FIELD_CAPPED), 10 (A_LEVEL_A) and 12 (A_RPA_ANALOGY, A_LEVEL_A_FIELD) processes; at m = 1 it is 3 under A_V1, and at m = 9.28 it is 0–6 [V wave 41C]"
- **Find:** "| Hybrid A01, m = 1.77 | 0.58 | 0.49 | 0.34 | 0.13 | 0.04 |\n\nEach value is A's share of the rank-first probability lost by B and D."
- **Replace with:** "| Hybrid A01, m = 1.77 | 0.58 | 0.49 | 0.34 | 0.12 | 0.04 |\n\nEach value is A's share of the rank-first probability lost by B and D. The hybrid A_RPA_ANALOGY value is 0.1245 in the CSV, so it rounds to 0.12, not 0.13 [V wave 41C]"
- **Find:** "| Assistance wins no process | **Unchanged** in every A × B/D cell. Maximum P(C first) is 0.140 (A_LEVEL_A_FIELD × BD_PROGRAM) |"
- **Replace with:** "| Assistance wins no process | **Unchanged** in every A × B/D cell. Maximum P(C first) is 0.167 (A_RPA_ANALOGY × BD_PROGRAM); 0.140 excluding the RPA-analogy spec (A_LEVEL_A_FIELD × BD_PROGRAM) [V wave 41C]"
- **Find:** "**Holds under the only audited manual-programme realization (A_FIELD).**"
- **Replace with:** "**Holds with assistance under A_FIELD, an [I] mapping of audited manual-casework throughput realization (not labour-savings realization) onto r_A** [V wave 41C]"

### `research/mission-2026-11-14/g0401-0103-ai-bd-recut.md`
- **Find:** "   - A's α ~ U(0.05, 0.25) is also an uncalibrated v1 prior."
- **Replace with:** "   - A's α ~ U(0.05, 0.25) is also an uncalibrated v1 prior. g0403-01 found no 2021+ audit of realized labour savings from a manual fix. One self-report (IOPC, about 0.25 per unit) and one peer-reviewed management study (Fenizia 2022, 0.065–0.091) bracket α without narrowing it. Mapping NAO manual-casework throughput realization onto A as r_A ~ tri(0.475, 1.0, 1.2) [I] leaves A modal in the same 6 processes with assistance (g0403-01 §3) [V wave 41C]"
- **Find:** "- That outcome tests A's prior, not AI. α ~ U(0.05, 0.25) has no source."
- **Replace with:** "- That outcome tests A's prior, not AI. α ~ U(0.05, 0.25) has no source. g0403-01 holds A to throughput realization from two NAO casework audits [I]: with assistance A still takes 94% of what B and D lose. With A01 routing at m = 1.77, C is modal in 5 processes and A in 1. If α is set to the peer-reviewed level, A is modal in at most 1 process. The r_A evidence is throughput against plan, not realized labour savings [V wave 41C]"
- **Find:** "and it is also [I] (P-G0403-01)."
- **Replace with:** "and it is also [I] (P-G0403-01). g0403-01 retains it as a lower-bound stress test (A_RPA_ANALOGY) because the RPA range is a technology-programme realization [V wave 41C]"

### `research/mission-2026-11-14/g0401-g0502-ai-routing-and-per-grant.md`
- **Find:** "but manual improvement (A), whose α is also an unsourced prior, becomes the modal winner in 6 of 15 processes. C becomes modal only if A is cut too or h runs up to 0.80 [S]."
- **Replace with:** "but manual improvement (A), whose α is also an unsourced prior, becomes the modal winner in 6 of 15 processes. C becomes modal only if A is cut too or h runs up to 0.80 [S]. With A held to NAO manual-casework throughput realization (g0403-01, r_A ~ tri(0.475, 1.0, 1.2) [I]) at the current m = 1.77, A01 routing is modal in 5 processes (P03, P07, P11, P13, P14) and A in 1 (P08); assistance is still modal nowhere [S] [V wave 41C]"

### `research/mission-2026-11-14/g0403-04-escaped-error-cost.md`
- **Find:** "7. **The ranking conclusion does not change.** Assistance is still modal nowhere."
- **Replace with:** "7. **The ranking conclusion does not change.** Assistance is still modal nowhere. These ranking figures use the v1 priors for A, B and D. With B and D at the recut’s BD_FIELD and A at g0403-01’s A_FIELD, assistance is still modal nowhere, but A01 routing at m = 1.77 reaches a mean P(C first) of 0.200 and is modal in 5 of 15 large-national processes [S] [V wave 41C]"

### `research/mission-2026-11-14/g0403-0104-m-detection-ofac.md`
- **Find:** "does not change the ranking conclusion: C's mean rank-first probability is ≤ 0.035 in every cell."
- **Replace with:** "does not change the ranking conclusion: C's mean rank-first probability is ≤ 0.035 in every cell. This is with the v1 priors for A, B and D; under BD_FIELD × A_FIELD (g0403-01), A01 routing at m = 1.56–1.77 reaches 0.200–0.204 and is modal in 5 large-national processes, while assistance stays modal nowhere [S] [V wave 41C]"

### `research/mission-2026-11-14/strategic-synthesis.md`
- **Find:** "raises C's rank-first probability but hands most processes to manual improvement, whose prior is also unsourced."
- **Replace with:** "raises C's rank-first probability but hands 6 of 15 large-national processes to manual improvement (A). A's saving α is still unsourced. Mapping NAO manual-casework throughput realization onto A [I] keeps those 6 processes with assistance, but at the current m = 1.77 A01 routing is then modal in 5 processes and A in 1 (g0403-01) [S] [V wave 41C]"

### `research/mission-2026-11-14/FINAL-STATUS.md`
- **Find:** "With B and D held to C's evidence standard, AI assistance still wins no process, and the processes B and D lose go to manual improvement, whose α is unsourced."
- **Replace with:** "With B and D held to C's evidence standard, AI assistance still wins no process, and the processes B and D lose go to manual improvement, whose α is unsourced. Holding A to NAO manual-casework throughput realization [I] (g0403-01) keeps A modal in 6 of 15 processes with assistance; with A01 routing at m = 1.77, C is modal in 5 and A in 1. No audit of realized labour savings from a manual fix was found [V wave 41C]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`
- **Find:** "\n---\n\n## Source register"
- **Replace with:** "\n### 11.56 AI economics: manual improvement held to the same standard (validated, wave 41C)\n\n**AI economics: manual improvement held to the same standard** (validated, wave 41C). Manual improvement (A) absorbed most of what conventional automation and redesign lost when those were cut to audited RPA realization. No 2021+ audit measures realized labour savings from a manual fix. The closest evidence is two NAO casework audits, re-read by the validator. DWP’s Targeted Case Review achieved 0.57 cases per agent per day against 1.20 expected in 2023-24 and 1.07 against 0.89 in 2024-25. Home Office PACE reached its planned 2.5 weekly decisions per active caseworker, but 72% of those decisions were administrative. These are throughput ratios, and they map onto A’s realization only by inference, which likely favours A. With that mapping, AI assistance is still modal nowhere and A keeps 6 of 15 large-national processes. With high-confidence routing at the current escaped-error multiple (1.77), AI is modal in 5 processes and A in 1. With α at the peer-reviewed level, A is modal in at most 1 process. The model re-runs exactly. [V wave 41C]\n\n---\n\n## Source register"
