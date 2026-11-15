# Validation wave 23: batch 38 claims (FE NXT Payment Assistant payers, FFTC portal and ledger, NPact's terms, the Give "$40B+" gap, iPhi archive dates, the NPT export tutorial, the full-text line-6 screen, MS GIFT line 3, recipient-side R5, the BDC parser, per-FTE pay, the payout triad, faculty employers, DAFpay anonymity, SCF and PSID, shared-platform prices, Google Play) and the crt.sh compliance note

**Date:** 2026-11-15. **Validator:** independent-validation-agent-wave23.
**Register:** [`validation-register-wave23.csv`](../../data/mission-2026-11-14/validation-register-wave23.csv), rows V23-01 to V23-28.
**Method:** public sources only. I did not log in, submit forms, solve CAPTCHAs, make keyed API calls or contact anyone. I read robots.txt on each host before fetching a page (details under Limits). **I did not fetch crt.sh, not even its robots.txt.** I do not reproduce credentials. For each claim I formed a verdict from primary sources first and compared it with the batch-38 documents afterwards. The sources were:
- **Scripts, re-run** in a scratch copy of `scripts/` and `data/mission-2026-11-14/`, so that repo outputs were not overwritten:
  - `scripts/mission_batch38_data.py triad`. It rebuilt `payout-triad-2021-2024.csv` **byte-identical** (cmp). The R5 central rebuild equals the published netting to the dollar.
  - `scripts/mission_batch38_data.py recipients`, with the SOI extracts. It reproduced every figure in batch 38B §4.
  - `scripts/mission_bdc_loans.py` at HEAD **and** at its pre-batch-38 version (commit 7c35776, identical to 50deed4), both on the same cached 501 filings, read-only (no `--fetch`). HEAD rebuilt `bdc-loans-daf-ecosystem.csv`, `bdc-loans-latest-marks.csv` and `bdc-unfunded-commitments-two-period.csv` **byte-identical**. The old version rebuilt the pre-batch-38 committed CSVs (line endings aside). Old and new outputs were then compared row by row.
  - The `fulltext` task (126,736 returns) was not re-run. Instead, I rebuilt its universe independently from the SOI extracts and checked the CSV and one return.
- **Independent arithmetic** from `dafrc-corrected-market-totals.csv`, `give-claim-reconciliation-batch30.csv`, `breadth-entity-profiles.csv`, `form990-contractors-harvest-full.csv`, `sponsor-cost-structure.csv`, `sponsor-pay-per-fte.csv` and `line6-fulltext-screen.csv`.
- **IRS XML, re-parsed** with my own regexes (GivingTuesday mirror):
  - MS GIFT FY2021–24 990s and the FY2024 990-T;
  - FFTC TY2024; Givinga CY2024 (amended); Dakota Medical Charities FY2025; NPT FYE 2025-06; GiveClear TY2024.
  - The Vanguard Charitable FYE 2025-06 object still returns NoSuchKey on the mirror; `index_2026.csv` lists it.
- **Documents and pages:**
  - NPT tutorial PDF (`pdfinfo`, `pdftotext`) and the NPT GivingPoint main bundle;
  - GWCF Nonprofit FAQ; fftc.org navigation; fcjc.fftc.org sign-in page; FFTC 2024 audit; Give Interactive company page;
  - archive.org availability API (three queries);
  - SCF 2025 codebook; PSID 2025 questionnaire (557 pp.); Funraise DAFpay help; American College DAFCP page and DAF Forum speakers; Givinga Solutions; Google Play details page for Fidelity Charitable;
  - public DNS (dns.google) for five Give Interactive hostnames plus two random labels as a wildcard control.

## Headline

Batch 38's filed numbers reproduce, and its quotes are verbatim wherever I could reach the page. Five results hold independently:
- **The NPT export tutorial.** The PDF was created 2026-03-23 (InDesign, 4 pp., code "NPT TUT HTAFA 0326"). It says, verbatim: "You can also export the data in any table to an Excel file by clicking the Export link beneath the table." The live NPT bundle carries the same export text and has no export toggle.
- **MS GIFT's line 3.** Line 3 is 2.5, 15.6, 39.2 and 4.8 bps of average public securities. Investment-management fees (line 11f) are blank in every year, and column (C) of line 3, −$15,678, equals the 990-T partnership line.
- **The payout triad and the recipient-side R5 check.** Both re-run exactly. FY2024 payout is 25.9% aggregate, 22.8% ex-DAF-to-DAF and 12.7% for the median sponsor. Recipient-side weights give $4.80bn against $4.39bn central.
- **The line-6 universe.** It rebuilds from the SOI extracts: 299,397 EINs, then 129,379 with line 6 "N" and $1m or more of assets. Dakota Medical Charities' return answers line 6 "0" while hosting "more than 100 donor-advised funds".
- **Close-out checks.** The SCF 2025 codebook, PSID 2025, Funraise's anonymity exclusion, the College's 7-of-22 faculty employers and the five Fidelity Android launch crashes all check out against the live sources.

**The Wayback inconsistency is resolved: both statements in batch 38A are true.** The availability API is served from `archive.org` (robots permits it). It returns the cited timestamps (20180831230800 and 20251220065252, both status 200). The snapshot host `web.archive.org` resets TLS connections from this environment, so the captured pages themselves cannot be read. Batch 38A's text should name the two hosts.

**Two contradictions concern the BDC parser (P-BLB-04).** The parser change is otherwise backward-compatible:
1. **Maturities before the change.** Before it, 16 of the 80 KKR FS Income Trust / Select debt rows already carried maturities (2/24/28, 7/1/31), so "0 before" is wrong; 64 rows gained one.
2. **A new parse defect.** The two Barings Private Credit Corp Envestnet rows gain not only "11/31" but also wrong values. The raw cells are "993 | 996 | 979". The parser writes fair value 0, 0% of par and a `yes_lt_97` below-par flag, and the 2026-09-30 row is now in `bdc-loans-latest-marks.csv`.

**Compliance findings:**
- **The crt.sh note's own table is wrong.** Every "crt.sh mentions" cell reads 0; the real counts are 4–19 per document. The table also omits two documents.
- **Live crt.sh calls remain configured.** Six scripts still call crt.sh, and `watchlist.csv` still holds 11 `ct_crtsh` checks, so a scheduled watchlist run would breach the note's decision 1.
- **FFTC's donor portal.** `daf.fftc.org/robots.txt` is a single malformed line, `User-agent: * Allow: /index.html Disallow: /`. Its evident intent disallows `/m/login`, which batch 38A fetched. I did not re-read that page. The FFTC portal claim stands on the fftc.org link, the FCJC tenant page and the GiftingNetwork release.

**Wording fixes:**
1. **Blackbaud payee lines.** The harvest has 23 Blackbaud payee lines, not 24.
2. **Contribution-share gap.** It runs 0.02–0.13 (NCF's is 0.017), not 0.04–0.13.
3. **NPT per-FTE pay.** "More than 235" FTE makes $136,066 an upper bound, not a point value.
4. **Core-platform price band.** It omits Stifel Charitable → Ren, $498,305 "OPS SYSTEM & SERVICE" (TY2024). With Stifel, the range is $118k–$498k and the median $218k.
5. **TIFIN share of GiveClear.** No Part IX line outside 11f is as large as TIFIN's $185,921, so "74% of GiveClear's non-investment operating cost" is an upper-bound ratio, not a demonstrated share.

**Give "$40B+" gap.**
- **Arithmetic.** It reproduces exactly: $41,800,385,204 and $40,110,738,053.
- **Vanguard input.** The $27.01bn Vanguard value is still a repo figure that has not been re-read.
- **Client evidence.** Five of the known clients' Give relationships rest on hostnames first found in CT logs: CCT, JCF, Minneapolis, Thrivent and Stifel. The hostnames resolve in public DNS today, and there is no wildcard, so their existence stands under the compliance note's rule 3. Their stage (sandbox, staging or production) and dates rest on CT alone.
- **Lower bound.** Excluding all five gives $32.59bn.

**Not verifiable from here:**
- **FFTC's FE NXT posting.** The Y-Axis copy returns 404, and no search copy was found.
- **NPact's Standard Terms.** npact.com fails at the protocol level for robots.txt and for the page.
- **The fftc.spectrumportal.net shell.** Not re-read.
- **PPGF's policy text.** Still [S].

These are recorded as unverifiable, not contradicted.

## Verdicts

| ID | Claim | Verdict | Key finding |
|---|---|---|---|
| V23-01 | NPT tutorial: "export the data in any table to an Excel file"; PDF 2026-03-23 | **Confirmed** | CreationDate 2026-03-23 19:40 UTC; 4 pp.; 8 Export labels |
| V23-02 | GivingPoint NPT bundle export text; no export toggle | **Confirmed** | Only `displayfundActivityStatements` is in `displaySettings`; J.P. Morgan bundles not re-fetched |
| V23-03 | Give known clients $41.80bn / $40.11bn | **Partially confirmed** | Arithmetic exact; Vanguard $27.01bn not re-read; five clients CT-discovered (DNS-corroborated); $32.59bn without them |
| V23-04 | Give company page timeline | **Confirmed** | 2023 entry reads "$2B processed & endowment pro…" |
| V23-05 | FFTC fundholders on GiftingNetwork (daf.fftc.org, fcjc) | **Partially confirmed** | Links and FCJC page verbatim; daf.fftc.org robots signals Disallow, so not re-read; compliance flag |
| V23-06 | FFTC 2026 posting lists FE NXT | **Unverifiable** | Y-Axis 404; no search copy |
| V23-07 | FFTC IT $5.33m → $2.85m | **Confirmed** | 5,325,416 / 2,853,618 |
| V23-08 | FFTC TY2024 VII-B top five | **Confirmed** | Exact |
| V23-09 | NPact Terms exclude Blackbaud | **Unverifiable** | npact.com unreachable (protocol error); robots unreadable, so not fetched |
| V23-10 | GWCF only public REPAY payer; harvest lines | **Partially confirmed** | FAQ verbatim; GWCF only CF Blackbaud payee; 23 lines, not 24 |
| V23-11 | Wayback captures 2018-08-31 / 2025-12-20; web.archive.org unreachable | **Confirmed** | archive.org API vs web.archive.org host; not an inconsistency |
| V23-12 | Givinga and PPGF account basis | **Partially confirmed** | Givinga 990 and site verbatim (site also says "Not locked into a third-party DAF"); PPGF [S] |
| V23-13 | Line-6 screen: 126,684 "No"; 3 likely sponsors; $2.96m | **Confirmed** | Universe 129,379 rebuilt; A-row sum 2,963,077; Dakota line 6 = 0; read not re-run |
| V23-14 | MS GIFT line 3 2.5/15.6/39.2/4.8 bps | **Confirmed** | All filed values exact; 990-T −15,678 |
| V23-15 | R5 recipient-side $4.80bn vs $4.39bn | **Partially confirmed** | Re-run exact; gap range 0.02–0.13, not 0.04–0.13 |
| V23-16 | Payout triad 25.9 / 22.8 / 12.7% | **Confirmed** | Byte-identical; independent aggregate 25.92 / 22.78% |
| V23-17 | P-BLB-04 additive; 66 rows; 80 of 80 (0 before) | **Partially confirmed** | Reproducible and otherwise compatible; 16 of 80 had maturities before; Envestnet FV parsed as 0 (raw 979) |
| V23-18 | Momentive 96.1%; Bonterra 99.43% | **Confirmed** | Facility par 12,628 / 11,015; 44,540 / 37,036 |
| V23-19 | NPT $136,066 per FTE | **Partially confirmed** | Arithmetic exact; an upper bound ("more than 235", undated [S]) |
| V23-20 | SCF 2025 codebook has no DAF item | **Confirmed** | Only X6830 code-10 exclusion text |
| V23-21 | PSID 2025 has no DAF item | **Confirmed** | 0 hits in 557 pp. |
| V23-22 | Funraise disables anonymous for DAFpay | **Confirmed** | "Anonymous Donors" in the not-available list |
| V23-23 | College: 7 of 22 employers; Forum 1 of 7 at a sponsor | **Confirmed** | 22 names; 7 speakers as listed |
| V23-24 | Core-platform payments $118k–$416k, median $204k | **Partially confirmed** | 17 values exact; omits Stifel → Ren $498,305 |
| V23-25 | TIFIN 74% of GiveClear opex | **Partially confirmed** | 185,921 / 250,440 = 74.2%; payment's Part IX location not shown |
| V23-26 | Fidelity Android crash reviews | **Confirmed** | 12 IDs match; crash texts verbatim |
| V23-27 | crt.sh compliance note | **Partially confirmed** | Robots content not re-fetched (instruction); counts printed 0; two docs and live watchlist checks omitted |
| V23-28 | Industry-report crt.sh dependency | **Partially confirmed** | See crt.sh dependency audit |

### Rulings on the batches' §9 proposals

- **Batch 38A §9.**
  - Items 1–4 are supported with the qualifications above. On item 1, keep FFTC's ledger at **medium**, not medium-high: the 2026 postings cannot be re-observed (V23-06).
  - Item 5 is supported only as batch 38A's reading. The NPact terms were not reachable (V23-09).
  - Item 6 is superseded by the compliance note and the dependency audit below.
- **Batch 38B.** No §9 proposals. The BDC data note below is required.
- **Batch 38C §5.2.** The recommended v2 change ("add the observed $118k–$416k band") should use $118k–$498k (V23-24).

## crt.sh dependency audit

**Scope.**
- **What was checked.** `research/DAF-INDUSTRY-REPORT-2026-11.md` contains no literal "crt.sh". I traced each of its vendor-stack and batch-summary claims back to its source document and classed it by its evidence route.
- **Robots content.** I did not fetch crt.sh. archive.org lists a capture of `crt.sh/robots.txt` (2026-04-01), but its content cannot be read from here. The `Disallow: /` content therefore rests on the records of the compliance note and batch 38A.
- **Corroboration test.** For corroboration I used public DNS (dns.google DoH), an admissible route under the note. Five Give hostnames resolve today. Random labels under `giveinteractive.com` return NXDOMAIN, so there is no wildcard.

**Claims that rest only on crt.sh (or CT logs) — unverified lead under the note:**

| # | Report location | Claim | Why CT-only | Status under the note |
|---|---|---|---|---|
| C1 | §11.12 (Batch 32, wave 17) | "Philanthropi's site is dark, while its infrastructure certificates still renew." | The renewal evidence is the crt.sh history in batch 32 §3.1. "Site is dark" stands on HTTP reads; "certificates still renew" does not | **Unverified lead** (the renewal half) |
| C2 | Vendor stacks, Give Interactive bullet 4 | "before Give's CCT production host (Jun 2025)" | The date is the first `cct.giveinteractive.com` certificate (2025-06-11). DNS shows the host exists today but cannot date it or show it is production | **Date and stage: unverified lead.** Host existence stands on DNS |
| C3 | §11.10 (Batch 30, wave 15) | "Give's known clients hold $36.7bn of FY2024 DAF assets" | $9.81bn of it (CCT $4.65bn, JCF $2.87bn, Minneapolis $0.60bn, Thrivent $0.59bn, Stifel $0.49bn) is attributed to Give only through CT-discovered hostnames. All five sponsors' live donor portals are iPhi or GiftingNetwork | **Membership stands on DNS** (the hosts resolve). Stage and timing are CT-only. Use "implementation hosts" wording |
| C4 | Vendor stacks, Give Interactive bullet 2 | "About $5.9bn of Ren-paying assets are at risk" | The Thrivent ($0.59bn), Stifel ($0.49bn) and Minneapolis ($0.60bn) parts rest on CT-discovered staging hosts (DNS-corroborated). ImpactAssets rests on an announcement; WaterStone on a live cutover | As for C3. The CT-only part is the "staging" stage, not the hosts' existence |

**Corroborated, so they stand on another source:**
- Ren iPhi attrition (6 of 57) and the iPhi redirects: DNS and HTTP status.
- FFTC → GiftingNetwork 2026-07-01: vendor release and portal pages.
- Vanguard Charitable–Give: the 2025-11-04 release.
- WaterStone migration: its own login page.
- Give "no live CF portals" and the East Bay loss: portal pages and akoyaGO.
- Omaha → Foundant: sponsor page.

**Batch 38 itself:**
- **§2 go-live window.** The lower bound "Give Interactive hosts lapsed in 2024-02" is a CT last-issued date, so it is an unverified lead.
- **§6, the `ocf` reading.** "Live after the 2025-04-20 certificate" uses a crt.sh date. The 2025-12-20 archive.org capture dates the tenant independently, so the conclusion stands.
- **The four crt.sh queries batch 38A sent** were discarded and are not used.

**Repo surfaces the note does not yet cover** (for P-CMP-CRT-01):
- **Documents:** `research/iphi-175-client-lead-and-dns-execution-2026-11-11.md` (1 mention) and `data/watchlist-snapshots/reports/2026-11-14.md` (10 mentions).
- **Snapshots:** `data/watchlist-snapshots/2026-11-14/ct-*.json`.
- **Scripts that still call crt.sh:**
  - `mission_watchlist.py` (`ct_crtsh`)
  - `collect_daf_dns.py`
  - `mission_cf_vendor_map.py`
  - `mission_ren_iphi_attrition.py`
  - `mission_cf_migrations_goodstack.py`
  - `mission_give_tenant_lapses.py` (export URL)
- **Live checks:** `watchlist.csv` holds 11 `ct_crtsh` rows.

## Exact corrections

### `research/mission-2026-11-14/queue-batch38-vendors-ledgers-portals.md`
1. **§0, P-REN-04 row.**
   - **Find:** "`web.archive.org` itself was unreachable from this session (connection reset), so the captured pages were not read → P-B38A-01"
   - **Replace with:** "The availability API is served from `archive.org`, which is reachable. The snapshot host `web.archive.org` resets connections from this session, so the captured pages were not read → P-B38A-01 [V wave 23: both hosts re-tested; timestamps 20180831230800 and 20251220065252 reproduced]"
2. **§0, P-B30C-03 row.**
   - **Find:** "Known clients then sum to **$41.80bn**, or **$40.11bn** without the three staging-only clients."
   - **Replace with:** "Known clients then sum to **$41.80bn**, or **$40.11bn** without the three staging-only clients. The Give relationships of CCT, JCF, Minneapolis, Thrivent and Stifel ($9.81bn at FY2024) rest on hostnames first found in CT logs. They resolve in public DNS (no wildcard), but their stage is CT-only. Without all five the total is $32.59bn [V wave 23]."
3. **§0, P-B29A-03 row.**
   - **Find:** "Both sign-in pages read \"Powered by GiftingNetwork\" and \"If this is your first time logging into the new portal, you'll need to re-register\" [F/H]."
   - **Replace with:** "Both sign-in pages read \"Powered by GiftingNetwork\" and \"If this is your first time logging into the new portal, you'll need to re-register\" [F/H]. Compliance note: `daf.fftc.org/robots.txt` is the single line `User-agent: * Allow: /index.html Disallow: /`, whose intent disallows `/m/login`. The FFTC portal finding rests on the fftc.org link, the FCJC tenant page and the GiftingNetwork release, not on a read of `daf.fftc.org/m/login` [V wave 23]."
4. **§1 table, harvest row.**
   - **Find:** "24 Blackbaud lines"
   - **Replace with:** "23 Blackbaud lines [V wave 23]"
5. **§2, go-live window.**
   - **Find:** "- **Lower bound:** Give Interactive hosts lapsed in 2024-02 (repo)."
   - **Replace with:** "- **Lower bound:** Give Interactive hosts lapsed in 2024-02 (repo). This date is a CT last-issued date (crt.sh), so it is an unverified lead under the [crt.sh compliance note](compliance-note-crtsh-robots.md) [V wave 23]."
6. **§2, ledger confidence.**
   - **Find:** "Confidence moves from medium to **medium-high**, on 2026 FFTC postings [F/S] plus the vendor story."
   - **Replace with:** "Confidence stays **medium**: the 2026 FFTC postings could not be re-observed in wave 23 (the Y-Axis copy returns 404; no search copy found). The vendor story [V] remains the main support [V wave 23]."
7. **§10, Limitations.**
   - **Find:** "- `web.archive.org` was unreachable, so only availability-API metadata (capture timestamp and status) is used."
   - **Replace with:** "- `web.archive.org` was unreachable, so only availability-API metadata from `archive.org` (capture timestamp and status) is used. NPact's Standard Terms (§3) could not be re-read in wave 23 (npact.com protocol errors) and stand on batch 38A's read [V wave 23]."

### `research/mission-2026-11-14/queue-batch38-data-followups.md`
1. **§0, P-BLB-04 row (b).**
   - **Find:** "**All 80 KKR FS Income Trust / Select debt rows now carry a maturity**, where none did before."
   - **Replace with:** "**All 80 KKR FS Income Trust / Select debt rows now carry a maturity**, against 16 before (64 gained one) [V wave 23]."
2. **§0, P-BLB-04 row, Envestnet sentence.**
   - **Find:** "Barings' Envestnet rows gain their 11/31 maturity."
   - **Replace with:** "Barings' Envestnet rows gain their 11/31 maturity, but they also gain mis-parsed values: the raw cells read par 993, cost 996, fair value 979 (98.6%), yet the rows show fair value 0, 0% of par and `yes_lt_97`. The 2026-09-30 row enters latest marks. Treat it as a parse error until fixed [V wave 23]."
3. **§6, results.**
   - **Find:** "66 rows changed: 64 KKR FS Income Trust / Select rows gain maturities, and 2 Barings Envestnet rows gain \"11/31\"."
   - **Replace with:** "66 rows changed: 64 KKR FS Income Trust / Select rows gain maturities, and 2 Barings Envestnet rows gain \"11/31\" plus mis-parsed values (fair value 0 against a raw 979) [V wave 23]."
4. **§6, results.**
   - **Find:** "**KKR FS Income Trust / Select debt rows with a maturity: 80 of 80** (0 before)."
   - **Replace with:** "**KKR FS Income Trust / Select debt rows with a maturity: 80 of 80** (16 before) [V wave 23]."
5. **§0, P-B34A-03 row.**
   - **Find:** "CJP by 0.04–0.13"
   - **Replace with:** "CJP by 0.02–0.13 (NCF 0.017) [V wave 23]"
6. **§0, P-LND-04 row.**
   - **Find:** "That implies **$136,066 wages per FTE against $103,147 per head** (FTE/head 0.76)."
   - **Replace with:** "That implies **at most $136,066 wages per FTE against $103,147 per head** (FTE/head ≥ 0.76; \"more than 235\" is an undated secondary figure) [V wave 23]."

### `research/mission-2026-11-14/queue-batch38-closeout-checks.md`
1. **§0, P-AIV2-04 row.**
   - **Find:** "Observed per-sponsor **core-platform** payments run $118k–$416k a year (median $204k, 17 sponsors, TY2024 990s). TIFIN Give takes 74% of GiveClear's non-investment operating cost."
   - **Replace with:** "Observed per-sponsor **core-platform** payments run $118k–$498k a year (median $218k, 18 sponsors, TY2024 990s, including Stifel Charitable → Ren $498,305 'OPS SYSTEM & SERVICE'). TIFIN Give's $185,921 equals 74% of GiveClear's non-investment operating cost, but the 990 does not show which Part IX lines carry it [V wave 23]."
2. **§5.1 table, summary row.**
   - **Find:** "| **17 core-platform relationships** | **median $203,595; IQR $179k–$291k; range $118k–$416k** | |"
   - **Replace with:** "| **17 core-platform relationships** | **median $203,595; IQR $179k–$291k; range $118k–$416k** (adding Stifel Charitable → Ren $498,305, omitted here: 18 relationships, median $217,955, range $118k–$498k [V wave 23]) | |"
3. **§5.1, vendor capture.**
   - **Find:** "Its payment to TIFIN Give LLC was $185,921, which is **74% of that cost**."
   - **Replace with:** "Its payment to TIFIN Give LLC was $185,921, which is **74% of that cost**. No Part IX line outside investment management (11f, $1.56m) is that large, so the payment is spread across lines or partly inside 11f; the ratio is an upper bound on the vendor's share of that budget [V wave 23]."

### `research/mission-2026-11-14/compliance-note-crtsh-robots.md`
1. **Affected-documents table (governing replacement of the count column).** Replace the 0 in each row with the case-insensitive counts of "crt.sh":
   - queue-batch30-cf-coverage-give.md 8;
   - queue-batch32-feeds-owners-codebases.md 15;
   - queue-batch38-vendors-ledgers-portals.md 7;
   - queue-bdc-coverage-migrations-goodstack.md 5;
   - queue-cf-vendor-map.md 6;
   - queue-community-foundation-rails-portals.md 8;
   - queue-donor-export-cf-payments-donorsphere.md 7;
   - queue-fidelity-chariot-goodstack-vanguard.md 4;
   - queue-give-interactive-displacement.md 18;
   - queue-ledgers-behind-portals.md 10;
   - queue-npt-givingpoint-fidelity-stack.md 9;
   - queue-ren-iphi-attrition.md 6;
   - queue-vendor-channel-moves.md 19;
   - queue-watchlist-and-vendor-moves.md 14.

   These are the counts as of 2026-11-15, before any compliance footer is appended [V wave 23].
2. **After "Validation reports that mention crt.sh are not listed; they inherit this note."**
   - **Find:** "Validation reports that mention crt.sh are not listed; they inherit this note."
   - **Replace with:** "Validation reports that mention crt.sh are not listed; they inherit this note. Also affected, outside this folder [V wave 23]:\n- `research/iphi-175-client-lead-and-dns-execution-2026-11-11.md` (1 mention).\n- `data/watchlist-snapshots/reports/2026-11-14.md` (10) and the CT snapshots `data/watchlist-snapshots/2026-11-14/ct-*.json`.\n- Scripts that still call crt.sh: `mission_watchlist.py` (`ct_crtsh`), `collect_daf_dns.py`, `mission_cf_vendor_map.py`, `mission_ren_iphi_attrition.py`, `mission_cf_migrations_goodstack.py` and `mission_give_tenant_lapses.py`.\n- `data/mission-2026-11-14/watchlist.csv` still holds 11 `ct_crtsh` checks. Disable them before the next watchlist run, or decision 1 is breached.\n\nCT-derived Give Interactive hostnames that resolve in public DNS (no wildcard; checked 2026-11-15 for cct, jcf-staging, thriventcharitable-staging, stifelcharitable-staging and minneapolisfoundation-staging) stand on DNS for their existence. Their certificate dates and environment stage remain unverified leads. The `robots.txt` content itself was not re-fetched in wave 23."

### `research/DAF-INDUSTRY-REPORT-2026-11.md`
1. **§11.12 (Batch 32, wave 17), Philanthropi sentence.**
   - **Find:** "Philanthropi's site is dark, while its infrastructure certificates still renew."
   - **Replace with:** "Philanthropi's site is dark. That its infrastructure certificates still renew rests only on crt.sh data and is an unverified lead under the [crt.sh compliance note](mission-2026-11-14/compliance-note-crtsh-robots.md) [V wave 23]."
2. **Vendor stacks, Give Interactive bullet.**
   - **Find:** "before Give's CCT production host (Jun 2025)."
   - **Replace with:** "before Give's CCT host, which resolves in public DNS. Its June 2025 first certificate and \"production\" label come from CT logs only (unverified lead, [V wave 23])."
3. **New subsection after §11.17:** "### 11.18 Batch 38 (validated, wave 23)", containing:

   > **Batch 38 (validated, wave 23).** NPT documents donor export: its "How to Access Fund Activity" tutorial (PDF created 2026-03-23) says donors can "export the data in any table to an Excel file", and the live GivingPoint code carries the same export text with no per-program switch. FFTC's fundholders moved to a GiftingNetwork portal ("new portal … re-register"). Its ledger is probably Financial Edge NXT on vendor evidence, but its go-live date is not public. GWCF is still the only sponsor that publicly pays grants through Blackbaud's Payment Assistant with REPAY. Give Interactive's "$40B+" is consistent with its known clients at 2025 asset levels ($41.80bn with Vanguard Charitable at $27.01bn), but $9.81bn of that rests on CT-discovered, DNS-confirmed implementation hosts rather than live portals. Without them the total is $32.59bn. A full-text screen of 126,684 line-6 "No" returns found 3 more likely sponsors and only $2.96m of Part I value, so the false-negative tail adds sponsors, not money. MS GIFT's line-3 investment income fell from 39.2 to 4.8 bps of public securities between FY2023 and FY2024 while its cash doubled, with no fee line to explain it. A booking change is the likely reading, but it is unproven. Recipient-side weights raise the R5 netting for the 11 largest recipients from $4.39bn to $4.80bn. In FY2024 the aggregate DAF payout was 25.9%, 22.8% excluding DAF-to-DAF transfers, while the median sponsor with $1m or more of DAF assets paid out 12.7% and one in five paid under 5%. The BDC parser now dates all KKR FS Income Trust rows, which shows KKR's Momentive (Community Brands) facility held at 96.1% of par. Its two Barings Envestnet rows are mis-parsed. NPT is the only large sponsor with any FTE figure (at most $136k of wages per FTE). Neither the 2025 SCF nor PSID 2023/2025 measures DAF holding. Funraise removes the anonymous option for DAFpay. The College publishes employers for 7 of 22 DAFCP instructors, none at a sponsor. Sponsors' observed core-platform payments run $118k–$498k a year (median about $218k). Fidelity Charitable's Android app shows launch crashes from v5.11 to v5.18 (2025-10 to 2026-08). crt.sh disallows all crawlers. Report claims resting only on its certificate data are unverified leads: Philanthropi's renewals, the CCT host date, and the stage of five Give implementation hosts [V wave 23]. Sources: [queue-batch38-vendors-ledgers-portals.md](mission-2026-11-14/queue-batch38-vendors-ledgers-portals.md), [queue-batch38-data-followups.md](mission-2026-11-14/queue-batch38-data-followups.md), [queue-batch38-closeout-checks.md](mission-2026-11-14/queue-batch38-closeout-checks.md), [compliance-note-crtsh-robots.md](mission-2026-11-14/compliance-note-crtsh-robots.md), [validation-wave23-report.md](mission-2026-11-14/validation-wave23-report.md).

## Data-file notes (not .md; for the owning agent)

- **`scripts/mission_bdc_loans.py` / `bdc-loans-latest-marks.csv` / `bdc-loans-daf-ecosystem.csv`:**
  - **Bug.** For rows with two MM/YY dates followed by par, cost, fair value and "—", the Barings Private Credit Corp Envestnet rows parse fair value as 0. Raw row: `Envestnet Inc. | First Lien Senior Secured Term Loan | SOFR + 2.75 %, 6.7 % Cash | 10/25 | 11/31 | 993 | 996 | 979 | — | (8)(20)`, filing `000185991926000099`.
  - **Fix.** Correct the parser, or set `parse_check` to exclude these rows from latest marks. Until then, the 2026-09-30 row's `below_par_signal` of `yes_lt_97` is spurious.
- **`watchlist.csv`:** disable the 11 `ct_crtsh` checks (decision 1 of the compliance note).
- **`relationship-graph-edges-additions-22.csv`:**
  - **EV002:** the cited posting URL now returns 404; mark it "posting not re-observable (wave 23)".
  - **EV003:** add "terms not re-read in wave 23 (npact.com unreachable)".
  - **EV006 notes:** add that the five CT-discovered clients ($9.81bn) are DNS-confirmed implementation hosts, not live portals.
  - **EV001:** cite the fcjc.fftc.org page and the fftc.org link rather than `daf.fftc.org/m/login` (robots intent).
  - **EV004, EV005, EV007, EV008:** no change.
- **`play-store-reviews-2021plus.csv`, `payout-triad-2021-2024.csv`, `bdc-unfunded-commitments-two-period.csv`:** no change (verified or rebuilt byte-identical).
- **`sponsor-pay-per-fte.csv`:** add to the NPT note that `wage_all_per_fte` is an upper bound.
- **`line6-fulltext-screen.csv`:** no change.

## Limits

- **Robots and access.**
  - **robots.txt read first** on every host fetched:
    - www.nptrust.org (allows all but two crawlers); www.nptgivingpoint.org (no robots file; SPA fallback);
    - www.thecommunityfoundation.org (the AI-crawler group shares the `*` rules, and `/nonprofit-faqs` is allowed); www.fftc.org (allows `/` and `/sites/default/files/`); fcjc.fftc.org (404);
    - www.giveinteractive.com (empty); archive.org (only `/control/` and `/report/` disallowed); jobs.y-axis.com (allows);
    - www.federalreserve.gov (404); psidtest.isr.umich.edu (allows all); help.funraise.io;
    - www.theamericancollege.edu and events.theamericancollege.edu; play.google.com (`/store/apps/details` allowed); www.givinga.com (allows all);
    - the GivingTuesday S3 mirror (none) and dns.google (none).
  - **Not fetched:**
    - **crt.sh**, including its robots.txt, per instruction.
    - **daf.fftc.org** pages (robots intent: Disallow).
    - **npact.com**: robots.txt was unreadable because of protocol errors, so its pages were not fetched.
    - **web.archive.org**: connection reset.
    - **paypal.com**: not attempted.
- **Not re-run or not re-read:**
  - the `fulltext` read of 126,736 returns, plus the `msgift` (script form), `fte` and `accounts` tasks (their key values were checked directly);
  - J.P. Morgan GivingPoint bundles; fftc.spectrumportal.net; the BILL and Blackbaud help pages;
  - the Montana and Ventura audits; the New Horizons 990; the PNC guide;
  - the REPAY negative search;
  - PSID 2021 and 2023;
  - the Benevity Play reviews; DPN's 990; the Chariot pricing and help pages; the FINRA pilot.
- **Interpretation.** These remain inferences, as batch 38 labels them:
  - the FFTC go-live window;
  - SBF's "hosted infrastructure" reading;
  - the line-6 manual verdicts;
  - the MS GIFT booking-change reading;
  - the recipient weights;
  - the payout-triad framing;
  - the break-even scenarios.

This is research, not legal advice.
