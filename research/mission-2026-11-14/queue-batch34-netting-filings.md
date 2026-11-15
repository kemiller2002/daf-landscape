# Queue batch 34 A: DAF-to-DAF netting rule R5 for the corrected market totals (P-B33A-01), a reviewed DAF-to-DAF recipient whitelist (P-NPO-04), attachment-only Schedule I sponsors (P-NPO-03), 2026-filed returns missing from the mirror (P-990-03), NPT "PROGRAM FEES" (P-GPT-01)

**Date:** 2026-11-15 · **Queue items:** P-B33A-01, P-NPO-04, P-NPO-03, P-990-03, P-GPT-01 (`data/mission-2026-11-14/research-priority-queue.csv`)

**Outputs**
- [`data/mission-2026-11-14/dafrc-market-totals-netted.csv`](../../data/mission-2026-11-14/dafrc-market-totals-netted.csv): corrected DAFRC grants and contributions, FY2021–24, with the R5 netting amount in three tiers (24 rows).
- [`data/mission-2026-11-14/daf-to-daf-recipient-whitelist.csv`](../../data/mission-2026-11-14/daf-to-daf-recipient-whitelist.csv): 1,411 panel EINs that received Schedule I lines from another panel sponsor, FY2021–24, each with a decision, rule and reason.
- [`data/mission-2026-11-14/queue-proposals-batch34a.csv`](../../data/mission-2026-11-14/queue-proposals-batch34a.csv): P-B34A-01 to P-B34A-03.
- **Script** (stdlib, functional style): [`scripts/mission_market_netting.py`](../../scripts/mission_market_netting.py). It transforms caches built by earlier scripts and parses nothing new.

**Conventions**
- Fiscal year (FY) is the calendar year in which the tax period ends, the DAFRC convention.
- **Recency:** everything is TY2021 or later. R5 covers FY2021–24 (the corrected-totals window). The filings work covers FY6/2021–FY2025 returns.
- **Labels:** **[F]** filed value; **[C]** script computation; **[I]** inference; **[U]** not found.
- **Governing corrections read first:**
  - wave 18 ([queue-batch33-panel-scans.md](queue-batch33-panel-scans.md), final section). None of its five items touches §4 of that report, the DAF-to-DAF flows that R5 builds on.
  - wave 16 ([queue-batch31-filings-feeds.md](queue-batch31-filings-feeds.md), final section).
- **Corrected market totals** are those of `dafrc-corrected-market-totals.csv` (rules R1–R4; FY2024 assets $323.27bn). The script rebuilds them from DAFRC plus `dafrc-corrections-itemized.csv`, and the rebuild matches to the dollar for all eight FY × metric cells [C].
- No logins, forms or contact were used. A ProPublica security check was met and not bypassed.
- **This is research, not legal or tax advice.**

---

## 0. Answers in brief

| Item | Answer | Confidence |
|---|---|---|
| **P-B33A-01** R5 netting | **R5 removes $4.05–8.03bn a year (central tier) from both corrected grants and corrected contributions** [C]:<br>- FY2021: $5.52bn, 11.5% of grants and 7.1% of contributions;<br>- FY2022: $6.40bn, 11.5% / 8.4%;<br>- FY2023: $4.05bn, 7.4% / 6.2%;<br>- FY2024: $8.03bn, 12.1% / 8.7%.<br><br>**Bounds:**<br>- Lower: $3.32–6.95bn a year (lines to national and processor recipients only).<br>- Upper: $4.88–9.42bn a year.<br><br>**Netted FY2024 (central):** grants **$58.41bn** (corrected $66.44bn), contributions **$84.74bn** ($92.77bn).<br>**Market payout on netted grants:** 25.2%, 21.0%, 22.3% and 22.8% (FY2021–24), against 28.5%, 23.8%, 24.0% and 25.9% gross.<br>**FY2024 grant growth:** +15.0% netted against +21.2% corrected. The FY2024 jump in sponsor-to-sponsor transfers (largely to NPT) inflates headline growth. | High on lines and caps [F/C]; the tier weights are [I] |
| **P-NPO-04** Whitelist | **One audited definition replaces the three nested tiers.** It covers 1,411 recipient EINs: 929 included and 482 excluded.<br><br>**Included:**<br>- 72 national/processor recipients with DAF share of assets ≥ 0.50 (W2);<br>- 767 community foundations, weighted (W3);<br>- 90 DAF-heavy single-issue or religious sponsors (W4), e.g. NCF, JCF, CJP, Donors Trust, Tides, PEF Israel, OJC Fund.<br><br>**Excluded:**<br>- 125 university/hospital sponsors (W1; $10.67bn of FY2021–24 lines);<br>- 342 single-issue sponsors (W4; $2.87bn), e.g. TNC, World Vision, JDC, United Ways;<br>- 15 national/processor recipients (W2; $0.73bn), e.g. Rockefeller Philanthropy Advisors (DAF share 0.07), Amalgamated, GoFundMe.org, Kiva.<br><br>**Affiliate pairs (W5):** 9 reviewed pairs (Dechomai, Impact Investing, Donors Capital/Donors Trust, NPT/NPT CAT, Ayco/GS DAPF and four same-name CF pairs) are kept out of the central tier ($0.17–0.28bn a year after caps). | High on the rule mechanics; thresholds are [I] |
| **P-NPO-03** Attachment-only Schedule I | **Not recoverable from public machine-readable data.**<br>- The e-file XML has no grant list. RCF FY2024 has one line, "See Attached Grant Report", $745,668,528 to 17,290 recipients; BofA CGF FY2024 has "SEE ATTACHED LIST OF DISTRIBUTIONS", $969,496,994 [F]. The attachments are binary PDFs that TEOS XML does not carry.<br>- IRS PDF images exist on ProPublica for TY2021–22 only (RCF, BofA, NYCT, Greater Horizons, GKCCF and FCG; listed in §3). Each download returns HTTP 403 "Security Check", so this needs human retrieval (P-B34A-02).<br>- **Size of the gap:** these grantor-years hold $2.02–2.56bn of DAF grants a year whose outflows R5 cannot see. At the itemising sponsors' central rate that is about **$0.16–0.32bn a year** of missing netting [I]. | High that it is gated [F]; size [I] |
| **P-990-03** 2026-filed returns | **All 19 recovered** by HTTP range reads of [`2026_TEOS_XML_05B.zip`](https://apps.irs.gov/pub/epostcard/990/xml/2026/2026_TEOS_XML_05B.zip). The index labels them "05A", and none is in the 05A zip [F].<br><br>**Harvest re-run (scratch):**<br>- 856/856 returns parse;<br>- FY2025 parsed coverage rises from **94 to 113 of 250 sponsors** [C];<br>- 54 contractor lines from the new returns.<br><br>**Key values:**<br>- Vanguard Charitable FY6/2025: 29,305 DAFs, contributions $5.75bn, grants $3.50bn, EOY **$27.01bn** [F].<br>- **Ayco Charitable Foundation FY6/2025:** final return. It merged into GS DAPF on 2025-07-01. The return reports 0 DAFs and $0 at year end, and a Schedule I/N transfer to GS DAF of **$1,162,195,533**, which is *not* in its Schedule D grants ($452.6m) [F]. | High [F] |
| **P-GPT-01** NPT "PROGRAM FEES" | **Not explained in any public NPT document.**<br><br>**Amounts:** the line has run at a flat **$3.7–4.3m since FY6/2021** ($3.80m, $4.19m, $3.74m, $4.07m, $4.29m) [F]. Over the same period DAF assets rose 3.5× ($15.9bn → $55.9bn) and grant counts rose 1.8×. So it is shaped like a fixed contract or licence, not an asset-based revenue share to private-label partners or a per-grant fee [I].<br><br>**Classification:** booked **100% Management & General in FY2021–23**, and moved to the Program column in FY2024–25. The $4,295,780 in the queue text is the FY2025 program column; the line total is $4,289,911 [F].<br><br>**Related revenue:**<br>- "Maintenance & hosting" revenue fell from $1.71m (FY2021) to $0.48m (FY2025).<br>- The consolidated summary statements show "Administrative and maintenance fees" of $656k (FY2025) and $994k (FY2024), below the 990's admin plus hosting ($1.11m and $1.50m). The gap ($457k and $501k) fits intra-group fees eliminated in consolidation [C/I].<br><br>**Ren:** still neither confirmed nor excluded. | High on lines [F]; reading [I] |

---

## 1. P-B33A-01: rule R5 (DAF-to-DAF netting)

### 1.1 Method
- **Why net.**
  - A transfer from sponsor A's DAFs to sponsor B's DAFs is in A's Schedule D Part I grants and in B's Part I contributions.
  - The panel sum therefore counts the same dollars as market grants *and* market contributions, although nothing left the DAF system.
  - R5 subtracts one amount N from both aggregates. It does not touch assets or accounts, which are stocks.
- **Lines.** Every Schedule I Part II line from a panel grantor-year (FY2021–24) to another DAFRC panel EIN comes from the `netpayout990/` cache of `mission_net_payout.py`:
  - return choice as in `mission_daf_to_daf.pick_returns`;
  - 46,537 lines from 1,523, 1,541, 1,552 and 1,545 grantor returns.
- **Market membership.** A line is netted only if:
  - the grantor-year has positive *corrected* DAF grants; and
  - the recipient-year has positive *corrected* DAF contributions, in the same FY.
  - 701 lines ($20–90m a year) fail this test. Examples: PayPal Giving Fund → Donors Fund FY2023 ($46.4m), because Donors Fund has no FY2023 DAFRC row; and Gordon Christian Trust → NCF FY2024, because the grantor has $0 corrected grants.
- **Weights by tier** (whitelist in §2):
  - **lower:** lines to W2 recipients (national or processor), × the grantor's DAF share of grants (Schedule D grants ÷ Part IX grants, median FY2022–25 from `sponsor-cost-structure.csv`);
  - **central:** lines to every whitelisted recipient, × the grantor's DAF share of grants × the recipient's DAF share of total assets;
  - **upper:** lines to every whitelisted recipient plus the W5 affiliate pairs, weight 1.
  - Missing shares take the segment median. For grants: national 1.00, processor 1.00, community foundation 0.36, single-issue 0.34. For assets: community foundation 0.23.
- **Caps.**
  - Per grantor-year, weighted lines may not exceed corrected DAF grants. Per recipient-year, they may not exceed corrected DAF contributions. Each line is scaled by min(1, grants ÷ sum, contributions ÷ sum).
  - Caps bite mainly on Dechomai: Asset Trust → Foundation lines of $0.19–0.44bn a year against Foundation DAF contributions of $36–172m, and Dechomai Foundation lines to AEF, Schwab and Fidelity above its DAF grants.
  - Cap reductions are $0.54–0.99bn a year in the upper tier and $9–80m a year in the central tier [C].

### 1.2 Results [C]

| FY | Corrected grants | R5 lower | **R5 central** | R5 upper | **Netted grants (central)** | Corrected contributions | **Netted contributions (central)** |
|---|---|---|---|---|---|---|---|
| 2021 | $48.03bn | $4.08bn (8.5%) | **$5.52bn (11.5%)** | $6.68bn (13.9%) | **$42.51bn** | $77.52bn | **$72.00bn** (−7.1%) |
| 2022 | $55.61bn | $4.79bn (8.6%) | **$6.40bn (11.5%)** | $7.40bn (13.3%) | **$49.21bn** | $76.48bn | **$70.08bn** (−8.4%) |
| 2023 | $54.83bn | $3.32bn (6.1%) | **$4.05bn (7.4%)** | $4.88bn (8.9%) | **$50.78bn** | $65.37bn | **$61.31bn** (−6.2%) |
| 2024 | $66.44bn | $6.95bn (10.5%) | **$8.03bn (12.1%)** | $9.42bn (14.2%) | **$58.41bn** | $92.77bn | **$84.74bn** (−8.7%) |

**Growth and payout** (payout = grants_t ÷ corrected DAF assets_{t−1}, with assets of $168.74bn, $234.01bn, $228.14bn and $256.37bn):

| FY | Grant growth, corrected → netted (central) | Contribution growth, corrected → netted | Payout, corrected → netted central [lower–upper] |
|---|---|---|---|
| 2022 | +15.8% → +15.8% | −1.3% → −2.6% | 23.8% → **21.0%** [20.6–21.7%] |
| 2023 | −1.4% → **+3.2%** | −14.5% → −12.5% | 24.0% → **22.3%** [21.9–22.6%] |
| 2024 | +21.2% → **+15.0%** | +41.9% → +38.2% | 25.9% → **22.8%** [22.2–23.2%] |
| 2021 | n/a (FY2020 not netted) | n/a | 28.5% → **25.2%** [24.5–26.0%] |

**Where the netted dollars land (central, by recipient segment):**

| Recipient segment | FY2021 | FY2022 | FY2023 | FY2024 |
|---|---|---|---|---|
| National | $3.98bn | $4.56bn | $3.02bn | $6.73bn |
| Community foundations | $1.15bn | $1.13bn | $0.38bn | $0.57bn |
| DAF-heavy single-issue | $0.35bn | $0.56bn | $0.45bn | $0.66bn |
| Processors | $0.05bn | $0.15bn | $0.20bn | $0.07bn |

**Largest pairs over FY2021–24, central** (directional, not netted against reverse flows):
1. GS DAPF → NPT $1.98bn
2. SVCF → NPT $1.50bn
3. NPT → SVCF $1.20bn
4. Fidelity → DAFgiving360 $0.89bn
5. Fidelity → NPT $0.84bn
6. Jasper Ridge Charitable Fund → DAFgiving360 $0.77bn
7. Fidelity → SVCF $0.70bn
8. BNY Mellon CGF → RCF $0.62bn
9. DAFgiving360 → NPT $0.59bn
10. DAFgiving360 → Fidelity $0.56bn

**Comparison with batch 33.** The batch-33 gross figures ($5.24bn FY2023 and $9.56bn FY2024, all panel grantors to national, processor and CF recipients) sit just above the R5 upper tier ($4.88bn and $9.42bn). The upper tier:
- drops the 15 low-DAF-share national/processor recipients;
- adds DAF-heavy single-issue recipients;
- restricts to the corrected market; and
- applies caps.

### 1.3 The community-foundation check (purpose text) [C/I]
The brief asked for an audit-based check of what share of lines to community foundations lands in DAFs. Schedule I purpose text was classified by `purpose_class` in the script (regex in the script; "explicit DAF" covers DAF, donor-advised, "family fund", successor or close-out wording).

| Recipient segment | Lines | $ | Explicit DAF | Explicit non-DAF | Generic |
|---|---|---|---|---|---|
| Community foundation | 13,141 | $5.56bn | 1.6% | 5.0% | **93.4%** |
| National | 3,951 | $23.39bn | 1.7% | 3.0% | 95.3% |
| Processor | 339 | $0.65bn | 16.6% | 6.9% | 76.4% |
| Single-issue | 16,179 | $5.57bn | 1.3% | 12.0% | 86.7% |
| University/hospital | 12,927 | $10.67bn | 0.9% | **45.2%** | 54.0% |

- **The text cannot settle the CF share** [I]:
  - The large national grantors use boilerplate for every grantee: "Public, societal benefit" (NPT), "For grant recipient's exempt purposes" (Fidelity), "Community & human services" (Vanguard).
  - The only clear contrast is that university and hospital lines are 45% explicitly programme-coded, which supports rule W1.
- **What the central tier uses instead:** each CF recipient's filed DAF share of total assets. The effective central/upper ratio for CF recipients is 54–67%.
- **What remains:** a recipient-side audit read (P-B34A-03). No audited statements were read here.

## 2. P-NPO-04: the recipient whitelist

### 2.1 Rules (one decision per recipient EIN)

| Rule | Test | Decision | EINs | FY2021–24 gross lines |
|---|---|---|---|---|
| W1 | DAFRC subtype "Universities and Healthcare" | exclude | 125 | $10.67bn |
| W2 | National (Standard) or donation processor with DAF share of total assets ≥ 0.50, or no cost-structure row | include | 72 | $23.31bn |
| W2 | National/processor with DAF share < 0.50 | exclude | 15 | $0.73bn |
| W3 | Community foundation | include; weighted by DAF share in the central tier | 767 | $5.56bn |
| W4 | Single-issue or religious with DAF share ≥ 0.50 | include | 90 | $2.70bn |
| W4 | Single-issue or religious with DAF share < 0.50 or no data | exclude | 342 | $2.87bn |
| W5 | Reviewed affiliate pair (below) | excluded from lower and central; included in upper | 9 pairs | $0.17–0.28bn a year after caps |

- **DAF share** is the median over FY2022–25 of Schedule D Part I EOY value ÷ Part X total assets, from `sponsor-cost-structure.csv`. A university with a share above 1 (a unit mismatch in that file, e.g. JHU 8.6) is excluded by W1 regardless.
- **W2 exclusions (largest first):**
  - Rockefeller Philanthropy Advisors (0.07; fiscal sponsor), $439m;
  - Amalgamated Charitable Foundation (0.21), $114m;
  - Edward Charles Foundation (0.05), $64m;
  - GoFundMe.org (0.23), $33m;
  - RSF Social Finance (0.44), $33m;
  - Kiva (0.03), $17m;
  - Social Impact Fund, Impact Charitable, MGM Resorts Foundation and six with under $1m.
- **W4 inclusions (largest first):**
  - NCF (0.95), $660m;
  - Impact Investing Charitable Foundation (0.91), $373m;
  - Jewish Communal Fund (0.96), $314m;
  - Tides Foundation (0.63), $280m;
  - International Generosity Foundation (0.99), $192m;
  - PEF Israel Endowment Funds (0.64), $133m;
  - Christian Community Foundation (0.87), $103m;
  - CJP (0.83), $100m;
  - OJC Fund, Donors Trust, the Jewish community foundations of San Diego and San Francisco, Word of Life, New Horizons and NEMA.
- **W4 exclusions (largest first):**
  - The Nature Conservancy (0.006), $406m;
  - World Vision (0.03), $150m;
  - Myriad USA, $97m;
  - JDC, $82m;
  - Global Impact, $77m;
  - Williams College, $66m;
  - Proteus Fund, Jewish National Fund, Social Good Fund, United Ways and Sierra Club Foundation.
  - These are programme grants or fiscal-sponsorship inflows, not DAF transfers [I].
- **W5 affiliate pairs** (hard-coded in `AFFILIATES`, each reviewed):
  - Dechomai Asset Trust / Dechomai Foundation;
  - Impact Investing Charitable Foundation / Trust;
  - Donors Capital Fund / Donors Trust;
  - NPT Charitable Asset Trust / NPT. The FY2025 NPT Schedule R lists NPT CAT as a controlled supporting organisation, with a $2,356,765 type-C transaction;
  - Ayco Charitable Foundation / GS DAPF (common control and identical boards; merged 2025-07-01 per the Ayco FY2025 Schedule O);
  - Dayton Foundation Depository / The Dayton Foundation;
  - and three same-name two-EIN community foundations (Rochester Area, St Louis, Portland).
  - Name-overlap candidates that were *not* adopted, for lack of evidence of common control, include Community Trust of Utah → The Community Foundation of Utah ($76m) and CF → United Way pairs.

### 2.2 How this replaces the nested tiers
- **Old tiers** (`net-payout-summary.csv`): tier_c (every panel EIN) was $43.5bn over FY2021–24, and tier_b (national + processor + CF) was $27.9bn.
- **New definition:** the whitelist carries $31.57bn of gross lines (W2 + W3 + W4 included).
- **After market restriction, weights and caps** it gives R5 of **$19.1bn (lower), $24.0bn (central) and $28.4bn (upper)** over FY2021–24 [C].
- **Net-payout use:** a sponsor-year's DAF-to-DAF transfers become the sum of its `netted_central` line amounts. The per-recipient totals are in the whitelist CSV.

## 3. P-NPO-03: sponsors whose Schedule I is "see attached"
- **XML check [F]:**
  - [RCF FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543189349301959_public.xml): one RecipientTable row, "See Attached Grant Report", $745,668,528, "Various charitable purposes - detail available upon request", Total501c3OrgCnt 17,290.
  - [BofA CGF FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503219349318170_public.xml): one row, "SEE ATTACHED LIST OF DISTRIBUTIONS C/O BANK OF AMERICA", $969,496,994.
  - Neither return has a supplemental table. The attachment is a binary PDF that TEOS XML does not publish.
- **PDF images (IRS scans of TY2021–22, hosted by ProPublica) [F]:**
  - RCF `352129262_202212_990_2024010322157440`;
  - BofA CGF `046010342_202212_990_2024010322156747`;
  - NY Community Trust `133062214_202212_990_2024010922202159`;
  - Greater Horizons `200849590_202212_990_2024010322164281`;
  - GKCCF `431152398_202212_990_2024010322164453` and `431152398_202112_990_2023051221225288`;
  - Fund for Charitable Giving `043296043_202212_990_2023120522068475` and `043296043_202112_990_2023030221007801`.
  - USCGT and Donors Fund have no TY2021+ image listed.
  - The download endpoint returned HTTP 403 with a "Security Check" page (tested for RCF and BofA). It was not bypassed, so this is a human-retrieval task (P-B34A-02).
- **Size [C/I].** Grantor-years whose Schedule I is not itemised hold $2.07bn, $2.48bn, $2.02bn and $2.56bn of corrected DAF grants (FY2021–24). Applying the itemising sponsors' central R5 rate (7.7–12.6%) gives $0.25bn, $0.30bn, $0.16bn and $0.32bn of transfers that R5 misses, so the central netting is a slight understatement. Inbound transfers *to* RCF, BofA and the others are seen and netted, because they appear on other grantors' Schedule I.
- `net-payout-by-sponsor.csv` was not changed: no transfer line was recovered.

## 4. P-990-03: 2026-filed returns not on the mirror
- **Index:** all 19 `http_404` returns in `form990-returns-schedule-d-harvest.csv` are in [`index_2026.csv`](https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv) (Last-Modified 2026-10-21) with batch label `2026_TEOS_XML_05A`. The mirror still returns 404 for them (checked for Vanguard and NPT CAT).
- **Retrieval:**
  - A stdlib range reader (scratchpad, not in the repo) read the central directories of `2026_TEOS_XML_05A.zip` (521,158,638 bytes) and `05B.zip` (513,423,358 bytes; both Last-Modified 2026-06-17; 84,172 members each).
  - It then fetched only each member's bytes and inflated them with `unzip`; members are Deflate64.
  - **All 19 are in 05B and none in 05A**, which confirms the batch-31 finding that the "05A" label spans both zips.
- **Harvest re-run:**
  - Each XML was parsed with the unchanged extractors of `mission_990_contractors.py` and `mission_net_payout.py`.
  - The extracts were written into a scratch copy of the extract cache, and `mission_990_contractors.py --task contractors` was re-run with `--out-dir` in the scratchpad.
  - Result: 856/856 returns `ok`, FY2025 sponsors parsed **94 → 113**, contractor lines 1,985 → 2,039 [C].
  - The repo harvest files were not overwritten. The table below holds every filled value.

| Sponsor | EIN | Period end | Filed | DAFs | Contributions | Grants | EOY value | DAFRC FY2024 assets | Object id |
|---|---|---|---|---|---|---|---|---|---|
| Vanguard Charitable | 232888152 | 2025-06-30 | 2026-05-12 | 29,305 | 5,751,399,753 | 3,502,746,479 | 27,012,089,382 | 21,949,164,416 | 202621329349306657 |
| Ayco Charitable Foundation | 141782466 | 2025-06-30 | 2026-05-14 | 0 | 408,133,167 | 452,610,491 | 0 | 1,382,785,126 | 202621349349304192 |
| Boston Foundation | 042104021 | 2025-06-30 | 2026-05-06 | 822 | 338,895,561 | 198,697,912 | 1,403,498,082 | 1,097,047,767 | 202641269349301584 |
| Jewish Community Federation of SF | 941156533 | 2025-06-30 | 2026-05-14 | 1,045 | 373,109,911 | 82,742,726 | 1,358,472,342 | 995,207,863 | 202621349349313567 |
| UCLA Foundation | 952250801 | 2025-06-30 | 2026-05-13 | 10 | 290,000 | **−109,807,268** | 526,582,034 | 605,741,214 | 202621339349305882 |
| East Bay CF | 946070996 | 2025-06-30 | 2026-05-15 | 338 | 40,354,980 | 54,195,201 | 376,743,019 | 529,385,653 | 202621359349313177 |
| Orange County CF | 330378778 | 2025-06-30 | 2026-05-13 | 474 | 114,558,192 | 112,297,501 | 502,021,899 | 471,973,737 | 202621339349305742 |
| Yale University | 060646973 | 2025-06-30 | 2026-05-15 | 10 | 1,250,000 | 15,606,765 | 255,888,717 | 246,976,222 | 202641359349303914 |
| Jewish CF of Greater MetroWest NJ | 221714130 | 2025-06-30 | 2026-05-15 | 335 | 31,173,269 | 25,924,552 | 278,011,535 | 228,390,607 | 202631359349308688 |
| Jewish Federation of Cleveland | 340714445 | 2025-06-30 | 2026-05-14 | 783 | 54,672,911 | 40,590,646 | 168,592,332 | 154,510,067 | 202621349349311222 |
| Blue Grass CF | 616053466 | 2025-06-30 | 2026-05-15 | 434 | 14,810,714 | 12,726,478 | 156,361,805 | 133,105,531 | 202631359349309403 |
| Jewish Federation of Greater Washington | 530212445 | 2025-06-30 | 2026-05-13 | 300 | 42,602,637 | 18,727,807 | 160,004,185 | 125,535,550 | 202641339349309439 |
| Central Carolina CF | 570793960 | 2025-06-30 | 2026-05-15 | 252 | 23,940,675 | 15,667,043 | 140,667,009 | 123,581,148 | 202631359349313608 |
| High Point CF | 561695787 | 2025-06-30 | 2026-05-13 | 131 | 12,144,212 | 6,577,371 | 106,810,050 | 92,576,410 | 202641339349305039 |
| American Foundation of Utah | 205823039 | 2025-12-31 | 2026-05-12 | 22 | 5,116 | 2,467,123 | 34,314,795 | 39,248,645 | 202641329349307459 |
| Endaoment | 844661797 | 2025-06-30 | 2026-05-15 | 1,213 | 25,033,424 | 18,679,151 | 18,900,000 | 23,816,741 | 202631359349315978 |
| NPT Charitable Asset Trust | 277059768 | 2025-06-30 | 2026-05-12 | 15 | 48,600,000 | 2,455,265 | 64,634,106 | 17,132,245 | 202631329349305758 |
| First Midwest Charitable Trust | 266654290 | 2025-12-31 | 2026-04-24 | 3 | 162,243 | 9,775,607 | 5,337,980 | 15,443,621 | 202631149349301723 |
| American Foundation for Charitable Support | 860857725 | 2025-12-31 | 2026-05-12 | 33 | 246,342 | 938,774 | 11,671,074 | 11,309,975 | 202631329349307093 |

- **Notes on the filled returns [F]:**
  - **Endaoment** agrees with batch 31 (1,213 DAFs, $18.9m).
  - **UCLA Foundation** files negative DAF grants; treat it as a suspect Part I under the R1–R4 conventions.
  - **Vanguard's** FY2025 Schedule I has 27,221 lines ($3.43bn). Its largest panel recipients are Fidelity $87.3m, RCF $85.2m, National Charitable Endowment $50.0m, DAFgiving360 $46.3m and NPT $31.6m.
- **Ayco merger.**
  - Part IV says the organisation terminated (Schedule N). Schedule O states: "Effective July 1, 2025, the ACF and GS Donor Advised Philanthropy Fund ('GS DAF') merged, and GS DAF is the surviving corporation… The Foundation is filing a final return for the year ended June 30, 2025".
  - Schedule I sends $1,162.2m to GS DAPF, and Schedule D supplemental reads "LINE 4B TRANSFER TO GS DAF: 1,162,195,533".
  - Ayco's Part I grants of $452.6m exclude the transfer, so the grants side is not double counted. Whether GS DAPF books it as FY2025 contributions decides an FY2025 R2 adjustment (P-B34A-01).
  - This is a TY2024 return.
- **NPT Charitable Asset Trust** FY2025: contributions $48.6m against $18,000 in FY2024. Its only panel grantee is NPT ($2.36m).

## 5. P-GPT-01: NPT "PROGRAM FEES" and related lines

### 5.1 Filed values (NPT EIN 23-7825575; [FY2025 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601289349302480_public.xml)) [F]

| Line | FY6/2021 | FY6/2022 | FY6/2023 | FY6/2024 | FY6/2025 |
|---|---|---|---|---|---|
| Part IX line 24 "PROGRAM FEES", total | 3,797,601 | 4,186,508 | 3,741,301 | 4,073,957 | 4,289,911 |
| …program column | −1,700 | 563 | — | 4,077,996 | 4,295,780 |
| …management & general | 3,800,677 | 4,185,944 | 3,741,301 | −2,448 | −3,557 |
| Part VIII "MAINTENANCE & HOSTING (FEES)", code 561000, exempt-function | 1,708,173 | 1,336,202 | 1,399,133 | 784,533 | 480,556 |
| Part VIII "ADMINISTRATIVE FEES" (earlier "MISCELLANEOUS") | 3,507,394 | 2,137,963 | 1,352,315 | 710,557 | 632,700 |
| Part VIII "PHILANTHROPIC CONSULTING" (unrelated; 990-T) | — | — | 109,600 | 161,785 | 144,502 |
| Part IX line 14, information technology | 2,246,126 | 3,167,698 | 3,595,447 | 3,649,680 | 5,871,282 |
| Schedule D Part I EOY DAF value | $15.94bn | $21.52bn | $22.84bn | $42.12bn | $55.90bn |

Object ids: 202231339349309863, 202311359349313966, 202431429349301368, 202511339349301311, 202601289349302480 (FY2021–25). The FY2025 990-T is [202641329339301324](https://apps.irs.gov/pub/epostcard/990/xml/2026/2026_TEOS_XML_05B.zip), from the 05B zip.

### 5.2 What the other public documents add
- **Schedule O (FY2025):** nothing on program fees, hosting or partners. It says NPT "posts its balance sheet and income statement on its website in NPT's annual report" [F].
- **Part III narrative:**
  - The FY2023 return: "partnering with an independent third party to increase the efficiency in which charities received grant funding".
  - FY2024: "a continued partnership".
  - FY2025: the sentence is absent [F].
  - Program fees already ran at $3.8m in FY2021, before that partnership, so the partnership cannot be the whole line [I].
- **Schedule R Part V (FY2025)** [F]:
  - NPT performs services for its supporting organisations (type L): $200,000, $175,000, $175,000, $70,386 and $57,700, $678,086 in total.
  - It receives reimbursements from them (type Q): $2,547,594.
  - No transaction with a for-profit or a partner institution is reported. Schedule R covers related organisations only.
- **[FY2025 consolidated statements](https://www.nptrust.org/wp-content/uploads/2026/09/FY25-AR-Consolidated-Financials-NPT.pdf)** (2 pages, InDesign, created 2026-09-01; linked from the 2025 annual report) [F]:
  - The statement of financial position and statement of activities only; no auditor's report and no notes.
  - "Administrative and maintenance fees" $656k (FY2025) and $994k (FY2024); "Other income" $1,641k and $81k.
  - The four operating-expense labels repeat balance-sheet captions ("Asset management fees payable", "Lease liability", "Grants payable"), so the expense breakdown cannot be read. That is a label error in the published PDF.
  - The consolidated fee line is $457k (FY2025) and $501k (FY2024) below the 990's admin plus hosting revenue [C]. This fits fees charged to consolidated affiliates (supporting organisations, NPT UK, NPT Transatlantic) and eliminated on consolidation [I].
- **Audited statements with notes:** not found in public (request-free) form [U]. The JPM, UBS and BMO Form ADV and fee schedules were not read in this batch.

### 5.3 Reading [I]
1. **"PROGRAM FEES" is a flat cost of about $4m a year.**
   - An asset-linked revenue share paid to private-label institutions would have roughly tripled with DAF assets (×3.5 since FY2021). This line moved +13%.
   - A per-grant processing fee would have tracked grant counts (×1.8). The per-grant cost fell from about $43 to about $27.
   - The pattern fits fixed contracts or licences: programme-delivery vendors, possibly including platform or grant-processing services.
2. **The FY2024 move from Management & General to Program** is a functional-allocation change, not a new cost. It coincides with the jump in reported IT (to $5.87m in FY2025).
3. **"Maintenance & hosting" revenue is a shrinking recharge** ($1.71m → $0.48m). Most of it is probably intra-group (eliminated in the consolidated $656k).
   - That weakens the batch-33 inference that NPT recharges hosting to an *external* counterparty such as partner banks. It does not rule that out.
4. **Ren:** the filings neither include nor exclude Ren in "PROGRAM FEES". The A4 NPT row should stay at "licence or platform vendor, payment line undisclosed".

## 6. Limitations
- **Schedule I coverage.**
  - Only grants above $5,000 are itemised.
  - Sponsors that point to an attachment (§3) are invisible as grantors.
  - The name-matched lines carried over from the cache are kept.
- **Same-FY matching.** A June-FYE grantor's FY2024 line may land in a December-FYE recipient's FY2024 or FY2025. R5 pairs the same FY label on both sides, so timing can shift netting between adjacent years.
- **DAF shares are proxies.**
  - Grantor DAF share of grants and recipient DAF share of total assets come from `sponsor-cost-structure.csv` (FY2022–25 medians, also applied to FY2021).
  - Some rows are implausible (university shares above 1). W1 neutralises those for universities, but similar errors elsewhere would mis-weight a recipient.
- **Whitelist thresholds** (0.50 DAF share) are judgement. Moving them changes W4 by tens of millions a year (Tides 0.63, PEF Israel 0.64, JCF SF 0.63 sit near the line).
- **Affiliates** were identified by name overlap and reviewed by hand. Common control outside that list (e.g. bank-captive families) is not tested.
- **Market denominators** are corrected DAFRC values, and FY2024 still contains unresolved imputations (`dafrc-corrected-market-totals.csv`, `imputed_value_remaining`).
- **No FY2025 netting.** The corrected-totals window ends at FY2024.
- **NPT.** Only public documents were used. Audited notes, partner contracts and Form ADV were not available or not read.

## 7. Source register

| ID | Source | Accessed | Used in |
|---|---|---|---|
| S1 | IRS e-file XML, GivingTuesday mirror `https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml`, via the `netpayout990/` cache (`mission_net_payout.py`) | earlier caches; NPT XMLs 2026-11-15 | §1–3, §5 |
| S2 | IRS TEOS [index_2026.csv](https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv) (Last-Modified 2026-10-21); [2026_TEOS_XML_05A.zip](https://apps.irs.gov/pub/epostcard/990/xml/2026/2026_TEOS_XML_05A.zip) and [05B.zip](https://apps.irs.gov/pub/epostcard/990/xml/2026/2026_TEOS_XML_05B.zip) (Last-Modified 2026-06-17), range reads | 2026-11-15 | §4, §5 |
| S3 | DAFRC 2025 dataset via `dafrc-sponsor-schedule-d-fy2019-2024.csv`; `dafrc-corrections-itemized.csv`; `dafrc-corrected-market-totals.csv` | repo | §1 |
| S4 | `sponsor-cost-structure.csv` (DAF share of assets and of grants) | repo | §1–2 |
| S5 | ProPublica Nonprofit Explorer organisation pages (PDF-image listings) for EINs 352129262, 046010342, 133062214, 200849590, 431152398, 311663020, 474844275, 043296043; download endpoint returned 403 "Security Check" | 2026-11-15 | §3 |
| S6 | NPT [2025 annual report page](https://www.nptrust.org/annual-reports/npt-annual-report/) and [FY25 consolidated financial statements PDF](https://www.nptrust.org/wp-content/uploads/2026/09/FY25-AR-Consolidated-Financials-NPT.pdf) | 2026-11-15 | §5 |
| S7 | Repo reports: queue-batch33-panel-scans.md §4 and wave-18 corrections; queue-batch31-filings-feeds.md §1 and wave-16 corrections; queue-npt-givingpoint-fidelity-stack.md §4 | repo | context |

## 8. Data dictionary

### `dafrc-market-totals-netted.csv` (one row per FY × metric × tier; FY2021–24)

| Column | Meaning |
|---|---|
| fiscal_year, metric | FY (DAFRC convention); `daf_grants` or `daf_contributions` |
| tier | `lower`, `central` or `upper` (§1.1) |
| corrected_value | Corrected DAFRC total (`dafrc-corrected-market-totals.csv`, rules R1–R4) |
| r5_netting_amount | Weighted, capped sponsor-to-sponsor amount N. The same N is subtracted from grants and contributions |
| netted_value | corrected_value − r5_netting_amount |
| netting_share_of_corrected | N ÷ corrected_value |
| weighted_before_caps | N before grantor and recipient caps |
| gross_lines_in_tier | Unweighted Schedule I $ of the lines in the tier (after the market-membership test) |
| lines, grantors, recipients | Counts of netted lines and distinct EINs |
| yoy_growth_corrected, yoy_growth_netted | Year-on-year growth. Blank for FY2021 (FY2020 not netted) |
| all_panel_lines_gross | All Schedule I $ from panel grantors to any other panel EIN in that FY (whitelist not applied) |
| grantor_daf_grants_no_parsed_return | Corrected DAF grants of panel sponsor-years with no parsed return in the cache |
| grantor_daf_grants_sched_i_not_itemised | Corrected DAF grants of sponsor-years whose Schedule I points to an attachment (§3) |
| sources | Provenance |

### `daf-to-daf-recipient-whitelist.csv` (one row per recipient EIN receiving lines from another panel sponsor, FY2021–24)

| Column | Meaning |
|---|---|
| recipient_ein, recipient_name, dafrc_type, dafrc_subtype, segment | DAFRC panel identity. Segment as in `mission_net_payout.segment_of` |
| daf_share_of_total_assets, daf_share_of_grants, cost_structure_fys | Medians from `sponsor-cost-structure.csv` and the FYs used. Blank means no row |
| decision, rule, reason | `include`/`exclude`; W1–W4; text reason with the share used |
| affiliate_pairs | W5 pair descriptions involving this recipient |
| inbound_lines_fy2021_2024, inbound_grantors, inbound_gross_fy2021_2024, inbound_gross_fy2021..fy2024 | Unweighted inbound Schedule I lines from panel grantors |
| purpose_explicit_daf_usd, purpose_explicit_non_daf_usd | Inbound $ whose purpose text is explicitly DAF or non-DAF (§1.3) |
| netted_lower/central/upper_fy2021_2024 | Inbound amount netted by R5 in each tier |
| source | Provenance |

### `queue-proposals-batch34a.csv`
- Columns and scales follow [queue-proposals-README.md](../../data/mission-2026-11-14/queue-proposals-README.md).
- IDs are P-B34A-01..03.

## 9. Reproduction
```
python3 scripts/mission_market_netting.py --np-cache NPCACHE      # NPCACHE holds netpayout990/ (mission_net_payout.py)
```
- The script prints a JSON summary covering:
  - the corrected-totals rebuild check;
  - decisions by rule;
  - segment default shares;
  - the purpose audit;
  - netted amounts by recipient segment;
  - affiliate amounts in the upper tier;
  - the top central pairs.
- Every §1–2 figure comes from that summary or from the two CSVs.
- §4 used a one-off stdlib zip range reader (central directory, then a member byte range, then `unzip -p` for Deflate64). Its output was parsed with the repo extractors `mission_990_contractors.extract_stream` and `mission_net_payout.extract_stream`, then fed to `python3 scripts/mission_990_contractors.py --irs-dir IRS --cache-dir SCRATCHCACHE --task contractors --out-dir SCRATCH`.
