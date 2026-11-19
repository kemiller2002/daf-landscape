# P-GAP19-05: a public exception-load proxy for the top-50 DAF sponsors, FY2023–FY2024

**Date:** 2026-11-19 · **Queue item:** P-GAP19-05 (from the [thoroughness gap audit](thoroughness-gap-audit-2026-11-19.md) §4, row 5)

**Outputs**
- [`data/mission-2026-11-14/exception-load-proxy-2026-11-19.csv`](../../data/mission-2026-11-14/exception-load-proxy-2026-11-19.csv): 167 rows [V wave 32A]
  - 100 `sponsor_year` rows, 94 of them with itemised Schedule I;
  - 48 `sponsor` rows (FY2023–24 pooled);
  - 6 `sponsor_type` rows, 5 `dafrc_segment` rows, 3 `all` rows, 1 `big4_nationals` row, and 4 single-year rows (`all_fy`, `big4_fy`).
  - The data dictionary is in §7.
- [`data/mission-2026-11-14/queue-proposals-gap19-05.csv`](../../data/mission-2026-11-14/queue-proposals-gap19-05.csv): P-G05-01..06.
- **Script:** [`scripts/mission_exception_load.py`](../../scripts/mission_exception_load.py) (stdlib, functional style: pure functions over immutable inputs, I/O only in `main`).
  - The universe, return choice, Schedule I lines and DAF-to-DAF flag are imported unchanged from `mission_recipient_sectors.py`.
  - The per-line IRS screen and its labels (`screen`, `labels_of`, `EXPLAINING`) are imported unchanged from `mission_recipient_compliance.py`.
  - Schedule F figures are read from `daf-foreign-grants-schedule-f-2023-2024.csv` (`mission_foreign_grants.py`).

**Rules applied**
- **Read first:**
  - [direction-recipient-compliance-screen.md](direction-recipient-compliance-screen.md), including its wave-26 corrections. They change the wording of two labels, not the line data used here.
  - [direction-foreign-grants-schedule-f.md](direction-foreign-grants-schedule-f.md).
  - [breadth-community-faith-infrastructure-emerging.md](breadth-community-faith-infrastructure-emerging.md) §6 (Q-B15). This is the existing four-national exception measure, quoted in [DAF-INDUSTRY-REPORT-2026-11.md](../DAF-INDUSTRY-REPORT-2026-11.md) §4 as "about 2.5–3% of dollars".
- **Recency:** every grant line is from a return with a tax period ending 2023-03-31 to 2024-12-31 (DAFRC FY2023–FY2024). The Pub 78 and BMF files are 2026-11 snapshots. Nothing before 2021 is used, except BMF ruling months as recorded on today's file.
- **No new bulk downloads:**
  - All inputs are the scratch copies already verified in P-NEW-REC-01 and P-NEW-FGN-01 (Content-Length and Last-Modified checked there).
  - Three small pages were requested to verify the source register: the IRS BMF landing page, its field guide `eo-info.pdf`, and the Schedule I/F "about" pages.
  - www.irs.gov/robots.txt was re-read on 2026-11-19. It disallows `/charities-non-profits/tax-exempt-organization-search` (a prefix) and the `forms-pubs-*-search` paths. One HEAD request went to `/charities-non-profits/tax-exempt-organization-search-bulk-data-downloads` before the prefix rule was noticed. That page is not used or cited here.
  - No crt.sh, certspotter or sec.gov. No outreach.
- **Labels:** **[F]** filed or IRS-published value; **[C]** computed by the script; **[I]** inference.
- **Framing.** A flag means the line would plausibly fall outside a sponsor's routine "listed public charity" path. It does **not** mean the grant was improper. It also does not say how a given sponsor actually routes the grant.

---

## 0. Answers in brief

Scope: 48 top-50 sponsors (46 DAFRC top-50 plus Stanford and UCLA Foundation, as in P-NEW-REC-01), 94 itemising sponsor-years. That is 604,915 Schedule I Part II lines ($91.02bn) plus 3,697 Schedule F foreign recipients ($1.92bn of Part IX line 3). The denominator is **608,612 recipient lines and $92.94bn** [F/C].

| Question | Answer [C] |
|---|---|
| **Broad proxy** (the five categories exactly as briefed) | **25.1% of recipient lines, 19.9% of dollars.**<br>Here the count share is the *larger* one: gap −5.2 pp, dollar share ÷ count share 0.79×. The reason is that 19.3% of lines go to recipients absent from Pub 78, mostly small church and group-subordinate lines. |
| **Core proxy** (unlabelled non-list recipients only; rulings inside the window only) | **7.4% of lines, 11.2% of dollars.**<br>The dollar share is larger: gap +3.75 pp, 1.51×.<br>Excluding SVCF and the university/hospital sponsors: **7.2% / 9.8%**. Without the Greater Horizons FY2024 totals row (§2), core is 7.41% / **10.96%** (gap +3.55 pp, 1.48×) and 7.2% / 9.6% excluding SVCF and university/hospital sponsors [V wave 32A] |
| **Count-vs-dollar gap by category** | - Fiscal-sponsor names: 0.12% of lines vs 1.30% of dollars (**10.7×**); on the EIN-keyed host list (19 Q-B15 hosts plus the Fiscal Sponsor Directory; $92.72bn base) 0.44% vs 1.94% (4.4×), or 0.42% vs 1.68% (4.0×) without 50CAN, Global Impact, NEO Philanthropy and Myriad USA ([g0503-0501-exception-proxy-refinements.md](g0503-0501-exception-proxy-refinements.md)) [V wave 39C]<br>- Private foundations / ER: 0.39% vs 1.39% (3.5×).<br>- Foreign: 0.63% vs 2.07% (3.3×).<br>- Recent ruling: 4.8% vs 5.9% (1.2×).<br>- Not 501(c)(3) or not in Pub 78: 19.3% vs 9.3% (**0.48×**). |
| **By sponsor type** (core, count / dollars) | - National (15 sponsors; Servant Foundation is counted under faith): 7.0% / 10.2%, or 7.0% / 9.9% without the Greater Horizons totals row [V wave 32A]<br>- Community foundation (22): 8.5% / **16.2%**.<br>- Faith (7, including Servant Foundation): 8.1% / 9.1%.<br>- DonorsTrust (single-issue, non-faith): 12.0% / 8.2%.<br>- Dechomai (processor, 9 lines): 22.2% / 5.6%.<br>- University/hospital (2): 60.0% / 3.8%. |
| … the distribution across sponsors | Sponsor-level broad dollar share: median **16.4%** (IQR 13.4–21.1%), range 1.35% (UCLA Foundation) to 59.8% (Greater Horizons, driven by one blank line of $212m). Outside the university/hospital sponsors the lowest is 5.6% (Dechomai, 9 lines), then 7.9% (Ayco). The 59.8% at Greater Horizons is an e-file totals row (§2). Without it Greater Horizons is 19.8%, the maximum is SVCF at 45.8% and the p75 is 20.7% [V wave 32A]<br>Sponsor-level broad count share: median 19.7% (IQR 15.5–25.2%). |
| … community foundations | The pooled community-foundation dollar share exceeds its count share by **+11.4 pp** (broad) and +7.7 pp (core). The **median CF** gap is −1.2 pp (broad), so the pooled gap comes from a few large lines, chiefly SVCF's $1.309bn FY2023 line to Further Future Foundation (BMF ruling 2023-03). |
| **Four nationals compared** (Fidelity, DAFgiving360, Vanguard, NPT) | **Like-for-like with the existing measure** (foreign + named fiscal sponsors + non-501(c)(3) IRC codes), FY2023–24: 1.96% + 1.50% + 0.15% ≈ **3.6% of dollars** (≈4.2% with the EIN-keyed fiscal-sponsor list at 2.10%; ≈3.9% without four directory hosts with large programmes of their own) [V wave 39C] The existing measure, for FY6/2025, is 1.46% + ≈1.20% + ≈0.03% = "2.5–3%". The difference is mostly NPT's higher FY2023–24 foreign share (7.4% vs 4.84%).<br>**Full proxy:** core 7.3% of lines / **10.0% of dollars**; broad 28.3% / 17.8%.<br>The existing measure therefore covers roughly a third of the core dollar proxy at these four. The difference is private foundations (2.05% of dollars, mostly operating foundations), recent rulings (4.25%) and unexplained non-list recipients (0.98%). |
| **Count side of the existing measure** | The existing "0.3–1% by count at nationals" [I] is reproduced for its own components: foreign + fiscal-sponsor lines are **0.47%** of big-4 lines (0.67% with the EIN-keyed fiscal-sponsor list) [V wave 39C] It does not hold for the full proxy: 7.3% (core) or 28.3% (broad) of recipient lines. |

**Reading [I]**
- On public data, the share of DAF grant flow that falls outside "listed 501(c)(3), long recognised, US, not a fiscal sponsor, not a private foundation" is **about 7% of recipient lines and 10–11% of dollars** on the core definition. The broad definition gives 20–25%. With the EIN-keyed fiscal-sponsor list and time-correct rulings the core is 7.76% / 11.61% (6.80% / 11.00% counting only true new organisations as recent) and the broad 24.79% / 19.85% ([g0503-0501-exception-proxy-refinements.md](g0503-0501-exception-proxy-refinements.md)) [V wave 39C]
- At the big nationals, a **dollar-weighted** measure overstates the review load relative to counts only for the categories already measured (foreign, fiscal sponsors, PFs). For the largest category, recipients missing from Pub 78 (churches and group subordinates), it **understates** it.
- Which way the gap runs depends on the definition. The old claim that "count-weighted it is far smaller" is true only for foreign and fiscal-sponsor grants.
- Community foundations carry the heaviest pooled **dollar** load. By median sponsor they are similar to the nationals.
- All of this is an upper-leaning screen. Many flagged lines (churches, group subordinates, government units, well-known POFs) are cleared by sponsors through standing rules, not case review. No sponsor publishes the actual routing (§5).

---

## 1. Method

1. **Universe and lines.**
   - Exactly those of P-NEW-REC-01: the top-50 DAFRC sponsors by FY2024 DAF assets, with one return per sponsor × DAFRC fiscal year (`mission_daf_to_daf.pick_returns` over the `netpayout990/` cache).
   - Every Schedule I Part II `RecipientTable` line comes from the P-NEW-REC-01 line cache. 94 of 94 itemising sponsor-years loaded, and the 604,915 lines and $91.02bn match that direction exactly [C].
   - **Not covered:** six sponsor-years file Schedule I as an attachment only, so their recipient lines are not public in e-file form:
     - BofA Charitable Gift Fund FY2023 and FY2024;
     - Renaissance Charitable Foundation FY2023 and FY2024;
     - Greater Horizons FY2023;
     - Greater Kansas City CF FY2023.
   - These have `sponsor_year` rows carrying only Part IX line 3 and total grants, and are left out of every aggregate. **Ranks 9 (Renaissance) and 11 (BofA) therefore have no proxy.**
2. **Grant year.** The return's tax period: end = `tax_period_end`, start = end − 1 year + 1 day. Schedule I has no grant dates.
3. **Line screen.**
   - `mission_recipient_compliance.screen` is applied unchanged: Pub 78 presence and codes, the EO BMF fields, and the legitimate-absence labels.
   - Placeholder EINs (999999999 and similar) are treated as blank.
   - The revocation list is not one of the five briefed categories, so it is not re-applied. Its results are in P-NEW-REC-01 (§6 below).
4. **Categories** (per line, not mutually exclusive):

   | Category | Rule | Source fields |
   |---|---|---|
   | `foreign` | Schedule I line with a foreign address (`F:` country) or a non-US Pub 78 country (code FORGN), **plus** every Schedule F foreign grant | Sched I address; Pub 78 country; Form 990 Part IX line 3 ($) and Schedule F Part II line 2 recipient counts (`Total501c3OrgCnt` + `TotalOtherOrgCnt`), or the number of Part II rows where line 2 is blank, plus Part III recipients |
   | `not_c3_or_not_pub78` | Blank/placeholder EIN; or EIN not in Pub 78; or BMF SUBSECTION ≠ 03; or BMF DEDUCTIBILITY = 2 | Pub 78; BMF |
   | `not_c3_or_not_pub78_unexplained` | As above, minus lines carrying one of the P-NEW-REC-01 explaining labels: government, church/religious, group subordinate, possible public university, LLC/possible disregarded entity, foreign | labels [I] |
   | `recent_ruling_24m` | BMF RULING month (YYYYMM) ≥ grant-year start − 24 months. Includes rulings dated after the grant year; that subset is reported separately (`recent_ruling_after_period_end_*`) | BMF RULING ("the month and year on a ruling or determination letter recognizing the organization's exempt status", [IRS eo-info.pdf](https://www.irs.gov/pub/foia/ig/tege/eo-info.pdf)) |
   | `fiscal_sponsor_name` | Normalised recipient name matches the 19-host Q-B15 list (New Venture Fund, Tides Foundation/Center, Hopewell, Windward, Rockefeller Philanthropy Advisors, Fractured Atlas, Community Partners, Social Good Fund, Players Philanthropy Fund, Trust for Conservation Innovation, Earth Island Institute, Third Sector New England, SEE, North Star Fund, Public Health Institute, Multiplying Good, FJC, Open Collective Foundation, Propel Nonprofits), or a generic marker ("fiscal sponsor/agent", "a project of", "sponsored project") | name rule [I] |
   | `pf_or_er` | **ER required** (`er_required`): Pub 78 code PF or SONFI, or BMF FOUNDATION 04 (private non-operating foundation) or 24 (509(a)(3) Type III not functionally integrated). **Operating foundation** (`pof_only`): Pub 78 POF, or BMF FOUNDATION 02/03 | Pub 78; BMF FOUNDATION codes per [eo-info.pdf](https://www.irs.gov/pub/foia/ig/tege/eo-info.pdf) |
   | `any` (broad) | Union of the five categories as briefed | — |
   | `any_core` | Union of foreign, `not_c3_or_not_pub78_unexplained`, recent rulings dated **inside** [start − 24 months, end], fiscal sponsor, and PF/ER | — |

   **Legal basis for the PF/ER split [F/I]:**
   - Under [26 U.S.C. §4966(c)](https://www.law.cornell.edu/uscode/text/26/4966), a DAF distribution escapes taxable-distribution status without expenditure responsibility only when it goes to a §170(b)(1)(A) organisation (other than a disqualified supporting organisation), to the sponsor, or to another DAF.
   - Private operating foundations are §170(b)(1)(A)(vii) organisations, via (F)(i) ([26 U.S.C. §170](https://www.law.cornell.edu/uscode/text/26/170)). They are therefore split out as `pof_only`: verification is needed, but not ER.
   - Non-operating PFs and Type III non-functionally-integrated SOs need ER under [§4945(h)](https://www.law.cornell.edu/uscode/text/26/4945) standards. The `er_required` flag is approximate in both directions. It overstates, because conduit and common-fund PFs (§170(b)(1)(F)(ii)–(iii)) are also (A)(vii) organisations. It understates, because donor-controlled Type I, Type II and functionally integrated Type III SOs are disqualified supporting organisations under §4966(d)(4)(A)(ii) but are not screened, and Pub 78 `SOUNK` recipients are not flagged [V wave 32A]
5. **Denominators.**
   - **Count:** Schedule I lines + Schedule F foreign recipients.
   - **Dollars:** Schedule I dollars (cash + non-cash) + Part IX line 3.
   - **Shares:** every category share uses these denominators, so categories can be compared and unions taken.
   - **Double counting:** Schedule I lines with a foreign address hold only **$12.2m**, against $1.92bn on line 3, so any double count of a foreign grant on both schedules is immaterial [C].
   - **DAF-to-DAF lines** ($12.73bn) stay in the base, as in P-NEW-REC-01. `any_*_ex_d2d` gives the broad shares without them.
6. **Sponsor type.**
   - `dafrc_segment` is the DAFRC segment.
   - `sponsor_type` splits single-issue into `faith` and `single_issue_other`, and moves Servant Foundation (The Signatry; a DAFRC "national") into `faith` [I, by charter and name].
   - **Faith** = NCF, Jewish Communal Fund, CJP Boston, Jewish Community Federation of San Francisco, Jewish Community Foundation of Los Angeles, Thrivent Charitable, Servant Foundation.
   - **`single_issue_other`** = DonorsTrust.
7. **Distribution.**
   - Each `sponsor_type` and `dafrc_segment` row gives the pooled shares, plus min / p25 / median / p75 / max of the **sponsor-level** pooled broad shares (`sponsor_any_*`), using inclusive quartiles.
   - The core-proxy sponsor distribution can be recomputed from the 48 `sponsor` rows.

## 2. Coverage and checks [C]

- 100 sponsor-years present; 94 itemised and loaded; 0 Schedule F rows missing; 0 object-id mismatches between the Schedule I return and the Schedule F row.
- **Schedule F count basis** for the 94 sponsor-years:
  - line 2 counts: 56, plus 5 that also have Part III recipients;
  - Part II rows used because line 2 is blank: 3;
  - no foreign grants: 28;
  - line 3 dollars but no count: 2 (AEF FY2024 $10,000; Raymond James FY2024 $200).
  - Where only Part II rows are available, each row is region × purpose, not a recipient, so the count is understated there.
- **Fiscal-sponsor matches:** 740 lines, $1.212bn, 25 recipient keys. All but about $55k (two generic-marker lines) come from the named list. Two false positives found in testing ("Quoddy Tides Foundation", "Illinois Public Health Institute") were removed by anchoring the patterns.
- **The largest single lines** that drive sponsor-level dollar shares:
  - SVCF FY2023 → Further Future Foundation (92-1117448), **$1,309.0m**, BMF ruling 2023-03 (recent ruling). The recipient renamed itself Navigation Charitable Fund on 2023-11-01. By end-2024 it had granted $41.1m and held $883.5m in its wholly owned for-profit, Voltage Park, Inc. ([b41n17-g0505-unlisted-recipients.md](b41n17-g0505-unlisted-recipients.md) §4.2) [V wave 36B]
  - Greater Horizons FY2024: a line with **no name and no EIN**, $212.2m (blank EIN, so `not_c3_or_not_pub78_unexplained`). It is not a grant. $212,187,406 is exactly the sum of the return's 3,282 named lines, and a second blank line carries $3,282, the line count. Together they are an e-filed totals row, so Greater Horizons' Schedule I dollars are double-counted. No other return among the 94 has this pattern [V wave 32A]
  - SVCF FY2023 → The Just Trust for Education, $131.6m (ruling 2023-02);
  - NPT FY2024 → BM-A Institute, $83.1m (ruling 2024-09, after NPT's year-end);
  - NCF: blank-EIN church lines of $88.0m (First Baptist Church Chandler, FY2023) and $54.0m (First Baptist Church of Fremont, FY2024).

## 3. Results

### 3.1 Pooled, all 48 sponsors (94 sponsor-years), FY2023–24 [C]
Denominator: 608,612 lines; $92.94bn. **Validation note:** this includes Greater Horizons' FY2024 totals row (two blank lines: $212,187,406 and 3,282). Without it the denominator is 608,610 lines and $92.72bn; raw not-c3/not-Pub-78 is 9.11% of dollars (0.47×); unexplained is 13,568 lines and $0.89bn (0.96%); blank EIN with no label is $0.06bn on 1,095 lines; broad is 25.08% / 19.72%; core is 7.41% / 10.96% (gap +3.55 pp); and FY2024 core is 7.36% / 9.73% [V wave 32A]

| Category | Lines | $ | Count share | Dollar share | Gap ($ − count), pp | $ share ÷ count share |
|---|---|---|---|---|---|---|
| Foreign (Sched I foreign address + Sched F) | 3,805 | $1.93bn | 0.63% | 2.07% | +1.45 | 3.32× |
| Not 501(c)(3) or not in Pub 78 (raw) | 117,401 | $8.66bn | 19.29% | 9.32% | −9.97 | 0.48× |
| … unexplained (no legitimate-absence label) | 13,570 | $1.10bn | 2.23% | 1.19% | −1.04 | 0.53× |
| BMF ruling ≤24 months before the grant year (or later) | 29,082 | $5.52bn | 4.78% | 5.94% | +1.16 | 1.24× |
| Fiscal-sponsor name | 740 | $1.21bn | 0.12% | 1.30% | +1.18 | 10.72× (EIN-keyed list on $92.72bn: 2,682 lines, $1.80bn, 0.44% / 1.94%, 4.4×) [V wave 39C]
| Private foundation / ER | 2,396 | $1.29bn | 0.39% | 1.39% | +0.99 | 3.52× |
| **Any (broad union)** | **152,661** | **$18.50bn** | **25.08%** | **19.90%** | **−5.18** | **0.79×** |
| **Any (core union)** | **45,104** | **$10.37bn** | **7.41%** | **11.16%** | **+3.75** | **1.51×** |

**Sub-components [C]:**
- **Private foundation / ER:**
  - ER required (PF/SONFI, or BMF 04/24): 422 lines, **$140.6m**;
  - operating foundations only: 1,974 lines, **$1.147bn**.
  - The largest are Lucas Museum of Narrative Art ($200.0m), XQ Institute ($134.1m), Schmidt Ocean Institute ($98.0m), Global Support and Development ($85.7m) and Chicago CRED ($66.5m), all POF.
  - The largest ER-required lines are Founders Pledge Inc ($53.9m: BMF code 04 but Pub 78 PC, so the IRS lists disagree. A sponsor relying on Pub 78 under Rev. Proc. 2018-32 would treat it as a public charity. Without it the ER-required total is about $86.7m [V wave 32A]), Huntington Foundation ($43.6m, Columbus Foundation) and Breakthrough Prize in Life Sciences Foundation ($6.0m, SVCF).
  - P-NEW-REC-01's narrower Pub 78-only PF/SONFI screen found 302 lines and $81.7m.
- **Recent rulings:** 4,090 lines ($588.8m) carry a ruling month **after** the grant year ended.
  - Examples: BM-A Institute 2024-09; Charter Fund 2025-08; Musical Instrument Museum 2025-08; KIPP New York 2025-12.
  - For long-established organisations a recent ruling month fits reinstatement or re-determination better than a new charity [I]. The core union excludes these lines.
- **Fiscal sponsors:** the top hosts are New Venture Fund ($432.0m, 47 lines), Rockefeller Philanthropy Advisors ($245.7m), Hopewell Fund ($149.6m), Tides Foundation ($112.2m), Windward Fund ($79.5m) and Tides Center ($67.9m).
- **Raw not-in-Pub-78 dollars ($8.66bn) by label:**

  | Label | $ | Lines |
  |---|---|---|
  | Church + group subordinate | $2.41bn | 50,520 |
  | LLC (CZ Biohub et al.) | $1.68bn | 87 |
  | Church | $1.58bn | 37,662 |
  | Group subordinate | $1.21bn | 10,794 |
  | **No label** | **$0.83bn** | **12,473** |
  | Government | $0.45bn | 3,190 |
  | Blank EIN, no label | $0.27bn | 1,097 |
  | Possible public university | $0.20bn | 1,032 |

  The 98,976 church and subordinate lines ($5.20bn) average about $52.5k, against $152.7k for the whole base. That is why this category, and with it the broad union, is **count-heavy**.

**By year:**
- Broad: FY2023 25.3% / 23.5%; FY2024 24.9% / 16.9%.
- Core: FY2023 7.5% / 12.4%; FY2024 7.4% / 10.1%.
- The FY2023 dollar figures include SVCF's $1.31bn Further Future line and its $1.66bn CZ Biohub LLC lines.

**Sensitivity:**
- Excluding university/hospital sponsors and SVCF (88 sponsor-years): broad 25.1% / 17.5%; core **7.2% / 9.8%**. Without the Greater Horizons totals row: broad 25.1% / 17.3%, core 7.2% / 9.6% [V wave 32A]
- Excluding DAF-to-DAF lines: broad 25.3% / 22.8%.

**Average line size:** $121,158 on flagged lines against $163,263 on others (broad). On the broad definition the flagged lines are smaller on average.

### 3.2 Distribution by sponsor type, FY2023–24 [C]
| Sponsor type | Sponsors (sponsor-years) | Lines | $ | Broad: count | Broad: $ | Broad gap pp | Core: count | Core: $ | Core gap pp | Sponsor median broad $ (p25–p75) | Sponsor median broad count (p25–p75) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| National (excl. Servant) | 15 (29) | 466,753 | $62.50bn | 26.47% | 17.83% | −8.6 | 7.02% | 10.18% | +3.2 | 16.78% (15.08–20.02%) | 24.54% (16.91–27.35%) [V wave 32A] |
| Community foundation | 22 (43) | 83,267 | $18.72bn | 17.49% | 28.89% | **+11.4** | 8.51% | **16.17%** | +7.7 | 14.65% (13.45–23.26%) | 18.33% (15.27–21.94%) |
| Faith (incl. Servant) | 7 (14) | 56,068 | $9.18bn | 24.60% | 19.26% | −5.3 | 8.13% | 9.14% | +1.0 | 18.54% (13.83–22.46%) | 24.62% (15.74–26.78%) |
| Single-issue, other (DonorsTrust) | 1 (2) | 1,705 | $0.63bn | 16.42% | 13.02% | −3.4 | 12.02% | 8.22% | −3.8 | n=1 | n=1 |
| Processor (Dechomai) | 1 (2) | 9 | $0.89bn | 22.22% | 5.60% | −16.6 | 22.22% | 5.60% | −16.6 | n=1 | n=1 |
| University/hospital | 2 (4) | 810 | $1.01bn | 61.36% | 4.01% | −57.3 | 60.00% | 3.80% | −56.2 | n=2 | n=2 |
| *Big-4 nationals* | 4 (8) | 337,139 | $49.14bn | 28.25% | 17.82% | −10.4 | 7.32% | 10.02% | +2.7 | 17.89% (16.13–19.42%) | 26.71% (24.08–29.21%) |
| *All* | 48 (94) | 608,612 | $92.94bn | 25.08% | 19.90% | −5.2 | 7.41% | 11.16% | +3.8 | 16.36% (13.39–21.08%) | 19.68% (15.48–25.18%) |

**Dollar shares by category and type [C]:**

| Sponsor type | Foreign | Not c3 / not Pub 78 (raw) | … unexplained | Recent ruling | Fiscal sponsor | PF/ER |
|---|---|---|---|---|---|---|
| National (excl. Servant) | 1.96% | 8.42% | 1.36% | 4.36% | 1.49% | 1.75% [V wave 32A] |
| Community foundation | 2.73% | 13.47% | 1.05% | **11.04%** | 1.02% | 0.77% |
| Faith | 1.83% | 9.08% | 0.48% | 6.89% | 0.99% | 0.51% |
| Big-4 nationals | 2.00% | 8.20% | 0.98% | 4.25% | 1.47% | **2.05%** |

**Count shares by category and type [C]:**

| Sponsor type | Foreign | Not c3 / not Pub 78 (raw) | … unexplained | Recent ruling | Fiscal sponsor | PF/ER |
|---|---|---|---|---|---|---|
| National (excl. Servant) | 0.36% | 21.13% | 2.28% | 4.64% | 0.08% | 0.39% [V wave 32A] |
| Community foundation | **1.34%** | 10.98% | 2.51% | 4.53% | **0.34%** | 0.41% |
| Faith | 0.98% | 16.98% | 1.41% | **6.20%** | 0.13% | 0.38% |
| Big-4 nationals | 0.43% | 22.61% | 2.33% | 4.91% | 0.04% | 0.41% |

**Reading [I]:**
- **National and faith sponsors** have count-heavy broad loads. Their many small church and group-subordinate lines (NCF, Thrivent, Fidelity, DAFgiving360) are absent from Pub 78. Under Rev. Proc. 2018-32 these can usually be cleared from the BMF or a group ruling.
- **Community foundations** have the most dollar-heavy load. Their **pooled** dollar-minus-count gap is +11.4 pp, but the **median CF** gap is −1.2 pp. The pooled gap comes mostly from SVCF (recent-ruling $1.31bn; foreign 4.2%), Marin (foreign 16.4% of dollars) and Community Foundation of New Jersey (PF/ER 12.6%).
- Among the national, community-foundation and faith types, community foundations have the highest foreign and fiscal-sponsor **count** shares (1.34% and 0.34%), about four times the nationals'. The two university/hospital sponsors are higher on foreign counts (56.2%) [V wave 32A]
- **University/hospital sponsors** are an outlier on counts. Stanford's 286 Part III foreign individual grants and Schedule F counts sit on a base of only 685 lines.

### 3.3 Per sponsor, FY2023–24 pooled [C]
Ranks 9 (Renaissance) and 11 (BofA CGF) are absent because their Schedule I is attachment-only (§1.1). "Lines" = Schedule I lines + Schedule F foreign recipients. Every column for every sponsor-year is in the CSV.

| Rank | Sponsor | Type | Lines + foreign recipients | $ | Any: count / $ | Core: count / $ | Core gap pp | Foreign $ | Fiscal-sponsor $ | PF/ER $ | Recent ruling $ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Fidelity Investments Charitable Gift Fund | national | 152,859 | $22.76bn | 30.20% / 16.78% | 7.55% / 8.32% | +0.8 | 0.52% | 1.78% | 0.72% | 4.54% |
| 2 | National Philanthropic Trust | national | 34,982 | $9.98bn | 22.70% / 20.69% | 9.55% / 15.75% | +6.2 | 7.45% | 2.05% | 3.09% | 3.98% |
| 3 | Donor Advised Charitable Giving Inc | national | 103,708 | $11.36bn | 28.88% / 18.99% | 6.93% / 9.56% | +2.6 | 0.98% | 0.87% | 3.98% | 3.49% |
| 4 | Vanguard Charitable Endowment Program | national | 45,590 | $5.04bn | 24.54% / 14.17% | 5.68% / 7.34% | +1.7 | 0.22% | 0.30% | 1.70% | 5.17% |
| 5 | Gs Donor Advised Philanthropy Fund | national | 13,733 | $5.19bn | 12.91% / 14.83% | 6.49% / 11.51% | +5.0 | 3.47% | 2.97% | 0.41% | 4.99% |
| 6 | Silicon Valley Community Foundation | community_foundation | 7,441 | $8.39bn | 21.46% / 45.84% | 16.54% / 25.24% | +8.7 | 4.20% | 0.85% | 0.34% | 19.53% |
| 7 | American Endowment Foundation | national | 27,110 | $2.44bn | 25.81% / 16.69% | 6.79% / 6.14% | -0.7 | 0.01% | 0.32% | 1.47% | 2.97% |
| 8 | Morgan Stanley Global Impact Funding Trust | national | 35,350 | $2.40bn | 18.39% / 19.34% | 6.29% / 9.90% | +3.6 | 1.86% | 0.46% | 0.32% | 6.63% |
| 10 | Natl Christian Charitable Fdn Inc | faith | 30,884 | $4.62bn | 24.62% / 20.85% | 7.50% / 5.89% | -1.6 | 0.03% | 0.05% | 0.69% | 6.14% |
| 12 | The Chicago Community Trust | community_foundation | 7,815 | $3.04bn | 15.64% / 14.04% | 7.72% / 9.67% | +2.0 | 1.93% | 2.27% | 0.81% | 4.12% |
| 13 | Impactassetsinc | national | 5,455 | $0.84bn | 16.63% / 16.95% | 10.76% / 15.00% | +4.2 | 1.19% | 3.61% | 0.57% | 8.88% |
| 14 | Foundation For The Carolinas | community_foundation | 3,004 | $1.13bn | 20.97% / 8.34% | 7.79% / 5.18% | -2.6 | 0.00% | 0.20% | 0.17% | 3.59% |
| 15 | Jewish Communal Fund | faith | 9,061 | $1.91bn | 13.73% / 16.81% | 8.65% / 14.72% | +6.1 | 5.77% | 4.09% | 0.42% | 4.79% |
| 16 | Greater Kansas City Community Foundation | community_foundation | 2,413 | $0.35bn | 26.19% / 25.93% | 9.24% / 7.13% | -2.1 | 0.18% | 0.12% | 0.45% | 3.08% |
| 17 | Greater Horizons | national | 3,294 | $0.43bn | 25.17% / 59.76% | 7.29% / 54.60% | +47.3 | 0.37% | 0.04% | 0.54% | 3.35% |
| 18 | Dechomai Asset Trust | processor | 9 | $0.89bn | 22.22% / 5.60% | 22.22% / 5.60% | -16.6 | 0.00% | 0.00% | 0.00% | 5.59% |
| 19 | Combined Jewish Philanthropies Of Greater  | faith | 2,072 | $0.50bn | 17.76% / 10.23% | 8.20% / 6.14% | -2.1 | 0.22% | 1.20% | 0.23% | 3.98% |
| 20 | Raymond James Charitable Endowment Fund | national | 12,716 | $0.52bn | 29.39% / 23.88% | 5.02% / 7.05% | +2.0 | 0.01% | 0.13% | 1.16% | 3.92% |
| 21 | The Ayco Charitable Foundation | national | 8,902 | $0.53bn | 14.32% / 7.94% | 3.19% / 1.65% | -1.5 | 0.04% | 0.03% | 0.27% | 1.31% |
| 22 | The Us Charitable Gift Trust | national | 12,030 | $0.41bn | 34.51% / 24.89% | 7.67% / 6.07% | -1.6 | 0.00% | 0.07% | 0.25% | 2.95% |
| 23 | Columbus Foundation | community_foundation | 3,539 | $0.56bn | 25.09% / 23.76% | 8.28% / 12.79% | +4.5 | 0.24% | 0.09% | 8.67% | 3.04% |
| 24 | The New York Community Trust | community_foundation | 5,158 | $0.38bn | 10.04% / 9.00% | 3.99% / 5.95% | +2.0 | 0.02% | 1.76% | 0.57% | 2.95% |
| 25 | The Oregon Community Foundation | community_foundation | 4,198 | $0.36bn | 18.37% / 13.44% | 7.22% / 4.00% | -3.2 | 0.02% | 0.18% | 0.04% | 2.48% |
| 26 | Donors Trust Inc | single_issue_other | 1,705 | $0.63bn | 16.42% / 13.02% | 12.02% / 8.22% | -3.8 | 0.06% | 0.01% | 0.35% | 6.86% |
| 27 | Boston Foundation Inc | community_foundation | 4,119 | $0.34bn | 13.28% / 16.48% | 6.29% / 11.02% | +4.7 | 0.99% | 1.07% | 0.18% | 8.64% |
| 28 | California Community Foundation | community_foundation | 4,018 | $0.61bn | 14.16% / 13.49% | 7.91% / 8.25% | +0.3 | 1.95% | 1.90% | 0.26% | 3.77% |
| 29 | The Community Foundation For Greater | community_foundation | 2,745 | $0.32bn | 16.54% / 9.48% | 7.10% / 5.03% | -2.1 | 0.10% | 0.56% | 0.04% | 3.78% |
| 30 | Servant Foundation | faith | 4,788 | $1.47bn | 27.74% / 18.54% | 7.79% / 11.23% | +3.4 | 0.00% | 0.00% | 0.25% | 14.04% |
| 31 | Jewish Community Federation Of San | faith | 2,105 | $0.23bn | 11.12% / 10.85% | 8.93% / 9.51% | +0.6 | 2.42% | 1.00% | 1.03% | 4.82% |
| 32 | The Bessemer Giving Fund | national | 3,019 | $0.27bn | 12.69% / 10.86% | 4.67% / 6.73% | +2.1 | 0.58% | 1.13% | 0.94% | 3.08% |
| 33 | Greater Houston Community Foundation | community_foundation | 3,450 | $0.45bn | 21.42% / 14.96% | 8.78% / 6.90% | -1.9 | 2.43% | 0.20% | 0.57% | 3.48% |
| 34 | Marin Community Foundation | community_foundation | 2,707 | $0.34bn | 15.59% / 24.32% | 11.86% / 22.62% | +10.8 | 16.43% | 1.51% | 0.18% | 2.77% |
| 35 | Community Foundation Of New Jersey | community_foundation | 2,534 | $0.16bn | 18.39% / 27.66% | 8.48% / 22.08% | +13.6 | 1.51% | 0.47% | 12.62% | 13.65% |
| 36 | American Gift Fund | national | 3,311 | $0.16bn | 17.19% / 15.32% | 4.41% / 4.26% | -0.2 | 0.01% | 0.02% | 0.11% | 2.86% |
| 37 | Jewish Community Foundation Of Los Angeles | faith | 2,466 | $0.31bn | 25.83% / 24.07% | 22.34% / 21.04% | -1.3 | 16.12% | 0.67% | 0.02% | 5.93% |
| 38 | The Denver Foundation | community_foundation | 2,340 | $0.26bn | 15.85% / 13.24% | 9.19% / 7.66% | -1.5 | 0.05% | 0.14% | 1.42% | 5.95% |
| 39 | The San Diego Foundation | community_foundation | 2,149 | $0.22bn | 15.17% / 14.19% | 8.52% / 6.63% | -1.9 | 0.50% | 0.04% | 0.18% | 4.82% |
| 40 | Community Foundation | community_foundation | 1,563 | $0.23bn | 22.46% / 14.33% | 7.17% / 3.37% | -3.8 | 0.00% | 0.00% | 0.09% | 4.27% |
| 41 | Tulsa Community Foundation | community_foundation | 3,117 | $0.33bn | 35.23% / 27.47% | 14.24% / 12.94% | -1.3 | 0.09% | 0.15% | 0.09% | 5.85% |
| 42 | Seattle Foundation | community_foundation | 11,124 | $0.33bn | 8.93% / 16.51% | 5.02% / 9.19% | +4.2 | 2.65% | 0.74% | 0.49% | 4.79% |
| 43 | The Board Of Trustees Of The Leland | university_hospital | 685 | $0.15bn | 70.07% / 19.75% | 68.91% / 19.55% | -49.4 | 17.73% | 0.09% | 0.55% | 0.31% |
| 44 | Ucla Foundation | university_hospital | 125 | $0.86bn | 13.60% / 1.35% | 11.20% / 1.14% | -10.1 | 0.00% | 0.02% | 0.04% | 0.65% |
| 45 | The Minneapolis Foundation | community_foundation | 2,788 | $0.20bn | 22.09% / 15.42% | 10.62% / 7.03% | -3.6 | 0.85% | 0.65% | 0.68% | 2.29% |
| 46 | T Rowe Price Program For Charitable | national | 4,694 | $0.19bn | 24.63% / 16.24% | 3.96% / 3.14% | -0.8 | 0.02% | 0.11% | 0.43% | 1.90% |
| 47 | Thrivent Charitable Impact & Investing | faith | 4,692 | $0.15bn | 50.62% / 41.13% | 3.77% / 2.58% | -1.2 | 0.00% | 0.01% | 0.03% | 1.65% |
| 48 | The San Francisco Foundation | community_foundation | 3,187 | $0.36bn | 14.21% / 13.49% | 9.04% / 8.97% | -0.1 | 0.16% | 2.91% | 0.55% | 5.56% |
| 49 | Community Foundation Of Tampa Bay Inc | community_foundation | 1,055 | $0.06bn | 18.29% / 21.79% | 5.21% / 3.70% | -1.5 | 0.44% | 0.00% | 0.18% | 1.91% |
| 50 | Saint Paul & Minnesota Foundation | community_foundation | 2,803 | $0.29bn | 25.22% / 12.05% | 8.17% / 4.18% | -4.0 | 0.00% | 0.14% | 0.13% | 1.90% |


**Notes [C/I]:**
- **Greater Horizons (59.8% of dollars)** is driven by one FY2024 line with no name and no EIN ($212.2m). That line is an e-filed total: it equals the sum of the 3,282 named lines, and a second blank line holds the count. Without them Greater Horizons is 25.1% / 19.8% broad and 7.2% / 9.5% core (core gap +2.3 pp) [V wave 32A]
- **SVCF (45.8%)** is driven by the $1.309bn Further Future Foundation line (recent ruling) and the $1.66bn CZ Biohub LLC lines (raw not-in-Pub-78; labelled, so not core).
- **Thrivent (50.6% of lines)** and **NCF** are dominated by church and group-subordinate recipients that are absent from Pub 78. Their core shares are low (3.8% / 2.6% and 7.5% / 5.9%).
- **Columbus Foundation** (8.7% PF/ER, the Huntington Foundation lines) and **Community Foundation of New Jersey** (12.6% PF/ER) have the highest PF/ER dollar shares.
- **Jewish Community Foundation of Los Angeles** (16.1%) and **Marin CF** (16.4%) have the highest foreign dollar shares.

## 4. Comparison with the existing four-national exception share

**Existing measure** ([breadth-community-faith-infrastructure-emerging.md](breadth-community-faith-infrastructure-emerging.md) §6.2–6.4; quoted in report §4). FY ended 6/2025, from the sponsors' Forms 990 ([Fidelity Charitable](https://projects.propublica.org/nonprofits/organizations/110303001/202601389349301700/IRS990), [DAFgiving360](https://projects.propublica.org/nonprofits/organizations/311640316/202611199349300601/IRS990ScheduleF), [Vanguard Charitable](https://projects.propublica.org/nonprofits/organizations/232888152/202621329349306657/IRS990), [NPT](https://projects.propublica.org/nonprofits/organizations/237825575/202601289349302480/IRS990ScheduleF)).

**This proxy:** the same four sponsors, FY2023 + FY2024 (tax periods ending 6/2023 and 6/2024), from the e-file XML.

| Component | Existing (FY6/2025) | This proxy, same definition (FY2023–24) [C] | This proxy, full category [C] |
|---|---|---|---|
| Foreign: Part IX line 3 ÷ lines 1–3 | 1.46% | **1.96%** (line 3 $976.1m of $49.90bn) | Foreign incl. Sched I foreign-address lines: 2.00% of $, 0.43% of lines |
| Named fiscal sponsors ÷ Schedule I $ | ≈1.20% | **1.50%** (same 19-host list) | 1.47% of $, 0.04% of lines |
| Non-501(c)(3) IRC-section text ÷ Schedule I $ | ≈0.03% | **0.15%** (NPT 0.78%; the others 0.00%) | Not c3 / not in Pub 78: 8.20% of $, 22.61% of lines (unexplained 0.98% / 2.33%) |
| Recent ruling (≤24 months) | not measured | — | 4.25% of $, 4.91% of lines |
| Private foundations / ER | not measured | — | 2.05% of $, 0.41% of lines (ER-required $61.0m; POF $948.6m) |
| **Sum / union** | **≈2.5–3%** of $ | **≈3.6%** of $ (simple sum, as in the existing method) | **Core 10.0% of $, 7.3% of lines; broad 17.8% of $, 28.3% of lines** |
| Count-based | "roughly 0.3–1%" [I]; NPT floor ≥0.35% | Foreign + fiscal-sponsor lines: 0.47% of big-4 lines | — |

**Per sponsor, FY2023–24 [C]:**

| Sponsor | Line 3 share | Named FS share of Sched I | Core: count / $ | Broad: count / $ |
|---|---|---|---|---|
| Fidelity Charitable | 0.50% (FY6/2025: 0.48%) | 1.79% (1.27%) | 7.55% / 8.32% | 30.20% / 16.78% |
| NPT | 7.42% (4.84%) | 2.21% (1.70%) | 9.55% / 15.75% | 22.70% / 20.69% |
| DAFgiving360 | 0.93% (1.23%) | 0.88% (1.05%) | 6.93% / 9.56% | 28.88% / 18.99% |
| Vanguard Charitable | 0.21% (0.12%) | 0.30% (0.45%) | 5.68% / 7.34% | 24.54% / 14.17% |

**Reading [I]**
1. **On its own definition, the existing figure holds up.** FY2023–24 gives about 3.6% against "2.5–3%". The difference is mostly NPT's foreign dollars ($742.8m over the two years, 7.4% of its grants, against 4.84% in FY6/2025), plus slightly higher fiscal-sponsor shares at Fidelity and NPT.
2. **On the briefed categories, it covers only about a third of the core dollar proxy** (3.6% of 10.0%). The categories it omits are:
   - **operating foundations:** $948.6m at the big four, 1.93% of their dollars, most of it a few large lines. DAFgiving360 alone has $446.4m, 3.9% of its dollars;
   - **recipients ruled within 24 months:** 4.25%;
   - **unexplained non-list recipients:** 0.98%.
3. **The count-side claim needs a qualifier.** "Count-weighted it is far smaller" (0.3–1%) is right for foreign and fiscal-sponsor grants (0.47% of lines). It is wrong for the full proxy:
   - new-ruling recipients are 4.9% of lines;
   - recipients absent from Pub 78 are 22.6% of lines (mostly churches and subordinates, clearable from the BMF or group rulings).
   - At the big four, flagged lines average $91,936 against $166,950 for the rest (broad).

## 5. Limits

- **A proxy for review need, not observed review.**
  - No sponsor publishes how it routes grants, how many exceptions it handles or how long review takes. This is still the gap (Q-N03).
  - A flagged line may be cleared by a standing rule. Examples: churches; subordinates of a known group ruling; government units; repeat grants to a known POF or fiscal sponsor.
  - An unflagged line may still be reviewed, for example for purpose restrictions, benefit or pledge flags, donor-advisor control, or SPLC-type holds.
- **Schedule I is a recipient-level list, not a grant-level list.**
  - It itemises each recipient once per return, and only above $5,000.
  - The count denominator (608,612 recipient lines) is therefore far below the number of grants. For example, Fidelity Charitable's two returns hold 152,859 recipient lines in all (`sponsor` row). Its own 2025 Giving Report records **2,664,446 grants in calendar 2024 alone** ([Fidelity Charitable 2025 Giving Report](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf), quoted via repo [daf-grant-exception-unit-economics-evidence-and-sensitivity-2026-11-12.md](../daf-grant-exception-unit-economics-evidence-and-sensitivity-2026-11-12.md)).
  - The count shares here are shares of **recipient-years**. Per-grant shares are probably lower for categories with large average grants (foreign, fiscal sponsors, PFs) and higher for small retail recipients. P-G05-02 proposes the reconciliation.
- **Snapshots, not as-of status.**
  - Pub 78 (2026-11-11) and the BMF (2026-11-09) describe today.
  - A recipient absent today may have been listed at grant time, and a ruling month may have been reset by reinstatement or re-determination. The 4,090 lines whose ruling postdates the grant year are kept out of `any_core` for this reason.
  - Organisations ruled within the window but later dissolved are missed.
- **Name rules are inference.**
  - Fiscal-sponsor matching uses a fixed 19-host list. Smaller hosts and sponsored projects listed under their own names are missed.
  - The explaining labels are those of P-NEW-REC-01, with its known false positives and negatives (e.g. Ahavas Zion is unlabelled).
- **Schedule F counts** are recipients (line 2) for 61 sponsor-years. They are Part II region rows for 3. Two sponsor-years have dollars but no count. Part II dollars are not split between "501(c)(3)-equivalent" and "other" recipients, so ER-likely foreign dollars cannot be isolated. The 680 "other organisation" foreign recipients are given as a count only (`sched_f_other_org_cnt`; 539 of them at SVCF).
- **Community-foundation Schedule I includes non-DAF grants** (discretionary, field-of-interest), so CF figures describe the whole grant book, not only DAF grants.
- **Missing inputs:**
  - BofA Charitable Gift Fund (rank 11) and Renaissance (rank 9) file Schedule I only as an attachment, so no recipient lines exist in e-file for FY2023–24;
  - Greater Horizons and Greater Kansas City CF lack FY2023;
  - the revocation list was not re-applied (not a briefed category; see P-NEW-REC-01: $74.8m, 0.082% of dollars);
  - grant dates and ED/ER determinations at grant time are not public.

## 6. Reproduction

```
python3 scripts/mission_exception_load.py . --np-cache NPCACHE --lines-cache LINES --bmf-dir BMF \
    --pub78 data-download-pub78.txt [--out PATH]
```
- NPCACHE holds `netpayout990/`. LINES is the P-NEW-REC-01 Schedule I line cache. BMF holds eo1–eo4, eo_pr and eo_xx. The Pub 78 file is the unzipped `data-download-pub78.zip`.
- The leading `.` is the repo-root positional (accepted for the repo's CLI convention; unused).
- The script writes the CSV and prints a JSON summary with:
  - every scope row;
  - the label mix of the raw not-in-Pub-78 pool;
  - the top recipients per category;
  - the Schedule F count-basis mix;
  - the missing and attachment-only sponsor-years.
- Run time is about 40 s.
- Every figure in this note comes from that CSV or summary, except where a row is marked as quoted from another repo file.

## 7. Data dictionary: `exception-load-proxy-2026-11-19.csv`

| Column | Meaning |
|---|---|
| row_type | One of:<br>- `sponsor_year`: one return;<br>- `sponsor`: FY2023–24 pooled, itemised years only;<br>- `sponsor_type`;<br>- `dafrc_segment`;<br>- `all` (`all_top50_itemising`, `all_ex_university_hospital`, `all_ex_university_hospital_ex_svcf`);<br>- `big4_nationals` (Fidelity, DAFgiving360, Vanguard, NPT);<br>- `all_fy`, `big4_fy`: single-year versions. |
| scope | Sponsor name (DAFRC panel) or scope label |
| ein, dafrc_segment, sponsor_type, rank_fy2024 | Sponsor EIN; DAFRC segment; sponsor type (§1.6: `faith`, `single_issue_other`, else the segment); DAFRC FY2024 DAF-asset rank. Blank for multi-sponsor scopes, except `sponsor_type` on `sponsor_type` rows |
| fiscal_year, sponsor_years, n_sponsors | DAFRC fiscal year(s) covered; sponsor-years and sponsors in the cell |
| object_id, tax_period_end | `sponsor_year` only: e-file object id and tax-period end of the return used |
| sched_i_status | `itemised`, or `attachment_only` (no recipient lines in e-file; proxy fields left blank) |
| sched_f_count_basis | `sponsor_year` only: how foreign recipients were counted:<br>- `line2_counts`;<br>- `part2_rows_fallback`;<br>- `+part3` (Part III recipients added);<br>- `none` (no foreign grants);<br>- `no_count` (line 3 dollars but no Schedule F count). |
| sched_i_lines, sched_i_usd | Schedule I Part II lines; their cash + non-cash dollars |
| sched_f_foreign_recipients, sched_f_foreign_usd | Schedule F foreign recipient count (per `sched_f_count_basis`); Form 990 Part IX line 3 |
| part_ix_total_grants_usd | Part IX lines 1–3 (from the Schedule F dataset) |
| denom_lines, denom_usd | Proxy denominators: `sched_i_lines + sched_f_foreign_recipients`; `sched_i_usd + sched_f_foreign_usd` |
| {cat}_lines, {cat}_usd, {cat}_count_share, {cat}_usd_share | For cat in `foreign`, `not_c3_or_not_pub78`, `not_c3_or_not_pub78_unexplained`, `recent_ruling_24m`, `fiscal_sponsor_name`, `pf_or_er`, `any`, `any_core` (definitions in §1.4). Shares are on the denominators. `foreign`, `any` and `any_core` include the Schedule F recipients and dollars |
| any_gap_pp, any_core_gap_pp | (dollar share − count share) × 100 for the broad and core unions |
| any_usd_to_count_ratio | Broad dollar share ÷ broad count share |
| avg_usd_flagged_line, avg_usd_other_line | Mean dollars per broad-flagged line and per other line (Schedule F recipients count as lines) |
| any_count_share_ex_d2d, any_usd_share_ex_d2d | Broad shares with DAF-to-DAF lines (batch-34 whitelist) removed from numerator and denominator |
| sched_i_foreign_address_usd | Schedule I dollars on foreign-flagged lines (double-count check against line 3) |
| l3_foreign_share_of_total_grants | Part IX line 3 ÷ lines 1–3 (the existing measure's foreign definition) |
| fiscal_sponsor_listed_share_of_sched_i_usd, fiscal_sponsor_any_share_of_sched_i_usd | Named-list fiscal-sponsor dollars, and list + generic markers, ÷ Schedule I dollars (the existing measure's definition) |
| irc_text_not_c3_share_of_sched_i_usd | Schedule I dollars whose filed IRC-section text is non-blank and not 501(c)(3), ÷ Schedule I dollars (the existing measure's definition) |
| recent_ruling_after_period_end_lines, _usd | Recent-ruling lines whose BMF ruling month is after the grant year |
| d2d_usd | DAF-to-DAF dollars in the base |
| sched_f_other_org_cnt | Schedule F Part II line 2 "other organisations" count (ER-likely foreign recipients) |
| er_required_lines, er_required_usd, pof_only_lines, pof_only_usd | Split of `pf_or_er`: ER-required (PF/SONFI, BMF 04/24) and operating-foundation-only |
| sponsor_any_{usd_share,count_share,gap_pp}_{min,p25,median,p75,max} | Group rows only: distribution of sponsor-level pooled broad shares across the sponsors in the group (inclusive quartiles) |
| source | Provenance string |

## 8. Source register

| ID | Source | Version / access | robots.txt |
|---|---|---|---|
| S1 | Form 990 Schedule I Part II lines, top-50 FY2023–24: IRS e-file XML ([IRS Form 990 series downloads](https://www.irs.gov/charities-non-profits/form-990-series-downloads)), read from the GivingTuesday mirror of IRS TEOS (`https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{object_id}_public.xml`); line cache of P-NEW-REC-01 | 94 returns; object ids in the CSV `sponsor_year` rows | mirror robots.txt 404 (no rules), per P-NEW-FGN-01 |
| S2 | Form 990 Part IX line 3 and Schedule F Part II line 2 / Part III: same returns, via [`daf-foreign-grants-schedule-f-2023-2024.csv`](../../data/mission-2026-11-14/daf-foreign-grants-schedule-f-2023-2024.csv) (P-NEW-FGN-01) | 100 sponsor-years | as S1 |
| S3 | [IRS Pub 78 data](https://apps.irs.gov/pub/epostcard/data-download-pub78.zip) | Last-Modified 2026-11-11 (verified in P-NEW-REC-01) | apps.irs.gov robots.txt → 404 (no rules) |
| S4 | [IRS EO BMF extract](https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf): [eo1.csv](https://www.irs.gov/pub/irs-soi/eo1.csv)–eo4, eo_pr, eo_xx | Last-Modified 2026-11-09 (eo1.hdr) | `/pub/` and this page not disallowed (re-read 2026-11-19) |
| S5 | [IRS EO BMF field guide (eo-info.pdf)](https://www.irs.gov/pub/foia/ig/tege/eo-info.pdf): RULING, AFFILIATION and FOUNDATION codes (02/03 operating foundation; 04 non-operating; 10 church; 17, 21–24 supporting organisations) | fetched 2026-11-19 | not disallowed |
| S6 | [About Schedule I (Form 990)](https://www.irs.gov/forms-pubs/about-schedule-i-form-990); [About Schedule F (Form 990)](https://www.irs.gov/forms-pubs/about-schedule-f-form-990) | HTTP 200, 2026-11-19 | `/forms-pubs/about-*` not disallowed (only `/forms-pubs-*-search`) |
| S7 | [26 U.S.C. §4966](https://www.law.cornell.edu/uscode/text/26/4966); [§4945](https://www.law.cornell.edu/uscode/text/26/4945); [§170](https://www.law.cornell.edu/uscode/text/26/170) (b)(1)(A)(vii), (F) | statute | LII robots: crawl-delay 10; `/uscode/` not disallowed |
| S8 | [Rev. Proc. 2018-32](https://www.irs.gov/irb/2018-23_IRB) (reliance on Pub 78 / BMF), via [queue-batch30-legal-circulars.md](queue-batch30-legal-circulars.md) §3 | — | — |
| S9 | Existing four-national measure: [breadth-community-faith-infrastructure-emerging.md](breadth-community-faith-infrastructure-emerging.md) §6, from Forms 990 FY6/2025 of [Fidelity Charitable](https://projects.propublica.org/nonprofits/organizations/110303001/202601389349301700/IRS990), [DAFgiving360](https://projects.propublica.org/nonprofits/organizations/311640316/202611199349300601/IRS990ScheduleF), [Vanguard Charitable](https://projects.propublica.org/nonprofits/organizations/232888152/202621329349306657/IRS990) and [NPT](https://projects.propublica.org/nonprofits/organizations/237825575/202601289349302480/IRS990ScheduleF) | quoted, not re-fetched | (as in that file) |
| S10 | [Fidelity Charitable 2025 Giving Report](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf) (2,664,446 grants in 2024), via [daf-grant-exception-unit-economics-evidence-and-sensitivity-2026-11-12.md](../daf-grant-exception-unit-economics-evidence-and-sensitivity-2026-11-12.md) | quoted, not re-fetched | — |
| S11 | Repo: DAFRC panel `dafrc-sponsor-schedule-d-fy2019-2024.csv` (universe, rank, segment); `daf-to-daf-recipient-whitelist.csv` (DAF-to-DAF flag); [direction-recipient-compliance-screen.md](direction-recipient-compliance-screen.md) (labels, revocation results) | repo | n/a |

## Regeneration note (after validation wave 32A) — governing

`scripts/mission_exception_load.py` now drops Schedule I lines with no name and no EIN whose amount equals the sum of the return's named lines, or the number of named lines (`drop_totals_rows`). Only Greater Horizons' FY2024 return has such lines (two: the $212.2m totals row and the 3,282 line count). The CSV was regenerated. It holds 167 rows, and the 8 rows touching Greater Horizons, National or the pooled scopes changed. For all top-50 itemising sponsors the CSV now gives:

| Measure | Value |
|---|---|
| Recipient lines | 608,610 |
| Grant dollars | $92.72bn |
| Broad share (lines / dollars) | 25.08% / 19.72% |
| Core share (lines / dollars) | 7.41% / 10.96% |

These figures match the wave 32A corrections above. The National sponsor-type row was not changed by this regeneration. Its de-duplicated values (Servant Foundation removed) are the ones in the wave 32A correction to §3.2 [V wave 32A].
