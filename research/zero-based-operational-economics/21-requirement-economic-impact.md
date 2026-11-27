# 21 — Requirement economic impact

Registers: [`requirement-economic-impact.csv`](data/registers/requirement-economic-impact.csv) (REI-001..051: cost category, driver, frequency, minutes per 1k accounts, infrastructure and external impact, responsible organisation, alternatives, prevention, risk, control objective preserved, priority, validation) and model output [`requirement-hours.csv`](data/model-outputs/requirement-hours.csv) (vendor and sponsor hours per Unbound requirement at the reference scenario; an activity's hours are split evenly across its requirements). **No mandatory control is proposed for removal.** Every alternative names the control objective it preserves and traces to the original requirement ID.

## 1. Requirements that drive the most recurring hours (reference: $500M, full administration)

| Requirement | Vendor h | Sponsor h | What it creates |
|---|---:|---:|---|
| CNV-PLT-010 (signed builds; two non-author approvers; release rings) | 929 | 35 | change review, defect and integration work under change control |
| CNV-ARC-005 (architecture and maintenance discipline) | 839 | 0 | maintenance, defects, integrations, regulatory change |
| GOV-AUTH-004 (authority and approvals) | 144 | 36 | manual journals, access recertification, approvals |
| SOC2-011 | 149 | 35 | change and release evidence |
| CNV-AIO-002 (AI dossiers with deterministic findings) | 122 | 58 | dossier preparation, AI change control |
| UNB-XIN-SVC-007, CNV-SVC-001 (service and case kernel) | 182 | 1 | human-handled contacts |
| CNV-GRT-011, CNV-GRT-001, CNV-GOV-004, CNV-GRT-009 and grant requirements on OA-GRT-005 | ~60 each | ~60 each | Tier-2 exception review (sponsor decides; vendor prepares) |

## 2. Prioritised redesign register (cost reduction with control objective preserved)

| Priority | Requirement | Cost category | Redesign proposal | Control objective preserved |
|---|---|---|---|---|
| **P1** | CNV-GRT-011 Tier-2 enhanced review (9% of grants × 42 min — the largest activity in the inventory) | manual review | reuse recipient-level determinations across grants, funds and sponsors; calibrate each trigger's specificity from replay false-positive rates; batch decisions on dossiers | enhanced human review of genuinely risky grants (§4966/4967) |
| **P1** | CNV-GOV-004 one-sponsor-per-person reserved authority | dedicated staffing (sponsor side) | contracted or fractional appointees; a shared bench of pre-appointed reviewers, each serving one sponsor; validate the 0.5 FTE per holder default | independence of reserved decisions |
| **P1** | CNV-GRT-001 pre-delegation batch approval | human approval | make the board delegation an **activation gate** with packaged resolutions, so no live "every grant is a human decision" phase exists | sponsor control |
| **P1** | CNV-GOV-003 three-distinct-person release | human approval | obtain auditor and board acceptance of the deterministic release design at onboarding; sponsor treasury officer as releaser | segregation of duties in payment release |
| **P1** | UNB-GAP-013 unidentified deposits and incomplete transfers | recurring investigation | notification-first contribution intents with unique fund references or virtual accounts | no plug postings; correct attribution |
| **P1 (new)** | Per-sponsor close, audit support and Schedule D packages (UNB-ACC-017/020; OA-ACG-007/010/011) — ≈ 870-1,190 vendor h per small sponsor (sponsor-unit-economics.csv) | dedicated staffing | continuous close with exception-only certification; one close workbench across sponsors on the shared cluster; agreed auditor reliance on automated controls | accurate, independently signed-off sponsor financial records |
| **P1 (new)** | Compliance SLAs of 24-48 h during December (sanctions, fraud, holds) | dedicated staffing | tiered SLAs by risk (true potential matches 24 h; low-score alerts 5 days), pre-December list hygiene; staff to the tiered peak | OFAC 10-business-day reporting; fraud holds |
| P2 | CNV-FIN-004 / CNV-GOV-003 layered reconciliation assurance | manual reconciliation | one independent attestation sample feeding the controller's sign-off | independent reconciliation |
| P2 | CNV-FIN-005 daily NAV sample | manual review | weekly or risk-triggered sampling (values come from the external manager, OD-M-07) | valuation integrity |
| P2 | CNV-GRT-003 180-day deep review | repetitive compliance | hybrid vetting: continuous monitoring + deterministic 180-day re-evaluation + human review of exceptions and high-risk tier ([15](15-charity-vetting-alternatives.md)) | 180-day validity rule |
| P2 | UNB-XIN-CLM-005, CNV-GRT-011 sampling, CNV-GOV-008 board sampling | manual review | one error-bound sampling plan serving all three | decision-quality assurance |
| P2 | CNV-PAY-002 / CNV-PAY-003 destination evidence; uncashed checks | operational exception | bank-originated account-owner match; reuse networked-rail enrolments; shift recipients to electronic rails | payment destination integrity; escheat compliance |
| P2 | CNV-SVC-001 / CNV-SVC-002 service and December readiness | operational exception | proactive status notices; grounded answers; shared service pool across sponsors | donor service quality |
| P2 | CNV-GOV-001 SOC 1 and SOC 2 | external subscription | combined examination by one firm; scope set by actual reliance | assurance for sponsors' auditors |
| P2 | UNB-ONB-025 integration certification | integration | certify once per counterparty, not per sponsor; reuse mappings | integration correctness |
| P2 | CNV-EXP-002, UNB-SMP-CFG-001 migration and configuration | integration / customisation | migration factory with reusable incumbent mappings; closed extension-point catalogue; no forks | complete, reconciled migration |
| P2 | CNV-AIO-001 AI governance | dedicated staffing | shared evaluation sets across sponsors; December change freeze | AI recommends, humans decide |
| P2 | CNV-PLT-011 72-hour hold default | operational exception | platform default threshold instead of holding every non-recurring recommendation | fraud hold for unusual grants |

Full list with P3 items: the register (28 P3, 18 P2, 5 P1 from the inventory track; two P1 items added from the model above).

## 3. Proposed standard economic impact record

Only for requirements with material recurring cost (rule of thumb: > 40 vendor or sponsor hours a year at the reference scale, any dedicated-staffing effect, any new external subscription, or any new independent human approval):

```
economic_impact:
  cost_category: manual-review | human-approval | recurring-investigation | dedicated-staffing |
                 external-subscription | infrastructure | integration | document-preparation |
                 operational-exception | sponsor-customization | manual-reconciliation | repetitive-compliance
  cost_driver: <unit that scales the cost: grants, accounts, sponsors, platform>
  activities: [OA-...]                 # links to the operational-activities register
  expected_frequency: <low/base/high per driver unit>
  human_minutes: <low/base/high per event>
  responsible_organization: sponsor | administrator | software_provider | external | shared_echelon
  infrastructure_impact: <none | text>
  external_costs: <none | text with price source>
  control_objective: <what must remain true>
  alternatives: [<design that preserves the objective at lower recurring cost>]
  prevention: [<upstream mechanism>]
  validation_method: <how the cost will be measured>
  evidence_class / confidence
```

Requirements with immaterial cost carry nothing.

## 4. Responsibilities that should remain with sponsors

Reserved legal decisions (Tier-2 grant decisions, declines, discretionary holds, complex gift acceptance), board delegations and policy adoption, reserved-authority appointments, payment release (or second release) through the sponsor's bank, monthly close sign-off, Form 990/Schedule D signing, state registrations, retention schedule approval, investment policy and adviser appointment, review of Unbound's SOC report and complementary user-entity controls, and funding transfers to disbursement accounts. Unbound prepares evidence for all of them.
