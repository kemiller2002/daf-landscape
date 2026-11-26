# The 13 submissions of 2026 on docket IRS-2023-0053: access check and 2023-24 baseline (P-B39N1-01)

**Prepared 2026-11-20. Desk research only.** No one was contacted. Nothing was logged into, registered for or submitted, and no API key was used. This is research, not legal or tax advice. Labels follow [direction-policy-lobbying-obbba.md](direction-policy-lobbying-obbba.md): **[F]** the source states it; **[C]** our count; **[I]** inference. Grades: **P** primary record read; **S** secondary; **SS** search-engine summary only, not opened.

**Outputs**
- [`data/mission-2026-11-14/docket-2026-submissions-2026-11-20.csv`](../../data/mission-2026-11-14/docket-2026-submissions-2026-11-20.csv): 13 rows, one per submission, with access status.
- [`data/mission-2026-11-14/queue-proposals-b39n1-01.csv`](../../data/mission-2026-11-14/queue-proposals-b39n1-01.csv): 5 follow-ups.
- [`scripts/mission_b39n1_01_docket_2026.py`](../../scripts/mission_b39n1_01_docket_2026.py): builds the CSV from the repo's docket pull and prints the counts. Run it as `python3 -I scripts/mission_b39n1_01_docket_2026.py . <out.csv>`.

---

## 0. Answer in brief

| Question | Answer |
|---|---|
| How many of the 13 submissions could be read? | **0 of 13** [C]. All rows are `blocked`. |
| Why? | www.regulations.gov and downloads.regulations.gov return a CloudFront **403 "Request blocked"** to this session, even for `/robots.txt` [F, P]. The task allowed only one fallback, copies the submitters published themselves, and **none was found** on any reachable site (§2.3). |
| What each letter asks on adviser-managed DAFs, fees and advisers, Form 990, or a meeting, draft or OBBBA | **Not known.** All content fields in the CSV are `not_read`. Nothing below infers what the letters say. |
| What can be said | (1) **Who** filed and **when** (docket metadata, §1). (2) The 2023-24 position of **two** of the filers, read from their own published 2024 letters: SIFMA and the NYSBA Tax Section (§4). (3) The current Unified Agenda entry for the rule, read on reginfo.gov (§5). |

---

## 1. The 13 submissions [F, P: docket metadata from the repo's API pull of 2026-11-15]

The rows come from [`daf-regs-2023-comments-summary.csv`](../../data/mission-2026-11-14/daf-regs-2023-comments-summary.csv) (phase `post-hearing_2026`). Submitter names are given **as the docket titles them**. Individuals named in those titles are referred to here only by role.

| Doc ID | Posted | Docket title (organisation part) | Resolved as | Earlier filings by the same organisation (2023-24) |
|---|---|---|---|---|
| -0242 | 2026-05-13 | "Alder and Colvin" | Adler & Colvin (misspelled in the docket title; wave 24A) | -0132 (joint with New Venture Fund) |
| -0243 | 2026-05-26 | NYSBA (filed with an individual's name) | NYSBA Tax Section. The person named was the Section's First Vice Chair in Feb 2024 (Report 1489 letterhead), and nysba.org has a "new Tax Section chair" post naming him | -0063 |
| -0244 | 2026-05-26 | AEF (filed with an individual's name) | American Endowment Foundation | -0017, -0059, -0090; outline -0201 |
| -0245 | 2026-05-26 | ABA (filed with an individual's name) | American Bar Association; **the docket title does not say which section** | RPTE -0060, -0228; ABA -0179; Tax Section outline -0183 |
| -0246 | 2026-05-26 | SIFMA (filed with an individual's name) | Securities Industry and Financial Markets Association | -0051; outline -0185 |
| -0247 | 2026-05-26 | "KA" (filed with an individual's name) | Kallina, a law firm or attorney | -0172; outline -0232 |
| -0248 | 2026-05-26 | RCF (filed with an individual's name) | Renaissance Charitable Foundation | -0015, -0055; outlines -0195, -0221 |
| -0249 | 2026-06-15 | AEF | American Endowment Foundation (second 2026 filing) | as -0244 |
| -0250 | 2026-06-15 | 'CF (Jenn Holcomb)' | Council on Foundations (**repo inference**) | -0006, -0118; outlines -0193, -0199 (if CF is the Council) |
| -0251 | 2026-06-15 | Ren (filed with an individual's name) | Ren, the DAF administration vendor | -0088 |
| -0252 | 2026-06-15 | ABA (a different individual's name) | American Bar Association; section not stated | as -0245 |
| -0253 | 2026-06-15 | RCF (same individual as -0248) | Renaissance Charitable Foundation (second 2026 filing) | as -0248 |
| -0254 | 2026-06-15 | 'MCF (Bob Sorge)' | Madison Community Foundation (**repo inference**) | -0085; outlines -0176, -0180, -0184, -0234 (if MCF is Madison CF) |

**Counts [C, script].**
- 13 submissions from 10 organisations.
- Posting dates: 1 on 2026-05-13, **6 on 2026-05-26** and **6 on 2026-06-15**.
- Three organisations filed twice: AEF, RCF and ABA.
- The 10 organisations made **28** earlier docket filings between 2023 and 2024.

**[I] Shape of the batch.** Two batches posted on the same day each, three weeks apart. Three filers came back for a second letter in the June batch. That pattern fits a second round of input: replies, or answers to questions asked after the first batch. **It does not establish that a meeting took place or a draft was circulated.** That would need the letters themselves. On posting versus receipt dates: the repo's earlier spot checks found -0242, -0244 and -0250 received and posted on the same day (direction-policy-lobbying-obbba.md §1.2).

**Name notes.** The task lists "Adler & Colvin" and "Kallina". The docket titles are "Alder and Colvin" and "KA (Emanuel J. Kallina)". The CSV keeps the docket spelling in `submitter_as_titled`.

---

## 2. Method and access log

### 2.1 Robots.txt, checked first (2026-11-20, UA `research-script/1.0`)

| Host | robots.txt result | Action taken |
|---|---|---|
| www.regulations.gov | **403** CloudFront "Request blocked" | One probe of the -0244 comment page: **403**. Treated as blocked |
| downloads.regulations.gov | **403** CloudFront "Request blocked" | One probe of `/IRS-2023-0053-0244/attachment_1.pdf`: **403**. Treated as blocked |
| api.regulations.gov | 403 `API_KEY_MISSING` | Not used. The task allows no API key, and DEMO_KEY was not used |
| www.aefonline.org | 200: `Disallow:` (allow all), crawl-delay 10 | Post and page sitemaps read at an 11 s pace. WP media API returned 401 |
| www.sifma.org | 200: content-signal comments; no rule covering letter pages | Full sitemap read (10,276 URLs [C]). 2024 DAF letter downloaded |
| nysba.org | 200: only `/wp-admin/` disallowed | Tax Section reports page, master index (as of 2026-11-11) and three May 2026 reports read. WP media API returned 401 |
| www.adlercolvin.com | 200: `/wp-admin/` disallowed, crawl-delay 10 | Post and page sitemaps read at an 11 s pace. One 2026 blog post read |
| www.reninc.com | 200: `/wp-admin/` disallowed for `*` | Blogs, resources and newsroom sitemaps read |
| www.rencharitable.org | 200: **`User-agent: *` / `Disallow: /`** | Not fetched |
| madisongives.org | 200: allow all, crawl-delay 10 | Post, blog and publications sitemaps read at an 11 s pace |
| www.americanbar.org | **403** Cloudflare challenge | Not fetched |
| cof.org (www.cof.org redirects here) | **403** Cloudflare challenge | Not fetched |
| www.reginfo.gov | No robots.txt (the path redirects to `/public/`) | RIN 1545-BI33 agenda page and EO 12866 meeting search read |
| blog.pgcalc.com | 200: preview paths only disallowed | One post read (secondary) |
| www.taxnotes.com | **403** | Not fetched. Search snippets only |

We did not change the user agent, use an archive mirror, log in or submit a form. The task limited the fallback to copies the submitters published themselves, so third-party mirrors were not tried.

### 2.2 Search for copies the submitters published

For each organisation we did (a) a web search for a 2026 letter on §4966 or DAF regulations and (b) a scan of the organisation's own sitemap or publications index, where robots allowed it. What we found:

| Organisation | Result |
|---|---|
| **SIFMA** | Sitemap advocacy items dated 2026-05-01 to 2026-06-30: 43 [C]. **None** is on DAFs or §4966. The only SIFMA DAF letter on the site is the 2024-02-08 comment. The 2026-27 PGP letter (published May 29, 2026) is about Treasury repo clearing, not DAFs |
| **NYSBA Tax Section** | The 2026 reports listed are Nos. 1519–1535. **None** is on §4966. The master index (to 2026-11-11) lists DAF items only as Nos. 1129, 1390 and **1489** (Feb 13, 2024). The 2026 docket filing is therefore not a numbered Tax Section report on the site [F]. It may be an unnumbered letter [I] |
| **AEF** | No 2026 policy letter on aefonline.org. The 2026-03-24 "Unlocking Generosity" white paper release does not mention Treasury, §4966, fees or Form 990 (WebFetch summary of the page) |
| **Adler & Colvin** | No 2026 DAF-regulation post. The 2026-08-20 post on H.R. 9721 (fiscal sponsorship) mentions Form 990 changes. It also says "Our firm is in contact with the IRS to lend our expertise as they think about what these 990 changes look like" (WebFetch extract). It does not mention §4966. The firm's 2024 joint letter URL (`/wp-content/uploads/2024/03/IRS-2023-0053-0132-…pdf`) now returns **404** |
| **Ren / RCF** | Nothing on reninc.com. rencharitable.org disallows all crawlers |
| **Madison CF** | Nothing on madisongives.org |
| **Kallina** | No firm website identified. A search found only the 2024 hearing speaker list (SS) |
| **ABA, Council on Foundations** | Hosts not fetchable (Cloudflare). Search shows related items: an ABA Tax Section PGP letter dated 2026-05-29, and a Council 2026 PGP comment listing "Donor Advised Funds: Final Regulations and Additional Proposed Regulations Addressing Certain Issues" (SS). **Neither is one of the 13 docket filings**, and neither was opened |

### 2.3 Result

| Access status | Count [C] |
|---|---:|
| readable (docket or submitter copy) | 0 |
| blocked | 13 |

---

## 3. Per-submission findings

The task asks for five fields per letter: the ask on adviser-managed DAFs, fees and advisers, Form 990, any meeting, draft or OBBBA reference, and quotes with page numbers. **None can be filled.** Each is recorded as `not_read` in the CSV. We have not drawn the positions from titles, earlier letters or press coverage, because that would be invention.

---

## 4. 2023-24 baseline from letters the filers themselves published [F, P]

Only two of the ten organisations have a 2023-24 letter that this session could read on the organisation's own site. They give a firm baseline against which the 2026 letters can be compared once read.

### 4.1 SIFMA, letter of 2024-02-08 (docket -0051 by title and date, [I]; 11 pp.)

| Topic | Position (verbatim, page) |
|---|---|
| Statutory authority | "we recommend that the IRS's expansion of the definition of donor-advisor to include personal IAs be stricken from the Proposal" (p. 3) |
| Process | "If such data or evidence does exist, then the IRS should repropose and publish its data and evidence for public comment" (p. 4) |
| Rule text | "we recommend that the IRS strike subparagraphs(h)(2) and (h)(3) of proposed §53.4966-1(h)" (p. 6) |
| Fees and advisers | "the negotiation of the fee on the donor-client's personal assets is separate and distinct from the negotiation of the fee for the DAF (which is negotiated with the sponsoring organization)" (p. 9). Also: "the Proposal will likely chill the market by either effectively prohibiting traditional IA compensation structures or otherwise subjecting them to excise taxes" (p. 9) |
| Fallback asks | Extend the "sponsoring organization as a whole" exception to "personal IAs who advise pooled assets in a DAF" (p. 9). Exclude managers of irrevocable trust assets (p. 10). Limit "personal IA" to an individual person, not a firm (p. 10) |
| Effective date | "we request that the IRS provide a one-year transition period" (p. 11) |
| Form 990 | Not mentioned (text search for "990") |

### 4.2 NYSBA Tax Section, Report No. 1489 of 2024-02-13 (docket -0063 by title and date, [I]; 37 pp.)

Pages are given as the printed number, with the PDF page in brackets.

| Topic | Position (verbatim, page) |
|---|---|
| Overall | "In general, we support the rules set forth in the Proposed Regulations, with an exception for the treatment of investment advisors" (p. 17 [PDF 22]) |
| Adviser-managed DAFs | "We recommend Treasury modify the Proposed Regulations' treatment of investment advisors … arm's-length fees paid from a DAF for investment advice should in principle and as a policy matter not be considered an excess benefit transaction" (p. 2 [PDF 7]) |
| Competition argument | "the standard in the Proposed Regulations is both over- and under-inclusive, because it may not entirely limit abuses in the case of sponsor-affiliated advice while precluding the use of independent advisors in situations that present a low-risk of abuse" (pp. 18–19 [PDF 23–24]) [V wave 45A] |
| Fee mechanism proposed | "advisory fees paid by the DAF to a non-sponsor independent advisor could be excepted from presumptive treatment as an excess benefit transaction as long as those fees do no[t] exceed what would have been charged by the sponsor to manage the DAF assets" (p. 20 [PDF 25]). The sponsor polices arm's-length pricing, with §482 and §4958 valuation as the standard (p. 20) |
| Fees as distributions | "We recommend adding a presumption that reasonable expenses incurred in the ordinary course of the sponsoring organization's operations do not achieve a result inconsistent with the purposes of Section 4966" (p. 31 [PDF 36]) |
| Form 990 | Not mentioned (text search for "990") |

### 4.3 Reading against the repo's summary of positions in 2023-24 [I]

- **SIFMA** is on the "strike the rule" side in direction-policy-lobbying-obbba.md §1.4 ("Some asked to strike the rule as inconsistent with the statute").
- **NYSBA** is closer to the "safe harbour" side ("written agreement plus sponsor oversight"). It does not deny Treasury's authority. It proposes an arm's-length test policed by the sponsor, and it explicitly flags a competitive bias in favour of sponsor-affiliated advisers.
- **Neither letter raised Form 990 reporting.** If the 2026 letters do discuss §6033 or Form 990, that would be **new** relative to these two baselines. It would fit the 2026-27 PGP's reframing to "§§4966 and 6033". This is a test for the follow-up, not a finding.
- **AEF and the others.** For AEF, RCF, Ren, Kallina, Adler & Colvin, the Council on Foundations and Madison CF, the repo still has no per-filer primary baseline. Their 28 docket IDs are listed in the CSV for the follow-up (P-B39N101-02).

---

## 5. Context read in passing [F, P unless marked]

| Item | Finding |
|---|---|
| Unified Agenda, RIN 1545-BI33 (reginfo.gov, requested with `pubId=202510`) | Final Rule Stage; "EO 14192 Designation: Not subject to, not significant"; Timetable "Final Action 07/00/2026". The page shows only "Publication ID: 2026", so the edition was unverified at drafting. Validation identified it: reginfo’s edition list for this RIN labels pubId 202510 “2026”, the 2026 Regulatory Plan and Unified Agenda (OIRA introduction PDF created 2026-07-01). The Spring 2025 edition (pubId 202504) gave Final Action 05/00/2026 [V wave 45A]. This replaces the "SS only" Unified Agenda row in direction-policy-lobbying-obbba.md §1.5 with a primary read, with the edition identified as the 2026 Unified Agenda [V wave 45A] |
| EO 12866 meetings for RIN 1545-BI33 (reginfo.gov) | "No records found". This is consistent with a "not significant" rule that OIRA does not review. **It is not evidence about meetings with Treasury or the IRS**, which this log does not cover |
| PG Calc blog, 2026-06-15 (S) | Says the rules "remain in the proposed phase while the IRS sorts through thousands of public comments". This conflicts with the docket's **249** public submissions; treat it as rhetorical. It also dates OBBBA to "late 2025", which is wrong: it was signed 2025-07-04 |

---

## 6. Limits

1. **No 2026 letter text.** Every content conclusion about the 13 letters is open. The next step is the owner-assisted download (P-B39N101-01).
2. **Docket metadata is second-hand within the repo.** It comes from the 2026-11-15 API pull. It was not re-queried, because no API key is allowed.
3. **Organisation inferences.** 'CF' as the Council on Foundations and 'MCF' as Madison Community Foundation are repo inferences, not verified. The ABA section behind -0245 and -0252 is unknown.
4. **The baseline matches are inferred.** SIFMA's 2024 letter is matched to docket -0051 and NYSBA Report 1489 to -0063 by title and date. The regulations.gov copies could not be compared.
5. **"Not found" is not "not published".** Search engines and sitemaps can miss PDFs. On Cloudflare hosts (ABA, Council on Foundations) and robots-disallowed hosts (rencharitable.org), nothing could be checked.

---

## 7. Data dictionary: `docket-2026-submissions-2026-11-20.csv` (13 rows)

| Column | Meaning |
|---|---|
| document_id | Docket document ID (IRS-2023-0053-0242 … -0254) |
| posted_date | Posting date on regulations.gov (repo API pull, 2026-11-15) |
| submitter_as_titled | Submitter title exactly as the docket lists it |
| org_key | Short key used for grouping: AEF, RCF, Ren, SIFMA, ABA, NYSBA, KA, AC, CF, MCF |
| submitter_resolved | Organisation the title is read as; "(inference)" where unverified |
| resolution_basis | Why the title is read that way |
| commenter_type | Category from the repo summary CSV |
| regulations_gov_url | Comment page URL |
| attachment_url_tried | Attachment URL probed. Only -0244 was probed, because the block is host-level |
| regsgov_page_status | HTTP result on the comment page |
| downloads_status | HTTP result for downloads.regulations.gov |
| submitter_copy_search | Hosts checked for a copy the submitter published, their robots result, and the outcome |
| access_status | `readable` or `blocked` (all 13 are `blocked`) |
| adviser_managed_ask, fees_and_advisers, form_990, meeting_draft_obbba, quotes_with_pages | Content fields; `not_read` for every row |
| prior_2023_24_ids | Docket IDs (suffix only) of the same organisation's 2023-24 filings, matched on title |
| baseline_2023_24_source | Whether a primary 2023-24 letter by this organisation was read (§4) |
| evidence_grade | Grade of the row's evidence |
| checked_date | 2026-11-20 |

The queue proposals file follows [`queue-proposals-README.md`](../../data/mission-2026-11-14/queue-proposals-README.md) and has 5 rows, P-B39N101-01 to -05, all `open`.

---

## Source register

| ID | Source | Date | URL | Grade |
|---|---|---|---|---|
| D1 | Repo docket pull: daf-regs-2023-comments-summary.csv (regulations.gov API v4, 2026-11-15) | 2026-11-15 | https://api.regulations.gov/v4/comments?filter[docketId]=IRS-2023-0053 | P (via repo) |
| D2 | regulations.gov comment page, -0244 (probe returned 403) | 2026-11-20 | https://www.regulations.gov/comment/IRS-2023-0053-0244 | blocked |
| D3 | downloads.regulations.gov attachment, -0244 (probe returned 403) | 2026-11-20 | https://downloads.regulations.gov/IRS-2023-0053-0244/attachment_1.pdf | blocked |
| B1 | SIFMA, comment on REG-142338-07 | 2024-02-08 | https://www.sifma.org/wp-content/uploads/2024/02/IRS-Proposed-Rule-Taxes-on-Taxable-Distributions-from-Donor-Advised-Funds.pdf | P |
| B2 | NYSBA Tax Section Report No. 1489 | 2024-02-13 | https://nysba.org/wp-content/uploads/2024/02/NYSBA-TS-Report-No-1489-on-Proposed-Regulations-under-Section-4966.pdf | P |
| N1 | NYSBA Tax Section reports page (2026 list, Nos. 1519–1535) | read 2026-11-20 | https://nysba.org/tax-section-reports/ | P |
| N2 | NYSBA master index of reports as of 2026-11-11 | 2026-11 | https://nysba.org/wp-content/uploads/2026/11/Master-index-reports-as-of-Nov-11-2026.pdf | P |
| X1 | SIFMA sitemap (10,276 URLs; advocacy items for May–June 2026) | read 2026-11-20 | https://www.sifma.org/sitemap.xml | P |
| X2 | SIFMA, 2026-27 PGP recommendations (not DAF) | 2026-05-29 | https://www.sifma.org/advocacy/letters/recommendations-for-2026-27-irs-priority-guidance-plan-notice-2026-23 | P |
| X3 | AEF post and page sitemaps | read 2026-11-20 | https://www.aefonline.org/sitemap_index.xml | P |
| X4 | AEF, "Unlocking Generosity" white paper release | 2026-03-24 | https://www.aefonline.org/thought-leadership/american-endowment-foundation-unveils-unlocking-generosity-landmark-white-paper/ | P (WebFetch summary) |
| X5 | Adler & Colvin sitemaps; H.R. 9721 post | 2026-08-20 | https://www.adlercolvin.com/blog/2026/08/20/h-r-9721-fiscal-sponsorship-in-the-halls-of-congress/ | P (WebFetch extract) |
| X6 | Adler & Colvin 2024 joint comment (now 404) | 2024-03 | https://www.adlercolvin.com/wp-content/uploads/2024/03/IRS-2023-0053-0132-Comment-from-NVF-and-AC.pdf | dead link |
| X7 | Ren sitemaps | read 2026-11-20 | https://www.reninc.com/sitemap_index.xml | P |
| X8 | Madison CF sitemaps | read 2026-11-20 | https://madisongives.org/sitemap_index.xml | P |
| R1 | reginfo.gov Unified Agenda entry, RIN 1545-BI33 | read 2026-11-20 | https://www.reginfo.gov/public/do/eAgendaViewRule?pubId=202510&RIN=1545-BI33 | P (2026 edition, pubId 202510) [V wave 45A] |
| R2 | reginfo.gov EO 12866 meetings search, RIN 1545-BI33 | read 2026-11-20 | https://www.reginfo.gov/public/do/eom12866SearchResults?pubId=&rin=1545-BI33&viewRule=true | P |
| S1 | PG Calc blog, "The State of Play…" | 2026-06-15 | https://blog.pgcalc.com/the-state-of-play-navigating-the-current-landscape-of-qcd-legislation-and-daf-regulations | S |
| SS1 | ABA Tax Section, 2026-27 PGP comments (not opened; Cloudflare) | 2026-05-29 | https://www.americanbar.org/content/dam/aba/administrative/taxation/policy/2026/2026-05-29-comments.pdf | SS |
| SS2 | Council on Foundations, 2026 PGP comment (not opened; Cloudflare) | 2026-05 | https://cof.org/sites/default/files/2026-05/2026%20IRS%20Priority%20Guidance%20Plan%20Comment.pdf | SS |
| S-TN | Tax Notes coverage of the 2024 letters (titles only; robots 403) | 2024 | https://www.taxnotes.com/research/federal/other-documents/public-comments-regulations/nysba-tax-section-issues-report-proposed-donor-advised-fund-regs/7j6xd | SS |
| R0 | Repo: direction-policy-lobbying-obbba.md §1.2, §1.4, §1.5 and wave 24A corrections | 2026-11-15 | direction-policy-lobbying-obbba.md | R |
