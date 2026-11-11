# Ren: concentration, contract durability, ownership and service-cost evidence
**Public-source assessment | November 11, 2026 | Covers Ren at `reninc.com`, not unrelated `tryren.com`**

## Decision summary

The existing **independently audited** RCF financials establish **$19,225,546 paid by Renaissance Charitable Foundation (RCF) to Ren in FY2024**, under a related-party administrative-services agreement with a **98% fee-share basis on *individual fundholder account* administrative-fee income** [N04]. The five-year FY2020–FY2024 disclosures were transcribed in [the earlier study](audited-revenue-and-client-cohorts-2026-11-11.md).

**New evidence:** Ren's [official Master Services Agreements page](https://www.reninc.com/master-service-agreements/) [N03] publishes separate **June 2023** templates for **Renaissance Acquisition Company LLC (Ren service provider)** [N01] and **Renaissance Charitable Foundation (RCF sponsor)** [N02]. Both contain a default one-year automatic renewal framework, requiring notice generally **60 days before** the work-order expiration, certain end-of-quarter early-termination charges, and provisions on customer materials and licensed deliverables. These are useful **published standard contracting terms**, not signed agreements for a particular client.

**Further finding:** Ren's investor capital and ownership arrangements changed in **July 2023** (Bain Tech Opportunities and Valeas; Bain describes the investment and Valeas calls it a control buyout) and **October 2025** (Great Hill Partners growth investment, with Bain continuing as a shareholder) [N05–N08]. Investors' announcements do not disclose company EV, equity price, debt, recurring-revenue amount, debt leverage, enterprise renewal cohorts, or consolidated margins.

**Bottom line:** We can establish one material **RCF→Ren gross service-fee flow** and publicly stated contract mechanisms. We **cannot** calculate Ren's fraction of total company revenue, EBITDA, software-versus-service margin, independent-sponsor revenue, RCF dependency in 2026, or actual customer churn. Treat any concentration percentage as **conditional algebra**, not an observed result.

## 1. Three contracts, three different parties

| Instrument | Supplier → buyer | What is established | What it does *not* establish |
|---|---|---|---|
| **Audited related-party RCF Administrative Services Agreement** | **Ren** provides services to **RCF** (actual related-party agreement cited in RCF audit) | FY2024 actual RCF→Ren payment **$19,225,546**, 98%-based individual-fundholder-fee formula [N04] | Signed full contract, term, termination rights, full schedule of work, actual Ren operating costs or general enterprise fee levels |
| **Renaissance Acquisition Company LLC public MSA template** | **Ren** → institutional **Customer** who signs order/work orders [N01] | Published general terms: work orders, renewals, defaults, termination, material ownership, liability | Whether **AEF**, **RCF**, or any specific current sponsor uses it without modifications, or the fees charged in any work order |
| **RCF public MSA template** | **RCF sponsor** → institutional **Customer** [N02] | Sponsor-facing arrangement may have its own order, renewal and exit terms | It is **not** the agreement under which RCF pays Ren 98% of certain fundholder fees |

**Important correction to possible conflation:** The fact that the RCF sponsor MSA and Ren service-provider MSA have very similar boilerplate does **not** mean they implement the 98% related-party financial arrangement. Their parties and directions of payment are different.

## 2. Standard contract durability and exit economics

The public Ren provider template [N01] discloses:

| Provision | Published default | Diligence implication |
|---|---|---|
| `§1.2` | Every mutually executed work order forms a separately scoped agreement; MSA generally controls unless a work order explicitly overrides a provision | Customer-level product, fee, renewal and unit economics can differ |
| `§1.3` | Change order can produce amended deliverables and payment schedule | Changes can produce revenue and implementation expense, neither of which is necessarily recurring |
| `§3.1–3.2` | Fees set **in work order**; otherwise undisputed invoices due in 30 days | Public MSA contains **no client-specific price or contract ARR** |
| `§4.1` | Initial term defined per work order; subsequent automatic **one-year renewals** unless **60-day prior written notice** | Mechanism for contract continuity, **not** proven logo retention or guaranteed cash |
| `§4.2–4.3` | Notice of material breach and generally **30 days to cure** | Service termination and customer/supplier remedies depend on exact facts |
| `§4.4` | For some termination types, customer pays projected fees through **end of termination quarter** | Bounded default exit charge, **not** a multi-year cancellation penalty; work order may override |
| `§4.5;5.1` | Ren returns **Customer Materials** upon exit or earlier request; customer owns those materials | No guaranteed canonical complete ledger export, schema, migration labor, retention clock or validation SLA |
| `§5.2;5.4` | Ren generally owns inventions/deliverables, with limited object-code license after final payment; work order can change treatment | IP rights and dependence on vendor tools can matter even when user-supplied data belongs to customer |
| `§2.3;5.3` | Ren may use subcontractors and has specified responsibilities, while third-party products carry their own terms | Asset custody, payment processors, compliance and hosting remain distinct dependencies |
| `§7.2;9` | Broad warranty limitations and generally a liability cap tied to **fees paid under the applicable work order during the preceding 12 months**, with exceptions | Contractual incident loss allocation matters but does not establish actual reliability, insurance or SOC controls |
| `§10.4` | Assignment ordinarily requires other party's written consent | Acquisitions, program swaps and contract novation may require third-party permissions |
| `§5.5` | Services said to be **nonexclusive** | No basis to assert a universal exclusive-client lock-in clause |

The work-order-specific caveat appears throughout. This table is **general commercial contract research, not legal advice or an interpretation of signed AEF/RCF contracts**. The template's PDF footer says “Confidential,” but the company deliberately provides it on a public legal-documents page. We record **summaries and citations**, not a redistributed copy or private orders.

The public **RCF sponsor** template has similar renewal/return-of-materials provisions, but it applies to a **different supplier**, RCF itself [N02]. The signed arrangement governing the related-party RCF→Ren payments was **not** located. Never use either standard template to calculate an actual RCF→Ren cancellation penalty.

**Real-world counterexample to absolute lock-in:** AEF migrated to Ren in 2025–26 while remaining AEF as the legal sponsor [N10,N11]. That proves sponsor-level platform replacement can occur, not what the incumbent charged or whether Ren was bound by the public standard MSA. AEF's new portal history constraint is detailed in the [switching study](revenue-retention-and-switching-2026-11-11.md).

## 3. RCF dependence: quantitative sensitivity without pretending we know Ren revenue

**Observed numerator:** the **$19,225,546 paid by RCF to Ren in FY2024**.  
**Unknown denominator:** **Ren consolidated recognizable FY2024 revenue, excluding intercompany eliminations** and subject to appropriate accounting recognition. Because the financial statements audited are RCF's and not Ren's, it is unsafe to assert that *every paid dollar* equals FY2024 recognized Ren revenue.

If and **only if** the RCF payment is comparable to recognized Ren revenue, and comparable **non-RCF revenue** is `X`, a hypothetical contribution concentration could be modeled as:

`RCF_equivalent_share = 19,225,546 / (19,225,546 + X)`

| Hypothetical total comparable non-RCF annual revenue | Hypothetical RCF-equivalent share |
|---:|---:|
| $0 | 100.0% |
| $10 million | ~65.8% |
| $19.23 million | 50.0% |
| $40 million | ~32.5% |
| $60 million | ~24.2% |
| $100 million | ~16.1% |

**Thresholds under the same deliberately strong assumptions:** Ren would require *more than* **$19.23m** comparable non-RCF revenue for the RCF-equivalent stream to be less than **50%**; more than **$57.68m** to be below **25%**; and more than **$173.03m** to be below **10%**. Those are **break-even identities, not estimates of Ren's actual customer mix**.

The machine-readable [sensitivity](../data/ren-rcf-dependence-sensitivity-2026.csv) includes additional illustrative other-revenue cases and **purely hypothetical service-cost** ratios. Its cost residual is **not** Ren EBITDA, gross profit, or a reliable margin. Without Ren's cost-to-serve ledger and other customers' invoices there is no responsible way to transform RCF's administrative payments into corporate earnings.

### Why 2020–2024 growth cannot be labeled “organic”

RCF payments increased from $7.51m in 2020 to $19.23m in 2024. Their growth can reflect sponsor new fund opening, market-return-driven billable balances, price/tier changes, adviser/custodian mix, service scope, and contract fee-share changes. We already know the formula moved **from 95% to 98% in 2023**, which mechanically affects received fees [N04]. Ren as a wider company also bought **Pinkaloo in 2021** and **Stellar/iPhi in 2023**, changing product mix and customer base [N09].

We cannot separate **organic price, organic volume, acquisitions, investment gains, or customer churn** from the audited RCF payment series alone. Nor can a fee increase prove better cost margins or renewal rate.

## 4. Ownership and financing chronology

| Date | Publicly documented transaction | What we know | What we do not know |
|---|---|---|---|
| **July 26, 2023** | Bain Capital Tech Opportunities and Valeas Capital investment [N05,N06] | Valeas calls the transaction a **control buyout**; Ren disclosed strategic growth investment | Debt/equity split, valuation, fees, cash-flow model, actual leverage, enterprise ARR |
| **October 28, 2025** | Great Hill Partners growth investment [N07,N08] | Great Hill joined investors; deal advisor says Bain continues as significant shareholder; board representation broadened | Equity percentages, seller proceeds vs fresh capital, post-deal EV, loan covenants, software vs services valuation |
| **2021 and 2023** | Pinkaloo and Stellar/iPhi product acquisitions [N09] | Acquired assets can change product/customer composition | Reconstructed pre/post acquisition customer cohorts, acquired ARR or integration economics |

**Investment implication:** Two rounds of private-equity participation and an acquisition history make a *pro forma*, same-product/same-customer bridge essential. Comparing public marketing-supported assets in 2023 vs 2026 is not a valid substitute for audited organic net retention or acquisition-adjusted growth.

Some [historical reporting](https://www.ibj.com/articles/indianapolis-based-ren-inc-snags-big-investment-from-bain-capital-fund) describes a large 2023 financing and roughly 200 customers [N13]. Those are dated secondary claims and not audited 2026 customer/contract denominators. Do not infer company valuation from a general PE fund's typical check size or a 2025 minority transaction.

## 5. Available 2025–2026 financial evidence and what remains closed

The [RCF legal resources index](https://renaissancecharitable.org/legal-resources/) [N12], as reviewed Nov 11, 2026, currently lists audits through **FY2024** and Forms 990 through FY2024. No publicly accessible **FY2025 audited RCF→Ren payment** was established in this review. This is an *availability limit*; **2025 payments were not zero**.

Likewise:
- **AEF** confirms Ren selected July 2025 and integrated April 2026, but does not disclose an executed price sheet, term, annual vendor fees, or implementation costs [N10,N11].
- Ren's public MSA has **no dollar price**. Customer-by-customer work orders determine fees [N01].
- Neither RCF's audit nor the MSA provides Ren's payroll, operating costs, R&D, hosting, grant-review staffing, third-party bank expenses, servicing volume by account, debt cost, interest or taxes.
- Sponsor-owned charitable AUM and grants are **not Ren revenue**. Supported-asset figures are **not billable revenue** without a contract bridge.

## 6. Questions that would resolve concentration and economics

**Tier A: minimal evidence package** (may be answerable without confidential contracts)
1. What is Ren's FY2024 and FY2025 total *recognized* revenue by administrative services, software license/subscription, and payments, each reconciled to consolidated company statements?
2. What share of Ren revenue came from **RCF**, and what entries reconcile RCF's **$19.225546m** audited FY2024 payment to Ren's company accounting?
3. How much of Ren's **2025 or 2026** annual revenue is generated by unrelated institutional sponsors and wealth firms, distinct from related-party RCF fees?
4. What was the percentage of first-day 2024 recurring billed revenue still billed to the same contractual customers 12 months later, excluding acquired and newly signed contracts? Show GRR/NRR separately.
5. Is the published June 2023 provider MSA currently used for **Ren Direct, AEF, and iPhi**, and what work-order exceptions govern actual customers?

**Tier B: stronger investment diligence**
6. Provide actual **RCF related-party agreement**, independent board review and renewal history, service-level responsibility and signed change from 95% to 98%.
7. Provide gross profit by **service bundle**: software hosting, accounting, donor service, grant screening, payment processing, compliance and admin, with volume-based activity drivers.
8. Provide pre/post Pinkaloo and Stellar acquisition pro forma contracts, new logo/customer records, churn and revenue bridge.
9. Explain Great Hill 2025 investor rights and any change-of-control or assignment restrictions under signed customer agreements.
10. Produce verified five-year transfer/exit evidence including complete fund ledgers, donor grants, audit history and sponsor-owned records.

**Tier C: risk tests**
11. If RCF administrator pricing shifted materially or RCF switched providers, what services are independently deliverable to other third-party sponsor contracts?
12. If sponsors' AUM declines 20% from markets or giving, how much of **Ren's own recognized revenue** is fixed versus asset-linked, and how do labor/hosting costs flex?
13. What fraction of revenue is covered by customer-written SLAs and legally enforceable data-export guarantees rather than best-efforts delivery terms?
14. What portions of operating costs are related-party transfer prices, and have they been independently assessed?

## 7. Conclusions bounded by evidence

**Observed:** One material RCF→Ren paid-service stream, published **unsigned** standard MSA terms with renewal/exit/IP provisions, named public sponsor customer AEF, two rounds of PE backing, and prior acquisitions.

**Inferred:** The structure *could* support recurring services and switching friction. That is a hypothesis about contract resilience and customer costs.

**Unknown:** Ren company size and margin, organic revenue, concentration, current year reported fees, signed AEF contract, actual 2026 renewals and churn, valuation and capital structure.

**Recommendation:** The highest-value next output is a **signed-contract, company financial and service-cost bridge**, not another asset-serviced market-share number. A public-source memo can document the questions, but cannot manufacture their answers.

See [clause and evidence register](../data/ren-public-contract-clauses-2026.csv), [source register](../data/ren-contract-concentration-sources-2026.csv), [sensitivity](../data/ren-rcf-dependence-sensitivity-2026.csv), and [audited payments](../data/rcf-ren-audited-admin-payments-2020-2024.csv).

**Research controls:** Public web records only. Published templates are quoted/summarized in context rather than uploaded. No restricted employer/client information, confidential signed work orders, investor-only data, or expert-network client details are included.
