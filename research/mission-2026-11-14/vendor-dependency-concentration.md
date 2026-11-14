# DAF vendor dependency graph and concentration analysis

> **Red-team status (2026-11-14):** independently reviewed in [red-team-wave2b-graph-data-incentives.md](red-team-wave2b-graph-data-incentives.md). The corrections in the final section govern where they conflict with the text.


**Date:** 2026-11-14. **Status:** public-source evidence only. No contracts, SOC reports, production systems or authenticated portals were reviewed.
**Data:** [`data/mission-2026-11-14/relationship-graph-edges.csv`](../../data/mission-2026-11-14/relationship-graph-edges.csv) has 167 edges. [`data/mission-2026-11-14/relationship-graph-nodes.csv`](../../data/mission-2026-11-14/relationship-graph-nodes.csv) has 131 nodes.
**Builds on:** `data/expanded-ecosystem-relationships-2026.csv` (edges L01–L21), `data/expanded-daf-market-map-2026.csv`, the Edward Jones, Ren-distribution, BofA/Morgan Stanley, NPT, Goldman, Charityvest/TIAA, DNS-reconnaissance, technology-audit and startup research files dated 2026-11-11/12.

---

## 1. Summary of findings

1. **Ren is the hub of the graph.** Ren appears in 34 edges and Renaissance Charitable Foundation (RCF) in 22 ([relationship-graph-edges.csv](../../data/mission-2026-11-14/relationship-graph-edges.csv)). Ren's DonorFirstX ("DFX powered by Ren") portal family hosts these branded programs:
   - RCF programs for Edward Jones ([E011: edwardjones.donorfirstx.com](https://edwardjones.donorfirstx.com/)), Ameriprise ([E019: ampf.donorfirstx.com](https://ampf.donorfirstx.com/)), RBC Wealth Management ([E023: rbcrcf.donorfirstx.com](https://rbcrcf.donorfirstx.com/)), Commonwealth/LPL ([E030: reninc.com](https://www.reninc.com/lpl-rcf-daf/); [E033: cfndaf.donorfirstx.com](https://cfndaf.donorfirstx.com/)), SEI (SEI Giving Fund) ([E045: sei.donorfirstx.com](https://sei.donorfirstx.com/)), the MDRT Foundation ([E065: mdrt.donorfirstx.com](https://mdrt.donorfirstx.com/)), Franklin Templeton ([E059: ft.donorfirstx.com](https://ft.donorfirstx.com/)) and First Citizens ([E063: firstcitizensdaf.donorfirstx.com](https://firstcitizensdaf.donorfirstx.com/)).
   - Two programs that RCF does not sponsor: **Morgan Stanley GIFT** ([E078: msgift.donorfirstx.com](https://msgift.donorfirstx.com/)) and the **Bank of America Charitable Gift Fund** ([E082: bofa.donorfirst.org](https://bofa.donorfirst.org/)).

   Most of this was re-verified live on 2026-11-14. The Ameriprise portal is the exception: its fetch did not show the footer, so Ren's role there rests on Ren's Ameriprise guide ([E020: reninc.com](https://www.reninc.com/ampf-rcf-daf/)). **New in this pass:** MS GIFT's donor site (`msgift.donorfirstx.com`) runs on Ren DFX ([E078: msgift.donorfirstx.com](https://msgift.donorfirstx.com/)). Earlier repo work had only documented RenPSG as MS GIFT's back-office administrator ([E077: morganstanley.com](https://morganstanley.com/what-we-do/wealth-management/gift/content-hub)).
2. **Edward Jones (standard program).** On the evidence below, RCF is the legal sponsor, RCF manages and administers the program, and Ren supplies the donor technology.
   - **RCF as sponsor: confirmed.** Edward Jones's own product page says RCF "manages and administers" the fund ([E011: edwardjones.donorfirstx.com](https://edwardjones.donorfirstx.com/)). Sponsor status follows from that page combined with RCF's own description of itself as the sponsoring charity of its programs ([E001: renaissancecharitable.org](https://renaissancecharitable.org/faqs/); [E011: edwardjones.donorfirstx.com](https://edwardjones.donorfirstx.com/)). <!-- CITE-CHECK: no URL for the Edward Jones product page itself is in the repo (JS-rendered); edge E012 points to the 2026 brochure, which per section 3 names neither RCF nor Ren. The quoted "manage and administer" wording is on the EJ portal (E011; confirmed V2B-15). -->
   - **RCF administration: confirmed.** ([E011: edwardjones.donorfirstx.com](https://edwardjones.donorfirstx.com/))
   - **Ren technology: confirmed.** ([E013: edwardjones.donorfirstx.com](https://edwardjones.donorfirstx.com/))
   - **Ren back-office administration for Edward Jones specifically: inferred only.** ([E014: renaissancecharitable.org](https://renaissancecharitable.org/faqs/))
   - **Private DAF:** Edward Jones's newer private DAF (part of its Generations offering) has no publicly identified sponsor, administrator or vendor. ([E017: edwardjones.com](https://www.edwardjones.com/us-en/why-edward-jones/news-media/press-releases/elevated-wealth-management))
3. **Apparently independent competitors share infrastructure.**
   - Seven or more wealth firms are on one sponsor (RCF) and one vendor (Ren). ([E015: edwardjones.com](https://www.edwardjones.com/sites/default/files/dam/jka6ifohxb/res-13116-a.pdf); [E022: ampf.donorfirstx.com](https://ampf.donorfirstx.com/); [E025: rbcrcf.donorfirstx.com](https://rbcrcf.donorfirstx.com/); [E029: prnewswire.com](https://www.prnewswire.com/news-releases/ren-partners-with-janney-montgomery-scott-to-deliver-a-branded-donor-advised-fund-solution-302280662.html); [E032: reninc.com](https://www.reninc.com/lpl-rcf-daf/); [E035: cfndaf.donorfirstx.com](https://cfndaf.donorfirstx.com/); [E041: advisors.ubs.com](https://advisors.ubs.com/mediahandler/media/662455/Donor%20Advised%20Fund%20FactSheet.pdf); [E047: sei.donorfirstx.com](https://sei.donorfirstx.com/); [E071: reninc.com](https://www.reninc.com/rcf-fisher-daf/); [E001: renaissancecharitable.org](https://renaissancecharitable.org/faqs/))
   - Charityvest's turnkey programs (TIAA, Temple, OneGive) ([E128: tiaa.org](https://www.tiaa.org/public/about-tiaa/news-press/press-releases/2026/09-28); [E132: foundationsource.com](https://foundationsource.com/newsroom/press-releases/temple-university-launches-custom-donor-advised-fund-program-in-partnership-with-foundation-source-and-charityvest/); [E134: oneascent.com](https://oneascent.com/wp-content/uploads/sites/25/2025/11/20260811-OAWM-ADV-Part-2A.pdf)) are on Foundation Source. ([E129: tiaa.org](https://www.tiaa.org/public/about-tiaa/news-press/press-releases/2026/09-28); [E133: foundationsource.com](https://foundationsource.com/newsroom/press-releases/temple-university-launches-custom-donor-advised-fund-program-in-partnership-with-foundation-source-and-charityvest/))
   - Chariot Disbursements now serves TIFIN Give/GiveClear ([E139: tifin.com](https://tifin.com/news/tifin-and-chariot-partner-to-transform-grant-payments/19418/); [E138: givechariot.com](https://www.givechariot.com/resources/insights/getting-to-know-tifin-give-a-chariot-disbursements-partner-)) (which also powers the new SEI Charitable Fund) ([E048: seic.com](https://www.seic.com/about-sei/newsroom/sei-launches-sei-charitable-fund-bringing-charitable-giving-advisor-and-client-wealth-experience)), Daffy, Founders Pledge, Groundswell ([E145: givechariot.com](https://www.givechariot.com/resources/insights/getting-to-know-daffy-a-chariot-disbursements-partner); [E146: givechariot.com](https://www.givechariot.com/post/founders-pledge-selects-chariot-to-power-grant-payments); [E147: givechariot.com](https://www.givechariot.com/llms.txt)), and Charityvest (from August 2026). ([E137: givechariot.com](https://givechariot.com/resources/insights/getting-to-know-charityvest-a-new-chariot-disbursements-partner))
   - CapShift serves both MS GIFT and RCF's Commonwealth channel. ([E081: capshift.com](https://capshift.com/wp-content/uploads/2026/05/052026-MS-GIFT-Menu-3.pdf); [E036: capshift.com](https://capshift.com/commonwealth/))
   - IRS EO BMF and Pub 78 data are the upstream source for every charity-eligibility check whose sources are disclosed (Chariot, Candid). ([E153: help.givechariot.com](https://help.givechariot.com/onboarding/trust-and-safety/compliance); [E154: developer.candid.org](https://developer.candid.org/docs/faqs-charity-check))
4. **Fidelity Charitable, DAFgiving360 and Vanguard Charitable are administered by their commercial affiliates.** Each one's audited statements or own disclosure say so ([E099: fidelitycharitable.org](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf); [E108: dafgiving360.org](https://dafgiving360.org/press-release/fiscal-year-2025-results); [E103: vanguardcharitable.org](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf)). Together they hold about **49%** of DAFRC's FY2024 sponsor assets of $327.87bn. ([DAFRC Annual DAF Report, Spring 2026 revision](https://www.dafresearchcollaborative.org/research/annual-daf-report)) <!-- CITE-CHECK: V2B-03 (validation-register-wave2b.csv): period-aligned DAFRC FY2024 shares give ~39%, not ~49%; superseded by red-team correction below -->
5. **Sponsor assets are moderately concentrated.** On a bounded estimate, CR3 is about 58%, CR4 about 66% and CR5 about 70%. HHI is about 1,290 for the listed sponsors, with an upper bound of about 1,370. ([Fidelity Charitable audited statements FY2025](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf); [Vanguard Charitable audited statements FY2025](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf); [DAFRC Annual DAF Report, Spring 2026 revision](https://www.dafresearchcollaborative.org/research/annual-daf-report)) <!-- CITE-CHECK: V2B-01: numerators are June-2025 values divided by a FY2024 denominator holding June-2024 values; period-aligned DAFRC census gives CR3 45.5%, CR5 55.8%, HHI 830; superseded by red-team correction -->
6. **Ren's market-share claim cannot be reconciled with public data.** Ren claims its technology serves ">60%" (website) ([Ren homepage, reviewed 2026-11-14](https://www.reninc.com/)), "approximately half" ($175bn+, Oct 2025) ([Great Hill/Ren release (Pulse 2.0 republication), 2025-10-28](https://pulse2.com/great-hill-partners-announces-strategic-growth-investment-in-donor-advised-fund-platform-ren/)) or "$200bn" (Apr 2026) ([AEF/Ren release, 2026-04-08](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/)) of US DAF assets.
   - Sponsors with public Ren evidence account for only about **8.7%** (RCF, AEF, MS GIFT, BofA CGF). ([DAFRC FY2024 analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)) <!-- CITE-CHECK: V2B-05: DAFRC FY2024 rows give $29.65bn = 9.04% -->
   - Three affiliate-administered giants plus NPT's own GivingPoint platform ([E092: nptrust.org](https://www.nptrust.org/philanthropic-resources/philanthropist/five-things-to-know-about-npt-givingpoint-a-conversation-with-chris-adams-svp-of-it-solutions-and-cybersecurity/)) account for about 66%. That leaves at most about 34% for everyone else. ([DAFRC Annual DAF Report, Spring 2026 revision](https://www.dafresearchcollaborative.org/research/annual-daf-report)) <!-- CITE-CHECK: V2B-03: period-aligned shares give ~52% / ~48%; superseded by red-team correction -->
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
- `historically_confirmed`: confirmed for a past period, with current status unverified. Examples: 2014 iPhi selections ([E160: stellartechsol.com](https://www.stellartechsol.com/sf/Home/ViewArticle/tabid/86/itemId/69/Default.aspx)), the 2020 NPT/Stellar documents ([E091: npt.stellartechsol.com](https://npt.stellartechsol.com/npt/Portals/5/docs/Manage%20Your%20DAF%20Account%20Online%20%28NPT%29.pdf)), an archived Pershing page ([E075: bnymellonwealth.com](https://bnymellonwealth.com/content/pershing/archived/us1/en/what-we-provide/investment-solutions/philanthropy-solutions.html)).
- `inferred`: a reasonable reading from indirect evidence that no party states outright. Examples: a Ren-domain support mailbox implies Ren servicing; a third-party page implies the sponsor.
- `disputed`: sources conflict. This applies to the Ren market-share claim, which is treated in prose because it is not an edge.
- `unknown`: the relationship slot is material and no evidence was found either way. Examples: the sponsor of Edward Jones's private DAF, Goldman PWM's vendor, TIFIN's LLM vendor, Ren–NPT today.

**Evidence handling.**
- Repo sources were reused with their original access date (2026-11-11 or 2026-11-12). ([relationship-graph-edges.csv](../../data/mission-2026-11-14/relationship-graph-edges.csv))
- The consequential ones were re-fetched on 2026-11-14 and carry that access date. In total, 122 of 167 edges were (re)checked this pass. ([relationship-graph-edges.csv](../../data/mission-2026-11-14/relationship-graph-edges.csv))
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
| **Edward Jones Charitable Gift Fund** | **Confirmed.** Portal footer "DFX powered by Ren" | **RCF: confirmed** ("partnered with Edward Jones to manage and administer"). **Ren: inferred** (RCF FAQ: Ren supplies "administrative infrastructure, and operational support" to RCF programs; RCF–Ren audited admin contract; Ren help-centre "EJ DAF opening instructions" seen only in search index) | **Confirmed (by combination).** EJ product page (search excerpt) and portal; RCF FAQ; no separate EJ charity found | edwardjones.donorfirstx.com; renaissancecharitable.org/faqs; EJ brochure ANG-13116H-A-E-SR ([E013: edwardjones.donorfirstx.com](https://edwardjones.donorfirstx.com/); [E012: edwardjones.com](https://www.edwardjones.com/sites/default/files/dam/jka6ifohxb/res-13116-a.pdf); [E001: renaissancecharitable.org](https://renaissancecharitable.org/faqs/)) |
| Edward Jones private DAF (Generations) | Unknown | Unknown | **Unknown** | EJ press release names no sponsor or vendor ([E017: edwardjones.com](https://www.edwardjones.com/us-en/why-edward-jones/news-media/press-releases/elevated-wealth-management)) |
| Ameriprise | Confirmed (Ren guide: nightly feed to Ren, Ren review) | Ren: confirmed | Confirmed (portal: "RCF DAF Program"; "Ameriprise is not affiliated with RCF") | ampf.donorfirstx.com; reninc.com/ampf-rcf-daf ([E019: ampf.donorfirstx.com](https://ampf.donorfirstx.com/); [E020: reninc.com](https://www.reninc.com/ampf-rcf-daf/)) |
| RBC Wealth Management | Confirmed (portal hosted on Ren DFX domain, same template) | Not stated | Confirmed ("RCF Donor-Advised Fund Program for RBC WM Clients") | rbcrcf.donorfirstx.com (**new**) ([E023: rbcrcf.donorfirstx.com](https://rbcrcf.donorfirstx.com/)) |
| Janney | Confirmed ("Ren will power Janney's full-service DAF program at RCF"; integrates with Janney SMART) | Ren: confirmed ("technology and managed services") | Confirmed | PR Newswire, 2024-10-18 (**new**) ([E026: prnewswire.com](https://www.prnewswire.com/news-releases/ren-partners-with-janney-montgomery-scott-to-deliver-a-branded-donor-advised-fund-solution-302280662.html)) |
| LPL (direct channel) | Implied by guide | Ren: confirmed ("Once Ren does a final review…") | Confirmed (RCF account owner) | reninc.com/lpl-rcf-daf ([E030: reninc.com](https://www.reninc.com/lpl-rcf-daf/)) |
| Commonwealth Charitable Fund (LPL trade name) | Confirmed (footer) | Not stated | **Inferred** (CapShift page refers to "your Renaissance Charitable Foundation DAF account") | cfndaf.donorfirstx.com; capshift.com/commonwealth (**new**) ([E033: cfndaf.donorfirstx.com](https://cfndaf.donorfirstx.com/); [E034: capshift.com](https://capshift.com/commonwealth/)) |
| Northwestern Mutual | Implied by Ren-hosted circular | Not stated | Confirmed (RCF program circular with partner-specific fees) | Repo ([E037: reninc.com](https://www.reninc.com/wp-content/uploads/2025/08/NWM-Program-Circular-11-24.pdf)) |
| UBS (RCF option) | Implied | Ren: confirmed ("partners with Ren to bring … technology and servicing") | Confirmed. **UBS is multi-sponsor:** its fact sheet lists Fidelity Charitable, ImpactAssets, NPT and RCF | reninc.com/why-ubs-advisors-choose-rcf; UBS fact sheet (**new**) ([E039: reninc.com](https://www.reninc.com/why-ubs-advisors-choose-rcf/); [E041: advisors.ubs.com](https://advisors.ubs.com/mediahandler/media/662455/Donor%20Advised%20Fund%20FactSheet.pdf)) |
| SEI Giving Fund | Confirmed (footer) | Not stated | Confirmed (RCF contact; GuideStar lists RCF "aka SEI Giving Fund") | sei.donorfirstx.com (**new**). **SEI separately launched the SEI Charitable Fund on 2026-10-28 on TIFIN Give/GiveClear**, so SEI distributes two competing stacks ([E045: sei.donorfirstx.com](https://sei.donorfirstx.com/); [E048: seic.com](https://www.seic.com/about-sei/newsroom/sei-launches-sei-charitable-fund-bringing-charitable-giving-advisor-and-client-wealth-experience)) |
| MDRT Global Gift Fund | Confirmed | Not stated | Confirmed ("offered through RCF") | mdrt.donorfirstx.com (**new**) ([E065: mdrt.donorfirstx.com](https://mdrt.donorfirstx.com/)) |
| Fisher Investments | Implied | Ren: confirmed (final review) | Confirmed | reninc.com/rcf-fisher-daf (**new**) ([E070: reninc.com](https://www.reninc.com/rcf-fisher-daf/)) |
| Pershing-custodied advisors | Implied | Ren: confirmed | Confirmed; Pershing data feed prefix TU5 → **custodian edge** | reninc.com/rcf-pershing-daf (**new**) ([E072: reninc.com](https://www.reninc.com/rcf-pershing-daf/)) |
| Franklin Charitable Giving Program | Confirmed | **RCF: confirmed** ("serviced by RCF" since 2005) | **Unknown**; not stated on the portal | ft.donorfirstx.com (**new**) ([E057: ft.donorfirstx.com](https://ft.donorfirstx.com/)) |
| First Citizens DAF | Confirmed | **RCF: confirmed** (agreement "to provide administrative services"); First-Citizens Bank is investment manager | **Not stated**; RCF described as operator of private-label programs | firstcitizensdaf.donorfirstx.com (**new**) ([E062: firstcitizensdaf.donorfirstx.com](https://firstcitizensdaf.donorfirstx.com/)) |
| TDA-coded RCF portal | Confirmed | Not stated | Confirmed (RCF) | tda.donorfirstx.com. The TD Ameritrade link is **inferred** only from the subdomain and file names ([E068: tda.donorfirstx.com](https://tda.donorfirstx.com/)) |
| **Morgan Stanley GIFT** | **Confirmed (new):** msgift.donorfirstx.com "DFX powered by Ren" | **RenPSG: confirmed** as unaffiliated back-office administrator (MS content hub; repo) | **No.** MS GIFT is its own 501(c)(3) (EIN 52-7082731). CapShift administers its recoverable grants | ([E078: msgift.donorfirstx.com](https://msgift.donorfirstx.com/); [E077: morganstanley.com](https://morganstanley.com/what-we-do/wealth-management/gift/content-hub); [E081: capshift.com](https://capshift.com/wp-content/uploads/2026/05/052026-MS-GIFT-Menu-3.pdf)) |
| **Bank of America CGF** | **Confirmed:** bofa.donorfirst.org "DFX powered by Ren" | Ren: **inferred** (support email @reninc.com) | **No.** Separate charitable trust; BofA Private Bank manages investments | ([E082: bofa.donorfirst.org](https://bofa.donorfirst.org/)) |
| American Endowment Foundation | Confirmed (Ren "technology and services now fully power all" AEF customers, 2026-04-08) | Ren: inferred (scope not enumerated) | **No.** AEF is an independent sponsor | aefonline.org release ([E085: aefonline.org](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/)) |
| NPT | **Unknown.** Only a historical Stellar (2020) link plus Ren's 2023 Stellar acquisition | No | No | Repo rule upheld ([E091: npt.stellartechsol.com](https://npt.stellartechsol.com/npt/Portals/5/docs/Manage%20Your%20DAF%20Account%20Online%20%28NPT%29.pdf); [E092: nptrust.org](https://www.nptrust.org/philanthropic-resources/philanthropist/five-things-to-know-about-npt-givingpoint-a-conversation-with-chris-adams-svp-of-it-solutions-and-cybersecurity/); [E007: reninc.com](https://www.reninc.com/blog/ren-bolsters-philanthropic-tech-services-offerings-with-acquisition-of-stellar-technology-solutions/)) |
| Goldman Sachs (PWM DAF, GS Gives) | Unknown | Unknown | No (separate charities) | No new evidence ([E119: gsbrandguidelines.com](https://www.gsbrandguidelines.com/disclosures/customer-relationship-summary-form-crs/docs/pwm-relationship-guide.pdf); [E120: gspf.goldman.com](https://gspf.goldman.com/gspf/LinkClick.aspx?fileticket=HLXWYjqZAGE%3D&mid=554&tabid=111)) |

**Interpretation.** Ren works through three distinct models:
- **Model A:** RCF sponsors and Ren administers, under a firm's brand. This covers Edward Jones, Ameriprise, RBC, Janney, LPL, Commonwealth, Northwestern Mutual, UBS-RCF, SEI Giving Fund, Fisher and MDRT.
- **Model B:** an independent or bank-affiliated sponsor buys Ren technology and, in some cases, Ren administration. This covers MS GIFT, BofA CGF and AEF.
- **Model C:** RCF acts as administrator to a program whose legal sponsor is not stated. This covers Franklin and First Citizens.

"Customer of Ren" therefore means different things in different rows, and the rows must not be collapsed.

**Edward Jones conclusion.** The public record supports the following for the *standard* Edward Jones Charitable Gift Fund:
- **(a) Ren technology: confirmed.**
- **(b) RCF administration: confirmed.** Ren-performed administration is **inferred**.
- **(c) RCF legal sponsorship: confirmed by combination** of Edward Jones's own product page and RCF's statements.

Edward Jones's 2026 brochure says only that "a third-party administrator is responsible for day-to-day operations" ([E015: edwardjones.com](https://www.edwardjones.com/sites/default/files/dam/jka6ifohxb/res-13116-a.pdf)) and names neither RCF nor Ren. The 2021 figure of more than $2.9bn in RCF-supported assets for Edward Jones (from a Ren guide in the repo) ([Ren/RCF Edward Jones adviser guide 2022 (HTTP 404 on 2026-11-14)](https://www.reninc.com/wp-content/uploads/2022/03/Advisor-Guide-and-FAQ-WH-RCF-2022-1.pdf)) is historical and should not be used as current program assets. Nothing public establishes that the private Generations DAF uses RCF or Ren. <!-- CITE-CHECK: Ren guide for the $2.9bn figure returned HTTP 404 on 2026-11-14; unverifiable -->

---

## 4. Shared-infrastructure findings

**4.1 Many wealth brands, one sponsor, one vendor (RCF + Ren).** At least eleven distribution brands route clients to the same legal sponsor and the same vendor:
- Edward Jones, Ameriprise, RBC, Janney, LPL, Commonwealth/LPL and Northwestern Mutual
- UBS (as one of four options), SEI, Fisher and MDRT

Two more programs (Franklin, First Citizens) are administered by RCF. Program circulars show partner-specific fees ([E037: reninc.com](https://www.reninc.com/wp-content/uploads/2025/08/NWM-Program-Circular-11-24.pdf)), so they compete on price and brand. Their charitable-law risk, grant-approval policy and vendor risk are shared: one sponsor board, one vendor contract (RCF pays Ren 98% of individual fund-holder admin fees, with audited FY2024 payments of $19.23m) ([E002: renaissancecharitable.org](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf)), and one portal codebase family. RCF's FY2024 Schedule D shows $5.91bn across 25,824 DAFs ([RCF Form 990 2024 public disclosure copy](https://renaissancecharitable.org/wp-content/uploads/2026/01/Form-990-Public-Disclosure-Copy-2024-RCF.pdf)). That is small relative to the market but highly concentrated in operational terms.

**4.2 One portal platform across competing sponsors.** DFX/DonorFirst also fronts:
- MS GIFT (about $9.1bn DAF value in FY2024, from a secondary source) ([secondary: philanthropy.org MS GIFT 990 extract](https://philanthropy.org/990/report/527082731/morgan-stanley-global-impact-funding-trust-inc))
- BofA CGF ($5.04bn net assets) ([BofA CGF Form 990 (ProPublica)](https://projects.propublica.org/nonprofits/organizations/46010342))
- AEF ($8.40bn) ([AEF Form 990 (ProPublica)](https://projects.propublica.org/nonprofits/organizations/341747398))
- community and university programs (Gulf Coast CF and Southeast Missouri State, both inferred from search index only) ([E088: gccf.donorfirstx.com](https://gccf.donorfirstx.com/); [E089: semo.donorfirstx.com](https://semo.donorfirstx.com/))

Morgan Stanley, Bank of America and the RCF-branded wirehouses therefore compete for clients through **portals from the same vendor** ([E078: msgift.donorfirstx.com](https://msgift.donorfirstx.com/); [E082: bofa.donorfirst.org](https://bofa.donorfirst.org/); [E085: aefonline.org](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/)). Together these publicly evidenced Ren-linked sponsors hold about $28.5bn (8.7% of DAFRC FY2024 assets). ([DAFRC FY2024 analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx))

**4.3 Foundation Source turnkey cohort.** Charityvest (an independent 501(c)(3)) sponsors the TIAA Wealth Management DAF, the Temple University DAF and OneAscent's OneGive ([E128: tiaa.org](https://www.tiaa.org/public/about-tiaa/news-press/press-releases/2026/09-28); [E132: foundationsource.com](https://foundationsource.com/newsroom/press-releases/temple-university-launches-custom-donor-advised-fund-program-in-partnership-with-foundation-source-and-charityvest/); [E134: oneascent.com](https://oneascent.com/wp-content/uploads/sites/25/2025/11/20260811-OAWM-ADV-Part-2A.pdf)). Foundation Source powers all three. ([E129: tiaa.org](https://www.tiaa.org/public/about-tiaa/news-press/press-releases/2026/09-28); [E133: foundationsource.com](https://foundationsource.com/newsroom/press-releases/temple-university-launches-custom-donor-advised-fund-program-in-partnership-with-foundation-source-and-charityvest/))

Foundation Source's ownership ties run through several parties:
- GTCR owns Foundation Source (2023). ([E121: foundationsource.com](https://foundationsource.com/newsroom/press-releases/gtcr-announces-acquisition-of-foundation-source/))
- Foundation Source acquired Vennfi, PG Calc and Giving Place. ([E122: foundationsource.com](https://foundationsource.com/newsroom/press-releases/foundation-source-acquires-vennfi-the-fintech-powering-donor-advised-fund-charityvest/); [E124: foundationsource.com](https://foundationsource.com/newsroom/press-releases/foundation-source-announces-acquisition-of-pg-calc-leading-provider-of-planned-giving-solutions/); [E123: foundationsource.com](https://foundationsource.com/newsroom/press-releases/foundation-source-acquires-giving-place-platform-for-private-foundations-and-family-offices/))
- A OneAscent fund holds an indirect equity interest in Foundation Source, while OneAscent also distributes OneGive. ([E136: oneascent.com](https://oneascent.com/wp-content/uploads/sites/25/2025/11/20260811-OAWM-ADV-Part-2A.pdf))
- Foundation Source separately serves Northern Trust, but for private foundations, not DAFs. ([E118: northerntrust.com](https://www.northerntrust.com/europe/pr/2025/northern-trust-collaborates-with-foundation-source-to-provide-modern-private-foundation-management-services))

**4.4 Chariot as a disbursement layer.** Chariot Disbursements partners, all company-stated, include:
- TIFIN Give ([E139: tifin.com](https://tifin.com/news/tifin-and-chariot-partner-to-transform-grant-payments/19418/); [E138: givechariot.com](https://www.givechariot.com/resources/insights/getting-to-know-tifin-give-a-chariot-disbursements-partner-)) (and therefore GiveClear programs, including the new SEI Charitable Fund ([E048: seic.com](https://www.seic.com/about-sei/newsroom/sei-launches-sei-charitable-fund-bringing-charitable-giving-advisor-and-client-wealth-experience)), AssetMark, Zions and Confluence channels ([E140: giveclear.org](https://www.giveclear.org/reports-and-financials); [E144: tifin.com](https://tifin.com/category/news/in-the-media)))
- Daffy, Founders Pledge, Groundswell and GoodToday ([E145: givechariot.com](https://www.givechariot.com/resources/insights/getting-to-know-daffy-a-chariot-disbursements-partner); [E146: givechariot.com](https://www.givechariot.com/post/founders-pledge-selects-chariot-to-power-grant-payments); [E147: givechariot.com](https://www.givechariot.com/llms.txt))
- Saint Paul & Minnesota Foundation and Brooklyn Org ([E149: givechariot.com](https://www.givechariot.com/llms.txt); [E150: givechariot.com](https://givechariot.com/resources/product-updates/whats-new-for-grantmakers--may-2026))
- Charityvest, which moves to Chariot from August 2026, "expanding to turnkey partner accounts shortly after" ([E137: givechariot.com](https://givechariot.com/resources/insights/getting-to-know-charityvest-a-new-chariot-disbursements-partner))

If Charityvest expands as stated, **TIFIN/GiveClear and Foundation Source/Charityvest, two otherwise competing advisor-DAF stacks, will share a grant-payment rail.** Chariot's deposit accounts are held at **Column N.A.** ([E152: givechariot.com](https://www.givechariot.com/llms.txt)) DAFgiving360 and Thrivent Charitable appear only as DAFpay (donor checkout) access points ([E109: givechariot.com](https://www.givechariot.com/llms.txt)). That is not evidence that their grants are paid through Chariot.

**4.5 Payment rails among the largest sponsors.**
- Fidelity Charitable uses Stripe and ACH. ([E102: fidelitycharitable.org](https://www.fidelitycharitable.org/nonprofits/faqs.html))
- Vanguard Charitable and NPT both document PayPal Grant Payments. ([E107: vanguardcharitable.org](https://www.vanguardcharitable.org/nonprofit-organizations); [E098: nptrust.org](https://www.nptrust.org/wp-content/uploads/2022/08/Grant-Payments-NPT.pdf))

These are third-party rails underneath otherwise in-house administration.

**4.6 Charity-eligibility data is effectively universal.**
- Chariot builds its database from IRS BMF, Form 990, Pub 78 and OFAC. ([E153: help.givechariot.com](https://help.givechariot.com/onboarding/trust-and-safety/compliance))
- Candid's Charity Check API relies on IRS BMF, Pub 78 and GuideStar data. ([E154: developer.candid.org](https://developer.candid.org/docs/faqs-charity-check))
- Groundswell markets a GuideStar integration. ([E155: groundswell.io](https://www.groundswell.io/products/donor-advised-fund))
- Ren, Edward Jones ("ensure the charity … is approved by the IRS") and Vanguard ("good standing with the IRS") describe IRS-status checks without naming a vendor.

The IRS EO BMF and Pub 78 are therefore the common upstream dependency. Their refresh cadence and coverage gaps (churches, group exemptions) are shared by every downstream checker.

**4.7 CapShift across competitors.** CapShift administers MS GIFT's recoverable-grant offering and provides recoverable-grant access to Commonwealth advisors' RCF DAFs. This is a niche dependency, but it is shared. ([E081: capshift.com](https://capshift.com/wp-content/uploads/2026/05/052026-MS-GIFT-Menu-3.pdf); [E036: capshift.com](https://capshift.com/commonwealth/))

**4.8 Investor and board linkages.**
- TIFIN's backers include J.P. Morgan, Franklin Templeton, SEI, Morningstar and Hamilton Lane. Of these: ([E051: seic.com](https://www.seic.com/about-sei/newsroom/sei-launches-sei-charitable-fund-bringing-charitable-giving-advisor-and-client-wealth-experience))
  - SEI distributes the TIFIN program while also distributing the RCF/Ren SEI Giving Fund. ([E047: sei.donorfirstx.com](https://sei.donorfirstx.com/); [E050: seic.com](https://www.seic.com/about-sei/newsroom/sei-launches-sei-charitable-fund-bringing-charitable-giving-advisor-and-client-wealth-experience))
  - Franklin Templeton distributes an RCF/Ren program. ([E060: ft.donorfirstx.com](https://ft.donorfirstx.com/))
  - Hamilton Lane manages a Vanguard Charitable pool. ([E106: vanguardcharitable.org](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf))
- J.P. Morgan's own DAF is sponsored by NPT. ([E095: jpmorgan.com](https://www.jpmorgan.com/content/dam/jpm/securities/documents/DAFExecutiveSummary.pdf))
- Ren's investors are Bain Capital Tech Opportunities (majority stake, 2023) ([E003: businesswire.com](https://www.businesswire.com/news/home/20230725652545/en/Ren-Secures-Strategic-Growth-Investment-Led-by-Bain-Capital-Tech-Opportunities)), Valeas ([E004: pulse2.com](https://pulse2.com/great-hill-partners-announces-strategic-growth-investment-in-donor-advised-fund-platform-ren/)) and Great Hill Partners (October 2025). ([E005: pulse2.com](https://pulse2.com/great-hill-partners-announces-strategic-growth-investment-in-donor-advised-fund-platform-ren/))
- Ren's board includes **Amy Danforth, former President of Fidelity Charitable** ([E006: pulse2.com](https://pulse2.com/great-hill-partners-announces-strategic-growth-investment-in-donor-advised-fund-platform-ren/)). This is a board-overlap edge only. It is **not** evidence that Fidelity Charitable uses Ren.

**4.9 Distribution multi-homing.** Distribution is not exclusive.
- UBS offers four sponsors. ([E041: advisors.ubs.com](https://advisors.ubs.com/mediahandler/media/662455/Donor%20Advised%20Fund%20FactSheet.pdf))
- SEI offers two stacks. ([E046: sei.donorfirstx.com](https://sei.donorfirstx.com/); [E049: seic.com](https://www.seic.com/about-sei/newsroom/sei-launches-sei-charitable-fund-bringing-charitable-giving-advisor-and-client-wealth-experience))
- LPL reaches RCF through two channels (its direct guide and Commonwealth). ([E030: reninc.com](https://www.reninc.com/lpl-rcf-daf/); [E033: cfndaf.donorfirstx.com](https://cfndaf.donorfirstx.com/))
- BNY's archived Pershing page listed both AEF and RCF. ([E075: bnymellonwealth.com](https://bnymellonwealth.com/content/pershing/archived/us1/en/what-we-provide/investment-solutions/philanthropy-solutions.html))
- Wells Fargo and J.P. Morgan use NPT. ([E093: conversations.wf.com](https://conversations.wf.com/donor-advised-funds); [E095: jpmorgan.com](https://www.jpmorgan.com/content/dam/jpm/securities/documents/DAFExecutiveSummary.pdf))
- Raymond James and Stifel run affiliated sponsors (Raymond James Charitable Endowment Fund, managed by Raymond James Trust ([E114: raymondjames.com](https://www.raymondjames.com/trust/)); Stifel Charitable Inc.) ([E115: stifel.com](https://stifel.com/individual/donor-advised-funds)) whose technology vendors are not public.

No public sponsor or vendor evidence was found for Baird, Truist, PNC, US Bank, Envestnet or Merrill (as a channel distinct from BofA CGF). They are therefore absent from the edge file rather than guessed.

---

## 5. Concentration analysis

Each market is measured separately. HHI and CR figures are on a 0–10,000 HHI scale and in percent.

### 5.1 Assets (sponsor-held DAF assets)

**Denominator.** DAFRC Spring 2026 revised FY2024 sponsor-held DAF assets: **$327.87bn** across 1,512 sponsors ([DAFRC Annual DAF Report, Spring 2026 revision](https://www.dafresearchcollaborative.org/research/annual-daf-report)). This is defensible as a census of Schedule D filers.

**Numerators.** FY2024 values are aligned to IRS tax year 2024. For June fiscal-year sponsors, that is the year ending June 2025. (source: repo inference — analyst period-alignment convention; no primary URL) <!-- CITE-CHECK: V2B-01: DAFRC labels June-FYE sponsors by FYE year (FY2024 = year ending June 2024), so this alignment does not match the denominator -->

| Sponsor | Value ($bn) | Measure | Share of $327.87bn ([DAFRC Annual DAF Report, Spring 2026 revision](https://www.dafresearchcollaborative.org/research/annual-daf-report)) |
|---|---|---|---|
| Fidelity Charitable | 85.86 | audited net assets, 6/30/2025 ([Fidelity Charitable audited statements FY2025](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf)) | 26.2% |
| National Philanthropic Trust | 55.90 | 990 Sch. D DAF value, TY2024 ([NPT Form 990 (ProPublica)](https://projects.propublica.org/nonprofits/organizations/237825575)) | 17.0% |
| DAFgiving360 | 47.42 | 990 net assets, FY6/2025 ([DAFgiving360 Form 990 (ProPublica)](https://projects.propublica.org/nonprofits/organizations/311640316)) | 14.5% |
| Vanguard Charitable | 27.21 | audited net assets, 6/30/2025 ([Vanguard Charitable audited statements FY2025](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf)) | 8.3% |
| GS PWM DAF | 12.6 | Sch. D (secondary, unverified) ([secondary: Nonprofit News Feed GS Philanthropy Fund extract](https://nonprofitnewsfeed.com/daf/goldman-sachs-philanthropy-fund/)) | 3.8% |
| MS GIFT | 9.11 | Sch. D (secondary) ([secondary: philanthropy.org MS GIFT 990 extract](https://philanthropy.org/990/report/527082731/morgan-stanley-global-impact-funding-trust-inc)) | 2.8% |
| AEF | 8.40 | 990 net assets CY2024 ([AEF Form 990 (ProPublica)](https://projects.propublica.org/nonprofits/organizations/341747398)) | 2.6% |
| RCF | 5.91 | Sch. D CY2024 ([RCF Form 990 2024 public disclosure copy](https://renaissancecharitable.org/wp-content/uploads/2026/01/Form-990-Public-Disclosure-Copy-2024-RCF.pdf)) | 1.8% |
| BofA CGF | 5.04 | 990 net assets FY2024 ([BofA CGF Form 990 (ProPublica)](https://projects.propublica.org/nonprofits/organizations/46010342)) | 1.5% |

**Results (bounded estimate):**
- **CR3 ≈ 57.7%**, **CR4 ≈ 66.0%**, **CR5 ≈ 69.8%** (source: repo inference — analyst computation from the shares above; no primary URL) <!-- CITE-CHECK: V2B-01: contradicted by period-aligned DAFRC census (CR3 45.5%, CR5 55.8%) -->
- HHI from the nine listed sponsors ≈ **1,289**. This is a lower bound. (source: repo inference — analyst computation from the shares above; no primary URL) <!-- CITE-CHECK: V2B-01: contradicted by period-aligned DAFRC census (HHI 830) -->
- Upper bound: spreading the remaining 21.5% in blocks no larger than the fifth-largest share (3.84%) gives **HHI ≤ ~1,370**. (source: repo inference — analyst computation from the shares above; no primary URL)

That places sponsor assets in the "moderately concentrated" band of the 2023 Merger Guidelines (1,000–1,800) ([DOJ/FTC 2023 Merger Guidelines](https://www.justice.gov/atr/2023-merger-guidelines)). <!-- CITE-CHECK: V2B-01: on period-aligned data sponsor assets are unconcentrated (<1,000) at all-sponsor level -->

**Caveats.**
- Net assets and Schedule D DAF value are mixed measures. Fidelity's and DAFgiving360's net assets may include small non-DAF balances.
- The GS and MS GIFT values are secondary extracts.
- An unlisted sponsor larger than $12.6bn ([secondary: Nonprofit News Feed GS Philanthropy Fund extract](https://nonprofitnewsfeed.com/daf/goldman-sachs-philanthropy-fund/)) would raise CR5. None is known in the repo, but the full DAFRC sponsor file has not been downloaded.
- Treat these figures as ±2 percentage points (CR) and ±100 (HHI).

Grants, as a cross-check (periods differ, so these are not combined into an index): Fidelity CY2025 $18.3bn ([Fidelity Charitable 2026 Giving Report](https://www.fidelitycharitable.org/insights/2026-giving-report.html)); DAFgiving360 FY2026 >$10bn ([DAFgiving360 FY2026 results](https://www.dafgiving360.org/press-release/fiscal-year-2026-results)); NPT FY2025 $6.44bn ([NPT annual report FY2025](https://www.nptrust.org/annual-reports/npt-annual-report/)); Vanguard CY2025 $3.96bn ([Vanguard Charitable 2025 annual report](https://www.vanguardcharitable.org/2025annualreport)). DAFRC FY2024 total grants were $64.60bn ([DAFRC Annual DAF Report, Spring 2026 revision](https://www.dafresearchcollaborative.org/research/annual-daf-report)).

### 5.2 Administration (who runs the back office)

**Defensible numerator (lower bounds, as a share of $327.87bn):** ([DAFRC Annual DAF Report, Spring 2026 revision](https://www.dafresearchcollaborative.org/research/annual-daf-report))
- **Affiliate-administered:** FMR for Fidelity Charitable (26.2%) ([E099: fidelitycharitable.org](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf)), Schwab subsidiaries for DAFgiving360 (14.5%) ([E108: dafgiving360.org](https://dafgiving360.org/press-release/fiscal-year-2025-results)), The Vanguard Group for Vanguard Charitable (8.3%) ([E103: vanguardcharitable.org](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf)). Together: **49.0%**, held by three separate administrators. <!-- CITE-CHECK: V2B-03: period-aligned total ~39% -->
- **Self-administered with the vendor unknown:** NPT, 17.0% ([NPT Form 990 (ProPublica)](https://projects.propublica.org/nonprofits/organizations/237825575)). GivingPoint's developer is not public. ([E092: nptrust.org](https://www.nptrust.org/philanthropic-resources/philanthropist/five-things-to-know-about-npt-givingpoint-a-conversation-with-chris-adams-svp-of-it-solutions-and-cybersecurity/)) <!-- CITE-CHECK: V2B-03: period-aligned NPT share 12.85% -->
- **Ren, publicly evidenced:** RCF, AEF, MS GIFT and BofA CGF, about **8.7%** ([DAFRC FY2024 analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)). Ren's role is technology in every case. Administration is confirmed for RCF and MS GIFT and inferred for AEF and BofA. ([E002: renaissancecharitable.org](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf); [E077: morganstanley.com](https://morganstanley.com/what-we-do/wealth-management/gift/content-hub); [E078: msgift.donorfirstx.com](https://msgift.donorfirstx.com/); [E082: bofa.donorfirst.org](https://bofa.donorfirst.org/); [E085: aefonline.org](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/)) <!-- CITE-CHECK: V2B-05 (9.04% on DAFRC rows) and V2B-16 (AEF release states administrative services) qualify this line -->
- **Other affiliated in-house (not quantified here):** Raymond James Trust, BNY Mellon N.A. and Stifel. ([E114: raymondjames.com](https://www.raymondjames.com/trust/); [E113: causeiq.com](https://causeiq.com/organizations/bny-mellon-charitable-gift-fund,300748315); [E115: stifel.com](https://stifel.com/individual/donor-advised-funds))
- **Foundation Source (Charityvest):** about $0.22bn (self-reported), about 0.07%. ([Charityvest 2025 results release, 2026-02-11](https://foundationsource.com/newsroom/press-releases/charityvest-reports-record-2025-charitable-giving-more-than-doubling-contributions-and-grants/))

**HHI: not computable as a point estimate.** About 34% of assets have no identified administrator. A bounded range, assuming each named administrator is distinct: (source: repo inference — analyst computation from the shares above; no primary URL)
- If Ren's share is only its evidenced 8.7% and the unknown 25% is atomised: HHI ≈ **1,330**. (source: repo inference — analyst computation from the shares above; no primary URL)
- If the entire unidentified 34% were Ren: HHI ≈ **2,410**, which is highly concentrated. (source: repo inference — analyst computation from the shares above; no primary URL)

**Ren's own claims cannot both hold alongside the disclosures above.** Ren claims ">60%" or "approximately half" of DAF assets on "Ren technology" ($175bn, Oct 2025; $200bn, Apr 2026) ([Ren homepage, reviewed 2026-11-14](https://www.reninc.com/); [Great Hill/Ren release (Pulse 2.0 republication), 2025-10-28](https://pulse2.com/great-hill-partners-announces-strategic-growth-investment-in-donor-advised-fund-platform-ren/); [AEF/Ren release, 2026-04-08](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/)). That is 53–61% of the FY2024 denominator ([DAFRC Annual DAF Report, Spring 2026 revision](https://www.dafresearchcollaborative.org/research/annual-daf-report)). Fidelity, DAFgiving360 and Vanguard disclose affiliate administration ([E099: fidelitycharitable.org](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf); [E108: dafgiving360.org](https://dafgiving360.org/press-release/fiscal-year-2025-results); [E103: vanguardcharitable.org](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf)), and NPT presents GivingPoint as its own platform ([E092: nptrust.org](https://www.nptrust.org/philanthropic-resources/philanthropist/five-things-to-know-about-npt-givingpoint-a-conversation-with-chris-adams-svp-of-it-solutions-and-cybersecurity/)). If those four are excluded, at most about 34% remains.

The claim therefore requires at least one of the following:
- Ren components (for example, technology modules, payments or data) inside one or more of the four largest sponsors, none of which is publicly disclosed
- a numerator that counts non-DAF charitable assets, such as community-foundation endowments on iPhi
- a different measure (for example, "rely on" any Ren component) or a later, larger denominator

**Status: disputed.** Do not cite Ren's percentage as a market share.

### 5.3 Software

**Not computable.** No denominator of sponsor technology spend or seats exists, and vendor counts are self-reported across different units:
- Ren: ">150 DAF programs" ([Ren homepage, reviewed 2026-11-14](https://www.reninc.com/))
- Foundant: "600+ clients" (cross-product, $62bn AUM) ([Foundant CommunitySuite page](https://www.foundant.com/products/communitysuite/)) <!-- CITE-CHECK: Foundant CommunitySuite page (breadth doc S10) states "700+ community foundations" and $62B AUM; "600+ clients" not found in a cited source -->
- Foundation Source: 20,000 DAF accounts, cross-product $55bn ([Foundation Source DAF OS product brief](https://foundationsource.com/resources/product-briefs/the-modern-operating-system-for-donor-advised-funds/))

DAFRC's 1,512 sponsors (803 community foundations, 606 single-issue, 103 national) ([DAFRC Annual DAF Report, Spring 2026 revision](https://www.dafresearchcollaborative.org/research/annual-daf-report)) give a count frame. However, vendor allocation for community foundations (Foundant CommunitySuite, Blackbaud/MicroEdge FIMS, iPhi legacy and others) is not public. The only asset-weighted statement possible is the administration bound above. The donor-portal layer is somewhat more concentrated than administration, because Ren DFX fronts some sponsors (MS GIFT, BofA) whose administration is otherwise separate.

### 5.4 Custody

**Not computable.**
- Fidelity Charitable's audited statements name **Fidelity Brokerage Services** as primary custodian. That gives a verified lower bound of about **26.2%** of sponsor assets at a single custodian family. ([E100: fidelitycharitable.org](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf))
- DAFgiving360 and Vanguard custody arrangements were not stated in the material reviewed. Affiliate custody is plausible but unverified.
- RCF is explicitly "custody and investment neutral" ([E019: ampf.donorfirstx.com](https://ampf.donorfirstx.com/); [E023: rbcrcf.donorfirstx.com](https://rbcrcf.donorfirstx.com/)). Its assets sit at whatever custodian the advisor uses (Pershing feed TU5 ([E073: reninc.com](https://www.reninc.com/rcf-pershing-daf/)); UBS ([E041: advisors.ubs.com](https://advisors.ubs.com/mediahandler/media/662455/Donor%20Advised%20Fund%20FactSheet.pdf)); Ameriprise ([E021: reninc.com](https://www.reninc.com/ampf-rcf-daf/)); others).
- Foundation Source and TIFIN market multi-custody, with BridgeFT supplying data aggregation (not custody). ([E127: foundationsource.com](https://foundationsource.com/newsroom/press-releases/foundation-source-elevates-turnkey-daf-platform-with-advisor-branded-multi-custodial-flexibility/))

A custodian HHI would need account-level custody data, which no sponsor publishes.

### 5.5 Distribution

**Not computable.** No market-wide denominator of DAF assets by originating advisor firm exists, and multi-homing (section 4.9) makes firm-level shares non-additive. The one distribution-level fact with scale is historical: Edward Jones's RCF program held more than $2.9bn in 2021 (dated 2021, Ren-sourced) ([Ren/RCF Edward Jones adviser guide 2022 (HTTP 404 on 2026-11-14)](https://www.reninc.com/wp-content/uploads/2022/03/Advisor-Guide-and-FAQ-WH-RCF-2022-1.pdf)). Distribution is best described as **fragmented at the brand level but consolidated at the sponsor/vendor level**. Thirteen-plus brands map to fewer than ten sponsor/vendor stacks in this graph. <!-- CITE-CHECK: source guide returned HTTP 404 on 2026-11-14; figure unverifiable (edward-jones research file V1-05) -->

### 5.6 Payments and charity verification (descriptive only)

- **Payments:** at the largest sponsors, Stripe/ACH (Fidelity) ([E102: fidelitycharitable.org](https://www.fidelitycharitable.org/nonprofits/faqs.html)) and PayPal (Vanguard, NPT) ([E107: vanguardcharitable.org](https://www.vanguardcharitable.org/nonprofit-organizations); [E098: nptrust.org](https://www.nptrust.org/wp-content/uploads/2022/08/Grant-Payments-NPT.pdf)). Among advisor-oriented challengers, Chariot is the emerging common rail.
- **Charity verification:** the IRS BMF/Pub 78 sit upstream of everyone, and Candid is the main commercial repackager.

No share can be computed because grant-payment volume by rail is not disclosed.

---

## 6. Single points of failure (SPOF)

An edge is marked as a SPOF where failure of that one node or edge would interrupt service for multiple *nominally independent* brands, and no public evidence of an alternative exists.

| # | SPOF | Exposed programs | Mitigants known | Severity basis |
|---|---|---|---|---|
| S1 | **RCF–Ren services contract** (Ren as sole administrator and technology for RCF) | Every RCF-branded program in section 3 (11+ brands), plus RCF administration for Franklin and First Citizens | RCF retains legal authority and assets; custody is spread across advisor custodians | One audited contract; 98% fee share; portal, admin and review all at Ren ([E002: renaissancecharitable.org](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf); [E001: renaissancecharitable.org](https://renaissancecharitable.org/faqs/)) |
| S2 | **Ren DFX portal platform** | The S1 programs plus MS GIFT, BofA CGF, AEF and community/university portals | Each sponsor's ledger and administration scope differs (unverified) | Same "DFX powered by Ren" platform family across ≥4 legally separate sponsors ([E013: edwardjones.donorfirstx.com](https://edwardjones.donorfirstx.com/); [E078: msgift.donorfirstx.com](https://msgift.donorfirstx.com/); [E082: bofa.donorfirst.org](https://bofa.donorfirst.org/); [E085: aefonline.org](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/)) |
| S3 | **Foundation Source platform for Charityvest** | Charityvest direct, TIAA, Temple, OneGive | Charityvest is the independent legal owner | Single vendor plus single sponsor for all turnkey programs ([E125: guide.charityvest.org](https://guide.charityvest.org/about-our-venture/charityvest-%2B-vennfi)) |
| S4 | **Chariot Disbursements / Column N.A.** | TIFIN/GiveClear programs (incl. SEI Charitable Fund), Daffy, Founders Pledge, Groundswell, Charityvest (2026+) | Sponsors retain approval; checks/ACH fallback not documented publicly | Shared payment rail across competing stacks; bank partner concentration ([E152: givechariot.com](https://www.givechariot.com/llms.txt); [E139: tifin.com](https://tifin.com/news/tifin-and-chariot-partner-to-transform-grant-payments/19418/); [E145: givechariot.com](https://www.givechariot.com/resources/insights/getting-to-know-daffy-a-chariot-disbursements-partner); [E146: givechariot.com](https://www.givechariot.com/post/founders-pledge-selects-chariot-to-power-grant-payments); [E137: givechariot.com](https://givechariot.com/resources/insights/getting-to-know-charityvest-a-new-chariot-disbursements-partner)) |
| S5 | **GiveClear Foundation as sole sponsor for TIFIN Give** | SEI Charitable Fund, AssetMark, Zions, Blue Trust, Ingalls & Snyder, Arlington, Confluence (sponsor for Confluence not confirmed) | None documented | Legal-sponsor SPOF analogous to RCF ([E048: seic.com](https://www.seic.com/about-sei/newsroom/sei-launches-sei-charitable-fund-bringing-charitable-giving-advisor-and-client-wealth-experience); [E140: giveclear.org](https://www.giveclear.org/reports-and-financials); [E144: tifin.com](https://tifin.com/category/news/in-the-media)) |
| S6 | **IRS EO BMF / Pub 78** | All eligibility screening | Manual alternative verification (churches etc.) | Upstream data dependency; refresh lag ([E153: help.givechariot.com](https://help.givechariot.com/onboarding/trust-and-safety/compliance); [E154: developer.candid.org](https://developer.candid.org/docs/faqs-charity-check)) |
| S7 | **Affiliate administrators** (FMR, Schwab, Vanguard) | One sponsor each, but about 49% of assets in total | Large, regulated parents | Not cross-brand SPOFs; vertical integration means sponsor and vendor cannot be separated ([E099: fidelitycharitable.org](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf); [E108: dafgiving360.org](https://dafgiving360.org/press-release/fiscal-year-2025-results); [E103: vanguardcharitable.org](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf)) |

---

## 7. Evidence-quality notes and corrections to prior work

- **Upgrade:** MS GIFT now has a confirmed Ren *technology* edge (DFX portal), in addition to the earlier confirmed RenPSG administration.
- **New programs:** RBC, Janney, Commonwealth/LPL, SEI Giving Fund, MDRT, Fisher, Pershing, Franklin and First Citizens join Edward Jones, Ameriprise, LPL, Northwestern Mutual and UBS on the Ren/RCF list.
- **SEI dual-stack:** SEI distributes both an RCF/Ren program and a GiveClear/TIFIN program. "SEI uses TIFIN" is incomplete.
- **Sources no longer live:** Ren help-centre articles (intercom.help/rengiving/…) for UBS, SEI, Commonwealth and Edward Jones returned 404 on 2026-11-14 and are cited only as search-index evidence. NPT's `/ubsdaf/` page ([E044: wealthmanagement.com](https://www.wealthmanagement.com/financial-planning/ubs-wealth-management-and-the-national-philanthropic-trust-launch-the-first-ubs-donor-advised-fund)) also returned 404; its edge is `historically_confirmed`.
- **Fetch failures:** the Edward Jones product page is JS-rendered (fetch returned only a disclaimer). The Morgan Stanley `/gift` page returned 503, and the BusinessWire and DAFgiving360 pages returned 403. These were corroborated via search-index excerpts and repo records, as noted per edge.
- **Not edges, recorded for context:** press reports say Daffy runs employee equity-donation programs for Anthropic and OpenAI. Daffy's CEO declined to confirm specific clients, so no edge was created.
- **AI edges:**
  - Candid supplies data to Anthropic's Claude for Nonprofits through an MCP connector (Candid press release, 2025-12-02) ([E156: candid.org](https://candid.org/press/candid-partners-with-anthropic-to-bring-trusted-data-to-claude-for-nonprofits/)). The direction is data into an AI product. It does not show that Candid or any DAF sponsor uses Claude internally.
  - TIFIN Give's "Louise" uses generative AI from an undisclosed vendor (`unknown`). ([E157: tifin.com](https://tifin.com/news/tifin-give-launches-louise-the-ai-platform-for-philanthropy/19124/))
  - No DAF sponsor discloses an LLM vendor.

---

## 8. Open questions (priority order)

1. **Ren market-share reconciliation:** which sponsors and assets make up Ren's $175–200bn? Does any of Fidelity Charitable, DAFgiving360, Vanguard Charitable or NPT use a Ren component? ([Great Hill/Ren release (Pulse 2.0 republication), 2025-10-28](https://pulse2.com/great-hill-partners-announces-strategic-growth-investment-in-donor-advised-fund-platform-ren/); [AEF/Ren release, 2026-04-08](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/))
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

- edwardjones.donorfirstx.com ([E013: edwardjones.donorfirstx.com](https://edwardjones.donorfirstx.com/))
- Edward Jones brochure ANG-13116H-A-E-SR ([E012: edwardjones.com](https://www.edwardjones.com/sites/default/files/dam/jka6ifohxb/res-13116-a.pdf))
- renaissancecharitable.org/faqs ([E001: renaissancecharitable.org](https://renaissancecharitable.org/faqs/))
- ampf, rbcrcf, cfndaf, sei, mdrt, ft, firstcitizensdaf, tda and msgift .donorfirstx.com ([E019: ampf.donorfirstx.com](https://ampf.donorfirstx.com/); [E023: rbcrcf.donorfirstx.com](https://rbcrcf.donorfirstx.com/); [E033: cfndaf.donorfirstx.com](https://cfndaf.donorfirstx.com/); [E045: sei.donorfirstx.com](https://sei.donorfirstx.com/); [E065: mdrt.donorfirstx.com](https://mdrt.donorfirstx.com/); [E059: ft.donorfirstx.com](https://ft.donorfirstx.com/); [E063: firstcitizensdaf.donorfirstx.com](https://firstcitizensdaf.donorfirstx.com/); [E068: tda.donorfirstx.com](https://tda.donorfirstx.com/); [E078: msgift.donorfirstx.com](https://msgift.donorfirstx.com/))
- bofa.donorfirst.org ([E082: bofa.donorfirst.org](https://bofa.donorfirst.org/))
- reninc.com UBS, LPL, Pershing and Fisher pages ([E040: reninc.com](https://www.reninc.com/why-ubs-advisors-choose-rcf/); [E030: reninc.com](https://www.reninc.com/lpl-rcf-daf/); [E072: reninc.com](https://www.reninc.com/rcf-pershing-daf/); [E070: reninc.com](https://www.reninc.com/rcf-fisher-daf/))
- Janney/Ren PR Newswire release (2024-10-18) ([E026: prnewswire.com](https://www.prnewswire.com/news-releases/ren-partners-with-janney-montgomery-scott-to-deliver-a-branded-donor-advised-fund-solution-302280662.html))
- UBS DAF fact sheet ([E041: advisors.ubs.com](https://advisors.ubs.com/mediahandler/media/662455/Donor%20Advised%20Fund%20FactSheet.pdf))
- SEI release (2026-10-28) ([E048: seic.com](https://www.seic.com/about-sei/newsroom/sei-launches-sei-charitable-fund-bringing-charitable-giving-advisor-and-client-wealth-experience))
- Fidelity Charitable FY2025 audited statements (note 7; custody note) ([E099: fidelitycharitable.org](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf))
- Vanguard Charitable FY2025 audited statements (related-party note) ([E103: vanguardcharitable.org](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf))
- ProPublica DAFgiving360 990 summary ([DAFgiving360 Form 990 (ProPublica)](https://projects.propublica.org/nonprofits/organizations/311640316))
- AEF/Ren release (2026-04-08) ([E085: aefonline.org](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/))
- Great Hill/Ren coverage (2025-10-28) ([E005: pulse2.com](https://pulse2.com/great-hill-partners-announces-strategic-growth-investment-in-donor-advised-fund-platform-ren/))
- Chariot partner pages and llms.txt ([E147: givechariot.com](https://www.givechariot.com/llms.txt); [E145: givechariot.com](https://www.givechariot.com/resources/insights/getting-to-know-daffy-a-chariot-disbursements-partner))
- Candid–Anthropic release (2025-12-02) ([E156: candid.org](https://candid.org/press/candid-partners-with-anthropic-to-bring-trusted-data-to-claude-for-nonprofits/))
- TIFIN "Louise" release ([E157: tifin.com](https://tifin.com/news/tifin-give-launches-louise-the-ai-platform-for-philanthropy/19124/))
- CapShift Commonwealth and MS GIFT pages ([E036: capshift.com](https://capshift.com/commonwealth/); [E081: capshift.com](https://capshift.com/wp-content/uploads/2026/05/052026-MS-GIFT-Menu-3.pdf))

The full URL list is in the edge file (88 distinct URLs).

## Red-team corrections (wave 2B, 2026-11-14) — governing
- **§1 item 4.** Replace "Together they hold about **49%**" with: "Together they held about **39%** of DAFRC's FY2024 sponsor assets (period-aligned: June-2024 values for June-FYE sponsors)." ([Fidelity Charitable audited statements FY2025](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf); [Vanguard Charitable audited statements FY2025](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf); [DAFRC FY2024 analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx))
- **§1 item 5.** Replace it with: "**Sponsor assets are unconcentrated at the all-sponsor level and moderately concentrated among national sponsors.** DAFRC FY2024 census: CR3 45.5%, CR5 55.8%, HHI 830; national-only CR3 63.2%, HHI 1,566 (see `derived-metrics.csv`)." ([DAFRC FY2024 analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx))
- **§1 item 6 and §5.2.**
  - Replace "about 66%. That leaves at most about 34%" with "about 52%. That leaves at most about 48%". ([Fidelity Charitable audited statements FY2025](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf); [Vanguard Charitable audited statements FY2025](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf))
  - Replace '"$200bn" (Apr 2026) of US DAF assets' with '"approximately $200 billion of donor-advised funds and other charitable assets" (AEF/Ren release, 2026-04-08; not a DAF-only figure)'. ([AEF/Ren release, 2026-04-08](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/))
  - Add: "The residual 47.8% plus NPT (12.9%) ≈ 60.6%, matching Ren's '60%+'; this would hold only if Ren counts NPT (Stellar/iPhi lineage) and nearly all other sponsors. Unverified." ([Ren homepage, reviewed 2026-11-14](https://www.reninc.com/))
- **§5.1 table.**
  - Replace the June-2025 values with the DAFRC FY2024 values: Fidelity 66.20, NPT 42.12, DAFgiving360 40.94, Vanguard 21.95, GS 11.84, SVCF 9.58, AEF 9.48, MS GIFT 9.43, RCF 5.63, NCF 5.46, BofA 5.11. ([DAFRC FY2024 analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx); [Fidelity Charitable audited statements FY2025](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf))
  - Delete the "±2 pp/±100" line.
  - Delete the caveat "the full DAFRC sponsor file has not been downloaded".
- **§4.1.** Replace "RCF's FY2024 Schedule D shows $5.91bn across 25,824 DAFs" with "RCF's FY2024 audited net assets were $5.90bn across 25,824 DAFs (DAFRC's Schedule D row is imputed at $5.63bn / 22,366)". ([RCF audited statements FY2024](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf); [DAFRC FY2024 analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx))
- **Edge E086.** Change `inferred` to `confirmed`. Add evidence: AEF 2025-07-23: "Ren will serve as a trusted technology and administrative services partner". Update §5.2 to read "Administration is confirmed for RCF, MS GIFT and AEF". ([AEF announcement, 2025-07-23](https://www.aefonline.org/?p=14296))
- **Edge E151.** Note "DAFpay checkout access only". Either retype it or add `scope=donor_checkout`.
- **§4 / S7.** Change "Vanguard" to "Vanguard (hybrid: Vanguard Group provides recordkeeping/admin support for $4.0m; admin fee funds Vanguard Charitable's own operations)". ([Vanguard Charitable audited statements FY2025](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf))
