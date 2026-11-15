# Direction P-NEW-REC-01: screening top-50 sponsors' Schedule I grant recipients against IRS revocation, Pub 78 and BMF data

**Date:** 2026-11-15 · **Queue item:** P-NEW-REC-01 (new direction from the owner)

**Outputs**
- [`data/mission-2026-11-14/recipient-compliance-screen-top50.csv`](../../data/mission-2026-11-14/recipient-compliance-screen-top50.csv): 5,296 rows. There are 1,584 `aggregate` rows (scope × FY × flag) and 3,712 `hit` rows (one per Schedule I line). The hit rows hold no personal data: recipients are organisations with EINs, and blank-EIN lines appear only in the aggregates.
- [`data/mission-2026-11-14/queue-proposals-batch41-n17.csv`](../../data/mission-2026-11-14/queue-proposals-batch41-n17.csv): P-B41N17-01..03.
- **Script:** [`scripts/mission_recipient_compliance.py`](../../scripts/mission_recipient_compliance.py) (stdlib, functional style). It reuses `mission_recipient_sectors.py`'s universe, its line cache and its DAF-to-DAF flag (`annotate`).

**Rules applied**
- **Read first:**
  - [direction-recipients-impact-matching.md](direction-recipients-impact-matching.md), including its wave-24A governing corrections. Neither correction touches the Schedule I lines used here.
  - [queue-batch30-legal-circulars.md](queue-batch30-legal-circulars.md) §3, with its wave-15 corrections (California sections only). The relevant point is that a grantor's reliance on IRS data is governed by **Rev. Proc. 2018-32 §8.01** (Pub 78 / EO BMF data, including from third parties such as Candid Charity Check).
- **Recency:** every grant line comes from a tax year ending 2023-03-31 to 2024-12-31 (DAFRC FY2023–FY2024, i.e. TY2022–TY2024 returns). Older revocation dates are used only to tell whether a revocation was in effect during those years.
- **Data sources:** only public IRS bulk data from irs.gov download paths, and robots.txt was read first:
  - `www.irs.gov/robots.txt` was read on 2026-11-15. It does not disallow `/pub/`.
  - `apps.irs.gov/robots.txt` redirects to a 404 page, so it sets no rules.
  - Local copies were used only after a HEAD request confirmed the same Content-Length and Last-Modified (§5).
- **No outreach and no logins.**
- **Labels:** **[F]** filed or IRS-published value; **[C]** script computation; **[I]** inference (name rules, possible explanations).
- **Framing.** Every flag is a **screening hit that needs review**. None of them says a grant was improper. Churches, governmental units, group-ruling subordinates and foreign grantees can legitimately be missing from Pub 78 or the BMF, and they are labelled. This is research, not legal or tax advice.

---

## 0. Answers in brief

The universe is 94 itemising sponsor-years (46 top-50 sponsors plus Stanford and UCLA Foundation): 604,915 Schedule I Part II lines, **$91.02bn**, 171,367 valid recipient EINs [F/C].

| Question | Answer [C] |
|---|---|
| **(a) Grants to EINs on the Auto-Revocation List, with revocation in effect before or during the grant year** | **1,837 lines, $74.8m, 1,163 EINs: 0.082% of dollars.**<br>- Revoked before the year and not reinstated (per the list) by year-end: 1,316 lines, $54.4m.<br>- Revoked during the year: 477 lines, $19.2m. The grant may predate the revocation date.<br>- Revoked before, reinstated during: 44 lines, $1.1m.<br>- **85% of the dollars ($63.6m) were posted by the IRS before the sponsor's year-end.** |
| … of which the recipient is **back in Pub 78 or the BMF today** | $53.1m (1,269 lines). The list's reinstatement column is blank for most, but the BMF shows a newer ruling. $44.8m have a ruling month on or after the revocation; $4.4m (136 lines) have a ruling dated after the sponsor's year-end, so the reinstatement's effective date needs checking. |
| … of which **not in Pub 78 or the BMF today** | **568 lines, $21.6m, 426 EINs (0.024%)**. Of these, posted by year-end and with no church, government, foreign or subordinate label: **274 lines, $10.5m.** This is the core review list. |
| **(b, c) EINs absent from Pub 78** (2026-11 snapshot) | **112,345 lines, $8.01bn (8.8%).**<br>- **In the BMF but not in Pub 78: $3.65bn.** All but $14.5m carry the group-subordinate label (BMF affiliation 9 or a group code); church foundation code 10 alone is $2.17bn.<br>- **In neither Pub 78 nor the BMF: $4.36bn (4.8%), 22,268 EINs.** |
| … absent from both: explained or not | Labelled share, by label:<br>- CZ Biohub/Institute LLCs (possible disregarded entities) **$1.68bn**;<br>- church/religious **$1.19bn** (plus $0.12bn also matching another EIN by name);<br>- government **$0.34bn**;<br>- possible public university **$0.19bn**.<br>**Unexplained: $0.82bn (0.90%), 6,338 EINs**, including $0.05bn whose name matches one Pub 78 entry under a different EIN (likely EIN error). |
| **Other screens** | **Blank or placeholder EIN:** 5,013 lines, $0.64bn.<br>**BMF non-501(c)(3) or not deductible** (mostly 501(c)(4)s and some 501(c)(6)s at community foundations): 398 lines, $29.6m.<br>**Private non-operating foundation or non-functionally-integrated Type III supporting organisation** (Pub 78 PF/SONFI, which need expenditure responsibility under §4966/§4945): 302 lines, **$81.7m**, $67.2m of it at community foundations. |
| **By sponsor type** (share of each segment's Schedule I dollars) | **Revocation hits:**<br>- national 0.074% ($46.7m);<br>- community foundations **0.112%** ($20.4m);<br>- single-issue 0.094% ($7.7m);<br>- processors and university sponsors 0.<br>**Absent-both, unexplained:**<br>- national 0.97% ($611m);<br>- CF 0.87% ($159m);<br>- single-issue 0.54% ($44m). |

**Reading [I]**
- On IRS public data, DAF sponsors' grants to revoked charities are **small: under 0.1% of dollars, and about 0.02% once later re-recognition is netted out**.
- The large "absent" pools are mostly organisations that the IRS lists legitimately leave out: subordinates under group rulings, churches, governmental units and disregarded LLCs.
- The open items are about $0.8bn of grants to EINs found in neither list with no label, plus $0.64bn of lines with a blank EIN. Both are most consistent with EIN reporting errors (§2.4).
- **Reliance under Rev. Proc. 2018-32 turns on what the IRS had published.** Most revocation hits were posted before the sponsor's year-end, so the date of each grant matters, and so does the sponsor's check log at grant time. Neither is visible in Schedule I.

---

## 1. Method

1. **Universe and lines.**
   - These are exactly those of [mission_recipient_sectors.py](../../scripts/mission_recipient_sectors.py): the top-50 DAFRC sponsors by FY2024 DAF assets, with one return per sponsor and fiscal year chosen by `mission_daf_to_daf.pick_returns`.
   - All 94 itemising sponsor-years are included. BofA CGF, Renaissance, Greater Horizons FY2023 and Greater Kansas City CF FY2023 file Schedule I as attachments only, so they are absent.
   - Every Schedule I Part II `RecipientTable` line was read from the cached line JSON. Each cache file was verified against the return's line count when built.
   - The DAF-to-DAF flag is kept. All figures are on all lines, and the CSV also gives `amount_usd_ex_d2d`. Revocation hits contain no DAF-to-DAF lines.
2. **Grant year.**
   - The grant year is the sponsor return's tax period: end = `tax_period_end`, start = end − 1 year + 1 day.
   - Schedule I gives no grant dates, so a line is "in" the year without a day.
3. **(a) Auto-Revocation List** ([data-download-revocation.zip](https://apps.irs.gov/pub/epostcard/data-download-revocation.zip), 1,248,287 records) [F].
   - **Record choice:** for each line, the script takes the latest record with revocation date ≤ period end.
   - **Status codes:**
     - `rev_before_not_reinstated`: revoked before the period start, with no list reinstatement by period end.
     - `rev_before_reinstated_in`: revoked before the start, reinstated during the period.
     - `rev_during`: revocation date inside the period, not retroactively reinstated.
     - Context only: `rev_reinstated_before` (reinstated on or before the start, or retroactively, i.e. reinstatement date = revocation date) and `rev_after` (first revocation after the year).
   - **Re-recognition fields.** The list's reinstatement column is blank for most re-exempted organisations. Each hit therefore also records:
     - whether the EIN is in Pub 78 or the BMF today;
     - the BMF ruling month;
     - whether that ruling postdates the sponsor's year-end.
   - **Posting.** `rev_posted_by_period_end` compares the IRS posting date with the period end.
4. **(b) Pub 78 data** ([data-download-pub78.zip](https://apps.irs.gov/pub/epostcard/data-download-pub78.zip), 1,437,291 records) [F].
   - Fields used: presence and deductibility codes (PC, PF, POF, SO, SONFI, SOUNK, EO, GROUP, FORGN, etc.).
   - **Name check.** For EINs missing from Pub 78, the normalised Schedule I name is matched against all Pub 78 names. Exactly one hit under another EIN gives the label `possible_ein_misreport`.
5. **(c) EO BMF** (eo1–eo4, eo_pr, eo_xx; [IRS SOI](https://www.irs.gov/pub/irs-soi/eo1.csv)) [F]. Fields used: SUBSECTION, DEDUCTIBILITY, FOUNDATION, STATUS, AFFILIATION, GROUP, RULING.
6. **Exception labels** (several can apply; the name rules are [I]):

   | Label | Rule |
   |---|---|
   | `government` | Sponsor's IRC text contains GOV, 170(c)(1), "public school" and similar; or a governmental name (CITY OF, SCHOOL DISTRICT, BOARD OF REGENTS, tribal names, and others) |
   | `church_or_religious` | BMF FOUNDATION 10; sponsor's IRC text "religious" or 170(b)(1)(A)(i); or a congregation, religious-order or yeshiva name |
   | `foreign` | Foreign address on the line, or a non-US Pub 78 country |
   | `group_subordinate` | BMF AFFILIATION 9, or a group code that is not a central organisation |
   | `possible_public_university` | Only for EINs absent from both lists: UNIVERSITY, COLLEGE, CURATORS or REGENTS in the name |
   | `llc_possible_disregarded_entity` | Only for EINs absent from both lists: "LLC" in the name |
   | `possible_ein_misreport`, `name_differs` | Context only. `name_differs` means less than one-third token overlap with the IRS name, i.e. a possible name change or wrong EIN |

   A hit is **"unexplained"** when it has none of the first six labels.
7. **Placeholder EINs** (999999999, 123456789 and similar) are treated as blank. The revocation file contains a 999999999 test record that would otherwise match.
8. **Hit list policy.**
   - Every revocation, PF/SONFI and non-501(c)(3) hit with an EIN is listed.
   - An absence hit is listed only when it is unexplained and the line is ≥ $100,000 (`--hit-min`).
   - All absence lines are in the aggregates.

## 2. Results

### 2.1 Pooled, FY2023–2024 [C]
| Flag | Lines | $ | EINs | % of $91.02bn |
|---|---|---|---|---|
| Revocation in effect before or during grant year | 1,837 | 74,756,533 | 1,163 | 0.082% |
| … revoked before, not reinstated by year-end (list) | 1,316 | 54,438,556 | 772 | 0.060% |
| … revoked during year | 477 | 19,236,011 | 394 | 0.021% |
| … revoked before, reinstated during year | 44 | 1,081,966 | 37 | 0.001% |
| … posted by sponsor's year-end | 1,533 | 63,624,183 | 936 | 0.070% |
| … in Pub 78/BMF today | 1,269 | 53,115,784 | 737 | 0.058% |
| … in Pub 78/BMF today, BMF ruling after sponsor's year-end | 136 | 4,423,249 | 107 | 0.005% |
| … **not in Pub 78/BMF today** | 568 | 21,640,749 | 426 | 0.024% |
| … not in lists today, posted by year-end, unexplained | 274 | 10,477,177 | 207 | 0.012% |
| Context: revoked but reinstated before the year | 10,235 | 870,790,959 | 4,920 | 0.957% |
| Context: first revoked after the year | 2,601 | 123,182,554 | 1,650 | 0.135% |
| EIN absent from Pub 78 (any) | 112,345 | 8,013,036,257 | 42,131 | 8.80% |
| … in BMF, not Pub 78 | 61,969 | 3,649,597,540 | 19,863 | 4.01% |
| … in BMF, not Pub 78, unexplained | 181 | 14,521,283 | 107 | 0.016% |
| … absent from Pub 78 and BMF | 50,376 | 4,363,438,717 | 22,268 | 4.79% |
| … absent from both, unexplained | 12,265 | 818,725,018 | 6,338 | 0.90% |
| … absent from both, unexplained, never revoked | 9,991 | 721,161,787 | 4,846 | 0.79% |
| Blank or placeholder EIN | 5,013 | 643,991,900 | — | 0.71% |
| BMF not 501(c)(3) or not deductible | 398 | 29,572,339 | 186 | 0.032% |
| Pub 78 PF or SONFI recipient | 302 | 81,749,628 | 201 | 0.090% |

**By year:**
- Revocation hits: FY2023 $32.2m (0.078%); FY2024 $42.5m (0.086%).
- Absent from both: FY2023 $2.98bn (7.2%, which includes the CZ LLC lines); FY2024 $1.38bn (2.8%).

**How the $74.8m of revocation hits divides** [C]:
- back in the lists with a BMF ruling month on or after the revocation: $44.8m;
- back in the lists but with an older ruling month: $8.4m. This is consistent with retroactive reinstatement or with a stale list record, but is unresolved;
- not in the lists: $21.6m.

### 2.2 By sponsor type, FY2023–2024 [C]
| Segment (sponsor-years) | Schedule I $ | Revocation hits $ (%) | … not in lists today $ | Absent Pub 78 (any) $ (%) | Absent both $ (%) | Absent both, unexplained $ (%) | Blank EIN $ | PF/SONFI $ |
|---|---|---|---|---|---|---|---|---|
| National (31) | 62.76bn | 46.7m (0.074%) | 14.2m | 4.96bn (7.9%) | 2.15bn (3.4%) | 611m (0.97%) | 362m | 11.4m |
| Community foundation (43) | 18.21bn | 20.4m (**0.112%**) | 5.5m | 2.38bn (13.1%) | 2.05bn (11.3%) | 159m (0.87%) | 137m | **67.2m** |
| Single-issue (14) | 8.18bn | 7.7m (0.094%) | 1.9m | 0.66bn (8.1%) | 0.16bn (1.9%) | 44m (0.54%) | 144m | 3.0m |
| Processor (2) | 0.89bn | 0 | 0 | 0.08m | 0.08m | 0.08m | 0 | 0 |
| University/hospital (4) | 0.98bn | 0 | 0 | 7.2m | 5.0m | 4.9m | 0 | 0.3m |

**Notes on the segments:**
- **Community-foundation absent-both** is dominated by SVCF's four CZ Biohub/Institute LLC lines ($1.66bn, FY2023).
- **CF PF/SONFI dollars** are driven by Columbus Foundation's lines to the Huntington Foundation ($43.6m) and Huntington-Akron Foundation ($4.0m), both Pub 78 code PF. Community foundations also make non-DAF grants (field-of-interest, discretionary), so some of these lines may not be DAF grants at all.
- **Revocation dollars by sponsor:**
  - Fidelity Charitable $14.2m (555 lines, 0.063% of its Schedule I);
  - NPT $8.8m;
  - DAFgiving360 (Donor Advised Charitable Giving) $6.5m;
  - NCF $5.3m;
  - Tulsa CF $4.3m (1.30% of its Schedule I, the highest share);
  - Servant Foundation $3.2m (0.22%);
  - Vanguard Charitable $3.2m.
  
  Per-sponsor rows are in the CSV (`scope_type = sponsor`).

### 2.3 Labels on the absent pools [C/I]
| Pool | Largest label groups ($) |
|---|---|
| In BMF, not Pub 78 ($3.65bn) | church + group subordinate $2.15bn; group subordinate $0.76bn; group subordinate + possible EIN misreport $0.30bn; group subordinate + name differs $0.17bn; **no label $13.6m** |
| BMF codes (subsection/deductibility/foundation) for the same pool | 03/1/10 (church) $2.17bn; 03/1/15 $0.62bn; 03/1/11 (school) $0.30bn; 03/0/10 $0.16bn; 04/2/00 $9.7m; 06/2/00 $1.7m |
| Absent from both ($4.36bn) | LLC $1.68bn; church/religious $1.19bn; **no label $0.77bn**; government $0.34bn; possible public university $0.19bn; church + possible EIN misreport $0.12bn; possible EIN misreport $0.05bn |
| Revocation hits ($74.8m) | no label $65.9m; church/religious $4.6m; government $1.0m; name differs $0.9m; possible public university $0.8m |

**Churches on the revocation list.** Churches are not required to file a Form 990, so they are not subject to automatic revocation. A `church_or_religious` label on a revocation hit therefore points to a name-rule false positive, or to a separately incorporated affiliate that did have a filing duty (e.g. a "parish foundation").

### 2.4 Top cases with context (screening hits needing review) [F/C, context I]
**Revocation hits**

| Recipient (EIN) | Sponsor(s) | $ | IRS record | Context |
|---|---|---|---|---|
| Heal Our Land Inc. (45-1501504) | Servant Foundation | 3.00m | Revoked 2019-05-15, posted 2019-08-12, no list reinstatement | Now in Pub 78 as POF; BMF ruling 2021-02, before the grant year. **Re-recognised; the list reinstatement field is blank** |
| Still She Rises Inc. (83-0943819) | Combined Jewish Philanthropies; Tulsa CF | 2.92m | Revoked 2021-05-15 | Now PC; BMF ruling 2022-07. Re-recognised; whether the effective date covers the whole grant year is unknown |
| Advanced Learning Charter School (26-3762954) | NPT | 2.50m | Revoked 2010-11-15 | Now PC; ruling 2015-10. Re-recognised |
| St Patrick's Catholic Church of Elkhorn (84-4733847) | Greater Horizons | 1.51m | Revoked 2022-11-15, posted 2023-04-10; the list name is "Saint Patricks Parish Foundation" | **Not in Pub 78/BMF.** The revoked entity looks like a parish *foundation* that shares the EIN; the church itself may be covered by the diocesan group ruling. Possible wrong EIN [I] |
| The Collective the CLTV Inc (32-0460234) | ImpactAssets | 1.20m | Revoked 2024-11-15, during the CY2024 year; posted 2025-03-10, after year-end | Not in the lists. The grant may predate the revocation date |
| Firefly Academy Inc (82-3749390) | Foundation for the Carolinas | 1.00m | Revoked 2024-05-15 during the year; posted 2024-08-12 | Not in the lists |
| Institute for Therapeutic Discovery (20-0109928) | American Endowment Foundation | 0.90m | Revoked 2024-11-15; posted 2025-03-10 | Not in the lists |
| "Fidelity Charitable" (22-3332686) | Community Foundation of New Jersey | 0.89m | That EIN was revoked 2019-11-15 | **Almost certainly a wrong EIN on a DAF-to-DAF line.** Fidelity Charitable is 11-0303001. Because of the wrong EIN it escaped the DAF-to-DAF whitelist [I] |
| "3400888 Charles Schwab & Co" (90-1034720) | Fidelity, MS GIFT, US Charitable Gift Trust | 0.40m | Revoked 2023-05-15 | The recipient name is a brokerage account reference. A data-entry or grant-routing artefact [I] |
| Stamford Hospital Health Foundation (22-2478748) | AEF, DAFgiving360, Fidelity | 0.67m | Revoked 2024-02-15 during the year | Not in the lists. Possibly merged into the hospital or another EIN [I] |
| Shinnecock Indian Nation (35-2177466) | NY Community Trust | 0.24m | Revoked 2017 (record "Shinnecock Indian Nation Fund") | Labelled `government`. Tribal governments are §7871 governmental units, so the revoked entity is probably a fund affiliate [I] |
| Project 2049 Institute (26-1894546) | NPT | 0.23m | Revoked 2013, reinstated 2023-05-15 during the year; IRS name now "Institute for Indo-Pacific Security" | Reinstatement within the year, plus a **name change** |

**Absent from Pub 78 and the BMF**

| Recipient (EIN) | Sponsor(s) | $ | Label | Context [I] |
|---|---|---|---|---|
| CZ Institute for Advanced Biological Imaging; CZ Biohub SF / New York / Chicago LLCs | SVCF (FY2023) | 1,656.6m | `llc_possible_disregarded_entity` | Single-member LLCs are not separately listed by the IRS. Recognition is through the member organisation |
| Ahavas Zion (45-3809063) | Fidelity | 68.5m (2 lines) | none | Never revoked. The name suggests a congregation, which is not caught by the name rule |
| University of Texas at Austin (74-6000203) | 22 sponsors | 55.5m | government / public university | A state instrumentality. Gifts are deductible under §170(c)(1) |
| Bright Future Fund (93-4678619) | Fidelity | 37.5m | none | Never revoked. Possibly not yet recognised, or a wrong EIN |
| US Central and Southern Province, Society of Jesus (43-0416129) | 5 sponsors | 35.3m | church/religious | A religious order, likely covered by the Official Catholic Directory group ruling |
| Heartland Alliance for Human Needs & Human Rights (36-1877640) | 10 sponsors | 16.6m | none | A well-known charity, probably listed under another EIN. Possible EIN error |
| LA Clippers Foundation (95-4493310) | GS DAF | 15.5m | none | Possible EIN error |
| Tulsa's Gathering Place (90-0986936) | Tulsa CF | 13.4m | none | The sponsor's IRC text is 170(b)(1)(A); possibly a public trust or governmental conduit |
| Regis High School (13-1624155) | 10 sponsors | 11.6m | none | A Jesuit school, plausibly under the Catholic group ruling |
| UT Southwestern Medical Center (75-6002868) | 3 sponsors | 9.3m | none | A state institution, not caught by the name rule |
| Rosebud Economic Development Corp (46-0454387) | Fidelity, ImpactAssets | 8.4m | possible EIN misreport | A tribally chartered corporation |

**Expenditure-responsibility and non-501(c)(3) screens**
- **Columbus Foundation → Huntington Foundation** (31-1681542, Pub 78 PF): $43.6m.
- **SVCF → Breakthrough Prize in Life Sciences Foundation** (PF): $6.0m.
- **Community foundations → 501(c)(4)s:**
  - NPH Action Fund: SVCF and SFF, $2.37m;
  - Center for Empowered Politics, $1.14m;
  - Neighbors for Affordable Housing, $1.0m;
  - and others.
- These are lawful with expenditure responsibility and charitable-purpose restrictions. Whether a line is a DAF grant or a discretionary CF grant is not visible.
- **Ohio State University and the University of Wisconsin System Board of Regents** show BMF subsection 01 (government instrumentality). They are governmental, not a compliance concern.

## 3. Limitations
- **Snapshots, not as-of data.**
  - Pub 78 (2026-11-11) and the BMF (2026-11-09) show today's status. An organisation absent today may have been listed when the grant was made, if it later merged, dissolved or terminated.
  - The revocation list is the only dated source. The `rev_after` context row ($123m) shows how much absence that kind of drift can explain.
- **Reinstatement is under-recorded in the list.** Most re-recognised organisations have a blank reinstatement field. The BMF ruling month is a proxy, because a reinstatement can be retroactive to the revocation date (applications within 15 months; Rev. Proc. 2014-11). The $44.8m "back in lists" portion may therefore never have been a lapse at all.
- **No grant dates.** `rev_during` lines may predate the revocation, and revocations posted after year-end were not public at grant time. Reliance under Rev. Proc. 2018-32 depends on the check made at grant time, which is not visible.
- **Schedule I coverage:**
  - It lists only grants over $5,000 per recipient. That is about 98% of Part IX line 1 dollars, but many small grants are left out.
  - Part II covers domestic organisations only. **Foreign grants (Schedule F) were not screened**; foreign grantees are not expected in Pub 78 except under treaty (FORGN).
  - Attachment-only sponsors (BofA CGF, Renaissance and two CF-years) are absent.
- **Community-foundation Schedule I includes non-DAF grants.** The CF figures are an upper bound for DAF-grant hits.
- **Name rules are inference.**
  - They can mislabel in both directions. For example, Ahavas Zion is missed as a congregation, and the "TEMPLE" rule was hand-tuned to skip Temple University.
  - The `possible_ein_misreport` label needs an exact normalised-name match to exactly one Pub 78 entry, so it under-detects.
- **EIN reporting by sponsors** (typos, a parent's or a fund's EIN) is the most likely cause of many unexplained hits. It is not verified here.
- **Group rulings.** Whether a subordinate is actually covered is not checked against the central organisation's roster.

## 4. Data dictionary: `recipient-compliance-screen-top50.csv`
| Column | Meaning |
|---|---|
| record_type | `aggregate` (one row per scope × fiscal_year × flag) or `hit` (one Schedule I line) |
| scope, scope_type, segment | Aggregates: `all_top50_itemising` (all), a DAFRC segment (segment), or a sponsor's DAFRC name (sponsor; pooled 2023–2024 only). Hits: the sponsor's name and segment |
| fiscal_year | DAFRC FY `2023`, `2024` or `2023-2024` |
| flag | Aggregates: the flag name (see §2.1; `all_lines` is the scope total). Hits: `;`-joined flags among `revoked_in_or_before_grant_year`, `absent_pub78_and_bmf`, `absent_pub78_in_bmf`, `bmf_not_501c3_or_not_deductible`, `pf_or_sonfi_recipient` |
| lines, amount_usd, distinct_eins | Aggregates: count, dollars and distinct recipient EINs. Hits: amount_usd is the line's cash plus non-cash |
| share_of_scope_usd, amount_usd_ex_d2d, sponsor_years | Aggregates: share of the scope's Schedule I dollars; the same amount excluding DAF-to-DAF lines; sponsor-years in the cell |
| sponsor_ein, tax_period_end | Hits: the grantor and its return's tax-period end (the grant year ends then) |
| recipient_ein, recipient_name, recipient_state, sched_i_irc_section | Hits: as filed on Schedule I |
| exception_labels | Hits: `;`-joined labels from §1.6 |
| rev_status, revocation_date, revocation_posted, reinstatement_date, rev_posted_by_period_end | Hits: the revocation record used and its status (§1.3) |
| rev_hit_in_pub78_or_bmf_now, bmf_ruling, bmf_ruling_after_period_end | Hits: re-recognition evidence |
| in_pub78, pub78_codes, in_bmf, bmf_subsection, bmf_deductibility, bmf_foundation, bmf_status | Hits: IRS list fields (2026-11 snapshots) |
| irs_ref_name, pub78_alt_ein_same_name | Hits: the IRS name (Pub 78, else BMF, else revocation list), and the single Pub 78 EIN carrying the same normalised name |
| d2d_line | Hits: 1 if the line is DAF-to-DAF under the batch-34 whitelist |
| source | Provenance |

## 5. Sources and reproduction
| ID | Source | Version | Robots |
|---|---|---|---|
| S1 | Schedule I Part II lines: IRS e-file XML (GivingTuesday mirror of IRS TEOS), cached by `mission_recipient_sectors.py` | 94 returns | (as in that run) |
| S2 | [IRS Auto-Revocation List](https://apps.irs.gov/pub/epostcard/data-download-revocation.zip) | Last-Modified 2026-11-11 10:21:54 GMT, 47,626,003 bytes (local copy identical in size) | apps.irs.gov robots.txt → 404 (no rules) |
| S3 | [IRS Pub 78 data](https://apps.irs.gov/pub/epostcard/data-download-pub78.zip) | Last-Modified 2026-11-11 10:21:19 GMT, 30,306,480 bytes (identical) | same |
| S4 | [IRS EO BMF](https://www.irs.gov/pub/irs-soi/eo1.csv) eo1–eo4, eo_pr, eo_xx | Last-Modified 2026-11-09 | www.irs.gov: `/pub/` not disallowed |
| S5 | Repo: `daf-to-daf-recipient-whitelist.csv`, the DAFRC panel, the `netpayout990/` cache | repo | n/a |
| S6 | [Rev. Proc. 2018-32](https://www.irs.gov/irb/2018-23_IRB) (reliance), via [queue-batch30-legal-circulars.md](queue-batch30-legal-circulars.md) §3 | — | — |

```
python3 scripts/mission_recipient_compliance.py --np-cache NPCACHE --bmf-dir BMF --lines-cache LINES \
    --pub78 data-download-pub78.txt --revocation data-download-revocation.txt [--hit-min 100000]
```
- The arguments are those of `mission_recipient_sectors.py`, plus the two unzipped IRS text files.
- The script prints a JSON summary covering pooled, by-year and by-segment aggregates, the label mixes and the top cases. Every figure above comes from that summary or the CSV.
- Run time is about 70 s.
