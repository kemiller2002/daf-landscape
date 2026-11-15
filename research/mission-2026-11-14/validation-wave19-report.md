# Validation wave 19: batch 34 claims (R5 DAF-to-DAF netting, recipient whitelist, Ayco merger, 2026-filed returns, NPT program fees, pass-through sponsors, DAF Direct, insurer channel, Jasper Ridge exit, escheat statutes, top-20 terms census, Fidelity CIAP custody terms, and the DAFRC adviser survey)

**Date:** 2026-11-15. **Validator:** independent-validation-agent-wave19.
**Register:** [`validation-register-wave19.csv`](../../data/mission-2026-11-14/validation-register-wave19.csv), rows V19-01 to V19-29.
**Method:** public sources only. I did not log in, submit forms, solve CAPTCHAs or contact anyone. I checked robots.txt before each scripted read and skipped what it excluded (details under Limits). I do not reproduce credentials. For each claim I formed a verdict from primary sources first and compared it with the batch-34 documents afterwards. The sources were:
- **Script re-run** in a scratch copy of the repo, so no repo file was overwritten.
  - `scripts/mission_market_netting.py --np-cache` pointed at a `netpayout990` cache built in wave 11 (7,559 files), **not** batch 34's cache.
  - Both outputs, `dafrc-market-totals-netted.csv` and `daf-to-daf-recipient-whitelist.csv`, are **byte-identical** to the repo.
  - The script's own check rebuilds the corrected totals and matches `dafrc-corrected-market-totals.csv` to the dollar in all eight FY × metric cells.
- **IRS TEOS 2026.** I wrote my own stdlib range reader for `2026_TEOS_XML_05B.zip` and pulled three members (Vanguard FY6/2025, Ayco FY6/2025, NPT FY2025 990-T), inflating them with `unzip` (Deflate64). I also grepped `index_2026.csv` for their batch labels.
- **IRS XML, re-parsed** with my own regex script from the GivingTuesday mirror:
  - NPT FY6/2021–25;
  - AOGF FYE 2026-03, CAF America FYE 2025-04, PPGF CY2024, BBGF CY2025, NFG CY2024;
  - BNY Mellon CGF CY2024;
  - Jasper Ridge CY2020, CY2021, CY2022 and its 2023 990-PF;
  - Thrivent CY2025, KCCF CY2024 and MDRT Foundation FYE 2025-08;
  - RCF and BofA CGF CY2024 (Schedule I);
  - Fidelity Charitable FYE 2025-06 (a text search for DAF Direct).
- **Documents:**
  - dafdirect.org: terms, About page and robots.txt;
  - the Ren-hosted Northwestern Mutual program circular (11-24);
  - the Alera release (windpress.info syndicated copy);
  - NPT's FY25 consolidated financials PDF;
  - RUUPA (Maine legislature copy), 12 Del. C. ch. 11 subch. II (delcode) and UCC §3-303 (LII);
  - Fidelity Charitable's CIAP Investment Policies and Guidelines (June 2026) and its CIAP overview flyer;
  - DAFRC's *Financial Planning in the Age of Donor Advised Funds* (2026) full-report PDF.

## Headline

Batch 34's numbers hold up. The R5 re-run is byte-identical on an independent cache, and every filed value I re-parsed matches to the dollar. **One batch-34 correction is wrong:** the pass-through report's §6 item 3 says wave 4's "Schwab received $750.6m" from Jasper Ridge is unsupported. The same CY2022 return's **Schedule I** reports Schwab at $51,933,609 cash plus $698,657,671 non-cash, which is **$750,591,280**. Batch 34B's $746,466,086 is the Schedule N line-item sum. Both are filed figures, and V4-08 stands. Two points need context rather than correction:
- **The PPGF (+$169m) and NFG (−$228m) gaps against DAFRC are already applied** as R1 in `dafrc-corrections-itemized.csv`. The corrected market totals, and so R5, already use the filed values. Do not adjust them again.
- **The '61% vs 6%' figure** is, as batch 34C says, 2018 U.S. Trust/TPI data cited by DAFRC. The repo's analyst landscape still attributes it to "DAFRC 2026", so the corrections below apply batch 34C's proposals.

## Verdicts

| ID | Claim | Verdict | Key finding |
|---|---|---|---|
| V19-01 | R5 central $5.52 / $6.40 / $4.05 / $8.03bn; bounds $3.32–6.95bn / $4.88–9.42bn | **Confirmed** | Byte-identical re-run on the wave-11 cache. N = 5,521,304,084 / 6,397,893,766 / 4,053,095,169 / 8,031,010,978. |
| V19-02 | Netted FY2024 grants $58.41bn, contributions $84.74bn | **Confirmed** | 58,411,055,855 and 84,742,625,676. |
| V19-03 | Payout 28.5 / 23.8 / 24.0 / 25.9% → 25.2 / 21.0 / 22.3 / 22.8% | **Confirmed** | On prior-year corrected assets (FY2023 $256.37bn): 25.92% → 22.78%. |
| V19-04 | FY2024 grant growth +21.2% → +15.0%; FY2023 −1.4% → +3.2% | **Confirmed** | 0.21179 → 0.150354. The CSV also fills FY2021 corrected growth (+34.8%), which the doc table shows as n/a. Harmless. |
| V19-05 | Whitelist: 1,411 EINs; W1 125; W2 72/15; W3 767; W4 90/342; $31.57bn; R5 cumulative $19.1 / $24.0 / $28.4bn | **Confirmed** | All counts and sums reproduce. |
| V19-06 | Ayco merged into GS DAPF effective 2025-07-01; $1,162,195,533 transfer outside Schedule D grants ($452.6m) | **Confirmed** | Final return; 0 DAFs; Schedule I purpose "MERGER" to EIN 31-1774905; Schedule O merger text read. |
| V19-07 | 19 returns labelled "05A" in the index sit in 05B; Vanguard FY6/2025 $27.01bn EOY | **Confirmed** (3 of 19 sampled) | Vanguard, Ayco and NPT 990-T are labelled 05A and found in 05B. Vanguard values exact. |
| V19-08 | NPT "PROGRAM FEES" $3.80–4.29m; moved from M&G to Program in FY2024; consolidated fees $656k / $994k | **Confirmed** | All five years exact; consolidated PDF figures exact. |
| V19-09 | Pass-through FY2024 filed $4.32bn vs DAFRC $4.38bn; PPGF +$169m, NFG −$228m | **Confirmed** | **Already applied as R1** in the repo's corrected totals. Context, not a new adjustment. |
| V19-10 | Latest year $3.87bn DAF; $4.81bn / $4.85bn with other funds | **Confirmed** | $3,869.3m; $4,805.0m; $4,850.7m. These mix fiscal years. |
| V19-11 | AOGF FYE 2026-03: 695 DAFs + 751,746 other accounts ($935.7m grants) | **Confirmed** | Schedule O micro-donation text read. |
| V19-12 | Benevity $54.7m = 2.35% of AOGF grants | **Confirmed** | $54,654,481; 2.35% is of org-level grants (3.93% of DAF-column grants). |
| V19-13 | CyberGrants $8.3m from CAF America | **Confirmed** | $8,287,044, "GRANT PROCESSING". |
| V19-14 | NFG sole member DCSO since 2024-06-07; $27.5m to DCSO; Bonterra Tech $2.49m | **Confirmed** | Schedule O text exact. |
| V19-15 | PayPal sole member of PPGF; code M $9,041,772; no fee disclosed | **Confirmed** | Schedule R also lists PayPal Inc codes C $2.21m, L $1.74m, O $0.69m and P $0.31m. "No fee" means no fee line or contractor entry. |
| V19-16 | BBGF CSRconnect note vs Schedule D $543.8m / $536.4m | **Confirmed** | Both read. |
| V19-17 | DAF Direct Trust: operator, 2015 terms, Massachusetts law, Fidelity/DAFgiving360/BNY listed, Fidelity robots header | **Confirmed** | Fidelity FYE 2025-06 990: 0 mentions. |
| V19-18 | BNY CGF board vote 2024-12-24 to stop the DAF program | **Confirmed** | Text is in Schedule N Part II **and** Schedule O (the doc names only O). |
| V19-19 | Northwestern Mutual and MDRT → RCF; MDRT Foundation has no DAF values | **Partially confirmed** | NWM circular names RCF; MDRT Foundation has no Schedule D DAF elements. MDRT → RCF rests on repo edges E065/E066, not re-read. |
| V19-20 | Alera Charitable on TIFIN Give (2025-11-12); GiveClear inferred | **Confirmed** | The release names no sponsor; [I] label is right. |
| V19-21 | Thrivent CY2025 9,198 / $93.6m / $700.4m; KCCF 665 / $80.7m / $125.8m | **Confirmed** | Exact. |
| V19-22 | Jasper Ridge: 13.15% support; $1.319bn Schedule N transfers; $1,231.1m in kind; 990-PF §507(b)(1)(A) | **Confirmed** | All exact; plan adopted 2022-12-08; dissolution effective 2023-12-31. |
| V19-23 | Batch 34B: V4-08's "Schwab $750.6m" is unsupported | **Contradicted** | Schedule I of the same return: Schwab $750,591,280. Schedule N line items: $746,466,086. |
| V19-24 | RUUPA §1005(c)(6)/(8); Del. §1175(b)(6), no void defence; UCC §3-303(b) | **Confirmed** | Statute text read first-hand. |
| V19-25 | Census covers 18 of 20; 6 of 20 explicit limits (~$84bn) | **Partially confirmed** | Counts match the CSV ($84.21bn). "18" includes DAFgiving360 (2024 text only) and AEF (no terms found). GKCCF and Greater Horizons pages returned 403 to me, so their quotes are unverified this wave. |
| V19-26 | Fidelity CIAP (June 2026): Other Custodian 70 vs 60 bps on first $500k | **Confirmed** | The fee table is "effective July 1, 2020"; the flyer's "$1M x 50 bps" is a typo. |
| V19-27 | DAFRC 35/21/10/4% and 83/69/69/63%; 669 advisers; six focus groups | **Confirmed** | Figures 3.4 and 5.1. The PDF has 46 pages, not 45. |
| V19-28 | "61% vs 6%" = 2018 U.S. Trust/TPI, cited by DAFRC | **Confirmed** | Endnotes 10–16 cite the 2018 study. |
| V19-29 | RCF $745.7m and BofA CGF $969.5m Schedule I "see attached" | **Confirmed** | One RecipientTable row each; RCF 17,290 recipients. |

## Exact corrections

### `research/mission-2026-11-14/queue-batch34-pass-through-channels.md`
1. **§6, item 3 (Jasper Ridge / V4-08).**
   - **Find:** "3. **`sponsor-mortality-analysis.md` and `validation-wave4-report.md` (V4-08 \"Schwab received $750.6m\").** The line-item sum of Schedule N in the CY2022 XML is **$746,466,086** to Schwab. Total transfers are $1,319,068,001. Adding the 2023 990-PF final grant ($2,956,978) gives $749.4m, which is still not $750.6m."
   - **Replace with:** "3. **`sponsor-mortality-analysis.md` and `validation-wave4-report.md` (V4-08 \"Schwab received $750.6m\"): no change.** V4-08's $750.6m is the CY2022 **Schedule I** amount to Schwab Charitable ($51,933,609 cash + $698,657,671 non-cash = $750,591,280). The **Schedule N** line items to Schwab sum to $746,466,086, within total Schedule N transfers of $1,319,068,001. Both are filed figures in the same return; cite which schedule is meant [V wave 19, V19-23]."
2. **§1.1, totals bullet (PPGF/NFG gap).**
   - **Find:** "  - PPGF is +$169.1m on the filed return; NFG is −$228.1m."
   - **Replace with:** "  - PPGF is +$169.1m on the filed return; NFG is −$228.1m. Both filed values already replace DAFRC's imputations under rule R1 (`dafrc-corrections-itemized.csv`), so the repo's corrected market totals, and R5, already include them. This is not a further adjustment [V wave 19]."
3. **§1.3 table, PPGF row.**
   - **Find:** "**No fee to PayPal disclosed.** PayPal donates personnel (\"PPGF HAS NO EMPLOYEES\"): Schedule R code M $9,041,772 (CY2024)"
   - **Replace with:** "**No fee to PayPal disclosed** (no Part VII-B or fee line). PayPal donates personnel (\"PPGF HAS NO EMPLOYEES\"): Schedule R code M $9,041,772 (CY2024). Schedule R also lists PayPal Inc transactions under codes C ($2,209,075), L ($1,742,154), O ($689,031) and P ($307,024) [V wave 19]"
4. **§2 table, BNY row.**
   - **Find:** "| Is the BNY listing current? | **No.** BNY Mellon Charitable Gift Fund's CY2024 990, Schedule O: "
   - **Replace with:** "| Is the BNY listing current? | **No.** BNY Mellon Charitable Gift Fund's CY2024 990, Schedule N Part II and Schedule O: "

### `research/mission-2026-11-14/queue-batch34-escheat-terms.md`
1. **§0, P-TRM-05 lead.**
   - **Find:** "**The census now covers 18 of the top 20; Dechomai and Raymond James are unreadable.**"
   - **Replace with:** "**The census now has at least one document read for 18 of the top 20; Dechomai and Raymond James are unreadable.** DAFgiving360 rests on its 2024 text (the 2026 Program Policies are unreadable), and AEF has no terms of use found [V wave 19]."
2. **§5.1, sources (page count).**
   - **Find:** "(PDF created 2026-04-23, modified 2026-05-07; 45 pp.)"
   - **Replace with:** "(PDF created 2026-04-23, modified 2026-05-07; 46 pp.)"

### `research/mission-2026-11-14/analyst-and-education-landscape.md`
1. **§4.1 table, "Who starts the philanthropy conversation" row.**
   - **Find:** "| **61%** of clients say they do; **6%** say the adviser does | DAFRC 2026 via [InvestmentNews, Oct 28 2026](https://www.investmentnews.com/practice-management/charitable-giving-season/268629) | Conflicts with sponsor framing of advisers \"driving\" growth (T8). |"
   - **Replace with:** "| **61%** of clients say they do; **6%** say the adviser does | 2018 U.S. Trust/TPI Study of the Philanthropic Conversation, as cited in DAFRC 2026 ([report](https://www.dafresearchcollaborative.org/s/DAF_FinancialAdvisorReport_Final_Web.pdf), endnotes 10–16); repeated by [InvestmentNews, Oct 28 2026](https://www.investmentnews.com/practice-management/charitable-giving-season/268629) | **Pre-2021 data, not a 2026 survey result**: historical context only. DAFRC's own 2026 \"61%\" figures are different (advisers serving $10m+ clients; advisers who personally use a DAF, against 26%) [batch 34C; V wave 19]. |"
2. **§4.1 table, DAFRC adoption row (access label).**
   - **Find:** "| Secondary: the executive summary page returned 403. A sponsor (DAFgiving360) hosts it. |"
   - **Replace with:** "| Primary: full report PDF read (created 2026-04-23; Figure 3.4). Convenience sample of 669 advisers, unweighted; funded by DAFgiving360 [batch 34C; V wave 19]. |"
3. **§4.1 table, reasons row.**
   - **Find:** "| tax benefits 83%; flexible timing 69%; convenience 69%; estate planning 63% | DAFRC 2026 via search summary of the [DAFgiving360 release](https://www.dafgiving360.org/press-release/dafrc-advisor-study) | Secondary. |"
   - **Replace with:** "| tax benefits 83%; flexible timing 69%; convenience 69%; estate planning 63% | DAFRC 2026, Figure 5.1 ([report](https://www.dafresearchcollaborative.org/s/DAF_FinancialAdvisorReport_Final_Web.pdf)) | Primary (very or extremely important) [V wave 19]. |"
4. **§5.2, T8 row.**
   - **Find:** "DAFRC 2026: 61% of clients initiate philanthropy talks and 6% say the adviser does ([InvestmentNews](https://www.investmentnews.com/practice-management/charitable-giving-season/268629))."
   - **Replace with:** "A 2018 U.S. Trust/TPI figure, cited in DAFRC 2026: 61% of clients say they initiate philanthropy talks and 6% say the adviser does. This is pre-2021 context, not 2026 evidence [V wave 19]."
5. **§6, item 1 funnel bullet.**
   - **Find:** "   - client-initiated conversations: 61% versus 6%;"
   - **Replace with:** "   - client-initiated conversations: 61% versus 6% (2018 U.S. Trust/TPI data, cited in DAFRC 2026; historical context only) [V wave 19];"

### `research/mission-2026-11-14/queue-batch33-market-structure.md`
Batch 34 supersedes wave-18 correction 10 for this sentence. Apply this item instead of that one. Item 1's find text also appears in the file's own quoted correction list; apply it to the §2.2 body occurrence only.
1. **§2.2, pass-through total.**
   - **Find:** "  Those five sponsors made about $4.4bn of FY2024 DAF grants (DAFRC)."
   - **Replace with:** "  Those five sponsors made about $4.4bn of FY2024 DAF grants as DAFRC publishes them, or **$4.32bn on filed returns** (PPGF $795.7m filed vs $626.6m imputed; NFG $199.8m filed vs $427.9m imputed; both already applied as R1 in the corrected totals). In the latest filed years they made $3.87bn in the DAF column, or $4.85bn with the AOGF and CAF America other-funds columns (batch 34B §1.1) [V wave 19]."
2. **§2.2, pass-through list, Bonterra line.**
   - **Find:** "  - Bonterra → NFG and CAF America (customer)"
   - **Replace with:** "  - Bonterra → NFG and CAF America (both vendor/customer links: Bonterra Tech $2.49m from NFG CY2024; CyberGrants $8.29m from CAF America FYE 2025-04). NFG has been controlled since 2024-06-07 by its sole member, Durable Capital for Sustainable Outcomes Inc. [batch 34B; V wave 19]"

### `research/mission-2026-11-14/full-universe-990-harvest-and-corrected-totals.md`
1. **Jasper Ridge bullet.**
   - **Find:** "mostly to Schwab ($750.6m) and Fidelity ($548.9m)"
   - **Replace with:** "mostly to Schwab ($750.6m per Schedule I; $746.5m in Schedule N line items) and Fidelity ($548.9m)"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`
1. **New subsection after §11.13:** "### 11.14 Batch 34 (validated, wave 19)", containing:

   > **Batch 34 (validated, wave 19).** Netting sponsor-to-sponsor DAF transfers (rule R5, central tier) removes $5.52bn, $6.40bn, $4.05bn and $8.03bn from both corrected DAF grants and corrected contributions in FY2021–24, which is 7–12% of grants. The lower and upper tiers give $3.32–6.95bn and $4.88–9.42bn a year. FY2024 netted grants are $58.41bn (corrected $66.44bn) and contributions $84.74bn ($92.77bn). Payout on prior-year corrected assets falls from 25.9% to 22.8%, and FY2024 grant growth from +21.2% to +15.0%: much of the FY2024 jump is transfers between sponsors, largely to NPT. A reviewed whitelist of 1,411 recipient EINs drives it. Universities and hospitals and low-DAF-share fiscal sponsors are excluded, and community foundations are weighted by their DAF share of assets. Ayco Charitable Foundation filed a final FY6/2025 return: it merged into GS DAPF on 2025-07-01 and moved $1.16bn to it outside its Schedule D grants. NPT's "PROGRAM FEES" have run flat at $3.7–4.3m since FY2021 while DAF assets rose 3.5×, and moved from M&G to Program in FY2024; the payee is undisclosed. On filed returns the five large pass-through sponsors made $4.32bn of FY2024 DAF grants ($3.87bn in the latest years, or $4.85bn with the "other funds" AOGF has just moved out of the DAF column: 751,746 accounts and $936m of grants). The PPGF and NFG filed values were already in the corrected totals. Benevity takes $54.7m a year from AOGF (2.35% of its grants) and CyberGrants $8.3m from CAF America. PayPal donates PPGF's staff, and NFG's sole member has been DCSO since 2024-06-07. DAF Direct is a Fidelity-run trust whose widget still lists BNY Mellon CGF, which voted on 2024-12-24 to wind down. Fraternal insurers run their own sponsors (Thrivent, Knights of Columbus). Northwestern Mutual uses RCF, and Alera white-labels TIFIN Give. Jasper Ridge's exit followed public support of 13.15% (CY2022) and $1.32bn of in-kind transfers, mostly to Schwab and Fidelity. RUUPA §1005(c)(6) and (c)(8), Delaware §1175(b)(6) (no void defence) and UCC §3-303(b) give voided gift checks statutory defences; no enforcement history was found. Six of the top 20 sponsors (about $84bn of assets) contractually limit automated or third-party access. Fidelity CIAP assets at an outside custodian pay 10 bps more on the first $500k. DAFRC's 2026 adviser report confirms 35/21/10/4% and 83/69/69/63%, but "61% of clients initiate vs 6%" is 2018 U.S. Trust/TPI data. Correction: Jasper Ridge's $750.6m to Schwab is the Schedule I figure, and Schedule N's line items total $746.5m [V wave 19]. Sources: [queue-batch34-netting-filings.md](mission-2026-11-14/queue-batch34-netting-filings.md), [queue-batch34-pass-through-channels.md](mission-2026-11-14/queue-batch34-pass-through-channels.md), [queue-batch34-escheat-terms.md](mission-2026-11-14/queue-batch34-escheat-terms.md), [validation-wave19-report.md](mission-2026-11-14/validation-wave19-report.md).

## Data-file notes (not .md; for the owning agent)

- **`dafrc-market-totals-netted.csv`, `daf-to-daf-recipient-whitelist.csv`:** reproduce byte-identically on an independent cache; no change. Optionally blank `yoy_growth_corrected` for FY2021 so it matches the doc's "n/a", or say in the doc that it compares with FY2020 corrected.
- **`relationship-graph-edges-additions-19.csv`:**
  - **ES016 (BNY → DAF Direct):** the source text is in Schedule N Part II as well as Schedule O.
  - **ES006 (PayPal → PPGF):** add "Sch R also lists codes C $2,209,075, L $1,742,154, O $689,031, P $307,024".
- **`pass-through-sponsors-2026.csv`:** add to the PPGF and NFG FY2024 rows "filed value already applied as R1 in dafrc-corrections-itemized.csv".
- **`sponsor-terms-census-top20-2026.csv`:** GKCCF and Greater Horizons terms pages returned 403 on 2026-11-15; keep their quotes as batch-34 reads, not re-confirmed.

## Limits

- **Robots and access.**
  - I did not fetch gspf.goldman.com (wave-18 rule).
  - dafresearchcollaborative.org groups ClaudeBot with `*`, whose rules disallow only `/config`, `/search`, `/account`, `/api` and `/static`, so `/s/` PDFs were read.
  - reninc.com names the `Anthropic-AI` agent with only an `Allow: /faqs/` line, which excludes nothing; `*` disallows only `/wp-admin/`.
  - growyourgiving.org and greaterhorizons.org allow all agents in robots.txt but returned HTTP 403 to my requests. I did not retry around the block.
- **Sampled, not exhaustive.** 3 of the 19 2026-filed returns; no re-read of the AOGF FYE 2021–25 Benevity series, CAF FYE 2024-04 ($5.41m), the Givinga Schedule I clusters, Bright Funds, or the CY2021 Jasper Ridge fee lines.
- **Not re-read:** the TPI 2026 release figures, the AdvisorHub and InvestmentNews custody-minimum articles, the California, New York, Massachusetts and Washington statute texts, the DAFgiving360 2026 policies (403), and the MDRT/RCF edges E065/E066.
- **Interpretation.** That R5's netted lines are DAF money (tier weights), the "fixed contract" reading of NPT's program fees, GiveClear as Alera's sponsor, and the support-test cause of Jasper Ridge's exit all remain inferences, as batch 34 labels them.
