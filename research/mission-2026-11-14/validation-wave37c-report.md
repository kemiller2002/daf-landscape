# Validation wave 37C: AI economics recut, B and D held to C's evidence standard (P-G0401-01, P-G0401-03)

*Validated 2026-11-19 by independent-validation-agent-wave37c. Nothing was committed or pushed.*

**Study under validation:** [g0401-0103-ai-bd-recut.md](g0401-0103-ai-bd-recut.md), with [`ai-bd-recut-2026-11-19.csv`](../../data/mission-2026-11-14/ai-bd-recut-2026-11-19.csv), [`ai-confidence-band-evidence-2026-11-19.csv`](../../data/mission-2026-11-14/ai-confidence-band-evidence-2026-11-19.csv) and [`scripts/mission_ai_bd_recut.py`](../../scripts/mission_ai_bd_recut.py).

**Register:** [`validation-register-wave37c.csv`](../../data/mission-2026-11-14/validation-register-wave37c.csv) (V37C-01 to V37C-23).

**Method.**
- The script was rerun with `--draws 10000 --archetypes NAT_LARGE --out` to scratch. This took about 4 minutes and covered CAL_CENTRAL plus the three framing scenarios, the sweeps, and the evidence, spec and meta rows.
- The other archetypes were checked against the committed CSV but not rerun.
- Sources were fetched with the generic user agent `research-script/1.0`, after reading each host's robots.txt with Python's `urllib.robotparser`. All six target paths were allowed (arxiv.org, www.fincen.gov, www.hudoig.gov, gsaig.gov and transforming-classification.blogs.archives.gov).
- arXiv's 15-second crawl delay was respected.
- Nothing was fetched from sec.gov, crt.sh or certspotter, and there was no outreach.
- CB-04 (OCBC benchmark), CB-06 (AFSA), CB-07 (Stanford GSB) and BD-E03/E04 (Treasury) were not re-fetched; they were not on this wave's checklist.

## Counts

| Result | n |
|---|---:|
| confirmed | 12 |
| partially_confirmed | 10 |
| contradicted | 1 |
| unverifiable | 0 |
| **Total** | **23** |

## Findings

### Replication (V37C-01, V37C-02): confirmed
- **The rerun reproduces the committed file exactly.** It wrote 31,515 rows, and every one is identical, cell for cell, to the committed CSV's evidence, spec and meta rows and its NAT_LARGE model rows.
- **The earlier headlines reproduce exactly.**
  - Assistance: P(C first) 0.002113, pool $444,899, P(break-even ≤ 5) 0.1316.
  - Routing (m = 1): 0.01234, $1,364,949, 0.3783.
  - These equal the `ai-routing-variant-2026-11-19.csv` rows.
- **Minor issues.**
  - The docstring advertises an `--evidence-only` flag that the script does not define.
  - The 8-row `ai-confidence-band-evidence-2026-11-19.csv` is hand-built; no script writes it.

### Evidence for each parameter
- **E15 (V37C-03 to V37C-05): confirmed.** All quotes are in the v3 full text (17 Jun 2022):
  - prevalence "less than 3% of the alerted ones" (p. 3);
  - the 80% false-positive cut and the baseline at "close to 80%" recall (p. 4);
  - "alert only 20% of the events while capturing over 90%" (p. 6).
  - **The arithmetic reproduces.** h = 0.779 and e = 0.00385 (≤ 0.39%); at 80% recall, 0.782 and 0.00767.
  - **0.77% is not strictly a bound,** because the baseline recall is only "close to" 80%.
- **"e = 0.10 overstated E15 more than tenfold" (V37C-06): partially confirmed.**
  - The ratio holds: 13–26 times.
  - But the routing note had already labelled 0.10 as a share of positives, not of closed alerts [I]. The fault was a denominator, not an overstatement of E15.
- **HICSS-56, pp. 3478–3479 (V37C-07): partially confirmed.**
  - Both quotes are exact: "~20%" of workload (p. 3478) and the dedicated re-check of auto-closed alerts (p. 3479).
  - But the paper describes a test: "Currently the bank is testing a set-up" (p. 3477) and "During the period of testing". The study's "production bank" (§1.2) and "AML production 0.20" (§5) overstate it.
- **FinCEN Bank of America order (V37C-08 to V37C-10).**
  - **Confirmed exactly:** the 5% false-negative tolerance (7.5% for Board escalation); +16,000 investigations a month, "double [the] prior ongoing monthly volume"; an "incremental 750" staff, plus 800 consultants for the lookback; about 8,900 missed SARs (about $4bn); and a $1.2bn civil money penalty ($750m credited to the OCC payment).
  - **Partially confirmed: the SAR-yield comparison.**
    - The 33–34% yield above the threshold comes from the bank's 2018–2020 testing. The 38–45% below it comes from 2022–Q1 2023.
    - The order presents this as drift across periods. It does not show a same-period band in which the threshold "carried no information".
  - **"Reversed" is [I].** BD-E05's claim that the redesign was "reversed" links two different changes: the 8,200-case cut came from the 2021 recalibration of risk-factor weights, and the doubling estimate from the threshold lowered in 2023.
- **HUD OIG 2021-OE-0007, report pp. 4–5 (V37C-11, V37C-12).**
  - **Confirmed:** 7% (1,015 of 13,644 hours), 15% (2,091) and 1% (24 of 2,100).
  - **The billing-bot 33% is not a shortfall.** OCFO said the 500-hour estimate "was for all three bots combined", yet it was reported for each bot. That makes it an over-report, not a realized-against-planned gap.
  - The 1% reflects a scope cut, and the 11% reflects work already done by hand.
  - All of these are expected or user-reported hours, not measured ones.
- **GSA OIG A210057 (V37C-13): confirmed.**
  - 9 of 10 bots; 30 of 90 minutes; 74%.
  - The 74% comes from the same owner survey in which 80% said the bot met or exceeded expectations.
  - Only one bot gives a numeric ratio. One (Receiving Reports) matched its estimate.
- **State Department deck (V37C-14): confirmed.**
  - "Reduced volume for humans to review (by 80%)" is on p. 6. The QC wording and the 450,000 cables are on p. 5.
  - The figure is an agency self-report, the evidence class the audits found overstated.

### Use of evidence (V37C-15, V37C-16)
- **"Audited realization" is fair as a labelled [I] stress on B.** It is not a calibrated parameter, for three reasons:
  - The inspectors general compared user-reported savings with agency claims, not with an analyst prior like v1's β·b_p.
  - The mode of 0.33 rests on a single quantified bot.
  - The study's own limit 2 concedes a risk of double counting.
- **Borrowing the range for D is labelled [I] in four places:** the docstring, the spec note, §0(B) and limit 3.
- **The label drops out in two places:** §0(B) item 2 ("cut to realized savings") and §5 ("Cutting B and D to audited realization").

### Results (V37C-17 to V37C-20)
- **P(rank first) table:** all 36 cells match.
- **Modal-winner claims match.** Archetype counts: CF_250M 4, CF_1BN 5, CF_SMALL 5, hybrid 8.
- **Framing claims match.**
  - Assistance under CAL_FIELD_INLOOP peaks at 0.73%; the text rounds this to "at or below 0.7%".
  - CAL_TASK_REVIEW with ABD_FIELD: 7.8%, 1 modal process.
  - Compliance: 11.9%, 2 modal processes.
- **Net results match.** "None" ranks first in 59–60% of process-draws under ABD_FIELD. C's net maximum is 11.2% (hybrid) and 8.8% (routing).
- **Vendor break-even matches:** 0.1316 / 0.3783 / 0.5045 / 0.576.
- **Sweeps and r_be match:** medians 0.43, 0.62 and 0.37; P(r_be ≥ 0.33) is 8.7% for assistance and 60%, 52% and 51% for A01 routing.
- **One discrepancy in the value-pool text.** It gives $114k–$384k and $17k–$55k, but the study's own table shows $100k under BD_WIDE (CF_1BN: $15.6k).
- **The fixed-r sweeps differ from the main variants on P09/P10.** They also scale D in P09/P10, which BD_FIELD and BD_PROGRAM exempt.

### Framing (V37C-21)
- **The headline "what replaces B and D is A, not AI" is fairly stated,** and A's unsourced α is flagged.
- **The "held to C's standard" claim is asymmetric for routing.**
  - B and D take an audited-realization haircut.
  - Routing's h upper half gets none: E15's 0.78 is retrospective, and State's 80% is a self-report of the kind the audits found to be 7–33% realized.
  - Because gross ranks are invariant to a common scale factor, one realization factor applied to all four options gives back the V1-priors ranking. A01 routing is then modal only in P03, and assistance and routing-note routing in none [C, from the CSV's V1_PRIORS strings].
- **The routing-modal claims should carry this caveat.**

### Repo passages (V37C-22, V37C-23)
- **The routing note still says the following:**
  - C's last place "reflects the comparison set (uncalibrated B and D priors)" (§A(2), A4).
  - "The E15 abstract does not report prevalence" (A5 limit 2).
- **gap19 still uses E15's 0.10 as an anchor for r.** The value is 1 − recall, not a per-output error. This is the one contradicted claim.
- **Strategic synthesis §0 B** is still true at h ≤ 0.49 but is silent on the recut.
- **The industry report's §11.40** says routing "changes no process's likely winner", which remains true for the routing-note ranges.
- **Not changed:** this wave did not touch earlier wave texts.

## Five key corrections
1. **E15 bound.** Per closed alert, E15 implies at most 0.39%, not 0.10. This changes the routing note (A2 table and limit 2), gap19 and synthesis §0.
2. **Bank of America yields.** 38–45% against 33–34% compares 2022–Q1 2023 with 2018–2020; it is not a same-period band.
3. **Routing-modal claims need an h-asymmetry caveat.** With one common factor on A–D, A01 routing is modal only in P03.
4. **D's cut is analogy [I], not "audited realization".** In addition, HUD's 33% billing-bot figure is an over-report, so the mode rests on one GSA bot.
5. **Routing note's "C's last place reflects B and D priors" is only partly true.** The recut hands processes to A, whose α is unsourced. Also correct the value-pool range to $100k–$384k.

## Exact corrections

### `research/mission-2026-11-14/g0401-0103-ai-bd-recut.md`

- **Find:** "- So the routing note's upper error bound, e = 0.10 attributed to E15, overstated E15's per-closed-alert error by more than ten times."
- **Replace with:** "- So the routing note's upper error bound, e = 0.10 attributed to E15, was a share of true positives missed (1 − recall), a denominator the routing note had already flagged as [I]. Per closed alert, E15 implies at most 0.39% (about 0.77% at the baseline’s ~80% recall), 13–26 times below 0.10. [V wave 37C]"

- **Find:** "Because π < 0.03, both miss rates are upper bounds."
- **Replace with:** "Because π < 0.03 and the graph model’s recall is “over 90%”, 0.39% is an upper bound. The 0.77% is approximate, because the baseline reaches “close to 80%” recall, possibly slightly below 0.80. Both count only SAR-label misses on account-days. [V wave 37C]"

- **Find:** "against 0.33–0.34 just above [F]: a band in which the threshold carried no information"
- **Replace with:** "against 0.33–0.34 just above it in the bank’s earlier 2018–2020 testing [F]. The two yields come from different periods, so they show a threshold that had drifted out of calibration, not a same-period band in which it carried no information [V wave 37C]"

- **Find:** "- The BofA order is a warning against assuming any e: a poorly calibrated threshold produced an error rate below the line no lower than above it."
- **Replace with:** "- The BofA order is a warning against assuming any e: by 2022–Q1 2023 the SAR yield just below the line (38–45%) exceeded the 33–34% the bank had measured just above it in 2018–2020, and was seven to nine times its later 5% false-negative tolerance. [V wave 37C]"

- **Find:** "The BofA order shows the opposite case. Event groups scoring 16–19 points, just below the investigation threshold, had a 38–45% SAR yield in 2022–Q1 2023, against 33–34% just above it."
- **Replace with:** "The BofA order shows the opposite case. Event groups scoring 16–19 points, just below the investigation threshold, had a 38–45% SAR yield in 2022–Q1 2023, against 33–34% just above it in the bank’s 2018–2020 testing. The order compares the two periods; it gives no same-period yield above the threshold. [V wave 37C]"

- **Find:** "When B and D alone are cut to realized savings (BD_FIELD), A becomes the modal gross winner in 6 of 15 processes at a large national (P01, P03, P07, P08, P13, P14)."
- **Replace with:** "When B is cut to the RPA-audit realization range and D to the same range by analogy [I] (BD_FIELD), A becomes the modal gross winner in 6 of 15 processes at a large national (P01, P03, P07, P08, P13, P14). [V wave 37C]"

- **Find:** "This rests on h up to 0.80 and on m = 1. At m = 5 under BD_FIELD, C is modal in no process at a large national."
- **Replace with:** "This rests on h up to 0.80 and on m = 1. At m = 5 under BD_FIELD, C is modal in no process at a large national. The upper half of that h range (E15’s retrospective 0.78, State’s self-reported 80%) has not been cut to realized savings the way B and D were. If one common realization factor applied to A, B, C and D alike, the gross ranking would be the V1-priors one: A01 routing modal in P03 only, and assistance and routing-note routing in none [C]. [V wave 37C]"

- **Find:** "For A01 routing it is **$114k–$384k** at a large national, and $17k–$55k at a $1bn community foundation."
- **Replace with:** "For A01 routing it is **$100k–$384k** at a large national across BD_FIELD, BD_WIDE, BD_PROGRAM and ABD_FIELD ($7.4k under B_FIELD), and $16k–$55k at a $1bn community foundation. [V wave 37C]"

- **Find:** "h: the lower bound is the production bank's ~20% workload cut (CB-02); the upper bound is E15's computed 0.78 and State's 80%."
- **Replace with:** "h: the lower bound is the ~20% workload cut in the bank’s test set-up (CB-02: “Currently the bank is testing a set-up”); the upper bound is E15’s computed 0.78 (retrospective) and State’s self-reported 80%. [V wave 37C]"

- **Find:** "Field: triangular(0.07, 0.33, 1.00). The low end is the HUD program level, the mode is the GSA closeout bot and HUD's billing bots, and the top is a bot that meets its estimate (1 of 10 in the GSA sample)."
- **Replace with:** "Field: triangular(0.07, 0.33, 1.00). The low end is the HUD program level, the mode is the GSA closeout bot (the only GSA bot with a numeric ratio, about 30 of 90 minutes), and the top is a bot that meets its estimate (1 of 10 in the GSA sample). HUD’s billing-bot 33% is not used as support: it arises because a 500-hour estimate for all three bots was reported for each bot. [V wave 37C]"

- **Find:** "Three internal-billing bots: 33% of the reported estimate [F]."
- **Replace with:** "Three internal-billing bots: 33% of the reported estimate [F]. The 500-hour estimate covered all three bots combined but was reported for each (report p. 5) [F], so this is an over-report, not a realized-against-planned shortfall. [V wave 37C]"

- **Find:** "**Partly confirmed.** Cutting B and D to audited realization raises C's rank-first probability about sixfold (route m = 1: 0.012 → 0.072). The first beneficiary is A, whose prior is also unsourced. C becomes modal only with routing and either A recut too or the A01 h range."
- **Replace with:** "**Partly confirmed.** Cutting B to RPA-audit realization and D to the same range by analogy [I] raises C's rank-first probability about sixfold (route m = 1: 0.012 → 0.072). The first beneficiary is A, whose prior is also unsourced. C becomes modal only with routing and either A recut too or the A01 h range, whose upper half is not haircut. [V wave 37C]"

- **Find:** "(AML production 0.20; AML retrospective 0.78; document classification 0.65–0.80)."
- **Replace with:** "(AML in-bank testing 0.20; AML retrospective 0.78; document classification 0.65–0.80, an agency self-report and a pilot). [V wave 37C]"

### `research/mission-2026-11-14/g0401-g0502-ai-routing-and-per-grant.md`

- **Find:** "So C's last place in the ranking reflects the comparison set (uncalibrated B and D priors) and the amenable share a_p ≤ 0.6. It does not reflect how AI is deployed."
- **Replace with:** "So C's last place in the ranking reflects the comparison set (uncalibrated B and D priors) and the amenable share a_p ≤ 0.6. It does not reflect how AI is deployed. The B/D recut ([g0401-0103-ai-bd-recut.md](g0401-0103-ai-bd-recut.md)) only partly confirms this: cutting B and D to RPA-audit realization (D by analogy [I]) raises routing’s P(C first) from 0.012 to 0.072, but manual improvement (A), whose α is also an unsourced prior, becomes the modal winner in 6 of 15 processes. C becomes modal only if A is cut too or h runs up to 0.80 [S]. [V wave 37C]"

- **Find:** "C's weakness in ranking is therefore not an artefact of the assist formula. It comes from a_p ≤ 0.6 and from B and D's v1 priors."
- **Replace with:** "C's weakness in ranking is therefore not an artefact of the assist formula. It comes from a_p ≤ 0.6 and from the v1 priors of A, B and D: cutting B and D alone hands processes to A, not to C [S] ([g0401-0103-ai-bd-recut.md](g0401-0103-ai-bd-recut.md)). [V wave 37C]"

- **Find:** "2. **e is bounded, not measured.** E15's 10% is a share of true positives missed, and converting it to a per-closed-case rate needs alert prevalence. The E15 abstract does not report prevalence."
- **Replace with:** "2. **e is bounded, not measured.** E15's 10% is a share of true positives missed. The E15 full text gives the prevalence (“less than 3% of the alerted ones”, p. 3), which converts it to at most 0.39% per closed alert (about 0.77% at the baseline’s ~80% recall) [C] ([g0401-0103-ai-bd-recut.md](g0401-0103-ai-bd-recut.md) CB-01c). The 0.10 upper end therefore no longer rests on E15. [V wave 37C]"

- **Find:** "Upper end: E15, where auto-closing AML alerts would miss about 10% of true positives (a share of positives, not of closed alerts, so [I])"
- **Replace with:** "Upper end: E15, where auto-closing AML alerts would miss about 10% of true positives (a share of positives, not of closed alerts, so [I]; per closed alert E15 implies at most 0.39%, so the 0.10 now rests on the OCBC invoice benchmark’s 10% error budget, CB-04) [V wave 37C]"

### `research/mission-2026-11-14/gap19-ai-calibration.md`

- **Find:** "- 0.10: share of true AML positives missed if triage auto-closes (E15)."
- **Replace with:** "- 0.10: share of true AML positives missed if triage auto-closes (E15). This is 1 − recall, not a rate per AI-handled output: with E15’s prevalence (under 3% of alerts) it is at most 0.39% of auto-closed alerts [C] ([g0401-0103-ai-bd-recut.md](g0401-0103-ai-bd-recut.md)). [V wave 37C]"

### `research/mission-2026-11-14/strategic-synthesis.md`

- **Find:** "It still changes no process's most likely winner at h ≤ 0.49 [S] ([g0401-g0502-ai-routing-and-per-grant.md](g0401-g0502-ai-routing-and-per-grant.md); wave 36B) [V wave 36B]"
- **Replace with:** "It still changes no process's most likely winner at h ≤ 0.49 [S] ([g0401-g0502-ai-routing-and-per-grant.md](g0401-g0502-ai-routing-and-per-grant.md); wave 36B) [V wave 36B]. Cutting conventional automation to RPA-audit realization, and redesign to the same range by analogy [I], raises C's rank-first probability but hands most processes to manual improvement, whose prior is also unsourced. Assistance is still modal nowhere; routing becomes modal in 3 of 15 large-national processes only with h up to 0.80, taken from a retrospective study and an agency self-report that were not haircut [S]. E15 implies at most 0.39% missed per auto-closed AML alert, not 0.10 [C] ([g0401-0103-ai-bd-recut.md](g0401-0103-ai-bd-recut.md); wave 37C). [V wave 37C]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

Waves 37A and 37B insert §11.42 and §11.43 first (both were present at the time of the check); §11.44 goes immediately before the source register.

- **Find:** "\n---\n\n## Source register"
- **Replace with:** "\n### 11.44 AI economics: B and D held to C's evidence standard (validated, wave 37C)\n\n**AI economics: B and D held to C's evidence standard** (validated, wave 37C). The recut reproduces the calibrated and routing results exactly (large national: P(C first) 0.0021 and 0.0123; AI pools $445k and $1.36m). Two federal inspector-general audits support cutting conventional automation to realized savings: HUD realized 7% of its estimated RPA hours, and GSA found 9 of 10 sampled bots off estimate. But only one GSA bot yields a ratio (about 30 of 90 minutes), and HUD’s 33% billing-bot figure is an over-report. Applying the same range to redesign is an analogy [I]. Cutting B and D lifts assistance’s rank-first probability from 0.2% to 1.5%, yet it is still modal nowhere; manual improvement, itself an unsourced prior, becomes modal in 6 of 15 processes. Routing becomes modal in 3 processes only with h up to 0.80, drawn from a retrospective study and an agency self-report that were not haircut. E15’s full text puts prevalence below 3%, so its miss rate is at most 0.39% per auto-closed alert, not 0.10. The Bank of America yields compare different periods (repo [`validation-wave37c-report.md`](mission-2026-11-14/validation-wave37c-report.md)) [V wave 37C]\n\n---\n\n## Source register"
