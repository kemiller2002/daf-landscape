# Revenue quality, customer retention, portability and switching costs in DAF technology

**Public-source assessment as of November 11, 2026.** A comparative analysis of Ren, TIFIN Give, and Chariot. All conclusions are based on public primary sources and explicitly labeled hypotheses. **No contract-level financial statements, renewal cohorts, executed migration test, private customer agreements, vendor accounts, or client intelligence were obtained.**

## Executive conclusions

1. **The primary customer may not be the donor.** A DAF sponsor legally controls donated assets [R01]. In TIFIN Give's March 31, 2025 Form ADV, the **sponsoring 501(c)(3) entity is the advisory client**, while donors and DAF advisers are authorized participants [R10]. Ren markets institutional *platform* and *branded* relationships, in addition to direct/sponsored fund accounts [R07]. Chariot operates different agreements for DAF providers, nonprofits, and payment services [R12,R13]. Thus a single wealth firm's DAF offering can contain several overlapping but separately terminable contracts.
2. **Recurring payment mechanics are not recurring *revenue quality*.** TIFIN's 2025 ADV describes billable, asset-linked technology/service and investment fees plus recurring SaaS subscriptions [R10]; its September 2026 group-level public terms default to subscriptions that auto-renew, subject to any controlling customer-specific agreement [R09]. **None proves net retention, actual revenue receipts, multi-year locked-in contracts, gross margins or renewals for TIFIN Give**. Ren's marketed scale is not its annual recurring revenue [R07]. Chariot's published 2026 nonprofit terms state default *DAFpay* fees of **2.9% of donation amounts (rounded to the nearest dollar)** absent fundraising-platform agreements, with subscription alternatives; its separate *Disbursements* business is not priced by this rule [R13].
3. **Provider switching can occur at several layers.** The donor may recommend an account-closing grant to a new sponsor, with original sponsor approval [R02,R03,R01]. A *sponsor* can replace donor portal and administrative software without changing the sponsor entity, demonstrated by American Endowment Foundation's Ren migration [R04,R05,R06]. A wealth firm may seek to switch its advisor integration or DAF sponsor, subject to contracts and approved account relationships. An API connectivity or payment service could be replaced without replacing the fund ledger, subject to permissions, reconciliation and agreement-specific limits [R12,R15].
4. **There is a documented nontrivial migration consequence.** AEF sunset its previous DonorCentral portal on October 31, 2026. The replacement Ren-powered portal displayed only the **past two years of account history**; older donor records must be requested through AEF staff [R06]. This is direct evidence of historical *self-service accessibility discontinuity*, **not** proof of irrevocable data loss, poor system integrity, higher costs or donor departure.
5. **Public contracts expose different friction, not automatic customer captivity.** TIFIN's general group terms give clients ownership of user-provided content, allow product and data use under a broad license, and end service access on termination, with customer-specific agreements controlling conflicts [R09]. Chariot's DAFpay provider addendum grants participation under a separate product scope, may be terminated, and permits retention of some aggregated/deidentified information [R12]; its nonprofit contract describes data exports but ends platform and deposit-account access after termination with 30 days' written notice from nonprofit [R13,R22]. These provisions inform negotiation priorities, **but they do not establish full data portability or fees under any enterprise agreement**.
6. **Neither company has a public, reliably comparable retention metric in the documents reviewed.** For Ren: no institution-by-institution renewing ARR, logo retention, gross revenue retention, net revenue retention or cancellations established. For TIFIN: public partnership announcements and historic ADV fees establish channels, not realized recurring contractual revenue. For Chariot: product usage and contract fee default are evidence of potential revenue flows, not active paying-client cohorts or customer lifetime value.

## 1. Define the actual units of retention

| Unit | Paying/decision-making actor | What might persist after another layer changes? | Appropriate metric | Incorrect proxy |
|---|---|---|---|---|
| **Legal sponsoring charity** | 501(c)(3) board/authorized officers | Donor fund assets, legal grant obligations; may change platform | Contract renewals, sponsor fund/account retention, migrated versus terminated programs | Ren “assets supported” as Ren revenue |
| **Platform/administrator agreement** | Sponsor, wealth enterprise, or other institution named in agreement | Platform access may terminate; sponsor may remain; data transfer costs | ARR by *unique paying legal customer* and product, billed recurring amounts, GRR/NRR | Count of branded portals and “powered” programs without fees |
| **Advisor/wealth-firm channel** | Wealth company and registered advisors, subject to sponsor/custody policy | Donor relationships, possible ongoing investment management | Advisor participation, conversion, assets remaining in authorized advice, relationship continuity | Charitable assets portrayed as donor-owned wealth |
| **DAF account and donor advisory role** | Sponsor owns assets; donor advises | Donor may recommend grant to another sponsor; grant rights depend on policies | Donor fund/account attrition, funded balances **net of grants**, advisor changes, grant activity | Fall in DAF balance always called churn |
| **Investment adviser/model relationship** | Sponsor/institution as client; DAF adviser may have sub-advisory role | Custodian and adviser assignments may differ from portal | Billed advised assets, advisory-fee retention, custody and model changes | Registered adviser AUM treated as platform-serviced sponsor assets |
| **Payment/DAFpay integration** | DAF provider, nonprofit or grantmaker depending product | Grant request lifecycle and historical payment reconciliation must transition | Eligible billable transactions, active integrated payers, net fee per grant, error-adjusted receipts | Gross grant dollar volume treated as platform ARR |
| **Nonprofit account/deposit workflow** | Nonprofit controls account and payout instructions | Charity may keep operating independently but loses tool access on termination | Active paying nonprofits, fee/volume cohorts, time to export and reconcile | Registered nonprofit count assumed to be paying customers |

**Interpretation:** Because DAF funds are charitable-owned after contribution, **“assets retained in the wealth ecosystem” is economic distribution language, not proof that the original donor legally controls that wealth** [R01,R08,R17]. A wealth manager can retain a relationship while a technology vendor changes, and a sponsor may retain grant control while a disbursement provider changes.

## 2. Public retention evidence, separated from conjecture

| Provider / segment | Documented recurrent fee or contractual mechanism | Evidence of migration and ownership | What cannot be responsibly concluded |
|---|---|---|---|
| **Ren platform and administration** | Branded and platform relationships marketed, enterprise contract terms not public [R07,R08]. Distinct sponsor admin fee tiers in prior research. | AEF chose Ren July 2025 and completed transition by April 2026; DonorCentral closed Oct 2026 with 2-year self-service history [R04,R05,R06] | Ren's customer retention, contract tenor, software gross margins, recurring enterprise revenue, donor retention after AEF migration |
| **TIFIN Give / GiveClear** | 2025 ADV describes negotiable recurring asset-linked administrative/technology and management fees, and SaaS implementation + ongoing subscription [R10]. 2026 TIFIN Group terms state default auto-renew subject to separate software agreement [R09]. | GiveClear is sponsor and TIFIN is platform in documented ecosystem [R16]. Client-provided content ownership recognized in broad group terms, but access ends upon termination [R09]. | 2026 TIFIN Give signed customer contracts, 2026 revenue, NRR, renewal rates, automatic portability or how each fee stream is allocated |
| **Chariot DAFpay** | Nonprofit contract default 2.9% of donation amount absent fundraising-platform arrangement; Chariot Subscription can substitute for transaction fees [R13]. Signed provider addendum separately governs provider integration [R12]. | Provider may terminate participation; nonprofit account has 30-day notice for termination. Data export appears as a dashboard feature, but terminated account loses access [R12,R13,R22]. | Percentage of customers paying default 2.9%, net take rate, margin, actual 2026 fees, SaaS ARPU, retention, data export SLAs |
| **Chariot Disbursements** | Separate service with grantmaker transaction fees discussed in the prior economics analysis [R13,R16]. | Legally different product/addendum; no universal contract migration clause verified. | Disbursements take rate from DAFpay terms, exclusivity with TIFIN, per-grant net income or retention |
| **Wealth partner channels (SEI, Confluence)** | TIFIN and other vendors announce signed partnerships and new launches [R16,R18]. | Named distribution and sponsorship relationships [R16,R18] | Contract annual value, number of paying donor households, cancellation penalties, activation rate, retained adviser assets, or logo retention |

**Specific TIFIN contract caution:** Its group Terms and Conditions expressly say a separate Software & Services Agreement can supersede the published general terms [R09]. Those terms also restrict third-party disclosure of competitive benchmarks by users of the service. **Public-domain analysis is not the same as accessing a vendor account under those terms.** Any future credentialed head-to-head test must establish a written benchmark/publication permission before distributing results [R09]. The same general caution applies to Chariot's nonprofit terms, which restrict competitive use and publication of performance information [R13]. Do not use a login to evade contractual limits.

## 3. Three different ways a DAF program can leave a provider

### Scenario A: donor-level transfer to another legal sponsor

The donor recommends a grant to a different sponsoring 501(c)(3); the existing sponsor retains decision authority, and the receiving sponsor maps it to the new DAF account. Fidelity Charitable provides the incoming sponsor details [R02]. Renaissance Charitable directs prospective customers to submit an **Account Closing Grant** from the previous DAF provider [R03]. This proves there are published *inbound* mechanisms, **not** that every outgoing sponsor must approve the request or will transfer the full amount, historical records, advisor rights, or legacy instructions. Confirm eligibility, grants pending, minimum balances and closure fees.

**Potential frictions:** donor and successor reconsent, grant restrictions, beneficiary arrangements, sold asset timing, sponsor acceptance, investment model liquidation, cost basis/record history, historical grant receipts, access to old statements.

### Scenario B: institutional sponsor retains the DAF funds but swaps its platform

AEF's public announcements provide the strongest real-world case: July 2025 Ren selection [R04]; April 2026 fully on Ren [R05]; old DonorCentral portal retired Oct. 31, 2026 with only **two prior years** of history in the new portal [R06]. The legal sponsor remains AEF. An institution can thus leave old software without a sponsor-to-sponsor asset transfer, but donor historical data can cross a new self-service boundary. The AEF evidence does **not** quantify migration expense, AEF client attrition or platform downtime.

**Potential frictions:** dual-run period, historical data extraction, charter/sponsor control of sponsor-owned records, casework, templates, grant/receipt event IDs, AML/vendor verification, service request backlog, permissions and MFA resets, bank and custodian feeds, source-of-truth cutover, continuity of pending grants, tax receipts.

### Scenario C: replace payment infrastructure without replacing a DAF ledger

Chariot's October 2026 DAFpay Provider Addendum makes explicit that DAF providers retain grant review, approval and disbursement decisions; the integration can be APIs or other provider-specific methods [R12,R15]. Changing a payment/checkout provider is thus conceptually separable from changing the legal sponsor or fund accounting. However, historical payment statuses, charity identification, returns, donor tracking, bank authorizations and outstanding grants may not travel automatically.

**Potential frictions:** reconciling old/new tracking IDs, nonprofit bank destination permission, repeated grants, pending settlement/returns, DAFpay versus Disbursements contracts, taxpayer/donor privacy and data retention. The DAFpay Provider Addendum is **not** itself proof of portability for Chariot Disbursements [R12].

## 4. Actual contract details worth a buyer's attention

### TIFIN Group public general software terms (Sep 10, 2026) [R09]

- General subscription auto-renews until termination, **unless its governing Software & Services Agreement says otherwise**.
- Service access ceases upon termination; fees are generally noncancelable and nonrefundable unless exceptions apply.
- The **client/user retains title to Provided Content**, but terms also grant a broad license for the vendor and service providers to use it for service provision, analytics, product development and related purposes. Ownership is not equivalent to an assured machine-readable export.
- General provisions discuss data retention limits and disclaimer of responsibility for lost stored content. Verify the exact separately negotiated enterprise data retention/backup obligations.
- The terms restrict disclosure of benchmark or competitive evaluations by service users unless permission exists.
- No public automatic 30-, 60- or 90-day complete migration export obligation was established for a TIFIN Give institution from this generic page.
- Those provisions cannot be represented as a private SEI or GiveClear agreement.

### Chariot public DAFpay Provider Addendum (Oct 14, 2026) [R12]

- Participation covers **DAFpay** provider access only, not the separate Gift Processing or Disbursements services.
- DAF providers retain legal/operational responsibility to approve and execute grants.
- Chariot may add/retire integration methods with reasonable efforts to notify material changes; providers should request API version stability commitments.
- Chariot may use aggregated/deidentified provider data for lawful purposes, and retain information as required; contractual history-export and deletion boundaries must be negotiated.
- Termination of addendum does not automatically terminate the underlying nonprofit terms, and an independently signed agreement supersedes the addendum if inconsistent.

### Chariot public Nonprofit Terms (Oct 14, 2026) [R13,R22]

- DAFpay donation fees default to **2.9%**, rounded to nearest whole dollar, **only when no alternate fundraising-platform contract sets fees**, with subscription-based alternatives (including possible no-per-transaction-fee volume).
- Nonprofit account termination requires **30 days prior written notice** from user. Post-termination platform, donor dashboard and deposit account access ends. It also must remove embedded platform elements.
- Platform provides donation/payment history and **data exports** as product functionality, but the text does not guarantee data export completeness, format, retention or a post-termination self-service window.
- 2.9% is **not the Chariot Disbursements grantmaker fee** and must not be used as that product's revenue rate.
- Actual payer, fee deductions, invoicing, subscription tiers and grants forwarded through nonprofit platform agreements may differ materially.

## 5. How to calculate retention without distorting it

### Four essential measurements

1. **Enterprise logo retention**, defined as: unique legal customers paying at the cohort opening who still pay at cohort close / opening paying customers. Report by sponsor, institution, and other buyer type; a renamed product isn't a churned institution.
2. **Gross revenue retention (GRR)**: (starting annualized contracted recurring fees − realized lost recurring fees from churn − fee contraction) / starting annualized contracted recurring fees, **excluding expansion and new customers**.
3. **Net revenue retention (NRR)**: (starting recurring − churn − contraction + expansion from the same opening cohort) / starting recurring. **Do not count new logos**.
4. **Asset-linked recurring revenue bridge**: separate changes in actual asset value or account balance from contract price, account openings, grants, withdrawals, investment results, customer departures, and tier changes. A sponsor's grant payout can reduce billed assets **without the institution ending its contract**.

Suggested cohort fields: customer legal entity ID, product, contract start/end, renewal/option, initial recurring run rate, fixed SaaS, billable average balance, fee rate/tier, transactions and payment source, net paying fees, end-of-period cohort size, expansions/contractions, customer cancellation reason, platform migration date, data-extract service commitments, legal sponsor ID, advisor/custodian link.

**Important:** AUM-linked fees fluctuate; calling them 100% “contractually recurring ARR” without a normalizing convention is potentially misleading. Distinguish *contractual fixed recurring* from *asset-linked recurring/variable* and from *usage/transaction* and *one-time implementation* income.

### Attribution rules

- **Ren:** no public ARR, churn or annual fee breakdown established. Its marketing claim of assets “supported” is a platform service footprint, not gross/recurring revenue [R07].
- **TIFIN:** historical ADV establishes type of fees; no publicly obtained customer cohort invoice data [R10].
- **Chariot:** nonprofit terms show default gross pricing and alternatives; not the fraction of transactions on each plan nor net fee revenue. Network dollar throughput is **not** revenue [R13].
- **Advisor economics:** retention of an authorized relationship or ability to advise charitable assets should not be equated with the donor owning the assets; sponsors legally own them [R01,R08,R17].

## 6. Switching cost rubric and real deliverables

A good migration test must *physically run* through all of these. See [switching-cost-control-matrix.csv](../data/switching-cost-control-matrix-2026.csv) for control-by-control evidence and [migration-runbook-2026.md](migration-runbook-2026.md) for adversarial cutover cases.

| Component | Why it may be difficult | Evidence needed |
|---|---|---|
| Legal sponsorship | Sponsor policy, charity acceptance, grant restrictions, new fund creation | Closing-grant process, written permission and transfer receipt |
| Donor/advisor access | Role IDs, delegated authority, SSO/MFA, donor consent | Back-to-back authorization and revocation tests |
| Ledger/positions | Transactions, lot data, NAV and daily units, custody balances, fee history | Transaction-complete export and recomputed trial balance |
| Grants and payees | Pending approval, eligibility, pledged grants, restrictions, recipient status | Grant reference ID mapping, approval lineage and no duplicate payouts |
| Historical statements | Donor tax receipts, quarterly statements, grant letters across multi-year history | Historical access or permanent sponsor-controlled archival with SLA |
| Payment pipeline | Bank account, nonprofit verification, checks/returns and reconciliation | Cutover reconciliation; no open unsettled grants left unowned |
| Contracts/data | License, renewal notice, fees, historical export rights, IP and confidentiality | Executed agreement, DPA, exit addendum, capped fees, retention guarantees |
| Operations/change | Staff retraining, service tickets, brand migration, support load, continuity | Dual-run case counts, SLA breaches and user impact measured |

Define switching cost as **auditable migration labor + externally contracted services + dual-run costs + verified exception handling + data reconstruction + contract/termination fees + measurable temporary business disruption**. All terms must be grounded in actual records before assigning dollars. High switching cost is not itself proof of high vendor retention, customer satisfaction, or pricing power.

## 7. Revenue quality hypotheses worth testing

| Hypothesis | Supporting public fact | What could falsify it |
|---|---|---|
| **H1: Ren's integrated administration increases institutional switching friction.** | AEF's multi-stage platform migration and historical access divergence [R04–R06] | Standard complete exports, low migration labor, short implementation and frequent customer exits |
| **H2: TIFIN may have a more scalable high-margin software revenue component.** | 2025 ADV explicitly describes recurring SaaS subscriptions and implementation fees [R10] | Most revenue actually being low-margin servicing/advisory allocations or implementations; little fixed recurring contract value |
| **H3: Wealth integration creates durable distribution relationships.** | Ren and TIFIN both market keeping investments with adviser/firm [R08,R17] | Advisors lose custody/fee relationships, little donor conversion, firm churn, or mobility regardless of vendor |
| **H4: Chariot's multi-sided integrations add retention through payout data and nonprofit coverage.** | Public donor/DAF provider/payment APIs, donor privacy and history, nonprofit account ties [R12–R15] | Low provider/nonprofit reuse, easy direct bank replacements, high transaction fees, high return rates or little data reuse |
| **H5: Asset portability is not equal to full historical portability.** | AEF portal only presents two years of history post-transition [R06] | Audited automated full-history export/canonical mapping with unrestricted client self-service across new/old systems |
| **H6: Reported assets and platform market share can be decoupled from software revenue.** | Ren claims powered assets; TIFIN ADV fee architecture [R07,R10] | Evidence all platform-serviced assets are billed to the vendor at the same rate and fully recognized as its revenue |

These are unverified explanations. **None is a company valuation**, and the publicly available material does not establish market dominance or recurring retention superiority.

## 8. Prioritized document request for proper investment diligence

1. **Revenue cohort and contracts.** Five-year contract-by-contract recurring revenue bridge, first five paying customers by cohorts, GRR/NRR, customer gross margin, top-five concentration, fixed vs asset-linked vs per-transaction vs implementation/marketing revenues, reconciled to signed agreements and financial statements.
2. **Signed terms.** Three representative current sponsor, wealth partner, and disbursement/nonprofit contracts, with redacted commercial terms if needed, including renewal, notice, assignments, data access and transition assistance, change of control, termination fees and exclusivity.
3. **Unit economics.** Annual cost-to-serve per sponsor and active fund; staffed vetting, financial reporting, custody feeds, security, managed payouts, bank fees, check returns, KYC exceptions, payment fraud loss, onboarding and customer success.
4. **Portability benchmark.** Demonstrate full export of five synthetic years of grants and receipts with zero exceptions, sponsor-to-sponsor account-closing grant where permitted, and a platform-only migration keeping the same legal sponsor.
5. **Chariot pricing segmentation.** Number of nonprofits on default 2.9% DAFpay terms vs fundraising-platform overrides vs subscription plans; gross and net pricing per donation; separate Disbursements grantmaker charges.
6. **TIFIN specific agreements.** Confirm whether September 2026 group terms apply to TIFIN Give and are overridden by actual enterprise contracts; obtain current 2026 ADV and sponsor-level contract/invoice breakdown.
7. **Ren product/contract map.** Separate Ren-owned branded programs, RCF-backed sponsor programs, and independent sponsor relationships like AEF; identify contracted annual fees, products and exit terms.
8. **Risk and oversight.** Current SOC 2 scoped reports, SOC 1 for accounting where material, data handling and incident reporting; inspect sponsor and vendor financial statements without conflating legal entities.
9. **Marketing data reconciliation.** Prove denominators for platform-serviced assets, sponsor assets, adviser AUM, grant throughput, number of active paying donors, and entity attribution.

## 9. Important public-source correction to earlier SOC 2 claim

AEF's **July 23, 2025** announcement claimed philanthropic Ren (`reninc.com`) held **SOC 2 Type II** [R20]; its **April 8, 2026** announcement called Ren **Type I** [R21]. Our earlier research wrongly dismissed the 2025 Type II claim as belonging to the unrelated `tryren.com` company. That is incorrect: **AEF itself published the Type II claim about philanthropic Ren.** We have now marked the status **conflicting**, and have revised the original assessment, matrix and comparison. Neither announcement is an auditor report. Only a direct review of actual scoped reports, observation periods and the associated legal entity can reconcile the statements.

## 10. Research conclusion

**Revenue quality remains unknown.** Public documents prove that Ren has institutional software/operations relationships, that TIFIN publicly discloses several fee streams with different persistence characteristics, that Chariot has contractual API/platform relationships and multiple fee paths, and that sponsor/portal transitions can involve actual historical-data consequences. They do **not** prove which company has higher retention or investor value.

The strongest next evidence is not another product brochure. It is a **matched cohort of paying contracts and a witnessed five-year migration test**. Until that exists, rank the *evidence gaps and plausible moat mechanisms*, not the vendors.

**Source register:** [revenue-retention-sources-2026.csv](../data/revenue-retention-sources-2026.csv). **Control matrix:** [switching-cost-control-matrix-2026.csv](../data/switching-cost-control-matrix-2026.csv). **Migration testing:** [migration-runbook-2026.md](migration-runbook-2026.md). **Sensitivity:** [revenue-cohort-sensitivity-2026.csv](../data/revenue-cohort-sensitivity-2026.csv).

_This research is based only on publicly accessible information and artificial examples; it contains no expert-network invitation, former-employer trade secrets, or restricted signed client agreements._
