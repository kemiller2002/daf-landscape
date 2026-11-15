# Batch 30C: closing unmapped community foundations (P-CFV-02), Foundation Cloud portal versus ledger (P-B29A-02), and Give Interactive tenants and lapses (P-GIV-06, P-GIV-07)

**Date:** 2026-11-15. **Author:** batch-30C queue agent.
**Queue items:** P-CFV-02, P-B29A-02, P-GIV-06 and P-GIV-07 (`data/mission-2026-11-14/research-priority-queue.csv`).

**Status:** public sources only.
- I did not log in, submit forms, contact anyone, or call any vendor or tenant API.
- Sponsor pages were read by script (robots.txt honoured, at most 1 request per second per host, a generic identifying User-Agent, no spoofing) and by hand with WebFetch.
- DNS lookups went through dns.google. Certificate data came from crt.sh and IRS e-file XML from the public `gt990datalake-rawdata` mirror.
- Homepages that refuse scripted reads were not worked around.

**Vendor tenant pages.** These were **not used as evidence** except where noted:
- Foundant's `*.fcsuite.com` robots.txt disallows AI agents (`ClaudeBot`, `anthropic-ai`, `GPTBot` and others) site-wide. I found this mid-run.
- Before then, the first run had fetched about 50 `/erp/portal` sign-in pages and one `/erp/donate/list` page.
- The final script makes no tenant-page requests. Two observations from those earlier fetches are kept, and are disclosed where used: the Blue Grass backlink and the Baltimore collision.

**Recency rule:** current-state claims rest on 2021+ evidence. A Blackbaud case study about Amarillo describes 2017–18 Giving Days and is not used.

**Built on (with their governing corrections):**
- `queue-cf-vendor-map.md`, with the wave-9 corrections.
- `queue-batch29-fit-ledgers.md`, with the wave-14 corrections.
- `queue-give-interactive-displacement.md`, with the wave-5 corrections.
- `queue-vendor-channel-moves.md`, wave-6 correction 1: CCT's GiftingNetwork portal is documented from 2024-02-06.
- `queue-ren-iphi-attrition.md`.
- `spectrumportal-tenant-audit.csv`.

**Labels:**
- [F] first-party text or a filed government record
- [V] vendor statement
- [H] HTTP or DNS observation
- [S] search-engine extract (page not opened)
- [I] inference

**Outputs:**

| File | Content |
|---|---|
| `scripts/mission_cf_vendor_close.py` | P-CFV-02 closure passes and the P-B29A-02 split. Reuses the v1 crawler (`mission_cf_vendor_map.py`). Stdlib, functional, cached |
| `scripts/mission_give_tenant_lapses.py` | P-GIV-06/07: certificate spans per Give tenant, the public-evidence table and the $40B claim reconciliation |
| `data/mission-2026-11-14/cf-vendor-map-by-ein-v2.csv` | All 803 CFs: the v1 columns plus `change_note` |
| `data/mission-2026-11-14/cf-vendor-close-signals-v2.csv` | Every new signal for the 315 v1-unmapped CFs (313 rows) |
| `data/mission-2026-11-14/cf-vendor-close-handchecks-batch30.csv` | Hand checks (WebFetch and filings) read by the script |
| `data/mission-2026-11-14/cf-vendor-map-summary-v2.json` | Coverage and v1-versus-v2 vendor shares |
| `data/mission-2026-11-14/spectrumportal-portal-vs-ledger-v2.csv` | The 14 Foundation Cloud rows, split |
| `data/mission-2026-11-14/give-tenants-lapses-batch30.csv` | 10 Give tenant rows (identity, lapse, replacement) |
| `data/mission-2026-11-14/give-claim-reconciliation-batch30.csv` | Known Give clients against the "$40B+" claim |
| `data/mission-2026-11-14/queue-proposals-batch30c.csv` | P-B30C-01 to P-B30C-03 |

---

## 0. Headline answers

| ID | Answer | Confidence |
|---|---|---|
| **P-CFV-02** | **65 of the 315 unmapped CFs now carry a vendor signal. 21 are at high or medium confidence, holding $1.68bn (2.54% of CF DAF assets); 44 are low-confidence DNS candidates ($0.49bn, 0.74%).**<br>- Unmapped share: 39.2% → **31.1%** by count, and 6.1% → **2.8%** by DAF assets.<br>- Of the 20 largest, 10 are closed at high or medium, 1 is a low candidate, 3 show no online fund portal and 6 remain blocked or unresolved.<br>- **Foundant's count share is still a floor: 46.5% (high/medium)**, up from 45.0%, and 51.7% if every low candidate holds.<br>- **Asset shares barely move:** Salesforce 23.7% → 24.8% (Arizona CF and CFSEM), Foundant 32.7% → 33.7%.<br>- 250 CFs remain unmapped; 210 of them hold under $10m. | High for the 21; low for the 44 candidates. One verified label collision (bcf → Bainbridge) |
| **P-B29A-02** | **None of the 14 Foundation Cloud (spectrumportal.net) rows is evidenced as an NPact ledger.**<br>- **5 run their portal over Blackbaud ($1.91bn, 81% of the group's $2.36bn):** CFES (high: FIMS → RE/FE NXT plus NPact tools, 2022–23), GWCF (medium), San Diego (low: undated Blackbaud case study), Tulsa (low: posting) and Kalamazoo (low).<br>- **1 is possibly NPact-hosted:** Santa Barbara, which pays Fusion Labs $130k for "hosted infrastructure".<br>- **7 have no GL evidence ($0.29bn).**<br>- **1 is not a fund portal:** New Mexico, a partner/grantee portal.<br>- **Recommendation:** treat `spectrumportal.net` as a portal layer (`ledger_implied` = no or unknown) and drop the NPACT "portal_suite_implied" ledger rows | High that the "portal ⇒ NPact ledger" rule fails; low to medium per row |
| **P-GIV-06** | **`nhf` and `jttw` stay unresolved, `tc-innov` stays a weak Thrivent inference, and `jmacarthurtrust`/`jmctdaf` stays at medium.**<br>- **`nhf`:** New Horizons Foundation Inc (84-1123082, Colorado Springs, $79m DAFs) is the only DAFRC sponsor with these initials, but no page links it to Give.<br>- **`jttw`:** no acronym match anywhere.<br>- **Gap in Give's claim:** known clients hold $36.74bn of FY2024 DAF assets, $3.26bn short of Give's "$40B+ live or in implementation (2025)" | Low |
| **P-GIV-07** | **Give lost five CF tenants holding $4.79bn of DAF assets. Only EBCF is shown live on Give, and none returned to Ren/iPhi.**<br>- **EBCF:** Give portal used by fund advisors (page of 2023-11-16) → akoyaGO GOfund ("almost ready" 2025-07-09); Give certificates stop 2026-03-27.<br>- **Omaha:** Give 2022–23 tenants (`omahafoundation`, probably `ocf-*`) → Foundant fundholder portal launched **2024-07-30**.<br>- **FFTC:** Give 2022-01 to 2024-02 ($654,500 in CY2023) → NPact Foundation Cloud on FE NXT (story 2025-03-07) → **GiftingNetwork since 2026-07-01**.<br>- **Kalamazoo and San Diego:** trials alongside Foundation Cloud portals that stayed in place.<br>- **No CF states a reason.**<br>- The 2025-04-20 `ocf.iphiview.com` certificate was a seven-name batch and the host is NXDOMAIN, so it is not evidence of a return | High on sequences and dates (EBCF, Omaha, FFTC); none on reasons |

---

## 1. P-CFV-02: closing the unmapped CFs

### 1.1 Method

`python3 scripts/mission_cf_vendor_close.py --fetch --cache-dir <dir>` runs over the 315 rows with `vendor_family = Unmapped` in v1. A rerun without `--fetch` rebuilds from the cache.

| Pass | What it does | Yield (decisive) |
|---|---|---|
| 1. Website | v1 homepage, or `<WebsiteAddressTxt>` from up to 8 harvested e-filed 990s | 0 new websites for the 37 with none |
| 2. Fresh crawl | v1 crawler (homepage + 3 internal login-like pages + 3 portal links) | Folded into passes 3–4 |
| 3. Raw-HTML scan | DAF-specific vendor hosts anywhere in the page source (menus built in JS are missed by anchor parsing) | 7 |
| 4. Login pages | sitemap.xml URLs with login-like paths, or else `/login/`, `/donor-login/`, `/fund-login/`, `/fundholder-login/`, `/donor-portal/`, `/fund-holders/` (at most 4 pages) | 4 |
| 5a. Own-domain DNS | CNAME chain for `donor`, `donors`, `portal`, `myfund`, `fund`, `giving`, `mycf`, `login`, `donorportal`, `fundportal` | 1 (CFSEM `mycf.cfsem.org` → `live.siteforce.com`, Salesforce) |
| 5b. Vendor-zone DNS | A record for `<domain stem>.<zone>` in zones confirmed at run time to have **no wildcard** (random label NXDOMAIN): `fcsuite.com`, `iphiview.com`, `spectrumportal.net`, `giveinteractive.com`. The stem must be unique among the 803 CFs. `donorsphere.org`, `donorcentral.com` and `donor-portal.org` are wildcards and are not used | 42 low candidates |
| 6. 990 full text | Latest harvested 990 XML (Schedules O and I, Part IX, VII-B) searched for vendor names. Word-bounded, after a false positive on the misspelling "FOUNDANTION" | 2 (Bryan, Battle Creek) + Miami (hand check) |
| 7. Repo cross-reference | `cf-ledger-families-2026(-v2).csv` and `ren-iphi-tenant-census.csv` (active tenants) | 1 (Warren County, `wccf.iphiview.com`) |
| 8. Hand checks | WebFetch reads of the 20 largest unmapped CFs (`cf-vendor-close-handchecks-batch30.csv`) | 6 first-party, 2 secondary, 1 exclusion, 5 "no portal" |

**Decision rule.** The strongest signal wins. The order of strength is:
1. First-party portal links, CNAMEs and hand checks;
2. a 990 text mention;
3. a vendor-zone DNS hit.

Confidence: a vendor link from the CF's own pages is **high**. A filing quote or a raw-HTML-only link is **medium**. A DNS label alone is **low**, and stays out of the share tables. Competing signals go in `conflicting_signals`.

### 1.2 Results

| Outcome | CFs | FY2024 DAF assets | Share of CF DAF assets ($66.14bn) |
|---|---|---|---|
| Closed, high | 15 | $1,311m | 1.98% |
| Closed, medium | 6 | $368m | 0.56% |
| Candidate, low (42 DNS + 2 990 text) | 44 | $486m | 0.74% |
| Still unmapped | 250 | $1,856m | 2.81% |

**Unmapped CFs that changed by evidence type:** 42 vendor-zone DNS, 7 raw HTML, 6 hand check (first-party), 4 login page, 2 hand check (secondary), 2 990 text, 1 CNAME, 1 Ren census.

**Vendor shares, v1 → v2.** Count shares use 803 CFs; asset shares use $66.14bn. Only high and medium rows count.

| Family | CFs v1 → v2 | Count share | DAF-asset share |
|---|---|---|---|
| Foundant | 361 → 373 | 45.0% → 46.5% | 32.7% → 33.7% |
| akoyaGO | 48 → 52 | 6.0% → 6.5% | 3.2% → 3.4% |
| Salesforce | 19 → 21 | 2.4% → 2.6% | 23.7% → 24.8% |
| Ren / Stellar iPhi | 22 → 23 | 2.7% → 2.9% | 5.9% → 5.9% |
| Foundation Cloud | 14 → 16 | 1.7% → 2.0% | 3.6% → 3.7% |
| Low-confidence only | 5 → 49 | 0.6% → 6.1% | 0.2% → 0.9% |
| Unmapped | 315 → 250 | 39.2% → 31.1% | 6.1% → 2.8% |

### 1.3 The 20 largest v1-unmapped CFs

| CF | DAF $m | v2 result | Evidence |
|---|---|---|---|
| Arizona CF | 424 | **Salesforce, high** | "Login Now" (ACF Connect) → `azfoundation.my.site.com` ([access-your-fund](https://www.azfoundation.org/access-your-fund/)) [F]. GL: Sage Intacct per the ledger file |
| CF for Southeast Michigan | 331 | **Salesforce, high** | `mycf.cfsem.org` CNAME `…live.siteforce.com`, `x-sfdc-trace-flags` header [H]; linked as "MyCF" from cfsem.org [F] |
| Baltimore CF | 181 | Unmapped (candidate rejected) | `bcf.fcsuite.com` exists, but its donate list links `bainbridgecf.org` (Bainbridge CF). bcf.org refuses scripted and WebFetch reads |
| Miami Foundation | 174 | **Foundant, medium** | TY2025 990 Schedule I: "Payments are processed using CSUITE, the Foundation's financial software, which is fully integrated with Foundant's grant management software" ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202632599349301468_public.xml)) [F]. `miamifoundation.spectrumportal.net` also resolves (conflict) |
| Hampton Roads CF | 154 | **Foundant, high** | Top nav "FundXPress" → `hamptonroadscf.fcsuite.com/erp/portal` (WebFetch) [F] |
| Armstrong County CF | 148 | No online fund portal found | Firespring site, no login link (WebFetch) |
| Blue Grass CF | 133 | **Foundant, medium** | `bgcf.fcsuite.com` resolves and its sign-in page linked `www.bgcf.org` (one fetch, before the robots review). `bgcf.spectrumportal.net` also resolves. Homepage refuses reads |
| Greater Kanawha Valley | 129 | Foundant, low | `tgkvf.fcsuite.com` resolves (DNS only) |
| High Point CF | 93 | No online fund portal found | "Donor Advisement Form" only |
| Erie CF | 90 | **akoyaGO, high** | Login page link → `gofund.akoyago.com/eriecommunityfoundation` [F] |
| CF (inspiringgood.org) | 79 | Unmapped | 403 to script and WebFetch |
| East Tennessee Foundation | 78 | Unmapped | Refuses reads |
| West Bend CF | 74 | Unmapped | No website on any harvested 990 |
| CF of Greenville | 67 | **Foundation Cloud, high** | "Fundholder Login" → `cfgreenville.spectrumportal.net` [F] |
| Lakeshore CF | 55 | No login on homepage | "For Our Donor Advised Fund Clients" page not opened |
| CF Boulder County | 55 | **akoyaGO, high** | "Fund Login" → `gofund.akoyago.com/CFBC` [F] |
| Permian Basin AF | 53 | **Foundant, high** | Login page → `permianbasin.fcsuite.com/erp/portal` [F] |
| Wichita Falls Area CF | 53 | Unmapped | Refuses reads |
| Hamilton County CF | 51 | Unmapped | Script certificate error; WebFetch 503 |
| CFs of the Hudson Valley | 42 | **Foundant, high** | "Donor Portal" → `cfhvny.fcsuite.com/erp/fundmanager/list` [F] |

Ventura County CF ($40m, rank 23) also closed: "Access My Fund" → `vccf.spectrumportal.net/accounts/signin` [F].

### 1.4 The residual 250

| Reason | CFs |
|---|---|
| Homepage read with no vendor signal on any pass | 159 |
| Transport refusal, not worked around | 42 |
| No website on any harvested 990 | 37 |
| HTTP 403/404/5xx | 9 |
| robots.txt disallow | 3 |

Most are small (210 hold under $10m). Hand checks show a real **"no online fund portal"** category. Of the 12 hand-checked homepages that loaded, 7 linked a vendor portal and 5 showed no fund login (Armstrong, High Point, Lakeshore, Savannah and the Pi Fund). An unmapped row is therefore not always a missed vendor.

### 1.5 Directories and certificate data

- **No public Foundant client directory or map was found.** Foundant pages name examples only ([CF landing page](https://www.foundant.com/lp-community-foundations/)) [S].
- **akoyaGO** serves tenants by path on `gofund.akoyago.com`, and its robots.txt is `Disallow: /`, so it cannot be enumerated.
- **Certificate data (CT) is not usable for Foundant or iPhi**, because both use wildcard certificates (v1 §8).
- **What works is DNS on vendor zones without a wildcard.** It shows a tenant exists, but not whose it is. Baltimore shows that a short stem can belong to another foundation. This is proposal P-B30C-01.

### 1.6 Limitations

- **The 44 low rows are candidates.** Label collisions are possible, and one is verified.
- **The homepage + 1 click + DNS method** misses logins kept in PDFs or newsletters, or placed deeper on the site.
- **Hand checks covered the top 20 plus Ventura.** WebFetch summaries come from a model reading the page; each closing link was a quoted URL.
- **990 text covers only the latest return** for each CF.
- **Portal is not ledger.** The `ledger_implied` rules from v1 apply. Salesforce rows say nothing about the GL.
- **DAF assets** are DAFRC FY2024 `eoy_daf_assets`.

---

## 2. P-B29A-02: Foundation Cloud portal versus ledger

All 14 rows sat in `cf-ledger-families-2026.csv` as NPACT "portal_suite_implied". [`spectrumportal-portal-vs-ledger-v2.csv`](../../data/mission-2026-11-14/spectrumportal-portal-vs-ledger-v2.csv) gives the split below; the v2 map sets `ledger_implied` accordingly.

| Class | Rows | DAF $m | Share of group | Members (confidence) |
|---|---|---|---|---|
| Portal over Blackbaud FE NXT | 3 | 1,140 | 48.4% | CFES (high), GWCF (medium), San Diego (low) |
| Portal over Blackbaud (product inferred) | 2 | 771 | 32.7% | Tulsa (low), Kalamazoo (low) |
| NPact-hosted, ledger possible | 1 | 152 | 6.5% | Santa Barbara (low) |
| Portal, GL not evidenced | 7 | 289 | 12.3% | Nevada, Amarillo, Montana, Frederick, Door County, NW Minnesota, Initiative Foundation |
| Not a fund portal | 1 | 5 | 0.2% | New Mexico (partner/grantee portal) |

**Evidence by row:**
- **CFES ($28.7m):** "[I]n August 2022 we began a transition" from FIMS ("Since 1998") to "Blackbaud's Raiser's Edge and Financial Edge" with "additional tools from NPact". Fundholders were invited to `cfes.spectrumportal.net` "As of April 23" (the page was updated 2023-04-24) ([cfes.org/transition](https://www.cfes.org/transition)) [F].
- **San Diego ($708m):**
  - The Blackbaud case study (undated, describing COVID-era remote work) says SDF "migrated from on-premises systems" to RE NXT and FE NXT ([casestudies.com](https://www.casestudies.com/company/blackbaud/case-study/the-san-diego-foundation-customer-case-study)) [V].
  - MySDF logins point to `sdfoundation.spectrumportal.net/accounts/signin` ([donor resources](https://www.sdfoundation.org/ways-to-give/current-donor-resources)) [F].
  - Confidence is low because the case study is undated.
- **Tulsa ($694m):** an Accounting Clerk posting ("Posted 6+ months ago") asks for "Experience with QuickBooks, Raiser's Edge, Financial Edge (preferred), Bill.com/DIVVY" ([ffwd copy](https://jobs.ffwd.org/companies/idealist/jobs/66859314-accounting-clerk)) [F, undated]. The Paylocity original is inactive.
- **GWCF:** batch 29 v2 row (Donor Central replaced, Blackbaud REPAY, 990 Blackbaud line). **Kalamazoo:** Blackbaud NXT donation forms on its homepage (tenant audit). **Santa Barbara:** TY2024 990 FUSION LABS INC "HOSTED INFRASTRUCTURE" $130,000.

**Readings:**
- **Every tenant with any GL evidence runs Blackbaud under Foundation Cloud.** That includes FFTC and CFGP from batch 29, which are outside this 14-row set [I].
- **New tenants.** Greenville and Ventura (§1.3), plus Miami and Blue Grass as DNS-only conflicts, add to the portal footprint. They add nothing to an NPact ledger count.

---

## 3. P-GIV-06: unresolved Give tenants

Certificate spans come from crt.sh (`%.giveinteractive.com`, full export of 2026-11-15, read by the script).

| Label | Certificates (first … last issued) | Best candidate | Evidence | Confidence |
|---|---|---|---|---|
| `nhf` | staging 2025-10-23…2026-09-01; production 2026-04-08…2026-09-22; SFTP 2026-10-05 | New Horizons Foundation Inc, 84-1123082, Colorado Springs; fiscal sponsor + DAF; FY2024 DAF assets $79.4m, 287 DAF accounts | Only DAFRC sponsor with initials NHF above $10m [I]. Website refuses reads; TY2023–24 990 XML names no vendor ([TY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503219349306440_public.xml)). National Heritage Foundation ($0 assets 2022) and NH Charitable Foundation (Foundant) are excluded | low |
| `jttw` | staging 2025-10-15…2026-09-01; production 2026-01-29…2026-09-01 | none | No DAFRC initials match (stopwords kept or dropped); no web use of the acronym; single-name certificates | none |
| `tc-innov` | not in crt.sh on 2026-11-15 (certspotter-only in batch 23) | Thrivent Charitable (weak) | `vc-`/`ia-`/`jcf-innov` pattern; Thrivent's own hosts are `thriventcharitable-staging` (2026-08-14) and `thrivent-sftp.int` (2026-10-05) | low |
| `jmacarthurtrust`, `jmctdaf` | staging 2025-03-04; production 2025-05-01…2026-08-01; `jmctdaf-staging` 2025-06-03…2026-07-14 | John MacArthur Charitable Trust, 83-0981937 (Newhall CA, ruling 2019) | Name match. The trust page `gracechurch.org/macarthur-trust` now returns 404; the search snippet says "support for the operations, development, and expansion of key partner ministries" [S]. No DAF program or Give link is shown; not a DAFRC sponsor | medium (unchanged) |

**$40B reconciliation** ([`give-claim-reconciliation-batch30.csv`](../../data/mission-2026-11-14/give-claim-reconciliation-batch30.csv)):
- **Known clients:** Vanguard 21.95, CCT 4.65, ImpactAssets 3.63, JCF 2.87, Servant/Signatry 1.41, Minneapolis 0.60, Thrivent 0.59, WaterStone 0.54 and Stifel 0.49, totalling **$36.74bn**.
- **Give's claim:** "$40B+ live or in implementation (2025)" ([giveinteractive.com/company](https://www.giveinteractive.com/company)) [V].
- **The gap of $3.26bn** must come from `nhf`, `jttw`, the trust, or a different measure such as total rather than DAF assets [I].
- **New Horizons alone would not close it.**

---

## 4. P-GIV-07: why Give tenants lapsed, and what replaced them

| Sponsor (DAF $bn) | Give certificates | Live on Give? | Replacement and timing | Sources |
|---|---|---|---|---|
| **East Bay CF** (0.53) | sandbox 2023-02-08; production 2023-06-06…**2026-03-27** | **Yes.** The campaign page (modified 2023-11-16) tells fund advisors to use the "Give Interactive donor portal" at `ebcf.giveinteractive.com` [F] | **akoyaGO GOfund.** "Our new donor portal is almost ready" (published **2025-07-09**): "final stages of launching our new and improved donor portal … addressing a few final technical issues" [F]. The site now links `gofund.akoyago.com/eastbay` | [campaign page](https://www.ebcf.org/donate-to-the-campaign-for-a-just-east-bay/); [portal notice](https://www.ebcf.org/our-new-donor-portal-is-almost-ready/) |
| **Omaha CF** (0.52) | `omahafoundation` 2023-05-03…2023-10-31; `ocf-*` (sandbox, staging, one `ocf-prod`) 2022-04-06…2023-12-07 | Not shown | **Foundant CommunitySuite.** "we launched a new online fundholder portal"; invitations "on July 30" (post of **2024-07-29**); login `omahafoundation.fcsuite.com`. Redesign 2025-03-04 [F] | [launch post](https://omahafoundation.org/news/ocf-launching-new-online-fundholder-portal-july-30/); [redesign](https://omahafoundation.org/news/your-ocf-online-account-has-a-new-look/) |
| **FFTC** (2.95) | sandbox 2022-01-10…2024-02-12; `myfftc` 2023-11-07…2024-01-06 | Not shown. Paid $654,500 "SOFTWARE" in CY2023 [F]; no Give line in CY2024 (5th payee $101,200) | **NPact Foundation Cloud + Blackbaud FE NXT** (NPact story 2025-03-07, "less than eight months") [V], then **GiftingNetwork**: "has been running a new donor portal on the GiftingNetwork platform since July 1, 2026" (release dated 2026-09-23) [V]. A Q1 2026 spotlight listed an "enhanced fundholder portal" as coming soon [S] | [990 CY2023](https://projects.propublica.org/nonprofits/organizations/566047886/202433209349318318/full); [NPact](https://npact.com/customer-stories/foundation-for-the-carolinas/); [PRLog](https://www.prlog.org/13172546-giftingnetworks-donor-portal-live-at-foundation-for-the-carolinas.html) |
| **Kalamazoo CF** (0.08) | staging 2024-06-20; production 2024-07-22…2025-10-19 | Not shown | **None.** The existing Foundation Cloud "Kalamazoo Connect" (`kalfound.spectrumportal.net`) is still linked (homepage modified 2026-11-12) [F]. A May 2023 notice took Kalamazoo Connect offline for an upgrade with new-account invitations [S; page now 404]. Give was trialled after it [I] | [kzcf.org](https://kzcf.org/) |
| **San Diego Foundation** (0.71) | staging only, 2025-04-15…2025-10-12 | No | **None.** MySDF on `sdfoundation.spectrumportal.net` over RE/FE NXT (§2) | [donor resources](https://www.sdfoundation.org/ways-to-give/current-donor-resources) |

**Answers:**
- **Why Give lapsed.** No sponsor gives a public reason. The pattern is that Give lost to **integrated CF suites**: Foundant at Omaha and akoyaGO at EBCF. At FFTC it lost to a **portal on an existing Blackbaud GL**: first NPact, then GiftingNetwork. At KZCF and SDF, Give was evaluated against Foundation Cloud and the incumbent stayed [I].
- **Live losses.** Only EBCF was a demonstrated live loss, after about 2.5 years (2023-06 to 2026-03).
- **Return to Ren/iPhi.** None.
  - `ocf.iphiview.com` was certified on 2025-04-20 in a ZeroSSL batch with `cafa`, `ccfnj`, `eqt`, `rj`, `www` and `maintenance`. It is now NXDOMAIN, and its owner is unattributed (repo Ren census).
  - Omaha is on Foundant and Oregon CF on Salesforce (`oregoncf.my.site.com/MyOCF_login`).
- **Durability.** The five lapsed tenants ($4.79bn of DAF assets) are mostly CFs. Give's live and pipeline book is national, faith-based and Ren-iPhi sponsors (batch 23 §2). The churn record is about community foundations [I].

---

## 5. Corrections to existing repo text (proposed)

1. **`cf-ledger-families-2026-v2.csv`, FFTC `product`.**
   - The product text reads "GiftingNetwork (Give Interactive) donor portal daf.fftc.org".
   - Change it to: "GiftingNetwork donor portal daf.fftc.org (live 2026-07-01 per GiftingNetwork release)".
   - GiftingNetwork is a separate, founder-led firm (`private-equity-daf-ecosystem-map.md`), not a Give product. FFTC's Give tenants lapsed in 2024.
2. **`cf-ledger-families-2026.csv`, the 12 NPACT "portal_suite_implied" rows** (GWCF was already moved in batch 29 v2).
   - Replace them with the classes in §2.
   - CFES moves to BLACKBAUD_FE (high).
   - San Diego, Tulsa and Kalamazoo move to Blackbaud (low).
   - Santa Barbara stays NPACT (low).
   - The other 7 become UNRESOLVED (portal only).
3. **`queue-give-interactive-displacement.md` §0 item 6 and `queue-processor-economics-vendor-profiles.md` (Lapsed: FFTC, OCF, Omaha, …).**
   - Read "OCF" as probably Omaha CF; it is one sponsor, not two.
   - Add: "only EBCF is shown live on Give; Omaha moved to Foundant 2024-07-30; EBCF to akoyaGO (notice 2025-07-09)".
4. **`queue-cf-vendor-map.md` §5, Give CF tenants.** EBCF's production host ran from 2023-06-06 to 2026-03-27 and was linked for fund advisors in 2023. It is a lapsed live tenant, not a certificate-only signal.

---

## 6. Source register

| # | Source | Type | Date | URL |
|---|---|---|---|---|
| S1 | Arizona CF access-your-fund | sponsor [F] | live 2026-11-15 | https://www.azfoundation.org/access-your-fund/ |
| S2 | CFSEM MyCF; dns.google CNAME | sponsor [F]/[H] | 2026-11-15 | https://cfsem.org/mycf/ ; https://dns.google/resolve?name=mycf.cfsem.org&type=CNAME |
| S3 | Hampton Roads CF homepage | sponsor [F] | live | https://www.hamptonroadscf.org/ |
| S4 | Miami Foundation TY2025 990 Schedule I | 990 [F] | TY2025 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202632599349301468_public.xml |
| S5 | CF Greenville; VCCF access page; CF Boulder County; CFs of Hudson Valley | sponsor [F] | live | https://cfgreenville.org/ ; https://vccf.org/my-vccf-fund/access-my-fund/ ; https://www.commfound.org/ ; https://www.communityfoundationshv.org/ |
| S6 | Foundant fcsuite.com robots.txt | vendor [H] | 2026-11-15 | https://bcf.fcsuite.com/robots.txt |
| S7 | CFES transition page | sponsor [F] | 2023-04-24 | https://www.cfes.org/transition |
| S8 | Blackbaud case study, San Diego Foundation | vendor [V] | undated | https://www.casestudies.com/company/blackbaud/case-study/the-san-diego-foundation-customer-case-study |
| S9 | SDF current donor resources | sponsor [F] | live | https://www.sdfoundation.org/ways-to-give/current-donor-resources |
| S10 | TCF Accounting Clerk posting (ffwd copy) | posting [F] | "6+ months ago" | https://jobs.ffwd.org/companies/idealist/jobs/66859314-accounting-clerk |
| S11 | crt.sh %.giveinteractive.com export | CT [H] | 2026-11-15 | https://crt.sh/?q=%25.giveinteractive.com |
| S12 | New Horizons Foundation 990s | 990 [F] | TY2023–24 | https://projects.propublica.org/nonprofits/organizations/841123082 |
| S13 | John MacArthur Charitable Trust | registry [S] | ruling 2019 | https://www.guidestar.org/profile/83-0981937 |
| S14 | Give Interactive company page ($40B+) | vendor [V] | live | https://www.giveinteractive.com/company |
| S15 | Give fund-of-funds release | press [V] | 2026-07-21 | https://pulse2.com/give-interactive-launches-fund-of-funds-platform-for-daf-sponsors-and-private-foundations/ |
| S16 | EBCF campaign page; portal notice | sponsor [F] | 2023-11-16; 2025-07-09 | https://www.ebcf.org/donate-to-the-campaign-for-a-just-east-bay/ ; https://www.ebcf.org/our-new-donor-portal-is-almost-ready/ |
| S17 | Omaha CF portal launch and redesign posts | sponsor [F] | 2024-07-29; 2025-03-04 | https://omahafoundation.org/news/ocf-launching-new-online-fundholder-portal-july-30/ ; https://omahafoundation.org/news/your-ocf-online-account-has-a-new-look/ |
| S18 | GiftingNetwork release on FFTC | vendor [V] | 2026-09-23 | https://www.prlog.org/13172546-giftingnetworks-donor-portal-live-at-foundation-for-the-carolinas.html |
| S19 | FFTC 990 CY2023 (Give $654,500) | 990 [F] | CY2023 | https://projects.propublica.org/nonprofits/organizations/566047886/202433209349318318/full |
| S20 | NPact FFTC story | vendor [V] | 2025-03-07 | https://npact.com/customer-stories/foundation-for-the-carolinas/ |
| S21 | Kalamazoo CF homepage; May 2023 Kalamazoo Connect notice | sponsor [F]/[S] | 2026-11-12; 2023-05 | https://kzcf.org/ ; https://kalfound.org/news/kalamazoo-connect-and-give-now-page-unavailable-may-18-30 |
| S22 | Ren iPhi tenant census (ocf) | repo | 2026-11-15 | data/mission-2026-11-14/ren-iphi-tenant-census.csv |

---

## 7. Data dictionary

### `cf-vendor-map-by-ein-v2.csv` (803 rows)

The columns are the v1 columns (see `queue-cf-vendor-map.md` §9) plus `change_note`. Rows that changed get these values:

| Column | v2 meaning |
|---|---|
| `evidence_type` | v1 values, plus: `raw_html_vendor_host`, `login_path_vendor_host`, `vendor_zone_dns_label` (DNS only, low), `990_text_vendor_name`, `repo_ren_census_live`, `hand_check_first_party`, `hand_check_secondary` |
| `confidence` | high (first-party link, CNAME or hand check); medium (filing quote, raw-HTML-only link or secondary hand check); low (DNS label or 990 text alone) |
| `crawl_status` | `v2:<status>` for re-crawled rows. `homepage_error_transport_not_cached` means a transport refusal |
| `retrieved` | 2026-11-15 for changed rows |
| `ledger_implied` | For the 14 Foundation Cloud rows: `no` (portal over Blackbaud, or not a fund portal), `yes` (NPact-hosted), `unknown` |
| `change_note` | `unchanged (v1)`; `unmapped -> <family> (<confidence>) via <evidence_type>`; `still unmapped after v2 passes` (with any hand-check note); `P-B29A-02 split: …` |

### `cf-vendor-close-signals-v2.csv`

| Column | Meaning |
|---|---|
| `ein`, `name` | CF identity |
| `family`, `product`, `ledger_implied` | Vendor signal (blank for notes and exclusions) |
| `evidence_type` | As above, plus `note` (login pages tried), `hand_check_no_portal`, `hand_check_exclude`, `repo_ledger_families` |
| `evidence_url` | Source |
| `detail` | Detail or quote |
| `strength` | Ordinal strength |

### `cf-vendor-close-handchecks-batch30.csv`

| Column | Meaning |
|---|---|
| `ein`, `name` | CF identity |
| `family`, `product`, `ledger_implied` | Vendor finding |
| `evidence_type` | `hand_check_first_party`, `hand_check_secondary`, `hand_check_exclude`, `hand_check_no_portal` or `split_only` |
| `source_url`, `detail` | Source and quote |
| `split_class`, `ledger_reading`, `confidence` | Used only for P-B29A-02 rows |
| `checked` | Date of the check |

### `spectrumportal-portal-vs-ledger-v2.csv` (14 rows)

| Column | Meaning |
|---|---|
| `ein`, `name`, `fy2024_daf_assets_usd`, `portal_url` | From the v1 map |
| `split_class` | `portal over Blackbaud FE NXT`, `… (inferred)`, `portal over Blackbaud (inferred)`, `NPact-hosted (ledger possible)`, `portal; GL not evidenced` or `not a fund portal (partner/grantee portal)` |
| `ledger_reading` | Proposed `cf-ledger-families` value |
| `confidence` | high / medium / low / none |
| `basis` | Evidence summary |
| `ledger_families_v1` | Prior value |
| `retrieved` | Date |

### `give-tenants-lapses-batch30.csv` (10 rows)

| Column | Meaning |
|---|---|
| `queue_item` | P-GIV-06 or P-GIV-07 |
| `label_pattern` | Tenant label regex |
| `ct_hosts_first_last_issued`, `ct_first_issued`, `ct_last_issued`, `ct_last_expiry` | 2021+ crt.sh certificate spans |
| `candidate_org`, `ein`, `fy2024_daf_assets_usd` | Candidate identity |
| `status_2026_11_15` | Tenant status |
| `replacement_or_current_vendor`, `replacement_timing` | What replaced Give, and when |
| `evidence`, `confidence`, `sources`, `retrieved` | Support for the row |

### `give-claim-reconciliation-batch30.csv`

| Column | Meaning |
|---|---|
| `ein`, `name` | Known client |
| `basis` | Why it counts as a client |
| `fy2024_daf_assets_usd` | DAFRC FY2024 DAF assets |

The file ends with a total row and a gap-to-$40bn row.

### `queue-proposals-batch30c.csv`

Follows the format in `queue-proposals-README.md`: P-B30C-01 (verify the DNS candidates and blocked homepages), P-B30C-02 (GL behind Foundation Cloud tenants), P-B30C-03 (`nhf`/`jttw` and the $40B gap).

## Validation corrections (wave 15, 2026-11-15) — governing
Source: [validation-wave15-report.md](validation-wave15-report.md); register `data/mission-2026-11-14/validation-register-wave15.csv`.

1. **Line 56 (§0, P-B29A-02).** Replace "CFES (high: FIMS → RE/FE NXT plus NPact tools, 2022–23)" with "CFES (high: FIMS → Blackbaud Raiser's Edge and Financial Edge, NXT generation inferred, plus NPact tools, 2022–23)".
2. **Line 173 (§2 table).** Replace "| Portal over Blackbaud FE NXT | 3 | 1,140 | 48.4% | CFES (high), GWCF (medium), San Diego (low) |" with "| Portal over Blackbaud FE (NXT stated or inferred) | 3 | 1,140 | 48.4% | CFES (high; 'Financial Edge', NXT not stated), GWCF (medium), San Diego (low) |".
3. **Line 58 (§0, P-GIV-07).**
   - Replace: "**Give lost five CF tenants holding $4.79bn of DAF assets. Only EBCF is shown live on Give, and none returned to Ren/iPhi.**"
   - With: "**Five CFs that held Give hosts ($4.79bn of DAF assets) did not stay on Give. Only one live loss is demonstrated: EBCF, $0.53bn. Omaha and FFTC had production-labelled hosts with no shown live use, Kalamazoo and San Diego were trials, and none returned to Ren/iPhi.**"
4. **Line 229 (§4 Durability).** Replace "The five lapsed tenants ($4.79bn of DAF assets)" with "The five CFs with lapsed Give hosts ($4.79bn of sponsor DAF assets, not Give AUM)".
5. **Line 208 (§3, gap bullet).** Append: "The gap compares FY2024 DAF assets with a 2025 claim, and it includes staging-only clients (Minneapolis, Thrivent, Stifel). Asset growth alone could close it [V wave 15]."
6. **Line 160 (§1.6).** Replace "**Hand checks covered the top 20 plus Ventura.**" with "**Hand checks covered the top 20 plus Ventura, Savannah and the Pi Fund.**"
7. **Line 114 (§1.3, Arizona row).** Append to Evidence: "Wave 15 could not re-read the sponsor page (403, and WebFetch returned nothing). The tenant `azfoundation.my.site.com` is confirmed to exist (it 301-redirects to `/s/`)."

## Compliance note (2026-11-15) — governing
crt.sh disallows all crawlers in its robots.txt. Any claim in this document that rests **only** on crt.sh certificate data is downgraded to an unverified lead until re-sourced. See [compliance-note-crtsh-robots.md](compliance-note-crtsh-robots.md).
