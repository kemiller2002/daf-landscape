# Citation re-check: low-priority owner re-fetches (2026-11-20)

Scope: the 148 rows in `data/mission-2026-11-14/owner-refetch-results-2026-11-20.csv` with `priority=low` and `result=fetched`. Each saved body was turned into text (pdftotext for PDFs, tags stripped for HTML, JSON parsed). Each was checked against the citing text in the repo, found by exact URL match across `research/**/*.md` and `data/**/*.csv`. Per-row detail: `citation-recheck.csv` (same folder).

## Counts by verdict

| Verdict | n |
|---|---|
| supports | 90 |
| partially supports | 7 |
| does not support | 3 |
| page changed | 3 |
| cannot judge | 45 |
| **total** | **148** |

The 45 "cannot judge" rows break down as follows:
- **18 homepage-only targets.** The repo cites a deeper page.
- **19 donate-page scan rows.** These are fetch-status records, not content claims.
- **8 others:**
  - 2 pages are JS shells: OF-155 and OF-218.
  - 5 bodies saved as "fetched" were really challenge pages: Reddit OF-513 to OF-516, and OF-253.
  - OF-121 is an access-status note.

The donate-scan group also contains three more such pages: the challenge or block pages OF-311 and OF-322 (Incapsula), and the JS shell OF-338. None of these pages were bypassed.

**Key documents:** none of the 148 low-priority URLs is cited verbatim in `research/DAF-INDUSTRY-REPORT-2026-11.md` or `research/mission-2026-11-14/strategic-synthesis.md`. The four apparent hits are deeper paths on the same hosts: tifin.com/news, dafresearchcollaborative.org/s/…, docs.daffy.org/agents…, and iphiview.com/tcf/LogIn. **No correction to either key document is needed from this batch.**

## Corrections (Find / Replace)

All find strings were copied from the files and checked to occur exactly once.

### Does not support (3): "unmapped" CF rows whose homepage now links a Foundant tenant

1. **OF-147, Wichita Falls.** File: `data/mission-2026-11-14/cf-vendor-map-by-ein-v2.csv`
   - Find: `752817894,Wichita Falls Area Community,53354456,https://www.wfacf.org/,,unmapped,,,none,2026-11-15,Unmapped,unknown`
   - Replace: `752817894,Wichita Falls Area Community,53354456,https://www.wfacf.org/,https://wichitacf.fcsuite.com/erp/donate,Foundant CommunitySuite,homepage_link_vendor_host,https://www.wfacf.org/,high,2026-11-20,Foundant,yes`
   - Evidence: the homepage nav has `href="https://wichitacf.fcsuite.com/erp/donate"` ("Donate").
2. **OF-260, Whitley County.** Same file.
   - Find: `351860518,WHITLEY COUNTY COMMUNITY,5769284,https://cfwhitley.org/,,unmapped,,,none,2026-11-15,Unmapped,unknown`
   - Replace: `351860518,WHITLEY COUNTY COMMUNITY,5769284,https://cfwhitley.org/,https://whitley.fcsuite.com/erp/donate,Foundant CommunitySuite,homepage_link_vendor_host,https://cfwhitley.org/,high,2026-11-20,Foundant,yes`
3. **OF-270, Clinton County (OH).** Same file.
   - Find: `311140087,CLINTON COUNTY FOUNDATION,6823964,https://clintoncountyohiofoundation.org/,,unmapped,,,none,2026-11-15,Unmapped,unknown`
   - Replace: `311140087,CLINTON COUNTY FOUNDATION,6823964,https://clintoncountyohiofoundation.org/,https://ccf.fcsuite.com/erp/portal,Foundant CommunitySuite,homepage_link_vendor_host,https://clintoncountyohiofoundation.org/,high,2026-11-20,Foundant,yes`

For all three rows, the trailing `change_note` ("still unmapped after v2 passes") should also be updated. The v1 file `cf-vendor-map-by-ein.csv` has the same stale "unmapped" rows; it is superseded, so it is left alone.

**Optional upgrades (verdict "supports").** Homepage links now give first-party evidence for these rows:
- Brevard (OF-254, `cfbrevard.fcsuite.com`): confidence low → high.
- Verdugos (OF-262): low → high.
- Blue Grass (OF-190): medium → high.
- Miami (OF-189): the homepage names "FCsuite.com" as an official donation portal.

### Page changed (3)

4. **OF-376, Benevity Ashby board.** File: `research/mission-2026-11-14/direction-news-hiring-signals.md`
   - Find: `(23 postings, 14 distinct roles)`
   - Replace: `(23 postings, 14 distinct roles on 2026-11-15; 18 postings, 12 roles on 2026-11-20)`
5. **OF-519, Stellar article.** File: `research/npt-givingpoint-iphi-architecture-and-stellar-customer-cohorts-2026-11-11.md`
   - Find: `- Helping Hands announcement: https://www.stellartechsol.com/sf/Home/ViewArticle/tabid/86/itemId/46/Default.aspx`
   - Replace: `- Helping Hands announcement: https://www.stellartechsol.com/sf/Home/ViewArticle/tabid/86/itemId/46/Default.aspx (now redirects to reninc.com/faith-based-community-foundations/; original not retrievable 2026-11-20)`
6. **OF-520, Stellar TMF case study PDF.** Same file.
   - Find: `- Minneapolis case study: https://www.stellartechsol.com/sf/Portals/26/docs/TMFProfileFINAL020712.pdf`
   - Replace: `- Minneapolis case study: https://www.stellartechsol.com/sf/Portals/26/docs/TMFProfileFINAL020712.pdf (now redirects to a Ren marketing page; PDF not retrievable 2026-11-20)`

### Partially supports (7)

7. **OF-198, Philanthropy Roundtable.** The rates are three-year averages, not 2022 data. The page says "the three year average DAF payout rate was 25.4 percent … 21.9 percent in 2022". File: `research/mission-2026-11-14/analyst-and-education-landscape.md`
   - Find: `national sponsors 25.4% and community foundations 17.1% (2022 data)`
   - Replace: `national sponsors 25.4% and community foundations 17.1% (three-year averages, 2020–2022)`
   - Same file, second fix. Find: `| 2024 (2022 data) |` → Replace: `| 2024 (2020–2022 data) |`
8. **OF-484, CAF American Donor Fund.** The 4.5% is the per-donation Donor Advised Gift retention, not a DAF balance fee. File: `research/mission-2026-11-14/direction-international-comparison.md`
   - Find: `CAF American Donor Fund: 4.5% on the first £50,000; Premier DAF minimum £50k, with a £2,000 a year minimum charge`
   - Replace: `CAF American Donor Fund: 4.5% retention on the first £50,000 of each Donor Advised Gift donation; standard DAF 1.35% on the first £100,000 (minimum £1,600 a year); Premier DAF minimum £50k, with a £2,000 a year minimum charge (schedule from 15 June 2026)`
9. **OF-523, Sunwest lockbox.** The PDF now reads $0.65 per check, $0.25 per scanline item and $100/month maintenance. File: `research/mission-2026-11-14/queue-infrastructure-nonprofit-costs-emerging.md`
   - Find: `About $0.35-$0.65 per item plus $105-$125/month (BancFirst, Sunwest, First Horizon list prices)`
   - Replace: `About $0.25-$0.65 per item plus $100-$125/month (BancFirst, Sunwest, First Horizon list prices; Sunwest PDF read 2026-11-20: $0.65/check, $0.25 scanline, $100/month maintenance + $25 web access)`
   - `data/mission-2026-11-14/nonprofit-receipt-cost-by-rail.csv` row R03 says "$105-$125" monthly and "PDFs not opened". Review it the same way; the cost model there is an assumption.
10. **OF-230, St Jude.** The page says "In three easy steps, you can grant to St. Jude from this page!" The fund-name-only claim is not on the page. File: `data/mission-2026-11-14/gift-office-daf-policies-2026.csv`
    - Find: `'give from your DAF in three clicks', DAFpay`
    - Replace: `'In three easy steps, you can grant to St. Jude from this page!', DAFpay`
    - Same file. Find: `Grant arrives with only fund name unless donor requests otherwise [S]` → Replace: `Grant arrives with only fund name unless donor requests otherwise [S; not on DAF page re-read 2026-11-20]`
11. **OF-149, Candid DAF blog.** "Pull data directly from Candid" and the Platinum Seal "twice" finding are confirmed. NAVi is not mentioned. The post is Candid's write-up of a webinar with a Vanguard Charitable grants manager; she did not author it. Files: `data/mission-2026-11-14/relationship-graph-edges-additions-25.csv` and `data/mission-2026-11-14/relationship-graph-edges-consolidated-2026-11-19.csv`; the string occurs once in each.
    - Find: `Candid blog by a Vanguard Charitable grants manager: most major DAF platforms incl. Vanguard Charitable ""pull data directly from Candid"" for donor search; NAVi charity locator among Candid partner sites; `
    - Replace: `Candid blog (write-up of a Candid webinar with a Vanguard Charitable grants manager): most major DAF platforms incl. Vanguard Charitable ""pull data directly from Candid"" for donor search; `
12. **OF-173, BBB WGA.** The quote is not verbatim on the page. File: `research/mission-2026-11-14/direction-charity-ratings-integrations.md`
    - Find: `"no charge for charity accreditation"`
    - Replace: `"no charge to charities for the accountability assessment"`
13. **OF-141, JCF investment FAQ.** The FAQ confirms the primary pools and the $5,000 primary minimum. The $500k, $1m and $2,500 thresholds are not on it. File: `data/mission-2026-11-14/sponsor-investment-menus-2026.csv`
    - Find: `"search-index captures of jcfny.org forms (2024-04, 2025-03); site returned HTTP 403 to fetch"`
    - Replace: `"search-index captures of jcfny.org forms (2024-04, 2025-03); investment FAQ read 2026-11-20 confirms $5,000 primary minimum (BlackRock Treasury Trust and/or JCF Short Duration Bond Fund), per-option expense ratios, no transaction costs; $500k/$1m/$2,500 thresholds not on FAQ"`

## Other notes (verdict "supports", no edit required)

- **OF-193:** the FWR reprint confirms $8.9bn, +34%, 38% recurring, 1.4m/155k, and 22,000 grants / $69m. The "85% to previously supported" figure rests only on the co-cited Chariot page.
- **OF-174:** the B+ Top-Rated threshold is on the co-cited Top-Rated page, not on the methodology page.
- **OF-375:** "CIAP fee capped at the standard schedule" is the repo's own [I] inference; the ADV does not state it.
- **OF-443:** the current assignee is Everest Effect; the application was filed by Kol Ventures LLC.
- **OF-219:** CASE 10.6% / 12.1% can be upgraded from [S] to [F].
- **OF-292 and OF-316 add new evidence:**
  - NRDC's homepage has a "Donor-advised Funds" link.
  - Groton Hill's donate page says "If paying by Donor Advised Fund use Federal Tax I.D. #: 04-2867945".
- **OF-255:** the Cleveland (TN) domain now redirects to cfocoeeregion.com.
- **OF-275:** the PDF belongs to CF of Greater Muscatine. The targets file says Dubuque; the repo correctly says Muscatine.

## Limits

- **Citing text was found by exact URL match only.** `citation-link-health-2026-11-19.csv` has no claim column, only `first_cited_at`. Claims that cite by footnote ID without the URL, or in other wording, were not traced.
- **For multi-claim rows, only the parts that can be checked against this page were judged.** Parts tied to co-cited sources were not re-checked.
- **Homepage-only targets cannot test the deeper-page claims.** Fetch-status rows (e.g. "robots_unreadable", "http_405") record access history, not page content.
- **Seven bodies classed as "fetched" were challenge, interstitial or JS-shell pages:** OF-253, OF-311, OF-322, OF-338 and OF-513 to OF-516. They were judged "cannot judge" and nothing was bypassed. Response headers (OF-218 CSP) were not captured.
- **Live job boards (Ashby) and homepages change.** A "page changed" verdict reflects 2026-11-20 only.
- **Patent checks covered only the page's title, assignee, status and dates.** Full claims were not compared.
