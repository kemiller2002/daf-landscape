# Historical DAF Sponsor and Technology Lifecycle, 2011–2026
**Research cutoff November 11, 2026. This is a sourced known-case ledger, not a population-wide mortality census.**

## Findings

Historical events must be classified by **legal sponsoring charity**, **for-profit technology company**, **product brand**, **donor access**, and **where charitable money actually went**. An acquisition, bankruptcy, grant, rebrand, and retired portal are different events and should not be counted as equivalent business failures. The [24-event record](../data/historical-daf-lifecycle-events-2011-2026.csv) includes 21 period events, two earlier antecedents, and one planned future sunset. There are **33 source records** in the [history source register](../data/historical-daf-lifecycle-sources-2011-2026.csv). The dataset is based on disclosed events, not an exhaustive list of firms, so it cannot establish a mortality rate.

## Core technology ownership history

| Date | Sourced technology or product transition | Unverified issue |
|---|---|---|
| Feb. 8, **2011** | Renaissance acquired Blackbaud's DAF technology business, part of the Giving Capital/Kintera DAF lineage [HL01,HL02] | Neither source-code genealogy nor customer migration success confirmed |
| **2016** | RenPSG announced Crown Philanthropic Solutions/DonorFirst acquisition agreement; Ren's later corporate timeline identifies it as an acquisition [HL03,HL04] | Exact close date, platform integration and retention unknown |
| Mar. **2021** | Pinkaloo founder confirmed its acquisition by RenPSG [HL05] | Acquisition is not proof of technology quality or vendor financial trouble |
| Jan. **2023** | Ren acquired Stellar Technology Solutions / iPhi [HL06] | No observed merging of all acquired ledgers into one architecture |
| Oct. **2024** | Foundation Source acquired Vennfi; Charityvest remained the separate legal charity [HL07] | Charityvest assets weren't thereby sold as corporate software assets |
| Apr. **2025** | TIFIN transferred Giving Place to Foundation Source while TIFIN Give kept a separate DAF offering [HL08] | No established cessation of TIFIN's DAF service |

This is a substantial commercial consolidation history, but it does **not** support company-wide software revenues, a single codebase, market share, profitability, or client churn by itself.

## Direct DAF charity lifecycle: National Heritage Foundation

National Heritage Foundation (NHF) is a genuinely relevant **DAF sponsoring-charity** case rather than an adjacent donation software firm.

- A federal appellate opinion documents its **2009 Chapter 11** reorganization and legal issues around donor contributions and advisory rights [HL15,HL16]. Chapter 11 did not mean immediate liquidation.
- The IRS explicitly **revoked its charitable determination in 2011** [HL14]. Separately, the later IRS-derived ProPublica entry identifies a **June 2014** exemption-issued date [HL20]. The original 2014 determination terms were not retrieved; we cannot assume the 2011 revocation continued unchanged through the end of the period.
- United Charitable's 2021 audited disclosures refer to NHF as a supporting charity [HL21]. The public IRS-based FY2022 extract shows **$0 year-end NHF assets**, expenses of roughly **$4.07 million**, and grant distributions of roughly **$4.04 million**, including **$3.84 million to United Charitable** [HL17–HL19]. An independent source flags the 2022 return as final, but the *original complete FY2022 Form 990 and Schedule N* have not been reviewed because the accessible PDF endpoint was blocked.
- The [five-point asset trajectory](../data/national-heritage-foundation-filing-trajectory-2014-2022.csv) shows declining *legal organization total assets* from 2014 to the reported 2022 zero. **It is not a measure of donor losses or confirmed individual account transfers**.

**Clarity conclusion:** This establishes a real sponsor's bankruptcy, tax status change and apparent later wind-down. It does **not** establish that every donor lost funds, that the full $3.84 million to United Charitable transferred with unchanged DAF advisory rights, or that the organization remained continuously disqualified after 2011. A legal and fund-level case study needs the original FY2022 filing, any Schedule N transfer data, the 2014 determination and legally permitted successor fund reconciliation.

**EDF next step:** Trace the actual creditor/fund control events, regulator action, sponsor support relationship and final permitted account transfers before attributing causes or calculating losses. Sponsor bankruptcy is legally distinct from failure of its software vendor.

## Direct technology continuity: American Endowment Foundation

AEF is a **continuing legal DAF sponsor** that changed donor portals:

1. **2024**: AEF's communications document its DonorCentral migration from Blackbaud to NPact and resetting donor logins; some older unsubmitted shopping-cart drafts were removed [HL09,HL10].
2. **2026**: AEF's scheduled March–April transition brought a new Ren-powered platform online [HL11].
3. **October 31, 2026**: AEF's [official sunset notice](https://engage.aefonline.org/dc-sunset/) states that DonorCentral access shut down, that the new Ren portal shows **two years of historical donor activity**, and that donors can request the older histories from AEF staff [HL12].

**Clarity conclusion:** There is verified retirement of a *DAF donor portal* and reduction in immediate **self-service access** to old statements, grants, and receipts. This does **not** mean that the charitable assets were lost, that the old records were permanently deleted, or that either previous vendor failed financially.

**Technology acceptance test:** A sponsor should demonstrate that a new provider can reconstruct **at least five years** of fund contributions, approved/denied grants, receipts, anonymization preferences, balances and fees with accurate sponsor ledger totals. Differentiate **approved** grants from unsubmitted drafts and self-service access from records retrievable through staff.

## Adjacent cases, correctly separated

- **TakeCharge.io** (2018): First-party fundraising experiment closed despite donations processed; no DAF sponsor or funds-lost evidence [HL22].
- **Everfund** (November 2024) and **Kambeo** (March 2026): First-party fundraising platform shutdowns with data-export/deletion requirements. Not verified core DAF administration or charity failures [HL23,HL24].
- **Flipcause** (November 2025 enforcement; 2026 Chapter 7 conversion): Payment intermediary legal/funds safeguarding risk. California AG remittance allegations and later bankruptcy figures are different dated amounts, not a combined loss estimate [HL25,HL26].
- **Schwab Charitable → DAFgiving360** (legal brand transition **June 18, 2024**) and **Classy → GoFundMe Pro** (2025): Rebrands, not firm collapse [HL13,HL28].
- **DonorPerfect** (November 2026): Adjacent CRM service interruption with possible donor record synchronization delays, not a closed company or proven data breach [HL29].
- **Benevity Alaya**: Product retirement is *scheduled for December 15, 2026*, so it is a future planned event relative to the study, not an observed failure [HL27].

## A credible 15-year closure rate still requires a true census

The existing observed examples are a **convenience sample**. To estimate a vendor or sponsor failure rate:
- Build a **2011–2025 sponsor EIN-year panel** using IRS Schedule D/990, DAFRC historical classifications, IRS tax determination records, legal entity changes and verified complete final returns. A filing gap alone isn't evidence of dissolution.
- Build a separate **for-profit vendor legal company-year and product SKU-year panel**, assigning launch, version, owner, acquisition, planned/complete sunset, bankruptcy and changed license.
- Join actual sponsor-to-provider signed contracts (not partner logos) by period.
- Track individually permitted and anonymized **charitable money, donor advisory rights and historical data** before/after actual transitions.
- Cross-check court cases with relevant primary dockets, not secondary bankruptcy headlines.
- Retain Unknown as an explicit state. Do **not** manufacture a mortality-rate numerator from this ledger.

## Connected affinity/community relevance

This lifecycle framework applies to **faith-based and affinity sponsors as well**. A megachurch, Catholic parish foundation, Jewish communal sponsor or Muslim community foundation may have distinct legal ownership and a connected private platform. Vendor closure might affect the **portal** without affecting the legal charity, while **sponsor insolvency** could implicate donated assets and donor rights. The new [affinity-sector analysis](affinity-dafs-megachurches-and-special-interest-organizations-2026-11-11.md) sets these roles apart.

### Research artifacts

- [Historical event ledger, 24 dated entries](../data/historical-daf-lifecycle-events-2011-2026.csv)
- [Source register, 33 entries](../data/historical-daf-lifecycle-sources-2011-2026.csv)
- [Historical Clarity audit, 18 questions](../data/historical-daf-lifecycle-clarity-challenges-2026.csv)
- [NHF five-year selected asset trajectory](../data/national-heritage-foundation-filing-trajectory-2014-2022.csv)

**No actual vendor platform, court docket/fund records, complete original NHF FY2022 IRS filing, or historical software population was independently executed or extracted.**
