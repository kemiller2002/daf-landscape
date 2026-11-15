# Direction P-NEW-RCP-01: who receives DAF grants (sector and concentration), impact investing inside DAFs, and corporate matching-gift treatment of DAF grants

**Date:** 2026-11-15 · **Queue item:** P-NEW-RCP-01 (new direction from the owner)

**Outputs**
- [`data/mission-2026-11-14/daf-grant-recipient-sectors-top50.csv`](../../data/mission-2026-11-14/daf-grant-recipient-sectors-top50.csv): 3,984 rows. Dollar shares by NTEE major group plus concentration, by scope (all, segment, each sponsor) × FY (2023, 2024, pooled) × basis (filed, DAF-weighted).
- [`data/mission-2026-11-14/daf-impact-pools-2026.csv`](../../data/mission-2026-11-14/daf-impact-pools-2026.csv): 20 rows. Published sizes of impact, ESG and sustainable pools and programmes, 2021+.
- [`data/mission-2026-11-14/matching-gift-daf-policies-2026.csv`](../../data/mission-2026-11-14/matching-gift-daf-policies-2026.csv): 16 rows. Corporate matching-gift clauses on DAF grants.
- [`data/mission-2026-11-14/queue-proposals-batch39-n4.csv`](../../data/mission-2026-11-14/queue-proposals-batch39-n4.csv): P-B39N4-01..03.
- **Script:** [`scripts/mission_recipient_sectors.py`](../../scripts/mission_recipient_sectors.py) (stdlib, functional style).

**Rules applied**
- **Governing corrections read first:**
  - wave 18 ([queue-batch33-panel-scans.md](queue-batch33-panel-scans.md), final section);
  - batch 34 ([queue-batch34-netting-filings.md](queue-batch34-netting-filings.md)): the reviewed DAF-to-DAF whitelist (P-NPO-04) and the attachment-only Schedule I sponsors (P-NPO-03).
  - None of the wave-18 items touches the Schedule I flows used here.
- **Recency:** all data are FY2023–FY2024 returns (tax years 2022–2024) or 2021+ publications. Pre-2021 matching-gift documents are kept only for traceability and flagged `recency_ok_2021plus = 0`.
- **robots.txt** was read for every host before fetching (§5). Hosts whose robots.txt could not be read (BusinessWire, DAFgiving360/Schwab Charitable, 3M) were **not fetched**; where they appear, they are labelled search-snippet [S]/[U].
- **No outreach, logins or forms.**
- **Labels:** **[F]** filed or primary-document value; **[P]** sponsor's own publication (not audited); **[C]** script computation; **[I]** inference; **[S]** secondary or search snippet; **[U]** not found or unverified.
- **This is research, not legal or tax advice.**

---

## 0. Answers in brief

| Question | Answer | Confidence |
|---|---|---|
| **1. Which sectors receive DAF grants (top 50, FY2023–24)** | **Size and exclusions.** Schedule I lines from the 46 itemising non-university top-50 sponsors (90 sponsor-years; 94 including Stanford and UCLA Foundation) total **$90.04bn**. **DAF-to-DAF transfers of $12.70bn (14.1%)** are removed, leaving **$77.34bn to 174,195 recipients** [C].<br><br>**Shares of the net dollars:**<br>- education **25.8%**;<br>- human services **14.3%**;<br>- public-society benefit **14.1%** (of which NTEE T philanthropy/federated/foundations 5.7 pts);<br>- religion **13.6%**;<br>- health **10.0%**;<br>- environment/animals 5.7%; arts 5.6%; international 5.6%;<br>- unclassified 4.9%.<br><br>**On the strict BMF-only basis**, which drops the name-rule fills, the shares are 27.9 / 15.8 / 15.9 / 12.6 / 8.8 / 6.0 / 6.2 / 6.3% [C]. | High on the filed lines and the join [F/C]; the NTEE taxonomy and name rules are [I] |
| **Concentration** | **Very diffuse:**<br>- top 10 recipients 10.0%, **top 100 24.3%**;<br>- **HHI 21** (0–10,000 scale);<br>- FY2023 top-100 28.6% (HHI 42), FY2024 22.4% (HHI 14).<br><br>**Mega-gifts drive the top:**<br>- Johns Hopkins $2.61bn from 32 sponsors;<br>- SVCF's single lines to Further Future Foundation ($1.31bn) and four Chan Zuckerberg Biohub/Institute LLCs ($1.66bn). [C] | High [C] |
| **National vs community foundations** | **National sponsors ($54.1bn net):**<br>- education 28.9%, religion **14.1%**, human services 14.2%, public benefit 12.3%;<br>- top-100 25.2%, HHI 28.<br><br>**Community foundations ($15.6bn):**<br>- education 18.2%, religion **2.9%**, human services 16.3%, health 18.8%, public benefit 20.7%;<br>- top-100 37.3%, HHI 109, driven by SVCF.<br><br>**Community foundations excluding SVCF ($9.65bn):**<br>- education 21.3%, **human services 21.2%**, health 10.5%, public benefit 13.4%, **environment 8.9%**, religion 4.3%;<br>- top-100 23.1%, HHI 10.<br><br>**Single-issue sponsors** (NCF, JCF, Thrivent and others): religion 32.5%.<br><br>**Reading:** national DAF money skews to education and religion; community-foundation money skews to local human services and environment. Concentration is similar once SVCF is set aside [C/I]. | High on the direction [C]; magnitudes depend on SVCF and a few mega-lines |
| **2. Impact investing inside DAFs** | **Fidelity Charitable reports $4.6B "invested for impact" in 2024** (five impact-investing pools plus other values-aligned options), against $2.3B in a base year it labels 2020 on p.13 and 2015 in its appendix [P].<br><br>**ImpactAssets** (an all-impact DAF sponsor) filed **Schedule D DAF value of $2.90bn at 2024-12-31** (2,197 DAFs) [F]. Its website shows $5B+ firm-wide AUM, $882M invested and $393M granted in 2025 [P].<br><br>**No sizes published:**<br>- Vanguard Charitable (4 ESG/impact options);<br>- DAFgiving360 (SRI pools);<br>- MS GIFT;<br>- Boston Foundation's Impact and Mission First pools (1% of Balanced Plus/Impact pool DAF assets from 2025-07-01, rising to 5% by 2030);<br>- SFF's BACIF. [U/P]<br><br>**A March 2026 commentary puts all impact-invested DAF capital at $3–4bn [S].** That is below Fidelity plus ImpactAssets alone, so definitions differ. | Medium: mostly self-reported |
| **3. Corporate matching gifts** | **No dominant rule; conditional acceptance is the modal clause.** Grants *from* a DAF are matched if the employee is the sole funder or is named on the fund, and gifts *into* a DAF are excluded:<br>- GE Foundation 2023 [F];<br>- Disney 2021 [F];<br>- EY 2022 (with acknowledgment letter) [F];<br>- Chevron, American Express and Edwards (2025 quotes) [S].<br><br>**Exclusions:** CarMax excludes both directions [S]. Bank of America's quoted clause excludes gifts *to* DAFs and is read by Double the Donation as excluding DAF grants; the same article contradicts itself [S]. Dow is contradictory [S].<br><br>**Sponsor side:** Fidelity Charitable defers to the employer and supplies grant confirmations [P].<br><br>**Reverse model:** Fidelity Investments matches employee contributions *into* a Fidelity Charitable sub-account [P]. | Medium-low: few 2021+ primary documents |

---

## 1. Recipient sectors (question 1)

### 1.1 Method
1. **Universe.**
   - Top-50 DAFRC sponsors by FY2024 DAF assets and their chosen FY2023–FY2024 returns, exactly as in [`mission_daf_to_daf.py`](../../scripts/mission_daf_to_daf.py) (`top_n`, `pick_returns` over the `netpayout990/` cache).
   - 100 sponsor-years, all with a return. 94 itemise Schedule I.
   - **Not itemised (attachment only, batch 34 §3):** BofA Charitable Gift Fund (both years), Renaissance Charitable (both), Greater Horizons FY2023, Greater Kansas City CF FY2023.
2. **Full Schedule I.** The `netpayout990/` cache keeps only panel-recipient lines plus the 25 largest, so the script re-reads every Schedule I Part II `RecipientTable` line from the same returns (IRS e-file XML).
   - **Sources:** 77 returns came from local copies already in scratch and 17 from the GivingTuesday mirror of IRS TEOS (`https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml`).
   - **Check:** a copy is accepted only if its line count equals the cached `sched_i_lines`. All 94 matched.
   - **Volume:** 604,915 lines; 171,370 distinct recipient EINs [F].
3. **DAF-to-DAF exclusion.** A line is excluded when any of these holds:
   - the recipient EIN has decision `include` in [`daf-to-daf-recipient-whitelist.csv`](../../data/mission-2026-11-14/daf-to-daf-recipient-whitelist.csv) (929 EINs: W2 nationals/processors with DAF share ≥ 0.5, W3 community foundations, W4 DAF-heavy single-issue sponsors);
   - it is a self-line;
   - it has a blank EIN and its normalised name matches exactly one whitelisted name.
   
   Lines to whitelist-`exclude` panel EINs (universities, hospitals, TNC, United Ways, RPA and similar) stay in as ordinary charities.
4. **Sector join.** Recipient EIN → IRS Exempt Organizations Business Master File (`eo1`–`eo4`, `eo_pr`, `eo_xx`; [IRS SOI EO BMF](https://www.irs.gov/pub/irs-soi/eo1.csv), Last-Modified 2026-11-09). 149,096 of 171,370 EINs matched [F]. The `NTEE_CD` first letter maps to the major groups:
   - A arts;
   - B education;
   - C–D environment/animals;
   - E–H health;
   - I–P human services;
   - Q international;
   - R–W public-society benefit (T = philanthropy, federated giving and grantmaking foundations, reported separately);
   - X religion;
   - Y mutual/membership;
   - Z unknown.
5. **Fallbacks** (flagged in the script's `method` field):
   - **BMF FOUNDATION code:** 10 church → religion, 11 school → education, 12 hospital/medical research → health. These are filed IRS classifications.
   - **Name-keyword rule:** for the rest, e.g. CHURCH, DIOCESE, YESHIVA → religion; UNIVERSITY, SCHOOL → education; HOSPITAL, BIOHUB → health. This is [I].
   - Every share is reported twice: of all net dollars (`share_of_non_d2d`), and of NTEE- or foundation-code-classified dollars only (`share_of_bmf_classified`).
6. **DAF weighting.** A sensitivity basis (`daf_weighted`) multiplies each sponsor-year's lines by its DAF share of grants from `sponsor-cost-structure.csv`, capped at 1. Coverage is 94/94 sponsor-years. It changes no headline share by more than 0.4 pts at the pooled level.
7. **Concentration** is computed on recipient keys (EIN, or normalised name if the EIN is blank):
   - distinct recipients;
   - top-10 and top-100 share;
   - HHI = Σ(share × 100)², on a 0–10,000 scale.

### 1.2 Coverage [F/C]
| Scope (itemising sponsor-years, ex university/hospital) | Schedule I itemised | Part IX line 1 (all grants to domestic orgs) | Schedule D DAF grants | Sched I ÷ Part IX | Sched I ÷ DAF grants |
|---|---|---|---|---|---|
| All | $90.04bn | $91.85bn | $90.26bn | **98.0%** | 99.8% |
| National | $62.76bn | $64.08bn | $64.87bn | 97.9% | 96.7% |
| Community foundation | $18.21bn | $18.62bn | $16.60bn | 97.8% | 109.7% |
| Single-issue | $8.18bn | $8.26bn | $7.91bn | 99.1% | 103.5% |

- **The >$5,000 limit costs about 2% of dollars.** Schedule I itemises grants over $5,000 per recipient, and the itemised total is 98% of Part IX line 1. The many small grants (by count) are therefore missing, but little money is.
- **Community foundations' Schedule I exceeds their DAF grants.** It includes discretionary, field-of-interest and scholarship grants as well. The DAF-weighted basis addresses this only proportionally.

### 1.3 Results: shares of net (non-DAF-to-DAF) dollars, FY2023–24 pooled, filed basis [C]
Each cell shows % of net dollars, with % of the BMF-classified basis in brackets.

| Group | All ex univ./hosp. | National | Community foundations | CF ex SVCF | Single-issue |
|---|---|---|---|---|---|
| Net dollars | **$77.34bn** | $54.13bn | $15.62bn | $9.65bn | $7.51bn |
| DAF-to-DAF excluded | $12.70bn (14.1%) | $8.63bn (13.7%) | $2.59bn (14.2%) | $0.52bn (5.1%) | $0.67bn (8.1%) |
| Education | **25.8%** (27.9) | 28.9% (30.6) | 18.2% (21.0) | 21.3% (22.3) | 19.6% (21.0) |
| Human services | **14.3%** (15.8) | 14.2% (15.3) | 16.3% (20.0) | 21.2% (23.9) | 11.1% (12.0) |
| Public-society benefit | **14.1%** (15.9) | 12.3% (13.5) | 20.7% (25.8) | 13.4% (15.5) | 12.7% (13.8) |
| … of which NTEE T | 5.7% | 5.7% | 5.0% | 5.5% | 6.7% |
| Religion | **13.6%** (12.6) | 14.1% (12.6) | 2.9% (2.8) | 4.3% (3.7) | 32.5% (30.6) |
| Health | **10.0%** (8.8) | 8.1% (8.8) | 18.8% (10.2) | 10.5% (12.0) | 5.1% (5.6) |
| Environment/animals | 5.7% (6.0) | 5.7% (5.9) | 6.8% (7.6) | 8.9% (9.0) | 3.3% (3.6) |
| Arts/culture | 5.6% (6.2) | 6.1% (6.6) | 5.3% (6.5) | 7.2% (8.0) | 2.7% (2.9) |
| International | 5.6% (6.3) | 5.5% (6.0) | 4.4% (5.5) | 4.3% (4.9) | 8.9% (9.7) |
| Unknown (Z) | 0.5% | 0.5% | 0.4% | 0.6% | 0.5% |
| Unclassified | 4.9% | 4.7% | 6.2% | 8.5% | 3.6% |
| Recipients | 174,195 | 151,778 | 37,378 | 34,807 | 30,066 |
| Top-10 / top-100 share | 10.0% / **24.3%** | 10.2% / 25.2% | 21.9% / 37.3% | 6.1% / 23.1% | 10.8% / 32.6% |
| HHI | **21** | 28 | 109 | 10 | 22 |

**Notes**
- **Processor segment:** Dechomai's lines are 91% DAF-to-DAF; the $0.08bn remainder is in the CSV.
- **University/hospital sponsors** (Stanford, UCLA Foundation: $0.94bn net, 88% education) are in `all_top50_itemising` but not in the table.
- **Community-foundation health** is 18.8% because SVCF's FY2023 lines to four Chan Zuckerberg Biohub/Institute LLCs ($1.66bn) are classified as health by the name rule; these LLCs are not in the BMF. On the BMF-only basis the share is 10.2%.
- **Year split (all ex university/hospital):** DAF-to-DAF rose from 11.3% (FY2023) to 16.4% (FY2024) of Schedule I. Sector shares moved by 1 pt or less [C].

**Classification mix (net dollars)** [C]:
- NTEE 82.0%;
- BMF foundation code 6.9% (church 4.6%, school 2.2%, hospital 0.1%);
- name rule 6.3%;
- unclassified 4.8%: in the BMF without NTEE 3.5%, EIN not in the BMF 0.9%, blank EIN 0.3%, government 0.1%.

**Largest NTEE codes** [C]:
- **Education:** B43 universities $6.90bn; B11 single-organisation support $2.74bn; B42 $1.16bn.
- **Religion:** X20 Christian $2.14bn; X21 Protestant $1.18bn; X30 Jewish $0.78bn.
- **International:** Q30 $1.27bn; Q33 relief $1.26bn.
- **Philanthropy (T):** T30 public foundations $1.34bn; T70 federated giving $0.73bn; T50 $0.43bn; T20 private grantmaking foundations $0.33bn.
- Some T30 recipients may themselves hold DAFs without being DAFRC panel members. They are kept, which is a small DAF-to-DAF leak [I].

**Largest recipients, all ex university/hospital, FY2023–24** [F/C]:

| Recipient | Amount | Sponsors | Classification |
|---|---|---|---|
| Johns Hopkins University | $2.61bn | 32 | B43 |
| Further Future Foundation (BMF name Navigation Charitable Fund) | $1.31bn | 1 (SVCF) | U05 |
| Stanford | $0.63bn | — | — |
| CZ Institute for Advanced Biological Imaging | $0.59bn | — | not in BMF |
| CZ Biohub SF | $0.58bn | — | not in BMF |
| Church of Jesus Christ of Latter-day Saints | $0.47bn | — | — |
| Harvard | $0.44bn | — | — |
| New Venture Fund | $0.43bn | — | — |
| Blue Meridian Partners | $0.36bn | — | — |
| The 85 Fund | $0.31bn | — | — |

- **Blank-name line:** Greater Horizons' FY2024 return carries a $212.2m line with a blank name and EIN. It is unclassified.

**DAF-to-DAF removed, by recipient segment** [C]:
- national $9.81bn;
- community foundations $1.55bn;
- single-issue (whitelisted) $1.07bn;
- processors $0.30bn.

**Kept lines to non-whitelisted panel EINs:** universities/hospitals $5.93bn, single-issue $1.05bn, nationals such as RPA $0.35bn.

### 1.4 Cross-check against a sponsor's own published split [P vs C]
Fidelity Charitable's [2025 Giving Report](https://fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf) (calendar 2024, p.12 and appendix) gives these shares of grant dollars:
- society benefit 25%;
- education 23%;
- religion 13%;
- human services 13%;
- health 8%;
- arts 6%;
- international 5%;
- environment 5%;
- other 2%.

**Fidelity FY2024 Schedule I in this script** (FYE June 2024): education 24.6%, religion 15.7%, human services 13.2%, health 10.5%, arts 6.1%, international 5.4%, environment 5.7%, public-society benefit 13.1%.

**The public-benefit gap is a classification effect.** Adding back Fidelity's excluded DAF-to-DAF lines ($1.19bn) lifts public-society benefit to 21.4% of all its Schedule I dollars, close to the sponsor's 25%. So Fidelity's "society benefit" evidently includes sponsor-to-sponsor grants [C/I]. The other sectors agree within about 2.7 pts, despite the period mismatch and the different taxonomies.

### 1.5 Limitations
- **Schedule I shape:**
  - It itemises only grants over $5,000 per recipient. That is about 2% of dollars, but most grants by count.
  - Part II is domestic organisations only. Foreign grants are on Schedule F, which was not parsed, so **international is understated** (foreign-address Part II lines total only $0.3m).
- **Attachment-only sponsors are invisible as grantors.** BofA CGF and RCF had ≈$0.83–0.97bn and $0.55–0.75bn of Schedule I totals a year.
- **Schedule I at community foundations includes non-DAF grants.** The DAF-weighted basis scales them proportionally but cannot separate them.
- **NTEE codes are assigned by the IRS/NCCS, sometimes coarsely.** Supporting organisations (B11, T-codes) hide the end use; e.g. "Further Future Foundation" is U05.
- **The name rule is inference**, used for 6.3% of dollars. Shares on the strict BMF-only basis are shown alongside.
- **Mega-gifts dominate a few cells:** SVCF/CZ, the Johns Hopkins gifts, Further Future. Per-sponsor rows are in the CSV.
- **Fiscal years** follow the DAFRC convention: a June-FYE FY2024 covers July 2023–June 2024.

## 2. Impact investing inside DAFs (question 2)

The full rows, with metric, as-of date, source and robots status, are in [`daf-impact-pools-2026.csv`](../../data/mission-2026-11-14/daf-impact-pools-2026.csv).

### Fidelity Charitable (largest sponsor) [P]
Source: [2025 Giving Report](https://fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf), p.13 and appendix.
- **"Amount invested for impact" $4.6B (2024)**, through "investment options, including five impact-investing pools, aligned with their values". The figure doubled from $2.3B. The report labels the base year 2020 on p.13 but 2015 in the appendix, an internal inconsistency.
- **Grants to impact-investing nonprofits:** $138M in 2024 ($70M in 2020; $618M lifetime).
- **Recoverable grants:** $10.8M in 2024 ($69.5M lifetime).
- **Total impact-investing support:** $687.5M at 2024-12-31, against a $1B goal for 2028.
- **Scale:** $4.6B is about 7% of Fidelity's filed FYE-6/2024 DAF assets of $66.2bn [C; the periods differ]. It is a sponsor definition that includes values-aligned (ESG) pools.
- The [sustainable and impact pools FAQ](https://www.fidelitycharitable.org/faqs/all/sustainable-impact-investing-pools.html) publishes no pool sizes.

### ImpactAssets (all DAF assets impact-oriented)
- **Schedule D DAF value** [F]:
  - $2.717bn and 2,083 DAFs at 2023-12-31 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202443189349305024_public.xml));
  - **$2.897bn and 2,197 DAFs at 2024-12-31** ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543169349307999_public.xml)), with contributions of $611.9m and DAF grants of $432.5m.
- **DAFRC mismatch:** DAFRC's FY2024 row for this EIN is *imputed* at $3.628bn (period 2023-12-31), $0.73bn above the filing. This is P-B39N4-02.
- **Website** [P] ([our-impact](https://impactassets.org/our-impact/), counters read 2026-11-15): $5B+ firm-wide AUM, including non-DAF products; $882M of private-market investments in 2025 (431 placements); $393M granted in 2025; $2B+ lifetime grants.
- **Press release:** "$4.6B AUM (Sept 2025)" was seen only as search text. BusinessWire's robots.txt could not be read, so the release was not fetched [S].

### Other national sponsors [U]
- **[Vanguard Charitable](https://www.vanguardcharitable.org/investments):** four values-driven options (ESG U.S. Stock/ESGV, ESG Global Stock, ESG International Stock/VSGX, Baillie Gifford Global Positive Impact/VBPIX). No size or take-up published.
- **DAFgiving360 (Schwab Charitable):** SRI balanced, large-cap and fixed-income pools; the fixed-income pool is on the TIAA-CREF Core Impact Bond Fund. This is from search text only, because robots.txt returns 403. No size found.
- **[MS GIFT](https://www.morganstanley.com/content/dam/msdotcom/en/assets/pdfs/MS_Impact-Investing-and-Donor-Advised-Funds_AL.pdf)** (MS Institute for Sustainable Investing, 2026): no pool size. The report says about 65% of MS GIFT donor giving in 2025 went to causes aligned with MSISV impact categories, and that 27% of surveyed U.S. investors use philanthropic assets for impact investing.

### Community foundations [P/U]
- **The Boston Foundation's [Mission First Pool](https://www.tbf.org/donors/mission-first-pool-faq):**
  - from 2025-07-01, 1% of DAF assets in the Balanced Plus and Impact Pools is allocated to it, rising 1 pt a year to 5% by 2030;
  - target return 1–3%;
  - donors can opt in up to 50% of a fund;
  - no dollar size.
- **TBF's [Impact Pool](https://www.tbf.org/donors/impact-investing):** no size.
- **The San Francisco Foundation's [BACIF](https://sff.org/what-we-do/investments/):** an allocation since July 2022, amount not published.
- **RSF Social Finance** (impact-finance DAF sponsor; DAFRC, filed) [F]: DAF assets $63.7m (FY2023) and $32.8m (FY2024).

### Market estimate [S]
- [GA Social Impact Collaborative, 2026-03-09](https://gasocialimpact.com/?p=12584), citing a 2021 NY Fed case study and ImpactAlpha 2024: "roughly $3 to $4 billion" of DAF capital is impact-invested, and CapShift has mobilised $1B.
- **Inconsistency:** Fidelity's self-reported $4.6B plus ImpactAssets' filed $2.9B already exceed this. The commentary appears to count dedicated impact programmes, not ESG/values-aligned pools [I].

### Reading [I]
- **Published, sponsor-level figures exist for only two programmes:** Fidelity (self-reported) and ImpactAssets (filed).
- A defensible floor for "impact-labelled DAF capital" in 2024 is ImpactAssets' $2.9bn [F]. Adding Fidelity's broader $4.6B gives ≈$7.5bn, about 2.3% of corrected FY2024 market DAF assets ($323.27bn) [C/I].
- **The other large sponsors offer ESG pools but do not publish sizes.**

## 3. Corporate matching gifts (question 3)

The full rows, with verbatim clauses, dates and source types, are in [`matching-gift-daf-policies-2026.csv`](../../data/mission-2026-11-14/matching-gift-daf-policies-2026.csv).

| Policy on grants *from* DAFs | Programmes (document date, label) |
|---|---|
| **Accepts, conditional on the employee being sole funder or named on the fund** | - GE Foundation ([2023 guidelines](https://www.ge.com/sites/default/files/mg_guidelines.pdf): "funded solely by the eligible GE participant") [F]<br>- Disney ([terms last modified 2021-02-03](https://files.doublethedonation.com/forms/walt-disney-guidelines.pdf): "if the employee or the employee's family established, and is named on, the fund") [F]<br>- Chevron (directly funded by the employee/retiree/director only) [S]<br>- American Express (fund set up by the employee in his or her name) [S]<br>- P&G (sole donor; 2014 PDF, stale) |
| **Accepts, with documentation** | - EY higher-education match ([2022](https://files.doublethedonation.com/forms/Ernst---Young-guidelines-1659381031.pdf): acknowledgment letter from the organisation) [F] |
| **Accepts** | - Edwards Lifesciences ("gifts coming out of an employee's donor-advised fund") [S] |
| **Excludes** | - CarMax ("gifts to and from donor-advised funds") [S]<br>- 3M (search text only; not fetched) [U] |
| **Ambiguous / contradictory** | - Bank of America: quoted clause "We do not match charitable gifts to private foundations, family or donor-advised funds"; DtD's FAQ says BofA is "known to match" [S]<br>- Dow: two contradictory quotes [S] |
| **Silent** | - Deloitte Foundation (higher education) [F] |
| **Gifts *into* DAFs** | Excluded wherever addressed: GE, AmEx, CarMax, Gates (2011, stale), P&G (2014, stale) |
| **Sponsor side** | - [Fidelity Charitable FAQ](https://fidelitycharitable.org/faqs/donor/grantmaking.html): the employer decides; the sponsor supplies grant confirmations [P]<br>- [Fidelity Investments' employee match](https://www.fidelitycharitable.org/employee-match-program.html) pays *into* a Match Account sub-account of the employee's Giving Account, tiered up to $50,000 (page cites 2017 eligibility guidelines) [P] |

- **Secondary source:** [Double the Donation, "Are DAFs eligible for matching gifts?"](https://doublethedonation.com/matching-gifts-donor-advised-funds), published 2025-09-16. Its robots.txt allows it, disallowing only `/api/360matchpro/`.
- **No published statistic** gives the share of matching programmes accepting DAF grants [U].

**Reading** [I]:
- The modal large-company rule lets a DAF grant be matched when the DAF is the employee's own money, and requires a receipt from the charity, not from the sponsor.
- An entrant's DAF product needs per-grant confirmations and a sole-funder or named-advisor attestation to be match-eligible.
- Gifts into a DAF are not matchable.

**Limitation:** only three primary documents dated 2021 or later were obtainable without logins. Most current programme terms sit behind Benevity/YourCause employee portals.

## 4. Data dictionary

### `daf-grant-recipient-sectors-top50.csv` (one row per scope × FY × basis × NTEE major group)

| Column | Meaning |
|---|---|
| scope, scope_type | `all_top50_itemising`, `all_ex_university_hospital` (type `all`); `national`, `processor`, `community_foundation`, `community_foundation_ex_svcf`, `single_issue`, `university_hospital` (type `segment`); a sponsor's DAFRC name (type `sponsor`) |
| segment, sponsor_rank_fy2024 | DAFRC segment (as in `mission_net_payout.segment_of`); FY2024 DAF-asset rank (sponsor rows) |
| fiscal_year | `2023`, `2024` or `2023-2024` (DAFRC FY convention) |
| basis | `schedule_i` (filed line amounts) or `daf_weighted` (× the sponsor-year's DAF share of grants, capped at 1) |
| ntee_major_group | `ALL` (scope totals and concentration) or one of education, religion, human_services, health, arts_culture, international, environment_animals, public_societal_benefit, mutual_membership, unknown_z, unclassified |
| amount_usd, share_of_non_d2d | Dollars after removing DAF-to-DAF lines, and share of the scope's non-DAF-to-DAF dollars |
| amount_ntee_or_bmf_only_usd, share_of_bmf_classified | Dollars classified by NTEE or BMF foundation code only (name rule excluded), and share of that classified total. On the `ALL` row: the classified total and its share of net dollars |
| lines, recipients | Schedule I lines and distinct recipients in the cell |
| public_benefit_T_philanthropy_usd | NTEE T dollars (public_societal_benefit and ALL rows) |
| name_rule_usd | Dollars classified by the name-keyword rule |
| total_sched_i_usd, d2d_excluded_usd, d2d_share | ALL rows: all Schedule I dollars, DAF-to-DAF dollars removed, and their share |
| top10_share, top100_share, hhi | ALL rows: concentration of non-DAF-to-DAF dollars by recipient (HHI on 0–10,000) |
| sponsor_years | ALL rows: sponsor-years in the cell |
| source | Provenance |

### `daf-impact-pools-2026.csv`

| Column | Meaning |
|---|---|
| row_id, sponsor_or_program, sponsor_type, program | Identity |
| metric, value_usd, value_text, as_of | What is measured, the number (blank if not published) and its date |
| source_type, label | Kind of source; [F]/[P]/[S]/[U] |
| source_url, accessed, robots | URL, access date, robots.txt status |
| notes | Caveats and cross-references |

### `matching-gift-daf-policies-2026.csv`

| Column | Meaning |
|---|---|
| row_id, company_or_program | Identity |
| policy_on_grants_from_daf, condition | Classification of grants *from* a DAF, and the condition for acceptance |
| policy_on_gifts_into_daf | Treatment of contributions *into* a DAF |
| guideline_text | Verbatim clause (or snippet text where marked) |
| document_date, recency_ok_2021plus | Document or quote date; 1 = 2021+, 0 = pre-2021 (traceability only) |
| source_type, label, source_url, accessed, robots, notes | Provenance |

### `queue-proposals-batch39-n4.csv`
- Columns and scales follow [queue-proposals-README.md](../../data/mission-2026-11-14/queue-proposals-README.md).
- IDs are P-B39N4-01..03.

## 5. Source register

| ID | Source | Accessed | Robots |
|---|---|---|---|
| S1 | IRS e-file XML (Schedule I Part II, Schedule D), GivingTuesday mirror of IRS TEOS; 94 returns listed by object id in the script's universe (`pick_returns`) | 2026-11-15 | Mirror robots.txt 404 (no rules) |
| S2 | [IRS EO BMF](https://www.irs.gov/pub/irs-soi/eo1.csv) eo1–eo4, eo_pr, eo_xx (Last-Modified 2026-11-09) | 2026-11-15 | Allowed (only `/charities-non-profits/tax-exempt-organization-search` disallowed) |
| S3 | Repo: `daf-to-daf-recipient-whitelist.csv` (batch 34), `dafrc-sponsor-schedule-d-fy2019-2024.csv`, `sponsor-cost-structure.csv`, `netpayout990/` cache | repo | n/a |
| S4 | [Fidelity Charitable 2025 Giving Report](https://fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf); [FAQ](https://fidelitycharitable.org/faqs/donor/grantmaking.html); [employee match](https://www.fidelitycharitable.org/employee-match-program.html); [pools FAQ](https://www.fidelitycharitable.org/faqs/all/sustainable-impact-investing-pools.html) | 2026-11-15 | Allowed |
| S5 | [ImpactAssets our-impact](https://impactassets.org/our-impact/) and home page | 2026-11-15 | Allowed |
| S6 | [Vanguard Charitable investments](https://www.vanguardcharitable.org/investments) | 2026-11-15 | Allowed |
| S7 | [Morgan Stanley ISI, Impact Investing and Donor-Advised Funds (2026)](https://www.morganstanley.com/content/dam/msdotcom/en/assets/pdfs/MS_Impact-Investing-and-Donor-Advised-Funds_AL.pdf) | 2026-11-15 | Allowed (`/content/dam/msdotcom/` allowed for all agents) |
| S8 | The Boston Foundation ([Mission First FAQ](https://www.tbf.org/donors/mission-first-pool-faq), [impact investing](https://www.tbf.org/donors/impact-investing)); [SFF investments](https://sff.org/what-we-do/investments/) | 2026-11-15 | Allowed |
| S9 | [GA Social Impact Collaborative, 2026-03-09](https://gasocialimpact.com/?p=12584) | 2026-11-15 | Allowed |
| S10 | [Double the Donation DAF article (2025-09-16)](https://doublethedonation.com/matching-gifts-donor-advised-funds) and hosted guideline PDFs (Disney, EY, Deloitte, P&G, Chevron, AmEx, Gates); [BofA company page](https://www.doublethedonation.com/matching-gifts/bank-of-america) | 2026-11-15 | Allowed (only `/api/360matchpro/` disallowed; `files.` host robots 404) |
| S11 | [GE Foundation matching guidelines](https://www.ge.com/sites/default/files/mg_guidelines.pdf) (2023) and the January 2020 version | 2026-11-15 | Allowed |
| S12 | Not fetched (robots.txt unreadable): businesswire.com (timeout), dafgiving360.org / schwabcharitable.org (403), multimedia.3m.com (403), cct.org (403). The NY Fed DAF case study PDF was fetched (robots allowed) but had no text layer | — | — |

## 6. Reproduction
```
python3 scripts/mission_recipient_sectors.py --np-cache NPCACHE --bmf-dir BMF --lines-cache LINES \
    [--xml-dir DIR ...] --fetch
```
- `NPCACHE/netpayout990` comes from `mission_net_payout.py`.
- `BMF` holds `eo1.csv`..`eo4.csv`, `eo_pr.csv`, `eo_xx.csv` from https://www.irs.gov/pub/irs-soi/.
- `LINES` caches the full Schedule I line lists, one JSON per object id.
- The script prints a JSON summary covering coverage, the classification mix, pooled shares, the DAF-to-DAF split, NTEE detail, top recipients and per-sponsor shares. Every §1 figure comes from that summary or from the CSV.
- §2–3 figures come from the cited pages; they were entered by hand into the two CSVs with verbatim text.
