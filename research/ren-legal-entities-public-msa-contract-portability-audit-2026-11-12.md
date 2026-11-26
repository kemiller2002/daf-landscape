# Ren legal entities and public master service agreements: contract and exit-rights audit
**Research date:** 2026-11-12. **Evidence:** Ren-published standard MSAs, public company history, RCF Form 990, official Morgan Stanley GIFT materials. **Important:** Public MSAs are CUSTOMER-FACING templates, NOT the private RCF↔Ren related-party services agreement and NOT proof of terms negotiated by any named institutional customer.

## Major discovery: public contract library
https://www.reninc.com/master-service-agreements/
- RCF MSA June 2023: https://www.reninc.com/wp-content/uploads/2025/08/Online-RCF-MSA_v1.pdf
- Renaissance Acquisition Company LLC (RAC, Ren) MSA June 2023: https://www.reninc.com/wp-content/uploads/2025/08/Online-RAC-MSA_v1.pdf
- Ren iPhi MSA June 2023: linked as a .docx, not yet text-reviewed.
- Product definitions are separately linked. Actual service scope, fee schedules and exceptions depend on signed Order Forms and Work Orders.

## Comparative standard terms (RCF and RAC agreements)
| Topic | Public RAC MSA | Public RCF MSA | Interpretation |
|---|---|---|---|
| Service counterparty | Renaissance Acquisition Company LLC | Renaissance Charitable Foundation Inc. | Distinct legal service counterparties; cannot collapse sponsor and vendor |
| Pricing | Work Order, not MSA | Work Order, not MSA | No customer-specific fee or Ren profit disclosure |
| Auto-renewal | 1 year; 60-day advance nonrenewal notice | same | Administrative switching friction, not proof of inability to exit |
| Material breach | 30-day cure; service suspension for nonpayment | same | Scope for interruption depends on specific contract |
| Termination fees | Certain terminations pay projected service fees through end of termination quarter | same | Not an unlimited penalty; actual Work Order may override |
| Return | Return all defined 'Customer Materials' on request or termination | same | Defined as materials **provided by customer**, not necessarily all vendor-generated records |
| IP | Provider owns inventions/deliverables except Customer Materials; customer gets limited object-code license after payment | same | Different from ownership of sponsor's underlying donor/transaction data |
| Warranty | Disclaims error-free and secure/uninterrupted operation | same | Does not prove platform insecure or unavailable |
| Liability | Generally capped at prior 12 months fees under affected Work Order, exceptions for gross negligence/willful misconduct/legal prohibition | same | Review indemnification and work-order overrides |
| Assignment | Written consent of other party generally required | same | Possible change-of-control relevance; need actual work order |
| Governing law | Indiana, Marion County disputes and arbitration | same | Forum selection, not evidence of dispute |
| Service exclusivity | Nonexclusive | same | No evidence of exclusive institution-wide channel |

**Caution:** Some language appears similar across the two MSAs; review both full documents and individual work orders before treating every clause as identical.

## Data portability: specific textual gap
RAC §4.5 says Ren returns Customer Materials (defined in §5.1 as materials *provided by Customer*). The template does not expressly require a normalized export of:
- donor/fund identity and account history;
- all generated transaction records and reconciliation entries;
- eligibility screening snapshots, reviewer rationale, exceptions and policy versions;
- grant approvals and overrides with timestamps and decision authority;
- payment instructions, bank confirmations, reissues and audit logs;
- all attachments and data lineage.

**Inference:** The MSA alone is insufficient evidence of complete exit portability. It does NOT prove Ren refuses exports, charges prohibitive migration fees, or retains sponsor-owned statutory records; work orders, data protection addenda and law may create additional obligations.

## Entity mapping
- **Renaissance Charitable Foundation Inc.** charitable sponsor, EIN 35-2129262, independently registered nonprofit.
- **Renaissance Acquisition Company LLC**, EIN 20-0235398 per Florida registration, active Indiana foreign LLC in Florida filings, named contracting party in public Ren MSA and RCF 2024 audited Note 9.
- **Renaissance Administration LLC**, EIN 35-2111971 per RCF 2024 Form 990, named Ren contractor/payee on Schedule L and Schedule O. Its precise legal relationship with Renaissance Acquisition Company requires entity filings, contract assignments and intercompany accounting.
- **RenPSG** historic corporate/brand usage and back-office administrator designation on Morgan Stanley GIFT site. Ren's own corporate timeline says it acquired Crown Philanthropic Solutions and rebranded as RenPSG in 2016; acquired Pinkaloo in 2021; acquired Stellar Technology Solutions/iPhi in 2023; Bain Capital Tech Opportunities and Valeas invested in 2023.
- **Ren iPhi** has a separately published platform MSA; do not assume it uses the same technology stack as DonorFirstX.
Sources: https://www.reninc.com/about-ren/ ; https://search.sunbiz.org/Inquiry/CorporationSearch/SearchResults?Detail=FL.DOS.Corporations.Shared.Contracts.FilingRecord&InquiryDirectionType=ForwardRecord&InquiryType=EntityName&ListNameOrder=RENAISSANCEACADEMY+N960000039960&SearchNameOrder=RENAISSANCEACQUISITION+F070000004550&SearchTerm=REM+YUL+H+MEDINA ; https://renaissancecharitable.org/wp-content/uploads/2026/01/Form-990-Public-Disclosure-Copy-2024-RCF.pdf

## Independent-sponsor comparison
Morgan Stanley GIFT publicly calls RenPSG an **unaffiliated back-office administrator** and Morgan Stanley Smith Barney its investment manager. Its 2024 impact report attributes donor/account/grant statistics to Renaissance Administration LLC. This reinforces the difference between RCF's related-party sponsor-service arrangement and an independent sponsor outsourcing to Ren. **No reliable named dollar payment to Ren from MS GIFT yet verified.**
Sources: https://www.morganstanley.com/what-we-do/wealth-management/gift ; https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-impact-report.pdf

## Clarity adjudication
- **Verified:** public RAC and RCF MSAs include nonrenewal, breach, limited materials return, IP and liability clauses.
- **Verified:** Renaissance Acquisition Company LLC and Renaissance Administration LLC are separately named in public records; entity ownership chain unverified.
- **Verified:** Ren has acquired multiple technology businesses, so the label 'Ren platform' is insufficient to infer a single codebase.
- **Unverified:** any named client actually signed unmodified standard terms; all data export rights; client-specific termination costs; Ren/RCF internal contract.
- **Unverified:** institutional Ren fee amounts outside RCF, operating margin, customer concentration.

## Next steps
1. Download and inspect iPhi MSA .docx and product definitions; compare license, data export, hosting, availability, liability and change-of-control terms.
2. Obtain entity filings for Renaissance Administration LLC, Renaissance Acquisition Company LLC, Ren Inc., RenPSG, and subsidiary brands; reconcile legal assignments.
3. Review independent-sponsor audits/990 Schedule O and Part IX to find Ren named payees and fees without equating all IT or admin expense with Ren revenue.
4. Draft standardized sponsor procurement questionnaire: data ownership, full export schemas, grant provenance, RTO/RPO, subcontractor register, security attestations, exit testing, work-order override and grant authority.
5. Benchmark competing vendor contracts where public. Never equate published MSA template with executed customer contract.
