# Queue batch 37 B: filing questions — line-6 "No" sponsors that hold DAFs, DAF-to-DAF disclosure, NPT's private-label book, adviser-managed shares at Fidelity and DAFgiving360, line-3 income booking, and the FY2024 DAFRC imputations

**Date:** 2026-11-15 · **Agent:** batch37 B · **Queue items:** P-99F-03, P-STF-03, P-GPT-03, P-QA3-06, P-B33A-03, P-99F-01 (`data/mission-2026-11-14/research-priority-queue.csv`)

**Outputs**
- [`data/mission-2026-11-14/line6-no-daf-holders.csv`](../../data/mission-2026-11-14/line6-no-daf-holders.csv): 44 returns of 44 non-DAFRC filers that answer Part IV line 6 "No" (or file a 990-EZ) and show DAF evidence. Each row carries a manual review verdict; 5 are likely sponsors and 8 possible (P-99F-03).
- [`data/mission-2026-11-14/dafrc-imputation-resolution-fy2024.csv`](../../data/mission-2026-11-14/dafrc-imputation-resolution-fy2024.csv): the 239 unresolved FY2024 asset and account rows (57 + 182), each re-tested (P-99F-01).
- [`data/mission-2026-11-14/queue-proposals-batch37b.csv`](../../data/mission-2026-11-14/queue-proposals-batch37b.csv): P-B37B-01 to P-B37B-03.
- **Script** (stdlib, functional style): [`scripts/mission_batch37_filings.py`](../../scripts/mission_batch37_filings.py), with tasks `line6`, `dafrc`, `texts` and `docs`. It reuses `mission_990_contractors` helpers and the batch-35 TEOS zip reader (`teos_fetch`).

**Conventions**
- FY = calendar year in which the tax period ends (DAFRC convention). **Recency:** every return read is FY2022 or later (TY2021+). Pre-2021 values appear only as a sponsor's last filed value bracketing an FY2024 imputation (P-99F-01, three rows).
- **Labels:** **[F]** filed or published value; **[C]** script computation; **[I]** inference or manual reading; **[S]** search-index or trade-press text; **[U]** not found.
- **Governing corrections read first:**
  - wave 21, end of [queue-batch36-metrics-rails.md](queue-batch36-metrics-rails.md): items 1–3 concern B2 account bounds and rail shares; none touches this batch;
  - wave 20, end of [queue-batch35-panel-screens.md](queue-batch35-panel-screens.md): support-test count wording; not used here;
  - wave 18, end of [queue-batch33-panel-scans.md](queue-batch33-panel-scans.md): item 1 applies (imputed values are year-end stocks; nothing here is summed across years). Items 4–5 apply to §5: DAFgiving360 is at 96–114 bps, and **MS GIFT is the only broker captive under 50 bps**;
  - wave 17, end of [queue-batch32-infund-costs.md](queue-batch32-infund-costs.md): items 4–7 and 10 apply to §5. A low line 3 is an anomaly *consistent with but larger than* fee netting, and income classified into gains is the competing explanation. §5 tests that explanation with audits.
- **Access.** robots.txt was read on every host before fetching:
  - fidelitycharitable.org, nptrust.org, fftc.org, endaoment.org, investmentnews.com and givechariot.com allow the paths used;
  - the S3 mirror and apps.irs.gov have none (404 or empty);
  - dafgiving360.org returned 403 even for robots.txt, so it was **not** fetched, and its figures below are [S];
  - businesswire.com's robots.txt timed out, so it was not fetched.
  - No logins, forms or contact. **This is research, not legal or tax advice.**

---

## 0. Answers in brief

| Item | Answer | Confidence |
|---|---|---|
| **P-99F-03** line 6 "No" but holds DAFs | **Screen:** 20,389 non-DAFRC 501(c)(3) EINs in the EO BMF with NTEE T30/T31/T70 or a DAF-like name. **9,566** filed a 990 or 990-EZ for FY2022+, and the newest return of each was read in full. 5,665 answer line 6 "No", 3,799 file a 990-EZ and 102 answer "Yes" (out of scope; the line-6 "Yes" population is covered by the outside-DAFRC scan) [F/C].<br>**DAF evidence in a "No" or 990-EZ return: 44 filers. After reading each one, 5 are likely sponsors and 8 possible** [I]. The rest are DAF holders at another sponsor (12), grants to or receipts from DAFs (10), affiliates (4), name matches (4) and one data-entry error.<br>- **Only one reports Schedule D Part I values: Groundswell Charitable Foundation** (workplace/app giving). Its **amended CY2024 return (filed 2026-01-28) reports 12,808 DAFs, $10,084,314 EOY and $9,691,912 contributions, but line 6 is still "No"**. The original CY2024 return and the CY2022–23 returns left Part I blank [F].<br>- The other likely sponsors say so in Part III or the mission text: DEED Community Giving Foundation ("will serve as a sponsoring organization of donor advised funds"), Visit.org Philanthropic Foundation, Caring Communities Foundation (line 6 "Yes" FY2020–24, "No" FY2025) and Impact France [F].<br>- **Size:** the 5 likely sponsors hold $21.2m of total assets; only $10.1m of DAF value is filed. **The false-negative tail adds sponsors, not money**, and the money is about 0.003% of FY2024 corrected DAF assets [C]. | High on the screen; verdicts [I]; universe limited to T30/T31/T70 and names |
| **P-STF-03** DAF-to-DAF reported separately? | **No sponsor in the screened filings or documents reports DAF-to-DAF grants as a separate line or note** [U].<br>- **Screened:** the FY2024 990 of each of the top-50 sponsors by FY2024 DAF assets, plus the named FY2023–25 returns: every Schedule O and Schedule D Part XIII text and every narrative leaf. Also Fidelity's FY2025 audit and 2026 Giving Report, NPT's FY2025 annual report and summary statements, and FFTC's 2025 audit.<br>- **Recipient side [F/C]:** each spike is one aggregated Schedule I line, and the recipients' Schedule D Part I shows only totals:<br>  - DAFgiving360 → Fidelity $976.6m (FYE 2025-06) = **3.7%** of Fidelity's FY2025 DAF contributions ($26.46bn, up $10.55bn), against +20,270 accounts;<br>  - Fidelity → Vanguard $480.1m = **8.3%** of Vanguard's FY2025 contributions, which were flat;<br>  - SVCF → NPT $1,591.3m (CY2024) = **11.0%** of NPT's FY2024 or **10.5%** of its FY2025 contributions, against +2,533 and +2,751 accounts.<br>Whether a transfer is one account or many cannot be read from public filings. | High that no separate disclosure exists in what was read |
| **P-GPT-03** NPT's private-label book | **NPT discloses no institutional/direct split** in its FY2023–25 990s (Schedule O and narrative), its FY2025 annual report, its FY2025 consolidated statements (a two-page summary with no segment note) or its financial-institutions page [U].<br>The page confirms "Private-label capabilities to support firm branding" and a 14–16-week program launch [F].<br>**New filed evidence of a bank channel:** NPT's FY2024 Schedule L (Part V text) says "Wells Fargo provides investment management services with respect to certain DAFs at NPT". It discloses five excess-benefit transactions, $2,144.17 repaid with interest, and a revised "application to open a DAF where Wells Fargo will serve as an investment manager" [F]. This corroborates the repo's code-only GP14 (Wells Fargo) program.<br>Entity totals only: FY2025 investments $47.84bn and cash $9.24bn; asset management fees $116.3m (FY2024 $94.3m) [F]. | High on absence; channel size remains [U] |
| **P-QA3-06** adviser-managed split | **Fidelity Charitable, assets [F/C]:** audited "Charitable Investment Advisor Program" (adviser-managed) investments are $22.43bn of $52.65bn (**42.6%**, June 2023), $27.55bn of $61.51bn (**44.8%**, 2024) and $37.14bn of $79.23bn (**46.9%**, 2025). **No account split is published:** the Giving Report counts 246,006 DAFs (YE2025) and 395,500 donors with no adviser breakdown [U].<br>**DAFgiving360 [S]:** "78% of assets in DAF accounts were associated with an advisor" (FY2025 release) and "77%" (CY2025, InvestmentNews quoting DAFgiving360). The FY2026 release cites ">5,400 advisory firms" and "an average of 15 donors" per advisor. This is an *adviser-relationship* share, **not** an adviser-managed share. No audit or account split was reachable [U]. | High for Fidelity assets; low for DAFgiving360 (secondary text only) |
| **P-B33A-03** line-3 income booking | **FFTC and the Foundation for the Charlotte Jewish Community: classification, confirmed by audit [F].**<br>- FFTC's 2025/2024 consolidated audit, which includes FCJC as a supporting organisation that "use[s] the Foundation to administer and invest their assets", says net investment income "consists of interest and dividends and is presented net of related expenses". Gains are a separate line ($606.9m in 2024, $678.8m before reclassifying agency funds and annuities).<br>- 37.7% of FFTC's 2024 investments sit in hedge, private and partnership funds ($1.73bn), whose income is inside NAV changes.<br>- The 990 matches: line 7 reports gross sales equal to gains with cost basis 0, i.e. realised gains only. Line 7d plus Part XI line 5 = $609.9m, against the audit's $606.9m [C].<br>- Fees are a minor layer: adding line 11f ($6.36m) back lifts FFTC's line 3 only from 33.8 to 50.9 bps.<br>**Endaoment FY2024 is a line-7 artefact:** $9.08m of "other" asset sales with cost basis 0 = gain; line 3 is $22,300. FY2025 is normal: line 3 $333,755 and 7d $84,522 [F].<br>**MS GIFT stays unexplained:** gross sales $3.96bn and cost $3.85bn are reported normally, line 3 is $3.39m on $7.92bn of public securities, and there is no public audit and no FY2025 return in the index yet (P-B37B-03). | High for FFTC/FCJC; [I] for Endaoment; open for MS GIFT |
| **P-99F-01** FY2024 imputations | **Of 239 unresolved rows, 2 gain a new filed value and 132 already equal a filed value** [C]:<br>- **New:** Highland Park Community Foundation's later FY2024 return (202543169349303214) files 3 accounts and $44,864, against 2 and $29,006 imputed.<br>- **Already filed:** 131 account rows and 1 asset row where DAFRC's "Imputed" value equals the 990 Part I figure (1,377 accounts, $0).<br>- **The 2026 harvest fill (FY2025 returns only) resolves no FY2024 value.** It brackets 2 sponsors (Gorge CF, USC: 4 rows; $63.9m imputed against a $63.6m interpolation). The full harvest brackets 3 more ($14.5m against $11.8m).<br>- **Université de Montréal ($427.1m imputed) files $0 again in FY2025**, so it cannot be bracketed.<br>- **Still unresolved:** 48 asset rows ($593.5m imputed) and 45 account rows (9,104 accounts). 79 FY2025 returns in index_2021–2026 added no value. | High |

---

## 1. P-99F-03: line 6 "No" (or 990-EZ) filers that hold DAFs

### 1.1 Method
- **Universe:**
  - IRS EO BMF (eo1–eo4), subsection 03, with NTEE T30 (public foundations), T31 (community foundations) or T70 (federated giving), or a name matching `DONOR ADVISED|GIFT FUND|GIVING FUND|CHARITABLE FUND|DAF`;
  - minus the 1,594 DAFRC panel EINs.
  - That gives 20,389 EINs. **9,566** have a 990 or 990-EZ in index_2021–2026 for a tax period ending 2022 or later. The newest such return per EIN was read (max tax period, then max object id) [C].
- **Extract (`extract_l6`)**, from the full XML (GivingTuesday mirror; TEOS zip fallback for 2026 returns):
  - return type, Part IV `DonorAdvisedFundInd`, total assets, and Schedule D Part I (both columns);
  - **every text leaf in the return** that mentions "donor advised" or "DAF", with a ±260-character window.
- **Automatic class:**
  - A = any positive Part I DAF value;
  - B = holding language (e.g. "establish/administer/maintain … donor advised", "N donor advised funds", "our donor advised funds");
  - C = mention or receipt only;
  - D = none.
- **Manual review [I]:** every A, B and C row in scope (line 6 "No" or 990-EZ) was read and given a verdict (`REVIEW` table in the script, with the reason in `review_note`).

### 1.2 Results

| Status | Returns | A | B | C | D |
|---|---|---|---|---|---|
| Line 6 "No" | 5,665 | 2 | 15 | 25 | 5,623 |
| 990-EZ | 3,799 | 0 | 0 | 2 | 3,797 |
| Line 6 "Yes" (out of scope) | 102 | | | | |

| Verdict [I] | Filers | Examples (FY, total assets) |
|---|---|---|
| **sponsor_likely** | **5** | **Groundswell Charitable Foundation** (CY2024 amended: 12,808 DAFs, $10.08m; $11.0m assets) ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202640289349301029_public.xml)); DEED Community Giving Foundation (FY2024, $7.2m); Caring Communities Foundation (FY2025, $1.4m); Impact France (FY2025, $0.9m); Visit.org Philanthropic Foundation (FY2024, $0.6m) |
| sponsor_possible | 8 | United Way of the Coastal Empire (Part XIII reconciliation item "DONOR ADVISED FUNDS −1,187,656"; $25.5m); Whitewater CF ($15.7m); Global Charitable Fund ($6.4m); Moriah Foundation ($6.1m); Wet Mountain Valley CF; Palmyra CF; Penny Foundation; Legacy Cellar Foundation (990-EZ, $7k) |
| data_entry_suspect | 1 | Boone County Senior Services Foundation: 70,085 "DAFs" with no value, on $2.2m of assets |
| affiliate_or_related | 4 | Tides Network; United Way of South Hampton Roads (a Schedule R related org "investing and distributing donor advised funds"); TSF Services (Seattle Foundation); an NCF affiliate |
| holder_at_other_sponsor | 12 | Seattle Christian Foundation (DAFs "held by National Christian Foundation"); Rotary and school foundations holding DAFs at community foundations |
| grant_or_receipt | 10 | Grants "to establish a donor advised fund" at Santa Barbara Foundation, etc. |
| name_or_other | 4 | "The Quick DAF Inc", "Charitable DAF HoldCo" |

### 1.3 Reading [I]
- **The line-6 false-negative tail is small and new.**
  - Three of the five likely sponsors are workplace, app or online-giving platforms (Groundswell, DEED, Visit.org). This is the same model as the micro-account processors (batch 36 §1).
  - Groundswell's 12,808 accounts average $787. It would fall into batch 36's A3 small-balance screen if it had ≥5,000 accounts and an average under $500. It does not quite: the average is above $500.
- **Money is negligible:** $10.1m of filed DAF value (0.003% of FY2024 corrected DAF assets of about $323bn) [C].
- **The "possible" group is mostly local community foundations whose wording is ambiguous.** Their Schedule D is blank, so no value can be added.
- **Not covered:** filers outside T30/T31/T70 without a DAF-like name. Groundswell, DEED and Visit.org happen to carry T30, but other workplace platforms may not (P-B37B-01).

## 2. P-STF-03: are DAF-to-DAF grants reported separately?

**Method.**
- `texts` task. It reads each target return's full XML and greps every narrative leaf for transfer-to-other-sponsor language: "transfer … other/another sponsoring organization/donor advised fund", "DAF-to-DAF", "fund-to-fund", "succession … another".
- **Targets:** the top 50 DAFRC sponsors by FY2024 DAF assets (FY2024 returns), plus the named FY2023–25 returns: 57 returns read [C].
- A broader regex ("sponsoring organization", "transfer … DAF") was also run over all 59 cached XMLs.
- The `docs` task greps the downloaded documents for the same terms.

**Results [F/U].**
- **No return carries a DAF-to-DAF note.** The only matches describe the filer's own status ("operates as a 'sponsoring organization' within the meaning of Code section 4966"; Fidelity: "for Schedule I purposes a recipient organization is only listed once").
- **No document reports it either:** Fidelity's audit (only fair-value level transfers), the Fidelity 2026 Giving Report, NPT's FY2025 annual report and statements, and FFTC's audit. DAFgiving360's annual report could not be fetched (403).

| Spike (grantor's Schedule I line) | Recipient's same-FY Schedule D contributions | Line ÷ contributions | Recipient Δ accounts |
|---|---|---|---|
| DAFgiving360 → Fidelity $976,570,217 (FYE 2025-06; one line, purpose "PUBLIC, SOCIETAL BENEFIT") ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202611199349300601_public.xml)) | Fidelity FY2025 $26,464,117,648 (FY2024 $15.91bn) | **3.7%** | +20,270 (204,614 → 224,884) |
| Fidelity → Vanguard $480,068,133 (FYE 2025-06) | Vanguard FY2025 $5,751,399,753 (flat) | **8.3%** | (batch 35 §5) |
| SVCF → NPT $1,591,322,838 (CY2024) | NPT FY2024 $14.52bn / FY2025 $15.15bn (NPT FY ends June) | **11.0% / 10.5%** | +2,533 (FY2024) / +2,751 (FY2025) |

- **Reading [I]:** the recipients' account growth is ordinary in each case, and none of their filings mentions the inflow. Whether a $1.59bn line is one account or many cannot be told from public data.
- Payout statistics net of DAF-to-DAF therefore still rely on the Schedule I edge netting in [queue-batch33-panel-scans.md](queue-batch33-panel-scans.md) §4.

## 3. P-GPT-03: NPT's private-label book

| Source | What it shows | Split? |
|---|---|---|
| NPT 990 FY2023–25 ([FY2024 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202511339349301311_public.xml), [FY2025 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601289349302480_public.xml)) | Schedule D: 15,407 → 17,940 → 20,691 DAFs; $22.84bn → $42.12bn → $55.90bn. No Schedule O text on institutions, partners or private label | No [U] |
| NPT FY2024 Schedule L Part V [F] | "WELLS FARGO PROVIDES INVESTMENT MANAGEMENT SERVICES WITH RESPECT TO CERTAIN DAFS AT NPT"; five de-minimis excess-benefit payments by Wells Fargo to donor-advisers who were Wells Fargo advisers (2021–24), all repaid ($2,144.17 with interest); the "application to open a DAF where Wells Fargo will serve as an investment manager" was revised | No; confirms a bank-managed channel |
| [FY2025 annual report](https://www.nptrust.org/annual-reports/npt-annual-report/) | $6.44bn granted; 159,000+ grants; "This report reflects NPT's U.S. donor-advised fund program only"; serves "individuals, families, foundations, corporations, family offices, and financial institutions" | No [U] |
| [FY2025 consolidated statements](https://www.nptrust.org/wp-content/uploads/2026/09/FY25-AR-Consolidated-Financials-NPT.pdf) (2 pages, in thousands) | Investments $47,837,978 and cash $9,243,758; contributions $15,290,620; net investment return $5,423,118; asset management fees $116,260 (FY2024 $94,289) | No notes, no segments [U] |
| [For Financial Institutions](https://www.nptrust.org/advisors-and-institutions/for-financial-institutions/) | "Private-label capabilities to support firm branding"; "Flexible partnership models"; launch "in approximately 14-16 weeks" | No figures |

- **Reading [I]:**
  - The bank and wealth share of NPT's $55.9bn stays unknown.
  - The Wells Fargo disclosure shows that some NPT DAFs are invested by a partner's advisers. It also shows that NPT's 990 can surface the channel only incidentally, through Schedule L.
  - The $116m of asset-management fees (about 27 bps of average FY2025 investments) is a cost line, not a channel split.

## 4. P-QA3-06: adviser-managed versus other at Fidelity and DAFgiving360

### 4.1 Fidelity Charitable (audited, Note 3) [F/C]

| June year end | CIAP adviser-managed investments | Total investments | **Share** | Source |
|---|---|---|---|---|
| 2023 | $22,433,249,315 | $52,650,176,429 | **42.6%** | [FY2024/23 audit](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2024-2023.pdf) |
| 2024 | $27,546,211,645 | $61,514,405,850 | **44.8%** | [FY2025/24 audit](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf) |
| 2025 | $37,139,208,368 (equities $15.61bn, mutual funds $10.08bn, alternatives/PE $7.06bn, fixed income $4.40bn) | $79,232,938,398 | **46.9%** | same |

- **Accounts [U]:**
  - The audit says the Gift Fund "maintains donor sub-accounts within each investment pool or advisor-managed account" but gives no counts.
  - The [2026 Giving Report](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf) gives 246,006 DAFs (YE2025) and about 395,500 donors, with no adviser split. Its only adviser item is the "advisor Practice Management & Consulting program".
  - The Schedule D count is 224,884 (FYE 2025-06), an average of $380k per account [C].
  - The CIAP $100k minimum (batch 32 §2) caps CIAP accounts at about 371k, which does not bind [C].
- **Trend [C]:** the CIAP share rose 4.3 points in two years. CIAP grew 66% (2023→25) against 39% for the other (pooled) investments ($30.22bn → $42.09bn).

### 4.2 DAFgiving360 [S]
- **FY2025 release (2025-07-29, via search index):** "Seventy eight percent of assets in DAF accounts were associated with an advisor"; "over 4,700 financial advisors".
- **CY2025:** "77% of DAF assets were associated with an advisor relationship"; "more than 5,200 financial advisors" ([InvestmentNews, 2026-01-27](https://www.investmentnews.com/practice-management/dafgiving360-donors-boost-2025-grants-to-nearly-10b/264994), quoting DAFgiving360).
- **FY2026 release (2026-07-28, via search index):** "more than 5,400 advisory firms … each advisor working with an average of 15 donors". At face value that is about 81,000 adviser-linked donors, against 128,497 FY2025 Schedule D accounts. The ~63% this implies mixes firms with advisers and donors with accounts [C/I].
- **Reading [I]:**
  - "Associated with an advisor" (DAFgiving360) and "adviser-managed" (Fidelity CIAP) are different concepts. A DAFgiving360 account can be adviser-linked yet invested in the pools.
  - **For A3/A4 scoring:** Fidelity ≈ 47% of assets adviser-managed (June 2025); DAFgiving360 ≈ 77–78% of assets adviser-associated, with the adviser-managed share unpublished.
  - **No account split exists for either sponsor.**

## 5. P-B33A-03: income versus gains for the line-3 focus hits

| Return | Line 3 | Line 7a gross sales / 7b cost | 7d | Part XI line 5 | Line 11f | Audit evidence |
|---|---|---|---|---|---|---|
| FFTC FY2024 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543219349306689_public.xml)) | $12,552,376 (33.8 bps) | $74,771,049 / **$0** | $74,771,049 | $535,172,646 | $6,359,863 | "Net investment income … consists of interest and dividends and is presented net of related expenses"; 2024 net investment income $15,415,927; net investment gains $606,880,847 (gross $678,752,434 less agency funds $70.8m and annuities $1.0m); hedge/private funds $1,670,954,169 and partnerships $63,738,227 of $4,595,397,102 investments ([2025/24 audit](https://www.fftc.org/sites/default/files/2026-10/Foundation_for_the_Carolinas12-31-25_Audit_FS_Client2.pdf)) |
| FCJC FY2024 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503219349315735_public.xml)) | $506,077 (23.2 bps) | $1,300,617 / **$0** | $1,300,617 | $20,931,507 | $532,385 | Consolidated in FFTC's audit; uses FFTC "to administer and invest" its assets (Note 1) |
| Endaoment FY2024 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202542899349300104_public.xml)) | $22,300 | "other" $9,081,225 / **$0** | $9,081,225 | $30,558 | — | No FY2024 audit found (FY22–23 audit only) [U] |
| Endaoment FY2025 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202631359349315978_public.xml)) | $333,755 | "other" $84,522 / $0 | $84,522 | $67,860 | — | — |
| MS GIFT FY2024 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503239349300435_public.xml)) | $3,390,568 (4.2 bps) | $3,955,990,369 / $3,846,812,022 | $109,178,347 | $586,049,974 | $4,237,948 | No public audit (batch 32); FY2025 990 not indexed [U] |

- **Reading:**
  - **FFTC and FCJC: classification [F/I].** Interest and dividends are booked net of expenses on one line. Income from 37.7% of investments (hedge, private and partnership funds) accrues inside fund NAVs and so appears in gains.
  - The 990 reproduces the audit's split: line 7 carries the realised part with a zero basis, and Part XI line 5 the unrealised part. 7d + XI 5 = $609.9m against the audit's $606.9m [C].
  - A netted fee layer exists but is small: the audit nets "related expenses", and the 990 also shows 11f of $6.36m. Even adding 11f back, line 3 is only 50.9 bps.
  - **Endaoment FY2024 [I]:** its "normal total return" comes from booking $9.08m of non-cash (likely crypto) liquidation proceeds as zero-basis gains. It is not an income-classification case. FY2025 looks ordinary.
  - **MS GIFT [I]:** unlike FFTC, it reports gross sales and cost basis, so its gains lines are complete. A 4 bps line 3 on $7.9bn of public securities remains unexplained without its audit. Wave 17's "classification more likely than fees" stays unproven for MS GIFT (P-B37B-03).

## 6. P-99F-01: FY2024 imputed sponsor-years

**Method.**
- `dafrc` task. Input: the 239 rows of `dafrc-corrections-itemized.csv` with fiscal_year 2024, applied 0, and metric `daf_assets_eoy` (57) or `daf_accounts_eoy` (182). Each row is tested in order:
  1. a FY2024 row in the 2026 harvest fill;
  2. any *other* FY2024 990 for the EIN in index_2021–2026 (amended or later), read in full;
  3. DAFRC's "Imputed" value equals the filed Part I value already used;
  4. a next filed (FY2025) value, from the fill, then the full harvest, then any FY2025 990 in the index, interpolated linearly with the last DAFRC-filed value (proxy only; not used when the FY2025 value is 0 after a positive one).

**Results [C].**

| Resolution | Asset rows (imputed $) | Account rows (imputed accounts) |
|---|---|---|
| **New filed value** (other FY2024 return) | 1 ($29,006 → $44,864) | 1 (2 → 3) |
| **Already equals filed** | 1 ($0) | **131 (1,377)** |
| Bracketed by fill FY2025 (proxy) | 2 ($63.92m → $63.57m) | 2 (50 → 45.5) |
| Bracketed by harvest FY2025 (proxy) | 3 ($14.48m → $11.84m) | 3 (116 → 109.5) |
| Next value $0, not used | 2 ($427.14m; Université de Montréal $427.13m) | — |
| **Unresolved** | **48 ($593.50m)** | **45 (9,104)** |
| **Total** | **57 ($1,099.1m)** | **182 (10,649)** |

- **The 2026 harvest fill holds FY2025 returns only** (144 rows), so it **cannot by itself turn any FY2024 imputation into a filed value**. It brackets 4 rows (Gorge CF, USC).
- Only 2 FY2024 returns outside the corrections file exist in the indexes. One is Highland Park CF's later FY2024 return, which supplies the two new filed values. 79 FY2025 returns were read and added no value beyond the harvest.
- **Largest unresolved asset rows:**
  - Foundation for Advanced Philanthropy $176.8m (no FY2024 990 indexed);
  - Walker Area CF $80.4m (Part I blank in FY2024 *and* FY2025);
  - Omaha Community Foundation $75.9m (count filed, value blank);
  - Milwaukee Jewish Federation $47.8m;
  - TOP Jewish Foundation $37.1m.
- **Net effect on FY2024 corrected totals:** +$15,858 and +1 account from new filed values. The 131 "already equal" account rows change no total; they only reclassify 1,377 accounts from imputed to filed.

## 7. Limitations
- **P-99F-03:**
  - The universe is NTEE T30/T31/T70 plus DAF-like names. A sponsor with another NTEE code and a neutral name is invisible.
  - Only the newest FY2022+ return per EIN was read (Groundswell's earlier returns were checked by hand).
  - Text verdicts are manual readings [I].
  - 990-N filers (no return content) cannot be screened.
- **P-STF-03:** DAFgiving360's and Vanguard's annual reports were not read (403, or no report found). The screen is a regex over narrative text, so a disclosure in a table without narrative would be missed.
- **P-GPT-03:** NPT's full audited notes (if any exist beyond the two-page summary) were not found. Partner ADVs and annual reports (J.P. Morgan, UBS, BMO, Rathbones, Cazenove) were not read in this batch.
- **P-QA3-06:** every DAFgiving360 figure is [S]: search-index snippets of its own releases and trade press. dafgiving360.org returned 403 to robots.txt and was not fetched.
- **P-B33A-03:**
  - FFTC's audit nets "related expenses" without stating them.
  - The Endaoment reading relies on the filing structure only.
  - MS GIFT is unresolved.
- **P-99F-01:** interpolations are proxies, not filed values, and are never applied to totals here. index_2026 still has Last-Modified 2026-10-21 (batch 36).

## 8. Source register

| ID | Source | Accessed | Used in |
|---|---|---|---|
| S1 | IRS EO BMF eo1–eo4.csv; IRS TEOS indexes [2021–2026](https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv) | local copies (2026-11-14/15) | §1, §6 |
| S2 | IRS e-file XML via the GivingTuesday mirror (9,566 + 81 + 59 returns; URLs per CSV row and §2–5 links); 2026 TEOS zips for unmirrored returns | 2026-11-15 | §1–6 |
| S3 | Fidelity Charitable audited statements [FY2025/24](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf) and [FY2024/23](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2024-2023.pdf); [2026 Giving Report](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf) | 2026-11-15 | §2, §4 |
| S4 | Foundation For The Carolinas [2025/2024 consolidated audit](https://www.fftc.org/sites/default/files/2026-10/Foundation_for_the_Carolinas12-31-25_Audit_FS_Client2.pdf) (linked from [foundation-financials](https://www.fftc.org/foundation-financials)) | 2026-11-15 | §5 |
| S5 | NPT [2025 Annual Report](https://www.nptrust.org/annual-reports/npt-annual-report/), [FY25 consolidated financials](https://www.nptrust.org/wp-content/uploads/2026/09/FY25-AR-Consolidated-Financials-NPT.pdf), [For Financial Institutions](https://www.nptrust.org/advisors-and-institutions/for-financial-institutions/) | 2026-11-15 | §2, §3 |
| S6 | DAFgiving360 FY2025 and FY2026 releases (dafgiving360.org; search-index text only [S]); [InvestmentNews 2026-01-27](https://www.investmentnews.com/practice-management/dafgiving360-donors-boost-2025-grants-to-nearly-10b/264994); [Chariot FY25 report recap](https://givechariot.com/resources/insights/breaking-down-the-dafgiving360-fy25-annual-report) (no adviser figures) | 2026-11-15 | §4 |
| S7 | Endaoment [FY22–23 audit](https://storage.googleapis.com/endaoment-static/docs-assets/audit-fy22-23.pdf) (search result only; out of window, not used for figures) | 2026-11-15 | §5 |
| S8 | Repo: `dafrc-sponsor-schedule-d-fy2019-2024.csv`, `dafrc-corrections-itemized.csv`, `form990-harvest-2026-fill.csv`, `form990-returns-schedule-d-harvest-full.csv`, `non-dafrc-daf-filers-990.csv`, `daf-to-daf-flows-990.csv`, `daf-to-daf-fy2025-counterparts.csv`, `npt-givingpoint-programs-2026.csv`, `low-investment-income-screen.csv` | repo | all |

## 9. Data dictionary

### `line6-no-daf-holders.csv` (one row per filer; newest FY2022+ return; line 6 "No" or 990-EZ with DAF evidence)

| Column | Meaning |
|---|---|
| ein, name, bmf_name, ntee, state | Filer (return name; BMF name, NTEE, state) |
| universe_basis, name_signal | `ntee` (T30/T31/T70) or `name` (DAF-like name only); 1 if the BMF name matches the DAF-name regex |
| fiscal_year, tax_period, return_type | FY (DAFRC convention), YYYYMM, `990` or `990EZ` |
| line6_status, daf_ind_part_iv | `line6_no`, `990EZ` or `line6_blank`; raw Part IV `DonorAdvisedFundInd` |
| evidence_class, evidence_source | A (`schedule_d_part_i_daf_values`), B (`text_says_holds_dafs`), B2 (holding and receipt language), C (`receipt_or_payment_mention_only`, `mention_only`) [C] |
| review_verdict, review_note | Manual verdict [I]: `sponsor_likely`, `sponsor_possible`, `data_entry_suspect`, `affiliate_or_related`, `holder_at_other_sponsor`, `grant_or_receipt`, `name_or_other`; reason |
| sd_daf_count, sd_daf_eoy, sd_daf_contributions, sd_daf_grants, sd_other_count, sd_other_eoy | Schedule D Part I, both columns [F] |
| total_assets_eoy | Part X (990) or Part II (990-EZ) EOY total assets [F] |
| n_daf_text_hits, n_hold_hits, hit_locations | Number of DAF text windows, holding-language windows, and the schedule/element they sit in |
| evidence_text | Up to two quoted windows (holding windows first) [F] |
| return_object_id, xml_status, xml_url, index_url | Provenance |

### `dafrc-imputation-resolution-fy2024.csv` (one row per unresolved FY2024 sponsor × metric)

| Column | Meaning |
|---|---|
| fiscal_year, ein, name, type, metric | Key (`daf_assets_eoy` or `daf_accounts_eoy`) |
| evidence_class_before, note_before | From `dafrc-corrections-itemized.csv` |
| dafrc_imputed_value, filed_value_fy2024_return, fy2024_return_object_id | DAFRC's imputed value; the value filed in the return the corrections file used (blank if none) |
| other_fy2024_returns_checked, other_fy2024_return_status | Other FY2024 990 object ids found in index_2021–2026 and their read status |
| fill_fy2024_value, fill_fy2025_value, fill_fy2025_object_id | 2026 harvest fill values (the fill holds FY2025 only) |
| harvest_fy2025_value, harvest_fy2025_object_id, index_fy2025_value, index_fy2025_object_id | Next filed value from the full harvest or a FY2025 990 in the index |
| last_filed_fy, last_filed_value | DAFRC's last non-imputed value before FY2024 |
| interpolated_fy2024_proxy | Linear interpolation last filed → FY2025 [C]; a proxy, never a filed value |
| resolution | `filed_value_from_other_fy2024_return`, `filed_value_from_2026_fill_fy2024`, `already_equals_filed_value`, `bracketed_by_{fill,harvest,index}_fy2025_proxy_only`, `next_value_zero_*_not_used`, `next_value_only_*_no_prior_filed`, `unresolved` |
| resolved_value, resolved_value_source | New value (filed or proxy) and its object id or `interpolation` |
| becomes_filed_value, becomes_new_filed_value | 1 if the row is now a filed value (incl. already equal); 1 if a new filed value replaces the imputation |
| delta_vs_imputed | resolved_value − dafrc_imputed_value |

### `queue-proposals-batch37b.csv`
- Format per [queue-proposals-README.md](../../data/mission-2026-11-14/queue-proposals-README.md).
- **P-B37B-01:** widen the line-6 false-negative screen beyond NTEE T30/T31/T70.
- **P-B37B-02:** DAFgiving360 audits, and adviser-managed versus adviser-associated shares.
- **P-B37B-03:** MS GIFT's audit or FY2025 return for the line-3 anomaly.

## 10. Reproduction
```
python3 scripts/mission_batch37_filings.py line6 --irs-dir IRS --work-dir WORK --fetch
python3 scripts/mission_batch37_filings.py dafrc --irs-dir IRS --work-dir WORK --fetch
python3 scripts/mission_batch37_filings.py texts --irs-dir IRS --work-dir WORK --fetch
python3 scripts/mission_batch37_filings.py docs  --doc-dir DOCS
```
- IRS holds eo1–eo4.csv and index_2021–2026.csv. WORK receives `l6/` (JSON extracts), `xmlfull/` (full XML for the text reads), and `teos/` and `zipcd/` (zip range reads).
- DOCS holds `pdftotext -layout` output of the S3–S5 PDFs and the text of the two NPT pages.
- Each task prints a JSON summary; every figure in §0–6 comes from those summaries, the two CSVs or the quoted documents. Ratios in §0 and §4–5 were computed from those figures.
