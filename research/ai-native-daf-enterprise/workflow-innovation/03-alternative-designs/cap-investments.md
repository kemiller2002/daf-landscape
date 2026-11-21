# Capability: investments and liquidity

**Outcome (BO-14–BO-17):** assets are invested per the investment policy statement, advisor mandates are respected, liquidity covers outflows, and excess business holdings are avoided.

**Evidence:**
- Fidelity's asset-allocation pools trail benchmarks by roughly its admin fee (EV-072).
- 35 of 37 Vanguard Charitable pools are Vanguard funds (industry report §2.1).
- Twin: a 30-day custodian outage in surge exhausts a 2% buffer.

| ID | Type | Mechanism | Maturity |
|---|---|---|---|
| D-INV-1 | Conventional | Affiliated pool menu; committee reviews; manual rebalancing; judgmental cash | Observed |
| D-INV-2 | Automation-first | Automated rebalancing and compliance monitoring | L1 |
| D-INV-3 | AI-native | Deterministic band rebalancer and pre-trade mandate checks; pipeline-based liquidity forecast with a seasonal buffer (INN-27); agent drafts committee analysis; committee decides | L2 (twin) |
| D-INV-4 | **Radical: no proprietary menu. Index-only default plus advisor mandates** | The sponsor offers one low-cost index allocation per risk band and otherwise only advisor-managed mandates through the API; no affiliated-fund revenue. This removes the conflict that the evidence shows and shrinks committee work to policy and mandate oversight | L1 |
| D-INV-5 | Ecosystem: outsourced CIO plus custodian model portfolios | The committee selects the OCIO and supervises; execution is fully external | L1 |

**Constraint pass:**
- **Fiduciary duty:** the committee decides policy and managers (DD-007). There is no autonomous discretionary authority.
- **§4943(e)** for gifts of private business interests (REG-006).
- **§4944 does not apply to DAFs** (REG-007), but prudence norms do; UPMIFA applicability is uncertain (REG-057).
- **D-INV-4** survives every constraint. It fails only on the economic incentives of sponsors with affiliated managers.

**Perspectives:**
- **Economist:** D-INV-4 removes fee layering, the largest donor cost layer in adviser programs.
- **Commercial:** it is a differentiator against affiliated nationals.
- **Adversarial:** an index-only default is still market risk. The liquidity model must handle crashes.
- **Customer advocate:** simplicity.

**Recommendation:** D-INV-3 plus D-INV-4 for a new sponsor, and D-INV-3 inside Model C (the client sponsor keeps its menu).
