# 00 — Executive findings

Research package: [file ingestion and straight-through processing](README.md) (2026-11-26).

This is industry research. It contains no product requirements; a product's requirements built on it belong in that
product's repository.

1. **115 distinct ways information enters a DAF sponsor**, across twelve domains: sponsor onboarding, advisor and donor
   administration, contributions, grants, charity vetting, investments, accounting and treasury, compliance, migration,
   customer service and platform configuration ([03](03-DAF-INGESTION-WORKFLOW-INVENTORY.md)). 38 are documented by
   public evidence; 77 are inferred from adjacent practice and regulation.
2. **Intake is pooled receipt plus free-text attribution.** Securities and wires land in one sponsor-level account; the
   fund key travels in an FBO line, DTC note or wire memo that sending institutions do not reliably carry
   (FIE-A-001, FIE-A-025, FIE-A-123, FIE-A-131). Sponsors respond by requiring notification first, rejecting, or holding
   and sweeping unidentified gifts (FIE-A-024, FIE-A-005, FIE-A-079). This, not file parsing, is the industry's main
   ingestion exception.
3. **Paper, fax and PDF remain first-class channels at the largest sponsors** (FIE-A-134), with physical controls
   (medallion guarantees, wet signatures). Bulk structured intake exists in community-foundation software and the TIFIN
   family, but no national sponsor publicly documents advisor bulk grants or roster uploads (FIE-A-022, FIE-A-055,
   FIE-A-093, FIE-A-104).
4. **Adjacent industries show the achievable pattern and its limit.** Healthcare's EFT/remittance reassociation and AP
   capture platforms reach 85–95% automated matching on structured data, but a permanent tail remains: 89% electronic
   remittance after decades of mandate; 9% (best-in-class) to 22% AP exceptions (FIE-B-005, FIE-B-009, FIE-B-012..015; several
   vendor-sourced).
5. **Few formats are genuinely needed**: CSV and JSON; BAI2 and/or ISO 20022 camt for bank reporting; the bank's lockbox
   output; IRS pipe-delimited and CSV datasets; OFAC SLS XML/CSV; PDF and images; one custodian feed per custodian.
   X9.100-187, DTCC messages, FIX, corporate-action messages, XBRL and licensed pricing feeds reach a sponsor through its
   bank or custodian and need not be parsed by a DAF platform ([05](05-FILE-FORMAT-INVENTORY.md)).
6. **Many workflows can be eliminated rather than automated** — determination letters (IRS datasets), charity W-9s,
   securities notification PDFs (structured intents), trade confirmations (custodian feeds), signed agreement PDFs
   (in-app acceptance): 14 of 115 ([08](08-STP-OPPORTUNITIES.md)).
7. **AI adds value on unstructured evidence and onboarding, not on structured financial files**; no public accuracy
   benchmark exists for DAF documents (FIE-C-048), so its value is a hypothesis to measure.
8. **Security and storage are commodity problems with clear answers**: native on-upload malware scanning exists on AWS
   and Azure at $0.09–$0.15 per GB, write-once retention with legal hold exists only on object storage, and document
   bytes in PostgreSQL cost about ten times object storage ([13](13-SECURITY-STORAGE-AND-AI-EVIDENCE.md)).
9. **Economics** ([09](09-ECONOMIC-ANALYSIS.md); handling times assumed, model revised after adversarial review):
   under modal assumptions routine ingestion takes about 8% of ~20 bps revenue for a $150k book at 90% routine STP
   (about 6% with prevention), about 23% for a $50k book, and about 19% (pooled) to 45% (standalone) at 1,000 funds.
   If investigations run at 3–5% of records and 135 minutes each, ingestion exceeds the whole fee. The investigation
   rate and its handling time — which nobody publishes — decide viability; prevention moves cost more than raising
   routine STP, and 99% STP has no adjacent-industry precedent.
10. **The main evidence gaps** are measured exception rates and handling minutes, and contract-only bank and custodian
    specifications ([11](11-EVIDENCE-GAPS.md)).
