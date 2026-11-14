# DAF vendor dependency graph and concentration analysis

**Date:** 2026-11-14. **Status:** public-source evidence only. No contracts, SOC reports, production systems or authenticated portals were reviewed.
**Data:** [`data/mission-2026-11-14/relationship-graph-edges.csv`](../../data/mission-2026-11-14/relationship-graph-edges.csv) has 167 edges. [`data/mission-2026-11-14/relationship-graph-nodes.csv`](../../data/mission-2026-11-14/relationship-graph-nodes.csv) has 131 nodes.
**Builds on:** `data/expanded-ecosystem-relationships-2026.csv` (edges L01–L21), `data/expanded-daf-market-map-2026.csv`, the Edward Jones, Ren-distribution, BofA/Morgan Stanley, NPT, Goldman, Charityvest/TIAA, DNS-reconnaissance, technology-audit and startup research files dated 2026-11-11/12.

---

## 1. Summary of findings

1. **Ren is the hub of the graph.** Ren appears in 34 edges and Renaissance Charitable Foundation (RCF) in 22. Ren's DonorFirstX ("DFX powered by Ren") portal family hosts these branded programs:
   - RCF programs for Edward Jones, Ameriprise, RBC Wealth Management, Commonwealth/LPL, SEI (SEI Giving Fund), the MDRT Foundation, Franklin Templeton and First Citizens.
   - Two programs that RCF does not sponsor: **Morgan Stanley GIFT** and the **Bank of America Charitable Gift Fund**.

   Most of this was re-verified live on 2026-11-14. The Ameriprise portal is the exception: its fetch did not show the footer, so Ren's role there rests on Ren's Ameriprise guide. **New in this pass:** MS GIFT's donor site (`msgift.donorfirstx.com`) runs on Ren DFX. Earlier repo work had only documented RenPSG as MS GIFT's back-office administrator.
2. **Edward Jones (standard program).** On the evidence below, RCF is the legal sponsor, RCF manages and administers the program, and Ren supplies the donor technology.
   - **RCF as sponsor: confirmed.** Edward Jones's own product page says RCF "manages and administers" the fund. Sponsor status follows from that page combined with RCF's own description of itself as the sponsoring charity of its programs.
   - **RCF administration: confirmed.**
   - **Ren technology: confirmed.**
   - **Ren back-office administration for Edward Jones specifically: inferred only.**
   - **Private DAF:** Edward Jones's newer private DAF (part of its Generations offering) has no publicly identified sponsor, administrator or vendor.
3. **Apparently independent competitors share infrastructure.**
   - Seven or more wealth firms are on one sponsor (RCF) and one vendor (Ren).
   - Charityvest's turnkey programs (TIAA, Temple, OneGive) are on Foundation Source.
   - Chariot Disbursements now serves TIFIN Give/GiveClear (which also powers the new SEI Charitable Fund), Daffy, Founders Pledge, Groundswell, and Charityvest (from August 2026).
   - CapShift serves both MS GIFT and RCF's Commonwealth channel.
   - IRS EO BMF and Pub 78 data are the upstream source for every charity-eligibility check whose sources are disclosed (Chariot, Candid).
4. **Fidelity Charitable, DAFgiving360 and Vanguard Charitable are administered by their commercial affiliates.** Each one's audited statements or own disclosure say so. Together they hold about **49%** of DAFRC's FY2024 sponsor assets of $327.87bn.
5. **Sponsor assets are moderately concentrated.** On a bounded estimate, CR3 is about 58%, CR4 about 66% and CR5 about 70%. HHI is about 1,290 for the listed sponsors, with an upper bound of about 1,370.
6. **Ren's market-share claim cannot be reconciled with public data.** Ren claims its technology serves ">60%" (website), "approximately half" ($175bn+, Oct 2025) or "$200bn" (Apr 2026) of US DAF assets.
   - Sponsors with public Ren evidence account for only about **8.7%** (RCF, AEF, MS GIFT, BofA CGF).
   - Three affiliate-administered giants plus NPT's own GivingPoint platform account for about 66%. That leaves at most about 34% for everyone else.
   - The claim therefore implies undisclosed Ren components inside one or more of the four largest sponsors, a non-DAF or later-dated denominator, or a different metric. **This finding is labelled disputed.**

---

## 2. Method and status rules

**Scope of edges.** An edge is a directed, typed relationship between two entities. The relationship types are:
- `sponsor_of`, `administers`, `technology_provider`, `custodian`, `investment_manager`
- `distributor_white_label`, `payment_processor`, `charity_verification`, `ai_provider`
- `acquirer`, `investor`, `board_overlap`

**Status rules (applied strictly):**
- `confirmed`: a dated or live primary statement by a party to the relationship, or an audited or regulatory filing, states the relationship *of that type*.
  - A logo or brand on a page confirms only a *partnership or distribution claim*.
  - A "DFX powered by Ren" footer confirms that Ren supplies the *portal technology*. It does not confirm administration, ledger, contract or SSO scope.
  - Where the evidence came from a search-engine excerpt because a direct fetch was blocked (403/503/JS-only), the `notes` field says so.
- `historically_confirmed`: confirmed for a past period, with current status unverified. Examples: 2014 iPhi selections, the 2020 NPT/Stellar documents, an archived Pershing page.
- `inferred`: a reasonable reading from indirect evidence that no party states outright. Examples: a Ren-domain support mailbox implies Ren servicing; a third-party page implies the sponsor.
- `disputed`: sources conflict. This applies to the Ren market-share claim, which is treated in prose because it is not an edge.
- `unknown`: the relationship slot is material and no evidence was found either way. Examples: the sponsor of Edward Jones's private DAF, Goldman PWM's vendor, TIFIN's LLM vendor, Ren–NPT today.

**Evidence handling.**
- Repo sources were reused with their original access date (2026-11-11 or 2026-11-12).
- The consequential ones were re-fetched on 2026-11-14 and carry that access date. In total, 122 of 167 edges were (re)checked this pass.
- The edges cite **88 distinct URLs**.

**Counts.**

| Edge status | n |
|---|---|
| confirmed | 134 |
| historically_confirmed | 17 |
| inferred | 11 |
| unknown | 5 |
| **Total edges** | **167** |

| Relationship type | n |
|---|---|
| technology_provider | 40 |
| distributor_white_label | 31 |
| sponsor_of | 24 |
| administers | 21 |
| payment_processor | 15 |
| investment_manager | 11 |
| investor | 9 |
| acquirer | 8 |
| charity_verification | 3 |
| custodian | 2 |
| ai_provider | 2 |
| board_overlap | 1 |

Nodes by type: 31 financial advisory firms, 30 DAF sponsors, 25 branded DAF programs, 14 technology vendors, 3 technology+administration vendors (Ren, Foundation Source, CapShift), 7 investment managers, 6 payment processors, 5 investors, 2 custodians, and others.

---

## 3. Ren–financial institution relationships: what each piece of evidence proves

For each pairing, the table separates (a) Ren technology, (b) Ren or RCF administration, and (c) RCF as legal sponsor.

| Institution / program | (a) Ren technology | (b) Administration | (c) RCF legal sponsor | Key evidence |
|---|---|---|---|---|
| **Edward Jones Charitable Gift Fund** | **Confirmed.** Portal footer "DFX powered by Ren" | **RCF: confirmed** ("partnered with Edward Jones to manage and administer"). **Ren: inferred** (RCF FAQ: Ren supplies "administrative infrastructure, and operational support" to RCF programs; RCF–Ren audited admin contract; Ren help-centre "EJ DAF opening instructions" seen only in search index) | **Confirmed (by combination).** EJ product page (search excerpt) and portal; RCF FAQ; no separate EJ charity found | edwardjones.donorfirstx.com; renaissancecharitable.org/faqs; EJ brochure ANG-13116H-A-E-SR |
| Edward Jones private DAF (Generations) | Unknown | Unknown | **Unknown** | EJ press release names no sponsor or vendor |
| Ameriprise | Confirmed (Ren guide: nightly feed to Ren, Ren review) | Ren: confirmed | Confirmed (portal: "RCF DAF Program"; "Ameriprise is not affiliated with RCF") | ampf.donorfirstx.com; reninc.com/ampf-rcf-daf |
| RBC Wealth Management | Confirmed (portal hosted on Ren DFX domain, same template) | Not stated | Confirmed ("RCF Donor-Advised Fund Program for RBC WM Clients") | rbcrcf.donorfirstx.com (**new**) |
| Janney | Confirmed ("Ren will power Janney's full-service DAF program at RCF"; integrates with Janney SMART) | Ren: confirmed ("technology and managed services") | Confirmed | PR Newswire, 2024-10-18 (**new**) |
| LPL (direct channel) | Implied by guide | Ren: confirmed ("Once Ren does a final review…") | Confirmed (RCF account owner) | reninc.com/lpl-rcf-daf |
| Commonwealth Charitable Fund (LPL trade name) | Confirmed (footer) | Not stated | **Inferred** (CapShift page refers to "your Renaissance Charitable Foundation DAF account") | cfndaf.donorfirstx.com; capshift.com/commonwealth (**new**) |
| Northwestern Mutual | Implied by Ren-hosted circular | Not stated | Confirmed (RCF program circular with partner-specific fees) | Repo |
| UBS (RCF option) | Implied | Ren: confirmed ("partners with Ren to bring … technology and servicing") | Confirmed. **UBS is multi-sponsor:** its fact sheet lists Fidelity Charitable, ImpactAssets, NPT and RCF | reninc.com/why-ubs-advisors-choose-rcf; UBS fact sheet (**new**) |
| SEI Giving Fund | Confirmed (footer) | Not stated | Confirmed (RCF contact; GuideStar lists RCF "aka SEI Giving Fund") | sei.donorfirstx.com (**new**). **SEI separately launched the SEI Charitable Fund on 2026-10-28 on TIFIN Give/GiveClear**, so SEI distributes two competing stacks |
| MDRT Global Gift Fund | Confirmed | Not stated | Confirmed ("offered through RCF") | mdrt.donorfirstx.com (**new**) |
| Fisher Investments | Implied | Ren: confirmed (final review) | Confirmed | reninc.com/rcf-fisher-daf (**new**) |
| Pershing-custodied advisors | Implied | Ren: confirmed | Confirmed; Pershing data feed prefix TU5 → **custodian edge** | reninc.com/rcf-pershing-daf (**new**) |
| Franklin Charitable Giving Program | Confirmed | **RCF: confirmed** ("serviced by RCF" since 2005) | **Unknown**; not stated on the portal | ft.donorfirstx.com (**new**) |
| First Citizens DAF | Confirmed | **RCF: confirmed** (agreement "to provide administrative services"); First-Citizens Bank is investment manager | **Not stated**; RCF described as operator of private-label programs | firstcitizensdaf.donorfirstx.com (**new**) |
| TDA-coded RCF portal | Confirmed | Not stated | Confirmed (RCF) | tda.donorfirstx.com. The TD Ameritrade link is **inferred** only from the subdomain and file names |
| **Morgan Stanley GIFT** | **Confirmed (new):** msgift.donorfirstx.com "DFX powered by Ren" | **RenPSG: confirmed** as unaffiliated back-office administrator (MS content hub; repo) | **No.** MS GIFT is its own 501(c)(3) (EIN 52-7082731). CapShift administers its recoverable grants | |
| **Bank of America CGF** | **Confirmed:** bofa.donorfirst.org "DFX powered by Ren" | Ren: **inferred** (support email @reninc.com) | **No.** Separate charitable trust; BofA Private Bank manages investments | |
| American Endowment Foundation | Confirmed (Ren "technology and services now fully power all" AEF customers, 2026-04-08) | Ren: inferred (scope not enumerated) | **No.** AEF is an independent sponsor | aefonline.org release |
| NPT | **Unknown.** Only a historical Stellar (2020) link plus Ren's 2023 Stellar acquisition | No | No | Repo rule upheld |
| Goldman Sachs (PWM DAF, GS Gives) | Unknown | Unknown | No (separate charities) | No new evidence |

**Interpretation.** Ren works through three distinct models:
- **Model A:** RCF sponsors and Ren administers, under a firm's brand. This covers Edward Jones, Ameriprise, RBC, Janney, LPL, Commonwealth, Northwestern Mutual, UBS-RCF, SEI Giving Fund, Fisher and MDRT.
- **Model B:** an independent or bank-affiliated sponsor buys Ren technology and, in some cases, Ren administration. This covers MS GIFT, BofA CGF and AEF.
- **Model C:** RCF acts as administrator to a program whose legal sponsor is not stated. This covers Franklin and First Citizens.

"Customer of Ren" therefore means different things in different rows, and the rows must not be collapsed.

**Edward Jones conclusion.** The public record supports the following for the *standard* Edward Jones Charitable Gift Fund:
- **(a) Ren technology: confirmed.**
- **(b) RCF administration: confirmed.** Ren-performed administration is **inferred**.
- **(c) RCF legal sponsorship: confirmed by combination** of Edward Jones's own product page and RCF's statements.

Edward Jones's 2026 brochure says only that "a third-party administrator is responsible for day-to-day operations" and names neither RCF nor Ren. The 2021 figure of more than $2.9bn in RCF-supported assets for Edward Jones (from a Ren guide in the repo) is historical and should not be used as current program assets. Nothing public establishes that the private Generations DAF uses RCF or Ren.

---

## 4. Shared-infrastructure findings

**4.1 Many wealth brands, one sponsor, one vendor (RCF + Ren).** At least eleven distribution brands route clients to the same legal sponsor and the same vendor:
- Edward Jones, Ameriprise, RBC, Janney, LPL, Commonwealth/LPL and Northwestern Mutual
- UBS (as one of four options), SEI, Fisher and MDRT

Two more programs (Franklin, First Citizens) are administered by RCF. Program circulars show partner-specific fees, so they compete on price and brand. Their charitable-law risk, grant-approval policy and vendor risk are shared: one sponsor board, one vendor contract (RCF pays Ren 98% of individual fund-holder admin fees, with audited FY2024 payments of $19.23m), and one portal codebase family. RCF's FY2024 Schedule D shows $5.91bn across 25,824 DAFs. That is small relative to the market but highly concentrated in operational terms.

**4.2 One portal platform across competing sponsors.** DFX/DonorFirst also fronts:
- MS GIFT (about $9.1bn DAF value in FY2024, from a secondary source)
- BofA CGF ($5.04bn net assets)
- AEF ($8.40bn)
- community and university programs (Gulf Coast CF and Southeast Missouri State, both inferred from search index only)

Morgan Stanley, Bank of America and the RCF-branded wirehouses therefore compete for clients through **portals from the same vendor**. Together these publicly evidenced Ren-linked sponsors hold about $28.5bn (8.7% of DAFRC FY2024 assets).

**4.3 Foundation Source turnkey cohort.** Charityvest (an independent 501(c)(3)) sponsors the TIAA Wealth Management DAF, the Temple University DAF and OneAscent's OneGive. Foundation Source powers all three.

Foundation Source's ownership ties run through several parties:
- GTCR owns Foundation Source (2023).
- Foundation Source acquired Vennfi, PG Calc and Giving Place.
- A OneAscent fund holds an indirect equity interest in Foundation Source, while OneAscent also distributes OneGive.
- Foundation Source separately serves Northern Trust, but for private foundations, not DAFs.

**4.4 Chariot as a disbursement layer.** Chariot Disbursements partners, all company-stated, include:
- TIFIN Give (and therefore GiveClear programs, including the new SEI Charitable Fund, AssetMark, Zions and Confluence channels)
- Daffy, Founders Pledge, Groundswell and GoodToday
- Saint Paul & Minnesota Foundation and Brooklyn Org
- Charityvest, which moves to Chariot from August 2026, "expanding to turnkey partner accounts shortly after"

If Charityvest expands as stated, **TIFIN/GiveClear and Foundation Source/Charityvest, two otherwise competing advisor-DAF stacks, will share a grant-payment rail.** Chariot's deposit accounts are held at **Column N.A.** DAFgiving360 and Thrivent Charitable appear only as DAFpay (donor checkout) access points. That is not evidence that their grants are paid through Chariot.

**4.5 Payment rails among the largest sponsors.**
- Fidelity Charitable uses Stripe and ACH.
- Vanguard Charitable and NPT both document PayPal Grant Payments.

These are third-party rails underneath otherwise in-house administration.

**4.6 Charity-eligibility data is effectively universal.**
- Chariot builds its database from IRS BMF, Form 990, Pub 78 and OFAC.
- Candid's Charity Check API relies on IRS BMF, Pub 78 and GuideStar data.
- Groundswell markets a GuideStar integration.
- Ren, Edward Jones ("ensure the charity … is approved by the IRS") and Vanguard ("good standing with the IRS") describe IRS-status checks without naming a vendor.

The IRS EO BMF and Pub 78 are therefore the common upstream dependency. Their refresh cadence and coverage gaps (churches, group exemptions) are shared by every downstream checker.

**4.7 CapShift across competitors.** CapShift administers MS GIFT's recoverable-grant offering and provides recoverable-grant access to Commonwealth advisors' RCF DAFs. This is a niche dependency, but it is shared.

**4.8 Investor and board linkages.**
- TIFIN's backers include J.P. Morgan, Franklin Templeton, SEI, Morningstar and Hamilton Lane. Of these:
  - SEI distributes the TIFIN program while also distributing the RCF/Ren SEI Giving Fund.
  - Franklin Templeton distributes an RCF/Ren program.
  - Hamilton Lane manages a Vanguard Charitable pool.
- J.P. Morgan's own DAF is sponsored by NPT.
- Ren's investors are Bain Capital Tech Opportunities (majority stake, 2023), Valeas and Great Hill Partners (October 2025).
- Ren's board includes **Amy Danforth, former President of Fidelity Charitable**. This is a board-overlap edge only. It is **not** evidence that Fidelity Charitable uses Ren.

**4.9 Distribution multi-homing.** Distribution is not exclusive.
- UBS offers four sponsors.
- SEI offers two stacks.
- LPL reaches RCF through two channels (its direct guide and Commonwealth).
- BNY's archived Pershing page listed both AEF and RCF.
- Wells Fargo and J.P. Morgan use NPT.
- Raymond James and Stifel run affiliated sponsors (Raymond James Charitable Endowment Fund, managed by Raymond James Trust; Stifel Charitable Inc.) whose technology vendors are not public.

No public sponsor or vendor evidence was found for Baird, Truist, PNC, US Bank, Envestnet or Merrill (as a channel distinct from BofA CGF). They are therefore absent from the edge file rather than guessed.

---

## 5. Concentration analysis

Each market is measured separately. HHI and CR figures are on a 0–10,000 HHI scale and in percent.

### 5.1 Assets (sponsor-held DAF assets)

**Denominator.** DAFRC Spring 2026 revised FY2024 sponsor-held DAF assets: **$327.87bn** across 1,512 sponsors. This is defensible as a census of Schedule D filers.

**Numerators.** FY2024 values are aligned to IRS tax year 2024. For June fiscal-year sponsors, that is the year ending June 2025.

| Sponsor | Value ($bn) | Measure | Share of $327.87bn |
|---|---|---|---|
| Fidelity Charitable | 85.86 | audited net assets, 6/30/2025 | 26.2% |
| National Philanthropic Trust | 55.90 | 990 Sch. D DAF value, TY2024 | 17.0% |
| DAFgiving360 | 47.42 | 990 net assets, FY6/2025 | 14.5% |
| Vanguard Charitable | 27.21 | audited net assets, 6/30/2025 | 8.3% |
| GS PWM DAF | 12.6 | Sch. D (secondary, unverified) | 3.8% |
| MS GIFT | 9.11 | Sch. D (secondary) | 2.8% |
| AEF | 8.40 | 990 net assets CY2024 | 2.6% |
| RCF | 5.91 | Sch. D CY2024 | 1.8% |
| BofA CGF | 5.04 | 990 net assets FY2024 | 1.5% |

**Results (bounded estimate):**
- **CR3 ≈ 57.7%**, **CR4 ≈ 66.0%**, **CR5 ≈ 69.8%**
- HHI from the nine listed sponsors ≈ **1,289**. This is a lower bound.
- Upper bound: spreading the remaining 21.5% in blocks no larger than the fifth-largest share (3.84%) gives **HHI ≤ ~1,370**.

That places sponsor assets in the "moderately concentrated" band of the 2023 Merger Guidelines (1,000–1,800).

**Caveats.**
- Net assets and Schedule D DAF value are mixed measures. Fidelity's and DAFgiving360's net assets may include small non-DAF balances.
- The GS and MS GIFT values are secondary extracts.
- An unlisted sponsor larger than $12.6bn would raise CR5. None is known in the repo, but the full DAFRC sponsor file has not been downloaded.
- Treat these figures as ±2 percentage points (CR) and ±100 (HHI).

Grants, as a cross-check (periods differ, so these are not combined into an index): Fidelity CY2025 $18.3bn; DAFgiving360 FY2026 >$10bn; NPT FY2025 $6.44bn; Vanguard CY2025 $3.96bn. DAFRC FY2024 total grants were $64.60bn.

### 5.2 Administration (who runs the back office)

**Defensible numerator (lower bounds, as a share of $327.87bn):**
- **Affiliate-administered:** FMR for Fidelity Charitable (26.2%), Schwab subsidiaries for DAFgiving360 (14.5%), The Vanguard Group for Vanguard Charitable (8.3%). Together: **49.0%**, held by three separate administrators.
- **Self-administered with the vendor unknown:** NPT, 17.0%. GivingPoint's developer is not public.
- **Ren, publicly evidenced:** RCF, AEF, MS GIFT and BofA CGF, about **8.7%**. Ren's role is technology in every case. Administration is confirmed for RCF and MS GIFT and inferred for AEF and BofA.
- **Other affiliated in-house (not quantified here):** Raymond James Trust, BNY Mellon N.A. and Stifel.
- **Foundation Source (Charityvest):** about $0.22bn (self-reported), about 0.07%.

**HHI: not computable as a point estimate.** About 34% of assets have no identified administrator. A bounded range, assuming each named administrator is distinct:
- If Ren's share is only its evidenced 8.7% and the unknown 25% is atomised: HHI ≈ **1,330**.
- If the entire unidentified 34% were Ren: HHI ≈ **2,410**, which is highly concentrated.

**Ren's own claims cannot both hold alongside the disclosures above.** Ren claims ">60%" or "approximately half" of DAF assets on "Ren technology" ($175bn, Oct 2025; $200bn, Apr 2026). That is 53–61% of the FY2024 denominator. Fidelity, DAFgiving360 and Vanguard disclose affiliate administration, and NPT presents GivingPoint as its own platform. If those four are excluded, at most about 34% remains.

The claim therefore requires at least one of the following:
- Ren components (for example, technology modules, payments or data) inside one or more of the four largest sponsors, none of which is publicly disclosed
- a numerator that counts non-DAF charitable assets, such as community-foundation endowments on iPhi
- a different measure (for example, "rely on" any Ren component) or a later, larger denominator

**Status: disputed.** Do not cite Ren's percentage as a market share.

### 5.3 Software

**Not computable.** No denominator of sponsor technology spend or seats exists, and vendor counts are self-reported across different units:
- Ren: ">150 DAF programs"
- Foundant: "600+ clients" (cross-product, $62bn AUM)
- Foundation Source: 20,000 DAF accounts, cross-product $55bn

DAFRC's 1,512 sponsors (803 community foundations, 606 single-issue, 103 national) give a count frame. However, vendor allocation for community foundations (Foundant CommunitySuite, Blackbaud/MicroEdge FIMS, iPhi legacy and others) is not public. The only asset-weighted statement possible is the administration bound above. The donor-portal layer is somewhat more concentrated than administration, because Ren DFX fronts some sponsors (MS GIFT, BofA) whose administration is otherwise separate.

### 5.4 Custody

**Not computable.**
- Fidelity Charitable's audited statements name **Fidelity Brokerage Services** as primary custodian. That gives a verified lower bound of about **26.2%** of sponsor assets at a single custodian family.
- DAFgiving360 and Vanguard custody arrangements were not stated in the material reviewed. Affiliate custody is plausible but unverified.
- RCF is explicitly "custody and investment neutral". Its assets sit at whatever custodian the advisor uses (Pershing feed TU5; UBS; Ameriprise; others).
- Foundation Source and TIFIN market multi-custody, with BridgeFT supplying data aggregation (not custody).

A custodian HHI would need account-level custody data, which no sponsor publishes.

### 5.5 Distribution

**Not computable.** No market-wide denominator of DAF assets by originating advisor firm exists, and multi-homing (section 4.9) makes firm-level shares non-additive. The one distribution-level fact with scale is historical: Edward Jones's RCF program held more than $2.9bn in 2021 (dated 2021, Ren-sourced). Distribution is best described as **fragmented at the brand level but consolidated at the sponsor/vendor level**. Thirteen-plus brands map to fewer than ten sponsor/vendor stacks in this graph.

### 5.6 Payments and charity verification (descriptive only)

- **Payments:** at the largest sponsors, Stripe/ACH (Fidelity) and PayPal (Vanguard, NPT). Among advisor-oriented challengers, Chariot is the emerging common rail.
- **Charity verification:** the IRS BMF/Pub 78 sit upstream of everyone, and Candid is the main commercial repackager.

No share can be computed because grant-payment volume by rail is not disclosed.

---

## 6. Single points of failure (SPOF)

An edge is marked as a SPOF where failure of that one node or edge would interrupt service for multiple *nominally independent* brands, and no public evidence of an alternative exists.

| # | SPOF | Exposed programs | Mitigants known | Severity basis |
|---|---|---|---|---|
| S1 | **RCF–Ren services contract** (Ren as sole administrator and technology for RCF) | Every RCF-branded program in section 3 (11+ brands), plus RCF administration for Franklin and First Citizens | RCF retains legal authority and assets; custody is spread across advisor custodians | One audited contract; 98% fee share; portal, admin and review all at Ren |
| S2 | **Ren DFX portal platform** | The S1 programs plus MS GIFT, BofA CGF, AEF and community/university portals | Each sponsor's ledger and administration scope differs (unverified) | Same "DFX powered by Ren" platform family across ≥4 legally separate sponsors |
| S3 | **Foundation Source platform for Charityvest** | Charityvest direct, TIAA, Temple, OneGive | Charityvest is the independent legal owner | Single vendor plus single sponsor for all turnkey programs |
| S4 | **Chariot Disbursements / Column N.A.** | TIFIN/GiveClear programs (incl. SEI Charitable Fund), Daffy, Founders Pledge, Groundswell, Charityvest (2026+) | Sponsors retain approval; checks/ACH fallback not documented publicly | Shared payment rail across competing stacks; bank partner concentration |
| S5 | **GiveClear Foundation as sole sponsor for TIFIN Give** | SEI Charitable Fund, AssetMark, Zions, Blue Trust, Ingalls & Snyder, Arlington, Confluence (sponsor for Confluence not confirmed) | None documented | Legal-sponsor SPOF analogous to RCF |
| S6 | **IRS EO BMF / Pub 78** | All eligibility screening | Manual alternative verification (churches etc.) | Upstream data dependency; refresh lag |
| S7 | **Affiliate administrators** (FMR, Schwab, Vanguard) | One sponsor each, but about 49% of assets in total | Large, regulated parents | Not cross-brand SPOFs; vertical integration means sponsor and vendor cannot be separated |

---

## 7. Evidence-quality notes and corrections to prior work

- **Upgrade:** MS GIFT now has a confirmed Ren *technology* edge (DFX portal), in addition to the earlier confirmed RenPSG administration.
- **New programs:** RBC, Janney, Commonwealth/LPL, SEI Giving Fund, MDRT, Fisher, Pershing, Franklin and First Citizens join Edward Jones, Ameriprise, LPL, Northwestern Mutual and UBS on the Ren/RCF list.
- **SEI dual-stack:** SEI distributes both an RCF/Ren program and a GiveClear/TIFIN program. "SEI uses TIFIN" is incomplete.
- **Sources no longer live:** Ren help-centre articles (intercom.help/rengiving/…) for UBS, SEI, Commonwealth and Edward Jones returned 404 on 2026-11-14 and are cited only as search-index evidence. NPT's `/ubsdaf/` page also returned 404; its edge is `historically_confirmed`.
- **Fetch failures:** the Edward Jones product page is JS-rendered (fetch returned only a disclaimer). The Morgan Stanley `/gift` page returned 503, and the BusinessWire and DAFgiving360 pages returned 403. These were corroborated via search-index excerpts and repo records, as noted per edge.
- **Not edges, recorded for context:** press reports say Daffy runs employee equity-donation programs for Anthropic and OpenAI. Daffy's CEO declined to confirm specific clients, so no edge was created.
- **AI edges:**
  - Candid supplies data to Anthropic's Claude for Nonprofits through an MCP connector (Candid press release, 2025-12-02). The direction is data into an AI product. It does not show that Candid or any DAF sponsor uses Claude internally.
  - TIFIN Give's "Louise" uses generative AI from an undisclosed vendor (`unknown`).
  - No DAF sponsor discloses an LLM vendor.

---

## 8. Open questions (priority order)

1. **Ren market-share reconciliation:** which sponsors and assets make up Ren's $175–200bn? Does any of Fidelity Charitable, DAFgiving360, Vanguard Charitable or NPT use a Ren component?
2. **Edward Jones private DAF:** what are its sponsor, administrator and technology? A program circular is needed.
3. **Edward Jones standard program:** a current program circular is needed for fee tiers, the investment manager of the seven portfolios, and an explicit RCF/Ren administration split.
4. **Franklin and First Citizens:** who is the legal sponsor? RCF administers both, but the portals do not name a sponsor.
5. **NPT GivingPoint:** what is its current ledger vendor? Is the historical Stellar/iPhi lineage still relevant?
6. **Goldman Sachs PWM DAF and GS Gives:** who are the administrator and portal vendor?
7. **Custody:** do DAFgiving360 and Vanguard Charitable use affiliate custody? Their audited notes need review.
8. **Chariot:** will Charityvest's expansion to turnkey accounts (TIAA, Temple, OneGive) happen? What fallback rails exist?
9. **Unverified channels:** do Baird, Truist, PNC, US Bank, Envestnet or Merrill have sponsor or vendor edges?
10. **DAFRC data:** the sponsor-level file is needed to replace the bounded CR5/HHI with a census-based HHI.

---

## 9. Data dictionary

### relationship-graph-edges.csv

| Field | Type | Definition |
|---|---|---|
| edge_id | string `E###` | Unique, stable within this file |
| source_entity | string | Entity performing or holding the role. Matches `nodes.entity` |
| source_type | enum | daf_sponsor, branded_daf_program, financial_advisory_firm, technology_vendor, technology_admin_vendor, investment_manager, custodian, custodian_data_api, payment_processor, charity_data_source, charity_data_vendor, ai_platform, investor, nonprofit_daf_program, other |
| target_entity | string | Entity receiving the role or service |
| target_type | enum | Same as source_type |
| relationship_type | enum | `sponsor_of`: legal sponsoring charity of a program. `administers`: back-office/operations. `technology_provider`: software or portal. `custodian`: holds or feeds custody accounts. `investment_manager`: manages pools or portfolios. `distributor_white_label`: brand or channel offering the DAF. `payment_processor`: grant/contribution payment rail. `charity_verification`: eligibility data supply. `ai_provider`: AI model/platform relationship. `acquirer`: ownership via acquisition or parent. `investor`: equity investor. `board_overlap`: shared or former officer/director |
| status | enum | confirmed / historically_confirmed / inferred / disputed / unknown (rules in section 2) |
| evidence_summary | text | What the source says, quoted where short |
| source_url | URL | Primary source used. Every edge has one |
| source_date | text | Publication, document or fiscal date. "live YYYY-MM-DD" means an undated live page observed on that date |
| accessed_date | date | 2026-11-14 if re-fetched this pass; otherwise the original repo access date |
| notes | text | Caveats, fetch failures, scope limits, links to corroborating sources |

### relationship-graph-nodes.csv

| Field | Type | Definition |
|---|---|---|
| entity | string | Canonical name used in edges |
| type | enum | Primary role type (first role seen in the edges) |
| legal_form | text | 501(c)(3), for-profit, program brand, etc. Generic values are marked "not individually verified" |
| EIN_if_charity | text | EIN where sourced (repo or IRS-derived URLs). Blank if not verified |
| parent | text | Owner or controlling entity, or "none legally" for affiliated-brand charities |
| notes | text | Scale figures with period and source caveats |

### Key sources (re-verified 2026-11-14)

- edwardjones.donorfirstx.com
- Edward Jones brochure ANG-13116H-A-E-SR
- renaissancecharitable.org/faqs
- ampf, rbcrcf, cfndaf, sei, mdrt, ft, firstcitizensdaf, tda and msgift .donorfirstx.com
- bofa.donorfirst.org
- reninc.com UBS, LPL, Pershing and Fisher pages
- Janney/Ren PR Newswire release (2024-10-18)
- UBS DAF fact sheet
- SEI release (2026-10-28)
- Fidelity Charitable FY2025 audited statements (note 7; custody note)
- Vanguard Charitable FY2025 audited statements (related-party note)
- ProPublica DAFgiving360 990 summary
- AEF/Ren release (2026-04-08)
- Great Hill/Ren coverage (2025-10-28)
- Chariot partner pages and llms.txt
- Candid–Anthropic release (2025-12-02)
- TIFIN "Louise" release
- CapShift Commonwealth and MS GIFT pages

The full URL list is in the edge file (88 distinct URLs).
