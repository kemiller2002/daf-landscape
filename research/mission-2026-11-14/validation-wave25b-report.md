# Validation wave 25B: new directions N12–N14 (nonprofit DAF revenue benchmarks, data standards and interoperability, non-cash gift infrastructure)

**Date:** 2026-11-15. **Validator:** independent-validation-agent-wave25b.
**Register:** [`validation-register-wave25b.csv`](../../data/mission-2026-11-14/validation-register-wave25b.csv), rows V25B-01 to V25B-31.
**Documents validated:**
- N12: [direction-nonprofit-daf-benchmarks.md](direction-nonprofit-daf-benchmarks.md) and `nonprofit-daf-revenue-benchmarks-2021-2026.csv` (102 rows)
- N13: [direction-data-standards-interoperability.md](direction-data-standards-interoperability.md) and `daf-data-standards-2026.csv` (32 rows)
- N14: [direction-noncash-gift-infrastructure.md](direction-noncash-gift-infrastructure.md), `noncash-gift-vendors-2026.csv` (17 rows) and `relationship-graph-edges-additions-23.csv` (20 rows)

**Method:** public sources only. I did not log in, submit forms, solve or bypass CAPTCHAs, make keyed API calls or contact anyone. I read robots.txt on each host before fetching any page on it, and did not fetch hosts whose robots.txt could not be read. **I did not use crt.sh.** SEC EDGAR was read with a generic User-Agent. For each claim I formed a verdict from the primary source first and compared it with the documents afterwards. The sources were:
- **N12:**
  - Chariot's 2026 report page and webinar page, and its 2025 summary (`.md` variants);
  - the M+R Benchmarks 2025 PDF (pdftotext, pp. 40–41 and 113);
  - NonProfit Times (2024-07-24, 2025-06-27), NonProfit PRO and TrueSense on M+R 2026;
  - the FreeWill 2026 DAF blog;
  - the Giving USA 2025 release (CY2024 totals);
  - the repo's `dafrc-market-totals-netted.csv`, for an independent recompute of every reconciliation ratio.
- **N13:**
  - dafdirect.org (home page and registration page);
  - Chariot docs v2026-04-01 (OAuth endpoints, checklist, overview, unintegrated-grant object, FDX);
  - the Endaoment async-grant OpenAPI page;
  - Fidelity Charitable's EFT page;
  - IRS: the release memo of 2024-12-16 and the TEOS schema page;
  - the JCF FY2025 and Schwab FY6/25 990 XMLs;
  - grants.gov data standards;
  - CFPB section 1033 sources: the CFPB PFDR page, Cozen (2026-04-09), Consumer Finance Monitor (2026-08-06), and a Federal Register API query of CFPB documents since 2025-08-01;
  - the 360Giving codelists.
- **N14:**
  - Ren's 2022-06-08 release, the DonateStock–GVNG release (PR Newswire) and engiven.com/nonprofits;
  - the ProPublica API for Dechomai Asset Trust and Dechomai Foundation;
  - nine 990 XMLs from the GivingTuesday mirror: Dechomai Foundation 2022–24 (Part VII contractors), Schwab FY6/22–FY6/25 and Fidelity FY6/22 (Schedule I);
  - AEF's Dechomai page;
  - the Charitable Solutions one-pager (text and pdfinfo);
  - Fidelity Charitable: the what-you-can-donate page, the 2026 Giving Report and the complex-assets fact sheet;
  - NPT's illiquid-asset guidelines (0824);
  - GivingIQ pricing;
  - EDGAR Form D XML for Engiven (two filings) and FreeWill, with the FreeWill filing index.

## Headline

The three documents are accurate on their numbers. 25 of 31 claims are confirmed, 3 partially confirmed and 3 unverifiable. None is contradicted.

**What holds independently:**
- **N12 benchmarks:**
  - Chariot 2026 is verbatim: $26.1bn of total giving at 54 nonprofits, $3.3bn of DAF revenue across 907,000 gifts, and "nearly 13% of total revenue" from under 1% of gifts. DAFs supply more than 22% of major-gift revenue while major gifts are 2% of DAF gifts. Median growth is +75% against +9%. International Relief is at 23.7%, the sector range is 4–24% and Health grew +99.4%. The median gift is $300.
  - The 2024 edition gives a median of 12% in 2023, with 12 of 20 participants at 10% or more, 6 of 20 at 20% or more, and $192m in total.
  - The 2025 edition gives 15% for participants under $10m, up 143%. Its median DAF revenue growth is +30% against −1%. The average DAF gift is $2,751 against $105 for non-DAF gifts, across 417,000 gifts and $1.15bn.
  - M+R 2025 gives $0.13 per online dollar, with Health at $0.01 and Environmental at $0.49; every sector bar matches. DAF revenue rose 6% and gift counts 11% in 2024, and 30% of participants offer DAF as a payment type.
  - M+R 2026, through two trade outlets, gives +44% revenue, +23% gifts and a $1,430 average gift.
- **N12 plausibility check.** Recomputed from the Giving USA 2025 published totals and the repo's netted file, every ratio reproduces:
  - $58.41bn / $592.50bn = 9.86% (range 9.62–10.04%);
  - / $392.45bn of individual giving = 14.88%;
  - / $438.29bn of individual plus bequest giving = 13.33%;
  - un-netted grants / total giving = 11.21%; DAFRC's published total / individual giving = 16.46%.

  Netted grants grew +37.4% over FY2021–24 and +15.0% in FY2024. GUSA's public-society benefit line ($66.84bn) is smaller than netted DAF contributions ($84.74bn).
- **N13 standards:**
  - DAF Direct lists three sponsors (Fidelity Charitable, DAFgiving360 and BNY Mellon Charitable), charges no fees, shows "© 2013" and publishes no API.
  - Chariot's guide says verbatim that it "does not require you to implement an exact API specification". The Chariot ID "must appear on the grant letter / remittance advice".
  - The Endaoment API is OpenAPI 4.87.0, and its required fields are exactly as stated.
  - Fidelity's ACH page says "Sent with grant notice" / "Emailed daily".
  - IRS: the memo gives TY2024v5.0 and the latest public TEOS 990X schema is 2024v5.0, while JCF (and Schwab FY6/25) filed 2024v5.5. JCF's 4,976 Schedule I rows carry one purpose string.
  - Grants Data Standards v3.0 is dated June 17, 2026, with HHS as the Standards Setting Agency.
  - Section 1033 status is as stated. The Federal Register shows no reconsideration NPRM published as of 2026-11-15; the latest item is the ANPR of 2025-08-22.
  - 360Giving's regrant codelist has FRG050 "Fiscal sponsor" and no DAF code.
- **N14 non-cash:**
  - Ren and The Giving Block launched on 2022-06-08 with a $100,000 minimum and 15% in traditional assets.
  - DonateStock's exclusive GVNG partnership is dated 2021-12-21, and Engiven's GVNG quote is live.
  - Dechomai Asset Trust took in $985.9m, $524.7m and $960.6m in CY2021–23.
  - Schedule I grants to Dechomai Asset Trust: DAFgiving360 $12.29m, $25.50m, $15.06m and $19.48m; Fidelity $56.73m non-cash.
  - AEF's Dechomai wording is verbatim.
  - Charitable Solutions was paid $2,998,459, $3,805,114 and $4,425,428, and the "1-3% WITH MINIMUM FEE OF $10,000" text is in the one-pager.
  - Fidelity: 65 days, about 500 complex contributions a year, $2.3bn and $2.6bn, 8%, and $18.1bn including $1.7bn of crypto.
  - NPT's seven minimums ($25k–$2m), on NPT BRO IACG 0824.
  - GivingIQ's 3.9% / 1.5% table.
  - Form D: Engiven $1.1m plus $1.2m = $2.3m; FreeWill $29,999,927 to six investors, filed 2022-03-04.

**What needs correcting or qualifying:**
1. **Chariot latency target (N13, V25B-12).** The guide says to "keep response times under ~3.5 seconds (ideally P95 under 2 seconds)", with a 99.5% availability floor. The doc says "P95 latency under about 3.5 seconds".
2. **Nacha robots (N13, V25B-16).** `achdevguide.nacha.org/robots.txt` returned 403 twice in this wave. Under the repo convention the host is unreadable, so it was not fetched. The 80-character CCD addenda and the CTX limit of 9,999 match the standard record layout, but cannot be re-observed from a primary page here.
3. **Fidelity FY6/22 grant to Dechomai (N14, V25B-25).** The $56.73m non-cash figure comes from an **amended** FY6/22 return, object 202430459349302913, filed in 2024. The same return shows $197,000 in cash to Dechomai Foundation.
4. **One-pager metadata (N14, V25B-27).** The PDF was created on 2014-11-18 and last modified on 2023-01-02. "A 2014 build" alone understates how recently it was touched. It is still undated, and the fee is not shown to be current.
5. **Candid robots (N12/N13).** candid.org/robots.txt now returns 200. It names ClaudeBot and anthropic-ai under `Disallow: /`, so the outcome is unchanged: candid.org was not fetched. The $2,995 → $3,934 snippet stays unverifiable (V25B-07, V25B-10).
6. **Snippet flag (N12, V25B-10).** The flag is justified. A 23× mean ratio at $3,934 implies a non-DAF mean near $171. The 2025 edition's "12 times" median ratio fits $300 / $25 exactly, so the $21 and $25 values look like non-DAF **medians**, not means.
7. **Engiven ~4% (N14, V25B-30).** The fee page on help.acst.com is allowed by robots but renders client-side, and no fee text is in its static HTML. Keep the figure as [S].

## Limits

- **Not fetched:**
  - candid.org and mrbenchmarks.com (their robots.txt names Claude agents in `Disallow: /` groups);
  - achdevguide.nacha.org (robots 403).
- **Ren's robots.txt** gives `Anthropic-AI` an `Allow: /faqs/` group with no Disallow lines. Under RFC 9309 that allows the whole site, so the 2022 release was read.
- **Federal Register.** The API returned an intermittent "IP blocked" body on one call. A retry a few seconds later succeeded, and nothing was bypassed.
- **Not re-checked in this wave:**
  - 360Giving's version (1.4) and adoption counts;
  - NPT's real-estate guideline values;
  - Fidelity's crypto page;
  - the Overflow and The Giving Block rows;
  - DonateStock Charitable's Schedule D values.

## Exact corrections

### `research/mission-2026-11-14/direction-nonprofit-daf-benchmarks.md`
1. **Rules applied, robots.**
   - **Find:** "**candid.org** robots returned 403, so it is unreadable and was not fetched."
   - **Replace with:** "**candid.org** robots returned 403 in this run. On 2026-11-15 it returns 200 and names ClaudeBot and anthropic-ai under `Disallow: /`, so it is still not fetched [V wave 25B]."
2. **§5 Limitations, snippet values.**
   - **Find:** "One snippet's non-DAF averages ($21→$25) conflict with the published 23× ratio, so those rows are flagged."
   - **Replace with:** "One snippet's non-DAF averages ($21→$25) conflict with the published 23× ratio, so those rows are flagged. A 23× ratio at $3,934 implies a non-DAF mean of about $171. The 2025 edition's median ratio of \"12 times\" fits $300 / $25 exactly, so the $21 and $25 values are probably non-DAF medians. They should not be used as averages [V wave 25B]."
3. **§0, plausibility row.**
   - **Find:** "This fits the vendor samples' ~10–13% (§4). | [D] |"
   - **Replace with:** "This fits the vendor samples' ~10–13% (§4). | [D]; recomputed from Giving USA 2025 totals ($592.50bn, $392.45bn, $45.84bn) [V wave 25B] |"

### `research/mission-2026-11-14/direction-data-standards-interoperability.md`
1. **Status line, robots.**
   - **Find:** "Hosts whose robots.txt could not be read (candid.org returned 403) were not fetched;"
   - **Replace with:** "Hosts whose robots.txt could not be read (candid.org returned 403; on 2026-11-15 it returns 200 with ClaudeBot and anthropic-ai disallowed) were not fetched [V wave 25B];"
2. **§2.2, service targets.**
   - **Find:** "- Service targets: 99.9% availability, P95 latency under about 3.5 seconds, at least 10 requests per second."
   - **Replace with:** "- Service targets: 99.9% availability (99.5% minimum), response times under about 3.5 seconds (ideally P95 under 2 seconds), and at least 10 requests per second [V wave 25B]."
3. **§2.4, Nacha source.**
   - **Find:** "([Nacha ACH Guide for Developers](https://achdevguide.nacha.org/ach-file-details)) [F]."
   - **Replace with:** "([Nacha ACH Guide for Developers](https://achdevguide.nacha.org/ach-file-details)) [F]. In wave 25B, `achdevguide.nacha.org/robots.txt` returned 403, so the page could not be re-read under the repo's robots convention. The values match the standard Nacha record layout but are unverified in that wave [V wave 25B]."
4. **§4, §1033 publication.**
   - **Find:** "Publication was not found."
   - **Replace with:** "Publication was not found. A Federal Register API query on 2026-11-15 (CFPB documents since 2025-08-01) shows the 2025-08-22 ANPR (2025-16139) as the latest Personal Financial Data Rights item, so no NPRM had been published [V wave 25B]."

### `research/mission-2026-11-14/direction-noncash-gift-infrastructure.md`
1. **§2.7, Fidelity grant.**
   - **Find:** "    - Fidelity: $56.73m non-cash (FY6/22);"
   - **Replace with:** "    - Fidelity: $56.73m non-cash (FY6/22). This comes from an amended FY6/22 return (object 202430459349302913, filed 2024), which also shows $197,000 in cash to Dechomai Foundation [V wave 25B];"
2. **§2.7, one-pager date.**
   - **Find:** "  - The document is undated; its file metadata shows a 2014 build. Treat the fee as the *last published* figure, not a current one."
   - **Replace with:** "  - The document is undated. Its file metadata shows it was created on 2014-11-18 and last modified on 2023-01-02. Treat the fee as the *last published* figure, not a current one [V wave 25B]."
3. **§2.2, Engiven fees.**
   - **Find:** "engiven.com/pricing returns 404."
   - **Replace with:** "engiven.com/pricing returns 404. The ACS help page (`help.acst.com/en/giving/realm-giving/guides/stock-and-cryptocurrency`) is allowed by robots but renders client-side, and its static HTML has no fee text, so the 4% stays unverified [V wave 25B]."

### `research/DAF-INDUSTRY-REPORT-2026-11.md`
1. **New subsection after the last §11 subsection.** Add "### 11.21 New directions N12–N14 (validated, wave 25B)", containing the paragraph below. If §11.21 is already taken (for example by wave 25A), use the next free number.

   > **New directions N12–N14 (validated, wave 25B).**
   > - **Nonprofit-side benchmarks.** The only nonprofit-file series is vendor-run.
   >   - Chariot/K2D 2026 finds DAFs at "nearly 13%" of $26.1bn in total giving across 54 large nonprofits ($3.3bn from 907,000 gifts, under 1% of gift count). DAFs supply more than 22% of major-gift revenue although only 2% of DAF gifts are major gifts. The median DAF gift is $300.
   >   - Earlier editions: a 12% median share in 2023 (20 organisations), and 15% for participants under $10m in 2024.
   >   - M+R 2025 reports $0.13 of DAF revenue per online dollar, ranging from $0.01 in Health to $0.49 in Environmental. M+R's DAF revenue rose 6% in 2024 and 44% in 2025, and its average DAF gift was $1,430.
   >   - Repo cross-check: FY2024 netted DAF grants of $58.41bn equal 9.9% of Giving USA's CY2024 total and 14.9% of individual giving. This is consistent with, and slightly below, the DAF-forward vendor panels.
   > - **Data standards.** No open, multi-sponsor DAF grant standard exists.
   >   - DAF Direct is closed and has 3 sponsors.
   >   - Chariot's DAFpay guide is the de facto spec. It is vendor-certified and carries Chariot's own correlation ID, which sponsors must print on the remittance.
   >   - Remittance travels outside the payment. At Fidelity, ACH grant details are emailed daily.
   >   - Public IRS schemas lag what is filed: TEOS lists 2024v5.0, while filed returns use 2024v5.5.
   >   - The closest US template is the federal Grants Data Standards v3.0 (2026-06-17).
   >   - The section 1033 rule is enjoined and its reconsideration NPRM unpublished. DAF accounts are probably out of its scope.
   > - **Non-cash gifts.**
   >   - Dechomai carries the largest visible complex-asset flows. It took in $525m–$986m a year in 2021–23, received $12–26m a year from DAFgiving360 and $56.7m from Fidelity (FY6/22, amended return), and is AEF's stated partner for illiquid gifts.
   >   - Fidelity took $2.6bn of non-publicly traded assets in 2025, with no extra fee and 65 days on average to liquidity.
   >   - NPT screens with minimums of $25k–$2m.
   >   - Nonprofit-side vendors charge 1.5–3.9% a gift (GivingIQ, published).

## Data-file notes (not .md; for the owning agent)

- **`nonprofit-daf-revenue-benchmarks-2021-2026.csv`:**
  - NPB101's `definition` repeats the reconciliation-ratio text. Replace it with "Growth in netted DAF grants, FY2021 central $42.51bn → FY2024 central $58.41bn".
  - NPB008 `notes`: add "probably non-DAF medians (12× at $300/$25 matches the 2025 edition's median ratio)".
- **`daf-data-standards-2026.csv`:**
  - DS17–19: if a latency target is recorded, use "responses under ~3.5 s (ideally P95 under 2 s); 99.5% availability minimum".
  - DS22: add "achdevguide.nacha.org robots 403 in wave 25B; not re-read".
- **`noncash-gift-vendors-2026.csv` NCG-08 and `relationship-graph-edges-additions-23.csv` EW020:**
  - Replace "file built 2014" / "file metadata 2014" with "created 2014-11-18, modified 2023-01-02".
- **`relationship-graph-edges-additions-23.csv` EW019:**
  - Add "amended FY6/22 return (filed 2024); also $197,000 cash to Dechomai Foundation".
