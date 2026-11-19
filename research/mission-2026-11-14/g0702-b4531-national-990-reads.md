# National-sponsor Form 990 reads: adviser-managed DAF assets (P-G07-02) and NPT's foreign grants (P-B45N31-02)

**Date:** 2026-11-19 · **Task:** g0702-b4531

**Outputs**
- [`data/mission-2026-11-14/adviser-managed-daf-assets-2026-11-19.csv`](../../data/mission-2026-11-14/adviser-managed-daf-assets-2026-11-19.csv): 488 rows in long format (P-G07-02).
- [`data/mission-2026-11-14/npt-foreign-grants-breakdown-2026-11-19.csv`](../../data/mission-2026-11-14/npt-foreign-grants-breakdown-2026-11-19.csv): 519 rows in long format (P-B45N31-02).
- [`data/mission-2026-11-14/queue-proposals-g0702-b4531.csv`](../../data/mission-2026-11-14/queue-proposals-g0702-b4531.csv): P-G0702-01..05.
- **Script:** [`scripts/mission_national_990_reads.py`](../../scripts/mission_national_990_reads.py) (stdlib, functional style).

**Evidence tags:** [F] filed figure (Form 990 XML); [P] the sponsor's or affiliate's own published document; [S] secondary or earlier repo quote not re-fetched here; [C] computed here; [I] inference.

## 0. Headline answers

| Question | Answer |
|---|---|
| **Fidelity Charitable adviser-managed share** | **46.9% of investments** (June 2025): Charitable Investment Advisor Program (CIAP) $37.14bn of $79.23bn [P/C]. The share rose each year: 40.4% (2022), 42.6% (2023), 44.8% (2024).<br>On Schedule D DAF value it is 43.5% (FY2025) [P/F/C].<br>Investment management fees, which equal Form 990 line 11f to the dollar in FY2022–25, are **26.1–26.9 bps of mean CIAP assets** [F/P/C]. That reading holds if the line is CIAP adviser fees only [I]. |
| **DAFgiving360 adviser-managed share** | **Not published.** Bounds from the 990 [C/I]:<br>- **hard floor 1.5%** of DAF value (FY2025): the identified adviser and broker-dealer contractors ($7.20m) divided by the 1.00% adviser-fee cap;<br>- **13.0%** if all of line 11f ($61.37m) is adviser fees charged at the cap;<br>- **48.9%** under a scenario that charges line 11f at Fidelity's 26.5 bps.<br>The often-cited 77–78% is assets "associated with an advisor", which is a different concept [S]. |
| **Vanguard Charitable** | **0%.** Trustees invest all assets in Vanguard Charitable's own options [P]. Line 11f is $0 in every year FY2021–25, and no adviser or broker-dealer appears in Part VII-B [F]. |
| **NPT** | **Not estimable.** Segregated "Financial Advisor Managed" accounts exist from $500k (discretionary) or $2m (non-discretionary), and "a different fee schedule may apply" [P].<br>Line 11f ($93.8m in FY2025; 22.5 bps of mean investments) mixes model-portfolio advisory fees with segregated-account fees [F/P/I].<br>Schedule L (FY2023–24) confirms that "Wells Fargo provides investment management services with respect to certain DAFs at NPT" [F]. |
| **Payments to broker-dealers and RIAs (Part VII-B top five)** | **Fidelity:**<br>- UBS Financial Services: $5.93m (FY2021), $7.85m (FY2022), $11.76m (FY2025);<br>- Morgan Stanley Wealth Management: $1.98m (FY2022);<br>- Wells Fargo Advisors: $3.41m (FY2025);<br>- Rockefeller Capital Management: $1.24m (FY2024);<br>- RIAs: ICONIQ Capital, Jordan Park, William Blair.<br>**DAFgiving360:** Graystone Consulting (Morgan Stanley) every year, $1.67m–$2.92m, plus RIAs (Natural Investments, Basswood, Cerity Partners, Baker Street, Dalton, Wetherby, Jordan Park).<br>**NPT and Vanguard:** none.<br>**Edward Jones** appears in no sponsor's top five in any year [F]. |
| **Schedule J** | No Schedule J at Fidelity, where FMR employs the staff. At the other three it covers only officers' pay (FY2025 top earners $0.61–1.06m). **No adviser or broker-dealer compensation runs through Schedule J** [F]. |
| **NPT FY2023–24 foreign grants: $742.8m** | **To NPT UK and other related organisations: $0 as filed.** Schedule R Part V line 1d ("gift, grant or capital contribution to related organisation") is "No" in both years. NPT UK is also absent from NPT Transatlantic's FY2024 list of material grantees [F/P].<br>**To other foreign organisations: $742.8m (100%).**<br>**Made through NPT Transatlantic:** this London DAF arm is a disregarded entity of NPT, so its grants sit inside NPT's own line 3. They come to **at most $134.9m (18.2%)**: FY2023 ≤ $81.9m (24.7%) and FY2024 ≤ $53.0m (12.9%) [P/C/I]. |
| **By region (FY2023–24 pooled, Part II)** | - Europe 44.3% ($328.5m);<br>- South Asia 17.3% ($128.2m);<br>- Middle East and North Africa 11.8% ($87.3m);<br>- South America 9.4% ($70.1m);<br>- Sub-Saharan Africa 7.5%;<br>- Central America and the Caribbean 4.7%;<br>- North America (Canada, Mexico) 2.8%;<br>- East Asia and the Pacific 2.0%;<br>- Russia and the Newly Independent States 0.2% [C]. |
| **By recipient type** | **All 901 Part II recipient lines** (413 in FY2023, 488 in FY2024) are counted as 501(c)(3)-equivalent on line 2, and **0** as "other organisations" on line 3, even though NPT says it uses both equivalency determination (ED) and expenditure responsibility (ER) [F].<br>By size, half the dollars (49.5%) are in lines of $1m to under $10m, and 16 lines of $10m or more carry 36.5% [C]. |
| **New finding (FY2025)** | NPT Transatlantic granted **£30.939m (≈ $40.1m) to NPT UK** in the year to 30 June 2025, and NPT UK reports the receipt [P]. NPT's FY2025 Schedule R line 1d is still "No" [F].<br>The single largest FY2025 Part II line is $39.1m to Europe, which is about the same size [F/I] (P-G0702-03). |

## 1. Method

### 1.1 Returns

- **Selection.**
  - Source: IRS TEOS e-file index CSVs `index_2021`–`index_2026`, from earlier scratch copies.
  - RETURN_TYPE 990, for the four EINs:
    - Fidelity Investments Charitable Gift Fund, 11-0303001;
    - Donor Advised Charitable Giving Inc. (DAFgiving360, formerly Schwab Charitable Fund), 31-1640316;
    - Vanguard Charitable Endowment Program, 23-2888152;
    - National Philanthropic Trust, 23-7825575.
  - Tax periods ending 2021-01 to 2025-12; the newest OBJECT_ID per tax period. FY is the calendar year in which the period ends (repo convention).
- **Result: 21 returns,** all June year-ends FY2021–FY2025, plus one DAFgiving360 return for 2021-12-30 to 2021-12-31.
  - That two-day return has all lines zero and is ignored in the estimates.
  - Fidelity FY2022 uses the later e-file 202430459349302913, which supersedes 202321309349304807.
- **Sources:**
  - 18 returns came from local XML copies already in scratch;
  - 3 were streamed from the GivingTuesday mirror of IRS TEOS (`gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml`).
- **Checks:** every filer EIN matches, with no fetch failures.

### 1.2 Extraction

Parsing is streamed: Schedule I is cleared as it is read. For each return the script takes:
- Part VII Section B (the five highest-paid contractors and the line 2 count over $100k);
- Part IX line 11a–g, plus line 24 rows mentioning investment or adviser costs;
- Part X lines 11–13 (investments) and line 16;
- Schedule D Part I (DAF count and value);
- Schedule J Part II;
- Schedule L text groups and Schedule O narratives that mention advisers, brokers or investment managers. "Donor-advised" and "donor advisor" hits are dropped;
- Schedule F Parts I, II, III and V;
- Schedule R: related-organisation groups, Part V line 1 indicators and line 2 transactions.

### 1.3 Contractor classes (name and service text only) [I]

- **affiliated_administrator:** FMR, Charles Schwab & Co, Vanguard Group.
- **wirehouse_brand:** Morgan Stanley (including Graystone Consulting), Merrill / Bank of America, UBS, Wells Fargo.
- **other_broker_dealer_or_bank_brand:** Edward Jones, Raymond James, LPL, Ameriprise, JPMorgan, Goldman, RBC, Stifel, Baird, Rockefeller and others.
- **investment_manager_or_adviser:** service text contains invest-, advis-, asset man- and similar.
- **other:** everything else.

Firm registration (whether a firm is an RIA or a broker-dealer) was **not** verified, because adviserinfo.sec.gov and sec.gov are out of bounds.

### 1.4 Published statements

- **Fetched 2026-11-19 after a robots.txt check (§6):**
  - Fidelity: three audited statements, the CIAP overview and the CIAP Investment Policies and Guidelines;
  - Vanguard Charitable: Policies & Guidelines (updated 2026-01-09);
  - NPT: DAF Guide (PDF created 2026-10-15), FY2025 consolidated financials and annual report page;
  - NPT UK: NPT UK and NPT Transatlantic 2024/25 annual report and accounts, and the 2023 grantmaking report;
  - Fed H.10 USD/GBP history.
- The quotes are fixed tables in the script (`PUBLIC`, `AFFILIATE_FACTS`, `TA_MATERIAL`).

### 1.5 Estimates

**Fidelity:**
- adviser-managed share = CIAP ÷ total investments (both from audit Note 3);
- the same CIAP figure ÷ Schedule D DAF value;
- fee rate = investment management fees ÷ mean of opening and closing CIAP.

**DAFgiving360.** With an adviser-fee cap c, adviser-managed assets ≥ adviser fees ÷ c. The script gives three figures:
- (i) **hard floor:** identified adviser, broker-dealer and wirehouse contractor payments ÷ 1.00%;
- (ii) **conditional floor:** line 11f ÷ 1.00%, which holds only if 11f is all adviser fees;
- (iii) **scenario:** line 11f ÷ 26.49 bps, Fidelity's FY2023–25 mean fee rate [I].

**NPT:** no bound. Its 11f includes model-portfolio advisory fees, so the conditional floor is not valid.

**Vanguard:** 0, from its policy text and the filed zeros.

### 1.6 NPT split

1. **Filed related-organisation grants.** These are taken from Schedule R Part V line 1d and line 2 transactions naming NPT UK or Transatlantic.
2. **"Made via Transatlantic" upper bound.**
   - Start from NPT Transatlantic's own grant total in GBP.
   - Subtract the material grants to bodies whose names mark them as US-registered [I]: Economics Education and Research Consortium Inc., Brown University, Longview Philanthropy USA Inc., British Schools and Universities Foundation, Stanford. These would be Schedule I lines, not Schedule F lines.
   - Convert at the mean Fed H.10 noon buying rate for 1 July–30 June: FY2023 1.2049; FY2024 1.2597; FY2025 1.2948.
   - It is an upper bound because unlisted grants under £1m may also go to US or Canadian bodies.
3. **Repair of NPT FY2024 Part II.** The purpose sits in the manner field and the manner in the valuation field. This is repaired as in `mission_foreign_grants.py`; all 488 lines ($410.3m) were affected.

### 1.7 Reproduce

```
python3 scripts/mission_national_990_reads.py . --irs-dir IRS_INDEX_DIR --cache EXTRACT_DIR \
    [--local-dir XML_DIR ...] --fetch --fx-h10 SAVED_dat00_uk.htm
```

## 2. Results: P-G07-02 adviser-managed assets

### 2.1 Filed fee lines, Part IX line 11f (investment management fees) [F]

| FY | Fidelity | DAFgiving360 | Vanguard | NPT |
|---|---|---|---|---|
| 2021 | $40.31m | $28.53m | $0 | $27.92m |
| 2022 | $56.69m | $39.73m | $0 | $34.18m |
| 2023 | $53.69m | $41.37m | $0 | $53.88m |
| 2024 | $67.31m | $47.59m | $0 | $74.18m |
| 2025 | $84.32m | $61.37m | $0 | $93.77m |
| 11f ÷ mean investments, FY2025 [C] | 11.67 bps | 13.88 bps | — | 22.51 bps |

Other filed lines:
- **Line 11a (management):**
  - Fidelity: $100.5m (FY2021) to $179.9m (FY2025). This is the administrative fee passed through to FMR, and it equals the audit's "Administrative fees" ($179,875,837).
  - DAFgiving360: $0.56m to $2.76m.
- **Line 11g (other):** below $3m everywhere.
- **Fidelity line 24 "OTH CHARITABL INV ADVISOR PRGM":** $13.32m, $8.18m, $9.98m, $20.67m and $15.62m in FY2021–25 [F]. The FY2025 audit's "Other expenses" ($21,311,634) is this line plus taxes, per the batch 37 reconciliation. What the line covers is not stated.

### 2.2 Part VII-B adviser, broker-dealer and wirehouse payments (top five only) [F, classes I]

| Sponsor | FY | Contractors > $100k | Adviser / BD / wirehouse firms in the top five (amount) | Subtotal |
|---|---|---|---|---|
| Fidelity | 2021 | 52 | UBS Financial Services (wirehouse) $5.93m; Jordan Park $4.14m; ICONIQ Capital $3.62m | $13.70m |
| Fidelity | 2022 | 57 | UBS $7.85m; Jordan Park $5.59m; ICONIQ $4.42m; Morgan Stanley Wealth Management (wirehouse) $1.98m | $19.84m |
| Fidelity | 2023 | 45 | ICONIQ $6.04m; Jordan Park $4.02m; William Blair & Co $1.12m | $11.18m |
| Fidelity | 2024 | 44 | ICONIQ $7.93m; Jordan Park $2.83m; Rockefeller Capital Management $1.24m | $11.99m |
| Fidelity | 2025 | 73 | UBS Financial Services $11.76m; ICONIQ $10.58m; Wells Fargo Advisors (wirehouse) $3.41m | $25.75m |
| DAFgiving360 | 2021 | 33 | Graystone Consulting (Morgan Stanley) $1.67m; Jordan Park $0.69m; Baker Street $0.67m; Wetherby $0.55m | $3.59m |
| DAFgiving360 | 2022 | 57 | Graystone $1.69m; Baker Street $0.98m; Jordan Park $0.84m; Wetherby $0.66m | $4.16m |
| DAFgiving360 | 2023 | 63 | Dalton Investments $2.63m; Basswood $2.03m; Graystone $1.84m; Natural Investments $1.61m | $8.10m |
| DAFgiving360 | 2024 | 74 | Natural Investments $2.11m; Graystone $2.04m; Basswood $1.63m; Cerity Partners $0.89m | $6.66m |
| DAFgiving360 | 2025 | 101 | Graystone $2.92m; Natural Investments $2.14m; Cerity Partners $1.14m; Baker Street $1.00m | $7.20m |
| NPT | 2021–25 | 9–19 | Only "consulting" firms: AP Advisory/AP Advisors, Disciplina Capital Management, Valor Advisors ($0.25–0.75m a year). ICONIQ Capital is paid for "consulting" ($0.39m FY2023 to $2.86m FY2025) | ≤ $0.75m |
| Vanguard | 2021–25 | 18–28 | None. The top five are Vanguard Group (occupancy and administration), UST Global, Slalom and Salesforce (technology) | $0 |

**Readings:**
- In each sponsor's top five, the remaining slot or slots go to the affiliated administrator (FMR LLC, Charles Schwab & Co) or to legal, audit and consulting firms.
- **The contractor count above $100k at DAFgiving360 tripled, from 33 to 101 (FY2021–25), while 11f doubled.** This is consistent with more adviser firms being paid from DAF assets [F/I].
- **Fidelity's top-five adviser firms account for only 18–35% of line 11f** (FY2021–25; $25.75m of $84.32m in FY2025), so most adviser fees go to firms below the top five [C].
- **Vanguard Schedule L:** Vanguard Brokerage Services broker commissions to an interested person's affiliate, $2,342 to $4,194 a year [F].
- **DAFgiving360 Schedule L:** Charles Schwab & Co, as "founder", is paid $4.29m to $11.43m a year for "brokerage & administrative services" [F].

### 2.3 Fidelity Charitable CIAP [P/C]

| June year end | CIAP adviser-managed investments | Total investments | Share of investments | Share of Schedule D DAF value | Audit investment management fees | bps of mean CIAP |
|---|---|---|---|---|---|---|
| 2022 | $18,112,561,857 | $44,823,238,524 | **40.4%** | 37.9% | $56,692,887 | — |
| 2023 | $22,433,249,315 | $52,650,176,429 | **42.6%** | 40.3% | $53,687,639 | 26.48 |
| 2024 | $27,546,211,645 | $61,514,405,850 | **44.8%** | 41.6% | $67,308,635 | 26.93 |
| 2025 | $37,139,208,368 | $79,232,938,398 | **46.9%** | 43.5% | $84,317,489 | 26.07 |

**Programme terms:**
- **Name and purpose:** "Charitable Investment Advisor Program … allows independent investment advisors to serve their clients beyond our investment pools by actively managing the contributions" ([overview](https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/ciap-overview.pdf), PDF dated 2025-04-16).
- **Minimum:** "$100,000 minimum balance requirement".
- **Fee basis:** the adviser is paid "a mutually agreeable and reasonable annual Investment Advisory Fee", with no numeric cap. Fees "cannot be assessed on Giving Account assets in the Fidelity Charitable investment pools", and advisers "may not charge fees on uninvested cash" ([CIAP Investment Policies and Guidelines](https://www.fidelitycharitable.org/docs/ciap-investment-policies-guidelines.pdf), PDF dated 2026-07-10).
- **Sponsor fee on CIAP assets:**
  - 60/30/20/15 bps tiers below $5m;
  - 70/30/20/15 bps when the assets are held at an "Other Custodian";
  - flat 19–11.5 bps from $5m.

**Readings:**
- The **FY2021** CIAP figure is unavailable: the 2022-2021 audit URL returns 404.
- The audit's investment management fees **equal line 11f to the dollar** in FY2022–25. At 26–27 bps of CIAP assets the rate is stable, and it is far below the 1% often assumed for adviser fees. This suggests many CIAP mandates are priced low, or that part of the adviser pay is billed outside the account [I].

### 2.4 DAFgiving360 bounds [C/I]

| FY | Schedule D DAF value | Hard floor: VII-B advisers ÷ 1% | Floor if 11f is all adviser fees (÷ 1%) | Scenario: 11f ÷ 26.49 bps |
|---|---|---|---|---|
| 2021 | $25.50bn | $0.36bn (1.4%) | $2.85bn (11.2%) | $10.77bn (42.2%) |
| 2022 | $26.30bn | $0.42bn (1.6%) | $3.97bn (15.1%) | $15.00bn (57.0%) |
| 2023 | $31.54bn | $0.81bn (2.6%) | $4.14bn (13.1%) | $15.61bn (49.5%) |
| 2024 | $40.94bn | $0.67bn (1.6%) | $4.76bn (11.6%) | $17.96bn (43.9%) |
| 2025 | $47.35bn | $0.72bn (1.5%) | $6.14bn (13.0%) | $23.17bn (48.9%) |

**Published and secondary statements** (not re-fetched; the robots.txt request returned 403):
- **Cap:** adviser fees are capped at 1.00% ([fees and minimums](https://www.dafgiving360.org/features/fees-and-minimums); DAFgiving360 Program Policies, Dec 2024, repo quote).
- **Eligibility:** the adviser must be approved and work with Schwab Advisor Services, with a $100k minimum (repo, Pave doc).
- **Adviser association:** "77% of DAF assets were associated with an advisor relationship" (CY2025, [InvestmentNews](https://www.investmentnews.com/practice-management/dafgiving360-donors-boost-2025-grants-to-nearly-10b/264994)) [S].

**Readings:**
- The 77% measures adviser *association*, not adviser *management* (batch 37 §4.2).
- **Best available statement:** DAFgiving360's adviser-managed share is at least 1.5% (hard floor) and probably at least 13% (if line 11f is adviser fees). It would be about half if its advisers charge what Fidelity's do. No first-party asset split was reachable (P-G0702-01).

### 2.5 Vanguard Charitable and NPT [P/F]

**Vanguard Charitable** ([Policies & Guidelines, updated 2026-01-09](https://www.vanguardcharitable.org/company-policies/policies-and-guidelines)):
- "Vanguard Charitable trustees have sole responsibility and authority to invest Vanguard Charitable's assets".
- "Vanguard Charitable does not itself charge investment fees; expense ratios are assessed by the underlying funds".
- A financial advisor may be added only as an "interested party" with some account access.
- **Share: 0%.** No programme name, no adviser-fee basis.

**NPT** ([DAF Guide](https://www.nptrust.org/a-guide-to-your-donor-advised-fund-npt/)):
- **Product:** "Segregated Accounts – Assets Managed by Your Financial Advisor or other Investment Professional". "DAF accounts over $500,000 may recommend a financial advisor to propose a custom investment portfolio. A different fee schedule may apply."
- **Minimums:** $500,000 for discretionary accounts and $2 million for non-discretionary accounts. "Financial advisors must be approved by NPT."
- **Fees:** model portfolios charge "an investment advisory fee and/or incurs trading costs". The segregated-account fee is not published.
- **Financial statements:** the [FY2025 consolidated financials](https://www.nptrust.org/wp-content/uploads/2026/09/FY25-AR-Consolidated-Financials-NPT.pdf) give asset management fees of $116,260k (FY2024 $94,289k) and investments of $47,837,978k, with no split.
- **Assets:** the [annual report](https://www.nptrust.org/annual-reports/npt-annual-report/) gives $56.4bn of assets under management.
- **Share: not estimable** (P-G0702-05).

### 2.6 Summary table: adviser-managed share by sponsor (latest year)

| Sponsor | Programme | Minimum | Adviser fee basis | Adviser-managed share | Evidence |
|---|---|---|---|---|---|
| Fidelity Charitable | Charitable Investment Advisor Program | $100k | "mutually agreeable and reasonable"; no cap; observed 26.1–26.9 bps of CIAP assets | **46.9% of investments; 43.5% of DAF value (June 2025)** | P/F/C |
| DAFgiving360 | Investment advisor (professionally managed) option | $100k (S) | capped at 1.00% (S) | **≥ 1.5% hard floor; ≥ 13% if line 11f is adviser fees; ~49% at Fidelity's fee rate (scenario)** | F/C/I/S |
| Vanguard Charitable | none | — | none; fund expense ratios only | **0%** | P/F |
| NPT | Segregated Account – Financial Advisor Managed | $500k discretionary / $2m non-discretionary | not published | **not estimable** | P/F |

## 3. Results: P-B45N31-02 NPT foreign grants

### 3.1 Totals [F/C]

| FY | Line 3 foreign grants | Part II total | Part II lines | Line 2 count, 501(c)(3)-equivalent | Line 3 count, other organisations | Foreign share of all grants |
|---|---|---|---|---|---|---|
| 2021 | $164.2m | $164.0m | 229 | 229 | 0 | 2.57% |
| 2022 | $174.4m | $174.1m | 309 | 428 | 0 | 3.14% |
| 2023 | $332.2m | $331.9m | 413 | 413 | 0 | 7.47% |
| 2024 | $410.6m | $410.3m | 488 | 488 | 0 | 7.38% |
| 2025 | $310.5m | $310.2m | 560 | 560 | 0 | 4.84% |
| **2023–24** | **$742.8m** | $742.2m | 901 | 901 | 0 | 7.42% |

- **Consistency:** FY2023–24 line 3 = $742,782,672, which matches the repo's $742.8m. NPT Europe pooled ($328.5m), Middle East and North Africa ($87.3m) and South America ($70.1m) also match direction-foreign-grants-schedule-f.md §3.3.
- **Other parts:** Part III (grants to foreign individuals) is $0 in every year. The public Part II lines show no recipient name, EIN or IRC section.
- **Recipient type:** NPT's Part V says it uses both ED and ER. Yet every recipient is counted in the 501(c)(3)/ED column, so either no ER grantee crossed into line 3, or ER grantees are counted as 501(c)(3)-equivalent [F/I].

### 3.2 Region and size [C]

| Region | FY2023 | FY2024 | FY2023–24 | Share |
|---|---|---|---|---|
| Europe | $167.2m | $161.2m | $328.5m | 44.3% |
| South Asia | $36.0m | $92.2m | $128.2m | 17.3% |
| Middle East and North Africa | $21.4m | $65.9m | $87.3m | 11.8% |
| South America | $34.4m | $35.8m | $70.1m | 9.4% |
| Sub-Saharan Africa | $45.0m | $10.8m | $55.8m | 7.5% |
| Central America and the Caribbean | $3.3m | $31.5m | $34.8m | 4.7% |
| North America (Canada, Mexico) | $13.4m | $7.2m | $20.5m | 2.8% |
| East Asia and the Pacific (incl. "Oceania") | $10.4m | $4.8m | $15.2m | 2.0% |
| Russia and the Newly Independent States | $0.8m | $1.0m | $1.8m | 0.2% |

**Part I:**
- Europe is the only region with an office and staff: 1 office with 6 employees (FY2023) and 9 employees (FY2024). This is NPT Transatlantic's London office.
- Part I also reports **investment** rows, which are not grants: Central America and the Caribbean $1.36bn (FY2023) and $1.70bn (FY2024), i.e. offshore funds. These must not be read as grants (as noted in the direction doc).

**Line sizes, FY2023–24:**
- under $100k: 494 lines, 2.0% of dollars;
- $100k to under $1m: 289 lines, 12.0%;
- $1m to under $10m: 102 lines, 49.5%;
- $10m to under $30m: 15 lines, 31.6%;
- $30m or more: 1 line, 4.8% ($36.0m, Middle East and North Africa, "EDUCATION", FY2024).

**Purpose labels:**
- FY2023: 52.8% of dollars are labelled "CULTURE & ARTS".
- FY2024: 66.6% are labelled "INTERNATIONAL".
- The labels shift from year to year and are NTEE-style, so a purpose split says little.

### 3.3 Affiliates (Schedule R and the affiliates' own accounts) [F/P/C]

**What Schedule R says, every year FY2021–25:**
- **Related organisations:**
  - NPT Transatlantic Limited (UK) is listed as a **disregarded entity**. Its income was $74.4m (FY2022) to $145.8m (FY2024), and its end-of-year assets rose from $105.4m to $279.7m.
  - National Philanthropic Trust UK Limited is a **related tax-exempt organisation** (UK).
- **Part V line 1d** (gift, grant or capital contribution to a related organisation) = **No**. Line 1e, the same *from* a related organisation, = Yes.
- **Part V line 2:** no transaction names NPT UK or Transatlantic.

**What the affiliates publish:**
- NPT Transatlantic is "an independent English charity (Charity Number 1153376) and is recognised by the Internal Revenue Service (IRS) as US public charity because it is considered a disregarded entity of National Philanthropic Trust" ([NPT UK](https://www.nptuk.org/what-is-npt-transatlantic/)).
- Its grants are therefore **NPT's own grants** in the 990. They are not grants *to* an affiliate.

| NPT FY (year to 30 June) | NPT Transatlantic grants | Of which to NPT UK | US-named material grantees (excluded) | Upper bound on Schedule F dollars made via Transatlantic | Share of line 3 |
|---|---|---|---|---|---|
| 2023 | £68m ([2023 grantmaking report](https://www.nptuk.org/annual-reports/2023-grantmaking-report/)) | not listed (no FY2023 grantee list found) | not available | $81.9m | ≤ 24.7% |
| 2024 | £47.49m ([2024/25 accounts](https://www.nptuk.org/transatlantic-annual-report-and-accounts-2025/), comparative) | not among the material grantees (all ≥ £1.257m) | £5.44m (EERC Inc. £3.339m; Brown University £2.102m) | $53.0m | ≤ 12.9% |
| **2023–24** | — | **$0 as filed** | — | **$134.9m** | **≤ 18.2%** |
| 2025 | £84.26m | **£30.939m ≈ $40.06m** | £13.10m (EERC Inc., Longview Philanthropy USA, British Schools and Universities Foundation, Stanford) | $92.1m (includes the NPT UK grant) | ≤ 29.7% |

**Answer to P-B45N31-02:**
- **To NPT UK and other affiliates:** $0 of FY2023–24's $742.8m, as filed and as far as the affiliates' accounts show.
- **To other foreign organisations:** the whole $742.8m.
- **Through NPT's own London arm:** at most $134.9m (18.2%) of it was made through NPT Transatlantic, whose donors are mostly UK–US dual taxpayers. This is the closest thing to an "affiliate" share in the window [P/C/I].
- **Interpretation:** most of NPT's foreign dollars ($607.9m or more, 81.8% or more) are US-side grants made by ED/ER directly to foreign charities [C/I].

### 3.4 FY2025 transfer to NPT UK [P/F/I]

**What the affiliates' accounts say:**
- **NPT Transatlantic** ([accounts note 19](https://www.nptuk.org/transatlantic-annual-report-and-accounts-2025/)): "NPT Transatlantic also granted £30.9m to National Philanthropic Trust UK Limited (NPT UK), which will be used by donors for ongoing granting to charities". The grant table lists it at £30,939k.
- **NPT UK** ([accounts note 14](https://www.nptuk.org/npt-uk-annual-report-and-accounts-2025/)): "Contributions of £30.9M were received from NPT Transatlantic and £30.9M from National Philanthropic Trust". Whether this is one transfer described twice, or two transfers, is not clear.

**What NPT's 990 says:**
- NPT's FY2025 Schedule R line 1d is "No".
- Its largest FY2025 Part II line is $39,100,000 to Europe ("ENVIRONMENT, ANIMALS"). At the FY mean rate, £30.939m is $40.06m, so the sizes match; the date-of-payment rate implied would be 1.2638 [C].

**Reading:** the size match is suggestive, not proof. If it is the transfer, NPT's FY2025 foreign grants include **≈ 12.9% sponsor-to-affiliate re-granting**. That is the cross-border analogue of a DAF-to-DAF flow, and the direction doc's limit 4 flags it (P-G0702-03).

### 3.5 Comparison with the repo's direction-foreign-grants work

- **Same totals:** P-NEW-FGN-01 reported NPT at $742.8m (39.3% of top-50 foreign dollars), Europe-led, with a $410.3m column-shift repair in FY2024. This task reproduces all three numbers.
- **What this task adds:**
  - (a) the affiliate test that limit 4 left open: $0 to NPT UK in FY2023–24, and ≤ 18.2% made through Transatlantic;
  - (b) the observation that NPT's whole Part II is in the 501(c)(3)/ED column;
  - (c) FY2021–22 and FY2025 context: foreign grants were 2.6–3.1% of NPT's grants before FY2023, 7.4–7.5% in FY2023–24 and 4.8% in FY2025;
  - (d) the FY2025 £30.9m affiliate transfer.
- **Effect on the top-50 netting:** if the FY2025 transfer were netted out, the national-segment foreign share in a future FY2025 refresh would fall by about $40m. No change is needed for FY2023–24 [C/I].

## 4. Limits

1. **Part VII-B shows only the five highest-paid contractors.** Most adviser firms (Fidelity: 73 over $100k in FY2025) are invisible, and firm type is inferred from the name.
2. **Line 11f is not labelled "adviser fees" in any return.**
   - At Fidelity it equals the audit's investment management fees, and the reading that these are CIAP adviser fees is inference.
   - At DAFgiving360 the content is unknown.
   - At NPT it includes model-portfolio fees.
3. **No first-party DAFgiving360 document was fetched.** Its robots.txt returned 403, so all DAFgiving360 programme terms are repo quotes [S].
4. **No Fidelity FY2021 CIAP figure:** the audit URL returns 404.
5. **NPT Transatlantic and NPT UK.**
   - Only the 2024/25 accounts (with FY2024 comparatives) are linked from nptuk.org. FY2023 rests on a £68m headline with no grantee list.
   - The Charity Commission register page failed to render for a scripted request (P-G0702-02).
   - The USD conversions use FY-mean H.10 rates, not payment-date rates.
6. **US-registered grantees** among Transatlantic's material grants are identified by name only [I]. Grants under £1m are not itemised, so the "via Transatlantic" figure is an upper bound.
7. **Recency:** all returns are FY2021+ (tax periods ending June 2021 to June 2025). The documents were fetched 2026-11-19.

## 5. Data dictionaries

### 5.1 adviser-managed-daf-assets-2026-11-19.csv

| Field | Meaning |
|---|---|
| sponsor, ein | Sponsor display name and 9-digit EIN |
| fy | Fiscal year (calendar year in which the tax period ends); blank for undated programme terms |
| tax_period, object_id | IRS TEOS tax period (YYYYMM) and e-file OBJECT_ID; blank for published-statement and estimate rows |
| row_type | `part9_line11`, `part9_line24`, `part7b_contractor`, `part7b_count_over_100k`, `part7b_adviser_subtotal`, `part10_investments`, `total_assets`, `sched_d_daf`, `sched_j_summary`, `sched_o_text`, `sched_l_text`, `public_statement`, `estimate` |
| item | Line or item name (e.g. `11f_investment_management`, contractor name, `ciap_assets`, `adviser_managed_share_of_investments`) |
| class | Contractor class (§1.3) [I] |
| value, unit | Value; unit is `usd`, `usd_thousands`, `count`, `share`, `bps` or `text` |
| detail | Services text, Schedule O/L excerpt (≤ 900 characters), quote, or estimate formula |
| form_ref | Form line reference; for `public_statement` rows the fetch status (`fetched`, `not_fetched_robots_403`, `repo_secondary`) |
| evidence | F / P / S / C / I, combined as needed |
| source_url | XML on the GivingTuesday mirror, or the published document |

### 5.2 npt-foreign-grants-breakdown-2026-11-19.csv

| Field | Meaning |
|---|---|
| fy | NPT fiscal year (June year end), or `2023-2024` for pooled rows |
| tax_period, object_id | Tax period end date and e-file OBJECT_ID (return rows only) |
| row_type | `total`, `recipient_type`, `region`, `region_pooled`, `size_band`, `size_band_pooled`, `region_x_size_band`, `purpose`, `largest_line`, `part1_activity`, `schedR_related_org`, `schedR_part5_line1`, `schedR_part5_line2`, `affiliate_account`, `affiliate_material_grant`, `fx_rate`, `affiliate_split` |
| dimension | Sub-key, e.g. `schedF_part2`, `form990_part9_line3_foreign_grants`, the Schedule R indicator name, `made_via_npt_transatlantic_upper_bound` |
| category | Region, size band, purpose text, organisation name or explanatory label |
| lines | Number of Part II lines or recipients; for related-organisation rows, country, income and assets; for material grants, a US-name flag |
| usd | US dollars (filed, or converted at the FY-mean H.10 rate for `affiliate_*` rows) |
| gbp | Pounds sterling as published by NPT UK / NPT Transatlantic |
| share | Share of the relevant total (Part II total for region, band and purpose; line 3 for affiliate_split) |
| note | Quote from the affiliate document, with the FX rate used |
| evidence, source_url | As in 5.1 |

## 6. Source register and robots log

**robots.txt checks** (2026-11-19, user agent "research-script/1.0"):

| Host | Result | Use |
|---|---|---|
| gt990datalake-rawdata.s3.amazonaws.com | 404 (no rules) | 3 XML returns streamed |
| www.irs.gov / apps.irs.gov | 200 / 302 | Nothing fetched; index CSVs reused from scratch copies |
| www.fidelitycharitable.org | 200; disallows /retired/, /sample-email/, /nuance/, /content/dam/fc-public/docs/vessel/ | Audits and CIAP PDFs (allowed paths) |
| www.vanguardcharitable.org | 200; disallows /core/, /profiles/, /search/, /admin/, /user/… | Policies page, advisors page, sitemap |
| www.nptrust.org | 200; `Disallow:` (empty) for * | Guide, financials, annual report, international page |
| www.nptuk.org | 200; `Disallow:` (empty) | Accounts PDFs and grantmaking reports |
| register-of-charities.charitycommission.gov.uk | 200; `Disallow:` (empty) | One page request; the content failed to render |
| www.federalreserve.gov | 404 (no rules) | H.10 GBP history |
| www.dafgiving360.org | **403 on robots.txt itself** | Nothing fetched |

**Primary sources:**
- **IRS Form 990 XML** (`https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml`):

  | Sponsor | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 |
  |---|---|---|---|---|---|
  | Fidelity | 202221339349302787 | 202430459349302913 | 202441369349301334 | 202521349349310887 | 202601389349301700 |
  | DAFgiving360 | 202230499349301028; 202201119349300745 (2-day) | 202330939349300403 | 202411039349301716 | 202541069349300729 | 202611199349300601 |
  | Vanguard | 202211339349310116 | 202331359349303108 | 202441359349309439 | 202511349349313096 | 202621329349306657 |
  | NPT | 202231339349309863 | 202311359349313966 | 202431429349301368 | 202511339349301311 | 202601289349302480 |

- **Fidelity Charitable:**
  - [audit 2025-2024](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf), [audit 2024-2023](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2024-2023.pdf), [audit 2023-2022](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2023-2022.pdf);
  - [CIAP overview](https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/ciap-overview.pdf);
  - [CIAP Investment Policies and Guidelines](https://www.fidelitycharitable.org/docs/ciap-investment-policies-guidelines.pdf).
- **Vanguard Charitable:** [Policies & Guidelines](https://www.vanguardcharitable.org/company-policies/policies-and-guidelines); [Professional Advisors](https://www.vanguardcharitable.org/advisors).
- **NPT:** [DAF Guide](https://www.nptrust.org/a-guide-to-your-donor-advised-fund-npt/); [FY2025 consolidated financials](https://www.nptrust.org/wp-content/uploads/2026/09/FY25-AR-Consolidated-Financials-NPT.pdf); [FY2025 annual report](https://www.nptrust.org/annual-reports/npt-annual-report/); [International Grantmaking](https://www.nptrust.org/donor-advised-funds/international-grantmaking/).
- **NPT UK / NPT Transatlantic:** [Transatlantic 2024/25 accounts](https://www.nptuk.org/transatlantic-annual-report-and-accounts-2025/); [NPT UK 2024/25 accounts](https://www.nptuk.org/npt-uk-annual-report-and-accounts-2025/); [2023 grantmaking report](https://www.nptuk.org/annual-reports/2023-grantmaking-report/); [What is NPT Transatlantic](https://www.nptuk.org/what-is-npt-transatlantic/).
- **FX:** [Federal Reserve H.10 USD/GBP history](https://www.federalreserve.gov/releases/h10/hist/dat00_uk.htm).

**Secondary sources (not re-fetched):**
- [DAFgiving360 fees and minimums](https://www.dafgiving360.org/features/fees-and-minimums) and the DAFgiving360 2024 Program Policies (repo quotes);
- [InvestmentNews 2026-01-27](https://www.investmentnews.com/practice-management/dafgiving360-donors-boost-2025-grants-to-nearly-10b/264994).

**Repo context:**
- [direction-foreign-grants-schedule-f.md](direction-foreign-grants-schedule-f.md);
- [queue-batch37-filing-questions.md](queue-batch37-filing-questions.md) §3–4;
- [pave-daf-adviser-managed-sponsor-access-2026-11-11.md](../pave-daf-adviser-managed-sponsor-access-2026-11-11.md).
