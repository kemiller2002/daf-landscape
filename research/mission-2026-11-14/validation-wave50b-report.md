# Validation wave 50B: institutional DAF programmes; giving circles

**Validator:** validator wave 50B · **Date:** 2026-11-20 · **Register:** [`data/mission-2026-11-14/validation-register-wave50b.csv`](../../data/mission-2026-11-14/validation-register-wave50b.csv) (31 rows, V50B-01 to V50B-31)

**Studies validated**
- b50-03, institutional DAF programmes: [`b50-03-institutional-daf-programs.md`](b50-03-institutional-daf-programs.md), `institutional-daf-programs-2026-11-20.csv`, `scripts/mission_institutional_dafs.py`, and the study's XML and policy-page cache in the session scratchpad.
- b50-04, giving circles: [`b50-04-giving-circles.md`](b50-04-giving-circles.md), `giving-circles-2026-11-20.csv`, `giving-circles-robots-log-2026-11-20.csv`, `scripts/mission_b50_04_build_csv.py`.
- Wave 50A (b50-01, b50-02 and §11.75) was not touched.

## 1. Method

- **b50-03 rebuild.** `mission_institutional_dafs.py` was run with `python3 -B` into a scratch root, with symlinked inputs and a copy of the study's cache. The output CSV is byte-identical to the committed CSV, and `check_totals.json` reports no failures.
- **b50-03 recompute.** Shares, top-10 concentration, average account size and the D-weighted host-share bounds were recomputed from the CSV in a separate script. The 131 + 53 segment split was recounted from the sponsor rows.
- **b50-03 raw XML.** I wrote a new parser and used it to re-read Schedule D Part I, Schedule I and Part IX in 11 returns: SUNY Binghamton FY2023–24, UCLA FY2023–24, Cornell FY2024, Harvard FY2024, Rochester FY2023–24 and Penn Presbyterian FY2023–24. The parser did not reuse the study's code. Université de Montréal was checked against the DAFRC panel and the corrections file.
- **b50-03 policy pages.** Ten pages were fetched again live: Stanford PDF, Cornell brochure, Brown, Mayo, Columbia, Harvard, Penn Medicine, Rochester PDF, Yale web and UND. Each was checked after a robots check covering all seven agents. 18 quote fragments and the entry minimums were tested verbatim, with whitespace normalised.
- **P-B5003-06.** I grepped `scripts/` and `data/` for netting and whitelist. The functions of `scripts/mission_market_netting.py` were then re-run read-only from a scratch script, against the existing Schedule I cache. Nothing was written to the repo. The re-run reproduces `dafrc-market-totals-netted.csv`; for example, FY2024 grants in the lower tier are $6,953,159,760.
- **b50-04 rebuild.** `mission_b50_04_build_csv.py` was run with an absolute scratch output path. The CSV is byte-identical, there are 0 quote failures, and the class counts and derived figures match the note.
- **b50-04 sources.** Twelve pages were fetched again live: Rooted in Community and In Abundance (PDF), Triangle and Idaho (PDF), the two Thrivent pages, the two Grapevine help pages, the Grapevine Giving Foundation page, Daffy, Fidelity and Groundswell. The Grapevine Giving Foundation FY2023 990 XML was also read raw.
- **Privacy scan.** All fields of the giving-circles CSV were scanned for personal-name patterns, and every URL slug in the robots log was reviewed by eye.
- **Constraints.** No commit or push. Only the two output files were written to the repo. User agent `research-script/1.0`. A path was fetched only when `*`, `research-script/1.0`, ClaudeBot, anthropic-ai, Claude-User, Claude-Web and Claude-SearchBot were all allowed, or robots.txt returned 404. No off-limits host was contacted.

### robots.txt log (2026-11-20)

| Host | robots.txt | Use |
|---|---|---|
| gt990datalake-rawdata.s3.amazonaws.com | 404: no rules | 1 XML (Grapevine Giving Foundation FY2023); the other 11 XMLs were read from the study cache |
| assets.stanford.edu | 404: no rules | 1 PDF |
| giving.cornell.edu, policy.brown.edu, plannedgiving.mayoclinic.org, giftplanning.columbia.edu, alumni.harvard.edu, www.med.upenn.edu, rochester.edu, plannedgiving.yale.edu, alumni.und.edu | 200; all checked agents allowed | 1 page each |
| johnsoncenter.org, trianglecf.org, www.idahocf.org, thriventcharitable.thrivent.com, help.grapevine.org, www.grapevine.org, www.daffy.org, www.fidelitycharitable.org, www.groundswell.io | 200; all checked agents allowed | 12 pages |

## 2. Counts

| Result | b50-03 | b50-04 | Total |
|---|---|---|---|
| Confirmed | 14 | 10 | 24 |
| Partially confirmed | 3 | 3 | 6 |
| Contradicted | 1 | 0 | 1 |
| Unverifiable | 0 | 0 | 0 |
| **Rows** | **18** | **13** | **31** |

## 3. Findings

### 3.1 b50-03, institutional DAF programmes: accept, with rounding, one mischaracterisation and a netting note

1. **The build reproduces, and the arithmetic holds.**
   - The scratch rebuild is byte-identical, and the four tiers sum to the corrected market totals.
   - The segment rule recounts as 131 "Universities and Healthcare" EINs plus 53 "Other" EINs with NTEE B (45), F (4), E (2) or H (2).
   - Sponsor counts are 165, 168, 174 and 171.
   - Segment assets are $3,222,881,188 in FY2021 and $3,586,202,268 in FY2024 (+11.3%, against +38.1% for the market).
   - Average account size is $905,835, against $97,680 for the market.
   - The top 10 hold 81.45%, 82.72%, 83.37% and 81.47%.
2. **Every share in §0 and §2.1 is truncated rather than rounded (V50B-04, -05).**
   - The institutional asset share runs 1.38% → 1.50% → 1.40% → 1.11%, not 1.37% → 1.10%.
   - The all-T4 share runs 5.95% → 4.67%, not 5.94% → 4.66%.
   - Some grant and contribution shares move by 0.01 pp in the same way.
   - The trend and the conclusions are unchanged. The corrections below fix §0 and 12 table rows.
3. **The filings bear out every filing-level claim (V50B-08 to -14).**
   - UCLA's filed DAF grants are −$109,714,372 and −$120,260,861.
   - Montréal's FY2024 imputed value of $427,129,062 is kept with `applied = 0`.
   - SUNY Binghamton's single Schedule I line of $84,184,036 to EIN 200849590 equals its Schedule D DAF grants. Its DAF assets fell from $236,056,744 to $158,178,210.
   - Cornell University received $9,233,114 of $13,553,754 (68.1%).
   - Harvard's DAF-worded lines total $21,035,198. After removing the $7,681,000 American Repertory Theatre line, $13,354,198 of $23,158,713 is DAF-labelled and non-host.
   - Rochester and Penn Presbyterian both report Part IX line 1 = 0.
   - One accounts figure is wrong: UCLA's corrected account counts are 12, 10, 10 and 10, so the range is 10–12, not 10–11.
   - SUNY Binghamton reports **one** DAF in both years. Its "programme" is a single $158–236m fund.
4. **Greater Horizons is mischaracterised (V50B-11, contradicted).**
   - The note calls it "a community-foundation DAF sponsor" that "the repo does not profile".
   - DAFRC classes it as National (Standard), and it ranks 17th by FY2024 DAF assets.
   - The repo profiles it in the capabilities, SOC 2 and ecosystem notes, and it is on the DAF-to-DAF whitelist.
   - Repo notes tie it to GKCCF, so "a CF-affiliated national sponsor" is the defensible wording.
5. **P-B5003-06: R5 netting already removes the transfer from the market totals, but not from this study's segment (V50B-18).**
   - Greater Horizons is on `daf-to-daf-recipient-whitelist.csv` as `include`, rule W2, with a DAF share of assets of 0.867.
   - The FY2024 line is netted at $65,147,879 in the lower tier (grantor DAF-share weight 0.774), $56,514,286 in the central tier (weight 0.671) and $84,184,036 in the upper tier. No cap binds.
   - b50-03's segment table uses un-netted corrected values. The transfer is therefore 16.2% of FY2024 institutional DAF grants: $521.1m with it, $436.9m without.
   - FY2024 segment grants also carry UCLA's imputed +$169.9m.
   - The rising FY2024 grants figure is therefore mostly two data items, not programme behaviour.
6. **The host-retention bounds reproduce, but one transfer drives the FY2024 bound (V50B-15).**
   - The bounds are 0.0566–0.6919 for FY2024 and 0.3939–0.9059 for FY2023.
   - SUNY Binghamton is 27% of FY2024 D, at a host share of 0–18%. Without it, the FY2024 bound is 8%–88% over 17 returns and $224.0m.
   - Most of the apparent FY2023→FY2024 fall in host retention is that one transfer.
7. **The policy quotes are confirmed (V50B-16, -17).**
   - All 18 fragments re-read verbatim on the live pages.
   - That covers the Stanford 50/40/30% tiers, Cornell's 50%/25%/none, Brown's one-quarter (effective September 7, 2023), Mayo's 60%, Columbia's, Harvard's and Penn's 50%, Rochester's vesting tiers, Yale's 50% and UND's 51%.
   - The entry minimums of $100k at Cornell, Brown, Mayo, UND and Rochester are confirmed.

### 3.2 b50-04, giving circles: accept, with an interpretation fix, an evidence caveat and a privacy flag

1. **The Johnson Center figures are confirmed (V50B-19, -20).**
   - Rooted in Community, p. 6, gives the host shares: CF 42%, technology platform 24%, nonprofit 7%, women's fund 3%, and 24% "operate independently without a fiscal sponsor". The five sum to 100%.
   - In Abundance gives nearly 4,000 groups, about 370,000 philanthropists and more than $3.1bn for 2017–2023.
   - It also gives the 45% hosted by a CF or women's fund, 543 group responses and the Q36 wording.
2. **"Three-quarters inside someone else's 501(c)(3)" overreaches (V50B-21).**
   - 76% use a third-party host or platform.
   - The platform option in the survey reads "e.g., Grapevine, GoFundMe". Only some platforms pool through a 501(c)(3).
3. **Product terms are confirmed verbatim (V50B-22 to -26).**
   - Triangle: $10,000 non-endowed fund; fee of 1% or $300.
   - Idaho: $25,000 minimum; 2.0% fee, $500 minimum; gift fees of 1–10%; the partner is advisory.
   - Thrivent: "in the form of a donor-advised fund", from $200 per person, with no fee and no fund-level minimum stated.
   - Daffy: campaign option dated 2025-08-28, up to 15 charities.
   - Fidelity: guidance only. Philanthropy Together is a Catalyst Fund grantee.
   - Groundswell: employer campaigns.
   - Grapevine: a 3% fee on off-platform gifts, which explicitly include "Donor Advised Fund grants". Its is-grapevine-free page conflicts on fees, as the note already flags. That page also puts ACH at 0.8% processing.
4. **The Grapevine Giving Foundation Schedule D figures are confirmed in raw XML (V50B-27).**
   - FY2023: 1 DAF, $10,131,877 contributions, $8,766,981 grants and $3,377,079 at year end.
   - The repo's corrected DAFRC panel replaces the imputed FY2023 grants of $2,656,657 with the filed figure.
   - For FY2024 it keeps imputed contributions of $14,111,183 and grants of $3,356,869, against filed values of $9,924,817 and $8,102,321. The note does not say this; a correction adds it.
5. **The CF sample counts reproduce exactly, but three of the 12 "hosted named circles" rows are thin (V50B-28).**
   - The counts are 1, 12, 1, 2, 1, 1, 11 and 4.
   - Buffalo (GC-018) is classed with no readable page text, and its own note says the search snippets were not used. Its class is unverified.
   - GNOF (GC-015) is a tag listing only.
   - North Texas (GC-013) is a pre-2021 narrative on a live page.
6. **Labelling the ~1,680 and ~960 figures as illustrative is justified (V50B-29).**
   - The arithmetic is exact.
   - The shares come from 543 groups reached through hosts and networks, which the note discloses.
   - The 4,000 base is a cumulative 2017–2023 count, not the number of groups active at one date. A correction adds this.
7. **Pre-2021 rows are handled properly (V50B-30).**
   - GS-004 (the 2017 study) is context only.
   - GC-013 is flagged in `source_date`.
   - GC-041 (Growfund) is marked historical, and its status rests on the repo's FY2023–25 990 reads.
8. **Individuals' names (V50B-31): flag.**
   - The CSV records no individual.
   - The robots log, however, carries personal names in URL slugs: file line 56 (a 2021 Maine CF donor story) and lines 62–64 (a CNY CF fund named after a person, in three language copies).
   - The names are not repeated here. Truncating those URL paths is an owner decision. A correction states this in the note.

## 4. Accept / modify / reject

| Claim | Study | Verdict | Action |
|---|---|---|---|
| Segment definition (131 + 53 EINs) | b50-03 | Accept | — |
| 165 / 168 / 174 / 171 sponsors | b50-03 | Accept | — |
| Assets $3.22bn → $3.59bn | b50-03 | Accept | — |
| Asset share 1.37% → 1.10% | b50-03 | Modify | 1.38% → 1.50% → 1.40% → 1.11%; fix §0 and §2.1 |
| All T4 $13.9bn → $15.1bn; 5.94% → 4.66% | b50-03 | Modify | 5.95% → 6.16% → 5.69% → 4.67% |
| Average account about $0.9m | b50-03 | Accept | — |
| Top 10 hold 81–83% | b50-03 | Accept | — |
| UCLA negative grants | b50-03 | Modify | Accounts 10–12, not 10–11 |
| Université de Montréal | b50-03 | Accept | — |
| SUNY Binghamton $84,184,036 to Greater Horizons | b50-03 | Accept | Add: 1 DAF; R5 nets it; 16% of segment grants |
| Greater Horizons a "community-foundation sponsor" the repo "does not profile" | b50-03 | Reject | National (Standard), rank 17, profiled in the repo |
| Cornell 42% / 68% | b50-03 | Accept | — |
| Harvard $13.4m of $23.2m | b50-03 | Accept | — |
| Rochester and Penn Presbyterian | b50-03 | Accept | — |
| Host-retention bounds 6–69% / 39–91% | b50-03 | Accept | Add: 8–88% without Binghamton |
| Policy-page quotes and minimums | b50-03 | Accept | — |
| P-B5003-06 | b50-03 | Answered | Yes for market totals ($56.5m central, $84.2m upper); no for the segment table |
| Johnson Center 42 / 24 / 24 / 7 / 3% | b50-04 | Accept | — |
| 4,000 groups / 370,000 people / $3.1bn / 45% | b50-04 | Accept | — |
| "Three-quarters inside someone else's 501(c)(3)" | b50-04 | Modify | "use a third-party host or platform" |
| Triangle and Idaho terms | b50-04 | Accept | — |
| Thrivent $200 per person | b50-04 | Accept | — |
| Daffy, Fidelity and Groundswell positions | b50-04 | Accept | — |
| Grapevine 3% fee including DAF grants | b50-04 | Accept | — |
| Grapevine Schedule D 1 DAF, $10,131,877 | b50-04 | Accept | Add: DAFRC FY2024 imputed values |
| CF sample counts | b50-04 | Modify | Note thin evidence for GC-018, GC-015 and GC-013 |
| ~1,680 / ~960 labelled illustrative | b50-04 | Accept | Add that the base is cumulative |
| Pre-2021 handling | b50-04 | Accept | — |
| No individuals named | b50-04 | Modify | Flag the personal names in robots-log URL slugs (owner decision) |

## 5. Limits

- Eleven of the 56 sample returns were re-read in raw XML, plus one Grapevine Giving Foundation return. The other sample rows were checked only through the byte-identical rebuild.
- The UCLA, Michigan State, Minnesota and Indiana policy pages were not fetched again. The four pages the study logged as blocked were not retried.
- The netting answer depends on the existing Schedule I cache (`npcache`), which was not rebuilt.
- The finding that Greater Horizons is affiliated with GKCCF rests on repo notes. Its Schedule R was not read.
- The personal-name scan is pattern-based, and the review of the robots-log URLs was manual.
- The giving-circles CF classifications were not re-derived page by page. Only the sources listed in §1 were re-read.

## Exact corrections

### `research/mission-2026-11-14/b50-03-institutional-daf-programs.md`

**Find:** "- assets 1.37% → 1.49% → 1.39% → **1.10%**;<br>- grants 0.59% → 0.73% → 0.78% → 0.78%;<br>- contributions 0.35% → 1.11% → 0.85% → **0.27%**.<br>**All T4:** assets 5.94% → 6.15% → 5.68% → **4.66%**; contributions 4.3% → 3.7%; grants 5.6% → 6.0%."
**Replace with:** "- assets 1.38% → 1.50% → 1.40% → **1.11%**;<br>- grants 0.60% → 0.74% → 0.79% → 0.78%;<br>- contributions 0.36% → 1.11% → 0.86% → **0.27%**.<br>**All T4:** assets 5.95% → 6.16% → 5.69% → **4.67%**; contributions 4.3% → 3.7%; grants 5.6% → 6.0% (shares rounded half-up from the CSV; earlier figures were truncated). [V wave 50B]"

**Find:** "- **Grants:** $0.29bn, $0.41bn, $0.43bn, **$0.52bn**."
**Replace with:** "- **Grants:** $0.29bn, $0.41bn, $0.43bn, **$0.52bn**. FY2024 includes UCLA’s imputed +$169.9m (filed −$120.3m) and SUNY Binghamton’s $84.2m transfer to Greater Horizons, which R5 nets from market totals but not from this segment ($0.437bn without it). [V wave 50B]"

**Find:** "**Greater Horizons**, a community-foundation DAF sponsor ($84.18m)."
**Replace with:** "**Greater Horizons** ($84.18m). DAFRC classes Greater Horizons as a National (Standard) sponsor, rank 17 by FY2024 DAF assets; repo notes tie it to the Greater Kansas City Community Foundation. R5 netting already removes the line from market totals. [V wave 50B]"

**Find:** "  - It has 10–11 accounts."
**Replace with:** "  - It has 10–12 accounts (corrected panel: 12, 10, 10 and 10 for FY2021–24; the filed FY2024 count of 10 replaces DAFRC’s imputed 11). [V wave 50B]"

**Find:** "| FY2024 | Institutions | 18 | $308.2m | **6%–69%** |"
**Replace with:** "| FY2024 | Institutions | 18 | $308.2m | **6%–69%** (8%–88% over 17 returns, $224.0m, without SUNY Binghamton’s $84.2m transfer) [V wave 50B]"

**Find:** "which the repo does not profile; it is understood to be an affiliate of the Greater Kansas City Community Foundation [I]."
**Replace with:** "which DAFRC classes as a National (Standard) sponsor, rank 17 by FY2024 DAF assets. The repo already profiles it (capabilities and SOC 2 notes, the top-50 league table, and the DAF-to-DAF whitelist), and repo notes tie it to the Greater Kansas City Community Foundation [I]. [V wave 50B]"

**Find:** "  - Its DAF assets fell from $236.1m to $158.2m [F]. See P-B5003-06."
**Replace with:** "  - Its DAF assets fell from $236.1m to $158.2m [F]. See P-B5003-06.\n  - **P-B5003-06 answer (validator).** In the market totals, yes. Greater Horizons (EIN 200849590) is on `daf-to-daf-recipient-whitelist.csv` as include, rule W2 (DAF share of assets 0.87). A read-only re-run of `scripts/mission_market_netting.py` reproduces `dafrc-market-totals-netted.csv` exactly and nets this FY2024 line at $65,147,879 (lower tier, weight 0.774), $56,514,286 (central, weight 0.671) and $84,184,036 (upper), with no cap binding. In this note’s segment table, no: §2.1 uses un-netted corrected values, and the line is 16% of FY2024 institutional DAF grants ($0.521bn, or $0.437bn without it). Schedule D line 1a reports one DAF in both years, so the programme is a single fund. [V wave 50B]"

**Find:** "| 2021 | Institutions (edu/health) | 165 | 3.223 | 1.37% | 0.278 | 0.35% | 0.287 | 0.59% | 12.4% |"
**Replace with:** "| 2021 | Institutions (edu/health) | 165 | 3.223 | 1.38% | 0.278 | 0.36% | 0.287 | 0.60% | 12.4% [V wave 50B]"

**Find:** "| 2022 | Institutions | 168 | 3.413 | 1.49% | 0.849 | 1.11% | 0.409 | 0.73% | 12.7% |"
**Replace with:** "| 2022 | Institutions | 168 | 3.413 | 1.50% | 0.849 | 1.11% | 0.409 | 0.74% | 12.7% [V wave 50B]"

**Find:** "| 2023 | Institutions | 174 | 3.579 | 1.39% | 0.561 | 0.85% | 0.432 | 0.78% | 12.7% |"
**Replace with:** "| 2023 | Institutions | 174 | 3.579 | 1.40% | 0.561 | 0.86% | 0.432 | 0.79% | 12.7% [V wave 50B]"

**Find:** "| 2024 | Institutions | 171 | 3.586 | 1.10% | 0.253 | 0.27% | 0.521 | 0.78% | 14.6% |"
**Replace with:** "| 2024 | Institutions | 171 | 3.586 | 1.11% | 0.253 | 0.27% | 0.521 | 0.78% | 14.6% [V wave 50B]"

**Find:** "| 2024 | Mission charities | 108 | 0.471 | 0.14% | 0.241 | 0.25% | 0.267 | 0.40% | 57.0% |"
**Replace with:** "| 2024 | Mission charities | 108 | 0.471 | 0.15% | 0.241 | 0.26% | 0.267 | 0.40% | 57.0% [V wave 50B]"

**Find:** "| 2021 | Religious (T4 only) | 178 | 8.508 | 3.63% | 1.791 | 2.30% | 1.369 | 2.85% | 20.0% |"
**Replace with:** "| 2021 | Religious (T4 only) | 178 | 8.508 | 3.64% | 1.791 | 2.31% | 1.369 | 2.85% | 20.0% [V wave 50B]"

**Find:** "| 2021 | Intermediaries (NTEE T) | 78 | 1.693 | 0.72% | 1.005 | 1.29% | 0.823 | 1.71% | 57.5% |"
**Replace with:** "| 2021 | Intermediaries (NTEE T) | 78 | 1.693 | 0.72% | 1.005 | 1.30% | 0.823 | 1.71% | 57.5% [V wave 50B]"

**Find:** "| 2024 | Intermediaries (NTEE T) | 84 | 1.238 | 0.38% | 0.634 | 0.68% | 0.710 | 1.06% | 49.9% |"
**Replace with:** "| 2024 | Intermediaries (NTEE T) | 84 | 1.238 | 0.38% | 0.634 | 0.68% | 0.710 | 1.07% | 49.9% [V wave 50B]"

**Find:** "| 2021 | **All T4** | 547 | 13.921 | 5.94% | 3.338 | 4.30% | 2.701 | 5.62% | 24.6% |"
**Replace with:** "| 2021 | **All T4** | 547 | 13.921 | 5.95% | 3.338 | 4.31% | 2.701 | 5.62% | 24.6% [V wave 50B]"

**Find:** "| 2022 | All T4 | 555 | 14.053 | 6.15% | 4.265 | 5.57% | 3.045 | 5.47% | 21.9% |"
**Replace with:** "| 2022 | All T4 | 555 | 14.053 | 6.16% | 4.265 | 5.58% | 3.045 | 5.48% | 21.9% [V wave 50B]"

**Find:** "| 2023 | All T4 | 579 | 14.586 | 5.68% | 3.464 | 5.30% | 3.570 | 6.51% | 25.4% |"
**Replace with:** "| 2023 | All T4 | 579 | 14.586 | 5.69% | 3.464 | 5.30% | 3.570 | 6.51% | 25.4% [V wave 50B]"

**Find:** "| 2024 | **All T4** | 580 | 15.087 | 4.66% | 3.390 | 3.65% | 3.968 | 5.97% | 27.2% |"
**Replace with:** "| 2024 | **All T4** | 580 | 15.087 | 4.67% | 3.390 | 3.65% | 3.968 | 5.97% | 27.2% [V wave 50B]"

### `research/mission-2026-11-14/b50-04-giving-circles.md`

**Find:** "No circle member is named, even where a source page names one."
**Replace with:** "No circle member is named, even where a source page names one. The companion robots log does carry URL slugs that contain individuals’ names: a 2021 Maine CF donor story (file line 56) and a CNY CF fund named after a person (file lines 62–64). Whether to truncate those URLs is an owner decision. [V wave 50B]"

**Find:** "Roughly three-quarters of circles therefore keep their money inside someone else's 501(c)(3), and community foundations are the largest single host."
**Replace with:** "Roughly three-quarters of circles (42 + 24 + 7 + 3 = 76%) therefore use a third-party host or platform, and community foundations are the largest single host. For the 24% platform share, the money sits in a 501(c)(3) only where the platform pools through one, as Grapevine does; the survey option also named GoFundMe. [V wave 50B]"

**Find:** "computed as 42% and 24% of 4,000 on the assumption that survey shares generalise."
**Replace with:** "computed as 42% and 24% of 4,000 on the assumption that survey shares generalise. The 4,000 is a cumulative 2017–2023 count of groups, not the number active at one date, so these figures are cumulative too. [V wave 50B]"

**Find:** "Supplement: Triangle CF is coded explicit_gc_fund_product (GC-034); Sacramento is blocked (GC-035)."
**Replace with:** "Supplement: Triangle CF is coded explicit_gc_fund_product (GC-034); Sacramento is blocked (GC-035).\n\nValidator note: the counts reproduce, but three of the 12 hosted_named_circles rows rest on thin evidence. Buffalo (GC-018) has no readable page text, and its row says the search snippets were not used as evidence, so its class is unverified. GNOF (GC-015) is a tag-page listing only. North Texas (GC-013) is an undated narrative citing 2015 and 2018. [V wave 50B]"

**Find:** "Whatever the legal reading, circle money held by the platform flows through lines that DAF market statistics count, while the account count stays at 1."
**Replace with:** "Whatever the legal reading, circle money held by the platform flows through lines that DAF market statistics count, while the account count stays at 1. The corrected DAFRC panel uses the filed FY2023 grants ($8,766,981, rule R1, replacing an imputed $2,656,657). For FY2024 it keeps DAFRC’s imputed values: contributions $14,111,183 and grants $3,356,869, against filed $9,924,817 and $8,102,321. DAFRC classes the foundation as National, Donation Processor. [V wave 50B]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

**Find:** "\n---\n\n## Source register"
**Replace with:** "\n\n### 11.76 Institutional DAF programmes and giving circles (validated, wave 50B)\n\n**Institutional DAF programmes and giving circles** (validated, wave 50B). A scratch rebuild of b50-03 reproduced its CSV byte for byte. University, school and health-system sponsors number 165, 168, 174 and 171 in FY2021–24 and hold $3.22bn rising to $3.59bn, about $0.9m per account; their share of corrected DAF assets falls from 1.38% to 1.11% (all single-issue sponsors: $13.9bn to $15.1bn, 5.95% to 4.67%). The top 10 hold 81–83%. Published host minimums, usually 50% and lower for large funds, were re-read verbatim at ten programmes. Schedule I bounds the host’s share of FY2024 DAF grants at 6–69%, pulled down by SUNY Binghamton Foundation’s $84.2m transfer to Greater Horizons, a National-class sponsor; rule R5 already nets that line from market totals ($56.5m in the central tier). For giving circles (b50-04), the Johnson Center survey puts 42% of groups at community foundations, 24% on platforms and 24% unhosted; nearly 4,000 groups gave over $3.1bn in 2017–2023. Few sponsors publish circle-fund terms; Thrivent sells one as a DAF, and Grapevine’s pooling foundation reports a single DAF ($10,131,877 contributions in FY2023) (repo [`validation-wave50b-report.md`](mission-2026-11-14/validation-wave50b-report.md)). [V wave 50B]\n\n---\n\n## Source register"
