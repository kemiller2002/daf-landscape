# Independent validation, wave 9 (V9-01 to V9-09)

**Date:** 2026-11-14 · **Validator:** independent-validation-agent-wave9 · **Register:** [`validation-register-wave9.csv`](../../data/mission-2026-11-14/validation-register-wave9.csv) (9 rows)

**Method.** For each claim, the primary source was fetched and a verdict formed before the repo document making the claim was read: the sponsor agreements, Candid licence and docs, Benevity PDF, SEC EDGAR filings and CF homepages. The verdict was then compared with `queue-sponsor-terms-data-clauses.md`, `queue-bdc-fix-labour-benevity.md` and `queue-cf-vendor-map.md`. No logins, form submissions or outreach were made. All evidence is from 2021 or later. The only exception is Vanguard's 2016 site Terms, which were read for context only.

## Verdicts

| ID | Claim | Result | Key point |
|---|---|---|---|
| V9-01 | NCF Program Agreement bans credential sharing with third parties and scraping, and authorizes no third-party service | **confirmed** | Verbatim. "Effective as of September 17, 2025". The third-party sentence continues "...or an NCF charitable fund on behalf of users". |
| V9-02 | Vanguard bars "electronic agent, bot", permits holder-run read-only aggregators, and names "grant recommendation processing services" | **confirmed with caveat** | "Read-only" is not in the text. The permission is for an Authorized Person to use "aggregators or similar web crawler devices for the purpose of aggregating information". A hosted aggregator that uses the donor's credentials is an "Unauthorized Third Party". |
| V9-03 | NPT Terms (2026-10-29) ban robot harvesting and AI-tool building | **confirmed** | The AI clause is broader than stated: it also covers "operation of a machine learning or AI system". |
| V9-04 | Fidelity Charitable License Agreement s.8 provides for third-party export | **confirmed with caveat** | s.8 is permissive ("may provide") and undated, and no live export feature was found. |
| V9-05 | AEF FAQ shows a DonorCentral "Export" button | **confirmed with caveat** | The button exports a grants-paid list in legacy DonorCentral. It appears on the Ren-migration "Technology Upgrade" support page, so it does not show a current or full-ledger export. |
| V9-06 | Candid licence (2026-09-14) bars redistribution and AI extraction, and requires all use to stop on termination; Charity Check sources | **partially confirmed** | The date, termination clause and the five sources (Pub78, BMF, IRB, revocations, OFAC SDN) are correct. "Bars AI extraction" and "bars redistribution" drop the scope qualifiers (below). |
| V9-07 | Bonterra BDC loans and script reproduction | **partially confirmed** | The 2024/2025 finding and FS KKR's $133.4m par at 99.5% are confirmed, and the script output is byte-identical. However, the Golub last marks are wrong, and five New Mountain BDCs marked at 98.25% are missing (below). |
| V9-08 | Benevity: the $500 cap, not the 2.99% fee, is lifted for matching gifts and securities | **confirmed** | The schedule (updated 2026-10-01) says the "Cause Support Fee Caps ... do not apply to matching transactions or gift of securities donations". The 2.99% rate and $500 cap are confirmed. |
| V9-09 | CF vendor map counts and the Stellar→Foundant migrations | **confirmed with caveat** | Counts recompute exactly. Spot-check vendor error rate is **0/15** (95% CI upper bound 21.8%), with 2/15 evidence-label defects. The migration dates in the repo are too early. |

## Details that change the record

### V9-07: the Bonterra loans, checked against EDGAR

- **9/8/2027 loan (legacy CyberGrants).**
  - **BlackRock TCP and BlackRock Direct Lending.** In their FY2025 10-Ks and Q3-2025 10-Qs, the loan appears only under the *December 31, 2024* schedule. Example: TCPC 5,832,706 par, 5,779,628 FV. The repo is correct for both.
  - **Golub Capital BDC: the repo is wrong.** The 10-Q for the period ending 2024-12-31 (accession 0001476765-25-000016) carries current-period XBRL contexts. It shows 92,893 + 7,599 + 3,957 (PIK) + 256 = **$104.7m par, fair value = par (100.0%)**. The repo has 2024-09-30 at 98.5%.
  - **Golub Capital Direct Lending: also wrong.** The 10-Q for 2024-12-31 (0001868878-25-000011) shows 5,153 + 3,591 + 128 + 682 = **$9.55m, at par**.
  - **Why the Golub rows were missed.** The script keeps only the earliest and latest filing per (term, BDC). The latest Golub filings found (2025-06-30 and 2025-09-30) carry only the 9/30/2024 comparative, so the Q1-FY2025 10-Qs were skipped.
  - **What this means.** Marking the loan at par just before it leaves the schedule fits repayment at par in early 2025, which supports the "probable 2025 refinancing" note.
- **3/5/2032 facility at 2026-09-30.** The repo's figures are confirmed as follows:
  - FSK: SF+4.8 (printed rounded), 133.4 par / 132.9 cost / 132.7 FV in $m, = 99.48%.
  - KFIT 99.43%; KFITS 99.43%.
  - AB PCI 99.0%; AB PLF 99.0%.
  - CCS IX term loan 99.19%.
- **Missing lenders.** The New Mountain family holds the facility at SOFR(Q)+5.00%, 03/2032, marked **98.25%**:

  | Lender | Par | FV |
  |---|---|---|
  | NMFC | 14,876 (+1,620) | 14,615 (+1,592) |
  | NM Guardian IV BDC | 9,211 | 9,050 |
  | NM Guardian IV Income Fund | 2,233 | 2,194 |
  | NM Private Credit Fund | 7,271 | 7,144 |
  | NMF SLF I | 6,570 | 6,455 |

  - These rows exist in `bdc-loans-daf-ecosystem.csv` only as `name_or_subtotal_row`. New Mountain prints the borrower on one row and the instruments on the following rows, which the parser does not join.
  - With these lenders included, the correct range is **98.2–99.5%**.
- **Script reproduction.**
  - `scripts/mission_bdc_loans.py` was re-run with a fresh cache and `--fetch`. Outputs were redirected to scratch through a wrapper, so the repo files were not touched.
  - Run stats: hits=1284, bdc_filings=189, rows 650→600, latest_mark_rows=231.
  - Both CSVs are **byte-identical** to the repo copies (sha256 prefixes `0dbe8a37c60e8bea` and `ba273839e4fa81f8`).
  - The script is reproducible. The errors above come from its design (earliest-plus-latest filing selection and the row-joining heuristic), not from drift.

### V9-06: Candid clause scope

- **Redistribution.**
  - Clause 3.b.ii bars republishing or distributing "except as expressly permitted herein".
  - Clause 3.b.v adds "except as permitted herein and in the Order Form".
  - Clause 3.a.i expressly permits providing Candid Data to Licensee Customers through the Licensee Site.
- **AI.** The AI sentence in 3.b.xi qualifies a prohibition on data mining or extraction for three purposes:
  1. compiling a nonprofit database "other than for Licensee's own internal business use";
  2. licensing or selling such a database;
  3. building a directly competitive service.

  It is not a free-standing ban on AI use of Candid Data.
- **Charity Check sources.** The FAQ adds the GuideStar database, and California AG and FTB data for the state endpoint.

### V9-09: spot-check (seed 20261114, 15 high/medium rows)

- **Vendor confirmed live on the foundation's site for all 15:** RI Foundation, Alaska CF, CF Grand Forks, CF Southwest (MO), Bermuda CF, N. Indiana CF, CF Wabash Co., Central Montana F., Philadelphia F. (Salesforce `philafound.my.site.com`), CF Texas Hill Country, San Diego F. (`spectrumportal.net`), Berrien CF (akoyaGO), Greater NW Kansas CF, Mackinac Island CF (akoyaGO) and Quad Cities CF.
- **Evidence-label defects:**
  - **RI Foundation.** The row is labelled `homepage_link_vendor_host`, but the homepage has no fcsuite link. The link is on `/giving/give-well/donorportal`, which matches the row's `evidence_url`.
  - **CF Grand Forks.** The `portal_url` is an event-ticket page. The fund-holder portal `grandforks.fcsuite.com/erp/portal` is linked from `/fh-portal.html`.
- **Migrations.** All three sites show live fcsuite fund logins.
  - ARCF's announcement "Arkansas Community Foundation announces database transition" is dated **April 20, 2026**.
  - Acadiana's TY2024 990 still lists Stellar ($118,458).
  - These point to **2025–2026** migrations rather than the repo's "probably 2023–2025".

## Exact corrections

### `research/mission-2026-11-14/queue-bdc-fix-labour-benevity.md`

1. **§1 item 2, Golub bullets.**
   - Replace "Golub Capital BDC: 2024-09-30, facility 98.5%." with "Golub Capital BDC: 2024-12-31, 100.0% of par ($104.7m; 10-Q 0001476765-25-000016)."
   - Replace "Golub Capital Direct Lending: 2024-09-30, 98.5%." with "Golub Capital Direct Lending: 2024-12-31, 100.0% of par ($9.55m; 10-Q 0001868878-25-000011)."
2. **§1 item 2, 2032 facility.**
   - Replace "is held at **2026-09-30** at 99.0–99.5%:" with "is held at **2026-09-30** at 98.2–99.5%:".
   - Add a bullet: "New Mountain Finance, NM Guardian IV BDC, NM Guardian IV Income Fund, NM Private Credit Fund and NMF SLF I: SOFR(Q)+5.00%, 03/2032, 98.25% (e.g. NMFC 14,876 par / 14,615 FV, $000). Not captured by the parser (borrower printed on its own row)."
   - Change "FS KKR: SF+4.8 (as printed)" to keep "(as printed; rounded, 4.75 not confirmed from FSK)".
3. **§2.2 (line "Golub Capital BDC (rows 4047–4050) and Golub Capital Direct Lending (rows 2478–2481): **2024-09-30**.")** Append: "These are the latest marks *in the filings the script selected*. The 12/31/2024 10-Qs carry current-period rows at par (see wave-9 V9-07)."
4. **§2.3 table, Golub rows.**
   - Change `| Golub Capital BDC | 09/2027 one-stop | 2024-09-30 | ... | 98.5 | not in schedule at 2025-09-30 |` to period `2024-12-31` and mark `100.0`.
   - Make the same change for Golub Capital Direct Lending.
   - Add a row: `| New Mountain family (5 BDCs) | 03/2032 | 2026-09-30 | SOFR+5.00% | 98.25 | held; missed by parser |`.

### `data/mission-2026-11-14/bdc-loans-latest-marks.csv`

- **Golub rows.** The rows for `GOLUB CAPITAL BDC, Inc.` and `GOLUB CAPITAL DIRECT LENDING CORP` with `period_ending` 2024-09-30 and maturity 09/2027 are superseded by 2024-12-31 rows (FV = par, `facility_fv_pct_of_par` 100.0). Regenerate the file with the script fixes below; do not hand-edit it.
- **New Mountain rows.** Add rows for New Mountain Finance Corp, New Mountain Guardian IV BDC, New Mountain Guardian IV Income Fund, New Mountain Private Credit Fund and NMF SLF I. Each is a Bonterra 03/2032 facility at 2026-09-30 with `facility_fv_pct_of_par` ≈ 98.25.

### `scripts/mission_bdc_loans.py`

1. **Filing selection.**
   - Current rule: keep the earliest and latest filing per (term, BDC).
   - Change: also keep the latest filing whose *own-period* rows contain the borrower, or keep all filings and let `dedupe` and `latest_marks` choose.
   - Reason: this fixes Golub's latest period, 2024-12-31.
2. **Row continuation.** When a borrower cell is followed by rows whose first cell is an instrument ("First lien", "First Lien(…)"), attach them to the borrower. This is New Mountain's layout, which is currently classified `name_or_subtotal_row`.

### `research/mission-2026-11-14/queue-sponsor-terms-data-clauses.md`

1. **§1 table, P-EXP-03 row.**
   - Replace "It also expressly *permits* account holders to use read-only \"aggregators\" [F]." with: "It also expressly permits an Authorized Person to use \"aggregators or similar web crawler devices for the purpose of aggregating information\" [F]; a third party using the holder's credentials is an \"Unauthorized Third Party\" and may not [F]. That this is in effect read-only, self-run aggregation is [I]."
   - Replace "and use of site data to build AI tools [F]" with "and use of site data or user data for the development or operation of any software, model or AI system [F]".
2. **§1 table, P-QA2-07 row.**
   - Replace "bars republication" with "bars republication except as expressly permitted (Licensee Customers via the Licensee Site; Order Form)".
   - Replace "expressly bars extraction for \"artificial intelligence\"" with "applies its database-building/resale/competition ban expressly to extraction \"for use in or through the use of artificial intelligence\" (internal business use is outside the ban)".
3. **§3 "Reading", item 2.** Mark "**Allowed:** read-only aggregation by the account holder." as [I]. Add: "Vanguard may block 'systematic, commercial or otherwise inappropriate' automated access in its discretion."
4. **§3 "Reading", item 3.** After "Its License Agreement provides for third-party export", insert "(s.8, permissive 'may provide', undated; no live feature found)".
5. **§4 (AEF).** Add: "The instruction sits on AEF's 'Technology Upgrade' (Ren) support site and covers only a grants-paid list in legacy DonorCentral."

### `research/mission-2026-11-14/queue-cf-vendor-map.md`

1. **§ Stellar/Ren → Foundant switches.** Replace "These are probably 2023–2025 migrations [I]. Dates are not established." with "These are probably 2025–2026 migrations [I]. Arkansas CF's 'announces database transition' post is dated 2026-04-20, and Acadiana still paid Stellar $118,458 in TY2024. Flint keeps a legacy `cfgf.iphiview.com` link."
2. **Accuracy section.** Add: "Wave-9 spot-check: 15 random high/medium rows, vendor correct 15/15 (0%; 95% upper bound 21.8%); 2 evidence-label defects."

### `data/mission-2026-11-14/cf-vendor-map-by-ein.csv`

- **EIN 222604963 (Rhode Island Foundation).** Change `evidence_type` from `homepage_link_vendor_host` to `site_link_vendor_host`. The link is on `/giving/give-well/donorportal`, not the homepage.
- **EIN 450448088 (CF of Grand Forks).** Change `portal_url` to `https://grandforks.fcsuite.com/erp/portal` and `evidence_url` to `https://www.gofoundation.org/fh-portal.html`. The current event-ticket link is evidence of a tenant, not of a portal.

## Primary sources used

- NCF Program Agreement: https://secure.ncfgiving.com/agreement
- Vanguard Charitable User Agreement: https://www.vanguardcharitable.org/company-policies/user-agreement
- NPT Terms of Use / Privacy: https://www.nptrust.org/privacy-policy/
- Fidelity Charitable License Agreement: https://www.fidelitycharitable.org/legal/license-agreement-and-copyright.html
- AEF platform resources: https://engage.aefonline.org/platform-resources/
- Candid API License Agreement: https://candid.org/terms-of-service/api-license-agreement/
- Candid Charity Check FAQ: https://developer.candid.org/reference/faqs-charity-check.md
- Candid Charity Check getting-started page: https://developer.candid.org/reference/get-started-with-charity-check.md
- Benevity Foundations Fees Schedule: https://go.benevity.com/hubfs/website/en/Benevity-Fees-Schedule.pdf
- EDGAR, FSK: https://www.sec.gov/Archives/edgar/data/1422183/000162828026070499/fsk-20260930.htm
- EDGAR, NMFC: https://www.sec.gov/Archives/edgar/data/1496099/000149609926000034/nmfc-20260930.htm
- EDGAR, NM Guardian IV BDC, NM Guardian IV Income Fund, NM Private Credit Fund and NMF SLF I: Q3-2026 10-Qs
- EDGAR, KFIT and KFITS: Q3-2026 10-Qs
- EDGAR, AB PCI and AB PLF: Q3-2026 10-Qs
- EDGAR, CCS IX: Q3-2026 10-Q
- EDGAR, TCPC: FY2025 10-K and Q3-2025 10-Q
- EDGAR, BlackRock Direct Lending: FY2025 10-K and Q3-2025 10-Q
- EDGAR, GBDC: 10-Q for 2024-12-31 (0001476765-25-000016)
- EDGAR, GDLC: 10-Q for 2024-12-31 (0001868878-25-000011) and 10-Q for 2025-09-30
- CF homepages for the 15 sampled rows
- arcf.org "announces database transition" post
- cfgf.org login page
- Acadiana TY2024 990 XML: https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503169349308100_public.xml
