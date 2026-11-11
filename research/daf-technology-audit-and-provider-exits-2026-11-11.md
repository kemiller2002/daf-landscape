# DAF Technology Audit and Provider Failure / Exit Study
**Evidence cut-off: November 11, 2026 | First-stage public-evidence assessment, not a penetration test**

## Executive assessment

A comprehensive donor-advised fund (DAF) market report needs a **technology, operational resilience and vendor-survival audit**. The existing research documented the roles of sponsors, technology providers, advisors and custodians, but has not independently examined the applications' source code, production ledger, service-level outcomes, present scoped SOC reports, data recovery practices, financial safeguarding, or migration performance.

This first-stage report adds:
- **12 active DAF/adjacent technology provider observations** with evidence maturity and unanswered test requirements.
- **24 testable control domains**: 13 P0, 9 P1, 2 P2.
- **11 dated company/product events** covering confirmed adjacent fundraising shutdowns, one insolvency, acquisitions, rebrands, planned sunset, major outage and a historic cyber-enforcement case.
- **34 qualified sources** including official product/API documentation, government regulators, first-party closure notices, and NIST/OWASP frameworks.
- **16 Clarity challenges** against unfounded assumptions about provider viability, data loss, company status, code quality, sponsorship and security.

**Do not describe these as completed technical certifications or scorecards:** no third-party vendor systems, protected portals, codebases, financial accounts, internal logs or scoped audit reports were accessed or tested. The study classifies public evidence and defines **verification gates**. Absence of public API documentation is not proof that a private enterprise API doesn't exist or that the code is poor; good public docs are not proof an implementation is safe.

**Most critical new finding:** The greatest technology risk is not a missing AI feature. It is a break between **(1) legal donor contribution, (2) sponsor/custodian financial ownership, (3) fee/ledger record, (4) legally approved grant, (5) payment settlement, (6) nonprofit receipt, and (7) historical record continuity**. Corporate insolvency, outage and migration can expose different parts of that chain. The sponsor's legal authority persists separately from a technology vendor's existence.

## 1. Audit model: assess actual jobs, not vendor adjectives

For every legal entity/product/SKU/environment/year, inspect:

| Pillar | Minimum evidence | Critical failure to prevent |
|---|---|---|
| **Funds and legal structure** | Sponsor legal EIN, segregated custodian/bank account, authorizations, company vs charity cash ownership | Vendor bankruptcy immobilizes or sweeps charitable money |
| **Accounting and settlement** | Balanced fund ledger and custodian reconciliation, return/reversal controls, independent nonprofit receipt | Double grant, unremitted gift, unrecorded return or false donor receipt |
| **Privacy and authorization** | Tenant, advisor and sponsor roles, object/property-level permission, donor anonymity, consent | Cross-donor access, unauthorized grant or donor exposure |
| **Technical interface** | Versioned API, idempotent command, retry/webhook semantics, rate limit, error response, replay | Duplication, lost integrations and inconsistent ledgers |
| **Security governance** | Current **scoped** SOC/independent testing and exceptions, incident procedure, disclosed subservice roles | Out-of-scope marketing assurance and hidden material breach scope |
| **Business continuity** | Tested restore, dependency map, recovered event queue, downtime state reconciliation | Records are irrecoverable after data deletion, acquisition or outage |
| **Supplier survival and exit** | Financial sustainability, legal protected funds, historical export in standard format, termination/escrow | Insolvency or product sunset strands sponsor and nonprofit |
| **Product correctness** | Held-out actual workflows; accepted assets, grant decisions, fees, appropriate tax lots | Software recommends or executes incorrect irreversible decisions |

Public benchmark frameworks: [NIST CSF 2.0](https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20) [TA31] and [OWASP API Security Top 10 (2023)](https://api-security.owasp.org/editions/2023/en/0x11-t10/) [TA32]. Both are **control design inputs**, not proof a vendor complies.

Full verification requirements and acceptance criteria: [24-control matrix](../data/technology-audit-control-matrix-2026.csv).

## 2. Active provider technology observations

### Ren

[Ren Giving Platform](https://www.reninc.com/giving-platform/) publicly markets donor/advisor and charity roles, account opening, contributions, grant recommendations, recurring grants, receipts and balances [TA10]. That establishes **offered workflows**, not their underlying service architecture. The main unanswered technical questions concern independent sponsor-controlled double-entry fund accounting, custodial reconciliation, failure correction and five-year export, role separation, signed enterprise API scope, and current assurance.

**Status:** product offered; no actual API/ledger/portability/security tests executed in this review. Its older public Type I/II security-report conflict remains documented in prior research; do not attribute current Type II report without reading actual report.

### Foundation Source + Vennfi/Charityvest

Official Sept. 23, 2025 announcement names [BridgeFT multi-custodian API](https://foundationsource.com/newsroom/press-releases/foundation-source-elevates-turnkey-daf-platform-with-advisor-branded-multi-custodial-flexibility/) [TA09]. The Oct. 17, 2024 acquisition of Vennfi [TA20] connected multiple product histories, while **Charityvest remains independent legal sponsor**. An announcement of support for major custodians is not an independently measured demonstration of *real-time accurate basis and lot data* at every custodian, reconciled corporate actions, or full system convergence after acquisitions. Require time-stamped feeds and complete legal-fund-to-custody ledger testing.

**Status:** credible named integration/acquisition, production performance and migrations not independently witnessed.

### TIFIN Give

Current product page markets advisor-centric white label, multi-custodial functionality and wealth growth [TA11]. The divestiture of **Giving Place** in April 2025 is separate from TIFIN Give continuing to offer a DAF platform [TA21]. Need independently tested 2026 holdings/lot opportunities, sponsor role authorization, 18 donor tax suitability cases, and service/contract data. No claim that a marketed engine is tax-accurate or deficient without running it.

### GivingTech DAFtech

[Institutional product page](https://givingtech.org/daf-institutions) advertises **technology-only licensing**, **full-service revenue share**, white label, approval systems, investment, portfolio reconciliation, Zapier/Make/API integration [TA12,TA13]. This is relevant enterprise competition. But **U.S. legal sponsor EIN / charity relationship, actual live institutional deployments, independent assurance and complete ledger correctness remain unverified**. A product website's "DAFtech is legal sponsor" phrase cannot substitute for a properly identified US charitable entity.

### Chariot

The [versioned Donor Accounts APIs](https://docs.givechariot.com/guides/dafpay/donor-accounts/overview) separate donor verification and sponsor grant request decisions [TA01]. [Webhook documentation](https://docs.givechariot.com/api/webhooks) states production deliveries may retry **up to 10 times over approximately five days**, uses at-least-once semantics requiring idempotent processing, and **does not retry failed sandbox webhooks** [TA02]. Its OAuth partner integration recommends **idempotent grant creation** and integer-cent amounts [TA03]. [Security page](https://help.givechariot.com/onboarding/trust-and-safety/security) claims SOC 2 Type II and security controls; no actual independent report scope read [TA04]. API docs include returned deposits and status/return events [TA30].

**Decision:** strongest *observable public API specificity* in this reviewed set, but **not a verified superior product, code architecture or security rating**. Run intentionally duplicated webhook, simultaneous sponsor decision, failed bank transfer, stale event and 5-day disabled endpoint scenarios.

### Daffy

[Public developer API](https://docs.daffy.org/) [TA06] exposes distinct donation/contribution resources [TA07,TA08], including private access constraints and created/received/completed timestamps. The fields enable useful causal event tracing but don't prove complete fund subledger/reconciliation, legal gift acceptance, sponsor grant approval or portable historical archives. Test permissions and export with authorized accounts; no private data accessed.

### NPT, Benevity, Bonterra, GoFundMe Pro, Blackbaud, DonorPerfect

- **NPT:** private-label sponsor model is documented in earlier research; underlying licensable software API, accounting architecture and migration details remain unknown.
- **Benevity:** Alaya **product**, not Benevity company, is scheduled for retirement on **Dec. 15, 2026**, with migration to Employee Engagement [TA19]. No claim the sunset has happened yet as of Nov. 11.
- **Bonterra:** CyberGrants-based corporate giving platform **continues** after corporate acquisition [TA22]. Acquisition is not proof of software failure or integration success.
- **GoFundMe Pro:** the Classy *brand* retired in 2025 while its software continues [TA23]. Not a defunct company.
- **Blackbaud:** historic 2020 donor data exfiltration and **2023 SEC** / **2024 FTC** enforcement document concrete security and disclosure failures [TA26,TA27]. Regulators' findings apply to that historic incident; do not claim all its current products are insecure.
- **DonorPerfect:** as of **Nov. 11, 2026**, its [status page](https://status.donorperfect.com/) [TA24] reported reporting/API/application interruptions amid an active cybersecurity investigation. Some donation collection channels remained available while related CRM synchronization was blocked. A downstream Fundraise Up incident also described donor record syncing delays [TA25]. **Root cause, exfiltration, ultimate recovery and amount of lost data were NOT established by this investigation.**

The [12-provider technology evidence matrix](../data/provider-technology-evidence-matrix-2026.csv) explicitly distinguishes *public technical specification*, *vendor feature assertion*, *independently observed functional result*, *current SOC report reviewed*, and *not verified*. Nearly all independent test fields are **not verified**, rather than scored zero or one.

## 3. Former companies, failed services, and non-failures

| Case | Verified status | Key consequence / limitation |
|---|---|---|
| **Flipcause** | CA Attorney General ordered operations cease **Nov. 14, 2025** for unremitted charitable funds and unregistered activity [TA14]; bankruptcy later converted to **Chapter 7 April 28, 2026** in independent legal reporting [TA15,TA34] | Critical warning on donation/payment segregation, regulator compliance, creditor recoveries. Legal company collapsed; Software4Nonprofits says it acquired the **technology**, branded **DONATION Pro** [TA16]. Program continuity ≠ creditors paid. |
| **Everfund** | Company posted closure notice for **Nov. 22, 2024** [TA17] | Donor data export and planned deletion are an exit risk. Not a core DAF sponsor. No customer-level data loss proven. |
| **Kambeo** | Self-posted service shutdown effective **March 30, 2026** [TA18] | Customers instructed to export donor information and disconnect Stripe. Company cites insufficient growth, **not proven poor code**. Not a core DAF sponsor. |
| **Benevity Alaya** | **Future product sunset Dec. 15, 2026** [TA19] | Migration to Benevity Employee Engagement; parent not closed; original 2025 notice reviewed as of Nov. 11. |
| **Vennfi** | **Acquired Oct. 17, 2024** [TA20] | For-profit technology changed owner, independent Charityvest sponsor retained charitable assets. Not failure. |
| **Giving Place** | **Sold Apr. 21, 2025** [TA21] | Family office/private-foundation product transferred; TIFIN Give's separate DAF software continues. |
| **CyberGrants** | **Acquired / integrated into Bonterra** [TA22] | Legacy CSR technology still marketed. Not closed. |
| **Classy** | **Rebranded GoFundMe Pro Jul. 2025** [TA23] | Name retired, platform continued. |
| **DonorPerfect** | **Security-related major service incident Nov. 11, 2026** [TA24,TA25] | Service boundary, queue/replay/backfill and disclosure tests. Not closed. |
| **Blackbaud** | **Historical regulatory security case**, 2020 event / 2023/24 enforcement [TA26,TA27] | Incident management and accuracy of disclosure materially affect trust; company remains operational. |
| **JustGiving 3scale dependency** | Planned third-party API management EOL **June 30, 2027** [TA28] | Migration to Blackbaud SKY API required, not JustGiving shutdown. |

### Flipcause: follow the money, not only the website

The [California AG announcement](https://oag.ca.gov/news/press-releases/attorney-general-bonta-warns-fundraising-platform-flipcause-immediately-stop-its) [TA14] alleged delayed transfers of about **$500k donations at that enforcement point in November 2025**. Separate 2026 bankruptcy reports described approximately **$29–30 million creditor exposures**, much of it associated with nonprofits [TA15,TA34]. **These are different dates and financial definitions** and cannot be added or treated as identical confirmed final losses.

A technology successor says customer campaign software and records became available under a new product [TA16]. That does not establish a corresponding resolution of bankruptcy claims or safeguarded charitable payments. **Lesson:** payment intermediary funds, charitable sponsor-owned assets, vendor service contracts, IP, source code, and donor records must each be located with their actual legal owner and failure waterfall. Even a migrated application cannot recreate untransferred charitable cash.

**EDF diagnostic boundary:** Flipcause has an observable adverse outcome (delayed charity remittances and later bankruptcy). Possible origin networks include cash/liability management, payment service design, governance, vendor capital constraints and legal compliance. **Technical root cause not established**; do not attribute failure to a specific tech stack or source code. EDF here should investigate observable money movement and control points before theorizing code defects.

### Everfund/Kambeo: survivability is not solely uptime

Both companies' first-party notices discuss donor record retrieval or exports and deletion on closure [TA17,TA18]. This makes **historical data portability and independent customer backups** a first-class procurement test. Their notices do **not** establish how many customers lost data or that the systems' code caused closure.

### DonorPerfect: service availability is multi-dimensional

During the Nov. 2026 incident, the official status log separated **donation collection that could continue** from **CRM ledger integration, reporting and API synchronization that could not** [TA24,TA25]. The correct test is whether every captured donation eventually generates the right legal/financial record exactly once. A live intake page without reliable backfill is incomplete operations, even though donor payment intake remains available.

### Blackbaud: security disclosure is part of the control system

The [SEC 2023 settlement](https://www.sec.gov/newsroom/press-releases/2023-48) describes misleading disclosures after a 2020 intrusion, including failures to escalate material facts internally [TA26]. The [FTC's finalized 2024 order](https://www.ftc.gov/news-events/news/press-releases/2024/05/ftc-finalizes-order-blackbaud-related-allegations-firms-security-failures-led-data-breach) concerns security practices and retention [TA27]. The requirements are **accurate cross-functional incident communication, minimization of sensitive data, access control, and tested disclosure pathways**, not merely a "SOC 2" marketing badge.

## 4. Five highest-priority executable supplier failure tests

**Test V1: Vendor insolvency / sponsor continuity.**
- Hypothetical tech vendor unavailable at 9 AM, live DAF sponsor retained independent charitable assets.
- Can authorized sponsor staff retrieve accounts, current balances, customer rights, grant approval history and bank signatures **without vendor access**?
- Required result: reconcile starting and ending sponsor assets, existing grants and onward charity distributions; record actual RTO/RPO with signed review.

**Test V2: Duplicate grant request and failed ACH.**
- Duplicate webhooks, out-of-order approval, retries over five days, failed/returned deposit, beneficiary account change.
- Required result: one and only one approved fund posting/settlement, confirmed external nonprofit receipt, correct corrected donor/grantee statements; no fabricated tax receipt.

**Test V3: Post-acquisition full migration.**
- Five years of donor contributions, investments, grant recommendations, sponsor decisions, supporting documents, tax receipts, anonymity restrictions.
- Required result: sponsor-owned export imported by independent receiving system, balances/transaction counts/roles 100% reconciled. If complete retention is legally restricted, document explicit authorized exceptions rather than losing data silently.

**Test V4: Upstream data outage / reconciliation.**
- Multi-custody pricing and basis stale, cybersecurity-driven API isolation, successful donation landing in pending sync.
- Required result: timestamped stale warnings; frozen sensitive calculations; deterministic replay, independent de-duplication and the ability to account for pending settlements.

**Test V5: SOC scope and breach escalation.**
- Request actual DAF system SOC report, exception/CUECs, vendor due diligence, incident notification timetable, donor PII retention/deletion and practice escalation.
- Required result: verify current audited scope and sponsor/third-party responsibilities; paper assertion alone does not pass.

**ALL FIVE: PROPOSED, NOT EXECUTED.** No production or private test was run.

## 5. Clarity implications and restraint

[16 Clarity challenges](../data/technology-audit-clarity-challenges-2026.csv) interrogate common failures of reasoning:

1. **Adjacent bankrupt fintech ≠ any DAF sponsor holds assets unsafely.** But it changes what evidence purchasers should demand.
2. **A company shutdown ≠ poor engineering.** Kambeo cites lack of growth; cause beyond that not independently established.
3. **Acquisition ≠ failure:** Vennfi, Giving Place, CyberGrants and Classy have different successor relationships.
4. **Scheduled product sunset ≠ past event:** Alaya is still a future December 2026 transition at this report's cutoff.
5. **Outage ≠ breach or irreversible data loss:** DonorPerfect's final cybersecurity impact is undetermined.
6. **Public API docs ≠ actual system quality:** Chariot and Daffy expose more useful documentation; no comparative security superiority is established.
7. **Company revenue scale ≠ donor-fund security or vendor survival:** test segregated financial assets, recognized revenue, bank payments and supportable customer obligations separately.
8. **Anonymity ≠ missing donor CRM bug:** where a DAF donor deliberately elects anonymity, correct behavior is non-disclosure.

Clarity asks whether the statement is a **verified observation, possible mechanism, source-limited inference, business recommendation or unsupported generalization**. EDF can explore an actually observed failure, but must not invent causes and then score vendors based on them.

## 6. What is still missing before this becomes a true technology audit

- **Direct DAF platform mortality census:** The confirmed examples above are largely adjacent fundraising platforms. We have **not** verified an historical series of failed *core DAF administration* companies. This is an important unknown, not proof no such failures occurred.
- A public-source census should track *legal sponsoring charities (EIN)* separately from the corporate *technology vendor* (legal business entity) and product names. Start from revised DAFRC historical sponsor EINS and IRS 990 Schedule D, compare multi-year filing status, formal dissolution/merger notices, official product deprecations, and verified successor agreements. **Missing IRS filings alone do not prove insolvency**.
- Verify historical **fund disposition**, sponsor/grant transfers, bank account authority and donor migration obligations after each confirmed closure. Company went out of business, legal sponsor revoked or changed, product sunset and charitable fund moved are four separate events.
- Live system tests for all critical DAF operations, security reports, performance, failure replay, export/restore and right-to-audit provisions.
- Provider unit economics and procurement: downtime/continuity liability, donor and sponsor data exit rights, custody/processor obligations, business financial viability and M&A consent.
- A comparison of **actual total cost of operation** across a modular provider stack and a vertically integrated technology/administration platform. Public software features alone cannot answer this.

## 7. Decision and research priority

**Immediately useful:** Add platform viability, charitable-asset separation and verified exit/migration to the existing Clarity+EDF DAF report as **non-negotiable diligence controls**, before spending effort on proprietary language or UI feature rankings.

**First providers for deeper authorized checks:** Ren, Foundation Source/Charityvest, TIFIN Give, GivingTech DAFtech, Chariot and Daffy, while using Flipcause, Everfund, Kambeo, DonorPerfect and Blackbaud as failure-mode reference cases. National sponsor NPT and corporate giving Benevity/Bonterra belong in different legal/operating comparison groups, not on a single universal ranking.

**Suggested added comprehensive chapters:** "DAF Technology and Operational Audit" and "Provider Mortality, Mergers and Data Continuity". The former concerns execution correctness; the latter concerns the survival and ownership of donor funds, software contracts, records and operational authority.

### Source index and validation status

- [30 plus 4 standards/legal/regulatory sources](../data/technology-audit-source-register-2026.csv): **34 entries**, dated, with explicit caveats
- [12 provider initial evidence assessments](../data/provider-technology-evidence-matrix-2026.csv): no production tests
- [24 technology controls](../data/technology-audit-control-matrix-2026.csv): 13 P0, 9 P1, 2 P2
- [11 company-product exit/incident cases](../data/technology-provider-exits-and-incidents-2026.csv): event types kept separate
- [16 Clarity challenges](../data/technology-audit-clarity-challenges-2026.csv): limits, counterclaims and falsification requests

Nothing in this file establishes that any named current DAF provider has a particular undisclosed source-code weakness, poor solvency, deficient donor funds controls, incomplete tax compliance, a specific system architecture, or a risk ranking. That requires independently verifiable, scoped, authorized evidence.
