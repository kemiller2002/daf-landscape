# The U.S. Donor-Advised Fund Industry, November 2026: Structure, Economics, Technology and AI

**Consolidated report.** Version 2026-11-15. Repository `kemiller2002/daf-landscape`.

**Consolidation (2026-11-15):** §11 was reorganised from a chronological list of batch summaries into themes, and figures in §1–§10 that later validation superseded were updated. Every change, with its governing source, is in the [consolidation changelog](mission-2026-11-14/consolidation-changelog.md). The pre-consolidation text is archived in [`archive/`](mission-2026-11-14/archive/DAF-INDUSTRY-REPORT-2026-11.pre-consolidation.md).

This report sits on top of the repository's research documents and datasets: 96 and 89 at the baseline inventory (repo [`repo-inventory-final.json`](../data/mission-2026-11-14/repo-inventory-final.json)), and 265 Markdown files under `research/` and 507 CSV files under `data/` as of 2026-11-19 (file count, PR #53). It does not repeat them. Each section states the current best understanding, its evidence state, and where the evidence lives.

**Labels used throughout:**
- **Claim states** follow the EDF claim-and-confidence policy: *internal-demonstration, suggestive, unsupported, contradicted*. Confidence runs Low → High.
- **[V]** = independently validated (registers in `data/mission-2026-11-14/validation-register*.csv`).
- **[RT]** = corrected by red-team review.
- **[S]** = scenario number, not an estimate.

**Decision-oriented companion:** [strategic synthesis A–G](mission-2026-11-14/strategic-synthesis.md). Its §0 (2026-11-19) holds the current governing A–G and top ten; the layered sections after it are kept for history. [gap19-11]
**Method and frameworks:** [Clarity/EDF application guide](mission-2026-11-14/clarity-edf-application-guide.md), pinned to the canonical framework commits.

---

## 1. Market size and shape

| Metric (DAFRC revised, FY2024) | Value | Note |
|---|---|---|
| Charitable assets in DAFs | $327.87bn | FY2020→FY2024 CAGR 18.1% ([DAFRC Updated Analysis memo](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf); [DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`derived-metrics.csv`](../data/mission-2026-11-14/derived-metrics.csv)) |
| Contributions | $90.57bn | +38.6% YoY after declines in FY2022–23 ([DAFRC Updated Analysis memo](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf); [DAFRC Annual DAF Report page](https://www.dafresearchcollaborative.org/research/annual-daf-report)) |
| Grants | $64.60bn | CAGR 16.1% ([DAFRC Updated Analysis memo](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf); [DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`derived-metrics.csv`](../data/mission-2026-11-14/derived-metrics.csv)) |
| Reported accounts | 3.59m | **79.5% are in 22 donation-processor sponsors holding 0.9% of assets**; about 66% (59.2% on corrected data) if Givinga, whose account unit is undefined, is excluded (§11.1) ([DAFRC Updated Analysis memo](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf); [DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`dafrc-sponsor-schedule-d-fy2019-2024.csv`](../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv)) |
| Traditional invested accounts | ≤ 737k | upper bound; no lower bound from public data ([DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`dafrc-sponsor-schedule-d-fy2019-2024.csv`](../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv); repo [`regulation-market-structure-portability.md`](../research/mission-2026-11-14/regulation-market-structure-portability.md)) |
| Sponsors | ~1,500 (1,512 reported) | about 803 community foundations ([DAFRC Annual DAF Report page](https://www.dafresearchcollaborative.org/research/annual-daf-report); [DAFRC Updated Analysis memo](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf)) |

DAFRC totals recompute exactly from its 8,751-row sponsor panel, which is reproduced in the repository with `scripts/mission_daf_metrics.py` [V] ([DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`scripts/mission_daf_metrics.py`](../scripts/mission_daf_metrics.py); repo [`validation-register-wave2b.csv`](../data/mission-2026-11-14/validation-register-wave2b.csv)). NPT's annual series agrees on dollars within about 2% for FY2020–23 ([NPT 2024 DAF Report](https://www.nptrust.org/philanthropic-resources/philanthropist/resources/2024-daf-report-highlights/2024-daf-report-npt/); [DAFRC Annual DAF Report 2025](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-DAF-Research-Collaborative.pdf); repo [`daf-market-annual-series.csv`](../data/mission-2026-11-14/daf-market-annual-series.csv)). It counts 1.55–1.84× fewer accounts because it excludes most processors ([NPT 2024 DAF Report](https://www.nptrust.org/philanthropic-resources/philanthropist/resources/2024-daf-report-highlights/2024-daf-report-npt/); [DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`daf-market-annual-series.csv`](../data/mission-2026-11-14/daf-market-annual-series.csv); repo [`derived-metrics.csv`](../data/mission-2026-11-14/derived-metrics.csv)).
Sources: [quantitative datasets](mission-2026-11-14/quantitative-datasets-and-data-dictionary.md); [processor share](mission-2026-11-14/regulation-market-structure-portability.md).

**Corrected totals (repository recomputation).** Filed Form 990 Schedule D values replace DAFRC's imputed rows, and double-counted terminated sponsors are removed. On that basis FY2024 assets are **$323.27bn** (−1.40% vs $327.87bn) and accounts are 7.8% lower, while contributions are +$2.20bn and grants +$1.84bn. There are 2,564 itemized adjustments ([corrected totals](mission-2026-11-14/full-universe-990-harvest-and-corrected-totals.md); `data/mission-2026-11-14/dafrc-corrected-market-totals.csv`, `dafrc-corrections-itemized.csv`; source: IRS e-file XML via the GivingTuesday mirror). Sponsors outside DAFRC's list hold only $0.15–0.89bn a year, except SDG Impact Fund's self-reported $10.1bn (FY2021–22).

**Vendor footprint from Form 990 (all 1,512 FY2024 sponsors).** In Part VII-B, Ren/Stellar is named as a paid contractor by 30 sponsors holding $48.55bn (14.8% of DAFRC assets) in any FY2022–25 return, or 18 sponsors holding $30.18bn (9.2%) in their latest return [V wave 5]. After the FY2025 filing refresh the latest-return measure is 19 sponsors and $31.56bn, the addition being Ayco's final return. Ayco merged into GS DAPF on 2025-07-01, so it is not a live client. The share is 9.6% of DAFRC FY2024 assets (repo [`validation-wave31a-report.md`](mission-2026-11-14/validation-wave31a-report.md); [`gap19-fy2025-refresh.md`](mission-2026-11-14/gap19-fy2025-refresh.md)). [V wave 33B] [gap19-11] GS DAPF ($11.84bn) appears in FY2022 only, and on corrected FY2024 assets the cumulative share is 15.0% ([vendor footprint](mission-2026-11-14/full-universe-990-harvest-and-corrected-totals.md), wave-5 governing note). Other DAF vendors appear at one to six sponsors each. 985 sponsors list no contractor above $100k. These counts are floors: Part VII-B lists only the top five contractors above $100k.

**Payout.**
- **Aggregate:** grants over beginning assets were 23.7–28.4% in FY2020–24 ([DAFRC Updated Analysis memo](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf); [DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`derived-metrics.csv`](../data/mission-2026-11-14/derived-metrics.csv)).
- **Typical sponsor:** the median sponsor with ≥$1m in assets pays out about 11–12.5%, and 19–24% of those sponsors pay out under 5% ([DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`derived-metrics.csv`](../data/mission-2026-11-14/derived-metrics.csv); repo [`scripts/mission_daf_metrics.py`](../scripts/mission_daf_metrics.py)).
- **By segment:** national sponsors' median is about 20%, community foundations about 11%, and university or hospital sponsors about 5.4% **[RT]** ([DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`validation-register-wave2b.csv`](../data/mission-2026-11-14/validation-register-wave2b.csv)).
- **Transfers between DAF sponsors** are 10–18% of the nationals' listed grant dollars. They inflate apparent payout and double-count in market sums. Pooled FY2021–24 payout net of these transfers is 19.0–21.5% against 23.9% gross (§11.1) ([Fidelity Charitable Form 990 FY2025](https://projects.propublica.org/nonprofits/organizations/110303001/202601389349301700/IRS990); [DAFgiving360 Form 990 FY2025](https://projects.propublica.org/nonprofits/organizations/311640316/202611199349300601/IRS990ScheduleF); [NPT Form 990 FY2025](https://projects.propublica.org/nonprofits/organizations/237825575/202601289349302480/IRS990ScheduleF); [Vanguard Charitable Form 990 FY2025](https://projects.propublica.org/nonprofits/organizations/232888152/202621329349306657/IRS990); repo [`breadth-community-faith-infrastructure-emerging.md`](../research/mission-2026-11-14/breadth-community-faith-infrastructure-emerging.md)).

Fund-level payout is not public in filings: Form 990 Schedule D Part I reports, per sponsor, only the number of donor-advised funds and their aggregate contributions, grants and year-end value ([IRS Schedule D (Form 990), Rev. Dec 2024](https://www.irs.gov/pub/irs-pdf/f990sd.pdf)). Voluntary account-level samples exist: DAFRC's 2024 National Study (111 programs, over 50,000 accounts) puts the median three-year account payout at 9% (15% excluding inactive accounts) and the mean at 18%, and 22% of accounts made no grants in 2020–22 ([executive summary](https://johnsoncenter.org/wp-content/uploads/2024/02/DAFRC_Executive_Summary_Key_Findings.pdf); repo [`direction-academic-literature.md`](mission-2026-11-14/direction-academic-literature.md) F1; [V wave 24B]). [gap19-11]

**Concentration differs by layer.** Do not conflate these markets:

| Layer | Measure | Finding | State |
|---|---|---|---|
| Sponsor assets | DAFRC FY2024 | CR3 45.5%, CR5 55.8%, HHI ≈ 830 (unconcentrated). National sponsors only: CR3 63.2%, HHI ≈ 1,566 ([DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`dafrc-sponsor-schedule-d-fy2019-2024.csv`](../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv); repo [`validation-register-wave2b.csv`](../data/mission-2026-11-14/validation-register-wave2b.csv)) | [V][RT] High |
| Administration | Period-aligned | About 39% of assets at three affiliate-linked nationals (Fidelity/FMR; Schwab; Vanguard as a hybrid) ([Fidelity Charitable FY2025 audited statements](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf); [DAFgiving360 FY2025 results](https://www.dafgiving360.org/press-release/fiscal-year-2025-results); [Vanguard Charitable FY2025 financial statements](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf); [DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)). Fully outsourced platform administration: ≥6 sponsors holding 9.1% ([DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`regulation-market-structure-portability.md`](../research/mission-2026-11-14/regulation-market-structure-portability.md)) | Medium |
| Software | Vendor self-reports | Licensed DAF software at 31–94% of sponsors (vendor self-reports and an older survey; superseded by the repository map below) ([Foundant CommunitySuite page](https://www.foundant.com/products/communitysuite/); [Tech Impact CF software landscape](https://techimpact.org/sites/default/files/2024-03/TECH%20IMPACT%20Integrated%20Software%20for%20Community%20Foundations.pdf); [DAFRC Annual DAF Report page](https://www.dafresearchcollaborative.org/research/annual-daf-report)). Community foundations: Foundant CommunitySuite claims 700+ ([Foundant CommunitySuite page](https://www.foundant.com/products/communitysuite/)); the repository's EIN-level map finds it at 361 of 803 foundations (45%) and 32.7% of mapped community-foundation DAF assets [V wave 9] ([CF vendor map](mission-2026-11-14/queue-cf-vendor-map.md)). National and white-label market: Ren (incl. iPhi), Foundation Source, TIFIN Give, Give Interactive ([Great Hill investment in Ren (Pulse 2.0)](https://pulse2.com/great-hill-partners-announces-strategic-growth-investment-in-donor-advised-fund-platform-ren/); [Foundation Source DAF OS brief](https://foundationsource.com/resources/product-briefs/the-modern-operating-system-for-donor-advised-funds/); [SEI Charitable Fund release](https://www.seic.com/about-sei/newsroom/sei-launches-sei-charitable-fund-bringing-charitable-giving-advisor-and-client-wealth-experience); [Give Interactive homepage](https://www.giveinteractive.com/)) | Low-Medium; HHI not computable |
| Custody | Audited notes | about 20.2% of period-aligned FY2024 assets with one custodian family (Fidelity Brokerage Services, Fidelity Charitable's custodian); lower bound ([Fidelity Charitable FY2025 audited statements](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf); [DAFRC Updated Analysis memo](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf)) <!-- CITE-CHECK RESOLVED 2026-11-14 (text corrected): 26.2% appears to be Fidelity's June-2025 net assets ($85.86bn, FID audit) over the DAFRC FY2024 total ($327.87bn) - the same period mismatch the red team corrected in V2B-01/V2B-03. Period-aligned Fidelity share is about 20.2%. Not changed. --> | lower bound only |
| Distribution | Channel graph | About 11 wealth-firm programs on RCF + Ren ([Edward Jones Charitable Gift Fund portal](https://edwardjones.donorfirstx.com/); [Ameriprise RCF portal](https://ampf.donorfirstx.com/); [RBC RCF portal](https://rbcrcf.donorfirstx.com/); [Ren LPL RCF page](https://www.reninc.com/lpl-rcf-daf/); [Ren UBS RCF page](https://www.reninc.com/why-ubs-advisors-choose-rcf/); [SEI Giving Fund portal](https://sei.donorfirstx.com/); [MDRT Global Gift Fund portal](https://mdrt.donorfirstx.com/); repo [`relationship-graph-edges.csv`](../data/mission-2026-11-14/relationship-graph-edges.csv)); SEI multi-sources (RCF/Ren and GiveClear/TIFIN) ([SEI Giving Fund portal](https://sei.donorfirstx.com/); [SEI Charitable Fund release](https://www.seic.com/about-sei/newsroom/sei-launches-sei-charitable-fund-bringing-charitable-giving-advisor-and-client-wealth-experience)) | Medium-High on edges |

Sources: [vendor dependency and concentration](mission-2026-11-14/vendor-dependency-concentration.md); [red team 2B](mission-2026-11-14/red-team-wave2b-graph-data-incentives.md).

---

## 2. Who does what: legal sponsor, administrator, technology, rails, distribution

The industry is a stack whose layers are often owned by different parties. The consolidated relationship graph (2026-11-19) has up to 893 nodes and 1,051 edges, merged from the base file and 26 additions files (1,110 rows; 51 duplicates merged, 8 alias self-loops set aside), every edge sourced and status-labelled (repo [`relationship-graph-edges-consolidated-2026-11-19.csv`](../data/mission-2026-11-14/relationship-graph-edges-consolidated-2026-11-19.csv); [V wave 31A]) (repo [`relationship-graph-nodes.csv`](../data/mission-2026-11-14/relationship-graph-nodes.csv); repo [`relationship-graph-edges.csv`](../data/mission-2026-11-14/relationship-graph-edges.csv)): 958 confirmed, 23 historically confirmed, 47 inferred, 11 unknown, 5 reported, 3 probable, 2 unverified lead, 1 pending, 1 rejected. A wave-2B red-team sample of 15 "confirmed" base edges found 0 status errors and 2 scope imprecisions. A 2026-11-19 red team of all 109 inferred, unknown, reported, probable, pending, vendor-claim and crt.sh-sourced edges (one independent public check each) marked 41 confirmed, 16 weakened, 52 unverified leads and 0 contradicted (repo [`gap19-graph-consolidation.md`](mission-2026-11-14/gap19-graph-consolidation.md); [V wave 31A]) [gap19-11] (repo [`validation-register-wave2b.csv`](../data/mission-2026-11-14/validation-register-wave2b.csv); repo [`red-team-wave2b-graph-data-incentives.md`](../research/mission-2026-11-14/red-team-wave2b-graph-data-incentives.md)).

### 2.1 Affiliate-integrated nationals
Fidelity Charitable, DAFgiving360 and Vanguard Charitable combine sponsor brand, affiliated investment funds and affiliated administration ([Fidelity Charitable FY2025 audited statements](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf); [DAFgiving360 FY2025 results](https://www.dafgiving360.org/press-release/fiscal-year-2025-results); [Vanguard Charitable FY2025 financial statements](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf)):
- Fidelity Charitable pays FMR affiliates amounts equal to donors' administrative fees **[V]** ([Fidelity Charitable FY2025 audited statements](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf)).
- Vanguard Charitable has 35 of 37 pools in Vanguard funds and pays a related-party service fee of $4.24m in FY2026 **[V]** ([Vanguard Charitable FY2026 financial statements](https://www.vanguardcharitable.org/sites/default/files/2026-11/VCEP_Financial_Statements_2026.pdf)).
- **New:** Vanguard Charitable selected **Give Interactive** for DAF recordkeeping, per a release issued by Give Interactive (Nov 2025) that quotes Vanguard Charitable's CIO **[vendor claim]**. Vanguard Charitable's FY2026 audited statements (FYE 2026-06-30) do not mention it, and go-live is unobserved ([Give Interactive / Vanguard Charitable release](https://www.giveinteractive.com/post/vanguard)).

### 2.2 The RCF–Ren spine
Renaissance Charitable Foundation sponsors branded programs for Edward Jones, Ameriprise, RBC, LPL/Commonwealth (RCF sponsorship confirmed by the CCF program circular and the West Virginia charity registry), Northwestern Mutual, UBS (one of four sponsors there), SEI, Fisher and MDRT ([Edward Jones Charitable Gift Fund portal](https://edwardjones.donorfirstx.com/); [Ameriprise RCF portal](https://ampf.donorfirstx.com/); [RBC RCF portal](https://rbcrcf.donorfirstx.com/); [Ren LPL RCF page](https://www.reninc.com/lpl-rcf-daf/); [Commonwealth Charitable Fund portal](https://cfndaf.donorfirstx.com/); [Northwestern Mutual RCF program circular](https://www.reninc.com/wp-content/uploads/2025/08/NWM-Program-Circular-11-24.pdf); [Ren UBS RCF page](https://www.reninc.com/why-ubs-advisors-choose-rcf/); [UBS DAF fact sheet](https://advisors.ubs.com/mediahandler/media/662455/Donor%20Advised%20Fund%20FactSheet.pdf); [SEI Giving Fund portal](https://sei.donorfirstx.com/); [Ren Fisher RCF page](https://www.reninc.com/rcf-fisher-daf/); [MDRT Global Gift Fund portal](https://mdrt.donorfirstx.com/); repo [`relationship-graph-edges.csv`](../data/mission-2026-11-14/relationship-graph-edges.csv)) <!-- CITE-CHECK RESOLVED 2026-11-14 (text corrected): RCF as sponsor of the Commonwealth Charitable Fund is only 'inferred' in relationship-graph-edges.csv (E034); LPL's own RCF channel is confirmed (E030). -->. Ren supplies the "DFX powered by Ren" portals ([Edward Jones Charitable Gift Fund portal](https://edwardjones.donorfirstx.com/); [MS GIFT donor portal](https://msgift.donorfirstx.com/)).

- **The payment flow:** RCF paid Ren $19.23m in FY2024. That equals 98% of RCF's admin-fee revenue from individual-fundholder accounts, the rate in force since FY2023 **[V]** ([RCF FY2024 audited statements](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf); [RCF FY2023 audited statements](https://renaissancecharitable.org/wp-content/uploads/2026/01/2023RCFAuditedFinancialStatements.pdf); repo [`rcf-ren-audited-admin-payments-2020-2024.csv`](../data/rcf-ren-audited-admin-payments-2020-2024.csv)).
- **Ren's role:** RCF describes it as platform, administrative infrastructure and operational support. Ren is not a technology-only vendor **[V]** ([RCF FAQ](https://renaissancecharitable.org/faqs/)).
- **Ren beyond RCF:** Ren portals also front Morgan Stanley GIFT (new finding), Bank of America's Charitable Gift Fund and AEF ([MS GIFT donor portal](https://msgift.donorfirstx.com/); [BofA Charitable Gift Fund portal](https://bofa.donorfirst.org/); [AEF/Ren release, Apr 2026](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/)). For Bank of America the only evidence is the portal; the earlier 10-K claim is **contradicted** **[V]** ([SEC full-text search, BofA filings](https://efts.sec.gov/LATEST/search-index?q=%22Charitable%20Gift%20Fund%22&ciks=0000070858); [BofA CGF Form 990 TY2024](https://projects.propublica.org/nonprofits/organizations/46010342/202503219349318170/full)). Ren-owned iPhi still serves the Cleveland Foundation and ImpactAssets ([Cleveland Foundation iPhi portal](https://www.iphiview.com/tcf/LogIn/tabid/444/Default.aspx); [ImpactAssets homepage (iPhi log-in)](https://impactassets.org/)). ImpactAssets is a late-stage Give Interactive migration, and iPhi lost 6 of 57 sponsors in 2023–Nov 2026 (§11.2).

**Edward Jones Charitable Gift Fund.** Each role has separate evidence:

| Role | Status | Evidence |
|---|---|---|
| RCF as legal sponsor | Confirmed | Edward Jones product page plus RCF's self-description ([Edward Jones DAF page](https://www.edwardjones.com/us-en/investment-services/investment-products/donor-advised-funds); [RCF FAQ](https://renaissancecharitable.org/faqs/)) |
| RCF manages and administers the fund | Confirmed | Edward Jones portal ([Edward Jones Charitable Gift Fund portal](https://edwardjones.donorfirstx.com/)) |
| Ren technology | Confirmed | Portal displays "DFX powered by Ren" ([Edward Jones Charitable Gift Fund portal](https://edwardjones.donorfirstx.com/)) |
| Ren back-office administration for Edward Jones specifically | Inferred only (partly corroborated) | Edward Jones's 2026 flyer says "a third-party administrator is responsible for day-to-day operations" but does not name it; the portal's terms are an agreement with Renaissance Acquisition Company LLC ("Ren"); RCF pays Ren under an audited contract, but nothing names Ren for Edward Jones ([Edward Jones Charitable Gift Fund flyer, 2026](https://www.edwardjones.com/sites/default/files/dam/jka6ifohxb/res-13116-a.pdf); [EJ portal Terms of Service](https://edwardjones.donorfirstx.com/Terms%20of%20Service.pdf)) ([RCF FY2024 audited statements](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf); repo [`relationship-graph-edges.csv`](../data/mission-2026-11-14/relationship-graph-edges.csv)) |

Two Edward Jones figures remain open:
- The 2021 "$2.9bn" figure is unverifiable (source PDF now 404) **[V]** ([Ren/RCF Edward Jones adviser guide (HTTP 404)](https://www.reninc.com/wp-content/uploads/2022/03/Advisor-Guide-and-FAQ-WH-RCF-2022-1.pdf) ([archived copy](http://web.archive.org/web/20250109124657/https://www.reninc.com/wp-content/uploads/2022/03/Advisor-Guide-and-FAQ-WH-RCF-2022-1.pdf)); repo [`validation-register.csv`](../data/mission-2026-11-14/validation-register.csv)).
- Edward Jones's private DAF has no public sponsor, administrator or vendor ([Edward Jones elevated wealth management release](https://www.edwardjones.com/us-en/why-edward-jones/news-media/press-releases/elevated-wealth-management)).

**Wave-3 additions [V].** Goldman's PWM DAF and GS Gives use Ren/Stellar software, with administration by Goldman entities. MS GIFT paid RenPSG $14.93m (CY2024). NPT's GivingPoint is built and hosted on Ren iPhi infrastructure, though only hosting evidence shows this and no contract is disclosed. Wave 12 extended this to 13 live NPT-sponsored program sites on the same Ren build (§11.2). Vanguard Charitable selected **Give Interactive** for recordkeeping. Give Interactive is controlled by **The Signatry Charitable Trust** (Signatry 2024 990 Schedule R), so a DAF sponsor controls the vendor that keeps another sponsor's records. See [vendor scope](mission-2026-11-14/queue-vendor-scope-ren-denominator.md) and [validation wave 3](mission-2026-11-14/validation-wave3-report.md).

### 2.3 Foundation Source / Charityvest
Foundation Source (owned by GTCR since 2023) acquired Vennfi (2024) and Giving Place (2025) ([GTCR acquires Foundation Source](https://foundationsource.com/newsroom/press-releases/gtcr-announces-acquisition-of-foundation-source/); [Foundation Source acquires Vennfi](https://foundationsource.com/newsroom/press-releases/foundation-source-acquires-vennfi-the-fintech-powering-donor-advised-fund-charityvest/); [Foundation Source acquires Giving Place](https://foundationsource.com/newsroom/press-releases/foundation-source-acquires-giving-place-platform-for-private-foundations-and-family-offices/)). Charityvest is an independent sponsor powered by Foundation Source, with TIAA, Temple and OneGive programs ([Charityvest + Vennfi guide](https://guide.charityvest.org/about-our-venture/charityvest-%2B-vennfi); [TIAA Wealth Management DAF release](https://www.prnewswire.com/news-releases/tiaa-wealth-management-makes-charitable-giving-part-of-the-financial-plan-with-new-donor-advised-fund-program-302891438.html); [Temple University DAF release](https://foundationsource.com/newsroom/press-releases/temple-university-launches-custom-donor-advised-fund-program-in-partnership-with-foundation-source-and-charityvest/); [OneAscent Form ADV Part 2A](https://files.adviserinfo.sec.gov/IAPD/Content/Common/crd_iapd_Brochure.aspx?BRCHR_VRSN_ID=1054956)).
- **Governance conflict:** Charityvest's President and director is paid by Foundation Source ($163,944 via Vennfi, 2024) ([Charityvest Form 990 TY2024](https://projects.propublica.org/nonprofits/organizations/812771871/202513189349315961/full)). This is stronger than previously recorded **[V]**.

### 2.4 TIFIN Give / GiveClear
GiveClear is the sponsor and TIFIN Give the platform ([Chariot partner profile: TIFIN Give](https://www.givechariot.com/resources/insights/getting-to-know-tifin-give-a-chariot-disbursements-partner-)). Since 2026-10-28 they also power the SEI Charitable Fund ([SEI Charitable Fund release](https://www.seic.com/about-sei/newsroom/sei-launches-sei-charitable-fund-bringing-charitable-giving-advisor-and-client-wealth-experience)). Chariot handles disbursement ([TIFIN and Chariot partnership](https://tifin.com/news/tifin-and-chariot-partner-to-transform-grant-payments/19418/)).

### 2.5 Payment rails
Four camps exist: Fidelity's own EFT/Stripe, PayPal Grant Payments (NPT, Vanguard), Ren's Rapid Disbursement Engine, and Chariot Disbursements (TIFIN/GiveClear, Daffy, Founders Pledge, Groundswell, Charityvest transitioning from Aug 2026) ([Fidelity Charitable nonprofit FAQ](https://www.fidelitycharitable.org/nonprofits/faqs.html); [PayPal Grant Payments launch](https://newsroom.paypal-corp.com/2022-08-25-PayPal-Launches-Grant-Payments,-Enabling-Charities-to-Quickly-Receive-Funds-from-Grantmakers); [Vanguard Charitable PayPal electronic granting release](https://prnewswire.com/news-releases/vanguard-charitable-launches-electronic-granting-solution-surpassing-100-million-in-electronic-grants-to-more-than-400-charities-in-first-4-months-301932762.html); [Ren Rapid Disbursement Engine release](https://prnewswire.com/news-releases/ren-debuts-rapid-disbursement-engine-expanding-philanthropic-services-to-meet-rapid-daf-growth-301999647.html); [TIFIN and Chariot partnership](https://tifin.com/news/tifin-and-chariot-partner-to-transform-grant-payments/19418/); [Chariot partner profile: Daffy](https://www.givechariot.com/resources/insights/getting-to-know-daffy-a-chariot-disbursements-partner); [Founders Pledge selects Chariot](https://www.givechariot.com/post/founders-pledge-selects-chariot-to-power-grant-payments); [Chariot llms.txt](https://www.givechariot.com/llms.txt); [Chariot partner profile: Charityvest](https://www.givechariot.com/resources/insights/getting-to-know-charityvest-a-new-chariot-disbursements-partner)).
- The only observed switch is Charityvest moving from PayPal to Chariot, still in transition: Chariot dates it from Aug 2026, while Charityvest's own charity guide still describes PayPal Grant Payments [V wave 6] ([Chariot partner profile: Charityvest](https://www.givechariot.com/resources/insights/getting-to-know-charityvest-a-new-chariot-disbursements-partner); repo [`company-timeline-events.csv`](../data/mission-2026-11-14/company-timeline-events.csv)).
- Fidelity's 2026 Giving Report: "Today, 67% of our grants are distributed via EFT" ([Fidelity Charitable 2026 Giving Report PDF](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf); also summarised in [Chariot on Fidelity's 2026 Giving Report](https://www.givechariot.com/resources/insights/top-8-takeaways-from-fidelity-charitables-2026-giving-report)) [V wave 4]. No electronic-only mandate is confirmed ([Fidelity Charitable nonprofit FAQ](https://www.fidelitycharitable.org/nonprofits/faqs.html)).

### 2.6 Eligibility data
IRS BMF, Pub 78, revocation and OFAC data sit upstream of every disclosed eligibility check ([IRS EO BMF extract](https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf); [IRS TEOS bulk data downloads](https://www.irs.gov/charities-non-profits/tax-exempt-organization-search-bulk-data-downloads); [IRS Auto-Revocation List](https://www.irs.gov/autorevocationlist); [Chariot compliance help page](https://help.givechariot.com/onboarding/trust-and-safety/compliance); [Candid Charity Check FAQ](https://developer.candid.org/docs/faqs-charity-check) ([archived copy](http://web.archive.org/web/20250425115007/https://developer.candid.org/docs/faqs-charity-check)); [RCF grantmaking due-diligence policy](https://renaissancecharitable.org/wp-content/uploads/2026/02/Grantmaking-Due-Diligence-Policy.pdf)).

### 2.7 Shared single points of failure
- The RCF–Ren contract. ([RCF FY2024 audited statements](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf))
- Ren's DFX portal family. ([Edward Jones Charitable Gift Fund portal](https://edwardjones.donorfirstx.com/); [MS GIFT donor portal](https://msgift.donorfirstx.com/); [BofA Charitable Gift Fund portal](https://bofa.donorfirst.org/))
- Foundation Source behind Charityvest's programs. ([Charityvest + Vennfi guide](https://guide.charityvest.org/about-our-venture/charityvest-%2B-vennfi))
- Chariot on Column N.A. ([Chariot llms.txt](https://www.givechariot.com/llms.txt))
- GiveClear as TIFIN Give's sole sponsor. ([Chariot partner profile: TIFIN Give](https://www.givechariot.com/resources/insights/getting-to-know-tifin-give-a-chariot-disbursements-partner-); [SEI Charitable Fund release](https://www.seic.com/about-sei/newsroom/sei-launches-sei-charitable-fund-bringing-charitable-giving-advisor-and-client-wealth-experience))
- The IRS master file. ([IRS EO BMF extract](https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf))

Sources: [vendor graph](mission-2026-11-14/vendor-dependency-concentration.md); [breadth](mission-2026-11-14/breadth-community-faith-infrastructure-emerging.md); prior `edward-jones-ren-*`, `ren-*`, `charityvest-*` files.

---

## 3. Economics and incentives

**Revenue model.**
- Sponsors charge tiered basis points on balances. Fidelity, DAFgiving360 and Charityvest start at 0.60% on the first $500k ([Fidelity Charitable fees](https://www.fidelitycharitable.org/giving-account/what-it-costs.html); [DAFgiving360 Program Policies, Dec 2024](https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf); [Charityvest fee guide](https://guide.charityvest.org/for-donors/fees-and-expenses)). RCF/Ren charges 0.65% with a $250 minimum ([RCF advisor-managed DAF fees](https://renaissancecharitable.org/advisor-managed-dafs/)). Bank of America charges 0.90% flat ([BofA CGF fee schedule](https://www.bankofamerica.com/content/documents/philanthropic/cgf_fee_schedule.pdf)). Daffy charges flat memberships of $0–40/month ([Daffy membership fees](https://help.daffy.org/en/articles/6323771-what-are-daffy-s-membership-fees); repo [`sponsor-fee-schedules.csv`](../data/mission-2026-11-14/sponsor-fee-schedules.csv)).
- Investment expense ratios flow to affiliated managers at the nationals ([Fidelity Charitable FY2025 audited statements](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf); [Vanguard Charitable FY2025 financial statements](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf)).
- Adviser fees on DAF assets (for example OneGive's waivable 55 bps **[V]** ([OneAscent Form ADV Part 2A](https://files.adviserinfo.sec.gov/IAPD/Content/Common/crd_iapd_Brochure.aspx?BRCHR_VRSN_ID=1054956))) bind distribution. Adviser fees are capped at 1.00% only at MS GIFT, DAFgiving360 and TIFIN Give; Fidelity CIAP, NPT, AEF and RCF publish no numeric cap, and observed RIA brochures charge 0–2.00% [V wave 11] (§11.4).

**Incentive structure.** Analysis: [industry incentives](mission-2026-11-14/industry-incentives-structural-analysis.md), with [RT] corrections.

| Practice | Classification | Confidence |
|---|---|---|
| Asset-based fee alignment favouring retention | **Mixed**: incentive documented, effect on payout unsupported **[RT]** ([Fidelity Charitable FY2025 audited statements](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf); [RCF FY2024 audited statements](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf); [DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)) | Low on effect |
| No payout requirement | Structural (statute) ([26 U.S.C. §4966](https://www.law.cornell.edu/uscode/text/26/4966); [IRS donor-advised funds page](https://www.irs.gov/charities-non-profits/charitable-organizations/donor-advised-funds)) | High |
| Edge-case grant review (§4966/4967) | Structural ([26 U.S.C. §4966](https://www.law.cornell.edu/uscode/text/26/4966); [26 U.S.C. §4967](https://www.law.cornell.edu/uscode/text/26/4967)) | Medium-High |
| Manual review of listed public charities | **Mixed** ([Rev. Proc. 2018-32 summary (The Tax Adviser)](https://www.thetaxadviser.com/issues/2018/aug/irs-updates-charitable-contribution-procedures/); [California AG release](https://oag.ca.gov/node/623769)) | Medium |
| Paper checks | Mixed, leaning habit ([Fidelity Charitable nonprofit FAQ](https://www.fidelitycharitable.org/nonprofits/faqs.html)) | Medium |
| History loss in platform migrations | Habit ([AEF DonorCentral sunset notice](https://engage.aefonline.org/dc-sunset/) ([archived copy](http://web.archive.org/web/20261003000017/https://engage.aefonline.org/dc-sunset/))) | Medium |
| Weak nonprofit leverage | Structural: the nonprofit is neither the payer nor the legal party, so sponsor revenue does not depend on its satisfaction. [I] inference from [`industry-incentives-structural-analysis.md`](mission-2026-11-14/industry-incentives-structural-analysis.md) (classification table) | Medium-High [gap19-11] |

**Who resists redesign (by incentive, not intent):** affiliated managers, fee-share administrators, advisers paid on DAF AUM, and discretion-valuing sponsors. [I] inference from [`industry-incentives-structural-analysis.md`](mission-2026-11-14/industry-incentives-structural-analysis.md) §5 (stakeholder table). [gap19-11]
**Who benefits:** working nonprofits, small donors, and challengers not paid on assets. [I] inference from [`industry-incentives-structural-analysis.md`](mission-2026-11-14/industry-incentives-structural-analysis.md) §5 (stakeholder table). [gap19-11]

**Challengers.**
- Daffy reports $2bn in assets (Sept 2026, company-reported) ([Daffy $2B release](https://www.daffy.org/resources/two-billion-assets-under-management)). Its FY2024 990 shows $334.19m net assets **[V]** ([Daffy Charitable Fund Form 990 TY2024](https://projects.propublica.org/nonprofits/organizations/863177440/202513209349301201/full)).
- Charityvest's 2025 figures are company-reported and not comparable to its 990 series **[V]** ([Charityvest 2025 annual report](https://www.charityvest.org/annual-report-2025); [Charityvest Form 990 TY2024](https://projects.propublica.org/nonprofits/organizations/812771871/202513189349315961/full)).
- Both raised effective prices as they moved upmarket ([Vennfi seed release ('zero fees')](https://www.newswire.com/news/this-startup-raised-3-7m-to-let-anyone-donate-stocks-and-etfs-with-a-21260863); [Physician on FIRE on Charityvest fees](https://www.physicianonfire.com/better-donor-advised-fund/); [Charityvest fee guide](https://guide.charityvest.org/for-donors/fees-and-expenses); [Daffy membership tier changes](https://help.daffy.org/en/articles/11730892-how-do-i-change-my-membership)). Incumbents removed minimums (2020) ([ThinkAdvisor on Fidelity minimums](https://www.thinkadvisor.com/2020/09/30/fidelity-charitable-ends-daf-account-minimums/); [Schwab Charitable minimums release](https://www.dafgiving360.org/press-releases/schwab-charitable-expands-access-and-options)).

**Vendor economics.** Ren's corporate revenue, margins and customer concentration are not public: no press, private-equity or registry source gives a figure (repo [`queue-batch37-vendor-economics-owners.md`](mission-2026-11-14/queue-batch37-vendor-economics-owners.md) Q-B06; [V wave 22]). Named Ren receipts in sponsor 990s total $44.98m in TY2024 (18 sponsors). RCF is 42.7% of that and the two Morgan Stanley programs 43.0% (batch 37A §1.2; V wave 22). This is a floor on receipts, limited to sponsors' top-five contractor lines, not Ren revenue. [V wave 33B] [gap19-11] The audited RCF payment is a named service fee, not Ren's ARR ([RCF FY2024 audited statements](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf)). Ren's claims of ">60%", "about half" or "$200bn" of DAF assets are **unsupported** on public evidence: ([Ren homepage](https://www.reninc.com/); [Great Hill investment in Ren (Pulse 2.0)](https://pulse2.com/great-hill-partners-announces-strategic-growth-investment-in-donor-advised-fund-platform-ren/); [AEF/Ren release, Apr 2026](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/))
- On public evidence, sponsors holding about **28%** of FY2024 DAF assets ($91.6bn of $327.9bn) use Ren technology in some form **[V wave 3]**. The consolidated relationship graph (2026-11-19) puts the share of FY2024 DAF assets at sponsors with any confirmed Ren/Stellar technology, administration or payment link at **32.2%** ($105.6bn, 54 sponsors), or 31.6% when the evidence is dated 2024 or later. This is a floor: six sponsors with confirmed Ren edges were not EIN-matched, and with them the share is 32.9%. The same shares hold on corrected FY2024 assets. The rise from 28% is breadth: 40 added sponsors ($15.9bn), 29 of them on tenant or portal-link observation and 11 on Form 990 payee lines (5 of those FY2022–23 only). NPT (12.8% of the market, about 40% of the tier) still rests on hosting evidence [I]. The figure measures a public Ren link, not Ren as system of record (repo [`gap19-graph-consolidation.md`](mission-2026-11-14/gap19-graph-consolidation.md) §4; [V wave 31A]). The full Form 990 harvest (all 1,512 sponsors) finds Ren/Stellar named by 30 sponsors holding $48.55bn (14.8%) in any FY2022–25 return, but only 18 sponsors holding $30.18bn (9.2%) in their latest return [V wave 5], and about 5% (RCF, MS GIFT) on Ren-paid administration. Nearly half of the 28% is NPT, evidenced by hosting (iPhi login redirect, shared Ren load balancer, Ren-hosted "NPT iPhi Statuspage") rather than a disclosed contract **[I: hosting inference, single-source]**. A 2026-11-19 second-source pass found no NPT filing, privacy-policy processor list, product article or Ren page naming Ren as NPT's vendor; Ren is not among NPT's five listed FY2025 contractors (the fifth is paid $220,927) ([gap19-second-source-pass.md](mission-2026-11-14/gap19-second-source-pass.md) C01) ([MS GIFT 990 via GivingTuesday mirror; Goldman PWM portal gspf.goldman.com; NPT GivingPoint](mission-2026-11-14/validation-wave3-report.md)). Ren's "60%+"/"about half" claims remain unreachable without Fidelity Charitable, DAFgiving360 or Vanguard Charitable, none of which shows a Ren vendor; Vanguard chose Give Interactive. (Earlier estimates: 8.7% → 9.0% → 28% of assets after NPT and Goldman evidence.) ([DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`validation-register-wave2b.csv`](../data/mission-2026-11-14/validation-register-wave2b.csv)) <!-- CITE-CHECK RESOLVED 2026-11-14 (text corrected): Validator V2B-05 recomputed $29.65bn = 9.04% for RCF, AEF, MS GIFT and BofA from DAFRC FY2024 (all imputed); the 8.7% ($28.5bn) figure was only partially confirmed. Not changed. -->.
- The "$200bn" figure includes non-DAF assets ([AEF/Ren release, Apr 2026](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/)).
- The arithmetic ceiling outside the four largest sponsors is about 48% **[RT]** ([Fidelity Charitable FY2025 audited statements](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf); [Vanguard Charitable FY2025 financial statements](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf); [DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`validation-register-wave2b.csv`](../data/mission-2026-11-14/validation-register-wave2b.csv)).

---

## 4. Operations: grant workflow, exceptions and portability

**Legal frame.**
- §4966 taxes taxable distributions: 20% on the sponsor, 5% (capped at $10k) on knowing managers ([26 U.S.C. §4966](https://www.law.cornell.edu/uscode/text/26/4966)).
- §4967 taxes prohibited benefits: 125% on the donor or adviser, 10% on knowing managers ([26 U.S.C. §4967](https://www.law.cornell.edu/uscode/text/26/4967)).
- §4958(c)(2) makes grants, loans and compensation to donors or advisers automatic excess benefits ([26 U.S.C. §4958](https://www.law.cornell.edu/uscode/text/26/4958)).
- Grants to listed §170(b)(1)(A) public charities are excepted from §4966, and grantors may rely on IRS status listings ([26 U.S.C. §4966](https://www.law.cornell.edu/uscode/text/26/4966); [Rev. Proc. 2018-32 summary (The Tax Adviser)](https://www.thetaxadviser.com/issues/2018/aug/irs-updates-charitable-contribution-procedures/)).

**Exception share.** Observable non-standard grants (foreign, fiscal-sponsor, non-501(c)(3)) are about 2.5–3% of dollars at the large nationals and far less by count ([Fidelity Charitable Form 990 FY2025](https://projects.propublica.org/nonprofits/organizations/110303001/202601389349301700/IRS990); [DAFgiving360 Form 990 FY2025](https://projects.propublica.org/nonprofits/organizations/311640316/202611199349300601/IRS990ScheduleF); [Vanguard Charitable Form 990 FY2025](https://projects.propublica.org/nonprofits/organizations/232888152/202621329349306657/IRS990); [NPT Form 990 FY2025](https://projects.propublica.org/nonprofits/organizations/237825575/202601289349302480/IRS990ScheduleF); repo [`breadth-community-faith-infrastructure-emerging.md`](../research/mission-2026-11-14/breadth-community-faith-infrastructure-emerging.md)). Foreign grants alone are 1.46% of dollars across the four largest nationals (NPT 4.84%) ([Fidelity Charitable Form 990 FY2025](https://projects.propublica.org/nonprofits/organizations/110303001/202601389349301700/IRS990); [DAFgiving360 Form 990 FY2025](https://projects.propublica.org/nonprofits/organizations/311640316/202611199349300601/IRS990ScheduleF); [Vanguard Charitable Form 990 FY2025](https://projects.propublica.org/nonprofits/organizations/232888152/202621329349306657/IRS990); [NPT Form 990 FY2025](https://projects.propublica.org/nonprofits/organizations/237825575/202601289349302480/IRS990ScheduleF); repo [`breadth-community-faith-infrastructure-emerging.md`](../research/mission-2026-11-14/breadth-community-faith-infrastructure-emerging.md)). This is a floor: new-charity reviews and declines are invisible in filings, because no sponsor publishes how it routes grants, how many exceptions it handles or how long review takes (repo [`gap19-exception-load-proxy.md`](mission-2026-11-14/gap19-exception-load-proxy.md) §5). On FY2023–24 Schedule I and F filings the like-for-like measure is about 3.6% of dollars at the four largest nationals. A broader review-need proxy (foreign recipients, recipients outside Pub 78 without an explaining label, rulings within 24 months, named fiscal sponsors, and private foundations or other recipients needing expenditure responsibility: the core proxy) is 10.0% of their dollars and 11.0% across the top 50 (10.96% after the Greater Horizons correction). [V wave 33B] It measures recipients, not observed review (§11.30; [V wave 32A]). [gap19-11]

**Discretion beyond tax exposure.** In 2026, after the April 21 SPLC indictment, the California AG's release named Fidelity Charitable, Vanguard Charitable and DAFgiving360 as having restricted grants **[RT confirmed]** ([California AG release](https://oag.ca.gov/node/623769)). Sixteen attorneys general, led by Minnesota, wrote to the three sponsors on 2026-05-21 about the decision "to stop or restrict payments" to SPLC ([multistate AG letter](https://oag.ca.gov/system/files/attachments/press-docs/2026-05-21%20SPLC%20-%20DAF%20Letter.pdf)). Whether the holds persisted is not shown in any public record found.

**Operating metrics.** No sponsor publishes grant turnaround P50/P90, exception rates or reviewer minutes. No sponsor publishes an SLA or a latency distribution by rail, and only 5 of 28 published turnaround statements are measured, all of them vendor figures (repo [`queue-batch36-metrics-rails.md`](mission-2026-11-14/queue-batch36-metrics-rails.md) P-PAY-05; [V wave 21]). No sponsor publishes human effort or exception rates (repo [`ai-economics-replacement-analysis.md`](mission-2026-11-14/ai-economics-replacement-analysis.md)). [gap19-11] NPT processed 159,543 grants in FY2025 ([NPT FY2025 annual report](https://www.nptrust.org/annual-reports/npt-annual-report/)). Its U.S. DAF program granted $6.44bn **[V][RT]** ([NPT FY2025 annual report](https://www.nptrust.org/annual-reports/npt-annual-report/)); the $6.61bn release figure likely includes U.K. and Transatlantic programs ([NonProfit Times on NPT FY2025](https://thenonprofittimes.com/?p=215695); [NPT FY2025 annual report](https://www.nptrust.org/annual-reports/npt-annual-report/)).

**Portability.**
- None of 12 sponsors reviewed publishes an outbound transfer policy (repo [`sponsor-transfer-portability-terms.csv`](../data/mission-2026-11-14/sponsor-transfer-portability-terms.csv)). Transfers are cash after liquidation and take 10 business days to 4 weeks ([Fidelity Charitable recommending a grant](https://www.fidelitycharitable.org/giving-account-guide/recommending-a-grant.html); [GTCF DAF transfer instructions](https://www.gtcf.org/wp-content/uploads/2026.05.18-GTCF_DAF_Transfer_Instructions.pdf)).
- No sponsor commits to moving grant history ([GTCF DAF transfer instructions](https://www.gtcf.org/wp-content/uploads/2026.05.18-GTCF_DAF_Transfer_Instructions.pdf); [Daffy help: closing an account](http://help.daffy.org/en/articles/6520234-how-do-i-close-my-daffy-account)). AEF's own migration kept two years ([AEF DonorCentral sunset notice](https://engage.aefonline.org/dc-sunset/) ([archived copy](http://web.archive.org/web/20261003000017/https://engage.aefonline.org/dc-sunset/))).
- Netting sponsor-to-sponsor transfers on filed 990s removes $8.03bn in FY2024 (rule R5, central tier; Batch 34, §11), consistent with Inequality.org's advocacy estimate of about $7.5bn ([Inequality.org on DAF-to-DAF giving](https://inequality.org/article/daf-to-daf-giving-2024/)).

Sources: prior batch 2A/2B/2C files; [regulation and portability](mission-2026-11-14/regulation-market-structure-portability.md); [breadth §6](mission-2026-11-14/breadth-community-faith-infrastructure-emerging.md).

---

## 5. Technology history: announced vs delivered

The timeline has 195 dated events across 16 company groups and 163 source URLs (repo [`company-timeline-events.csv`](../data/mission-2026-11-14/company-timeline-events.csv); repo [`announced-vs-delivered.csv`](../data/mission-2026-11-14/announced-vs-delivered.csv)). Of 39 announced capabilities: (repo [`announced-vs-delivered.csv`](../data/mission-2026-11-14/announced-vs-delivered.csv))

| Delivery status | Count |
|---|---|
| Evidence of delivery | 17 |
| Partial | 11 |
| No public evidence yet | 9 |
| Contradicted | 2 |

Re-checked 2026-11-19: 5 status changes, all upward (repo [`announced-vs-delivered-refresh-2026-11-19.csv`](../data/mission-2026-11-14/announced-vs-delivered-refresh-2026-11-19.csv)) [V wave 31B].

By company:
- **Daffy:** 5 of 5 delivered. ([Daffy MCP docs](https://docs.daffy.org/agents/mcp); [Daffy membership tier changes](https://help.daffy.org/en/articles/11730892-how-do-i-change-my-membership); repo [`announced-vs-delivered.csv`](../data/mission-2026-11-14/announced-vs-delivered.csv))
- **Chariot Disbursements:** the clearest beta-to-production trail ([Chariot Disbursements FAQ](https://docs.givechariot.com/guides/disbursements/faq); [Chariot partner profile: Daffy](https://www.givechariot.com/resources/insights/getting-to-know-daffy-a-chariot-disbursements-partner); repo [`announced-vs-delivered.csv`](../data/mission-2026-11-14/announced-vs-delivered.csv)).
- **TIFIN Give:** announces most often, and its Louise AI has only vendor evidence ([TIFIN Give Louise release](https://www.prnewswire.com/news-releases/tifin-give-launches-louise-ai-capabilities-for-philanthropy-302595069.html); repo [`announced-vs-delivered.csv`](../data/mission-2026-11-14/announced-vs-delivered.csv)).
- **Ren and Foundation Source:** broad claims (daily unitization, DAF OS) with little public delivery evidence ([Ren faith/community foundation page](https://www.reninc.com/faith-based-community-foundations/); [Foundation Source DAF OS brief](https://foundationsource.com/resources/product-briefs/the-modern-operating-system-for-donor-advised-funds/); repo [`announced-vs-delivered.csv`](../data/mission-2026-11-14/announced-vs-delivered.csv)).

**Private-equity ownership changes are followed fast by leadership change and roll-ups.** GTCR named a new CEO at Foundation Source six days after closing, followed by four acquisitions in about 17 months ([GTCR acquires Foundation Source](https://foundationsource.com/newsroom/press-releases/gtcr-announces-acquisition-of-foundation-source/); [Foundation Source press releases (CEO, PG Calc)](https://foundationsource.com/category/newsroom/press-releases/page/5/); [Foundation Source acquires PG Calc](https://foundationsource.com/newsroom/press-releases/foundation-source-announces-acquisition-of-pg-calc-leading-provider-of-planned-giving-solutions/); [Foundation Source acquires Vennfi](https://foundationsource.com/newsroom/press-releases/foundation-source-acquires-vennfi-the-fintech-powering-donor-advised-fund-charityvest/); [Foundation Source acquires Giving Place](https://foundationsource.com/newsroom/press-releases/foundation-source-acquires-giving-place-platform-for-private-foundations-and-family-offices/); [Pacific Foundation Services deal record](https://www.privsource.com/acquisitions/deal/n8S0zL); repo [`company-timeline-events.csv`](../data/mission-2026-11-14/company-timeline-events.csv)). Customer effects are unobserved: no repo source ties an ownership change to a sponsor-level fee or service change. [I] absence finding from [`private-equity-daf-ecosystem-map.md`](mission-2026-11-14/private-equity-daf-ecosystem-map.md) and [`company-timeline-events.csv`](../data/mission-2026-11-14/company-timeline-events.csv). [gap19-11]

**Ren's dates, scale claims and SOC 2 type drift over time.** (repo [`company-timeline-events.csv`](../data/mission-2026-11-14/company-timeline-events.csv)) SOC 2 is stated as "Type 2" in July 2025 and "Type 1" in April 2026, both in Ren's own boilerplate, and Bain Capital's July 2023 investment release says "Type 1"; no report has been seen and Ren publishes no trust page **[V; vendor claim]** ([Bain Capital/Ren release, Jul 2023](https://www.baincapital.com/news/ren-secures-strategic-growth-investment-led-bain-capital-tech-opportunities)) ([AEF/Ren release, Jul 2025](https://www.aefonline.org/thought-leadership/american-endowment-foundation-selects-ren-as-a-strategic-partner-to-expand-philanthropy-drive-innovation-and-foster-growth-in-financial-services/); [AEF/Ren release, Apr 2026](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/)).

Missing evidence is not treated as non-delivery. Source: [competitive histories](mission-2026-11-14/competitive-history-timelines.md).

---

## 6. Regulation

- **Proposed regulations:** the 2023 proposed §4966 regulations (REG-142338-07) are **neither final nor withdrawn** (Federal Register query, 2026-11-14) ([Federal Register 2023-24982 (proposed §4966 regs)](https://www.federalregister.gov/documents/2023/11/14/2023-24982/taxes-on-taxable-distributions-from-donor-advised-funds-under-section-4966); [Federal Register API query](https://www.federalregister.gov/api/v1/documents.json?conditions%5Bterm%5D=%22donor%20advised%20fund%22&conditions%5Bagencies%5D%5B%5D=internal-revenue-service&order=newest)). The comment period was extended to Feb 15, 2024 ([Federal Register 2024-00260](https://www.federalregister.gov/documents/2024/01/09/2024-00260/taxes-on-taxable-distributions-from-donor-advised-funds-under-section-4966); repo [`validation-register-wave2b.csv`](../data/mission-2026-11-14/validation-register-wave2b.csv)).
- **Guidance plan:** the 2026–27 Priority Guidance Plan (2026-09-29) reframes the project as "guidance under sections 4966 and 6033 regarding certain DAF arrangements" ([IRS 2026-2027 Priority Guidance Plan](https://www.irs.gov/pub/irs-counsel/2026-2027-initial-pgp.pdf); [ArentFox Schiff on 2026-27 PGP](https://www.afslaw.com/perspectives/alerts/irs-and-treasury-release-2026-2027-priority-guidance-plan-what-tax-exempt)).
- **The pending adviser question:** the proposal would treat a donor's personal investment adviser who manages DAF assets as a donor-advisor. This would affect the adviser-managed channel ([Federal Register 2023-24982 (proposed §4966 regs)](https://www.federalregister.gov/documents/2023/11/14/2023-24982/taxes-on-taxable-distributions-from-donor-advised-funds-under-section-4966); [Baker McKenzie on proposed DAF regs](https://www.globalcompliancenews.com/2024/06/01/https-insightplus-bakermckenzie-com-bm-tax-united-states-donor-fund-proposed-regulations_05172024/)).
- **OBBBA (2025):** excludes DAF gifts from the new nonitemizer deduction and adds a 0.5%-AGI floor and a 35% cap from 2026 ([IRS nonitemizer deduction reminder](https://www.irs.gov/newsroom/irs-reminder-permanent-charitable-contribution-deduction-begins-for-returns-filed-next-year-for-taxpayers-who-do-not-itemize); [Vanguard Charitable on OBBBA](https://www.vanguardcharitable.org/news/could-2025-budget-reconciliation-bill-impact-your-giving); [IRS Publication 505 (2026)](https://www.irs.gov/publications/p505)).
- **Not enacted:** the ACE Act; IRA-to-DAF QCD bills (introduced only); California AB 1712 (failed 2020) ([Steptoe on the ACE Act](https://www.steptoe.com/en/news-publications/senators-king-and-grassley-introduce-daf-and-private-foundation-reform-legislation.html); [Rep. Smith QCD-to-DAF bill release](https://adriansmith.house.gov/media/press-releases/smith-panetta-introduce-bipartisan-bill-support-charitable-giving); [Sen. Young QCD-to-DAF bill release](https://www.young.senate.gov/?p=13549); [LegiScan CA AB 1712](https://legiscan.com/CA/bill/AB1712/2019)).
- **No DAF-specific SEC or FINRA rule found.** ([Reed Smith on SEC 2026 focus](https://www.reedsmith.com/articles/private-equity-behind-the-scenes/sec-sets-the-tone-for-2026-regulatory-focus-on-investment-managers/); repo [`regulatory-status-tracker.csv`](../data/mission-2026-11-14/regulatory-status-tracker.csv)) The SEC withdrew its predictive-analytics conflicts proposal (2025-06-12) ([Alston & Bird on SEC withdrawals](https://www.alston.com/en/insights/publications/2025/06/sec-withdraws-multiple-rule-proposals)).

Tracker: `data/mission-2026-11-14/regulatory-status-tracker.csv`.

---

## 7. AI in DAF operations

**Adoption.**
- 30 use cases were inventoried, with 2 more (Bonterra) identified by red team ([Bonterra Que release](https://www.businesswire.com/news/home/20251001579571/en/Bonterra-Launches-Que-The-First-Agentic-AI-Platform-for-Funders-Nonprofits-and-Supporters); repo [`ai-use-case-inventory.csv`](../data/mission-2026-11-14/ai-use-case-inventory.csv); repo [`validation-register-wave2a.csv`](../data/mission-2026-11-14/validation-register-wave2a.csv)).
- 10 are DAF-direct: 6 announced, 1 demonstrated, 2 deployed with evidence, 1 unverified (repo [`ai-use-case-inventory.csv`](../data/mission-2026-11-14/ai-use-case-inventory.csv)).
- **There is no public evidence of AI in sponsor-side approval or eligibility determination** (an absence finding; on 2026-11-19 the grant-review and privacy pages of Fidelity Charitable, Vanguard Charitable and NPT disclosed no AI or automated grant review; DAFgiving360 was not checked). (repo [`ai-use-case-inventory.csv`](../data/mission-2026-11-14/ai-use-case-inventory.csv); repo [`validation-register-wave2a.csv`](../data/mission-2026-11-14/validation-register-wave2a.csv)) The one sponsor-side exception is Daffy's announced charity-data flagging **[RT]** ([FF News on Daffy AI](https://ffnews.com/newsarticle/paytech/daffy-is-using-ai-to-reshape-the-future-of-charitable-giving/)).
- The agentic frontier is donor-side: TIFIN Give's Louise executes donor requests, and Daffy's MCP server exposes `make_donation` with no documented limits **[V]** ([TIFIN Give Louise release](https://www.prnewswire.com/news-releases/tifin-give-launches-louise-ai-capabilities-for-philanthropy-302595069.html); [Daffy MCP docs](https://docs.daffy.org/agents/mcp)).

**Economics** ([AI economics](mission-2026-11-14/ai-economics-replacement-analysis.md), with red-team corrections):
- Inference cost is immaterial: about $0.45 per heavy document review against about $83 of reviewer time **[V]** ([Anthropic API pricing](https://platform.claude.com/docs/en/about-claude/pricing); [BLS compliance officers (May 2025)](https://www.bls.gov/ooh/business-and-financial/compliance-officers.htm); [BLS ECEC June 2026](https://www.bls.gov/news.release/ecec.nr0.htm); repo [`ai-process-economics.csv`](../data/mission-2026-11-14/ai-process-economics.csv)).
- The model's result that "AI on the existing workflow ranks last in 16/16 processes" is **determined by its assumptions**, not by evidence about AI **[RT]** (repo [`ai-process-economics.csv`](../data/mission-2026-11-14/ai-process-economics.csv); repo [`validation-register-wave2a.csv`](../data/mission-2026-11-14/validation-register-wave2a.csv); repo [`red-team-wave2a-ai-and-entrant.md`](../research/mission-2026-11-14/red-team-wave2a-ai-and-entrant.md)).
- What is reasoned rather than modelled: redesign removes exception classes, while AI only shortens handling. AI economics clear plausible governance costs at vendor or network scale, not per process per sponsor. [I] inference from [`ai-economics-replacement-analysis.md`](mission-2026-11-14/ai-economics-replacement-analysis.md) (redesign mechanism) and [`ai-economics-v2-observed-costs.md`](mission-2026-11-14/ai-economics-v2-observed-costs.md) (the buyer is an administrator or platform). Calibrated to 21 published studies, the ranking is unchanged and the large-national AI value pool falls to $445k (repo [`gap19-ai-calibration.md`](mission-2026-11-14/gap19-ai-calibration.md); [V wave 31A]). [gap19-11]
- The single most important missing evidence is a measured exception, handling-time and QA study at any sponsor. [I] inference from [`ai-economics-replacement-analysis.md`](mission-2026-11-14/ai-economics-replacement-analysis.md) (no sponsor publishes human effort or exception rates) and [`gap19-exception-load-proxy.md`](mission-2026-11-14/gap19-exception-load-proxy.md) §5 (Q-N03 still open). [gap19-11]

**Governance** ([AI failure modes](mission-2026-11-14/ai-governance-failure-modes.md)):
- **Accountability:** liability attaches to the sponsor and to knowing fund managers ([26 U.S.C. §4966](https://www.law.cornell.edu/uscode/text/26/4966); [26 U.S.C. §4967](https://www.law.cornell.edu/uscode/text/26/4967)), so approval authority must stay human or deterministic.
- **The control rule:** **AI may add a flag, never clear one.** This converts the gravest failure, a missed sanctions or prohibited-benefit case, from risk created to risk reduced. (repo [`ai-governance-failure-modes.md`](../research/mission-2026-11-14/ai-governance-failure-modes.md))
- **Rubric rating** (not observed incidents): unconstrained AI creates risk in 13 of 16 failure modes and redistributes it in 3 (repo [`ai-failure-mode-register.csv`](../data/mission-2026-11-14/ai-failure-mode-register.csv); repo [`validation-register-wave2a.csv`](../data/mission-2026-11-14/validation-register-wave2a.csv)).

---

## 8. Entry strategy for an AI-native provider

From [entrant simulation](mission-2026-11-14/ai-native-entrant-simulation.md), red-teamed:
- **What not to build:** a sponsoring charity, custody, payment rails, charity master data or a full system-of-record. Each can be partnered: sponsor-of-record APIs (Endaoment; Daffy for Developers), Chariot, custodians, and IRS bulk data ([Endaoment institutions page](https://endaoment.org/institutions); [Daffy for Developers](https://www.daffy.org/resources/daffy-for-developers); [Chariot Disbursements FAQ](https://docs.givechariot.com/guides/disbursements/faq); [IRS TEOS bulk data downloads](https://www.irs.gov/charities-non-profits/tax-exempt-organization-search-bulk-data-downloads)).
- **The cheapest probe:** Strategy 3, an AI-native operating layer over existing sponsors with exception-only routing under **deterministic sponsor rules** plus continuous eligibility monitoring.
  - **[RT]** It is a **conditional probe, not a recommendation.** At $120k/yr it needs about 76k–369k grants/yr per customer to break even, which most independent and community-foundation sponsors lack ([Charityvest 2025 results release](https://foundationsource.com/newsroom/press-releases/charityvest-reports-record-2025-charitable-giving-more-than-doubling-contributions-and-grants/); [Fidelity Charitable 2026 Giving Report](https://www.fidelitycharitable.org/insights/2026-giving-report.html); [Anthropic API pricing](https://platform.claude.com/docs/en/about-claude/pricing); [BLS compliance officers (May 2025)](https://www.bls.gov/ooh/business-and-financial/compliance-officers.htm); repo [`entry-strategy-comparison.csv`](../data/mission-2026-11-14/entry-strategy-comparison.csv); repo [`ai-process-economics.csv`](../data/mission-2026-11-14/ai-process-economics.csv); repo [`validation-register-wave2a.csv`](../data/mission-2026-11-14/validation-register-wave2a.csv)).
  - Its capital advantage is a headcount assumption: it needs about 42 customers for $5m ARR against 5 for a full platform ([Endaoment institutions page](https://endaoment.org/institutions); repo [`entry-strategy-comparison.csv`](../data/mission-2026-11-14/entry-strategy-comparison.csv); repo [`validation-register-wave2a.csv`](../data/mission-2026-11-14/validation-register-wave2a.csv)).
- **Gating question:** do sponsor–vendor contracts grant API and data-export rights? [I] inference from [`ai-native-entrant-simulation.md`](mission-2026-11-14/ai-native-entrant-simulation.md) (risk 1); open as Q-N04 in [`FINAL-STATUS.md`](mission-2026-11-14/FINAL-STATUS.md). [gap19-11] **Round-2 answer (partial):** public vendor templates allow batch export but not live integration, no top-10 sponsor publishes a donor-side export, and several sponsor terms bar credential sharing or automation (§11.4). Executed contracts remain unseen.

---

## 9. Evidence quality, validation and limits

**Independent validation and red-team review** checked **80 consequential claims** in waves 1–2B. Later waves bring the registers to 1,036 rows through wave 32B, in 37 files with 1,012 distinct claim IDs (table below; [C] counted by leading result word over `data/mission-2026-11-14/validation-register*.csv`; method in [gap19-11-consistency-pass.md](mission-2026-11-14/gap19-11-consistency-pass.md) §1, caveat in §4; [V wave 33B]) [gap19-11] (repo [`validation-register.csv`](../data/mission-2026-11-14/validation-register.csv); repo [`validation-register-wave2a.csv`](../data/mission-2026-11-14/validation-register-wave2a.csv); repo [`validation-register-wave2b.csv`](../data/mission-2026-11-14/validation-register-wave2b.csv)). These were done by agents that did not author the work and were not given the original conclusions.

| Result | Waves 1–2B | All registers through wave 32B [C] |
|---|---|---|
| Confirmed | 45 | 784 |
| Partially confirmed | 25 | 195 |
| Contradicted | 7 | 32 |
| Unable to verify | 3 | 15 |
| Other (audit-defect notes, "supported", "plausible", "passed") | 0 | 10 |
| **Rows** | **80** | **1,036** [gap19-11] |

Model arithmetic, the DAFRC recomputation and 6 hand-checked derived metrics reproduced exactly ([DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`validation-register-wave2a.csv`](../data/mission-2026-11-14/validation-register-wave2a.csv); repo [`validation-register-wave2b.csv`](../data/mission-2026-11-14/validation-register-wave2b.csv)). Corrections were appended to source documents as dated, governing sections; no original text was deleted.

**Limits.**
- All evidence is public-source. No vendor tests, sponsor interviews or contracts were obtained (repo [`FINAL-STATUS.md`](mission-2026-11-14/FINAL-STATUS.md), limits). [gap19-11]
- The shared web-search budget ran out during the mission. Some items rest on direct fetches or search summaries and are flagged. (repo [`regulation-market-structure-portability.md`](../research/mission-2026-11-14/regulation-market-structure-portability.md); repo [`breadth-community-faith-infrastructure-emerging.md`](../research/mission-2026-11-14/breadth-community-faith-infrastructure-emerging.md))
- Wayback Machine page content could not be retrieved from this environment. Only the archive.org availability API worked, so an archived link shows that a capture exists, not what it says (repo [`competitive-history-timelines.md`](mission-2026-11-14/competitive-history-timelines.md); [`FINAL-STATUS.md`](mission-2026-11-14/FINAL-STATUS.md), limits). [gap19-11]
- The coverage matrix measures depth on a purposive set of 33 entities, not the about-1,500-sponsor universe ([DAFRC Annual DAF Report page](https://www.dafresearchcollaborative.org/research/annual-daf-report); repo [`coverage-matrix-entities.csv`](../data/mission-2026-11-14/coverage-matrix-entities.csv)).

**Evidence that would most change this report:**
1. A sponsor time-and-motion study.
2. Ren's denominator for its share claims.
3. Give Interactive's scope at Vanguard Charitable.
4. Sponsor–vendor API and data-export clauses.
5. Fund-level payout by fee model.
6. Final §4966/6033 guidance.

Round 2 partly answered items 2–4: Ren's footprint is measured several ways (§3), Give Interactive appears to be Vanguard Charitable's ledger only (§11.2), and public API and export terms are mapped (§11.4). Validation waves 3–32B are reported per wave (`research/mission-2026-11-14/validation-wave*-report.md`) and listed in §11. [gap19-11] See [synthesis §F](mission-2026-11-14/strategic-synthesis.md) and the [research queue](../data/mission-2026-11-14/research-priority-queue.csv).

---

## 10. DAF Evidence Quadrants (consensus, 2026-11-14)

This is the repository's own evidence-scored positioning method. It is **not** a Gartner Magic Quadrant, and no analyst firm publishes one for DAF platforms ([analyst landscape](mission-2026-11-14/analyst-and-education-landscape.md)).
- **Method:** [evidence-quadrant-methodology.md](mission-2026-11-14/evidence-quadrant-methodology.md).
- **Two blind scorers plus adjudication:** [quadrant-calibration.md](mission-2026-11-14/quadrant-calibration.md).
- **Positions:** `data/mission-2026-11-14/quadrant-positions.csv` (rows with scorer = consensus).
- **Charts:** `mission-2026-11-14/quadrants/A1-consensus.svg` … `A5-consensus.svg`.

**Calibration statistics.**
- 305 cells were scored by both scorers: 67% matched exactly and 99.7% were within 1 point.
- Of 43 providers, 18 positions were reproduced by both scorers and 18 were adjudicated. The other 7 have insufficient evidence.
- Every position is *internal-demonstration* under the EDF claim policy. "(b)" marks a boundary position: the point estimate is within 0.25 of a midline.

| Area | Proven Leaders | Scale Operators | Forward Builders | Focused Specialists | Insufficient evidence |
|---|---|---|---|---|---|
| A1 Platform & administration | Ren; Give Interactive (b); Foundation Source (b) | Fidelity in-house; NPT GivingPoint*; TIFIN Give (b); Foundant (b) | Blackbaud FE NXT (b) | Givinga; NPact | NCF; SVCF |
| A2 Disbursement rails | Chariot Disbursements; PayPal Grant Payments; Chariot DAFpay (b); Ren RDE (b); Every.org (b) | Fidelity EFT (b) | — | DAF Direct | — |
| A3 Adviser-channel sponsors | DAFgiving360 (b); RCF (b); Charityvest (b) | Fidelity Charitable; AEF; NPT (b); Vanguard Charitable (b); GiveClear (b) | — | — | GS PF; MS GIFT; BofA CGF; NCF |
| A4 Consumer sponsors | Daffy; DAFgiving360 (b); Endaoment (b); Charityvest (b) | Fidelity Charitable | Every.org (b) | — | Givinga |
| A5 Eligibility data | IRS baseline; Candid; Goodstack; Benevity (b); Chariot verification (b) | — | — | — | — |

\*NPT GivingPoint is Ren-built and Ren-hosted on wave-3 evidence. Its row is mis-scoped and should be merged into Ren at the next re-score.

**v1.1 re-score (fresh scorer under the tightened rules; [quadrant-v11-rescore.md](mission-2026-11-14/quadrant-v11-rescore.md)).** 30 of 42 providers keep their v1.0 consensus quadrant. Of the 12 that move, 7 sit on a midline in both versions. The 5 substantive changes:
- **DAFgiving360 (A3/A4) → Scale Operators.** Its DAFpay evidence now belongs to the vendor, it documents only inbound transfers, and the only rail it documents is the mailed check.
- **NPT (A3) → insufficient evidence.** GivingPoint was merged into Ren, and its 2-page summary statements score U on assurance.
- **Ren Rapid Disbursement Engine → insufficient evidence.** Nothing public covers the engine's API, controls or portability.
- **Givinga (A1) → insufficient evidence.**
- **Fidelity → Proven Leaders (boundary).** This rests on the scorer's reading, not new evidence, so treat it as unresolved.

New evidence: GiveClear's audited CY2024 statements (Capin Crouse), which carry an unmodified opinion dated 2025-11-06 (repo [`quadrant-v11-rescore.md`](mission-2026-11-14/quadrant-v11-rescore.md)). [gap19-11]

The v1.1 AI overlay has no GREEN providers:
- **RED (provisional):** Benevity Match Assurance.
- **AMBER (near red):** TIFIN Give/GiveClear Louise.
- **AMBER:** Daffy MCP, Chariot, Foundant, Blackbaud, Goodstack, and Candid (low).

**v1.1 consensus: the current reference** ([quadrant-v11-blind-and-calibration.md](mission-2026-11-14/quadrant-v11-blind-and-calibration.md)).

A blind second scorer under v1.1 matched the fresh scorer exactly on 74% of commonly scored cells and within 1 point on 99.7%. 22 of the 28 providers that both scorers could plot landed in the same quadrant (79%) (repo [`quadrant-v11-blind-and-calibration.md`](mission-2026-11-14/quadrant-v11-blind-and-calibration.md), provider-level table). [gap19-11] Final status: 22 reproduced, 11 adjudicated, 9 insufficient evidence. This table **supersedes the v1.0 table above**, which is retained for history.

| Area | Proven Leaders | Scale Operators | Forward Builders | Focused Specialists | Insufficient evidence |
|---|---|---|---|---|---|
| A1 Platform & administration | Foundation Source; Ren (b); Fidelity in-house (b); Foundant (b); Blackbaud FE NXT (b) | TIFIN Give | Give Interactive (b) | NPact | Givinga; NCF; SVCF |
| A2 Disbursement rails | Chariot Disbursements; Chariot DAFpay; PayPal Grant Payments; Every.org (b) | Fidelity EFT (b); Ren RDE (b) | — | DAF Direct | — |
| A3 Adviser-channel sponsors | Charityvest; Fidelity Charitable (b); RCF (b); Vanguard Charitable (b) | AEF; DAFgiving360; GiveClear (b) | — | — | GS PF; MS GIFT; BofA CGF; NCF; NPT |
| A4 Consumer sponsors | Daffy; Charityvest; Fidelity Charitable (b) | DAFgiving360 | Every.org; Endaoment (b) | — | Givinga |
| A5 Eligibility data | IRS baseline; Candid; Chariot verification; Benevity; Goodstack (b) | — | — | — | — |

**v1.1 AI overlay.** No provider is GREEN.
- **RED (provisional):** Benevity. Its AI auto-submits match requests with no documented approval step.
- **AMBER, near red:** TIFIN Give/GiveClear.
- **AMBER:** Chariot, Daffy, Blackbaud, Foundant, Goodstack.
- **AMBER (low):** Candid.
- **Inform-only:** Fidelity.

**Main movers from v1.0 to v1.1 and why.**
- **DAFgiving360 → Scale Operators.** The vendor's evidence no longer counts toward the sponsor, and it documents only inbound transfers and check payments.
- **NPT → insufficient evidence.** GivingPoint was merged into Ren, and its summary statements do not count as an audit.
- **Ren → boundary.** It absorbed the NPT evidence, but its SOC statements contradict each other.
- **Give Interactive → Forward Builders (boundary).**

**v1.2 targeted update (bank programs and NCF; [quadrant-v12-targeted-rescore.md](mission-2026-11-14/quadrant-v12-targeted-rescore.md); evidence validated in [wave 6](mission-2026-11-14/validation-wave6-report.md)).** Public program terms were found for Morgan Stanley GIFT, BofA CGF and NCF, which lets these providers be placed:

| Provider | v1.1 | v1.2 (X / Y) |
|---|---|---|
| BofA Charitable Gift Fund (A3) | insufficient evidence | **Scale Operators** (2.47 / 1.18) |
| Morgan Stanley GIFT (A3) | insufficient evidence | **Scale Operators** (2.76 / 1.33) |
| NCF (A3) | insufficient evidence | **Proven Leaders**, effectively boundary (2.80 / 2.42) |
| NCF platform (A1) | insufficient evidence | **Proven Leaders (boundary)** |
| Goldman Sachs PF (A3) | insufficient evidence | still insufficient evidence |

On Goldman Sachs PF, wave 6 found that its 2012 and 2017 circulars are also public. All of them state check payment, so a further re-score could place it.

AI overlay: MS GIFT is AMBER (provisional), because its "automated" vetting has undocumented controls. Its board still approves every grant.

Caveat: both scoring passes were run by one agent, so independence is weaker than the five-area calibrations.

**What the quadrants show.**
- **Most providers sit near the midlines.** Forward-capability evidence (data export, SOC scope, portability terms) is the scarcest input, so the uncertainty bands are wide.
- **The bank-affiliated programs are opaque.** Under v1.0–v1.1, Goldman, Morgan Stanley GIFT and BofA CGF could not be placed on public evidence. The v1.2 update places MS GIFT and BofA CGF as Scale Operators; Goldman Sachs PF remains insufficient evidence.
- **Large incumbents** (Fidelity, NPT, Vanguard, AEF) score high on execution and low on openness and portability.
- **Challengers and infrastructure** (Daffy, Endaoment, Chariot) score higher on forward capability.

**AI-governance overlay (v1.0; superseded by the v1.1 overlay above, retained for history).**
- **AMBER (high):** TIFIN Give's Louise. It acts on donor requests with no published controls, but GiveClear still approves every grant.
- **AMBER:** Daffy. Its MCP server exposes a donation tool with no documented limits.
- **Watch:** Benevity. Its AI auto-submits, and oversight is undocumented.

**What would move positions.**
- Published SOC report scopes.
- Data-export clauses in executed contracts.
- Outbound transfer terms.
- Measured grant timing.
- Bank-program disclosures.

The open questions behind each are in the research queue (`P-QCAL-*`).

---

## 11. Round-2 findings: thematic consolidation (validated through wave 12)

This section consolidates the round-2 workstreams (failures, complaints, buyers, payments, contracts, mortality, vendors, ledgers, fees, credit, agentic controls). It was reorganised by theme on 2026-11-15. It replaces the earlier chronological, batch-by-batch list, which is preserved verbatim in [the pre-consolidation archive](mission-2026-11-14/archive/DAF-INDUSTRY-REPORT-2026-11.pre-consolidation.md).

- **Traceability.** Each item links its workstream, and every workstream carries inline primary-source citations.
- **Corrections.** Validation waves 4–12 appended governing corrections to each workstream. Where a later wave corrected a figure, only the corrected figure appears here. Superseded figures and their replacements are listed in the [consolidation changelog](mission-2026-11-14/consolidation-changelog.md).
- **Validation reports:** [wave 8](mission-2026-11-14/validation-wave8-report.md) (batch 23), [wave 9](mission-2026-11-14/validation-wave9-report.md) (batch 24), [wave 10](mission-2026-11-14/validation-wave10-report.md) (batch 25), [wave 11](mission-2026-11-14/validation-wave11-report.md) (batch 26), [wave 12](mission-2026-11-14/validation-wave12-report.md) (batch 27). Earlier waves (3–7) are linked from the workstreams they corrected.

### 11.1 Market structure and data quality

**Sponsor cost structure from Form 990** ([sponsor-cost-structure-and-sensitivities.md](mission-2026-11-14/sponsor-cost-structure-and-sensitivities.md); 5,272 returns, full Part IX)
- **DAF-allocated operating cost (latest 990s, fiscal years ending Jun 2024/25)** is about $2.1–2.8bn, or 67–89 bps of DAF assets depending on allocation. Excluded: investment fees and university/hospital foundations.
- **By sponsor type:** standard nationals run at about 25–32 bps and community foundations at about 127–177 bps.
- **Cost per grant:** Fidelity about $68, DAFgiving360 $55, Vanguard $134, NPT $419 [V wave 5]. Fidelity's figure includes its charitable-investment-advisor program and taxes; without them it is about $59, and against a period-matched grant count it is about $71 (wave-5 governing note).
- **Scale economies are strong:** cost elasticity to scale is 0.41 for nationals and 0.84 for community foundations.

**Sensitivity of the market statistics** (same workstream)
- Excluding Givinga drops the processor share of accounts from 80.5/77.4/79.5% (FY2022/23/24) to 63.0/67.0/66.0% (59.2% for FY2024 on corrected data) (repo [`sponsor-cost-structure-and-sensitivities.md`](mission-2026-11-14/sponsor-cost-structure-and-sensitivities.md) item 5; [V wave 5]). [gap19-11]
- FY2022 account growth flips from +72% to −7%.
- Givinga's account unit is undefined [V wave 5]. In CY2022 its largest fundraiser was a charity sweepstakes operator, so game or app-user records are one candidate explanation and employer-provisioned employee accounts are another. Neither is confirmed, and the count fell in 2023 and rose by 465k in 2024 with no named fundraiser.
- Recommendation: exclude SDG Impact Fund from market totals and footnote it.
- Corrected FY2024 totals ($323.27bn) are in §1.

**Payout net of DAF-to-DAF transfers** ([queue-net-payout-fidelity-outliers.md](mission-2026-11-14/queue-net-payout-fidelity-outliers.md); `scripts/mission_net_payout.py`) [V wave 11]
- Scope: FY2021–24 pooled, sponsors with itemised Schedule I, excluding processors (n = 3,373 sponsor-years).
- Gross payout is 23.9%. Net payout is 21.5%, 20.8% or 19.0%, depending on how widely sponsor-to-sponsor transfers are defined (repo [`queue-net-payout-fidelity-outliers.md`](mission-2026-11-14/queue-net-payout-fidelity-outliers.md), segment table; [V wave 11]). [gap19-11]
- Nationals fall from 23.8% gross to 20.9% net.
- 12.1% of national sponsors' DAF grants go to other national sponsors.

**Large sponsor-to-sponsor flows** ([queue-vendor-channel-moves.md](mission-2026-11-14/queue-vendor-channel-moves.md))
- DAFgiving360's $976.6m FY2025 grant line to Fidelity Charitable cannot be attributed from public data, because Fidelity's Schedule B is redacted. A few very large account moves is the best reading (inference).
- Fidelity's CY2025 outlier grants and post-SPLC flows are in §11.8.

**Analyst and education coverage** ([analyst-and-education-landscape.md](mission-2026-11-14/analyst-and-education-landscape.md))
- No analyst firm covers DAF platforms: no Gartner MQ or Hype Cycle, no Forrester Wave, and no coverage from IDC, Celent or Datos.
- Curricula, including the new DAFCP credential, repeat the aggregate 25.2% payout framing.
- New adviser data: 35% of advisers recommend DAFs most or all of the time (DAFRC 2026, n=669) [V].

### 11.2 Vendors and platform shifts

**Ren footprint and scope** ([vendor scope](mission-2026-11-14/queue-vendor-scope-ren-denominator.md); share figures in §1 and §3)
- Goldman's DAFs and NPT's GivingPoint run on Ren technology [V].
- Headline shares: about 28% of FY2024 DAF assets on Ren technology in some form [V wave 3], or 32.2% as a floor on any confirmed Ren/Stellar link in the consolidated graph (repo [`gap19-graph-consolidation.md`](mission-2026-11-14/gap19-graph-consolidation.md) §4; [V wave 31A]); [gap19-11] 9.2% at sponsors naming Ren/Stellar in their latest 990 (14.8% in any FY2022–25 return); about 5% on Ren-paid administration.

**NPT GivingPoint is a Ren white-label book** ([queue-npt-givingpoint-fidelity-stack.md](mission-2026-11-14/queue-npt-givingpoint-fidelity-stack.md)) [V wave 12]
- 13 live program sites run on the same Ren build and carry NPT or NPT UK sponsor text: J.P. Morgan Charitable Gift Fund, UBS, BMO, Glenmede, Tolleson, Pitcairn, NPT UK, NPT Transatlantic, Rathbones, Cazenove Capital and others.
- Eight sit on Ren's load balancer. The rest are on an AWS Global Accelerator pair, attributed to Ren by inference.
- NPT's payment to Ren is undisclosed. No Ren, Stellar or iPhi payee appears, and the fee most likely sits in the $5.87m IT line (+$2.22m).
- Ren is NPT's technology and hosting vendor, not its administrator.
- NPT, J.P. Morgan and ICGF iPhi hosts now redirect to Ren-hosted GivingPoint sites naming NPT as sponsor ([queue-ren-iphi-attrition.md](mission-2026-11-14/queue-ren-iphi-attrition.md)) [V wave 11].

**Ren iPhi attrition, 2023–Nov 2026** ([queue-ren-iphi-attrition.md](mission-2026-11-14/queue-ren-iphi-attrition.md); `scripts/mission_ren_iphi_attrition.py`) [V wave 11]
- 6 of 57 sponsors left, or 10.5% (Wilson interval 4.9–21.1%) (repo [`queue-ren-iphi-attrition.md`](mission-2026-11-14/queue-ren-iphi-attrition.md) item 1). The FY2025 filings show no Ren attrition so far: 10 sponsors name a Ren entity ($3.35m), and all 8 comparable FY2024 payers name Ren again. The largest Ren clients (MS GIFT, RCF, US Charitable Gift Trust, NCF) have not yet filed FY2025 (repo [`gap19-fy2025-refresh.md`](mission-2026-11-14/gap19-fy2025-refresh.md); [V wave 31A]). [V wave 33B] [gap19-11] The strict rate is 8.8%, because Gulf Coast's move is still "launching soon".
- Exits are concentrated May 2025–Jun 2026.
- Community foundations are hit hardest: 5 of 28 left.
- Destinations: Foundant 4, akoyaGO 1, Give Interactive 1.
- Separately, the migration census found that Ren iPhi lost 4 of 8 flagged foundations in 2025–26 [V wave 10].

**All six dated community-foundation portal switches end on Foundant (Yakima, undated, went to akoyaGO)** ([queue-bdc-coverage-migrations-goodstack.md](mission-2026-11-14/queue-bdc-coverage-migrations-goodstack.md)) [V wave 10]
- From Ren iPhi: Arkansas (instructions emailed 2026-06-01), Flint (about 2026, weakly dated), Acadiana (2025).
- From Blackbaud: Winston-Salem (2024).
- From donor-portal.org: Indian River (2023).

**Give Interactive: a third white-label stack, owned by a sponsor's trust** ([Give displacement](mission-2026-11-14/queue-give-interactive-displacement.md))
- The Signatry's trust controls Give Interactive (99%) [V]. Give Interactive is Vanguard Charitable's ledger vendor.
- Two Ren clients have completed migrations to it (WaterStone, The Signatry). About $5.9bn of Ren-paying assets are at risk.
- Give Interactive has no live community-foundation portals ([queue-cf-vendor-map.md](mission-2026-11-14/queue-cf-vendor-map.md)).
- At Chicago Community Trust, GiftingNetwork was the documented front end by Feb 2024, before Give's CCT production host (Jun 2025). The Dec 2025 portal refresh fits continued GiftingNetwork incumbency; Give's role at CCT remains unclear ([queue-vendor-channel-moves.md](mission-2026-11-14/queue-vendor-channel-moves.md), wave-6 governing note).

**Fidelity Charitable stack** ([queue-npt-givingpoint-fidelity-stack.md](mission-2026-11-14/queue-npt-givingpoint-fidelity-stack.md)) [V wave 12]
- FMR provides record-keeping, systems and administration. The 990 shows $0 IT and no employees, and there is no Ren marker.

**Community-foundation portal vendors (803 foundations)** ([queue-cf-vendor-map.md](mission-2026-11-14/queue-cf-vendor-map.md); `scripts/mission_cf_vendor_map.py`) [V wave 9]
- Coverage: 481 of 803 foundations mapped, holding 90.5% of community-foundation DAF assets. A 15-row spot-check found 0/15 vendor errors.
- By count: Foundant CommunitySuite runs 361 foundations (45%).
- By assets: Foundant holds 32.7%, Salesforce 23.7% (19 foundations), GiftingNetwork 11.5% (2) and Ren/Stellar iPhi 5.9% (22).
- Three foundations migrated from Stellar to Foundant (likely 2025–26).
- Portal does not equal ledger: about 43% of mapped assets sit behind portal-only front ends.

Donor-portal vendors at the top 40 by FY2024 DAF assets ([queue-community-foundation-rails-portals.md](mission-2026-11-14/queue-community-foundation-rails-portals.md)) [V wave 7]:

| Portal vendor | Foundations |
|---|---|
| Foundant CommunitySuite | 13 |
| Salesforce | 6 |
| Ren/Stellar iPhi | 5 |
| NPact (Foundation Cloud on spectrumportal.net; NPact attribution from third-party sources) | 3 |
| GiftingNetwork | 2 (CCT, FFTC) |
| One each: DonorSphere, Blackbaud NetCommunity, SmartSimple, Akoya, Power Pages | 5 |

**Channel moves** ([queue-vendor-channel-moves.md](mission-2026-11-14/queue-vendor-channel-moves.md))
- The Commonwealth Charitable Fund is unchanged on LPL's conversion day. Its circular confirms RCF as sponsor and RenPSG as administrator [V].
- Foundation for the Carolinas and Chicago Community Trust run "Powered by GiftingNetwork" portals [V].

**Ledgers behind the portals**
- **Named ledgers at portal-only foundations** ([queue-ledgers-behind-portals.md](mission-2026-11-14/queue-ledgers-behind-portals.md)) [V wave 10]: named for only 3 of the 29 portal-only community foundations. These are Sage Intacct at CF Northeast Florida, Fund 360 on Salesforce at Maine CF (Accounting Seed underneath not confirmed for Maine), and GKCCF's own platform. Arizona CF moved from Blackbaud FIMS to Sage Intacct + Salesforce.
- **Salesforce-centred ledger segment** ([queue-ledger-segment-npact-owner.md](mission-2026-11-14/queue-ledger-segment-npact-owner.md)) [V wave 12]:
  - Named at 11 sponsors holding $3.5bn (Fund 360/Accounting Seed; Sage Intacct + Salesforce). NetSuite is now confirmed at SVCF ($9.58bn, with NPact FIT; vendor case study, medium-high) and Pittsburgh ($0.53bn, with Salesforce; high). NCF ($5.46bn) is unresolved [V wave 13].
  - Moves off FIMS are confirmed at Arizona, Vermont and JCF San Diego.
  - The NYCT and California CF ledger readings rest only on job-posting skills (weak).
- **Other back-office facts** ([queue-ledgers-behind-portals.md](mission-2026-11-14/queue-ledgers-behind-portals.md)) [V wave 10]: donor-portal.org is run by GKCCF/Greater Horizons. Northeast Retirement Services is owned by Community Financial System.
- **DonorSphere** ([queue-donor-export-cf-payments-donorsphere.md](mission-2026-11-14/queue-donor-export-cf-payments-donorsphere.md)) [V wave 8]: built by FidTech Partners (Stamford, CT) and used by Greater Houston CF, Hawaii CF, FJC and the Jewish Federation of Greater Pittsburgh.
- **NPact ownership** ([queue-adviser-fees-pools-npact.md](mission-2026-11-14/queue-adviser-fees-pools-npact.md) [V wave 11]; [queue-ledger-segment-npact-owner.md](mission-2026-11-14/queue-ledger-segment-npact-owner.md) [V wave 12]):
  - NPact's SaaS terms name Fusion Laboratories as manufacturer [V wave 10].
  - BroadWest bought Fusion Labs in Dec 2020, and the company was later renamed NPact.
  - Fusion paid about $6.4m for FIMS/DonorCentral (2022).
  - The current owner is unconfirmed; Cambria Group lists NPact as a portfolio company. BroadWest's Texas status is not active (right to transact not established), contrary to the agent's reading.

**Assurance** ([queue-assurance-everyorg-givinga-monitoring.md](mission-2026-11-14/queue-assurance-everyorg-givinga-monitoring.md))
- None of 13 vendors publishes a SOC report with period and system scope [V wave 5].
- Ren's statements alternate between Type 2 and Type 1.

### 11.3 Payments and nonprofit-side economics

**Grant payment policy** ([queue-payment-rails-cluster.md](mission-2026-11-14/queue-payment-rails-cluster.md); [queue-nonprofit-side-panel.md](mission-2026-11-14/queue-nonprofit-side-panel.md))
- Fidelity's EFT-only policy is **not in effect**. Its 2026 Giving Report states 67% of grants go by EFT [V], and unenrolled charities still receive checks.
- No sponsor checked requires EFT today; Fidelity is "transitioning" to it [V wave 12].
- No sponsor publishes a grant-timing SLA. Checks are voided or returned at 90 days.
- NPT and Vanguard still use PayPal Grant Payments, and NPT does not pay by ACH [V wave 12].

2026 EFT providers by sponsor ([queue-bank-programs-and-eft-providers.md](mission-2026-11-14/queue-bank-programs-and-eft-providers.md), with wave-6 corrections):

| Rail | Sponsors |
|---|---|
| PayPal Grant Payments | NPT (up to $250k); Vanguard (up to $10m) |
| Chariot | Daffy; TIFIN Give; Charityvest (transitioning from Aug 2026); seven community foundations |
| Stripe plus own ACH | Fidelity |
| Own or administrator ACH | AEF (via Ren), NCF, three community foundations |
| Check only | BofA; DAFgiving360 (per its 2024 policies) |

Grant-payment rails at the top 30 community foundations ([queue-community-foundation-rails-portals.md](mission-2026-11-14/queue-community-foundation-rails-portals.md)) [V wave 7]:

| Rail | Foundations |
|---|---|
| Own ACH, no provider named | 10 (Seattle makes ACH mandatory from 2026-06-30) |
| Named third party | 2: Chariot at Saint Paul & Minnesota; Bill.com at Greater Atlanta |
| Checks only documented (DAF grants) | 2: Chicago Community Trust; New Hampshire, via Citizens Bank's Checkmint |
| Nothing published | 15 |

- None of the 30 uses PayPal Grant Payments or Ren ACH.
- Outside the top 30, Greater Washington (#38) has paid grants through Blackbaud and REPAY since Sept 2026 [V wave 7]. REPAY is the embedded payments rail of Blackbaud Financial Edge NXT, and Blackbaud named BILL as its successor on 2026-09-29 (early adopters only) [V wave 14].
- The community-foundation channel is fragmented and largely runs its own ACH, which leaves an open payments field without a dominant rail.

**What nonprofits pay to receive DAF grants** ([queue-nonprofit-side-panel.md](mission-2026-11-14/queue-nonprofit-side-panel.md), 33 entities [V wave 12]; [queue-agentic-products-dafpay-fees.md](mission-2026-11-14/queue-agentic-products-dafpay-fees.md) [V wave 8])
- Sponsors charge nonprofits $0 to receive grants. The exceptions are Benevity (2.99%, cap $500), DAFpay at default terms (2.9%) and ForGood (1.5%) (repo [`queue-nonprofit-side-panel.md`](mission-2026-11-14/queue-nonprofit-side-panel.md) P-NPT-06; [V wave 12]). [gap19-11]
- These are list prices only:
  - DAFpay's 2.9% default is rounded to whole dollars. The rounding applies only where no platform agreement sets the fee, so about 4% on a $25 gift is the nonprofit's worst case.
  - Platform add-ons run up to 4.85% (Bloomerang).
  - DAF Direct and PayPal Giving Fund charge nonprofits $0 [V].
- Grant minimums: $50 at Fidelity and DAFgiving360 (DAFgiving360 from a 2024 policy document), $250 at NPT and MS GIFT, $500 at Vanguard.
- Nonprofit cost per $1,000 grant ([nonprofit costs](mission-2026-11-14/queue-infrastructure-nonprofit-costs-emerging.md)): about $1–2 on free EFT rails, about $5–8 by check, about $32 on DAFpay at its 2.9% default.

**Payment intermediaries**
- DAF Direct is a recommendation router for three sponsors (Fidelity Charitable, DAFgiving360, BNY Mellon CGF). Its legal operator is DAF Direct Trust, and technical evidence suggests Fidelity runs it. No funds flow through it ([queue-infrastructure-nonprofit-costs-emerging.md](mission-2026-11-14/queue-infrastructure-nonprofit-costs-emerging.md) §Q-B18).
- Givinga is a single-sponsor platform whose account counts are unstable.
- **DAFpay access** ([queue-all-in-cost-dafpay-access.md](mission-2026-11-14/queue-all-in-cost-dafpay-access.md)) [V wave 10]: Chariot's default flow passes donor credentials through to the sponsor. Its credential-free method is named only for DAFgiving360 and Foundant-hosted community foundations. How it reaches Vanguard and NCF donors, whose terms bar this (§11.4), is not public.

**Bank-program terms** ([queue-bank-programs-and-eft-providers.md](mission-2026-11-14/queue-bank-programs-and-eft-providers.md), with wave-6 corrections)

| Sponsor | What the public terms show |
|---|---|
| MS GIFT | Donor Circular (Aug 2024) is public via its Ren DFX portal. Grants paid by mail or bank details; statements view-only; no outbound-transfer terms. |
| BofA CGF | Check-only grants. Contributions (not grants) can be exported to Excel. Balances can go to another DAF only if BofA terminates the donor's advisory rights. |
| Goldman Sachs PF | Circulars from 2008, 2012 and 2017 all state check payment. The live donor web runs on Ren iPhi. |
| NCF | Says most grants go by its own "eGrants" electronic payment, on a Salesforce portal. Its site data still carries iPhi donor-web IDs, so a Ren back-office link cannot be ruled out. |

### 11.4 Donor cost and portability

**All-in annual cost at $250k with each sponsor's typical pool** ([queue-all-in-cost-dafpay-access.md](mission-2026-11-14/queue-all-in-cost-dafpay-access.md); `scripts/mission_all_in_cost.py`) [V wave 10]

| Sponsor | All-in cost |
|---|---|
| Daffy | 0.26% |
| Vanguard | 0.62% |
| Fidelity | 1.15% |
| DAFgiving360 | 1.25% |
| NCF | 1.45% |
| San Francisco Foundation | 2.13% |

- Pool choice is as large a lever as sponsor choice. Fidelity's 60%-equity pool costs 0.55%; its index pool costs 0.015% (repo [`queue-all-in-cost-dafpay-access.md`](mission-2026-11-14/queue-all-in-cost-dafpay-access.md); [V wave 10]). [gap19-11]
- Edward Jones's 0.70% program fee rests on a search-index capture of Ren help pages that now return 404, so it is low confidence [V wave 33B] (repo [`queue-all-in-cost-dafpay-access.md`](mission-2026-11-14/queue-all-in-cost-dafpay-access.md); [V wave 10]). [gap19-11]

**Adviser fees: the largest, and often uncapped, cost layer** ([queue-all-in-cost-dafpay-access.md](mission-2026-11-14/queue-all-in-cost-dafpay-access.md); [queue-adviser-fees-pools-npact.md](mission-2026-11-14/queue-adviser-fees-pools-npact.md); `data/mission-2026-11-14/adviser-fees-observed-2026.csv`) [V waves 10–11]
- Adviser fees are the largest cost layer in adviser-led programs.
- MS GIFT, DAFgiving360 and TIFIN Give cap them at 1.00%. MS GIFT's cap excludes legacy pools and UMA manager fees.
- Fidelity CIAP, NPT, AEF and RCF publish no numeric cap. Fidelity caps the fee only relative to the adviser firm's own standard schedule (wave-11 governing note). Observed RIA brochures charge 0–2.00%.
- AEF's implied average adviser fee is 0.46%.
- Vanguard Charitable has no adviser-managed option.
- NPT's adviser-managed minimum is $500k for discretionary accounts and $2m for non-discretionary.

**Donor data export: none at the top 10** ([queue-donor-export-cf-payments-donorsphere.md](mission-2026-11-14/queue-donor-export-cf-payments-donorsphere.md)) [V wave 8]
- None of the 10 largest sponsors publishes a donor-side machine-readable export or a portability statement. This rests on public material only; logged-in features could not be checked.
  - Fidelity: PDF only.
  - Vanguard: view only.
  - AEF: two years of grant history. Its live FAQ shows an "Export" button, but the instruction covers only a grants-paid list in legacy DonorCentral ([queue-sponsor-terms-data-clauses.md](mission-2026-11-14/queue-sponsor-terms-data-clauses.md)) [V wave 9].
  - SVCF: its 2025 fund agreement bars automated collection for non-grantmaking purposes, and puts third-party portal access without SVCF approval at the advisor's risk, with an indemnity.
- Greater Washington CF's CSV export shows that portability is technically trivial.

**Sponsor terms restricting automation and credential sharing** ([queue-sponsor-terms-data-clauses.md](mission-2026-11-14/queue-sponsor-terms-data-clauses.md)) [V wave 9]
- NCF's 2025 Program Agreement bans credential sharing with third-party services and scraping, and authorizes no third-party access.
- Vanguard's User Agreement treats an outside service that uses the donor's login as an "Unauthorized Third Party". It permits the account holder's own aggregators; that this amounts to read-only, self-run aggregation is an inference.
- NPT's 2026 terms ban robot harvesting and using site or user data to develop or operate any software, model or AI system.
- Fidelity's licence only says Fidelity "may provide" an export (undated clause; no live feature found).
- These terms conflict with credential-based rails (DAFpay) and with donor-side AI agents.

**Vendor contract templates and data rights** ([queue-contract-data-rights-agent-controls.md](mission-2026-11-14/queue-contract-data-rights-agent-controls.md))
- Sponsors own their data, but no incumbent public template grants API access.
- NPact §2.4 (Aug 2025) bars third-party transaction access [V]. iPhi allows a 15-day export window [V]; this is Ren's published template, and executed customer terms may differ (wave-4 governing note).
- So an entrant can reach batch exports without vendor consent, but **not live integration**.

**Candid API licence (2026-09-14)** ([queue-sponsor-terms-data-clauses.md](mission-2026-11-14/queue-sponsor-terms-data-clauses.md)) [V wave 9]
- On termination, licensees must stop all use of the data. The licence has no retention carve-out, while the IRS third-party reliance rule (Rev. Proc. 2018-32 §8.01(2)) requires grantors to retain the report [V wave 14].
- Data mining is barred for building a database, reselling or competing with Candid.
- Charity Check draws on Pub78, the BMF, the IRB, revocations and the OFAC SDN list.

### 11.5 AI and agentic controls

**Agentic giving products** ([queue-agentic-products-dafpay-fees.md](mission-2026-11-14/queue-agentic-products-dafpay-fees.md)) [V wave 8]
- None of 21 agentic giving products (2024–26) has independent outcome evidence, and no product touches sponsor approval (repo [`queue-agentic-products-dafpay-fees.md`](mission-2026-11-14/queue-agentic-products-dafpay-fees.md) P-INF-08; [V wave 8]). The later census of 30 products finds none that meets the RED test (repo [`direction-ai-product-census.md`](mission-2026-11-14/direction-ai-product-census.md); wave 28). [gap19-11]

**Agentic donation controls** ([queue-agentic-controls-and-sponsor-audits.md](mission-2026-11-14/queue-agentic-controls-and-sponsor-audits.md); [queue-contract-data-rights-agent-controls.md](mission-2026-11-14/queue-contract-data-rights-agent-controls.md))

No public contract at Daffy, TIFIN Give/GiveClear, Endaoment or Chariot treats an AI agent as a distinct actor. All four allocate the loss from erroneous actions to the donor or customer.

| Provider | Agent-initiated donation controls |
|---|---|
| Daffy | Sponsor approval before payment is the binding control. Its member agreement predates its MCP server and does not identify which agent acted. Its MCP documents no spend limits [V]. |
| TIFIN Give / GiveClear | Louise has 8 of 10 controls undocumented; TIFIN publishes no Louise controls. |
| Endaoment | The partner grant call needs only the partner's API key, and no review step is documented for that path. |
| Chariot | Best pattern: a Chariot-hosted confirmation step with sponsor review preserved. It has no human-vs-agent field. |

**AI economics v2 on observed costs** ([ai-economics-v2-observed-costs.md](mission-2026-11-14/ai-economics-v2-observed-costs.md); `scripts/mission_ai_economics_v2.py`, seeded Monte Carlo with 10,000 draws)

Cost pools are anchored to Form 990 operating cost with elasticity-based scaling. The process-handling share, amenability, redesign share, QA rate and fixed costs remain stated assumptions.

What survives from v1:
- Redesign or conventional fixes are the most likely winners in all 16 processes.
- AI on the existing workflow ranks first in at most 17% of draws (repo [`ai-economics-v2-observed-costs.md`](mission-2026-11-14/ai-economics-v2-observed-costs.md)). [gap19-11]
- Inference cost is immaterial.
- One AI project exceeds the entire IT line of a $250m community foundation in 67% of draws (repo [`ai-economics-v2-observed-costs.md`](mission-2026-11-14/ai-economics-v2-observed-costs.md)). [gap19-11]

What changes:
- "AI ranks last everywhere" fails for complex-asset and non-standard-grantee review.
- A shared AI platform breaks even in 43% of draws with the five largest nationals in the network, and in 0.4% with community foundations under $250m alone. Calibrated to 21 published studies (2021+), the 43% falls to 16% and the large-national AI value pool to $445k from $1.18m ($202k on field evidence, $793k on task experiments). No process changes its most likely winner. The calibrated figure assumes re-review only on AI-handled cases; on v2's all-touched basis the pool is $110k (repo [`gap19-ai-calibration.md`](mission-2026-11-14/gap19-ai-calibration.md); [V wave 31A]).
- A $120k/yr AI product cannot be funded from process savings below about $1bn of DAF assets (repo [`ai-economics-v2-observed-costs.md`](mission-2026-11-14/ai-economics-v2-observed-costs.md), implications item 1, [I] on [S] outputs). [gap19-11] The economic buyer is an administrator or platform vendor, not an individual sponsor.

What the cost-structure data does to the v1 model ([sponsor-cost-structure-and-sensitivities.md](mission-2026-11-14/sponsor-cost-structure-and-sensitivities.md)):
- It refutes the "technology expense undisclosed" premise and the assumption that cost grows linearly with grant volume.
- It confirms the base labour pool, which is about 6–8% of observed cost per grant.
- It confirms that a $150k–$750k standalone AI build is prohibitive for most community foundations (median IT spend is $17k–$116k).

**Labour rates** ([queue-pe-lenders-labour-rates.md](mission-2026-11-14/queue-pe-lenders-labour-rates.md)) [V wave 8]: the Form 990 median loaded rate is $38.87/h across 898 sponsors. It is $57–73/h at $250m+ sponsors and $86/h at DAFgiving360.

### 11.6 Capital markets: owners, lenders, buyers, failures and sponsor mortality

**Who is interested in DAF organizations** ([firms-interested-in-daf-organizations.md](mission-2026-11-14/firms-interested-in-daf-organizations.md); 89 firms)
- Revealed interest comes from private-equity incumbents (GTCR; Bain, majority in 2023 and a significant shareholder after 2025 [V]; Great Hill) and wealth platforms (SEI, LPL, AssetMark, Envestnet).
- Vanguard signed to acquire Altruist (not closed). Altruist launched DAFs sponsored by Endaoment 41 days later [V].
- Platforms sign white-label deals rather than buy DAF vendors, and common PE ownership has not forced vendor alignment.
- Sponsors themselves cannot be acquired. They merge or affiliate under charity law.

**Private equity across the DAF ecosystem** ([private-equity-daf-ecosystem-map.md](mission-2026-11-14/private-equity-daf-ecosystem-map.md); 120 ownership rows across ~60 companies; wave-7 and wave-8 corrections applied)

The map adds about 40 investors beyond the earlier list, across three groups:
- **Nonprofit-software investors:** JMI, Summit, Susquehanna, Fulcrum, FTV, Metamorph/ABS, LLR, Rubicon, Warburg (Bloomerang 2024).
- **Benevity co-owners:** General Atlantic, TPG Rise, Generation.
- **Wealth-platform owners:** Carlyle, Madison Dearborn, CD&R, Reverence, GIC, ICONIQ.

Portfolio adjacencies, where one owner holds a DAF asset alongside a distribution or software asset:
- **Bain:** Ren, Envestnet and FreeWill.
- **GTCR:** Foundation Source, AssetMark and a CAPTRUST stake (25% in 2020; undisclosed since Carlyle joined in 2023) [V wave 7].
- **General Atlantic and TPG:** Benevity (stakes evidenced only from 2020–21) and Creative Planning.
- **TA:** Orion (co-owned with Genstar; distributes GiftingNetwork DAFs) and Momentive.

No owner has steered its wealth platform to its own DAF vendor.

Likely next deals (inference, medium confidence):
- Hg exits or uses a continuation vehicle for Benevity (2026–28) [I] (repo [`private-equity-daf-ecosystem-map.md`](mission-2026-11-14/private-equity-daf-ecosystem-map.md), exit-window table). [gap19-11]
- Apax sells or recapitalises Bonterra (2027–28) [I]. Bonterra bought Deed on 2026-03-05, putting it head-to-head with Benevity (repo [`private-equity-daf-ecosystem-map.md`](mission-2026-11-14/private-equity-daf-ecosystem-map.md) item 5 and exit-window table). [gap19-11]
- GTCR sells or recapitalises Foundation Source (2027–29) [I] (repo [`private-equity-daf-ecosystem-map.md`](mission-2026-11-14/private-equity-daf-ecosystem-map.md), exit-window table). [gap19-11]
- TA/Genstar exit Orion.

**Lenders and BDC marks** ([queue-pe-lenders-labour-rates.md](mission-2026-11-14/queue-pe-lenders-labour-rates.md) [V wave 8]; [queue-bdc-fix-labour-benevity.md](mission-2026-11-14/queue-bdc-fix-labour-benevity.md) [V wave 9]; [queue-bdc-coverage-migrations-goodstack.md](mission-2026-11-14/queue-bdc-coverage-migrations-goodstack.md) [V wave 10])
- **Foundation Source:** Audax remains its first-lien lender (S+5.00%, 2030, at par); Audax was already recorded as its lender in 2020 [V wave 8].
- **Bonterra:** the Golub-led CyberGrants/Bonterra loan due 2027 was refinanced in 2025 into an S+4.75–5.00% loan due 2032. Golub marked the old 2027 loan at par at 2024-12-31 [V].
- **Bonterra 2032 holders:** the fixed BDC parser finds 13 holders, marked 97.7–99.5% (KKR Enhanced Fund-L lowest at 97.71%, 2026-06-30). The BDC parser now dates each row by its own period [V wave 10].
- **Momentive (Community Brands):** FS KKR marks it at 96.1% [V].
- **Other lenders found:** Golub to Momentive and Orion; Ares, Blue Owl and Benefit Street to Envestnet.
- **Not found:** no BDC lender for Ren or Benevity.

**Failed and retreated ventures** ([failed-daf-startups-deep-research.md](mission-2026-11-14/failed-daf-startups-deep-research.md); 50 cases)
- Outcomes: 12 acquisitions, 11 voluntary shutdowns, 6 regulator or insolvency events, 5 pivots.
- **Donor money was lost only where one operator held unsegregated funds:** Ammado, Flipcause and SDG Impact Fund.
- Most DAF-tech exits are acquisitions by consolidators (Ren, Foundation Source, TIFIN).
- Crypto-giving revenue is cyclical. Shift4 cut The Giving Block earnout liability by $47.1m in FY2022 [V].
- Entrant rule: never hold donor funds, disclaim title to donations in transit, and check processor reserve terms.

**Sponsor mortality** ([sponsor-mortality-analysis.md](mission-2026-11-14/sponsor-mortality-analysis.md))
- Verified exit rate is 0.19–1.48% a year by count and about 0.2% by assets, recomputed exactly [V].
- In every confirmed closure, assets moved to another sponsor.
- DAFRC marks some still-active sponsors as closed (Donors Fund, amended FY2024 990: 6,290 DAFs, $315.8m [V]).

**Sponsor audits** ([queue-agentic-controls-and-sponsor-audits.md](mission-2026-11-14/queue-agentic-controls-and-sponsor-audits.md))
- Read: Fidelity, Vanguard (FY2026), RCF, NCF and Charityvest. All have unmodified opinions, none has a going-concern paragraph, and none references a SOC report.
- Available on request only: Daffy and AEF.
- Not public or not reachable: GS PF, MS GIFT and BofA CGF post nothing, and NPT posts summaries only.

### 11.7 Customer experience

**User complaints** ([daf-user-complaints-deep-research.md](mission-2026-11-14/daf-user-complaints-deep-research.md); 244 records)
- Top themes: app login and crash failures (mostly the Fidelity Charitable app, 2012–2026), grant delays (nonprofits), sponsor discretion (the 2026 SPLC holds; letter from 16 AGs [V]) and gift-receipt friction.
- Of complaint and mixed records, 117 are fixable and 47 structural. All critical records are structural.
- Every donor lawsuit found failed or is pending (Fairbairn lost after a bench trial [V]).
- Counts lack customer-base denominators, and Reddit was inaccessible.

Related customer-facing frictions are covered by theme: data export and credential terms (§11.4), grant minimums and payment rails (§11.3), and history loss in migrations (§4).

### 11.8 Monitoring and open questions

**Monitors in place**
- A dated terms monitor (`scripts/mission_terms_monitor.py`) snapshots 18 vendor and sponsor terms for change tracking ([queue-assurance-everyorg-givinga-monitoring.md](mission-2026-11-14/queue-assurance-everyorg-givinga-monitoring.md)).

**Not yet measurable** ([queue-net-payout-fidelity-outliers.md](mission-2026-11-14/queue-net-payout-fidelity-outliers.md))
- Fidelity's $727m of CY2025 outlier grants and the post-SPLC DAF-to-DAF flows will not be visible until the 2027–28 filings.

**Open questions carried by the workstreams**
- Gulf Coast's move off iPhi is still "launching soon" ([queue-ren-iphi-attrition.md](mission-2026-11-14/queue-ren-iphi-attrition.md)).
- NPT's payment to Ren is undisclosed ([queue-npt-givingpoint-fidelity-stack.md](mission-2026-11-14/queue-npt-givingpoint-fidelity-stack.md)).
- How DAFpay reaches donors whose sponsor terms bar credential sharing ([queue-all-in-cost-dafpay-access.md](mission-2026-11-14/queue-all-in-cost-dafpay-access.md)).
- NPact's current owner ([queue-ledger-segment-npact-owner.md](mission-2026-11-14/queue-ledger-segment-npact-owner.md)).
- The NYCT and California CF ledgers, which rest on job-posting skills only ([queue-ledger-segment-npact-owner.md](mission-2026-11-14/queue-ledger-segment-npact-owner.md)).
- Givinga's account unit ([sponsor-cost-structure-and-sensitivities.md](mission-2026-11-14/sponsor-cost-structure-and-sensitivities.md)).
- Edward Jones's program fee, whose help pages now return 404 ([queue-all-in-cost-dafpay-access.md](mission-2026-11-14/queue-all-in-cost-dafpay-access.md)).
- Give Interactive's role at CCT ([queue-vendor-channel-moves.md](mission-2026-11-14/queue-vendor-channel-moves.md)).

### 11.9 Batch 29 (validated, wave 14)

**Batch 29 (validated, wave 14).** Peterson v. WaterStone is pending in discovery, with the MTD fully briefed and final productions due 2027-02-14. It is the first 2021+ successor-adviser suit to get this far; Pinkert and Fairbairn failed. California's AB 488 excludes a DAF sponsor only if it does not name charities to non-advisers, and excludes a vendor only if it "solely" provides technical services. Public complaint rates per 10,000 accounts (Daffy 11.2, Vanguard 5.4, Fidelity 2.3, DAFgiving360 1.3) measure venue coverage, not service quality. At least 17% of the top 200 sponsors itemise grant voids, refunds or recoveries on their 990s (median about 0.3% of grants). That reflects accounting presentation, not void incidence. ImpactAssets' $160.8m CY2024 line to NPT is most likely a donor-recommended DAF-to-DAF transfer; NPT sent $63.5m the other way over FY2024–25. The Giving Block earnout (maximum $246m; $57.8m fair value at acquisition) settled at $10.4m, and Fidelity Charitable's crypto inflow fell 88% in 2022 and 54% in 2025, so crypto-dependent entrants (crypto was 99.7% of Endaoment's FY6/24 contributions) carry drawdown risk. Not holding funds removes the fundraiser bond in only some states (CT, NJ, OH, GA, IL in the 18-state sample; MN, NH, RI, LA per the 2023 survey) [V wave 14]. Sources: [queue-batch29-regulation-litigation-crypto.md](mission-2026-11-14/queue-batch29-regulation-litigation-crypto.md), [queue-batch29-complaints-voids.md](mission-2026-11-14/queue-batch29-complaints-voids.md), [queue-batch29-fit-ledgers.md](mission-2026-11-14/queue-batch29-fit-ledgers.md), [validation-wave14-report.md](mission-2026-11-14/validation-wave14-report.md).

### 11.10 Batch 30 (validated, wave 15)

**Batch 30 (validated, wave 15).** California's platform law reaches DAF technology vendors on its text, and custody is not the test. An own-brand app that lists charities for "grants of recommended donations" is Type A (§12599.9(a)(1)(A); 11 CCR 314(m)). A white-label portal licensed to a sponsor is Type E (314(q)). The DAF exclusion names only the sponsor. Type E duties are light for a vendor that never holds funds: a disclosure (§317(d)(3)) and five-business-day remittance (§320(c)(1)). Candid's Charity Check PDF meets most of Rev. Proc. 2018-32 §8.01. It prints no time of day, though the JSON gives one in GMT, and it still cites the superseded Rev. Proc. 2011-33. Only Candid's subscriber licence, not its API licence, allows retention after termination. Current wealth-captive terms: GS DAF $20k minimum and $100 grants by check or wire (circular reproduced in FireAid's 2025 report); MS GIFT $25k and $250 with a 0.27% administrator fee; BofA CGF a flat first-dollar 0.90%–0.10%. Givinga's 1,421,011 accounts ($1.37 average) come from an e-filed amended CY2024 return. Givinga Foundation is the sponsor behind Janus Henderson's 0.30% Charitable Investment Accounts. Every.org files 990-PF and holds only $0.1–0.3m of audited donor credit, so it has no DAF book. Goodstack US reported 3 DAFs in FY2025, down from 7,268. Endaoment reported 6,000 DAFs for FY6/24. Unmapped community foundations fell from 39.2% to 31.1% of 803 by count, and from 6.1% to 2.8% by DAF assets. Foundant leads on count (46.5%, a floor) and Salesforce on assets (24.8%, adding Arizona CF and CFSEM). None of the 14 Foundation Cloud portals is evidenced as an NPact ledger; 81% of their assets sit on Blackbaud. Give Interactive's only demonstrated live CF loss is East Bay (to akoyaGO). Omaha moved to Foundant on 2024-07-30, and FFTC went through NPact to GiftingNetwork on 2026-07-01. Give's known clients hold $36.7bn of FY2024 DAF assets, against its "$40B+" 2025 claim [V wave 15]. Sources: [queue-batch30-legal-circulars.md](mission-2026-11-14/queue-batch30-legal-circulars.md), [queue-batch30-everyorg-givinga-goodstack.md](mission-2026-11-14/queue-batch30-everyorg-givinga-goodstack.md), [queue-batch30-cf-coverage-give.md](mission-2026-11-14/queue-batch30-cf-coverage-give.md), [validation-wave15-report.md](mission-2026-11-14/validation-wave15-report.md). Sources: [queue-batch30-legal-circulars.md](mission-2026-11-14/queue-batch30-legal-circulars.md), [queue-batch30-everyorg-givinga-goodstack.md](mission-2026-11-14/queue-batch30-everyorg-givinga-goodstack.md), [queue-batch30-cf-coverage-give.md](mission-2026-11-14/queue-batch30-cf-coverage-give.md), [validation-wave15-report.md](mission-2026-11-14/validation-wave15-report.md).

### 11.11 Batch 31 (validated, wave 16)

**Batch 31 (validated, wave 16).** AEF's line 11f ($26.4m, $29.5m and $36.0m for TY2022–24; 0.40–0.46% of assets; $1,876–$2,254 per account) is exactly the investment expense its audit nets inside investment return. Schedule D Part XII line 4a adds it back. So 11f measures the average fund-borne adviser and manager cost per dollar, not what a fee-charging account pays. If fee-charging accounts pay 1.00%, they would hold about 46% of assets. Adviser brochures add two DAF-specific menus: Davenport's RCF private label charges a 1.00%→0.75% wrap on SMAs and 0.75% on models, with RCF's admin fee on top. NPT also pays an intermediary layer that donors do not see as adviser fees: Hollencrest receives 5–25 bps of assets introduced to NPT. Part IX understates all-in cost at the nationals. GS DAF's visible 28.7 bps is about its admin layer (a 26.4 bps bound), and the 0.62–0.67% GSAM fund expense ratios are off the 990. At MS GIFT the visible advisory-type lines are only about 7.8% of a 1.00% advisory ceiling. Endaoment's FY2025 990 (in IRS zip 05B) reports 1,213 DAFs, $25.03m in and $18.68m out; all $24.33m of Part VIII contributions were crypto. That makes FY2024's round 6,000 the outlier. Every.org filed 990-PF for CY2020–24 because it was in a 507(b)(1)(B) 60-month termination. Letter 4422 (2025-10-23) reclassified it as a 170(b)(1)(A)(vi) public charity as of 2020-01-01. Since 2026-09 it accepts IRA QCDs that can fund a "giving credit" balance, and §408(d)(8)(B)(i) bars QCDs to DAFs, so how those balances are classified now matters. Fidelity Charitable is the only DAF sponsor with a named Addepar feed, which requires a G-Number. Empower offers a separate "Fidelity Charitable" connection. Ren's own front-end code maps "Ren for Charities ACH" to its RDE rail, apart from "Legacy" third-party payments, but Ren still names none of its "25+" programs beyond AEF. NPact's W-9s show the same Fusion Laboratories LLC, taxed as a partnership, moving from Dallas to Wakefield, MA between 2024-02 and 2025-07; no sale is evidenced. Santa Barbara's own posting puts its GL on Blackbaud FE NXT. No Foundation Cloud tenant now shows an NPact-hosted ledger [V wave 16]. Sources: [queue-batch31-fees-costs.md](mission-2026-11-14/queue-batch31-fees-costs.md), [queue-batch31-filings-feeds.md](mission-2026-11-14/queue-batch31-filings-feeds.md), [queue-batch31-ren-npact-gl.md](mission-2026-11-14/queue-batch31-ren-npact-gl.md), [validation-wave16-report.md](mission-2026-11-14/validation-wave16-report.md). Sources: [queue-batch31-fees-costs.md](mission-2026-11-14/queue-batch31-fees-costs.md), [queue-batch31-filings-feeds.md](mission-2026-11-14/queue-batch31-filings-feeds.md), [queue-batch31-ren-npact-gl.md](mission-2026-11-14/queue-batch31-ren-npact-gl.md), [validation-wave16-report.md](mission-2026-11-14/validation-wave16-report.md).

### 11.12 Batch 32 (validated, wave 17)

**Batch 32 (validated, wave 17).** Fidelity Charitable's audit Note 3 and its expense-ratio page give an asset-weighted pool expense ratio of 26.3 bps (FY2025; 27.4 bps FY2024). That is 13.9 bps per invested dollar, because 47% of investments sit in CIAP accounts whose fund costs are unpublished. With Part IX operating cost, Fidelity's all-in floor is about 50–52 bps. CIAP adviser fees, which the audit books gross and which equal line 11f, run at a stable 26.1–26.9 bps of average CIAP assets (31–35 bps with the line-24 CIAP item), about 60% of AEF's rate. MS GIFT's 1.00% advisory cap and 0.07% MSSB fee do not appear in Part IX (visible advisory-type lines are 7.8 bps), and its Schedule D reconciliation is zero-filled. Its line-3 investment income (4–35 bps against 128–424 bps at ten peers) is an anomaly too large for fee netting alone. A full Schedule G screen of 5,272 returns finds three sponsors besides Givinga whose DAF contributions include sweepstakes or auction gross receipts, with the agent keeping 40–85%: Pledgeling, CAF America (Omaze, FYE April 2022–23) and Our Change. Endaoment's FY2023 990 understated year-end net assets by $12.2m against its audit, and the FY2024 return silently reopened at the audited figure. All four returns answer "audited: No". The FY2025 −$2.50m prior-period adjustment and $1.39m self-grant are unexplained, and 1,213 (FY2025) is the best-evidenced DAF count. Every.org now lets IRA gifts fund "giving credit", which it calls its "DAF structure"; on the statute and the 2023 proposed regulations that balance looks like a 4966(d)(2) fund, which would put such IRA gifts outside the QCD exclusion. This is an open question, not a finding. Of 58 tier-B "exits", 14 are documented and 18 are not exits, so the central exit bound falls from 1.20% to 0.89% a year (0.44% documented only). Fidelity Charitable is still the only DAF sponsor named among Addepar's 406 feeds. Clearlake's unchanged 9,751,837 Blackbaud shares are now about 21.7% after buybacks, with no new proposal. Givinga has raised $22.4m across six Form D offerings since 2019 ($10.77m in the current one). Groundswell's sponsor reached $11.9m revenue and 12,808 accounts. Philanthropi's site is dark, while its infrastructure certificates still renew. DonorFirst/DFX, iPhi and Vennfi run on as acquirer stacks, and Amicus is merged into TIFIN Give [V wave 17]. Sources: [queue-batch32-infund-costs.md](mission-2026-11-14/queue-batch32-infund-costs.md), [queue-batch32-filing-reconciliations.md](mission-2026-11-14/queue-batch32-filing-reconciliations.md), [queue-batch32-feeds-owners-codebases.md](mission-2026-11-14/queue-batch32-feeds-owners-codebases.md), [validation-wave17-report.md](mission-2026-11-14/validation-wave17-report.md). Sources: [queue-batch32-infund-costs.md](mission-2026-11-14/queue-batch32-infund-costs.md), [queue-batch32-filing-reconciliations.md](mission-2026-11-14/queue-batch32-filing-reconciliations.md), [queue-batch32-feeds-owners-codebases.md](mission-2026-11-14/queue-batch32-feeds-owners-codebases.md), [validation-wave17-report.md](mission-2026-11-14/validation-wave17-report.md).

### 11.13 Batch 33 (validated, wave 18)

**Batch 33 (validated, wave 18).** 185 returns from 113 DAFRC sponsors (3.5% of line-6 "Yes" returns, TY2021+) answer that they hold DAFs but leave Schedule D Part I blank. DAFRC imputes 78 of them ($1.60bn summed across four years' year-end values, at most $0.69bn in any one year) and drops 77 from 31 sponsors as "closed". Carrying those sponsors' last values forward puts $151–172m a year (≤0.07% of DAF assets) outside the totals. Treating reporting gaps as non-exits lowers the mechanical central exit rate from 1.20% to 0.91% a year (0.89% with manual coding). Sweepstakes and auction receipts inside DAF contributions are at most 0.17% of the market (FY2022), falling to 0.05% in FY2024. MS GIFT is the only broker or bank captive whose line-3 investment income is below 50 bps of assets; DAFgiving360 is next at 96–114 bps. Among the top 50 sponsors, grants to other top-50 DAF-holding sponsors were $3.39bn (FY2023) and $6.03bn (FY2024), or 6.2% and 9.3% of market grants. Panel-wide, lines to DAF-holding sponsors were $5.24bn and $9.56bn, an upper bound on double counting. About half of the gross top-50 pair flow nets out. NPT is the main net receiver (+$1.89bn over two years) and SVCF the main net sender (−$1.21bn, chiefly one $1.59bn CY2024 line); Vanguard sent ImpactAssets $308m in FY2024. Where a void window is published (Fidelity, GiveClear, BlueGive) it is 90 days, with funds returned to the donor account. PayPal Giving Fund instead may remove the charity and reassign funds, a rule unchanged since at least 2022; its 2025 policy only shortened check delivery to 45 days after month-end. No sponsor states an escheat treatment. Six top-40 community foundations (18.2% of top-40 CF DAF assets) publicly document a donor grant-history export, all on packaged portals, and Foundant added one on 2024-08-27. BofA's guide shows "Export to Excel" on the Grant Listing too. J.P. Morgan's GivingPoint code says "NPT will issue a check", and its payment enum has no Ren RDE value, so NPT pays on its own rails. Corporate giving products closed for parent-level reasons (AmazonSmile "spread too thin"; Virgin Money Giving's investment need and loss of marathon "brand exposure"), and Meta handed processing to PayPal Giving Fund. Foundant merged with SmartSimple (2024-08-13) and took in GivingData (May 2025). The $20.2bn faith segment (186 sponsors) has no common platform; NCF's $5.46bn Salesforce captive is a DAFRC-imputed value. Edward Jones reports "nearly $535 million" invested in its Charitable Gift Fund (described as both 2023 assets and since inception), administered by RCF; its private DAF's sponsor is still not public. **Goldman:** a 2021+ GS DAF circular (ETF ratios as of 2024-09-30; check or wire; Goldman Sachs Wealth Services, L.P. in Ayco's former role) is reproduced in FireAid's 2025 report, so batch 33C's "newest circular 2017" is superseded [V wave 18]. Sources: [queue-batch33-panel-scans.md](mission-2026-11-14/queue-batch33-panel-scans.md), [queue-batch33-voids-exports-rails.md](mission-2026-11-14/queue-batch33-voids-exports-rails.md), [queue-batch33-market-structure.md](mission-2026-11-14/queue-batch33-market-structure.md), [validation-wave18-report.md](mission-2026-11-14/validation-wave18-report.md). Sources: [queue-batch33-panel-scans.md](mission-2026-11-14/queue-batch33-panel-scans.md), [queue-batch33-voids-exports-rails.md](mission-2026-11-14/queue-batch33-voids-exports-rails.md), [queue-batch33-market-structure.md](mission-2026-11-14/queue-batch33-market-structure.md), [validation-wave18-report.md](mission-2026-11-14/validation-wave18-report.md).

### 11.14 Batch 34 (validated, wave 19)

**Batch 34 (validated, wave 19).** Netting sponsor-to-sponsor DAF transfers (rule R5, central tier) removes $5.52bn, $6.40bn, $4.05bn and $8.03bn from both corrected DAF grants and corrected contributions in FY2021–24, which is 7–12% of grants. The lower and upper tiers give $3.32–6.95bn and $4.88–9.42bn a year. FY2024 netted grants are $58.41bn (corrected $66.44bn) and contributions $84.74bn ($92.77bn). Payout on prior-year corrected assets falls from 25.9% to 22.8%, and FY2024 grant growth from +21.2% to +15.0%: much of the FY2024 jump is transfers between sponsors, largely to NPT. A reviewed whitelist of 1,411 recipient EINs drives it. Universities and hospitals and low-DAF-share fiscal sponsors are excluded, and community foundations are weighted by their DAF share of assets. Ayco Charitable Foundation filed a final FY6/2025 return: it merged into GS DAPF on 2025-07-01 and moved $1.16bn to it outside its Schedule D grants. NPT's "PROGRAM FEES" have run flat at $3.7–4.3m since FY2021 while DAF assets rose 3.5×, and moved from M&G to Program in FY2024; the payee is undisclosed. On filed returns the five large pass-through sponsors made $4.32bn of FY2024 DAF grants ($3.87bn in the latest years, or $4.85bn with the "other funds" AOGF has just moved out of the DAF column: 751,746 accounts and $936m of grants). The PPGF and NFG filed values were already in the corrected totals. Benevity takes $54.7m a year from AOGF (2.35% of its grants) and CyberGrants $8.3m from CAF America. PayPal donates PPGF's staff, and NFG's sole member has been DCSO since 2024-06-07. DAF Direct is a Fidelity-run trust whose widget still lists BNY Mellon CGF, which voted on 2024-12-24 to wind down. Fraternal insurers run their own sponsors (Thrivent, Knights of Columbus). Northwestern Mutual uses RCF, and Alera white-labels TIFIN Give. Jasper Ridge's exit followed public support of 13.15% (CY2022) and $1.32bn of in-kind transfers, mostly to Schwab and Fidelity. RUUPA §1005(c)(6) and (c)(8), Delaware §1175(b)(6) (no void defence) and UCC §3-303(b) give voided gift checks statutory defences; no enforcement history was found. Six of the top 20 sponsors (about $84bn of assets) contractually limit automated or third-party access. Fidelity CIAP assets at an outside custodian pay 10 bps more on the first $500k. DAFRC's 2026 adviser report confirms 35/21/10/4% and 83/69/69/63%, but "61% of clients initiate vs 6%" is 2018 U.S. Trust/TPI data. Correction: Jasper Ridge's $750.6m to Schwab is the Schedule I figure, and Schedule N's line items total $746.5m [V wave 19]. Sources: [queue-batch34-netting-filings.md](mission-2026-11-14/queue-batch34-netting-filings.md), [queue-batch34-pass-through-channels.md](mission-2026-11-14/queue-batch34-pass-through-channels.md), [queue-batch34-escheat-terms.md](mission-2026-11-14/queue-batch34-escheat-terms.md), [validation-wave19-report.md](mission-2026-11-14/validation-wave19-report.md). Sources: [queue-batch34-netting-filings.md](mission-2026-11-14/queue-batch34-netting-filings.md), [queue-batch34-pass-through-channels.md](mission-2026-11-14/queue-batch34-pass-through-channels.md), [queue-batch34-escheat-terms.md](mission-2026-11-14/queue-batch34-escheat-terms.md), [validation-wave19-report.md](mission-2026-11-14/validation-wave19-report.md).

### 11.15 Batch 35 (validated, wave 20)

**Batch 35 (validated, wave 20).** AOGF (Benevity) has moved its micro-donation accounts out of the Schedule D DAF column. Its FYE 2026-03 return reports 695 DAFs, down from 710,352, and 751,746 "other" accounts carrying $935.7m of grants. Applied back to FY2024, that basis cuts corrected market accounts by 21.8% (3.31m → 2.59m) but grants by only 1.2%. Three micro-account processors (Givinga, AOGF and PPGF) hold 76.2% of corrected FY2024 accounts, so account counts and per-account averages should be reported with and without them. Among 123 few-account, large-balance sponsors, the Community Foundation of South Lake County reported 30.04% public support for FY9/2025 and ticked the Schedule A private-foundation box. Los Altos CF (26.0%) and Community Foundations Inc (25.6%) passed only on the prior-year test. Fidelity Charitable's FY2025 Schedule I sends $3.46bn to 927 DAFRC-panel sponsors and Vanguard's $586m to 506. Fidelity → Vanguard is $480.1m against $87.3m back, a net $392.8m. Vanguard's FY2025 DAF contributions ($5.75bn) were flat on FY2024. No top-20 sponsor names a software service as an appointable party. Vanguard alone permits an Authorized Person with their own Vanguard-issued login to use "aggregators", while still barring bots. GS DAF ("or another third party") and SVCF (prior approval) leave an entity route open. Network for Good, now For Good, became a subsidiary of DCSO (dba The Resiliency Company) in June 2024. The two share a CEO and general counsel, and DCSO took about $27.0m from NFG. For Good reports $193.1m of 2024 DAF grants. Vanguard's audited pool balances put asset-weighted in-fund cost at ≈3.6 bps (3.5–4.8). Daffy is the only DAF API with third-party agent wrappers: Pipedream, Zapier and Metorial expose donation creation, and Composio and Corsair expose gift creation. Daffy keys carry no documented scope. Every.org's ForGood (check) rail fell from 73.9% of grants (2020) to 1.1% (2024). Chariot reports 94.57% of grant payments sent electronically. No contradictions were found. The corrections are wording only: wrappers that only create gifts are not documented fund debits, and DCSO's legal name is Durable Capital for Sustainable Outcomes Inc [V wave 20]. Sources: [queue-batch35-panel-screens.md](mission-2026-11-14/queue-batch35-panel-screens.md), [queue-batch35-access-owners-faith.md](mission-2026-11-14/queue-batch35-access-owners-faith.md), [queue-batch35-agents-analysts-rails.md](mission-2026-11-14/queue-batch35-agents-analysts-rails.md), [validation-wave20-report.md](mission-2026-11-14/validation-wave20-report.md). Sources: [queue-batch35-panel-screens.md](mission-2026-11-14/queue-batch35-panel-screens.md), [queue-batch35-access-owners-faith.md](mission-2026-11-14/queue-batch35-access-owners-faith.md), [queue-batch35-agents-analysts-rails.md](mission-2026-11-14/queue-batch35-agents-analysts-rails.md), [validation-wave20-report.md](mission-2026-11-14/validation-wave20-report.md).

### 11.16 Batch 36 (validated, wave 21)

**Batch 36 (validated, wave 21).** On a strict "ongoing advisory privilege" basis, applying only AOGF's own FYE 2026 reclassification, the DAF market held 2.59m accounts in FY2024 (1.12m in FY2021), not 3.31m. Grants fall only 1.2% and assets under 0.03%. Excluding the two other micro-account processors (Givinga and PayPal Giving Fund) leaves 0.79m accounts in FY2024. On that basis accounts grew 9.7% a year over FY2021–24, against 20.6% on corrected totals. Account counts and per-account averages should therefore always be shown with and without the processors. Replacing DAFRC's "closed" flags and imputations for blank Schedule D returns moves market assets by −$25m to +$170m a year (at most 0.07%). DAFRC's imputations interpolate linearly between filed years, as the CF of Middle Tennessee rows show exactly. Fidelity Charitable is the only sponsor publishing a dated electronic-grant series: >50%, nearly 54%, >58% and 67% of grants by EFT in its 2023–2026 reports. Two of those reports give EFT counts that do not reconcile with the shares. Latency is published as policy, not measurement. The only measured figures are vendor ones: Charityvest says 95% of checks are deposited within 35 days of sending, and AssetMark reports a median of 2 days overall and 0 days electronic. No donor contract read admits a software service as a delegate. Vanguard interested parties "must be individuals". DAFpay bars use "on behalf of or to provide services to third parties". Endaoment's terms bar sharing API credentials and tokens, and it sanctions only registered OAuth clients and keyed Partner API integrations. Daffy alone lets a corporation or trust act as a Financial Advisor or Organizer with its own login. Benevity's Match Assurance AI pre-checks and submits match requests while administrators approve by default, so its AI overlay moves from RED to AMBER (provisional): a configurable auto-approval rule can still remove the human. On DAFpay, a sponsor-side `anonymous` flag governs the sponsor's letter. Chariot still pulls the donor's name and contact details, and the grant ID must appear on the remittance. Schwab's custodial feed carries DAF registration codes (DASCG, DASPL); Fidelity's and Pershing's, as documented by BridgeFT, do not. With fees not donor-covered, DAFpay costs nonprofits $5–$29 more per $1,000 than card on all five platforms with published comparisons. Chariot says fee-free subscriptions made up "80% of DAFpay usage" in the past year (undated). Schwab's Online Services Agreement, which binds DAFgiving360 users, treats shared credentials as authorising the recipient and caps Schwab's liability at $100 [V wave 21]. Sources: [queue-batch36-metrics-rails.md](mission-2026-11-14/queue-batch36-metrics-rails.md), [queue-batch36-agent-terms-controls.md](mission-2026-11-14/queue-batch36-agent-terms-controls.md), [queue-batch36-anonymity-feeds-fees.md](mission-2026-11-14/queue-batch36-anonymity-feeds-fees.md), [validation-wave21-report.md](mission-2026-11-14/validation-wave21-report.md). Sources: [queue-batch36-metrics-rails.md](mission-2026-11-14/queue-batch36-metrics-rails.md), [queue-batch36-agent-terms-controls.md](mission-2026-11-14/queue-batch36-agent-terms-controls.md), [queue-batch36-anonymity-feeds-fees.md](mission-2026-11-14/queue-batch36-anonymity-feeds-fees.md), [validation-wave21-report.md](mission-2026-11-14/validation-wave21-report.md).

### 11.17 Batch 37 (validated, wave 22)

**Batch 37 (validated, wave 22).** Ren's revenue is not public. Its named receipts in sponsor 990s, a floor limited to top-five contractor lines, were $44.98m in TY2024 from 18 sponsors. RCF (42.7%) and the two Morgan Stanley programs (43.0%) account for 85.8%. Chariot has filed one Form D ($10,999,978 from 59 investors, 2024), and nothing public points to a sale. Foundation Source's GTCR-era debt is held by Audax Private Credit Fund at par: a term loan and DDTL due 2030-09-06 and a revolver due 2029-09-06. Audax's small LP stake is marked at 1.38x cost, against 1.44x at end-2025. JMI still lists Bloomerang as a holding without an exit status. Goldman's flagship DAF paid its own affiliates (GS Trust, GS & Co), Oak Hill, Ayco and Sapient as its top five contractors in CY2024. Ren's Stellar unit no longer appears among them, although the separate Goldman Sachs Charitable Gift Fund still pays Stellar directly. Registered funds hold about $212m of funded Bonterra debt at 97.7–98.3% of par; a BDC, FS KKR Capital Corp, is the largest funded holder ($149.6m). No N-PORT holding names Ren, Foundation Source, Benevity, Bloomerang or Chariot. Fidelity Charitable's audited adviser-managed (CIAP) share of investments rose from 42.6% (2023) to 46.9% (2025); no sponsor publishes an adviser-managed account split. No sponsor reports DAF-to-DAF grants separately. DAFgiving360's $977m grant to Fidelity was 3.7% of Fidelity's FY2025 DAF contributions. NPT's 990 discloses a Wells Fargo-managed DAF channel only through excess-benefit corrections. The line-6 "No" false-negative tail adds a few small workplace-giving sponsors but not money: Groundswell's amended return reports 12,808 DAFs and $10.1m while still answering "No". Of DAFRC's FY2024 imputations, 48 asset rows ($593.5m) and 45 account rows remain unresolvable from filings. On payment redirection, the Commerce OIG's July 2026 benchmark asks for a callback, dual approval and sender checks. Fidelity documents verifier checks, a wet signature and a discretionary callback to the charity's public number. Vanguard and NPT avoid holding bank details by paying through PayPal. Chariot (and Daffy through it) restricts bank changes to the account Owner, with mandatory 2FA. On DAFpay the nonprofit sees what the donor provides, whatever the anonymity flag. Daffy disclaims reviewing the authority of corporate or trust designees. No probability survey measures DAF ownership: the 2022 SCF expressly excludes DAFs. The four largest national sponsors are the Premier Partners of the American College's DAF Forum 2027, and the adviser curricula outlines read contain no payout, fee or portability items [V wave 22]. Sources: [queue-batch37-vendor-economics-owners.md](mission-2026-11-14/queue-batch37-vendor-economics-owners.md), [queue-batch37-filing-questions.md](mission-2026-11-14/queue-batch37-filing-questions.md), [queue-batch37-controls-education.md](mission-2026-11-14/queue-batch37-controls-education.md), [validation-wave22-report.md](mission-2026-11-14/validation-wave22-report.md). Sources: [queue-batch37-vendor-economics-owners.md](mission-2026-11-14/queue-batch37-vendor-economics-owners.md), [queue-batch37-filing-questions.md](mission-2026-11-14/queue-batch37-filing-questions.md), [queue-batch37-controls-education.md](mission-2026-11-14/queue-batch37-controls-education.md), [validation-wave22-report.md](mission-2026-11-14/validation-wave22-report.md).

### 11.18 Batch 38 (validated, wave 23)

**Batch 38 (validated, wave 23).** NPT documents donor export: its "How to Access Fund Activity" tutorial (PDF created 2026-03-23) says donors can "export the data in any table to an Excel file", and the live GivingPoint code carries the same export text with no per-program switch. FFTC's fundholders moved to a GiftingNetwork portal ("new portal … re-register"). Its ledger is probably Financial Edge NXT on vendor evidence, but its go-live date is not public. GWCF is still the only sponsor that publicly pays grants through Blackbaud's Payment Assistant with REPAY. Give Interactive's "$40B+" is consistent with its known clients at 2025 asset levels ($41.80bn with Vanguard Charitable at $27.01bn), but $9.21bn (corrected from $9.81bn; [crtsh-resourcing-2026-11-19.md](mission-2026-11-14/crtsh-resourcing-2026-11-19.md)) of that rests on CT-discovered, DNS-confirmed implementation hosts rather than live portals. Without them the total is $32.59bn. A full-text screen of 126,684 line-6 "No" returns found 3 more likely sponsors and only $2.96m of Part I value, so the false-negative tail adds sponsors, not money. MS GIFT's line-3 investment income fell from 39.2 to 4.8 bps of public securities between FY2023 and FY2024 while its cash doubled, with no fee line to explain it. A booking change is the likely reading, but it is unproven. Recipient-side weights raise the R5 netting for the 11 largest recipients from $4.39bn to $4.80bn. In FY2024 the aggregate DAF payout was 25.9%, 22.8% excluding DAF-to-DAF transfers, while the median sponsor with $1m or more of DAF assets paid out 12.7% and one in five paid under 5%. The BDC parser now dates all KKR FS Income Trust rows, which shows KKR's Momentive (Community Brands) facility held at 96.1% of par. Its two Barings Envestnet rows are mis-parsed. NPT is the only large sponsor with any FTE figure (at most $136k of wages per FTE). Neither the 2025 SCF nor PSID 2023/2025 measures DAF holding. Funraise removes the anonymous option for DAFpay. The College publishes employers for 7 of 22 DAFCP instructors, none at a sponsor. Sponsors' observed core-platform payments run $118k–$498k a year (median about $218k). Fidelity Charitable's Android app shows launch crashes from v5.11 to v5.18 (2025-10 to 2026-08). crt.sh disallows all crawlers. Report claims resting only on its certificate data are unverified leads: Philanthropi's renewals, the CCT host date, and the stage of five Give implementation hosts [V wave 23]. Sources: [queue-batch38-vendors-ledgers-portals.md](mission-2026-11-14/queue-batch38-vendors-ledgers-portals.md), [queue-batch38-data-followups.md](mission-2026-11-14/queue-batch38-data-followups.md), [queue-batch38-closeout-checks.md](mission-2026-11-14/queue-batch38-closeout-checks.md), [compliance-note-crtsh-robots.md](mission-2026-11-14/compliance-note-crtsh-robots.md), [validation-wave23-report.md](mission-2026-11-14/validation-wave23-report.md).

### 11.19 New directions N5–N8 (validated, wave 24B)

**New directions N5–N8 (validated, wave 24B).**
   > - **News.** GDELT counts 9,486 English articles naming donor-advised funds in 2021 to 2026-11-14. Per million articles monitored, coverage fell from 22–27 (2021–22) to 12.1 (2025H1) and recovered to about 22 in 2026. Legislation and tax framing dominates (34% of articles), payout reform peaked in 2021 (20%), and AI is a small but rising frame (1.2% → 5.8%). The themes do not show the 2026 rebound is policy-led.
   > - **Hiring.** A snapshot of 168 open roles at 12 employers finds AI named in 29% of vendor roles against 13% at sponsors. None of Fidelity Charitable's 11 roles mentions AI. Chariot is hiring an Applied AI Engineer and an agentic-infrastructure engineer. Job ads show intent, not deployment.
   > - **Donate pages.** Among the 300 charities receiving the most DAF dollars ($24.08bn), 186 donate pages could be scanned. 13–14% show DAFpay, about 2% DAF Direct, and about 41% any DAF option. Most of those offer text instructions only.
   > - **Donor behaviour.** No sponsor publishes donor age or gender; BofA finds 9% of wealthy individuals, and 20% of those aged 21–45, use a DAF. Fidelity's median account was $27,860 in 2025, after a 19% fall in 2022, and its average grant $5,801. Medians are small: DAFgiving360 $500 [S], Daffy $100. Crisis responses are modest next to annual flows: Fidelity's more than $128m for Ukraine (H1 2022) and about $50m for Helene/Milton.
   > - **Literature.** Account-level studies (DAFRC 2024: a 9% median account payout, 22% of accounts inactive in 2020–22) qualify, but do not contradict, the 23.9% aggregate. The spread of published payout rates is largely definitional. Sources: [direction-news-hiring-signals.md](mission-2026-11-14/direction-news-hiring-signals.md), [direction-nonprofit-donate-pages.md](mission-2026-11-14/direction-nonprofit-donate-pages.md), [direction-donor-behaviour-crises.md](mission-2026-11-14/direction-donor-behaviour-crises.md), [direction-academic-literature.md](mission-2026-11-14/direction-academic-literature.md), [validation-wave24b-report.md](mission-2026-11-14/validation-wave24b-report.md).

### 11.20 New directions N1–N4 (validated, wave 24A)

**New directions N1–N4 (validated, wave 24A).** The 2023 proposed DAF regulations are still proposed: docket IRS-2023-0053 holds 249 public submissions (173 in the comment period, 63 hearing requests and outlines, and 13 new ones in May–June 2026 from AEF, RCF, Ren, SIFMA, the ABA and NYSBA tax sections and others), no final rule, and a 2026–27 Priority Guidance Plan item for "guidance under §§4966 and 6033 regarding certain donor advised fund arrangements". Federal lobbying filings that name DAFs come from 33 clients (359 filings, 2021–2026 Q3; whole-filing amounts): Vanguard Charitable $1.74m, NPT $1.09m and Fidelity Charitable $180k; AEF and Ren Acquisition first registered on 2024-02-01. From 2026 the new $1,000/$2,000 non-itemizer deduction excludes gifts to DAFs, and the 0.5% floor and 35% value cap reward bunching; Fidelity Charitable attributes part of its 13.4% account growth in 2025 to bunching, and Giving USA puts accelerated individual giving at about $1.71bn. No DAF incumbent holds a 2021+ giving patent found by a citation crawl (TIFIN's US12705394B2 is a generic LLM-privacy patent), and no Item 1.05 cyber 8-K came from a DAF-linked issuer except Coinbase; the reference enforcement case remains Blackbaud's 2020 breach (SEC $3m, 49 states and DC $49.5m, an FTC order, California $6.75m). Abroad, Canada (3.5%/5% disbursement quota; C$16.6bn in DAFs at 834 charities) and Australia (4%/5% today; 6% decided on 2026-02-26) set sponsor-level payout floors, while the UK (£3.1bn; 28.3% payout) has none; US vendors appear abroad only at adviser and community-foundation sponsors (Ren at NPT UK, Foundant at ACF, NPact at Calgary). Among the top 50 sponsors, $77.34bn of FY2023–24 Schedule I grants (after $12.70bn of DAF-to-DAF transfers) went 25.8% to education, 14.3% to human services, 14.1% to public-society benefit and 13.6% to religion, with the top 100 recipients taking 24.3%. National sponsors skew to education and religion, community foundations to human services and health, and Silicon Valley CF supplies most community-foundation DAF-to-DAF flows. Impact-labelled DAF capital is published only by Fidelity ($4.6B, self-reported) and ImpactAssets ($2.90bn filed) [V wave 24A]. Sources: [direction-policy-lobbying-obbba.md](mission-2026-11-14/direction-policy-lobbying-obbba.md), [direction-patents-security.md](mission-2026-11-14/direction-patents-security.md), [direction-international-comparison.md](mission-2026-11-14/direction-international-comparison.md), [direction-recipients-impact-matching.md](mission-2026-11-14/direction-recipients-impact-matching.md), [validation-wave24a-report.md](mission-2026-11-14/validation-wave24a-report.md).

### 11.21 New directions N12–N14 (validated, wave 25B)

**New directions N12–N14 (validated, wave 25B).**
   > - **Nonprofit-side benchmarks.** The only nonprofit-file series is vendor-run.
   >   - Chariot/K2D 2026 finds DAFs at "nearly 13%" of $26.1bn in total giving across 54 large nonprofits ($3.3bn from 907,000 gifts, under 1% of gift count). DAFs supply more than 22% of major-gift revenue although only 2% of DAF gifts are major gifts. The median DAF gift is $300.
   >   - Earlier editions: a 12% median share in 2023 (20 organisations), and 15% for participants under $10m in 2024.
   >   - M+R 2025 reports $0.13 of DAF revenue per online dollar, ranging from $0.01 in Health to $0.49 in Environmental. M+R's DAF revenue rose 6% in 2024 and 44% in 2025, and its average DAF gift was $1,430.
   >   - Repo cross-check: FY2024 netted DAF grants of $58.41bn equal 9.9% of Giving USA's CY2024 total and 14.9% of individual giving. This is consistent with, and slightly below, the DAF-forward vendor panels.
   > - **Data standards.** No open, multi-sponsor DAF grant standard exists.
   >   - DAF Direct is closed and has 3 sponsors.
   >   - Chariot's DAFpay guide is the de facto spec. It is vendor-certified and carries Chariot's own correlation ID, which sponsors must print on the remittance.
   >   - Remittance travels outside the payment. At Fidelity, ACH grant details are emailed daily.
   >   - Public IRS schemas lag what is filed: TEOS lists 2024v5.0, while filed returns use 2024v5.5.
   >   - The closest US template is the federal Grants Data Standards v3.0 (2026-06-17).
   >   - The section 1033 rule is enjoined and its reconsideration NPRM unpublished. DAF accounts are probably out of its scope.
   > - **Non-cash gifts.**
   >   - Dechomai carries the largest visible complex-asset flows. It took in $525m–$986m a year in 2021–23, received $12–26m a year from DAFgiving360 and $56.7m from Fidelity (FY6/22, amended return), and is AEF's stated partner for illiquid gifts.
   >   - Fidelity took $2.6bn of non-publicly traded assets in 2025, with no extra fee and 65 days on average to liquidity.
   >   - NPT screens with minimums of $25k–$2m.
   >   - Nonprofit-side vendors charge 1.5–3.9% a gift (GivingIQ, published). Sources: [direction-nonprofit-daf-benchmarks.md](mission-2026-11-14/direction-nonprofit-daf-benchmarks.md), [direction-data-standards-interoperability.md](mission-2026-11-14/direction-data-standards-interoperability.md), [direction-noncash-gift-infrastructure.md](mission-2026-11-14/direction-noncash-gift-infrastructure.md), [validation-wave25b-report.md](mission-2026-11-14/validation-wave25b-report.md).

### 11.22 New directions N9–N11 (validated, wave 25A)

**New directions N9–N11 (validated, wave 25A).** No state has a DAF reporting, payout or donor-intent mandate found for 2021–2026. California's DAF bills all failed: AB 1712 and AB 2936 in 2020, and AB 1353, which died at the desk on 2022-02-01. The California AG has no DAF-specific registration form; its 2022 DAF report (57 sponsors, $105.3bn) created no filing duty. State rules that do name DAFs are narrower:
   > - **Platform laws.** California's AB 488 (Gov. Code §12599.9, in force from 2023; regulations 2024–25) and Hawaii's Act 205 as amended by Act 108 (effective 2026-07-01) treat a DAF sponsor as a regulated platform only if it names charities to people without advisory privileges.
   > - **Political disclosure.** California FPPC Reg. 18424.3 (operative 2021-12-22) makes officials name the sponsor, fund and donor behind DAF-sourced behested payments; 33 of 2,029 state reports used it, totalling $1,242,728.
   > - **Tax credits.** Illinois Gives and Kansas's pregnancy-resource credit (K.A.R. 92-12-152, effective 2026-04-17) exclude DAF gifts.
   > - **Wealth taxes.** New York's pending A3632 would count DAF gifts. California's Proposition 40, whose transfer rule would have done the same, was rejected (about 52.8% no, unofficial).
   > - **AG letters.** Sixteen attorneys general wrote to Fidelity Charitable, Vanguard Charitable and DACG on 2026-05-21 urging them to reconsider SPLC payment holds, with no legal demand. A 21-state letter to GoFundMe (19 AGs and 4 secretaries of state, 2026-03-03) demanded disclosure of "the role and nature of any DAF sponsor".
   >
   > Among the top-20 sponsors, 13 sites ($173.8bn of $250.6bn) could be scanned. Automated axe-core checks found critical WCAG failures on 7 of 37 pages, at NPT, Vanguard, SVCF and NCF, and serious failures (mostly colour contrast) on 22. A same-day re-scan of 21 pages reproduced every count. These are partial automated checks, not a ranking. No readable sponsor publishes a response-time promise, a public chat channel or a WCAG conformance claim. Three publish phone hours, AEF's accessibility statement is placeholder text, and FFTC relies on the accessiBe overlay.
   >
   > Community-foundation consolidation in 2021–2026 was small. No two top-100 CFs combined, and only 5 of 803 DAFRC CF filers reported a >25% disposition or final return. The largest events were Orange & Sullivan with Rockland (NY AG-approved; about $71m), Coastal CF into San Diego Foundation ($10.07m), Keweenaw into the CF of the Upper Peninsula ($10.55m) and a $21.6m Watertown transfer that may be a reorganisation. 34 top-100 CFs (43% of top-100 CF DAF assets) publish a full fee schedule. Their median admin fee is 100 / 100 / 67 bps at $100k / $1m / $10m, about 1.7x, 2.2x and 3.6–4.7x the national sponsors' 60 / 45 / 14–19 bps, before investment costs. [V wave 25A] Sources: [direction-state-daf-law-tracker.md](mission-2026-11-14/direction-state-daf-law-tracker.md), [direction-sponsor-accessibility-service.md](mission-2026-11-14/direction-sponsor-accessibility-service.md), [direction-cf-consolidation-fees.md](mission-2026-11-14/direction-cf-consolidation-fees.md), [validation-wave25a-report.md](mission-2026-11-14/validation-wave25a-report.md).

### 11.23 New directions N15–N18 (validated, wave 26)

**New directions N15–N18 (validated, wave 26).**
   > - **Faith giving.** Church giving platforms do not offer DAF grants at checkout.
   >   - Only Overflow does, through Chariot since June 2023. Pushpay lists DAF attribution as "coming soon".
   >   - Subsplash and Planning Center record DAF gifts after the fact. Tithely, Givelify, Kindrid and ACST/Vanco show nothing.
   >   - Faith sponsors pay congregations directly. NCF pays by ACH or electronic transfer, and JCF NY by check or ACH/wire at staff discretion. JCF NY's median grant is $750.
   >   - Religion is 27% of Fidelity's grant count but 13.1% of its dollars (implied average about $2,815). In the repo's Schedule I it is 13.6% of dollars across 55,993 recipients. The 22 top-300 religion recipients hold only 15% of religion's $10.55bn, and none of the scanned ones is a congregation.
   > - **Gift offices.** Recipients split on whether a DAF grant can pay a pledge.
   >   - Caltech and Stanford Live allow it if the sponsor does not mention the pledge. WashU and Chicago Booth bar it. Duke books only a "non-binding intention".
   >   - Fidelity accepts non-binding pledges. Vanguard and Daffy bar binding ones, and all three bar bifurcated event payments.
   >   - Ohio State Athletics excludes DAFgiving360 gifts from priority points.
   >   - At least 12 of the 33 largest university and AMC recipients run their own DAF.
   >   - Four large universities offer DAFpay or DAF Direct one step past the scanned donate URL. The donate-page share of 41.2% is therefore a lower bound (43.4% counting them).
   > - **Recipient compliance.** Screening 604,915 top-50 Schedule I lines ($91.02bn) against IRS lists finds:
   >   - 0.082% ($74.8m) went to EINs under a revocation in effect at the time. $53.1m of those recipients are listed again today, and only $10.5m is posted, unlisted and unexplained.
   >   - The $8.01bn absent from Pub 78 is mostly subordinates, churches, governmental units and CZ Biohub LLCs. $0.82bn (0.90%) is unexplained and most likely EIN error.
   >   - These are screening hits, not findings of improper grants. The script reproduces exactly.
   > - **Corporate DAFs.** 49 company programs appear in 2021–2026 filings. Tides is the most-named sponsor (8), then SVCF (4) and Fidelity (3), and 26 programs do not name a sponsor.
   >   - Published corporate splits: Fidelity, 556 corporate DAFs granting $539.8m in 2025; SVCF corporate-advised funds, about $153m (2025) and $189m (2024); AOGF/Benevity, 695 DAF-column accounts granting $1.39bn (FYE 2026-03).
   >   - Notable programs: Apollo's $200m share-funded DAF, Urban Outfitters' $46m prefunding, Cognizant's 2022 conversion of its foundation to a DAF, and Circle's Pledge 1% DAF at Fidelity. Sources: [direction-faith-giving-platforms.md](mission-2026-11-14/direction-faith-giving-platforms.md), [direction-gift-office-daf-handling.md](mission-2026-11-14/direction-gift-office-daf-handling.md), [direction-recipient-compliance-screen.md](mission-2026-11-14/direction-recipient-compliance-screen.md), [direction-corporate-dafs.md](mission-2026-11-14/direction-corporate-dafs.md), [validation-wave26-report.md](mission-2026-11-14/validation-wave26-report.md).

### 11.24 New directions N19–N22 (validated, wave 27)

**New directions N19–N22 (validated, wave 27).**
   > - **Investment menus and performance.** At least 6 of the top-20 sponsors publish pool returns against benchmarks: Fidelity, Vanguard Charitable, FFTC, GKCCF, Greater Horizons (identical figures to GKCCF) and CJP. NPT publishes returns without benchmarks. NCF relaunched its pools on 2026-09-01 and so far shows benchmark-only pro forma figures.
   >   - Index menus track within about 0.1 pp. Vanguard's 5-year median is −0.04 pp; GKCCF's is −0.09 pp to 2025-12-31.
   >   - Fidelity's 7 asset-allocation pools trail by 0.58–0.76 pp over 5 years. Fidelity's returns include its admin fee, and the gap matches it: each pool trails its own underlying fund by about 0.6 pp.
   >   - ESG and impact options trailed over trailing windows dominated by 2022–23: GKCCF −2.4 pp and Fidelity −1.2 pp.
   >   - Adviser-managed minimums run from $25k (AEF) and $100k (GKCCF; Fidelity CIAP per repo) to $5m (SVCF, GS IMAP).
   > - **Donor tax 2026 (illustrative, not tax advice).** Every parameter matches P.L. 119-21, Rev. Proc. 2025-32 and IRS guidance, and the script reproduces exactly.
   >   - A DAF never beats a direct gift of the same asset in the same year. It loses for non-itemizers, because DAF gifts are excluded from the $2,000 joint non-itemizer deduction (H1: $720 vs $0).
   >   - Bunching pays near the standard deduction (+$3,672 for H2).
   >   - The 35% cap holds the value of each deductible dollar to $0.35.
   >   - Giving stock in kind is the largest lever for any vehicle: $4.5k, $28.8k and $191k in the three profiles.
   >   - Private-foundation figures: $11,120 excise if the donated stock is sold. The "$447k never used" at a $1.5m gift depends on an interpretation of the 0.5% floor for carryovers (about $437k otherwise).
   > - **Grant geography (FY2023–24, top-50 sponsors, ex university/hospital).**
   >   - CA 20.0%, NY 13.6%, DC 6.4%, MA 6.0% and MD 4.7% of dollars. The top 5 hold 50.7% of dollars against 21.4% of population.
   >   - $113 per resident nationally and $3,550 in DC; $23,240 per registered 501(c)(3).
   >   - Community foundations keep 60% in state (median 71%; Chicago Community Trust 20%, San Diego 92%), against 7.6% for national sponsors.
   >   - Schedule I addresses match BMF states for 94.4% of dollars. Lockbox addresses inflate Iowa ($644m vs $231m).
   >   - The script reproduces on every state row.
   > - **Donor feature census.** Table stakes are stock, complex-asset and crypto acceptance, recurring grants, search and vetting, family roles and adviser access.
   >   - Differentiators sit with digital-first sponsors: Daffy's member MCP server, app, campaigns and CSV export; TIFIN Give's AI assistant; Endaoment's API.
   >   - Fidelity's app had 24 iOS ratings and Daffy's 560 on 2026-11-15.
   >   - 267 of 476 cells remain unassessed, so absences are "not found", not proven. Sources: [direction-investment-menus-performance.md](mission-2026-11-14/direction-investment-menus-performance.md), [direction-donor-tax-scenarios-2026.md](mission-2026-11-14/direction-donor-tax-scenarios-2026.md), [direction-grant-geography.md](mission-2026-11-14/direction-grant-geography.md), [direction-donor-feature-census.md](mission-2026-11-14/direction-donor-feature-census.md), [validation-wave27-report.md](mission-2026-11-14/validation-wave27-report.md).

### 11.25 New directions N23–N26 (validated, wave 28)

**New directions N23–N26 (validated, wave 28).**
   > - **Sponsor marketing spend (Form 990 line 12, TY2021–24; both scripts reproduce exactly).**
   >   - Reported advertising is tiny at nationals: affiliated-commercial sponsors $21.7m (1.39 bps of DAF contributions), of which Schwab is $20.3m (about $390 per net new account). Without Schwab it is $1.36m.
   >   - Independent nationals: $3.1m (0.41 bps). Digital-first: $0.17m (1.7 bps; 6.6 bps with Endaoment's line-24 marketing).
   >   - Fidelity reports $0 on line 12 and $121–180m a year of administrator fees on line 11a. Parent- and platform-paid marketing is off the 990, so line 12 is a lower bound.
   >   - Community foundations: $67.2m, about 18 bps of DAF contributions (12.7 bps allocated) and $7,981 per net new account. Across CFs, advertising intensity is not positively ranked with account growth (ρ −0.25, n=55).
   > - **Executive compensation (top 50, TY2024).**
   >   - 10 of 12 affiliated-commercial sponsors carry no paid executive on their own 990. Staff are the parent's (Schedule O: FMR services agreement; 474 MS Services/Eaton Vance; Schwab employees), or a bank trustee is paid (BofA $24.1m).
   >   - Pooled staff cost: 2.9 bps of DAF assets for affiliated sponsors against 78.7 bps at community foundations.
   >   - Top-officer pay per $bn of DAF assets: NPT $14k, DAFgiving360 $20k and Vanguard $23k, against a CF median of $734k. Median CF top pay is $725k and barely scales with size (elasticity 0.23).
   >   - Related-organisation pay is concentrated at Greater Horizons (90%), The Signatry (93%) and the UCLA Foundation (85%).
   > - **AI products (30 rows).**
   >   - No product meets the RED test. Only TIFIN Louise and Daffy's MCP server can move DAF money, and both end in sponsor review. Fidelity's assistant is search only. Foundation Source's CEO (2026-10-28) describes a roadmap AI screening tool framed as a flag for review.
   >   - Grantmaking tools (SmartSimple, Fluxx Finn, YourCause) document opt-in, no-training and human-decision controls (provisional GREEN). Givebutter Magic is a GREEN/AMBER boundary case.
   >   - "Blackbaud Copilot" did exist as a Blackbaud assistant name in 2024–25. Classy is now GoFundMe Pro.
   > - **Charity ratings in DAF platforms.**
   >   - No top-20 sponsor shows CN ratings in its grant flow. Where a search vendor is named, it is Candid/GuideStar (BofA's 2025 guide; Groundswell). CN's own Giving Basket takes DAF grants via Chariot DAFpay at 2.9%.
   >   - CN's API licence is non-sublicensable, requires a linkback and bars using ratings "in any other calculation", which constrains AI rankers.
   >   - CN rates 245,000+ charities, about 17% of Pub 78 records.
   >   - Church grants in the BMF but not Pub 78 ($2.17bn in the top-50 sample) are mostly group-ruling subordinates: a ratings gap, not an eligibility gap. Sources: [direction-sponsor-marketing-spend.md](mission-2026-11-14/direction-sponsor-marketing-spend.md), [direction-sponsor-executive-compensation.md](mission-2026-11-14/direction-sponsor-executive-compensation.md), [direction-ai-product-census.md](mission-2026-11-14/direction-ai-product-census.md), [direction-charity-ratings-integrations.md](mission-2026-11-14/direction-charity-ratings-integrations.md), [validation-wave28-report.md](mission-2026-11-14/validation-wave28-report.md).

### 11.26 New directions N27–N30 (validated, wave 29)

**New directions N27–N30 (validated, wave 29).**
   > - **Sponsor financial resilience (Form 990, TY2021–24, top 100; the script reproduces exactly from a fresh download of all 415 returns).**
   >   - At national sponsors, DAFs are 99–100% of net assets, so the 990 can only bound a sponsor's own reserve. Median non-DAF net assets cover 29.4 months of operating cost at bank- and broker-affiliated nationals, against 2.2 months at independent nationals.
   >   - Several nationals show zero or negative non-DAF net assets. At MS GIFT the gap equals its liabilities exactly (−$133m in TY2024), so Schedule D reports DAF value before liabilities. NPT, Renaissance, CAF America and AOGF are also below zero.
   >   - Fidelity's non-DAF net assets are exactly its Schedule D "other funds" ($381m). Program-service revenue is $0 at all 15 affiliated sponsors: the DAF fee is an internal transfer.
   >   - Community foundations show 417 months of cover, but only 1.6 months once board-designated endowment is excluded.
   >   - NPT's FY2023 Schedule D value ($22.84bn against $27.92bn of net assets) is a real filed figure, very likely a filer error: NPT's consolidated statements report $28.51bn of net assets at 2023-06-30 [V wave 34A].
   > - **Nonprofit-side experience (60 coded rows, 2021–26).**
   >   - Identity and data issues lead the nonprofit complaints: 16 of 48, and 15 of 34 excluding Benevity.
   >   - Defaults, not chosen anonymity, drive the problem. Only 36% of sponsors default to full contact data, and 35% to fund name only (DAFRC, 128 sponsors, 86% community foundations). At the FY2024 top 20, full contact is the documented default for 33.2% of assets and withholding for 17.2%, and 44.6% is undocumented [V wave 34A]. Only 49% of donors say they are always thanked.
   >   - In Chariot's one-nonprofit sample, check-paying providers took 7–162 days and the fastest ACH providers 1–2 days.
   >   - Only the donor can trigger a Fidelity reissue. YourCause's forfeiture rule is a workplace-giving rule.
   >   - AFP's DAF curriculum is funded by Fidelity Charitable. NPT's "79% partially anonymous" headline is not supported by DAFRC data.
   > - **Public opinion (2021–26).**
   >   - The only DAF policy polls are advocate-sponsored Ipsos opt-ins (n=1,005): 69% (2022) and 71% (2024) back a 10% payout, and support for granting within 5 years rose from 72% to 79%.
   >   - Only 17–19% know how DAFs work (Lilly: 11.4% familiar).
   >   - Trust in high-net-worth philanthropy is 29% (2025), and trust in philanthropy fell from 33% to 29% (2026). Universal-deduction support runs at 85–88%.
   >   - Elite opinion runs against reform, including a 33-member Ways and Means letter (2024).
   > - **League table and concentration (corrected DAFRC values; reproduced and independently rebuilt).**
   >   - Fidelity holds 20.5–21.7% of assets. NPT ($42.12bn) passed DAFgiving360 ($40.94bn) in FY2024. The top 50 hold 83–86% of assets and 78–81% of grants.
   >   - Asset concentration rose (CR5 51.0 → 56.9%, HHI 734 → 853) while grant concentration fell (CR5 53.6 → 46.6%, HHI 803 → 653). Both are "unconcentrated" by HHI, and R5 netting barely moves them (FY2024 grant HHI 669).
   >   - FY2023 uses NPT's anomalous filed value. Corrected, CR5 would be about 53.8% instead of 52.9%.
   >   - FY2025 is partial: 899 filers, 67.6% of assets. Sources: [direction-sponsor-financial-resilience.md](mission-2026-11-14/direction-sponsor-financial-resilience.md), [direction-nonprofit-side-experience.md](mission-2026-11-14/direction-nonprofit-side-experience.md), [direction-public-opinion-dafs.md](mission-2026-11-14/direction-public-opinion-dafs.md), [direction-league-table-concentration.md](mission-2026-11-14/direction-league-table-concentration.md), [validation-wave29-report.md](mission-2026-11-14/validation-wave29-report.md).

### 11.27 New directions N31–N33 (validated, wave 30)

**New directions N31–N33 (validated, wave 30).**
   > - **Foreign grants (Form 990 Part IX line 3 and Schedule F, top 50, FY2023–24; reproduced from a fresh download of all 118 returns).**
   >   - Direct foreign grants are **$1.89bn of $98.27bn, 1.92%** ($845m in FY2023, $1,046m in FY2024).
   >   - NPT gives 39% of the dollars, SVCF 19% and GS DAF 9.5%. Fidelity sends 0.5% of its grants abroad directly.
   >   - Community foundations 2.60%, nationals 1.75%. Europe takes 49.6% and the Middle East and North Africa 12.4%.
   >   - Narratives describing equivalency determination or expenditure responsibility cover 41 sponsor-years and about 95% of foreign dollars.
   >   - SVCF reports 539 of the 672 foreign recipients not shown to be 501(c)(3)-equivalent.
   >   - Nine US intermediaries received $216m, of which about $165m is estimated to have gone abroad. "Friends of" organisations received $433m.
   >   - NPT's FY2024 Schedule F has shifted columns ($410m, verified in the XML and repaired).
   >   - Adding direct foreign grants lifts the international share of DAF grants from 5.6% (Schedule I, NTEE Q) to 7.8%.
   > - **Recipient lobbying (Schedule C, top-50 recipients; reproduced from a fresh download of 13,011 returns; 19 returns hand-checked).**
   >   - Of $77.3bn of net DAF grants, 71.2% go to recipients with a parseable 501(c)(3) return. Of those covered dollars, **42.2% go to recipients that report any lobbying** (30.0–58.8% of all dollars). By count the share is 20%.
   >   - The share is highest for environment (61%), education (55%) and health (51%) recipients, and lowest for religion (7%, mostly uncovered churches). It is 45.9% at national sponsors and 34.7% at community foundations.
   >   - Lobbying is a small part of recipients' spending: median 0.20% of expenses, and none above 20%.
   >   - 36 of 12,985 recipients (0.13% of covered dollars) disclose political campaign activity. These are self-disclosures needing review.
   >   - Schedule C is self-reported. The measure describes recipients, not the use of DAF grants.
   > - **The long tail (corrected DAFRC panel, FY2021–24; reproduced exactly).**
   >   - 1,240 of 1,514 sponsors hold under $50m: $9.18bn, 2.84% of assets. 947 hold under $10m (0.69%) and 423 under $1m (0.04%). The top 50 hold 85.5%.
   >   - Without Givinga and the terminated BNY Mellon fund, the tail's 46.4% of accounts is 3.49%.
   >   - Half the tail sponsors are community foundations; the median tail sponsor is 29 years old.
   >   - The median tail sponsor has 24 DAFs averaging $133k (top 50: 1,464 and $836k). Its median payout is 11.7% (top 50: 19.6%), and 26.8% pay out under 5% (37.6% under $1m).
   >   - 134 of the 138 FY2021–24 entrants and 85 of the 90 candidate exits are in the tail.
   >   - Foundant serves 80% of tail CFs with an identified vendor, and 38% show none.
   >   - No tail sponsor has a published fee in the repo. AI-native implications are inference only. Sources: [direction-foreign-grants-schedule-f.md](mission-2026-11-14/direction-foreign-grants-schedule-f.md), [direction-recipient-lobbying.md](mission-2026-11-14/direction-recipient-lobbying.md), [direction-long-tail-sponsors.md](mission-2026-11-14/direction-long-tail-sponsors.md), [validation-wave30-report.md](mission-2026-11-14/validation-wave30-report.md).

### 11.28 Thoroughness pass part B (validated, wave 31B)

**Thoroughness pass part B (validated, wave 31B).**
   > - **crt.sh re-sourcing (DNS re-run of 167 hosts on 2026-11-19; no crt.sh or certspotter request).**
   >   - Of 139 Give Interactive hostnames, 89 still resolve. donorsphere.org and donor-portal.org answer any label (DNS wildcards), so their certificate-only tenant labels count for nothing.
   >   - Give's nine known clients hold $36.74bn of FY2024 DAF assets on DNS evidence. Only $23.90bn (Vanguard Charitable, The Signatry and WaterStone) rests on first-party or filing evidence. These figures use the DAFRC values; with ImpactAssets at its filed $2.90bn, the DNS-only part is $12.1bn.
   >   - The five clients discovered from certificate logs hold $9.21bn, not $9.81bn. Without them the total is $32.59bn.
   >   - On admissible evidence Give lost three community-foundation tenants (East Bay, Carolinas and Kalamazoo, $3.56bn on DAFRC values), not five.
   >   - Only $6.06bn of tenants (The Signatry and CCT) is dated before September 2025.
   >   - Certspotter is no longer used, because its operator's robots.txt disallows its API.
   > - **Second sources.**
   >   - Give Interactive's Vanguard Charitable mandate rests on a release Give issued. Vanguard Charitable's FY2026 audited statements do not mention it and show no software capitalised.
   >   - RCF's sponsorship of the Commonwealth Charitable Fund is confirmed by its circular and the West Virginia registry.
   >   - Bain Capital's 2023 release adds a third Ren SOC 2 statement ("Type 1").
   >   - DAFgiving360's tiered fee is confirmed in its December 2024 Program Policies.
   >   - Sixteen attorneys general wrote to Fidelity Charitable, DAFgiving360's sponsor and Vanguard Charitable on 2026-05-21 about SPLC payment restrictions.
   > - **Wealth channels.**
   >   - The Edward Jones Form CRS and advisory brochure name no DAF; its private DAF's sponsor is still undisclosed. The 10-K negatives were not re-read (sec.gov robots).
   >   - SEI runs two DAFs: RCF (Ren) and GiveClear (TIFIN Give).
   >   - Bank of America N.A. is the Charitable Gift Fund's sole trustee, and BofA Private Bank administers it.
   >   - Fidelity Charitable paid Wells Fargo Advisors $3.41m for investment management in FY2025.
   >   - Wells Fargo's live pages no longer name NPT.
   >   - AOGF's PNC payments ($196k, $149k) are labelled like all its contractors and do not show DAF administration.
   > - **AI.** Twelve of the 20 entities were re-read. None documents AI in grant approval or money movement. NCF's AI site search is the one donor-facing feature. Parent-firm AI (Morgan Stanley, SEI, Edward Jones) is not tied to the DAF programs.
   > - **Clarity/EDF.** The four new outcomes follow the EDF v0.3 sequence and alter no validated number. Fidelity's fee-sized shortfall holds only over five years for its active asset-allocation pools, and in every window for Money Market.
   > - **Fees and delivery.**
   >   - Minneapolis, San Francisco and Greater Cincinnati now have 2025–26 fee schedules.
   >   - The CF medians stay 100 / 100 / 67 bps at $100k / $1m / $10m, so the 1.7x / 2.2x / 3.6–4.7x ratios stand. Coverage rises to 37 schedules and 46% of top-100 CF DAF assets once the census is merged.
   >   - Of 39 announced-vs-delivered items, 17 are delivered, 11 partial, 9 without evidence and 2 contradicted (was 15 / 10 / 12 / 2).
   >   - 18 newer announcements add 8 delivered, 3 partial and 7 without evidence. The ImpactAssets DAF hub, promised for 2026-09-08, is overdue. Source: [validation-wave31b-report.md](mission-2026-11-14/validation-wave31b-report.md).

### 11.29 Thoroughness pass part A (validated, wave 31A)

**Thoroughness pass part A (validated, wave 31A).**
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
   >   - Every changed cell has a resolving pointer. Source: [validation-wave31a-report.md](mission-2026-11-14/validation-wave31a-report.md).

### 11.30 Gap-audit batch part A (validated, wave 32A)

**Gap-audit batch part A** (validated, wave 32A). Top-50 sponsors' FY2023–24 Schedule I and F filings were screened for grants that leave the routine "listed, long-recognised US public charity" path. The routes screened were foreign recipients, recipients outside Pub 78 without an explaining label, rulings within 24 months, named fiscal sponsors and private foundations. On that core definition the share is 7.4% of recipient lines and 11.0% of dollars, once one $212.2m totals row is removed. The broad definition gives 25% and 20%; it is count-heavy because of churches and group subordinates. At the four largest nationals the existing "2.5–3%" measure reproduces at 3.6%, about a third of their core 10.0%. Operating foundations ($949m) need no expenditure responsibility under §4966(c)(2)(A). The screen measures recipients, not observed review. A census of 18 DAF entrants from 2021–2026 finds no documented shutdown: 10 active, 1 acquired, 1 pivoted, 6 unknown. Survival is 66.7–100%, with a 3.7%/yr hazard bound if the unknowns survive. Uncommon Giving operated in 2020, so the strict subset (n=8) is the cleaner read (repo [`validation-wave32a-report.md`](mission-2026-11-14/validation-wave32a-report.md)) [V wave 32A]" Source: [validation-wave32a-report.md](mission-2026-11-14/validation-wave32a-report.md).

### 11.31 Gap-audit batch part B (validated, wave 32B)

**Gap-audit batch part B** (validated, wave 32B). Complaint rates were put on FY2024 DAFRC denominators with R1 corrections, using Trustpilot, BBB and Google Play records from 2021 to 2026-11-19. Among the 15 largest sponsors only Fidelity Charitable and RCF (one low-attribution review of its administrator, Ren) have any such record, so zero counts mean "not observed". Fidelity shows 27 review-venue complaints: 1.32 per 10,000 accounts [95% CI 0.87–1.92], or 2.13 per $1bn of grants. AOGF (Benevity) shows 0.78 per 10,000 accounts but 28.7 per $1bn, or 24.1 on US-only reviewers, so the ranking turns on the denominator. Processor complaints describe payout rules: paper-check thresholds, lost checks and EFT vetting. A 51-jurisdiction bill search found no 2021–2026 state payout, account-reporting or donor-intent mandate on DAF sponsors; Connecticut could not be checked. Most state DAF wording is tax treatment. New Jersey's hospital-conversion law, whose DAF clause dates from P.L.2014 c.82, lets a court reallocate unspent conversion assets held in a DAF (repo [`validation-wave32b-report.md`](mission-2026-11-14/validation-wave32b-report.md)) [V wave 32B] Source: [validation-wave32b-report.md](mission-2026-11-14/validation-wave32b-report.md).

### 11.32 New-batch part A (validated, wave 33A)

**New-batch part A** (validated, wave 33A). A filing-based check of vendor DAF-share claims sampled 2,352 charities that received top-50 sponsors' FY2023–24 Schedule I grants and read their own 990s. Universities, hospitals, foundations and panel sponsors were excluded. Top-50 DAF grants are a median 5.9% (95% CI 5.3–7.4%) and a pooled 6.9% (6.1–7.8%) of line 1h contributions. Pooled shares fall from 17.8% under $1m of revenue to 3.7% at $100m and over. Top-50 grants are 67.3% of netted FY2024 DAF grants; scaling by that gives about 10% of 1h, or 15% of private contributions, an inference that leans high. On that basis Chariot's "nearly 13%" lies between the two largest bands. Among 1,220 usable sponsors under $50m, tail community foundations' allocated operating cost is a median 205 bps of DAF assets (rule A), twice top-50 CFs' 102 bps, but 1.6× on an admin-only rule. Tail CFs look cheaper per account only because their accounts are an eighth the size. Re-read processor rules show $100 check thresholds, monthly batches and redirection to charities chosen by the employer or processor. Written rules fully explain two of seven named complaints, but most complaints predate the rule versions read (repo [`validation-wave33a-report.md`](mission-2026-11-14/validation-wave33a-report.md)) [V wave 33A]

### 11.33 New-batch part B (validated, wave 33B)

**New-batch part B** (validated, wave 33B). Notice 2017-73 §4 still governs DAF pledge payments. Taxpayers "may rely" on it "until additional guidance is issued" (§7), and the Federal Register to 2026-11-19 holds only the 2023 §4966 proposal, which recites §4 as background. The §4967 prohibited-benefits project is in the 2023–24 and 2024–25 Priority Guidance Plans but not the 2025–26 or 2026–27 plans; the 2026–27 plan adds §§4966/6033 guidance on "certain donor advised fund arrangements". Of the top-30 university and medical gift offices, 2 ($841.5m of FY2023–24 DAF grants) publish the notice's rule, 8 ($852.9m) forbid DAF payment of personal or binding pledges or book DAF commitments as non-binding, and 20 ($5,418.7m) are silent or unread. Among the top-15 sponsors AEF [F] and NPT [S] follow the notice and five bar binding pledges. Under P.L. 119-21, six of the seven top-10 sponsor pages read in full say DAF gifts are outside the $1,000/$2,000 non-itemizer deduction. Vanguard's bunching example misstates the gain ($655; $2,450 at its own 35% rate), and MS GIFT states the floor carryover without its §170(d)(1)(C) condition (repo [`b41n16-b42n20-daf-tax-guidance.md`](mission-2026-11-14/b41n16-b42n20-daf-tax-guidance.md); [`validation-wave33b-report.md`](mission-2026-11-14/validation-wave33b-report.md)) [V wave 33B] Source: [validation-wave33b-report.md](mission-2026-11-14/validation-wave33b-report.md).

### 11.34 Data quality and donor data (validated, wave 34A)

**Data quality and donor data** (validated, wave 34A). A round-2 check of DAFRC's FY2024 panel found nothing left to replace. All 24 top-50 sponsors with imputed rows already carry R1 values equal to their filed FY2024 Form 990s in 95 of 96 cells; UCLA Foundation's grants, filed as −$120,260,861, keep the imputed $169.9m. The FY2024 market ($323.27bn) and corrected top 50 ($276.27bn) are unchanged. NPT's FY2023 Schedule D value ($22.84bn) is 81.8% of its Part X net assets ($27.92bn), against 101.3% and 100.6% in the adjacent years, and NPT's own consolidated statements report $28.51bn of net assets at 2023-06-30, so it is very likely a filer error. Using Part X would put FY2023 at $261.44bn and FY2023–24 growth at 23.6%, not 26.1%; the headline keeps the filed value. At the FY2024 top 20 ($250.63bn), full contact is the documented default for 33.2% of assets, led by Fidelity, and name or fund name only for 17.2%. For 44.6% the default is undocumented, and no sponsor defaults to anonymous. The survey finding that sponsors withhold donor contact data by default does not hold as a rule at the nationals, and neither does its opposite (repo [`validation-wave34a-report.md`](mission-2026-11-14/validation-wave34a-report.md)) [V wave 34A]


### 11.35 Recipient basis, ratings and tail fees (validated, wave 34B)

**Recipient basis, ratings and tail fees** (validated, wave 34B). The IRS assigns DAF grants to Form 990 line 1f. On a denominator of lines 1a + 1b + 1c + 1f (contributions less government grants and related-organisation transfers), top-50 DAF grants are a median 7.7% and a pooled 10.3% of sampled recipients' contributions, against 5.9% and 6.9% on line 1h; eight recipients' lines match their XML exactly. Chariot's 12.6% lies above the ≥$100m band (5.8–8.7% unscaled to scaled), the closer size match. Of $74.07bn of top-50 FY2023–24 DAF-weighted grants, 76.9% reach recipients that pass every Charity Navigator rule filings can test, or 76.5% if only full 990s count towards the three-return rule. CN publishes no revenue threshold. Church-status organisations without e-filed returns take 8.3% of dollars. EINs absent from the BMF take 5.6%; they are mostly governmental units and CZ Biohub LLCs, not revoked charities. Among 60 sampled sponsors under $50m, 7 (11.7%; Wilson 5.8–22.2%) publish a 2021-or-later admin rate and 16 (26.7%) some fee term. On six schedules, tail CFs charge a median 150 bps at $100k, against 100 bps at top-100 CFs (repo [`validation-wave34b-report.md`](mission-2026-11-14/validation-wave34b-report.md)) [V wave 34B]

### 11.36 Tail fee pool and grant purposes (validated, wave 35A)

**Tail fee pool and grant purposes** (validated, wave 35A). Seven 2021-or-later admin schedules published by sampled sponsors under $50m were applied to each tail sponsor's FY2024 DAF assets at its own average account. On them, the tail's admin-fee pool is about $138m a year (the median over the six community-foundation schedules) if all 1,240 sponsors charge, or about $90m if only the 641 community foundations charge. The range, $76m–$184m, rests on six CF schedules and one non-CF schedule. One CF charges no admin fee, and the bootstrap interval of the six-schedule median runs from about $65m–$72m to $155m–$162m depending on the seed. Charging non-CF sponsors CF prices is unevidenced. Across the six schedules, a median 66.7% of 603 usable tail CFs recover less than rule-A allocated DAF cost, and 24.9% less than the admin-only floor. Separately, top-50 Schedule I purpose text cannot measure restricted giving. Of 322,773 FY2024 lines from 48 sponsors, 98.2% carry boilerplate, sector labels, aggregates or blanks, and 1.2% name a specific use; Fidelity Charitable files one string on all 80,308 lines. Repo shares built on purpose text describe reporting practice, not donor restrictions (repo [`validation-wave35a-report.md`](mission-2026-11-14/validation-wave35a-report.md)) [V wave 35A]

### 11.37 Ren defaults and national 990 reads (validated, wave 35B)

" + "**Ren defaults and national 990 reads** (validated, wave 35B). Of 28 Ren-linked programmes, 7 default to full contact including email, and all 7 rest on one Ren-generic ‘Giving Platform Donor User Guide’ (2026-10-06, SHA-1 93d97b49e84a) whose text never names RCF. RCF's own 2023–24 guide said ‘The default is Fund Name Only’, as BofA's 2026 guide does, so on Ren the stated default tracks guide vintage. That does not show a configurable sponsor setting, and it does not prove a platform default. On FY2024 assets, Ren-administered sponsors split 49.2% fund name only, 21.0% full contact (an upper bound) and 29.8% with no stated default. Fidelity's audited advisor-managed investments were $37.14bn of $79.23bn (46.9%, June 2025), and its investment management fees equal line 11f to the dollar. Vanguard Charitable has no adviser-managed option, and DAFgiving360's share is unpublished. NPT's $742.8m of FY2023–24 foreign grants include no filed grant to a related organisation (Schedule R line 1b, not 1d). In FY2025, however, NPT Transatlantic granted £30.9m to NPT UK while line 1b stayed No (repo [`validation-wave35b-report.md`](mission-2026-11-14/validation-wave35b-report.md)) [V wave 35B]" + "

---

## Source register

Every external URL cited inline in this document, deduplicated, in order of first citation. Dates are publication or access dates as recorded in the repository's workstream source registers and validation registers.

- DAFRC Updated Analysis memo (Apr 2026; accessed 2026-11-14): https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf
- DAFRC Updated Analysis dataset (Spring 2026; accessed 2026-11-14): https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx
- DAFRC Annual DAF Report page (revised Spring 2026; accessed 2026-11-14): https://www.dafresearchcollaborative.org/research/annual-daf-report
- NPT 2024 DAF Report (2024 edition (FY2023 data)): https://www.nptrust.org/philanthropic-resources/philanthropist/resources/2024-daf-report-highlights/2024-daf-report-npt/
- DAFRC Annual DAF Report 2025 (Dec 2025): https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-DAF-Research-Collaborative.pdf
- Fidelity Charitable Form 990 FY2025 (FYE 2025-06-30): https://projects.propublica.org/nonprofits/organizations/110303001/202601389349301700/IRS990
- DAFgiving360 Form 990 FY2025 (FYE 2025-06-30): https://projects.propublica.org/nonprofits/organizations/311640316/202611199349300601/IRS990ScheduleF
- NPT Form 990 FY2025 (FYE 2025-06-30): https://projects.propublica.org/nonprofits/organizations/237825575/202601289349302480/IRS990ScheduleF
- Vanguard Charitable Form 990 FY2025 (FYE 2025-06-30): https://projects.propublica.org/nonprofits/organizations/232888152/202621329349306657/IRS990
- Fidelity Charitable FY2025 audited statements (FYE 2025-06-30): https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf
- DAFgiving360 FY2025 results (2025-07-29): https://www.dafgiving360.org/press-release/fiscal-year-2025-results
- Vanguard Charitable FY2025 financial statements (FYE 2025-06-30): https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf
- Foundant CommunitySuite page (accessed 2026-11-14): https://www.foundant.com/products/communitysuite/
- Tech Impact CF software landscape (Jul 2022): https://techimpact.org/sites/default/files/2024-03/TECH%20IMPACT%20Integrated%20Software%20for%20Community%20Foundations.pdf
- Great Hill investment in Ren (Pulse 2.0) (2025-10-28): https://pulse2.com/great-hill-partners-announces-strategic-growth-investment-in-donor-advised-fund-platform-ren/
- Foundation Source DAF OS brief (metrics as of 2025-12-31): https://foundationsource.com/resources/product-briefs/the-modern-operating-system-for-donor-advised-funds/
- SEI Charitable Fund release (2026-10-28): https://www.seic.com/about-sei/newsroom/sei-launches-sei-charitable-fund-bringing-charitable-giving-advisor-and-client-wealth-experience
- Give Interactive homepage (accessed 2026-11-14): https://www.giveinteractive.com/
- Edward Jones Charitable Gift Fund portal (live 2026-11-14): https://edwardjones.donorfirstx.com/
- Ameriprise RCF portal (live 2026-11-14): https://ampf.donorfirstx.com/
- RBC RCF portal (live 2026-11-14): https://rbcrcf.donorfirstx.com/
- Ren LPL RCF page (live 2026-11-14): https://www.reninc.com/lpl-rcf-daf/
- Ren UBS RCF page (live 2026-11-14): https://www.reninc.com/why-ubs-advisors-choose-rcf/
- SEI Giving Fund portal (live 2026-11-14): https://sei.donorfirstx.com/
- MDRT Global Gift Fund portal (live 2026-11-14): https://mdrt.donorfirstx.com/
- Vanguard Charitable FY2026 financial statements (FYE 2026-06-30; posted 2026-11): https://www.vanguardcharitable.org/sites/default/files/2026-11/VCEP_Financial_Statements_2026.pdf
- Give Interactive / Vanguard Charitable release (2025-11-04): https://www.giveinteractive.com/post/vanguard
- Commonwealth Charitable Fund portal (live 2026-11-14): https://cfndaf.donorfirstx.com/
- Northwestern Mutual RCF program circular (Nov 2024): https://www.reninc.com/wp-content/uploads/2025/08/NWM-Program-Circular-11-24.pdf
- UBS DAF fact sheet (Feb 2023): https://advisors.ubs.com/mediahandler/media/662455/Donor%20Advised%20Fund%20FactSheet.pdf
- Ren Fisher RCF page (live 2026-11-14): https://www.reninc.com/rcf-fisher-daf/
- MS GIFT donor portal (live 2026-11-14): https://msgift.donorfirstx.com/
- RCF FY2024 audited statements (FYE 2024-12-31; accessed 2026-11-14): https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf
- RCF FY2023 audited statements (FYE 2023-12-31; accessed 2026-11-14): https://renaissancecharitable.org/wp-content/uploads/2026/01/2023RCFAuditedFinancialStatements.pdf
- RCF FAQ (live 2026-11-14): https://renaissancecharitable.org/faqs/
- BofA Charitable Gift Fund portal (live 2026-11-14): https://bofa.donorfirst.org/
- AEF/Ren release, Apr 2026 (2026-04-08): https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/
- SEC full-text search, BofA filings (run 2026-11-14): https://efts.sec.gov/LATEST/search-index?q=%22Charitable%20Gift%20Fund%22&ciks=0000070858
- BofA CGF Form 990 TY2024 (e-filed 2025-11-17): https://projects.propublica.org/nonprofits/organizations/46010342/202503219349318170/full
- Cleveland Foundation iPhi portal (accessed 2026-11-14): https://www.iphiview.com/tcf/LogIn/tabid/444/Default.aspx
- ImpactAssets homepage (iPhi log-in) (accessed 2026-11-14): https://impactassets.org/
- Edward Jones DAF page (accessed 2026-11-14): https://www.edwardjones.com/us-en/investment-services/investment-products/donor-advised-funds
- Ren/RCF Edward Jones adviser guide (HTTP 404) (c. 2021-22; 404 on 2026-11-14): https://www.reninc.com/wp-content/uploads/2022/03/Advisor-Guide-and-FAQ-WH-RCF-2022-1.pdf
- Edward Jones elevated wealth management release (2025): https://www.edwardjones.com/us-en/why-edward-jones/news-media/press-releases/elevated-wealth-management
- GTCR acquires Foundation Source (2023-09-13): https://foundationsource.com/newsroom/press-releases/gtcr-announces-acquisition-of-foundation-source/
- Foundation Source acquires Vennfi (2024-10-17): https://foundationsource.com/newsroom/press-releases/foundation-source-acquires-vennfi-the-fintech-powering-donor-advised-fund-charityvest/
- Foundation Source acquires Giving Place (2025-04-30): https://foundationsource.com/newsroom/press-releases/foundation-source-acquires-giving-place-platform-for-private-foundations-and-family-offices/
- Charityvest + Vennfi guide (updated 2025): https://guide.charityvest.org/about-our-venture/charityvest-%2B-vennfi
- TIAA Wealth Management DAF release (2026-09-28): https://www.prnewswire.com/news-releases/tiaa-wealth-management-makes-charitable-giving-part-of-the-financial-plan-with-new-donor-advised-fund-program-302891438.html
- Temple University DAF release (2025-11-25): https://foundationsource.com/newsroom/press-releases/temple-university-launches-custom-donor-advised-fund-program-in-partnership-with-foundation-source-and-charityvest/
- OneAscent Form ADV Part 2A (2026-08-11): https://files.adviserinfo.sec.gov/IAPD/Content/Common/crd_iapd_Brochure.aspx?BRCHR_VRSN_ID=1054956
- Charityvest Form 990 TY2024 (e-filed 2025-11-14): https://projects.propublica.org/nonprofits/organizations/812771871/202513189349315961/full
- Chariot partner profile: TIFIN Give (2026-02-05): https://www.givechariot.com/resources/insights/getting-to-know-tifin-give-a-chariot-disbursements-partner-
- TIFIN and Chariot partnership (2025-12-02): https://tifin.com/news/tifin-and-chariot-partner-to-transform-grant-payments/19418/
- Fidelity Charitable nonprofit FAQ (live 2026-11-14): https://www.fidelitycharitable.org/nonprofits/faqs.html
- PayPal Grant Payments launch (2022-08-25): https://newsroom.paypal-corp.com/2022-08-25-PayPal-Launches-Grant-Payments,-Enabling-Charities-to-Quickly-Receive-Funds-from-Grantmakers
- Vanguard Charitable PayPal electronic granting release (2023-05-03): https://prnewswire.com/news-releases/vanguard-charitable-launches-electronic-granting-solution-surpassing-100-million-in-electronic-grants-to-more-than-400-charities-in-first-4-months-301932762.html
- Ren Rapid Disbursement Engine release (2023-11-28): https://prnewswire.com/news-releases/ren-debuts-rapid-disbursement-engine-expanding-philanthropic-services-to-meet-rapid-daf-growth-301999647.html
- Chariot partner profile: Daffy (Jul 2026): https://www.givechariot.com/resources/insights/getting-to-know-daffy-a-chariot-disbursements-partner
- Founders Pledge selects Chariot (undated): https://www.givechariot.com/post/founders-pledge-selects-chariot-to-power-grant-payments
- Chariot llms.txt (2026): https://www.givechariot.com/llms.txt
- Chariot partner profile: Charityvest (2026-07-29): https://www.givechariot.com/resources/insights/getting-to-know-charityvest-a-new-chariot-disbursements-partner
- Chariot on Fidelity's 2026 Giving Report (2026-03-24): https://www.givechariot.com/resources/insights/top-8-takeaways-from-fidelity-charitables-2026-giving-report
- IRS EO BMF extract (accessed 2026-11-14): https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf
- IRS TEOS bulk data downloads (accessed 2026-11-14): https://www.irs.gov/charities-non-profits/tax-exempt-organization-search-bulk-data-downloads
- IRS Auto-Revocation List (accessed 2026-11-14): https://www.irs.gov/autorevocationlist
- Chariot compliance help page (accessed 2026-11-12): https://help.givechariot.com/onboarding/trust-and-safety/compliance
- Candid Charity Check FAQ (accessed 2026-11-14): https://developer.candid.org/docs/faqs-charity-check
- RCF grantmaking due-diligence policy (rev. Mar 2023): https://renaissancecharitable.org/wp-content/uploads/2026/02/Grantmaking-Due-Diligence-Policy.pdf
- Fidelity Charitable fees (accessed 2026-11-14): https://www.fidelitycharitable.org/giving-account/what-it-costs.html
- DAFgiving360 Program Policies, "Updated December 2024" (first-party PDF hosted on a third-party site; fee table p. 9; accessed 2026-11-19): https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf
- Charityvest fee guide (accessed 2026-11-14): https://guide.charityvest.org/for-donors/fees-and-expenses
- RCF advisor-managed DAF fees (accessed 2026-11-11): https://renaissancecharitable.org/advisor-managed-dafs/
- BofA CGF fee schedule (accessed 2026-11-14): https://www.bankofamerica.com/content/documents/philanthropic/cgf_fee_schedule.pdf
- Daffy membership fees (2026-08-06): https://help.daffy.org/en/articles/6323771-what-are-daffy-s-membership-fees
- 26 U.S.C. §4966 (current code; accessed 2026-11-14): https://www.law.cornell.edu/uscode/text/26/4966
- IRS donor-advised funds page (accessed 2026-11-14): https://www.irs.gov/charities-non-profits/charitable-organizations/donor-advised-funds
- 26 U.S.C. §4967 (current code; accessed 2026-11-14): https://www.law.cornell.edu/uscode/text/26/4967
- Rev. Proc. 2018-32 summary (The Tax Adviser) (Aug 2018): https://www.thetaxadviser.com/issues/2018/aug/irs-updates-charitable-contribution-procedures/
- California AG release (2026-05-22): https://oag.ca.gov/node/623769
- AEF DonorCentral sunset notice (2026-10-31): https://engage.aefonline.org/dc-sunset/
- Daffy $2B release (2026-09-30): https://www.daffy.org/resources/two-billion-assets-under-management
- Daffy Charitable Fund Form 990 TY2024 (e-filed 2025-11-16): https://projects.propublica.org/nonprofits/organizations/863177440/202513209349301201/full
- Charityvest 2025 annual report (2026-02-11): https://www.charityvest.org/annual-report-2025
- Vennfi seed release ('zero fees') (2020-11-19): https://www.newswire.com/news/this-startup-raised-3-7m-to-let-anyone-donate-stocks-and-etfs-with-a-21260863
- Physician on FIRE on Charityvest fees (2022-03-08): https://www.physicianonfire.com/better-donor-advised-fund/
- Daffy membership tier changes (2026-08-28): https://help.daffy.org/en/articles/11730892-how-do-i-change-my-membership
- ThinkAdvisor on Fidelity minimums (2020-09-30): https://www.thinkadvisor.com/2020/09/30/fidelity-charitable-ends-daf-account-minimums/
- Schwab Charitable minimums release (2020-11-10): https://www.dafgiving360.org/press-releases/schwab-charitable-expands-access-and-options
- Ren homepage (live 2026-11-14): https://www.reninc.com/
- 26 U.S.C. §4958 (current code; accessed 2026-11-14): https://www.law.cornell.edu/uscode/text/26/4958
- NPT FY2025 annual report (FY ended 2025-06-30): https://www.nptrust.org/annual-reports/npt-annual-report/
- NonProfit Times on NPT FY2025 (2025-12-01): https://thenonprofittimes.com/?p=215695
- Fidelity Charitable recommending a grant (accessed 2026-11-14): https://www.fidelitycharitable.org/giving-account-guide/recommending-a-grant.html
- GTCF DAF transfer instructions (2026-05-18): https://www.gtcf.org/wp-content/uploads/2026.05.18-GTCF_DAF_Transfer_Instructions.pdf
- Daffy help: closing an account (2026-04-02): http://help.daffy.org/en/articles/6520234-how-do-i-close-my-daffy-account
- Inequality.org on DAF-to-DAF giving (2026-06-22): https://inequality.org/article/daf-to-daf-giving-2024/
- Daffy MCP docs (accessed 2026-11-14): https://docs.daffy.org/agents/mcp
- Chariot Disbursements FAQ (accessed 2026-11-14): https://docs.givechariot.com/guides/disbursements/faq
- TIFIN Give Louise release (2025-10-27): https://www.prnewswire.com/news-releases/tifin-give-launches-louise-ai-capabilities-for-philanthropy-302595069.html
- Ren faith/community foundation page (accessed 2026-11-14): https://www.reninc.com/faith-based-community-foundations/
- Foundation Source press releases (CEO, PG Calc) (2023-09 to 2024-02): https://foundationsource.com/category/newsroom/press-releases/page/5/
- Foundation Source acquires PG Calc (2024-02-13): https://foundationsource.com/newsroom/press-releases/foundation-source-announces-acquisition-of-pg-calc-leading-provider-of-planned-giving-solutions/
- Pacific Foundation Services deal record (2025-06-25 (secondary)): https://www.privsource.com/acquisitions/deal/n8S0zL
- AEF/Ren release, Jul 2025 (2025-07-23): https://www.aefonline.org/thought-leadership/american-endowment-foundation-selects-ren-as-a-strategic-partner-to-expand-philanthropy-drive-innovation-and-foster-growth-in-financial-services/
- Federal Register 2023-24982 (proposed §4966 regs) (2023-11-14): https://www.federalregister.gov/documents/2023/11/14/2023-24982/taxes-on-taxable-distributions-from-donor-advised-funds-under-section-4966
- Federal Register API query (queried 2026-11-14): https://www.federalregister.gov/api/v1/documents.json?conditions%5Bterm%5D=%22donor%20advised%20fund%22&conditions%5Bagencies%5D%5B%5D=internal-revenue-service&order=newest
- Federal Register 2024-00260 (2024-01-09): https://www.federalregister.gov/documents/2024/01/09/2024-00260/taxes-on-taxable-distributions-from-donor-advised-funds-under-section-4966
- IRS 2026-2027 Priority Guidance Plan (2026-09-29): https://www.irs.gov/pub/irs-counsel/2026-2027-initial-pgp.pdf
- ArentFox Schiff on 2026-27 PGP (2026-10-07): https://www.afslaw.com/perspectives/alerts/irs-and-treasury-release-2026-2027-priority-guidance-plan-what-tax-exempt
- Baker McKenzie on proposed DAF regs (2024-05-17 (search)): https://www.globalcompliancenews.com/2024/06/01/https-insightplus-bakermckenzie-com-bm-tax-united-states-donor-fund-proposed-regulations_05172024/
- IRS nonitemizer deduction reminder (2026-11-10): https://www.irs.gov/newsroom/irs-reminder-permanent-charitable-contribution-deduction-begins-for-returns-filed-next-year-for-taxpayers-who-do-not-itemize
- Vanguard Charitable on OBBBA (2025-07-09, updated Oct 2026): https://www.vanguardcharitable.org/news/could-2025-budget-reconciliation-bill-impact-your-giving
- IRS Publication 505 (2026) (2026): https://www.irs.gov/publications/p505
- Steptoe on the ACE Act (2021): https://www.steptoe.com/en/news-publications/senators-king-and-grassley-introduce-daf-and-private-foundation-reform-legislation.html
- Rep. Smith QCD-to-DAF bill release (2025-04-10): https://adriansmith.house.gov/media/press-releases/smith-panetta-introduce-bipartisan-bill-support-charitable-giving
- Sen. Young QCD-to-DAF bill release (2026-03-04): https://www.young.senate.gov/?p=13549
- LegiScan CA AB 1712 (status 2020-02-03): https://legiscan.com/CA/bill/AB1712/2019
- Reed Smith on SEC 2026 focus (2026 (search)): https://www.reedsmith.com/articles/private-equity-behind-the-scenes/sec-sets-the-tone-for-2026-regulatory-focus-on-investment-managers/
- Alston & Bird on SEC withdrawals (Jun 2025): https://www.alston.com/en/insights/publications/2025/06/sec-withdraws-multiple-rule-proposals
- Bonterra Que release (2025-10-01): https://www.businesswire.com/news/home/20251001579571/en/Bonterra-Launches-Que-The-First-Agentic-AI-Platform-for-Funders-Nonprofits-and-Supporters
- FF News on Daffy AI (2025-04-09): https://ffnews.com/newsarticle/paytech/daffy-is-using-ai-to-reshape-the-future-of-charitable-giving/
- Anthropic API pricing (read 2026-11-14): https://platform.claude.com/docs/en/about-claude/pricing
- BLS compliance officers (May 2025) (accessed 2026-11-14): https://www.bls.gov/ooh/business-and-financial/compliance-officers.htm
- BLS ECEC June 2026 (released 2026-09-09): https://www.bls.gov/news.release/ecec.nr0.htm
- Endaoment institutions page (read 2026-11-14): https://endaoment.org/institutions
- Daffy for Developers (May 2023): https://www.daffy.org/resources/daffy-for-developers
- Charityvest 2025 results release (2026-02-11): https://foundationsource.com/newsroom/press-releases/charityvest-reports-record-2025-charitable-giving-more-than-doubling-contributions-and-grants/
- Fidelity Charitable 2026 Giving Report (2026 (CY2025 data)): https://www.fidelitycharitable.org/insights/2026-giving-report.html
- Fidelity Charitable 2026 Giving Report PDF (2026 (CY2025 data); first-party source per validation W4-14): https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf

## Validation corrections (wave 4, 2026-11-14) — governing
Source: [validation-wave4-report.md](mission-2026-11-14/validation-wave4-report.md). Where these conflict with the text above, these govern. **Applied in §2.5 during the 2026-11-15 consolidation** (see [consolidation changelog](mission-2026-11-14/consolidation-changelog.md)).

- **W4-14** (research/DAF-INDUSTRY-REPORT-2026-11.md line 96): replace "About 67% of Fidelity grants already go by EFT ([Chariot …])" → cite first-party: "Fidelity's 2026 Giving Report: 'Today, 67% of our grants are distributed via EFT' ([PDF](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf))"

## Validation corrections (wave 18, 2026-11-15) — governing
Source: [validation-wave18-report.md](mission-2026-11-14/validation-wave18-report.md).

1. **GS PF re-score note (after the v1.2 changes table).**
   - **Find:** "On Goldman Sachs PF, wave 6 found that its 2012 and 2017 circulars are also public. All of them state check payment, so a further re-score could place it."
   - **Replace with:** "On Goldman Sachs PF, wave 6 found that its 2012 and 2017 circulars are also public, and all of them state check payment. A 2021+ circular (ETF ratios as of 2024-09-30, reproduced in FireAid's Sept 2025 report) states check **or wire**, so a further re-score could place it (V15-09, V18-01)."
2. **Bank-programs table, BofA row.**
   - **Find:** "| BofA CGF | Check-only grants. Contributions (not grants) can be exported to Excel."
   - **Replace with:** "| BofA CGF | Check-only grants. Contributions can be exported to Excel (guide text), and the Grant Listing screenshot also shows an \"Export to Excel\" button (scope not stated; V18-19)."
3. **Bank-programs table, Goldman row.**
   - **Find:** "| Goldman Sachs PF | Circulars from 2008, 2012 and 2017 all state check payment. The live donor web runs on Ren iPhi. |"
   - **Replace with:** "| Goldman Sachs PF | Goldman-hosted circulars from 2008, 2012 and 2017 state check payment. The newest known circular (ratios as of 2024-09-30, FireAid App. B) states check or wire. The live donor web runs on Ren iPhi. |"
4. **New subsection after §11.12:** "### 11.13 Batch 33 (validated, wave 18)", containing:

## Validation corrections (wave 19, 2026-11-15) — governing
Source: [validation-wave19-report.md](mission-2026-11-14/validation-wave19-report.md).

1. **New subsection after §11.13:** "### 11.14 Batch 34 (validated, wave 19)", containing:

## Validation corrections (wave 20, 2026-11-15) — governing
Source: [validation-wave20-report.md](mission-2026-11-14/validation-wave20-report.md).

1. **New subsection after §11.14:** "### 11.15 Batch 35 (validated, wave 20)", containing:

   

2. **Housekeeping (§11.14).** The batch-34 paragraph ends with its "Sources:" list twice. Delete the second copy, which starts at the second occurrence of " Sources: [queue-batch34-netting-filings.md]" and runs to the end of that paragraph.

## Validation corrections (wave 21, 2026-11-15) — governing
Source: [validation-wave21-report.md](mission-2026-11-14/validation-wave21-report.md).

1. **New subsection after §11.15:** "### 11.16 Batch 36 (validated, wave 21)", containing:

## Validation corrections (wave 22, 2026-11-15) — governing
Source: [validation-wave22-report.md](mission-2026-11-14/validation-wave22-report.md).

1. **Line 146, Vendor economics** (batch 37A §7 proposal 3, validated). Applied by gap19-11 C-R05, with a repo citation in place of the marker. [gap19-11]
   - **Find:** "Ren's corporate revenue, margins and customer concentration are not public ((source: repo inference — no primary URL))."
   - **Replace with:** "Ren's corporate revenue, margins and customer concentration are not public ((source: repo inference — no primary URL)). Named Ren receipts in sponsor 990s total $44.98m in TY2024 (18 sponsors). RCF is 42.7% of that and the two Morgan Stanley programs 43.0% (batch 37A §1.2; V wave 22). This is a floor on receipts, not Ren revenue."
2. **New subsection after §11.16:** "### 11.17 Batch 37 (validated, wave 22)", containing:

## Validation corrections (wave 23, 2026-11-15) — governing
Source: [validation-wave23-report.md](mission-2026-11-14/validation-wave23-report.md).

1. **§11.12 (Batch 32, wave 17), Philanthropi sentence.**
   - **Find:** "Philanthropi's site is dark, while its infrastructure certificates still renew."
   - **Replace with:** "Philanthropi's site is dark. That its infrastructure certificates still renew rests only on crt.sh data and is an unverified lead under the [crt.sh compliance note](mission-2026-11-14/compliance-note-crtsh-robots.md) [V wave 23]."
2. **Vendor stacks, Give Interactive bullet.**
   - **Find:** "before Give's CCT production host (Jun 2025)."
   - **Replace with:** "before Give's CCT host, which resolves in public DNS. Its June 2025 first certificate and \"production\" label come from CT logs only (unverified lead, [V wave 23])."
3. **New subsection after §11.17:** "### 11.18 Batch 38 (validated, wave 23)", containing:

## Validation corrections (wave 24B, 2026-11-15) — governing
Source: [validation-wave24b-report.md](mission-2026-11-14/validation-wave24b-report.md).

1. **§1, payout (F1, F4).** The first sentence and the DAFRC bullet are applied by gap19-11 C-R01, with a primary citation in place of the marker. The remaining bullets of this item still govern. [gap19-11]
   - **Find:** "Fund-level payout is not public ((source: repo inference — no primary URL))."
   - **Replace with:** "Fund-level payout is not public in filings ((source: repo inference — no primary URL)). Voluntary account-level samples exist:\n- DAFRC's 2024 National Study (111 programs, over 50,000 accounts) puts the median three-year account payout at 9% (15% excluding inactive accounts) and the mean at 18%. 22% of accounts made no grants in 2020–22 ([executive summary](https://johnsoncenter.org/wp-content/uploads/2024/02/DAFRC_Executive_Summary_Key_Findings.pdf); doi:10.4087/ymfd7624).\n- This does not contradict the 23.9% aggregate, because a few large, fast-paying accounts carry the aggregate. Published payout figures also differ by definition: IPS's 9.7% is a median of sponsors' rates on grants ÷ (year-end assets + grants), while NPT's 23.9% is an aggregate on beginning assets ([IPS 2025](https://www.ips-dc.org/wp-content/uploads/2025/04/Independent-Report-on-DAFs-FINAL-04-03-2025.pdf)) [V wave 24B]."
2. **§1, transfers bullet (F3).**
   - **Find:** "They inflate apparent payout and double-count in market sums."
   - **Replace with:** "They inflate apparent payout and double-count in market sums. California's 2022 AG audit reports 18% of community-foundation DAF grants going to other DAFs. That figure covers 2016–20 and 57 California-registered sponsors, and its definition is unclear. In the repo's top-50 filings, community foundations other than SVCF send about 5% of Schedule I dollars to other DAF sponsors ([CA AG 2022](https://oag.ca.gov/system/files/media/donor-advised-funds-overview.pdf); [`daf-grant-recipient-sectors-top50.csv`](../data/mission-2026-11-14/daf-grant-recipient-sectors-top50.csv)) [V wave 24B]."
3. **§3 incentive table, fee-alignment row (F2).**
   - **Find:** "incentive documented, effect on payout unsupported **[RT]**"
   - **Replace with:** "incentive documented. No evidence links fee structure to payout; one correlational study finds that national sponsors whose websites stress donor benefits have lower payout ([Flannery & Mittendorf 2025, NVSQ](https://doi.org/10.1177/08997640251331853)) **[RT; V wave 24B]**"
4. **New subsection after §11.18.** Add "### 11.19 New directions N5–N8 (validated, wave 24B)", containing the paragraph below. If wave 24A has already added an §11.19, renumber this one as the next free number.

## Validation corrections (wave 24A, 2026-11-15) — governing
Source: [validation-wave24a-report.md](mission-2026-11-14/validation-wave24a-report.md).

1. **New subsection after §11.18:** "### 11.19 New directions N1–N4 (validated, wave 24A)". Renumber if another wave-24 subsection lands first. It contains:

## Validation corrections (wave 25B, 2026-11-15) — governing
Source: [validation-wave25b-report.md](mission-2026-11-14/validation-wave25b-report.md).

1. **New subsection after the last §11 subsection.** Add "### 11.21 New directions N12–N14 (validated, wave 25B)", containing the paragraph below. If §11.21 is already taken (for example by wave 25A), use the next free number.

## Validation corrections (wave 25A, 2026-11-15) — governing
Source: [validation-wave25a-report.md](mission-2026-11-14/validation-wave25a-report.md).

1. **New subsection after §11.21:** "### 11.22 New directions N9–N11 (validated, wave 25A)". Renumber if another subsection lands first. It contains:

   

`research/mission-2026-11-14/direction-sponsor-accessibility-service.md` needs no change.

## Validation corrections (wave 26, 2026-11-15) — governing
Source: [validation-wave26-report.md](mission-2026-11-14/validation-wave26-report.md).

1. **New subsection after the last §11 subsection.** Add "### 11.23 New directions N15–N18 (validated, wave 26)", containing the paragraph below. If §11.23 is already taken, use the next free number.

## Validation corrections (wave 27, 2026-11-15) — governing
Source: [validation-wave27-report.md](mission-2026-11-14/validation-wave27-report.md).

1. **New subsection after §11.23.** Add "### 11.24 New directions N19–N22 (validated, wave 27)", containing the paragraph below. If §11.24 is already taken, use the next free number.

## Validation corrections (wave 28, 2026-11-15) — governing
Source: [validation-wave28-report.md](mission-2026-11-14/validation-wave28-report.md).

1. **New subsection after §11.24.** Add "### 11.25 New directions N23–N26 (validated, wave 28)", containing the paragraph below. If §11.25 is already taken, use the next free number.

## Validation corrections (wave 29, 2026-11-15) — governing
Source: [validation-wave29-report.md](mission-2026-11-14/validation-wave29-report.md).

1. **New subsection after §11.25.** Add "### 11.26 New directions N27–N30 (validated, wave 29)", containing the paragraph below. If §11.26 is already taken, use the next free number.

## Validation corrections (wave 30, 2026-11-15) — governing
Source: [validation-wave30-report.md](mission-2026-11-14/validation-wave30-report.md).

1. **§11.20, sector-share sentence (N1–N4 paragraph).**
   - **Find:** "and 13.6% to religion, with the top 100 recipients taking 24.3%."
   - **Replace with:** "and 13.6% to religion, with the top 100 recipients taking 24.3%. Schedule I shows international recipients (NTEE Q) at 5.6%, but direct foreign grants (Part IX line 3 / Schedule F, $1.89bn) sit outside Schedule I. Including them, international is 7.8% of Schedule I plus foreign grants [V wave 30]."
2. **New subsection after §11.26.** Add "### 11.27 New directions N31–N33 (validated, wave 30)", containing the paragraph below. If §11.27 is already taken, use the next free number.

## Validation corrections (wave 31A, 2026-11-19) — governing
These corrections from [validation-wave31a-report.md](mission-2026-11-14/validation-wave31a-report.md) could not be applied inline and govern the text above:

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
5. **New subsection after §11.27.** Add "### 11.28 Thoroughness pass part A (validated, wave 31A)", containing the paragraph below. If §11.28 is already taken, use the next free number. **Applied as §11.29**; the quoted copy below is retained for history and is not a second finding. [gap19-11]

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
