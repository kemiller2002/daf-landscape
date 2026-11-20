# b50-03: DAF programmes run by single-issue charities (universities, health systems, national charities)

- **Task:** b50-03, a new direction. Researched 2026-11-20.
- **Scope:** DAF sponsors in the DAFRC 2025 panel that are neither national sponsors nor community foundations. This is tier T4 in `scripts/mission_pf_to_daf_flows.py`. The focus is the institutions (universities, schools, their foundations, hospitals and health systems) and national issue charities. Faith-based sponsors are reported only as context; see `faith-sponsors-church-dollars-2026-11-20.csv`.
- **Read first:**
  - [direction-gift-office-daf-handling.md](direction-gift-office-daf-handling.md). It covers the recipient side of university DAF gifts. Its table lists in-house DAFs for 12 of 33 recipients, and Columbia's "≥50% to Columbia" rule.
  - [direction-league-table-concentration.md](direction-league-table-concentration.md). Its §1.1 sets out the corrected-value method reused here.
- **Outputs:**
  - [`data/mission-2026-11-14/institutional-daf-programs-2026-11-20.csv`](../../data/mission-2026-11-14/institutional-daf-programs-2026-11-20.csv): 430 rows in six row types (§7).
  - [`scripts/mission_institutional_dafs.py`](../../scripts/mission_institutional_dafs.py): stdlib, functional style.
  - [`data/mission-2026-11-14/queue-proposals-b50-03.csv`](../../data/mission-2026-11-14/queue-proposals-b50-03.csv): 6 proposals.
- **Rules followed:**
  - robots.txt was read for every host and checked for ClaudeBot, anthropic-ai, Claude-User, Claude-Web, Claude-SearchBot, `research-script/1.0` and `*`. An unreadable or 403 robots.txt was treated as a disallow.
  - Generic user agent only: `research-script/1.0`.
  - No logins, forms or outreach. No sec.gov, crt.sh or certspotter. No off-limits hosts.
  - Evidence is from 2021 or later. Undated live pages are flagged.
  - This is research, not legal or tax advice.
- **Labels:**
  - **[C]** computed by the script.
  - **[F]** filed value or first-party page read in full.
  - **[I]** inference.

## 0. Answers in brief

| Question | Answer | Confidence |
|---|---|---|
| **How many, how big (Q1)** | **Institutional sponsors (universities, schools, their foundations, hospitals, health systems): 165–174 with positive DAF assets each year FY2021–24** [C].<br>- **Assets:** $3.22bn → $3.41bn → $3.58bn → **$3.59bn** (+11% over FY2021–24, against +38% for the market).<br>- **Contributions:** $0.28bn, $0.85bn, $0.56bn, **$0.25bn**. These are erratic and driven by the UCLA Foundation.<br>- **Grants:** $0.29bn, $0.41bn, $0.43bn, **$0.52bn**.<br>- **Accounts:** about 4,000 throughout (4,148 → 3,959), averaging roughly $0.9m each.<br>- **Concentration:** the top 10 hold 81–83% of segment assets.<br>**All T4 (institutions plus faith, issue and intermediary sponsors outside the four T1 core sponsors):** 547–580 sponsors, $13.9bn → **$15.1bn**. | High [C] on the arithmetic. Medium on segment size, because two rows look mis-measured (§2.3). |
| **Market share and trend (Q4)** | **Institutional share is small and falling** [C]:<br>- assets 1.37% → 1.49% → 1.39% → **1.10%**;<br>- grants 0.59% → 0.73% → 0.78% → 0.78%;<br>- contributions 0.35% → 1.11% → 0.85% → **0.27%**.<br>**All T4:** assets 5.94% → 6.15% → 5.68% → **4.66%**; contributions 4.3% → 3.7%; grants 5.6% → 6.0%.<br>The fall is relative: segment assets grew slowly while the T1 national sponsors grew 55%. | High [C] |
| **Where the grants go (Q2)** | **Schedule I cannot pin the host share for most universities, because a university that is its own sponsor pays DAF grants to itself internally.** Those payments never appear on Schedule I. For the 18 FY2024 institutional returns with positive DAF grants ($308m), the dollar-weighted bound on the share kept by the host is **6%–69%** (FY2023: 39%–91%) [C]. Where filings are explicit, the range is wide:<br>- **Mostly external:** Harvard (≥58% of FY2024 DAF grants are labelled DAF lines to non-affiliates), Yale (≥68%), EY Foundation (≥78%), Rotary Foundation (≥90%). SUNY Binghamton Foundation's FY2024 DAF grants went entirely to **Greater Horizons**, a community-foundation DAF sponsor ($84.18m).<br>- **Mostly host:** Cornell University Foundation, 42% (FY2023) and **68%** (FY2024) to Cornell. University of Arizona Foundation ≥78%. Rochester and Penn Presbyterian report no grants to any outside organisation, which is consistent with 100% host. | Medium on the bounds; low on any single segment-wide figure |
| **Published host rules (Q3)** | **Yes. 12 of the 18 programme pages read state a host minimum, usually 50%** [F]:<br>- **50%:** Stanford (falling to 40% for gifts of $10m+ and 30% for $20m+), Columbia, Yale, UCLA, Penn Medicine, Harvard ("at least half of your distributions") and MSU (a 50% "MSU Only" account).<br>- **Other levels:** UND 51% of annual distributions; Mayo Clinic 60%; Brown 25%.<br>- **Tiered by size:** Cornell (50% under $500k, 25% over, none over $1m) and Rochester (100% / 50% / 25% / 0%).<br>The rule is usually set on contributions or over the fund's life, not per year. That is why single-year Schedule I flows (Harvard, Yale) can exceed 50% external without breaching it. | High [F] on the quoted rules; four pages were blocked (§4.1) |

## 1. Method

### 1.1 Universe and segments
- **Panel:** DAFRC 2025 sponsor panel (`dafrc-sponsor-schedule-d-fy2019-2024.csv`, from the [DAFRC 2025 dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)). Values are overridden by `applied = 1` R1–R4 rows of `dafrc-corrections-itemized.csv`, using `corrected()` from `scripts/mission_league_table.py`.
- **Tiers:** `tier_of()` from `scripts/mission_pf_to_daf_flows.py`, unchanged.
  - **T1:** the FY2024 top-50 national and processor sponsors, plus NCF, JCF, DonorsTrust and Thrivent.
  - **T2:** other national sponsors.
  - **T3:** community foundations.
  - **T4:** all other "Single Issue Charity" rows.
- **T4 split (`t4_class`):** DAFRC subtype plus NTEE major from the IRS EO BMF, taken from `daf-long-tail-sponsors-fy2021-2024.csv`.
  - `institution_edu_health`: subtype "Universities and Healthcare" (131 EINs), or subtype "Other" with NTEE B, E, F, G or H (53 EINs).
  - `religious`
  - `intermediary_t`: subtype "Other" with NTEE T. Examples: Tides, Pew, United Way Miami.
  - `mission_other`: subtype "Other" with any other NTEE. Examples: Rotary, NIF, National Trust.
  - `unclassified`
- **Check [C]:** for every FY2021–24 × metric cell, T1+T2+T3+T4 equals `dafrc-corrected-market-totals.csv` to within $1. The script records this in `check_totals.json` and reports no failures.
- **FY** is the calendar year in which the tax period ends.

### 1.2 Schedule I sample (Q2)
- **Sample:** the top 20 `institution_edu_health` and top 8 `mission_other` sponsors by FY2024 corrected assets. That gives 56 FY2023–24 Form 990 XMLs from the GivingTuesday mirror of IRS TEOS. Object ids come from `form990-returns-schedule-d-harvest-full.csv`.
- **Parsed fields:** Schedule D Part I (DAF count, contributions, grants, year-end value), every Schedule I Part II line (recipient EIN, amount, purpose), Schedule R related-organisation EINs, and Part IX lines 1 and 3.
- **Line classes, applied in order:**
  1. **host:** the recipient EIN is the filer, a Schedule R related organisation, or a listed `HOST_EXTRA` EIN (four foundation → university pairs).
  2. **DAF-labelled:** the purpose mentions DAF or donor advised.
  3. **research:** the purpose mentions research, sub-award or subcontract.
  4. **other.**
- **Bounds on the host share of Schedule D DAF grants (D):**
  - `ext_min = min(D, DAF-labelled non-host)`
  - `ext_max = min(D, DAF-labelled + other non-host + unitemised (Part IX L1 − Schedule I) + foreign (Part IX L3))`
  - `host_min = 1 − ext_max/D`
  - `host_max = 1 − ext_min/D`. For a separate foundation, `host_max` is also capped at host lines ÷ D.
- **Point estimate:** given only when D is at least 90% of Part IX lines 1+3, so that the filer's grants are essentially all DAF grants. The point is then `host_min`. This is an assumption, flagged in the CSV.
- **Aggregate:** a D-weighted mean of the bounds over returns with D > 0.

### 1.3 Policy pages (Q3)
- **Pages:** 22 URLs for 19 programmes. They were found by web search for university, hospital and charity DAF programme terms, starting from the sponsors in the sample and the gift-office note.
- **Fetching:** robots.txt was read per host. Pages were fetched with `research-script/1.0`. PDFs were read with `pdftotext`.
- **Extraction:** sentences matching a share or minimum pattern were extracted automatically (`extracted_sentences`). The rule read from them is recorded in the script's `READINGS` and quoted below.
- **Column reassembly:** several PDFs are two-column, and their sentences were reassembled. This is flagged per row.

## 2. Results: size and trend (Q1, Q4)

### 2.1 Segment table [C]
$bn; share is of the corrected market total. "n" = sponsors with positive DAF assets.

| FY | Segment | n | Assets | Share | Contributions | Share | Grants | Share | Grants ÷ prior-year assets |
|---|---|---|---|---|---|---|---|---|---|
| 2021 | Institutions (edu/health) | 165 | 3.223 | 1.37% | 0.278 | 0.35% | 0.287 | 0.59% | 12.4% |
| 2022 | Institutions | 168 | 3.413 | 1.49% | 0.849 | 1.11% | 0.409 | 0.73% | 12.7% |
| 2023 | Institutions | 174 | 3.579 | 1.39% | 0.561 | 0.85% | 0.432 | 0.78% | 12.7% |
| 2024 | Institutions | 171 | 3.586 | 1.10% | 0.253 | 0.27% | 0.521 | 0.78% | 14.6% |
| 2021 | Mission charities (`mission_other`) | 88 | 0.378 | 0.16% | 0.218 | 0.28% | 0.197 | 0.41% | 67.6% |
| 2024 | Mission charities | 108 | 0.471 | 0.14% | 0.241 | 0.25% | 0.267 | 0.40% | 57.0% |
| 2021 | Religious (T4 only) | 178 | 8.508 | 3.63% | 1.791 | 2.30% | 1.369 | 2.85% | 20.0% |
| 2024 | Religious (T4 only) | 178 | 9.674 | 2.99% | 2.249 | 2.42% | 2.441 | 3.67% | 27.1% |
| 2021 | Intermediaries (NTEE T) | 78 | 1.693 | 0.72% | 1.005 | 1.29% | 0.823 | 1.71% | 57.5% |
| 2024 | Intermediaries (NTEE T) | 84 | 1.238 | 0.38% | 0.634 | 0.68% | 0.710 | 1.06% | 49.9% |
| 2021 | **All T4** | 547 | 13.921 | 5.94% | 3.338 | 4.30% | 2.701 | 5.62% | 24.6% |
| 2022 | All T4 | 555 | 14.053 | 6.15% | 4.265 | 5.57% | 3.045 | 5.47% | 21.9% |
| 2023 | All T4 | 579 | 14.586 | 5.68% | 3.464 | 5.30% | 3.570 | 6.51% | 25.4% |
| 2024 | **All T4** | 580 | 15.087 | 4.66% | 3.390 | 3.65% | 3.968 | 5.97% | 27.2% |
| 2024 | Market (corrected) | 1,479 | 323.270 | — | 92.774 | — | 66.442 | — | 25.9% |

The CSV has every FY × segment, including T1–T3, `unclassified`, accounts and median sponsor size.

### 2.2 Who they are [C]
FY2024 institutional sponsors by corrected DAF assets:
- Stanford ($680m)
- UCLA Foundation ($608m)
- Université de Montréal ($427m, imputed; see §2.3)
- Notre Dame ($262m)
- Yale ($247m)
- Harvard ($201m)
- Cornell University Foundation ($186m)
- SUNY Binghamton Foundation ($158m)
- MIT ($93m)
- USC ($60m)

The top 10 hold 81.5% of segment assets. The median institutional sponsor held $1.35m in FY2024. Average account size is about $0.9m (3,959 accounts, $3.59bn), against about $98k for the whole market. These are few, large funds.

### 2.3 Measurement problems that move the segment [C/F]
- **UCLA Foundation (17% of FY2024 segment assets).**
  - Filed Schedule D DAF grants are **negative**: −$109.7m for FY2023 and −$120.3m for FY2024 (XML 202411309349304501, 202521349349311822).
  - DAFRC carries FY2023 as +$109.7m. The corrections file keeps an imputed +$169.9m for FY2024 grants.
  - Its contributions ($79m, $286m, $357m, $90m over FY2021–24) cause most of the segment's contribution swings.
  - It has 10–11 accounts.
- **Université de Montréal (12% of FY2024 segment assets).**
  - 657–714 "DAFs" holding $390–429m, with **$0 contributions and $0 grants** for FY2021–23.
  - The filed FY2024 return reports $0, but the corrections file keeps the imputed $427.1m (`applied = 0`).
  - Without it, FY2024 segment assets would be $3.16bn [I]. See P-B5003-02.
- **Excluding both:** segment assets are flat, at $2.66bn → $2.66bn → $2.54bn → $2.55bn. Grants rise from $0.23bn to $0.35bn, and contributions are $0.16–0.56bn.
- **Classification:** NTEE-based classing puts a few non-institutions in the segment. The Pennsylvania Automotive Association (NTEE B99, $55m) and the EY Foundation (B120, $21m) are examples. They are kept, because the rule is mechanical.

### 2.4 Off-panel institutions [C]
- The repo's non-DAFRC Schedule D filers (`non-dafrc-daf-filers-990.csv`) include 82, 73, 58 and 51 filers with education or health names reporting DAF values in FY2021–24. They hold $0.149bn, $0.112bn, $0.032bn and $0.057bn. That is under 0.07% of the market in each year.
- Several programmes with published terms have **no DAFRC row**: Penn, MSU, the UND Foundation, and Johns Hopkins (which has an "own DAF" per the gift-office note). They may report DAF balances outside the Schedule D DAF column. The panel count is therefore a floor (P-B5003-04).

## 3. Results: where the DAF grants go (Q2)

### 3.1 Sample table [C]
Generated from the CSV `schedule_i_sample` rows. "self" means the sponsor is the institution itself; "foundation" means a separate foundation for the host. n/a means D was zero, blank or negative.

| Sponsor (FY) | Structure | Sched D DAF grants $m | Sched I to host $m | DAF-labelled non-host $m | Other non-host $m | Research $m | Unitemised + foreign $m | Host share min–max | Point (DAF-dominant) |
|---|---|---|---|---|---|---|---|---|---|
| Stanford (2023) | self | 64.1 | 0.2 | 0.0 | 44.7 | 0.2 | 11.4 | 13%–100% | 13% |
| Stanford (2024) | self | 84.6 | 4.5 | 0.0 | 70.1 | 0.0 | 14.7 | 0%–100% | 0% |
| UCLA Foundation (2023) | foundation | −109.7 | 366.9 | 0.0 | 50.3 | 0.0 | 0.0 | n/a | — |
| UCLA Foundation (2024) | foundation | −120.3 | 372.7 | 0.0 | 70.3 | 0.0 | 0.0 | n/a | — |
| Université de Montréal (2023, 2024) | self | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | n/a | — |
| Notre Dame (2023) | self | 18.2 | 0.0 | 0.0 | 57.1 | 0.0 | 17.4 | 0%–100% | — |
| Notre Dame (2024) | self | 16.9 | 0.0 | 0.0 | 42.0 | 0.0 | 18.5 | 0%–100% | — |
| Yale (2023) | self | 10.5 | 0.0 | 1.0 | 9.7 | 86.4 | 30.7 | 0%–91% | — |
| Yale (2024) | self | 4.1 | 0.0 | 2.8 | 11.3 | 123.1 | 33.5 | 0%–31% | — |
| Harvard (2023) | self | 12.9 | 0.0 | 3.3 | 1.0 | 141.0 | 29.1 | 0%–75% | — |
| Harvard (2024) | self | 23.2 | 7.7 | 13.4 | 8.7 | 152.0 | 38.9 | 0%–42% | — |
| Cornell Univ. Foundation (2023) | foundation | 24.3 | 10.3 | 0.0 | 13.7 | 0.0 | 0.3 | 42%–42% | 42% |
| Cornell Univ. Foundation (2024) | foundation | 13.6 | 9.2 | 0.0 | 4.0 | 0.0 | 0.3 | 68%–68% | 68% |
| SUNY Binghamton Fdn (2023) | foundation | 61.2 | 70.5 | 0.0 | 0.0 | 0.0 | 0.0 | 100%–100% | — |
| SUNY Binghamton Fdn (2024) | foundation | 84.2 | 15.4 | 0.0 | 84.2 | 0.0 | 0.0 | 0%–18% | — |
| MIT (2023) | self | 2.8 | 5.2 | 0.2 | 6.9 | 0.0 | 3.9 | 0%–92% | — |
| MIT (2024) | self | 8.6 | 5.6 | 1.1 | 6.0 | 0.0 | 6.2 | 0%–87% | — |
| USC (2023) | self | 12.9 | 1.7 | 0.0 | 1.2 | 0.0 | 10.0 | 13%–100% | 13% |
| USC (2024) | self | 17.8 | 1.3 | 0.0 | 1.0 | 170.8 | 16.6 | 1%–100% | — |
| Dartmouth (2023) | self | 22.2 | 0.0 | 1.1 | 1.0 | 0.0 | 4.6 | 70%–95% | 70% |
| Dartmouth (2024) | self | 10.3 | 0.0 | 1.0 | 1.0 | 0.0 | 5.9 | 24%–91% | 24% |
| Pennsylvania Automotive Assn Fdn (2023) | self | 8.9 | 0.0 | 0.0 | 9.0 | 0.0 | 0.8 | 0%–100% | 0% |
| Pennsylvania Automotive Assn Fdn (2024) | self | 11.5 | 0.0 | 0.0 | 11.7 | 0.0 | 0.7 | 0%–100% | 0% |
| Northwestern (2023) | self | 0.1 | 0.1 | 0.0 | 1.7 | 110.9 | 10.9 | 0%–100% | — |
| Northwestern (2024) | self | 7.8 | 0.0 | 0.0 | 4.9 | 117.5 | 13.3 | 0%–100% | — |
| Penn Presbyterian Medical Center (2023) | self | 0.7 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 100%–100% | — |
| Penn Presbyterian Medical Center (2024) | self | 1.9 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 100%–100% | — |
| Univ. of Arizona Foundation (2023) | foundation | 1.8 | 97.9 | 0.0 | 0.2 | 0.0 | 0.0 | 87%–100% | — |
| Univ. of Arizona Foundation (2024) | foundation | 2.0 | 117.2 | 0.0 | 0.4 | 0.0 | 0.0 | 78%–100% | — |
| Vanderbilt (2024) | self | 1.0 | 0.0 | 0.0 | 4.6 | 67.3 | 3.1 | 0%–100% | — |
| Columbia (2023) | self | 10.0 | 17.4 | 0.0 | 6.2 | 139.3 | 33.0 | 0%–100% | — |
| Columbia (2024) | self | 13.9 | 16.0 | 0.0 | 10.1 | 156.0 | 24.1 | 0%–100% | — |
| EY Foundation (2023) | self | 6.0 | 0.0 | 4.9 | 13.1 | 0.0 | 3.4 | 0%–19% | — |
| EY Foundation (2024) | self | 4.6 | 0.0 | 3.6 | 13.2 | 0.0 | 4.3 | 0%–22% | — |
| Rochester (2023) | self | 3.5 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 100%–100% | — |
| Rochester (2024) | self | 2.1 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 100%–100% | — |
| Brown (2023) | self | 0.1 | 0.0 | 0.0 | 0.0 | 47.5 | 2.8 | 0%–100% | — |
| Brown (2024) | self | 0.2 | 0.0 | 0.0 | 0.0 | 45.5 | 3.2 | 0%–100% | — |
| International Generosity Fdn (2023) | self | 103.2 | 0.0 | 0.0 | 34.5 | 0.0 | 68.7 | 0%–100% | 0% |
| International Generosity Fdn (2024) | self | 119.0 | 0.0 | 0.0 | 56.5 | 0.0 | 62.5 | 0%–100% | 0% |
| Rotary Foundation (2023) | self | 7.6 | 0.0 | 6.9 | 11.2 | 0.0 | 271.4 | 0%–10% | — |
| Rotary Foundation (2024) | self | 9.9 | 0.0 | 8.9 | 12.2 | 0.0 | 263.2 | 0%–10% | — |
| Horizons Foundation (2023) | self | 7.8 | 0.0 | 0.0 | 6.8 | 0.1 | 0.8 | 3%–100% | 3% |
| Horizons Foundation (2024) | self | 8.3 | 0.0 | 0.0 | 6.2 | 0.0 | 0.8 | 17%–100% | 17% |
| Makeway Foundation (2023, 2024) | self | −3.2 / −8.7 | 0.0 | 0.0 | 0.0 | 0.0 | 14.6 / 21.4 | n/a | — |
| Asian Pacific Community Fund (2023) | self | 1.8 | 0.3 | 0.0 | 1.6 | 0.0 | 0.1 | 6%–100% | 6% |
| Asian Pacific Community Fund (2024) | self | 3.3 | 0.2 | 0.0 | 3.1 | 0.0 | 0.5 | 0%–100% | — |
| New Israel Fund (2023) | self | 4.8 | 0.0 | 0.0 | 2.7 | 0.0 | 22.4 | 0%–100% | — |
| New Israel Fund (2024) | self | 4.4 | 0.0 | 0.0 | 4.6 | 0.0 | 31.2 | 0%–100% | — |
| Indian Land Tenure Fdn (2023) | self | 1.1 | 0.0 | 0.0 | 1.3 | 0.0 | 0.2 | 0%–100% | — |
| Indian Land Tenure Fdn (2024) | self | 1.4 | 0.0 | 0.0 | 1.5 | 0.0 | 0.1 | 0%–100% | 0% |
| Music Center Fdn (2023) | self | 0.5 | 0.0 | 0.0 | 8.2 | 0.0 | 0.0 | 0%–100% | — |
| Music Center Fdn (2024) | self | 0.6 | 0.0 | 0.0 | 9.0 | 0.0 | 0.0 | 0%–100% | — |

Vanderbilt FY2023 has a blank Schedule D DAF grants field. The CSV keeps the row.

**Dollar-weighted bounds** (`schedule_i_summary` rows):

| FY | Group | Returns | DAF grants | Host share |
|---|---|---|---|---|
| FY2023 | Institutions | 17 | $260.2m | 39%–91% |
| FY2023 | Mission charities | 7 | $126.9m | 0.3%–95% |
| FY2024 | Institutions | 18 | $308.2m | **6%–69%** |
| FY2024 | Mission charities | 7 | $146.8m | 1%–94% |

### 3.2 Reading the sample [F/I]
1. **Labelled filers are the most informative, and they show large external flows.**
   - **Harvard's Schedule I note [F]:** "THE UNIVERSITY HAS INCLUDED DONATIONS FROM DONOR ADVISED FUNDS (DAF) THAT EXCEEDED THE MINIMUM REPORTING THRESHOLD. IN TOTAL, THE UNIVERSITY REPORTED 85 IRC 501(C)(3) CHARITABLE ORGANIZATIONS THAT RECEIVED DONATIONS FROM HARVARD UNIVERSITY THROUGH THESE DAF" (FY2024; 70 organisations in FY2023). The lines labelled "DAF DISTRIBUTION" to non-affiliates total $13.4m against $23.2m of DAF grants.
   - **Harvard affiliate:** a further $7.7m "DAF DISTR. & CHAR. CONTRIB." line went to the American Repertory Theatre, a Schedule R affiliate, and is counted as host.
   - **MIT** files the same note (18 organisations in FY2024).
   - **Yale:** $2.8m of $4.1m.
   - **Single-year flows can exceed 50% external** because the published rules bind contributions or the fund's lifetime (§4) [I].
2. **DAF-only foundations give clean figures.**
   - **Cornell University Foundation** describes itself as "A DONOR ADVISED FUND PROVIDING A SERVICE FOR CORNELL ALUMNI AND FRIENDS" [F]. Its Part IX line 1 equals its DAF grants exactly in FY2024 ($13,553,754). Cornell University received **42% (FY2023) and 68% (FY2024)** [C].
3. **One large flow was a DAF-to-DAF transfer, not donor-advised grantmaking at the host.**
   - SUNY Binghamton Foundation's FY2024 DAF grants ($84,184,036) equal a single "UNRESTRICTED SUPPORT" line to **Greater Horizons** (EIN 200849590), the DAF arm of the Greater Kansas City Community Foundation.
   - Its DAF assets fell from $236.1m to $158.2m [F]. See P-B5003-06.
4. **Some filers report no grants to outside organisations, which is consistent with keeping everything at the host.**
   - Rochester and Penn Presbyterian report Part IX line 1 = $0 and no Schedule I organisation lines, while reporting DAF grants of $2.1–3.5m and $0.7–1.9m [F].
   - Rochester's Schedule D note says the advisor "MAKES GRANT RECOMMENDATIONS TO THE UNIVERSITY" [F].
   - A reporting gap cannot be ruled out [I].
5. **Mission charities mostly grant outside.**
   - Rotary's DAF lines (purpose suffix "-DAF") cover ≥90% of its DAF grants. Its Part III text: DAFs "SUPPORT EITHER THE ROTARY FOUNDATION PROGRAMS OR OTHER IRS-APPROVED CHARITIES" [F].
   - The EY Foundation labels "DONOR ADVISED FUND" lines covering ≥78%.
   - The International Generosity Foundation and the Pennsylvania Automotive Association pay out roughly their DAF grants as external grants. They behave like community-style sponsors, not restricted-purpose ones [I].

## 4. Results: published host rules (Q3)

### 4.1 Page register and robots log
| # | Programme | URL | robots / HTTP | Host minimum read |
|---|---|---|---|---|
| 1 | Stanford | https://assets.stanford.edu/a/f/78141/x/889a0f5be4/wp_daf_02252025.pdf | robots 404; 200 | 50% (<$10m), 40% ($10m+), 30% ($20m+) |
| 2 | Columbia | https://giftplanning.columbia.edu/what-you-can-give/donor-advised-fund | allowed; 200 | 50% |
| 3 | Yale (web) | https://plannedgiving.yale.edu/what-you-can-give/donor-advised-fund | allowed; 200 | 50% |
| 4 | Yale (2025 PDF) | https://plannedgiving.yale.edu/sites/yale/files/2025-09/Donor%20Advised%20Fund_2pager_2025_FIN.pdf | allowed; 200 | 50% |
| 5 | Notre Dame | https://plannedgiving.nd.edu/gift-options/how-to-give/donor-advised-fund/ | **robots unreachable → not fetched** | — |
| 6 | Dartmouth | https://giftplanning.dartmouth.edu/node/14 | allowed; 200 | not found (URL serves the general planned-giving page) |
| 7 | UCLA | https://legacy.ucla.edu/org_files/776/pdf/gift_pdf/Donor%20Advised%20Fund.pdf | allowed; 200 | 50% |
| 8 | Rochester (web) | https://rochester.giftplans.org/what-to-give/donor-advised-fund | allowed; 200 | 100/50/25/0% by size |
| 9 | Rochester (2024 PDF) | https://rochester.edu/giving/wilson-society/wp-content/uploads/2024/01/GP-2073_DAF_SlipSheet_R2-2.pdf | allowed; 200 | same tiers |
| 10 | Cornell (grant form) | https://giving.cornell.edu/make-a-grant/ | allowed; 200 | none on form |
| 11 | Cornell (brochure) | https://giving.cornell.edu/download/2558/ | allowed; 200 | 50% (<$500k), 25% (>$500k), none (>$1m) |
| 12 | Univ. of Minnesota Foundation | https://give.umn.edu/giving/donor-advised-funds | allowed; 200 | none (general explainer) |
| 13 | Michigan State | https://spartan.msu.edu/spartan-story-hub/news/2022/11/donor-advised-fund-offers-new-options-for-giving | allowed; 200 | 50% "MSU Only" account |
| 14 | UND Foundation | https://alumni.und.edu/gift-planning/donor-advised-funds.html | allowed; 200 | 51% of annual distributions |
| 15 | Brown | https://policy.brown.edu/policy/donor-advised-funds | allowed; 200 | 25% of each contribution |
| 16 | Penn Medicine | https://www.med.upenn.edu/pennmedplannedgiving/penn-donor-advised-fund.html | allowed; 200 | 50% |
| 17 | Harvard | https://alumni.harvard.edu/giving/gift-planning/DAF | allowed; 200 | 50% of distributions |
| 18 | MIT | https://giving.mit.edu/donor-advised-funds | **robots 403 → not fetched** | — |
| 19 | Michigan | https://giving.umich.edu/um/donor-advised-fund | allowed; **page 403** | — |
| 20 | Mayo Clinic | https://plannedgiving.mayoclinic.org/donor-advised-funds | allowed; 200 | 60% |
| 21 | Rotary Foundation | https://www.rotary.org/en/donate/donor-advised-fund | allowed; **page 429** | — |
| 22 | Indiana Univ. Foundation | https://iufoundation.iu.edu/ways-give/planned-giving/plan-a-future-gift/donor-advised-funds.html | allowed; 200 | none (page about external DAFs) |

"Allowed" means robots.txt returned 200 and allowed the path for ClaudeBot, anthropic-ai, Claude-User, Claude-Web, Claude-SearchBot, `research-script/1.0` and `*`.

**Count:** 18 programme pages read. 12 programmes state a host minimum. Three state none on the page read (Minnesota, IU, the Cornell grant form; Cornell's rule is in its brochure). Dartmouth's URL no longer carries DAF terms. Four were not read.

### 4.2 Verbatim quotes [F]
- **Stanford** (PDF, file dated 2025-02-25): "Half of the gift amount must be designated to Stanford. The other half may be used to support other approved charities. (Note that for gifts of $10 million or more, Stanford requires that only 40 percent come to the university; for a gift of $20 million or more, only 30 percent must be reserved for Stanford.)" Also: "Establish a donor advised fund at Stanford with a minimum gift of $1 million."
- **Columbia** (page © 2026): "Flexible: at least 50% goes to Columbia, and the rest may be distributed to other eligible nonprofit organizations." and "Minimum gift level: $1 million".
- **Yale:**
  - Web page: "At least 50% of your fund may be designated for Yale use, and the rest may be made to qualified public charities that you recommend."
  - 2025 PDF, two columns reassembled: "At least 50 percent of the gifts donated to the fund and any appreciation or income attributed to those amounts must be designated for purposes at Yale." Also "The minimum initial gift … is $5 million."
- **UCLA** (undated PDF, two columns reassembled): "At least 50% of the distributions should be directed to any area of UCLA." Also "The total annual distribution amount should be at least 5% of the fund's market value."
- **Rochester** (2024 PDF): "a certain percentage of a DAF must be vested, (allocated or reserved) for charitable purposes within the University of Rochester." The tiers are 100% ($100k–$199,999), 50% ($200k–$499,999), 25% ($500k–$999,999) and 0% ($1m+).
- **Cornell University Foundation** (undated brochure, columns reassembled): "For accounts under $500,000, 50% or more of the funds contributed must eventually be allocated to Cornell. For accounts greater than $500,000, 25% must be allocated to Cornell. … For accounts greater than $1,000,000, there is no minimum Cornell allocation."
- **Michigan State** (2022-11 article): "Fifty percent is allocated into the MSU Only account, and 50 percent is allocated into the Discretionary account." The programme was run with BNY Mellon. The repo records that BNY Mellon CGF terminated in December 2024; the programme's current status was not checked.
- **UND Foundation** (page © 2026, infographic text): "51 % … minimum of total annual grant distributions to UND".
- **Brown** (Effective Date: September 7, 2023): "One-quarter of the initial contribution and one-quarter of each addition made to the Fund and of any income and appreciation thereon, will be irrevocably donated and allocated to the Brown Portion."
- **Penn Medicine** (undated): "At least 50% of the gift must be designated over time to University programs, with the remaining balance available to other charitable organizations." and "At least 5% of the DAF must be distributed annually."
- **Harvard** (page © 2026): "(at least half of your distributions must be designated for Harvard)".
- **Mayo Clinic** (page © 2026, comparison-table cell): "Mayo Clinic receives 60% and other charities receive up to 40%".

### 4.3 Patterns [I]
- **50% is the modal rule.** It is written in three forms:
  - on **contributions** (Stanford, Yale PDF, Brown at 25%, Cornell);
  - on **distributions** (Columbia, UCLA, Harvard, UND);
  - as a **split account** (MSU, Mayo).
- **The required share falls with size** at Stanford, Cornell and Rochester, down to 0% at $1m+ for Cornell and Rochester. Large donors get near-commercial flexibility.
- **Entry minimums are high:** $100k at Cornell, Rochester, Brown, Mayo and UND; $250k at UCLA; $1m at Stanford and Columbia; $5m at Yale. This matches the roughly $0.9m average account in §2.2.
- **Payout rules are rare:** only UCLA and Penn state a 5% annual payout.

## 5. Limits
- **Self-sponsoring institutions:** DAF grants to the host are internal transfers and are invisible on Schedule I. The bounds are therefore wide, and there is no segment-wide point estimate. Point estimates exist only for DAF-dominant filers, and they assume all grants are DAF grants.
- **Line classes are text rules on purpose fields.**
  - Unlabelled DAF grants fall in "other".
  - Research sub-awards with non-research wording (Notre Dame's "See Part IV") also fall in "other", which widens the bounds.
  - Schedule R affiliates are counted as host. For example, Stanford Health Care counts as host for Stanford, and the American Repertory Theatre for Harvard.
- **Schedule I thresholds:** it itemises only grants over $5,000. Unitemised and foreign grants enter only `ext_max`.
- **Data quality:**
  - **UCLA Foundation:** negative filed DAF grants and imputed FY2024 values kept in the corrected panel.
  - **Université de Montréal:** a $0.43bn imputed FY2024 value with zero flows.
  - **Makeway Foundation:** negative DAF grants.
  - **Vanderbilt FY2023:** blank.
  - These are left as the corrected panel has them, and flagged in §2.3 and P-B5003-01/02.
- **Segment boundary:** NTEE-based classing is mechanical and puts a few non-institutions in the segment. Religious sponsors are excluded from "institutions" but are in T4.
- **Policy pages:**
  - Several are undated live pages, or PDFs whose sentences had to be reassembled from columns.
  - Rules may differ from the gift instrument actually signed.
  - Four target pages were not read (§4.1).
  - The page sample is search-driven, not random. It over-represents programmes that publish terms.
- **Coverage:** the panel is a floor for institutional DAF programmes (§2.4).

## 6. Source register
| ID | Source | URL | Used for |
|---|---|---|---|
| S1 | DAFRC Annual DAF Report 2025, updated analysis dataset | https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx | Panel (via repo CSV) |
| S2 | DAFRC 2025 report PDF | https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf | Market totals (via repo CSV) |
| S3 | IRS Form 990 e-file XML, GivingTuesday mirror of IRS TEOS (robots.txt 404, checked 2026-11-20) | `https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml`; 56 object ids in the CSV `return_object_id` / `url` columns | Schedule D/I/R, Part IX |
| S4 | IRS TEOS index (object ids, via repo harvest) | https://apps.irs.gov/pub/epostcard/990/xml/2025/index_2025.csv | Return selection |
| S5 | IRS EO BMF NTEE (via `daf-long-tail-sponsors-fy2021-2024.csv`) | https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf | Segment class |
| S6–S27 | Programme pages, as listed in §4.1 | see §4.1 | Host rules |
| R1 | Harvard FY2024 Form 990 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202531349349307548_public.xml | DAF Schedule I note |
| R2 | Cornell University Foundation FY2024 Form 990 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202511049349301926_public.xml | Point estimate |
| R3 | SUNY Binghamton Foundation FY2024 Form 990 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202443169349304339_public.xml | Greater Horizons line |
| R4 | University of Rochester FY2024 Form 990 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202521359349317402_public.xml | DAF note; Part IX line 1 = 0 |
| R5 | Rotary Foundation FY2024 Form 990 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202520929349300202_public.xml | "-DAF" lines; DAF programme text |

## 7. Data dictionary: `institutional-daf-programs-2026-11-20.csv`
One file, six `row_type`s. Columns not used by a row type are blank. Money is in USD.

| Column | Row types | Meaning |
|---|---|---|
| `row_type` | all | `segment_year` (40), `off_panel_inst_filers` (4), `sponsor` (302: institution and mission T4 sponsors), `schedule_i_sample` (56), `schedule_i_summary` (6), `policy_page` (22) |
| `fiscal_year` | segment_year, off_panel, sample, summary | FY = calendar year in which the tax period ends |
| `segment` | most | `ALL`; `T1_core_top50`; `T2_national_other`; `T3_community`; `T4_single_issue`; `T4:<t4_class>` |
| `ein`, `name` | sponsor, sample, policy | Sponsor EIN, and the name from DAFRC or the filed return |
| `dafrc_subtype`, `bmf_ntee` | sponsor | DAFRC subtype; IRS EO BMF NTEE code |
| `n_sponsor_rows`, `n_positive_assets` | segment_year, off_panel | Sponsor-year rows in the segment; rows with DAF assets > 0 |
| `daf_assets_eoy`, `daf_contributions`, `daf_grants`, `daf_accounts_eoy` | segment_year, off_panel | Corrected sums; for off_panel, filed sums |
| `share_<metric>` | segment_year | Segment sum ÷ corrected market total |
| `median_sponsor_assets` | segment_year | Median DAF assets of sponsors with positive assets |
| `grants_over_prior_year_assets` | segment_year | Segment grants ÷ segment prior-FY assets |
| `<metric>_fy<YYYY>` | sponsor | Corrected sponsor value for each FY2021–24 |
| `corrections_fy2021_24` | sponsor | R1–R4 rules applied to the sponsor |
| `tax_period_end`, `return_object_id`, `url` | sample | Return identity and XML URL |
| `sched_d_daf_grants`, `sched_d_daf_eoy`, `sched_d_daf_contributions`, `sched_d_daf_count` | sample, summary | Filed Schedule D Part I values (summary: summed D) |
| `structure` | sample | `sponsor_is_host` or `separate_foundation` |
| `sched_i_lines`, `sched_i_total` | sample | Count and sum of Schedule I Part II lines |
| `i_host`, `i_daf_labelled`, `i_research`, `i_other` (+ `n_*`) | sample, summary | Schedule I dollars (and line counts) per class (§1.2) |
| `unitemised_domestic` | sample | max(0, Part IX L1 − Schedule I total) |
| `foreign_grants_ix_l3`, `ix_l1` | sample | Part IX line 3 and line 1 |
| `n_related_orgs` | sample | Schedule R related organisations with an EIN |
| `daf_dominant` | sample | 1 if D ≥ 90% of Part IX L1 + L3 |
| `host_share_min`, `host_share_max` | sample, summary | Bounds on the share of D kept by the host (summary: D-weighted) |
| `host_share_point` | sample | Point estimate for DAF-dominant filers (= min bound; assumption) |
| `n_returns` | summary | Returns in the weighted bound |
| `robots_status`, `http_status`, `text_chars` | policy | robots verdict, page HTTP status, extracted text length |
| `extracted_sentences` | policy | Automatically extracted verbatim sentences (`||`-separated) |
| `host_rule`, `min_share_to_host`, `quote`, `page_date` | policy | Rule read, minimum share, verbatim quote, page date |
| `note`, `source` | all | Caveats; source description or URL |

## 8. Reproduce
```
python3 scripts/mission_institutional_dafs.py . --cache <scratch>/b5003/cache --fetch   # fetches 56 XMLs + 22 pages
python3 scripts/mission_institutional_dafs.py . --cache <scratch>/b5003/cache           # rebuild from cache
```
The script prints row counts and any mismatch against the corrected totals. The run on 2026-11-20 printed none.
