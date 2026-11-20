# Validation wave 44B: tail community-foundation fee sample (b4501-01) and Assets Under Movement / NPT foreign (g050303-02)

**Date:** 2026-11-20 · **Validator:** validator wave 44B · **Register:** [`validation-register-wave44b.csv`](../../data/mission-2026-11-14/validation-register-wave44b.csv) (22 rows, V44B-01 to V44B-22)

**What was done**
- **Study 1.** Re-ran `scripts/mission_b4501_01_tail_cf_fees.py --task census` against the b4501 crawl cache in a scratch root (so no repo file was written). The CSV came out byte-identical and the Appendix E1–E7 tables matched exactly. Independently re-implemented the draw, medians, bootstraps, publication counts, pools and sensitivity from the CSVs. Fetched 10 of the 14 new fee documents live with `research-script/1.0`; robots.txt was checked first on every host, and all allowed the fetch.
- **Study 2.** Re-fetched AUM's FY2022–FY2024 and NPT's FY2024–FY2025 XML from the GivingTuesday mirror (robots.txt 404, so no rules apply). All five files were byte-identical to the scratch cache. Parsed them with my own code. Re-ran `scripts/mission_aum_npt_foreign.py` with a fresh extract cache: the CSV was byte-identical. Recounted the 58 inbound lines from the 94 line-cache files and re-parsed the 21 FY2025 returns. Checked FY2025 coverage against the IRS TEOS 2025–2026 indexes.
- No repo file other than the two outputs was written. Scripts were run with `-B`; the pre-existing `scripts/__pycache__` was left as found.

## Counts

| Study | Rows | confirmed | partially confirmed | contradicted | unverifiable |
|---|---|---|---|---|---|
| 1. Tail CF fee sample (b4501-01) | 13 | 10 | 2 | 1 | 0 |
| 2. AUM and NPT foreign (g050303-02) | 9 | 8 | 1 | 0 | 0 |
| **Total** | **22** | **18** | **3** | **1** | **0** |

## Findings

### Study 1: tail CF fee sample

1. **The draw is as stated** (V44B-01). Seed 20261120 + stratum index over the 641-CF frame, with the original 31 excluded, gives allocation 19 / 26 / 14 / 1. My independent draw returns exactly the 60 EINs in the CSV, with no overlap with the original 31.
2. **The medians are right** (V44B-02, -03).
   - Pooled: 137.5 / 137.5 / 125 bps at $25k / $100k / $500k (n = 20).
   - Extension alone: 112.5 at all three balances.
   - The bootstrap gives 100–150 at each balance under three different seeds.
3. **The publication counts are right** (V44B-04): 14/60 found, and 20/91 pooled.
4. **The no-schedule share is wrong by one CF** (V44B-05, contradicted).
   - The script's own table E3 gives 37/53 = 69.8% (pooled 54/79 = 68.4%).
   - Counting unreadable sites, it gives 44/60 = 73.3% and 66/91 = 72.5%.
   - The document's §0 and §2.1 instead say 38/53 = 71.7%, 55/79 = 69.6%, 45/60 and 67/91. Each is one CF too many.
   - The conclusions do not change.
5. **The pools check out** (V44B-06, -07, -08).
   - **Realised pool:** $49.4m (sum over 641 rows: $49,398,460), unchanged.
   - **Flat ceiling:** $6,101.3m × 137.5 bps = $83.9m. But the $89.9m it "replaces" applied each schedule at each CF's own average account. On the like-for-like flat basis, the old 150 bps gives $91.5m, so the fall is $7.6m.
   - **Sensitivity [I]:** I reproduce +$8.9m design-weighted, for a pool of $58.3m. 10 of the 14 new publishers show no 990 fee line.
6. **The live spot-check passes** (V44B-09, -10). All 10 documents fetched say what the CSV says:
   - Wichita: 2.0% / 1.5% / 1.0% tiers with a $200 minimum, which gives 200 / 175 / 130 bps;
   - Rome: 1.5% on the first $1m, $250 minimum annual fee, $5,000 minimum gift;
   - Yellow Springs: DAF 0.50% annually, board approved June 22, 2026;
   - Horizon: 100 bp on the first $1m, $250 minimum, $25,000 DAF minimum;
   - New Bremen: "underwrites it's fund fees";
   - Benton: 1.25% on the first $2m, .75% above;
   - Humboldt: 1.75% for "most funds";
   - Broomfield: 1.5% for most DAFs, "although some exceptions apply";
   - Western Indiana: 1%;
   - Skagit: 2% / 1.75% / 1.5% bands.
7. **"Tail CFs charge more than the top 100" is no longer established** (V44B-11, partially confirmed).
   - The tail point estimate is still 37.5 bps higher (137.5 vs 100 at $100k).
   - A bootstrap of the difference in medians gives −2.5 to +50 bps, with 13.5% of resamples showing no premium. A one-sided permutation test gives p = 0.04.
   - So the claim fails at the two-sided 95% level, while the evidence still leans towards a premium.
   - The author's §0 wording ("about the same to somewhat higher") is fair. §3's "about the same as the top 100" understates the point estimate.
8. **The b45n33 claim that tail minimums are lower also falls** (V44B-12). The pooled tail opening-minimum median is $10,000, the same as the top-100 figure.
9. **Repo text needs restating** (V44B-13). The old figures appear in:
   - FINAL-STATUS (150 bps at $100k; the $90m ceiling);
   - strategic-synthesis §558 (150 bps; 6–7 schedules);
   - b45n33 §0 and §2.4.

   In the industry report, the old figures appear only in earlier waves' §11 paragraphs (34B, 35A). Those are left alone, and a new §11.64 restates them.

### Study 2: Assets Under Movement and NPT foreign

1. **AUM fails W2** (V44B-14). Its DAF share of assets is 0.2048 (FY2023) and 0.2105 (FY2024), from the filed Schedule D line 4 EOY ÷ Part X line 16. It fails W2 (≥ 0.5) in both years, as the whitelist CSV already records (0.210544).
2. **The roll-forward gap is −$111,423,280, and the test is valid** (V44B-15).
   - **Inputs:** column (a) (DAF-only) lines 2–4 of AUM's own returns, with the FY2023 EOY as the opening value. Column (b) is blank in both years.
   - **What was left out cannot close it.** Investment returns and fees are omitted, but org-wide investment income was only $7.2m. Adding returns would widen the gap, not close it.
   - **The balance sheet locates the gap.** FY2024 net assets rose $130.8m while the filed DAF value rose $28.7m. So non-DAF net assets grew about $102.0m, against only $14.6m of non-DAF contributions less grants implied by Schedule D. The DAF-labelled inflows evidently ended up largely in non-DAF funds.
   - **Consequence:** the 0.949 contributions share and 0.977 grants share are unreliable, and the assets basis is right.
3. **The other filed facts hold** (V44B-16, -17).
   - FY2022: Part IV line 6 = 1 with a blank Schedule D Part I.
   - FY2023 and FY2024 Part III: "Fiscally sponsored projects: These are engaged in furtherance of the mission…".
4. **The inbound lines are as stated** (V44B-18). There are 58 lines, $58,033,863, from 24 filers. Of these, 38 lines ($54,259,515) are generic. One GS DAPF line was checked in its XML: $16,102,500, "COMMUNITY & HUMAN SERVICES".
5. **The arithmetic of the de facto addition is right, but it needs framing** (V44B-19, partially confirmed).
   - **Figures:** $56,559,012 with AUM dropped; $102,478,303 apportioned on assets.
   - **Overstatement:** the document's "defensible" range of $67.0m–$102.5m uses flow bases it calls broken. It also keeps Possibility Labs and Common Counsel in full.
   - **Upper bound:** AUM's non-DAF remainder includes pooled and unrestricted funds as well as projects, so it caps fiscal-sponsorship flow rather than estimating it.
   - **Fit with 43B:** wave 43B's $35.1m–$114.6m (low end: all three DAF-sponsor hybrids dropped) stays the governing range. $102.5m and $56.6m are points inside it.
6. **The whitelist scenario reproduces** (V44B-20). Broad ex-DAF-to-DAF is 25.02% / 22.82% with AUM whitelisted. This is immaterial.
7. **The NPT line is in FY2025** (V44B-21). There is one $39,100,000 Europe row in FY2025 (object 202601289349302480), equal to 12.59% of line 3, and no such row in FY2024 (largest Europe row $25.0m).
8. **The FY2025 totals reproduce** (V44B-22).
   - 21 sponsors: $678,845,354 with the line and $639,745,354 without.
   - The TEOS indexes confirm that 24 of the 50 have a FY2025 return.
   - The three mirror 404s are in the IRS bulk zip 2026_TEOS_XML_05B (cached). With them, the 24-sponsor totals are $687.8m and $648.7m (the line is 5.68% of the total).
   - Two of the 21 now 404 on the mirror and were read from IRS-zip copies.

### Reconciliation with wave 43B

Wave 43B held that AUM belongs as a fiscal sponsor only as a hybrid, in a sensitivity, with the addition stated as $35.1m–$114.6m. Nothing here contradicts that. The proposed wording adds the two AUM-specific points ($102.5m apportioned on its W2 asset share; $56.6m with AUM dropped) inside the 43B range. It does not replace the range. §11.61 is not edited.

## Accept / modify / reject

| Claim | Decision | Note |
|---|---|---|
| Draw (seed 20261120 + i, 31 excluded) | Accept | Independently reproduced |
| Pooled 137.5 / 137.5 / 125 (n = 20; 100–150) | Accept | |
| Extension 112.5 | Accept | |
| Found 14/60; pooled 20/91 | Accept | |
| No-schedule share 71.7% (38/53) | **Modify** | 37/53 = 69.8%; pooled 54/79 = 68.4%; incl. unreadable 44/60, 66/91 |
| Realised pool $49.4m unchanged | Accept | |
| Flat ceiling $83.9m, "from $89.9m" | **Modify** | Value right; the like-for-like flat comparison is $91.5m → $83.9m |
| Sensitivity about $58m [I] | Accept | Keep it labelled as a sensitivity |
| 14 new schedules (10 spot-checked live) | Accept | |
| "Charge more" no longer established | **Modify** | Not established, but the point estimate is still 37.5 bps higher |
| Restate repo 150 bps / 6-schedule claims | Accept | Corrections below |
| AUM 0.205 / 0.211, fails W2 | Accept | |
| Roll-forward gap −$111,423,280 | Accept | Test valid; balance-sheet corroboration added |
| FY2022 line 6 = 1, blank Part I | Accept | |
| Part III "Fiscally sponsored projects" | Accept | |
| 58 lines, $58,033,863; $54.26m generic | Accept | |
| $56.6m dropped / $102.5m apportioned | **Modify** | Report as points inside the 43B range of $35.1m–$114.6m; flow bases are sensitivities only |
| Whitelisted broad ex-D2D 25.02 / 22.82 | Accept | |
| NPT $39.1m line in FY2025, not FY2024 | Accept | |
| FY2025 $678.8m / $639.7m (21 sponsors) | Accept | Can be extended to 24 sponsors: $687.8m / $648.7m |
| Keep AUM off the whitelist, in the de facto set | Accept | Consistent with 43B |

## Limits

- **Spot-check coverage.** 4 of the 14 schedules were not re-fetched live: Yampa Valley, Dubois, Marion and Brookline. Their transcriptions were verified only against the cache, by the script's quote check.
- **Permutation test.** It uses the top-100 `admin_bps_100k` values as filed, not re-run through the tail engine. Both give a median of 100.
- **Roll-forward corroboration.** It compares total net assets with the Schedule D DAF value. Fund-level net assets are not filed.

## Source register

| Source | URL / path | Date |
|---|---|---|
| AUM Form 990 FY2022 / FY2023 / FY2024 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202302999349302215_public.xml ; …/202413159349300006_public.xml ; …/202543179349307759_public.xml | re-fetched 2026-11-20 |
| NPT Form 990 FY2024 / FY2025 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202511339349301311_public.xml ; …/202601289349302480_public.xml | re-fetched 2026-11-20 |
| IRS TEOS index 2025 / 2026; bulk zip | https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv ; https://apps.irs.gov/pub/epostcard/990/xml/2026/2026_TEOS_XML_05B.zip | cached copies |
| Fee documents (10) | See register rows V44B-09 and V44B-10 | fetched 2026-11-20 |
| Repo data | `tail-cf-fee-sample-2026-11-20.csv`, `long-tail-fee-census-2026-11-19.csv`, `tail-realised-fees-all-2026-11-20.csv`, `cf-daf-fee-census-2026.csv`, `daf-long-tail-sponsors-fy2021-2024.csv`, `aum-npt-foreign-2026-11-20.csv`, `daf-to-daf-recipient-whitelist.csv` | as filed |

## Exact corrections

18 items in 7 files. Apply in the order listed; each Find occurs exactly once before and after the earlier items for its file are applied (checked by script). `\n` stands for a newline.

### `research/mission-2026-11-14/b4501-01-tail-cf-fee-sample.md`

**Find:** "Of readable sites, **extension 38/53 = 71.7%** (Wilson 58.4–82.0%; bootstrap 58.5–83.0%). Pooled: **55/79 = 69.6%** (Wilson 58.8–78.7%)."
**Replace with:** "Of readable sites, **extension 37/53 = 69.8%** (Wilson 56.5–80.5%; bootstrap 56.6–81.1%). Pooled: **54/79 = 68.4%** (Wilson 57.5–77.6%). These are the script’s own table E3 figures; 38/53 and 55/79 counted one CF too many. [V wave 44B]"

**Find:** "the shares are 45/60 = 75.0% and 67/91 = 73.6%."
**Replace with:** "the shares are 44/60 = 73.3% and 66/91 = 72.5% (table E3). [V wave 44B]"

**Find:** "38/53 (71.7%; 58.4–82.0%)"
**Replace with:** "37/53 (69.8%; 56.5–80.5%) [V wave 44B]"

**Find:** "**55/79 (69.6%; 58.8–78.7%)**"
**Replace with:** "**54/79 (68.4%; 57.5–77.6%)** [V wave 44B]"

**Find:** "from $89.9m at 147 bps [C]."
**Replace with:** "from $89.9m at 147 bps [C]. The two are not like-for-like: $89.9m applied each schedule at each CF’s own average account, while $83.9m applies one flat median to all assets. On the flat basis the old 150 bps median gives $91.5m, so the like-for-like fall is $7.6m. [V wave 44B]"

**Find:** "On price they are about the same as the top 100 at $100k (137.5 vs 100), with a bootstrap interval that reaches 100."
**Replace with:** "On price the tail point estimate is still higher at $100k (137.5 vs 100), but the difference is not established: the bootstrap interval of the pooled median reaches 100, and a bootstrap of the difference in medians against the 34 top-100 schedules gives −2.5 to +50 bps. [V wave 44B]"

### `research/mission-2026-11-14/b45n33-01-long-tail-fee-census.md`

**Find:** "**Tail CFs publish less and charge more.**"
**Replace with:** "**Tail CFs publish less and charge more.** *Restated by b4501-01 (20 tail-CF schedules from 91 sampled CFs): tail-CF medians are 137.5 / 137.5 / 125 bps (bootstrap 100–150 at each balance), publication is 20/91 = 22.0% (14.7–31.5%), and the pooled opening-minimum median is $10,000, equal to the top-100 figure. Neither a higher tail price nor a lower tail minimum is now established; the n = 6 figures below are superseded.* [V wave 44B]"

**Find:** "(n = 6, including the 0% Adirondack Trust Company Community Fund): **150 / 150 / 138 bps**"
**Replace with:** "(n = 6, including the 0% Adirondack Trust Company Community Fund): **150 / 150 / 138 bps** (superseded: 137.5 / 137.5 / 125 on 20 schedules, b4501-01) [V wave 44B]"

**Find:** "- **[C] Fee levels.** The tail-CF medians are higher than the top-100 medians at $100k (150 vs 100 bps) and $500k (138 vs 100)."
**Replace with:** "- **[C] Fee levels.** The tail-CF medians are higher than the top-100 medians at $100k (150 vs 100 bps) and $500k (138 vs 100). Superseded: on 20 tail-CF schedules (b4501-01) the medians are 137.5 vs 100 at $100k and 125 vs 100 at $500k, and the bootstrap interval of the tail median (100–150) reaches the top-100 median, so the difference is not established. [V wave 44B]"

### `research/mission-2026-11-14/FINAL-STATUS.md`

**Find:** "Tail community foundations that do publish charge a median 150 bps at $100k."
**Replace with:** "Tail community foundations that do publish charged a median 150 bps at $100k on 6 schedules. On 20 schedules from 91 sampled CFs (22.0% publishing; b4501-01) the median is 137.5 bps (bootstrap 100–150), so a premium over the top-100 median of 100 bps is no longer established. [V wave 44B]"

**Find:** "with $90m as a published-schedule ceiling."
**Replace with:** "with $90m as a published-schedule ceiling (about $84m flat at the 20-schedule tail-CF median of 137.5 bps; b4501-01). [V wave 44B]"

**Find:** "Three of the five are also DAF sponsors, so the addition is $35.1m–$114.6m (0.04–0.12% of proxy dollars)."
**Replace with:** "Three of the five are also DAF sponsors, so the addition is $35.1m–$114.6m (0.04–0.12% of proxy dollars).\n  - Within that range, Assets Under Movement’s own returns give a DAF share of assets of 0.205 / 0.211, so it fails whitelist rule W2 and stays off the DAF-to-DAF whitelist; its FY2024 Schedule D misses its roll-forward by $111.4m. Apportioning its 58 lines by its asset share gives an addition of $102.5m; dropping it alone gives $56.6m (g050303-02). [V wave 44B]"

### `research/mission-2026-11-14/strategic-synthesis.md`

**Find:** "That rests on 6–7 published schedules: only 11.7% of 60 sampled tail sponsors publish a rate."
**Replace with:** "That rests on 6–7 published schedules: only 11.7% of 60 sampled tail sponsors publish a rate. A larger sample (b4501-01: 20 tail-CF schedules from 91 sampled CFs) lowers the tail-CF median to 137.5 bps at $100k (bootstrap 100–150), puts the flat CF schedule ceiling at about $84m, and leaves a tail premium over the top-100 median of 100 bps unestablished. [V wave 44B]"

### `research/mission-2026-11-14/g0503-03-de-facto-fiscal-sponsors.md`

**Find:** "the lower end drops the three DAF-sponsor hybrids [V wave 43B]"
**Replace with:** "the lower end drops the three DAF-sponsor hybrids [V wave 43B]. Within that range, apportioning Assets Under Movement’s 58 lines by its own filed DAF share of assets (0.205 in FY2023, 0.211 in FY2024; the whitelist W2 basis) gives $102.5m (0.111% of proxy dollars), and dropping Assets Under Movement alone gives $56.6m (0.061%). Its FY2024 Schedule D flows miss their roll-forward by $111.4m, so flow-based shares are not used (g050303-02-aum-and-npt-foreign.md). [V wave 44B]"

### `research/mission-2026-11-14/g050303-02-aum-and-npt-foreign.md`

**Find:** "**$67.0m–$102.5m hybrid-adjusted**: AUM's non-DAF remainder on the grants and assets bases."
**Replace with:** "**$102.5m on the assets basis**: AUM’s non-DAF remainder at its W2 share. The $67.0m and $70.5m flow-based variants rest on the FY2024 Schedule D that does not roll forward and are sensitivities only. All of these sit inside the validated wave-43B range of $35.1m–$114.6m, whose low end drops all three DAF-sponsor hybrids. The non-DAF remainder also holds AUM’s pooled and unrestricted funds, so it is an upper bound on fiscal-sponsorship flow. [V wave 44B]"

**Find:** "This is consistent with DAF balances being moved to projects or pooled funds as internal transfers that Schedule D does not report as grants, or with a reclassification."
**Replace with:** "This is consistent with DAF balances being moved to projects or pooled funds as internal transfers that Schedule D does not report as grants, or with a reclassification. The balance sheet points the same way: FY2024 net assets rose $130.8m while the filed DAF value rose $28.7m, so non-DAF net assets grew about $102.0m, against only $14.6m of non-DAF contributions less grants implied by Schedule D. Most of the gap therefore sits in non-DAF funds, which favours the assets basis. [V wave 44B]"

**Find:** "Three of the 24 returned HTTP 404 on the mirror: Boston Foundation, Jewish Community Federation of San Francisco and UCLA Foundation (P-G05030302-04)."
**Replace with:** "Three of the 24 returned HTTP 404 on the mirror: Boston Foundation, Jewish Community Federation of San Francisco and UCLA Foundation (P-G05030302-04). All three are in the IRS TEOS bulk file 2026_TEOS_XML_05B. Adding them gives 24 sponsors with $687.8m on line 3 with the NPT line and $648.7m without it (the line is 5.68%); the foreign share of grants is 1.634% with the line and 1.543% without. [V wave 44B]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

**Find:** "\n---\n\n## Source register"
**Replace with:** "\n\n### 11.64 Tail CF fees on 20 schedules; Assets Under Movement apportioned (validated, wave 44B)\n\n**Tail CF fees on 20 schedules, Assets Under Movement and NPT’s Europe line** (validated, wave 44B). Sixty more tail community foundations, drawn by seed and stratum with the original 31 excluded, add 14 fee schedules. A byte-identical re-run and an independent recomputation give pooled medians of 137.5 / 137.5 / 125 bps at $25k / $100k / $500k (n = 20; bootstrap 100–150), against 100 bps for the top 100 at $100k. A tail price premium is therefore no longer established, and the six-schedule median of 150 bps is superseded. Pooled publication is 20/91 (22.0%), and the readable-site no-schedule share is 69.8%, not 71.7%. The realised CF fee pool stays $49.4m and the flat schedule ceiling is $83.9m. Ten of the 14 schedules were confirmed live. Assets Under Movement’s own returns give a DAF share of assets of 0.205 / 0.211, and its FY2024 Schedule D misses its roll-forward by $111.4m. Inside the wave-43B range of $35.1m–$114.6m, apportioning its lines by that share gives $102.5m, and dropping it gives $56.6m. NPT’s $39.1m Europe line is in its FY2025 return, so FY2024 foreign grants are unchanged (repo [`validation-wave44b-report.md`](mission-2026-11-14/validation-wave44b-report.md)) [V wave 44B]\n\n---\n\n## Source register"
