# Validation wave 36C: NPT and Ren follow-ups (npt-ren-followups-2026-11-19)

- **Study validated:** [npt-ren-followups-2026-11-19.md](npt-ren-followups-2026-11-19.md), its data file [`npt-ren-followups-2026-11-19.csv`](../../data/mission-2026-11-14/npt-ren-followups-2026-11-19.csv) and [`scripts/mission_npt_ren_followups.py`](../../scripts/mission_npt_ren_followups.py).
- **Register:** [`data/mission-2026-11-14/validation-register-wave36c.csv`](../../data/mission-2026-11-14/validation-register-wave36c.csv) (18 claims, V36C-01 to V36C-18).
- **Validator:** independent-validation-agent-wave36c. **Date:** 2026-11-19. No file other than this report and the register was edited. Nothing was committed.
- **Access rules followed:**
  - robots.txt was read first on every host. The donorfirstx hosts return 404 (no rules). archive.org, nptrust.org and irs.gov allow the paths used.
  - The same UA was used as in the study (`research-script/1.0`), and it was never changed.
  - crt.sh, certspotter and sec.gov were not used, and there was no outreach.
  - Scratch output is in the session scratchpad, `v36c/`.

## Counts

| Result | Claims |
|---|---|
| confirmed | 14 |
| partially_confirmed | 3 (V36C-05 switch bracket, V36C-14 framing of "line 1b should read Yes", V36C-18 "Schedule F line 3") |
| contradicted | 1 (V36C-11 Part V line 2 count: 12, not 13) |
| unverifiable | 0 |

There are **22 exact corrections** across six research files, plus one insertion (§11.41) in the industry report.

## Findings

### Reproducibility (V36C-01, -02)

- **csv mode.** Rerun from the cached FY2025 and FY2024 XML, the H.10 page and `qnr/wayback.json`, it rebuilds the 79-row CSV byte for byte (md5 `70df32fccc436eda8811ffe3ef19c475`).
- **npt990 mode.** Rerun, it prints every Schedule R, Part IX, Schedule F and FX figure the study uses.
- **wayback mode.** Rerun offline from a copy of the 369-file cache, it gives an identical JSON and the same seven captures.
- **Live availability API.** Three probes, sent 6 seconds apart, all returned HTTP 429, so I stopped. The capture list therefore rests on the study's cache.
- **Two small discrepancies:**
  - the study's own "HTTP 429 came back once" is not logged anywhere, so it cannot be checked;
  - the header says the script has two modes, but it has three.

### Guides, hashes and live headers (V36C-03, -04)

- **Live HEAD requests on 7 of the 9 guide URLs:**
  - five Giving Platform copies (rcf, ubs, ampf, mdrt, rbcrcf);
  - both 2309 guides (tda, ubs).
  
  All seven match the study's Content-Length, Last-Modified and ETag.
- **Live hashes.** The rcf Giving Platform guide (`93d97b49e84a…`), the TDA 2309 guide (`789efac9bf3b…`) and the UBS 2309 guide (`0025f0fe726a…`) were downloaded again and re-hashed. All three match. The cached ubs Giving Platform copy hashes the same as the rcf copy.
- **Text.** Both 2309 guides say "The default is “Fund Name Only”." The Giving Platform guide says "By default, this includes the grant advisor's name, email, and address". The two 2309 guides differ only in phone, email and portal name.
- **New point: the ETag is not independent evidence.** On IIS the ETag is the file's write time, stored as a byte-swapped FILETIME with a change counter. For example, `…4d71dd1` is the high DWORD `0x01dd714d`, which is 2026-11-10 19:59.
  - So "same ETag and same Last-Modified" is one fact, not two.
  - Identical sub-second write times on seven host names also fit a single physical file served under several virtual hosts.

### Bracket for the switch (V36C-05): partially confirmed

- **The dates are right:** the PDF was created 2026-10-06, the server write time is 2026-11-10, and the last capture is 2026-07-22. The bracket built on them is mis-specified in two ways.
- **For the file,** 2026-10-06 to 2026-11-10 is a **hard** bound, not a "most likely" sub-range of 2026-07-22 to 2026-11-19.
- **For the wording, there is no lower bound.**
  - No file at the Giving Platform path has ever been read saying "Fund Name Only".
  - The 2026-07-22 capture proves only that an earlier file existed at that path.
  - The "Fund Name Only" texts sit on other paths (the 2309 guides).
- **UBS.** "UBS has served the Fund Name Only guide continuously" rests on the file's write time. That shows the file existed, not that it was linked continuously.
- The study's §1.4 "Reading" already admits most of this. The §0 headline and the bracket line do not.

### NPT consolidated statements and the $116.3m (V36C-06, -07): confirmed

- **Sources.** Both PDFs were downloaded again: FY2025 (`e7529055f11c…`) and FY2024 (`ddfc47eeea7a…`).
- **The relabel is confirmed.** In the FY2025 PDF, the expense block reuses the liability captions:

  | FY2025 PDF caption | FY2025 | FY2024 | Caption for the FY2024 figure in the FY2024 PDF |
  |---|---|---|---|
  | "Asset management fees payable" | 116,260 | 94,289 | "Program services" |
  | "Lease liability" | 13,230 | 12,025 | "Fundraising" |
  | "Grants payable" | 34,263 | 28,661 | "General and administrative" |

  The real balance-sheet liability "Asset management fees payable" is 400 (FY2025) and 353 (FY2024).
- **Corroboration.** NPT's FY2025 990 fundraising column ($12.87m) and management-and-general column ($33.61m) are close to the 13,230 and 34,263 rows.
- **So $116.26m is program services expense excluding grants, not an asset-management fee.** The repo's 27 bps "fee" reading must go.
- **Small discrepancy:** the study's §2.3 table calls the figure "audited", although the PDF has no auditor's report.

### FY2025 Part IX and line 11f (V36C-08, -09): confirmed

- **FY2025 program column excluding grants: $114,171,773.**
  - line 11f: $93,512,965 (81.9%);
  - staff: $13,063,841;
  - "PROGRAM FEES": $4,295,780;
  - IT: $1,996,236;
  - the eight other lines: $1,302,951, which ties to the dollar.
- **FY2024 program column excluding grants: $92,939,609**, of which line 11f is $73,967,492.
- **Line 11f in all columns:** $93,771,463 (FY2025) and $74,179,211 (FY2024).
- **Scenario arithmetic.** Mean Part X investments are $41,655,677,696, so line 11f is 22.4 bps. The residual after the model fee is $31,029,448 to $51,857,287.
- **Contractors.** There are 9 (FY2025) and 18 (FY2024) contractors over $100k. ICONIQ Capital is paid $2,860,300 for "CONSULTING".
  - Challenge: ICONIQ is an investment firm. "No adviser firm named" is literally true, but it does not rule out investment-related payees.

### Schedule R (V36C-10, -11)

- **Indicators: confirmed.** Schedule R has exactly 19 direct-child `*Ind` elements, so the a–s schema-order labels are sound. The governing line is **1b** (`GiftGrntOrCapContriToOthOrgInd`), and it is **0**. Line 1c is 1. Lines 1l, 1n, 1o and 1q are 1.
- **Parts I and II: confirmed.**
  - Part I: Transatlantic has income of $141,768,810 and EOY assets of $279,696,494.
  - Part II: NPT UK has a blank exempt code and `ControlledOrganizationInd` 0.
- **Line 2: contradicted.** It has **12** rows, not 13: 2 of type C, 5 of type L and 5 of type Q. None names NPT UK or Transatlantic.
- **New interpretation point.** NPT UK's own accounts call NPT "the charity's sole member". If sole membership gives NPT the power to appoint NPT UK's board, then NPT UK may be a controlled entity. In that case line 2 would also need any transaction with it over $50k. The study accepts NPT's "not controlled" at face value.

### IRS instructions and Appendix F (V36C-12, -13, -14)

- **The instruction texts are confirmed live from irs.gov** (robots.txt checked).
  - **i990sr.pdf:** SHA-1 `509585485fc9…`, ModDate 2025-01-08, Last-Modified 2025-01-09. The disregarded-entity exception and the Part V line 1 sentence are verbatim. Line 1 also says "A single transaction may be described by and reported in more than one line".
  - **i990.pdf:** SHA-1 `63250e5a5368…`, ModDate 2025-12-11. Both Appendix F sentences are verbatim.
- **The reasoning is the stronger reading.** The line-1 exclusion names only transactions *with* disregarded entities, and Appendix F makes a disregarded entity's activities the parent's own.
- **The study does not address a contrary reading.** Appendix F's own carve-out ("except … on Schedule R (Form 990), in which disregarded entities must be separately reported") could be read by a preparer as keeping the report-as-parent rule off Schedule R. On that reading, Transatlantic's grant stays out of Part V.
- **Framing (V36C-14): partially confirmed.**
  - **Framed as an interpretation:** the CSV row note is conditional and tagged [I], and §3.2 labels its reading [I].
  - **Framed as a finding of error:** the §0 cell ("The filed No is not reconciled by the instructions … line 1b should read Yes") and §3.2's "Either way … inconsistent … No reading of the disregarded-entity exception reconciles them".
  - g0702 §3.4 (V35B wording) also says flatly "so line 1b should read Yes".
  - The corrections below reframe all of these as this repo's interpretation.

### Affiliate accounts (V36C-15): confirmed

- **NPT Transatlantic, note 19:** verbatim, and the grant table row reads 30,939 (£'000).
- **NPT UK, note 14:** verbatim.

### $39.1m Europe line and FX (V36C-16, -17, -18)

- **Uniqueness: confirmed.**
  - Exactly one line is $39,100,000. The next lines are $16,770,000 and $12,080,347.
  - £30.939m at the FY2025 minimum H.10 rate is $37,615,636, so no other line can carry it at any FY2025 rate.
  - The Part II totals (560 lines, $310,238,950; Europe 411 lines, $154,427,213), the Part I Europe total ($154,655,237), the roundness counts (17 of 57; 6 of 25) and the purpose counts (93 and 64) all match.
- **FX arithmetic: confirmed.** The implied rate is 1.26378. Over 250 days the mean is 1.2948, the minimum 1.2158 and the maximum 1.3754. 11 days fall within ±0.0025.
- **New FX point.** The ±0.0025 band (±0.2%) is narrower than a bank FX spread. At ±1% the matching days rise to 54, from 2024-07-01 to 2025-04-07. The date window is weak evidence.
- **"12.6% of Schedule F line 3 ($310.5m)": partially confirmed.** $310,506,570 is **Form 990 Part IX line 3**. Schedule F Part I line 3 is $2,972,941,202, and the Schedule F Part II total is $310,238,950.

### Repo passages corrected

**"$116.3m asset management fees" and its variants.** The research/ grep found five passages:
- g0702 §2.5;
- queue-batch37: the P-GPT-03 row, the source row and the "27 bps" bullet;
- queue-batch35 §5.2, which carries the 27 bps reading.

**Schedule R passages that miss the line-1b nuance, or that say disregarded entities are wholly outside Part V:**
- FINAL-STATUS.md ("Schedule R does not cover disregarded entities");
- direction-foreign-grants §4;
- g0702: the §0 cell, §1.6 step 1 and the §3.4 bullet.

**Left unchanged:**
- `DAF-INDUSTRY-REPORT-2026-11.md` §11.37 already says "no filed grant … (Schedule R line 1b, not 1d)";
- `validation-wave35b-report.md` is a historical record.

**Follow-ups that are not Find/Replace (data files, outside research/):**
- `data/mission-2026-11-14/adviser-managed-daf-assets-2026-11-19.csv` row 444 carries `asset_management_fees_usd_thousands` = 116260. It should become a program-services-excluding-grants row, or be flagged.
- `queue-proposals-g0702-b4531.csv` and `research-priority-inputs.csv` (P-G0702-05) describe "the composition of the $116.3m asset management fees". Their row text should be relabelled.

## Exact corrections

### `research/mission-2026-11-14/npt-ren-followups-2026-11-19.md`

- **Find:** "It has two modes:"
- **Replace with:** "It has three modes (the third, `csv`, rebuilds the data file from the cached inputs) [V wave 36C]"

- **Find:** "**The full-contact file reached the RCF portals between 2026-07-22 and 2026-11-19, most likely 2026-10-06 to 2026-11-10.**"
- **Replace with:** "**The current full-contact file was first served on the RCF portals between 2026-10-06 (its PDF creation time) and 2026-11-10 (its server write time). When the wording itself changed has no lower bound: no file at this path has been read saying “Fund Name Only”.** [V wave 36C]"

- **Find:** "They are one deployment, written to the servers at 2026-11-10 19:59:13 GMT [F]."
- **Replace with:** "They are one deployment, written to the servers at 2026-11-10 19:59:13 GMT [F]. On IIS the ETag encodes the file's write time, so the shared ETag restates the shared Last-Modified and is not independent evidence; one physical file served under several host names would look the same [V wave 36C]"

- **Find:** "- **Bracket:** the switch on this path happened **after 2026-07-22 and by 2026-11-19**. Within that, the file evidence points to 2026-10-06 to 2026-11-10 [F/H/I]."
- **Replace with:** "- **Bracket:** the current file went live on this path between **2026-10-06 and 2026-11-10** (PDF creation time; HTTP Last-Modified). That is a hard bound for the file. The wording switch is bounded only above, by 2026-11-10: the 2026-07-22 capture shows that an earlier file existed, not what it said [F/H/I] [V wave 36C]"

- **Find:** "guide continuously from at least June 2024 [F] / April 2025 [H] to today"
- **Replace with:** "guide file since at least June 2024 [F] (server write time; captured April 2025 [H]) to today. Continuous linking is not shown [V wave 36C]"

- **Find:** "**Part V line 2:** 13 transactions, all with the US supporting organisations (types C, L, Q)."
- **Replace with:** "**Part V line 2:** 12 transactions, all with the US supporting organisations (2 of type C, 5 of type L and 5 of type Q) [V wave 36C]"

- **Find:** "is not reconciled by the instructions.**"
- **Replace with:** "is not reconciled by the instructions on this repo's reading [I]. That is an interpretation, not an established filing error.** [V wave 36C]"

- **Find:** "is a line-1b gift or grant, and line 1b should read Yes."
- **Replace with:** "would, on this reading, be a line-1b gift or grant, so line 1b would read Yes [I] [V wave 36C]"

- **Find:** "is inconsistent with the affiliates' audited accounts.** No reading of the disregarded-entity exception reconciles them."
- **Replace with:** "is, on this repo's reading of Appendix F, inconsistent with the affiliates' audited accounts.** That is an interpretation, not an established filing error. Appendix F itself exempts Schedule R from the report-as-parent rule (“except … on Schedule R (Form 990), in which disregarded entities must be separately reported”), and a preparer could read that as keeping Transatlantic's own grants out of Part V. The IRS has not ruled [V wave 36C]"

- **Find:** "| Audited consolidated"
- **Replace with:** "| Consolidated (summary PDF, no auditor's report) [V wave 36C]"

- **Find:** "So the size is consistent with a wire in mid-November 2024 to February 2025, or on 1 July 2024."
- **Replace with:** "So the size is consistent with a wire in mid-November 2024 to February 2025, or on 1 July 2024. The ±0.0025 band is narrower than a typical bank FX spread: at ±1% the matching H.10 days rise to 54 (2024-07-01 to 2025-04-07), so the timing evidence is weak [V wave 36C]"

- **Find:** "12.6% of NPT's FY2025 Schedule F line 3 ($39.1m of $310.5m)"
- **Replace with:** "12.6% of NPT's FY2025 Form 990 Part IX line 3, grants to foreign organisations ($39.1m of $310,506,570; Schedule F Part II totals $310,238,950) [V wave 36C]"

### `research/mission-2026-11-14/g0702-b4531-national-990-reads.md`

- **Find:** "give asset management fees of $116,260k (FY2024 $94,289k)"
- **Replace with:** "give program services expense excluding grants of $116,260k (FY2024 $94,289k; the FY2025 PDF mislabels the row “Asset management fees payable”, and the FY2024 PDF captions the same FY2024 figure “Program services”) [V wave 36C]"

- **Find:** "(related organisations in Parts II–IV; disregarded entities such as NPT Transatlantic are outside it).**"
- **Replace with:** "(related organisations in Parts II–IV; NPT's own transactions with disregarded entities such as NPT Transatlantic are outside it, but on this repo's reading of Appendix F their grants to NPT UK are not).** [V wave 36C]"

- **Find:** "so transfers to or by a disregarded entity such as NPT Transatlantic never appear there [V wave 35B]."
- **Replace with:** "so NPT's own transactions with a disregarded entity such as NPT Transatlantic never appear there [V wave 35B]. A disregarded entity's grants to a Part II–IV organisation (Transatlantic's £30.939m to NPT UK in FY2025) are NPT's activities under Appendix F and, on this repo's reading, belong on line 1b [V wave 36C]"

- **Find:** "so line 1b should read Yes"
- **Replace with:** "so line 1b should, on this repo's reading of Appendix F, read Yes (an interpretation, not an IRS finding) [V wave 36C]"

### `research/mission-2026-11-14/queue-batch37-filing-questions.md`

- **Find:** "asset management fees $116.3m (FY2024 $94.3m) [F]."
- **Replace with:** "program services expense excluding grants $116.3m (FY2024 $94.3m), captioned “Asset management fees payable” in the FY2025 PDF by a layout error [F] [V wave 36C]"

- **Find:** "asset management fees $116,260 (FY2024 $94,289)"
- **Replace with:** "program services expense excluding grants $116,260 (FY2024 $94,289; row mislabelled “Asset management fees payable”) [V wave 36C]"

- **Find:** "The $116m of asset-management fees (about 27 bps of average FY2025 investments) is a cost line, not a channel split."
- **Replace with:** "The $116m row is program services expense excluding grants, mislabelled “Asset management fees payable”. It is a cost line, not a fee rate or a channel split; NPT's FY2025 990 line 11f program-column investment management fees are $93.5m, 22.4 bps of mean Part X investments [V wave 36C]"

### `research/mission-2026-11-14/queue-batch35-access-owners-faith.md`

- **Find:** "The label repeats a liability caption and looks like a layout error [I]. If it is NPT's asset-management fee expense, it equals **≈27 bps** of average investments [C: 116.26 / ((47.84 + 36.92) / 2)]. That would be a fee paid by NPT, probably including the 0.10–0.15% advisory fee and adviser-managed accounts."
- **Replace with:** "The label repeats a liability caption and is a layout error: the FY2024 PDF prints the same FY2024 figure ($94,289k) as “Program services”, so $116,260k is program services expense excluding grants, not an asset-management fee, and the ≈27 bps reading is withdrawn. The nearest public fee measure is FY2025 990 line 11f (program column $93.5m, 22.4 bps of mean Part X investments) [V wave 36C]"

### `research/mission-2026-11-14/FINAL-STATUS.md`

- **Find:** "None of NPT's FY2023–24 foreign grants went to related organisations as filed, though Schedule R does not cover disregarded entities."
- **Replace with:** "None of NPT's FY2023–24 foreign grants went to related organisations as filed (Schedule R Part V line 1b = No). Part V excludes only NPT's own transactions with its disregarded entities; on the repo's reading of Appendix F, a disregarded entity's grants to a related organisation are NPT's, so the filed No is a weak test [V wave 36C]"

### `research/mission-2026-11-14/direction-foreign-grants-schedule-f.md`

- **Find:** "But Part V does not cover disregarded entities such as NPT Transatlantic, and in FY2025 Transatlantic granted £30.9m to NPT UK while line 1b stayed No [V wave 35B]."
- **Replace with:** "Part V excludes NPT's own transactions with its disregarded entities, but under Appendix F a disregarded entity's grants are NPT's activities: in FY2025 Transatlantic granted £30.9m to NPT UK while line 1b stayed No, which this repo reads, as an interpretation and not an IRS finding, as a line that should have read Yes [V wave 35B] [V wave 36C]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

- **Find:** "\n---\n\n## Source register"
- **Replace with:** "\n### 11.41 NPT and Ren follow-ups (validated, wave 36C)\n\n**NPT and Ren follow-ups** (validated, wave 36C). Ren's full-contact ‘Giving Platform Donor User Guide’ (SHA-1 93d97b49e84a) was first served on seven RCF portals between 2026-10-06, its PDF creation time, and 2026-11-10, the shared server write time. The IIS ETag encodes that same time, so it adds no independent evidence. When the wording itself changed has no lower bound, because no archived file at that path could be opened. NPT's two-page FY2025 summary labels its program services expense excluding grants ($116.26m; FY2024 $94.29m, captioned ‘Program services’ in the FY2024 PDF) as ‘Asset management fees payable’. In the 990 proxy, line 11f investment management fees are 81.9% of program services excluding grants ($93.51m), and the segregated-account share stays unpublished. NPT's FY2025 Schedule R line 1b reads No, although NPT Transatlantic, a disregarded entity, granted £30.939m to NPT UK. This repo reads Appendix F as requiring Yes, but that is an interpretation, not an IRS finding. The $39.1m Europe Schedule F line is the only candidate for the transfer, and the match is not proven (repo [`validation-wave36c-report.md`](mission-2026-11-14/validation-wave36c-report.md)) [V wave 36C]\n\n---\n\n## Source register"
