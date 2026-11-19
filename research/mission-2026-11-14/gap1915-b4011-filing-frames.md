# Two IRS e-file filing frames: new DAF sponsors beyond DAFRC, and community-foundation exits (Schedule N)

**Queue items:** P-GAP19-15-01 (frame A) and P-B40N11-02 (frame B). **Task:** gap1915-b4011. **Prepared:** 2026-11-19.
**Status:** desk research from public filings only; no outreach, no logins.
**Script:** [`scripts/mission_filing_frames.py`](../../scripts/mission_filing_frames.py) (stdlib only, functional style). One run of `--task all` re-derives every number below.
**Outputs:**
- [`data/mission-2026-11-14/daf-startup-cohort-additions-2026-11-19.csv`](../../data/mission-2026-11-14/daf-startup-cohort-additions-2026-11-19.csv): 16 rows (7 new cohort members, 9 screened-out rows).
- [`data/mission-2026-11-14/cf-exits-schedule-n-2021-2026.csv`](../../data/mission-2026-11-14/cf-exits-schedule-n-2021-2026.csv): 195 rows (one per flagged return × Schedule N recipient).
- [`data/mission-2026-11-14/new-daf-holders-frame-2022-2026.csv`](../../data/mission-2026-11-14/new-daf-holders-frame-2022-2026.csv): 179 rows, the full frame-A list of DAF holders (support file for the additions).
- [`data/mission-2026-11-14/queue-proposals-gap1915-b4011.csv`](../../data/mission-2026-11-14/queue-proposals-gap1915-b4011.csv): 6 rows.

**Builds on:** [gap19-startup-cohort.md](gap19-startup-cohort.md) (and its [V wave 32A] corrections, [validation-wave32a-report.md](validation-wave32a-report.md)); [sponsor-mortality-analysis.md](sponsor-mortality-analysis.md); `cf-consolidation-2021-2026.csv` and `scripts/mission_cf_fee_census.py --task schedn`.

Run: `python3 scripts/mission_filing_frames.py . --irs-dir <dir with index_2019..2026.csv> --bmf-dir <dir with eo*.csv> --cache <dir> --task all --fetch`

---

## 1. Bottom line

1. **Only 179 of 36,115 new 501(c)(3) Form 990 filers report any DAF account on Schedule D Part I.** The frame is every Form 990 in the IRS e-file index 2022–2026 whose filer is a 501(c)(3) with a BMF ruling of 2021-01 or later (86,637 returns, 83,020 read). Of the 179 holders, 43 are in the DAFRC panel and 136 are not. After removing organisations with a return or formation year before 2021, 122 holders are in the window: 24 in DAFRC and 98 not.
2. **Most of the 98 non-DAFRC in-window holders are not DAF sponsors.** They are schools, shelters, clubs and ministries that fill Schedule D Part I by mistake: 18 of the 28 with ≥50 "accounts" report $0 of DAF value, and several put dollar amounts in the count field (e.g. 2,435,213 "accounts", $0 value). Applying the cohort's pre-registered rule leaves **7 new cohort members** missed by DAFRC and by the earlier frames: Givmo Charitable Fund, Spiral Giving Network, Neta Foundation, One Big Gift, DAF Gives Charitable (DAFshare), Monument Charitable and Overflow Foundation. All are small (1 to 31 accounts; $0 to $7.6m of DAF assets). 3 are active by a 2026 e-filing; 4 are unknown.
3. **The largest new non-DAFRC sponsor is excluded by rule, not missed.** Bridges Philanthropic Fund (ruled 2025-01) reported 42 DAF accounts and $107.0m on its TY2025 return. It is run by an Omaha wealth manager (Schedule O), so it falls under the "products of pre-2021 incumbents" exclusion, like bank DAF programs. That exclusion is the ambiguous one that wave 32A flagged.
4. **Part IV line 6 is not a safe pre-filter.** Groundswell's amended TY2024 return reports 12,808 DAF accounts and $10.1m in Schedule D Part I while answering "No" on line 6, and its three other returns report no Part I data at all. Across the frame, 14 of 179 holders (7.8%) never answered "Yes" on line 6. The scan therefore read every mirrored return in full instead of relying on line 6.
5. **Community-foundation exits are small, steady and mostly outside DAFRC.** Among 16,947 Form 990/990-EZ returns (2021–2026 index) filed by 3,673 CF-named or NTEE-T31 filers, **24 geographic community foundations filed an exit return** (Schedule N Part I, or the final-return box) with an exit date in 2021–2026: **6 in 2021, 2 in 2022, 4 in 2023, 6 in 2024, 6 in 2025 and 0 so far in 2026**. 23 of the 24 are small (largest observed total assets under $10m; median $248k; 16 under $1m). 12 filed 990-EZ. **19 of the 24 are not in the DAFRC panel.**
6. **Exiting CFs do not name DAF balances on Schedule N.** None of the 24 describes a DAF transfer; the assets are described as cash, investments or a remainder-trust interest. 4 (Rusk County, Fairfield, Milbank, Coastal) still reported DAF accounts on Schedule D of the exit-year return. 9 of the 24 transferred to another community foundation, and 7 filed a final return with no Schedule N Part I.

---

## 2. Method

### 2.1 Common machinery
- **Index.** IRS TEOS e-file index files `index_2019.csv`–`index_2026.csv` (`https://apps.irs.gov/pub/epostcard/990/xml/{YYYY}/index_{YYYY}.csv`), as already downloaded in the scratchpad.
- **BMF.** IRS Exempt Organizations Business Master File extract (eo1–eo4, Puerto Rico and international files, November 2026). Fields used: `SUBSECTION`, `RULING`, `FOUNDATION`, `NTEE_CD`, `NAME`, `STATE`.
- **XML.** The GivingTuesday mirror of IRS TEOS XML, `https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml`, read with a generic user agent (`research-script/1.0`). The pattern is the one in `scripts/mission_national_990_reads.py` and `mission_cf_fee_census.py`.
- **Two passes per return.**
  - A *head* pass streams the XML in 16 KiB chunks and stops at the end of Form 990 Part IV (or the end of Form 990-EZ). It reads the final-return box (`FinalReturnInd`), Part I line 2 (`ContractTerminationInd`), Part IV lines 6, 31 and 32 (`DonorAdvisedFundInd`, `TerminateOperationsInd`, `PartialLiquidationInd`), 990-EZ line 36 (`OrganizationDissolvedEtcInd`), total assets, formation year, website and mission.
  - A *full* pass reads the whole return and extracts Schedule D Part I (`DonorAdvisedFundsHeldCnt`, `…VlEOYAmt`, `…ContriAmt`, `…GrantsAmt`), Schedule N Parts I and II (description, date, fair market value, method, recipient name and EIN, IRC section, supplementary text), and Schedule O passages that mention DAFs together with termination or transfer words.
  - Because the line-6 test failed (§1 item 4), the full pass was run on **every** mirrored return in both frames. The head-pass flags are kept as columns, and their recall is reported.
- **Caching.** One JSON extract per OBJECT_ID, so a re-run makes no requests.

### 2.2 Frame A (P-GAP19-15-01)
- **Universe.** Index years 2022–2026, `RETURN_TYPE` = 990. The filer is a 501(c)(3) in the BMF with `RULING` ≥ 202101.
- **Pre-filter (documented, as the task allows).**
  - *Return type:* only Form 990. Schedule D Part I is filed only with Form 990, so 990-EZ, 990-N and 990-PF are dropped.
  - *BMF foundation code:* kept 15 (170(b)(1)(A)(vi)), 16 (509(a)(2)), 17 and 21–24 (509(a)(3) supporting organisations).
  - *Dropped:* private foundations (codes 02–04, 415 returns), which cannot be sponsoring organisations under IRC 4966(d)(1); churches (10, 1,686 returns); schools (11, 4,656); hospitals (12, 779); medical research (13, 116); and codes 09, 18 and 25 (30).
  - *Result:* 7,682 returns dropped, 86,637 returns kept, covering 36,115 EINs.
- **Holder.** An EIN with Schedule D Part I DAF accounts > 0 in any scanned return.
- **Window test.** The cohort's rule is "first observable entry event in 2021-01..2026-11". An EIN fails the test if the index lists any return of any type for a tax period before 2021-01, or if its Form 990 formation year is before 2021. This is the Uncommon Giving logic from wave 32A, applied mechanically.
- **Comparison.** EINs are matched against `sponsor-entry-exit-panel.csv` (DAFRC FY2019–FY2024, 1,594 EINs) and against `daf-startup-cohort-2021-2026.csv`.
- **Cohort rule.** Every in-window, non-DAFRC holder not already in the cohort file was screened by hand with the pre-registered rule in gap19-startup-cohort.md §2.1: the product definition (i)–(iii); the exclusions (community foundations, single-issue charities, products of pre-2021 incumbents, no giving account); and the status rule (`active` needs dated evidence on or after 2025-11-19).
  - **Status evidence.** The status evidence is the filer's own e-filed return. Its `ReturnTs` (e-file timestamp) counts as dated tier-1 evidence. The homepage was read where robots.txt allowed it.
  - **Account threshold.** Frame A applied a ≥50-account threshold only to DAFRC subtype "Other". Non-DAFRC entities have no DAFRC type, so the analogue used here is:
    - a dedicated DAF sponsor (one whose 990 says it exists to sponsor DAFs) is treated like DAFRC "National", with no threshold;
    - every other charity is screened as single-issue.
  - **Screen tables.** The `SCREEN` and `EXIT_CLASS` tables in the script record each call.

### 2.3 Frame B (P-B40N11-02)
- **Universe.** Index years 2021–2026, `RETURN_TYPE` 990 or 990-EZ. The filer either matches a community-foundation name pattern (`COMMUNITY FOUNDATION/FDN/TRUST/FUND/ENDOWMENT`, `AREA FOUNDATION`, `FOUNDATION FOR (THE) GREATER`, `REGIONAL FOUNDATION`) in the index name, or has BMF NTEE code T31.
  - This gives 16,947 returns (12,214 Form 990, 4,733 990-EZ) from 3,673 EINs.
  - By basis: name only 6,373 returns, T31 only 5,751, both 4,823.
  - 990-EZ is included beyond the queue text ("Form 990 filer") because small CFs, the likely exiters, file it.
- **Trigger.** Any of: Part I line 2; the final-return box; Part IV line 31 or 32; 990-EZ line 36. Schedule N is read for every return, so Schedule N filed without any trigger is also caught.
- **Event classes (per return):**

  | Class | Rule |
  |---|---|
  | `exit_liquidation_schedule_n` | Schedule N Part I lines present |
  | `exit_final_return_no_schedule_n_part_i` | Final-return box set, but no Part I lines |
  | `disposition_over_25pct` | Schedule N Part II lines only |
  | `schedule_n_without_detail_lines` / `flag_only_no_schedule_n` | Remaining flagged returns |

- **Exit counts.**
  - An exit is counted once per filer EIN, in the year of its earliest exit-class return. The year comes from the earliest Schedule N distribution date, or else the tax-period end.
  - Only filers classed `geographic_cf` (a place-based community foundation or community trust; hand-coded) are counted as CF exits. Supporting organisations held at a CF, faith-based foundations, community chests, corporate or employee funds, service-club funds and other "community"-named charities are kept in the CSV but not counted.
  - **Small** = the largest total assets seen in any scanned return of that EIN (end-of-year from every return; beginning-of-year from the flagged returns) is below $10m.

### 2.4 Robots and access log (2026-11-19)

| Host | robots.txt | Use |
|---|---|---|
| gt990datalake-rawdata.s3.amazonaws.com | HTTP 404 (no rules) | XML reads |
| www.givmocharitable.org | 200, `Allow: /` | homepage |
| www.theoverflowfoundation.org, www.spiralgivingnetwork.org | 200; disallows `/config`, `/search`, `/account$` | homepage only |
| www.onebiggift.org | 200, empty `Disallow:` | homepage |
| dafshare.com | 200, no disallow for `*` | homepage |
| www.netafoundation.org | 200; disallows `*?lightbox=` | homepage |
| bridgesphilanthropicfund.org | 200; disallows `/calendar/action*`, `/events/action*`, `/cdn-cgi*` | homepage |

- **Not used:** sec.gov, crt.sh and certspotter.
- **No logins:** DAFshare shows a login page, which was not used.

---

## 3. Results: frame A (new DAF sponsors)

### 3.1 Funnel

| Step | Count |
|---|---|
| 501(c)(3) EINs in the BMF with ruling ≥ 2021-01 | 513,145 |
| Form 990 returns in index 2022–2026 from those EINs, after the foundation-code pre-filter | 86,637 returns / 36,115 EINs |
| Returns read from the mirror | 83,020 |
| Returns not mirrored (HTTP 404; all listed in `index_2026`) | 3,617 (990 EINs have no readable return) |
| EINs answering "Yes" on Part IV line 6 in any return | 265 |
| Returns answering "Yes" on line 6 but reporting 0 DAF accounts | 198 |
| **EINs with Schedule D Part I DAF accounts > 0 (holders)** | **179** (329 returns) |
| Positive returns answering "No" on line 6 | 17 |
| Holders that never answered "Yes" on line 6 (line-6 filter would miss them) | 14 (7.8%) |
| Holders in the DAFRC panel / not in it | 43 / 136 |
| Holders passing the window test | 122 |
| …in DAFRC / not in DAFRC | 24 / 98 |
| …not in DAFRC with latest DAF value > 0 | 64 |
| …not in DAFRC with ≥ 50 accounts | 28, of which 18 report $0 DAF value |

### 3.2 Recovery of the existing cohort
- **Found as holders:** SC01 Daffy, SC02 Groundswell (only through its amended TY2024 return), SC08 Goodstack (Percent Impact Foundation), SC09 Uncommon Charitable Impact, SC10–SC17, SX01 Telescope Fund, and both SX17 EINs.
- **Uncommon fails the window test here.** SC09 is a holder, but the index lists a return for tax period 2020-12. This matches the wave 32A correction.
- **Not found: SC18 I Maaser Inc.** It filed 990-EZ for TY2022, then Form 990 for TY2023 and TY2024. Both Form 990s attach Schedule D but report 0 DAF accounts.
- **Not filers:** SC03–SC07 have no sponsor EIN or a post-panel one.
- **Groundswell and I Maaser look the same in filings.** Both present as DAF products in the market yet did not report Part I DAFs on their original returns, so a Schedule D frame alone undercounts entrants that call their accounts something else.

### 3.3 Additions (rows in `daf-startup-cohort-additions-2026-11-19.csv`)

| ID | Entity (EIN) | Ruling | DAF accounts / value (latest) | Category | Status (date) |
|---|---|---|---|---|---|
| SA01 | Givmo Charitable Fund (99-2418877) | 2024-09 | 31 / $865 (TY2025) | core sponsor, DAF inside a mobile app | active (TY2025 990 e-filed 2026-07-27) |
| SA02 | Spiral Giving Network (87-2497866) | 2022-12 | 1 / $449 (TY2025) | DAF-like account embedded in banking (sole member Spiral Financial, Inc.) | active (TY2025 990 e-filed 2026-08-12) |
| SA03 | Neta Foundation (93-2276661) | 2023-11 | 19 / $7.59m (TY2024) | core sponsor, venture-philanthropy DAF | unknown (last e-file 2025-10-12; site © 2025) |
| SA04 | One Big Gift (99-3997336) | 2024-12 | 6 / $0.93m (TY2025) | core sponsor, endowment-style DAFs for nonprofits | active (TY2025 990 e-filed 2026-08-18) |
| SA05 | DAF Gives Charitable / DAFshare (93-4052953) | 2023-12 | 1 / $106k (TY2024); 740 grants in 2024 | group-giving platform on a sponsor | unknown (e-filed 2025-11-17, two days before the cutoff) |
| SA06 | Monument Charitable (93-2565248) | 2024-06 | 12 / $3.76m (TY2024) | core sponsor, non-cash ("atypical") assets | unknown (e-filed 2025-11-14; no website) |
| SA07 | Overflow Foundation (88-3232461) | 2023-01 | 29 / not reported (TY2024) | DAF-adjacent: stock/crypto gift processing, corporate giving vehicle of Overflow | unknown (e-filed 2025-11-15) |

**Screened out:**

| ID | Entity | Reason |
|---|---|---|
| SAX01 | Bridges Philanthropic Fund | $107.0m; run by a pre-2021 wealth manager |
| SAX02 | Anderson Donor Advised Charitable Fund | 31 accounts; no public product found [I] |
| SAX03 | JustFund | Entry before the window |
| SAX04 | The Alternatives Foundation | Single-issue |
| SAX05 | Mortarstone Trust and Kindred One Foundation | One DAF each |
| SAX06 | Fenwick Community Fund | Employer member fund |
| SAX07 | Richmond Christian Foundation | Local faith foundation |
| SAX08 | Ten in-window community foundations | Community-foundation exclusion |
| SAX09 | Other in-window Part I filers (79 EINs) | Single-issue or operating charities, often with implausible entries |

**Effect on the cohort, as arithmetic only (the cohort file itself is not edited).**
- With the 7 additions the cohort is 25: active 13, acquired 1, pivoted 1, unknown 10, shut 0.
- Operating in any form ranges from 15/25 = 60.0% (Wilson 95% 40.7–76.6%), counting unknowns as failures, to 25/25 (86.7–100%).
- Among the 15 resolved, 15 are not shut (79.6–100%).
- All 7 additions enter by IRS ruling in 2022–2024. 4 of the 7 are strict-window companies (Neta, One Big Gift, DAFshare and Monument all have 2023–2024 formation years); the other 3 have parents whose founding dates were not verified.

### 3.4 Comparison with DAFRC
- **The 136 non-DAFRC holders are mostly not sponsors.** They are dominated by charities with one to a few "DAFs" or with implausible entries.
- **The largest in-window holders outside DAFRC are already known or excluded.** They are Bridges ($107.0m, excluded by rule), Percent Impact Foundation (Goodstack, $10.8m, already SC08), Groundswell ($10.1m, visible only on an amended return, already SC02) and Neta ($7.6m, added as SA03). Every other one reports under $4m.
- **The new in-window sponsors DAFRC misses are tiny.** The seven additions together report $12.39m of DAF assets on their latest positive returns, of which Neta and Monument account for $11.36m.

---

## 4. Results: frame B (community-foundation exits)

### 4.1 Screen

| Step | Count |
|---|---|
| Returns in the universe / EINs | 16,947 / 3,673 |
| Read / not mirrored (all `index_2026`) | 16,629 / 318 |
| Part I line 2 set | 78 |
| Final-return box set | 82 |
| Part IV line 31 / line 32 set | 43 / 42 |
| 990-EZ line 36 set | 49 |
| Returns with any trigger | 135 |
| Returns with Schedule N | 136 (4 of them with no trigger set) |
| CSV rows (return × recipient) | 195: 120 liquidation, 47 disposition, 20 final-return without Part I, 5 Schedule N without detail lines, 3 flag only |
| Filers with an exit-class return, any year | 85 (14 in tax year 2020) |
| …with exit year 2021–2026 | 71: 24 geographic CF, 11 CF-held supporting organisations, 5 community chests, 5 corporate or employee funds, 5 service-club funds, 1 faith-based, 20 other "community"-named charities |

### 4.2 Geographic CF exits per year (exit year = earliest Schedule N date, else tax-period end)

| Year | Exits | Small (< $10m) | In DAFRC panel |
|---|---|---|---|
| 2021 | 6 | 6 | 1 (Shelby) |
| 2022 | 2 | 2 | 2 (Fairfield, Milbank) |
| 2023 | 4 | 4 | 1 (Rusk County) |
| 2024 | 6 | 5 | 1 (Coastal, $11.1m, the only non-small exit) |
| 2025 | 6 | 6 | 0 |
| 2026 (to 2026-11-19; filing lag) | 0 | 0 | 0 |
| **Total** | **24** | **23** | **5** |

**Profile of the 24 exits:**
- **Size:** median largest-observed total assets $248k; 16 were under $1m.
- **Form:** 12 filed 990-EZ.
- **States:** OH and MI have 4 each, WI 3, and the rest are spread across 10 states.
- **Assets moved:** Schedule N fair market value distributed totals $26.9m. The largest transfers are Coastal Community Foundation to the San Diego Foundation ($10.07m, 2024-07-15), Three Rivers Area CF to Sturgis Area CF ($5.44m, 2024-12-31), Rusk County CF to Eau Claire CF ($2.14m) and Angel Fire CF to Taos CF ($1.26m in its first exit return).
- **Recipients:** 9 of 24 went to another CF. The rest went to a city, a school foundation, a local charity, or were not itemised; 7 filed a final return with no Schedule N Part I.
- **DAF balances:**
  - No geographic CF exit names DAF balances on Schedule N.
  - 4 reported DAF accounts on the exit-year Schedule D: Rusk County 6, Fairfield 12, Milbank 4, Coastal 39.
  - Elsewhere in the frame, DAF balances are named only by:
    - Greater White Bear Lake Community Foundation, a Part II disposition to CommunityGiving of "fund balances related to DAF, endowment funds and designated funds" ($4.97m, 2025);
    - The Kingdom Trust (NTEE T31), "donor advised funds transferred to public charity donor advised funds";
    - two CF-held supporting organisations that dissolved into a DAF at their CF (L2 Foundation and Ingebritson Family Foundation).

### 4.3 Comparison with the repo's sponsor-mortality and CF-consolidation work
- **`sponsor-mortality-analysis.md` (tier A).** Its 11 ceased DAFRC sponsors include 5 CFs: Sunbury, Shelby, Fairfield, Rusk County and Milbank.
  - All 5 reappear here. Sunbury's exit is dated 2020-07, so it falls outside 2021–2026.
  - Frame B adds **19 geographic CF exits in 2021–2025 that are not in the DAFRC panel**, almost all below $1–5m.
  - The panel's CF exit rate (1.1%/yr) is therefore a rate for DAFRC-sized CFs. The very small CFs that DAFRC never tracked exit at a steady 2–6 per year in filed returns.
- **`cf-consolidation-2021-2026.csv`.**
  - The DAFRC-list Schedule N screen found 5 filed CF liquidations: C010 Shelby, C013 Milbank, C014 Rusk, C017 Coastal, and C012 Fairfield as a disposition. All are reproduced.
  - The press-sourced C002 (Three Rivers Area CF joins Sturgis Area CF as an affiliate, 2025-01-01) is confirmed by filing: a Schedule N liquidation of $5.44m dated 2024-12-31.
  - C011 Keweenaw, C018 White Bear Lake and C019 Watertown appear here as Part II dispositions, not exits.
- **Reading.** Of the two readings in the queue item, "a handful of small exits" is closer to the data than "a measurable trend", but the handful is about five times larger than DAFRC shows. There are about 4–6 geographic-CF exits a year, overwhelmingly sub-$1m organisations, and they move cash or investments to a neighbouring CF or a local charity without naming DAFs.

---

## 5. Limits

1. **Mirror lag.** 3,617 frame-A returns and 318 frame-B returns, all in `index_2026`, were not on the mirror (HTTP 404) on 2026-11-19. 990 frame-A EINs have no readable return. The 2026 columns (new sponsors ruled 2025–2026; 2026 CF exits) are therefore incomplete (P-G1915B-01).
2. **Frame A depends on the BMF ruling date.**
   - A reinstated organisation receives a new ruling date; this is why 513,145 EINs pass the ruling filter and why the window test is needed.
   - A new sponsor under an old EIN or a group exemption is missed.
   - Organisations already gone from the November 2026 BMF are not in frame A.
3. **Form 990 only.** New sponsors filing 990-EZ (I Maaser for TY2022) or 990-N have no Schedule D and are invisible (P-G1915B-02).
4. **Schedule D Part I is self-reported and noisy.**
   - 198 returns answer "Yes" on line 6 with 0 accounts; 17 positive returns answer "No".
   - Many small charities enter dollar values as account counts.
   - Entities that do not call their accounts DAFs report nothing: Groundswell's original returns and I Maaser.
5. **Hand classification.**
   - The product, incumbent and community-foundation calls in `SCREEN` and the entity classes in `EXIT_CLASS` are analyst judgements from the filer's own 990 text and homepage. [I] marks inference.
   - The "incumbent" boundary (Bridges vs GivingTrax) is the ambiguity wave 32A recorded.
   - The status of four additions is unresolved because their latest returns were e-filed 2–38 days before the 12-month cutoff (P-G1915B-03).
6. **The CF name and NTEE screen misses some CFs.** A terminated CF usually leaves the BMF, so only its index name can place it in frame B. Exited CFs named without "community" or "area foundation" are missed (P-G1915B-05). The name pattern also pulls in many non-CFs, which are kept in the CSV but classed out of the count.
7. **Exit year and size.**
   - The exit year is the earliest Schedule N distribution date, or else the tax-period end.
   - Size is the largest total assets seen in 2021+ index returns plus the beginning-of-year assets of the flagged return. CFs that wound down before 2021 show small values.
   - Schedule N FMV covers all assets, not only DAFs.
8. **`transferee_name_overlap` is a crude heuristic** (≥60% shared distinctive name words). It flags likely self-successors (Employees Community Fund, Haven CF) but also neighbours with a shared place name (Holmes County CF and Holmes County Education Foundation).
9. **No state-registry, Candid or ProPublica checks.** The cohort file's `last_990_period_propublica` column is filled from the IRS index for the additions; ProPublica was not used.

---

## 6. Data dictionaries

### 6.1 `daf-startup-cohort-additions-2026-11-19.csv`
The columns and meanings are identical to `daf-startup-cohort-2021-2026.csv` (see [gap19-startup-cohort.md §8](gap19-startup-cohort.md)), with these conventions:

| Column | Convention for the additions |
|---|---|
| `cohort_id` | SA01–SA07 for members; SAX01–SAX09 for screened-out rows |
| `frames` | `D` = the IRS e-file frame of this note (frames A–C are the cohort's) |
| `ein` | Multiple EINs separated by `;`. SAX09 gives a count and points to the frame CSV |
| `status_evidence` | Quotes the filer's own 990 and its e-file timestamp (`ReturnTs`) |
| `last_990_period_propublica` | Holds the latest tax period in the **IRS e-file index**; ProPublica was not used |
| `app_store_id`, `app_listing_last_dated_item` | Blank: not checked |
| `notes` | The frame facts (largest account count and its period, latest DAF value, BMF ruling) |

### 6.2 `cf-exits-schedule-n-2021-2026.csv` (one row per flagged return × Schedule N part × recipient)

| Column | Meaning |
|---|---|
| `row_id` | CFX0001… |
| `filer_ein`, `filer_name`, `index_name`, `state` | Filer EIN; name from the XML header; name in the IRS index; state |
| `cf_basis` | Why the filer is in frame B: `name` (pattern on the index name), `ntee_T31` (BMF NTEE), or both |
| `entity_class` | Hand-coded: `geographic_cf`, `cf_supporting_org`, `faith_based_cf`, `community_chest_or_fund`, `corporate_or_employee_fund`, `service_club_fund`, `other_named_cf_like` |
| `ntee`, `in_bmf_2026_11`, `in_dafrc_panel` | BMF NTEE code; whether the EIN is in the Nov-2026 BMF; whether it is in `sponsor-entry-exit-panel.csv` |
| `form`, `object_id`, `tax_period_end` | Return type, IRS OBJECT_ID, tax-period end |
| `final_return_ind`, `part1_line2_ind`, `terminate_ops_ind`, `partial_liq_ind`, `ez_dissolved_ind` | Raw values of the five triggers (`1`/`true`/`X` = set; blank = not present) |
| `event_class` | See §2.3 |
| `event_year` | Year of the earliest Schedule N date in the row, else the tax-period end |
| `has_schedule_n`, `schedn_part` | Whether Schedule N is attached; `I_liquidation` or `II_disposition` |
| `transferee_name`, `transferee_ein` | Recipient, with the name from the BMF when the return gives only an EIN |
| `transferee_is_cf` | Recipient matches the CF pattern or has BMF NTEE T31 |
| `transferee_name_overlap` | Crude successor heuristic (§5 item 8) |
| `transfer_date` | Earliest distribution date in the group |
| `fmv_usd`, `n_lines` | Fair market value summed over the group's lines; number of lines |
| `asset_desc` | Schedule N descriptions (distinct, `;`-joined) |
| `daf_named`, `daf_named_evidence` | Whether a Schedule N description or text, or a Schedule O termination passage, mentions donor-advised funds; the matching text |
| `sched_d_daf_count`, `sched_d_daf_value_eoy` | Schedule D Part I on the same return |
| `max_total_assets_scanned`, `small_cf_lt_10m` | Size measure (§2.3) and the < $10m flag |
| `return_ts` | E-file timestamp of the flagged return |
| `xml_url` | Mirror URL of the return |

### 6.3 `new-daf-holders-frame-2022-2026.csv` (one row per frame-A holder)

| Column | Meaning |
|---|---|
| `ein`, `name`, `state`, `bmf_ruling`, `bmf_foundation`, `ntee` | Identity and BMF fields |
| `returns_scanned`, `returns_ok` | Index returns in the frame, and those read |
| `returns_daf_ind_yes` | Returns answering "Yes" on Part IV line 6 |
| `returns_daf_count_gt0`, `returns_daf_count_gt0_line6_no` | Returns with Part I accounts > 0, and those of them answering "No" on line 6 |
| `max_daf_count`, `max_daf_count_tax_period` | Largest Part I account count and its period |
| `latest_daf_value_eoy`, `latest_daf_tax_period` | DAF value on the latest positive return |
| `first_index_tax_period`, `formation_yr`, `pre_window_evidence`, `in_window` | Window test (§2.2) |
| `in_dafrc_panel`, `in_cohort_file`, `listed_in_index_2026` | Matches to DAFRC, to the cohort file and to the 2026 index |
| `latest_tax_period`, `website`, `mission` | From the latest return read |
| `evidence_url` | Mirror URL of the return with the largest account count |

---

## 7. Source register

**IRS primary data**
- IRS TEOS e-file index, 2019–2026: https://apps.irs.gov/pub/epostcard/990/xml/2025/index_2025.csv (and the same path for each year)
- IRS EO Business Master File: https://www.irs.gov/pub/irs-soi/eo1.csv, https://www.irs.gov/pub/irs-soi/eo2.csv, https://www.irs.gov/pub/irs-soi/eo3.csv, https://www.irs.gov/pub/irs-soi/eo4.csv
- E-filed return XML (IRS TEOS, GivingTuesday mirror), pattern `https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml`. Returns cited in the text:
  - Groundswell amended TY2024 (12,808 accounts, line 6 = 0): https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202640289349301029_public.xml ; original TY2024: https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513219349318726_public.xml
  - Givmo TY2025: https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202602089349300530_public.xml
  - Spiral Giving Network TY2025: https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202612249349301741_public.xml
  - Neta Foundation TY2024: https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202542859349300019_public.xml
  - One Big Gift TY2025: https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202632309349302723_public.xml
  - DAF Gives Charitable TY2024: https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543219349326029_public.xml
  - Monument Charitable TY2024: https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513189349304316_public.xml
  - Overflow Foundation TY2024: https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533199349300323_public.xml
  - Bridges Philanthropic Fund TY2025: https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202612549349300906_public.xml
  - Coastal Community Foundation final return (Schedule N to San Diego Foundation): https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202530559349300993_public.xml
  - Three Rivers Area Community Foundation (Schedule N to Sturgis Area CF): https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202542029349301519_public.xml
  - Flathead Community Foundation 2020 liquidation: https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202141059349302019_public.xml
  - Every other row's return URL is in the `xml_url` / `evidence_url` / `status_evidence_url` columns.

**Organisation pages (homepages, fetched 2026-11-19 after a robots check)**
- https://www.givmocharitable.org/
- https://www.spiralgivingnetwork.org/
- https://www.netafoundation.org/
- https://www.onebiggift.org/
- https://dafshare.com/
- https://www.theoverflowfoundation.org/
- https://bridgesphilanthropicfund.org/

**Repository sources**
- `data/mission-2026-11-14/sponsor-entry-exit-panel.csv` (from the [DAFRC 2025 dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx))
- `data/mission-2026-11-14/daf-startup-cohort-2021-2026.csv`
- `data/mission-2026-11-14/cf-consolidation-2021-2026.csv`
- `data/mission-2026-11-14/sponsor-exit-verification.csv`
- `research/mission-2026-11-14/sponsor-mortality-analysis.md`
- `research/mission-2026-11-14/gap19-startup-cohort.md`
- `research/mission-2026-11-14/validation-wave32a-report.md`

**Robots files read:**
- https://gt990datalake-rawdata.s3.amazonaws.com/robots.txt (404)
- https://www.givmocharitable.org/robots.txt
- https://www.theoverflowfoundation.org/robots.txt
- https://www.onebiggift.org/robots.txt
- https://dafshare.com/robots.txt
- https://www.spiralgivingnetwork.org/robots.txt
- https://www.netafoundation.org/robots.txt
- https://bridgesphilanthropicfund.org/robots.txt
