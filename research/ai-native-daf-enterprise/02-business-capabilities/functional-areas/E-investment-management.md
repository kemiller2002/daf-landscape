# E. Investment management

**Capabilities:** C2.3 Custody and positions, C2.4 Investment policy and execution, C2.5 Liquidity and treasury.
**Outcomes:** O-04, O-03, O-05, O-14.
**Accountable:** Investment Committee (policy). The CIO or outsourced CIO is responsible; the CFO and Treasurer are accountable for liquidity.

## 1 Existing industry operating model

**Investment menus differ widely** ([`direction-investment-menus-performance.md`](../../../mission-2026-11-14/direction-investment-menus-performance.md) §1):

| Sponsor | Menu |
|---|---|
| Fidelity Charitable | About 25 pools plus CIAP (adviser program, $100k minimum); pool expense ratios 0.015–0.93% |
| Vanguard Charitable | 36 options |
| NPT | 7 model portfolios |
| AEF | Adviser-managed only |
| MS GIFT | FA-run, advisory fee ≤ 1.00% |

**Affiliated managers capture the investment expense ratios** at the nationals ([industry report §3](../../../DAF-INDUSTRY-REPORT-2026-11.md)). Vanguard Charitable has 35 of 37 pools in Vanguard funds (§2.1).

**All-in cost is mostly hidden from the 990.** Fidelity's asset-weighted pool expense ratio is 26.3 bps (FY2025). Its all-in floor is about 50–52 bps, with 47% of investments in CIAP accounts whose fund costs are unpublished (industry report §11.12).

**Fidelity's active pools trail benchmarks by about the admin fee over five years** [I] (strategic synthesis §0 A).

**Adviser fees:**
- Only MS GIFT, DAFgiving360 and TIFIN Give publish a 1.00% cap.
- Fidelity CIAP, NPT, AEF and RCF publish no numeric cap.
- RIA brochures charge 0–2.00% (strategic synthesis A11).
- AEF's line 11f implies 0.40–0.46% of assets as fund-borne adviser and manager cost (industry report §11.11).

**All-in cost at $250k** runs from 0.26% (Daffy) to 2.13% (San Francisco Foundation). Pool choice is as large a lever as sponsor choice (strategic synthesis A10).

**AI.** No evidence of AI discretionary investment management in DAF programs (industry report §7).

## 2 Actual required business outcomes

1. Assets invested in line with a board-approved IPS, and charitable value preserved for future grants (O-04).
2. Enough liquidity to pay grants when recommended, including in market stress (O-04, O-06).
3. Donor and advisor choices honored within menu and mandate (O-02).
4. Costs disclosed and reasonable, with adviser fees bounded by policy (O-09, O-14).
5. No excess business holdings, and no jeopardizing exposure beyond policy (O-07).

## 3 Legal and risk constraints

- **Board fiduciary duty** of care and loyalty.
- **State prudent-investor or UPMIFA standards.** Their applicability to DAF assets is debated; see the [regulatory map](../../08-governance-and-compliance/regulatory-applicability-map.md).
- **§4943 as applied to DAFs** (§4943(e)).
- **Pooled funds:** the Philanthropy Protection Act, ICA §3(c)(10) and Securities Act §3(a)(4) exempt charitable pooled income funds from registration under conditions. Verify these in the regulatory map.
- **Advisor-managed programs:**
  - The advisor is a separate fiduciary under the Advisers Act and their own Form ADV.
  - The proposed §4966 regulations (REG-142338-07, still proposed) would treat a donor's personal investment adviser who manages DAF assets as a donor-advisor (industry report §6). That would affect fees and compensation. **Design for both outcomes.**
- **Conflicts:** sponsor-affiliated funds and revenue sharing.

## 4 Proposed AI-native operating model

Three authorities are separated. No component holds two of them.

| Authority | Who holds it | Mechanism |
|---|---|---|
| **Recommendation** (what should the portfolio be?) | Donor or advisor for their account selections; CIO/OCIO for pool construction | `InvestmentRequested`; OCIO proposals to the committee |
| **Fiduciary authorization** (is this permitted?) | Investment Committee sets the IPS, menu, bands, mandates and liquidity parameters (H). Each request is checked against them by the mandate checker (D) | Policy objects `ips@vN`, `menu@vN`, `mandate/{advisor}@vN` |
| **Execution** (place the trade) | Deterministic rebalancer and order router → qualified custodian; external managers within their mandates | `TradeInstructed` with pre-trade check IDs |

**No autonomous discretionary authority (DD-007).**
- AI agents may analyze managers, draft committee materials, explain portfolios to donors and detect drift.
- They never place trades and never change bands.
- The rebalancer is deterministic: band breach → compute trades → pre-trade checks (liquidity floor, concentration, restricted list, §4943 aggregation) → instruct.

**Advisor-managed programs:**
- The advisor submits trades or a model via API.
- The mandate checker validates them *pre-trade*: eligible instruments, concentration, liquidity sleeve, prohibited self-dealing (no investment in donor-affiliated entities without H approval).
- The fee engine enforces a **published adviser-fee cap** [A policy choice; a 1.00% cap matches the three programs that publish one].
- The enterprise does not compete for the advisor's client (DD-010).

**Liquidity:**
- The cash buffer per pool is sized by the liquidity model from:
  - the recommendation pipeline (submitted and approved, not yet paid);
  - historical grant seasonality;
  - stress scenarios, parameters approved by the committee (H).
- In market disruption, pre-approved playbooks allow bounded D actions: draw the buffer, sell the most liquid sleeve first. Anything beyond the playbook goes to CIO and committee (H).

**Transparency:** an all-in cost disclosure per account (admin + fund ER + adviser fee), computed by the fee engine and shown before selection.

## 5 Eliminated activities

| Activity | Disposition |
|---|---|
| ACT-033 Manual rebalancing spreadsheet | Automated, deterministic |
| ACT-034 After-the-fact advisor trade review | Transformed into pre-trade checks |
| ACT-035 Cash forecasting by spreadsheet | Automated from the pipeline |
| ACT-057 Advisor fee reconciliation | Automated |

ACT-032 (committee oversight) and ACT-036 (manager due diligence) are retained and human-accountable, with agent-prepared materials.

## 6 New workflows

- **WF-E1 Donor allocation change.** `InvestmentRequested` → menu validation (D) → `TradeInstructed` (exchange units between pools) → `PositionChanged`.
- **WF-E2 Pool rebalance.** `PositionChanged` / `NavStruck` → `PolicyBandBreached` → rebalancer → pre-trade checks → `TradeInstructed` → custodian → reconciliation.
- **WF-E3 Advisor trade.** Advisor API → mandate check (D) → accept, reject with reason, or case (H) → `TradeInstructed`.
- **WF-E4 Liquidity watch.** Daily, and on `RecommendationSubmitted` surges: forecast → buffer below floor → liquidity raise per playbook (D) or CIO case (H).
- **WF-E5 IPS change.**
  1. OCIO proposal with agent-drafted analysis.
  2. Digital-twin simulation of liquidity and fees.
  3. Committee approval (H).
  4. `PolicyPublished`.
  5. Transition trades.

## 7 Required data

- IPS, menu and mandates (versioned).
- Positions (custodian mirror).
- Prices with sources.
- Benchmarks.
- Pool NAV and units.
- The recommendation pipeline.
- Grant seasonality history.
- The relationship graph (for §4943 and self-dealing).
- Adviser registry and fee terms.
- Restricted list.

## 8 Required APIs

- `/v1/positions`
- `/v1/investment-requests`
- `/v1/policies` (IPS, menu, mandate)
- `/v1/fees` (all-in disclosure)
- `/v1/ledger` (NAV and units)
- `/v1/reports` (performance against benchmark)
- `/v1/events`

Advisor platforms consume `/v1/positions` and submit to `/v1/investment-requests` under scoped privileges.

## 9 Event triggers

`InvestmentRequested`, `TradeInstructed`, `PositionChanged`, `PolicyBandBreached`, `NavStruck`, `RecommendationSubmitted` and `GrantApproved` (liquidity), `CustodianUnavailable` (suspend trading), `PolicyPublished`.

## 10 AI agent responsibilities

| Agent | Category | Responsibility | Prohibited |
|---|---|---|---|
| Manager due-diligence analyst | 2 | Summarize manager documents and performance attribution; draft committee memos | Selecting managers |
| Advisor copilot | 2 | Explain mandate rejections; prepare compliant alternatives for the advisor | Submitting trades |
| Service answer agent | 2 | Explain holdings and costs to donors from authoritative data | Recommending allocations as advice |
| Improvement agent | 2 | Detect cost or tracking anomalies; propose menu changes | Changing policy |

## 11 Deterministic automation responsibilities

- Menu and mandate validation.
- Rebalancing.
- Pre-trade checks.
- Order routing.
- NAV computation.
- Liquidity forecast.
- §4943 aggregation.
- Fee caps.
- All-in cost disclosure.
- Performance reporting against benchmarks.

## 12 Human oversight requirements

- The Investment Committee adopts the IPS, menu, managers, bands and liquidity parameters, and reviews performance.
- CIO or OCIO actions beyond the playbook.
- Approval of advisor mandates: a new advisor firm requires due diligence (H).
- Any investment in a donor-related entity (H; default deny).

## 13 Exception management

| Exception | Route |
|---|---|
| Mandate rejection disputed | Case to the CIO delegate |
| Rebalance blocked by a pre-trade check | Case to the CIO delegate |
| Liquidity below the floor beyond the playbook | CIO, with notice to the committee |
| Custodian outage | Degraded mode; see the scenario in [`../../11-scenarios-and-validation/`](../../11-scenarios-and-validation/) |

## 14 Security and compliance controls

- No software or person can transfer securities out of sponsor custody except to whitelisted destinations under dual control.
- Rebalancer parameters are policy objects that engineers cannot edit.
- Advisor credentials are scoped per account and revocable.
- The fee engine enforces caps.
- Committee decisions are recorded with the evidence pack.

## 15 Estimated staffing implications

**Drivers:**
- number of pools and managers (committee and OCIO workload);
- number of advisor firms (onboarding due diligence);
- mandate exceptions.

**Direction:** investment operations staff are largely removed. The OCIO is contracted; a treasury analyst remains. Numeric FTE is in [`../../09-financial-models/`](../../09-financial-models/).

## 16 Cost and performance model

**Cost drivers:** OCIO fee (bps), fund expense ratios, custodian fees, trading costs, adviser fees (borne by the account).

**Design targets [A]:**

| Measure | Target |
|---|---|
| All-in cost disclosure | 100% of accounts |
| Pre-trade rejection explanations | 100% machine-readable |
| Grants delayed by liquidity | Zero |
| Policy-band breaches outstanding past the tolerance window | Zero |
| Index-based default menu | Keeps donor all-in cost in the lower range observed in the repository (for example Vanguard 0.62% at $250k vs Fidelity 1.15%; strategic synthesis A10). This is a design target, not a promise of returns |

## 17 Implementation dependencies

- Qualified custodian with order and position APIs or files.
- OCIO contract.
- Committee charter.
- IPS.
- Advisor onboarding standard (area I).
- Liquidity model parameters.
- Pricing sources.

## 18 Measurable success criteria

1. Days with any band breach beyond tolerance.
2. Liquidity shortfall incidents.
3. Advisor-fee cap exceptions. Target: zero.
4. All-in cost by account decile.
5. Tracking difference against benchmarks, net of fees.
6. Trade breaks between instruction and custodian.
