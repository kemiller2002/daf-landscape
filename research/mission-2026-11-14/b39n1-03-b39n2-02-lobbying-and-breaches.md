# DAF-adjacent lobbying (LDA 2021–2026) and DAF-parent breach notices (MA, VT, ME)

Queue items **P-B39N1-03** (lobbying) and **P-B39N2-02** (breach registers). Built 2026-11-20 by `scripts/mission_lda_breach.py`. Every figure here comes from that script's output or is quoted from a primary register page linked in §6.

Evidence tags: [C] computed by the script; [P] read from a primary register page; [I] inference.

---

## Summary

**(A) Lobbying.** The earlier scan (`daf-lobbying-lda-2021plus.csv`) kept only filings that name DAFs or the DAF bills. This pass pulls **every** 2021+ LD-2, plus LD-1 registrations (42 of the 1,760), for the 33 clients [V wave 43C] in that file plus seven sponsor parents and distributors (Charles Schwab, FMR/Fidelity Investments, Vanguard Group, Morgan Stanley, Goldman Sachs, BNY, TIFIN). That is **1,760 filings** (latest version of each) for 35 entities. TIFIN has no LDA filings [C].

- All **359** filings in the earlier file are recovered. **339** name DAFs in their own text; the other 20 were captured by the earlier pass through the QCD-to-DAF bill number [C].
- **509** filings carry at least one policy tag: charitable deduction, §4966, P.L. 119-21/OBBBA or QCD. **255** of them do not name DAFs and are **not** in the earlier file. These are the "DAF-adjacent, unnamed" filings this item asked for. Their whole-filing amounts total **$43.3m** (not issue-specific) [C]. Of these, 86 filings ($29.6m) carry only the OBBBA tag once the H.R. 3975 false QCD matches are removed. They are mostly the parents’, AICPA’s, SIFMA’s and KPMG’s retirement or business-tax lines. The charity-relevant core, with a charitable-deduction, QCD or §4966 tag, is 169 filings ($13.65m) [V wave 43C]
- Charitable-deduction lobbying that does not name DAFs comes from the **charity-side coalition**: 161 new filings. Independent Sector has 45, American Heart Association 29, Philanthropy Roundtable 19, CASE 15, AFP 13, United Philanthropy Forum 12 and Global Generosity 10 [C].
- **§4966 is never lobbied without naming DAFs.** Two SIFMA self-filed lines do cite §4966 by number: “Section 4966 Donor Advised Fund Regulations” (2023 Q4) and “IRS proposed rule regarding Section 4966 Donor Advised Funds” (2024 Q1). The matches sit past the CSV’s 1,500-character `line_text` cut, and both lines also name DAFs. No other 2021–26 line cites [V wave 43C]"4966" or "taxable distribution". 71 of the 73 filings tagged §4966 got the tag from DAF-plus-regulation wording, and the two SIFMA filings from the section number. All 73 also name DAFs [V wave 43C]
- **The sponsor parents lobbied on OBBBA, but not on its charitable provisions.** FMR, Goldman Sachs, Morgan Stanley and Vanguard Group have 42 OBBBA-tagged filings between them. Their lines cover retirement, financial-services, corporate or international tax. None of their 2021–26 lines names DAFs, §4966 or QCDs [C].
  - The one charitable-deduction line among the parents is FMR's 2026 Q3 filing. It lists **H.R. 9173, the "Charitable Deductions for Digital Asset Donations Act"** inside a digital-asset tax list [P].
  - Only the charity-side and professional clients put OBBBA and the charitable deduction on the same line. That happens in **37 filings**, from Independent Sector, Council on Foundations, AHA, AFP, United Philanthropy Forum, AICPA, CFAI, CASE, Global Generosity and KPMG. NPT and Vanguard Charitable tie P.L. 119-21 to DAF or tax-exempt issues on their own lines [C/P].
- **LD-203.** Eight self-filing registrants among the sponsor parents and DAF-program financial firms filed a total of 6,482 organisation-level contribution items for 2021 to 2026 H1. The largest totals are UBS PAC at $7.42m FECA, Morgan Stanley at $6.52m ($2.19m FECA plus **$4.34m honorary expenses**), Goldman Sachs at $3.58m (including a **$1.0m** presidential inaugural committee item), Fidelity (FMR) PAC at $3.49m, Ameriprise PAC at $0.93m and the Vanguard committee at $0.80m. Schwab Corp. and Thrivent filed "no contributions" organisation reports [C].
  - No LD-203 item is paid to or honours a national DAF sponsor. Most of Morgan Stanley’s 98 honorary items go to nonprofits, such as housing groups, Goodwill and the American Red Cross; six have ‘charity’ or ‘foundation’ in the payee name. One of them, $75,000 to Arlington Community Foundation, goes to a community foundation, a type that usually sponsors DAFs (not checked for this one) [V wave 43C]
  - The DAF sponsors themselves (Vanguard Charitable, NPT, AEF, Ren, NCF, the community foundations) all lobby through outside firms. LD-203 is filed by registrants, not clients, so they have no attributable LD-203.

**(B) Breach registers.** Massachusetts (OCABR annual reports) and Vermont (AGO) were readable. Maine returned HTTP 403 to robots.txt and to the register, so nothing was taken from it.

| Notice | Massachusetts: MA residents, data types (date reported) | Vermont: VT residents, data types (date) | Entity named on the register |
|---|---|---|---|
| Vanguard, 2026-07 | **1,224**; SSN, financial account (2026-11-12) | **94**; Social Security Numbers (2026-11-04) | Vanguard Group (Inc.) |
| Ameriprise, 2026-03 | **2,216**; SSN, financial account (2026-04-17) | **83**; SSN, financial account codes, credit/debit info (2026-04-17) | Ameriprise Financial, Inc. |
| Fidelity, 2024-08 | **2,768**; SSN, financial account, driver's licence (2024-10-09) | not listed (archive covers this period) | Fidelity Investments |
| TD Ameritrade/Schwab (MOVEit), 2023-05 | **1,103**; SSN, account number, driver's licence (2023-08-08) | not listed (archive covers this period) | TD Ameritrade, Inc. and Charles Schwab & Co., Inc., a TD Ameritrade affiliate |
| Fidelity Investments Life / Empire Fidelity (IMS), 2023-10 | **2,528**; SSN, financial account (2024-03-01) | not listed | Fidelity Investments Life Insurance Company & Empire Fidelity Investments Life Insurance Company |
| Infosys McCamish's own notice (same incident) | **72,858**; SSN, medical, financial account, driver's licence, card (2024-06-28) | posted 2024-06-27; the sample letter's data elements are a mail-merge field. Its Rhode Island paragraph says "This incident affected 2,424 individuals." | Infosys McCamish Systems, LLC |
| Morgan Stanley, 2021 | **407**; SSN (2021-07-02) | outside the archive (it starts 2022-03) | Morgan Stanley |

**No register entry names a charitable or DAF entity.** The 570 Vermont table rows, 2,463 Vermont archived notice titles, 13,760 parsed Massachusetts rows (2021–2026) and the one opened Vermont PDF were all searched. None mentions Fidelity Charitable, Schwab Charitable/DAFgiving360, Vanguard Charitable, GIFT, RCF/DonorFirst, NPT, "charitable gift fund" or "donor-advised" [C]. Every notice is filed by the parent or a vendor. That fits the earlier finding from California (direction-patents-security.md §3.3).

---

## A. Lobbying (LDA)

### A.1 Method [C]

- **Source.**
  - lda.gov REST API v1, anonymous, no key and no login.
  - The terms (https://lda.gov/api/tos/) allow anonymous use at 15 requests a minute. robots.txt allows `/api/v1/` with `Crawl-delay: 4`. The script waits 4.2 s between calls.
  - The OpenAPI document says the lda.senate.gov API was deprecated on 2026-01-09 and **sunset on 2026-07-31**, with lda.gov as its successor. lda.senate.gov returned HTTP 503 "Site Under Maintenance".
  - Required citation: data retrieved from LDA.gov on 2026-11-20. "Senate Office of Public Records cannot vouch for the data or analyses derived from these data after the data have been retrieved from LDA.gov."
- **Targets (44 queries, 36 entities).**
  - **The 33 client names in the earlier CSV** are queried by name. Results are accepted when the normalised client name matches exactly; normalising drops case, punctuation, a leading "The" and suffixes such as Inc or LLC. Alias groups merge the two JFNA names, the two Philanthropy Roundtable names, and "REN" with "REN ACQUISITION COMPANY LLC". "GoFundMe" is added as an alternate query.
  - **The seven parents** are matched by name pattern:
    - Schwab: `^CHARLES SCHWAB`, covering the Corporation and & Co.;
    - FMR: `^FMR LLC`, `^FIDELITY INVESTMENTS` and `^FIDELITY MANAGEMENT & RESEARCH`;
    - Vanguard Group: "Vanguard", "Vanguard Group" or "The Vanguard Group, Inc." The client named "VANGUARD" is a Pennsylvania mutual fund group represented by Porterfield, Fettig & Sears;
    - Morgan Stanley and Goldman Sachs: any name containing them;
    - BNY: Bank of New York Mellon, BNY Mellon and the former BNY Mellon Corp.;
    - TIFIN.
  - Because Charles Schwab Corporation is already among the 33, Schwab appears as a single entity, "CHARLES SCHWAB".
- **Pull.** `/filings/?client_name=…&filing_dt_posted_after=2021-01-01`, all pages. A query with more than 600 hits (only "REN") goes through `/clients/` first, then `/filings/?client_id=` for each accepted client record. Only filings with `filing_year` ≥ 2021 are kept. For each registrant, client, year, period and report-or-registration, the latest posted version is kept, as in the earlier method.
- **Tagging.** Each lobbying-activity line (one issue code's specific-issues text) is tested with the regexes in `TAGS`:
  - `daf_named`: "donor advised", DAF/DAFs, Accelerating Charitable Efforts, ACE Act. "DAF" is ignored when the line mentions the Air Force and no donor.
  - `charitable_deduction`: charitable contribution, deduction, giving, donation or gift; non-itemizer; universal charitable; "Charitable Act"; §170; "charitable tax".
  - `s4966`: "4966", "taxable distribution", or "donor-advised fund(s)" within a few words of "regulation".
  - `obbba`: 119-21, One Big Beautiful, OBBBA; also "H.R. 1" in 2025+ filings.
  - `qcd`: qualified charitable distribution, QCD, charitable or IRA rollover, Legacy IRA; also H.R. 2891 or S. 3975 in 2025+ filings.
  - `charity_sector`: charit, philanthrop, nonprofit, exempt organisation, foundation. This is context only. It also fires on non-giving bills such as the "Retirement Fairness for **Charities** and Educational Institutions Act" (403(b) investments), which accounts for most of Vanguard Group's 32 charity_sector filings.
- **Filing flags.**
  - `filing_names_daf`: any line in the filing names DAFs.
  - `filing_has_policy_tag`: any line carries one of the four policy tags.
  - `daf_adjacent_unnamed`: a policy tag and no DAF naming anywhere in the filing.
  - `in_prior_daf_csv`: the filing UUID appears in the earlier 359-row file.

### A.2 Coverage [C]

| | Value |
|---|---:|
| Raw filing rows pulled (before de-duplication) | 2,059 |
| Filings kept (latest version, 2021+) | 1,760 |
| Entities with ≥1 filing | 35 of 36 (TIFIN: none) |
| Earlier 359 filings recovered | 359 |
| Lines carrying any tag (rows in the CSV) | 1,041 |
| Filings with a policy tag | 509 |
| …that name DAFs | 339 named DAFs in total; see A.3 |
| …DAF-adjacent and unnamed | 275, of which **255 are new** (20 were the earlier QCD-bill rows) |

Filings by year: 2021: 296, 2022: 295, 2023: 304, 2024: 322, 2025: 319, 2026: 224 (through Q3).

Filings carrying each tag (each filing counted once per tag): daf_named 339; charitable_deduction 335; s4966 73; obbba 140; qcd 132; charity_sector 576. The qcd count falls to 126 (2025: 18; 2026: 33) once six AICPA and KPMG filings are removed. They were matched only on H.R. 3975, the Tax Fairness for Disaster Victims Act, not on the QCD bill S. 3975. The 509 and the 255 are unchanged, because all six also carry OBBBA [V wave 43C]

By year:

| Year | DAF named | Charitable deduction | §4966 | OBBBA | QCD | Adjacent, unnamed |
|---|---:|---:|---:|---:|---:|---:|
| 2021 | 63 | 48 | 0 | 0 | 24 | 22 |
| 2022 | 68 | 55 | 0 | 0 | 37 | 27 |
| 2023 | 44 | 56 | 13 | 0 | 10 | 40 |
| 2024 | 73 | 64 | 28 | 0 | 4 | 29 |
| 2025 | 53 | 66 | 19 | 93 | 20 | 93 |
| 2026 | 38 | 46 | 13 | 47 | 37 | 64 |

- §4966 / DAF-regulation lines first appear in 2023. Philanthropy Roundtable's earliest is the generic "regulatory issues relating to donor-advised funds" (2023 Q1). The specific lines, such as Fidelity Charitable's "Donor advised funds regulation" and SIFMA's, start in 2023 Q4, after the November 2023 DAF proposed regulations. Apart from two SIFMA lines (2023 Q4 and 2024 Q1) that cite “Section 4966” beyond the CSV’s 1,500-character cut, no line cites [V wave 43C]"4966" by number, so the tag rests on the DAF-plus-regulation wording.
- OBBBA drives the 2025 jump in unnamed adjacent filings [C].

### A.3 By entity [C]

Amounts are reported income (outside firms) plus expenses (self-filers) per filing, summed over 2021–26. They cover **all issues** in the filing.

| Entity | Group | Filings | All-filing $ | Names DAF | Policy tag | Adjacent unnamed (new) | Main tags (filings) |
|---|---|---:|---:|---:|---:|---:|---|
| Vanguard Charitable | sponsor | 24 | 1.74m | 24 | 6 | 0 | OBBBA 3, QCD 6 |
| National Philanthropic Trust | sponsor | 25 | 1.09m | 25 | 23 | 0 | chardeduct 15, OBBBA 8, QCD 4 |
| Fidelity Charitable Gift Fund | sponsor | 23 | 0.18m | 17 | 7 | 0 | §4966 7 ("Donor advised funds regulation") |
| American Endowment Foundation | sponsor | 13 | 0.37m | 13 | 13 | 0 | chardeduct 13 |
| Ren / Ren Acquisition | vendor | 18 | 0.60m | 18 | 6 | 0 | chardeduct 6 |
| National Christian Foundation | sponsor | 8 | 0.11m | 8 | 8 | 0 | chardeduct 8 |
| Greater Washington CF | CF | 23 | 0.24m | 23 | 23 | 0 | chardeduct 23, §4966 7 |
| NY Community Trust | CF | 23 | 0.21m | 9 | 9 | 0 | §4966 7 |
| GoFundMe | platform | 4 | 0.08m | 4 | 4 | 0 | §4966 3 |
| **FMR / Fidelity Investments** | parent | 267 | 20.77m | 0 | 11 | **11** | OBBBA 10; chardeduct 1 (H.R. 9173) |
| **Vanguard Group** | parent | 93 | 15.74m | 0 | 12 | **12** | OBBBA 12 |
| **Goldman Sachs** | parent | 147 | 27.16m | 0 | 12 | **12** | OBBBA 12 |
| **Morgan Stanley** | parent | 98 | 25.85m | 0 | 8 | **8** | OBBBA 8 |
| **BNY** | parent | 44 | 2.29m | 0 | 0 | 0 | – |
| **Charles Schwab** (Corp. and & Co.) | parent | 142 | 19.22m | 1 | 1 | 1 | ACE Act 2022 (DAF named); OBBBA remittance tax 2025 |
| TIFIN | parent | 0 | – | – | – | – | – |
| UBS Americas | financial | 23 | 3.29m | 11 | 0 | 0 | – |
| Ameriprise | financial | 23 | 6.85m | 0 | 4 | 1 | QCD 3 (H.R. 2891) |
| Edward Jones | financial | 23 | 0.54m | 1 | 4 | 0 | QCD 4 |
| Thrivent | financial | 35 | 4.54m | 0 | 4 | 0 | QCD 4 (H.R. 2891) |
| SIFMA | trade assn | 46 | 44.57m | 2 | 10 | 8 | OBBBA 8, §4966 2 |
| Independent Sector | nonprofit assn | 66 | 2.66m | 1 | 46 | **45** | chardeduct 46, QCD 12, OBBBA 8 |
| American Heart Association | charity | 91 | 6.98m | 7 | 43 | **36** | chardeduct 36, QCD 24 |
| Philanthropy Roundtable | donor advocacy | 88 | 4.40m | 57 | 58 | 25 | §4966 33, chardeduct 26 |
| AICPA | professional | 92 | 34.22m | 6 | 23 | 21 | OBBBA 23 |
| CASE | nonprofit assn | 23 | 0.62m | 8 | 23 | 15 | chardeduct 23, QCD 9 |
| AFP | nonprofit assn | 25 | 0.20m | 11 | 24 | 13 | chardeduct 24 |
| United Philanthropy Forum | philanthropy assn | 19 | 0.28m | 4 | 19 | 12 | chardeduct 17, QCD 7 |
| Global Generosity | donor advocacy | 23 | 0.04m | 9 | 19 | 10 | chardeduct 19 |
| Council on Foundations | philanthropy assn | 50 | 1.90m | 24 | 25 | 2 | QCD 23, OBBBA 6 |
| CF Awareness Initiative | CF coalition | 23 | 4.02m | 19 | 23 | 4 | chardeduct 23, §4966 6 |
| JFNA | nonprofit assn | 63 | 6.08m | 27 | 22 | 3 | chardeduct 20, QCD 9 |
| Individual client (name withheld) [V wave 43C] | individual | 21 | 0 | 1 | 7 | 7 | chardeduct 7 |
| KPMG | accounting | 46 | 12.56m | 1 | 6 | 5 | OBBBA 6 |
| Americans for Tax Reform | tax advocacy | 23 | 1.26m | 6 | 3 | 3 | OBBBA 3 |
| Philanthropy Southwest | philanthropy assn | 5 | 0.03m | 2 | 3 | 1 | chardeduct 3 |

**Reading [C/P/I].**

- **Charitable deduction.** The 161 new unnamed charitable-deduction filings come mostly from operating-charity and sector associations. Their lines name the Charitable Act (S. 566/H.R. 3435 in the 118th Congress; S. 317/H.R. 801 in the 119th), "universal charitable deduction", and in 2025 "Provisions affecting nonprofits and private foundations in Title VII of H.R. 1 … 1% floor on corporate charitable contributions" (Independent Sector via Ernst & Young, 2025 Q2) [P]. This is the coalition that shaped the non-itemizer deduction and the floors in P.L. 119-21. The DAF sponsors lobbied on the same law but framed it around DAFs [I].
- **QCD.** The 37 new unnamed QCD-tagged filings include 3 AICPA filings tagged only because the bill pattern matches H.R. 3975 (a disaster-relief bill). The 34 genuine ones are mostly Legacy IRA / IRA charitable-rollover lines: AHA 17, Independent Sector 11, AFP 4 [V wave 43C]. The QCD-to-DAF bill H.R. 2891 also appears in Ameriprise's and Thrivent's own filings (2025–26), which the earlier pass already caught by bill number. Edward Jones' outside firm names "qualified charitable distributions to donor advised funds" outright [P].
- **§4966.** Every filing tagged for §4966 also names DAFs. Lobbying on the DAF regulations is fully visible to a DAF keyword search, and the earlier coverage limit does not apply to it [C].
- **Parents.** FMR, Vanguard Group, Goldman Sachs and Morgan Stanley together report $89.5m of all-issue lobbying over 2021–26. In 605 filings, none of their lines names DAFs, §4966 or QCDs.
  - Their 42 OBBBA filings concern "Retirement savings tax incentives, including the relevant provisions of H.R.1" (FMR), "Tax issues related to financial services, including P.L. 119-21" (Goldman via Capitol Tax Partners), "General Business and International Tax Provisions" (Morgan Stanley) and similar [P].
  - So the parents' lobbying does not reach the DAF provisions, as far as the filings show. Their DAF sponsors lobby separately: Fidelity Charitable through FMR LLC itself, Vanguard Charitable through K&L Gates. Schwab Charitable, Morgan Stanley GIFT and the Goldman Sachs Philanthropy Fund have no LDA presence [C/I].

### A.4 LD-203 contributions (self-filing sponsor parents and DAF-program financial firms) [C]

- **Scope.** Registrants that file for themselves and are a target sponsor, a sponsor parent or a target financial firm. FMR LLC files for both Fidelity Charitable and FMR.
- **Method.** `/contributions/?registrant_id=…&filing_dt_posted_after=2021-01-01`. One report is kept per registrant, filer type, lobbyist, year and half (the latest posted, so amendments replace originals).
- **What the CSV holds.** Organisation-filed items are kept line by line. Lobbyist-filed items are only counted and summed, and no individual names are reproduced.

| Registrant (linked target) | Org reports | Org items | Org total $ | FECA | Honorary (HE) | Presidential library / inaugural (PLE / PIC) | Lobbyist reports / items / $ |
|---|---:|---:|---:|---:|---:|---:|---|
| UBS Americas Inc. | 11 | 1,989 | 7,420,000 | 7,420,000 | 0 | 0 | 32 / 17 / 33,021 |
| Morgan Stanley & Co. LLC | 11 | 989 | 6,523,952 | 2,188,750 | 4,335,202 | 0 | 44 / 0 / 0 |
| The Goldman Sachs Group, Inc. | 11 | 1,297 | 3,575,782 | 2,575,782 | 0 | PIC 1,000,000 | 76 / 137 / 143,000 |
| FMR LLC (Fidelity Charitable; FMR) | 11 | 1,217 | 3,488,500 | 3,458,500 | 25,000 | PLE 5,000 | 67 / 150 / 132,000 |
| Ameriprise Financial, Inc. | 11 | 558 | 931,000 | 931,000 | 0 | 0 | 22 / 7 / 8,000 |
| Vanguard Group | 11 | 432 | 796,500 | 796,500 | 0 | 0 | 41 / 1 / 250 |
| The Charles Schwab Corporation | 11 (all "no contributions") | 0 | 0 | 0 | 0 | 0 | 39 / 35 / 18,250 |
| Thrivent Financial for Lutherans | 5 (all "no contributions") | 0 | 0 | 0 | 0 | 0 | 12 / 2 / 800 |

- Eleven organisation reports cover 2021 mid-year through 2026 mid-year.
- The six charity-type HE or PLE items paid to charities or foundations go to unrelated recipients:
  - Morgan Stanley: Charity Vision International, Arlington Community Foundation, and two Horton's Kids events;
  - FMR: Congressional Black Caucus Foundation, John F. Kennedy Library Foundation.
- None goes to a national DAF sponsor. The $75,000 Arlington Community Foundation item goes to a community foundation, a type that usually sponsors DAFs [V wave 43C]
- BNY, Edward Jones, Vanguard Charitable, NPT, AEF, Ren, NCF, GoFundMe and the community foundations had no self-filed registration matched to the target, so they have no attributable LD-203.

---

## B. State breach-notice registers

### B.1 Method [C]

- **Robots, logged by the script in `robots_log.json`.**
  - `ago.vermont.gov/robots.txt` (HTTP 200): the `*` group disallows only admin, search, user, calendar and core paths, and the `/documents/` disallow is commented out. The listing, document pages and `/sites/ago/files/documents/*.pdf` are allowed.
  - `www.mass.gov/robots.txt` (200): `/lists/` and `/doc/` are allowed; only `/doc/courts-dwnld-*` is disallowed.
  - `www.maine.gov/robots.txt` and `apps.web.maine.gov/robots.txt` (the latter redirects to the former): both HTTP 403 (CloudFront "Request blocked"). The Maine viewer list (`/agviewer/content/ag/985235c7-…/list.html`) also returned 403, and the old `apps.web.maine.gov/online/aeviewer/ME/40/list.shtml` returned 404. **Maine was not used.** The user agent was not changed.
  - The generic user agent was `research-script/1.0`. A curl probe with the same user agent got 403 from www.mass.gov, but Python urllib got 200, and only the latter was used.
- **Vermont.**
  - Since 2026-04-17 the Security Breach Notices page posts a **summary table**: date reported, organisation, organisation type, number of VT residents affected, categories of data. It no longer posts notice PDFs, and the page says copies can be requested by email (not done; no outreach).
  - Under it is an **archive of 2,463 posted notices** across 50 listing pages, effectively 2022-03 to 2026-06-13 plus three older strays.
  - Archive titles matching a notice were opened and the posted PDF read with `pdftotext`.
- **Massachusetts.**
  - OCABR annual "Data Breach Notification Report" PDFs for 2021–2026 were linked from the list page and read with `pdftotext -layout`.
  - A row is any line with a reported date in its first 45 characters. Organisation names wrapped onto neighbouring lines are reattached.
  - MA residents affected is the integer just before the trailing Yes/No flags.
  - **Data-type flags.**
    - 2023: SSN, account number, driver's licence, credit/debit.
    - 2024–26: SSN, medical, financial account, driver's licence, credit/debit.
    - 2021–22: blanks rather than "No", so each "Yes" was assigned to the nearest header column. Those years also carry "credit monitoring provided", which is not a data type and is excluded.
  - Rows parsed: 2021: 2,602; 2022: 2,226; 2023: 2,427; 2024: 2,289; 2025: 2,196; 2026: 2,020; 13,760 in total. 39 rows have no parseable count.
- **Matching.** Names were matched with the patterns in `NOTICES`. The candidate entry for each notice is the largest-count row whose report date falls in a window set from the breach date and the California filing dates in `daf-security-incidents-2021plus.csv` (SI-08, SI-09, SI-11, SI-13, SI-14, SI-15). All rows for these entities in 2021–26 are kept in the CSV, with `candidate_for_notice` = Y/N.
- **Charity test.** A strict pattern (`DAF_ENTITY`) was run over all VT table names, VT archive titles, MA organisation names and the opened VT PDF text: Fidelity Charitable / Fidelity Investments Charitable, Schwab Charitable, DAFgiving360, Vanguard Charitable / Charitable Endowment Program, GIFT / Global Impact Funding Trust, Renaissance Charitable, RCF, DonorFirst, donor-advised, "charitable gift fund", National Philanthropic Trust.

### B.2 Results [P/C]

- **Vanguard (BN-VAN-2026).**
  - Vermont table: "Vanguard Group, Inc.", Financial Services, reported 11-4-2026, **94** VT residents, "Social Security Numbers".
  - Massachusetts 2026: "Vanguard Group Inc.", reported 12-Nov-26, **1,224** MA residents, SSN = Yes, financial account = Yes, medical / driver's licence / card = No.
  - These are the first register-sourced counts for this incident. The earlier record (SI-13) had only a secondary "couple hundred thousand" and a secondary report of the VT 94, which is now confirmed from the register.
- **Ameriprise (BN-AMP-2026).**
  - Vermont: reported 4-17-2026, **83** VT residents; SSN, financial account codes, credit or debit account info.
  - Massachusetts 2026 #2026-604: reported 17-Apr-26, **2,216** MA residents; SSN and financial account.
  - Ameriprise files many small notices. Massachusetts lists 20 Ameriprise rows in 2021–26, most of them for 1 to 6 residents.
- **Fidelity Investments (BN-FID-2024).** Massachusetts 2024: "Fidelity Investments", reported 09-Oct-24, **2,768** MA residents; SSN, financial account, driver's licence. The Vermont archive covers this date range but has no Fidelity Investments notice. The national 77,099 figure in SI-08 still rests on a secondary source citing Maine, which is unread.
- **TD Ameritrade / Schwab (BN-SCH-2023).**
  - Massachusetts 2023 #30224: reported 8-Aug-23, **1,103** MA residents; SSN, account number, driver's licence (no card).
  - The register names the filer as "TD Ameritrade, Inc. and Charles Schwab & Co., Inc., a TD Ameritrade affiliate" (wrapped across three lines). Five Schwab or TDA rows fall in the window; the other four are 1 to 15 residents.
- **Fidelity Investments Life / Empire Fidelity, via IMS (BN-FLI-2023).** Massachusetts 2024 #2024-428: reported 01-Mar-24, **2,528** MA residents, Insurance Company type; SSN and financial account.
- **IMS's own notice (BN-IMS-2023, the same October–November 2023 ransomware).**
  - Massachusetts 2024: "Infosys McCamish Systems, LLC", Technology, reported 28-Jun-24, **72,858** MA residents. All five data flags are Yes.
  - The Vermont archive posted IMS's sample consumer letter on 2024-06-27. It dates the unauthorised activity to 2023-10-29 to 2023-11-02, leaves the data elements as a merge field (`<<b2b_text_1(name, data elements)>>`), and does not name any client: no Fidelity entity and no charitable entity.
- **Morgan Stanley (BN-MS-2021).** Massachusetts 2021 #21714: "Morgan Stanley", reported 7/2/2021 (the same day as the California filing in SI-15), **407** MA residents; SSN, with credit monitoring provided. The Vermont archive starts in 2022-03, so 2021 is not covered.
- **Charitable or DAF entity named: none** in any register entry or opened notice [C].
  - The broad pattern (charit, philanthrop, donor, foundation) finds only unrelated organisations: Catholic Charities affiliates, International Orthodox Christian Charities, the Indiana Donor Network (organ donation), and medical or research foundations.
  - The registers therefore cannot show whether DAF donor records were inside the breached parent systems. Only the sample notices could say, and since April 2026 Vermont no longer posts them (P-B3903-02).

### B.3 What this changes [I]

- Every parent notice names only the parent or vendor, and the state counts are modest:
  - Vanguard: 94 VT, 1,224 MA;
  - Ameriprise: 83 VT, 2,216 MA;
  - Fidelity: 2,768 MA.
- The IMS vendor incident is far larger: 72,858 MA residents for IMS's own notice alone. It also covers the most data types: SSN, medical, financial account, driver's licence and card.
- For DAF trust risk, the vendor layer (recordkeepers and administrators) is the one to watch, not the brokerage parents.

---

## Limits

1. **Keyword tags are textual.** A filing can lobby on DAFs or charitable rules under wording the regexes miss, such as "tax-exempt organization issues" alone or "Title VII". `charity_sector` over-captures 403(b) "Retirement Fairness for Charities" bills. `obbba` on parent filings mostly reflects non-charitable titles of the law. The `qcd_bill` pattern also matches H.R. 3975 (six false positives), and the LD-203 CSV’s `honoree_name` column held individual names; the script now withholds them (and individual payees) on non-FECA items [V wave 43C; redaction applied 2026-11-20]
2. **Amounts are whole-filing** and cover all issues; they are not DAF- or charity-specific. Summing them across entities double-counts nothing, because each filing belongs to one client. They are still not a DAF lobbying spend.
3. **Client-bounded universe.** Only the 33 clients and seven parents were pulled. Other organisations lobbying on the charitable provisions of OBBBA are out of scope (P-B3903-03).
4. **Name matching.** Client records with very different names (for example, a subsidiary under a new brand) can be missed. TIFIN has no client record under that string. BNY matched only "Bank of New York Mellon" records, because no client record starts with "BNY".
5. **LD-203 attribution.** It is filed by registrants and their lobbyists, not clients. Outside-firm LD-203s are not attributed to their clients. Lobbyist-filed items are summed, not itemised.
6. **Massachusetts parsing.** PDF-to-text layout varies by year and wraps long names. Data-type flags for 2021–22 come from column position. Each candidate row was checked against its raw line, which is kept in `evidence`, but the other rows were not all checked by hand. Massachusetts gives no breach date or description, so candidates are matched by report-date window and size.
7. **State counts only.** Massachusetts and Vermont give residents of their own state. National totals need Maine (blocked) or the notices themselves.
8. **Vermont coverage.** The archive runs from about 2022-03 to 2026-06-13 and the table from 2026-04-17. A missing notice in that span can mean the AGO did not post it, not that none was filed.

---

## Data dictionary

### `data/mission-2026-11-14/lda-daf-adjacent-2021plus-2026-11-20.csv` (1,041 rows; one row per tagged lobbying-activity line)

| Column | Meaning |
|---|---|
| filing_uuid, filing_year, filing_period, filing_type, dt_posted | LDA filing identifiers (latest version kept per registrant, client, year, period) |
| registrant, registrant_id, client, client_id | As filed (LDA ids) |
| target_entity | Entity group (normalised client name or parent group) |
| target_source | `csv33` (client in the earlier DAF CSV) or `parent7` (added sponsor parent or distributor) |
| target_category | Category from the earlier CSV, or `sponsor_parent_or_distributor` |
| sponsor_link | For parents, the DAF sponsor brand linked in repo research |
| self_filer | Y if the registrant is the client (or FMR for Fidelity) |
| income_usd, expenses_usd | Whole-filing amounts as reported |
| line_no, issue_code | Position and general issue code of the activity line |
| tag_daf_named, tag_charitable_deduction, tag_s4966, tag_obbba, tag_qcd, tag_charity_sector | Line-level tags (Y/N); regexes in A.1 |
| filing_names_daf | Any line of the filing names DAFs |
| filing_has_policy_tag | Any line of the filing carries one of the four policy tags |
| daf_adjacent_unnamed | Policy tag present and no DAF naming in the filing |
| in_prior_daf_csv | UUID present in `daf-lobbying-lda-2021plus.csv` |
| government_entities | Entities contacted for that line |
| line_text | Specific-issues text (whitespace-collapsed, first 1,500 characters) |
| filing_document_url, api_url | LDA print view and API record |

### `data/mission-2026-11-14/lda-ld203-daf-sponsor-contributions-2021plus-2026-11-20.csv` (6,482 rows; organisation-filed LD-203 items)

| Column | Meaning |
|---|---|
| registrant, registrant_id, linked_target | Self-filing registrant and the target entity or entities it files for |
| filing_uuid, filing_year, filing_period, filing_type | LD-203 report (latest version per registrant and half-year) |
| contribution_type | feca, he (honorary), me (meeting), ple (presidential library), pic (presidential inaugural) |
| contributor_name, payee_name, honoree_name | As filed for FECA items (contributor is the PAC or the organisation; payees are committees, honorees officeholders). For honorary-expense and other non-FECA items, honoree names are replaced by “[individual names withheld]” and payees naming a person by “[individual payee withheld]” (privacy) |
| amount_usd, contribution_date | As filed |
| pacs | PACs listed on the report |
| filing_document_url | LDA print view |

### `data/mission-2026-11-14/breach-notices-daf-parents-2026-11-20.csv` (68 rows)

| Column | Meaning |
|---|---|
| notice_id, notice_label | Target notice (BN-VAN-2026, BN-AMP-2026, BN-FID-2024, BN-SCH-2023, BN-FLI-2023, BN-IMS-2023, BN-MS-2021) |
| register | Vermont AGO summary table, Vermont AGO archive, Massachusetts OCABR annual report YYYY, or Maine AG |
| register_status | `listed`, `no entry in reporting window`, or `blocked: …` |
| candidate_for_notice | Y = the register entry taken as this notice (largest count in the report-date window); N = another entry for the same entity in 2021–26 |
| entity_named | Organisation name as on the register (wrapped lines reattached for centred 2024+ MA rows) |
| date_reported | Date reported to the state (ISO) |
| number_affected_state | Residents of that state affected, as listed |
| number_affected_stated_in_notice | Count sentences found in an opened notice PDF |
| data_types_register | Data categories from the register (MA Yes flags or VT category text) |
| data_types_in_notice_text | Data elements stated in an opened notice ("What information was involved") |
| daf_entity_named, daf_terms_found | Strict DAF/charity entity test on the name or notice text |
| entries_for_entity_in_window | Rows for the entity in the notice's report-date window |
| matched_on | Which text matched (organisation name, notice title, MA main line) |
| source_url, pdf_url | Register page or annual PDF; posted notice PDF |
| evidence | Raw register line or row, flags, and the wrapped name |

---

## Source register

| Id | Source | Accessed | URL |
|---|---|---|---|
| L1 | lda.gov API root and filings endpoint | 2026-11-20 | https://lda.gov/api/v1/filings/ |
| L2 | lda.gov contributions (LD-203) endpoint | 2026-11-20 | https://lda.gov/api/v1/contributions/ |
| L3 | lda.gov API terms of service (anonymous 15/min; citation clause) | 2026-11-20 | https://lda.gov/api/tos/ |
| L4 | lda.gov OpenAPI document (lda.senate.gov sunset 2026-07-31; page_size ≤ 25) | 2026-11-20 | https://lda.gov/api/openapi/v1/ |
| L5 | lda.gov robots.txt (Allow /api/v1/, Crawl-delay 4) | 2026-11-20 | https://lda.gov/robots.txt |
| L6 | lda.senate.gov robots.txt (HTTP 503 maintenance page) | 2026-11-20 | https://lda.senate.gov/robots.txt |
| L7 | Example filings cited: FMR 2026 Q3 (H.R. 9173); Independent Sector 2025 Q2 (Title VII of H.R. 1); Vanguard Charitable 2025 Q2 (P.L. 119-21) | 2026-11-20 | linked per row in `filing_document_url` of the lobbying CSV |
| B1 | Vermont AGO Security Breach Notices (summary table and archive listing) | 2026-11-20 | https://ago.vermont.gov/categories/security-breach-notices |
| B2 | Vermont AGO: Infosys McCamish Systems notice (2024-06-27) and PDF | 2026-11-20 | https://ago.vermont.gov/document/2024-06-27-infosys-mccamish-systems-data-breach-notice-consumers ; https://ago.vermont.gov/sites/ago/files/documents/2024-06-27%20Infosys%20McCamish%20Systems%20Data%20Breach%20Notice%20to%20Consumers.pdf |
| B3 | ago.vermont.gov robots.txt | 2026-11-20 | https://ago.vermont.gov/robots.txt |
| B4 | Massachusetts OCABR Data Breach Notification Reports (list) | 2026-11-20 | https://www.mass.gov/lists/data-breach-reports |
| B5 | Massachusetts annual reports 2021–2026 (PDF) | 2026-11-20 | https://www.mass.gov/doc/data-breach-report-2021/download … https://www.mass.gov/doc/data-breach-report-2026/download |
| B6 | www.mass.gov robots.txt | 2026-11-20 | https://www.mass.gov/robots.txt |
| B7 | Maine AG breach viewer (HTTP 403) and robots.txt (HTTP 403) | 2026-11-20 | https://www.maine.gov/agviewer/content/ag/985235c7-cb95-4be2-8792-a1252b4f8318/list.html ; https://www.maine.gov/robots.txt |
| R1 | Earlier LDA scan and DAF CSV | repo | research/mission-2026-11-14/direction-policy-lobbying-obbba.md §2; data/mission-2026-11-14/daf-lobbying-lda-2021plus.csv |
| R2 | Earlier security-incident rows SI-06 to SI-15 (California AG links) | repo | data/mission-2026-11-14/daf-security-incidents-2021plus.csv; research/mission-2026-11-14/direction-patents-security.md §3.3 |

Reproduce: `python3 scripts/mission_lda_breach.py . --cache <dir> [--step lda|breach|all] [--offline]`. All HTTP responses are cached in `<dir>`, and `--offline` rebuilds the outputs from the cache.
