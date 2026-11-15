# Direction: donor-facing feature census (P-NEW-FEAT-01)

**Date:** 2026-11-15. **Queue item:** P-NEW-FEAT-01 (new owner direction).

**Scope.** 28 sponsors:
- the FY2024 top 20 by corrected DAF assets;
- 6 digital-first sponsors: Daffy, Charityvest, Endaoment, Every.org, Givinga, and GiveClear/TIFIN Give;
- 2 app comparators: GoFundMe Giving Funds and The Donors' Fund.

Each sponsor is scored on 17 donor-facing features, plus app ratings.

**Outputs:**
- `data/mission-2026-11-14/donor-feature-census-2026.csv`: 504 rows (28 sponsors × 18 fields), each with a URL and an evidence label.
- `data/mission-2026-11-14/queue-proposals-batch42-n22.csv`: 3 queue proposals.

**Rules followed:**
- Public product pages, help centres and app-store listings only.
- robots.txt was read before every fetch, and pages were skipped where robots.txt was unreadable or disallowed the page. That rule was checked for `*`, ClaudeBot, Claude-User and anthropic-ai.
- No logins, outreach or form submissions.
- Current features are based on 2025–2026 evidence. Older documents are flagged `recency_ok=no`.

**Governing corrections respected:**
- Batch 36, waves 21–22:
  - Endaoment's T&C bars sharing API credentials. Its sanctioned routes are OAuth or the Partner API.
  - Daffy Organizers and Advisors may be entities.
  - Benevity moves to AMBER.
- Batch 35, wave 20: Daffy *gift* writes are not counted as fund debits.
- Accessibility note §4: no quality ranking is implied.

## 0. Answer in brief

| Question | Finding |
|---|---|
| **What is table stakes?** | Five features appear wherever a sponsor documents its offering, and are almost never documented as absent: **stock contributions** (13 Y), **complex/illiquid assets** (15 Y), **crypto** (13 Y; Vanguard is the one top-5 sponsor where none was found), **family/successor roles** (14 Y) and **some adviser access** (14 Y, 5 partial). **Recurring grants** (10 Y) and **charity search plus vetting** (9 and 8 Y) are standard wherever there is a self-serve portal [F/C]. |
| **What differentiates?** | These features are rare and concentrated at digital-first sponsors: a **native app** (5 confirmed iOS routes, 2 of them through parent or general apps), **giving pages and campaigns** (5 Y, all digital), **workplace programmes** (Daffy for Work and Givinga Y; 6 partial), **AI assistant or agent access** (2 Y: Daffy's MCP server and TIFIN Give's Louise), a **public API** (3 Y: Daffy, Endaoment, Every.org) and a **self-serve data export** (3 Y; 11 ND). |
| **Where can a new entrant differentiate?** | (1) **Donor-level impact reporting.** Only Endaoment publishes public impact reports; everyone else stops at grant status. (2) **A portable, documented data export plus scoped agent access.** Daffy has the only member MCP server and documents no key scopes. Endaoment requires a registered OAuth client. (3) **Consumer payroll or round-up funding.** No sponsor offers it; Givinga's payroll integration is employer-side. (4) **Adviser data feeds outside the wirehouses.** Addepar feeds exist only for Fidelity, GS, MS and BofA. (5) **Android plus a good app.** Fidelity's apps have 24 iOS and 29 Play ratings; Daffy has 560 iOS ratings and no Android listing was found. |
| **Confidence** | **Medium-low for absences.** 267 of 476 sponsor-feature cells are `U`, because no readable page covered them. Six sponsor sites could not be read: robots.txt unreadable or 403 at dafgiving360.org, gspf.org, morganstanley.com, raymondjamescharitable.org and every.org, and a 403 on the cct.org home page. **ND means "not found on the pages read", not "absent"** [I]. |

## 1. Method
1. **Sponsor list.**
   - The top 20 follow `sponsor-a11y-axe-2026.csv` (FY2024 corrected assets).
   - Digital-first sponsors are as listed in the queue item. GoFundMe Giving Funds and The Donors' Fund were added because they turned up in App Store and Play results as DAF apps.
2. **Fetching.**
   - A robots-aware fetcher was used. It parsed robots.txt with Python `urllib.robotparser`; a robots.txt it could not read counted as a block.
   - Crawls were seeded from each home page or help centre and kept to links whose paths contained feature keywords, up to 16–25 pages per sponsor.
   - Help centres read: help.daffy.org, support.every.org, guide.charityvest.org, intercom.help/give-ria and docs.daffy.org.
3. **App stores.**
   - apps.apple.com and play.google.com detail pages are allowed by robots.txt. Their search pages and the iTunes Search API (`itunes.apple.com/search`) are disallowed, so they were not used.
   - App IDs came from sponsor pages, earlier repo work (batch 28) or web-search results. The search engine did the lookup; the hosts themselves were not fetched.
4. **Reuse.** Rows labelled `C` carry evidence already validated in the repo:
   - `sponsor-data-feeds-2026.csv`
   - `delegated-access-routes-2026.csv`
   - `donor-data-export-top10-2026.csv`
   - `donor-export-evidence-cf-2026.csv`
   - `bank-program-terms-2026.csv`
   - `daf-agent-wrappers-2026.csv`
   - `agentic-philanthropy-products-2026.csv`
5. **Values.**
   - `Y`: documented.
   - `P`: partial or conditional.
   - `ND`: not found on the pages read.
   - `U`: not assessed, because no readable page covered the feature.
6. **Labels.**
   - `F`: first-hand fetch on 2026-11-15.
   - `C`: carried from a repo CSV.
   - `S`: web-search snippet only; the host was not fetched.

## 2. Census matrix

Key: ● Y · ◐ P · ○ ND · · U. The column order is listed under the table. App ratings are given in §3.

| Sponsor | iOS | And | Rec | Stk | Cry | Cpx | Srch | Vet | Trk/Imp | Fam | Adv | Page | Work | AI | API | Exp | Pay |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Fidelity Charitable (1) | ● | ● | ● | ● | ● | ● | ● | ● | ◐ | ● | ● | ○ | ◐ | ◐ | ○ | ○ | ○ |
| NPT (2) | · | · | · | ● | ● | ● | · | · | · | ● | ● | · | · | · | ○ | ◐ | · |
| DAFgiving360 (3) | ● | ●S | ● | · | · | · | · | · | · | · | ● | · | · | · | · | ◐ | · |
| Vanguard Charitable (4) | ○ | ○ | ● | ● | ○ | ● | ● | ● | ◐ | ● | ● | ○ | ◐ | ○ | ○ | ○ | ○ |
| GS Philanthropy Fund (5) | · | · | · | · | · | · | · | · | ◐ | ● | ● | · | · | · | ○ | ○ | · |
| SVCF (6) | ○ | · | ○ | ● | ● | ● | ◐ | · | · | ● | ◐ | · | · | ○ | ○ | ○ | · |
| Morgan Stanley GIFT (7) | · | · | ● | · | · | · | · | ● | ● | ● | ● | · | · | · | ○ | ○ | · |
| AEF (8) | · | · | · | ● | · | ● | · | ● | · | ● | ● | · | · | · | · | ○ | · |
| RCF / Ren (9) | · | · | ● | · | ● | ● | · | ● | · | · | ● | · | · | · | · | ○ | · |
| NCF (10) | ○ | · | ● | ● | ● | ● | · | ● | ◐ | ● | ◐ | · | · | ○ | · | ○ | · |
| BofA CGF (11) | ◐ | · | ● | · | · | · | ● | · | ● | ● | ● | · | · | · | · | ◐ | · |
| Chicago Community Trust (12) | · | · | · | · | · | · | · | · | · | · | ◐ | · | · | · | · | ● | · |
| ImpactAssets (13) | · | · | · | ● | · | ● | · | · | ◐ | · | · | · | · | · | · | · | · |
| Jewish Communal Fund (14) | · | · | · | · | · | · | · | · | · | ● | ◐ | · | · | · | · | · | · |
| FFTC (15) | · | · | · | · | · | · | · | · | · | ◐ | · | · | · | · | · | ○ | · |
| GKCCF (16) | · | · | · | · | ● | ● | · | · | · | ● | ● | · | ◐ | · | · | ◐ | · |
| Greater Horizons (17) | · | · | · | · | · | · | · | · | · | · | ● | · | · | · | · | · | · |
| CJP (18) | · | · | · | ● | ● | ● | · | · | ◐ | · | · | · | ◐ | · | · | · | · |
| Raymond James Charitable (19) | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · |
| Dechomai (20) | · | · | · | · | ● | ● | · | · | · | · | · | · | · | · | · | · | · |
| **Daffy** | ● | · | ● | ● | ● | ● | ● | ○ | ◐ | ● | ● | ● | ● | ● | ● | ● | ○ |
| **Charityvest** | ○ | · | ○ | ● | ● | ● | ● | · | · | ○ | ◐ | ● | ◐ | ○ | ○ | ○ | ○ |
| **Endaoment** | ○ | · | ○ | ● | ● | ● | ● | ● | ● | ● | ● | ◐ | ○ | ◐ | ● | ◐ | ○ |
| **Every.org** | · | · | ● | ● | ● | ◐ | ● | ◐ | · | ○ | ○ | ● | ◐ | ○ | ● | ○ | ○ |
| **Givinga** | · | · | · | · | · | · | ● | ● | ● | · | · | · | ● | · | ○ | ● | ● |
| **GiveClear / TIFIN Give** | ○ | · | ● | ● | ● | ● | ● | · | ◐ | ● | ● | ● | ○ | ● | ○ | ◐ | ○ |
| GoFundMe Giving Funds | ● | ● | · | · | · | · | · | · | · | · | · | ● | · | · | · | · | · |
| The Donors' Fund | ● | ● | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · |

**Columns:**
- iOS / And: iOS or Android app route.
- Rec: recurring or scheduled grants.
- Stk / Cry / Cpx: stock, crypto and complex-asset contributions.
- Srch / Vet: charity search; charity vetting.
- Trk/Imp: grant tracking or impact reporting.
- Fam: family, successor or co-advisor roles.
- Adv: adviser access or data feeds.
- Page: giving pages, campaigns or social sharing.
- Work: workplace or matching.
- AI: AI assistant.
- API: API or agent access.
- Exp: self-serve data export.
- Pay: payroll or round-ups.

**Cell notes:**
- The DAFgiving360 iOS ● is DAF granting inside Schwab Mobile.
- "●S" (DAFgiving360 Android) rests on a search-engine snippet of dafgiving360.org only.
- The BofA iOS ◐ means balances appear in the MyMerrill and BofA parent apps.

### 2.1 Feature counts (28 sponsors)

| Feature | Y | P | ND | U |
|---|---|---|---|---|
| Complex/illiquid assets | 15 | 1 | 0 | 12 |
| Family/successor roles | 14 | 1 | 2 | 11 |
| Adviser access/feeds | 14 | 5 | 1 | 8 |
| Stock contributions | 13 | 0 | 0 | 15 |
| Crypto contributions | 13 | 0 | 1 | 14 |
| Recurring grants | 10 | 0 | 3 | 15 |
| Charity search | 9 | 1 | 0 | 18 |
| Charity vetting | 8 | 1 | 1 | 18 |
| Giving pages/social | 5 | 1 | 2 | 20 |
| iOS app route | 5 | 1 | 6 | 16 |
| Android app | 4 | 0 | 1 | 23 |
| Grant tracking/impact | 4 | 8 | 0 | 16 |
| API/agent access | 3 | 0 | 9 | 16 |
| Data export | 3 | 6 | 11 | 8 |
| Workplace/matching | 2 | 6 | 2 | 18 |
| AI assistant | 2 | 2 | 5 | 19 |
| Payroll/round-ups | 1 | 0 | 7 | 20 |

## 3. Key evidence by feature

**Apps** (store pages read 2026-11-15):

| App | iOS | Android | Other detail | Sources |
|---|---|---|---|---|
| Fidelity Charitable | 3.6 from 24 ratings; v5.22 released "3d ago" | 3.8 from 29 reviews; 5K+ downloads; updated 2026-11-09 | – | [App Store](https://apps.apple.com/us/app/fidelity-charitable/id552407907); [Play](https://play.google.com/store/apps/details?id=com.fidelity.charitable&hl=en_US&gl=US) |
| Daffy | 4.9 from 560 ratings; v1.54.4 | No Play listing found by web search; `com.daffy.app` belongs to an unrelated developer | – | [App Store](https://apps.apple.com/us/app/daffy-save-invest-give/id1578035540) |
| DAFgiving360 (Schwab Mobile) | Version note: "DAFgiving360™ - Recommend grants with a redesigned, fully native mobile experience" (16.3.0, Mar 26). The 4.8 rating from 1.2M ratings is app-level. | – | – | [Schwab Mobile](https://apps.apple.com/us/app/schwab-mobile/id407358186) |
| GoFundMe | 4.7 from 49K ratings | 4.6 from 82.8K reviews | Listing: "Giving Funds are donor-advised funds (DAF)" | [App Store](https://apps.apple.com/us/app/gofundme-fundraise-and-give/id734130700) |
| The Donors' Fund | 5.0 from 28 ratings | 4.5 from 35 reviews | – | [App Store](https://apps.apple.com/us/app/the-donors-fund/id6446094453) |

- **No standalone app was found** for Vanguard Charitable (repo batch 28; web search), NCF (search snippet: "mobile site"), Endaoment (web app), Charityvest or TIFIN Give [I].

**Recurring grants:**
- Fidelity: "set up recurring grant recommendations" ([home](https://www.fidelitycharitable.org/)).
- Vanguard: "setting up recurring grants" ([home](https://www.vanguardcharitable.org/)).
- NCF: "schedule recurring grants for up to three years" ([guide](https://www.ncfgiving.com/guide-to-giving-at-NCF)).
- Ren: "Options for recurring or scheduled grants" ([FAQ](https://www.reninc.com/faqs/)).
- Daffy ([help](https://help.daffy.org/en/collections/3148647-donate-to-charities)).
- TIFIN Give ([granting FAQ](https://intercom.help/give-ria/en/articles/10670838-granting-faqs)).
- Every.org ([help](https://support.every.org/hc/en-us/articles/4410882247827-How-do-I-cancel-a-recurring-donation)).
- BofA ([guide 2025-09](https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf)) [C].
- DAFgiving360: 38% of 1.5M CY2025 grants were recurring [C].

**Non-cash assets:**
- Fidelity lists crypto, S-corp, LLC/LP and pre-IPO assets ([what you can donate](https://www.fidelitycharitable.org/giving-account/what-you-can-donate.html)).
- Daffy "received more than $675 million in stock contributions in 2026 alone, including over $600 million in private and restricted stock" ([home](https://www.daffy.org/)).
- SVCF ([complex assets](https://www.svcf.org/advisors/complex-assets)), CJP ([DAF page](https://www.cjp.org/donor-advised-funds?hsLang=en)), GKCCF ([contribute](https://www.growyourgiving.org/individual-family-giving/contribute-to-your-fund/)) and NCF ([assets](https://www.ncfgiving.com/assets)) all list crypto.

**Family and adviser roles:**
- Daffy: roles and permissions, successor, Daffy for Families, and adding an adviser ([manage](https://help.daffy.org/en/collections/10671593-manage-your-daf); [what's new](https://help.daffy.org/en/collections/12314612-what-s-new)).
- TIFIN Give: "Add family members to your DAF" ([collection](https://intercom.help/give-ria/en/collections/9568157-involve-the-family-in-giving)) and advisor-managed accounts ([article](https://intercom.help/give-ria/en/articles/9450522-advisor-managed-accounts)).
- Endaoment: "donors, their family and advisors" ([app](https://endaoment.org/app)).
- Adviser *data feeds* (Addepar) are listed only for Fidelity, GS, MS GIFT and BofA ([Addepar listing](https://integrations.addepar.com/product/fidelity-investments-charitable-gift-fund-donor-advised-fund)) [C].

**Giving pages and workplace:**
- Daffy runs campaigns with matching ([help](https://help.daffy.org/en/collections/6682672-run-campaigns)) and Daffy for Work ([help](https://help.daffy.org/en/collections/5328886-daffy-for-work)).
- Every.org fundraisers can cover up to 10 nonprofits (2026-10-29, [help](https://support.every.org/hc/en-us/articles/56925184326675-How-can-I-create-a-fundraiser-for-multiple-nonprofits)).
- Charityvest has Community Funds ([guide](https://guide.charityvest.org/community-funds/donate-to-a-community-fund)).
- TIFIN Give has community giving campaigns ([help](https://intercom.help/give-ria/en/articles/10693593-community-giving-campaigns)).
- Givinga offers "Flexible matching, payroll integration" ([home](https://www.givinga.com/)).
- The top 20 show corporate DAF programmes (Fidelity, Vanguard, GKCCF), but no donor giving pages.

**AI and agent access:**
- Daffy's MCP server: "Connect Claude, ChatGPT or any other AI assistant to your Daffy account and it can search charities, check your balance, … and make or cancel donations … available to every Daffy member" ([docs](https://docs.daffy.org/agents/mcp)).
- TIFIN Give: "Most inquiries can be handled directly on the platform through our AI Assistant Louise" ([FAQ](https://intercom.help/give-ria/en/articles/9845503-tifin-give-faqs)).
- Endaoment: OAuth and Partner API ([api](https://endaoment.org/api)), plus a first-party ndao CLI with MCP mode [C].
- Every.org: free Charity API ([docs](https://docs.every.org/docs/intro)).
- Fidelity's Virtual Assistant is an "automated natural language search engine" for the site, with no account access ([terms](https://www.fidelitycharitable.org/legal/virtual-assistant.html)).

**Export:**
- Daffy: "consolidated tax receipts in a PDF or CSV" ([guide](https://www.daffy.org/resources/donating-crypto-complete-guide)).
- CCT: grant history as CSV ([FAQ 2025-12](https://donorportal.cct.org/ma/docs/cct/CCT-Donor-Portal-FAQ.pdf)) [C].
- BofA: contributions to Excel only [C].
- Fidelity and Vanguard: PDFs or on-screen views only [C].

**Payroll and round-ups:**
- Givinga integrates payroll on the employer side only.
- Daffy for Work says "No payroll integration or IT support is required" ([post](https://www.daffy.org/resources/daffy-modernizes-workplace-giving)).
- No consumer round-up feature was found anywhere [I].

## 4. Reading: table stakes vs differentiators vs white space

1. **Table stakes for any entrant** [I]:
   - accept stock, crypto and complex assets (or partner for them; see noncash-gift-vendors-2026.csv);
   - recurring grants;
   - charity search with vetting;
   - successor and family roles;
   - adviser view access.

   Each is documented at the largest sponsors and at every digital-first sponsor read. Lacking one is a reason not to switch.
2. **Digital-first differentiators already taken** [I]:
   - Daffy covers nearly every feature (app, campaigns, Daffy for Work, MCP, API, CSV).
   - TIFIN Give has an AI assistant, campaigns and family roles, but no app.
   - Endaoment is strongest on advisers, non-cash assets, impact and API access.
   - An entrant competing on "modern app plus campaigns" meets Daffy head-on.
3. **White space** (ND or U at nearly all 28 sponsors) [I]:
   - **(a) Donor-level impact reporting.** Today this means grant status only. Endaoment's impact reports are platform-level.
   - **(b) A portable export with documented scope,** for example a CSV/JSON grant ledger.
   - **(c) Scoped, auditable agent access.** Today agent access exists at Daffy, which documents no key scopes, and at Endaoment, whose OAuth registration is gated. Batch 36 found no sponsor documents per-action limits.
   - **(d) Consumer payroll or round-up funding.**
   - **(e) Adviser feeds for RIAs outside the four wirehouse feeds.**
   - **(f) Android.** It is confirmed only where a parent app exists (Fidelity, GoFundMe, The Donors' Fund).
4. **Caveat.** A top-20 sponsor may ship (a), (b) or (e) inside a vendor portal without saying so. For example, GivingPoint's code contains Excel export handlers (batch 33B). Proposal P-B42N22-02 tests this.

## 5. Limitations
- **Many unknowns.** 267 of 476 cells are `U`. Six sponsor hosts were unreadable, and Charityvest's marketing pages render client-side. Its help guide was read instead.
- **Absence is not proven.** `ND` is "not found in 16–25 pages read".
- **Store ratings are popularity signals,** not quality measures. Schwab and GoFundMe ratings cover whole apps.
- **Older documents.** Some carried rows rest on documents from before 2025: the GS 2008 circular, MS GIFT's 2024-08 circular and BofA's 2024 guidelines. All are flagged `recency_ok=no`.
- **Pass-through vs DAF.** Every.org is a pass-through platform, and Givinga is employer and partner infrastructure. Their features are not all donor-DAF features.

## 6. Source register

| ID | Source | Type | Date | URL |
|---|---|---|---|---|
| S01 | Apple App Store listings (Fidelity Charitable, Daffy, Schwab Mobile, GoFundMe, The Donors' Fund) | app store | read 2026-11-15 | https://apps.apple.com/us/app/fidelity-charitable/id552407907 ; https://apps.apple.com/us/app/daffy-save-invest-give/id1578035540 ; https://apps.apple.com/us/app/schwab-mobile/id407358186 ; https://apps.apple.com/us/app/gofundme-fundraise-and-give/id734130700 ; https://apps.apple.com/us/app/the-donors-fund/id6446094453 |
| S02 | Google Play listings (Fidelity, GoFundMe, The Donors' Fund) | app store | read 2026-11-15 | https://play.google.com/store/apps/details?id=com.fidelity.charitable&hl=en_US&gl=US ; https://play.google.com/store/apps/details?id=com.GoFundMe.GoFundMe&hl=en_US&gl=US ; https://play.google.com/store/apps/details?id=org.thedonorsfund.mobile&hl=en_US&gl=US |
| S03 | Fidelity Charitable product pages and Virtual Assistant terms | sponsor | live | https://www.fidelitycharitable.org/ ; https://www.fidelitycharitable.org/giving-account/what-you-can-donate.html ; https://www.fidelitycharitable.org/giving-account/giving-account-details.html ; https://www.fidelitycharitable.org/legal/virtual-assistant.html |
| S04 | Vanguard Charitable pages and FAQs | sponsor | live | https://www.vanguardcharitable.org/ ; https://www.vanguardcharitable.org/faqs ; https://www.vanguardcharitable.org/advisors |
| S05 | NPT DAF page | sponsor | live | https://www.nptrust.org/donor-advised-funds/ |
| S06 | SVCF pages | sponsor | live | https://www.svcf.org/advisors/complex-assets ; https://www.svcf.org/donors/philanthropic-advising |
| S07 | AEF home and advisors | sponsor | live | https://www.aefonline.org/ ; https://www.aefonline.org/advisors/ |
| S08 | Ren DAF pages and FAQ | administrator | live | https://www.reninc.com/faqs/ ; https://www.reninc.com/giving-vehicles/donor-advised-fund/ |
| S09 | NCF guide, assets, support | sponsor | live | https://www.ncfgiving.com/guide-to-giving-at-NCF ; https://www.ncfgiving.com/assets ; https://www.ncfgiving.com/support |
| S10 | ImpactAssets, JCF, FFTC, GKCCF, CJP, Dechomai pages | sponsor | live | https://impactassets.org/donor-advised-fund/ ; https://www.jcfny.org/ ; https://www.fftc.org/individual-family-giving ; https://www.growyourgiving.org/open-a-donor-advised-fund/ ; https://www.cjp.org/donor-advised-funds?hsLang=en ; https://www.dechomai.org/ |
| S11 | Daffy site, help centre, developer docs | sponsor | live | https://www.daffy.org/ ; https://help.daffy.org/en/ ; https://docs.daffy.org/agents/mcp |
| S12 | Charityvest Guide | sponsor | live | https://guide.charityvest.org/ |
| S13 | Endaoment site, API page, llms.txt, release notes | sponsor | live; release notes 2026-11-12 | https://endaoment.org/app ; https://endaoment.org/api ; https://endaoment.org/llms.txt ; https://blog.endaoment.org/release-notes |
| S14 | Every.org help centre and Charity API docs | platform | articles 2021–2026 | https://support.every.org/hc/en-us/articles/32398815517459-How-can-I-donate-stock-to-a-charity-using-Every-org ; https://docs.every.org/docs/intro |
| S15 | Givinga home and demo page | vendor | live | https://www.givinga.com/ ; https://www.givinga.com/schedule-a-demo |
| S16 | TIFIN Give help centre (GiveClear sponsor) | sponsor platform | live | https://intercom.help/give-ria/en/ |
| S17 | Repo CSVs carried (`C`) | repo | 2026-11-14/15 | sponsor-data-feeds-2026.csv; delegated-access-routes-2026.csv; donor-data-export-top10-2026.csv; donor-export-evidence-cf-2026.csv; bank-program-terms-2026.csv; daf-agent-wrappers-2026.csv; agentic-philanthropy-products-2026.csv |
| S18 | Web-search snippets (`S`; host not fetched) | search | 2026-11-15 | dafgiving360.org/how-to-recommend-grant-mobile; every.org privacy policy; NCF mobile-site page |

**Blocked or not used:**
- **robots.txt unreadable (403):** www.dafgiving360.org and dafgiving360.org, www.every.org, www.gspf.org, morganstanley.com, raymondjamescharitable.org.
- **robots.txt disallowed:** www.rencharitable.org; apps.apple.com `*/search?*`; play.google.com `/store/search`; itunes.apple.com Search API.
- **Home page returned 403:** cct.org.
- **Returned 404:** bankofamerica.com/philanthropic/charitable-gift-fund/, tifingive.com, and NCF's "go-mobile" page.
- crt.sh was not used.

## 7. Data dictionary

### `donor-feature-census-2026.csv` (one row per sponsor × feature)

| Column | Meaning |
|---|---|
| census_id | DFC-001… |
| sponsor | Sponsor or platform name |
| segment | `top20`, `digital` or `digital comparator` |
| fy2024_rank | FY2024 corrected DAF-asset rank (blank for digital) |
| feature | One of: ios_app, android_app, app_rating, recurring_grants, stock_contrib, crypto_contrib, complex_assets, charity_search, charity_vetting, grant_tracking_impact, family_successor_roles, adviser_access_feeds, giving_pages_social, workplace_matching, ai_assistant, api_agent_access, data_export, payroll_roundups |
| value | `Y` documented; `P` partial or conditional; `ND` not found on pages read; `U` not assessed. For app_rating, the rating text. |
| detail | Short quote or paraphrase |
| evidence_url | Primary URL (blank where carried without a single URL; see notes) |
| evidence_date | Document or page date (`live 2026-11-15` for undated live pages) |
| evidence_label | `F` first-hand fetch; `C` carried from a repo CSV; `S` search snippet only |
| recency_ok | `yes` (2025–2026 or live), `no` (older document), `unknown` |
| retrieved | Access date |
| notes | Carried-file pointer and caveats |

### `queue-proposals-batch42-n22.csv`

Columns and scales follow [queue-proposals-README.md](../../data/mission-2026-11-14/queue-proposals-README.md):
- `importance`, `gap`, `commercial`, `availability` and `effort` are 1–5.
- `p_change` is 0–1.
- `state` is `open`.
- `proposed_by` is `batch42 N22`.
