# Recipient sectors for all itemising DAF sponsors, with foreign and sub-$5,000 grants, reconciled to sponsors' own splits (P-B39N4-01)

**Date:** 2026-11-20 · **Task ID:** b39n4-01 · **Queue item:** P-B39N4-01 (from [queue-proposals-batch39-n4.csv](../../data/mission-2026-11-14/queue-proposals-batch39-n4.csv)) · **Builds on:** [direction-recipients-impact-matching.md](direction-recipients-impact-matching.md) §1 (top-50 join, validated byte-identical in wave 24A), [direction-foreign-grants-schedule-f.md](direction-foreign-grants-schedule-f.md) (with the wave-30 and wave-37A glosses), [b40n120201-01-coverage-gap-decomposition.md](b40n120201-01-coverage-gap-decomposition.md) (with its wave-41B corrections)

**Outputs**
- Script: [`scripts/mission_sector_join_all.py`](../../scripts/mission_sector_join_all.py). It is new. It imports `mission_recipient_sectors.py` (and `mission_non_top50_numerator.py` for the universe) and modifies neither.
- Data: [`data/mission-2026-11-14/sector-join-all-sponsors-2026-11-20.csv`](../../data/mission-2026-11-14/sector-join-all-sponsors-2026-11-20.csv). 15,168 rows: 14,616 `share` rows and 552 `reconciliation` rows. The data dictionary is in §7.
- Queue proposals: [`data/mission-2026-11-14/queue-proposals-b39n4-01.csv`](../../data/mission-2026-11-14/queue-proposals-b39n4-01.csv) (P-B39N401-01 to 04).

**Tags:** [F] computed from filings by the script · [P] quoted from a sponsor's own publication (not audited) · [S] search snippet only · [I] inference or allocation assumption.

**Rules applied.** All data are FY2023–FY2024 returns or 2024–2026 publications. robots.txt was checked for every host before fetching (§6). No outreach, logins or forms. No repo file was modified; nothing was committed.

---

## 0. Answers in brief

| Question | Answer |
|---|---|
| **(a) All itemising sponsors** | **Coverage.** 2,705 itemising sponsor-years from 1,379 sponsors, 1,092,809 Schedule I lines and 264,127 distinct recipient EINs (224,264 in the BMF) [F].<br><br>**Size.** The non-university/hospital scope has $122.34bn of filed Schedule I. That falls to $107.92bn after DAF-weighting, and to **$93.41bn net of DAF-to-DAF** ($14.51bn, 13.4%) [F].<br><br>**Headline shares** (DAF-weighted, base treatment, with foreign and sub-$5,000 grants added, $101.01bn):<br>- education **23.0%**;<br>- human services **14.6%**;<br>- religion **14.1%**;<br>- public-society benefit **13.2%** (NTEE T 5.7 pts of it);<br>- health 9.2%;<br>- environment/animals 5.6%; arts 5.5%; international (NTEE Q) 5.3%;<br>- **foreign grants (Schedule F) 3.1%**;<br>- unclassified 5.9%; unknown (Z) 0.5% [F/I].<br><br>**Against the top 50 alone.** Adding the other 1,331 sponsors changes no sector by more than 3 points. Education is lower (23.0% against 25.1% on the same layer for the top 50) and human services is slightly higher. |
| **Non-top-50 sponsors differ** | **Size.** $19.26bn DAF-weighted net Schedule I [F].<br><br>**Shares:**<br>- education 16.7%, against 26.1% at the top 50;<br>- human services 17.5% (14.2%);<br>- religion 15.4% (13.8%);<br>- public benefit 13.1% (14.1%);<br>- unclassified 11.4% (4.5%).<br><br>**Concentration** is lower: top 100 recipients 14.1%, HHI 4.4 (filed basis) [F].<br><br>**Non-top-50 community foundations** ($6.59bn): human services 19.4%, education 18.9%, religion 8.6%, arts 8.5%, against 4.6% religion for all CFs [F]. |
| **(b) Foreign grants as a sector** | **DAF-weighted.** Part IX line 3 adds **$3.15bn** over FY2023–24: **3.1%** of the extended base, or 3.3% before sub-$5,000 grants. That is 2.4% at the top 50 and **5.7% at non-top-50 sponsors** [F].<br><br>**Filed basis.** The same bucket is $8.34bn (6.9%). It is dominated by panel sponsors that are operating charities with small DAF books: World Vision files $1.14bn and $1.10bn of line 3 with a DAF weight of 0.003–0.005, and the Rotary Foundation, JDC and PEF Israel follow. So **the filed-basis foreign share is not DAF money**, and the DAF-weighted basis is the headline [F/I].<br><br>**International + foreign** = 8.4% of the extended base. That is a recipient-sector share, not money leaving the US (wave 37A gloss) [I]. |
| **(c) Reconciliation: DAF-to-DAF and NTEE T** | **Fidelity's published dollar split** (2025 and 2026 Giving Reports) is matched far better when **DAF-to-DAF grants are kept and classified by the receiving sponsor's NTEE code** (treatment t_b), with NTEE T left inside society benefit [P vs F]. Sum of absolute differences across 9 sectors, Fidelity FY2024 lines:<br>- t_b **0.12–0.13**;<br>- base treatment (DAF-to-DAF dropped) 0.21–0.24;<br>- T also dropped 0.31–0.34.<br><br>**Society benefit** moves from 13.1% to 21.0% under t_b, against Fidelity's 25% (CY2024) and 23.4% (CY2025).<br><br>**DAFgiving360** (search snippet only; robots blocked) says the "highest percent" of grant recommendations goes to the public and education sectors. Our FY2024 lines put public benefit 2nd only under t_b, in dollars [S/F].<br><br>**Vanguard Charitable** publishes grant counts only. Counts do not discriminate between treatments [P/F]. |
| **Which treatment to use** | **Two views, used for different purposes [I]:**<br>- **To compare with sponsor-published splits or Giving USA-style "society benefit", use t_b.** It gives public-society benefit **23.7%** of the DAF-weighted extended base (education 20.2%, human services 12.8%, religion 12.5%).<br>- **For where DAF money ends up, keep the base treatment.** DAF-to-DAF dropped, so nothing is counted twice; public benefit 13.2%. Report NTEE T as its own 5.7-point line (t_c) rather than dropping it: the Fidelity test rejects dropping T (t_d). |
| **Sub-$5,000 grants** | **Handled as in b40n120201-01 / wave 41B.** Line 1 minus Schedule I is allocated by the `small10` key for full itemisers ($3.47bn DAF-weighted) and pro rata for the partial itemisers ($0.98bn) [F/I].<br><br>**Effect:** it moves religion +0.4 pts and human services +0.2, and lowers public benefit by 0.2 and education by 0.3 (DAF-weighted, base treatment). The layer without it (`sched_i` / `plus_foreign`) is the low end of the wave-41B envelope [F/I]. |

---

## 1. Method

### 1.1 Existing join and its validation history (read first)
- **The top-50 join.** [`mission_recipient_sectors.py`](../../scripts/mission_recipient_sectors.py) (P-NEW-RCP-01, [direction-recipients-impact-matching.md](direction-recipients-impact-matching.md) §1) joins every Schedule I Part II line of the top-50 sponsors to the IRS EO BMF `NTEE_CD`. It drops DAF-to-DAF lines via [`daf-to-daf-recipient-whitelist.csv`](../../data/mission-2026-11-14/daf-to-daf-recipient-whitelist.csv). Its headline is $77.34bn net, with education 25.8%, human services 14.3%, public benefit 14.1% and religion 13.6%.
- **Wave 24A** rebuilt its 3,984-row CSV byte-identical from fresh XML (V24A; [validation-wave24a-report.md](validation-wave24a-report.md) finding 1). It found that P-B39N4-02 (ImpactAssets) duplicated an existing R1 correction. Wave 24B used its community-foundation DAF-to-DAF share.
- **Waves 30 and 37A** revised the international share to 7.8% with Schedule F ([direction-foreign-grants-schedule-f.md](direction-foreign-grants-schedule-f.md)). They glossed it as a recipient-sector share, not money leaving the US.
- **The all-sponsor line caches** (`q120201/lines`), the `drop_totals_rows` rule (wave 32A) and the Part IX/Schedule F extracts come from [b40n1202-01](b40n1202-01-non-top50-numerator.md) and [b40n120201-01](b40n120201-01-coverage-gap-decomposition.md). Wave 41B validated the latter byte-identical. Its corrections that matter here:
  - report the sub-$5,000 component with its assumption envelope (dropping it is the low end);
  - 129 sponsor-years carry the default weight, and 122 itemising FY2024 sponsor-years have zero corrected DAF grants;
  - the DAF-to-DAF residual is a netting-tier choice.

### 1.2 Universe and lines
- **Universe.** Every DAFRC 2025 panel sponsor-year FY2023–FY2024 in the netpayout990 cache, with return choice `mission_daf_to_daf.pick_returns`. That is 3,097 sponsor-years; the **2,705** that itemise Schedule I are used (94 top-50, 2,611 other), exactly the b40n1202-01 / b40n120201-01 set.
- **Lines.** Top-50 lines come from `rcp/lines` and the rest from `q120201/lines`. Caches only; nothing was fetched. All 2,705 loaded with status `ok`.
- **Totals rows.** Filer totals rows are dropped (`mission_exception_load.drop_totals_rows`). Among the top 50 this removes two blank lines on Greater Horizons' FY2024 return ($212,187,406 and $3,282).
- **Reproduction of the top-50 figure.** The top-50 non-university/hospital net is therefore **$77,131,527,070 = P-NEW-RCP-01's $77,343,717,758 − $212,190,688** exactly, and every top-50 share agrees with P-NEW-RCP-01 to within 0.1 pt apart from unclassified (4.6% against 4.9%) [F].

### 1.3 Join
- **Classification.** `mission_recipient_sectors.load_bmf` and `annotate`, unchanged:
  - the DAF-to-DAF flag: whitelist `include` EINs, self-lines, and unique whitelisted-name matches for blank EINs;
  - NTEE major group, with BMF FOUNDATION-code and name-rule fallbacks.
- **Public-society benefit** is carried internally as NTEE T and other R–W, so treatments can move T.
- **Checks.** Per sponsor-year, the Schedule I total and the DAF-to-DAF total equal `si_non_d2d + si_d2d` and `si_d2d` in the coverage-gap CSV to the cent (maximum absolute difference $0.00 over 2,705 rows) [F].

### 1.4 Foreign grants bucket
- **Source.** Form 990 Part IX line 3 (`l3`, column A; itemised on Schedule F Parts II–III) per sponsor-year, from [`coverage-gap-decomposition-2026-11-20.csv`](../../data/mission-2026-11-14/coverage-gap-decomposition-2026-11-20.csv) (`row_type = sponsor_itemised`). It enters as sector `foreign_schedule_f`.
- **Cross-check.** For the 94 top-50 sponsor-years, `l3` equals `part_ix_l3_foreign_usd` in [`daf-foreign-grants-schedule-f-2023-2024.csv`](../../data/mission-2026-11-14/daf-foreign-grants-schedule-f-2023-2024.csv) in every row (no difference above $1) [F].
- **Recipient sector.** Foreign grants are a destination bucket, not an NTEE sector. Region and purpose detail for the top 50 stay in the foreign-grants CSV.

### 1.5 Sub-$5,000 grants (b40n120201-01 rules, with the wave-41B corrections)
- **The component.** Per sponsor-year, non-itemised domestic grants = Part IX line 1 − Schedule I total (all lines, including DAF-to-DAF). Negative values (Schedule I > line 1) are kept in the net.
- **Full itemisers** (Schedule I ≥ 50% of line 1). Their sum is spread over sectors by the mix of the scope's positive non-DAF-to-DAF lines under $10,000 (the `small10` key, the nearest observed analogue of sub-$5,000 gifts).
- **Partial itemisers** (< 50%: suspected partial itemisation, not small gifts). Spread pro rata over all positive non-DAF-to-DAF lines (the `all` key).
- **Timing.** The allocation is made per FY and per scope, then pooled.
- **Layers.**
  - `sched_i`: filed lines only, the low end of the wave-41B envelope;
  - `plus_foreign`: adds line 3;
  - `plus_foreign_sub5k`: adds the allocated component.
- **What is never allocated.** As in b40n120201-01, no DAF-to-DAF-like part is carved out of the sub-$5,000 component, and grants to individuals (line 2) are excluded.

### 1.6 Bases and treatments
- **Bases.**
  - `schedule_i`: filed dollars.
  - `daf_weighted`: each sponsor-year × w2 = min(1, corrected DAFRC DAF grants ÷ (L1 + L3)), the decomposition-B weight of b40n120201-01. Lines, line 3 and the sub-$5,000 component are weighted alike.
- **Why DAF-weighted is the headline for all sponsors.** Unlike the top 50, the panel includes operating charities with small DAF programmes (§3.3).
- **Treatments:**

| Code | DAF-to-DAF lines | NTEE T |
|---|---|---|
| `t_a_base` | excluded | in public-society benefit (P-NEW-RCP-01 convention) |
| `t_b_d2d_included` | kept, classified by the receiving sponsor's own NTEE (mostly T and community-foundation codes) | in public-society benefit |
| `t_c_t_separate` | excluded | own bucket `philanthropy_t` |
| `t_d_t_excluded` | excluded | excluded (treated as pass-through like DAF-to-DAF) |

### 1.7 Reconciliation design
- **Published splits** are coded as constants in the script and listed in the source register:
  - Fidelity 2025 Giving Report (CY2024; dollars and volumes);
  - Fidelity 2026 Giving Report (CY2025; dollars and volumes, with $727m of outliers removed by Fidelity);
  - Vanguard Charitable 2024 and 2025 annual reports (grant counts for five causes, divided by total grants issued).
- **Comparison.** Each is compared with the sponsor's own FY2024 lines (and the FY2023–24 pool) under t_a, t_b and t_d. t_c maps to the same published buckets as t_a. Dollars are compared on all three layers; counts on Schedule I line counts.
- **Mapping to Fidelity's labels:**
  - International affairs = NTEE Q + foreign;
  - Society benefit = R–W, including T;
  - Other = Y, Z and unclassified.
- **Distance.** The sum and the maximum of absolute share differences.

---

## 2. Coverage [F]

| Scope (FY2023–24) | Sponsor-years | Sponsors | Schedule I filed | DAF-to-DAF filed | Part IX L1 | Part IX L3 | Recipients | Top-100 share | HHI |
|---|---|---|---|---|---|---|---|---|---|
| All itemising | 2,705 | 1,379 | $131.62bn | $16.01bn (12.2%) | $137.15bn | $9.06bn | 291,588 | 21.9% | 12.8 |
| All ex university/hospital | 2,495 | 1,273 | $122.34bn | $15.85bn (13.0%) | $127.93bn | $8.34bn | 289,387 | 19.6% | 12.1 |
| Top 50 ex university/hospital | 90 | 46 | $89.83bn | $12.70bn (14.1%) | $91.85bn | $1.89bn | 174,194 | 24.2% | 21.2 |
| Non-top-50 ex university/hospital | 2,405 | 1,227 | $32.51bn | $3.16bn (9.7%) | $36.08bn | $6.45bn | 193,501 | 14.1% | 4.4 |
| Community foundations ex SVCF | 1,538 | 782 | $22.30bn | $1.02bn (4.6%) | $24.11bn | $0.19bn | 121,973 | 14.2% | 4.8 |

- **Concentration** is computed on filed, non-DAF-to-DAF dollars by recipient key.
- **Schedule I ÷ line 1** is 95.6% for all ex university/hospital, against 97.8% at the top 50. Non-top-50 sponsors leave more of line 1 unitemised (90.1%), which is why the sub-$5,000 layer matters more for them.
- **Classification mix** (filed, non-DAF-to-DAF, all sponsors):
  - NTEE 77.6%;
  - name rule 8.2%;
  - BMF church/school/hospital codes 7.3%;
  - in BMF without NTEE 3.9%;
  - EIN not in BMF 1.8% (plus 0.2% government);
  - blank EIN 0.9% (plus 0.1% government).

  That is less NTEE-coded than the top 50 (82.0%) [F].

## 3. Results

### 3.1 All sponsors, by treatment and layer (all ex university/hospital, FY2023–24, DAF-weighted) [F/I]

Each cell is a % of the row base.

| Treatment · layer | Base | Educ. | Human svc | Religion | Public benefit | (of which T) | Health | Env. | Arts | Intl (Q) | Foreign (Sch. F) | Unclass. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| t_a · sched_i | $93.41bn | 24.1 | 14.9 | 14.2 | 13.9 | 6.0 | 9.6 | 5.7 | 5.6 | 5.6 | — | 5.9 |
| t_a · plus_foreign | $96.57bn | 23.3 | 14.4 | 13.7 | 13.4 | 5.8 | 9.3 | 5.5 | 5.5 | 5.4 | 3.3 | 5.7 |
| **t_a · plus_foreign_sub5k** | **$101.01bn** | **23.0** | **14.6** | **14.1** | **13.2** | 5.7 | **9.2** | 5.6 | 5.5 | 5.3 | **3.1** | 5.9 |
| t_b · sched_i | $107.92bn | 21.0 | 12.9 | 12.5 | 25.0 | — | 8.3 | 4.9 | 4.9 | 4.8 | — | 5.2 |
| **t_b · plus_foreign_sub5k** | **$115.52bn** | **20.2** | **12.8** | **12.5** | **23.7** | — | 8.0 | 4.9 | 4.8 | 4.6 | 2.7 | 5.2 |
| t_c · plus_foreign_sub5k | $101.01bn | 23.0 | 14.6 | 14.1 | 7.4 (ex T) | 5.7 (own bucket) | 9.2 | 5.6 | 5.5 | 5.3 | 3.1 | 5.9 |
| t_d · plus_foreign_sub5k | $95.23bn | 24.4 | 15.5 | 14.9 | 7.9 (ex T) | excluded | 9.8 | 5.9 | 5.9 | 5.6 | 3.3 | 6.3 |

- **Filed basis** (t_a, plus_foreign_sub5k, $120.41bn): education 21.3, human services 14.5, religion 13.0, public benefit 12.7, health 8.6, **foreign 6.9**, unclassified 6.6 [F].
- **Year split** (t_a, DAF-weighted, full layer): FY2023 $47.09bn and FY2024 $53.93bn.
  - Education 23.3 → 22.7; human services 13.9 → 15.2; religion 13.4 → 14.6; health 10.6 → 8.0 (FY2023 holds SVCF's CZ Biohub lines); foreign 3.1 → 3.2.
  - DAF-to-DAF (DAF-weighted) rose from $5.14bn to $9.36bn [F].

### 3.2 Top 50 versus the other 1,331 sponsors (t_a, DAF-weighted, ex university/hospital) [F]

| Group | Top 50, sched_i | Non-top-50, sched_i | Top 50, full layer | Non-top-50, full layer |
|---|---|---|---|---|
| Base | $74.15bn | $19.26bn | $77.91bn (plus_foreign) | $23.11bn |
| Education | 26.1 | 16.7 | 25.1 | 15.6 |
| Human services | 14.2 | 17.5 | 14.0 | 16.8 |
| Religion | 13.8 | 15.4 | 13.9 | 14.5 |
| Public benefit | 14.1 | 13.1 | 13.5 | 11.9 |
| Health | 10.1 | 7.8 | 9.7 | 7.3 |
| Arts | 5.5 | 6.0 | 5.5 | 5.7 |
| Environment | 5.6 | 6.1 | 5.5 | 6.0 |
| International (Q) | 5.6 | 5.3 | 5.4 | 4.8 |
| Foreign (Sch. F) | — | — | 2.4 | 5.7 |
| Unclassified | 4.5 | 11.4 | 4.5 | 10.9 |

For the top 50, the full layer and plus_foreign are within 0.1 pt of each other: top-50 sub-$5,000 dollars are $1.92bn DAF-weighted, against a $77.9bn base.

**By segment** (all panel sponsors, DAF-weighted, t_a, sched_i):

| Segment | Base | Educ. | Human svc | Religion | Public benefit | Health | Env. | Arts | Intl | Unclass. | Foreign (plus_foreign) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| National (all) | $56.67bn | 28.5 | 14.4 | 14.2 | 12.4 | 8.2 | 5.6 | 6.0 | 5.5 | 4.6 | 3.0 |
| · non-top-50 national | $3.05bn | 19.4 | 17.7 | 14.7 | 13.9 | 8.4 | 4.7 | 4.5 | 6.4 | 9.2 | 15.0 |
| Processor (all) | $5.51bn | 14.4 | 19.6 | 9.6 | 10.8 | 10.0 | 8.5 | 4.0 | 8.9 | 13.4 | 1.9 |
| Community foundation (all) | $20.00bn | 17.9 | 17.1 | 4.6 | 19.1 | 16.3 | 6.8 | 6.1 | 3.7 | 8.0 | 2.2 |
| · ex SVCF | $14.31bn | 19.9 | 20.6 | 6.2 | 13.8 | 9.8 | 8.2 | 7.5 | 3.3 | 10.2 | 1.0 |
| · non-top-50 CFs | $6.59bn | 18.9 | 19.4 | 8.6 | 14.3 | 8.5 | 7.2 | 8.5 | 1.8 | 12.4 | 0.3 |
| Single-issue (all) | $11.23bn | 17.8 | 11.1 | 33.1 | 13.5 | 4.6 | 2.7 | 3.9 | 7.5 | 5.4 | 6.1 |
| · non-top-50 single-issue | $4.20bn | 14.3 | 11.2 | 34.2 | 14.8 | 3.7 | 2.1 | 5.8 | 5.1 | 8.6 | 11.5 |

**Readings [I]**
- **Small community foundations.** The non-top-50 CF tail gives more to religion (8.6% vs 2.9% at top-50 CFs in P-NEW-RCP-01) and to arts. Its foreign share is almost nil.
- **Processors.** The segment (PayPal Giving Fund and others outside the top 50) is the most human-services-heavy (19.6%) and the least classifiable (13.4% unclassified).
- **Non-top-50 national and single-issue foreign shares.** Their large DAF-weighted foreign shares (15.0%, 11.5%) come from cross-border intermediaries on the panel (CAF America w2 ≈ 0.85–0.93, Myriad USA, PEF Israel) [F].

### 3.3 The foreign bucket and why the filed basis misleads [F/I]
- **Filed line 3.** Non-top-50 itemisers file $7.14bn of line 3, against $40.81bn of Schedule I.
- **The largest filers are operating charities on the DAFRC panel.** Their DAF programmes are tiny next to their grantmaking:

| Sponsor | Line 3 | w2 |
|---|---|---|
| World Vision | $1,136.2m (FY2023), $1,095.2m (FY2024) | 0.003–0.005 |
| Rotary Foundation | $270.6m, $262.3m | 0.03 |
| American Jewish Joint Distribution Committee | $235.9m, $231.6m | ≈0.001–0.007 |
| PEF Israel Endowment Funds | $281.1m, $261.6m | 0.19–0.25 |

- **Effect of weighting.** w2 cuts the non-top-50 foreign bucket from $6.45bn to $1.31bn (ex university/hospital).
- **Top-50 figures** ($1.890bn filed; $1.838bn DAF-weighted) match the foreign-grants direction's $1.891bn / $1.837bn.
- **The weighted figure is still an assumption.** It assumes a sponsor's DAF grants go abroad in the same proportion as its other grants (P-B39N401-04).
- **What the bucket is not.** Foreign + NTEE Q = 8.4% (t_a, full layer, DAF-weighted) is a recipient-sector share. Money leaving the US is measured separately in b45n31-01 (3.82% of top-50 grants).

### 3.4 Sub-$5,000 component [F/I]
- **Size.** For all ex university/hospital it is $4.33bn filed for full itemisers and $1.26bn for partial itemisers; DAF-weighted, $3.47bn and $0.98bn.
- **Effect on shares.** Allocating it moves shares by at most 0.4 pt. The small-line key carries more religion and human services, and less education and public benefit, than the all-line key.
- **Envelope.** The `sched_i` and `plus_foreign` layers are the measured-only bounds, as wave 41B asks.

---

## 4. Reconciliation against sponsors' own published splits

### 4.1 Fidelity Charitable (dollars) [P vs F]
- **Published splits.** The 2025 Giving Report (CY2024; p.20 and the appendix) and the 2026 Giving Report (CY2025; p.9, with $727m of "significant outlier granting" removed from the sector chart per its methodology) give grant-dollar shares by "charitable sector".
- **Our comparison base.** Fidelity's FY2024 return (FYE 2024-06-30, so half a year earlier than CY2024): $11.33bn net Schedule I, plus $1.19bn of DAF-to-DAF lines.

Share of grant dollars:

| Sector | Fidelity CY2024 | Fidelity CY2025 | Ours t_a (sched_i) | Ours t_b (sched_i) | Ours t_b (full layer) | Ours t_d (sched_i) |
|---|---|---|---|---|---|---|
| Education | 23% | 24.8% | 24.6% | 22.4% | 22.2% | 26.0% |
| Society benefit | **25%** | **23.4%** | 13.1% | **21.0%** | 20.7% | 7.9% |
| Religion | 13% | 13.1% | 15.7% | 14.3% | 14.4% | 16.7% |
| Human services | 13% | 12.2% | 13.2% | 12.1% | 12.1% | 14.0% |
| Health | 8% | 7.5% | 10.5% | 9.5% | 9.4% | 11.1% |
| Arts and culture | 6% | 5.9% | 6.1% | 5.5% | 5.5% | 6.4% |
| International affairs | 5% | 5.5% | 5.4% | 4.9% | 5.4% | 5.7% |
| Environment and animals | 5% | 5.2% | 5.7% | 5.2% | 5.2% | 6.1% |
| Other | 2% | 2.5% | 5.7% | 5.2% | 5.2% | 6.1% |
| **Sum of absolute differences vs CY2024** | | | 0.237 | **0.123** | 0.130 | 0.342 |
| **… vs CY2025** | | | 0.212 | **0.118** | 0.118 | 0.309 |
| **Max absolute difference vs CY2024** | | | 11.9 pts | **4.1 pts** | 4.3 pts | 17.1 pts |

- **The verdict is the same on the pooled FY2023–24 lines:** t_b 0.10–0.15, t_a 0.23–0.27, t_d 0.32–0.36. It also holds on every layer [F].
- **What remains under t_b [I]:**
  - society benefit −2.4 to −4.3 pts;
  - "Other" +2.7 to +3.2 pts. That is our unclassified, which Fidelity's internal system presumably assigns to sectors.
  - health +1.4 to +2.0 pts;
  - religion +1.2 to +1.4 pts.
- **Why Fidelity's society benefit is larger [I].** Its sector chart evidently counts grants to other DAF sponsors and grantmaking intermediaries as "society benefit". That is consistent with the NTEE T and community-foundation codes those recipients carry. Dropping NTEE T as well (t_d) moves away from the published split, so Fidelity does not treat T as pass-through.
- **Volumes do not discriminate.** Against Fidelity's grant-volume split (27% religion, 20% human services …), Schedule I line counts give sums of absolute differences of 0.27–0.32 under every treatment. Schedule I has one line per recipient over $5,000, not one per grant, so counts are not like-for-like [F/I].

### 4.2 Vanguard Charitable (counts only) [P vs F]
- **What is published.** The 2024 and 2025 annual reports give grant counts for five causes:
  - CY2024 (240,064 grants issued): human services 68,000+, religion 52,000+, education 36,000+, health 30,000+, environment and wildlife 19,000+;
  - CY2025 (267,838 grants issued): 72,000+, 54,000+, 38,000+, 33,000+, 20,000+.
- **No dollar split is published.**
- **Our comparison.** Vanguard's FY2024 line counts: human services 18.2%, religion 26.3%, education 14.6%, health 6.4%, environment 7.3%, against published 28.3 / 21.7 / 15.0 / 12.5 / 7.9%.
- **Result.** Sums of absolute differences are 0.21–0.23 under t_a, t_b and t_d alike. The count test cannot discriminate, and its mismatch reflects the line-per-recipient structure of Schedule I [F/I].

### 4.3 DAFgiving360 (robots-blocked; snippet only) [S vs F]
- **Not fetched.** `www.dafgiving360.org/robots.txt` and `www.schwabcharitable.org/robots.txt` both returned 403 (Access Denied) at 2026-11-20 01:49 UTC, so neither site was fetched.
- **The snippet.** A search-engine snippet of the [FY2025 Giving Report page](https://www.dafgiving360.org/resource/giving-report) reads: "our donors' support spanned across all charity types, with the highest percent of their grant recommendations going to charities in the public and education sectors" [S]. Whether this is a dollar or a count share is unknown.
- **Our DAFgiving360 FY2024 lines (FYE 2024-06; full layer):**
  - t_a: education 31.7%, religion 16.2%, human services 14.0%, arts 8.0%, **public benefit 7.8%**;
  - t_b: education 27.9%, **public benefit 18.5%**, religion 14.5%, human services 12.3%.
- **By line count,** religion leads (31%) under every treatment.
- **Reading [I].** The snippet is consistent only with dollar shares under t_b. This is weak, independent support for the Fidelity result (P-B39N401-03).

### 4.4 Treatment settled [I]
- **Sponsor-comparable view: t_b.** DAF-to-DAF grants are counted, classified by the receiving sponsor's NTEE code, and NTEE T stays in public-society benefit. Use this view to quote or benchmark sponsor-published splits.
  - On the DAF-weighted full layer, all ex university/hospital: education 20.2%, **public-society benefit 23.7%**, human services 12.8%, religion 12.5%, health 8.0%, foreign 2.7%.
- **End-recipient view: t_a, shown as t_c.** DAF-to-DAF is dropped, because those dollars are counted again when the receiving sponsor grants them out. NTEE T is shown as its own 5.7-point line, not removed: it includes real operating intermediaries (T30 public foundations, T70 federated giving) as well as some DAF-holding public foundations off the whitelist.
- **Dropping T (t_d) is rejected** by the Fidelity test.

---

## 5. Limits
- **Non-itemising sponsors are absent.** BofA CGF, Renaissance, The Donors Fund, Stifel and others have $2.60bn of FY2024 corrected DAF grants (b40n120201-01), so this is "all itemising", not all sponsors. Their line 3 is near zero.
- **Weighting is pro rata.** w2 assumes a sponsor's DAF grants share its other grants' sector and foreign mix. That matters most for community foundations (discretionary and scholarship grants) and for the operating charities on the panel. 122 itemising FY2024 sponsor-years have zero corrected DAF grants and so carry w2 = 0 (wave 41B).
- **Unclassified dollars are higher outside the top 50:** 11.4% of DAF-weighted non-top-50 net, against 4.5% (P-B39N401-02). Name rules (8.2% of all-sponsor dollars) are inference.
- **The sub-$5,000 allocation is an assumption.** The `small10` key is a proxy, and the partial-itemiser rule is the b40n120201-01 convention. The measured-only layers are reported alongside.
- **The reconciliation is thin:**
  - one sponsor publishes a dollar split (Fidelity);
  - one publishes counts (Vanguard);
  - one is a snippet (DAFgiving360);
  - periods are offset by six months (FYE June against calendar year);
  - Fidelity removes outliers ($727m in CY2025) and does not publish its taxonomy;
  - our Fidelity FY2024 $11.33bn net differs from its $14.9bn CY2024 grants, which may include DAF-to-DAF, grants abroad and period differences.
- **Taxonomies differ.** NTEE "public-society benefit" (R–W) is not guaranteed to match Fidelity's "society benefit" or DAFgiving360's "public" sector. The mapping is inference.
- **Fiscal years** follow the DAFRC convention.

## 6. Robots and requests
Log: scratchpad `q0401/robots/log.tsv`. User agent `research-script/1.0`.

| Host | robots.txt | Fetched |
|---|---|---|
| www.fidelitycharitable.org | 200; disallows /retired/, /sample-email/, /nuance/, /content/dam/fc-public/docs/vessel/ only | 2025 and 2026 Giving Report PDFs (allowed paths) |
| fidelitycharitable.org | 301 to www | — |
| www.vanguardcharitable.org | 200; disallows /core/, /profiles/, /search/, /admin/, /user/ … | /2023annualreport, /2024annualreport, /2025annualreport, /newsroom, /news and three /news/ pages (allowed) |
| www.dafgiving360.org | **403** | **not fetched** (search snippet only) |
| www.schwabcharitable.org | **403** | **not fetched** |
| gt990datalake-rawdata.s3.amazonaws.com | not contacted (caches only; 404 at b40n120201-01) | — |

A web search engine was used to locate pages. sec.gov, crt.sh and certspotter were not used.

**Reproduction**
```
S=<scratchpad>
python3 scripts/mission_sector_join_all.py . --np-cache $S/npcache --lines-cache-top50 $S/rcp/lines \
    --lines-cache $S/q120201/lines --bmf-dir $S/rcp/bmf [--out CSV]
```
- It runs in about 25 seconds, from cache only.
- Two runs gave byte-identical CSVs (md5 `6fcefe1ad983f2b60b35a39dcd30b328`).
- stdout is a JSON diagnostic: coverage, checks, method mix, ALL rows, share tables, the reconciliation.

## 7. Data dictionary: `sector-join-all-sponsors-2026-11-20.csv`

| Column | Meaning |
|---|---|
| `row_type` | `share` (sector shares) or `reconciliation` (published split vs computed) |
| `scope` | Scope name (e.g. `all_ex_university_hospital`, `non_top50_community_foundation`, `top50_national`) or sponsor name |
| `scope_type` | `all`, `segment` or `sponsor` |
| `tier_filter` | `all`, `top50` or `other` (non-top-50): the sponsor tier the scope draws on |
| `segment` | DAFRC segment of the scope (national, processor, community_foundation, single_issue, university_hospital), blank for all-segment scopes |
| `fiscal_year` | `2023`, `2024` or `2023-2024` (pooled). Treatments other than t_a only for 2024 and pooled |
| `basis` | `schedule_i` (filed USD) or `daf_weighted` (× w2) |
| `treatment` | `t_a_base`, `t_b_d2d_included`, `t_c_t_separate`, `t_d_t_excluded` (§1.6) |
| `layer` | `sched_i`, `plus_foreign` or `plus_foreign_sub5k` (§1.5) |
| `sector` | `ALL`, an NTEE major group, `philanthropy_t` (t_c only), `foreign_schedule_f`. In reconciliation rows: a published label, or `SUM_ABS_DIFF` |
| `amount_usd` | USD in the sector on the row's basis, treatment and layer |
| `share` | `amount_usd` ÷ the scope's ALL amount. In reconciliation rows: the computed share (or the sum of absolute differences on `SUM_ABS_DIFF` rows) |
| `lines` | Schedule I line count in the sector (DAF-to-DAF lines included under t_b). Blank for the foreign bucket |
| `sponsor_years`, `sponsors` | Sponsor-years and distinct sponsors in the scope (ALL rows) |
| `sched_i_total_usd` | Schedule I total, including DAF-to-DAF lines, after totals-row drop (ALL rows) |
| `d2d_usd` | DAF-to-DAF lines (ALL rows) |
| `ntee_t_non_d2d_usd` | Non-DAF-to-DAF dollars to NTEE T recipients (ALL rows) |
| `part_ix_l1_usd`, `foreign_l3_usd` | Part IX lines 1 and 3 (ALL rows) |
| `sub5k_full_usd`, `sub5k_partial_usd` | Line 1 − Schedule I total for full (≥50%) and partial (<50%) itemisers (ALL rows) |
| `recipients`, `top10_share`, `top100_share`, `hhi` | Concentration on filed non-DAF-to-DAF dollars by recipient key (ALL rows of selected scopes, t_a, sched_i, schedule_i basis) |
| `published_source`, `published_period`, `metric` | Reconciliation: source id (see register), period, and `dollars` or `volume` |
| `published_share`, `diff` | Reconciliation: published share and computed − published |
| `max_abs_diff` | Reconciliation, `SUM_ABS_DIFF` rows: the largest absolute sector difference |
| `source` | Source note (ALL and `SUM_ABS_DIFF` rows only) |

## 8. Source register
- **IRS Form 990 e-file XML** (Schedule I Part II, Part IX), GivingTuesday mirror of IRS TEOS: `https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml`. It was read through the existing caches `rcp/lines`, `q120201/lines` and `q12011/p9`.
- **IRS SOI Exempt Organizations Business Master File:** https://www.irs.gov/pub/irs-soi/eo1.csv (and eo2–eo4, eo_pr, eo_xx; the 2026-11 snapshot in `rcp/bmf`).
- **Fidelity Charitable, 2025 Giving Report** (CY2024): https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf. See p.20, "Distribution of grant dollars and volumes, by charitable sector", and the appendix; the methodology is on p.19.
- **Fidelity Charitable, 2026 Giving Report** (CY2025): https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf. See p.9, "Granting by charitable sector in 2025". The methodology on p.12 states the $727m outlier removal.
- **Vanguard Charitable, 2024 annual report:** https://www.vanguardcharitable.org/2024annualreport ("Top cause areas"; 240,064 total grants issued; calendar year, footnote 1).
- **Vanguard Charitable, 2025 annual report:** https://www.vanguardcharitable.org/2025annualreport ("Top cause areas"; 267,838 total grants issued).
- **DAFgiving360, Fiscal Year 2025 Giving Report:** https://www.dafgiving360.org/resource/giving-report. Not fetched (robots.txt 403); search snippet only [S].
- **Repo inputs:**
  - [`coverage-gap-decomposition-2026-11-20.csv`](../../data/mission-2026-11-14/coverage-gap-decomposition-2026-11-20.csv);
  - [`daf-foreign-grants-schedule-f-2023-2024.csv`](../../data/mission-2026-11-14/daf-foreign-grants-schedule-f-2023-2024.csv);
  - [`daf-to-daf-recipient-whitelist.csv`](../../data/mission-2026-11-14/daf-to-daf-recipient-whitelist.csv);
  - [`dafrc-sponsor-schedule-d-fy2019-2024.csv`](../../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv);
  - [`daf-grant-recipient-sectors-top50.csv`](../../data/mission-2026-11-14/daf-grant-recipient-sectors-top50.csv) (the top-50 comparison).
