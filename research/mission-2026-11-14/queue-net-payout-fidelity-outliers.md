# Net payout after DAF-to-DAF transfers; Fidelity's CY2025 outlier granting; post-SPLC flow feasibility

**Queue items:** Q-N06, P-VCM-03, P-CMP-04. The full text of each is in [`research-priority-queue.csv`](../../data/mission-2026-11-14/research-priority-queue.csv).

**Date:** 2026-11-15. **Method:** public filings and reports only. No outreach.

**Recency:** FY2021–FY2024. FY2020 is used only for the beginning DAF assets of FY2021.

**Labels:**
- **[F]** filed or first-party value.
- **[I]** inference.
- **[U]** unknown.

**Files written:**

| File | Rows | Content |
|---|---|---|
| [`scripts/mission_net_payout.py`](../../scripts/mission_net_payout.py) | — | Stdlib, functional style. Reuses the index and helper functions of [`mission_990_contractors.py`](../../scripts/mission_990_contractors.py) |
| [`data/mission-2026-11-14/net-payout-by-sponsor.csv`](../../data/mission-2026-11-14/net-payout-by-sponsor.csv) | 6,180 | One row per sponsor-year |
| [`data/mission-2026-11-14/net-payout-summary.csv`](../../data/mission-2026-11-14/net-payout-summary.csv) | 70 | Segment × year × sample |
| [`data/mission-2026-11-14/queue-proposals-net-payout.csv`](../../data/mission-2026-11-14/queue-proposals-net-payout.csv) | 4 | Proposals P-NPO-01 to P-NPO-04 |

Governing corrections from [quantitative-datasets-and-data-dictionary.md](quantitative-datasets-and-data-dictionary.md) are respected:
- Payouts use beginning-of-year assets: grants_t / assets_{t−1}.
- Fiscal year (FY) = the calendar year in which the tax period ends, so June-FYE values are never set against December totals.
- All values are sponsor-level, not account-level.

---

## 1. Answers

| Item | Answer | Label |
|---|---|---|
| **Q-N06** Net payout by segment | **Netting transfers between sponsors lowers aggregate payout by about 1.6–3.1 points a year (tier A); the median sponsor moves by only about 0.4–1.2 points.**<br><br>Pooled FY2021–24, sponsors with itemised Schedule I (n = 3,421 sponsor-years, 1,018 sponsors, $831bn beginning DAF assets):<br>- **Excluding processors:** gross 23.9%; net 21.5% (tier A), 20.8% (tier B), 19.0% (tier C).<br>- **National sponsors:** 23.8% gross and 20.9% net (tier A), because 12.1% of their DAF grants go to other national sponsors.<br>- **Community foundations:** 22.1% gross and 20.4% net (tier A). The FY2024 CF figure is driven by one SVCF → NPT line of $1.59bn.<br>- **Single-issue sponsors:** 31.7% gross and 30.4% net.<br>- **University and hospital sponsors:** 13.1% gross and 11.7% net.<br>- **Processors:** above 100% gross. Their assets pass through, so payout is not meaningful for them; 14% of their DAF grants go to national sponsors. | [F] amounts; [I] treating sponsor-to-sponsor grants as DAF money |
| **P-VCM-03** Fidelity's $727m CY2025 outlier | **Cannot be identified from public data yet.**<br>- **Why:** CY2025 straddles Fidelity's FY2025 (Jul 2024–Jun 2025) and FY2026 (Jul 2025–Jun 2026). The FY2026 return is not in the IRS index as of 2026-10-21.<br>- **Report wording:** "granting totaling", unlike the CY2024 "one outlier grant", which suggests more than one grant [I].<br>- **Candidate lines:** the FY2025 Schedule I lines that could hold the Jan–Jun 2025 part are NPT $346.8m, Johns Hopkins $340.3m (of which $131.4m non-cash), ImpactAssets $203.7m and GS PF $159.9m.<br>- **Ruled out:** the $480.1m Vanguard line is already the best match for the CY2024 $430m outlier (edge EF005).<br>- **Search:** no press report or recipient announcement names a $727m Fidelity outlier. | [F] report text and lines; [U] recipients |
| **P-CMP-04** Post-SPLC DAF-to-DAF outflows | **Not measurable yet.**<br>- **FY2026 returns** (Jul 2025–Jun 2026) of Fidelity, Vanguard and DAFgiving360 hold only April–June 2026 after the holds. They are expected in the IRS index around May 2027.<br>- **FY2027 returns** (Jul 2026–Jun 2027) are the first clean post-hold window, expected around May 2028.<br>- **Recipient side:** returns do not show sources, because Schedule B is redacted.<br>- **Baseline:** §5 gives the FY2021–FY2025 baseline the later test will use. | [F] filing calendar; [I] expected dates |

---

## 2. Q-N06 method

### 2.1 Data

**Universe.** Every EIN in the DAFRC 2025 updated panel with a row in FY2021–FY2024: 1,566 sponsors ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo copy [`dafrc-sponsor-schedule-d-fy2019-2024.csv`](../../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv)).

**Segment** comes from the sponsor's latest DAFRC type and subtype:

| Segment | DAFRC type / subtype |
|---|---|
| national | National / Standard |
| processor | National / Donation Processor |
| community_foundation | Community Foundation |
| single_issue | Single Issue / Other and Religiously-Affiliated |
| university_hospital | Single Issue / Universities and Healthcare |

**Returns:**
- **Location:** the IRS TEOS e-file index 2020–2026 (`https://apps.irs.gov/pub/epostcard/990/xml/{YYYY}/index_{YYYY}.csv`).
- **Download:** the GivingTuesday mirror (`https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml`).
- **Count:** 7,559 returns parsed. 6,161 of the 6,180 sponsor-year rows have a parsed return; 19 have no Form 990 in the index.
- **Selection:** within a fiscal year the latest submission per tax period is used, so amended returns supersede originals. Where a year holds two tax periods (short years, fiscal-year changes), the return that carries Schedule D DAF values is used. This fixed DAFGiving360 FY2021, which also has a December-2021 return with zero grants.

**Fields parsed from each return:**
- **Schedule D Part I:** DAF grants (line I-3) and end-of-year value (line I-4).
- **Part IX line 1:** grants to domestic organisations.
- **Schedule I Part II:** every `RecipientTable` line.

### 2.2 Definitions

**Sponsor transfer.** A Schedule I line whose recipient EIN is a DAFRC panel EIN other than the filer's own. When the EIN is blank, an exact match on the normalised name to a single panel name is accepted; 391 lines in total matched this way. The definition comes in three nested tiers:

| Tier | Recipients included | Reading |
|---|---|---|
| **A** | National Standard sponsors (Fidelity, Schwab/DAFgiving360, NPT, Vanguard, GS, ImpactAssets …) | Conservative; closest to "DAF-to-DAF" |
| **B** | A + donation processors + community foundations | Broad |
| **C** | Every panel EIN, adding single-issue, religious, university and hospital sponsors | Upper bound. It includes plainly non-transfer program grants, such as Fidelity → Johns Hopkins $831.9m in FY2023 |

**Ratios:**
- **Gross payout** = Schedule D DAF grants_t / Schedule D DAF assets_{t−1}.
- **Net payout (tier)** = (DAF grants − min(transfers, DAF grants)) / assets_{t−1}.

**Beginning assets** come from the prior fiscal year's Schedule D in that sponsor's own return. Where that return is missing, the filed DAFRC value is used (column `boy_source`).

**Sample (`in_payout_sample` = 1):**
- Schedule D grants present and not negative. 31 sponsor-years report negative grants, which are probably sign errors; they are excluded, not corrected.
- Beginning assets of at least $1m, and not DAFRC-imputed.
- A parsed return.
- Result: 3,828 sponsor-years.

**Headline sample (`itemized_only`).** It additionally requires an itemised Schedule I, which leaves 3,421 sponsor-years. A Schedule I counts as itemised when it meets both conditions below:
- It totals at least 50% of Part IX line 1.
- Less than half of its total sits on a "see attached / view attached grant report" line.

**Excluded as not itemised:** 130 sponsor-years point to an attachment, including RCF, BofA CGF, NY Community Trust, Greater Horizons, Greater Kansas City CF and the US Charitable Gift Trust. Their transfers are unknown, not zero.

**Coverage.** Beginning DAF assets in the headline sample are $158.2bn, $216.0bn, $213.7bn and $243.0bn for FY2021–FY2024. That is 94%, 92%, 93% and 95% of the DAFRC panel's prior-year totals ($168.8bn, $234.3bn, $229.7bn and $256.4bn).

### 2.3 Limitations (state with any use)

1. **Schedule I threshold.** Schedule I lists only grants of more than $5,000 per recipient, and only to domestic organisations and governments. Grants to foreign organisations are on Schedule F and are not parsed. Sub-$5,000 sponsor-to-sponsor grants are missed, which is immaterial in dollars. A sponsor that answers "No" on Part IV line 21 has no Schedule I at all.
2. **Aggregation.** Sponsors report one line per recipient per year, so it cannot be seen whether a line is one account move or many (see [queue-state-filings-transfer-terms.md §5.1](queue-state-filings-transfer-terms.md)).
3. **Mixed funds.** Schedule I covers all grants, not only DAF grants, so for community foundations a grant to another sponsor may come from unrestricted or field-of-interest funds. Netting assumes such grants left DAFs, which overstates the netting slightly [I]. Conversely, a "transfer" may fund a programme rather than a DAF: CAF America and processor recipients are examples.
4. **Affiliated pairs.** Dechomai Asset Trust → Dechomai Foundation ($315–475m a year) is an affiliated-entity transfer inside the processor segment.
5. **Attachments.** Non-itemising filers (item 2.2) are excluded from the net figures. They hold about 5% of beginning assets ($44.8bn of $875.7bn pooled), including RCF ($4.2bn) and BofA CGF ($3.8bn) in FY2024 (P-NPO-03).
6. **Mixed fiscal years.** June- and December-FYE sponsors are mixed within a fiscal year, as in DAFRC. Medians are across sponsors and say nothing about account behaviour.

---

## 3. Q-N06 results

All values are from the headline sample in [`net-payout-summary.csv`](../../data/mission-2026-11-14/net-payout-summary.csv): `sample = itemized_only`. Payouts are aggregates (Σ grants / Σ beginning assets).

### 3.1 By segment, pooled FY2021–FY2024

| Segment | Sponsor-yrs (sponsors) | Beg. DAF assets $bn | DAF grants $bn | Transfers A / B / C $bn | Share of grants, tier A | Gross | Net A | Net B | Net C | Median gross → net C |
|---|---|---|---|---|---|---|---|---|---|---|
| National | 204 (62) | 548.5 | 130.4 | 15.76 / 20.30 / 31.80 | 12.1% | 23.8% | 20.9% | 20.1% | 18.0% | 21.8% → 15.2% |
| Community foundation | 2,163 (621) | 197.3 | 43.5 | 3.26 / 4.28 / 6.25 | 7.5% | 22.1% | 20.4% | 19.9% | 18.9% | 10.9% → 10.4% |
| Single-issue | 785 (248) | 71.1 | 22.5 | 0.91 / 1.18 / 2.64 | 4.1% | 31.7% | 30.4% | 30.0% | 28.0% | 18.3% → 15.7% |
| University / hospital | 221 (71) | 8.9 | 1.2 | 0.13 / 0.13 / 0.35 | 10.9% | 13.1% | 11.7% | 11.6% | 9.2% | 6.8% → 5.3% |
| Processor | 48 (16) | 5.1 | 13.4 | 1.89 / 1.99 / 2.44 | 14.1% | 260.6% | 223.8% | 222.0% | 213.2% | n/m |
| **All excluding processors** | 3,373 (1,002) | 825.8 | 197.6 | 20.07 / 25.90 / 41.03 | 10.2% | **23.9%** | **21.5%** | **20.8%** | **19.0%** | 12.3% → 11.1% |
| All | 3,421 (1,018) | 830.9 | 211.0 | 21.96 / 27.88 / 43.47 | 10.4% | 25.4% | 22.8% | 22.0% | 20.2% | 12.5% → 11.2% |

### 3.2 By year, all segments excluding processors

| FY | Sponsor-yrs | Beg. assets $bn | Grants $bn | Transfers, tier A $bn | Gross | Net A | Net B | Net C |
|---|---|---|---|---|---|---|---|---|
| 2021 | 819 | 157.6 | 42.3 | 4.31 | 26.8% | 24.1% | 22.9% | 21.2% |
| 2022 | 823 | 215.3 | 48.4 | 4.82 | 22.5% | 20.3% | 19.4% | 17.9% |
| 2023 | 843 | 212.0 | 48.2 | 3.53 | 22.7% | 21.1% | 20.6% | 18.5% |
| 2024 | 888 | 240.8 | 58.7 | 7.40 | 24.4% | 21.3% | 20.8% | 18.9% |

**National, by year (gross → net A):**

| FY | Gross | Net A | Share of grants to tier A sponsors |
|---|---|---|---|
| 2021 | 29.2% | 25.5% | 12.6% |
| 2022 | 22.6% | 19.4% | 13.9% |
| 2023 | 20.8% | 18.9% | 9.3% |
| 2024 | 24.1% | 21.1% | 12.3% |

**Community foundations, by year (gross → net A):** 20.6% → 19.4%, 21.0% → 20.5%, 24.9% → 23.9% and 21.6% → 17.9% for FY2021–FY2024. The FY2024 drop is mostly one line: SVCF → NPT, $1,591.3m ([SVCF CY2024 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543149349305759_public.xml)).

### 3.3 Findings

1. **Transfers between sponsors are about 10% of DAF grants (tier A), and 13–21% under the broader tiers.** Between $3.5bn and $7.4bn a year of 990 "DAF grants" in FY2021–24 is money landing in another national sponsor, against $42–59bn of grants. Netting it lowers aggregate payout by 1.6–3.1 points a year (tier A) or 4.2–5.6 points (tier C). The market's "25% payout" is therefore partly double-counted. On the pooled figures, net payout is 21–22% under tiers A and B, and 19–20% under the upper-bound tier C [F amounts / I interpretation].
2. **Netting matters most for national sponsors and least for the median sponsor.** National net payout falls 2.9 points under tier A. The median sponsor across all segments falls about 0.4–1.2 points, because most small community foundations make few sponsor grants: 2,139 of 3,373 non-processor sponsor-years show some tier C transfer, most of them small. The share of sponsors paying out under 5% rises from 17.8% gross to 20.9% net (tier C) [F].
3. **A few lines drive single years:**

| Grantor → recipient | FY | Amount | Source |
|---|---|---|---|
| SVCF → NPT | FY2024 | $1,591.3m | |
| GS PF → NPT | FY2021 | $1,144.1m | [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202243089349301314_public.xml) |
| Fidelity → SVCF | FY2022 | $843.4m | [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202430459349302913_public.xml) |
| Jasper Ridge → DAFgiving360 | FY2022 | $750.6m | final return |
| BNY Mellon CGF → RCF | FY2024 | $619.8m | termination |
| NPT → SVCF | FY2021 | $610.9m | [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202231339349309863_public.xml) |

   Year-to-year changes in segment net payout should be read as lumpy [F].
4. **Tier C is not a credible point estimate.** It treats grants to Johns Hopkins as DAF transfers, because universities with DAF programmes sit in the DAFRC panel: for example Fidelity → JHU $831.9m in FY2023 and DAFGiving360 → JHU $481.8m (FY2023) and $517.4m (FY2024). Religious denominations and federations are counted the same way. **Use tier A as the conservative net figure and tier B as the broad one.** P-NPO-04 proposes an audited whitelist.
5. **Fit with sponsor self-reporting.** Fidelity's reports remove outlier granting and "accounts with significant transfer activity" (§4). Sponsor-published payout averages therefore already sit closer to the net series than to the 990 gross series [I].

---

## 4. P-VCM-03: Fidelity's "significant outlier granting totaling $727 million" (CY2025)

**Report text [F].** The 2026 Giving Report (PDF created 2026-04-21, 15 pages) says: "Significant outlier granting totaling $727 million was removed from calculations for the average grant size on page 6 and granting by charitable sector on page 9." ([2026 Giving Report](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf), methodology page).

The 2025 report said: "One outlier grant of $430 million was removed …", and separately: "A limited number of accounts with significant transfer activity were excluded from the analysis." ([2025 Giving Report](https://fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf), p.19).

**Consistency check [F/I].** CY2025 reported $18.3bn in grants, 3M grants and an average grant of $5,801. (18.3bn − 0.727bn) / 3.03M ≈ $5,800, so the $727m is inside the $18.3bn and outside the average. The same check on CY2024 holds: (14.9bn − 0.43bn) / 2,664,446 ≈ $5,431, against a published $5,422. The CY2025 sector table ("Society benefit 23.4% of dollars") also excludes it.

**Fidelity Schedule I, largest lines (USD m).** Blank means the recipient is not among that year's 25 largest lines, not that it received nothing. Values come from `sched_i_top_lines` in the script's extract.

| Recipient (DAFRC segment) | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 |
|---|---|---|---|---|---|
| Vanguard Charitable (national) | | | | | **480.1** |
| National Philanthropic Trust (national) | 178.1 | 318.2 | 195.0 | 153.3 | **346.8** |
| Johns Hopkins University (university) | | | 831.9 | 273.1 | **340.3** (131.4 non-cash) |
| ImpactAssets (national) | | 31.0 | | 87.8 | **203.7** |
| Church of Jesus Christ of LDS | 141.7 | 195.0 | 125.8 | 145.2 | 189.1 |
| GS Philanthropy Fund (national) | | 104.2 | | | **159.9** |
| Silicon Valley CF (CF) | | 843.4 | | | 147.5 |
| Schwab Charitable / DAFgiving360 (national) | 101.8 | 506.8 | 183.3 | 100.9 | 117.8 |
| Schedule I lines; total | 64,214; $9.86bn | 65,439; $11.24bn | 72,328; $10.13bn | 80,308; $12.51bn | 89,891; $15.07bn |

**Return XMLs by year:** [FY2021](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202221339349302787_public.xml), [FY2022](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202430459349302913_public.xml), [FY2023](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202441369349301334_public.xml), [FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202521349349310887_public.xml) and [FY2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601389349301700_public.xml) (submitted 2026-05-18).

**Reading:**
- **Located so far [F]:** only the Jan–Jun 2025 half of CY2025 is in a filed return (FY2025), and Schedule I lines are annual totals by recipient, so they cannot be split by half-year. The Jul–Dec 2025 half sits in FYE 6/2026, which is not in the IRS index as of its 2026-10-21 update. Fidelity filed in May in 2024, 2025 and 2026, so the return is expected around May 2027 [I].
- **Unlikely candidate [I]:** the Vanguard $480.1m line is already the best match for the CY2024 $430m outlier (EF005).
- **Possible but unproven [I]:** the FY2025 lines that rose well above their FY2021–24 range are NPT (+$29m over its prior maximum), ImpactAssets (+$116m) and GS PF (+$56m). Even if all of that excess fell in Jan–Jun 2025, it sums to about $200m, far below $727m. JHU's $340m line is within its prior range.
- **Conclusion [I, weak]:** most of the $727m probably sits in Jul–Dec 2025, or in recipient lines that do not stand out. Whether it was DAF-to-DAF is **[U]**.
- **No outside identification:** searches for a $727m Fidelity outlier, or for 2025 recipient announcements naming Fidelity Charitable, found nothing that identifies it. Fidelity's Schedule B is "RESTRICTED" in the public XML ([queue-vendor-channel-moves.md](queue-vendor-channel-moves.md)).
- **Next step:** P-NPO-01.

---

## 5. P-CMP-04: can 2026 post-SPLC DAF-to-DAF outflows be measured yet?

**No.** The holds began in April 2026 after the SPLC indictment ([daf-user-complaints-deep-research.md §5.3](daf-user-complaints-deep-research.md); [CA AG release](https://oag.ca.gov/node/623769)).

| Source | Window covered | Shows sponsor-to-sponsor detail? | Expected public | Status 2026-11-15 |
|---|---|---|---|---|
| Fidelity, Vanguard and DAFgiving360 Form 990, FYE 6/2026 (Schedule I) | Jul 2025–Jun 2026; only Apr–Jun 2026 is post-hold | Yes, a recipient-EIN total per year | IRS index about Apr–May 2027. Past submissions: Fidelity 2026-05-18, DAFgiving360 2026-04-29, Vanguard FY2024 2025-05-14 ([harvest](../../data/mission-2026-11-14/form990-returns-schedule-d-harvest-full.csv)); mirror lag after that | Not filed |
| Same sponsors, FYE 6/2027 | Jul 2026–Jun 2027, fully post-hold | Yes | About May 2028 | Not filed |
| GS PF and Mightycause (calendar year; on SPLC's October 2026 list) CY2026 990 | Jan–Dec 2026 | Yes | About May–Nov 2027 | Not filed |
| Recipient community foundations' CY2026 990 | Jan–Dec 2026 | **No.** Schedule D contributions are not split by source, and Schedule B donor names are redacted in public copies | 2027 | Not filed |
| Sponsor audited statements (Fidelity posts its audit) and giving reports | FY or CY totals | No recipient detail; giving reports may exclude transfer accounts (§4) | FY2026 audit about autumn 2026; 2027 Giving Report about April 2027 | Gives totals only |

**Baseline already in the data (USD m) [F].** The later test will compare against these Schedule I lines from [`net-payout-by-sponsor.csv`](../../data/mission-2026-11-14/net-payout-by-sponsor.csv):

| Sponsor | Measure | FY2021 | FY2022 | FY2023 | FY2024 |
|---|---|---|---|---|---|
| Fidelity | → community foundations | 106.4 | 959.3 | 97.5 | 148.8 |
| Fidelity | → national sponsors (tier A) | 521.4 | 1,289.3 | 732.2 | 833.3 |
| Vanguard | → community foundations | 39.4 | 26.7 | 22.6 | 46.7 |
| Vanguard | → tier A | 330.9 | 79.7 | 177.7 | 416.4 |
| DAFGiving360 | → community foundations | 41.1 | 53.7 | 60.6 | 90.8 |
| DAFGiving360 | → tier A | 522.8 | 370.1 | 300.5 | 659.5 |

FY2025 lines for Fidelity and DAFGiving360 are in [`daf-to-daf-flows-990.csv`](../../data/mission-2026-11-14/daf-to-daf-flows-990.csv). Vanguard's FY2025 XML (object 202621329349306657) is indexed but still returns HTTP 404 on the mirror (rechecked 2026-11-15).

**Limits of the eventual test:**
- Year-to-year volatility is large: Fidelity → CFs ran from $97m to $959m in FY2021–24.
- Schedule I cannot tell a hold-motivated move from any other.

A credible test therefore needs FY2027, recipient-level lines (named CFs), and preferably more than one post-hold year. Until then, **no measurement is possible and none is offered.**

---

## 6. Data dictionary

### 6.1 `net-payout-by-sponsor.csv` (one row per DAFRC sponsor × FY2021–FY2024)

| Column | Meaning |
|---|---|
| `ein`, `sponsor_name`, `dafrc_type`, `dafrc_subtype`, `segment` | DAFRC identity. Segment as in §2.1 |
| `fiscal_year`, `tax_period_end`, `object_id`, `xml_status` | Return used (`ok`, `http_404`, `no_990_in_index`) |
| `boy_daf_assets`, `boy_source` | Beginning DAF assets. Source is one of `990_prior_fy_sched_d`, `dafrc_filed`, `dafrc_imputed` or `missing` |
| `daf_grants_sched_d`, `daf_eoy_assets_sched_d`, `daf_contributions_sched_d` | Schedule D Part I lines I-3, I-4 and I-2 from the return |
| `dafrc_total_daf_grants`, `dafrc_grants_source` | DAFRC value, for comparison |
| `part_ix_line1_grants`, `sched_i_lines`, `sched_i_total`, `sched_i_coverage_of_part_ix` | Schedule I completeness |
| `sched_i_itemized_ok`, `sched_i_points_to_attachment` | 1 = Schedule I is usable for netting / 1 = a "see attached" line holds half or more of the total |
| `transfers_tier_a/b/c` | Schedule I cash plus non-cash to panel recipients by tier (§2.2), excluding the filer's own EIN |
| `transfers_to_<segment>` | The same, split by recipient segment |
| `transfers_noncash_tier_c`, `transfer_recipients_tier_c`, `name_matched_lines` | Composition |
| `largest_transfer_recipient`, `largest_transfer_usd` | Largest recipient line to a panel recipient (any tier) |
| `transfer_share_of_daf_grants_tier_a/c` | Transfers / DAF grants |
| `gross_payout`, `net_payout_tier_a/b/c` | Ratios (§2.2). Net values are blank when Schedule I is not itemised |
| `in_payout_sample`, `exclusion_reason` | Sample flag (§2.2) |
| `xml_url`, `boy_xml_url` | Evidence |

### 6.2 `net-payout-summary.csv`

| Column | Meaning |
|---|---|
| `segment` | The five segments, `all_ex_processor` and `all` |
| `fiscal_year` | 2021–2024 or `FY2021-2024` (pooled) |
| `sample` | `itemized_only` (headline) or `all_in_sample` (adds non-itemised filers, whose transfers count as 0, so their net equals their gross) |
| `sponsor_years`, `sponsors`, `sponsor_years_not_itemized` | Counts |
| `boy_daf_assets`, `daf_grants`, `transfers_tier_*` | Sums; transfers are capped at each sponsor's DAF grants |
| `transfer_share_tier_a/c` | Σ transfers / Σ grants |
| `agg_gross_payout`, `agg_net_payout_tier_*` | Σ grants / Σ beginning assets, before and after netting |
| `median_*`, `p25_gross_payout`, `p75_gross_payout` | Distribution across sponsors |
| `share_below_5pct_gross`, `share_below_5pct_net_tier_c` | Share of sponsor-years with payout under 5% |
| `sponsors_with_any_tier_c_transfer` | Count of sponsor-years with any transfer under tier C |

### 6.3 Reproduce

```
python3 scripts/mission_net_payout.py --irs-dir DIR --cache-dir CACHE --fetch --workers 24
```

`DIR` holds `index_2020.csv` to `index_2026.csv` from the IRS TEOS index. A network run took about 2 minutes. A re-run from the cache takes seconds.

## 7. Sources

| ID | Source | Use |
|---|---|---|
| S1 | [IRS TEOS index](https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv) (2020–2026; 2026 file dated 2026-10-21) | Return locator; FY2026 not filed |
| S2 | GivingTuesday XML mirror, `{OBJECT_ID}_public.xml` (URLs per row in the CSV) | Schedule D, Part IX and Schedule I |
| S3 | [DAFRC 2025 updated dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx) (repo copy) | Universe, segments, fallback beginning assets |
| S4 | [Fidelity Charitable 2026 Giving Report](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf) | $727m outlier text; CY2025 totals |
| S5 | [Fidelity Charitable 2025 Giving Report](https://fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf) | $430m outlier; transfer-account exclusion |
| S6 | Repo: [queue-state-filings-transfer-terms.md](queue-state-filings-transfer-terms.md), [queue-vendor-channel-moves.md](queue-vendor-channel-moves.md), [daf-to-daf-flows-990.csv](../../data/mission-2026-11-14/daf-to-daf-flows-990.csv), [full-universe-990-harvest-and-corrected-totals.md](full-universe-990-harvest-and-corrected-totals.md) | Prior flow matrix, EF005, filing dates |
| S7 | Web searches (2026-11-15) for "$727 million" Fidelity outlier, 2025 recipient announcements and a Fidelity H1-2025 release | No identifying result |
