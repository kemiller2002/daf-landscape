# Report and synthesis consistency pass (P-GAP19-11, remainder)

**Date:** 2026-11-19. **Task ID:** gap19-11. **Status:** proposals only. Neither [`DAF-INDUSTRY-REPORT-2026-11.md`](../DAF-INDUSTRY-REPORT-2026-11.md) nor [`strategic-synthesis.md`](strategic-synthesis.md) was edited. Every change is written as a Find/Replace pair in §5, and a script checked that each Find string occurs exactly once in its file (§5.0).

**Scope.**
1. Every "(source: repo inference — no primary URL)" marker in the two files: recount, then a replacement citation, an `[I]` relabel, or softening.
2. A run of `scripts/mission_citation_audit.py` on the two files, with the flagged lines triaged and fixes proposed for 30 of them.
3. Stale figures in report §2 and §9.
4. One current A–G and top-ten section, drawn from the governing figures, with the older layers marked as superseded (§6).

The report's counts paragraph (line 7) was already refreshed and is not touched here.

---

## 1. Method

- **Marker count.** `grep -o` for "repo inference" in both files, plus a check for close variants. The variants searched were "no primary URL", "unsourced", "inference" and an un-parenthesised "source: repo". Each hit was read in context, and the repo was searched (`grep -l`) for a document that states the claim.
- **Citation audit.** `python3 scripts/mission_citation_audit.py research/DAF-INDUSTRY-REPORT-2026-11.md research/mission-2026-11-14/strategic-synthesis.md`.
  - The script takes glob patterns, not a root. Passing `.` as the first argument fails: `ValueError: Unacceptable pattern: PosixPath('.')`. So the two files were passed as globs.
  - The flagged lines were triaged by a stdlib, functional-style helper. It imports the audit's own `FIGURE` and `CITATION` regexes and sorts each flagged line into one of three categories (§3). The helper is `scratchpad/q1911/triage_audit.py`, outside the repo. Its rules are given in §3 so the counts can be reproduced.
- **Validation tallies (§9 table).** A stdlib helper (`scratchpad/q1911/vreg_counts.py`) reads all 37 `data/mission-2026-11-14/validation-register*.csv` files. It maps each `validation_result` by its leading word: confirmed, partially/partly confirmed, contradicted/refuted, unable/unverifiable. Anything else counts as "other".
- **Graph status counts.** These were recomputed from [`relationship-graph-edges-consolidated-2026-11-19.csv`](../../data/mission-2026-11-14/relationship-graph-edges-consolidated-2026-11-19.csv) with `self_loop = False`.
- **Primary-source check.** One check was made: the Form 990 Schedule D PDF on irs.gov, for the fund-level payout marker. `robots.txt` was read first (log in §8). No other web requests were made, and there was no crt.sh, certspotter or sec.gov use. All evidence is 2021 or later.
- **Find-uniqueness check.** A stdlib script parsed §5 of this file. For each `### \`path\`` block it unescaped `\"` and `\n` in every Find string and counted occurrences in the target file. It also checked that every Replace string contains `[gap19-11]` (§5.0).

## 2. Marker table

**Recount.** The report has **17** markers, not 18. The synthesis has **6**, not 7.
- In the report, 13 sit in body text. The other 4 are quoted inside two governing correction items in the appendix: wave 22 item 1 (Find and Replace) and wave 24B item 1 (Find and Replace).
- Both earlier counts were one too high. The likeliest reason is that one marker per file was removed in an earlier edit, but no changelog entry was found that says so.
- No close variants exist. Every hit is the exact string "((source: repo inference — no primary URL))" or "(source: repo inference — no primary URL)". The audit's `CITATION` regex accepts `source:`, so these markers are never flagged by `mission_citation_audit.py` (§3).

Action codes:
- **(a)** cite a repo document or primary URL;
- **(b)** relabel as `[I] inference from <file>`;
- **(c)** soften or remove.

| ID | File:line | Claim (short) | Action | Support found | Correction |
|---|---|---|---|---|---|
| M-R01 | report:44 | Fund-level payout is not public | (a) | [IRS Schedule D (Form 990), Rev. Dec 2024](https://www.irs.gov/pub/irs-pdf/f990sd.pdf) Part I reports only the number of funds and aggregate contributions, grants and year-end value. [`direction-academic-literature.md`](direction-academic-literature.md) F1 covers voluntary account-level samples [V wave 24B] | C-R01 |
| M-R02 | report:136 | Weak nonprofit leverage is structural | (b) | [`industry-incentives-structural-analysis.md`](industry-incentives-structural-analysis.md) l.237 and the classification table l.401: "Nonprofit is not the payer or the legal party" | C-R02 |
| M-R03 | report:138 | Who resists redesign | (b) | Same file, §5 stakeholder table (l.255–267) and summary item 5 (l.34–35) | C-R03 |
| M-R04 | report:139 | Who benefits | (b) | Same file, §5 (l.261–263) | C-R04 |
| M-R05 | report:146 | Ren revenue, margins and concentration not public | (a) | [`queue-batch37-vendor-economics-owners.md`](queue-batch37-vendor-economics-owners.md) Q-B06: "No press, PE or registry source gives a figure" [V wave 22]. Also applies the pending wave-22 governing item 1 | C-R05 |
| M-R06 | report:161 | New-charity reviews and declines are invisible in filings | (a) | [`gap19-exception-load-proxy.md`](gap19-exception-load-proxy.md) §5: "No sponsor publishes how it routes grants, how many exceptions it handles or how long review takes" [V wave 32A] | C-R06 |
| M-R07 | report:165 | No sponsor publishes turnaround P50/P90, exception rates or reviewer minutes | (a) | [`queue-batch36-metrics-rails.md`](queue-batch36-metrics-rails.md) P-PAY-05: no SLA or latency distribution; 5 of 28 statements are measured [V wave 21]. [`ai-economics-replacement-analysis.md`](ai-economics-replacement-analysis.md) l.72: no sponsor publishes human effort or exception rates | C-R07 |
| M-R08 | report:195 | PE customer effects are unobserved | (b) | Absence finding from [`private-equity-daf-ecosystem-map.md`](private-equity-daf-ecosystem-map.md) and `company-timeline-events.csv` | C-R08 |
| M-R09 | report:227 | Redesign removes exceptions; AI shortens handling; AI pays at vendor or network scale | (b) | [`ai-economics-replacement-analysis.md`](ai-economics-replacement-analysis.md) l.86 (already labelled [I] there); [`ai-economics-v2-observed-costs.md`](ai-economics-v2-observed-costs.md) (buyer is an administrator or platform); [`gap19-ai-calibration.md`](gap19-ai-calibration.md) [V wave 31A] | C-R09 |
| M-R10 | report:228 | The most important missing evidence is a sponsor time-and-motion study | (b) | [`ai-economics-replacement-analysis.md`](ai-economics-replacement-analysis.md) l.72; [`gap19-exception-load-proxy.md`](gap19-exception-load-proxy.md) §5 (Q-N03 still open) | C-R10 |
| M-R11 | report:244 | Gating question: API and data-export rights | (b) | [`ai-native-entrant-simulation.md`](ai-native-entrant-simulation.md) l.169 (risk 1); [`FINAL-STATUS.md`](FINAL-STATUS.md) l.221 (Q-N04) | C-R11 |
| M-R12 | report:262 | All evidence is public-source; no vendor tests, interviews or contracts | (a) | [`FINAL-STATUS.md`](FINAL-STATUS.md) l.210 | C-R12 |
| M-R13 | report:264 | The Wayback Machine could not be read | (c) | Contradicted as worded: the report cites `web.archive.org` captures 4 times (3 distinct). [`competitive-history-timelines.md`](competitive-history-timelines.md) l.65 and [`FINAL-STATUS.md`](FINAL-STATUS.md) l.211 say page content could not be retrieved and only the availability API worked | C-R13 |
| M-R14 | report:1175 | Quoted in the wave-22 item 1 Find | none to the quote | Historical instruction text. C-R05 applies the same change with a citation | C-R14 (note) |
| M-R15 | report:1176 | Quoted in the wave-22 item 1 Replace | none to the quote | As above | C-R14 (note) |
| M-R16 | report:1194 | Quoted in the wave-24B item 1 Find | none to the quote | Historical. C-R01 applies the same change with a citation | C-R15 (note) |
| M-R17 | report:1195 | Quoted in the wave-24B item 1 Replace | none to the quote | As above | C-R15 (note) |
| M-S01 | synthesis:20 | Fund-level payout is not public (A2) | (a) | As M-R01 | C-S01 |
| M-S02 | synthesis:49 | "Prevent exceptions before automating" rests on reasoning | (b) | [`ai-economics-replacement-analysis.md`](ai-economics-replacement-analysis.md) l.86 | C-S02 |
| M-S03 | synthesis:101 | Paper-check workflows generate their own exceptions | (a)+(b) | [`gap19-complaints-with-denominators.md`](gap19-complaints-with-denominators.md) l.252–255: lost checks become months-long cases; EFT enrollment is also a complaint source [V wave 32B]. Mechanism from `ai-economics-replacement-analysis.md` l.86 | C-S03 |
| M-S04 | synthesis:111 | Gating condition: no contractual API rights | (b) | As M-R11 | C-S04 |
| M-S05 | synthesis:122 | Cross-sponsor data: "no one aggregates it today" | (b) | [`direction-data-standards-interoperability.md`](direction-data-standards-interoperability.md): no open multi-sponsor standard; DAF Direct is closed, with 3 sponsors (wave 25B) | C-S05 |
| M-S06 | synthesis:123 | Value moves to provable control and scoped SOC reports | (b) | [`queue-assurance-everyorg-givinga-monitoring.md`](queue-assurance-everyorg-givinga-monitoring.md) P-QA1-04: none of 13 vendors publishes a scoped SOC report [V wave 5] | C-S06 |

**Totals by action.**
- **(a):** 7 (M-R01, R05, R06, R07, R12, S01, S03).
- **(b):** 12 (M-R02, R03, R04, R08, R09, R10, R11, S02, S03 in part, S04, S05, S06).
- **(c):** 1 (M-R13).
- **Quoted correction text:** 4 (M-R14–R17), handled with a note.

M-S03 is counted under (a). No claim was found to be unsupportable, so none is proposed for removal.

## 3. Citation-audit triage

**Run.** `mission_citation_audit.py` flags **225 lines**: 201 in the report and 24 in the synthesis.

The audit's `CITATION` regex accepts any of these on the same line: a URL, a markdown link, `.md`/`.csv`/`.json`/`.py`, `source:`, `[V]`, `[I]` or a bracketed source ID. As a result, the sections the task names as most consequential are almost unflagged: §1, the original A–G and the original top ten each have **0** flags. The 23 markers in §2 also escape the audit, because they contain `source:`.

**Triage rules** (in order; implemented in `triage_audit.py`):
1. **False positive.** A correction instruction (`- **Find:**` / `- **Replace with:**`), a version or file-path line, or a bold label line whose only figure is a date.
2. **Internal pointer only (acceptable).** Either the same line carries a wave, section, batch, validation-ID, "(was #n)" or table "same" reference, or the line's contiguous block (paragraph, list or quote, including a list's lead-in line within three lines above) carries a repo link or URL.
3. **Needs a citation.** Everything else.

| Category | Report | Synthesis | Total |
|---|---|---|---|
| Needs a citation | 9 | 0 | **9** |
| Cited by internal repo pointer only (acceptable) | 183 | 24 | **207** |
| False positive | 9 | 0 | **9** |
| **Flagged** | **201** | **24** | **225** |

**What the categories contain.**
- **Needs a citation.** Report lines 309, 318, 558, 559, 616, 618, 656, 657 and 658. In each case a table, or a blank line after a sourced lead-in, separates the claim from its source.
- **False positives.** Report line 3 (version line) and line 285 (chart paths). The other 7 are Find/Replace instruction lines in the correction appendix: 1142, 1143, 1148, 1149, 1186, 1247 and 1264.
- **Internal pointer only.**
  - Most are sub-bullets of §11 blocks whose lead-in cites the repo document.
  - 28 lines (l.1269–1296) are a verbatim second copy of §11.29, left in the wave-31A appendix after it was applied (C-R24).
  - The 24 synthesis lines are wave-layer bullets citing "(wave N)", and corrections-table rows reading "same".

**Thirty fixes proposed** (§5, items A01–A30). The 9 "needs a citation" lines come first. The other 21 are internal-pointer lines in the synthesis's top-ten and A–G layers, plus number-bearing headline lines in report §11 that state a figure governing elsewhere. Each gets a same-line repo link, and where a later validated figure exists, that figure as well:
- A04: §11.2 Ren headline shares still lack the 32.2% graph floor.
- A22: the top-ten Ren item lacks the 32.2% floor and the latest-return update to 19 sponsors and $31.56bn.
- A20: the FY2024 netting monitor lacks the FY2025 covered-filer netting.

## 4. Stale figures in §2 and §9

| Item | Current text | Governing figure | Source | Correction |
|---|---|---|---|---|
| §2 graph size | "up to 893 nodes and 1,051 edges" | Already refreshed (wave-31A item 2 applied) | [`gap19-graph-consolidation.md`](gap19-graph-consolidation.md) l.43; consolidated CSV, 1,051 rows with `self_loop=False` | none |
| §2 status counts | "134 confirmed (one more after red-team), 17 historically confirmed, 11 inferred, 5 unknown" (base-file counts, which sum to 167) | 958 confirmed, 47 inferred, 23 historically confirmed, 11 unknown, 5 reported, 3 probable, 2 unverified lead, 1 pending, 1 rejected (sum 1,051). Red team of 109 weaker edges: 41 confirmed, 16 weakened, 52 unverified, 0 contradicted | Wave-31A governing item 3, **not yet applied**; recomputed here from the CSV | C-R20 |
| §9 "80 consequential claims" table | 45 / 25 / 7 / 3 (waves 1–2B only) | Through wave 32B: 1,036 register rows (1,012 distinct claim IDs; 10 IDs repeat) in 37 files. 784 confirmed, 195 partially confirmed, 32 contradicted, 15 unable to verify, 10 other (7 wave-13 audit notes: 5 defects, 1 cosmetic and 1 "passed 22 of 24"; 2 wave-12 "supported" and "weakly supported"; 1 wave-10 "plausible") [V wave 33B] [C]. The 80-row subset reproduces 45/25/7/3 exactly | 37 `validation-register*.csv` files | C-R21, C-R22 |
| §9 waves pointer | "Validation waves 3–12 are reported per wave" | Waves 3–32B | `research/mission-2026-11-14/validation-wave*-report.md` | C-R23 |
| §1 vendor footprint | "18 sponsors holding $30.18bn (9.2%) in their latest return" | 19 sponsors and $31.56bn after the FY2025 refresh (the addition is Ayco's final return) | [`validation-wave31a-report.md`](validation-wave31a-report.md) l.55; [`gap19-fy2025-refresh.md`](gap19-fy2025-refresh.md) | C-R25 |
| §4 / A5 / F "2.5–3%" exception share | FY6/2025 measure | Like-for-like FY2023–24: about 3.6% of dollars at the four largest nationals. The review-need proxy (core) is 10.0% of their dollars and 11.0% across the top 50. It is a proxy for review need, not observed review | [`gap19-exception-load-proxy.md`](gap19-exception-load-proxy.md) l.45, l.286 and the regeneration note [V wave 32A] | C-R06, C-S07, C-S08 |

**Caveat on the §9 tally.** The leading-word rule counts "confirmed at low confidence; admin tiers contradicted" as confirmed and "contradicted (citation); substance confirmed" as contradicted. A one-to-one map of the 61 free-text result values is possible but was not attempted. The 1,036 rows are register rows; the number of distinct claims across waves is lower, because some later waves re-check earlier claims.

## 5. Exact corrections

### 5.0 Conventions and check

- `\"` stands for a literal double quote and `\n` for a newline. The checker unescapes both before counting.
- Every Replace string contains `[gap19-11]` at the end of the text it introduces. Where a Find string carries unchanged context after the changed text (needed for uniqueness, or to keep a heading or table cell), that context follows the tag. In a table row the tag sits inside the last cell.
- **Check result** (run 2026-11-19 by `scratchpad/q1911/check_finds.py`): all Find strings occur exactly once in their target files, and all Replace strings contain the tag. The per-item counts are in §5.4.
- **Ordering.** Apply C-R01 before C-R15, and C-R05 before C-R14. C-S09 inserts §0 and should be applied last.

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

**C-R01** (M-R01; supersedes the marker wording of wave-24B item 1; the rest of that item still governs)
- **Find:** "\nFund-level payout is not public ((source: repo inference — no primary URL))."
- **Replace with:** "\nFund-level payout is not public in filings: Form 990 Schedule D Part I reports, per sponsor, only the number of donor-advised funds and their aggregate contributions, grants and year-end value ([IRS Schedule D (Form 990), Rev. Dec 2024](https://www.irs.gov/pub/irs-pdf/f990sd.pdf)). Voluntary account-level samples exist: DAFRC's 2024 National Study (111 programs, over 50,000 accounts) puts the median three-year account payout at 9% (15% excluding inactive accounts) and the mean at 18%, and 22% of accounts made no grants in 2020–22 ([executive summary](https://johnsoncenter.org/wp-content/uploads/2024/02/DAFRC_Executive_Summary_Key_Findings.pdf); repo [`direction-academic-literature.md`](mission-2026-11-14/direction-academic-literature.md) F1; [V wave 24B]). [gap19-11]"

**C-R02** (M-R02)
- **Find:** "| Weak nonprofit leverage | Structural ((source: repo inference — no primary URL)) | Medium-High |"
- **Replace with:** "| Weak nonprofit leverage | Structural: the nonprofit is neither the payer nor the legal party, so sponsor revenue does not depend on its satisfaction. [I] inference from [`industry-incentives-structural-analysis.md`](mission-2026-11-14/industry-incentives-structural-analysis.md) (classification table) | Medium-High [gap19-11] |"

**C-R03** (M-R03)
- **Find:** "and discretion-valuing sponsors. ((source: repo inference — no primary URL))"
- **Replace with:** "and discretion-valuing sponsors. [I] inference from [`industry-incentives-structural-analysis.md`](mission-2026-11-14/industry-incentives-structural-analysis.md) §5 (stakeholder table). [gap19-11]"

**C-R04** (M-R04)
- **Find:** "and challengers not paid on assets. ((source: repo inference — no primary URL))"
- **Replace with:** "and challengers not paid on assets. [I] inference from [`industry-incentives-structural-analysis.md`](mission-2026-11-14/industry-incentives-structural-analysis.md) §5 (stakeholder table). [gap19-11]"

**C-R05** (M-R05; applies the pending wave-22 governing item 1 with a citation in place of the marker)
- **Find:** "**Vendor economics.** Ren's corporate revenue, margins and customer concentration are not public ((source: repo inference — no primary URL))."
- **Replace with:** "**Vendor economics.** Ren's corporate revenue, margins and customer concentration are not public: no press, private-equity or registry source gives a figure (repo [`queue-batch37-vendor-economics-owners.md`](mission-2026-11-14/queue-batch37-vendor-economics-owners.md) Q-B06; [V wave 22]). Named Ren receipts in sponsor 990s total $44.98m in TY2024 (18 sponsors). RCF is 42.7% of that and the two Morgan Stanley programs 43.0% (batch 37A §1.2; V wave 22). This is a floor on receipts, limited to sponsors' top-five contractor lines, not Ren revenue. [V wave 33B] [gap19-11]"

**C-R06** (M-R06, plus the stale "2.5–3%" in §4)
- **Find:** "This is a floor: new-charity reviews and declines are invisible in filings ((source: repo inference — no primary URL))."
- **Replace with:** "This is a floor: new-charity reviews and declines are invisible in filings, because no sponsor publishes how it routes grants, how many exceptions it handles or how long review takes (repo [`gap19-exception-load-proxy.md`](mission-2026-11-14/gap19-exception-load-proxy.md) §5). On FY2023–24 Schedule I and F filings the like-for-like measure is about 3.6% of dollars at the four largest nationals. A broader review-need proxy (foreign recipients, recipients outside Pub 78 without an explaining label, rulings within 24 months, named fiscal sponsors, and private foundations or other recipients needing expenditure responsibility: the core proxy) is 10.0% of their dollars and 11.0% across the top 50 (10.96% after the Greater Horizons correction). [V wave 33B] It measures recipients, not observed review (§11.30; [V wave 32A]). [gap19-11]"

**C-R07** (M-R07)
- **Find:** "No sponsor publishes grant turnaround P50/P90, exception rates or reviewer minutes ((source: repo inference — no primary URL))."
- **Replace with:** "No sponsor publishes grant turnaround P50/P90, exception rates or reviewer minutes. No sponsor publishes an SLA or a latency distribution by rail, and only 5 of 28 published turnaround statements are measured, all of them vendor figures (repo [`queue-batch36-metrics-rails.md`](mission-2026-11-14/queue-batch36-metrics-rails.md) P-PAY-05; [V wave 21]). No sponsor publishes human effort or exception rates (repo [`ai-economics-replacement-analysis.md`](mission-2026-11-14/ai-economics-replacement-analysis.md)). [gap19-11]"

**C-R08** (M-R08)
- **Find:** "Customer effects are unobserved ((source: repo inference — no primary URL))."
- **Replace with:** "Customer effects are unobserved: no repo source ties an ownership change to a sponsor-level fee or service change. [I] absence finding from [`private-equity-daf-ecosystem-map.md`](mission-2026-11-14/private-equity-daf-ecosystem-map.md) and [`company-timeline-events.csv`](../data/mission-2026-11-14/company-timeline-events.csv). [gap19-11]"

**C-R09** (M-R09)
- **Find:** "AI economics clear plausible governance costs at vendor or network scale, not per process per sponsor. ((source: repo inference — no primary URL))"
- **Replace with:** "AI economics clear plausible governance costs at vendor or network scale, not per process per sponsor. [I] inference from [`ai-economics-replacement-analysis.md`](mission-2026-11-14/ai-economics-replacement-analysis.md) (redesign mechanism) and [`ai-economics-v2-observed-costs.md`](mission-2026-11-14/ai-economics-v2-observed-costs.md) (the buyer is an administrator or platform). Calibrated to 21 published studies, the ranking is unchanged and the large-national AI value pool falls to $445k (repo [`gap19-ai-calibration.md`](mission-2026-11-14/gap19-ai-calibration.md); [V wave 31A]). [gap19-11]"

**C-R10** (M-R10)
- **Find:** "The single most important missing evidence is a measured exception, handling-time and QA study at any sponsor. ((source: repo inference — no primary URL))"
- **Replace with:** "The single most important missing evidence is a measured exception, handling-time and QA study at any sponsor. [I] inference from [`ai-economics-replacement-analysis.md`](mission-2026-11-14/ai-economics-replacement-analysis.md) (no sponsor publishes human effort or exception rates) and [`gap19-exception-load-proxy.md`](mission-2026-11-14/gap19-exception-load-proxy.md) §5 (Q-N03 still open). [gap19-11]"

**C-R11** (M-R11)
- **Find:** "do sponsor–vendor contracts grant API and data-export rights? ((source: repo inference — no primary URL))"
- **Replace with:** "do sponsor–vendor contracts grant API and data-export rights? [I] inference from [`ai-native-entrant-simulation.md`](mission-2026-11-14/ai-native-entrant-simulation.md) (risk 1); open as Q-N04 in [`FINAL-STATUS.md`](mission-2026-11-14/FINAL-STATUS.md). [gap19-11]"

**C-R12** (M-R12)
- **Find:** "No vendor tests, sponsor interviews or contracts were obtained. ((source: repo inference — no primary URL))"
- **Replace with:** "No vendor tests, sponsor interviews or contracts were obtained (repo [`FINAL-STATUS.md`](mission-2026-11-14/FINAL-STATUS.md), limits). [gap19-11]"

**C-R13** (M-R13; softened)
- **Find:** "- The Wayback Machine could not be read. ((source: repo inference — no primary URL))"
- **Replace with:** "- Wayback Machine page content could not be retrieved from this environment. Only the archive.org availability API worked, so an archived link shows that a capture exists, not what it says (repo [`competitive-history-timelines.md`](mission-2026-11-14/competitive-history-timelines.md); [`FINAL-STATUS.md`](mission-2026-11-14/FINAL-STATUS.md), limits). [gap19-11]"

**C-R14** (M-R14, M-R15; note on the historical instruction)
- **Find:** "1. **Line 146, Vendor economics** (batch 37A §7 proposal 3, validated)."
- **Replace with:** "1. **Line 146, Vendor economics** (batch 37A §7 proposal 3, validated). Applied by gap19-11 C-R05, with a repo citation in place of the marker. [gap19-11]"

**C-R15** (M-R16, M-R17; note on the historical instruction)
- **Find:** "1. **§1, payout (F1, F4).**"
- **Replace with:** "1. **§1, payout (F1, F4).** The first sentence and the DAFRC bullet are applied by gap19-11 C-R01, with a primary citation in place of the marker. The remaining bullets of this item still govern. [gap19-11]"

**C-R20** (§2 status counts; applies wave-31A governing item 3)
- **Find:** "134 confirmed (one more after red-team), 17 historically confirmed, 11 inferred, 5 unknown. A red-team sample of 15 \"confirmed\" edges found 0 status errors and 2 scope imprecisions"
- **Replace with:** "958 confirmed, 23 historically confirmed, 47 inferred, 11 unknown, 5 reported, 3 probable, 2 unverified lead, 1 pending, 1 rejected. A wave-2B red-team sample of 15 \"confirmed\" base edges found 0 status errors and 2 scope imprecisions. A 2026-11-19 red team of all 109 inferred, unknown, reported, probable, pending, vendor-claim and crt.sh-sourced edges (one independent public check each) marked 41 confirmed, 16 weakened, 52 unverified leads and 0 contradicted (repo [`gap19-graph-consolidation.md`](mission-2026-11-14/gap19-graph-consolidation.md); [V wave 31A]) [gap19-11]"

**C-R21** (§9 sentence)
- **Find:** "**Independent validation and red-team review** checked **80 consequential claims**"
- **Replace with:** "**Independent validation and red-team review** checked **80 consequential claims** in waves 1–2B. Later waves bring the registers to 1,036 rows through wave 32B, in 37 files with 1,012 distinct claim IDs (table below; [C] counted by leading result word over `data/mission-2026-11-14/validation-register*.csv`; method in [gap19-11-consistency-pass.md](mission-2026-11-14/gap19-11-consistency-pass.md) §1, caveat in §4; [V wave 33B]) [gap19-11]"

**C-R22** (§9 table)
- **Find:** "| Result | Count |\n|---|---|\n| Confirmed | 45 |\n| Partially confirmed | 25 |\n| Contradicted | 7 |\n| Unable to verify | 3 |"
- **Replace with:** "| Result | Waves 1–2B | All registers through wave 32B [C] |\n|---|---|---|\n| Confirmed | 45 | 784 |\n| Partially confirmed | 25 | 195 |\n| Contradicted | 7 | 32 |\n| Unable to verify | 3 | 15 |\n| Other (audit-defect notes, \"supported\", \"plausible\", \"passed\") | 0 | 10 |\n| **Rows** | **80** | **1,036** [gap19-11] |"

**C-R23** (§9 waves pointer)
- **Find:** "Validation waves 3–12 are reported per wave and listed in §11."
- **Replace with:** "Validation waves 3–32B are reported per wave (`research/mission-2026-11-14/validation-wave*-report.md`) and listed in §11. [gap19-11]"

**C-R24** (housekeeping: duplicate of §11.29 left in the wave-31A appendix)
- **Find:** "5. **New subsection after §11.27.** Add \"### 11.28 Thoroughness pass part A (validated, wave 31A)\", containing the paragraph below. If §11.28 is already taken, use the next free number."
- **Replace with:** "5. **New subsection after §11.27.** Add \"### 11.28 Thoroughness pass part A (validated, wave 31A)\", containing the paragraph below. If §11.28 is already taken, use the next free number. **Applied as §11.29**; the quoted copy below is retained for history and is not a second finding. [gap19-11]"

**C-R25** (§1 vendor footprint, FY2025 refresh)
- **Find:** "or 18 sponsors holding $30.18bn (9.2%) in their latest return [V wave 5]."
- **Replace with:** "or 18 sponsors holding $30.18bn (9.2%) in their latest return [V wave 5]. After the FY2025 filing refresh the latest-return measure is 19 sponsors and $31.56bn, the addition being Ayco's final return. Ayco merged into GS DAPF on 2025-07-01, so it is not a live client. The share is 9.6% of DAFRC FY2024 assets (repo [`validation-wave31a-report.md`](mission-2026-11-14/validation-wave31a-report.md); [`gap19-fy2025-refresh.md`](mission-2026-11-14/gap19-fy2025-refresh.md)). [V wave 33B] [gap19-11]"

**C-R26** (pointer to the consolidated section, §6)
- **Find:** "**Decision-oriented companion:** [strategic synthesis A–G](mission-2026-11-14/strategic-synthesis.md)."
- **Replace with:** "**Decision-oriented companion:** [strategic synthesis A–G](mission-2026-11-14/strategic-synthesis.md). Its §0 (2026-11-19) holds the current governing A–G and top ten; the layered sections after it are kept for history. [gap19-11]"

**Audit fixes in the report (A01–A16).**

**A01** (l.309, needs citation)
- **Find:** "New evidence: GiveClear's audited 2024 statements, which carry an unmodified opinion."
- **Replace with:** "New evidence: GiveClear's audited CY2024 statements (Capin Crouse), which carry an unmodified opinion dated 2025-11-06 (repo [`quadrant-v11-rescore.md`](mission-2026-11-14/quadrant-v11-rescore.md)). [gap19-11]"

**A02** (l.318, needs citation)
- **Find:** "22 of 28 placeable providers landed in the same quadrant."
- **Replace with:** "22 of the 28 providers that both scorers could plot landed in the same quadrant (79%) (repo [`quadrant-v11-blind-and-calibration.md`](mission-2026-11-14/quadrant-v11-blind-and-calibration.md), provider-level table). [gap19-11]"

**A03** (l.396, number-bearing)
- **Find:** "- Excluding Givinga drops the processor share of accounts from 80.5/77.4/79.5% (FY2022/23/24) to 63.0/67.0/66.0% (59.2% for FY2024 on corrected data)."
- **Replace with:** "- Excluding Givinga drops the processor share of accounts from 80.5/77.4/79.5% (FY2022/23/24) to 63.0/67.0/66.0% (59.2% for FY2024 on corrected data) (repo [`sponsor-cost-structure-and-sensitivities.md`](mission-2026-11-14/sponsor-cost-structure-and-sensitivities.md) item 5; [V wave 5]). [gap19-11]"

**A04** (l.421, number-bearing; adds the governing 32.2% floor)
- **Find:** "- Headline shares: about 28% of FY2024 DAF assets on Ren technology in some form;"
- **Replace with:** "- Headline shares: about 28% of FY2024 DAF assets on Ren technology in some form [V wave 3], or 32.2% as a floor on any confirmed Ren/Stellar link in the consolidated graph (repo [`gap19-graph-consolidation.md`](mission-2026-11-14/gap19-graph-consolidation.md) §4; [V wave 31A]); [gap19-11]"

**A05** (l.404, number-bearing)
- **Find:** "- Gross payout is 23.9%. Net payout is 21.5%, 20.8% or 19.0%, depending on how widely sponsor-to-sponsor transfers are defined."
- **Replace with:** "- Gross payout is 23.9%. Net payout is 21.5%, 20.8% or 19.0%, depending on how widely sponsor-to-sponsor transfers are defined (repo [`queue-net-payout-fidelity-outliers.md`](mission-2026-11-14/queue-net-payout-fidelity-outliers.md), segment table; [V wave 11]). [gap19-11]"

**A06** (l.431, number-bearing)
- **Find:** "- 6 of 57 sponsors left, or 10.5% (Wilson interval 4.9–21.1%)."
- **Replace with:** "- 6 of 57 sponsors left, or 10.5% (Wilson interval 4.9–21.1%) (repo [`queue-ren-iphi-attrition.md`](mission-2026-11-14/queue-ren-iphi-attrition.md) item 1). The FY2025 filings show no Ren attrition so far: 10 sponsors name a Ren entity ($3.35m), and all 8 comparable FY2024 payers name Ren again. The largest Ren clients (MS GIFT, RCF, US Charitable Gift Trust, NCF) have not yet filed FY2025 (repo [`gap19-fy2025-refresh.md`](mission-2026-11-14/gap19-fy2025-refresh.md); [V wave 31A]). [V wave 33B] [gap19-11]"

**A07** (l.523, number-bearing)
- **Find:** "- Sponsors charge nonprofits $0 to receive grants. The exceptions are Benevity (2.99%, cap $500), DAFpay at default terms (2.9%) and ForGood (1.5%)."
- **Replace with:** "- Sponsors charge nonprofits $0 to receive grants. The exceptions are Benevity (2.99%, cap $500), DAFpay at default terms (2.9%) and ForGood (1.5%) (repo [`queue-nonprofit-side-panel.md`](mission-2026-11-14/queue-nonprofit-side-panel.md) P-NPT-06; [V wave 12]). [gap19-11]"

**A08** (l.558, needs citation)
- **Find:** "- Pool choice is as large a lever as sponsor choice. Fidelity's 60%-equity pool costs 0.55%; its index pool costs 0.015%."
- **Replace with:** "- Pool choice is as large a lever as sponsor choice. Fidelity's 60%-equity pool costs 0.55%; its index pool costs 0.015% (repo [`queue-all-in-cost-dafpay-access.md`](mission-2026-11-14/queue-all-in-cost-dafpay-access.md); [V wave 10]). [gap19-11]"

**A09** (l.559, needs citation)
- **Find:** "- Edward Jones's 0.70% program fee rests on help pages that now return 404, so it is low confidence."
- **Replace with:** "- Edward Jones's 0.70% program fee rests on a search-index capture of Ren help pages that now return 404, so it is low confidence [V wave 33B] (repo [`queue-all-in-cost-dafpay-access.md`](mission-2026-11-14/queue-all-in-cost-dafpay-access.md); [V wave 10]). [gap19-11]"

**A10** (l.597, number-bearing)
- **Find:** "- None of 21 agentic giving products (2024–26) has independent outcome evidence, and no product touches sponsor approval."
- **Replace with:** "- None of 21 agentic giving products (2024–26) has independent outcome evidence, and no product touches sponsor approval (repo [`queue-agentic-products-dafpay-fees.md`](mission-2026-11-14/queue-agentic-products-dafpay-fees.md) P-INF-08; [V wave 8]). The later census of 30 products finds none that meets the RED test (repo [`direction-ai-product-census.md`](mission-2026-11-14/direction-ai-product-census.md); wave 28). [gap19-11]"

**A11** (l.616, needs citation)
- **Find:** "- AI on the existing workflow ranks first in at most 17% of draws."
- **Replace with:** "- AI on the existing workflow ranks first in at most 17% of draws (repo [`ai-economics-v2-observed-costs.md`](mission-2026-11-14/ai-economics-v2-observed-costs.md)). [gap19-11]"

**A12** (l.618, needs citation)
- **Find:** "- One AI project exceeds the entire IT line of a $250m community foundation in 67% of draws."
- **Replace with:** "- One AI project exceeds the entire IT line of a $250m community foundation in 67% of draws (repo [`ai-economics-v2-observed-costs.md`](mission-2026-11-14/ai-economics-v2-observed-costs.md)). [gap19-11]"

**A13** (l.623, number-bearing)
- **Find:** "- A $120k/yr AI product cannot be funded from process savings below about $1bn of DAF assets."
- **Replace with:** "- A $120k/yr AI product cannot be funded from process savings below about $1bn of DAF assets (repo [`ai-economics-v2-observed-costs.md`](mission-2026-11-14/ai-economics-v2-observed-costs.md), implications item 1, [I] on [S] outputs). [gap19-11]"

**A14** (l.656, needs citation; forecast)
- **Find:** "- Hg exits or uses a continuation vehicle for Benevity (2026–28)."
- **Replace with:** "- Hg exits or uses a continuation vehicle for Benevity (2026–28) [I] (repo [`private-equity-daf-ecosystem-map.md`](mission-2026-11-14/private-equity-daf-ecosystem-map.md), exit-window table). [gap19-11]"

**A15** (l.657, needs citation; forecast plus a dated fact)
- **Find:** "- Apax sells or recapitalises Bonterra (2027–28). Bonterra bought Deed in Mar 2026, putting it head-to-head with Benevity."
- **Replace with:** "- Apax sells or recapitalises Bonterra (2027–28) [I]. Bonterra bought Deed on 2026-03-05, putting it head-to-head with Benevity (repo [`private-equity-daf-ecosystem-map.md`](mission-2026-11-14/private-equity-daf-ecosystem-map.md) item 5 and exit-window table). [gap19-11]"

**A16** (l.658, needs citation; forecast)
- **Find:** "- GTCR sells Foundation Source (2027–29)."
- **Replace with:** "- GTCR sells or recapitalises Foundation Source (2027–29) [I] (repo [`private-equity-daf-ecosystem-map.md`](mission-2026-11-14/private-equity-daf-ecosystem-map.md), exit-window table). [gap19-11]"

### `research/mission-2026-11-14/strategic-synthesis.md`

**C-S01** (M-S01)
- **Find:** "Fund-level payout is not public. ((source: repo inference — no primary URL))"
- **Replace with:** "Fund-level payout is not public in filings: Schedule D Part I reports only sponsor-level aggregates ([IRS Schedule D (Form 990), Rev. Dec 2024](https://www.irs.gov/pub/irs-pdf/f990sd.pdf)). Voluntary samples put the median account's three-year payout at about 9% ([direction-academic-literature.md](direction-academic-literature.md) F1; [V wave 24B]). [gap19-11]"

**C-S02** (M-S02)
- **Find:** "AI only shortens handling), not on the model. ((source: repo inference — no primary URL))"
- **Replace with:** "AI only shortens handling), not on the model. [I] inference from [ai-economics-replacement-analysis.md](ai-economics-replacement-analysis.md) (redesign removes the cause of exceptions; AI can only shorten their handling). [gap19-11]"

**C-S03** (M-S03)
- **Find:** "A process that should not exist; it generates its own exceptions ((source: repo inference — no primary URL))"
- **Replace with:** "A process that should not exist; it generates its own exceptions. In the complaint corpus lost checks become months-long cases, though EFT enrollment is also a complaint source ([gap19-complaints-with-denominators.md](gap19-complaints-with-denominators.md); [V wave 32B]); the mechanism is [I] inference from [ai-economics-replacement-analysis.md](ai-economics-replacement-analysis.md) [gap19-11]"

**C-S04** (M-S04)
- **Find:** "with no contractual API rights, (1) has nothing to run on. ((source: repo inference — no primary URL))"
- **Replace with:** "with no contractual API rights, (1) has nothing to run on. [I] inference from [ai-native-entrant-simulation.md](ai-native-entrant-simulation.md) (risk 1); open as Q-N04 in [FINAL-STATUS.md](FINAL-STATUS.md). [gap19-11]"

**C-S05** (M-S05)
- **Find:** "([Chariot llms.txt](https://www.givechariot.com/llms.txt); (source: repo inference — no primary URL))"
- **Replace with:** "([Chariot llms.txt](https://www.givechariot.com/llms.txt)). \"No one does today\" is [I] inference from [direction-data-standards-interoperability.md](direction-data-standards-interoperability.md): no open multi-sponsor grant-request standard was found, and DAF Direct is closed, with 3 sponsors (wave 25B). [gap19-11]"

**C-S06** (M-S06)
- **Find:** "attested SOC reports that match purchased scope. ((source: repo inference — no primary URL))"
- **Replace with:** "attested SOC reports that match purchased scope. [I] inference from [queue-assurance-everyorg-givinga-monitoring.md](queue-assurance-everyorg-givinga-monitoring.md) P-QA1-04: none of 13 vendors publishes a SOC report with period and system scope **[V wave 5]**. [gap19-11]"

**C-S07** (A5 row, stale "2.5–3%")
- **Find:** "Observable non-standard grants (foreign, fiscal-sponsor, non-501(c)(3)) are about 2.5–3% of dollars at large nationals and far less by count."
- **Replace with:** "Observable non-standard grants (foreign, fiscal-sponsor, non-501(c)(3)) are about 2.5–3% of dollars at large nationals and far less by count. FY2023–24 filings reproduce the measure at about 3.6%, and a broader review-need proxy is 10.0% of the four nationals' dollars and 11.0% across the top 50. That proxy measures recipients, not observed review ([gap19-exception-load-proxy.md](gap19-exception-load-proxy.md); [V wave 32A]). [gap19-11]"

**C-S08** (F row, revision trigger)
- **Find:** "or exception rates far above the 2.5–3% observable non-standard share"
- **Replace with:** "or *measured* exception rates far above the observable non-standard share (2.5–3% for FY6/2025; 3.6% like-for-like in FY2023–24 [V wave 33B]). The 10.0–11.0% review-need proxy is not a measured exception rate and does not trigger this ([gap19-exception-load-proxy.md](gap19-exception-load-proxy.md); [V wave 32A]) [gap19-11]"

**C-S09** (inserts §0 before §A and marks the original A–G as superseded)
- **Find:** "## A. What the DAF industry believes that may be wrong"
- **Note:** insert §6 without its leading "> " quote markers, after applying the wave-33B corrections to §6. The Replace string below is a placeholder and must be substituted by hand, so the checker's tag test does not cover it [V wave 33B].
- **Replace with:** "<the full text of §6 of gap19-11-consistency-pass.md, from \"## 0. Current A–G and top ten\" to its last line>\n\n---\n\n## A. What the DAF industry believes that may be wrong (superseded for current figures by §0) [gap19-11]"

**C-S10** (marks the original top ten as superseded)
- **Find:** "## G. The ten most important discoveries (ranked by strategic significance)"
- **Replace with:** "## G. The ten most important discoveries (ranked by strategic significance; superseded by §0 G, evidence text kept) [gap19-11]"

**C-S11** (marks the wave 14–21 A–G deltas)
- **Find:** "**A. Beliefs that may be wrong.** Two beliefs are now weaker at market level."
- **Replace with:** "*Superseded by §0 for current figures; kept as the wave 14–21 record.* [gap19-11] **A. Beliefs that may be wrong.** Two beliefs are now weaker at market level."

**C-S12** (marks the wave 14–21 top ten)
- **Find:** "### (b) Re-ranked top ten (supersedes the 2026-11-15 list above for ranking only)"
- **Replace with:** "### (b) Re-ranked top ten (supersedes the 2026-11-15 list above for ranking only; itself superseded by §0 G) [gap19-11]"

**C-S13** (marks the wave 22–30 A–G deltas)
- **Find:** "**A. Beliefs that may be wrong.** Several beliefs are now weaker."
- **Replace with:** "*Superseded by §0 for current figures; kept as the wave 22–30 record.* [gap19-11] **A. Beliefs that may be wrong.** Several beliefs are now weaker."

**C-S14** (marks the wave 22–30 top ten)
- **Find:** "### (b) Re-ranked top ten (supersedes the wave 14–21 list for ranking only)"
- **Replace with:** "### (b) Re-ranked top ten (supersedes the wave 14–21 list for ranking only; itself superseded by §0 G) [gap19-11]"

**Audit fixes in the synthesis (A17–A30).**

**A17** (l.106)
- **Find:** "or be priced well below $120k."
- **Replace with:** "or be priced well below $120k ([red-team-wave2a-ai-and-entrant.md](red-team-wave2a-ai-and-entrant.md): \"Preferred research probe: Strategy 3, conditional on measuring operating cost pools\"). [gap19-11]"

**A18** (l.181, top ten #4)
- **Find:** "the dollar effect on Ren is small (Ren/Stellar iPhi holds 5.9% of community-foundation DAF assets)."
- **Replace with:** "the dollar effect on Ren is small (Ren/Stellar iPhi holds 5.9% of community-foundation DAF assets: [queue-cf-vendor-map.md](queue-cf-vendor-map.md); [V wave 9]). FY2025 filings show no Ren attrition so far ([gap19-fy2025-refresh.md](gap19-fy2025-refresh.md); [V wave 31A]). [gap19-11]"

**A19** (l.379, F monitor)
- **Find:** "- Peterson v. WaterStone: pending, with final productions due 2027-02-14. A ruling for the plaintiff would weaken \"every donor lawsuit failed or is pending\" (wave 14)."
- **Replace with:** "- Peterson v. WaterStone: pending, with final productions due 2027-02-14. A ruling for the plaintiff would weaken \"every donor lawsuit failed or is pending\" ([queue-batch29-regulation-litigation-crypto.md](queue-batch29-regulation-litigation-crypto.md) P-CMP-07; [validation-wave14-report.md](validation-wave14-report.md) V14-11). [gap19-11]"

**A20** (l.383, F monitor; adds the FY2025 netting lower bound)
- **Find:** "The netted FY2024 growth of +15.0% depends heavily on transfers to NPT (wave 19)."
- **Replace with:** "The netted FY2024 growth of +15.0% depends heavily on transfers to NPT ([queue-batch34-netting-filings.md](queue-batch34-netting-filings.md); wave 19). In the first FY2025 filings, netting is $3.05–3.80bn (7.1% central) on covered filers, a lower bound ([gap19-fy2025-refresh.md](gap19-fy2025-refresh.md); [V wave 31A]). [gap19-11]"

**A21** (l.384, F monitor)
- **Find:** "A stall would weaken the rail-migration reading (wave 21)."
- **Replace with:** "A stall would weaken the rail-migration reading ([queue-batch36-metrics-rails.md](queue-batch36-metrics-rails.md); [validation-wave21-report.md](validation-wave21-report.md)). [gap19-11]"

**A22** (l.502, wave 22–30 top ten #7; adds the governing graph floor and latest-return count)
- **Find:** "Named receipts are a $44.98m floor in TY2024, 85.8% from three customers (wave 22)."
- **Replace with:** "Named receipts are a $44.98m floor in TY2024, 85.8% from three customers ([queue-batch37-vendor-economics-owners.md](queue-batch37-vendor-economics-owners.md); wave 22). Any confirmed Ren/Stellar link covers 32.2% of FY2024 DAF assets as a floor ([gap19-graph-consolidation.md](gap19-graph-consolidation.md) §4; [V wave 31A]), and 19 sponsors holding $31.56bn name Ren in their latest return. One of them is Ayco's final return, which is not a live client ([validation-wave31a-report.md](validation-wave31a-report.md); [gap19-fy2025-refresh.md](gap19-fy2025-refresh.md)). [V wave 33B] [gap19-11]"

**A23** (l.503, wave 22–30 top ten #8)
- **Find:** "The tail is 2.84% of assets (wave 30)."
- **Replace with:** "The tail is 2.84% of assets ([direction-long-tail-sponsors.md](direction-long-tail-sponsors.md); wave 30). [gap19-11]"

**A24** (l.403, notable items)
- **Find:** "The central sponsor exit bound falls from 1.20% to 0.89% a year (0.44% documented only) (wave 17)."
- **Replace with:** "The central sponsor exit bound falls from 1.20% to 0.89% a year (0.44% documented only) ([queue-batch32-filing-reconciliations.md](queue-batch32-filing-reconciliations.md); [queue-batch33-panel-scans.md](queue-batch33-panel-scans.md); wave 17). [gap19-11]"

**A25** (l.476, E item)
- **Find:** "SVCF reports 539 of the 672 foreign recipients not shown to be 501(c)(3)-equivalent (wave 30)."
- **Replace with:** "SVCF reports 539 of the 672 foreign recipients not shown to be 501(c)(3)-equivalent ([direction-foreign-grants-schedule-f.md](direction-foreign-grants-schedule-f.md); wave 30). [gap19-11]"

**A26** (l.481, F monitor)
- **Find:** "- §4966 regulations: the 2026–27 Priority Guidance Plan lists DAF guidance (item 4). A final rule would revise A9 (wave 24A)."
- **Replace with:** "- §4966 regulations: the 2026–27 Priority Guidance Plan lists DAF guidance (Tax Exempt Organizations, item 4) ([IRS 2026-2027 Priority Guidance Plan](https://www.irs.gov/pub/irs-counsel/2026-2027-initial-pgp.pdf); [direction-policy-lobbying-obbba.md](direction-policy-lobbying-obbba.md)). A final rule would revise A9 (wave 24A). [gap19-11]"

**A27** (l.482, F monitor)
- **Find:** "- State activity: New York A3632 (pending wealth tax that counts DAF gifts); Hawaii's platform law, effective 2026-07-01 (wave 25A)."
- **Replace with:** "- State activity: New York A3632 (pending wealth tax that counts DAF gifts); Hawaii's platform law (Act 205 as amended by Act 108), effective 2026-07-01 ([direction-state-daf-law-tracker.md](direction-state-daf-law-tracker.md); [validation-wave25a-report.md](validation-wave25a-report.md) V25A-08). A 51-jurisdiction bill search found no 2021–2026 state payout, account-reporting or donor-intent mandate; Connecticut could not be checked ([gap19-state-law-50-state-check.md](gap19-state-law-50-state-check.md); [V wave 32B]). [gap19-11]"

**A28** (l.484, F monitor)
- **Find:** "- NPT FY2023: its audited statements would settle whether $22.84bn is a filer error (wave 29)."
- **Replace with:** "- NPT FY2023: its audited statements would settle whether $22.84bn is a filer error ([direction-league-table-concentration.md](direction-league-table-concentration.md); [direction-sponsor-financial-resilience.md](direction-sponsor-financial-resilience.md); wave 29). [gap19-11]"

**A29** (l.509, notable items)
- **Find:** "AEF and Ren first registered on 2024-02-01 (wave 24A)."
- **Replace with:** "AEF and Ren first registered on 2024-02-01 ([direction-policy-lobbying-obbba.md](direction-policy-lobbying-obbba.md); wave 24A). [gap19-11]"

**A30** (l.510, notable items)
- **Find:** "- Grant geography: the top five states take 50.7% of dollars against 21.4% of population (wave 27)."
- **Replace with:** "- Grant geography: the top five states take 50.7% of dollars against 21.4% of population ([direction-grant-geography.md](direction-grant-geography.md); wave 27). [gap19-11]"

The audit-fix count is 30: A01–A16 in the report and A17–A30 in the synthesis.

### 5.4 Check output

Each line is `item | target | occurrences | tag-present`. Pasted from `check_finds.py`, run against the files as they stood on 2026-11-19:

```
C-R01 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
C-R02 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
C-R03 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
C-R04 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
C-R05 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
C-R06 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
C-R07 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
C-R08 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
C-R09 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
C-R10 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
C-R11 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
C-R12 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
C-R13 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
C-R14 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
C-R15 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
C-R20 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
C-R21 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
C-R22 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
C-R23 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
C-R24 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
C-R25 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
C-R26 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
A01 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
A02 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
A03 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
A04 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
A05 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
A06 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
A07 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
A08 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
A09 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
A10 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
A11 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
A12 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
A13 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
A14 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
A15 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
A16 | research/DAF-INDUSTRY-REPORT-2026-11.md | 1 | tag
C-S01 | research/mission-2026-11-14/strategic-synthesis.md | 1 | tag
C-S02 | research/mission-2026-11-14/strategic-synthesis.md | 1 | tag
C-S03 | research/mission-2026-11-14/strategic-synthesis.md | 1 | tag
C-S04 | research/mission-2026-11-14/strategic-synthesis.md | 1 | tag
C-S05 | research/mission-2026-11-14/strategic-synthesis.md | 1 | tag
C-S06 | research/mission-2026-11-14/strategic-synthesis.md | 1 | tag
C-S07 | research/mission-2026-11-14/strategic-synthesis.md | 1 | tag
C-S08 | research/mission-2026-11-14/strategic-synthesis.md | 1 | tag
C-S09 | research/mission-2026-11-14/strategic-synthesis.md | 1 | tag
C-S10 | research/mission-2026-11-14/strategic-synthesis.md | 1 | tag
C-S11 | research/mission-2026-11-14/strategic-synthesis.md | 1 | tag
C-S12 | research/mission-2026-11-14/strategic-synthesis.md | 1 | tag
C-S13 | research/mission-2026-11-14/strategic-synthesis.md | 1 | tag
C-S14 | research/mission-2026-11-14/strategic-synthesis.md | 1 | tag
A17 | research/mission-2026-11-14/strategic-synthesis.md | 1 | tag
A18 | research/mission-2026-11-14/strategic-synthesis.md | 1 | tag
A19 | research/mission-2026-11-14/strategic-synthesis.md | 1 | tag
A20 | research/mission-2026-11-14/strategic-synthesis.md | 1 | tag
A21 | research/mission-2026-11-14/strategic-synthesis.md | 1 | tag
A22 | research/mission-2026-11-14/strategic-synthesis.md | 1 | tag
A23 | research/mission-2026-11-14/strategic-synthesis.md | 1 | tag
A24 | research/mission-2026-11-14/strategic-synthesis.md | 1 | tag
A25 | research/mission-2026-11-14/strategic-synthesis.md | 1 | tag
A26 | research/mission-2026-11-14/strategic-synthesis.md | 1 | tag
A27 | research/mission-2026-11-14/strategic-synthesis.md | 1 | tag
A28 | research/mission-2026-11-14/strategic-synthesis.md | 1 | tag
A29 | research/mission-2026-11-14/strategic-synthesis.md | 1 | tag
A30 | research/mission-2026-11-14/strategic-synthesis.md | 1 | tag
items=66 ok=66 bad=0
sequential apply (C-S09 last): 0 problems
```

## 6. Proposed consolidated section (for strategic-synthesis.md, §0)

The text below is the proposed new section. Links are relative to `research/mission-2026-11-14/`.
- **Figures.** Each figure is the latest validated one: the wave 22–30 layer, then §11.28–§11.31 of the report (waves 31A–32B) and the gap19 documents' governing appendices.
- **Ranking.** The top-ten order is carried over from the wave 22–30 list (the latest validated ranking). No new ranking judgement is introduced; only the evidence lines are refreshed.

> ## 0. Current A–G and top ten (governing, 2026-11-19)
>
> This section is the current reading. It draws its figures from the latest validated sources:
> - the wave 22–30 layer below;
> - the industry report's [§11.28–§11.31](../DAF-INDUSTRY-REPORT-2026-11.md) (waves 31A–32B);
> - the governing appendices of the documents cited.
>
> Where it conflicts with A–G, the wave 14–21 additions or the wave 22–30 additions, this section governs. Those layers are kept for their evidence text and history. **[I]** marks inference; **[S]** marks a scenario figure.
>
> **A. Beliefs that may be wrong**
> - **"Millions of DAF customers."** DAFRC reports 3.59m FY2024 accounts, but 79.5% sit in 22 donation processors holding 0.9% of assets ([regulation-market-structure-portability.md](regulation-market-structure-portability.md)). On corrected FY2024 totals (3.31m accounts, a different basis from DAFRC's 3.59m) the ongoing-advisory basis gives 2.59m, or 0.79m without Givinga and PayPal Giving Fund [V wave 33B] ([queue-batch36-metrics-rails.md](queue-batch36-metrics-rails.md); wave 21). *Contradicted as stated; High.*
> - **"DAFs pay out about 25%."** FY2024 aggregate payout is 25.9%, 22.8% net of DAF-to-DAF transfers and 12.7% at the median sponsor with at least $1m ([queue-batch38-data-followups.md](queue-batch38-data-followups.md); wave 23). The median account pays about 9% over three years in voluntary samples ([direction-academic-literature.md](direction-academic-literature.md) F1; wave 24B). First FY2025 filings net $3.05–3.80bn on covered filers, a lower bound ([gap19-fy2025-refresh.md](gap19-fy2025-refresh.md); wave 31A). *Suggestive; Medium-High on distribution.*
> - **"Three giants dominate."** Sponsor-asset CR3 is 45.5%, CR5 55.8% and HHI 830, unchanged after graph consolidation ([gap19-graph-consolidation.md](gap19-graph-consolidation.md); wave 31A). On the league-table basis, asset concentration rose over FY2021–24 (CR5 51.0% → 56.9%) while grant concentration fell ([direction-league-table-concentration.md](direction-league-table-concentration.md); wave 29). *Partially contradicted; Medium.*
> - **"Ren powers over half of DAF assets."** Any confirmed Ren/Stellar link covers 32.2% of FY2024 DAF assets as a floor ($105.6bn, 54 sponsors; 32.9% with six EIN-unmatched sponsors) ([gap19-graph-consolidation.md](gap19-graph-consolidation.md) §4; wave 31A). NPT, 12.8% of FY2024 DAF assets ($42.12bn of $327.87bn, per the wave-31A text), still rests on hosting evidence alone [V wave 33B]; no second source names Ren as NPT's vendor ([gap19-second-source-pass.md](gap19-second-source-pass.md) C01; wave 31B). 19 sponsors holding $31.56bn name Ren in their latest 990. One of them is Ayco's final return, which is not a live client ([validation-wave31a-report.md](validation-wave31a-report.md); [gap19-fy2025-refresh.md](gap19-fy2025-refresh.md)). [V wave 33B] *Unsupported on public evidence; Medium.*
> - **"Grant approval is the bottleneck."**
>   - The like-for-like non-standard share is about 3.6% of the four largest nationals' FY2023–24 dollars.
>   - A broader review-need proxy is 7.4% of top-50 recipient lines and 11.0% of dollars. That proxy measures recipients, not review ([gap19-exception-load-proxy.md](gap19-exception-load-proxy.md); wave 32A).
>   - Grants to EINs under an IRS revocation are 0.082% of top-50 Schedule I dollars ([direction-recipient-compliance-screen.md](direction-recipient-compliance-screen.md); wave 26).
>
>   *Suggestive; Medium.*
> - **"Donors can move a DAF easily."** None of 12 sponsors publishes an outbound transfer policy ([sponsor-transfer-portability-terms.csv](../../data/mission-2026-11-14/sponsor-transfer-portability-terms.csv)). NPT is the one top-10 sponsor documenting a donor export (Excel) ([queue-batch38-vendors-ledgers-portals.md](queue-batch38-vendors-ledgers-portals.md); wave 23). *Suggestive; Medium-High.*
> - **"The 2023 regulations are imminent; states will act."** The rules are still proposed, and the docket holds 249 submissions ([direction-policy-lobbying-obbba.md](direction-policy-lobbying-obbba.md); wave 24A). A 51-jurisdiction search found no 2021–2026 state payout, reporting or donor-intent mandate; Connecticut was not checked ([gap19-state-law-50-state-check.md](gap19-state-law-50-state-check.md); wave 32B). *High on federal status; Medium on states.*
> - **"Challengers are cheaper; adviser fees are capped."**
>   - All-in cost at $250k runs from 0.26% (Daffy) to 2.13% (San Francisco Foundation) ([queue-all-in-cost-dafpay-access.md](queue-all-in-cost-dafpay-access.md); wave 10).
>   - Only MS GIFT, DAFgiving360 and TIFIN Give/GiveClear publish an adviser-fee cap, at 1.00%. MS GIFT's cap excludes Legacy Pools and Select UMA manager fees, and Fidelity CIAP, NPT, AEF and RCF publish none ([queue-all-in-cost-dafpay-access.md](queue-all-in-cost-dafpay-access.md); [validation-wave10-report.md](validation-wave10-report.md) V10-05; [queue-adviser-fees-pools-npact.md](queue-adviser-fees-pools-npact.md)). [V wave 33B]
>   - Fidelity's active asset-allocation pools trail benchmarks by about its admin fee over five years [I] ([direction-investment-menus-performance.md](direction-investment-menus-performance.md); waves 27, 31B).
>
>   *Suggestive; Medium.*
> - **"AI agents can give safely on a donor's behalf."** No product of 30 meets the RED test. Only TIFIN Louise and Daffy's MCP server can move DAF money ([direction-ai-product-census.md](direction-ai-product-census.md); wave 28). *Unsupported; Medium.*
> - **"A DAF is more tax-efficient than giving directly."** For itemizers the tax is identical. For non-itemizers a DAF loses from 2026 ([direction-donor-tax-scenarios-2026.md](direction-donor-tax-scenarios-2026.md); wave 27; illustrative). *Contradicted; Medium-High.*
> - **"Complaint rates show service quality."** Among the 15 largest sponsors, only Fidelity Charitable and RCF have review-venue records at all. Fidelity's rate is 1.32 per 10,000 accounts, and the ranking against AOGF flips with the denominator ([gap19-complaints-with-denominators.md](gap19-complaints-with-denominators.md); wave 32B). *Contradicted as a quality measure; Medium.*
> - **"DAF startups fail often."** 18 entrants from 2021–2026 show no documented shutdown: 10 active, 1 acquired, 1 pivoted, 6 unknown ([gap19-startup-cohort.md](gap19-startup-cohort.md); wave 32A). *Suggestive; Low-Medium (small n).*
>
> **B. What AI changes.** The flag-only rule (AI may add a flag, never clear one) still governs ([ai-governance-failure-modes.md](ai-governance-failure-modes.md)).
> - Inference cost is immaterial: about $0.45 per heavy review against about $83 of reviewer time ([ai-economics-replacement-analysis.md](ai-economics-replacement-analysis.md); wave 2A).
> - Calibrated to 21 published studies, the large-national AI value pool is $445k ($202k–$793k across framings; $110k on the all-touched basis). Shared-platform break-even falls to 16% of draws, and no process changes its most likely winner [S] ([gap19-ai-calibration.md](gap19-ai-calibration.md); wave 31A).
> - AI work is at vendors: AI appears in 29.1% of vendor job postings (44 of 151) against 13.3% of sponsor postings (2 of 15, a small sample) [V wave 33B] ([direction-news-hiring-signals.md](direction-news-hiring-signals.md); wave 24B).
> - First-party reading of 13 of 20 entities (7 were blocked) found none documenting AI in grant approval, eligibility or money movement. This is an absence finding; the wave-31B validator spot-checked 12 [V wave 33B] ([gap19-ai-coverage-20-entities.md](gap19-ai-coverage-20-entities.md); wave 31B).
>
> **C. Where incumbents are vulnerable**
> - **Shared single points of failure.** RCF pays Ren 98% of individual-fundholder admin-fee revenue ($19.23m, FY2024) ([RCF FY2024 audited statements](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf)). Named Ren receipts are a $44.98m floor, 85.8% from three customers ([queue-batch37-vendor-economics-owners.md](queue-batch37-vendor-economics-owners.md); wave 22).
> - **Community-foundation cost gap.** Median admin fees are 100 / 100 / 67 bps at $100k / $1m / $10m, about 1.7x / 2.2x / 3.6–4.7x the nationals' ([direction-cf-consolidation-fees.md](direction-cf-consolidation-fees.md); waves 25A, 31B).
> - **Legacy attrition.** Ren iPhi lost 6 of 57 sponsors in 2023–Nov 2026 ([queue-ren-iphi-attrition.md](queue-ren-iphi-attrition.md); wave 11). FY2025 filings show no Ren attrition yet ([gap19-fy2025-refresh.md](gap19-fy2025-refresh.md); wave 31A).
> - **Unproven challenger claims.** Give Interactive's nine known clients hold $36.74bn on DNS evidence, of which only $23.90bn rests on first-party or filing evidence. It lost three community-foundation tenants, not five ([crtsh-resourcing-2026-11-19.md](crtsh-resourcing-2026-11-19.md); wave 31B).
> - **Assurance and service.** None of 13 vendors publishes a scoped SOC report ([queue-assurance-everyorg-givinga-monitoring.md](queue-assurance-everyorg-givinga-monitoring.md); wave 5). No readable top-20 sponsor publishes a response-time promise ([direction-sponsor-accessibility-service.md](direction-sponsor-accessibility-service.md); wave 25A).
> - **Not vulnerable.** Fidelity holds 20.5–21.7% of corrected assets every year in FY2021–24 ([direction-league-table-concentration.md](direction-league-table-concentration.md); wave 29). Foundant serves 282 of 351 tail community foundations with an identified vendor ([direction-long-tail-sponsors.md](direction-long-tail-sponsors.md); wave 30). [V wave 33B]
>
> **D. What entrants should avoid building**
> - **Credential-based integrations.** Six of the top 20 sponsors (about $84bn) contractually limit automated or third-party access ([queue-batch34-escheat-terms.md](queue-batch34-escheat-terms.md); wave 19).
> - **Waiting for an open rail.** No open multi-sponsor grant-request standard exists ([direction-data-standards-interoperability.md](direction-data-standards-interoperability.md); wave 25B).
> - **Holding donor funds.** Losses occurred only where one operator held unsegregated funds ([failed-daf-startups-deep-research.md](failed-daf-startups-deep-research.md)).
> - **A standalone long-tail business** [I]. The 1,240 sponsors under $50m hold 2.84% of assets ([direction-long-tail-sponsors.md](direction-long-tail-sponsors.md); wave 30).
> - **Selling the DAF as tax-superior** to a direct gift (wave 27).
>
> **E. What becomes more valuable**
> - **Distribution access.** The fastest-growing sponsors are channel- or platform-led [I] ([direction-sponsor-marketing-spend.md](direction-sponsor-marketing-spend.md); wave 28).
> - **Nonprofit identity and remittance data.** Only 36% of sponsors default to sharing full contact data ([direction-nonprofit-side-experience.md](direction-nonprofit-side-experience.md); wave 29).
> - **Measured latency.** Only 5 of 28 published turnaround statements are measured ([queue-batch36-metrics-rails.md](queue-batch36-metrics-rails.md); wave 21).
> - **Retained, dated eligibility evidence** [I] ([direction-recipient-compliance-screen.md](direction-recipient-compliance-screen.md); wave 26).
> - **Local knowledge.** Community foundations keep 60.0% of US grant dollars in-state, against 7.6% for nationals ([direction-grant-geography.md](direction-grant-geography.md); wave 27).
>
> **F. What would change our conclusions** (the existing F table and monitors still apply)
> - A measured exception, handling-time and QA study at any sponsor (Q-N03) ([gap19-exception-load-proxy.md](gap19-exception-load-proxy.md) §5).
> - One executed sponsor–vendor contract with API or export terms (Q-N04) ([FINAL-STATUS.md](FINAL-STATUS.md)).
> - The 26 top-50 FY2025 returns not yet indexed: re-run netting, concentration and the Ren footprint ([gap19-fy2025-refresh.md](gap19-fy2025-refresh.md)).
> - A second source on NPT's Ren relationship (C01) ([gap19-second-source-pass.md](gap19-second-source-pass.md)).
> - Peterson v. WaterStone ([queue-batch29-regulation-litigation-crypto.md](queue-batch29-regulation-litigation-crypto.md)) and any final §4966 rule, or guidance under the new 2026–27 item on §§4966 and 6033 DAF arrangements. The §4967 prohibited-benefits project, which would have codified the Notice 2017-73 pledge rule, has left the plan ([IRS 2026-2027 Priority Guidance Plan](https://www.irs.gov/pub/irs-counsel/2026-2027-initial-pgp.pdf); [b41n16-b42n20-daf-tax-guidance.md](b41n16-b42n20-daf-tax-guidance.md)). [V wave 33B]
> - A Daffy MCP cap or confirmation step ([direction-ai-product-census.md](direction-ai-product-census.md)).
>
> **G. Top ten (order carried from the wave 22–30 list; evidence refreshed)**
> 1. **Donor data and automation are contractually closed, and no open standard fills the gap.** Six of the top 20 limit automated access ([queue-batch34-escheat-terms.md](queue-batch34-escheat-terms.md)). DAF Direct is closed, with 3 sponsors ([direction-data-standards-interoperability.md](direction-data-standards-interoperability.md)). NPT's Excel export is the one top-10 exception ([queue-batch38-vendors-ledgers-portals.md](queue-batch38-vendors-ledgers-portals.md)). Executed contracts remain unseen ([FINAL-STATUS.md](FINAL-STATUS.md) Q-N04).
> 2. **Most "DAF accounts" are not DAF customers.** DAFRC reports 3.59m accounts. On corrected totals (3.31m, a different basis) the ongoing-advisory count is 2.59m [V wave 33B], or 0.79m without Givinga and PayPal Giving Fund ([queue-batch36-metrics-rails.md](queue-batch36-metrics-rails.md)). The long tail's 46.4% of accounts is 3.49% without Givinga and BNY Mellon CGF ([direction-long-tail-sponsors.md](direction-long-tail-sponsors.md)).
> 3. **Market payout and growth are overstated by transfers between sponsors.** FY2024: 25.9% aggregate, 22.8% net, 12.7% at the median sponsor ([queue-batch38-data-followups.md](queue-batch38-data-followups.md)). Netted grants are $58.41bn ([queue-batch34-netting-filings.md](queue-batch34-netting-filings.md)). FY2025 covered-filer netting is $3.05–3.80bn so far, a lower bound ([gap19-fy2025-refresh.md](gap19-fy2025-refresh.md)).
> 4. **Nonprofits bear the cost of fragmented rails and thin donor data.** Any DAF option appears on 41.2% of top donate pages (a lower bound), and DAFpay on 13.7% ([direction-nonprofit-donate-pages.md](direction-nonprofit-donate-pages.md)). Processor complaints describe payout rules: paper-check thresholds, lost checks and EFT vetting ([gap19-complaints-with-denominators.md](gap19-complaints-with-denominators.md); wave 32B).
> 5. **Donor cost sits in fund and adviser layers the 990 does not show.** Program-service revenue is $0 at all 15 affiliated sponsors ([direction-sponsor-financial-resilience.md](direction-sponsor-financial-resilience.md)). Fidelity's fee-sized shortfall holds over five years for its active pools [I] ([direction-investment-menus-performance.md](direction-investment-menus-performance.md); wave 31B).
> 6. **Community foundations carry a structural cost gap.** Admin fees are 1.7–4.7x the nationals', on 37 schedules covering 46% of top-100 CF DAF assets ([direction-cf-consolidation-fees.md](direction-cf-consolidation-fees.md); wave 31B). Staff cost is 78.7 bps against 2.9 bps ([direction-sponsor-executive-compensation.md](direction-sponsor-executive-compensation.md)).
> 7. **Ren's footprint is below its claims.** The confirmed-link floor is 32.2% of assets ([gap19-graph-consolidation.md](gap19-graph-consolidation.md)). Named receipts are a $44.98m floor, 85.8% from three customers ([queue-batch37-vendor-economics-owners.md](queue-batch37-vendor-economics-owners.md)). NPT remains hosting-only evidence ([gap19-second-source-pass.md](gap19-second-source-pass.md) C01).
> 8. **The platform market is segmented, and Foundant holds the long tail.** Foundant serves 282 of 351 tail community foundations with an identified vendor ([direction-long-tail-sponsors.md](direction-long-tail-sponsors.md)). Give Interactive's first-party-evidenced book is $23.90bn of a $36.74bn DNS-evidenced client set ([crtsh-resourcing-2026-11-19.md](crtsh-resourcing-2026-11-19.md)).
> 9. **Agentic products are donor-side and unproven.** None of 30 meets the RED test, and only two can move DAF money ([direction-ai-product-census.md](direction-ai-product-census.md)). No re-read entity documents AI in approval ([gap19-ai-coverage-20-entities.md](gap19-ai-coverage-20-entities.md)).
> 10. **The operations-AI value pool is thin.** The calibrated large-national pool is $445k and break-even falls to 16% of draws [S] ([gap19-ai-calibration.md](gap19-ai-calibration.md)). The review-need proxy (11.0% of top-50 dollars) bounds what could need review, but no observed review data exist ([gap19-exception-load-proxy.md](gap19-exception-load-proxy.md)).
>
> **Notable, outside the top ten.**
> - 42.2% of covered DAF dollars go to recipients that report any lobbying (median intensity 0.20%) ([direction-recipient-lobbying.md](direction-recipient-lobbying.md)).
> - International grants are 7.8% of DAF grants with direct foreign grants included ([direction-foreign-grants-schedule-f.md](direction-foreign-grants-schedule-f.md)).
> - NPT passed DAFgiving360 for #2 in FY2024 ([direction-league-table-concentration.md](direction-league-table-concentration.md)).
> - The startup cohort shows no documented shutdown ([gap19-startup-cohort.md](gap19-startup-cohort.md)). [gap19-11]

## 7. Results and limits

**Results.**
- **Markers.** 17 in the report and 6 in the synthesis, not 18 and 7. For the 19 body markers the proposals are: 7 citation replacements, 12 `[I]` relabels (one item, M-S03, combines a citation with a relabel), and 1 softening (the Wayback limit, which was contradicted as worded). The 4 markers quoted in the correction appendix get historical notes.
- **Citation audit.** 225 lines flagged: 9 need a citation, 207 are cited by an internal pointer only, and 9 are false positives.
- **Stale figures.** One governing correction was never applied: the wave-31A §2 status counts. The §9 table covers waves 1–2B only; the registers now hold 1,036 rows. The "2.5–3%" exception share appears without the wave-32A 3.6% / 10.0% / 11.0% context in report §4 and synthesis A5 and F. The §1 latest-return Ren count is now 19 sponsors and $31.56bn.

**Limits.**
- **Triage is mechanical.** "Internal pointer only" is generous: a lead-in that cites a whole document counts as support for every sub-bullet. The 30 fixes were checked against the cited files by text search, not by re-validating each claim.
- **§9 tallies are by register row, not claim.** The leading-word map is coarse (§4 caveat).
- **The consolidated §0 is drafted, not validated.** Every figure in it is copied from a validated document. It needs an independent validation pass before it governs. Wave 33B validated it; with the corrections in [validation-wave33b-report.md](validation-wave33b-report.md) applied, it may govern [V wave 33B].
- **Not checked.** No primary URL other than the IRS Schedule D PDF was re-fetched. The report sections not named in the task (§10, the remainder of §11, the source register) were checked only through the audit.

## 8. Source register and robots log

| ID | Source | Use | Access |
|---|---|---|---|
| P1 | [IRS Schedule D (Form 990), Rev. December 2024](https://www.irs.gov/pub/irs-pdf/f990sd.pdf) | Part I lines 1–4: number of DAFs; aggregate contributions, grants and end-of-year value | Fetched 2026-11-19T18:02Z, HTTP 200, user agent `research-script/1.0` |
| P2 | [About Schedule D (Form 990)](https://www.irs.gov/forms-pubs/about-schedule-d-form-990) | Confirms Schedule D carries DAF reporting | Fetched 2026-11-19, HTTP 200 |
| P3 | [DAFRC 2024 National Study executive summary](https://johnsoncenter.org/wp-content/uploads/2024/02/DAFRC_Executive_Summary_Key_Findings.pdf) | Account-level payout (quoted from the wave-24B governing correction; not re-fetched) | Repo |
| P4 | [IRS 2026-2027 Priority Guidance Plan](https://www.irs.gov/pub/irs-counsel/2026-2027-initial-pgp.pdf) | Item 4 (already cited in both files; not re-fetched) | Repo |
| P5 | [RCF FY2024 audited statements](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf) | 98% / $19.23m (already cited; not re-fetched) | Repo |
| R | Repo documents and CSVs linked inline | All other figures | Local read |

**robots.txt log.** `https://www.irs.gov/robots.txt` was fetched on 2026-11-19 (HTTP 200). The `User-agent: *` group disallows only the `/forms-pubs-*-search` paths and lists no `/pub/` rule, so P1 and P2 are allowed. No other host was contacted.

## 9. Data dictionary: `data/mission-2026-11-14/queue-proposals-gap19-11.csv`

The columns match `queue-proposals-gap19-13.csv`:
- `question_id` (P-G1911-nn);
- `question`;
- `area`;
- `importance`, `p_change`, `gap`, `commercial`, `availability` and `effort`: 1–5 scores, with p_change a probability from 0 to 1;
- `depends_on`;
- `breadth_gap` (yes/no);
- `state` (open);
- `assigned_to` (blank);
- `conclusion_affected`;
- `proposed_by`;
- `rationale`;
- `evidence_pointer`.
