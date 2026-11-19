# P-GAP19-01: FY2025 filing refresh for the 1,512 DAFRC sponsors (league table, DAF-to-DAF netting, Ren/Stellar footprint)

**Date:** 2026-11-19 · **Queue item:** P-GAP19-01 (`data/mission-2026-11-14/research-priority-queue.csv`) · **Workstream:** G01

**Outputs** (all new `-fy2025-refresh` files; no existing output was overwritten)
- [`data/mission-2026-11-14/form990-harvest-fy2025-refresh.csv`](../../data/mission-2026-11-14/form990-harvest-fy2025-refresh.csv): 977 rows, one per FY2025 Form 990 now in the IRS index for the 1,512 sponsors (974 EINs).
- [`data/mission-2026-11-14/daf-sponsor-league-table-fy2025-refresh.csv`](../../data/mission-2026-11-14/daf-sponsor-league-table-fy2025-refresh.csv): 56 FY2025 rows (the FY2024 top 50, filed or not, plus six provisional entrants), with FY2025 R5 attribution and a change column against the as-built table.
- [`data/mission-2026-11-14/daf-concentration-fy2025-refresh.csv`](../../data/mission-2026-11-14/daf-concentration-fy2025-refresh.csv): 10 rows. FY2025 CRn/HHI over covered filers, gross and R5-netted.
- [`data/mission-2026-11-14/dafrc-market-totals-netted-fy2025-refresh.csv`](../../data/mission-2026-11-14/dafrc-market-totals-netted-fy2025-refresh.csv): 6 rows. FY2025 R5 over covered filers, three tiers.
- [`data/mission-2026-11-14/form990-contractors-fy2025-refresh.csv`](../../data/mission-2026-11-14/form990-contractors-fy2025-refresh.csv): 1,066 FY2025 Part VII-B lines.
- [`data/mission-2026-11-14/vendor-footprint-990-fy2025-refresh.csv`](../../data/mission-2026-11-14/vendor-footprint-990-fy2025-refresh.csv): 21 DAF-relevant vendor groups, FY2025 against FY2024.
- [`data/mission-2026-11-14/queue-proposals-g01.csv`](../../data/mission-2026-11-14/queue-proposals-g01.csv): P-G01-01 to P-G01-03.
- **Script** (stdlib, functional style): [`scripts/mission_fy2025_refresh.py`](../../scripts/mission_fy2025_refresh.py). It imports the parsing, league-table, netting and vendor functions of `mission_990_contractors.py`, `mission_net_payout.py`, `mission_league_table.py` and `mission_market_netting.py` unchanged.

**Rules applied**
- **Governing corrections read first:**
  - [direction-league-table-concentration.md](direction-league-table-concentration.md), including wave 29. The NPT FY2023 anomaly is outside FY2025.
  - [queue-batch34-netting-filings.md](queue-batch34-netting-filings.md): the R5 rule, the W1–W5 whitelist and the tier weights are used unchanged.
  - [full-universe-990-harvest-and-corrected-totals.md](full-universe-990-harvest-and-corrected-totals.md), waves 5 and 19. Wave 5 defines the "latest parsed return" Ren measure used in §4.2.
  - [vendor-footprint-990-harvest.md](vendor-footprint-990-harvest.md): Ren grouping and the Indianapolis address guard.
  - [queue-ren-iphi-attrition.md](queue-ren-iphi-attrition.md), wave 11 and the crt.sh compliance note. No crt.sh data was used here. One crt.sh-only lead is now backed by a filing (§4.3).
  - [queue-batch35-panel-screens.md](queue-batch35-panel-screens.md), wave 20: the 144 TEOS fill rows and the Fidelity/Vanguard FY2025 counterpart lines.
- **Fiscal year (FY)** is the calendar year in which the tax period ends (DAFRC convention). "FY2025" therefore mixes TY2024 June-FYE returns (Fidelity, NPT, DAFgiving360, Vanguard) with TY2025 calendar-year returns.
- **Labels:** **[F]** filed value; **[C]** script computation; **[I]** inference.
- **No extrapolation.** Every FY2025 figure is a filed value or a sum over covered filers. No missing sponsor is imputed, and no covered-only ratio is presented as a market figure.
- **Access:** I checked robots.txt first. apps.irs.gov has none (the request redirects to a 404 page), and the GivingTuesday S3 bucket has none (NoSuchKey).
  - I used only the IRS TEOS index CSVs and two monthly TEOS zips, downloaded whole and deleted after extraction, plus the GivingTuesday per-object mirror.
  - No crt.sh, ProPublica downloads, logins, forms or outreach were used.
- **This is research, not legal or tax advice.**

---

## 0. Answers in brief

| Question | Answer | Confidence |
|---|---|---|
| **New returns since the as-built harvest** | **76 new FY2025 returns** [F]:<br>- **75 from sponsors that had no FY2025 return before.** They are 51 community foundations, 21 single-issue sponsors and 3 nationals (Fiduciary Charitable Foundation $149.1m; Impact Charitable $14.7m; DonateStock, which leaves the value blank).<br>- **One supersedes an earlier return:** Fidelity Charitable's *amended* FY6/2025 return (AmendedReturnInd X, submitted 2026-10-14). Its Schedule D and Part VII-B are identical to the original.<br>- All 76 are in the new IRS batch `2026_TEOS_XML_10A`, added to `index_2026.csv` on 2026-11-18. They were submitted between 2026-09-25 and 2026-10-22, and none is on the GivingTuesday mirror yet (HTTP 404).<br>- 73 of the 75 new sponsors close in December 2025. Together they hold $1.53bn of FY2025 DAF assets (filed) against $1.47bn of FY2024 corrected assets. The largest are Baltimore CF ($204.5m), Fiduciary ($149.1m) and Lancaster County CF ($132.5m). | High [F] |
| **FY2025 coverage** | **974 sponsors** have a parsed FY2025 return, up from 899 [C]:<br>- they hold **68.0% of FY2024 corrected assets**, up from 67.6%, and 62.7% of grants, up from 62.4%;<br>- **24 of the FY2024 top 50** are covered (unchanged), holding 70.6% of top-50 assets.<br>- **All 977 located returns parse.** 757 come from the mirror and 220 from TEOS zip members (144 from 05B, 76 from 10A). The 901 returns parsed before reproduce their Schedule D Part I values exactly. | High [C] |
| **Top-50 returns still missing** | **26, all because they are not in the IRS index yet. None is held back by mirror lag** [F]:<br>- GS DAPF, SVCF, MS GIFT, AEF, RCF, NCF, BofA CGF, ImpactAssets, FFTC, GKCCF, Greater Horizons, Dechomai Asset Trust, NY Community Trust, Columbus, Donors Trust, US Charitable Gift Trust, Oregon CF, "The Community Foundation for Greater …" (EIN 58-1344646), Bessemer Giving Fund, Greater Houston CF, Signatry, CF of New Jersey, Denver Foundation, JCF Los Angeles, Tulsa CF and American Gift Fund.<br>- Every one is a December filer whose latest indexed return is FY2024, which arrived in batches `2025_TEOS_XML_11A–11D`. Their FY2025 returns were due on 2026-11-16 and fall after the 10A cut-off.<br>- The six covered top-50 returns that exist only in TEOS zips are Fidelity (amended), Vanguard, Ayco, Boston Foundation, JCF of San Francisco and UCLA Foundation. All six were parsed from the zips. | High [F] |
| **League table: what changes** | **Nothing in the top 50** [C]:<br>- The same 24 filed, 26 not yet filed, 6 provisional entrants and 1 confirmed exit (Ayco merger).<br>- The only row-level change is Fidelity's superseding amended return, which carries the same values.<br>- Filed FY2025 leaders are unchanged: Fidelity **$85.48bn**, NPT **$55.90bn**, DAFgiving360 **$47.35bn**, Vanguard **$27.01bn** [F].<br>- The 75 new filers are all small. The largest ranks #120 on FY2024 assets, so none crosses the FY2024 rank-50 value of $581.1m. | High |
| **FY2025 concentration (covered filers only)** | **Assets:** CR5 **82.4%**, HHI **1,885**, against 82.9% and 1,906 as built. **Grants:** CR5 75.9%, HHI 1,647. **Contributions:** CR5 81.6%, HHI 1,995 [C].<br>- These ratios fall slightly only because small filers enlarge the denominator.<br>- **They are not comparable with the FY2021–24 market series** (FY2024 assets: CR5 56.9%, HHI 853). The covered set has the four largest sponsors but not ranks 5–11 of FY2024. | High [C]; not a market figure |
| **DAF-to-DAF netting, FY2025 (new)** | **R5 over covered filers is $3.05bn lower, $3.38bn central and $3.80bn upper: 6.4%, 7.1% and 8.0% of the $47.65bn of covered FY2025 DAF grants** (4.1%, 4.6% and 5.1% of covered contributions) [C].<br>- **The central rate is lower than FY2024's 12.1% because of coverage, not behaviour.** The membership test drops $2.20bn of central-weighted lines whose recipient has not filed yet: RCF $342m, SVCF $324m, ImpactAssets $292m, GS DAPF $202m, Signatry $194m and others.<br>- **Largest central pairs:**<br>  - DAFgiving360 → Fidelity **$967.1m**, from one filed line of $976.6m, against $121–129m a year in FY2022–24 (P-G01-02);<br>  - Fidelity → Vanguard $473.5m;<br>  - Fidelity → NPT $344.1m;<br>  - NPT → Fidelity $282.2m.<br>- **Netted grants concentration (covered):** CR5 75.9% gross → 74.7% central, HHI 1,647 → 1,593. As in FY2021–24, netting moves the shape only slightly. | High on lines [F]; tier weights [I]; covered-only |
| **Ren/Stellar footprint, FY2025** | **No Ren attrition is visible in the FY2025 filings so far** [F/C]:<br>- 10 sponsors name a Ren entity in an FY2025 return ($3.35m), against 9 ($3.12m) in the as-built FY2025 lines. The addition is Ayco's final return: Stellar, $223,523.<br>- All 8 FY2024 Ren payers whose FY2025 return is parsed name Ren again.<br>- Rising lines: Stifel ($498k → **$801k**, "ops system & service"), Thrivent ($270k → $479k, Renaissance Acquisition Co), Christian Community Foundation ($295k → $366k) and Goldman Sachs Charitable Gift Fund ($139k → $173k).<br>- The big-ticket Ren clients have not filed FY2025: MS GIFT ($14.93m in FY2024), RCF ($19.23m), US Charitable Gift Trust ($4.43m) and NCF ($2.50m).<br>- **Wave-5 "latest parsed return" measure:** 18 → **19 sponsors**, $30.18bn → **$31.56bn** of DAFRC FY2024 assets (9.2% → 9.6%). On corrected FY2024 assets it is $30.58bn, 9.5%. The +1 is Ayco, which merged into GS DAPF on 2025-07-01, so it is not a live client.<br>- Any-year reach is unchanged: 30 sponsors, $48.55bn DAFRC (14.8%). | High [F]; reach is a floor |
| **Give Interactive, Foundation Source, Foundant** | **Give Interactive:** one new filed payer, **Kalamazoo Community Foundation**, CY2025, "technology/software consultation", **$416,932**, Overland Park KS [F]. Until now this link rested on a crt.sh-only lead.<br>**Vanguard's FY6/2025 return has no Give Interactive line.** The contract was announced on 2025-11-04, after that period, so the first Part VII-B test is the FY6/2026 return. Vanguard's FY2025 lines are UST Global ($4.07m + $2.12m), Slalom, Vanguard Group and Salesforce.<br>**Foundation Source:** still no line.<br>**Foundant:** no FY2025 line. None of its 3 FY2024 payers has an FY2025 return yet. | High [F] |
| **Daffy** | **Not testable.** Daffy Charitable Fund (EIN 86-3177440) has no FY2025 return in the index, so its self-reported $2bn cannot be checked against Schedule D yet [F]. | High |

---

## 1. Method

### 1.1 Locating FY2025 returns
- **Universe:** the 1,512 FY2024 DAFRC sponsors, `select_targets(rows, 0)`.
- **Index files:**
  - [index_2025.csv](https://apps.irs.gov/pub/epostcard/990/xml/2025/index_2025.csv): Last-Modified 2026-01-21, unchanged since the as-built run.
  - [index_2026.csv](https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv): Last-Modified **2026-11-18**, against 2026-10-21 as built. It has 516,019 rows against 472,357, and adds batch `2026_TEOS_XML_10A` with 43,662 rows.
- **Selection:** returns with RETURN_TYPE 990 whose TAX_PERIOD ends in 2025. One return per tax period, the newest OBJECT_ID (`mission_990_contractors.latest_per_period`).
- **Result:** 977 returns for 974 EINs. Three EINs have two FY2025 periods (short years). As in the league table, `fy2025_filed` keeps the latest submission per EIN.

### 1.2 Fetching and parsing
- **Each return is read once.** The XML goes to a temporary file and is parsed by two extractors:
  - `mission_990_contractors.extract_stream`: header, Part VII-B, Part IV, Part IX and Schedule D;
  - `mission_net_payout.extract_stream(full=True)`: every Schedule I Part II line to a DAFRC panel EIN, plus totals and the top 25 lines.
- **Sources:**
  - **GivingTuesday mirror:** 757 returns.
  - **HTTP 404:** 220 returns, fetched instead from the IRS monthly zips.
    - [`2026_TEOS_XML_05B.zip`](https://apps.irs.gov/pub/epostcard/990/xml/2026/2026_TEOS_XML_05B.zip) (513.4 MB; index label "05A") held 144 members.
    - [`2026_TEOS_XML_10A.zip`](https://apps.irs.gov/pub/epostcard/990/xml/2026/2026_TEOS_XML_10A.zip) (258.9 MB; Last-Modified 2026-11-18) held 76 members.
    - Both zips were downloaded whole, the needed members extracted with `unzip`, and the zips then deleted.
- **Check [C]:** the 901 returns that were parsed before (757 mirror rows plus 144 fill rows) reproduce their Schedule D Part I count, contributions, grants and year-end value exactly (`prior_values_check = match`).

### 1.3 League table and concentration
- **League table:** `mission_league_table.build()` is run twice, unchanged:
  - with the refreshed returns (`harvest = refresh rows`, `fill = ()`);
  - with the as-built inputs (`harvest-full` + `2026-fill`).
- **The as-built run reproduces the published FY2025 rows.** The only difference is the rank of Ayco, a $0 filer, which shifts as more filers rank ahead of it.
- **The corrected-totals rebuild check passes** (20/20 cells).
- **FY2021–24 rows are unchanged.** They are not repeated in the refresh file; use `daf-sponsor-league-table-fy2021-2025.csv`.
- **FY2025 shares, ranks and CRs** are over covered filers only (`fy2025_filed_covered_total_only`). This is the same convention as the as-built §4.3.

### 1.4 FY2025 R5 netting (new; covered filers only)
- **Rule implementation:** the batch-34 functions of `mission_market_netting.py`, unchanged: `recipient_decision` (W1–W4), `weights` (lower/central/upper with W5 affiliates), `capped`, `cost_shares` and the segment defaults.
- **Lines:** they come from `mission_daf_to_daf.pick_returns` over the refreshed `netpayout990` cache, with `FYS` set to (2025,).
- **The one necessary substitution:** there are no corrected (R1–R4) FY2025 values. The market-membership test and the grantor and recipient caps therefore use **filed FY2025 Schedule D grants and contributions of covered filers**.
- **Consequences** (both kept visible, not estimated away):
  - A line to a recipient without an FY2025 return is not netted. The amount is reported as `central_weighted_lines_to_recipients_not_yet_filed`, $2.20bn.
  - A grantor without an FY2025 return contributes no lines.
- **Attribution:** as in the league table, outbound R5 is attributed to the grantor (netted grants) and inbound R5 to the recipient (netted contributions).

### 1.5 Vendor screen
- **Normaliser:** FY2025 Part VII-B lines go through the repository normaliser `normalize_vendor`, unchanged, including the Indianapolis address guard for bare "Renaissance" and "Stellar".
- **Comparisons:**
  - **FY2024:** `form990-contractors-harvest-full.csv`.
  - **As-built FY2025 lines:** the same file. Its 801 FY2025 lines come from mirror-parsed returns only, because the 144 fill returns' lines were never written to the repository.
- **Asset reach:** paying sponsors' FY2024 corrected assets (R1–R4). The DAFRC figure is also given for comparability with wave 5.
- **"Latest parsed return" (wave 5):** a sponsor counts if a Ren entity appears in its newest parsed FY2022–25 return.

---

## 2. Coverage

| Measure | As built (index 2026-10-21 + 2026 fill) | Refresh (index 2026-11-18) |
|---|---|---|
| FY2025 returns located / parsed | 902 / 902 | **977 / 977** |
| Sponsors with a parsed FY2025 return | 899 | **974** |
| Share of FY2024 corrected assets covered | 67.6% | **68.0%** |
| Share of FY2024 corrected grants covered | 62.4% | 62.7% |
| FY2024 top 50 with FY2025 return | 24 (70.6% of top-50 assets) | **24 (70.6%)** |
| Covered FY2025 filed DAF assets / contributions / grants | $265.75bn / $73.79bn / $47.40bn | $267.28bn / $74.17bn / $47.65bn |
| Covered accounts (after the plausibility screen) | 1,242,711 | 1,246,924 |
| FY2025 Part VII-B lines | 801 (mirror returns only) | **1,066** (316 returns list ≥1) |

- **Accounts screen:** the same two filers are blanked as before, California Home for the Aged and Communities in Schools Gulf South.
- **Period mix of the 977 returns:**
  - 443 end in June 2025;
  - 367 end in December 2025;
  - 167 end in other months.
- **What the refresh did not reach.** Calendar-year returns submitted between 2026-10-23 and the 2026-11-16 extended deadline are not in the index yet. These are the 26 top-50 sponsors and most remaining December filers.
  - Every one of the 26 filed its FY2024 return in the November 2025 batches (`2025_TEOS_XML_11A–11D`).
  - Their FY2025 returns can be expected in the corresponding 2026 batches [I]. The publication date is not announced. Proposal P-G01-01 re-runs the refresh when they appear.

## 3. Results: league table, concentration and netting

### 3.1 FY2025 filed top 10 among covered filers (not a market ranking)

| Filer rank | Sponsor | FY2025 assets [F] | Grants [F] | Grant share of covered, gross → netted central [C] |
|---|---|---|---|---|
| 1 | Fidelity Charitable | $85.48bn | $15.25bn | 32.0% → 31.8% |
| 2 | National Philanthropic Trust | $55.90bn | $6.42bn | 13.5% → 13.3% |
| 3 | DAFgiving360 | $47.35bn | $8.87bn | 18.6% → **17.3%** |
| 4 | Vanguard Charitable | $27.01bn | $3.50bn | 7.4% → 7.5% |
| 5 | Chicago Community Trust | $4.44bn | $1.10bn | 2.3% → 2.4% |
| 6 | Jewish Communal Fund | $3.41bn | $1.02bn | 2.1% → 2.3% |
| 7 | Raymond James Charitable | $2.32bn | $0.46bn | 1.0% → 0.9% |
| 8 | CJP Greater Boston | $2.15bn | $0.23bn | 0.5% → 0.5% |
| 9 | Boston Foundation | $1.40bn | $0.20bn | 0.4% → 0.4% |
| 10 | Jewish Community Federation of SF | $1.36bn | $0.08bn | 0.2% → 0.2% |

- **Same-sponsor change for the 24 covered top-50 sponsors** (unchanged from as built): assets $194.99bn → $240.14bn (+23.2%), contributions +26.9%, grants +16.0% [C].
- **Churn:** 6 provisional entrants (Independent Charitable Gift Fund, Stifel, Christian Community Foundation, Goldman Sachs Charitable Gift Fund, JCF San Diego, Communities Foundation of Texas). There is 1 exit (Ayco, merger).

### 3.2 Concentration, FY2025 covered filers

| Metric · basis | Covered total | CR1 | CR3 | CR5 | CR10 | CR50 | HHI | As-built CR5 / HHI |
|---|---|---|---|---|---|---|---|---|
| Assets · gross | $267.28bn | 32.0% | 70.6% | 82.4% | 86.4% | 94.2% | 1,885 | 82.9% / 1,906 |
| Contributions · gross | $74.17bn | 35.7% | 71.1% | 81.6% | 88.5% | 96.1% | 1,995 | 82.0% / 2,016 |
| Grants · gross | $47.65bn | 32.0% | 64.1% | 75.9% | 84.4% | 94.8% | 1,647 | 76.3% / 1,664 |
| Grants · R5 central | $44.27bn | 31.8% | 62.5% | 74.7% | 83.8% | 94.5% | 1,593 | n/a (new) |
| Contributions · R5 central | $70.80bn | 35.3% | 71.2% | 81.5% | 88.3% | 96.0% | 1,981 | n/a (new) |

These are shares of covered filers. The FY2021–24 market series, for example FY2024 assets CR5 56.9% and HHI 853, is the only market concentration measure in the repository. **No FY2025 market CR or HHI is reported.**

### 3.3 FY2025 R5 netting (covered filers)

| Tier | R5 amount | % of covered grants ($47.65bn) | % of covered contributions ($74.17bn) | Lines | Grantors | Recipients |
|---|---|---|---|---|---|---|
| Lower | $3.05bn | 6.4% | 4.1% | 305 | 119 | 21 |
| **Central** | **$3.38bn** | **7.1%** | **4.6%** | 2,122 | 258 | 417 |
| Upper | $3.80bn | 8.0% | 5.1% | 2,131 | 260 | 417 |

- **Schedule I lines to any panel EIN:** $11.15bn gross, before the whitelist.
- **Central R5 by recipient segment:** national $2.91bn; community foundations $0.21bn; DAF-heavy single-issue $0.18bn; processors $0.07bn.
- **Not netted because the recipient has not filed FY2025:** $2.20bn central-weighted. The largest recipients are RCF $342m, SVCF $324m, ImpactAssets $292m, GS DAPF $202m, Signatry $194m, AEF $129m, MS GIFT $114m and NCF $77m.
- **Attachment-only Schedule I grantors:** $96.4m of FY2025 DAF grants whose outflows R5 cannot see.
- **Top central pairs** [F lines, C weights]:
  1. DAFgiving360 → Fidelity $967.1m. The filed line is $976,570,217, "Public, societal benefit", object 202611199349300601. The same pair was $129.1m, $120.9m and $127.7m in FY2022–24.
  2. Fidelity → Vanguard $473.5m (filed $480.1m; batch 35).
  3. Fidelity → NPT $344.1m.
  4. NPT → Fidelity $282.2m.
  5. DAFgiving360 → NPT $160.8m.
  6. Fidelity → DAFgiving360 $116.9m.
  7. NPT → Jewish Communal Fund $87.8m.
  8. Vanguard → Fidelity $86.4m.
  9. Fidelity → AOGF $65.2m.
  10. NPT → Los Altos Mountain View CF $50.7m.
- **Reading [I]:**
  - The covered-set central rate (7.1%) is a lower bound for FY2025, not a trend against FY2024 (12.1%). The missing recipients and grantors include the largest DAF-to-DAF counterparties: GS DAPF, SVCF and RCF.
  - A single FY2025 line (DAFgiving360 → Fidelity) is 29% of covered central R5. That makes FY2025 netting unusually sensitive to one transfer (P-G01-02).

## 4. Results: vendor footprint from Part VII-B

### 4.1 DAF-relevant vendors, FY2025 refresh against FY2024 (source: `vendor-footprint-990-fy2025-refresh.csv`)

| Vendor | FY2025 sponsors (refresh / as built) | FY2025 Σ comp. | FY2024 sponsors · Σ comp. | FY2024 payers with FY2025 parsed → named again |
|---|---|---|---|---|
| **Ren (incl. Stellar/iPhi)** | **10 / 9** | $3.35m | 17 · $44.66m | 8 → **8** |
| Blackbaud | 7 / 3 | $2.21m | 7 · $2.05m | 3 → 3 |
| Salesforce | 3 / 2 | $1.97m | 2 · $3.04m | 1 → 1 |
| Stripe | 2 / 1 | $1.78m | 1 · $0.44m | 1 → 1 |
| Mightycause | 2 / 1 | $0.98m | 3 · $3.99m | 1 → 1 |
| PayPal | 2 / 1 | $0.84m | 2 · $1.05m | 1 → 1 |
| Benevity (AOGF) | 1 / 1 | $54.45m | 1 · $45.97m | 1 → 1 |
| Bonterra (CyberGrants) | 1 / 1 | $8.29m | 2 · $7.90m | 1 → 1 |
| CAF America (GS Gives) | 1 / 1 | $0.88m | 1 · $0.31m | 1 → 1 |
| **Give Interactive** | **1 / 0** (Kalamazoo CF) | $0.42m | 0 | – |
| Northeast Retirement Services | 1 / 1 | $0.12m | 1 · $0.11m | 1 → 1 |
| Gloo (Servant Foundation) | 0 / 0 | – | 1 · $14.00m | 1 → **0** |
| Foundant Technologies | 0 / 0 | – | 3 · $0.69m | 0 parsed |
| NPact (AEF), TIFIN (GiveClear), Charitable Solutions (Dechomai) | 0 / 0 | – | 1 each | 0 parsed |
| Foundation Source, CSuite, Chariot | 0 / 0 | – | 0 | – |

The FY2025 and FY2024 columns cover different sponsor sets, so the compensation totals are **not** a trend. Only the last column is a like-for-like comparison.

**The one like-for-like drop is Gloo at Servant Foundation.** Its FY3/2025 return lists no Gloo line, against $14.0m in FY2024. Its top five now begin with Haven Creative Hub LLC, "creative services: advertising and promotions", $36.57m [F]. The fifth-listed payee received $795,757. So any Gloo payment booked as independent-contractor compensation in FY3/2025 was below that amount, or the cost was booked elsewhere [C/I]. That is a large drop or a reclassification, not proof that the relationship ended.

### 4.2 Ren payers (FY2022–25 lines; full panel in the run summary)
- **Named in an FY2025 return [F]:**
  - Stifel Charitable: $801,302, "ops system & service". It was $179k, $234k and $498k in FY2022–24.
  - Thrivent: $479,172 (Renaissance Acquisition Co).
  - Christian Community Foundation (WaterStone): $366,469.
  - T. Rowe Price Program: $259,797.
  - Ayco: $223,523, Stellar, final return.
  - Community Foundation of Greater Memphis (EIN 58-1723645): $203,119, Stellar Technology Solutions LLC, \"software\" [V wave 31A].
  - Greater Green Bay CF: $185,735, Stellar, "ERP system provider".
  - Goldman Sachs Charitable Gift Fund: $172,604.
  - Jewish Federation of Greater Seattle: $155,909.
  - Jewish Federation of Greater Philadelphia (EIN 23-1500085): $500,842, Renaissance Administration [V wave 31A].
- **Ren payers whose FY2025 return is not yet indexed:** MS GIFT, RCF, NCF, ImpactAssets, US Charitable Gift Trust, Cleveland Foundation, CF of Greater Des Moines, CF of Acadiana, Catholic Community Foundation (EIN 38-3941057), GS DAPF (Stellar FY2022 only), Bradley Impact Fund, Baton Rouge Area Foundation, RSF Social Finance and CF of Greater Flint.
- **Parsed FY2025 returns with no Ren line:** Jewish Communal Fund, Servant Foundation, Arkansas CF, "Jewish Federation of Metropolitan …" (EIN 36-2167761), Greater Miami Jewish Federation and Southwest Florida CF. **None of these named Ren in FY2024 either**, so they are not new FY2025 attrition.
- **Measures:**

| Measure | As built (wave 5) | Refresh |
|---|---|---|
| Sponsors naming Ren in any FY2022–25 return | 30 ($48.55bn DAFRC; 14.8%) | 30 ($48.55bn DAFRC; $48.37bn corrected, 15.0%) |
| Sponsors naming Ren in their latest parsed return | 18 ($30.18bn DAFRC; 9.2%) | **19** ($31.56bn DAFRC, 9.6%; $30.58bn corrected, 9.5%) |

- **Why the +1 should be discounted [I]:** it is Ayco, whose latest return is now its final FY6/2025 return, which names Stellar. Ayco merged into GS DAPF on 2025-07-01. GS DAPF's own Stellar line appears only in FY2022.
- **The live-client measure is therefore effectively unchanged.** It remains a floor (top five contractors over $100k only).

### 4.3 Named checks
- **Kalamazoo Community Foundation → Give Interactive** [F]: "TECHNOLOGY/SOFTWARE CONSULTATION", $416,932, CY2025. Source: [990, TEOS 10A member 202622939349301622](https://apps.irs.gov/pub/epostcard/990/xml/2026/2026_TEOS_XML_10A.zip).
  - The repository had this link only as a crt.sh tenant label in `cf-vendor-map-signals.csv`, downgraded by the compliance note. It is now a filed fact.
  - The same sponsor is mapped to Foundation Cloud (EI070) and Blackbaud NXT (EK032), so which systems Give Interactive covers there is open (P-G01-03).
- **Other crt.sh-only Give Interactive leads have parsed FY2025 returns without a Give Interactive line** (Chicago Community Trust, Minneapolis Foundation, East Bay CF and San Diego Foundation). Part VII-B shows only the top five contractors over $100k, so this is not evidence of absence.
- **Vanguard Charitable FY6/2025:** no Give Interactive line, as expected, because the contract dates from 2025-11-04. Vanguard remains the P-990-07 watch item for the FY6/2026 return.
- **Foundation Source:** still no Part VII-B line at any sponsor.
- **Foundant:** no FY2025 evidence yet.

## 5. Changes against earlier repository figures

| Item | Earlier | Now | Effect |
|---|---|---|---|
| FY2025 sponsors parsed | 899 (direction-league-table §4.3) | **974** | +75 small December filers |
| FY2025 coverage of FY2024 corrected assets / grants | 67.6% / 62.4% | 68.0% / 62.7% | +0.4 pt / +0.3 pt |
| FY2024 top 50 with FY2025 return | 24 of 50 | 24 of 50 | none; all 26 missing are unindexed, not unmirrored |
| Covered-filer assets CR5 / HHI | 82.9% / 1,906 | 82.4% / 1,885 | denominator effect only |
| Fidelity FY2025 return | original 202601389349301700 | amended 202622879349301322 | same Schedule D and Part VII-B values |
| FY2025 R5 netting | none ("No FY2025 netting", batch 34 §6) | $3.05/3.38/3.80bn, covered filers only | new, partial by construction |
| FY2025 Part VII-B lines | 801 | 1,066 | adds the 144 fill and 76 new returns |
| Ren, latest-return measure (wave 5) | 18 sponsors, $30.18bn | 19 sponsors, $31.56bn | Ayco final return; not a live client |
| Give Interactive filed payers | 1 (FFTC, FY2023) | 2 (adds Kalamazoo CF, CY2025) | a crt.sh-only lead becomes a filed fact |
| Servant Foundation–Gloo (Part VII-B) | $14.0m (FY2024) | no line in FY3/2025; fifth-listed payee $795,757 | Gloo payment below $0.8m or booked elsewhere |

**Nothing in the FY2021–24 league table, concentration or netting series changes.** Their inputs are untouched.

## 6. Limitations
- **The index cut-off is not the filing deadline.** `index_2026.csv` (2026-11-18) holds submissions up to 2026-10-22, so most calendar-year FY2025 returns, including 26 of the top 50, are absent. **All FY2025 figures are covered-filer figures.**
- **FY2025 values are filed and uncorrected.** No R1–R4 pass exists for FY2025. Known suspect rows are kept as filed:
  - UCLA Foundation's negative grants;
  - Armstrong County CF, which files $10.3m against a FY2024 corrected value of $148.2m (already flagged in the full-universe report).
- **The Ayco/GS DAPF R2 question** (P-B35A-03) is unresolved until GS DAPF's CY2025 return is indexed.
- **FY2025 R5 substitutes filed covered values for corrected values** in membership and caps, and it drops lines to recipients that have not filed. It is not comparable with FY2021–24 R5. The batch-34 caveats also apply: tier weights, DAF-share proxies from `sponsor-cost-structure.csv`, the W5 list, and same-FY-label matching across June and December year ends.
- **Part VII-B lists only the five highest contractors over $100k.** Absence is not evidence of no relationship. The FY2025 vendor columns cover a different sponsor set from FY2024.
- **Scope not done** in this item, though named in the P-GAP19-01 text: the Schedule F foreign-grant parse and the FY2025 `mission_net_payout.py` payout re-run. These are carried in P-G01-01.

## 7. Data dictionary

### `form990-harvest-fy2025-refresh.csv` (977 rows; one per located FY2025 return)
| Column | Meaning |
|---|---|
| ein, sponsor_name, type, subtype, selection, fy2024_asset_rank, fy2024_daf_assets | DAFRC universe fields (`all_fy2024_dafrc`); `fy2024_daf_assets` is the DAFRC value as published |
| fiscal_year, tax_year, tax_period, tax_period_end, return_ts, return_object_id, return_type, amended_ind | Return identity (FY = year the period ends; tax_year = IRS TaxYr) |
| xml_status | `ok` for all 977 rows |
| xml_source | `gt_mirror` or `teos_zip` |
| xml_batch_id | IRS index XML_BATCH_ID (index_2026 rows only) |
| index_year, index_last_modified | Index file the return was located in, and its Last-Modified date |
| prior_status | `in_prior_harvest_ok`, `in_prior_2026_fill`, `new_since_prior_ein_new_to_fy2025` or `new_since_prior_supersedes_earlier_fy2025_return` |
| prior_values_check | `match` when the earlier parse has identical Schedule D Part I values; blank for new returns |
| filer_name_990, contractors_listed, contractors_over_100k_cnt, daf_ind_part_iv | As in the full harvest |
| sched_d_present, sched_d_daf_count, sched_d_daf_contributions, sched_d_daf_grants, sched_d_daf_eoy_value | Schedule D Part I DAF column, as filed |
| sched_d_other_funds_count, sched_d_other_funds_eoy_value | Schedule D Part I column (b) |
| part_ix_* | Part IX totals (IT, other fees, management, investment management) |
| total_assets_eoy | Part X total assets at year end |
| part_ix_line1_grants_domestic_orgs | Part IX line 1 |
| sched_i_lines, sched_i_total, sched_i_panel_lines | Schedule I Part II line count, total, and lines to DAFRC panel EINs |
| sched_i_itemised | 0 when Schedule I points to an attachment (`mission_net_payout.itemized`) |
| fy2024_corrected_daf_assets | FY2024 corrected (R1–R4) DAF assets of the sponsor |
| dafrc_eoy_daf_assets_same_fy, dafrc_assets_source_same_fy | DAFRC row for FY2025 (none exists; blank) |
| xml_url | Mirror URL, or the TEOS zip URL with `#member` |
| index_url, source_url | IRS index CSV; ProPublica `/full` page (citation only, not fetched) |

### `daf-sponsor-league-table-fy2025-refresh.csv` (56 rows; FY2025 only)
- **Columns:** identical to `daf-sponsor-league-table-fy2021-2025.csv` (see the direction report §6), with these differences:
  - `daf_grants_netted_central`, `share_daf_grants_netted_central`, `daf_contributions_netted_central`, `r5_outbound_central` and `r5_inbound_central` are filled for covered FY2025 filers, from the covered-only FY2025 R5 (§1.4);
  - `share_basis` says so;
  - `as_built_row_type`, `as_built_rank_assets` and `as_built_daf_assets_eoy` give the same EIN's row in the as-built FY2025 table;
  - `change_vs_as_built` is one of `unchanged`, `superseding_return`, `new_row:<type>` or `<old>-><new>`.
- **FY2021–24 rows** are unchanged and stay in the original file.

### `daf-concentration-fy2025-refresh.csv` (10 rows)
- **Columns:** as `daf-concentration-fy2021-2025.csv`.
- **basis values:**
  - `fy2025_filed_covered_only` (gross; 4 metrics);
  - `fy2025_filed_covered_only_netted_r5_{lower,central,upper}` (grants and contributions). Here `market_total` is the covered filed total minus covered R5.

### `dafrc-market-totals-netted-fy2025-refresh.csv` (6 rows; metric × tier)
| Column | Meaning |
|---|---|
| fiscal_year, metric, tier, basis | 2025; `daf_grants` or `daf_contributions`; `lower`, `central` or `upper`; `fy2025_filed_covered_only` |
| covered_filed_value | Sum of positive filed FY2025 values over covered filers |
| r5_netting_amount, netted_value, netting_share_of_covered | R5 amount N, the value net of N, and N ÷ covered value |
| weighted_before_caps, gross_lines_in_tier, lines, grantors, recipients | As in `dafrc-market-totals-netted.csv` |
| all_panel_lines_gross | All FY2025 Schedule I $ from covered grantors to other panel EINs |
| central_weighted_lines_to_recipients_not_yet_filed | Central-weighted $ of lines whose recipient has no FY2025 return (not netted) |
| grantor_daf_grants_sched_i_not_itemised | Filed FY2025 DAF grants of covered grantors whose Schedule I is an attachment |
| sources | Provenance |

### `form990-contractors-fy2025-refresh.csv` (1,066 rows)
Columns as `form990-contractors-harvest-full.csv`. `source_url` is the mirror or TEOS-zip URL.

### `vendor-footprint-990-fy2025-refresh.csv` (21 rows; DAF-relevant vendor groups plus the named four)
| Column | Meaning |
|---|---|
| vendor, vendor_category | Normaliser group and category |
| fy2025_refresh_sponsors, _compensation, _lines | FY2025 lines in this refresh |
| fy2025_refresh_payers_fy2024_corrected_assets, fy2025_refresh_payers_share_of_fy2024_corrected_market | Reach of the FY2025 payers (÷ $323.27bn) |
| fy2025_prior_harvest_sponsors, fy2025_prior_harvest_compensation | FY2025 lines in `form990-contractors-harvest-full.csv` |
| fy2024_sponsors, fy2024_compensation, fy2024_payers_fy2024_corrected_assets | FY2024 lines in the full harvest |
| fy2024_payers_with_fy2025_return_parsed, fy2024_payers_named_again_fy2025, fy2024_payers_not_named_fy2025 | Like-for-like persistence test |
| fy2025_new_payers_vs_fy2024, fy2025_sponsors | Sponsor names |
| source | Provenance |

### `queue-proposals-g01.csv`
- Format per [queue-proposals-README.md](../../data/mission-2026-11-14/queue-proposals-README.md).
- **P-G01-01:** finish the refresh on the November batches, adding Schedule F and net payout.
- **P-G01-02:** the $976.6m DAFgiving360 → Fidelity line.
- **P-G01-03:** re-source the crt.sh-only Give Interactive leads.

## 8. Reproduction
```
# IRS holds index_2025.csv and index_2026.csv; members of 2026_TEOS_XML_05B.zip and 2026_TEOS_XML_10A.zip extracted to D05B, D10A
python3 -I scripts/mission_fy2025_refresh.py --irs-dir IRS --work WORK --fetch \
    --local-xml-dir 2026_TEOS_XML_05B=D05B --local-xml-dir 2026_TEOS_XML_10A=D10A --summary-json SUMMARY.json
```
- **Run time:** about 35 seconds with the network for 977 returns (8 threads), and about 5 seconds from the cache.
- **Summary JSON:** the run prints a JSON summary with coverage (refresh and as built), churn, concentration, netting tiers and pairs, the vendor table and the Ren panel. Every figure above comes from that summary or from the CSVs.
- **Scratch:** the extract cache and the zip members were kept in the session scratchpad only. The two zips were deleted after extraction.

## Validation corrections (wave 31A, 2026-11-19) — governing
These corrections from [validation-wave31a-report.md](validation-wave31a-report.md) could not be applied inline and govern the text above:

1. **§4.2, unnamed payer (Memphis).**
   - **Find:** "  - Community Foundation (EIN 58-1723645): $203,119."
   - **Replace with:** "  - Community Foundation of Greater Memphis (EIN 58-1723645): $203,119, Stellar Technology Solutions LLC, \"software\" [V wave 31A]."
2. **§4.2, unnamed payer (Philadelphia).**
   - **Find:** "  - Jewish Federation of Greater … (EIN 23-1500085): $500,842, Renaissance Administration."
   - **Replace with:** "  - Jewish Federation of Greater Philadelphia (EIN 23-1500085): $500,842, Renaissance Administration [V wave 31A]."
3. **§4.3, Kalamazoo provenance.**
   - **Find:** "\"TECHNOLOGY/SOFTWARE CONSULTATION\", $416,932, CY2025."
   - **Replace with:** "\"TECHNOLOGY/SOFTWARE CONSULTATION\", $416,932, CY2025 (read from the TEOS 10A zip; on 2026-11-19 the return was not yet on the GivingTuesday mirror or ProPublica, so it has not been independently re-read [V wave 31A])."
4. **§6, suspect filed values.**
   - **Find:** "  - Armstrong County CF, which files $10.3m against a FY2024 corrected value of $148.2m (already flagged in the full-universe report)."
   - **Replace with:** "  - Armstrong County CF, which files $10.3m against a FY2024 corrected value of $148.2m (already flagged in the full-universe report).
  - Greater Green Bay CF, which files a negative FY2025 DAF year-end value (−$5,666,175; object 202513179349310111) [V wave 31A]."
