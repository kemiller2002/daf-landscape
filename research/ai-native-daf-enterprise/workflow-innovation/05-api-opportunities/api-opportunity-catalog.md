# API opportunity catalog

**Data:** [`api-opportunities.csv`](api-opportunities.csv) (16 opportunities, AO-01 to AO-16).
**Derived from:** the [innovation register](../02-creative-hypotheses/innovation-register.csv) (INN-01 to INN-38) and the parent [API catalog](../../04-enterprise-apis/api-catalog.md) (API-01 to API-23).
**Status:** design opportunities. Maturity follows the register; no API here is operationally validated (L4).

## 1. Rules used

1. **An API is not a service.** Every opportunity is built as a module inside the modular monolith (DD-009), unless §4 gives a reason to separate it. "Expose as API" describes a *contract*, not a deployment.
2. **Deterministic versus AI.** A capability whose output changes money, legal state or the evidence of a decision is deterministic. AI appears only as drafting or extraction inside a capability, behind schema validation, and never as the decider (DD-002 and DD-005).
3. **The reuse score is shown as its components, never combined.** The components are the number of enterprise functions served (`n_functions`), the sponsors served (single, multi or network) and the volume driver. Use them to compare like with like; there is no single number.
4. **Money never crosses an external API.** The payment gate (AO-09) stays internal and instruction-only. Any design that pools or holds funds for several sponsors is likely money transmission ([regulatory map §14](../../08-governance-and-compliance/regulatory-applicability-map.md)).

## 2. Opportunities ranked by reuse components

| ID | Capability | Functions | Sponsors | Volume driver | Saleable alone | Main regulatory exposure | Priority |
|---|---|---|---|---|---|---|---|
| AO-01 | Recipient verification passport | 5 | multi | recipients × source refreshes | high | Low. OFAC liability stays with each user | P1 |
| AO-04 | Policy evaluation (decide plus back-test) | 5 | multi (policy sets per tenant) | decisions | high | Sponsor keeps decision authority | P1 |
| AO-06 | Evidence ledger and audit package | 4 | multi | control operations | high | Retention; auditor independence | P1 |
| AO-03 | Determination store | 4 | single, then multi | non-routine recipients | medium | Reliance on another party's equivalency determination needs counsel | P1 |
| AO-10 | Delegation tokens | 4 | multi | delegations | low (feature) | Sponsor control | P1 |
| AO-07 | Verified payee registry | 3 | multi (two-sided) | electronic payees | medium-high | **Must never hold funds** | P1 |
| AO-08 | Structured remittance and recipient inbox | 3 | multi | grants paid | medium | Donor privacy choices | P1 |
| AO-12 | Contribution intents with unique references | 3 | single | contributions | low | None | P1 |
| AO-11 | Transfer protocol and history export | 3 | multi (needs counterparties) | transfers and migrations | low direct, high strategic | Transfer is a grant decided by the sending sponsor | P2 |
| AO-13 | Asset underwriting (indicative acceptance) | 3 | multi possible | complex gifts | medium | §4943(e); Forms 8283 and 8282; final acceptance is human | P2 |
| AO-05 | Policy compiler and policy packs | 3 | multi | policy versions | medium | Correlated error across adopters | P2 |
| AO-02 | Cross-sponsor verification network | 2 | network | overlapping recipients | high **if** overlap is real | Shared due-diligence reliance; data-sharing and antitrust | P2 (pending [overlap evidence](../08-experiments/recipient-overlap-evidence.md)) |
| AO-15 | Liquidity forecast | 2 | single | pipeline | none | Fiduciary | P2 |
| AO-14 | Exception case market | 2 | multi | non-routine cases | medium | Decisions stay under each sponsor's delegation | P3 |
| AO-16 | Evidence-graded discovery | 2 | multi | donor sessions | low-medium | Charity-data licensing for AI use | P3 |
| AO-09 | Payment gate and netting | 1 | per instruction | payments | **not to be sold** | Instruction-only | P1 (internal) |

## 3. The strongest independent products

| Product | Buyer | Why they would pay | Named alternatives (repository evidence) | What would make it fail |
|---|---|---|---|---|
| **AO-01 + AO-04 + AO-06 bundle**: "verified decisions with evidence" | Mid-size sponsors and administrators that keep their recordkeeper | Removes per-grant lookups, produces dated evidence, needs no replatforming | Candid Charity Check (data, not decisions); Chariot compliance checks (payments-adjacent); Ren, Foundation Source, TIFIN Give (embedded in their platforms; no public policy-as-code) | Sponsors' vendor contracts block integration (EV-122, GAP-002); measured exception pools are too small to pay (parent 10- §6) |
| **AO-07 + AO-08**: payee registry and recipient inbox | Sponsors, with recipients free; possibly a neutral consortium | Fewer checks and payee hijacks; lower cost for recipients | Chariot (DAFpay network); PayPal Grant Payments; Fidelity's own EFT enrollment; Benevity, Blackbaud and Bonterra on the nonprofit side | Chariot or PayPal network incumbency; recipients will not enroll a second time |
| **AO-02**: verification network | Many sponsors | Each new member reuses others' evidence | No shared ledger in the repository evidence | Low cross-sponsor overlap; liability or antitrust objections; free riding |
| **AO-11**: transfer protocol | Challengers, donors, regulators | Lowers donor switching cost (EV-121) | None | Incumbents decline to adopt. Value accrues to donors, not to a payer |

**Endaoment and Daffy for Developers** sell *sponsor-of-record* APIs (industry report §8), which is a different layer. They are partners or channels for Model D, not competitors to AO-01 to AO-08.

## 4. Do NOT build as a separate service

| Candidate | Reason it stays a module (DD-009) |
|---|---|
| Payment gate (AO-09) | It must sit in the same transaction as grant state and the ledger posting. Separating it creates distributed-transaction failure modes on the money path, the worst place to have them |
| Policy evaluation (AO-04) | It is called synchronously by grants, onboarding, payments and investments. In-process calls keep decisions deterministic and replayable, and it can be *exposed* without being *separated* |
| Ledger and fund accounting | The outbox and the posting must commit atomically with business state |
| Delegation tokens (AO-10) | They are part of the authorization model, and splitting them would duplicate policy enforcement |
| Contribution intents (AO-12), liquidity forecast (AO-15) | Low volume, single consumer |
| Determination store (AO-03) | Its data is joined to recipient and grant state; there is no isolation need |
| Each agent "as a microservice" | Agents already run out of process behind the tool broker. One runtime pool is enough; one service per agent adds nothing |

**Candidates for separate operation, if evidence arrives:**
- **AO-02 (network)** and **AO-07 (registry)** may warrant a *separately governed* deployment run by a neutral operator. The reason would be **trust and governance** (competitors sharing data), not scale.
- **Cell isolation** for a bank or large sponsor is a deployment choice, the same monolith in a separate cell. It is not a new service.

## 5. Events that connect the opportunities

```
CharityEligibilityChanged ─▶ AO-01 passport ─▶ AO-04 decide ─▶ GrantApproved ─▶ AO-09 gate ─▶ PaymentInstructed
SanctionsListUpdated      ─▶ AO-01 rescreen universe          GrantFlagged  ─▶ AO-14 case market
DeterminationExpiring     ─▶ AO-03 ─▶ case                     PaymentSettled ─▶ AO-08 remittance ─▶ recipient inbox
PaymentProfileChanged     ─▶ AO-07 cooling-off                 every decision ─▶ AO-06 evidence ledger
TransferOutRequested      ─▶ AO-04 (eligibility of receiving sponsor) ─▶ AO-11 transfer message + history export
```

## 6. Open questions

- Does cross-sponsor recipient overlap make AO-02 worth a network? This depends on the [overlap evidence](../08-experiments/recipient-overlap-evidence.md).
- Can a sponsor legally rely on evidence another sponsor contributed? This needs counsel. It is the parent API-12 issue.
- Will recipients enroll in yet another registry, or should AO-07 federate with existing rails (Chariot, PayPal) instead?
