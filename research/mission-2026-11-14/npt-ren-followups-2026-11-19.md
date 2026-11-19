# NPT and Ren follow-ups: RCF default switch dating, NPT segregated accounts, NPT Schedule R line 1b

- **Task:** npt-ren-followups. It covers three queue items:
  - P-B442802-01, from [b4428-02-ren-private-label-defaults.md](b4428-02-ren-private-label-defaults.md);
  - P-G0702-05 and P-G0702-03, from [g0702-b4531-national-990-reads.md](g0702-b4531-national-990-reads.md).
  Both are read with their [V wave 35B] corrections from [validation-wave35b-report.md](validation-wave35b-report.md). The governing Schedule R line is **1b** (gift, grant or capital contribution *to* a related organisation), not 1d (V35B-29/-30).
- **Date:** 2026-11-19. Every page, PDF and API answer was read on that date.
- **Data:** [`data/mission-2026-11-14/npt-ren-followups-2026-11-19.csv`](../../data/mission-2026-11-14/npt-ren-followups-2026-11-19.csv) (data dictionary in §6).
- **Script:** [`scripts/mission_npt_ren_followups.py`](../../scripts/mission_npt_ren_followups.py). It has two modes:
  - `wayback` enumerates captures through the archive.org availability API, with a cached, repeatable run;
  - `npt990` prints the Schedule R Part V indicators, the Part IX program-column composition, the Schedule F Part II line tests and the H.10 FX tests from NPT's FY2025 XML.
- **Queue:** [`data/mission-2026-11-14/queue-proposals-npt-ren-followups.csv`](../../data/mission-2026-11-14/queue-proposals-npt-ren-followups.csv) (6 rows).
- **Labels:**
  - [F] first-party text or filing read this pass;
  - [C] computed by the script;
  - [I] inference;
  - [H] capture metadata from the archive.org availability API (date only, not content);
  - [B] blocked.

## 0. Answers

__ANSWERS__

## 1. P-B442802-01: dating the RCF default switch

__ITEM1__

## 2. P-G0702-05: NPT segregated (adviser-managed) account assets

### 2.1 What NPT publishes

**Search.**
- nptrust.org robots.txt has `User-agent: * Disallow:` (allow all).
- Its sitemaps (page, reports and annual-reports) list no audit or financial-statement page.
- NPT's WordPress media API (`/wp-json/wp/v2/media?search=`) was queried for "financial", "audit", "consolidated", "statements", "990", "FY24", "FY25", "notes", "independent", "auditor", "RSM", "segregated" and "investment".
- The only financial statements it holds are **seven "Consolidated Statements" PDFs, FY2019 to FY2025**. Each is a two-page summary: a statement of financial position and a statement of activities, with **no notes and no auditor's report**.
- nptuk.org (robots allow all) holds no NPT US statements. Media searches for "consolidated" and "statements" returned 0 results.

**Full audited statements with notes for FY2024–FY2025 are not on either site** [F].

| FY | File | PDF created | Pages | SHA-1 (12) |
|---|---|---|---|---|
| 2025 | FY25-AR-Consolidated-Financials-NPT.pdf | 2026-09-01 | 2 | `e7529055f11c` |
| 2024 | Consolidated-Statements-2024-NPT.pdf | 2025-10-28 | 2 | `ddfc47eeea7a` |
| 2023 | Consolidated-Statements-2023.pdf | 2024-05-15 | 2 | `0afc021a7e4d` |

**Investment split.** None is published. The statements carry three lines only:
- "Investments, fair value": $47,837,978k (FY2025), $36,915,275k (FY2024);
- "Investments, other": $56,847k and $56,469k;
- cash: $9,243,758k and $5,970,720k.

There is no line or note for model portfolios versus segregated accounts [F]. The 990 does not split by account type either:
- Part X: publicly traded securities $40.67bn and other securities $6.32bn (EOY FY2025);
- Schedule D Part VII: alternative investments $3.46bn, limited partnerships $0.96bn, preferred stock and crypto $0.16bn;
- Schedule D Part VII also lists closely held equity of $1.73bn [F].

### 2.2 The "$116.3m asset management fees" is program services expense, not asset-management fees

The FY2025 summary's expense block reuses liability captions. The FY2024 summary prints the same FY2024 figures under functional-expense captions:

| Row in FY2025 PDF (expense block) | FY2025 $k | FY2024 $k | Caption for the same FY2024 figure in the FY2024 PDF |
|---|---|---|---|
| "Grants to charitable organizations" | 6,408,840 | 5,616,957 | Grants to charitable organizations |
| "Asset management fees payable" | **116,260** | **94,289** | **Program services** |
| "Lease liability" | 13,230 | 12,025 | Fundraising |
| "Grants payable" | 34,263 | 28,661 | General and administrative |
| "Total Expenses" | 6,572,593 | 5,751,932 | TOTAL EXPENSES |

- The four rows add to total expenses (6,408,840 + 116,260 + 13,230 + 34,263 = 6,572,593) only as grants + program services + fundraising + G&A.
- The real liability "Asset management fees payable" is $400k (FY2025) and $353k (FY2024) on the balance sheet.

So **$116.26m is NPT's consolidated program-services expense excluding grants**, not its asset-management fee [F/C]. This confirms the "layout error" suspicion in `queue-batch35-access-owners-faith.md` and corrects:
- g0702-b4531 §2.5;
- `queue-batch37-filing-questions.md` (P-GPT-03 row and its source row).

See queue row P-NPTREN-06.

### 2.3 Composition of program services, from the 990 (Part IX column B, excluding grants) [C]

The consolidated $116.26m is not broken down anywhere public. The nearest public breakdown is NPT's own Form 990 Part IX, column B (program services), less grants (lines 1–3).

The 990 covers NPT and its disregarded entities, including NPT Transatlantic. The consolidated statements also include NPT's supporting organisations [I], which file their own 990s. That would explain why the 990 figure is $2.09m lower in FY2025 and $1.35m lower in FY2024.

| Component (990 Part IX col B) | FY2025 $ | Share | FY2024 $ | Share |
|---|---|---|---|---|
| Line 11f investment management fees | 93,512,965 | 81.9% | 73,967,492 | 79.6% |
| Staff: officers' compensation, wages, pension, benefits and payroll tax | 13,063,841 | 11.4% | 12,231,490 | 13.2% |
| Other expenses "PROGRAM FEES" | 4,295,780 | 3.8% | 4,077,996 | 4.4% |
| Information technology | 1,996,236 | 1.7% | 1,240,891 | 1.3% |
| Occupancy, office, advertising, conferences, legal, other fees, insurance, all other | 1,302,951 | 1.1% | 1,421,740 | 1.5% |
| **Program services excluding grants (990)** | **114,171,773** | 100% | **92,939,609** | 100% |
| Audited consolidated "program services" | 116,260,000 | | 94,289,000 | |

**Line 11f in total** (all columns) is $93,771,463 in FY2025 and $74,179,211 in FY2024.

**Part VII-B** lists no investment manager among NPT's five highest-paid contractors. ICONIQ Capital, the largest, is listed for "CONSULTING" ($2.86m in FY2025). Nine contractors were paid over $100k in FY2025 and 18 in FY2024 [F]. So no adviser firm behind line 11f is named.

### 2.4 What the fee data can and cannot say about segregated accounts

- **Pooled model fees** come from NPT's "Investment Descriptions and Performance" (PDF modified 2026-09-14). Besides fund expense ratios:
  - Impact portfolios carry "a 0.15% investment advisory fee";
  - the actively managed and index portfolios carry "a 0.10% investment advisory fee and trading/transaction costs up to 4 cents per share" [F].
- **Segregated accounts:** NPT's Segregated Account Investment Information Form (PDF 2024-01-31) asks the adviser to "List all account numbers associated with this DAF and the investment advisory fee for each account". The fee is set **per account** and never published [F].
- **Scenario arithmetic [C/I]:**
  - mean FY2025 Part X investments (lines 11 + 12) are $41.66bn, so line 11f column B is 22.4 bps;
  - if every invested dollar paid only the published model fee of 0.10–0.15%, and that fee sat in line 11f, it would come to $41.7m–$62.5m;
  - that leaves **$31.0m–$51.9m** of line 11f (FY2025; FY2024: $29.7m–$44.5m) as something other than the model advisory fee: segregated-account adviser fees, trading costs or sub-manager fees.
  - This residual is **not** an asset estimate. It cannot be turned into a segregated-account share without a per-account fee rate, and the model fee may be netted in fund returns rather than booked in line 11f.
- **Answer:** the adviser-managed share is **still not estimable from public sources**. The composition of the $116.26m line can be given only through the 990 proxy above (82% line 11f). P-NPTREN-03 points to state charity registries, which may hold the full audits.

## 3. P-G0702-03: NPT FY2025 Schedule R Part V line 1b against the £30.939m transfer

### 3.1 What the return says [F]

The return is NPT's FY2025 Form 990: object 202601289349302480, EIN 237825575, tax year ending 2025-06-30.

**Part V line 1, read in schema order a to s (19 indicators):**
- 1b `GiftGrntOrCapContriToOthOrgInd` = **0 (No)**;
- 1c `GiftGrntCapContriFromOthOrgInd` = 1 (Yes);
- 1d (loans to) = 0;
- 1l, 1n, 1o and 1q = 1;
- all others = 0.

**Part I (disregarded entities):**
- NPT TRANSATLANTIC LIMITED, London (EIN 981125584): total income $141,768,810, end-of-year assets $279,696,494;
- plus six US LLCs, all with zero income.

**Part II (related tax-exempt organisations):**
- NATIONAL PHILANTHROPIC TRUST UK LIMITED, London: exempt-code section blank, direct controlling entity NATIONAL PHILANTHROPIC TRUST, "controlled organization" = **No**;
- six US supporting organisations, each controlled.

**Part V line 2:** 13 transactions, all with the US supporting organisations (types C, L, Q). None names NPT UK or Transatlantic.

### 3.2 What the IRS instructions require [F]

- **Instructions for Schedule R (Rev. December 2024)** ([PDF](https://www.irs.gov/pub/irs-pdf/i990sr.pdf), modified 2025-01-08, SHA-1 `509585485fc9`), "Disregarded entity exception": "Disregarded entities are treated as related organizations for purposes of reporting on Schedule R (Form 990), Part I, but not for purposes of reporting transactions with related organizations in Part V, or otherwise on Form 990."
- **Same instructions, Part V line 1:** "Check 'Yes' in the appropriate boxes of line 1 if the filing organization engaged in any of the transactions listed in Part V with any related organizations (other than disregarded entities listed in Part I)."
- **2025 Instructions for Form 990, Appendix F** ([PDF](https://www.irs.gov/pub/irs-pdf/i990.pdf), modified 2025-12-11, SHA-1 `63250e5a5368`): "A disregarded entity ... is generally treated as a branch or division of its parent organization for federal tax purposes. Therefore, financial and other information applicable to a disregarded entity must be reported as the parent organization's information, except on Form 990, Part VI, lines 10a and 10b, and on Schedule R (Form 990), in which disregarded entities must be separately reported." Also: "The organization must also report the activities of a disregarded entity in the appropriate parts (including schedules) of the Form 990."
- irs.gov robots.txt was read first. It disallows search and listing paths, not `/pub/irs-pdf/`.

**Reading [I]:**
- The exception removes transactions **between NPT and Transatlantic** from Part V, because Transatlantic is NPT for tax purposes.
- It does not remove Transatlantic's transactions **with a third related organisation**. Under Appendix F those are NPT's own activities.
- NPT UK is a Part II related organisation. So Transatlantic's £30.939m grant to NPT UK is, for the 990, a grant by NPT to a related organisation, and **line 1b should read Yes**. The instructions also count a single transaction on more than one line where it fits.
- NPT UK's own note 14 also records "£30.9M from National Philanthropic Trust". If that is a second, direct transfer, it independently requires 1b = Yes.
- **Either way, the filed "No" is inconsistent with the affiliates' audited accounts.** No reading of the disregarded-entity exception reconciles them.

**Line 2 [I]:**
- Line 2 covers transactions over $50,000 with **controlled entities** (section 512(b)(13)). For 501(c)(3) filers, it also covers related tax-exempt organisations **not described in section 501(c)(3)**.
- NPT lists NPT UK as not controlled and gives it no exempt-code section. The second test could therefore apply, but whether a UK charity counts as "not described in section 501(c)(3)" depends on facts not on the return.
- Line 2 is a weaker test than 1b and is not relied on here.

**Other possible explanations, none documented [I]:**
- (a) NPT treats the transfer as a grant made on donor recommendation from DAFs, not an organisational gift. The instructions make no such carve-out for line 1b.
- (b) Preparer error.
- (c) Timing: no — both affiliates' accounts and NPT's 990 cover the year to 30 June 2025.

### 3.3 Is the $39.1m Europe line the transfer? [F/C/I]

**Part II facts:**
- FY2025 Part II has 560 lines totalling $310,238,950. Europe has 411 lines totalling $154,427,213 (Part I Europe: $154,655,237).
- The largest line is **$39,100,000, Europe, "ENVIRONMENT, ANIMALS", wire transfer**. The next lines are $16.77m (Middle East and North Africa) and $12.08m (Europe). So the $39.1m line is the only one that could carry £30.939m at any FY2025 exchange rate.

**FX test (Fed H.10 noon rates, 250 days, 1 July 2024 to 30 June 2025):**
- Range 1.2158 to 1.3754; mean 1.2948.
- £30.939m converts to $37.62m at the minimum, $40.06m at the mean and $42.55m at the maximum.
- The implied rate for $39.1m is **1.26378**. H.10 was within ±0.0025 of it on 11 days: 2024-07-01, 2024-11-15, 2024-11-20, 2024-12-02, 2024-12-13, 2025-02-18, 2025-02-20, 2025-02-21, 2025-02-24, 2025-02-25 and 2025-02-27.
- So the size is consistent with a wire in mid-November 2024 to February 2025, or on 1 July 2024.

**Round-number test:**
- $39,100,000 is a round $100k figure. A GBP grant converted at a market rate would rarely be round.
- But round figures are common in this schedule: 17 of the 57 Part II lines of $1m or more are exact $100k multiples, and so are 6 of the 25 Europe lines of $1m or more. Roundness does not discriminate.
- It fits a USD-denominated wire from NPT to NPT UK (note 14's "£30.9M from National Philanthropic Trust") at least as well as a GBP grant by Transatlantic [I].

**Purpose label:**
- "ENVIRONMENT, ANIMALS" is an odd label for a sponsor-to-sponsor DAF transfer, which would more naturally carry a philanthropy-type label such as "PUBLIC, SOCIETAL BENEFIT" (a label on 93 of the 560 FY2025 lines; "ENVIRONMENT, ANIMALS" is on 64). No NPT sponsor-to-sponsor line can be identified to compare with.
- The label may reflect the donor's intended use. NPT UK's note says the money "will be used by donors for ongoing granting to charities". This weighs mildly against the match [I].

**Verdict:**
- The $39.1m line is the **only candidate**, and its size is consistent with £30.939m.
- Nothing on the return names the recipient, and the purpose label fits poorly. **Not proven.**
- Whichever way it falls, at most one of NPT UK's two £30.9m receipts can sit in Schedule F as a single line (V35B).
- If both receipts are real and separate, the other one is not in Part II as a single line. It would then sit outside Schedule F or be split into lines under $16.8m [I].

**Effect:** if the line is the transfer, 12.6% of NPT's FY2025 Schedule F line 3 ($39.1m of $310.5m) is affiliate re-granting. That is in line with the g0702 estimate of ≈ 12.9% at the mean rate [C].

## 4. Method

1. **Robots and access.** Every host's robots.txt was fetched first with UA `research-script/1.0` and logged (§7). archive.org, nptrust.org, nptuk.org and irs.gov allow the paths used. The donorfirstx hosts return 404 for robots.txt, which is treated as no rules. web.archive.org reset the connection, so its robots.txt could not be read; nothing on that host was requested again, including the CDX API. The WebFetch tool also refused web.archive.org.
2. **Wayback.** The script probes `https://archive.org/wayback/available?url=…&timestamp=…` on a monthly grid from 2021-01 to 2026-11. It bisects every interval whose ends return different closest captures, down to one day, and retries empty answers up to three times (the API intermittently returns `{}`). Every answer is cached as JSON (scratchpad `qnr/wb/`).
3. **Live files.** The current guide PDFs were re-fetched. For each, the full SHA-1, PDF Creation/ModDate (`pdfinfo`) and the HTTP `Last-Modified` and `ETag` headers were recorded.
4. **NPT.** The consolidated statements and investment documents were found through the WordPress media API and read with `pdftotext`. The 990 figures are from the IRS XML (scratchpad copy of `202601289349302480.xml` and `202511339349301311.xml`, the same objects as the g0702 extract cache).
5. **FX.** The saved Fed H.10 USD/GBP history (`dat00_uk.htm`, as used by `mission_national_990_reads.py`) gives the daily rates.
6. **Commands:**
   - `python3 -I scripts/mission_npt_ren_followups.py . wayback <cache> <out.json> [--fetch]`
   - `python3 -I scripts/mission_npt_ren_followups.py . npt990 <NPT_FY2025.xml> <dat00_uk.htm>`

## 5. Limits

- **Wayback content and hashes were not available.** web.archive.org (snapshots and CDX) was unreachable. The task's "SHA-1 hashes of bracketing captures" can therefore be given only for the live files, not for the archived ones. The availability API also returns only a capture that is closest to some probe, so two captures within a day of each other, or captures shadowed by neighbours, can be missed. It gives no digest and no status for non-200 captures.
- **HTTP Last-Modified** is the server file's write time. A redeploy resets it, so it dates the last copy, not the first publication.
- **The PDF CreationDate** of the current guide (2026-10-06) is set by pdf-lib at save time. The text may be older than the file.
- **NPT:** no notes are public, so the "program services" composition is a 990 proxy, not the audited breakdown. The FY2025 PDF's caption error is inferred from the FY2024 PDF and the arithmetic. NPT has not confirmed it.
- **Schedule R:** the reading of line 1b is ours. The IRS has not ruled on it. The two £30.9m figures in NPT UK's note 14 may be one transfer described twice.
- **Schedule F:** the Part II lines carry no recipient name, so the match rests on size alone.

## 6. Data dictionary: `npt-ren-followups-2026-11-19.csv`

| Column | Meaning |
|---|---|
| `item` | P-B442802-01, P-G0702-05 or P-G0702-03 |
| `row_type` | `wayback_capture`, `wayback_none`, `live_file`, `npt_statement`, `npt_part_ix`, `npt_fee_doc`, `sched_r_indicator`, `sched_r_org`, `irs_instruction`, `sched_f_line`, `sched_f_test`, `fx_test`, `affiliate_accounts` or `finding` |
| `subject` | What the row describes (URL path, line, document or test) |
| `date` | Capture timestamp (UTC, YYYYMMDDhhmmss), document date or filing period |
| `value` | Number or code, as filed, captured or computed |
| `unit` | usd, gbp, usd_per_gbp, count, share, indicator, text |
| `sha1` | Full SHA-1 of the file read this pass (blank when not fetched) |
| `quote` | Verbatim text supporting the row, where one exists |
| `source_url` | Primary URL (for Wayback rows, the snapshot URL as returned by the API, which was not opened) |
| `evidence` | F, C, I, H or B (see labels above) |
| `note` | Reading or caveat |
| `retrieved` | 2026-11-19 |

## 7. Robots and access log (2026-11-19)

| Host | robots.txt | Used for | Result |
|---|---|---|---|
| archive.org | 200; disallows only `/control/` and `/report/` | Wayback availability API | answered (intermittent empty `{}` answers, retried) |
| web.archive.org | connection reset (three curl tries; WebFetch refused) | snapshots, CDX API | **not used [B]** |
| rcf, ubs, tda, ampf, rbcrcf, mdrt, rcfgivingfund, northwesternmutual `.donorfirstx.com` | 404 (no rules) | live guide PDFs and HEAD requests | 200 |
| www.nptrust.org | 200; `User-agent: * Disallow:` (Yisou and Baidu blocked) | sitemaps, WP media API, PDFs | 200 (about-npt and financials paths 404) |
| www.nptuk.org | 200; `User-agent: * Disallow:` | WP media API | 200, no NPT US statements |
| www.irs.gov | 200; disallows search and listing paths only | i990sr.pdf, i990.pdf | 200 |

Cached, not re-fetched: NPT's FY2024 and FY2025 990 XML, the NPT UK and NPT Transatlantic 2024/25 accounts (nptuk.org; robots allow, per g0702) and the Fed H.10 page.

## 8. Source register (primary URLs)

| # | Source | Date | URL |
|---|---|---|---|
| S1 | Ren "Giving Platform Donor User Guide" (RCF core portal; identical file on six more RCF portals) | PDF 2026-10-06; HTTP Last-Modified 2026-11-10 | https://rcf.donorfirstx.com/pdf/RCF/Donor%20User%20Guide.pdf |
| S2 | Same guide, UBS portal | as S1 | https://ubs.donorfirstx.com/pdf/UBS/Donor%20User%20Guide.pdf |
| S3 | RCF Donor User Guide, template 2309 (TDA portal) | PDF 2024-07-12 | https://tda.donorfirstx.com/pdf/tda/RCF%20Donor%20User%20Guide.pdf |
| S4 | UBS Donor User Guide, template 2309 | PDF 2024-06-14 | https://ubs.donorfirstx.com/pdf/UBS/UBS%20Donor%20User%20Guide.pdf |
| S5 | Wayback Machine availability API | queried 2026-11-19 | https://archive.org/wayback/available?url=rcf.donorfirstx.com/pdf/RCF/Donor%20User%20Guide.pdf |
| S6 | NPT FY2025 consolidated statements (2 pages) | PDF 2026-09-01 | https://www.nptrust.org/wp-content/uploads/2026/09/FY25-AR-Consolidated-Financials-NPT.pdf |
| S7 | NPT FY2024 consolidated statements (2 pages) | PDF 2025-10-28 | https://www.nptrust.org/wp-content/uploads/2025/10/Consolidated-Statements-2024-NPT.pdf |
| S8 | NPT FY2023 consolidated statements (2 pages) | PDF 2024-05-15 | https://www.nptrust.org/wp-content/uploads/2024/05/Consolidated-Statements-2023.pdf |
| S9 | NPT WordPress media API (search used to list all statement PDFs) | queried 2026-11-19 | https://www.nptrust.org/wp-json/wp/v2/media?search=consolidated |
| S10 | NPT Investment Descriptions and Performance (model advisory fees) | PDF 2026-09-14 | https://www.nptrust.org/wp-content/uploads/2024/09/Investment-Descriptions-and-Performance-NPT.pdf |
| S11 | NPT DAF Segregated Account Investment Information Form | PDF 2024-01-31 | https://www.nptrust.org/wp-content/uploads/2023/09/DAF-Segregated-Account-Investment-Information-NPT.pdf |
| S12 | NPT FY2025 Form 990 (object 202601289349302480) | filed 2026 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601289349302480_public.xml |
| S13 | NPT FY2024 Form 990 (object 202511339349301311) | filed 2025 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202511339349301311_public.xml |
| S14 | Instructions for Schedule R (Form 990), Rev. December 2024 | PDF 2025-01-08 | https://www.irs.gov/pub/irs-pdf/i990sr.pdf |
| S15 | 2025 Instructions for Form 990, Appendix F | PDF 2025-12-11 | https://www.irs.gov/pub/irs-pdf/i990.pdf |
| S16 | NPT Transatlantic Annual Report and Accounts 2024/25 (note 19, grant table) | year to 2025-06-30 | https://www.nptuk.org/transatlantic-annual-report-and-accounts-2025/ |
| S17 | NPT UK Annual Report and Accounts 2024/25 (note 14) | year to 2025-06-30 | https://www.nptuk.org/npt-uk-annual-report-and-accounts-2025/ |
| S18 | Federal Reserve H.10 USD/GBP history | page dated 2026-11-16 | https://www.federalreserve.gov/releases/h10/hist/dat00_uk.htm |
