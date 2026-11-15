# Direction: executive compensation and staffing at the 50 largest DAF sponsors, TY2021–2025

**Date:** 2026-11-15 · **Agent:** batch43 N24 · **Queue item:** P-NEW-EXC-01 (owner direction, `data/mission-2026-11-14/research-priority-queue.csv`)

**Outputs**
- [`data/mission-2026-11-14/sponsor-executive-compensation-2021-2025.csv`](../../data/mission-2026-11-14/sponsor-executive-compensation-2021-2025.csv): 1,277 rows: 225 sponsor-year returns, 1,019 person rows (top officer plus up to five highest-paid), 27 segment-year aggregates and 6 segment trend rows (§10).
- [`data/mission-2026-11-14/queue-proposals-batch43-n24.csv`](../../data/mission-2026-11-14/queue-proposals-batch43-n24.csv): P-B43N24-01 to -03.
- **Script:** [`scripts/mission_sponsor_compensation.py`](../../scripts/mission_sponsor_compensation.py). It is new, stdlib only and written in a functional style. It reuses `mission_990_contractors` helpers and the batch-35 TEOS range-request zip reader.

**Conventions**
- **TY** is the year in which the tax period *begins*: TY2021 = periods ending 2021-12 to 2022-11. **FY** is the year in which the period ends (DAFRC convention).
- **Recency:** every return is TY2021–TY2025.
- **Labels:** **[F]** filed value; **[C]** script computation; **[I]** inference or classification; **[U]** not found.
- **Names:** individuals are named only in the top-50 table (§3), exactly as the return spells them. Everywhere else, including aggregates and the digital-first supplement, people appear only by role.
- **Governing corrections read first:**
  - [sponsor-cost-structure-and-sensitivities.md](sponsor-cost-structure-and-sensitivities.md), wave 5:
    - "operating cost" excludes lines 1–4 and 11f;
    - the Givinga account unit is undefined;
    - Fidelity's cost figures are labelled "latest 990 (FY Jun-2024/25)".
    - The context columns here come from that file's `operating_cost_ex_invest_mgmt`, and Givinga per-account ratios are not interpreted.
  - [queue-batch38-data-followups.md](queue-batch38-data-followups.md), wave 23 item 6: NPT's FTE figure is "at most $136,066 wages per FTE". This batch uses W-2 head counts only and makes no FTE claim.
- **Access:**
  - robots.txt was read before fetching. The GivingTuesday S3 mirror returned 404 (no robots file). apps.irs.gov redirects (302).
  - 219 returns came from the mirror. 6 came from IRS TEOS zips by HTTP range request.
  - No logins, forms or contact. **This is research, not legal or tax advice.**

---

## 0. Bottom line

1. **Coverage.** All 225 Form 990s indexed for the 55 EINs (top 50 plus 5 digital-first) in TY2021–2025 were read: 56, 55, 55, 56 and 3 returns by tax year. There are no failures [C]. Every TY2024 top officer paid over $150k (39) has a Schedule J Part II row, and in every case its total equals Part VII columns D+E+F [F/C].
2. **Most affiliated-commercial sponsors carry no executive pay on their own 990.**
   - **[F]** In TY2024, 10 of the 12 affiliated-commercial sponsors in the top 50 report either a $0 top officer or only an institutional trustee:
     - Fidelity Charitable, GS DAPF, MS GIFT, Renaissance, Ayco, US Charitable Gift Trust, T. Rowe Price and Raymond James report $0 top officers;
     - BofA and Bessemer list only an institutional trustee.
   - **[F]** Only DAFgiving360 (President $967,879) and Vanguard Charitable (President $608,684) pay a top officer from the sponsor.
   - **[F] Schedule O states where the pay sits:**
     - Fidelity Charitable: "engages FMR LLC ... pursuant to a services agreement";
     - US Charitable Gift Trust: "all officers of the trust are employees of 474 MS Services Group, Inc. or Eaton Vance Distributors, Inc. and receive no compensation from the trust";
     - DAFgiving360: the workforce "are employees of Charles Schwab & Co." under an administrative services agreement. Even so, it books $40.6m of Part IX lines 5–10 and the President's pay as its own.
3. **Pay per $ of DAF assets differs by one to two orders of magnitude between nationals and community foundations [C].** TY2024 figures:

   | Segment | Top-officer pay per $bn of DAF assets | Top-officer pay per 1,000 accounts | Part IX lines 5–10 (pooled) |
   |---|---|---|---|
   | Self-staffed nationals | NPT **$14,336**; DAFgiving360 $20,440; Vanguard $22,534; AEF $76,458 | NPT $38,727; DAFgiving360 $7,532 | NPT 6.9 bps; DAFgiving360 8.6 bps; Vanguard 5.6 bps |
   | Community foundations (median of 21) | **$733,697** | $877,615 | **78.7 bps** of DAF assets (median 106.7 bps; 52.2 bps of *total* assets) |
   | Faith / single-issue (median) | $504,383 | — | 66.4 bps |
   | Affiliated-commercial (pooled) | — | — | **2.9 bps** |

   - Community-foundation pay is whole-organisation pay. Those foundations also run endowment and grantmaking programmes, so the DAF ratios overstate DAF-attributable pay (§9).
4. **Absolute pay is similar; the base is not.**
   - **[F/C]** TY2024 median top-officer pay (paid officers only) is $725,134 at community foundations, $664,762 at faith / single-issue, $595,238 at independent nationals and $788,282 at the two paid affiliated-commercial sponsors.
   - **[C]** Pay barely scales with size. Among the 21 community foundations, the log-log slope of top-officer pay on total assets is **0.23** (r² 0.34). Across 34 paid non-university sponsors it is 0.08 against total assets and 0.05 against DAF assets.
   - **[I]** Executive pay is close to a fixed cost per organisation. Nationals spread it over far more DAF assets: per $bn, community-foundation pay is 10–51× that of the four self-staffed nationals.
5. **Pay paid by related organisations is concentrated in a few structures [F].** In TY2024, Part VII column E is positive at only 6 sponsors:
   - **Greater Horizons:** 90% of its Part VII pay sits in column E. Its President is the Greater Kansas City Community Foundation CEO, filed on both returns.
   - **The Signatry Charitable Trust:** 93%. Its President is the Servant Foundation CEO.
   - **UCLA Foundation:** 85%. Staff are employees of the UC Regents.
   - **ImpactAssets:** 8%. The CEO's pay is split between the organisation and related organisations.
   - **Tulsa CF:** 20%.
   - **Denver Foundation:** 8%.

   Affiliated-commercial parents (FMR, Goldman Sachs, Morgan Stanley, Schwab) are **not** reported as related organisations for pay. Column E is $0 at every affiliated-commercial sponsor in every year, so their officers' pay is simply absent from the 990.
6. **Trends, TY2021→TY2024, matched sponsors [C]:**

   | Segment | Top-officer pay (median growth/yr) | Part IX lines 5–10 (median growth/yr) | DAF assets (median growth/yr) | Pay per $bn of DAF assets (median) |
   |---|---|---|---|---|
   | Community foundations (21) | **+6.6%** (pooled +7.7%) | +9.7% | **+4.5%** (pooled +1.0%) | rose from $584,536 to $733,697 |
   | Faith / single-issue (8 paid) | +11.3% | +10.3% | +8.0% | — |
   | Independent nationals (4 paid) | +3.4% | +16.1% | **+25.5%** | fell from $140,879 to $124,880 |

   - **[I]** Pay per $ of DAF assets is falling at nationals and rising at community foundations.

## 1. Method

### 1.1 Universe
- **Ranking:** FY2024 end-of-year DAF assets from the DAFRC panel ([dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)), with applied corrections from `dafrc-corrections-itemized.csv` (`daf_assets_eoy`, applied = 1).
  - The corrections promote The Signatry Charitable Trust (filed $796.8m against DAFRC's $403.7m) into the top 50, at #35. They push Seattle Foundation to #52.
  - The 50th sponsor holds $581m of DAF assets.
- **Supplement (outside the top 50, labelled):** five digital-first sponsors named in [direction-donor-feature-census.md](direction-donor-feature-census.md): Daffy, Charityvest, Endaoment, Givinga and GiveClear. Every.org files a 990-PF and is excluded.
- **Segments [I]** (manual table `SEGMENT` in the script):
  - **affiliated_commercial (12):** a national sponsor founded by, branded with or administered by a for-profit financial firm. Fidelity, Schwab (DAFgiving360), Vanguard, Goldman Sachs (GS DAPF), Ayco, Morgan Stanley (MS GIFT), Eaton Vance / Morgan Stanley (US Charitable Gift Trust), BofA, Raymond James, Bessemer, T. Rowe Price, and Renaissance (for-profit administrator).
  - **independent_national (6):** NPT, AEF, ImpactAssets, Greater Horizons (a GKCCF affiliate), Dechomai and American Gift Fund.
  - **community_foundation (21).**
  - **faith_single_issue (9):** NCF, Servant Foundation, The Signatry, Thrivent Charitable (a Thrivent affiliate), JCF, CJP, JCF San Francisco, JCF Los Angeles and DonorsTrust.
  - **university_health (2):** Stanford and the UCLA Foundation. They are shown, but excluded from the comparisons because whole-university payroll swamps the ratios.
  - **digital_first (5):** the supplement.

### 1.2 Returns and extraction
- **Returns:** every `RETURN_TYPE = 990` row for the 55 EINs in IRS `index_2021`–`index_2026` (index_2026 copy of 2026-11-15) with TY 2021–2025.
  - One row is kept per EIN × tax period: the highest object id, so amendments supersede.
  - Where a sponsor changed its fiscal year and has two returns in one TY (DAFgiving360 TY2021; Ayco TY2024), aggregates keep the later period end.
- **Streamed XML extract** (`extract_stream`), cached as JSON per object id:

  | Area | Fields |
  |---|---|
  | **Part VII Section A** | Every person: name, title, average hours (organisation / related organisations), role boxes, columns **D** (reportable compensation from the organisation), **E** (reportable compensation from related organisations) and **F** (other compensation); section totals; line 2 (number over $100k) |
  | **Schedule J Part II** | Every row: base, bonus, other, deferred and non-taxable pay, totals and amounts reported on a prior 990, each for the filing organisation and for related organisations |
  | **Part V line 2a** | W-2 employees; Part I line 5 is kept as a cross-check |
  | **Part IX lines 5–10** | Total column, plus line 25 |
  | **Schedule D Part I** | DAF count and end-of-year value |
  | **Schedule R** | Names of related organisations |
  | **Schedule O** | The first sentence matching an employer or payer pattern ("employees of", "paid by", "compensated by", "administrative services agreement", "has no employees", ...), quoted |

- **Institutional trustees** (Part VII box "institutional trustee": BofA, Bessemer Trust, RBC Trust) are kept out of person-level pay. Their fees go in `institutional_trustee_comp_def`.

### 1.3 Top officer and five highest-paid
- **Top officer:** the current (not "former") officer or key employee whose title ranks first on CEO / chief executive > president > executive director.
  - Vice, VP, assistant, associate and deputy titles do not count as president.
  - Titles marked as past (former, previous, thru, until, left, resigned, ending, senior advisor) rank below current ones.
  - Subsidiary or regional heads (UK, Transatlantic, regional, "SMC") are excluded.
  - Ties go to the higher-paid officer and are flagged `_multiple`.
  - If no title matches, the highest-paid officer working ≥ 20 hours a week is used.
  - One manual override [I]: Stanford's president, since its return lists the CEO of Stanford Management Company first.
- **Five highest-paid:** the five other listed individuals with the largest D+E+F. For community foundations and nationals they are mostly staff; for some affiliated-commercial sponsors they are board fees.
- **Pay measure:** Part VII D+E+F (`comp_total_def`). Schedule J totals are carried alongside and agree for every matched TY2024 top officer paid over $150k.

### 1.4 Ratios (per sponsor-year)
- `top_pay_per_bn_daf` = top-officer D+E+F ÷ (Schedule D EOY DAF value / 1e9). It falls back to the corrected DAFRC same-FY value if Schedule D is blank.
- `top_pay_per_1000_accounts` = top-officer pay ÷ (Schedule D DAF count / 1,000).
- `staff_cost_bps_daf_assets` = Part IX lines 5–10 ÷ DAF EOY value × 10,000. `staff_cost_bps_total_assets` uses Part X total assets instead.
- **Context** (joined by object id from `sponsor-cost-structure.csv`, which covers only FY2022+ harvest returns: 184 of 225):
  - lines 11a and 11g;
  - operating cost excluding 11f;
  - `ctx_fee_and_trustee_bps_daf_assets` = (11a + 11g + institutional-trustee fees) ÷ DAF assets.
- **Flags** (`flag_affiliate_pay`):
  - `top_officer_paid_by_related_org` (D = 0, E > 0);
  - `top_officer_split_org_and_related`;
  - `top_officer_0_on_990[_affiliate_staffed]` (a top officer is listed with $0);
  - `no_staff_cost_on_990[_affiliate_staffed]` (and Part IX lines 5–10 are $0 or absent);
  - `no_officer_listed_institutional_trustee`;
  - `no_officer_identified`.
  - The `_affiliate_staffed` suffix is added for affiliated_commercial sponsors [I].
  - `top_officer_shared_with` marks the same person as top officer of two sponsors in the universe in one TY (GKCCF / Greater Horizons; Servant Foundation / The Signatry).

## 2. Coverage

| TY | Returns | Notes |
|---|---|---|
| 2021 | 56 | DAFgiving360 has two (short period 2021-12 and FYE 2022-06) |
| 2022 | 55 | |
| 2023 | 55 | |
| 2024 | 56 | Ayco has two (2024-12 and FYE 2025-06) |
| 2025 | 3 | T. Rowe Price (FYE 2026-03), Thrivent and Saint Paul & Minnesota (FYE 2025-12); others not yet indexed |

- All 55 sponsors have TY2021–2024 returns.
- **Sources:** 219 returns came from the mirror and 6 from TEOS 2025/2026 zips.
- **Person rows:** 1,019 (206 top officers; 153–176 at each highest-paid rank). 860 match a Schedule J row by name.

## 3. Top 50: latest TY2024 return (top officer)

**Columns:**
- **Seg.:** AC affiliated-commercial; IN independent national; CF community foundation; FS faith / single-issue; UH university / health; DF digital-first supplement (role only).
- **Pay** is Part VII D+E+F [F]; ratios are [C].
- **Names and titles** are exactly as filed.

| # | Sponsor | Seg. | TY (period end) | Top officer title (as filed) | Name (as filed) | Part VII D+E+F ($) | of which E ($) | Per $bn DAF ($) | Per 1,000 accts ($) | Staff l5–10 ($m) | W-2 (V 2a) | Staff bps of DAF | Flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | FIDELITY INVESTMENTS CHARITABLE GIFT FUND | AC | 2024 (202506) | PRESIDENT | JACOB PRUITT | 0 | 0 | 0 | 0 | 0.00 | 0 | 0.0 | no_staff_cost_on_990_affiliate_staffed |
| 2 | NATIONAL PHILANTHROPIC TRUST | IN | 2024 (202506) | PRESIDENT & CEO (AS OF 2/26/25) | HOLLY WELCH STUBBING | 801,307 | 0 | 14,336 | 38,727 | 38.72 | 310 | 6.9 |  |
| 3 | DONOR ADVISED CHARITABLE GIVING INC | AC | 2024 (202506) | PRESIDENT | SAMUEL W KANG | 967,879 | 0 | 20,440 | 7,532 | 40.59 | 226 | 8.6 |  |
| 4 | VANGUARD CHARITABLE ENDOWMENT PROGRAM | AC | 2024 (202506) | PRESIDENT | REBECCA MOFFETT | 608,684 | 0 | 22,534 | 20,771 | 15.20 | 121 | 5.6 |  |
| 5 | GS DONOR ADVISED PHILANTHROPY FUND | AC | 2024 (202412) | PRESIDENT | KAREY D DYE | 0 | 0 | 0 | 0 | 0.00 | 0 | 0.0 | no_staff_cost_on_990_affiliate_staffed |
| 6 | Silicon Valley Community Foundation | CF | 2024 (202412) | President & CEO | Nicole Taylor | 1,268,486 | 0 | 132,436 | 1,254,680 | 21.04 | 110 | 22.0 |  |
| 7 | MORGAN STANLEY GLOBAL IMPACT FUNDING TRUST INC | AC | 2024 (202412) | PRESIDENT | MELANIE SCHNOLL-BEGUN | 0 | 0 | 0 | 0 |  | 0 |  | no_staff_cost_on_990_affiliate_staffed |
| 8 | AMERICAN ENDOWMENT FOUNDATION | IN | 2024 (202412) | CHIEF EXECUTIVE OFFICER | RONDAL RANSOM | 640,563 | 0 | 76,458 | 40,168 | 12.56 | 149 | 15.0 |  |
| 9 | Renaissance Charitable Foundation Inc | AC | 2024 (202412) | President & Chairman | Gregory W Baker | 0 | 0 | 0 | 0 | 0.00 | 0 | 0.0 | no_staff_cost_on_990_affiliate_staffed |
| 10 | NATL CHRISTIAN CHARITABLE FDN INC | FS | 2024 (202412) | CEO | KENDRA VANDERMEULEN | 309,560 | 0 | 54,465 | 9,691 | 44.38 | 285 | 78.1 |  |
| 11 | BANK OF AMERICA CHARITABLE GIFT FD | AC | 2024 (202412) | — | — |  |  |  |  |  | 0 |  | no_officer_listed_institutional_trustee |
| 12 | The Chicago Community Trust | CF | 2024 (202509) | President & CEO | Andrea Saenz | 685,048 | 0 | 154,162 | 343,382 | 16.21 | 150 | 36.5 |  |
| 13 | IMPACTASSETSINC | IN | 2024 (202412) | CEO & CIO | MARGRET TRILLI | 502,035 | 221,770 | 173,302 | 228,509 | 8.80 | 54 | 30.4 | top_officer_split_org_and_related |
| 14 | JEWISH COMMUNAL FUND | FS | 2024 (202506) | EXECUTIVE VP AND CEO | RACHEL SCHNOLL | 774,873 | 0 | 227,558 | 153,107 | 5.06 | 25 | 14.9 |  |
| 15 | FOUNDATION FOR THE CAROLINAS | CF | 2024 (202412) | CEO | CATHY BESSANT | 737,104 | 0 | 281,582 | 704,015 | 15.48 | 141 | 59.1 |  |
| 16 | Greater Kansas City Community Foundation | CF | 2024 (202412) | DIRECTOR/PRESIDENT & CEO | DEBORAH WILKERSON | 549,913 | 0 | 213,641 | 180,181 | 12.56 | 145 | 48.8 |  (shared top officer) |
| 17 | Greater Horizons | IN | 2024 (202412) | DIRECTOR/PRESIDENT | DEBORAH WILKERSON | 549,913 | 490,724 | 217,263 | 180,004 |  | 0 |  | top_officer_paid_by_related_org (shared top officer) |
| 18 | Combined Jewish Philanthropies of Greater Boston Inc | FS | 2024 (202506) | President & CEO | Marc Baker | 765,265 | 0 | 356,647 | 967,465 | 22.37 | 184 | 104.3 |  |
| 19 | RAYMOND JAMES CHARITABLE ENDOWMENT FUND | AC | 2024 (202503) | PRESIDENT (AS OF 04/23/24) | NICOLE HISLER | 0 | 0 | 0 | 0 | 0.08 | 0 | 0.4 | top_officer_0_on_990_affiliate_staffed |
| 20 | DECHOMAI ASSET TRUST | IN | 2024 (202412) | BOARD PRESIDENT | GREG DYER | 0 | 0 | 0 | 0 |  | 0 |  | no_staff_cost_on_990 |
| 21 | THE NEW YORK COMMUNITY TRUST | CF | 2024 (202412) | PRESIDENT | AMY FREITAG | 1,014,261 | 0 | 808,452 | 755,783 | 15.84 | 86 | 126.2 |  |
| 22 | COLUMBUS FOUNDATION | CF | 2024 (202412) | PRESIDENT & CEO | DOUGLAS F KRIDLER | 1,012,706 | 0 | 821,790 | 660,604 | 10.97 | 72 | 89.1 |  |
| 23 | Donors Trust Inc | FS | 2024 (202412) | President and CEO | Lawson R Bader | 507,792 | 0 | 419,040 | 877,016 | 3.18 | 18 | 26.3 |  |
| 24 | THE US CHARITABLE GIFT TRUST | AC | 2024 (202412) | PRES. & CHIEF PHIL. OFF. | STEPHEN W CLARKE | 0 | 0 | 0 | 0 | 0.26 | 0 | 2.2 | top_officer_0_on_990_affiliate_staffed |
| 25 | THE AYCO CHARITABLE FOUNDATION | AC | 2024 (202506) | PRESIDENT | KAREY DYE | 0 | 0 |  |  | 0.00 | 0 |  | no_staff_cost_on_990_affiliate_staffed |
| 26 | The Oregon Community Foundation | CF | 2024 (202412) | CEO/Asst Secretary/Treasurer | Lisa Mensah | 690,765 | 0 | 624,353 | 495,527 | 17.01 | 137 | 153.8 |  |
| 27 | Boston Foundation Inc | CF | 2024 (202506) | President & CEO | M Lee Pelton | 915,854 | 0 | 652,551 | 1,114,180 | 20.15 | 157 | 143.6 |  |
| 28 | CALIFORNIA COMMUNITY FOUNDATION | CF | 2024 (202506) | PRESIDENT & CEO | MIGUEL SANTANA | 731,053 | 0 | 658,596 | 877,615 | 16.29 | 104 | 146.8 |  |
| 29 | THE COMMUNITY FOUNDATION FOR GREATER | CF | 2024 (202412) | PRESIDENT | FRANK FERNANDEZ | 663,435 | 0 | 647,021 | 891,714 | 10.94 | 97 | 106.7 |  |
| 30 | Servant Foundation | FS | 2024 (202503) | Chief Executive Officer, President | Stephen A French | 401,936 | 0 | 513,803 | 868,112 | 8.89 | 86 | 113.6 |  (shared top officer) |
| 31 | JEWISH COMMUNITY FEDERATION OF SAN | FS | 2024 (202506) | CEO | JOY SISISKY | 772,970 | 0 | 568,999 | 739,684 | 15.12 | 136 | 111.3 |  |
| 32 | THE BESSEMER GIVING FUND | AC | 2024 (202412) | — | — |  |  |  |  | 0.04 | 0 | 0.5 | no_officer_listed_institutional_trustee |
| 33 | GREATER HOUSTON COMMUNITY FOUNDATION | CF | 2024 (202412) | PRESIDENT & CEO | STEPHEN D MAISLIN | 791,256 | 0 | 858,109 | 261,572 | 8.43 | 54 | 91.4 |  |
| 34 | MARIN COMMUNITY FOUNDATION | CF | 2024 (202506) | PRESIDENT & CEO | RHEA SUH | 732,783 | 0 | 709,122 | 1,495,480 | 13.86 | 86 | 134.1 |  |
| 35 | THE SIGNATRY CHARITABLE TRUST | FS | 2024 (202412) | President | Stephen A French | 401,903 | 391,860 | 504,383 | 156,748 | 0.20 | 0 | 2.5 | top_officer_paid_by_related_org (shared top officer) |
| 36 | COMMUNITY FOUNDATION OF NEW JERSEY | CF | 2024 (202412) | TRUSTEE, PRESIDENT/CEO | HANS DEKKER | 677,240 | 0 | 917,457 | 1,081,850 | 3.66 | 29 | 49.6 |  |
| 37 | THE DENVER FOUNDATION | CF | 2024 (202412) | PRESIDENT | JAVIER A SOTO | 534,496 | 0 | 733,697 | 876,223 | 6.90 | 68 | 94.7 |  |
| 38 | JEWISH COMMUNITY FOUNDATION OF LOS ANGELES | FS | 2024 (202412) | President & CEO | AARON LERNER | 664,762 | 0 | 936,660 | 557,686 | 6.18 | 34 | 87.1 |  |
| 39 | THE SAN DIEGO FOUNDATION | CF | 2024 (202506) | PRESIDENT & CEO | MARK A STUART CFRE | 737,408 | 0 | 986,480 | 974,119 | 16.82 | 131 | 225.1 |  |
| 40 | TULSA COMMUNITY FOUNDATION | CF | 2024 (202412) | CHIEF EXECUTIVE OFFICER | PHIL LAKIN JR | 725,134 | 0 | 1,034,420 | 903,031 | 16.93 | 427 | 241.5 |  |
| 41 | COMMUNITY FOUNDATION | CF | 2024 (202504) | PRESIDENT & CEO | ROBERT M FOCKLER | 429,177 | 0 | 583,030 | 467,004 | 3.14 | 20 | 42.6 |  |
| 42 | THE BOARD OF TRUSTEES OF THE LELAND | UH | 2024 (202508) | PRESIDENT/TRUSTEE | JONATHAN D LEVIN | 1,564,885 | 0 | 2,626,260 | 24,451,300 | 5,963.70 | 45,075 | 100,086.0 |  |
| 43 | AMERICAN GIFT FUND | IN | 2024 (202412) | — | — |  |  |  |  | 3.62 | 0 | 56.3 | no_officer_listed_institutional_trustee |
| 44 | UCLA FOUNDATION | UH | 2024 (202506) | PRESIDENT/CIO | JUSTIN E BARTON | 1,198,187 | 1,063,968 | 2,275,400 | 119,818,700 | 0.00 | 0 | 0.0 | top_officer_paid_by_related_org |
| 45 | THE MINNEAPOLIS FOUNDATION | CF | 2024 (202503) | PRESIDENT & CEO | RT RYBAK | 477,199 | 0 | 771,713 | 481,533 | 10.36 | 73 | 167.6 |  |
| 46 | T ROWE PRICE PROGRAM FOR CHARITABLE | AC | 2024 (202503) | PRESIDENT (AS OF 2/1/2025) | DANIEL TAMBELLINI | 0 | 0 | 0 | 0 | 0.64 | 0 | 9.9 | top_officer_0_on_990_affiliate_staffed |
| 47 | THRIVENT CHARITABLE IMPACT & INVESTING | FS | 2024 (202412) | PRESIDENT & CEO | MANDY TUONG | 722,775 | 0 | 1,216,240 | 86,601 | 5.49 | 1 | 92.4 |  |
| 48 | THE SAN FRANCISCO FOUNDATION | CF | 2024 (202506) | CEO | FRED BLACKWELL | 670,879 | 0 | 1,038,250 | 1,275,440 | 20.34 | 122 | 314.8 |  |
| 49 | COMMUNITY FOUNDATION OF TAMPA BAY INC | CF | 2024 (202506) | PRESIDENT/CEO | MARLENE M SPALTEN | 493,128 | 0 | 749,332 | 1,146,810 | 3.99 | 39 | 60.6 |  |
| 50 | SAINT PAUL & MINNESOTA FOUNDATION | CF | 2024 (202412) | PRESIDENT/CEO/SECRETARY | ERIC JOLLY | 805,411 | 0 | 1,386,090 | 1,054,200 | 10.13 | 87 | 174.3 |  |
| D | GIVINGA FOUNDATION INC | DF | 2024 (202412) | PRESIDENT/DIRECTOR/TREASURER | (role only) | 0 | 0 | 0 | 0 |  | 0 |  | no_staff_cost_on_990 |
| D | CHARITYVEST INC | DF | 2024 (202412) | PRESIDENT | (role only) | 0 | 0 | 0 | 0 | 0.00 | 0 | 0.0 | no_staff_cost_on_990 |
| D | ENDAOMENT INC | DF | 2024 (202506) | Chief Operating Officer | (role only) | 155,163 | 0 | 8,209,680 | 127,917 | 0.76 | 7 | 403.8 |  |
| D | GiveClear Foundation | DF | 2024 (202412) | Executive Director | (role only) | 0 | 0 | 0 | 0 | 0.01 | 0 | 0.4 | top_officer_0_on_990 |
| D | Daffy Charitable Fund | DF | 2024 (202412) | President | (role only) | 0 | 0 | 0 | 0 |  | 0 |  | no_staff_cost_on_990 |

**Notes:**
- **NPT TY2024:** a former President & CEO is also listed, with $1,035,821 [F]. The table shows the current officer.
- **Greater Horizons and GKCCF:** the same person and the same pay are filed twice (column E at Greater Horizons, column D at GKCCF).
- **The Signatry and Servant Foundation:** the same applies.
- **Thrivent Charitable:** reports 1 W-2 employee but $5.5m of lines 5–10 [F].
- **Stanford and UCLA:** ratios are meaningless at university scale and are excluded from comparisons.

## 4. Segment comparison (TY2024, one return per sponsor)

| Segment | n | Top officer paid by org / via related only / $0 or none | Median top-officer pay (paid) | Median per $bn DAF | Median per 1,000 accounts | Part IX 5–10, pooled bps of DAF | Median W-2 (V 2a) | Median top-6 pay | Top-6 share of lines 5–10 (median) |
|---|---|---|---|---|---|---|---|---|---|
| Affiliated-commercial | 12 | 2 / 0 / 10 | $788,282 | $21,487 | $14,152 | **2.9** | 0 | $240,000 | 16% |
| Independent national | 6 | 3 / 1 / 2 | $595,238 | $124,880 | $110,086 | 8.9 | 27 | $1,982,580 | 13% |
| Community foundation | 21 | 21 / 0 / 0 | $725,134 | $733,697 | $877,615 | **78.7** | 97 | $2,400,976 | 19% |
| Faith / single-issue | 9 | 8 / 1 / 0 | $664,762 | $504,383 | $557,686 | 66.4 | 34 | $2,163,494 | 20% |
| Digital-first (supplement) | 5 | 1 / 0 / 4 | $155,163 | n/m | $127,917 | 11.5 | 0 | $24,000 | n/m |

- **Source:** `segment_year` rows [C].
- **Affiliated-commercial medians** are over the 2 paid sponsors (DAFgiving360 and Vanguard). Their "top-6" figure is mostly board and trustee fees at the others.
- **Part VII line 2** (individuals over $100k): the median is 33 at community foundations, 21 at faith / single-issue, 14 at independent nationals and 0 at affiliated-commercial sponsors.
- **Where affiliated-commercial costs sit instead** (TY2024 context, (11a + 11g + institutional-trustee fees) ÷ DAF assets) [C]:

  | Sponsor | bps of DAF assets | Main line |
  |---|---|---|
  | BofA | **50.8** | trustee fee $24.1m (Part VII column D to Bank of America) |
  | Renaissance | 32.5 | 11g $19.2m |
  | Raymond James | 30.6 | 11a $7.1m |
  | Fidelity | 21.0 | 11a $179.9m (latest 990, FY Jun-2025) |
  | MS GIFT | 17.5 | 11g $16.0m |
  | Ayco | 15.8 | |
  | Bessemer | 7.7 | |
  | US Charitable Gift Trust | 5.3 | |
  | T. Rowe Price | 2.5 | |
  | GS DAPF | 2.1 | |

  - Self-staffed nationals for comparison: DAFgiving360 0.8 (plus 8.6 bps of staff), NPT 0.3 (plus 6.9) and AEF 5.2 (plus 15.0).
  - Among independents, American Gift Fund pays its institutional trustee (RBC Trust Company (Delaware)) $3.62m, or 56.3 bps, reported as column F "other compensation" and on Part IX line 5. Dechomai pays 40.0 bps in fees.
  - **[I]** The affiliated model moves executive and staff cost into service and trustee fees. On the 990 that cost is visible only as a fee total.

## 5. Where the sponsor shows $0 because an affiliate pays (TY2021–2024)

| Sponsor (segment) | Years | What the return shows [F] | Payer named in the return [F] |
|---|---|---|---|
| Fidelity Charitable (AC) | all | President and all officers $0; Part IX lines 5–10 $0; 0 W-2 | Schedule O: "engages FMR LLC ('FMR') pursuant to a services agreement"; FY Jun-2025 line 11a $179.9m |
| GS DAPF (AC) | all | President $0; lines 5–10 $0 | Schedule O: officers "employed by a company where a ... officer or director is an officer or director"; Schedule R lists Ayco |
| The Ayco Charitable Foundation (AC) | all | President $0 (the same name as GS DAPF's President, as filed); lines 5–10 $0 | Schedule R lists GS DAPF |
| MS GIFT (AC) | all | President $0; no lines 5–10 filed | not stated in the Schedule O screen [U]; 11g $16.0m |
| Renaissance Charitable Foundation (AC) | all | President & Chairman $0 (10 h/week); lines 5–10 $0 | not stated in the Schedule O screen [U]; 11g $19.2m |
| US Charitable Gift Trust (AC) | all | President $0; independent directors paid board fees (Part IX lines 5–10 $190k–$257k) | "all officers of the trust are employees of 474 MS Services Group, Inc. or Eaton Vance Distributors, Inc. and receive no compensation from the trust" |
| T. Rowe Price Program (AC) | TY2022–25 | President $0 (TY2021 $6,520); lines 5–10 $0.55–0.70m | [U] |
| Raymond James CEF (AC) | all | TY2021–23: no executive officer listed, trustees paid $15.5–16.5k; TY2024: President $0 | [U]; 11a $7.1m |
| BofA Charitable Gift Fund (AC) | all | Only Bank of America as institutional trustee, paid **$17.7m → $24.1m** (TY2021→24) | Part VII column D |
| Bessemer Giving Fund (AC) | all | Only Bessemer Trust Company as institutional trustee ($10k–$45k) | Schedule O: "it has no employees" |
| Dechomai Asset Trust (IN) | all | Board President $0; no staff | Schedule O: "Dechomai Asset Trust has no employees" |
| American Gift Fund (IN) | all | Directors $30–60k; RBC Trust institutional trustee $1.8m → $3.6m (column F) | Part VII |
| Greater Horizons (IN) | all | President D = 0, **E $435k → $491k** | GKCCF (Schedule R) |
| The Signatry Charitable Trust (FS) | all | President D+F ≈ $6–10k; **E $260k–$436k** | Schedule O: "all officers are employed by, and serve as officers of, a related organization" |
| UCLA Foundation (UH) | all | President / CIO mostly column E ($1.06m in TY2024) | "All UCLA Foundation staff are employees of the Regents of University of California" |
| Daffy (DF) | all | President $0; no lines 5–10 | [U] (Schedule O screen empty) |
| Charityvest (DF) | all | President $0 | Schedule O TY2024: the President "is compensated by Foundation Source"; "reportable compensation received from Vennfi, Inc. totaled $163,944" (an unrelated payer, so not in column E) |
| GiveClear (DF) | TY2024 | Executive Director $0 | Schedule O: management company Attolero, LLC; the Executive Director is its owner and "is compensated by" it; "$72,000" |
| Givinga (DF) | all | President $0; no lines 5–10 | Schedule R: Givinga, Inc. (related taxable corporation); payer not stated [U] |

- **[I]** Three patterns hide pay.
  - **(a)** The staff are the parent's employees under a services agreement, which shows only as line 11a or 11g. Examples: Fidelity, MS GIFT and Renaissance.
  - **(b)** A bank trustee takes a fee reported in Part VII as compensation to an institution. Examples: BofA, Bessemer and American Gift Fund.
  - **(c)** A related charity employs the executive, which shows in column E. Examples: Greater Horizons, The Signatry and UCLA.
- Only (c) is visible as executive pay on the 990.
- **DAFgiving360** is the exception among commercial affiliates. Its staff are Schwab employees, but payroll ($40.6m) and officer pay pass through its own Part IX and Part VII [F].

## 6. Related-organisation pay (Part VII column E)

| TY | Sponsors with E > 0 (non-university) | Column E total, non-university | Note |
|---|---|---|---|
| 2021 | 3 | $2.0m | Greater Horizons $634k; The Signatry $916k; Tulsa CF $438k |
| 2024 | 5 | $3.1m | Greater Horizons $758k; The Signatry $1.45m; ImpactAssets $222k; Tulsa CF $492k; Denver Foundation $180k |

- **Source:** `part_vii_sum_related_e`, individuals only [F/C].
- Column E is never positive at an affiliated-commercial sponsor. The parent firm's pay of sponsor officers therefore never enters the 990 as related-organisation pay. The 990 counts a parent as a related organisation only under the control tests of the Schedule R instructions, which these parents do not meet as filed [I].

## 7. The five highest-paid after the top officer (role level, TY2024)

| Segment | Persons | Median pay | #1 / #3 / #5 (median) | Most common roles [I, title keywords] |
|---|---|---|---|---|
| Community foundation | 105 | $324,351 | $436,463 / $316,624 / $265,918 | CFO / finance (25), development / philanthropy (17), technology (11), programmes (8), COO (6) |
| Faith / single-issue | 40 | $326,582 | $393,764 / $345,108 / $271,386 | CFO (8), technology (6), development (5), COO (4) |
| Independent national | 19 | $336,271 | $380,946 / $313,521 / $292,255 | legal counsel (3), technology (3), subsidiary CEOs (3) |
| Affiliated-commercial | 24 | $47,500 | — | mostly directors' and trustees' fees; staff appear only at DAFgiving360 and Vanguard |

- **Source:** person rows (`highest_paid_1..5`) [F/C].
- **Concentration:** the top six take a median **19%** of lines 5–10 at community foundations and 13% at independent nationals [C].

## 8. Trends TY2021→TY2024 (matched sponsors; `segment_trend` rows)

| Segment | Matched / paid both years | Top-officer pay growth/yr, median (pooled) | Lines 5–10 growth/yr, median (pooled) | DAF assets growth/yr, median (pooled) | Top officer changed |
|---|---|---|---|---|---|
| Affiliated-commercial | 12 / 2 | +22.1% (+21.1%) | +10.9% (+16.8%) | +14.1% (+20.0%) | 0 of 2 |
| Independent national | 6 / 4 | +3.4% (+3.9%) | +16.1% (+16.0%) | +25.5% (+30.4%) | 2 of 4 |
| Community foundation | 21 / 21 | +6.6% (+7.7%) | +9.7% (+9.5%) | +4.5% (+1.0%) | 7 of 21 |
| Faith / single-issue | 9 / 8 | +11.3% (+11.2%) | +10.3% (+11.1%) | +8.0% (+7.4%) | 3 of 8 |

- **Per-year medians** (`segment_year`), TY2021 → 2022 → 2023 → 2024:
  - top-officer pay at community foundations: $535,190 → $596,698 → $680,084 → $725,134;
  - community-foundation pay per $bn of DAF assets: $584,536 → $792,899 → $798,339 → $733,697;
  - pooled community-foundation lines 5–10: 61.8 → 78.1 → 83.4 → 78.7 bps of DAF assets;
  - independent nationals' pay per $bn: $140,879 → $172,686 → $170,498 → $124,880.
- The affiliated-commercial rate covers DAFgiving360 (President $582,167 → $967,879) and Vanguard ($305,760 → $608,684, but TY2021 is a part-year: "PRESIDENT (AS OF 11/01/2021)").
- **Transitions inflate or deflate single years.** Seven of 21 community foundations changed top officer. Two-officer years are flagged `_multiple` (Chicago Community Trust TY2021, Servant Foundation TY2022, NCF TY2022, JCF Los Angeles TY2023, GiveClear TY2022), and part-year officers (for example California Community Foundation TY2023, $120,034) are kept as filed.

## 9. Reading [I]
- **For cost benchmarking**, executive pay on the 990 is not comparable across segments without the fee lines.
  - Affiliated-commercial sponsors look almost free of staff cost (2.9 bps pooled).
  - Once the service and trustee fees that replace payroll are added back, the range is 2–51 bps. That range brackets the self-staffed nationals' 5.6–15 bps of staff.
  - The fee lines also pay for systems and investment administration, so the labour share inside them is unknown (P-B43N24-01).
- **Community-foundation pay is a whole-organisation cost.** Its per-DAF ratios overstate DAF-attributable pay, and Part IX gives no DAF split. Under allocation A of the cost-structure note (DAF share of assets), DAF-allocated staff cost per $ of DAF assets equals the whole-organisation ratio to total assets: a median of 52.2 bps for community foundations. That is still 6–9× the self-staffed nationals.
- **Pay does not scale with assets** (elasticity 0.05–0.23). Consolidation, or outsourcing to a national's platform, would mostly remove fixed executive layers rather than variable pay.
- **Pay at the 50 largest sponsors grew faster than DAF assets** at community foundations and faith sponsors (TY2021–24). It grew slower at independent nationals, where assets roughly doubled.

## 10. Limitations
- **The top-officer rule is title-based.** Five transition years have two current CEO-titled officers; the higher-paid is kept and the year flagged. Stanford uses a manual override.
- **Part VII column E is filer-defined.** Pay by an unrelated employer (Foundation Source / Vennfi at Charityvest; Attolero at GiveClear) shows only in Schedule O text. The Schedule O screen is a regex: absence of a quote is [U], not evidence of no affiliate.
- **DAF assets and accounts** come from the same return's Schedule D. Ratios for organisations with few DAF accounts (Stanford, UCLA, Endaoment) are not meaningful, and Givinga's account unit is undefined (wave-5 correction).
- **Lines 5–10 are whole-organisation and include benefits and payroll tax.** No FTE adjustment is made (see the batch-38 wave-23 correction).
- **Context columns** (11a, 11g, operating cost) exist only for the 184 returns in the FY2022+ harvest. TY2021 Dec-FYE returns lack them.
- **TY2025** has 3 returns. Trend rows stop at TY2024.
- **The segment table is a manual classification [I].** Renaissance (administrator-affiliated) and Thrivent Charitable (fraternal financial affiliate, classed as faith) are judgement calls.

## 11. Data dictionary: `sponsor-executive-compensation-2021-2025.csv` (129 columns; `record_type` selects the row kind)

**sponsor_year** (225 rows; one per return)

| Field | Meaning |
|---|---|
| `ein`, `sponsor_name`, `rank_fy2024` | EIN, DAFRC name and corrected FY2024 DAF-asset rank (blank = digital-first supplement) |
| `segment`, `segment_note` | Segment [I] and the affiliate named |
| `fy`, `tax_year`, `tax_period`, `object_id`, `returns_for_period`, `return_ts`, `amended_ind`, `xml_source`, `xml_url` | Return identity; `returns_for_period` counts index rows (amendments) for the period |
| `employees_part_v_2a`, `employees_part_i_5` | W-2 employees [F] |
| `part_vii_listed`, `part_vii_paid` | Persons listed (including institutions); individuals with D+E+F > 0 |
| `institutional_trustee_names`, `institutional_trustee_comp_def` | Institutional trustees and their D+E+F |
| `part_vii_n_over_100k` | Part VII line 2 |
| `part_vii_sum_org_d`, `part_vii_sum_related_e`, `part_vii_sum_other_f` | Column sums over individuals [C] |
| `part_vii_tot_org`, `part_vii_tot_related`, `part_vii_tot_other` | Filed section totals (line 1d), including institutions [F] |
| `related_share_of_part_vii` | E ÷ (D+E+F), individuals |
| `top6_comp_total`, `top6_comp_related` | Top officer plus five highest-paid |
| `l05`–`l10`, `staff_cost_l5_10`, `l25_total_expenses` | Part IX total column [F]; sum of lines 5–10 [C] |
| `total_assets_eoy`, `daf_assets_eoy`, `daf_assets_source`, `daf_accounts`, `daf_accounts_source` | Part X and Schedule D (fallback: corrected DAFRC same FY) |
| `top_officer_title`, `top_officer_name`, `top_officer_basis` | As filed; selection basis (`title_rank1` CEO, `2` president, `3` executive director, `+3` past-marked, `_multiple`, `highest_paid_officer`, `manual_override`, `none`) |
| `top_officer_hours_org`, `top_officer_hours_related` | Average hours per week |
| `top_officer_comp_org_d`, `_related_e`, `_other_f`, `_total_def` | Part VII columns |
| `top_officer_schj_total`, `top_officer_schj_matched` | Schedule J Part II total (organisation + related) when the name matches |
| `top_officer_shared_with` | Other universe EIN with the same top officer in the TY |
| `sched_j_present` | Schedule J filed |
| `top_pay_per_bn_daf`, `top_pay_per_1000_accounts`, `top_pay_per_bn_total_assets` | Ratios [C] |
| `staff_cost_bps_daf_assets`, `staff_cost_bps_total_assets`, `staff_cost_per_account`, `staff_cost_per_employee` | Ratios [C] |
| `ctx_operating_cost_ex_invest_mgmt`, `ctx_outside_services_l11`, `ctx_fees_mgmt_l11a`, `ctx_fees_other_l11g`, `ctx_staff_share_of_opex_ex_l11f`, `ctx_fee_and_trustee_bps_daf_assets` | Context from `sponsor-cost-structure.csv` (FY2022+ harvest returns only) |
| `flag_affiliate_pay` | §1.4 |
| `sched_r_related_names`, `sched_o_comp_text` | Schedule R names (first 8); quoted Schedule O payer sentences |

**person** (1,019 rows): `person_role` (`top_officer`, `highest_paid_1..5`) plus the following:

| Field | Meaning |
|---|---|
| `person_name`, `title`, `roles` | As filed; role boxes (trustee, officer, key employee, highest compensated, former) |
| `institutional` | 1 = institutional trustee |
| `hours_org`, `hours_related`, `comp_org_d`, `comp_related_e`, `comp_other_f`, `comp_total_def` | Part VII |
| `schj_matched`, `schj_base_org` … `schj_prior_990_related` | Schedule J Part II columns B(i)–(iii), C, D, E, F for the filing organisation (`_org`) and related organisations (`_related`) |

**segment_year** (27 rows) and **segment_trend** (6 rows):
- `segment_year`:
  - counts: `n_returns`, `n_top_officer_paid`, `n_top_paid_by_org`, `n_top_paid_related_only`, `n_top_zero_or_none`, `n_flag_affiliate_pay`;
  - medians: `median_*`;
  - pooled sums and ratios: `sum_*`, `pooled_staff_cost_bps_daf_assets`, `pooled_staff_plus_l11a_bps_daf_ctx` (over `n_ctx` returns with context).
- `segment_trend` (`tax_year` = "2021-2024"):
  - `median_` and `pooled_` compound annual growth of top-officer pay, lines 5–10 and DAF assets;
  - `top_officer_changed_title_or_person`.
- Aggregates use one return per sponsor × TY.

## 12. Reproduce
```
python3 scripts/mission_sponsor_compensation.py --irs-dir <dir with index_2021..2026.csv> --work-dir <cache dir> [--fetch]
```
- Without `--fetch`, the script uses the cached JSON extracts.
- It prints coverage and the TY2024 log-log elasticities (§0.4).
- No values are hand-typed except the segment table and the Stanford override.

## Sources
- IRS Form 990 e-file XML via the [GivingTuesday mirror](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601389349301700_public.xml) (URL per return in `xml_url`) and [IRS TEOS](https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv) indexes and zips, read 2026-11-15.
- [DAFRC Annual DAF Report 2025 updated dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx) with repo corrections (`dafrc-corrections-itemized.csv`).
- Repo: `sponsor-cost-structure.csv` (context), `direction-donor-feature-census.md` (digital-first list).
