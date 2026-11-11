# DAF platform economics, distribution control and fee transparency

**Public-source investigation: November 11, 2026**  
**Purpose:** Determine where revenues accrue in advisor-led DAF programs, how the TIFIN Give–GiveClear–Chariot structure differs from Ren/RCF, and what available fee disclosures do and do not establish. No confidential industry-client or former-employer information used. **Not an investment recommendation, a revenue audit, legal opinion or current negotiated fee quote.**

## Executive synthesis

**1. A DAF 'platform' is not one economic business.** At least six independently contractible economic functions appear in the ecosystem: legal sponsorship/administration; DAF platform/technology; investment advice/model management; custodian/broker; advisor/client distribution; and grant disbursements/compliance. A single brand may combine functions or bundle services. Public fee schedules often capture only one layer. Comparing a donor's RCF fee with TIFIN's investment-adviser service fee is an **invalid apples-to-apples price comparison**.

**2. TIFIN Give's 2025 Form ADV reveals materially more about monetization than its product page.** The company-hosted March 31, 2025 Part 2A brochure [E01] discloses: administration/technology service fees; investment management fees; optional subadvisory fees paid to the DAF adviser; SaaS implementation and subscription fees; marketing/sponsorship fees paid by investment-model sponsors to enhance visibility; and a nominal per-transaction guest-giving fee. Which entities actually pay, how charges are passed through to specific 2026 DAF programs, and actual realized rates require current contracts.

**3. There is a genuine disclosed conflict issue to investigate, not a proven misconduct finding.** The 2025 TIFIN brochure's Item 14 says sponsorship payments to increase portfolio visibility create an incentive to recommend those portfolios above others [E01]. The broker/custodian is chosen by the client, and TIFIN discloses no custody of the sponsor's assets. The mere existence and disclosure of these arrangements do **not** establish biased recommendations in any specific account. Ask for how portfolio ranking, sponsor approval, audit trails and disclosure work in practice.

**4. Distribution and legal ownership are different.** Ren's published direct onboarding specifies that the investment account must list **Renaissance Charitable Foundation as owner**, not the donor [E13]; TIFIN's Form ADV likewise says its advisory clients are the DAF sponsor charities, not retail donors [E01]. A wealth manager saying it 'retains AUM' may mean it retains the adviser-client relationship and the ability to manage investments for a charitable sponsor, **not donor legal ownership** of gifted assets [E16]. This distinction is crucial when valuing custody retention and advisor economics.

**5. Sponsor assets, adviser regulatory AUM, platform supported assets, and grant flows are different metrics.** In the dated March 2025 brochure, TIFIN Give reports **$4,674,789 of discretionary advisory AUM as of Dec. 31, 2024** [E19]. GiveClear separately self-reports **$372m under management** and **$83.2m granted in 2025** [E08]. Neither is a valid denominator for the other: the entities, control/accounting scope, dates and definitions differ. Do not treat this as a growth-rate series or claim TIFIN technology supports only $4.7m.

**6. Payment processing is a distinct cost and control boundary.** Chariot says its Disbursements product charges the **grantmaker** a transaction fee, while nonprofits have no charge for basic disbursement service [E10]. Its API offers optional just-in-time funding and organization-verification bypass paths [E11,E12]. Rate, charged legal entity, liability for returns, cash settlement, and operational ownership are not publicly established. A modular approach can reduce infrastructure costs but also creates reconciliation and dependency work.

## A. Economic roles and fee ownership

| Role | Controls or delivers | Potential economic compensation | Publicly established provider example | Required contract verification |
|---|---|---|---|---|
| **Sponsor charity** | Legal acceptance/ownership; grant approvals; tax receipts and policy | Annual admin fees; program-specific costs | Renaissance Charitable Foundation [E03–E05,E17]; GiveClear [E08] | Exact sponsor fee, custody contract, terms, who receives fees |
| **DAF operator / administrator** | Donor/charity servicing, accounting, grant review support, reporting | AUM-based fees, per-account servicing, fixed service fees | Ren with RCF [E03,E17]; TIFIN service fees [E01] | Sponsor vs operator revenue split and costs |
| **Platform / software vendor** | Portals, APIs, records and integrations | SaaS implementation + subscription, per-account/AUM licensing | TIFIN [E01]; Ren program fees opaque for partners [E15] | Price and minimum volume, implementation, exit and change orders |
| **Investment adviser and model** | Approved investment strategy and model selection | Management bps, subadvisory bps, potentially model sponsorship fees | TIFIN advisory [E01]; RCF advisor managed [E04] | Reconciliation of sponsor vs advisor authorization and fee disclosure |
| **Custodian / broker** | Legal accounts, positions, securities settlement, custody statements | Custodial fees, trading and underlying asset expenses | Client-selected in TIFIN 2025 ADV [E01] | Custody costs and asset control boundaries |
| **Wealth firm / channel** | Advisor relationship, client engagement, referrals/distribution | Advisory fees on sponsor-owned assets if permitted; relationship retention | SEI DAF with TIFIN and GiveClear [E09] | Who is registered adviser, whose client, compensation and conflicts |
| **Payments / nonprofit verification** | Grant delivery, recipient verification, tracking, returns | Per-transaction fee to grantmaker; nonprofit add-on subscriptions | Chariot Disbursements [E10–E12] | Fee amount; ACH/check; failures; refund and bank balances |

**Important distinction:** The labels above are *functional roles*. Depending on contracts, one legal company might perform several, and the money may be charged to a charity account then shared via service agreements. The public record does not establish actual gross margin or revenue ownership for a given Ren, TIFIN, or GiveClear implementation.

## B. TIFIN Give March 2025 Form ADV: disclosed economic streams

| Item | Public disclosure | Interpretation | Missing current evidence |
|---|---|---|---|
| Service fee at ≤ $1m | Generally **30 bps/year**, calculated daily on DAF assets | TIFIN service/technology/admin fee paid by advisory client | Whether 2026 negotiated program and particular donor schedule pass through that amount |
| Investment management at ≤ $1m | Generally **10 bps/year** | Separate from technology and advisor layers | Product scope and actual client fee |
| Service fee at greater than $1m | Generally **10–20 bps/year** | Different *account-balance band* described in brochure, **not** established as progressive tiers | Negotiated rate and applicability |
| Investment management at greater than $1m | Generally **3.34 bps/year** | Separate management fee | Current scope |
| Subadvisory fee | Generally **0–100 bps/year**, paid to DAF adviser | Can materially change total donor expense even if TIFIN headline fee looks low | Whether assessed, by whom, and where disclosed |
| SaaS | **One-time implementation fee plus annual subscription** | Potential non-AUM revenue stream | Absolute prices, contracts and renewal terms |
| Model-portfolio sponsorship | Payments from model sponsors to enhance placement | Incentive/conflict **explicitly disclosed**; not a proven product-bias outcome | Algorithmic/merchandising independence, disclosures, actual revenue |
| Guest giving | 'Nominal' per-transaction donor fee | Additional channel beyond advisory/DAF account charges | Current product availability and actual transaction pricing |
| Brokerage/custody/fund fees | **Separate** from TIFIN's listed management charges | Hidden from headline bps comparison if omitted | All-in returns/net expenses and subservice control |

All figures in this table are **2025 historical regulatory disclosure**, not confirmed 2026 contracting or a DAF donor invoice [E01]. In particular, do not add all streams together without first verifying which apply to a particular legal sponsor and balance.

### Further disclosure details that affect diligence

- TIFIN states clients choose their own custodian/broker; TIFIN retained a third-party trading provider [E01].
- It describes its model-portfolio investment recommendations as **rules-based**, using platform charitable-giving profiles; it warns recommendations are not necessarily profit maximizing [E01]. This relates to the *DAF investment model recommendation*. The later September 2025 **Tax Intelligence** product about donor tax-lot opportunity detection has a different stated purpose and should not automatically be assumed to use identical input data or algorithms.
- Its 2025 ADV reports continuous platform access but says investment positions are not monitored directly by investment advisory personnel, and sponsor custodians supply statements [E01]. Ask what operational exception monitoring is in the current service package.
- SEC IAPD confirms the registered investment adviser record [E02], but regulatory registration is not independent product quality or fee verification.

### Investor diligence question

Can TIFIN retain more economic value *without making donor outcomes worse* by earning platform/SaaS revenue, admin, investment management and sponsored portfolio placement fees? A definitive answer needs actual 2026 fee receipts, contracts, portfolio ranking controls, customer retention and measured contribution/grant operations. The mere presence of multiple fee streams should not be assumed to equal strong margins or conflicts in every account.

## C. Ren/RCF vs direct sponsor fee benchmarks

**Do not conflate these three different account offerings:**
1. **Ren Direct / RCF advisor-managed** [E03,E04]: annual admin 65 bps on first $500k, 35 bps next $500k, 25 bps next $1.5m, 20 bps next $2.5m; **$250 annual minimum**.
2. **RCF donor-directed** [E05]: 60, 30, 20 and 15 bps across corresponding tiers; **$250 annual minimum**. This is a *different product category* from an advisor-managed account.
3. **Fidelity Charitable individual Giving Account** [E06]: 60, 30, 20 and 15 bps over those tiers; **$100 annual minimum**, with investment expenses additional.

**DAFgiving360**, formerly Schwab Charitable, publishes 60/30/20/15 bps on the corresponding first four tiers [E07]. We could not establish a comparable minimum annual fee in the reviewed public source, and for its core pools the charge is incorporated into pooled expenses with periodic rebate mechanics. Do not assume a minimum of zero.

### Modeled annual administrative fee, constant balance and first $5m tiers only

| Synthetic balance | Ren/RCF advisor-managed | RCF donor-directed | Fidelity individual | DAFgiving360 tier calculation* |
|---:|---:|---:|---:|---:|
| $10,000 | **$250** | **$250** | **$100** | **$60** |
| $100,000 | $650 | $600 | $600 | $600 |
| $600,000 | $3,600 | $3,300 | $3,300 | $3,300 |
| $2,000,000 | $7,500 | $6,500 | $6,500 | $6,500 |

*The $60 DAFgiving360 row is a mathematical application of its published rate, **not a confirmed donor invoice or verified minimum fee**. Every number above represents **annual sponsor administrative charge only**, *before* investment and advisor expenses, grant-processing exceptions, cost-of-custody and changes in balance [E03–E07]. The underlying formula is included in [the fee model CSV](../data/daf-admin-fee-scenarios-2026.csv).

**Inference:** For a $10k donor, a $250 minimum is effectively 2.5% of assets per year, while a $100 minimum is 1%. This can erode some reasons to prefund small DAFs and is relevant to earlier 2026 donor tax-fit segmentation. It does not establish all-in fees or that one sponsor should be chosen regardless of features.

### Why we cannot include TIFIN as a fourth comparable donor line

TIFIN's **2025** 30+10 bps at an account ≤$1m is an investment adviser *entity-level fee disclosure*, whereas the above lines are donor-facing *sponsor administration charges*. They differ in who pays, included services and additional sponsor/wealth-firm layers. Adding 40 bps and showing that against 65 bps would be **misleading**. Ask for a current complete program circular for the TIFIN/GiveClear arrangement, including each fee layer and who pays it.

## D. Scale and denominator reconciliation

| Claim | Company/entity | Time period | Units | What it **does not** show |
|---|---|---|---|---|
| $4,674,789 investment-adviser AUM [E19] | TIFIN Give Inc. | Dec. 31, 2024 (2025 Form ADV) | Discretionary regulatory AUM | Sponsor DAF assets on entire platform, 2025/26 distribution, 2026 ARR |
| $372m managed assets [E08] | GiveClear Foundation | 2025 sponsor self-report | Sponsor-level fund balances (self-described) | TIFIN investment-adviser AUM or vendor revenue |
| $83.2m grants, 16,249 grants [E08] | GiveClear Foundation | 2025 sponsor self-report | Charitable **outflow** and count | AUM, ARR, grants necessarily processed by a single provider |
| $200b+ supported assets / 150+ programs [E15] | Ren marketing | Source reviewed 2026 | Platform-serviced assets/programs | Ren's own AUM, revenue or firm profit |
| Retail/admin fee schedules [E03–E07] | Charitable sponsoring organizations | Public page reviewed 2026 | Fee *charged* to account (by product) | Amount retained by technology vendor |

**Do not use an AUM-like statistic as revenue.** A sponsor can hold $372m without the platform capturing every basis point of sponsor charges; a technology company can service more assets than its registered adviser directly manages. A grant dollar is money moving through a workflow, not a percentage-based ARR stream unless priced accordingly.

The GiveClear page links FY2024 audited accounts and Form 990, but the linked files were not accessible for inspection during this review [E18]. Its FY2025 impact values are *self-reported*, not independently confirmed by those inaccessible files. A CPA-level financial model would require actual contract terms and audited sponsor accounts.

## E. Illustrative economics formulas (sensitivity, not estimated vendor results)

- Annual **sponsor admin dollars** = `sum(balance within each balance tier × rate) or minimum annual charge, whichever greater`.
- Annual **platform AUM-linked dollars** = `billable asset base × contracted rate`, if contract uses asset pricing, subject to scope of billable assets.
- Annual **fixed SaaS dollars** = `subscription + recognized implementation revenue`, with contract and accounting treatment specified.
- Annual **investment-management dollars** = `eligible assets × contracted portfolio/adviser rates`, mindful of sponsor ownership, custodial and tier exclusions.
- Annual **grant-infrastructure dollars** = `eligible disbursements × contracted transaction fee + applicable subscription`, adjusted for returns, exceptions and failed deliveries.
- **Provider gross margin** must subtract hosting, staff/reviews/exception resolution, fund accounting, security/audit, support, onboarding, third-party payments, fraud and losses. We do not have sufficient cost evidence to estimate it.
- **Channel value** includes relationship retention and potential investment management, but those are not necessarily platform-company revenues.

For a purely hypothetical $100m billable platform balance:
- 10 basis points would generate **$100,000 gross annual AUM-linked revenue**.
- 20 basis points would generate **$200,000**; 30 basis points **$300,000**.
- 10,000 billable grants at $1, $5 or $10 per grant would generate **$10,000, $50,000 or $100,000 gross transaction charges**.

These are mathematical sensitivities only, **not** actual Ren, TIFIN, Chariot or sponsor contract rates and not margins.

## F. Central strategic question: where is the moat?

**Ren thesis:** Integrated administrative operations, complex assets, accounting, sponsor relationships, and bank-rail payments might create durable switching costs. But donor-facing fees don't tell us Ren's captured share; provider claims of scale need clear denominator and partner/contract stability evidence.

**TIFIN thesis:** Building DAFs into advisor-managed wealth distribution could increase retention and conversion. A channel-embedded white-label platform may be sticky, while the charitable sponsor and nonprofit disbursement portions are separately outsourced. Yet multiple parties divide revenue and controls, and fee/marketing conflicts require disciplined oversight.

**Chariot thesis:** Standardizing nonprofit verification and payout delivery across sponsors may create network value. But the per-transaction grantmaker fee and additional account/bank dependencies could increase marginal cost or reconciliation complexity. Its capability to speed payments cannot be inferred from 'instant' in-network account availability to final external bank receipt.

**Fidelity / DAFgiving360 thesis:** Their direct donor relationships and fee transparency anchor donor alternatives and put competitive pressure on advisor-led bundled fees. Yet the advisor model may provide non-tax benefits not captured by a basic admin comparison.

**Most likely common theme:** The winning long-term economic unit may be **an institutionally distributed charitable relationship with end-to-end verifiable administration**, not simply a more polished donor portal or faster API endpoint. That is an investigation hypothesis, not measured market evidence.

## G. Next verification actions, ordered by information value

1. Obtain **2026 current TIFIN Form ADV Part 2A**, compare Item 4/5/14/15 against 2025 disclosure and SEC IAPD. Do not rely on old rate bands for a live contract [E01,E02].
2. Obtain **complete program-level fee schedules** from actual TIFIN/SEI/GiveClear arrangements, including sponsor admin, TIFIN service + management, subadvisory, SaaS implementation/subscription, custody, investments, Chariot and unexpected payments.
3. Get **Ren's institutional partner price schedule** and segmentation by RCF-backed versus other sponsor programs. The retail Ren Direct fee schedule is not a proxy for Ren's enterprise technology ARR.
4. For TIFIN model sponsorship disclosures, request an evidence-backed explanation of fund visibility/placement, portfolio ranking, advisor independent choice, donor disclosures and material conflict mitigation. Do not allege wrongdoing from disclosed incentives alone.
5. Obtain 2025 GiveClear public Form 990 and audited statements where officially accessible; calculate sponsorship/operating expense per account and per completed grant only after consistent units and attribution.
6. Collect Chariot's **actual grantmaker contract prices**, effective fee by rail and claim status, bank arrangements, KYC false positives, delayed checks, refunds and reconciliation staff minutes.
7. Distinguish **retained advisor relationship and fee rights** from legally owned DAF assets. Verify how asset portability, custodian replacement and successor advisors affect distribution economics.
8. Run scenarios at 10K, 100K, 600K and 2m under **full all-in fees** and grant volumes, without assuming every enterprise program uses the same tiers.

## Research integrity

All findings are dated and source-specific. None establishes vendor revenue, profitability, contract allocations, investment recommendation bias, actual partner cash flows, independent audit opinions, comparative business success, or consented live demonstrations. The TIFIN ADV is a **2025 historical disclosure** and may have changed. No private vendor/client data is included.

Related research: [Ren–TIFIN operating model](ren-tifin-chariot-deep-dive-2026-11-11.md), [donor tax fit](donor-tax-personas-2026.md), [tax opportunity comparison](tax-opportunity-lifecycle-2026-11-11.md).
