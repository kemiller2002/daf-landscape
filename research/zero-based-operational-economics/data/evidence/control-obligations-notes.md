# Minimum human control obligations: evidence notes

Last reviewed: 2026-11-27. Register: [`../registers/control-obligations.csv`](../registers/control-obligations.csv), rows CO-001 to CO-063.

This is research, not legal, tax, audit or banking advice. Where a row or finding says "needs professional confirmation", nobody has been engaged and no opinion has been obtained. Mandate classes and evidence classes follow [`../CONVENTIONS.md`](../CONVENTIONS.md). All effort figures in the register are `ASSUMPTION`-grade estimates for one sponsor with about 2,000 funds and 2,000 grants a year. The register's `evidence_class` describes whether the obligation exists, not the effort figure.

## Method

1. **Repository first.** I read these before going to the web:
   - `docs/financial-core-control-spec-v0.5.md`, invariant 9: AI agents have no independent financial authority.
   - `docs/automated-charity-assurance-180-day-decision-record-v0.1.md`: the 180-day cycle is policy, not a legal safe harbor.
   - `docs/sponsor-white-label-grant-policy-affirmations-v0.1.md`, items WL-09/10 and D7/D8.
   - `data/sponsor-governance-controls-2026.csv`: O10, two Ren employees sit on the RCF board.
   - `data/technology-audit-control-matrix-2026.csv`: C01, C02, C04, C09, C11.
   - `data/ren-public-contract-clauses-2026.csv`: Ren's public MSA template.
   - `research/competitive-displacement/data/registers/adversarial-challenges.csv`:
     - CHL-037: a platform that creates ACH files is a TPSP.
     - CHL-038: Nacha's 2026 fraud monitoring is mandatory.
     - CHL-066: SOC 1, crime cover and bank due diligence for a licensor.
   - `research/commercial-opportunity/servicing-economics/03-organization-and-budget.md`: fractional roles and the CST-C08 regulatory opinion.
   - Unbound requirements: `governance/SPONSOR-AUTHORITY-AND-AUTONOMOUS-OPERATIONS.md` (GOV-AUTH-001..026, CNV-GOV-001..011) and the CNV-GRT, CNV-PAY, CNV-FIN, CNV-LEG and CNV-PLT clauses.
2. **Primary sources on the web.** I read statute and regulation text on Cornell LII, plus OFAC, Nacha, AICPA and IRS pages. Two items were read only through search summaries and are flagged:
   - the Massachusetts 201 CMR 17 page returned HTTP 403;
   - COSO's text was read through the AAA compendium, which is a secondary source.
3. **Classification.** Each obligation is classed by what actually compels it:
   - statute or regulation → `LEGAL-MANDATE`;
   - agency guidance → `REGULATORY-GUIDANCE`;
   - Nacha Rules, bank or MSA terms → `CONTRACTUAL`;
   - auditing standards or COSO → `AUDITOR-EXPECTATION`;
   - Unbound requirements → `ECHELON-POLICY`.

Mandate-class counts in the register: LEGAL-MANDATE 24, CONTRACTUAL 11, AUDITOR-EXPECTATION 7, ECHELON-POLICY 7, UNCERTAIN 6, RISK-BASED 4, REGULATORY-GUIDANCE 3, INDUSTRY-PRACTICE 1.

## (1) Which decisions are reserved to the sponsor, which can be delegated, and which can be automated

**What the law reserves to the sponsor (LEGAL-MANDATE)**

- **The sponsor must own and control the fund.** A DAF is a fund "owned and controlled by a sponsoring organization" (IRC 4966(d)(2)(A)(ii)). For a contribution to be deductible, the sponsor must give a contemporaneous written acknowledgment that it "has exclusive legal control over the assets contributed" (170(f)(18)(B)). Donors and advisors hold only "advisory privileges".
  - So final authority over grants, the ownership of assets and the investment mandate must sit with the sponsor (CO-001, CO-003).
  - An administrator, software provider or AI agent cannot hold that authority.
- **The taxes fall on the sponsor and on named individuals.** The 20% tax on taxable distributions falls on the sponsor. Personal taxes fall on "fund managers" who knowingly agree: 5% under 4966 and 10% under 4967. Fund managers are the sponsor's officers, directors and trustees, or persons with similar powers, plus employees with authority over the act (4966(d)(3)).
  - The sponsor therefore needs a named, accountable roster of people (CO-008).
  - This is why Unbound's CNV-GOV-004 rule, that Unbound vendor staff never hold A3+ authority, is sound.
- **Sponsor-only acts:**
  - filing the Form 990 and Schedule D Part I DAF data (6033(k), CO-012);
  - holding blocked property and remaining responsible for OFAC reports, even when an agent files them (31 CFR 501.603(a)(1), CO-019);
  - escheat as holder (CO-036);
  - state registration and audits (CO-038, CO-053);
  - adopting the investment policy and appointing the RIA (CO-055).

**What can be delegated to an administrator under the sponsor's authority**

The administrator can do the following, but legal responsibility does not move with the work:
- preparing acknowledgments, grant dossiers, payment files and return data;
- running sanctions screening;
- monitoring charity status;
- running reconciliation matching;
- preparing the OFAC report data.

The Ren MSA template (subcontracting, return of materials) and Unbound CNV-PAY-001 (sponsor is the Originator, Unbound is a TPSP) follow this pattern.

**What software can do under sponsor-approved policy**

These are deterministic checks with a human handling exceptions:
- the eligibility check for 170(b)(1)(A) public charities (CO-005);
- the related-party payee block for 4958(c)(2) automatic excess benefit (CO-010);
- generating acknowledgments from an approved template (CO-002);
- list screening and delta re-screening (CO-017);
- retention (CO-015, CO-020);
- NOC and return matching (CO-031);
- continuous reconciliation matching (CO-040).

**Uncertain: can a policy approve a grant with no human looking at it? (CO-004)**

No statute, regulation or guidance I found requires a human to sign off each grant, and none expressly allows approval by an automated policy. Unbound's CNV-GRT-001 and CNV-GOV-008 take a conservative middle line:
- the board adopts a version-pinned policy;
- the board names a delegate and an exception reviewer;
- the board receives quarterly reports with sampled human review.

Counsel must confirm this. The 2023 proposed regulations remain **proposed, not final**. The Council on Foundations page, updated 2026-05-08, says they have not been finalized, and I found no later evidence (CO-014).

## (2) Does any rule require two humans to authorize a payment?

**No legal mandate found.**
- No IRC section, OFAC regulation or Nacha rule that I read requires two-person authorization.
- Nacha requires each non-consumer Originator, TPSP and TPS to have risk-based fraud monitoring, reviewed at least annually. Phase 2 took effect 2026-06-19, with 2026-06-22 as the practical date. Nacha says this does not require screening each entry before processing (CO-029).

Dual authorization comes from three other places (CO-033):
- **AUDITOR-EXPECTATION and INDUSTRY-PRACTICE.** COSO Principle 10 expects incompatible duties to be separated, or documented alternative controls where separation is impractical.
- **CONTRACTUAL where a bank requires it.** UCC 4A-202 allocates wire-fraud loss using "commercially reasonable" security procedures. A customer who refuses a procedure the bank offered, and agrees in writing to be bound, bears the risk. Deposit agreements can similarly push check-fraud losses onto customers who decline positive pay (Cincinnati Ins. v. Wachovia, CO-034).
- **ECHELON-POLICY.** Unbound CNV-GOV-003 requires three distinct people until the auditor and the board have accepted the deterministic release gate.

Practical reading: dual control is effectively required by auditors and banks, but it is not law. That means its form can be designed. For example, the second party can be a sponsor officer releasing through the bank portal.

## (3) How independent must reconciliation be, and who can do it?

- **Legal basis: none found.** The obligation is AUDITOR-EXPECTATION, from COSO and the user auditor's evaluation under AU-C 402. Unbound mandates it as ECHELON-POLICY:
  - GOV-AUTH-014: the agent that initiates a transaction cannot attest its settlement;
  - CNV-GOV-003: reconciliation sits outside the payment chain, internal or outsourced, with at least monthly independent review;
  - CNV-FIN-004: continuous matching, controller sign-off monthly.
- **Independence is functional, not organizational.** The reconciler must not hold rights to initiate, approve or release payments, or to post unreconciled adjustments. Any of these can satisfy that:
  - sponsor finance staff;
  - an outsourced bookkeeper or CPA engaged by the sponsor;
  - a shared Echelon accountant who has no payment rights.
- **Separation the sponsor's external auditor needs.** The auditor (CO-038) must stay independent and should not run the reconciliation itself. AICPA non-attest-service rules were not re-read in this pass and need professional confirmation.
- **Best fit for a founder-led TPA:**
  - automated daily matching (Unbound);
  - exceptions resolved by a person outside the release chain;
  - monthly sign-off by the sponsor's controller or a fractional controller engaged by the sponsor (CO-041).

## (4) Minimum named roles for a TPA, and whether they can be fractional

No statute names roles for a DAF administrator. The roles that sources expect are listed below.

| Role | Basis | Fractional or shared? |
|---|---|---|
| Sanctions compliance officer | OFAC Framework (guidance): "appointed a dedicated OFAC sanctions compliance officer". Its footnote says this "may be the same person serving in other senior compliance positions" | Yes. Shared with Nacha and privacy compliance is acceptable under the guidance |
| Compliance owner for Nacha TPSP duties (annual Rules Compliance Audit, fraud-monitoring review, TPS risk assessment if TPS) | Nacha Operating Rules (contractual) | Yes. The audit itself can be external |
| Security program owner | 201 CMR 17 requires designated employee(s) (from prior knowledge; page returned 403). NY SHIELD scales safeguards for small businesses. SOC 2 CC1. Unbound CNV-GOV-003 gives the CISO a line to the audit committee | Yes. A vCISO is acceptable; the 03 budget already assumes one |
| Controller / financial-close owner, if Unbound prepares ledgers | AUDITOR-EXPECTATION (SOC 1 control owner) | Yes, but not the same person as the payment preparer |
| Payment-file preparer and release coordinator | CONTRACTUAL / AUDITOR-EXPECTATION | Must be distinct from the releaser and the reconciler |
| Change approvers for control-relevant code (two, neither the author) | ECHELON-POLICY CNV-PLT-010; ITGC expectation for SOC 1 | Needs at least 3 qualified engineers, or an external reviewer |
| Incident lead and breach-notice decision | State breach laws (LEGAL-MANDATE); counsel decides | Fractional with a breach-counsel retainer |
| Contract and assurance owner (SOC 1/SOC 2 coordination, bridge letters) | CONTRACTUAL / AUDITOR-EXPECTATION | Fractional |

Rule of thumb: one person can hold several *compliance-owner* roles. No one person may hold two *incompatible duties* on the same transaction:
- prepare and release;
- release and reconcile;
- author and approve a change.

## (5) Limits of each staffing arrangement

- **Sponsor personnel.**
  - Strongest independence from Echelon. These are the only people who can legally hold the sponsor's reserved authority and perform CUECs (CO-045).
  - Limits: availability, especially at December peaks; Unbound requires one sponsor per person for reserved authority (SPD-ADV-001); training; the sponsor's appetite.
  - Small sponsors may have no finance staff, which pushes the work to a fractional controller engaged by the sponsor.
- **Shared or fractional Echelon personnel.**
  - Acceptable for compliance-owner, security-owner, contract, engineering-approver and exception-handling roles. They are not independent of Echelon.
  - They cannot hold sponsor A3+ authority (CNV-GOV-004). They cannot be both preparer and releaser.
  - They should not sit on a sponsor board without disinterested-director procedures (see O10 for RCF/Ren; CO-011).
  - Shared time must be allocated by an explicit key (servicing-economics 03, item 4).
- **External professionals.** Mandatory for:
  - the state-required financial audit (CO-038);
  - the SOC 1 and SOC 2 service auditor (CO-043, CO-044);
  - legal opinions on money transmission, investment advice and fund-manager status (CO-025, CO-056, CO-008).

  Recommended for:
  - the Nacha Rules Compliance Audit (CO-027);
  - independent OFAC program testing (CO-022);
  - expenditure-responsibility grants (CO-007).

  Limits: cost, lead time, and the rule that an auditor cannot also operate the controls it audits.
- **AI agents.**
  - Useful for evidence gathering, dossiers, ranking matches, drafting reports and running deterministic checks.
  - They are not a human control, not independent (same organization, often the same model family), and not legal advice or external audit.
  - Unbound already rules out agent self-approval, self-attestation and binding legal interpretation (GOV-AUTH-003/011/014, CNV-AIO-001; CO-062).
  - Any control that a human must perform for independence or under OFAC, auditing or Nacha expectations stays with a named human. The agent prepares the evidence; the human decides.

## Minimum independent control coverage: one TPA, one sponsor

The goal is the smallest set of human seats that satisfies law, contracts and likely auditor expectations without dedicated full-time Unbound staff for each control. Hours are `ASSUMPTION` (register `recurring_effort_estimate`).

| # | Control seat | Must be independent of | Minimum satisfier | Fractional ok | Indicative hours/yr | Register |
|---|---|---|---|---|---|---|
| 1 | Grant authority delegate and exception reviewer | Unbound (vendor) | Sponsor officer or contracted officer appointed by board resolution | Yes | 40 + 6 board | CO-003, CO-004, CO-008, CO-057, CO-058 |
| 2 | Payment releaser (second person, or the bank-portal approver) | Payment-file preparer | Sponsor treasury officer | Yes | 50 | CO-032, CO-033 |
| 3 | Payment-file preparer and exception coordinator | Releaser and reconciler | Shared Echelon operations, or automation plus sponsor | Yes | in ops load | CO-033, CO-034, CO-035 |
| 4 | Reconciliation exception reviewer | Initiation and release | Sponsor finance, outsourced bookkeeper/CPA, or Echelon accountant without payment rights | Yes | 100 | CO-040 |
| 5 | Monthly reconciliation and close sign-off (controller) | Payment chain | Sponsor controller or fractional controller engaged by sponsor | Yes | 24 | CO-041 |
| 6 | Sanctions compliance officer (match disposition, 10-business-day reports, program) | none required; testing is separate | Sponsor compliance officer (sponsor-side duty); Echelon compliance owner for Unbound's own program | Yes (OFAC footnote) | 12 + 24 + 2 | CO-018, CO-019, CO-021 |
| 7 | Independent sanctions-program testing | Screening designers and operators | External consultant or sponsor internal audit | Yes | 16 | CO-022 |
| 8 | Nacha TPSP compliance owner and annual fraud-monitoring review | n/a | Echelon compliance owner (TPSP side); sponsor treasury (Originator side) | Yes | 12 + 12 | CO-026, CO-029 |
| 9 | Nacha Rules Compliance Audit | ACH operations | External payments auditor (recommended) | n/a | 40 prep + fee | CO-027 |
| 10 | Security program owner and incident lead | Engineering change authors (for its review role) | vCISO (fractional) | Yes | 100 | CO-050, CO-051, CO-052 |
| 11 | Change approvers for control-relevant code | Author | 2 engineers other than the author, or an external reviewer | Shared | 60 | CO-047 |
| 12 | Access reviewer | Access administrator | Sponsor (its users); Echelon manager (staff) | Yes | 16 | CO-048 |
| 13 | CUEC performer | Service organization | Sponsor personnel | Yes | 24 | CO-045 |
| 14 | Financial statement auditor | Sponsor and Echelon | External CPA firm | n/a | fee | CO-038 |
| 15 | SOC 1 and SOC 2 Type 2 service auditor | Echelon | External CPA firm | n/a | 200 prep + fee | CO-043, CO-044 |
| 16 | Form 990 / Schedule D preparer and officer signer | n/a | Outsourced CPA prepares; sponsor officer signs | Yes | 24 | CO-012 |
| 17 | Counsel: perimeter (money transmission, investment advice), 4966 delegation, fund-manager status, state registrations | n/a | External counsel (initially one-time) | n/a | 60 one-time | CO-004, CO-008, CO-025, CO-054, CO-056 |

What the table implies:
- With sponsor personnel in seats 1, 2, 5 and 13, the Unbound/Echelon side needs **no dedicated full-time control staff**. It needs fractional owners for compliance (seats 6, 8), security (10) and controllership if Unbound keeps books, plus engineers with enough headcount for seat 11.
- If the sponsor cannot staff seats 2 and 5, the Unbound-side minimum becomes **two Echelon people who are not in each other's chain, plus an external fractional controller**. Under CNV-GOV-003, Unbound also falls back to the three-person rule.
- Unbound itself now has four bounded human touchpoints (CO-004, CO-018, CO-033, CO-041) that no amount of automation removes. All four are performed by humans outside Unbound's own staff.

## Open matters needing professional confirmation (none commissioned)

1. **Board-delegated automated grant approval.** Does it satisfy the sponsor's "control" for 4966 and 170(f)(18)? Who are the 4966(d)(3) fund managers when approval runs through policy (CO-004, CO-008)? Tax counsel.
2. **Contracted officers.** Is a contracted, non-employee officer appointed by the board a "fund manager", and what D&O or indemnification is needed (CO-008, CNV-GOV-004)? Counsel.
3. **Nacha roles.** Confirm TPSP vs TPS status for the chosen architecture; whether the Rules Compliance Audit must be external; and the current audit deadline (CO-026, CO-027, OQ-009). ODFI and payments counsel.
4. **Money transmission perimeter.** Federal MSB status and state licensing for every funds-flow variant (CO-025; CST-C08 launch gate). Regulatory counsel.
5. **Investment perimeter.** Whether relaying donor allocation choices among sponsor-approved options, and reporting factual information, keeps Unbound outside RIA and broker-dealer registration. Relevance of the Philanthropy Protection Act / 3(c)(10)(B) (CO-056). Securities counsel.
6. **GLBA/FTC Safeguards for Echelon.** Is a for-profit DAF administrator a "financial institution" or a covered service provider (CO-049)? Privacy counsel.
7. **Massachusetts 201 CMR 17.** Confirm the "designate one or more employees" and service-provider oversight wording, and any applicability limit for nonprofits. The page was not readable this pass (CO-050).
8. **Unclaimed property for grant checks.** Whether checks payable to charities are treated as vendor checks, and the dormancy and exemption rules by state (CO-036). Unclaimed-property specialist.
9. **SOC reliance approach.** Whether the sponsor's external auditor will rely on a SOC 1 Type 2, test directly, or accept a deterministic release gate in place of a second human (CO-033, CO-043; CNV-GOV-001/003 gates). Sponsor's auditor.
10. **OFAC strict liability.** Confirm the civil-liability standard in OFAC's Economic Sanctions Enforcement Guidelines, which I did not read in this pass (CO-016).
11. **Proposed DAF regulations.** Check finalization status after 2026-05-08 (CO-014).
12. **Auditor independence.** Whether the sponsor's audit firm may perform bookkeeping or reconciliation under the AICPA independence rules (question 3).
13. **UPMIFA.** Whether it applies to DAF assets in the sponsor's state(s) (CO-055).
14. **California and Hawaii charitable fundraising platform registration.** The statutes were taken from Unbound CNV-LEG-002 and were not re-read (CO-054).

## Sources (all accessed 2026-11-27)

Statutes and regulations
- https://www.law.cornell.edu/uscode/text/26/4966: IRC 4966 taxable distributions; DAF, sponsoring organization and fund manager definitions
- https://www.law.cornell.edu/uscode/text/26/4967: IRC 4967 prohibited benefits
- https://www.law.cornell.edu/uscode/text/26/4958: IRC 4958(c)(2), (f)(1)(E)-(F), (f)(7)-(8)
- https://www.law.cornell.edu/uscode/text/26/170: IRC 170(f)(18)
- https://www.law.cornell.edu/uscode/text/26/6033: IRC 6033(k)
- https://www.law.cornell.edu/cfr/text/26/53.4945-5: expenditure responsibility
- https://www.govinfo.gov/content/pkg/FR-2023-11-14/html/2023-24982.htm: 2023 proposed DAF regulations (88 FR 77922; seen via search, Federal Register site blocked fetch)
- https://cof.org/node/20145: Council on Foundations status page (updated 2026-05-08: not finalized)
- https://www.irs.gov/instructions/i990sd: Schedule D instructions, Part I
- https://www.irs.gov/charities-non-profits/eo-operational-requirements-recordkeeping-requirements-for-exempt-organizations: IRS EO recordkeeping
- https://www.law.cornell.edu/cfr/text/31/501.601: OFAC recordkeeping (10 years)
- https://www.law.cornell.edu/cfr/text/31/501.603: OFAC blocked property reports
- https://www.law.cornell.edu/cfr/text/31/501.604: OFAC rejected transaction reports
- https://www.law.cornell.edu/uscode/text/31/5312: BSA financial institution definitions
- https://www.fincen.gov/sites/default/files/administrative_ruling/FIN-2013-R002.pdf: FinCEN payment processor exemption ruling (seen via search)
- https://www.law.cornell.edu/uscode/text/15/44: FTC Act "corporation" definition
- https://www.law.cornell.edu/uscode/text/15/80b-3: Advisers Act 203(b)(4)
- https://www.govinfo.gov/content/pkg/PLAW-104publ62/html/PLAW-104publ62.htm: Philanthropy Protection Act of 1995 (seen via search)
- https://www.law.cornell.edu/ucc/4A/4A-202: UCC 4A-202 security procedures
- https://california.public.law/codes/government_code_section_12586: Cal. Gov. Code 12586 (seen via search)
- https://www.oag.ca.gov/sites/all/files/agweb/pdfs/charities/pdf/nonprofit-integrity-act-nov04-auditreq.pdf: CA AG Nonprofit Integrity Act audit guidance (seen via search)
- https://nysenate.gov/legislation/laws/EXC/172-B: NY Exec. Law 172-b (seen via search)
- https://www4.erie.gov/comptroller/sites/www4.erie.gov.comptroller/files/2026-06/2026.06.03_oag_sugarman_presentation.pdf: NY AG Charities Bureau presentation 2026-06-03 (seen via search)
- https://www.nysenate.gov/legislation/laws/GBS/899-BB: NY SHIELD Act (seen via search)
- https://ag.ny.gov/resources/organizations/data-breach-reporting/shield-act: NY AG SHIELD guidance (seen via search)
- https://www.mass.gov/regulations/201-CMR-1700-standards-for-the-protection-of-personal-information-of-ma-residents: 201 CMR 17.00 (fetch returned 403; search summary only)
- https://www.mass.gov/info-details/requirements-for-data-breach-notifications: MA breach notification (seen via search)
- https://www.ag.state.mn.us/Consumer/Handbooks/CharitiesLaws/CH7.asp: MN AG UPMIFA handbook (seen via search)

Guidance, rules and standards
- https://ofac.treasury.gov/media/16331/download: OFAC, A Framework for OFAC Compliance Commitments (2019); text extracted and read
- https://www.govinfo.gov/content/pkg/FR-2006-10-31/pdf/06-8961.pdf: Treasury Anti-Terrorist Financing Guidelines (voluntary; seen via search)
- https://nacha.org/content/third-parties-ach-network: Nacha TPSP/TPS definitions and obligations
- https://nacha.org/rules/ach-rules-compliance-audit-requirements: Nacha Rules Compliance Audit rule
- https://www.nacha.org/rules/risk-management-topics-fraud-monitoring-phase-1: Nacha fraud monitoring Phase 1 (seen via search)
- https://www.nacha.org/rules/risk-management-topics-fraud-monitoring-phase-2: Nacha fraud monitoring Phase 2
- https://www.nacha.org/rules/third-party-sender-roles-and-responsibilities: Nacha TPS roles (seen via search)
- https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-1: AICPA SOC 1 description
- https://standards.auasb.gov.au/node/288: ASA 402 (Australian analogue of AU-C 402; seen via search)
- https://aaahq.org/node/35020: COSO 2013 compendium, Principle 10 (secondary; seen via search)
- https://www.ftc.gov/business-guidance/resources/safeguards-rule-what-your-business-needs-know: FTC Safeguards Rule guidance (seen via search)
- https://www.osc.ny.gov/state-agencies/gfo/chapter-xiv/xiv1-outstanding-check-outreach-and-escheatment: NY OSC escheat guidance (seen via search)
- https://www.quimbee.com/cases/cincinnati-insurance-co-v-wachovia-bank: positive pay case summary (secondary; seen via search)
- https://www.reninc.com/wp-content/uploads/2025/08/Online-RAC-MSA_v1.pdf: Ren public MSA template (cited via repository register N01; not re-fetched)

Repository sources (local)
- `docs/financial-core-control-spec-v0.5.md`; `docs/automated-charity-assurance-180-day-decision-record-v0.1.md`; `docs/sponsor-white-label-grant-policy-affirmations-v0.1.md`
- `data/sponsor-governance-controls-2026.csv`; `data/technology-audit-control-matrix-2026.csv`; `data/ren-public-contract-clauses-2026.csv`
- `research/competitive-displacement/data/registers/adversarial-challenges.csv` (CHL-037, CHL-038, CHL-066); `research/competitive-displacement/14-alternative-enterprise-models.md`
- `research/commercial-opportunity/servicing-economics/03-organization-and-budget.md`, `07-market-entry-strategy.md`, `08-adversarial-review.md`
- `/home/user/kemiller2002/unbound/requirements/governance/SPONSOR-AUTHORITY-AND-AUTONOMOUS-OPERATIONS.md` and CNV-* clauses in `requirements/` (GRT, PAY, FIN, LEG, PLT)
