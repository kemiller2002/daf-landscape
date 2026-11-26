# 07 — Institutional integration research

Research package: [file ingestion and straight-through processing](README.md) (2026-11-26).

## 1. Who the institutions are and what they send

| Institution | What reaches the sponsor | How | Specification access |
|---|---|---|---|
| Sponsor's operating bank | Prior-day and intraday reporting; wire and ACH credit detail; ACH returns and NOCs; lockbox batches and images; paid-check and positive-pay files | Bank SFTP/host-to-host, bank APIs, portal downloads | BAI2 and ISO 20022 are public standards, but each bank's implementation guide, type-code table and lockbox layout is contract-only (FIE-B-030, FIE-B-035) |
| Custodian / investment manager | Positions, transactions, cash, prices, corporate-action outcomes, receipts of donated securities | Daily files via custodian data services and APIs (Schwab Data Delivery, Fidelity Integration Xchange, Pershing NetX360/Wove; FIE-B-055..057) | Contract-only |
| Grant-payment networks | Disbursement status, returns, unclaimed funds, destination changes | REST APIs and webhooks (Chariot Disbursements, FIE-A-096; PayPal Grant Payments, FIE-A-103) | Public developer docs (Chariot) |
| Complex-asset intermediaries | Acceptance, liquidation confirmations, proceeds | Letters and wires (Dechomai for DAFgiving360 and AEF, FIE-A-041, FIE-A-047) | Not public |
| Corporate giving platforms | Payroll deduction and actuals files; matching-gift remittances | SFTP with PGP (Benevity, YourCause; FIE-A-113..117) | Private |
| Predecessor DAF platforms | Accounts, history, documents at migration | One-time services (Ren "Data Migration", FIE-A-050) | Not public |
| Government | IRS EO BMF, Pub 78, auto-revocation, 990-N, 990 XML; OFAC SLS; state registries | Public downloads (FIE-B-043..052) | Public layouts |

## 2. The integration problem is attribution, not transport

Transport is solved: banks and custodians run mature file and API distribution. The persistent problem is linking a
reported movement to the right fund (02 §2, FIE-A-131). Institutions carry a free-text field (FBO line, DTC note, wire
memo, ACH addenda, ISO 20022 remittance information) that the sponsor can populate in advance through its own
instructions. Healthcare solved the equivalent problem — reassociating an EFT with its remittance — with a trace number
carried on both (CAQH CORE, FIE-B-001..007). The DAF analogue is a sponsor-issued reference per expected gift and a grant
ID in outbound payment addenda (FIE-A-130, FIE-A-138).

## 3. Onboarding a new institution without building from scratch

Traditional EDI trading-partner onboarding takes 8–12 weeks per partner, 7–10 days on mapping alone (FIE-B-021,
vendor-sourced). The shared-infrastructure alternative:

1. Receive sample files and documentation; inspect and classify the formats.
2. Match against existing mappings (most banks share BAI2 or camt.053 semantics; custodians do not share formats).
3. Propose mappings (AI-assisted), validate against samples and synthetic edge cases.
4. Approve; run in parallel (shadow) through at least one month-end; reconcile to an independent statement.
5. Activate; monitor for schema drift.

Marginal cost depends on reuse: a second bank speaking the same standard is mostly configuration; each new custodian
is a new mapping because feeds are proprietary. Estimates are in [09](09-ECONOMIC-ANALYSIS.md) (assumed, anchored on
the EDI analogue).

## 4. Where direct APIs should replace files

APIs suit event-shaped, low-latency data: grant-payment status (Chariot), identity and account verification, intraday
balances. Files remain superior for point-in-time institutional sets (prior-day statements, end-of-day positions) where
the file *is* the reconciliation unit, carries control totals and is the system of record for the business date, and
for government snapshots. Custodians offer both in parallel (FIE-B-055..057).
