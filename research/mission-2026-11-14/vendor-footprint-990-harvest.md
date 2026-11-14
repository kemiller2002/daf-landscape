# Vendor footprint from Form 990 Part VII-B, and DAFRC processing gaps

*Queue items P-VEN-06 and P-MOR-03. Prepared 2026-11-14. Script: `scripts/mission_990_contractors.py` (stdlib only, functional style). Outputs in `data/mission-2026-11-14/`: `form990-contractors-harvest.csv`, `form990-returns-schedule-d-harvest.csv`, `form990-harvest-sponsor-universe.csv`, `vendor-footprint-from-990.csv`, `dafrc-processing-gaps.csv`, `queue-proposals-990-harvest.csv`.*

## 1. Bottom line

- **Coverage.** All **250 of 250** target sponsor EINs were found in the IRS e-file index. All 250 have at least one parsed FY2022–FY2025 Form 990. The harvest located 856 returns and parsed 837; the other 19 are 2026 filings that the mirror does not hold yet. Together the targets hold **$313.9bn of DAFRC's $327.9bn FY2024 DAF assets (95.7%)** ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)). The run produced 1,985 contractor lines across 174 sponsors and 910 normalised vendors.
- **Both checks against existing figures pass.**
  - The parsed Schedule D year-end DAF value matches DAFRC's filed value for the same EIN and fiscal year in **573 of 574** comparable returns. The one exception, Coastal Community Foundation FY2022, differs by about 12%.
  - The automated harvest reproduces **114 of 119** amounts in the manual `form990-top-contractors.csv`. The 5 misses are all on Vanguard Charitable's FY2025 return, which is not mirrored yet.
- **Ren is the only DAF technology vendor with breadth in Part VII-B.** Ren entities appear at **25 sponsors** holding **$48.4bn** of FY2024 DAF assets, 15.4% of the harvested universe. The entities are RenPSG, Renaissance Administration, Renaissance Acquisition Co, Ren Technology Services and Stellar Technology Solutions/iPhi. Ren was paid **$117.1m** in total over FY2022–FY2025 lines.
  - **15 of these 25 sponsor links are not in the relationship graph.** They include National Christian Foundation (Stellar, **$2.50m** in FY2024, up from $1.20m in FY2022), the US Charitable Gift Trust (Renaissance Administration, $4.43m), the T. Rowe Price Program (Ren PSG), Ayco Charitable Foundation, Servant Foundation, and Jewish federations and community foundations.
- **Other named DAF vendors show up only thinly, because Part VII-B lists just the top five payees above $100k:**
  - Foundant: 6 community foundations, $3.9bn.
  - NPact: American Endowment Foundation (AEF) only.
  - Give Interactive: one line, Foundation for the Carolinas, $654,500 in FY2023.
  - TIFIN Give: GiveClear only.
  - Blackbaud: Greater Washington Community Foundation only.
  - Salesforce: Vanguard Charitable and NCF.
  - CAF America: GS Gives only.
  - PayPal: AOGF and Pure.
  - Chariot and Foundation Source: **no lines**.
- **P-MOR-03: most of DAFRC's FY2024 imputation is filing lag, not lost data.** **632 of 713** imputed FY2024 rows now have an e-filed 990 that reports a DAF value: **$90.98bn filed against $95.86bn imputed**.
  - Substituting the filed values lowers DAFRC's FY2024 total by **$4.88bn (−1.5%)**. Accounts fall by 286,799, of which **PayPal Charitable Giving Fund accounts for −314,335**: DAFRC imputed 694,979 accounts, and the 990 reports 380,644.
  - 522 of the 632 returns were submitted Jul–Dec 2025, 105 by June 2025 and 5 in 2026. Only the 105 early filers ($4.40bn imputed, $4.17bn filed) look like true processing gaps; the rest are timing. DAFRC does not publish its data cut-off.
- **Very few sponsors that DAFRC marks closed still report DAFs.** **4 sponsor-years** were found:
  - Donors Fund Inc: FY2024, 6,290 DAFs, **$315.8m**.
  - Greater Pike Community Foundation: FY2024, $7.0m.
  - Helping Hands Support: FY2023, $5.5m.
  - Christian Ministries Foundation: FY2023, $0.25m.

  All four returns were submitted between April 2025 and April 2026, so these are late filings, not missed ones.
- **The larger defect is the reverse case: DAFRC imputes DAF values where a filed 990 shows none.** This happens in 88 FY2021–FY2023 rows ($3.64bn). The two largest are terminated sponsors whose assets were transferred to other panel sponsors and so are double-counted:
  - Jasper Ridge: **$1.49bn** imputed for FY2022.
  - TIAA Charitable: **$0.26bn** imputed for FY2021.

## 2. Method

### 2.1 Sponsor universe
The source is `dafrc-sponsor-schedule-d-fy2019-2024.csv` (DAFRC Spring 2026 edition, [dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)). It includes:
- **all 103 National sponsors** present in FY2024 (81 Standard and 22 Donation Processor);
- the **147 largest Community Foundation and Single Issue sponsors** by FY2024 `eoy_daf_assets`. The smallest of these holds $92.6m.

The full list is in `form990-harvest-sponsor-universe.csv`. FY2024 DAFRC values are used as published, including the imputed ones.

### 2.2 Which source works
| Source | Result on 2026-11-14 | Used for |
|---|---|---|
| IRS TEOS e-file index, `https://apps.irs.gov/pub/epostcard/990/xml/{YYYY}/index_{YYYY}.csv` ([2025](https://apps.irs.gov/pub/epostcard/990/xml/2025/index_2025.csv)) | Works (HTTP 200, full download; range requests are ignored). Years 2021–2026 were loaded | Finding returns: EIN, TAX_PERIOD, RETURN_TYPE, OBJECT_ID |
| GivingTuesday 990 data lake per-object mirror, `https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml` (e.g. [Fidelity FY2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601389349301700_public.xml)) | Works. HTTP 404 for 19 of 856 harvest returns, all submitted in 2026 | Return content |
| ProPublica XML download (`/nonprofits/download-xml?object_id=`) | HTTP 403 (bot check), as already noted in `validation-wave3-report.md` | Not used. The ProPublica `/full` page URL is kept as a human-readable citation |
| IRS monthly XML ZIP batches (`{YYYY}_TEOS_XML_*.zip`) | Reachable in principle, but each is multi-GB and the server ignores HTTP range requests, so files cannot be fetched one at a time | Not used (proposal P-990-03) |

### 2.3 Return selection and parsing
- **Fiscal year** is the calendar year in which the tax period ends, the DAFRC convention. For example, Fidelity FY2025 is 7/2024–6/2025. The harvest keeps FY2022–FY2025 Form 990s. 990-EZ and 990-PF have no Part VII-B.
- **One return per tax period:** the highest OBJECT_ID, so an amended or duplicate submission supersedes the original. Example: Fidelity's FY2022 return appears in both the 2023 and 2024 indexes.
- **The XML is streamed with `xml.etree.iterparse`, and parsing stops after Schedule D.** That way, the very large Schedule I grant lists of the biggest sponsors are never downloaded in full. Only the parsed JSON is cached.

From each return the script reads:

| Section | Fields |
|---|---|
| Header | TaxYr, period dates, ReturnTs (submission time), filer |
| **Part VII Section B** | every `ContractorCompensationGrp`: name, `ServicesDesc`, `CompensationAmt`, and city/state from the address. Also `CntrctRcvdGreaterThan100KCnt` |
| Part IV line 6 | `DonorAdvisedFundInd` |
| Part IX | total of line 11g (other fees), 11b (management), 11f (investment management) and line 14 (information technology) |
| **Schedule D Part I** | `DonorAdvisedFundsHeldCnt`, `…ContriAmt`, `…GrantsAmt`, `…VlEOYAmt` |

### 2.4 Vendor normaliser (`normalize_vendor`, a pure function)
- **Ordered regex rules on the payee name only**, never on the services text. They map each name to `vendor_group`, `vendor_entity` and `vendor_category`. There are about 100 rules covering:
  - Ren entities;
  - DAF technology vendors: Foundation Source, Give Interactive, TIFIN, Foundant, NPact, Blackbaud/MicroEdge, CSuite, Crown/DonorFirst, Pinkaloo, Groundswell, Bonterra/CyberGrants/Network for Good, Benevity, Fluxx, SmartSimple, Kindsight, DonorPerfect;
  - payment processors: Chariot, PayPal/Braintree, Stripe, BlueSnap, DAF Direct;
  - grant administration (CAF America) and charity data (Candid);
  - enterprise software;
  - giving platforms and outsourced administrators: FrontStream, Mightycause, CiviCore, Gloo, Charitable Solutions, TASC;
  - financial-firm affiliates: FMR, Schwab, Vanguard Group, Goldman/Ayco, Morgan Stanley/Graystone, UBS, BofA/Merrill, and others;
  - investment consultants, technology consultancies, and audit firms.
- **Address guard.** A bare "Renaissance" or "Stellar" payee counts as Ren only when the payee city is Indianapolis, Ren's home at 8910 Purdue Rd and 8888 Keystone Crossing. This keeps out, for example, Renaissance Technologies.
- **Unmatched names** keep a cleaned legal name: no punctuation, no LLC/Inc/LP. They get a category from keywords in the services description and `match_method = cleaned_name`.
- Every Ren and DAF-vendor line was reviewed by hand (§3.2). No false positives were found.

### 2.5 Comparison with the graph
- Graph edges come from `relationship-graph-edges.csv` and `relationship-graph-edges-additions.csv`. The vendor side of each edge is passed through the same normaliser.
- The sponsor side is matched to a target EIN by distinctive-token overlap, plus a short alias table for labels that share no token with the legal name, such as "DAFgiving360" and "National Christian Foundation".
- 77 (vendor, sponsor) pairs matched.
- `sponsor_links_not_in_graph` counts rule-matched vendor and sponsor pairs with no matching edge. Graph labels for branded programs and private vendors do not resolve to EINs; the 50 unmatched labels are listed in the run summary.

### 2.6 DAFRC processing gaps (`gap_universe`, `gap_row`)
The gap check tests two sets of sponsor-years:
- **(a) Closed:** every fiscal year from a DAFRC "Assume Sponsor Closed" EIN's last panel row through FY2024 (82 EINs, 251 sponsor-years).
- **(b) Imputed:** every `Imputed` row in FY2021–FY2024 (850 rows).

For each, the script takes the newest Form 990 for the same fiscal year from the IRS index and parses Schedule D Part I. `gap_class` is assigned from the result. Submission timing comes from `ReturnTs`.

## 3. Results: P-VEN-06

### 3.1 Coverage
| Measure | Value |
|---|---|
| Target EINs | 250 (103 national + 147 largest others) |
| In the IRS e-file index with any Form 990 | 250 |
| With ≥1 FY2022–25 Form 990 parsed | **250** |
| Returns located / parsed / not yet mirrored | 856 / 837 / 19 |
| Parsed returns by fiscal year | FY2022 247; FY2023 249; FY2024 247; FY2025 94 (most FY2025 returns are not yet due or not yet mirrored) |
| Returns listing ≥1 contractor | 559 (278 list none) |
| Contractor lines / sponsors with any line | 1,985 / 174 |
| Contractors paid > $100k, as reported (`CntrctRcvdGreaterThan100KCnt`) | 17,935, of which only 1,985 (11%) are itemised; universities dominate |
| Sponsors with no Part VII-B line in any parsed year | 76 ($17.9bn FY2024 assets). Examples: BofA Charitable Gift Fund, Dechomai, Daffy, Endaoment, BNY Mellon CGF, Greater Horizons |

The 19 returns that are not mirrored include Vanguard Charitable FY2025 (OBJECT_ID 202621329349306657), Ayco Charitable FY2025, Endaoment FY2025 and NPT Charitable Asset Trust FY2025.

### 3.2 Vendor footprint for DAF-relevant vendors
Asset share is the share of the $313.9bn harvested universe, using DAFRC FY2024 assets for each sponsor paying the vendor in any year from FY2022 to FY2025. Compensation is the sum of the listed Part VII-B amounts across FY2022–FY2025 lines (source: `vendor-footprint-from-990.csv`).

| Vendor (group) | Sponsors paying | Σ compensation | DAF assets covered | % of universe | Fiscal years | Sponsor links new to graph |
|---|---|---|---|---|---|---|
| **Ren (incl. Stellar/iPhi)** | **25** | $117.07m | $48.37bn | 15.4% | 2022–25 | **15** |
| Foundant Technologies | 6 | $1.36m | $3.88bn | 1.2% | 2022, 2024 | 6 (vendor absent from graph) |
| Salesforce | 2 | $4.11m | $27.41bn | 8.7% | 2022–24 | 1 (Vanguard Charitable) |
| Bonterra (CyberGrants / Network for Good) | 2 | $25.72m | $0.52bn | 0.2% | 2022–25 | 2 (vendor absent from graph) |
| Mightycause | 2 | $9.08m | $0.54bn | 0.2% | 2022–25 | 2 |
| PayPal (incl. Braintree) | 2 | $4.56m | $0.27bn | 0.1% | 2022–25 | 2 |
| Excellence in Giving | 2 | $2.26m | $10.02bn | 3.2% | 2023–25 | 2 |
| Clearwater Analytics | 2 | $0.94m | $9.74bn | 3.1% | 2024 | 2 |
| Benevity | 1 (AOGF) | $163.18m | $0.27bn | 0.1% | 2022–25 | 0 |
| TASC | 1 (Give Back Foundation) | $57.50m | $0.01bn | 0.0% | 2022–25 | 1 |
| BlueSnap | 1 (AOGF) | $19.96m | $0.27bn | 0.1% | 2022–25 | 1 |
| Gloo | 1 (Servant Foundation) | $18.50m | $1.01bn | 0.3% | 2023–24 | 1 |
| Charitable Solutions | 1 (Dechomai Foundation) | $11.23m | $0.14bn | 0.0% | 2022–24 | 1 |
| CAF America | 1 (GS Gives) | $1.67m | $0.52bn | 0.2% | 2022–25 | 0 |
| NPact | 1 (AEF) | $0.67m | $9.48bn | 3.0% | 2022–24 | 0 (AEF edge exists) |
| Give Interactive | 1 (Foundation for the Carolinas) | $0.65m | $2.95bn | 0.9% | 2023 | **1** |
| SS&C Advent | 1 (Stifel) | $0.63m | $0.49bn | 0.2% | 2023–25 | 1 |
| Blackbaud | 1 (Greater Washington CF) | $0.33m | $0.40bn | 0.1% | 2023, 2025 | 1 |
| TIFIN Give | 1 (GiveClear) | $0.19m | $0.03bn | 0.0% | 2024 | 0 |
| Foundation Source, Chariot, CSuite, Fluxx, Candid, DAF Direct | 0 | — | — | — | — | — |

For context, financial-firm affiliates dominate the largest programs:
- FMR: **$545.7m** over FY2022–25, at Fidelity Charitable alone.
- Goldman Sachs/Ayco: $71.3m across 4 sponsors.
- Raymond James: $43.1m.
- Schwab: $29.8m.
- Morgan Stanley/Graystone: $23.3m across 4 sponsors.
- UST Global: $21.6m.
- Vanguard Group: $10.8m.

ICONIQ Capital, investment management and consulting, is paid by Fidelity Charitable, NPT and Silicon Valley Community Foundation, which together hold $117.9bn of FY2024 assets. None of these ICONIQ links is in the graph.

### 3.3 New vendor relationships, as Part VII-B payments not in the graph
- **National Christian Foundation pays Stellar Technology Solutions:** $1,201,477 (FY2022), $1,451,871 (FY2023) and **$2,495,829** (FY2024), for "software/consulting". It also pays Salesforce $1.36m in FY2024. The graph has only the Salesforce/Skuid edge (E164). Source: [990 FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513109349303201_public.xml).
- **The US Charitable Gift Trust pays Renaissance Administration LLC**, "donor serv/fd acct/tax": $3.68m, $3.74m and **$4.43m** (FY2022–24). This is an outsourced-administration relationship, not just software. Source: [990 FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533189349305673_public.xml).
- **The T. Rowe Price Program for Charitable Giving pays Ren PSG**, "technology": $211k–$301k a year over FY2022–25. Source: [990 FY2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202501959349302200_public.xml).
- **Ayco Charitable Foundation pays Stellar**, "software provider": $330,735 (FY2022) and $336,481 (FY2023). This is a second Goldman-family program on iPhi. Source: [990 FY2023](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202413109349304401_public.xml).
- **Servant Foundation paid Renaissance Philanthropic Solutions Group** "managed services" $828,787 in FY2022. By FY2024 the large technology payee is Gloo LLC ($14.0m, "data and technique services"). Sources: [FY2022](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202320469349302877_public.xml); [FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202500439349301825_public.xml).
- **Jewish Communal Fund paid Renaissance Acquisition Company** for "previous donor portal support": $417,742 in FY2023. This is consistent with the inferred Give Interactive migration in graph edge EA006. Source: [990 FY2023](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202410969349301036_public.xml).
- **Foundation for the Carolinas paid Give Interactive LLC** for "software": **$654,500** in FY2023. This is the only Part VII-B line for Give Interactive in the universe, and there is no FFTC edge in the graph. Source: [990 FY2023](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202433209349318318_public.xml).
- **Ren and Stellar at community and Jewish foundations:**
  - Community Foundation of Greater Des Moines: Stellar, then "Ren Technology Services", about $0.2m a year ([FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503149349303740_public.xml)).
  - "Jewish Federation of Greater …" (EIN 23-1500085; name truncated in DAFRC): Renaissance Administration, "investment administrative services", $0.50m in FY2025 ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601679349301260_public.xml)).
  - Greater Miami Jewish Federation: "Renaissance", Indianapolis, "foundation admin svc", $379k in FY2023 ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202421369349315457_public.xml)).
  - Smaller Stellar customers: Arkansas CF, Baton Rouge Area Foundation, Community Foundation of Acadiana, "Jewish Federation of Metropolitan …" (EIN 36-2167761), RSF Social Finance, the Community Foundation with EIN 58-1723645, and Bradley Impact Fund (RenPSG, "fund consulting").
- **Thrivent changed which Ren entity it pays:** Stellar at $278k–$281k in FY2022–24, then Renaissance Acquisition Company LLC at $479k in FY2025. Source: [990 FY2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202612669349300236_public.xml).
- **Foundant appears at 6 community foundations:** Columbus ($344,614, "operating platform services", FY2024, [990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513189349305651_public.xml)), Denver, Winston-Salem, the Ozarks, "The Community Foundation for Greater …" (EIN 58-1344646; name truncated in DAFRC) and "Community Foundation of the …" (EIN 58-2381589). Foundant is not a node in the graph.
- **Donation-processor sponsors pay platform vendors:**
  - AOGF paid Benevity $54.45m and BlueSnap $5.54m in FY2025 ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202641969349302754_public.xml)).
  - CAF America paid CyberGrants $8.29m in FY2025 ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202610489349300906_public.xml)).
  - Network for Good paid Bonterra Tech $2.49m in FY2024 ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513039349301631_public.xml)).
  - GiveClear paid TIFIN Give $185,921 in FY2024 ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533199349302978_public.xml)).
- **Already-known Ren payments were reproduced exactly:**
  - MS GIFT RenPSG: $14,930,249 for CY2024 ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503239349300435_public.xml)).
  - RCF Renaissance Administration: $19,225,546 ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543189349301959_public.xml)).
  - Also confirmed: Stifel, GS Gives, Cleveland, ImpactAssets, WaterStone (Christian Community Foundation Inc), and GS PWM (Stellar $390,398 in FY2022).

**Implication.** Part VII-B shows Ren as a broad but mostly small-ticket software vendor. 15 of its 25 payer sponsors pay it $100k–$500k a year. The large-ticket exceptions are outsourced administration contracts:
- RCF: $19.2m.
- MS GIFT: $14.9m.
- US Charitable Gift Trust: $4.4m.
- NCF: $2.5m, and rising fast.

By assets, Ren's 990-evidenced footprint is 15.4% of the top-250 universe. That is a **floor**, not a share (§6).

## 4. Results: P-MOR-03, DAFRC processing gaps
Source: `dafrc-processing-gaps.csv` (1,101 sponsor-years).

| Universe | FY | Sponsor-years | 990 reports DAF value | Count but blank value | 990 filed, no DAFs | No 990 in index |
|---|---|---|---|---|---|---|
| Closed (no DAFRC row) | 2020–22 | 87 | 0 | 0 | 78 | 9 |
| Closed | 2023 | 82 | **2** ($5.7m) | 0 | 66 | 14 (1 filed a 990-PF) |
| Closed | 2024 | 82 | **2** ($322.7m; 6,333 DAFs) | 0 | 63 | 17 (1 filed a 990-EZ) |
| Imputed row | 2021 | 56 | 1 | 13 ($1.00bn imputed) | 38 ($1.17bn imputed) | 4 |
| Imputed row | 2022 | 53 | 0 | 13 ($0.47bn imputed) | 36 ($2.23bn imputed) | 4 |
| Imputed row | 2023 | 28 | 2 | 11 ($0.28bn imputed) | 14 ($0.25bn imputed) | 1 |
| Imputed row | **2024** | **713** | **632** (imputed $95.86bn; filed **$90.98bn**) | 17 ($0.71bn imputed) | 57 ($0.25bn imputed) | 7 |

**Findings**
1. **Closed but still filing DAFs.** Four cases (§1). Donors Fund Inc reported 6,290 DAFs and $315,757,385 for FY2024; DAFRC's last filed value for it was FY2022, at $80.7m ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202600719349301710_public.xml)). All four returns were submitted between 2025-04 and 2026-04, so these are late filers, not processing misses.
2. **FY2024 imputation is mostly a timing artefact, and its direction is mixed.** For the 632 rows with filed values:

   | Segment | Rows | Imputed | Filed |
   |---|---|---|---|
   | National | 53 | $55.10bn | $52.75bn |
   | Community | 359 | $27.41bn | $25.04bn |
   | Single issue | 220 | $13.35bn | $13.20bn |

   - Filed values exceed imputed values in 210 rows and fall below them in the rest.
   - Largest falls: AEF (imputed $9.48bn, filed $8.38bn, [990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513219349310376_public.xml)), Dechomai Asset Trust (−$0.79bn), ImpactAssets (−$0.73bn), BofA CGF (−$0.37bn).
   - Largest rises: GS PWM (+$0.80bn), Signatry (+$0.39bn), RCF (+$0.28bn), Daffy (+$0.15bn).
   - 551 of the 632 are calendar-year filers (period 202412). Most were submitted in Nov 2025, at the extended deadline.
3. **Net effect on DAFRC's FY2024 total ($327.87bn):**
   - −$4.88bn from replacing the 632 imputed values;
   - −$0.25bn from dropping the 57 rows whose 990 reports no DAFs;
   - +$0.32bn from the two closed sponsors that filed DAFs.

   That is **−$4.80bn, or −1.5%**. The 17 rows with a count but a blank value stay unresolved, and 7 rows have no return. The account count falls by about 287k (−8%), almost entirely PayPal Charitable Giving Fund: 380,644 filed against 694,979 imputed ([990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533079349301308_public.xml)).
4. **Imputation against filed "no DAF" returns (FY2021–23: 88 rows, $3.64bn).** The largest cases are sponsors that had already terminated and moved their assets to other panel sponsors:
   - Jasper Ridge Charitable Fund: FY2022 imputed at **$1,493,085,967** ([final 990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202313149349304316_public.xml));
   - TIAA Charitable: FY2021 imputed at $261,839,418 ([final 990 with Schedule N to RCF](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202111979349301206_public.xml)).

   The same assets also appear at Fidelity, Schwab and RCF, so DAFRC FY2021 and FY2022 totals ($234.3bn and $229.7bn) are overstated by at least these amounts.
5. **Count without value (54 rows, FY2021–24).** Some filers report a DAF count in Schedule D Part I but leave the year-end value blank. Examples are Omaha Community Foundation (1,224 DAFs in FY2022, [990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202333179349309438_public.xml)) and Université de Montréal (714 DAFs in FY2024). For these rows DAFRC's imputation is a reasonable response, not an error.
6. **Data-entry flags (`implausible_daf_count_flag`):** 4 returns, kept but flagged:
   - Bayhealth Foundation: 7,823,222 DAFs with no value;
   - Fountain Hills Community Foundation: count equals value (80,829);
   - Osterman Community Foundation: 25,000 DAFs against $22,337;
   - Philanthropi: average under $100 per account. This is plausible for a micro-DAF app, but it is flagged anyway.

## 5. Comparison with the sponsor-mortality artefact tier
The mortality study (`sponsor-mortality-analysis.md` §2.3) found 15 "reporting artefacts", meaning a later 990 still reports DAFs. This pass is narrower: it requires a *same-fiscal-year* 990. On that test only the 4 closed sponsor-years above report DAFs in the year DAFRC treats as closed. The other artefacts report DAFs in a later year or under the panel-exit definitions. The two analyses agree on Donors Fund Inc (6,290 DAFs / $315.8m FY2024).

## 6. Limitations
- **Part VII-B lists only the five highest-paid independent contractors paid more than $100k.** A vendor paid less, or ranked sixth or lower, is invisible:
  - 235 of the 837 returns report more than five contractors above $100k.
  - Only 11% of the 17,935 reported engagements above $100k are itemised.
  - Absence from Part VII-B is therefore **not** evidence of no relationship. For example, Ren powers NPT's portal (graph E-edges), yet NPT lists no Ren line.
- **Not every vendor payment is reported as contractor compensation.** Software licences, hosting and platform fees are often booked in Part IX line 14 (IT) or as revenue shares, and do not appear here. Part IX totals are captured per return for context only. An affiliate's fees may sit under the parent's name, such as FMR or Schwab.
- **Vendor names are as filed.** The normaliser groups entities; it does not establish corporate ownership beyond the rule table. The Ren grouping (RenPSG, Renaissance Administration, Renaissance Acquisition Co, Ren Technology Services, Stellar/iPhi) follows the repository's existing treatment and the shared Indianapolis address.
- **Asset coverage figures add up the FY2024 DAF assets of the paying sponsors.** They show reach, not vendor revenue or market share. The paying year can differ from FY2024.
- **The mirror lags.** FY2025 is only partly available: 94 sponsors parsed, and 19 returns filed in 2026 are not yet mirrored.
- **DAFRC's data cut-off is not published**, so "processing gap" and "filing lag" are separated only by submission date (`submitted_before_2026` and `return_ts`).
- **Graph matching is heuristic.** "New link" counts can include relationships the graph records under a branded-program label. The named new links in §3.3 were checked by hand against the edge text.
- **No-invent rule.** Every value comes from the cited XML or DAFRC row. Blank means the field was absent, not zero.

## 7. Data dictionary

### `form990-contractors-harvest.csv` (1,985 rows; one per Part VII-B line)
| Column | Meaning |
|---|---|
| `ein`, `sponsor_name`, `sponsor_type` | DAFRC EIN, name and type |
| `tax_year` | IRS TaxYr (year the period begins) |
| `fiscal_year` | Year the period ends (DAFRC convention) |
| `tax_period_end` | TaxPeriodEndDt |
| `return_object_id` | IRS e-file OBJECT_ID |
| `contractor_name`, `services`, `compensation` | Part VII-B as filed (name lines joined; `ServicesDesc`; `CompensationAmt` in USD) |
| `contractor_city`, `contractor_state` | Payee address |
| `vendor_group`, `vendor_entity`, `vendor_category`, `match_method` | Normaliser output (`rule` or `cleaned_name`) |
| `source_url` | GivingTuesday mirror XML |
| `filing_page_url` | ProPublica `/full` page for the same object |

### `form990-returns-schedule-d-harvest.csv` (856 rows; one per located return)
| Column | Meaning |
|---|---|
| Universe fields | `selection`, `fy2024_asset_rank`, `fy2024_daf_assets` |
| Return identity | `fiscal_year`, `tax_year`, `tax_period`, `return_ts`, `return_object_id`, `return_type`, `amended_ind` |
| `xml_status` | `ok` or `http_404` |
| `contractors_listed`, `contractors_over_100k_cnt` | Itemised lines; reported count above $100k |
| `daf_ind_part_iv` | Part IV line 6 |
| `sched_d_*` | Schedule D Part I count, contributions, grants and year-end value |
| `part_ix_*` | Part IX line totals |
| `total_assets_eoy` | Total assets at year end |
| `dafrc_eoy_daf_assets_same_fy`, `dafrc_assets_source_same_fy` | DAFRC value and provenance for the same EIN and fiscal year (validation) |
| URLs | `xml_url`, `index_url`, `source_url` |

### `form990-harvest-sponsor-universe.csv` (250 rows)
Target list with `selection` rule, FY2024 assets and their source, returns found in the index, returns parsed, and fiscal years parsed.

### `vendor-footprint-from-990.csv` (910 rows; one per vendor group)
| Column | Meaning |
|---|---|
| `vendor`, `vendor_category`, `vendor_entities` | Normalised group, category, and the entities seen |
| `sponsors_paying`, `sponsor_names`, `sponsor_eins` | Distinct paying sponsors |
| `total_compensation`, `max_annual_compensation_one_sponsor`, `contractor_lines` | Sums across FY2022–25 lines |
| `sponsor_daf_assets_fy2024_dafrc` | Σ DAFRC FY2024 DAF assets of paying sponsors |
| `sponsor_daf_assets_latest_990_sched_d` | Σ latest parsed Schedule D year-end value of paying sponsors |
| `tax_years`, `fiscal_years` | Years with lines |
| `vendor_in_existing_graph` | 1 if the normalised vendor appears in any graph edge |
| `sponsor_links_not_in_graph`, `new_link_sponsors` | Rule-matched vendors only: paying sponsors with no matching edge |
| `raw_names_seen`, `services_seen` | Audit trail, truncated |

### `dafrc-processing-gaps.csv` (1,101 rows; one per tested sponsor-year)
| Column | Meaning |
|---|---|
| `gap_kind` | `dafrc_closed_no_row` or `dafrc_imputed_row` |
| `dafrc_fy`, `dafrc_operating_status`, `dafrc_end_of_tax_period`, `dafrc_eoy_daf_assets`, `dafrc_daf_accounts` | DAFRC row; blank for closed years |
| `last_filed_fy`, `last_filed_daf_assets` | Last positive filed DAFRC value before that year |
| `gap_class` | One of: `closed_but_990_reports_daf_value`, `imputed_but_990_reports_daf_value`, `*_990_reports_daf_count_value_blank_or_zero`, `*_990_filed_no_dafs`, `990_in_index_xml_not_mirrored`, `no_990_in_irs_index[_filed_990EZ/PF]` |
| `return_object_id`, `tax_period`, `tax_period_end`, `return_ts`, `submitted_before_2026`, `index_year`, `xml_status` | Return evidence |
| `other_return_type_same_fy` | A 990-EZ or 990-PF for the same fiscal year, if one exists |
| `filed_daf_*` | Schedule D Part I as filed |
| `implausible_daf_count_flag` | Count > 1m; count > 100k with no value; or under $100 per account |
| `value_delta_filed_minus_dafrc` | Filed value minus DAFRC value |
| `source_urls` | DAFRC dataset, IRS index and XML |

### Reproduce
```
# DIR holds index_2021..2026.csv (downloaded automatically with --fetch)
python3 scripts/mission_990_contractors.py --irs-dir DIR --cache-dir CACHE --fetch --task all
```
A full run with the network takes about 25 minutes for about 1,750 returns (8 threads). A re-run from the cache is offline and takes under a minute.
