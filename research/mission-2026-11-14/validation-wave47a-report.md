# Validation wave 47A: recipient census, tail CF fund counts and rule F, sponsored-project recall

**Date:** 2026-11-20 · **Validator:** validator wave 47A · **Register:** [`validation-register-wave47a.csv`](../../data/mission-2026-11-14/validation-register-wave47a.csv) (29 claims, V47A-01 … V47A-29)

**Studies validated**
1. [b40n1202-04-recipient-census.md](b40n1202-04-recipient-census.md) (P-B40N1202-04), with `recipient-census-2026-11-20.csv` and `scripts/mission_recipient_census.py`.
2. [b45n33-02-01-tail-cf-fund-counts.md](b45n33-02-01-tail-cf-fund-counts.md) (P-B45N33-02-01), with `tail-cf-fund-counts-2026-11-20.csv` and `scripts/mission_tail_cf_fund_counts.py`.
3. [g050303-01-sponsored-project-recall.md](g050303-01-sponsored-project-recall.md) (P-G050303-01), with `sponsored-project-recall-2026-11-20.csv`, the hand-check CSV and `scripts/mission_sponsored_project_recall.py`.

## Method
- **Re-runs, writing only to scratch.**
  - The census script ran cache-only with `--out` pointed at scratch (3 min 24 s). Its CSV is byte-identical to the committed file (md5 `4798a3af0726e5ed2a8df18ad30a23dc`), and its JSON matches the study's `run3.json`.
  - The sponsored-project script ran with `--hand` and `--out` pointed at scratch. Its CSV is byte-identical to the committed file.
  - The tail CF script writes to a fixed relative path. `--task build` was therefore run from a scratch sandbox whose `data/mission-2026-11-14/` held symlinks to every repo data file except the output. Its CSV is byte-identical to the committed file.
- **Row-level decomposition (census).** A scratch wrapper imported the census module unchanged and captured the central committed rows and weights, with `se_components` and `write_csv` stubbed so that nothing reached the repo. It recomputed band and basis aggregates, which reproduce 9.161% / 8.809% and 13.714% / 13.576%.
- **Spot-check (census).** 15 added census recipients were drawn with `random.Random(47)` (29 returns). Part VIII lines were re-read live from the GivingTuesday mirror, taking direct children of the `IRS990`/`IRS990EZ` element.
- **Live source re-reads (tail CF and recall), 13 URLs.** Each was fetched only after a robots.txt check that parsed research-script/1.0, ClaudeBot, anthropic-ai, Claude-User, Claude-Web and Claude-SearchBot and required all six to be allowed.
  - Luzerne FY2024 990 XML, Loudoun 2022 report, Morton homepage and directory, Dallas CF homepage and scholarships page, Luzerne homepage, Cherokee Strip homepage, Will County fund list, IRS i990sd.pdf, TSNE project list, Northwest Film Forum fiscal-sponsorship page.
  - All hosts allowed all six agents (gt990datalake: robots.txt 404).
- **Name check (recall).** An EO BMF (eo1–eo4, cached) substring search covered 25 of the 30 distinct `project_likely` names.

## Counts by study and result

| Study | Claims | Confirmed | Partially confirmed | Contradicted | Unverifiable |
|---|---|---|---|---|---|
| 1. Recipient census (V47A-01…12) | 12 | 10 | 2 | 0 | 0 |
| 2. Tail CF fund counts and rule F (V47A-13…20) | 8 | 6 | 2 | 0 | 0 |
| 3. Sponsored-project recall (V47A-21…29) | 9 | 8 | 1 | 0 | 0 |
| **All** | **29** | **24** | **5** | **0** | **0** |

## Findings

### 1. Recipient census
- **Every stated figure reproduces [V47A-01…08].**
  - Old headline: 9.161% (8.301–10.149%) and 13.714%.
  - New headline: 8.809% (7.937–9.704%; census-fixed 8.213–9.410%) and 13.576% (12.244–14.974%; 12.694–14.522%).
  - Standard error with census strata fixed: ratio 0.733 (−27%) and 0.804 (−20%).
  - Frame: 4,458 = 282 + 696 + 3,480. Returns: 13,588.
  - Thin strata: 4 → 33 and 15 → 56 respondents.
  - ≥$100m band: 4.667% → 4.167%.
  - All 24 SE components match. The old components add in quadrature to 0.498, against the total of 0.495.
- **Spot-check: 15 of 15 match [V47A-11].** Both bases match to the dollar on all 29 returns.
- **Bootstrap design [V47A-09]: right in principle, with two qualifications.**
  - Holding complete strata fixed is the correct design-based treatment. A fully enumerated stratum has no sampling variance, and the repo method's with-replacement resampling of a census stratum is wrong.
  - *First qualification.* Neither variant applies an FPC to the old sample's partly sampled ≥$25m strata (n/N up to 40/42), so the old figure is overstated a little. An approximate N²/n-weighted FPC (mean 1 − f = 0.92 on those strata) puts the 1h reduction near 26% rather than 27%.
  - *Second qualification.* The census-fixed interval covers FY2023–24 finite-population sampling error only. It excludes the allocation envelope (about ±0.3 points on 1h, b40n120201-01), which was not re-run on the enlarged sample, and any year-to-year variance.
- **Why 1h − 1d − 1e moves less [V47A-10]: the study's untested candidate holds up.**
  - In the non-certainty ≥$100m strata, the census raised the weighted 1h denominator by $26.97bn ($146.96bn → $173.93bn). It raised the 1a + 1b + 1c + 1f denominator by only $3.37bn ($76.76bn → $80.13bn).
  - Of the 1h rise, $22.7bn is line 1e (government grants) and $0.9bn is line 1d.
  - Health alone adds $20.5bn of 1h, $11.4bn of it on line 1e.
  - Holding that band at its old values gives 9.17% on 1h, so the band explains essentially the whole −0.35-point fall. On 1h − 1d − 1e the same test gives 13.68%, so the band explains about 0.10 of the 0.14-point fall.
  - The recipients the census adds are largely government-funded, so they enlarge 1h far more than the private-contributions basis.
- **Repo text [V47A-12].**
  - Eight places cite 9.2% / 13.7% as the recipient headline with no census figure: FINAL-STATUS (4), strategic-synthesis (1), b40n12-daf-share-of-recipient-revenue (1), the b40n120201-01 recommendation (1) and b40n1202-b43n26-02 (1).
  - direction-recipients-impact-matching.md has no such citation.
  - In the industry report the figure appears only in earlier waves' §11 paragraphs (§11.53 wave 41B, §11.63 wave 44A). These are left unedited, and a new §11.69 carries the update.

### 2. Tail CF fund counts and rule F
- **The core claims reproduce [V47A-13…15, 19].**
  - Coverage: 15 of 60.
  - Shares: F 0.181, A 0.209, G 0.233.
  - Rule F cost: $2,108 per account and 276 bps.
  - The Schedule D column (b) definition matches the IRS instructions (Rev. December 2024) verbatim.
- **Loudoun [V47A-16].** The live 2022 report shows 33 / 26 / 21 / 7 / 12 / 10 / 1 = 110. The 2024 and 2025 report PDFs in the cache had no extractable text.
- **Luzerne [V47A-17].**
  - Live sources: the FY2024 990 says "MANAGES OVER 400 FUNDS" and the homepage says "700+ Charitable Funds".
  - Schedule D (live XML): column (a) 105, column (b) 282.
  - Using 700+ would lower the median share F to 0.160. The cost medians would not move.
- **Morton [V47A-18]: partially confirmed.**
  - The live directory reproduces 30 / 48 / 10 / 12 / 4 / 2, plus 12 entries in the endowed-DAF section.
  - The live homepage, which the study itself quotes, says "more than 150 endowment funds". That exceeds the 106 non-DAF plus 12 endowed-DAF directory funds.
  - So 123 is a floor, and Morton's share F (0.138) is an upper bound (≤ 17/150 = 0.113). The medians are unchanged.
- **Dallas CF (PA) [V47A-20]: partially confirmed.**
  - Live sources confirm "Charitable Funds 28", and Schedule D gives 14 DAFs.
  - The live scholarships page says it "administers 18 scholarship funds". 14 + 18 = 32 is more than 28.
  - Either the total is stale or some scholarship funds are filed as DAFs, so share F of 0.500 may be overstated. The medians are unchanged.

### 3. Sponsored-project recall
- **The counts and the dollar result reproduce exactly [V47A-21…23, 26–27].**
  - NP lines: 122, $23,543,216, 28 EINs.
  - The three brief examples are all flagged.
  - Myriad: 26 lines, $18,232,969.
  - $0 added to the fiscal-sponsor figure; the non-keyed sensitivity stays at 5 → 5.
  - Refined figure: $1,799,848,564.
- **The directory confirmations hold live [V47A-28].** TSNE lists Future Chefs and Northwest Film Forum lists Upstart Crow Collective. Both are current listings.
- **Precision and recall arithmetic are right [V47A-24, 25].** Wilson intervals: 50.68–74.38% and 71.22–92.25%. Recall: 0.5588 / 0.6676.
- **The hand check is plausible but generous [V47A-29].**
  - 35 of 38 true-positive calls are unconfirmed, and 30 of the 34 `project_likely` notes are the same boilerplate sentence.
  - The SOL VIDA and HAPPENSTANCE notes cite the task brief, which is not independent evidence.
  - The BMF search argues against most calls being aliases: no same-name exempt entity for most names. It does surface two leads the study does not discuss:
    - Shalom Bayit: 85-3882884, NY, ruled 2021-02, already listed in `own_name_bmf_eins`.
    - Detroit Action Commonwealth: MI, ruled 2014-09, a possible exempt arm behind the Detroit Action Education Fund line.
  - Recall inherits this judgement, so 56% is a lower-leaning figure:
    - if only the 4 confirmed or own-EIN calls are projects, line recall is about 92%;
    - at 70% accuracy for the likely calls, it is about 64%.
  - The study's 51.7–61.1% band covers sampling only.
  - The $0 dollar conclusion does not depend on any of this.

## Accept / modify / reject

| Study | Claim | Verdict | Reason |
|---|---|---|---|
| Recipient census | Old 9.16% / 13.71% reproduced | **Accept** | Byte-identical re-run |
| Recipient census | New 8.81% (7.94–9.70; 8.21–9.41) / 13.58% (12.24–14.97; 12.69–14.52) | **Accept** | Re-run; quote the allocation envelope beside the census-corrected CI |
| Recipient census | SE −27% / −20% with census strata fixed | **Modify** | Correct as computed; without FPC on the old partly sampled strata the 1h figure is about −26% (approximate) |
| Recipient census | Frame 4,458 / 3,480 added; 13,588 returns; thin strata 4→33, 15→56 | **Accept** | JSON and stratum rows |
| Recipient census | ≥$100m band 4.67% → 4.17% | **Accept** | Row-level recomputation |
| Recipient census | Variance components | **Accept** | All 24 match; quadrature check |
| Recipient census | Census strata fixed is the right design | **Accept with qualification** | Design-based yes; sampling-only, FY2023–24 only |
| Recipient census | 1h − 1d − 1e moves less (cause untested) | **Modify** | Mechanism now tested: ≥$100m band, mostly line 1e |
| Tail CF | 15 of 60 publish all-fund counts | **Accept** | Byte-identical rebuild |
| Tail CF | Rule F share 0.181 vs 0.209 vs 0.233 | **Accept** | Luzerne 700+ would give 0.160 |
| Tail CF | $2,108 per account; 276 bps | **Accept** | Robust to every disputed total |
| Tail CF | Loudoun 110; Schedule D column (b) definition | **Accept** | Live primary sources |
| Tail CF | Luzerne 400 (vs 318 / 500 / 700+) | **Accept** | Same-period 990; sensitivity noted |
| Tail CF | Morton 123 | **Modify** | A floor: homepage says more than 150 endowment funds |
| Tail CF | Dallas CF (PA) 28 vs 14 | **Modify** | 18 scholarship funds + 14 DAFs > 28 |
| Recall | 122 lines, $23.54m, 28 EINs; Myriad 26 / $18.23m; brief examples | **Accept** | Byte-identical re-run |
| Recall | Precision 63.3% (84.4% ex Myriad) | **Accept as ceiling** | Only 3 of 60 confirmed |
| Recall | FBO recall 55.9% lines / 66.8% dollars | **Modify** | Lower-leaning; judgement range about 56–92% of lines |
| Recall | $0 added; $1,799,848,564 reproduced | **Accept** | Structural; re-run |
| Recall | TSNE and NWFF confirmations | **Accept** | Live re-read |
| Recall | 35 of 38 calls unconfirmed: too generous? | **Modify** | Plausible but not shown; two undiscussed BMF leads |

## Limits
- **Recipient census.** The FPC adjustment is an approximation: it weights strata by N²/n and assumes equal within-stratum variance. The validator did not re-run the allocation envelope on the enlarged sample.
- **Live re-reads.** These are 2026-11-20 pages, so they confirm current text, not the grant-year state. tsne.org sets Crawl-delay 10; the validator made one robots.txt request and one page request.
- **BMF search.** It is a substring match on current names, and 5 of the 30 distinct likely names were too generic to search.

## Exact corrections

### `research/DAF-INDUSTRY-REPORT-2026-11.md`
**Find:** "\n---\n\n## Source register"
**Replace with:** "\n\n### 11.69 Recipient census; tail CF fund counts; sponsored-project recall (validated, wave 47A)\n\n**Recipient census, tail CF fund counts and sponsored-project recall** (validated, wave 47A). All three studies re-run byte for byte from caches. Reading all 4,458 recipients with revenue of $25m or more, on an enlarged sample of 6,132 EINs, moves the central DAF share of recipient contributions from 9.2% to 8.8% on line 1h (95% CI 7.9–9.7%; 8.2–9.4% with census strata fixed) and from 13.7% to 13.6% on 1h − 1d − 1e (12.2–15.0%; 12.7–14.5%). All 15 re-read returns match. Almost all of the fall comes from the ≥$100m band. The recipients it adds are largely government-funded, so the private-contributions basis barely moves. These intervals cover sampling only, and the allocation envelope still applies. Among tail community foundations, 15 of 60 publish an all-fund count. On allocation rule F, DAFs are a median 0.181 of funds and cost $2,108 per account or 276 bps. Morton’s 123 funds is a floor. The own-name project rule adds $0 to the fiscal-sponsor figure. The FBO rule’s 56% recall is a lower-leaning judgement. [V wave 47A]\n\n---\n\n## Source register"

### `research/mission-2026-11-14/FINAL-STATUS.md`
**Find:** "Central estimate 9.2% of line 1h and 13.7% of 1h−1d−1e. The assumption range is 8.8–9.4% and 13.2–14.1%."
**Replace with:** "Central estimate 9.2% of line 1h and 13.7% of 1h−1d−1e on the 2,352-EIN sample. The assumption range is 8.8–9.4% and 13.2–14.1%. With every recipient of $25m or more read (4,458; 6,132 EINs in all), the central estimate is 8.8% on 1h (95% CI 7.9–9.7%; census-corrected 8.2–9.4%) and 13.6% on 1h−1d−1e (12.2–15.0%; 12.7–14.5%). These intervals cover sampling only, and the allocation envelope was not re-run (b40n1202-04). [V wave 47A]"

**Find:** "and the sampling CI 8.3–10.2% and 12.3–15.2%."
**Replace with:** "and the sampling CI 8.3–10.2% and 12.3–15.2% (2,352-EIN sample). The census-enlarged sample gives 8.8% and 13.6%, with census-corrected CIs of 8.2–9.4% and 12.7–14.5% (b40n1202-04). [V wave 47A]"

**Find:** "the committed-frame central figure is 13.7% (assumption envelope about 13.2–14.1%; CI 12.3–15.2%) [V wave 41B]"
**Replace with:** "the committed-frame central figure is 13.7% (assumption envelope about 13.2–14.1%; CI 12.3–15.2%) [V wave 41B]. On the census-enlarged sample it is 13.6% (CI 12.2–15.0%; census-corrected 12.7–14.5%) (b40n1202-04). [V wave 47A]"

**Find:** "  - The all-recipient 9.2% and 13.7% figures are not like-for-like with Chariot."
**Replace with:** "  - The all-recipient 9.2% and 13.7% figures (8.8% and 13.6% on the census-enlarged sample, b40n1202-04) are not like-for-like with Chariot. [V wave 47A]"

### `research/mission-2026-11-14/strategic-synthesis.md`
**Find:** "and the sampling CI 8.3–10.2% and 12.3–15.2% ([b40n120201-01-coverage-gap-decomposition.md](b40n120201-01-coverage-gap-decomposition.md)) [V wave 41B]."
**Replace with:** "and the sampling CI 8.3–10.2% and 12.3–15.2% ([b40n120201-01-coverage-gap-decomposition.md](b40n120201-01-coverage-gap-decomposition.md)) [V wave 41B]. Reading every recipient of $25m or more (4,458) and enlarging the sample to 6,132 EINs moves the central case to 8.8% (CI 7.9–9.7%; census-corrected 8.2–9.4%) and 13.6% (12.2–15.0%; 12.7–14.5%). Those intervals cover sampling only ([b40n1202-04-recipient-census.md](b40n1202-04-recipient-census.md)). [V wave 47A]"

### `research/mission-2026-11-14/b40n12-daf-share-of-recipient-revenue.md`
**Find:** "the figures are 9.2% (1h) and 13.7% (1h − 1d − 1e) (b40n120201-01) [V wave 41B]."
**Replace with:** "the figures are 9.2% (1h) and 13.7% (1h − 1d − 1e) (b40n120201-01) [V wave 41B]. On the census-enlarged sample (6,132 EINs, with every recipient of $25m or more read) they are 8.8% (census-corrected CI 8.2–9.4%) and 13.6% (12.7–14.5%) (b40n1202-04). [V wave 47A]"

### `research/mission-2026-11-14/b40n120201-01-coverage-gap-decomposition.md`
**Find:** "Keep the floor (8.4% / 12.6%) as the measured-only figure."
**Replace with:** "Keep the floor (8.4% / 12.6%) as the measured-only figure. For reporting, the census-enlarged sample supersedes these: 8.8% (7.9–9.7%; census-corrected 8.2–9.4%) on 1h and 13.6% (12.2–15.0%; 12.7–14.5%) on 1h − 1d − 1e ([b40n1202-04-recipient-census.md](b40n1202-04-recipient-census.md)). [V wave 47A]"

### `research/mission-2026-11-14/b40n1202-b43n26-02-chariot-size-match.md`
**Find:** "- **The all-recipient central figures (9.2% / 13.7%) are unchanged.**"
**Replace with:** "- **The size match leaves the all-recipient central figures (9.2% / 13.7%) unchanged.** The census-enlarged sample later moved them to 8.8% / 13.6% (b40n1202-04). [V wave 47A]"

### `research/mission-2026-11-14/b40n1202-04-recipient-census.md`
**Find:** "The census-fixed figure is the right measure of what the census bought (§2.2)."
**Replace with:** "The census-fixed figure is the right measure of what the census bought (§2.2). Neither variant applies a finite-population correction to the old sample’s partly sampled ≥$25m strata (n/N up to 40/42), so the old census-fixed SE is slightly overstated. An approximate correction puts the 1h reduction near 26% rather than 27%. [V wave 47A]"

**Find:** "Keep 9.2% / 13.7% as the 2,352-EIN result."
**Replace with:** "Keep 9.2% / 13.7% as the 2,352-EIN result. The census-corrected intervals cover sampling only. The allocation envelope (about ±0.3 points on 1h, b40n120201-01) was not re-run on the enlarged sample, so quote it beside them. [V wave 47A]"

**Find:** "One candidate is that the census strata whose shares fell most (health ≥$100m) carry large line 1d/1e amounts, so their fall weighs less on the narrower denominator; this is untested."
**Replace with:** "One candidate was that the census strata whose shares fell most (health ≥$100m) carry large line 1d/1e amounts, so their fall weighs less on the narrower denominator. A validator decomposition supports it. In the non-certainty ≥$100m strata, the census raised the weighted 1h denominator by $26.97bn ($146.96bn → $173.93bn) but the 1a + 1b + 1c + 1f denominator by only $3.37bn ($76.76bn → $80.13bn). Of the 1h rise, $22.7bn is line 1e and $0.9bn line 1d. Health alone adds $20.5bn of 1h, $11.4bn of it on line 1e. Holding that band at its old values gives 9.17% on 1h and 13.68% on 1h − 1d − 1e. [V wave 47A]"

### `research/mission-2026-11-14/b45n33-02-01-tail-cf-fund-counts.md`
**Find:** "so Morton's total is 106 directory funds + 17 Schedule D DAFs = **123** (`total_basis = directory_non_daf_plus_sched_d_daf`)."
**Replace with:** "so Morton's total is 106 directory funds + 17 Schedule D DAFs = **123** (`total_basis = directory_non_daf_plus_sched_d_daf`). The homepage says ‘more than 150 endowment funds’ (re-read 2026-11-20). That exceeds the 106 non-DAF directory funds plus the 12 entries in the directory’s endowed-DAF section. So 123 is a floor, and Morton’s share F (0.138) is an upper bound (≤ 17/150 = 0.113). The medians are unchanged. [V wave 47A]"

**Find:** "Examples are Dallas (PA), with 14 of 28 funds but 20% of assets, and Oceana, with 64 of 200+ funds but 21% of assets."
**Replace with:** "Examples are Dallas (PA), with 14 of 28 funds but 20% of assets, and Oceana, with 64 of 200+ funds but 21% of assets. Dallas’s scholarships page counts 18 scholarship funds, and 14 Schedule D DAFs + 18 = 32 exceeds the stated 28. Either the homepage total is stale or some scholarship funds are filed as DAFs, so its share F (0.500) may be overstated; the medians do not move. [V wave 47A]"

**Find:** "- Adding the 3 endowment-only or cumulative totals (n = 18): share 0.222, $2,016 per account, 257 bps."
**Replace with:** "- Adding the 3 endowment-only or cumulative totals (n = 18): share 0.222, $2,016 per account, 257 bps.\n- Disputed totals (validator): using Luzerne’s homepage 700+ instead of the 990’s ‘over 400’ lowers the median share to 0.160. Morton at 167 (150 endowment funds + 17 DAFs) or Dallas at 32 leaves it unchanged. The $2,108 and 276 bps medians are unchanged in every case. [V wave 47A]"

### `research/mission-2026-11-14/g050303-01-sponsored-project-recall.md`
**Find:** "- The pooled dollar recall is distorted by Myriad: its large alias lines carry the pooled dollar precision."
**Replace with:** "- The pooled dollar recall is distorted by Myriad: its large alias lines carry the pooled dollar precision.\n- **Judgement bound (validator).** 35 of the 38 true-positive calls are unconfirmed, and 30 of the 34 project_likely notes are the same sentence, so recall is lower-leaning. If only the 4 confirmed or own-EIN calls are projects, the post-stratified true NP lines fall to about 8 and line recall rises to about 92%. At 70% accuracy for the likely calls, line recall is about 64%. Read 56% as the low end of a judgement range, not a point. [V wave 47A]"

**Find:** "The 63% figure is an upper-leaning judgement [I]."
**Replace with:** "The 63% figure is an upper-leaning judgement [I]. Two of the likely calls (SOL VIDA, HAPPENSTANCE THEATER) rest on the task brief that named them, which is not independent evidence. [V wave 47A]"

**Find:** "SOL VIDA's same-name BMF entity is in CA, while the filed line is in Denver, CO, so it is unrelated."
**Replace with:** "SOL VIDA's same-name BMF entity is in CA, while the filed line is in Denver, CO, so it is unrelated. Two further leads are not resolved. Shalom Bayit (Tides Center) has same-name BMF entities, including 85-3882884 (NY, ruled 2021-02), already listed in `own_name_bmf_eins`. Detroit Action Commonwealth (MI, ruled 2014-09) may be the exempt arm behind the Detroit Action Education Fund line. Both need a check before they count as projects. [V wave 47A]"
