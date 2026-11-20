# Validation wave 48B: tail CF fund totals from Form 990 narratives, and rule F

**Date:** 2026-11-20 · **Validator:** validator wave 48B · **Register:** [`data/mission-2026-11-14/validation-register-wave48b.csv`](../../data/mission-2026-11-14/validation-register-wave48b.csv) (18 rows, V48B-01…18)

**Study validated:** [b45n33-02-01-01-fund-totals-from-990.md](b45n33-02-01-01-fund-totals-from-990.md), with [`fund-totals-from-990-2026-11-20.csv`](../../data/mission-2026-11-14/fund-totals-from-990-2026-11-20.csv) and [`scripts/mission_fund_totals_from_990.py`](../../scripts/mission_fund_totals_from_990.py). Reconciled against [b45n33-02-01-tail-cf-fund-counts.md](b45n33-02-01-tail-cf-fund-counts.md) (validated in wave 47A).

---

## 1. Method

- **Re-run.** The script and its two imported modules, plus the four input CSVs, were copied to a scratch root and run there with `python3 -B`, so nothing in the repository was written. It used the local caches of the GivingTuesday mirror: 187 `{object_id}.xml` directories plus the `get()`-style JSON caches. The CSV it wrote is byte-identical to the repo CSV, and the printed report is identical to the analyst's saved report.
- **Independent recounts.** These used my own code, not the study's parser:
  - the EIN-FY return index, rebuilt from the two harvest files;
  - a raw-text regex count of the narrative fields;
  - the parent element of every `Desc` field;
  - a recomputation of rule F for every row from opex, Schedule D DAFs, accounts and DAF assets;
  - all medians, the F ÷ A and F ÷ G counts, band-weighted medians, and the robustness rows.
- **Reading.** I read all 36 selected totals in their own XML context, using raw-text extraction that is independent of ElementTree. For the questionable cases I also read the FY2022 and FY2023 returns. I read a fresh random 30 of the 182 hits classed as non-totals (seed 48020; 10 of them overlap the study's 40). I ran two recall probes over all 1,913 returns.
- **Reconciliation.** I compared the 02-01 CSV and the 990 CSV CF by CF. I compared opex, fund totals and rule A against the whole frame, and I pooled the two samples, preferring the 990 value for the two overlapping CFs.
- **Network.** None. All XML came from the existing local caches of `gt990datalake-rawdata.s3.amazonaws.com` (robots.txt 404, as logged by the study). No hosts named in the robots or site-terms rules were touched.

## 2. Counts

| Result | n |
|---|---|
| Register rows | 18 |
| Confirmed | 14 |
| Partially confirmed | 4 |
| Contradicted | 0 |
| Unverifiable | 0 |
| Selected totals read in XML context | 36 of 36 (plus FY2022–23 returns for 6 CFs) |
| Non-total hits read (fresh sample) | 30, all correct exclusions |
| Exact corrections proposed | 14 (b45n33-02-01-01: 7; b45n33-02-01: 3; long-tail cost note: 2; FINAL-STATUS: 1; industry report: 1 new §11.72) |

## 3. Findings

### 3.1 Search, coverage and precision (V48B-01…06)
- **The headline counts are confirmed:** 1,913 returns, 24,831 fields, 284 hits (102 / 20 / 90 / 39 / 11 / 22 by class), 95 returns with a total, and 36 of 641 CFs (18 / 15 / 3 by band). The extension gives 40.
- **The field label is imprecise.**
  - Only 16,315 of the 24,831 fields are Part III (5,514) or Schedule O (10,801).
  - The other 8,516 are Part VIII/IX line descriptions: `OtherExpensesGrp`, `OtherRevenueMiscGrp` and `ProgramServiceRevenueGrp`. The bare `Desc` tag inside `IRS990` also matches them.
  - None of them yields a regex hit, so no result changes.
- **Precision of 35/36 is confirmed by reading every total.**
  - Northern Alleghenies' Schedule O gives Elk County CF "TOTAL OF 257 CHARITABLE FUNDS" and McKean County CF "TOTAL OF 81 FUNDS". The filer is the parent of both, so **338** is right. The same pattern holds in FY2022 (202 + 63) and FY2023 (209 + 73).
  - Billings' "OVER 50 FUNDS FOR CHARITIES" follows "WE MANAGE ENDOWMENT FUNDS FOR COMMUNITY 501(C)(3) ORGANIZATIONS". It most likely means agency funds, so excluding it is right.
- **Currency, not precision, is the weak point.**
  - **Stateline:** the FY2024 narrative ("166 funds in 2024 including 10 new funds … $880,028 … 385 donors … 145 grants to 70 agencies") repeats the FY2022 passage word for word with only the year changed. FY2023 says 169.
  - **Phelps County:** "approximately 100" is unchanged across FY2022–24.
  - **Luzerne:** "over 400" is unchanged across FY2022–24.
  - **Eau Claire:** it moves 220 → 360 → 330.
- **Missed totals.**
  - My 30 excluded hits were all correct exclusions.
  - The two recall probes found no total at any CF that lacks one. The first looked for "total number of funds … N" and "funds grew / increased / reached N". The second looked for N followed by up to six words and then "funds", with type words removed. Recall against other phrasings is still unmeasured.

### 3.2 Rule F, A and G (V48B-07…12)
- **Every rule-F figure is confirmed.** My recomputation matches every row.
  - Rule F: share 0.245, $4,500 per account (n = 31), 258 bps (n = 34).
  - Rule A: 0.178, $3,518, 203 bps. Rule G: 0.356, $6,707, 323 bps.
  - F > A at 24 of 34 (median F ÷ A 1.13), and F < G at 26 of 34 (median F ÷ G 0.70).
  - Band-weighted: 0.195, $4,035, 307 bps. The bootstrap CIs reproduce.
- **The stated-totals variant is confirmed.**
  - The robustness row keeps stated and approximate totals (n = 17) and gives 0.162. Stated totals alone (n = 15) also give 0.162; both medians fall on Wayne County, 64 ÷ 394.
  - The row label omits that the row also drops the one sum-of-types total.
- **The band skew is confirmed and is stronger than the note says.**
  - 17 of 34 CFs are in the $10–50m band, against 32% of the frame.
  - Within every band, the F set's median opex is above the frame's: $1.71m vs $1.55m, $0.63m vs $0.49m, and $0.67m vs $0.28m.
  - Band weighting therefore does not remove the size lean. The band-weighted per-account median ($4,035) is Stateline's value alone; with Stateline at 169 it becomes $3,963.
- **The Phelps County outlier is confirmed and explained.**
  - 38 Schedule D DAFs ÷ "approximately 100" gives 0.380, against an asset share of 0.005.
  - The DAF assets are $162,075, down from $348,379 in FY2022, so the rule-F cost ($163k) exceeds them: 10,073 bps.
  - Dropping Phelps leaves 0.241, $4,577 and 255 bps.
- **The sum-of-types CF (EIN 275098203) has a soft numerator.** Its narrative lists 42 DAFs plus 7 corporate advised funds, while Schedule D says 54. On the narrative counts its share would be 0.309–0.360 rather than 0.397. It has no account count, and the medians do not move.

### 3.3 Reconciling $4,500 with 02-01's $2,108 (V48B-13, 14)
- **Rule F per account is, in practice, whole-org opex per fund.** Schedule D DAFs equal screened accounts at 28 of 31 990 CFs and 12 of 13 02-01 CFs, so F per account = opex × (DAFs ÷ funds) ÷ accounts ≈ opex ÷ funds. The two medians are $4,398 and $2,108 per fund.
- **Why the two sets differ** [C]:

| | 02-01 web sample | 990-narrative set | Frame (tail CFs) |
|---|---|---|---|
| CFs (per account) | 15 (13) | 34 (31) | 641 |
| Median opex | $431k | $1,317k | $630k |
| Median total funds | 200 | 296.5 | – |
| Rule A per account, same CFs | $2,607 | $3,518 | $2,859 (n = 549) |
| Rule A bps, same CFs | 194 | 203 | 205 (n = 603) |
| Rule F per account, by band ($10–50m / $1–10m / <$1m) | $4,647 / $2,157 / $1,612 | $5,159 / $2,703 / $4,035 | – |
| Rule F per account, median (CI) | $2,108 ($1,612–$4,864) | $4,500 ($3,536–$5,215) | – |
| Rule F bps, median (CI) | 276 (144–352) | 258 (204–371) | – |

- **Three things drive the per-account gap. The study names only the first.**
  1. **Band mix.** The 990 set has 50% of its CFs at $10–50m, against 40% in 02-01 and 32% in the frame. On its own this is not enough: the band-weighted 990 value is still $4,035.
  2. **Selection on organisation size within bands.** CFs that write fund totals into Part III spend more than the frame, and much more under $1m: $670k against $281k in the frame and $179k in 02-01. All three under-$1m 990 CFs are mid-sized organisations with few DAF dollars.
  3. **Fragility of 02-01's median.** $2,108 is a single CF (CF of Northeast Iowa, 1,000 funds). It is the 7th of 13 values, and $4,647 sits two places above it. Its CI ($1,612–$4,864) covers most of the gap.
- **Per DAF dollar, the two sets agree.** They give 258 and 276 bps, and pooling them gives 261 bps (CI 203–335).
- **Pooled and scaled checks** [C/I]:
  - Pooling the two sets gives 47 CFs. On these, rule F is $4,036 per account (n = 42, CI $2,515–$4,956), or $3,694 band-weighted.
  - The per-CF F ÷ A median (1.13), applied to the frame's rule-A median ($2,859), gives about **$3.2k per account** [I].
- **Verdict on which figure the repo should carry:**
  - **Per DAF dollar:** about **258 bps**, from the 34-CF 990 set. Both samples support it.
  - **Share:** **0.245**. Rule A on the same CFs gives 0.178.
  - **Per account:** **$4,500** (n = 31; band-weighted $4,035). It should say that the set leans toward larger-opex CFs, so a frame-level value is probably lower, about $3.2k [I].
  - **02-01's $2,108** should be kept only as that 15-CF web sample's value. It is not a frame-wide figure.

## 4. Accept / modify / reject

| Claim | Verdict | Note |
|---|---|---|
| 1,913 returns; 284 hits; 102 all-funds in 95 returns | **Accept** | Byte-for-byte re-run and independent index |
| 24,831 Part III and Schedule O fields | **Modify** | 8,516 are Part VIII/IX labels; no hits from them |
| 36 of 641 CFs with a total (18 / 15 / 3) | **Accept** | |
| Precision 35/36; Northern Alleghenies 338; Billings excluded | **Accept** | All 36 read in context |
| 0 of 40 excluded hits missed | **Accept** | Fresh 30 also clean; recall probes clean |
| Rule F 0.245, $4,500, 258 bps | **Accept** | Every row recomputed |
| Rule A 0.178, $3,518, 203; rule G 0.356, $6,707, 323 | **Accept** | |
| F > A at 24 of 34 | **Accept** | F < G at 26 of 34 |
| Share F 0.162 on stated totals | **Accept** | Label should also say that the sum-of-types total is dropped |
| Band skew; band-weighted $4,035 | **Modify** | Also an opex skew within bands; the weighted median is one CF (Stateline, stale total) |
| Phelps County outlier (10,073 bps) | **Accept** | Its "approximately 100" is unchanged FY2022–24 |
| Per-account gap due to band lean | **Modify** | Within-band size selection and the fragile 02-01 median matter more |
| Per-dollar agreement (258 vs 276 bps) | **Accept** | |
| Stateline FY2024 total of 166 | **Modify** | Copied from FY2022; FY2023 says 169 |
| Sum-of-types share 0.397 | **Modify** | Narrative DAFs 42 (+7) vs Schedule D 54 |
| 02-01's $2,108 as the repo's rule-F per-account figure | **Reject as headline** | Keep as the 15-CF sample value; carry $4,500 (about $3.2k frame-scaled [I]) |

## 5. Blocked or not done
- **No fetches.** No XML was fetched; everything came from the existing caches. Validation therefore depends on those caches matching the mirror. One file came from the study's own cached fetch.
- **Recall is unmeasured.** Recall against an independent hand count of totals across all narratives was not measured. Only targeted probes were run.
- **No cross-source check.** Totals were not checked against websites or audits, so currency is judged only by comparing years within the filings.

## Exact corrections

### `research/mission-2026-11-14/b45n33-02-01-01-fund-totals-from-990.md`

**Find:** "24,831 Part III and Schedule O text fields."
**Replace with:** "24,831 text fields: 5,514 Part III, 10,801 Schedule O, and 8,516 Part VIII/IX line descriptions that the `Desc` tag also matches (none of these yields a hit). [V wave 48B]"

**Find:** "  - In all, 24,831 fields."
**Replace with:** "  - In all, 24,831 fields, of which 8,516 are Part VIII/IX line descriptions (`OtherExpensesGrp`, `OtherRevenueMiscGrp`, `ProgramServiceRevenueGrp`) caught by the bare `Desc` tag; none yields a hit, so the results are unaffected. [V wave 48B]"

**Find:** "The 990 set leans toward the $10–50m band (17 of 34), so its per-account costs are higher than the 02-01 sample's ($4,500 vs $2,108)."
**Replace with:** "The 990 set leans toward the $10–50m band (17 of 34) and, within every band, toward CFs with above-frame opex (median opex $1.32m, against $0.63m for the frame and $0.43m for the 02-01 set), so its per-account costs are higher than the 02-01 sample's ($4,500 vs $2,108); band weighting alone still leaves $4,035, and the 02-01 median is a single CF. [V wave 48B]"

**Find:** "Band-weighted: F $4,035, A $1,940, G $3,825."
**Replace with:** "Band-weighted: F $4,035, A $1,940, G $3,825. The repo carries $4,500 as the rule-F cost per account in place of 02-01’s $2,108 (n = 13, one CF at the median). Because this set’s median opex is about twice the frame’s, a frame-level value is probably lower: the per-CF F ÷ A median (1.13) on the frame’s rule-A median ($2,859) gives about $3.2k [I]. [V wave 48B]"

**Find:** "| Stated or approx totals only (drop lower bounds)"
**Replace with:** "| Stated or approx totals only (drop lower bounds and the one sum-of-types total) [V wave 48B]"

**Find:** "which suggests stale round numbers (P-B45N33-02-01-01-02)."
**Replace with:** "which suggests stale round numbers (P-B45N33-02-01-01-02). Phelps County’s ‘approximately 100’ is also unchanged in FY2022–24 while its DAF assets fell from $348k to $162k. Stateline’s FY2024 narrative repeats its FY2022 text word for word (166 funds, 10 new, $880,028 from 385 donors), and its FY2023 return says 169; using 169 moves only the band-weighted per-account median ($4,035 to $3,963). [V wave 48B]"

**Find:** "as Phelps County's 38 DAFs at 0.5% of assets suggest (P-B45N33-02-01-01-03)."
**Replace with:** "as Phelps County's 38 DAFs at 0.5% of assets suggest (P-B45N33-02-01-01-03). The sum-of-types CF lists 42 DAFs and 7 corporate advised funds against 54 on Schedule D, so its share (0.397) may be high by 0.04–0.09; it has no account count and does not move the medians. [V wave 48B]"

### `research/mission-2026-11-14/b45n33-02-01-tail-cf-fund-counts.md`

**Find:** "By band: **$4,647 / $2,157 / $1,612** (rule A $3,282 / $2,819 / $1,174)."
**Replace with:** "By band: **$4,647 / $2,157 / $1,612** (rule A $3,282 / $2,819 / $1,174). The $2,108 median is one CF (CF of Northeast Iowa, 1,000 funds), the 7th of 13 values with $4,647 two places above it. The 990-narrative pass (b45n33-02-01-01, n = 31) gives $4,500, and the repo carries that figure. [V wave 48B]"

**Find:** "- **Rule F is the whole-org cost per fund.** Its median is about $2,100 for tail CFs (IQR $1,600–$5,300)."
**Replace with:** "- **Rule F is the whole-org cost per fund.** Its median is about $2,100 for these 15 CFs (IQR $1,600–$5,300). On the 34 CFs with a 990-narrative total (b45n33-02-01-01) it is $4,398. The difference reflects this sample’s low opex: its median is $431k, against $630k for the frame. [V wave 48B]"

**Find:** "  - **About $2.1k per DAF account and about 280 bps of DAF assets** (sample medians; weighted medians identical), against rule A's $2.6k and 194 bps on the same CFs."
**Replace with:** "  - **About $2.1k per DAF account and about 280 bps of DAF assets** (sample medians; weighted medians identical), against rule A's $2.6k and 194 bps on the same CFs. The per-account figure is superseded by the 990-narrative pass (b45n33-02-01-01: $4,500 on n = 31, band-weighted $4,035, about $3.2k frame-scaled [I]); per DAF dollar the two agree (258 vs 276 bps). [V wave 48B]"

### `research/mission-2026-11-14/b45n33-long-tail-operating-cost.md`

**Find:** "The repo has no non-DAF fund counts to test this (P-B45N33-02-01)."
**Replace with:** "Fund counts now test this. On 34 tail CFs whose 990 narratives state an all-funds total, the fund-count rule F gives a median of $4,500 per DAF account and 258 bps, against rule A’s $3,518 and 203 bps on the same CFs. F exceeds A at 24 of 34 CFs, the expected direction. The set leans to larger-opex CFs, so the frame-level value is probably nearer $3.2k [I] (b45n33-02-01-01). The earlier 15-CF web sample gave $2,108 and 276 bps (b45n33-02-01). [V wave 48B]"

**Find:** "A fund-count rule (P-B45N33-02-01) or audited notes by fund type (P-B45N33-02-02) would test them."
**Replace with:** "A fund-count rule has since been tested: rule F puts 0.245 of cost on DAFs, or $4,500 per account and 258 bps, on 34 CFs (b45n33-02-01-01). Audited notes by fund type (P-B45N33-02-02) have not yet been used as a test. [V wave 48B]"

### `research/mission-2026-11-14/FINAL-STATUS.md`

**Find:** "  - Rule F puts 0.18 of costs on DAFs (A 0.21, G 0.23), giving a median of $2,108 per DAF account and 276 bps. These results are suggestive only."
**Replace with:** "  - Rule F puts 0.18 of costs on DAFs (A 0.21, G 0.23), giving a median of $2,108 per DAF account and 276 bps. These results are suggestive only.\n  - Superseded by the 990-narrative pass (34 CFs): rule F puts 0.245 of costs on DAFs (A 0.178, G 0.356), giving $4,500 per DAF account and 258 bps. The set leans to larger-opex CFs, so the frame-level value per account is probably lower (about $3.2k [I]). [V wave 48B]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

**Find:** "\n---\n\n## Source register"
**Replace with:** "\n\n### 11.72 Tail CF fund totals from 990 narratives; rule F on 34 CFs (validated, wave 48B)\n\n**Tail CF fund totals from Form 990 narratives** (validated, wave 48B). The study re-runs byte for byte from cached mirror XML. It covers 1,913 FY2022–24 returns and 24,831 text fields, of which 8,516 are Part VIII/IX line labels that yield no hits. It finds 284 hits, and 36 of 641 tail community foundations state an all-funds total. The validator re-read all 36 totals in context, and 35 state all funds, including Northern Alleghenies’ two affiliates (257 + 81 = 338). A fresh sample of 30 excluded hits and two recall probes found no missed total. On fund-count rule F, DAFs are a median 0.245 of funds, against 0.178 of assets and 0.356 of grants. That costs $4,500 per DAF account and 258 bps, and F exceeds A at 24 of 34 CFs. Per DAF dollar this matches the earlier 15-CF web sample (276 bps). Per account it supersedes that sample’s $2,108, which rests on one CF. But the 990 set’s median opex is twice the frame’s, so a frame-wide value is probably nearer $3.2k [I]. Phelps County’s 10,073 bps rests on an unchanged ‘approximately 100’ (repo [`validation-wave48b-report.md`](mission-2026-11-14/validation-wave48b-report.md)). [V wave 48B]\n\n---\n\n## Source register"
