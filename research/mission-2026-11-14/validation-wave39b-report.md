# Validation wave 39B: escaped-error detection probability (g0403-0104) and line 6 against Schedule D (g1915b-04)

*Independent validation, 2026-11-19. Validator: independent-validation-agent-wave39b. Register: [`data/mission-2026-11-14/validation-register-wave39b.csv`](../../data/mission-2026-11-14/validation-register-wave39b.csv) (36 claims).*

## Counts

| Study | Claims | Confirmed | Partially confirmed | Contradicted | Unverifiable |
|---|---:|---:|---:|---:|---:|
| 1. m inputs: IRS detection and OFAC (V39B-01 to V39B-19) | 19 | 13 | 5 | 1 | 0 |
| 2. Line 6 against Schedule D (V39B-20 to V39B-36) | 17 | 15 | 2 | 0 | 0 |
| **All** | **36** | **28** | **7** | **1** | **0** |

## Method

- **Retrieval.** One helper fetched every file with user agent `research-script/1.0`. It read each host's robots.txt with `urllib.robotparser` and logged every request. Hosts: www.irs.gov (robots 200; `/pub/` and `/statistics/` allowed), www.tigta.gov (200), ofac.treasury.gov (200; `/media/` and the enforcement pages allowed), www.dafresearchcollaborative.org (200; `/s/` allowed), gt990datalake-rawdata.s3.amazonaws.com (robots 404, no rules) and www.law.cornell.edu (200). No user agent was changed. Nothing was fetched from sec.gov, crt.sh or certspotter, and no one was contacted.
- **Reruns.** `python3 scripts/mission_m_detection_ofac.py . --route --efile-dir <IRS index dir> --out <scratch>` reproduced the 385-row CSV byte for byte in 19 s. `scripts/mission_line6_check.py` was run against a scratch root (symlinked inputs), so the repo was not written. Its CSV (md5 4535b051…) and JSON summary are byte-identical to the study's.
- **Re-fetched:** Data Book Table 3-5 (FY2021–25) and SOI Form 4720 Table 1 (CY2021–25); TE/GE Accomplishments Letters FY2021–24; TIGTA 2026-1S0-042 (Figure 5 on p. 9 was read as an image); the six OFAC year pages and all 15 release PDFs; the in-process compliance strategies page and Pub 5313; 26 U.S.C. §6501; both DAFRC technical appendices; `25eofinextractdoc.xlsx`; the Form 990 PDF (line 6 wording); and nine return XMLs. Those nine are Groundswell (amended and original TY2024, TY2023), Legacy Global, Mitchell Hamline, Jasper Ridge FY2022 and TIAA Charitable FY2021, plus a seeded random sample of 60 reverse-case returns. Ayco's FY2025 XML returned 404 on the mirror.

## Findings: Study 1 (escaped-error m inputs)

1. **The primary numbers hold.**
   - All 20 Data Book exam cells match exactly. So do the four SOI §4966 sponsor-tax counts and amounts (7, 15, 10, 6; $112,913, $179,819, $1,150,071, $101,894) and the CY2025 residual of $264,759.
   - So do the TE/GE filings examined (3,249 / 3,425 / 2,464 / 1,955) with their change rates, 87 OFAC page rows with no charity, and all 15 release penalties and counts.
   - The P bounds (0.001151 / 0.001846 / 0.009921) and every composite m reproduce.
2. **Contradicted: the FY2025 TE/GE count is quoted, not derived (V39B-06).**
   - TIGTA's Figure 5 (p. 9) gives **2,777** EO examination closures in FY2025, with 28% no change.
   - The study derives 2,762 from "15 percent fewer". The broad rate is 0.383%, not 0.381%. No P setting changes.
3. **The 723 figure is mis-described (V39B-07).** TIGTA's 723 is TE/GE's workforce reduction from January 2025 to January 2026 (about 32%), across voluntary separation, deferred resignation and other incentives. It is not deferred resignations in FY2025.
4. **"Every bound on P is an upper bound" holds only narrowly (V39B-10).**
   - q = 1 makes P an upper bound on the exam channel for a *randomly selected* filer, and nothing more.
   - Exams are not random: 34.1% / 35.3% / 39.6% / 37.5% of EO closures in FY2021–24 were picked up from a related examination (Pub 5329).
   - Large sponsors may be examined above the all-filer rate. The Data Book gives no size breakdown.
   - The incidence ratio 15 ÷ 1,512 bounds P only if every sponsor has at least one escaped taxable distribution a year. If errors are rarer, it bounds nothing.
   - Non-exam channels are excluded: press, state attorneys general, donor complaints and whistleblowers.
   - **Better framing:** 0.0012–0.0099 is average-filer exam coverage, a plausible central range, not a ceiling.
   - The substantive conclusion survives this. Tripling P leaves P07's m at 3.9 for a $40k grant, and the central composite at 1.58.
5. **The processor analogue includes a bank (V39B-13).**
   - American Express National Bank is a national bank, which §2.3's scope excludes.
   - Without it (n = 7), the processor median is **$95.62** (6.9 units), not $168.50. The maximum is $624.28 (45.0 units), not $2,011.68.
6. **The Amex case is more than one missed alert (V39B-14).**
   - The release cites "a combination of human error and sanctions compliance program deficiencies".
   - After the closed alert, a customer-care agent lifted the suspension, and a wrong re-suspension code let seven more transactions through.
   - So $430,500 (31,055 units) is an upper bound on the cost of a single missed alert.
7. **The composite 1.56 is fragile (V39B-17).**
   - §4.2 itself says a DAF sanctions miss is usually the missed-true-match kind.
   - Pricing P01/P14 at the Amex per-alert figure, with the same unsourced P_OFAC (0.01 / 0.1 / 1), gives composites of **13.7 / 128 / 1,269**.
   - The robust result is narrower: the §4966 excise channel is negligible (0.008 of the central m). The composite is not pinned down.
8. **Minor (V39B-18).** "≤ 0.035 in every cell" is 0.0353 at most.

## Findings: Study 2 (line 6 against Schedule D)

1. **Everything counted reproduces.**
   - Forward case: 44 returns, 35 EINs. 33 plausible returns (24 EINs) hold 13,374 accounts and $265,248,473.
   - Reverse case: 3,297 returns, 1,511 EINs.
   - The by-year table, the DAFRC treatment split (17 / 2 / 2 / 23), the EIN-level split (8 / 16), the SOI agreement (3,160 / 3 / 134) and the carry-forward ($53.2m / $358.0m / $453.8m / $1,771.4m) all match.
2. **The return XMLs re-read exactly.**
   - Groundswell's amended TY2024 return: 12,808 accounts, $10,084,314, `DonorAdvisedFundInd` 0, amended X, e-filed 2026-01-28.
   - Legacy Global FY2023: 347 accounts, $218,867,001, line 6 = 0.
   - Mitchell Hamline: 4 accounts, $4,266,549.
   - Groundswell's original TY2024 return (202513219349318726, e-filed 2025-11-17) and its TY2023 return have line 6 = 0 and no Part I DAF data.
   - That original came after DAFRC's 1 October 2025 cut-off. DAFRC's spring update replaced only submitted or imputed values (data available by 1 March 2026) and did not re-vet.
3. **DAFRC's rule and the SOI documentation are confirmed.**
   - The appendix selects on Part I(a) filing with at least $1 of DAF assets. Neither appendix mentions Part IV or line 6.
   - The SOI 990 extract has `dnradvisedfundscd` (Pt IV-6) and 32 Schedule A fields, but no Schedule D field.
4. **The reverse case overstates disagreement (V39B-31).**
   - Form 990 line 6 asks about donor advised funds "or any similar funds or accounts".
   - **567 reverse returns (226 EINs)** carry P-MOR-01's own status `flag_yes_other_funds_column_only`: they report Part I column (b), not (a). In the 60-return XML sample, 8 report column (b) > 0.
   - **341 more** report column (a) DAF contributions or grants but no or zero year-end count. These are wind-downs: Ayco FY2025, Jasper Ridge FY2022, and TIAA Charitable's final FY2021 return.
   - At most **2,389 returns (1,153 EINs)** show no Part I activity at all.
5. **The Ayco reading is right, and stronger than stated (V39B-32).**
   - Ayco's FY2025 return reports $408.1m of DAF contributions and $452.6m of DAF grants, with zero DAFs and zero total assets at year end.
   - Its line-6 "Yes" is correct, so this is not a reporting gap.
6. **The "floor" holds for counts but not for money (V39B-34).**
   - A count taken from a read subset cannot fall as more returns are read.
   - But 12 of the 14 plausible outside-panel rows are operating charities by the note's own reading. Long Island Children's Museum alone is $2.60m of $15.81m. So the figure is not a floor on missed DAF assets.
   - The batch-38 rate (5 plausible returns, $2,963,077, in 126,736 returns) is an estimate for the unread remainder, not a bound.
7. **The FY2024 non-DAFRC account arithmetic holds (V39B-35).** 11,992 + 12,808 = 24,800. P-MOR-01's FY2024 is already flagged incomplete.

## Exact corrections

### `research/mission-2026-11-14/g0403-0104-m-detection-ofac.md`

- **Find:** "| 2025 | 889 | 77 | 188 | 2,762 [C] | 594,022 | 1,596,231 | 0.150% | 0.056% | 0.381% |"
- **Replace with:** "| 2025 | 889 | 77 | 188 | 2,777 [F: TIGTA Figure 5, p. 9; 2,762 derived earlier] | 594,022 | 1,596,231 | 0.150% | 0.056% | 0.383% [V wave 39B]"

- **Find:** "Coverage is therefore not rising."
- **Replace with:** "Coverage is therefore not rising. Corrections: TIGTA’s Figure 5 (p. 9) quotes 2,777 EO examination closures in FY2025 (28% no change), so the FY2025 count need not be derived (limit 4); and 723 is TE/GE’s workforce reduction from January 2025 to January 2026 (about 32%) through voluntary separation, deferred resignation or other incentives (p. 5), not deferred resignations in FY2025 alone [F] [V wave 39B]"

- **Find:** "Press, whistleblower and state AG detection are not quantified."
- **Replace with:** "Press, whistleblower and state AG detection are not quantified. The settings are therefore upper bounds only for a randomly selected filer on the exam channel. Exams are not random: 34.1%–39.6% of EO closures in FY2021–24 were picked up from a related examination (Pub 5329), and large sponsors may be examined above the all-filer rate. The incidence ratio (15 ÷ 1,512) bounds P only if every sponsor has at least one escaped taxable distribution a year. Read 0.0012–0.0099 as average-filer exam coverage, not as a ceiling on P for a given sponsor; tripling it leaves the central composite at 1.58 [C/I] [V wave 39B]"

- **Find:** "As a sanctions-screening analogue for P01/P14 at a DAF sponsor, they are the nearest regime [I]."
- **Replace with:** "As a sanctions-screening analogue for P01/P14 at a DAF sponsor, they are the nearest regime [I]. American Express National Bank is a national bank, which §2.3 otherwise excludes; without it the processor group (n = 7) has median $95.62 (6.9 units) and maximum $624.28 (45.0 units) [C] [V wave 39B]"

- **Find:** "The penalty was $430,500 per missed alert, or **31,055 handling units**."
- **Replace with:** "The penalty was $430,500 per missed alert, or **31,055 handling units**. The release attributes the 214 transactions to “a combination of human error and sanctions compliance program deficiencies”: after the alert was closed, a customer-care agent lifted the suspension and an incorrect re-suspension code let seven more transactions through. So $430,500 prices one missed alert plus two later control failures, an upper bound per missed alert [F/I] [V wave 39B]"

- **Find:** "- **Proposed m for the routing model:** low 1.0, central **1.6–1.8**, high **9.3** with the OFAC analogue, or 55 if bank-SAR transfer is kept [I]."
- **Replace with:** "- **Proposed m for the routing model:** low 1.0, central **1.6–1.8**, high **9.3** with the OFAC analogue, or 55 if bank-SAR transfer is kept [I]. The OFAC figures assume per-violation pricing. Pricing P01/P14 at the Amex per-missed-alert figure (31,055 units), the kind §4.2 says fits a DAF sanctions miss, with the same unsourced P_OFAC gives composite m of 13.7 / 128 / 1,269 (low / central / high). The robust result is that the §4966 channel is negligible (0.008 of the central m); the composite is not pinned down [C] [V wave 39B]"

### `research/mission-2026-11-14/g0403-04-escaped-error-cost.md`

- **Find:** "That gap is why P is swept from 0.01 to 1."
- **Replace with:** "That gap is why P is swept from 0.01 to 1. [g0403-0104-m-detection-ofac.md](g0403-0104-m-detection-ofac.md) fills it: IRS exams reach 0.12%–0.30% of e-filed 990/990-EZ returns a year (FY2021–25), and at most 15 returns a year report the sponsor §4966 tax (CY2021–24). That puts P at about 0.0012–0.0099, which is average-filer exam coverage rather than a strict ceiling [C/I] [V wave 39B]"

- **Find:** "5. **Proposed m for the routing model (single m, weighted by AI-amenable pool):** **low 1.0, central 2.4, high 106** [I]."
- **Replace with:** "5. **Proposed m for the routing model (single m, weighted by AI-amenable pool):** **low 1.0, central 2.4, high 106** [I]. Superseded: wave 38B corrects these to 2.20 and 88.5 (P08 at its correction unit). g0403-0104 then bounds detection and lowers the central to 1.77 (bank-SAR transfer kept) or 1.56 (OFAC per-violation analogue), with high 55 or 9.3. Pricing a sanctions miss per missed alert (Amex 2022) instead gives a central of about 128, so the composite still turns on the unsourced P01/P14 terms [C/I] [V wave 39B]"

- **Find:** "- At the central m = 2.4, the routing pool is **$1.26m**, against $1.36m at m = 1 and $445k for assistance. C ranks first with probability 0.009."
- **Replace with:** "- At the central m = 2.4, the routing pool is **$1.26m**, against $1.36m at m = 1 and $445k for assistance. C ranks first with probability 0.009. At the wave-38B central of 2.20 the pool is $1.27m, and at g0403-0104’s 1.77 / 1.56 it is $1.31m / $1.32m [S] [V wave 39B]"

### `research/mission-2026-11-14/g0401-g0502-ai-routing-and-per-grant.md`

- **Find:** "Its central 2.4 is mostly assumption-driven, and at m = 2.42 the large-national routing pool is $1.26m [S]. [V wave 38B]"
- **Replace with:** "Its central 2.4 is mostly assumption-driven, and at m = 2.42 the large-national routing pool is $1.26m [S]. [V wave 38B] Corrected: the central is 2.20 (wave 38B, $1.27m). Bounding detection with IRS exam and SOI §4966 data lowers it to 1.56–1.77 ($1.31m–$1.32m). It is still assumption-driven, through operational rework and the P01/P14 sanctions term ([g0403-0104-m-detection-ofac.md](g0403-0104-m-detection-ofac.md)) [C/S] [V wave 39B]"

- **Find:** "Wave 38B bounds it at 1.0–106 (central 2.4), but detection probability, the bank-to-DAF transfer and operational rework remain unsourced (P-G0403-04). [V wave 38B]"
- **Replace with:** "Wave 38B bounds it at 1.0–106 (central 2.4), but detection probability, the bank-to-DAF transfer and operational rework remain unsourced (P-G0403-04). [V wave 38B] After wave 38B’s P08 correction the range is 1.0–88.5 (central 2.20). Detection probability is now bounded from IRS data at 0.0012–0.0099 (average-filer coverage), which lowers the central to 1.56–1.77. The bank-transfer or sanctions-pricing term and operational rework remain unsourced [V wave 39B]"

### `research/mission-2026-11-14/g0401-0103-ai-bd-recut.md`

- **Find:** "The DAF excise regime gives 1–174 units per escaped P07/P08 error, and the composite central m is 2.4 [C/I]. [V wave 38B]"
- **Replace with:** "The DAF excise regime gives 1–174 units per escaped P07/P08 error, and the composite central m is 2.4 [C/I]. [V wave 38B] P08 carries no sponsor tax, so the composite central is 2.20. With IRS-bounded detection (P ≈ 0.0018), an escaped P07 error costs about 1.02 units at a $5,100 grant, and the central m is 1.56–1.77 [C/I] [V wave 39B]"

### `research/mission-2026-11-14/strategic-synthesis.md`

- **Find:** "Wave 38B bounds m at 1.0–106 with a mostly assumption-driven central 2.4 ($1.26m)."
- **Replace with:** "Wave 38B bounds m at 1.0–88.5 with a mostly assumption-driven central of 2.20 ($1.27m). Bounding detection with IRS exam and SOI §4966 data lowers the central to 1.56–1.77 ($1.31m–$1.32m), though pricing a sanctions miss per missed alert would raise it to about 128 [C/S] [V wave 39B]"

### `research/mission-2026-11-14/FINAL-STATUS.md`

- **Find:** "For DAF sponsors the central m is about 2.2, resting mostly on assumptions."
- **Replace with:** "For DAF sponsors the central m is about 2.2 (wave 38B). Bounding IRS detection (P ≈ 0.0012–0.0099) lowers it to 1.56–1.77, and it rests mostly on unsourced operational-rework and sanctions-pricing assumptions [V wave 39B]"

- **Find:** "Wave 38B's central m is 2.4, but bank-style compliance errors that escape would erase the gain."
- **Replace with:** "The central m is 2.20 after wave 38B’s correction (it was given as 2.4), and IRS-bounded detection lowers it to 1.56–1.77. Bank-style compliance errors that escape, or sanctions misses priced per missed alert, would still erase the gain [V wave 39B]"

### `research/mission-2026-11-14/g1915b-04-line6-vs-schedule-d.md`

- **Find:** "returns from 1,511 EINs, FY2021–FY2026.**"
- **Replace with:** "returns from 1,511 EINs, FY2021–FY2026.** Not all are disagreements. Line 6 also asks about “any similar funds or accounts”, and at least 567 of these returns (226 EINs) are P-MOR-01’s “other funds column only” rows, which fill Schedule D Part I column (b) instead of (a); in a 60-return XML sample, 8 had column (b) > 0. A further 341 report column (a) DAF contributions or grants with no or zero year-end count, as a sponsor winding down would (Ayco FY2025, Jasper Ridge FY2022, TIAA Charitable FY2021). At most 2,389 returns (1,153 EINs) show no Part I activity at all [C] [V wave 39B]"

- **Find:** "while 2,720 EINs report accounts > 0."
- **Replace with:** "while 2,720 EINs report accounts > 0. Part of the gap is column-(b) filers whose “Yes” is correct under line 6’s “similar funds or accounts” wording, so what is over-counted is DAF sponsors, not wrong answers [I] [V wave 39B]"

- **Find:** "Ayco's FY2025 return reports zero DAFs at year end, so for Ayco a carry-forward is wrong."
- **Replace with:** "Ayco's FY2025 return reports zero DAFs at year end, so for Ayco a carry-forward is wrong. Its line 6 “Yes” is also correct: the return reports $408.1m of DAF contributions and $452.6m of DAF grants during the year, with zero DAFs and zero total assets at year end. It is a wind-down, not a reporting gap [F] [V wave 39B]"

- **Find:** "**The forward counts are therefore a floor.**"
- **Replace with:** "**The forward counts are therefore a floor** on returns that put a count in Part I column (a) while answering “No”. They are not a floor on DAF assets missed: most plausible outside-panel rows are operating charities (Long Island Children’s Museum alone is $2.60m of the $15.81m). The batch-38 rate (5 plausible returns, $3.0m, in 126,736 large-filer returns) is an estimate for the unread remainder, not a bound [I] [V wave 39B]"

- **Find:** "The filer may not be vetted (Groundswell had no FY2023 Part I and its FY2024 Part I arrived by amendment on 2026-01-28), or it may not be a sponsor."
- **Replace with:** "The filer may not be vetted (Groundswell had no FY2023 Part I and its FY2024 Part I arrived by amendment on 2026-01-28), or it may not be a sponsor. Groundswell’s original TY2024 return (202513219349318726) was e-filed on 2025-11-17, after DAFRC’s 1 October 2025 cut-off, with line 6 = 0 and no Part I. The spring 2026 update replaced only submitted or imputed values with data available by 1 March 2026 and did not re-vet [F] [V wave 39B]"

### `research/mission-2026-11-14/full-universe-990-harvest-and-corrected-totals.md`

- **Find:** "file a 990-EZ (no Schedule D) or file on paper are invisible (proposal P-99F-03)."
- **Replace with:** "file a 990-EZ (no Schedule D) or file on paper are invisible (proposal P-99F-03). Reading Schedule D directly ([g1915b-04-line6-vs-schedule-d.md](g1915b-04-line6-vs-schedule-d.md)) finds 14 plausible line-6 “No” returns outside the panel in FY2021–26 (12,863 accounts, $15.81m). The FY2021–24 part is 7 returns and $10.83m, 93% of it Groundswell. The asset totals do not move, but FY2024 non-DAFRC accounts roughly double, from 11,992 to about 24,800 [C] [V wave 39B]"

- **Find:** "FY2025 (172 rows) is partial and not shown."
- **Replace with:** "FY2025 (172 rows) is partial and not shown. The FY2024 account total (11,992) excludes Groundswell Charitable Foundation’s 12,808 accounts, which appear only on an amended return e-filed 2026-01-28 that answers line 6 “No” [F] [V wave 39B]"

### `research/mission-2026-11-14/direction-long-tail-sponsors.md`

- **Find:** "file a 990-EZ or file on paper are invisible."
- **Replace with:** "file a 990-EZ or file on paper are invisible. Reading Schedule D directly adds 14 plausible line-6 “No” returns outside DAFRC in FY2021–26 ($15.81m, most of it Groundswell’s $10.08m in FY2024), so the asset picture holds, but FY2024 non-DAFRC accounts roughly double (11,992 to about 24,800) [C] [V wave 39B]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

- **Find:** "\n---\n\n## Source register"
- **Replace with:** "\n### 11.49 Detection probability, OFAC analogue and the line 6 filing gap (validated, wave 39B)\n\n**Detection probability, OFAC analogue and the line 6 filing gap** (validated, wave 39B). IRS Data Book Table 3-5 confirms 666–1,383 Form 990/990-EZ/990-N examinations a year in FY2021–25, about 0.12%–0.30% of e-filed 990 and 990-EZ returns. SOI’s Form 4720 study confirms at most 15 returns a year reporting the sponsor §4966 tax (CY2021–24, $0.10m–$1.15m a year). These put the chance that an escaped DAF error is detected and taxed near 0.1%–1%. That is average-filer exam coverage, not a strict ceiling: exams are partly targeted, and the incidence bound assumes an escaped error at every sponsor. With it, the central escaped-error m falls from 2.20 to 1.56–1.77. But pricing a sanctions miss per missed alert (Amex 2022, $430,500) instead of per violation gives about 128, so m still turns on unsourced terms. No OFAC penalty from 2021 to 2026 names a charity. On filings, 44 Form 990s answer line 6 “No” while reporting DAF accounts. DAFRC selects on Schedule D, not line 6, and misses only $10.83m in FY2021–24, 93% of it Groundswell. Of 3,297 “Yes” returns without Part I accounts, at least 567 report “similar funds” in column (b) instead, so many are not errors. [V wave 39B]\n\n---\n\n## Source register"

## Notes for the integrator

- Every Find was checked by script against the current files and occurs exactly once (see the check below). Values use curly quotes; Finds contain no straight double quotes.
- Wave 39A may insert §11.48 before this item. The anchor `\n---\n\n## Source register` is unique, so applying 39A first leaves this Find intact.
- Not proposed as corrections, but noted in the register: the forward table's FY2025 "outside DAFRC" column includes two panel members with no FY2025 row (V39B-25), and max P(C first) is 0.0353 (V39B-18).
