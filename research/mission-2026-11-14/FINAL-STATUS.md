# Final status report: DAF research mission (2026-11-14 → 2026-11-15)

**Every count below was computed from the repository, not estimated.** The commands are listed in each row.

## Repository and branch
- **Repository:** `kemiller2002/daf-landscape`. Integration branch `main`.
- **Working branch:** `claude/daf-landscape-research-tdxdiq`. This is the branch the session was authorized to use. Merging to `main` is through **draft PR #20**: https://github.com/kemiller2002/daf-landscape/pull/20. Nothing was force-pushed and no research was deleted.
- **Final commit SHA:** a file cannot contain the SHA of the commit that adds it. The PR #20 description records the head SHA after this file was committed. The parent of the commit that adds this file is `1b8f763`.
- **Pre-existing open PRs:** #1 and #16 are left untouched.

## Counts (refresh 2026-11-19, through PR #59) — governing

Recomputed from the repository on branch `claude/daf-landscape-research-tdxdiq` just before PR #59 merged. These counts supersede the tables below. The PR #59 description records the head SHA.

| Item | Count | How computed |
|---|---|---|
| Pull requests merged in this mission | #20–#59 (40 PRs) | GitHub |
| Research documents | 301 documents, 1,107,759 words | `research/**/*.md` |
| Datasets | 570 CSV files, 258,236 data rows | `data/**/*.csv` (headers excluded) |
| Unique URLs cited in research markdown | 3,839 | regex over `research/**/*.md` |
| Independent validation | **1,439 register rows** in 48 register files (waves 1–36C): 1,054 confirmed, 309 partially confirmed, 52 contradicted, 17 unverifiable, 7 other | `validation-register*.csv`, classified by the leading word of `validation_result` |
| Research queue | 711 items: 349 done, 231 open, 75 blocked, 50 monitoring, 5 deprioritized historical, 1 declined | `research-priority-queue.csv`, `state` |
| Industry report | §11.1–§11.41 | `research/DAF-INDUSTRY-REPORT-2026-11.md` |

**Additions in PR #59 (validated; report §11.39–§11.41):**
- **Community-foundation locality.** Across 95 of the top-100 community foundations, the median CF keeps 83% of grant dollars in its own state. In-state share falls about 2.5 points for every 10 points of DAF share. This is an association, not a measured effect, and a composition reading fits the data equally well. Omaha's figures rest on a truncated filing, and Armstrong County was ranked on a DAFRC data error.
- **Corporate DAFs.** 13 of 14 sponsors publish no corporate split. Where the split is measured, corporate DAFs are 3.4–3.9% of DAF grants; 9.1% is a ceiling that applies only to the measured pool.
- **Unlisted recipients.** About 4% of the $0.82bn of top-50 grants to unlisted EINs is identifiable sponsor EIN misreporting. The roughly 51% that is "unmatched" is an upper bound on grantees the IRS lists do not recognise.
- **Large single grants.** SVCF's $1.309bn FY2023 line went to Further Future Foundation, now Navigation Charitable Fund. That fund owns Voltage Park and had granted out 3.1% of the money by end-2024.
- **AI routing.** Confidence-gated routing roughly triples intervention C's value pool, but only when an escaped error costs about one case-handling's worth or less. C still almost never ranks first.
- **Exceptions per grant.** Measured by number of grants, about 7–8.5% fall in the core exception categories.
- **NPT and Ren follow-ups.**
  - The $116.3m that had been called "asset management fees" is in fact program services excluding grants. Five passages were corrected.
  - The full-contact Ren guide went live between 2026-10-06 and 2026-11-10.
  - Reading the instructions, NPT's Schedule R line 1b should arguably read Yes. This is an interpretation.

## Counts (refresh 2026-11-19, through PR #58) (superseded by the table above)

These counts were recomputed from the repository on branch `claude/daf-landscape-research-tdxdiq` just before PR #58 merged, and supersede the tables below. The PR #58 description records the head SHA.

| Item | Count | How computed |
|---|---|---|
| Pull requests merged in this mission | #20–#58 (39 PRs) | GitHub |
| Research documents | 293 documents, 1,068,274 words | `research/**/*.md` |
| Datasets | 556 CSV files, 219,447 data rows | `data/**/*.csv` (headers excluded) |
| Unique URLs cited in research markdown | 3,784 | regex over `research/**/*.md` |
| Independent validation | **1,349 register rows** in 45 register files (waves 1–35C): 992 confirmed, 285 partially confirmed, 48 contradicted, 17 unverifiable, 7 other | `validation-register*.csv`, classified by the leading word of `validation_result` |
| Research queue | 685 items: 338 done, 216 open, 75 blocked, 50 monitoring, 5 deprioritized historical, 1 declined | `research-priority-queue.csv`, `state` |
| Industry report | §11.1–§11.38 | `research/DAF-INDUSTRY-REPORT-2026-11.md` |

**Additions in PR #58 (validated; report §11.36–§11.38):**
- **Tail admin-fee pool.** CFs-only central estimate is about $90m. The whole-tail figure of about $138m is an upper bracket, with a range of $76m–$184m, replacing the $92m hypothetical.
- **Schedule I purpose text cannot measure donor restrictions.** About half of dollars carry generic text, about half carry sector labels, and about 1–2% have a specific purpose.
- **Ren acknowledgement defaults track guide vintage.** The evidence shows neither a sponsor setting nor a platform limit.
- **Adviser-managed assets.** The share is 46.9% at Fidelity Charitable and 0% at Vanguard. DAFgiving360 is only bracketed and NPT cannot be estimated.
- **NPT foreign grants.** None of NPT's FY2023–24 foreign grants went to related organisations as filed (Schedule R Part V line 1b = No). Part V excludes only NPT's own transactions with its disregarded entities; on the repo's reading of Appendix F, a disregarded entity's grants to a related organisation are NPT's, so the filed No is a weak test [V wave 36C] In FY2025, £30.9m went from NPT Transatlantic to NPT UK.
- **The $6.18bn "church" block is about half congregations.** Faith sponsors send about 22–26% of it, and none of the 14 congregation giving pages read offers a DAF option.

**Process note.** A correction-applier bug truncated replacement text at inner double quotes. It was found in wave 35B and fixed. The 17 affected passages from waves 34S/34A/34B were repaired and audited against their reports.

## Counts (refresh 2026-11-19, through PR #57) (superseded by the table above)

Recomputed from the repository on branch `claude/daf-landscape-research-tdxdiq` just before PR #57 merged. These figures supersede the tables below. The PR #57 description records the head SHA.

| Item | Count | How computed |
|---|---|---|
| Pull requests merged in this mission | #20–#57 (38 PRs) | GitHub |
| Research documents | 285 documents, 1,025,124 words | `research/**/*.md` |
| Datasets | 542 CSV files, 216,399 data rows | `data/**/*.csv` (headers excluded) |
| Unique URLs cited in research markdown | 3,752 | regex over `research/**/*.md` |
| Independent validation | **1,249 register rows** in 42 register files (waves 1–34B, including 34S): 932 confirmed, 250 partially confirmed, 43 contradicted, 17 unverifiable, 7 other | `validation-register*.csv`, classified by the leading word of `validation_result` |
| Research queue | 661 items: 330 done, 200 open, 75 blocked, 50 monitoring, 5 deprioritized historical, 1 declined | `research-priority-queue.csv`, `state` |
| Industry report | §11.1–§11.35 | `research/DAF-INDUSTRY-REPORT-2026-11.md` |

**Additions in PR #57 (validated; report §11.34–§11.35, synthesis §0 wave 34S):**
- **Synthesis §0 validated.** No figures were wrong. 14 wording and scope corrections were applied, including that the review-need proxy is an indicator, not a bound, and that the staff-cost gap is about 3.5–9×.
- **NPT FY2023 Schedule D is understated.** NPT's consolidated statements give net assets of $28.51bn. The filed value stays in the headline series, and a sensitivity variant shows FY2023 market assets of $261.44bn. All top-50 imputed FY2024 rows had already been replaced, and the headline totals are unchanged.
- **Donor-information defaults at the top-20 sponsors.** Neither "withheld by default" nor "shared by default" holds as a rule. Full contact is the documented default for 33.2% of assets and withholding for 17.2%; the default is undocumented for 44.6%.
- **DAF share of recipient giving.** On the private-giving proxy (1h − 1d − 1e), the median is 7.7% and the pooled share 10.3%. 76.5–76.9% of top-50 DAF dollars go to recipients eligible for a Charity Navigator rating.
- **Long-tail fee census.** 7 of 60 sampled tail sponsors (11.7%) publish a 2021+ admin rate. Tail community foundations that do publish charge a median 150 bps at $100k.

## Counts (refresh 2026-11-19, through PR #56) (superseded by the table above)

These counts were recomputed from the repository on branch `claude/daf-landscape-research-tdxdiq` just before PR #56 merged. They supersede the tables below. The PR #56 description records the head SHA.

| Item | Count | How computed |
|---|---|---|
| Pull requests merged in this mission | #20–#56 (37 PRs) | GitHub |
| Research documents | 278 documents, 992,042 words | `research/**/*.md` |
| Datasets | 530 CSV files, 213,229 data rows | `data/**/*.csv` (headers excluded) |
| Unique URLs cited in research markdown | 3,706 | regex over `research/**/*.md` |
| Independent validation | **1,128 register rows** in 39 register files (waves 1–33B): 847 confirmed, 219 partially confirmed, 39 contradicted, 16 unverifiable, 7 other (audit or defect rows) | `validation-register*.csv`, classified by the leading word of `validation_result`. This differs slightly from the per-wave tallies used in earlier tables |
| Research queue | 640 items: 322 done, 187 open, 75 blocked (reasons recorded), 50 monitoring, 5 deprioritized historical, 1 declined | `research-priority-queue.csv`, `state` |
| Industry report | §11.1–§11.33 | `research/DAF-INDUSTRY-REPORT-2026-11.md` |
| Strategic synthesis | New §0, "Current A–G and top ten (governing)". Older layers are marked superseded | `strategic-synthesis.md` |

**Additions since PR #53 (all validated; report §11.30–§11.33):**
- **Exception-load proxy.** Across the top 50 sponsors, 7.4% of recipient lines and 11.0% of dollars need non-routine review.
- **Complaints.** Measured against accounts and grants, grant delay is the top complaint category. Processor complaint rates run far above sponsors' rates per grant dollar.
- **State law.** A 50-state check found no state DAF mandate. New Jersey's hospital-conversion clause is the one reach into DAF money.
- **Startup cohort.** Survival for the 2021–26 startup cohort is 64.7–100%.
- **Recipient revenue.** Top-50 DAF grants are a median 5.9% (pooled 6.9%) of recipients' contributions.
- **Long-tail costs.** Tail community foundations' allocated DAF cost is about 205 bps, 1.6–2.2× the top-50 community foundations.
- **Processor rules.** Processors' published disbursement rules include thresholds, cadence and redirection.
- **Pledges.** Notice 2017-73 §4 still governs DAF pledge payments.
- **Sponsor tax pages.** Their OBBBA errors are documented: Vanguard's bunching example, DAFgiving360's "inflation adjustment", and a calculator with no floor or cap.
- **Consistency pass.** 66 edits were applied, including 7 citations added, 12 relabels and 1 softening.

## Counts (refresh 2026-11-19, through PR #53) (superseded by the table above)

Recomputed from the repository at merge commit `7932eb4` (PR #53). Supersedes the tables below.

| Item | Count | How computed |
|---|---|---|
| Pull requests merged in this mission | #20–#53 (34 PRs) | GitHub |
| Research documents | 265 documents, 920,517 words | `research/**/*.md` |
| Datasets | 507 CSV files, 208,707 data rows | `data/**/*.csv` (headers excluded) |
| Unique URLs cited in research markdown | 3,584 | regex over `research/**/*.md` |
| Independent validation | **944 register rows** in 35 register files (waves 1–31B): 724 confirmed, 175 partially confirmed, 24 contradicted, 14 unverifiable, 7 audit rows | `validation-register*.csv`; waves 31A (33/8/1/1) and 31B (32/9/0/1) added to the PR #50 totals |
| Research queue | 591 items: 311 done, 75 blocked (reasons recorded), 50 monitoring, 149 open, 5 deprioritized historical, 1 declined | `research-priority-queue.csv`, `state` |
| Industry report | §11.1–§11.29 | `research/DAF-INDUSTRY-REPORT-2026-11.md` |
| Owner-directed new research directions | 33 (N1–N33), all validated | `research/mission-2026-11-14/direction-*.md` |

**Thoroughness pass, 2026-11-19 (validated, report §11.28–§11.29):**
- The coverage matrix was rebuilt from post-baseline evidence, and all 20 AI cells marked "not investigated" now have findings.
- Ten single-source claims got a second source.
- The AI-economics behavioural assumptions were calibrated against public evidence. The break-even for intervention C falls from 43% to 16%.
- Edward Jones and four thin wealth channels were profiled from public filings.
- The relationship graph was consolidated to up to 893 nodes and 1,051 edges.
- Fee and announced-versus-delivered evidence was refreshed. The delivery table now reads 17 delivered, 11 partial, 9 with no evidence and 2 contradicted.
- FY2025 filings were refreshed where the IRS index has them.
- crt.sh and certspotter are disabled for robots compliance, and claims that rested only on them are now leads.

## Counts (final refresh 2026-11-15 ~17:30 UTC, through PR #50) (superseded by the table above)

Recomputed from the repository at merge commit `20a0eb8` (PR #50). Supersedes the tables below.

| Item | Count | How computed |
|---|---|---|
| Pull requests merged in this mission | #20–#50 (31 PRs) | GitHub |
| Research documents | 248 documents, 835,836 words | `research/**/*.md` |
| Datasets | 470 CSV files, 176,636 data rows | `data/**/*.csv` (headers excluded) |
| Unique URLs cited in research markdown | 3,424 | regex over `research/**/*.md` |
| Independent validation | **859 register rows** in 33 register files (waves 1–30): 659 confirmed, 158 partially confirmed, 23 contradicted, 12 unverifiable, 7 audit rows | `validation-register*.csv`, `validation_result` |
| Research queue | 536 items: 299 done, 75 blocked (reasons recorded), 49 monitoring, 107 open, 5 deprioritized historical, 1 declined | `research-priority-queue.csv` |
| Industry report | §11.1–§11.27 | `research/DAF-INDUSTRY-REPORT-2026-11.md` |
| Owner-directed new research directions | 33 (N1–N33), all validated | `research/mission-2026-11-14/direction-*.md` |

**Seventh-round additions (validated, report §11.27):** direct foreign grants are 1.92% of top-50 sponsors' grants ($1.89bn over FY2023–24), lifting the international sector share from 5.6% to 7.8%; about 42% of covered DAF grant dollars go to charities that report any lobbying, with median lobbying intensity of about 0.2% of expenses (descriptive, lawful activity); 1,240 sponsors under $50m hold 2.84% of assets, pay out less (median 11.7%) and account for nearly all entries and exits.

## Counts (final refresh 2026-11-15 ~16:50 UTC, through PR #48) (superseded by the table above)

Recomputed from the repository at merge commit `ed840bd` (PR #48). Supersedes the tables below.

| Item | Count | How computed |
|---|---|---|
| Pull requests merged in this mission | #20–#48 (29 PRs) | GitHub |
| Research documents | 244 documents, 817,983 words | `research/**/*.md` |
| Datasets | 463 CSV files, 153,340 data rows | `data/**/*.csv` (headers excluded) |
| Unique URLs cited in research markdown | 3,422 | regex over `research/**/*.md` |
| Independent validation | **821 register rows** in 32 register files (waves 1–29): 625 confirmed, 154 partially confirmed, 23 contradicted, 12 unverifiable, 7 audit rows | `validation-register*.csv`, `validation_result` |
| Research queue | 524 items: 296 done, 75 blocked (reasons recorded), 49 monitoring, 98 open, 5 deprioritized historical, 1 declined | `research-priority-queue.csv` |
| Industry report | §11.1–§11.26 | `research/DAF-INDUSTRY-REPORT-2026-11.md` |
| Owner-directed new research directions | 30 (N1–N30), all validated | `research/mission-2026-11-14/direction-*.md` |

**Sixth-round additions (validated, report §11.26):** national sponsors hold almost no own money visible on the 990 (some show negative non-DAF net assets); nonprofits' top DAF pain is not knowing the donor, driven by sponsor defaults; DAF-specific polls exist mainly from reform advocates and show majority support for payout rules alongside low awareness; Fidelity leads every year and asset concentration rose while grant concentration fell (FY2021–24). NPT's FY2023 Schedule D DAF value is a real filed figure out of line with its balance sheet — likely a filer error carried into DAFRC.

**Open items note:** the 98 open items are mostly agent-generated follow-ups from the 30 new directions; none is required for the report's conclusions.

## Counts (final refresh 2026-11-15 ~16:10 UTC, through PR #46) (superseded by the table above)

Recomputed from the repository at merge commit `0ead3d8` (PR #46). Supersedes the tables below.

| Item | Count | How computed |
|---|---|---|
| Pull requests merged in this mission | #20–#46 (27 PRs) | GitHub |
| Research documents | 239 documents, 792,725 words | `research/**/*.md` |
| Datasets | 453 CSV files, 152,403 data rows | `data/**/*.csv` (headers excluded) |
| Unique URLs cited in research markdown | 3,371 | regex over `research/**/*.md` |
| Independent validation | **785 register rows** in 31 register files (waves 1–28): 597 confirmed, 148 partially confirmed, 22 contradicted, 11 unverifiable, 7 audit rows | `validation-register*.csv`, `validation_result` |
| Research queue | 509 items: 292 done, 75 blocked (reasons recorded), 49 monitoring, 87 open, 5 deprioritized historical, 1 declined | `research-priority-queue.csv` |
| Industry report | §11.1–§11.25 | `research/DAF-INDUSTRY-REPORT-2026-11.md` |
| Owner-directed new research directions | 26 (N1–N26), all validated | `research/mission-2026-11-14/direction-*.md` |

**Fifth-round additions (validated, report §11.25):** sponsors tied to financial firms show little advertising or officer pay on their own 990s because parents bear it (cost appears as administrator or trustee fees); community foundations spend far more per new account. Of 30 philanthropy AI products, none is RED; only TIFIN Louise and Daffy's MCP server touch DAF money (both AMBER). No sponsor shows charity ratings inside its grant flow; Charity Navigator rates about 17% of eligible charities and its licence restricts AI use.

**Compliance (added):** wave 28 found one fetch of an irs.gov path that irs.gov's robots.txt disallows; its facts were relabelled as carried from earlier repository sources.

## Counts (final refresh 2026-11-15 ~15:30 UTC, through PR #44) (superseded by the table above)

Recomputed from the repository at merge commit `9450c05` (PR #44). Supersedes the tables below.

| Item | Count | How computed |
|---|---|---|
| Pull requests merged in this mission | #20–#44 (25 PRs) | GitHub |
| Research documents | 234 documents, 767,051 words | `research/**/*.md` |
| Datasets | 443 CSV files, 150,460 data rows | `data/**/*.csv` (headers excluded) |
| Unique URLs cited in research markdown | 3,309 | regex over `research/**/*.md` |
| Independent validation | **746 register rows** in 30 register files (waves 1–27 incl. 2A/2B, 24A/24B, 25A/25B): 570 confirmed, 139 partially confirmed, 19 contradicted, 11 unverifiable, 7 audit rows | `validation-register*.csv`, `validation_result` |
| Research queue | 493 items: 288 done, 75 blocked (reasons recorded), 49 monitoring, 75 open, 5 deprioritized historical, 1 declined | `research-priority-queue.csv` |
| Industry report | §11.1–§11.24 | `research/DAF-INDUSTRY-REPORT-2026-11.md` |
| Owner-directed new research directions | 22 (N1–N22), all validated | `research/mission-2026-11-14/direction-*.md` |

**Fourth-round additions (validated, report §11.24):** only 6 of the top 20 sponsors (a verified floor) publish pool returns against benchmarks; index menus track within ~0.1 pp. Illustrative 2026 tax scenarios (not tax advice) show a DAF is equivalent to a direct gift for itemizers and worse for non-itemizers. Five states receive half of DAF grant dollars; community foundations keep 60% in-state versus 7.6% for nationals. A 28-sponsor feature census separates table stakes from differentiators.

## Counts (final refresh 2026-11-15 ~14:55 UTC, through PR #42) (superseded by the table above)

Every number below was recomputed from the repository at merge commit `3627b5c` (PR #42). It supersedes the PR #40 table that follows.

| Item | Count | How computed |
|---|---|---|
| Pull requests merged in this mission | #20–#42 (23 PRs) | GitHub |
| Research documents (markdown under `research/`) | 229 documents, 748,250 words | file walk over `research/**/*.md` |
| Datasets (CSV under `data/`) | 430 files, 145,199 data rows | file walk over `data/**/*.csv` (header rows excluded) |
| Unique URLs cited in research markdown | 3,234 | regex over `research/**/*.md` |
| Independent validation | **710 register rows** in 29 register files (waves 1, 2A, 2B, 3–23, 24A, 24B, 25A, 25B, 26): 539 confirmed, 134 partially confirmed, 19 contradicted, 11 unverifiable, 7 audit/defect rows | `data/mission-2026-11-14/validation-register*.csv`, column `validation_result` |
| Research queue | 477 items: 284 done, 75 blocked (each with a recorded reason), 49 monitoring, 63 open, 5 deprioritized historical, 1 declined (no outreach) | `data/mission-2026-11-14/research-priority-queue.csv` |
| Industry report | §11.1–§11.23 | `research/DAF-INDUSTRY-REPORT-2026-11.md` |
| Owner-directed new research directions | 18 (N1–N18), all validated (waves 24A–26) | `research/mission-2026-11-14/direction-*.md` |

**Third-round additions (validated, report §11.23):** church platforms rarely carry a DAF rail (Overflow via Chariot is the exception); university gift offices split on whether DAF grants can pay pledges, and none read lets DAF grants buy event benefits; a recipient compliance screen of 604,915 top-50 grant lines finds revoked-at-grant-year hits of $74.8m (0.082%), mostly later reinstated — all framed as screening hits, not improper grants; 49 corporate DAF programs found in SEC filings.

## Counts (final refresh 2026-11-15 ~14:15 UTC, through PR #40) (superseded by the table above)

Every number below was recomputed from the repository at merge commit `a17d759` (PR #40).

| Item | Count | How computed |
|---|---|---|
| Pull requests merged in this mission | #20–#40 (21 PRs) | GitHub |
| Research documents (markdown under `research/`) | 224 documents, 726,837 words | file walk over `research/**/*.md` |
| Datasets (CSV under `data/`) | 420 files, 139,679 data rows | file walk over `data/**/*.csv` (header rows excluded) |
| Unique URLs cited in research markdown | 3,107 | regex over `research/**/*.md` |
| Independent validation | **673 register rows** in 28 register files (waves 1, 2A, 2B, 3–23, 24A, 24B, 25A, 25B): 508 confirmed, 129 partially confirmed, 19 contradicted, 10 unverifiable, 7 audit/defect rows | `data/mission-2026-11-14/validation-register*.csv`, column `validation_result` |
| Research queue | 461 items: 280 done, 75 blocked (each with a recorded reason), 49 monitoring (await future filings), 51 open, 5 deprioritized historical, 1 declined (no outreach) | `data/mission-2026-11-14/research-priority-queue.csv` |
| Coverage matrix | 33 entities, 396 cells; 62.6% investigated; 14.4% partially validated or better | `scripts/mission_coverage.py` |
| Industry report | §11.1–§11.22 (§11.9–§11.22 added after batch 28) | `research/DAF-INDUSTRY-REPORT-2026-11.md` |

**Open items.** The 51 open items are mostly narrow refinements generated by agents in the last rounds (queue proposals). The 75 blocked items need partner data, signed contracts or SOC reports, gated registries or forms, human retrieval, or sites that refuse automated access or disallow it in robots.txt. The 49 monitoring items wait for CY2025/FY2026 filings, court rulings or quarterly fund filings.

**Compliance.** crt.sh's robots.txt disallows all crawlers; claims resting only on its data are unverified leads and all crt.sh calls are disabled ([compliance-note-crtsh-robots.md](compliance-note-crtsh-robots.md)). Agents disclosed a small number of fetches made before robots.txt was read; that content was discarded or flagged in the relevant validation reports. No outreach was made. An exposed credential seen on a vendor site earlier in the mission was not used or reproduced.

### Main additions since batch 28 (all validated; see report §11.9–§11.22)
- **Market totals netted for DAF-to-DAF transfers:** FY2024 grants $58.41bn, payout 22.8% (25.9% gross; median sponsor 12.7%) ([queue-batch34-netting-filings.md](queue-batch34-netting-filings.md)).
- **Account metric restated:** 2.59m FY2024 accounts on an ongoing-advisory basis (0.79m excluding Givinga and PayPal Giving Fund) ([queue-batch36-metrics-rails.md](queue-batch36-metrics-rails.md)).
- **Where DAF money goes:** $77.34bn to ~174k recipients net of DAF-to-DAF; education 25.8%, human services 14.3% ([direction-recipients-impact-matching.md](direction-recipients-impact-matching.md)).
- **Agent access:** no top-20 sponsor names software as an appointable agent; Daffy is wrapped by third-party agent tools with unscoped keys ([queue-batch35-agents-analysts-rails.md](queue-batch35-agents-analysts-rails.md), [queue-batch36-agent-terms-controls.md](queue-batch36-agent-terms-controls.md)).
- **No open DAF data standard;** grant metadata does not travel with payments ([direction-data-standards-interoperability.md](direction-data-standards-interoperability.md)).
- **Nonprofit side:** 41.2% of top DAF recipients' donate pages show any DAF option, 13.7% DAFpay ([direction-nonprofit-donate-pages.md](direction-nonprofit-donate-pages.md)).
- **Policy:** the 2023 proposed DAF regulations remain proposed, with a new May–June 2026 comment batch; no state has a DAF reporting or payout law ([direction-policy-lobbying-obbba.md](direction-policy-lobbying-obbba.md), [direction-state-daf-law-tracker.md](direction-state-daf-law-tracker.md)).
- **Community foundations:** median admin fee about 1.7×, 2.2× and 3.6–4.7× national sponsors at $100k, $1m and $10m ([direction-cf-consolidation-fees.md](direction-cf-consolidation-fees.md)).
- **International:** payout floors abroad apply to funds as a whole, never to accounts ([direction-international-comparison.md](direction-international-comparison.md)).

## Counts (superseded — refreshed 2026-11-15, after queue batches through #28)

| Item | Count | How computed |
|---|---|---|
| Pull requests merged | #20–#27 merged; #28 merges with this refresh | GitHub |
| Research documents (markdown) | 81 → 164, ~449k words | `scripts/mission_inventory.py` |
| Datasets | 60 → 348; 112,166 data rows | Most rows are machine-harvested Form 990, DAFRC, BDC and CF-portal panels |
| **Sources: curated unique URLs in narrative documents** | **~1,850+** (baseline 431) | Narrative markdown only. Bulk machine-harvested filing URLs are counted separately. |
| **Organizations investigated** | ~300 sponsors, vendors, investors and channels with sourced profiles; 89 interested firms; 50 venture cases; ~60 companies in the PE ownership map; **1,512 sponsors** with parsed Form 990 data; **803 community foundations** scanned for portal vendors (481 mapped) | Respective datasets |
| **Independent validation** | **253 validation-register rows across 13 waves**: 177 confirmed (incl. with caveats or corrections), ~54 partially confirmed or weakly supported, 10 contradicted or refuted, 3 unable to verify, and 8 consolidation-audit rows (all fixed) | `validation-register*.csv` |
| **Evidence Quadrants** | v1.1 calibrated (42 providers, 5 areas); v1.2 targeted update for BofA CGF, MS GIFT and NCF | quadrant docs |
| **Consolidation** | Report §11 rewritten thematically; synthesis A–G and top 10 re-ranked; originals archived; changelog and wave-13 audit | `consolidation-changelog.md`, `validation-wave13-report.md` |
| Research queue | 139 done, 28 monitoring, 18 blocked (partner data, gated registries, unreachable archives, API credentials), 5 deprioritized historical, 1 declined (no outreach), 128 open (mostly narrow refinements) | `research-priority-queue.csv` |
| Coverage matrix | 62.6% of entity cells investigated; 14.4% partially validated or better | `scripts/mission_coverage.py` |

## Most important new discoveries

The full ranked list with evidence, uncertainty, implications and next actions is in [strategic-synthesis.md §G](strategic-synthesis.md).

1. **Most DAF "accounts" are pass-through processor accounts.** They are 79.5% of accounts and hold 0.9% of assets. ([DAFRC Updated Analysis memo](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf); [DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`dafrc-sponsor-schedule-d-fy2019-2024.csv`](../../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv)) Traditional invested accounts number at most 737k. ([DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`regulation-market-structure-portability.md`](../../research/mission-2026-11-14/regulation-market-structure-portability.md))
2. **Software is two markets plus one captive market.** About 39% of assets sit at affiliate-linked nationals. ([Fidelity Charitable FY2025 audited statements](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf); [DAFgiving360 FY2025 results](https://www.dafgiving360.org/press-release/fiscal-year-2025-results); [Vanguard Charitable FY2025 financial statements](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf); [DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`validation-register-wave2b.csv`](../../data/mission-2026-11-14/validation-register-wave2b.csv)) Fully outsourced administration covers ≥6 sponsors holding 9.1% of assets. ([DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`regulation-market-structure-portability.md`](../../research/mission-2026-11-14/regulation-market-structure-portability.md)) The community-foundation long tail is on Foundant. ([Foundant CommunitySuite page](https://www.foundant.com/products/communitysuite/); [Tech Impact CF software landscape](https://techimpact.org/sites/default/files/2024-03/TECH%20IMPACT%20Integrated%20Software%20for%20Community%20Foundations.pdf))
3. **Apparently independent wealth-firm DAFs share one sponsor–vendor spine (RCF + Ren).** ([RCF FAQ](https://renaissancecharitable.org/faqs/); [Edward Jones Charitable Gift Fund portal](https://edwardjones.donorfirstx.com/); [Ameriprise RCF portal](https://ampf.donorfirstx.com/); [RBC RCF portal](https://rbcrcf.donorfirstx.com/); [Ren LPL RCF page](https://www.reninc.com/lpl-rcf-daf/); [Ren UBS RCF page](https://www.reninc.com/why-ubs-advisors-choose-rcf/); [SEI Giving Fund portal](https://sei.donorfirstx.com/); [MDRT Global Gift Fund portal](https://mdrt.donorfirstx.com/); repo [`relationship-graph-edges.csv`](../../data/mission-2026-11-14/relationship-graph-edges.csv)) Ren's DFX portal also fronts Morgan Stanley GIFT (new), Bank of America's fund and AEF ([MS GIFT donor portal](https://msgift.donorfirstx.com/); [BofA Charitable Gift Fund portal](https://bofa.donorfirst.org/); [AEF/Ren release, Apr 2026](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/)), and Ren-owned iPhi serves the Cleveland Foundation and ImpactAssets. ([Cleveland Foundation iPhi portal](https://www.iphiview.com/tcf/LogIn/tabid/444/Default.aspx); [ImpactAssets homepage (iPhi log-in)](https://impactassets.org/))
4. **Ren's ">half of DAF assets" claim is not reachable on public evidence, though Ren's footprint is about three times earlier estimates.** ([Ren homepage](https://www.reninc.com/); [Great Hill investment in Ren (Pulse 2.0)](https://pulse2.com/great-hill-partners-announces-strategic-growth-investment-in-donor-advised-fund-platform-ren/)) On public evidence, sponsors holding about **28%** of FY2024 DAF assets ($91.6bn of $327.9bn) use Ren technology in some form **[V wave 3]**. The full Form 990 harvest (all 1,512 sponsors) finds Ren/Stellar named by 30 sponsors holding $48.55bn (14.8%) in any FY2022–25 return, but only 18 sponsors holding $30.18bn (9.2%) in their latest return [V wave 5], and about 5% (RCF, MS GIFT) on Ren-paid administration. Nearly half of the 28% is NPT, evidenced by hosting (iPhi login redirect, shared Ren load balancer, Ren-hosted "NPT iPhi Statuspage") rather than a disclosed contract **[I: hosting inference, single-source]**. A 2026-11-19 second-source pass found no NPT filing, privacy-policy processor list, product article or Ren page naming Ren as NPT's vendor; Ren is not among NPT's five listed FY2025 contractors (the fifth is paid $220,927) ([gap19-second-source-pass.md](gap19-second-source-pass.md) C01) ([MS GIFT 990 via GivingTuesday mirror; Goldman PWM portal gspf.goldman.com; NPT GivingPoint](validation-wave3-report.md)). Ren's "60%+"/"about half" claims remain unreachable without Fidelity Charitable, DAFgiving360 or Vanguard Charitable, none of which shows a Ren vendor; Vanguard chose Give Interactive. (Earlier estimates: 8.7% → 9.0% → 28% after NPT and Goldman evidence.) ([DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`validation-register-wave2b.csv`](../../data/mission-2026-11-14/validation-register-wave2b.csv)) <!-- CITE-CHECK RESOLVED 2026-11-14 (text corrected): Validator V2B-05 recomputed $29.65bn = 9.04% for RCF, AEF, MS GIFT and BofA from DAFRC FY2024 (all imputed); the 8.7% ($28.5bn) figure was only partially confirmed. Not changed. -->, and the "$200bn" figure includes non-DAF assets. ([AEF/Ren release, Apr 2026](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/))
5. **The value pool for DAF operations AI is thin, and redesign should precede AI.** The model's "AI ranks last" result is an artifact of its assumptions. ([Anthropic API pricing](https://platform.claude.com/docs/en/about-claude/pricing); [BLS compliance officers (May 2025)](https://www.bls.gov/ooh/business-and-financial/compliance-officers.htm); [BLS ECEC June 2026](https://www.bls.gov/news.release/ecec.nr0.htm); repo [`ai-process-economics.csv`](../../data/mission-2026-11-14/ai-process-economics.csv); repo [`validation-register-wave2a.csv`](../../data/mission-2026-11-14/validation-register-wave2a.csv))
6. **The agentic AI frontier is donor-side**, through TIFIN Give's Louise and Daffy's MCP server. ([TIFIN Give Louise release](https://www.prnewswire.com/news-releases/tifin-give-launches-louise-ai-capabilities-for-philanthropy-302595069.html); [Daffy MCP docs](https://docs.daffy.org/agents/mcp)) No public evidence shows AI in sponsor-side approval. (repo [`ai-use-case-inventory.csv`](../../data/mission-2026-11-14/ai-use-case-inventory.csv); repo [`validation-register-wave2a.csv`](../../data/mission-2026-11-14/validation-register-wave2a.csv))
7. **Payout splits behind the average.** The median sponsor pays out about 11–12.5%, and about one in five sponsors with ≥$1m pays out under 5%. ([DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`derived-metrics.csv`](../../data/mission-2026-11-14/derived-metrics.csv); repo [`scripts/mission_daf_metrics.py`](../../scripts/mission_daf_metrics.py))
8. **Fee pass-through is near-total at RCF.** RCF pays Ren 98% of its individual-fundholder admin-fee revenue. ([RCF FY2024 audited statements](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf); [RCF FY2023 audited statements](https://renaissancecharitable.org/wp-content/uploads/2026/01/2023RCFAuditedFinancialStatements.pdf); repo [`rcf-ren-audited-admin-payments-2020-2024.csv`](../../data/rcf-ren-audited-admin-payments-2020-2024.csv)) The causal effect on payout is unsupported, and segment medians run against it. ([DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`validation-register-wave2b.csv`](../../data/mission-2026-11-14/validation-register-wave2b.csv))
9. **Portability is a legal right with operational lock-in.** No sponsor publishes an outbound transfer policy or offers history portability. ([GTCF DAF transfer instructions](https://www.gtcf.org/wp-content/uploads/2026.05.18-GTCF_DAF_Transfer_Instructions.pdf); [Daffy help: closing an account](http://help.daffy.org/en/articles/6520234-how-do-i-close-my-daffy-account); [AEF DonorCentral sunset notice](https://engage.aefonline.org/dc-sunset/) ([archived copy](http://web.archive.org/web/20261003000017/https://engage.aefonline.org/dc-sunset/)); repo [`sponsor-transfer-portability-terms.csv`](../../data/mission-2026-11-14/sponsor-transfer-portability-terms.csv))
10. **A previously unknown vendor, Give Interactive, says it holds Vanguard Charitable's DAF recordkeeping [vendor claim; not in Vanguard Charitable's FY2026 audited statements].** ([Give Interactive / Vanguard Charitable release](https://www.giveinteractive.com/post/vanguard))

## Contradictions and unresolved questions

**Resolved contradictions:**
- **Concentration:** CR3 58% vs 45.5% came from a period mismatch; 45.5% is correct. ([Fidelity Charitable FY2025 audited statements](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf); [DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`validation-register-wave2b.csv`](../../data/mission-2026-11-14/validation-register-wave2b.csv))
- **NPT FY2025 grants:** $6.44bn is the U.S. DAF program; $6.61bn likely includes the U.K. ([NPT FY2025 annual report](https://www.nptrust.org/annual-reports/npt-annual-report/); [NonProfit Times on NPT FY2025](https://thenonprofittimes.com/?p=215695))
- **SPLC grant holds:** confirmed by the California AG's release. ([California AG release](https://oag.ca.gov/node/623769))

**Contradicted prior claims:**
- The Bank of America 10-K evidence of Ren. The only evidence is the portal. ([SEC full-text search, BofA filings](https://efts.sec.gov/LATEST/search-index?q=%22Charitable%20Gift%20Fund%22&ciks=0000070858); [BofA CGF Form 990 TY2024](https://projects.propublica.org/nonprofits/organizations/46010342/202503219349318170/full); [BofA Charitable Gift Fund portal](https://bofa.donorfirst.org/))
- Chariot's "Fidelity electronic-only by July 2026". Not confirmed; about 67% of Fidelity grants already go by EFT. ([Chariot on Fidelity's 2026 Giving Report](https://www.givechariot.com/resources/insights/top-8-takeaways-from-fidelity-charitables-2026-giving-report); [Fidelity Charitable nonprofit FAQ](https://www.fidelitycharitable.org/nonprofits/faqs.html))
- The entrant model's "model-assisted clearing". Reconciled to deterministic clearing only. (repo [`validation-register-wave2a.csv`](../../data/mission-2026-11-14/validation-register-wave2a.csv); repo [`ai-governance-failure-modes.md`](../../research/mission-2026-11-14/ai-governance-failure-modes.md))

**Still unresolved:**
- Ren's denominator for its share claims. ([Ren homepage](https://www.reninc.com/); [Great Hill investment in Ren (Pulse 2.0)](https://pulse2.com/great-hill-partners-announces-strategic-growth-investment-in-donor-advised-fund-platform-ren/))
- Ren's SOC 2 Type 1 vs Type 2 statements. ([AEF/Ren release, Jul 2025](https://www.aefonline.org/thought-leadership/american-endowment-foundation-selects-ren-as-a-strategic-partner-to-expand-philanthropy-drive-innovation-and-foster-growth-in-financial-services/); [AEF/Ren release, Apr 2026](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/))
- Sponsor, administrator and technology vendor for the Edward Jones private DAF and Goldman Sachs. ([Edward Jones elevated wealth management release](https://www.edwardjones.com/us-en/why-edward-jones/news-media/press-releases/elevated-wealth-management))
- Give Interactive's scope at Vanguard Charitable. ([Give Interactive / Vanguard Charitable release](https://www.giveinteractive.com/post/vanguard))
- Whether sponsor–vendor contracts grant API and data-export rights.
- Real exception rates and handling times anywhere in the market.
- Fund-level payout by fee model.
- Content of the forthcoming §4966/6033 guidance. ([IRS 2026-2027 Priority Guidance Plan](https://www.irs.gov/pub/irs-counsel/2026-2027-initial-pgp.pdf))
- Builders of the NCF and SVCF Salesforce portals.
- Funding and AI evidence for Endaoment, Goodstack, Every.org and Grantable.

## Research coverage and limitations
- **Public sources only.** No vendor demos, contracts, interviews or sponsor operational data were obtained.
- **Search and archive limits.** The shared web-search budget was exhausted mid-mission. Several sites blocked automated access (Every.org, JCF, the Chicago Community Trust and GKCCF portals, dafgiving360.org, tifin.com, congress.gov). The Wayback Machine could only confirm that snapshots exist, not show their content.
- **Scenario numbers.** All AI and entrant cost figures are labelled scenarios. The red team showed that the rankings depend on unsourced amenability and redesign-share assumptions.
- **Coverage denominator.** The coverage matrix covers a purposive set of 33 entities. 18 of them still have a majority of checklist items not investigated, mostly wealth channels other than Edward Jones, faith and community sponsors, and new vendors.
- **Validation ceiling.** Validation is independent of the authoring agent but uses the same model family. Under the EDF claim policy this is cross-agent checking, not cross-executor reproducibility.

## Highest-value next investigations
Ranked by expected information value in `research-priority-queue.csv` (open questions only):
1. **Q-N02:** Give Interactive's scope at Vanguard Charitable and its client list.
2. **Q-B04:** Goldman Sachs and Morgan Stanley GIFT administration and technology stack.
3. **Q-N01:** Ren's share-claim denominator, including whether NPT is counted through Stellar/iPhi.
4. **Q-N04:** API and data-export rights in sponsor–vendor contracts. This is the gating question for any entrant.
5. **Q-N05:** spend limits and authority separation in TIFIN Louise and Daffy MCP.
6. **Q-B18:** whether Givinga and DAF Direct are multi-sponsor infrastructure.
7. **Q-N03:** a sponsor time-and-motion study of exception rate, handling minutes and QA. It ranks lower only because public availability is low. It is the gating evidence for every AI-economics conclusion and should be pursued through an authorized partner.

---

## Source register

Every external URL cited inline in this document, deduplicated, in order of first citation. Dates are publication or access dates as recorded in the repository's workstream source registers and validation registers.

- DAFRC Updated Analysis memo (Apr 2026; accessed 2026-11-14): https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf
- DAFRC Updated Analysis dataset (Spring 2026; accessed 2026-11-14): https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx
- Fidelity Charitable FY2025 audited statements (FYE 2025-06-30): https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf
- DAFgiving360 FY2025 results (2025-07-29): https://www.dafgiving360.org/press-release/fiscal-year-2025-results
- Vanguard Charitable FY2025 financial statements (FYE 2025-06-30): https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf
- Foundant CommunitySuite page (accessed 2026-11-14): https://www.foundant.com/products/communitysuite/
- Tech Impact CF software landscape (Jul 2022): https://techimpact.org/sites/default/files/2024-03/TECH%20IMPACT%20Integrated%20Software%20for%20Community%20Foundations.pdf
- RCF FAQ (live 2026-11-14): https://renaissancecharitable.org/faqs/
- Edward Jones Charitable Gift Fund portal (live 2026-11-14): https://edwardjones.donorfirstx.com/
- Ameriprise RCF portal (live 2026-11-14): https://ampf.donorfirstx.com/
- RBC RCF portal (live 2026-11-14): https://rbcrcf.donorfirstx.com/
- Ren LPL RCF page (live 2026-11-14): https://www.reninc.com/lpl-rcf-daf/
- Ren UBS RCF page (live 2026-11-14): https://www.reninc.com/why-ubs-advisors-choose-rcf/
- SEI Giving Fund portal (live 2026-11-14): https://sei.donorfirstx.com/
- MDRT Global Gift Fund portal (live 2026-11-14): https://mdrt.donorfirstx.com/
- MS GIFT donor portal (live 2026-11-14): https://msgift.donorfirstx.com/
- BofA Charitable Gift Fund portal (live 2026-11-14): https://bofa.donorfirst.org/
- AEF/Ren release, Apr 2026 (2026-04-08): https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/
- Cleveland Foundation iPhi portal (accessed 2026-11-14): https://www.iphiview.com/tcf/LogIn/tabid/444/Default.aspx
- ImpactAssets homepage (iPhi log-in) (accessed 2026-11-14): https://impactassets.org/
- Ren homepage (live 2026-11-14): https://www.reninc.com/
- Great Hill investment in Ren (Pulse 2.0) (2025-10-28): https://pulse2.com/great-hill-partners-announces-strategic-growth-investment-in-donor-advised-fund-platform-ren/
- Anthropic API pricing (read 2026-11-14): https://platform.claude.com/docs/en/about-claude/pricing
- BLS compliance officers (May 2025) (accessed 2026-11-14): https://www.bls.gov/ooh/business-and-financial/compliance-officers.htm
- BLS ECEC June 2026 (released 2026-09-09): https://www.bls.gov/news.release/ecec.nr0.htm
- TIFIN Give Louise release (2025-10-27): https://www.prnewswire.com/news-releases/tifin-give-launches-louise-ai-capabilities-for-philanthropy-302595069.html
- Daffy MCP docs (accessed 2026-11-14): https://docs.daffy.org/agents/mcp
- RCF FY2024 audited statements (FYE 2024-12-31; accessed 2026-11-14): https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf
- RCF FY2023 audited statements (FYE 2023-12-31; accessed 2026-11-14): https://renaissancecharitable.org/wp-content/uploads/2026/01/2023RCFAuditedFinancialStatements.pdf
- GTCF DAF transfer instructions (2026-05-18): https://www.gtcf.org/wp-content/uploads/2026.05.18-GTCF_DAF_Transfer_Instructions.pdf
- Daffy help: closing an account (2026-04-02): http://help.daffy.org/en/articles/6520234-how-do-i-close-my-daffy-account
- AEF DonorCentral sunset notice (2026-10-31): https://engage.aefonline.org/dc-sunset/
- Give Interactive / Vanguard Charitable release (2025-11-04): https://www.giveinteractive.com/post/vanguard
- NPT FY2025 annual report (FY ended 2025-06-30): https://www.nptrust.org/annual-reports/npt-annual-report/
- NonProfit Times on NPT FY2025 (2025-12-01): https://thenonprofittimes.com/?p=215695
- California AG release (2026-05-22): https://oag.ca.gov/node/623769
- SEC full-text search, BofA filings (run 2026-11-14): https://efts.sec.gov/LATEST/search-index?q=%22Charitable%20Gift%20Fund%22&ciks=0000070858
- BofA CGF Form 990 TY2024 (e-filed 2025-11-17): https://projects.propublica.org/nonprofits/organizations/46010342/202503219349318170/full
- Chariot on Fidelity's 2026 Giving Report (2026-03-24): https://www.givechariot.com/resources/insights/top-8-takeaways-from-fidelity-charitables-2026-giving-report
- Fidelity Charitable nonprofit FAQ (live 2026-11-14): https://www.fidelitycharitable.org/nonprofits/faqs.html
- AEF/Ren release, Jul 2025 (2025-07-23): https://www.aefonline.org/thought-leadership/american-endowment-foundation-selects-ren-as-a-strategic-partner-to-expand-philanthropy-drive-innovation-and-foster-growth-in-financial-services/
- Edward Jones elevated wealth management release (2025): https://www.edwardjones.com/us-en/why-edward-jones/news-media/press-releases/elevated-wealth-management
- IRS 2026-2027 Priority Guidance Plan (2026-09-29): https://www.irs.gov/pub/irs-counsel/2026-2027-initial-pgp.pdf
