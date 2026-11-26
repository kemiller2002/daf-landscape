# Validation wave 45B: Schedule A excess over 2% (b40n1202-b43n26-01) and Canada carry-forward (b3946-02)

**Date:** 2026-11-20 · **Validator:** validator wave 45B · **Register:** [`validation-register-wave45b.csv`](../../data/mission-2026-11-14/validation-register-wave45b.csv) (25 rows, V45B-01 to V45B-25)

**What was done**
- **Study 1.** Re-ran `scripts/mission_schedule_a_excess.py` cache-only (`sa01/schA`, `q1226/f990p8`, `rcp/bmf`) in a scratch copy of the repo, so no repo file was written. The CSV came out byte-identical (md5 0d880582624a8c9a790d5355f62c7f52). Recomputed the sponsor-status join, the in-kind concentration, the line-5 zero split and the shares above 100% from the CSV and cache with my own code. Re-fetched 16 Schedule A returns from the GivingTuesday mirror (robots.txt 404) and parsed them independently. Fetched the IRS Schedule A instructions (www.irs.gov robots.txt 200; `/instructions/` not disallowed). I also read the regulation text: ecfr.gov returned an unblock page and its API path is disallowed, so I read it through law.cornell.edu (robots.txt allows `/cfr/`; crawl-delay 10 respected).
- **Study 2.** Re-ran the study's command with `--out` and `--summary` sent to scratch. The CSV came out byte-identical (md5 93dd0f4c04d6b754a16d2ae019f6ef06). Checked the raw Schedule 6, Sections A–C and Schedule 8 rows for Brandon, Brampton, St. Kevin's and Pemberton. I made 4 requests to open.canada.ca, at least 21 s apart (robots.txt `Crawl-delay: 20`): robots.txt, two CKAN searches and the 2022 Schedule 8 file. I read s.149.1 at laws-lois.justice.gc.ca (robots.txt 404), in the current text and the parent pass's 2022-11-17 point-in-time copy. www.canada.ca timed out from this session.
- All scripts ran with `python3 -B` (one `-I` for scratch tools). User agent `research-script/1.0`. No outreach, logins or forms. sec.gov, crt.sh and certspotter were not used.

## Counts

| Study | Rows | confirmed | partially confirmed | contradicted | unverifiable |
|---|---|---|---|---|---|
| 1. Schedule A excess (b40n1202-b43n26-01) | 14 | 10 | 4 | 0 | 0 |
| 2. Canada carry-forward (b3946-02) | 11 | 8 | 3 | 0 | 0 |
| **Total** | **25** | **18** | **7** | **0** | **0** |

## Findings

### Study 1: Schedule A excess over 2%

1. **Every number reproduces.** The rerun is byte-identical. All figures checked match the CSV and the rerun JSON:
   - Part II filers: 1,496 respondents, 54,914 weighted, 84.34% of the numerator.
   - Line 1(e) ÷ 1h quartiles are 1.0 / 1.0 / 1.0.
   - Large-donor share: pooled 18.47%, median 1.81%.
   - Net DAF share: all in-scope 13.04%, Part II 13.94%.
   - Line 5 = 0 for 46.07% of Part II filers.
   - Net shares above 100%: 4.95% rising to 6.89%.
   - FOUNDATION 15 holds 98.37% of top-50 DAF grants.
   - The 1f baseline equals the committed `b6_1f` point estimates: median 0.0808679, pooled 0.11043.
2. **The premise is right as a quote, but incomplete (V45B-01).**
   - **What the instructions say.** Part II line 5 says the 2% limit "doesn’t apply to contributions from organizations qualifying as publicly supported organizations under section 170(b)(1)(A)(vi)" or governmental units.
   - **What the regulation adds.** Treas. Reg. §1.170A-9(f)(6)(i) makes that exemption "except as provided in paragraph (f)(6)(v)". Paragraph (f)(6)(v) removes it where the grant represents amounts "expressly or impliedly earmarked by a donor to such governmental unit or section 170(b)(1)(A)(vi) organization as being for, or for the benefit of, the particular organization". This is the agent-or-conduit rule.
   - **DAFs are not addressed.** The instructions do not repeat this rule and do not mention donor-advised funds in the line 5 text. Neither text says whether donor advice on a DAF grant counts as implied earmarking.
   - **Consequences.**
     - The 98.4% (vi) share is an upper bound on the DAF dollars that stay outside line 5.
     - A filer that attributes DAF grants to the advising donor is following a defensible reading of the regulation. It is not simply departing from practice, as limit 3 implies.
     - Under either reading, DAF grants are treated as coming from the sponsor only when no earmarking is found.
3. **Small number fixes.**
   - **In-kind share.** The four in-kind charities hold 23.64% of the weighted excess. That rounds to 23.6%, not 23.5%; 23.5% is the sum of the rounded components.
   - **Sponsor total.** $49.85bn is the FOUNDATION 15 amount, out of $50.68bn for the top 50 as a whole.
   - **Confidence intervals.** The 1f-row CIs (6.9–9.8% and 9.7–12.4%) differ from the parent's (6.4–9.7% and 9.8–12.5%), because the bootstrap seeds differ. Only the point estimates reproduce "exactly".
   - **Baseline for 13.9%.** The like-for-like baseline is Part II's 1f pooled share of 11.4%, not 11.04%.
4. **Line 5 = 0 splits two ways.** Of the 46.1%:
   - 31.1 points (368 recipients) have no `SubstantialContributorsTotAmt` element in any matched return;
   - 15.0 points (132) file an explicit 0.
   - The denominator is all 1,496 Part II recipients, including 12 with 1f ≤ 0.
5. **XML spot-check: 16 of 16 match.** These were 12 Part II returns (including Feeding America, Good360 and Grounded Solutions), 2 Part III and 2 with no support schedule. For each, line 1(e), line 1(f), line 5 and the Part III lines in the IRS XML equal the cache.
6. **The five-year-ratio method is sound as a central estimate (V45B-12).**
   - Line 1 includes government grants, which are exempt from the 2% limit. Because the ratio is applied to an equally inclusive line 1(e), the dollar estimate stays consistent.
   - The avg and all variants bracket the window assumption.
   - Two unsigned biases remain:
     - one-off gifts in years t−4 to t−1 inflate year t, and a large gift in year t is spread back across the window;
     - the cap at 1f assumes the excess sits in 1f and not in 1a–1d. This second bias is not stated in the study.
7. **The framing is mostly carried, but the label overstates (V45B-13).**
   - §0 has a clear "What the net figure means" bullet, and limit 1 says plainly that this is "not an individual-only share".
   - However, §0 and §2.2 call E the "large-donor share of 1f". E is only the above-2% excess, a floor on large-donor money (limit 2). The headline label should say so.
8. **Propagation.** Grepping for `b6_1f`, "1f basis" and "individual-only" finds two places in the parent study that need the result: the "1f alone" bullet (line 23) and §5 item 1, which still says Schedule A "was not parsed". The industry report mentions line 1f only in the wave 34B §11 paragraph, which is left alone, so a new §11.66 carries the result.

### Study 2: Canada carry-forward

1. **Every headline count reproduces.**
   - Previous-release line 865: 10 of 22 (C$556,228).
   - Schedule 8 only: 11.
   - Filed returns: 13 (C$662,419; C$1,810,425 uncovered).
   - Proxy, unscreened: 17 (C$223,589 uncovered).
   - Proxy, screened: 16 (C$1,342,412 covered; C$1,134,291 uncovered).
   - Total shortfall: C$2,494,652.
   - The lookback depths (13 / 8 / 1) and the verdict split (13 / 3 / 2 / 4) also match.
2. **Header-only files, and no 2026 release.**
   - The cached 2019–2022 Schedule 8 files are header-only. I re-downloaded the 2022 file: 88 bytes, header only.
   - CKAN lists 36 "List of charities" datasets, for 1990–2025. A second search ("charities 2026") returns no 2026 title.
3. **Brampton is confirmed.** In 2023 the DQ was C$440,622 against spending of C$1,482,345, an excess of C$1,041,723. The 2024 shortfall of C$144,218 leaves a pool of C$897,505, which covers the 2025 shortfall of C$68,344.
4. **The nil-quota reading matches the statute, but the inputs are fragile (V45B-20).**
   - **The statute.** In the current text (to 2026-10-29), DQ paragraph (c) is "in any other case, nil". Subsection (21) defines the excess as spending that "exceeds its disbursement quota for the year". So in a year with line 5850 = N, all qualifying spending is literally a disbursement excess.
   - **The inputs.** Line 5850 is self-reported, and later filings strain both rescues:
     - St. Kevin's Parish answered N for 2023 and 2024. Yet its 2025 Schedule 8 line 805 is a round C$5,000,000 (its line 870 reads 5), and its total assets rose from C$1.08m to C$5.70m.
     - Pemberton's 2025 line 5900, covering April 2022 to March 2024, is C$37,966. That is above its C$25k threshold.
   - Whether the CRA accepts excesses from nil-quota years is unverified, because canada.ca was unreachable. The robust filed count is 11 of 22.
5. **Old-rate excesses: a reasonable literal reading (V45B-21).** Subsections (20) and (21) read word for word the same in the 2022-11-17 and current texts, and s.149.1 itself sets no transitional limit. Not checked: the application provisions of the amending Acts, and the text in force for the FPE 2020–2021 years.
6. **The Brandon screen is justified, but a third reading fits better (V45B-22).**
   - **The data.** Line 5900 is C$2,409,770 (2020) and C$2,536,352 (2021), against C$74,229,087 in 2022 and total assets of C$73.2m, C$81.5m and C$73.2m.
   - **A pattern.** Both low values are close to 3.5% of the property: they imply bases of C$68.9m and C$72.5m, rising towards the 2022 figure.
   - **If line 5900 holds the quota instead:**
     - the 2020–2021 excesses are C$630,293 and C$530,355;
     - the FIFO pool at 2025 is C$694,092;
     - Brandon is partly covered, with C$216,610 left;
     - total uncovered dollars are C$0.44m;
     - 16 of 22 sponsors are still fully covered.
   - This reading sits between the screened (C$1.13m) and unscreened (C$0.22m) results, and should be reported alongside them.
7. **The payout and both quota formulas are confirmed.**
   - The netted payout is 12.0455% (586 sponsors, C$15.39bn). It is 12.20% without the 22 sponsors and 12.10% without the 6, and 12.053% if the uncovered dollars were paid out.
   - **Pre-2023 DQ.** The 2022-11-17 text is "A × B × 0.035/365", with B nil at or below C$100k / C$25k. The script matches this except for the A/365 day-count factor, which is stated in the limits.
   - **Post-2023 DQ and line 5850.** These match the current text and the data dictionary.

## Accept / modify / reject

| Claim | Decision | Note |
|---|---|---|
| S1 premise: (vi) and governmental grants are exempt from the 2% limit | **Modify** | Add the regulation's earmarking exception. The 98.4% becomes an upper bound on exempt DAF dollars. |
| S1 98.4% of top-50 DAF grants from FOUNDATION 15 sponsors | Accept (wording) | $49.85bn of $50.68bn |
| S1 Part II filers hold 84.3% of the numerator | Accept | |
| S1 line 1(e) = 1h | Accept | |
| S1 large-donor share 18.5% pooled / 1.8% median | Accept (relabel) | It is the above-2% excess, a floor |
| S1 net DAF share 13.0% / 13.9% | Accept | Not individual-only. The Part II baseline is 11.4%. |
| S1 in-kind charities hold 23.5% | **Modify** | 23.6% |
| S1 46.1% report line 5 = 0 | Accept (add split) | 31.1 points absent, 15.0 points explicit 0 |
| S1 shares above 100%: 5.0% → 6.9% | Accept | |
| S1 five-year-ratio method | Accept | Add the 1a–1d cap caveat (in this report only) |
| S1 headline framing | **Modify** | Relabel E; carry the result into the parent study |
| S2 13 / 16 of 22; C$1.13m uncovered | Accept | 11 of 22 is the robust filed count |
| S2 2019–2022 Schedule 8 files header-only | Accept | |
| S2 no 2026 release | Accept | |
| S2 Brampton | Accept | |
| S2 nil-quota reading | Accept (flag) | Literal text holds; the 5850 inputs are fragile |
| S2 pre-2023 excesses carry forward | Accept (flag) | Literal reading; CRA guidance unverified |
| S2 Brandon screen | **Modify** | Report the third reading (C$216,610 left; C$0.44m uncovered) |
| S2 12.05% payout unchanged | Accept | |
| S2 pre-2023 quota formula | Accept | |

## Limits

- I did not rebuild the bootstrap independently. The CIs rest on the byte-identical rerun.
- The CRA's administrative position on nil-quota and old-rate excesses was not checked, because www.canada.ca timed out.
- The regulation was read on law.cornell.edu, not ecfr.gov, because ecfr.gov served an unblock page and its API path is disallowed by robots.txt.
- The Brandon "quota on line 5900" reading is an inference from the numbers. Nothing in the filing labels it.

## Source register

| Source | URL | Accessed |
|---|---|---|
| IRS, Instructions for Schedule A (Form 990) (2025) | https://www.irs.gov/instructions/i990sa | 2026-11-20 |
| 26 CFR 1.170A-9 (LII copy of eCFR) | https://www.law.cornell.edu/cfr/text/26/1.170A-9 | 2026-11-20 |
| IRS e-file XML, GivingTuesday mirror (16 returns) | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml | 2026-11-20 |
| IRS EO BMF (cached) | https://www.irs.gov/pub/irs-soi/eo1.csv | Last-Modified 2026-11-09 |
| Income Tax Act s.149.1, current to 2026-10-29 | https://laws-lois.justice.gc.ca/eng/acts/I-3.3/section-149.1.html | 2026-11-20 |
| Income Tax Act, point-in-time 2022-11-17 (parent-pass copy) | https://laws-lois.justice.gc.ca/eng/acts/I-3.3/20221117/P1TT3xt3.html | 2026-11-20 (cached) |
| CKAN "List of charities" search | https://open.canada.ca/data/api/3/action/package_search?q=%22List%20of%20charities%22&rows=50 | 2026-11-20 03:40 UTC |
| CRA 2022 Schedule 8 file | https://open.canada.ca/data/dataset/b2acb3be-c720-4329-a8c0-d4d36c8db61e/resource/cea1f612-e919-4c3c-a401-21ca1a4ef415/download/schedule_8_dq_2022_updated.csv | 2026-11-20 03:40 UTC |
| CRA open-data dictionary v2.0 (cached) | https://open.canada.ca/data/dataset/05b3abd0-e70f-4b3b-a9c5-acc436bd15b6/resource/19375510-2919-480c-8f8c-e8721d285b72/download/open-data-data-dictionary-v2.0_eng.pdf | cached |

## Exact corrections

### `research/mission-2026-11-14/b40n1202-b43n26-01-schedule-a-excess.md`

**Find:** "or from governmental units [P]."
**Replace with:** "or from governmental units [P]. The regulation behind this, Treas. Reg. §1.170A-9(f)(6)(i) and (v), withdraws the exemption where the grant represents amounts “expressly or impliedly earmarked by a donor” to the (vi) organisation for the particular recipient. Neither text says whether donor advice on a DAF grant is such earmarking, so the (vi) share below is an upper bound on the DAF dollars that stay outside line 5 [P/I]. [V wave 45B]"

**Find:** "FY2024 DAF grants ($49.85bn): 47 of the 50 sponsors [F]."
**Replace with:** "FY2024 DAF grants ($49.85bn of $50.68bn): 47 of the 50 sponsors [F]. [V wave 45B]"

**Find:** "- **Large-donor share of 1f (central, current-year allocation)** [F]:"
**Replace with:** "- **Large-donor share of 1f (central, current-year allocation; this is the above-2% excess only, a floor on large-donor money)** [F]: [V wave 45B]"

**Find:** "together hold 23.5% of the weighted Part II excess."
**Replace with:** "together hold 23.6% of the weighted Part II excess (the rounded components in §2.4 sum to 23.5%). [V wave 45B]"

**Find:** "reproduces the committed `b6_1f` figures exactly (median 8.09%, pooled 11.04%)."
**Replace with:** "reproduces the committed `b6_1f` figures exactly (median 8.09%, pooled 11.04%). Only the point estimates match. The bootstrap intervals differ from the parent’s (6.4–9.7% and 9.8–12.5%) because the seeds differ. [V wave 45B]"

**Find:** "4. **Line 5 = 0 for 46.1% of Part II filers (weighted).**"
**Replace with:** "4. **Line 5 = 0 for 46.1% of Part II filers (weighted).** Of these, 31.1 points (368 recipients) have no line 5 element in any matched return, and 15.0 points (132) file an explicit 0. [V wave 45B]"

**Find:** "A filer may attribute DAF grants to the advising donor, or a sponsor may not be (vi)."
**Replace with:** "A filer may attribute DAF grants to the advising donor, or a sponsor may not be (vi). Treas. Reg. §1.170A-9(f)(6)(v) supports the first where donor advice counts as implied earmarking. [V wave 45B]"

### `research/mission-2026-11-14/b40n1202-b43n26-recipient-basis-and-rating-eligibility.md`

**Find:** "- **Narrowest basis, 1f alone:** median 8.1% (6.4–9.7%), pooled 11.0% (9.8–12.5%) [F]."
**Replace with:** "- **Narrowest basis, 1f alone:** median 8.1% (6.4–9.7%), pooled 11.0% (9.8–12.5%) [F]. Net of the Schedule A Part II line 5 excess over 2% (central allocation), these are 8.9% and 13.0%, and 12.0% and 13.9% for Part II filers. That is the DAF share of contributions from donors below the 2% limit, not an individual-only share ([b40n1202-b43n26-01-schedule-a-excess.md](b40n1202-b43n26-01-schedule-a-excess.md)). [V wave 45B]"

**Find:** "and the Schedule A Part II and III support lines were not parsed (P-B40N1202-B43N26-01)."
**Replace with:** "and the Schedule A Part II and III support lines were not parsed here. They are parsed in [b40n1202-b43n26-01-schedule-a-excess.md](b40n1202-b43n26-01-schedule-a-excess.md): the line 5 excess over 2% is 18.5% of Part II filers’ 1f pooled (median 1.8%). Netting it out does not isolate individual giving, because grants from 170(b)(1)(A)(vi) organisations and each large donor’s first 2% stay in. [V wave 45B]"

### `research/mission-2026-11-14/b3946-02-canada-carry-forward.md`

**Find:** "If they were kept, Brandon would be covered, and uncovered dollars would fall to C$0.22m (17 of 22 covered)."
**Replace with:** "If they were kept, Brandon would be covered, and uncovered dollars would fall to C$0.22m (17 of 22 covered). Another reading fits the figures. The two values (C$2,409,770 and C$2,536,352) are close to 3.5% of the property, implying bases of C$68.9m and C$72.5m that rise towards the C$74.2m filed for 2022. Read that way, those values are the old DQs and the 2020–2021 excesses are C$630,293 and C$530,355. Brandon is then partly covered, with C$216,610 left, uncovered dollars total C$0.44m, and 16 of 22 are still fully covered [I]. [V wave 45B]"

**Find:** "Treating all spending in a nil-DQ year as an excess is the literal text of s.149.1(21)."
**Replace with:** "Treating all spending in a nil-DQ year as an excess is the literal text of s.149.1(21). The DQ definition’s paragraph (c) is “nil”, and (21) counts spending that “exceeds its disbursement quota for the year”. But line 5850 is self-reported. St. Kevin’s Parish answered N for 2023 and 2024, yet its 2025 line 805 is a round C$5,000,000 and its total assets rose from C$1.08m to C$5.70m. Pemberton’s 2025 line 5900 (April 2022 to March 2024) is C$37,966, above its C$25k threshold. [V wave 45B]"

**Find:** "as worded in both versions, not confirmed CRA guidance [I]."
**Replace with:** "as worded in both versions, not confirmed CRA guidance [I]. Subsections (20) and (21) read word for word the same in the 2022-11-17 and current texts, and s.149.1 itself sets no transitional limit. The amending Acts’ application provisions and the text in force for FPE 2020–2021 were not checked. [V wave 45B]"

### `research/mission-2026-11-14/b39n3-0406-canada-netting-dq.md`

**Find:** "10 of the 22 are covered by an excess shown in their 2024-release return."
**Replace with:** "10 of the 22 are covered by an excess shown in their 2024-release return. Adding 2023 Schedule 8 excesses and nil-quota years gives 13 of 22 on filed returns. A pre-2023 proxy gives 16 of 22, leaving C$1.13m uncovered ([b3946-02-canada-carry-forward.md](b3946-02-canada-carry-forward.md)). [V wave 45B]"

**Find:** "Whether older excesses cover them is open (P-B3946-02)."
**Replace with:** "Followed up in [b3946-02-canada-carry-forward.md](b3946-02-canada-carry-forward.md): Brampton and Caledon CF is covered by its 2023 excess, Fredericton CF and Collège de l’Assomption only with a pre-2023 proxy, and Caritas-Sherbrooke partly. Brandon, Lithuanian and Rogan are not covered. [V wave 45B]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

**Find:** "\n---\n\n## Source register"
**Replace with:** "\n\n### 11.66 Schedule A 2% excess; Canadian carry-forwards (validated, wave 45B)\n\n**Schedule A 2% excess; Canadian quota carry-forwards** (validated, wave 45B). Both studies reproduce byte for byte. Netting each recipient’s Schedule A Part II line 5 excess over 2% out of line 1f raises the pooled top-50 DAF share from 11.0% to 13.0% (Part II filers: 11.4% to 13.9%). That is the DAF share of contributions from donors below the 2% limit, not an individual-only share. The excess is 18.5% of Part II filers’ 1f pooled (median 1.8%). It is a floor on large-donor money, and four in-kind charities hold 23.6% of it. The IRS instructions exempt grants from 170(b)(1)(A)(vi) organisations, which make 98.4% of top-50 DAF grants. Treas. Reg. §1.170A-9(f)(6)(v) withdraws that exemption for amounts “expressly or impliedly earmarked by a donor”, so filers may treat DAF grants differently. In Canada, 13 of 22 sponsors in quota shortfall are covered on filed returns, or 16 with a pre-2023 proxy, leaving C$1.13m uncovered. Two nil-quota rescues rest on self-reported line 5850. Brandon’s screened 2020–21 line 5900 looks like 3.5% of its property; read that way, C$216,610 of its shortfall stays uncovered (C$0.44m in all). The 12.05% netted payout is unchanged (repo [`validation-wave45b-report.md`](mission-2026-11-14/validation-wave45b-report.md)) [V wave 45B]\n\n---\n\n## Source register"
