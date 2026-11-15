# Queue batch 38 B: data follow-ups — processor account basis, a full-text line-6 screen, MS GIFT's line 3, recipient-side R5 check, Endaoment fund count, BDC commitment notes, per-FTE pay and a payout triad

**Date:** 2026-11-15 · **Agent:** batch38 B · **Queue items:** P-B36A-01, P-B37B-01, P-B37B-03, P-B34A-03, P-B32B-02, P-BLB-04, P-LND-04, P-ANL-08 (`data/mission-2026-11-14/research-priority-queue.csv`)

**Outputs**
- [`data/mission-2026-11-14/line6-fulltext-screen.csv`](../../data/mission-2026-11-14/line6-fulltext-screen.csv): 77 returns with Schedule D Part I DAF values or DAF-holding language, out of 126,684 line-6 "No" returns read in full. Every row has a manual verdict (P-B37B-01).
- [`data/mission-2026-11-14/payout-triad-2021-2024.csv`](../../data/mission-2026-11-14/payout-triad-2021-2024.csv): 48 rows (FY2021–24 × 2 sample scopes × 6 segments). **Analysis, not a filed statistic** (P-ANL-08).
- [`data/mission-2026-11-14/sponsor-pay-per-fte.csv`](../../data/mission-2026-11-14/sponsor-pay-per-fte.csv): 20 sponsors, per-head pay, Part VII paid-officer split and public FTE evidence (P-LND-04).
- [`data/mission-2026-11-14/bdc-unfunded-commitments-two-period.csv`](../../data/mission-2026-11-14/bdc-unfunded-commitments-two-period.csv) (new), plus refreshed `bdc-loans-daf-ecosystem.csv` and `bdc-loans-latest-marks.csv` (P-BLB-04).
- [`data/mission-2026-11-14/queue-proposals-batch38b.csv`](../../data/mission-2026-11-14/queue-proposals-batch38b.csv): P-B38B-01 and P-B38B-02.
- **Scripts** (stdlib only, functional style):
  - [`scripts/mission_batch38_data.py`](../../scripts/mission_batch38_data.py), new, with tasks `fulltext`, `triad`, `recipients`, `msgift`, `fte` and `accounts`. It reuses the batch-37 extract helpers and the batch-35 TEOS zip reader. `triad` and `recipients` re-run the batch-34 R5 pipeline in memory using the unchanged `mission_market_netting` functions.
  - [`scripts/mission_bdc_loans.py`](../../scripts/mission_bdc_loans.py): additive P-BLB-04 changes. Existing output columns are unchanged.

**Conventions**
- FY = calendar year in which the tax period ends (DAFRC convention).
- **Recency:** every return read is FY2022 or later, except the FY2021 MS GIFT return (TY2021) and the FY2021 rows of the triad and R5 window.
- **Labels:** **[F]** filed or published value; **[C]** script computation; **[I]** inference or manual reading; **[S]** search-index or third-party text; **[U]** not found.
- **Governing corrections read first:**
  - wave 22, end of [queue-batch37-filing-questions.md](queue-batch37-filing-questions.md). Its two items concern NPT's Schedule L wording and do not touch this batch.
  - wave 21, end of [queue-batch36-metrics-rails.md](queue-batch36-metrics-rails.md). Item 1 (B2 account bounds) is noted. Items 2–3 concern rail shares and are not used here.
  - [queue-batch34-netting-filings.md](queue-batch34-netting-filings.md) has no corrections section. R5 is rebuilt here to the dollar (§4, §8).
  - Batch 37 §5 (wave 17/18 items as applied there): MS GIFT is the only broker captive under 50 bps, and a low line 3 is an anomaly *consistent with* fee netting or income-in-gains, not proof of either.
- **Access.**
  - robots.txt was read on every host before fetching. The S3 mirror has none (404). apps.irs.gov redirects. givinga.com allows all. nptrust.org allows all except two named crawlers.
  - endaoment.org **disallows `/funds/` and `/orgs/`**, so its public fund pages were **not** fetched.
  - app.endaoment.org and docs.endaoment.org return 403, including for robots.txt, and were not fetched.
  - paypal.com allows the Giving Fund policy paths, but all four policy URLs returned 403 (not retried further).
  - charitiesnys.com returned HTTP 500 for robots.txt, so the NY registry was not used.
  - A public Ethereum RPC refused archive log queries without a token, and further RPC probing was not permitted in this session.
  - No logins, forms or contact. **This is research, not legal or tax advice.**

---

## 0. Answers in brief

| Item | Answer | Confidence |
|---|---|---|
| **P-B36A-01** PPGF / Givinga account basis | **Both read as accounts with ongoing advisory privileges, so both stay in the A1 central account metric.**<br>**Givinga [F]:** its CY2024 990 Part III calls the foundation "a sponsoring organization built and designed to support the charitable giving activities of all its individual account holders". Its own site (fetched 2026-11-15) describes the employee Charitable Savings Account as "a secure giving account that holds funds until you're ready to disburse", "Employees can view live balances", "Portable", "Built on proprietary DAFs", giving employees "access to ... the Donor Advised Fund".<br>**PPGF [S]:** the policy pages still return 403. Search-index text of the Donor Account Policy: donors may not recommend more than their Donor Account balance; "at least 5% of the funds held in each Donor Account are recommended for distribution each year"; after 36 months without recommendations an account is inactive and PPGF may choose the charities; donations are "final and irrevocable". PPGF's 990 has no account-basis wording [F].<br>**Re-run trigger not met:** index_2026 is still Last-Modified 2026-10-21. No TY2025 990 is indexed for PPGF, Givinga, NFG, Bright Funds (EIN 462109112) or CAF America (the newest is FYE 2025-04) [F]. `mission_account_metric.py` was therefore not re-run. | High for Givinga (filed and first-party text); medium for PPGF (secondary text only) |
| **P-B37B-01** full-text line-6 screen | **Universe:** 129,379 section 501(c)(3) EINs whose newest FY2022+ SOI-extract return answers line 6 "N" with ≥ $1m of assets, minus 65 DAFRC panel and 2,490 batch-37 universe EINs = **126,824**. 126,736 have a FY2022+ 990 in TEOS index_2021–2026, and **all 126,736 newest returns were read in full** (112,060 from the mirror, 14,676 from TEOS zips). 52 now answer "Yes", leaving 126,684 in scope [C].<br>**Evidence:** 11 returns with Part I values, 66 with holding language, 331 with mention only, 126,276 with none.<br>**Verdicts on the 77 A/B rows [I]:**<br>- **3 likely sponsors:** Dakota Medical Charities ("home of ... more than 100 donor-advised funds"; $89.5m of assets); New Mexico Community Trust ($10.6m); Bayou Community Foundation ($3.5m). None reports Part I values.<br>- 6 possible; 7 unexplained Part I values at operating charities; 3 data-entry errors; 16 negations; 14 other meanings of "sponsoring organization"; 13 holders at another sponsor; 9 grants or receipts; 6 affiliates.<br>**Money:** Part I EOY values on all 11 A rows total **$2.96m** [C]. As in batch 37, **the tail adds sponsors, not money.** | High on coverage; verdicts [I] |
| **P-B37B-03** MS GIFT line 3 | **Still unexplained, but narrowed:**<br>- **Year pattern [F/C]:** line 3 is $1.08m (FY2021), $8.03m (FY2022), $22.33m (FY2023) and $3.39m (FY2024). That is **2.5, 15.6, 39.2 and 4.8 bps** of average Part X line 11 public securities.<br>- **FY2024 line 3 is below plausible interest on its own cash:** savings and temporary cash investments are $703.5m at year end ($302.9m at the start).<br>- **Line 3 includes partnership K-1 income:** column (C) −$15,678 equals the FY2024 990-T partnership income line ("INVESTMENT IN PARTNERSHIPS") [F].<br>- **No fee netting is visible:** 11f is blank in every year. 11g other fees are $9.8m–$16.0m and line 24 "FA commissions" $1.9m–$2.8m. Gains are complete: 7d is $109.2m and Part XI line 5 is $586.0m, a total-return proxy of 864 bps [C].<br>- **No public audit:** the 990 ticks audited, consolidated statements (E&Y prepares the return). No FY2025 990 is indexed. The NY registry could not be reached.<br>**Reading [I]:** the swing from 39 bps to 5 bps between FY2023 and FY2024, while cash doubled, points to a booking change: dividends and interest booked inside account-level total return or gains. A fee wedge cannot produce that swing. Unproven without the audit. | High on filed values; reading [I] |
| **P-B34A-03** recipient-side R5 check | **Targets:** the 10 largest CF and single-issue recipients by central netting, plus Greater Horizons (named). Together they receive **$5.67bn of gross FY2021–24 lines, of which R5 central nets $4.39bn (77%)** [C].<br>**Recipient-side test:** same-FY Schedule D DAF contributions ÷ Part VIII 1h total contributions (SOI extracts). Swapping it in for the asset-share weight gives **$4.80bn (+9%)**. The contribution share is lower than the asset share for 5 of 11 recipients: NCF, Greater Horizons, Christian Community Foundation and CJP by 0.04–0.13, and PEF Israel by far (19.5% against 0.64).<br>**Capacity:** inbound lines never exceed the recipient's same-FY DAF contributions. They are close at PEF Israel (78% over FY2021–24; 97% in FY2024) and Impact Investing CF (74%).<br>**FY mismatch:** 83% of SVCF's inbound dollars (Dec FYE) come from grantors with another FYE, mostly NPT (June). Its FY2022 lines are 52% of same-FY and **108% of next-FY** DAF contributions. Timing is material at the largest recipient.<br>**Audits:** none of the recipients' audits were read in this batch [U]. | High on arithmetic; weights remain [I] |
| **P-B32B-02** Endaoment fund count | **Not counted [U].**<br>- endaoment.org's robots.txt disallows `/funds/` and `/orgs/`. The app and docs hosts return 403.<br>- On-chain counting needs log queries against OrgFundFactory `0x10fD9348136dCea154F752fe0B6dB45Fc298A589` (Ethereum, Base and OP, per the docs via search index [S]). A public RPC refused archive queries without a token, and other RPC probing was not permitted here.<br>- The FY2024–25 audits are not reachable (docs host 403). | — |
| **P-BLB-04** BDC parser | **Two changes, both additive:**<br>(a) Each inline-XBRL money fact in a hit row is read with its own context date. Rows with facts on two or more dates are split into **per-period rows** in a new CSV.<br>(b) MM/YY maturities are now parsed. **All 80 KKR FS Income Trust / Select debt rows now carry a maturity**, where none did before.<br>**Effect on latest marks:** KKR's Momentive 2031-07 facility was previously split from its own rows by the missing maturity and showed as "not_in_schedule_at_2026-09-30". It now shows as **held at 96.1% of par** (Income Trust $12.6m par; Select $11.0m). Its Bonterra 2032-03 rows group at 99.43%. Barings' Envestnet rows gain their 11/31 maturity. Latest-mark rows fall from 304 to 298 because duplicates merge. | High (no hand-typed values) |
| **P-LND-04** per-FTE pay | **No public FTE disclosure exists for 19 of the 20 largest staffed non-university sponsors** [U]. The audits read (NCF, Vanguard Charitable, FFTC, NPT, RCF, Fidelity) state no headcount.<br>NPT is the only one with a figure: "more than 235 fulltime employees" in the US, from a job-board copy of its recruiting text [S], against 310 W-2 employees. That implies **$136,066 wages per FTE against $103,147 per head** (FTE/head 0.76).<br>The Part VII split is filed [F]. Median **non-officer wages per head are $84,226**, against $95,566 for all wages per head. Two flagged sponsors (Vail Valley Foundation, Onward) remain part-time-heavy. | High on per-head [F/C]; FTE [S/U] |
| **P-ANL-08** payout triad | **Analysis [C]**, FY2024:<br>- **Aggregate** payout (corrected grants ÷ prior-year assets): **25.9%**;<br>- **ex-DAF-to-DAF** (R5 central): **22.8%** [22.2–23.2%];<br>- **median sponsor** (BOY DAF assets ≥ $1m, 1,071 sponsors): **12.7%** gross and 12.2% ex-DAF-to-DAF. The interquartile range is 5.8–22.8%, and 20.6% of sponsors are below 5%.<br>FY2021–23 medians are 11.9%, 10.7% and 12.0%. By segment (FY2024 median): national 22.2%, community foundations 11.6%, single-issue 16.7%, university/hospital 5.1%. **The typical sponsor pays out about half the aggregate rate**, and netting moves the aggregate more than the median. | High on arithmetic; framing [I] |

---

## 1. P-B36A-01: account basis of PPGF and Givinga

| Sponsor | Evidence | Label | Reading |
|---|---|---|---|
| Givinga Foundation (474172718) | CY2024 amended 990 Part III: "THE GIVINGA FOUNDATION IS A SPONSORING ORGANIZATION BUILT AND DESIGNED TO SUPPORT THE CHARITABLE GIVING ACTIVITIES OF ALL ITS INDIVIDUAL ACCOUNT HOLDERS EQUALLY"; "WE BELIEVE DONOR ADVISED FUNDS SHOULD BE ACCESSIBLE TO ALL" ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503179349301975_public.xml)) | [F] | Accounts are donor accounts at a sponsor |
| Givinga (site) | [Solutions](https://www.givinga.com/solutions): CSA "holds funds until you're ready to disburse"; "Optional individual employee accounts"; "Employees can view live balances"; "Portable — doubles as a valuable employee benefit"; "Built on proprietary DAFs". [Workplace giving](https://www.givinga.com/workplace-giving): a CSA "gives employees access to ... the Donor Advised Fund". [Janus Henderson accounts](https://www.givinga.com/insights/blog/partner-spotlight-janus-henderson-launches-charitable-investment-accounts-powered-by-givinga): donors "contribute once, invest ... and recommend grants" | [F] (first-party web) | Ongoing privileges by design. The site [terms](https://www.givinga.com/terms-and-conditions) are website terms only, with no account terms |
| PayPal Giving Fund (450931286) | Donor Account Policy via search index: grant recommendations capped at the Donor Account balance; at least 5% recommended each year; 36 months without recommendations makes an account inactive, after which "the funds may be distributed to eligible charities selected by PayPal Giving Fund"; gifts are "final and irrevocable". A 2024 amendment says donated funds are kept in "a secure, dedicated bank account" | [S] | Ongoing privileges, subject to a minimum annual distribution and inactivity sweep |
| PPGF 990 CY2024 | Part III: "make it easy for donors to support the charities they care about on the websites and apps they use every day"; no account-basis wording | [F] | Neutral |

- **Result:** neither processor's own text disclaims ongoing privileges, and both describe balances that donors direct later. Batch 36's A1 rule (exclude only on the sponsor's own statement) therefore keeps their 1.80m FY2024 accounts. A2 stays the cited "accounts excluding micro-account processors" bound.
- **Caveat [I]:** Givinga's 1,421,011 accounts average $8.73 (EOY $12.4m). Many are probably employee accounts opened by default with little or no balance. The privilege exists, but the count measures enrolment rather than active advising.
- **Index check [F]** (`accounts` task):

| Target | Newest indexed 990 | TY2025 period sought | Indexed? |
|---|---|---|---|
| PPGF | 202412 | 202512 | No |
| Givinga | 202412 (original and amended) | 202512 | No |
| Network for Good | 202412 | 202512 | No |
| Bright Funds (EIN 462109112) | 202412 (two returns) | 202512 | No |
| CAF America | 202504 (FYE 2025-04) | 202604 | No |

- index_2026 Last-Modified is **Wed, 21 Oct 2026 13:03:05 GMT** (HEAD request, 2026-11-15).

## 2. P-B37B-01: full-text line-6 screen beyond NTEE T30/T31/T70

### 2.1 Method
- **Universe (`soi_newest`):**
  - IRS SOI annual 990 extracts 22–25eoextract990 (TY2021+);
  - subsection 03, newest tax period ≥ 202201 per EIN;
  - `dnradvisedfundscd` = "N" and `totassetsend` ≥ $1,000,000;
  - minus the DAFRC panel (65) and the batch-37 universe, i.e. BMF NTEE T30/T31/T70 or a DAF-like name (2,490).
- **Return read:** the newest FY2022+ Form 990 per EIN in TEOS index_2021–2026 (`newest`). The SOI row only selects the EIN, so the line-6 status comes from the return itself.
- **Extract (`extract_ft`):**
  - Part IV `DonorAdvisedFundInd`; Part X total assets; Schedule D Part I (both columns, count, contributions, grants and EOY);
  - every text leaf in the return that matches `donor[- ]advised | DAF(s) | donor[- ]directed fund(s) | sponsoring organi[sz]ation`, with a ±260-character window.
  - The mention list is wider than batch 37's: it adds donor-directed funds and the IRC 4966 term.
- **Classes:**
  - A = any positive Part I DAF value;
  - B1 = strong holding language (e.g. "N donor advised funds", "our donor advised funds", "serves as a sponsoring organization", "offers/administers ... donor advised funds");
  - B2/B3 = batch-37 holding patterns (B3 with receipt language);
  - C = mention or receipt only.
- **Manual reading [I]:** every A and B row (77) has a verdict in the script's `REVIEW` table, with the reason in `review_note`. The 331 C rows were not hand-read (P-B38B-02).

### 2.2 Results [C]

| Step | Count |
|---|---|
| SOI 501(c)(3) EINs with a FY2022+ return | 299,397 |
| … line 6 "N", assets ≥ $1m | 129,379 |
| − DAFRC panel / − batch-37 universe | 65 / 2,490 |
| Universe | 126,824 |
| With a FY2022+ 990 in index_2021–2026 (newest: FY2022 776, FY2023 1,581, FY2024 39,022, FY2025 83,362, FY2026 1,995) | 126,736 |
| Read OK (mirror 112,060; TEOS zip 14,676) | 126,736 |
| Newest return answers line 6 "Yes" (out of scope) | 52 |
| **In scope (line 6 "No")** | **126,684** |
| A (Part I values) / B1 / B2 / B3 / C / none | 11 / 24 / 39 / 3 / 331 / 126,276 |

| Verdict [I] | Rows | Examples |
|---|---|---|
| **sponsor_likely** | **3** | **Dakota Medical Charities** (ND, NTEE T50, FY2025, $89.5m): "serves as the home of Impact Foundation, ... Giving Hearts Day ... and more than 100 donor-advised funds" ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202602299349302105_public.xml)); **New Mexico Community Trust** (FY2024, $10.6m): mission "to manage and administer endowment and donor advised funds"; **Bayou Community Foundation** (LA, S01, FY2024, $3.5m): grants "requested by donors through Donor Advised Funds" |
| sponsor_possible | 6 | Sharp HealthCare Foundation (articles allow administering DAFs; $200.0m); Greater Rochester Community Health Foundation ("grant awards from donor advised and designated funds"; $24.9m); Miller-Dwan Foundation ("donor-directed funds"); Samaritan Bethany Foundation (Part I 14 DAFs, $267,568); Greater Gig Harbor Foundation; Starkey Foundation (one fund) |
| part_i_values_unexplained | 7 | Long Island Children's Museum (2 DAFs, $2.60m); a hockey club, an air-ambulance operator and a blood bank. These are operating charities with no DAF text |
| data_entry_suspect | 3 | Amount-like counts with no value (232,650; 2,934,838; 503,114) |
| not_sponsor_negation | 16 | "does not sponsor/maintain any donor advised funds", incl. 10 bank-trustee trusts with the same boilerplate |
| other_meaning | 14 | HUD-housing, charter-school and specialty-board "sponsoring organizations"; DAF services |
| holder_at_other_sponsor | 13 | Battelle (fund at The Columbus Foundation), Habitat Charlotte (FFTC), Lever Foundation (Charityvest) |
| grant_or_receipt | 9 | Dissolution transfers into DAFs at community foundations and federations |
| affiliate_or_related | 6 | NCF affiliates (Kentucky, Houston); Schedule R related organisations "administration of donor advised funds" (New Venture Fund, Washburn University Foundation) |

### 2.3 Reading [I]
- **Batch 37's conclusion holds on the full universe.** Beyond T30/T31/T70 and DAF-like names, only 3 of 126,684 line-6 "No" filers read as sponsors, and none files Part I values. The A-row Part I values total $2.96m and come mostly from operating charities misusing the DAF column.
- Combined with batch 37, the line-6 false-negative tail is **8 likely sponsors** (5 + 3). Only Groundswell files Part I values ($10.1m).
- **What the screen cannot see:**
  - filers under $1m of assets outside the batch-37 universe;
  - 990-EZ and 990-N filers outside it;
  - workplace platforms that hold "giving accounts" without using any of the four mention terms.

## 3. P-B37B-03: MS GIFT line 3

| FY (return) | Line 3 | Avg public securities (Part X 11) | **bps** | Savings/temp cash EOY | 7d net gain | Part XI 5 | 11g other fees | Line 24 items |
|---|---|---|---|---|---|---|---|---|
| 2021 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202203199349314745_public.xml)) | $1,083,289 | $4.31bn | **2.5** | $721.7m | $581.7m | −$215.7m | $9.76m | bank/processing $7.53m; meetings $0.87m |
| 2022 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202302999349301010_public.xml)) | $8,034,502 | $5.15bn | **15.6** | $318.6m | $44.0m | −$917.4m | $12.31m | FA commissions $2.81m |
| 2023 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202403209349313980_public.xml)) | $22,326,357 | $5.70bn | **39.2** | $302.9m | −$27.4m | $777.8m | $13.13m | FA commissions $1.92m |
| 2024 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503239349300435_public.xml)) | $3,390,568 (col C −$15,678; col D $3,406,246) | $7.14bn | **4.8** | $703.5m | $109.2m | $586.0m | $15.97m | FA commissions $2.03m |

- **Other filed facts [F]:**
  - 11f is blank in all four years.
  - Part XI line 9 FY2024 is a $3.0m "prior period adjustment related to grants payable".
  - Every return ticks "financial statements audited" and "consolidated".
  - The FY2024 [990-T](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503239339300405_public.xml) reports partnership income of −$15,678 ("INVESTMENT IN PARTNERSHIPS"), the same figure as line 3 column (C).
  - Schedule O and Schedule F carry no investment-income wording. Hits for "investment income booking" are nil.
  - The 2024 Impact Report (local copy) has no financial notes.
- **Reading [I]:**
  - The anomaly is year-specific, not structural.
  - FY2023's 39 bps is low but in the range of a cash-plus-some-dividends booking.
  - FY2024's 5 bps sits below plausible interest on $0.3–0.7bn of cash alone, while total return is normal.
  - The pattern fits income booked inside account-level total return (unitised or managed-account NAV changes, landing in Part XI line 5 or line 7) better than a fee wedge, which would need 11f/11g entries far above the $16m reported.
- **Open:** the FY2025 990 (not indexed at 2026-10-21) and the consolidated audit. The NY Charities Bureau site returned 500 to robots.txt, so it was not used.

## 4. P-B34A-03: recipient-side validation of R5 central weights

**Method (`recipients` task) [C].**
- R5 is rebuilt in memory from `mission_market_netting` functions. Central netting matches the published $5.52bn, $6.40bn, $4.05bn and $8.03bn to the dollar.
- **Targets:** the 10 included CF or single-issue recipients with the largest FY2021–24 central netting, plus Greater Horizons (named in the queue item; DAFRC type National).
- **For each recipient-year:**
  - inbound gross lines, central and upper netted amounts;
  - corrected Schedule D DAF contributions (same FY and next FY);
  - Part VIII line 1h total contributions from the SOI extracts;
  - the share of inbound dollars from grantors whose FYE month differs.

| Recipient (FYE) | Gross lines FY21–24 | Central | Central ÷ gross | DAF share of assets (central weight) | DAF contrib ÷ total contrib | Gross ÷ DAF contrib | Inbound from other-FYE grantors |
|---|---|---|---|---|---|---|---|
| SVCF (Dec) | $2,942m | $2,287m | 0.78 | 0.78 | 0.92 | 0.30 | 83% |
| NCF (Dec) | $660m | $582m | 0.88 | 0.95 | 0.93 | 0.07 | 56% |
| Greater Horizons (Dec) | $430m | $340m | 0.79 | 0.87 | 0.83 | 0.20 | 80% |
| Impact Investing CF (Dec) | $373m | $203m | 0.55 | 0.91 | 1.00 | 0.74 | 18% |
| JCF (Jun) | $314m | $290m | 0.92 | 0.96 | 1.00 | 0.10 | 21% |
| Tides Foundation (Dec) | $280m | $164m | 0.59 | 0.63 | 0.70 | 0.19 | 71% |
| International Generosity Foundation (Dec) | $192m | $181m | 0.94 | 0.99 | 1.00 | 0.51 | 35% |
| Greater Kansas City CF (Dec) | $140m | $93m | 0.66 | 0.73 | 0.82 | 0.09 | 18% |
| PEF Israel (Nov) | $133m | $80m | 0.60 | 0.64 | **0.20** | **0.78** | 100% |
| Christian Community Foundation (Mar) | $103m | $83m | 0.81 | 0.87 | 0.76 | 0.19 | 94% |
| CJP (Jun) | $100m | $82m | 0.82 | 0.83 | 0.70 | 0.15 | 9% |
| **Total** | **$5,667m** | **$4,385m** | **0.77** | | | | |

**Reading [I].**
- **The central weights are not too high for these recipients.**
  - Their recipient-side DAF share of contributions is at or above the asset share for 6 of 11, and within 0.13 below it for 4 more.
  - Substituting it lifts their FY2021–24 netting from $4.39bn to $4.80bn (+9%). By year: FY2021 $1.37bn vs $1.22bn, FY2022 $1.62bn vs $1.43bn, FY2023 $0.88bn vs $0.83bn, FY2024 $0.93bn vs $0.90bn.
- **The exception is PEF Israel.**
  - Only 19.5% of its contributions go to DAFs, yet inbound lines from other sponsors equal 78% of those DAF contributions (97% in FY2024).
  - Either most sponsor-to-sponsor money into PEF lands in DAFs, so the line nearly fills its DAF contributions, or most lands in non-DAF funds, so the asset weight of 0.64 is too high.
  - Filings cannot separate the two.
- **Impact Investing CF's** 0.55 central ratio reflects caps and grantor weights rather than its own weight (0.91). Its inbound lines come largely from the related Impact Investing Charitable Trust (a W5 pair excluded from the central tier).
- **Timing.**
  - SVCF's FY2022 inbound ($1.20bn, mostly NPT June-FYE lines) is 52% of its same-FY and 108% of its next-FY DAF contributions. Its FY2023 inbound ($0.28bn) is 25% of same-FY.
  - Same-FY matching therefore shifts netting between years at the largest recipient, though not in total.
  - NCF (7% of DAF contributions) is insensitive.
- **Audits were not read [U].** The queue's audit-based share (DAF vs other funds receiving sponsor transfers) remains open for SVCF, Tides and PEF Israel.
- **Proposal:** P-B38B-01 adds the contribution-share weight and a lag variant across all 929 recipients.

## 5. P-B32B-02: Endaoment fund count

| Route | Status |
|---|---|
| Public fund pages (endaoment.org/funds/…) | robots.txt: `User-Agent: * Disallow: /funds/ Disallow: /orgs/` → not fetched |
| app.endaoment.org, docs.endaoment.org | 403 (including robots.txt) → not fetched |
| api.endaoment.org | robots.txt 404. No documented unauthenticated fund-list endpoint was identified, and guessing endpoints was not attempted |
| On-chain factory events | OrgFundFactory `0x10fD9348136dCea154F752fe0B6dB45Fc298A589` on Ethereum, Base and OP Mainnet, event `EntityDeployed(address indexed entity, uint8 indexed entityType, address indexed entityManager)` per docs.endaoment.org text seen via search index [S]. publicnode.com refused `eth_getLogs` ("Archive requests require a personal token"), and other public RPC calls were not permitted in this session |
| FY2024/FY2025 audits | Not reachable (docs host 403) |

- **Result [U]:** the Schedule D counts (331; not reported; 6,000; 1,213) still have no public cross-check.
- Completing this needs an owner-approved archive RPC or block-explorer API credential for the factory logs. P-B32B-02 stays open.

## 6. P-BLB-04: commitment notes and two-digit maturities

**Changes to `mission_bdc_loans.py`** (documented in its docstring under "P-BLB-04"):
- (a) `xbrl_facts()` reads each `<ix:nonFraction>` in a hit row with its context date, concept, unit and scale. `two_period_rows()` splits every row with money facts on two or more dates into one row per (date, concept) and keeps a repeat once (own-period filing first). Output: `bdc-unfunded-commitments-two-period.csv`.
- (b) `DATE` also accepts MM/YY (month 01–12), and `identity_note()` reads `maturity_month()`.
- Main-CSV columns are unchanged, and the two-period rows still never enter latest marks.

**Results [C]** (cache from batch 36/Q-N16; 501 filings; no new fetches):
- Main CSV: 1,252 rows, as before. 66 rows changed: 64 KKR FS Income Trust / Select rows gain maturities, and 2 Barings Envestnet rows gain "11/31".
- **KKR FS Income Trust / Select debt rows with a maturity: 80 of 80** (0 before).
- Latest marks: 304 → 298 rows.
  - KKR's Momentive (Community Brands) 2031-07 facility was flagged "not_in_schedule_at_2026-09-30" from stale 2024-12-31 rows. It is now **held at 2026-09-30, 96.1% of par**:
    - Income Trust: $11.78m + $0.85m par; facility $12.63m;
    - Select: $11.02m.
  - KKR's Bonterra 2032-03 rows group into one facility per lender at 99.43% of par: Income Trust $44.5m; Select $37.0m.
- **Two-period commitment rows: 94** (money facts only), split from 49 filing rows. Groups: Community Brands/Momentive, Bonterra, Foundation Source, Bloomerang and Orion.
  - Example: Monroe Capital Income Plus, Bloomerang delayed draw $3.186m (2025-12-31) → $3.200m (2026-09-30); revolver $1.6m → $2.4m.
  - TCP Capital's CyberGrants/Bonterra unfunded balance: $555,556 (2021), $397,558 (2022), $194,444 (2023), $200,000 (2024). The current-period column prints "NA" and is listed in `periods_without_value`.
- **Quarterly refresh:** this run uses cached filings through the 2026-09-30 10-Qs. A refresh with `--fetch` reads new EDGAR filings when they appear.

## 7. P-LND-04: per-head vs per-FTE pay

- **Selection:** the 20 largest sponsors by Part I line 5 employees (latest return per EIN in `sponsor-salary-per-employee.csv`), excluding DAFRC single-issue categories. Universities and hospitals dominate otherwise, and none is a DAF labour benchmark.
- **Part VII** is read from each return [F]: persons with reportable compensation who are officers, key employees or highest compensated.

| Sponsor (FY) | W-2 heads | Paid Part VII staff | Wages per head (l5+l7) | Non-officer wages per head (l7 ÷ heads − Part VII staff) | Public FTE | Wages per FTE |
|---|---|---|---|---|---|---|
| NPT (2025) | 310 | 19 | $103,147 | $90,961 | 235+ US full-time [S] | **$136,066** |
| DAFgiving360 (2025) | 226 | 11 | $142,123 | $137,008 | [U] | — |
| Boston Foundation (2024) | 174 | 15 | $96,138 | $80,097 | [U] | — |
| Communities Foundation of Texas (2025) | 163 | 20 | $104,589 | $88,973 | [U] | — |
| Chicago Community Trust (2025) | 150 | 10 | $89,130 | $77,181 | [U] | — |
| AEF (2024) | 149 | 14 | $72,621 | $61,856 | [U] | — |
| FFTC (2024) | 141 | 14 | $88,891 | $76,553 | [U] | — |
| CAF America (2025) | 141 | 7 | $96,362 | $87,394 | [U] | — |
| Vanguard Charitable (2024) | 119 | 11 | $94,994 | $84,226 | [U] | — |
| … (full list in CSV) | | | | | | |

- **Median of the 20:** wages per head $95,566; non-officer wages per head **$84,226** [C].
- **Flagged rows:**
  - Tulsa CF (427 heads, $32,602 per head);
  - Vail Valley Foundation and Onward (part-time-heavy);
  - Community Action Partnership (no line 7);
  - Rockefeller Philanthropy Advisors (672 heads, including sponsored-project staff). Its only public "45 full-time staff" figure is undated, pre-2024 and not used.
- **Reading [I]:**
  - Per-FTE pay cannot be built from public sources for these sponsors. Audits do not disclose headcount, and 990s give only W-2 counts.
  - NPT's one secondary figure implies FTE ≈ 0.76 × heads. If that ratio were general, per-FTE wages would be about 1.3× per-head. That is an illustration, not a finding.
  - For AI-economics labour rates, the non-officer per-head series is the safer filed basis.

## 8. P-ANL-08: payout triad (analysis)

**Definitions [C]** (`triad` task):
- **Aggregate:** corrected market DAF grants_t ÷ corrected DAF assets_{t−1}, with rules R1–R4 as in `dafrc-corrected-market-totals.csv`.
- **Ex-DAF-to-DAF:** (grants − R5 netting) ÷ assets_{t−1}, in the R5 lower, central and upper tiers, rebuilt exactly.
- **Median sponsor:** median of sponsor-level corrected grants_t ÷ corrected BOY DAF assets.
  - Two scopes: BOY > $0, and BOY ≥ $1m. The ≥ $1m scope is the headline, because small bases give extreme ratios.
  - The sponsor-level ex-DAF-to-DAF figure subtracts the sponsor's own central outbound lines.

| FY | Aggregate | Ex-DAF-to-DAF central [lower–upper] | Median sponsor (BOY ≥ $1m) | Median ex-DAF-to-DAF | P25–P75 | Sponsors < 5% | n |
|---|---|---|---|---|---|---|---|
| 2021 | 28.5% | 25.2% [24.5–26.0] | 11.9% | 11.6% | 5.6–22.4% | 22.1% | 1,000 |
| 2022 | 23.8% | 21.0% [20.6–21.7] | 10.7% | 10.4% | 5.0–19.3% | 25.1% | 1,034 |
| 2023 | 24.0% | 22.3% [21.9–22.6] | 12.0% | 11.9% | 5.9–22.0% | 19.8% | 1,027 |
| 2024 | **25.9%** | **22.8%** [22.2–23.2] | **12.7%** | **12.2%** | 5.8–22.8% | 20.6% | 1,071 |

**FY2024 by segment (BOY ≥ $1m):**

| Segment | n | Aggregate | Aggregate ex-D2D | Median | Median ex-D2D | Sponsors < 5% |
|---|---|---|---|---|---|---|
| National | 68 | 24.0% | 20.8% | 22.2% | 18.6% | 13.2% |
| Community foundation | 637 | 21.6% | 18.1% | 11.6% | 11.4% | 17.3% |
| Single-issue | 273 | 35.3% | 33.4% | 16.7% | 16.3% | 22.7% |
| University/hospital | 77 | 14.0% | 12.3% | 5.1% | 5.1% | 49.4% |
| Processor | 16 | 190% | 181% | 157% | 157% | 12.5% |

**Practitioner reading (analysis, not a filed statistic) [I].**
1. The headline aggregate payout of about 24–29% is dollar-weighted toward national sponsors.
2. **The typical sponsor pays out about half that, 11–13%**, and one in five sponsors pays under 5% of opening DAF assets.
3. Netting DAF-to-DAF transfers lowers the aggregate by 1.7–3.3 points. It barely moves the median (0.1–0.5 points), because transfers are concentrated in a few large national sponsors.
4. National sponsors are the only segment whose median sits near the aggregate. Community foundations' median (11.6%) is about half their aggregate (21.6%).

**Caveats.**
- Sponsor-level values include DAFRC imputations where no filed value exists (batch 37 §6). They are not separated here.
- Processors' payout exceeds 100% (pass-through), so they are reported separately and are not removed from "all".
- Whether the triad changes adviser beliefs is the queue's testing question. It needs an adviser panel, which is out of scope here, and no outreach was made.

## 9. Limitations
- **P-B36A-01:** PPGF's policy text is [S]. Givinga's per-account activity is unknown.
- **P-B37B-01:**
  - The SOI extracts select the universe. A filer whose newest SOI row is older than its newest TEOS return was read on the newer return. Filers absent from the SOI extracts were not screened.
  - The 331 C rows are unreviewed.
  - Verdicts are [I].
- **P-B37B-03:** no audit was obtained, and the FY2025 return is unindexed.
- **P-B34A-03:**
  - The SOI 1h total is matched by EIN and the tax-period year.
  - Contribution shares use corrected DAFRC DAF contributions, which may be imputed in some years.
  - No audits were read.
- **P-B32B-02:** blocked (§5).
- **P-BLB-04:** XBRL facts depend on lenders tagging commitment notes. Untagged notes (heading-dated) are not split.
- **P-LND-04:** one secondary FTE figure only.
- **P-ANL-08:** see §8 caveats.

## 10. Source register

| ID | Source | Accessed | Used in |
|---|---|---|---|
| S1 | IRS SOI annual extracts [22–25eoextract990](https://www.irs.gov/statistics/soi-tax-stats-annual-extract-of-tax-exempt-organization-financial-data) (local copies); EO BMF eo1–eo4; TEOS [index_2021–2026](https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv) | local; HEAD 2026-11-15 | §1, §2, §4 |
| S2 | IRS e-file XML (GivingTuesday mirror; 2026 TEOS zips): 126,736 screen returns, MS GIFT 990 and 990-T FY2021–24, 20 sponsor returns, Givinga and PPGF CY2024 | 2026-11-15 | §1–3, §7 |
| S3 | Givinga [solutions](https://www.givinga.com/solutions), [workplace giving](https://www.givinga.com/workplace-giving), [terms](https://www.givinga.com/terms-and-conditions), [Janus Henderson post](https://www.givinga.com/insights/blog/partner-spotlight-janus-henderson-launches-charitable-investment-accounts-powered-by-givinga) | 2026-11-15 | §1 |
| S4 | PPGF Donor Account Policy and policy-updates pages (search-index text only [S]: [donor account policy](https://paypal.com/us/webapps/mpp/givingfund/policies/donor-account-policy)) | 2026-11-15 | §1 |
| S5 | Endaoment docs (search-index text [S]): [contracts overview](https://docs.endaoment.org/developers/contracts/overview), [entity deployment](https://docs.endaoment.org/developers/contracts/entity-deployment); endaoment.org/robots.txt | 2026-11-15 | §5 |
| S6 | SEC EDGAR BDC filings (cached; 501 filings) | cache 2026-11-14/15 | §6 |
| S7 | NPT recruiting text via job board [S] ([work at NPT](https://www.nptrust.org/contact-us/work-at-npt/) fetched; figure not on page); fiscalsponsordirectory.org RPA listing [S] | 2026-11-15 | §7 |
| S8 | Repo: `dafrc-sponsor-schedule-d-fy2019-2024.csv`, `dafrc-corrections-itemized.csv`, `dafrc-market-totals-netted.csv`, `sponsor-cost-structure.csv`, `sponsor-salary-per-employee.csv`, `daf-to-daf-recipient-whitelist.csv`; Schedule I cache of `mission_net_payout.py` | repo | §4, §7, §8 |

## 11. Data dictionary

### `line6-fulltext-screen.csv` (one row per filer with A or B evidence; newest FY2022+ 990)

| Column | Meaning |
|---|---|
| ein, name, bmf_ntee, state | Filer (index name; BMF NTEE; return state) |
| fiscal_year, tax_period, amended | FY (DAFRC convention), YYYYMM, AmendedReturnInd |
| line6_status, soi_line6, soi_tax_pd | Part IV line 6 in the return read (`line6_no` / `line6_blank`); SOI value and period that selected the EIN |
| evidence_class | A (Part I values), B1 (strong holding), B2 (holding), B3 (holding and receipt) [C] |
| review_verdict, review_note | Manual verdict [I] (§2.2 list) and reason |
| sd_daf_count … sd_other_eoy | Schedule D Part I, both columns [F] |
| total_assets_eoy | Part X line 16 EOY [F] |
| n_text_hits, n_strong_hits, hit_locations, evidence_text | Text windows matched, strong windows, schedule/element of the shown windows, up to two windows (strongest first) |
| return_object_id, xml_source, xml_url | Provenance (`gt_mirror` or `teos_zip`) |

### `payout-triad-2021-2024.csv` (one row per FY × scope × segment)

| Column | Meaning |
|---|---|
| fiscal_year, scope, segment | FY2021–24; `all_sponsors_boy_gt_0` or `sponsors_boy_ge_1m`; `all` or `mission_net_payout` segment |
| sponsor_years | Sponsors in the median sample |
| aggregate_gross_payout | `all`: corrected market grants ÷ prior-year corrected assets; segment rows: sums over the sample |
| aggregate_ex_daf_to_daf_central / _lower / _upper | As above, net of R5 (lower and upper for `all` only) |
| median_sponsor_gross_payout, median_sponsor_ex_daf_to_daf_central, p25/p75_sponsor_gross_payout | Sponsor-level distribution |
| share_sponsors_gross_below_5pct, share_sponsors_ex_d2d_below_5pct | Share of sample under 5% |
| boy_daf_assets, daf_grants, r5_central_outbound | Dollar bases |
| label, sources | "analysis [C]" and provenance |

### `sponsor-pay-per-fte.csv` (one row per sponsor; latest return)

| Column | Meaning |
|---|---|
| ein, sponsor_name, category, fiscal_year | Sponsor and return year |
| employees_part_i_l5, l05_…, l07_…, loaded_l5_10 | Part I line 5 and Part IX lines 5, 7 and 5–10 [F] |
| wage_all_per_head, loaded_all_per_head | (l5 + l7) ÷ heads; loaded ÷ heads [C] |
| part_vii_listed, part_vii_paid, part_vii_paid_staff, part_vii_paid_staff_comp, part_vii_paid_lt_35h | Part VII Section A counts: all listed; paid; paid officers, key and highest-compensated employees; their reportable compensation; of whom < 35 h/week [F] |
| non_officer_heads, non_officer_wage_per_head, officer_avg_comp_part_vii | heads − paid Part VII staff; l7 ÷ that; average Part VII staff compensation [C] |
| fte_public, fte_label, fte_source | Public FTE figure, label (S/U) and source text |
| wage_all_per_fte, loaded_all_per_fte, fte_to_head_ratio | Only where fte_public is set [C] |
| flags, return_object_id, xml_url | From `sponsor-salary-per-employee.csv`; provenance |

### `bdc-unfunded-commitments-two-period.csv` (one row per lender × borrower row × fact date × concept)

| Column | Meaning |
|---|---|
| company_group, target_company, identity_note, borrower_name_as_listed, lender_bdc, lender_cik | As in `bdc-loans-latest-marks.csv` |
| period_ending | The fact's own XBRL context date |
| row_type_source, instrument, maturity, maturity_month | Parsed type and terms of the source row |
| xbrl_concept, value_printed, xbrl_scale, value_usd | Fact concept (e.g. `us-gaap:InvestmentCompanyFinancialCommitmentToInvesteeFutureAmount`, `tcpc:UnfundedBalances`, `us-gaap:InvestmentOwnedAtFairValue`), printed text, scale, dollars (negated when sign="-") |
| periods_in_row, periods_without_value | All dates referenced in the row; dates with no money fact (e.g. "NA") |
| filing_period_ending, form, filing_date, adsh, dup_count, dup_filings, table_row_index, row_cells_raw, filing_url | Provenance; repeats across filings kept once |

### `queue-proposals-batch38b.csv`
- Format per [queue-proposals-README.md](../../data/mission-2026-11-14/queue-proposals-README.md).
- **P-B38B-01:** recipient-side contribution-share weight and lag tier for R5.
- **P-B38B-02:** confirm the new line-6 sponsor candidates and review class-C rows.

## 12. Reproduction
```
python3 scripts/mission_batch38_data.py fulltext   --irs-dir IRS --soi-dir SOI --work-dir WORK --fetch
python3 scripts/mission_batch38_data.py triad      --np-cache NPCACHE
python3 scripts/mission_batch38_data.py recipients --np-cache NPCACHE --soi-dir SOI
python3 scripts/mission_batch38_data.py msgift     --irs-dir IRS --work-dir WORK --fetch
python3 scripts/mission_batch38_data.py fte        --work-dir WORK --fetch
python3 scripts/mission_batch38_data.py accounts   --irs-dir IRS
python3 scripts/mission_bdc_loans.py --cache-dir CACHE
```
- **Directories:**
  - IRS holds eo1–eo4.csv and index_2021–2026.csv; SOI holds 21–25eoextract990.csv.
  - NPCACHE holds `netpayout990/` from `mission_net_payout.py`.
  - WORK receives `ft/` (JSON extracts), `xmlfull/` and `zipcd/`.
  - CACHE is the `mission_bdc_loans.py` EDGAR cache.
- Every figure above comes from the JSON summaries these tasks print, from the CSVs, or from the quoted documents.

## Validation corrections (wave 23, 2026-11-15) — governing
Source: [validation-wave23-report.md](validation-wave23-report.md); register `data/mission-2026-11-14/validation-register-wave23.csv`.

1. **§0, P-BLB-04 row (b).**
   - **Find:** "**All 80 KKR FS Income Trust / Select debt rows now carry a maturity**, where none did before."
   - **Replace with:** "**All 80 KKR FS Income Trust / Select debt rows now carry a maturity**, against 16 before (64 gained one) [V wave 23]."
2. **§0, P-BLB-04 row, Envestnet sentence.**
   - **Find:** "Barings' Envestnet rows gain their 11/31 maturity."
   - **Replace with:** "Barings' Envestnet rows gain their 11/31 maturity, but they also gain mis-parsed values: the raw cells read par 993, cost 996, fair value 979 (98.6%), yet the rows show fair value 0, 0% of par and `yes_lt_97`. The 2026-09-30 row enters latest marks. Treat it as a parse error until fixed [V wave 23]."
3. **§6, results.**
   - **Find:** "66 rows changed: 64 KKR FS Income Trust / Select rows gain maturities, and 2 Barings Envestnet rows gain \"11/31\"."
   - **Replace with:** "66 rows changed: 64 KKR FS Income Trust / Select rows gain maturities, and 2 Barings Envestnet rows gain \"11/31\" plus mis-parsed values (fair value 0 against a raw 979) [V wave 23]."
4. **§6, results.**
   - **Find:** "**KKR FS Income Trust / Select debt rows with a maturity: 80 of 80** (0 before)."
   - **Replace with:** "**KKR FS Income Trust / Select debt rows with a maturity: 80 of 80** (16 before) [V wave 23]."
5. **§0, P-B34A-03 row.**
   - **Find:** "CJP by 0.04–0.13"
   - **Replace with:** "CJP by 0.02–0.13 (NCF 0.017) [V wave 23]"
6. **§0, P-LND-04 row.**
   - **Find:** "That implies **$136,066 wages per FTE against $103,147 per head** (FTE/head 0.76)."
   - **Replace with:** "That implies **at most $136,066 wages per FTE against $103,147 per head** (FTE/head ≥ 0.76; \"more than 235\" is an undated secondary figure) [V wave 23]."
