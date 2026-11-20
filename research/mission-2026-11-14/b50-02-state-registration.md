# b50-02: State charitable-registration status of DAF sponsors (public registry data)

**Date:** 2026-11-20 · **Task:** b50-02 (new direction: sponsors' state charity registration)

**Outputs**
- [`data/mission-2026-11-14/state-registration-2026-11-20.csv`](../../data/mission-2026-11-14/state-registration-2026-11-20.csv): 700 rows (100 sponsors × 7 states). The data dictionary is in §5.
- [`scripts/mission_state_registration.py`](../../scripts/mission_state_registration.py): new, standard library only, functional style. Run it from the repo root: `python3 -I scripts/mission_state_registration.py . <cache_dir>`.
- [`data/mission-2026-11-14/queue-proposals-b50-02.csv`](../../data/mission-2026-11-14/queue-proposals-b50-02.csv): P-B5002-01 to -06.

**Labels:** **[F]** means a field as published by the registry. **[C]** means a script computation. **[I]** means an inference.

**Framing.** Everything below describes **public registry status on the day the data was pulled**. That status is not a compliance finding.
- A state requires registration only from organizations that solicit, or in some states hold charitable assets, there. Each state has its own exemptions.
- "Not found" therefore often means "not required" or "exempt without filing a claim".
- An expiration-notice status a few days after a due date usually reflects filing or processing lag.
- Nothing here implies wrongdoing by any sponsor.

**Context read first.**
- [`direction-state-daf-law-tracker.md`](direction-state-daf-law-tracker.md): state DAF law, with no state DAF-specific registration regime.
- [`queue-state-filings-transfer-terms.md`](queue-state-filings-transfer-terms.md) §2.3 and [`gap19-startup-cohort.md`](gap19-startup-cohort.md) §2.4 record earlier failed attempts on the CA, NY and MA registries (CA 404, NY reCAPTCHA, MA unreachable). This pass rechecked all three and reached the same result.
- [`data/mission-2026-11-14/state-intermediary-registration-2026.csv`](../../data/mission-2026-11-14/state-intermediary-registration-2026.csv) covers solicitation statutes.

---

## 1. Headline answers

| Question | Answer |
|---|---|
| **Which states could be checked by script?** | **Two: Colorado and Connecticut.** Both publish official registry data as public-domain open data, and robots.txt allows the SODA `/resource/` path for `*` and names no Claude agent [C]. The five candidate states (CA, NY, PA, MA, WA) are **manual only**; the reasons are in §2. |
| **Share of sponsors current, Colorado** (FEIN join) | **Top-50: 17 of 50 (34%) current.** Of the 35 sponsors with a CO record, 49% are current. **Small sample: 4 of 50 (8%)**; 4 of the 9 with a record are current. 15 top-50 and 41 small-sample sponsors have no CO record [C]. |
| **Share of sponsors current, Connecticut** (name join) | **Top-50: 28 of 50 (56%)** current, or 26 without the low-confidence name matches. That is 90% of the 31 matched. **Small sample: 6 of 50 (12%)**, or 5 without low-confidence matches. That is 6 of the 7 matched [C]. |
| **Who is delinquent?** | **CT: none** in either frame. **CO: 19 sponsors carry an expiration-notice status.** 14 of them are NOTICE 1, dated 2026-11-16, **five days past a 2026-11-15 due date** that fell on a Sunday. That is almost certainly filing lag, not lapse [I]. **Five have been past due for more than 30 days** (§3.2). |
| **Enforcement notices** | **None found in the sources checked.** Those were the CO and CT status fields (no REVOKED, DENIED or SUSPENDED status for any sampled sponsor) and the repo's state-AG litigation rows. The CA, NY and PA enforcement lists were **not** checked (manual only). |

## 2. Method

### 2.1 Sample

All of the sample comes from [`daf-long-tail-sponsors-fy2021-2024.csv`](../../data/mission-2026-11-14/daf-long-tail-sponsors-fy2021-2024.csv), using corrected FY2024 DAFRC ranks.
- **top50:** the 50 rows with `size_band_fy2024 == top50`.
- **small50:** a seeded random sample of 50 EINs, drawn from the EIN-sorted list with `random.Random(20261120).sample`.
  - The pool is 1,429 sponsors in bands `mid`, `t10_50`, `t1_10` and `t0_1` (FY2024 DAF assets above zero and rank above 50).
  - The draw gave 9 `mid`, 13 `t10_50`, 14 `t1_10` and 14 `t0_1` sponsors.

### 2.2 Access log (robots.txt and terms, read 2026-11-20 before any other fetch from each host)

| State | Host / source | robots.txt | Other controls | Decision |
|---|---|---|---|---|
| **CO** | data.colorado.gov `/resource/37wu-kn3g.json` (Colorado Secretary of State, Charities Program) | 200. The `*` group disallows only browse, odata and collocate paths. No Claude agent is named. `robotparser` allows `/resource/` for `*`, ClaudeBot, anthropic-ai, Claude-User, Claude-Web and Claude-SearchBot | Licence: Public Domain (dataset metadata) | **Scripted.** FEIN join, 1 s crawl delay |
| **CT** | data.ct.gov `/resource/ngch-56tr.json` (DCP eLicense credentials) | 200, same Socrata template, same verdicts | Licence: Public Domain | **Scripted.** Name join on credential `PUBLIC CHARITY*` (29,220 rows) |
| CA | oag.ca.gov (allows `/charities` pages, crawl-delay 10, honoured); rct.doj.ca.gov; ca-rcf.evokeplatform.com | oag: allowed. rct.doj.ca.gov: robots 404, and the legacy `Search.aspx` also returns **404**. evokeplatform: `/robots.txt` returns the app's HTML shell, so no rules | oag.ca.gov `/conditions` and `/disclaimer` contain no automation clause. **No bulk or open-data file:** oag.ca.gov/charities links only the two search tools, and the data.ca.gov sitemap (4,876 URLs) has no registry dataset. The new portal is a session-based low-code app (Azure auth, `/accessManagement/auth/me`) with no documented public API, and its bundle ships reCAPTCHA (Form.io) components | **Manual only.** The portal was not scripted and I did not try to reverse-engineer its API |
| NY | charities-search.ag.ny.gov; charitiesnys.com; data.ny.gov | charities-search: `Disallow:` (empty). charitiesnys.com: **HTTP 500**, treated as disallowed | The current JS bundle (`/assets/index-C5m9GbLo.js`) sends an **`X-Recaptcha-Token`** header to `charities-search-api.ag.ny.gov/api/FileNet/RegistrySearch`. A CAPTCHA is an anti-automation control. No registry dataset on data.ny.gov (Socrata catalog search) | **Manual only** |
| PA | www.charities.pa.gov (Charities OnLine); www.pa.gov enforcement list; data.pa.gov | **www.charities.pa.gov: `User-agent: *` / `Disallow: /`** | The pa.gov enforcement list is a Coveo-driven search, not a static list. No data.pa.gov registry dataset | **Manual only (robots)** |
| MA | www.mass.gov; filings.ago.state.ma.us; charity.ago.state.ma.us | mass.gov **403** (treated as disallowed). The AGO hosts were **unreachable** (connection failure) | none | **Manual only** |
| WA | data.wa.gov; ccfs.sos.wa.gov | data.wa.gov: allowed. ccfs: 404 page, so no rules | **data.wa.gov holds no charities registry dataset** (catalog searches for charity, charities, charitable and fundrais). Its only SOS registry item is a 2015 link to corporations search saying the "Corporations Data Extract feature is no longer available". The CCFS app loads **Cloudflare Turnstile** (a CAPTCHA) | **Manual only** |
| – | api.us.socrata.com (catalog search) | robots.txt redirects to a 404 page, so no rules | – | Used for dataset discovery only |
| – | www.coloradosos.gov `/pubs/charities/FAQ/*`, portal.ct.gov `/dcp/charities/...` | Allowed. The disallowed paths (e.g. `/ccsa/pages/search/`) were not touched | – | Fetched for status and exemption definitions |

No logins, forms or outreach were used, and no CAPTCHA was attempted. The user agent was `research-script/1.0`. crt.sh, certspotter, sec.gov and the repo's off-limits hosts were not used.

### 2.3 Matching and status mapping

**Colorado.**
- **Matching:** `fein` (`NN-NNNNNNN`) is joined to the sample EIN, filtered to `registranttypeabbr = 'Charitable Organization'` (710 rows returned). Where a FEIN has more than one `entityid`, the entity with the latest `statusdate` is used.
- **Status:** `currentStatus` [F] is mapped to a class [I]:
  - GOOD and REMINDER → *current*;
  - EXEMPT → *exempt*;
  - NOTICE 1, 2 or 3 (and their ESTIMATE variants) → *delinquent*;
  - REVOKED and REGISTRATION DENIED → *revoked*;
  - WITHDRAWN → *withdrawn*.
- **Notice schedule:** the CO SOS publishes it ([notices FAQ](https://www.coloradosos.gov/pubs/charities/FAQ/notices.html)) [F]:
  - the SOS expiration date is 7½ months after fiscal year end;
  - "Expiration notice 1: One day after the SOS due date", notice 2 after 10 days, notice 3 "18 days after expiration date".
- **Solicitation:** a registration "is valid until the day on which the required financial report is due". An organization listed as "expired – may not solicit" or "suspended" cannot solicit ([2018 changes](https://www.coloradosos.gov/pubs/charities/news/2018/20181001Changes.html), [consumers FAQ](https://www.coloradosos.gov/pubs/charities/FAQ/consumers.html)) [F].
- **Latest filing year** is the year of the latest `fiscalYearEndDate` on the entity's filings, i.e. the latest fiscal year whose financials CO holds.

**Connecticut.**
- **Matching:** there is no EIN. The normalised legal name (case, punctuation, `&`→AND, leading THE, trailing INC/CORP/LLC etc.) is matched against the credential `name`, `businessname` and `dba`.
  - A unique-prefix match is allowed only for names of 25 or more characters, because IRS names are truncated.
  - Names made only of generic words (e.g. "COMMUNITY FOUNDATION") are not matched.
  - **Confidence:** *medium* where the credential's address state equals the IRS BMF state, otherwise *low*.
- **Status:** `status` [F] is mapped to a class [I]:
  - ACTIVE, ACTIVE IN RENEWAL, ACTIVE UNDER REVIEW and APPROVED → *current*;
  - LAPSED → *delinquent*;
  - INACTIVE, CLOSED and EXPIRED APPLICATION → *inactive*;
  - SUSPENDED → *suspended*;
  - DENIED → *revoked*.
- DCP does not define these labels on the dataset page. Per DCP, registrations "expire after the last day of the eleventh month following the end of the organization's fiscal year" ([DCP general information](https://portal.ct.gov/dcp/charities/general-information-on-the-connecticut-solicitation-of-charitable-funds-act)) [F].
- CT carries no fiscal year, so `latest_filing_year` is blank. The credential's effective and expiration dates are given instead.

**Enforcement.**
- The registry status itself (revoked or suspended).
- The `state AG` plaintiff rows of [`daf-litigation-2021plus.csv`](../../data/mission-2026-11-14/daf-litigation-2021plus.csv) (2 rows, SDG Impact Fund and Flipcause), matched by normalised name. Neither is in the sample.

## 3. Results

### 3.1 Shares by state and frame [C]

| State | Frame | n | current | delinquent | withdrawn / inactive | not found | share current (of sample) | share current (of those found) |
|---|---|---|---|---|---|---|---|---|
| CO | top50 | 50 | 17 | 14 (11 ≤30 days past due) | 4 withdrawn | 15 | **34%** | 49% (17/35) |
| CO | small50 | 50 | 4 | 5 (3 ≤30 days) | 0 | 41 | **8%** | 44% (4/9) |
| CO | all | 100 | 21 | 19 (14 ≤30 days) | 4 | 56 | 21% | 48% (21/44) |
| CT | top50 | 50 | 28 (26 excl. low-confidence) | 0 | 3 inactive | 19 | **56%** | 90% (28/31) |
| CT | small50 | 50 | 6 (5) | 0 | 1 inactive | 43 | **12%** | 86% (6/7) |
| CT | all | 100 | 34 (31) | 0 | 4 | 62 | 34% | 90% (34/38) |
| CA, NY, PA, MA, WA | both | 500 | – | – | – | – | manual only | – |

- **Exempt:** no sampled sponsor carries CO status EXEMPT.
- **CT:** four "current" CT matches hold the credential "PUBLIC CHARITY-EXEMPT FROM FINANCIAL REQUIREMENTS": Servant Foundation, Signatry, UCLA Foundation and St Luke's Foundation [F].
- **Either state:** 47 of the 100 sponsors appear in at least one of the two registries. 18 are current in both.
- **Latest fiscal year in CO:** among the 21 CO-current sponsors, CO holds FY2025 financials for 18, FY2024 for 2 and FY2026 for 1 (T. Rowe Price, FYE 2026-03-31) [C].

**Reading the gap between frames [I].** The top-50 includes the national sponsors that solicit nationwide. Most small-sample sponsors are local community foundations, which would solicit in CO or CT only if based there. The low share for small sponsors mostly reflects where they operate, not lapses. Only 1 small-sample sponsor (Yampa Valley CF) is based in CO, and none in CT.

### 3.2 Sponsors with a delinquent-class status

**Connecticut:** none.

**Colorado, 5 days past due:** 14 sponsors. Each is NOTICE 1 with status date 2026-11-16 and due date 2026-11-15, which was a Sunday.

| Frame | Sponsors | Status in CT |
|---|---|---|
| top50 | GS Donor Advised Philanthropy Fund, Silicon Valley Community Foundation, Morgan Stanley Global Impact Funding Trust, American Endowment Foundation, Renaissance Charitable Foundation, ImpactAssets, Greater Kansas City Community Foundation, Greater Horizons, The U.S. Charitable Gift Trust, Community Foundation of New Jersey, American Gift Fund | 8 current, 3 not found |
| small50 | Indian Land Tenure Foundation, Donors Capital Fund, The American Ireland Fund | 2 current, 1 not found |

- All 14 are calendar-year filers whose latest CO financials are FY2024. Their FY2025 report was due on the extended date of 2026-11-15 [F/C].
- **This is a timing artefact of a snapshot five days after a mass due date [I].**
- P-B5002-02 re-pulls the file after 2026-12-15 to test this.

**Colorado, more than 30 days past due:** 5 sponsors, listed below with their latest CO filing [F].

| Sponsor | Frame | CO status (date) | Expired | Latest CO fiscal year | CT |
|---|---|---|---|---|---|
| The New York Community Trust | top50 | NOTICE 3 (2024-11-16) | 2024-11-15 | FY2022 | current |
| Tulsa Community Foundation | top50 | NOTICE 3 (2026-09-06) | 2026-08-15 | FY2024 (a renewal approved 2026-08-31 is on file) | current |
| UCLA Foundation | top50 | NOTICE 3 (2012-11-29) | 2003-11-15 | FY2002 (2002 initial registration only) | current (exempt from financial requirements) |
| Baton Rouge Area Foundation | small50 | NOTICE 3 (2025-12-16) | 2025-12-15 | FY2023 | inactive ("due to non-renewal of credential") |
| Jewish Foundation of Greensboro | small50 | NOTICE 3 (2024-02-16) | 2024-02-15 | FY2022 (2023 initial registration) | not found |

- **What this does and does not show [I].** CO registration is needed only while soliciting in CO, and an expired registration remains listed rather than being withdrawn. These rows show that the CO registration lapsed. They do **not** show that the sponsor solicited in CO while it was lapsed.
- **Withdrawn in CO:** 4 top-50 sponsors withdrew their registrations [F]:
  - Foundation for the Carolinas (2023);
  - Ayco Charitable Foundation (2026-09-04);
  - The Community Foundation for Greater Atlanta (2021, recorded as "THE COMMUNITY FOUNDATION FOR GREATER" in the frame);
  - Greater Houston Community Foundation (2018).
- **Withdrawn or inactive in CT:** the same pattern holds for Foundation for the Carolinas, Ayco and Greater Houston CF.

### 3.3 Not found

**Colorado.** 15 top-50 sponsors have no CO record under their FEIN [C]:
- Bank of America Charitable Gift Fund, The Chicago Community Trust, Jewish Communal Fund, Dechomai Asset Trust, Columbus Foundation, Oregon Community Foundation and Bessemer Giving Fund;
- the Community Foundation of Tampa Bay, and the sponsor recorded as "COMMUNITY FOUNDATION" (EIN 58-1723645, TN);
- six California or Minnesota sponsors: the Jewish Community Federation of San Francisco, the Jewish Community Foundation of Los Angeles, The San Diego Foundation, the Stanford board of trustees, The Minneapolis Foundation and The San Francisco Foundation.

**Connecticut.** 19 top-50 sponsors are not matched by name.
- Two were skipped as generic names: "COMMUNITY FOUNDATION" and "THE COMMUNITY FOUNDATION FOR GREATER".
- Several are IRS abbreviations or spellings that do not normalise to a registry name, so they may be false negatives [I]: "NATL CHRISTIAN CHARITABLE FDN INC", "BANK OF AMERICA CHARITABLE GIFT FD", "IMPACTASSETSINC", "THE US CHARITABLE GIFT TRUST" and "JEWISH COMMUNITY FEDERATION OF SAN".

**Meaning.** Absence is consistent with:
- not soliciting in the state;
- a statutory exemption;
- in CT only, a name mismatch.

## 4. Exemption rules and lags that limit comparison

| State | Who must register / exemptions (summary) | Cycle and lag |
|---|---|---|
| CO | Charitable organizations soliciting in CO. Exemptions under C.R.S. 6-16-104(6), e.g. churches. An exemption claim is optional: "It is not necessary to take any action if by law the organization is exempt" ([exemption FAQ](https://www.coloradosos.gov/pubs/charities/FAQ/exemption.html)). So "not found" ≠ "non-compliant" | Due 7½ months after FYE, with extensions. Notice 1 is sent one day after the due date. **A Nov-15 mass due date makes a late-November snapshot show many NOTICE 1 records** |
| CT | Organizations soliciting in CT. Exempt: religious bodies, accredited schools, governmental units, and organizations that "normally receive less than fifty thousand dollars ($50,000) in contributions annually" without paid solicitors. Exemption must be claimed on CPC-54 ([DCP](https://portal.ct.gov/dcp/charities/general-information-on-the-connecticut-solicitation-of-charitable-funds-act)) | Registration expires at the end of the 11th month after FYE. Many renewals already show 2026-12-01 effective dates (renewals processed early) |
| CA | Charities holding property or doing business in CA register with the AG Registry (RRF-1 annually). Some religious, educational and hospital organizations are exempt ([oag.ca.gov/charities](https://oag.ca.gov/charities)) | Not checked |
| NY | Dual EPTL 8-1.4 / Exec. Law Art. 7-A regime, with different exemptions (e.g. religious organizations) | Not checked |
| PA, MA, WA | Each has its own thresholds, exemptions and annual cycles | Not checked |

These differences, together with the lag between filing and status update, mean **status shares are not comparable across states**. They describe registry status, not conduct.

## 5. Data dictionary: `state-registration-2026-11-20.csv`

One row per sponsor × state (100 × 7 = 700).

| Column | Meaning |
|---|---|
| `sample_frame` | `top50` (FY2024 rank 1–50) or `small50` (seeded sample, seed 20261120) |
| `sample_order` | Order within the frame (by FY2024 asset rank) |
| `ein` | 9-digit EIN from the frame file |
| `sponsor_name` | IRS name as in the frame file (may be truncated) |
| `sponsor_category`, `size_band_fy2024`, `fy2024_rank_assets`, `daf_assets_fy2024`, `bmf_state` | Copied from `daf-long-tail-sponsors-fy2021-2024.csv` |
| `state` | CO, CT, CA, NY, PA, MA or WA |
| `registry` | Registry name and source dataset |
| `access_mode` | `scripted_open_data` or `manual_only` |
| `status_class` | [I] mapped class: `current`, `delinquent`, `suspended`, `revoked`, `exempt`, `withdrawn`, `inactive`, `pending`, `not_found`, or `manual_only` (not checked) |
| `match_confidence` | CO: `high (FEIN)`. CT: `medium` (name and address state equal BMF state) or `low` (name only) |
| `days_past_due` | [C] For delinquent CO rows: days from the expiration/due date to 2026-11-20 |
| `status_raw` | [F] Registry status. CT: `status / statusreason (credential)` |
| `status_date` | [F] CO `statusDate`; CT credential `effectivedate` |
| `latest_fiscal_year_end`, `latest_filing_year` | [F/C] CO only: latest fiscal year end on file, and its year |
| `latest_filing_type`, `latest_filing_date` | [F] CO: type and approval date of the latest filing. CT: effective date |
| `last_renewal_or_master_date` | [F] CO: latest RENEWAL or MASTER filing approval date |
| `next_due_or_expiration` | [F] CO `expirationDate` (or next renewal date); CT `expirationdate` |
| `registry_id`, `registry_name` | [F] CO `entityId`; CT `fullcredentialcode`; registered name |
| `match_method` | How the row was matched (FEIN exact; normalised name exact; unique prefix; generic name not matched) |
| `enforcement_notice` | Registry status if revoked or suspended, plus any state-AG row in the repo litigation file. `none in sources checked` for CO and CT; for manual-only states, `registry not checked; none in repo litigation file` |
| `enforcement_source` | URL for any enforcement hit (none in this run) |
| `source_url` | Registry or dataset page |
| `retrieved` | 2026-11-20 |
| `notes` | Interpretation caveat (CO lag, not-found meaning) or the manual-only reason |

## 6. Limits

- **Two states only.** CA, NY, PA, MA and WA are manual only (§2.2), so the CA and NY shares the brief asked for are **not available** from this pass. P-B5002-01 and P-B5002-03 cover them.
- **Snapshot timing.** The CO data were pulled five days after a mass due date (§3.2). CO statuses update daily, and CT records were refreshed on various dates (`recordrefreshedon`).
- **CT is matched on name.** False negatives come from truncated IRS names and name variants. 4 matches are low-confidence; St Luke's Foundation (MN) matched a CT-addressed organization and is probably a different entity [I]. P-B5002-04 proposes an EIN crosswalk.
- **Status vocabulary.** The CO definitions are published. The CT class mapping is an inference.
- **Enforcement.** Only registry status fields and the repo's litigation file were checked. The state AG press releases and the PA, CA and NY disciplinary lists were not read, so "none found" is limited to those sources.
- **Frame.** The FY2024 top-50 uses the corrected DAFRC ranks in the long-tail file. It differs slightly from the FY2025-refresh league table.

## 7. Source register

| ID | Source | Type | Date | URL |
|---|---|---|---|---|
| SR01 | Colorado SOS, Registration of Charities, Paid Solicitors … (open data 37wu-kn3g) | official open data [F] | pulled 2026-11-20 | https://data.colorado.gov/resource/37wu-kn3g.json (page: https://data.colorado.gov/Business/Registration-of-Charities-Paid-Solicitors-Professio/37wu-kn3g) |
| SR02 | Connecticut DCP, State Licenses and Credentials (ngch-56tr) | official open data [F] | pulled 2026-11-20 | https://data.ct.gov/resource/ngch-56tr.json (page: https://data.ct.gov/Business/State-Licenses-and-Credentials/ngch-56tr) |
| SR03 | Colorado SOS, Filing notice schedule | official [F] | read 2026-11-20 | https://www.coloradosos.gov/pubs/charities/FAQ/notices.html |
| SR04 | Colorado SOS, Changes to the CCSA effective 2018-10-01 | official [F] (archived page) | 2018, read 2026-11-20 | https://www.coloradosos.gov/pubs/charities/news/2018/20181001Changes.html |
| SR05 | Colorado SOS, Donors and consumers FAQ | official [F] | read 2026-11-20 | https://www.coloradosos.gov/pubs/charities/FAQ/consumers.html |
| SR06 | Colorado SOS, Exemption claims FAQ | official [F] | read 2026-11-20 | https://www.coloradosos.gov/pubs/charities/FAQ/exemption.html |
| SR07 | CT DCP, General Information on the Solicitation of Charitable Funds Act | official [F] | read 2026-11-20 | https://portal.ct.gov/dcp/charities/general-information-on-the-connecticut-solicitation-of-charitable-funds-act |
| SR08 | CA AG, Charities page (links to both search tools) | official [F] | read 2026-11-20 | https://oag.ca.gov/charities |
| SR09 | CA AG, Delinquency page | official [F] | read 2026-11-20 | https://oag.ca.gov/charities/delinquency |
| SR10 | CA legacy Registry Search Tool (HTTP 404) | access evidence | 2026-11-20 | https://rct.doj.ca.gov/Verification/Web/Search.aspx?facility=Y |
| SR11 | CA new registry portal | access evidence | 2026-11-20 | https://ca-rcf.evokeplatform.com/app/publicPortal/verification |
| SR12 | NY Charities Bureau registry search (reCAPTCHA-gated API) | access evidence | 2026-11-20 | https://charities-search.ag.ny.gov/RegistrySearch |
| SR13 | PA Charities OnLine (robots disallow all) | access evidence | 2026-11-20 | https://www.charities.pa.gov/robots.txt |
| SR14 | PA DOS, Charities Enforcement and Disciplinary Actions | official [F] (not machine-readable) | read 2026-11-20 | https://www.pa.gov/agencies/dos/alerts-and-notices/charities-enforcement-and-disciplinary-actions |
| SR15 | WA SOS, Corporations & Charities (links to CCFS, Turnstile-protected) | access evidence | 2026-11-20 | https://www.sos.wa.gov/corporations-charities |
| SR16 | data.wa.gov, Corporations Search (WA) link dataset, "Data Extract … no longer available" | official [F] | 2015 metadata, read 2026-11-20 | https://data.wa.gov/api/views/f9jk-mm39.json |
| SR17 | Socrata Discovery API (dataset discovery for WA, NY, PA, CO, CT) | catalog | 2026-11-20 | https://api.us.socrata.com/api/catalog/v1 |
| SR18 | data.ca.gov sitemap (no charity registry dataset) | catalog | 2026-11-20 | https://data.ca.gov/sitemap.xml |
| SR19 | MA AG public-charity search (mass.gov robots 403) | access evidence | 2026-11-20 | https://www.mass.gov/how-to/search-for-a-public-charity |
| SR20 | Repo: sponsor frame and litigation file | repo | 2026-11 | data/mission-2026-11-14/daf-long-tail-sponsors-fy2021-2024.csv ; data/mission-2026-11-14/daf-litigation-2021plus.csv |
