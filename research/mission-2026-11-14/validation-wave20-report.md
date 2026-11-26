# Validation wave 20: batch 35 claims (AOGF reclassification and account-metric restatement, public-support cliff, 2026 TEOS fill, Fidelity/Vanguard FY2025 counterparts, delegated-access routes, DCSO / For Good, TIFIN Give, faith platforms, Vanguard pool weights, Daffy agent wrappers, analyst catalogues, Every.org and Chariot rails)

**Date:** 2026-11-15. **Validator:** independent-validation-agent-wave20.
**Register:** [`validation-register-wave20.csv`](../../data/mission-2026-11-14/validation-register-wave20.csv), rows V20-01 to V20-26.
**Method:** public sources only. I did not log in, submit forms, solve CAPTCHAs, make keyed API calls or contact anyone. I read robots.txt on each host before fetching a page and skipped what it excluded (details under Limits). I do not reproduce credentials. For each claim I formed a verdict from primary sources first and compared it with the batch-35 documents afterwards. The sources were:
- **IRS XML, re-parsed** with my own regex scripts (GivingTuesday mirror):
  - AOGF FYE 2026-03 and FYE 2025-03 (amended);
  - Givinga CY2024 (amended) and PPGF CY2024;
  - Community Foundation of South Lake County FY9/2025, Los Altos CF FY6/2025, National Charitable Fund CY2023 and CY2024;
  - DCSO / The Resiliency Company CY2024;
  - JCF NY FY6/2024 and FY6/2025;
  - Every.org 990-PF CY2020–2024;
  - Fidelity Charitable FYE 2025-06 (Schedule I, 89,891 lines).
- **IRS TEOS 2026:** Vanguard Charitable FYE 2025-06 (member 202621329349306657 of `2026_TEOS_XML_05B.zip`, from the wave-19 validator's own range read, not batch 35's cache); a HEAD of `index_2026.csv` and an EIN grep of it.
- **Repo files, recomputed:** `dafrc-corrected-market-totals.csv`, `dafrc-sponsor-schedule-d-fy2019-2024.csv`, `dafrc-corrections-itemized.csv`, and batch 35's four panel CSVs, `delegated-access-routes-2026.csv`, `relationship-graph-edges-additions-20.csv` and `daf-agent-wrappers-2026.csv`.
- **Documents:**
  - For Good 2024 Annual Report (PDF);
  - Vanguard Charitable User Agreement (May 2025), FY2025 audit (text layer) and FY2026 audit (Note 3 page OCR'd with tesseract), and the investments page (36 expense ratios, "Last updated 09/30/2026");
  - SVCF DAF agreement, Fidelity Program Guidelines (PDF 2026-09-11), and the GS DAF circular in the FireAid report appendix;
  - Pipedream (app and action `.md`), Zapier, Composio and npm registry entries for the Daffy wrappers; docs.daffy.org auth, MCP and gifts pages;
  - Datos Insights report pages (2021 and 2024);
  - PR Newswire (TIFIN Give / SEI) and Pulse 2.0 (TIFIN.AI);
  - Chariot `disbursements.md` and its help-centre tracking page;
  - sponsor homepages hjcf.org, ccfmemphis.com and knightscharitable.org.
- **Script:** I did **not** re-run `scripts/mission_batch35_screens.py`. A full run fetches 1,142 submissions. I re-derived its key numbers from filings and from the output CSVs instead (V20-01 to V20-11).

## Headline

Batch 35's filed numbers hold up to the dollar. Three results reproduce independently:
- **AOGF's column shift:** 710,352 DAF accounts become 695, and 751,746 accounts with $935.7m of grants move to "other funds".
- **The account-metric restatement:** −21.8% of accounts, −1.2% of grants. Givinga, AOGF and PPGF hold 76.2% of FY2024 accounts.
- **The Fidelity/Vanguard counterpart lines:** Fidelity sends $3,462,769,914 to 927 panel EINs and Vanguard $585,900,349 to 506. Fidelity → Vanguard is $480.1m against $87.3m back, a net $392.8m. My Schedule I parse matches on EINs alone.

The Vanguard pool-weighted cost (3.58 bps FY2026; 3.83 bps FY2025, with the stated bounds) reproduces from my own OCR of Note 3, which ties to the $33,880,084,002 total, and my own scrape of the expense ratios. Every delegated-access quote I re-read is verbatim: Vanguard, GS, SVCF and Fidelity.

**No claim is contradicted.** Three wording fixes are needed:
1. **Daffy wrappers.** §0 counts five wrappers as documenting a write action that "commits fund money". Only Pipedream, Zapier and Metorial document donation creation. Composio and Corsair expose only gift creation, and Daffy's Gifts reference does not say whether a gift debits the fund. The batch's own §1.2 already labels that point [I].
2. **DCSO's name.** DCSO files under its legal name, Durable Capital for Sustainable Outcomes Inc. "The Resiliency Company" is its *doing-business-as* name, not the filing name.
3. **Two clarifications:**
   - The Every.org sentence pairs a 2020→2024 share change with a 2023→2024 dollar change.
   - The "17 of 123" support count excludes a 509(a)(2) first-five-years filer, Crewe, which shows 0%.

## Verdicts

| ID | Claim | Verdict | Key finding |
|---|---|---|---|
| V20-01 | AOGF 710,352 → 695 DAFs; 751,746 other accounts, $935.7m | **Confirmed** | FYE 2026-03 Schedule D exact; Schedule O "only with respect to its donor-advised funds" and "without ongoing advisory privileges". |
| V20-02 | Accounts 3.31m → 2.59m (−21.8%); grants −$0.78bn (−1.2%) | **Confirmed** | 720,545 − 695 = 719,850. 40.23% × $1,950.2m = $784.6m. A scenario, not a filed value. |
| V20-03 | Givinga + AOGF + PPGF = 76.2% of accounts; 787,283 without them | **Confirmed** | 1,421,011 + 720,545 + 380,644 = 2,522,200. Donation Processor subtype: 22 sponsors, 2.85m accounts, $4.24bn of grants. |
| V20-04 | Reclassification screen: 8 pairs, AOGF the only column shift | **Partially confirmed** | The CSV classes and the AOGF row match the filings; the script was not re-run. |
| V20-05 | No TY2025 returns for PPGF, NFG, Givinga, CAF FYE 2026-04 or GS DAPF | **Confirmed** | index_2026 Last-Modified 2026-10-21; no rows for those EINs. |
| V20-06 | South Lake County 30.04%, private-foundation box ticked, 50 DAFs | **Confirmed** | `PrivateFoundation170Ind` X; PY 31.74%; no 33⅓% or 10% box. |
| V20-07 | Los Altos 26.0%; NCF 14.1% → 29.4% | **Confirmed** | Los Altos excess over the 2% cap $83,438,747. NCF CY2024 passed on facts and circumstances. |
| V20-08 | 553 returns, 123 sponsors, 17 below 33⅓% | **Confirmed** | An 18th EIN (Crewe, a 509(a)(2) first-five-years filer at 0%) is correctly not flagged. Say so. |
| V20-09 | 144 fill rows, all in 05B; $33.79bn / $5.13bn / $7.96bn | **Confirmed** | CSV sums exact; Vanguard's $27.01bn re-read. |
| V20-10 | Fidelity $3.46bn → 927; Vanguard $585.9m → 506 | **Confirmed** | Exact to the dollar on an independent parse; include/exclude splits reproduce. |
| V20-11 | Fidelity → Vanguard $480.1m; reverse $87.3m; net $392.8m; 8.3% | **Confirmed** | 480,068,133 − 87,288,229 = 392,779,904. Vanguard DAF contributions $5,751.4m vs $5,746.9m. |
| V20-12 | DCSO "files as The Resiliency Company"; $27.46m revenue; Schedule R C $26.96m | **Partially confirmed** | Values exact. Legal name is Durable Capital for Sustainable Outcomes Inc; Resiliency is the DBA. |
| V20-13 | Shared officers (Ross, Goldfine); board; contractors | **Confirmed** | Related-org pay $125,000 and $104,308. |
| V20-14 | For Good 2024: $219.7m, $193.1m, $27.47m committed, $2.9m paid, Bonterra | **Confirmed** | All quotes verbatim; the report dates the rebrand to 2023. |
| V20-15 | Vanguard aggregator clause; bot and credential-sharing ban | **Confirmed** | User Agreement, "Last Updated: May 2025". |
| V20-16 | GS "(or another third party)"; SVCF prior approval; Fidelity "an individual" plus firm associates | **Confirmed** | All verbatim. The GS text is a third-party copy, as labelled. |
| V20-17 | JCF NY IT $478,777 / $479,026; no vendor in VII-B | **Confirmed** | VII-B lists investment managers and rent only. |
| V20-18 | Faith platforms: 7 of 8 resolved | **Partially confirmed** | HJCF, CCF Memphis and KofC re-confirmed. Atlanta, DJCF, JUF and shalomdc returned 403 to me. |
| V20-19 | Vanguard 3.58 / 3.83 bps; bounds 3.50–4.81 / 3.70–5.72 | **Confirmed** | My OCR plus scrape gives 3.583 / 3.833; ex-PAF 3.256 / 3.533. |
| V20-20 | TIFIN Give: no sale process; TIFIN.AI omits Give; SEI deal 2026-01-29 | **Partially confirmed** | SEI and TIFIN.AI re-read. Confluence and Canterbury (GlobeNewswire, robots 403) not re-read. |
| V20-21 | Daffy wrappers and their write actions | **Confirmed** | Pipedream create-donation and proxy; Zapier Create Donation / Gift; Composio CREATE_GIFT; Corsair `gifts.create`; Metorial create/cancel. |
| V20-22 | "At least five document a write action that commits fund money" | **Partially confirmed** | Three create donations. Two are gift-only, and whether a gift debits the fund is undocumented. |
| V20-23 | Datos 2021 (33 pp, 18 interviews) and 2024 UHNW titles | **Confirmed** | Page text verbatim; the sitemap census was not re-run. |
| V20-24 | Every.org ForGood 73.9% → 1.1%; KBF + Founders Pledge 19.0% | **Confirmed** | 713,148 / 964,640 and 474,870 / 44,931,032. The $2.45m is the 2023 figure. |
| V20-25 | Chariot 94.57% electronic; 5-day window, 3 emails | **Confirmed** | Verbatim. |
| V20-26 | PPGF CY2024 $797.9m to 14,871 recipients | **Confirmed** | Part I and Schedule I. |

## Exact corrections

### `research/mission-2026-11-14/queue-batch35-agents-analysts-rails.md`
1. **§0, P-CON-06 row (money-moving wrappers).**
   - **Find:** "• At least five of them document a **write action that commits fund money** (Operator.io also re-exposes Composio's Create Gift):<br>"
   - **Replace with:** "• At least five of them document a **money-related write action** (Operator.io also re-exposes Composio's Create Gift). Three document **donation** creation (Pipedream, Zapier, Metorial). Composio and Corsair expose only **gift** creation, and Daffy's Gifts reference does not say whether a gift debits the fund balance [I; V wave 20]:<br>"
2. **§1.2, reading 4 (gift path).**
   - **Find:** "4. **The gift path is under-examined.**"
   - **Replace with:** "4. **The gift path is under-examined** (so W01 and W06 are not counted as documented fund debits; V wave 20)."
3. **§0, P-ASR-06 row (years).**
   - **Find:** "Its share of grants fell from 73.9% (2020) to 1.1% (2024), while the dollar amount fell from $2.45m to $0.47m as grants rose 2.7x [C]."
   - **Replace with:** "Its share of grants fell from 73.9% (2020) to 1.1% (2024). From 2023 to 2024 its dollar amount fell from $2.45m to $0.47m while total grants rose 2.7x ($16.78m → $44.93m) [C; V wave 20]."

### `research/mission-2026-11-14/queue-batch35-access-owners-faith.md`
1. **§0, P-B34B-03 row (DCSO name).**
   - **Find:** "DCSO (EIN 99-0468956, Delaware, formed 2024) files as **\"The Resiliency Company\"**, a climate-resilience \"parent organization\" with 10 employees."
   - **Replace with:** "DCSO (EIN 99-0468956, Delaware, formed 2024) files under its legal name, Durable Capital for Sustainable Outcomes Inc, **doing business as \"The Resiliency Company\"**. It is a climate-resilience \"parent organization\" with 10 employees [V wave 20]."
2. **§2 table, Identity row.**
   - **Find:** "| Identity | EIN 99-0468956, Washington DC; formed 2024, Delaware; dba **The Resiliency Company**; website resiliency.com |"
   - **Replace with:** "| Identity | Legal name Durable Capital for Sustainable Outcomes Inc; EIN 99-0468956, Washington DC; formed 2024, Delaware; dba **The Resiliency Company** (DoingBusinessAsName on the return); website resiliency.com [V wave 20] |"

### `research/mission-2026-11-14/queue-batch35-panel-screens.md`
1. **§0, P-B34B-02 row (support count).**
   - **Find:** "17 of the 123 screened sponsors fall below 33⅓% in at least one year."
   - **Replace with:** "17 of the 123 screened sponsors fall below 33⅓% on the 170 test in at least one year. Crewe Endowment Foundation, a 509(a)(2) filer in its first five years (0% in FY2021), is not counted [V wave 20]."

### `research/DAF-INDUSTRY-REPORT-2026-11.md`
1. **New subsection after §11.14:** "### 11.15 Batch 35 (validated, wave 20)", containing:

   > **Batch 35 (validated, wave 20).** AOGF (Benevity) has moved its micro-donation accounts out of the Schedule D DAF column. Its FYE 2026-03 return reports 695 DAFs, down from 710,352, and 751,746 "other" accounts carrying $935.7m of grants. Applied back to FY2024, that basis cuts corrected market accounts by 21.8% (3.31m → 2.59m) but grants by only 1.2%. Three micro-account processors (Givinga, AOGF and PPGF) hold 76.2% of corrected FY2024 accounts, so account counts and per-account averages should be reported with and without them. Among 123 few-account, large-balance sponsors, the Community Foundation of South Lake County reported 30.04% public support for FY9/2025 and ticked the Schedule A private-foundation box. Los Altos CF (26.0%) and Community Foundations Inc (25.6%) passed only on the prior-year test. Fidelity Charitable's FY2025 Schedule I sends $3.46bn to 927 DAFRC-panel sponsors and Vanguard's $586m to 506. Fidelity → Vanguard is $480.1m against $87.3m back, a net $392.8m. Vanguard's FY2025 DAF contributions ($5.75bn) were flat on FY2024. No top-20 sponsor names a software service as an appointable party. Vanguard alone permits an Authorized Person with their own Vanguard-issued login to use "aggregators", while still barring bots. GS DAF ("or another third party") and SVCF (prior approval) leave an entity route open. Network for Good, now For Good, became a subsidiary of DCSO (dba The Resiliency Company) in June 2024. The two share a CEO and general counsel, and DCSO took about $27.0m from NFG. For Good reports $193.1m of 2024 DAF grants. Vanguard's audited pool balances put asset-weighted in-fund cost at ≈3.6 bps (3.5–4.8). Daffy is the only DAF API with third-party agent wrappers: Pipedream, Zapier and Metorial expose donation creation, and Composio and Corsair expose gift creation. Daffy keys carry no documented scope. Every.org's ForGood (check) rail fell from 73.9% of grants (2020) to 1.1% (2024). Chariot reports 94.57% of grant payments sent electronically. No contradictions were found. The corrections are wording only: wrappers that only create gifts are not documented fund debits, and DCSO's legal name is Durable Capital for Sustainable Outcomes Inc [V wave 20]. Sources: [queue-batch35-panel-screens.md](mission-2026-11-14/queue-batch35-panel-screens.md), [queue-batch35-access-owners-faith.md](mission-2026-11-14/queue-batch35-access-owners-faith.md), [queue-batch35-agents-analysts-rails.md](mission-2026-11-14/queue-batch35-agents-analysts-rails.md), [validation-wave20-report.md](mission-2026-11-14/validation-wave20-report.md).

2. **Housekeeping (§11.14).** The batch-34 paragraph ends with its "Sources:" list twice. Delete the second copy, which starts at the second occurrence of " Sources: [queue-batch34-netting-filings.md]" and runs to the end of that paragraph.

## Data-file notes (not .md; for the owning agent)

- **`daf-agent-wrappers-2026.csv`:**
  - **W01 `moves_or_commits_money`:** change "gift: commits fund money…" to "gift [I]: Daffy docs do not say whether a gift debits the fund". This matches W05 and W06.
- **`relationship-graph-edges-additions-20.csv` (ET001–ET003):** the entity labels already use "Durable Capital for Sustainable Outcomes Inc (dba The Resiliency Company)". No change.
- **`public-support-cliff-screen.csv`:** no change. The `below_33_cy` flag already excludes Crewe (first-five-years).
- **`infund-expense-nationals-2026.csv` N061 / N070 (batch 35B proposal 2):** the proposal is supported. 3.58 bps (FY2026) and 3.83 bps (FY2025) reproduce. Coverage is 97.8% when the Total Return Solutions Fund is excluded from the denominator, and 97.7% when it is included.
- **`daf-to-daf-fy2025-counterparts.csv`, `form990-harvest-2026-fill.csv`, `daf-reclassification-screen.csv`:** no change.

## Limits

- **Robots and access.**
  - Every host's robots.txt was read first:
    - irs.gov and the GivingTuesday S3 mirror;
    - vanguardcharitable.org, svcf.org, fidelitycharitable.org, fireaidla.org (404, no file) and forgood.org;
    - pipedream.com, zapier.com (ClaudeBot group excludes only /app/, /editor/ and similar), composio.dev and registry.npmjs.org;
    - docs.daffy.org (404), datos-insights.com, prnewswire.com and pulse2.com;
    - help.givechariot.com, www.givechariot.com and the sponsor homepages.
  - **Chariot:** givechariot.com's robots.txt returned a redirect, and the page request followed it to www.givechariot.com. I read that host's robots.txt (`Disallow: /admin/*` only) right after the page request, so this read came before that host's robots.txt was checked. It permits the path.
  - **403 responses:** atlantajewishfoundation.org, djcf.org, juf.org and shalomdc.org returned 403 to my requests. Their robots files allow access, and I did not retry around the block.
  - globenewswire.com returns 403 on robots.txt, so I did not fetch it. The iphiview.com and fcsuite.com hosts were not used.
- **Not re-run:**
  - `mission_batch35_screens.py`, in full;
  - the Datos and Cerulli sitemap censuses;
  - the MCP Registry, Operator.io and n8n checks;
  - the Tyve, Momentum, Kambeo, ioby and GWWC post-mortems;
  - the EO BMF foundation codes;
  - CertSpotter for JCF / Give Interactive;
  - NPT's FY25 consolidated statements;
  - the BofA, NPT, JCF, GKCCF and CJP terms rows of the delegated-access CSV.
- **Reuse.** The Fidelity FY2025 XML, the AOGF FYE 2026 XML and the Vanguard TEOS member are the copies the wave-19 validator fetched independently. Batch 35's own caches (`netpayout990/`, `b35/`) were not used.
- **Interpretation.** These remain inferences, as batch 35 labels them:
  - the agent-feasibility readings (Vanguard read-only path; entity routes at GS and SVCF);
  - "separable, not for sale" for TIFIN Give;
  - DCSO's ~$27m being drawn from operating reserves;
  - the BMF lag for South Lake County.
