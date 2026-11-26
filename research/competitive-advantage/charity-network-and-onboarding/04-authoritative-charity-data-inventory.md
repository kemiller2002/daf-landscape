# 04 - Authoritative charity data inventory

Status: research draft (2026-11-26). Not legal advice. Evidence classes per 01-research-methodology.md.

Machine-readable outputs: `data/charity-data-sources.csv` (30 sources, one row each) and `data/sources-DAT.csv` (36 cited sources). This note verifies, updates and extends the earlier inventories. It does not repeat them:
- `unbound/research/charity-sources/FEDERAL-SOURCE-INVENTORY.csv`, `INITIAL-SOURCE-VERIFICATION.md`, `FIVE-STATE-COMPARATIVE-FINDINGS.md`, `NATIONAL-STATE-SOURCE-MATRIX.csv` (2026-11-21; landing pages only, "no external datasets were ingested");
- `daf-landscape/research/mission-2026-11-14/b43n26-03-charity-data-terms-ai.md` (licence terms of Candid, Charity Navigator and four others; IRS as the public-domain baseline);
- `b50-02-state-registration.md` (state registry access log);
- `b40n1202-b43n26-03-non-bmf-recipients.md` (Schedule I recipients missing from the BMF);
- `direction-data-standards-interoperability.md` (the IRS exit from AWS).

What is new in this run: on 2026-11-26 I downloaded the current IRS bulk files (EO BMF regions 1-4, Pub 78, automatic revocation, 990-N, and the 990 XML indexes for 2025 and 2026), the OFAC SLS exports and the California AG "May Not Operate" CSV. I parsed them with stdlib Python, so the volumes, change rates and cross-file inconsistencies below are measured, not quoted.

## Summary

- **The whole US federal eligibility core is free, public domain and scriptable.** It is about 6.3 million rows and about 1.0 GB uncompressed per monthly snapshot: BMF, Pub 78, the revocation list, 990-N and OFAC. On top of that, the 990 e-file XML adds about 4.5 GB compressed per filing year (2025: 748,906 returns). No subscription is needed [VERIFIED-FACT, High; DAT-013..DAT-019]. This confirms UNB-CHAR-DEC-001: a first-party registry needs no Candid dependency for status data.
- **No single file establishes current eligibility.** Five of my measurements show why [VERIFIED-FACT, High; DAT-013/014/016]:
  - Pub 78 lists **0 of 237,380** 501(c)(3) group-ruling subordinates that are on the BMF.
  - 242,141 BMF 501(c)(3) EINs are absent from Pub 78.
  - 997 Pub 78 EINs are absent from the BMF.
  - **31,579** EINs with an *open* automatic revocation are still on the BMF, and 19,663 of them are in Pub 78. "Open" means that no row for the EIN has a reinstatement date on or after its latest revocation date; this order-independent definition is set out in the adversarial review response below.
  - For 22,366 of those 31,579 (71%), the BMF ruling month is later than the revocation date, which points to re-recognition. That leaves about 9,200 unexplained.
  - The revocation posting lag depends on the batch. All 38,826 August-2026 postings landed exactly 88 days after their effective date. The 14,294 other 2026 postings had p10/p50/p90 of 85/115/272 days. The lag is therefore batch-scheduled, not continuous.
- **Change rates are lumpy, so staleness rules must be asymmetric.** Revocation postings run at about 500-5,000 a month, but the August batch is about 39,000-40,000: 40,453 in Aug-2025 and 38,826 in Aug-2026. That is about 70% of a year's postings in one release. New BMF ruling dates run at about 6,800-13,700 a month in 2026 [VERIFIED-FACT, High; DAT-014/016]. Net BMF churn cannot be measured from one snapshot. Unbound must archive monthly to learn it [INFERENCE].
- **IRS page labels do not match the actual file timestamps.** The TEOS page says the revocation file was "Last updated Nov. 11" but the file is dated Nov 17. It says 990-N was posted "Nov. 9" but the file is dated Nov 23. It shows a 990 XML posting of "Oct. 21" but batch 10A is dated Nov 18. The 990 page's link list also omits files that exist on the server (`2022_TEOS_XML_02A.zip`, 1.41 GB). Freshness must come from the HTTP `Last-Modified` header, the content's maximum dates and the file hash, never from page text [VERIFIED-FACT, High; DAT-003/006].
- **The cadences now published** (IRS Pub 5891, 3-2026) [VERIFIED-FACT, High; DAT-004]:
  - Pub 78 and the revocation list: monthly, generally on the 2nd Tuesday;
  - 990-N: weekly, generally Monday;
  - determination letters (PDF/TIF images, 2014 onward only): monthly, 2nd Wednesday;
  - EO BMF: extracted monthly.
  - Determination letters have **no documented bulk download**, and TEOS search paths are robots-disallowed. Foundation classification from a letter is therefore a direct-evidence or manual item, not a feed.
- **OFAC lists have no schedule.** OFAC itself says changes "can be sporadic" and come "at an ever increasing pace". It offers delta files but advises a full refresh. The first page of recent actions showed 10 action dates in 26 days [VERIFIED-FACT, High; DAT-020/021]. Sanctions screening needs at least a daily full pull plus hash comparison, not a monthly cycle.
- **Licensing splits sharply** [VERIFIED-FACT, High]:
  - US federal data: public domain under 17 U.S.C. 105.
  - UK (CCEW, OSCR): Open Government Licence v3. OSCR adds "no direct marketing" and "not present as the Register".
  - Canada (CRA): OGL-Canada. Australia (ACNC): CC BY 3.0 AU, from search results only.
  - OpenCorporates: ODbL share-alike unless paid [VENDOR-CLAIM, Medium].
  - ProPublica: no resale, sublicensing or bulk republication [VENDOR-CLAIM, Medium].
  - Candid and Charity Navigator: licence-bound, including AI and calculation limits (b43n26-03).
  - State registries: no open licence found, except Colorado and Connecticut on Socrata (Public Domain).
- **State data cannot be automated broadly.** California's adverse-status CSV (29,536 rows, with FEIN, updated on the 1st and 3rd Wednesday) is the one high-value state feed verified here. NY, PA, WA and MA are manual-only behind CAPTCHA or robots rules (b50-02). This corrects one point: b50-02's "no bulk or open-data file" for California is right for the full registry but not for the adverse list [VERIFIED-FACT, High; DAT-022].
- **Public data can establish:**
  - IRS recognition and subsection;
  - public charity versus private foundation, and supporting-organization type where coded;
  - the church *code*, where a church applied;
  - IRS group-ruling central status;
  - posted automatic revocation and reinstatement;
  - 501(p) suspension and SDN listing;
  - filing activity.
- **Public data cannot establish:**
  - current existence or good standing in real time;
  - status of churches that never applied;
  - membership of a group-ruling subordinate. The IRS says only the central organization determines it (Pub 4573);
  - a governmental unit's EIN or status;
  - Type III functional integration where the code is generic;
  - 509(a)(3) control relationships with donors (needed for DAF disqualified-supporting-organization tests);
  - bank-account ownership;
  - foreign equivalency.

  These need direct evidence [INFERENCE, High].

## 1. US federal sources: verified detail

All of these files are on irs.gov or apps.irs.gov, whose robots rules allow the file paths. The table gives measured values for the current files.

| Source | Current file (Last-Modified) | Rows / size | Cadence (stated → observed) | History in file | Key fields for eligibility |
|---|---|---|---|---|---|
| EO BMF (eo1-eo4) | 2026-11-09 (page "posting 11/10/2026") | 1,984,891 rows, 0 duplicate EINs *within eo1-eo4*; 343 MB CSV. Do not add eo_pr/eo_xx: their 5,060 rows duplicate eo4 | "extracted monthly" → monthly | **None**. Cumulative current state; "the organization's name is removed ... including this file" on revocation | SUBSECTION, FOUNDATION (10 church … 21-24 SO type), AFFILIATION (6/8 central, 9 subordinate), GROUP (GEN), DEDUCTIBILITY, STATUS, RULING, FILING_REQ_CD |
| Pub 78 | 2026-11-11 | 1,437,288 EINs; 30 MB zip / 103 MB | monthly, ~2nd Tue | None | Deductibility code (PC, PF, POF, SO, SONFI, SOUNK, GROUP, LODGE, EO, FORGN, UNKWN) |
| Automatic revocation | 2026-11-17 (max posting 2026-11-11) | 1,248,282 rows / 1,228,742 EINs; 48 MB zip / 148 MB | monthly, ~2nd Tue | **Full since 2011** | Revocation date, posting date, reinstatement date |
| 990-N | 2026-11-23 (page: Nov 9) | 1,557,850 EINs (latest only); 94 MB zip / 287 MB | weekly, Mon | Latest only | Tax year, terminated flag (57,583 T), principal officer (personal data) |
| 990 e-file XML | index_2026 2026-11-18 | 2025: 748,906 returns, 4.46 GB zipped; 2026 YTD (to batch 10A): 516,019, 3.02 GB | monthly batches | 2019+ on IRS site | Schedule A (public-support basis, SO type), Part IV, Schedule R (related orgs), final-return flags |
| Determination letters | TEOS only | images | monthly, 2nd Wed | 2014+ (older via Form 4506-B) | Foundation classification, effective date, reinstatement addendum |
| 501(c)(3) revocations (for cause) | XLSX + IRB | small | per IRB | cumulative | IRB date governs; "TEOS ... may continue to show an organization as eligible ... for a short time" |
| 501(p) suspensions | HTML (reviewed 2026-06-28) | 9 orgs, no EINs | ad hoc | current | Name and city only |
| 1023-EZ approvals | XLSX per year | latest listed 2024 | quarterly extract, annual files | 2014+ | Officers, state of incorporation (personal data) |
| SOI annual extract | ZIP per filing year | latest: filed 2025 | annual | 2012+ | SOI-adjusted financials |

Sources: DAT-001..DAT-017. Evidence class VERIFIED-FACT, High, except the 990-N terminated-flag field mapping (INFERENCE from the Pub 5891 item list, Medium).

**History of e-file distribution.** The IRS stopped updating the AWS Open Data `irs990` dataset from 31 Dec 2021, and the registry now marks it Deprecated (`direction-data-standards-interoperability.md`). Distribution moved to `apps.irs.gov/pub/epostcard/990/xml/<year>/` with yearly index CSVs [VERIFIED-FACT, High; DAT-006]. The new channel has three hazards:
- Index schema drift: the 2022 index has no `XML_BATCH_ID` column; 2025 and 2026 do.
- Very large single ZIPs: 1.41 GB for 2022 batch 02A.
- An HTML link list that is not a complete manifest.

Ingestion should therefore drive from the index CSVs and probe batch names, not scrape the page [INFERENCE, High].

**Robots note.** irs.gov disallows `/charities-non-profits/tax-exempt-organization-search*` for all agents. That prefix also matches the bulk-download *page*. The data files themselves sit on apps.irs.gov, which has no robots restrictions. During this run, one request to `irs.gov/node/56981` was redirected onto that page. I used the copy once (DAT-003) and did not fetch it again. A production connector should hard-code the file URLs, which are stable and documented in Pub 5891, and never crawl TEOS [RECOMMENDATION].

## 2. Cross-file consistency: why "one source" fails

These were measured on the same-week files (DAT-013/014/016). All are VERIFIED-FACT, High, except where marked.

| Check | Result | Consequence |
|---|---|---|
| BMF 501(c)(3) subordinates (affiliation 9) in Pub 78 | **0 of 237,380** | Pub 78 absence is not ineligibility. Subordinate status depends on the central's GROUP listing plus the central's own roster (Pub 4573) |
| BMF 501(c)(3) not in Pub 78 | 242,141 (237,380 subordinates; 125,381 church-coded; 3,826 independents) | The BMF covers more recognized organizations, but it is not the reliance list |
| Pub 78 EINs not in BMF | 997 (842 PC) | Snapshot timing or removal skew: hold for review, never auto-pass |
| Open revocation (definition in the adversarial review response) but still in BMF | 31,579 (19,663 also in Pub 78) | For 22,366 (71%), the BMF RULING month is later than the revocation date. That points to re-recognition under a new determination (Rev. Proc. 2018-32 s4.06 subsequent listing), so the reinstatement field cannot be relied on alone [INFERENCE, Medium-High]. About 9,213 remain unexplained and go to review |
| Days from revocation date to posting (2026) | August batch: 88 days for all 38,826 rows. Other months: p10/p50/p90 = 85/115/272 (n=14,294) | Revocation by operation of law precedes publication by 3 to 9 months, depending on which batch carries it. This window is disclosed and cannot be eliminated |
| BMF NAME length | max 70 chars; 638,687 names are 35 chars or longer | Pub 78 names run to 150 chars. Match on EIN, never on name equality, and grant to the Pub 78/BMF legal name (CNV-GRT-003) |
| 990-N file | one row per EIN | Prior years are overwritten. Unbound must archive weekly to keep filing history |

## 3. Sanctions (OFAC)

- **Formats.** SLS serves:
  - legacy CSV: `SDN.CSV` 5.86 MB, plus `ALT`, `ADD` and `CONS_PRIM` (0.27 MB);
  - XML;
  - Advanced Sanctions Data Model XML: `SDN_ADVANCED.XML` 129 MB, `CONS_ADVANCED.XML` 4.6 MB;
  - customised datasets and an archive of delta files.

  The files are served with a `Digest: sha-256` header, and all were dated 2026-11-23 [VERIFIED-FACT, High; DAT-018/019].
- **Cadence.** There is no fixed schedule. FAQ 88 calls changes "sporadic" and warns of an "ever increasing pace". FAQ 90 confirms that public delta files exist. Delta-only pipelines can miss clerical updates that are published as UIDs only [VERIFIED-FACT, High; DAT-020]. RECOMMENDATION: poll at least every 6 hours. Compare the Digest header, take a full reload on change, and keep each version (UNB-EXT-004).
- **Scope.** OFAC covers US lists only. UN, UK OFSI and EU lists are separate sources, needed for foreign grantees under CNV-GRT-006/008 [INFERENCE, High]. The 501(p) list is a tax-deductibility overlay with names only. Pair it with SDN entries such as Holy Land Foundation [VERIFIED-FACT, High; DAT-008].

## 4. State sources

- **California AG.** The "May Not Operate or Solicit" CSV has 29,536 rows and carries FEIN, registry number and Secretary of State number:
  - by registration status: Revoked 23,516, Delinquent 3,936, Suspended 1,177;
  - by entity status: 907 rows are cease-and-desist orders.

  It is updated on the 1st and 3rd Wednesday. The real-time Registry Search Tool "controls" where the two differ [VERIFIED-FACT, High; DAT-022]. Use it as an adverse-signal feed with a 14-day staleness bound. It is not a registration-positive list.
- **New York, Pennsylvania, Washington, Massachusetts.** These are manual only: CAPTCHA, robots `Disallow: /`, or no dataset (b50-02 access log). Colorado and Connecticut are scriptable Socrata datasets marked Public Domain (b50-02).
- **The other 45 or so jurisdictions** remain "not verified" in `NATIONAL-STATE-SOURCE-MATRIX.csv`. This run did not change that.
- **State standing is a separate attribute.** Registration exemptions (churches, schools, small organizations; Texas largely has no registration) mean "not found" is never "non-compliant" (`FIVE-STATE-COMPARATIVE-FINDINGS.md` FIVE-001/009). State standing is a sponsor-policy input, not a federal eligibility fact [INFERENCE, High].
- **Corporate existence.** No free multi-state bulk source was verified. OpenCorporates aggregates registries, but the free tier is ODbL share-alike and capped by default at 200 requests a month and 50 a day. A paid licence removes share-alike [VENDOR-CLAIM, Medium; DAT-029]. Share-alike conflicts with a proprietary first-party registry, so OpenCorporates suits on-demand lookups under a paid licence, not bulk ingestion [INFERENCE, Medium].

## 5. Government units, schools and universities

Governmental units are valid DAF recipients as 170(b)(1)(A)(v) and 170(c)(1) donees [INFERENCE from statute, Medium; counsel to confirm]. They are mostly absent from the BMF and Pub 78: BMF foundation code 14 has only 360 records. Public directories give existence but **no EINs**:
- **Census 2022 government units file:** 11.5 MB ZIP, last modified 2023-08-24, quinquennial (DAT-033).
- **NCES CCD:** SY 2025-26 preliminary directory, annual (DAT-034).
- **IPEDS:** not verified this run.

EIN-to-government binding therefore needs direct evidence: a W-9 or IRS governmental-status letter, plus a bank-ownership check (CNV-PAY-002) [INFERENCE, High]. This matches the "foreign or government" bucket: 2,414 EINs and $596m of non-BMF Schedule I dollars (b40n1202 §0).

## 6. Group exemptions

The BMF exposes the structure:
- GEN in `GROUP`: 397,259 non-zero records;
- `AFFILIATION`: 6 or 8 = central (3,964 records), 9 = subordinate (393,222).

Pub 78 flags centrals with `GROUP` (2,465, plus combinations) and lists no subordinates [VERIFIED-FACT, High; DAT-002/005/016]. Pub 4573 is explicit: "The central organization that holds a group exemption (rather than the IRS) determines which organizations are included". Donors "may rely on central organization verification" [VERIFIED-FACT, High; DAT-011].

The public data can tell Unbound three things: a GEN exists, which central holds it, and whether an EIN is *coded* as a subordinate. It cannot tell Unbound whether a subordinate is still on the central's current roster. That needs a central-issued roster or confirmation letter. CNV-GRT-003's "group-exemption subordinates flagged" rule is necessary but not sufficient [INFERENCE, High].

## 7. International registries

| Registry | Access | Cadence | Licence | Verified? |
|---|---|---|---|---|
| Charity Commission (England and Wales) | Daily JSON/TSV extract; REST API with subscription key | daily / live | OGL v3. Must "acknowledge the source"; rate and quota limits may apply | API terms fetched (DAT-024). The download page returned 403 to the agent; the extract details come from a search summary (DAT-025) |
| OSCR (Scotland) | Free CSV, plus a 5-year annual-returns file; API beta (since May 2023) by application | daily | OGL v3 plus no direct marketing, no "claims to be the Scottish Charity Register", fixed attribution text | Fetched (DAT-023) |
| CRA (Canada) | open.canada.ca CKAN: yearly "List of charities" 1994-2025 (identification, core financial, qualified donees, directors CSVs) | annual (P1Y); 2025 modified 2026-11-18 | OGL-Canada | Catalogue API fetched (DAT-026). Other qualified donees are separate web lists (DAT-027) |
| ACNC (Australia) | data.gov.au CSV/XLSX | weekly (search result) | CC BY 3.0 AU; some AIS years CC BY 2.5 | **Not first-hand**: data.gov.au robots disallows all agents and returned 403 (DAT-028) |
| NGOsource (commercial ED) | Paid per determination; repository reissue | per certificate, which expires | Proprietary | Fees from third parties only (one reports a $250 reissue): VENDOR-CLAIM, Low (DAT-035) |

Foreign registries prove registration *in that jurisdiction*. They do not prove US 501(c)(3) equivalency. Equivalency stays deferred under CNV-GRT-008 and needs an equivalency determination or expenditure responsibility [INFERENCE, High].

## 8. Aggregators and websites

- **ProPublica Nonprofit Explorer.** A no-key JSON API built from the IRS BMF, SOI extracts and 990 XML/PDF. Its Data Terms bar resale, sublicensing and republishing "the raw data in its entirety" [VENDOR-CLAIM, Medium; DAT-030/031]. It is fine for analyst look-ups, but not as a product feed, because the primary IRS files are better and unencumbered.
- **Candid, Charity Navigator.** See b43n26-03. Candid needs written consent for AI/ML extraction and requires deletion on termination. Charity Navigator ratings may not be used "in any other calculation". Candid API list prices start at $2,750 a year (`direction-charity-ratings-integrations.md`) [VENDOR-CLAIM, High].
- **GivingTuesday 990 Data Infrastructure.** An XML data lake (via AWS) and data marts, useful for pre-2019 history. No licence text was found [VENDOR-CLAIM, Low; DAT-032]. Verify the terms before any retention.
- **Open990.** Not checked this run.
- **Charity websites.** Self-asserted and spoofable. Pages can carry prompt-injection text. Treat them as quoted untrusted data (CNV-AIO-002): never as an eligibility fact, and never as a bank-detail source [INFERENCE, High].

## 9. Minimal no-subscription ingestion set, with volumes

| # | Feed | Poll | Rows per snapshot | Uncompressed size | Change signal | Retention |
|---|---|---|---|---|---|---|
| 1 | EO BMF eo1-eo4 | daily HEAD; monthly change | 1.98M | 0.34 GB | Last-Modified + sha-256 | every monthly snapshot (diffs about 1-2% a month [ASSUMPTION, to be measured]) |
| 2 | Pub 78 | daily HEAD | 1.44M | 0.10 GB | same | every version |
| 3 | Auto-revocation | daily HEAD | 1.25M | 0.15 GB | same; max(posting date) | every version |
| 4 | 990-N | daily HEAD (weekly change) | 1.56M | 0.29 GB | same | every version (the file overwrites history) |
| 5 | 990 XML index + selected returns | weekly | about 0.75M returns a year | 4.5 GB zipped per year (full); far less if only Schedule A/R for grantees | new batch ID | returns for EINs in scope |
| 6 | OFAC SDN + Consolidated (advanced XML or CSV) | every 6 h | about 20k entries | 0.14 GB | Digest header | every version |
| 7 | 501(p) page, 501(c)(3) revocation XLSX | daily | under 1k | under 1 MB | content hash | every version |
| 8 | CA AG May-Not-Operate CSV | twice monthly (crawl-delay 10) | 29.5k | 3 MB | as-of date | every version |
| 9 (optional) | CCEW, OSCR, CRA | daily / daily / annual | country-scale | under 1 GB | per source | per licence; attribution stored |

Total core (1-4 and 6-8): about **6.3M rows and about 1.0 GB per monthly cycle**. Archived monthly, that is about 12 GB a year of raw snapshots before compression, or much less as row-level diffs [INFERENCE from measured sizes, High]. Measured change rates:
- revocation postings 53,000-66,000 a year (2022-2026), concentrated in an August batch of about 39,000-40,000 and a smaller March batch (about 5,300-6,500);
- reinstatement rows in total: 184,830 since 2011;
- new rulings in the BMF at about 6,800-13,700 a month (2026).

All are VERIFIED-FACT, High (DAT-014/016). The ruling counts are a lower bound, because revoked organizations have already been removed.

## 10. What public data can and cannot establish for DAF grant eligibility

| Question | Public source | Can establish? | Residual gap: direct evidence needed |
|---|---|---|---|
| IRS-recognized 501(c)(3)? | BMF SUBSECTION 03, Pub 78 | Yes, as of snapshot date (about 1-3 months lag) | Revocations not yet posted (3-9 month window); retroactive reinstatement |
| Public charity vs private foundation | Pub 78 PC/PF/POF; BMF FOUNDATION | Yes for most; "UNKWN" or "SOUNK" are not determinable | Determination letter (images, 2014+), or Schedule A |
| 509(a)(3) type (DAF disqualified SO tests) | BMF 21-24; Pub 78 SO/SONFI/SOUNK; 990 Schedule A | Partly: 15,043 records carry legacy code 17 and 14,137 Pub 78 rows say SOUNK | Type certification and **donor/advisor control of supported organizations**. This is not public; ask the grantee or advisor |
| Church status | BMF FOUNDATION 10 (293,661 records) | Only for churches that applied, or subordinates coded under a church GEN | Self-certification or central letter for non-applicant churches. The b40n1202 "religious-pattern, no IRS trace" bucket held $1.35bn |
| Group subordinate inclusion | BMF GEN and AFFILIATION | Coded membership only | Central's current roster or letter (Pub 4573) |
| Current legal existence | none at federal level; 990-N terminated flag; state corporate registries (manual) | No (weak signals only) | State good-standing certificate or registry look-up; charity attestation |
| State solicitation standing | CA adverse list; CO and CT open data | Adverse signals in a few states | Per-state manual look-up where sponsor policy requires it |
| Sanctions | OFAC SDN + Consolidated; 501(p) | Candidate matches | Human disposition of fuzzy matches (CNV-GRT-006) |
| Government unit | Census, NCES (no EIN) | Existence only | W-9 or governmental letter; EIN binding |
| Foreign charity | CCEW, OSCR, CRA, ACNC registers | Home-country registration | Equivalency determination or expenditure responsibility (CNV-GRT-008) |
| Payee bank account | none | No | Account-ownership verification or bank letter (CNV-PAY-002) |

The legal framing (DAF taxable distributions under IRC 4966 and the disqualified supporting-organization tests) is INFERENCE, Medium, for counsel review. It sits in REG's scope (05/06).

## 11. Proposed ingestion design: states, rules and failure behaviour

- **Snapshot record:** `source_key, url, http_last_modified, sha256, fetched_at, content_max_effective_date, row_count, schema_fingerprint, parser_version, status ∈ {fetched, validated, published, quarantined, superseded}`. It is append-only (UNB-CHAR-008/040).
- **Validation gates before `published`:**
  1. Row count within ±5% of the previous version. The revocation file is exempt in August; otherwise quarantine.
  2. Schema fingerprint is unchanged, else quarantine plus an alert.
  3. Max effective date does not regress.
  4. Header sha-256 matches the body.
- **Per-EIN federal status derivation.** A pure function of (BMF, Pub 78, revocation, 501(p), OFAC, posting dates) → `{recognized_current, recognized_unlisted_subordinate, not_listed_unknown, revoked_posted, reinstated, suspended_501p, sanctions_candidate, conflict}`.
  - `conflict` covers cases such as revoked-without-reinstatement but present in BMF, or Pub 78 present but BMF absent.
  - `conflict` maps to *hold for review*, never auto-pass (CNV-GRT-003 fail-safe).
- **Freshness SLAs per source:**
  - BMF, Pub 78, revocation: stale after 45 days without a new version;
  - 990-N: 14 days;
  - OFAC: 24 hours;
  - CA list: 21 days.

  When a source is stale, approval falls back to "pending refresh" for adverse-sensitive checks. Informational changes (name or address) never block payment (CNV-GRT-003).
- **Never infer negatives from absence** in Pub 78, state lists or the 990 index (UNB-CHAR-016, FIVE-001).

## Implications for Unbound

1. **The status-data layer is not a moat.** Any entrant can rebuild Ren or Chariot's IRS-derived directory from about 1 GB a month of public-domain files [INFERENCE, High]. The barrier sits in the direct-evidence layer: group rosters, church attestations, supporting-organization control certifications, governmental EIN binding, bank-ownership proofs and foreign equivalency. Incumbents have accumulated that evidence over years.
2. **Unbound's edge is correctness at the boundaries.** Measurable discrepancies (about 9,200 unexplained open-revocation EINs on the BMF, 997 Pub 78-only EINs, the 3-9 month posting window) are things a deterministic, archived, multi-source reconciler can surface and incumbents' single-feed checks may not [HYPOTHESIS, testable against the Schedule I recipients in b40n1202].
3. **Rights are clean for the core.** Federal files carry no licence friction for AI use, caching or retention (b43n26-03). Keep UK, Canadian and Australian data with their attribution metadata. Exclude ProPublica, Candid, Charity Navigator and OpenCorporates' free tier from any shared store (CNV-TEN-001, CNV-GRT-004).
4. **Ratified decisions.** No conflict found. One refinement to CNV-GRT-003: "latest TEOS/Pub78 ... posting dates" should be read as the file's `Last-Modified` and content dates, not the IRS page label. Those differed by up to 4 weeks in this run.

Candidate requirement refinements (one line each):
- UNB-EXT-001 (refine): Ingest BMF, Pub 78, revocation and 990-N by fixed file URL, versioned by `Last-Modified` and sha-256. Never crawl TEOS, which is robots-disallowed.
- UNB-CHAR-011 (refine): Derive freshness from file and content dates, not page labels. Store per-source SLAs (BMF/Pub 78/revocation 45 days; 990-N 14 days; OFAC 24 hours; CA 21 days).
- UNB-CHAR-015 (refine): Model August mass revocation postings and the 3-9 month revocation-to-posting window (88 days in the August batch) as a disclosed risk window on approval evidence.
- NEW: Cross-file conflict states (revoked-not-reinstated but in BMF; in Pub 78 but not in BMF) SHALL produce a review hold, not a pass or fail.
- NEW: Group-subordinate eligibility SHALL require central-issued roster evidence with an expiry. BMF coding alone is insufficient (Pub 4573).
- UNB-EXT-004 (refine): Poll OFAC SLS at least every 6 hours with Digest comparison, full reload, and versioned retention. Add UN, OFSI and EU lists for foreign grantees.
- UNB-EXT-016/018 (refine): Exclude ODbL share-alike and no-resale aggregator data from registry storage unless a paid licence is recorded in the SharedStoreRegister.
- NEW: Archive 990-N weekly and BMF monthly, because the IRS files overwrite history.

## Adversarial review response (ADVA-04/05/06/16)

- **One definition (ADVA-05).** An EIN is *open-revoked* if no row for it has a reinstatement date on or after its latest revocation date. The rule does not depend on row order or tie-breaks. On the 2026-11 files it gives:
  - 1,063,397 open-revoked EINs;
  - 31,579 of them on the BMF, 19,663 of them in Pub 78.

  Earlier figures came from different tie-break rules: 31,616/19,699 (04), 19,695 (05) and 19,689 (ADVA). 04 now uses only the new figures; 05 and 06 should adopt them. [VERIFIED-FACT, High]
- **Re-recognition (ADVA-06): upheld.** For 22,366 of the 31,579 (71%), the BMF ruling is later than the revocation date. Apply the Rev. Proc. 2018-32 s4.06 subsequent-listing rule deterministically and review only the residual 9,213. [INFERENCE, Medium-High]
- **The 88-day lag (ADVA-16): upheld.** It is an August-batch artefact; other months run 85/115/272 days (p10/p50/p90). The summary, section 2 and section 10 have been revised.
- **BMF duplicates (ADVA-04).** 04 already used eo1-eo4 only, with 0 duplicates. The 5,060 duplicates arise only when eo_pr/eo_xx are added; table note added. Figures unchanged: 237,380 subordinates, 1,659,108 501(c)(3)s.
- **Script location.** References now point to `scripts/dat_irs_*.py` and `data/dat-irs-*-output.txt`.

## Open questions / evidence gaps

- **BMF churn.** Additions and removals per month need two archived snapshots. Wayback was unreachable from this environment. Start archiving now.
- **The ~9,213 open-revocation BMF EINs with no later ruling.** Are they data defects, or reinstatements not reflected in RULING? Sample them against TEOS manually (TEOS is robots-blocked for automation).
- **CCEW and ACNC first-hand verification.** Both were blocked (403, robots). Confirm the extract tables, cadence and licence manually.
- **GivingTuesday and Open990 terms.** Not found or not checked.
- **IPEDS and Census unit files.** Contents and identifiers not opened. Is there a public EIN crosswalk for governmental units? (Not found.)
- **501(p) list.** It has no EINs or dates. Confirm whether the IRS publishes structured data, or whether the OFAC SDN is the operational source.
- **State registries.** 45+ jurisdictions remain unverified (`STATE-REGISTRY-VERIFICATION-QUEUE.csv`). Of the remainder, only CA (adverse list), CO and CT are confirmed scriptable.
- **Analysis scripts.** The measured counts come from `scripts/dat_irs_stats.py` and `scripts/dat_irs_join.py`, with outputs in `data/dat-irs-stats-output.txt` and `data/dat-irs-join-output.txt`. The figures given in the adversarial review response come from the order-independent definition there; `dat_irs_join.py` still uses the earlier tie-break and should be updated to match.
