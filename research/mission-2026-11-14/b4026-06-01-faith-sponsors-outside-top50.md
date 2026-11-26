# Faith sponsors outside the top 50: how much they add to church DAF dollars (P-B4026-06-01)

**Date:** 2026-11-20 · **Task ID:** b4026-06-01 · **Builds on:** [b4026-06-church-daf-recipients.md](b4026-06-church-daf-recipients.md) with its wave-35C corrections ([validation-wave35c-report.md](validation-wave35c-report.md)); [b40n1202-01-non-top50-numerator.md](b40n1202-01-non-top50-numerator.md) (all-panel line cache and weight rule)

**Outputs**
- Script: [`scripts/mission_faith_sponsors_outside.py`](../../scripts/mission_faith_sponsors_outside.py). It is new. It imports `mission_church_recipients.py`, `mission_recipient_basis_eligibility.py` and `mission_non_top50_numerator.py` and modifies none of them.
- Data: [`data/mission-2026-11-14/faith-sponsors-church-dollars-2026-11-20.csv`](../../data/mission-2026-11-14/faith-sponsors-church-dollars-2026-11-20.csv). 3,245 rows in long format (§6).
- Queue proposals: [`data/mission-2026-11-14/queue-proposals-b4026-06-01.csv`](../../data/mission-2026-11-14/queue-proposals-b4026-06-01.csv), 4 rows.

Tags: **[F]** computed by the script from filings, the BMF or the DAFRC dataset · **[P]** quoted primary source · **[I]** inference.

## 0. Answer in brief

- **The base reproduces exactly.** In scenario S0 (top 50 only) the block is 29,469 recipients and $6,177,546,936, with a faith share of 22.10%. The congregation share is 21.18% and the share across all church-coded recipients 25.72%. Nationals send 74.22% [F].
- **Faith sponsors outside the top 50 add $1,080.3m to the church block.** That is +17.5% on the base block's $6,177.5m [F].
  - **Panel sponsors supply almost all of it: $1,079.6m from 149 DAFRC panel faith sponsors.** The 3 non-panel sponsors with block lines add $0.7m (S2).
  - The added dollars go to 1,934 church-block recipients that no top-50 sponsor paid, as well as to existing block churches. The block becomes 31,403 recipients and $7,257.8m [F].
- **It is concentrated.** One sponsor, the OJC Fund (Brooklyn; DAFRC "Religiously-Affiliated"), sends $545.3m, half of the addition. 76.4% of its own DAF-weighted dollars go to the block. Every block recipient is church-status in the BMF (FOUNDATION 10; filing-requirement code 06 for 99.6% of the dollars), but by name only about two-fifths of its block dollars go to congregations: 38.9% on filed Schedule I names, 41.6% on BMF names, 44.7% under this study’s own rules. On filed names, 25.9% go to yeshivas and schools, 16.5% to chesed or relief funds, 1.5% to communal umbrella bodies and 17.2% to names the rule cannot type. Its lines are not pass-throughs: 0.30% of its Schedule I dollars go to DAF sponsors, other DAFRC panel members or federations, none of them in the block (b4026-0601-01-p0503-ojc-groundswell.md) [V wave 43B] Next come:
  - The Signatry Charitable Trust, $152.3m (the Servant Foundation's sister trust, added by the name rule);
  - CCF-LA Supporting Organization, $139.6m (of which $75.9m goes to the Roman Catholic Archbishop of Los Angeles; the Archbishop's $103.7m total from faith sponsors outside the top 50 also includes about $27.8m, mostly from Catholic Community Foundation of Los Angeles) [V wave 42B];
  - Catholic Community Foundation of Los Angeles (EIN 383941057, the one supported organisation of CCF-LA Supporting Organization), $33.5m [V wave 42B];
  - **WaterStone / Christian Community Foundation, $27.8m**;
  - Knights of Columbus Charitable Fund, $15.5m;
  - Christian Community Foundation of Memphis, $15.4m;
  - **Catholic Community Foundation of Minnesota, $15.2m** [F].
- **The named NCF affiliates add almost nothing as DAF sponsors.** NCF Wisconsin and NCF Real Property are not in the DAFRC panel. Their FY2023–24 Form 990s report no DAF grants on Schedule D, and the FY2024 returns read by hand answer "No" to Part IV line 6 (`DonorAdvisedFundInd` 0). Their DAF activity is therefore reported by NCF itself (EIN 581493949), which is already in the top 50. NCF Supporting Organization (a panel member) sends $29.5k to the block. Of 474 non-panel faith-named candidates with a FY2023–24 Form 990, only 4 report Schedule D DAF grants above zero [F].
- **Re-estimated faith share of church-block DAF dollars** [F]:

  | Scenario | Block $m | Faith share | Congregations | All church-coded | Nationals' share of block |
  |---|---|---|---|---|---|
  | S0 top 50 (base) | 6,177.5 | 22.1% | 21.2% | 25.7% | 74.2% |
  | S2 top 50 + all faith sponsors outside it | 7,257.8 | **33.7%** | 29.7% | 35.7% | 63.2% |
  | S3 all panel sponsors + non-panel faith (like-for-like) | 8,104.5 | **30.2%** | 26.6% | 31.8% | 58.8% |

  - S2 is the task's definition: the top 50 plus faith sponsors outside it.
  - S3 is the fair comparison. It adds every non-top-50 panel sponsor, faith or not, so community foundations and smaller nationals are counted too.
  - **Central estimate: about 30% of church-block DAF dollars come from faith sponsors (S3), against 22% in the base.** The task-defined figure is 34%. Without the OJC Fund the figures are 25.1% (S3) and 28.3% (S2) [F]. These are sensitivities, not a new central figure, because the block is defined by church status and every OJC recipient has it. Keeping only the OJC Fund’s congregation-named recipients gives 27.3% (S3) and 30.7% (S2); dropping only its yeshiva and chesed-fund lines gives 28.2% and 31.6%. A congregations-only filter applied to every sponsor gives 23.0% (S3) and 25.8% (S2) (b4026-0601-01-p0503-ojc-groundswell.md) [V wave 43B]
- **"Nationals send about three-quarters" no longer holds outside the top-50 frame.** National sponsors' block dollars barely change ($4,584.9m in S0, $4,767.6m in S3), but the denominator grows, so their share falls:
  - from 74.2% to 63.2% (S2) and 58.8% (S3);
  - for congregations, from 76.1% to 67.8% (S2) and 62.4% (S3).
  - **"About three-fifths" is the defensible all-panel statement.** Without the OJC Fund it is 63.1% in S3, between three-fifths and two-thirds [F]. Two national sponsors that do not itemise Schedule I (BofA Charitable Gift Fund, Renaissance) are absent from every scenario, so all national shares are understated by an unknown amount [V wave 42B].

## 1. Method

1. **Base and frame.**
   - The base is reproduced from the same caches by importing the base study's functions:
     - `mission_church_recipients`: the block constant, Outreach 100 parsing and matching, and the recipient-type name rules;
     - `mission_recipient_basis_eligibility`: `units_b` (Charity Navigator rule order), `load_history` (IRS TEOS index 2019–2026) and `load_bmf_extra`;
     - `mission_non_top50_numerator`: `sponsor_years` and `weight_fallback`.
   - The block rule is unchanged: in the BMF, SUBSECTION 03, FOUNDATION 10, not a private foundation, not a national or processor panel sponsor, and no 990/990-EZ/990-PF in the index. The rule is applied to the union of recipient EINs across all sponsors read, which holds 37,426 church-coded EINs, 35,587 of them in the block.
2. **Sponsor tiers and line sources.**
   - **top50**: 94 sponsor-years from the committed `rcp/lines` cache.
   - **panel_other**: all 2,611 itemising non-top-50 panel sponsor-years from `q120201/lines` (b40n1202-01). They were read from the cache only; there was no re-fetch.
   - **nonpanel_faith**: see 4.
3. **Faith sponsors in the panel (systematic).**
   - The rule is DAFRC 2025 subtype "Religiously-Affiliated" (192 sponsors beyond the base study's seven), plus National or Community Foundation panel sponsors whose name matches a faith word list. That list is CHRISTIAN, CATHOLIC, JEWISH, SIGNATRY, SERVANT FOUNDATION, LUTHERAN, METHODIST, BAPTIST, PRESBYTERIAN, EPISCOPAL, MUSLIM, ISLAMIC, ARCHDIOCESE and DIOCESE.
   - The name rule adds Servant Foundation (as in the base), The Signatry Charitable Trust and The Catholic Foundation of North Georgia.
   - Single-issue sponsors are left to the DAFRC subtype, so universities, hospitals and a YMCA camp with "Christian" in its name are not swept in.
   - 194 faith panel sponsors lie outside the top 50; 172 of them have itemised lines (340 sponsor-years).
   - Each faith sponsor is labelled christian, catholic, jewish or other_faith from its name. The base study's seven keep their base labels.
4. **Faith sponsors outside the panel (systematic).**
   - **Candidates.** 1,289 BMF 501(c)(3) EINs not in the panel whose names match NCF-affiliate, Christian/Catholic/Jewish foundation or federation, UJA, or denominational-foundation patterns. Hospital, medical, health, college, school, home and similar names are excluded (`FAITH_NONPANEL_RX`, `NONPANEL_EXCLUDE_RX`).
   - **Returns.** 474 candidates have a FY2023 or FY2024 Form 990 (DLN 93493) in the TEOS index: 919 returns, choosing the latest object id per period and the latest period per fiscal year.
   - Each return was read with the repo's own extractor (`mission_net_payout.fetch_extract`) from the GivingTuesday mirror; all 919 returned `ok`.
   - **Kept.** A sponsor-year is kept if Schedule D reports DAF grants above zero and Schedule I is itemised. Its lines were then read with `load_lines`. This kept 5 sponsor-years at 4 sponsors.
5. **DAF weighting.**
   - The rule is b40n1202-01's: the `sponsor-cost-structure.csv` DAF share of grants, capped to [0, 1]; otherwise Schedule D DAF grants ÷ Part IX line 1, capped; otherwise 1.
   - All top-50 weights equal the base's, since S0 reproduces to the dollar. All 5 non-panel sponsor-years use the Schedule D ratio.
6. **DAF-to-DAF netting.**
   - As in the base, `annotate` drops lines to the grantor itself and to whitelisted DAF sponsors (by EIN, or by unique name for blank-EIN lines).
   - Extension: in scenarios that include the non-panel tier, lines to the 4 kept non-panel sponsors are also netted. Church recipients are never sponsors, so netting changes frame totals, not block dollars.
7. **Recipient type.** The base's name rules apply, with the Outreach 100 override (cached 2023/2024 lists in `q2606/outreach`), re-matched in each scenario.
8. **Scenarios.**
   - S0: top 50 only.
   - S1: top 50 + panel faith sponsors outside it.
   - S2: S1 + non-panel faith sponsors.
   - S3p: all panel sponsors.
   - S3: S3p + non-panel faith sponsors.
   - Sensitivities that drop one sponsor (the OJC Fund) or the name-rule sponsors are exact. Lines are additive, so removing a sponsor removes exactly its block dollars from both numerator and denominator.

**Run.**

```
S=<scratchpad>; Q=$S/q2661
python3 scripts/mission_faith_sponsors_outside.py . --np-cache $S/npcache --lines-cache-top50 $S/rcp/lines \
    --lines-cache $S/q120201/lines --bmf-dir $S/rcp/bmf --index-dir $S/irs --outreach-dir $S/q2606/outreach \
    --work $Q [--fetch]
```

- `--fetch` was used once, to read the non-panel returns into `$Q/netpayout990` and `$Q/lines`. The committed CSV comes from a later cache-only run. A second cache-only run produced a byte-identical CSV (md5 e497f4ac…).
- stdout is a JSON diagnostic: candidate funnel, extract status, weight sources and per-scenario headline figures.
- **Requests.**
  - gt990datalake-rawdata.s3.amazonaws.com: robots.txt returned 404 (no restriction) at 2026-11-20T01:16:46Z, logged in `$Q/robots/log.tsv`. After that, 919 + 5 + 5 return reads.
  - 3 raw XMLs were saved to `$Q/xml/` to check the Schedule D reading by hand (NCF Wisconsin, UJA-Federation of New York, NCF Real Property).
  - No other host was contacted.

## 2. Results

### 2.1 Added dollars to the church block (S2 against S0) [F]

| | Recipients | Block $m (DAF-weighted, FY2023–24) |
|---|---|---|
| Base block (top 50) | 29,469 | 6,177.5 |
| + panel faith sponsors outside top 50 (149 with block lines) | +1,931 new | +1,079.6 |
| + non-panel faith sponsors (3 with block lines) | +3 new | +0.7 |
| **Block with all faith sponsors** | **31,403** | **7,257.8** |

**By faith kind (added $m):** Jewish 613.2 (the OJC Fund 545.3); Christian 375.3; Catholic 91.0; Muslim 0.7. The CCF-LA Supporting Organization is labelled Christian by name, but it is Catholic on its own Form 990: a Type II supporting organisation of Catholic Community Foundation of Los Angeles (EIN 383941057) whose mission is “donor advised fund granting to charities with Catholic values”. It holds one DAF account. Its largest recipient is the Archdiocese of Los Angeles ($24.0m in FY2023 and $51.9m in FY2024, $75.9m in all). Relabelled Catholic, the Catholic figure is $230.6m and the Christian $235.7m [V wave 42B]. This changes only the split, not the faith total.

**By faith rule:** DAFRC subtype $926.0m; name rule $153.6m (almost all the Signatry Charitable Trust); non-panel BMF name plus Schedule D $0.7m.

**By recipient type (base name rules, added $m):** congregation 391.2; unclassified 218.6; ministry/order 172.8; denominational body 153.5; school/seminary 144.2. The added dollars lean less toward congregations (36%) than the base block does (52%) [F].

**Named sponsors from the task** [F]:

| Sponsor | Status | Block $m | Recipients | Share of own $ to block |
|---|---|---|---|---|
| WaterStone / Christian Community Foundation (751750059) | panel, DAFRC religious | 27.8 | 411 | 14.3% |
| Catholic Community Foundation of Minnesota (411744184) | panel, DAFRC religious | 15.2 | 78 | 31.9% |
| NCF Supporting Organization (474168487) | panel, DAFRC religious | 0.03 | 1 | — |
| NCF Wisconsin (311733328) | not in panel; 990s show no DAFs | 0 | — | — |
| NCF Real Property (582655939) | not in panel; 990s show no DAFs | 0 | — | — |
| Other Jewish community foundations and federations in the panel (outside top 50, excluding OJC) | panel, DAFRC religious | 67.3 | — | 3–13% each for the larger ones |
| UJA-Federation of New York (510172429) | not in panel; Part IV line 6 is Yes, but Schedule D column (a), donor advised funds, is empty and all its accounts sit in column (b) [V wave 42B] "funds and other accounts" only (18 accounts, $0.9m grants FY2024) | 0 | — | — |

**Largest recipients of the added faith dollars:** the Roman Catholic Archbishop of Los Angeles ($103.7m); Come and See Foundation ($53.9m, mostly from the Signatry Trust); World Literature Crusade ($47.0m); YouVersion ($18.0m); the USCCB Phoenix unit ($16.1m); then a run of Brooklyn and Monsey Orthodox bodies from the OJC Fund, such as Keren Mugein Imoisheya ($14.1m) and Congregation Chonen Vnosen ($12.4m). The top 30 are in `block:top_recipient_outside_faith` [F].

### 2.2 Re-estimated faith share [F]

| Scope | S0 | S1 | S2 | S3p | S3 |
|---|---|---|---|---|---|
| Block | 22.1% | 33.7% | 33.7% | 30.2% | 30.2% |
| Block congregations | 21.2% | 29.7% | 29.7% | 26.6% | 26.6% |
| All church-coded (FOUNDATION 10) | 25.7% | 35.7% | 35.7% | 31.8% | 31.8% |
| Faith sponsors' share of all frame dollars | 10.0% | 14.1% | 14.1% | 11.7% | 11.7% |

- Faith over-representation in the block (block share ÷ frame share) is 2.2× in S0, 2.4× in S2 and 2.6× in S3.

**Sensitivities (exact, by sponsor removal):**

| | S2 faith share | S2 nationals | S3 faith share | S3 nationals |
|---|---|---|---|---|
| central | 33.7% | 63.2% | 30.2% | 58.8% |
| without name-rule sponsors (Signatry Trust, Catholic Fdn N. Georgia) | 32.3% | 64.5% | 28.8% | 60.0% |
| without the OJC Fund | 28.3% | 68.3% | 25.1% | 63.1% |
| without both | 26.6% | 69.9% | 23.6% | 64.4% |

### 2.3 What happens to "nationals send about three-quarters" [F]

- National sponsors (DAFRC National, excluding the Servant Foundation and the Signatry Trust) send $4,584.9m to the block in S0. Adding non-top-50 nationals raises that to $4,767.6m in S3.
- Their share falls from 74.2% to 63.2% (S2) and 58.8% (S3), because faith sponsors (+$1,080m) and non-top-50 community foundations and other sponsors (+$664m in S3) enlarge the block.
- **Fidelity Charitable is still the largest single source.** Its $2,157.9m is 26.6% of the S3 block, against 34.9% in the base.
- **Statement for reuse:** "Across all DAFRC panel sponsors, national sponsors send about three-fifths of church-block DAF dollars (58.8%), faith sponsors about 30%, and community foundations and others about 11%. Within the top-50 frame the national share is 74%."
- The base study's E3 reading changes from "explains about a fifth to a quarter" to **about three-tenths** (30.2% of block dollars, 31.8% of church-coded dollars, all panel sponsors). The conclusion that most church DAF dollars arrive from non-faith sponsors still holds, at about 70% [I].

## 3. Limits

1. **Concentration.** Half the addition is one sponsor (the OJC Fund). Its weight (DAF share of grants, 0.99 in FY2023–24 cost-structure rows) and its line amounts are taken as filed. Re-read: its FY2023 and FY2024 Form 990s (years ending June) answer Yes to Part IV line 6 and report 4,731 and 5,976 DAFs, DAF grants of $338.3m and $385.7m against total grants of $338.9m and $390.7m (weights 0.998 and 0.987), and year-end DAF assets of only $42.5m and $34.5m. Its Schedule I line counts (3,009 and 3,410) match the cache. It is a pass-through sponsor, 22nd by FY2023 DAF grants in the DAFRC panel but 284th by DAF assets, which is why an assets-ranked top 50 omits it [V wave 42B]. Any error in its Schedule I moves the faith share by up to about 5 points. An audit of all 6,419 lines (b4026-0601-01-p0503-ojc-groundswell.md) finds no pass-through to DAF sponsors or federations in the block. But 42.4% of its block dollars go to yeshiva/school and chesed-fund names on filed names (41.3% on BMF names). About 7.4% of its FY2023–24 DAF contributions arrive as grants from other panel sponsors, mainly PayPal Charitable Giving Fund ($44.4m); reattributing that share lowers the S3 faith share from 30.2% to 29.7% [V wave 43B]
2. **Non-panel coverage.** The non-panel search uses names. A faith DAF sponsor without a faith word in its name (for example "Eder Deferred Gifts" or "Ten Talents") is found only if DAFRC lists it.
   - Candidates are kept only on their own Schedule D. Organisations that run DAFs through a separately incorporated foundation (UJA-Federation, Jewish United Fund Chicago, NCF affiliates) are counted where that foundation files, which is usually NCF or a panel foundation.
   - 815 candidates had no FY2023–24 Form 990 in the index (990-EZ, 990-PF, paper filers or no filing) and were not read.
3. **Sponsor-level DAF weighting** is applied pro rata to all of a sponsor's lines, as in the base. Federations and Catholic foundations also make discretionary grants. If their DAF grants go to churches at a different rate than their other grants, their contribution is misstated.
4. **Faith-kind labels are name-based.** The CCF-LA Catholic reading is an inference (§2.1).
5. **No unitemised money.** Grants of $5,000 or less per recipient-year, and sponsors that file Schedule I as an attachment (BofA Charitable Gift Fund, Renaissance), are outside every scenario, as in the base and b40n1202-01. Congregations get many small grants, so all church-block totals are floors.
6. **Recipient types and the block rule** inherit every caveat of the base and wave 35C (name-rule classification, FOUNDATION 10 includes non-congregations, the 2026-11 BMF applied to FY2023–24).
7. **Double counting across tiers.** Top-50 grants to non-panel faith sponsors (for example Fidelity to a federation) are not netted in S0–S1. They never reach the church block directly, so block dollars are unaffected.

## 4. How this updates the base study (suggested wording, not applied)

- b4026-06 §3.5 "Answer to the faith-versus-other question": the faith share of church-block DAF dollars rises from 22.1% (top 50) to 30.2% across all DAFRC panel sponsors (33.7% counting only faith sponsors outside the top 50; 25.1% without the OJC Fund). Nationals' share falls from 74.2% to 58.8% (b4026-06-01).
- b4026-06 §4 E3: "about a fifth to a quarter" should become "about three-tenths across all panel sponsors; about a fifth to a quarter within the top 50".
- The wave-35C insertions that quote "nationals send 74.2%" (the faith-platforms doc and industry report §11.38) should add "within the top-50 frame; 58.8% across all panel sponsors".

## 5. Source register

| # | Source | Accessed | Used for | Tag |
|---|---|---|---|---|
| S1 | IRS Form 990 Schedule I Part II and Schedule D Part I, FY2023–24 e-file XML via the GivingTuesday mirror of IRS TEOS, e.g. https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503219349322400_public.xml (NCF Wisconsin FY2024); index https://apps.irs.gov/pub/epostcard/990/xml/2024/index_2024.csv | 2026-11-20 (non-panel); caches 2026-11-14/19 (panel) | lines, DAF grants, DAF indicator | F |
| S2 | DAFRC Annual DAF Report 2025, Updated Analysis dataset, https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx (repo copy `dafrc-sponsor-schedule-d-fy2019-2024.csv`) | repo | panel, type and subtype ("Religiously-Affiliated") | F |
| S3 | IRS EO BMF extract, https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf (repo cache `rcp/bmf`) | 2026-11-14 | church status, candidate names, city and state | F |
| S4 | IRS EO BMF data dictionary, https://www.irs.gov/pub/foia/ig/tege/eo-info.pdf | via base study | FOUNDATION 10 definition | P |
| S5 | IRS Instructions for Form 990 Schedule D, https://www.irs.gov/instructions/i990sd (Part I: column (a) donor advised funds, column (b) funds and other accounts) | not fetched in this task; the column split is read from the XML element names (`DonorAdvisedFunds*` against `FundsAndOtherAccounts*`) | reading UJA-Federation's Schedule D | P |
| S6 | Outreach 100 2023/2024 lists, https://outreach100.com/largest-churches-in-america/2023 and /2024 (cached by b4026-06) | 2026-11-19 | congregation override | P |
| S7 | `sponsor-cost-structure.csv` (repo) | repo | DAF weights | F |
| S8 | b4026-06, validation-wave35c-report, b40n1202-01 (repo) | repo | base figures and method | R |

## 6. Data dictionary: `faith-sponsors-church-dollars-2026-11-20.csv`

| Column | Meaning |
|---|---|
| `section` | `<scope>:<table>` or `sponsor_register`. Scopes are `block` (`no_efiled_990_church`), `block_congregations` (block ∩ type congregation), `church_coded_all` (all FOUNDATION 10 recipients) and `frame`. Tables: `summary`, `sponsor_group`, `sponsor_tier`, `sponsor`, `rtype_x_faith`, `top_recipient_outside_faith` |
| `scenario` | S0_top50, S1_top50_plus_panel_faith, S2_top50_plus_all_faith, S3p_all_panel, S3_all_panel_plus_nonpanel_faith (blank for `sponsor_register`) |
| `key` | Statistic name, sponsor group, tier, sponsor EIN, recipient EIN, or `rtype\|faith flag\|tier` |
| `label` | Sponsor DAFRC or BMF name, or recipient BMF name |
| `detail` | Sponsor: the faith rule that admitted it. Register: DAFRC type/subtype, or city, state and BMF FOUNDATION. Top recipient: city, state and type |
| `tier` | top50, panel_other, nonpanel_faith (register: nonpanel_candidate) |
| `sponsor_group` | faith_christian, faith_catholic, faith_jewish, faith_other_faith, national, community_foundation, other |
| `recipients`, `lines` | Distinct recipients; Schedule I lines (sponsor-year × recipient) |
| `usd_daf_weighted` | FY2023–24 DAF-weighted, non-DAF-to-DAF Schedule I dollars, rounded. For `summary:faith_share` it is the faith dollars |
| `usd_schedule_i` | The same before weighting (summary rows only) |
| `share` | Share of the scope's DAF-weighted dollars |
| `value` | The statistic. summary: as named. sponsor_group/tier: share of scope. sponsor: share of the sponsor's own scenario dollars going to the block. top_recipient: recipient's total block dollars. register: faith rule (panel) or candidate status (`kept`, `no_daf_grants_on_sched_d`) |
| `note` | Definition of `value`. Register: per-return object id, Schedule D DAF grants, weight and weight source |
| `source` | Primary sources |
