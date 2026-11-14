# Community-foundation vendor map by EIN (P-QA1-05) and Give Interactive registry check (P-GIV-03)

**Date:** 2026-11-14. **Status:** public pages only. I logged in nowhere, submitted no forms and contacted no one. Donor-login pages were fetched without credentials, only to read their host, headers and markers.
**Recency rule:** every vendor signal is a page that was live on 2026-11-14, a 2021+ certificate, or a 990 line for tax years 2021–2025.

**Evidence labels:**
- **[F]:** first-party. That means the foundation's own homepage link, redirect, page marker, DNS record or IRS e-file return.
- **[V]:** a vendor statement.
- **[R]:** a third-party source.
- **[I]:** my inference.

## Key findings

**Coverage.**
- **Universe.** 803 DAFRC FY2024 community foundations (CFs), holding **$66.14bn** of DAF assets.
- **Mapped.** 481 CFs (59.9%) are mapped to a named portal vendor at high or medium confidence. They hold **$59.9bn, or 90.5% of CF DAF assets**.
- **Mapped at high confidence only.** 477 CFs, also 90.5% of assets.
- **Unmapped.** No vendor was found for the other 39% of CFs, which hold 6% of assets. Most of them are small.

**Vendor shares.** Foundant CommunitySuite is the clear count leader: 361 CFs, 45% of all CFs and 75% of mapped CFs. The asset weighting is different:
- Foundant holds 32.7% of CF DAF assets.
- Salesforce Experience Cloud holds 23.7% with only 19 CFs, led by SVCF.
- GiftingNetwork holds 11.5% with 2 CFs (CCT and FFTC).
- Ren/Stellar iPhi has 22 CFs and 5.9% of assets.
- akoyaGO has 48 CFs and 3.2% of assets.
- Foundation Cloud (spectrumportal.net) has 14 CFs and 3.6% of assets.

**Portal is not ledger.** For 27 mapped CFs, holding about 43% of CF DAF assets, the portal is a front-end layer: Salesforce, GiftingNetwork, SmartSimple, Power Pages, donor-portal.org or Fund-Miner. The general ledger behind these portals is not public. This is proposal P-CFV-01.

**Validation.** On the 35 rows where a named vendor was already in the hand-checked v2 top-40 file, the crawler independently found a vendor for 32. It agreed on all 32 (`cf-vendor-map-summary.json`).

**Migration signals.** The data show three Stellar→Foundant switches and five foundations with two live fund-login vendors (§5).

**Give Interactive.** No CF production tenant was found apart from the known CCT tenant. The certificate data show lapsed or staging-only Give tenants at East Bay, Kalamazoo, San Diego, Minneapolis and FFTC (§5).

**P-GIV-03.**
- Every automated registry route was blocked: Delaware was CAPTCHA-gated; Kansas, Missouri and OpenCorporates were refused or challenged. **I record P-GIV-03 as blocked.**
- SEC EDGAR has no Give Interactive filings.
- Control evidence remains the Signatry Charitable Trust's Schedule R: a 99% interest, with general-partner status from CY2023 (§7).

## 1. Method

The script is [`scripts/mission_cf_vendor_map.py`](../../scripts/mission_cf_vendor_map.py). It is stdlib-only, written in functional style, and every response is cached so reruns are offline.

| Step | Source | What is recorded |
|---|---|---|
| Universe | `dafrc-sponsor-schedule-d-fy2019-2024.csv`: rows with `type = Community Foundation` and `fiscal_year_end = 2024` | EIN, name, `eoy_daf_assets` |
| Homepage | `<WebsiteAddressTxt>` in the CF's latest e-filed 990. The first 96 KB is read with an HTTP Range request from the IRS e-file mirror (`xml_url` in `form990-returns-schedule-d-harvest-full.csv`) | 766 of 803 have a usable website; 37 list none |
| 990 Part VII-B | `form990-contractors-harvest-full.csv`, tax years 2021+ | Foundant, Stellar/Ren, NPact, Akoya, FidTech, Give Interactive, GiftingNetwork and Blackbaud/MicroEdge payees. Only payees above $100k are listed in a 990, so this is a floor |
| Crawl | Steps below | Outbound link hosts, redirect targets, response headers, page markers |
| DNS | dns.google DNS-over-HTTPS CNAME chain for portal hosts on the CF's own domain | For example, `myfund.jaxcf.org` → `…live.siteforce.com` → `salesforce.com` |
| Certificate transparency | crt.sh, for certificates issued in 2021 or later, on `fcsuite.com`, `iphiview.com`, `spectrumportal.net`, `donorsphere.org`, `giveinteractive.com` and `donor-portal.org` | Tenant labels. A label counts only when it equals the CF's own website domain stem, and only one CF has that stem |
| Seed | `community-foundation-rails-portals-2026-v2.csv` (top 40, hand-checked) | Used only when the crawl found nothing: 4 rows (CCT, Pittsburgh, CFTexas, GiveWell) |

**Crawl steps:**
1. Read robots.txt; 5 sites disallow crawling.
2. Fetch the homepage.
3. Follow up to 3 same-site links that look like donor logins.
4. Inspect up to 3 off-site or subdomain portal links, and only when no vendor host had been found.

**Crawl politeness:**
- At most one request per second per host, through a global per-host throttle.
- A generic research User-Agent.
- Retries on transport errors only. Blocked sites were not worked around.

**Donor-login context.** A link counts as donor-login context when its text or path matches login, fund-holder, donor-portal or "My…" patterns, and does not match grant-application, scholarship, nonprofit or apply patterns.
- Generic hosts count only in a donor-login context. These are Salesforce `*.my.site.com`/`force.com`, SmartSimple, Power Pages, Blackbaud-hosted pages, CyberGrants and Foundant GLM (`grantinterface.com`).
- DAF-specific hosts count anywhere on the site. For example, any `*.fcsuite.com/erp/...` link is a CommunitySuite tenant, including its `erp/donate` module.

**Vendor host signatures:**

| Vendor | Hosts |
|---|---|
| Foundant CommunitySuite | `*.fcsuite.com` |
| Ren/Stellar iPhi | `*.iphiview.com` |
| Foundation Cloud | `*.spectrumportal.net` |
| akoyaGO | `gofund`, `godonate` and `goapply2` on `akoyago.com` |
| DonorSphere | `*.donorsphere.org` |
| Give Interactive | `*.giveinteractive.com` |
| GiftingNetwork | "Powered by GiftingNetwork" marker |
| Blackbaud DonorCentral | `*.donorcentral.com` or `edonorcentral.com` |
| Fund-Miner | `fund-miner.com` |
| Unidentified white-label | `*.donor-portal.org` |

**Decision rule.** Each CF gets one row, and the strongest signal wins. The order of strength is:
1. A homepage or redirect link to a vendor host, in donor-login context.
2. A DNS CNAME, page marker or response header.
3. The v2 hand check.
4. A site link to a DAF-specific vendor host.
5. A 990 payee.
6. A certificate-transparency label match.

**Confidence levels:**
- **High:** first-party portal evidence (rules 1–4).
- **Medium:**
  - a 990 payee alone, for a DAF-ledger vendor;
  - akoyaGO when only GoApply (grant-application) links were found;
  - a site-wide akoyaGO link without corroboration.
- **Low:**
  - a certificate label alone;
  - Foundant GLM only, which is a grants module and supports no ledger inference.
- **None:** nothing found.

Every competing vendor signal is kept in `conflicting_signals` and in [`cf-vendor-map-signals.csv`](../../data/mission-2026-11-14/cf-vendor-map-signals.csv), which holds 3,376 signal rows.

**`ledger_implied` flag:**
- `yes` for integrated fund-accounting suites whose portal sits on the vendor's own ledger: CommunitySuite, iPhi, Foundation Cloud, akoyaGO, DonorSphere, and Blackbaud DonorCentral over FIMS/FE NXT [I].
- `unknown` for portal layers.

## 2. Coverage

| Measure | CFs | Share of CFs | CF DAF assets ($bn) | Share of assets |
|---|---|---|---|---|
| Universe (FY2024 DAFRC CFs) | 803 | 100% | 66.14 | 100% |
| Website on 990 | 766 | 95.4% | | |
| Homepage crawled (HTTP response with body) | 697 | 86.8% | | 96.8% |
| Homepage refused or errored (mostly RemoteDisconnected or WAF) | 64 | 8.0% | | |
| No website on 990 | 37 | 4.6% | | |
| robots.txt disallows | 5 | 0.6% | | |
| **Mapped to a named vendor, high or medium confidence** | **481** | **59.9%** | **59.88** | **90.5%** |
| High confidence only | 477 | 59.4% | | 90.5% |
| Portal found, vendor unidentified (NYCT MyGrants, Marin givingcenter) | 2 | 0.2% | 2.13 | 3.2% |
| Foundant GLM link only (low confidence, no ledger inference) | 5 | 0.6% | 0.11 | 0.2% |
| No portal or vendor signal | 315 | 39.2% | 4.02 | 6.1% |

The gap is concentrated in small CFs. Of the 315 with no signal, 244 hold less than $10m of DAF assets. The largest unmapped CFs are Arizona CF ($423m) and CF for Southeast Michigan ($330m). Baltimore CF, the Miami Foundation, Hampton Roads, Blue Grass and Greater Kanawha Valley ($128m–$180m each) also refused scripted reads.

## 3. Vendor shares

This table covers all 803 CFs, with the high and medium confidence rows mapped to vendors ([summary JSON](../../data/mission-2026-11-14/cf-vendor-map-summary.json)).

| Vendor family | CFs | Share of CFs | DAF assets ($bn) | Share of CF DAF assets | Share of mapped CFs | Share of mapped assets |
|---|---|---|---|---|---|---|
| Foundant (CommunitySuite) | 361 | 45.0% | 21.61 | 32.7% | 75.1% | 36.1% |
| Salesforce Experience Cloud | 19 | 2.4% | 15.65 | 23.7% | 4.0% | 26.1% |
| GiftingNetwork | 2 | 0.2% | 7.60 | 11.5% | 0.4% | 12.7% |
| Ren / Stellar iPhi | 22 | 2.7% | 3.90 | 5.9% | 4.6% | 6.5% |
| donor-portal.org (unidentified white-label; GKCCF) | 1 | 0.1% | 2.57 | 3.9% | 0.2% | 4.3% |
| Foundation Cloud (spectrumportal.net; NPact per [R]) | 14 | 1.7% | 2.36 | 3.6% | 2.9% | 3.9% |
| akoyaGO | 48 | 6.0% | 2.13 | 3.2% | 10.0% | 3.6% |
| DonorSphere / FidTech | 3 | 0.4% | 1.31 | 2.0% | 0.6% | 2.2% |
| SmartSimple (Boston) | 1 | 0.1% | 1.10 | 1.7% | 0.2% | 1.8% |
| Blackbaud (DonorCentral ×6; NetCommunity ×1) | 7 | 0.9% | 0.86 | 1.3% | 1.5% | 1.4% |
| Microsoft Power Pages (Seattle) | 1 | 0.1% | 0.69 | 1.0% | 0.2% | 1.1% |
| Fund-Miner (Nebraska CF, Paso del Norte) | 2 | 0.2% | 0.10 | 0.1% | 0.4% | 0.2% |
| Give Interactive (production portal) | 0 | 0% | 0 | 0% | — | — |
| Portal found, vendor unidentified | 2 | 0.2% | 2.13 | 3.2% | | |
| Foundant GLM only | 5 | 0.6% | 0.11 | 0.2% | | |
| No signal | 315 | 39.2% | 4.02 | 6.1% | | |

**By size band** (count of CFs per vendor family):
- **$1bn or more (10 CFs):**
  - Salesforce 3 (SVCF, Oregon CF, California CF)
  - GiftingNetwork 2 (CCT, FFTC)
  - Foundant 2 (Columbus, CF Greater Atlanta)
  - donor-portal.org 1 (GKCCF)
  - SmartSimple 1 (Boston)
  - unidentified 1 (NYCT)
- **$100m–$1bn (90 CFs):** Foundant 46, Salesforce 12, Ren iPhi 7, Foundation Cloud 5, akoyaGO 5, DonorSphere 3, Blackbaud 2, Power Pages 1, unidentified 1, unmapped 8.
- **$10m–$100m (275 CFs):** Foundant 163, akoyaGO 21, Ren iPhi 12, Foundation Cloud 6, Blackbaud 5, unmapped 63.
- **Under $10m (428 CFs):** Foundant 150, akoyaGO 22, Foundation Cloud 3, Ren iPhi 3, Salesforce 3, GLM-only 3, unmapped 244.
- **$10m–$100m** also has Foundant GLM-only 2, Fund-Miner 2 and Salesforce 1.

**Reading [I]:**
- Foundant dominates the long tail and the mid-market.
- The biggest CFs have instead built portals on general-purpose platforms (Salesforce, GiftingNetwork, custom apps), so the asset-weighted market for an integrated CF ledger is much smaller than the count suggests.
- No CF above $1bn runs Ren iPhi, Foundation Cloud or akoyaGO as its donor portal.
- This replaces the capped Foundant X1 placeholder noted in the queue item: Foundant's footprint is now counted, not vendor-claimed.

## 4. Portal versus ledger

- **Integrated suites (`ledger_implied = yes`).** 454 of the 481 mapped CFs run portals that are modules of an integrated fund-accounting suite. For these, the portal vendor is the ledger vendor [I, based on product architecture].
- **Portal layers (`ledger_implied = unknown`).** 27 mapped CFs, holding **42.7% of all CF DAF assets**, run portal layers whose GL is not public:
  - Salesforce: 19 CFs, including SVCF, Oregon CF, California CF, Philadelphia, CICF/Indianapolis and Dayton.
  - GiftingNetwork: 2 (CCT, FFTC).
  - Boston (SmartSimple), Seattle (Power Pages), GKCCF (donor-portal.org) and Fund-Miner ×2.
  - Pittsburgh (Blackbaud NetCommunity).
- **Two known ledgers.**
  - Greater Washington CF runs Foundation Cloud for the portal and states Blackbaud Financial Edge NXT for the ledger (v2 file; 990 Blackbaud lines for TY2022 and TY2024).
  - SVCF's 990 names only consultants (Slalom).
- **Next step.** This is the open part of the market map (P-CFV-01).

## 5. Notable signals

**Stellar/Ren → Foundant switches** [F 990 + F live link]. Each foundation below has a Stellar 990 payee but a live Foundant CommunitySuite fund login on 2026-11-14:

| Foundation | Stellar 990 payee | Foundant CommunitySuite fund login, live 2026-11-14 |
|---|---|---|
| Arkansas Community Foundation | "database provider fees" (TY2021–22) | `arcf.fcsuite.com` "FUNDHOLDER LOGIN" |
| Community Foundation of Acadiana | "software support" $118,458 (TY2024) | `cfacadiana.fcsuite.com/erp/portal/fundadvisor` |
| CF of Greater Flint | $114,605 (TY2022) | `cfgf.fcsuite.com` donor portal |

At Flint, a legacy `cfgf.iphiview.com` contact link is still on the site. These are probably 2023–2025 migrations [I]. Dates are not established.

**Dual live fund logins:**
- **CF Tampa Bay:** `cftampabay.fcsuite.com` and `cftampabay.spectrumportal.net`, both labelled "Fundholder Login".
- **Winston-Salem Foundation:** `wsfoundation.spectrumportal.net`, alongside an `/fund-portal` redirect to `wsfdn.fcsuite.com`. The TY2024 990 shows Foundant at $187,344.
- **New Mexico CF:** a `nmcf.spectrumportal.net` sign-in, with fcsuite donate pages.
- **Indian River CF:** `ircf.donor-portal.org` "My Fund: Login" and `indianriver.fcsuite.com/erp/portal`.
- **Yakima Valley CF:** an akoyaGO donor login and a legacy `yvcf.iphiview.com` give page.

The direction of each move is open (P-CFV-03). With Kalamazoo (below), Foundation Cloud appears at several former Foundant, Give or iPhi sites [I].

**Give Interactive certificate tenants at CFs** (crt.sh, certificates from 2021 on):

| Foundation | Give tenants in CT logs | Current portal |
|---|---|---|
| Chicago Community Trust | `cct` production, 2025-06-11 to 2026-08-15; sandbox and staging to 2026-09 | GiftingNetwork (role of the Give tenant unknown, as in v2) |
| East Bay CF | `ebcf` production, 2023-06-06 to 2026-03-27 | akoyaGO GOfund |
| Kalamazoo CF | `kzcf` production, 2024-07-22 to 2025-10-19 | "Kalamazoo Connect" on `kalfound.spectrumportal.net` |
| San Diego Foundation | staging only, 2025 | Foundation Cloud |
| Minneapolis Foundation | staging only, from 2026-02 | iPhi DonorView |
| FFTC | sandbox and staging, 2022–2024 | GiftingNetwork (Give was paid $654,500 in TY2023) |

No CF in the universe links to a `giveinteractive.com` portal from its homepage. The certificate data alone cannot say whether a tenant is a pilot, a back-office use or a lapsed contract [I].

**Hosts newly identified in this pass:**
- **Fund-Miner** (`fund-miner.com`): Nebraska CF ("NCF Connect") and Paso del Norte. This is a small CF portal vendor not previously in the repo.
- **Blackbaud DonorCentral on `*.donorcentral.com`:** Princeton Area, The Community Foundation for Greater New Haven (`cfgnh`), St. Joseph County, Appalachian Ohio, Northern Cincinnati and Valley CF. The one tenant sampled (`pacf.donorcentral.com`) loads Blackbaud SKY UX assets (`sky.blackbaudcdn.net`, BLKB fonts) [F]. Graph edges are marked `inferred`.

## 6. Graph edges and queue proposals

[`relationship-graph-edges-additions-9.csv`](../../data/mission-2026-11-14/relationship-graph-edges-additions-9.csv) holds 440 edges, EI001–EI440. Each is a vendor → CF `technology_provider` edge. Edges already in earlier edge files were skipped, matched on vendor and normalised CF name.

**Confirmed edges (417).** These rest on first-party evidence only, meaning the CF's own homepage link or redirect to the vendor host, a DNS CNAME or a portal response header:

| Vendor | Confirmed edges |
|---|---|
| Foundant | 345 |
| Akoya | 43 |
| Stellar | 14 |
| Salesforce | 13 |
| Fund-Miner | 2 |

**Inferred edges (23):**
- **NPact (Foundation Cloud), 13.** The `spectrumportal.net` host is first-party, but NPact's ownership of it rests only on [R] sources, per the wave-7 governing correction.
- **Blackbaud (`donorcentral.com`), 6.**
- **Akoya GoApply-only or uncorroborated, 4.**

Target names carry the EIN and domain because DAFRC truncates some names (for example "COMMUNITY FOUNDATION" for Greater Memphis).

The proposals are in [`queue-proposals-cf-vendor-map.csv`](../../data/mission-2026-11-14/queue-proposals-cf-vendor-map.csv):

| ID | Question |
|---|---|
| P-CFV-01 | Ledger behind portal-layer CFs |
| P-CFV-02 | Close the unmapped tail |
| P-CFV-03 | Date the migrations and dual portals |
| P-CFV-04 | Identify the operators of donor-portal.org and Fund-Miner |
| P-GIV-05 | Human read of the Kansas and Delaware registry records |

## 7. P-GIV-03: Give Interactive LLC in public business registries

All checks were made on 2026-11-14 with read-only requests. No search form was submitted past a CAPTCHA.

| Registry or source | Result |
|---|---|
| Delaware Division of Corporations, ICIS entity search ([namesearch.aspx](https://icis.corp.delaware.gov/ecorp/entitysearch/namesearch.aspx)) | The page carries a CAPTCHA panel (`ctl00_ContentPlaceHolder1_pnlCaptcha`, `captchaDiv`). **Blocked (CAPTCHA-gated).** Delaware also does not publish LLC members or managers in the free search, so the most it could give is file number, formation date and registered agent |
| Kansas Secretary of State business entity search ([Search.aspx](https://www.sos.ks.gov/eforms/BusinessEntity/Search.aspx), linked from [sos.ks.gov/businesses](https://sos.ks.gov/businesses/businesses.html)) | HTTP 403 (CloudFront "Request blocked"). **Blocked.** `ksbiz.kansas.gov` could not be reached through the proxy |
| Missouri SOS business search (bsd.sos.mo.gov) | HTTP 403. **Blocked** |
| OpenCorporates search | reCAPTCHA challenge page. **Blocked.** The API needs a key |
| SEC EDGAR full-text search and company search | 0 hits for "Give Interactive" and no registrant, so no Form D or other filing [F] |
| Give Interactive [company page](https://www.giveinteractive.com/company) [V] | Lists officers, not owners: Lucas Cherry (Founder & CEO; former EVP at The Signatry), Sam Hoefer (CPO), Neil McQueen (CTO), Jen McMaster (VP Technology) and Hannah Erickson (VP Client Delivery). No ownership statement |

**What stands.**
- Control evidence remains [EB001](../../data/mission-2026-11-14/relationship-graph-edges-additions-2.csv). The Signatry Charitable Trust's Schedule R lists Give Interactive LLC (EIN 84-4835291, Delaware LLC, Overland Park KS) at an ownership share of 0.99 for CY2020–CY2024. The Trust is general or managing partner from CY2023 ([queue-give-interactive-displacement.md §5](queue-give-interactive-displacement.md)).
- No public source names the holder of the remaining ~1%, or any management-equity holders [U].
- Whether the Trust holds the interest in its general assets or inside DAFs (IRC 4943(e)) is still not disclosed.
- **P-GIV-03 status:** blocked. Follow-up is P-GIV-05, a human read of the Kansas foreign-LLC record and annual report.

## 8. Limitations

- **Portal ≠ ledger.** The map records the donor-facing system. For integrated suites the ledger is inferred from product architecture [I], and is not proven for each CF.
- **Homepage-based crawl.**
  - CFs whose login sits in JavaScript menus, behind a WAF, or two or more clicks deep are missed.
  - 64 homepages refused scripted reads and were not worked around: no User-Agent spoofing and no browser automation.
  - Small CFs with no website, or with a site on a parent CF, show up as unmapped.
- **Affiliates and supporting organisations** that share a parent's tenant are each counted. Examples are Dayton Foundation Depository, The Indianapolis Foundation (CICF portal) and Huron County CF (on Erie's `fcsuite` tenant). This inflates counts slightly but not assets much.
- **Certificate transparency is weak for the big vendors.** Foundant and iPhi mostly use wildcard certificates (only 11 and 7 named `fcsuite` and `iphiview` hosts since 2021). crt.sh intermittently returned 404/502 for `%.domain` queries; bare-domain queries were used as well.
- **990 lines** cover only the five highest-paid contractors above $100k, and the service text does not name the product (for example, Foundant "grant management" in TY2021 could be GLM).
- **Point in time.** Everything was live on 2026-11-14. Dual-portal CFs are mid-transition, so their mapped vendor may change.
- **DAF assets** are the DAFRC FY2024 `eoy_daf_assets` (which include DAFRC corrections), not 990-reported values.

## 9. Data dictionary: `data/mission-2026-11-14/cf-vendor-map-by-ein.csv` (803 rows)

| Column | Meaning |
|---|---|
| `ein` | 9-digit EIN (DAFRC) |
| `name` | DAFRC sponsor name (may be truncated) |
| `fy2024_daf_assets_usd` | DAFRC FY2024 end-of-year DAF assets |
| `homepage` | Website from the latest e-filed 990 `WebsiteAddressTxt`, normalised to `https://host/` |
| `portal_url` | Donor or fund-login URL behind the decision (blank if none) |
| `portal_vendor` | Product label, e.g. "Foundant CommunitySuite", "Ren (Stellar) iPhi DonorView", "Salesforce Experience Cloud", "unidentified (portal found, no vendor marker)", "unmapped" |
| `evidence_type` | `homepage_link_vendor_host`, `homepage_link_redirect_vendor_host`, `site_link_vendor_host`, `portal_redirect_vendor_host`, `portal_page_redirect_vendor_host`, `portal_page_marker`, `portal_response_header`, `dns_cname`, `repo_v2_manual_check`, `990_part_vii_b_contractor`, `ct_tenant_label_matches_domain_stem`, `portal_fetch` (portal fetched, no vendor) |
| `evidence_url` | Page, DNS query, crt.sh query or ProPublica 990 page holding the evidence |
| `confidence` | `high`, `medium`, `low` or `none` (rules in §1) |
| `retrieved` | 2026-11-14 |
| `vendor_family` | Grouping used for the share tables |
| `ledger_implied` | `yes` (integrated fund-accounting suite), `unknown` (portal layer) or `no` (GLM) |
| `evidence_detail` | Link text and URL, header, CNAME chain or 990 line |
| `corroborating_evidence` | Other signals for the same vendor |
| `conflicting_signals` | Signals for other vendors (migrations, dual portals, certificate tenants) |
| `vendor_990_lines` | All matched 990 Part VII-B vendor lines, TY2021+ |
| `crawl_status` | `ok_<http>`, `homepage_error:<reason>`, `no_homepage` or `robots_disallowed` |
| `crawl_vendor_family` | Vendor found by the crawl alone (used for the v2 agreement check) |
| `homepage_source` | IRS e-file XML the website came from |

**Companion files:**
- `cf-vendor-map-signals.csv`: every signal per EIN, including family, product, evidence and strength.
- `cf-vendor-map-summary.json`: coverage, shares, certificate tenant counts, v2 agreement and edge counts.

**To reproduce:** `python3 scripts/mission_cf_vendor_map.py --fetch --cache-dir <dir>` makes network calls. Without `--fetch` the script runs from the cache only.

## Validation corrections (wave 9, 2026-11-14) — governing
Source: [validation-wave9-report.md](validation-wave9-report.md). Where these conflict with the text above, these govern.

1. **§ Stellar/Ren → Foundant switches.** Replace "These are probably 2023–2025 migrations [I]. Dates are not established." with "These are probably 2025–2026 migrations [I]. Arkansas CF's 'announces database transition' post is dated 2026-04-20, and Acadiana still paid Stellar $118,458 in TY2024. Flint keeps a legacy `cfgf.iphiview.com` link."
2. **Accuracy section.** Add: "Wave-9 spot-check: 15 random high/medium rows, vendor correct 15/15 (0%; 95% upper bound 21.8%); 2 evidence-label defects."
