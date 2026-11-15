# DAF policy: the 2023 proposed regulations, federal lobbying and the 2025 tax law (P-NEW-POL-01)

**Prepared 2026-11-15. Desk research only. No regulator, sponsor, vendor or lobbyist was contacted. Nothing was logged into or submitted.** This is research, not legal or tax advice. Recency rule: 2021+ sources, except the statute and the 2023 proposal itself.

**Labels.** **[F]** means the source states it directly. **[C]** is our own count or arithmetic on sourced data. **[I]** is an inference or judgment. Evidence grades: **P** = primary record read (API record, statute, IRS page, filing); **S** = secondary (law firm, press, sponsor marketing); **SS** = search-engine summary only, not opened.

**Companion data.**
- [`data/mission-2026-11-14/daf-regs-2023-comments-summary.csv`](../../data/mission-2026-11-14/daf-regs-2023-comments-summary.csv): all 249 public submissions posted to docket IRS-2023-0053, each with a commenter type and phase.
- [`data/mission-2026-11-14/daf-lobbying-lda-2021plus.csv`](../../data/mission-2026-11-14/daf-lobbying-lda-2021plus.csv): 359 LDA filings (2021 to 2026 Q3) whose issue text names DAFs, the ACE Act or the QCD-to-DAF bill.
- [`data/mission-2026-11-14/queue-proposals-batch39-n1.csv`](../../data/mission-2026-11-14/queue-proposals-batch39-n1.csv): 3 follow-up questions (P-B39N1-01 to -03).

**Repo context read first, with governing corrections applied.**
- [`regulation-market-structure-portability.md`](regulation-market-structure-portability.md) Q-B09: the 2023 proposal is neither final nor withdrawn; Priority Guidance Plan (PGP) trajectory; OBBBA indirect effects.
- [`industry-incentives-structural-analysis.md`](industry-incentives-structural-analysis.md) §3.4–3.5, with red-team wave 2B: the comment deadline was **February 15, 2024 (extended)**, not January 16. Wave 4 (W4-13) dates the attorneys-general letter to May 21, 2026.
- [`queue-batch38-closeout-checks.md`](queue-batch38-closeout-checks.md) §8 (P-ANL-10): says Fidelity's 2026 Giving Report "does not mention OBBBA or the 0.5% floor". §3.2 below refines that: the report's PDF does tie account growth to bunching ahead of the 2026 tax changes. A correction is proposed in §5. It is not governing until validated.
- [`analyst-and-education-landscape.md`](analyst-and-education-landscape.md), [`queue-batch34-pass-through-channels.md`](queue-batch34-pass-through-channels.md), [`queue-batch37-controls-education.md`](queue-batch37-controls-education.md): mention OBBBA only in passing (CE courses; the Dec 2025 "Universal Sponsored Account"). Nothing here conflicts with their corrections.

**Access and robots.txt.** We read robots.txt on every host before fetching from it.
- **APIs used:**
  - api.regulations.gov v4 with DEMO_KEY: 10 requests an hour. We spent 9 detail calls in total.
  - lda.gov API: robots.txt allows `/api/v1/` at 15 requests a minute. We paced at about 4.5 seconds per call. lda.senate.gov returned 503 "Site Under Maintenance", so we used lda.gov, the LDA system now in use.
- **Hosts we could not read, so not fetched:**
  - www.regulations.gov and downloads.regulations.gov: robots.txt returned 403 from CloudFront. **We therefore did not open any comment-letter PDF.** Positions below come from the NPRM text, sponsor pages and law-firm and press summaries.
  - cof.org: Cloudflare challenge on robots.txt. Council on Foundations pages are cited only from search summaries or the earlier repo citation.
  - unitedphilforum.org and councilofnonprofits.org disallow ClaudeBot.
  - congress.gov disallows anthropic-ai. The statute was read on govinfo.gov instead.
  - sifma.org: robots.txt holds only content-signal comments with no rules.
- crt.sh was not used.

---

## 0. Executive answers

| Q | Answer | Confidence |
|---|---|---|
| **1. Comments on REG-142338-07** | Docket **IRS-2023-0053** (RIN 1545-BI33) holds **249 posted public submissions** (API, 2026-11-15) [[A1](https://api.regulations.gov/v4/comments?filter[docketId]=IRS-2023-0053)]. By posting date [C]: **173** in the comment period (posted by Feb 22, 2024); **63** hearing requests and outlines (Mar–May 2024); and **13 new submissions posted May 13 – Jun 15, 2026**, from AEF, RCF, Ren, SIFMA, ABA, NYSBA, Kallina, Adler & Colvin, "CF (Jenn Holcomb)" and "MCF". The 2026 batch is not in the repo. Secondary counts were snapshots: "more than 150 organizations" (Morgan Lewis, May 2024) and 179 (NPQ, Apr 2024) [[S02](https://www.morganlewis.com/pubs/2024/05/irs-holds-two-day-hearing-on-proposed-donor-advised-fund-regulations),[S03](https://nonprofitquarterly.org/tax-rules-investment-houses-and-donor-advised-funds-whats-at-stake/)]. **By type (postings) [C]:** community foundations 77; individuals 32 plus 5 anonymous; CF and philanthropy associations 29; national sponsors 24; professional bodies 17; law firms 15; faith or single-issue sponsors 13; financial industry 10; fiscal sponsors 8; nonprofit associations 7; advocacy groups 6; vendor (Ren) 2; unclassified 4. **Academics: none identifiable from titles.** | High on counts. Medium on types: classification is by title only |
| **Main positions** | Most commenters asked for the rule to be narrowed or withdrawn. The main targets:<br>– the **personal-investment-advisor-as-donor-advisor** rule, which makes adviser fees paid from the DAF an automatic excess benefit;<br>– the **broad "distribution"** definition, with no administrative-expense carve-out;<br>– the **broad DAF definition**, which sweeps in field-of-interest, fiscal-sponsorship and similar funds.<br>Fidelity Charitable opposed the adviser rule and asked for prospective effect [[S04](https://www.fidelitycharitable.org/articles/proposed-donor-advised-fund-regulations.html)]. Community foundations argued the rule favours national sponsors [[S02](https://www.morganlewis.com/pubs/2024/05/irs-holds-two-day-hearing-on-proposed-donor-advised-fund-regulations)]. Reform advocates (IPS authors writing in NPQ) supported it [[S03](https://nonprofitquarterly.org/tax-rules-investment-houses-and-donor-advised-funds-whats-at-stake/)]. **Personal benefit (§4967) was not proposed in 2023**; the NPRM covers §4966 only [[P01](https://www.govinfo.gov/content/pkg/FR-2023-11-14/html/2023-24982.htm)]. | Medium: individual letters were not read |
| **Status 2026** | **Still proposed. Not final, not withdrawn.**<br>– 2025–26 PGP (Sept 30, 2025): item 35, "Final regulations under §4966", listed under **Deregulation and Burden Reduction** [[P02](https://www.irs.gov/pub/irs-counsel/2025-2026-initial-pgp.pdf)].<br>– 2026–27 PGP (Sept 29, 2026): Tax Exempt Organizations item 4, "Guidance under §§4966 and 6033 regarding certain donor advised fund arrangements" [[P03](https://www.irs.gov/pub/irs-counsel/2026-2027-initial-pgp.pdf)].<br>– The API shows no final rule [[A2](https://api.regulations.gov/v4/documents?filter[searchTerm]=donor%20advised%20fund%204966&filter[agencyId]=IRS)]. | High |
| **2. Lobbying (LDA 2021–2026 Q3)** | **33 clients** filed 359 reports whose issue text names DAFs, the ACE Act or H.R. 2891/S. 3975 [C; [A3](https://lda.gov/api/v1/filings/?filing_specific_lobbying_issues=donor%20advised)].<br>**Sponsors as LDA clients:** Vanguard Charitable (K&L Gates; $1.74m over 24 filings); NPT (Miller & Chevalier, CM Strategic; $1.09m); Fidelity Charitable (FMR LLC in-house; $180k; "Donor advised funds regulation" from Q4 2023); AEF and Ren (both **first registered in 2024**, after the NPRM); NCF (2025–26).<br>**Associations:** the Community Foundation Awareness Initiative is the biggest DAF-specific spender ($3.33m across 19 DAF-mentioning filings); Council on Foundations ($1.2m); Philanthropy Roundtable ($1.38m outside firms plus $1.79m self-filed).<br>**Not found as LDA clients:** Schwab Charitable/DAFgiving360, Daffy, Morgan Stanley GIFT, Goldman Sachs Philanthropy Fund. Charles Schwab Corp. named the ACE Act once (Q1 2022).<br>**Issues named:** ACE Act (2021–23); Charitable Act/non-itemizer; P.L. 119-21; QCD-to-DAF (2025–26); the §4966 proposal (Fidelity, AFP, SIFMA, Global Generosity).<br>Amounts are **whole-filing totals, not DAF-specific**. | High that the filings exist. Medium on coverage: the keyword search misses filings that do not name DAFs |
| **3. OBBBA (P.L. 119-21) from 2026** | All four provisions apply to tax years beginning after Dec 31, 2025 [[P04](https://www.govinfo.gov/content/pkg/PLAW-119publ21/html/PLAW-119publ21.htm)]:<br>– **§70424:** non-itemizer deduction of $1,000/$2,000, permanent. Cash only; **gifts to DAFs and supporting organizations do not qualify** [[P05](https://www.irs.gov/newsroom/irs-reminder-permanent-charitable-contribution-deduction-begins-for-returns-filed-next-year-for-taxpayers-who-do-not-itemize)].<br>– **§70425:** 0.5% contribution-base floor for itemizers. Floor-disallowed amounts carry forward only from years in which a percentage limit is exceeded. The 60% cash limit is made permanent.<br>– **§70111:** new §68 cuts *all* itemized deductions by 2/37 for the top bracket, which in effect caps their value at 35%.<br>– **§70426:** corporate 1% floor, inside the 10% cap.<br>**Bunching evidence (2025):**<br>– Fidelity Charitable: accounts +13.4% to 246,006 "as some donors took advantage of strategies like bunching" [[P06](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf)].<br>– InvestmentNews on DAFgiving360: "many donors accelerated contributions into 2025" [[S08](https://www.investmentnews.com/practice-management/dafgiving360-donors-boost-2025-grants-to-nearly-10b/264994)].<br>– Giving USA 2026 (via press): about $1.71bn of individual giving accelerated into late 2025, much of it likely into DAFs and foundations [[S09](https://philanthropydaily.com/the-bequest-economy-the-driving-force-behind-americas-giving-boom/)].<br>– **No sponsor has published 2025 contribution totals split by month, or any 2026 contribution data.** | High on the law. Low to medium on behaviour: these are sponsor narratives, not measured shifts |

---

## 1. The 2023 proposed regulations (REG-142338-07)

### 1.1 Docket facts [F, P]

- **Docket:** IRS-2023-0053. Title: "Taxes on Taxable Distributions From Donor Advised Funds Under Section 4966 (REG-142338-07)". RIN 1545-BI33. Docket last modified 2026-06-15 [[A4](https://api.regulations.gov/v4/dockets/IRS-2023-0053)].
- **NPRM:** IRS-2023-0053-0001 (FR 2023-24982, Nov 14, 2023). The comment window in the API is 2023-11-14 to 2024-02-16T04:59:59Z, which is Feb 15, 2024 at 11:59 pm ET. That matches the extension in FR 2024-00260 [[A2](https://api.regulations.gov/v4/documents?filter[searchTerm]=donor%20advised%20fund%204966&filter[agencyId]=IRS)].
- **Other documents in the docket:**
  - Hearing notices: FR 2024-04262 (Feb 29, 2024) and FR 2024-08419 (Apr 19, 2024).
  - Hearing agenda (IRS-2023-0053-0239), posted Apr 29, 2024.
  - **No final rule and no withdrawal.** The only newer IRS match for the search terms is the "Trump Accounts" rule, IRS-2026-1321-0002 (Oct 1, 2026), which sits in a different docket.
- **Earlier record:** the NPRM preamble says the 2006–2017 notices drew 118 comments, 74 of them on DAFs and taxable distributions [[P01](https://www.govinfo.gov/content/pkg/FR-2023-11-14/html/2023-24982.htm)]. **Do not confuse these with the 2023–24 comments.**

### 1.2 How many comments? [C on A1]

| Measure | Count | Note |
|---|---:|---|
| Public submissions posted (all dates) | **249** | `totalElements` from the comments endpoint, 2026-11-15. None withdrawn. Documents run from -0002 to -0254; the gaps are agency documents |
| Posted by 2024-02-22 (comment period, including late posting of letters received by Feb 15) | 173 | Posting date is not receipt date. One spot check (AEF -0201) was received Apr 5 and posted Apr 9, 2024 |
| Posted 2024-02-23 to 2024-05-13 (mostly hearing requests and outlines) | 63 | e.g. -0238 TEGE Council "Outline of Testimony", subtype Public Hearing/Meeting; -0201 AEF "outline of topics … for the public hearing on May 6, 2024" |
| **Posted 2026-05-13 to 2026-06-15** | **13** | Subtype "Public Comment", attached to the NPRM or the correction document. Received and posted the same day (spot checks -0242, -0244, -0250) |
| Distinct submitter titles after simple normalization, excluding "Anonymous" | 183 | **Upper bound on distinct submitters.** Variants such as "ABA" and "American Bar Association" are not merged |
| Distinct community foundations | 54–56 | 54 if "MCF" means Madison Community Foundation (our inference from "Bob Sorge") |
| Distinct national sponsors | 11 | AEF, Fidelity Charitable, Schwab Charitable, Vanguard Charitable, NPT, RCF, Morgan Stanley GIFT, U.S. Charitable Gift Trust, iGiftFund, ImpactAssets, Impact Investing Charitable Foundation |
| Secondary snapshots | ">150 organizations" (Morgan Lewis, 2024-05-08); 179 (NPQ, 2024-04-03); 47 and 158 (Federal Register page captures; SS) | Snapshots on different dates. Use the API count |

**Hearing.** May 6–7, 2024. Morgan Lewis counts **34 in-person speakers** [[S02](https://www.morganlewis.com/pubs/2024/05/irs-holds-two-day-hearing-on-proposed-donor-advised-fund-regulations)], consistent with the repo's ">30" [S08 in the regulation note].

### 1.3 Commenter-type breakdown [C; classification by title]

Postings (n = 249). A single organization often filed both a letter and a hearing outline.

| Commenter type | All postings | Comment period | Hearing phase 2024 | 2026 batch |
|---|---:|---:|---:|---:|
| Community foundation | 77 | 52 | 24 | 1 |
| Individual (named) | 32 | 28 | 4 | 0 |
| Anonymous | 5 | 5 | 0 | 0 |
| CF or philanthropy association (CoF, CFAI, regional associations, JFNA) | 29 | 22 | 6 | 1 |
| National DAF sponsor | 24 | 14 | 6 | 4 |
| Professional body (ABA sections, AICPA, ACTEC, NYSBA, TEGE Council) | 17 | 6 | 8 | 3 |
| Law firm or attorney | 15 | 8 | 5 | 2 |
| Faith or single-issue sponsor (NCF, Signatry, JCF, WaterStone…) | 13 | 9 | 4 | 0 |
| Financial industry (SIFMA, RIAs, Northern Trust) | 10 | 8 | 1 | 1 |
| Fiscal sponsor or other public charity | 8 | 6 | 2 | 0 |
| Nonprofit-sector association | 7 | 6 | 1 | 0 |
| Advocacy or policy group (Philanthropy Roundtable, U.S. Impact Investing Alliance, DAF Policy Network, Sustainable Economies Law Center) | 6 | 5 | 1 | 0 |
| DAF platform vendor (Ren) | 2 | 1 | 0 | 1 |
| Unclassified (FAOG, FPLG, Faith & Giving, Telling Queer History) | 4 | 3 | 1 | 0 |

**Academics.** No submission title names a university or academic affiliation. Some of the 32 named individuals may be academics, but titles do not show it [I]. IPS reform authors argued their case in NPQ, but we found no IPS-titled submission in the docket [C; [S03](https://nonprofitquarterly.org/tax-rules-investment-houses-and-donor-advised-funds-whats-at-stake/)]. **Reform-side voices are close to absent from the posted record** [I]: of the four advocacy titles, only the U.S. Impact Investing Alliance and the Sustainable Economies Law Center are not sponsor-aligned or donor-freedom groups, and their positions are unread.

### 1.4 Main positions by issue

What the proposal said is quoted from the NPRM [P01]. Positions come from secondary summaries and sponsor pages, because the letters themselves could not be opened.

| Issue | What the NPRM proposed [F, P01] | Opposing positions (who) | Supporting positions (who) |
|---|---|---|---|
| **Definition of DAF and advisory privileges** | Broad definition, including advisory privileges deemed to exist from a donor-advisor relationship and an anti-abuse rule | Community foundations objected to the "broad definition of 'DAF'". It would reclassify field-of-interest and other collaborative funds, funds that grant to individuals, and funds that work with for-profit companies [[S02](https://www.morganlewis.com/pubs/2024/05/irs-holds-two-day-hearing-on-proposed-donor-advised-fund-regulations)]. Nonprofit New York warned it may sweep in "virtually all fiscal sponsorship arrangements" (SS). Opponents said barring board members from giving to single-entity DAFs would "chill vital charitable giving" [[S03](https://nonprofitquarterly.org/tax-rules-investment-houses-and-donor-advised-funds-whats-at-stake/)] | IPS authors: the rules clarify useful definitions, and they want more, such as a payout rule [[S03](https://nonprofitquarterly.org/tax-rules-investment-houses-and-donor-advised-funds-whats-at-stake/)] |
| **Investment adviser as donor-advisor** | A personal investment advisor who manages both the DAF and the donor's personal assets "would be a donor-advisor … while serving in that dual capacity". Exception: services to the sponsor "as a whole", with fees charged uniformly. Treasury flagged that a "counterincentive may be created … to not advise distributions out of their DAFs" | Most comments focused on this rule (NPQ). Sponsors said it would "upend a widely accepted and decades-long investment management practice". The Dayton Foundation said most of its $545m in DAF assets are managed by donors' advisers [[S03](https://nonprofitquarterly.org/tax-rules-investment-houses-and-donor-advised-funds-whats-at-stake/)]. Fidelity Charitable: "Investment advisors provide a service to and on behalf of the sponsoring organization" [[S04](https://www.fidelitycharitable.org/articles/proposed-donor-advised-fund-regulations.html)]. Some asked to strike the rule as inconsistent with the statute. Others proposed a written agreement plus sponsor oversight as a safe harbour. Community foundations said the rule favours national sponsors, which can buy investment advice more cheaply [[S02](https://www.morganlewis.com/pubs/2024/05/irs-holds-two-day-hearing-on-proposed-donor-advised-fund-regulations)] | IPS (NPQ) supported the proposal overall |
| **Fees and the definition of "distribution"** | "Reasonable investment and grant-related fees paid from DAF assets generally would not be considered distributions". An unreasonable fee would be a deemed distribution. No general administrative-expense carve-out | Most commenters wanted an administrative-expense exception, and some wanted the §4945 "grant" definition [[S02](https://www.morganlewis.com/pubs/2024/05/irs-holds-two-day-hearing-on-proposed-donor-advised-fund-regulations)]. Fidelity: the definition "should not reach reasonable expenses supporting a sponsoring organization's charitable mission". It warned of fee rises across accounts [[S04](https://www.fidelitycharitable.org/articles/proposed-donor-advised-fund-regulations.html)] | Not found |
| **Personal benefit (§4967), tickets, pledges** | **Not proposed.** The preamble recalls that Notice 2017-73 floated §4967 rules on tickets and pledges, but the 2023 NPRM covers §4966 only. The repo's earlier §4958 and §4967 PGP items were dropped from the 2025–26 plan | Not applicable. Some commenters asked for consultation before any re-proposal [[S02](https://www.morganlewis.com/pubs/2024/05/irs-holds-two-day-hearing-on-proposed-donor-advised-fund-regulations)] | Not applicable |
| **Effective date and process** | Would apply to taxable years ending on or after final publication | Fidelity called the effective date unusual and asked for prospective rules with a "reasonable transition period". Several asked for withdrawal and re-proposal, citing a "chilling effect" [[S02](https://www.morganlewis.com/pubs/2024/05/irs-holds-two-day-hearing-on-proposed-donor-advised-fund-regulations),[S04](https://www.fidelitycharitable.org/articles/proposed-donor-advised-fund-regulations.html)] | Not found |

**[I] What the 2026 batch suggests.** Thirteen fresh submissions arrived on the 2023 docket in May–June 2026. Most are adviser-channel sponsors and their counsel (AEF, RCF, Ren, SIFMA, Adler & Colvin, ABA and NYSBA tax sections). The 2026–27 PGP then re-framed the item, on Sept 29, 2026, as guidance on "certain donor advised fund arrangements" under §§4966 and 6033. One reading is a targeted project, perhaps on adviser-managed DAF arrangements plus Form 990 reporting. That reading is consistent with the repo's Q-B09 interpretation, but unconfirmed: **the 2026 letters were not readable** (downloads.regulations.gov is blocked).

### 1.5 Status as of 2026-11-15 [F]

| Item | Text | Source |
|---|---|---|
| 2025–26 PGP (Sept 30, 2025), Deregulation and Burden Reduction, item 35 | "Final regulations under §4966 regarding donor advised funds, including excise taxes on sponsoring organizations and fund management. Proposed regulations were published on November 14, 2023." | [[P02](https://www.irs.gov/pub/irs-counsel/2025-2026-initial-pgp.pdf)] |
| 2026–27 PGP (Sept 29, 2026), Tax Exempt Organizations, item 4 | "Guidance under §§4966 and 6033 regarding certain donor advised fund arrangements." Item 5 is §6033 reporting, including fiscal sponsorship | [[P03](https://www.irs.gov/pub/irs-counsel/2026-2027-initial-pgp.pdf)] |
| Federal Register / regulations.gov | No final rule and no withdrawal (API search, 2026-11-15) | [[A2](https://api.regulations.gov/v4/documents?filter[searchTerm]=donor%20advised%20fund%204966&filter[agencyId]=IRS)] |
| Unified Agenda | A secondary source reports a July 2026 target for finalization (SS). We did not reach reginfo.gov's rule page; the Fall 2025 and Spring 2025 queries returned no DAF text | SS only |
| Council on Foundations | Filed a comment on the 2026 PGP (Notice 2026-23) asking for final DAF regulations (SS, cof.org PDF dated 2026-05; not opened) | SS |

---

## 2. Federal lobbying on DAF issues (LDA, 2021 – 2026 Q3)

### 2.1 Method [C]

- **Queries:** lda.gov `filings` endpoint, `filing_specific_lobbying_issues` = "donor advised", "donor-advised", "DAF", "Accelerating Charitable Efforts", "Charitable Rollover Facilitation", "2891" and "3975". We also ran per-client queries for 18 sponsors, vendors and associations.
- **Duplicates:** the API returns one row per matching activity, so the same filing can appear more than once on a page. We de-duplicated by `filing_uuid`.
- **Filters:**
  - Kept filings whose issue text matches the DAF, ACE or QCD-to-DAF pattern.
  - Dropped "DAF" meaning Department of the Air Force (3 clients) and H.R. 2891 of the 118th Congress (SAFE Banking).
  - Where an amendment exists, kept the latest version per registrant, client, year and period.
- **Result:** **359 filings, 33 clients**. By filing year: 2021: 63; 2022: 68; 2023: 44; 2024: 73; 2025: 57; 2026: 54. The 20 rows matched only on the QCD-to-DAF bill are included in the 2025 and 2026 counts.
- **Amounts:**
  - Reported **income** (outside firms) or **expenses** (self-filers) for the whole filing, covering all issues. They are not DAF-specific.
  - LDA rounds to $10,000. Blank means under $5,000 or a registration.
  - Self-filer amounts such as AICPA, SIFMA, UBS, Schwab Corp. and KPMG are organization-wide, so the DAF share is a small, unknown fraction [I].
- **Coverage limit:** filings that lobby on DAFs without naming them, such as "charitable giving" or "philanthropic sector", are missed. Example: Council on Foundations' self-filed 2025–26 reports name H.R. 2891 but not "donor advised", so they were captured only through the bill query.

### 2.2 DAF sponsors and vendors that lobby [F, P; sums C]

| Client | Registrant(s) | Years | Filings in CSV | Sum of reported amounts | DAF issue text (abridged) |
|---|---|---|---:|---:|---|
| **Vanguard Charitable** | K&L Gates | 2021–26 | 24 | $1.74m | "Issues related to donor-advised funds"; S. 1981 / H.R. 6595 ACE Act (2021–23); P.L. 119-21 "issues related to tax-exempt organizations" (2025 Q4); H.R. 2891 (2025–26); H.R. 8783 (2026 Q2: $130k, the highest quarter) |
| **National Philanthropic Trust** | Miller & Chevalier; CM Strategic | 2021–26 | 25 | $1.09m | "Legislative and regulatory tax issues relating to … donor-advised funds"; ACE Act; Charitable Act; "H.R. 1 (Public Law 119-21)"; S. 3975/H.R. 2891 (2026 Q2) |
| **Fidelity Charitable Gift Fund** | FMR LLC (in-house) | 2021–26 | 17 | $180k | "Donor advised funds" + ACE Act (2021–22). **"Donor advised funds regulation"** from 2023 Q4 to 2025 Q1 and 2026 Q2. No activity in 2025 Q2–Q4, 2026 Q1 or 2026 Q3 |
| **American Endowment Foundation** | Tiger Hill Partners | **2024–26 (first registered 2024)** | 13 | $370k | "Issues related to charitable contributions and donor advised funds" |
| **Ren** / **Ren Acquisition Co.** | Integer LLC / Tiger Hill Partners | **2024–26** | 12 + 6 | $370k + $230k | "Donor-advised funds"; "charitable contributions and donor advised funds" |
| **National Christian Foundation** | Integer LLC | 2025–26 | 8 | $105k | "Donor-advised funds and charitable giving" |
| Greater Washington CF; NY Community Trust | Van Scoyoc | 2021–26; 2023–26 | 23; 9 | $240k; $90k | "Tax policy … community foundations; … Donor Advised Funds (DAFs)" |
| GoFundMe (sponsor of GoFundMe Giving Funds) | Van Scoyoc | 2026 | 4 | $80k | "Tax policy and regulations related to Donor Advised Funds (DAFs)" |
| UBS Americas | self | 2024–26 | 11 | $1.47m (org-wide) | "… and Donor Advised Funds" within a tax list |
| Charles Schwab Corp. | self | 2022 Q1 | 1 | $530k (org-wide) | "H.R. 6595, Accelerating Charitable Efforts Act" |
| Edward Jones; Ameriprise; Thrivent | Davis & Harman; self | 2025–26 | 4; 3; 4 | org-wide | "qualified charitable distributions to donor advised funds"; H.R. 2891 |

**Not found as LDA clients in 2021–26 (per-client query, zero results):** Schwab Charitable / DAFgiving360 / Donor Advised Charitable Giving; Renaissance Charitable Foundation (lobbying appears under "Ren"); Daffy; Goldman Sachs Philanthropy Fund; Morgan Stanley GIFT. "Chariot" and "Foundation Source" matched unrelated clients.

### 2.3 Associations, advocacy groups and professional bodies

| Client | Filings | Sum | Main DAF issue lines |
|---|---:|---:|---|
| **Community Foundation Awareness Initiative** (informal coalition; Van Scoyoc) | 19 | $3.33m (DAF-mentioning filings only; $4.02m across all 2021–26 quarterly filings) | "Rules regarding donor-advised funds"; ACE Act (2021–22); "Donor Advised Funds (DAFs) H.R.2891/S.3975"; "Public Law 119-21 … Charitable tax issues" |
| **Council on Foundations** (Akin Gump, Federal Policy Group, S-3 Group; self-files from 2025) | 30 | $1.2m | "donor-advised funds; private foundations …"; ACE Act (2021–22); H.R. 2891/S. 3975 and P.L. 119-21 (2025–26) |
| **Philanthropy Roundtable** (outside: Miller & Chevalier, Article One, Jean Marie; self from 2023) | 43 + 14 | $1.38m + $1.79m | "Tax policy relating to donor-advised funds, private foundations"; ACE Act; donor privacy; H.R. 1 (P.L. 119-21) |
| Jewish Federations of North America (self + Miller & Chevalier) | 17 + 11 | org-wide | "Charitable tax and donor advised fund issues"; ACE Act; Charitable Act |
| Association of Fundraising Professionals | 11 | $80k | 2024: "Providing comments to Treasury raising questions with new regulations impacting donor-advised funds (DAFs)" |
| SIFMA (self) | 2 | org-wide | 2023 Q4 – 2024 Q1: "IRS proposed rule regarding Section 4966 Donor Advised Funds" |
| AICPA; KPMG | 6; 1 | org-wide | "Exempt organization issues, including donor-advised funds"; OBBBA implementation |
| Global Generosity, Inc. | 9 | $30k | "proposed regulations covering donor advised funds (DAFs)"; "benefits of donor advised funds (DAFs) for faith-based charities" |
| Others: United Philanthropy Forum, CASE, American Heart Association, Independent Sector, Americans for Tax Reform, Philanthropy Southwest, one individual (ACE Act 2021) | — | — | Mostly the universal-deduction bill text "eliminate the current exclusion of gifts to donor-advised funds" (2021–22), or the ACE Act |

### 2.4 Readings [I]

- **ACE Act era (2021–Q1 2023).** Every major sponsor and association lobbying file names S. 1981 / H.R. 6595. The bill numbers disappear after the 117th Congress, consistent with the repo's "never reintroduced" finding.
- **Proposed-rule era (Q4 2023–2025).**
  - Fidelity's issue line changes to "Donor advised funds regulation".
  - SIFMA, AFP and Global Generosity name the proposed rule.
  - **AEF and Ren register lobbyists for the first time in 2024**, and Ren Acquisition hires a second firm. These are the adviser-channel sponsors and the vendor most exposed to the personal-investment-advisor rule. Timing alone does not prove motive.
- **OBBBA era (2025–26).**
  - NPT, Vanguard Charitable, CoF and CFAI name P.L. 119-21. No filing states a position on the DAF exclusion from the non-itemizer deduction.
  - The live DAF bill is **QCD-to-DAF (H.R. 2891 / S. 3975)**. Vanguard, NPT, CFAI, CoF, United Philanthropy Forum, JFNA, Edward Jones, Ameriprise and Thrivent name it.
- **Treasury/IRS as targets.** 138 of 359 filings list Treasury or IRS as a contacted entity. That includes NPT (24 of 25), Ren (11 of 12), AEF (8 of 13) and Philanthropy Roundtable outside firms (25 of 43). Vanguard Charitable's and CoF's filings list only Congress.

---

## 3. OBBBA (P.L. 119-21, signed July 4, 2025): charitable provisions effective 2026

### 3.1 Statute [F, P04 unless noted]

| Provision | Section of P.L. 119-21 → IRC | Mechanics | DAF relevance |
|---|---|---|---|
| Non-itemizer deduction | §70424 → §170(p) | Strikes "$300 ($600" and inserts "$1,000 ($2,000"; drops the 2021-only limit; permanent | IRS: "Cash contributions made either to supporting organizations or to establish or maintain a donor advised fund do not qualify" [[P05](https://www.irs.gov/newsroom/irs-reminder-permanent-charitable-contribution-deduction-begins-for-returns-filed-next-year-for-taxpayers-who-do-not-itemize), IR-2026-135, Nov 10, 2026]. The exclusion carries over from the existing §170(p) definition; the 2025 Act does not mention DAFs |
| 0.5% floor (individual itemizers) | §70425 → new §170(b)(1)(I); §170(d)(1)(C) | Contributions are allowed only to the extent the aggregate exceeds 0.5% of the contribution base. The floor is applied first to the most restricted categories. **Floor-disallowed amounts carry forward only from years in which a percentage limit is exceeded.** The 60% cash limit is made permanent (§170(b)(1)(G)(i)) | Rewards concentrating gifts into one year: bunching. A DAF is the usual vehicle for bunching [I] |
| 35% value cap | §70111 → new §68 | Itemized deductions are reduced by 2/37 of the lesser of (1) itemized deductions or (2) taxable income above the start of the 37% bracket. Applied after other limits. Covers **all** itemized deductions, not only charitable ones (consistent with Thomson Reuters [[S10](https://tax.thomsonreuters.com/news/charitable-deduction-unpacked-individual-itemizers/)]) | Makes 2025 gifts worth up to 37 cents per dollar and 2026+ gifts worth 35 cents for top-bracket donors. This drove the pre-funding advice in 2025 |
| Corporate 1% floor | §70426 → §170(b)(2)(A); §170(d)(2) | Deductible only to the extent contributions exceed 1% of taxable income, up to the 10% cap. Floor-disallowed amounts carry forward only from years in which the 10% cap is exceeded. 5-year carryforward | Corporate DAFs and corporate-sponsored programs, e.g. workplace giving [I] |
| Effective date (all four) | — | Taxable years beginning after Dec 31, 2025 | — |

### 3.2 Evidence of 2025 bunching or timing shifts

| Source | What it says | Grade | What it does not show |
|---|---|---|---|
| Fidelity Charitable, 2026 Giving Report (PDF) | "The number of Fidelity Charitable donor-advised funds grew by 13.4% to 246,006, as some donors took advantage of strategies like bunching donations in the face of tax law changes that took effect in 2026." Grants: $18.3bn (+23%). 69% of contributions were non-cash [[P06](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf)] | P (sponsor) | No total for 2025 contributions, and no monthly or Q4 split. The web page omits the bunching sentence ([page](https://www.fidelitycharitable.org/insights/2026-giving-report.html)) |
| DAFgiving360 CY2025 results, via InvestmentNews (Jan 27, 2026) | "In the run-up to changes under the One Big Beautiful Bill Act, many donors accelerated contributions into 2025." Grants $9.9bn (+28%); a record 74% of contributions non-cash [[S08](https://www.investmentnews.com/practice-management/dafgiving360-donors-boost-2025-grants-to-nearly-10b/264994)] | S. The sponsor press release itself is at [businesswire](https://www.businesswire.com/news/home/20260127969044/en/DAFgiving360-Donors-Grant-Nearly-%2410-Billion-to-Charities-in-Most-Active-Year-on-Record) (not opened) | No contribution totals |
| Vanguard Charitable CY2025 (Mar 2026) | $3.9bn of grants (+27%). "More than a quarter of the grants were made between November 1 and December 31" [[S11](https://www.mychesco.com/a/news/business/vanguard-charitable-reports-3-9-billion-in-grants-to-nonprofits-in-2025/)]. A Kiplinger article attributes higher year-end giving partly to "getting ahead of these changes" (SS; the page did not render) | S | This is grant timing, not contribution timing |
| Giving USA 2026 (via Philanthropy Daily, Jul 17, 2026) | "an estimated $1.71 billion in individual giving was accelerated into late 2025 to maximize tax advantages". J. Bergdoll (IU Lilly School) says much of it likely went into "intermediary vehicles such as donor-advised funds (DAFs) and private foundations" [[S09](https://philanthropydaily.com/the-bequest-economy-the-driving-force-behind-americas-giving-boom/)] | S (Giving USA report not read) | DAF share not quantified |
| Bloomberg Tax, "Wealthy Americans Speed Donations Ahead of GOP Tax Law Limits" | Title only (paywall) [[S12](https://news.bloombergtax.com/daily-tax-report/wealthy-americans-speed-donations-ahead-of-gop-tax-law-limits)] | SS | — |
| NPT, "What Tax Reform Means for Charitable Giving in 2026" (Jul 1, 2026) | Advice only ("bundle" contributions); no NPT data [[S13](https://www.nptrust.org/?p=12140)] | S | — |
| Adviser and law-firm guidance (Lowenstein, Jul 16, 2025; Haynes Boone, Oct 22, 2025) | Recommend accelerating 2025 gifts, directly or through a DAF [[S14](https://www.lowenstein.com/news-insights/publications/client-alerts/obbba-provisions-impact-charitable-contribution-deductions-te),[S15](https://www.haynesboone.com/news/alerts/one-big-beautiful-bill-revamps-charitable-giving-tax-rules-for-2026-and-beyond.pdf)] | S | This is advice, not observed behaviour |

**[I] Reading.**
- Two of the three largest sponsors attribute part of their 2025 growth to tax-driven acceleration or bunching: Fidelity directly, and DAFgiving360 as reported by InvestmentNews.
- Giving USA's estimate of the acceleration (~$1.71bn) is small against $617bn of total giving.
- **No sponsor has published 2025 contribution totals by month, or any 2026 contribution figure.** The test of a 2026 pull-back (a "hangover" year) needs CY2026 sponsor reports (Jan–Mar 2027) or Form 990 Schedule D for FY2026, which arrives in late 2027.
- The non-itemizer exclusion matters little to DAF sponsors' assets, but it shapes small-donor marketing: a $1,000 cash gift to a DAF earns no deduction for a non-itemizer, while the same gift made directly to a charity does.

---

## 4. Gaps and caveats

1. **Comment letters unread.** downloads.regulations.gov is blocked, so positions by named commenter are limited to sponsor pages and summaries. The 13 letters from 2026 are the most decision-relevant unread documents.
2. **Commenter types are assigned from titles.** "DAF Policy Network", "FAOG", "FPLG" and "Faith & Giving" are unidentified. "CF" and "MCF" in 2026 are inferred.
3. **LDA keyword coverage.** Filings that do not name DAFs or the specific bills are missed. Amounts are per filing, not per issue.
4. **No 2026 behavioural data.**
5. **Unified Agenda target** not verified on reginfo.gov.

## 5. Proposed corrections to repo text (not governing until validated)

1. **queue-batch38-closeout-checks.md §8, P-ANL-10, first bullet.**
   - **Append:** "The report PDF (p. 4, Key findings) says DAF count grew 13.4% to 246,006 'as some donors took advantage of strategies like bunching donations in the face of tax law changes that took effect in 2026'. It names the tax changes but not OBBBA or the 0.5% floor [batch 39 n1]."
2. **regulation-market-structure-portability.md Q-B09 §1.**
   - **Add:** "Docket IRS-2023-0053 holds 249 posted public submissions (API, 2026-11-15), including 13 new submissions posted May 13 – Jun 15, 2026 (AEF, RCF, Ren, SIFMA, ABA, NYSBA, Adler & Colvin, Kallina, 'CF', 'MCF') [batch 39 n1]."
3. **regulation-market-structure-portability.md Q-B09 §2 table, 2025–26 row.**
   - **Replace "(fall 2025)" with:** "(Sept 30, 2025; item 35 under Deregulation and Burden Reduction; IRS PDF read)."

---

## Source register

| ID | Source | Date | URL | Grade |
|---|---|---|---|---|
| A1 | regulations.gov API v4, comments in docket IRS-2023-0053 (page size 250; 249 records) | queried 2026-11-15 | https://api.regulations.gov/v4/comments?filter[docketId]=IRS-2023-0053 | P |
| A2 | regulations.gov API v4, IRS documents matching "donor advised fund 4966" | queried 2026-11-15 | https://api.regulations.gov/v4/documents?filter[searchTerm]=donor%20advised%20fund%204966&filter[agencyId]=IRS | P |
| A3 | lda.gov API, filings search (issue text and client-name queries) | queried 2026-11-15 | https://lda.gov/api/v1/filings/?filing_specific_lobbying_issues=donor%20advised | P |
| A4 | regulations.gov API v4, docket record IRS-2023-0053; comment detail spot checks -0201, -0238, -0242, -0244, -0250 | queried 2026-11-15 | https://api.regulations.gov/v4/dockets/IRS-2023-0053 | P |
| P01 | Federal Register 2023-24982, NPRM text (govinfo HTML) | 2023-11-14 | https://www.govinfo.gov/content/pkg/FR-2023-11-14/html/2023-24982.htm | P |
| P02 | Treasury/IRS 2025–2026 Priority Guidance Plan | 2025-09-30 | https://www.irs.gov/pub/irs-counsel/2025-2026-initial-pgp.pdf | P |
| P03 | Treasury/IRS 2026–2027 Priority Guidance Plan | 2026-09-29 | https://www.irs.gov/pub/irs-counsel/2026-2027-initial-pgp.pdf | P |
| P04 | Public Law 119-21 (govinfo HTML), §§70111, 70424–70426 | 2025-07-04 | https://www.govinfo.gov/content/pkg/PLAW-119publ21/html/PLAW-119publ21.htm | P |
| P05 | IRS IR-2026-135, non-itemizer deduction reminder | 2026-11-10 | https://www.irs.gov/newsroom/irs-reminder-permanent-charitable-contribution-deduction-begins-for-returns-filed-next-year-for-taxpayers-who-do-not-itemize | P |
| P06 | Fidelity Charitable, 2026 Giving Report (PDF) | 2026 | https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf | P (sponsor) |
| S02 | Morgan Lewis, "IRS Holds Two-Day Hearing on Proposed DAF Regulations" | 2024-05-08 | https://www.morganlewis.com/pubs/2024/05/irs-holds-two-day-hearing-on-proposed-donor-advised-fund-regulations | S |
| S03 | Nonprofit Quarterly (Collins & Flannery, IPS), "Tax Rules, Investment Houses, and DAFs: What's at Stake" | 2024-04-03 | https://nonprofitquarterly.org/tax-rules-investment-houses-and-donor-advised-funds-whats-at-stake/ | S |
| S04 | Fidelity Charitable, "Proposed Donor-Advised Fund Regulations" (comment-letter summary) | updated 2024-02-23 | https://www.fidelitycharitable.org/articles/proposed-donor-advised-fund-regulations.html | S (sponsor) |
| S08 | InvestmentNews, "DAFgiving360 donors boost 2025 grants to nearly $10B" | 2026-01-27 | https://www.investmentnews.com/practice-management/dafgiving360-donors-boost-2025-grants-to-nearly-10b/264994 | S |
| S09 | Philanthropy Daily (W. Nardi), "The Bequest Economy" (Giving USA 2026 figures) | 2026-07-17 | https://philanthropydaily.com/the-bequest-economy-the-driving-force-behind-americas-giving-boom/ | S |
| S10 | Thomson Reuters Tax, "Charitable deduction unpacked" | 2025-12-02 | https://tax.thomsonreuters.com/news/charitable-deduction-unpacked-individual-itemizers/ | S |
| S11 | MyChesCo, "Vanguard Charitable Reports $3.9 Billion in Grants … in 2025" | 2026-03-09 | https://www.mychesco.com/a/news/business/vanguard-charitable-reports-3-9-billion-in-grants-to-nonprofits-in-2025/ | S |
| S12 | Bloomberg Tax, "Wealthy Americans Speed Donations Ahead of GOP Tax Law Limits" | 2025 | https://news.bloombergtax.com/daily-tax-report/wealthy-americans-speed-donations-ahead-of-gop-tax-law-limits | SS |
| S13 | NPT, "What Tax Reform Means for Charitable Giving in 2026" | 2026-07-01 | https://www.nptrust.org/?p=12140 | S |
| S14 | Lowenstein Sandler, "OBBBA Provisions Impact Charitable Contribution Deductions" | 2025-07-16 | https://www.lowenstein.com/news-insights/publications/client-alerts/obbba-provisions-impact-charitable-contribution-deductions-te | S |
| S15 | Haynes Boone, "One Big Beautiful Bill Revamps Charitable Giving Tax Rules for 2026 and Beyond" | 2025-10-22 | https://www.haynesboone.com/news/alerts/one-big-beautiful-bill-revamps-charitable-giving-tax-rules-for-2026-and-beyond.pdf | S |
| R01 | Repo: regulation-market-structure-portability.md Q-B09 (status, PGP, OBBBA) | 2026-11-14 | regulation-market-structure-portability.md | R |
| R02 | Repo: industry-incentives-structural-analysis.md §3.4–3.5 with wave 2B (deadline Feb 15, 2024) | 2026-11-14 | industry-incentives-structural-analysis.md | R |

---

## Data dictionary

### `daf-regs-2023-comments-summary.csv` (249 rows, one per posted submission)

| Column | Meaning |
|---|---|
| document_id | regulations.gov document ID (IRS-2023-0053-NNNN) |
| posted_date | Posting date from the API (YYYY-MM-DD). Not the receipt date |
| phase_by_posted_date | `comment_period_2023-24` (posted ≤ 2024-02-22), `hearing_requests_outlines_2024` (2024-02-23 to 2024-05-13) or `post-hearing_2026` (2026) |
| submitter_as_titled | Document title with "Comment from " removed |
| commenter_type | Our classification from the title: community_foundation, national_daf_sponsor, single_issue_faith_daf_sponsor, cf_or_philanthropy_association, nonprofit_sector_association, fiscal_sponsor_or_other_public_charity, professional_body, law_firm_or_attorney, financial_industry, advocacy_or_policy_group, daf_platform_vendor, individual_named, anonymous, other_or_unclassified |
| withdrawn | API withdrawn flag (all False) |
| regulations_gov_url | Public page for the submission (not fetched; robots.txt unreadable) |
| note | Spot-check results from the API detail endpoint, or the basis of an inference |

### `daf-lobbying-lda-2021plus.csv` (359 rows, one per LDA filing)

| Column | Meaning |
|---|---|
| filing_uuid | LDA filing UUID |
| filing_year, filing_period | Report year and quarter |
| filing_type | LDA type code (Q1–Q4 quarterly; 1A etc. amendments; 1T etc. terminations; RR registration) |
| dt_posted | Date posted to LDA |
| registrant | Lobbying firm, or the organization itself if self-filing |
| client | Client on whose behalf lobbying was reported |
| client_category | Our classification (national_daf_sponsor, daf_platform_vendor, community_foundation, cf_coalition_or_philanthropy_association, donor_advocacy_group, nonprofit_trade_association, financial_firm, financial_trade_association, professional_body, accounting_firm, giving_platform, operating_charity, tax_advocacy_group, single_issue_faith_daf_sponsor, individual_philanthropist) |
| self_filer | Y if the amount is reported as expenses (an in-house filer) |
| income_usd / expenses_usd | Amount reported for the **whole filing**, all issues, rounded to $10k. Blank means <$5k or not applicable |
| issue_codes | General issue codes of the matching activities (mostly TAX) |
| daf_mention_type | `DAF central to issue line` (the line leads with DAFs or is short) or `DAF one item among several` (heuristic) |
| bills_or_rules_named | Regex tags: ACE Act; Charitable Act; OBBBA/P.L. 119-21; QCD-to-DAF (H.R. 2891/S. 3975); universal-giving bill; proposed §4966 regs; Charity Parity Act; Legacy IRA/rollover |
| treasury_or_irs_contacted | Y if the matching activities list Treasury or IRS among government entities |
| government_entities | Entities listed on the matching activities |
| daf_issue_snippet | Up to 400 characters around the first DAF, ACE or QCD-to-DAF mention (public filing text) |
| filing_document_url | LDA public print view |
| api_url | LDA API record |
| match_basis | `DAF/ACE keyword` or `QCD-to-DAF bill only (H.R.2891/S.3975)` |

### `queue-proposals-batch39-n1.csv`

Columns and scales follow [`queue-proposals-README.md`](../../data/mission-2026-11-14/queue-proposals-README.md). There are three rows, P-B39N1-01 to -03, all with state `open`.
