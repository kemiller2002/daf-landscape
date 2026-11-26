# Validation wave 15: batch 30 claims (California platform law, Candid, wealth-captive circulars, Every.org, Givinga, Goodstack, Endaoment, CF vendor coverage, Give tenants)

**Date:** 2026-11-15. **Validator:** independent-validation-agent-wave15.
**Register:** [`validation-register-wave15.csv`](../../data/mission-2026-11-14/validation-register-wave15.csv), rows V15-01 to V15-32.
**Method:** public sources only. I did not log in, submit forms or contact anyone. I formed each verdict from primary sources first and compared it with the batch-30 documents afterwards. I fetched no `*.fcsuite.com` page: Foundant's robots.txt bars AI agents, so Foundant tenants were checked by DNS only. The sources were:
- statute and regulation texts: Cal. Gov. Code §12599.9 (public.law mirror), 11 CCR §§314–323 (AG PDF, 19 pp), the AG platforms page (including its HTML source) and the PL-1 form and instructions;
- Candid: the Charity Check sample PDF (pdftotext), the API schema and FAQ (`.md`), and the Subscriber License Agreement (WebFetch, because curl got 403);
- sponsor terms: the FireAid/Latham report with Appendix B, the GS DAF Program Circular (pdftotext); the MS GIFT circular (I ran my own tesseract OCR on all 16 pages); the BofA CGF fee schedule and guideline paths; and Fidelity Charitable licence s.8;
- IRS: the 2019–2026 e-file indexes (HEAD shows the 2026 file was last modified 2026-10-21) and 12 XMLs from the GivingTuesday mirror: Every.org, Givinga original and amended, Goodstack FY2024 and FY2025, Endaoment FY6/22–FY6/24 (FY6/25 returns 404), Miami TY2025 and FFTC CY2023 and CY2024;
- Every.org's FY2023 audited statements (Drive download, pdftotext);
- the Janus Henderson CIA site and its Zendesk JSON, a Givinga blog post, the Goodstack terms, the Endaoment docs (fee schedule, submit-settled-grant OpenAPI and Fund Policies) and the Altruist fee schedule;
- CF pages: CFSEM, CFES, Omaha, EBCF (two pages), the GiftingNetwork PRLog release and the Give company page (Arizona CF refused both curl and WebFetch);
- dns.google (CNAME, A, and wildcard probes with random labels) and crt.sh for `ebcf`, `myfftc` and `omahafoundation.giveinteractive.com`.

**Scripts.** I did not re-run `scripts/mission_cf_vendor_close.py`. It needs its fetch cache, and none exists on this machine. Without `--fetch` it rebuilds only from that cache, and with `--fetch` it re-probes hosts and writes into `data/`. Instead I recomputed every coverage and share figure independently, from `cf-vendor-map-by-ein.csv` (v1), `cf-vendor-map-by-ein-v2.csv`, `spectrumportal-portal-vs-ledger-v2.csv`, `give-claim-reconciliation-batch30.csv` and the DAFRC FY2024 file. All the figures reproduce.

## Verdicts

| ID | Claim | Verdict | Key finding |
|---|---|---|---|
| V15-01 | §12599.9(a)(1)(A) and (E) text | **Confirmed** | Verbatim. |
| V15-02 | Vendor exclusion (B) "solely" and the DAF exclusion (C) | **Partially confirmed** | Quotes are accurate. (C) is conjunctive: the sponsor must solicit DAF accounts, receive recommendations, *and* not list charities to non-advisers. The doc quotes only the last limb. Its reading is unchanged. |
| V15-03 | 11 CCR 314(m), (q), (j), (d) | **Confirmed** | The regulation's labels are "Solicitation type A" and "Solicitation type E". |
| V15-04 | Type E disclosure "316(d)(3)"; remittance "318(c)(1)" | **Contradicted (citations); substance confirmed** | §316 covers good standing and §318 covers consent. The disclosure is **§317(d)(3)(A)**. The five-business-day and monthly-eligibility rule is **§320(c)(1)**. |
| V15-05 | AG page and PL-1: $625, Jan 15 / Jul 15, type labels, new filing service | **Confirmed** | PL-1 instructions define "consulting" platforms in Type E terms, so the doc's [I] becomes [F]. The late-Aug-2026 banner is now inside an HTML comment, which means it has been retired. |
| V15-06 | Candid sample PDF contents | **Confirmed** | IronPdf, created 2025-04-16, 1 page. It prints no time of day, cites 2011-33, and has no "most current update" statement. |
| V15-07 | JSON `report_date` in GMT; FAQ cites 2011-33; IRS checked "every 20 minutes" | **Confirmed** | |
| V15-08 | Subscriber licence §11.1 retention, §2.5, Charity Check "(discontinued)" | **Confirmed** | Dated 2026-09-14. Read through WebFetch. |
| V15-09 | GS DAF circular: $20k, $5k additions, $100 grants, check or wire, 0.60%→0.03%, ratios as of 2024-09-30 | **Confirmed** | FireAid App. B, p. 15. PDF created 2025-09-26. Latham named. |
| V15-10 | MS GIFT terms: $25k, $250, 0.27% (min $100), 0.07%, 1.00% | **Confirmed** | My own OCR. Last-Modified 2024-08-23. |
| V15-11 | BofA CGF: 0.90%→0.10% flat first-dollar, 0.12%; 2025/2026 guideline paths 404 | **Confirmed** | |
| V15-12 | Fidelity licence s.8 "may provide … export", Last Reviewed January 2021 | **Confirmed** | Aggregator evidence not re-read. |
| V15-13 | Every.org filed 990-PF for CY2020–2024; no CY2025 return yet | **Confirmed** | Five 990PF index rows; no 61-1913297 row in the 2026 index. |
| V15-14 | Every.org customer deposits and the "$0.11m–$0.54m" balance stock | **Partially confirmed** | Audited 2022 and 2023 figures match, and so do the 990-PF $544,382, $9.66m and $44.93m. **But the 990-PF's deferred revenue at 2023-12-31 (BOY) is $514,058, against $112,808 of audited customer deposits on the same date.** The 990-PF line is a broader measure, so the range mixes two measures. 2021 not re-read. |
| V15-15 | Givinga 1,421,011 from e-filed amended return 202503179349301975 | **Confirmed** | Values match exactly. The *original* return (202522379349301497, 2025-08-25) had a Schedule D with no DAF Part I values, and the amendment added them. |
| V15-16 | Givinga bank-fraud loss $316,184; Schedule R Givinga Inc; average $1.37 | **Confirmed** | |
| V15-17 | Janus Henderson CIA: 0.30%, Givinga Foundation as sponsor | **Confirmed** | 0.30% is "calculated daily and deducted monthly". Checks are "payable to Givinga Foundation". Givinga's blog post is dated 2025-09-16. The sponsor role is read from the operating text; no page uses the word "sponsor". |
| V15-18 | Goodstack FY2025: 3 DAFs; 16 grants = $1,623,550 | **Confirmed** | Recomputed: 54 grants totalling $2,078,401. |
| V15-19 | Goodstack "Donor Advised Basis"; "or such other charitable entity" | **Confirmed** | Effective 2026-06-22. |
| V15-20 | Endaoment: 331 / not reported / 6,000; FY6/25 404; DAFRC "Imputed" | **Confirmed** | |
| V15-21 | Endaoment out-of-scope rows; Altruist 0.50%→0.10% | **Confirmed** | |
| V15-22 | Endaoment settled-grant API wording; Fund Policies | **Confirmed** | v4.87.0; policies updated 2026-08-14. |
| V15-23 | Unmapped 39.2%→31.1% by count and 6.1%→2.8% by assets; Foundant 46.5% / 51.7%; Salesforce 24.8% | **Confirmed** | Recomputed exactly from v1 and v2. |
| V15-24 | Arizona CF and CFSEM on Salesforce | **Partially confirmed** | CFSEM confirmed: CNAME `…live.siteforce.com` and `x-sfdc-trace-flags`. The Arizona tenant `azfoundation.my.site.com` exists, but its first-party link could not be re-read (403 and empty WebFetch). |
| V15-25 | Miami 990 "CSUITE … fully integrated with Foundant's grant management software" | **Confirmed** | Medium is the right grade. |
| V15-26 | No wildcard on fcsuite.com or spectrumportal.net; DNS hits; ocf.iphiview.com NXDOMAIN | **Confirmed** | |
| V15-27 | Foundation Cloud split; CFES "FIMS → RE/FE NXT" | **Partially confirmed** | Arithmetic exact ($1,911m = 81.0% of $2,358m). The CFES page says "Raiser's Edge and Financial Edge" and does not say NXT. |
| V15-28 | Omaha → Foundant (invitations 2024-07-30) | **Confirmed** | Post dated Jul 29, 2024. Give certificates run 2023-05-03 to 2023-10-31. |
| V15-29 | FFTC: Give $654,500 (CY2023) → NPact → GiftingNetwork since 2026-07-01 | **Confirmed** | No Give line in the CY2024 top 5. The release is dated Sept. 23, 2026 [V]. |
| V15-30 | EBCF: Give (2023) → akoyaGO (notice 2025-07-09) | **Confirmed** | Certificates run 2023-06-06 to 2026-03-27 (36). The notice does not name akoyaGO; the vendor comes from the site's current links. |
| V15-31 | Give known clients $36.74bn; gap $3.26bn to "$40B+" | **Confirmed** | Arithmetic exact. The gap compares FY2024 assets with a 2025 claim and includes staging clients, so asset growth alone could close it. |
| V15-32 | "Give lost five CF tenants holding $4.79bn" | **Partially confirmed** | The sum is right. The doc's own table calls Kalamazoo and SDF trials, and only EBCF is a shown live loss. |

**Tally:** 26 confirmed, 5 partially confirmed, 1 contradicted (citation only), 0 unverifiable.

## Exact corrections

### `research/mission-2026-11-14/queue-batch30-legal-circulars.md`
1. **Line 94 (§2.4).** Replace "**Type E disclosure (316(d)(3)).**" with "**Type E disclosure (317(d)(3)(A)).**"
2. **Line 95 (§2.4).** Replace "**Type E remittance (318(c)(1)).**" with "**Type E remittance (320(c)(1)).**" (§316 is "Good Standing of Charitable Organizations" and §318 is "Consent from Recipient Charitable Organizations" [V wave 15].)
3. **Line 72 (§2.2, (C)).**
   - Replace: "It applies only where the sponsor \"does not list or reference by name …\""
   - With: "It applies only where the sponsor \"solicits donors to open donor-advised fund accounts or similar accounts, receives recommendations from donors …, and … does not list or reference by name one or more recipient charitable organizations for solicitation purposes on its platform for persons who do not have advisory privileges\" (the conditions are conjunctive)."
4. **Line 78 (§2.2).**
   - Replace: "**[I]** \"Consulting\" appears to correspond to Type E."
   - With: "\"Consulting\" corresponds to Type E. The PL-1 instructions describe \"consulting charitable fundraising platforms that provide their fundraising platform software to charitable organizations, who can then solicit or receive donations through the platform\" [F]."
5. **Line 79 (§2.2).** Append: "The AG page's replacement banner is now commented out in the page source. The page points filers to the Registry's Online Filing Service [V wave 15]."

### `research/mission-2026-11-14/queue-batch30-everyorg-givinga-goodstack.md`
1. **Line 33 (§0, P-QA3-07 cell), the bullet "The CY2024 990-PF shows deferred revenue of $544,382 [F]".**
   - Replace with: "The CY2024 990-PF shows deferred revenue of $544,382 (BOY $514,058) [F]. This is a broader measure than audited customer deposits: at 2023-12-31 the 990-PF shows $514,058, while the audit shows $112,808."
2. **Line 66 (§1.2 [I]).**
   - Replace: "The stock of donor balances is small: $0.11m–$0.54m against $17m–$45m of annual grants [C]."
   - With: "The stock of donor balances is small: audited customer deposits were $0.11m–$0.33m (2021–2023), against $17m–$45m of annual grants [C]. The 990-PF deferred revenue ($0.51m BOY, $0.54m EOY 2024) is not like-for-like with those deposits [V wave 15]."
3. **Line 58 (§1.2 table, 2024 column).** Replace "n/a. Part II deferred revenue: **$544,382**" with "n/a. Part II deferred revenue: **$544,382** (BOY $514,058; not comparable with audited customer deposits)".
4. **Line 103 (§2.1 Conclusion).** Append: "The original CY2024 return (202522379349301497, ReturnTs 2025-08-25) included Schedule D but no DAF Part I values. The amended return added them, which is consistent with DAFRC sourcing the figures outside its XML pipeline [V wave 15]."
5. **Line 118 (§2.2, Janus Henderson row, "Who is the sponsor" cell).** Replace "**Givinga Foundation** [F]:" with "**Givinga Foundation** ([F] operating text; the sponsor role is read from it, since no JH page uses the word 'sponsor'):".

### `research/mission-2026-11-14/queue-batch30-cf-coverage-give.md`
1. **Line 56 (§0, P-B29A-02).** Replace "CFES (high: FIMS → RE/FE NXT plus NPact tools, 2022–23)" with "CFES (high: FIMS → Blackbaud Raiser's Edge and Financial Edge, NXT generation inferred, plus NPact tools, 2022–23)".
2. **Line 173 (§2 table).** Replace "| Portal over Blackbaud FE NXT | 3 | 1,140 | 48.4% | CFES (high), GWCF (medium), San Diego (low) |" with "| Portal over Blackbaud FE (NXT stated or inferred) | 3 | 1,140 | 48.4% | CFES (high; 'Financial Edge', NXT not stated), GWCF (medium), San Diego (low) |".
3. **Line 58 (§0, P-GIV-07).**
   - Replace: "**Give lost five CF tenants holding $4.79bn of DAF assets. Only EBCF is shown live on Give, and none returned to Ren/iPhi.**"
   - With: "**Five CFs that held Give hosts ($4.79bn of DAF assets) did not stay on Give. Only one live loss is demonstrated: EBCF, $0.53bn. Omaha and FFTC had production-labelled hosts with no shown live use, Kalamazoo and San Diego were trials, and none returned to Ren/iPhi.**"
4. **Line 229 (§4 Durability).** Replace "The five lapsed tenants ($4.79bn of DAF assets)" with "The five CFs with lapsed Give hosts ($4.79bn of sponsor DAF assets, not Give AUM)".
5. **Line 208 (§3, gap bullet).** Append: "The gap compares FY2024 DAF assets with a 2025 claim, and it includes staging-only clients (Minneapolis, Thrivent, Stifel). Asset growth alone could close it [V wave 15]."
6. **Line 160 (§1.6).** Replace "**Hand checks covered the top 20 plus Ventura.**" with "**Hand checks covered the top 20 plus Ventura, Savannah and the Pi Fund.**"
7. **Line 114 (§1.3, Arizona row).** Append to Evidence: "Wave 15 could not re-read the sponsor page (403, and WebFetch returned nothing). The tenant `azfoundation.my.site.com` is confirmed to exist (it 301-redirects to `/s/`)."

### `research/DAF-INDUSTRY-REPORT-2026-11.md`
1. **New subsection after §11.9:** "### 11.10 Batch 30 (validated, wave 15)", containing:

   > **Batch 30 (validated, wave 15).** California's platform law reaches DAF technology vendors on its text, and custody is not the test. An own-brand app that lists charities for "grants of recommended donations" is Type A (§12599.9(a)(1)(A); 11 CCR 314(m)). A white-label portal licensed to a sponsor is Type E (314(q)). The DAF exclusion names only the sponsor. Type E duties are light for a vendor that never holds funds: a disclosure (§317(d)(3)) and five-business-day remittance (§320(c)(1)). Candid's Charity Check PDF meets most of Rev. Proc. 2018-32 §8.01. It prints no time of day, though the JSON gives one in GMT, and it still cites the superseded Rev. Proc. 2011-33. Only Candid's subscriber licence, not its API licence, allows retention after termination. Current wealth-captive terms: GS DAF $20k minimum and $100 grants by check or wire (circular reproduced in FireAid's 2025 report); MS GIFT $25k and $250 with a 0.27% administrator fee; BofA CGF a flat first-dollar 0.90%–0.10%. Givinga's 1,421,011 accounts ($1.37 average) come from an e-filed amended CY2024 return. Givinga Foundation is the sponsor behind Janus Henderson's 0.30% Charitable Investment Accounts. Every.org files 990-PF and holds only $0.1–0.3m of audited donor credit, so it has no DAF book. Goodstack US reported 3 DAFs in FY2025, down from 7,268. Endaoment reported 6,000 DAFs for FY6/24. Unmapped community foundations fell from 39.2% to 31.1% of 803 by count, and from 6.1% to 2.8% by DAF assets. Foundant leads on count (46.5%, a floor) and Salesforce on assets (24.8%, adding Arizona CF and CFSEM). None of the 14 Foundation Cloud portals is evidenced as an NPact ledger; 81% of their assets sit on Blackbaud. Give Interactive's only demonstrated live CF loss is East Bay (to akoyaGO). Omaha moved to Foundant on 2024-07-30, and FFTC went through NPact to GiftingNetwork on 2026-07-01. Give's known clients hold $36.7bn of FY2024 DAF assets, against its "$40B+" 2025 claim [V wave 15]. Sources: [queue-batch30-legal-circulars.md](mission-2026-11-14/queue-batch30-legal-circulars.md), [queue-batch30-everyorg-givinga-goodstack.md](mission-2026-11-14/queue-batch30-everyorg-givinga-goodstack.md), [queue-batch30-cf-coverage-give.md](mission-2026-11-14/queue-batch30-cf-coverage-give.md), [validation-wave15-report.md](mission-2026-11-14/validation-wave15-report.md).

## Data-file notes (not .md; for the owning agent)

- **`spectrumportal-portal-vs-ledger-v2.csv` / `cf-vendor-map-by-ein-v2.csv`, CFES row:** change `split_class` from "portal over Blackbaud FE NXT" to "portal over Blackbaud FE (NXT inferred)". The confidence for Blackbaud stays high.
- **`digital-sponsor-entities-2026.csv`, Every.org row:** the `balance_proxy` note should say the 990-PF deferred revenue (BOY $514,058) is not comparable with audited customer deposits ($112,808 at 2023-12-31).
- **`give-tenants-lapses-batch30.csv`:** no value changes. The status text for Kalamazoo and San Diego should read "trial; incumbent retained", not "lapsed tenant".
- **`cf-vendor-map-by-ein-v2.csv`:** two rows are named "Omaha Community Foundation": EIN 47-0645958, with $519.7m, and EIN 36-3789990, with $75.9m. They share one portal URL. The second EIN looks mis-joined and should be checked. This was not investigated here.
- **`relationship-graph-edges-additions-15.csv`:** EO001–EO015 are consistent with the sources re-read (EO001/002/004 JH, EO008 "OUR ADMINISTRATIVE PROVIDER GIVINGA, INC.", EO012 Goodstack terms, EO014 Altruist, EO015 Chariot in the Fund Policies). No changes.
- **`wealth-captive-terms-2026.csv`:** the values checked (minimums, minimum grants, fee tiers, rails) match. No changes.

## Limits

- **Statute.** It was read through the public.law mirror; leginfo was not retried.
- **Candid.** The Subscriber Licence was read through a summarising fetch tool.
- **Every.org.** The FY2021 and FY2022 audit reports were not opened, so the 2021 deposit figure is unverified.
- **Arizona CF.** The first-party fund-access page was not readable by script or WebFetch.
- **Not re-checked:**
  - the Fidelity aggregator notices (Morningstar 2023, Empower snippet);
  - the Tulsa job posting and the San Diego Blackbaud case study;
  - New Horizons and the `nhf`/`jttw` certificate spans;
  - the hand-check rows other than Arizona, CFSEM and Miami;
  - the Bainbridge label collision, which rests on a fetch made before the robots.txt review. Wave 15 confirmed only that `bcf.fcsuite.com` resolves.
- **`mission_cf_vendor_close.py`** was not re-run (see Method). The figures were recomputed from its outputs.
