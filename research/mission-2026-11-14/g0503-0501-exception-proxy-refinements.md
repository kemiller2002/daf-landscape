# P-G05-03 and P-G05-01: refinements to the exception-load proxy (fiscal sponsors; time-correct recent rulings)

**Date:** 2026-11-19 · **Task:** g0503-0501 · **Queue items:** P-G05-03 and P-G05-01 (from [queue-proposals-gap19-05.csv](../../data/mission-2026-11-14/queue-proposals-gap19-05.csv)) · **Builds on:** [gap19-exception-load-proxy.md](gap19-exception-load-proxy.md), including its wave-32A corrections and the regeneration note (Greater Horizons totals row dropped). The governing base is 608,610 recipient lines and $92.72bn.

**Outputs**
- [`data/mission-2026-11-14/exception-proxy-refined-2026-11-19.csv`](../../data/mission-2026-11-14/exception-proxy-refined-2026-11-19.csv): 167 rows, with the same row types and scopes as `exception-load-proxy-2026-11-19.csv`.
  - It has 206 columns: the base columns under refined definitions, the `base_*` comparison columns, and the sub-category columns (§7.1).
- [`data/mission-2026-11-14/fiscal-sponsor-ein-list-2026-11-19.csv`](../../data/mission-2026-11-14/fiscal-sponsor-ein-list-2026-11-19.csv): 433 host rows and 347 distinct EINs (§7.2).
- [`scripts/mission_exception_refined.py`](../../scripts/mission_exception_refined.py): stdlib, functional style.
  - It imports `mission_exception_load.py` unchanged (`line_flags`, `tally`, `shares`, `build_rows`, `drop_totals_rows`, `FISCAL_SPONSORS`, `FISCAL_MARKER` and so on). That file was not modified.
- [`data/mission-2026-11-14/queue-proposals-g0503-0501.csv`](../../data/mission-2026-11-14/queue-proposals-g0503-0501.csv): P-G0503-01..06.

**Labels:** **[F]** filed or published value; **[C]** computed by the script; **[I]** inference.

**Framing.** As in the parent note, a flag means a line would plausibly fall outside a sponsor's routine path. It does not mean the grant was improper.

---

## 0. Answers in brief

| Question | Answer [C] |
|---|---|
| **(A) Fiscal-sponsor share**, 19-name list → EIN-keyed list | **0.12% → 0.44% of lines; 1.31% → 1.94% of dollars.** That is 740 → 2,682 lines and $1.212bn → $1.800bn.<br>The dollar ÷ count ratio falls from **10.7× to 4.4×**. The directory adds many hosts with smaller lines.<br>(The parent note's 1.30% is on the pre-regeneration denominator of $92.94bn. On $92.72bn the base is 1.31%.) |
| … components | - 19 Q-B15 hosts, now EIN-keyed (20 EINs): 825 lines, $1.268bn.<br>- Hosts found only in the Fiscal Sponsor Directory: **1,965 lines, $557.1m**.<br>- Excluded as community-foundation / United Way hosts: 113 lines, $25.7m.<br>- Blank-EIN name fallback: 2 lines, $0.68m. Generic markers: 4 lines, $60k.<br>- Including the excluded hosts: 0.46% / 1.97%. |
| **(B) Recent ruling, time-correct** | Of the 29,082 flagged lines ($5.520bn):<br>- **25,185 lines ($4.951bn) carried a recent ruling at grant time**: 4.14% of lines, 5.34% of dollars, against 4.78% / 5.95% before.<br>- **True new organisations: 19,231 lines, $4.376bn (3.16% / 4.72%).** |
| … split of the 29,082 lines | - new organisation: 19,218 lines, $4,373.7m;<br>- new group subordinate: 13 lines, $2.4m;<br>- **newly listed church: 3,047 lines, $356.1m**;<br>- **reinstatement: 1,974 lines, $84.1m**;<br>- **re-determination: 933 lines, $134.5m**;<br>- **not recent at grant time (ruling reset after the grant): 2,561 lines, $411.4m**;<br>- after the grant year: new organisation 52 lines ($87.8m), church 1,015 ($58.2m), other 269 ($12.3m). |
| **Core union** | **7.41% / 10.96% → 7.76% / 11.61%** of lines / dollars. The gap is +3.85 pp.<br>Counting only true new organisations as "recent": **6.80% / 11.00%**. |
| **Broad union** | 25.08% / 19.72% → **24.79% / 19.85%**. |
| What moved the core | - Fiscal-sponsor list alone (original recent flag): 7.73% / 11.59%, i.e. **+0.32 pp lines, +0.63 pp dollars**.<br>- Time-correct recent ruling on top of that: +0.03 / +0.02 pp. The in-window set is almost unchanged, because 277 lines drop out and 470 come in.<br>- New organisations only: −0.96 / −0.61 pp. |
| Archived BMF available? | **Yes.** NCCS publishes the monthly IRS EO BMF as a dated public mirror. 37 complete months (2023-06 to 2026-07) and the NCCS legacy files of 2022-01 and 2022-08 were used.<br>The fallback proxy (first appearance in the e-file index) was also computed for comparison (§3.2). |

**Reading [I]**
- Both refinements leave the headline roughly where it was: core about **7.8% of lines and 11.6% of dollars**, broad about 25% / 20%. They change what sits inside it.
- **Fiscal sponsors** are about three times more common by count than the 19-name list showed (0.44% of lines). They are less extreme by dollar weight (4.4×, not 10.7×). The largest additions are intermediaries such as Global Impact, NEO Philanthropy, King Baudouin Foundation US and Give2Asia, plus some hosts with large programmes of their own (50CAN, $94.2m). For those, "fiscal sponsor" is an upper bound (P-G0503-01).
- **New grantees.** About one in three recent-ruling lines (9,799 of 29,082; $1.06bn of $5.52bn) is *not* a new organisation. These are:
  - rulings reset after the grant: 2,561 lines, $411m;
  - reinstatements: 1,974 lines, $84m;
  - re-determinations: 933 lines, $135m;
  - newly listed churches: 3,047 lines, $356m, plus 1,015 lines ($58m) listed only after the grant year;
  - other rulings after the grant year: 269 lines, $12m.
- The new-grantee cohort proper is **3.2% of lines and 4.7% of dollars**. Its dollars are concentrated: SVCF's $1.309bn Further Future Foundation line is still a true new organisation (ruling 2023-03, present in the 2023-06 BMF with that month).

---

## 1. Method

### 1.1 (A) Fiscal-sponsor list, EIN-keyed (P-G05-03)

1. **Sources tried (robots.txt, 2026-11-19):**
   - **Fiscal Sponsor Directory** (`fiscalsponsordirectory.org`). robots.txt is `User-Agent: * / Disallow:` (empty), so every path is allowed. **Used:** one page, [All Fiscal Sponsors (alpha ordered)](https://fiscalsponsordirectory.org/all-fiscal-sponsors-alpha-ordered/) (HTTP 200, 242,714 bytes). It lists **413 hosts** with name, city and state. Listing pages have no EIN (one sample, Community Partners, was checked), so the remaining ~440 pages were not crawled.
   - **National Network of Fiscal Sponsors** (`www.fiscalsponsors.org`). robots.txt is a Squarespace file: `/config`, `/search`, `/account`, `/api/`, `/static/` and some query patterns are disallowed for all agents. The named AI agents share that `*` group, and `/member-directory` is allowed. The [member directory](https://www.fiscalsponsors.org/member-directory) page (HTTP 200) has **no member list in its HTML**. The list is rendered client-side by a third-party script (`cfapi.communitybox.co` / `dashboard.communitybox.co`). **Not used:** this would mean calling a widget API, with membership gating via memberspace. No login was attempted.
2. **19 Q-B15 hosts.**
   - These are recipient EINs whose **current BMF name** matches the original `FISCAL_SPONSORS` regex: 17 EINs, with two for Tides (Foundation and Center).
   - Three hosts are not in the 2026-11 BMF: Players Philanthropy Fund, Open Collective Foundation and Trust for Conservation Innovation (now "Multiplier"). For these the script takes the **modal EIN that sponsors reported** on Schedule I lines matching the regex, when it covers at least half of them. This gave 276601178, 814004928 and 912166435.
   - These hosts are always counted.
3. **Directory hosts → EIN** (current EO BMF, 2026-11-09), in this order:
   - exact normalised name + state (292), or + city (1);
   - **near match in the same city** (27): same token set, one name containing the other with at least 2 non-generic tokens, or a 40-character truncated BMF name [I];
   - for hosts still unmatched or ambiguous, **the single EIN sponsors reported on Schedule I** for the same normalised name, with the BMF state equal to the host's state when the EIN is in the BMF (17) [I].
   - This keyed **337 of 413** hosts. 71 are unmatched and 5 ambiguous; all are listed in the CSV with `match_method`.
   - Spot checks of the Schedule I pass agree with known legal names: The Field = Performance Zone Inc; Fresh Arts = Spacetaker; Heluna Health = Public Health Foundation Enterprises; Players Philanthropy Fund = Stonier Scholarship Inc (Pub 78 name for 27-6601178).
4. **Exclusion.** Directory hosts that are **community foundations or United Ways** (BMF NTEE T31 / T70, or "Community Foundation" / "United Way" in the name) are listed but not counted in the headline flag. There are 15 EINs, 113 lines and $25.7m. Grants to them are mostly to their own or donor funds. A broader rule (all NTEE T codes) was tested and rejected: it would have excluded Tides Foundation and known hosts such as Community Initiatives and New Horizons Foundation.
5. **Line flag** (`fiscal_sponsor_name`, refined): recipient EIN on the list (excluded hosts aside); or blank EIN with a name matching the old regex or a directory host name exactly; or a generic marker ("fiscal sponsor/agent", "a project of", "sponsored project").

### 1.2 (B) Time-correct recent ruling (P-G05-01)

1. **Scope:** the 29,082 lines (15,096 EINs) flagged `recent_ruling_24m` by the unchanged script. Their 2026-11 BMF ruling month is on or after grant-year start − 24 months.
2. **Archived BMF** (the IRS URLs serve only the current extract, Last-Modified 2026-11-09 in cache; no dated IRS copies were found):
   - NCCS mirror of the IRS EO BMF, `https://nccsdata.s3.us-east-1.amazonaws.com/raw/bmf/{YYYY-MM}-BMF.csv`. The NCCS catalog describes these as "the unmodified IRS or NCCS file — Raw archives (for replication only)" ([NCCS BMF catalog](https://nccs.urban.org/nccs/catalogs/catalog-bmf.html)).
   - Months 2023-06 to 2026-07 return HTTP 200, with Last-Modified on the 1st of each month from 2023-08 onward (2023-06: 18 Jun 2023; 2023-07: 5 Jul 2023). 2022-09 to 2023-05 and 2026-08 to 2026-10 return 403.
   - The files are the IRS layout with leading zeros stripped from EIN and codes, and with REGION / RYEAR / ID appended.
   - Each month was **streamed and filtered** to the 171,369 recipient EINs (`--filter-archive`); nothing over 1 MB was stored unfiltered.
   - **2023-08 is truncated** (1,409,209 rows against about 1.83–1.97m; Content-Length 294.8 MB). It is dropped by rule: filtered rows below 90% of the median.
   - Four pairs of months have identical Content-Length (2024-01/02, 2025-01/02, 2025-10/11, 2026-01/02), consistent with no IRS update that month.
   - **Prior existence:** NCCS legacy BMF `legacy/bmf/BMF-2022-01-501CX-NONPROFIT-PX.csv` and `BMF-2022-08-…`, field `RULEDATE`. The 2020-04 file was not used (rule: 2021+ evidence only).
3. **As-of snapshot:** the first complete monthly file dated after the grant-year end month (a file dated the 1st of M reflects month M−1).
   - For year ends from 2023-03 to 2023-05 this is 2023-06. These are 336 lines ($121.4m) with a gap of 3 months or more (`rr_asof_lag_ge3m`).
4. **Reference ruling:** the ruling month in the as-of snapshot. If the EIN is absent there, it is the first ruling month in a later snapshot, or failing that the 2026-11 month.
5. **Earlier-existence evidence** (any one is enough):
   - **reinstatement:** an IRS auto-revocation ([revocation list](https://apps.irs.gov/pub/epostcard/data-download-revocation.zip), cached 2026-11-11) dated before the reference month (2,044 of the 15,096 EINs have a revocation record);
   - **re-determination:**
     - an older ruling month in any earlier snapshot (2022 legacy or monthly); or
     - an e-filed return in the IRS e-file index ([index_2021–2026.csv](https://www.irs.gov/charities-non-profits/form-990-series-downloads)) for a tax period at least **36 months** before the reference month. The 36 months allows for a first return retroactive to formation.
6. **Classes** (`rr_*`):
   - `dropped_reset_after_grant`: the reference ruling is before the cutoff, so the ruling was not recent at grant time;
   - in window [start − 24 months, end], `tc_*` (all count in the time-correct flag):
     - `tc_reinstatement`, `tc_redetermination` (by the evidence above);
     - otherwise `tc_newly_listed_church` if the line carries the P-NEW-REC-01 church/religious label (churches need no application, so a first ruling does not date them) [I];
     - otherwise `tc_new_subordinate` (BMF GROUP ≠ 0) or `tc_new_org`;
   - after the grant year: `after_period_new_org`, `after_period_church`, `after_period_other`.
7. **Refined flags:**
   - `recent_ruling_24m` = `tc_*` + `after_period_new_org`; this is the broad union's component.
   - `any_core` uses `tc_*`, as the original core used only in-window rulings.
   - `any_core_new_only` uses `tc_new_org` + `tc_new_subordinate`.
8. **Fallback proxy, kept for comparison:** `rr_efile_proxy_new` marks a line as new when the EIN has no e-filed return for a tax period before the cutoff month (index 2021–2026). It is restricted to base in-window lines.

### 1.3 Unchanged

Universe, returns, Schedule I lines, Schedule F denominators, the foreign, not-c3/not-Pub-78 and PF/ER categories, and every other column are exactly those of `mission_exception_load.py`. The `base_*` columns reproduce the governing CSV for the all-sponsor scope (7.41% / 10.96% core; 25.08% / 19.72% broad).

## 2. Coverage and checks [C]

- 94 itemised sponsor-years, 608,610 lines and $92.72bn, identical to the regenerated base.
- 171,369 recipient EINs in the line set. The archive filter used them without the two placeholder EINs, 000000001 and 999999999, which are treated as blank in any case.
- **Archive rows per month** after filtering to recipient EINs: 143,490 (2023-06) to 150,264 (2024-08); legacy 140,571 (2022-01) and 143,994 (2022-08).
- 10,827 of the 15,096 recent-ruling EINs appear in the e-file index.
- **Base vs refined, recent-ruling lines:**

  | Base status (2026-11 ruling) | → Refined class | Lines | $m |
  |---|---|---|---|
  | in window (24,992 lines) | tc_new_org | 18,825 | 4,350.8 |
  | | tc_newly_listed_church | 3,017 | 354.3 |
  | | tc_reinstatement | 1,938 | 82.8 |
  | | tc_redetermination | 922 | 128.5 |
  | | tc_new_subordinate | 13 | 2.4 |
  | | dropped_reset_after_grant | 272 | 12.8 |
  | | after_period_other | 5 | 0.1 |
  | after grant year (4,090 lines) | dropped_reset_after_grant | 2,289 | 398.6 |
  | | after_period_church | 1,015 | 58.2 |
  | | tc_new_org | 393 | 22.9 |
  | | after_period_other | 264 | 12.2 |
  | | after_period_new_org | 52 | 87.8 |
  | | tc_reinstatement / tc_redetermination / tc_newly_listed_church | 36 / 11 / 30 | 1.4 / 6.1 / 1.8 |

  **Reading:**
  - The parent note's guess was right: most of the 4,090 after-period lines (2,289, $398.6m) belonged to organisations the BMF already listed at grant time with an old ruling. Examples, with the as-of ruling first and the 2026-11 ruling second:
    - Charter Fund: 2005-05 / 2025-08, $76.8m;
    - Musical Instrument Museum: 2006-03 / 2025-08, $36.2m;
    - Life Covenant Church: 1975-07 / 2025-12, $30.8m.
  - BM-A Institute ($83.1m, ruling 2024-09) is a genuine after-period new organisation: it is absent from every snapshot before then.

## 3. Results

### 3.1 Fiscal sponsors (P-G05-03) [C]

All 48 sponsors, FY2023–24 pooled:

| Measure | Lines | $ | Count share | $ share | $ ÷ count |
|---|---|---|---|---|---|
| Base: 19-name regex + markers | 740 | $1,211.6m | 0.12% | 1.31% | 10.7× |
| Q-B15 hosts, EIN-keyed | 825 | $1,267.7m | 0.14% | 1.37% | 10.1× |
| Directory-only hosts | 1,965 | $557.1m | 0.32% | 0.60% | 1.9× |
| **Refined flag (headline)** | **2,682** | **$1,799.8m** | **0.44%** | **1.94%** | **4.4×** |
| Including community-foundation / United Way hosts | 2,795 | $1,825.5m | 0.46% | 1.97% | 4.3× |
| … of which DAF-to-DAF lines (whitelist) | 193 | $145.3m | 0.03% | 0.16% | — |

- **Largest directory-only hosts** (top-50 Schedule I $, lines):
  - 50CAN Inc $94.2m (14);
  - Global Impact $51.5m (35);
  - NEO Philanthropy $47.5m (44);
  - King Baudouin Foundation US $46.5m (54);
  - Edward Charles Foundation $23.5m (30);
  - New Horizons Foundation $20.2m (33);
  - Global Fund for Women $17.2m (33);
  - Community Initiatives $12.5m (30);
  - Give2Asia $12.0m (17);
  - Panorama Global $10.4m (29).
- **Q-B15 hosts:** EIN keying adds "Multiplier" lines (Trust for Conservation Innovation's new name; $43.5m in all) and others filed under variant names.
- 221 of the directory EINs receive at least one top-50 Schedule I line.
- **DAF-to-DAF overlap:** $112.2m of the $145.3m is Tides Foundation, which is also on the DAF-to-DAF whitelist (as in the base).

**By sponsor type**, fiscal-sponsor count / $ share, base → refined:

| Sponsor type | Base | Refined |
|---|---|---|
| National (29 sponsor-years) | 0.08% / 1.49% | 0.32% / 2.09% |
| Community foundation (43) | 0.34% / 1.02% | **1.19% / 1.67%** |
| Faith (14) | 0.13% / 0.99% | 0.32% / 2.02% |
| Big-4 nationals | 0.04% / 1.47% | 0.24% / 2.05% |

**Largest sponsor-level moves** in fiscal-sponsor dollar share:

| Rank | Sponsor | Base | Refined | Core $ |
|---|---|---|---|---|
| 19 | CJP Boston | 1.20% | 4.73% | 6.14% → 9.67% |
| 24 | New York Community Trust | 1.76% | 4.93% | 5.95% → 9.09% |
| 15 | Jewish Communal Fund | 4.09% | 7.13% | — |
| 42 | Seattle Foundation | 0.74% | 3.32% | — |
| 48 | San Francisco Foundation | 2.91% | 4.60% | — |

### 3.2 Recent rulings (P-G05-01) [C]

Shares of all lines and dollars (608,610 lines; $92.72bn):

| Measure | Lines | $ | Count share | $ share |
|---|---|---|---|---|
| Base `recent_ruling_24m` (2026-11 ruling) | 29,082 | $5,520.4m | 4.78% | 5.95% |
| Base, in window only (used in core) | 24,992 | $4,931.7m | 4.11% | 5.32% |
| **Time-correct, recent at grant time (`rr_tc`)** | **25,185** | **$4,950.8m** | **4.14%** | **5.34%** |
| … true new organisations (`tc_new_org` + `tc_new_subordinate`) | **19,231** | **$4,376.1m** | **3.16%** | **4.72%** |
| … newly listed churches | 3,047 | $356.1m | 0.50% | 0.38% |
| … reinstatements | 1,974 | $84.1m | 0.32% | 0.09% |
| … re-determinations | 933 | $134.5m | 0.15% | 0.15% |
| Refined broad component (`tc` + after-period new orgs) | 25,237 | $5,038.6m | 4.15% | 5.43% |
| Not recent at grant time (dropped) | 2,561 | $411.4m | 0.42% | 0.44% |

- **Largest true new-organisation recipients** (as-of ruling = 2026-11 ruling):
  - Further Future Foundation (SVCF), $1,309.0m, 2023-03;
  - Come and See Foundation, $139.9m (30 lines), 2022-10;
  - The Just Trust for Education, $131.6m, 2023-02;
  - Our American Future Foundation, $118.8m (19), 2022-11.
- **Largest re-determinations:**
  - Telescope Fund, $33.1m, 2023-05;
  - New Leaders, $10.5m, 2022-07;
  - Yeshivat Darche Eres, $7.1m, 2022-12.
- **Largest reinstatements:**
  - Affordable Housing for Artists, $4.9m, 2021-12;
  - Oyate Group, $3.3m, 2022-08.
- **By sponsor type**, time-correct recent count / $ share (base → refined; true new organisations only):
  - National: 4.64% / 4.37% → 4.00% / 3.77% (3.03% / 3.29%);
  - Community foundation: 4.53% / 11.04% → 4.03% / 10.73% (3.42% / 10.53%);
  - **Faith: 6.20% / 6.89% → 5.36% / 5.38% (3.74% / 2.81%)**. Faith sponsors lose the most when churches and reinstatements are split out;
  - Big-4: 4.91% / 4.25% → 4.21% / 3.65% (3.18% / 3.20%).
- **Largest dollar falls from rulings reset after the grant:**
  - Fidelity: $61.7m; recent share 4.54% → 4.17%;
  - Goldman Sachs Philanthropy Fund: $61.2m; 4.99% → 3.80%;
  - NCF: $56.5m; 6.14% → 4.69%;
  - NPT: $48.0m; 3.98% → 2.64%;
  - Servant Foundation: $45.8m; 14.04% → 10.64%.
- **Fallback proxy (e-file first appearance), compared with the archive:**
  - The proxy calls 18,382 of the 19,218 archive-classed new-organisation lines new (95.6%).
  - It also calls new 3,004 newly listed church lines, 1,659 reinstatement lines and 413 re-determination lines.
  - Its in-window "new" count, 23,158 lines and $4,668.8m (3.81% / 5.04%), is therefore about 20% above the archive-based new-organisation count. That is the expected bias of a proxy that cannot see revocations or non-filers.

### 3.3 Proxy unions, before and after [C]

Count / dollar share. "Core, new orgs only" counts only `tc_new_org` + `tc_new_subordinate` as recent.

| Scope | Sponsor-years | Fiscal sponsor (base) | Fiscal sponsor (refined) | Recent (base) | Recent (time-correct) | Recent, new orgs only | Core (base) | **Core (refined)** | Core, new orgs only | Broad (base) | **Broad (refined)** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| All top-50 itemising | 94 | 0.12% / 1.31% | 0.44% / 1.94% | 4.78% / 5.95% | 4.14% / 5.34% | 3.16% / 4.72% | 7.41% / 10.96% | **7.76% / 11.61%** | 6.80% / 11.00% | 25.08% / 19.72% | **24.79% / 19.85%** |
| Excl. university/hospital | 90 | 0.12% / 1.32% | 0.44% / 1.96% | 4.78% / 6.01% | 4.14% / 5.39% | 3.16% / 4.76% | 7.34% / 11.04% | 7.69% / 11.70% | 6.73% / 11.08% | 25.03% / 19.89% | 24.75% / 20.02% |
| … and excl. SVCF | 88 | 0.12% / 1.37% | 0.43% / 2.01% | 4.75% / 4.65% | 4.11% / 3.98% | 3.12% / 3.30% | 7.23% / 9.61% | 7.56% / 10.27% | 6.60% / 9.60% | 25.08% / 17.28% | 24.77% / 17.36% |
| Big-4 nationals | 8 | 0.04% / 1.47% | 0.24% / 2.05% | 4.91% / 4.25% | 4.21% / 3.65% | 3.18% / 3.20% | 7.32% / 10.02% | 7.55% / 10.62% | 6.54% / 10.17% | 28.25% / 17.82% | 27.79% / 18.00% |
| National (excl. Servant) | 29 | 0.08% / 1.49% | 0.32% / 2.09% | 4.64% / 4.37% | 4.00% / 3.77% | 3.03% / 3.29% | 7.02% / 9.88% | 7.29% / 10.49% | 6.33% / 10.02% | 26.47% / 17.55% | 26.10% / 17.70% |
| Community foundation | 43 | 0.34% / 1.02% | 1.19% / 1.67% | 4.53% / 11.04% | 4.03% / 10.73% | 3.42% / 10.53% | 8.51% / 16.17% | 9.39% / 16.84% | 8.80% / 16.64% | 17.49% / 28.89% | 17.86% / 29.27% |
| Faith | 14 | 0.13% / 0.99% | 0.32% / 2.02% | 6.20% / 6.89% | 5.36% / 5.38% | 3.74% / 2.81% | 8.13% / 9.14% | 8.38% / 10.21% | 6.77% / 7.63% | 24.60% / 19.26% | 23.97% / 18.82% |
| DonorsTrust | 2 | 0.35% / 0.01% | 0.41% / 0.02% | 9.50% / 6.86% | 8.68% / 6.70% | 8.04% / 6.56% | 12.02% / 8.22% | 11.96% / 8.20% | 11.38% / 8.07% | 16.42% / 13.02% | 15.84% / 12.92% |
| FY2023 | 46 | 0.13% / 1.22% | 0.44% / 1.86% | 4.71% / 7.62% | 3.95% / 7.03% | 3.07% / 6.34% | 7.47% / 12.42% | 7.84% / 13.08% | 6.96% / 12.40% | 25.33% / 23.47% | 24.92% / 23.54% |
| FY2024 | 48 | 0.12% / 1.38% | 0.44% / 2.01% | 4.84% / 4.55% | 4.30% / 3.91% | 3.24% / 3.36% | 7.36% / 9.73% | 7.69% / 10.37% | 6.65% / 9.82% | 24.87% / 16.56% | 24.68% / 16.74% |

- **Core gap** (dollar share − count share): +3.55 pp (base) → **+3.85 pp** (refined); +4.20 pp on the new-organisations-only core.
- The broad union's dollar ÷ count ratio is 0.80×, against 0.79× in the base.
- Processor (Dechomai) and university/hospital rows hardly change; they are in the CSV.

**Reading [I]**
- The core proxy's "about 7% of lines, 10–11% of dollars" (parent note §0) becomes **about 7.8% / 11.6%**. On the stricter new-grantee definition it is **6.8% / 11.0%**.
- The refinements push in opposite directions: the fiscal-sponsor list raises the core and the new-organisation split lowers it. Each moves it by less than one percentage point.
- Community foundations still carry the heaviest core dollar load (16.8%), and their fiscal-sponsor count share (1.19%) is now nearly four times the nationals' (0.32%).

## 4. Comparison with the four-national measure (parent §4)

- The like-for-like component of the existing "2.5–3%" measure used the 19-host list: 1.50% of the four nationals' Schedule I dollars. On the EIN-keyed list it is **2.10% of Schedule I dollars** (`fiscal_sponsor_any_share_of_sched_i_usd`, big-4 row), or 2.05% of proxy dollars and 0.24% of lines [C].
- The like-for-like simple sum therefore rises from ≈3.6% to **≈4.2% of dollars**: 1.96% foreign + 2.10% fiscal sponsors + 0.15% non-501(c)(3) IRC text [C]. This is still above the FY6/2025 "2.5–3%".
- The count-side claim ("0.3–1% by count at nationals") still holds for foreign + fiscal-sponsor lines. The big-4 fiscal-sponsor count share is 0.24%, against 0.04% before [C].

## 5. Limits

- **Directory listing is self-reported, and a host's EIN is not a project.**
  - Every grant to a listed host is flagged, including grants to the host's own programmes. Examples are 50CAN, Global Fund for Women and Open Space Institute.
  - The directory-only $557.1m is therefore an upper bound (P-G0503-01).
  - Conversely, hosts absent from the directory are missed: 71 directory hosts are unmatched and 5 ambiguous. The NNFS list could not be read (§1.1).
- **Matching is inference.**
  - Near matches (27) and the Schedule I-reported pass (17) rest on name, city or state agreement. Two of the 17 are uncertain: United Way of Southwest Colorado → "Team Up" (EIN 237113221; $42k) and SPM Disability Justice Fund → "Disability Power Bloc" ($31k). Both are immaterial.
  - The community-foundation / United Way exclusion is a judgement. Including those hosts changes the share by +0.02 pp lines and +0.03 pp dollars.
- **Archive coverage:**
  - No usable dated BMF exists for 2022-09 to 2023-05 (NCCS 403; web.archive.org was unreachable from this session: connection reset at the network proxy, so its robots.txt could not be read and it was not used).
  - FY2023 years ending 2023-03 to 2023-05 rely on the 2023-06 file (336 lines, $121.4m; P-G0503-05).
  - The 2023-08 file is truncated and was dropped. NCCS's re-hosting (leading zeros stripped, columns appended) was normalised.
- **Earlier-existence evidence is incomplete:**
  - Small organisations filing 990-N are not in the e-file index, so some reinstatements and re-determinations look "new".
  - Revocation records give the revocation date, and the BMF gives the new ruling month; the reinstatement letter itself is not public.
  - The 36-month e-file rule and the church rule are judgements [I].
- **Churches:** the 3,047 newly listed church lines ($356.1m) stay in the time-correct flag. They are only excluded from the new-organisations-only core (P-G0503-04).
- All other limits of the parent note apply: recipient-level Schedule I, community-foundation non-DAF grants, attachment-only sponsors (BofA, Renaissance), and no observed routing.

## 6. Reproduction

```
# 1. recipient EINs
python3 scripts/mission_exception_refined.py . --np-cache NPCACHE --lines-cache LINES --bmf-dir BMF \
    --pub78 data-download-pub78.txt --write-eins EINS.txt
# 2. each month M in 2023-06..2026-07 (and the legacy 2022 files with --legacy)
curl -sS -A research-script/1.0 https://nccsdata.s3.us-east-1.amazonaws.com/raw/bmf/M-BMF.csv | \
    python3 scripts/mission_exception_refined.py . --filter-archive EINS.txt > ARCH/M.csv
curl -sS -A research-script/1.0 https://nccsdata.s3.us-east-1.amazonaws.com/legacy/bmf/BMF-2022-08-501CX-NONPROFIT-PX.csv | \
    python3 scripts/mission_exception_refined.py . --filter-archive EINS.txt --legacy > ARCH/L2022-08.csv
# 3. the directory page, saved as all-fiscal-sponsors-alpha-ordered.html
# 4. run (about 90 s)
python3 scripts/mission_exception_refined.py . --np-cache NPCACHE --lines-cache LINES --bmf-dir BMF \
    --pub78 data-download-pub78.txt --revocation data-download-revocation.txt --efile-index-dir IRS \
    --bmf-archive-dir ARCH --fsd-html all-fiscal-sponsors-alpha-ordered.html [--out PATH] [--fs-list-out PATH]
```
- The inputs are as in parent §6, plus:
  - IRS = the folder holding `index_2021.csv`–`index_2026.csv`;
  - ARCH = the filtered archive files (`YYYY-MM.csv`, `LYYYY-MM.csv`).
- The run prints a JSON summary with:
  - match methods;
  - Q-B15 EINs;
  - archive months used and dropped;
  - the class totals;
  - the base → refined cross-tab;
  - the e-file proxy cross-tab;
  - the all-sponsor shares;
  - top recipients per sub-category.
- Every figure here comes from that CSV or summary.

## 7. Data dictionaries

### 7.1 `exception-proxy-refined-2026-11-19.csv` (167 rows × 206 columns)

| Column(s) | Meaning |
|---|---|
| row_type … `sponsor_any_*` | Same columns, rows and definitions as `exception-load-proxy-2026-11-19.csv` ([parent §7](gap19-exception-load-proxy.md#7-data-dictionary-exception-load-proxy-2026-11-19csv)), **except**:<br>- `fiscal_sponsor_name_*` is the EIN-keyed flag (§1.1).<br>- `recent_ruling_24m_*` is `tc_*` + `after_period_new_org` (§1.2).<br>- `any_*` and `any_core_*` are rebuilt from those.<br>- `recent_ruling_after_period_end_*` counts `after_period_*` classes.<br>- `fiscal_sponsor_listed_share_of_sched_i_usd` uses keyed hosts plus name fallback.<br>- The `sponsor_any_*` distributions use the refined broad union. |
| fs_q19_ein_* | Lines whose EIN is one of the 20 Q-B15 host EINs |
| fs_fsd_ein_*, fs_fsd_only_ein_* | Lines whose EIN is a directory host; … and not a Q-B15 host |
| fs_name_fallback_*, fs_marker_* | Blank-EIN lines matched by name; generic-marker lines |
| fs_grantmaker_host_* | Lines to directory hosts excluded as community foundation / United Way |
| fs_all_incl_grantmakers_* | Fiscal-sponsor flag without that exclusion |
| fs_d2d_* | Headline fiscal-sponsor lines that are also DAF-to-DAF (whitelist) |
| rr_base_* | The unchanged recent-ruling flag (= `base_recent_ruling_24m_*`) |
| rr_tc_* | Recent at grant time (all `tc_*` classes) |
| rr_{class}_* | Lines per class (§1.2.6):<br>- `tc_new_org`, `tc_new_subordinate`, `tc_newly_listed_church`, `tc_reinstatement`, `tc_redetermination`;<br>- `dropped_reset_after_grant`;<br>- `after_period_new_org`, `after_period_church`, `after_period_other`. |
| rr_asof_lag_ge3m_* | `rr_tc` lines whose as-of snapshot is at least 3 months after the year end |
| rr_efile_proxy_new_*, rr_efile_proxy_new_and_tc_* | Fallback proxy (no e-filed return for a tax period before the cutoff): on base in-window lines, and on `rr_tc` lines |
| any_core_new_only_*, any_core_new_only_gap_pp | Core union with only true new organisations as "recent"; includes Schedule F like `any_core` |
| any_core_fs_all_* | Refined core including community-foundation / United Way hosts |
| any_core_base_recent_* | Core with the refined fiscal-sponsor flag but the original recent-ruling flag (isolates the P-G05-03 effect) |
| base_{fiscal_sponsor_name, recent_ruling_24m, any, any_core}_{lines, usd, count_share, usd_share}, base_any_core_gap_pp | The same scope from the unchanged script |
| *_count_share, *_usd_share | On the row's `denom_lines` / `denom_usd` (Schedule I + Schedule F) |
| source | Provenance string |

### 7.2 `fiscal-sponsor-ein-list-2026-11-19.csv` (433 rows)

| Column | Meaning |
|---|---|
| source | `q_b15_19_list` (20 rows) or `fiscalsponsordirectory` (413 rows) |
| host_name, host_location, host_url, host_state | As listed (directory) or BMF / matched name (Q-B15); parsed state |
| match_method | One of:<br>- `name_state`, `name_state_city`, `near_name_same_city`, `sched_i_reported_ein`, `unmatched`, `ambiguous` (directory);<br>- `bmf_name_matches_q_b15_regex`, `sched_i_reported_modal_ein` (Q-B15). |
| ein | Keyed EIN (blank if unmatched or ambiguous) |
| bmf_name, bmf_city, bmf_state, bmf_subsection, bmf_ntee, bmf_ruling | From the 2026-11 EO BMF where available |
| grantmaker_host | True when excluded from the headline flag (community foundation / United Way, not Q-B15) |
| top50_sched_i_lines, top50_sched_i_usd | Top-50 FY2023–24 Schedule I lines and dollars to that EIN |

## 8. Source register

| ID | Source | Version / access | robots.txt (checked 2026-11-19) |
|---|---|---|---|
| S1 | Parent inputs: Schedule I lines, Schedule F, Pub 78, EO BMF 2026-11, DAFRC panel, DAF-to-DAF whitelist (parent §8, S1–S4, S11) | cached; unchanged | as parent |
| S2 | [Fiscal Sponsor Directory: All Fiscal Sponsors (alpha ordered)](https://fiscalsponsordirectory.org/all-fiscal-sponsors-alpha-ordered/); sample listing [Community Partners](https://fiscalsponsordirectory.org/?page_id=459) | HTTP 200, 2026-11-19; 413 hosts | `User-Agent: * / Disallow:` (all allowed) |
| S3 | [NNFS member directory](https://www.fiscalsponsors.org/member-directory) | HTTP 200; list not in HTML (communitybox.co widget); not used | `/member-directory` allowed; `/api/`, `/search`, `/config`, `/account` disallowed |
| S4 | [NCCS BMF catalog](https://nccs.urban.org/nccs/catalogs/catalog-bmf.html) and [BMF dataset page](https://nccs.urban.org/nccs/datasets/bmf/) | HTTP 200 | robots.txt 404 (no rules) |
| S5 | NCCS raw monthly IRS EO BMF, e.g. [2024-06-BMF.csv](https://nccsdata.s3.us-east-1.amazonaws.com/raw/bmf/2024-06-BMF.csv); 2023-06 … 2026-07 | Last-Modified 2023-06-18 … 2026-07-01; 2023-08 truncated, dropped; 2022-09–2023-05 and 2026-08–10 HTTP 403 | robots.txt → S3 AccessDenied (no robots file) |
| S6 | NCCS legacy BMF [2022-01](https://nccsdata.s3.us-east-1.amazonaws.com/legacy/bmf/BMF-2022-01-501CX-NONPROFIT-PX.csv), [2022-08](https://nccsdata.s3.us-east-1.amazonaws.com/legacy/bmf/BMF-2022-08-501CX-NONPROFIT-PX.csv) | Last-Modified 2023-10-25 | as S5 |
| S7 | [IRS auto-revocation list](https://apps.irs.gov/pub/epostcard/data-download-revocation.zip) | cached copy dated 2026-11-11 (P-NEW-REC-01) | apps.irs.gov robots.txt 404 (per parent) |
| S8 | IRS e-file index `index_2021.csv`–`index_2026.csv` ([Form 990 series downloads](https://www.irs.gov/charities-non-profits/form-990-series-downloads)) | cached copies (2026-11-14/15) | per parent S4: `/pub/` not disallowed |
| S9 | [IRS EO BMF field guide (eo-info.pdf)](https://www.irs.gov/pub/foia/ig/tege/eo-info.pdf): RULING, GROUP, NTEE fields | per parent S5 | per parent |
| S10 | web.archive.org (considered for dated IRS eo1–eo4) | connection reset at the session's network proxy; not used | not readable |
