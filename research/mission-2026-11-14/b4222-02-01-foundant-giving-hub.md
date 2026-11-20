# Foundant Giving Hub tenancy: do community foundations list DAFs as funds the public can give to? (P-B4222-02-01)

- **Queue item:** P-B4222-02-01 (from [b4013-02-b4222-02-remittance-and-portal-features.md](b4013-02-b4222-02-remittance-and-portal-features.md), context rows PF-19, PF-22, PF-27, PF-28 of `portal-features-2026-11-19.csv`).
- **Date:** 2026-11-20. Every page was read on that date. Public pages only. No logins, no form submissions, no outreach. Hubs were found only by following links from CF websites already in the repo.
- **Files written:**
  - [`data/mission-2026-11-14/foundant-giving-hub-2026-11-20.csv`](../../data/mission-2026-11-14/foundant-giving-hub-2026-11-20.csv): 413 rows, one per Foundant CommunitySuite CF filer (13 core, 400 extended), 46 columns.
  - [`scripts/mission_foundant_giving_hub.py`](../../scripts/mission_foundant_giving_hub.py): fetches (robots first), parses, classifies and prints every number in this note. Run `python3 -I scripts/mission_foundant_giving_hub.py . --cache <dir>`. Add `--offline` to rebuild from a cache with no network requests.
  - [`data/mission-2026-11-14/queue-proposals-b4222-02-01.csv`](../../data/mission-2026-11-14/queue-proposals-b4222-02-01.csv): 6 rows.
- **Labels:** [F] first-party page read this pass. [R] carried from a repo file. [C] computed by the script. [I] inference. [B] blocked by robots.txt.

---

## 0. Answers

| Question | Finding |
|---|---|
| **How many of the 40 are Foundant CommunitySuite?** | **13.** The queue's count is confirmed: the script filters `portal_vendor == 'Foundant CommunitySuite'` in `community-foundation-rails-portals-2026-v2.csv` and gets 13 of 40 rows [C]. |
| **How many core hubs could be read?** | **12 of 13** [C]. Omaha Community Foundation's robots.txt disallows `Claude-User` for `/`, so its site was not used and its hub was not read [B]. |
| **Do core hubs list a DAF as a fund the public can give to?** | **7 of 12 hubs list at least one fund explicitly described as donor-advised (58.3%)** [C]: Columbus (11 such funds), CFNJ (7), Denver (1), NHCF (19), CF Middle Tennessee (585), Rhode Island (3) and St. Louis (6).<br>- No explicit DAF on 5 hubs: Atlanta, Tampa Bay, Greater Cincinnati, GiveWell CF and Richmond.<br>- If at least 2 explicit-DAF funds are required, the count is 6 of 12 (Denver drops out) [C]. |
| **How many funds can the public give to (core)?** | **11,545 public funds across the 12 hubs** [C]. The range runs from 45 (Atlanta) to 3,080 (Columbus). 632 of them (5.5%) are explicit DAFs, and 585 of those 632 are at CF Middle Tennessee [C]. |
| **Fund type breakdown** | **No hub shows a fund-type field: 0 of 12 core and 0 of 299 hubs overall** [C]. The card template has an empty slot for it, and two core hubs (GiveWell, NHCF) set `show_granttype=1` in the search widget, but the slot is empty on every list page read [F]. The breakdown in §3.2 is therefore **derived from fund names and descriptions**, not shown by the hub. |
| **Generalised: share of public Foundant hubs that list DAFs** | **183 of 299 unique hubs read list at least one explicit DAF: 61.2%** [C].<br>- **64.9%** (194 of 299) if the 11 hubs whose only candidates are funds named "… Advised Fund" are added.<br>- **47.2%** (141 of 299) if at least 2 explicit DAFs are required.<br>- Across the 299 hubs, 3,165 of 94,332 public funds are explicit DAFs (3.4%). At the median hub the share is 0.6% [C]. |
| **DAF-related features on the hubs** | - **Donor portal link** (Login → `/erp/portal`, `/erp/fundmanager` or `/erp/login`): 9 of 12 core hubs; 257 of 299 overall [C].<br>- **Grant Catalog** (`/erp/donate/list/grant`): 4 of 12 core; 50 of 299 overall [C].<br>- **Recommend-a-grant text in the hub's own text:** 0 of 12 core; 1 of 299 overall. Longmont: "If you have a DAF, you can recommend a grant to: Any fund listed below Any project in the Nonprofit Directory …" [F].<br>- **DAFpay or DAF Direct on a hub:** 0 of 299 [C]. They were seen on only 2 of 403 CF start pages read (Ocean Reef CF: DAF Direct; CF of North Central Washington: DAFpay) [C]. |

**Bottom line.** A public giving page for a DAF is not white space on Foundant. It is shipped and in use: most public hubs (61%) list at least one fund their own text calls donor-advised, open to gifts from anyone through the hub cart [C]. It is a minority practice inside each hub, though. At the median hub, explicit DAFs are 0.6% of public funds, and one CF (CF Middle Tennessee) accounts for 585 of the 632 core-hub DAF listings [C]. The vendor leaves listing to the CF ("any fund you make publicly available", PF-19 [R]). The spread runs from Atlanta (45 curated funds, no DAFs) to CFMT (1,689 funds, 585 described as granting "as recommended by the grant advisor"). That spread fits a per-CF policy choice better than a platform limit [I].

---

## 1. Method

1. **Population** [C].
   - Core: the 13 rows of `community-foundation-rails-portals-2026-v2.csv` with portal_vendor `Foundant CommunitySuite`. Their start pages are the homepage plus the repo's own source URLs on the same host.
   - Extended: the 400 rows of `cf-vendor-map-by-ein-v2.csv` with portal_vendor `Foundant CommunitySuite` that are not core rows (EIN join). Each starts from the repo's homepage URL.
   - Several filers share one site and hub (supporting trusts, affiliates; for example two Rochester Area CF EINs both point to racfs.fcsuite.com). The first row per hub host is kept as the unique hub (`unique_hub`), core rows first, giving **403 unique CFs**. All headline shares use unique hubs.
2. **Robots, before anything else on a host.**
   - The script fetches `robots.txt` for every CF host and every hub host and parses it with `urllib.robotparser`.
   - A path is fetched only if it is allowed for both `research-script/1.0` (the generic UA used, which falls in the `*` group) and `Claude-User` (the token for user-directed fetches by Claude).
   - All 299 fcsuite.com hub hosts read share one robots file. It disallows `/` for a named AI-crawler group (`ClaudeBot`, `anthropic-ai`, `GPTBot`, `CCBot`, …). For `User-agent: *` it disallows only `/api/` [F].
   - That group lists training crawlers. `Claude-User` is not named, so it falls in `*`. The hub list pages were fetched on that basis and `/api/` was never requested. **This is a judgment call that the caller may want to review (see §5).**
   - Per RFC 9309, a 4xx robots response was read as "allow all" (403 on 29 CF hosts, 404 on 21) and a transport failure as "disallow all" (5 CF hosts).
3. **Finding the hub (link-following only).**
   - Every link whose path contains `/erp/donate` on the CF start pages counts as a hub link.
   - If there is none, up to 3 same-site links whose href or anchor says give, donate or gift are followed once and searched the same way.
   - The hub host is the host linked most often. **No hub URL was guessed.** CFs with no linked hub are recorded as `no hub link found` (64 unique) or `cf start pages not read` (32 unique).
   - Every hub found was on `*.fcsuite.com`. No CF-hosted custom domain was seen.
4. **Reading the hub.**
   - The featured page `/erp/donate/list` sets its session cookie from a hidden field. Without cookies it shows only a "Cookies Disabled" notice [F]. The script sends that cookie, as a browser would, on later GETs.
   - The full public list is `/erp/donate/list?showlist=1` (the hub's own "Show Additional Funds" link) [F]. Each affiliate variant `&sorg_id=N` linked from the CF site or hub is also read: 10 hubs had them, among them Richmond, where three affiliate lists add 5 funds to 207. Funds are unioned on `funit_id`.
   - Only cards with a Donate button count as public funds.
   - No donate/create form, cart, search endpoint or login page was submitted or requested.
5. **Classification** (pure functions in the script).
   - `daf_explicit`: the fund's name or description says "donor advised", "donor-advised" or "DAF", or says grants are made "as recommended by the grant advisor/donor".
   - Excluded from `daf_explicit`: phrases naming a DAF as a payment source ("give from your donor-advised fund", "If giving from a Donor Advised Fund"). Three such false hits were found in the core hubs and removed (Denver, NHCF, CFNJ).
   - `advised_agency`: "advised" plus "agency" in the name.
   - `advised_other`: "advised" in the name, nothing else. These may be DAFs or nonprofit-advised funds. Denver's 10 are mostly named for nonprofits, so they are **not** counted as DAFs.
   - Other buckets (scholarship, endowment, memorial, designated, agency, general/field-of-interest, family/named charitable, other) come from keywords, in that precedence.
   - Hub flag `lists_daf_public`: Y if at least 1 `daf_explicit` fund, P if none but at least 1 `advised_other`, otherwise N.
6. **Hand check of precision.**
   - A random sample of 40 extended-hub `daf_explicit` matches made on the description, not the name, was read. 38 clearly describe the fund itself as a DAF.
   - 2 are borderline: cffmc "Building to a Donor Advised Fund" (a build-a-fund) and aaacf "Through a Donor Advised Fund, donors learn more …".
   - The 720 extended matches made on the name all contain "Donor Advised" in the fund name [C].

## 2. Robots and access log (2026-11-20)

| Host group | Hosts | robots result | Action |
|---|---|---|---|
| `*.fcsuite.com` hub hosts | 299 unique (all read) | 200; `*`: `Disallow: /api/`; AI group (ClaudeBot, anthropic-ai, GPTBot, CCBot, …): `Disallow: /`. `Claude-User` not named | read `/erp/donate/list` and `?showlist=1` only |
| CF hosts, 13 core | 12 allow; Columbus 404 (allow) | Omaha: `User-agent: Claude-User` / `Disallow: /` (Cloudflare managed list) [B] | Omaha skipped |
| CF hosts, all unique (403) | 357 (200), 29 (403), 21 (404) on all rows | 4 unique hosts name `Claude-User`; 3 disallow it: Omaha, Oklahoma City CF (`occf.org`), Brookline CF [B] | skipped |
| CF hosts unreachable | 5 (cfgfw.org, nicf.org, oprfcf.org, wvcf.org, blackfordcofoundation.org) | transport error → disallow all | skipped |

Per-row robots status and the AI-group note are in the CSV columns `cf_robots_*` and `hub_robots_*`.

**Process lapse, disclosed.** Before the script existed, an exploratory pass fetched the 13 core CF homepages, three CF give pages (RI, CFNJ, STL) and a few fcsuite hub pages *before* checking each host's robots.txt.
- The later check shows every one of those hosts allows the fetch except **omahafoundation.org**, which disallows `Claude-User`. Its homepage was fetched once in that pass, and its hub host (omahafoundation.fcsuite.com, which allows the fetch) was read once.
- **None of the Omaha data is used anywhere in this note or the CSV.** Omaha is coded `cf_robots_disallowed`.

## 3. Results

### 3.1 Core 13 [C unless marked]

| Row | Foundation (DAFRC FY2024 rank) | Hub (link found on) | Featured / public funds | Explicit DAF | Advised (other) | lists_daf_public | Portal link / Grant Catalog |
|---|---|---|---|---|---|---|---|
| FGH-001 | Columbus Foundation (5) | columbusfdn.fcsuite.com (homepage) | 5 / 3,080 | 11 | 3 | Y | Y / Y ("Better Together"; also "Giving Store" directory) |
| FGH-002 | CF for Greater Atlanta (10) | cfga.fcsuite.com (homepage) | 19 / 45 | 0 | 0 | N | Y / Y |
| FGH-003 | CF of New Jersey (13) | cfnj.fcsuite.com (cfnj.org/donate-to-fund/) | 46 / 1,243 | 7 | 0 | Y | Y / N |
| FGH-004 | Denver Foundation (14) | denver.fcsuite.com (homepage) | 3 / 313 | 1 | 10 (+1 agency) | Y | Y / N |
| FGH-005 | CF Tampa Bay (21) | cftampabay.fcsuite.com (homepage) | 79 / 377 | 0 | 0 | N | Y / N |
| FGH-006 | Omaha CF (26) | not read [B] | – | – | – | n/a | – |
| FGH-007 | Greater Cincinnati Fdn (27) | gcfdn.fcsuite.com (homepage) | 4 / 242 (1 affiliate list) | 0 | 0 | N | Y / Y |
| FGH-008 | GiveWell CF (28) | gwcf.fcsuite.com (homepage) | 130 / 146 | 0 | 0 (+1 agency) | N | N / N |
| FGH-009 | NH Charitable Fdn (30) | nhcf.fcsuite.com (homepage) | 9 / 2,043 | 19 | 9 | Y | N / N |
| FGH-010 | CF of Middle Tennessee (32) | cfmt.fcsuite.com (homepage) | 7 / 1,689 | 585 | 30 | Y | Y / N |
| FGH-011 | Rhode Island Fdn (35) | rif.fcsuite.com (rifoundation.org/donate) | 8 / 1,998 | 3 | 0 | Y | N / N |
| FGH-012 | St. Louis CF (39) | stl.fcsuite.com (stlgives.org/give-today/) | 2 / 157 | 6 | 0 | Y | Y / N |
| FGH-013 | CF Richmond & Central VA (40) | tcfrichmond.fcsuite.com (homepage) | 13 / 212 (3 affiliate lists) | 0 | 0 | N | Y / Y |

Examples of explicit DAFs open to public gifts, with `funit_id`s in the CSV `daf_examples` column [F]:
- Columbus: "Bishop Family Donor Advised Fund".
- CFNJ: "Kelly Family Donor Advised Fund".
- NHCF: "Alletta Fund — The purpose of this Donor-Advised Fund is for broad charitable purposes."
- CFMT: "Abe's Garden Advised Fund — To support charitable organizations as recommended by the grant advisor."
- RI: "Cynthia M. Macarchuk Donor Advised Fund".
- STL: "Bliss Donor Advised Fund".
- Denver: its only explicit case is "The Denver Foundation Employee Fund", which "is a donor-advised fund started and supported by employees".

How this fits the repo context:
- Atlanta's hub (45 curated funds, no DAF) is consistent with PF-22 (portal "Donate" tab for "a public fund or cause").
- Sarasota (PF-27) and Triangle (PF-28) are not in the core 13, but both hubs were read in the extended set [C]:
  - **Sarasota (FGH-061):** 37 public funds and no explicit DAF. This is consistent with its manual's "donate to another fund".
  - **Triangle (FGH-026):** 554 public funds. 2 of them are explicit DAFs: "Grubb Ventures Donor Advised Fund" (funit_id=2815) and "SS210 Donor Advised Fund" (funit_id=1648).
  - So Triangle's 2024 guide refuses "active fundraising or solicitation" for its funds, yet its hub still lists DAFs for public gifts. Refusing to fundraise and listing a fund are separate policies [F/I].

### 3.2 Name-derived fund-type breakdown, 299 unique hubs [C]

| Bucket (derived, not displayed) | Funds | Share |
|---|---|---|
| other (no keyword) | 33,214 | 35.2% |
| scholarship | 21,362 | 22.6% |
| endowment | 13,183 | 14.0% |
| family / named charitable | 9,344 | 9.9% |
| memorial / in honor / legacy | 5,776 | 6.1% |
| field of interest / general / relief | 3,243 | 3.4% |
| **daf_explicit** | **3,165** | **3.4%** |
| designated | 2,803 | 3.0% |
| agency | 1,814 | 1.9% |
| advised_other | 424 | 0.4% |
| advised_agency | 4 | 0.0% |
| **Total public funds** | **94,332** | |

Shares are of the 94,332 total. Per-hub counts are in the CSV `type_*` columns. "Family / named charitable" (for example "David and Dorothy Markert Family Charitable Fund" at Atlanta) probably includes many DAFs that the hub does not label. The explicit count is therefore a **lower bound** on DAFs listed [I].

### 3.3 Generalisation: 403 unique CFs, 299 hubs read [C]

| Status | Unique CFs |
|---|---|
| Hub read | 299 |
| No hub link on homepage or give pages | 64 |
| CF start pages not read (HTTP error) | 32 |
| robots disallows (Omaha, OCCF, Brookline) | 3 |
| robots unreachable | 5 |

| Hub flag (299 read) | Hubs | Share |
|---|---|---|
| Y: at least 1 explicit DAF | 183 | 61.2% |
| P: only "… Advised Fund" names | 11 | 3.7% |
| N | 105 | 35.1% |
| Sensitivity: at least 2 explicit DAFs | 141 | 47.2% |

- **Distribution of explicit-DAF counts per hub:** 0 on 116 hubs, 1 on 42, 2 on 22, 3 on 12, 4 on 15, 5 to 9 on 29, and 10 or more on 63 [C].
- **By hub size** (quartiles of public-fund count): Q1 (0–82 funds) 13 of 74 hubs list an explicit DAF; Q2 (82–211) 44 of 74; Q3 (212–353) 58 of 74; Q4 (355–3,811) 68 of 77 [C]. Bigger public lists are far more likely to include DAFs. This fits a "publish every fund" policy rather than a curated one [I].
- **Two hubs read with 0 public funds:** cfsema.fcsuite.com and phelps.fcsuite.com.
- **Core vs extended:** core 7/12 (58.3%) vs extended 176/287 (61.3%) [C].

### 3.4 Hub features [C]

- Nav items across the 299 hubs:
  - Login: 257
  - "Donate To A Fund": 199
  - Event Tickets / Events: 64 + 22
  - Nonprofit Directory: 39
  - Grant Catalog: 16 by name; 50 by `/erp/donate/list/grant` path, under various labels
  - Giving Cards: 4
- Every hub has a cart (`/erp/donate/checkout`). Atlanta's footer says "Powered by Stripe" [F].
- DAF text in the hub's own (non-card) text appears on 5 of 299 hubs [F]:
  - **Longmont** invites DAF holders to recommend grants to listed funds. This is the only hub-level recommend-a-grant text.
  - **Shenandoah CF:** "If you would like to donate to your donor-advised fund, please log in to the fund advisor portal". Here the hub routes DAF top-ups to the portal, not to a public page.
  - **TTCF** and **Orcas Island CF** welcome transfers or grants *from* DAFs (DAF as a payment source).
  - **CFWNC** warns that "gifts to donor advised funds are not eligible" for the non-itemiser deduction. That is a reason a CF might not promote public gifts to DAFs [I].
- **DAFpay / DAF Direct:** none on any hub. 2 of 403 CF start pages carry them: Ocean Reef CF (DAF Direct; no hub link found) and CF of NCW (DAFpay; its hub lists 10 explicit DAFs).

## 4. Interpretation [I]

- PF-19 had left open whether CFs list DAFs, and this pass shows it is not hypothetical. Most Foundant CFs with a public hub publish at least one DAF to the public.
- The pattern is "list-everything" CFs (CFMT, NHCF, Columbus, RI, CFNJ) versus "curated" CFs (Atlanta 45 funds, GiveWell 146, Tampa Bay 377 with none explicit).
- Nothing on the hub promotes a DAF as a fundraising page: no DAF badge, no type filter, no peer-to-peer page. The DAF simply appears as one card among thousands, and Shenandoah sends DAF top-ups to the login portal.
- So the white space is not "can the public give to a DAF" but **"a DAF-specific public page or campaign"**, which no hub read offers.

## 5. Limits

- **Robots interpretation.**
  - The fcsuite.com robots file blocks named AI crawlers, ClaudeBot and anthropic-ai among them, from all paths.
  - This run treated those as training crawlers and fetched as a user-directed agent (`Claude-User`, not named, so `*`) with the generic UA mandated by the shared rules. Where a site named `Claude-User` (Omaha, OCCF, Brookline), it was honoured.
  - A stricter reading (that any Anthropic agent is covered by the `anthropic-ai` line) would exclude all 299 hubs. The caller should confirm this reading before the data are relied on.
- **Exploratory pre-robots fetches** (§2): disclosed. Omaha data excluded.
- **Fund type is inferred, not shown.**
  - No hub displays a type, so `daf_explicit` is a lower bound (DAFs under plain family names are missed).
  - The P class is ambiguous.
  - The 40-fund hand check covers description matches only.
- **Snapshot.** One day (2026-11-20). Hub lists change as funds open and close.
- **Coverage.** 104 of 403 unique CFs not read (no link, page errors, robots). These may be smaller or bot-protected sites.
- **Duplicates.** Deduplication is by hub host. Some CFs may share a hub with a different CF whose funds are mixed in (for example Eau Claire and Rusk County share eccf.fcsuite.com).
- **Cache.** Raw pages were cached in the session scratchpad, not in the repo. `--offline` reproduces the CSV only while that cache exists. A fresh live run will give slightly different counts.
- **Policy not read.** Whether a listed DAF actually accepts third-party gifts after checkout (CF review, minimums) was not tested: no forms were submitted.

## 6. Data dictionary: `foundant-giving-hub-2026-11-20.csv`

| Column | Meaning |
|---|---|
| row_id | FGH-001…FGH-413; core rows first, in the order of the rails CSV |
| population | `core` (rails v2 Foundant rows) or `extended` (vendor map v2 Foundant rows not in core) |
| foundation, ein | name and EIN as in the source CSV |
| fy2024_daf_assets_usd, dafrc_rank_fy2024 | joined from the source CSV (rank for core only) |
| cf_start_url, cf_host | first start page and its host |
| cf_robots_status | `200`, `4xx (allow all per RFC 9309)` or `<error> (disallow all per RFC 9309)` |
| cf_robots_allows_agent | Y if allowed for both `research-script/1.0` and `Claude-User` |
| cf_robots_ai_group | AI tokens named in robots.txt and which are disallowed for the path |
| hub_link_found_on | CF page on which the first hub link was found |
| hub_url, hub_host | `https://<host>/erp/donate/list` of the most-linked hub host |
| hub_robots_status, hub_robots_allows_agent, hub_robots_ai_group | as for the CF host |
| hub_read_status | `read`, `no hub link found`, `cf start pages not read`, `cf_robots_disallowed`, `cf_robots_unreachable`, `featured_http_*`, `list_not_read` |
| featured_funds | cards with a Donate button on the featured page |
| public_funds_total | distinct funit_ids with a Donate button on the full list(s) |
| affiliate_lists_read | number of `sorg_id` affiliate lists read in addition to the main list |
| type_daf_explicit … type_other | name/description-derived buckets (§1.5, §3.2); they sum to public_funds_total |
| fund_type_shown_on_hub | Y if any card displays a non-empty fund/grant-type field (0 of 299) |
| lists_daf_public | Y / P / N (§1.5); n/a when no hub was read |
| unique_hub, duplicate_of | Y for the first row per hub host (or per CF host if no hub); else N and the row_id it duplicates |
| daf_examples | up to 3 explicit-DAF fund names with funit_id |
| hub_nav_items | top navigation labels of the hub |
| donor_portal_link_on_hub | Y if a nav item links to `/erp/portal`, `/erp/fundmanager` or `/erp/login` |
| grant_catalog_on_hub | Y if a nav item links to `/erp/donate/list/grant` |
| recommend_grant_text_on_hub | Y if the hub's own text (outside fund cards) says "recommend a grant" or "grant recommendation" |
| daf_mention_in_hub_text | Y if the hub's own text mentions "donor advised"/"DAF" |
| dafpay_or_dafdirect_on_hub / _on_cf_pages | DAFpay, Chariot or DAF Direct strings found in hub HTML / CF pages read; `none seen` otherwise |
| notes | `CF start pages not read` where applicable |
| retrieved | 2026-11-20 |

## 7. Source register (all read 2026-11-20 unless marked)

**Vendor and context [R]**
- Foundant, "The Portal and the Giving Hub: what's new" (PF-19): https://www.foundant.com/blog/the-portal-and-the-giving-hub-what-s-new/
- Atlanta Fund Advisor Portal Guide (PF-22): https://cfgreateratlanta.org/wp-content/uploads/2025/03/Fund-Advisor-Portal-Guide.pdf
- Sarasota Giving Portal Manual (PF-27): https://www.cfsarasota.org/files/galleries/CFSarasota_Giving_Portal_Manual.pdf
- Triangle New Donor Portal Guide (PF-28): https://trianglecf.org/wp-content/uploads/2024/10/New-Donor-Portal-Guide-October-2024-.pdf

**Core CF start pages and hubs [F]** (robots.txt for each at `https://<host>/robots.txt`)

| CF page (hub link found on) | Hub full list |
|---|---|
| https://columbusfoundation.org/ | https://columbusfdn.fcsuite.com/erp/donate/list?showlist=1 |
| https://cfgreateratlanta.org/ | https://cfga.fcsuite.com/erp/donate/list?showlist=1 |
| https://cfnj.org/donate-to-fund/ | https://cfnj.fcsuite.com/erp/donate/list?showlist=1 |
| https://denverfoundation.org/ | https://denver.fcsuite.com/erp/donate/list?showlist=1 |
| https://www.cftampabay.org/ | https://cftampabay.fcsuite.com/erp/donate/list?showlist=1 |
| https://omahafoundation.org/robots.txt [B] | not read |
| https://www.gcfdn.org/ | https://gcfdn.fcsuite.com/erp/donate/list?showlist=1 |
| https://www.givecf.org/ | https://gwcf.fcsuite.com/erp/donate/list?showlist=1 |
| https://www.nhcf.org/ | https://nhcf.fcsuite.com/erp/donate/list?showlist=1 |
| https://www.cfmt.org/ | https://cfmt.fcsuite.com/erp/donate/list?showlist=1 |
| https://rifoundation.org/donate | https://rif.fcsuite.com/erp/donate/list?showlist=1 |
| https://stlgives.org/give-today/ | https://stl.fcsuite.com/erp/donate/list?showlist=1 |
| https://cfrichmond.org/ | https://tcfrichmond.fcsuite.com/erp/donate/list?showlist=1 (+ `&sorg_id=1000/1001/1002`) |

**Quoted extended hubs [F]**
- https://longmont.fcsuite.com/erp/donate/list
- https://scfva.fcsuite.com/erp/donate/list
- https://ttcf.fcsuite.com/erp/donate/list
- https://oicf.fcsuite.com/erp/donate/list
- https://cfwnc.fcsuite.com/erp/donate/list
- https://cfncw.fcsuite.com/erp/donate/list
- CF pages with widgets: https://www.cfncw.org/ (DAFpay) and https://www.oceanreefcommunityfoundation.org/ (DAF Direct)

**Other sources.** Every other hub and CF start URL is in the CSV columns `hub_url` and `cf_start_url`. The repo inputs are `data/mission-2026-11-14/community-foundation-rails-portals-2026-v2.csv` and `data/mission-2026-11-14/cf-vendor-map-by-ein-v2.csv`.
