# Final status report: DAF research mission (2026-11-14 → 2026-11-15)

**Every count below was computed from the repository, not estimated.** The commands are listed in each row.

## Repository and branch
- **Repository:** `kemiller2002/daf-landscape`. Integration branch `main`.
- **Working branch:** `claude/daf-landscape-research-tdxdiq`. This is the branch the session was authorized to use. Merging to `main` is through **draft PR #20**: https://github.com/kemiller2002/daf-landscape/pull/20. Nothing was force-pushed and no research was deleted.
- **Final commit SHA:** a file cannot contain the SHA of the commit that adds it. The PR #20 description records the head SHA after this file was committed. The parent of the commit that adds this file is `1b8f763`.
- **Pre-existing open PRs:** #1 and #16 are left untouched.

## Counts (refresh 2026-11-20, through PR #68) — governing

These counts were recomputed from the git-tracked files on branch `claude/daf-landscape-research-tdxdiq` just before PR #68 merged. They supersede the tables below, and the PR #68 description records the head SHA.

| Item | Count | How computed |
|---|---|---|
| Pull requests merged in this mission | #20–#68 (49 PRs) | GitHub |
| Research documents | 378 documents, 1,459,552 words | `research/**/*.md` |
| Datasets | 707 CSV files, 491,086 data rows | `data/**/*.csv` (headers excluded) |
| Unique URLs cited in research markdown | 4,296 | regex over `research/**/*.md` |
| Independent validation | **2,227 register rows** in 75 register files (waves 1–46B): 1,591 confirmed, 513 partially confirmed, 86 contradicted, 26 unverifiable, 11 other | `validation-register*.csv`, classified by the leading words of `validation_result` |
| Research queue | 964 items: 425 done, 405 open, 78 blocked, 50 monitoring, 5 deprioritized historical, 1 declined | `research-priority-queue.csv`, `state` |
| Industry report | §11.1–§11.68 | `research/DAF-INDUSTRY-REPORT-2026-11.md` |

**Additions in PR #68 (validated; report §11.67–§11.68):**
- **Non-BMF recipients ($4.18bn, 22,269 EINs).**
  - $1.59bn sits in four Chan Zuckerberg LLCs, which are disregarded entities of Chan Zuckerberg Biohub Inc, a 501(c)(3).
  - $1.35bn goes to untraced religious bodies and $0.60bn to government units.
  - 884 of the 1,213 CN filing-rule passers had filed final or terminating returns, so the eligible upper bound falls from 77.3% to 76.9%.
  - These shares use filings available in November 2026. Tested against the filings the IRS had processed by each sponsor’s fiscal-year end, the grant-time share is 72.7% (FY2023 68.1%, FY2024 76.7%; 68.8% if every grant fell on the first day of the year) (b40n1202-b43n26-04). [V wave 47B]
  - $5.45m went to EINs revoked before the sponsor's fiscal year (core signal; no sponsors named; reinstatement can be retroactive).
- **Grant-count denominators.**
  - 12 of the top-15 sponsors state 2024 grant counts (Fidelity 2,664,446). No processor does.
  - Review-venue complaints run about 0.017 per 10,000 grants a year at Fidelity. AOGF is at most 2.32; the per-grant ranking between the two is open.
- **In-portal charity data.**
  - NPT embeds GuideStar; AEF and MS GIFT run on Ren (IRS-based); CF portals are Candid via vendors.
  - Seven top-20 sponsors are not found. Charity Navigator is not found inside any portal.
- **Tax pages, ranks 11–25, and Fidelity calculators.**
  - Fidelity's tax-savings calculator omits the 2026 floor, cap and non-itemizer path. It overstates savings by 7–69% (H2–H4) and shows no saving for H1 (the non-itemizer path saves $720 over 3 years).
  - Its securities calculator understates savings by about 3.5–18%, mainly because it omits the 3.8% NIIT.
  - BofA has a “0.05%” floor footnote error. JCF and Columbus misdescribe the cap and the corporate floor.
  - All five 2026 law parameters were verified on govinfo and LII.
- **Pass-through recipients.**
  - The core 10 intermediaries take 2.3% of top-50 DAF dollars, publish no DAF route, and grant out about 0.86 per dollar in (0.78 without Blue Meridian).
  - $183.1m moves within the set.
- **Foundant / NCF.**
  - Foundant documentation is blocked: its hosts disallow Anthropic agents.
  - NCF documents a donate button, but its Program Agreement host disallows all agents.
- **Robots provenance (open owner decision).**
  - Earlier validated work cites pages from hosts whose robots.txt now disallows Anthropic agents or all agents: secure.ncfgiving.com (74 lines in 37 files; see validation-wave46a-report.md), www.foundant.com and donorportal.cct.org.
  - New findings from those hosts were withdrawn this round; earlier content is flagged, not deleted.

## Counts (refresh 2026-11-20, through PR #67) (superseded by the table above)

These counts were recomputed from the git-tracked files on branch `claude/daf-landscape-research-tdxdiq` just before PR #67 merged. They supersede the tables below, and the PR #67 description records the head SHA.

| Item | Count | How computed |
|---|---|---|
| Pull requests merged in this mission | #20–#67 (48 PRs) | GitHub |
| Research documents | 370 documents, 1,426,915 words | `research/**/*.md` |
| Datasets | 693 CSV files, 490,671 data rows | `data/**/*.csv` (headers excluded) |
| Unique URLs cited in research markdown | 4,219 | regex over `research/**/*.md` |
| Independent validation | **2,151 register rows** in 73 register files (waves 1–45B): 1,535 confirmed, 501 partially confirmed, 84 contradicted, 20 unverifiable, 11 other | `validation-register*.csv`, classified by the leading words of `validation_result` |
| Research queue | 930 items: 420 done, 378 open, 76 blocked, 50 monitoring, 5 deprioritized historical, 1 declined | `research-priority-queue.csv`, `state` |
| Industry report | §11.1–§11.66 | `research/DAF-INDUSTRY-REPORT-2026-11.md` |

**Additions in PR #67 (validated; report §11.63–§11.66):**
- **Charity-data terms for AI uses.**
  - Of the 24 commercial-provider cells, only one use is permitted outright: Charity Navigator lets licensees cache ratings.
  - Candid's AI/ML consent clause qualifies its ban on mining for three listed purposes.
  - 8 of the 12 "silent" cells are really "not determinable" (Every.org and Pledge).
  - Only IRS data is free on all four uses.
  - Pledge runs a partner MCP server that is not in the AI census.
- **Chariot size match.**
  - Matched on their own contributions, recipients give 10.0% (8.2–12.1%) pooled and 5.8% median, against Chariot's 12.6%.
  - Size matching does not close the gap. Its 0.6–4.4 pt interval reflects recipient sampling only.
  - The all-recipient 9.2% and 13.7% figures (8.8% and 13.6% on the census-enlarged sample, b40n1202-04) are not like-for-like with Chariot. [V wave 47A]
- **Tail CF fees on 20 schedules.**
  - The pooled median is 137.5 / 137.5 / 125 bps at $25k / $100k / $500k.
  - The premium over the top 100 (+37.5 bps at $100k) is not established at the two-sided 95% level (one-sided p = 0.04).
  - Tail and top-100 opening minimums are equal ($10,000).
  - The realised pool is unchanged at $49.4m.
- **Assets Under Movement and NPT.**
  - AUM fails the DAF-to-DAF whitelist rule (its DAF share of assets is 0.21). Its FY2024 Schedule D roll-forward gap is −$111.4m.
  - The governing fiscal-sponsor addition stays $35.1m–$114.6m: AUM apportioned on assets gives $102.5m, AUM dropped gives $56.6m.
  - NPT's $39.1m Europe line is in FY2025, so FY2024 foreign grants are unchanged.
- **Foundant Giving Hub census withdrawn** before validation, because fcsuite.com's robots.txt disallows Anthropic agents. P-B4222-02-01 is re-scoped to vendor documentation (P-B4222-02-01-01; renumbered from a colliding ID).
- **Blank vs zero DAF-grant cells.**
  - All 248 blank IPS FY2023 cells are blank-filed, and all 100 explicit zeros are zero-filed.
  - IPS's 9.68% median is unchanged.
  - A blank line 3(a) is a preparer choice and not evidence of no grants.
  - The repo panel under IPS's rule gives 9.86%.
- **2026 docket letters.**
  - All 13 are unreadable: regulations.gov returns 403. The queue item is blocked and the owner needs to download them.
  - RIN 1545-BI33 (2026 Unified Agenda) targets the final rule for 07/2026, a target that has passed, with no EO 12866 meetings.
- **Schedule A excess over 2%.**
  - Gifts from (vi) organisations are exempt from the 2% limit unless earmarked (Reg. §1.170A-9(f)(6)(v)). So 98.4% of top-50 DAF dollars is an upper bound on DAF dollars outside line 5.
  - The DAF share of 1f net of the excess is 13.0% (all) and 13.9% (Part II, against 11.4%). This is not an individual-only share.
- **Canadian carry-forwards.**
  - 11–13 of the 22 shortfall sponsors are covered on filed returns, and 16 with the screened pre-2023 proxy (C$0.44–1.13m uncovered).
  - The netted payout stays 12.05%.
  - The nil-quota and old-rate readings rest on statute text alone, without CRA guidance.

## Counts (refresh 2026-11-20, through PR #66) (superseded by the table above)

These counts were recomputed from the git-tracked files on branch `claude/daf-landscape-research-tdxdiq` just before PR #66 merged. They supersede the tables below. The PR #66 description records the head SHA. The validation-result classifier now normalises underscores and "partly", so its split differs slightly from earlier tables; the row total is exact.

| Item | Count | How computed |
|---|---|---|
| Pull requests merged in this mission | #20–#66 (47 PRs) | GitHub |
| Research documents | 357 documents, 1,378,041 words | `research/**/*.md` |
| Datasets | 672 CSV files, 463,947 data rows | `data/**/*.csv` (headers excluded) |
| Unique URLs cited in research markdown | 4,132 | regex over `research/**/*.md` |
| Independent validation | **2,058 register rows** in 69 register files (waves 1–43C): 1,465 confirmed, 480 partially confirmed, 82 contradicted, 20 unverifiable, 11 other | `validation-register*.csv`, classified by the leading words of `validation_result` |
| Research queue | 890 items: 412 done, 347 open, 75 blocked, 50 monitoring, 5 deprioritized historical, 1 declined | `research-priority-queue.csv`, `state` |
| Industry report | §11.1–§11.62 | `research/DAF-INDUSTRY-REPORT-2026-11.md` |

**Additions in PR #66 (validated; report §11.60–§11.62):**
- **Sector shares across all sponsors (DAF-weighted, $101.0bn):**
  - education 22.98%, human services 14.60%, religion 14.06%, public-society benefit 13.17%, foreign 3.12%.
  - Coding DAF-to-DAF grants as society benefit (t_b) matches sponsor-published splits (public-society benefit 23.7%). It double-counts, so it is never a market share.
  - The Fidelity fit is *consistent with* sponsor-to-sponsor counting; it does not prove it.
- **AI overlay rules clarified (§7a–§7c, proposed, binding from the next re-score).**
  - Chariot Disbursements stays AMBER, with an adjudication note.
  - NCF's AMBER (low) is provisional.
  - Benevity's stale RED is noted where it still appears.
- **OJC Fund and Groundswell.**
  - 0.30% of OJC dollars pass to DAF sponsors, none in the church block. About two-fifths of OJC church-block dollars go to congregations.
  - The faith share of church DAF dollars stays about 30%, with sensitivities of 23–29%.
  - Groundswell's 12,808 accounts are per-user DAFs by count. Its Part IV line 6 = 0 contradicts its own Schedule D.
- **De facto fiscal sponsors.**
  - 11 hosts are found from FBO / c/o lines, 82% of them via ImpactAssets' filings; 5 are on neither list.
  - Three of the five are also DAF sponsors, so the addition is $35.1m–$114.6m (0.04–0.12% of proxy dollars).
  - Within that range, Assets Under Movement’s own returns give a DAF share of assets of 0.205 / 0.211, so it fails whitelist rule W2 and stays off the DAF-to-DAF whitelist; its FY2024 Schedule D misses its roll-forward by $111.4m. Apportioning its 58 lines by its asset share gives an addition of $102.5m; dropping it alone gives $56.6m (g050303-02). [V wave 44B]
  - The governing exception-proxy figures stand; fiscal sponsors 0.47% / 2.06% and core 7.79% / 11.73% are upper bounds.
- **Lobbying (LDA 2021+) and breach notices.**
  - Charitable-deduction lobbying that never names DAFs comes from charity-side groups (169 charity-relevant filings, $13.65m whole-filing).
  - FMR, Vanguard, Goldman Sachs and Morgan Stanley filed 605 lobbying reports and none names DAFs, §4966 or IRA charitable distributions. FMR's 2026 Q3 filing lists H.R. 9173 (digital-asset donations).
  - Two SIFMA lines do cite §4966 by number; both also name DAFs.
  - No Vermont or Massachusetts breach notice names a DAF sponsor. Vanguard's 2026 breach affected 1,224 Massachusetts residents and 94 in Vermont.
  - LD-203 honorary-expense items now withhold individual names.

## Counts (refresh 2026-11-20, through PR #65) (superseded by the table above)

These counts were recomputed from the repository on branch `claude/daf-landscape-research-tdxdiq` just before PR #65 merged. They supersede the tables below. The PR #65 description records the head SHA.

| Item | Count | How computed |
|---|---|---|
| Pull requests merged in this mission | #20–#65 (46 PRs) | GitHub |
| Research documents | 349 documents, 1,337,397 words | `research/**/*.md` |
| Datasets | 657 CSV files, 440,420 data rows | `data/**/*.csv` (headers excluded) |
| Unique URLs cited in research markdown | 4,105 | regex over `research/**/*.md` |
| Independent validation | **1,984 register rows** in 66 register files (waves 1–42C): 1,420 confirmed, 458 partially confirmed, 80 contradicted, 19 unverifiable, 7 other | `validation-register*.csv`, classified by the leading word of `validation_result` |
| Research queue | 865 items: 402 done, 332 open, 75 blocked, 50 monitoring, 5 deprioritized historical, 1 declined | `research-priority-queue.csv`, `state` |
| Industry report | §11.1–§11.59 | `research/DAF-INDUSTRY-REPORT-2026-11.md` |

**Additions in PR #65 (validated; report §11.57–§11.59):**
- **AI GREEN overlays rechecked.**
  - Givebutter Magic is now AMBER: it is not flag-only, and its AI fraud review has undocumented limits.
  - SmartSimple, Fluxx Finn and YourCause remain GREEN (provisional). YourCause summaries still have to be enabled on request.
  - None of these is the first GREEN under §7.
- **Realised tail fees, all 641 tail community foundations plus 29 non-CF tail sponsors.**
  - Tail CFs realise about $49.4m ($38.5–61.5m; 94% imputed from size-band medians). The whole tail realises about $49–74m.
  - The $90m and $138m schedule figures remain as list-price ceilings.
  - Fee rates fall with size, and publishing a schedule makes no difference once size is controlled.
- **Faith sponsors outside the top 50.**
  - They add $1.08bn to the church block. Across all panel sponsors, faith sponsors send about 30% of it (25% without the OJC Fund, a pass-through sponsor in the asset sense whose Schedule I goes to church-status Orthodox bodies, not to other DAF sponsors; 27–29% if its non-congregation recipients are discounted, 23% if every sponsor is limited to congregation names) [V wave 43B], against 22% in the top-50 frame.
  - Nationals send about 59%, against 74% top-50 only, an understatement because BofA and RCF do not itemise. CCF-LA is Catholic.
- **Corporate 1% floor.** No company ties a 2025 DAF gift to the floor. Apollo predates the bill and Circle was a scheduled pledge. BlackRock, Unum and URBN fit the timing but state no tax motive.
- **AI realization for routing and correlated execution.**
  - With the upper half of h cut by the RPA analogue [I], routing is modal in 2 processes at a large national at m = 1.77 (3 at m = 1.56), against 5 uncut. Hybrid stays at 5.
  - Correlated execution shifts rank-first from B to A and C.
  - Assistance is modal nowhere in any cell.

## Counts (refresh 2026-11-20, through PR #64) (superseded by the table above)

These counts were recomputed from the repository on branch `claude/daf-landscape-research-tdxdiq` just before PR #64 merged. They supersede the tables below. The PR #64 description records the head SHA.

| Item | Count | How computed |
|---|---|---|
| Pull requests merged in this mission | #20–#64 (45 PRs) | GitHub |
| Research documents | 341 documents, 1,295,968 words | `research/**/*.md` |
| Datasets | 644 CSV files, 406,312 data rows | `data/**/*.csv` (headers excluded) |
| Unique URLs cited in research markdown | 4,066 | regex over `research/**/*.md` |
| Independent validation | **1,896 register rows** in 63 register files (waves 1–41C): 1,359 confirmed, 435 partially confirmed, 77 contradicted, 18 unverifiable, 7 other | `validation-register*.csv`, classified by the leading word of `validation_result` |
| Research queue | 841 items: 394 done, 316 open, 75 blocked, 50 monitoring, 5 deprioritized historical, 1 declined | `research-priority-queue.csv`, `state` |
| Industry report | §11.1–§11.56 | `research/DAF-INDUSTRY-REPORT-2026-11.md` |
| Standards | `standards/daf-grant-record/` schema v0.1 (draft, unendorsed) with 24 test vectors | `scripts/mission_validate_grant_record.py` |

**Additions in PR #64 (validated; report §11.54–§11.56):**
- **Open DAF grant record.** Published as a draft, unendorsed JSON Schema with 24 test vectors that pass. The purpose vocabulary is Candid PCS, which is CC BY 4.0, capped at 5 codes per facet.
- **Non-cash intake vendors.** Their claims far exceed what the affiliated charities file. FreeWill pays at most about 1,000 organisations against its claim of 55,000. The Giving Block's figures contradict each other.
- **DPN.** Counted in neither the sponsor nor the processor totals; it appears as a memo line.
- **Filing-break screen.** Only two breaks above $250m: NPT FY2023 and Dechomai FY2021. As a sensitivity only, FY2023 would be $261.69bn and FY2021 $234.79bn.
- **Tail fees.** Non-publishing tail community foundations do charge, at about 70–129 bps all-fund, with size a confound. The community-foundation pool is about $49m on realised all-fund rates across all 641 tail CFs ($38.5m–$61.5m), with $90m as a published-schedule ceiling (about $84m flat at the 20-schedule tail-CF median of 137.5 bps; b4501-01). [V wave 44B] Non-CFs rarely show fees (6 of 29 sampled; none worded as an internal fund fee), so the whole tail realises about $49m–$74m, not $138m [V wave 42A]
- **Recipient DAF share, coverage gap decomposed.** Central estimate 9.2% of line 1h and 13.7% of 1h−1d−1e on the 2,352-EIN sample. The assumption range is 8.8–9.4% and 13.2–14.1%. With every recipient of $25m or more read (4,458; 6,132 EINs in all), the central estimate is 8.8% on 1h (95% CI 7.9–9.7%; census-corrected 8.2–9.4%) and 13.6% on 1h−1d−1e (12.2–15.0%; 12.7–14.5%). These intervals cover sampling only, and the allocation envelope was not re-run (b40n1202-04). [V wave 47A] These are all-recipient figures, not a like-for-like match to Chariot’s 12.6%. Size-matched on recipients’ own 1h−1d−1e ($50–200m a year), the central share is 10.0% (sampling CI 8.2–12.1%), median 5.8%, about 2.6 points below Chariot; period and numerator differences are unquantified (b40n1202-b43n26-02). [V wave 44A]
- **Manual improvement (A), calibrated to the NAO casework evidence [I].** Under AI assistance, A is still the modal choice in 6 of 15 processes. Under A01 routing at m ≈ 1.8, AI is modal in 5 processes and A in 1; with the upper half of h held to the RPA realization range [I], 2 and 4 (g0403-0105-04) [S] [V wave 42C]

## Counts (refresh 2026-11-20, through PR #63) (superseded by the table above)

Recomputed from the repository on branch `claude/daf-landscape-research-tdxdiq` just before PR #63 merged. These counts supersede the tables below. The PR #63 description records the head SHA.

| Item | Count | How computed |
|---|---|---|
| Pull requests merged in this mission | #20–#63 (44 PRs) | GitHub |
| Research documents | 333 documents, 1,256,217 words | `research/**/*.md` |
| Datasets | 630 CSV files, 359,631 data rows | `data/**/*.csv` (headers excluded) |
| Unique URLs cited in research markdown | 4,034 | regex over `research/**/*.md` |
| Independent validation | **1,813 register rows** in 60 register files (waves 1–40C): 1,303 confirmed, 411 partially confirmed, 74 contradicted, 18 unverifiable, 7 other | `validation-register*.csv`, classified by the leading word of `validation_result` |
| Research queue | 812 items: 385 done, 296 open, 75 blocked, 50 monitoring, 5 deprioritized historical, 1 declined | `research-priority-queue.csv`, `state` |
| Industry report | §11.1–§11.53 | `research/DAF-INDUSTRY-REPORT-2026-11.md` |

**Additions in PR #63 (validated; report §11.51–§11.53):**
- **Propagation.** The refined exception proxy now appears in the gap19 note, report §4 and the synthesis. FY2024 non-DAFRC accounts become 24,800 with Groundswell included; its accounts average $787, which raises the same comparability caveat as processor accounts. They are DAFs in the legal sense and meet DAFRC’s Schedule D Part I(a) rule: one DAF per user, mostly employees, funded by the user and by employer matches (b4026-0601-01-p0503-ojc-groundswell.md) [V wave 43B]
- **DAF grant schema and processor accounts.**
  - Chariot and Endaoment carry all 8 core grant-record fields. Form 990 requires only the recipient EIN in full.
  - Processors are 76.7% of corrected FY2024 accounts. With all 22 processors removed, sponsor accounts are about 770,785.
- **Non-top-50 numerator.** Measured directly, the all-sponsor DAF share of recipient contributions is 8.4–9.9% on line 1h and 12.6–14.8% on 1h−1d−1e. Allocating the coverage gap by component replaces the ÷ 0.849 upper figures with a central 9.2% and 13.7%. The assumption envelope is about 8.8–9.4% and 13.2–14.1%, and the sampling CI 8.3–10.2% and 12.3–15.2% (2,352-EIN sample). The census-enlarged sample gives 8.8% and 13.6%, with census-corrected CIs of 8.2–9.4% and 12.7–14.5% (b40n1202-04). [V wave 47A] The 8.4% and 12.6% floors stand as measured-only figures (b40n120201-01) [V wave 41B] The like-for-like overstatement from the earlier scaling is only about 0.4 percentage points.
- **Canada follow-ups.**
  - Sponsors' gifts to public foundations go mostly to hospitals and federations; the middle netting tier is about 12.0%.
  - The Schedule 8 gap follows the answer to line 5850. JCF Montreal meets the quota.
  - CanadaHelps is not a DAF.
- **990 margin proxy retired.** ΔR1 is other-fund growth, an endowment, or a reporting-basis gap, not a fee surplus.
- **Who pays sponsor marketing.** No filing shows a parent paying beyond what the charity pays it, and Fidelity's FMR costs are not separately stated. The adviser-programme expenses found are Fidelity $8–21m a year and DAFgiving360 commissions.

## Counts (refresh 2026-11-19, through PR #62) (superseded by the table above)

These counts were recomputed from the repository on branch `claude/daf-landscape-research-tdxdiq` just before PR #62 merged. They supersede the tables below. The PR #62 description records the head SHA.

| Item | Count | How computed |
|---|---|---|
| Pull requests merged in this mission | #20–#62 (43 PRs) | GitHub |
| Research documents | 325 documents, 1,214,126 words | `research/**/*.md` |
| Datasets | 616 CSV files, 350,202 data rows | `data/**/*.csv` (headers excluded) |
| Unique URLs cited in research markdown | 4,004 | regex over `research/**/*.md` |
| Independent validation | **1,724 register rows** in 57 register files (waves 1–39C): 1,243 confirmed, 387 partially confirmed, 69 contradicted, 18 unverifiable, 7 other | `validation-register*.csv`, classified by the leading word of `validation_result` |
| Research queue | 790 items: 375 done, 284 open, 75 blocked, 50 monitoring, 5 deprioritized historical, 1 declined | `research-priority-queue.csv`, `state` |
| Industry report | §11.1–§11.50 | `research/DAF-INDUSTRY-REPORT-2026-11.md` |

**Additions in PR #62 (validated; report §11.48–§11.50):**
- **Grant remittance and portal features.**
  - No sponsor states its ACH SEC code on any public page we read. NPT does not send ACH payments.
  - Several vendor portals already offer export.
  - NCF is the only top-20 sponsor that documents giving into a donor's fund.
  - No portal offers a donor-level impact report.
- **Sponsor-published grant statistics.**
  - The unrestricted share as sponsors report it is 63–74% by count: Fidelity 63–64% "where needed most", DAFgiving360 72%, NPT 66% (restated), Vanguard 70%.
  - By dollars, Vanguard's unrestricted share is about 52%.
  - Fidelity's disclosure split is 80% full / 15% fund name / 5% anonymous.
- **Detection probability.** An escaped DAF error has roughly a 0.1–1% chance per year of being detected and taxed, measured as average-filer coverage. The composite m is fragile: it is about 1.6 when OFAC penalties are priced per transaction and 14–1,270 when priced per missed alert.
- **Line 6 versus Schedule D.**
  - 33 returns that hold DAFs answer "No" on line 6, carrying $265m. SOI extracts keyed on line 6 drop them; DAFRC does not use line 6.
  - Non-DAFRC FY2024 accounts are 24,800: 11,992 at line-6 “Yes” filers plus Groundswell’s 12,808 (average $787 per account; per-employee DAFs funded by employees and employer matches, so DAFs, but processor-like in size) [V wave 43B], with $353.9m of DAF assets (`non-dafrc-daf-filers-summary-with-groundswell-2026-11-19.csv`) [V wave 40A]
- **Exception proxy refinements.**
  - EIN-keyed fiscal sponsors account for 0.44% of lines and 1.94% of dollars; dropping large-programme hosts gives 1.68%. Five de facto hosts found from filers’ own “FBO” naming (g0503-03-de-facto-fiscal-sponsors.md) would raise this to at most 0.47% / 2.06%, and the core to at most 7.79% / 11.73%. Three of the five are also DAFRC-vetted DAF sponsors and 82% of the detections come from one filer, so these are upper bounds and the headline stands [V wave 43B]
  - The time-correct recent-ruling flag counts true new organisations at 3.16% of lines and 4.72% of dollars.
  - Core is 7.76% / 11.61%.

## Counts (refresh 2026-11-19, through PR #61) (superseded by the table above)

These counts were recomputed from the repository on branch `claude/daf-landscape-research-tdxdiq` just before PR #61 merged, and they supersede the tables below. The PR #61 description records the head SHA.

| Item | Count | How computed |
|---|---|---|
| Pull requests merged in this mission | #20–#61 (42 PRs) | GitHub |
| Research documents | 317 documents, 1,178,666 words | `research/**/*.md` |
| Datasets | 601 CSV files, 345,584 data rows | `data/**/*.csv` (headers excluded) |
| Unique URLs cited in research markdown | 3,925 | regex over `research/**/*.md` |
| Independent validation | **1,628 register rows** in 54 register files (waves 1–38C): 1,181 confirmed, 360 partially confirmed, 63 contradicted, 17 unverifiable, 7 other | `validation-register*.csv`, classified by the leading word of `validation_result` |
| Research queue | 762 items: 366 done, 265 open, 75 blocked, 50 monitoring, 5 deprioritized historical, 1 declined | `research-priority-queue.csv`, `state` |
| Industry report | §11.1–§11.47 | `research/DAF-INDUSTRY-REPORT-2026-11.md` |

**Additions in PR #61 (validated; report §11.45–§11.47):**
- **Canada.** Payout net of DAF-to-DAF transfers is 12.0% (12.8% under tier A; 8.8% under tier C, which is an upper bound). The charity-level disbursement quota rarely binds on DAF sponsors.
- **DAF money abroad through non-Q recipients.** Adds $1.35bn. The measured share of total grants reaching abroad is 5.20% [I-alloc], or 5.10% excluding fundraising and PRI rows.
- **Escaped-error cost m.** Bank SAR penalties work out at $36k–$471k per SAR, which is 2,600–34,000 handling-times; carrying that to DAF sponsors is analogy only [I]. For DAF sponsors the central m is about 2.2 (wave 38B). Bounding IRS detection (P ≈ 0.0012–0.0099) lowers it to 1.56–1.77, and it rests mostly on unsourced operational-rework and sanctions-pricing assumptions [V wave 39B] Routing beats assistance up to about m = 10.
- **Sponsor economics.**
  - Dechomai is 0.1–3.0% of national sponsors' DAF contributions.
  - Audited fee economics: Fidelity passes its whole fee to FMR and runs an operating deficit; Renaissance passes 98% to Ren; JCF keeps a small surplus.
  - The 990 non-DAF net-asset change is not an operating margin and is retired as one: it tracks other-fund growth, endowment returns, campaign receipts and Schedule D reporting basis, and the fee surplus is identifiable in it at none of the five audited sponsors. [b4427-03] [V wave 40C]
- **Filing frames.**
  - 7 new small DAF sponsors were found that DAFRC missed.
  - 24 place-based community foundations exited in 2021–2026, 19 of them outside DAFRC. That is about 3× the filed-exit count for overlapping years, not 5×.

## Counts (refresh 2026-11-19, through PR #60) (superseded by the table above)

Recomputed from the repository on branch `claude/daf-landscape-research-tdxdiq` just before PR #60 merged. These figures supersede the tables below. The PR #60 description records the head SHA.

| Item | Count | How computed |
|---|---|---|
| Pull requests merged in this mission | #20–#60 (41 PRs) | GitHub |
| Research documents | 309 documents, 1,141,857 words | `research/**/*.md` |
| Datasets | 585 CSV files, 340,594 data rows | `data/**/*.csv` (headers excluded) |
| Unique URLs cited in research markdown | 3,866 | regex over `research/**/*.md` |
| Independent validation | **1,536 register rows** in 51 register files (waves 1–37C): 1,118 confirmed, 337 partially confirmed, 57 contradicted, 17 unverifiable, 7 other | `validation-register*.csv`, classified by the leading word of `validation_result` |
| Research queue | 734 items: 358 done, 245 open, 75 blocked, 50 monitoring, 5 deprioritized historical, 1 declined | `research-priority-queue.csv`, `state` |
| Industry report | §11.1–§11.44 | `research/DAF-INDUSTRY-REPORT-2026-11.md` |

**Additions in PR #60 (validated; report §11.42–§11.44):**
- **Payout definitions.** IPS's 9.7% median reproduces from IPS's own file. The 23.9% figure is NPT's FY2023 aggregate. The gap from 23.9% to 9% comes mostly from the move from pooled to median sponsor (−9.4 pts) and from the denominator (−5.9 pts). The remainder is a residual that mixes sample, window and definition, so it is not purely the distribution within sponsors.
- **DAF money abroad.** The 150 largest international recipients carry $1.87bn of DAF money abroad; this figure depends on an allocation assumption. Including direct foreign grants, measured outflow is 3.82% of total grants. The earlier 7.8% is a share by recipient sector. Adding the 458 largest recipients outside NTEE Q raises measured outflow to 5.20% of total grants (6.44% of net Schedule I plus line 3; 5.10% without program-related-investment and fundraising rows) [I-alloc] [V wave 38A]
- **Dechomai.** $3.27bn of non-cash intake in 2021–24, 83% of it private business interests, with $1.15bn routed to six national sponsors. Its fee take is not measured, and its fee and administration outflows are 0.39–0.62% of intake.
- **DAFpay Network TY2025.** "Other fees" are 3.0% of contributions and are booked as an expense. The return is not audited.
- **Canada.** The CRA T3010 panel reproduces Blumberg & Pasha: C$18.60bn at 864 sponsors in the 2025 release. Counting blank disbursement lines as zero, the median payout is 4–5%.
- **Australia.** The 6% giving-fund minimum has been decided but was not registered as of 2026-11-19. Only the rename to "giving fund" has commenced.
- **AI economics.** With B and D held to C's evidence standard, AI assistance still wins no process, and the processes B and D lose go to manual improvement, whose α is unsourced. Holding A to NAO manual-casework throughput realization [I] (g0403-01) keeps A modal in 6 of 15 processes with assistance; with A01 routing at m = 1.77, C is modal in 5 and A in 1; with the upper half of h held to the RPA range [I], 2 and 4, and correlated realization moves probability from B to A and C, not back to V1 priors (g0403-0105-04) [S] [V wave 42C] No audit of realized labour savings from a manual fix was found [V wave 41C] The bound E15 implies is a miss rate of at most 0.39% per auto-closed alert, not 0.10.

## Counts (refresh 2026-11-19, through PR #59) (superseded by the table above)

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
- **AI routing.** Confidence-gated routing roughly triples intervention C's value pool when an escaped error costs one case-handling's worth. It still beats assistance up to about ten, and the pool falls below assist near m = 20. The central m is 2.20 after wave 38B’s correction (it was given as 2.4), and IRS-bounded detection lowers it to 1.56–1.77. Bank-style compliance errors that escape, or sanctions misses priced per missed alert, would still erase the gain [V wave 39B] [V wave 38B] C still almost never ranks first.
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
- **Tail admin-fee pool.** CFs-only central estimate is about $90m. The whole-tail figure of about $138m is an upper bracket, with a range of $76m–$184m, replacing the $92m hypothetical. Non-publishing tail CFs do charge (7 of 25 sampled disclose internal fees at 70–129 bps of total assets), giving a floor-type CF pool of about $63m; non-CF charging is untested [V wave 41B]. Superseded: size-banded realised all-fund rates across all 641 tail CFs give $49.4m ($38.5m–$61.5m; 94% imputed from band medians), and the whole tail $49.4m–$74.3m central ($38.5m–$92.5m) because only 6 of 29 sampled non-CFs show any fee line (b4427b-0405) [V wave 42A]
- **Schedule I purpose text cannot measure donor restrictions.** About half of dollars carry generic text, about half carry sector labels, and about 1–2% have a specific purpose.
- **Ren acknowledgement defaults track guide vintage.** The evidence shows neither a sponsor setting nor a platform limit.
- **Adviser-managed assets.** The share is 46.9% at Fidelity Charitable and 0% at Vanguard. DAFgiving360 is only bracketed and NPT cannot be estimated.
- **NPT foreign grants.** None of NPT's FY2023–24 foreign grants went to related organisations as filed (Schedule R Part V line 1b = No). Part V excludes only NPT's own transactions with its disregarded entities; on the repo's reading of Appendix F, a disregarded entity's grants to a related organisation are NPT's, so the filed No is a weak test [V wave 36C] In FY2025, £30.9m went from NPT Transatlantic to NPT UK.
- **The $6.18bn "church" block is about half congregations.** Faith sponsors send about 22–26% of it within the top-50 frame and about 30% across all itemising DAFRC panel sponsors (25% without the OJC Fund; about 23% if every sponsor is limited to congregation-named recipients) [V wave 43B], where nationals send about 59% rather than three-quarters; none of the 14 congregation giving pages read offers a DAF option [V wave 42B].

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
- **NPT FY2023 Schedule D is understated.** NPT's consolidated statements give net assets of $28.51bn. The filed value stays in the headline series, and a sensitivity variant shows FY2023 market assets of $261.44bn ($261.69bn at the DAF roll-forward midpoint; FY2023→24 growth 23.5% rather than 26.1%). A screen of all 4,633 testable sponsor-years FY2021–24 finds one other filed break above $250m: Dechomai Asset Trust FY2021 ($267.7m filed against $1,148.1m of net assets). Its roll-forward midpoint would add $774.0m, giving an FY2021 market of $234.79bn rather than $234.01bn. Its overlap with Dechomai Foundation is untested, and the headline keeps filed values (b4427b-b4501 §2) [V wave 41B] All top-50 imputed FY2024 rows had already been replaced, and the headline totals are unchanged.
- **Donor-information defaults at the top-20 sponsors.** Neither "withheld by default" nor "shared by default" holds as a rule. Full contact is the documented default for 33.2% of assets and withholding for 17.2%; the default is undocumented for 44.6%.
- **DAF share of recipient giving.** On the private-giving proxy (1h − 1d − 1e), top-50 DAF grants are a median 7.7% and a pooled 10.3%; with every itemising panel sponsor measured, the pooled share is 12.6% on the same recipients and 12.1% adding recipients with no top-50 grant (floors; the scaled 15.4% is superseded) [V wave 40B]. With the coverage gap allocated by component, the committed-frame central figure is 13.7% (assumption envelope about 13.2–14.1%; CI 12.3–15.2%) [V wave 41B]. On the census-enlarged sample it is 13.6% (CI 12.2–15.0%; census-corrected 12.7–14.5%) (b40n1202-04). [V wave 47A] 76.5–76.9% of top-50 DAF dollars go to recipients eligible for a Charity Navigator rating on November 2026 filings. At grant time (filings processed by each sponsor’s fiscal-year end) the share is 72.7% (72.4–72.7% across variants; 71.5% allowing for IRS posting and Charity Navigator refresh lags) (b40n1202-b43n26-04). [V wave 47B]
- **Long-tail fee census.** 7 of 60 sampled tail sponsors (11.7%) publish a 2021+ admin rate. Tail community foundations that do publish charged a median 150 bps at $100k on 6 schedules. On 20 schedules from 91 sampled CFs (22.0% publishing; b4501-01) the median is 137.5 bps (bootstrap 100–150), so a premium over the top-100 median of 100 bps is no longer established. [V wave 44B]

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
- **Exception-load proxy.** Across the top 50 sponsors, 7.4% of recipient lines and 11.0% of dollars need non-routine review. With the EIN-keyed fiscal-sponsor list and time-correct rulings it is 7.76% / 11.61% (6.80% / 11.00% counting only true new organisations as recent), or 7.74% / 11.35% if four hosts with large programmes of their own are not counted as fiscal sponsors [V wave 39C]
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

**Seventh-round additions (validated, report §11.27):** direct foreign grants are 1.92% of top-50 sponsors' grants ($1.89bn over FY2023–24), lifting the international sector share from 5.6% to 7.8% (a recipient-sector share; DAF money measured as reaching abroad, including via US-registered NTEE Q and friends-of recipients, is 3.82% of top-50 grants, or 4.74% of net Schedule I plus line 3) [V wave 37A]; about 42% of covered DAF grant dollars go to charities that report any lobbying, with median lobbying intensity of about 0.2% of expenses (descriptive, lawful activity); 1,240 sponsors under $50m hold 2.84% of assets, pay out less (median 11.7%) and account for nearly all entries and exits.

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
- **Where DAF money goes:** $77.34bn to ~174k recipients net of DAF-to-DAF; education 25.8%, human services 14.3% at the top 50 ([direction-recipients-impact-matching.md](direction-recipients-impact-matching.md)). Across all 1,379 itemising sponsors, DAF-weighted with foreign and sub-$5,000 grants ($101.01bn, FY2023–24): education 23.0%, human services 14.6%, religion 14.1%, public-society benefit 13.2%, foreign grants 3.1%; on the basis comparable with sponsor-published splits (DAF-to-DAF kept), public-society benefit is 23.7% ([b39n4-01](b39n4-01-sector-join-all-sponsors.md)) [V wave 43A]
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
