# 08 — Straight-through processing opportunities and workflow redesign

Research package: [file ingestion and straight-through processing](README.md) (2026-11-26).

For each workflow in the [inventory](03-DAF-INGESTION-WORKFLOW-INVENTORY.md) the research compared five approaches:
(1) conventional manual processing; (2) conventional automation; (3) AI-enhanced conventional processing;
(4) AI-native redesign; (5) eliminating the workflow through a better upstream integration. The inventory's
`redesign_disposition` records the result (industry-generic, before any product's release scoping):

<!-- BEGIN GENERATED: dispositions -->
| Disposition | Workflows |
|---|---|
| keep | 65 |
| redesign | 25 |
| eliminate-file | 14 |
| challenge | 5 |
| defer | 4 |
| merge | 2 |
<!-- END GENERATED: dispositions -->

## 1. The biggest opportunity is prevention, not processing speed

**Unidentified contributions.** Every sponsor studied receives securities and wires into a pooled sponsor account and
then attributes them to a fund using free text: Fidelity Charitable's FBO line, NPT's "contribution receipt account …
then posted" (FIE-A-001, FIE-A-025, FIE-A-131). Donor information "does not always transmit through the DTC wiring
system" (FIE-A-123), and community-foundation staff still report orphan stock gifts (FIE-A-106). Three documented
responses exist: require notification first (NPT, GKCCF, The Signatry), reject (Fidelity Charitable for wires without
an account number), or hold then sweep to a general fund (NCF) (FIE-A-079).

**Redesign (PROPOSED, FIE-A-135):** a contribution intent captured before the transfer issues a unique reference and
generates the transfer instructions containing it (DTC note, wire memo, check memo, per-intent crypto address). Matching
becomes deterministic on the reference; orphans become the residual. This does not need new industry standards — the
free-text fields already exist; the change is generating their content.

## 2. Replace documents with authoritative sources

| Collected today | Authoritative alternative | Evidence |
|---|---|---|
| Charity IRS determination letters | IRS EO BMF, Pub 78, auto-revocation (monthly, public) | FIE-B-043..045; Chariot uses BMF, Pub 78 and OFAC (FIE-A-097) |
| Charity W-9 for public-charity grants | Not needed for grants; EIN from BMF | Inferred |
| Advisor Form ADV PDFs | SEC IAPD by CRD | Inferred |
| Gift-of-securities notification PDF | Structured contribution intent | FIE-A-024, FIE-A-089 (online forms exist) |
| Charity bank letters | Grant-payment networks with their own verification (Chariot, PayPal Grant Payments) or account validation | FIE-A-096, FIE-A-103 |
| Trade confirmations | Custodian transaction feed | FIE-B-055..057 |
| Signed fund-agreement PDFs | Versioned in-app acceptance | Inferred |

## 3. Request structured information in the first place

Bulk features exist only in community-foundation software and TIFIN-family sponsors (Foundant and NPact grant imports;
BlueGive and Give RIA bulk securities uploads; FIE-A-093, FIE-A-104, FIE-A-109). Fidelity Charitable documents no
multi-client advisor process (FIE-A-022) and none was found at Ren, NPT or DAFgiving360 (FIE-A-055). A published CSV
template and API with validation before submission turns advisor e-mail and paper into structured, pre-validated input.

## 4. Where STP is realistic and where it is not

| Flow | Realistic STP | Basis |
|---|---|---|
| IRS and OFAC dataset refresh | ≈100% (machine) with human adjudication of matches | Public, structured, stable layouts (FIE-B-043..051) |
| Bank-reported electronic receipts (ACH, wire) with a reference | ≥90% auto-match | AR and bank reconciliation vendor ranges 85–95% (FIE-B-012, FIE-B-013, FIE-B-015; vendor-reported, inferred) |
| Securities receipts with a reference | High, but mutual funds and outside custodians are slow (4–6 weeks) | FIE-A-132 |
| Checks through lockbox | Lower: remittance quality varies | FIE-B-023, FIE-A-006 |
| Bulk grant recommendations | As high as interactive grants (same eligibility rules) | Inferred |
| Complex assets, successions, legal documents | ≈0% by design: a human decision is inherent | FIE-A-010, FIE-A-011 (65-day average to liquidity), FIE-A-019 |

Adjacent industries say plan for a permanent tail: after about 25 years of HIPAA mandates, 89% of healthcare
remittances are *electronic* — an adoption rate, not an auto-posting rate (FIE-B-005); AP best-in-class still has 9%
exceptions against 22% for others (FIE-B-009). Planning targets: 75–85% routine STP in a new institution's first
months, 90% after calibration, 95% as a stretch; 99% has no adjacent-industry precedent and is treated as a prevention
scenario in the economic analysis (09), where prevention is modelled with its own cost rather than assumed free.

## 5. AI-native redesign — where it changes the work

AI is valuable where input is unstructured and a human decision follows anyway: assembling complex-asset dossiers,
pre-filling successor and death-certificate cases, classifying correspondence and mail, and proposing mappings when
onboarding an institution or migrating a sponsor. It adds nothing to structured bank, custodian, IRS or OFAC files,
which deterministic parsers handle completely. Evidence for document-AI accuracy on DAF documents does not exist
publicly (FIE-C-048); any claim of AI-driven STP for evidence documents is a hypothesis until measured.
