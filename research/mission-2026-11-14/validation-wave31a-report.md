# Validation wave 31A: thoroughness pass part A (AI calibration, graph consolidation, FY2025 refresh, coverage matrix)

**Date:** 2026-11-19. **Validator:** independent-validation-agent-wave31a.
**Register:** [`validation-register-wave31a.csv`](../../data/mission-2026-11-14/validation-register-wave31a.csv), rows V31A-01 to V31A-43.
**Documents validated:**
- [gap19-ai-calibration.md](gap19-ai-calibration.md), with `ai-calibration-evidence-2026-11-19.csv` (21 sources), `ai-process-economics-calibrated-2026-11-19.csv` (23,577 rows) and `scripts/mission_ai_economics_calibrated.py`
- [gap19-graph-consolidation.md](gap19-graph-consolidation.md), with `relationship-graph-edges-consolidated-2026-11-19.csv` (1,059 rows), `relationship-graph-redteam-2026-11-19.csv` (109 rows) and `scripts/mission_graph_consolidate.py`
- [gap19-fy2025-refresh.md](gap19-fy2025-refresh.md), with `form990-harvest-fy2025-refresh.csv` (977 rows) and the other `-fy2025-refresh` files
- [coverage-matrix-rebuild-2026-11-19.md](coverage-matrix-rebuild-2026-11-19.md), with `coverage-matrix-entities-2026-11-19.csv` (396 cells), including the 20 `ai` cells taken from `ai-coverage-20-entities-2026-11-19.csv`

**Method:** public sources only. I did not log in, submit forms, solve CAPTCHAs, make keyed API calls or contact anyone. I did not use crt.sh or certspotter. I read robots.txt on each host before fetching anything from it:
- `api.openalex.org` (Allow /), `arxiv.org` (/abs allowed; I kept 15 s between requests), `www.nber.org` (/system/files not disallowed), `www.gov.uk` (Content API not disallowed), `www.bankofengland.co.uk` (/report not disallowed), `www.prnewswire.com` (news releases not disallowed), `www.bankofamerica.com` (/philanthropic not disallowed) and `projects.propublica.org` (/nonprofits/organizations not disallowed). All were read.
- `gt990datalake-rawdata.s3.amazonaws.com` and `bofa.donorfirst.org` returned 404 for robots.txt, so they have no rules. As in earlier waves, I fetched from them.
- I made no request to `apps.irs.gov`. The 2026-11-18 IRS index and the `2026_TEOS_XML_10A` zip were therefore not re-read. The older `index_2025.csv` copy in the session was used instead.

For each claim I formed my own verdict first, from the primary source or by re-running the script in a scratch copy of the repository, and only then compared it with the documents.

## Headline

Of 43 claims, 33 are confirmed, 8 partially confirmed, 1 contradicted and 1 unverifiable.
- **The scripts reproduce.** Both re-runs are byte-identical:
  - the AI calibration script, re-run from scratch in 5 minutes 11 seconds;
  - the graph script, re-run offline from the pass's response cache.
  - The FY2025 refresh could not be re-run because the 2026-11-18 index is not in the session. Its outputs were recomputed from the CSVs and spot-checked in 11 primary XMLs.
- **All 21 AI studies resolve, and every effect size is stated fairly.**

**What holds independently:**
- **AI calibration.**
  - **Studies.** All 21 studies resolve: 14 DOIs through OpenAlex records and 5 arXiv /abs pages, plus the GOV.UK and Bank of England pages. The cited effects are stated fairly:
    - Brynjolfsson et al.: +14% (NBER) and +15% (QJE); handle time −3.8 min (−9%); 38% adherence.
    - Dell'Acqua et al.: 25.1% faster and 12.2% more tasks; 19% less likely to be correct outside the frontier.
    - Noy & Zhang: −40% time, +18% quality.
    - METR: +19% time, against a believed −20%.
    - DWP: 19 min/day. GDS: 26 min/day.
    - Bick et al.: 5.4% and 1.4% of hours. Humlum & Vestergaard: about 3%.
    - Eloundou et al.: 15% and 47–56% of tasks.
    - Legal RAG tools: 17–33% hallucination.
    - Bank of England / FCA: 2% fully autonomous.
  - **Model results.**
    - 0 modal-winner changes, in my own argmax over all 2,496 process comparisons.
    - Large-national value pool $1.18m → $445k (p25–p75 $145k–$1.06m); $202k under the field framing and $793k under the task framing.
    - Break-even 43% → 16.5%.
    - Implied saving 17.4% → 7.9%.
- **Graph consolidation.**
  - Counts: 1,110 rows → 1,059 consolidated edges; 51 rows merged in 44 groups; 8 self-loops; 1,051 live edges; 893 nodes.
  - Status counts and every listed degree reproduce. So do the red-team tallies of 41 confirmed, 16 weakened, 52 unverified leads and 0 contradicted.
  - CR3 45.5%, CR5 55.8% and HHI 830 reproduce.
  - Re-read live: NPact acquired DonorCentral NXT and FIMS from Blackbaud (PR Newswire, 2022-09-12).
  - Re-read live: the BofA Program Guidelines v3.2024 say "administered by Bank of America Private Bank" and do not name Ren. The portal still says "DFX powered by Ren".
  - Re-read live: BNY CGF's TY2024 XML records the decision of 2024-12-24 to stop operating the DAF program.
- **FY2025 refresh.**
  - Coverage: 974 sponsors, 68.04% of FY2024 corrected assets and 62.74% of grants; 24 of the top 50 (70.6%).
  - The DAFgiving360 → Fidelity line of $976,570,217 is in the XML.
  - Nine of the 10 Ren/Stellar FY2025 lines were read in the XML, and the 10 sum to $3,348,472.
  - The latest-return measure is 19 sponsors and $31.56bn; the any-year measure is 30 sponsors and $48.55bn.
  - Spot-checked in the IRS index: 8 of the 26 missing top-50 sponsors filed FY2024 in batches 11A–11D.
- **Coverage matrix.**
  - All 147 changed cells have pointers that resolve, and 30 of the 32 checked by hand address their item.
  - The 20 `ai` cells match `ai-coverage-20-entities-2026-11-19.csv` exactly.

**What needs correcting or qualifying:**
1. **The Ren-linked share is a floor, and its comparison with the 28% set is wrong (V31A-30, V31A-31).**
   - My own recompute reproduces 32.2% ($105.62bn, 54 sponsors) and 31.6% for 2024+ sources. On corrected FY2024 assets the figures are 32.2% ($103.96bn of $323.27bn) and 31.6%.
   - **Six sponsors with confirmed Ren edges were not matched by EIN.** Their own edges or 990s carry the EIN: Thrivent, T. Rowe Price Program, CF of Greater Memphis, JF of Greater Philadelphia, Greater Green Bay CF and Catholic Community Foundation (38-3941057).
   - Including them gives **60 sponsors, $107.71bn, 32.9%** (32.8% corrected), and 32.2% for 2024+ sources.
   - **The 28% was not "seven sponsors, $84.13bn".** V3-06 built $91.62bn from 18 sponsors, including ImpactAssets, T. Rowe Price, Thrivent, Stifel, Cleveland and the iPhi long tail.
   - Against those 18 sponsors, the confirmed tier:
     - adds 40 sponsors ($15.88bn): 11 on Part VII-B payee lines ($8.97bn) and 29 on tenant or portal-link observation ($6.91bn);
     - drops 4 ($1.88bn): two EIN misses and two moves to Give Interactive or Foundant.
   - NPT is still 39.9% of the tier, on hosting evidence.
2. **The re-review basis q = r·a (V31A-07).**
   - This basis is coherent for per-output error rates, which is the task framing.
   - In the field framing it also multiplies v2's *unsourced* QA range by a ≈ 0.37. That cuts the QA charge by about 60% without evidence. On v2's literal basis the field pool is $0.
   - The doc discloses this. The headline wording should carry it.
3. **The comparison count is 13 runs, not 12 (V31A-02).** 156 = 13 runs × 6 archetypes × 2. Three of the 13 runs are baselines compared with themselves.
4. **The coverage-matrix doc is stale against its CSV (V31A-42).** After the 20 `ai` cells were filled:
   - NI is 74, DS 37 and EC 110;
   - 322 cells (81.3%) are investigated;
   - only Candid is majority-NI.
   - The md and `coverage-summary-2026-11-19.json` still say 94 NI and 76.3%.
5. **Coverage judgement call (V31A-41).** DAFgiving360 `grant_workflow` IC rests only on the $50 minimum-grant row of V12-04. Under R2 that is PV.
6. **FY2025 primary gaps (V31A-33, V31A-39).** The 76 new 10A returns, including Kalamazoo → Give Interactive ($416,932), are not on the mirror or ProPublica yet, and I did not fetch the IRS zip. They are internally consistent but not independently re-read.
7. **Minor:**
   - In the FY2025 doc, EIN 58-1723645 is the CF of Greater Memphis and 23-1500085 the JF of Greater Philadelphia.
   - Greater Green Bay CF files a negative FY2025 DAF EOY value (−$5,666,175), which the doc does not flag.
   - The BofA technology edge's consolidated head (EA023) cites api.certspotter.com. It should cite E082, the portal.

## Rulings on the seven graph Find/Replace proposals

| # | Target | Ruling |
|---|---|---|
| FR1 | Industry report, graph size | **Accept, with qualifier.** Write "up to 893 nodes": some sponsors appear once with and once without an EIN. |
| FR2 | Industry report, status counts and red team | **Accept as proposed.** |
| FR3 | Industry report, Ren 28% | **Superseded.** Use the governing text below. It states the floor, the six EIN misses, the evidence mix and NPT's weight. |
| FR4 | vendor-dependency-concentration.md, 167 edges | **Accept.** |
| FR5 | vendor-dependency-concentration.md, degrees | **Accept.** The degrees reproduce. |
| FR6 | vendor-dependency-concentration.md, BofA administration | **Accept.** The PDF text was re-read 2026-11-19. |
| FR7 | vendor-dependency-concentration.md, Commonwealth Charitable Fund sponsor | **Accept.** EF001 (the CCF Program Circular) names RCF. |

## Limits

- **Not independently re-read:**
  - the 76 new FY2025 returns, because they are only in the 10A zip on apps.irs.gov;
  - the 2026-11-18 index;
  - Ayco's final return, which is TEOS-only.
- **The graph re-run used the pass's response cache.** It tests reproducibility, not the fetches. I redid four red-team checks live: PR Newswire, the BofA PDF, the BofA portal and the BNY XML.
- **The 21 studies were read at abstract or report level.** Full texts were read only for E01, E08 and E09 (NBER PDFs) and for E06 and E07 (GOV.UK HTML). Mapping studies to parameters is the author's inference and was judged, not re-derived.
- **Coverage spot-check:** 32 of the 147 changed cells were read by hand. The rest were checked only to confirm that their pointers resolve.

## Exact corrections

### `research/mission-2026-11-14/gap19-ai-calibration.md`
1. **§1 item 1, comparison count.**
   - **Find:** "In 156 comparisons (12 scenario-model runs × 6 archetypes × gross and net), the most likely winner changes in **no process**. That covers v2 and both v2b pool variants."
   - **Replace with:** "In 156 comparisons (13 scenario-model runs, 3 of them the baselines themselves, × 6 archetypes × gross and net; 120 are non-trivial), the most likely winner changes in **no process**. That covers v2 and both v2b pool variants [V wave 31A]."
2. **§1 item 6, re-review basis.**
   - **Find:** "   - The central case charges review only to AI-handled cases. That is a modelling choice (§3.2). It is not a measurement."
   - **Replace with:** "   - The central case charges review only to AI-handled cases. That is a modelling choice (§3.2). It is not a measurement. In the field framing it also scales v2's unsourced QA range by a (≈0.37), cutting that charge by about 60% without new evidence. So the field-framing $202k, and half of the central $445k, depend on the basis as much as on the evidence [V wave 31A]."

### `research/mission-2026-11-14/gap19-graph-consolidation.md`
1. **§1, concentration bullet.**
   - **Find:** "**The Ren-linked asset share changes:** 32.2% ($105.62bn, 54 sponsors) on confirmed edges, against the report's 28% ($91.6bn). Restricted to sources dated 2024 or later it is 31.6%."
   - **Replace with:** "**The Ren-linked asset share changes:** 32.2% ($105.62bn, 54 sponsors) on confirmed edges, against the report's 28% ($91.6bn). Restricted to sources dated 2024 or later it is 31.6%. On corrected FY2024 assets the shares are the same (32.2%, $103.96bn of $323.27bn; 31.6%). These are floors. Six sponsors with confirmed Ren edges were not EIN-matched: Thrivent, T. Rowe Price Program, CF of Greater Memphis, JF of Greater Philadelphia, Greater Green Bay CF and Catholic Community Foundation (38-3941057). With them the share is 32.9% (60 sponsors, $107.71bn), or 32.2% on 2024+ sources [V wave 31A]."
2. **§4, comparison with the 28% set.**
   - **Find:** "- The report's **28% ($91.6bn)** was built from wave-3 evidence. The seven Ren sponsors that wave-3 text names (NPT, GS PWM DAF, GS Gives, AEF, MS GIFT, RCF, BofA CGF) hold $84.13bn here. The consolidated confirmed tier adds 47 more sponsors ($21.49bn), mostly from 990 payee harvests and iPhi/DFX tenant sweeps. The largest are NATL CHRISTIAN CHARITABLE FDN INC $5.46bn; IMPACTASSETSINC $3.63bn; Combined Jewish Philanthropies of Greater Boston Inc $1.93bn; RAYMOND JAMES CHARITABLE ENDOWMENT FUND $1.89bn; THE AYCO CHARITABLE FOUNDATION $1.38bn; THE US CHARITABLE GIFT TRUST $1.36bn."
   - **Replace with:** "- The report's **28% ($91.6bn)** was built from wave-3 evidence. V3-06 sums 18 sponsors to $91.62bn: RCF, MS GIFT, ImpactAssets, T. Rowe Price, Thrivent, WaterStone/CCF, GS Gives, Stifel, Cleveland, AEF, NPT, GS PWM, BofA and the iPhi long tail (Minneapolis, Arkansas, Gulf Coast 59-1052433, Stanislaus, Marion). Against that set, the confirmed tier adds 40 sponsors ($15.88bn) and drops 4 ($1.88bn).
     - **Added on Part VII-B payee lines (11, $8.97bn):** NCF $5.46bn, Ayco $1.38bn, US Charitable Gift Trust $1.36bn and others. Five of them rest on FY2022–23 lines only.
     - **Added on iPhi/DFX/DonorView tenant or portal-link observation (29, $6.91bn):** CJP $1.93bn, Raymond James $1.89bn, Saint Paul & Minnesota $0.58bn and others.
     - **Dropped:** Thrivent and T. Rowe Price (Ren edges confirmed but not EIN-matched), WaterStone/CCF (Ren now historical; Give Interactive live) and Gulf Coast CF of Venice (Ren historical; Foundant) [V wave 31A]."
3. **§7, status of the proposals.**
   - **Find:** "These are proposals only; neither document was edited."
   - **Replace with:** "These are proposals only; neither document was edited. Validation wave 31A accepts FR1 (as \"up to 893 nodes\"), FR2 and FR4–FR7, and supersedes FR3 with the governing text in validation-wave31a-report.md [V wave 31A]."

### `research/mission-2026-11-14/gap19-fy2025-refresh.md`
1. **§4.2, unnamed payer (Memphis).**
   - **Find:** "  - Community Foundation (EIN 58-1723645): $203,119."
   - **Replace with:** "  - Community Foundation of Greater Memphis (EIN 58-1723645): $203,119, Stellar Technology Solutions LLC, \"software\" [V wave 31A]."
2. **§4.2, unnamed payer (Philadelphia).**
   - **Find:** "  - Jewish Federation of Greater … (EIN 23-1500085): $500,842, Renaissance Administration."
   - **Replace with:** "  - Jewish Federation of Greater Philadelphia (EIN 23-1500085): $500,842, Renaissance Administration [V wave 31A]."
3. **§4.3, Kalamazoo provenance.**
   - **Find:** "\"TECHNOLOGY/SOFTWARE CONSULTATION\", $416,932, CY2025."
   - **Replace with:** "\"TECHNOLOGY/SOFTWARE CONSULTATION\", $416,932, CY2025 (read from the TEOS 10A zip; on 2026-11-19 the return was not yet on the GivingTuesday mirror or ProPublica, so it has not been independently re-read [V wave 31A])."
4. **§6, suspect filed values.**
   - **Find:** "  - Armstrong County CF, which files $10.3m against a FY2024 corrected value of $148.2m (already flagged in the full-universe report)."
   - **Replace with:** "  - Armstrong County CF, which files $10.3m against a FY2024 corrected value of $148.2m (already flagged in the full-universe report).
  - Greater Green Bay CF, which files a negative FY2025 DAF year-end value (−$5,666,175; object 202513179349310111) [V wave 31A]."

### `research/mission-2026-11-14/coverage-matrix-rebuild-2026-11-19.md`
1. **§1, investigated row.**
   - **Find:** "| Cells investigated (status other than NI) | 248 (62.6%) | 302 (76.3%) |"
   - **Replace with:** "| Cells investigated (status other than NI) | 248 (62.6%) | 302 (76.3%); **322 (81.3%)** after the 20 `ai` cells were filled (P-G02-01) [V wave 31A] |"
2. **§1, NI row.**
   - **Find:** "| Not investigated (NI) | 148 | 94 |"
   - **Replace with:** "| Not investigated (NI) | 148 | 94; **74** after P-G02-01 |"
3. **§1, DS row.**
   - **Find:** "| Discovery started (DS) | 58 | 30 |"
   - **Replace with:** "| Discovery started (DS) | 58 | 30; **37** after P-G02-01 |"
4. **§1, EC row.**
   - **Find:** "| Evidence collected (EC) | 113 | 97 |"
   - **Replace with:** "| Evidence collected (EC) | 113 | 97; **110** after P-G02-01 |"
5. **§1, majority-NI entities.**
   - **Find:** "- After (5): Candid / IRS BMF, OneAscent, Pave, SEI, TIAA."
   - **Replace with:** "- After (5): Candid / IRS BMF, OneAscent, Pave, SEI, TIAA. After the 20 `ai` cells were filled (P-G02-01), only Candid / IRS BMF is majority-NI; OneAscent, Pave, SEI and TIAA have 6 NI cells of 12. Segment shares investigated after P-G02-01:
     - national 97.2%;
     - independent 95.0%;
     - technology vendors 84.4%;
     - digital 83.3%;
     - wealth 71.4%;
     - payments 70.8%;
     - community 69.4%.
     PV-or-better shares are unchanged, because the `ai` cells are EC or DS [V wave 31A]."
6. **NI by item, `ai` row.**
   - **Find:** "| ai | 25 | 20 |"
   - **Replace with:** "| ai | 25 | 20 (0 after P-G02-01: 13 EC, 7 DS) |"
7. **§4 heading.**
   - **Find:** "## 4. Cells still Not investigated (94), by entity"
   - **Replace with:** "## 4. Cells still Not investigated (94 before P-G02-01; 74 after, with every `ai` entry below now filled), by entity"
8. **§4 patterns, `ai` bullet.**
   - **Find:** "- `ai` is the largest remaining gap: 20 of 33 entities. P-G02-01 proposes a cheap public check for it."
   - **Replace with:** "- `ai` was the largest remaining gap (20 of 33 entities). P-G02-01 has since filled all 20 cells from `ai-coverage-20-entities-2026-11-19.csv` (13 EC, mostly documented absence; 7 DS). `custody_invest` (13) is now the largest NI item [V wave 31A]."
9. **§2, judgement calls.**
   - **Find:** "- **JCF.** Only rows for JCF New York (EIN 23-7174183) were used."
   - **Replace with:** "- **DAFgiving360 `grant_workflow` (PV → IC)** rests only on the $50 minimum-grant row of V12-04, a narrow part of the item. Under R2 it would stay PV [V wave 31A].
- **JCF.** Only rows for JCF New York (EIN 23-7174183) were used."

### `research/mission-2026-11-14/strategic-synthesis.md`
1. **Ren dependency evidence (finding on Ren).**
   - **Find:** "sponsors holding about **28%** of FY2024 DAF assets ($91.6bn of $327.9bn) use Ren technology in some form **[V wave 3]**. Only 18 sponsors holding $30.18bn (**9.2%**) name Ren or Stellar in their latest 990"
   - **Replace with:** "sponsors holding about **28%** of FY2024 DAF assets ($91.6bn of $327.9bn) use Ren technology in some form **[V wave 3]**. The consolidated graph of 2026-11-19 puts the share with any confirmed Ren technology, administration or payment link at about **32–33%** (32.2%, $105.6bn, 54 sponsors, as a floor; 32.9% with six sponsors whose EIN was missed). The rise comes from breadth: 40 added sponsors, $15.9bn, mostly small iPhi tenants plus NCF, CJP, Raymond James and the US Charitable Gift Trust. NPT, at 12.8% of the market, still rests on hosting evidence [V wave 31A]. Only 18 sponsors holding $30.18bn (**9.2%**) name Ren or Stellar in their latest 990 (19 and $31.56bn after the FY2025 refresh, the addition being Ayco's final return)"
2. **Operations-AI value pool (finding #10).**
   - **Find:** "10. **The operations-AI value pool is thin** (was #10). Revocation hits are 0.082% of top-50 grant dollars (wave 26)."
   - **Replace with:** "10. **The operations-AI value pool is thin** (was #10). Calibrating s, q and a to 21 published studies (2021+) cuts v2's large-national AI value about 60%: $1.18m → $445k, with $202k under field evidence and $793k under task experiments. The shared-platform break-even falls from 43% to 16% of draws. No process changes its most likely winner. v2's implied 17% labour saving sits above every field measurement (3–5% of hours; 9–13% per case in customer support). The $445k assumes re-review is charged only on AI-handled cases, a modelling choice; on v2's all-touched basis it is $110k ([gap19-ai-calibration.md](gap19-ai-calibration.md); wave 31A). Revocation hits are 0.082% of top-50 grant dollars (wave 26)."

### `research/DAF-INDUSTRY-REPORT-2026-11.md`
1. **§4 vendor bullet, Ren-linked share (replaces graph proposal FR3).**
   - **Find:** "- On public evidence, sponsors holding about **28%** of FY2024 DAF assets ($91.6bn of $327.9bn) use Ren technology in some form **[V wave 3]**."
   - **Replace with:** "- On public evidence, sponsors holding about **28%** of FY2024 DAF assets ($91.6bn of $327.9bn) use Ren technology in some form **[V wave 3]**. The consolidated relationship graph (2026-11-19) puts the share of FY2024 DAF assets at sponsors with any confirmed Ren/Stellar technology, administration or payment link at **32.2%** ($105.6bn, 54 sponsors), or 31.6% when the evidence is dated 2024 or later. This is a floor: six sponsors with confirmed Ren edges were not EIN-matched, and with them the share is 32.9%. The same shares hold on corrected FY2024 assets. The rise from 28% is breadth: 40 added sponsors ($15.9bn), 29 of them on tenant or portal-link observation and 11 on Form 990 payee lines (5 of those FY2022–23 only). NPT (12.8% of the market, about 40% of the tier) still rests on hosting evidence [I]. The figure measures a public Ren link, not Ren as system of record (repo [`gap19-graph-consolidation.md`](mission-2026-11-14/gap19-graph-consolidation.md) §4; [V wave 31A])."
2. **Graph size (graph proposal FR1, accepted with qualifier).**
   - **Find:** "The relationship graph has 131 nodes and 167 edges, every edge sourced and status-labelled"
   - **Replace with:** "The consolidated relationship graph (2026-11-19) has up to 893 nodes and 1,051 edges, merged from the base file and 26 additions files (1,110 rows; 51 duplicates merged, 8 alias self-loops set aside), every edge sourced and status-labelled (repo [`relationship-graph-edges-consolidated-2026-11-19.csv`](../data/mission-2026-11-14/relationship-graph-edges-consolidated-2026-11-19.csv); [V wave 31A])"
3. **Status counts (graph proposal FR2, accepted).**
   - **Find:** "134 confirmed (one more after red-team), 17 historically confirmed, 11 inferred, 5 unknown. A red-team sample of 15 \"confirmed\" edges found 0 status errors and 2 scope imprecisions"
   - **Replace with:** "958 confirmed, 23 historically confirmed, 47 inferred, 11 unknown, 5 reported, 3 probable, 2 unverified lead, 1 pending, 1 rejected. A wave-2B red-team sample of 15 \"confirmed\" base edges found 0 status errors and 2 scope imprecisions. A 2026-11-19 red team of all 109 inferred, unknown, reported, probable, pending, vendor-claim and crt.sh-sourced edges (one independent public check each) marked 41 confirmed, 16 weakened, 52 unverified leads and 0 contradicted (repo [`gap19-graph-consolidation.md`](mission-2026-11-14/gap19-graph-consolidation.md); [V wave 31A])"
4. **AI economics v2, platform break-even.**
   - **Find:** "- A shared AI platform breaks even in 43% of draws with the five largest nationals in the network, and in 0.4% with community foundations under $250m alone."
   - **Replace with:** "- A shared AI platform breaks even in 43% of draws with the five largest nationals in the network, and in 0.4% with community foundations under $250m alone. Calibrated to 21 published studies (2021+), the 43% falls to 16% and the large-national AI value pool to $445k from $1.18m ($202k on field evidence, $793k on task experiments). No process changes its most likely winner. The calibrated figure assumes re-review only on AI-handled cases; on v2's all-touched basis the pool is $110k (repo [`gap19-ai-calibration.md`](mission-2026-11-14/gap19-ai-calibration.md); [V wave 31A])."
5. **New subsection after §11.27.** Add "### 11.28 Thoroughness pass part A (validated, wave 31A)", containing the paragraph below. If §11.28 is already taken, use the next free number.

   > **Thoroughness pass part A (validated, wave 31A).**
   > - **AI economics calibrated to published evidence (21 sources, 2021+, all resolving).**
   >   - **Field studies:**
   >     - customer support +14–15% resolutions per hour, −9% handle time;
   >     - whole-job savings 3–5.4% of hours;
   >     - UK civil service 19 min/day against a comparison group (26 min/day self-reported);
   >     - experienced developers 19% slower.
   >   - **Experiments:** consulting tasks 25% faster, writing −40%.
   >   - **Errors:** legal RAG hallucination 17–33%. Only 2% of UK financial-firm AI use cases are fully autonomous.
   >   - **Model results:**
   >     - The ranking of redesign, conventional automation, manual fixes and AI-on-workflow is unchanged in every process.
   >     - The large-national AI value pool falls about 60%, from $1.18m to $445k ($202k–$793k across framings).
   >     - v2's implied 17% labour saving becomes 7.9%.
   >     - Shared-platform break-even falls from 43% to 16% of draws.
   >   - The re-review basis (AI-handled cases only) is a modelling choice. On v2's all-touched basis the pool is $110k.
   > - **Relationship graph consolidated (27 files, 1,110 rows → 1,051 live edges, up to 893 nodes; reproduced exactly).**
   >   - Red team of 109 weaker edges: 41 confirmed, 16 weakened, 52 unverified, 0 contradicted.
   >   - The DonorCentral edges belong to NPact, not Blackbaud (acquired 2022-09-12).
   >   - BofA's guidelines name Bank of America Private Bank as administrator, with Ren as technology vendor. BNY Mellon CGF's iPhi tenant is historical (program ended 2024-12-24).
   >   - Sponsor-asset CR3 45.5%, CR5 55.8% and HHI 830 are unchanged.
   >   - The Ren-linked share is 32.2% as a floor (32.9% with six EIN-unmatched sponsors; 31.6% on 2024+ evidence). It is up from 28% through breadth, not new evidence on the largest sponsors.
   > - **FY2025 filing refresh (index of 2026-11-18).**
   >   - 76 new returns bring coverage to 974 sponsors and 68.0% of FY2024 corrected assets. The top 50 are unchanged at 24 filed, and 26 remain unindexed.
   >   - Covered-filer DAF-to-DAF netting is $3.05–3.80bn (7.1% central), a lower bound. One DAFgiving360 → Fidelity line of $976.6m is 29% of it.
   >   - No Ren attrition is visible: 10 FY2025 Ren payers ($3.35m), and all 8 comparable FY2024 payers name Ren again.
   >   - Kalamazoo CF pays Give Interactive $416,932. This is not yet independently re-read.
   > - **Coverage matrix rebuilt (396 cells).**
   >   - PV-or-better rises from 14.4% to 37.4%.
   >   - Investigated cells rise from 62.6% to 81.3% after the 20 `ai` cells were filled, most as documented absence.
   >   - Every changed cell has a resolving pointer.

## Data-file notes (not .md; for the owning agent)

- **`coverage-summary-2026-11-19.json`:** regenerate it from the current matrix CSV. It still reports 94 NI, 30 DS, 97 EC and 76.3%, against 74, 37, 110 and 81.3% in the CSV.
- **`relationship-graph-edges-consolidated-2026-11-19.csv`:**
  - **EIN resolution.** Add EINs to the resolver for Thrivent Charitable (41-1802412), T. Rowe Price Program (31-1709466), JF of Greater Philadelphia (23-1500085), Greater Green Bay CF (39-1699966), CF of Greater Memphis (58-1723645) and Catholic Community Foundation (38-3941057). The 990-derived EC-series edges already carry these EINs in their evidence text.
  - **E088 (gccf.donorfirstx.com).** Check which Gulf Coast CF the edge belongs to (57-0908490 or 59-1052433).
  - **BofA technology edge.** Prefer E082 (bofa.donorfirst.org) over EA023 (api.certspotter.com) as head.
  - **Certspotter-sourced edges.** Classify these edges with the crt.sh-sourced class.
- **`coverage-matrix-entities-2026-11-19.csv`:** consider PV for DAFgiving360 `grant_workflow` (only the V12-04 minimum-grant row). V12-04 has 7 rows under one claim id, so pointers to it are ambiguous; P-G02-02 would fix this.
- **`ai-process-economics-calibrated-2026-11-19.csv`:** no value changes.
- **FY2025 refresh files:** no value changes. When P-G01-01 re-runs, re-read the 76 10A returns from the mirror once they are posted.
