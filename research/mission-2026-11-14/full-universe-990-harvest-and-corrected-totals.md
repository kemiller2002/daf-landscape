# Full-universe Form 990 harvest, DAF filers outside DAFRC, and corrected DAFRC totals

*Queue items P-990-04, P-MOR-01, P-990-01, P-990-02 and P-990-05. Prepared 2026-11-14. Builds on `vendor-footprint-990-harvest.md` (top-250 pass) and `sponsor-mortality-analysis.md` as amended by `validation-wave4-report.md`. Scripts (stdlib only, functional style): `scripts/mission_990_contractors.py` (extended, not rewritten) and the new `scripts/mission_dafrc_corrected_totals.py`. DAFRC source data is not modified.*

## 1. Bottom line

- **Coverage is complete (P-990-04).** All **1,512 of 1,512** FY2024 DAFRC sponsors ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)) have at least one FY2022–FY2025 Form 990 in the [IRS e-file index](https://apps.irs.gov/pub/epostcard/990/xml/2025/index_2025.csv), and every one has at least one return parsed. The harvest located 5,416 returns and parsed 5,272. The 144 not parsed are all FY2025 returns that the GivingTuesday mirror does not hold yet. Together the 1,512 sponsors hold 100% of DAFRC's $327.87bn FY2024 DAF assets.
- **Moving from 250 to 1,512 sponsors barely changes the vendor picture.**
  - 985 of the 1,512 sponsors list no Part VII-B contractor in any year. They hold $25.3bn, 7.7% of assets.
  - Ren (including Stellar/iPhi) goes from 25 to **30 paying sponsors**. Assets covered rise only from $48.37bn to $48.55bn, which is 14.8% of the full universe. The 5 new Ren payers are small (all under $63m): Southwest Florida CF, Catholic Community Foundation of Los Angeles, Greater Green Bay CF, CF of Greater Flint and the Jewish Federation of Greater Seattle.
  - Foundant (6), NPact (1), Give Interactive (1), TIFIN (1) and CAF America (1) are unchanged. CSuite/CommunitySuite, Chariot and Foundation Source still have **no lines**.
  - Blackbaud rises from 1 to 13 payers. 12 of these are single-issue charities, mostly hospital and university foundations paying for Raiser's Edge/CRM; the other is a community foundation (Greater Washington).
  - The one vendor that is new to this analysis is **Northeast Retirement Services**, which does donor and fund accounting for 3 sponsors with $3.33bn of assets.
- **DAF filers outside DAFRC (P-MOR-01) are numerous but small, with one exception.** The [IRS SOI annual Form 990 extracts](https://www.irs.gov/statistics/soi-tax-stats-annual-extract-of-tax-exempt-organization-financial-data) carry the Part IV line 6 answer for every e-filed 990, so the population was scanned in full rather than sampled.
  - Each year 1,235–1,341 filers whose EIN is not in DAFRC answer "Yes". Of these, **413–538 a year report a positive Schedule D Part I DAF value** (999 distinct EINs over FY2020–FY2024).
  - Their combined DAF assets are **$0.15bn (FY2023) to $0.89bn (FY2020)**, between 0.06% and 0.53% of DAFRC.
  - The exception is **SDG Impact Fund (EIN 46-2368538): $10.10bn in FY2021 and FY2022**, about 4.3–4.5% of DAFRC's total ([FY2022 990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202342799349301349_public.xml)).
  - DAFRC's list therefore misses roughly 400–540 small sponsors a year, typically about $0.1m each.
- **Corrected DAFRC totals (P-990-01/02).** Corrected values replace imputed rows with filed values where a filed value exists, and remove the double-counted terminated sponsors:

  | FY | Assets published → corrected | Δ | Main driver |
  |---|---|---|---|
  | 2020 | $168.76bn → $168.74bn | −0.01% | minor |
  | 2021 | $234.33bn → $234.01bn | −0.14% | TIAA Charitable −$0.26bn (R2) |
  | 2022 | $229.69bn → $228.14bn | **−0.67%** | Jasper Ridge −$1.49bn (R2) |
  | 2023 | $256.39bn → $256.37bn | −0.01% | minor |
  | 2024 | $327.87bn → **$323.27bn** | **−1.40%** | 637 imputed rows replaced (−$4.88bn); Donors Fund and Greater Pike added (+$0.32bn) |

  The FY2024 correction also moves the flow and account totals:
  - Contributions rise **+$2.20bn (+2.4%)** and grants **+$1.84bn (+2.8%)**, because DAFRC imputed both too low.
  - Accounts fall **−280,584 (−7.8%)**, of which PayPal Charitable Giving Fund is −314,335.
  - Asset growth for FY2023→24 falls from 27.9% to **26.1%**. The FY2024 payout rate (grants ÷ prior-year assets) rises from 25.2% to **25.9%**. FY2021→22 asset growth goes from −2.0% to **−2.5%**.
- **New graph edges (P-990-05).** There are **45 new 990-evidenced vendor→sponsor edges** (EC001–EC045), all `confirmed` because each filed 990 names the payee. They include:
  - NCF–Stellar: $2.50m in FY2024 ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513109349303201_public.xml));
  - US Charitable Gift Trust–Renaissance Administration: $4.43m in FY2024 ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533189349305673_public.xml));
  - 15 further Ren/Stellar edges;
  - 6 Foundant edges;
  - 3 Northeast Retirement Services edges.

## 2. Method

### 2.1 Sources

| Source | Status 2026-11-14 | Used for |
|---|---|---|
| DAFRC sponsor dataset, Spring 2026 (`data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv`, from the [DAFRC xlsx](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)) | read only | Sponsor universe, published values and their provenance flags |
| DAFRC published memo totals (`daf-market-annual-series.csv`, series `DAFRC_2025_UPDATED`, [memo](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf)) | read only | "Published" column |
| IRS TEOS e-file index 2020–2026, `https://apps.irs.gov/pub/epostcard/990/xml/{YYYY}/index_{YYYY}.csv` | works | EIN → OBJECT_ID per tax period |
| GivingTuesday mirror of the IRS XML, `https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml` | works; HTTP 404 for 144 FY2025 returns | Part VII-B, Part IV, Part IX, Schedule D Part I |
| IRS SOI annual extracts `https://www.irs.gov/pub/irs-soi/{yy}eoextract990.zip`, yy = 20–25 ([index page](https://www.irs.gov/statistics/soi-tax-stats-annual-extract-of-tax-exempt-organization-financial-data)) | works (about 274k–364k returns per file) | Part IV line 6 (`dnradvisedfundscd`) for all e-filed 990s |
| `sponsor-exit-verification.csv` (mortality study, tier A) | read only | Final-return year and Schedule N for ceased sponsors |

### 2.2 Full harvest (P-990-04)
- `select_targets(rows, 0)` now returns all 1,512 FY2024 sponsors: 103 National, 803 Community, 606 Single Issue.
- Run as `--n-sponsors 0 --out-tag=-full`. The `*-full.csv` outputs sit beside the original top-250 files, which are untouched.
- `vendor-footprint-from-990.csv` was rebuilt for the full universe. The previous version is kept unchanged as `vendor-footprint-from-990-top250.csv`.
- Return selection, streaming parse and the vendor normaliser are as in the top-250 pass (§2.3–2.4 of `vendor-footprint-990-harvest.md`). Two rules were added after reviewing unmatched names: Northeast Retirement Services and GiveGab.
- **Validation.** The parsed Schedule D year-end value equals DAFRC's filed value, within 0.5%, for **3,624 of 3,632** comparable sponsor-years. Exceptions include Coastal Community Foundation FY2022 and Armstrong County CF FY2024 ($9.5m filed against $148.2m in DAFRC).

### 2.3 Outside-DAFRC scan (P-MOR-01, task `outside`)
1. Read all six SOI extracts. Keep rows with `dnradvisedfundscd = Y` and a tax period ending in 2020–2025. Keep one row per (EIN, tax period), with the later extract winning. Result: 14,199 rows.
2. Split by whether the EIN appears anywhere in the DAFRC panel:
   - 7,524 rows are DAFRC EINs;
   - **6,675 rows (2,468 EINs) are not**.
3. For each non-DAFRC row, find the newest Form 990 OBJECT_ID for the same tax period in the IRS index and parse Schedule D Part I (6,506 parsed; 168 have no matching OBJECT_ID and 1 is not mirrored).
4. Classify each row as one of:
   - `reports_daf_value`;
   - `reports_daf_count_value_blank_or_zero`;
   - `reports_daf_data_implausible` (the same flag as the gaps check);
   - `flag_yes_other_funds_column_only`: the "Yes" refers only to Schedule D Part I column (b), "funds and other accounts";
   - `flag_yes_but_no_sched_d_daf_data`;
   - `no_990_object_in_irs_index`.
5. Only `reports_daf_value` rows count towards the asset estimate.

This is a **full scan of "Yes" answers, not a sample**.

### 2.4 Corrected totals (P-990-01/02, `mission_dafrc_corrected_totals.py`)
**Rows tested:**
- every DAFRC FY2020–FY2024 row with at least one `Imputed` metric;
- every sponsor-year DAFRC treats as closed (no row).

That is 1,250 sponsor-years. For each, the script takes the newest same-fiscal-year Form 990 (an amended return supersedes the original), using the same functions as the gaps task. All 1,177 needed returns were parsed.

The rules below apply per metric (assets, contributions, grants, accounts), and only where DAFRC's own provenance flag for that metric is `Imputed`:

| Rule | Condition | Correction |
|---|---|---|
| **R1** filed replaces imputed | Same-FY 990 reports the Schedule D Part I field | Filed value (a filed 0 counts) |
| **R2** terminated double count | Tier-A ceased sponsor, FY ≥ final-return FY | Final return's Part I value, or 0 where blank or no return. The assets moved by Schedule N to sponsors already in the panel |
| **R3** 990 says no DAFs | Part IV line 6 = No and Part I blank | 0 |
| **R4** closed but filed | No DAFRC row; same-FY 990 reports a positive DAF value | Filed values added |
| Unresolved (kept) | No same-FY 990, 990-EZ/PF only, Part IV "Yes" with Part I blank, implausible count, negative amount, or a count with zero/blank value | Published value kept; listed with `applied = 0` |

Every changed value is a row in `dafrc-corrections-itemized.csv` with its rule, return OBJECT_ID, submission date and XML URL. The totals file shows the published memo value, the DAFRC dataset sum, the corrected value and the delta split by rule.

### 2.5 Edges (P-990-05)
- **Pair selection.** One edge per (vendor group, sponsor EIN) Part VII-B relationship absent from `relationship-graph-edges.csv`, `-additions.csv` and `-additions-2.csv`. The sponsor matching was hardened in this pass: it uses the 990 filer name as well as the DAFRC name, reads parenthetical aliases such as "WaterStone (Christian Community Foundation Inc)", and treats ambiguous single-token labels as unmatched.
- **Eligible vendors:**
  - DAF-specialist vendors (Ren/Stellar, Foundant, NPact, Give Interactive, TIFIN, CSuite, Crown, Pinkaloo, CAF America and others), and outsourced administrators, at any sponsor;
  - general donor-technology and payment vendors (Blackbaud, Bonterra, Stripe, PayPal, BlueSnap) only at National and Community sponsors. At university and hospital foundations those lines evidence fundraising CRM, not DAF administration.
- **Relationship type:** `administers` when the service text names administration, donor services, fund accounting or fiduciary work; otherwise `technology_provider` or `payment_processor`.
- **Status:** `confirmed` in every case, because the 990 names the payee.

## 3. Results: full-universe vendor footprint (P-990-04)

### 3.1 Coverage

| Measure | Top-250 pass | Full pass |
|---|---|---|
| Target EINs | 250 | **1,512** |
| In IRS index with any 990 / with ≥1 parsed FY2022–25 990 | 250 / 250 | 1,512 / 1,512 |
| Returns located / parsed / not mirrored | 856 / 837 / 19 | 5,416 / 5,272 / 144 (all FY2025) |
| Sponsors parsed, by FY (2022/23/24/25) | 246/249/247/94 | 1,490 / 1,508 / 1,504 / 755 |
| Returns with ≥1 Part VII-B line | 559 | 1,565 |
| Contractor lines / sponsors with any line / normalised vendors | 1,985 / 174 / 910 | 5,074 / 527 / 2,490 |
| Contractors >$100k reported vs itemised | 17,935 vs 1,985 | 53,782 vs 5,074 (9.4%) |
| Sponsors with no line in any year | 76 ($17.9bn) | **985 ($25.3bn)** |

### 3.2 DAF-relevant vendors, full universe
Source: `vendor-footprint-from-990.csv`. Asset share is out of $327.87bn, using each paying sponsor's DAFRC FY2024 assets. Compensation is the sum of listed lines over FY2022–25.

| Vendor | Sponsors (top-250 → full) | Σ compensation | Sponsor DAF assets | % of DAFRC | New edges |
|---|---|---|---|---|---|
| Ren (incl. Stellar/iPhi) | 25 → **30** | $119.00m | $48.55bn | 14.8% | 17 |
| Blackbaud | 1 → 13 | $6.01m | $0.46bn | 0.1% | 1 (12 of 13 are single-issue charities, excluded) |
| Foundant Technologies | 6 → 6 | $1.36m | $3.88bn | 1.2% | 6 |
| Salesforce | 2 → 4 | $7.64m | $27.41bn | 8.4% | – (enterprise software, not edged) |
| Stripe | 0 → 4 | $2.81m | $0.11bn | 0.0% | 2 |
| Northeast Retirement Services | – → 3 | $1.17m | $3.33bn | 1.0% | 3 |
| Bonterra (CyberGrants / NfG) | 2 → 3 | $25.98m | $0.58bn | 0.2% | 3 |
| Mightycause | 2 → 3 | $10.95m | $0.56bn | 0.2% | 3 |
| PayPal (incl. Braintree) | 2 → 2 | $4.56m | $0.27bn | 0.1% | 2 |
| NPact | 1 → 1 (AEF) | $0.67m | $9.48bn | 2.9% | 0 (edge EA024 exists) |
| Give Interactive | 1 → 1 (FFTC) | $0.65m | $2.95bn | 0.9% | 0 (edge EB007 exists) |
| CAF America | 1 → 1 (GS Gives) | $1.67m | $0.52bn | 0.2% | 0 |
| TIFIN Give | 1 → 1 (GiveClear) | $0.19m | $0.03bn | 0.0% | 0 |
| CSuite/CommunitySuite, Chariot, Foundation Source | 0 → 0 | – | – | – | – |

**Reading.**
- The 1,262 sponsors outside the top 250 hold $14.0bn (4.3%). Most pay no contractor more than $100k, so Part VII-B cannot show their platform vendor.
- Ren's 990-evidenced reach is **14.8% of DAFRC assets**. It is a floor: NPT, for example, runs on Ren but lists no Ren line.
- Community-foundation platforms (Foundant, CSuite, Blackbaud FIMS) are mostly paid under the $100k threshold and are structurally under-observed.

### 3.3 Selected new relationships (all in `relationship-graph-edges-additions-3.csv`)
- **EC027 Stellar → National Christian Foundation**, "software/consulting": $1.20m (FY2022), $1.45m (FY2023) and $2.50m (FY2024).
- **EC026 Ren (Renaissance Administration LLC) → The US Charitable Gift Trust**, "donor serv/fd acct/tax": $3.68m, $3.74m and $4.43m (FY2022–24). Typed `administers`.
- **EC030 Stellar → Catholic Community Foundation of Los Angeles**, "payment processing": $0.30–0.31m a year in FY2022–24 ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533179349310063_public.xml)).
- **EC034 Ren → Jewish Federation of Greater Seattle**, "endowment platform service": $0.13–0.16m a year in FY2022–25 ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601359349310185_public.xml)).
- **EC038, EC041, EC042: Stellar at Greater Green Bay CF** ("ERP system provider", $185,735 in FY2025, [990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513179349310111_public.xml)), **CF of Greater Flint** ($114,605 in FY2022) and **Southwest Florida CF** ($110,707 in FY2022).
- **EC021–EC023 Northeast Retirement Services:**
  - Advisors Charitable Gift Fund, "donor accounting", $107k–$154k a year in FY2022–25 ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202602569349300060_public.xml));
  - Foundation for the Carolinas, "fiduciary services", $499,715 in FY2022 ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202343199349307329_public.xml));
  - Winston-Salem Foundation, "endowment unitization", $159,325 in FY2022.
- **EC043 Stripe → Community Foundation of the Texas Hill Country**, "donation processing software": $1,054,498 in FY2025 ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202602059349301405_public.xml)).
- **EC016 GiveGab → Community Foundation of Sarasota County**, "give day platform": $135,000 in FY2022 ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202310409349300126_public.xml)).
- Earlier top-250 findings are carried into edges for the first time:
  - Foundant at 6 community foundations (EC008–EC013);
  - T. Rowe Price–Ren PSG (EC029);
  - Ayco–Stellar (EC032);
  - donation processors' platform vendors: AOGF–BlueSnap and AOGF–PayPal, CAF America–CyberGrants, Network for Good–Bonterra (EC002–EC004, EC024);
  - Dechomai–Charitable Solutions (EC006);
  - Give Back Foundation–TASC (EC045).
- **Duplicates suppressed:** Give Interactive–FFTC (EB007), NPact–AEF (EA024), Stellar–Memphis (E160/EA029), Stellar–WaterStone (EA004), Ren–Servant (EB003), Ren–Jewish Communal Fund (EB006).

## 4. Results: DAF sponsors outside DAFRC (P-MOR-01)
Source: `non-dafrc-daf-filers-summary.csv` and `non-dafrc-daf-filers-990.csv` (6,675 rows).

| FY | Non-DAFRC "Yes" returns | Report DAF value | Count, no value | Implausible | Other-funds column only | No DAF data | No 990 object | DAF assets | Excl. SDG Impact Fund | Accounts | % of DAFRC assets |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2020 | 1,297 | 498 | 102 | 19 | 116 | 417 | 145 | $0.89bn | $0.89bn | 12,521 | 0.53% |
| 2021 | 1,322 | 538 | 92 | 36 | 133 | 513 | 10 | $10.58bn | $0.48bn | 4,296 | 4.51% |
| 2022 | 1,341 | 496 | 102 | 48 | 135 | 555 | 5 | $10.49bn | $0.38bn | 6,721 | 4.57% |
| 2023 | 1,308 | 424 | 108 | 41 | 141 | 592 | 2 | $0.15bn | $0.15bn | 2,376 | 0.06% |
| 2024* | 1,235 | 413 | 106 | 42 | 140 | 529 | 4 | $0.34bn | $0.34bn | 11,992 | 0.10% |

\*FY2024 lacks returns processed in 2026, because no 2026 SOI extract exists yet. FY2025 (172 rows) is partial and not shown.

**Findings**
1. **DAFRC misses a long tail of small sponsors, not money.**
   - Each year roughly 410–540 filers that are absent from DAFRC report DAF assets. In FY2023 only 13 hold more than $1m and 3 more than $10m; the median is about $0.1m.
   - Excluding SDG Impact Fund, they add **0.06–0.5%** to DAFRC's assets.
   - A further 92–108 report a DAF count without a value.
   - **For sponsor counts the miss is material:** about 27–37% more sponsors than DAFRC's roughly 1,450–1,510.
2. **SDG Impact Fund is the one large omission.** It reported $238.0m (FY2020), **$10,098,899,773 (FY2021)** and **$10,103,954,026 (FY2022)** ([FY2021 990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202242139349301369_public.xml), [FY2022 990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202342799349301349_public.xml)). No FY2023+ "Yes" row appears in the extracts. This is consistent with the mortality study (P-FAIL-02). Whether DAFRC excluded it by vetting is unknown (proposal P-99F-02).
3. **Other notable non-DAFRC filers:**
   - Vancouver Foundation: $214.1m, FY2020;
   - Oregon Jewish Community Foundation: $54.4m in FY2020 and $43.7m in FY2024, with no "Yes" row in FY2021–23;
   - In His Steps Foundation: $43.5m, FY2024;
   - US Family Foundation: $27–33m;
   - National Society for Hebrew Day Schools: about $50m, FY2020–21;
   - Maalot: $24.9m, FY2024.
4. **About half of the "Yes" answers are not DAF evidence.** 116–141 a year fill only Schedule D column (b), "funds and other accounts" (for example St Paul's School). Another 417–592 attach Schedule D with Part I blank.
5. **Bottom-line estimate.**
   - Including SDG Impact Fund, DAFRC understates DAF assets by **about 4.5% in FY2021–22**.
   - Excluding it, DAFRC understates DAF assets by **0.1–0.5%**.
   - DAFRC understates the number of sponsors by about 400–540 a year.

## 5. Results: corrected DAFRC totals (P-990-01, P-990-02)
Source: `dafrc-corrected-market-totals.csv`. "Dataset" is the sum of the DAFRC sponsor rows; the published memo values equal it to rounding.

| FY | Metric | Dataset (published) | Corrected | Δ | Δ% | R1 | R2 | R3 | R4 |
|---|---|---|---|---|---|---|---|---|---|
| 2020 | Assets | $168.760bn | $168.740bn | −$0.020bn | −0.01% | −0.001 | 0 | −0.019 | 0 |
| 2020 | Contributions | $49.499bn | $49.497bn | −$0.002bn | 0.00% | 0 | 0 | −0.002 | 0 |
| 2020 | Grants | $35.542bn | $35.641bn | +$0.100bn | +0.28% | +0.101 | 0 | −0.001 | 0 |
| 2020 | Accounts | 1,566,221 | 1,566,151 | −70 | 0.00% | −10 | 0 | −60 | 0 |
| 2021 | Assets | $234.334bn | $234.013bn | −$0.321bn | −0.14% | −0.015 | **−0.262** | −0.044 | 0 |
| 2021 | Contributions | $77.525bn | $77.522bn | −$0.003bn | 0.00% | 0 | 0 | −0.003 | 0 |
| 2021 | Grants | $47.902bn | $48.032bn | +$0.130bn | +0.27% | +0.136 | 0 | −0.006 | 0 |
| 2021 | Accounts | 1,890,629 | 1,888,462 | −2,167 | −0.11% | −62 | −1,896 | −209 | 0 |
| 2022 | Assets | $229.688bn | $228.144bn | −$1.544bn | −0.67% | −0.005 | **−1.493** | −0.046 | 0 |
| 2022 | Contributions | $76.486bn | $76.478bn | −$0.008bn | −0.01% | 0 | 0 | −0.008 | 0 |
| 2022 | Grants | $55.429bn | $55.610bn | +$0.181bn | +0.33% | +0.187 | 0 | −0.005 | 0 |
| 2022 | Accounts | 3,258,359 | 3,258,113 | −246 | −0.01% | −14 | −6 | −226 | 0 |
| 2023 | Assets | $256.387bn | $256.368bn | −$0.019bn | −0.01% | −0.018 | 0 | −0.006 | +0.006 |
| 2023 | Contributions | $65.361bn | $65.367bn | +$0.006bn | +0.01% | 0 | 0 | 0 | +0.006 |
| 2023 | Grants | $54.774bn | $54.830bn | +$0.056bn | +0.10% | +0.052 | 0 | 0 | +0.004 |
| 2023 | Accounts | 3,030,552 | 3,030,383 | −169 | −0.01% | −150 | 0 | −34 | +15 |
| 2024 | Assets | $327.871bn | **$323.270bn** | −$4.601bn | **−1.40%** | −4.882 | 0 | −0.042 | +0.323 |
| 2024 | Contributions | $90.572bn | **$92.774bn** | +$2.202bn | +2.43% | +1.595 | 0 | −0.042 | +0.649 |
| 2024 | Grants | $64.602bn | **$66.442bn** | +$1.840bn | +2.85% | +1.327 | 0 | −0.034 | +0.547 |
| 2024 | Accounts | 3,590,067 | **3,309,483** | −280,584 | −7.82% | −286,571 | −6 | −340 | +6,333 |

R1–R4 columns are in $bn, except accounts.

**Findings**
1. **The double-counted terminated sponsors are the main FY2021–22 defect.**
   - **Jasper Ridge Charitable Fund FY2022:** DAFRC imputes $1,493,085,967. The final 990 reports 0 at year end, after Schedule N transfers of about $1.32bn, mostly to Schwab ($750.6m) and Fidelity ($548.9m) ([final 990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202313149349304316_public.xml); recipients per wave-4 V4-08).
   - **TIAA Charitable FY2021:** DAFRC imputes $261,839,418 and 1,879 accounts. The final short-year 990 reports 0, after a $138,461,300 transfer to RCF on 2021-03-09 ([final 990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202111979349301206_public.xml)). The "244 accounts" figure refers only to a separate $354,551 residual transfer (wave-4 correction #1).
   - **One smaller R2 case:** Pittsburgh Leadership Fund FY2021 (grants $286k, 17 accounts).
2. **FY2024 is mostly a timing correction.**
   - 637 imputed asset values now have a filed value. Filed is higher in 210 and lower in 427.
   - Largest falls: AEF −$1.10bn ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513219349310376_public.xml)), Dechomai Asset Trust −$0.79bn, ImpactAssets −$0.73bn, BofA CGF −$0.37bn.
   - Largest rises: GS PWM +$0.80bn, Signatry +$0.39bn, RCF +$0.28bn.
   - The returns behind the 632 rows submitted before 2026 account for the whole −$4.88bn (`delta_from_returns_submitted_before_2026`).
3. **Imputation biases flows downward and balances upward.**
   - Contributions were under-imputed by $1.60bn (R1). Examples: GS PWM $3.41bn imputed against $5.83bn filed; Signatry $0.19bn against $1.00bn.
   - Grants were under-imputed by $1.33bn (R1). Example: BNY Mellon CGF $0.14bn against $0.73bn.
   - Accounts were over-imputed, almost entirely at PayPal Charitable Giving Fund: 694,979 imputed against 380,644 filed ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533079349301308_public.xml)).
4. **R4 additions are late or amended filers.**
   - Donors Fund Inc FY2024: $315,757,385, 6,290 accounts, contributions $648.4m and grants $546.9m, from the **amended** TY2024 return filed 2026-03-12 ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202431629349301673_public.xml); wave-4 correction #5).
   - Greater Pike CF FY2024: $7.0m.
   - Helping Hands Support FY2023: $5.5m.
   - Christian Ministries Foundation FY2023: $0.25m.
5. **What remains imputed after correction:**
   - FY2024: $1.10bn of assets in 57 rows, and 10,649 accounts.
   - FY2020–23: $0.50–1.92bn a year.

   These rows are Part IV "Yes" with Part I blank, missing returns, or suspect entries. Examples of suspect entries: USC FY2024 reports −$53.0m; Université de Montréal FY2024 reports 714 DAFs with $0 value. Both are kept as published.
6. **Growth and ratios after correction:**
   - FY2023→24 asset growth: 27.9% published, **26.1%** corrected.
   - FY2021→22 asset growth: −2.0% published, **−2.5%** corrected.
   - FY2024 payout (grants ÷ prior-year assets): 25.2% published, **25.9%** corrected.
   - FY2024 average account: $91,327 published, **$97,680** corrected.

## 6. Limitations
- **Part VII-B lists only the five largest contractors paid over $100k.** Only 9.4% of the reported engagements over $100k are itemised. Absence of a vendor is not evidence of no relationship, and asset coverage is a floor.
- **The FY2025 mirror lags.** 144 FY2025 returns are not mirrored. The FY2025 footprint is partial, and FY2025 corrections are out of scope.
- **The outside-DAFRC scan sees only filers that answer Part IV line 6 "Yes".**
  - Sponsors that answer "No", file a 990-EZ (no Schedule D) or file on paper are invisible (proposal P-99F-03).
  - FY2020 has 145 "Yes" rows with no matching OBJECT_ID in the 2020–2026 indexes.
  - The 2026 SOI extract does not exist yet, so FY2024 is short of late filers.
  - Non-DAFRC EINs may include entities DAFRC excluded deliberately by vetting. The scan cannot tell exclusion from omission.
- **The corrected totals keep DAFRC's universe, fiscal-year convention and non-imputed values.** They do not add non-DAFRC sponsors (§4 gives that separately) and do not net out DAF-to-DAF transfers (P-99F-06).
- **The R2 list depends on tier A of the mortality study (11 EINs).** Other terminated sponsors outside the 100 verified exit candidates would be missed. R3 relies on the filer's own Part IV answer.
- **A filed value replaces an imputed one even when the return was submitted after DAFRC's (unpublished) cut-off.** The corrected series is therefore "best current filed data", not a critique of DAFRC's process at the time. `return_ts` and `submitted_before_2026` let readers apply a cut-off.
- **The graph-matching heuristic was tightened** (§2.5). The `sponsor_links_not_in_graph` counts in the rebuilt footprint therefore differ slightly from the top-250 copy. Edge additions were checked by hand against the existing edge lists for duplicates.
- **No-invent rule.** Every value comes from the cited XML, SOI extract or DAFRC row. Blank means the field was absent.

## 7. Data dictionary

### `form990-contractors-harvest-full.csv` (5,074 rows), `form990-returns-schedule-d-harvest-full.csv` (5,416), `form990-harvest-sponsor-universe-full.csv` (1,512)
Same columns as the top-250 files. See `vendor-footprint-990-harvest.md` §7. `selection` is `national_all` or `all_fy2024_dafrc`.

### `vendor-footprint-from-990.csv` (2,490 rows; full universe) and `vendor-footprint-from-990-top250.csv` (910; previous version, unchanged)
Same columns as before: `vendor`, `vendor_category`, `vendor_entities`, `sponsors_paying`, `total_compensation`, `max_annual_compensation_one_sponsor`, `contractor_lines`, `sponsor_daf_assets_fy2024_dafrc`, `sponsor_daf_assets_latest_990_sched_d`, `tax_years`, `fiscal_years`, `sponsor_names`, `sponsor_eins`, `vendor_in_existing_graph`, `sponsor_links_not_in_graph`, `new_link_sponsors`, `raw_names_seen`, `services_seen`.

### `non-dafrc-daf-filers-990.csv` (6,675 rows; one per non-DAFRC EIN × tax period answering Part IV line 6 "Yes")
| Column | Meaning |
|---|---|
| `ein`, `name`, `fiscal_year`, `tax_pd` | Filer and period. FY is the year the period ends |
| `soi_extract_year`, `soi_url`, `soi_total_assets_eoy` | SOI extract supplying the "Yes" flag |
| `status` | Classification (§2.3) |
| `sched_d_daf_*` | Schedule D Part I column (a), as filed |
| `sched_d_other_funds_*` | Part I column (b) |
| `total_assets_eoy`, `daf_value_share_of_total_assets` | Context |
| `daf_ind_part_iv_xml` | Part IV line 6 in the XML |
| `return_object_id`, `return_ts`, `index_year`, `xml_url`, `index_url` | Evidence |

### `non-dafrc-daf-filers-summary.csv` (one row per FY 2020–2025)
Status counts by FY; `non_dafrc_daf_assets` (and `_excl_ge_1bn`), accounts, contributions and grants (`reports_daf_value` rows only); `dafrc_sponsors_fy`; `dafrc_daf_assets_fy`; `non_dafrc_assets_pct_of_dafrc`; `filers_ge_1bn`; `fy_complete_in_soi`.

### `dafrc-corrected-market-totals.csv` (20 rows; FY2020–24 × 4 metrics)
| Column | Meaning |
|---|---|
| `published_memo_value` | DAFRC memo (rounded) value |
| `dataset_sum_as_published` | Sum of DAFRC sponsor rows |
| `corrected_value`, `delta`, `delta_pct` | After R1–R4 |
| `delta_R*`, `n_R*` | Delta and number of sponsor rows per rule |
| `imputed_value_as_published`, `imputed_value_remaining`, `n_imputed_rows_unresolved` | Imputation before and after |
| `delta_from_returns_submitted_before_2026` | Part of the delta that rests on returns submitted before 2026-01-01 |
| `dataset_sponsor_rows`, `sources` | Context and source references |

### `dafrc-corrections-itemized.csv` (3,547 rows; 2,564 with `applied = 1`)
| Column | Meaning |
|---|---|
| `fiscal_year`, `ein`, `name`, `type`, `metric` | Sponsor-year and metric |
| `dafrc_row` | `present` or `none (assumed closed)` |
| `dafrc_operating_status`, `dafrc_source`, `dafrc_value` | DAFRC row |
| `filed_value`, `corrected_value`, `delta` | Filed and corrected values |
| `applied`, `rule` | Whether the value changed, and which rule changed it |
| `evidence_class` | `990_part_i_reported`, `990_part_iv_no_part_i_blank`, `990_part_iv_yes_or_blank_part_i_blank`, `990_xml_not_mirrored`, `no_990_in_index[_filed_990EZ/PF]` |
| `part_iv_line6`, `return_object_id`, `tax_period`, `return_ts`, `submitted_before_2026`, `amended_ind`, `other_return_type_same_fy` | Return evidence |
| `note`, `source_urls` | Explanation; DAFRC dataset, IRS index and XML |

### `relationship-graph-edges-additions-3.csv` (45 rows, EC001–EC045)
Same columns as `relationship-graph-edges.csv`:
- `evidence_summary` lists every Part VII-B line: FY, payee as filed, service and amount.
- `source_url` is the latest return's XML.
- `notes` gives the vendor group, entities, DAFRC name and type, the ProPublica filing page and the Part VII-B caveat.

### `queue-proposals-990-full.csv`
7 proposals, P-99F-01 to P-99F-07, in the format of `queue-proposals-README.md`.

### Reproduce
```
# DIR holds index_2020..2026.csv; SOI holds {20..25}eoextract990.csv (both downloaded with --fetch)
python3 scripts/mission_990_contractors.py --irs-dir DIR --cache-dir CACHE --fetch --task contractors --n-sponsors 0 --out-tag=-full --footprint-name vendor-footprint-from-990.csv
python3 scripts/mission_990_contractors.py --irs-dir DIR --soi-dir SOI --cache-dir CACHE --fetch --task outside
python3 scripts/mission_dafrc_corrected_totals.py --irs-dir DIR --cache-dir CACHE --fetch
```
With 16–24 threads, a full network run took a few minutes. Re-runs from the cache are offline: under a minute each.
