# Validation wave 33A: DAF share of recipient revenue, long-tail operating cost, processor disbursement rules

**Validator:** independent-validation-agent-wave33a · **Validated on:** 2026-11-19 · **Register:** [`validation-register-wave33a.csv`](../../data/mission-2026-11-14/validation-register-wave33a.csv) (46 claims, V33A-01 to V33A-46)

**Studies checked**
1. [b40n12-daf-share-of-recipient-revenue.md](b40n12-daf-share-of-recipient-revenue.md) (P-B40N12-02). Claims V33A-01 to -16.
2. [b45n33-long-tail-operating-cost.md](b45n33-long-tail-operating-cost.md) (P-B45N33-02). Claims V33A-17 to -30.
3. [g1913-processor-disbursement-rules.md](g1913-processor-disbursement-rules.md) (P-G1913-04). Claims V33A-31 to -46.

**Method.** Both scripts were re-run with outputs written to scratch only (`scratchpad/v33a/`). The long-tail script writes to `<root>/data/...`, so it was given a scratch root that symlinks its two inputs. The recipient-revenue script ran with `--out` set to scratch. Before reading each note's conclusions, I recomputed the headline figures from the CSVs with independent code: weighted quantiles, a Taylor-linearised ratio variance, a certainty-fixed bootstrap, and sensitivity cuts.

Primary documents were re-fetched with user agent `research-script/1.0` after a robots.txt check (404 or 410 read as allowed; any other non-200 read as disallowed):
- 16 IRS e-file XMLs (GivingTuesday mirror) for 8 sampled recipients;
- 3 sponsor XMLs (Community Foundation of the Fox, Henry County CF, Fidelity);
- 22 processor rule pages and PDFs;
- 2 Chariot pages.

No crt.sh, certspotter or sec.gov. No outreach. Evidence is 2021 or later.

## Summary counts

| Result | Study 1 (recipient share) | Study 2 (long-tail cost) | Study 3 (processor rules) | Total |
|---|---|---|---|---|
| confirmed | 9 | 11 | 12 | **32** |
| partially_confirmed | 5 | 3 | 3 | **11** |
| contradicted | 2 | 0 | 1 | **3** |
| unverifiable | 0 | 0 | 0 | **0** |
| **Total** | 16 | 14 | 16 | **46** |

## Findings

### Study 1: DAF share of recipient revenue (P-B40N12-02)

**Reproduces exactly.**
- The re-run CSV is byte-identical to the committed file after sorting (V33A-01).
- The median of 5.9% (5.3–7.4%), the pooled share of 6.9%, P25 2.2% and P75 16.5% all recompute from the CSV.

**Intervals are sound and slightly conservative.**
- An independent Taylor-linearised stratified interval gives 6.12–7.66%, against the reported 6.1–7.8%.
- A bootstrap that holds the 400 certainty units fixed gives 6.29–7.66%.
- The reported bootstrap also resamples the certainty stratum, which widens it a little (V33A-02).
- The weights (N_h / (n_h − missing)) are implemented as described. 54% of the weighted respondents sit in the <$1m band, so the all-recipient median is a small-charity statistic (V33A-03).

**The "unreadable" group is mislabelled (contradicted, V33A-04).**
- None of the 9 `xml_not_read` EINs is unreadable. All 16 of their returns parsed, but none carries a line 1h or EZ line 1 element.
- The 2 real fetch failures (one 404, one parse error) belong to EINs whose other year matched.
- These EINs belong with the zero-contribution out-of-scope group, not with missing-at-random. The effect on the headline is negligible.

**Exclusions reproduce, but sponsors outside the DAFRC 2025 panel leak into the frame (V33A-05, -06).**
- The sampled frame keeps Jewish federations: UJA-Federation of New York, JFNA, Los Angeles, Houston and Hartford.
- It also keeps National Christian Foundation Wisconsin, whose share is 260% at a weight of 402.
- Dropping these and Navigation Charitable Fund lowers the pooled share from 6.89% to 6.58%. The median does not move (5.91%).

**Coverage of 67.3% is confirmed against `dafrc-market-totals-netted.csv` (V33A-07).**
- 2024 `daf_grants` central `netted_value` is $58,411,055,855, and $39,294,358,093 / $58,411,055,855 = 0.6727.
- FY2023 is 0.6850 and raw DAFRC is 0.6082.
- The numerator is domestic, itemised Schedule I. The denominator is Schedule D DAF grants, which include foreign (Schedule F) grants.

**Line 1h is the right base for a "share of contributions", but not for the title's "revenue" (V33A-08).**
- 1h equals Part I line 8 in all 4,096 cached 990s that carry both.
- 1h includes government grants: 64% of IRC's 1h, and 97.5% of Albina Head Start's.
- On total revenue, the pooled share is 4.2% and the median 4.2%.
- 1h−1e (private contributions) is the closer match to Chariot's "total giving".

**Scaling (V33A-09).**
- The arithmetic is exact.
- Dividing a median by a coverage ratio has no estimator behind it.
- The pooled scaling credits to frame recipients the denominator's foreign grants, sub-$5,000 lines and grants to charities outside the frame, so it leans high.

**The Chariot comparison is not like-for-like and is partly mis-sourced (V33A-10 to -12).**
- "Large nonprofits" is tagged [P] but is not on either Chariot page. They say "54 participating nonprofits" and "54 participating organizations". The phrase comes from the repo's own paraphrase.
- Averaged, the $26.1bn over five years is about $97m of total giving per participant-year [I]. That falls between the two largest bands.
- On the private basis, the scaled $25–100m figure (15.7%) and the scaled ≥$100m figure (8.4%) bracket Chariot's 12.6% [I]. So "not consistent on large organisations" holds only against the ≥$100m band.
- IRC, a named Chariot participant, is 4.7% of 1h but 13.1% of 1h−1e.
- Chariot states its 4–24% sector range on individual revenue, but its International Relief 23.7% on total revenue. The note labels both "individual revenue".

**990 spot checks: 8 of 8 confirmed (V33A-13, -14).**
- Denominators were checked for IRC, National Congress of Parents and Teachers, South Bay Pioneers, Caring & Sharing Community Resources, Napa Institute, Albina Head Start, Valley of the Kings Sanctuary and Second Nature.
- 1h was re-read from the re-fetched XMLs, and 1e as well where present.
- Numerators were re-summed from the raw Schedule I line cache, and the grantor counts match.

**Gradient and sector figures recompute (V33A-15, -16).**

### Study 2: Long-tail operating cost (P-B45N33-02)

**Reproduces exactly (V33A-17).** The output CSV is byte-identical and all printed tables match.

**The operating-cost definition is the repo standard (V33A-18).** The script reuses `operating_cost_ex_invest_mgmt` from `mission_sponsor_cost_structure.cost_row`: line 25 less lines 1–3, line 4 and line 11f. The one difference is that the long-tail script's "bps of total assets" uses end-of-year assets, where the cost-structure note averages beginning and end of year.

**Spot checks confirmed against the XML (V33A-21, -22).**
- Fox: line 25 $8,442,898, grants $6,278,447, 11f $613,712, so opex $1,550,739. Total assets are $148,593,728. Schedule D shows 99 accounts, $22,777,440 of DAF assets and $1,940,700 of DAF grants. That gives $2,401 per account and 104 bps.
- Fidelity: $161,573,385 of opex, 204,614 accounts, $782.70 per account, 24.2 bps.

**The AM "floor" is not a floor (V33A-20).**
- Column C carries line 11f investment fees. At Fox, 11f is all in column C and makes up 69% of it.
- Taking 11f out of column C gives a lower bound of $829 per account and 61 bps for tail CFs, against the stated $1,179 and 90 bps. Top-50 CFs fall to 24 bps, against 57.
- Fidelity books nothing in column C, so AM is undefined for nationals.

**"Twice as costly" holds only for some rules (V33A-23, -24).**
- Ratios of medians: rule A 2.0×, rule G 2.2×, AM 1.6×. The closest size band ($10–50m) gives 1.75×.
- Rule-A bps is whole-organisation opex ÷ total assets. It compares whole organisations, not DAF administration, and the top-50 CF group has n = 21.
- The CF pool comparison includes the tail itself.
- The elasticity cross-check holds. The median total-asset gap is 56× ($28.8m against $1.62bn), and 56^0.16 ≈ 1.9×.

**The identity, robustness series, ≤100 bps shares and examples are all confirmed (V33A-25 to -30).**

### Study 3: Processor disbursement rules (P-G1913-04)

**Rule pages: 22 fetched, every quote found.**
- 22 rule pages and PDFs were re-fetched, against the minimum of 12.
- Every short quote in the CSV for a fetched page was found verbatim: 41 of 41 non-empty quotes. Every self-stated date was found on its page (V33A-31 to -41).
- The Benevity Causes help centre still returns 403.
- YourCause's 120-day void (email 92 and the SFA overview) and "over 90 days" stale (payment statuses) are both on the pages, so the internal inconsistency the note reports is real.
- One classification issue: DEC-01 files Dechomai's donor-side "minimum fee of $10,000" as a `payout_threshold`.

**Complaint-to-rule coding mostly holds, with three problems (V33A-42 to -45).**
- **-039 is not "contradicted".** The record is dated 2024-07-01, but the $9.51 minimum and 12-month backstop come from terms last updated 2026-09-01. The record's "went to another entity" also fits the re-grant clause. Recode as unverified.
- **-036 is "partial" by the note's own definitions.** The rule permits a wait inside 45 + 90 days but does not predict it, and the YourCause attribution is inferred.
- **Rule versions are later than most complaints.** 11 of the 14 grant-delay records predate the rule versions they were coded against; only -001, -037 and -040 come after them. The note documents rule drift (PPGF went from 90 days to 45) but does not apply it to the coding.
- **-001 and -034 remain the strongest fits.** For -034, the record does not show that the 180-day hold elapsed before the redirect.

**Sponsor comparison confirmed (V33A-46).**

## Exact corrections

### `research/mission-2026-11-14/b40n12-daf-share-of-recipient-revenue.md`

1. - **Find:** "- **What it measures.** The numerator is DAF grants from the top-50 sponsors. The denominator is each recipient's own Form 990 Part VIII line 1h (total contributions). Recipients that are universities, hospitals, foundations or DAF sponsors are excluded."
   - **Replace with:** "- **What it measures.** The numerator is DAF grants from the top-50 sponsors. The denominator is each recipient's own Form 990 Part VIII line 1h (total contributions), not total revenue: on total revenue the pooled share is 4.2% and the median 4.2%. Recipients that are universities, hospitals, foundations or DAFRC-panel DAF sponsors are excluded [V wave 33A]"
2. - **Find:** "- **Scaled to all DAF grants [I].** Dividing by that coverage gives a pooled share of **≈10.2%** and a median of **≈8.8%**. On a private-contributions denominator (1h less line 1e government grants), the scaled pooled share is **≈15.0%**."
   - **Replace with:** "- **Scaled to all DAF grants [I].** Dividing by that coverage gives a pooled share of **≈10.2%**. On a private-contributions denominator (1h less line 1e government grants), the scaled pooled share is **≈15.0%**. Both lean high, because the netted denominator includes Schedule F foreign grants, sub-$5,000 lines and grants to charities outside this frame. A median divided by coverage (≈8.8%) has no estimator behind it and is illustrative only [V wave 33A]"
3. - **Find:** "  - Chariot's 54 participants are "large nonprofits" [P]. For large recipients specifically, the filings give lower shares: ≥$100m pooled 3.7% (scaled 5.5% [I]; 8.4% [I] on the private basis), and $25–100m pooled 6.3% (scaled 9.3% [I])."
   - **Replace with:** "  - Chariot's pages say "54 participating nonprofits" [P]; "large" is the repo's paraphrase, not a Chariot quote. Its $26.1bn of total giving over five years averages about $97m per participant-year [I]. For large recipients the filings give: ≥$100m pooled 3.7% (scaled 5.5% [I]; 8.4% [I] on the private basis), and $25–100m pooled 6.3% (scaled 9.3% [I]; 15.7% [I] on the private basis). The two private-basis figures bracket Chariot's 12.6% [V wave 33A]"
4. - **Find:** "Chariot's 54 participants are "large nonprofits", so its 12.6% would sit at the high end for that size class."
   - **Replace with:** "Chariot's participants average about $97m of total giving a year [I], between the two largest bands. On the private basis, the scaled figures of 15.7% ($25–100m) and 8.4% (≥$100m) bracket its 12.6%, so the gap is clear only against the ≥$100m band. The comparison is not like-for-like: CRM-coded gifts from all sponsors over 2021–25, against top-50 Schedule I over FY2023–24 [V wave 33A]"
5. - **Find:** "Its large members (IRC 4.7%, MSF 13.1%) carry big denominators."
   - **Replace with:** "Its large members (IRC 4.7%, MSF 13.1%) carry big denominators, often government grants: IRC is 13.1% of 1h−1e because line 1e is 64% of its 1h. Chariot's 23.7% for International Relief is stated on total revenue, not individual revenue [V wave 33A]"
6. - **Find:** "  - Unreadable returns (9 EINs) are treated as missing at random within their stratum."
   - **Replace with:** "  - Nine EINs are treated as missing at random within their stratum. All 16 of their returns parsed but report no line 1h or EZ line 1, so they belong with the zero-contribution out-of-scope group. The effect on the estimates is negligible [V wave 33A]"
7. - **Find:** "   - 22,269 recipient EINs ($4.36bn) are not in the BMF and are excluded."
   - **Replace with:** "   - 22,269 recipient EINs ($4.36bn) are not in the BMF and are excluded.
   - DAF sponsors outside the DAFRC 2025 panel stay in the frame. Examples are Jewish federations (UJA-Federation of New York, JFNA, Los Angeles, Houston, Hartford) and National Christian Foundation Wisconsin (share 260%, weight 402). Dropping them and Navigation Charitable Fund lowers the pooled share from 6.9% to 6.6%; the median is unchanged at 5.9% [V wave 33A]"

### `research/mission-2026-11-14/b45n33-long-tail-operating-cost.md`

1. - **Find:** "**Per dollar, tail CFs cost about twice top-50 CFs (205 vs 102 bps, rule A) and about 8.5 times top-50 nationals (24 bps)."
   - **Replace with:** "**Per dollar, tail CFs cost about twice top-50 CFs under rules A and G (205 vs 102 bps, 2.0×; 285 vs 131 bps, 2.2×), but 1.6× on the AM floor and 1.75× for the closest band ($10–50m, 178 vs 102 bps). Rule A per dollar is whole-org opex ÷ total assets, so this compares whole organisations, not DAF administration. Tail CFs are about 8.5 times top-50 nationals (24 bps) [V wave 33A]"
2. - **Find:** "Admin-only floor AM: **$1,179** ($617–$2,418)."
   - **Replace with:** "Admin-only floor AM: **$1,179** ($617–$2,418). Column C often holds line 11f investment fees (69% of column C at Community Foundation of the Fox); with 11f removed from column C, the lower bound is $829 per account and 61 bps (medians) [V wave 33A]"
3. - **Find:** "The tail-CF pooled figures here are 255 bps (A) and 406 bps (G); tail CFs are about twice as costly per dollar as the CF average, consistent with the scale elasticity of 0.84 reported there."
   - **Replace with:** "The tail-CF pooled figures here are 255 bps (A) and 406 bps (G); tail CFs are about twice as costly per dollar as the CF average, which itself includes the tail. This is consistent with the scale elasticity of 0.84 reported there: median total assets are $28.8m (tail CFs) and $1.62bn (top-50 CFs), a 56× gap, and 56^0.16 ≈ 1.9 [V wave 33A]"

### `research/mission-2026-11-14/g1913-processor-disbursement-rules.md`

1. - **Find:** "A $50 balance unpaid after a year (-039) therefore **contradicts** the written rule."
   - **Replace with:** "A $50 balance unpaid after a year (-039) would breach the current rule, but the record dates from 2024-07-01, before these terms (2026-09-01), and "went to another entity" fits the re-grant clause. It is coded unverified [V wave 33A]"
2. - **Find:** "- **Fully explained:** -036 (Blackbaud check not reissued after about three months). Reissue eligibility starts at 45 days and the replacement takes 60–90 days (YC-03)."
   - **Replace with:** "- **Partly explained:** -036 (Blackbaud check not reissued after about three months). Reissue eligibility starts at 45 days and the replacement takes 60–90 days (YC-03), so the rule permits the wait but does not predict it, and the record's YourCause attribution is inferred [V wave 33A]"
3. - **Find:** "- **Contradicted:** -039. A $50 balance unpaid after a year should have been paid under the $9.51 minimum and the 12-month backstop (NFG-01)."
   - **Replace with:** "- **Unverified:** -039. Under today's $9.51 minimum and 12-month backstop (NFG-01, terms of 2026-09-01) a $50 balance should be paid within a year. The record is from 2024-07-01, the rule then in force was not read, and the re-grant clause (NFG-05) fits "went to another entity" [V wave 33A]"
4. - **Find:** "| contradicted | -039 | 1 |"
   - **Replace with:** "| unverified | -039 | 1 | [V wave 33A]"
5. - **Find:** "- The not-explained and contradicted records (5 of 14) are operational failures measured against the processors' own rules."
   - **Replace with:** "- The not-explained records (4 of 14) are operational failures measured against the processors' current written rules; -039 needs the 2024 rule text [V wave 33A]"
6. - **Find:** "- **Complaint fit is our judgement.** It rests on single-review paraphrases."
   - **Replace with:** "- **Complaint fit is our judgement.** It rests on single-review paraphrases. 11 of the 14 grant-delay records predate the rule versions they are coded against (Benevity terms 2025-12-24, fee schedule 2026-10-01; For Good terms 2026-09-01); only -001, -037 and -040 come after them [V wave 33A]"

### `data/mission-2026-11-14/processor-disbursement-rules-2026-11-19.csv`

1. - **Find:** "CMP-G1913-039,contradicted"
   - **Replace with:** "CMP-G1913-039,unverified (2024 rule version not read) [V wave 33A]"
2. - **Find:** "CMP-G1913-034; CMP-G1913-036,full"
   - **Replace with:** "CMP-G1913-034; CMP-G1913-036,full (-034); partial (-036) [V wave 33A]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

1. **New subsection after §11.31.** Add "### 11.32 New-batch part A (validated, wave 33A)", containing the paragraph below. If §11.32 is already taken, use the next free number.
   - **Find:** "lets a court reallocate unspent conversion assets held in a DAF (repo [`validation-wave32b-report.md`](mission-2026-11-14/validation-wave32b-report.md)) [V wave 32B] Source: [validation-wave32b-report.md](mission-2026-11-14/validation-wave32b-report.md)."
   - **Replace with:** "lets a court reallocate unspent conversion assets held in a DAF (repo [`validation-wave32b-report.md`](mission-2026-11-14/validation-wave32b-report.md)) [V wave 32B] Source: [validation-wave32b-report.md](mission-2026-11-14/validation-wave32b-report.md).

### 11.32 New-batch part A (validated, wave 33A)

> **New-batch part A** (validated, wave 33A). A filing-based check of vendor DAF-share claims sampled 2,352 charities that received top-50 sponsors' FY2023–24 Schedule I grants and read their own 990s. Universities, hospitals, foundations and panel sponsors were excluded. Top-50 DAF grants are a median 5.9% (95% CI 5.3–7.4%) and a pooled 6.9% (6.1–7.8%) of line 1h contributions. Pooled shares fall from 17.8% under $1m of revenue to 3.7% at $100m and over. Top-50 grants are 67.3% of netted FY2024 DAF grants; scaling by that gives about 10% of 1h, or 15% of private contributions, an inference that leans high. On that basis Chariot's "nearly 13%" lies between the two largest bands. Among 1,220 usable sponsors under $50m, tail community foundations' allocated operating cost is a median 205 bps of DAF assets (rule A), twice top-50 CFs' 102 bps, but 1.6× on an admin-only rule. Tail CFs look cheaper per account only because their accounts are an eighth the size. Re-read processor rules show $100 check thresholds, monthly batches and redirection to charities chosen by the employer or processor. Written rules fully explain two of seven named complaints, but most complaints predate the rule versions read (repo [`validation-wave33a-report.md`](mission-2026-11-14/validation-wave33a-report.md)) [V wave 33A]"

New subsection text:

> **New-batch part A** (validated, wave 33A). A filing-based check of vendor DAF-share claims sampled 2,352 charities that received top-50 sponsors' FY2023–24 Schedule I grants and read their own 990s. Universities, hospitals, foundations and panel sponsors were excluded. Top-50 DAF grants are a median 5.9% (95% CI 5.3–7.4%) and a pooled 6.9% (6.1–7.8%) of line 1h contributions. Pooled shares fall from 17.8% under $1m of revenue to 3.7% at $100m and over. Top-50 grants are 67.3% of netted FY2024 DAF grants; scaling by that gives about 10% of 1h, or 15% of private contributions, an inference that leans high. On that basis Chariot's "nearly 13%" lies between the two largest bands. Among 1,220 usable sponsors under $50m, tail community foundations' allocated operating cost is a median 205 bps of DAF assets (rule A), twice top-50 CFs' 102 bps, but 1.6× on an admin-only rule. Tail CFs look cheaper per account only because their accounts are an eighth the size. Re-read processor rules show $100 check thresholds, monthly batches and redirection to charities chosen by the employer or processor. Written rules fully explain two of seven named complaints, but most complaints predate the rule versions read (repo [`validation-wave33a-report.md`](mission-2026-11-14/validation-wave33a-report.md)) [V wave 33A]

## Scratch artefacts (not committed)
The following are in `/tmp/claude-0/-home-user/ed3d1503-0f0d-5a0d-a5e2-85e6e3196309/scratchpad/v33a/`:
- `share.csv` and `share.json`: recipient-share re-run;
- `ltroot/` and `lt.md`: long-tail re-run;
- `xml/`: re-fetched 990s;
- `rules/`: re-fetched rule pages;
- `web/`: Chariot pages;
- `tools/`: `ci.py`, `sens.py`, `qcheck.py`, `ctx.py`, `fetch.py` and `reg.py`.
