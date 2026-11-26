# Thoroughness gap audit (2026-11-19)

**Purpose.** This audit tells the owner where the DAF research is still not thorough. It does not restate findings. Every judgement below points to a repository file or a count computed from one.

**Inputs read.** These are the mission requirements as reconstructed from [`00-baseline-inventory-and-mission-plan.md`](00-baseline-inventory-and-mission-plan.md) §5 and [`FINAL-STATUS.md`](FINAL-STATUS.md). The audit also used:
- [industry report](../DAF-INDUSTRY-REPORT-2026-11.md) §1–§11 and [`strategic-synthesis.md`](strategic-synthesis.md);
- `coverage-matrix-entities.csv` and `coverage-summary.json`;
- `research-priority-queue.csv` (536 items);
- the "Limits" sections of `validation-wave*-report.md` (waves 14–30 have them; waves 1–13 do not have a section with that name);
- the 33 `direction-*.md` documents;
- `scripts/mission_citation_audit.py`, run on 2026-11-19.

**Method limits.**
- No web fetching. Claims about what public sources exist, or are newer, are expectations to be tested, not findings.
- §2 and §5 use keyword and heading heuristics. They show where to look; they do not prove a gap.

**Overlap with the current thoroughness pass.** Commit `767dd5e` started three other workstreams: a monitoring sweep, crt.sh re-sourcing and link health. This audit does not duplicate them. Items that those passes may close are marked *(sibling pass)*.

---

## 0. Verdict in brief

1. **Breadth is real, but the depth gauge is broken.** The coverage matrix has not been reassessed since the baseline. All 396 cells still read `coordinator baseline 2026-11-14 (not independent validation)`. Keyword reconciliation finds that later datasets touch about 77 of the 206 cells marked "not investigated" or "discovery started". About 129 cells still have no later evidence. These are concentrated in wealth channels (Edward Jones, SEI, OneAscent, TIAA, Pave) and infrastructure vendors (Foundant, NPact, DAF Direct, Candid).
2. **Headline structural claims lean on inference or vendor statements.** Four examples: Ren's ~28% technology footprint (about half of it is NPT, on hosting evidence only), Give Interactive at Vanguard Charitable (vendor release; go-live not observed), "data and automation are contractually closed" (public templates only) and the DAFgiving360 fee schedule (a search snippet of a page that returned 403).
3. **The AI economics still turn on assumed behaviour.** Costs are now observed. Time saving, QA re-review, amenability and process share are still triangular guesses, and the red team showed that the rankings follow them. A public calibration from cross-industry evidence has not been tried.
4. **Recency is mostly good. The gaps are FY2025 filings and specific old documents.** Market, concentration and vendor-footprint figures are FY2024, or a partial FY2025 (26 of the top 50 had not filed). Some fee, terms and rail evidence dates from 2008–2024.
5. **The headline documents are layered and partly stale internally.** The report header still says "96 research documents and 89 datasets", against 248 and 470. §2 still says "131 nodes and 167 edges", against 1,088 edges across 26 files. §9's validation table still shows the first 80 claims, against 859 register rows. The synthesis carries three successive top-ten lists.

---

## 1. Requirement scorecard

Status scale: **strong** (requirement met with validated, current evidence), **adequate** (met, with known gaps), **thin** (partially met; important parts rest on few sources or assumptions), **missing** (not done).

| # | Requirement (source) | Status | Evidence in repo | Specific gap |
|---|---|---|---|---|
| 1 | Baseline inventory (plan §1–2) | **Strong** | `00-baseline-inventory-and-mission-plan.md`; `repo-inventory-baseline.json`, `repo-inventory-final.json`; FINAL-STATUS count tables recomputed through PR #50 | Report header (line 7) still cites the baseline-era "96 documents / 89 datasets". The 59 pre-mission `data/*.csv` files are inventoried but only 7 have a dictionary entry (§5). |
| 2 | Coverage matrix (plan §3) | **Thin** | `scripts/mission_coverage.py`; 33 entities × 12 items = 396 cells | Never re-assessed after 2026-11-14: every cell has `assessed_by` = coordinator baseline. 148 NI and 58 DS cells are stale in both directions: about 77 are touched by later datasets, and about 129 have no evidence (§2). The queue's breadth bonus is computed from this stale matrix. The denominator is purposive (33 entities against about 1,500 sponsors). |
| 3 | AI economics, interventions A–D (plan wave 1; `ai-economics-*`) | **Adequate on cost, thin on behaviour** | v1 (16 processes); v2/v2b Monte Carlo with Form 990 Part IX costs (8,078 result rows); red team 2A | Time saving *s*, QA re-review *q*, amenability *a*, redesign share *d* and process share φ are still assumed (`ai-economics-v2-observed-costs.md` §3.2). No measured exception rate or handling time exists anywhere (Q-N03 blocked). Cross-industry public calibration was not attempted. "AI ranks last" was shown to be set by assumptions (V2A-04). |
| 4 | AI-native competitor simulation | **Adequate** | `ai-native-entrant-simulation.md`; `entry-strategy-comparison.csv` (36 rows); buy/build matrix (20) | The break-even (76k–369k grants a year per customer) rests on the assumption-driven model, and the red team judged S3 a *conditional probe* (V2A-21, low confidence). Integration cost per sponsor is reasoned, not measured. No public integration-effort comparables (e.g. Chariot certification timelines) are collected. |
| 5 | Vendor dependency graph, incl. Ren, Edward Jones and financial institutions | **Adequate on Ren/RCF, thin on other channels** | 131 nodes; 167 base edges plus 25 addition files = 1,088 edges (956 confirmed, 81 inferred, 11 unknown) | The graph was never merged. 886 entities in edges have no node record. Concentration and hub statistics and the red-team sample (15 of 167) predate about 900 edges. Edward Jones: private DAF unknown; Ren back-office role inferred; $2.9bn unverifiable. U.S. Bank and Merrill have 0 edges, PNC 1, Wells Fargo 3. The Commonwealth→RCF sponsorship is inferred (E034). |
| 6 | AI governance and failure modes | **Adequate** | `ai-governance-failure-modes.md`; 16-mode register; AI product census (30 products, wave 28) | Risk ratings are a rubric, not observed incidents (V2A-30, low). Four "GREEN" grantmaking overlays are provisional (P-B43N25-01 open). The donor-side controls of Daffy MCP and Louise are documented only by the vendors' own pages. |
| 7 | Clarity/EDF incentives | **Thin** | `industry-incentives-structural-analysis.md` (EDF on 3 outcomes); `incentive-map.csv` (34 rows); application guide (682 words) | EDF was applied only to three 2026-11-14 outcomes (paper checks, 10-day review, transfer friction). 29 of the 33 direction docs never mention Clarity or EDF, though several are incentive findings: the CF cost gap, flat CF pay, data-sharing defaults and the absence of a standard. |
| 8 | Company timelines; announced vs delivered | **Adequate, stale** | 195 timeline events; 39 announced capabilities (15 delivered, 10 partial, 12 no evidence, 2 contradicted) | Not refreshed since 2026-11-14. Several announced dates have passed unchecked (Charityvest's Chariot switch, Aug 2026; the Confluence 2026 rollout; GiveClear Direct; Benevity Alaya by 2026-12-15). There are no rows for Give Interactive, Foundant/GivingData, Blackbaud Giving Fund, Endaoment, Every.org or Givinga, although later work shows them to be central. |
| 9 | Validation and red team | **Strong, with a stated ceiling** | 859 register rows (waves 1–30): 659 confirmed, 158 partially confirmed, 23 contradicted, 12 unverifiable; red teams 2A/2B | Same model family (cross-agent, not cross-executor). Waves 14–30 list many items "not re-checked" (e.g. wave 26 checked 4 of 49 corporate filings; wave 25A checked 21 of 37 axe pages; wave 17 checked 6 of 5,272 cached returns). Re-runs reused session caches (waves 26, 27, 30), so they test the computation, not the inputs. Coverage cells were never moved to IC from the later registers. |
| 10 | Datasets and data dictionaries | **Adequate** | 409 mission CSVs; most direction and queue docs carry a dictionary | 21 mission CSVs have no dictionary entry, and 52 of 59 pre-mission CSVs are outside the central dictionary (§5). `direction-donor-tax-scenarios-2026.md` has no dictionary for its 3 CSVs. |
| 11 | Prioritisation algorithm | **Adequate in design, weak in use** | `mission_prioritize.py`; EIV formula; dependency and breadth modifiers; all 536 rows scored | Proposing agents score their own items, with no calibration. Dividing by effort lets narrow, cheap items top the open list: #8 overall is a Pushpay watch-page re-read at EIV 96. The breadth factor depends on the stale matrix. 106 open items are mostly narrow refinements. |
| 12 | Syntheses A–G | **Adequate** | `strategic-synthesis.md` with A–G and three appended update layers | Delta layers (wave 13, waves 14–21, waves 22–30) make the current position hard to read. C, D and E are heavily [I]-labelled. The citation audit flags 25 lines, and 7 inference markers have no primary URL. |
| 13 | Top 10 | **Adequate** | Re-ranked three times | #1 (contractually closed) rests on public templates and donor terms, with no executed contract. #7 (Ren below its claims) depends partly on NPT hosting inference. #10 (thin AI value pool) depends on assumed behaviour (rows 3 and 5 above). |
| 14 | Backlog | **Strong in volume** | 536 items: 299 done, 106 open, 75 blocked with reasons, 49 monitoring | About 42 of the 75 blocked items need partners, contracts, logins or owner retrieval, so they are outside public-source reach. FY2025 filing refreshes sit in monitoring, not in the open queue. |
| 15 | Citations | **Adequate** | 3,424 unique URLs; source registers in report and synthesis | `mission_citation_audit.py` flags 149 report lines and 25 synthesis lines that state a figure with no same-line marker. The report has 18 "(source: repo inference — no primary URL)" markers. 8 direction docs have no source register (§5). |
| 16 | Evidence quadrants | **Adequate, stale** | v1.0 → v1.1 blind calibration (74% exact, 99.7% within 1) → v1.2 targeted; 270 position rows | Scored 2026-11-14/15. Since then only the wave-21 Benevity correction has been applied. Not re-scored with the NPT export (wave 23), the iPhi attrition, the accessibility failures (wave 25A), the Give Interactive scope or the agentic census (wave 28). The GS PF Y2 cell is "U" because the only circular dates from 2008. |
| 17 | Failed startups | **Adequate, no denominator** | 50 cases; deep-research doc | Self-stated limits: visibility bias; no systematic search of lapsed registrations or app delistings; no survivor cohort. Wayback content, Crunchbase and PitchBook were not used. |
| 18 | Complaints | **Thin** | 244-row corpus; 17-row normalised rates | 104 of 244 rows are App Store reviews (53 about one app). Reddit was inaccessible, and Bogleheads came via search extraction. There are no per-account denominators. The CFPB query was inconclusive. |
| 19 | Analysts and education | **Adequate** | 44 sources; absence finding (no analyst DAF landscape) | Adviser studies are mostly sponsor-funded and read via press coverage. Primary PDFs sit behind forms (excluded here). There are no conversion data. |
| 20 | Interested firms | **Adequate** | 89 firms | Search-based. 39 of 64 dated rows have evidence over 12 months old. Private deals and LOIs are invisible. 8 open buyer questions (P-BUY-01…08). |
| 21 | PE firms | **Adequate** | 120 company and 60 investor rows; BDC/N-PORT lender work | No lenders found for Ren, Foundation Source (GTCR era), Bonterra, Benevity or Foundant. Form ADV Schedule A/B were not pulled for adviser-owned firms. Several deal dates are missing (`private-equity-daf-ecosystem-map.md` §8). |
| 22 | Recency rule (2021+) | **Adequate** | 5 items deprioritised as historical; most sources 2024–2026 | Specific pre-2021 documents still carry current-state claims, and key FY2025 data is not yet used (§4). |

---

## 2. Coverage-matrix cells still uninvestigated (most important entities)

**How this list was made.** The audit took every NI or DS cell in `coverage-matrix-entities.csv` and checked whether a later dataset mapped to that checklist item names the entity. For example, fees were checked against `sponsor-fee-schedules`, `cf-daf-fee-census` and `all-in-cost-comparison`. Custody was checked against `sponsor-investment-menus` and `sponsor-pool-returns`. Assurance was checked against `vendor-assurance-scope`. A cell is listed below only if no mapped dataset names the entity.

This is a heuristic: a name match is not evidence that the item is answered. Several assurance and operating-evidence cells are probably *insufficient public information*, not *not investigated*, and should be relabelled as such (P-GAP19-02).

**Tier 1: entities central to the top-10 findings**

| Entity | Cells with no later evidence | Note |
|---|---|---|
| Edward Jones | financials, custody_invest, grant_workflow, assurance, ownership_funding, timeline, ai | The mission names it explicitly. Q-B05 and Q-N08 are blocked; the 10-K and ADV routes are not recorded as tried (P-GAP19-07). |
| Ren (RenPSG) | operating_evidence; custody_invest (likely n/a for a vendor) | Corporate revenue is not public. Operating evidence: no customer turnaround or error data. |
| National Philanthropic Trust | assurance, ai | NPT on Ren rests on hosting evidence, not a contract (§3, C01). |
| DAFgiving360 | assurance, ai | Site returns 403 to agents. The fee schedule comes from a search snippet (C08). |
| Vanguard Charitable | assurance, ai | Give Interactive scope not observed (C02). |
| Fidelity Charitable | assurance | Probably IP. |
| Morgan Stanley GIFT | assurance, ai | |
| Goldman Sachs (two programs) | grant_workflow, assurance, timeline, ai | The only public circular is from 2008; gspf.goldman.com disallows robots. |
| Bank of America CGF | assurance, timeline, ai | |
| American Endowment Foundation | financials, grant_workflow, ai | AEF's 990 is in the harvest, but no AEF-specific financial review is recorded. |
| Give Interactive | custody_invest, grant_workflow, ai, operating_evidence | Now holds Vanguard's ledger and several CFs. |
| Foundant (CommunitySuite) | financials, fees, custody_invest, distribution, grant_workflow, timeline, operating_evidence | It holds most of the tail (282 of 351 mapped tail CFs), but the vendor itself is barely profiled. |
| Stellar / iPhi | financials, fees, custody_invest, ai | |

**Tier 2: channels and infrastructure**

| Entity | Cells with no later evidence |
|---|---|
| SEI (SEI Charitable Fund) | financials, fees, custody_invest, grant_workflow, assurance, ai, operating_evidence |
| OneAscent (OneGive) | financials, custody_invest, grant_workflow, assurance, ownership_funding, timeline, ai, operating_evidence |
| TIAA (Charityvest program) | financials, grant_workflow, assurance, ownership_funding, ai, operating_evidence |
| Pave Finance | financials, fees, tech_admin, grant_workflow, assurance, timeline, ai, operating_evidence (mentioned in only 2 datasets) |
| Jewish Communal Fund | fees, distribution, grant_workflow, assurance, ownership_funding, timeline, ai, operating_evidence |
| National Christian Foundation | grant_workflow, assurance, ownership_funding, timeline, ai |
| Silicon Valley CF | distribution, assurance, ownership_funding, timeline, ai |
| NPact | financials, fees, custody_invest, distribution, grant_workflow, ai, operating_evidence |
| DAF Direct | financials, fees, custody_invest, assurance, ai, operating_evidence |
| Candid / IRS BMF | financials, fees, custody_invest, timeline, operating_evidence |
| Givinga | fees, tech_admin, custody_invest, grant_workflow |
| Endaoment | financials, tech_admin, custody_invest, distribution |
| Charityvest | custody_invest, assurance, ai |
| Foundation Source | custody_invest, grant_workflow |
| GiveClear | custody_invest, assurance |
| TIFIN Give / Chariot / Daffy | custody_invest |
| Benevity | custody_invest, grant_workflow |
| RCF | ai |

**Cross-cutting pattern.**
- `assurance` has no evidence for 13 entities, and `ai` for 17.
- For sponsors, assurance is structurally non-public (SOC reports are not published). The matrix should say so (IP) rather than imply the work was skipped.
- For `ai`, a sponsor-level check of privacy policies, AI disclosures and job postings is feasible from public sources, but has not been done for DAFgiving360, Vanguard, NPT, MS GIFT, Goldman, BofA or AEF.

---

## 3. Claims resting on one source, search snippets, vendor self-claims or unverified leads (top 30 by importance)

Importance reflects how much a top-10 finding, a headline figure or the entrant conclusion depends on the claim. "Basis" is the weakest link that carries the claim.

| # | Claim (where) | Basis | Why it matters | Public route to a second source |
|---|---|---|---|---|
| C01 | Sponsors with about 28% of FY2024 DAF assets use Ren technology; nearly half of that is NPT (report §3; FINAL-STATUS #4) | Hosting inference for NPT (iPhi login redirect, shared Ren load balancer, Ren-hosted status page). No NPT contract or 990 payee line. | Sets the Ren footprint range (9.2% named payees vs 28% any use) and top-10 #7 | NPT FY2025 990 Part VII-B; NPT audited statement notes; GivingPoint privacy policy processor list (P-GAP19-01/-03) |
| C02 | Give Interactive holds Vanguard Charitable's DAF recordkeeping (report §2.1; FINAL-STATUS #10) | Vendor's own release (2025-11-04). Ledger-only scope inferred from job postings. Go-live not observed. | Vendor-share picture for the third-largest sponsor | Vanguard Charitable FY2026 audited statements (2026-11, already cited for other figures); FY2026 990 Part VII-B; Vanguard privacy notice |
| C03 | Give Interactive's "$40B+" matches known clients ($41.80bn; $32.59bn without certificate-log hosts) (synthesis C) | Vendor claim; $9.81bn rests on crt.sh certificate hosts (unverified leads) | Vendor concentration and the Ren displacement narrative | *(sibling pass: crt.sh re-sourcing)*; 990 payee lines in FY2025 |
| C04 | Donor data and automation are contractually closed (top-10 #1) | Public vendor templates and donor terms only. NPT's Excel export already breaks part of it. No executed contract has been seen. | The #1 strategic finding and the entrant gating question | SEC material-contract exhibits (TIFIN/AssetMark/SEI/Envestnet 8-K and 10-K exhibits); public-body procurement postings and board minutes that publish executed DAF-platform agreements |
| C05 | No public evidence of AI in sponsor-side approval or eligibility (report §7; synthesis B) | Absence finding: a one-day job-posting snapshot of 12 employers (86 of 168 postings are Blackbaud's) plus the product census | Supports "agentic risk is donor-side" | Sponsor privacy policies, AI-use disclosures and terms for the top 20; a repeat hiring scan (P-B39N5-01 is scheduled for 2027-02) |
| C06 | Daffy's MCP server exposes `make_donation` with no documented cap; TIFIN Louise executes donor requests (report §7) | Daffy docs (absence in docs that change); Louise has only its vendor release and blog (AVD12 partial) | The only two money-moving agentic products | Daffy changelog and terms re-read; TIFIN help-centre or ADV disclosures |
| C07 | Ren SOC 2 is "Type 2" (Jul 2025) vs "Type 1" (Apr 2026) (report §5) | Ren boilerplate in AEF releases; no report seen | Assurance claims for the largest white-label vendor | Probably IP. Check Ren's trust page and customer audit notes; else relabel the cell IP |
| C08 | DAFgiving360 fees: 0.60% on the first $500k and the tiers (report §3) | **Search snippet; page returned 403** (report source register) | Part of the national benchmark (60/45 bps) in the CF 1.7–4.7× ratio | First-party program policy PDF or donor circular; 990 Schedule O fee description |
| C09 | Edward Jones: Ren back-office role "inferred only"; private DAF has no known sponsor; "$2.9bn" unverifiable (report §2.2) | Inference from the RCF–Ren contract; 404 source | Mission names Edward Jones explicitly | Jones Financial Companies 10-K; Edward Jones ADV 2A and Form CRS (P-GAP19-07) |
| C10 | RCF sponsors the Commonwealth Charitable Fund (report §2.2) | Edge E034 "inferred" | Count of RCF wealth programs ("about 11") | LPL/Commonwealth ADV 2A; portal terms |
| C11 | CF median admin fee 100/100/67 bps, 1.7–4.7× nationals (top-10 #6) | n = 34 published schedules; 5 of the dated fee documents are from 2016–2020 | A top-10 finding | Re-fetch current schedules (P-GAP19-09) |
| C12 | Licensed DAF software at "31–94% of sponsors"; Foundant "700+" (report §1 table) | Vendor self-reports plus Tech Impact (Jul 2022) | The repo's own EIN map (361 of 803 CFs) supersedes this, but the table row still cites the old range | Replace with the repo map; drop or footnote the 2022 range |
| C13 | Cost per grant at large nationals is $55–$135 (`sponsor-cost-structure-and-sensitivities.md`) | Self-reported grant counts matched to the nearest 990; the doc itself notes period bias | The anchor for AI value-pool sizing | Period-matched counts from FY2025 annual reports and 990s |
| C14 | NPT processed 159,543 grants in FY2025 (report §4) | Single self-reported annual report | Used in volume and cost ratios | Schedule I line counts (recipients >$5k only; a floor) |
| C15 | "67% of Fidelity grants by EFT" (report §2.5) | Single first-party report; 11 of 20 rail-share observations are over 12 months old | Rail-share picture and the paper-check EDF outcome | Fidelity 2027 Giving Report when published; nonprofit-side receipt panels |
| C16 | Daffy has $2bn in assets (Sep 2026) (report §3) | Company-reported; the latest 990 shows $334.19m (FY2024) | Challenger growth narrative | Daffy FY2025 990 Schedule D (P-GAP19-01) |
| C17 | Charityvest 2025 results (contributions doubled; 48,744 grants) | Company-reported; not comparable to the 990 series [V] | Used to test the entrant break-even | Charityvest FY2025 990 |
| C18 | California AG release names Fidelity, Vanguard and DAFgiving360 as restricting SPLC grants (report §4) | One government release; whether the holds persisted is unknown | The "discretion beyond tax exposure" argument | Sponsor statements and later AG or court filings |
| C19 | About $7.5bn moved sponsor-to-sponsor in 2024 (report §4) | Inequality.org (an advocacy source), cited alone in §4 although the repo has its own netting | Portability and double-counting | Substitute the repo's netted DAF-to-DAF figure (`daf-to-daf-flows-990.csv`) |
| C20 | 69% and 71% back a 10% payout (synthesis F) | Advocate-sponsored Ipsos opt-in polls only | Public-opinion monitor | Look for non-advocate polls (Gallup/AP-NORC/Pew topical modules) |
| C21 | BofA/Escalent 2026: 98% of DAF users cite tax-free growth | Unverifiable (V29-28, low) | Donor-motive claims | Primary BofA study PDF if public; otherwise drop |
| C22 | No state has a DAF payout, reporting or donor-intent mandate (report §6; synthesis A9) | Not a 50-state search (V25A-17 unverifiable) | Regulatory risk framing | Fifty-state legislature search (P-GAP19-14) |
| C23 | At least 12 of 33 large recipients run an in-house DAF | 10 of the 12 rest on search text | Recipient-side competition | Read the 10 gift-office pages directly |
| C24 | Check providers took 7–162 days; ACH 1–2 days (synthesis top-10 #4) | Chariot's own sample (an interested vendor); "only vendors publish measured latency" | Nonprofit-cost finding | Nonprofit-side public disclosures (AFP/forum posts, CF FAQs) |
| C25 | AI named in 29.1% of vendor and 13.3% of sponsor postings (synthesis B) | One snapshot; Blackbaud is 51% of postings | "AI work is at vendors" | Re-scan, with Blackbaud reported separately |
| C26 | NPT's FY2023 Schedule D $22.84bn is "most likely a filer error" (synthesis d) | Inference; audited statements not read (P-B44N27-01 open) | FY2023 CR5/HHI and NPT share | NPT FY2023 audited statements |
| C27 | Foundation Source "DAF OS" metrics and its AI roadmap | Vendor brief (metrics as of 2025-12-31); AVD33/AVD34 have no delivery evidence | The FS/Charityvest/TIAA stack | Customer-side 990s and program circulars |
| C28 | NYCT moving to Sage Intacct + Salesforce; FFTC ledger is Financial Edge NXT | Aggregator copy of job postings (V12-07 weak; V23-06 unverifiable) | CF ledger-family shares | First-party careers pages; 990 Part VII-B |
| C29 | Philanthropi certificates still renew; the CCT Give host's first certificate in June 2025 | crt.sh only (unverified leads) | Vendor-exit and migration dating | *(sibling pass: crt.sh re-sourcing)* |
| C30 | BMO 0.25% flat for the NPT program; Commonwealth RCF revenue share up to 5 bps; Engiven about 4% fee | Unverifiable (V16-09, V25B-30 low); search extract | Adviser and intermediary economics | Current ADV 2A brochures (BMO, Commonwealth); Engiven first-party pricing |

---

## 4. Stale items

### 4.1 Evidence predating 2021 that still carries a current-state claim

- **Goldman Sachs Philanthropy Fund:** seven program-term rows rest on the August 2008 circular (`bank-program-terms-2026.csv`). The v1.2 quadrant left GS PF Y2 as "U" for this reason.
- **CF fee schedules dated 2016–2020:** Minneapolis (2020-09), San Francisco (2019), Greater Cincinnati (2020-07), San Antonio (2020-10) and Toledo (rev. 12-2016) in `cf-daf-fee-census-2026.csv`. All five are in the top-100 fee median.
- **Rev. Proc. 2018-32 summary:** cited via an August 2018 secondary summary (The Tax Adviser) in report §3–§4. The rule is current, but the citation should be the IRS primary text.
- **Eleven base graph edges dated 2012–2020:** for example Stellar→Minneapolis (2012), DAF Direct edges (2013–16) and Salesforce/Skuid→NCF (c.2014–15). They are labelled `historically_confirmed`, which is correct. Any current-state reading of them needs a 2024+ check.
- **Pricing history:** the 2020 fee-minimum items (ThinkAdvisor, Schwab) and the Vennfi 2020 seed release are used as history. That is acceptable under the recency rule.

### 4.2 Key source more than 12 months old, where newer data probably exists

| Item | Source age | Likely newer source |
|---|---|---|
| All market, concentration and vendor-footprint figures | FY2024 (DAFRC Spring 2026); FY2025 is partial (94 sponsors parsed; 26 of the top 50 unfiled) | Tax-year-2025 990s (calendar-year returns due 2026-11-16 on extension) as they reach the mirror; DAFRC FY2025 release (P-GAP19-01) |
| CF software share "31–94%" | Tech Impact, Jul 2022 | The repo's own 2026 EIN map |
| UBS DAF fact sheet | Feb 2023 | Current UBS DAF materials and ADV |
| RCF grantmaking due-diligence policy | rev. Mar 2023 (hosted 2026-02) | Check for a later revision |
| Northwestern Mutual RCF circular | Nov 2024 | 2025/2026 circular |
| Adviser-fee evidence | 21 of 24 rows over 12 months old (AEF 2023–24 filings) | 2026 annual ADV amendments (filed by March 2026) |
| Grant-rail shares | 11 of 20 observations over 12 months old (Vanguard PayPal 2023–24; NPT 2022) | 2026 sponsor reports; nonprofit-side panels |
| Daffy for Developers; Ren Rapid Disbursement Engine | May 2023; Nov 2023 | Current developer docs and Ren pages |
| Baker McKenzie on proposed regs | 2024, search-only | Primary Federal Register text (already cited); 2026 docket comments (P-B39N1-01 open) |
| Announced-vs-delivered and timeline | Reviewed 2026-11-14 | Re-check (P-GAP19-10) |
| Coverage matrix; quadrants | Assessed 2026-11-14/15 | Rebuild (P-GAP19-02); re-score after it |
| Interested firms | 39 of 64 dated rows over 12 months old | Deal and press refresh (lower priority) |

### 4.3 Internal staleness in the headline documents

- **Industry report, line 7:** "96 research documents and 89 datasets". FINAL-STATUS reports 248 and 470.
- **Industry report §2 and `vendor-dependency-concentration.md` line 7:** "131 nodes and 167 edges". There are 1,088 edges across the base file and 25 additions.
- **Industry report §9:** the result table covers "80 consequential claims". The registers hold 859 rows.
- **Strategic synthesis:** three top-ten lists, each superseding the last "for ranking only".

---

## 5. Documents lacking a source register or data dictionary; datasets lacking a dictionary entry

### 5.1 Direction docs without a source register

These were identified by heading search plus a URL count. Filing-based docs cite return object IDs inside their CSVs, so their sources exist but are not visible in the document.

| Doc | Inline URLs | Note |
|---|---|---|
| `direction-league-table-concentration.md` | 0 | Sources in the CSVs only |
| `direction-nonprofit-donate-pages.md` | 0 | 182 scanned pages listed in the CSV only |
| `direction-sponsor-accessibility-service.md` | 0 | 37 audited pages in the CSV only |
| `direction-sponsor-marketing-spend.md` | 0 | 990 object IDs in the CSV only |
| `direction-long-tail-sponsors.md` | 1 | |
| `direction-cf-consolidation-fees.md` | 33 inline | No consolidated register; fee-source dates live in the CSV |
| `direction-news-hiring-signals.md` | 33 inline | No register |
| `direction-donor-tax-scenarios-2026.md` | 11 inline | **No register and no data dictionary** for `donor-tax-scenarios-2026.csv`, `donor-tax-scenarios-2026-sensitivity.csv` and `donor-tax-parameters-2026.csv` |

### 5.2 Other mission docs without a source-register heading

The ones that matter most are:
- `sponsor-cost-structure-and-sensitivities.md` (19 URLs);
- `sponsor-mortality-analysis.md` (35);
- `queue-ren-iphi-attrition.md` (109);
- `queue-watchlist-and-vendor-moves.md`;
- `queue-nonprofit-side-panel.md`;
- `queue-bdc-coverage-migrations-goodstack.md`;
- `queue-cf-vendor-map.md`;
- `ai-economics-v2-observed-costs.md`;
- `00-baseline-inventory-and-mission-plan.md`;
- `red-team-wave2b-graph-data-incentives.md`;
- all quadrant rationale and calibration docs;
- `evidence-quadrant-methodology.md`.

The quadrant docs and `evidence-quadrant-methodology.md` also have **no data dictionary** for the quadrant CSVs.

### 5.3 Mission datasets with no dictionary entry

These 21 files are not described under any dictionary, schema or columns heading in `research/**`. Proposal files, validation registers, per-scorer quadrant score files and graph-edge addition files were excluded from the check.

- **Analysis outputs:** `ai-economics-v2b-results.csv`, `aogf-benevity-reconciliation.csv`, `form990-top-contractors.csv`, `give-interactive-client-timeline.csv`, `sponsor-app-defects-2021plus.csv`, `sponsor-grant-payment-policies.csv`.
- **BDC files:** `bdc-loans-daf-ecosystem-v1.csv`, `bdc-loans-daf-ecosystem-v2.csv`, `bdc-loans-latest-marks-v2.csv`.
- **Tax scenarios:** `donor-tax-parameters-2026.csv`, `donor-tax-scenarios-2026.csv`, `donor-tax-scenarios-2026-sensitivity.csv`.
- **Quadrants:** `quadrant-positions.csv` (cited 13 times, including by the report); `quadrant-calibration-criteria.csv`, `quadrant-calibration-criteria-v11-vs-v11blind.csv`, `quadrant-calibration-criteria-v12a-vs-v12b.csv`; `quadrant-calibration-providers.csv`, `quadrant-calibration-providers-v11-vs-v11blind.csv`, `quadrant-calibration-providers-v12a-vs-v12b.csv`.
- **Mission infrastructure:** `coverage-matrix-entities.csv` (described in prose only), `research-priority-queue.csv` (columns explained only in the proposals README).

**Pre-mission data.** Of the 59 top-level `data/*.csv` files, only 7 appear in `quantitative-datasets-and-data-dictionary.md`. Several have companion `*-source-register-*.csv` files, but there is no column dictionary.

---

## 6. Prioritised plan (public sources only)

The plan excludes anything that needs outreach, logins, forms, partner data or owner retrieval. Machine-readable rows are in [`queue-proposals-gap19.csv`](../../data/mission-2026-11-14/queue-proposals-gap19.csv), scored on the queue's scales.

**How the order was set.** The order below is by judgement: the importance of the conclusion affected, then expected value per effort. The mechanical EIV is shown for comparison. It ranks P-GAP19-02 first because the formula divides by effort.

| Rank | ID | Task | Expected value | Effort | EIV |
|---|---|---|---|---|---|
| 1 | P-GAP19-01 | FY2025 Form 990 re-harvest (Schedule D, VII-B, I, F) and re-run of league table, netting and vendor footprint | High: refreshes every market, concentration and vendor-share headline; first public test of the Give Interactive switch and of Daffy's $2bn | 3 (mirror lag) | 46.7 |
| 2 | P-GAP19-03 | Second-source pass on C01–C10 | High: each top-10 dependency either confirmed or relabelled | 3 | 40.0 |
| 3 | P-GAP19-02 | Rebuild the coverage matrix from waves 3–30 (with IP relabels) | High for honesty: fixes the mission's own depth gauge and the queue's breadth bonus | 2 | 112.5 |
| 4 | P-GAP19-04 | Calibrate AI time-saving, QA and amenability from public empirical studies; re-run v2/v2b | High: the AI A–D ranking and top-10 #10 turn on these | 3 | 37.3 |
| 5 | P-GAP19-05 | Public exception-load proxy for the top 50 from Schedule I/F and BMF | Medium-high: replaces the four-national 2.5–3% with a distribution; a substitute for the blocked time-and-motion study | 2 | 44.8 |
| 6 | P-GAP19-12 | EDF on four new observed outcomes | Medium-high: closes the Clarity/EDF requirement for post-baseline findings | 2 | 48.0 |
| 7 | P-GAP19-07 | Edward Jones from the 10-K, ADV and Form CRS, and RCF filings | Medium-high: a named mission target with 7 uncovered cells | 2 | 36.0 |
| 8 | P-GAP19-08 | SEI, OneAscent, TIAA, Pave profiles; Wells/Merrill/PNC/U.S. Bank/Baird/Truist channel test | Medium: channel blind spots | 3 | 32.0 |
| 9 | P-GAP19-06 | Merge the graph (1,088 edges), add missing nodes, red-team 40 inferred/unknown edges | Medium: §2 statistics and single-point-of-failure list are 6.5× out of scope | 3 | 25.6 |
| 10 | P-GAP19-09 | Refresh stale fee, terms and rail evidence; recompute the CF/national ratio with a source-age column | Medium: protects top-10 #6 | 2 | 28.8 |
| 11 | P-GAP19-10 | Announced-vs-delivered refresh plus at least 15 new rows | Medium | 2 | 25.3 |
| 12 | P-GAP19-11 | Report and synthesis consistency and citation pass; one current top ten | Medium: readability and auditability | 2 | 13.5 |
| 13 | P-GAP19-13 | Complaints from BBB, Trustpilot and Google Play, with per-account denominators | Low-medium | 3 | 13.5 |
| 14 | P-GAP19-14 | Fifty-state "donor advised" legislative search | Low-medium: converts an unverified negative | 3 | 12.0 |
| 15 | P-GAP19-15 | Failed-startup survivor cohort (denominator) | Low-medium | 3 | 11.2 |

**What this plan cannot fix.** These items are blocked on non-public evidence and stay blocked:
- a sponsor time-and-motion study (Q-N03);
- executed contracts beyond whatever public filings exist (P-CON-01);
- sponsor SOC report scope;
- program-level asset figures for private-label books (P-GPT-03);
- the paywalled or form-gated adviser and nonprofit benchmark reports (P-B40N12-01, P-B44N28-02).

The report should continue to present the conclusions that depend on them as conditional.

---

## 7. Limits of this audit

- **No fetching.** Where §4 says newer data "probably" exists, that is an expectation to be tested.
- **Heuristic reconciliation in §2.** A name appearing in a mapped dataset was treated as coverage. Some cells listed as uncovered may be answered in prose, and some "covered" ones may be shallow.
- **Judgement in §3.** The importance ranking is the auditor's judgement. The basis column is taken from the repo's own labels: the validation registers, `[V]`/`[I]` tags and source-register annotations.
- **Same model family.** This audit was done by an agent of the same model family as the researchers and validators.

## Source register (repository files and commands used)

- `research/mission-2026-11-14/FINAL-STATUS.md`; `00-baseline-inventory-and-mission-plan.md`; `strategic-synthesis.md`; `research/DAF-INDUSTRY-REPORT-2026-11.md` (incl. source register lines 924–1058)
- `research/mission-2026-11-14/validation-wave14-report.md` … `validation-wave30-report.md` ("Limits" sections); `red-team-wave2a-ai-and-entrant.md`; `red-team-wave2b-graph-data-incentives.md`
- `research/mission-2026-11-14/direction-*.md` (33 files; heading and URL scan)
- `research/mission-2026-11-14/ai-economics-replacement-analysis.md`, `ai-economics-v2-observed-costs.md`, `ai-native-entrant-simulation.md`, `ai-governance-failure-modes.md`, `industry-incentives-structural-analysis.md`, `competitive-history-timelines.md`, `failed-daf-startups-deep-research.md`, `daf-user-complaints-deep-research.md`, `analyst-and-education-landscape.md`, `firms-interested-in-daf-organizations.md`, `private-equity-daf-ecosystem-map.md`, `vendor-dependency-concentration.md`, `quadrant-*.md`, `sponsor-cost-structure-and-sensitivities.md`
- `data/mission-2026-11-14/coverage-matrix-entities.csv`, `coverage-summary.json`, `research-priority-queue.csv`, `validation-register*.csv`, `relationship-graph-edges*.csv`, `relationship-graph-nodes.csv`, `announced-vs-delivered.csv`, `company-timeline-events.csv`, `cf-daf-fee-census-2026.csv`, `bank-program-terms-2026.csv`, `adviser-fee-evidence-2026.csv`, `grant-rail-shares-panel-2026.csv`, `daf-hiring-signals-2026.csv`, `vendor-assurance-scope-2026.csv`, `queue-proposals-README.md`
- `python3 scripts/mission_citation_audit.py` (2026-11-19): 149 flagged lines in the report and 25 in the synthesis
