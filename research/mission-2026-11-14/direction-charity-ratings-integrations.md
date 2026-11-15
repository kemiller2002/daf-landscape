# Direction P-NEW-RAT-01: charity ratings and data providers inside DAF platforms

**Date:** 2026-11-15. **Queue item:** P-NEW-RAT-01 (new direction from the owner).
**Status:** Desk research from public sources only. No outreach, logins, form submissions or keyed API calls. robots.txt was read on every host before fetching. Hosts whose robots.txt could not be read, or that disallow Claude agents, were not fetched; facts about them come from search-engine snippets and are labelled [S]. crt.sh was not used. Recency rule: current state is 2021–2026. Pre-2021 facts (the 2020 ImpactMatters acquisition) appear only as context and are flagged.

**Read first, with governing corrections respected:**
- [queue-batch30-legal-circulars.md](queue-batch30-legal-circulars.md) §3 (Candid Charity Check against Rev. Proc. 2018-32 §8.01; the two Candid licences differ on retention). Its wave-15 corrections touch only the California sections.
- [direction-donor-feature-census.md](direction-donor-feature-census.md) (`charity_search` and `charity_vetting` cells). Its wave-27 correction (Android) does not touch this topic.
- [direction-recipient-compliance-screen.md](direction-recipient-compliance-screen.md) (IRS Pub 78/BMF/revocation screen of top-50 Schedule I lines). Its wave-26 corrections are applied where its figures are cited: "LLC-named recipients … $1.68bn (75 lines), of which the four CZ Biohub/Institute LLCs are $1.66bn".

**Outputs:**
- `data/mission-2026-11-14/charity-data-provider-integrations-2026.csv` (one row per provider fact or integration)
- `data/mission-2026-11-14/relationship-graph-edges-additions-25.csv` (edges EY001–EY020)
- `data/mission-2026-11-14/queue-proposals-batch43-n26.csv` (P-B43N26-01 to -03)

**Evidence labels.**
- **[F]** first-hand fetch of the cited page.
- **[S]** search-engine snippet only. The host was blocked by robots.txt, its robots.txt was unreadable, or the fetch returned 403/404/bot challenge.
- **[C]** carried from a repo file, with the file named.
- **[I]** inference by this agent.

---

## 0. Answers in one table

| Question | Answer | Confidence |
|---|---|---|
| **Does any DAF sponsor embed Charity Navigator (CN) ratings in its grant flow?** | **No public evidence found for any top-20 sponsor.**<br>- **Fidelity Charitable** lists CN and GuideStar on its ["Research charities" guidance page](https://www.fidelitycharitable.org/guidance/research-charities.html) "for reference purposes only" and points to the CN Advisory System on its [fraud page](https://www.fidelitycharitable.org/guidance/research-charities/avoiding-fraudulent-charities.html) [F]. Neither page describes a Giving Account integration. The only embedded third-party element is a **Giving Compass news widget** ("The Giving Compass Widget is provided by an independent third party") [F].<br>- **DAFgiving360** lists Candid and CN as research resources on its explore-charities page [S; host robots 403].<br>- The flow runs the other way: CN's own **Giving Basket accepts DAF grants through Chariot's DAFpay** (2.9% fee) ([Give Lively](https://www.givelively.org/resources/daf-donations-on-giving-basket)) [F]. | Medium. Logged-in portals were not checked |
| **Who powers sponsor charity search?** | **Candid (GuideStar), where anyone is named.**<br>- **Bank of America CGF:** donors "search the GuideStar database" (2025-09 guide) [C: donor-feature-census DFC-188].<br>- **Vanguard Charitable:** a Candid blog by a Vanguard Charitable grants manager says most major DAF platforms "pull data directly from Candid" for donor search. Vanguard's NAVi charity locator is among Candid's 200+ partner sites. Platinum-Seal organisations reportedly received twice the DAF grant dollars on Vanguard's site [S; candid.org robots 403].<br>- **Groundswell:** "Candid GuideStar integration" [C: E155].<br>- **Daffy:** says its database holds "every US-based not-for-profit organization in good standing with the IRS" (IRS-sourced; no vendor named) [S].<br>- **Every.org:** runs its own free Charity API covering "over 1 million 501(c)(3) organizations" ([docs](https://docs.every.org/docs/intro)) [F]. | Medium for Candid's dominance; low for any named sponsor beyond BofA |
| **What do donors see inside DAF platforms?** | **Mostly eligibility and profile data, not ratings.**<br>- Sponsor portals show IRS-derived eligibility (501(c)(3), public-charity status) and Candid profile content (mission, programs, financials, seal level) where Candid powers search.<br>- Star ratings (CN), letter grades (CharityWatch), BBB accreditation and GiveWell recommendations appear only as **outbound links or guidance**, not as in-flow badges, at every sponsor whose public pages were read. | Medium |
| **Licensing and price** | - **CN API:** GraphQL. Fixed-quota tiers "Startups, Small, Midsize, Enterprise" plus usage-based "Academics/Personal Use". 1,000 requests/minute per key. Alerts feed only on Midsize/Enterprise. 30-day free trial. Tiers keyed to "how many nonprofits you facilitate transactions to, and your total transaction volume". Annual usage reporting is required. Licence is "non-exclusive, non-transferable, non-sublicensable"; caching is permitted, redistribution and resale are not; linkback attribution is mandatory ([developer portal](https://developer.charitynavigator.org/plans); [terms, "Last updated October 2026"](https://www.charitynavigator.org/products-and-services/api/)) [F]. Dollar prices are rendered by script and were not captured.<br>- **Candid:** "starting at" **$2,750** Charity Check, **$4,800** Essentials and **$9,900** Premier; billing period unstated ([explore-APIs](https://candid.org/explore-apis/)) [S]. API licence requires ceasing "all use of the Candid Data" on termination [C: batch29 §4].<br>- **Every.org:** free API; no programmatic donations [F].<br>- **Pledge:** "no charge to use our API"; 5% fee on Donate-API donations [F].<br>- **Goodstack:** pricing not published [F].<br>- **IRS:** free monthly bulk files [F]. | High for CN/Every.org/Pledge structure; low for Candid figures |
| **Coverage** | - **CN:** "more than 245,000 charities rated" ([about](https://www.charitynavigator.org/about-us/)) out of about 1.7 million profiles ([help, 2026-04-09](https://intercom.help/charity-navigator/en/articles/8610643-donating-through-the-giving-basket)) [F]. That is **about 17% of the 1,437,291 Pub 78 records** [I; C: recipient screen].<br>- **Candid:** "over 1.8 million" organisations per Fidelity's page [F]; 1.9 million per Candid's January 2026 release [S].<br>- **BBB WGA:** about 1,500 national-charity reports (2024 annual report) [S].<br>- **CharityWatch:** no 2021+ count found [S].<br>- **GiveWell:** a short top-charity list (four per secondary sources) [S].<br>- **Goodstack:** "over 9 million good causes"; 240+ countries [F].<br>- **Benevity:** "more than two million validated nonprofits" [F].<br>- **Pledge:** "over 2 million" [S]. | Medium |
| **Gaps** | - **Small charities:** a CN rating needs ≥3 e-filed 990s in six years, and at least two of the latest four must be full Form 990s. 990-EZ and 990-N filers are therefore unrated ([CN help, 2026-04-09](https://intercom.help/charity-navigator/en/articles/8557824-charity-navigator-s-rating-system)) [F].<br>- **Churches:** they do not file 990s, so no ratings, and they are often absent from Pub 78. In the repo screen, BMF church code 10 holds **$2.17bn** of top-50 DAF grant dollars that are in the BMF but not Pub 78, and another **$1.19bn** of church-labelled lines are absent from both [C].<br>- **Foreign:** CN is US-only; Candid flags FORGN; global coverage sits with Goodstack, Benevity and TechSoup/NGOsource. | High |
| **Implication for an AI-native entrant** | **Eligibility is a solved, cheap commodity; quality signals are fragmented, licence-bound and cover a minority of grantees.** Use IRS files for the reliance record, and license one ratings feed for display under its attribution rules. Build the differentiator around the roughly 83% of Pub 78 entities with no rating (§6). | [I] |

---

## 1. Method and access log

- **Repo inputs.**
  - Donor-feature census `charity_search`/`charity_vetting` cells (DFC-008 to DFC-495).
  - Recipient-compliance screen figures (Pub 78 1,437,291 records; church and foreign labels).
  - Batch 29/30 Candid licence findings.
  - Edges E153–E156 (Chariot's IRS sources; Candid→Groundswell; Candid→Anthropic MCP).
- **robots.txt read (2026-11-15).**
  - **Allowed and fetched:** www.charitynavigator.org (only `/search`, `/basket`, `/profile` and similar are disallowed), developer.charitynavigator.org, intercom.help, developer.candid.org, cdn.candid.org (robots 404 = no rules), docs.every.org (404), blog.every.org, support.every.org (`/hc/en-us/articles` not disallowed), goodstack.io, www.pledge.to, www.givelively.org, www.givingcompass.org, benevity.com (explicitly allows ClaudeBot), www.fidelitycharitable.org, www.daffy.org, docs.endaoment.org, www.irs.gov, www.prnewswire.com, www.nptechforgood.com.
  - **Not fetched:**
    - **give.org:** robots.txt **disallows ClaudeBot, Claude-Web and anthropic-ai**. All BBB WGA facts are [S]. Its S3-hosted annual report was also not fetched, to respect that intent.
    - **candid.org, blog.candid.org, docs.candid.org, dev.candid.org:** 403 on robots.txt.
    - **www.every.org:** 403.
    - **www.dafgiving360.org and www.schwabcharitable.org:** 403.
    - **www.philanthropy.com and www.cuinsight.com:** disallow Claude agents.
    - **files.givewell.org:** bot-challenge page instead of robots.txt.
  - **Fetch failures:**
    - www.givewell.org returned a bot challenge to curl for `/charities/top-charities`. `/plan` was read through WebFetch.
    - www.charitywatch.org returned 403 to the fetch tool. No further attempt was made.
    - nonprofitpro.com redirected (307).
- **No keyed calls.** The CN GraphQL playground, Candid APIs and Every.org API were not called. Plan pages and documentation only.

---

## 2. Provider profiles

### 2.1 Charity Navigator (EIN 13-4148824)

| Item | Finding | Label / source |
|---|---|---|
| Ratings | Encompass Rating System, 0–4 stars. Enhanced in April 2026: "we now score 49 metrics across 10 evaluation areas". Beacon ratings dropped from the API on 2026-04-07 | [F] [release notes](https://www.charitynavigator.org/about-us/our-methodology/ratings/release-notes); [changelog](https://developer.charitynavigator.org/changelog) |
| Coverage | "more than 245,000 charities rated" (also on the developer portal: "more than 245,000 rated nonprofits"). About **1.7 million** nonprofits listed ("Most, but not all, of the 1.7 million nonprofits on the site" can receive Giving Basket gifts) | [F] [about](https://www.charitynavigator.org/about-us/); [developer](https://developer.charitynavigator.org/); [help 2026-04-09](https://intercom.help/charity-navigator/en/articles/8610643-donating-through-the-giving-basket) |
| Eligibility | - Must be a "U.S.-based 501(c)(3) public charity".<br>- "Private foundations, nonprofit subsidiaries, and organizations with revoked or inactive IRS status are not eligible".<br>- Needs "at least three electronically filed IRS Form 990s within the past six years".<br>- "At least two of the four most recent filings must be the standard Form 990".<br>- No revenue floor. | [F] [help, 2026-04-09](https://intercom.help/charity-navigator/en/articles/8557824-charity-navigator-s-rating-system) |
| DAFs as ratees | "DAFs were determined to be ineligible for a rating due to their unusual financial structure" (2024-04-08) | [F] release notes |
| Alerts | Advisory/alert system. On 2026-10-07 the API added alert "sources, nonprofit responses and fake charity details" (premium queries only) | [F] changelog |
| Impact data | - ImpactMatters acquired 2020 (pre-2021; context only) [S].<br>- Impact-Genome-based impact ratings removed 2025-10-07 (v25).<br>- "Launched new Impact Ratings, in collaboration with True Impact" 2026-06-16 (v30.1).<br>- Partnership with True Impact and Blackbaud's YourCause to distribute impact reports to "corporate philanthropy programs, and employee giving platforms". | [F] release notes; [CN blog](https://www.charitynavigator.org/donor-basics/blog/2026-new-strategic-partnership-that-puts-impact-at-the-center-of-giving1/) |
| AI search | "Horizon AI Search", powered by Giving Compass's natural-language search API, launched 2025-11-24 | [F] [CN release](https://www.charitynavigator.org/about-us/press-release/charity-navigator-launches-ai-horizon-search); [Giving Compass API release 2026-01-20](https://www.givingcompass.org/giving-compass-launches-api-to-enable-smarter-philanthropy-where-giving-decisions-are-made/) |
| Giving Basket | - Multi-charity checkout, powered by Give Lively. All funds pass through the **Give Lively Foundation** (its EIN is on receipts).<br>- Give Lively Foundation "charges a 2.5% platform fee"; CN charges none.<br>- Limits: $10–$100,000 per donation; up to 20 nonprofits per cart.<br>- Recipients must be in good standing with the IRS and the California AG registry and carry no "Giving Not Recommended" alert.<br>- **DAF gifts through DAFpay (Chariot), 2.9% fee**, one-time only, not refundable. | [F] [CN help](https://intercom.help/charity-navigator/en/articles/8610643-donating-through-the-giving-basket); [Give Lively](https://www.givelively.org/resources/understand-charity-navigator-giving-basket-donations-and-data-reports); [Give Lively DAF page](https://www.givelively.org/resources/daf-donations-on-giving-basket) |
| Causeway | Cause-fund portfolio platform, "originally launched in 2022 and acquired by Charity Navigator in 2023". Relaunched 2024-09-12. The release does not say whether funds sit in a DAF or name the legal holder | [F] [PR Newswire 2024-09-12](https://www.prnewswire.com/news-releases/charity-navigator-launches-causeway---ahead-of-giving-season-2024-302246077.html) |
| API: what and how | - GraphQL. **Data Essentials** (`publicSearchFaceted`, `bulkNonprofits`) on every plan.<br>- **Premium Data** (`publishedAlerts`) only on Midsize/Enterprise.<br>- Fixed-quota plans "Startups, Small, Midsize, Enterprise"; "Academics/Personal Use" is usage-billed.<br>- 1,000 requests/minute per key. All paid plans start with a 30-day free trial.<br>- Tiers depend on "how many nonprofits you facilitate transactions to, and your total transaction volume", with an annual usage report required. | [F] [plans](https://developer.charitynavigator.org/plans); [data sharing](https://developer.charitynavigator.org/datasharing) |
| API: licence | - Licence "limited, non-exclusive, non-transferable, non-sublicensable".<br>- Fields: EIN, name, URL, address, active advisories, Encompass score/star/publication date/ID, mission, category/cause.<br>- Caching allowed. Redistribution, resale and competing products are restricted.<br>- 1,000 searches/day cap clause in the terms. CN may terminate for convenience on 30 days' notice. | [F] [terms, "Last updated October 2026"](https://www.charitynavigator.org/products-and-services/api/) |
| API: attribution | - "A linkback to a Charity Navigator web page is required wherever our data is used".<br>- Star images "are required to link to the corresponding Charity Navigator rating page".<br>- Ratings may not "be used in any other calculation or manipulated". | [F] [attribution](https://developer.charitynavigator.org/attribution) |
| Cause data | The API's `causes` field is sourced from Candid's Philanthropy Classification System under CC BY 4.0 | [F] changelog |
| Named API users (2026) | - **RoundUp** (since 2026): shows only 3–4-star nonprofits; monthly refresh.<br>- **Givelink** (since spring 2026).<br>- **Allegory** (grant-funding OS, 2026-05-18).<br>- **Carefull** (seniors' giving monitor) [S].<br>- **Perplexity** media mention [S].<br>- **Benevity** named as validation partner [S].<br>- **None is a DAF sponsor.** | [F] [RoundUp](https://developer.charitynavigator.org/customerstory-roundup); [Givelink](https://developer.charitynavigator.org/customerstory-givelink); [Allegory](https://www.charitynavigator.org/about-us/press-release/allegory-integrates-cn-api) |
| Business model | "We don't charge the charities we evaluate"; funded by donors, foundations and corporations, plus API subscriptions | [F] about |

### 2.2 Candid (GuideStar + Foundation Center)

| Item | Finding | Label / source |
|---|---|---|
| APIs | - Essentials v4 and Premier v4 (2026-03-25).<br>- Charity Check (+ Bulk of 25, PDF v2 2025-04-18 with California AG/FTB status).<br>- Grants, Demographics, News ("over 65,000 sources"), Nonprofit Eligibility, Taxonomy (GraphQL), RFP.<br>- Data on Snowflake (2025-04-01) and WRDS (2025-05-06). | [F] [developer.candid.org](https://developer.candid.org/); [llms.txt](https://developer.candid.org/llms.txt) |
| Charity Check sources | "IRS Publication 78, IRS Business Master File, Internal Revenue Bulletin, Automatic Revocation of Exemption, and OFAC Specially Designated National list". Candid pings the IRS "every 20 minutes" and pushes off-cycle updates "in less than 24 hours" | [F] [verification guide 2026-09-07](https://developer.candid.org/docs/verification-using-charity-check.md); [FAQ 2026-09-07](https://developer.candid.org/reference/faqs-charity-check.md) |
| Reliance | FAQ still cites Rev. Proc. 2011-33. Rev. Proc. 2018-32 §8.01 governs; the PDF has gaps on the "most current update" statement and the time stamp | [C] [queue-batch30-legal-circulars.md](queue-batch30-legal-circulars.md) §3 |
| Seals | - Bronze/Silver/Gold/Platinum, renewed yearly. Gold requires a 2024 or 2025 audit/990; Platinum requires a 2025 metric.<br>- The Bronze "Donation" section collects payee legal name, EIN and payment address, "or don't accept donations/don't agree to share information with Candid partners". This is the profile-to-partner data feed.<br>- Premier API exposes `gs_profile_update_level` (e.g. "Platinum 2026") for eligibility rules. | [F] [2026 seals guide](https://cdn.candid.org/seals-of-transparency/2026/candid-seals-guide-2026.pdf); [seal-as-eligibility doc](https://developer.candid.org/docs/guidestar-seal-as-eligibility-requirement.md) |
| Distribution | "more than 200 websites that serve the nonprofit sector", e.g. GlobalGiving and Benevity ([NPTechForGood, 2026-07-19](https://www.nptechforgood.com/2026/07/19/the-top-3-charity-rating-badge-programs-for-nonprofits/)) [F, third-party]. Candid's own page says profiles are shared with 200+ sites, Vanguard Charitable's logo among them [S] | as stated |
| Coverage | "over 1.8 million nonprofit organizations" ([Fidelity page](https://www.fidelitycharitable.org/guidance/research-charities.html)) [F]; "1.9 million organizations" (Candid search release, 2026-01-15) [S] | as stated |
| Price | Explore-APIs: "starting at" $2,750 Charity Check, $4,800 Essentials, $9,900 Premier (period unstated). AlternativeTo reports a range of $2,750–$50,000 "per month"; this conflicts with the official framing and is unresolved | [S] [candid.org/explore-apis](https://candid.org/explore-apis/) |
| Licence | - API Licence (2026-09-14): cease "all use of the Candid Data" on termination; no retention carve-out.<br>- The Subscriber Licence lets pre-termination copies be retained.<br>- Third-party access only as named in the Order Form. | [C] [queue-batch29-regulation-litigation-crypto.md](queue-batch29-regulation-litigation-crypto.md) §4; batch30 §3.3 |
| AI | Candid–Anthropic MCP connector for Claude for Nonprofits (2025-12-02) | [C] edge E156 |
| Model | Nonprofit; "Candid and Charity Navigator are nonprofits with no equity owners" | [C] [private-equity-daf-ecosystem-map.md](private-equity-daf-ecosystem-map.md) |

### 2.3 CharityWatch

- **Grades:** letter grades from "A+ to F, based solely on financial efficiency measurements". Top-Rated status needs B+ or higher ([methodology](https://www.charitywatch.org/charitywatch-criteria-methodology); [top-rated](https://www.charitywatch.org/top-rated-charities)) [S].
- **Access:** detailed ratings are gated behind a donation-based membership; a Consumer Reports comparison says it is the only one of the three main raters that requires this [S, undated].
- **Coverage:** no 2021+ count found. The roughly 600 figure is from a 2013 archive and is not used.
- **Integrations:** no API, licence or DAF integration found. Schwab Charitable guidance lists "Charity Watch" as a vetting resource [S]. Daffy's vetting guide also lists it [S].

### 2.4 GiveWell (The Clear Fund, EIN 20-8625442)

- **Not a data provider to platforms.** It is a recommender and grantmaker.
- **DAF guidance:** its DAF page names Vanguard Charitable and Fidelity Charitable as "Popular DAF providers". Donors recommend grants to "The Clear Fund" and put the allocation (All Grants, Top Charities or Unrestricted Fund) in the purpose field ([givewell.org/plan](https://www.givewell.org/plan)) [F].
- **Volume:** GiveWell reported $616m raised in its 2025 metrics year (+49%) [S].
- **Coverage:** a short top-charity list (four per secondary sources) [S].
- **Integrations:** no API or licensing offer found. Daffy's guide lists it as a research resource [S].

### 2.5 BBB Wise Giving Alliance / Give.org

All facts here are [S], because give.org's robots.txt disallows Claude agents.
- **Standards:** 20 Standards for Charity Accountability. Charities meeting all 20 are "BBB Accredited Charities".
- **Fees:** "no charge for charity accreditation". The seal licence is optional, "for a sliding scale annual fee … based on the level of total contributions" ([about seal licensing](https://give.org/about-charity-seal-licensing)).
- **Coverage:** about 1,500 reports on nationally soliciting charities (2024 annual report).
- **Integrations:** no API or platform integration found. Repo P-CMP-08 found that BBB has no DAF-sponsor profiles [C].

### 2.6 ImpactMatters

- **Acquisition:** acquired by CN in October 2020 (pre-2021; context only) [S].
- **Current state:** the impact methodology fed CN's Impact & Results beacon. Impact ratings based on Impact Genome data were removed on 2025-10-07, and True Impact-based Impact Ratings launched on 2026-06-16 [F, CN release notes].
- **[I]** The ImpactMatters lineage is no longer a distinct live dataset.

### 2.7 Every.org (EIN 61-1913297)

- **Charity API:** Nonprofits API, Fundraisers API, Donate Button/Link and Webhooks. Search covers "over 1 million 501(c)(3) organizations". It is "free". "Every.org does not provide programmatic donations or disbursements via API". The data source is not stated. Named users: Giving Multiplier, Fungi Foundation, Noble Strength Foundation ([docs](https://docs.every.org/docs/intro)) [F].
- **No ratings:** "No, Every.org is not a nonprofit evaluator or ratings organization" (2022-04-14; [help](https://support.every.org/hc/en-us/articles/360059998993-Do-you-rate-nonprofits)) [F].
- **Origin:** "Giving Commons" open-infrastructure framing, Gates-funded (2022-11-15; [blog](https://blog.every.org/giving-commons/)) [F].

### 2.8 Goodstack (ex-Percent)

- **Coverage:** "a global database of over 9 million good causes" ([verifications](https://goodstack.io/verifications)) [F].
- **KYNP ("Know Your Nonprofit"), 2026-08-03:**
  - three due-diligence tiers plus ongoing monitoring;
  - screening across "240+ countries and territories", "130+ international and national sanctions lists", "120+ law enforcement and financial crime watchlists" and adverse media from "11,000+ sources";
  - "7.5 million nonprofit verifications";
  - customers named: Google, Canva, ElevenLabs ([blog](https://goodstack.io/blog/7-5m-verifications-in-introducing-kynp-know-your-nonprofit)) [F].
- **Pricing:** not published.
- **DAF link:** Goodstack's US flows are legally donor-advised gifts via Goodstack Impact Foundation US [C: batch30 B §3].

### 2.9 Pledge (Pledgeling Technologies)

- **Database:** "the world's largest and most compliant database of verified 501(c)(3) nonprofit & charitable organizations"; no count on the page [F].
- **Fees:** "no charge to use our API"; Donate API takes 5% plus processing ([pledge.to/products/apis](https://www.pledge.to/products/apis)) [F].
- **Coverage:** the developer page says "over 2 million nonprofits" [S].
- **Logo partners:** include Blackbaud and California Community Foundation [F, logos only; nature of relationship not stated].

### 2.10 IRS data (the shared base layer)

- **Bulk files:** Pub 78, the Auto-Revocation list, 990-N and the Form 990 e-file XML. "The data set files are updated monthly". No fee is stated ([TEOS bulk downloads, reviewed 2026-09-16](https://www.irs.gov/charities-non-profits/tax-exempt-organization-search-bulk-data-downloads)) [F]. The EO BMF extract is linked separately.
- **Repo snapshot:** Pub 78 data Last-Modified 2026-11-11, 1,437,291 records; BMF 2026-11-09 [C: recipient screen §5].
- **Reliance:** Rev. Proc. 2018-32 §8.01 lets grantors rely on TEOS/BMF data, or third-party reports meeting its elements, if a copy is retained [C].
- **Who builds on it:**
  - Chariot's compliance database draws on "six primary sources incl. IRS BMF, Form 990, Pub 78, OFAC" [C: E153].
  - Daffy's database is IRS-based [S].
  - Candid's Charity Check repackages it [F].

### 2.11 Adjacent providers seen in DAF-adjacent flows

| Provider | Relevance | Source |
|---|---|---|
| **Giving Compass** (501(c)(3)) | - Natural-language search, impact and feed APIs (2026-01-20) for "wealth advisors, philanthropic leaders, and donor-focused organizations"; price not disclosed.<br>- Powers CN Horizon.<br>- Its news widget is embedded on Fidelity Charitable's guidance pages. | [F] |
| **Benevity** | - "more than two million validated nonprofits". Claude for Nonprofits MCP integration partner (2025-12-02).<br>- Due-diligence add-ons include watchlist screening.<br>- CN, TechSoup, LexisNexis and Moody's are named as due-diligence partners on a page version seen only in a snippet. | [F] [release](https://benevity.com/press-releases/benevity-integrates-global-nonprofit-network-with-anthropics-claude); [due diligence](https://benevity.com/solutions/nonprofit-due-diligence); partners [S] |
| **ECFA / MinistryWatch** | Faith-sector accreditation and ratings (e.g. MinistryWatch "Donor Confidence Score"). The only rater family that covers some ministries CN cannot rate. No DAF integration found | [S] |
| **NGOsource** (TechSoup) | Equivalency determinations for foreign grantees. NPT requires "a legal opinion of equivalency" or charitable-use controls for non-US grants [S]. No 2025–26 fee schedule verified | [S] |

---

## 3. Sponsor and vendor integration matrix (public evidence)

**Key.**
- **Embedded:** the provider's data appears in the donor's grant flow.
- **Linked:** an outbound reference only.
- **Source:** used for eligibility.
- **ND:** nothing found on the pages read.

| Sponsor / vendor | Candid | Charity Navigator | Other raters | IRS direct | Evidence |
|---|---|---|---|---|---|
| Fidelity Charitable | Linked ("GuideStar … over 1.8 million") | Linked; CN Advisory System cited for fraud | Giving Compass news widget (embedded, not a rating); Great Nonprofits listed | "IRS databases" in due diligence | [F] [research](https://www.fidelitycharitable.org/guidance/research-charities.html); [fraud](https://www.fidelitycharitable.org/guidance/research-charities/avoiding-fraudulent-charities.html); [due diligence](https://www.fidelitycharitable.org/legal/granting-due-diligence.html); [supported charities](https://www.fidelitycharitable.org/giving-account/supported-charities.html) |
| DAFgiving360 (Schwab) | Listed as the main search resource (keyword, location, category, revenue, EIN) | Listed | Schwab material lists GuideStar, CN, Charity Watch | Researches eligibility of charities not in its databases | [S] (host robots 403) |
| Vanguard Charitable | **Embedded** (NAVi locator among Candid partner sites; "pull data directly from Candid") | ND | ND | ND | [S] candid.org blog; 2017 GuideStar directory launch is pre-2021 context |
| Bank of America CGF | **Embedded** ("search the GuideStar database") | ND | ND | ND | [C] DFC-188 (2025-09 PDF) |
| NPT | ND (own due-diligence articles name no vendor) | ND | ND | 501(c)(3) and public-charity check; foreign equivalency | [S] |
| Daffy | ND as source; GuideStar listed in vetting guide | Listed in vetting guide | CharityWatch, GiveWell, GivingCompass listed | **Source:** "every US-based not-for-profit organization in good standing with the IRS" | [S]; churches [F] [help 2026-04-02](https://intercom.help/daffy/en/articles/5596770-can-i-donate-to-a-church-or-other-house-of-worship) |
| Every.org | ND | ND | "not a nonprofit evaluator" | Own 1M+ dataset; source not stated | [F] |
| Endaoment | ND | ND | ND | Public org search endpoint; source not stated | [F] [docs](https://docs.endaoment.org/developers/quickstart/search-for-org.md) |
| Groundswell | **Embedded** ("Candid GuideStar integration") | ND | ND | ND | [C] E155 |
| Chariot (DAFpay) | ND | **Rail into CN Giving Basket** | — | **Source:** BMF, 990, Pub 78, OFAC (six sources) | [C] E153; [F] Give Lively |
| Benevity | "uses Candid" (third-party claim) | Named partner [S] | TechSoup; watchlists | Government registries | [F]/[S] |
| Morgan Stanley GIFT | ND | ND | ND | "Charity Vetting Automated" (no provider named) | [C] DFC-117 |

**[I] Reading.**
- **Candid is the de facto search and profile layer inside sponsor portals.** CN appears only as donor-education links.
- The one live CN↔DAF money link runs **into** CN's Giving Basket via Chariot DAFpay, not from CN data into sponsor portals.
- The owner's hypothesis of a CN partnership with Fidelity Charitable or DAFgiving360 is **not supported by public evidence**. Both point donors to CN; neither shows embedded ratings on pages read.

---

## 4. What donors are shown

| Signal | Provider | Where seen in DAF context | Typical display |
|---|---|---|---|
| Eligibility (501(c)(3), public charity, not revoked, not SDN) | IRS via Candid Charity Check, Chariot, or in-house | All sponsors (approval step, mostly invisible) | Pass/hold. A charity not in the database triggers sponsor research (DAFgiving360, Daffy, Vanguard FAQ) |
| Profile (mission, programs, financials, seal) | Candid | Vanguard, BofA, Groundswell (embedded); Fidelity, DAFgiving360 (linked) | Profile card. Seal level (Bronze–Platinum + year) |
| Star rating 0–4 + score; alerts | CN | No sponsor embed found. Embedded at RoundUp, Givelink, Allegory (non-DAF) | Star image with mandatory linkback |
| Letter grade A+–F | CharityWatch | Linked only (Schwab, Daffy guides) | Behind membership |
| Accreditation (20 standards) | BBB WGA | No integration found | Seal licensed to charity for a fee |
| Cost-effectiveness recommendation | GiveWell | GiveWell's own DAF instructions | Grant to The Clear Fund with allocation note |
| Global verification / KYNP | Goodstack, Benevity | Workplace and corporate giving; Goodstack's US DAF entity | Verified / not verified |

---

## 5. Licensing and business models

| Provider | Model | Published price | Key licence terms for an entrant |
|---|---|---|---|
| CN | Nonprofit; donor-funded plus API subscriptions | Tier names only; dollar prices script-rendered, not captured; 30-day trial | No sublicensing or redistribution; caching allowed; linkback and star-image rules; no recalculation of ratings; annual usage report; tier keyed to transaction volume; terminable on 30 days' notice |
| Candid | Nonprofit; subscriptions and API licences | "Starting at" $2,750 / $4,800 / $9,900 [S] | Cease all use on termination (API licence); third parties only as named in the Order Form; Derivative Works owned by licensee [C] |
| CharityWatch | Membership donations | n/a | No API found |
| BBB WGA | Free evaluation; seal licence fee paid by the charity | Sliding scale (not captured) [S] | No API found |
| GiveWell | Donor-funded grantmaker | n/a | No data licence offered |
| Every.org | Free API; tips | Free | Terms page not readable (403) |
| Goodstack | Commercial verification and donation infrastructure | Not published | Not read |
| Pledge | Free API; 5% on Donate-API gifts | Stated | Not read |
| IRS | Public | Free | Public domain; reliance under Rev. Proc. 2018-32 |
| Giving Compass | Nonprofit API vendor | Not disclosed | Not read |

---

## 6. Coverage and gaps

**Coverage arithmetic [I].**
- CN rated (245,000) ÷ Pub 78 records (1,437,291) = **17.0%**.
- CN rated ÷ CN profiles (about 1.7m) = **14.4%**.
- Every.org (1m+), Daffy (1.7m+ per census DFC-368), Charityvest (1.4m) and Givinga (1.7m) all sit near the Pub 78/BMF universe. They are **eligibility** universes, not quality universes.

**Small charities.**
- CN's three-e-filed-990 and two-full-990 rules exclude 990-EZ and 990-N filers by construction.
- Candid's Gold Seal accepts a 990-N, so seals reach further down than stars.
- The Chariot/Candid eligibility layers cover small organisations fully, because Pub 78 does.

**Churches.**
- Not rated by CN in practice (no 990).
- Candid returns a "Pub78 Church Message" and a "BMF Church Message" field ("not required to appear on the IRS BMF to establish their status") ([fields doc, 2026-11-10](https://developer.candid.org/reference/interpret-charity-check-data-fields.md)) [F].
- Daffy handles houses of worship manually ("a few days to several weeks") [F].
- In the repo's top-50 Schedule I screen, BMF foundation code 10 holds **$2.17bn** of grant dollars in the BMF but not Pub 78. **$1.19bn** of church/religious-labelled dollars are absent from both lists [C: direction-recipient-compliance-screen.md §0]. These are the largest blind spot for any ratings-led search.

**Group subordinates.** BMF-not-Pub 78 dollars are $3.65bn, almost all group-subordinate [C]. Ratings attach to the central organisation, if at all.

**Foreign.**
- CN rates only US-based charities [F].
- Candid flags FORGN [F].
- NPT requires equivalency or charitable-use controls [S].
- Global verification sits with Goodstack (240+ countries) and Benevity (2m+) [F], and with NGOsource for equivalency [S].
- The recipient screen did not screen Schedule F [C].

**DAFs and private foundations.** CN does not rate DAF sponsors (2024) or private foundations, so DAF-to-DAF and PF grants carry no rating [F].

---

## 7. Implications for an AI-native entrant [I]

1. **Two layers, two procurement paths.**
   - **Eligibility:** IRS Pub 78/BMF/revocation plus OFAC. This is free, monthly and reliance-grade under Rev. Proc. 2018-32 if the entrant time-stamps and retains its own BMF-sourced report. Building it in-house avoids Candid's no-retention-after-termination clause.
   - **Quality** (ratings, seals, impact): licensed and attribution-bound.
2. **CN is the cheapest recognisable quality signal to embed, but its licence constrains agents.**
   - "Non-sublicensable" and the ban on using ratings "in any other calculation" mean an LLM ranker that **blends** CN scores into its own score risks breaching the terms.
   - Mandatory linkbacks and official star images assume a web UI, not a chat or MCP surface.
   - An entrant should ask for written clarification before using ratings as model features (see P-B43N26-03).
3. **Candid is the incumbent sponsor layer.** An entrant that matches sponsor portals on search needs Candid-grade profiles. The open route is IRS 990 e-file XML plus Candid's CC BY PCS taxonomy (which CN itself uses).
4. **The differentiator is the unrated majority.**
   - About 83% of Pub 78 entities, churches ($2.17bn + $1.19bn in the top-50 sample) and foreign grantees have no star rating.
   - An AI vetting layer that reads 990/990-EZ/990-N, state registries and the charity's own site can produce transparent, source-cited summaries where no rating exists. It must label them as non-ratings to avoid "rating" claims.
5. **AI search is already commoditising.** CN Horizon (Giving Compass), Candid's Claude MCP connector and Benevity's Claude MCP integration mean natural-language charity search is not a moat by itself. Moats are reliance-grade audit trails, grant execution and church/foreign handling.
6. **Rails matter more than ratings for DAF money flow.** The live CN↔DAF link is DAFpay into the Giving Basket. Grant initiation from rating sites is a distribution channel that sponsors have not shut out.

---

## 8. Source register

| ID | Source | Type | Date / version | Label |
|---|---|---|---|---|
| R1 | [CN API terms](https://www.charitynavigator.org/products-and-services/api/) | licence | "Last updated October 2026" | F |
| R2 | [CN developer portal](https://developer.charitynavigator.org/); [plans](https://developer.charitynavigator.org/plans); [attribution](https://developer.charitynavigator.org/attribution); [data sharing](https://developer.charitynavigator.org/datasharing); [changelog](https://developer.charitynavigator.org/changelog) | vendor docs | live 2026-11-15; changelog to 2026-10-07 | F |
| R3 | [CN customer stories: RoundUp](https://developer.charitynavigator.org/customerstory-roundup), [Givelink](https://developer.charitynavigator.org/customerstory-givelink) | vendor case study | 2026 | F |
| R4 | [CN ratings release notes](https://www.charitynavigator.org/about-us/our-methodology/ratings/release-notes) | methodology | 2023-09 to 2026-08 | F |
| R5 | [CN rating-system help](https://intercom.help/charity-navigator/en/articles/8557824-charity-navigator-s-rating-system); [Giving Basket help](https://intercom.help/charity-navigator/en/articles/8610643-donating-through-the-giving-basket); [Spring 2026 update](https://intercom.help/charity-navigator/en/articles/14471517-spring-2026-rating-methodology-update) | help centre | 2026-04-09 | F |
| R6 | [CN about](https://www.charitynavigator.org/about-us/) | first-party | live | F |
| R7 | [CN Horizon release](https://www.charitynavigator.org/about-us/press-release/charity-navigator-launches-ai-horizon-search); [Allegory release](https://www.charitynavigator.org/about-us/press-release/allegory-integrates-cn-api); [True Impact blog](https://www.charitynavigator.org/donor-basics/blog/2026-new-strategic-partnership-that-puts-impact-at-the-center-of-giving1/) | press | 2025-11-24; 2026-05-18; 2026 | F |
| R8 | [Give Lively: CN Giving Basket](https://www.givelively.org/resources/understand-charity-navigator-giving-basket-donations-and-data-reports); [DAF donations on Giving Basket](https://www.givelively.org/resources/daf-donations-on-giving-basket) | vendor docs | live (© 2026) | F |
| R9 | [Causeway relaunch, PR Newswire](https://www.prnewswire.com/news-releases/charity-navigator-launches-causeway---ahead-of-giving-season-2024-302246077.html) | press | 2024-09-12 | F |
| R10 | [Giving Compass API release](https://www.givingcompass.org/giving-compass-launches-api-to-enable-smarter-philanthropy-where-giving-decisions-are-made/) | press | 2026-01-20 | F |
| R11 | [Candid developer portal](https://developer.candid.org/); [llms.txt](https://developer.candid.org/llms.txt); [Charity Check FAQ](https://developer.candid.org/reference/faqs-charity-check.md); [fields](https://developer.candid.org/reference/interpret-charity-check-data-fields.md); [verification guide](https://developer.candid.org/docs/verification-using-charity-check.md); [seal-as-eligibility](https://developer.candid.org/docs/guidestar-seal-as-eligibility-requirement.md) | vendor docs | 2026-09-07 to 2026-11-10 | F |
| R12 | [Candid 2026 Seals guide](https://cdn.candid.org/seals-of-transparency/2026/candid-seals-guide-2026.pdf) | vendor PDF | 2026 | F |
| R13 | [candid.org/explore-apis](https://candid.org/explore-apis/); Candid DAF blog (Vanguard grants manager); Candid search release 2026-01-15 | vendor | — | S (robots 403) |
| R14 | [NPTechForGood badge programs](https://www.nptechforgood.com/2026/07/19/the-top-3-charity-rating-badge-programs-for-nonprofits/) | trade press | 2026-07-19 | F |
| R15 | [Fidelity Charitable research charities](https://www.fidelitycharitable.org/guidance/research-charities.html); [fraud page](https://www.fidelitycharitable.org/guidance/research-charities/avoiding-fraudulent-charities.html); [high-impact](https://www.fidelitycharitable.org/guidance/giving-strategies/high-impact.shtml); [due diligence](https://www.fidelitycharitable.org/legal/granting-due-diligence.html); [supported charities](https://www.fidelitycharitable.org/giving-account/supported-charities.html) | sponsor | live 2026 | F |
| R16 | DAFgiving360 explore-charities / finding charities; Schwab vetting guidance | sponsor | — | S (robots 403) |
| R17 | Daffy answers pages (IRS database; vetting guides) | sponsor | — | S |
| R18 | [Daffy churches help](https://intercom.help/daffy/en/articles/5596770-can-i-donate-to-a-church-or-other-house-of-worship) | sponsor help | 2026-04-02 | F |
| R19 | [Every.org Charity API docs](https://docs.every.org/docs/intro); [Do you rate nonprofits](https://support.every.org/hc/en-us/articles/360059998993-Do-you-rate-nonprofits); [Giving Commons](https://blog.every.org/giving-commons/) | platform | live; 2022-04-14; 2022-11-15 | F |
| R20 | [Endaoment Find a Nonprofit](https://docs.endaoment.org/developers/quickstart/search-for-org.md); [Org FAQ](https://docs.endaoment.org/organizations/resources/organization-faq.md) | platform docs | live | F |
| R21 | [Goodstack verifications](https://goodstack.io/verifications); [KYNP blog](https://goodstack.io/blog/7-5m-verifications-in-introducing-kynp-know-your-nonprofit) | vendor | live; 2026-08-03 | F |
| R22 | [Pledge APIs](https://www.pledge.to/products/apis) | vendor | live (© 2026) | F |
| R23 | [Benevity–Claude release](https://benevity.com/press-releases/benevity-integrates-global-nonprofit-network-with-anthropics-claude); [due diligence](https://benevity.com/solutions/nonprofit-due-diligence) | vendor | 2025-12-02; live | F |
| R24 | [GiveWell DAF page](https://www.givewell.org/plan) | recommender | live | F |
| R25 | CharityWatch methodology / top-rated pages; Consumer Reports comparison | rater | — | S |
| R26 | Give.org seal licensing; 2024 BBB WGA annual report | rater | 2024 report | S (robots disallow Claude) |
| R27 | [IRS TEOS bulk downloads](https://www.irs.gov/charities-non-profits/tax-exempt-organization-search-bulk-data-downloads) | government | reviewed 2026-09-16 | F |
| R28 | Repo: direction-recipient-compliance-screen.md; direction-donor-feature-census.md / donor-feature-census-2026.csv; queue-batch30-legal-circulars.md; queue-batch29-regulation-litigation-crypto.md; relationship-graph edges E153–E156 | repo | 2026-11-14/15 | C |
| R29 | ImpactMatters acquisition coverage (MinistryWatch, Devex, EA Forum) | press | 2020 (pre-2021; context only) | S |

---

## 9. Data dictionary

### `charity-data-provider-integrations-2026.csv`

| Column | Meaning |
|---|---|
| row_id | CDP-001… |
| provider | Data or ratings provider (Charity Navigator, Candid, CharityWatch, GiveWell, BBB WGA, ImpactMatters, Every.org, Goodstack, Pledge, IRS, Giving Compass, Benevity) |
| row_type | `coverage`, `eligibility_rule`, `pricing`, `licence`, `product`, `integration`, `gap`, `business_model` |
| integrator | For `integration` rows: the sponsor, vendor or platform using the provider. Blank otherwise |
| integrator_type | `daf_sponsor`, `daf_technology_vendor`, `payment_rail`, `giving_platform`, `ai_platform`, `workplace_giving`, `grant_platform` or blank |
| integration_mode | `embedded` (data in donor flow), `linked` (outbound reference), `eligibility_source`, `rail`, `api_customer` or blank |
| shown_to_donors | What the donor sees (rating, seal, profile, eligibility only, none) |
| value | The fact, figure or tier as stated |
| quote_or_basis | Verbatim quote (≤40 words) or basis |
| source_url | Primary URL (repo path for carried rows) |
| source_date | Document date, or `live 2026-11-15` for undated pages |
| evidence_label | F, S, C or I (see the head of this note) |
| recency_ok | `yes` (2021–2026 or live), `context_only` (pre-2021) |
| retrieved | 2026-11-15 |
| notes | Caveats and conflicts |

### `relationship-graph-edges-additions-25.csv`

Same columns as `relationship-graph-edges.csv`. The prefix is `EY`. `status` is `confirmed` (first-party [F] or repo [C]) or `reported` (snippet [S] only). Relationship types reuse existing vocabulary where possible (`charity_verification`, `api_partner`, `technology_provider`, `integration_partner`, `acquired`, `data_feed`, `ai_provider`, `payment_processor`, `partnership`). One new type, `donor_research_link`, means a sponsor page links donors to the provider without embedding its data.

### `queue-proposals-batch43-n26.csv`

Columns and scales follow [queue-proposals-README.md](../../data/mission-2026-11-14/queue-proposals-README.md). The prefix is `P-B43N26-`, and `proposed_by` is `batch43 N26`.

---

## 10. Limits

- **No logged-in views.** Sponsor portals may embed ratings behind login. Every "ND" means not found on public pages read.
- **Blocked or failed hosts.** candid.org, give.org (Claude disallowed), dafgiving360.org, schwabcharitable.org and www.every.org could not be read. Their facts are [S]. CharityWatch and GiveWell pages returned 403 or a bot challenge to the fetch tools.
- **Prices not captured.** CN's dollar prices sit in a script-rendered page that was not executed. Candid's "starting at" figures are a snippet with an unstated billing period.
- **Vanguard claims.** The Vanguard–Candid evidence (NAVi; "twice the amount in DAF grants" for Platinum-Seal organisations) comes from Candid's marketing blog via snippet. It is undated in what was seen.
- **Coverage counts are vendor-stated.** Goodstack's "9 million" causes and "7.5 million" verifications are different measures.
- **Benevity's CN partnership** appears only in a search snippet of its due-diligence page. The page fetched today does not name partners.
- **Fetch-tool summaries.** WebFetch summarises pages. Quotes above are short extracts returned by it, or by direct text extraction for the CN developer pages and the Candid docs (downloaded as Markdown).
