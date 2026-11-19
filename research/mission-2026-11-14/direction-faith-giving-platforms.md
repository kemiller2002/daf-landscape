# Direction P-NEW-FTH-01: do church giving platforms and faith DAF sponsors support DAF grants, and why do religious donate pages rarely show a DAF option?

**Date:** 2026-11-15 · **Queue item:** P-NEW-FTH-01 (new direction from the owner)

**Outputs**
- [`data/mission-2026-11-14/faith-giving-platform-daf-support-2026.csv`](../../data/mission-2026-11-14/faith-giving-platform-daf-support-2026.csv): 23 rows. It covers 10 church giving platforms (one unresolved), 9 faith DAF sponsors, 2 national-sponsor benchmarks, the Chariot rail and 2 non-cash processors.
- [`data/mission-2026-11-14/queue-proposals-batch41-n15.csv`](../../data/mission-2026-11-14/queue-proposals-batch41-n15.csv): P-B41N15-01..03.

**Rules applied**
- **Read first:**
  - [direction-nonprofit-donate-pages.md](direction-nonprofit-donate-pages.md), with its governing wave-24B correction. The USCCB "donate page" is a news article, so religion is 3 of 13 (23%) without it.
  - [direction-recipients-impact-matching.md](direction-recipients-impact-matching.md), with its governing wave-24A corrections. Neither touches the religion share.
  - [queue-batch33-market-structure.md](queue-batch33-market-structure.md): faith *sponsor* platforms, with the wave-18/19 corrections.
  - [compliance-note-crtsh-robots.md](compliance-note-crtsh-robots.md): no crt.sh.
- **Polite fetching:**
  - robots.txt was read for every host before any page on it.
  - Unreadable or blanket-disallow robots.txt meant the host was not fetched: help.thesignatry.com (`User-agent: * Disallow: /`), religionnews.com (403), catholiccommunityfoundation.org (no response).
  - Pages under a disallowed path were not fetched (jewishdetroit.org `/wp-content/`).
  - No logins, forms, donations or outreach.
- **Recency:** all platform pages are live 2026 pages or posts dated 2023-06 to 2026-10. Sponsor policies are dated 2023-12 to 2026. Recipient dollars are the repo's FY2023–24 Schedule I lines.
- **Labels:**
  - **[O]** observed on a fetched live page;
  - **[F]** filed or formal document (policy PDF, annual report);
  - **[S]** search-result statement only, not confirmed on a fetched page;
  - **[C]** computation;
  - **[R]** existing repo finding;
  - **[I]** inference;
  - **[U]** unresolved.

---

## 0. Answers in brief

| Question | Answer |
|---|---|
| **Do church giving platforms take DAF grants in checkout?** | **Only Overflow does, through Chariot (since 2023-06-29)** [O].<br>- **Pushpay** lists "DAF Attribution" as *Coming soon* and "DAF/IRA Automation" as upcoming, with no rail named [O].<br>- **Subsplash** and **Planning Center** let churches *record* DAF and QCD gifts (Planning Center by batch or API) and put them on statements; neither offers a grant rail [O].<br>- **Tithely, Givelify, Kindrid/Ministry Brands and ACST Realm/Vanco:** no DAF content on their product pages [O].<br>- **"OneRealm":** no product of that name found [U]. |
| **Stock and crypto** | Common, through two processors [O]:<br>- **Engiven** for Pushpay, Tithely, Subsplash and ACST Realm;<br>- **The Giving Block** for Ministry Brands.<br>A search extract says Ministry Brands stock gifts land in the *Modern Philanthropy Foundation donor-advised fund* [S]. If so, the church receives them as a processor-DAF grant. |
| **How congregations are told to receive DAF gifts** | Only Subsplash publishes congregation-facing DAF instructions (2026-10-01) [O]:<br>- list the legal name, EIN and mailing address;<br>- add a "Give from my Donor-Advised Fund" button or link;<br>- record the gift as from the sponsor and do not receipt the donor.<br>It names Fidelity, DAFgiving360, Vanguard and NCF, not DAFpay. |
| **Published DAF volume statistics from platforms** | **None.** No church platform publishes DAF volume.<br>- Overflow's launch post cites only industry figures.<br>- Scale figures exist but do not split out DAFs: Pushpay "$62.9B" cumulative; Ministry Brands "$6.5B" a year; Givelify "over $1 billion in 2023"; Tithely 53,000 churches; ACST+Vanco 40,000+ churches [O]. |
| **How faith sponsors pay congregations** | **Sponsor-initiated, sponsor-paid; no donate page needed** [O/F]:<br>- **NCF:** grants "via ACH or electronic transfer when available", wire on request; any 501(c)(3) public charity "including churches".<br>- **JCF NY:** check or ACH/wire "at the discretion of JCF staff… sent directly to the charity", after staff verify tax status and mailing address; 99% of grants name the fundholder.<br>- **JCF LA:** ACH (24–48 h) or check (up to four weeks); synagogue dues allowed as a "spiritual benefit". JCF NY bars memberships with a nondeductible portion.<br>- **WaterStone** and **NCF** run single-charity funds that let churches take in stock and complex assets.<br>- **LDS:** tithing is "not processed by Philanthropies"; local leaders handle it. |
| **Faith sponsors on the DAFpay rail** | **Thin.** Chariot's partner lists name Dallas Jewish Community Foundation and Jewish Federation of Northern NJ as disbursement partners, and Thrivent Charitable on DAFpay (Oct 2025 [S]) [O]. NCF, Signatry, WaterStone and JCF NY do not appear. |
| **Why 21% vs 13.6%? (evidence-based; §4)** | **E1. The scan does not reach congregations.** The 22 top-300 religion recipients hold only **15%** of religion's $10.55bn (all sectors: 31%); 14 pages holding 7.9% were scanned, and none is a congregation [C].<br>**E2. Religion DAF money is many small grants:**<br>- Fidelity: religion is **27% of grants but 13.1% of dollars**, implied average ≈ **$2,815** vs $5,801 [F/C];<br>- Schedule I: religion has **32% of recipients** for 13.6% of dollars [C].<br>**E3. Sponsors push grants to churches** by name or EIN and pay by ACH or check [O/F].<br>**E4. Church platforms lack a DAF rail** (except Overflow) [O].<br>**E5. Churches need not be IRS-listed or file a 990.** That adds onboarding friction: Chariot needs alternative verification, and Fidelity mails checks to the Form 990 address [O]. The effect is [I].<br>**E6. Tithing, dues and pledges run through church channels**, not public donate pages (LDS; synagogue dues) [O/I]. |

---

## 1. Church giving platforms (CSV FTH-01..FTH-10)

| Platform | In-checkout DAF grant | DAF recording | Stock / crypto | Source |
|---|---|---|---|---|
| **Pushpay** | **Announced, not live.** "DAF Attribution" is labelled *Coming soon*: "Gifts from donor-advised funds match automatically to donor records". "DAF/IRA Automation": "Donors can start a DAF or IRA gift from the giving journey". "Enhanced Giving Statements… Includes DAF gifts… by default" [O] | Announced | Yes, through Engiven ("zero annual fees") [O] | [pushpay.com/digital-giving](https://pushpay.com/digital-giving) (undated, © 2026) |
| **Tithely** | Not found. Home and giving pages list card, ACH, AMEX, wallets, text, kiosk and tap [O] | Not found | Through Engiven. The 2026-09-09 post says "no annual fee, and the donor covers the transaction cost" and does not mention DAFs [O]. The help centre returned 403; a "4% fee, manual entry" FAQ is a search extract only [S] | [get.tithe.ly](https://get.tithe.ly/); [blog](https://get.tithe.ly/blog/crypto-stock-giving-for-churches) |
| **Subsplash Giving** | **No.** Recording plus instructions (§2) | **Yes:** "Record and manage… donor-advised fund (DAF), and qualified charitable distribution (QCD)" gifts; non-cash gifts "appear in a distinct section of each statement" (2025-11-19) [O] | Through Engiven [O] | [product post](https://subsplash.com/blog/new-subsplash-giving-tools-simplify-multiply-generosity); [DAF guide](https://www.subsplash.com/blog/donor-advised-funds-for-churches) |
| **Planning Center Giving** | **No** | **Yes** (2024-09-12): "Set up new payment sources for nondeductible gifts (QCDs and DAFs)", entered "using our batches tool or API". Statements can include them, "clearly marked as nondeductible" [O] | Not on the fetched page | [planningcenter.com blog](https://www.planningcenter.com/blog/2024/09/track-nondeductible-donations-in-giving) |
| **Overflow** | **Yes, Chariot.** Launched 2023-06-29: "Recommending a DAF gift with Overflow is as straightforward as checking out from an online store." The church sees "which donor initiated the gift". The current page says "we make it easy to accept DAF contributions through Chariot" [O] | Yes (dashboard) | Yes (repo §2.3 of direction-noncash-gift-infrastructure.md) [R] | [launch](https://www.overflow.co/learn/overflow-introduces-new-way-to-give); [DAF page](https://www.overflow.co/overflow-giving/dafs) |
| **Givelify** | Not found [O] | Not found | Not found | [givelify.com](https://www.givelify.com/); [giving page](https://www.givelify.com/organizations/solutions/giving/) |
| **Kindrid** (Ministry Brands) | Not found. Online, mobile and text giving only [O] | Not found | Not on page | [ministrybrands.com/kindrid](https://www.ministrybrands.com/kindrid) |
| **Ministry Brands Amplify** | Not found. The DAF explainer URL served a generic page with no DAF text [O] | Not found | Through The Giving Block: "setting up your account with The Giving Block" [O]. Stock reportedly routed to the Modern Philanthropy Foundation DAF [S] | [stock-crypto](https://www.ministrybrands.com/giving/stock-crypto); [help FAQ (403)](https://help.ministrybrands.com/hc/en-us/articles/20045162705947-Stock-Crypto-Donation-FAQ) |
| **Vanco faith / ACS Technologies Realm** | Not found. Vanco's faith arm and ACST combined on 2025-12-03 and operate as ACS Technologies, serving "more than 40,000 churches and ministries" [O] | Not found | Realm: "With our Engiven integration, your donors can give stocks and cryptocurrency"; "not available in Canada" [O] | [Vanco release](https://www.vancopayments.com/newsroom/vanco-and-acs-technologies-unite-to-deliver-more-connected-services-and-solutions-for-churches); [Realm giving](https://www.acstechnologies.com/realm/tools/giving/) |
| **OneRealm** | **[U]** No product of this name was found. onerealm.com returns 404. Treated as a possible reference to ACST Realm; nothing was invented | — | — | — |

**Chariot's own documentation** ([help.givechariot.com/llms-full.txt](https://help.givechariot.com/llms-full.txt), read 2026-11-15) names no church giving platform among its integrations or partners [O]. It does address houses of worship directly:
- "Religious institutions such as churches, synagogues, mosques, and other places of worship **can still be eligible**, even if they are **not listed** in the IRS Exempt Organizations database." Verification uses "EIN documentation", "articles of incorporation or bylaws" and the IRS 14-point church criteria.
- "Houses of worship may qualify even if they have not formally filed for 501(c)(3) status, depending on the policies of the DAF provider."
- Pub 78 exceptions include "Churches and Religious Organizations – Not required to register or file Form 990s" and "Subordinate Organizations – Groups under a group exemption may not have individual listings."

**Reading [I]:** the large church platforms (Pushpay, Tithely, Subsplash, Planning Center, Ministry Brands, ACST/Vanco) have added stock and crypto through processors. They treat DAF grants as gifts that arrive from outside and are recorded afterwards, not as a checkout method. Overflow is the only Chariot-connected church platform found. Pushpay's roadmap item is the main sign this may change; P-B41N15-03 tracks it.

## 2. What congregations are told to do

- **Subsplash (2026-10-01, guest author)** [O]. "Churches can receive DAF grants by listing their legal name, EIN, and mailing address on their giving page."
  - Add a "Give from my Donor-Advised Fund" button or link.
  - Put "We accept gifts from Donor Advised Funds" in materials.
  - "Record the gift as coming from the DAF sponsor."
  - Thank the donor if known, but do not issue a tax receipt.
  - It cites Fidelity's 2026 report on religion's lead in grant counts and does not mention DAFpay.
- **Planning Center** documents only the bookkeeping step: a DAF payment source, then batch or API entry [O].
- **Pushpay, Tithely, Givelify, Kindrid/Ministry Brands, ACST/Vanco:** no congregation-facing DAF instructions were found on the pages read [O]. Ministry Brands' DAF URL showed no DAF content.
- **Sponsor-side guidance:**
  - Endaoment says DAFs "can give to churches, provided they meet specific criteria". Donors search "for the church by name or EIN" [O] ([FAQ](https://faq.endaoment.org/donors/dafs/dafs-giving-to-churches)).
  - Fidelity's nonprofit FAQ suggests "adding the DAF Direct widget". It says non-EFT grants go by "checks mailed to the addresses listed on your organization's IRS Form 990" [O] ([FAQ](https://www.fidelitycharitable.org/nonprofits/nonprofits-frequently-asked-questions.html)).

## 3. Faith DAF sponsors: how they pay churches and synagogues (CSV FTH-12..FTH-19)

| Sponsor | What they say | Source |
|---|---|---|
| **NCF** (repo: $5.46bn) | "You can recommend a grant to any 501(c)(3) public charity, including churches." "We often distribute grants via ACH or electronic transfer when available." A wire costs "usually about $25". "Most charities are approved within a few business days" [O]. No applications are accepted. The **Single-Charity Fund** lets a ministry "Accept cash, stocks, or mutual funds" and "the net proceeds of business interests, real estate" [O] | [support](https://www.ncfgiving.com/support/); [charities](https://www.ncfgiving.com/charities/); [single-charity fund](https://www.ncfgiving.com/single-charity-fund-for-charities) |
| **The Signatry** | **Not read.** The help article now redirects to help.thesignatry.com, whose robots.txt disallows all paths [O] | [redirect notice](https://intercom.help/the-signatry/articles/6716462-granting-to-an-unlisted-recipient-charity) |
| **WaterStone** | The **Charity Advised Fund** is "a custom solution for churches and nonprofit organizations to receive and manage charitable gifts". Fees: 1.00% on the first $1M (minimum $395); 3% one-time on non-traditional assets. Site totals: "$1.5 Billion Given in Grants", "$4.6 Million+ Weekly in Grants", "15,000+ Charities Supported". **How grants are paid is not stated** [O] | [charity-advised fund](https://waterstone.org/charity-advised-fund/); [home](https://waterstone.org/) |
| **Jewish Communal Fund (NY)** | Staff "verify its tax-exempt status and official mailing address". "Grants are transmitted by check or electronic funds transfer (ACH or wire) at the discretion of JCF staff and are sent directly to the charity." The grant letter names the fundholder to thank. No grants for "memberships that have a nondeductible portion, tuition" [F]. **FY2023:** $907.9M granted, of which **Religion $81.4M** (9.0% [C]); "40% of our grant dollars went to Jewish organizations"; "nearly 80,000 individual grants"; "median grant amount of $750"; 99% of grants share fundholder contact details [F]. The top religious recipients by count are two Brooklyn congregations | [Policy Guide Aug 2024](https://jcfny.org/app/uploads/2024/08/Policy-Guide-Aug-2024_SP.pdf); [2023 Giving Report](https://jcfny.org/app/uploads/2024/04/2023-JCF-Giving-Report.pdf) |
| **JUF Chicago** | Staff check each recommendation for consistency with Federation purposes. Aggregate goal: 40–60% to JUF and its agencies. Minimum grant $100. No grants that discharge "a legally enforceable pledge" [F]. Payment method not stated | [Policies Dec 2023](https://www.juf.org/wp-content/uploads/2024/08/POLICIES_PROCEDURES_Dec_2023.pdf) |
| **Jewish Community Foundation LA** | "dues for synagogues and other religious institutions confer only a spiritual benefit" and "may be paid from a DAF". Religious groups not in the IRS database "may be eligible". ACH arrives in "24 to 48 hours"; checks "up to four weeks" [O] | [grantmaking guidelines](https://www.jewishfoundationla.org/grantmaking-guidelines/) |
| **LDS Philanthropies / Deseret Trust** | "Tithing and Fast Offering donations are not processed by Philanthropies"; local leaders take them on a slip or online form. The Church DAF is "administered by the Deseret Trust Company", and donors "may choose to give up to 60 percent to other charities" [O]. No official route for tithing from an outside DAF was found | [online donations FAQ](https://philanthropies.churchofjesuschrist.org/philanthropies/online-donations-faq.html); [DAF page](https://philanthropies.churchofjesuschrist.org/gift-planning/how-to-give/family-directed-giving-tools/donor-advised-fund-daf/) |
| **Catholic Community Foundation of Minnesota** | FYE 2025-06-30: "about $45 million" in grants across 4,630 grants (≈ $9,700 average [C]); $752M assets [O]. Payment method and parish split are not on the homepage. Other Catholic foundations were seen only as search extracts [S] | [ccf-mn.org](https://www.ccf-mn.org/) |

**Fidelity Charitable benchmark** (2026 Giving Report, CY2025) [F], [PDF](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf):

| Sector | Share of grant count | Share of grant dollars | Accounts granting | Implied average grant [C] |
|---|---|---|---|---|
| Religion | 27% | 13.1% | 49.7% | ≈ $2,815 |
| Education | 11.1% | 24.8% | 49.5% | ≈ $12,960 |
| All | — | $18.3B in total | — | $5,801 (reported) |

Also from the report: "67% of our grants are distributed via EFT"; "98% of grant recommendations were initiated digitally".

## 4. Explaining the gap: religion is 21% on donate pages but 13.6% of top-50 DAF dollars

The two repo figures measure different things:
- **21%** is the share of 14 scanned donate pages of top-300 religion recipients that show any DAF option (3 of 14; 0 DAFpay).
- **13.6%** is religion's share of all net Schedule I dollars across 174,195 recipients.

The evidence below explains why they diverge.

**E1. The scan sees parachurch ministries, not congregations** [C from repo CSVs]
- Religion has **$10.55bn across 55,993 recipients** (all ex university/hospital, FY2023–24). That is **32.1% of all recipients** and **27.0% of all lines**, but 13.6% of dollars.
- Average per recipient: **$188k for religion vs $444k for all sectors.** Average per line: **$65k vs $129k**.
- The 22 religion recipients in the top-300 sample hold **$1.58bn, 15.0% of religion dollars**. The sample as a whole holds 31.4% of all net dollars. The 14 scanned religion pages hold $0.84bn (7.9%).
- Those 22 are mostly parachurch ministries (Samaritan's Purse, Cru, Wycliffe, CRS, Focus on the Family, Salvation Army). Only 2–4 are congregations (LDS, Life.Church, Congregation Ohr Torah, possibly Amidei Zion of Bobov). None of the congregations was scanned: LDS had no donate link, Life.Church was unreachable, and the others had no website. Under the name rules of [b4026-06-church-daf-recipients.md](b4026-06-church-daf-recipients.md), two of the four are congregations (Life.Church, Ohr Torah); LDS is the denominational central and Amidei Zion of Bobov is unclassified. That study then read 14 pages of 50 seeded church-block congregations (10 giving pages, 4 homepages): none showed a DAF option (95% upper bound 21.5%), and a wave-35C re-read of 8 giving pages confirmed this [V wave 35C].
- **So the 21% says little about the congregations that receive most religion DAF dollars by count** [I].

**E2. Religion DAF money arrives as many small grants**
- Fidelity: 27% of grants and 13.1% of dollars, an implied ≈ $2,815 average [F/C].
- JCF NY: median grant $750 [F].
- Schedule I: religion's line and recipient shares (27% and 32%) are about twice its dollar share [C].
- **Inference:** small, repeat grants are more often set up by the donor in the sponsor portal than started from a church web page [I]. NCF, for example, publishes a recurring-schedule feature ([ncfgiving.com story](https://www.ncfgiving.com/stories/automate-your-giving-with-recurring-schedules-2/), search-listed [S]).
- Schedule I misses grants of $5,000 or less. Overall that costs about 2% of dollars (repo), but religion likely loses more lines than other sectors [I]. P-B41N15-02 would test this.

**E3. Faith sponsors pay churches without a donate-page step** [O/F]
- NCF, JCF NY and JCF LA all describe the same flow: the sponsor verifies the recipient's status and address, then pays by ACH or check, sending a letter that names the fundholder.
- Single-issue sponsors send **32.5% of their dollars to religion** [R]. Their grants therefore need no button on the church's site.
- These sponsors are largely absent from Chariot's partner lists [O]. A DAFpay widget on a church page would serve mainly donors at national sponsors [I]. In the top-50 church block, nationals send 74.2% of DAF-weighted dollars and the seven faith sponsors 22.1%, against the faith sponsors' 10.0% of all top-50 dollars (b4026-06) [V wave 35C].

**E4. Church giving platforms have no DAF rail** [O]
- Of the nine resolved church platforms, only Overflow offers in-checkout DAF grants. Pushpay's is "coming soon".
- A congregation using Pushpay, Tithely, Givelify, Kindrid, ACST/Vanco, Subsplash or Planning Center has no DAF method to switch on. At most it can add text instructions, as Subsplash advises.
- **Inference:** this probably keeps DAF options off congregation pages. The 14 congregation pages later read (b4026-06) showed Subsplash (5), Pushpay (3) and Planning Center (1), with no platform detected on 7, and none showed a DAF option [O] [V wave 35C]. It does not explain the 14 scanned pages: those are large ministries on Blackbaud, Fundraise Up, EveryAction and Stripe forms, not church platforms (repo `donate_platforms` field) [R/I].

**E5. Church legal status adds onboarding friction** [O → I]
- Churches need not apply for recognition or file a 990.
- Chariot runs alternative verification for unlisted houses of worship, and acceptance "depend[s] on the policies of the DAF provider".
- Fidelity mails non-EFT checks to the Form 990 address, which churches do not file.
- **Inference:** these frictions make self-serve DAF onboarding harder for congregations than for 990-filing charities.

**E6. Recurring religious obligations use church channels** [O/I]
- LDS tithing is handled by local leaders, not Philanthropies.
- Synagogue dues may be paid from some DAFs (JCF LA) but not where a membership carries a nondeductible benefit (JCF NY). Such payments follow the congregation's invoice or membership process, not its public donate page [I].

**Counter-evidence and limits**
- Religion's figure rests on 14 pages; any cell with n < 15 is indicative only (repo). The 95% interval for 3/14 is wide, roughly 8–48% (Wilson, [C]).
- Fidelity's religion share by count may partly reflect donor demographics, not payment mechanics.
- Platform pages show marketed features. A feature could exist without being on the pages read, which is why rows are "not_found", not "no".

## 5. Gaps and blocked items

- **Not fetched (robots or access):**
  - help.thesignatry.com (robots disallow-all);
  - support.tithe.ly / help.tithe.ly articles (403);
  - help.ministrybrands.com FAQ (403);
  - jewishdetroit.org policy PDF (under disallowed `/wp-content/`);
  - religionnews.com (robots 403);
  - catholiccommunityfoundation.org (robots no response);
  - overflow.co `/giving-methods/dafs` and `/churches` (404).
- **Search-only [S] claims, not relied on for conclusions:**
  - Ministry Brands stock routed to the Modern Philanthropy Foundation DAF;
  - Engiven 4% fee on Tithely;
  - Overflow "$4,000+" average DAF gift;
  - the year of the Thrivent–Chariot post (October 2025).
- **No platform publishes DAF volume.** No faith sponsor publishes the share of its grants paid to congregations by ACH versus check.
- **Unresolved:** "OneRealm" [U]; WaterStone's and the Signatry's payment methods; Catholic parish payment practice.

## 6. Source register

| ID | Source | Date | Used in | Label |
|---|---|---|---|---|
| FTH-S01 | [Pushpay digital giving](https://pushpay.com/digital-giving) | undated, © 2026 | §1, FTH-01 | O |
| FTH-S02 | [Pushpay Catholic donor development](https://pushpay.com/solutions/catholic/donor-development) | undated | §0 | O |
| FTH-S03 | [Subsplash: DAFs for churches](https://www.subsplash.com/blog/donor-advised-funds-for-churches) | 2026-10-01 | §2 | O |
| FTH-S04 | [Subsplash: new giving tools](https://subsplash.com/blog/new-subsplash-giving-tools-simplify-multiply-generosity) | 2025-11-19 | §1 | O |
| FTH-S05 | [Planning Center: nondeductible donations](https://www.planningcenter.com/blog/2024/09/track-nondeductible-donations-in-giving) | 2024-09-12 | §1 | O |
| FTH-S06 | [Overflow DAF launch](https://www.overflow.co/learn/overflow-introduces-new-way-to-give) | 2023-06-29 | §1 | O |
| FTH-S07 | [Overflow DAF page](https://www.overflow.co/overflow-giving/dafs) | undated | §1 | O |
| FTH-S08 | [Tithely home](https://get.tithe.ly/); [giving software](https://get.tithe.ly/product/church-giving-software) | undated | §1 | O |
| FTH-S09 | [Tithely crypto and stock blog](https://get.tithe.ly/blog/crypto-stock-giving-for-churches) | 2026-09-09 | §1 | O |
| FTH-S10 | [Tithely Engiven FAQ](https://support.tithe.ly/hc/en-us/articles/36234778126871) (403) | — | §5 | S |
| FTH-S11 | [Givelify home](https://www.givelify.com/); [giving](https://www.givelify.com/organizations/solutions/giving/); [blog](https://www.givelify.com/blog/preferred-church-giving-app/) | 2024-03-29 / undated | §1 | O |
| FTH-S12 | [Ministry Brands Kindrid](https://www.ministrybrands.com/kindrid) | undated | §1 | O |
| FTH-S13 | [Ministry Brands stock and crypto](https://www.ministrybrands.com/giving/stock-crypto) | undated | §1 | O |
| FTH-S14 | [Ministry Brands help FAQ](https://help.ministrybrands.com/hc/en-us/articles/20045162705947-Stock-Crypto-Donation-FAQ) (403) | — | §0, §5 | S |
| FTH-S15 | [Ministry Brands DAF explainer URL](https://www.ministrybrands.com/church-management/legacy-giving/donor-advised-funds) | undated | §2 | O |
| FTH-S16 | [Vanco + ACS Technologies release](https://www.vancopayments.com/newsroom/vanco-and-acs-technologies-unite-to-deliver-more-connected-services-and-solutions-for-churches) | 2025-12-03 | §1 | O |
| FTH-S17 | [ACST Realm eGiving](https://www.acstechnologies.com/realm/tools/giving/) | undated | §1 | O |
| FTH-S18 | [Chariot help, full text](https://help.givechariot.com/llms-full.txt) | read 2026-11-15 | §1, §4 E5 | O |
| FTH-S19 | [Chariot: Thrivent Charitable on DAFpay](https://www.givechariot.com/post/thrivent-charitable-on-dafpay-in-new-partnership-with-chariot) | "Oct 7" (2025 per search) | §0 | O/S |
| FTH-S20 | [NCF support / grantmaking](https://www.ncfgiving.com/support/) | undated | §3 | O |
| FTH-S21 | [NCF charities](https://www.ncfgiving.com/charities/) | undated | §3 | O |
| FTH-S22 | [NCF Single-Charity Fund](https://www.ncfgiving.com/single-charity-fund-for-charities) | undated | §3 | O |
| FTH-S23 | [WaterStone home](https://waterstone.org/) | undated | §3 | O |
| FTH-S24 | [WaterStone Charity Advised Fund](https://waterstone.org/charity-advised-fund/) | undated | §3 | O |
| FTH-S25 | [JCF NY Policy Guide](https://jcfny.org/app/uploads/2024/08/Policy-Guide-Aug-2024_SP.pdf) | 2024-08 | §3 | F |
| FTH-S26 | [JCF NY 2023 Giving Report](https://jcfny.org/app/uploads/2024/04/2023-JCF-Giving-Report.pdf) | FY2023 | §3, §4 E2 | F |
| FTH-S27 | [JCF LA grantmaking guidelines](https://www.jewishfoundationla.org/grantmaking-guidelines/) | © 2001–2026 | §3 | O |
| FTH-S28 | [JUF policies](https://www.juf.org/wp-content/uploads/2024/08/POLICIES_PROCEDURES_Dec_2023.pdf) | 2023-12 | §3 | F |
| FTH-S29 | [LDS Philanthropies DAF](https://philanthropies.churchofjesuschrist.org/gift-planning/how-to-give/family-directed-giving-tools/donor-advised-fund-daf/) | undated | §3 | O |
| FTH-S30 | [LDS online donations FAQ](https://philanthropies.churchofjesuschrist.org/philanthropies/online-donations-faq.html) | undated | §3, §4 E6 | O |
| FTH-S31 | [Fidelity Charitable 2026 Giving Report](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf) | 2026 (CY2025) | §3, §4 E2 | F |
| FTH-S32 | [Fidelity nonprofit FAQ](https://www.fidelitycharitable.org/nonprofits/nonprofits-frequently-asked-questions.html) | undated | §2, §4 E5 | O |
| FTH-S33 | [CCF Minnesota](https://www.ccf-mn.org/) | FYE 2025-06-30 | §3 | O |
| FTH-S34 | [Endaoment: DAFs giving to churches](https://faq.endaoment.org/donors/dafs/dafs-giving-to-churches) | undated | §2 | O |
| FTH-S35 | [The Giving Block faith page](https://thegivingblock.com/faith-based-fundraising/) | undated | CSV FTH-23 | O |
| FTH-S36 | [Engiven ministries](https://engiven.com/ministries) | undated | CSV FTH-22 | O |
| FTH-R1 | `nonprofit-donate-page-daf-scan-2026.csv` (religion rows) | 2026-11-15 | §4 E1 | R/C |
| FTH-R2 | `daf-grant-recipient-sectors-top50.csv` (all_ex_university_hospital, 2023–2024, schedule_i) | 2026-11-15 | §4 E1–E2 | R/C |
| FTH-R3 | `faith-sponsor-platforms-2026.csv`; queue-batch33 §3 | 2026-11-15 | §3 | R |
| FTH-R4 | direction-noncash-gift-infrastructure.md §2.2–2.3 (Engiven, Overflow) | 2026-11-15 | §1 | R |

## 7. Data dictionary: `faith-giving-platform-daf-support-2026.csv`

| Column | Meaning |
|---|---|
| `row_id` | FTH-NN |
| `entity` | Platform, sponsor or rail as named on its site |
| `parent_or_owner` | Owner or parent as stated on the page or in the repo |
| `segment` | `church_giving_platform`, `faith_daf_sponsor`, `national_daf_sponsor_benchmark`, `rail`, `noncash_processor` |
| `in_checkout_daf_grant` | `yes`, `announced_not_live`, `no (recording only)`, `not_found` (nothing on the pages read; not proof of absence), `unresolved`, `n/a` |
| `daf_rail_named` | Rail named by the entity (e.g. Chariot) or `none` |
| `daf_gift_recording` | Whether the platform records DAF gifts received off-platform |
| `stock_giving`, `crypto_giving` | As stated on the pages read |
| `noncash_partner` | Engiven, The Giving Block, in-house, etc. |
| `congregation_daf_guidance` | What congregations are told, or sponsor recipient rules (quoted or paraphrased) |
| `grant_payment_method_to_congregation` | Sponsor rows: ACH, check or wire as stated |
| `published_daf_volume_stat` | DAF-specific volume figures, verbatim; `none` if absent |
| `published_scale_stat` | General scale figures (not DAF-specific) |
| `evidence_url`, `evidence_date`, `accessed` | Primary page, its date (or `undated`), and the fetch date |
| `label` | O / F / S / U as in the header |
| `confidence` | high / medium / low |
| `notes` | Extra URLs, caveats and computations ([C]) |
