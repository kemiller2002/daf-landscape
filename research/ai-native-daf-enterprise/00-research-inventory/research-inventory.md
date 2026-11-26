# Research inventory: existing DAF evidence for the AI-native enterprise design

**Date:** 2026-11-20. **Branch:** `claude/ai-native-daf-architecture-lsfr4y`. **Status:** audit of existing repository research; no new primary research.
**Companion registers:** [`evidence-register.csv`](evidence-register.csv) (EV-001 … EV-156) and [`gap-register.csv`](gap-register.csv) (GAP-001 … GAP-040). Downstream design documents cite those IDs.

**Labels used here.**
- **[V]** independently validated in a `validation-register*.csv` wave; **[V wNN]** names the wave where the governing text says so.
- **[VC]** vendor or company claim, not independently verified.
- **[I]** inference (the repo's or this inventory's). **[S]** scenario/model output, not an estimate of any firm's cost.
- **[A]** absence finding (searched, not found; not proof of absence).
- **[X]** contradicted or superseded.
- Confidence follows the repo's Low → High scale.

**Governing rule applied.** Where documents conflict, this inventory uses, in order: (1) `research/mission-2026-11-14/strategic-synthesis.md` §0 (2026-11-19); (2) the "Validation corrections … governing" appendices and §11.28–§11.79 of `research/DAF-INDUSTRY-REPORT-2026-11.md`; (3) governing appendices of the cited workstream files; (4) earlier body text. Where an earlier figure is superseded, both are listed in §6 (Contradictions).

---

## 1. Scope and method

### 1.1 What was read

| Layer | Files | How read |
|---|---|---|
| Governing synthesis | `research/mission-2026-11-14/strategic-synthesis.md` §0, §A | Full §0; §A table |
| Consolidated report | `research/DAF-INDUSTRY-REPORT-2026-11.md` §1–§9, §11.1–§11.79, all "Validation corrections" appendices | Full, URLs stripped for reading |
| Mission status | `research/mission-2026-11-14/FINAL-STATUS.md` | Governing counts table (PR #74), contradictions, open questions, owner decisions |
| Failures and history | `failed-daf-startups-deep-research.md`, `gap19-startup-cohort.md`, `competitive-history-timelines.md`, `private-equity-daf-ecosystem-map.md` (via report §11.6), `research/historical-daf-sponsor-technology-lifecycle-2011-2026.md` | Summaries, pattern sections, governing corrections |
| Operating cost | `sponsor-cost-structure-and-sensitivities.md` (via §11.1), `direction-sponsor-executive-compensation.md` (via §0 and §11.25), `b51-04-sponsor-operating-efficiency.md`, `b45n33-long-tail-operating-cost.md`, `b51-03-grant-size-distribution.md` | Bottom-line tables and results |
| AI | `ai-economics-replacement-analysis.md`, `ai-economics-v2-observed-costs.md` (via §11.5 and its governing notes), `gap19-ai-calibration.md`, `g0401-*`, `g0403-*` (via §0 and §11.40–§11.59), `ai-governance-failure-modes.md`, `ai-native-entrant-simulation.md`, `direction-ai-product-census.md` | Executive findings, governing red-team corrections |
| Exceptions | `gap19-exception-load-proxy.md`, `g0503-0501-exception-proxy-refinements.md` (via §0) | §0 answers and regeneration note |
| Commercial agenda | `research/commercial-opportunity/2026-11-20-research-agenda.md` | Full |
| Standard | `standards/daf-grant-record/schema-v0.1.json`, report §11.54 | Schema keys and required fields |
| Queue | `data/mission-2026-11-14/research-priority-queue.csv` | Parsed by script |
| Other prior-repo files | `batch-2a-charity-vetting-grant-approval-2026-11-12.md`, `ren-instant-grant-approval-rcf-policy-clarity-audit-2026-11-12.md` | Targeted grep only |

Not read in full: the ~300 individual queue/batch/direction workstream files. Their validated content enters through the report's §11 and the synthesis §0, which is the repo's own consolidation path. Where a number below is attributed to a workstream file, it was read in that file or in the report paragraph that cites it.

### 1.2 Counts computed by command (2026-11-20)

```bash
cd /home/user/daf-landscape
git ls-files research | grep -c '\.md$'                # 412 tracked research docs = 81 top-level + 326 mission + 4 mission archive + 1 commercial agenda (FINAL-STATUS governing table: 410 at PR #74; the commercial agenda landed after it; the remaining 1-file difference is not explained here)
find research -name '*.md' -not -path '*ai-native-daf-enterprise*' | wc -l   # 412 (same set; excludes this workstream's new, untracked files)
find data -name '*.csv' | wc -l                        # 765 (FINAL-STATUS: 764 at PR #74)
ls research/*.md | wc -l                               # 81 prior-repo top-level research docs
ls research/mission-2026-11-14/*.md | wc -l            # 326 (plus 4 in mission-2026-11-14/archive/)
wc -l research/DAF-INDUSTRY-REPORT-2026-11.md          # 1,511 lines
python3 - <<'EOF'
import csv, collections, glob
q = list(csv.DictReader(open('data/mission-2026-11-14/research-priority-queue.csv')))
print(len(q), collections.Counter(r['state'] for r in q))
# 1087 {'open': 517, 'done': 436, 'blocked': 78, 'monitoring': 50, 'deprioritized_historical': 5, 'declined': 1}
files = glob.glob('data/**/validation-register*.csv', recursive=True)
rows = [r for f in files for r in csv.DictReader(open(f))]
print(len(files), len(rows))   # 86 files, 2,557 rows
EOF
```

Validation results by leading word of the result column (same script): confirmed 1,853 (+7 "confirmed with caveat(s)"), partially_confirmed 466 + "partially" 94 + "partly" 2, contradicted 92, unverifiable 28 + unable_to_verify 3, other 12. FINAL-STATUS's governing classification is 1,861 confirmed, 562 partially confirmed, 92 contradicted, 31 unverifiable, 11 other; the small differences come from how compound result words are binned, not from different rows.

Open/blocked queue items by area (top): Market sizing 47, Data quality 44, Regulation 40, Payment rails 20, Market structure 19, AI economics 17, Nonprofit experience 15, Recipient economics 14, AI governance 12, Operations 11, Data rights 8.

### 1.3 Method limits carried from the repo
- **All evidence is public-source.** No vendor tests, sponsor interviews, executed contracts or sponsor operating data were obtained (FINAL-STATUS, limits). This is the single largest constraint on the enterprise design: every operating-cost and exception-load number below is a filing-based proxy or a scenario.
- **Validation is same-model-family cross-agent checking**, not cross-executor reproducibility (FINAL-STATUS).
- **Robots and terms.** The owner lifted the site-terms restriction on 2026-11-20; robots.txt and the no-bypass rule still apply. Several hosts remain blocked (regulations.gov 403; dafgiving360.org robots; secure.ncfgiving.com; foundant.com; Every.org bot challenge). Wayback content could not be fetched; only availability was confirmed.
- **Coverage matrix** is a purposive set of 33 entities, not the ~1,500-sponsor universe.

---

## 2. Evidence inventory by theme

Each theme lists key findings with numbers exactly as the governing text states them, the files, the evidence state and confidence. EV IDs point into `evidence-register.csv`.

### 2.1 Market size and structure

| Finding | State | Conf. | EV | Source |
|---|---|---|---|---|
| DAFRC FY2024: assets $327.87bn (FY2020→24 CAGR 18.1%), contributions $90.57bn, grants $64.60bn, 3.59m reported accounts, ~1,500 sponsors (1,512 reported; about 803 community foundations) | [V] | High | EV-001–EV-004 | report §1 |
| Corrected FY2024 (filed Schedule D replaces imputations): $323.27bn assets (−1.40%), accounts 7.8% lower; corrected top 50 $276.27bn | [V w34A] | High | EV-005 | report §1, §11.34 |
| 79.5% of accounts in 22 donation-processor sponsors holding 0.9% of assets; Givinga's 1,421,011 accounts average $1.37 | [V] | High | EV-006, EV-007 | report §1, §11.1 |
| Ongoing-advisory basis (AOGF reclassification): 2.59m accounts FY2024; 0.79m without Givinga and PayPal Giving Fund; processor-free series 770,785 (not 786,822) | [V w33B/w40A] | High | EV-008 | §0 A; report §11.16, §11.51 |
| Traditional invested accounts ≤ 737k (upper bound) | [V] | Medium | EV-009 | report §1 |
| Concentration: sponsor-asset CR3 45.5%, CR5 55.8%, HHI 830 (national sponsors only: CR3 63.2%, HHI ≈1,566); league-table CR5 51.0% → 56.9% FY2021–24 while grant CR5 53.6% → 46.6% | [V] | High | EV-010, EV-011 | §0 A; report §1, §11.26 |
| Fidelity holds 20.5–21.7% of corrected assets FY2021–24; NPT ($42.12bn) passed DAFgiving360 ($40.94bn) in FY2024; top 50 hold 83–86% of assets | [V w29] | High | EV-012 | report §11.26 |
| Long tail: 1,240 of 1,514 sponsors under $50m hold $9.18bn, 2.84% of assets; median tail sponsor 24 DAFs averaging $133k (top 50: 1,464 and $836k) | [V w30] | High | EV-013 | report §11.27 |
| Payout: FY2024 aggregate 25.9%, 22.8% net of DAF-to-DAF, 12.7% at median sponsor ≥$1m; DAFRC account-sample median three-year payout 9% (15% excl. inactive), 22% of accounts made no grants 2020–22 | [V w23/w24B] | Medium-High | EV-014, EV-015 | §0 A; report §1, §11.18 |
| DAF-to-DAF netting (rule R5 central): $8.03bn removed FY2024; netted grants $58.41bn; FY2025 covered-filer netting $3.05–3.80bn (lower bound) | [V w19/w31A] | Medium-High | EV-016 | report §11.14, §11.29 |
| Netted FY2024 DAF grants equal 9.9% of Giving USA CY2024 total and 14.9% of individual giving | [V w25B] | Medium | EV-017 | report §11.21 |
| DAF share of recipient contributions: central 8.8% of line 1h (CI 7.9–9.7%) and 13.6% of 1h − 1d − 1e (sampling CI only) | [V w47A] | Medium | EV-018 | §0 notable; report §11.69 |
| Sponsor mortality: verified exit rate 0.19–1.48%/yr by count, ~0.2% by assets; in every confirmed closure assets moved to another sponsor | [V] | Medium | EV-019 | report §11.6 |
| International: direct foreign grants $1.89bn of $98.27bn (1.92%) top 50 FY2023–24; money measured as reaching abroad 5.20% of top-50 grants | [V w30/w38A] | Medium | EV-020 | report §11.27, §11.45 |
| CFs keep 60.0% of US grant dollars in-state vs 7.6% for nationals (median CF 83.0% in a 95-CF sample) | [V w27/w36A] | Medium-High | EV-021 | §0 E; report §11.39 |
| Corporate DAFs 3.9% of grants (2024) and 3.4% (2025) on Fidelity+SVCF; no 990 splits corporate from individual | [V w36A] | Medium | EV-022 | report §11.39 |
| Institutional (university/school/health) sponsors hold $3.59bn, 1.11% of corrected assets (FY2024) | [V w50B] | Medium | — | report §11.76 |

Files: `regulation-market-structure-portability.md`, `full-universe-990-harvest-and-corrected-totals.md`, `queue-batch36-metrics-rails.md`, `queue-batch38-data-followups.md`, `queue-batch34-netting-filings.md`, `direction-league-table-concentration.md`, `direction-long-tail-sponsors.md`, `sponsor-mortality-analysis.md`, `b40n1202-04-recipient-census.md`.

**Design reading [I].** The serviceable market is ~0.77–0.79m advisory accounts and ~$320bn, heavily concentrated in ~50 sponsors. Per-account economics must be modelled without processor accounts. Payout headline numbers are definitional; a design that reports payout must state its formula.

### 2.2 Sponsors

| Sponsor | Key evidence | State | EV |
|---|---|---|---|
| **Fidelity Charitable** | FMR provides recordkeeping, systems and administration; 990 shows $0 IT and no employees; pays FMR affiliates amounts equal to donors' admin fees; 67% of grants by EFT (2026 Giving Report); EFT not required; 2,664,446 grants CY2024 to 213,000 unique nonprofits (12.5 each); average grant $5,801 (2025); CIAP 46.9% of investments (June 2025); default disclosure 80% full contact / 15% fund name / 5% anonymous (2025); 0.60% first $500k; $50 grant minimum | [V] | EV-023–EV-027, EV-059 |
| **NPT** | #2 by FY2024 assets ($42.12bn); U.S. DAF program granted $6.44bn FY2025 ($6.61bn release likely includes U.K.); FY2024 grant count 129,575 (governing); mean grant $73,866 (FY21) → $40,381 (FY25); pays by PayPal Grant Payments (up to $250k) or wire, no ACH; GivingPoint is a 13-site Ren white-label book on hosting evidence only; only top-10 sponsor documenting donor export (Excel); 2026 terms ban robot harvesting and using site data to develop AI; $250 grant minimum | [V]; Ren link [I] | EV-028–EV-031 |
| **DAFgiving360 (Schwab)** | 194 employees, 1,100,000 grants FY2024 (5,670 grants/employee); 0.60% first $500k; 1.00% adviser-fee cap; check-only per 2024 policies; 38% of grants recurring (FY2025); $976.6m FY2025 grant line to Fidelity unexplained; robots-blocked | [V] | EV-032, EV-033 |
| **Vanguard Charitable** | 119 employees, 221,825 grants FY2024; average grant $14,808 (CY2025, 267,838 grants); PayPal Grant Payments up to $10m; no adviser-managed option; $25,000 minimum; related-party service fee $4.24m FY2026; selected Give Interactive for recordkeeping per Give's release only [VC]; User Agreement treats outside services using donor login as "Unauthorized Third Party" | [V]; Give scope [VC] | EV-034–EV-036 |
| **AEF** | Ren-administered; moved to Ren platform 2026; new portal shows two years of history; implied average adviser fee 0.46%; 149 employees, 109,708 grants (CY2024 derived) | [V] | EV-037 |
| **Greater Horizons (GKCCF)** | Runs donor-portal.org back office for other CFs; related-organisation pay 90%; publishes pool returns vs benchmarks (identical to GKCCF); FY2024 $212.2m blank Schedule I totals row (data artefact) | [V] | — |
| **Community foundations** | Admin fees median 100/100/67 bps at $100k/$1m/$10m (1.7x/2.2x/3.6–4.7x nationals); staff cost 78.7 bps of DAF assets; Foundant CommunitySuite at 361 of 803 (45%), 32.7% of mapped CF DAF assets; Foundant serves 282 of 351 tail CFs with identified vendor; all six dated portal switches ended on Foundant; consolidation 2021–26 small | [V] | EV-038–EV-041 |
| **Faith sponsors** | Church-status recipients with no e-filed 990 take 8.3% of top-50 DAF dollars; faith sponsors send ~30% (30.2%) of block dollars all-panel; JCF median grant $750 (FY2023), 23 employees / 89,485 grants; none of 14 congregation pages showed a DAF option | [V w35C/w42B] | EV-042, EV-043 |
| **RCF** | Pays Ren 98% of individual-fundholder admin-fee revenue ($19.23m FY2024); 0.65% with $250 min; ~11 wealth-firm programs on RCF + Ren; 2023 policy: Charity Check adequate for >98% of historical grants (risk-mitigation coverage, not auto-approval) | [V] | EV-044, EV-045 |

Files: `queue-npt-givingpoint-fidelity-stack.md`, `b51-04-sponsor-operating-efficiency.md`, `b51-03-grant-size-distribution.md`, `b44n28-01-donor-info-defaults.md`, `b4013-02-b4222-02-remittance-and-portal-features.md`, `direction-cf-consolidation-fees.md`, `queue-cf-vendor-map.md`, `b4026-06-church-daf-recipients.md`, `ren-instant-grant-approval-rcf-policy-clarity-audit-2026-11-12.md`.

### 2.3 Infrastructure providers

| Provider | Key evidence | State | EV |
|---|---|---|---|
| **Ren / iPhi / Stellar** | Confirmed-link floor 32.2% of FY2024 DAF assets ($105.6bn, 54 sponsors; 32.9% with six EIN-unmatched); 9.6% at 19 sponsors naming Ren in latest 990 (incl. Ayco's final return); named receipts $44.98m floor TY2024, 85.8% from three customers; revenue not public; claims of ">60%", "about half", "$200bn" unsupported; SOC 2 described as Type 2 (Jul 2025) and Type 1 (Apr 2026, and Bain 2023); iPhi lost 6 of 57 sponsors 2023–Nov 2026 (10.5%; Wilson 4.9–21.1%); FY2025 filings show no attrition yet; Rapid Disbursement Engine uses sponsors' own bank rails | [V]; claims [VC] | EV-046–EV-050 |
| **TIFIN Give / GiveClear** | GiveClear sponsor, TIFIN platform; SEI Charitable Fund since 2026-10-28; Chariot disburses; Louise "executes real donor requests" with 8 of 10 controls undocumented; GiveClear reviews grants within 48 hours; adviser-fee cap 1.00%; acquired Amicus.io | [V]; Louise [VC] | EV-051, EV-089 |
| **Chariot** | Disbursements on Column N.A.; Daffy, TIFIN, Charityvest (transitioning from Aug 2026), Founders Pledge, Groundswell, 7 CFs; DAFpay 2.9% default to nonprofits; best documented agent-confirmation pattern but no human-vs-agent field; one Form D ($10,999,978, 2024); "nearly 13%" DAF share claim vs 10.0% size-matched | [V]; share [VC] | EV-052–EV-054 |
| **Foundation Source / Charityvest / Vennfi** | GTCR-owned since 2023; acquired Vennfi (2024), Giving Place (2025), PG Calc, Pacific Foundation Services; Charityvest President paid by Foundation Source ($163,944 via Vennfi, 2024); Charityvest fees "zero" (2020) → 0.45% cap (2022) → 0.60% first $500k (2026); 48,744 grants (2025, company); Audax first-lien S+5.00% due 2030 | [V] | EV-055, EV-056 |
| **Give Interactive** | Controlled 99% by The Signatry's trust; nine known clients $36.74bn on DNS evidence, $23.90bn on first-party/filing evidence; lost three CF tenants (not five); Vanguard mandate rests on Give's own release | [V]; Vanguard [VC] | EV-057 |
| **Foundant** | CommunitySuite claims 700+ [VC]; mapped at 361 CFs; 282 of 351 tail CFs; SmartSimple AI Application Analysis is a Foundant-wide service (provisional GREEN) | [V] | EV-040 |
| **Daffy** | $2bn assets company-reported (Sept 2026) vs $334.19m FY2024 990 net assets; $0–40/month memberships; all-in 0.26% at $250k; MCP `make_donation` with no documented limit; 5 of 5 announcements delivered; complaint rate 11.2 per 10,000 accounts (venue coverage) | [V]/[VC] | EV-058, EV-088 |
| **Endaoment** | Partner API tiers (Growth setup $0–25k + $2k–5k/month; Strategic $25k–100k + $5k–15k/month); 1,213 DAFs FY2025 (best-evidenced; 6,000 FY2024 outlier); crypto 99.7% of FY6/24 contributions; partner grant call needs only API key | [V] | EV-060, EV-061 |
| **Givinga** | Single-sponsor platform; 1,421,011 accounts at $1.37 average; account unit undefined | [V] | EV-007 |
| **Blackbaud** | REPAY embedded rail; BILL named successor 2026-09-29; 2020 breach: SEC $3m, 49 states+DC $49.5m, FTC order, California $6.75m | [V] | EV-062 |
| **Bonterra** | Que agentic platform (2025-10-01); bought Deed 2026-03-05; 2032 loan marked 97.7–99.5% | [V] | — |
| **PayPal Grant Payments** | NPT (up to $250k), Vanguard (up to $10m); PayPal Giving Fund may remove charity and reassign funds | [V] | EV-063 |
| **Every.org** | Files 990-PF CY2020–24, reclassified as public charity; $0.1–0.3m donor credit; "giving credit" from IRA QCDs raises classification question; site blocked by bot challenge | [V] | — |
| **Goodstack** | US reported 3 DAFs FY2025, down from 7,268 | [V] | — |
| **Payment rails overall** | Four camps; only observed switch Charityvest PayPal→Chariot (in transition); top-30 CFs: 10 own ACH, 2 named third party, 2 checks only, 15 nothing published | [V] | EV-064, EV-065 |

Files: `gap19-graph-consolidation.md`, `queue-batch37-vendor-economics-owners.md`, `queue-ren-iphi-attrition.md`, `crtsh-resourcing-2026-11-19.md`, `competitive-history-timelines.md`, `queue-agentic-controls-and-sponsor-audits.md`, `queue-bank-programs-and-eft-providers.md`, `queue-community-foundation-rails-portals.md`.

### 2.4 Economics and fees

| Finding | State | Conf. | EV |
|---|---|---|---|
| 0.60% first-tier admin fee is a near-convention (Fidelity, DAFgiving360, Charityvest); RCF 0.65% ($250 min); BofA 0.90% flat; Daffy $0–40/month | [V] | High | EV-066 |
| All-in cost at $250k: Daffy 0.26%, Vanguard 0.62%, Fidelity 1.15%, DAFgiving360 1.25%, NCF 1.45%, San Francisco Foundation 2.13%; pool choice as large a lever as sponsor choice (Fidelity 60%-equity pool 0.55%, index 0.015%) | [V w10] | Medium | EV-067 |
| Adviser fees: only MS GIFT, DAFgiving360, TIFIN Give publish a 1.00% cap (MS GIFT's excludes legacy pools and UMA manager fees); Fidelity CIAP, NPT, AEF, RCF publish none; observed RIA brochures 0–2.00% | [V w33B] | Medium-High | EV-068 |
| CF median admin fee 100/100/67 bps vs nationals 60/45/14–19 bps (37 schedules, 46% of top-100 CF DAF assets) | [V w31B] | Medium | EV-069 |
| Tail CF schedules: pooled medians 137.5/137.5/125 bps at $25k/$100k/$500k (n=20); tail price premium no longer established; realised CF fee pool $49.4m, list ceiling $83.9m–$138m | [V w44B/w42A] | Medium | EV-070 |
| Program-service revenue $0 at all 15 affiliated sponsors (the DAF fee is an internal transfer); Fidelity passes its fee to its administrator one-for-one, RCF 98%, JCF keeps 20–33% | [V w29/w38B] | High | EV-071 |
| Fidelity active asset-allocation pools trail benchmarks by ~0.58–0.76 pp over 5 years, matching the admin fee; index menus track within ~0.1 pp | [V w27]; cause [I] | Medium | EV-072 |
| Sponsor marketing (990 line 12) tiny: affiliated $21.7m (1.39 bps of contributions), Schwab $20.3m; CFs $67.2m (~18 bps); parent-paid marketing off-990 | [V w28/w40C] | Medium | EV-073 |
| Nonprofit cost to receive a $1,000 grant: ~$1–2 free EFT, ~$5–8 check, ~$32 on DAFpay at 2.9% default; sponsors charge nonprofits $0 except Benevity (2.99%, cap $500), DAFpay (2.9%), ForGood (1.5%) | [V w12] | Medium | EV-074 |
| Altruist/Endaoment adviser DAF at 50 bps vs cited 60–65 bps "typical" | press [VC] | Low-Medium | — |
| DAF vs direct gift tax: identical for itemizers; DAF loses for non-itemizers from 2026 (excluded from $1,000/$2,000 deduction); 0.5%-AGI floor, 35% cap | [V w27] | Medium-High | EV-075 |

Files: `queue-all-in-cost-dafpay-access.md`, `queue-adviser-fees-pools-npact.md`, `direction-cf-consolidation-fees.md`, `b4501-04-tail-fee-pool-revision.md`, `b4427b-0405-realised-tail-fees-all.md`, `direction-sponsor-financial-resilience.md`, `direction-investment-menus-performance.md`, `direction-sponsor-marketing-spend.md`, `queue-nonprofit-side-panel.md`, `direction-donor-tax-scenarios-2026.md`.

### 2.5 Operations: grant workflow, exceptions, eligibility, payment rails, reconciliation

| Finding | State | Conf. | EV |
|---|---|---|---|
| **No sponsor publishes** grant turnaround P50/P90, exception rates, reviewer minutes, an SLA or rail latency distribution; only 5 of 28 published turnaround statements are measured, all vendor figures | [A] | High | EV-076 |
| Published policy latencies: Vanguard most grants within 2 business days, new-charity diligence 2–10 business days; DAFgiving360 checks mailed 7–10 business days + USPS 7–10; AEF 5–10 business days; one sponsor 10+ business days | [V prior-repo batch 2A] | Medium | EV-077 |
| Measured latency (vendor): Charityvest 95% of checks deposited within 35 days; AssetMark median 2 days overall, 0 electronic; Chariot one-nonprofit sample: check providers 7–162 days, fastest ACH 1–2 days | [VC] | Low-Medium | EV-078 |
| Exception proxy (top-50, FY2023–24, governing): core 7.76% of lines / 11.61% of dollars (EIN-keyed fiscal sponsors, time-correct rulings); 6.80% / 11.00% true new orgs only; broad 24.79% / 19.85%. Measures recipients, not review | [V w39C] | Medium | EV-079 |
| Four-national like-for-like non-standard share ~4.2% of dollars (3.9% without four large-programme hosts); earlier "2.5–3%" (FY6/2025) | [V w39C] | Medium | EV-080 |
| Per grant at Fidelity, NPT, Vanguard: core ~7–8.5% of grants (2.8–7.9% if no unitemised recipient flagged); broad 17–31% depends on grants-per-recipient assumption; JCF size bands imply β 0–0.3 and broad per-grant share near 28–31% | [V w36B/w51A]; [C/I] | Low-Medium | EV-081 |
| Grants to EINs under revocation 0.082% of top-50 Schedule I dollars ($74.8m); $818.7m to EINs on neither IRS list, ~half not found by name/state | [V w26/w36B] | Medium-High | EV-082 |
| Grant-time rating eligibility: 72.66% of top-50 FY2023–24 DAF dollars went to CN-rating-eligible recipients | [V w47B] | Medium | — |
| Grant size: ~97% of grants under $50k (JCF); grants ≥$1m are 0.07–0.10% of grants but lines ≥$1m carry ~two-thirds of itemised dollars; median Schedule I line $18,650; grants per line 7–33 | [V w51A] | Medium-High | EV-083 |
| Average grant: Fidelity $5,801 (2025); Vanguard $14,808 (2025); NPT mean $40,381 (FY25); MS GIFT $11,000 (2024); JCF median $750 / average $11,639 (FY2023); DAFgiving360 median $500 [S]; Daffy median $100 | [V]/[F] | Medium-High | EV-084 |
| Payment rails: Fidelity 67% EFT (2026 report), EFT not required; NPT/Vanguard PayPal; BofA and DAFgiving360 check-only per policies; Seattle Foundation ACH mandatory from 2026-06-30; void window 90 days where published | [V] | High | EV-085 |
| Remittance: no public page for eight readable top-10 sponsors states an ACH SEC code or grant ID in addenda; every documented route carries grant detail out of band (email, dashboard, portal, letter) | [V w39A] | Medium-High | EV-086 |
| Purpose text: 98.2% of 322,773 FY2024 Schedule I lines carry boilerplate/sector/aggregate/blank; 1.2% name a specific use; Fidelity files one string on all 80,308 lines | [V w35A] | High | EV-087 |
| Reconciliation: no public measure of reconciliation break rates or servicing contact volumes anywhere | [A] | High | — (GAP-005) |
| Grant voids/refunds itemised by ≥17% of top-200 sponsors (median ~0.3% of grants), reflecting presentation, not incidence | [V w14] | Low | — |

Files: `gap19-exception-load-proxy.md`, `g0503-0501-exception-proxy-refinements.md`, `g0401-g0502-ai-routing-and-per-grant.md`, `b51-03-grant-size-distribution.md`, `b4013-02-b4222-02-remittance-and-portal-features.md`, `queue-batch36-metrics-rails.md`, `direction-recipient-compliance-screen.md`, `b40n13-01-grant-purpose-panel.md`, `batch-2a-charity-vetting-grant-approval-2026-11-12.md`.

### 2.6 Regulation and litigation

| Finding | State | Conf. | EV |
|---|---|---|---|
| §4966: 20% on sponsor, 5% (cap $10k) on knowing manager; §4967: 125% on donor/adviser, 10% on knowing manager; §4958(c)(2) automatic excess benefit; listed public-charity grants excepted, reliance on IRS listings permitted | statute [V] | High | EV-090 |
| 2023 proposed regs (REG-142338-07) neither final nor withdrawn; docket 249 submissions; 2026–27 PGP reframes as §§4966/6033 guidance on "certain DAF arrangements"; 2026 Unified Agenda lists final rule as not significant with a July 2026 target that has passed; §4967 project left the plan | [V w24A/w33B/w45A] | High | EV-091 |
| Proposed rule would treat a donor's personal investment adviser managing DAF assets as a donor-advisor | [V] | Medium-High | EV-092 |
| OBBBA: DAF gifts excluded from non-itemizer deduction; 0.5%-AGI floor and 35% cap from 2026; corporate 1% floor for tax years after 2025 | [V] | High | EV-075 |
| No state 2021–2026 DAF payout, reporting or donor-intent mandate (51 jurisdictions; Connecticut unchecked); CA AB 488 / Hawaii Act 205 treat a sponsor as a platform only if it names charities to non-advisers; CA platform law reaches DAF tech vendors on its text (white-label portal = Type E) | [V w25A/w32B/w15] | Medium | EV-093, EV-094 |
| Notice 2017-73 §4 still governs pledge payments ("may rely … until additional guidance") | [V w33B] | High | EV-095 |
| Litigation: Pinkert (no standing), Fairbairn (judgment for Fidelity), Keefer (strict compliance); Peterson v. WaterStone pending in discovery, final productions due 2027-02-14; Georgia AG suing SDG Impact Fund | [V w14/w50A] | High | EV-096 |
| Discretion beyond tax exposure: 2026 SPLC holds by Fidelity, Vanguard, DAFgiving360 (CA AG release); 16-AG letter 2026-05-21 | [V RT] | High | EV-097 |
| Money transmission: FinCEN payment-processor exemption conditions; grants not obviously "purchases of goods or services" → holding funds needs counsel | [I] on statute | Medium | EV-098 |
| Fundraiser bond removed by not holding funds only in some states (CT, NJ, OH, GA, IL in 18-state sample; MN, NH, RI, LA per 2023 survey) | [V w14] | Medium | EV-099 |
| Canada 3.5%/5% quota, C$16.6bn; Australia 6% decided (not registered at 2026-11-19); UK none | [V w24A/w37B] | Medium | — |
| No DAF-specific SEC/FINRA rule; SEC withdrew predictive-analytics proposal 2025-06-12 | [V] | Medium | — |
| Candid API licence: no retention carve-out vs Rev. Proc. 2018-32 §8.01(2) retention requirement; written consent needed for data mining "for use in artificial intelligence"; CN bars ratings "in any other calculation" | [V w9/w14/w44A] | Medium-High | EV-100 |
| IRS exam coverage 0.12%–0.30% of e-filed 990/990-EZ; ≤15 returns/yr report sponsor §4966 tax; no OFAC penalty 2021–26 names a charity | [V w39B] | Medium | EV-101 |

Files: `direction-policy-lobbying-obbba.md`, `b41n16-b42n20-daf-tax-guidance.md`, `b39n1-01-docket-2026-submissions.md`, `gap19-state-law-50-state-check.md`, `direction-state-daf-law-tracker.md`, `queue-batch29-regulation-litigation-crypto.md`, `b50-01-daf-litigation.md`, `queue-sponsor-terms-data-clauses.md`, `b43n26-03-charity-data-terms-ai.md`, `g0403-0104-m-detection-ofac.md`.

### 2.7 AI / agentic products and AI economics

| Finding | State | Conf. | EV |
|---|---|---|---|
| Census of 30 products (22 vendors): none meets RED test; only TIFIN Louise and Daffy MCP can move DAF money, both end in sponsor review; 3 provisional GREEN (SmartSimple, Fluxx Finn, YourCause), none an A1–A5 provider | [V w28/w42A] | Medium | EV-088, EV-089 |
| First-party read of 13 of 20 entities (7 blocked): none documents AI in grant approval, eligibility or money movement | [A] [V w33B] | Medium | EV-102 |
| AI in 29.1% of vendor job postings (44 of 151) vs 13.3% of sponsor postings (2 of 15) | [V w33B] | Low-Medium | EV-103 |
| Pledge partner MCP `create_donation` with no documented confirmation, cap or cancel — RED (provisional) pending second scorer | [V w48A] provisional | Low | EV-104 |
| Agentic contracts: no public contract at Daffy, TIFIN/GiveClear, Endaoment or Chariot treats an AI agent as a distinct actor; all allocate loss to donor/customer; no donor contract admits a software service as delegate | [V] | Medium | EV-105 |
| Inference ~$0.45 per heavy review vs ~$83 reviewer time | [V] [S] | Medium | EV-106 |
| Calibrated large-national AI value pool $445k ($202k–$793k across framings; $110k all-touched); $1bn CF $69k; $250m CF $18k; $10–100m CF $2.4k; implied labour saving 7.9% | [V w31A] [S] | Low-Medium | EV-107 |
| Shared-platform break-even 16% of draws (CFs alone 3.6%); homogeneous large-national network needs median 17 sponsors, only 5 exist | [V w31A] [S] | Low-Medium | EV-108 |
| Routing confident cases to AI alone: pool $1.06–1.36m if escaped error costs 1–5 handling-times; m bounded 1.0–88.5, central 2.20 → 1.56–1.77 with detection data; ~128 if sanctions miss priced per alert; assistance modal nowhere | [V w36B–w42C] [S] | Low | EV-109 |
| Field evidence: support +14–15% resolutions/hour; whole-job savings 3–5.4% of hours; legal RAG hallucination 17–33%; 2% of UK financial-firm AI use cases fully autonomous | [V w31A] | Medium | EV-110 |
| $120k/yr AI product cannot be funded from process savings below ~$1bn DAF assets; one AI project exceeds IT line of a $250m CF in 67% of draws; median CF IT $17k–$116k | [S]/[I] | Low-Medium | EV-111 |
| Grant-review-only labour pool ~$16k/yr at a 48,744-grant sponsor and ~$975k/yr at Fidelity scale; S3 at $120k needs ~76k–369k grants/yr | [S] | Low | EV-112 |
| Governance: unconstrained AI creates risk in 13 of 16 failure modes (rubric, not incidents); flag-only rule | [S]/[I] | Medium | EV-113 |
| Fidelity donor survey: 93% rate AI transparency important; 39.8% uneasy about data use | [VC] survey | Low-Medium | EV-114 |

Files: `direction-ai-product-census.md`, `gap19-ai-coverage-20-entities.md`, `direction-news-hiring-signals.md`, `b43n26-03-0304-pledge-mcp-cn-ai.md`, `queue-agentic-controls-and-sponsor-audits.md`, `queue-batch36-agent-terms-controls.md`, `ai-economics-replacement-analysis.md`, `ai-economics-v2-observed-costs.md`, `gap19-ai-calibration.md`, `g0401-g0502-ai-routing-and-per-grant.md`, `g0403-04-escaped-error-cost.md`, `g0403-0104-m-detection-ofac.md`, `g0403-0105-04-routing-realization-and-correlation.md`, `ai-governance-failure-modes.md`.

### 2.8 Failures, exits, acquisitions and private equity
See §10 for the structural reading. Key numbers: 50 purposive cases (12 acquisitions, 11 voluntary shutdowns, 6 regulator/insolvency events, 5 pivots) [V]; donor money lost only where one operator held unsegregated funds (Ammado ~€3.8M; Flipcause >$29M owed to >3,200 orgs; SDG Impact Fund alleged) [V; causes unadjudicated]; 18-entrant 2021–26 cohort: 10 active, 1 acquired, 1 pivoted, 6 unknown, 0 shut [V w32A]; six of six documented DAF-tech exits went to Ren, Foundation Source or TIFIN [V]; Giving Block earnout max $246m → $10.4m settled [V w14]. EV-115–EV-120.

### 2.9 Donor, adviser and nonprofit experience

| Finding | State | Conf. | EV |
|---|---|---|---|
| Portability: none of 12 sponsors publishes outbound transfer policy; transfers cash after liquidation, 10 business days–4 weeks; no history portability (AEF migration kept two years); none of top 10 publishes donor machine-readable export (NPT Excel the one documented exception) | [V w8/w23] | Medium-High | EV-121 |
| Terms: six of top 20 (~$84bn) contractually limit automated/third-party access; NCF bans credential sharing and scraping; NPT bans using data to develop AI; Vanguard "Unauthorized Third Party"; Endaoment bars sharing API credentials | [V w9/w19] | Medium-High | EV-122 |
| Public vendor templates allow batch export but not live integration (iPhi 15-day export window; NPact §2.4 bars third-party transaction access) | [V w4] | Medium | EV-123 |
| Donor contact defaults at FY2024 top 20: full contact documented for 33.2% of assets, withholding 17.2%, undocumented 44.6%; DAFRC survey: 36% of sponsors default to full contact | [V w34A] | Medium | EV-124 |
| Complaints: 244 records; app login/crash, grant delays, sponsor discretion, receipts; Fidelity 1.32 per 10,000 accounts; rates measure venue coverage not quality | [V w32B] | Medium | EV-125 |
| Donate pages: any DAF option on 41.2% of top donate pages (lower bound; 43.4% incl. one-step); DAFpay 13.7% | [V w26] | Medium | EV-126 |
| Nonprofit identity/data issues lead nonprofit complaints (16 of 48); only 49% of donors say always thanked | [V w29] | Medium | — |
| Accessibility: critical WCAG failures on 7 of 37 pages (NPT, Vanguard, SVCF, NCF); no readable top-20 sponsor publishes a response-time promise or chat channel | [V w25A] | Medium | EV-127 |
| Fraud controls: notices + MFA at 52.0% of top-20 assets (strict login MFA 35.2%), bank-change checks 29.8%; no DOJ release 2021–26 describes a DAF diversion | [V w49B] | Medium | EV-128 |
| Advisers: 35% recommend DAFs most or all of the time (DAFRC 2026, n=669); public knowledge 17–19% know how DAFs work | [V] | Medium | — |
| Fidelity app 24 iOS ratings vs Daffy 560 (2026-11-15); 267 of 476 feature cells unassessed | [V w27] | Low | — |

### 2.10 Data standards (`standards/daf-grant-record`)
- Draft, **unendorsed** "Minimal open DAF grant record, v0.1", JSON Schema 2020-12, 13 properties, 9 required (`schema_version`, `grant_id`, `fund_id`, `recipient`, `amount`, `purpose`, `anonymity`, `status`, `dates`); optional `sponsor_id`, `restriction_text`, `payment_reference`, `external_ids`. Validated with jsonschema 4.26.0 against 24 vectors; Chariot cents and Endaoment USDC micro-units normalise to decimal strings [V w41A]. EV-129.
- No open multi-sponsor grant-request standard exists; DAF Direct is closed with 3 listed sponsors (one, BNY Mellon CGF, ended its DAF program Dec 2024); Chariot DAFpay guide is the de facto vendor spec, carrying Chariot's correlation ID; IRS Schedule I requires only recipient EIN, annual amount and free-text purpose above $5,000; federal Grants Data Standards v3.0 (2026-06-17) is the closest US template; §1033 rule enjoined [V w25B/w40A]. EV-130.
- Files: `b4013-03-02-daf-grant-record-schema.md`, `direction-data-standards-interoperability.md`, `b40n13-03-g1913-03-schema-and-processor-accounts.md`, `validation-wave41a-report.md`.

---

## 3. Verified facts vs vendor claims

| # | Topic | Vendor / company claim [VC] | Verified or best public evidence | EV |
|---|---|---|---|---|
| 1 | Ren share of DAF assets | ">60%", "about half / $175bn+", "$200bn" | 32.2% confirmed-link floor; 9.6% latest-990 payees; ~5% Ren-paid administration; "$200bn" includes non-DAF assets [V] | EV-046 |
| 2 | Ren SOC 2 | "Type 2" (Jul 2025), "Type 1" (Apr 2026; Bain 2023) | No report seen; no trust page; none of 13 vendors publishes a scoped SOC report [V] | EV-049 |
| 3 | Ren charity network | 140k (2023), 93k in network (2026), ">1 million charities annually" (2026) | Drift only; no denominator [V as drift] | — |
| 4 | Ren instant approval | "over half" of grants approved instantly | RCF policy: Charity Check adequate for >98% of historical grants = risk-mitigation coverage, not auto-approval share; officer review above $500k [V prior repo] | EV-045 |
| 5 | Give Interactive at Vanguard | Vanguard selected Give for recordkeeping (Give release) | Not in Vanguard FY2026 audit; go-live unobserved [V absence] | EV-057 |
| 6 | Give Interactive scale | "$40B+" | $36.74bn on DNS evidence; $23.90bn on first-party/filing evidence [V w31B] | EV-057 |
| 7 | Daffy AUM | $2bn (Sept 2026) | FY2024 990 net assets $334.19m [V] | EV-058 |
| 8 | Charityvest 2025 | Record 2025 results, 48,744 grants | Company-reported; not comparable to 990 series [V] | EV-055 |
| 9 | Chariot DAF share | DAFs "nearly 13%" of giving (12.6% derived) | Size-matched central 10.0% (8.2–12.1%) [V w44A] | EV-054 |
| 10 | Chariot on Fidelity | Fidelity electronic-only by July 2026 | Not confirmed; Fidelity "transitioning", 67% EFT, EFT not required [V] | EV-085 |
| 11 | Chariot "1,200+ DAF providers" | Vendor figure | Unattributed; DAFRC counts 1,512 sponsors [V RT] | — |
| 12 | DAFpay reach | 70+ platform partners | Claimed; credential-free path named only for DAFgiving360 and Foundant CFs [V w10] | EV-053 |
| 13 | Foundant | CommunitySuite 700+ CFs | 361 of 803 CFs mapped (45%) [V w9] | EV-040 |
| 14 | Fidelity EFT speed | EFT "up to 9x faster" | Marketing claim; no measured latency published [VC] | EV-076 |
| 15 | Fidelity grant share via EFT | "67% of our grants are distributed via EFT" | First-party, validated [V w4]; two report EFT counts do not reconcile with shares [V w21] | EV-085 |
| 16 | Charityvest check latency | 95% of checks deposited within 35 days | Vendor-measured only [VC] | EV-078 |
| 17 | AssetMark latency | Median 2 days, 0 days electronic | Vendor-measured only [VC] | EV-078 |
| 18 | TIFIN Louise | "Execute real donor requests" | Vendor evidence only; 8 of 10 controls undocumented [V as absence] | EV-089 |
| 19 | Daffy MCP | `make_donation` "moves real money" | Docs confirm; no per-donation limit or confirmation documented [V] | EV-088 |
| 20 | NPT anonymity | "79% partially anonymous" | Not supported by DAFRC data [V w29] | — |
| 21 | NPT–Ren | (no claim by either) | Hosting evidence only; no second source; Ren not among NPT's five FY2025 contractors [V absence] | EV-030 |
| 22 | Giving Block volume | "over $300 million since 2018" | 22,343 × $11,019 = $246.2m conflicts [V w41A] | — |
| 23 | FreeWill Impact Fund | 55,000 organisations | Paid at least 263 (0.48–1.79%) [V w41A] | — |
| 24 | Dechomai fees | Published 1–3% | Fee/admin outflows 0.39–0.62% of intake; charged fee not measurable [V w37B] | — |
| 25 | Endaoment DAF count | 6,000 DAFs FY6/24 | 1,213 FY2025 best-evidenced; FY2024 round number the outlier [V w16] | EV-061 |
| 26 | Goodstack DAFs | 7,268 (earlier) | 3 DAFs FY2025 [V w15] | — |
| 27 | Foundation Source "DAF OS" / Ren daily unitization | Broad capability claims | Little public delivery evidence; missing evidence ≠ non-delivery [V] | EV-117 |
| 28 | Edward Jones | $2.9bn (2021) | Unverifiable (PDF 404) [V] | — |
| 29 | Ren AI / Givinga / FS AI products | Marketing of automation | None shipped; FS CEO roadmap tool framed as a flag for review [V w28] | EV-089 |
| 30 | Altruist/Endaoment | 60–65 bps "typical" adviser DAF | Press-cited comparison only [VC] | — |

---

## 4. Assumptions and hypotheses currently in the repo

### 4.1 Model assumptions (all [S] unless sourced)
- **AI economics v1/v2/calibrated:** process-handling share, AI amenability `a` (v1 capped 0.45), redesign share `d`, QA rate, fixed costs, manual-improvement α (still unsourced), escaped-error multiple `m` (central 1.77, range 1.0–88.5; ~128 on per-alert sanctions pricing), auto-close share `h` (upper half rests on a retrospective study and an agency self-report), realization factor r_C ~ tri(0.07, 0.33, 1.00) mapped from HUD/GSA RPA audits [I]. Seeds: v2 seed 42, 10,000 draws.
- **Exception unit economics (prior repo):** 3% exceptions, 25 minutes per exception, $65/hour, 40% time saved (`daf-grant-exception-unit-economics-evidence-and-sensitivity-2026-11-12.md`). Not reconciled with the economics doc's $55.45/h (red-team item 16 open).
- **Entrant simulation:** loaded cost per FTE $170k/$210k/$260k (not sourced); S3 revenue $36k/$120k/$240k per sponsor; S2 $0.50/$1.50/$3.00 per grant event; S1 $0.3m/$1.0m/$3.0m per sponsor. Capital to month 24: S1 $8.8m/$17.0m/$29.4m; S2 $3.2m/$6.6m/$12.4m; S3 $2.3m/$5.0m/$9.7m.
- **Grants per recipient line:** n_i = max(1, k·d_i^β), β swept 0–1; evidence now favours β 0–0.3 (P-B5103-01 open).
- **AI-economics v2 grant size input:** log-uniform $5–40k average, which the size data show is a two-tier mixture (P-B5103-04).
- **Netting rule R5** central tier with a 1,411-EIN reviewed whitelist; allocation rules A/G/AM/F for CF DAF cost.

### 4.2 Hypotheses stated in the repo
- H-ENT-1 (entrant simulation): an AI-native operating layer (S3) over existing sponsors, exception-only routing under deterministic sponsor rules plus continuous eligibility monitoring, is the cheapest probe — **conditional, not a recommendation** [RT].
- H-ENT-2: S3 must be scoped on the whole operating burden (reconciliation, servicing, payee data, year-end evidence, rule changes); none of these cost pools is publicly measured.
- H-ENT-3: AI economics clear governance cost only at vendor or network scale; the economic buyer is an administrator or platform, not a single sponsor [I].
- H-ENT-4: redesign removes exception classes; AI only shortens handling [I].
- H-FAIL-1: consolidator acquisition is the base-case exit; build to be acquirable [I].
- H-FAIL-2: consumer-direct CAC has not been shown viable for small startups (Daffy the unaudited counterexample) [I].
- H-DIST: fastest-growing sponsors are channel- or platform-led [I].
- H-NP: nonprofit identity and remittance data become more valuable; retained, dated eligibility evidence becomes more valuable [I].
- H-RES: "compete on resilience" — documented exit plan, sponsor-owned export, escrowed code, attested segregation [I].

### 4.3 Commercial-opportunity agenda (2026-11-20) — explicitly "research hypotheses, not validated demand"
- Buyer segments: (1) mid-sized sponsors and CFs; (2) wealth managers/RIAs/broker-dealers/family offices; (3) DAF tech and infrastructure vendors; (4) banks, trust companies, new entrants; (5) PE/VC/strategic acquirers; (6) nonprofits, universities, advancement teams; (7) education/credentialing organisations; (8) unexpected adjacent buyers.
- Offers to validate: independent technology audits and vendor comparisons; operating-model and workflow redesign incl. AI governance; market intelligence; investor due diligence; adviser-centric workflows; narrowly scoped operational software "where repeated customer evidence supports build"; training partnerships.
- DAFCP question: whether certification improves access, credibility, referrals or conversion vs practical expertise.
- Guardrails: public research is not proof of willingness to pay; no fabricated contacts, pricing, demand or capabilities; no unsolicited outreach without approval.
- **No evidence in the repo yet tests any of these** (no interviews, no pricing data, no named-prospect validation).

---

## 5. Decisions already made (governing for this workstream unless revisited)

| # | Decision | Source | Status |
|---|---|---|---|
| D1 | **AI may add a flag, never clear one.** Only humans or deterministic rules remove flags or approve | `ai-governance-failure-modes.md` §1, §5; synthesis §0 B | Governing |
| D2 | Routine-tier clearing by **deterministic, sponsor-approved rules only**; "model-assisted clearing" withdrawn | entrant simulation red-team item 11; FINAL-STATUS contradictions | Governing |
| D3 | **What not to build:** a sponsoring charity, custody, payment rails, charity master data, a full system-of-record; partner instead (sponsor-of-record APIs: Endaoment, Daffy for Developers; Chariot; custodians; IRS bulk data) | report §8; entrant sim §4 | Governing (S1 only via sponsor partner) |
| D4 | **Never hold donor funds**; contractually disclaim title to in-flight donations; check processor reserve terms | `failed-daf-startups-deep-research.md` §7 | Governing |
| D5 | Inbound DAF initiation (DAFpay-style) eliminated from scope | entrant sim §4 | Governing for S3 |
| D6 | Avoid credential-based integrations; do not wait for an open rail; avoid a standalone long-tail business; do not sell the DAF as tax-superior | synthesis §0 D | Governing |
| D7 | S3 is a **conditional research probe**, not a recommendation | entrant sim red-team item 10 | Governing |
| D8 | Minimum governance operating model (10 items): inventory/tiering; decision record standard (inputs, source snapshot IDs, policy version, model ID/version, prompt version, reviewer); asymmetric permissions; eval before deploy and on every model change; seeded known-bad cases; agent controls (scoped tokens, per-agent limits, mandatory donor confirmation, cancel window, agent identity); untrusted-content isolation; data minimisation/no-training; donor transparency; exit plan | `ai-governance-failure-modes.md` §5 | Recommended |
| D9 | Separate donor/agent recommendation from sponsor approval and from payment, each with identity, timestamp, limits | `ai-governance-failure-modes.md` §1.3 | Recommended |
| D10 | AI overlay method §7a–§7c: overlay confined to A1–A5 provider rows; a GREEN component never offsets an AMBER; "first GREEN" defined; none of 137 ratings qualifies | report §11.60 | Governing method |
| D11 | Owner decision 2026-11-20: site-terms restriction on automated reads lifted; robots.txt and no-bypass (CAPTCHAs, bot challenges, logins, forms) still apply | FINAL-STATUS | Governing |
| D12 | crt.sh/certspotter excluded (operator robots disallow API); crt.sh-only facts are unverified leads | report §11.28; compliance note | Governing |
| D13 | Privacy: individual donor names redacted (PF-flow CSV, 2026-11-20) | FINAL-STATUS | Governing |
| D14 | Reporting conventions: show account counts with and without processors; exclude SDG Impact Fund from totals; headline keeps filed values (NPT FY2023); NPT FY2024 grant count 129,575 governs; 990 ΔR1 "margin proxy" retired | report §11.1, §11.16, §11.34, §11.53, §11.79 | Governing |
| D15 | Scenario numbers labelled [S]; missing evidence is not treated as non-delivery; Clarity governs reasoning, EDF only where outcomes observed | synthesis method; report §5 | Governing |
| D16 | Technology acceptance test: a new provider should reconstruct at least five years of contributions, approved/denied grants, receipts, anonymisation preferences, balances and fees | `historical-daf-sponsor-technology-lifecycle-2011-2026.md` | Recommended |
| D17 | Open owner decisions still pending: Pledge AMBER vs RED; CZ Biohub LLC look-through; robots-blocked sources (NCF agreement, foundant.com, CCT portal) | FINAL-STATUS | Open |

---

## 6. Contradictions and superseded findings

A designer must use the right-hand column. "File" is where the governing correction lives.

| # | Earlier claim | Governing finding | File |
|---|---|---|---|
| C1 | Sponsor-asset CR3 ≈58%, HHI ≈1,289 | CR3 45.5%, HHI 830 (period mismatch inflated CR3 ~12 pts) | `red-team-wave2b-graph-data-incentives.md`; report §1 |
| C2 | Ren powers ">60%"/"over half" of DAF assets | 28% [V w3] → 32.2% confirmed-link floor; 9.6% latest-990 payees | `gap19-graph-consolidation.md` §4 |
| C3 | Bank of America 10-K evidences Ren | Contradicted; only the portal | report §2.2 |
| C4 | Fidelity electronic-only by July 2026 (Chariot) | Not confirmed; 67% EFT; EFT not required | report §2.5, §11.3 |
| C5 | Entrant model "model-assisted clearing" | Deterministic clearing only | entrant sim red-team 11 |
| C6 | "AI on existing workflow ranks last in 16/16 processes" | Assumption-determined; v2: C first in ≤17% of draws; calibrated P(C first) 0.002 at large national | `ai-economics-replacement-analysis.md` red-team; `gap19-ai-calibration.md` |
| C7 | Large-national AI pool $1.18m; platform break-even 43% | $445k; 16% | `gap19-ai-calibration.md`; report wave-31A correction 4 |
| C8 | Exception share "2.5–3%" at nationals | ~3.6% like-for-like FY2023–24 → ~4.2% EIN-keyed; core proxy 11.0% → 10.96% → 11.61% of dollars | `g0503-0501-exception-proxy-refinements.md` |
| C9 | Fiscal sponsors 10.7× count-to-dollar gap | 4.4× on EIN-keyed host list | same |
| C10 | Give Interactive lost five CF tenants; CT-discovered clients $9.81bn | Three tenants; $9.21bn | `crtsh-resourcing-2026-11-19.md` |
| C11 | 3.59m DAF accounts / 79.5% processors | Corrected 3.31m; 2.59m ongoing-advisory; 0.79m ex Givinga/PPGF; processor-free 770,785 not 786,822 | `queue-batch36-metrics-rails.md`; report §11.51 |
| C12 | "DAFs pay out ~25%" | 25.9% aggregate, 22.8% net, 12.7% median sponsor; 23.9% gross (pooled sample) equals NPT's figure only by coincidence | `queue-batch38-data-followups.md`; `b39n8-01-payout-definition-bridge.md` |
| C13 | Recipient DAF share "about 10%" scaled (and Chariot 12.6%) | 8.4% floor → 9.2% central → 8.8% census central; Chariot size-matched 10.0% | `b40n1202-04-recipient-census.md`; `b40n1202-b43n26-02-chariot-size-match.md` |
| C14 | Tail CF price premium (six-schedule median 150 bps) | Superseded: 137.5 bps pooled (n=20); premium not established | report §11.64 |
| C15 | Tail fee pool ~$138m | List-price ceiling; realised $49–74m | report §11.57 |
| C16 | Tail CF cost per DAF account $2,108 (15-CF web sample) | Rule F $4,500 per account (34 CFs), frame-wide ~$3.2k [I] | `b45n33-02-01-01-fund-totals-from-990.md` |
| C17 | "DAF startups fail often" | 18-entrant cohort: no documented shutdown | `gap19-startup-cohort.md` |
| C18 | "DAF is more tax-efficient than direct giving" | Identical for itemizers; worse for non-itemizers from 2026 | `direction-donor-tax-scenarios-2026.md` |
| C19 | Complaint rates show service quality | Venue coverage only; ranking flips with denominator | `gap19-complaints-with-denominators.md` |
| C20 | NPT FY2024 grant count 130,875 | 129,575 governs (FY25 series) | report §11.79 |
| C21 | NPT FY2025 grants $6.61bn | U.S. DAF program $6.44bn | report §4 |
| C22 | Sponsors withhold donor contact by default (survey) | Does not hold as a rule at nationals; RCF split depends on guide vintage (33.2%/17.2% vs 30.9%/19.5%) | `b44n28-01-donor-info-defaults.md`; `b4428-02-ren-private-label-defaults.md` |
| C23 | 990 ΔR1 as sponsor operating margin | Retired as a margin measure | report §11.53 |
| C24 | Escaped-error central m 2.20 | 1.56–1.77 with IRS detection data; ~128 on per-alert sanctions pricing | `g0403-0104-m-detection-ofac.md` |
| C25 | E15 miss rate 0.10 per auto-closed AML alert | At most 0.39% | `g0401-0103-ai-bd-recut.md` |
| C26 | Givebutter Magic provisional GREEN | AMBER (not flag-only; AI on by default) | report §11.57 |
| C27 | SVCF average grant $211,337 | About $106,000 (net of $1.667bn transfers to other sponsors) | report §11.71 |
| C28 | Fidelity cost per grant ~$68 | ~$59 ex CIAP/taxes; ~$71 period-matched; b51-04 opex per grant $61 (CY2024 count) | report §11.1; `b51-04` §3.5 |
| C29 | Scale elasticity 0.41 nationals / 0.84 CFs | b51-04: 0.49 nationals, 0.64 CFs (0.56 full universe); earlier figures bracket these | `b51-04-sponsor-operating-efficiency.md` |
| C30 | International share of DAF grants 7.8% | That is a recipient-sector share; money actually abroad 3.82% → 5.20% of top-50 grants | report §11.42, §11.45 |
| C31 | Edward Jones $2.9bn (2021) | Unverifiable | report §2.2 |
| C32 | Ren "instant approval" for over half of grants | RCF's >98% is Charity Check risk-coverage, not auto-approval | `ren-instant-grant-approval-rcf-policy-clarity-audit-2026-11-12.md` |

**Unreconciled inside the repo (designer beware):**
- Labour rate $65/h (prior-repo exception model) vs $55.45/h (AI economics) vs $38.87/h 990 median / $57–73/h at $250m+ sponsors / $86/h DAFgiving360 (`queue-pe-lenders-labour-rates.md`). Red-team item 16 asked for reconciliation; not done.
- Fidelity grant volume: entrant simulation uses 3.0m (CY2025); b51-04 uses 2,664,446 (CY2024). Different years, not an error, but models must state which.
- Cost per grant has two bases: total operating cost per grant (wave 5: Fidelity ~$68, DAFgiving360 $55, Vanguard $134, NPT $419) and b51-04 FY2024 opex per stated grant (Fidelity $61, DAFgiving360 $69, Vanguard $162, NPT $474). Both are whole-sponsor cost, not processing cost.
- Fidelity's EFT counts in two Giving Reports do not reconcile with the stated shares [V w21].

---

## 7. Research gaps (decision-critical)

Full list with retrieval paths in [`gap-register.csv`](gap-register.csv). The most decision-critical:

1. **Q-N03 — measured exception rate, reviewer minutes and QA rate at any sponsor** (queue state `blocked`: "needs sponsor time-and-motion access"). Every AI-economics and staffing conclusion depends on it. GAP-001.
2. **Q-N04 — executed sponsor–vendor contract with API/export terms** (queue `done` only on public templates; executed contracts unseen). Gates any operating-layer or migration design. GAP-002.
3. **Reconciliation, servicing and payee-maintenance cost pools** — not measured anywhere; S3's viability depends on them. GAP-005, GAP-006.
4. **Content of §§4966/6033 guidance on "certain DAF arrangements"** and the 13 unread 2026 docket letters (P-B39N101-01, top EIV in queue). GAP-008.
5. **Agent controls at Daffy MCP / TIFIN Louise / Pledge MCP** (Q-N05 `done` as absence: no limits documented). GAP-011.
6. **Money-transmission and state-solicitation posture of a non-custodial operator** (P-B30A-02 blocked; counsel needed). GAP-012, GAP-013.
7. **Human error-rate baseline and escaped-error cost** (m rests on unsourced terms). GAP-004.
8. **Grants-per-recipient function n(d)** (P-B5103-01) — drives per-grant exception share. GAP-003.
11. **Shadow-mode falsification test** of a deterministic-rules-plus-AI-flag workflow (≥10,000 grants, zero false clears on an audited sample). GAP-034.
12. **Sponsor-of-record partnership terms** for an entrant (Endaoment, Daffy for Developers, GiveClear, NPT private label). GAP-027.
9. **Willingness to pay and buyer evidence for the commercial agenda** — none. GAP-014.
10. **26 top-50 FY2025 returns not yet indexed** (P-MON19-03) — netting, concentration, Ren footprint. GAP-009.

---

## 8. Findings requiring revalidation (time-sensitive)

| Item | Why time-sensitive | Recheck trigger / date | Queue |
|---|---|---|---|
| FY2025 filings for 26 top-50 sponsors (incl. MS GIFT, RCF, US Charitable Gift Trust, NCF) | Netting, concentration, Ren attrition all re-run | Next TEOS batches (2026_TEOS_XML_11A onward) | P-MON19-03 |
| Chariot/Charityvest rail transition | Chariot dates it Aug 2026; Charityvest's guide still says PayPal | Monthly | watchlist |
| Fidelity EFT-only date / Stripe notice | Unconfirmed July 2026 date; archived FAQ unread | Monthly; Wayback access | P-B4013-02-02, P-FCG-01 |
| §§4966/6033 guidance; Unified Agenda July 2026 target passed | Could redefine adviser-managed DAFs and fund-manager duties | Federal Register; next Unified Agenda | P-B4142-01, P-B39N101-03 |
| Peterson v. WaterStone | Ruling on MTD; productions due 2027-02-14 | Docket | P-B5001-01 |
| Daffy MCP / Pledge MCP limits | No cap or confirmation documented; Pledge RED pending second scorer | Docs re-read; second scorer | P-B43N26-0304-01 |
| Give Interactive at Vanguard / ImpactAssets / others | Mandate rests on Give release; ImpactAssets DAF hub (2026-09-08) overdue | Quarterly log-in link read | P-G06-02 |
| Gulf Coast move off iPhi | "Launching soon" | Quarterly | — |
| Australia 6% minimum | Decided, not registered | legislation.gov.au | P-B39N3-07 |
| Benevity Alaya retirement | Scheduled 2026-12-15 | After date | — |
| Pushpay "DAF Attribution" | "Coming soon" | Monthly | P-B41N15-03 |
| Hiring AI-signal snapshot | One-time snapshot | Re-run on/after 2027-02-15 | P-B39N5-01 |
| Blackbaud REPAY → BILL | Named 2026-09-29, early adopters only | Quarterly | — |
| Vanguard–Altruist acquisition | Signed, not closed | Close | — |
| Ren "Giving Platform" donor-default guide | Default tracks guide vintage | Monthly hash | P-B442802-02 |
| Sponsor tax-page errors (Vanguard bunching, MS GIFT carryover) | Correction watch | 60 days | P-B4142-03 |
| NCF pool relaunch (2026-09-01) | Benchmark-only pro forma so far | Next performance report | — |
| Startup cohort unknowns (6) | Status unknown | When registries readable | P-GAP19-15-02 |

---

## 9. Unexplored opportunities relevant to an AI-native enterprise

Each was touched in the repo but not pursued to a design or a buyer test. All are [I].

1. **Cross-sponsor grant remittance and reconciliation for nonprofits.** S2 MVP in the entrant simulation; remittance always travels out of band (EV-086); no open standard; draft `daf-grant-record` v0.1 unendorsed. Never piloted or priced.
2. **Continuous eligibility monitoring with retained, dated evidence.** Rev. Proc. 2018-32 §8.01(2) requires retention; Candid's API licence lacks a retention carve-out (EV-100). An evidence-retention design that satisfies both is unexplored.
3. **Policy-as-code with back-testing against final §4966/6033 rules.** Proposed in entrant simulation §7.1; no prototype; Schedule I purpose text is 98.2% boilerplate, so purpose data must be captured at source.
4. **Size-tiered processing.** b51-03: per-grant automation is a small-grant count problem; risk review is a ~0.1%-of-grants mega-grant problem. Not built into any model (P-B5103-04).
5. **Congregations as recipients.** 8.3% of top-50 DAF dollars to church-status recipients without e-filed 990s; no DAF option on 14 congregation pages; church platforms lack DAF checkout except Overflow via Chariot. No design work.
6. **History portability / migration-as-a-service.** AEF kept two years; no sponsor commits to history portability; five-year acceptance test proposed. Unexplored as a product.
7. **Tail-CF shared services.** Median 66.7% of tail CFs recover less than rule-A DAF cost; Foundant holds the tail; CF staff cost 78.7 bps. A shared back office (Greater Horizons' donor-portal.org is the one observed instance) is not analysed.
8. **Agent-recommendation gateway.** No public contract treats an AI agent as an actor; Chariot's confirmation step is the best pattern but lacks a human-vs-agent field. A sponsor-side gateway (identity, limits, confirmation, cancel window) is specified only as governance principles.
9. **Measured service latency as a product feature.** Only 5 of 28 turnaround statements are measured; no sponsor publishes an SLA.
10. **Nonprofit identity/contact defaults.** 44.6% of top-20 assets have undocumented defaults; identity issues lead nonprofit complaints.
11. **Complex-asset intake (P03).** The one process where AI-on-workflow was competitive; Fidelity took $2.6bn of non-publicly-traded assets in 2025 (65 days to liquidity); Dechomai the main intermediary. No design.
12. **PF-to-DAF wind-down channel.** $9.43bn from 2,801 foundations to core nationals TY2022–24; wind-downs 7.9%. Not explored as a segment.
13. **Fraud and account-takeover controls.** Strict login MFA at 35.2% of top-20 assets; bank-change checks 29.8%. Not designed.
14. **Pledge-payment and matching-gift compliance.** Notice 2017-73 rule followed by AEF and NPT; universities split; matching-gift eligibility mostly undocumented. A rules service is unexplored.
15. **Succession/bequest defaults.** Terms vary (Fidelity 90-day unclaimed rule; NPT/Vanguard perpetual; SVCF three generations). Not designed.
16. **Accessibility and response-time commitments.** Critical WCAG failures at four top-20 sponsors; no response-time promise anywhere.
17. **Corporate DAFs and the 1% floor**, **giving circles** (~4,000 groups, $3.1bn 2017–23), **Canada/Australia quota compliance** — mapped, not pursued.
18. **DAFCP/education channel** (commercial agenda) — not researched.

---

## 10. Failed, exited and acquired companies: what they reveal structurally

Sources: `failed-daf-startups-deep-research.md` (50 cases), `gap19-startup-cohort.md` (18–25 entrants), `competitive-history-timelines.md` (195 events, 39 announcements), `private-equity-daf-ecosystem-map.md` (120 ownership rows, ~60 companies), `historical-daf-sponsor-technology-lifecycle-2011-2026.md` (24 events, 33 sources).

### 10.1 Case table (selected)

| Case | Event | Structural lesson | State |
|---|---|---|---|
| Ammado | 2018 court-ordered liquidation; ~€3.8M donations unaccounted | Single operator holding unsegregated funds | [V] facts; cause unadjudicated |
| Flipcause | CA AG enforcement Nov 2025; Chapter 7 conversion 2026; >$29M owed to >3,200 orgs; Stripe terminated processing and held a reserve ($1.45M per Flipcause filings; ~$790k at issue per Stripe) | Operator claimed title to donations; processor reserve frozen | [V w4 corrected] |
| SDG Impact Fund | Georgia SoS barred it as a charity (2026); AG seeking receiver; self-reported $10.1bn (FY2021–22) excluded from totals | Sponsor-governance failure; partner due diligence is first-order | [V] allegations |
| National Heritage Foundation | 2009 Chapter 11; 2011 revocation; FY2022 $0 assets, $3.84m to United Charitable | Sponsor insolvency ≠ vendor failure; trace fund-level transfers | [V] |
| Pinkaloo, Crown/DonorFirst, Stellar/iPhi | Acquired by Ren (2021, 2016, 2023) | Buyers pay for plumbing; product fate undisclosed | [V] |
| Amicus.io | $8.7M Series B (2020); acquired by TIFIN ~16 months later for "pipes" | Consumer-bank embedding pivoted into adviser platform | [V] |
| Vennfi, Giving Place | Acquired by Foundation Source (2024, 2025); Giving Place had two owners in 14 months | PE roll-up; Charityvest remained separate charity | [V] |
| The Giving Block | Shift4 earnout max $246m; $(47.1)M fair-value cut FY2022; settled $10.4m; ~12% staff cut | Crypto revenue is cyclical | [V] |
| Network for Good | Software into Bonterra; DAF nonprofit continued (now For Good, DCSO subsidiary since 2024) | Charity as separate legal entity protects funds | [V] |
| Google One Today, AmazonSmile, GoFundMe Charity, Virgin Money Giving, BT MyDonate | Closed 2019–23 for adoption/strategy | Borrowed channels are withdrawn | [V] |
| Swell, ioby, TakeCharge.io | Closed on scale (Swell ~$35M AUM; ioby >$21M lifetime) | Low take rates do not fund acquisition [I] | [V] facts |
| AEF DonorCentral sunset | Portal retired 2026-10-31; two years of history in new Ren portal | History loss is a migration habit | [V] |
| Uncommon Giving | Pivoted consumer DAF wallet → employer CSR suite | Channel pivot, not death | [V] |
| Causeway | Acquired by Charity Navigator 2023-08-22 | — | [V] |
| BNY Mellon CGF | DAF program ended 2024-12-24 | Bank sponsor exit; assets moved | [V] |
| Ayco Charitable Foundation | Merged into GS DAPF 2025-07-01; $1.16bn moved outside Schedule D grants | Intra-family consolidation distorts flow stats | [V] |
| Benevity Alaya | Retirement scheduled 2026-12-15 | Acquired products retire ~5 years later | [V] scheduled |

### 10.2 Structural patterns
1. **Money is lost in payments/custody, not in the DAF ledger** (P1; High observed). Every loss case had one operator controlling unsegregated donor funds. Design implication: non-custodial architecture, legal title disclaimers, processor-reserve diligence (D4).
2. **Consolidator acquisition is the modal DAF-tech exit** (P2; Medium-High): six of six documented exits went to Ren, Foundation Source or TIFIN; no acquirer disclosed codebase or migration outcomes. Consolidators are both competitors and likely buyers.
3. **PE ownership changes are followed by management change and acquisitions within ~0–6 months** (competitive history §4.3); customer effects (churn, pricing, service) are unobserved. No owner has steered its wealth platform to its own DAF vendor.
4. **Distribution dependence** (P3; Medium): startups pivot consumer → employer → bank/adviser; corporate parents withdraw giving products.
5. **Low take rates vs CAC** (P4; Low-Medium, mostly inference); challengers repriced upward (Charityvest, Daffy $40 tier).
6. **Regulatory/solicitation exposure for intermediaries is growing** (P5; Medium-High).
7. **Governance failure in mission-branded entities** (P7; Medium, 3–4 cases).
8. **Not supported:** that technology/code quality, AI, or proposed §4966 rules caused any exit.
9. **Survival of 2021–26 entrants is high but uninformative:** 12/12 resolved survive (Wilson 75.7–100%); 66.7–100% bounds over 18; annual shutdown hazard ≤3.7% (rule-of-three); at DAFRC's 1.2%/yr base rate, 0.28 exits expected — zero observed is not evidence of superior survival.
10. **Sponsors themselves cannot be acquired; they merge or affiliate under charity law**, and in every confirmed sponsor closure assets moved to another sponsor (mortality 0.19–1.48%/yr by count).
11. **Announced vs delivered:** of 39 tracked capabilities, 17 delivered, 11 partial, 9 no evidence, 2 contradicted; delivery quality differs by company, not size (Daffy 5/5; TIFIN 5/8).

---

## 11. Operating-structure observations relevant to org design

### 11.1 Staffing and cost evidence

Register rows: EV-039, EV-131–EV-143.

| Measure | Value | State | Source |
|---|---|---|---|
| DAF-allocated operating cost, all sponsors (latest 990s) | $2.1–2.8bn, 67–89 bps of DAF assets | [V w5] | `sponsor-cost-structure-and-sensitivities.md` |
| By type (earlier) | Standard nationals ~25–32 bps; CFs ~127–177 bps | [V] | same |
| FY2024 medians (b51-04) | Top-50 nationals 23 bps, $1,395 per DAF account; top-50 CFs 162 bps whole-org, 102 bps rule A, $12,036 per account | [C] [V w51A] | `b51-04-sponsor-operating-efficiency.md` |
| CF cost by size (rule A) | 373 bps (<$10m), 149 ($10–100m), 118 ($100m–1bn), 80 (≥$1bn) | [C] | same |
| Scale elasticity | CFs 0.64 (SE 0.05); nationals ex processors 0.49 (SE 0.08); CF cost driven by whole-foundation size (total assets 0.78; DAF terms 0.03) | [C] | same |
| Affiliate staffing | 14 of top 50 report zero employees with documented affiliate staffing; 63% of their FY2024 opex is Part IX 11a+11g fees paid to parent; own-990 cost 84% lower after controls | [C] [V w51A] | same |
| Staff cost (Part IX lines 5–10) | CFs 78.7 bps of DAF assets; four self-staffed nationals 5.6–15.0 bps; affiliated-commercial 2.9 bps | [V w34S] | `direction-sponsor-executive-compensation.md` |
| Top-officer pay per $bn DAF assets | NPT $14k, DAFgiving360 $20k, Vanguard $23k vs CF median $734k; median CF top pay $725k (elasticity 0.23) | [V w28] | same |
| Accounts per employee | CFs ≥$10m ~8–11; own-staff top-50 nationals 85 (Schwab 578, Vanguard 232) | [C] | `b51-04` |
| Grants per employee FY2024 | DAFgiving360 5,670; JCF 3,891; Vanguard 1,864; AEF 736; NPT 453; ImpactAssets 250; SVCF 132; FFTC 117 (~50-fold range) | [C] | `b51-04` §3.5 |
| Opex per grant FY2024 | DAFgiving360 $69; JCF $89; Vanguard $162; AEF $209; NPT $474; Fidelity $61; RCF $122; MS GIFT $151; GS DAPF $457; ImpactAssets $1,917; SVCF $2,487; FFTC $2,319 | [C] | `b51-04` §3.5 |
| Trend FY2021→24 (112 own-staff CFs) | Opex +35%, DAF assets +9%, accounts +6%, employees +14%, cost per DAF dollar +21%, cost per account +25%; real opex per employee flat | [C] [V w51A] | `b51-04` |
| Labour rates | 990 median loaded $38.87/h (898 sponsors); $57–73/h at $250m+; $86/h DAFgiving360; BLS-based $55.45/h used in AI economics | [V w8] | `queue-pe-lenders-labour-rates.md` |
| Tail CFs | Median opex $630k, 5 employees, 205 bps of total assets; DAFs 17.7% of assets, 27.6% of grants; DAF admin plausibly $1.2k–$4.1k per account (central $2.9k), 90–285 bps; rule F $4,500 per account, 258 bps (34 CFs) | [C]/[I] | `b45n33-long-tail-operating-cost.md`; `b45n33-02-01-01-fund-totals-from-990.md` |
| IT spend | 3,157 returns report IT; median CF IT $17k–$116k | [V] | `ai-economics-replacement-analysis.md` governing update |
| Non-DAF reserves | Bank/broker-affiliated nationals 29.4 months of opex; independent nationals 2.2 months; CFs 1.6 months ex board-designated endowment | [V w29] | `direction-sponsor-financial-resilience.md` |

**Design readings [I].**
- Two operating archetypes exist: retail/self-service (Fidelity, DAFgiving360, RCF: ~$4.5–6k average grant, 20–33 grants per line, thousands of grants per employee) and high-touch (NPT, GS, SVCF, FFTC: $31k–$211k average, 4–10 grants per line, hundreds per employee). An AI-native enterprise must declare which it is.
- Affiliate-staffed sponsors' true cost is off their 990; the nationals' "23 bps" is a floor, not a benchmark for a standalone entity.
- CF cost is whole-organisation; DAF administration is not separable on public data.

### 11.2 Exception-load proxies and grant counts
- Core review-need proxy 7.76% of lines / 11.61% of dollars (top 50); ~7–8.5% of grants at Fidelity/NPT/Vanguard on the core definition; broad per-grant share 17–31% (likely 28–31% given JCF bands). These are **recipient screens, not observed review**; many flagged lines are cleared by standing rule.
- Grant counts: Fidelity 2,664,446 (CY2024; 3.0m CY2025 per 2026 report as used in entrant sim); DAFgiving360 1,100,000 (FY2024); Vanguard 221,825 (FY2024) / 267,838 (CY2025); RCF 160,000; NPT 129,575 (FY2024) / 159,543 (FY2025); MS GIFT 122,000; AEF 109,708; JCF 89,485 (FY2024) / 77,364 (FY2023); Charityvest 48,744 (2025, company); GS DAPF 29,254.
- Recurring grants 38% at DAFgiving360 (FY2025); 63–74% of grants unrestricted by count at Fidelity, NPT, DAFgiving360, Vanguard.

### 11.3 AI economics (summary for org design)
- Inference is not the constraint (~$0.45 vs ~$83). Oversight, integration and residual human workload are.
- Calibrated AI value pools are small: $445k large national; $69k at a $1bn CF; $18k at $250m [S].
- Routing (auto-close) beats assistance only if the escaped-error multiple is low; bank-style AML enforcement would rule out auto-closing wherever such errors can escape [C/I].
- Manual improvement (A) is modal in up to 6 of 15 large-national processes under audited-realization assumptions; AI assistance is modal nowhere.

### 11.4 Entrant simulation (as governed)
- Legal core is small (six statutory parts); commercial core (custody, rails, sponsor trust, adviser distribution) is large and incumbent-held.
- S3 requires ~42 customers for $5m ARR (S1: 5); S3 average FTE 5/9/14 in first 24 months vs S1 20/32/45 [S].
- Conditions under which S3 fails: data access gated by vendors; small cost pool; buyers want bundles; final guidance favours record owners; incumbents match within 12–18 months; sponsor counsel forbids model-assisted decisions.

### 11.5 AI governance failure modes (summary)
- 16 failure modes; unconstrained AI creates risk in 13, redistributes in 3 (rubric, no observed DAF AI incidents, no human-error baseline).
- Highest trust-risk AI use: donor-facing tax answers (Moffatt v. Air Canada precedent; legal AI hallucination 17–33%).
- Governance burden is highest where AI's economic case is strongest (unstructured, high-judgment work) — the binding constraint is governance, not model capability [I].
- Vendor due-diligence questions: does AI change grant state; model/version change evaluation; add-only screening; agent labelling and limits; exportable decision records incl. AI outputs; training on customer data; model-retirement plan.

---

## 12. Design-question index (EV and GAP IDs)

Use this to trace design choices to evidence. "Evidence" rows are the strongest available; "Gaps" are what would change the answer.

| Design question | Evidence | Gaps |
|---|---|---|
| How big is the serviceable market (accounts, assets, grants)? | EV-001–EV-009, EV-013, EV-016 | GAP-009 |
| Who are the realistic partners vs competitors among platforms? | EV-040, EV-041, EV-046–EV-058, EV-149 | GAP-010, GAP-022, GAP-023 |
| What fee can an AI-native sponsor or operator charge? | EV-066–EV-071, EV-038, EV-060, EV-073 | GAP-014, GAP-018 |
| How many staff per unit of volume does a DAF sponsor need today? | EV-039, EV-132–EV-141, EV-025, EV-032, EV-034 | GAP-001, GAP-005, GAP-006, GAP-007, GAP-040 |
| What share of grants needs human judgment? | EV-079–EV-083, EV-045, EV-147 | GAP-001, GAP-003, GAP-026 |
| Where may AI act, and where must a human or deterministic rule decide? | EV-090, EV-113, EV-154, EV-109, EV-101 | GAP-004, GAP-024, GAP-034 |
| Is AI worth it economically, and at what scale? | EV-106–EV-112, EV-143, EV-153 | GAP-001, GAP-004, GAP-034 |
| How should agent-originated recommendations be handled? | EV-088, EV-089, EV-104, EV-105 | GAP-011, GAP-024 |
| Build or partner: sponsor, custody, rails, master data, ledger? | EV-060, EV-064, EV-065, EV-098, EV-116, EV-119, EV-123 | GAP-002, GAP-012, GAP-016, GAP-027, GAP-028 |
| Payment rails and remittance design | EV-063–EV-065, EV-074, EV-085, EV-086, EV-144 | GAP-016, GAP-020, GAP-030, GAP-039 |
| Eligibility evidence and retention | EV-082, EV-090, EV-100, EV-045 | GAP-021 |
| Regulatory obligations and pending changes | EV-090–EV-097, EV-099, EV-075 | GAP-008, GAP-012, GAP-013, GAP-037 |
| Data rights, portability and integration constraints | EV-121–EV-123, EV-031, EV-129, EV-130 | GAP-002, GAP-031, GAP-038 |
| Donor/nonprofit experience targets | EV-076–EV-078, EV-124–EV-127, EV-059 | GAP-006, GAP-020 |
| Fraud and security controls | EV-128, EV-062, EV-049, EV-148 | GAP-025, GAP-029 |
| Failure modes of DAF businesses to design against | EV-115–EV-120, EV-019, EV-150 | GAP-036 |
| Which earlier claims must not be cited | EV-151–EV-156; §6 above | — |
