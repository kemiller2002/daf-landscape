# Beneficium public-data acquisition economics: evidence notes

Status: research evidence, last reviewed 2026-11-27. This builds on the competitive-displacement reports 02-05 and `charity-data-sources.csv` (68 sources), and on charity-network reports 04, 06 and 20. It does not repeat them. Registers:

- [beneficium-data-sources.csv](../registers/beneficium-data-sources.csv): 29 sources. `existing_register_ref` links each row to its `charity-data-sources.csv` key.
- [beneficium-dataset-sizing.csv](../registers/beneficium-dataset-sizing.csv): 38 assumptions.

The Beneficium repository was not accessible, so this work lives in daf-landscape.

## 1. Answer in brief

- **Storage is small.** The full federal core is about 0.9-1.0 GB per monthly cycle, uncompressed. The 990 XML adds about 4.5 GB a year compressed (measured 4.46 GB for 2025). Ten years of everything, compressed, comes to about **190 GB base** (range 35 GB to 1.2 TB, depending on whether full snapshots or diffs are kept, and whether website and NPPES snapshots are kept). The structured database is about **10 GB in year 1** (17 GB with indexes). These figures are well below the 1 TB raw / 150 GB DB that charity-network 20 assumed. Storage cost is immaterial either way.
- **Bandwidth.** The base is about **46 GB a year, or 3.8 GB a month** (range 0.85-12 GB a month). The IRS republishes whole files, so bytes do not spike in August even though revocation rows do (38,826 rows in August 2026).
- **Workload is set by connector count, not by data volume.** Base connector maintenance runs from **76 h/yr** (public directory, 5 connectors) to **296 h/yr** (continuous regulatory monitoring, 13 connectors) and **820 h/yr** (automated verification evidence, 26 connectors). Pipeline operations add about 150 h/yr. All of this is incurred with zero customers.
- **The BMF is about 1.98M rows, not 1.9M.** It holds 1,984,891 rows (about 1.69M are 501(c)(3)). A registry that keeps revoked organizations resolvable needs about 3.2M EIN entities.
- **Most of the value beyond the BMF comes from four free IRS files plus sanctions.** These are Pub 78, the revocation list, 990-N, OFAC/CSL and, for depth, the 990 XML. State registries, websites and directories cost the most per unit of value.

## 2. Sampling log (bounded, authorized)

All downloads went into a new empty directory, `.../scratchpad/beneficium-sample/`. Parsers ran with `python3 -I` from a separate `.../scratchpad/beneficium-scripts/` directory. **All samples were deleted after measurement.** Total downloaded: about 185 MB (cap 300 MB). No file exceeded 60 MB.

| File | Method | Bytes | Result |
|---|---|---|---|
| `irs-soi/eo1.csv` (2026-11-09) | `curl -s URL \| head -c 62914560 > eo1.csv` (no Content-Length or Range on irs.gov/pub/irs-soi) | 49,166,596 (complete) | 281,266 rows, 281,266 unique EINs, 28 columns; c3 236,941; non-zero GEN 44,011; AFFILIATION 9: 43,480; c3 foundation codes 15: 98,011, 16: 65,922, 10: 39,596, 04: 22,883 |
| `irs-soi/eo_de.csv` | same | 1,893,636 | 10,595 rows (DE only), same 28 columns. State files are a partition of eo1-eo4 |
| `data-download-pub78.zip` (2026-11-11) | `curl --max-filesize 62914560` | 30,306,480 zip; 103,029,917 member | 1,437,288 records |
| `data-download-revocation.zip` (2026-11-17) | same | 47,625,777 zip; 148,494,106 member | 1,248,282 records; 184,830 reinstated; 2026 postings Jan 118, Feb 2,319, Mar 5,318, Apr 1,077, May 1,452, Jun 766, Jul 684, Aug 38,826, Sep 1,195, Oct 463, Nov 902 (reproduces charity-network 06) |
| `2025_TEOS_XML_10A.zip` (posted 2025-11-19) | same | 56,507,372 zip; 298,238,712 uncompressed (5.4x) | 9,836 returns (990 5,085; 990EZ 3,044; 990PF 1,443; 990T 264); avg 30.3 KB/return; Schedule I in 1,137 990s with 7,574 recipient rows; 990-PF grants in 1,011 PFs with 15,097 rows; Schedule A 6,359; Schedule R 1,040; **8 distinct `returnVersion` values** (2022v5.0 to 2024v5.2); tax years 2024: 9,018, 2023: 705, 2022: 113 |

Cross-file checks on the NE region (eo1 states: NY, NJ, MA, CT, ME, NH, RI, VT):

- **Pub 78 vs BMF presence.** 216,145 Pub 78 rows; **161 are not in BMF eo1**.
- **Name agreement.** After normalizing to A-Z0-9, 215,926 names are identical, 36 differ only by truncation and **22 are materially different**. The raw string mismatch rate is 53%, so normalization is mandatory.
- **eo1 c3 not in Pub 78.** 23,987 eo1 c3 EINs are absent from Pub 78, but **only 721 are not group subordinates**.
- **Open revocations.** **4,894 eo1 EINs (1.7%) still appear in the BMF with an unreinstated latest revocation row.**
- **National extrapolation (x7.06 = 1,984,891 / 281,266).** About 1,140 Pub 78-not-in-BMF EINs (prior national count 997), about 155 name conflicts and about 34.5k open-revocation-on-BMF EINs (prior 31,614). The factor assumes the NE is representative (Medium).

Parse timing, measured with `time` on a 4-vCPU sandbox:

- XML byte-scan of 9,836 returns: 1.5 CPU-s.
- BMF + Pub 78 + revocation parse (2.98M rows): 4.1 CPU-s.

HEAD/Range probes only (no download):

- **990 XML ZIPs.** Every linked ZIP was probed with `curl -sI`, and the per-year totals were summed:

  | Year | Compressed size |
  |---|---|
  | 2019 | 3.009 GB |
  | 2020 | 3.386 GB |
  | 2021 | 3.716 GB |
  | 2022 | 4.012 GB (includes the unlinked `2022_TEOS_XML_02A.zip`, 1,408,196,885 B) |
  | 2023 | 4.294 GB |
  | 2024 | 4.391 GB |
  | 2025 | 4.464 GB |
  | 2026 to batch 10A | 3.025 GB |
  | **Total** | **30.3 GB** |

  Probing 2021/2022 months 02A-12A returned 302 (absent), except 2022 02A.
- **990 index CSVs.**

  | Year | Size |
  |---|---|
  | 2019 | 52.9 MB |
  | 2020 | 50.7 MB |
  | 2021 | 74.8 MB |
  | 2022 | 72.2 MB |
  | 2023 | 77.5 MB |
  | 2024 | no Content-Length |
  | 2025 | 93.1 MB |
  | 2026 | 64.4 MB |

  The 2021-2024 ZIPs and indexes all carry Last-Modified 2025-03-06, which means they were republished.
- **990-N ZIP.** 93,849,500 B (2026-11-23). It was not downloaded because it exceeds the cap.
- **OFAC** (`curl -r 0-0`, since HEAD gives no length): `SDN_ADVANCED.XML` 129,071,029 B; `CONS_ADVANCED.XML` 4,580,958 B; `SDN.CSV` 5,855,269 B; `CONS_PRIM.CSV` 268,568 B. All are Last-Modified 2026-11-23.
- **Trade.gov CSL.** `consolidated.csv` is 19,083,418 B, Last-Modified 2026-11-27 02:30 GMT. Note that **HEAD returns 404 while a ranged GET returns 206**.
- **FAC full CSVs** (`app.fac.gov/dissemination/public-data/gsa/full/`, all regenerated 2026-11-26 about 07:30 GMT): 3.35 GB in total.

  | File | Bytes |
  |---|---|
  | federal_awards | 1,342,358,613 |
  | notes_to_sefa | 732,336,414 |
  | passthrough | 558,817,697 |
  | general | 272,618,620 |
  | findings_text | 260,951,817 |
  | corrective_action_plans | 112,674,820 |
  | findings | 68,082,099 |
  | additional_eins | 4,784,988 |
  | additional_ueis | 1,836,610 |
  | secondary_auditors | 428,696 |

- **CA AG May-Not-Operate CSV.** 3,167,253 B, as of 2026-11-18.
- **Other files.**

  | File | Size | Date |
  |---|---|---|
  | NPPES monthly full ZIP | 1,130,479,129 B | 2026-11-03 |
  | NPPES weekly increment | 6,373,117 B | |
  | IPEDS HD2024.zip | 1,088,372 B | |
  | NCES CCD school directory ZIP | 13,242,150 B | |
  | Census 2022 government units ZIP | 11,459,763 B | 2023-08-24 |

- **Not reachable or not sized.**
  - USAspending files host: the listing returned 404. Third-party mirrors report a 145-200 GB zipped dump (Data Rescue Project; UCSB). An ad hoc listing attempt was refused by the session's safety classifier and was not retried.
  - SAM extracts: an account and API key are required, so these were not attempted.
  - IRS SOI extract URLs tried returned 404.
  - The TEOS bulk page links only 3 data files. **No bulk determination-letter ZIP was found.**
  - The NY/CO Socrata CSV exports were not sized, because a full export would exceed the cap. The NY dataset Last-Modified is 2026-11-26.

**Extrapolation methods.**

- BMF bytes = eo1 bytes/row x full row count.
- National conflict counts = NE counts x 7.06.
- 990 uncompressed = compressed x 5.4 (one batch).
- Annual grant edges = sample rows x 76.1 (748,906 / 9,836). This is Low confidence, because 10A is a small October batch.
- Annual bytes = file size x pulls per year at the observed cadence.
- Compressed CSV size uses about 3.2x, the Pub 78 and revocation zip ratios (ASSUMPTION for the BMF, which is served uncompressed).

## 3. Per-source findings (what is new versus the existing register)

- **BMF (BDS-001/002).** This re-confirms the prior inventory: no history, no tombstones, monthly. The state files are **redundant**. The page gives no length and does not support Range, so freshness must come from Last-Modified plus a hash.
- **Pub 78 / revocation / 990-N (BDS-003/004/005).** These are the only IRS files with ETag. Pub 78 and BMF agree to within about 0.07% on presence after the subordinate rules are applied. Names need normalization. The revocation list is the only IRS source with built-in history (2011+).
- **990 XML (BDS-006/007/008).**
  - The IRS site now holds 2019+ only, and pre-2019 years are not there. A 10-year archive must therefore start accumulating now or use third-party mirrors (licence check needed).
  - The highest maintenance burden in the federal set comes from multiple schema versions per batch, unlinked files, a bulk republication and the late-2025 page outage.
  - Grant edges: Schedule I typically carries recipient EINs, while 990-PF grants usually carry names only, so identity resolution, not acquisition, is the cost.
- **Determination letters (BDS-009).** These come per EIN and on demand only. They are essential evidence for new organizations and reinstatements, but they are not a bulk feed.
- **Historical BMF (BDS-010).** NCCS archives are ODC-BY 1.0, and attribution must be kept. They are useful for a one-time backfill and for back-testing change rates, as charity-network 06 already did.
- **Sanctions (BDS-012/013).** Both are free and keyless. The CSL is a superset feed for US lists but **HEAD fails**, so connectors must use GET/Range. OFAC changes on about 110-130 days a year.
- **SAM (BDS-014/015).** These need an account and API key. The rate limit is 10 requests/day without a role and 1,000 with one. The exclusions extract is a daily full file; the entity public extract is monthly. Sizes are UNKNOWN.
- **FAC (BDS-017).** Keyless CSV, regenerated nightly. Beneficium needs only general, findings and additional_eins/ueis (about 347 MB). This is the only bulk EIN-UEI bridge.
- **USAspending (BDS-016).** Do not ingest the dump. Pull recipient-filtered awards by UEI via the keyless API.
- **States (BDS-018..021).** The CA adverse CSV is the only verified bulk state feed. NY and most others are search-only. Corporate registries carry no EIN.
- **Religious, fiscal-sponsor and NPPES sources (BDS-023/025/026).** These are evidence or low value, not feeds. Directories carry no reuse licence. NPPES is 1.13 GB a month for marginal eligibility value.
- **Websites (BDS-027).** These are the costliest per unit of value. Use them only in the automated-verification scenario.

## 4. Sources needed per scenario

| Scenario | Sources (BDS) | Connectors (base) | Connector h/yr low / base / high |
|---|---|---|---|
| S1 Public directory only | 001, 003, 004, 005, 011 (+022 derived) | 5 | 44 / 76 / 172 |
| S2 + historical filings | S1 + 006/007, 010 (backfill) | 7 | 92 / 172 / 364 |
| S3 + grant relationship intelligence | S2 + 008 (+016 optional) | 8 | 132 / 232 / 484 |
| S4 Continuous regulatory monitoring | S1 + 012, 013, 014, 017, 018 + 3 state registries (0-10) | 13 (11-20) | 152 / 296 / 1,168 |
| S5 Automated verification evidence | S4 + S3 + 009, 015, 019, 021, 023, 024, 025, 026, 027, 029 | 26 (20-33) | 432 / 820 / 2,304 |

Add **pipeline operations of 50 / 150 / 300 h/yr** in every scenario (BDZ-037). That gives base totals of about **226 h (S1), 446 h (S4) and 970 h (S5)** a year. Per connector this is roughly 15-32 h/yr, which sits below the 40 h per connector-year used in RC-06. The difference comes from simple federal files. The state and website connectors cost more than 40 h each.

## 5. Zero-customer maintenance workload and schema-drift evidence

The connectors, archive and monitoring run whether or not any sponsor exists. That is S1 76 h, S4 296 h and S5 820 h, plus about 150 h of operations. Drift evidence for 2021-2026, all VERIFIED-FACT from probes or the prior register (BDZ-038):

- The 990 bulk distribution moved from AWS to TEOS, and file naming changed from `download990xml_YYYY_N` to `YYYY_TEOS_XML_MMA`.
- All 2021-2024 ZIPs and indexes were republished on 2025-03-06.
- An unlinked 1.41 GB ZIP exists.
- index_2024 serves no Content-Length.
- The 990 page had an outage of about a month in November 2025, and batch 2025_10A was posted late (2025-11-19).
- IRS page dates disagree with file Last-Modified.
- OFAC moved to the Sanctions List Service, which gives no HEAD length.
- The trade.gov CSL HEAD returns 404, and the CSL host changed in the past.
- The UK OFSI list closed on 2026-01-28.
- Eight e-file schema versions appear in one monthly batch.

This works out to **about 1-6 breaking events a year (base 3)** across federal sources, plus annual XML schema releases. The design implications are a quarantine state, hash- and Last-Modified-based freshness, and source-silence alerts (charity-network 06 section 7).

## 6. Function ownership proposal

| Function | Owner | Rationale |
|---|---|---|
| Acquisition of public sources | **Beneficium** | Shared, sponsor-neutral public evidence; zero-customer cost borne once |
| Normalization and schema-drift handling | **Beneficium** | Same |
| History retention (raw archive, temporal records) | **Beneficium** | IRS keeps no history; only the first archiver has it |
| Identity resolution (EIN, UEI, name, successor candidates) | **Beneficium** proposes; **Unbound** confirms merges that affect a sponsor's grants | Candidate links are shared; merges that move money are decisions |
| Regulatory monitoring (change detection, sanctions delta rescreen) | **Beneficium** emits events; **Unbound** fans them out to the grants affected | Separation of facts from per-sponsor impact |
| Verification (automated evidence assembly, status checks at approval/release) | **Unbound** using Beneficium evidence | Grant-time control sits in grant processing |
| Sponsor eligibility decisions and overlays | **Sponsor** (configured in Unbound) | Legal responsibility under 4966/4967 sits with the sponsor |
| Human investigations (adverse findings, sanctions potential matches) | **Unbound** operations under sponsor policy; sponsor decides the outcome | Human judgement and accountability |
| Charity representative verification | **Unbound** (Transitus if it hosts charity identity) | Account and authority, not a public fact |
| Payment enrollment | **Transitus**/payment provider | Rail-specific |
| Bank ownership verification | **Payment provider** (account validation) with Transitus orchestration | Requires bank data and vendor contracts |
| Fraud investigation | **Unbound** with payment provider; sponsor informed | Spans identity and payments |
| Commercial data (Candid, OCD, paid state bulk) | **Sponsor** or **Unbound** licence per use; **never** pooled in Beneficium | Redistribution limits (report 03) |
| Support (charity and sponsor questions about data) | **Unbound** front line; **Beneficium** answers source questions | Charities are not Beneficium users |

## 7. Caveats and open items

- **SAM extract sizes, USAspending and determination letters are UNKNOWN.** SAM extract sizes and USAspending scope remain UNKNOWN, and so does the bulk availability of determination letters.
- **Seasonality is unmeasured.** BMF change rates rest on one measured month (2026-06 to 2026-07). Two snapshots from different months were not re-derived here, because only one current BMF was available.
- **Grant-edge counts are uncertain.** They rest on one small batch.
- **Licence status.** Licences for state lists (CA "unclear"), directories and website snapshots need counsel review. The federal sources are public domain.
- **What is new in this session.** Several items are new here and could be added to project memory:
  - the CSL HEAD-404 behaviour;
  - FAC full-file sizes;
  - 990 per-year compressed totals;
  - the 8-schema-version observation.

  All come from this session's probes.
