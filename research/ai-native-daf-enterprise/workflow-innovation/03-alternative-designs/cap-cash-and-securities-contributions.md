# Capability: cash and publicly traded securities contributions

Complex noncash assets are W4 (another file). Cash and securities are treated separately because their failure modes differ.

## Cash (BO-02)

| ID | Type | Mechanism | Maturity |
|---|---|---|---|
| D-CASH-1 | Conventional | Check or wire; staff match the deposit to the donor; letter generated | Observed [I] |
| D-CASH-2 | Automation-first | Lockbox and ACH with auto-matching on name and amount | L1 |
| D-CASH-3 | AI-native | Contribution intent with a unique reference; bank feed event → deterministic match → units → acknowledgment (parent PoC) | L3 (PoC journey) |
| D-CASH-4 | **Radical: pull, not push** | The donor authorizes the sponsor to debit a verified bank account (ACH debit or a pay-by-bank mandate) at the moment of intent. There is no deposit to match, because the sponsor initiated the movement with its own key | L1 |
| D-CASH-5 | Ecosystem | A payment processor handles collection and remits net settlement with itemization | L1 (watch processor fee and money-transmission placement, REG-042/043) |

## Publicly traded securities (BO-03)

| ID | Type | Mechanism | Maturity |
|---|---|---|---|
| D-SEC-1 | Conventional | Donor's broker sends a DTC transfer with a free-text reference; orphan deposits matched manually; liquidate | Observed [I] |
| D-SEC-2 | Automation-first | DTC instructions pre-filled for the donor; auto-matching on reference | L1 |
| D-SEC-3 | AI-native | Transfer intent with a unique reference; custodian event → match → completed-gift date rule (delivery) → valuation at mean of high/low or close per policy → units → acknowledgment | L2 |
| D-SEC-4 | **Radical: broker-initiated gift API** | The advisor's custodian sends a structured gift message (donor, lots, cost basis, account reference) *with* the transfer, so attribution, basis records and acknowledgment data arrive together | L0 (needs custodian cooperation) |
| D-SEC-5 | Ecosystem: per-donor sub-accounts at the sponsor's custodian (INN-23) | Matching by account number | L1 |

**Constraint pass:**
- **Completed-gift date** follows delivery rules, which matters at year-end.
- **Acknowledgment content** must include the exclusive-control statement (REG-008, REG-009).
- **Pull debits** need donor authorization and NACHA rules.

**Perspectives:**
- **Architect:** unique keys everywhere (W11 D-W11-4).
- **Adversarial:** pull debits create a fraud vector through stolen bank accounts, so account ownership must be verified.
- **Economist:** small savings per item, large at scale.

**Experiments:** E4 (orphan-deposit rate under keyed vs unkeyed intake). E9 (crash between settlement and posting).
**Recommendation:** D-CASH-3/4 and D-SEC-3/5; propose D-SEC-4 to custodian partners.
