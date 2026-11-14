# AI-native DAF technology entrant: first-principles simulation

> **Red-team status (2026-11-14):** this document was independently reviewed in [red-team-wave2a-ai-and-entrant.md](red-team-wave2a-ai-and-entrant.md). The corrections in the final section govern where they conflict with the text.

**Date:** 2026-11-14 · **Status:** Analytical simulation. Regulatory items are drawn from primary sources. Capital, headcount and pricing figures are **SCENARIO assumptions**, labeled as such. No company facts are invented. This is not legal advice.
**Data:** `data/mission-2026-11-14/ai-native-component-buy-build-matrix.csv` (20 components) · `data/mission-2026-11-14/entry-strategy-comparison.csv` (3 strategies × dimensions)
**Builds on, does not repeat:** `startups-and-emerging-competitors-2026-11-12.md`, `challenger-economics-daffy-chariot-charityvest-2026-11-12.md`, `pave-finance-daf-market-entry-study-2026-11-11.md`, `expanded-daf-ecosystem-2026-11-11.md`, `daf-grant-exception-unit-economics-evidence-and-sensitivity-2026-11-12.md`, `ren-instant-grant-approval-rcf-policy-clarity-audit-2026-11-12.md`, `batch-2a-charity-vetting-grant-approval-2026-11-12.md`.

## 1. Executive summary
1. **What a DAF business legally needs is small. What it commercially needs is large.** The statutory core has six parts: a non-private-foundation charitable sponsor with exclusive legal control, a written acknowledgment for donors, controls against taxable distributions, prohibited-benefit and excess-benefit controls, excess-business-holdings monitoring, and Schedule D reporting [R1–R7]. The commercial core is custody, payment rails, sponsor trust and adviser distribution. All four are licensed, relationship-bound or already held by incumbents.
2. **The entrant should not build a sponsor, custody or payment rails.** Each is available to buy or partner. Endaoment publishes partner API tiers as sponsor of record [P1]. Chariot sells disbursement and eligibility checks to grantmakers [P2, P3]. Custodians, including Altruist, Schwab, Fidelity and BNY, are named as supporting Endaoment DAF accounts [P1].
3. **Recommended entry: Strategy 3, the AI-native operating layer.** It should be built so that two of its modules, continuous eligibility monitoring and cross-system reconciliation, can later be sold as Strategy 2 APIs. Strategy 3 has the lowest scenario capital (base about $5.0m to month 24, range $2.3–9.7m), the lowest regulatory dependency and the fastest falsifiable test. Strategy 1, a complete platform, needs roughly 3–4× the capital (base about $17m). It also has to displace systems of record that carry high switching costs.
4. **Main risk to the recommendation: the value pool for grant-review automation is thin.** The repo's hypothetical exception model puts the gross labor saving at a 48,744-grant sponsor (Charityvest's 2025 volume) at about **$16k/year**. At Fidelity Charitable's 3.0m grants it is about **$975k/year**. A product that only automates grant review is therefore not commercially meaningful for most sponsors. The layer has to absorb reconciliation, servicing, monitoring and audit evidence as well, or it fails.
5. **What AI changes structurally:** decisions become versioned policy-as-code, eligibility becomes a continuous monitor instead of a per-grant lookup, humans review exceptions only, and the audit trail is event-sourced. **What AI cannot remove:** the sponsor's legal discretion, donor and adviser trust, licensed custody and money movement, and access to distribution.

## 2. Method and evidence rules
- **Facts** carry a source ID and access date (2026-11-14 unless stated). Repo-inherited facts keep their original citation.
- **Inference** is marked *Inference*. **SCENARIO** marks assumptions chosen for modeling. Their ranges are sensitivity bands, not estimates of market reality.
- The entrant is hypothetical. It is assumed to be a for-profit technology company that is not a charity, does not take custody and is not a registered investment adviser, unless a strategy requires one.
- The design starts from the legal and operational minimum rather than from an incumbent's feature list. Every incumbent feature that is not required by law, by a counterparty (custodian, auditor, bank) or by a demonstrated buyer need is treated as optional.

## 3. Regulatory and operational minimum for a viable DAF business

### 3.1 Primary-source minimums (facts)
| # | Requirement | Primary source | Who bears it |
|---|---|---|---|
| R1 | A **sponsoring organization** is described in IRC §170(c) (excluding governmental units under §170(c)(1)), is **not a private foundation**, and maintains one or more DAFs. A **DAF** is separately identified by reference to donor contributions, is **owned and controlled by the sponsor**, and the donor or appointee has or expects advisory privileges over distributions or investments. | 26 U.S.C. §4966(d) — https://www.law.cornell.edu/uscode/text/26/4966 | Sponsor |
| R2 | **Taxable distributions**, meaning grants to natural persons or for non-§170(c)(2)(B) purposes without expenditure responsibility, carry a 20% tax on the sponsor. A fund manager who knowingly agrees owes 5%, capped at $10,000 per distribution. | §4966(a)–(c), same URL | Sponsor and its managers |
| R3 | **Prohibited benefits.** A person who advises a distribution conferring a "more than incidental benefit" on a donor, advisor or related person, or who receives that benefit, owes 125% of the benefit. A knowing fund manager owes 10%, capped at $10,000. | 26 U.S.C. §4967 — https://www.law.cornell.edu/uscode/text/26/4967 | Donor, advisor, recipient, managers |
| R4 | **Automatic excess benefit.** Any grant, loan, compensation or similar payment from a DAF to a donor, advisor, family member or 35%-controlled entity is an excess benefit transaction. The tax is 25%, rising to 200% if uncorrected, plus 10% on managers (capped at $20,000). | 26 U.S.C. §4958(c)(2), (f)(7) — https://www.law.cornell.edu/uscode/text/26/4958 | Disqualified persons, managers |
| R5 | **Excess business holdings** rules apply to DAFs as if they were private foundations. | 26 U.S.C. §4943(e) — https://www.law.cornell.edu/uscode/text/26/4943 | Sponsor |
| R6 | **Deductibility** requires a contemporaneous written acknowledgment that the sponsor has **exclusive legal control**. Veterans, fraternal and cemetery organizations and non-functionally-integrated Type III supporting organizations cannot be sponsors for deduction purposes. | 26 U.S.C. §170(f)(18) — https://www.law.cornell.edu/uscode/text/26/170 | Sponsor (donor loses deduction) |
| R7 | **Form 990 Schedule D Part I** requires the number of DAFs at year end, contributions, grants and year-end value (lines 1–4). Line 5 asks whether donors were told in writing that the assets are the organization's property under its exclusive legal control. Line 6 asks whether grantees, donors and advisors were told in writing that funds are for charitable purposes only and not for donor or private benefit. | Form 990 Sched. D (Rev. Dec 2024) — https://www.irs.gov/pub/irs-pdf/f990sd.pdf ; instructions https://www.irs.gov/instructions/i990sd | Sponsor |
| R8 | The **Pension Protection Act of 2006** (Pub. L. 109-280) enacted the DAF provisions above: §§4966, 4967, 4958(c)(2), 4943(e) and 170(f)(18). | https://www.congress.gov/bill/109th-congress/house-bill/4 | — |
| R9 | **Proposed §4966 regulations** (REG-142338-07, 88 FR 77922, Nov 14 2023) are **not final**. The Council on Foundations' May 2026 comment asked Treasury to prioritize finalizing them. Commentary on the 2026–2027 Priority Guidance Plan says §4966 guidance remains listed. | https://www.federalregister.gov/documents/2023/11/14/2023-24982/taxes-on-taxable-distributions-from-donor-advised-funds-under-section-4966 ; https://cof.org/sites/default/files/2026-05/2026%20IRS%20Priority%20Guidance%20Plan%20Comment.pdf ; https://www.wealthmanagement.com/philanthropy/treasury-and-irs-release-2026-2027-priority-guidance-plan | Rule risk for all |
| R10 | The IRS says it may disallow deductions, impose §4966/§4958 taxes, or revoke exemption for DAF arrangements that give improper benefits. | https://www.irs.gov/charities-non-profits/charitable-organizations/donor-advised-funds | Sponsor, donors |
| R11 | **State charitable solicitation:** commentary dated September 2026 says about 40 states plus DC require registration before solicitation. NASCO's Unified Registration Statement simplifies filing but does not replace state-specific rules. | https://www.wolterskluwer.com/en/expert-insights/charitable-solicitation-registration ; https://www.venable.com/insights/publications/2018/07/does-my-nonprofit-really-have-to-register-before-a | Sponsor; possibly vendor as solicitor or co-venturer (*Inference*) |
| R12 | **Money transmission:** FinCEN's money-transmitter definition has a payment-processor exemption. FinCEN rulings describe four conditions, including facilitating purchases of goods or services and settling only through BSA-regulated clearing systems. | 31 CFR 1010.100(ff)(5) — https://www.ecfr.gov/current/title-31/subtitle-B/chapter-X/part-1010/subpart-A/section-1010.100 ; FIN-2014-R012 https://www.fincen.gov/system/files/administrative_ruling/FIN-2014-R012.pdf | Any entity that takes possession of funds |
| R13 | **Investment of charitable pools:** the Philanthropy Protection Act of 1995 (Pub. L. 104-62) amended Investment Company Act §3(c)(10) to exempt certain charitable collective investment funds. It made companion amendments to the Securities Act, the Exchange Act and the Advisers Act. | https://www.govinfo.gov/content/pkg/PLAW-104publ62/html/PLAW-104publ62.htm | Sponsor and its pools |
| R14 | **Broker-dealer customer identification (CIP)** applies to the custodian opening the sponsor's account. | 31 CFR 1023.220 — https://www.ecfr.gov/current/title-31/subtitle-B/chapter-X/part-1023/subpart-B/section-1023.220 | Custodian |
| R15 | **OFAC:** sanctions apply to all U.S. persons, including nonprofits. Treasury publishes a risk-factor matrix for charities that disburse funds to grantees. | https://ofac.treasury.gov/media/15651/download ; https://ofac.treasury.gov/media/16331/download | Sponsor and vendor |

### 3.2 Inferences from the minimums
- *Inference:* **the entrant itself needs none of the charity-level statuses.** Every tax in R2–R5 falls on the sponsor, its managers, or donors and advisors. That makes the sponsor's *legal discretion* the binding constraint on how far a vendor can automate. A vendor can execute policy. The sponsor's managers carry personal excise-tax exposure (§4966(a)(2), §4967(a)(2)), so they will keep authority over any decision that is not routine.
- *Inference:* **the entrant can stay outside money transmission** if grant money never sits in an account the entrant controls. That is possible when the sponsor's bank originates payments, or when a disbursement partner with a bank relationship does (Chariot names Column N.A. as a key partner and FS Vector as compliance counsel [P3]). Charitable grants are not obviously "purchases of goods or services," so an entrant that holds funds should not assume the payment-processor exemption covers it. This needs counsel.
- *Inference:* **the entrant can stay outside RIA and broker-dealer registration** if it does not give investment advice for compensation or effect securities transactions. Charging basis points on invested DAF assets for portfolio management would change that.
- *Inference:* **the entrant may be pulled into state solicitation regimes** if it markets a sponsor's DAF and is paid per contribution. Fixed-fee software contracts, with the sponsor as the only solicitor, reduce that exposure. Counsel review is needed state by state.

### 3.3 Minimum operating capabilities (whoever provides them)
1. A sponsor entity with governance and exclusive legal control (R1, R6).
2. Contribution intake, acknowledgment and substantiation (R6).
3. Custody at a qualified bank or broker (R13, R14).
4. A per-fund sub-ledger reconciled to the custodian and bank (R7 lines 1–4 depend on it).
5. Grant controls covering recipient status, purpose, private and prohibited benefit, and related parties (R2–R4).
6. Holdings monitoring for donor-related businesses (R5).
7. Verified-payee disbursement with return handling (R12, R15).
8. Written notices to donors and grantees, with evidence they were sent (R7 lines 5–6).
9. Year-end reporting and audit support (R7).
10. Sanctions and identity screening (R14, R15).

Everything else is a choice made for competitive or distribution reasons, not a requirement for viability. That includes donor apps, giving baskets, advisor dashboards, DAFpay-style inbound initiation and gamified engagement.

## 4. Component decisions (summary of the matrix CSV)
| Component | Decision | Named candidates (fit status) | Why |
|---|---|---|---|
| Sponsoring charity functions | **Partner** | Endaoment (evidenced: sponsor of record with public Partner API tiers [P1]); GiveClear (evidenced: sponsor for TIFIN Give/SEI [P4]); Charityvest (evidenced: independent sponsor on Foundation Source software [P5]); NPT private label (evidenced [P6]); RCF (evidenced, but related-party fee share with Ren [F1]); AEF (evidenced as an independent sponsor administered by Ren, fit for a new vendor hypothetical); Fidelity Charitable CIAP (evidenced for adviser-managed investing only [P7], as a tech partner hypothetical); NCF (hypothetical) | A captive sponsor is slow to build and raises §4958 and independence questions. RCF paid Ren $19.23m in FY2024 under a 98% fundholder-fee formula, the in-repo example of related-party economics [F1]. |
| State registration | Partner (sponsor files) | — | Keep the vendor out of the solicitor role. |
| Custody | **Buy/integrate** | Altruist (evidenced as a supported custodian on Endaoment's page; self-clearing since March 2023 [P8]); Schwab, Fidelity, BNY (evidenced via Endaoment [P1]); Apex (hypothetical for sponsor accounts); BridgeFT (evidenced in Foundation Source multi-custody announcements [repo U03]) | Licensed and capital-heavy. Building it adds nothing. |
| Investment | Partner | Pave (hypothetical; no DAF sponsor integration found, see repo study); sponsor pools; CIAP; AEF adviser program | Advice for a fee triggers Advisers Act registration. Offer only liquidity forecasting for grants. |
| Complex assets | Partner | GivingIQ (hypothetical fit) | Low volume and high judgment. AI helps extract documents and monitor §4943(e). |
| Donor experience | Reuse the sponsor UI (S3) or build (S1) | Sponsor portals; Endaoment embedded API | An operating layer should not compete for the front end. |
| Advisor experience | Partner/integrate | TIFIN Give (evidenced advisor tooling, including "tax intelligence" [P9]); Charityvest advisor program (evidenced); Pave (hypothetical) | Distribution sits inside adviser platforms. |
| Charity eligibility | **Reuse + automate** | IRS EO BMF (evidenced; 1,984,891 records, posted 11/10/2026 [D1]); Candid Charity Check API (evidenced; BMF, Pub 78, GuideStar data; bulk 25 EINs per call [D2]); Chariot eligibility database (evidenced; OFAC is one of six sources [P3]) | The data is commodity. The differentiation is monitoring every active payee continuously. |
| Grant approval | **Automate routine grants as policy-as-code; sponsor keeps authority** | Sponsor policies (RCF March 2023 policy: Charity Check adequate for >98% of historical grants, officer review above $500k [repo]) | Routine grants are rule applications. Exceptions need judgment. |
| Payments | **Partner** | Chariot Disbursements (evidenced: grantmaker-paid fee, nonprofits not charged, check fallback [P2]); PayPal Grant Payments and Stripe (evidenced at Vanguard Charitable/NPT and Fidelity Charitable respectively [repo]) | Avoid holding funds (R12). |
| Inbound DAF initiation | **Eliminate from scope** | Chariot DAFpay (evidenced, 70+ platform partners claimed [P10]) | Not needed for viability. The incumbent has a network lead. |
| Accounting | Build the event-sourced ledger (S1) or automate reconciliation (S2/S3) | Incumbent ledgers | The system of record is the deepest lock-in. |
| Compliance (OFAC, KYC, related party, §4943) | Buy screening data; **automate** monitoring | KYC vendors (not evaluated, hypothetical) | Continuous rescreening. Graph-based related-party detection. |
| Reporting | **Automate** | — | Schedule D and audit evidence fall out of an event log. |
| CRM | Buy plus a servicing agent | Commodity CRMs (not evaluated) | Low differentiation. |

## 5. Three entry strategies, simulated

### 5.1 Shared SCENARIO assumptions
- Loaded cost per FTE: **$170k / $210k / $260k** (low/base/high). Not sourced.
- 24-month capital = 2 × (average headcount × loaded cost) + 2 × annual non-headcount cost. Non-headcount covers SOC 2, counsel, cloud, model inference, data licences and insurance.
- Revenue figures are list-price-style assumptions per customer. Wherever possible each is set against a public price anchor that is *a different product*, and that difference is stated.

### 5.2 Sourced comparables (facts; none are like-for-like)
| Company | Disclosed financing | Source (accessed 2026-11-14) | Comparability |
|---|---|---|---|
| Daffy (Aside Inc.) | $4.8m seed (2020); $17.1m Series A led by Ribbit (Feb 8 2022) | https://www.businesswire.com/news/home/20220208005152/en ; https://www.daffy.org/answers/how-much-did-daffy-raise-in-their-series-a-funding-round-and-who-backed-it | Operates a consumer sponsor plus technology, closest to S1 + sponsor |
| Chariot | $11m Series A led by Maveron (Aug 2024); SSIR reported about $4m seed (not verified from a primary source) | https://givechariot.com/resources/insights/chariot-announces-11-million-series-a-investment-round-led-by-maveron ; https://ssir.org/articles/entry/fast_philanthropy | Payments and eligibility infrastructure, closest to S2 |
| Givefront | $2m seed (Dec 2025) | https://techcrunch.com/2025/12/18/these-21-year-old-dropouts-raised-2m-to-build-givefront-a-fintech-for-nonprofits/ | Nonprofit finance, adjacent to S2 |
| Pave Finance | >$15m Series A at $100m pre-money (company-reported, Sept 14 2026) | https://www.pavefinance.com/newsletter/series-a | Wealth infrastructure, adjacent to S3's adviser integration |
| Ren / RCF | RCF paid Ren **$19.23m** in FY2024; 98% fee-share formula; 25,824 year-end DAFs | https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf ; `data/rcf-ren-audited-admin-payments-2020-2024.csv` | Ceiling example of full-outsourcing revenue from one sponsor relationship. Not Ren ARR. |
| Endaoment | Partner tiers: Growth setup $0–25k plus $2k–5k/month; Strategic setup $25k–100k plus $5k–15k/month | https://endaoment.org/institutions | Sponsor-as-API price points, the nearest public price for an institutional DAF integration |
| Chariot pricing | Core 1% per donation; Growth $4,740/yr; DAFpay 2.9% initiation; disbursement fee to grantmakers unpublished | https://www.givechariot.com/chariot-pricing ; https://docs.givechariot.com/guides/disbursements/faq | Per-transaction anchor for S2 |

### 5.3 Simulation results (SCENARIO; detail in CSV)
| Dimension | S1 Complete platform | S2 Modular APIs | S3 AI-native operating layer |
|---|---|---|---|
| Average FTE, first 24 months | 20 / 32 / 45 | 7 / 12 / 18 | 5 / 9 / 14 |
| **Capital to month 24** | **$8.8m / $17.0m / $29.4m** | **$3.2m / $6.6m / $12.4m** | **$2.3m / $5.0m / $9.7m** |
| Months to first paying customer | 18 / 24 / 30 | 6 / 9 / 12 | 4 / 6 / 9 |
| Revenue per customer (assumed) | $0.3m / $1.0m / $3.0m per sponsor | $0.50 / $1.50 / $3.00 per grant event | $36k / $120k / $240k per sponsor |
| Customers for $5m ARR | 17 / 5 / 2 sponsors | 10m / 3.3m / 1.7m grant events | 139 / 42 / 21 sponsors |
| Implementation effort per customer | Very high: data migration, custodial re-papering, donor re-login (NPT's 14–16 weeks is for its *own* platform [P6]) | Low–medium: API integration | Medium: read access to ledger and grants, policy encoding workshop |
| Regulatory dependencies | Sponsor partner, custodian, payments partner, SOC 2, state registration via sponsor | Money-transmission analysis if disbursing; low for eligibility and reconciliation | Low: vendor-risk review, SOC 2; sponsor keeps authority |
| Distribution barriers | Very high: incumbents own systems of record; banks buy sponsor+tech bundles (e.g., SEI Charitable Fund powered by TIFIN Give, sponsored by GiveClear [P4]) | High: Chariot and Candid already sell overlapping APIs | High: needs data access that incumbent vendors control; large sponsors run in-house platforms |
| Recurring revenue potential | Highest per customer; slowest to win | Usage-based; base case needs about Fidelity Charitable's annual grant volume (3.0m in CY2025 [D3]) | Moderate; must expand scope beyond review to justify price |
| Switching costs once won | High | Low–medium (network of verified payees can raise it) | Low at first; rises with the accumulated policy library and decision history |

*Interpretation (inference):* S1's base capital ($17.0m) sits in the range of Daffy's combined seed plus Series A ($21.9m) and above Chariot's Series A. That fits with S1 being a venture-scale bet that requires sponsor-side wins before it produces evidence. S2's base case requires grant-event volume of the order of the largest sponsor, which makes it a bet on winning incumbents or a network. S3 is the only strategy whose falsification test fits in one seed-sized round.

### 5.4 The constraint on S3's value pool
The repo's hypothetical exception-labor model (`daf-grant-exception-unit-economics-evidence-and-sensitivity-2026-11-12.md`) assumes 3% exceptions, 25 minutes per exception, $65/hour and 40% of time saved. Applied to sourced grant counts:
- Charityvest, 48,744 grants in 2025 [P5]: **≈$15.8k/yr** gross saving.
- Fidelity Charitable, 3.0m grants in CY2025 [D3]: **≈$975k/yr**.

*Inference:* at the base S3 price ($120k/yr), grant-review savings alone would justify the purchase only at the very largest sponsors, and those sponsors are the most likely to build in-house. **S3 must therefore be priced and scoped on the whole operating burden.** That means reconciliation breaks, donor and adviser status contacts, payee data maintenance, year-end evidence and rule-change management. None of these cost pools is publicly measured. That gap is the single most important unknown (see §9).

## 6. MVPs and falsifiable signals (6–12 months)
| Strategy | Smallest commercially meaningful product | Signal that validates | Signal that falsifies |
|---|---|---|---|
| S1 | One sponsor-of-record partner, such as a white-label sponsor or a mid-size community foundation, running a *new* adviser channel's funds entirely on the entrant's event-sourced ledger. Daily three-way reconciliation with the custodian and bank. Payments through a partner rail. | Signed sponsor agreement plus ≥500 live funds or ≥$50m assets. Zero unexplained reconciliation breaks older than T+1 for 90 days. Clean auditor walkthrough. | No sponsor will commit a system-of-record migration within 12 months, or the partner sponsor requires the entrant to bear sponsor-level liability. |
| S2 | Cross-sponsor **DAF grant reconciliation API** for nonprofits and grantmakers. It matches remittances from many sponsors and rails to CRM gift records. Eligibility monitoring follows as a second endpoint. | ≥3 paying customers renewing after 6 months. ≥95% auto-match on an audited sample with a measured error rate. | Chariot or CRM vendors bundle equivalent matching at no cost, or auto-match cannot beat the manual baseline. |
| S3 | **Policy-as-code grant pre-review + continuous payee eligibility monitor + exception workbench**, run in shadow mode and then live at two independent sponsors. Read access to the grant queue; decisions written back as recommendations. | On ≥10,000 shadow grants: zero false clears on a stratified sample audited by the sponsor; ≥98% agreement with human decisions on the routine tier; ≥30% fewer reviewer minutes per 1,000 grants; at least one sponsor converts to paid **and expands scope** to reconciliation or servicing. | Sponsor counsel will not allow model-assisted clearing at any tier. Or data access depends on an incumbent vendor that refuses it. Or measured exception rate × minutes yields savings below the price (see §5.4). |

All thresholds are proposed test criteria, not market data.

## 7. What AI-native design changes, and what it only speeds up

### 7.1 Structural changes
| Legacy pattern (as publicly described) | AI-native redesign | Why it is structural |
|---|---|---|
| Grant policy is a PDF interpreted by reviewers. Example: RCF's March 2023 risk-tiered policy [repo]. | **Policy-as-code.** Each sponsor rule is versioned, executable and testable against past grants. Model-assisted classification covers purpose, ticket or membership benefit, pledges and earmarks, and each output cites the rule it applied. | Policy changes become diffable and can be back-tested. When the §4966 rules are finalized (R9), the sponsor can re-run historical grants against them. |
| Eligibility looked up at grant time. Sponsors cite 2–10+ business days for new-charity diligence (Vanguard, Fidelity) [repo batch-2a]. | **Continuous eligibility monitoring** of every active payee against BMF refreshes, Pub 78, revocations and OFAC list updates [D1, D2, R15]. Grants to pre-cleared payees inherit a current status. | Diligence moves off the grant's critical path, so latency falls for repeat grants (DAFgiving360 reports 38% scheduled recurring in FY2025 [repo]). |
| Every grant enters a review queue. | **Exception-only human review.** Routine tiers clear automatically under rules the sponsor has signed off. Humans see only cases the rules mark as non-routine, each with an assembled evidence pack. | Human time goes to judgment. The approval record states which rule or person decided. |
| Mutable records reconciled at month end. | **Event-sourced ledger and audit trail.** Every recommendation, approval, liquidation, payment and return is an immutable event. Schedule D lines 1–4 and evidence for lines 5–6 are queries against it (R7). | Grant status becomes one state machine shared by donor, adviser, sponsor and nonprofit. The audit can be continuous. |
| Related-party checks rely on donor self-attestation. | **Graph-based related-party screening** that matches donors' disclosed affiliations, addresses and officers against payees (R3, R4). | Finds §4967 and §4958(c)(2) exposure before payment. Every flag still needs human confirmation. |

### 7.2 Speed-ups only
- Drafting donor and adviser communications and answering status questions.
- Extracting data from complex-asset documents.
- Reconciliation break triage, until the ledger itself is event-sourced.
- State registration calendars.
- Proposal generation for advisers.

These cut cost but do not change who is accountable. Incumbents are already marketing them. Ren markets "over half" of grants approved instantly [repo audit]. TIFIN Give markets "tax intelligence" [P9]. GivingTech markets AI support [repo U17].

### 7.3 What AI cannot remove
1. **Sponsor legal control and discretion** (R1, R6). An approval is the sponsor's act. Managers face personal excise taxes (R2, R3).
2. **Trust.** Donors give irrevocably to a charity. The sponsor's brand and governance carry that trust. Software does not.
3. **Custody and money movement.** These are licensed, need capital, and carry insolvency risk. Flipcause in the repo's exits dataset shows what happens when remittances are delayed (`data/technology-provider-exits-and-incidents-2026.csv`, X01).
4. **Distribution access.** Wealth platforms and custodians decide which DAF appears next to client accounts. The SEI/TIFIN Give/GiveClear bundle [P4] and Endaoment's custodian list [P1] show distribution is negotiated at the institution level.
5. **Edge-case legal judgment.** Foreign grantees (equivalency determination or expenditure responsibility), churches and government units, and allegation-versus-finding decisions.

## 8. Recommendation
**Enter with Strategy 3, an AI-native operating layer sold to independent and community-foundation sponsors.** Build it on an event-sourced core so that eligibility monitoring and reconciliation can become Strategy 2 APIs. Do not build a sponsor, custody or payment rails. Treat Strategy 1 as an option to exercise only through a sponsor-of-record partnership, after S3 has produced decision and reconciliation data no incumbent has.

**Why:**
- Lowest capital at risk before a decisive test (base about $5.0m versus $17.0m for S1).
- No dependency on licences.
- Lines up with the actual binding constraint, sponsor discretion: the product makes sponsor policy executable rather than trying to replace it.
- Produces measured exception rates, reviewer minutes and break rates that the market does not publish (see the repo's evidence-gap register). That data would also decide whether S1 or S2 is worth pursuing.

**Conditions under which this recommendation is wrong:**
1. **Data access is gated by incumbent vendors.** If independent sponsors' grant queues and ledgers sit inside Ren, Foundation Source or TIFIN Give systems with no contractual API rights, and those vendors refuse, S3 has nothing to run on. In that case partnering with an API-first sponsor such as Endaoment, an S1-lite route, is better.
2. **The operating-cost pool is small.** If measured exception rates are around 0.5% and reviewer minutes are low (the lower-left of the repo sensitivity grid: about $21.7k/yr per 1m grants), and reconciliation and servicing costs are similarly small, a $120k/yr product cannot be justified. The thesis then becomes a feature that incumbents absorb.
3. **Wealth-firm buyers want bundles.** If the buyers who matter are banks and RIAs that buy a sponsor plus technology plus brand (SEI's model [P4]), the winning entry is S1 through a white-label sponsor partner, and S3 never reaches the decision-maker.
4. **Final §4966 regulations favor system-of-record owners.** For example, rules that expand the DAF definition or fund-manager duties in ways that require the ledger owner to attest controls. A layer that does not own the record would then be marginal.
5. **Incumbents match the policy-as-code features within 12–18 months.** Ren's instant-approval positioning suggests the direction. If they do, S3's differentiation goes, unless the entrant has accumulated cross-sponsor eligibility and outcome data that incumbents lack.
6. **Sponsors' risk appetite prohibits model-assisted decisions** even with sign-off on deterministic routine tiers. That would reduce S3 to a speed-up product (§7.2).

## 9. Open questions and evidence gaps
1. Measured per-grant exception rate, reviewer minutes and appeal rate at any sponsor. None is publicly disclosed (repo gap register).
2. Contractual data rights of independent sponsors on incumbent platforms: who owns API access to the grant queue? (See the repo's Ren MSA portability audit.)
3. Chariot's disbursement fee level and its regulatory structure for holding funds. Not published [P2, P3].
4. Whether Fidelity Charitable, NCF or AEF would host a third-party operating layer at all. Hypothetical.
5. The cost to serve per account for reconciliation and servicing. Not derivable from Form 990 functional expenses (repo challenger-economics doc).
6. State-by-state treatment of a fixed-fee software vendor that also markets a sponsor's DAF.
7. Whether Candid Charity Check returns an explicit OFAC field. Third-party sources say yes; Candid's official reference was not confirmed [D2].

## 10. Source register (accessed 2026-11-14 unless dated)
**Statute and regulation:** R1–R15 as cited in §3.1:
- §4966 — https://www.law.cornell.edu/uscode/text/26/4966
- §4967 — https://www.law.cornell.edu/uscode/text/26/4967
- §4958 — https://www.law.cornell.edu/uscode/text/26/4958
- §4943 — https://www.law.cornell.edu/uscode/text/26/4943
- §170 — https://www.law.cornell.edu/uscode/text/26/170
- Form 990 Schedule D — https://www.irs.gov/pub/irs-pdf/f990sd.pdf
- Schedule D instructions — https://www.irs.gov/instructions/i990sd
- PPA 2006 — https://www.congress.gov/bill/109th-congress/house-bill/4
- Proposed §4966 regulations — https://www.federalregister.gov/documents/2023/11/14/2023-24982/taxes-on-taxable-distributions-from-donor-advised-funds-under-section-4966
- Council on Foundations 2026 comment — https://cof.org/sites/default/files/2026-05/2026%20IRS%20Priority%20Guidance%20Plan%20Comment.pdf
- 2026–2027 Priority Guidance Plan commentary — https://www.wealthmanagement.com/philanthropy/treasury-and-irs-release-2026-2027-priority-guidance-plan
- IRS DAF page — https://www.irs.gov/charities-non-profits/charitable-organizations/donor-advised-funds
- State solicitation registration — https://www.wolterskluwer.com/en/expert-insights/charitable-solicitation-registration ; https://www.venable.com/insights/publications/2018/07/does-my-nonprofit-really-have-to-register-before-a
- 31 CFR 1010.100 — https://www.ecfr.gov/current/title-31/subtitle-B/chapter-X/part-1010/subpart-A/section-1010.100
- FinCEN FIN-2014-R012 — https://www.fincen.gov/system/files/administrative_ruling/FIN-2014-R012.pdf
- Philanthropy Protection Act 1995 — https://www.govinfo.gov/content/pkg/PLAW-104publ62/html/PLAW-104publ62.htm
- 31 CFR 1023.220 — https://www.ecfr.gov/current/title-31/subtitle-B/chapter-X/part-1023/subpart-B/section-1023.220
- OFAC charity risk matrix — https://ofac.treasury.gov/media/15651/download
- OFAC compliance framework — https://ofac.treasury.gov/media/16331/download

**Data sources:**
- D1 IRS EO BMF — https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf
- D2 Candid Charity Check — https://developer.candid.org/docs/charity-check-1 ; https://developer.candid.org/reference/charity-check-bulk-api ; https://developer.candid.org/docs/faqs-charity-check
- D3 Fidelity Charitable 2026 Giving Report — https://www.fidelitycharitable.org/insights/2026-giving-report.html (via repo)

**Providers:**
- P1 Endaoment — https://endaoment.org/institutions
- P2 Chariot Disbursements — https://docs.givechariot.com/guides/disbursements/faq
- P3 Chariot compliance — https://help.givechariot.com/onboarding/trust-and-safety/compliance
- P4 SEI Charitable Fund / TIFIN Give / GiveClear — https://www.seic.com/about-sei/newsroom/sei-launches-sei-charitable-fund-bringing-charitable-giving-advisor-and-client-wealth-experience ; https://tifin.com/news/tifin-give-partners-with-sei-to-deliver-white-labeled-donor-advised-fund-solutions-to-bank-and-trust-clients/19590/ ; https://www.giveclear.org/reports-and-financials
- P5 Charityvest 2025 results — https://foundationsource.com/newsroom/press-releases/charityvest-reports-record-2025-charitable-giving-more-than-doubling-contributions-and-grants/
- P6 NPT institutions — https://www.nptrust.org/advisors-and-institutions/for-financial-institutions/
- P7 Fidelity Charitable CIAP — https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/ciap-overview.pdf
- P8 Altruist self-clearing — https://www.wealthmanagement.com/financial-technology/now-self-clearing-altruist-becomes-a-true-custodian
- P9 TIFIN Give tax intelligence — https://tifin.com/news/tifin-give-launches-first-of-its-kind-tax-intelligence-for-philanthropy/18820/
- P10 Chariot about and pricing — https://www.givechariot.com/about ; https://www.givechariot.com/chariot-pricing

**Financial:**
- F1 RCF FY2024 audit — https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf

**Financing:**
- Daffy — https://www.businesswire.com/news/home/20220208005152/en ; https://www.daffy.org/answers/how-much-did-daffy-raise-in-their-series-a-funding-round-and-who-backed-it
- Chariot — https://givechariot.com/resources/insights/chariot-announces-11-million-series-a-investment-round-led-by-maveron ; https://ssir.org/articles/entry/fast_philanthropy
- Givefront — https://techcrunch.com/2025/12/18/these-21-year-old-dropouts-raised-2m-to-build-givefront-a-fintech-for-nonprofits/
- Pave — https://www.pavefinance.com/newsletter/series-a ; https://www.pavefinance.com/capabilities

**Other:**
- Ren platform — https://www.reninc.com/giving-platform/
- RCF due diligence policy — https://renaissancecharitable.org/wp-content/uploads/2026/02/Grantmaking-Due-Diligence-Policy.pdf
- AEF advisors — https://www.aefonline.org/advisors/
- Charityvest advisor fees — https://advisorguide.charityvest.org/getting-started/how-client-fees-work
- GivingIQ — https://givingiq.com/press/announce
- Foundation Source DAFs — https://foundationsource.com/donor-advised-funds/
- Fidelity Charitable grant timeline — https://www.fidelitycharitable.org/faqs/all/grant-processing-timeline.html
- Vanguard Charitable grant status — https://www.vanguardcharitable.org/faq/how-do-i-check-status-my-grant

## 11. Data dictionary

### `data/mission-2026-11-14/ai-native-component-buy-build-matrix.csv`
| Column | Definition |
|---|---|
| component_id | C01–C20 identifier |
| component | One of: Sponsoring charity functions; Custody & investment; Donor experience; Advisor experience; Charity eligibility; Grant approval; Payments; Accounting; Compliance; Reporting; CRM |
| sub_function | Specific function within the component |
| minimum_viable_requirement | What must exist for a viable DAF operation (not incumbent feature parity) |
| regulatory_or_control_anchor | Statute, regulation, form line or control that creates the requirement |
| decision | buy / partner / reuse / build / automate / eliminate, or a stated combination by strategy |
| decision_rationale | Why that decision, including inference |
| candidate_providers | Named real providers where public evidence exists; "not evaluated" otherwise |
| partner_fit_evidence_status | Per provider: *evidenced* (public documentation shows the provider offers this role) or *hypothetical* (plausible, no public evidence of fit for a new entrant) |
| evidence_urls | Primary URLs, separated by " ; " |
| ai_native_effect | *changes* (structural redesign), *accelerates* (speed/cost only), or *none* |
| what_ai_cannot_remove | Residual legal, trust, licensing or distribution constraint |
| strategy_relevance | Which of S1/S2/S3 needs the component and how |
| confidence | high / medium / low confidence in the decision |

### `data/mission-2026-11-14/entry-strategy-comparison.csv`
| Column | Definition |
|---|---|
| strategy_id | S1 complete platform; S2 modular APIs; S3 AI-native operating layer |
| strategy | Strategy name |
| dimension | Metric or qualitative dimension compared |
| low / base / high | Sensitivity band values. For "customers needed" rows, *low* corresponds to the low-revenue case and so needs more customers. Blank for text rows. |
| unit | Unit of measure (USD, USD m, FTE, months, qualitative, text) |
| value_type | SCENARIO (assumption), INFERENCE (reasoned judgment), PROPOSAL (designed test), or a sourced anchor described in notes |
| basis_or_formula | Formula or reasoning that generates the value |
| anchor_source_url | Public source for any comparable used (blank when purely assumed) |
| notes | Comparability limits and caveats |

## Red-team corrections (wave 2A, 2026-11-14) — governing

10. **`ai-native-entrant-simulation.md`, Exec #3 and §8.** Replace "Recommended entry: Strategy 3" with:
    > "Preferred research probe: Strategy 3, conditional on measuring operating cost pools. On the repo's own parameters, $120k/yr requires ≈369k grants/yr from grant review alone, or ≈76k grants/yr if S3 captured all redesign and AI value in its scope; most independent and community-foundation sponsors are below both."

    Replace "lowest scenario capital" with:
    > "lowest assumed capital (by headcount assumption; S3 needs ~42 customers for $5m ARR vs 5 for S1)."
11. **Same doc, §6 S3 row and the CSV `falsifiable_signal_6_12m`.** Replace "zero false clears… model-assisted clearing" with:
    > "routine-tier clearing by deterministic, sponsor-approved rules only; AI may add flags or evidence but not clear (consistent with ai-governance-failure-modes.md §5)."
12. **Same doc, R9 and §8 condition 4.** Replace "Commentary… says §4966 guidance remains listed" with:
    > "The 2026–27 Priority Guidance Plan (2026-09-29) lists 'Guidance under sections 4966 and 6033 regarding certain donor advised fund arrangements', replacing the prior plan's final §4966 regulations item."

    Change condition 4 to "Forthcoming §4966/6033 guidance…".
13. **Same doc, §4 and §5.2.** Add the missing players:
    - Daffy for Developers (open APIs, 2023) as a second sponsor-of-record API.
    - Goodstack (nonprofit verification and eligibility API) as an S2 competitor.
    - Every.org APIs.
    - Bonterra Que, Benevity and Blackbaud as incumbents able to bundle S3 features.
    - Givinga, Stellar/iPhi, DAFtech and Give Interactive as DAF-tech vendors.
14. **Same doc, §9 Q7.** Answer it: the RCF policy states that Charity Check "Includes the result of GuideStar's OFAC verification".
15. **Same doc, Endaoment custodians.** Replace "are named as supporting Endaoment DAF accounts" with "are named on Endaoment's institutions page ('The DAF follows the assets…'); custodial agreements not verified".
16. **Same doc, §5.4.** Note that the $65/h rate and exception model differ from the economics doc's $55.45/h model, and reconcile them.
