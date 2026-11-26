# 14 - Alternative enterprise models

Status: research (2026-11-26; revision 2 after adversarial review, see [20](20-adversarial-review.md)). Legal conclusions here are **not** legal advice and require professional confirmation; they are marked as such. Revision 2 incorporates the compliance and procurement reviews (CHL-037..043, CHL-018, CHL-019, CHL-066). Economics from [results.md](model/out/results.md) and PR #87 (SRC-002). EDF and Clarity applied as described in §4.

## 1. Is the conventional DAF administrator the right organisational unit?

**Not as the entry unit.** It carries the most capital, liability, governance and staffing, and it competes where incumbents' distribution economics are strongest. It may be the right *eventual* unit if a design partner anchors it.

## 2. Comparison

| Model | Required capital | Revenue structure | Gross margin (indicative) | Regulatory exposure | Staffing | Governance | Customer ownership | Liability / insurance | Distribution | Time to revenue | Defensibility | External dependence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Technology licensor (MD-6) | ~$6-8M P50 to payback (ER-7/ER-4) | Per-account licence ($81-150) or subscription | High (vendor variable ~$31/acct) | **Moderate**: a platform that creates ACH or positive-pay files is almost certainly a Nacha TPSP (annual Rules audit; fraud-monitoring rules since 2026); SOC 1 Type II likely because sponsors' auditors rely on it; a bank third party under the 2023 interagency guidance in bank channels (counsel: OQ-009) | Engineering, security, support | Standard company | Sponsor or channel partner | E&O, cyber | Needs channel (ER-7) | 15-18 months | Low-moderate (copyable; switching costs once installed) | Channel partner; hosting |
| Shared infrastructure provider (registry, evidence, reconciliation utilities) | $0.5-2M | Subscription per sponsor or per grant | High | Low; becomes SOC 1 relevant if relied on | Small | Standard | Sponsors | E&O; media rider if publishing facts | Direct to sponsors and platforms | 6-12 months | Low (public data) except archive | IRS/OFAC availability |
| Sponsor enablement platform (sponsor-in-a-box for new sponsors) | $2-4M | Licence + implementation | Medium | Moderate (formation support; not legal advice) | Implementation | Standard | New sponsors | E&O | Weak (≈6.5 new sponsors a year) | 12-18 months | Low | Counsel partners |
| Modular operational services (exceptions, reconciliation, vetting as a service) | $1-3M | Per event / per account | Medium | Moderate: acting for sponsors on reserved-adjacent work | Ops staff by workload | Controls, SOC 1 | Sponsor | E&O, crime | Direct | 9-15 months | Low-moderate | Sponsor platforms' APIs |
| Federated sponsor network (several sponsors share infrastructure; each keeps legal control) | $3-6M | Cost-sharing + fees | Low-medium | High coordination; antitrust and data-sharing terms (counsel) | Shared services | Multi-party governance | Members | Shared | Requires a convener | 24+ months | High if formed | Member commitment |
| Charity intelligence provider | $0.5-1.5M (ER-1) | API subscription | High if volume | Low; defamation/media risk if publishing ratings | 2-4 | Standard | Platforms and sponsors | Media rider | Direct; Candid incumbent | 9-15 months | Low (except archive) | Public data |
| Financial workflow infrastructure (reconciliation, file ingestion, STP) | $1-3M | Per file / per transaction | Medium-high | Low-moderate | Engineering | Standard | Sponsors, administrators | E&O | Direct | 12-18 months | Low-moderate | Bank and custodian formats |
| Exception management service (hybrid MD-7) | ~$6-9M | Licence + exception fees | Medium | Moderate | Exception desk | SOC 1/2 | Sponsor | E&O, crime | Channel or direct | 15-18 months | Moderate | Sponsor platform |
| Full-service administrator (MD-5) | $4.5M founder-led (PR #87) to ~$10.3M market-pay (ER-5, revision 2) | 15-25 bps or per-account + bps | Low-medium | Highest: holds and releases charitable money under sponsor authority; OFAC; 4966/4967 support; Nacha | 3 core + workload hires + independent reconciler | Three-person release; board reporting | Sponsor (and donors indirectly) | E&O, D&O, crime, cyber | Direct; competes with Ren economics | 15-18 months | Moderate once operating | Bank, custodian, rails |

## 3. What must stay with the sponsor and what may be delegated

| Responsibility | Must remain with sponsor | Delegable (with oversight) | Status |
|---|---|---|---|
| Exclusive legal control of assets (IRC 4966 sponsoring organisation) | Yes | — | Legal conclusion: **requires counsel confirmation** |
| Approval of grants and reserved decisions (variance, discretionary grants, policy exceptions) | Yes (can adopt rules that pre-approve) | Preparation, evidence, routine release under adopted rules | Operational hypothesis grounded in CNV clauses |
| Charity eligibility determination | Responsibility yes | Evidence gathering, monitoring, screening, dossier | Operational hypothesis |
| Taxable-expenditure and prohibited-benefit (4966/4967) policy | Yes | Rule execution, flagging | Legal conclusion: counsel |
| OFAC compliance | Sponsor accountable | Screening and alert triage; **the vendor has its own direct obligations as a US person** facilitating payments, and OFAC record retention is now 10 years (31 CFR 501.601) | Legal conclusion: counsel (CHL-039) |
| State charitable-solicitation law | Sponsor registration | An administrator that holds and releases money or receives contributions for compensation may fall within state definitions of commercial fundraiser or fundraising counsel | Counsel: top-10-state opinion (CHL-043) |
| Pending 4966 regulations (88 FR 77922, proposed Nov 2023) | — | Would treat some personal investment advisers as donor-advisors, affecting advisor-channel economics | Monitor; scenario in [16](16-commercial-entry-strategy.md) §7 (CHL-042) |
| Payment origination (Nacha Originator) | Sponsor as Originator (CNV-PAY-001) | A vendor that creates files is a TPSP regardless of who transmits; TPSP obligations (audit, fraud monitoring) are its own, not delegated | Counsel (OQ-009); research view: assume TPSP status (CHL-037) |
| Acknowledgments (170(f)(8)/(18)) | Sponsor's obligation | Production and delivery | Operational |
| Financial statements, audit, Form 990 | Yes | Data, reconciliation, evidence | Operational |
| Investment policy | Yes (board) | Execution via custodian/adviser | Operational |

## 4. EDF and Clarity

- **EDF** was applied only to **observed outcomes**, as the framework intends (PR #87 precedent): the observed switch record (S01-S44) diagnoses that the failure mode of "better technology does not displace" is a **distribution-and-incentive constraint**, not a capability gap. EDF was not executed on hypothetical companies.
- **Clarity** readiness was applied to the decisions in [23](23-executive-decision-register.md): most are **not ready** because no owner has accepted ownership, review dates and outcome measures. This package supplies options and evidence, not decisions.

## 5. Recommendation

Every model also needs (CHL-018, CHL-019): a subprocessor register (hosting, AI model provider, data sources, email, payments) with DPA, no-training and residency terms and an AI-off mode; and a contract-terms register (liability cap, indemnities, insurance limits, breach SLA, audit rights) costed before G1. Eligibility determinations remain the sponsor's; the vendor disclaims them and supplies evidence.

Begin as a **technology licensor**, delivered first as a module inside a channel partner's offering ([16](16-commercial-entry-strategy.md)), with narrow non-custodial services as pre-sales components (charity eligibility evidence, migration assessment and reconciliation), sold through or alongside a channel partner; keep full administration as an option exercised only behind a signed anchor (DEC-002). Echelon Foundry does not need to become a conventional DAF administrator to enter the market.
