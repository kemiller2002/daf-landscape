# Queue Q-N16, P-CFV-03 and P-FCG-02: BDC lender coverage, CF ledger/portal switches, Goodstack's US DAF sponsor

**Date:** 2026-11-14 · **Queue items:** Q-N16 (BDC lender coverage and Golub dating), P-CFV-03 (dating the 2022–2026 CF switches), P-FCG-02 (Goodstack US foundation FY2025 990) · **Recency:** 2021+ evidence only · **No outreach, logins or form submissions.**

**Data written:**
- [`bdc-loans-daf-ecosystem.csv`](../../data/mission-2026-11-14/bdc-loans-daf-ecosystem.csv) (regenerated, 1,252 rows) and [`bdc-loans-latest-marks.csv`](../../data/mission-2026-11-14/bdc-loans-latest-marks.csv) (regenerated, 304 rows)
- [`bdc-loans-daf-ecosystem-v2.csv`](../../data/mission-2026-11-14/bdc-loans-daf-ecosystem-v2.csv) and [`bdc-loans-latest-marks-v2.csv`](../../data/mission-2026-11-14/bdc-loans-latest-marks-v2.csv): the wave-9 files, kept unchanged (sha256 prefixes `0dbe8a37c60e8bea` and `ba273839e4fa81f8`)
- [`cf-vendor-migrations-2022-2026.csv`](../../data/mission-2026-11-14/cf-vendor-migrations-2022-2026.csv) (8 event rows, 50 evidence rows)
- [`queue-proposals-bdc-migrations.csv`](../../data/mission-2026-11-14/queue-proposals-bdc-migrations.csv) (4 proposals, P-BMG-01 to P-BMG-04)

**Scripts:**
- [`scripts/mission_bdc_loans.py`](../../scripts/mission_bdc_loans.py) (Q-N16 fixes a–d, below)
- [`scripts/mission_cf_migrations_goodstack.py`](../../scripts/mission_cf_migrations_goodstack.py) (new; tasks `migrations` and `goodstack`)

**Builds on:** [validation-wave9-report.md](validation-wave9-report.md) V9-07 (the defects) · [queue-bdc-fix-labour-benevity.md](queue-bdc-fix-labour-benevity.md) · [queue-cf-vendor-map.md](queue-cf-vendor-map.md) §5 and its wave-9 corrections · [queue-fidelity-chariot-goodstack-vanguard.md](queue-fidelity-chariot-goodstack-vanguard.md) §4 and its wave-7 corrections

**Evidence tags:** **[F]** read from a filing or published page · **[S]** computed by a script from those sources · **[I]** inference.

---

## 1. Key findings

1. **Golub is fixed: the legacy CyberGrants/Bonterra 9/2027 loan was last marked at par on 2024-12-31.** [S] Golub Capital BDC: $104,705k par, fair value = par (100.0%); Golub Capital Direct Lending: $9,554k, 100.0%. Both are `not_in_schedule_at_2025-09-30`. This matches wave 9 exactly ([GBDC 10-Q 0001476765-25-000016](https://www.sec.gov/Archives/edgar/data/1476765/000147676525000016/); GDLC 10-Q 0001868878-25-000011). Every 2027-loan holder's last mark is now 2024-12-31 at 99.3–100%, except Golub BDC 3 (2024-03-31, 98.0%, before its 2024 merger into GBDC) and BlackRock Capital Investment (2023-12-31, before its 2024 merger into TCPC).
2. **New Mountain is now captured: five funds hold the 3/5/2032 Bonterra facility at 98.25–98.27% (2026-09-30).** [S] Funded par ($000), from each fund's Q3-2026 10-Q:

   | Lender | Funded par | Facility FV % par | Spread |
   |---|---|---|---|
   | New Mountain Finance Corp | 17,017 (14,876 + 1,620 + 521 drawn DDTL) | 98.25 | SOFR(Q)+5.00% |
   | New Mountain Guardian IV BDC | 12,394 | 98.26 | SOFR(Q)+5.00% |
   | New Mountain Private Credit Fund | 10,104 | 98.25 | SOFR(Q)+5.00% |
   | NMF SLF I | 8,797 | 98.25 | SOFR(Q)+5.00% |
   | New Mountain Guardian IV Income Fund | 3,004 | 98.27 | SOFR(Q)+5.00% |

   Each also lists undrawn 03/2027 and 10/2027 commitments, now typed `undrawn_commitment` and excluded from the facility percentage. Source: for example [NMFC 10-Q](https://www.sec.gov/Archives/edgar/data/1496099/000149609926000034/nmfc-20260930.htm). **With these funds, 13 BDCs hold the 2032 facility at 98.25–99.5% of par.** New Mountain marks lowest, FS KKR highest (99.47%).
3. **No other BDC lender exists for Benevity, Ren, Foundant or Fundraise Up.** [F] EDGAR full-text search over 10-K/10-Q since 2021 returns no hit from any BDC CIK for "Benevity", "Benevity Inc", "Renaissance Philanthropic", "RenPSG", "RenPhil", "Foundant", "Foundant Technologies" or "Fundraise Up" (each is an auditable `no_bdc_hit` row). Benevity and Fundraise Up appear on EDGAR only as Form D issuers.
   - **Lender sets for the other targets are unchanged:** Bloomerang has 7 Golub/Monroe funds; Foundation Source has Audax Private Credit Fund; Orion has 17 lenders.
   - **Community Brands/Momentive gains two historical lenders:** New Mountain Guardian III (02/2028 loan, last 2024-06-30 at 100%) and Oaktree Specialty Lending (2021 rows).
   - **Outside the BDC filter:** registered funds hold Bonterra LLC loans too, for example KKR US Direct Lending Fund-U (N-PORT/N-CSR). See P-BMG-01.
4. **P-CFV-03: every dated move is *to* Foundant, and the map's Foundation Cloud "dual logins" are outgoing portals, not wins.** [F]/[I] Table in §3.2.
   - **Three Ren (Stellar) iPhi → Foundant switches are now dated:**
     - Acadiana: 2025-05-14 [I].
     - Flint: around January 2026 [I].
     - Arkansas: 2026-06-01 [F].
   - **Yakima left iPhi for akoyaGO** (undated). Its iPhi host no longer resolves.
   - **CF Tampa Bay and Winston-Salem went from Blackbaud with a Foundation Cloud (spectrumportal.net) fund portal to Foundant:**
     - Winston-Salem: 2024-09-30 [I].
     - Tampa Bay: summer 2026 [I].
   - **New Mexico CF has no fund-login migration.** Its spectrumportal site is a partner/grantee portal, and Foundant serves only donations.
   - **Indian River moved from a donor-portal.org white-label portal to Foundant** on 2023-07-31.
5. **What this means [I]:**
   - Ren iPhi lost 4 of the 8 flagged CFs between 2025 and 2026, including $350m (Arkansas) and $145m (Acadiana) DAF books.
   - Foundant won 6 of 8.
   - No flagged CF moved *to* Foundation Cloud. The "Foundation Cloud appears at former Foundant/iPhi sites" reading in queue-cf-vendor-map.md §5 does not hold for these five.
6. **P-FCG-02: the FY2025 jump is real money, but the DAF count is a reporting change [F]/[I].**
   - **Growth:** revenue rose from $3.12m to $16.34m. Grants paid rose from $1.74m to $6.94m. Year-end cash rose from $1.81m to $12.63m.
   - **The DAF count change:** Schedule D went from 7,268 DAFs ($1.81m) to 3 DAFs ($10.77m year-end; $11.58m contributed; only $1.66m granted).
   - **Evidence that a few large donors drive it:** "substantial contributors" account for $13.02m of $19.73m five-year support. The largest Schedule I grants are $200k each.
   - **Reading [I]:** in FY2025 the foundation reports a few large donor-advised funds (probably corporate or major-donor programmes) as DAFs, and stopped counting per-user micro-donation balances (for example Adyen Giving round-ups) as DAFs. Its audited statements would confirm this (P-BMG-04).

---

## 2. Q-N16: BDC lender coverage and Golub dating

### 2.1 Method: changes to `mission_bdc_loans.py`

The script header documents each change as Q-N16 (a)–(d). All numbers still come only from the filing text.

1. **(a) Filing selection walks back.**
   - **Old rule:** per (EDGAR phrase, BDC), the script read the earliest and latest filing only. Golub's 12/31/2024 10-Q, the last one with current-period Bonterra rows, was never read, because later filings show only the 9/30/2024 comparative.
   - **New rule:** the script reads the latest filing, then earlier ones. It stops when every dated debt facility seen in the walked filings, or in the earliest filing, has at least one own-period row (`period_ending == filing_period_ending`). It then adds the earliest filing.
   - `which_filing` = `latest` / `walkback` / `earliest`. A facility's first own-period row met on the way back is its last mark.
2. **(b) BDC identity by CIK.**
   - Some BDC hits carry the Exchange Act file number (000-5xxxx) instead of 814-. Examples: BlackRock Direct Lending, CCS IX, Golub BDC 4, Golub DL Unlevered, NM Guardian IV Income Fund, NM Private Credit Fund and KKR FS Income Trust Select.
   - All hits of a CIK that has any 814- hit are now kept.
3. **(c) Row continuation.**
   - Two layouts were missed:
     - `INSTR.match` is anchored, so "First lien …" first cells never matched.
     - New Mountain prints the borrower alone and starts the first instrument row with the industry (`Software | First lien (2)(11)(12) | SOFR(Q) | 5.00 % | …`).
   - **Fixes:**
     - A `LIEN` pattern ("first/second lien", "senior secured", "subordinated") now qualifies a continuation row.
     - A name-only borrower row also takes the next row when its second cell is an instrument.
   - **New row type `undrawn_commitment`.** Rows labelled "Undrawn"/"Unfunded" no longer count in facility FV % of par.
4. **(d) Extra phrases and an incremental hit cache.**
   - **Phrases added:** Foundant Technologies, RenPhil, Benevity Inc, Momentive Software and Bonterra LLC. The last is a cross-check on the "Bonterra" paging.
   - **Cache:** phrases already searched are not searched again.
5. **Status flag.**
   - `lender_latest_schedule_period` is now computed over **all filings read, before deduplication**. Without this, a later filing whose only Bonterra rows are repeated comparatives would be dropped by dedupe, and the lender's latest period would understate.

**Run.** `python3 scripts/mission_bdc_loans.py --cache-dir <dir> --fetch`.
- The cache was seeded with the 168 wave-9 documents; 236 more were fetched.
- A second run without `--fetch` reproduced both CSVs byte-for-byte (sha256 prefixes `ed55e1e98f2af170` and `0d2689ba0cc0b645`).
- Run stats: hits 1,495; filings read 501 (122 latest, 269 walk-back, 110 earliest; the old rule would read 232); rows 2,312 → 1,252 after dedupe; latest-mark rows 304. Row periods come from XBRL for 1,682 rows, schedule headings for 574 and the filing-period fallback for 40; 160 rows are flagged `row_period_conflict`.

### 2.2 Before and after

| | v2 (wave 9, `-v2.csv`) | v3 (this run) |
|---|---|---|
| Schedule rows / latest-mark rows | 600 / 231 | 1,252 / 304 |
| Filings read | 189 | 501 |
| `debt` rows | 334 | 668 |
| `name_or_subtotal_row` | 83 | 207 (borrower header rows now followed by parsed tranches) |
| `undrawn_commitment` | n/a | 75 |
| Bonterra lenders in latest marks / with held debt | 17 / 9 | 22 / 14 |
| Community Brands/Momentive lenders | 21 | 25 |
| Bloomerang, Envestnet, Foundation Source, Orion lenders | 7, 11, 1, 17 | unchanged |
| Golub BDC / GDLC 9/2027 last mark | 2024-09-30, 98.5% | **2024-12-31, 100.0%** |
| New Mountain Bonterra 2032 rows | `name_or_subtotal_row` only | 5 lenders, 98.25–98.27% |
| Lenders added | | NMF SLF I, NM Guardian IV BDC, NM Guardian IV Income Fund, NM Guardian III, Oaktree Specialty Lending. New Mountain Finance and NM Private Credit Fund were already present for other targets and now also carry Bonterra rows |

### 2.3 Bonterra holders after the fix (`bdc-loans-latest-marks.csv`)

| Lender | Facility | Latest row period | Facility FV % par | Status |
|---|---|---|---|---|
| Golub Capital BDC | 09/2027 | 2024-12-31 | 100.0 | not in schedule at 2025-09-30 |
| Golub Capital Direct Lending | 09/2027 | 2024-12-31 | 100.0 | not in schedule at 2025-09-30 |
| BlackRock TCP / BlackRock Direct Lending | 09/2027 | 2024-12-31 | 99.34 | not in schedule at 2025-12-31 |
| Monroe Capital / Monroe Income Plus | 09/2027 | 2024-12-31 | 99.39 / 99.38 | not in schedule at 2025-12-31 / 2026-03-31 |
| AB Private Lending Fund | 09/2027 | 2024-12-31 | 99.74 | not in schedule at 2026-09-30 |
| AB PCI, AB PLF, CCS IX, Crescent | 03/2032 | 2026-09-30 | 99.01–99.02 | held |
| FS KKR; KFIT; KFITS | 03/2032 | 2026-09-30 | 99.47; 99.43; 99.43 | held |
| New Mountain (5 funds) | 03/2032 | 2026-09-30 | 98.25–98.27 | held |
| KKR Enhanced US Direct Lending Fund-L | 3/5/2032 | 2026-06-30 | not computed (layout parsed as `possible_unfunded_commitment`; TL $30,474k par / $29,776k FV in `row_cells_raw`) | held |

AB PLF's 2027 last mark moved from 2024-06-30 to 2024-12-31, a further correction found by the walk-back.

### 2.4 Limitations

- **Merged BDCs.** `status` for Golub BDC 3 and BlackRock Capital Investment still reads `held_at_lender_latest_period`, because their last schedules predate their 2024 mergers.
- **Parsing gaps.** KKR Enhanced US Direct Lending Fund-L's columns are not parsed, and the KKR FS Income Trust maturity is still not parsed. Use `row_cells_raw` for these rows.
- **Search coverage.** Name search finds only filings whose text names the borrower. Registered funds (811-) are out of scope (P-BMG-01).
- **Walk-back stop rule.** The walk-back stops on facility keys (lender, company group, maturity month). An amended maturity creates a new key, and walking continues until that older key's own-period row is found.

---

## 3. P-CFV-03: dating the CF ledger and portal switches

### 3.1 Method

`python3 scripts/mission_cf_migrations_goodstack.py --cache-dir <dir> --fetch --task migrations` fetches 29 public sources (all cached; an offline rerun is byte-identical). It applies one stated rule to each source:

| Rule | Value recorded |
|---|---|
| WordPress REST API (`/wp-json/wp/v2/...`) | `date` / `modified` |
| JSON-LD | `datePublished` |
| Webflow comment | "Last Published" date |
| PDF | `/CreationDate`; text via `pdftotext` |
| crt.sh | certificate `not_before` range |
| dns.google | status (NOERROR / NXDOMAIN) |
| Page text | HTTP status and a regex snippet |

The script adds every 990 Part VII-B vendor line (Stellar, Foundant, akoya, Blackbaud, NPact), TY2021+, from [`form990-contractors-harvest-full.csv`](../../data/mission-2026-11-14/form990-contractors-harvest-full.csv). Where no source states a year, the event date comes from a coded inference rule:
- **Acadiana:** a weekday check.
- **Winston-Salem:** the first Foundant 990 line.
- **Tampa Bay:** a pending-transition notice.

Each such date is tagged [I] in `date_basis`.

Two sources were not available:
- **Wayback Machine:** the connection was reset.
- **Acadiana's `/upgrade` page:** now HTTP 404. Its dates come from a search-engine index of that page. They are marked as such and not treated as [F].

### 3.2 Results (event rows)

| CF (FY2024 DAF assets) | Map signal | Move | Date | Basis | Confidence |
|---|---|---|---|---|---|
| Arkansas CF ($350m) | Stellar 990 payee, Foundant portal | Ren iPhi → Foundant CommunitySuite | **2026-06-01** | [Post](https://www.arcf.org/blog/arkansas-community-foundation-announces-database-transition/) (WP date 2026-04-20, modified 2026-08-13): "has transitioned to a new database … instructions … were emailed on June 1". [User guide PDF](https://www.arcf.org/app/uploads/2026/06/Fundholder-Portal-How-to-Guide3.pdf) created 2026-06-01, invitations from "no-reply@fcsuite.com" [F]. Legacy [arcf.iphiview.com](https://arcf.iphiview.com/arcf/) login page still answers (footer © 2021) | high |
| CF of Acadiana ($145m) | Stellar 990 payee, Foundant portal | Ren iPhi → Foundant CSuite | **2025-05-14** [I] | The indexed `/upgrade` page gives blackout March 19–April 6, login e-mails "May 5–May 9" and portal live "May 14", with no year. Of 2022–2027, May 5–9 runs Monday–Friday only in **2025** [S]. The [Donors page](https://www.cfacadiana.org/who-we-help/donors/) with "Donor Portal" was created 2025-04-09 (WP API). `cfacadiana.iphiview.com` is NXDOMAIN. Stellar was paid $118,458 in TY2024, the last full iPhi year | medium |
| CF of Greater Flint ($29m) | Stellar 990 payee, Foundant portal | Ren iPhi → Foundant | **about 2026-01** [I] | The [login page](https://www.cfgf.org/who-we-are/login) linking the fcsuite Donor Portal has JSON-LD datePublished 2026-01-20. The [2026 grant FAQ](https://stdidcfgfprod.blob.core.windows.net/cfgf/documents/CFGF_FAQ_2026.pdf) (created 2026-02-25) says "CFGF has transitioned to a new grant application portal". [cfgf.iphiview.com](https://cfgf.iphiview.com/cfgf/) still live: "we are moving to a new system. Gifts … may not appear in the donor portal". Stellar $114,605 in TY2022; not listed TY2023–24 | low-medium |
| CF Tampa Bay ($590m) | Dual fund login (fcsuite + spectrumportal) | Blackbaud Raiser's Edge + Foundation Cloud portal → Foundant | **summer 2026** [I] | [Portal guide](https://www.cftampabay.org/portal-guide): "transition from our current system, Raiser's Edge, to a new platform powered by Foundant"; old portal "through June 15"; new Fund Advisor Portal "late July"; later "This summer, we have transitioned". The year is inferred: on 2026-11-14 [online gifts](https://www.cftampabay.org/give-now/cftb-funds) are still "temporarily unavailable during our transition", `cftampabay.spectrumportal.net` returns "Not Found", and the FYE-June-2025 990 has no Foundant payee. The homepage still carries both "Fundholder Login" buttons | medium-low |
| Winston-Salem Foundation ($357m) | Dual fund login (spectrumportal + fcsuite) | Blackbaud + Foundation Cloud portal → Foundant | **2024-09-30** [I] | [/portal](https://www.wsfoundation.org/portal): "This summer we migrated from Blackbaud to Foundant"; current Fund Portal closed "August 21"; "September 30: New Fund Portal launched". No year is stated; it is set by the first Foundant 990 line, TY2024 (calendar 2024), Foundant Technologies $187,344 [F]. The homepage "Fundholders Login" still points to `wsfoundation.spectrumportal.net` ("Foundation Cloud Community Portal", which loads Blackbaud's bbCheckout) | medium |
| New Mexico CF ($5m) | Dual fund login (spectrumportal + fcsuite) | **None. Misclassified** | n/a | spectrumportal is a partner portal: the [NMRRF Login](https://nmcf.org/nmrrf/) page (created 2026-06-05) is for "pre-approved agency partners to apply for New Mexico Rapid Response Funding", and the [Login](https://nmcf.org/login/) page (created 2026-05-14) is a partner login. fcsuite appears only as `newmexicocf.fcsuite.com/erp/donate/list`. No fundholder login on the site | high (reclassification) |
| Indian River CF ($72m) | Dual fund login (donor-portal.org + fcsuite) | donor-portal.org white-label → Foundant "My Fund" | **2023-07-31** | ["My Fund has been Upgraded!"](https://ircommunityfoundation.org/my-fund-has-been-upgraded/) created 2023-07-31 (WP API), "Go to My Fund" → `indianriver.fcsuite.com/erp/portal`. [User guide](https://ircommunityfoundation.org/wp-content/uploads/2025/03/RESOURCE-My-Fund-User-Guide-1.pdf) re-issued 2025-03-18. `ircf.donor-portal.org` had named certificates 2021-02-08 to 2022-01-04 ([crt.sh](https://crt.sh/?q=ircf.donor-portal.org); unverified lead). `donor-portal.org` has a DNS wildcard, so DNS cannot confirm the tenant [crt19]. The header "My Fund: Login" to donor-portal.org is a leftover link | high |
| Yakima Valley CF ($18m) | Dual login (akoyaGO + iPhi) | Ren iPhi → akoyaGO | not established | The homepage "Donor Login" goes to `gofund.akoyago.com/yakimavalleycf`. The iPhi "Give Now" link points to `yvcf.iphiview.com`, which is NXDOMAIN on 2026-11-14. No vendor payee in TY2022–24 990s | none (date) |

### 3.3 Reading [I]

- **Direction.** All six dated or datable moves end on Foundant (Arkansas, Acadiana, Flint, Tampa Bay, Winston-Salem, Indian River). The seventh (Yakima) ends on akoyaGO. None ends on Ren iPhi or on Foundation Cloud.
- **Ren iPhi attrition.**
  - **Exits:** among the 8 flagged CFs, 4 iPhi tenants left in 2025–2026, at least three of them in the 13 months from May 2025.
  - **Last 990 lines:** Stellar's last lines at the three Foundant switchers were $100–124k a year.
  - **Arkansas:** the CF still ran iPhi until June 2026, so the absence of Stellar from its TY2023–24 lists means fees under the $100k listing threshold, not an earlier exit.
  - **How to measure attrition across the map:** a DNS/live sweep of `*.iphiview.com` tenants plus TY2025 990s (P-BMG-03).
- **Foundation Cloud.**
  - **These are not wins.** At Tampa Bay and Winston-Salem, the spectrumportal "Fundholder Login" is the outgoing portal that fronted a Blackbaud ledger. At New Mexico it is grants-side. So these three are not Foundation Cloud wins, and `ledger_implied = yes` for spectrumportal is wrong at least for Tampa Bay and Winston-Salem (P-BMG-02).
  - **Map correction.** The CF vendor map should show Tampa Bay and Winston-Salem as Foundant (portal) on a former Blackbaud ledger, and New Mexico as Foundant (donations) with Foundation Cloud (partner grants).
- **Stale links.** Old portal links stay on CF sites for months to years after a switch: Indian River's for 3 years, Winston-Salem's for 2 years, and Arkansas and Flint still have iPhi pages live. Link-based vendor maps therefore overstate legacy vendors unless the link target is checked.

### 3.4 Limitations

- **Missing history.** No Wayback history was available, and Acadiana's announcement survives only as a search-index copy.
- **Inferred years.** Three dates rest on stated inference rules: Acadiana (weekday), Winston-Salem (990 year) and Tampa Bay (pending-transition notice).
- **990 listing threshold.** 990 Part VII-B lists only the five highest-paid contractors above $100k, so absence is weak evidence.
- **Point in time.** All pages were read on 2026-11-14.

---

## 4. P-FCG-02: Goodstack Impact Foundation US (Percent Impact Foundation, EIN 87-3165286)

### 4.1 Method

`--task goodstack` parses three e-filed returns from the IRS e-file mirror with ElementTree:
- [FY2023](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202411459349301006_public.xml), filed 2024-05-23;
- [FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202522489349301512_public.xml), filed 2025-09-04;
- [FY2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202602459349300235_public.xml), filed 2026-09-02, prepared by CliftonLarsonAllen.

It reads Part I, Part IX lines, Part X, Schedule A, Schedule D, Schedule F, Schedule I and Schedule O. The IRS index has no later return.

### 4.2 Results [F]

| | FY2023 | FY2024 | FY2025 |
|---|---|---|---|
| Contributions | $268,231 | $3,116,428 | $16,343,906 |
| Grants paid (domestic / foreign) | $228,688 ($111,346 / $117,342) | $1,739,654 ($1,529,638 / $210,016) | $6,942,359 ($6,785,051 / $157,308) |
| Total expenses | $243,744 | $1,792,402 | $7,124,781 |
| Non-grant expenses | $15,056 | $52,748 | $182,422 (accounting $38,725, other fees $66,741, office $58,116) |
| Cash, year-end | $27,833 | $1,812,959 | $12,625,525 |
| Grants payable, year-end | n/a | $634,300 | $2,026,604 |
| Net assets, year-end | $26,045 | $1,350,071 | $10,569,322 |
| Schedule D: DAFs held | (no Schedule D) | **7,268** | **3** |
| Schedule D: contributions / grants / year-end value | n/a | $2,945,016 / $1,210,123 / $1,812,959 | **$11,582,483 / $1,660,000 / $10,772,483** |
| Schedule A: substantial contributors (5-year) / total support | $8,969 / $268,231 | $1,671,229 / $3,384,659 | **$13,015,738 / $19,728,691** |
| Schedule I: US grantees > $5k / total | 4 / $83,350 | 26 / $385,699 | 54 / $2,078,401 |
| Largest Schedule I grants | Dibs for Kids $38,825 | American Heart Association $102,279 | Chicago Urban League, Latino Policy Forum, Untours Foundation $200,000 each; Global Glimpse $150,000; four San Diego organisations $100,000 each |
| Schedule F regions | South Asia | South Asia | Europe $99,575; South Asia $57,733 |
| Employees / contractors > $100k | 0 / none | 0 / none | 0 / none |
| Officers | 3 at 0.01 h/week | 4 at 0.01 h/week | Halkias (president) and Nagoski (treasurer) at 1 h/week; Orrick 0.5 h/week |

**Schedule O FY2023 (Part VI line 3)** [F]: "the Foundation has engaged Percent, a company registered in England and Wales, to perform platform and non-platform services … nonprofit validation and vetting … accounting, charity onboarding, operations, customer service". FY2024 and FY2025 drop this sentence. FY2025 says the 990 is completed "within a week of the audited reports' sign-off".

**Related public pages** [F]:
- The foundation's [US page](https://www.giftall.org/united-states) calls it "Goodstack Impact Foundation US (previously known as Percent Impact Foundation)" and says "since the start of 2023, we've donated over $8.7 million". The three returns' grants total $8.91m.
- The [FAQ](https://www.giftall.org/) explains card charges from "Goodstack Impact Foundation" as Adyen Giving round-ups ("used by retailers including UNIQLO and Hungry Jack's"). It says donations are "consolidated and distributed as a single aggregated payment … at least once a month".
- The [Undeliverable Donation Policy](https://goodstack.org/legal/undeliverable-donation-policy) (effective 2024-11-15) works in three steps:
  1. The foundation "reserves the right to reassign funds to another Charity" if the recommended charity fails due diligence, closes or "does not onboard with Goodstack".
  2. It then asks the donor to choose again "if possible".
  3. Otherwise it chooses "a similar Charity" or one "with a wide-ranging charitable mission". The donor's tax status is unchanged.

### 4.3 Explaining the FY2025 change [I]

- **Two flows, not one.**
  - **DAF flow:** Schedule D now covers $11.58m of contributions, 71% of total contributions, but only $1.66m of grants.
  - **Non-DAF flow:** about $4.76m of contributions passed through to $5.28m of grants. These are aggregated, recommended-charity gifts such as checkout round-ups and workplace giving.
  - **FY2024 by contrast:** almost all flow was reported as DAF (7,268 accounts), which is what you would expect if every donor or platform user balance was counted as a fund.
- **Three large funds.** The FY2025 count of 3 with $10.77m year-end value, together with $13.0m from substantial contributors, fits a few large corporate or major-donor advised funds opened in 2025. The $100k–200k Chicago and San Diego grants look like advised grants from such funds.
- **What would confirm it:** the audited FY2025 statements or the Schedule B donor names, which are restricted in the public XML (P-BMG-04).
- **Sponsor universe.** The foundation passes the DAF-sponsor test (Schedule D Part I, 3 DAFs, $10.8m). It belongs in the non-DAFRC sponsor list and graph as a vendor-routed sponsor, linked to Goodstack (We Are Percent Ltd) as technology and service provider. The governing wave-7 wording stands: the foundations "operate independently and are not subsidiaries or affiliates".
- **Scale.** At $10.8m it is under 0.01% of US DAF assets. Its importance is the operating model, not its size: corporate checkout donations land in a 501(c)(3) with undeliverable-donation reassignment rules. Its growth is +424% in contributions year on year.

---

## 5. Queue proposals ([`queue-proposals-bdc-migrations.csv`](../../data/mission-2026-11-14/queue-proposals-bdc-migrations.csv))

| ID | Question |
|---|---|
| P-BMG-01 | Registered-fund (N-PORT/N-CSR) holders of DAF-vendor loans, e.g. KKR US Direct Lending Fund-U for Bonterra |
| P-BMG-02 | Audit spectrumportal.net (Foundation Cloud) tenants: ledger behind, live versus stale link, grants-only |
| P-BMG-03 | Measure Ren iPhi CF attrition 2023–2026 by DNS sweep, TY2025 990s and notices |
| P-BMG-04 | Goodstack US FY2025: what the 3 DAFs are; sponsor-universe entry |

---

## 6. Data dictionary

### 6.1 `bdc-loans-daf-ecosystem.csv` and `bdc-loans-latest-marks.csv`

The columns are as documented in [queue-bdc-fix-labour-benevity.md](queue-bdc-fix-labour-benevity.md) §2.1 and the script's `FIELDS`/`LATEST_FIELDS`. Changes:

| Column | Change |
|---|---|
| `which_filing` | Adds `walkback`: a filing read between latest and earliest because a facility lacked an own-period row |
| `row_type` | Adds `undrawn_commitment`: an instrument labelled Undrawn/Unfunded. It is excluded from `facility_debt_par`/`facility_fv_pct_of_par` but kept in the latest-marks table |
| `lender_latest_schedule_period` | Now the latest filing period among **all filings read** for (lender, company group), computed before deduplication |
| `row_type = no_bdc_hit` | Now also written for the new phrases (Foundant Technologies, RenPhil, Benevity Inc, Momentive Software). "None from an 814- filer" means none from any CIK that has an 814- filing |

### 6.2 `cf-vendor-migrations-2022-2026.csv`

| Column | Meaning |
|---|---|
| `record_type` | `event` (one row per CF) or `evidence` (one row per fetched source or 990 line) |
| `ein`, `cf_name` | CF EIN (9 digits) and short name |
| `fy2024_daf_assets_usd` | From `cf-vendor-map-by-ein.csv` (DAFRC FY2024) |
| `map_signal` | Why the CF vendor map flagged it: `stellar_990_payee_foundant_portal` or `dual_live_fund_login` |
| `evidence_id` | Evidence key. `AR-`, `AC-`, `FL-`, `TB-`, `WS-`, `NM-`, `IR-` and `YV-` are page and API sources; `990-<ein>-TY<yyyy>` is a 990 vendor line; a `-none` suffix means a harvested return with no vendor line |
| `evidence_kind` | `announcement`, `announcement_removed`, `donor_notice`, `donor_notice_pdf`, `portal_page`, `legacy_portal_live`, `legacy_portal_dns`, `crt_sh` or `990_part_vii_b` |
| `url` | Source fetched (for 990 lines, the ProPublica filing page or XML) |
| `http_status` | HTTP status when fetched on 2026-11-14 (0 = transport failure) |
| `value` | Extracted dated fields, e.g. `wp_date=…; wp_modified=…`, `date_published=…`, `webflow_last_published=…`, `pdf_created=…`, `ct_first_not_before=…`, `dns_status=NXDOMAIN`; for 990 rows, the tax year and period end |
| `snippet` | Regex match from the page or PDF text (up to 4 matches of 240 characters), or the 990 contractor line |
| `from_system`, `to_system`, `direction` | Event rows: outgoing and incoming ledger/portal, and the reading ([I] where inferred) |
| `event_date` | Event rows: date copied from the named evidence row or set by the stated inference rule. For New Mexico CF it is the creation date of the partner-portal page, not a migration date |
| `date_basis` | How the date was obtained, with [I] marking inference |
| `date_confidence` | high, medium, medium-low, low-medium or none |
| `implication` | Effect on the Ren iPhi / Foundation Cloud reading |
| `evidence_ids` | Event rows: all evidence rows for the CF |
| `retrieved` | 2026-11-14 |

### 6.3 `queue-proposals-bdc-migrations.csv`

The format is in [queue-proposals-README.md](../../data/mission-2026-11-14/queue-proposals-README.md).

## Validation corrections (wave 10, 2026-11-15) — governing
Source: [validation-wave10-report.md](validation-wave10-report.md). Where these conflict with the text above, these govern.

- **§1 finding 2 (line 34).** Replace "**With these funds, 13 BDCs hold the 2032 facility at 98.25–99.5% of par.** New Mountain marks lowest, FS KKR highest (99.47%)." with: "**With these funds, 13 BDCs hold the 2032 facility at 97.7–99.5% of par.** At 2026-09-30, New Mountain marks lowest of the parsed lenders and FS KKR highest (99.47%). KKR Enhanced US Direct Lending Fund-L's latest schedule (2026-06-30, columns 'Par/Shares | Fair Value') marks the term loan at 29,776/30,474 = 97.71%."
- **Latest-marks table (line 122), KKR Enhanced row.** Replace "not computed (layout parsed as `possible_unfunded_commitment`; TL $30,474k par / $29,776k FV in `row_cells_raw`)" with "97.71 (TL 30,474 par / 29,776 FV; DDTL 03/25 3,319 / 3,243; revolver and DDTL 10/25 partly unfunded, footnote (c)); parser still types the rows `possible_unfunded_commitment`".
- **§3.1 inference list (line 153).** Replace "- **Winston-Salem:** the first Foundant 990 line." with "- **Winston-Salem:** none needed; the /portal page states 'As of July 15, 2024' (the 990 line corroborates)."
- **§3.2 Winston-Salem row (line 170).** Replace "**2024-09-30** [I]" with "**2024-09-30** [F]". Replace "No year is stated; it is set by the first Foundant 990 line" with "The same page states 'As of July 15, 2024, everyone will need to complete the registration process' for the Grants Portal, which fixes the year; corroborated by the first Foundant 990 line". Change the confidence from medium to high.
- **§3.2 Arkansas row.** After "were emailed on June 1", add: "(the instruction-email date, used as the event date; no go-live date is stated)".
- **§3.4 (line 191).** Replace "Three dates rest on stated inference rules: Acadiana (weekday), Winston-Salem (990 year) and Tampa Bay (pending-transition notice)." with "Two dates rest on stated inference rules: Acadiana (weekday) and Tampa Bay (pending-transition notice). Flint's date is a CMS page date only."
- **§4 heading and any summary that uses "affiliated".** Keep "Goodstack Impact Foundation US (Percent Impact Foundation, EIN 87-3165286)". Wherever a summary calls it "Goodstack-affiliated", replace that with "Goodstack-linked (service-provider relationship; not a subsidiary or affiliate)".

## Compliance note (2026-11-15) — governing
crt.sh disallows all crawlers in its robots.txt. Any claim in this document that rests **only** on crt.sh certificate data is downgraded to an unverified lead until re-sourced. See [compliance-note-crtsh-robots.md](compliance-note-crtsh-robots.md).
