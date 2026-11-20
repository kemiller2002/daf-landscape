# P-B43N26-01: Which charity data provider powers the in-portal search at top-20 sponsors?

**Task:** P-B43N26-01 (TASKID b43n26-01). **Date:** 2026-11-20.
**Context:**
- [direction-charity-ratings-integrations.md](direction-charity-ratings-integrations.md) §3, the matrix this pass extends;
- [`charity-data-provider-integrations-2026.csv`](../../data/mission-2026-11-14/charity-data-provider-integrations-2026.csv);
- [b43n26-03-charity-data-terms-ai.md](b43n26-03-charity-data-terms-ai.md), for the licence terms.

**Outputs:**
- [`data/mission-2026-11-14/in-portal-data-provider-2026-11-20.csv`](../../data/mission-2026-11-14/in-portal-data-provider-2026-11-20.csv): 20 rows (IPD-014 withdrawn on robots grounds).
- [`scripts/mission_b43n26_01_in_portal_provider.py`](../../scripts/mission_b43n26_01_in_portal_provider.py): schema check and tallies.
- [`data/mission-2026-11-14/queue-proposals-b43n26-01.csv`](../../data/mission-2026-11-14/queue-proposals-b43n26-01.csv): 5 proposals.

Labels: **[F]** first-party or vendor text fetched in this run. **[C]** repo record, not re-fetched. **[S]** search-engine snippet only. **[I]** our inference.

---

## 0. Summary

**In-portal provider found for 2 of the 9 named sponsors.**

| Sponsor | In-portal provider | Mode | Strength |
|---|---|---|---|
| NPT | Candid (GuideStar) | **embedded** | Sponsor-specific [F], but from a 2021 launch article (still live, modified 2026-02-09) |
| AEF | Ren's own IRS-based listing | **eligibility-only** | Vendor-level [F] + [I]. AEF's platform is "powered by Ren"; a Ren post says Ren built its own listing instead of using GuideStar. Giving Compass impact data is only *announced* for Ren (2026-05-13) |
| DAFgiving360 | not found | — | Host robots 403, so not read. Outbound links to Candid and CN (repo snippets) |
| Goldman Sachs PF | not found | — | — |
| Morgan Stanley GIFT | not found | — | "Charity Vetting Automated with advanced tech", no vendor named |
| NCF | not found | — | Own list: "Search from thousands of charities – already researched and approved" |
| JCF | not found | — | Outbound links only (GuideStar, CN, BBB WGA and others) |
| Raymond James Charitable | not found | — | Hosts' robots.txt timed out |
| Chicago Community Trust | not found | — | Portal "Powered by The GiftingNetwork"; free-text "Organization Name" field |
| **CF portals generally** | **Candid (GuideStar / Charity Check)** | **embedded** | Vendor-level: Foundant CommunitySuite and Give Interactive [F]. Three of three CF portal guides read (Tampa Bay, Central New York, Santa Cruz County) show an in-portal Candid or GuideStar search |

Script output (`python3 scripts/mission_b43n26_01_in_portal_provider.py .`):
- 21 rows, 0 errors.
- Rows by mode: embedded 7, not_found 7, linked 3, eligibility_only 2, announced 1, vendor_claim 1.
- Rows by evidence scope: sponsor-specific 14, vendor-level 7.
- Named sponsors by in-portal mode: embedded 1, eligibility_only 1, not_found 7.

**Readings [I].**
1. **Where a provider is named, it is Candid.** Every in-portal search named, at NPT and on the CF vendors, is Candid/GuideStar, which fits the §3 reading that "Candid is the de facto search and profile layer". Charity Navigator appears only as an outbound link (NPT, JCF, DAFgiving360 [C]). We found no CN data inside a sponsor portal.
2. **Ren is the exception.** Ren states it replaced GuideStar with its own IRS-sourced listing. Its next data layer is Giving Compass, not Candid. This matters for AEF and other Ren-run programmes.
3. **Wealth-firm sponsors say nothing.** Goldman Sachs, Morgan Stanley and Raymond James publish no public statement of their search data. "Not found" here means not disclosed in robots-readable sources. It does not mean no provider.
4. **Candid's generic claim is not evidence.** Candid tells nonprofits their profiles reach "All major U.S.-based donor-advised funds including Fidelity Charitable". This names no other sponsor, so it is not counted for any sponsor (IPD-021).

---

## 1. Method

1. **Scope.**
   - The nine named top-20 sponsors, plus "CF portals generally".
   - CF portals are covered through the portal vendors' own pages (Foundant, Give Interactive, akoyaGO) and through public CF portal guides.
2. **Discovery.**
   - About 20 web-search queries were run. They combined sponsor names with "GuideStar", "Candid", "Charity Navigator", "portal", "charity search" and the vendor names.
   - Search results were used only to find URLs. Every claim in the CSV comes from a page fetched in this run, except the DAFgiving360 linked rows, which are carried from the repo [C].
3. **Robots and fetching.**
   - A scratchpad fetcher (user agent `research-script/1.0`) read each host's robots.txt with `urllib.robotparser` before every request:
     - 200: parsed and applied;
     - 404: allowed;
     - 401, 403, 429, 5xx, timeout or network error: treated as disallowed, and the page was not fetched.
   - Each request was logged (§1.1).
   - No logins, forms or user-agent changes. login.jcfny.org was read only as its public landing HTML (title and meta). No credentials were entered.
4. **Coding.**
   - Each row gets one `integration_mode`:
     - **embedded:** the provider's data drives search or profiles in the donor's grant flow;
     - **linked:** an outbound reference only;
     - **eligibility_only:** a status check or IRS-only listing with no ratings or profiles;
     - **announced:** a future-tense partnership;
     - **vendor_claim:** a provider's generic claim;
     - **not_found:** nothing public names the provider.
   - `evidence_scope` separates sponsor-specific statements from vendor-level ones, where the vendor's capability is assumed to apply to its client [I].
5. **Quote check.** All 18 quotes in the CSV were matched verbatim against the fetched text, after whitespace and apostrophe normalisation (18 of 18).
6. **Computation.** The repo script checks the schema and vocabulary and prints the tallies in §0. The in-portal mode per sponsor counts only embedded, eligibility_only and announced rows. It ignores linked and vendor_claim rows, because they say nothing about the in-portal search.

### 1.1 Robots log (per host, 2026-11-20 UTC)

64 requests to 43 hosts; 44 returned 200.

| Host | robots.txt | Decision | Requests | 200 | Other statuses |
|---|---|---|---|---|---|
| www.nptrust.org | 200 | allowed | 3 | 3 | |
| www.dafgiving360.org | **403** | disallowed (skipped per task) | 1 | 0 | |
| www.schwab.com | 200 | allowed | 1 | 1 | |
| wealthmanagement.com | 200 | allowed | 1 | 0 | 404 |
| pwm.gs.com | 200 | allowed | 1 | 1 | |
| ayco.com | **timeout** | disallowed | 1 | 0 | |
| www.morganstanley.com | 200 | allowed | 1 | 1 | |
| prod-mssip.morganstanley.com | 200 | allowed | 1 | 0 | 503 |
| advisor.morganstanley.com | **timeout** | disallowed | 3 | 0 | |
| www.aefonline.org | 200 | allowed | 3 | 2 | 404 |
| engage.aefonline.org | 200 | allowed | 1 | 1 | |
| donorwelcome.aefonline.org | 200 | allowed | 1 | 1 | |
| www.reninc.com | 200 | allowed | 2 | 1 | 404 |
| intercom.help | 200 | allowed | 1 | 0 | 404 |
| www.givingcompass.org | 200 | allowed | 1 | 1 | |
| givingcompass.org | 200 | allowed | 1 | 1 | |
| www.ncfgiving.com | 200 | allowed | 3 | 3 | |
| jcfny.org | 200 | allowed | 9 | 9 | |
| login.jcfny.org | 200 | allowed (landing HTML only) | 1 | 1 | |
| www.raymondjames.com | **timeout** | disallowed | 2 | 0 | |
| www.raymondjamescharitable.org | **timeout** | disallowed | 1 | 0 | |
| donorportal.cct.org | 200 | allowed | 2 | 1 | 404 |
| www.cct.org | 200 | allowed | 1 | 0 | 403 |
| www.foundant.com | 200 | allowed for `*`, but **disallows ClaudeBot / anthropic-ai / Claude-Web**: content withdrawn | 3 | 3 | |
| communityfoundations.foundant.com | 200 | allowed | 1 | 1 | |
| dev.foundant.com | 200 | allowed for `*`, but **disallows ClaudeBot / anthropic-ai / Claude-Web**: content withdrawn | 1 | 1 | |
| resources.foundant.com | 200 | **disallowed by rules** | 1 | 0 | |
| support.foundant.com | 200 | allowed | 1 | 0 | 403 |
| techimpact.org | 200 | allowed | 1 | 1 | |
| www.armanino.com | 200 | allowed | 1 | 1 | |
| www.envestnet.com | 200 | allowed | 1 | 1 | |
| www.cftampabay.org | 200 | allowed | 1 | 1 | |
| cnycf.org | 200 | allowed | 1 | 1 | |
| craft-cfscc-prod.s3.amazonaws.com | 404 (none) | allowed | 1 | 1 | |
| www.racf.org | 200 | allowed | 1 | 1 | |
| vermontcf.org | 200 | allowed | 1 | 1 | |
| www.nccommunityfoundation.org | 200 | allowed | 1 | 1 | |
| www.thecommunityfoundation.org | 200 | allowed | 1 | 1 | |
| candid.org | **403** | disallowed | 1 | 0 | |
| blog.candid.org | **403** | disallowed | 1 | 0 | |
| cms2.candid.org | **network error** | disallowed | 1 | 0 | |
| learning.candid.org | 200 | allowed | 1 | 1 | |
| www.guidestar.org | 200 | allowed | 1 | 1 | |

The fetcher and the raw log (`robots-fetch-log-b43n26-01.tsv`) are in the session scratchpad, not the repo.

---

## 2. Results table

See the CSV for the full quotes and URLs. Row IDs are given in brackets.

| Sponsor | Provider | Mode | Key quote | Source |
|---|---|---|---|---|
| NPT (IPD-001) | Candid (GuideStar) | embedded | "Partnering with GuideStar’s powerful search database, donors can search by a wide variety of criteria including topic and issue area, Tax ID code, geographic location, state or ZIP code." | [nptrust.org](https://www.nptrust.org/philanthropic-resources/philanthropist/how-npt-givingpoint-can-accelerate-your-online-giving/), 2021-07-29, mod. 2026-02-09 |
| NPT (IPD-002) | Candid, CN, BBB WGA | linked | "Independent, third-party databases, such as Candid’s Guidestar , Charity Navigator , or Better Business Bureau’s Wise Giving Alliance , are also helpful…" | [nptrust.org](https://www.nptrust.org/philanthropic-resources/philanthropist/awareness-for-donors-due-diligence-when-choosing-nonprofit-organizations-for-grant-recommendations/), 2024-05-01 |
| DAFgiving360 (IPD-003/004) | not found | not_found; CDP list linked | "we work with the Center for Disaster Philanthropy to quickly compile a list of vetted nonprofits" | [schwab.com](https://www.schwab.com/learn/story/giving-effectively-times-disaster); host dafgiving360.org 403 |
| Goldman Sachs PF (IPD-005) | not found | not_found | — | [pwm.gs.com](https://pwm.gs.com/nam/en-us/insights/wealth-planning/philanthropy/finding-and-funding-effective-nonprofit-organizations), 2025-03-06 |
| Morgan Stanley GIFT (IPD-006) | not found | not_found | "Charity Vetting Automated with advanced tech" | [MS GIFT How it Works PDF](https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-how-it-works.pdf), 2025-10-24 |
| AEF (IPD-007) | Ren own IRS-based listing | eligibility_only (vendor-level) | "Ren created this listing to get IRS updates faster than they were able to through Guidestar…" | [reninc.com](https://www.reninc.com/blog/ren-for-charities-streamlines-clients-giving/), 2022-09-12 |
| AEF (IPD-008) | portal = Ren | (vendor evidence) | "The AEF Technology Platform , powered by Ren…" | [engage.aefonline.org](https://engage.aefonline.org/?p=12588) |
| AEF (IPD-009) | Giving Compass | announced | "In the first phase, Giving Compass will incorporate impact data for up to 93,000 nonprofits within Ren’s network" | [givingcompass.org](https://www.givingcompass.org/giving-compass-and-ren-accelerate-nonprofit-impact-discovery-for-daf-advisors/), 2026-05-13 |
| NCF (IPD-010) | own vetted list | not_found | "Search from thousands of charities – already researched and approved – so you can give with confidence." | [ncfgiving.com/support](https://www.ncfgiving.com/support) |
| JCF (IPD-011) | GuideStar, CN, BBB, ProPublica, IRS | linked | "GuideStar : Searchable database of more than 850,000 not-for-profit organizations" | [jcfny.org](https://jcfny.org/philanthropic-resources/) |
| Raymond James (IPD-012) | not found | not_found | — | robots timed out |
| CCT (IPD-013) | not found | not_found | "Powered by The GiftingNetwork, Donor Portal is a full-service platform" | [CCT Donor Portal User Guide](https://donorportal.cct.org/ma/docs/cct/DonorPortalUserGuide.pdf), 2024-02-06 |
| Foundant (IPD-015; IPD-014 withdrawn) | Candid | embedded (vendor) | (IPD-014, a foundant.com quote, withdrawn: www.foundant.com and dev.foundant.com robots.txt disallow ClaudeBot, anthropic-ai and Claude-Web, which this repo treats as applying) | [Tech Impact 2022](https://techimpact.org/sites/default/files/2024-03/TECH%20IMPACT%20Integrated%20Software%20for%20Community%20Foundations.pdf) |
| CF Tampa Bay (IPD-016) | Candid (Charity Check) | embedded | "Choose Search Grantee to search Community Foundation Tampa Bay's database and Candid (GuideStar Charity Check)." | [cftampabay.org](https://www.cftampabay.org/portal-guide) |
| CNYCF (IPD-017) | Candid | embedded | "…from a list of nonprofits in the CNYCF database and in Candid, the world’s largest database of nonprofit organizations." | [cnycf.org](https://cnycf.org/introducing-mygiving), mod. 2026-04-08 |
| CF Santa Cruz (IPD-018) | Candid (GuideStar) | embedded | "Search for the organization you want to support in GuideStar, the world's largest database of nonprofit organizations." | [2025 portal guide](https://craft-cfscc-prod.s3.amazonaws.com/uploads/2025-CFSCC-Donor-Portal-Guide.pdf), 2025-04-01 |
| Give Interactive (IPD-019) | Candid (GuideStar profiles) | embedded (vendor) | "…create pages that pull in the nonprofits’ GuideStar profiles and information" | Tech Impact, July 2022 |
| akoyaGO (IPD-020) | Candid (Charity Check) | eligibility_only (vendor) | "The system also integrates with GuideStar charity check." | Tech Impact, July 2022 |
| Generic (IPD-021) | Candid | vendor_claim | "All major U.S.-based donor-advised funds including Fidelity Charitable" | [guidestar.org](https://www.guidestar.org/UpdateNonprofitProfile) |

---

## 3. Notes by sponsor

### 3.1 NPT
- **Corrects §3.** The direction memo coded NPT "ND" for Candid. NPT's own GivingPoint article names GuideStar as the search database (embedded).
- **Caveat on date.** The article was published in 2021 and modified in 2026. It is still on the live site, but no 2024–2026 source restates the integration (queue proposal P-B43N26-01-01).
- **Fallback.** Donors can add an NGO "by manually adding the grantee to their Charity List", so the search index is not the eligibility boundary.

### 3.2 DAFgiving360
- **Not read.** Per the task, dafgiving360.org was skipped because its robots.txt returns 403.
- **Third-party copy.** The one copy read, a Schwab Learn article, describes curated lists built with the Center for Disaster Philanthropy, not a data feed.
- **Repo rows.** Rows CDP-015, CDP-034 and CDP-039 [C/S] record outbound Candid, CN and CharityWatch links only.

### 3.3 Goldman Sachs PF, Morgan Stanley GIFT, Raymond James Charitable
- **Not found.**
- **Morgan Stanley.** MS GIFT markets automated vetting with no vendor named.
- **Blocked hosts.** These hosts' robots.txt did not answer within 30 s, so they were treated as disallowed: advisor.morganstanley.com (three PDFs, incl. a DAF primer), ayco.com, www.raymondjames.com and raymondjamescharitable.org.
- **Context only.** Morgan Stanley at Work's workplace programme runs on TIFIN Give (search snippet). That is not evidence for MS GIFT's own portal.

### 3.4 NCF and JCF
- **NCF.** Describes its own pre-screened list and a research team. No external provider is named.
- **JCF.** Staff verify "tax-exempt status and official mailing address" for each recommended organisation (Policy Guide, Aug 2024). Outside providers appear only in a resource list.

### 3.5 AEF (via Ren)
- **Platform.** AEF moved to a Ren-run platform. Its pilot page says donors "can search by name of charity or EIN", with a manual-add fallback.
- **Ren's listing.** Ren says it built its own listing "to get IRS updates faster than they were able to through Guidestar".
- **Coding.** We code AEF eligibility-only by vendor-level inference [I], because AEF does not name the source itself.
- **Giving Compass.** The partnership (2026-05-13) is "laying the groundwork" in the future tense, so it is coded *announced*, not embedded.

### 3.6 Chicago Community Trust
- **Portal.** The 2024 donor-portal guide names GiftingNetwork as the portal.
- **Grant form.** Its screenshot shows a free-text "Organization Name" field with no provider branding.
- **No GiftingNetwork evidence.** No GiftingNetwork vendor page naming a charity data provider was found.
- **Give Interactive not used.** The repo's candidate Give Interactive link for CCT rests on certificate-log evidence, which this run does not use. So the Give Interactive GuideStar feature (IPD-019) is **not** applied to CCT.

### 3.7 CF portals generally
- **Foundant.** CommunitySuite (700+ community foundation clients per its own page) markets Candid as a built-in integration for the donor portal.
- **Portal guides.** Three of three CF portal guides read show a "Search Grantee" step that covers the foundation's own list plus Candid or GuideStar (Tampa Bay, Central New York, Santa Cruz County). The first two are explicitly on Foundant (fcsuite).
- **Other vendors.** Give Interactive pulls GuideStar profiles into its charity-discovery pages (2022). akoyaGO integrates Charity Check (2022).
- **No provider stated.** Vermont CF replaced Blackbaud/NPact DonorCentral with a Salesforce-hosted portal in May 2025. The NC Community Foundation portal is "hosted by Foundant Technologies". Neither page names a data provider.

---

## 4. Licence implications (from b43n26-03)

- **Candid display is tied to the Licensee Site.** Under Candid's public API terms, display is limited to the licensee's site and its bound customers. Data mining "for use in artificial intelligence … large language models, machine learning" needs Candid's prior written consent, and all use must stop on termination (b43n26-03 §2.2).
  - For NPT, the portal is its own, so NPT is plausibly the licensee [I].
  - For CF portals, Candid search is a vendor-built integration (Foundant, Give Interactive). The licensee and its Order Form are probably the vendor's [I].
  - So a CF that adds an AI assistant over its portal search would need consent through, or from, its vendor (queue proposal P-B43N26-01-05).
- **Ren's IRS-based listing carries no third-party licence limits** (IRS baseline, b43n26-03 §2.7). That makes Ren clients the cleanest base for AI ranking.
- **Giving Compass terms were not assessed** in b43n26-03. If the Ren layer goes live, it needs its own terms read.
- **Charity Navigator** appears only as outbound links at these sponsors. Its "no use in any other calculation" rule is not engaged by any portal found here.

---

## 5. Limits

1. **No logins.** No portal was observed directly. Every "embedded" finding rests on sponsor or vendor descriptions, and some of them are older (NPT 2021; Tech Impact 2022; Ren 2022).
2. **Not found means not disclosed.** "Not found" (7 of 9 named sponsors) means not disclosed in robots-readable public sources. Three of the seven rest partly on hosts whose robots.txt timed out. DAFgiving360 was skipped by rule.
3. **Candid hosts blocked.** candid.org and blog.candid.org return 403 to robots, so Candid's own partner and DAF blog posts (which a search snippet says name Vanguard and Fidelity) could not be read. No sponsor in scope was found named on a readable Candid page.
4. **Vendor-level rows are inferences.** These rows (AEF via Ren; CF via Foundant or Give Interactive) assume the vendor's feature is switched on for the client. A CF can disable the integration.
5. **CF sample is small.** The CF examples (3) are a convenience sample of portal guides found by search. They show the pattern, not its prevalence (queue proposal P-B43N26-01-03).
6. **Stale figure.** JCF's "850,000" GuideStar figure is stale page copy. It is quoted to evidence the link, not as a coverage number.

---

## 6. Data dictionary: `in-portal-data-provider-2026-11-20.csv`

| Column | Meaning |
|---|---|
| row_id | IPD-001 … IPD-021 |
| sponsor | Sponsor, vendor or CF the row describes |
| sponsor_scope | `top20` (named in task), `cf_vendor` (CF portal software vendor), `cf_example` (an individual CF), `vendor_claim` |
| portal_vendor | Portal technology vendor, if stated (`not named` otherwise) |
| provider | Charity data provider named, or `not found` |
| integration_mode | `embedded`, `linked`, `eligibility_only`, `announced`, `vendor_claim`, `not_found` (§1 item 4) |
| evidence_scope | `sponsor_specific` (the sponsor's own statement) or `vendor_level` (the vendor's statement applied to a client [I]) |
| quote | Short verbatim quote from the fetched source (empty for not_found rows with no relevant text) |
| source_url | Primary URL (canonical where the fetch used a `?p=` form; see notes) |
| source_date | Publication or modified date as shown by the source; `live` where undated |
| evidence_label | F / C / S (see header) |
| host_robots | robots.txt result and decision for the source host |
| retrieved | Fetch date (UTC) |
| notes | Caveats, fallbacks and related URLs |

---

## 7. Source register (primary URLs)

**NPT**
- https://www.nptrust.org/philanthropic-resources/philanthropist/how-npt-givingpoint-can-accelerate-your-online-giving/
- https://www.nptrust.org/philanthropic-resources/philanthropist/awareness-for-donors-due-diligence-when-choosing-nonprofit-organizations-for-grant-recommendations/

**DAFgiving360 (Schwab)**
- https://www.schwab.com/learn/story/giving-effectively-times-disaster

**Goldman Sachs PF**
- https://pwm.gs.com/nam/en-us/insights/wealth-planning/philanthropy/finding-and-funding-effective-nonprofit-organizations

**Morgan Stanley GIFT**
- https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-how-it-works.pdf

**AEF and Ren**
- https://engage.aefonline.org/?p=12588
- https://www.aefonline.org/charities/
- https://www.reninc.com/blog/ren-for-charities-streamlines-clients-giving/
- https://www.givingcompass.org/giving-compass-and-ren-accelerate-nonprofit-impact-discovery-for-daf-advisors/

**NCF**
- https://www.ncfgiving.com/support

**JCF**
- https://jcfny.org/philanthropic-resources/
- https://jcfny.org/app/uploads/2024/08/Policy-Guide-Aug-2024_SP.pdf
- https://jcfny.org/charity-grants/

**Chicago Community Trust**
- https://donorportal.cct.org/ma/docs/cct/DonorPortalUserGuide.pdf

**CF portal vendors**
- (Two foundant.com sources withdrawn 2026-11-20 on robots.txt grounds.)
- Tech Impact report (Foundant, Give Interactive, akoyaGO): https://techimpact.org/sites/default/files/2024-03/TECH%20IMPACT%20Integrated%20Software%20for%20Community%20Foundations.pdf

**CF portal guides**
- https://www.cftampabay.org/portal-guide
- https://cnycf.org/introducing-mygiving
- https://craft-cfscc-prod.s3.amazonaws.com/uploads/2025-CFSCC-Donor-Portal-Guide.pdf
- https://vermontcf.org/giving/donors-and-fundholders/donorcentral-and-grant-rec-form
- https://www.nccommunityfoundation.org/for-fundholders/navigating-the-online-fund-portal/for-fundholders

**Candid**
- https://www.guidestar.org/UpdateNonprofitProfile
