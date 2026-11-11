# Ren vs. TIFIN Give, with Chariot as infrastructure
**Evidence-led competitive and operating-model assessment | 2026-11-11**

**Purpose.** Compare the *actual roles* and publicly documented capabilities of Ren (reninc.com) and TIFIN Give. Determine when Chariot is a complementary integration, an outsourced payment layer, or a competitor to Ren's payments service. This is not an independent product benchmark, security audit, legal opinion, recommendation to select a vendor, or investment rating. All observations use public information; no confidential former-employer or expert-network information is used.

**Read with:** [comparison dataset](../data/platform-comparison-2026-11-11.csv), [source register](../data/platform-deep-dive-sources.csv), and [test protocol](platform-evaluation-protocol.md). Source IDs C001–C025 are local to this investigation, not the general landscape or SOC 2 source registers.

## Executive conclusions

1. **There is a documented partnership, not merely a proposed architecture.** TIFIN announced use of **Chariot Disbursements** on Dec. 2, 2025 [C010]; Chariot subsequently documented the actual division of labor: **TIFIN Give = technology; GiveClear Foundation = legal DAF sponsor and final grant approver; wealth firms = program distribution; Chariot = disbursement infrastructure** [C011]. This is a substantially stronger fact than inferring a partnership from comparable products.
2. **Ren publicly presents a broader vertically integrated administrative stack.** It markets donor/advisor and branded portals, DAF operations, grants, custody-adjacent reporting, **fund accounting with daily unitization**, managed services, and an integrated Rapid Disbursement Engine [C002,C004,C005]. Some of these capabilities are described for specific product lines or customer segments; there is no proof all are delivered together in every contract.
3. **TIFIN's strongest documented emphasis is the advisor/wealth enterprise channel.** It markets multi-custody flexibility, advisor-managed investments, tax-intelligence tooling, white labeling, multi-generational engagement, fully digital onboarding and AI-assisted donor conversations [C008,C009]. It also publicly claims administrative automation, but **the exact general-ledger/subaccounting system, accounting controls and integration architecture have not been independently established**.
4. **Chariot has two distinct offerings that must not be conflated.** **DAFpay** initiates donor grant requests, providing nonprofit checkout and provider integration [C017,C018,C019]. **Chariot Disbursements** is a grantmaker payment delivery and recipient-verification solution, integrated with TIFIN [C010,C016]. Chariot does not replace sponsor fiduciary approval or DAF fund accounting solely by providing these layers.
5. **The competition overlaps in payments.** Ren markets payments on an institution's existing bank rails (ACH or check and positive pay), while TIFIN has adopted Chariot's recipient-facing payment infrastructure [C004,C010,C016]. These are distinct architectural choices, **not proven winner/loser results**. Their speed, costs, intermediary risk, fraud outcomes, reconciliation quality and bank dependencies require common tests.
6. **Assurance remains unverified at the report level.** The philanthropic Ren's April 2026 sponsor-hosted announcement states SOC 2 Type I [C021]; Chariot states Type II [C020]; TIFIN previously claimed SOC 2 without type [C022]. The actual independent reports, periods and scoped systems **were not inspected**. Do not mistakenly attribute an unrelated tryren.com Type II claim to reninc.com.

## 1. Product and entity map

| Function | Ren model: publicly documented | TIFIN Give + GiveClear + Chariot: publicly documented |
|---|---|---|
| Legal donor-advised fund sponsor | Renaissance Charitable Foundation can serve as sponsor; Ren also markets program support with alternative sponsorship options [C002,C003,C006] | GiveClear Foundation serves as sponsor in documented TIFIN-led programs; SEI Charitable Fund also identifies GiveClear [C011,C013] |
| Technology operator | Ren supplies portal and administrative infrastructure, with legacy product lines including DFX and separate foundation accounting solutions [C002,C005] | TIFIN Give provides firm/advisor-branded technology [C008,C011] |
| Client distribution and branding | Institutional platform/branded partners, including firms and foundations [C001,C002] | Wealth advisors, banks/trusts, broker-dealers and asset managers; named SEI, Confluence, AssetMark, Blue Trust relationship evidence [C011,C013,C014,C015] |
| Contribution and investments | Ren's sponsor example places customer at custody; Ren's systems and services include subaccounting, accounting for separately managed accounts [C002] | TIFIN markets multi-custody and advisor-managed portfolios; GiveClear reports TIFIN-supported investment/fund-transfer automation [C008,C012] |
| Grantee eligibility and grant decision | Ren provides vetting and submits grants for sponsor staff approval/denial; Renaissance Charitable retains legal grant approval [C002,C006] | GiveClear approves/rejects donor grant recommendations; TIFIN operates workflows and Chariot handles disbursement [C011] |
| Outbound grant payment | Ren Rapid Disbursement Engine, ACH/check, existing sponsor bank rails, positive pay and payment status [C004] | Chariot Disbursements; Chariot Deposit Accounts through Column N.A. and fallback mailed check [C010,C016,C024] |
| Nonprofit-facing interface | Ren for Charities portal for multi-program ACH onboarding and grant data [C001,C004] | Chariot account, gift data, donor/source metadata and disbursement tracking [C011,C016] |
| Independence | Different sponsor, vendor and custody roles should not be collapsed into a Ren legal entity [C002,C006] | Explicit four/five-entity structure; TIFIN is *not* itself the charitable sponsor in the cited arrangement [C011] |

### Architectures, schematically

**Illustrative Ren arrangement, grounded in product descriptions [C002,C004,C006]:**

Donor/advisor → Ren portal + administrative workflow → sponsor (Renaissance Charitable or selected sponsor) authorizes → Ren-backed ledger/reporting/treasury workflow → Ren Rapid Disbursement Engine on existing financial institution rails → nonprofit (ACH/check) → payment reconciliation.

**Documented TIFIN–GiveClear–Chariot arrangement [C010,C011,C016]:**

Wealth firm's branded donor portal (TIFIN Give) → donor grant recommendation → GiveClear Foundation decision → TIFIN integration and Chariot Disbursements → nonprofit's Chariot Deposit Account at Column N.A. (if claimed/eligible), or check fallback → nonprofit payout/acknowledgement and accounting/reconciliation.

These high-level diagrams **do not** assert internal message flows, cloud infrastructure, deployment topology, number of ledgers, hosting systems, custody locations, or a universal grant path. Technical boundaries have to be confirmed by demonstrations and implementation design.

## 2. Feature/capability differentiation

Status key: **D** = directly described in official technical or detailed service docs; **M** = marketed by an official vendor source; **U** = unassessed, not absent; **P** = verified public partner-role statement. Neither D nor M means functionality independently tested.

| Capability | Ren | TIFIN Give | Chariot's relevant role | Assessment |
|---|---|---|---|---|
| DAF sponsor support | D (RCF; other sponsor options M) | P (GiveClear) | U | Both can support a program; legal sponsors are distinct [C002,C003,C011] |
| Institutional white-label donor/advisor experience | D/M | M | DAFpay embed, not full portal | Broad overlap [C002,C008,C017] |
| Fund accounting / daily unitization | M, explicitly stated for foundation solution | U: TIFIN markets automation, not detailed ledger controls | U: not a DAF subledger provider in reviewed docs | Potential differentiator; compare tested same product SKUs [C005,C012] |
| Investment flexibility / multi-custody | D specific customer/sponsor models | M multi-custody, alternatives, advisor managed | Not a custody-investment solution | Both claim advisor access; different documentary specificity [C002,C008,C009] |
| Grant screening and approval workflows | D + sponsor authority | M charity search/due diligence; P GiveClear approves | DAFpay APIs respect DAF provider review | Regulatory decision authority remains with sponsor [C002,C006,C009,C011,C019] |
| Disbursements | M integrated ACH/check directly on institution bank rails | P via Chariot | D Chariot Disbursements (digital + fallback check) | **Overlap in outcome, different integration/value chain** [C004,C010,C016] |
| Documented external API specifications | Historic API integration offering, no public endpoint schema confirmed | No public implementation-grade schema reviewed | D DAFpay OAuth/Donor Accounts and disbursement APIs | **Visibility gap ≠ absence of APIs** [C002,C017,C018,C019] |
| Identity / access | M SSO, MFA for certain Ren solutions | U as to exact implementation | D OAuth, authorization and verification schemes for DAFpay; verified bank-control person | No cross-vendor measured IAM conclusion [C002,C005,C018,C019,C024] |
| Tax-intelligence / conversational AI | U (do not assume absent) | M tax intelligence and action-capable conversational AI | U for sponsor/core wealth AI | Needs live evaluation of authorization, accuracy and guardrails [C008,C009] |
| Family and next-gen engagement | U as to latest relative feature depth | M family experiences, community campaigns | U | Marketed TIFIN emphasis; not proved superior [C008] |
| Scale / deployed references | M 150+ DAF programs, $200B+; base and date not independently validated | P SEI and Confluence launches, Chariot lists 100+ firms and 1,500+ advisors | P technology partner | References are useful; incomparable volume metrics [C001,C011,C013,C015] |
| SOC 2 independent report inspected | No | No | No | Do not score vendor claims as audited performance [C020,C021,C022] |

### Critical product-scope caution

Ren publishes a service catalog covering DFX/DonorFirstX, branded program administration and separate product lines [C002]. Its community-foundation site specifically markets general ledger, NAVs and daily unitization [C005]. **An evaluator must confirm which Ren stack is being offered** before crediting all functions to the same deployment. Conversely, TIFIN's claim of end-to-end administration [C014] does **not** establish that it lacks any fund accounting system; it simply gives fewer inspectable details in the sources reviewed.

## 3. Selection criteria that actually distinguish these solutions

### A. A foundation or sponsor replacing core administration technology

**Initial fit hypothesis:** Ren merits a stronger *first evaluation* for deep accounting and mature outsourced grant operations because it explicitly documents them [C002,C005]. TIFIN must be tested for ledgers, daily unitization, correction/reversal workflows, investment valuation, sponsor approvals and program-level financial statements. This is *not* a verified finding that Ren is better or TIFIN incapable.

**Discriminating tests:** Post 20 linked contributions, 50 grant recommendations, 5 reversals, 3 SMA corporate actions and 1 month-end close; reconcile sponsor GL, pooled-fund NAV, custodian records, ACH/check returns, donor statements and management reports. Request event and audit trails.

### B. Wealth manager launching a branded DAF product without a new sponsoring charity

**Initial fit hypothesis:** TIFIN/SEI/GiveClear is a directly evidenced, newly launched branded advisor-channel pattern [C013,C014]. Ren offers competing sponsored/branded program models [C001,C002,C003]. Compare advisor retention/control of invested assets, custody neutrality, timing/price of implementation, donor onboarding, permission models, fee disclosures and program flexibility.

**Discriminating tests:** Launch two programs in a demo tenant: pooled investments and advisor-managed SMA, each with 2 advisors, 3 donors, estate successors, branded letters, charitable gifts of securities, and an approved grantee. Validate who has legal acceptance and grant authority.

### C. A sponsor with a working platform that needs faster grant payments

**Initial fit hypothesis:** A full platform replacement is unnecessary until there is evidence the core platform is the bottleneck. Compare Ren's on-existing-bank-rails payment service [C004] against Chariot Disbursements [C016] on common reliability, operational cost, non-claimed nonprofit experience, data completeness, exceptions, payment identifiers, check handling and bank risks.

**Discriminating tests:** On identical grants and recipient cohorts, capture timestamps for approval, bank release, recipient-account availability, ultimate external-bank receipt, successful match in charity CRM, returns/voids, and total staff minutes.

## 4. Chariot's two products and the risk of the wrong comparison

**Chariot DAFpay (checkout/initiated grant recommendation) [C017,C018,C019]:** A nonprofit or fundraising platform can surface a DAF payment option. A provider integration can identify available grantable balance, create a recommendation with required idempotency, and query its status. **Provider's normal review pipeline is not bypassed**. Donor Accounts were introduced in **beta on May 8, 2026** [C023], so confirm production availability and access before planning around them.

**Chariot Disbursements (approved payment delivery) [C010,C016,C024]:** After grant approval, grantmaker sends disbursement data and funding instructions; Chariot helps verify the nonprofit and deliver electronically to a verified Chariot Deposit Account or send a check when not claimed. Chariot is a fintech, **not a bank**; Column N.A. supplies deposit accounts [C016]. Instant *in-network* availability is not the same as transferred funds arriving in the nonprofit's external operating bank account. Chariot's public FAQ describes fees to the grantmaker, generally not nonprofit recipients [C016].

**Ren's Rapid Disbursement Engine [C004]** also performs grant routing, ACH/check, status, and fraud controls, with the distinctive **claim** that payments originate on the program's existing bank rails. It may substitute for some Chariot Disbursements functions in a given workflow. There is **no verified public Ren–Chariot integration** in this investigation, and that absence of evidence must not be written as “Ren cannot integrate.”

**Architecture consequence:** Decide which system is *source of truth* for grant approval, reservation of funds, payment initiation, settlement, returns, status notifications, and final reconciliation. Without this, both a bundled vendor and composable vendors can create duplicate or invisible failure states.

## 5. Scale, adoption, and claims that cannot be fairly ranked

- Ren markets **$200B+** supported charitable assets and **150+** DAF programs on some pages [C001]. A separate Ren page calls out **$175B+** and 2.2M grants per year [C026], while a Ren payments page has displayed **1.7M, 2M or greater annual grants** across snapshots [C004]. These statements may reflect different update dates or product scopes; **do not build a precise market share, growth rate, or productivity metric** from them without audited definitions, periods, and denominators.
- TIFIN markets **more than $90M grants in 2024** and **15K transactions** [C008]; GiveClear reports **$83.2M in 2025 grants and 16,249 grants** across its sponsor's operations [C012]. These are **different entities and periods** and not a clean same-portfolio series.
- Chariot's Feb. 2026 explanation states TIFIN Give supported **1,500+ advisors, 100+ firms, and 2,000+ donors** [C011]. This is a partner statement, not independent audit or an apples-to-apples account census compared with Ren.
- A vendor's “instant approval,” another's “2–5 day grant processing,” and another's “instant bank availability” refer to **different events** [C001,C009,C016]. Do not use them as a speed ranking. Define recommendation → decision → approved payment → funds available → funds withdrawn and reconciled.

## 6. Assurance, regulatory and control boundaries

- Actual SOC 2 **report scope** matters more than the badge: Ren's public 2026 claim is Type I; Chariot publicly states Type II; TIFIN's published statement is unspecified [C020,C021,C022]. No independent reports reviewed.
- Obtain **SOC 1 where fund accounting impacts financial statements**, in addition to appropriate SOC 2 report coverage for admin portals, donor data, Chariot payments, TIFIN tenant isolation and sponsor integrations.
- Sponsors, not donor recommendation interfaces, retain final grant approval, as confirmed by both Renaissance Charitable [C006] and Chariot's description of GiveClear [C011].
- For the TIFIN/Chariot implementation, determine which financial institution and entity is the legal account holder, where money is parked between sponsor authorization and nonprofit availability, and who handles rejected recipients/returned checks [C016,C024].
- Verify any AI action path stops at sponsor approval. A conversational user experience that can propose a grant must not silently become an unrestricted payment authorization [C008,C011].

## 7. Competitive thesis and falsification tests

**Thesis H1:** Ren is especially defensible where outsourcing complexity and fund accounting are high. **Disprove** with TIFIN demonstrations of equally strong sponsor ledger, daily unitization, case management, corrections, data lineage, accounting assurance and lower operating costs.

**Thesis H2:** TIFIN's advisor-centric integration may win more newly launched wealth enterprise DAF programs. **Disprove** if Ren demonstrates better adoption, lower time-to-live, comparable multi-custody/AI/advisor experiences, or favorable distribution economics in comparable new programs.

**Thesis H3:** Chariot can be independently valuable as shared nonprofit payment infrastructure without replacing a sponsor platform. **Disprove** if bundled systems achieve similar recipient coverage, cost per payment, exception handling and donor data quality at lower integration risk, or if Chariot's additional banking/identity dependencies introduce new failure modes.

**Thesis H4:** Better capture of complete grant instructions, automated eligibility checks and deterministic exception handling will drive more cost reduction than autonomous AI grant approval. **Disprove** through measured volume-based time/cost studies where AI-autonomous decisions outperform with equal oversight, accuracy and compliance.

**Thesis H5:** Sponsors may become dependent on a small set of shared technology providers, reducing apparent competition. **Disprove** by mapping independent ledger, grants, IAM, bank and payment vendors behind each “competing” sponsor, not just portal brands.

## 8. Practical answer for industry expert interviews

A defensible public-information answer to “who competes?” is:

> Ren and TIFIN Give overlap most clearly in institutional DAF technology and branded wealth-firm offerings. Their respective public positioning differs: Ren foregrounds administration, accounting and large-program infrastructure, while TIFIN foregrounds advisor-led distribution, multi-custody investment flexibility and digital experiences. TIFIN publicly relies on GiveClear for sponsorship and has integrated Chariot Disbursements for the final payment leg. Chariot may complement DAF platforms, while its grant-payment service overlaps some of Ren's own payment offering. A reliable selection decision requires a defined sponsor model, accounting needs, custody constraints, control obligations and independent performance testing.

This explanation is based on public evidence. Do not interpret it as knowledge of private product architecture, customer contracts, internal code, operational unit economics or strategic plans.

## Recommendations, ranked by evidence impact

1. **Highest priority: same-scenario demo** of Ren vs. TIFIN including legal sponsor, fund accounting, sponsor approval, investment positions, reporting, disbursement exception and charity receipt. A UI demo without records and control evidence is insufficient.
2. **Source-of-truth and contract map**: collect which entity owns account, ledger, custody, grant decision, payment, personal data, security controls and exceptions in each implementation.
3. **Payments benchmark**: for Chariot Disbursements and Ren Rapid Disbursement Engine, include both claimed and unclaimed charities, failed validation, returned check and bank outage; measure the *same* timestamps and completed grants.
4. **Security and assurance**: obtain permissioned, current SOC reports; ask for audit scope and residual sponsor/CUEC obligations. Do not store confidential reports in this public-research corpus.
5. **Commercial benchmark**: minimums, fees, pricing tiers, sponsor costs, custody/AUM economics, payment transaction charges, migration expenses and exit rights, supported by dated, authorized quotations.

## Source limitations

Public pages describe capabilities and partnerships, not independently measured uptime, grant throughput, latency, availability, security, price or implementation quality. Historic service descriptions [C002] may not match every current contract. Product pages are not evidence of exclusive capabilities: **U means we have not verified, not that a competing vendor lacks it**.

**Next:** run the buyer-neutral [evaluation protocol](platform-evaluation-protocol.md) and update [comparison data](../data/platform-comparison-2026-11-11.csv) only with documented or directly tested outcomes.
