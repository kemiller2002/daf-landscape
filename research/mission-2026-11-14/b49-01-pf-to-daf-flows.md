# Private-foundation-to-DAF flows: a census of 990-PF grants to DAF sponsors, tax years 2022-2024 (b49-01)

**Date:** 2026-11-20 · **Task ID:** b49-01 · **Topic:** new to this repo

**Outputs**
- Script: [`scripts/mission_pf_to_daf_flows.py`](../../scripts/mission_pf_to_daf_flows.py). It has five stages: frame, extend, harvest, bulk and build. Stdlib only, functional style.
- Data: [`data/mission-2026-11-14/pf-to-daf-flows-2026-11-20.csv`](../../data/mission-2026-11-14/pf-to-daf-flows-2026-11-20.csv). It has 29,204 rows, one per (990-PF return, matched DAF sponsor). The data dictionary is in §5.
- Queue proposals: [`data/mission-2026-11-14/queue-proposals-b49-01.csv`](../../data/mission-2026-11-14/queue-proposals-b49-01.csv) (P-B4901-01..06).
- Aggregates: the build stage writes every figure quoted below to `pf_to_daf_summary.json` in the cache directory (§8).

Tags: [F] computed from filings by the script · [P] quoted primary source · [I] inference.

## 0. Answer in brief

- **Scale.** This is a census, not a sample. The frame holds every 990-PF in the IRS e-file index for tax years 2022-2024: 371,359 returns, the latest submission per EIN and tax period. Of these, 371,358 were parsed (1 XML is unavailable). Itemised Part XV grant lines cover 98.2-98.7% of grants paid. [F]
- **How much PF money reaches DAF sponsors.** Three nested definitions (§2.4):
  - **Core (T1): $2.55bn (TY2022), $2.96bn (TY2023), $3.91bn (TY2024).** That is $9.43bn over three years, from 2,801 distinct PFs. T1 is the FY2024 top-50 national sponsors and processors plus NCF, Jewish Communal Fund, DonorsTrust and Thrivent. [F]
  - **Adding other national sponsors and processors (T1-T2):** $3.49bn, $3.96bn and $5.23bn. [F]
  - **Adding community foundations (T1-T3):** $4.88bn, $5.41bn and $7.05bn. That is $17.34bn over three years from 10,623 PFs. [F]
  - **DAF-labelled lines with no identifiable sponsor (T0):** a further $0.15bn, $0.28bn and $0.49bn ($0.92bn in total). Their recipient is written only as "DAF", "Donor Advised Fund" or "X family DAF". [F]
  - **As a share of all PF grants paid:** T1 is 2.2%, 2.4% and 3.0%. T1-T3 is 4.1%, 4.3% and 5.4%. [F]
- **Against the repo's DAF contribution totals** (DAFRC corrected market totals, same-numbered FY):
  - T1 equals **3.3%, 4.5% and 4.2%** of all DAF contributions. Over three years it is 4.0% ($9.43bn of $234.6bn). [F]
  - T1-T3 equals 6.4%, 8.3% and 7.6%. This is an upper bound: much T3 money is not DAF money. [F][I]
- **Concentration.** Pass-through PFs that are not winding down dominate the flow.
  - The top 10 PFs give **31%** of T1 dollars over three years, the top 50 give 54% and the top 100 give 65%. [F]
  - The single largest PF gave 7.8% of T1 dollars. None of the top 10 T1 grantors filed a final or §507(b)(1)(A) return in any of the three years. [F]
- **Wind-downs.**
  - 8,020 PF returns over three years were flagged as winding down: Heading item G "final return" (7,834) or item E §507(b)(1)(A) termination (1,329). [F]
  - **877 of them (10.9%) made a grant to a T1-T3 sponsor in the same year, totalling $1.22bn.** That is **7.0% of all T1-T3 dollars**. [F]
  - Within T1, terminating PFs gave $0.75bn, or **7.9% of T1**. A median terminating PF that gave to a sponsor had $0.41m of beginning-of-year book assets and gave $295k. [F]
  - In those final years, sponsors received 18.6%, 22.9% and 22.7% of all grants paid by terminating PFs (T1-T3). [F]
  - The flagged figure is a floor. A further 438 return-years moved at least half of beginning-of-year assets to T1-T3 sponsors without a termination flag in that year (§3.5). [F]
- **Sponsor dependence on PF money** (T1 sponsors; PF receipts ÷ DAFRC Schedule D contributions):
  - Fidelity Charitable 4.0-5.8%; NPT 4.9-8.3%; Schwab/DAFgiving360 4.3-9.5%; Vanguard Charitable 6.0-9.8%. [F]
  - The highest shares: Jewish Communal Fund 18-21%, DonorsTrust 10-19% and ImpactAssets 11-16%. [F]
  - Community-foundation ratios run up to 50-70% (Boston, Atlanta, San Francisco, Minneapolis). They are not DAF shares, because PF grants to CFs largely fund programmes (§3.4). [F][I]

## 1. Question and scope

The question has two parts:
- How much money moves from private foundations into DAF sponsors?
- How much of it comes from foundations that are winding down into DAFs?

**Universe.**
- *Grantor:* every Form 990-PF e-filed for tax years 2022-2024.
- *Recipient:* the repo's DAF sponsor universe, the DAFRC 2025 panel ([`dafrc-sponsor-schedule-d-fy2019-2024.csv`](../../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv), 1,594 EINs). The panel contains the repo's FY2024 top-50 ([`daf-sponsor-league-table-fy2021-2025.csv`](../../data/mission-2026-11-14/daf-sponsor-league-table-fy2021-2025.csv)).

**Why tax year.** The tax year follows the 990-PF `TaxYr` convention: the year in which the tax period begins. DAFRC fiscal years are the calendar year in which the period ends. For calendar-year filers, which are most PFs and most large sponsors, the two coincide. For June filers the PF tax year runs six months ahead of the same-numbered DAFRC FY. [I]

**Legal frame.** Form 990-PF Heading item E is for a foundation "that has terminated its private foundation status under section 507(b)(1)(A) during the tax year being reported, by distributing all its net assets to one or more public charities without keeping any right, title, or interest in those assets" [P: IRS, Instructions for Form 990-PF, https://www.irs.gov/instructions/i990pf].
- National DAF sponsors and community foundations are public charities, so a transfer of all assets to a DAF sponsor can use this route. [I]
- Item F (60-month termination under §507(b)(1)(B)) is a conversion to public-charity status, not a wind-down. It is counted separately and excluded from "terminating".
- IRS overview page: https://www.irs.gov/charities-non-profits/private-foundations/termination-of-private-foundation-status [P].

## 2. Method

### 2.1 Frame (index only, no sampling)

- **Source.** IRS TEOS e-file index files `index_2023.csv` to `index_2026.csv` (https://apps.irs.gov/pub/epostcard/990/xml/{year}/index_{year}.csv), taking rows with `RETURN_TYPE = 990PF`.
- **Tax year.** Derived from `TAX_PERIOD`: month 12 gives the same year, any other month the year before.
- **Selection.** Tax years 2022-2024 are kept. For each (EIN, TAX_PERIOD) the latest `OBJECT_ID` is used, so an amended return supersedes the original.
- **Index versions.** The cached `index_2026.csv` (21 Oct 2026) was later extended with the IRS file last modified 18 Nov 2026 (task `extend`). That added 886 returns (56 for TY2023 and 830 for TY2024). Re-keying by (EIN, period) then dropped 45 superseded submissions.
- **Final frame:** 121,849 (TY2022), 124,598 (TY2023) and 124,912 (TY2024) returns. [F]
- **Late filers.** TY2024 fiscal-year filers with periods ending as late as November 2025 were due, with extension, by October 2026. A few late filers may still be missing from the index. [I]

### 2.2 XML

- **Primary source.** Each frame return was read from the GivingTuesday 990 data-lake mirror of IRS TEOS (`https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml`). The XML was parsed in memory and discarded.
- **Mirror misses (1,954).** 1,953 of them were 2026 submissions, and all 1,953 were read straight from the **IRS monthly bulk zips** (`2026_TEOS_XML_10A`: 886 members; `2026_TEOS_XML_05B`: 1,067 members, although the index names `05A`). The remaining miss is a TY2022 return listed in `index_2023.csv`, which has no batch-ID column.
  - The script reads each zip's central directory and the needed members with HTTP range requests (`Accept-Ranges: bytes` is honoured as of 20 Nov 2026). No zip is downloaded whole.
- **Final sources:** 369,405 returns from the GT mirror and 1,953 from IRS bulk zips. One TY2022 return is in neither, because it has no batch ID in `index_2023.csv`. [F]
- **Per return**, the script extracts:
  - flags: `FinalReturnInd`, `InitialReturnInd`, `AmendedReturnInd`, `PFStatusTermSect507b1AInd`, `PF60MonthTermSect507b1BInd` and `OrganizationDissolvedEtcInd`;
  - assets: FMV of assets (`FMVAssetsEOYAmt`) and book assets at the beginning and end of the year;
  - grants paid: Part I line 25 (`ContriPaidRevAndExpnssAmt`), the Part XV line 3a total (`TotalGrantOrContriPdDurYrAmt`), and the count and sum of `GrantOrContributionPdDurYrGrp` lines.
- **Grants paid.** The script takes Part XV 3a, otherwise line 25, otherwise the sum of itemised lines.
- **Per grant line** it keeps the recipient business name, city, state, country, relationship, foundation status, purpose and amount.
- **Candidate filter.** To keep the cache small (about 30 MB), only *candidate* lines are kept. A candidate line has DAF-like words in the name or purpose, a 9-digit EIN in its text, or a normalised name equal to a panel name. Lines to individuals are dropped.

### 2.3 Matching a grant line to a sponsor

The 990-PF Part XV schema has **no recipient-EIN field**, so EIN matching applies only when a filer typed an EIN into a text field (67 return-sponsor rows). Matching then proceeds in this order, and the first rule that matches is used:
1. **EIN written in the text.** Any 9-digit EIN in the name, purpose or status text that is a panel EIN.
2. **Exact normalised name.** The name, or the name with a duplicated Line 2 removed, must equal a DAFRC or BMF legal name of a panel EIN.
   - When several panel EINs share the name, the one in the line's state wins, then the one whose current BMF name carries it.
   - The match is rejected when the BMF state and the line's state differ.
   - Names made only of generic words (for example "COMMUNITY FOUNDATION" or "JEWISH COMMUNITY FOUNDATION") are never matched by name.
3. **Exact normalised first segment.** The same rules applied to the text before " - ", "FBO", "C/O", "(", ",", "/" and similar separators. This catches "XYZ FUND AT FIDELITY CHARITABLE"-style names via rule 4 and "THE COLUMBUS FOUNDATION - SMITH FUND"-style names here.
4. **Brand alias** for national sponsors (`ALIASES` in the script). Examples:
   - "Fidelity Charitable", or Fidelity together with DAF/donor-advised;
   - "Schwab Charitable" or "DAFgiving360";
   - "Vanguard Charitable";
   - "J.P. Morgan Charitable Giving Fund", which maps to NPT. The repo already documents this program as "offered in conjunction with National Philanthropic Trust" ([queue-ren-iphi-attrition.md](queue-ren-iphi-attrition.md)), and the PF lines give NPT's Jenkintown, PA address.
5. **No match, but the line says "DAF" or "donor advised"** in its recipient name or purpose: the line goes to bucket **T0** (DAF-labelled, sponsor unattributed). It is kept apart from sponsor totals.

**Match methods** (return-sponsor rows, all tiers): 67,287 by exact name, 1,715 by first segment, 181 by both, 4,325 by alias, 20 by alias plus a name rule, 67 by EIN in text, and 671 T0. [F]

**Spot audit** (seeded random 15 rows each in T1, T2 and T3, plus the 20 largest T1 rows, read by hand): no false positive was found. That is evidence of precision on large rows, not a measured error rate. [F]

### 2.4 Sponsor tiers

The panel mixes pure DAF sponsors with universities and fiscal sponsors, so results are reported in nested tiers:

| Tier | Definition | Why |
|---|---|---|
| T1 core | FY2024 top-50 sponsors classed National (Standard or Donation Processor), plus NCF, Jewish Communal Fund, DonorsTrust and Thrivent (top-50 single-issue sponsors that are mainly DAF administrators; a judgment) | Inflows are almost all DAF contributions |
| T2 | Other DAFRC National sponsors and processors (e.g. AOGF, Blackbaud Giving Fund, Charities Aid Foundation America, Rockefeller Philanthropy Advisors, Amalgamated Charitable Foundation) | Mix of DAFs, fiscal sponsorship and pass-through giving |
| T3 | Community foundations | PF grants fund DAFs *and* CF programmes or field-of-interest funds |
| T4 | Other single-issue panel members (universities, hospitals, federations, other charities) | Mostly ordinary grants to the charity; shown only as an upper bound |
| T0 | DAF-labelled lines with no identifiable sponsor | DAF money, sponsor unknown |

As a lower-bound check on matching, the script also reports each tier using only alias and EIN matches (`by_tier_alias_or_ein_only`). T1 is still $2.04bn, $2.40bn and $3.19bn on that basis. [F]

### 2.5 Wind-downs

**"Terminating"** means the return carries `FinalReturnInd` or a §507(b)(1)(A) flag. **"Conversion signature"** means the PF's grants to a tier were at least 50% of its beginning-of-year book assets, with book assets of at least $100k; such a return may or may not be flagged.

## 3. Results

### 3.1 Totals by year [F]

| | TY2022 | TY2023 | TY2024 | 3-yr |
|---|---|---|---|---|
| 990-PF returns parsed | 121,848 | 124,598 | 124,912 | 371,358 |
| PF grants paid (all recipients) | $117.70bn | $125.45bn | $130.50bn | $373.65bn |
| **T1 core: $** | **$2.55bn** | **$2.96bn** | **$3.91bn** | **$9.43bn** |
| T1: PFs / grant lines | 1,423 / 1,850 | 1,615 / 2,025 | 1,756 / 2,188 | 2,801 PFs |
| T1-T2: $ | $3.49bn | $3.96bn | $5.23bn | $12.68bn |
| T1-T3: $ | $4.88bn | $5.41bn | $7.05bn | $17.34bn |
| T1-T3: PFs | 6,198 | 6,669 | 6,639 | 10,623 PFs |
| All panel incl. T4: $ | $7.80bn | $8.97bn | $10.29bn | $27.06bn |
| T0 DAF-labelled, sponsor unknown | $0.15bn | $0.28bn | $0.49bn | $0.92bn |
| T1 as % of PF grants paid | 2.2% | 2.4% | 3.0% | |
| T1-T3 as % of PF grants paid | 4.1% | 4.3% | 5.4% | |
| T1-T3 $ whose purpose text says DAF / donor advised | $0.55bn (11%) | $0.82bn (15%) | $1.26bn (18%) | |

**Itemisation.** Itemised XML lines equal 98.7%, 98.4% and 98.2% of grants paid. Each year about 1,200-1,330 returns report grants paid but itemise none ($1.57bn, $2.06bn and $2.32bn of grants paid). Their sponsor grants, if any, are missed. [F]

**T0 concentration.** One PF’s two lines ($291.6m in TY2024 and $141.1m in TY2023) are 47% of T0, and a few T0 lines do name a panel sponsor (for example Community Foundation of Sarasota County, $9.0m), so T0 is mostly, not wholly, unattributed. [V wave 49B]

### 3.2 Against the repo's DAF contribution totals [F]

The denominator is DAFRC corrected market DAF contributions ([`dafrc-corrected-market-totals.csv`](../../data/mission-2026-11-14/dafrc-corrected-market-totals.csv), `corrected_value`):

| | FY2022 | FY2023 | FY2024 |
|---|---|---|---|
| DAF contributions (DAFRC corrected) | $76.48bn | $65.37bn | $92.77bn |
| T1 ÷ contributions | 3.3% | 4.5% | 4.2% |
| T1 + T0 ÷ contributions | 3.5% | 5.0% | 4.7% |
| T1-T2 ÷ contributions | 4.6% | 6.1% | 5.6% |
| T1-T3 ÷ contributions (upper bound) | 6.4% | 8.3% | 7.6% |

**Reading [I].** Private foundations supply roughly **4-5 cents of every DAF contribution dollar** at the core national sponsors' level, and at most about 8 cents under the broadest DAF-relevant definition. Most DAF money comes from other sources: individuals, estates and corporations.

**PF grant to sponsor, then DAF grant out.** A PF grant to a DAF sponsor is a qualifying distribution for the PF. The money then counts again as a DAF contribution, and later as a DAF grant. The repo's netting work (DAF-to-DAF, [`daf-to-daf-flows-top50.csv`](../../data/mission-2026-11-14/daf-to-daf-flows-top50.csv)) does not net PF-to-DAF flows. These are flows into the DAF system from outside it, not double counts within it. [I] Validator check: the DAF-to-DAF file reads Form 990 Schedule I and this file reads 990-PF Part XV, so no row is in both. Two DAFRC-panel sponsors filed 990-PFs: Jasper Ridge Charitable Fund (final §507(b)(1)(A) return, TY2023, $4.2m to Schwab and Fidelity) and Every.org (TY2024, $0.5m to T2 processors); those $4.7m are sponsor-to-sponsor transfers in substance (0.03% of T1-T3). [V wave 49B]

### 3.3 Concentration (top PFs) [F]

| T1 core | TY2022 | TY2023 | TY2024 | 3-yr |
|---|---|---|---|---|
| PFs | 1,423 | 1,615 | 1,756 | 2,801 |
| Top-1 share | 10.8% | 7.4% | 6.7% | 7.8% |
| Top-10 share | 36.1% | 32.1% | 34.3% | 30.9% |
| Top-50 share | 61.2% | 58.0% | 60.2% | 53.9% |
| Top-100 share | 73.1% | 70.0% | 71.2% | 64.7% |

For T1-T3 over three years: 10,623 PFs; top-1 4.3%, top-10 17.5%, top-50 38.7%, top-100 50.8%.

**Largest PF grantors to T1, three-year total** (organisation names from the IRS index; care-of names removed):

| PF (EIN) | T1 receipts | Terminating in window |
|---|---|---|
| The Carl Victor Page Memorial Foundation (20-1922957) | $731.4m | no |
| H&H Evergreen Foundation (46-5066162) | $564.5m | no |
| The Paul E Singer Foundation (27-2009342) | $416.2m | no |
| Pivotal Philanthropies Foundation (88-2918646) | $261.0m | no |
| The Jen-Hsun & Lori Huang Foundation (26-1551239) | $184.3m | no |
| NSN Foundation Inc (22-3769097) | $169.5m | no |
| A Good Name Foundation Inc (58-1375066) | $156.6m | no |
| Horowitz Family Foundation (35-7050910) | $144.1m | no |
| Aurora Foundation (36-7634806) | $143.6m | no |
| The Zoom Foundation (06-1600601) | $139.4m | no |

The largest return-sponsor rows (one PF return to one sponsor, filed lines summed; the largest single filed lines are $275.0m in TY2022 and $242.5m and $235.0m in TY2024, all to NPT) include: [V wave 49B]
- $276.0m to NPT (TY2022);
- $257.5m to NPT (TY2024);
- $236.3m to NPT (TY2024);
- $218.0m and $220.7m to Schwab Charitable;
- $161.5m to the J.P. Morgan Charitable Giving Fund (NPT program; the filed address line reads National Philanthropic Trust, Jenkintown PA). [V wave 49B]

The flow is therefore lumpy: one or two PFs move a year's T1 total by $0.2-0.3bn. [F]

**By recipient, three years** [F]:
- NPT $2.38bn (582 return-sponsor rows);
- Fidelity Charitable $2.18bn (1,458);
- Schwab/DAFgiving360 $1.77bn (844);
- Vanguard Charitable $0.79bn (422);
- Jewish Communal Fund $0.54bn (357);
- NCF $0.48bn (429);
- GS DAPF $0.27bn (173).

In T2, AOGF received $0.96bn, Rockefeller Philanthropy Advisors $0.88bn and Charities Aid Foundation America $0.42bn. These are mainly pass-through or fiscal-sponsor flows, not DAFs.

### 3.4 Share of each top-50 sponsor's contributions that comes from PFs [F]

**Denominator.** Each sponsor's DAF contributions in the league table (DAFRC Schedule D Part I line 2, same-numbered FY). The table shows PF receipts / contributions ($m) and the share. T3 and T4 rows are ratios, not DAF shares, because the numerator includes non-DAF grants.

| Rank | Sponsor | Segment | TY/FY2022 | TY/FY2023 | TY/FY2024 |
|---|---|---|---|---|---|
| 1 | Fidelity Charitable | national | 612.0 / 15,195.9 (4.0%) | 727.7 / 12,620.2 (5.8%) | 836.8 / 15,914.8 (5.3%) |
| 2 | National Philanthropic Trust | national | 648.2 / 13,187.3 (4.9%) | 525.2 / 9,212.4 (5.7%) | 1,203.8 / 14,523.9 (8.3%) |
| 3 | Donor Advised Charitable Giving (Schwab / DAFgiving360) | national | 420.8 / 9,756.2 (4.3%) | 697.6 / 7,319.3 (9.5%) | 648.4 / 9,300.7 (7.0%) |
| 4 | Vanguard Charitable | national | 215.2 / 3,020.7 (7.1%) | 231.5 / 2,359.7 (9.8%) | 344.2 / 5,746.9 (6.0%) |
| 5 | GS Donor Advised Philanthropy Fund | national | 49.1 / 1,659.6 (3.0%) | 116.1 / 2,448.5 (4.7%) | 101.6 / 5,833.8 (1.7%) |
| 6 | Silicon Valley Community Foundation | CF | 68.4 / 2,317.0 (3.0%) | 59.4 / 1,112.5 (5.3%) | 127.1 / 2,835.1 (4.5%) |
| 7 | Morgan Stanley GIFT | national | 34.6 / 1,250.4 (2.8%) | 33.0 / 1,875.5 (1.8%) | 67.4 / 2,959.4 (2.3%) |
| 8 | American Endowment Foundation | national | 51.7 / 1,305.5 (4.0%) | 42.9 / 1,171.5 (3.7%) | 33.8 / 1,690.2 (2.0%) |
| 9 | Renaissance Charitable Foundation | national | 8.8 / 914.6 (1.0%) | 9.5 / 1,348.1 (0.7%) | 69.9 / 2,159.9 (3.2%) |
| 10 | National Christian Foundation | core single-issue | 173.3 / 2,232.0 (7.8%) | 137.4 / 2,184.5 (6.3%) | 172.1 / 2,907.6 (5.9%) |
| 11 | Bank of America Charitable Gift Fund | national | 22.6 / 949.4 (2.4%) | 34.0 / 1,020.5 (3.3%) | 29.1 / 1,489.7 (2.0%) |
| 12 | Chicago Community Trust | CF | 21.5 / 1,580.0 (1.4%) | 28.5 / 1,325.1 (2.1%) | 12.3 / 1,727.5 (0.7%) |
| 13 | ImpactAssets | national | 40.7 / 371.9 (11.0%) | 127.8 / 796.9 (16.0%) | 77.0 / 611.9 (12.6%) |
| 14 | Jewish Communal Fund | core single-issue | 156.2 / 862.5 (18.1%) | 197.5 / 934.5 (21.1%) | 185.4 / 876.3 (21.2%) |
| 17 | Greater Horizons | national | 13.8 / 388.9 (3.5%) | 15.1 / 763.3 (2.0%) | 22.9 / 633.4 (3.6%) |
| 19 | Raymond James Charitable | national | 0.9 / 668.9 (0.1%) | 15.3 / 374.2 (4.1%) | 9.4 / 515.6 (1.8%) |
| 20 | Dechomai Asset Trust | processor | 0.0 / 524.7 (0.0%) | 0.0 / 960.6 (0.0%) | 27.7 / 674.6 (4.1%) |
| 23 | DonorsTrust | core single-issue | 56.1 / 300.3 (18.7%) | 23.1 / 224.4 (10.3%) | 33.1 / 285.5 (11.6%) |
| 24 | US Charitable Gift Trust | national | 2.3 / 198.2 (1.2%) | 1.7 / 229.1 (0.7%) | 0.5 / 314.1 (0.1%) |
| 25 | Ayco Charitable Foundation | national | 9.4 / 251.7 (3.7%) | 4.0 / 251.1 (1.6%) | 9.7 / 317.7 (3.0%) |
| 30 | Servant Foundation | national | 0.3 / 883.0 (0.0%) | 2.1 / 843.8 (0.2%) | 0.2 / 511.7 (0.0%) |
| 32 | Bessemer Giving Fund | national | 9.9 / 114.9 (8.6%) | 5.8 / 129.2 (4.5%) | 21.7 / 254.7 (8.5%) |
| 35 | The Signatry Charitable Trust | national | 8.0 / 134.4 (6.0%) | 12.6 / 138.1 (9.1%) | 7.8 / 997.9 (0.8%) |
| 43 | American Gift Fund | national | 3.7 / 115.0 (3.3%) | 3.1 / 139.1 (2.3%) | 1.0 / 123.8 (0.8%) |
| 46 | T. Rowe Price Program for Charitable Giving | national | 12.7 / 151.0 (8.4%) | 1.7 / 102.5 (1.6%) | 9.3 / 125.0 (7.5%) |
| 47 | Thrivent Charitable Impact & Investing | core single-issue | 0.0 / 66.1 (0.0%) | 0.0 / 70.5 (0.0%) | 0.0 / 134.7 (0.0%) |
| 27 | Boston Foundation | CF (ratio) | 38.3 / 271.4 (14.1%) | 34.4 / 102.5 (33.6%) | 61.0 / 124.9 (48.9%) |
| 29 | Community Foundation for Greater Atlanta | CF (ratio) | 30.0 / 90.3 (33.2%) | 146.3 / 240.5 (60.8%) | 133.3 / 244.2 (54.6%) |
| 45 | Minneapolis Foundation | CF (ratio) | 18.0 / 94.1 (19.1%) | 27.1 / 66.5 (40.8%) | 39.5 / 56.3 (70.1%) |
| 48 | San Francisco Foundation | CF (ratio) | 35.6 / 143.9 (24.7%) | 64.2 / 114.4 (56.1%) | 46.7 / 88.3 (52.9%) |

`sponsor_shares_top50` in the summary JSON lists all 50. Its university rows (Stanford, UCLA Foundation) exceed 100% because they compare all PF grants to a university with its small DAF book.

**Reading [I]**:
- The four largest national sponsors take **4-10%** of their DAF contributions from PFs.
- Faith-based and ideological sponsors with institutional donor bases (JCF, DonorsTrust) and the impact-investing sponsor ImpactAssets take **10-21%**.
- A few sponsors take **under 1%**: Servant Foundation, Thrivent, and US Charitable Gift Trust (FY2023-2024). Their PF receipts are small under every match method, so this is not an alias gap. The reason, whether a donor base without PFs or PF grants filed under other names, is not established.

### 3.5 Wind-downs: foundations terminating into DAF sponsors [F]

| | TY2022 | TY2023 | TY2024 | 3-yr |
|---|---|---|---|---|
| Returns flagged final or §507(b)(1)(A) | 2,418 | 2,692 | 2,910 | 8,020 |
| …of which §507(b)(1)(A) | 385 | 447 | 497 | 1,329 |
| (§507(b)(1)(B) 60-month, excluded) | 357 | 378 | 371 | 1,106 |
| Grants paid by terminating PFs | $1.91bn | $1.78bn | $2.01bn | $5.70bn |
| Terminating returns with a T1 grant | 130 (5.4%) | 196 (7.3%) | 199 (6.8%) | 525 |
| Terminating returns with a T1-T3 grant | 254 (10.5%) | 303 (11.3%) | 320 (11.0%) | 877 |
| Terminating → T1 $ | $185.4m | $289.9m | $271.0m | $746.2m |
| Terminating → T1-T3 $ | $355.8m | $408.1m | $455.9m | $1,219.9m |
| …as % of tier total, T1 | 7.3% | 9.8% | 6.9% | 7.9% |
| …as % of tier total, T1-T3 | 7.3% | 7.5% | 6.5% | 7.0% |
| …as % of terminating PFs' grants paid (T1-T3) | 18.6% | 22.9% | 22.7% | |
| Terminating → T0 (DAF-labelled, sponsor unknown) | $37.7m | $28.4m | $46.7m | $112.7m |

- **§507(b)(1)(A) subset.** 189 returns gave $345.6m to T1-T3, of which 101 returns and $181.4m went to T1.
- **Typical case.** A terminating PF that gave to a T1-T3 sponsor had median beginning-of-year book assets of **$410k** and gave **$295k**. Wind-downs into DAFs are mostly small foundations.
- **Largest wind-downs to sponsors, three years** (organisation names; sponsor in brackets):
  - The Holocene Foundation, TY2024, $56.4m (Vanguard Charitable; final return, no §507(b)(1)(A) flag);
  - Fund for Art Science and Technology, TY2024, $45.5m (Silicon Valley CF);
  - Cherese Mari Laulhere Foundation, TY2023, $44.4m (Orange County CF; §507(b)(1)(A));
  - **Cognizant US Foundation, TY2022, $35.6m (BNY Mellon Charitable Gift Fund; §507(b)(1)(A) and final return)**;
  - HWR Charitable Foundation, TY2022, $30.4m (Marin CF);
  - The Perrin Family Foundation, TY2023, $23.1m (Bank of America CGF and ImpactAssets; §507(b)(1)(A)).
- **Cross-check.** The Cognizant row independently confirms the repo's earlier finding that Cognizant "converted its US private foundation into a DAF in late 2022" ([direction-corporate-dafs.md](direction-corporate-dafs.md)).

**Conversion signature: unflagged wind-downs.** Over three years, 962 return-years sent at least 50% of beginning-of-year book assets to T1-T3 sponsors (book assets ≥ $100k):
- 524 of these were flagged terminating;
- **438 were not.** Many are probably foundations that empty into a DAF in one year and file the final return the next (proposal P-B4901-02);
- for T1 alone the counts are 581 return-years, 349 of them flagged.

Separately, PFs whose sponsor grants were at least 50% of their grants paid number 1,375, 1,484 and 1,604 a year in T1-T3, with $3.0bn, $3.3bn and $4.6bn. These are mostly ongoing "PF-to-DAF pass-through" funders, not wind-downs.

**Answer to the second question [F][I].** On the flags the IRS asks for, **about 7-8% of PF-to-DAF-sponsor dollars come from foundations in their final year**: $0.75bn of $9.43bn in T1 and $1.22bn of $17.34bn in T1-T3. By count, about **one in nine** winding-down foundations sends money to a DAF sponsor in its final year. Counting the 438 unflagged asset-test cases would raise the dollar share, but the three-year window cannot confirm that they are wind-downs.

### 3.6 Robustness and recall [F]

- **Alias and EIN only.** Without any name-based matching, T1 is still $2.04bn, $2.40bn and $3.19bn: 80%, 81% and 81% of the full T1 figures.
- **Recall review.** The script lists DAF-looking candidate lines that matched nothing (`unmatched_review`). The largest groups are:
  - lines labelled only "DAF" or "Donor Advised Fund" (in T0);
  - "Jewish Community Foundation" with a CA address ($137m; ambiguous between the San Diego and Los Angeles foundations, so left unmatched);
  - "The Chicago Community Foundation" ($127m). This is a separate EIN, 36-3432023, held c/o The Chicago Community Trust and not in the DAFRC panel, so it is excluded;
  - "Christian Community Foundation" in TN ($85m; generic name).

  Together these come to about 2% of the T1-T3 total ($349m of $17.34bn).
- **Brand-name misses (validator).** Re-running `match_line` over every cached candidate line leaves about 565 lines and $188m over three years ($64m, $56m and $69m) that name a T1 brand in a misspelt or abbreviated form (for example “FIDELITY INV CHARITABLE GIFT FUND”, “GOLDMAN SACHS PHILANTHROPHY FUND”, “SCHWAB FUND FOR CHARITABLE GIVING”, “TROWE PRICE - DONOR ADVISED FUND”). That is about 2.0% of T1, so T1 is a floor. T2-T3 misses include Tides Foundation (state rule), St Louis Community Foundation (two panel EINs share the name) and Community Foundation of Sarasota County. [V wave 49B]
- **Precision.** A seeded hand audit of 45 random rows (15 each in T1, T2 and T3) and the 20 largest T1 rows found no false matches. The audit ran on the build before the last alias additions (brand plus "DAF" wording, and the generic-name block), which changed T1 by under 1.5%. An independent re-read of 37 matched rows in raw XML (14 T1, 8 T2 and 10 T3 drawn with a new seed, the 4 largest T1 rows and the Cognizant row) found all 37 correct; the 95% lower bound on precision is about 91%. [V wave 49B] Rows such as "MCHPP" → AOGF are correct: the full filed name is "MCHPP - AMERICAN ONLINE GIVING FOUNDATION".

## 4. Limits

- **Matching is name-based.** 990-PF Part XV has no recipient-EIN field. Of 74,266 return-sponsor rows (all tiers, before the CSV filter), 93% rest on exact or first-segment names, 6% on brand aliases and 0.1% on an EIN written in the text. Recall is incomplete (§3.6), and T0 ($0.92bn) is DAF money whose sponsor is unknown.
- **T3 and T4 are not DAF-only.** PF grants to community foundations and universities largely fund programmes. Only 11-18% of T1-T3 dollars carry DAF wording, but that wording is optional, so this is not a DAF share. T1 is the defensible "into DAFs" figure.
- **T1 includes some non-DAF receipts.**
  - NCF, JCF and DonorsTrust also hold some non-DAF funds. Without the four judgment additions (NCF, JCF, DonorsTrust, Thrivent), T1 is $2.17bn, $2.61bn and $3.52bn ($8.29bn), or 2.8%, 4.0% and 3.8% of DAF contributions; Thrivent receives nothing in any year. [V wave 49B]
  - NPT, Fidelity Charitable and others receive some PF grants for pooled or sponsor-level funds. A few purpose texts say "general operating"; for a DAF sponsor that usually still means a DAF credit, but this is not verified.
- **Timing.** PF tax year ≠ sponsor FY for non-calendar filers, and a PF grant may be booked by the sponsor in the next FY. Per-sponsor ratios for single years are therefore noisy, particularly for lumpy recipients (NPT 2024, Atlanta CF).
- **Missing returns.**
  - 1 frame return has no XML.
  - About 1,200-1,330 returns a year report grants without itemised XML lines ($1.6-2.3bn of grants paid).
  - Paper-filed 990-PFs, if any remain, are outside the e-file index. Their number was not measured.
- **Candidate filter during harvest.** Lines were kept only when they looked DAF-like or matched a *unique* panel name under the key table at harvest time. A later version of the key table (state-disambiguated, de-duplicated names) is a superset. Re-running `harvest` with today's script would keep slightly more lines; ambiguous-name lines without DAF words in the name are the at-risk set.
- **Termination flags are self-reported.**
  - Some final returns are filed by PFs that merge or move rather than wind down.
  - `OrganizationDissolvedEtcInd` (Part VI-A line 5) is reported but not used. It counted 2,899, 3,194 and 3,437 "Yes" answers, more than the final-return counts.
- **DAFRC denominators.** FY2024 contains many imputed sponsor rows (see `dafrc-corrected-market-totals.csv`).
- **Privacy.** PF names are organisation names from public filings. Care-of names are stripped. Recipient fund names are truncated at the first separator in the CSV, so "FBO person" tails are dropped. No individual is profiled. However, the cut keeps names that lead the string: the validator found individual donor or account-holder names in `recipient_name_filed` (named giving accounts and named funds) and in `purpose_text` (named family DAFs, in-memory purposes), about 176 rows on a tight name heuristic. Before wider use, blank `purpose_text` or replace it with a DAF flag, and cut `recipient_name_filed` to the matched sponsor brand. [V wave 49B] **Done 2026-11-20:** both fields are redacted in the CSV and in the script (1,031 of 29,204 rows carry the DAF-wording flag).

## 5. Data dictionary: `pf-to-daf-flows-2026-11-20.csv`

**Rows.** One row per (990-PF return, matched sponsor), or per return for T0. All T0-T3 rows are included. T4 rows are included only where the line text says DAF or donor advised, or the PF is terminating. The summary JSON aggregates all rows, including the omitted T4 rows.

**Derivable columns.**
- XML URL = `https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{return_object_id}_public.xml`. For the 1,953 returns that came from IRS bulk zips, the zip is the one named by the index `XML_BATCH_ID`, or its sibling volume.
- Source for every row: IRS Form 990-PF Part XV line 3a, e-file XML; frame = IRS TEOS index 2023-2026; sponsors = DAFRC 2025 panel.

| Column | Meaning |
|---|---|
| pf_ein | 990-PF filer EIN (9 digits) |
| pf_name | Filer name from the IRS index, with care-of/attention tails removed |
| tax_year | 990-PF tax year (year the period begins) |
| tax_period | YYYYMM period end (IRS index) |
| return_object_id | IRS e-file object id (latest submission for the EIN-period) |
| pf_final_return | 1 if Heading item G "Final return" is checked |
| pf_507b1a | 1 if item E §507(b)(1)(A) termination is checked |
| pf_507b1b_60month | 1 if item F 60-month §507(b)(1)(B) termination is checked (not a wind-down) |
| pf_dissolved_ind | 1 if Part VI-A line 5 (liquidation, termination, dissolution or substantial contraction) is answered Yes |
| pf_terminating | 1 if pf_final_return or pf_507b1a |
| pf_fmv_assets_eoy | Item I, FMV of all assets at end of year (USD) |
| pf_book_assets_boy | Part II total assets, beginning of year, book value (USD) |
| pf_total_grants_paid | Part XV 3a total, else Part I line 25, else the sum of itemised lines (USD) |
| sponsor_ein | Matched DAFRC panel EIN (blank for T0) |
| sponsor_name, sponsor_type, sponsor_subtype | DAFRC panel name, type and subtype (latest year) |
| sponsor_segment | national / processor / community_foundation / university_hospital / single_issue (as in mission_net_payout.segment_of) |
| sponsor_tier | T1_core_top50, T2_national_other, T3_community, T4_single_issue, T0_daf_label_unattributed (§2.4) |
| sponsor_rank_fy2024 | FY2024 asset rank in the league table (blank if outside the top-50) |
| match_method | ein_in_text / name_exact / name_first_segment / alias / daf_label_only (several joined by ";") |
| lines | Number of Part XV lines aggregated in the row |
| amount_usd | Sum of the lines' amounts (USD) |
| daf_purpose_amount_usd | Part of amount_usd on lines whose name or purpose says DAF or donor advised |
| largest_line_usd | Largest single line (USD) |
| share_of_pf_grants_paid | amount_usd ÷ pf_total_grants_paid |
| recipient_name_filed | Redacted 2026-11-20 (“[redacted; see sponsor_name]”): filed names can carry donors’ or account holders’ names. The raw text stays in the source XML |
| purpose_text | Redacted 2026-11-20 to a flag: “DAF wording” if any line's purpose says donor-advised or DAF, else “[redacted]” |

## 6. Source register (primary URLs)

| # | Source | URL | Used for |
|---|---|---|---|
| S1 | IRS TEOS e-file index, 2023-2026 | https://apps.irs.gov/pub/epostcard/990/xml/2023/index_2023.csv (and 2024, 2025, 2026) | Frame; the 2026 file was re-fetched on 20 Nov 2026 (Last-Modified 18 Nov 2026) |
| S2 | IRS Form 990 series downloads page (bulk zips) | https://www.irs.gov/charities-non-profits/form-990-series-downloads | Bulk-zip provenance |
| S3 | IRS bulk zips used | https://apps.irs.gov/pub/epostcard/990/xml/2026/2026_TEOS_XML_10A.zip ; https://apps.irs.gov/pub/epostcard/990/xml/2026/2026_TEOS_XML_05B.zip | 1,953 XMLs missing from the GT mirror (range requests) |
| S4 | GivingTuesday 990 data lake (mirror of IRS TEOS XML) | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml | 369,405 XMLs |
| S5 | IRS, Instructions for Form 990-PF (items E, F, G; Part XV) | https://www.irs.gov/instructions/i990pf | Definitions of §507(b)(1)(A) termination, 60-month termination, final return |
| S6 | IRS, Termination of private foundation status | https://www.irs.gov/charities-non-profits/private-foundations/termination-of-private-foundation-status | Legal frame |
| S7 | IRS Exempt Organizations Business Master File extract | https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf | Panel EIN legal names and states (cached eo1-eo4.csv) |
| S8 | DAFRC Annual DAF Report 2025, updated dataset | https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx | Sponsor universe, per-sponsor contributions (via repo CSVs) |
| R1 | Repo: DAFRC corrected market totals | data/mission-2026-11-14/dafrc-corrected-market-totals.csv | Market DAF contribution denominators |
| R2 | Repo: sponsor league table | data/mission-2026-11-14/daf-sponsor-league-table-fy2021-2025.csv | Top-50 ranks, per-sponsor contributions |
| R3 | Repo: J.P. Morgan Charitable Giving Fund as NPT program | research/mission-2026-11-14/queue-ren-iphi-attrition.md | Alias JPM CGF → NPT (EIN 23-7825575) |
| R4 | Repo: Cognizant PF-to-DAF conversion | research/mission-2026-11-14/direction-corporate-dafs.md | Cross-check of §3.5 |

## 7. Robots and terms log (checked 20 Nov 2026, user agent `research-script/1.0`)

| Host | robots.txt result | Action |
|---|---|---|
| gt990datalake-rawdata.s3.amazonaws.com | 404 (NoSuchKey): no robots file | Fetched XML objects |
| apps.irs.gov | `/robots.txt` redirects to an irs.gov 404 page: no robots file | Fetched index CSVs; bulk zips by range |
| www.irs.gov | Only a `User-agent: *` group; no ClaudeBot / anthropic-ai / Claude-* groups. `/instructions/` and `/charities-non-profits/` are not disallowed | Read two instruction/guidance pages |
| www.nptrust.org | `User-agent: *` with empty Disallow; only YisouSpider and Baiduspider blocked | Read the sitemap only (no page used as evidence) |

Not used: sec.gov, crt.sh, certspotter, charitynavigator.org, ncfgiving.com, and the Foundant and fcsuite hosts.

## 8. Reproduce

```
CACHE=<scratch>/b4901/cache ; IRS=<dir with index_2023..2026.csv and eo1-eo4.csv>
python3 scripts/mission_pf_to_daf_flows.py . frame   --irs-dir $IRS --cache $CACHE --bmf-dir $IRS
python3 scripts/mission_pf_to_daf_flows.py . extend  --irs-dir $IRS --index-2026 <newer index_2026.csv> --cache $CACHE --bmf-dir $IRS
python3 scripts/mission_pf_to_daf_flows.py . harvest --cache $CACHE --bmf-dir $IRS --procs 48      # ~35 min, 371k XMLs
python3 scripts/mission_pf_to_daf_flows.py . bulk    --irs-dir $IRS --index-2026 <newer index_2026.csv> --cache $CACHE --bmf-dir $IRS
python3 scripts/mission_pf_to_daf_flows.py . build   --cache $CACHE --bmf-dir $IRS                  # writes the CSV and $CACHE/pf_to_daf_summary.json
```

The harvest is resumable: chunks are written atomically and keyed by object id. The cache (gzip JSONL, about 30 MB) is in the session scratchpad and is not committed.
