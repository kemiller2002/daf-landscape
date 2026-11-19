# Validation wave 35A: tail fee pool revision and Schedule I grant-purpose panel

**Date:** 2026-11-19 · **Validator:** independent-validation-agent-wave35a · **Register:** [`data/mission-2026-11-14/validation-register-wave35a.csv`](../../data/mission-2026-11-14/validation-register-wave35a.csv) (38 claims)

**Studies checked**
- **Study 1.** [`b4501-04-tail-fee-pool-revision.md`](b4501-04-tail-fee-pool-revision.md), its CSV and `scripts/mission_tail_fee_pool.py`. Register V35A-01 to 19.
- **Study 2.** [`b40n13-01-grant-purpose-panel.md`](b40n13-01-grant-purpose-panel.md), its CSV and `scripts/mission_grant_purpose_panel.py`. Register V35A-20 to 38.

**What was done**
- **Study 1.**
  - The script was re-run into scratch on copies of its three input CSVs.
  - The fee engine, pools, bootstrap and both coverage tables were recomputed with an independent script (own tier parser).
  - The inputs were checked against the census CSV as it now stands.
  - The 12 proposed edits were re-checked against their target files.
- **Study 2.**
  - The script was re-run into scratch with a fresh purpose cache, so all 48 XMLs were re-parsed.
  - The Fidelity, NPT, T. Rowe Price and ImpactAssets values were read directly from their XMLs.
  - The IRS Schedule I instructions and the Fidelity FAQ were re-read live (robots.txt checked first, User-Agent `research-script/1.0`).
  - 60 randomly drawn purpose strings were hand-audited.
  - The repo was searched for passages that rely on purpose-text shares.
- **Requests made.** Only to www.irs.gov (robots.txt, the i990si HTML and PDF; two irs-prior PDF URLs returned 404) and www.fidelitycharitable.org (robots.txt and one FAQ page).
- **Not done.** No outreach, and no crt.sh, certspotter or sec.gov. Nothing was committed or pushed.

Scratch: `/tmp/claude-0/-home-user/ed3d1503-0f0d-5a0d-a5e2-85e6e3196309/scratchpad/v35a/` (`feeroot/`, `pool_out.txt`, `gp/`, `sample60.csv`, `irs/`, `fc/`, `bin/`).

## Counts

| Study | Claims | confirmed | partially_confirmed | contradicted | unverifiable |
|---|---|---|---|---|---|
| 1. Tail fee pool | 19 | 11 | 6 | 2 | 0 |
| 2. Grant-purpose panel | 19 | 12 | 7 | 0 | 0 |
| **Total** | **38** | **23** | **13** | **2** | **0** |

## Study 1 findings: tail fee pool

**Holds.**
- **The script reproduces exactly.** The re-run writes a 109-row CSV identical to the committed one.
- **An independent recompute gives every pool, coverage ratio and loss share.**
  - The frame: 1,240 sponsors and $9,180.1m, of which 641 CFs hold $6,101.3m.
  - The seven schedule pools.
  - The central $137.6m, the CFs-only $89.9m, and the range $76.3m–$183.6m.
  - Per-sponsor coverage of 1/7 (rule A), 0/5 (G) and 4/7 (AM).
  - Population loss shares of 66.7%, 73.1% and 24.9%.

**Contradicted (2).**
1. **The fallback average account is $144.2k, not $143.5k.** The study's figure is not what the script uses: the median over the 551 tail CFs with an average account is $144,232. Outputs are unaffected.
2. **The census CSV is no longer stale.** The study says the CSV "still shows CMAF as `no_published_fee`" (and repeats this in Limit 8). It now shows `partial`, tagged [V wave 34B]. CMAF has no `admin_tiers` and is outside the 2021+ set, and the re-run on the corrected CSV is identical, so no input changes.

**Partially confirmed (6; the last two bullets are one register row, V35A-17).**
- **Wave 34B did not confirm all seven schedules.** It confirmed six and only partially confirmed Whatcom (V34B-24): the live fee page returned a bot check, so the 2% scale rests on the census cache. Whatcom gives the highest CF pool ($179.6m).
- **"No 2021+ tail schedule is that low [100 bps] except ATC's 0%" is wrong.** Pikes Peak's endowed-DAF column, from the same 2025 document and already used as a sensitivity, is exactly 100 bps at $100k.
- **The bootstrap interval depends on the seed.** With seeds 1, 2, 3 and 42, the $72.2m–$155.2m interval moves to $65.4m–$72.2m at the low end and $155.2m–$162.0m at the high end.
- **The population count is 604, not 603.** 604 usable tail CFs have DAF assets; 603 is the number with a rule-A cost.
- **Applying CF schedules to non-CF tail sponsors is defensible only as an upper bracket.**
  - Non-CFs hold $3,078.8m:
    - religious $1,429.2m;
    - single-issue $831.8m;
    - national $411.2m;
    - university/hospital $343.7m;
    - processors $62.9m.
  - Only 1 of 29 sampled non-CFs publishes a rate, and that rate is Cal Poly Pomona's 2%, which sets the top of the range.
  - The only national fee family in the repo charges 60 bps on the first $500k (Fidelity Charitable, `sponsor-fee-schedules.csv`).
  - With CFs at the CFs-only central ($89.9m) and non-CFs at a flat 60 bps, the pool is about $108m [C on that assumption].
  - Conclusions:
    - The whole-tail $138m should always be shown next to the CFs-only $90m.
    - The headline range spans the charge-set assumption as well as the spread of schedules: its low end has non-CFs paying nothing, and its high end has a non-CF rate charged by everyone.
- **Proposals 5–8 describe a median of shares as "the median schedule".** The $138m is the midpoint of two schedule pools (Athens $130.9m and Homer $144.4m), not a schedule. Likewise, "the median schedule leaves 66.7%" describes the median of six shares.
- **Proposal 6 misattributes its source.** It credits "wave 30" with the new 6–7-schedule basis.

**Proposals: mechanics and history.** All 12 Finds occur exactly once, and sequential application succeeds (the study's own check gives 12/12; this wave's check is below). History records are kept:
- proposal 11 appends a superseded note and keeps the $92m text;
- V30-38 and the queue rows are untouched.

## Study 2 findings: Schedule I grant-purpose panel

**Holds.**
- **The script reproduces exactly from fresh XML parses.** All 48 returns re-parse from XML. The output CSV is byte-identical and `audit.csv` is identical (3,880 rows).
- **The four XML checks hold:**
  - **Fidelity:** 80,308 lines, $12,514,527,756 and one string, filed in mixed case as "For grant recipient's exempt purposes".
  - **NPT:** 18,583 lines and 8 sector labels.
  - **T. Rowe Price:** "MULTIPLE" on all 2,479 lines; the Part II line 1h note is verbatim.
  - **ImpactAssets:** "GENERAL SUPPORT" on 2,733 of 2,733 lines, $580,073,941.
- **The IRS column (h) wording and the "more than $5,000 aggregate" rule are verbatim** in both the HTML and the PDF (Rev. December 2024).
- **The pooled shares, regime counts and segment shares all match the CSV.** So do the 107 gala/event lines and the Fidelity FAQ.

**Partially confirmed (7; the instructions bullet is a nuance on confirmed row V35A-27, and the repo-implications bullet covers V35A-37 and 38).**
- **NPT quote.** The ellipsis drops "EXCEPT FOR EXPENDITURE RESPONSIBILITY GRANTS WHERE A SPECIFIC CHARITABLE PURPOSE IS REQUIRED". The quote also stops before "TO ENSURE THAT THE RECIPIENT COMPLIES WITH THE RESTRICTIONS ON DONOR ADVISED FUNDS SET FORTH IN THE INTERNAL REVENUE CODE". So the "restrictions in writing" are statutory DAF conditions, not donor purpose restrictions. Only the first sentence supports the study's point: specific purposes are recommended, and unrestricted is the default.
- **SFF quote.** It comes from the applicant (discretionary) grants paragraph. SFF's advised-grants paragraph says "THE GRANT WILL BE USED SOLELY FOR THE PURPOSE SPECIFIED IN THE LETTER", which is better evidence for DAFs.
- **Compliance reading.** "General support" is the IRS's own example. But the 36.5% of lines in `boiler_exempt` ("FOR GRANT RECIPIENT'S EXEMPT PURPOSES", "CHARITABLE GIFT") are close to the "charitable" the instructions rule out. Saying "the boilerplate strings do not count as non-compliance" overstates the case for them.
- **Which instructions apply.** 19 of the 48 returns end on or before 2024-06-30 (tax year 2023), so the Rev. 12/2024 instructions did not formally govern them. The prior revision was not retrievable here.
- **Keyword audit.** On 60 random sponsor-string pairs (seed 2026111935):
  - 40 agree, 3 are ambiguous and 17 disagree.
  - Weighted by lines, agreement is 97.6% (1,115 of 1,143).
  - 16 of the 17 disagreements under-count specific use. The causes are free text with no keyword hit, PROGRAMS and SUPPORT in `CATEGORY_WORDS`, and OPERATIONS firing `boiler_general` inside "REHAB OPERATIONS".
  - 1 over-counts: "NATIONAL CITY FIRE DEPARTMENT", a recipient name.
  - The 45 largest strings (82% of lines) are all classed correctly.
  - A generous upper bound on the specific share is about 1.8% of lines, so the headline holds.
- **Robots log.** The DAFgiving360 page was requested in the same command as its 403 robots.txt. RFC 9309 treats a 4xx robots.txt as no restriction, so this is a process lapse, not a breach; nothing from the page is used.
- **Repo implications.** The study's verdicts are fair, with two refinements:
  - Schedule F shares are dollar shares, so the restatement should say "lines (or dollars)".
  - ImpactAssets' "all" holds for CY2024 only: the repo records earlier ImpactAssets grants to NPT as partly "FBO Friends of UBS Optimus Foundation".
  - The repo passages that rely on purpose-text shares are listed in group (c) below. The industry report and strategic synthesis have none.

## Accept / modify / reject: the 12 fee-pool proposals

| # | Target | Verdict | Reason |
|---|---|---|---|
| 1 | `direction-long-tail-sponsors.md` §0 Published fee | **Accept** | Counts (7/60, 16/60 after wave 34B, 6/31 CFs, 0–200 bps, CF median 150) all verified |
| 2 | `direction-long-tail-sponsors.md` §0 revenue pool | **Modify** | Add CFs-only $90m and the zero-fee schedule; "median schedule" → "median published tail-CF schedule pool" |
| 3 | `direction-long-tail-sponsors.md` §3.6 Fee | **Accept** | Verified |
| 4 | `direction-long-tail-sponsors.md` §5 item 1 | **Accept** | Verified (1 of 7 rule A, 4 of 7 AM) |
| 5 | `direction-long-tail-sponsors.md` §5 item 7 | **Modify** | Central is the median of six schedule pools, not a schedule; name Cal Poly Pomona as the 2%; flag that non-CF charging is unevidenced |
| 6 | `strategic-synthesis.md` D | **Modify** | "(wave 30; …)" misattributes the new basis; add the CFs-only figure first-class; same "median schedule" wording |
| 7 | `b45n33-long-tail-operating-cost.md` §0 | **Modify** | "the median schedule leaves 66.7%" → "the median across the six schedules is 66.7%" |
| 8 | `b45n33-long-tail-operating-cost.md` §2.4 | **Modify** | Same wording fix; all figures verified (0.58, 0.36, 150 ÷ 205 = 73%, 150 ÷ 285 = 53%) |
| 9 | `b45n33-long-tail-operating-cost.md` §4 | **Accept** | Verified |
| 10 | `b45n33-long-tail-operating-cost.md` §6 R1 | **Accept** | Verified |
| 11 | `consolidation-changelog-wave30.md` row 10 | **Accept** | Keeps the history, appends the superseded note |
| 12 | `DAF-INDUSTRY-REPORT-2026-11.md` §11.27 | **Accept** | §11.35 does report 7 of 60; the validated text is framed as "when this section was validated" |

Totals: **7 accept, 5 modify, 0 reject.**

**Note on the study's own check.** Once the items in group (b) are applied, `--task check-corrections` on the study note will fail, because its Finds will be gone. That is expected.

**Other repo issue (not corrected here).** `DAF-INDUSTRY-REPORT-2026-11.md` has the heading `### 11.35 Recipient basis, ratings and tail fees (validated, wave 34B)` twice in a row. It should be removed by hand; it cannot be targeted by a once-only Find.

## Exact corrections

Apply in order. Each Find is verbatim and occurs exactly once in its file as it stands on 2026-11-19. In Find and Replace strings, `\n` stands for a newline and `\"` for a literal double quote; every other character is verbatim. The check is described at the end of this section.

**Groups**
- **(a)** Corrections to the two studies (first two groups).
- **(b)** The final form of each accepted or modified fee-pool proposal, written against its target file.
- **(c)** Passages that rely on purpose-text shares.
- **(d)** The industry report.

### `research/mission-2026-11-14/b4501-04-tail-fee-pool-revision.md`

1. **Find:** "Wave 34B confirmed all seven 2021+ schedules and the T7 coverage arithmetic (V34B-24 to 33, 38)."
   - **Replace with:** "Wave 34B confirmed six of the seven 2021+ schedules (V34B-25 to 30) and partially confirmed Whatcom's (V34B-24: the live fee page returned a bot-verification page, so the scale rests on the census's 2026-11-19 cache), plus the T7 coverage arithmetic (V34B-32, 33, 38) [V wave 35A]"
2. **Find:** "The census CSV still shows CMAF as `no_published_fee`, but that column is not used here."
   - **Replace with:** "The census CSV now shows CMAF as `partial` (no `admin_tiers`; `in_2021plus_distribution` = no), so it is outside the schedule set; re-running `--task pool` on the corrected CSV reproduces all 109 rows unchanged [V wave 35A]"
3. **Find:** "A seeded bootstrap of the 6-schedule median gives $72m–$155m (90%)"
   - **Replace with:** "A seeded bootstrap of the 6-schedule median gives $72m–$155m (90%); with seeds 1, 2, 3 and 42 the endpoints run $65.4m–$72.2m and $155.2m–$162.0m, because a median of six resampled values takes few distinct values [V wave 35A]"
4. **Find:** "No 2021+ tail schedule is that low except ATC's 0%; CF of West Texas's 1.0% is dated 2016"
   - **Replace with:** "No standard 2021+ tail schedule is that low except ATC's 0%, but Pikes Peak's endowed-DAF column in the same 2025 document (1.00% on the first $3m) is exactly 100 bps at $100k; CF of West Texas's 1.0% is dated 2016 [V wave 35A]"
5. **Find:** "This is a bracketing assumption. It rests on 1 of 29 sampled non-CFs publishing a rate, and on the census's [I] reading that outside CFs \"a DAF is mostly an accommodation, not a product\"."
   - **Replace with:** "This is a bracketing assumption. It rests on 1 of 29 sampled non-CFs publishing a rate, and on the census's [I] reading that outside CFs \"a DAF is mostly an accommodation, not a product\". Charging non-CFs CF schedules (`whole_tail`) is equally unevidenced. Non-CF tail sponsors hold $3,078.8m (religious $1,429.2m, single-issue $831.8m, nationals $411.2m, university/hospital $343.7m, processors $62.9m). If they charged a flat 60 bps (Fidelity Charitable's first-tier rate in `sponsor-fee-schedules.csv`, minimum ignored) while CFs charged the CFs-only central, the pool would be about $108m [C on that assumption] [V wave 35A]"
6. **Find:** "- **Population.** All 603 usable tail CFs with DAF assets in the cost study (579 with a rule-G cost)."
   - **Replace with:** "- **Population.** The 604 usable tail CFs with DAF assets in the cost study, of which 603 have a rule-A and AM cost and 579 a rule-G cost. [V wave 35A]"
7. **Find:** "(or the tail-CF median, $143.5k, where it is missing)"
   - **Replace with:** "(or the tail-CF median, $144.2k ($144,232, over the 551 tail CFs with their own average account), where it is missing) [V wave 35A]"
8. **Find:** "**Headline: central about $138m; range about $76m–$184m** (bold cells)."
   - **Replace with:** "**Headline: central about $138m; range about $76m–$184m** (bold cells). The central and high figures have the whole tail charging CF-type (or Cal Poly Pomona's) prices; the low figure has non-CFs charging nothing. The range therefore spans the charge-set assumption as well as the schedule spread, and the CFs-only central ($89.9m) is as defensible a central figure as the whole-tail one. [V wave 35A]"
9. **Find:** "8. **The CMAF reclassification** (wave 34B) is not reflected in the census CSV's `fee_status`. It does not affect this note, which uses only rows with a rate."
   - **Replace with:** "8. **The CMAF reclassification** (wave 34B) is now reflected in the census CSV (`fee_status` = `partial`). It does not affect this note, which uses only rows with a rate; the re-run on the corrected CSV is identical [V wave 35A]"

### `research/mission-2026-11-14/b40n13-01-grant-purpose-panel.md`

10. **Find:** "- **NPT (rank 2):** \"IF THE DONOR ADVISOR DOES NOT RECOMMEND A SPECIFIC CHARITABLE PURPOSE, NPT AWARDS THE GRANT AS \"UNRESTRICTED\" … NPT ALSO SPECIFIES GRANT FUND RESTRICTIONS IN WRITING\". Yet NPT's purpose column holds only 8 sector labels."
    - **Replace with:** "- **NPT (rank 2):** \"IF THE DONOR ADVISOR DOES NOT RECOMMEND A SPECIFIC CHARITABLE PURPOSE, NPT AWARDS THE GRANT AS \"UNRESTRICTED\" EXCEPT FOR EXPENDITURE RESPONSIBILITY GRANTS WHERE A SPECIFIC CHARITABLE PURPOSE IS REQUIRED.\" So donor-recommended specific purposes exist and unrestricted is the default. The next sentence, \"NPT ALSO SPECIFIES GRANT FUND RESTRICTIONS IN WRITING TO ENSURE THAT THE RECIPIENT COMPLIES WITH THE RESTRICTIONS ON DONOR ADVISED FUNDS SET FORTH IN THE INTERNAL REVENUE CODE\", concerns statutory DAF conditions, not donor purpose restrictions. Yet NPT's purpose column holds only 8 sector labels [V wave 35A]"
11. **Find:** "The filer states outright that restricted and unrestricted grants are merged under one word."
    - **Replace with:** "The filer states that grants of different purposes (endowment, general operating, special project) to the same organisation are combined under one word, and it uses that word on all 2,479 lines; that restricted and unrestricted grants are merged is the reading here [I] [V wave 35A]"
12. **Find:** "- **SFF (rank 48):** \"ORGANIZATIONS THAT ARE AWARDED GRANTS ARE REQUIRED TO ACCEPT THE SPECIFIC GRANT RESTRICTIONS\"."
    - **Replace with:** "- **SFF (rank 48):** \"ORGANIZATIONS THAT ARE AWARDED GRANTS ARE REQUIRED TO ACCEPT THE SPECIFIC GRANT RESTRICTIONS\" (applicant grants); for advised grants, \"THE GRANT WILL BE USED SOLELY FOR THE PURPOSE SPECIFIED IN THE LETTER\". [V wave 35A]"
13. **Find:** "Under the IRS's own wording, \"general support\" is a specific description, so the boilerplate strings do not count as non-compliance."
    - **Replace with:** "Under the IRS's own wording, \"general support\" is an acceptable description, so the `boiler_general` and `boiler_unrestricted` strings are compliant on their face. The `boiler_exempt` strings (\"FOR GRANT RECIPIENT'S EXEMPT PURPOSES\", \"CHARITABLE GIFT\"; 36.5% of lines) are closer to the \"charitable\" the instructions rule out, so compliance is arguable for them; this panel does not decide it [V wave 35A]"
14. **Find:** "\"Nearly\" can become \"all\"."
    - **Replace with:** "\"Nearly\" can become \"all\" for the CY2024 return; the repo records earlier ImpactAssets grants to NPT (CY2021–23) as partly \"FBO Friends of UBS Optimus Foundation\", and other years were not re-read. [V wave 35A]"
15. **Find:** "should be restated as \"X% of lines are *reported* with generic text\"."
    - **Replace with:** "should be restated as \"X% of lines (or dollars) are *reported* with generic text\". [V wave 35A]"
16. **Find:** "Community-foundation shares are sensitive."
    - **Replace with:** "Community-foundation shares are sensitive. A wave 35A audit of 60 random sponsor-string pairs (seed 2026111935) agreed with the assigned class on 40, was ambiguous on 3 and disagreed on 17 (97.6% agreement by lines). 16 of the 17 under-count specific use: free text with no keyword hit (e.g. \"FOR MEDIA OUTREACH\"), PROGRAMS and SUPPORT in `CATEGORY_WORDS` (\"SUPPORT THE CHILDREN'S FOOD AND NUTRITION PROGRAMS\"), and OPERATIONS in `boiler_general` (\"TO SUPPORT THE LOGGERHEAD TURTLE REHAB OPERATIONS.\"); one over-counts a recipient name (\"NATIONAL CITY FIRE DEPARTMENT\"). Counting every `other_descriptive` line, every `boiler_general` string with a programme, project or fund keyword and every label containing PROGRAMS as specific gives about 1.8% of lines. [V wave 35A]"
17. **Find:** "| IRS, Instructions for Schedule I (Form 990) (Rev. 12/2024) | https://www.irs.gov/instructions/i990si | Column (h) wording; the over-$5,000 aggregate rule | 2026-11-19"
    - **Replace with:** "| IRS, Instructions for Schedule I (Form 990) (Rev. 12/2024) | https://www.irs.gov/instructions/i990si | Column (h) wording; the over-$5,000 aggregate rule | 2026-11-19; re-read 2026-11-19 by wave 35A (HTML and PDF). The revision is continuous-use from tax year 2024; 19 of the 48 returns end on or before 2024-06-30 (tax year 2023) and fell under the prior revision, which was not re-read [V wave 35A]"
18. **Find:** "Treated as disallowed. The page request was sent in the same command and also returned 403; nothing from it is used"
    - **Replace with:** "Treated as disallowed, but the page request was sent in the same command, before that decision could apply; it also returned 403 and nothing from it is used. RFC 9309 treats a 4xx robots.txt as no restriction, so this is a process lapse, not a breach [V wave 35A]"

### `research/mission-2026-11-14/direction-long-tail-sponsors.md`

19. **Find:** "**None of the 1,240 tail sponsors has a published fee in the repository** [C]:<br>- the CF fee census stops at the 100th-largest CF ($101.4m);<br>- the national schedules cover 11 sponsors, all above $50m.<br>For comparison, 16 of the top 50 have a published schedule in the repository. **This is the largest gap in this profile** (P-B45N33-01). | High on the absence"
    - **Replace with:** "**When this profile was written, no tail sponsor had a published fee in the repository; the fee census (P-B45N33-01) has since sampled 60.** 7 of them (11.7%; Wilson 5.8–22.2%) publish a 2021+ admin rate and 16 (26.7%) some fee term; 6 of 31 sampled CFs publish a rate. At $100k the published rates run 0–200 bps, with a CF median of 150 bps (n = 6), against 100 bps for top-100 CFs ([b45n33-01-long-tail-fee-census.md](b45n33-01-long-tail-fee-census.md); [b4501-04-tail-fee-pool-revision.md](b4501-04-tail-fee-pool-revision.md)). | High on the publication count; low on the fee level (n = 6–7) [b4501-04] [V wave 35A]"
20. **Find:** "Its revenue pool is small: about $92m a year if the whole tail charged the 100 bps CF median [C on that assumption]."
    - **Replace with:** "Its admin-fee pool is small: about $138m a year if every tail sponsor charged like the median of the published tail-CF schedules, or about $90m if only CFs charge, within about $76m–$184m. One published CF schedule charges no admin fee, so the data do not bound the pool away from zero. The earlier $92m used the top-100 CF median of 100 bps. Only 11.7% of sampled tail sponsors publish a rate, so these figures rest on 6–7 schedules [C on those assumptions] [b4501-04] [V wave 35A]"
21. **Find:** "- **Fee:** the repo has no tail fee observation. P-B45N33-01 fills this."
    - **Replace with:** "- **Fee:** P-B45N33-01 found a 2021+ admin rate at 7 of 60 sampled tail sponsors (6 of 31 CFs): 0–200 bps at $100k, CF median 150 bps ([b45n33-01-long-tail-fee-census.md](b45n33-01-long-tail-fee-census.md)) [b4501-04] [V wave 35A]"
22. **Find:** "   - **Not yet shown:** the tail's actual fees (P-B45N33-01) and its cost base (P-B45N33-02)."
    - **Replace with:** "   - **Since shown:** 7 of 60 sampled tail sponsors publish a 2021+ admin rate (P-B45N33-01). At its own average account, the published fee covers rule-A allocated DAF cost at 1 of 7 publishers and the admin-only floor at 4 of 7 (P-B45N33-02, P-B45N33-02-03; [b4501-04-tail-fee-pool-revision.md](b4501-04-tail-fee-pool-revision.md)) [b4501-04] [V wave 35A]"
23. **Find:** "   - At the 100 bps median CF admin rate (top-100 census, $100k–$1m), the tail's entire admin-fee pool would be about **$92m a year** [C on that assumption]."
    - **Replace with:** "   - The tail's entire admin-fee pool is about **$138m a year** if every tail sponsor charged like the median of the six published tail-CF schedules, each applied at the sponsor's own average account, or about **$90m** if only CFs charge. The range is about **$76m–$184m**: the low end has only CFs charging, at the lowest non-zero published schedule (Hutchinson, 125 bps); the high end has the whole tail at the highest (Cal Poly Pomona's 2%). Charging non-CF sponsors ($3.08bn) CF-type prices is unevidenced: 1 of 29 sampled non-CFs publishes a rate. The earlier $92m applied the top-100 CF median (100 bps). The range rests on 6 CF schedules (7 with Cal Poly Pomona) from a 60-sponsor sample in which 11.7% publish a rate, and one publisher charges no admin fee, so the data do not bound the pool away from zero ([b4501-04-tail-fee-pool-revision.md](b4501-04-tail-fee-pool-revision.md)) [C on those assumptions] [b4501-04] [V wave 35A]"

### `research/mission-2026-11-14/strategic-synthesis.md`

24. **Find:** "At the 100 bps CF median, their whole admin-fee pool would be about $92m a year [C on that assumption] (wave 30)."
    - **Replace with:** "Their whole admin-fee pool is about $138m a year if every tail sponsor charged like the median of the published tail-CF schedules (150 bps at $100k), or about $90m if only CFs charge, within about $76m–$184m. That rests on 6–7 published schedules: only 11.7% of 60 sampled tail sponsors publish a rate. It replaces wave 30's $92m at the top-100 CF median of 100 bps ([b4501-04-tail-fee-pool-revision.md](b4501-04-tail-fee-pool-revision.md)) [C on those assumptions] [b4501-04] [V wave 35A]"

### `research/mission-2026-11-14/b45n33-long-tail-operating-cost.md`

25. **Find:** "Only 15.3% (rule A) and 18.0% (rule G) of tail CFs have allocated cost at or below 100 bps, the top-100 CF census median admin fee (a hypothetical fee for the tail, which has no fee in the repo). At the median, a 100 bps fee would cover about half (100 ÷ 205) of rule-A cost."
    - **Replace with:** "Against published tail fees (P-B45N33-01: 6 CF schedules, 0–200 bps at $100k, median 150), each applied to every usable tail CF at its own average account, the median share across the six schedules is 66.7% of tail CFs below rule-A cost (n = 603), 73.1% below rule-G cost (n = 579) and 24.9% below the AM floor. Across the five non-zero schedules the rule-A share runs 51.7–74.8%. At the medians, a 150 bps fee covers about 73% (150 ÷ 205) of rule-A cost. The earlier comparison used the top-100 median of 100 bps, at or below which sit 15.3% (A) and 18.0% (G) of tail CFs ([b4501-04-tail-fee-pool-revision.md](b4501-04-tail-fee-pool-revision.md)) [b4501-04] [V wave 35A]"
26. **Find:** "- **[C] Against the fee side.** The repo's only CF fee benchmark is the top-100 CF census median of 100 bps (`direction-long-tail-sponsors.md` §0; no tail sponsor has a published fee). Only **15.3%** of tail CFs (rule A, n = 603) and **18.0%** (rule G, n = 579) have DAF cost at or below 100 bps. At the median, a 100 bps fee would cover about 49% (100 ÷ 205) of rule-A cost and 35% (100 ÷ 285) of rule-G cost. **[I] If tail CFs charge near the census median, most run DAFs at a loss under either rule, covered by unrestricted, endowment or agency-fund income.** This needs tail fee data (P-B45N33-01, P-B45N33-02-03)."
    - **Replace with:** "- **[C] Against the fee side.** The fee census (P-B45N33-01) found 6 published 2021+ tail-CF schedules: 0–200 bps at $100k, median 150 bps, against the top-100 CF median of 100 bps. Each applied to every usable tail CF at its own average account, the median share across the six schedules is **66.7%** of tail CFs below rule-A cost (n = 603; 51.7–74.8% across the five non-zero schedules), **73.1%** below rule-G cost (n = 579) and **24.9%** below the AM floor. In aggregate the fee recovers a median 0.58 of rule-A and 0.36 of rule-G cost. At the medians, 150 bps covers about 73% (150 ÷ 205) of rule-A cost and 53% (150 ÷ 285) of rule-G cost. At each publisher's own average account, the fee covers rule-A cost at 1 of 7, rule-G cost at 0 of 5 and the AM floor at 4 of 7 (P-B45N33-02-03). **[I] At observed tail prices, most tail CFs still run DAFs below fully allocated cost under either rule, covered by unrestricted, endowment or agency-fund income, while about three quarters cover the admin-only floor.** The fee level rests on n = 6 ([b4501-04-tail-fee-pool-revision.md](b4501-04-tail-fee-pool-revision.md)) [b4501-04] [V wave 35A]"
27. **Find:** "- **No fee data for the tail**; the 100 bps comparison is a hypothetical benchmark from the top-100 census."
    - **Replace with:** "- **Tail fee data are thin**: the fee comparison uses 6 published tail-CF schedules (P-B45N33-01) from a sample in which 11.7% of sponsors publish a rate; the 100 bps top-100 median is kept only as a reference [b4501-04] [V wave 35A]"
28. **Find:** "| Universe, bands, corrected FY2024 values, 100 bps census median"
    - **Replace with:** "| Universe, bands, corrected FY2024 values, 100 bps census median (as the fee benchmark, superseded by `long-tail-fee-census-2026-11-19.csv` and `tail-fee-pool-revision-2026-11-19.csv`) [b4501-04] [V wave 35A]"

### `research/mission-2026-11-14/consolidation-changelog-wave30.md`

29. **Find:** "N33: tail fee pool about $92m a year [C on assumption]"
    - **Replace with:** "N33: tail fee pool about $92m a year [C on assumption] (superseded 2026-11-19: about $138m central, $76m–$184m range on published tail schedules, n = 6–7; b4501-04-tail-fee-pool-revision.md) [b4501-04] [V wave 35A]"

### `research/mission-2026-11-14/direction-foreign-grants-schedule-f.md`

30. **Find:** "Free text, usually generic.<br>- General support 22.1%.<br>- NPT's NTEE-style labels \"INTERNATIONAL\" 18.6%."
    - **Replace with:** "Free text, usually generic; shares are dollars by the keyword bucket of the *reported* text, not donor restrictions or uses (P-B40N13-01).<br>- Generic text (\"general support\", \"tax-exempt purpose\" and similar) 22.1%.<br>- NPT's NTEE-style labels \"INTERNATIONAL\" 18.6% [V wave 35A]"
31. **Find:** "- **Purpose buckets (main scope):**"
    - **Replace with:** "- **Purpose buckets (main scope).** These are dollars by the keyword bucket of the *reported* purpose text. The general-support bucket is the last rule and also catches \"exempt purpose\", \"charitable\", \"program\", \"support\" and \"mission\". The largest raw texts in the sector buckets (\"INTERNATIONAL\", \"EDUCATION\", \"CULTURE & ARTS\", \"ENVIRONMENT & ANIMAL PROTECTION\", \"HEALTH\") are sector labels of the kind taxonomy filers use on Schedule I. So the buckets describe how filers label recipients, not donor restrictions or uses (P-B40N13-01) [V wave 35A]"
32. **Find:** "  - Single-issue: general support 96.0%."
    - **Replace with:** "  - Single-issue: general-support bucket 96.0%. This is generic reported text, led in FY2023 by \"IN FURTHERANCE OF GRANTEE'S TAX-EXEMPT PURPOSE\" ($46.9m of $74.0m) and \"GENERAL SUPPORT\" ($25.7m), not a measured share of unrestricted grants. [V wave 35A]"
33. **Find:** "while direct foreign grants carry 0.05% relief purpose text [C/I]."
    - **Replace with:** "while direct foreign grants carry 0.05% relief purpose text [C/I]. The 0.05% is a floor: 22.1% of these dollars carry generic text and 18.6% the bare label \"INTERNATIONAL\", either of which can cover relief grants. [V wave 35A]"

### `research/mission-2026-11-14/queue-batch29-complaints-voids.md`

34. **Find:** "ImpactAssets uses that purpose text for nearly every grant, so it says nothing."
    - **Replace with:** "ImpactAssets uses that purpose text on every line of its CY2024 Schedule I (2,733 of 2,733, one distinct string; P-B40N13-01), so it says nothing about this grant's use. [V wave 35A]"

### `research/mission-2026-11-14/industry-incentives-structural-analysis.md`

35. **Find:** "  - *Informational:* purpose fields that indicate benefit risk."
    - **Replace with:** "  - *Informational:* purpose fields that indicate benefit risk. These exist only in sponsors' internal recommendation records: event, gala, ticket, auction, golf, dinner, luncheon or sponsorship text appears on 107 of 322,773 top-50 Schedule I lines (0.03%), so public purpose text cannot supply this signal (P-B40N13-01). [V wave 35A]"
36. **Find:** "  - Grant-purpose sensitivity is documented: an unrestricted purpose expedites the grant."
    - **Replace with:** "  - Grant-purpose sensitivity is documented by a sponsor, not in filings. Fidelity Charitable's FAQ says selecting \"Where It Is Needed Most\" \"can also help expedite the processing\" (re-read 2026-11-19). Fidelity's FY2024 Schedule I carries one purpose string on all 80,308 lines, so the restricted share and its processing effect are not observable in public data (P-B40N13-01). [V wave 35A]"

### `research/mission-2026-11-14/ai-economics-replacement-analysis.md`

37. **Find:** "DAFgiving360 FY2025: 38% recurring, 70%+ unrestricted ([press release](https://www.dafgiving360.org/press-release/fiscal-year-2025-results))"
    - **Replace with:** "DAFgiving360 FY2025: 38% recurring, 70%+ unrestricted ([press release](https://www.dafgiving360.org/press-release/fiscal-year-2025-results); sponsor-reported and not testable from Schedule I, where DAFgiving360's FY2024 return files 38 sector labels on 55,292 lines and no restricted or unrestricted text; P-B40N13-01) [V wave 35A]"

### `research/daf-grant-exception-unit-economics-evidence-and-sensitivity-2026-11-12.md`

38. **Find:** "38% scheduled as recurring, and 70%+ unrestricted."
    - **Replace with:** "38% scheduled as recurring, and 70%+ unrestricted (sponsor-reported; Schedule I cannot test it, because DAFgiving360's FY2024 return files sector labels only; P-B40N13-01). [V wave 35A]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

39. **Find:** "\n---\n\n## Source register"
    - **Replace with:** "\n### 11.36 Tail fee pool and grant purposes (validated, wave 35A)\n\n**Tail fee pool and grant purposes** (validated, wave 35A). Seven 2021-or-later admin schedules published by sampled sponsors under $50m were applied to each tail sponsor's FY2024 DAF assets at its own average account. On them, the tail's admin-fee pool is about $138m a year (the median over the six community-foundation schedules) if all 1,240 sponsors charge, or about $90m if only the 641 community foundations charge. The range, $76m–$184m, rests on six CF schedules and one non-CF schedule. One CF charges no admin fee, and the bootstrap interval of the six-schedule median runs from about $65m–$72m to $155m–$162m depending on the seed. Charging non-CF sponsors CF prices is unevidenced. Across the six schedules, a median 66.7% of 603 usable tail CFs recover less than rule-A allocated DAF cost, and 24.9% less than the admin-only floor. Separately, top-50 Schedule I purpose text cannot measure restricted giving. Of 322,773 FY2024 lines from 48 sponsors, 98.2% carry boilerplate, sector labels, aggregates or blanks, and 1.2% name a specific use; Fidelity Charitable files one string on all 80,308 lines. Repo shares built on purpose text describe reporting practice, not donor restrictions (repo [`validation-wave35a-report.md`](mission-2026-11-14/validation-wave35a-report.md)) [V wave 35A]\n\n---\n\n## Source register"

**Check result.** `v35a/bin/check_corrections.py` parses this section and checks the 39 items across 12 files. For each item it requires that:
- the Find occurs exactly once in the file as it stands;
- the Find still occurs exactly once in the in-memory text after the earlier items for that file have been applied;
- the Replace ends with `[V wave 35A]`.

It also checks that the §11.36 paragraph has 150–200 words. Result on 2026-11-19: **39/39 pass across 12 files**; sequential application succeeds; the paragraph has 192 words. No repository file was written by the check.
