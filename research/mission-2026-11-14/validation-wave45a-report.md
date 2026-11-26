# Validation wave 45A: blank vs zero DAF-grant cells, and the 2026 docket submissions

**Validated:** 2026-11-20 · **Validator:** validator wave 45A · **Register:** [`data/mission-2026-11-14/validation-register-wave45a.csv`](../../data/mission-2026-11-14/validation-register-wave45a.csv) (20 rows, V45A-01 to V45A-20)

**Studies validated**
1. [b39n8-01-01-blank-vs-zero.md](b39n8-01-01-blank-vs-zero.md), its CSV and `scripts/mission_blank_vs_zero.py` (V45A-01 to -10).
2. [b39n1-01-docket-2026-submissions.md](b39n1-01-docket-2026-submissions.md), its CSV and `scripts/mission_b39n1_01_docket_2026.py` (V45A-11 to -20).

## Method

**Study 1.**
- Re-ran the script with `python3 -B`, writing the CSV and summary JSON to a scratch folder. The cache inputs were the IPS xlsx files, IRS TEOS index_2023–2026 and the existing extract990 caches.
- Wrote a separate stdlib checker. It does not use the study's modules for parsing or selection. It:
  - parses IPS's sponsor-list xlsx directly;
  - selects each EIN's same-period Form 990 from the IRS index files, taking the newest OBJECT_ID processed by 2024 and also the newest overall;
  - downloads the **raw e-file XML for every return** from the GivingTuesday mirror (361 XMLs);
  - reads Schedule D Part I lines 1(a)–4(a) with ElementTree.
- This covers all 248 blank cells, all 100 explicit IPS zeros and the 138 panel zero-years, not a spot-check of 10.
- Recomputed the panel medians on the corrected panel, and the roll-forward from the raw lines.

**Study 2.**
- Re-ran the script and compared its output with the repo CSV.
- Probed regulations.gov **once**: robots.txt, UA `research-script/1.0`.
- Checked robots.txt on each host before fetching (log below).
- Downloaded both 2024 PDFs and checked every quote page by page with pdftotext.
- Read SIFMA's full sitemap, NYSBA's reports page and master index, the reginfo.gov rule page under three pubIds, the reginfo agenda home page, OIRA's introduction PDF, the EO 12866 search, and the Adler & Colvin URLs.

**Robots and access log (2026-11-20, UA `research-script/1.0`).**

| Host | Result |
|---|---|
| gt990datalake-rawdata.s3.amazonaws.com | robots.txt 404, no rules. 361 raw XMLs fetched |
| www.regulations.gov | 403, CloudFront "Request blocked" on the single robots.txt probe. Nothing else requested |
| www.sifma.org | robots.txt has content-signal comments only, no Disallow lines. Sitemap, PGP letter page and 2024 PDF fetched |
| nysba.org | Only /wp-admin/ is disallowed. Reports page, master index and Report 1489 fetched |
| www.reginfo.gov | /robots.txt redirects (301) to /public/. Rule pages, agenda home, OIRA intro and EO 12866 search fetched |
| www.adlercolvin.com | Only /wp-admin/ is disallowed, crawl-delay 10. Two URLs fetched, 11 s apart |
| www.irs.gov | One TY2024 MeF schema page read (WebFetch). The XSD packages were not retrieved |

## Counts by study and result

| Study | Confirmed | Partially confirmed | Contradicted | Unverifiable | Total |
|---|---:|---:|---:|---:|---:|
| 1. Blank vs zero (b39n8-01-01) | 8 | 2 | 0 | 0 | 10 |
| 2. Docket 2026 (b39n1-01) | 10 | 0 | 0 | 0 | 10 |
| **All** | **18** | **2** | **0** | **0** | **20** |

V45A-15 is confirmed with a page-citation nit. V45A-17 is confirmed and also closes the study's open edition caveat.

## Findings

### Study 1: blank vs zero

1. **Everything numeric reproduces.** The script output is byte-identical to the repo CSV.
   - The independent raw-XML read gives 248 of 248 blank-filed: Schedule D is present and the DonorAdvisedFundsGrantsAmt element is absent.
   - Filed line 1(a) matches IPS's accounts cell on 248 of 248. Filed line 4(a) equals IPS's DAF-assets cell **exactly** on 248 of 248.
   - Line 2(a) is blank on the same 148 returns where IPS's contributions cell is blank.
   - Medians: IPS 9.6751% (n = 1,487); newest returns 9.6754% (n = 1,488); blanks as 0%, 7.7223% (n = 1,735); beginning-assets formula 12.1891% and 10.0188%; panel P0 9.3297%, P1 10.1929% and P2 9.8587% (n = 1,400).
   - Roll-forward: 197 sponsors; 127 with outflow ≤ 0; 55 above 10%; 35 exactly 0; 28 with identical assets in both years.
2. **Prosperity Foundation.**
   - The original return 202413209349308606 has no line 3(a) element.
   - The amendment 202521259349300817 carries AmendedReturnInd and DonorAdvisedFundsGrantsAmt 550000, which is 60.86% on IPS assets of $353,670.
   - Avenues Early Childhood Services' 2026 object is also an amended return, and line 3(a) is still blank.
3. **Extension: all 100 explicit IPS zeros are zero-filed**, not only the 49 in the repo set. This answers the study's proposal -02. IPS's blank/0 split follows the filed element on all 348 cells.
4. **Is "blank-filed" vs "zero-filed" meaningful? Partly.**
   - The format allows both forms. 103 distinct returns read carry an explicit 0 (100 IPS zeros plus 3 panel-only), and MeF accepted 256 distinct returns (248 IPS blanks plus 8 panel-only) without the element, so the element is optional. The schema does not drop zeros.
   - Every one of the 248 blank-filed returns contains other explicit zero-valued elements. One blank-filer wrote 0 on line 2(a) but left line 3(a) blank.
   - So absence records a preparer or software choice for that line, not a separate fact about grants. The distinction matters for provenance (IPS copies it faithfully) but carries no information about whether grants were made.
   - The XSD packages were not read. The IRS TY2024 MeF page links schemas for software developers but says nothing about zero handling.
5. **Interpretation challenge on §3.5.**
   - The roll-forward ignores investment return. Most FY2023 periods had positive market returns [I], so a fund paying grants about equal to its gains shows outflow ≤ 0.
   - "127 compatible with no grants" is a necessary condition, not evidence. "Blank is probably zero for most" goes further than the test allows.
   - The 35 exact-zero outflows and 28 identical asset values look like stale or carried-forward entries.
6. **Repo text.**
   - The bridge's 9.33–10.20% bracket (bridge §0 and §3.2) should now point to the filed-evidence point estimate, 9.86%.
   - 10.20% is the IPS-screened grants > 0 variant (PB2152, n = 1,344). Unscreened, the figure is 10.19% (n = 1,349). The string "10.19%" occurs nowhere in the repo.
   - The industry report's wave 37A paragraph (§11.42, line 1041) is left unchanged, as the rules require. The new §11.65 carries the update.
   - 9.86% is not a reconciliation to IPS. The universes still differ: 172 sponsors are IPS-only and 87 are not on IPS's list, and the panel has no IPS screens.

### Study 2: docket 2026 submissions

7. **Access.** regulations.gov returned 403, CloudFront "Request blocked", on the one probe. The UA was not changed. 0 of 13 letters readable is confirmed.
8. **Metadata.**
   - The script output is byte-identical to the repo CSV.
   - The repo docket summary has 249 rows, 13 of them posted in 2026: 1 on 05-13, 6 on 05-26 and 6 on 06-15.
   - The unique earlier filing IDs per organisation sum to 28.
9. **SIFMA.**
   - The sitemap holds 10,278 entries (10,277 unique), against 10,276 stated. This is a live file, and the difference is immaterial.
   - 43 /advocacy/ URLs have a lastmod in May–June 2026.
   - The only DAF letter is lastmod 2024-02-08.
   - The 2026-27 PGP letter page reads "Published on: May 29, 2026 … Issue: Treasury Clearing", with no DAF or §4966 text.
10. **NYSBA.**
    - Reports 1519–1535 are listed and none is on §4966. No. 1529 is "Amendments to Section 4968", the endowment excise tax.
    - The master index's DAF and §4966 entries are Nos. 1129, 1390 and 1489 only.
11. **Quotes.**
    - All SIFMA quotes appear verbatim on the stated pages. The p. 6 quote reads "strike subparagraphs(h)(2) and (h)(3) of proposed §53.4966-1(h)", with no space in the PDF itself.
    - All NYSBA quotes appear verbatim. The PDF breaks "arm's-length" with a hyphen at a line end on PDF 7, and "do no[t]" corrects the PDF's own typo.
    - One citation nit: the competition quote runs across printed pp. 18–19 [PDF 23–24].
    - Neither PDF contains "990" or "6033".
12. **Unified Agenda edition identified.**
    - On reginfo's edition list for RIN 1545-BI33, pubId 202510 sits after "Spring 2025" and is labelled "2026".
    - The agenda home page names the current edition the "2026 Regulatory Plan and the Unified Agenda of Federal Regulatory and Deregulatory Actions". Its OIRA introduction PDF (StaticContent/202510) was created 2026-07-01.
    - That edition shows: Final Rule Stage; Priority "Substantive, Nonsignificant"; EO 14192 "Not subject to, not significant"; Final Action 07/00/2026.
    - The Spring 2025 edition (pubId 202504) gave Final Action 05/00/2026, so the target slipped two months.
    - The July 2026 target has passed with no final rule reported.
    - The EO 12866 meeting search shows "No records found".
13. **Adler & Colvin.**
    - The 2024 joint comment PDF returns 404.
    - The 2026-08-20 post contains the "in contact with the IRS … 990 changes" sentence and no "4966".
    - It does mention donor-advised funds, as exempt from H.R. 9721's fiscal-sponsorship rules. The study does not mention this, but it does not change the study's reading.
14. **§1.5 correction warranted.** The "SS only" Unified Agenda row in direction-policy-lobbying-obbba.md can now be replaced with a primary read, and gap item 5 closed.

## Accept / modify / reject

| Study | Claim | Decision | Note |
|---|---|---|---|
| 1 | 248 of 248 blank-filed; lines 1(a) and 4(a) match | **Accept** | Independently re-read all 248 raw XMLs |
| 1 | IPS median 9.6751%, unchanged | **Accept** | |
| 1 | Prosperity amendment $550,000; newest median 9.6754% | **Accept** | |
| 1 | Blanks as 0%: 7.7223% | **Accept** | It is a bound, not an estimate |
| 1 | 49 of 49 explicit zeros zero-filed | **Accept, extend** | 100 of 100 |
| 1 | Panel 86 blank / 52 zero; P2 9.8587% | **Accept** | Not a reconciliation to IPS (universe) |
| 1 | Roll-forward 127/197 and 55 > 10%, "blank probably zero for most" | **Modify** | Numbers stand. The reading is unsupported because investment return is ignored |
| 1 | Blank-filed vs zero-filed as classes | **Modify** | Provenance distinction only: both forms are valid and absence is a preparer choice |
| 2 | regulations.gov 403; 0 of 13 readable | **Accept** | |
| 2 | SIFMA: no 2026 DAF letter; only letter 2024-02-08 | **Accept** | URL count 10,278 vs 10,276 (live file) |
| 2 | NYSBA: 1519–1535 no §4966; latest 1489 | **Accept** | |
| 2 | SIFMA and NYSBA 2024 quotes | **Accept, minor modify** | Competition quote is on pp. 18–19 [PDF 23–24] |
| 2 | Neither letter mentions Form 990 | **Accept** | |
| 2 | Unified Agenda entry; edition unverified | **Accept, resolve** | Edition is the 2026 Unified Agenda (pubId 202510) |
| 2 | Adler & Colvin 404 | **Accept** | |
| 2 | Replace the §1.5 "SS only" row | **Accept** | Exact text below |

## Exact corrections

### `research/mission-2026-11-14/b39n8-01-payout-definition-bridge.md`

**Find:** "So the two bounds, 9.33% and 10.20%, bracket IPS's 9.68% [F]."
**Replace with:** "So the two bounds, 9.33% and 10.20%, bracket IPS's 9.68% [F]. Read against the filed Schedule D, DAFRC’s FY2023 zeros are 86 filed blanks (81 with assets > 0) and 52 filed zeros. Dropping the 81 blanks, as IPS does, gives 9.86% (n = 1,400), 0.18 points above IPS (b39n8-01-01-blank-vs-zero.md). [V wave 45A]"

**Find:** "  - IPS, dropping only the blanks, gives 9.68%."
**Replace with:** "  - IPS, dropping only the blanks, gives 9.68%.\n  - The panel with IPS’s rule applied on filed evidence (drop the 81 sponsor-years whose line 3(a) is filed blank, keep the 51 filed zeros) gives 9.86% (n = 1,400). All 248 IPS blanks are filed blanks and all 100 IPS zeros are filed zeros. The 10.20% bound is the IPS-screened variant (n = 1,344); unscreened it is 10.19% (n = 1,349). [V wave 45A]"

### `research/mission-2026-11-14/b39n8-01-01-blank-vs-zero.md`

**Find:** "So blank is probably zero for most of these sponsors, but not for all [I]."
**Replace with:** "This screen cannot show that blank means zero. It ignores investment return, and most FY2023 periods had positive market returns [I], so a fund whose grants roughly offset its gains also shows an outflow ≤ 0. An outflow ≤ 0 is necessary for zero grants, not sufficient. The 35 exact zeros and 28 identical year-on-year asset values look more like stale entries than evidence of no grants [I]. [V wave 45A]"

**Find:** "IPS's other 51 explicit zeros were not read (proposal -02)."
**Replace with:** "IPS's other 51 explicit zeros were read in validation. All 51 are zero-filed, so 100 of 100 explicit IPS zeros carry a filed 0 (proposal -02 answered). [V wave 45A]"

**Find:** "The four raw checks (§7) match the extracts."
**Replace with:** "The four raw checks (§7) match the extracts. Validation re-read all 248 primary returns as raw XML and got the same classification on every one. [V wave 45A]\n- **What blank means in e-file XML.** The 990 e-file format allows both forms. 103 distinct returns read carry an explicit DonorAdvisedFundsGrantsAmt of 0, and MeF accepted 256 without the element, so it is optional. Every one of the 248 blank-filed returns contains other explicit zero-valued elements. An absent element records a preparer or software choice for that line, not a separate fact about grants. The XSD itself was not read. [V wave 45A]"

### `research/mission-2026-11-14/b39n1-01-docket-2026-submissions.md`

**Find:** "(p. 18 [PDF 23])"
**Replace with:** "(pp. 18–19 [PDF 23–24]) [V wave 45A]"

**Find:** "so **the edition is unverified**"
**Replace with:** "so the edition was unverified at drafting. Validation identified it: reginfo’s edition list for this RIN labels pubId 202510 “2026”, the 2026 Regulatory Plan and Unified Agenda (OIRA introduction PDF created 2026-07-01). The Spring 2025 edition (pubId 202504) gave Final Action 05/00/2026 [V wave 45A]"

**Find:** "subject to the edition caveat"
**Replace with:** "with the edition identified as the 2026 Unified Agenda [V wave 45A]"

**Find:** "P (edition unverified)"
**Replace with:** "P (2026 edition, pubId 202510) [V wave 45A]"

### `research/mission-2026-11-14/direction-policy-lobbying-obbba.md`

**Find:** "| Unified Agenda | A secondary source reports a July 2026 target for finalization (SS). We did not reach reginfo.gov's rule page; the Fall 2025 and Spring 2025 queries returned no DAF text | SS only |"
**Replace with:** "| Unified Agenda | RIN 1545-BI33, ‘Taxes on Taxable Distributions Under Section 4966’: Final Rule Stage; Priority ‘Substantive, Nonsignificant’; EO 14192 Designation ‘Not subject to, not significant’; Timetable ‘Final Action 07/00/2026’. The edition is the 2026 Regulatory Plan and Unified Agenda (reginfo pubId 202510, labelled ‘2026’; OIRA introduction dated 2026-07-01). The Spring 2025 edition gave Final Action 05/00/2026. The July 2026 target has passed with no final rule (A2). OIRA lists no EO 12866 meetings for the RIN | [reginfo.gov, 2026 edition](https://www.reginfo.gov/public/do/eAgendaViewRule?pubId=202510&RIN=1545-BI33); [Spring 2025](https://www.reginfo.gov/public/do/eAgendaViewRule?pubId=202504&RIN=1545-BI33) (P) [V wave 45A] |"

**Find:** "5. **Unified Agenda target** not verified on reginfo.gov."
**Replace with:** "5. **Unified Agenda target** verified on reginfo.gov in wave 45A: Final Action 07/00/2026 in the 2026 Unified Agenda (05/00/2026 in Spring 2025). The target has passed without a final rule. [V wave 45A]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

**Find:** "\n---\n\n## Source register"
**Replace with:** "\n\n### 11.65 Blank DAF-grant cells and the 2026 docket letters (validated, wave 45A)\n\n**Blank DAF-grant cells and the 2026 docket letters** (validated, wave 45A). Both studies reproduce byte for byte. All 248 blank ‘Grants from DAFs’ cells in IPS’s FY2023 list are also blank on the filed Schedule D. The validator read all 248 raw e-file XMLs, and filed lines 1(a) and 4(a) equal IPS’s cells on every one. IPS’s 9.68% median therefore does not move; on the newest returns it is 9.6754%, after one $550,000 amendment. All 100 explicit IPS zeros are filed zeros. In the repo panel, 86 of DAFRC’s 138 FY2023 zeros are filed blanks. Dropping the 81 of them with assets turns the 9.33–10.20% bracket into 9.86%, 0.18 points above IPS. E-file XML allows both an explicit 0 and an absent element, so a blank records a preparer’s choice, not evidence of no grants. The 7.72% figure, which counts every blank as zero, stays a bound [I]. None of the 13 docket letters of 2026 could be read, because regulations.gov returns 403. The 2026 Unified Agenda lists the §4966 final rule as not significant, with a July 2026 target that has passed. [V wave 45A]\n\n---\n\n## Source register"
