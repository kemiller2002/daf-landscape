# 06 — Minimum human control obligations

Register: [`control-obligations.csv`](data/registers/control-obligations.csv) — 63 obligations (CO-001..063), each with mandate class, citation, source URL and date, whether a human and independence are required, who can satisfy it, whether it can be fractional/shared, sponsor personnel, external, or automated with oversight, minimum coverage, limitations and recurring effort. Notes with sources: [control-obligations-notes.md](data/evidence/control-obligations-notes.md). **Not legal advice.** No professional was engaged; fourteen matters await confirmation (§6).

## 1. The decisive distinction: law versus expectation

| Obligation | Mandate class | Practical consequence |
|---|---|---|
| Sponsor "owns and controls" the fund; acknowledgments state "exclusive legal control" (IRC 4966(d)(2), 170(f)(18)(B)) | **LEGAL-MANDATE** | Final grant authority, asset ownership and investment mandate sit with the sponsor. An administrator, software or AI cannot hold it. |
| 20% tax on taxable distributions (sponsor); 5%/10% personal taxes on knowing "fund managers" (4966, 4967) | **LEGAL-MANDATE** | The sponsor needs a named, accountable roster. Unbound's rule that vendor staff never hold A3+ authority (CNV-GOV-004) is sound. |
| Form 990 Schedule D DAF reporting (6033(k)); OFAC blocking/reject reports within 10 business days, annual report by Sept 30, 10-year records (31 CFR 501) | **LEGAL-MANDATE** (sponsor holds it; agent may file) | Unbound prepares data; sponsor officer signs or remains responsible. |
| State registration; state-required audits (e.g., CA ≥ $2M, NY > $1M revenue thresholds) ; escheat | **LEGAL-MANDATE** (sponsor) | Sponsor-owned; Unbound supplies data. |
| **Two-person payment authorization** | **AUDITOR-EXPECTATION / INDUSTRY-PRACTICE / CONTRACTUAL** (UCC 4A-202 shifts wire-fraud loss to a customer who refuses offered security procedures); **ECHELON-POLICY** (CNV-GOV-003) | Not law. Its form can be designed: a sponsor treasury officer releasing in the bank portal satisfies it. |
| **Independent reconciliation** | **AUDITOR-EXPECTATION** (COSO; AU-C 402) and ECHELON-POLICY (GOV-AUTH-014, CNV-GOV-003, CNV-FIN-004) | Independence is functional: the reconciler holds no payment rights. Sponsor finance, an outsourced CPA or an Echelon accountant without release rights all qualify. |
| **SOC 1 / SOC 2 reports** | AUDITOR-EXPECTATION and CONTRACTUAL | Required to sell to institutions; owner decision OD-P-GOV starts SOC 1 readiness before the first staffed client. |
| Nacha TPSP Rules Compliance Audit; risk-based fraud monitoring (mandatory since 2026-06-19/22, reviewed annually) | **CONTRACTUAL** (Nacha rules via ODFI) | Applies if the platform originates or transmits ACH as a TPSP. Monitoring need not screen each entry pre-processing. |
| Sanctions compliance officer | REGULATORY-GUIDANCE (OFAC Framework) | May be the same person as other compliance roles (OFAC footnote). |
| Security programme owner; breach notification | LEGAL-MANDATE (state breach laws); state safeguards rules | Fractional vCISO acceptable; breach counsel retainer. |
| Change approval by two non-authors for control-relevant code | **ECHELON-POLICY** (CNV-PLT-010); ITGC auditor expectation | Needs at least three qualified engineers (or an external reviewer). Cannot be met by one person. |

## 2. Answers to the mission's questions

1. **Reserved to the sponsor:** final authority over grants and assets; the fund-manager roster; Form 990/Schedule D; OFAC holder obligations; escheat; state registration and audits; investment policy and adviser appointment.
2. **Delegable to an administrator** (responsibility does not move): acknowledgments, grant dossiers, payment files, screening, charity monitoring, reconciliation matching, OFAC report data.
3. **Automatable under sponsor-approved policy:** public-charity eligibility checks, related-party payee blocks (4958(c)(2)), acknowledgment generation, list screening and delta re-screening, retention, return matching, continuous reconciliation matching.
4. **Uncertain:** whether a board-adopted, version-pinned policy may approve a grant with no person looking at it (CO-004). Nothing found requires or expressly permits it. Unbound's middle line — board policy, named delegate and exception reviewer, quarterly sampled review — is retained. The 2023 proposed DAF regulations remain proposed (Council on Foundations page updated 2026-05-08).

## 3. Minimum independent control coverage (one TPA, one sponsor)

| Seat | Must be independent of | Minimum satisfier | Fractional? |
|---|---|---|---|
| Grant authority delegate and exception reviewer | Unbound | Sponsor officer (board-appointed) | Yes |
| Payment releaser | Payment-file preparer | Sponsor treasury officer | Yes |
| Payment-file preparer / exception coordinator | Releaser, reconciler | Echelon operations or automation plus sponsor | Yes |
| Reconciliation exception reviewer | Initiation and release | Sponsor finance, outsourced CPA, or Echelon accountant without payment rights | Yes |
| Monthly close sign-off (controller) | Payment chain | Sponsor controller or fractional controller | Yes |
| Sanctions compliance officer | — (testing separate) | Sponsor (sponsor duty); Echelon compliance owner (Unbound's programme) | Yes |
| Sanctions-programme testing | Screening operators | External or sponsor internal audit | — |
| Nacha TPSP compliance owner | — | Echelon compliance owner | Yes |
| Nacha Rules Compliance Audit | ACH operations | External auditor (recommended) | — |
| Security programme owner, incident lead | Change authors (review role) | vCISO | Yes |
| Change approvers (two non-authors) | Author | Two other engineers or external reviewer | Shared |
| Access reviewer | Access administrator | Sponsor (users); Echelon manager (staff) | Yes |
| Complementary user-entity controls | Service organisation | Sponsor personnel | Yes |
| Financial-statement auditor; SOC 1/SOC 2 service auditor | Sponsor and Echelon | External CPA firms | — |
| Form 990 preparer / signer | — | Outsourced CPA / sponsor officer | Yes |
| Counsel (perimeter, delegation, fund-manager status, registration) | — | External counsel (initially one-time) | — |

**Implication.** With sponsor personnel in the delegate, releaser, sign-off and complementary-control seats, **the Echelon side needs no dedicated full-time control staff**. It needs a fractional compliance owner, a fractional security owner, and — if it keeps books — a fractional controller, plus three engineers for change approval. If the sponsor cannot staff the releaser and sign-off seats, Echelon needs two people outside each other's chain plus an external fractional controller, and CNV-GOV-003's three-person rule applies.

In the model this is encoded as: 2 named persons per segregated pool (initiation, authorization, reconciliation), 3 named engineers, fractional floors for controller (0.03 FTE) and compliance (0.03 FTE) and a security/on-call owner (0.1 FTE) whenever Echelon runs controls (`min_named_*`, `min_fraction_fte` in [`roles.csv`](data/model-inputs/roles.csv)).

## 4. Limits of each arrangement

| Arrangement | Strength | Limitation |
|---|---|---|
| Sponsor personnel | Holds legal authority; independent of vendor by construction | Availability and skill vary; small sponsors may lack a treasury officer; due diligence may still demand vendor-side controls |
| Shared Echelon personnel | Economical across products | Independence is lost if the same person prepares and releases or authors and approves; today one human holds every role, so no shared pool exists yet |
| External professionals | Independent; qualified | Cost per hour; availability at peaks; auditor-independence rules limit what the sponsor's auditor can do |
| AI agents | Prepare evidence, triage, draft | **Not** independent controls, legal advice or external audit; their outputs need human acceptance and change control |
| Fractional officers | Satisfy named-role expectations | Must not hold incompatible duties on the same transaction; key-person risk if one fractional person covers several roles |

## 5. What this changes economically

- The original model priced a salaried controller and compliance staff into fixed cost and also priced their minutes as events. The obligation analysis supports **fractional, workload-sized roles** plus sponsor-held seats.
- It does **not** support "zero humans": four bounded human touchpoints (grant authority, sanctions disposition, payment release, monthly sign-off) remain even under full automation, all of which can be performed outside Echelon's staff.
- It **adds** costs the original under-weighted: three engineers for change approval; external Nacha audit and sanctions testing; breach counsel; SOC 1 when Echelon runs controls.

## 6. Matters requiring professional confirmation (none commissioned; DF-ASR-2026-0D0F)

Board-delegated automated grant approval and fund-manager status; contracted officers as fund managers; Nacha TPSP vs TPS status and audit externality; money-transmission perimeter; investment-adviser/broker perimeter; GLBA/FTC Safeguards applicability; Massachusetts 201 CMR 17 text; escheat of grant checks; the sponsor auditor's SOC reliance approach; OFAC civil-liability standard; finalisation of the proposed DAF regulations; auditor-independence limits on reconciliation; UPMIFA applicability; California and Hawaii platform registration.
