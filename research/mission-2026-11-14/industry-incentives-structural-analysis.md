# Why the DAF system operates as it does: incentives, structural constraints and habits

> **Red-team status (2026-11-14):** independently reviewed in [red-team-wave2b-graph-data-incentives.md](red-team-wave2b-graph-data-incentives.md). The corrections in the final section govern where they conflict with the text.


**Research date:** 2026-11-14 | **Evidence cutoff:** sources retrieved or re-read 2026-11-11 to 2026-11-14 | **Companion data:** [`data/mission-2026-11-14/incentive-map.csv`](../../data/mission-2026-11-14/incentive-map.csv)

**Framework basis.** This document applies Clarity and EDF as pinned in [`clarity-edf-application-guide.md`](clarity-edf-application-guide.md): Clarity commit `8cd4801`, EDF v0.3 commit `41fea6f`. EDF's sequence is used **only for observed outcomes** (§6). Unobserved hypotheses get Clarity treatment only: posture, admissibility and reconsideration criteria (§7).

Claims carry EDF claim states and qualitative confidence labels from Low to High. These labels are not probabilities. A directly documented fact, such as a statute, an audited note or a published fee schedule, is labelled **documented** and bounded to its source, entity and date. It is not given an unbounded "supported" label.

**Scope.** This is a public-source analysis. It is not legal advice, an allegation of misconduct, or an estimate of any company's profits. It reuses prior repo evidence, which is cited by file. New sources are listed in §10.

---

## 1. Executive summary

1. **The core revenue model rewards assets that stay, not grants that leave.** Sponsor administrative fees are charged as tiered basis points on balances: Fidelity, DAFgiving360 and RCF all charge 60/30/20/15 bps, and RCF's advisor-managed tier charges 65 bps [[S32](https://www.fidelitycharitable.org/giving-account/what-it-costs.html),[S33](https://www.dafgiving360.org/features/fees-and-minimums); repo `daf-economics-and-distribution-2026-11-11.md`].
   - At Fidelity Charitable, the trustees pay FMR affiliates an amount equal to the administrative fee charged to donors, net of tier credits [[S30](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf)].
   - At RCF, 98% of a specified fundholder-fee base goes to Ren: $19,225,546 in FY2024 [[S34](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf)].
   - At Vanguard Charitable, 35 of 37 investment pools are Vanguard funds [[S31](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf)].
   - **Inference (suggestive, Medium):** every party that is paid on assets is better off when balances grow than when they are granted out. That tilts incentives toward accumulation and away from technology that speeds grant-out.
   - **Counterweight:** sponsor inactivity policies and an aggregate payout rate of about 25% ([S21](https://www.dafresearchcollaborative.org/research/annual-daf-report); [DAFRC updated memo](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf)) blunt this tilt, so it is a tilt, not a proven outcome (§3.2).
2. **Sponsor liability is real but narrower than operations suggest.**
   - §4966 taxes the sponsor 20% of a taxable distribution and §4967 taxes a donor 125% of a prohibited benefit [[S04](https://www.law.cornell.edu/uscode/text/26/4966),[S05](https://www.law.cornell.edu/uscode/text/26/4967)].
   - Grants to §170(b)(1)(A) public charities are excepted from §4966 [[S04](https://www.law.cornell.edu/uscode/text/26/4966)], and grantors can rely on IRS TEOS/BMF status listings under Rev. Proc. 2018-32 [[S07](https://www.thetaxadviser.com/issues/2018/aug/irs-updates-charitable-contribution-procedures/)].
   - **Inference:** blanket manual review of well-known, currently listed public charities is mostly *mixed*, leaning habit, rather than legally compelled. Review of edge cases (foreign grantees, benefit risk, Type III supporting organizations) is structural. Confidence: Medium.
3. **Regulatory uncertainty is a structural brake on redesign.**
   - The November 2023 proposed §4966 regulations, REG-142338-07, were **still not final** as of the latest sources I found: Council on Foundations, May 8, 2026, and PG Calc, June 15, 2026 [[S02](https://cof.org/page/proposed-rule-taxes-taxable-distributions-donor-advised-funds-under-section-4966),[S03](https://blog.pgcalc.com/the-state-of-play-navigating-the-current-landscape-of-qcd-legislation-and-daf-regulations)]. I found no final rule published by 2026-11-14. That absence is a gap in the evidence, not a confirmed fact; a Federal Register check is still required.
   - The proposal would treat a donor's personal investment advisor who manages DAF assets as a donor-advisor, which brings §4958 into play [[S01](https://www.govinfo.gov/content/pkg/FR-2023-11-14/html/2023-24982.htm)]. That puts an unresolved liability question over the advisor-managed DAF channel.
4. **Paper checks persist because the decision sits with both parties, and neither faces a forcing incentive. No law requires checks.**
   - Fidelity Charitable "does not currently require EFT," says EFT is "up to 9x faster," and asks nonprofits whose board policy prohibits EFT to update it [[S26](https://www.fidelitycharitable.org/nonprofits/faqs.html)].
   - EDF classification: **mixed**, with organizational and informational origins dominating. Confidence: Medium (§6.1).
5. **Who resists redesign.**
   - Likely resisters are holders of asset-based fee streams: affiliated managers, platform administrators on AUM-linked fee shares, and advisors earning AUM fees on DAF assets. Some sponsors also prize discretion that a standardized rail or data-sharing regime would constrain.
   - Likely beneficiaries are working charities, small donors, and challenger platforms not paid on AUM.
   - This is an **incentive analysis, not a finding of intent** (Clarity: "incentives over intent").
   - Defenders' evidence is real and is presented here: payout rates, universal inactivity policies at large nationals, and donor flexibility [[S21](https://www.dafresearchcollaborative.org/research/annual-daf-report),[S24](https://www.philanthropyroundtable.org/resource/donor-advised-funds-payout-trends-inactivity-policies-and-accessibility/)].

---

## 2. Method and the structural-vs-habit test

The mission guide gives the test for each persistent behaviour:
- **Structural constraint:** an EDF origin network shows it is held in place by a regulatory, legal-liability or financial origin whose control point the actor cannot change on its own.
- **Historical habit:** the only sustaining origins are organizational or informational, and a feasible control point lies within the actor's own authority.
- **Mixed:** both kinds of origin interact. This is the default.

**Clarity admissibility screen applied.** I rejected these candidate claims:
- "Sponsors deliberately slow grants." This substitutes motivation for incentives.
- "DAFs warehouse wealth." This is unbounded. The evidence is aggregate, and account-level inactivity is about 22% in a voluntary historical sample [[S22](https://johnsoncenter.org/wp-content/uploads/2024/02/DAFRC_Executive_Summary_Key_Findings.pdf)].
- Any point estimate of "fees lost to delay." No denominator exists.

---

## 3. Incentive analysis by domain

### 3.1 Fee incentives: asset-based administration and affiliated investment expense

**Documented facts:**
- **Fidelity Charitable** individual Giving Account: 0.60% on the first $500k, then 0.30%, 0.20% and 0.15%, with a $100 minimum and investment expenses on top [[S32](https://www.fidelitycharitable.org/giving-account/what-it-costs.html); repo fee model].
- **DAFgiving360:** the same first four tiers. Its professionally managed accounts require $100k, and the external advisor fee is capped at 1% [[S33](https://www.dafgiving360.org/features/fees-and-minimums)].
- **RCF:** advisor-managed 65/35/25/20 bps, with a $250 minimum [repo `daf-economics-and-distribution-2026-11-11.md`, E03–E05].
- **Fidelity Charitable FY2025 audit, Note 7.** The trustees contracted with FMR LLC and affiliates. The Gift Fund paid FMR "amounts equal to the administrative fee the Gift Fund charged donors, net of tier price credits." FY2025 administrative fee expense was $179,875,837, and investment-management fee expense was $84,317,489 [[S30](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf)].
- **Vanguard Charitable FY2025.** It paid Vanguard $4,014,052 in related-party service fees, and 35 of 37 pools hold Vanguard mutual funds or ETFs [[S31](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf)].
- **RCF FY2024 audit.** It paid Ren $19,225,546 under a 98%-of-specified-fundholder-fee formula, and Ren personnel overlap with RCF's board [[S34](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf); repo `data/rcf-ren-audited-admin-payments-2020-2024.csv`].

**Inference:**
- An administrator or affiliate paid as a share of balance-based fees earns more when assets grow, through contributions and investment returns, and less when grants leave.
- That does not prove anyone slows grants. Sponsors also earn on contribution inflows, which better grant tools may encourage, and audited payout is about 25% [[S21](https://www.dafresearchcollaborative.org/research/annual-daf-report)].
- **Claim state:** *suggestive*. **Confidence:** Medium that the incentive exists, Low that it causes any measured delay.

**Effect on modernization:**
- AUM-linked pricing discourages one kind of modernization: tools whose main value is speeding grant-out or lowering balances.
- It is neutral or positive for tools that bring in contributions, such as complex-asset intake and advisor integrations. Those are what the market has invested in, as Ren and TIFIN's asset-retention marketing shows [repo [R08](https://www.reninc.com/wealth-management-firms/), [R17](https://tifin.com/product/give/)].

### 3.2 Asset retention: no fund-level payout rule; sponsor-level payout and inactivity policies

**Documented facts:**
- **No statutory DAF payout requirement.**
  - Madoff, January 8, 2026: "there are no payout rules that apply to donor-advised funds" [[S19](https://www.philanthropy.com/opinion/a-tax-scholar-suggests-policy-fixes-for-charitable-giving/)].
  - IPS, November 15, 2023, calls for a payout requirement and for account-by-account reporting [[S17](https://www.ips-dc.org/release-new-report-from-the-institute-for-policy-studies-reveals-the-true-cost-of-billionaire-philanthropy/)].
- **DAFRC FY2024, revised Spring 2026** ([DAFRC updated analysis, Apr 2026](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf)):
  - 1,512 sponsors and 3.59m accounts ([DAFRC](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf)).
  - $90.57bn contributions, $64.60bn grants and $327.87bn assets ([DAFRC](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis.pdf)).
  - **Aggregate payout rate 25.2%** [[S21](https://www.dafresearchcollaborative.org/research/annual-daf-report)].
- **DAFRC national study (2014–2022, 111 voluntary sponsor programs).** About 22% of accounts made no grant in the latest three-year window. The median account-level three-year payout was 9%, or 15% for active accounts [[S22](https://johnsoncenter.org/wp-content/uploads/2024/02/DAFRC_Executive_Summary_Key_Findings.pdf); repo].
- **Fidelity's current inactivity rule.** A grant is required at least every two years. After two years with no grant, Fidelity grants 5% of the balance to a trustee-approved charity [[S25](https://fidelitycharitable.org/faqs/all/how-often-do-i-grant.html)].
- **Philanthropy Roundtable report (Jack Salmon).** It reports that 100% of the national sponsors analysed, covering 89% of accounts, enforce "stringent and well-defined inactivity policies" [[S24](https://www.philanthropyroundtable.org/resource/donor-advised-funds-payout-trends-inactivity-policies-and-accessibility/)]. I read only the summary; the full text returned HTTP 403.

**Where evidence is contested:**
- **Payout benchmarks.**
  - IPS (Collins & Flannery, March 24, 2022) rejects comparisons with the 5% foundation payout: "DAFs were never intended to hold funds in perpetuity". It notes that a 20% payout leaves 80% held [[S18](https://inequality.org/article/independent-research-donor-advised-funds/)].
  - Defenders cite the 20–25% aggregate rate [[S21](https://www.dafresearchcollaborative.org/research/annual-daf-report),[S24](https://www.philanthropyroundtable.org/resource/donor-advised-funds-payout-trends-inactivity-policies-and-accessibility/)].
  - Both are aggregate, asset-weighted figures. Neither shows the distribution across accounts. The DAFRC account-level median of 9% sits between the two camps [[S22](https://johnsoncenter.org/wp-content/uploads/2024/02/DAFRC_Executive_Summary_Key_Findings.pdf)].
- **DAF-to-DAF flows.** IPS reports $2.5bn of national-DAF-to-national-DAF grants in 2021 [[S17](https://www.ips-dc.org/release-new-report-from-the-institute-for-policy-studies-reveals-the-true-cost-of-billionaire-philanthropy/)]. Such grants are expressly non-taxable under §4966(c)(2) [[S04](https://www.law.cornell.edu/uscode/text/26/4966)] and inflate measured payout. How much they inflate it is **unknown**.
- **Who funds the research.** Search summaries of the Roundtable's material say a related DAFRC study was supported by the Roundtable [[S24](https://www.philanthropyroundtable.org/resource/donor-advised-funds-payout-trends-inactivity-policies-and-accessibility/)]. I could not verify this on the DAFRC page, which does not state its funders [[S21](https://www.dafresearchcollaborative.org/research/annual-daf-report)]. Treat sponsor- and advocate-funded research on both sides as interested.

**Effect on modernization:**
- Inactivity enforcement is a *sponsor-chosen* control. That makes it modernizable: automated nudges and default-grant workflows are within sponsor authority.
- The absence of a legal payout rule removes any external forcing function for grant-out tooling.

### 3.3 Advisor compensation: AUM fees on charitable assets

**Documented facts:**
- **Open-architecture advisor programs.** Fidelity CIAP, DAFgiving360 PMA (≤1% advisor fee, $100k minimum), NPT (adviser-managed accounts from $500k discretionary or $2m nondiscretionary) and AEF all let an external advisor charge fees on sponsor-owned assets [repo `batch-1a`; [S33](https://www.dafgiving360.org/features/fees-and-minimums)].
- **OneAscent's August 11, 2026 ADV** discloses a waivable 55 bps adviser fee on OneGive/Charityvest DAF assets. It also discloses an affiliate's indirect minority interest in the Foundation Source ownership chain [[S42](https://oneascent.com/wp-content/uploads/sites/25/2025/11/20260811-OAWM-ADV-Part-2A.pdf); repo `oneascent-onegive-charityvest-disclosed-incentives-2026-11-11.md`].
- **TIFIN Give's 2025 ADV** discloses that sponsorship payments from model providers create an incentive to recommend those portfolios [[S37](https://tifin.com/wp-content/uploads/TIFIN-Give-Part-2A-of-Form-ADV-Brochure-2025.pdf)].
- **Broker-affiliated channels.**
  - MS GIFT names RenPSG as back-office administrator and Morgan Stanley Smith Barney as investment manager [repo `bofa-morgan-stanley-institutional-ren-evidence-2026-11-11.md`].
  - An Edward Jones page surfaced by search describes its Charitable Gift Fund as offered "in conjunction with" Renaissance Charitable Foundation [[S43](https://www.edwardjones.com/us-en/investment-services/investment-products/donor-advised-funds)]. This is a search snippet only; the page text could not be retrieved on 2026-11-14, so treat it as unverified.
  - **Not found:** a public statement of how Edward Jones or Morgan Stanley advisors are paid on DAF assets. This is an open question, not an inference.
- **FINRA/SEC.** Reg BI imposes disclosure, care and conflict obligations on broker-dealer recommendations of securities to retail customers [[S46](https://www.finra.org/rules-guidance/key-topics/regulation-best-interest)].
  - I found **no DAF-specific FINRA or SEC rule or enforcement action**.
  - It is **unresolved in my sources** whether recommending a DAF contribution is a securities recommendation, or whether the Advisers Act fiduciary duty governs instead. This is a legal question for counsel.

**Inference:** advisor AUM compensation turns DAF recommendation into partly a retention decision.
- The repo's household model shows that an RIA loses 25% of fee revenue on a $500k gift without a sponsor mandate, and is fee-neutral with a 0.75% mandate [repo `research/batch-1a-relationship-retention-fee-waterfall-2026-11-12.md`] (source: repo inference — no primary URL).
- This **accelerates** DAF adoption through advisor channels, and modernization of advisor-facing tools.
- It **discourages** donor-direct or grant-accelerating designs that shrink managed balances.
- **Claim state:** *suggestive*. **Confidence:** Medium-High that the incentive exists; Low on its magnitude across the market.

### 3.4 Sponsor liability: §§4966, 4967, 4958 and the unfinished 2023 proposed regulations

**Documented facts:**
- **§4966 (taxable distributions):**
  - 20% tax on the sponsor; 5% on a knowing fund manager, capped at $10,000 per distribution.
  - A taxable distribution is a payment to a natural person, a payment for a non-§170(c)(2)(B) purpose, or a payment made without expenditure responsibility.
  - Excepted: distributions to §170(b)(1)(A) organizations other than disqualified supporting organizations, to the sponsor itself, or to another DAF [[S04](https://www.law.cornell.edu/uscode/text/26/4966)].
- **§4967 (prohibited benefits):** 125% of a "more than incidental" benefit, on the donor or advisor; 10% on a knowing manager, capped at $10,000 [[S05](https://www.law.cornell.edu/uscode/text/26/4967)].
- **IRS:** the sponsor has legal control, and the IRS may impose §4966 and §4958 taxes or revoke exemption [[S06](https://www.irs.gov/charities-non-profits/charitable-organizations/donor-advised-funds)].
- **Proposed regulations (Federal Register, November 14, 2023; REG-142338-07) [[S01](https://www.govinfo.gov/content/pkg/FR-2023-11-14/html/2023-24982.htm)]:**
  - A personal investment advisor managing DAF assets "would be a donor-advisor … while serving in that dual capacity," subject to §4958(c)(2).
  - "Reasonable investment and grant-related fees paid from DAF assets generally would not be considered distributions."
  - Comments were due January 16, 2024 ([Federal Register NPRM 2023-24982](https://www.govinfo.gov/content/pkg/FR-2023-11-14/html/2023-24982.htm)).
  - The preamble counted 1,624 self-identified sponsors.
- **Status:** not finalized as of May 8, 2026 [[S02](https://cof.org/page/proposed-rule-taxes-taxable-distributions-donor-advised-funds-under-section-4966)] and June 15, 2026 [[S03](https://blog.pgcalc.com/the-state-of-play-navigating-the-current-landscape-of-qcd-legislation-and-daf-regulations)]. The 2026–2027 Priority Guidance Plan lists "§§4966 and 6033 … donor advised fund arrangements" [[S02](https://cof.org/page/proposed-rule-taxes-taxable-distributions-donor-advised-funds-under-section-4966),[S03](https://blog.pgcalc.com/the-state-of-play-navigating-the-current-landscape-of-qcd-legislation-and-daf-regulations)]. ([IRS 2026–2027 PGP](https://www.irs.gov/pub/irs-counsel/2026-2027-initial-pgp.pdf)) <!-- CITE-CHECK: S02 (2026-05-08) and S03 (2026-06-15) predate the 2026-09-29 PGP release, so they cannot support the PGP wording; primary IRS PGP link added (see red-team wave 2B F5). -->
- **Reliance:** Rev. Proc. 2018-32 lets grantors rely on TEOS/BMF public-charity status listings, subject to knowledge exceptions [[S07](https://www.thetaxadviser.com/issues/2018/aug/irs-updates-charitable-contribution-procedures/)]. I read secondary summaries; the primary IRB text is not yet read.

**Inference:**
- For a grant to a currently listed public charity, statutory exposure is narrow.
- Real risk sits in edge cases: grants to individuals, foreign grantees, disqualified supporting organizations, tickets or pledges that create §4967 benefits, and political or reputational events.
- **2026 example (documented fact).** After the DOJ indicted the Southern Poverty Law Center (SPLC), a public charity, in April 2026, Fidelity Charitable, Vanguard Charitable and DAF Giving (Donor Advised Charitable Giving, Inc.) restricted or halted payments. Sixteen attorneys general asked them on May 22, 2026 to weigh donor intent [[S16](https://oag.ca.gov/node/623769)].
  - This shows that sponsor discretion reaches beyond the §4966 statutory floor and is exercised for reasons beyond tax exposure.
  - Liability aversion is therefore partly **reputational and discretionary**, not purely statutory.
- **Claim state:** *suggestive*. **Confidence:** Medium.

### 3.5 Regulatory uncertainty: federal bills, OBBBA, states

**Documented facts:**
- **ACE Act (King–Grassley).** It proposed 15-year payout conditions for standard DAFs and stalled for lack of consensus [[S03](https://blog.pgcalc.com/the-state-of-play-navigating-the-current-landscape-of-qcd-legislation-and-daf-regulations),[S11](https://www.steptoe.com/en/news-publications/senators-king-and-grassley-introduce-daf-and-private-foundation-reform-legislation.html)]. PG Calc (June 2026) judges major standalone charitable legislation unlikely this Congress [[S03](https://blog.pgcalc.com/the-state-of-play-navigating-the-current-landscape-of-qcd-legislation-and-daf-regulations)].
- **Charity Parity Act (H.R. 8783 / S. 4511, May 2026).** It would extend QCDs to 401(k)/403(b)/457(b) plans and keep DAFs excluded as recipients [[S03](https://blog.pgcalc.com/the-state-of-play-navigating-the-current-landscape-of-qcd-legislation-and-daf-regulations),[S13](https://www.coons.senate.gov/?p=23646)].
- **S. 3975 (Sen. Young), introduced March 3, 2026.** It would allow QCDs to DAFs and is the Senate companion to H.R. 891 [[S12](https://riponadvance.com/stories/young-introduces-bill-to-expand-charitable-giving-options-for-older-americans/)]. Critics frame it as enabling warehousing.
  - **Inference:** a QCD-to-DAF pathway would expand inflows and strengthen asset-based incentives.
- **OBBBA, effective for 2026 [[S08](https://www.irs.gov/newsroom/irs-reminder-permanent-charitable-contribution-deduction-begins-for-returns-filed-next-year-for-taxpayers-who-do-not-itemize),[S09](https://www.grantthornton.com/insights/alerts/tax/2025/legislative-updates/2026-individual-tax-planning-guide),[S10](https://tax.thomsonreuters.com/news/charitable-deduction-unpacked-individual-itemizers/)]:**
  - 0.5%-of-AGI floor for itemizers ([S10](https://tax.thomsonreuters.com/news/charitable-deduction-unpacked-individual-itemizers/); [P.L. 119-21, H.R. 1](https://www.congress.gov/bill/119th-congress/house-bill/1)).
  - Value cap of 35% at the top bracket ([S09](https://www.grantthornton.com/insights/alerts/tax/2025/legislative-updates/2026-individual-tax-planning-guide); [S10](https://tax.thomsonreuters.com/news/charitable-deduction-unpacked-individual-itemizers/)).
  - Permanent nonitemizer deduction of $1,000 single or $2,000 MFJ for cash gifts, **excluding DAF contributions**. The IRS confirmed this on November 10, 2026 [[S08](https://www.irs.gov/newsroom/irs-reminder-permanent-charitable-contribution-deduction-begins-for-returns-filed-next-year-for-taxpayers-who-do-not-itemize)].
  - **Inference:**
    - DAFs become relatively less attractive to small standard-deduction donors.
    - DAFs become relatively more useful for bunching, to clear the floor.
    - This pushes the market toward larger, advisor-led accounts, which is the segment where asset-based incentives are strongest.
- **California:**
  - AB 1712 (Wicks, 2019–20) would have required account-level DAF reporting. It was pulled in January 2020 amid privacy and cost objections [[S15](https://ministrywatch.com/california-would-be-first-state-law-to-reach-donor-advised-funds/)].
  - AB 2221 (Irwin) was chaptered on September 27, 2026 as Ch. 590, Stats. 2026 [[S14](https://www.govbuddy.com/california/bills/ab-2221/)]. As summarized, it updates charitable fundraising-platform rules and **keeps the DAF-sponsor exclusion**. I found no DAF-specific mandate in it, but the summary was secondary and the official text is unverified.
  - Philanthropy Roundtable's post "A DAF Storm is Brewing in California Again" (undated in my capture; HTTP 403) reportedly says Madoff and Wicks are pushing new rules [search summary only, S24b]. Status: **unknown**.

**Effect on modernization:**
- Unfinished federal rules discourage investment in automated grant-decisioning and advisor-fee designs, because the definitions of "distribution" and "donor-advisor" could change. This is **structural**: no sponsor can finalize Treasury rules.
- **Posture:** Guardrail, meaning high impact but correctable once rules are final.

### 3.6 Customer switching costs

**Documented facts:**
- **DAF-to-DAF transfers** are excepted from §4966 [[S04](https://www.law.cornell.edu/uscode/text/26/4966)]. They require the releasing sponsor's approval of a closing grant [repo [R02](https://www.fidelitycharitable.org/faqs/all/transfer-to-giving-account.html), [R03](https://renaissancecharitable.org/how-to-open-a-renaissance-charitable-daf/)].
- **WaterStone litigation (InvestmentNews, February 27, 2026).** A successor advisor alleges that the sponsor stopped honoring grant recommendations and cut off information on a roughly $21m fund after a transfer was raised. Counsel responded: "The plaintiff in this case is not the donor" [[S20](https://www.investmentnews.com/practice-management/multimillion-dollar-donor-advised-fund-lawsuit-puts-spotlight-on-control-risks/265478)]. These are allegations, not findings.
- **Institutional switching (AEF to Ren).** AEF's DonorCentral was retired on October 31, 2026, and the new portal shows only two years of history [repo [R06](https://engage.aefonline.org/dc-sunset/)].
- **Contract terms:**
  - Ren's published MSA template has one-year auto-renewals unless notice is given 60 days before, plus quarter-end termination charges [[S35](https://www.reninc.com/wp-content/uploads/2025/08/Online-RAC-MSA_v1.pdf)].
  - TIFIN's group terms default to auto-renewal [[S36](https://tifin.com/terms-conditions/)].

**Inference:**
- Donor switching friction is **structural at the legal layer**: the sponsor owns the assets and has discretion.
- It is **mixed at the operational layer**: closing-grant paperwork and history loss are within sponsor control.
- Low donor switching weakens competitive pressure on fees and modernization.
- **Claim state:** *suggestive*. **Confidence:** Medium.

### 3.7 Organizational silos, procurement and legacy contracts

**Documented facts:**
- Related-party procurement is common among large sponsors:
  - Fidelity Charitable uses FMR affiliates [[S30](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf)].
  - Vanguard Charitable uses Vanguard [[S31](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf)].
  - RCF uses Ren, with board overlap [[S34](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf)].
  - Charityvest's board includes a Foundation Source executive [repo [G01](https://guide.charityvest.org/governance-and-legal/overview), [G20](https://finance.yahoo.com/small-business/articles/charityvest-appoints-matt-nash-james-120000597.html)].
- Charityvest's conflicts policy requires recusal [repo [G02](https://www.charityvest.org/documents/Charityvest%20Conflict%20of%20Interest%20Policy.pdf)]. Whether it was applied in practice is **not observed**.

**Inference:**
- When the vendor is an affiliate whose fees track sponsor fees, competitive procurement of a cheaper or faster administrator has a counter-incentive inside the corporate family.
- **This is not evidence of bad decisions.** Integration can also lower cost: Vanguard Charitable's management and general expense was $8.59m on $27.2bn of net assets [[S31](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf)].
- **Classification:** structural where the affiliate relationship is written into the trustee contract, as at Fidelity; habit where renewal is passive under an auto-renew clause.
- **Confidence:** Low-Medium. No signed renewal decisions have been observed.

### 3.8 Vendor lock-in

The repo already documents several sources of lock-in:
- vendor-retained IP and only a limited licence [[S35](https://www.reninc.com/wp-content/uploads/2025/08/Online-RAC-MSA_v1.pdf), M08];
- no guaranteed structured export [M07];
- AEF's two-year history cutoff [repo [R06](https://engage.aefonline.org/dc-sunset/)];
- loss of Chariot access on termination [repo [R22](https://www.givechariot.com/legal-nonprofit)].

**Inference:** lock-in lengthens contract life and slows adoption of better tools. **Mixed.** Its origins are financial (termination fees) and informational (no schema standard). **Confidence:** Medium.

### 3.9 Donor expectations: anonymity, receipts, year-end

**Documented facts (Fidelity Charitable):**
- About 4% of grants are anonymous, and nonprofits then receive no donor identity [[S26](https://www.fidelitycharitable.org/nonprofits/faqs.html)].
- Nonprofits "should not send the donor a tax receipt" for DAF grants [[S26](https://www.fidelitycharitable.org/nonprofits/faqs.html)].
- Grant recommendations "may take 10 or more business days," and "longer than normal" during peaks [[S27](https://www.fidelitycharitable.org/faqs/all/grant-processing-timeline.html)].
- 2025 contribution cutoffs ran from November 10 (outside mutual funds) to December 31 (web) [[S28](https://www.fidelitycharitable.org/giving-account/what-you-can-donate/charitable-year-end-tax-deadlines.html)].
- In calendar 2025: 3 million grant recommendations, $18.3bn granted, over 395,000 donors [[S29](https://www.fidelitycharitable.org/insights/2026-giving-report.html)].

**Inference:**
- The tax receipt is issued at *contribution*, so the donor's tax-timing need is met before any grant moves. Year-end pressure therefore falls on contribution intake, which is asset-accretive, rather than on grant speed.
- The year-end crunch is **structural**: the tax year is fixed by law. How it is handled, through manual intake or paper postmarks, is **habit**.
- **Confidence:** Medium.

### 3.10 Nonprofit bargaining power

**Documented facts:**
- Donor identity reaches the nonprofit only if the donor chooses [[S26](https://www.fidelitycharitable.org/nonprofits/faqs.html)].
- Chariot's 2026 nonprofit terms set a DAFpay default of 2.9% unless another contract applies [repo [R13](https://www.givechariot.com/legal-nonprofit)].
- DAF Direct, a sponsor-backed widget, was offered free. The Chronicle reported in 2015 that adoption had stalled [[S45](https://www.philanthropy.com/news/effort-to-spur-giving-from-donor-advised-funds-online-appears-to-stall/)]. Its current status is unverified.

**Inference:**
- Nonprofits are price-takers. They cannot choose the sponsor, the rail or the data fields, and their only levers are enrolling in EFT and integrating a widget.
- Because nonprofits do not pay sponsors, sponsor revenue does not depend on nonprofit satisfaction. Their weak leverage is **structural**, rooted in the legal and financial relationship.
- **Confidence:** Medium-High.

---

## 4. Where incentives discourage modernization even when better technology exists

| Better technology exists (evidence) | Incentive that discourages adoption | Classification | Confidence |
|---|---|---|---|
| EFT/Stripe 1–2 days versus checks; "up to 9x faster" [[S26](https://www.fidelitycharitable.org/nonprofits/faqs.html)] | No sponsor mandate; nonprofit board policies; no penalty for checks | Mixed, leaning habit | Medium |
| Automated status checks against TEOS/BMF are legally reliable [[S07](https://www.thetaxadviser.com/issues/2018/aug/irs-updates-charitable-contribution-procedures/)] | Liability and reputational aversion (SPLC precedent [[S16](https://oag.ca.gov/node/623769)]); unfinished regulations [[S02](https://cof.org/page/proposed-rule-taxes-taxable-distributions-donor-advised-funds-under-section-4966)] | Mixed | Medium |
| Faster grant-out and default-grant automation | AUM-linked fees to affiliates and administrators [[S30](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf),[S34](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf)] | Structural (financial) | Low-Medium on effect |
| Standard exports and portable history | Vendor IP, termination charges, no schema standard [[S35](https://www.reninc.com/wp-content/uploads/2025/08/Online-RAC-MSA_v1.pdf), [R06](https://engage.aefonline.org/dc-sunset/)] | Mixed | Medium |
| Shared donor data for nonprofits (opt-in) | Anonymity expectations; sponsor ownership of the relationship; past privacy objections (AB 1712 [[S15](https://ministrywatch.com/california-would-be-first-state-law-to-reach-donor-advised-funds/)]) | Mixed | Medium |
| Donor-direct low-fee DAFs (DAFgiving360 and Fidelity at the $100 minimum) | Advisor AUM retention favours advisor-managed accounts [repo batch-1a; [S42](https://oneascent.com/wp-content/uploads/sites/25/2025/11/20260811-OAWM-ADV-Part-2A.pdf)] | Structural (financial) | Medium |

---

## 5. Stakeholders: who benefits from a redesigned system and who resists

"Redesign" here means faster default grant-out, electronic rails, interoperable data, and transparent all-in fees. These are *incentive positions*, not observed lobbying. Clarity's operational test asks whether the idea can survive incentives, time and pressure.

| Stakeholder | Likely position | Basis |
|---|---|---|
| Working nonprofits | **Benefit** | Faster cash; donor data where consented; lower processing fees [[S26](https://www.fidelitycharitable.org/nonprofits/faqs.html), [R13](https://www.givechariot.com/legal-nonprofit)] |
| Small and standard-deduction donors | **Benefit** (weakly engaged) | Lower minimums; OBBBA already tilts them toward direct giving [[S08](https://www.irs.gov/newsroom/irs-reminder-permanent-charitable-contribution-deduction-begins-for-returns-filed-next-year-for-taxpayers-who-do-not-itemize)] |
| Challenger platforms not paid on AUM (Chariot, Daffy-type) | **Benefit** | Earn on transactions or subscriptions [R13; repo challenger economics] |
| Affiliated managers (FMR, Vanguard and others) | **Resist** shrinking balances; neutral on speed | Fees track assets [[S30](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf),[S31](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf)] |
| Fee-share administrators (Ren under the RCF formula) | **Resist** balance reduction; **accelerate** intake technology | 98% fee-base share [[S34](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf)] |
| Advisors on DAF AUM | **Resist** grant acceleration and portability that moves assets away | 55 bps and up to 1% fees [[S42](https://oneascent.com/wp-content/uploads/sites/25/2025/11/20260811-OAWM-ADV-Part-2A.pdf),[S33](https://www.dafgiving360.org/features/fees-and-minimums)] |
| Sponsors (discretion-heavy) | **Mixed** | Value discretion (SPLC, WaterStone [[S16](https://oag.ca.gov/node/623769),[S20](https://www.investmentnews.com/practice-management/multimillion-dollar-donor-advised-fund-lawsuit-puts-spotlight-on-control-risks/265478)]); also benefit from efficiency |
| Community foundations | **Mixed** | Opposed account-level reporting [[S15](https://ministrywatch.com/california-would-be-first-state-law-to-reach-donor-advised-funds/)]; some lack the scale to modernize |
| Regulators / Treasury | Neutral or slow | Regulations unfinished [[S02](https://cof.org/page/proposed-rule-taxes-taxable-distributions-donor-advised-funds-under-section-4966),[S03](https://blog.pgcalc.com/the-state-of-play-navigating-the-current-landscape-of-qcd-legislation-and-daf-regulations)] |
| Critics (IPS, Madoff) | Want payout and transparency rules, not necessarily technology | [[S17](https://www.ips-dc.org/release-new-report-from-the-institute-for-policy-studies-reveals-the-true-cost-of-billionaire-philanthropy/),[S18](https://inequality.org/article/independent-research-donor-advised-funds/),[S19](https://www.philanthropy.com/opinion/a-tax-scholar-suggests-policy-fixes-for-charitable-giving/)] |
| Defenders (DAFRC data users, Philanthropy Roundtable, sponsors) | Favor self-regulation; resist mandates | [[S21](https://www.dafresearchcollaborative.org/research/annual-daf-report),[S24](https://www.philanthropyroundtable.org/resource/donor-advised-funds-payout-trends-inactivity-policies-and-accessibility/)] |

---

## 6. EDF diagnoses of observed outcomes

### 6.1 Outcome A: paper checks remain an active DAF grant rail in 2026

- **System context.**
  - *Primary system:* the payment stage of DAF grants.
  - *Context:* national sponsors in 2026 ([S26](https://www.fidelitycharitable.org/nonprofits/faqs.html)).
  - *Focus:* why checks remain in use.
- **Outcome (factual).** Fidelity Charitable mails checks to nonprofits not enrolled in EFT [[S26](https://www.fidelitycharitable.org/nonprofits/faqs.html)]. DAFgiving360 states that checks are mailed in an average of 7–10 business days, plus USPS delivery [repo `batch-2a`, DAFgiving360 FAQ].
- **Manifestations:**
  - check transmittal letters;
  - void and reissue procedures that depend on the donor;
  - sponsors marketing EFT as faster [[S26](https://www.fidelitycharitable.org/nonprofits/faqs.html)].
- **Origin network:**
  - *Organizational:* nonprofit board policies prohibiting EFT, which Fidelity explicitly mentions; sponsors not requiring EFT.
  - *Informational:* unverified bank details. Moving to EFT needs onboarding, and checks go to the address on the Form 990.
  - *Financial:* EFT is free to nonprofits at Fidelity, so cost is **not** an origin there [[S26](https://www.fidelitycharitable.org/nonprofits/faqs.html)].
  - *Regulatory:* **no statutory check requirement found.**
- **Propagation:** informational (no bank details on file) → operational (default to check) → financial (float and delay) → human (nonprofit reconciliation).
- **Evidence:** direct statements from sponsor FAQs. Industry-wide check share is **not observed**.
- **Control points:**
  1. Sponsor default to EFT with an opt-out. High influence; within sponsor control.
  2. Shared verified-bank registry (Stripe, Chariot, PayPal networks). Medium influence; costs vendor fees.
  3. Nonprofit board policy updates. Low cost but diffuse control.
- **Ranking:** 1 > 2 > 3 by controllability. No numeric scores are assigned.
- **Diagnostic sufficiency:** enough to justify a sponsor-level EFT-default pilot. Not enough to size the benefit.
- **Unknowns:**
  - the check share by sponsor;
  - the cost of fraud and returns on each rail.
- **Next responsible action:** obtain check versus EFT counts from Form 990 narratives or sponsor reports.
- **Classification:** **Mixed, leaning historical habit.** Confidence: Medium.
- **Reconsider if** a bank-fraud or KYC rule is shown to require checks for unverified payees, or if sponsors report that EFT enrollment is blocked by an external constraint.

### 6.2 Outcome B: grant review takes "10 or more business days," with trustee approval of each grant, including for well-known public charities

- **System context:** Fidelity Charitable grant approval in 2026 [[S27](https://www.fidelitycharitable.org/faqs/all/grant-processing-timeline.html)].
- **Outcome:** the stated processing time is 10 or more business days, longer at peak; selecting "Where It Is Needed Most" speeds it up [[S27](https://www.fidelitycharitable.org/faqs/all/grant-processing-timeline.html)].
- **Manifestations:**
  - requests to charities and donors for more information;
  - a recommendation to file grants under $10k online [[S28](https://www.fidelitycharitable.org/giving-account/what-you-can-donate/charitable-year-end-tax-deadlines.html)].
- **Origin network:**
  - *Regulatory:* sponsor legal control and §4966/4967 exposure [[S04](https://www.law.cornell.edu/uscode/text/26/4966)–[S06](https://www.irs.gov/charities-non-profits/charitable-organizations/donor-advised-funds)].
  - *Regulatory-uncertainty:* unfinished regulations [[S02](https://cof.org/page/proposed-rule-taxes-taxable-distributions-donor-advised-funds-under-section-4966)].
  - *Reputational/discretionary:* the SPLC pattern [[S16](https://oag.ca.gov/node/623769)].
  - *Organizational:* trustee-approval design.
  - *Informational:* purpose fields that indicate benefit risk.
- **Propagation:** a restricted grant purpose triggers manual inquiry, which adds days and creates peak backlogs.
- **Evidence:**
  - Grant-purpose sensitivity is documented: an unrestricted purpose expedites the grant.
  - The share of time spent on status checks versus purpose review is **not observed**. Repo hypothesis H2, "most grants reviewed manually," is *unsupported* [repo `batch-2a`].
- **Control points:**
  1. Automated status-plus-purpose triage, with human review of exceptions only.
  2. Clear purpose taxonomies.
  3. Final regulations (outside sponsor control).
- **Diagnostic sufficiency:** sufficient for an Experimental-posture pilot. Insufficient to claim that automation is safe at scale.
- **Classification:**
  - Status verification of listed public charities: **mixed, leaning habit**. Reliance under Rev. Proc. 2018-32 is available [[S07](https://www.thetaxadviser.com/issues/2018/aug/irs-updates-charitable-contribution-procedures/)].
  - Purpose and benefit review: **structural** (§4967).
  - Confidence: Medium.
- **Reconsider if:**
  - final regulations broaden "distribution" or impose new diligence duties;
  - the IRS publishes enforcement against sponsors that relied on BMF;
  - sponsor data show that most delay is purpose-related rather than status-related.

### 6.3 Outcome C: transfers between sponsors face friction and dispute

- **Outcome:** a closing grant requires releasing-sponsor approval [R02, [R03](https://renaissancecharitable.org/how-to-open-a-renaissance-charitable-daf/)]. WaterStone is alleged to have refused or ignored a successor's requests [[S20](https://www.investmentnews.com/practice-management/multimillion-dollar-donor-advised-fund-lawsuit-puts-spotlight-on-control-risks/265478)].
- **Origins:**
  - *Regulatory/legal:* sponsor ownership and legal control [[S06](https://www.irs.gov/charities-non-profits/charitable-organizations/donor-advised-funds)].
  - *Financial:* loss of the fee base.
  - *Informational:* successor-advisor status.
- **Control points:**
  - published transfer service levels;
  - successor designations at account opening.
- **Classification:** **structural** at the legal core; **mixed** in execution.
- **Confidence:** Medium on mechanism; Low on prevalence, since it rests on one litigated case.

---

## 7. Clarity results for unobserved hypotheses (no EDF)

| Hypothesis | Admissibility | Claim state | Confidence | Posture | Reconsider if… |
|---|---|---|---|---|---|
| H1: AUM-linked fees cause slower grant processing | Passes only if bounded to incentive, not intent | unsupported | Low | Experimental | Sponsor-level data correlate fee structure with time-to-grant after controlling for mix |
| H2: Final §4966 regulations would unlock automation investment | Passes | unsupported | Low-Medium | Guardrail | Regulations finalize with a clear "reasonable fee" and advisor safe harbor, and vendors announce automated approval |
| H3: QCD-to-DAF (S. 3975) would raise DAF asset growth | Passes | suggestive (mechanism only) | Medium | Strategic, for policy makers | Bill dies, or enacted with payout conditions |
| H4: Requiring account-level reporting would chill giving | Defender claim [[S15](https://ministrywatch.com/california-would-be-first-state-law-to-reach-donor-advised-funds/)] | unsupported | Low | Guardrail | Evidence from any jurisdiction adopting it |
| H5: A 20–25% aggregate payout proves DAFs are not warehousing | Fails the bounded-truth test (aggregate versus account) | contradicted as stated by account-level 9% median [[S22](https://johnsoncenter.org/wp-content/uploads/2024/02/DAFRC_Executive_Summary_Key_Findings.pdf)] | Medium | n/a | Account-level national data released |
| H6: Better nonprofit UX (widgets) materially raises DAF grants | Passes | unsupported; DAF Direct reported stall [[S45](https://www.philanthropy.com/news/effort-to-spur-giving-from-donor-advised-funds-online-appears-to-stall/)] | Low | Experimental | Randomized widget tests published |

---

## 8. Critic and defender positions, and where evidence is contested

**Critics:**
- **IPS** (2022, 2023): payout requirement, account-level reporting, and ending foundation-to-DAF payout counting. They cite $85.5bn of DAF contributions in 2022 and 27% of individual giving [[S17](https://www.ips-dc.org/release-new-report-from-the-institute-for-policy-studies-reveals-the-true-cost-of-billionaire-philanthropy/),[S18](https://inequality.org/article/independent-research-donor-advised-funds/)].
- **Madoff** (2026): a time-limited distribution rule; DAFs as a "halfway house." In the WaterStone context she says "if you don't give up dominion and control, you don't get the tax benefits" [[S19](https://www.philanthropy.com/opinion/a-tax-scholar-suggests-policy-fixes-for-charitable-giving/),[S20](https://www.investmentnews.com/practice-management/multimillion-dollar-donor-advised-fund-lawsuit-puts-spotlight-on-control-risks/265478)].

**Defenders:**
- **DAFRC** (data producer, not advocate): 25.2% payout and segmentation of donation processors [[S21](https://www.dafresearchcollaborative.org/research/annual-daf-report)].
- **Philanthropy Roundtable** (Salmon): universal inactivity policies at large nationals [[S24](https://www.philanthropyroundtable.org/resource/donor-advised-funds-payout-trends-inactivity-policies-and-accessibility/)].
- **Opponents of AB 1712:** privacy and cost of account-level reporting [[S15](https://ministrywatch.com/california-would-be-first-state-law-to-reach-donor-advised-funds/)].
- National Philanthropic Trust handed its DAF report to DAFRC [[S21](https://www.dafresearchcollaborative.org/research/annual-daf-report)].

**Contested points:**
1. **The right payout denominator.** Aggregate versus account-level; whether DAF-to-DAF transfers inflate it.
2. **Whether inactivity policies bind in practice.** Policies exist, but enforcement counts are not published.
3. **Whether donor privacy is a sufficient reason to bar account-level reporting.** This is a normative question.
4. **Independence of research funding on both sides.** It is unresolved. Neither side's numbers should be treated as neutral by default.

---

## 9. Synthesis: structural versus habit

| Inefficiency | Classification | Main origin | Confidence |
|---|---|---|---|
| Asset-based fee alignment favouring retention | **Structural** (financial, contractual) | Trustee/affiliate contracts [[S30](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf),[S34](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf)] | Medium-High |
| No payout requirement | **Structural** (regulatory) | Statute [[S19](https://www.philanthropy.com/opinion/a-tax-scholar-suggests-policy-fixes-for-charitable-giving/)] | High |
| Advisor AUM on DAF assets | **Structural** (financial), with regulatory overhang [[S01](https://www.govinfo.gov/content/pkg/FR-2023-11-14/html/2023-24982.htm)] | Program fees [[S33](https://www.dafgiving360.org/features/fees-and-minimums),[S42](https://oneascent.com/wp-content/uploads/sites/25/2025/11/20260811-OAWM-ADV-Part-2A.pdf)] | Medium-High |
| Edge-case grant review | **Structural** (§4966/4967) | Statute [[S04](https://www.law.cornell.edu/uscode/text/26/4966),[S05](https://www.law.cornell.edu/uscode/text/26/4967)] | Medium-High |
| Manual review of listed public charities | **Mixed, leaning habit** | Liability aversion plus reliance available [[S07](https://www.thetaxadviser.com/issues/2018/aug/irs-updates-charitable-contribution-procedures/),[S16](https://oag.ca.gov/node/623769)] | Medium |
| Paper checks | **Mixed, leaning habit** | Board policies, defaults [[S26](https://www.fidelitycharitable.org/nonprofits/faqs.html)] | Medium |
| Year-end intake crunch | Timing **structural**; handling **habit** | Tax year; manual and postmark processes [[S28](https://www.fidelitycharitable.org/giving-account/what-you-can-donate/charitable-year-end-tax-deadlines.html)] | Medium |
| History loss in migrations | **Habit/mixed** | Vendor choices [R06] | Medium |
| Auto-renewal lock-in | **Mixed** | Contract terms [[S35](https://www.reninc.com/wp-content/uploads/2025/08/Online-RAC-MSA_v1.pdf),[S36](https://tifin.com/terms-conditions/)] | Low-Medium |
| Donor-to-sponsor switching | Legal core **structural**; process **mixed** | §4966 exception plus sponsor approval [[S04](https://www.law.cornell.edu/uscode/text/26/4966),[S20](https://www.investmentnews.com/practice-management/multimillion-dollar-donor-advised-fund-lawsuit-puts-spotlight-on-control-risks/265478)] | Medium |
| Weak nonprofit leverage | **Structural** | Nonprofit is not the payer or the legal party | Medium-High |

**Open questions:**
1. Have §4966 final regulations appeared after June 2026 (latest status: [S03](https://blog.pgcalc.com/the-state-of-play-navigating-the-current-landscape-of-qcd-legislation-and-daf-regulations))? This needs a Federal Register check.
2. What are the check versus EFT shares by sponsor?
3. How are Edward Jones and Morgan Stanley advisors compensated on DAF assets?
4. What is the status of S. 3975 and H.R. 891?
5. Does California have a live DAF-specific bill in 2026 (prior: [S14](https://www.govbuddy.com/california/bills/ab-2221/), [S15](https://ministrywatch.com/california-would-be-first-state-law-to-reach-donor-advised-funds/))?
6. How often are inactivity policies actually enforced?
7. Who funds the DAFRC research?

---

## 10. Sources (new in this document; repo-sourced items cited by file or ID above)

| ID | Source | Date | URL |
|---|---|---|---|
| S01 | Federal Register, Proposed Regs §4966 (REG-142338-07) | 2023-11-14 | https://www.govinfo.gov/content/pkg/FR-2023-11-14/html/2023-24982.htm |
| S02 | Council on Foundations regulatory tracker | 2026-05-08 | https://cof.org/page/proposed-rule-taxes-taxable-distributions-donor-advised-funds-under-section-4966 |
| S03 | PG Calc, "State of Play: QCD legislation and DAF regulations" | 2026-06-15 | https://blog.pgcalc.com/the-state-of-play-navigating-the-current-landscape-of-qcd-legislation-and-daf-regulations |
| S04 | 26 U.S.C. §4966 (Cornell LII) | read 2026-11-14 | https://www.law.cornell.edu/uscode/text/26/4966 |
| S05 | 26 U.S.C. §4967 (Cornell LII) | read 2026-11-14 | https://www.law.cornell.edu/uscode/text/26/4967 |
| S06 | IRS, Donor-advised funds | read 2026-11-14 | https://www.irs.gov/charities-non-profits/charitable-organizations/donor-advised-funds |
| S07 | Rev. Proc. 2018-32 summary (The Tax Adviser) | 2018-08 | https://www.thetaxadviser.com/issues/2018/aug/irs-updates-charitable-contribution-procedures/ |
| S08 | IRS nonitemizer deduction reminder (DAF excluded); Pub 6196 | 2026-11-10; 2026-10 | https://www.irs.gov/newsroom/irs-reminder-permanent-charitable-contribution-deduction-begins-for-returns-filed-next-year-for-taxpayers-who-do-not-itemize ; https://www.irs.gov/pub/irs-pdf/p6196.pdf |
| S09 | Grant Thornton 2026 individual planning guide | 2025 | https://www.grantthornton.com/insights/alerts/tax/2025/legislative-updates/2026-individual-tax-planning-guide |
| S10 | Thomson Reuters, "Charitable deduction unpacked" | 2025-12-02 | https://tax.thomsonreuters.com/news/charitable-deduction-unpacked-individual-itemizers/ |
| S11 | Steptoe, King–Grassley ACE Act | 2021 | https://www.steptoe.com/en/news-publications/senators-king-and-grassley-introduce-daf-and-private-foundation-reform-legislation.html |
| S12 | Ripon Advance, Young QCD-to-DAF bill (S. 3975) | 2026-03 | https://riponadvance.com/stories/young-introduces-bill-to-expand-charitable-giving-options-for-older-americans/ |
| S13 | Sen. Coons release, Charity Parity Act | 2026-05-14 | https://www.coons.senate.gov/?p=23646 |
| S14 | AB 2221 (Irwin) status, Ch. 590 Stats. 2026 | 2026-09-27 | https://www.govbuddy.com/california/bills/ab-2221/ |
| S15 | MinistryWatch/Tigner, CA AB 1712 | 2020-02-12 | https://ministrywatch.com/california-would-be-first-state-law-to-reach-donor-advised-funds/ |
| S16 | California AG, 16 AGs letter re SPLC payments | 2026-05-22 | https://oag.ca.gov/node/623769 |
| S17 | IPS, True Cost of Billionaire Philanthropy release | 2023-11-15 | https://www.ips-dc.org/release-new-report-from-the-institute-for-policy-studies-reveals-the-true-cost-of-billionaire-philanthropy/ |
| S18 | IPS (Collins & Flannery), DAF critique | 2022-03-24 | https://inequality.org/article/independent-research-donor-advised-funds/ |
| S19 | Chronicle of Philanthropy / The Conversation, Madoff interview | 2026-01-08 | https://www.philanthropy.com/opinion/a-tax-scholar-suggests-policy-fixes-for-charitable-giving/ |
| S20 | InvestmentNews, WaterStone DAF lawsuit | 2026-02-27 | https://www.investmentnews.com/practice-management/multimillion-dollar-donor-advised-fund-lawsuit-puts-spotlight-on-control-risks/265478 |
| S21 | DAFRC Annual DAF Report (revised Spring 2026) | 2026 spring | https://www.dafresearchcollaborative.org/research/annual-daf-report |
| S22 | DAFRC National Study key findings | 2024-02 | https://johnsoncenter.org/wp-content/uploads/2024/02/DAFRC_Executive_Summary_Key_Findings.pdf |
| S23 | DAFRC financial advisor research | 2026 | https://www.dafresearchcollaborative.org/financial-advisors |
| S24 | Philanthropy Roundtable (Salmon), payout and inactivity report; S24b "A DAF Storm is Brewing in California Again" (403, search summary only) | date not captured | https://www.philanthropyroundtable.org/resource/donor-advised-funds-payout-trends-inactivity-policies-and-accessibility/ ; https://www.philanthropyroundtable.org/a-daf-storm-is-brewing-in-california-again/ |
| S25 | Fidelity Charitable, How often do I grant | read 2026-11-14 | https://fidelitycharitable.org/faqs/all/how-often-do-i-grant.html |
| S26 | Fidelity Charitable, Nonprofit FAQs | read 2026-11-14 | https://www.fidelitycharitable.org/nonprofits/faqs.html |
| S27 | Fidelity Charitable, Grant processing timeline | read 2026-11-14 | https://www.fidelitycharitable.org/faqs/all/grant-processing-timeline.html |
| S28 | Fidelity Charitable, 2025 year-end contribution guidelines | 2025 | https://www.fidelitycharitable.org/giving-account/what-you-can-donate/charitable-year-end-tax-deadlines.html |
| S29 | Fidelity Charitable 2026 Giving Report | 2026 (CY2025 data) | https://www.fidelitycharitable.org/insights/2026-giving-report.html |
| S30 | Fidelity Charitable audited FS FY2025, Note 7 | FY ended 2025-06-30 | https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf |
| S31 | Vanguard Charitable FY2025 financial statements | FY ended 2025-06-30 | https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf |
| S32 | Fidelity Charitable, What it costs | read 2026-11-11 | https://www.fidelitycharitable.org/giving-account/what-it-costs.html |
| S33 | DAFgiving360 fees and minimums | read 2026-11-12 | https://www.dafgiving360.org/features/fees-and-minimums |
| S34 | RCF FY2024 audited financial statements | FY2024 | https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf |
| S35 | Ren (RAC) MSA template | 2023-06 label; posted 2025-08 | https://www.reninc.com/wp-content/uploads/2025/08/Online-RAC-MSA_v1.pdf |
| S36 | TIFIN terms | 2026-09-10 | https://tifin.com/terms-conditions/ |
| S37 | TIFIN Give Form ADV Part 2A | 2025-03-31 | https://tifin.com/wp-content/uploads/TIFIN-Give-Part-2A-of-Form-ADV-Brochure-2025.pdf |
| S42 | OneAscent Wealth Management ADV Part 2A | 2026-08-11 | https://oneascent.com/wp-content/uploads/sites/25/2025/11/20260811-OAWM-ADV-Part-2A.pdf |
| S43 | Edward Jones, donor-advised funds page (search snippet; fetched page lacked text) | snippet seen 2026-11-14 | https://www.edwardjones.com/us-en/investment-services/investment-products/donor-advised-funds |
| S45 | Chronicle, "Effort to spur giving from DAFs online appears to stall" (DAF Direct) | 2015 | https://www.philanthropy.com/news/effort-to-spur-giving-from-donor-advised-funds-online-appears-to-stall/ |
| S46 | FINRA, Regulation Best Interest | read 2026-11-14 | https://www.finra.org/rules-guidance/key-topics/regulation-best-interest |

**Repo-sourced items reused:**
- R02, R03, R06, R13 and R22: `data/revenue-retention-sources-2026.csv`
- G01, G02 and G20: `data/sponsor-governance-sources-2026.csv`
- MS GIFT: `research/bofa-morgan-stanley-institutional-ren-evidence-2026-11-11.md`
- `research/batch-1a`, `research/batch-1c` and `research/batch-2a` files

**Integrity notes:**
- S07, S12, S14 and S24 were read through secondary summaries.
- S24's full text returned HTTP 403.
- No numbers were invented. Every figure is quoted from a source.

---

## 11. Data dictionary: `data/mission-2026-11-14/incentive-map.csv`

| Column | Type | Definition |
|---|---|---|
| `stakeholder` | text | Actor holding the incentive (sponsor, affiliate, administrator, advisor, donor, nonprofit, regulator, vendor) |
| `incentive` | text | What the actor gains or avoids |
| `mechanism` | text | How the incentive operates (fee formula, statute, contract clause, policy) |
| `evidence_url` | URL | Primary or best-available source. Multiple URLs are separated by ` ; ` |
| `evidence_date` | text | Publication or period date of the evidence, or the read date where undated |
| `effect_on_modernization` | enum | `accelerates` / `discourages` / `neutral`. The direction the incentive pushes adoption of better tools; mixed effects are described in notes |
| `structural_or_habit` | enum | `structural constraint` / `historical habit` / `mixed` / `unknown`, under the mission guide's test (§2) |
| `clarity_status` | text | Claim state from the EDF claim policy (documented = bounded fact; suggestive; unsupported; contradicted) plus confidence label (Low to High) |
| `notes` | text | Fact versus inference, contested points, reconsideration trigger |

## Red-team corrections (wave 2B, 2026-11-14) — governing
- **§1.3 and §3.4 Status.** Replace it with: "No final rule in the Federal Register as of 2026-11-14 (only the NPRM 2023-11-14, the comment extension to Feb 15, 2024, and the 2024 hearing notices). The 2026–2027 PGP (released 2026-09-29) lists 'Guidance under §§4966 and 6033 regarding certain donor advised fund arrangements', replacing the prior 'final regulations' item." ([Federal Register NPRM 2023-24982](https://www.govinfo.gov/content/pkg/FR-2023-11-14/html/2023-24982.htm); [comment extension 2024-00260](https://www.federalregister.gov/d/2024-00260); [IRS 2026–2027 PGP](https://www.irs.gov/pub/irs-counsel/2026-2027-initial-pgp.pdf)) Also change "Comments were due January 16, 2024" to "February 15, 2024 (extended)".
- **§3.4 SPLC.** Change "DAF Giving" to "DAFgiving360 (Donor Advised Charitable Giving, Inc.)". Add the indictment date, April 21, 2026, and the source [[S16](https://oag.ca.gov/node/623769)].
- **§6.1 Outcome A.**
  - Add: "Fidelity states it is 'transitioning grant payments to EFT' as part of a 'digital-first policy'; Chariot (Mar 2026) reports 67% of Fidelity grants by EFT and a planned move to electronic-only in July 2026 (not confirmed on Fidelity's live FAQ, which still says EFT is not required)." ([Fidelity nonprofit FAQ](https://www.fidelitycharitable.org/nonprofits/faqs.html); [Chariot, Mar 2026](https://www.givechariot.com/resources/insights/top-8-takeaways-from-fidelity-charitables-2026-giving-report))
  - Delete "neither faces a forcing incentive".
  - Change "Industry-wide check share is not observed" to "Fidelity: ~33% of grants by check in 2025 (secondary)" ([Chariot, Mar 2026](https://www.givechariot.com/resources/insights/top-8-takeaways-from-fidelity-charitables-2026-giving-report)).
- **§9.**
  - Change "Asset-based fee alignment favouring retention | Structural … | Medium-High" to "Mixed (incentive documented; effect unsupported) | Medium (existence) / Low (effect)".
  - Add the DAFRC segment payout medians as counter-evidence.
  - Change "Manual review of listed public charities | Mixed, leaning habit" to "Mixed".
- **incentive-map.csv.**
  - Treasury/IRS row: change `clarity_status` to "documented (status); suggestive, Low-Medium (effect)".
  - Vanguard row: change `structural_or_habit` to `mixed`.

## Validation corrections (wave 4, 2026-11-14) — governing
Source: [validation-wave4-report.md](validation-wave4-report.md). Where these conflict with the text above, these govern.

- **W4-13** (research/mission-2026-11-14/industry-incentives-structural-analysis.md line 143): replace "Sixteen attorneys general asked them on May 22, 2026" → "Sixteen attorneys general, led by Minnesota, asked them in a letter dated May 21, 2026 (California release May 22)"
