# The U.S. Donor-Advised Fund Industry, November 2026: Structure, Economics, Technology and AI

**Consolidated report.** Version 2026-11-15. Repository `kemiller2002/daf-landscape`.

**Consolidation (2026-11-15):** §11 was reorganised from a chronological list of batch summaries into themes, and figures in §1–§10 that later validation superseded were updated. Every change, with its governing source, is in the [consolidation changelog](mission-2026-11-14/consolidation-changelog.md). The pre-consolidation text is archived in [`archive/`](mission-2026-11-14/archive/DAF-INDUSTRY-REPORT-2026-11.pre-consolidation.md).

This report sits on top of the repository's 96 research documents and 89 datasets (repo [`repo-inventory-final.json`](../data/mission-2026-11-14/repo-inventory-final.json)). It does not repeat them. Each section states the current best understanding, its evidence state, and where the evidence lives.

**Labels used throughout:**
- **Claim states** follow the EDF claim-and-confidence policy: *internal-demonstration, suggestive, unsupported, contradicted*. Confidence runs Low → High.
- **[V]** = independently validated (registers in `data/mission-2026-11-14/validation-register*.csv`).
- **[RT]** = corrected by red-team review.
- **[S]** = scenario number, not an estimate.

**Decision-oriented companion:** [strategic synthesis A–G](mission-2026-11-14/strategic-synthesis.md).
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

**Vendor footprint from Form 990 (all 1,512 FY2024 sponsors).** In Part VII-B, Ren/Stellar is named as a paid contractor by 30 sponsors holding $48.55bn (14.8% of DAFRC assets) in any FY2022–25 return, or 18 sponsors holding $30.18bn (9.2%) in their latest return [V wave 5]. GS DAPF ($11.84bn) appears in FY2022 only, and on corrected FY2024 assets the cumulative share is 15.0% ([vendor footprint](mission-2026-11-14/full-universe-990-harvest-and-corrected-totals.md), wave-5 governing note). Other DAF vendors appear at one to six sponsors each. 985 sponsors list no contractor above $100k. These counts are floors: Part VII-B lists only the top five contractors above $100k.

**Payout.**
- **Aggregate:** grants over beginning assets were 23.7–28.4% in FY2020–24 ([DAFRC Updated Analysis memo](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf); [DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`derived-metrics.csv`](../data/mission-2026-11-14/derived-metrics.csv)).
- **Typical sponsor:** the median sponsor with ≥$1m in assets pays out about 11–12.5%, and 19–24% of those sponsors pay out under 5% ([DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`derived-metrics.csv`](../data/mission-2026-11-14/derived-metrics.csv); repo [`scripts/mission_daf_metrics.py`](../scripts/mission_daf_metrics.py)).
- **By segment:** national sponsors' median is about 20%, community foundations about 11%, and university or hospital sponsors about 5.4% **[RT]** ([DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`validation-register-wave2b.csv`](../data/mission-2026-11-14/validation-register-wave2b.csv)).
- **Transfers between DAF sponsors** are 10–18% of the nationals' listed grant dollars. They inflate apparent payout and double-count in market sums. Pooled FY2021–24 payout net of these transfers is 19.0–21.5% against 23.9% gross (§11.1) ([Fidelity Charitable Form 990 FY2025](https://projects.propublica.org/nonprofits/organizations/110303001/202601389349301700/IRS990); [DAFgiving360 Form 990 FY2025](https://projects.propublica.org/nonprofits/organizations/311640316/202611199349300601/IRS990ScheduleF); [NPT Form 990 FY2025](https://projects.propublica.org/nonprofits/organizations/237825575/202601289349302480/IRS990ScheduleF); [Vanguard Charitable Form 990 FY2025](https://projects.propublica.org/nonprofits/organizations/232888152/202621329349306657/IRS990); repo [`breadth-community-faith-infrastructure-emerging.md`](../research/mission-2026-11-14/breadth-community-faith-infrastructure-emerging.md)).

Fund-level payout is not public ((source: repo inference — no primary URL)).

**Concentration differs by layer.** Do not conflate these markets:

| Layer | Measure | Finding | State |
|---|---|---|---|
| Sponsor assets | DAFRC FY2024 | CR3 45.5%, CR5 55.8%, HHI ≈ 830 (unconcentrated). National sponsors only: CR3 63.2%, HHI ≈ 1,566 ([DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`dafrc-sponsor-schedule-d-fy2019-2024.csv`](../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv); repo [`validation-register-wave2b.csv`](../data/mission-2026-11-14/validation-register-wave2b.csv)) | [V][RT] High |
| Administration | Period-aligned | About 39% of assets at three affiliate-linked nationals (Fidelity/FMR; Schwab; Vanguard as a hybrid) ([Fidelity Charitable FY2025 audited statements](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf); [DAFgiving360 FY2025 results](https://www.dafgiving360.org/press-release/fiscal-year-2025-results); [Vanguard Charitable FY2025 financial statements](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf); [DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)). Fully outsourced platform administration: ≥6 sponsors holding 9.1% ([DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`regulation-market-structure-portability.md`](../research/mission-2026-11-14/regulation-market-structure-portability.md)) | Medium |
| Software | Vendor self-reports | Licensed DAF software at 31–94% of sponsors ([Foundant CommunitySuite page](https://www.foundant.com/products/communitysuite/); [Tech Impact CF software landscape](https://techimpact.org/sites/default/files/2024-03/TECH%20IMPACT%20Integrated%20Software%20for%20Community%20Foundations.pdf); [DAFRC Annual DAF Report page](https://www.dafresearchcollaborative.org/research/annual-daf-report)). Community foundations: Foundant CommunitySuite claims 700+ ([Foundant CommunitySuite page](https://www.foundant.com/products/communitysuite/)); the repository's EIN-level map finds it at 361 of 803 foundations (45%) and 32.7% of mapped community-foundation DAF assets [V wave 9] ([CF vendor map](mission-2026-11-14/queue-cf-vendor-map.md)). National and white-label market: Ren (incl. iPhi), Foundation Source, TIFIN Give, Give Interactive ([Great Hill investment in Ren (Pulse 2.0)](https://pulse2.com/great-hill-partners-announces-strategic-growth-investment-in-donor-advised-fund-platform-ren/); [Foundation Source DAF OS brief](https://foundationsource.com/resources/product-briefs/the-modern-operating-system-for-donor-advised-funds/); [SEI Charitable Fund release](https://www.seic.com/about-sei/newsroom/sei-launches-sei-charitable-fund-bringing-charitable-giving-advisor-and-client-wealth-experience); [Give Interactive homepage](https://www.giveinteractive.com/)) | Low-Medium; HHI not computable |
| Custody | Audited notes | about 20.2% of period-aligned FY2024 assets with one custodian family (Fidelity Brokerage Services, Fidelity Charitable's custodian); lower bound ([Fidelity Charitable FY2025 audited statements](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf); [DAFRC Updated Analysis memo](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf)) <!-- CITE-CHECK RESOLVED 2026-11-14 (text corrected): 26.2% appears to be Fidelity's June-2025 net assets ($85.86bn, FID audit) over the DAFRC FY2024 total ($327.87bn) - the same period mismatch the red team corrected in V2B-01/V2B-03. Period-aligned Fidelity share is about 20.2%. Not changed. --> | lower bound only |
| Distribution | Channel graph | About 11 wealth-firm programs on RCF + Ren ([Edward Jones Charitable Gift Fund portal](https://edwardjones.donorfirstx.com/); [Ameriprise RCF portal](https://ampf.donorfirstx.com/); [RBC RCF portal](https://rbcrcf.donorfirstx.com/); [Ren LPL RCF page](https://www.reninc.com/lpl-rcf-daf/); [Ren UBS RCF page](https://www.reninc.com/why-ubs-advisors-choose-rcf/); [SEI Giving Fund portal](https://sei.donorfirstx.com/); [MDRT Global Gift Fund portal](https://mdrt.donorfirstx.com/); repo [`relationship-graph-edges.csv`](../data/mission-2026-11-14/relationship-graph-edges.csv)); SEI multi-sources (RCF/Ren and GiveClear/TIFIN) ([SEI Giving Fund portal](https://sei.donorfirstx.com/); [SEI Charitable Fund release](https://www.seic.com/about-sei/newsroom/sei-launches-sei-charitable-fund-bringing-charitable-giving-advisor-and-client-wealth-experience)) | Medium-High on edges |

Sources: [vendor dependency and concentration](mission-2026-11-14/vendor-dependency-concentration.md); [red team 2B](mission-2026-11-14/red-team-wave2b-graph-data-incentives.md).

---

## 2. Who does what: legal sponsor, administrator, technology, rails, distribution

The industry is a stack whose layers are often owned by different parties. The relationship graph has 131 nodes and 167 edges, every edge sourced and status-labelled (repo [`relationship-graph-nodes.csv`](../data/mission-2026-11-14/relationship-graph-nodes.csv); repo [`relationship-graph-edges.csv`](../data/mission-2026-11-14/relationship-graph-edges.csv)): 134 confirmed (one more after red-team), 17 historically confirmed, 11 inferred, 5 unknown. A red-team sample of 15 "confirmed" edges found 0 status errors and 2 scope imprecisions (repo [`validation-register-wave2b.csv`](../data/mission-2026-11-14/validation-register-wave2b.csv); repo [`red-team-wave2b-graph-data-incentives.md`](../research/mission-2026-11-14/red-team-wave2b-graph-data-incentives.md)).

### 2.1 Affiliate-integrated nationals
Fidelity Charitable, DAFgiving360 and Vanguard Charitable combine sponsor brand, affiliated investment funds and affiliated administration ([Fidelity Charitable FY2025 audited statements](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf); [DAFgiving360 FY2025 results](https://www.dafgiving360.org/press-release/fiscal-year-2025-results); [Vanguard Charitable FY2025 financial statements](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf)):
- Fidelity Charitable pays FMR affiliates amounts equal to donors' administrative fees **[V]** ([Fidelity Charitable FY2025 audited statements](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf)).
- Vanguard Charitable has 35 of 37 pools in Vanguard funds and pays a related-party service fee of $4.24m in FY2026 **[V]** ([Vanguard Charitable FY2026 financial statements](https://www.vanguardcharitable.org/sites/default/files/2026-11/VCEP_Financial_Statements_2026.pdf)).
- **New:** Vanguard Charitable selected **Give Interactive** for DAF recordkeeping (Nov 2025 release) ([Give Interactive / Vanguard Charitable release](https://www.giveinteractive.com/post/vanguard)).

### 2.2 The RCF–Ren spine
Renaissance Charitable Foundation sponsors branded programs for Edward Jones, Ameriprise, RBC, LPL/Commonwealth (Commonwealth sponsorship by RCF inferred), Northwestern Mutual, UBS (one of four sponsors there), SEI, Fisher and MDRT ([Edward Jones Charitable Gift Fund portal](https://edwardjones.donorfirstx.com/); [Ameriprise RCF portal](https://ampf.donorfirstx.com/); [RBC RCF portal](https://rbcrcf.donorfirstx.com/); [Ren LPL RCF page](https://www.reninc.com/lpl-rcf-daf/); [Commonwealth Charitable Fund portal](https://cfndaf.donorfirstx.com/); [Northwestern Mutual RCF program circular](https://www.reninc.com/wp-content/uploads/2025/08/NWM-Program-Circular-11-24.pdf); [Ren UBS RCF page](https://www.reninc.com/why-ubs-advisors-choose-rcf/); [UBS DAF fact sheet](https://advisors.ubs.com/mediahandler/media/662455/Donor%20Advised%20Fund%20FactSheet.pdf); [SEI Giving Fund portal](https://sei.donorfirstx.com/); [Ren Fisher RCF page](https://www.reninc.com/rcf-fisher-daf/); [MDRT Global Gift Fund portal](https://mdrt.donorfirstx.com/); repo [`relationship-graph-edges.csv`](../data/mission-2026-11-14/relationship-graph-edges.csv)) <!-- CITE-CHECK RESOLVED 2026-11-14 (text corrected): RCF as sponsor of the Commonwealth Charitable Fund is only 'inferred' in relationship-graph-edges.csv (E034); LPL's own RCF channel is confirmed (E030). -->. Ren supplies the "DFX powered by Ren" portals ([Edward Jones Charitable Gift Fund portal](https://edwardjones.donorfirstx.com/); [MS GIFT donor portal](https://msgift.donorfirstx.com/)).

- **The payment flow:** RCF paid Ren $19.23m in FY2024. That equals 98% of RCF's admin-fee revenue from individual-fundholder accounts, the rate in force since FY2023 **[V]** ([RCF FY2024 audited statements](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf); [RCF FY2023 audited statements](https://renaissancecharitable.org/wp-content/uploads/2026/01/2023RCFAuditedFinancialStatements.pdf); repo [`rcf-ren-audited-admin-payments-2020-2024.csv`](../data/rcf-ren-audited-admin-payments-2020-2024.csv)).
- **Ren's role:** RCF describes it as platform, administrative infrastructure and operational support. Ren is not a technology-only vendor **[V]** ([RCF FAQ](https://renaissancecharitable.org/faqs/)).
- **Ren beyond RCF:** Ren portals also front Morgan Stanley GIFT (new finding), Bank of America's Charitable Gift Fund and AEF ([MS GIFT donor portal](https://msgift.donorfirstx.com/); [BofA Charitable Gift Fund portal](https://bofa.donorfirst.org/); [AEF/Ren release, Apr 2026](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/)). For Bank of America the only evidence is the portal; the earlier 10-K claim is **contradicted** **[V]** ([SEC full-text search, BofA filings](https://efts.sec.gov/LATEST/search-index?q=%22Charitable%20Gift%20Fund%22&ciks=0000070858); [BofA CGF Form 990 TY2024](https://projects.propublica.org/nonprofits/organizations/46010342/202503219349318170/full)). Ren-owned iPhi still serves the Cleveland Foundation and ImpactAssets ([Cleveland Foundation iPhi portal](https://www.iphiview.com/tcf/LogIn/tabid/444/Default.aspx); [ImpactAssets homepage (iPhi log-in)](https://impactassets.org/)). ImpactAssets is a late-stage Give Interactive migration, and iPhi lost 6 of 57 sponsors in 2023–Nov 2026 (§11.2).

**Edward Jones Charitable Gift Fund.** Each role has separate evidence:

| Role | Status | Evidence |
|---|---|---|
| RCF as legal sponsor | Confirmed | Edward Jones product page plus RCF's self-description ([Edward Jones DAF page](https://www.edwardjones.com/us-en/investment-services/investment-products/donor-advised-funds); [RCF FAQ](https://renaissancecharitable.org/faqs/)) |
| RCF manages and administers the fund | Confirmed | Edward Jones portal ([Edward Jones Charitable Gift Fund portal](https://edwardjones.donorfirstx.com/)) |
| Ren technology | Confirmed | Portal displays "DFX powered by Ren" ([Edward Jones Charitable Gift Fund portal](https://edwardjones.donorfirstx.com/)) |
| Ren back-office administration for Edward Jones specifically | Inferred only | RCF pays Ren under an audited contract, but nothing names Ren for Edward Jones ([RCF FY2024 audited statements](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf); repo [`relationship-graph-edges.csv`](../data/mission-2026-11-14/relationship-graph-edges.csv)) |

Two Edward Jones figures remain open:
- The 2021 "$2.9bn" figure is unverifiable (source PDF now 404) **[V]** ([Ren/RCF Edward Jones adviser guide (HTTP 404)](https://www.reninc.com/wp-content/uploads/2022/03/Advisor-Guide-and-FAQ-WH-RCF-2022-1.pdf); repo [`validation-register.csv`](../data/mission-2026-11-14/validation-register.csv)).
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
IRS BMF, Pub 78, revocation and OFAC data sit upstream of every disclosed eligibility check ([IRS EO BMF extract](https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf); [IRS TEOS bulk data downloads](https://www.irs.gov/charities-non-profits/tax-exempt-organization-search-bulk-data-downloads); [IRS Auto-Revocation List](https://www.irs.gov/autorevocationlist); [Chariot compliance help page](https://help.givechariot.com/onboarding/trust-and-safety/compliance); [Candid Charity Check FAQ](https://developer.candid.org/docs/faqs-charity-check); [RCF grantmaking due-diligence policy](https://renaissancecharitable.org/wp-content/uploads/2026/02/Grantmaking-Due-Diligence-Policy.pdf)).

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
- Sponsors charge tiered basis points on balances. Fidelity, DAFgiving360 and Charityvest start at 0.60% on the first $500k ([Fidelity Charitable fees](https://www.fidelitycharitable.org/giving-account/what-it-costs.html); [DAFgiving360 fees and minimums](https://www.dafgiving360.org/features/fees-and-minimums); [Charityvest fee guide](https://guide.charityvest.org/for-donors/fees-and-expenses)). RCF/Ren charges 0.65% with a $250 minimum ([RCF advisor-managed DAF fees](https://renaissancecharitable.org/advisor-managed-dafs/)). Bank of America charges 0.90% flat ([BofA CGF fee schedule](https://www.bankofamerica.com/content/documents/philanthropic/cgf_fee_schedule.pdf)). Daffy charges flat memberships of $0–40/month ([Daffy membership fees](https://help.daffy.org/en/articles/6323771-what-are-daffy-s-membership-fees); repo [`sponsor-fee-schedules.csv`](../data/mission-2026-11-14/sponsor-fee-schedules.csv)).
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
| History loss in platform migrations | Habit ([AEF DonorCentral sunset notice](https://engage.aefonline.org/dc-sunset/)) | Medium |
| Weak nonprofit leverage | Structural ((source: repo inference — no primary URL)) | Medium-High |

**Who resists redesign (by incentive, not intent):** affiliated managers, fee-share administrators, advisers paid on DAF AUM, and discretion-valuing sponsors. ((source: repo inference — no primary URL))
**Who benefits:** working nonprofits, small donors, and challengers not paid on assets. ((source: repo inference — no primary URL))

**Challengers.**
- Daffy reports $2bn in assets (Sept 2026, company-reported) ([Daffy $2B release](https://www.daffy.org/resources/two-billion-assets-under-management)). Its FY2024 990 shows $334.19m net assets **[V]** ([Daffy Charitable Fund Form 990 TY2024](https://projects.propublica.org/nonprofits/organizations/863177440/202513209349301201/full)).
- Charityvest's 2025 figures are company-reported and not comparable to its 990 series **[V]** ([Charityvest 2025 annual report](https://www.charityvest.org/annual-report-2025); [Charityvest Form 990 TY2024](https://projects.propublica.org/nonprofits/organizations/812771871/202513189349315961/full)).
- Both raised effective prices as they moved upmarket ([Vennfi seed release ('zero fees')](https://www.newswire.com/news/this-startup-raised-3-7m-to-let-anyone-donate-stocks-and-etfs-with-a-21260863); [Physician on FIRE on Charityvest fees](https://www.physicianonfire.com/better-donor-advised-fund/); [Charityvest fee guide](https://guide.charityvest.org/for-donors/fees-and-expenses); [Daffy membership tier changes](https://help.daffy.org/en/articles/11730892-how-do-i-change-my-membership)). Incumbents removed minimums (2020) ([ThinkAdvisor on Fidelity minimums](https://www.thinkadvisor.com/2020/09/30/fidelity-charitable-ends-daf-account-minimums/); [Schwab Charitable minimums release](https://www.dafgiving360.org/press-releases/schwab-charitable-expands-access-and-options)).

**Vendor economics.** Ren's corporate revenue, margins and customer concentration are not public ((source: repo inference — no primary URL)). The audited RCF payment is a named service fee, not Ren's ARR ([RCF FY2024 audited statements](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf)). Ren's claims of ">60%", "about half" or "$200bn" of DAF assets are **unsupported** on public evidence: ([Ren homepage](https://www.reninc.com/); [Great Hill investment in Ren (Pulse 2.0)](https://pulse2.com/great-hill-partners-announces-strategic-growth-investment-in-donor-advised-fund-platform-ren/); [AEF/Ren release, Apr 2026](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/))
- On public evidence, sponsors holding about **28%** of FY2024 DAF assets ($91.6bn of $327.9bn) use Ren technology in some form **[V wave 3]**. The full Form 990 harvest (all 1,512 sponsors) finds Ren/Stellar named by 30 sponsors holding $48.55bn (14.8%) in any FY2022–25 return, but only 18 sponsors holding $30.18bn (9.2%) in their latest return [V wave 5], and about 5% (RCF, MS GIFT) on Ren-paid administration. Nearly half of the 28% is NPT, evidenced by hosting (iPhi login redirect, shared Ren load balancer, Ren-hosted "NPT iPhi Statuspage") rather than a disclosed contract ([MS GIFT 990 via GivingTuesday mirror; Goldman PWM portal gspf.goldman.com; NPT GivingPoint](mission-2026-11-14/validation-wave3-report.md)). Ren's "60%+"/"about half" claims remain unreachable without Fidelity Charitable, DAFgiving360 or Vanguard Charitable, none of which shows a Ren vendor; Vanguard chose Give Interactive. (Earlier estimates: 8.7% → 9.0% → 28% of assets after NPT and Goldman evidence.) ([DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`validation-register-wave2b.csv`](../data/mission-2026-11-14/validation-register-wave2b.csv)) <!-- CITE-CHECK RESOLVED 2026-11-14 (text corrected): Validator V2B-05 recomputed $29.65bn = 9.04% for RCF, AEF, MS GIFT and BofA from DAFRC FY2024 (all imputed); the 8.7% ($28.5bn) figure was only partially confirmed. Not changed. -->.
- The "$200bn" figure includes non-DAF assets ([AEF/Ren release, Apr 2026](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/)).
- The arithmetic ceiling outside the four largest sponsors is about 48% **[RT]** ([Fidelity Charitable FY2025 audited statements](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf); [Vanguard Charitable FY2025 financial statements](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf); [DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`validation-register-wave2b.csv`](../data/mission-2026-11-14/validation-register-wave2b.csv)).

---

## 4. Operations: grant workflow, exceptions and portability

**Legal frame.**
- §4966 taxes taxable distributions: 20% on the sponsor, 5% (capped at $10k) on knowing managers ([26 U.S.C. §4966](https://www.law.cornell.edu/uscode/text/26/4966)).
- §4967 taxes prohibited benefits: 125% on the donor or adviser, 10% on knowing managers ([26 U.S.C. §4967](https://www.law.cornell.edu/uscode/text/26/4967)).
- §4958(c)(2) makes grants, loans and compensation to donors or advisers automatic excess benefits ([26 U.S.C. §4958](https://www.law.cornell.edu/uscode/text/26/4958)).
- Grants to listed §170(b)(1)(A) public charities are excepted from §4966, and grantors may rely on IRS status listings ([26 U.S.C. §4966](https://www.law.cornell.edu/uscode/text/26/4966); [Rev. Proc. 2018-32 summary (The Tax Adviser)](https://www.thetaxadviser.com/issues/2018/aug/irs-updates-charitable-contribution-procedures/)).

**Exception share.** Observable non-standard grants (foreign, fiscal-sponsor, non-501(c)(3)) are about 2.5–3% of dollars at the large nationals and far less by count ([Fidelity Charitable Form 990 FY2025](https://projects.propublica.org/nonprofits/organizations/110303001/202601389349301700/IRS990); [DAFgiving360 Form 990 FY2025](https://projects.propublica.org/nonprofits/organizations/311640316/202611199349300601/IRS990ScheduleF); [Vanguard Charitable Form 990 FY2025](https://projects.propublica.org/nonprofits/organizations/232888152/202621329349306657/IRS990); [NPT Form 990 FY2025](https://projects.propublica.org/nonprofits/organizations/237825575/202601289349302480/IRS990ScheduleF); repo [`breadth-community-faith-infrastructure-emerging.md`](../research/mission-2026-11-14/breadth-community-faith-infrastructure-emerging.md)). Foreign grants alone are 1.46% of dollars across the four largest nationals (NPT 4.84%) ([Fidelity Charitable Form 990 FY2025](https://projects.propublica.org/nonprofits/organizations/110303001/202601389349301700/IRS990); [DAFgiving360 Form 990 FY2025](https://projects.propublica.org/nonprofits/organizations/311640316/202611199349300601/IRS990ScheduleF); [Vanguard Charitable Form 990 FY2025](https://projects.propublica.org/nonprofits/organizations/232888152/202621329349306657/IRS990); [NPT Form 990 FY2025](https://projects.propublica.org/nonprofits/organizations/237825575/202601289349302480/IRS990ScheduleF); repo [`breadth-community-faith-infrastructure-emerging.md`](../research/mission-2026-11-14/breadth-community-faith-infrastructure-emerging.md)). This is a floor: new-charity reviews and declines are invisible in filings ((source: repo inference — no primary URL)).

**Discretion beyond tax exposure.** In 2026, after the April 21 SPLC indictment, the California AG's release named Fidelity Charitable, Vanguard Charitable and DAFgiving360 as having restricted grants **[RT confirmed]** ([California AG release](https://oag.ca.gov/node/623769)). Persistence of those holds is unknown ((source: repo inference — no primary URL)).

**Operating metrics.** No sponsor publishes grant turnaround P50/P90, exception rates or reviewer minutes ((source: repo inference — no primary URL)). NPT processed 159,543 grants in FY2025 ([NPT FY2025 annual report](https://www.nptrust.org/annual-reports/npt-annual-report/)). Its U.S. DAF program granted $6.44bn **[V][RT]** ([NPT FY2025 annual report](https://www.nptrust.org/annual-reports/npt-annual-report/)); the $6.61bn release figure likely includes U.K. and Transatlantic programs ([NonProfit Times on NPT FY2025](https://thenonprofittimes.com/?p=215695); [NPT FY2025 annual report](https://www.nptrust.org/annual-reports/npt-annual-report/)).

**Portability.**
- None of 12 sponsors reviewed publishes an outbound transfer policy (repo [`sponsor-transfer-portability-terms.csv`](../data/mission-2026-11-14/sponsor-transfer-portability-terms.csv)). Transfers are cash after liquidation and take 10 business days to 4 weeks ([Fidelity Charitable recommending a grant](https://www.fidelitycharitable.org/giving-account-guide/recommending-a-grant.html); [GTCF DAF transfer instructions](https://www.gtcf.org/wp-content/uploads/2026.05.18-GTCF_DAF_Transfer_Instructions.pdf)).
- No sponsor commits to moving grant history ([GTCF DAF transfer instructions](https://www.gtcf.org/wp-content/uploads/2026.05.18-GTCF_DAF_Transfer_Instructions.pdf); [Daffy help: closing an account](http://help.daffy.org/en/articles/6520234-how-do-i-close-my-daffy-account)). AEF's own migration kept two years ([AEF DonorCentral sunset notice](https://engage.aefonline.org/dc-sunset/)).
- About $7.5bn moved sponsor-to-sponsor in 2024 ([Inequality.org on DAF-to-DAF giving](https://inequality.org/article/daf-to-daf-giving-2024/)).

Sources: prior batch 2A/2B/2C files; [regulation and portability](mission-2026-11-14/regulation-market-structure-portability.md); [breadth §6](mission-2026-11-14/breadth-community-faith-infrastructure-emerging.md).

---

## 5. Technology history: announced vs delivered

The timeline has 195 dated events across 16 company groups and 163 source URLs (repo [`company-timeline-events.csv`](../data/mission-2026-11-14/company-timeline-events.csv); repo [`announced-vs-delivered.csv`](../data/mission-2026-11-14/announced-vs-delivered.csv)). Of 39 announced capabilities: (repo [`announced-vs-delivered.csv`](../data/mission-2026-11-14/announced-vs-delivered.csv))

| Delivery status | Count |
|---|---|
| Evidence of delivery | 15 |
| Partial | 10 |
| No public evidence yet | 12 |
| Contradicted | 2 |

By company:
- **Daffy:** 5 of 5 delivered. ([Daffy MCP docs](https://docs.daffy.org/agents/mcp); [Daffy membership tier changes](https://help.daffy.org/en/articles/11730892-how-do-i-change-my-membership); repo [`announced-vs-delivered.csv`](../data/mission-2026-11-14/announced-vs-delivered.csv))
- **Chariot Disbursements:** the clearest beta-to-production trail ([Chariot Disbursements FAQ](https://docs.givechariot.com/guides/disbursements/faq); [Chariot partner profile: Daffy](https://www.givechariot.com/resources/insights/getting-to-know-daffy-a-chariot-disbursements-partner); repo [`announced-vs-delivered.csv`](../data/mission-2026-11-14/announced-vs-delivered.csv)).
- **TIFIN Give:** announces most often, and its Louise AI has only vendor evidence ([TIFIN Give Louise release](https://www.prnewswire.com/news-releases/tifin-give-launches-louise-ai-capabilities-for-philanthropy-302595069.html); repo [`announced-vs-delivered.csv`](../data/mission-2026-11-14/announced-vs-delivered.csv)).
- **Ren and Foundation Source:** broad claims (daily unitization, DAF OS) with little public delivery evidence ([Ren faith/community foundation page](https://www.reninc.com/faith-based-community-foundations/); [Foundation Source DAF OS brief](https://foundationsource.com/resources/product-briefs/the-modern-operating-system-for-donor-advised-funds/); repo [`announced-vs-delivered.csv`](../data/mission-2026-11-14/announced-vs-delivered.csv)).

**Private-equity ownership changes are followed fast by leadership change and roll-ups.** GTCR named a new CEO at Foundation Source six days after closing, followed by four acquisitions in about 17 months ([GTCR acquires Foundation Source](https://foundationsource.com/newsroom/press-releases/gtcr-announces-acquisition-of-foundation-source/); [Foundation Source press releases (CEO, PG Calc)](https://foundationsource.com/category/newsroom/press-releases/page/5/); [Foundation Source acquires PG Calc](https://foundationsource.com/newsroom/press-releases/foundation-source-announces-acquisition-of-pg-calc-leading-provider-of-planned-giving-solutions/); [Foundation Source acquires Vennfi](https://foundationsource.com/newsroom/press-releases/foundation-source-acquires-vennfi-the-fintech-powering-donor-advised-fund-charityvest/); [Foundation Source acquires Giving Place](https://foundationsource.com/newsroom/press-releases/foundation-source-acquires-giving-place-platform-for-private-foundations-and-family-offices/); [Pacific Foundation Services deal record](https://www.privsource.com/acquisitions/deal/n8S0zL); repo [`company-timeline-events.csv`](../data/mission-2026-11-14/company-timeline-events.csv)). Customer effects are unobserved ((source: repo inference — no primary URL)).

**Ren's dates, scale claims and SOC 2 type drift over time.** (repo [`company-timeline-events.csv`](../data/mission-2026-11-14/company-timeline-events.csv)) SOC 2 is stated as "Type 2" in July 2025 and "Type 1" in April 2026, both in Ren's own boilerplate; no report has been seen **[V]** ([AEF/Ren release, Jul 2025](https://www.aefonline.org/thought-leadership/american-endowment-foundation-selects-ren-as-a-strategic-partner-to-expand-philanthropy-drive-innovation-and-foster-growth-in-financial-services/); [AEF/Ren release, Apr 2026](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/)).

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
- **There is no public evidence of AI in sponsor-side approval or eligibility determination.** (repo [`ai-use-case-inventory.csv`](../data/mission-2026-11-14/ai-use-case-inventory.csv); repo [`validation-register-wave2a.csv`](../data/mission-2026-11-14/validation-register-wave2a.csv)) The one sponsor-side exception is Daffy's announced charity-data flagging **[RT]** ([FF News on Daffy AI](https://ffnews.com/newsarticle/paytech/daffy-is-using-ai-to-reshape-the-future-of-charitable-giving/)).
- The agentic frontier is donor-side: TIFIN Give's Louise executes donor requests, and Daffy's MCP server exposes `make_donation` with no documented limits **[V]** ([TIFIN Give Louise release](https://www.prnewswire.com/news-releases/tifin-give-launches-louise-ai-capabilities-for-philanthropy-302595069.html); [Daffy MCP docs](https://docs.daffy.org/agents/mcp)).

**Economics** ([AI economics](mission-2026-11-14/ai-economics-replacement-analysis.md), with red-team corrections):
- Inference cost is immaterial: about $0.45 per heavy document review against about $83 of reviewer time **[V]** ([Anthropic API pricing](https://platform.claude.com/docs/en/about-claude/pricing); [BLS compliance officers (May 2025)](https://www.bls.gov/ooh/business-and-financial/compliance-officers.htm); [BLS ECEC June 2026](https://www.bls.gov/news.release/ecec.nr0.htm); repo [`ai-process-economics.csv`](../data/mission-2026-11-14/ai-process-economics.csv)).
- The model's result that "AI on the existing workflow ranks last in 16/16 processes" is **determined by its assumptions**, not by evidence about AI **[RT]** (repo [`ai-process-economics.csv`](../data/mission-2026-11-14/ai-process-economics.csv); repo [`validation-register-wave2a.csv`](../data/mission-2026-11-14/validation-register-wave2a.csv); repo [`red-team-wave2a-ai-and-entrant.md`](../research/mission-2026-11-14/red-team-wave2a-ai-and-entrant.md)).
- What is reasoned rather than modelled: redesign removes exception classes, while AI only shortens handling. AI economics clear plausible governance costs at vendor or network scale, not per process per sponsor. ((source: repo inference — no primary URL))
- The single most important missing evidence is a measured exception, handling-time and QA study at any sponsor. ((source: repo inference — no primary URL))

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
- **Gating question:** do sponsor–vendor contracts grant API and data-export rights? ((source: repo inference — no primary URL)) **Round-2 answer (partial):** public vendor templates allow batch export but not live integration, no top-10 sponsor publishes a donor-side export, and several sponsor terms bar credential sharing or automation (§11.4). Executed contracts remain unseen.

---

## 9. Evidence quality, validation and limits

**Independent validation and red-team review** checked **80 consequential claims** (repo [`validation-register.csv`](../data/mission-2026-11-14/validation-register.csv); repo [`validation-register-wave2a.csv`](../data/mission-2026-11-14/validation-register-wave2a.csv); repo [`validation-register-wave2b.csv`](../data/mission-2026-11-14/validation-register-wave2b.csv)). These were done by agents that did not author the work and were not given the original conclusions.

| Result | Count |
|---|---|
| Confirmed | 45 |
| Partially confirmed | 25 |
| Contradicted | 7 |
| Unable to verify | 3 |

Model arithmetic, the DAFRC recomputation and 6 hand-checked derived metrics reproduced exactly ([DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); repo [`validation-register-wave2a.csv`](../data/mission-2026-11-14/validation-register-wave2a.csv); repo [`validation-register-wave2b.csv`](../data/mission-2026-11-14/validation-register-wave2b.csv)). Corrections were appended to source documents as dated, governing sections; no original text was deleted.

**Limits.**
- All evidence is public-source. No vendor tests, sponsor interviews or contracts were obtained. ((source: repo inference — no primary URL))
- The shared web-search budget ran out during the mission. Some items rest on direct fetches or search summaries and are flagged. (repo [`regulation-market-structure-portability.md`](../research/mission-2026-11-14/regulation-market-structure-portability.md); repo [`breadth-community-faith-infrastructure-emerging.md`](../research/mission-2026-11-14/breadth-community-faith-infrastructure-emerging.md))
- The Wayback Machine could not be read. ((source: repo inference — no primary URL))
- The coverage matrix measures depth on a purposive set of 33 entities, not the about-1,500-sponsor universe ([DAFRC Annual DAF Report page](https://www.dafresearchcollaborative.org/research/annual-daf-report); repo [`coverage-matrix-entities.csv`](../data/mission-2026-11-14/coverage-matrix-entities.csv)).

**Evidence that would most change this report:**
1. A sponsor time-and-motion study.
2. Ren's denominator for its share claims.
3. Give Interactive's scope at Vanguard Charitable.
4. Sponsor–vendor API and data-export clauses.
5. Fund-level payout by fee model.
6. Final §4966/6033 guidance.

Round 2 partly answered items 2–4: Ren's footprint is measured several ways (§3), Give Interactive appears to be Vanguard Charitable's ledger only (§11.2), and public API and export terms are mapped (§11.4). Validation waves 3–12 are reported per wave and listed in §11. See [synthesis §F](mission-2026-11-14/strategic-synthesis.md) and the [research queue](../data/mission-2026-11-14/research-priority-queue.csv).

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

New evidence: GiveClear's audited 2024 statements, which carry an unmodified opinion.

The v1.1 AI overlay has no GREEN providers:
- **RED (provisional):** Benevity Match Assurance.
- **AMBER (near red):** TIFIN Give/GiveClear Louise.
- **AMBER:** Daffy MCP, Chariot, Foundant, Blackbaud, Goodstack, and Candid (low).

**v1.1 consensus: the current reference** ([quadrant-v11-blind-and-calibration.md](mission-2026-11-14/quadrant-v11-blind-and-calibration.md)).

A blind second scorer under v1.1 matched the fresh scorer exactly on 74% of commonly scored cells and within 1 point on 99.7%. 22 of 28 placeable providers landed in the same quadrant. Final status: 22 reproduced, 11 adjudicated, 9 insufficient evidence. This table **supersedes the v1.0 table above**, which is retained for history.

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
- Excluding Givinga drops the processor share of accounts from 80.5/77.4/79.5% (FY2022/23/24) to 63.0/67.0/66.0% (59.2% for FY2024 on corrected data).
- FY2022 account growth flips from +72% to −7%.
- Givinga's account unit is undefined [V wave 5]. In CY2022 its largest fundraiser was a charity sweepstakes operator, so game or app-user records are one candidate explanation and employer-provisioned employee accounts are another. Neither is confirmed, and the count fell in 2023 and rose by 465k in 2024 with no named fundraiser.
- Recommendation: exclude SDG Impact Fund from market totals and footnote it.
- Corrected FY2024 totals ($323.27bn) are in §1.

**Payout net of DAF-to-DAF transfers** ([queue-net-payout-fidelity-outliers.md](mission-2026-11-14/queue-net-payout-fidelity-outliers.md); `scripts/mission_net_payout.py`) [V wave 11]
- Scope: FY2021–24 pooled, sponsors with itemised Schedule I, excluding processors (n = 3,373 sponsor-years).
- Gross payout is 23.9%. Net payout is 21.5%, 20.8% or 19.0%, depending on how widely sponsor-to-sponsor transfers are defined.
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
- Headline shares: about 28% of FY2024 DAF assets on Ren technology in some form; 9.2% at sponsors naming Ren/Stellar in their latest 990 (14.8% in any FY2022–25 return); about 5% on Ren-paid administration.

**NPT GivingPoint is a Ren white-label book** ([queue-npt-givingpoint-fidelity-stack.md](mission-2026-11-14/queue-npt-givingpoint-fidelity-stack.md)) [V wave 12]
- 13 live program sites run on the same Ren build and carry NPT or NPT UK sponsor text: J.P. Morgan Charitable Gift Fund, UBS, BMO, Glenmede, Tolleson, Pitcairn, NPT UK, NPT Transatlantic, Rathbones, Cazenove Capital and others.
- Eight sit on Ren's load balancer. The rest are on an AWS Global Accelerator pair, attributed to Ren by inference.
- NPT's payment to Ren is undisclosed. No Ren, Stellar or iPhi payee appears, and the fee most likely sits in the $5.87m IT line (+$2.22m).
- Ren is NPT's technology and hosting vendor, not its administrator.
- NPT, J.P. Morgan and ICGF iPhi hosts now redirect to Ren-hosted GivingPoint sites naming NPT as sponsor ([queue-ren-iphi-attrition.md](mission-2026-11-14/queue-ren-iphi-attrition.md)) [V wave 11].

**Ren iPhi attrition, 2023–Nov 2026** ([queue-ren-iphi-attrition.md](mission-2026-11-14/queue-ren-iphi-attrition.md); `scripts/mission_ren_iphi_attrition.py`) [V wave 11]
- 6 of 57 sponsors left, or 10.5% (Wilson interval 4.9–21.1%). The strict rate is 8.8%, because Gulf Coast's move is still "launching soon".
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
- Outside the top 30, Greater Washington (#38) has used Blackbaud and REPAY (two separate firms) since Sept 2026 [V wave 7].
- The community-foundation channel is fragmented and largely runs its own ACH, which leaves an open payments field without a dominant rail.

**What nonprofits pay to receive DAF grants** ([queue-nonprofit-side-panel.md](mission-2026-11-14/queue-nonprofit-side-panel.md), 33 entities [V wave 12]; [queue-agentic-products-dafpay-fees.md](mission-2026-11-14/queue-agentic-products-dafpay-fees.md) [V wave 8])
- Sponsors charge nonprofits $0 to receive grants. The exceptions are Benevity (2.99%, cap $500), DAFpay at default terms (2.9%) and ForGood (1.5%).
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

- Pool choice is as large a lever as sponsor choice. Fidelity's 60%-equity pool costs 0.55%; its index pool costs 0.015%.
- Edward Jones's 0.70% program fee rests on help pages that now return 404, so it is low confidence.

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
- On termination, licensees must stop all use of the data.
- Data mining is barred for building a database, reselling or competing with Candid.
- Charity Check draws on Pub78, the BMF, the IRB, revocations and the OFAC SDN list.

### 11.5 AI and agentic controls

**Agentic giving products** ([queue-agentic-products-dafpay-fees.md](mission-2026-11-14/queue-agentic-products-dafpay-fees.md)) [V wave 8]
- None of 21 agentic giving products (2024–26) has independent outcome evidence, and no product touches sponsor approval.

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
- AI on the existing workflow ranks first in at most 17% of draws.
- Inference cost is immaterial.
- One AI project exceeds the entire IT line of a $250m community foundation in 67% of draws.

What changes:
- "AI ranks last everywhere" fails for complex-asset and non-standard-grantee review.
- A shared AI platform breaks even in 43% of draws with the five largest nationals in the network, and in 0.4% with community foundations under $250m alone.
- A $120k/yr AI product cannot be funded from process savings below about $1bn of DAF assets. The economic buyer is an administrator or platform vendor, not an individual sponsor.

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
- Hg exits or uses a continuation vehicle for Benevity (2026–28).
- Apax sells or recapitalises Bonterra (2027–28). Bonterra bought Deed in Mar 2026, putting it head-to-head with Benevity.
- GTCR sells Foundation Source (2027–29).
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
- DAFgiving360 fees and minimums (accessed 2026-11-14 (search snippet; page 403)): https://www.dafgiving360.org/features/fees-and-minimums
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
