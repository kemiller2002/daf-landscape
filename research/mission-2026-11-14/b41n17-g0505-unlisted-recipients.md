# Unlisted Schedule I recipients and the two largest single-line drivers (P-B41N17-01, P-G05-05)

**Date:** 2026-11-19 · **Task ID:** b41n17-g0505 · **Builds on:** [direction-recipient-compliance-screen.md](direction-recipient-compliance-screen.md) (P-NEW-REC-01, with its wave-26 corrections), [gap19-exception-load-proxy.md](gap19-exception-load-proxy.md) (P-GAP19-05, with its wave-32A corrections and the governing regeneration note), and [b40n1202-b43n26-recipient-basis-and-rating-eligibility.md](b40n1202-b43n26-recipient-basis-and-rating-eligibility.md) (wave-34B correction: EINs missing from the BMF are mostly CZ Biohub LLCs and government bodies, not revoked charities).

**Outputs**
- Script: [`scripts/mission_unlisted_recipients.py`](../../scripts/mission_unlisted_recipients.py). It is new. It imports the line pipeline and `screen` from `mission_recipient_compliance.py` and `is_totals_row` from `mission_exception_load.py`, unchanged. Stdlib only, functional style.
- Data: [`data/mission-2026-11-14/unlisted-recipients-resolution-2026-11-19.csv`](../../data/mission-2026-11-14/unlisted-recipients-resolution-2026-11-19.csv). It holds 10,801 rows: 27 `summary` rows and 10,774 `recipient` rows (6,917 unlisted-EIN keys and 3,857 blank-EIN keys). The data dictionary is in §7.
- Queue proposals: [`data/mission-2026-11-14/queue-proposals-b41n17-g0505.csv`](../../data/mission-2026-11-14/queue-proposals-b41n17-g0505.csv) (5 rows).

Tags: **[F]** filed or IRS-published value · **[C]** computed by the script · **[P]** quoted primary source · **[I]** inference · **[H]** reviewer hand judgement.

---

## 0. Answers in brief

**(A) P-B41N17-01: who the unlisted recipients are**

| Pool (FY2023–24, top-50 Schedule I) | As briefed | Resolved here | Sponsor EIN misreport, or identifiable listed charity | Legitimately absent (church, government, subsidiary) | Recognised before but now revoked | Not found by name and state on 2026-11 lists (an upper bound on unrecognised: matcher recall unmeasured) [V wave 36B] |
|---|---|---|---|---|---|---|
| **EIN in neither Pub 78 nor BMF, no explaining label** | 12,265 lines, $818.7m [C] | same | **$28.6–36.5m (3.5–4.5%)**. Tier-A matches are $33.5m. $5.3m of the matches have a filed EIN one or two digits off, or one adjacent swap, from the listed EIN [C/H] | $190.8m (23.3%) by extended religious and public-body name rules [C/I] | $87.4m (10.7%): the filed EIN is on the revocation list, and no listed record has the name [C] | **$419.4m (51.2%)** (no match, $384.2m, plus tier-C matches, mostly false (2 of 28 right in the pooled 75-key hand check), $35.2m) [V wave 36B]. Another $74.9m (9.1%) is ambiguous [C/H] |
| **Blank or placeholder EIN** | 5,013 lines, $644.0m [C] | **5,011 lines, $431.8m.** Greater Horizons' two FY2024 totals rows ($212,187,406 and 3,282) are dropped (§4.1) | **$36.8m (8.5%)** are identifiable listed charities whose EIN was left blank. That is tier A, with 12 of 12 judged correct [C/H] | **$286.4m (66.3%)**: church-labelled $183.7m (NCF's two church lines alone are $142.0m), government $77.7m, other labels and extended rules $25.0m [C] | n/a | $31.3m (7.2%). Another $56.5m (13.1%) is ambiguous [C/H] |

- **Most of the unlisted-EIN pool is not sponsor EIN error.** A name-and-state match finds a listed charity under another EIN for only about 4% of the dollars. P-NEW-REC-01 had called "most likely EIN error" the main explanation (§2.4 there). The data do not support that [C/H].
- About half of the pool goes to organisations that **this matcher did not find on either IRS list under any EIN** by name and state. That is an upper bound on unlisted recipients, not a count: the matcher's recall is unmeasured (brand names such as “Fidelity Charitable” are missed), a few tier-C keys counted here are right (The Policy Circle; Social Good Fund; National Abortion Federation filed in DC), and the class includes plausibly legitimate absences such as group-ruling schools and an apparently tribal enterprise (Rosebud Economic Development Corporation, SD, $8.4m) [H/I] [V wave 36B] Examples are Heartland Alliance for Human Needs & Human Rights ($14.6m) and Regis High School ($11.2m), which have no BMF or Pub 78 record under those names [C/F].
- **Blank-EIN lines are mostly churches and government units.** About two-thirds of the net dollars go to them, and neither needs an EIN-based Pub 78 check under a sponsor's standing rules [I]. About 9% go to listed charities whose EIN was simply omitted.
- **Matcher precision (40-key hand check, stratified by tier).**
  - 18 of the 35 judged keys are correct (**51%**, Wilson 95% 36–67%). 5 keys were unsure. If unsure keys count as wrong, precision is 18/40 = 45%.
  - Precision splits sharply by tier:
    - **tier A** (identical name, same state): **17 of 17 judged** (Wilson 82–100%; 17/21 = 81% if unsure counts as wrong). A validator sample of 14 other tier-A keys found 6 correct, 2 wrong (a word-order collision and a same-name collision) and 6 unsure, so pooled tier A is 23 of 25 judged, or 66% if unsure counts as wrong [H] [V wave 36B]
    - tier B (fuzzy, same state): 1 of 3;
    - **tier C** (identical name, other state): **0 of 15**. The validator's 13 further tier-C keys had 2 correct (national organisations filed with another state), so pooled 2 of 28 [H] [V wave 36B]
  - The misreport estimate therefore rests on tier A, plus a quarter to a half of tier B [H]. On the pooled 75-key check (tier A 23/35 to 23/25, tier B 6/17 to 10/17, tier C 2/28) it is $26.7–36.9m (3.3–4.5%) [C/H] [V wave 36B]

**(B) P-G05-05: the two largest single-line drivers**
- **Greater Horizons FY2024, $212.2m, no name and no EIN.** The return confirms this is a totals row, not a grant [F].
  - The last two of its 3,284 `RecipientTable` elements carry only a `CashGrantAmt`: 212,187,406 and 3,282.
  - 212,187,406 equals the sum of the 3,282 named lines exactly. 3,282 equals the `Total501c3OrgCnt` filed on line 2 of the same schedule.
  - Part IX line 1 is $224,183,118, so the named lines are already within it, and adding the totals row would exceed it.
  - Neither Schedule I's Part I text nor Schedule O mentions the rows.
- **SVCF FY2023, $1.309bn, "Further Future Foundation" (EIN 92-1117448).** SVCF filed the line under that name, not as "Navigation Charitable Fund" as the brief says [F].
  - **The recipient renamed itself** Navigation Charitable Fund on 2023-11-01. It operates as "The Navigation Fund": a Delaware nonprofit corporation formed in 2022, recognised under 501(c)(3), and classed as a 170(b)(1)(A)(vi) public charity in its first five years. It holds no DAFs [F].
  - **Source of the money.** The $1,309,000,000 is exactly its total 2023 contributions, and Schedule B (contributor details) is restricted. The fund's site says it began "with an initial gift from Jed McCaleb" [P]. The SVCF line is cash, purpose "Sciences" [F]. SVCF's Schedule I does not say whether the grant came from a DAF, and SVCF's Schedule R does not list the recipient [F/I]. That this grant is the McCaleb gift is an inference, not a filed fact: no filing names the donor, though the fund's Schedule A counts the full $1,309,000,000 as public support, consistent with a single gift from a publicly supported charity such as SVCF [F/I] [V wave 36B]
  - **Controlling relationship.** NCF owns **100% of Voltage Park, Inc.** (EIN 92-3779527), a for-profit Delaware C corporation in San Mateo whose stated activity is "cloud infrastructure". Its equity is carried at **$883.5m** at end-2023 and end-2024 [F].
  - **What it did with the money (2023–24):**
    - granted $41.1m (3.1% of the gift). Of this, $17.1m went to **Vanguard Charitable** with "non-binding recommendations", which is in effect DAF-to-DAF routing, and $16.6m went to Humane America Animal Foundation;
    - held $883.5m in Voltage Park (67.5%) and $405.0m in savings and temporary cash at end-2024. Net assets at end-2024 were $1,289.1m [F/C].

---

## 1. Method (A)

1. **Pools.**
   - The P-NEW-REC-01 pipeline is reproduced exactly: the same 94 itemising sponsor-years, the same line cache, and `mission_recipient_compliance.screen` with no revocation or name inputs.
   - `ein_unlisted` is the flag `absent_pub78_and_bmf` with none of the six explaining labels. It reproduces **12,265 lines and $818,725,018**, matching P-NEW-REC-01 §2.1 [C].
   - `blank_ein` is a blank or placeholder EIN. It reproduces **5,013 lines and $643,991,900** [C].
   - The two Greater Horizons totals rows are dropped by `is_totals_row`, the rule from the P-GAP19-05 regeneration. That leaves 5,011 lines and $431,801,212.
2. **Unit.** One key per distinct (pool, filed EIN, normalised token set, state), pooled across sponsor-years. This gives 6,917 and 3,857 keys.
3. **Reference files.**
   - Every record in the EO BMF (eo1–eo4, eo_pr, eo_xx; 2026-11-09) and Pub 78 (2026-11-11), about 3.4m names in total.
   - A matched EIN counts as **listed** if it is in Pub 78 or has BMF subsection 03.
4. **Matcher rules** (published in the script header and constants):
   - **Normalisation:**
     - upper case; `&` becomes AND; apostrophes are removed; other punctuation becomes a space;
     - abbreviations are expanded (FDN→FOUNDATION, ST→SAINT, CTR→CENTER, INTL→INTERNATIONAL and 30 others, listed in `ABBR`);
     - stop and legal-form words are dropped (`STOP`: THE, OF, AND, FOR, INC, CORP, LLC, CO, LTD, TRUST, FUND and others);
     - the **set** of tokens is compared, so word order is ignored.
   - **Score:** Jaccard |A∩B| / |A∪B|. Both the Pub 78 and the BMF spelling of each reference EIN are tried.
   - **Tiers:**
     - **A:** score 1.0 and same state.
     - **B:** score ≥ 0.80, same state, at least 2 tokens, and the two token sets differ by no entity-marking token. `DISTINGUISH` lists 30 such tokens, including FOUNDATION, ENDOWMENT, LEGACY, II, III, ALUMNI, FRIENDS, PARENTS, BOOSTERS, INTERNATIONAL and PROPERTY.
     - **C:** score 1.0 in another state, or with no state on the line, and at least 2 tokens.
   - **Winner and ties:** the best tier wins, then the highest score. If more than one EIN ties at the best (tier, score), and exactly one of them is listed, that one is taken. Otherwise the key is `ambiguous`.
   - **Blocking.** Exact: candidates must share one of the target's k rarest tokens (document frequency over all 3.4m names), with k = ⌊0.2n⌋ + 1. A record scoring ≥ 0.80 can lack at most ⌊0.2n⌋ of the target's tokens, so blocking never drops a qualifying candidate.
   - **Typo check.** For the unlisted-EIN pool, the filed and matched EINs are compared. A difference of one or two digits, or one adjacent swap, is flagged `ein_typo_like`.
5. **Resolution classes** (`resolution`):
   - **Matched:**
     - `matched_listed_other_ein`: a unique match to a listed charity;
     - `matched_bmf_non_c3`;
     - `ambiguous`.
   - **No match:** classified in this order:
     1. foreign address;
     2. P-NEW-REC-01 label (blank pool only; the unlisted-EIN pool has none by construction);
     3. filed EIN on the revocation list (`unmatched_revoked_ein`);
     4. extended public-body name rule (`PUBLIC_EXT`, e.g. UNIVERSITY OF, MEDICAL CENTER, AUTHORITY, COUNTY, DISTRICT, LIBRARY). This follows the wave-34B finding that BMF-absent EINs are often government bodies;
     5. extended religious name rule (`RELIGIOUS_EXT`, e.g. AHAVAS, BETH, BAIS, KEHILLAT, BAPTIST, LUTHERAN, CATHOLIC, MINISTRIES, MISSION);
     6. subsidiary or fund name (`SUBSIDIARY_EXT`);
     7. otherwise `unmatched_other`.
6. **Hand check.**
   - The sample is deterministic: 20 matched keys per pool, allocated across tiers in proportion to key counts (largest remainder, at least 1 per tier), then the lowest SHA-1 of the key in each tier.
   - Each pair was judged on filed name and state against matched name, city and state, using only the CSV fields and general knowledge (no outside lookups). Each was marked `correct`, `wrong` or `unsure`, with a one-line reason.
   - The verdicts are stored in the script (`HANDCHECK`) and written to the CSV [H].
7. **Estimate** of sponsor EIN misreporting in `ein_unlisted`:
   - **lower bound** = tier A × 17/21 (unsure counted as wrong) + tier B × 1/4 = **$28.6m**;
   - **upper bound** = tier A × 1 + tier B × 2/4 = **$36.5m**;
   - tier C (0/15) and ambiguous keys are not counted.
   - "Genuinely unrecognised" = `unmatched_other` plus tier-C matches.
8. **Privacy.** Blank-EIN keys with no listed match may name individuals. P-NEW-REC-01 kept blank-EIN lines out of its hit rows for this reason. Here their names are withheld and their keys hashed (2,145 keys, `name_withheld = 1`). State and dollar amounts are kept.

## 2. Coverage and checks [C]
- Both pools reproduce the P-NEW-REC-01 figures to the line and the dollar.
- The dropped totals rows are exactly the two Greater Horizons FY2024 lines named in the P-GAP19-05 regeneration note. $643,991,900 − $431,801,212 = $212,190,688 = 212,187,406 + 3,282.
- The text vocabulary has 7,482 distinct tokens across 10,774 targets. Run time is about 80 s.
- **DAF-to-DAF:** only $3.4m of the unlisted-EIN pool sits on whitelisted DAF-to-DAF lines (`d2d_line`). A DAF-to-DAF line filed with a wrong EIN escapes the whitelist; one example is "Fidelity Charitable" (OH, $0.89m), which the matcher also misses (§5).

## 3. Results (A)

### 3.1 Unlisted-EIN pool ($818.7m, 12,265 lines, 6,917 keys) [C]
| Resolution | Keys | Lines | $m | % of $ |
|---|---|---|---|---|
| Matched to a listed charity, other EIN: tier A | 264 | 507 | 33.46 | 4.09% |
| … tier B | 83 | 154 | 6.09 | 0.74% |
| … tier C (judged false, §3.3) | 362 | 632 | 35.20 | 4.30% |
| … of which typo-like EIN (all tiers) | 55 | — | 5.31 | 0.65% |
| Ambiguous (several listed EINs tie) | 508 | 852 | 74.90 | 9.15% |
| Matched BMF non-501(c)(3) | 7 | 14 | 1.28 | 0.16% |
| No match, filed EIN revoked | 1,391 | 2,031 | 87.39 | 10.67% |
| No match, religious name (extended rule) | 765 | 1,457 | 125.75 | 15.36% |
| No match, public-body name (extended rule) | 400 | 639 | 65.05 | 7.95% |
| No match, subsidiary or fund name | 46 | 84 | 5.37 | 0.66% |
| **No match, other** | **3,091** | **5,895** | **384.24** | **46.93%** |

**Largest cases:**
- **Clear misreports, a listed record under another EIN:**
  - Junipero Serra High School (CA, $4.09m; the listed record is "Junipero Serra High School A Corp"; there are two such schools in CA, so this is [I]);
  - Delbarton School ($1.94m; the same filed EIN also carries “Order of St Benedict of NJ Delbarton School”, $0.83m, unmatched, so the filed EIN may be the operating order's rather than a keying error) [I] [V wave 36B]
  - Center for Investigative Reporting ($1.93m);
  - National Abortion Federation ($1.85m MD, tier A; the further $1.56m filed with a DC address is a tier-C key, so it is counted in the not-found total although the match looks right) [V wave 36B]
  - Blue Ridge Conservancy ($1.62m);
  - Fred Hutchinson ($1.92m, tier B: "Cancer Research Center" against the current "Cancer Center").
- **Typo-like EINs** include American Endowment Foundation (341947398 filed for 341747398; $1.0m, from Stanford's board of trustees), Million Dollar Women Fund (one digit) and K18N Foundation (two digits) [C].
- **Unmatched, the largest** [C/F]:
  - LA Clippers Foundation ($15.5m, GS DAF);
  - Heartland Alliance for Human Needs & Human Rights ($14.6m, plus $2.0m as "National Immigrant Justice Center" under the same EIN);
  - Philanthropic Impact Foundation ($12.0m + $3.7m);
  - Regis High School ($11.2m);
  - Pahara Institute ($11.0m);
  - Exygy Inc ($9.75m, SVCF);
  - the top 10 unmatched keys hold 24.3% of `unmatched_other` dollars, the top 100 hold 56.8%.
  - Heartland Alliance has related EINs on the BMF (Heartland Alliance International, Heartland Alliance Health) but none under the parent's name. Regis High School appears only as a property trust. Being absent from the lists is a fact here, but these names do not look like new or unknown grantees [I].
- **Revoked filed EIN:** the largest are Pet Network Humane Society ($3.8m), KIPP NYC Public Charter Schools ($3.1m), As The Word Turns ($2.4m) and Firefly Academy ($2.25m, also in P-NEW-REC-01 §2.4).
- **Extended religious rule:** led by Ahavas Zion ($68.5m), which P-NEW-REC-01 noted as missed by its congregation rule.
- **Extended public-body rule** (wave-34B pattern): UT Southwestern Medical Center ($9.3m), the Tulsa River Parks Authority / Gathering Place ($13.4m on two keys), Ruby Valley Conservation District, North Logan City and Clatsop County.

### 3.2 Blank-EIN pool ($431.8m net, 5,011 lines, 3,857 keys) [C]
| Resolution | Keys | Lines | $m | % of $ |
|---|---|---|---|---|
| Matched listed charity: tier A | 595 | 763 | 36.75 | 8.51% |
| … tier B | 118 | 153 | 4.45 | 1.03% |
| … tier C | 233 | 306 | 10.14 | 2.35% |
| Ambiguous | 758 | 1,046 | 56.47 | 13.08% |
| Matched BMF non-501(c)(3) | 8 | 9 | 16.15 | 3.74% |
| No match, church label | 1,060 | 1,454 | 183.68 | 42.54% |
| No match, government label | 349 | 435 | 77.72 | 18.00% |
| No match, possible public university / LLC labels | 89 | 100 | 6.31 | 1.46% |
| No match, extended public-body / religious / subsidiary rules | 190 | 232 | 18.73 | 4.34% |
| No match, foreign address | 2 | 2 | 0.28 | 0.07% |
| **No match, other** | **455** | **511** | **21.12** | **4.89%** |

- **Church label:** dominated by NCF's First Baptist Church Chandler ($88.0m) and First Baptist Church of Fremont ($54.0m), as in P-GAP19-05 §2.
- **Government label:** Chicago Public Schools ($25.0m, Chicago Community Trust) and Grand Prairie ISD ($16.0m, NPT).
- **Matched non-501(c)(3):** the $16.0m Escondido Union School District line matched the district's school-facilities corporation. The grantee is the district, a government body [I].
- **Identifiable listed grantees with the EIN omitted:**
  - Regents of the University of Michigan ($3.6m);
  - Coral Ridge Presbyterian Church ($3.0m);
  - Bethel Baptist Church Ministries ($2.0m);
  - Steans Family Foundation ($1.48m, Pub 78 PF);
  - Church of Jesus Christ of Latter-day Saints ($1.46m).
- **Withheld names.** The `unmatched_other` blank-EIN names (withheld) include apparent personal names and commercial payees such as architects, title companies and apartment complexes [H]. This is not quantified (P-B41N17G0505-03).

### 3.3 Hand check of 40 matches [H]
| Tier | Correct | Wrong | Unsure | Precision (judged) |
|---|---|---|---|---|
| A (identical name, same state) | 17 | 0 | 4 | 100% (Wilson 82–100%) |
| B (Jaccard ≥ 0.80, same state) | 1 | 2 | 1 | 33% |
| C (identical name, other state) | 0 | 15 | 0 | 0% (Wilson 0–20%) |
| **All** | **18** | **17** | **5** | **51% (36–67%)** |

By pool: unlisted-EIN 5 correct / 11 wrong / 4 unsure; blank-EIN 13 / 6 / 1.

**Validator re-check (wave 36B).** An independent seeded sample of 40 other matched keys (14 tier A, 13 tier B, 13 tier C) gave:
- **tier A:** 6 correct, 2 wrong, 6 unsure. The wrong keys are “The Wildlife Center of Texas” TX matched to “Texas Wildlife Center”, Amarillo (word order is ignored), and “Gateway Center” GA matched to a Cordele record.
- **tier B:** 5 correct, 5 wrong, 3 unsure. Two of the wrong keys, YMCA of Stamford and Los Angeles Mission Foundation, have filed EINs on the revocation list but were matched to other organisations; matching runs before the revocation class.
- **tier C:** 2 correct, 11 wrong. The correct ones are The Policy Circle and Social Good Fund, national organisations filed with a donor-side state.

Pooled over 75 keys: tier A 23 of 25 judged (66% if unsure counts as wrong), tier B 6 of 13, tier C 2 of 28 [H] [V wave 36B]

- **Tier-C errors** are all common Catholic, Baptist or Methodist parish and school names, plus generic names, matched in another state. Examples: St Matthew's Catholic Church AZ→MS; Ursuline Academy MA→DE; St Raymond of Penafort PA→VA.
- **Tier-B errors:**
  - Zionsville Community High School matched its **PTO**;
  - "Good Shepherd United Methodist Church" matched a BMF name truncated to "Good Shepherd United Church of".
- **Unsure:** generic names with one in-state listing (Sacred Heart School IL, Sacred Heart Catholic School FL, Church of the Resurrection NC), "Our Lady of Lourdes" matched to "Our Lady of Lourdes Fund Inc" (FUND is a stop word), and Elizabeth (Ann) Seton School CA.
- **Retuning.** The rules were not retuned after the sample, so the precision above is that of the published rules. P-B41N17G0505-01 proposes retuning on a fresh sample.

### 3.4 Reading [I]
- Sponsor EIN misreporting that can be shown from public names and states is **$27–37m**, 3.3–4.5% of the $818.7m, on the pooled 75-key hand check ($28.6–36.5m on the original 40 keys). Part of it is filing under a parent, religious-order or predecessor EIN rather than keying error (e.g. Delbarton School; Fred Hutchinson's pre-merger EIN) [C/H/I] [V wave 36B] A sixth of it ($5.3m) is clear keying error (one or two digits off, or one swap).
- An upper bound counts every ambiguous key as misreport and assumes tier C were right: $33.5m + $6.1m + $35.2m + $74.9m = $149.7m (18%). The hand check makes that bound implausible.
- **Recall is not measured.** Misreports where the sponsor used the grantee's brand name ("Fidelity Charitable", "LISC") rather than its IRS name are missed. The true misreport share is therefore higher than 4% [I]. A plausible ceiling is still well below half the pool, because the largest unmatched names are also absent from the IRS lists under every EIN, not only the filed one.
- About **half the pool ($419m) goes to organisations that the matcher did not find under that name in that state.** This is an upper bound on unlisted recipients, not a count of them: recall is unmeasured, and the class includes some correct tier-C matches [V wave 36B] The candidate explanations are:
  - group-ruling subordinates under unlisted names (e.g. Catholic high schools; Regis High School);
  - organisations that merged or dissolved after the grant (Pub 78 and the BMF are 2026 snapshots);
  - new organisations not yet listed;
  - a residue of government bodies and congregations missed by the name rules.
  - It is not evidence of grants to ineligible recipients.
- For the blank-EIN pool the picture is cleaner: two-thirds is churches and government units, 9–10% is identifiable listed charities, and about 7% is unidentified.

## 4. Results (B)

### 4.1 Greater Horizons FY2024 (object id 202513189349309621; tax period ending 2024-12-31) [F]
- **Filing.** Schedule I, softwareId 24020961 (2024v5.1), preparer Forvis Mazars LLP. Its Part I holds only `GrantRecordsMaintainedInd = true`, plus a line-2 monitoring statement. That statement says grantees are "checked against the IRS public charity list and watch list" and that significant restricted grants are monitored through progress and final reports.
- **The two rows.** The schedule has 3,284 `RecipientTable` elements. Elements 3,283 and 3,284, the last two, contain only `<CashGrantAmt>212187406</CashGrantAmt>` and `<CashGrantAmt>3282</CashGrantAmt>`. They have no name, address, EIN, IRC section or purpose.
- **Why they are totals:**
  - The 3,282 named rows sum to $212,187,406, exactly the first figure [C].
  - Line 2 reports `Total501c3OrgCnt = 3282` and `TotalOtherOrgCnt = 0`. The second row repeats the count.
  - Part IX line 1 (grants to domestic organisations) is $224,183,118. The named rows ($212.2m) fit inside it; named rows plus the totals row ($424.4m) do not [F/C].
  - Part III scholarships are separate: 224 recipients, $1,413,260, which equals Part IX line 2.
- **Filing text.** Schedule O has eight explanations (Part VI governance, Part VIII line 11d, Part XI line 9). None refers to Schedule I, a totals row or a grant without a recipient.
- **Conclusion:** an e-file totals row and count row keyed as recipient lines. The filing text has no explanation for them. They should be dropped, as `mission_exception_load.drop_totals_rows` now does [F/I].

### 4.2 SVCF FY2023 → Further Future Foundation / Navigation Charitable Fund [F unless tagged]
**Filer side.** SVCF's return is object id 202413129349304911, tax period ending 2023-12-31.
- **The line itself.** Schedule I line: "Further Future Foundation", 2991 Sacramento Street, Suite 230, Berkeley CA 94702; EIN 921117448; IRC 501(c)(3); cash $1,309,000,000; non-cash $0; purpose "Sciences".
- **Size against SVCF totals.**
  - It is 26.8% of SVCF's Part IX line 1 ($4,886,115,481) [C].
  - SVCF reports $4,889,252,836 of DAF grants on Schedule D Part I. These are at least its whole line 1, so the line was very probably a DAF grant [I].
- **What SVCF's text says.** Schedule I Part I line 2 is SVCF's standard grantee stipulations (charitable use only, no benefit to advisors, no pledge payment, return of unused funds, reports for some grants). Schedule O has seven explanations, all on governance or Part XI. None mentions the grant or the recipient, and the name appears nowhere else in the return (no Schedule R entry).

**Recipient side.** Its own Forms 990 are TY2023 (object id 202433209349325783, filed 2024-11-15) and TY2024 (202513009349302251, filed 2025-10-27).

| Item | TY2023 | TY2024 |
|---|---|---|
| Name on return | "The Navigation Fund" (name-change box checked); index name "Navigation Charitable Fund (fka Further Future Foundation)" | The Navigation Fund |
| Formation; domicile; status | 2022; Delaware corporation; 501(c)(3); Schedule A 170(b)(1)(A)(vi), first five years; DonorAdvisedFundInd = 0 | same |
| Contributions | **$1,309,000,000** (Schedule B contributor "RESTRICTED"; no non-cash contributions reported) | $0 |
| Investment income | $4.15m | $18.95m |
| Grants paid | $4.125m: Humane America Animal Foundation $2.375m; **Vanguard Charitable $1.75m** ("criminal justice reform") | $37.0m: **Vanguard Charitable $15.375m**; Humane America Animal Foundation $14.24m; NYU $5.0m ("new program area"); $1.91m abroad (Schedule F; Europe, Sub-Saharan Africa); 6 non-501(c)(3) payees including consultancies |
| Total expenses; employees | $5.06m; 3 | $39.3m; 7 |
| End-of-year assets | $1,308.1m: cash $5.8m; savings/temporary cash $418.8m; **other securities $883.5m = "Voltage Park, Inc."** (Schedule D Part VII, end-of-year market value) | $1,289.5m: savings/temporary cash $405.0m; Voltage Park $883.5m |
| Controlled entity (Schedule R Part IV) | Voltage Park Inc, EIN 92-3779527, San Mateo CA, "cloud infrastructure", Delaware, C corporation, 100% owned, controlled; share of income $1.17m, of end-of-year assets $11.8m | same entity; share of income $139.0m, of end-of-year assets $1,063.9m |
| Governance (Schedule O) | Articles amended 2023-11-01 to change the name from Further Future Foundation to Navigation Charitable Fund. No conflict-of-interest, whistleblower or retention policy in 2023 (adopted 2024). Audit planned for November 2024 | Board of 3; conflict-of-interest procedure described |
| Part III program text | "$375,000 … 5 nonprofit organizations … climate change"; "$1.6 million … 14 … criminal justice"; "$2 million … 17 … farm animal welfare" | $14.24m to Humane America and $15.375m to Vanguard Charitable, each "along with non-binding recommendations to fund organizations…"; $6.03m across three digital-sentience organisations, including "an endowment for a new program area at NYU" |

**Reading [I]**
- **What it is.** A newly formed (2022) grantmaking public charity. In its first year it received a single $1.309bn cash grant from SVCF, which met its 170(b)(1)(A)(vi) public-support test under the first-five-years rule. Its website names its founding donor: "With an initial gift from Jed McCaleb, our co-founders Seemay Chou and David Coman-Hidy set out to create a different kind of grantmaking organization" ([navigation.org/about](https://www.navigation.org/about), read 2026-11-19) [P]. That the SVCF grant is this gift, made through a McCaleb-advised fund, is an inference: SVCF does not publish its fund holders.
- **Sponsor or controlling relationship.**
  - SVCF is not a related organisation of the fund, and neither return lists the other on Schedule R.
  - The fund in turn **controls a for-profit**, Voltage Park Inc, holding 100% of its equity. Voltage Park holds two-thirds of the fund's assets ($883.5m book). Its Schedule R share of assets rose from $11.8m to $1,063.9m in 2024.
  - The fund's filings do not explain the investment, but its About page does: “The Navigation Fund’s founding endowment was provided by Jed McCaleb … We've made strategic investments, including in Lightning AI (formerly Voltage Park), with the goal of achieving strong financial returns that enable us to do more through our grantmaking. At this time, we do not do impact investing” (navigation.org/about, read 2026-11-19) [P] [V wave 36B] "Cloud infrastructure" is the only description filed.
- **What it did with the money.**
  - By end-2024 it had paid $41.1m in grants (3.1%) and held $883.5m in Voltage Park and $405.0m in cash and short-term investments.
  - $17.1m of the grants (42% of grants paid) went to **Vanguard Charitable**, a national DAF sponsor, with "non-binding recommendations". That is a DAF-to-DAF-style movement one step removed.
  - The fund's website reports grants "over $60 million annually" and "217 organizations in 2025". FY2025 filings are not yet available to check this.
- **For the exception-load proxy.** The SVCF line is a single DAF-scale transfer into a new charity that mostly held the money as for-profit equity and cash in 2023–24. Flagging it as a "recent ruling" (BMF ruling 2023-03, foundation code 15) is correct. Its weight in SVCF's sponsor-level share (45.8% broad) reflects one transaction, not a pattern of review load.

## 5. Limits
- **Snapshots.** Pub 78 and the BMF date from 2026-11. An organisation listed at grant time and dropped since will not match, and a newly listed one under a new EIN can produce a false "misreport".
- **The line cache holds state only.** There is no city or ZIP, so same-state duplicates (e.g. several Sacred Heart schools) cannot be told apart. This is why tier A has 4 unsure keys of 21.
- **Recall is not measured.** Brand-name versus legal-name misses ("Fidelity Charitable", "LISC", "UNC Greensboro") and truncated BMF names reduce it. The misreport estimate is a floor on the identifiable share, not on the true share.
- **Hand check.** One reviewer, name and state only, no outside lookups. 40 keys sampled by key, not by dollars. Tier-level precision is the robust result. The pooled 51% depends on the tier mix of the sample.
- **Extended name rules are inference.** Some public or religious names may be mislabelled (e.g. RONCALLI CATHOLIC SCHOOLS fell into the public-body class because of SCHOOLS). These classes are "plausibly legitimately absent", not verified.
- **Community-foundation Schedule I includes non-DAF grants.**
- **Navigation Charitable Fund.** Its two Forms 990 are self-reported and unaudited for 2023; the 2023 audit was planned for November 2024. The fund's Schedule R asset share for Voltage Park ($11.8m) does not match the $883.5m book value of the same holding in TY2023, and the filings do not reconcile them. The fund's About page names the holding “Lightning AI (formerly Voltage Park)” and calls it a strategic investment made “with the goal of achieving strong financial returns” [P]; neither the page nor the filings describe its business further [V wave 36B] Nothing here says what Voltage Park does beyond "cloud infrastructure".
- **Blocked or missing:**
  - **Voltage Park's own disclosures** were not read. It is a private C corporation with no Form 990.
  - **SVCF fund-level data** is not public.
  - **FY2025 Forms 990** for the Navigation fund are not yet in the IRS index.
  - **Withheld names.** Blank-EIN names that may be individuals are withheld from the CSV.

## 6. Reproduction
```
python3 scripts/mission_unlisted_recipients.py . --np-cache NPCACHE --lines-cache LINES --bmf-dir BMF \
    --pub78 data-download-pub78.txt --revocation data-download-revocation.txt [--out PATH]
```
- The inputs are those of `mission_recipient_compliance.py` / `mission_exception_load.py`: the `netpayout990/` cache, the P-NEW-REC-01 line cache, BMF eo1–eo4/eo_pr/eo_xx, and the unzipped Pub 78 and revocation files. The leading `.` is accepted for the repo's CLI convention and is unused.
- The script writes the CSV and prints a JSON summary: the pools as briefed, the dropped totals rows, the class table, hand-check precision by tier and pool, the 40 sampled pairs, and the top matched, unmatched and ambiguous keys. Every figure in §0–§3 comes from that output.
- Part B figures were read directly from the e-file XMLs listed in §8. The Greater Horizons arithmetic (named-row sum, row positions) was recomputed with a stdlib one-off over the XML and agrees with the line cache.
- Run time is about 80 s.

## 7. Data dictionary: `unlisted-recipients-resolution-2026-11-19.csv`
| Column | Meaning |
|---|---|
| row_type | `summary` (one row per pool × resolution, plus `ALL` and `matched_tier_A/B/C`) or `recipient` (one key) |
| pool | `ein_unlisted` (EIN in neither Pub 78 nor BMF, no explaining label) or `blank_ein` (blank or placeholder EIN, totals rows removed) |
| key | pool \| filed EIN \| sorted normalised tokens \| state. For withheld blank-EIN keys, `blank_ein\|withheld\|` plus 16 hex digits of SHA-1 |
| filed_ein, filed_name, filed_state | As filed on Schedule I. The state is the US state, or `F:` + country. The name is blank when `name_withheld = 1` |
| name_withheld | 1 for blank-EIN keys without a listed match (possible individuals; §1.8) |
| lines, usd, n_sponsors, sponsors, fiscal_years | Lines and cash + non-cash dollars pooled over FY2023–24; number of grantor sponsors and the first five names; DAFRC fiscal years |
| d2d_line | 1 if any line is DAF-to-DAF under the batch-34 whitelist |
| resolution | Class (§1.5) |
| match_tier, match_score, match_n_best | Tier A/B/C; Jaccard score; number of tied EINs at the best level (1 = unique). The score is 0 when no candidate reached 0.80 |
| matched_ein, matched_name, matched_state, matched_city, matched_source, matched_pub78_codes, matched_bmf_subsection | Best reference record (Pub 78 name preferred); source `bmf`, `pub78` or both |
| ein_digit_distance, ein_typo_like | Unlisted-EIN pool: `transposition` or Hamming distance between filed and matched EIN; 1 if transposition or ≤ 2 digits |
| filed_ein_revocation_name | Name on the most recent revocation record for the filed EIN, if any |
| handcheck_sample, handcheck_verdict, handcheck_note | 1 for the 40 sampled keys; reviewer verdict (`correct`/`wrong`/`unsure`) and reason [H] |
| keys, typo_like_keys, typo_like_usd | Summary rows: key count; typo-like keys and dollars |
| source | Provenance |

## 8. Source register
| ID | Source | Version / access | robots.txt |
|---|---|---|---|
| S1 | Top-50 Schedule I Part II lines, FY2023–24: IRS e-file XML ([IRS Form 990 series downloads](https://www.irs.gov/charities-non-profits/form-990-series-downloads)) via the GivingTuesday mirror of IRS TEOS; P-NEW-REC-01 line cache | 94 returns | mirror `robots.txt` → HTTP 404 (no rules), re-checked 2026-11-19 20:08 UTC |
| S2 | SVCF FY2023 Form 990: [202413129349304911_public.xml](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202413129349304911_public.xml) | fetched 2026-11-19, 3,063,731 bytes | as S1 |
| S3 | Greater Horizons FY2024 Form 990: [202513189349309621_public.xml](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513189349309621_public.xml) | scratch copy from the same mirror (2026-11-14) | as S1 |
| S4 | Navigation Charitable Fund TY2023 Form 990: [202433209349325783_public.xml](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202433209349325783_public.xml); TY2024: [202513009349302251_public.xml](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513009349302251_public.xml); object ids from the IRS TEOS index files index_2024.csv and index_2025.csv ([IRS Form 990 series downloads](https://www.irs.gov/charities-non-profits/form-990-series-downloads)) | fetched 2026-11-19 (34,935 and 57,651 bytes) | as S1 |
| S5 | [IRS Pub 78 data](https://apps.irs.gov/pub/epostcard/data-download-pub78.zip) | Last-Modified 2026-11-11 (verified in P-NEW-REC-01) | apps.irs.gov robots → 404 (per P-NEW-REC-01; not re-fetched) |
| S6 | [IRS EO BMF](https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf): [eo1.csv](https://www.irs.gov/pub/irs-soi/eo1.csv)–eo4, eo_pr, eo_xx | Last-Modified 2026-11-09 | `/pub/` not disallowed (per P-GAP19-05; not re-fetched) |
| S7 | [IRS Auto-Revocation List](https://apps.irs.gov/pub/epostcard/data-download-revocation.zip) | Last-Modified 2026-11-11 | as S5 |
| S8 | [The Navigation Fund, About](https://www.navigation.org/about) (and the [home page](https://www.navigation.org/)) | HTTP 200, 2026-11-19 | `robots.txt` → 200, only a `Sitemap:` line (no disallow rules) |
| S9 | Repo: [direction-recipient-compliance-screen.md](direction-recipient-compliance-screen.md); [gap19-exception-load-proxy.md](gap19-exception-load-proxy.md); [b40n1202-b43n26-recipient-basis-and-rating-eligibility.md](b40n1202-b43n26-recipient-basis-and-rating-eligibility.md); DAFRC panel; `daf-to-daf-recipient-whitelist.csv` | repo | n/a |

No crt.sh, certspotter or sec.gov was used. There was no outreach, login or form submission, and requests used the generic user agent `research-script/1.0`.
