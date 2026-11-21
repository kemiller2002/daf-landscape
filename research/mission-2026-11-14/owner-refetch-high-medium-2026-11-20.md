# Owner-directed re-fetch: high- and medium-priority targets, plus sources blocked on 2026-11-20

**Date:** 2026-11-20.

**Basis.** These sources were fetched under the [owner decision on robots.txt](../education/owner-decision-robots-2026-11-20.md). No login, CAPTCHA, bot challenge or paywall was bypassed.

**Related files:**
- Fetch log: [`owner-refetch-results-2026-11-20.csv`](../../data/mission-2026-11-14/owner-refetch-results-2026-11-20.csv).
- Low-priority citation re-check: [owner-refetch-citation-recheck-2026-11-20.md](owner-refetch-citation-recheck-2026-11-20.md).

All corrections listed below have been applied to the named files in this commit.

## 1. Per-target results

| Target | Obtained | Key facts | Effect | Repo location |
|---|---|---|---|---|
| OF-016 Chariot/K2D DAF Fundraising Report | Webinar and toolkit pages. The report PDF sits behind a HubSpot form; the slides are view-only on DocSend | 54 organisations; $26.1bn total giving; $3.3bn DAF revenue; 907k DAF gifts. Median DAF growth +75% against +9%. Two-thirds of DAF gifts are under $1,000. Major gifts are 2% of DAF gifts but more than 22% of major-gift revenue. Median gift $300 | Confirmed. The identification method and the major-gift threshold are only in the gated PDF | `direction-nonprofit-daf-benchmarks.md`; NPB001–021 |
| OF-017 M+R Benchmarks 2026 | Web chapter with its chart data. The PDF is behind a reCAPTCHA form | DAF revenue +44%; DAF gifts +23%; average DAF gift $1,430. **New: 46.1% of participants accept DAF on their main donation page (30% in the 2025 edition).** No 2026 figure for DAF revenue per online dollar | NPB073–075 upgraded to [P]; new row NPB-MR26-46 | same files |
| OF-018 DAFRC *Reinventing the Cycle* | Full PDF (IU ScholarWorks API, CC BY) | Fundraiser study: 46 participants, June–October 2023. Six challenges, with no frequencies. "only 4% of grants are completely anonymous and that 79% of partially anonymous grants include identifiable information" (endnote 37) | **Changed:** NPT's "79% partially anonymous" headline misreads this | `direction-nonprofit-side-experience.md`; `nonprofit-side-daf-issues-2021-2026.csv` |
| OF-019 Candid API licence | Full licence, updated 2026-09-14 | s.3.b.xi now reads "in or through the use of" AI, and a survival sentence is added. Still no caching clause | Confirmed; wording changed | `b43n26-03-charity-data-terms-ai.md` |
| OF-020 NCF Program Agreement | Full agreement, effective 2025-09-17 | The donate button is a revocable licence covering only the charity's own NCF fund. No donor-eligibility, minimum, receipting or visibility terms. Third parties get a written acknowledgment | New | `b4222-02-01-01-foundant-docs-ncf-donate.md`; `foundant-docs-ncf-donate-2026-11-20.csv` D09 |
| OF-035 Goldman Sachs Philanthropy Fund circular | Login page only | — | Not obtained (login) | — |
| OF-038 FreeWill DAF reports | Report pages gated by a HubSpot form | The blog repeats the 72/20/33/81/10% figures; no sample size given | Not obtained | — |
| OF-061 Mayo Clinic DAF page | Full page | DAFpay; Mayo's own DAF has a $100k minimum with a 60/40 split; no pledge or benefit clause | Confirmed; new details | `gift-office-daf-policies-2026.csv` GO-21 |
| OF-062 NYU | Homepage only; giving pages return 403 | — | Not obtained | — |
| OF-072 JCF | Homepage only; subpages behind a Cloudflare challenge | $4bn, 5,500 funds, $5k minimum | Unchanged | — |
| OF-073 BofA Charitable Gift Fund | Programme page and Accessible Banking page | Service is through an adviser; no hours or SLA; WCAG 2.1 A/AA statement | New | `sponsor-service-levels-2026.csv` |
| OF-074 Morgan Stanley GIFT | Programme page | $25,000 minimum; no hours, SLA or accessibility link | New | same (rank 7) |
| OF-075 Oregon Community Foundation FY2024 audit | Full PDF | No fee-revenue line; operating expenses $22.0m; advised funds $1.007bn; no split for corporate DAFs | Status changed | `sponsor-fee-revenue-margin-2026-11-19.csv` rank 25 |
| OF-076 Candid blog | Full post (2026-06-08) | Confirms NPB007–009. Gives a 2022–25 comparison of +75% against +12%, which conflicts with Chariot's 2021–25 figure of +9% | [R] → [S] | NPB007–009 |
| OF-079 Foundant | foundant.com plus the support-site Zendesk API | Giving Hub lists any non-Private fund that has a checking account. The Donor Advised flag has no system function. Fia is in beta | **New:** no DAF-specific default, so DAFs are visible unless marked Private | `b4222-02-01-01…`; `gap19-fee-and-delivery-refresh.md` |
| OF-081 Schedule I grant lists | IRS TEOS graphic prints | Schedule I says only "See Attached Grant Report"; the attachment is absent | **Changed:** P-B34A-02 cannot be met from public filings | `queue-batch34-netting-filings.md` |
| OF-084 Cornell | DAF page | No DAFpay or DAF Direct; EIN shown; notification form | New | donate-page scan |
| OF-086 Doctors Without Borders | Donate form | EIN shown; link to a DAF FAQ; the DAF page returns 403 | Partial | donate-page scan |
| OF-094, OF-096, OF-097 | Pages read | Support the citing claims | Confirmed | `citation-link-health-2026-11-19.csv` |

## 2. Sources blocked during today's investigations

| Source | Result |
|---|---|
| Foundant leadership | Read from foundant.com/about/leadership-team. CEO Josh Mallamud and others are now recorded in PV07 |
| Blackbaud leadership | investor.blackbaud.com returns an Akamai 403. blackbaud.com's executive page was read. CEO Gianoni and Chief Data & AI Officer Carrie Cobb are recorded in PV06 |
| Ren / Great Hill release (2025-10-28) | Business Wire is walled, so a syndicated copy was read. Ren claims "more than 150 DAF programs … over $175 billion … roughly half" of US DAF assets, which is a vendor claim. Great Hill's advisers were Houlihan Lokey and Goodwin. Recorded in PV01 |
| Northern Trust | Srilatha Lakkaraju, Director of Charitable Giving Solutions, is confirmed on northerntrust.com. Recorded in PW13 |
| DAFRC site | The adviser study (669 advisers) and the annual report match what the repository already records |
| JD Supra | Nothing new |
| Indeed, Glassdoor | Both serve a security challenge, which was not bypassed |

## 3. Still blocked (needs the owner's own browser)

| Source | Block |
|---|---|
| Chariot/K2D report PDFs; FreeWill PDFs | HubSpot form |
| M+R 2026 PDF | reCAPTCHA |
| Goldman Sachs Philanthropy Fund circular | Login |
| NYU and Doctors Without Borders DAF pages, JCF subpages, DAFgiving360, Business Wire, investor.blackbaud.com, ProPublica downloads | Cloudflare or Akamai walls |
| web.archive.org; several sponsor and university hosts | Session proxy cannot reach them (reset or 502) |
| regulations.gov comment attachments | downloads.regulations.gov returns 403. Comment metadata is being collected through the official API |
