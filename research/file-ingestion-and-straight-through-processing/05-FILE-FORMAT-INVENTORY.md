# 05 — File format inventory

Research package: [file ingestion and straight-through processing](README.md) (2026-11-26). Evidence ids `FIE-*` resolve in [`data/file-ingestion-2026-11/evidence.csv`](../../data/file-ingestion-2026-11/evidence.csv). Classification: **CONFIRMED** (public source), **INFERRED** (reasoned from confirmed facts), **PROPOSED** (innovation, not observed practice). The machine-readable inventory with licensing, public samples and parser risk is [`formats.csv`](../../data/file-ingestion-2026-11/formats.csv). Recommendations are for a new US DAF platform in general; a specific product's decisions belong in its own repository.

## Summary

1. **The DAF data surface is narrow and US-centric.** Seven groups of formats cover almost all real flows:
   - CSV/XLSX for migration and bulk import
   - JSON for the API
   - NACHA for outbound grants plus returns and NOCs
   - BAI2 now and camt.053/054 later for bank reporting
   - IRS TEOS datasets (CSV, pipe-delimited, ZIP)
   - OFAC SLS (XML or CSV)
   - PDF and images for documents

   Nearly everything else (ISO 20022 pacs, X9.100-187, DTCC, FIX, corporate actions, pricing feeds) reaches a sponsor through its bank or custodian. a new DAF platform should consume the outputs of those systems and not take part in those networks.
2. **US payment infrastructure is now ISO 20022.**
   - CHIPS switched on 2024-04-08 (FIE-B-027).
   - Fedwire switched on 2025-07-14 (FIE-B-026).
   - FedNow has been ISO 20022 from its launch (FIE-B-029).
   - Swift ended MT/MX coexistence for cross-border instructions on 2025-11-22 (FIE-B-028).

   Corporate bank reporting has not caught up. BAI2 is still the US default, and I found no sunset (FIE-B-035, inferred). **a new DAF platform should design one canonical bank-transaction model, ship BAI2 first, and make camt.053/054 a conditional adapter.**
3. **Nacha's 2026 fraud-monitoring rules already apply.** Phase 1 took effect 2026-03-20 and Phase 2 on 2026-06-19; some Nacha pages say 06-22 (FIE-B-034). A sponsor that sends grant ACH credits is a non-consumer Originator, so it now needs risk-based processes to detect credits originated under false pretenses. Grant-payee verification, bank-detail change controls and an audit trail are therefore compliance features, not optional extras.
4. **The best numbers on electronic versus manual cost come from healthcare.** In the 2024 CAQH Index:
   - Remittance advice costs $6.24 manual versus $3.03 electronic (FIE-B-002).
   - Claim payment costs $5.59 versus $3.24 (FIE-B-003).
   - Status inquiries cost $18.18 versus $3.68 (FIE-B-004).
   - Average medical-provider cost is $7.93 manual versus $3.39 electronic (FIE-B-001).
   - Even after ~25 years under a HIPAA mandate, only **89%** of remittances are fully electronic (FIE-B-005).

   AP shows the same pattern. The average invoice costs $9.40, best-in-class costs $2.78, and exception rates run 9% for best-in-class against 22% for others (FIE-B-008/009, inferred). **Plan for a permanent 5–20% exception tail** (FIE-B-066, proposed). An AI-native product should compete on how cheaply it handles that tail, not on pretending the tail does not exist.
5. **Email is the riskiest ingestion channel.** BEC losses reached $2.77B in 2024 (FIE-B-019). Only ~17.6% of surveyed senders publish DMARC p=reject (FIE-B-020, inferred). Authorized email ingestion is acceptable for documents. It must never be enough on its own to change payment instructions.

---

## Formats

The table gives the short version. Full rows are in B-formats.csv.

| Format | Governing body / spec access | Licensing | DAF-relevant use | Parser risk | Recommendation |
|---|---|---|---|---|---|
| CSV (RFC 4180) | IETF, public | Free | Migration, bulk import, BMF, OFAC, CA registry, custodian files | Medium | **Initial** |
| IRS pipe-delimited | IRS, public | Free | Pub 78, auto-revocation, 990-N | Low–med | **Initial** |
| Fixed-width | Per producer | Free layouts | NACHA, OFAC .FF, legacy feeds | Medium | **Conditional** (NACHA is required in any case) |
| JSON + JSON Schema | IETF / json-schema.org | Free | Public API, webhooks | Low | **Initial** |
| XML + XSD | W3C | Free | OFAC Advanced XML, IRS 990 XML, ISO 20022 | Medium (XXE, size) | **Initial** (hardened streaming) |
| ISO 20022 camt.052/053/054 | ISO/RA; free catalogue; bank MUGs | Free; MyStandards account | Bank statements and notifications | Medium (bank variance) | **Conditional** |
| ISO 20022 pain.001/002 | ISO/RA | Free; bank certification | Grant payment initiation and status | Medium | **Conditional** |
| ISO 20022 pacs.008/004 | Fed/TCH/Swift, participant specs | Participant-only | Interbank only | n/a | **Not applicable** |
| NACHA ACH | Nacha; free dev guide; Rules $75/$110 | ODFI agreement | Grant ACH, returns, NOC | Medium | **Initial** |
| BAI2 | BAI; bank type-code variants | Free spec (historically) | Prior-day / intraday reporting | Medium | **Initial** |
| MT940/942 | Swift | Member docs; bank guides | Non-US banks | Medium | **Deferred** |
| OFX/QFX | FDX (OFX royalty-free); QFX Intuit | Free / Intuit | Consumer bank downloads | Medium | **Deferred** |
| X9.100-187 ICL | ASC X9 (ANSI webstore) | Paid | Check image exchange | High | **Not applicable** (consume bank output) |
| Lockbox files | Bank-proprietary | Contract | Mailed check gifts | High | **Conditional** |
| X12 823 / 820 | X12 | Paid ($1,200/yr dev seat) | EDI lockbox, B2B remittance | High | **Deferred** |
| XBRL | XBRL Intl | Free | None (990 is MeF XML) | n/a | **Not applicable** |
| IRS 990 MeF XML | IRS; schemas via e-Services | Free (registration) | Grantee due diligence; sponsor 990 data | High | **Conditional** |
| XLSX | ECMA-376 / ISO 29500 | Free | Uploads, exports | Med–high | **Initial** (values only, no macros) |
| PDF | ISO 32000 | Free (inferred) | Receipts out; documents in | High for extraction | **Initial** |
| TIFF | Adobe TIFF 6.0 | Free | Lockbox / RDC images | Low–med | **Conditional** |
| JPEG/PNG/HEIC | ISO / W3C / MPEG | HEVC patents (inferred) | Phone photos of checks and forms | Medium | **Initial** (normalize HEIC) |
| ZIP | PKWARE APPNOTE | Free | IRS/OFAC bulk files | Medium (bombs, traversal) | **Initial** |

### 1.1 Delimited, fixed-width, JSON and XML

- **CSV (initial).** CSV will carry migration data from incumbent DAF platforms and from sponsors' spreadsheets. The IRS EO BMF is CSV: `eo1-4.csv` by region and `eo_xx.csv` by state, cumulative, sorted by EIN, 1,984,891 records, posted 2026-11-10 (FIE-B-043). The CA AG registry is also CSV (FIE-B-052).
  - Risks: dialect variation, encodings, Excel stripping leading zeros from EINs and ZIP codes, and locale-dependent dates.
  - Proposed approach: publish an **a new DAF platform CSV profile** (UTF-8, header row, ISO-8601 dates, decimal amounts as text, plus a manifest or trailer with a row count and amount totals, borrowing the NACHA control-total idea). Accept other dialects through a tolerant reader that ends in human-confirmed column mapping.
- **Fixed-width (conditional).** NACHA files are fixed-width, so a new DAF platform needs a declarative layout engine regardless. OFAC still publishes `.FF` files (FIE-B-051). Legacy custodian feeds are often fixed-width (inferred).
- **JSON + JSON Schema (initial).** This is the API contract. Represent money as decimal strings, never binary floats. Version the schemas.
- **XML + XSD (initial).** Needed for OFAC Advanced XML, IRS 990 XML and ISO 20022. The parser must disable DTDs and external entities and must stream, because 990 ZIPs reach many GB (FIE-B-047).

### 1.2 ISO 20022 and US adoption

- **Fedwire Funds:** one-day cutover from FAIM on **2025-07-14**. Fedwire settles more than $4.7T per day (FIE-B-026).
- **CHIPS:** live on **2024-04-08**. Day one carried 555,345 payments worth $1.81T (FIE-B-027).
- **FedNow:** ISO 20022-native. Specs are on Swift MyStandards and need a free account (FIE-B-029). Q1 2026 volume was 2.73M payments worth ~$271B. 1,725 institutions (19.7% of US FIs) were live in Q1 2026, and more than 1,800 by July 2026 (FIE-B-025).
- **Swift:** cross-border coexistence ended on **2025-11-22**, with 97% of instructions already in ISO 20022. camt.052/053/054 became available in SR2025 (FIE-B-028). I could not confirm a formal MT940 retirement date for corporate reporting on swift.com.
- **Catalogue:** iso20022.org provides MDRs and XSDs free of charge (FIE-B-030). Banks still apply their own usage guidelines.

**What this means for DAFs.** A sponsor never sends or receives pacs messages directly. Its bank does that. Two things matter to the sponsor:
- **Richer wire and instant-payment remittance data.** Fedwire's ISO 20022 fields can carry donor identity and fund references on inbound gift wires. a new DAF platform should map fields such as `RmtInf` and `Dbtr` from camt.054 or from the bank API.
- **camt.053/054** gradually replacing BAI2.

Recommendation:
- **camt.053/054:** conditional, adopted bank by bank.
- **pain.001:** conditional, for sponsors whose bank prefers one payables format.
- **pacs:** not applicable.

### 1.3 NACHA ACH (initial)

- **Spec and licensing.** The file is fixed-width ASCII with 94-character records. The ACH Developer Guide is free. The full Operating Rules cost $75 for members and $110 for non-members in 2026 (FIE-B-031). Banks add their own header and origination requirements (FIE-B-031).
- **Control totals.** Batch (8) and file (9) control records carry entry/addenda counts, an entry hash (the sum of 8-digit RDFI routing numbers, last 10 digits kept) and debit/credit totals. Files are blocked in groups of 10 records (FIE-B-032, inferred from the dev guide). **This is the model to copy for a new platform's own batch imports.**
- **Returns and NOCs.**
  - Return reason codes span R01–R85. Some codes are retired or reserved, and vendor counts differ (FIE-B-033).
  - NOC/COR codes C01–C13 must update grantee bank records under change control.
  - The authoritative list is only in the paid Rules.
- **2026 rules** (FIE-B-034):
  - Phase 1 (2026-03-20) covers ODFIs, plus non-consumer Originators, TPSPs and TPSs with at least 6M ACH entries in 2023.
  - Phase 2 (2026-06-19, or 06-22 on some pages) covers all other non-consumer Originators.
  - RDFIs must also monitor incoming credits.
  - Most DAF sponsors fall under Phase 2. a new DAF platform should give them payee-verification evidence, change-of-bank-detail controls, velocity and anomaly checks, and an exportable audit trail.
- **Network scale.** 35.2B payments worth $93T moved in 2025. Same Day ACH carried 1.4B payments worth $3.9T, up 16.7% (FIE-B-024).

### 1.4 BAI2 (initial) and SWIFT MT940/942 (deferred)

- I found no BAI sunset. Bank material positions camt.053 as the successor to BAI2 and MT940 (FIE-B-035, inferred). Banks add proprietary type codes and 88-continuation text, so each bank needs its own type-code mapping table.
- MT940/942 matter only for non-US banks. Defer.

### 1.5 OFX/QFX (deferred)

OFX 2.3 is published by FDX, and OFX 2.2 carries a royalty-free license (FIE-B-039). It is a consumer and small-business aggregation format, and institutional DAF sponsors will not rely on it. QFX is Intuit's proprietary variant.

### 1.6 Checks: X9.100-187, RDC and lockbox

- **X9.100-187-2021** ("Electronic Exchange of Check and Image Data") is a paid standard. Its companion is TR 47-2022 (FIE-B-036). **Not applicable.** Sponsors deposit through their bank's RDC or wholesale lockbox, and a new DAF platform consumes what those services produce.
- **Lockbox files.**
  - Formats are bank-proprietary data files (often derived from BAI) plus image files (often TIFF/JPEG).
  - No public samples were found.
  - **Conditional:** build configurable per-bank mappings with control totals, and route low-confidence remittance OCR to review.
- **X12 823** is the EDI lockbox format, with DEP/BAT loops and a 997 acknowledgement (FIE-B-038). **X12 820** carries remittance. Both require an X12 license; the developer license is $1,200 per year per seat, and commercial redistribution needs a commercial license (FIE-B-037). **Defer both.**
- **Why checks still matter.** The 2024 US check count fell to 9.2B, but the average check is now $2,653 (FIE-B-023). Checks remain the method most often targeted by fraud: 63% of organizations reported check fraud in 2024 and 58% in 2025 (FIE-B-018). The median cost to issue a check is $2.01–4.00, versus $0.26–0.50 for ACH (FIE-B-017).

### 1.7 XBRL and IRS 990

- **XBRL is not applicable.** Since the Taxpayer First Act, the 990 family must be e-filed for tax years beginning after 2019-07-01 (FIE-B-050), and the format is **MeF XML/XSD**.
- **MeF schemas and business rules** are distributed by tax year through the e-Services Secure Object Repository. Access requires registration, and each release includes DIFF files (FIE-B-049).
- **Public 990 XML** is now published as monthly ZIPs on IRS.gov. The latest XML posting was 2026-10-21 (FIE-B-047). The **AWS Open Data copy is deprecated**, and the IRS stopped updating it at the end of 2021 (FIE-B-048).
- **Recommendation:** conditional. Read 990 XML for grantee enrichment in phase 2. Sponsor 990 filing (Schedule D, Part I covers DAFs) stays with the sponsor's preparer or transmitter, and a new DAF platform exports the needed aggregates as CSV/XLSX.

### 1.8 Office, document and image formats

- **XLSX (initial).** Read cell values only. Reject `.xlsm` and macros. Ignore formulas and use cached values with a warning.
- **PDF (initial).**
  - Outbound: receipts and statements, archived as PDF/A.
  - Inbound: classify, then extract, then send to human review.
  - Scanned and text PDFs need separate handling, and inbound files must be sanitized because PDFs can carry JavaScript.
- **TIFF (conditional).** Only for lockbox or RDC images.
- **JPEG/PNG/HEIC (initial).** Normalize HEIC at ingestion and strip EXIF data (PII, location).
- **ZIP (initial).** Required for IRS and OFAC files. Guard against zip bombs, path traversal and Zip64 edge cases.

### 1.9 Custodian and brokerage data

| Source | Spec public? | Delivery | DAF use | Recommendation |
|---|---|---|---|---|
| DTCC (DTC, DWAC, ACATS, NSCC) | Participant docs only | SPA screens, MQ, CCF; ISO 15022 | Stock gifts land at the sponsor's custodian; DWAC needs custodian approval through a FAST agent (FIE-B-054) | **Not applicable** (track gift lifecycle from custodian data) |
| Schwab | No (contract) | Schwab Data Delivery, Advisor Center download, server SFTP, plus APIs (FIE-B-055) | Pool positions and transactions | **Conditional** |
| Fidelity Wealthscape Integration Xchange | No (contract) | Bulk inbound/outbound feeds, APIs, FIX; 200+ third-party integrations (FIE-B-056) | Same | **Conditional** |
| BNY Pershing NetX360 / Wove | No (contract) | Daily files via FTP/email (archived page), Integration Hub APIs (FIE-B-057, inferred) | Same | **Conditional** |
| Envestnet/Yodlee, Orion, Addepar, Black Diamond | No (commercial) | APIs and files | Aggregators can stand in for N custodian integrations | **Conditional** (one aggregator rather than N custodians; no specs retrieved this session) |
| FIX | Yes (CC BY-ND) (FIE-B-040) | Session protocol | Liquidating gifted securities | **Deferred** |
| ICE / Bloomberg pricing | No; licensed, display/non-display and redistribution fees (FIE-B-058) | Feeds | Gift-date valuation, pool NAV | **Deferred** (use custodian valuations to avoid redistribution liability) |
| Corporate actions (MT564 / seev) | ISO catalogue free | Swift | Pool holdings | **Not applicable** (custodian handles them) |

### 1.10 Government and charity datasets

| Dataset | Format | Cadence and latest posting | Notes |
|---|---|---|---|
| EO BMF | CSV (state, region, international) | Monthly; posted 2026-11-10; 1,984,891 records | Code sheet `eo-info.pdf`; address is the HQ filing address (FIE-B-043) |
| Pub 78 | Pipe-delimited ASCII in ZIP | Monthly; posted 2026-11-11 | No DBA names (FIE-B-044) |
| Auto-revocation | Pipe-delimited ZIP | Monthly; posted 2026-11-11 | Known date errors for revocations from 2020-04-01 to 07-14 (FIE-B-045); encode as a rule |
| 990-N e-Postcard | Pipe-delimited ZIP | Monthly; posted 2026-11-09 | (FIE-B-046) |
| 990-series XML | XML in monthly ZIPs | Latest posting 2026-10-21 | Packaging varies by year (FIE-B-047) |
| OFAC SLS | Advanced XML, XML, CSV, FF, PDF, deltas | Event-driven | Legacy CSV is 4 files joined on ENT_NUM; remarks spill into SDN_COMMENTS.CSV; PIP/DEL retired ~Sept 2023 (FIE-B-051) |
| CA Registry of Charitable Trusts | CSV plus data legend | Annual; next update was scheduled for 2026-04-01 | Incomplete for non-CA entities; no API (FIE-B-052) |
| NY Charities Bureau | Not researched in depth this session | n/a | Treat as manual lookup until verified |
| Candid / GuideStar | JSON APIs | Licensed | Charity Check from $2,750 (contact sales); license restricts use (FIE-B-053) |

**Recommendation.** At launch, run scheduled pulls of BMF, Pub 78, revocation, 990-N and OFAC. Load them into versioned snapshot tables in PostgreSQL with diffing between snapshots. a new DAF platform must be able to decide grantee eligibility from public IRS and OFAC data alone. Candid is an optional, sponsor-paid enrichment.

---

