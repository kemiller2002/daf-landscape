# Competitive History Timelines: DAF Technology Providers and Sponsors, 1987–2026

**Research date:** November 14, 2026. **Status:** public-source desk research. This is not an audit or an exhaustive census.

**Datasets:**
- [company-timeline-events.csv](../../data/mission-2026-11-14/company-timeline-events.csv): 195 dated events across 20 company labels (16 company groups).
- [announced-vs-delivered.csv](../../data/mission-2026-11-14/announced-vs-delivered.csv): 39 announced capabilities, each with the later evidence found.

**Builds on:**
- [historical lifecycle ledger](../historical-daf-sponsor-technology-lifecycle-2011-2026.md)
- [technology audit and provider exits](../daf-technology-audit-and-provider-exits-2026-11-11.md)
- [Ren contract durability](../ren-contract-durability-concentration-2026-11-11.md)
- [Ren/TIFIN/Chariot deep dive](../ren-tifin-chariot-deep-dive-2026-11-11.md)
- [startups scan](../startups-and-emerging-competitors-2026-11-12.md)

Events taken from those files are tagged `prior_repo_source(<ID>)` so the original source stays traceable. They are not counted as new findings.

---

## 1. Summary

1. **Payment rails are the most active area of change, and providers are dividing into camps.** Between 2014 and 2026 the sponsors studied adopted four different electronic grant rails:
   - Fidelity Charitable: its own EFT (2014), later Stripe and ACH.
   - PayPal Grant Payments (2022): NPT, Vanguard Charitable and, until 2026, Charityvest.
   - Ren's Rapid Disbursement Engine (2023), which uses each sponsor's own bank rails.
   - Chariot Disbursements (2025): Daffy, Charityvest, TIFIN/AssetMark, Groundswell, Founders Pledge and others.

   The only observed switch between rails is Charityvest moving from PayPal to Chariot in August 2026. Chariot's goal of becoming a "ubiquitous payment layer" is only **partially** met, because none of the three largest sponsors is a documented Chariot Disbursements user. *Confidence: medium.*

2. **Private-equity ownership changes are followed within days to months by leadership turnover, acquisitions and launches.**
   - **Foundation Source:** GTCR acquired it on Sept. 13, 2023, and a new CEO was named six days later. Four acquisitions followed in about 17 months: PG Calc, Vennfi, Giving Place and Pacific Foundation Services.
   - **Ren:** it launched the Rapid Disbursement Engine four months after the 2023 Bain/Valeas investment. A second private-equity firm, Great Hill, invested in Oct. 2025.

   What we cannot observe is how this affected customers: retention, service quality and pricing. *Confidence: high for the sequence; unknown for the effects.*

3. **How well announcements are backed by later evidence differs by company, not by company size.**
   - **Daffy** (5 of 5 announcements delivered) and **Chariot's Disbursements line** have the clearest trails from announcement to documentation to customer use.
   - **TIFIN Give** announces features most often. Five of its eight tracked announcements have documented delivery. The remaining gaps are mainly vendor-only claims, such as the Louise AI.
   - **Ren** and **Foundation Source** make broad capability claims (daily unitization, DAF OS) with little public delivery evidence. Both also have an unresolved or conflicting assurance or naming record.

   Under the evidence rule used here, none of these gaps proves non-delivery.

4. **Pricing history follows two directions.**
   - **Incumbents lowered access barriers.** Fidelity Charitable removed its $5,000 minimum on Sept. 30, 2020. Schwab Charitable removed its minimums on Nov. 10, 2020. Vanguard Charitable's $25,000 minimum appears unchanged.
   - **Challengers that started with "zero" or flat fees added fee tiers as they moved upmarket.**
     - Daffy started with $3/$5/$20 tiers and now has a $40 tier that switches on automatically when certain features are used.
     - Charityvest was described as having "zero fees" in 2020. In 2022 its invested-account fee topped out at 0.45%. Its 2026 schedule charges 0.60% on the first $500k.
   - The date of the Charityvest fee change has not been established, so **it cannot be attributed to the 2024 acquisition.**

5. **Ren's own historical account and metrics drift over time.** These are diligence flags, not misconduct findings:
   - Ren's timeline dates the Ren rename to 2021, but the dated press release is March 22, 2022.
   - The timeline pairs the RenPSG rename with the Crown acquisition, but the rename came about five months earlier.
   - Scale claims move between $175B+ and $200B+.
   - SOC 2 is described as Type II in July 2025 and Type 1 in April 2026.
   - The charity network is described as 140k (2023), as 93k "in network" (2026), and as "over a million charities annually" (2026).

---

## 2. Method and evidence classes

- **Sources.** Wherever possible we used first-party pages: press releases, help centers, developer changelogs and sponsor FAQs. Each event row records which of four methods produced it:
  - `fetched_full_text`: page read in full. 105 rows.
  - `search_result_summary`: a primary or secondary URL surfaced by search whose content was summarized but not fully fetched, often because the site returned 403. 39 rows.
  - `prior_repo_source`: carried forward from earlier work in this repository. 31 rows.
  - `archive_availability_api`: 20 rows. **Wayback Machine page content could not be retrieved from this environment.** Only the archive.org availability API worked. Archived rows therefore prove only that **a snapshot exists at a timestamp** (HTTP 200). They do not show what the page said. The task suggested reading archived pricing pages; that could not be done. The snapshot URLs are recorded so a later session with archive access can read them, for example the Daffy membership page on 2023-01-27 and 2025-01-07, and Fidelity's "What it costs" page on 2020-05-31 and 2020-10-28.
- **Evidence classes.**
  - `primary` (156): a company, sponsor or regulator speaking about itself or its own customers.
  - `secondary` (19): trade press or deal databases.
  - `archived` (20).
- **Confidence.** 105 rows are high, 80 medium and 10 low.
- **Delivery status.**
  - `evidence_of_delivery`: later public documentation, a changelog entry, a customer statement or a usage metric shows the capability exists.
  - `partial`: the capability exists for some scope, or the only evidence is the vendor's own assertion.
  - `no_public_evidence_yet`: none found, **which is not proof of non-delivery**.
  - `contradicted`: a later primary statement conflicts with the claim.
- **Limits.** The web-search budget for this session ran out partway through. GiveClear Direct, Chariot's DAFpay launch date, NPT's international program and Givinga's funding were not searched further. Several first-party sites, including tifin.com, businesswire.com and dafgiving360.org, blocked automated fetching, so those items rely on search summaries or earlier captures.

---

## 3. Company timelines

### 3.1 Ren (Renaissance → RenPSG → Ren), with Renaissance Charitable Foundation

| Date | Event | Type |
|---|---|---|
| 1987 | Renaissance, Inc. founded to administer charitable trusts | positioning |
| 2000 | DAF offering launched; **Renaissance Charitable Foundation (RCF)** formed as sponsor | product launch |
| 2005 / 2010 | First institutional DAF program; first multi-gift institutional program | product launch |
| 2011-02-08 | Acquires Blackbaud's DAF platform (Giving Capital/Kintera lineage) | acquisition |
| 2016-05-23 | Rebrands as **RenPSG**; ">$6.3B" serviced; CEO E. Edward Thompson | positioning |
| 2016-10-24 | Agreement to acquire **Crown Philanthropic Solutions / DonorFirst**; "$16.1B" supported | acquisition |
| 2017 | "The Giving Platform" launched (retrospective claim) | product launch |
| 2019 | **Joe Fisher** becomes CEO, "tech-focused leadership team" | leadership |
| 2021-03-09 | Acquires **Pinkaloo** (no-minimum giving accounts) | acquisition |
| 2022-03-22 | **RenPSG renamed Ren**; ">$20B" supported | positioning |
| 2022-06-08 | Crypto DAF with The Giving Block via RCF ($100k minimum) | product launch |
| 2023-01-20 | Acquires **Stellar Technology Solutions / iPhi CoreEnterprise** | acquisition |
| 2023 | RCF→Ren fee share rises from **95% to 98%** of fundholder admin-fee income (audited) | pricing |
| 2023-06 | Publishes standard MSA templates | documentation |
| 2023-07-26 | **Bain Capital Tech Opportunities + Valeas** investment, "first institutional capital"; >200 customers | ownership |
| 2023-11-28 | **Rapid Disbursement Engine** launched | product launch |
| 2024-10-15 | Janney Charitable Giving Fund with Ren | partnership |
| 2025-07-23 | **AEF selects Ren** (release says SOC 2 Type II) | partnership |
| 2025-10-28 | **Great Hill Partners** growth investment; Bain remains significant shareholder | ownership |
| 2026-04-06/08 | AEF migration go-live; Ren "fully powers" AEF ($10.3B AUM); **SOC 2 Type 1** | technology migration |
| 2026-05-13 | Giving Compass impact-data partnership (planned phase 1) | partnership |
| 2026-08-06 | **Ren Recognize** (charity thank-you tool) | product launch |
| 2026-10-31 | AEF legacy DonorCentral portal shut down | discontinuation |

**Narrative.** Ren's history falls into three phases:
1. **Trust and DAF administration, 1987–2015.**
2. **Consolidation through acquisitions, 2011–2023:** the Blackbaud DAF platform, Crown/DonorFirst, Pinkaloo and Stellar/iPhi. That is four acquired technology lineages in 12 years.
3. **Financial-sponsor-backed platform growth, 2023–present.**

The Bain/Valeas release describes the 2023 deal as Ren's *first institutional capital*. In other words, the platform was assembled by acquisition before any private-equity money arrived.

The RCF relationship runs alongside the whole history. RCF was created in 2000 as Ren's own sponsor. Its audited related-party fee share rose to 98% in 2023, the same year as the Bain deal. We do not claim the two are connected.

**Gaps.**
- No public evidence was found on what became of the acquired codebases: iPhi, DonorFirst/DFX and Pinkaloo. Pinkaloo's marketing site is still live in November 2026, more than five years after the acquisition.
- The DFX collateral is coded "2302" (Feb 2023). Its lineage from DonorFirst is inferred from the name only.

### 3.2 TIFIN Give, GiveClear Foundation and Giving Place

| Date | Event | Type |
|---|---|---|
| 2018-09-03 | giveclear.org snapshot exists (GiveClear has a web presence before any documented TIFIN link) | archived |
| 2021-12-05 | givingplace.com snapshot (independent Giving Place) | archived |
| 2023-10-02 | **Morgan Stanley at Work** giving solution on TIFIN Give tech, sponsored by **MS GIFT** (not GiveClear) | partnership |
| 2024-02-02 | TIFIN Give **acquires Giving Place** (family office / private foundation); $670M philanthropy assets | acquisition |
| 2024-06-18 | **AssetMark** DAF program moves to TIFIN Give (GiveClear sponsor) | partnership |
| 2024-11-19 | Community campaigns feature ("already deployed") | product launch |
| 2025-02-19 | Single-charity fund option | product launch |
| 2025-04-21/30 | **Giving Place sold to Foundation Source**; TIFIN "refines focus" on DAFs | divestiture, target-market shift |
| 2025-09 | **Tax Intelligence** | announced capability |
| 2025-10-27 | **"Louise"** AI platform | announced capability |
| 2025-12-02 | **Chariot Disbursements** partnership | partnership |
| 2025 (FY) | GiveClear: $83.2M grants (vs $3.22M in 2023), $372M AUM | scale claim |
| 2026-01-29 | SEI white-label partnership (bank and trust) | partnership |
| 2026-02-26 | Confluence Financial Partners | partnership |
| 2026 | GiveClear lists **"GiveClear Direct"** consumer DAF as planned | target-market shift |
| 2026-10-28 | **SEI Charitable Fund** launched (TIFIN tech, GiveClear sponsor) | delivered evidence |

**Narrative.** TIFIN Give has the clearest **target-market reversal** in the sample. It entered family-office and private-foundation software by buying Giving Place in February 2024, then sold it about 14 months later to say it would focus on DAFs. After the sale, TIFIN's DAF work moved toward bank, trust and RIA distribution (SEI, Confluence) and toward advisor tools (Tax Intelligence, Louise). The 2023 Morgan Stanley at Work deployment matters because it shows TIFIN technology running with a sponsor other than GiveClear. TIFIN therefore cannot be read only as the "GiveClear platform".

GiveClear's self-reported grants grew roughly 26-fold from 2023 to 2025. That growth comes in the same period as the AssetMark, Arlington and Zions additions. Organic growth and partner onboarding cannot be separated with the data available.

### 3.3 Chariot

| Date | Event | Type |
|---|---|---|
| 2019-07-17 | givechariot.com snapshot **predates** the stated founding. Treat with caution: possibly an earlier owner of the domain | archived |
| early 2022 | Founded (Serfati, Kahane, Schneider) after the MyTen card project; Y Combinator | positioning |
| 2024-08-09 | **$11M Series A** led by Maveron | funding |
| 2024-09-20 | New developer documentation site | documentation |
| 2025-02-24 | Authentication moves from **OAuth 2.0 to API keys** | technology migration |
| 2025-03-17 | Disbursement APIs in **beta** (pilot) | announced capability |
| 2025-04-30* | **Chariot Disbursements** launched with 6 DAF partners incl. Daffy | product launch |
| 2026-01-28 | **Gift Processing platform** (LLM coding, CRM export) | product launch |
| 2026-05-08 | DAFpay **Donor Accounts (beta)** | announced capability |
| 2026-05-15 | **FDX API (beta)**: read-only bank data | announced capability |
| 2026-07-29 | **Charityvest** moving to Chariot (replacing PayPal) | partnership |
| 2026-09-08 | **OAuth 2.0 reintroduced** for apps acting on nonprofits' behalf | technology migration |
| 2026-10-14 | DAFpay default 2.9% nonprofit fee (public terms) | pricing |

\*The page shows "Apr 30" with no year. 2025 is inferred from search-index metadata and a Wayback snapshot of /disbursements dated 2025-05-14.

**Narrative.** Chariot's scope has widened in four steps:
1. A **DAF checkout button** (DAFpay).
2. A **grantmaker payout network** (Disbursements, 2025).
3. A **nonprofit back-office tool** (Gift Processing, 2026).
4. **Bank-account-like infrastructure** (Chariot Deposit Accounts at Column N.A., plus FDX data access in 2026).

This is the most deliberate target-market expansion in the sample. Chariot moved from serving donors and nonprofits to serving sponsors, which puts it in direct overlap with Ren's RDE and PayPal Grant Payments.

The authentication history (OAuth 2.0, then API keys in 2025, then OAuth 2.0 again in 2026) is a small but real **integration-stability signal** for partners.

### 3.4 Daffy (Daffy Charitable Fund, powered by Aside Inc.)

| Date | Event | Type |
|---|---|---|
| 2020 | ~$4.8M seed (investor list inconsistent across sources) | funding |
| 2021-09-30 | **Public launch**: flat monthly membership; no DAF-transfer-in at launch | product launch |
| 2022-02-08 | **$17.1M Series A** | funding |
| 2023 | Daffy for Work cash matching; **public API** | product launch |
| 2024 | Private stock program; **Custom Portfolios** (Jul) | product launch |
| 2025-04-30 | Launch partner of **Chariot Disbursements** | partnership |
| 2025-11-12 | **Custom Liquidation** | product launch |
| 2025 FY | 15,700 funds; $470M contributions; **$720M assets** (goal was $475M); $125M donations | scale claim |
| 2026-03-18 | **$1B assets**; $155M DAF transfers in since launch, incl. **$75M from Fidelity Charitable** | scale claim |
| 2026-04/06 | Stock-based employer matching; partial liquidation; individual stocks in portfolios | product launch |
| 2026-07-21 | Chariot is the **default donation rail**; >$380M sent electronically | technology migration |
| 2026-08 | Fee schedule shows **$40 Philanthropist tier**; tiers upgrade automatically with feature use | pricing |
| 2026-09-28 | **MCP server** for AI agents, available to all members | product launch |
| 2026-09-30 | **$2B assets**, >$500M donated; $800M contributed Jan–Sep 2026 | scale claim |
| 2026-10-22 | Private and restricted stock liquidation plans; >$600M private stock received through Aug 2026 | product launch |
| 2026-11-12 | Frec direct-indexing integration | partnership |

**Narrative.** Daffy's stated audience moved from "the rest of us" (2021) to "everyone" (2025–26). Its asset growth is now driven by **stock, including private stock, and by transfers from incumbent DAFs**, not small recurring gifts:
- Private and restricted stock received through August 2026 was more than four times the 2025 total.
- 63% of members still have accounts under $10k, according to Daffy.

Pricing changed with the market. The flat fees stayed, but more features now push an account into a higher tier: family members, custom portfolios and custom liquidation. All Daffy metrics are self-reported and unaudited. One post was publicly corrected on 2026-07-28, which counts in Daffy's favor on transparency but is also a reminder to check its numbers.

### 3.5 Charityvest / Vennfi

| Date | Event | Type |
|---|---|---|
| 2019-12 | Public launch (Vennfi tech + Charityvest 501(c)(3)) | product launch |
| 2019 | Audit: Vennfi paid % of Charityvest monthly income (rate undisclosed) | pricing structure |
| 2020-11-19 | Vennfi $2.3M seed (total $3.7M); "**zero fees**"; free stock donations from 2020-12-01 | funding, announced capability |
| 2022-03-08 | Invested accounts: admin fee "**tops out at 0.45%**"; fee waivers through 2022/2023 | pricing |
| 2022-04-26 | Low-fee ETF investments | product launch |
| 2024-10-17 | **Vennfi acquired by Foundation Source**; assets stay with Charityvest | ownership |
| 2025-11-25 | Temple University program | partnership |
| 2026-02-11 | 2025: $265.5M contributions, $119.2M grants | scale claim |
| 2026-08 | Grant payments move from **PayPal → Chariot** | technology migration |
| 2026-09-28 | **TIAA** DAF program (Charityvest sponsor, FS tech) | partnership |
| reviewed 2026-11-14 | Invested accounts **0.60% first $500k**, $100 minimum | pricing |

**Narrative.** Charityvest's positioning moved from a consumer and workplace "zero-fee" app (2020) to the sponsor behind white-label institutional programs (Temple, TIAA, advisor turnkey programs) under Foundation Source. The visible pricing change from a 0.45% top rate to 0.60% on the first tier cannot be dated from the evidence available, so it **cannot be attributed to the 2024 acquisition**. Archived fee pages would settle this. The PayPal-to-Chariot switch is the sample's only documented case of a sponsor changing electronic payment rails.

### 3.6 Foundation Source

| Date | Event | Type |
|---|---|---|
| 2007–2011 | Private-foundation administration; Charity Navigator (2010) and Fidelity family-office (2011) alliances | positioning, partnership |
| 2020-01-28 | **Incline Equity Partners** acquisition | ownership |
| 2021-02-10 | Sunil Garga CEO | leadership |
| 2023-07-18 | Impactfully Select SaaS | product launch |
| 2023-09-13 | **GTCR** acquires from Incline | ownership |
| 2023-09-19 | **Joseph Mrak CEO** | leadership |
| 2024-02-13 | **PG Calc** (planned giving) | acquisition |
| 2024-10-17 | **Vennfi** (Charityvest tech) | acquisition |
| 2025-04-30 | **Giving Place** (from TIFIN) | acquisition |
| 2025-06-25 | **Pacific Foundation Services** (~$40B under administration) | acquisition |
| 2025-09-23 | Multi-custodial turnkey DAF (BridgeFT) | announced capability |
| 2025-10-22 | Own 501(c)(3) fiscal sponsor | target-market shift |
| 2026-03-10 | Sabrina Bailey, President | leadership |
| 2026-09-30 | New CTO (Manu Sood) and new Head of Product role; "AI focus" | leadership |
| undated | **DAF OS / FundOS** marketed to DAF-sponsoring charities | target-market shift |

**Narrative.** Foundation Source is the clearest example of **private-equity ownership followed by an acquisition program**. Under GTCR it has moved from private-foundation administration into planned giving, consumer and advisor DAFs, family-office software, fiscal sponsorship, endowment sub-accounting and, most recently, sponsor-level DAF administration software (DAF OS/FundOS). That last product competes with Ren. It has changed CTO twice in five years (2021, 2026). The DAF OS/FundOS names are used inconsistently across the site's menus, which suggests the product line is still being consolidated. *Confidence: medium.*

### 3.7 Incumbent sponsors: Fidelity Charitable, DAFgiving360 (Schwab), Vanguard Charitable, NPT

- **Fidelity Charitable**
  - 1991: founded.
  - 2013: led the **DAF Direct** widget. Schwab Charitable was an initial sponsor. dafdirect.org still lists a Fidelity (fmr.com) contact address in 2026.
  - 2014: EFT grants.
  - 2015: Bitcoin. By 2015, DAF Direct adoption had reached 1,251 charities and was described as "a slow road".
  - 2020-09-30: **$5,000 minimum removed.**
  - 2026: grants paid by EFT through **Stripe** or ACH.
  - Its 2026 FAQ describes a "digital-first" transition while saying EFT is "not currently required". This **contradicts** a May 2026 Chariot post saying Fidelity would be electronic-only from July 2026.
- **Schwab Charitable → DAFgiving360**
  - 2011: Charitable Legacy program.
  - 2020-11-10: minimums removed, six weeks after Fidelity.
  - 2021: $100 minimum fee reportedly removed. *Low confidence.*
  - 2024-06-18: legal and brand rename.
- **Vanguard Charitable**
  - Fee cuts in 2006 and 2011.
  - The **$25,000 minimum** is still cited in 2026, by Daffy, which is a competitor source.
  - 2023-05: **PayPal Grant Payments** live; more than $1B paid electronically to over 13,000 charities by Nov 2024.
  - Adjacent: trade press reports that Vanguard Group plans to acquire Altruist, which launched Endaoment-sponsored DAFs in Oct 2026. Whether this relates to Vanguard Charitable is **unknown**.
- **NPT**
  - 2021 (inferred): **NPT GivingPoint** donor portal rebuilt after a two-year project.
  - 2022: PayPal Grant Payments launch partner.
  - Growth claims: grantmaking up 251% since 2019.
  - Its international DAF history was **not reconstructed**.

**Pattern.** The incumbents' visible technology changes are mostly **access and payment-rail** changes: minimums, EFT and payment partners. They are not new donor features. That is the gap Daffy now targets with its comparisons against the incumbents and the $75M it reports receiving from Fidelity Charitable.

### 3.8 Smaller and adjacent players

- **Stellar Technology Solutions / iPhi.**
  - 1999: founded, according to a third-party profile.
  - iphi.com snapshots exist from 2009.
  - January 2023: sold to Ren, with Capstone as adviser.
  - What happened to the iPhi product afterward is unknown.
- **Pinkaloo.** Acquired March 9, 2021. Its site is still live.
- **Groundswell.**
  - 2021: launched as "philanthropy as a benefit" with a $15M seed.
  - By 2026: a full CSR suite (employee giving, volunteering, grants management, employee communities, employee assistance fund).
  - May 2026: listed as a Chariot Disbursements partner.
  - This is a **target-market widening** from DAF-as-benefit to corporate CSR software.
- **Givinga.** Founded around 2015. In 2026 it presents itself as "financial-grade" corporate philanthropy and charitable-payment infrastructure. Earlier positioning and funding were not verified.
- **Blackbaud / YourCause.**
  - 2011: Blackbaud exits DAF technology by selling it to Renaissance.
  - 2019: buys YourCause (CSR) for about $157M.
  - The 2024 AEF move from Blackbaud to NPact, followed by the 2026 move to Ren, shows a sponsor migrating its portal twice in about two years.
- **Benevity.**
  - Dec 2020: Hg takes control at about a $1B valuation.
  - Dec 2021: acquires Alaya.
  - Dec 15, 2026: Alaya **scheduled** to be retired, about five years after the acquisition.

---

## 4. Pattern analysis

### 4.1 Announced versus delivered

Of 39 tracked announcements:
- 15 have `evidence_of_delivery`
- 10 are `partial`
- 12 are `no_public_evidence_yet`
- 2 are `contradicted`

| Company | Delivered | Partial | No public evidence yet | Contradicted | Reading |
|---|---|---|---|---|---|
| Daffy | 5 | 0 | 0 | 0 | Announcements usually come with docs and later usage metrics (self-reported). |
| TIFIN Give | 5 | 2 | 1 | 0 | High announcement frequency. Delivery shown by help docs (Tax Intelligence), customer launches (SEI) and a partner (Chariot). Vendor-only: Louise AI, community campaigns. |
| GiveClear | 0 | 0 | 2 | 0 | Consumer product and 2026 targets not due yet. |
| Chariot | 1 | 3 | 1 | 0 | Disbursements strongly delivered. Several features stay in long **beta** (Gift Processing APIs, Donor Accounts, FDX). |
| Ren | 2 | 2 | 3 | 1 | Few dated feature announcements; broad marketed capabilities without public delivery detail; conflicting SOC statements. |
| Foundation Source | 0 | 1 | 2 | 0 | Grows by acquisition; capability claims (DAF OS, multi-custody) have no named customers. |
| Charityvest | 1 | 1 | 1 | 0 | Positioning changed from "zero fees". |
| Fidelity Charitable | 0 | 1 | 0 | 1 | Contradiction comes from a **third party's** claim, not Fidelity's own. |
| Vanguard Charitable | 1 | 0 | 0 | 0 | PayPal grants announced, then delivered with metrics. |
| Others | 0 | 0 | 2 | 0 | Groundswell's 24-hour claim; Benevity sunset not yet due. |

**What this does and does not show.**

1. **Companies that publish versioned developer documentation (Daffy, Chariot) are much easier to verify.** That reflects how they communicate. It is **not** evidence that their engineering is better.
2. **TIFIN Give** is the company that "repeatedly announces" capabilities in the sense of the brief: eight dated product or partnership releases in 24 months. For most of them we did find later delivery evidence. The weak spot is **AI execution claims (Louise)**, where no help documentation or user report was found.
3. **Ren and Foundation Source** have the reverse problem. They publish few dated feature announcements, so their *marketed* capabilities have no announcement date to test. Absence of evidence here mostly reflects enterprise sales models, where documentation sits behind logins.
4. **Long-running betas** (Chariot) are a separate pattern. The feature exists, but it is not clear when production use will be widely available.

### 4.2 Target-market shifts

| Company | From | To | Evidence anchor |
|---|---|---|---|
| Ren | Charitable trusts (1987) | DAF sponsor (2000), then institutional DAF technology, then network/payments (RDE), charity tools (Recognize) | Timeline, RDE PR, help docs |
| TIFIN Give | Community/workplace DAF (MS at Work 2023) plus family offices (Giving Place 2024) | DAF-only, wealth enterprise / bank and trust (2025–26) | TIFIN, SEI releases |
| GiveClear | Sponsor for TIFIN and partner programs | Planned direct-to-consumer sponsor (2026) | GiveClear page |
| Chariot | DAF checkout (2022) | Grantmaker payouts (2025), nonprofit back office (2026), bank-data APIs (2026) | Changelog, PRs |
| Daffy | Small recurring donors (2021) | Stock and private-stock donors, employers, AI agents (2024–26) | Daffy posts |
| Charityvest | Consumer/workplace "zero-fee" app (2020) | White-label institutional sponsor (Temple, TIAA) | FS/TIAA releases |
| Foundation Source | Private-foundation administration | Full charitable-services company plus DAF sponsor software | FS newsroom |
| Groundswell | DAF as employee benefit (2021) | Corporate CSR suite (2026) | Site, BW |

**Implication.** Specialization is giving way to overlapping, broad platforms. Ren, Foundation Source and TIFIN now all sell to wealth-management and institutional channels. Chariot and Ren's RDE now overlap in payments. Daffy and GiveClear (planned) both reach consumers directly.

### 4.3 Ownership changes and what followed

| Ownership event | What followed (observable) | Not observable |
|---|---|---|
| Ren: Bain/Valeas, 2023-07 | RDE (+4 months); AEF win (+24 months); second PE round (+27 months) | Customer churn, pricing, margins |
| Ren: Great Hill, 2025-10 | Giving Compass (planned), Ren Recognize | Roadmap delivery |
| Foundation Source: Incline, 2020-01 | New CEO (+13 months), new CTO (+21 months) | |
| Foundation Source: GTCR, 2023-09 | New CEO (+6 days); 4 acquisitions in 17 months; new President, CTO and Head of Product (2026) | Integration of acquired platforms |
| Giving Place: TIFIN 2024-02, then FS 2025-04 | Two owners in 14 months; TIFIN shifted to DAF-only | Giving Place customer retention |
| Vennfi → Foundation Source, 2024-10 | Institutional programs (Temple, TIAA); payment rail switch (2026); fee schedule now 0.60% first tier (date unknown) | Whether fees changed because of the deal |
| Stellar/iPhi → Ren, 2023-01 | None found | Product fate |
| Pinkaloo → Ren, 2021-03 | Brand site still live 2026 | Active sales or customers |
| Benevity: Hg 2020; Alaya 2021 | Alaya scheduled for retirement Dec 2026 | Migration outcome |

**Reading.** The most consistent observable effect of a PE transaction is a **change in management and/or an acquisition within roughly 0–6 months**. Product retirements for acquired assets show up years later: Alaya after about 5 years; AEF's legacy portal after 2 years. Only half of the acquired DAF platforms in the record have any public trace of what happened to them.

### 4.4 Historical pricing changes

| Date | Company | Change | Direction |
|---|---|---|---|
| 2006, 2011 | Vanguard Charitable | Fee reductions | Down |
| 2020-09-30 | Fidelity Charitable | $5k minimum removed | Access opened |
| 2020-11-10 | Schwab Charitable | $5k/$500 minimums removed | Access opened |
| 2021 (low conf.) | Schwab Charitable | $100 minimum fee removed | Down |
| 2020 → 2022 → 2026 | Charityvest | "Zero fees", then 0.45% top rate (with waivers), then 0.60% first $500k | Up on headline first tier |
| 2021 → 2026 | Daffy | $3/$5/$20, then added $40 tier with feature-based upgrades | Up for heavier users |
| 2023 | RCF→Ren | Fee share 95%, then 98% | Toward vendor |
| 2026 | Chariot DAFpay | 2.9% default to nonprofits (subscription alternatives) | n/a (no history) |
| 2026-10 | Altruist/Endaoment | Advisor DAF at 50 bps vs a cited 60–65 bps "typical" | Price pressure |

**Reading.** At the low end, the incumbents compete by removing minimums. The challengers raise their *effective* price for complex features. **The 0.60% first-tier administrative fee is close to an industry convention:** Fidelity, Vanguard and Charityvest's 2026 schedule all use it.

---

## 5. Implications

1. **Due diligence on any provider should include a dated timeline of how it describes itself.** Ren's rename year, SOC type and network size all changed between documents. Ask for dated, defined metrics and for the actual SOC reports.
2. **Ask which payment rail a sponsor uses and what it would cost to switch.** Charityvest's 2026 switch shows rails can be swapped. The AssetMark transition shows sponsors keep the legacy provider running during a move. Charities now face separate enrollment flows for Fidelity (Stripe/ACH), PayPal and Chariot.
3. **Treat PE ownership changes as signals to watch for acquisition integration risk, not as findings.** For Foundation Source, the question is whether Charityvest/Vennfi, Giving Place, PG Calc and PFS run on shared systems. For Ren, the question is the status of iPhi, DFX and Pinkaloo.
4. **Score AI announcements separately from documented workflows.** Louise (TIFIN) and the AI focus at Foundation Source have no public delivery documentation. Daffy's MCP server has public docs. Agent-initiated grants need sponsor-approval boundaries that can be inspected.
5. **Read fee changes over time.** Challengers' "flat" or "zero" pricing has moved toward tiered pricing for complex use. Model costs at the feature level, not the headline price.

---

## 6. Caveats

- **Absence of evidence is not evidence of non-delivery.** Every `no_public_evidence_yet` label reflects the limits of this search: a capped search budget, blocked sites and gated customer documentation.
- **Archived rows are pointers only.** No Wayback page content was read.
- **Most metrics are self-reported and unaudited**, including Daffy assets, GiveClear grants, Ren scale and Chariot volumes.
- Some dates are inferred, and each is flagged in its row: Chariot Disbursements year; NPT GivingPoint month; Tax Intelligence day; the DFX file code; the date of the Charityvest fee change.
- A company "timeline" on a corporate site is a retrospective, marketing-shaped account. Where it conflicts with a contemporaneous release (Ren 2016 and 2021/2022), the release is preferred.
- The Vanguard Group/Altruist item is adjacent and comes from a secondary source only. It must not be read as a Vanguard Charitable event.
- No confidential, employer or expert-network information was used.

## 7. Open questions

1. What happened to the iPhi CoreEnterprise, DonorFirst/DFX and Pinkaloo codebases inside Ren?
2. When exactly did Charityvest's fee schedule change from a 0.45% top rate to 0.60% on the first tier? Archived guide pages would answer this.
3. When was Daffy's $40 tier introduced? The 2025-01-07 and 2023-01-27 membership-page snapshots exist but were not read.
4. Did Fidelity Charitable adopt, delay or never plan an electronic-only policy for July 2026?
5. When was GiveClear founded? There is a 2018 snapshot. Did "GiveClear Direct" launch in 2026?
6. When did DAFpay originally launch, and how has its fee changed over time?
7. What does NPT's international DAF history look like, and which vendor sits behind NPT GivingPoint?
8. Is Vanguard Group's reported plan to acquire Altruist linked in any way to Vanguard Charitable?
9. What is the actual relationship between Foundation Source's DAF OS and FundOS products, and does any sponsor use them besides Charityvest?

---

## 8. Data dictionary

### company-timeline-events.csv (195 rows)

| Field | Definition |
|---|---|
| `event_id` | `CT###`, sorted chronologically. |
| `event_date` | ISO date or partial date (YYYY, YYYY-MM). Future scheduled events are allowed and flagged. |
| `date_precision` | `day`, `month`, `year`, `year (early)`, `day (scheduled)`. |
| `company` | Primary entity, with counterparties after "/" (e.g., `Ren / American Endowment Foundation`). |
| `event_type` | One of: `positioning`, `product_launch`, `archived_documentation`, `pricing_change`, `leadership_change`, `acquisition`, `discontinuation`, `technology_migration`, `announced_capability`, `delivered_capability_evidence`, `partnership_start`, `target_market_shift`, `funding_ownership_change`, plus the extension `scale_milestone_claim` (self-reported asset, grant or account milestones). There is no `partnership_end` row; the Charityvest–PayPal end is recorded as the 2026-08 `technology_migration`. |
| `description` | Factual summary; numbers as reported by the source. |
| `source_url` | Source supporting the event. Archived rows use web.archive.org snapshot URLs. |
| `source_date` | Publication date of the source, or "reviewed YYYY-MM-DD" for undated live pages. |
| `evidence_class` | `primary` (entity or its customer/regulator), `secondary` (press, deal databases), `archived` (Wayback snapshot existence). |
| `verification_method` | `fetched_full_text`, `search_result_summary`, `prior_repo_source(<ID>)`, `archive_availability_api`. |
| `confidence` | `high` / `medium` / `low`, reflecting source quality, date certainty and corroboration. |
| `notes` | Conflicts, inferences and limitations. |

### announced-vs-delivered.csv (39 rows)

| Field | Definition |
|---|---|
| `avd_id` | `AVD##`. |
| `company` | The announcing entity. For AVD35 the claim is about Fidelity Charitable but was made by Chariot. |
| `announced_capability` | What was claimed. |
| `announce_date`, `announce_source_url` | When and where it was announced. |
| `subsequent_delivery_evidence` | Later evidence found, or "none located". |
| `evidence_source_url`, `evidence_date` | Source(s), separated by " ; ". |
| `delivery_status` | `evidence_of_delivery`, `partial`, `no_public_evidence_yet`, `contradicted`. |
| `evidence_type` | e.g., `customer_facing_help_doc`, `public_developer_docs`, `customer_primary_release`, `vendor_assertion_only`, `none_found`, `not_yet_due`. |
| `notes` | Caveats, including that delivery evidence is often vendor-authored. |
