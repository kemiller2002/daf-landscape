# Red-team validation, wave 2b: vendor graph, quantitative datasets, incentives

**Validator:** red-team-agent-wave2b (independent; did not author the documents under review). **Date:** 2026-11-14.
**Register:** [`data/mission-2026-11-14/validation-register-wave2b.csv`](../../data/mission-2026-11-14/validation-register-wave2b.csv) (27 claims, V2B-01 to V2B-27).
**Under review:** `vendor-dependency-concentration.md` (+ graph CSVs), `quantitative-datasets-and-data-dictionary.md` (+ datasets, `scripts/mission_daf_metrics.py`), `industry-incentives-structural-analysis.md` (+ `incentive-map.csv`).

Primary documents were retrieved independently: [Fidelity Charitable FY2025 audit](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf), [RCF FY2024 audit](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf), [Vanguard Charitable FY2025 statements](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf), the [DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx) and [report page](https://www.dafresearchcollaborative.org/research/annual-daf-report), the [Federal Register API](https://www.federalregister.gov/api/v1/documents.json?conditions[term]=%22donor-advised%22+4966), the [IRS 2026–2027 Priority Guidance Plan PDF](https://www.irs.gov/pub/irs-counsel/2026-2027-initial-pgp.pdf), the [CA Attorney General release](https://oag.ca.gov/node/623769), the [NPT annual report](https://www.nptrust.org/annual-reports/npt-annual-report/), the AEF/Ren releases ([AEF/Ren release, 2026-04-08](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/); [AEF, 2025-07-23](https://www.aefonline.org/?p=14296)), Ren's homepage ([reninc.com](https://www.reninc.com/)) and the live portals (URLs per edge in `data/mission-2026-11-14/relationship-graph-edges.csv`).

## Results

| Result | n |
|---|---|
| confirmed | 13 |
| partially_confirmed | 11 |
| contradicted | 3 |
| unable_to_verify | 0 (one sub-element, Fidelity's July 2026 EFT-only date, is unverified inside [V2B-13](https://www.fidelitycharitable.org/nonprofits/faqs.html)) |

---

## 1. Findings ranked by severity

### Critical

**F1. The graph doc's sponsor-asset concentration mixes two periods ([V2B-01](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf), [V2B-03](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf)).** In §5.1 the graph doc divides June-2025 values by a June-2024 denominator:

- **The numerators are June 2025.** The doc uses Fidelity $85.86bn, NPT $55.90bn, DAFgiving360 $47.42bn and Vanguard $27.21bn (`research/mission-2026-11-14/vendor-dependency-concentration.md` §5.1; [Fidelity FY2025 audit](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf); [Vanguard Charitable FY2025 statements](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf)).
- **The denominator is June 2024.** DAFRC's FY2024 total of $327.87bn already contains these same four sponsors at June-2024 values: $66.20bn, $42.12bn, $40.94bn and $21.95bn ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)).
- **Proof of DAFRC's convention.** Fidelity's audited net assets were $66,543,007,630 at 6/30/2024 ([Fidelity FY2025 audit](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf)), which matches DAFRC's FY2024 row of $66.20bn ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)). Vanguard's were $22.08bn at 6/30/2024 ([Vanguard Charitable FY2025 statements](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf)) against DAFRC's $21.95bn. DAFRC labels a June fiscal year by the year in which it ends. The graph doc assumed the IRS tax-year convention instead, which labels a fiscal year by the year in which it begins.
- **Effect.** The four numerators are inflated by about $45bn. CR3 is overstated by about 12 percentage points and HHI by about 460 points (`data/mission-2026-11-14/derived-metrics.csv`; `research/mission-2026-11-14/vendor-dependency-concentration.md`).
- **Knock-on errors.** Three other figures carry the same mismatch:
  - "~49% affiliate-administered" should be 39.4% ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)).
  - "~66% big four" should be 52.2% ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)).
  - "at most ~34% for everyone else" should be 47.8% ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)).
- **The band also changes.** The "moderately concentrated" label is wrong for the all-sponsor universe, where HHI is 830 (unconcentrated, below 1,000). It holds only for national sponsors, where HHI is 1,566 (`data/mission-2026-11-14/derived-metrics.csv`).

### High

**F2. Ren's market-share claim is misquoted, and the bound used to dispute it is wrong ([V2B-04](https://www.reninc.com/), [V2B-27](https://oag.ca.gov/node/623769)).** What Ren actually says depends on the source:

| Source | Ren's wording |
|---|---|
| [reninc.com](https://www.reninc.com/) (live) | "60%+ U.S. DAF assets using Ren technology"; "$200B+ Charitable assets supported" |
| [AEF/Ren release, 2026-04-08](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/) | "approximately $200 billion of donor-advised funds **and other charitable assets**" |
| [Great Hill release, 2025-10-28](https://www.businesswire.com/news/home/20251028702541/en/Great-Hill-Partners-Announces-Strategic-Growth-Investment-in-Philanthropy-Tech-Platform-Ren) | "$175 billion in charitable funding … approximately half of all donor-advised fund assets" |

- **The $200bn figure is not a DAF number.** It must not be converted into "61% of DAF assets". ([AEF/Ren release, 2026-04-08](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/); [reninc.com](https://www.reninc.com/))
- **The correct ceiling for sponsors outside the big four is 47.8%, not 34%** ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)).
- **The 60% claim still cannot hold without a big-four sponsor.** One arithmetic fit stands out: the 47.8% residual plus NPT's 12.85% equals 60.6% ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)), which almost exactly matches Ren's "60%+" ([reninc.com](https://www.reninc.com/)).
  - This is consistent with Ren counting NPT through the Stellar/iPhi lineage. Ren bought Stellar in January 2023 ([Ren on Stellar acquisition, 2023-01-20](https://www.reninc.com/blog/ren-bolsters-philanthropic-tech-services-offerings-with-acquisition-of-stellar-technology-solutions/)), and NPT's portal was hosted on Stellar in 2020 (source: repo `research/mission-2026-11-14/vendor-dependency-concentration.md` — historical 2020 document, no primary URL in register).
  - It would also require Ren to touch essentially every other sponsor, which is implausible given that Foundant and Blackbaud serve community foundations ([Tech Impact, 2022](https://techimpact.org/sites/default/files/2024-03/TECH%20IMPACT%20Integrated%20Software%20for%20Community%20Foundations.pdf)).
- **Keep the status at disputed.**

**F3. The incentives doc's fee-to-payout causation is overstated, and its labels are inconsistent ([V2B-22](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)).**

- **The labels disagree.** The same claim is rated "suggestive, Medium" in §1, "Structural, Medium-High" in §9 (`industry-incentives-structural-analysis.md`), and "structural constraint" in the incentive map (`data/mission-2026-11-14/incentive-map.csv`).
- **The cross-sectional evidence runs the other way.** I recomputed from the DAFRC panel (filed values, sponsors with at least $1m of prior assets, FY2023 median sponsor payout): ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx))

| Sponsor segment | Median payout | n |
|---|---|---|
| National standard | 20.0% ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)) | 64 |
| Community foundations | 11.0% ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)) | 609 |
| University/healthcare | 5.4% (49% of these sponsors pay out under 5%) ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)) | 73 |

- **Implication.** The sponsors with the tightest affiliate AUM-fee linkage (Fidelity 22.8%, DAFgiving360 21.0%, NPT 24.4%; `data/mission-2026-11-14/derived-metrics.csv`) pay out about twice the median sponsor. That the incentive *exists* is documented. Any *effect* on payout or grant speed is unsupported and confounded by donor mix.

**F4. The incentives doc's Outcome A (paper checks) omits the most relevant fact ([V2B-13](https://www.fidelitycharitable.org/nonprofits/faqs.html)).**

- **What the live Fidelity FAQ says.** It says "we do not currently require EFT enrollment". It also says "As Fidelity Charitable moves towards a digital-first policy we are transitioning grant payments to EFT" ([Fidelity nonprofit FAQ](https://www.fidelitycharitable.org/nonprofits/faqs.html)).
- **What Chariot reports (Mar 2026).** 67% of Fidelity grants already go by EFT (about 1m checks in 2025), and Fidelity is "moving to electronic-only disbursement in July 2026" ([Chariot, Mar 2026](https://www.givechariot.com/resources/insights/top-8-takeaways-from-fidelity-charitables-2026-giving-report)).
  - The July date is not on the live official page ([Fidelity nonprofit FAQ](https://www.fidelitycharitable.org/nonprofits/faqs.html)), so it is unverified.
- **Effect on the doc's claims.** This contradicts "neither faces a forcing incentive" and "industry-wide check share not observed". It supports sponsor controllability: the largest sponsor is pulling the control point itself.

### Medium

- **F5. The §4966 status sourcing is wrong ([V2B-08](https://www.federalregister.gov/api/v1/documents.json?conditions[term]=%22donor-advised%22+4966)).**
  - **The core claim stands.** Not finalized is now confirmed rather than inferred: the Federal Register shows no final rule as of 2026-11-14 ([Federal Register API](https://www.federalregister.gov/api/v1/documents.json?conditions[term]=%22donor-advised%22+4966)).
  - **The PGP attribution is wrong.** The 2026–2027 Priority Guidance Plan was released on **2026-09-29** ([IRS 2026–2027 PGP](https://www.irs.gov/pub/irs-counsel/2026-2027-initial-pgp.pdf)), so it cannot come from the May/June sources S02/S03. Its item reads "Guidance under §§4966 and 6033 regarding certain donor advised fund arrangements", which replaces "final regulations under §4966". The plan is framed around deregulation and burden reduction.
  - **The comment deadline is wrong.** It was extended to **Feb 15, 2024**, not Jan 16 ([FR 2024-00260](https://www.federalregister.gov/d/2024-00260)).
- **F6. AEF administration is understated ([V2B-16](https://www.aefonline.org/?p=14296)).** Edge E086 is marked inferred. However, AEF's 2025-07-23 release ([AEF, 2025-07-23](https://www.aefonline.org/?p=14296)) says Ren is a "technology and administrative services partner", so the status should be **confirmed**.
- **F7. Vanguard is a hybrid, not "affiliate-administered" ([V2B-03](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf), [V2B-11](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf)).** Vanguard Group receives a $4.01m service fee ([Vanguard Charitable FY2025 statements](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf)). The 0.60% admin fee "is used to pay the operating expenses of Vanguard Charitable" ([Vanguard Charitable FY2025 statements](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf)). "Fees track assets" therefore holds for Vanguard only through fund expense ratios.
- **F8. The "manual review of listed charities: mixed, leaning habit" label is weakened by the SPLC holds ([V2B-26](https://pulse2.com/great-hill-partners-announces-strategic-growth-investment-in-donor-advised-fund-platform-ren/)).** The SPLC was a listed charity throughout, and BMF reliance does not cover criminal-charge or reputational risk. Drop "leaning habit".
- **F9. The graph omits SVCF and NCF.** SVCF ($9.58bn, #6; [DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)) and NCF are missing from the §5.1 table ([V2B-25](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)). The graph doc's caveat that "the full DAFRC sponsor file has not been downloaded" is stale, because the companion dataset contains it.

### Low

- **RCF "$5.91bn Schedule D" ([V2B-24](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf)).** The figure is audited net assets of $5.90bn ([RCF FY2024 audit](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf)). DAFRC's Schedule D values for RCF are imputed: $5.63bn and 22,366 accounts ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)).
- **Fee tiers ([V2B-12](https://www.fidelitycharitable.org/content/dam/fc-public/docs/advisors/giving-account-administrative-fees.pdf)).** RCF's 60/30/20/15 schedule applies only to donor-directed DAFs ([RCF donor-directed DAFs](https://renaissancecharitable.org/donor-directed-dafs/)).
- **Edge E151.** It is typed `payment_processor`, but the evidence shows only DAFpay donor checkout ([Chariot llms.txt](https://www.givechariot.com/llms.txt)).

---

## 2. Adjudications

**(a) CR3 57.7% / HHI 1,289 (graph doc) vs CR3 45.5% / HHI 830 (datasets doc; `data/mission-2026-11-14/derived-metrics.csv`).**
- **The datasets doc is correct** for the definition "share of DAFRC FY2024 sponsor-held DAF assets, all 1,506 sponsors with positive values". I independently recomputed CR3 45.52%, CR5 55.83% and HHI 830.31 ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)).
- **The graph doc's numbers are an artifact of period misalignment** (F1). Its arithmetic is correct: I reproduced 57.70% and 1,289.2 (`research/mission-2026-11-14/vendor-dependency-concentration.md`).
- **Defensible alternative definitions:**
  - national sponsors only: CR3 63.2%, HHI 1,566 (`data/mission-2026-11-14/derived-metrics.csv`);
  - filed values only: HHI 1,600 (`data/mission-2026-11-14/derived-metrics.csv`). This is not market concentration, because imputed small sponsors drop out.
- **Caveat.** About 30% of FY2024 assets are imputed ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)). That could move HHI by tens of points, not hundreds.

**(b) Ren's 53–61% ($175–200bn; [Great Hill release, 2025-10-28](https://www.businesswire.com/news/home/20251028702541/en/Great-Hill-Partners-Announces-Strategic-Growth-Investment-in-Philanthropy-Tech-Platform-Ren); [AEF/Ren release, 2026-04-08](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/)) vs the graph's bound.**
- **The graph doc's ceiling is wrong.** The ceiling is 47.8%, not 34%, for sponsors outside the big four ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)).
- **The ratio itself is miscomputed.** The $200bn is "DAFs and other charitable assets" ([AEF/Ren release, 2026-04-08](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/)), so 61% is not a valid DAF ratio.
- **Ren's homepage "60%+ of DAF assets" remains irreconcilable** unless Ren counts at least one big-four sponsor (NPT fits numerically) plus nearly all other sponsors. ([reninc.com](https://www.reninc.com/); [DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx))
- **Verdict: disputed**, with a sharper and testable hypothesis: is NPT GivingPoint on iPhi/Ren today?

**(c) NPT FY2025 grants: $6.44bn ([NPT annual report](https://www.nptrust.org/annual-reports/npt-annual-report/)) vs $6.61bn ([NonProfit Times](https://thenonprofittimes.com/?p=215695)).**
- **$6.44bn** comes from the annual report, which states it "reflects NPT's U.S. donor-advised fund program only". It excludes NPT UK and Transatlantic, rose 17%, and covers 159,543 grants ([NPT annual report](https://www.nptrust.org/annual-reports/npt-annual-report/)).
- **$6.61bn** comes from press coverage dated 2025-12-01 ([NonProfit Times](https://thenonprofittimes.com/?p=215695)). It rose 20% and mentions the affiliates.
- **Verdict.** The $0.17bn gap is most plausibly affiliate grantmaking (inferred; source: repo inference — no primary URL). Use **$6.44bn** for any US-DAF or DAFRC comparison.

**(d) SPLC: confirmed.**
- **The core facts check out.** The CA AG release (2026-05-22; [CA AG release, 2026-05-22](https://oag.ca.gov/node/623769)) states the DOJ indictment of April 21, 2026. It names Fidelity Investments Charitable Gift Fund, Vanguard Charitable Endowment Program and Donor Advised Charitable Giving, Inc. as having stopped payments, and records that 16 AGs signed.
- **Corroboration.** The Chronicle of Philanthropy, ProPublica and Fox Business report the same.
- **Not verified.** Whether the holds are still in place in November 2026 (last primary record: [CA AG release, 2026-05-22](https://oag.ca.gov/node/623769)).
- **Wording fix.** The incentives doc should say "DAFgiving360 (Donor Advised Charitable Giving, Inc.)".

**(e) 2023 proposed §4966 regulations: still proposed as of 2026-11-14 ([Federal Register API](https://www.federalregister.gov/api/v1/documents.json?conditions[term]=%22donor-advised%22+4966)).**
- **The record.** The Federal Register shows only the NPRM (2023-11-14), the comment extension (2024-01-09) and the hearing notices (2024-02-29, 2024-04-19). There is no final rule ([Federal Register API](https://www.federalregister.gov/api/v1/documents.json?conditions[term]=%22donor-advised%22+4966)).
- **The 2026–27 PGP.** It was released 2026-09-29 and carries a re-scoped "guidance under §§4966 and 6033" item ([IRS 2026–2027 PGP](https://www.irs.gov/pub/irs-counsel/2026-2027-initial-pgp.pdf)).
- **Recent signal.** Tax Notes (2026-10-07, secondary) reports that the IRS expects new guidance soon (source: Tax Notes, paywalled — no URL in `validation-register-wave2b.csv`).
- **Uncertainty.** It now concerns scope as much as timing.

---

## 3. Reproduced calculations

`python3 scripts/mission_daf_metrics.py` reported "1372 rows; recompute mismatches: 0" and produced a byte-identical `derived-metrics.csv`. Hand checks against the input files:

| Metric | Hand calculation | File value |
|---|---|---|
| CAGR of DAFRC assets, FY20–24 (`data/mission-2026-11-14/derived-metrics.csv`) | (327.87/168.76)^0.25 − 1 = 0.18061 | 0.180614 |
| FY2024 market payout (beginning assets) ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)) | 64,602,340,649 / 256,387,402,068 = 0.25197 | 0.251972 |
| Fidelity FY2024 sponsor payout ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)) | 12,657,447,280 / 55,604,736,854 = 0.22763 | 0.227633 |
| FY2024 filed share of assets ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)) | 0.70182 | 0.701824 |
| FY2024 contributions YoY ([DAFRC memo](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf)) | 90.57 / 65.36 − 1 = 0.38571 | 0.38571 |
| FY2024 asset HHI, all rows (`data/mission-2026-11-14/derived-metrics.csv`) | 830.31 | 830.31 |

The graph doc's figures were also reproduced from its own inputs:
- the nine shares sum to 78.5% (`research/mission-2026-11-14/vendor-dependency-concentration.md`);
- CR3 is 57.70%, CR4 65.99% and CR5 69.84% (`research/mission-2026-11-14/vendor-dependency-concentration.md`);
- HHI is 1,289.2 (`research/mission-2026-11-14/vendor-dependency-concentration.md`).

Period-aligned, using DAFRC FY2024:
- the big four hold 52.2% ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx));
- the three affiliate-administered sponsors hold 39.4% ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx));
- the four Ren-evidenced sponsors hold 9.04% ($29.65bn) ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)).

---

## 4. Edge sample (15 random `confirmed` edges, seed 20261114)

| Edge | Check | Verdict |
|---|---|---|
| E023 RCF sponsor_of RBC program ([portal](https://rbcrcf.donorfirstx.com/)) | portal names "Renaissance Charitable Foundation Donor-Advised Fund Program for RBC WM Clients" | OK |
| E072 RCF sponsor_of Pershing channel ([Ren](https://www.reninc.com/rcf-pershing-daf/)) | "RCF … must be listed as the account owner"; TU5 | OK |
| E151 Chariot payment_processor Thrivent ([llms.txt](https://www.givechariot.com/llms.txt)) | llms.txt: "Thrivent Charitable on DAFpay" | **Type issue**: donor checkout, not grant disbursement |
| E158 Benevity → AOGF ([Benevity help](https://causeshelp.benevity.org/hc/en-us/articles/360001149426-What-charitable-foundations-does-Benevity-work-with-granting-disbursing-entities)) | help page returned 403; search shows AOGF disburses US Benevity donations | OK (search excerpt) |
| E041 UBS distributes RCF option ([UBS fact sheet](https://advisors.ubs.com/mediahandler/media/662455/Donor%20Advised%20Fund%20FactSheet.pdf)) | fact sheet: "four national sponsoring organizations: Fidelity Charitable, Impact Assets, National Philanthropic Trust, Renaissance Charitable" | OK |
| E155 Candid → Groundswell ([Groundswell](https://www.groundswell.io/products/donor-advised-fund)) | "Built-In Integration with Candid's Guidestar" | OK (vendor claim) |
| E007 Ren acquirer Stellar | Jan 20, 2023 ([Ren on Stellar acquisition, 2023-01-20](https://www.reninc.com/blog/ren-bolsters-philanthropic-tech-services-offerings-with-acquisition-of-stellar-technology-solutions/)) | OK |
| E140 AssetMark → GiveClear ([GiveClear](https://www.giveclear.org/reports-and-financials)) | "AssetMark enables streamlined charitable giving" | OK |
| E071 Fisher channel ([Ren](https://www.reninc.com/rcf-fisher-daf/)) | Ren page guide; RCF owner | OK |
| E138 TIFIN Give → GiveClear ([Chariot](https://www.givechariot.com/resources/insights/getting-to-know-tifin-give-a-chariot-disbursements-partner-)) | Chariot profile | OK |
| E048 GiveClear sponsor_of SEI Charitable Fund | "sponsored by GiveClear Foundation", Oct 28, 2026 ([SEI](https://www.seic.com/about-sei/newsroom/sei-launches-sei-charitable-fund-bringing-charitable-giving-advisor-and-client-wealth-experience)) | OK |
| E135 OneAscent → OneGive | ADV 2026-08-11 ([OneAscent ADV](https://oneascent.com/wp-content/uploads/sites/25/2025/11/20260811-OAWM-ADV-Part-2A.pdf)) | OK |
| E125 Foundation Source → Charityvest ([Charityvest guide](https://guide.charityvest.org/about-our-venture/charityvest-%2B-vennfi)) | "comprehensive software and administrative services … for a fee" | OK |
| E129 Foundation Source → TIAA DAF ([TIAA](https://www.tiaa.org/public/about-tiaa/news-press/press-releases/2026/09-28)) | TIAA URL returned 503; coverage says Charityvest is "operating on Foundation Source's infrastructure" | **Qualified**: sponsor-level statement, not program-level |
| E082 Ren → BofA CGF ([portal](https://bofa.donorfirst.org/)) | "DFX powered by Ren"; charitablegiftfund@reninc.com | OK |

**Status error rate: 0/15 (0%; small-sample 95% CI about 0–22%)** (sample: `data/mission-2026-11-14/relationship-graph-edges.csv`).
- Type or qualification issues: 2/15 (13%) (`data/mission-2026-11-14/relationship-graph-edges.csv`).
- One upgrade-direction error was found outside the sample (E086; [AEF, 2025-07-23](https://www.aefonline.org/?p=14296)).

---

## 5. Overconfidence flags

1. **Graph doc §5.1.** "±2 pp (CR) and ±100 (HHI)". The actual error is 12 pp and 460 points (`data/mission-2026-11-14/derived-metrics.csv`; [DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)). The stated band was not justified.
2. **Incentives §9.** "Asset-based fee alignment … Structural, Medium-High". The effect is unsupported and contrary in the cross-section ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)); lower it to Medium for existence and Low for effect.
3. **incentive-map, Treasury/IRS row.** "documented; High" with effect "discourages". That the rule is unfinished is documented ([Federal Register API](https://www.federalregister.gov/api/v1/documents.json?conditions[term]=%22donor-advised%22+4966)). That this discourages modernization is inference, so lower it to suggestive, Low-Medium.
4. **incentive-map, Vanguard row.** "structural constraint" on the basis of "fees track assets". The affiliate fee is a fixed-scale $4m ([Vanguard Charitable FY2025 statements](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf)), so mark it mixed, Medium.
5. **Incentives §1.4.** "neither faces a forcing incentive". Fidelity is transitioning to EFT ([Fidelity nonprofit FAQ](https://www.fidelitycharitable.org/nonprofits/faqs.html)).
6. **Graph §1.6.** "That leaves at most about 34%". The correct figure is 47.8% ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)).
7. **Datasets §2.4.** Fidelity and DAFgiving360 fee pages are described as "fetched fresh". Both returned 403 to me ([Fidelity fees](https://www.fidelitycharitable.org/giving-account/what-it-costs.html); [DAFgiving360 fees](https://www.dafgiving360.org/features/fees-and-minimums)), so mark them as search-snippet or PDF-sourced unless a capture exists.

---

## 6. Recommended corrections (exact wording)

**`vendor-dependency-concentration.md`**
- **§1 item 4.** Replace "Together they hold about **49%**" with: "Together they held about **39%** of DAFRC's FY2024 sponsor assets (period-aligned: June-2024 values for June-FYE sponsors)." ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx))
- **§1 item 5.** Replace it with: "**Sponsor assets are unconcentrated at the all-sponsor level and moderately concentrated among national sponsors.** DAFRC FY2024 census: CR3 45.5%, CR5 55.8%, HHI 830; national-only CR3 63.2%, HHI 1,566 (see `derived-metrics.csv`)."
- **§1 item 6 and §5.2.**
  - Replace "about 66%. That leaves at most about 34%" with "about 52%. That leaves at most about 48%". ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx))
  - Replace '"$200bn" (Apr 2026) of US DAF assets' with '"approximately $200 billion of donor-advised funds and other charitable assets" (AEF/Ren release, 2026-04-08; not a DAF-only figure)'. ([AEF/Ren release, 2026-04-08](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/))
  - Add: "The residual 47.8% plus NPT (12.9%) ≈ 60.6%, matching Ren's '60%+'; this would hold only if Ren counts NPT (Stellar/iPhi lineage) and nearly all other sponsors. Unverified." ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); [reninc.com](https://www.reninc.com/))
- **§5.1 table.**
  - Replace the June-2025 values with the DAFRC FY2024 values: Fidelity 66.20, NPT 42.12, DAFgiving360 40.94, Vanguard 21.95, GS 11.84, SVCF 9.58, AEF 9.48, MS GIFT 9.43, RCF 5.63, NCF 5.46, BofA 5.11. ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx))
  - Delete the "±2 pp/±100" line.
  - Delete the caveat "the full DAFRC sponsor file has not been downloaded".
- **§4.1.** Replace "RCF's FY2024 Schedule D shows $5.91bn across 25,824 DAFs" with "RCF's FY2024 audited net assets were $5.90bn across 25,824 DAFs (DAFRC's Schedule D row is imputed at $5.63bn / 22,366)". ([RCF FY2024 audit](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf); [DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx))
- **Edge E086.** Change `inferred` to `confirmed`. Add evidence: AEF 2025-07-23: "Ren will serve as a trusted technology and administrative services partner". Update §5.2 to read "Administration is confirmed for RCF, MS GIFT and AEF". ([AEF, 2025-07-23](https://www.aefonline.org/?p=14296))
- **Edge E151.** Note "DAFpay checkout access only". Either retype it or add `scope=donor_checkout`.
- **§4 / S7.** Change "Vanguard" to "Vanguard (hybrid: Vanguard Group provides recordkeeping/admin support for $4.0m; admin fee funds Vanguard Charitable's own operations)". ([Vanguard Charitable FY2025 statements](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf))

**`quantitative-datasets-and-data-dictionary.md`**
- **§4 / §6, NPT.** Replace "NPT's FY2025 grants conflict between $6.44b and $6.61b" with "NPT FY2025 grants: $6.44b for the U.S. DAF program only (annual report); $6.61b in the Dec-2025 release likely includes NPT UK/Transatlantic (inferred). Use $6.44b." ([NPT annual report](https://www.nptrust.org/annual-reports/npt-annual-report/); [NonProfit Times](https://thenonprofittimes.com/?p=215695))
- **§3.** Add: "Never divide June-2025 sponsor values by the DAFRC FY2024 total; DAFRC FY2024 = period ending June 2024 for June-FYE sponsors (verified against the Fidelity and Vanguard audits)." ([Fidelity FY2025 audit](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf); [Vanguard Charitable FY2025 statements](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf))

**`industry-incentives-structural-analysis.md`**
- **§1.3 and §3.4 Status.** Replace it with: "No final rule in the Federal Register as of 2026-11-14 (only the NPRM 2023-11-14, the comment extension to Feb 15, 2024, and the 2024 hearing notices). The 2026–2027 PGP (released 2026-09-29) lists 'Guidance under §§4966 and 6033 regarding certain donor advised fund arrangements', replacing the prior 'final regulations' item." Also change "Comments were due January 16, 2024" to "February 15, 2024 (extended)". ([Federal Register 2023-24982](https://www.govinfo.gov/content/pkg/FR-2023-11-14/html/2023-24982.htm); [FR 2024-00260](https://www.federalregister.gov/d/2024-00260); [IRS 2026–2027 PGP](https://www.irs.gov/pub/irs-counsel/2026-2027-initial-pgp.pdf))
- **§3.4 SPLC.** Change "DAF Giving" to "DAFgiving360 (Donor Advised Charitable Giving, Inc.)". Add the indictment date, April 21, 2026, and the source [S16].
- **§6.1 Outcome A.**
  - Add: "Fidelity states it is 'transitioning grant payments to EFT' as part of a 'digital-first policy'; Chariot (Mar 2026) reports 67% of Fidelity grants by EFT and a planned move to electronic-only in July 2026 (not confirmed on Fidelity's live FAQ, which still says EFT is not required)." ([Fidelity nonprofit FAQ](https://www.fidelitycharitable.org/nonprofits/faqs.html); [Chariot, Mar 2026](https://www.givechariot.com/resources/insights/top-8-takeaways-from-fidelity-charitables-2026-giving-report))
  - Delete "neither faces a forcing incentive".
  - Change "Industry-wide check share is not observed" to "Fidelity: ~33% of grants by check in 2025 (secondary)". ([Chariot, Mar 2026](https://www.givechariot.com/resources/insights/top-8-takeaways-from-fidelity-charitables-2026-giving-report))
- **§9.**
  - Change "Asset-based fee alignment favouring retention | Structural … | Medium-High" to "Mixed (incentive documented; effect unsupported) | Medium (existence) / Low (effect)".
  - Add the DAFRC segment payout medians as counter-evidence.
  - Change "Manual review of listed public charities | Mixed, leaning habit" to "Mixed".
- **incentive-map.csv.**
  - Treasury/IRS row: change `clarity_status` to "documented (status); suggestive, Low-Medium (effect)".
  - Vanguard row: change `structural_or_habit` to `mixed`.

---

## 7. Gaps that remain

- Whether NPT GivingPoint runs on iPhi/Ren today. This is the decisive test for Ren's claim.
- Whether Fidelity's EFT-only switch actually took effect.
- Whether the SPLC holds have been lifted.
- The DAFgiving360 fee page and the Benevity help page were blocked (403).

## Validation corrections (wave 4, 2026-11-14) — governing
Source: [validation-wave4-report.md](validation-wave4-report.md). Where these conflict with the text above, these govern.

- **W4-15** (research/mission-2026-11-14/red-team-wave2b-graph-data-incentives.md line 69): replace "(about 1m checks in 2025)" → drop this, or mark it "[inference: about 33% of about 3m grants]"; the report does not state it
