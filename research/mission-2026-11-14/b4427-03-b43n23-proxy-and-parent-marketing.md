# P-B4427-03 and P-B43N23-01: retiring the 990 balance-sheet proxy (ΔR1); who pays for marketing at affiliated nationals

**Date:** 2026-11-19. **Task ID:** b4427-03-b43n23.

**Outputs**
- [`proxy-reconciliation-parent-marketing-2026-11-19.csv`](../../data/mission-2026-11-14/proxy-reconciliation-parent-marketing-2026-11-19.csv): 569 rows in long format. Part A has 117 rows (5 sponsors × FY2023–2024). Part B has 452 rows (8 filers × 4 returns, plus audit rows). The data dictionary is in §6.
- Script: [`scripts/mission_proxy_reconciliation.py`](../../scripts/mission_proxy_reconciliation.py). Stdlib only, functional. Run it as `python3 scripts/mission_proxy_reconciliation.py . --xml-dir <e-file XML dir> --audit-text-dir <pdftotext dir> [--audit-text-dir <second dir>]`. Two runs gave byte-identical CSVs. Every audit figure and quote is checked against the pdftotext output, and every check passed (`unverified/mismatch rows: 0`).
- Queue proposals: [`queue-proposals-b4427-03-b43n23.csv`](../../data/mission-2026-11-14/queue-proposals-b4427-03-b43n23.csv) (6 rows).

**Inputs read first**
- [b4014-b4427-sponsor-economics.md](b4014-b4427-sponsor-economics.md) and its CSV `sponsor-fee-revenue-margin-2026-11-19.csv`.
- The wave-38B corrections ([validation-wave38b-report.md](validation-wave38b-report.md), V38B-24…31). They are already applied in both docs.
- [direction-sponsor-financial-resilience.md](direction-sponsor-financial-resilience.md), including its 38B-corrected lines (§0 item 6, §1.5, §6).
- [direction-sponsor-marketing-spend.md](direction-sponsor-marketing-spend.md) §1 item 5 and §5. This is the source of the "parent may pay marketing" hypothesis that Part B tests.

**Evidence tags:** [F] read from a filing or audited statement; [C] computed by the script; [I] inference.

**Conventions:** FY is the year in which the fiscal period ends. TY is the IRS tax year (the year the period begins). R1 = Part X line 32 − Schedule D Part I line 4 column (a), and ΔR1 = R1(t) − R1(t−1), exactly as in the resilience study. The script's ΔR1 matches the resilience CSV to the dollar in all 10 sponsor-years.

---

## 1. Headlines

1. **ΔR1 should be retired as an operating-margin proxy [C].** It is not a margin at any of the five sponsors where an audited fee figure exists. At every one of them, an identifiable balance-sheet item explains it, and the audited fee surplus cannot be found in it:

   | Sponsor | What ΔR1 actually is |
   |---|---|
   | Fidelity | 100% growth of Schedule D column (b) "other funds" (both years) |
   | JCF | 104% and 96% growth of the board-designated endowment, which *is* column (b) |
   | CJP | 106% endowment returns less PP&E in FY2023. In FY2024, 34% endowment returns less PP&E, and most of the rest is the Israel Emergency Fund campaign ($56.0m of receipts) |
   | RCF | 0% from any of the four named items. It is entirely the gap between Schedule D DAF value, total assets and liabilities |
   | NCF | Funds that the audit counts as donor-advised or charitable but that sit outside Schedule D columns (a) and (b): +$112.2m in 2024 |

2. **The one "close match" (JCF) is a coincidence [C/F].**
   - JCF's R1 equals its audited "functioning as endowment" fund ($21,302,379 and $24,202,416) plus its audited "reserve fund" ($2,558,752 and $2,681,442), to the dollar.
   - The operating fund that receives the fee sits inside "Undesignated – available for operations". That line plus "designated and semi-designated" equals the Schedule D DAF value to the dollar in both years.
   - So JCF's fee surplus is reported inside column (a) and never reaches R1.

3. **At Fidelity no fee surplus can reach R1 [F/C].**
   - Fidelity pays FMR an amount "equal to the administrative fee the Gift Fund charged its donors" (Note 7, FY2022–FY2025).
   - R1 minus column (b) is $0 in every year.
   - Part IX line 11a equals the audited administrative fee to the dollar in all four years: $124,608,555, $121,190,522, $139,686,600 and $179,875,837.

4. **NCF's own operating fund fell while ΔR1 rose [F/C].** In 2024 the NCCF column's audited "Operating" net assets went from $29,463k to $24,666k (−$4.80m), while ΔR1 was +$105.8m. The identity closes to within rounding: −$4.80m operating, +$0.07m restricted, +$0.00m annuity reserve, +$112.21m funds beyond Schedule D (a)+(b), and −$1.70m column (b) give +$105.78m.

5. **Error if ΔR1 is read as the fee surplus [C]:**

   | Sponsor | FY2023 | FY2024 |
   |---|---|---|
   | Fidelity | +$47.6m | +$70.7m |
   | RCF | +$6.3m | +$57.0m |
   | NCF, against the 38B-corrected NCCF fee less 990 operating cost | +$89.6m | +$139.1m |
   | JCF, against the post-UJA surplus | +$1.6m | +$1.2m |
   | CJP | not computable | not computable |

6. **The administrator fee (Part IX line 11a) means different things at different sponsors [F]:**
   - **Fidelity:** the whole donor fee, paid to FMR.
   - **Raymond James:** part of the Raymond James Trust N.A. (RJTNA) payment ($5.7–9.8m on line 11a; $9.3–14.5m on Schedule L).
   - **DAFgiving360 and Vanguard:** small amounts ($0.5–2.8m).
   - **GS, MS and BofA:** zero or blank. Their administrators are paid on line 11g (Morgan Stanley's RenPSG) or "other expenses" (GS's "Agency fee" of $7.1–8.5m), or not at all (BofA, whose corporate trustee shows no admin line).

7. **Who pays for marketing, from filed text [F]:**

   | Sponsor | Filed position |
   |---|---|
   | Fidelity | Schedule O lists **fundraising** among the services FMR provides under the services agreement. Payments are "in aggregate", and costs FMR bears "are not separately stated". Its marketing is therefore bought inside the fee, at an undisclosed amount |
   | Raymond James | Schedule O lists **fundraising**, occupancy and officers under the RJTNA service agreement. Part of line 11a is booked in the fundraising column ($0.17–0.29m) |
   | DAFgiving360 | The charity books its own advertising on line 12 ($2.65m → $6.88m, 100% fundraising column), and its workforce are Schwab employees reimbursed by the charity |
   | Vanguard | The charity books its own fundraising expense (audit: $3.83m in FY2024 and $4.09m in FY2025). It also receives in-kind professional services from Vanguard ($0.79m and $1.00m) and has an undrawn interest-free facility of up to $6.5m |
   | Goldman Sachs (both funds), Morgan Stanley GIFT, BofA | **Not disclosed.** No Schedule O, R or L text addresses marketing, and no statement is posted |

8. **No parent pays charity marketing on the record [F/I].** None of the eight filers states that the parent bears brand or adviser marketing for the charity. Where the filing speaks, the charity pays: through the fee (Fidelity, Raymond James), by reimbursement (Schwab staff), or on its own lines (Schwab and Vanguard advertising and fundraising). Brand-level advertising that the parent runs for its own business is outside every filing read.

---

## 2. Part A: decomposition of ΔR1 (P-B4427-03)

### 2.1 Method
- **Sponsor-years.** Fidelity, RCF, NCF, JCF and CJP, FY2023 and FY2024. These are the five sponsors whose audits disclose the internal DAF fee (b4014-b4427 §3.2). ΔR1 uses each year's own return and the prior year's return, with the object IDs in the CSV.
- **Sequential decomposition [C].** All terms except c4 are read from the e-file XML.
  - **c1:** the change in Schedule D Part I column (b) EOY value ("funds and other accounts").
  - **c2:** Schedule D Part V current-year endowment investment earnings (line 1c). This is counted only when the Part V endowment is not itself the column (b) fund. At JCF the EOY balances are equal, so c2 = 0 there and the earnings appear as a memo row.
  - **c3:** the change in Part X line 10c net PP&E.
  - **c4:** the audited fee surplus, applying the wave-38B corrections:
    - Fidelity and RCF: fee − opex;
    - JCF: fee − opex − the $2.0m operating-fund grant to UJA, the like-for-like post-grant figure;
    - NCF: NCCF-column fee − NCCF's own 990 operating cost;
    - CJP: not computable (0, flagged).
  - **Residual** = ΔR1 − (c1 + c2 + c3 + c4).
- **Audit anchors [F/C].** These locate the residual using each audit's own classes of net assets. Every anchor is checked with its label and numbers on one line of the pdftotext output.
  - RCF: total assets and liabilities.
  - NCF: the consolidating statement, NCCF column, "Operating", "Donor-advised or charitable funds", restricted net assets and annuity reserves.
  - JCF: reserve fund, endowment, undesignated, and designated or semi-designated.
  - CJP: the consolidating schedule of activities by functional area.

### 2.2 Results [C; $m]

| Sponsor | FY | ΔR1 | c1 col (b) | c2 endowment returns | c3 PP&E | c4 audited fee surplus | Residual | Where the residual sits (audit anchor) |
|---|---|---|---|---|---|---|---|---|
| Fidelity | 2023 | +36.32 | +36.32 | 0 | 0 | −11.29 | +11.29 | R1 − col (b) = 0 both years. The fee deficit is not borne by R1 (no own funds) |
| Fidelity | 2024 | +48.78 | +48.78 | 0 | 0 | −21.89 | +21.89 | same |
| RCF | 2023 | +6.57 | 0 | 0 | 0 | +0.28 | +6.29 | −Δliabilities −22.60; Δ(total assets − Schedule D DAF value) +29.16 |
| RCF | 2024 | +57.19 | 0 | 0 | 0 | +0.15 | +57.04 | −Δliabilities +18.81; Δ(total assets − Schedule D DAF value) +38.38. At end-2024 the Schedule D DAF value equals total assets ($5,913,566,776) |
| NCF | 2023 | +59.82 | −72.76 | 0 | +4.30 | −29.82 | +158.10 | NCCF operating net assets $29.46m at EOY. The FY2022 split is not in the statements read |
| NCF | 2024 | +105.78 | −1.70 | 0 | −0.71 | −33.37 | +141.56 | NCCF operating −4.80; restricted +0.07; annuity reserves +0.00; funds beyond Schedule D (a)+(b) +112.21 |
| JCF | 2023 | +1.80 | +1.87 | 0 (memo: 3.39 inside c1) | −0.06 | +0.24 | −0.25 | R1 − col (b) = audit reserve fund ($2,558,752). Schedule D DAF value = undesignated + designated (exact) |
| JCF | 2024 | +3.02 | +2.90 | 0 (memo: 4.51 inside c1) | 0 | +1.85 | −1.72 | R1 − col (b) = audit reserve fund ($2,681,442), exact |
| CJP | 2023 | +15.64 | 0 | +18.00 | −1.37 | n/a | −0.99 | Audit non-DAF areas +20.09: operations +1.85, endowment and reserves +18.16, JCEP +0.08 |
| CJP | 2024 | +75.81 | 0 | +26.71 | −0.72 | n/a | +49.82 | Audit non-DAF areas +74.77: operations +47.10, of which Israel Emergency Fund receipts 56.00; endowment and reserves +27.41 |

**Share of ΔR1 explained by c1 + c2 + c3 (non-fee balance-sheet items) [C]**

| Sponsor | FY2023 | FY2024 |
|---|---|---|
| Fidelity | 100% | 100% |
| JCF | 101% | 96% |
| CJP | 106% | 34% |
| RCF | 0% | 0% |
| NCF | not meaningful (column (b) fell while ΔR1 rose) | not meaningful |

### 2.3 Reading [I]
- **ΔR1 is a "where did the non-DAF money go" measure, not "what did operations earn".**
  - At Fidelity and JCF it is pure column (b) movement.
  - At CJP it is federation endowment and campaign money.
  - At RCF and NCF it is the difference between two independently reported very large numbers (Part X net assets and the Schedule D DAF value), which moves with reporting basis. RCF's Schedule D DAF value equals total assets in 2024 but exceeds them by $38.4m in 2023. NCF's audit carries $62.1m (2023) and $174.3m (2024) of donor-advised or charitable funds beyond Schedule D columns (a) and (b).
- **The fee surplus, where it exists, is booked inside a fund the 990 does not separate from DAFs or other funds.**
  - At JCF it sits in the undesignated (column (a)) balance.
  - At RCF it is undifferentiated within net assets without donor restrictions.
  - At NCF it sits in the NCCF "Operating" class, which the 990 merges into R1, but there it is swamped by fund-basis movements more than 20× larger.
  - At Fidelity there is no surplus to retain.
- **Verdict.** Retire ΔR1 as an operating-margin or fee-reliance proxy everywhere in the repo. Keep it only as a descriptive "change in non-DAF net assets".
- **What to use instead.** There is no 990 substitute. An operating result has to come from audits that report an own operating fund:
  - NCF: the NCCF "Operating" class;
  - CJP: the "CJP Operations" area, which is federation-wide;
  - RCF: fee − opex;
  - Fidelity: by contract, zero.
  - Group medians of ΔR1 ÷ operating cost (resilience §0 item 6, §7) should be labelled balance-sheet movement only.

---

## 3. Part B: marketing at affiliated-commercial nationals (P-B43N23-01)

### 3.1 Method
- **Filers.** Eight filers stand for seven brands. Goldman Sachs has two: GS DAF (GS Donor Advised Philanthropy Fund, 31-1774905) and the Goldman Sachs Charitable Gift Fund (11-3813663).
- **Returns.** The TY2021–2024 returns selected by the resilience study. These are FY2022–FY2025 (June, March and December year-ends).
- **Fields extracted from the XML [F]:**
  - Part IX lines 11a, 11f, 11g and 12, by functional column;
  - "Other expense" lines whose description mentions admin, agency, commission, market, advert, promot or fundrais;
  - Part VII Section B contractors and Schedule L business transactions naming the parent or administrator;
  - Schedule O passages about the services agreement, the workforce, the corporate trustee, board ties or marketing;
  - whether Schedule R names a parent-group company (charities excluded), or lists a Part V transaction with one.
- **Audited statements.**
  - Read where they are posted and robots-allowed: Fidelity FY2022–FY2025 (three PDFs) and Vanguard FY2024–FY2025.
  - Each related-party quote is verified verbatim.
  - The whole text is searched for marketing, advertis, promotion and brand: 0 hits in all four statements.
- **Robots.txt.** It was checked first for every fetch (§5.2). No logins, forms or outreach.

### 3.2 Results by sponsor [F unless marked]

| Sponsor (FY) | Line 11a: amount and what it covers | Parent or administrator payments | Line 12 advertising | Marketing: filed statement | Audit |
|---|---|---|---|---|---|
| **Fidelity** (FY6/22–25) | $124.6m, $121.2m, $139.7m, $179.9m, all in the program column. Equals the audited "Administrative fees" paid to FMR each year [C] | FMR LLC "ADMIN & INV MGMT SVC" $121.6m–$159.9m (Part VII B) | $0 | Schedule O: FMR provides "RECORD-KEEPING, SYSTEMS, ADMINISTRATION, FUNDRAISING, INVESTMENT ADVISORY SERVICES AND SERVICES OF OFFICERS…"; "SEPARATE COSTS BORNE BY FMR IN PROVIDING SERVICES UNDER THE SA… ARE NOT SEPARATELY STATED." Fundraising is **recharged inside the fee**; the amount is not disclosed. Schedule R lists a disregarded "02210 LLC" whose activity is "FUNDRAISING", with $0 income and assets in all four years | Note 7: paid FMR "at amounts equal to the administrative fee the Gift Fund charged its donors" (FY2025: "net of any tier price credits"). No marketing term |
| **DAFgiving360** (FY6/22–25) | $1.04m → $2.76m, of which fundraising column $0.12–0.39m. Payee not named | Charles Schwab & Co "BROKERAGE & ADMIN SERVICES": Part VII B $5.0–9.8m; Schedule L $6.9–11.4m. "ADMINISTRATIVE FEE EXP" $6.3–10.9m on other expenses | **$2.65m → $6.88m, 100% fundraising column** | Schedule O: "THE WORKFORCE… ARE EMPLOYEES OF CHARLES SCHWAB & CO. … PAYROLL… FULFILLED BY CHARLES SCHWAB & CO. AND REIMBURSED BY" the charity. Advertising is **borne by the charity**. Parent brand marketing is not disclosed | Blocked (HTTP 403) |
| **Vanguard** (FY6/22–25) | $0.54–1.74m, of which fundraising column $0.33–0.43m | The Vanguard Group "OCCUPANCY/ADMIN. SVCS." on Schedule L: $3.07m, $3.64m, $3.92m, $4.01m. The FY2024–25 figures equal the audit's related-party fees | $0.28–0.39m, half in the fundraising column | Schedule O: none on marketing. Audit: fundraising expenses $3,833,010 (FY2024) and $4,091,664 (FY2025), **borne by the charity**. In-kind professional services from Vanguard: $788,129 and $1,000,342. Interest-free facility of up to $6.5m, undrawn | Read FY2024–25. No marketing term |
| **GS DAF** (CY2021–24) | $0 | Ayco "ADMIN/INVST ADVISORY" $0.89m (2021) and "ADMIN. SERVICES" $3.23m (2023) and $1.03m (2024). GS Trust Co and GS & Co investment, advisory and tech: $11.6–14.6m and $3.9–8.1m. "AGENCY FEE" $7.1–8.5m (payee not named) | $0 | **Not disclosed** | Not posted |
| **GS Charitable Gift Fund** (FY6/22–25) | blank | CAF America "GRANT ADMINISTRATION" $0.22–0.88m | blank | Schedule O: "DOES NOT HAVE ANY EMPLOYEES". Marketing **not disclosed**. Schedule R names The Goldman Sachs Group Inc only as controller of the GS Foundation | Not posted |
| **Morgan Stanley GIFT** (CY2021–24) | blank | RenPSG "ADMIN & LEGAL" $9.8–14.9m (line 11g). Morgan Stanley "INVESTMENT ADVISOR" $2.7–4.2m (line 11f). "FA commissions and misc." $2.81m, $1.92m, $2.03m (TY2022–24) | blank | Schedule O: "3 [later 4] BOARD MEMBERS ARE SENIOR EXECUTIVES AT MORGAN STANLEY." Marketing **not disclosed**. The "FA commissions" line is the only adviser-related cost on the return; its payee and basis are not stated | Not posted |
| **BofA Charitable Gift Fund** (CY2021–24) | blank | No admin or administrator line. Line 11f $17.7–24.1m. "BANK OF AMERICA, TRUSTEE" (Part VII) | blank | Schedule O: "TRUST HAS CORPORATE TRUSTEE". Marketing **not disclosed** | Not posted. Schedule O says audited statements are filed with the Massachusetts Attorney General |
| **Raymond James** (FY3/22–25) | $9.26m, $9.79m, $5.70m, $7.10m, of which fundraising column $0.19m, $0.29m, $0.17m, $0.21m | Raymond James Trust N.A. "ADMIN SVC & INV MGMT": Schedule L $9.26m, $9.79m, $11.45m, $14.50m. From FY3/24, part of it moves to line 11f ($6.28m and $8.33m) | $0 | Schedule O: RJTNA services include "ADMINISTRATIVE AND INVESTMENT ADVISORY SERVICES, RECORD-KEEPING, ACCOUNTING SERVICES, FUNDRAISING, SYSTEMS, OCCUPANCY AND EQUIPMENT, AND SERVICES OF OFFICERS". Fundraising is **recharged under the service agreement** | Blocked (robots.txt unreachable) |

- **Schedule R.** No filer lists its parent firm as a related organization, and none lists a Schedule R Part V transaction with it.
- **Schedule L.** This is where the parent appears, as an "interested person" business transaction, at Schwab, Vanguard and Raymond James. At Fidelity the parent appears in Part VII Section B.

### 3.3 Reading [I]
- **The hypothesis in the marketing direction (§5) is half right.**
  - Parents do supply the operating machinery.
  - The filings that speak say the charity pays for it, fundraising included. At Fidelity and Raymond James the payment is through the administrator fee. At Schwab it is by reimbursing parent-employed staff and buying its own advertising.
  - What remains invisible is the parent's *own-account* brand and adviser marketing, such as Fidelity Investments or Schwab advertising that features the DAF, or adviser incentives. No filing or audit read here quantifies it.
- **Morgan Stanley's "FA commissions" is the only line that may be adviser compensation borne by a charity.** It is $1.9–2.8m a year. The payee is not named, so this is not established (proposal P-B43N23-04).
- **For an entrant's cost comparison:**
  - Fidelity's whole fee ($121–180m) is the price of a bundle that includes fundraising.
  - Schwab's line 12 ($6.9m in FY2025) is a floor on the charity-borne marketing cost, not a ceiling. Staff marketing time is in reimbursed salaries.
  - For GS, MS and BofA nothing is known beyond $0 on line 12.

---

## 4. Limits
- **Five sponsors and two years in Part A.** The NCF FY2023 audit anchor is incomplete: the FY2022 NCCF operating figure needs the NCF 2023 statements, which were not read.
- **CJP has no fee surplus.** Its fee ($1.58m and $1.64m) is an interfund charge inside federation operations.
- **c4 definitions follow wave 38B.**
  - For NCF, c4 mixes an audited fee with a 990 cost, because the NCCF-column G&A includes fees paid between group entities.
  - Using the NCCF column's own G&A plus fund-raising instead (−$69.5m and −$76.8m) would only enlarge the residual.
- **The column (b) and Part V overlap test is an equality test on EOY balances.** It fires only at JCF. At CJP the Part V endowment is not in column (b), which is blank.
- **Part B audits:**
  - Only Fidelity and Vanguard statements could be read.
  - DAFgiving360 returned 403 and Raymond James' robots.txt was unreachable; neither was bypassed.
  - GS, MS and BofA do not post statements.
  - Vanguard FY2022–FY2023 statements were not found (guessed paths returned 404).
  - A FY2026 Vanguard statement was fetched (the about-us page links it). It repeats the same related-party wording, but its FY2026 figures are outside scope and are not used.
- **Schedule O keyword screen.** It could miss marketing language phrased otherwise. As a check, every Schedule O entry of all eight Morgan Stanley and BofA returns was read in full, and a wider keyword screen (agreement, fee, employ, reimburs, fundrais) was read for the latest return of every other filer; neither found further marketing language.
- **Massachusetts Attorney General filings (BofA) were not consulted.** The public-charity search is a form interface, which the rules exclude.

## 5. Source register and access log

### 5.1 Sources
| ID | Source | Used in |
|---|---|---|
| S1 | Form 990 e-file XML, GivingTuesday mirror `https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{object_id}_public.xml`. Part A: 202441369349301334, 202521349349310887, 202430459349302913 (Fidelity); 202443109349303629, 202543189349301959, 202303149349303205 (RCF); 202443169349306424, 202513109349303201, 202323179349311657 (NCF); 202410969349301036, 202500369349300210, 202330479349300013 (JCF); 202421289349303727, 202541259349302634, 202321319349304847 (CJP). Part B: the 32 object IDs in the CSV | §2, §3 |
| S2 | Fidelity Charitable audited statements: FY2023/2022 https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2023-2022.pdf ; FY2024/2023 …/audited-financial-statements-2024-2023.pdf ; FY2025/2024 …/audited-financial-statements-2025-2024.pdf | §2, §3 |
| S3 | RCF 2024 audited statements (2023 comparative): https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf | §2 |
| S4 | NCF 2024 consolidated statements with consolidating schedules: https://site.ncfgiving.com/wp-content/uploads/2026/07/NCF-24-Consolidated-FS-Final.pdf | §2 |
| S5 | JCF FY2024 statements (FY2023 comparative): https://jcfny.org/app/uploads/2025/07/JCF-FINAL-FS-FY2024.pdf | §2 |
| S6 | CJP audited statements 2023–2024: https://www.cjp.org/hubfs/Financial%20Statements/2024/Audited%20Financial%20Statements%202023%E2%80%932024.pdf ; 2022–2023: https://www.cjp.org/hubfs/Financial%20Statements/2023/Audited%20Financial%20Statements%202022%E2%80%932023.pdf | §2 |
| S7 | Vanguard Charitable FY2025/2024 statements: https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf (FY2026 file, wording check only: https://www.vanguardcharitable.org/sites/default/files/2026-11/VCEP_Financial_Statements_2026.pdf) | §3 |
| S8 | Repo: `sponsor-fee-revenue-margin-2026-11-19.csv` (fee, opex, UJA grant, NCCF 990 operating cost); `sponsor-financial-resilience-2021-2024.csv` (ΔR1 cross-check) | §2 |
| S9 | Repo: [validation-wave38b-report.md](validation-wave38b-report.md) (c4 definitions) | §2 |

### 5.2 robots.txt and fetch log (2026-11-19, agent `research-script/1.0`)
| Host | robots.txt | Result |
|---|---|---|
| gt990datalake-rawdata.s3.amazonaws.com | 404 (no rules) | XML reused from the b4014-b4427 cache; nothing new fetched |
| www.fidelitycharitable.org | 200, allowed | FY2023/2022 PDF fetched (200); FY2022/2021 path 404; the other two PDFs from the cache |
| www.vanguardcharitable.org | 200, allowed | /about-us (200); FY2026 PDF (200); two guessed FY2023/FY2024 paths 404 |
| www.schwabcharitable.org | 403 | page 403; not bypassed (www.dafgiving360.org was 403 in b4014-b4427) |
| www.raymondjames.com | unreachable (treated as disallow) | nothing fetched (raymondjamescharitable.com and rjcef.com were unreachable in b4014-b4427) |
| www.bankofamerica.com | 200, allowed | home page only; no charitable-fund statements linked |
| RCF, NCF, JCF, CJP hosts | 200, allowed (b4014-b4427 §4.2) | cached PDFs reused |

sec.gov, crt.sh, certspotter and ProPublica were not used.

## 6. Data dictionary: `proxy-reconciliation-parent-marketing-2026-11-19.csv`

The file is in long format, with one row per sponsor × year × item.

| Column | Meaning |
|---|---|
| part | `A` = ΔR1 decomposition (P-B4427-03); `B` = parent marketing (P-B43N23-01) |
| sponsor, ein | Filer |
| fiscal_year | Part A: FY (year the period ends). Part B: period end as YYYY-MM (blank on sponsor-level audit rows) |
| tax_year_990, object_id_990 | The return used |
| item | See the lists below |
| value_usd | USD, or a ratio for `share_*` items (4 dp), or `true`/`false` for flags |
| value_text | Verbatim text: contractor or Schedule L name and description, Schedule O passage (first 900 characters), audit quote, or other-expense description |
| evidence | F, C, F/C |
| source_ref | Mirror URL of the return, audit document stem or URL, or repo CSV |
| note | Basis, verification flags (`verified=true`, `equal=true`) and the prior-year object ID |

**Part A items**
- `delta_r1`
- `c1_other_funds_growth_sched_d_col_b`
- `c2_endowment_returns_outside_col_b`
- `c2_memo_endowment_returns_inside_col_b`
- `c3_ppe_change`
- `c4_audit_fee_surplus`
- `residual_after_c1_to_c4`
- `share_of_delta_r1_from_c1_c2_c3`
- `delta_r1_less_fee_surplus`
- `anchor_*`: audit locations of the residual
  - Fidelity: `anchor_r1_minus_col_b_eoy`
  - RCF: `anchor_minus_change_in_total_liabilities`, `anchor_change_in_total_assets_less_sched_d_daf_value`
  - NCF: `anchor_nccf_audit_operating_net_assets_eoy`, `_change`, `anchor_nccf_funds_beyond_sched_d_col_a_and_b_eoy`, `_change`, `anchor_nccf_net_assets_with_restrictions_change`, `anchor_nccf_annuity_reserves_change`
  - JCF: `anchor_r1_minus_col_b_equals_audit_reserve_fund`, `anchor_col_b_equals_audit_endowment`, `anchor_sched_d_daf_value_equals_undesignated_plus_designated`
  - CJP: `anchor_audit_non_daf_areas_change`, `anchor_audit_cjp_operations_change`, `anchor_audit_israel_emergency_fund_receipts`

**Part B items**
- `audit_status`
- `audit_related_party_quote`
- `audit_marketing_term_count`
- `part_ix_11a_management_fees_total` (column split in note)
- `part_ix_11a_fundraising_column`
- `part_ix_12_advertising_total`
- `part_ix_11g_other_fees_total`
- `part_ix_11f_investment_mgmt_fees_total`
- `part_vii_b_contractor_parent_or_administrator`
- `schedule_l_business_transaction_parent`
- `part_ix_24_other_expense_line`
- `schedule_o_passage`
- `schedule_o_services_agreement_includes_fundraising`
- `schedule_o_mentions_marketing_advertising_brand`
- `schedule_r_filed`
- `schedule_r_names_parent_company`
- `schedule_r_part_v_transaction_with_parent_company`
- `check_11a_equals_audited_fee_paid_to_fmr` (Fidelity, FY2022–25)

---

## Exact corrections

Each Find occurs exactly once in its file as of 2026-11-19. They were checked with `grep -c` after the wave-38B edits.

### `research/mission-2026-11-14/direction-sponsor-financial-resilience.md`

- **Find:** "Fee reliance therefore has to be inferred from the balance sheet (item 6) or read from audited statements (P-B44N27-02)."
- **Replace with:** "Fee reliance cannot be inferred from the balance sheet: at the five sponsors with audited fee data the fee surplus is not identifiable in ΔR1 (item 6). It has to be read from audited statements (P-B44N27-02; [b4427-03-b43n23-proxy-and-parent-marketing.md](b4427-03-b43n23-proxy-and-parent-marketing.md)). [b4427-03]"

- **Find:** "6. **Operating surplus: the 990 headline is uninformative. The change in non-DAF net assets is a better balance-sheet signal, but audits show it is not an operating margin [C].** [V wave 38B]"
- **Replace with:** "6. **Operating surplus: the 990 headline is uninformative, and the change in non-DAF net assets (ΔR1) is a balance-sheet movement, not an operating signal. At the five sponsors with audited fee data it follows Schedule D other-fund growth, endowment returns, campaign receipts and Schedule D reporting basis; the fee surplus is identifiable in it at none [C].** [V wave 38B] [b4427-03]"

- **Find:** "| **ΔR1** | R1(TY) − R1(TY−1). The sponsor's own balance-sheet surplus, including fees moved from DAF accounts and returns on its own funds |"
- **Replace with:** "| **ΔR1** | R1(TY) − R1(TY−1). Change in non-DAF net assets: Schedule D column (b) funds, endowment returns, PP&E, donor-restricted and campaign funds, and any gap between the Schedule D DAF value and the balance sheet. Not an operating result [b4427-03]"

- **Find:** "Only at JCF is it within about $1.6m. Treat ΔR1 as a non-DAF balance-sheet movement, not an operating result. [V wave 38B]"
- **Replace with:** "Only at JCF is it within about $1.6m, and that is coincidence: JCF’s R1 is its board-designated endowment plus its reserve fund, while the operating fund that receives the fee is reported inside the Schedule D DAF value. Treat ΔR1 as a non-DAF balance-sheet movement, not an operating result. [V wave 38B] [b4427-03]"

- **Find:** "Its balance-sheet trace is ΔR1."
- **Replace with:** "It has no reliable balance-sheet trace: the fee surplus is not identifiable in ΔR1 at any of the five sponsors with audited fee data. [b4427-03]"

- **Find:** "  - Affiliated-commercial sponsors' staff, technology and marketing are paid by the parent under services agreements (compensation direction §5; cost-structure §8)."
- **Replace with:** "  - Affiliated-commercial sponsors buy staff, technology and fundraising from the parent under services agreements (compensation direction §5; cost-structure §8), and the filings that speak show the charity paying: Fidelity’s payment to FMR equals its fee and covers fundraising, Raymond James’s service agreement covers fundraising, DAFgiving360 reimburses Schwab for its workforce and books its own advertising, and Vanguard Charitable books its own fundraising expense while receiving $0.8–1.0m a year of in-kind professional services from Vanguard. Brand marketing the parent bears on its own account is not disclosed. [b4427-03]"

### `research/mission-2026-11-14/b4014-b4427-sponsor-economics.md`

- **Find:** "Because the UJA grant leaves the operating fund, the like-for-like figure is the post-grant surplus, which ΔR1 exceeds by $1.56m and $1.18m [C]. [V wave 38B]"
- **Replace with:** "Because the UJA grant leaves the operating fund, the like-for-like figure is the post-grant surplus, which ΔR1 exceeds by $1.56m and $1.18m [C]. [V wave 38B] The match is coincidental: JCF’s R1 equals its board-designated endowment (Schedule D column (b)) plus its reserve fund to the dollar, and the operating fund that receives the fee is reported inside the Schedule D DAF value. Endowment growth ($1.87m and $2.90m) is 104% and 96% of ΔR1 [C]. [b4427-03]"

- **Find:** "The audits show it mostly measures other-fund and endowment movements [I]."
- **Replace with:** "The audits show it mostly measures other-fund and endowment movements; the b4427-03 decomposition confirms this at Fidelity and JCF and finds Schedule D reporting-basis gaps at RCF and NCF and campaign receipts at CJP [C]. [b4427-03]"

- **Find:** "| JCF | −$0.4m | −$0.8m | Close: the operating fund is most of R1's movement |"
- **Replace with:** "| JCF | −$0.4m | −$0.8m | Close by coincidence: R1 is the board-designated endowment (Schedule D column (b)) plus the reserve fund, and the operating fund sits inside the Schedule D DAF value, so ΔR1 is endowment growth [C] [b4427-03]"

- **Find:** "(R1 is negative throughout), not by operations |"
- **Replace with:** "(R1 is negative throughout), not by operations. R1 = (total assets − Schedule D DAF value) − liabilities; at end-2024 the Schedule D DAF value equals total assets to the dollar, so R1 equals minus liabilities [C] [b4427-03]"

- **Find:** "and annuity reserves |"
- **Replace with:** "and annuity reserves. In 2024 NCCF’s audited operating net assets fell $4.8m while ΔR1 rose $105.8m; $110.5m of the rise is funds the audit counts as donor-advised or charitable beyond the Schedule D DAF value [C] [b4427-03]"

- **Find:** "without the decomposition in proposal P-B4427-03."
- **Replace with:** "at all: the decomposition in [b4427-03-b43n23-proxy-and-parent-marketing.md](b4427-03-b43n23-proxy-and-parent-marketing.md) finds the audited fee surplus identifiable in ΔR1 at none of the five sponsors. [b4427-03]"

### `research/mission-2026-11-14/direction-sponsor-marketing-spend.md`

- **Find:** "or recover it through administrator fees (line 11a; Fidelity $121–180m a year) or fund expense ratios."
- **Replace with:** "or recover it through administrator fees (line 11a; Fidelity $121–180m a year) or fund expense ratios. Filings settle part of this: Fidelity’s and Raymond James’s Schedule O list fundraising among the services bought from the parent under the services agreement, so that marketing is paid for from the administrator fee; DAFgiving360’s own advertising is on line 12 and its workforce is reimbursed to Schwab; Vanguard Charitable books its own fundraising and receives in-kind professional services from Vanguard; Goldman Sachs, Morgan Stanley and BofA file nothing on who pays ([b4427-03-b43n23-proxy-and-parent-marketing.md](b4427-03-b43n23-proxy-and-parent-marketing.md)). [b4427-03]"

### `research/mission-2026-11-14/FINAL-STATUS.md`

- **Find:** "  - The 990 non-DAF net-asset change is not an operating margin."
- **Replace with:** "  - The 990 non-DAF net-asset change is not an operating margin and is retired as one: it tracks other-fund growth, endowment returns, campaign receipts and Schedule D reporting basis, and the fee surplus is identifiable in it at none of the five audited sponsors. [b4427-03]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

- **Find:** "The 990 balance-sheet proxy does not reproduce these margins. [V wave 38B]"
- **Replace with:** "The 990 balance-sheet proxy does not reproduce these margins. [V wave 38B] It is retired as a margin measure: it is Schedule D other-fund growth at Fidelity, endowment growth at JCF, Schedule D reporting basis at RCF and NCF, and campaign and endowment gains at CJP. Parent-firm marketing is only partly visible: Fidelity and Raymond James list fundraising among the services bought under their administrator agreements, DAFgiving360 pays its own advertising and reimburses Schwab for its workforce, Vanguard Charitable books its own fundraising, and Goldman Sachs, Morgan Stanley and BofA file nothing on who pays. [b4427-03]"
