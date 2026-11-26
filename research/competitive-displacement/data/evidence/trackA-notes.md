# Track A: charity information sources beyond prior research

Accessed 2026-11-26. Public sources only. I made no logins, signups or outreach. The machine-readable output is `trackA-sources.csv` (38 rows, same folder). It extends `04-authoritative-charity-data-inventory.md` and `b43n26-03-charity-data-terms-ai.md`; it does not repeat them. Candid and Charity Navigator are already covered in detail by b43n26-03 (AI/ML consent clause, calculation ban, deletion on termination). I found nothing that changes that work, so they get no new rows.

## 1. Decision summary

### Free, commercially usable and bulk (machine-readable, no subscription)

| Source | Evidence |
|---|---|
| Consolidated Screening List | Downloaded: 26,339 rows, 11 lists from Commerce, State and Treasury, updated daily, no key |
| UK Sanctions List | OGL v3; CSV and XML |
| FAC single audits | Free api.data.gov key; CSV 1998 onward; carries **EIN and UEI** |
| USAspending | No key; full database snapshot |
| SAM.gov exclusions extract | Daily. D&B-sourced fields carry "no bulk dissemination" terms |
| Colorado business entities | Public Domain; explicit dissolved and revoked statuses |
| New York active corporations | 4.29M rows; 288,708 not-for-profit corporations |
| GLEIF | CC0 |
| Wikidata | CC0; 17,428 items carry an EIN |
| Ireland charity register | CC BY 4.0, weekly |
| New Zealand charity register | CC BY 3.0 NZ, OData with no key |
| IRS written determinations | Public domain, but redacted |

### Licence-restricted (redistribution, commercial use or AI reuse)

| Source | Restriction |
|---|---|
| OpenSanctions | CC BY-NC 4.0. "Any use inside a for-profit business requires a data licence". Compliance screening counts as commercial use even without revenue. Embedding the data in a product needs a reseller licence. Prices are by quote only; a 2022 article gave EUR 595/month, which is dated |
| ProPublica NPE | **CC BY-NC-ND 3.0 US** plus "commercial users may be subject to additional use fees". This is stronger than prior research's "no resale" framing |
| GivingTuesday 990 data | **ODbL 1.0 / DbCL 1.0**. A public derivative database must be shared alike. This resolves prior DAT-032's "no licence found" |
| MSRB EMMA | Commercial redistribution is restricted. The continuing-disclosure feed cost $45,000/yr on the 2017 price list |
| OCD (Catholic directory) | Proprietary |
| BBB WGA, ECFA, CoF Standards, Fiscal Sponsor Directory | No reuse licence found. Treat as link-out or manual evidence |
| PACER | Fees rise to $0.12/page from 2027-01-01 |

No public term found for any new source names AI or ML use specifically. The exceptions are OpenSanctions, which binds all commercial use, and BBB's separate AskGive.org AI terms.

### Vetting role

**Can support automated vetting** (deterministic flags after EIN binding):
- CSL, UK list, UN list and EU FSF (sanctions and export control);
- SAM exclusions;
- FAC going-concern and material-weakness flags;
- Colorado-style corporate status;
- IRS 990 bulk files (already in prior research).

**Informs only:**
- USAspending, SAM entity, NASCO, CourtListener/PACER, EMMA;
- community-foundation, ECFA and fiscal-sponsor directories;
- foreign registries (registration does not establish equivalency);
- GLEIF and Wikidata (crosswalks).

**Not useful as a feed:** PayPal Giving Fund, Chariot, Bonterra (closed systems; competitor benchmarks), Open990 (unreachable) and CF Insights.

## 2. Corrections and extensions to prior research

1. **UK sanctions.** Prior research (04 §3, UNB-EXT-004) says to add "UN, OFSI and EU lists". The **OFSI Consolidated List closed at 09:00 GMT on 2026-01-28** and is no longer updated. The FCDO UK Sanctions List is now the sole UK source. It changes the identifier scheme: new designations get only a UK Sanctions List Unique ID, and the legacy OFSI Group ID is kept only for earlier designations. Pipelines keyed on Group ID will silently miss new designations.
2. **US screening beyond OFAC.** The trade.gov CSL adds BIS (Entity List 3,427 rows, Denied Persons 1,596, Unverified, Military End User), State (ITAR-debarred 801, ACN 105) and the OFAC non-SDN lists, in one keyless file. As of 2026-10-01 some ACN-program persons appear only on the SDN list. Read the CSV with a raised field-size limit, because some fields exceed 131 KB.
3. **ProPublica.** The licence is CC BY-NC-ND 3.0 US, with fees possible for commercial users. The evidence is a search-index copy of the legacy API page, which now 301-redirects; the current API doc has no licence text. The Data Store terms add: no charging for access, no stand-alone redistribution, no sublicensing or resale. Classed VENDOR-CLAIM, Medium.
4. **GivingTuesday.** Its licence is ODbL/DbCL, the same share-alike conflict as OpenCorporates' free tier. The GivingTuesday *website* ToS (2021) separately bars commercial exploitation and scraping of the site.
5. **Open990.** On 2026-11-26 it was unreachable: TLS mismatch on open990.org and HTTP 530 on open990.com. Mark it unavailable, though this does not prove it has shut down.
6. **IRS 990 bulk files.** No 2026 discontinuation notice was found. An Aspen Institute comment letter (Nov 2025) reports a roughly one-month outage of the 990 downloads page, with the PDF bulk ZIPs still unavailable while XML had resumed. This supports the prior "archive every batch" rule.
7. **Group rulings.** USCCB GEN 0928 is a concrete case of the roster gap in prior §6. The IRS letter (latest dated 2025-09-30) says the IRS does *not* verify subordinate inclusion. Donors verify via the commercial Official Catholic Directory or the USCCB. Entries marked with an asterisk have their own letters. The donee must supply the OCD cover page and listing page.
8. **State registration.** About 40 states plus DC require registration. The NASCO/MRFP **Single Portal is paused**, with "little indication that they will resume" (Loeb, Nov 2026, on the 2026 NASCO conference). There is no national registration dataset, and NASCO's annual report is a self-described sample. New signal for DAF policy: Georgia's Secretary of State fined an unregistered DAF $100,000 and issued an emergency cease-and-desist (per Loeb's summary of the NASCO report).
9. **Single-audit threshold.** The threshold is $1,000,000 for fiscal years beginning on or after 2024-10-01 (previously $750,000). The source is secondary and eCFR was not read. FAC is the rare public source that joins **EIN to UEI**, and it adds a `additional_eins` table.

## 3. Identity-resolution findings (measured)

- **USAspending** recipient search returns UEI and DUNS but no EIN. A keyword search for "American National Red Cross" returned 30 recipient rows across the parent, child and recipient levels.
- **State corporate registries** (NY, CO) carry no EIN. The binding has to be made by name, address and registered agent.
- **Wikidata.** 17,428 items have an EIN; only 369 have both an EIN and an LEI.
- **GLEIF.** Coverage of charities is sparse. The American National Red Cross has LEI 4EDKCQ2ZCBIECQ6VUQ69 (ACTIVE/ISSUED).
- **Churches.** Churches need not apply for recognition (IRC 508(c)(1)(A)), so the BMF and Pub 78 omit non-applicants. ECFA (2,700+ members) and the OCD are the only structured third-party lists found for them, and neither is open-licensed.

## 4. URLs and what each establishes

**Sanctions and exclusions**
- open.gsa.gov/api/exclusions-api: Exclusions API v4; key tiers 10 and 1,000/day; extract up to 1M records; D&B terms.
- open.gsa.gov/api/sam-entity-extracts-api: public, FOUO and Sensitive extract levels; daily exclusions extract naming.
- trade.gov/consolidated-screening-list: the 11 lists, file URLs, daily 5 AM ET refresh, official-publication disclaimer.
- data.trade.gov/.../consolidated.csv: downloaded, 19.1 MB, Last-Modified 2026-11-26.
- gov.uk/government/publications/the-uk-sanctions-list: formats, OGL v3, updated 2026-11-26.
- gov.uk/guidance/moving-to-a-single-list-...-28-january-2026: OFSI list closure.
- opensanctions.org/licensing, /docs/commercial/exemption, /faq/commercial/pricing-tier: CC BY-NC, commercial licence types, who is exempt.

**Federal funding and audits**
- fac.gov/api, /api/dictionary, /data/download: API key requirement, 11 endpoints, EIN/UEI and finding fields, CSV coverage 1998-2015 and 2016 to present.
- api.usaspending.gov (tested) and the GitHub README: no key, database snapshot.

**Courts and litigation**
- wiki.free.law CourtListener v4 overview: rate limits (5/min, 50/hr, 125/day), commercial agreements available.
- courtlistener.com/help/api/bulk-data: quarterly files, Public Domain Mark.
- pacer.uscourts.gov pricing; wawb.uscourts.gov notice: fees and the 2027 increase.
- irs.gov/written-determinations: weekly redacted 6110 releases.

**Municipal bonds**
- msrb.org Terms (2026-01-01), Data Access Fee Policy, Subscription Agreement, 2017 price list: restrictions and prices.

**Directories and religious evidence**
- give.org/terms-of-use: no data licence; framing and logo restrictions.
- developer.bbb.org/terms-of-use: the IABBB API covers business data only.
- usccb.org tax-and-group-ruling and the 25-1009 memo: GEN 0928 mechanics.
- ecfa.org/members and About: 2,700+ members.
- cof.org/community-foundation-standards: "more than 500" accredited community foundations.
- cof.org/cfinsights/results: FY24 data from 445 respondents.
- fiscalsponsordirectory.org facts page: 376 sponsors and 20,566 projects (May 2024).

**State charity regulation and corporate registries**
- loeb.com Nov 2026 NASCO summary: Single Portal paused; DAF enforcement.
- nasconet.org annual reports: sample-only compilation.
- georgia.gov/bulk-corporations-data: $1,000 full database, $100 account, $500 monthly.
- in.gov, oklahoma.gov and maine.gov: bulk fees (from search snippets).
- data.ny.gov n9v6-gdp6 and data.colorado.gov 4ykn-tg5h: measured counts and statuses.

**Foreign registries**
- odata.charities.govt.nz: live OData collections (NZ).
- data.gov.ie package_show (register-of-charities-in-ireland): CC-BY-4.0, weekly, XLSX dated 2026-11-15.

**Open identifiers**
- gleif.org lei-data-terms-of-use: CC0, free, no endorsement implied.
- query.wikidata.org: P1297 counts.

**Payment networks and competitors**
- paypal.com PPGF nonprofit certification policy (2025-09-10): eligibility and exclusions.
- docs.givechariot.com: EIN search and the `claimed` flag.
- Bonterra Nonprofit Hub FAQ and vetting PDF: ownership verification, subsection choice, ACH as a separate step.
- givechariot.com "grants that go nowhere good" (VENDOR-CLAIM): EWS bank-matching anecdote.

**990 aggregators**
- projects.propublica.org/datastore/terms: no-redistribution terms.
- 990data.givingtuesday.org/data-use-license: ODbL/DbCL.
- givingtuesday.org/terms-of-service: website ToS.

## 5. Gaps and blocked items

- **Blocked hosts.** These returned 403, robots blocks or challenges: Florida Sunbiz, the Ireland regulator site, the NZ site (Cloudflare), the de Gruyter article and the ECFA terms page (404). cfo.gov is outside the session's allowed network, so the EIN-display controller alert was not read; it needs to be allowed in network settings to verify.
- **Unverified.** The UN XML URL returned 404 here. The EU FSF token requirement comes from third-party documentation. Current MSRB prices and the OCD licence and price are UNKNOWN. The TX, KY and MN bulk fees are UNKNOWN. The CSL API key requirement is UNKNOWN.
- **Not attempted.** I did not open Benevity Causes Portal data exposure, beyond the prior terms work. I did not read the National Network of Fiscal Sponsors member list.
