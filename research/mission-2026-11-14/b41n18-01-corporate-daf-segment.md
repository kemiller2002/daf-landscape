# Corporate-DAF segment at sponsors that do not publish it (P-B41N18-01)

**Date:** 2026-11-19 · **Task:** P-B41N18-01 (proposed by batch41 N18) · **Builds on:** [direction-corporate-dafs.md](direction-corporate-dafs.md), including its wave-26 governing corrections, and SA01–SA05 in [`corporate-daf-programs-2021-2026.csv`](../../data/mission-2026-11-14/corporate-daf-programs-2021-2026.csv).

**Outputs**
- [`data/mission-2026-11-14/corporate-daf-segment-2026-11-19.csv`](../../data/mission-2026-11-14/corporate-daf-segment-2026-11-19.csv): 76 rows in the SA01–SA05 column layout:
  - SN01–SN61: one row per Form 990 return, recording that it has no split;
  - SV2021–SV2025 and FC2024–FC2025: published corporate splits;
  - SE01–SE04: estimates;
  - CN01–CN04: corporate programs named on sponsor pages that the SEC-based list does not have.
- [`scripts/mission_b41n18_01_corporate_segment.py`](../../scripts/mission_b41n18_01_corporate_segment.py): builds the CSV and computes every [C] and [I] figure. Run it as `python3 -I scripts/mission_b41n18_01_corporate_segment.py . <extract.json>`.
- [`data/mission-2026-11-14/queue-proposals-b41n18-01.csv`](../../data/mission-2026-11-14/queue-proposals-b41n18-01.csv): P-B41N1801-01 to -04.

**Labels:** [F] first-party document read this pass · [X] Form 990 e-file XML value · [C] computed here · [I] inference or extrapolation · [R] repo value carried over, not re-read.

---

## 0. Answers in brief

| Question | Answer | Confidence |
|---|---|---|
| Do the 14 sponsors publish a corporate vs individual split? | **13 of 14 publish none, for any of the four metrics** (DAF counts, contributions, grants, fees), in any CY2021–2025 source read:<br>- 61 Form 990 returns: Schedule O and Schedule D narrative, plus a full-text scan of every narrative field;<br>- audited statements where reachable;<br>- annual reports and web pages.<br>**The exception is SVCF.** Its audited notes give **corporate-advised fund grants** for every year 2021–2025: about $100m, $175m, $134m, $189m and $153m [F]. SVCF publishes no corporate count, contribution, asset or fee figure. | High for the sources read; 5 community foundations’ statements could not be read: Chicago and California CF (robots.txt 403), Oregon CF (/assets disallowed), Columbus (none located) and GKCCF (no statements link) (§6) [V wave 36A] |
| Corporate share where data exist (grants) | - **SVCF:** 2.8%–6.9% of advised-fund grants by year [C].<br>- **Fidelity Charitable:** 3.5% (2024) and 2.95% (2025) of all grants [C].<br>- **Pooled Fidelity + SVCF:** **3.9% (CY2024)** and **3.4% (CY2025)** [C].<br>- Adding AOGF's Schedule D DAF column as if it were all corporate raises the pooled share to **9.1%** [C]. That is an upper bound only for this three-sponsor pool, not for the market. It mixes CY2025 with FYE 2026-03 and puts AOGF’s non-DAF other-funds column ($935.7m) in the denominator. Its level is set mainly by AOGF’s weight in the pool ($1.39bn of $22.8bn). AOGF’s Schedule D Part XIII says corporate donors give into its DAFs with ongoing advice, while individual micro-donations carry none. So the column is probably mostly corporate [I], and 9.1% is likely close to the pool’s true value rather than a loose bound [V wave 36A] | High (lower bound); medium (upper bound) |
| Corporate share of assets | **Not estimable from published data** except at AOGF: its DAF column holds $205.7m of $268.0m Schedule D end-of-year value (76.7%) [C]. Neither Fidelity nor SVCF publishes corporate assets. | — |
| Extrapolation to the 13 sponsors without a split | **[I] $278m–$691m of corporate DAF grants**, on $9.95bn of FY2024 Schedule D grants. This applies the observed 2.8%–6.9% range. It assumes their mix is like Fidelity's and SVCF's, which is untested. Tides and GKCCF probably sit above it (§4). | Low |
| Do sponsor sources confirm the repo's named programs? | **Sponsor-side confirmation in the 2021+ window: PagerDuty and Unity (Tides blog, 2021), NVIDIA (SVCF page, 2022) and Remitly (RPA article, 2026).**<br>- Okta and Twilio appear only in dated Tides posts (2018, 2019).<br>- The other named programs appear in no sponsor's 990, audited statements or pages: Braze, Olo, Zuora, Upwork, Rapid7, Hyatt (NPT), CrowdStrike (CAF), Brilliant Earth, Pluralsight and Lam.<br>- Four corporate programs that the SEC list lacks were found on sponsor pages: DoorDash and eBay (SVCF), Bain Capital Relief Fund and IR+M (Boston Foundation). | High |

---

## 1. Scope and method

**Sponsors.**
- Four named in the task: Tides Foundation, CAF America, Rockefeller Philanthropy Advisors (RPA) and National Philanthropic Trust (NPT).
- **The 10 largest community foundations**, defined as the 10 rows with `type = Community Foundation` and the highest FY2024 `daf_assets_eoy` in [`daf-sponsor-league-table-fy2021-2025.csv`](../../data/mission-2026-11-14/daf-sponsor-league-table-fy2021-2025.csv): SVCF, Chicago Community Trust, Foundation For The Carolinas, Greater Kansas City CF, New York Community Trust, Columbus Foundation, Oregon CF, Boston Foundation, California CF and CF for Greater Atlanta.
- Religiously-affiliated community foundations (Jewish community foundations, the Christian Community Foundation) are typed "Single Issue Charity" in the league table and are not included.

**Steps.**
1. **Return list.** All Form 990 filings for the 14 EINs were taken from the IRS e-file index files for 2022–2026 (`apps.irs.gov/pub/epostcard/990/xml/<year>/index_<year>.csv`, read from the copies cached in earlier passes). That gave **63 filings**, tax periods 2021-04 to 2025-09. Where an amended return exists, only the latest is kept, leaving **61 returns**.
2. **XML.** Each return was read from the GivingTuesday 990 data lake, `https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/<object_id>_public.xml`.
   - 49 files were byte copies cached by earlier passes; 14 were fetched this pass.
   - All 63 parsed, and the EIN in each file matches the index.
3. **Extraction.**
   - Schedule D Part I DAF and "funds and other accounts" columns (`DonorAdvisedFundsHeldCnt`, `…ContriAmt`, `…GrantsAmt`, `…VlEOYAmt`).
   - Every Schedule D supplemental and Schedule O explanation.
   - A regex scan of **every** text field in each return (Part III program text, mission, Schedule I purposes) for corporate-DAF phrases.
   - The values match the repo harvest [`form990-returns-schedule-d-harvest-full.csv`](../../data/mission-2026-11-14/form990-returns-schedule-d-harvest-full.csv) for the 46 overlapping returns that have harvest values (0 mismatches). A 47th overlapping return, Boston Foundation 202641269349301584, has blank harvest values (http_404) [C] [V wave 36A]
4. **Audited statements and reports.** These were found through each host's robots-allowed sitemap or financials page, then converted with `pdftotext` and searched for "corporate", "company" and "advised":
   - Tides consolidated FS (CY2022, CY2023, CY2024);
   - CAF America FS (FYE 2023-04, 2024-04) and the CAF Group Annual Report 2024/25;
   - SVCF audited FS (FY2022–FY2025);
   - Boston Foundation FY2023 and FY2025;
   - Foundation For The Carolinas CY2025;
   - NYCT 2025 financials and 2025 annual report;
   - CF for Greater Atlanta CY2024;
   - Fidelity Charitable Giving Reports 2025 and 2026, re-read to check SA01.
5. **Name check (task item 6).** Every CD row naming a sponsor was searched, by company and fund name, across all 63 XMLs, the fetched pages, the PDF texts and the sponsors' sitemap URL lists. Hits in Schedule I recipient or address fields were false positives (for example "Huntington Road", "Brazelton") and were discarded by hand.
6. **Estimate.** The script computes the pooled shares and the [I] extrapolation from rows SV, FC and SN (§4).

**Rules followed.**
- robots.txt was fetched and logged for every host before any other request (§8).
- A generic User-Agent (`research-script/1.0`) was used, with at least 2 s between requests and the stated crawl-delay where one was set.
- No logins, forms or outreach.
- sec.gov, crt.sh and certspotter were not used.
- Evidence is from 2021 onward. Three June- or April-year-end returns ending in 2021 (FYE 2021-04/06) are flagged `in_window_edge`, and the estimate does not use them.

---

## 2. Results: what each sponsor publishes

**One finding holds for all 61 returns: Form 990 never splits DAFs by donor type.**
- Schedule D Part I has no corporate column.
- Schedule O and Schedule D narrative only describe policies, governance and compensation.
- Part III and mission text mention corporations only as one donor group among several:
  - Tides: "contributions received from individuals, families, foundations, and corporations";
  - CAF America: "connecting donors – individuals, families and corporations";
  - NPT: "individuals, families and companies";
  - NYCT: "individuals, families, and businesses";
  - FFTC: "supports personal and corporate philanthropy".

### 2.1 Split status by sponsor and metric (CY2021–2025)

"none" means no corporate vs individual split was found in any source read.

| Sponsor | DAF counts | Contributions | Grants | Fees | Other first-party sources read | FY2024 Sch D total (DAFs; grants; EOY) [X] |
|---|---|---|---|---|---|---|
| Tides Foundation | none | none | none | none (fees "1% on standard donor advised funds to 5%"; no corporate schedule) | Consolidated FS CY2022–24; corporations page; fees FAQ | 261; $210.7m; $324.5m |
| CAF America | none | none | none | none | FS FYE 2023-04 and 2024-04, which split by entity (CAF America / CADF / CAF Canada) only; corporations page; Employee Engagement Fund page | 770; $821.2m; $441.3m (FYE 2024-04) |
| Rockefeller Philanthropy Advisors | none | none | none | none | Sitemap: no annual report or FS found | 67; $41.8m; $87.2m |
| National Philanthropic Trust | none | none | none | none | Annual Reports FY23, FY24, FY25 (web): totals and sectors only | 17,940; $5,563.3m; $42,119.3m (FYE 2024-06) |
| **SVCF** | none | none | **corporate-advised grants, 2021–2025** | none (corporate fee minimum only for SVCF-managed scholarship funds: $50,000 corporate vs $35,000 individual) | Audited FS FY2022–25; corporate-advised fund page; fund-types page | 1,011; $3,064.4m; $9,578.1m |
| Chicago Community Trust | none (990 only) | none (990 only) | none (990 only) | none | robots.txt 403: site not fetched | 1,914; $1,407.7m; $4,650.0m (FYE 2024-09) |
| Foundation For The Carolinas | none | none | none | none | Audited FS CY2025; FAQ ("individual, nonprofit and corporate clients") | 1,047; $721.8m; $2,617.7m |
| Greater Kansas City CF | none | none | none | none ("Keeping fees low and reasonable"; "Not requiring minimums") | Corporate-giving pages: "**Hundreds of companies** rely on us to organize their philanthropy under one structure: a corporate donor-advised fund"; no FS found | 3,052; $297.1m; $2,574.0m |
| New York Community Trust | none | none | none | none | 2025 financials; 2025 annual report (assets by fund type: DAF 34%, no corporate type) | 1,342; $123.5m; $1,254.6m |
| Columbus Foundation | none (990 only) | none (990 only) | none (990 only) | none | Sitemap 404; FS not located | 1,533; $171.9m; $1,232.3m |
| Oregon CF | none (990 only) | none (990 only) | none (990 only) | none | `/assets` disallowed by robots.txt: PDFs not fetched | 1,394; $94.3m; $1,106.4m |
| Boston Foundation | none | none | none | none | FS FY2023 and FY2025; company-giving page names corporate DAFs (CN03, CN04) | 734; $144.3m; $1,097.0m (FYE 2024-06) |
| California CF | none (990 only) | none (990 only) | none (990 only) | none | robots.txt 403: site not fetched | 827; $209.8m; $1,090.7m (FYE 2024-06) |
| CF for Greater Atlanta | none | none | none | none | Consolidated FS CY2024 (net assets by fund type; donor-advised $1,025.4m; no corporate type) | 744; $140.4m; $1,025.4m |

Year-by-year values for every return are in CSV rows SN01–SN61. One filed anomaly is passed through unchanged: NYCT's CY2023 Schedule D DAF grants are $13.4m, against $125.5m in CY2022 and $123.5m in CY2024 [X].

### 2.2 Corporate signals that are not splits

- **Tides CY2024 Schedule I** lists a $1,696,333 grant to "AMERICAN ONLINE GIVING FOUNDATION INC (EMPLOYEE GIVING)" [X] ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202523189349301347_public.xml)). This is one $1.7m Tides grant to AOGF’s employee-giving program (purpose “Equity, human rights, and economic empowerment”). It does not show which Tides fund made the grant, or that the money is corporate, so it is a signal only [V wave 36A] The corporations page also advertises "partnerships with employee giving match programs" [F].
- **CAF America** sells an Employee Engagement Fund: company-funded matching-gift and volunteer-grant funds [F]. These funds are not reported separately.
- **The CAF Group (UK) Annual Report 2024/25** reports "Corporate donors £71.2m paid out to charities worldwide" [F]. This is a group-wide figure, not CAF America's and not DAF-specific, so it is **not used** for sizing.
- **Fidelity Charitable 2024:** the corporate share of grant *count* was 24,975 of "nearly 2.7 million" grants, about **0.9%** [C]. The corporate share of grant *dollars* was 3.5%: corporate grants average more than three times the dollar size.
- **Fidelity Charitable, accounts:** 556 corporate DAFs against 224,884 DAFs on its FYE 2025-06 Schedule D is about **0.25%** of accounts [C]. The periods differ (CY2025 vs FYE 2025-06), but corporate DAFs are clearly a tiny share by count and a low-single-digit share by grant dollars.

---

## 3. Published splits used for sizing

### 3.1 Fidelity Charitable (SA01, re-read)

| Year | Corporate DAFs | Corporate grants | All grants | Corporate share [C] | Source |
|---|---|---|---|---|---|
| 2024 | 518 | $525M (24,975 grants; average $21,024) | $14.9bn | 3.52% | [2025 Giving Report](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf) [F] |
| 2025 | 556 | $539.8M (26,036 grants; average $20,732) | $18.3bn | 2.95% | [2026 Giving Report](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf) [F] |

The 2025 report also gives 2023 corporate grants as $237M. SA01's note on the restatement ($256m in the 2024 report) still applies. No corporate assets, contributions or fees are published.

### 3.2 SVCF corporate-advised funds (SA02, extended back to 2021)

Each audited statement gives two years, under its "Corporate Advised" and "Advised Funds" programme descriptions in Note 1 (Programs), not in a net-asset note [V wave 36A].

| Year | Corporate-advised grants | Donor-advised grants | Corporate share of the two [C] | Source |
|---|---|---|---|---|
| 2021 | ~$100m | ~$2,155m | 4.43% | [FY2022 audit](https://www.svcf.org/assets/img/heroA/svcf-financial-statement-audit-2022.pdf) [F] |
| 2022 | ~$175m | ~$2,553m | 6.41% | [FY2023 audit](https://www.svcf.org/assets/img/heroA/svcf-financial-statement-audit-2023.pdf) [F] |
| 2023 | ~$134m | ~$4,657m | 2.80% | [FY2024 audit](https://www.svcf.org/assets/img/heroA/svcf-financial-statement-audit-2024.pdf) [F] |
| 2024 | ~$189m | ~$3,077m | 5.79% | [FY2025 audit](https://www.svcf.org/assets/files/publications/SVCF-CFS-FY25_Updated-Financials.pdf) [F] |
| 2025 | ~$153m | ~$2,051m | 6.94% | FY2025 audit [F] |

- In the 2023 share, the denominator is inflated by large one-off donor-advised grants: SVCF's 2023 top impact areas were Health $1.6bn and Sciences $1.4bn ([by-the-numbers 2023](https://www.svcf.org/annual-reports/2023/by-the-numbers)) [F].
- **It is not established whether Schedule D Part I includes corporate-advised funds.** CY2024 Schedule D grants ($3,064m) are close to the donor-advised line alone. CY2022 Schedule D grants ($3,936m) match neither line, probably because of grants-payable timing (P-B41N1801-03).

### 3.3 AOGF (SA03, carried over)

- FYE 2026-03 Schedule D values were re-read from the cached XML [X]:
  - DAF column: 695 accounts; $1,557.8m contributions; $1,390.0m grants; $205.7m end-of-year value;
  - other-funds column: 751,746 accounts; $935.7m grants.
- The wave-26 correction applies: the DAF column also holds "other fund structures". It is used here **only as an upper bound** on corporate.

---

## 4. Bounded estimate

**A. Sponsors with data (Fidelity, SVCF, AOGF), corporate share of DAF grants [C]:**

| Basis | Corporate grants | Denominator | Share |
|---|---|---|---|
| Fidelity + SVCF, CY2024 (SE01) | $714m | $18.17bn | **3.93%** |
| Fidelity + SVCF, CY2025 (SE02): lower bound | $692.8m | $20.50bn | **3.38%** |
| Plus AOGF DAF column treated as wholly corporate, CY2025 / FYE 2026-03 (SE03): upper bound | $2,082.8m | $22.83bn | **9.12%** |

**The bounded answer: corporate DAFs account for about 3.4%–9.1% of grants across the sponsors that publish data.** The lower figure (3.4%–3.9%) is the published fact. Everything above it depends on how much of AOGF's DAF column is corporate.

**Assets.** No bound is possible at Fidelity or SVCF. [I] Corporate DAFs are probably lighter in assets than in grants, because the one sponsor with column data shows a pass-through pattern:
- AOGF DAF column: end-of-year value is 0.15× grants ($205.7m ÷ $1,390.0m) [C];
- Fidelity overall: 5.6× ($85.5bn ÷ $15.25bn, FYE 2025-06 Schedule D, repo harvest) [C].

**B. [I] Extrapolation to the 13 sponsors without a split (SE04).**
- Method: apply the lowest and highest single-year shares observed at Fidelity and SVCF (2.80% to 6.94%, CY2021–2025) to the 13 sponsors' FY2024 Schedule D DAF grants. FY2024 follows the league-table convention: Tides FYE 2024-12, CAF FYE 2024-04, NPT FYE 2024-06, and so on.
- Base: $9.95bn of grants, of which NPT is $5.56bn.
- Result: **$278m–$691m of corporate DAF grants [I]**. Two further caveats apply. If a sponsor reports corporate funds outside its Schedule D DAF column (unknown even at SVCF, §3.2), the corporate amount adds to the base rather than sitting inside it. CAF America’s FYE 2024-04 Schedule D ($821.2m grants; $441.3m end-of-year value) does not match CAF America’s own column in its consolidating schedule ($730.5m grants to third parties; $200.5m designated DAFs). The end-of-year value is near the consolidated $430.8m, so the base may include CADF and CAF Canada [V wave 36A]

Why this is low confidence:
- **NPT dominates the base**, and NPT publishes nothing on its corporate book. Hyatt is the only NPT corporate DAF named in SEC filings.
- **Tides is probably above the band [I].**
  - It is Pledge 1%'s default U.S. corporate DAF partner (direction doc §3).
  - Eight SEC-named corporate DAFs sit at Tides. That is **≥3.1% of its 261 CY2024 DAFs by count** [C], if all eight are still active.
  - Its web page claims "over 400 donor advised funds", which does not reconcile with the 261 on its 990.
- **GKCCF's "hundreds of companies" claim** implies ≥200 corporate DAFs [I: reading "hundreds" as at least 200]. That is **≥6.6% of its 3,052 DAFs by count**, which is far above Fidelity's 0.25%. The page is undated marketing copy and counts companies, not funds, so the 200-fund floor is an inference, not a filed number [V wave 36A]
- Count floors from named programs elsewhere are small:
  - RPA: ≥1 of 67 (1.5%; Remitly) [C];
  - SVCF: ≥5 named corporate-advised funds (Brilliant Earth, Pluralsight, NVIDIA, DoorDash, eBay) against 1,011 Schedule D DAFs (0.5%) [C]. It is unknown whether Schedule D counts them.

---

## 5. Named corporate DAF programs checked against sponsor sources (task item 6)

| CD row | Company | Sponsor per repo | Sponsor-side evidence this pass | Status |
|---|---|---|---|---|
| CD21 | PagerDuty | Tides | Tides blog 2021-07-09: "$350,000 from the Pagerduty.org Fund at Tides Foundation" ([page](https://www.tides.org/blog/pagerduty-org-leverages-technology-to-help-save-lives/)) [F] | **Confirmed** |
| CD23 | Unity | Tides | Tides blog 2021-07-12: "work with through Tides is Unity and the Unity Charitable Fund" ([page](https://www.tides.org/blog/jessica-lindl-on-empowering-unity-creators-and-employees-to-make-the-world-a-better-place/)) [F] | **Confirmed** |
| CD17 | Okta | Tides | Tides blog 2018-01-16 on the Okta for Good partnership ([page](https://www.tides.org/blog/okta-tides-partner-strengthen-connections-people-technology-community/)) [F] | Confirmed, **dated (pre-2021)** |
| CD09 | Twilio | Tides (secondary) | Only a 2019 Tides video post (`/blog/video-tides-twilio-edovo/`) [F] | Still only dated evidence |
| CD13, CD18, CD19, CD20, CD22 | Braze, Olo, Zuora, Upwork, Rapid7 | Tides | Not named in any Tides 990, audited statement, the corporations page or a sitemap URL. The corporations page names only Sephora. | Not confirmed by sponsor (SEC filings only) |
| CD33 | NVIDIA | SVCF | "the NVIDIA Foundation, a corporate advised fund at Silicon Valley Foundation" ([svcf.org/nvidia](https://www.svcf.org/nvidia), dated 2022-11-09) [F] | **Confirmed** |
| CD30, CD31, CD32 | Brilliant Earth, Pluralsight, Lam | SVCF | Not on any SVCF page or statement read | Not confirmed by sponsor |
| CD12 | Remitly | RPA | RPA article 2026-01-12 on the Remitly Foundation's "partnership with RPA" ([page](https://www.rockpa.org/centering-community-to-advance-financial-health-insights-from-the-remitly-foundations-philanthropic-journey/)) [F]. It does not say DAF. | Relationship confirmed; vehicle per the 10-K only |
| CD49 | Hyatt | NPT | Not in NPT's 990s or annual reports | Not confirmed by sponsor |
| CD29 | CrowdStrike | "Charities Aid Foundation" | Not in CAF America's 990s, FS or pages | Not confirmed; the entity stays ambiguous |
| CD01, CD27, CD28 | Circle, Align, Steve Madden | Fidelity | Fidelity reports give aggregates only | Not confirmed by sponsor (no fund-level disclosure) |
| **New: CN01** | DoorDash | SVCF | "DoorDash to establish a corporate advised fund with SVCF" ([donor story](https://www.svcf.org/annual-reports/donor-2025/donor-stories-2025-26-doordash)) [F] | Add (private-side discovery) |
| **New: CN02** | eBay Foundation | SVCF | "has had a corporate advised fund at SVCF since 2008" ([donor story](https://www.svcf.org/annual-reports/donor/donor-stories-ebay), 2023) [F] | Add |
| **New: CN03** | Bain Capital | Boston Foundation | "the Bain Capital Relief Fund, a corporate Donor Advised Fund (DAF)" ([company giving](https://www.tbf.org/donors/company-giving), undated) [F] | Add (undated) |
| **New: CN04** | Income Research + Management | Boston Foundation | "Why One Firm Chose a DAF for Its Corporate Philanthropy" (same page) [F] | Add (undated) |

**Pattern.** Sponsors confirm corporate funds only in marketing stories, never in filings. This fits the direction doc's finding that "sponsor anonymity is the norm".

---

## 6. Limits

- **Robots-blocked or unreachable sites.** These were not read beyond their 990s:
  - Chicago Community Trust and California Community Foundation: robots.txt returned 403;
  - Oregon CF: `/assets` disallowed;
  - Columbus Foundation: sitemap 404, no statements located;
  - GKCCF: no statements link found.
  Any of them could publish an SVCF-style corporate line.
- **Year coverage.** CY2025 Form 990s are not yet filed for most calendar-year sponsors. SVCF's and Fidelity's 2025 figures come from audited statements and reports.
- **Schedule D scope.** It is unknown whether community foundations put corporate-advised funds in the Schedule D DAF column. That affects any share computed on Schedule D denominators (P-B41N1801-03).
- **The extrapolation (SE04)** rests on two sponsors. It is a scale indication, not a measurement.
- **AOGF's column** mixes corporate and other structures, so the 9.1% figure is a ceiling.
- **Fund-name lists** (NYCT annual report) were not classified (P-B41N1801-02).
- **Cached files.** 49 of the 63 XMLs were byte copies from earlier passes' caches. All parsed with matching EINs, and the values match the repo harvest.
- **Fidelity fee terms** ($10,000 plus 0.60% tiered) are carried from the direction doc [R] and were not re-read.

---

## 7. Data dictionary: `corporate-daf-segment-2026-11-19.csv`

The columns are identical to `corporate-daf-programs-2021-2026.csv`. Their use in this file:

| Column | Meaning here |
|---|---|
| program_id | SNnn = one Form 990 return with no corporate split; SVyyyy = SVCF published corporate-advised grants for year yyyy; FCyyyy = Fidelity published corporate grants; SEnn = estimate; CNnn = corporate program named on a sponsor page and absent from CD01–CD49 |
| row_type | `sponsor_aggregate`, `estimate` or `company_program` |
| company, ticker, cik | Descriptor for aggregate rows; company name for CN rows (private companies have no ticker or CIK) |
| sponsor | Sponsor name |
| sponsor_basis | Source type: `Form 990 Sch D/Sch O (e-file XML)`, `audited statements`, `sponsor report`, `sponsor page`, `computed` |
| fund_name | Fund label where one exists |
| program_type | `sponsor_no_corporate_split` (SN), `sponsor_corporate_program` (SV/FC), `pooled_published_share` / `extrapolated_share` (SE), `corporate_advised_fund` / `corporate_daf` (CN) |
| year_established | CN rows only, as stated by the sponsor |
| evidence_year | Fiscal year end (SN, as `FYE yyyy-mm`), calendar year (SV/FC) or estimate basis (SE) |
| amount_usd | SV/FC: corporate grants in USD. SE: corporate grants in the estimate (low end for SE04). SN and CN: blank, because no corporate figure exists |
| amount_basis | SN: the explicit no-split statement for counts, contributions, grants and fees, plus Schedule D Part I DAF totals (count, contributions, grants, EOY). SV/FC: quoted basis plus the [C] share. SE: method and result |
| shares | Not used (blank) |
| purpose_tags | SN: sponsor segment (national, community, …); SV/FC: `published corporate split (grants only)`; SE: `bounded estimate` or `extrapolation [I]`; CN: purpose |
| pledge_1pct | Not used (blank) |
| source_url, source_form, source_date | Primary source (990 XML URL in the GivingTuesday data lake, PDF or page); form type; filing year or publication date |
| label | X = 990 XML value; F = first-party document; C = computed; I = inference or extrapolation |
| recency_flag | `in_window`; `in_window_edge` for fiscal years ending before Dec 2021, and for undated pages |
| notes | What the non-990 sources show for that sponsor (audited statements, reports, robots blocks); EIN and object_id for SN rows |

Amounts are **not additive across rows**: SN rows have none, and SE rows re-use SV/FC values.

---

## 8. Source register and robots log

### 8.1 robots.txt log (2026-11-19 UTC)

| Host | robots.txt result | Used? |
|---|---|---|
| gt990datalake-rawdata.s3.amazonaws.com | 404 (no robots file, so allowed) | Yes: 14 XML fetches |
| apps.irs.gov | 302 to irs.gov/404 (no robots file) | Index files read from earlier-pass caches |
| www.tides.org | 200 (disallows /wp-admin, /wp-json, search only) | Yes |
| cafamerica.org | 200 (disallows /admin, /forms; crawl-delay 10, honoured) | Yes |
| www.rockpa.org | 200 (allow all) | Yes |
| www.nptrust.org | 200 (allow all for `*`) | Yes |
| www.svcf.org | 200 (disallows /cpresources, /vendor, /cache) | Yes |
| www.fidelitycharitable.org | 200 (disallows /retired, /nuance, a docs/vessel path) | Yes (2 PDFs) |
| www.fftc.org | 200 (Drupal defaults) | Yes |
| www.growyourgiving.org (GKCCF) | 200 (allow all) | Yes |
| thenytrust.org (redirect from nycommunitytrust.org) | 200 (allow all) | Yes |
| www.columbusfoundation.org | 404 (allowed) | Sitemap 404; homepage only |
| oregoncf.org | 200 (**disallows /assets**) | Not fetched (PDFs sit under /assets) |
| www.tbf.org | 200 (allow all for `*`) | Yes |
| cfgreateratlanta.org | 200 (crawl-delay 10, honoured) | Yes |
| www.cct.org | **403** | **Not fetched** |
| www.calfund.org | **403** | **Not fetched** |
| www.giarts.org, www.philanthropy.com | 200 | Checked, not used |

The web fetch log (sitemaps, pages and PDFs) has 148 requests: 147 returned 200 and 1 returned 404 (the Columbus sitemap). The 14 XML fetches are logged separately.

### 8.2 Sources

| ID | Source | Date | Used for | Label |
|---|---|---|---|---|
| S1 | 61 Form 990 e-file XMLs (one per sponsor return; URL pattern `https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/<object_id>_public.xml`; each URL is in CSV `source_url`), located via IRS index `https://apps.irs.gov/pub/epostcard/990/xml/<year>/index_<year>.csv` (2022–2026) | filed 2022–2026 | SN rows; narrative scan; Tides Sch I AOGF grant | X |
| S2 | [Tides FY22 FS](https://www.tides.org/wp-content/uploads/2023/11/Tides-Organizations-FY22-FS-and-SS-FINAL.pdf); [2023 audited](https://www.tides.org/wp-content/uploads/2024/12/2023-Consolidated-Audited-Financials.pdf); [FY24 FS](https://www.tides.org/wp-content/uploads/2025/10/2024-Tides-Organizations-FY24-Consolidated-FS.pdf); [corporations page](https://www.tides.org/partners/corporations/); [fees FAQ](https://www.tides.org/faq/fees-funds-tides/) | 2023–2025 | Tides split status, fees | F |
| S3 | Tides blog: [PagerDuty](https://www.tides.org/blog/pagerduty-org-leverages-technology-to-help-save-lives/) (2021-07-09); [Unity](https://www.tides.org/blog/jessica-lindl-on-empowering-unity-creators-and-employees-to-make-the-world-a-better-place/) (2021-07-12); [Okta](https://www.tides.org/blog/okta-tides-partner-strengthen-connections-people-technology-community/) (2018); [Twilio](https://www.tides.org/blog/video-tides-twilio-edovo/) (2019) | 2018–2021 | §5 | F |
| S4 | CAF America [FY23 audit report](https://cafamerica.org/getContentAsset/cf187d66-6ee7-50e2-9579-78a80e2de3a6/727347a9-de62-4980-909f-5714723a79ba/EXTERNAL-VIEW-CAF-America-FY23-audit-report-Charities-Aid-Foundation-America-FYE-April-2023-audit-report.pdf); [FS April 2024](https://cafamerica.org/getContentAsset/29cbabcf-6b31-5092-855f-0aa951aff618/727347a9-de62-4980-909f-5714723a79ba/Consolidated-Financial-Statements-with-Supplemental-Schedules-CAF-America-April-2024.pdf); [corporations](https://cafamerica.org/who-we-serve/corporations); [Employee Engagement Fund](https://cafamerica.org/what-we-do/employee-engagement-fund); [CAF Group AR 2024/25](https://cafamerica.org/getContentAsset/1171eaf0-d8a9-5832-94ef-c051568b6136/727347a9-de62-4980-909f-5714723a79ba/CAF-Group-Annual-Report-2024_25.pdf) (p. 27) | 2023–2025 | CAF split status; group corporate figure (not used) | F |
| S5 | NPT annual reports: [FY23](https://www.nptrust.org/annual-reports/the-2023-annual-report/); [FY24](https://www.nptrust.org/annual-reports/the-2024-annual-report/); [FY25](https://www.nptrust.org/annual-reports/npt-annual-report/); [corporate DAF article](https://www.nptrust.org/philanthropic-resources/philanthropist/five-ways-a-corporate-donor-advised-fund-can-help-clients-meet-their-csr-goals/) (2023) | 2023–2026 | NPT split status | F |
| S6 | [RPA Remitly article](https://www.rockpa.org/centering-community-to-advance-financial-health-insights-from-the-remitly-foundations-philanthropic-journey/); RPA sitemap (`https://www.rockpa.org/sitemap_index.xml`) | 2026-01-12 | CD12 check | F |
| S7 | SVCF audited FS: [FY2022](https://www.svcf.org/assets/img/heroA/svcf-financial-statement-audit-2022.pdf), [FY2023](https://www.svcf.org/assets/img/heroA/svcf-financial-statement-audit-2023.pdf), [FY2024](https://www.svcf.org/assets/img/heroA/svcf-financial-statement-audit-2024.pdf), [FY2025](https://www.svcf.org/assets/files/publications/SVCF-CFS-FY25_Updated-Financials.pdf) | 2023–2026 | SV rows | F |
| S8 | SVCF pages: [corporate advised fund](https://www.svcf.org/donors/charitable-giving-options/corporate-advised-fund); [fund types](https://www.svcf.org/advisors/fund-types); [NVIDIA](https://www.svcf.org/nvidia); [DoorDash](https://www.svcf.org/annual-reports/donor-2025/donor-stories-2025-26-doordash); [eBay](https://www.svcf.org/annual-reports/donor/donor-stories-ebay); [by the numbers 2023](https://www.svcf.org/annual-reports/2023/by-the-numbers) | 2022–2025 | fees, CN01–02, CD33 | F |
| S9 | Fidelity Charitable [2025 Giving Report](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf); [2026 Giving Report](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf) | 2025–2026 | FC rows | F |
| S10 | [GKCCF corporate giving](https://www.growyourgiving.org/corporate-giving/); [corporate foundation](https://www.growyourgiving.org/corporate-giving/corporate-foundation/) | live 2026-11-19 | "hundreds of companies" | F |
| S11 | [NYCT financials page](https://thenytrust.org/about/financials-annual-reports/); [2025 financials](https://thenytrust.org/wp-content/uploads/2026/07/2025-New-York-Community-Trust-Financials.pdf); [2025 annual report](https://thenytrust.org/wp-content/uploads/2026/07/NYCT_AnnualReport2025_Digital.pdf); [corporations page](https://thenytrust.org/foundations-corporations-family-offices/) | 2026 | NYCT split status | F |
| S12 | [TBF financial information](https://www.tbf.org/who-we-are/financial-information); [FY25 audited](https://www.tbf.org/-/media/tbf/files/financial-information/financial-statements/tbf-fy25-audited-financials.pdf); [FY23 audited](https://www.tbf.org/-/media/tbf/files/financial-information/financial-statements/tbf-fy23-audited-financial-statements.pdf); [company giving](https://www.tbf.org/donors/company-giving) | 2023–2025 | TBF split status; CN03–04 | F |
| S13 | [FFTC financials](https://www.fftc.org/foundation-financials); [CY2025 audited FS](https://www.fftc.org/sites/default/files/2026-10/Foundation_for_the_Carolinas12-31-25_Audit_FS_Client2.pdf); [FAQ](https://www.fftc.org/faqs) | 2026 | FFTC split status | F |
| S14 | [CFGA financial information](https://cfgreateratlanta.org/financial-information/); [CY2024 consolidated financial report](https://cfgreateratlanta.org/wp-content/uploads/2025/11/The-Community-Foundation-for-Greater-Atlanta-Inc.-2024-Consolidated-Financial-Report.pdf) | 2025 | Atlanta split status | F |
| S15 | [AOGF 990 FYE 2026-03](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202642259349301349_public.xml) (cached XML, re-parsed) | filed 2026 | SE03 upper bound | X |
| S16 | Repo: `daf-sponsor-league-table-fy2021-2025.csv` (sponsor selection, FY2024 convention); `form990-returns-schedule-d-harvest-full.csv` (cross-check; Fidelity FYE 2025-06 Sch D); `corporate-daf-programs-2021-2026.csv` (CD and SA rows) | 2026-11 | selection, checks | R |
