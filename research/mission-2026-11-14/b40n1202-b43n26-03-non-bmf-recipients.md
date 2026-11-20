# Top-50 recipient EINs not in the November 2026 EO BMF: what they are (P-B40N1202-B43N26-03)

**Date:** 2026-11-20 · **Task ID:** b40n1202-b43n26-03 · **Builds on:** [b40n1202-b43n26-recipient-basis-and-rating-eligibility.md](b40n1202-b43n26-recipient-basis-and-rating-eligibility.md) §4.1 (`not_in_bmf`: 22,269 recipients, $4.18bn DAF-weighted) and §5 item 8

**Outputs**
- Script: [`scripts/mission_non_bmf_recipients.py`](../../scripts/mission_non_bmf_recipients.py). It is new. It imports `build_numerator`, `load_history`, `cn_filing_test` and `no_ein_lines` from `mission_recipient_basis_eligibility.py` (the script that produced the 22,269 figure) and modifies nothing. Its only network use is optional (`--fetch`): it reads the earliest and latest e-filed return headers per EIN from the GivingTuesday mirror of IRS TEOS XML.
- Data: [`data/mission-2026-11-14/non-bmf-recipients-2026-11-20.csv`](../../data/mission-2026-11-14/non-bmf-recipients-2026-11-20.csv). 22,323 rows: 54 `aggregate` and 22,269 `recipient`. The data dictionary is in §6.
- Queue proposals: [`data/mission-2026-11-14/queue-proposals-b40n1202-b43n26-03.csv`](../../data/mission-2026-11-14/queue-proposals-b40n1202-b43n26-03.csv) (6 rows).

Tags: [F] computed by the script · [P] quoted primary source · [I] inference or assumption.

## 0. Answer in brief

- **The universe reproduces exactly.** There are 22,269 recipient EINs and $4,175.4m DAF-weighted ($4,360.5m Schedule I), which is 5.64% of the $74.07bn top-50 total. 1,213 of them, holding $292.8m, pass CN's filing rules [F].
- **Most of these EINs appear in no IRS bulk file at all.** 18,928 of the 22,269 (85%) are absent from Pub 78, the revocation list, the 990-N e-Postcard file and the TEOS e-file index 2019–2026 [F].
  - 3 are in Pub 78;
  - 1,613 have a revocation row, and 1,441 of those have no reinstatement date;
  - 1,252 are in the e-Postcard file;
  - 2,271 are in the TEOS index (2,254 with a 990-series return).
- **Categories (first match wins, §1.4).** Dollars are DAF-weighted. Shares are of non-BMF dollars, then of all top-50 dollars [F]:

| Category | EINs | $m | Share of non-BMF $ | Share of top-50 $ |
|---|---|---|---|---|
| subsidiary or disregarded entity (LLC name; added category) | 59 | 1,610.7 | 38.6% | 2.17% |
| still unresolved | 16,205 | 1,543.4 | 37.0% | 2.08% |
| — of which religious-pattern name, no IRS trace | 14,647 | 1,313.0 | 31.4% | 1.77% |
| foreign or government | 2,542 | 631.1 | 15.1% | 0.85% |
| merged or terminated | 1,334 | 240.7 | 5.8% | 0.32% |
| revoked (automatic revocation, not reinstated) | 1,405 | 83.6 | 2.0% | 0.11% |
| invalid or typo EIN | 568 | 46.4 | 1.1% | 0.06% |
| new EIN | 156 | 19.5 | 0.5% | 0.03% |
| **Total** | **22,269** | **4,175.4** | 100% | 5.64% |

  - On the task's six-way split, the LLC category folds into unresolved: 16,264 EINs, $3,154.2m (75.5%).
  - Four Chan Zuckerberg LLCs hold $1,594.0m of the subsidiary bucket, almost all of it in FY2023 [F].
  - The subsidiary category's label (LLC, disregarded) rests on name rules [I].
- **Reconciling the 1,213 ($0.29bn) that pass CN's filing rules.** 884 of them ($220.4m, 75%) filed a final return or reported terminating or dissolving on their latest e-filed return. They had three or more recent returns because they were established organisations that then closed or merged.
  - The rest: 136 revoked ($15.5m), 15 new ($9.1m), 47 foreign or government ($4.1m), 2 LLC ($0.3m), 4 invalid ($0.06m) and 125 unresolved ($43.3m) [F].
  - So the "upper bound of about 77.3%" in the parent note §4.1 is too generous. At most about $43m of the $293m (0.06 points of top-50 dollars) looks like live organisations that CN might list [I].
- **Revoked at the time of the grant.** These are EINs in the revoked category whose automatic revocation took effect before the granting sponsor's fiscal year began. They received **$7.24m DAF-weighted across 141 EINs from 32 of the 50 sponsors** in FY2023–24. That is 0.010% of top-50 DAF-weighted dollars [F].
  - **$6.33m** ($7.01m Schedule I; 30 sponsors) went to EINs whose revocation the IRS had also posted publicly before that fiscal year began [F].
  - Of that $6.33m:
    - $1.87m went to names now listed in the BMF under another EIN (stale EIN; the money probably reached a recognised successor);
    - $0.68m went to government-unit names;
    - $1.23m went to EINs whose name matches only partly;
    - $2.55m went to EINs with a matching name and no BMF successor [F].
  - A further $11.30m (272 EINs) went to EINs revoked during the sponsor's fiscal year, so the grant may have come before or after the revocation.
  - $65.04m (1,092 EINs) went to EINs revoked only after the fiscal year ended [F].
  - Most revoked dollars therefore went to organisations that were exempt when paid and lost their status later. 866 of the 1,405 revoked EINs have 2025 or 2026 revocation dates [F].
  - **This is a public-data screen of sponsor due diligence, not evidence of improper grants.** Revocations can be reinstated retroactively (§3.6). Grant dates within the fiscal year are unknown. A grant to a revoked organisation can still serve a charitable purpose under a sponsor's expenditure-responsibility process.

## 1. Method

### 1.1 Universe and dollars

The universe is exactly the `not_in_bmf` units of `mission_recipient_basis_eligibility.py`, imported rather than re-derived:
- top-50 DAFRC sponsors by FY2024 DAF assets;
- FY2023–24 Schedule I Part II lines;
- totals rows dropped, DAF-to-DAF lines dropped, positive amounts, EIN present;
- EIN absent from all six BMF files (eo1–4, eo_pr, eo_xx; cached 2026-11-14).

`daf_weighted` multiplies each sponsor-year's lines by that sponsor's DAF share of grants. Each line also keeps the IRC-section text from Schedule I. The script re-reads it from the same cached line files, and an assertion checks that the lines align one to one. Each line also keeps the sponsor return's `tax_period_end`.

`name_as_filed` is the recipient name on the sponsor line carrying the most DAF-weighted dollars for that EIN.

### 1.2 Evidence joined per EIN (IRS bulk files only)

| Source | Fields used |
|---|---|
| Pub 78 data | Presence, name, deductibility code |
| Automatic revocation list | Name, DBA, revocation date, posting date, reinstatement date (latest row per EIN by posting date) |
| Form 990-N e-Postcard data | EIN, tax year, organisation name, "terminated" flag. Officer names and addresses are never read into memory. |
| TEOS e-file index 2019–2026 | Every return type (990-T included): tax periods and filer name |
| Return headers (earliest and latest e-filed 990/990-EZ/990-PF per EIN; 4,202 read, 59 not on the mirror) | `InitialReturnInd`, `FinalReturnInd`, `ApplicationPendingInd`, `NameChangeInd`, `TerminateOperationsInd` (990 Part IV line 31), `OrganizationDissolvedEtcInd` (990-EZ) |
| Full BMF (every row) | Name and state index for the wrong-EIN test |

### 1.3 Earlier BMF extracts

**Not obtainable from IRS bulk downloads.** The IRS EO BMF page (reviewed 16-Nov-2026) links only the current eo1–4 and state files, plus "SIT 2016/2017" CSVs, which are pre-2021 and outside the evidence rule. The TEOS bulk page offers only current Pub 78, revocation and e-Postcard files [P]. Final-return flags, e-Postcard termination flags and revocation dates stand in for a past snapshot. A dated snapshot is queued as P-B40N1202-B43N2603-05.

**Robots log (checked 2026-11-20):**
- www.irs.gov/robots.txt returned HTTP 200. It disallows search paths and `/charities-non-profits/tax-exempt-organization-search`; `/pub/` and the pages read here are not disallowed.
- apps.irs.gov/robots.txt returned 404 (the request redirected to www.irs.gov/404), so no rules apply.
- gt990datalake-rawdata.s3.amazonaws.com/robots.txt returned 404.

The user agent was `research-script/1.0`. sec.gov was not used.

### 1.4 Category rules (first match wins)

Name similarity (`name_sim`):
- Names are normalised: upper case, punctuation removed, stop-words such as INC, THE and OF dropped.
- The score is the larger of the `difflib` ratio and the token containment of the shorter name, where the shorter name has at least 2 tokens and covers at least 60% of the longer one.
- A pair whose differing tokens include an affiliate word (FOUNDATION, FRIENDS, ALUMNI, SCHOOL, TRUST, FUND, …) is capped at 0.7, so "X" and "X Foundation" never count as the same organisation.
- Thresholds: `NAME_OK` = 0.80, `NAME_BAD` = 0.45, `FUZZY_OK` = 0.90.

1. **revoked.** The EIN has a revocation row with no reinstatement date, and its name or DBA scores `name_sim` ≥ 0.45 against the filed name. Subs, in order:
   - `government_unit_name`;
   - `name_now_in_bmf_other_ein` (one same-state BMF EIN carries the name);
   - `no_bmf_successor` (≥ 0.80);
   - `name_partial_match` (0.45–0.80).
2. **invalid_or_typo (a).** A live revocation row under an unrelated name (< 0.45), for example a placeholder EIN 999999999 that the revocation list holds as "TEST COMPANY".
3. **foreign_or_government.**
   - The line address is foreign (no case was found: Schedule I Part II lines with an EIN are domestic).
   - Or the IRC-section text names a government, 170(c)(1) or 115.
   - Or a government-unit name rule matches: school district, public school by level, state university, local government, state, federal or tribal.
   - Failing those, a heuristic: a non-religious name whose EIN has digits 3–5 equal to "600". This is the pattern of the large public-university and school-district EINs seen here. No IRS source documents it, and about 4 of 20 sampled cases look non-governmental [I].
4. **subsidiary_or_disregarded.** An LLC or "limited liability" name. This category is added to the task's list because it holds 39% of the dollars.
5. **invalid_or_typo (b).** One of:
   - an EIN prefix the IRS does not assign (IRS valid-prefix table [P]);
   - IRS history under an unrelated name while the filed name is on a BMF EIN;
   - no IRS trace, and the filed name maps to exactly one BMF EIN, either one digit or one adjacent transposition away with `name_sim` ≥ 0.80 (`typo_`), or as the only same-state BMF EIN with the same normalised name or a fuzzy match ≥ 0.90 (`wrong_ein_`; still `typo_` if two or fewer digits differ).
   - Religious-pattern names qualify only through the neighbour test, because names like "First Presbyterian Church" recur within states.
6. **merged_or_terminated.** One of:
   - a final-return, terminate-operations or dissolved indicator on the latest e-filed return;
   - an e-Postcard "terminated" flag;
   - IRS history under the filed name (≥ 0.80) with that name now on a same-state BMF EIN.
7. **new_ein.** One of:
   - the first e-filed or e-Postcard tax period ends in 2022 or later;
   - an initial-return indicator on the earliest return;
   - an application-pending indicator.
8. **unresolved.** Everything else. Subs:
   - has IRS filings;
   - revoked then reinstated but still not in the BMF;
   - e-Postcard only or Pub 78 only;
   - religious-pattern name with no IRS trace;
   - name in the BMF but ambiguous or out of state;
   - other.

### 1.5 Revoked-at-grant timing

Each sponsor line is dated only to the sponsor's fiscal year, taken as the 12 months ending on its `tax_period_end`. Short years are not detected. The script compares two dates with that window:
- the revocation **effective** date, which the IRS sets at "the original filing due date of the third annual return or notice" [P];
- the **posting** date, when the revocation appeared on the public list.

Buckets: `before_fy_posted_before_fy`, `before_fy_posted_later`, `during_fy`, `after_fy`. Only the revoked category is timed. EINs in invalid_or_typo (a) are excluded because their revocation row belongs to another organisation.

### 1.6 Reproduction

```
S=<scratchpad>
python3 scripts/mission_non_bmf_recipients.py . --np-cache $S/npcache --lines-cache $S/rcp/lines --bmf-dir $S/rcp/bmf \
    --index-dir $S/irs --epostcard $S/nb03/epost/data-download-epostcard.txt --xml-cache $S/nb03/xmlhdr [--fetch] [--base-cache F]
```

- `--index-dir` holds `index_YYYY.csv`, `data-download-revocation.txt` and `data-download-pub78.txt`, as cached for the parent note.
- The run takes about 3.5 minutes with warm caches.
- A run with a fresh base and a run from the pickled base produce byte-identical CSVs.
- The script prints a JSON summary: evidence counts, header status, timing buckets, the largest EINs per category, and the CN-pass reconciliation.

## 2. Results by category

All figures are [F]. $m are DAF-weighted.

| Category / sub | EINs | $m | FY2023 $m | FY2024 $m |
|---|---|---|---|---|
| **subsidiary_or_disregarded** / llc_name | 59 | 1,610.7 | 1,603.2 | 7.6 |
| **unresolved** | 16,205 | 1,543.4 | 687.5 | 855.9 |
| · no IRS trace, religious-pattern name | 14,647 | 1,313.0 | | |
| · no IRS trace, other | 1,078 | 155.3 | | |
| · has IRS filings, no BMF row, no revocation or termination signal | 168 | 46.8 | | |
| · no IRS trace; name in BMF only in another state | 117 | 16.7 | | |
| · revoked then reinstated, still not in BMF | 106 | 6.8 | | |
| · no IRS trace; name ambiguous in state (exact 24, fuzzy 32) | 56 | 4.3 | | |
| · e-Postcard only / Pub 78 only | 32 / 1 | 0.6 / 0.04 | | |
| **foreign_or_government** | 2,542 | 631.1 | 354.1 | 277.0 |
| · IRC-section text says government / 170(c)(1) | 447 | 300.2 | | |
| · local-government name | 747 | 89.3 | | |
| · school-district name | 629 | 79.4 | | |
| · public school by level (elementary, high, …) | 354 | 77.0 | | |
| · state university / community college | 198 | 45.5 | | |
| · state, federal or tribal | 56 | 26.2 | | |
| · EIN "600" heuristic | 111 | 13.5 | | |
| · foreign address | 0 | 0 | | |
| **merged_or_terminated** | 1,334 | 240.7 | 117.2 | 123.5 |
| · final / terminate / dissolved flag on latest return | 1,187 | 233.4 | | |
| · e-Postcard terminated | 102 | 3.2 | | |
| · IRS history; name now on another BMF EIN | 45 | 4.0 | | |
| **revoked** | 1,405 | 83.6 | 43.2 | 40.4 |
| · no BMF successor | 1,197 | 69.8 | | |
| · name now on another BMF EIN | 95 | 7.7 | | |
| · partial name match | 44 | 3.4 | | |
| · government-unit name | 69 | 2.7 | | |
| **invalid_or_typo** | 568 | 46.4 | 23.4 | 22.9 |
| · typo: neighbour EIN (1 digit / transposition) with matching name | 333 | 25.9 | | |
| · wrong EIN: exact name unique in state | 66 | 6.5 | | |
| · wrong EIN: fuzzy name unique in state | 75 | 4.8 | | |
| · EIN on revocation list under an unrelated name | 36 | 4.3 | | |
| · EIN prefix not assigned by the IRS | 49 | 3.1 | | |
| · IRS history under another name; filed name on a BMF EIN | 5 | 1.0 | | |
| · typo: exact name unique in state, ≤ 2 digits differ | 4 | 0.8 | | |
| **new_ein** | 156 | 19.5 | 8.1 | 11.4 |
| · first tax period 2022 or later | 140 | 18.2 | | |
| · initial-return flag | 16 | 1.3 | | |

Every sub-category row with its Schedule I dollars and shares is in the CSV (`scope = category_sub`).

## 3. Findings

### 3.1 The largest bucket by count is churches and other religious bodies that never appear in IRS files [I]

14,647 EINs ($1.31bn) have a religious-pattern name and no trace in Pub 78, the revocation list, the e-Postcard file or the TEOS index. Examples are a Jesuit province, a Latter-day Saints entity, yeshivas and Catholic parishes.

Two features of the law make this expected [I]:
- churches are not required to apply for recognition or to file a 990;
- subordinates under a group ruling need not appear individually in the BMF.

This bucket overlaps the parent note's church finding (8.3% of top-50 dollars to BMF church-code organisations with no e-filed 990). It is the part with no BMF row at all.

Sensitivity: 2,350 of these EINs ($0.23bn) carry a name that matches exactly one same-state BMF EIN (898 exact, 1,452 fuzzy). If all were sponsor-entered wrong EINs, the invalid/typo bucket would grow to about $0.28bn. Because common church names recur, the central run does not count them (P-B40N1202-B43N2603-01).

### 3.2 Subsidiary LLCs carry 39% of the dollars

Four Chan Zuckerberg LLCs hold $1,594.0m:
- CZ Institute for Advanced Biological Imaging LLC, $563.9m;
- CZ Biohub SF LLC, $554.3m;
- CZ Biohub New York LLC, $238.6m;
- CZ Biohub Chicago LLC, $237.2m.

$1,603.2m of the LLC bucket's $1,610.7m falls in FY2023 [F]. A single-member LLC owned by a 501(c)(3) is normally disregarded for tax purposes and has no BMF row of its own [I]. The parent's Schedule R would confirm this (P-B40N1202-B43N2603-02). The other 55 LLC-named EINs total $16.8m.

### 3.3 Government units are about one dollar in seven

2,542 EINs ($631.1m) are government units. They include:
- the University of Texas at Austin ($54.5m);
- Penn State ($31.4m);
- Washoe County School District ($28.6m);
- UT MD Anderson ($25.4m);
- Detroit Public Schools Community District ($23.4m);
- UT Southwestern ($22.5m).

Gifts to governmental units are deductible under §170(c)(1) without BMF listing [I]. 447 of them ($300.2m) are labelled by the sponsors' own IRC-section text. The rest rest on name rules. No EIN-bearing line had a foreign address.

### 3.4 Merged or terminated organisations explain the 1,213 CN filing-rule passers

1,187 EINs ($233.4m) filed a final return or reported terminating or dissolving on their latest e-filed return. 884 of them ($220.4m) are among the 1,213 that pass CN's filing rules. The largest:
- Bright Future Fund, $37.4m;
- Heartland Alliance for Human Needs & Human Rights, $15.9m;
- Philanthropic Impact Foundation, $15.7m;
- Pahara Institute, $10.4m;
- BPS Foundation, $5.2m;
- Rocky Mountain Prep, $5.1m;
- IllumiNative, $5.0m.

Flags are counted per EIN across both headers read. In the merged category, 1,181 EINs carry `FinalReturnInd`, 684 `TerminateOperationsInd` and 459 `OrganizationDissolvedEtcInd` [F].

Reconciliation of the 1,213 ($292.8m) [F]:

| Category | EINs | $m |
|---|---|---|
| merged_or_terminated | 884 | 220.4 |
| unresolved (has filings, no termination signal) | 125 | 43.3 |
| revoked | 136 | 15.5 |
| foreign_or_government | 47 | 4.1 |
| new_ein | 15 | 9.1 |
| subsidiary_or_disregarded | 2 | 0.3 |
| invalid_or_typo | 4 | 0.1 |
| **Total** | **1,213** | **292.8** |

The 125 unresolved passers are the only plausible "live, not yet re-listed" organisations [I]. The largest is the LA Clippers Foundation ($15.5m). They are queued as P-B40N1202-B43N2603-06.

### 3.5 Wrong and mistyped EINs are small in dollars

The invalid/typo bucket holds 568 EINs and $46.4m (1.1% of non-BMF dollars) [F]. Examples:
- a large church entered one digit off its BMF EIN, filed under a name that matches the BMF entry;
- Catholic Charities of the Archdiocese of New York under an EIN one digit away;
- "Blue Ridge Conservancy" and "Crossroads Fund" under EINs that appear in no IRS file, while the same name is the only BMF entry in the state;
- 49 EINs whose prefix the IRS never assigns, including 999999999.

A one-digit neighbour with a similar name is a probable, not certain, typo. For example, "New Community Church" is filed one digit away from BMF "New Life Community Church" [I].

### 3.6 Revoked at the time of the grant (compliance-relevant; read with care)

Scope: the 1,405 EINs in the revoked category, i.e. on the IRS automatic revocation list with no reinstatement date and with a name matching the name as filed.

| Revocation timing vs the sponsor's fiscal year | Line-EINs | DAF-weighted $m | Schedule I $m | Sponsors |
|---|---|---|---|---|
| Effective before FY began; posted before FY began | 110 | 6.33 | 7.01 | 30 |
| Effective before FY began; posted during or after FY | 32 | 0.91 | 0.92 | 11 |
| **Effective before FY began (distinct EINs)** | **141** | **7.24** | | **32** |
| Effective during FY | 272 | 11.30 | 12.36 | 32 |
| Effective after FY ended | 1,092 | 65.04 | 69.68 | 45 |

Notes on the table [F]:
- Line-EIN counts are per bucket. An EIN with lines in two fiscal years can appear in two buckets.
- Of the $7.24m effective before the fiscal year began, $2.11m is FY2023 and $5.12m is FY2024.
- The median time from revocation to the start of the fiscal year is 4.1 years (line-weighted). 59% of lines are three or more years after revocation.
- Four sponsors account for 64% of the before-FY dollars. Sponsors are not named here: the screen cannot distinguish a lapse from a documented decision.

Composition of the $6.33m posted before the fiscal year began [F]:
- $1.87m (14 EINs): the same name is now on another same-state BMF EIN. This is likely a stale EIN for an organisation re-recognised or succeeded under a new number. For example, an old UCSF EIN revoked in 2022, and a Lutheran high school revoked in 2011 whose name is listed under a current EIN.
- $0.68m (20 EINs): government-unit names, such as a public library. Deductibility there rests on §170(c)(1), not on exemption.
- $1.23m (10 EINs): partial name match.
- $2.55m (66 EINs): matching name and no BMF successor. This is the core of the signal.

**How to read this.**
1. The IRS says an automatically revoked organisation "is not eligible to receive tax-deductible contributions and will be removed from … Publication 78" [P]. A DAF grant is not itself a deductible gift (the donor's deduction arose on contribution to the fund), but sponsors generally confirm public-charity status before granting [I].
2. Revocations can be reversed retroactively. The IRS's streamlined and 15-month procedures can reinstate status "retroactively … to the date of revocation" [P]. A later reinstatement would remove an EIN from this count. 106 non-BMF EINs already show a reinstatement date.
3. Grant dates within the fiscal year are unknown, which is why the "during FY" bucket is reported separately.
4. A sponsor can pay a non-exempt organisation for a charitable purpose with expenditure responsibility, or pay a fiscal sponsor that names the project on the line. Neither is visible on Schedule I [I].
5. This uses public data only. It measures what a public-data screen would have flagged at grant time; it is not a finding about any sponsor or grantee.

Most revoked-recipient dollars ($65.0m of $83.6m) went to organisations revoked only after the FY2023–24 grants. 866 of the 1,405 have revocation dates in 2025 or 2026 [F]. For these organisations, the grant came first and the loss of status later.

## 4. Limits

1. **Absence of evidence is not evidence of absence.** "No IRS trace" means absent from the four public bulk files and the TEOS e-file index. Paper filers before 2019, churches and group subordinates can be legitimate and still absent.
2. **Name rules.** The government, religious and LLC labels rest on regular expressions over filed names and IRC text. The "600" EIN heuristic is undocumented, and about 4 of 20 sampled cases look non-governmental. Typo and wrong-EIN matches are probable, not confirmed. City was not used because the cached Schedule I lines keep only the state.
3. **No earlier BMF.** The IRS posts only the current extract (§1.3), so "dropped from the BMF after the grant" can be inferred only from final-return flags and revocation dates.
4. **One header pair per EIN.** Only the earliest and latest e-filed returns were read, and 59 were missing from the mirror. A final-return flag on the latest return can coexist with a successor that files under a new EIN.
5. **Fiscal-year dating.** Each grant is dated only to a 12-month window ending on the sponsor's `tax_period_end`. Short or long periods are not handled.
6. **Revocation file timing.** The revocation, Pub 78 and BMF files were cached 2026-11-11 to 2026-11-14, and the e-Postcard file is dated 2026-11-16. Later reinstatements are not reflected.
7. **Dollars.** DAF-weighting is sponsor-level, as in the parent study. Schedule I dollars are given alongside.
8. **Organisations only.** The per-EIN rows list organisational recipients (Schedule I Part II lines with an EIN). No individuals are listed. Names are as the sponsor filed them; the name on the largest line is kept.

## 5. Headline claims for validation

1. The 22,269 EINs and $4,175.4m DAF-weighted reproduce the parent §4.1 `not_in_bmf` row. The 1,213 EINs / $292.8m CN filing-rule passers also reproduce. Evidence: script JSON `non_bmf_eins`, `usd_dw`, `cn_pass`; CSV `scope = all`.
2. 18,928 of the 22,269 EINs (85%) appear in none of Pub 78, the revocation list, the e-Postcard file or the TEOS index 2019–2026. 3 are in Pub 78. Evidence: JSON `evidence_counts`.
3. Four CZ LLC EINs hold $1,594.0m, 38% of non-BMF dollars. Evidence: CSV recipient rows 882242512, 882010111, 931478843, 922259616.
4. 14,647 religious-pattern EINs with no IRS trace hold $1,313.0m. Evidence: CSV `category_sub` `unresolved/no_irs_trace_religious_name`.
5. 884 of the 1,213 CN filing-rule passers ($220.4m) carry a final-return, terminate or dissolved flag on their latest e-filed return. Evidence: CSV `scope = cn_filing_rule_pass_1213`; header cache.
6. Government units hold $631.1m across 2,542 EINs. 447 of them ($300.2m) are labelled by the sponsors' own IRC-section text. Evidence: CSV `category_sub` `foreign_or_government/*`.
7. EINs revoked effective before the granting sponsor's fiscal year received $7.24m DAF-weighted (141 EINs, 32 sponsors). $6.33m of it went to revocations posted before the fiscal year. Evidence: JSON `revoked_timing`; revocation list rows by EIN.
8. $65.0m of the $83.6m paid to revoked EINs went to EINs revoked only after the fiscal year ended. Evidence: JSON `revoked_timing.after_fy`, `revoked_rev_year`.
9. Wrong or mistyped EINs total $46.4m (568 EINs). 333 of them are one digit or one transposition away from a BMF EIN with a matching name. Evidence: CSV `category_sub` `invalid_or_typo/*`.

## 6. Data dictionary: `non-bmf-recipients-2026-11-20.csv`

| Column | Meaning |
|---|---|
| row_type | `aggregate` (54 rows) or `recipient` (22,269 rows, one per EIN) |
| scope | Aggregate rows only: `category` (seven-way), `category_six_way` (task's six; LLC folded into unresolved), `category_sub` (category/sub), `cn_filing_rule_pass_1213` (the 1,213 CN filing-rule passers by category), `all` |
| category | Category (or `category/sub` for `category_sub` rows). Values: revoked, foreign_or_government, subsidiary_or_disregarded, invalid_or_typo, merged_or_terminated, new_ein, unresolved |
| recipients | Aggregate: EIN count |
| usd_daf_weighted | DAF-weighted FY2023–24 dollars, rounded (recipient rows: that EIN's total) |
| usd_schedule_i | Aggregate: unweighted Schedule I dollars |
| usd_daf_weighted_fy2023 / _fy2024 | Aggregate: DAF-weighted dollars by sponsor fiscal year (year of `tax_period_end`) |
| share_of_non_bmf_daf_weighted | Aggregate: share of the scope's DAF-weighted dollars ($4,175.4m for every scope except `cn_filing_rule_pass_1213`, where the base is $292.8m) |
| share_of_all_top50_daf_weighted | Aggregate: share of all top-50 DAF-weighted dollars including blank-EIN lines ($74,073.8m) |
| ein | Recipient rows: 9-digit EIN as filed |
| name_as_filed | Recipient rows: sponsor-filed recipient name on the EIN's largest line |

## 7. Source register

| # | Source | URL | Date | Used for |
|---|---|---|---|---|
| S1 | IRS EO BMF extract (eo1–4, eo_pr, eo_xx) and its page | https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf ; files at https://www.irs.gov/pub/irs-soi/eo1.csv etc. | Files cached 2026-11-14; page reviewed 16-Nov-2026, read 2026-11-20 | Universe (not in BMF); name index; no earlier extracts offered |
| S2 | IRS TEOS bulk data downloads page | https://www.irs.gov/charities-non-profits/tax-exempt-organization-search-bulk-data-downloads | "Last updated: Nov. 11, 2026"; read 2026-11-20 | Lists the three bulk files below |
| S3 | Pub 78 data | https://apps.irs.gov/pub/epostcard/data-download-pub78.zip | Cached 2026-11-14 (file dated 2026-11-11) | Pub 78 match |
| S4 | Automatic revocation list | https://apps.irs.gov/pub/epostcard/data-download-revocation.zip | Cached 2026-11-14 (file dated 2026-11-11) | Revocation, posting and reinstatement dates |
| S5 | Form 990-N e-Postcard data | https://apps.irs.gov/pub/epostcard/data-download-epostcard.zip | Downloaded 2026-11-20 (file dated 2026-11-16) | Terminated flag, first tax year |
| S6 | IRS TEOS e-file index 2019–2026 | https://apps.irs.gov/pub/epostcard/990/xml/2024/index_2024.csv (and 2019–2026) | Cached 2026-11-14/15 | Filing history, filer names |
| S7 | GivingTuesday mirror of IRS TEOS XML | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml | Read 2026-11-20 (4,202 headers) | Initial, final, terminate and pending indicators |
| S8 | IRS, "Automatic revocation of exemption" | https://www.irs.gov/charities-non-profits/automatic-revocation-of-exemption | Reviewed 28-Jun-2026; read 2026-11-20 | Effective-date rule; "not eligible to receive tax-deductible contributions" |
| S9 | IRS, "Automatic revocation – how to have your tax-exempt status reinstated" | https://www.irs.gov/charities-non-profits/charitable-organizations/automatic-revocation-how-to-have-your-tax-exempt-status-reinstated | Read 2026-11-20 | Retroactive reinstatement "to the date of revocation" |
| S10 | IRS, "Valid EINs" (valid EIN prefixes by campus) | https://www.irs.gov/businesses/small-businesses-self-employed/valid-eins (redirect from …/how-eins-are-assigned-and-valid-ein-prefixes) | Reviewed 04-Nov-2026; read 2026-11-20 | Unassigned-prefix test |
| S11 | Parent note and script | [b40n1202-b43n26-recipient-basis-and-rating-eligibility.md](b40n1202-b43n26-recipient-basis-and-rating-eligibility.md); `scripts/mission_recipient_basis_eligibility.py` | 2026-11-19 | Universe, dollars, CN filing tests |
