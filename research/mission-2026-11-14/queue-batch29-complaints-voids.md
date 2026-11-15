# Batch 29 (C): complaint rates per 10,000 accounts (P-QA3-04), void/refund scan of the top 200 sponsors (P-B28-02), ImpactAssets' $160.8m grant to NPT (P-WAT-02)

**Research date:** 2026-11-15. **Recency rule:** 2021 onward (complaints dated 2021+; returns for TY2021–2024).
**Method:** public sources only. No accounts were created and no one was contacted.

**Files written**
- Scripts: `scripts/mission_complaint_rates.py`, `scripts/mission_void_scan.py`. Both are stdlib-only and written in a functional style. The void scan imports the IRS-index and XML helpers from `scripts/mission_990_contractors.py`.
- Data:
  - `data/mission-2026-11-14/complaint-rates-normalised.csv` (17 rows);
  - `data/mission-2026-11-14/daf-grant-voids-top200.csv` (837 rows);
  - `data/mission-2026-11-14/daf-grant-voids-top200-summary.csv` (8 rows);
  - `data/mission-2026-11-14/queue-proposals-batch29c.csv` (3 proposals).

**Read first:**
- `queue-batch28-ledgers-voids-cf-apps.md` §3, with the wave-13 corrections in `validation-wave13-report.md` (Fidelity TY2021 = $16,130,006, 0.141%);
- `daf-user-complaints-deep-research.md` §3 and §9, with the wave-4 corrections;
- `daf-grant-voids-disclosures.csv` (40 rows).

Evidence labels:
- **[F]** a filed or first-party figure;
- **[C]** computed here from [F];
- **[I]** inference.

---

## 1. Summary

| Item | Answer | Confidence |
|---|---|---|
| **P-QA3-04** | **A per-account complaint rate can be computed, but it measures where the corpus looked, not how sponsors perform.** 123 complaint or mixed records dated 2021 or later are in scope; 75 of them name an A3/A4 sponsor. Per 10,000 FY2024 accounts (2021–26 window, not annualised) [C]: **Daffy 11.2** (10.1 without App Store records); **Vanguard Charitable 5.4**; **Fidelity Charitable 2.3** (**1.1** without its 24 App Store reviews); **DAFgiving360 1.3**. GS DAPF's 2.4 rests on a single record. Charityvest and MS GIFT each have one record. **NPT, RCF, AEF, GiveClear, NCF, BofA, Endaoment, Givinga and Every.org have zero records**, so they have no rate. On high-plus-critical severity, the order is reversed: Vanguard 2.9, Fidelity 1.0 (0.5 without App Store), DAFgiving360 0.8, Daffy 0. Most of the big three's high-severity weight comes from the six shared 2026 SPLC records (CMP-215–220). Pooled over the 7 sponsors with records: **1.9 per 10k (1.3 without App Store)**. CFPB re-check: **no DAF sponsor is a CFPB "company"**. Sponsor-name queries for 2021+ return only the brokerage, bank and other unrelated firms (§2.4) | High on the arithmetic. **Low as a performance measure**: the venue bias is stated in §2.5 |
| **P-B28-02** | **The scan covered the top 200 sponsors by corrected FY2024 DAF assets: 798 TY2021–24 Form 990s located, 785 parsed.** **29 sponsors (14.5%) itemise at least one grant void, refund, rescission or reversal with a figure**, in 72 of 785 returns (9.2%). Those 29 hold **37.5%** of scanned top-200 DAF assets. Excluding accrual "reversal of grant expense" items, the count is 26 (13.0%). **By type:** nationals 9 of 43 (20.9%), community foundations 17 of 113 (15.0%), single-issue charities 3 of 44 (6.8%). **Void share** (|items| ÷ Part I line 13 grants), per disclosing return: median **0.30%**, IQR 0.13–1.05%. Excluding accrual reversals: median 0.27%, IQR 0.13–0.75%, max 4.6% (CCF TY2023). **Nationals:** median 0.15% (IQR 0.06–0.40%). **Community foundations:** median 0.28–0.29%, IQR to about 0.8–0.9%. The scan reproduces all 8 of batch 28's itemising sponsors and adds 21. New examples: **ImpactAssets "RETURNED GRANT FUNDS" $7.44m (TY2022, 3.3%)**, Rockefeller Philanthropy Advisors $1.8–4.5m a year, Goldman Sachs Charitable Gift Fund $55k/$85k, BofA $125k, and Seattle, Cleveland, Denver, Greater Washington, Baltimore, Santa Barbara and Princeton | High on filed figures; medium on comparability (labels differ) |
| **P-WAT-02** | **The $160,826,426 is a single ImpactAssets Schedule I line to NPT (EIN 23-7825575), purpose "GENERAL SUPPORT"** [F]. ImpactAssets uses that purpose text for nearly every grant, so it says nothing. **Best reading [I]:** a donor-recommended DAF-to-DAF transfer, by one or a few large ImpactAssets accounts, into NPT donor-advised funds. It is not a grant for NPT's own operations, and not a program migration. **Why:** (a) ImpactAssets' DAF count *rose* 2,083 → 2,197 in CY2024; (b) **money flows the other way too**: NPT granted ImpactAssets **$22.86m (FY2024)** and **$40.64m (FY2025)** [F]; (c) ImpactAssets granted NPT in CY2021–23 as well ($3.10m, $0.80m and $1.20m, partly "FBO Friends of UBS Optimus Foundation") [F]. **That corrects the watchlist's "neither appears in CY2023"**, though those were small, earmarked grants. UBS distributes both sponsors (a 2025-02 UBS factsheet lists "Impact Assets"; the current UBS DAF page names only NPT, Fidelity and RCF), so a **UBS-channel consolidation is possible but unproven** [I]. **Recurrence in CY2025 cannot be tested:** ImpactAssets' CY2025 990 is not in the IRS index (latest period 202412) | High on the filed line; low on the purpose |

---

## 2. P-QA3-04: complaints per 10,000 accounts

### 2.1 Method

- **Numerator.** Rows of `daf-user-complaints-corpus.csv` that meet three conditions:
  - `valence` is `complaint` or `mixed`;
  - the first four-digit year in `date` is 2021 or later. So `c.2021` is in, while `c.2015-2021`, `c.2018-2022` and undated rows are out. That leaves 123 of the 165 complaint or mixed rows;
  - each row is counted by `severity` (low, medium, high, critical).
- **Attribution.** A record counts once for each named A3/A4 sponsor, using a regex on `organization`.
  - Generic rows are attributed to nobody: "DAF sponsors (generic)", "Multiple sponsors" and "Commercial sponsors (generic)".
  - CMP-220's "big three" is read as Fidelity Charitable, Vanguard Charitable and DAFgiving360. These are the sponsors named in CMP-215–219 for the same 2026 SPLC holds.
  - 8 records are shared across sponsors, so per-sponsor counts sum to more than the pooled count.
- **Sponsors.** The union of A3 (12) and A4 (7) in `quadrant-A3-A4-rationale.md` §1, which gives 16 entities.
- **Denominator.** DAFRC FY2024 `number_of_daf_accounts` ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)), with the R1 "filed replaces imputed" corrections in `dafrc-corrections-itemized.csv` applied (the corrected-totals pipeline).
  - Corrections change the figures for Daffy (4,869 → 8,905), Endaoment (425 → 6,000), RCF, MS GIFT, BofA, AEF, GS DAPF, NCF and GiveClear.
  - Every.org has no DAFRC row.
  - Givinga's 1,421,011 "accounts" are workplace-giving accounts, not comparable DAFs.
- **Rate.** Records ÷ accounts × 10,000, over the whole 2021–26 window, not annualised. Each rate is computed with and without `venue_type = app_store`.
- **Zero counts.** A zero count gives a blank rate, not 0, because absence from a convenience sample is not evidence of no complaints.

### 2.2 Results (`complaint-rates-normalised.csv`)

| Sponsor (area) | FY2024 accounts (corrected) | Records L/M/H/C | All venues per 10k | High+critical per 10k | Without App Store per 10k | High+critical w/o App Store | App Store records |
|---|---|---|---|---|---|---|---|
| Daffy (A4) | 8,905 | 7/3/0/0 = 10 | **11.230** | — | 10.107 | — | 1 |
| Vanguard Charitable (A3) | 27,660 | 3/4/8/0 = 15 | **5.423** | **2.892** | 5.423 | 2.892 | 0 |
| GS DAPF (A3) | 4,134 | 0/0/1/0 = 1 | 2.419 | 2.419 | 2.419 | 2.419 | 0 |
| Fidelity Charitable (A3/A4) | 204,614 | 11/15/20/1 = 47 | **2.297** | 1.026 | **1.124** | 0.489 | **24** |
| DAFgiving360 (A3/A4) | 112,188 | 2/4/9/0 = 15 | 1.337 | 0.802 | 1.337 | 0.802 | 0 |
| Charityvest (A3/A4) | 18,427 | 1/0/0/0 = 1 | 0.543 | — | 0.543 | — | 0 |
| Morgan Stanley GIFT (A3) | 21,800 | 1/0/0/0 = 1 | 0.459 | — | 0.459 | — | 0 |
| NPT, RCF, AEF, GiveClear, NCF, BofA (A3); Endaoment, Givinga, Every.org (A4) | 17,940; 25,824; 15,947; 228; 31,943; 17,840; 6,000; 1,421,011; n/a | 0 | blank | blank | blank | blank | 0 |
| **Pooled** (7 sponsors with records; each record once) | 397,728 | 24/26/24/1 = 75 | **1.886** | 0.629 | **1.257** | 0.352 | 25 |

Fidelity's FY2024 count of 204,614 matches its filed FYE 2024-06 Schedule D ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202521349349310887_public.xml)) [F].

### 2.3 Reading

- **Excluding App Store records halves Fidelity's rate (2.30 → 1.12) and leaves everyone else nearly unchanged.**
  - Of Fidelity's 47 records, 24 are 2021+ iOS reviews. The corpus scanned only the Fidelity, Daffy, DAFpay, Groundswell, Donors Fund and Benevity apps (corpus §3).
  - DAFgiving360 and Vanguard have no App Store records because none were sampled, not because they are free of complaints.
- **The challenger's high rate reflects its venues.**
  - Daffy's 10 records are 7 low and 3 medium.
  - 7 of them are a single Bogleheads thread cluster (c.2024), and 1 is Trustpilot.
  - A small, online-native user base that writes on forums produces more records per account than an adviser-channel sponsor whose donors rarely post.
- **The high-severity order is driven by one 2026 event.**
  - CMP-215–220, the SPLC holds, are six high-severity records shared by Fidelity, Vanguard and DAFgiving360.
  - Because Vanguard has the smallest account base of the three, the same records give it the highest high-severity rate (2.9).
- **The zero rows are uninformative.** Adviser-channel sponsors (NPT, RCF, AEF, NCF, BofA) have no consumer app, no Trustpilot profile and almost no forum presence (corpus §3). Their donors complain, if at all, to their adviser.

### 2.4 CFPB and BBB (sampling-frame check)

- **CFPB.** The CFPB public API ([endpoint](https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/)) was queried on 2026-11-15 with `search_term=<name>&date_received_min=2021-01-01`.
  - **Companies matched:**
    - "Schwab": only "CHARLES SCHWAB CORPORATION, THE" (1,124);
    - "Vanguard": "Vanguard Financial Services, Inc." (26);
    - "Morgan Stanley": "MORGAN STANLEY & CO. LLC" (981);
    - "Goldman": "GOLDMAN SACHS BANK USA" (21,172);
    - "Bank of America": the bank (93,764);
    - "Fidelity": FNIS and other unrelated "Fidelity" firms (19,587).
  - **Zero hits** for Daffy, Charityvest, Endaoment, Givinga, Every.org, GiveClear, "National Philanthropic", "Renaissance", "American Endowment" and "National Christian".
  - The `field=complaint_what_happened` parameter is now rejected ("not a valid choice"). `field=all` returns 0 for "charity". **Narratives therefore cannot be searched through the public API**, so the corpus's "inconclusive" verdict stands.
  - **Structural point [I]:** DAF sponsors are charities, not CFPB-covered financial-product providers. Any DAF complaint filed with the CFPB would sit under the affiliated broker or bank, with no field that separates it out.
- **BBB.** BBB has no sponsor profiles (corpus §3, [search](https://www.bbb.org/search?find_country=USA&find_text=Fidelity%20Charitable)).
- **Trustpilot.** The Fidelity, Vanguard, Schwab, Every.org and Endaoment pages return 404.
- **Conclusion:** no public venue offers a sponsor-level sampling frame with denominators.

### 2.5 Venue bias (stated plainly)

1. **Selection by venue access.** Reddit was blocked, and Bogleheads could be read only through search extraction. App Store coverage depends on whether a sponsor has an app and whether the corpus sampled it. Trustpilot profiles exist only for Daffy, Charityvest (0 reviews) and Benevity.
2. **Channel bias.** Consumer and challenger sponsors face donors directly online. Adviser-channel sponsors' end clients route complaints through advisers, and those complaints never reach public venues.
3. **Event clustering.** A single 2026 controversy supplies most of the high-severity records for three sponsors.
4. **Denominator mismatch.** Accounts are a FY2024 stock. Complaints are a 2021–26 flow. Givinga's accounts are workplace accounts.
5. **Therefore** the rates are fit only to describe this corpus. They must not be used to rank sponsors' service quality, and X6 should stay capped as the A3/A4 rationale specifies.

---

## 3. P-B28-02: void/refund/rescission scan, top 200 sponsors, TY2021–2024

### 3.1 Method

- **Universe.** The 200 largest DAFRC FY2024 sponsors by `eoy_daf_assets`, with R1 corrections applied: 43 national, 113 community foundation, 44 single-issue charity.
- **Returns.** For each sponsor, every Form 990 in the IRS e-file index ([index_2021–2026.csv](https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv)) whose tax year is 2021–2024.
  - Tax year = the year the 12-month period starts.
  - The newest object id per period is used, so an amended return supersedes the original.
  - This yields 798 returns, of which 785 were parsed. The other 13 are TY2024 returns filed in 2026 that the [GivingTuesday mirror](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601389349301700_public.xml) does not yet hold (HTTP 404).
  - Ayco's 202506 return is a short-period return, which the period rule labels TY2024.
  - 217 returns were read from batch 28's local copies; 581 were fetched (4 workers).
- **What is read.**
  - Every `SupplementalInformationDetail` in any schedule. These carry the Schedule O explanations of Part XI line 9 and Part XII, and the Schedule D Part XIII reconciliation text.
  - Part I line 13 `CYGrantsAndSimilarPaidAmt`, used as the denominator.
  - Part XI line 9 total and Schedule D Part I DAF grants, for context.
  - The whole XML is streamed; Schedule I tables are discarded.
- **Hit rule.**
  - A hit is any of: void(ed); grant/scholarship refund; returned grant(s); return of (prior-year) grants; grant cancellation(s); rescind/rescission; reversal of grant (expense); uncashed; escheat; outstanding/stale-dated check.
  - The amount comes from the same line item. Two filed layouts are recognised: "$ AMOUNT - LABEL" (Fidelity) and "LABEL [-] AMOUNT" (everyone else).
  - IRS redaction (`XXX-XX-XXXX`) is reported as `REDACTED`.
- **Review.** All 128 hits were reviewed against the filed text. 19 are policy or description text with no figure (East Bay's conflict-of-interest "voided" transactions; St Louis, Maine and other Schedule I "rescind" policies). They are kept and flagged `no (descriptive or policy text; no figure)`.
- **Item class.** Each label is coded into one of four classes:
  - voided grant or uncashed check;
  - refunded/returned grant;
  - rescinded/cancelled grant;
  - reversal of grant expense (accrual).
  The last class records a cancelled *commitment*, not money returned, so the summary is also run without it.
- **Void share.** The sum of distinct |amounts| of grant-related items in a return ÷ Part I grants. Items come from Schedule O where present, otherwise from Schedule D, so an item shown in both places counts once.
  - Pittsburgh TY2024 is the one return where Schedule D (737,230) and Schedule O (162,141) give different "refund" figures. Only Schedule O is used.

### 3.2 Disclosure rate (`daf-grant-voids-top200-summary.csv`)

| Group | Sponsors scanned | Disclosing sponsors | Rate | Returns disclosing / scanned | Share of group DAF assets held by disclosers | Void share per disclosing return: median (IQR; max) |
|---|---|---|---|---|---|---|
| All | 200 | 29 | **14.5%** | 72 / 785 (9.2%) | 37.5% | **0.30%** (0.13–1.05%; 26.5%) |
| National | 43 | 9 | 20.9% | 16 / 172 | 41.6% | **0.15%** (0.06–0.40%; 3.3%) |
| Community foundation | 113 | 17 | 15.0% | 49 / 444 | 31.8% | 0.29% (0.16–0.88%; 26.5%) |
| Single-issue charity | 44 | 3 | 6.8% | 7 / 169 | 8.0% | 1.48% (0.86–1.93%; 18.7%) |
| *Excl. accrual reversals*: all | 200 | 26 | 13.0% | 66 / 785 | 37.4% | 0.27% (0.13–0.75%; **4.6%**) |
| *Excl. accrual reversals*: CF | 113 | 15 | 13.3% | 47 / 444 | 31.5% | 0.28% (0.15–0.80%; 4.6%) |
| *Excl. accrual reversals*: single-issue | 44 | 2 | 4.5% | 3 / 169 | 7.5% | 0.39% (0.20–0.93%; 1.5%) |

The two maxima come from accrual reversals, not voids:
- **26.5%:** Tahoe Community Foundation TY2022, "Reversal of Grant Expenses" $2,915,146 on $11.0m of grants;
- **18.7%:** Pew TY2024, "Reversal of prior year grant expense" $29,940,972.

### 3.3 Disclosers (filed labels; amounts and links are in the CSV)

- **Nationals (9):**
  - Fidelity: "ADJUSTMENT FOR PRIOR YEAR VOIDED GRANTS", 0.07–0.16%, TY2021–24.
  - GS DAPF: "GRANT REFUNDS" $9.18m, TY2024.
  - AEF: "REFUNDED GRANTS", TY2023–24.
  - BofA CGF: "GRANT REFUNDED $-125,000", TY2023. **New; batch 28 listed BofA as "nothing".** The item sits in a Part XI line 9 list with 2022/2023 refundable advances ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202520169349301042_public.xml)).
  - ImpactAssets: "RETURNED GRANT FUNDS" $7,441,360, TY2022 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202333199349308098_public.xml)). New.
  - Ayco: $75k.
  - Goldman Sachs Charitable Gift Fund: "RETURN OF GRANT FUNDS" $55k / $85k. New.
  - National Charitable Endowment: "RETURNED GRANT" $15k. New.
  - Rockefeller Philanthropy Advisors: "REFUNDED/RESCINDED AND AMENDED GRANTS" $1.82m / $4.52m / $4.03m. New.
- **Community foundations (17):**
  - SVCF: TY2021 $13,452,814 (0.52%) is new; TY2022 $6.86m; TY2023–24 redacted.
  - Columbus, OCF and CCF, as in batch 28.
  - New: Denver, Seattle, Cleveland, Pittsburgh, Arizona, Greater Washington, St Louis, Oklahoma City ("CANCELED/REFUNDED GRANTS" $1.24m, 2.1%), Baltimore, Santa Barbara, Princeton, Baton Rouge (reversal) and Tahoe (reversal).
- **Single-issue charities (3):**
  - Jewish Community Federation of San Francisco: "REFUNDS AND CANCELLATIONS OF PRIOR PERIOD GRANTS".
  - Stanford: "GRANT REFUND" $3,792.
  - Pew: reversals.
- **Batch 28 cross-check.** All 8 of batch 28's itemising sponsors are reproduced, with identical figures (e.g. Fidelity $16,130,006 / $16,044,329 / $16,590,356 / $11,153,865; CCF −$2,971,713 TY2024). The 13 "nothing" sponsors stay at nothing, except BofA, whose TY2023 item batch 28 missed.

### 3.4 Interpretation [I]

- **Disclosure is driven by accounting, not by void incidence.**
  - An item appears only where book and 990 treatment differ (Part XI line 9 / Schedule D Part XII).
  - NPT, DAFgiving360, Vanguard, MS GIFT, Ren/RCF and NCF itemise nothing in four years. Their voids are almost certainly netted inside grants paid.
- **Nationals disclose more often, and community foundations show higher shares.**
  - Nationals: 21% disclose, median 0.15%.
  - Community foundations: 15% disclose, median 0.28%.
  - Community-foundation figures are entity-wide, covering scholarships and competitive grants with clawback terms, and are dominated by "rescinded" and "returned" items rather than check voids.
- **Only Fidelity's label is specifically about voided grants.** No filer gives counts, causes, or a check-versus-EFT split.

---

## 4. P-WAT-02: ImpactAssets' $160.8m CY2024 grant to NPT

| Fact | Value | Source |
|---|---|---|
| Schedule I line, CY2024 | NATIONAL PHILANTHROPIC TRUST, EIN 237825575, cash $160,826,426, purpose "GENERAL SUPPORT". 1 line; the largest of 2,733 lines totalling $580.1m | [F] [CY2024 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543169349307999_public.xml) |
| Other DAF sponsors, same year | GiveClear $86,038,909; Fidelity $7,823,172 + $4,284,252 (two name variants); Vanguard Charitable $1.5m; Impact Charitable $1.7m | [F] same |
| Earlier grants to NPT | CY2021 $3,096,667 "NPT FBO Friends of UBS Optimus Foundation"; CY2022 $696,667 (same, "Ukraine Relief Fund") + $101,000; CY2023 $1,201,667 "UKRAINE RELIEF" | [F] [CY2021](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202243159349306794_public.xml), [CY2022](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202333199349308098_public.xml), [CY2023](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202443189349305024_public.xml) |
| NPT grants to ImpactAssets | FY2024 (Jul 2023–Jun 2024) $22,856,124 "HUMAN SERVICES"; FY2025 $40,638,414 "PUBLIC, SOCIETAL BENEFIT" | [F] NPT [FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202511339349301311_public.xml), [FY2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601289349302480_public.xml) |
| ImpactAssets Schedule O | No explanation of DAF-to-DAF transfers; only boilerplate (GlobalGiving ED, due diligence) | [F] CY2024 XML |
| ImpactAssets DAFs | 2,083 → 2,197 accounts; DAF grants $155.7m → $432.5m (CY2023 → CY2024) | [F] (`queue-npt-dafgiving360-misc.md` §4) |
| NPT FY2025 | DAF contributions $15.15bn (FY2024 $14.52bn); accounts 17,940 → 20,691 | [F] NPT XML |
| UBS channel | UBS factsheet created 2025-02-04: "four national sponsoring organizations: Fidelity Charitable, Impact Assets, National Philanthropic Trust, Renaissance Charitable" ([PDF](https://advisors.ubs.com/mediahandler/media/742684/Donor%20Advised%20funds-Made%20Simple.pdf)). The current UBS page lists NPT, Fidelity and RCF only ([page](https://www.ubs.com/us/en/wealth-management/our-solutions/giving/donor-advised-funds.html), approval expiry 5/1/2027) | [F] |
| Public statements | No ImpactAssets, NPT or trade-press item describes the transfer (searches 2026-11-15) | — |
| CY2025 | ImpactAssets' CY2025 990 is not in the IRS index (latest period 202412), so recurrence cannot be tested | [F] |

**Reading.**
- **Most likely [I]:** one or a few large donor-recommended transfers of DAF balances from ImpactAssets to NPT DAF accounts.
- **Against a program migration:**
  - the ImpactAssets DAF count rose;
  - no announcement exists, whereas the AssetMark move to GiveClear left a redirect trail (P-VEN-08);
  - NPT sends money the other way at a similar scale ($63.5m over FY2024–25).
- **Against an operating grant:** an operating grant of this size to NPT has no precedent.
- **Possible links [I]:** the UBS-channel overlap and the drop of "Impact Assets" from UBS's current DAF page fit a UBS-client consolidation, but nothing ties the $160.8m to UBS.
- **Correction to the watchlist (`relationship-graph-edges-additions-4.csv` ED005 / P-WAT-02 evidence):**
  - Replace "neither appears in CY2023" with "NPT received small earmarked ImpactAssets grants in CY2021–23 ($0.8–3.1m a year); the $160.8m general-support line is new in CY2024".
  - Add the reverse flow: NPT → ImpactAssets $22.9m (FY2024) and $40.6m (FY2025).

---

## 5. Limitations

- **Complaints.**
  - Convenience corpus (§2.5).
  - Severity coding comes from the original corpus and was not re-coded here.
  - Multi-sponsor attribution counts a record fully for each sponsor.
  - "Big three" is an interpretation.
  - The window is not annualised.
- **Void scan.**
  - The keyword list may miss idiosyncratic labels (e.g. "grant adjustments").
  - Amounts depend on the two layouts recognised. All 109 grant-related figures were eyeballed against the snippet, but not every one was checked against the PDF.
  - The denominator is current-year grants, while numerators often relate to earlier years.
  - Part I grants are entity-wide.
  - 13 TY2024 returns were not yet mirrored.
  - SVCF's redacted TY2023–24 figures were not recovered here (the PDF or audit route remains open).
- **P-WAT-02.**
  - Schedule I aggregates by recipient, so the number of underlying transfers is unknown.
  - NPT's Schedule B donor names are not public.

---

## 6. Data sources

| ID | Source | Date | Link |
|---|---|---|---|
| S1 | DAF user complaints corpus (244 rows) | 2026-11-14 | `data/mission-2026-11-14/daf-user-complaints-corpus.csv` |
| S2 | DAFRC Annual DAF Report 2025 dataset, FY2024 rows | Spring 2026 | https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx |
| S3 | DAFRC R1 corrections | 2026-11-14 | `data/mission-2026-11-14/dafrc-corrections-itemized.csv` |
| S4 | CFPB complaint API | 2026-11-15 | https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/ |
| S5 | IRS TEOS e-file indexes 2021–2026 | 2026-11 | https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv |
| S6 | IRS 990 XML (GivingTuesday mirror), 785 returns | TY2021–24 | per-row `source_url` in `daf-grant-voids-top200.csv` |
| S7 | ImpactAssets 990 CY2021–24 | filed 2022–25 | links in §4 |
| S8 | NPT 990 FY2024–25 | filed 2025–26 | links in §4 |
| S9 | UBS DAF factsheet; UBS DAF page | 2025-02; accessed 2026-11-15 | links in §4 |
| S10 | Batch 28 voids table, with wave-13 corrections | 2026-11-15 | `data/mission-2026-11-14/daf-grant-voids-disclosures.csv` |

---

## 7. Data dictionary

### `complaint-rates-normalised.csv`

| Column | Meaning |
|---|---|
| sponsor, ein, quadrant_areas | A3/A4 entity, EIN (blank for Every.org), and the area(s) where it is scored |
| fy2024_accounts_dafrc_published / _corrected | DAFRC FY2024 `number_of_daf_accounts`, as published and after R1 corrections |
| accounts_source | DAFRC source field, plus a correction note |
| all_n_low … all_n_critical, all_n_total, all_n_high_critical | Complaint and mixed records, 2021+, all venues, by severity |
| all_rate_per_10k, all_high_critical_rate_per_10k | Records ÷ corrected accounts × 10,000 (2021–26 window; blank when there are 0 records or no denominator) |
| noapp_* | Same, excluding `venue_type = app_store` |
| n_app_store | App Store records included in all_n_total |
| n_multi_sponsor_records | Records also attributed to another sponsor |
| venue_coverage | venue_type values present |
| record_ids | Corpus record ids counted |
| interpretable | Reading guidance (zero records / weak / descriptive only) |

The last row is a pooled total over the sponsors with at least one record, with each record counted once.

### `daf-grant-voids-top200.csv`

There is one row per hit, plus one `none found` row per scanned return with no hit.

| Column | Meaning |
|---|---|
| hit_id | `{object_id}-{n}`; blank on none-found rows |
| sponsor, ein, sponsor_type, dafrc_subtype | DAFRC name and type (national / community foundation / single-issue charity) |
| fy2024_rank, fy2024_daf_assets_corrected | Rank and value of corrected FY2024 DAF assets |
| tax_year, tax_period_end, object_id, xml_status | Return identity; status `ok`, `ok (local copy)` or `http_404` |
| schedule, line_reference | XML schedule element and FormAndLineReferenceDesc as filed |
| matched_term, item_class | Keyword matched; event class (voided grant or uncashed check / refunded or returned grant / rescinded or cancelled grant / reversal of grant expense (accrual)) |
| label_snippet | The filed text around the match (about ±90 chars) |
| amount_usd_auto, amount_status, amount_usd | Item amount as parsed (sign as filed); `parsed`, `redacted` or `no amount in item` |
| grant_related | `yes`, or `no (descriptive or policy text; no figure)` |
| review | `automatic`, or a reviewer note |
| grants_paid_part_i_line13_usd, pct_of_part_i_grants | Denominator and abs(amount) ÷ grants × 100 |
| part_xi_line9_other_changes_usd, sched_d_daf_grants_usd | Context |
| in_batch28_top30_scan | `yes` if the EIN appears in `daf-grant-voids-disclosures.csv` |
| source_url, retrieved | XML link; 2026-11-15 |

### `daf-grant-voids-top200-summary.csv`

| Column | Meaning |
|---|---|
| item_scope | All grant-related items, or excluding accrual reversals |
| group | all / national / community foundation / single-issue charity |
| sponsors_in_top_n, sponsors_with_scanned_return, returns_scanned | Coverage |
| sponsors_disclosing, sponsor_disclosure_rate_pct | Sponsors with at least one figure-bearing item in any TY2021–24 return |
| returns_disclosing, return_disclosure_rate_pct | Returns with at least one such item |
| daf_assets_share_disclosing_pct | Disclosers' share of the group's corrected FY2024 DAF assets |
| void_share_n, _min, _p25, _median, _p75, _max | Distribution of per-return void share (%) across disclosing returns |

---

## 8. Reproduction

```
python3 scripts/mission_complaint_rates.py
python3 scripts/mission_void_scan.py --irs-dir <dir with index_2021..2026.csv> --cache-dir <cache> [--xml-dir <raw xml by object id>] --fetch --n 200
```

The extract cache (`voidscan/{object_id}.json`) holds only the matching explanations and the header amounts.

## Validation corrections (wave 14, 2026-11-15) — governing
Source: [validation-wave14-report.md](validation-wave14-report.md); register `data/mission-2026-11-14/validation-register-wave14.csv`.

1. **Line 31 (§1, P-B28-02).**
   - Replace: "**29 sponsors (14.5%) itemise at least one grant void, refund, rescission or reversal with a figure**, in 72 of 785 returns (9.2%). Those 29 hold **37.5%** of scanned top-200 DAF assets."
   - With: "**The scan's hit rule finds 29 sponsors (14.5%), in 72 of 785 returns; validation wave 14 found at least 5 more that it misses** (\"recovery of prior year grants\": Greater Houston, Maine, the Fund for Charitable Giving; \"grant returns\": Fox Valley; \"prior year grant adjustments\": Vermont). The floor is therefore **at least 34 sponsors (17.0%)** in 85 returns (10.8%), holding about 38.0% of scanned DAF assets."
   - Also replace "nationals 9 of 43 (20.9%), community foundations 17 of 113 (15.0%)" with "nationals at least 10 of 43 (23.3%), community foundations at least 21 of 113 (18.6%)".
2. **§3.1 Hit rule.** Append: "Known misses (wave 14): 'recovery of prior year grants', 'grant returns', 'prior year grant adjustments'."
3. **§3.2 table.** Add a footnote: "Rates are floors; see validation-wave14-report.md for 5 missed sponsors. Void-share statistics use n = 70 returns (two SVCF returns are redacted)."
4. **Lines 187–188 (§3.4).** Replace "Nationals: 21% disclose, median 0.15%." and "Community foundations: 15% disclose, median 0.28%." with "Nationals: at least 23% disclose, median 0.15%. Community foundations: at least 19% disclose, median about 0.28%."
5. **Line 30 (§1, P-QA3-04).**
   - Replace: "Most of the big three's high-severity weight comes from the six shared 2026 SPLC records (CMP-215–220)."
   - With: "The six shared 2026 SPLC records (CMP-215–220) supply most high-severity weight for Vanguard (6 of 8) and DAFgiving360 (6 of 9). For Fidelity they supply 6 of 21 on all venues (11 are App Store login reviews) and 6 of 10 without the App Store."
6. **Line 198 (§4 table).** Replace "1 line; the largest of 2,733 lines" with "the one general-support line (a second NPT-EIN line, $10,000 'FBO Friends of UBS Optimus Foundation', also appears); the largest of 2,733 lines".
