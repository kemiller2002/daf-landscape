# Validation wave 24A: new directions N1–N4 (policy and lobbying, patents and security, international vehicles, recipients/impact/matching)

**Date:** 2026-11-15. **Validator:** independent-validation-agent-wave24a.
**Register:** [`validation-register-wave24a.csv`](../../data/mission-2026-11-14/validation-register-wave24a.csv), rows V24A-01 to V24A-36.
**Documents validated:**
- N1 [`direction-policy-lobbying-obbba.md`](direction-policy-lobbying-obbba.md), with `daf-regs-2023-comments-summary.csv` and `daf-lobbying-lda-2021plus.csv`;
- N2 [`direction-patents-security.md`](direction-patents-security.md), with `giving-tech-patents-2021plus.csv` and `daf-security-incidents-2021plus.csv`;
- N3 [`direction-international-comparison.md`](direction-international-comparison.md), with `international-daf-vehicles-2026.csv`;
- N4 [`direction-recipients-impact-matching.md`](direction-recipients-impact-matching.md), with `daf-grant-recipient-sectors-top50.csv`, `daf-impact-pools-2026.csv` and `matching-gift-daf-policies-2026.csv`;
- the literature flags F1–F4 in [`direction-academic-literature.md`](direction-academic-literature.md), only where they touch N1–N4.

**Method:** public sources only. I did not log in, submit forms, solve CAPTCHAs or contact anyone. The only keyed API was api.regulations.gov with the public `DEMO_KEY` (2 calls). I read robots.txt on each host before fetching a page (details under Limits). **I did not use crt.sh.** I used a generic User-Agent. For each claim I formed a verdict from primary sources first and compared it with the documents afterwards.
- **Script re-run.** `scripts/mission_recipient_sectors.py` ran in a scratch copy of `scripts/` and `data/mission-2026-11-14/`, so repo outputs were not overwritten. It used an **empty lines cache**, so all 94 returns were re-read from the GivingTuesday mirror; none came from the author's local copies. The BMF files had Last-Modified 2026-11-09. All 94 line counts matched the cache. **`daf-grant-recipient-sectors-top50.csv` was rebuilt byte-identical (cmp).** I also summed the cached lines myself (Johns Hopkins; the whitelist exclusion) as a check on the script.
- **API re-pulls:**
  - regulations.gov: the docket's comments (one page of 250) and documents.
  - lda.gov: my own issue-text queries (387 unique filings) at 15 requests a minute or slower, plus client-name queries for AEF, Ren Acquisition and Renaissance Charitable.
  - SEC EDGAR: submissions JSON for all 19 issuers, with paged history for the large banks and brokers.
- **Documents read:**
  - 2025–26 and 2026–27 Priority Guidance Plans; P.L. 119-21 (§§70111, 70424–70426); IR-2026-135; Fidelity Charitable 2025 and 2026 Giving Reports; Philanthropy Daily (Giving USA 2026).
  - Google Patents pages (TIFIN, Gravvy ×2); SEC 2023-48 and 2022-168; Minnesota AG, FTC and California AG releases; Coinbase 8-K; Blackbaud FY2025 10-K; the California AG breach export (5,440 rows) and seven detail pages; Benevity status page.
  - Blumberg–Pasha 2026 T3010 report; NPT UK DAF report page; HMRC policy paper; PFC DQ note; Australian Treasury consultation paper; Leigh release of 2026-02-26; JBWere submission; CEPS Philanthropie Aktuell 01/25; giving.eu; the ACF portal article; Calgary Foundation DonorCentral.
  - ImpactAssets Schedule D (two XMLs) and website; GE and Disney matching guidelines.

## Headline

**All four documents hold up.** Of 36 claims, 33 are confirmed and 3 partially confirmed. None is contradicted outright, and none is unverifiable.

1. **N4 reproduces exactly from fresh data.** The re-run rebuilds the 3,984-row sector CSV byte-identical even though every return was re-fetched. The figures it reproduces:
   - $77.34bn net, after removing $12.70bn (14.1%) of DAF-to-DAF;
   - every sector share in the §1.3 table;
   - top-100 24.3% and HHI 21;
   - the national and community-foundation splits;
   - Schedule I = 98.0% of Part IX line 1.

   The only differences are the summary's `via` field and `distinct_eins`: 171,369 here against the doc's 171,370.
2. **N1's primary records check out.**
   - **Docket.** 249 submissions, split 173/63/13, and the commenter-type counts reproduce.
   - **Status.** The 2025–26 PGP item 35 and the 2026–27 PGP item 4 are verbatim. The docket holds no final rule.
   - **LDA amounts.** Vanguard Charitable $1.74m, NPT $1.09m and Fidelity Charitable $180k are exact.
   - **First registrations.** AEF and Ren Acquisition both first registered on **2024-02-01** (Tiger Hill Partners), which is inside the extended comment period.
   - **OBBBA.** The statute text and the IRS DAF exclusion are verbatim.
   - **Bunching.** The Fidelity bunching sentence and Giving USA's $1.71bn are verbatim.
3. **N2's enforcement facts are exact.**
   - **Blackbaud resolutions.** SEC $3m (2023-03-09); 49 states + DC, which is 50 AG offices, $49.5m (2023-10-05); FTC order (2024-05-20); California $6.75m (2024-06-13).
   - **Blackbaud 10-K.** Incident costs of $3.1m and $13.7m; two subrogation suits pending.
   - **Item 1.05.** Coinbase is the only Item 1.05 8-K across all 19 issuers.
   - **Patents.** TIFIN US12705394B2 and both Gravvy publications match Google Patents, including claim 1.
4. **N3's figures are exact.**
   - **Canada.** C$16,644,279,820 across 834 charities; disbursement quota 3.5% / 5% above C$1m.
   - **UK.** £3.1bn and 28.3%, with grants divided by prior year-end assets across ten charities.
   - **Australia.** The current 4% and 5% minimums; 3,707 funds; the 2026-02-26 decision for 6% with smoothing and two years' grace; A$10.7bn.
   - **Elsewhere.** Swiss CHF 1.2bn; Giving Europe's 19 countries and 12,749 donations; Foundant–ACF (2021-08-02); NPact–Calgary (DonorCentral host and NPact privacy link); Ren–NPT UK (npt.iphiview.com and nptukgiving.org links).

**Partial confirmations:**
1. **V24A-04, LDA 359 filings / 33 clients.** The count depends on method. My keyword-only re-pull contains 350 of the 359 CSV filings. The other 9 are AEF filings that surface only through the doc's per-client query. My own amendment rule gives 337 filings and 32 client names.
2. **V24A-20, parent-firm breach notices.** Every cited California notice and its dates are confirmed. The counts are secondary and were not re-verified. The California register also holds a **pre-2021 RenPSG notice** (breach 2018-06, reported 2018-10-18). "No breach notice … for any DAF recordkeeper (Ren …)" is therefore true only inside the 2021+ window.
3. **V24A-35, ImpactAssets.**
   - **Filed figures.** Exact: $2,896,880,396 and 2,197 DAFs. The DAFRC row is imputed at $3,628,163,475 (period 2023-12-31).
   - **The "open" framing is wrong.** The repo already applied **R1_filed_replaces_imputed** to this EIN in `dafrc-corrections-itemized.csv` (−$731,283,079). The corrected $323.27bn total already uses the filed value, so P-B39N4-02 duplicates an existing correction.

**Wording fixes** (not verdict-changing):
1. **Giving USA.** It also reports $310m of corporate giving retimed into late 2025, for "just over $2 billion" in all. N1 cites only the $1.71bn individual part.
2. **Fidelity's 13.4%.** The 2026 report uses 13.4% for both the DAF count and the number of grant recommendations. Cite the bunching sentence, not the number alone.
3. **UK relief.** The restriction applied from 15 March 2023 to charities not already recognised. For existing EU/EEA charities, HMRC's transition runs "until 1 April 2024" for Corporation Tax, IHT and other taxes, and "until tax year 2024/25" for Income Tax and CGT. N3's "ran to 2024/25" should use HMRC's wording.
4. **Australian sources.** The A$10.7bn comes from JBWere (S24), not the Treasury paper (S23). Treasury's 2,292 private funds (March 2025) and JBWere's 2,388 PAFs (June 2025) are different counts.
5. **Docket title.** Submission -0242 is titled "Alder and Colvin" in the docket. The firm is Adler & Colvin.

## Verdicts

| ID | Claim | Verdict | Key finding |
|---|---|---|---|
| V24A-01 | Docket IRS-2023-0053: 249 submissions, 173 / 63 / 13 | **Confirmed** | API totalElements 249; 2026 batch -0242 to -0254 |
| V24A-02 | Commenter types (CF 77, individuals 32+5, associations 29, nationals 24 …) | **Confirmed** | All counts reproduce; title-based classification spot-checked |
| V24A-03 | Still proposed; PGP 2025–26 item 35 and 2026–27 item 4 wording | **Confirmed** | Verbatim; 5 agency documents in docket, no final rule |
| V24A-04 | LDA: 359 filings, 33 clients | **Partially confirmed** | 350 of 359 in keyword re-pull; 9 AEF rows only via per-client query |
| V24A-05 | Vanguard Charitable $1.74m / 24 filings | **Confirmed** | $1,740,000 exact (23 quarterlies + 1 RR) |
| V24A-06 | NPT $1.09m / 25 filings | **Confirmed** | $1,090,000 exact |
| V24A-07 | Fidelity Charitable $180k; "regulation" from Q4 2023 | **Confirmed** | Exact; 2023 Q3 also has no DAF-text filing |
| V24A-08 | AEF and Ren first registered 2024 | **Confirmed** | Both RR dated 2024-02-01 (Tiger Hill) |
| V24A-09 | Non-itemizer $1,000/$2,000; DAF gifts excluded | **Confirmed** | §70424 text; IR-2026-135 verbatim |
| V24A-10 | 0.5% floor, 2/37 §68 cut, 1% corporate floor, 60% permanent | **Confirmed** | Statute verbatim |
| V24A-11 | Fidelity +13.4% "bunching"; Giving USA ~$1.71bn | **Confirmed** | Verbatim; GUSA adds $310m corporate (≈$2bn total) |
| V24A-12 | TIFIN US12705394B2 | **Confirmed** | Active, 2026-08-11, priority 2024-06-26; claim 1 as paraphrased |
| V24A-13 | Gravvy application(s) | **Confirmed** | A1 2023 abandoned; A1 2025 pending; shared-account claim 1 |
| V24A-14 | Blackbaud SEC $3m | **Confirmed** | 2023-03-09; >13,000 customers |
| V24A-15 | 49 AGs + DC, $49.5m | **Confirmed** | 50 AG offices incl. DC; IN/VT co-led; >400 TB; 7 years |
| V24A-16 | FTC order 2024-05-20 | **Confirmed** | "millions of consumers" |
| V24A-17 | California $6.75m 2024-06-13 | **Confirmed** | Release says "subject to court approval" and links a judgment PDF |
| V24A-18 | Coinbase 8-K is the only Item 1.05 | **Confirmed** | Items 1.05, 9.01; $180–400m; 19 issuers screened |
| V24A-19 | Blackbaud 10-K $3.1m / $13.7m; 2 subrogation suits | **Confirmed** | Verbatim |
| V24A-20 | Parent-firm notices; none names a sponsor | **Partially confirmed** | Notices and dates exact; counts secondary; pre-2021 RenPSG notice exists |
| V24A-21 | Benevity ~108,000 deactivated ~30 h | **Confirmed** | 2025-06-17 04:00 to 06-18 10:24 MDT |
| V24A-22 | Canada DQ 3.5% / 5% above C$1m | **Confirmed** | PFC (secondary); C-32, Royal Assent 2022-12-15 |
| V24A-23 | Canada C$16.64bn, 834 charities | **Confirmed** | Blumberg–Pasha verbatim |
| V24A-24 | UK £3.1bn, 28.3% | **Confirmed** | Ten charities; prior-year-end denominator |
| V24A-25 | Australia 4% / 5%; 3,707 funds | **Confirmed** | Treasury paper verbatim |
| V24A-26 | Australia 6% decision 2026-02-26 | **Confirmed** | Smoothing 3 yrs; 2-yr grace; after guideline amendment |
| V24A-27 | A$10.7bn PAF net assets (2023) | **Confirmed** | JBWere (S24), not S23 |
| V24A-28 | Swiss CHF 1.2bn | **Confirmed** | CEPS verbatim |
| V24A-29 | UK reliefs UK-only from April 2024 | **Confirmed** | From 15 Mar 2023 for new applicants; HMRC transition wording |
| V24A-30 | Giving Europe: 19 countries, 12,749 donations | **Confirmed** | Rebrand dated 2026-02-10 |
| V24A-31 | Ren–NPT UK, Foundant–ACF, NPact–Calgary | **Confirmed** | Live links and ACF article |
| V24A-32 | $77.34bn net; $12.70bn (14.1%) DAF-to-DAF; 98% itemised | **Confirmed** | Byte-identical rebuild from fresh fetch |
| V24A-33 | Sector shares; top-100 24.3%; national vs CF | **Confirmed** | All cells reproduce; SVCF drives CF DAF-to-DAF |
| V24A-34 | Fidelity $4.6B invested for impact | **Confirmed** | Base-year inconsistency (2020 vs 2015) is real |
| V24A-35 | ImpactAssets $2.90bn vs DAFRC $3.63bn (open gap) | **Partially confirmed** | Values exact; repo already applied R1 (−$731.3m) |
| V24A-36 | GE and Disney matching clauses | **Confirmed** | Verbatim; Disney last modified 2021-02-03 |

### Rulings on the literature flags (only where they touch N1–N4)

- **F1 (account-level payout from voluntary samples).** Consistent with N3. N3 says floors abroad are never per account, and it warns against reading across payout rates. N1 and N4 do not use account-level payout. No change to N1–N4.
- **F2 (donor-benefit orientation predicts lower payout).** None of N1–N4 relies on this. No ruling here.
- **F3 (community foundations may send the largest share of grants to other DAFs).** N4's re-run data qualifies the flag:
  - **Segment shares.** Among top-50 sponsors, community foundations send 14.2% of Schedule I to whitelisted DAF sponsors, against 13.7% for nationals.
  - **The SVCF effect.** Silicon Valley CF alone accounts for $2.07bn of the segment's $2.59bn. That is 25.8% of SVCF's own Schedule I. Without SVCF the community-foundation share is 5.1%.
  - **Reading.** The California AG's 18% CF figure is consistent with a sample in which SVCF, a California sponsor, weighs heavily. It is not evidence that community foundations in general out-send nationals.

  P-B39N8-02 should test the CF result with and without SVCF.
- **F4 (payout dispersion is mostly definitional).** Consistent with N3 §7.7, which says not to read the UK 28.3%, Canada 12% and US 22.8% figures across. No change.

### Rulings on the documents' proposals

- **N1 §5.**
  - **Item 1** (Fidelity PDF bunching sentence) is supported (V24A-11).
  - **Item 2** (docket 249 / 13 new) is supported (V24A-01). Write "Adler & Colvin (titled 'Alder and Colvin')".
  - **Item 3** (PGP dating) is supported (V24A-03).
- **N4 P-B39N4-02.** Narrow it. The ImpactAssets replacement is already in `dafrc-corrections-itemized.csv` (R1). Keep only a check for any remaining top-50 imputed rows.

## Exact corrections

### `research/mission-2026-11-14/direction-policy-lobbying-obbba.md`
1. **§0, Q2 row (governing addition).**
   - **Find:** "AEF and Ren (both **first registered in 2024**, after the NPRM)"
   - **Replace with:** "AEF and Ren (both **first registered in 2024**, after the NPRM: AEF and Ren Acquisition Co. registrations are both dated 2024-02-01 (Tiger Hill Partners), inside the extended comment period [V wave 24A])"
2. **§2.1, Result bullet.**
   - **Find:** "- **Result:** **359 filings, 33 clients**."
   - **Replace with:** "- **Result:** **359 filings, 33 clients**. A keyword-only re-pull in wave 24A contained 350 of the 359; the other 9 (all AEF) surface only through the per-client query, so the count depends on that step and on the amendment rule [V wave 24A]."
3. **§3.2 reading.**
   - **Find:** "- Giving USA's estimate of the acceleration (~$1.71bn) is small against $617bn of total giving."
   - **Replace with:** "- Giving USA's estimate of the acceleration (~$1.71bn of individual giving, plus $310m of corporate giving, 'just over $2 billion' retimed in all) is small against $617bn of total giving [V wave 24A]."
4. **§5, item 2.**
   - **Find:** "(AEF, RCF, Ren, SIFMA, ABA, NYSBA, Adler & Colvin, Kallina, 'CF', 'MCF') [batch 39 n1]."
   - **Replace with:** "(AEF, RCF, Ren, SIFMA, ABA, NYSBA, Adler & Colvin (docket title 'Alder and Colvin'), Kallina, 'CF', 'MCF') [batch 39 n1; V wave 24A]."

### `research/mission-2026-11-14/direction-patents-security.md`
1. **§0, DAF administrators row.**
   - **Find:** "**No breach notice found** for any DAF recordkeeper (Ren, NPact, Foundant, Foundation Source)"
   - **Replace with:** "**No 2021+ breach notice found** for any DAF recordkeeper (Ren, NPact, Foundant, Foundation Source). The California register does hold a pre-2021 notice from Renaissance Philanthropic Solutions Group (RenPSG), breach 2018-06-05/13, reported 2018-10-18, outside the recency window [V wave 24A]"
2. **§3.3, first bullet.**
   - **Find:** "Every 2021+ hit is at a **parent or affiliate**."
   - **Replace with:** "Every 2021+ hit is at a **parent or affiliate** (affected counts other than the primary notices are secondary and were not re-verified in wave 24A) [V wave 24A]."

### `research/mission-2026-11-14/direction-international-comparison.md`
1. **§3, Gift Aid flows.**
   - **Find:** "Income Tax and CGT relief ran to 2024/25, and higher-rate relief on gifts to non-UK charities ended."
   - **Replace with:** "The measure applied from 15 March 2023 to charities not already recognised. For existing EU/EEA charities HMRC's transition ran \"until 1 April 2024\" for Corporation Tax, IHT, SDLT and other taxes and \"until tax year 2024/25\" for Income Tax and CGT; Gift Aid and higher-rate relief on gifts to non-UK charities then ended [V wave 24A]."
2. **§5, Market size.**
   - **Find:** "- **Fund counts:** 3,707 giving funds at 2025-03-03 (2,292 private, 1,415 public) [F: S23]."
   - **Replace with:** "- **Fund counts:** 3,707 giving funds at 2025-03-03 (2,292 private, 1,415 public) [F: S23]. JBWere's 2,388 PAFs (June 2025, S24) is a different date and source [V wave 24A]."
3. **§1 market table, Australia row.**
   - **Find:** "| Australia | A$10.7bn (2023) in private ancillary funds alone | n/a | n/a | 3,707 giving funds at 2025-03-03 [F: S23; S: S24] |"
   - **Replace with:** "| Australia | A$10.7bn (2023) in private ancillary funds alone [S: S24] | n/a | n/a | 3,707 giving funds at 2025-03-03 [F: S23] |"

### `research/mission-2026-11-14/direction-recipients-impact-matching.md`
1. **§2, ImpactAssets (governing replacement).**
   - **Find:** "- **DAFRC mismatch:** DAFRC's FY2024 row for this EIN is *imputed* at $3.628bn (period 2023-12-31), $0.73bn above the filing. This is P-B39N4-02."
   - **Replace with:** "- **DAFRC mismatch:** DAFRC's published FY2024 row for this EIN is *imputed* at $3.628bn (period 2023-12-31), $0.73bn above the filing. The repo has already replaced it: `dafrc-corrections-itemized.csv` applies R1_filed_replaces_imputed to this EIN (−$731,283,079, object 202543169349307999), so the corrected $323.27bn already uses $2.897bn. P-B39N4-02 is narrowed to any remaining top-50 imputed rows [V wave 24A]."
2. **§1.3 Notes, after the year-split bullet.**
   - **Find:** "- **Year split (all ex university/hospital):** DAF-to-DAF rose from 11.3% (FY2023) to 16.4% (FY2024) of Schedule I. Sector shares moved by 1 pt or less [C]."
   - **Replace with:** "- **Year split (all ex university/hospital):** DAF-to-DAF rose from 11.3% (FY2023) to 16.4% (FY2024) of Schedule I. Sector shares moved by 1 pt or less [C].\n- **SVCF drives the community-foundation DAF-to-DAF share.** SVCF sent $2.07bn (25.8% of its Schedule I) to whitelisted sponsors, out of the segment's $2.59bn; without SVCF the share is 5.1%. This bears on literature flag F3 (CA AG: CFs 18%) [V wave 24A]."

### `research/DAF-INDUSTRY-REPORT-2026-11.md`
1. **New subsection after §11.18:** "### 11.19 New directions N1–N4 (validated, wave 24A)". Renumber if another wave-24 subsection lands first. It contains:

   > **New directions N1–N4 (validated, wave 24A).** The 2023 proposed DAF regulations are still proposed: docket IRS-2023-0053 holds 249 public submissions (173 in the comment period, 63 hearing requests and outlines, and 13 new ones in May–June 2026 from AEF, RCF, Ren, SIFMA, the ABA and NYSBA tax sections and others), no final rule, and a 2026–27 Priority Guidance Plan item for "guidance under §§4966 and 6033 regarding certain donor advised fund arrangements". Federal lobbying filings that name DAFs come from 33 clients (359 filings, 2021–2026 Q3; whole-filing amounts): Vanguard Charitable $1.74m, NPT $1.09m and Fidelity Charitable $180k; AEF and Ren Acquisition first registered on 2024-02-01. From 2026 the new $1,000/$2,000 non-itemizer deduction excludes gifts to DAFs, and the 0.5% floor and 35% value cap reward bunching; Fidelity Charitable attributes part of its 13.4% account growth in 2025 to bunching, and Giving USA puts accelerated individual giving at about $1.71bn. No DAF incumbent holds a 2021+ giving patent found by a citation crawl (TIFIN's US12705394B2 is a generic LLM-privacy patent), and no Item 1.05 cyber 8-K came from a DAF-linked issuer except Coinbase; the reference enforcement case remains Blackbaud's 2020 breach (SEC $3m, 49 states and DC $49.5m, an FTC order, California $6.75m). Abroad, Canada (3.5%/5% disbursement quota; C$16.6bn in DAFs at 834 charities) and Australia (4%/5% today; 6% decided on 2026-02-26) set sponsor-level payout floors, while the UK (£3.1bn; 28.3% payout) has none; US vendors appear abroad only at adviser and community-foundation sponsors (Ren at NPT UK, Foundant at ACF, NPact at Calgary). Among the top 50 sponsors, $77.34bn of FY2023–24 Schedule I grants (after $12.70bn of DAF-to-DAF transfers) went 25.8% to education, 14.3% to human services, 14.1% to public-society benefit and 13.6% to religion, with the top 100 recipients taking 24.3%. National sponsors skew to education and religion, community foundations to human services and health, and Silicon Valley CF supplies most community-foundation DAF-to-DAF flows. Impact-labelled DAF capital is published only by Fidelity ($4.6B, self-reported) and ImpactAssets ($2.90bn filed) [V wave 24A].

## Data-file notes (not .md; for the owning agent)

- **`queue-proposals-batch39-n4.csv`, P-B39N4-02:** narrow it to "check for remaining top-50 FY2024 rows still imputed". Note that ImpactAssets is already replaced by R1 in `dafrc-corrections-itemized.csv` (V24A-35).
- **`daf-security-incidents-2021plus.csv`:** add to the notes of SI-08, SI-10, SI-14 and SI-06 that the counts were not re-verified in wave 24A. A one-line note is optional: a RenPSG 2018 California notice exists, pre-2021, and is excluded by the recency rule.
- **`international-daf-vehicles-2026.csv`:** no change. Row I24 already cites S24 for the A$10.7bn; only the .md table mixes the two sources.
- **`daf-regs-2023-comments-summary.csv`:** optional. Add to the -0242 note that it is titled "Alder and Colvin" (Adler & Colvin).
- **`daf-grant-recipient-sectors-top50.csv`, `daf-lobbying-lda-2021plus.csv`, `giving-tech-patents-2021plus.csv`, `daf-impact-pools-2026.csv`, `matching-gift-daf-policies-2026.csv`:** no change. The sector CSV was rebuilt byte-identical. The rest were checked where cited.

## Limits

- **robots.txt read first** on every host fetched:
  - api.regulations.gov returns an API-key error in place of a robots file; the API terms allow `DEMO_KEY`, and I used 2 calls.
  - lda.gov allows `/api/v1/` at 15 requests a minute.
  - www.irs.gov: `/pub/` and `/newsroom/` are allowed. www.govinfo.gov: `/content/` is allowed.
  - www.fidelitycharitable.org: `/content/dam/fc-public/docs/insights/` is allowed. philanthropydaily.com: crawl-delay 180; I made one fetch.
  - patents.google.com: only `/patent/` is allowed, and only that was fetched.
  - www.sec.gov and data.sec.gov: Archives and the APIs are allowed, used with a generic UA.
  - www.ftc.gov; ag.state.mn.us (`/Office/Communications/` allowed); oag.ca.gov (press releases, the breach list export and `/ecrime/` detail pages allowed); status.benevity.org.
  - carleton.ca, www.nptuk.org, giving.eu, communityfoundation.org.au, calgaryfoundation.org and pfc.ca: all allow.
  - ministers.treasury.gov.au (Drupal defaults); www.gov.uk; ceps.unibas.ch (sitemaps only); www.jbwere.com.au (open); impactassets.org; www.ge.com.
  - storage.googleapis.com and files.doublethedonation.com: no robots file.
- **Not fetched:**
  - crt.sh, per instruction.
  - www.regulations.gov and downloads.regulations.gov, so no comment letters were opened.
  - canada.ca, ato.gov.au and acnc.gov.au.
  - The Maine and Massachusetts breach registers, so the secondary counts were not re-verified.
  - The California Blackbaud judgment PDF; USPTO Patent Center, so statuses remain Google's labels.
- **Not re-run or not re-read:**
  - the patent citation crawl (146 rows) and the claim-theme tags;
  - the matching-gift rows other than GE and Disney;
  - the CAF, Prism, Charities Trust, CHIMP, Canada Gives, APS and Israeli provider details;
  - the Morgan Stanley ISI PDF, the TBF and SFF pages and the GA Social Impact commentary;
  - the DAFRC-whitelist construction itself (batch 34, validated earlier);
  - LDA filings for the associations, beyond the sums my pull reproduced: CFAI $3.33m, CoF $1.2m, Philanthropy Roundtable $1.38m + $1.79m.
- **Interpretation.** These remain [I], as the documents label them: the targeted-project reading of the 2026–27 PGP item, lobbying motives, the FTO reading, the Australian guideline timing and the CF vs national skew.

This is research, not legal or tax advice.
