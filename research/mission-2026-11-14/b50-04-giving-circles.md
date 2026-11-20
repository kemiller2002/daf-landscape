# b50-04: Giving circles and collective giving on DAF and fund infrastructure

TASKID b50-04. Retrieved 2026-11-20. Evidence is from 2021 onwards unless a row is flagged. Only organisations and products are recorded. No circle member is named, even where a source page names one. The companion robots log does carry URL slugs that contain individuals’ names: a 2021 Maine CF donor story (file line 56) and a CNY CF fund named after a person (file lines 62–64). Whether to truncate those URLs is an owner decision. [V wave 50B]

**Outputs**
- `data/mission-2026-11-14/giving-circles-2026-11-20.csv` has 72 rows: 41 provider rows and 31 sizing rows.
- `data/mission-2026-11-14/giving-circles-robots-log-2026-11-20.csv` is the robots and fetch log, 145 rows.
- `data/mission-2026-11-14/queue-proposals-b50-04.csv` holds 6 proposals.
- `scripts/mission_b50_04_giving_circles.py` draws the sample, checks robots.txt, scans sitemaps and fetches pages.
- `scripts/mission_b50_04_build_csv.py` builds the CSV, checks quotes verbatim against the cached text and computes the summary counts.

## Summary

1. **Where circle money sits.** Johnson Center and Philanthropy Together ran a survey in 2023 (543 groups), published in 2024 and 2026. Asked which institutional host or fiscal agent they use, groups answered:

   | Host or fiscal agent | Share of groups |
   |---|---|
   | Community foundation | 42% |
   | Technology platform such as Grapevine | 24% |
   | No third party | 24% |
   | Nonprofit organisation | 7% |
   | Women's fund | 3% |

   The same data say 45% were "hosted by either a community foundation or women's fund, which managed donations and disbursements" (GS-006 to GS-011). Roughly three-quarters of circles (42 + 24 + 7 + 3 = 76%) therefore use a third-party host or platform, and community foundations are the largest single host. For the 24% platform share, the money sits in a 501(c)(3) only where the platform pools through one, as Grapevine does; the survey option also named GoFundMe. [V wave 50B]
2. **Own 501(c)(3) is not separately quantified.** The 24% "don't use a third party" bucket mixes incorporated circles with informal groups that pool money through a member. The reports describe incorporation only qualitatively, so no share is given for circles that hold their own 501(c)(3).
3. **The legal vehicle varies, and pages rarely state it.**
   - Two sources say the circle fund is a DAF: Thrivent Charitable's giving-circle fund (GC-036) and the African American Legacy Fund at The Indianapolis Foundation / CICF (GC-032).
   - Two CF term sheets describe a non-endowed or endowed component fund that the group advises: Triangle (GC-034) and Idaho (GC-030).
   - Minneapolis Foundation's RMD Giving Circle pools IRA gifts. If those are qualified charitable distributions, the fund cannot be a DAF (IRC 408(d)(8)(B)). This is an inference.
   - 31 of the 41 provider rows say nothing about the vehicle.
4. **Few sponsors publish explicit giving-circle fund products with terms.**
   - In a systematic 1-in-3 sample of the top-100 community foundations (33 CFs), 1 published circle-fund terms (Idaho).
   - 12 host named circles without publishing fund terms.
   - 1 runs committee-advised affinity funds, 2 run DAF-holder co-funding programmes, 1 promotes an independent circle and 1 shows a circle converted to a field-of-interest fund.
   - 11 had nothing findable, and 4 were blocked.

   One purposive supplement from the repo CF list, Triangle CF, publishes the clearest term sheet: a $10,000 non-endowed fund and a 1% fee with a $300 minimum.
5. **National DAF sponsors mostly do not offer a pooled circle product.**
   - Fidelity Charitable offers guidance only. It is also a funder of Philanthropy Together through its Catalyst Fund.
   - Daffy's "Giving circle" is a campaign option that sends gifts to a shared charity list. No jointly advised pooled fund was found.
   - Groundswell offers employer campaigns only.
   - Thrivent Charitable is the one national sponsor found selling a giving circle "in the form of a donor-advised fund". It allows $200 per person, but it does not state the fund-level minimum or the fee.
6. **Platforms.** Grapevine pools circle money through its own 501(c)(3), Grapevine Giving Foundation (EIN 87-2389502). It reports "$60 million+" granted since 2020 and "100,000+" members. It charges no platform fee on online card or bank gifts, but "a 3% platform fee" on off-platform gifts, which explicitly include "Donor Advised Fund grants". Its 990 Schedule D reports **one** DAF in each of FY2022 to FY2025, with DAF contributions of $4.78m, $10.13m, $9.92m and $9.16m (GS-016 to GS-031).
7. **Sizing.** Between 2017 and 2023, nearly 4,000 collective giving groups and about 370,000 participants gave more than $3.1bn (In Abundance, 2024). No 2021+ source splits the dollars by host type. Group counts by host are therefore only illustrative: about 1,680 CF-hosted and about 960 platform-hosted groups, computed as 42% and 24% of 4,000 on the assumption that survey shares generalise. The 4,000 is a cumulative 2017–2023 count of groups, not the number active at one date, so these figures are cumulative too. [V wave 50B]

## 1. Method

1. **Research (Q1, Q3).** Johnson Center for Philanthropy (GVSU) reports by the Collective Giving Research Group, with Philanthropy Together:
   - *In Abundance* (April 2024; 2023 survey)
   - *Patterns in the Tapestry* (December 2024)
   - *Rooted in Community: The Infrastructure Powering Collective Giving* (February 2026)

   All were fetched as PDFs after a robots check, converted with `pdftotext`, and grepped for host, fiscal-agent and platform terms. Philanthropy Together's own site could not be used: its robots.txt returns HTTP 403, which the rules treat as disallowed.
2. **CF sample (Q2).**
   - **Sample frame.** I took the repo CF list `data/mission-2026-11-14/cf-vendor-map-by-ein-v2.csv`, which carries homepages, and ranked it by FY2024 DAF assets. From the top 100 I kept every third rank: 1, 4, 7, …, 100. CICF's homepage appears twice (ranks 43 and 97), so it was de-duplicated, leaving **33 CFs**. Command: `python3 -I scripts/mission_b50_04_giving_circles.py . sample OUT`.
   - **Per-CF scan.**
     - The script fetched each CF's robots.txt and checked it against `*`, our UA, ClaudeBot, anthropic-ai, Claude-User, Claude-Web and Claude-SearchBot, with wildcard and `$` support and longest-match rules.
     - A robots.txt that was unreachable or returned anything other than 200 or 404 was treated as disallowed.
     - The script then crawled up to 25 sitemaps per site and took any homepage links matching `circle|collective-giving|giving-together`.
     - It fetched up to 6 candidate pages per site, ranking hub and product pages ahead of stories, blogs and events in the final version.
   - **Gap-filling.** Where the scan found nothing, I ran site-restricted web searches. I treated search results only as pointers and fetched every page I used through the same robots-checked fetcher.
   - **Supplements.** Two CFs from the repo list were added purposively after a general search: Triangle (rank 59) and Sacramento (rank 81, blocked).
3. **National sponsors and platforms (Q2).** Fidelity Charitable, Daffy, Groundswell, Thrivent Charitable, Grapevine and Global Impact's Growfund. Growfund was checked only through repo 990 reads.
4. **Quotes.** `mission_b50_04_build_csv.py` checks every quote in the CSV verbatim against the cached page text, with whitespace normalised. For PDFs it uses non-layout `pdftotext` output. Result: 0 missing quotes. Fragments joined by " ... " are checked one at a time.
5. **990 figures.** Grapevine Giving Foundation's Schedule D values come from the repo harvest `form990-returns-schedule-d-harvest-full.csv`, which uses IRS e-file XML via the GivingTuesday mirror. They were selected by EIN in the script, not retyped.

## 2. How giving circles hold money (Q1)

| Structure | Evidence (2021+) | Share | Source |
|---|---|---|---|
| Community foundation fund (DAF, component, endowed or non-endowed, field-of-interest, affinity) | "Forty-two percent of giving circles are hosted by community foundations" | 42% of groups | Rooted in Community (2026), Fig. 2; GS-006 |
| Women's fund | "or women's funds (3%)" | 3% | GS-009 |
| Technology platform (Grapevine; its 501(c)(3) pools and grants) | "followed by technology platforms such as Grapevine (24%)" | 24% | GS-007 |
| Nonprofit host or fiscal sponsor (incl. nonprofit-led "host-supporting" groups) | "nonprofit organizations (7%)" | 7% | GS-008 |
| No fiscal sponsor: own 501(c)(3), or informal (member gives on the group's behalf) | "While 24% of groups operate independently without a fiscal sponsor" | 24% | GS-010 |
| Host manages money (CF + women's fund) | "45% of collective giving groups were hosted by either a community foundation or women's fund, which managed donations and disbursements" | 45% | In Abundance p.10; GS-011 |

**How the survey asked the question.** The question (In Abundance appendix, Q36: "What type of organization serves as the institutional host or fiscal agent?") offered six options:
- "We don't use a third party - we give directly to the group or to a member who makes the donation"
- Technology platform (e.g., Grapevine, GoFundMe)
- Community foundation
- Nonprofit supporting organization
- Women's fund
- Other

There is no separate "own 501(c)(3)" option. The typology figure places governance on a spectrum from "Informal / Unincorporated" to "Formal / Incorporated 501(c)(3)" without a share, and *Patterns in the Tapestry* says only that some groups "are incorporated as independent 501(c)(3)s".

**Why hosts matter.** Rooted in Community says hosts handle "the compliance and administrative requirements that allow grassroots collective giving groups to operate without forming their own 501(c)(3)". It also reports that 47% of groups have paid staff support, "most often provided by host organizations".

**Inconsistency in affiliation figures.** In Abundance reports that "52% had a host organization, 22% were part of a network, and 7% were affiliated with a nonprofit". Rooted in Community reanalyses the same survey as "49% through a host organization … 24% through a network, and 13% through a nonprofit sponsor". Both are recorded as published, and only the Rooted in Community host-type shares are used in the CSV.

**Platform history.** Grapevine launched circles in March 2020. Until its own foundation was formed, it "worked with a 501.c.3 nonprofit fiscal sponsor to enable it to pool charitable donations for giving circles". The Grapevine Giving Foundation was announced on 2022-11-09.

## 3. Results: sponsors and products (Q2)

### 3.1 National sponsors and platforms

| Entity | Class | What exists | Verbatim terms |
|---|---|---|---|
| Thrivent Charitable | explicit circle fund product (DAF) | Giving-circle fund for groups | Vehicle: "in the form of a donor-advised fund". Minimum: "can be established with as little as $200/person … (giving circle fund minimum applies.)". Advice: fund sent "to the chair/fund advisor for signing". Grants: "As a group, members make decisions on what organizations to grant to". No fee or fund-level minimum is stated. |
| Fidelity Charitable | guidance only | Article and webinar; no group account | "Philanthropy Together is a grantee of the Fidelity Charitable Catalyst Fund." |
| Daffy | campaign feature | Campaigns with a "Giving circle" option (2025-08-28) | "Giving circle: Invite family, friends, or coworkers to rally around a shared list of nonprofits." Campaigns "can include up to 15 charities". No pooled joint fund and no "Daffy groups" product was found. |
| Groundswell | campaign feature (employer) | Employer campaigns and employee fundraisers | "Rally your workforce around specific causes or disaster relief efforts with time-bound giving campaigns." No circle product. |
| Grapevine / Grapevine Giving Foundation | platform fiscal host | Circles pool through its 501(c)(3) | "Grapevine does not charge platform fees for online donations…". Off-platform: "for off-platform donations such as checks, Donor Advised Fund grants, wire transfers, and ACH payments, Grapevine charges a 3% platform fee". Cards: "2.2% + $0.30 (3.5% for AmEx; +1.5% for non-US cards)". A second help page says "We don't charge your circle or your nonprofit partners any platform fees or administrative fees" and prices non-US cards at 3.2% + 30¢. The two pages conflict. |
| Global Impact (Growfund) | historical | "Growfund for Giving Circles" launched before 2021 | Repo 990 read: DAF line 6 "No" in FY2025; Growfund not described in FY2025 Part III (`tier-b-daf-exit-reasons.csv`). No current terms. |

### 3.2 Community foundations

Results for the systematic sample of 33 CFs, computed by the build script:

| offering_class | CFs | Examples (CSV row) |
|---|---|---|
| explicit_gc_fund_product | 1 | Idaho CF: Collective Giving Handbook 2026 (GC-030) |
| hosted_named_circles | 12 | Memphis GiVE 365 (GC-006); Minneapolis (GC-007); SPMCF Power of Possible (GC-008); North Texas WORTH (GC-013); Richmond (GC-014); Coastal LAAGC (GC-023); Lancaster LGBTQ+ Giving Circle Fund (GC-029); CICF African American Legacy Fund (GC-032); NoCo giving groups (GC-033); CFNJ Impact100 Essex release (GC-005); GNOF EPNO tag (GC-015); Buffalo 21st Century Fund (GC-018, page content not readable) |
| committee_advised_pooled | 1 | Cleveland affinity funds (GC-011) |
| daf_cofunding_program | 2 | Maine "Giving Together" (GC-016); Vermont "Giving Together" (GC-025) |
| supports_independent_circle | 1 | Louisville / Impact 100 Louisville (GC-012) |
| historical | 1 | CNY Future Fund, now a field-of-interest fund (GC-022) |
| none_found | 11 | SVCF, GKC, Oregon CF, GiveWell CF, CFCV, Charlottesville, SD, Armstrong, Toledo, Salina, Lincoln |
| blocked | 4 | Atlanta (robots unreachable); Miami and Blue Grass (robots 403); Pittsburgh (page 403 although robots allow) |

Supplement: Triangle CF is coded explicit_gc_fund_product (GC-034); Sacramento is blocked (GC-035).

Validator note: the counts reproduce, but three of the 12 hosted_named_circles rows rest on thin evidence. Buffalo (GC-018) has no readable page text, and its row says the search snippets were not used as evidence, so its class is unverified. GNOF (GC-015) is a tag-page listing only. North Texas (GC-013) is an undated narrative citing 2015 and 2018. [V wave 50B]

**Verbatim terms where published.**

| Sponsor | Minimum | Fee | Who advises / how grants are recommended |
|---|---|---|---|
| Triangle CF (2026-01 one-pager) | "make an irrevocable contribution of $10,000 to open a non-endowed fund" … "Giving Circles with a balance of less than $10,000 are considered on a case-by-case basis in consultation with Foundation staff." Online gifts: "minimum online contribution of $100". Members: "Contribution amounts can vary, from $10 to $25,000 or more – Giving Circle organizers decide" | "Annual administrative fee of 1% of fund balance or a minimum of $300 per year" | "Fund advisors recommend grants and they are processed through the Foundation" |
| Idaho CF (Handbook 2026) | Non-endowed: "Minimum to establish fund: $25,000" (endowed also $25,000; scholarship $50,000) | Non-endowed: "Typically, 2.0% of average daily fund balance with a minimum fee of $500, whichever is greater, plus investment fee of approximately .2%" and "Some funds have fees on contributions (gift fees) between 1%-10%". Endowed: "Typically, 1.0%-2.0% … minimum fee of $500". Fees are negotiated: "a mutually agreed upon fee schedule" | "This relationship allows the Partner to be advisory in nature and ICF to hold the legal status." "Partner will make all recommendations for grant distribution in accordance with their fund agreement and ICF Grant Making Policy." |
| Cleveland Foundation (affinity funds) | "There is no giving minimum and donations are pooled." | not stated | "committees are comprised of at least five members of that community and its allies"; "committee-advised grantmaking" |
| Minneapolis Foundation | not stated ("Each giving circle decides together how it will raise money") | not stated | "The Minneapolis Foundation can provide grantmaking advice, carries out the group's funding decisions, and ensures that all grant recipients are qualified public charities." |
| CICF / Indianapolis Foundation (AALF) | not stated | not stated | "endowed donor-advised fund"; "empowers a committee of donors to design a grant-making process and make charitable distributions" |
| Coastal CF (LAAGC) | Founding donor "$5,000 or more" to the endowment | not stated | Dues "$500 annual Community Membership and a $250 Young Professional Membership"; "Members help shape how resources are invested" |
| CF of Greater Memphis (GiVE 365) | "pools $365 per member each year" | not stated | members "select an annual theme, and decide together which nonprofit projects to fund" |
| NoCo Foundation (Loveland Generations) | "Diamond ($1,000); Gold ($750); and Silver ($500)" | not stated | "solicits grant proposals once a year" |
| North Texas CF (WORTH) | "Each membership of $250 is placed in the WORTH Endowment Fund" | not stated | membership matched by four private funders. Page undated, content refers to 2015 and 2018 |
| CFNJ (Impact100 Essex release, 2025-05-08) | "gifts of $1,150 per member, per year" | not stated | "chosen from among four finalists by Impact100 Essex members" |

### 3.3 Vehicle: DAF or not?

- **Stated DAF:** Thrivent Charitable (GC-036) and CICF's African American Legacy Fund (GC-032).
- **Stated non-DAF fund types:** Triangle uses a "non-endowed fund". Idaho offers endowed, non-endowed, administrative, special-project and scholarship funds, with the circle as advisory committee. CNY's former circle became a "field-of-interest fund". Cleveland uses "affinity funds" with Foundation endowments.
- **Inferred non-DAF:** Minneapolis' RMD Giving Circle pools IRA gifts. A QCD cannot be made to a DAF, so the fund is presumably a non-DAF fund. The page does not name the fund type. Queue item P-B5004-02 follows this up.
- **Two different "collective DAF" models.** Maine's and Vermont's "Giving Together" and Richmond's quarterly needs programme are a different pattern. Individual DAF holders co-fund a shared slate from their own DAFs, and no group fund exists.

### 3.4 Platform channel in DAF filings

Grapevine Giving Foundation's Schedule D Part I, from the repo harvest:

| FY | DAF count | Contributions | Grants | EOY value |
|---|---|---|---|---|
| 2022 (amended return) | 1 | $4,776,952 | $2,718,593 | $2,058,359 |
| 2023 | 1 | $10,131,877 | $8,766,981 | $3,377,079 |
| 2024 | 1 | $9,924,817 | $8,102,321 | blank (DAFRC imputed $4,508,877) |
| 2025 | 1 | $9,156,802 | $8,484,172 | $672,630 |

Whatever the legal reading, circle money held by the platform flows through lines that DAF market statistics count, while the account count stays at 1. The corrected DAFRC panel uses the filed FY2023 grants ($8,766,981, rule R1, replacing an imputed $2,656,657). For FY2024 it keeps DAFRC’s imputed values: contributions $14,111,183 and grants $3,356,869, against filed $9,924,817 and $8,102,321. DAFRC classes the foundation as National, Donation Processor. [V wave 50B] Proposal P-B5004-03 asks for this to be reconciled.

## 4. Sizing (Q3)

| Metric | Value | Basis |
|---|---|---|
| Collective giving groups, 2017–2023 | nearly 4,000 | In Abundance (GS-001) |
| Participants | approximately 370,000 | GS-002 |
| Dollars donated, 2017–2023 | more than $3.1bn | GS-003 |
| Prior landscape (2017 study, pre-2021, context only) | 1,600 groups; $1.29bn; 150,000+ people | GS-004 |
| Survey base | 543 group responses; 1,406 member responses | GS-005 |
| Grapevine (platform, live page) | "$60,000,000" granted since 2020; "100,000+" members; 8,600 nonprofits | GS-013, GS-014 |
| Grapevine Giving Foundation page (undated) | "over 84,000 members across 1,100 Giving Circles" | GS-015 |

**Computed by the build script.** These are illustrative only, not estimates of record.
- Groups by host, taking the survey shares × 4,000 groups:
  - CF ≈ 1,680
  - platform ≈ 960
  - no third party ≈ 960
  - nonprofit ≈ 280
  - women's fund ≈ 120

  This assumes the 543 responding groups represent all groups. The survey was disseminated through hosts and networks, so hosted groups may be over-represented.
- Average dollars per group over 2017–2023: $775,000. Average annual flow if spread evenly over 7 years: about $443m a year.
- Grapevine Giving Foundation's FY2023 DAF contributions ($10.13m) equal 2.29% of that average annual flow. The bases differ: one is a single year of platform contributions, the other a 7-year cumulative average.

**What cannot be sized.**
- Dollars by host type, because no published cross-tab exists.
- The number of CF "giving circle funds" nationally.
- Circle dollars held in DAF form versus other fund types.

## 5. Limits

- **Robots and server blocks.**
  - Philanthropy Together (robots 403), Atlanta CF (robots unreachable), Miami Foundation and Blue Grass CF (robots 403), and Sacramento Region CF (robots 403) were not read.
  - Pittsburgh Foundation and the Council on Foundations FAQ allowed all agents in robots.txt but returned HTTP 403 to the page.
  - No host disallowed a Claude agent specifically.
- **Discovery gaps.** A sitemap scan misses pages not listed in sitemaps, PDFs linked only from pages, and products named "giving group", "affinity fund" or "donor circle". Site-restricted web search caught some of these. "none_found" means nothing was found, not that nothing exists.
- **Undated pages.** Many CF pages carry no date, so the dates recorded are retrieval dates. North Texas WORTH content refers to 2015 and 2018, and Louisville's Impact 100 page refers to a 2021 grant cycle. Both are flagged in `source_date`.
- **Unreadable page.** Buffalo's 21st Century Fund page returned HTTP 200 but its static HTML carries no programme text.
- **Research base.** All 2021+ quantitative evidence comes from one 2023 survey (In Abundance and its 2024 and 2026 reanalyses). The two reports differ slightly on affiliation shares (§2).
- **Daffy.** Only public marketing and help pages were read. The flow of campaign gifts is as described there, not tested.
- **Thrivent.** The fund-level minimum and fee are not published on the pages read.

## 6. Data dictionary: `giving-circles-2026-11-20.csv`

| Column | Meaning |
|---|---|
| row_id | GC-nnn = provider row; GS-nnn = sizing metric |
| record_type | `provider` or `sizing_metric` |
| entity, ein | Organisation as named in the repo CF list or on the source. EIN is taken from the repo list or stated on the source page |
| entity_type | community_foundation / national_sponsor / platform |
| sample_basis | `systematic_1in3_top100_cf (cf-vendor-map-by-ein-v2.csv)`, `purposive_supplement (...)` or blank (national) |
| cf_rank_fy2024, fy2024_daf_assets_usd | Rank and FY2024 DAF assets from the repo CF list |
| offering_class | `explicit_gc_fund_product`, `hosted_named_circles`, `committee_advised_pooled`, `daf_cofunding_program`, `supports_independent_circle`, `campaign_feature`, `platform_fiscal_host`, `guidance_only`, `none_found`, `blocked` or `historical` (definitions in the script header) |
| product_or_program | Product or programme name (organisation-level; no members) |
| vehicle_stated | Legal or fund form as stated on the source, else "not stated" |
| minimum_quote, fee_quote, who_advises_quote, grant_process_quote, member_contribution_quote, other_quote | Verbatim quotes. " ... " separates non-adjacent fragments. In sizing rows, other_quote holds the quote that supports `value` |
| metric, value, unit, period | Sizing rows only. `value` is the number in the quote, written without separators |
| source_url | Primary URL (or repo file for GC-041). In 990 rows, the ProPublica filing page; the XML URL is in the repo harvest |
| source_date | Date on the source, or "live page" / "undated" |
| robots | robots.txt result from the fetch log, or the sitemap-scan result plus sitemaps read |
| fetch_status | HTTP status of the page fetch, `blocked_robots`, or `sitemap scan only` |
| quote_check | `verified k/n` against cached text; `computed from <repo file>`; `no quotes`; `no page (sitemap scan / search only)` |
| retrieved | 2026-11-20 (or "repo harvest") |
| notes | Caveats; secondary pages used |

Companion log `giving-circles-robots-log-2026-11-20.csv` has these columns: checked, scope (page or sitemap scan), url, robots_result, http_status, bytes.

## 7. Source register (primary URLs)

| # | Source | URL | Date | Robots |
|---|---|---|---|---|
| 1 | Johnson Center / Philanthropy Together, *In Abundance* | https://johnsoncenter.org/wp-content/uploads/2024/04/in-abundance-an-analysis-of-the-thriving-landscape-of-collective-giving-in-the-u-s.pdf | 2024-04 | allowed |
| 2 | Johnson Center, *Patterns in the Tapestry* | https://johnsoncenter.org/wp-content/uploads/2024/12/patterns-in-the-tapestry-a-typology-of-collective-giving-groups.pdf | 2024-12 | allowed |
| 3 | Johnson Center, *Rooted in Community* | https://johnsoncenter.org/wp-content/uploads/2026/02/rooted-in-community-the-infrastructure-powering-collective-giving.pdf | 2026-02 | allowed |
| 4 | Johnson Center, US Collective Giving Research Initiative | https://johnsoncenter.org/us-collective-giving-research-initiative/ | live | allowed |
| 5 | Grapevine fees | https://help.grapevine.org/fees-for-using-grapevine | live | allowed |
| 6 | Grapevine "Is Grapevine free" | https://help.grapevine.org/is-grapevine-free | live | allowed |
| 7 | Grapevine Giving Foundation | https://www.grapevine.org/about-us/grapevine-giving-foundation | undated | allowed |
| 8 | Grapevine foundation announcement | https://www.grapevine.org/blog/announcing-our-newest-way-to-amplify-giving-the-grapevine-giving-foundation | 2022-11-09 | allowed |
| 9 | Grapevine about / home | https://www.grapevine.org/about ; https://www.grapevine.org/ | live | allowed |
| 10 | Grapevine Global Giving Circle Directory | https://www.grapevine.org/global-giving-circle-directory | live | allowed |
| 11 | Daffy campaigns update | https://www.daffy.org/resources/daffy-campaigns-updates | 2025-08-28 | allowed |
| 12 | Daffy help: campaigns; matching | https://help.daffy.org/en/articles/8538853-what-is-a-daffy-campaign ; https://help.daffy.org/en/articles/8545821-how-does-campaign-matching-work | live | allowed |
| 13 | Fidelity Charitable, The power of giving circles | https://www.fidelitycharitable.org/articles/the-power-of-giving-circles.html | live | allowed |
| 14 | Groundswell giving product; FAQ | https://www.groundswell.io/products/giving ; https://www.groundswell.io/faq | live | allowed |
| 15 | Thrivent Charitable giving circles | https://thriventcharitable.thrivent.com/steps-giving/givingcircles ; https://thriventcharitable.thrivent.com/giving/giving-circles | live | allowed |
| 16 | Triangle CF giving-circle one-pager | https://trianglecf.org/wp-content/uploads/2026/01/Giving-Circles-one-pager-1.pdf | 2026-01 | allowed |
| 17 | Idaho CF Collective Giving Handbook 2026 | https://www.idahocf.org/docs/Collective-Giving-Handbook-2026.pdf | 2026 | allowed |
| 18 | Minneapolis Foundation: giving circles; collective giving; RMD circle story | https://www.minneapolisfoundation.org/giving-circles/ ; https://www.minneapolisfoundation.org/collective-giving/ ; https://www.minneapolisfoundation.org/stories/giving-circles/collective-giving-powered-by-iras/ | live / 2026 | allowed |
| 19 | Saint Paul & Minnesota Foundation, Power of Possible | https://spmcf.org/donors/ways-to-give/pop-giving-circle | live | no robots (404) |
| 20 | CF of Greater Memphis, GiVE 365 | https://cfgm.org/get-involved/give-365/ | live | allowed |
| 21 | CFNJ, Impact100 Essex release | https://cfnj.org/news/impact100-essex-awards-100000-grant-to-perinatal-health-equity-initiative/ | 2025-05-08 | allowed |
| 22 | Cleveland Foundation affinity funds | https://www.clevelandfoundation.org/philanthropy-giving/ways-to-give/affinity-funds/overview | live | allowed |
| 23 | CF of Louisville, Impact 100 | https://www.cflouisville.org/impact-100/ | undated (2021 cycle) | allowed |
| 24 | North Texas CF, collective giving | https://northtexascf.org/collective-giving/ | undated | allowed |
| 25 | CF for a Greater Richmond, collective giving | https://cfrichmond.org/give/services/collective-giving/ | live | allowed |
| 26 | Greater New Orleans Foundation, collective-giving tag | https://www.gnof.org/tag/collective-giving/ | live | allowed |
| 27 | Maine CF, Giving Together | https://www.mainecf.org/2022/07/giving-together-for-good/ | 2022-07 | allowed |
| 28 | Vermont CF, Giving Together | https://vermontcf.org/your-impact/giving-together/ | live | allowed |
| 29 | CNY CF, Future Fund | https://cnycf.org/funds/future-fund-of-central-new-york/ | live | allowed |
| 30 | Coastal CF, LAAGC | https://coastalcommunityfoundation.org/special-initiatives/lowcountry-african-american-giving-circle/ | live | allowed |
| 31 | Lancaster County CF, LGBTQ+ Giving Circle | https://www.lancfound.org/lgbtq-giving-circle/ | live | allowed |
| 32 | CICF, African American Legacy Fund | https://www.cicf.org/african-american-legacy-fund-of-indianapolis/ | live | allowed |
| 33 | NoCo Foundation, collaborative giving | https://nocofoundation.org/donors/collaborative-giving | live (cites 2024-06-30) | allowed |
| 34 | CF for Greater Buffalo, 21st Century Fund | https://www.cfgb.org/community-change/initiatives/21st-century-fund/ | live (no static text) | robots returned HTML |
| 35 | Grapevine Giving Foundation 990s (via repo harvest) | https://projects.propublica.org/nonprofits/organizations/872389502/202413199349309371/full (FY2023; other years in CSV) | FY2022–FY2025 | n/a (repo) |
| 36 | Blocked / not read | philanthropytogether.org (robots 403); sacregcf.org/fees (robots 403); cfgreateratlanta.org (robots unreachable); miamifoundation.org, bgcf.org (robots 403); pittsburghfoundation.org/giving-circles and cof.org FAQ (page 403) | — | logged |

The full list of URLs checked is in `data/mission-2026-11-14/giving-circles-robots-log-2026-11-20.csv`. Cached page text is kept only in the session scratchpad and is not committed.

## 8. Reproduce

```
python3 -I scripts/mission_b50_04_giving_circles.py . sample   <CACHE>
python3 -I scripts/mission_b50_04_giving_circles.py . discover <CACHE> [ranks...]
python3 -I scripts/mission_b50_04_giving_circles.py . fetch    <CACHE> URL [URL...]
for f in <CACHE>/raw/*.pdf; do pdftotext "$f" <CACHE>/pdfraw/$(basename "$f" .pdf).txt; done
python3 -I scripts/mission_b50_04_build_csv.py . <CACHE>
```
