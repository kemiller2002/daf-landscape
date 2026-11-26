# Validation wave 37A: payout-definition bridge (P-B39N8-01) and DAF money abroad (P-B45N31-01)

**Date:** 2026-11-19 · **Validator:** independent-validation-agent-wave37a · **Register:** [`data/mission-2026-11-14/validation-register-wave37a.csv`](../../data/mission-2026-11-14/validation-register-wave37a.csv) (37 claims)

**Scope:**
- [b39n8-01-payout-definition-bridge.md](b39n8-01-payout-definition-bridge.md), its CSV and `scripts/mission_payout_bridge.py`.
- [b45n31-01-daf-money-abroad.md](b45n31-01-daf-money-abroad.md), its CSV and `scripts/mission_daf_money_abroad.py`.

Both scripts were re-run with outputs written to scratch. The FY2023 grid, the IPS reproduction and the R1–R4 panel merge were recomputed independently, without importing the scripts. The IPS xlsx files were re-read. The DAFRC national study PDF was re-fetched after a robots.txt check. 18 Form 990 XMLs (9 recipients, FY2023 and FY2024) were re-read from the GivingTuesday mirror; its robots.txt returns HTTP 404, i.e. no rules. User agent: `research-script/1.0`. No outreach; crt.sh, certspotter and sec.gov were not used.

## Counts

| Study | Claims | Confirmed | Partially confirmed | Contradicted | Unverifiable |
|---|---|---|---|---|---|
| Payout bridge (V37A-01 to 19) | 19 | 14 | 3 | 2 | 0 |
| DAF money abroad (V37A-20 to 37) | 18 | 12 | 6 | 0 | 0 |
| **Total** | **37** | **26** | **9** | **2** | **0** |

## Findings: payout-definition bridge

1. **Reproduction holds.** The rerun CSV is byte-identical (md5 `ede2ca5c…`, 2,621 rows), with the panel rebuild at 10/10 and R5 at 12/12. An independent merge gives the same FY2023 figures:
   - beginning assets, excluding processors: median 11.22%, pooled 22.58%;
   - IRS formula, excluding processors: median 9.21%, pooled 16.75%;
   - market total 24.03% ($54.83bn / $228.14bn).

   The account-weighted median is 15.63%. One row differs in my count: a sponsor with a blank assets cell, which the script correctly excludes (V37A-01–04). Note that the script writes into the repo path unless `--out` is given.
2. **The 23.9% provenance is correct.** IPS p.14 quotes NPT's FY2023 overall payout ("dividing all of this year's grants by all beginning assets") as 23.9%. The repo's own 23.9% is a different statistic: pooled FY2021–24, excluding processors, on the itemised Schedule I sample. The full corrected panel gives 23.69% on that window, so the equality is specific to the sample.

   Report line 42, report line 406 and strategic-synthesis line 291 use the repo figure, correctly described as pooled FY2021–24. However, line 42 sits where readers expect NPT's headline. The §11.42 text below flags this (V37A-05, 06).
3. **The IPS 9.68% reproduces exactly.** IPS's FY2023 sheet gives:
   - 1,735 sponsors, of which 1,487 have a rate;
   - median 0.0967507, the same when recomputed as g/(a+g);
   - 248 blank grants cells and 100 explicit zeros;
   - 7.72% if the blanks count as 0.

   The 2020–22 summary medians also reproduce. On the repo panel:
   - 9.33% for 1,481 sponsors with assets > 0;
   - 9.34% with IPS's screens;
   - 10.20% for sponsors with grants > 0 (screened).

   On the 1,315 EINs in both datasets, every rate agrees to within 0.05 points. Of the 172 IPS-only sponsors, none ever appears in the DAFRC panel (V37A-07–10).
4. **The decomposition arithmetic is exact.** D = 5.87, W1 = 9.41, W2 = −8.32 and the residual is 6.63 points. Together they make up the full 14.9-point gap; the shares are 10%, 39%, 7% and 44% (V37A-11, 12).
5. **The attribution is over-labelled.** The table tags the residual [I], but the headline and the shares call it "within-sponsor distribution". DAFRC sampled just over 50,000 accounts at 111 programmes: 83 community foundations, 15 nationals and 13 religiously affiliated organisations. The panel holds 685,120 accounts excluding processors, and Fidelity alone has 190,162. W is a weighting of a population DAFRC did not sample, so the residual mixes sample composition, window and definition with within-sponsor dispersion.

   DAFRC's own means also cut against the W step: 16% at nationals against 18% at community foundations (V37A-13). The study's §6 claim that DAFRC's programme mix "is not published" is **contradicted** (V37A-17).
6. **"Coincidence" is overstated.** The IRS-formula median sponsor is within about 0.6 points of 9% in every year of DAFRC's window (FY2020 9.39%, FY2021 8.42%, FY2022 9.55%). That the two figures measure different things is shown. That their closeness is accidental is not testable. The study's own §5.1 wording, "numerical proximity, not identity", is the defensible one (V37A-14).
7. **The pivot-sponsor count is contradicted.** Fidelity sets the account-weighted median in 3 of 5 years (FY2020, 2023, 2024), not 4. In FY2022 the pivot is T. Rowe Price on beginning assets (22.56% against Fidelity's 23.15%) and The Alaska Community Foundation on the IRS formula (19.19% against 19.25%). The conclusion that W2 rests on Fidelity's neighbourhood survives (V37A-15).
8. **The DAFRC figures are confirmed** from the re-fetched PDF (sha256 `6fa27204…`): 9%, 15% for accounts that made grants, 18% mean, 22% inactive in 2020–22, 111 programmes and more than 50,000 accounts. The denominator is indeed not stated (V37A-16). The grid ranges and the robots log are confirmed. The ranges apply to the rows excluding processors; with processors, the FY2021 pooled gap reaches 11.1 points (V37A-18, 19).

## Findings: DAF money abroad

1. **Reproduction holds.** The rerun CSV is byte-identical (md5 `9fbb8530…`). The recipient rows sum to $1,867,725,106 abroad from $3,178,770,151 inbound (58.76%), or 61.68% for the 147 recipients that file a Form 990. The combined figure is ($1,890.79m + $1,867.73m) / $98,265.36m = 3.825%. The 3.88%, 4.78%, 4.74% and 5.93% figures also reproduce (V37A-20–23).
2. **The XML re-read matches.** For 8 recipients (MSF USA, IRC, World Central Kitchen, Friends of the IDF, Central Fund of Israel, One Acre Fund, CFR, UNRWA USA), Part IX line 3, line 25 and Schedule F Part I equal the CSV in both years. CFR's Part I is entirely "INVESTMENTS" ($699.3m).

   UNRWA USA's FY2024 return puts $44.4m on line 1 (domestic grants), but its Schedule F Part II shows a $51.5m grant "TO SUPPORT UNRWA" in the Middle East. The max() rule rightly counts this as foreign (V37A-24).
3. **The central measure does not double count.** It takes max(line 3, Part I non-investment), never the sum. The direct route (sponsor line 3) and the indirect route (sponsor Schedule I) cannot overlap. Two caveats:
   - 11 recipients, with $178.3m abroad, are themselves DAF sponsors in the DAFRC panel (V37A-26).
   - **Total expenses** is the consistent base for an expense numerator. But applying the in-year expense mix to inbound DAF dollars is an allocation assumption [I]. For example, Friends of the IDF's FY2023 revenue was 1.97× its expenses. The headline "$1.868bn [C]" should carry that caveat (V37A-27).
4. **AIEF's zero is filed but probably understates.** Line 14b is Yes, and Schedule F Part IV answers Yes to both a transfer to a foreign corporation and ownership of one in both years (V37A-25).
5. **The friends-of, Q05, NTEE and region shares are confirmed:**
   - friends-of: 17 recipients, 87.6%;
   - Q05: 12.25%;
   - regions: Sub-Saharan Africa 35.2%; Europe 31.5% of the combined total against 49.6% of the direct route; Sub-Saharan Africa 6.7× the direct figure.

   "Relief in Gaza" is an inference: Schedule F reports only "Middle East and North Africa" (V37A-28–32).
6. **The [I] extrapolation is arithmetically exact and correctly tagged.** However, its sensitivity check (ranks 101–150) does not test ranks 151 and below: 5,270 recipients averaging about $0.26m each (V37A-34).
7. **The repo's international share needs a gloss.** The 7.8% at report §11.27, strategic-synthesis (lines 98 and 623), FINAL-STATUS line 149 and direction-foreign-grants line 44 is a recipient-sector share. Read as money leaving the US, it should be about 4.7% measured (5.9% [I]) on the same base, or 3.82% of total grants. The 1.92% direct share stands (V37A-35–37).

## Exact corrections

### `research/mission-2026-11-14/b39n8-01-payout-definition-bridge.md`

- **Find:** "lands next to DAFRC's account median (9%) by coincidence, not because the two measure the same thing."
- **Replace with:** "lands next to DAFRC's account median (9%). This is numerical proximity, not identity: the two do not measure the same thing, and the proximity holds in every year of DAFRC's window (FY2020–22 medians 9.4%, 8.4%, 9.6%), so it cannot be shown to be a coincidence without account-level data. [V wave 37A]"

- **Find:** "Fidelity's own rate in 4 of 5 years (FY2023: 15.6% IRS formula, 21.5% beginning assets)."
- **Replace with:** "Fidelity's own rate in 3 of 5 years (FY2020, FY2023 and FY2024; FY2023: 15.6% IRS formula, 21.5% beginning assets). [V wave 37A]"

- **Find:** "(v) **Within-sponsor distribution** (residual to 9%) **−6.6** [I]."
- **Replace with:** "(v) **Residual to 9%** (within-sponsor distribution plus DAFRC's different sample, three-year window and undisclosed denominator, which cannot be separated) **−6.6** [I]. [V wave 37A]"

- **Find:** "- within-sponsor: 44% [I]."
- **Replace with:** "- residual (within-sponsor distribution plus sample, window and definition differences): 44% [I]. [V wave 37A]"

- **Find:** "Excluding processors, the account-weighted median is Fidelity Charitable's own rate in FY2020, 2022, 2023 and 2024."
- **Replace with:** "Excluding processors, the account-weighted median is Fidelity Charitable's own rate in FY2020, 2023 and 2024. In FY2022 it is another sponsor next to Fidelity: T. Rowe Price Program for Charitable Giving on beginning assets (22.56%; Fidelity 23.15%) and The Alaska Community Foundation on the IRS formula (19.19%; Fidelity 19.25%). [V wave 37A]"

- **Find:** "the voluntary 111-programme sample (no processors; its mix of national and CF programmes is not published here);"
- **Replace with:** "the voluntary 111-programme sample: 83 community foundations, 15 national programmes and 13 religiously affiliated organisations (study slides p.3), no processor category, and just over 50,000 accounts, against 685,120 FY2023 EOY accounts in the panel excluding processors (Fidelity alone 190,162). The account-weighted median W therefore describes a population DAFRC did not sample; [V wave 37A]"

- **Find:** "It is a construction, not data."
- **Replace with:** "It is a construction, not data. DAFRC's own account means run the other way from sponsor rates: 16% at national programmes and 18% at community foundations (study slides p.14). [V wave 37A]"

### `research/mission-2026-11-14/b45n31-01-daf-money-abroad.md`

- **Find:** "**$1.868bn** [C]."
- **Replace with:** "**$1.868bn** [C for the arithmetic; allocating DAF dollars at each recipient's average foreign-expense share is an assumption, I]. [V wave 37A]"

- **Find:** "Part IV line 14b answered Yes, but Schedule F Part I reports $0."
- **Replace with:** "Part IV line 14b answered Yes, but Schedule F Part I reports $0. Its Schedule F Part IV answers Yes to both a transfer to a foreign corporation and ownership of one in FY2023 and FY2024, so the zero probably understates its foreign spending. [V wave 37A]"

- **Find:** "6. **Double counting with the direct route is unlikely but not ruled out.**"
- **Replace with:** "6. **Double counting with the direct route is unlikely but not ruled out.** Validation found none: the central measure takes the larger of line 3 and Part I, never their sum, and the two routes cannot overlap at the sponsor. 11 of the 150 recipients ($178.3m abroad) are themselves DAFRC-panel DAF sponsors (e.g. KBFUS, JNF, World Vision, Rotary Foundation), so some inbound may sit in a DAF there before going abroad. [V wave 37A]"

- **Find:** "As a sensitivity, ranks 101–150 give 61.6% and almost the same total."
- **Replace with:** "As a sensitivity, ranks 101–150 give 61.6% and almost the same total. Neither tests ranks 151 and below (5,270 recipients, $1.369bn, about $0.26m each), where small US-based Q-coded groups may weigh more. [V wave 37A]"

- **Find:** "Timing is ignored: a gift booked in FY2024 may be spent later."
- **Replace with:** "Timing is ignored: a gift booked in FY2024 may be spent later. For example, Friends of the IDF's FY2023 revenue ($282.0m) was 1.97 times its total expenses ($143.2m). [V wave 37A]"

### `research/mission-2026-11-14/strategic-synthesis.md`

- **Find:** "an upper-leaning combination [V wave 34S]"
- **Replace with:** "an upper-leaning combination [V wave 34S]. DAF money measured as actually reaching abroad (direct grants plus the top 150 NTEE Q and friends-of recipients at their own foreign-expense shares) is 4.74% on the same base, or 5.93% extrapolated [I] ([b45n31-01-daf-money-abroad.md](b45n31-01-daf-money-abroad.md)) [V wave 37A]"

- **Find:** "An upper-leaning combination, not money leaving the US"
- **Replace with:** "An upper-leaning combination, not money leaving the US. Measured money abroad on the same base: 4.74% (5.93% extrapolated [I]; 3.82% of total grants) [V wave 37A]"

### `research/mission-2026-11-14/FINAL-STATUS.md`

- **Find:** "lifting the international sector share from 5.6% to 7.8%"
- **Replace with:** "lifting the international sector share from 5.6% to 7.8% (a recipient-sector share; DAF money measured as reaching abroad, including via US-registered NTEE Q and friends-of recipients, is 3.82% of top-50 grants, or 4.74% of net Schedule I plus line 3) [V wave 37A]"

### `research/mission-2026-11-14/direction-foreign-grants-schedule-f.md`

- **Find:** "so 7.8% is an upper-leaning combination, not a measure of money leaving the US [I]."
- **Replace with:** "so 7.8% is an upper-leaning combination, not a measure of money leaving the US [I]. P-B45N31-01 measures money leaving the US at 4.74% of the same base (5.93% extrapolated [I]). [V wave 37A]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

- **Find:** "\n---\n\n## Source register"
- **Replace with:** "\n### 11.42 Payout definitions and DAF money abroad (validated, wave 37A)\n\n**Payout definitions and DAF money abroad** (validated, wave 37A). Both studies reproduce byte for byte. In the payout bridge, 23.9% is NPT’s FY2023 aggregate (all grants over all prior-year assets), and the corrected panel gives 24.0%. The 23.9% gross figure in §1 and §11.1 is a different statistic: the repo’s pooled FY2021–24 itemised sample, which equals NPT’s number only by coincidence. IPS’s 9.68% median reproduces exactly from its sponsor file (1,487 rated sponsors). The panel gives 9.33% on the same formula, and the whole gap comes from which sponsors are included. The bridge from 23.9% to DAFRC’s 9% account median is exact arithmetic, but its last step (−6.6 points) is a residual [I]. DAFRC sampled about 50,000 accounts at 111 programmes, 83 of them community foundations, not the panel’s account population. Fidelity sets the account-weighted median in 3 of 5 years, not 4. On money abroad, $1.868bn reached abroad through the top 150 NTEE Q and friends-of recipients, 58.8% of their DAF inbound. With direct grants, that is 3.82% of top-50 grants, or 4.74% of net Schedule I plus line 3 (5.93% extrapolated [I]). The 7.8% in §11.27 is a recipient-sector share, not money leaving the US. [V wave 37A]\n\n---\n\n## Source register"

## Find-uniqueness check

Each **Find** above was checked by script (with `\n` unescaped; no Find contains double quotes), and the 17 items were also applied in sequence to in-memory copies without collision. Every Find occurs exactly once in its target file as of 2026-11-19.
