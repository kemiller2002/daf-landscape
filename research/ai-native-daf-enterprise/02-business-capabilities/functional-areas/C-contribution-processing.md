# C. Contribution processing

**Capabilities:**
- C2.1 Contribution intake
- C2.2 Asset acceptance and valuation
- C2.3 Custody and positions
- C4.1 Ledger
- C4.2 Reconciliation

**Outcomes:** O-01, O-03, O-04, O-05, O-07. **Accountable:** Controller (intake and books); CFO, with the complex-asset specialist and the gift acceptance committee (non-cash acceptance).

## 1 Existing industry operating model

**Non-cash intake has three layers** ([`direction-noncash-gift-infrastructure.md`](../../../mission-2026-11-14/direction-noncash-gift-infrastructure.md) §1):

| Layer | Examples | What it does |
|---|---|---|
| Nonprofit-side intake vendors | The Giving Block, Engiven, Overflow, GivingIQ, FreeWill | Charge the nonprofit 1.5–4% or a subscription |
| Intermediary charities | DonateStock Charitable, FreeWill Impact Fund, Dechomai, Realty Gift Fund | Receive, sell and re-grant |
| Sponsor complex-asset desks | Fidelity Charitable, NPT, Ren's sponsors, Daffy | Accept complex assets into DAFs |

**Complex-asset volume and timing.** Fidelity Charitable received $2.6bn of non-publicly traded assets in 2025 ($2.3bn in 2024; 8% of contributions). It handles about 500 complex contributions a year and averages 65 days from acceptance to liquidity (same file, §1 item 6).

**Dechomai is a hub for complex assets.**
- Dechomai Asset Trust took in $986m (CY2021), $525m (CY2022) and $961m (CY2023).
- National sponsors grant to it (DAFgiving360 $12.3m–$25.5m a year).
- AEF partners with it for illiquid gifts (same file, §1 item 4; industry report §11.43).

**Published complex-asset fees vary widely.**
- No extra fee at Fidelity and Ren.
- NPT charges a cost-based gift processing fee.
- Dechomai charges 1–3%, with a $10k minimum (same file, §1 item 5).

**Crypto is cyclical and concentrated.**
- Fidelity Charitable's crypto inflow fell 88% in 2022 and 54% in 2025.
- Crypto was 99.7% of Endaoment's FY6/24 contributions.
- The Giving Block earnout settled at $10.4m against a $246m maximum ([industry report §11.9](../../../DAF-INDUSTRY-REPORT-2026-11.md); [`queue-batch29-regulation-litigation-crypto.md`](../../../mission-2026-11-14/queue-batch29-regulation-litigation-crypto.md)).
- Ren/RCF has accepted crypto via The Giving Block since 2022, with a $100k minimum.

**Private-foundation money arriving in DAFs.** Core national sponsors received $9.43bn from 2,801 foundations in TY2022–24, about 4% of DAF contributions ([industry report §11.74](../../../DAF-INDUSTRY-REPORT-2026-11.md)).

**Conventional mechanics** [I]:
- Inbound stock transfers are matched to donors by staff using DTC instructions and donor notifications ("orphan" deposits).
- Acknowledgment letters are batch-generated.
- Complex gifts run through a manual desk with legal review.

## 2 Actual required business outcomes

1. Only acceptable assets enter, under a published acceptance policy (O-01).
2. The gift is complete and dated correctly, and the asset is under sponsor control in qualified custody (O-01, O-03).
3. Units are booked at a policy value (O-05).
4. The acknowledgment is correct, including the §170(f)(18) exclusive-legal-control statement, and is delivered (O-01).
5. Non-cash obligations are tracked: Form 8283 donee signature, and Form 8282 if the asset is disposed of within 3 years (O-07).
6. The asset is liquidated or held per policy and liquidity needs (O-04).

## 3 Legal and risk constraints

**Legal** (verify each against the [regulatory map](../../08-governance-and-compliance/regulatory-applicability-map.md)):
- §170(f)(8) and §170(f)(18) acknowledgments. The strict-acknowledgment line in *Keefer* is in [`b50-01-daf-litigation.md`](../../../mission-2026-11-14/b50-01-daf-litigation.md).
- §170(f)(11): the donor obtains a qualified appraisal for non-cash gifts over $5,000, and the sponsor signs the Form 8283 donee acknowledgment.
- Form 8282: disposition within 3 years.
- §4943 excess business holdings, as applied to DAFs by §4943(e).
- OFAC.
- State law for real property: transfer, environmental and title.

**Risk:**
- Assets with liabilities: partnership capital calls, mortgages, environmental contamination.
- UBTI-generating assets.
- Illiquidity.
- Valuation disputes.
- Source-of-funds and sanctions exposure in crypto.
- Self-dealing: a donor contributes private stock and then wants the sponsor to sell it back to an insider. This is §4958/§4967 exposure.

## 4 Proposed AI-native operating model

**Contribution processing becomes an intent-and-settlement matching system with a specialist lane:**

1. **Intent first.** Every expected gift is declared (`ContributionIntentDeclared`) with a unique reference embedded in the transfer instruction:
   - a DTC delivery note;
   - a wire memo;
   - a crypto deposit address per intent;
   - a deed escrow reference.

   This makes most matching deterministic and turns orphan deposits into a residual.
2. **The asset class decides the lane** (D, acceptance policy table):

| Lane | Asset classes | Decision | Specialist review? |
|---|---|---|---|
| **L1 Straight-through** | Cash (ACH, wire, check lockbox); publicly traded securities and mutual funds; listed ETFs | D throughout: settlement match → screen → completed-gift date → valuation at policy price → units → acknowledgment | No |
| **L2 Policy-listed digital assets** | Crypto assets on the policy whitelist, received via a qualified custodian or broker with chain-analytics screening | D, with P chain-risk scoring feeding a D threshold; liquidate on receipt by default | Only on a risk-score breach |
| **L3 Complex** | Private company stock, LP/LLC interests, real estate, restricted or control stock, insurance, collectibles, non-whitelisted crypto | **H**, by the complex-asset specialist (and the gift acceptance committee above threshold), with an AI-prepared dossier | **Indispensable** |

3. **Why specialist review is indispensable in L3.** The decision turns on facts that are unstructured, adversarial or liability-bearing:
   - transfer restrictions and rights of first refusal in operating agreements;
   - capital-call obligations;
   - environmental and title defects;
   - §4943 control percentages across the donor's family and entities;
   - a realistic exit path and the buyer's relationship to the donor (self-dealing risk).

   The AI reads and extracts these into a schema and drafts a memo. **A person accepts or declines.** The assessment in [`ai-governance-failure-modes.md`](../../../mission-2026-11-14/ai-governance-failure-modes.md), lines 122–123, assigns the same split: a deterministic checklist plus AI extraction and memo.
4. **Valuation support.**
   - L1: market-close rule (D).
   - L3: the sponsor books by policy (often at net liquidation proceeds, or at cost until sale [A policy choice]). The donor's qualified appraisal is the donor's obligation. The document extraction agent checks the appraisal's *form* (qualified appraiser declarations, dates, fields required by the 8283 instructions) and flags gaps. It does not opine on value.
5. **Custody integration.** Every asset lands in a custody or escrow account titled to the sponsor (DD-008). The enterprise never takes possession of private keys. The custodian or broker is the authority on positions; the enterprise keeps a mirror (C2.3).
6. **Settlement reconciliation.** Three-way match, continuously, of custodian or bank receipt, intent, and ledger. The orphan-deposit matcher proposes a match for the residual, and the donor or a human confirms.
7. **Exception routing.** Single queue (C5.3), cases typed by lane and reason.

## 5 Eliminated activities

- ACT-010: manual orphan matching. **Transformed**, through intents plus an agent proposing the residual.
- ACT-011: hand-produced acknowledgments. **Automated**, schema-tested.
- ACT-013: Form 8282 tracking by memory. **Automated** from the disposition event.
- ACT-015: year-end surge staffing for routine gifts. **Reduced**; elastic processing.
- ACT-016: liquidate every security by default. **Transformed** into a per-asset policy option.

## 6 New workflows

- **WF-C1 Straight-through public-security gift.** `ContributionIntentDeclared` → `ContributionReceived` (custodian feed) → match → `ScreeningCompleted` → `ContributionSettled` → `NavStruck`-based units → `AcknowledgmentIssued` → optional `TradeInstructed` (liquidate or reallocate).
- **WF-C2 Complex asset.**
  1. Intent with asset descriptor.
  2. The complex-asset dossier agent requests documents and extracts terms.
  3. Deterministic checklist (§4943 test over the relationship graph, transfer restrictions, liabilities present?).
  4. `ExceptionCase` to the specialist; the committee above threshold.
  5. Accept or decline.
  6. Transfer into escrow or custody.
  7. `ContributionSettled` at policy value.
  8. Exit plan.
  9. Disposition triggers `NoncashAssetDisposed` → 8282 obligation.
- **WF-C3 Crypto.** A per-intent deposit address at a qualified custodian → chain-risk score → D threshold → auto-liquidate → settle in cash → acknowledgment describing the asset and units received, not a dollar value for the donor's deduction.
- **WF-C4 Orphan deposit.** `ContributionReceived` unmatched at T+1 → agent proposes candidates → donor confirmation, or a human decision → match or return.
- **WF-C5 Year-end cutoff.** Deterministic completed-gift-date rules per asset type, applied at the moment of settlement evidence. A dashboard shows in-flight intents against the deadline.

## 7 Required data

- Intents with references.
- Custodian, bank and broker receipt feeds.
- The asset master (identifier schemes).
- The acceptance policy table.
- Relationship graph (for §4943 and self-dealing).
- Appraisal documents and extracted fields.
- Valuation method per asset.
- Completed-gift-date rules.
- 8283 and 8282 obligations.
- Chain-analytics results (crypto).

## 8 Required APIs

- `/v1/contribution-intents`
- `/v1/contributions`
- `/v1/positions`
- `/v1/documents` (appraisals, operating agreements)
- `/v1/cases`
- `/v1/ledger`
- `/v1/reconciliation`
- `/v1/decisions` (acceptance records)
- `/v1/events`

Partners and custodians submit receipts through an ingestion adapter that emits `ContributionReceived`.

## 9 Event triggers

- `ContributionIntentDeclared`
- `ContributionReceived`
- `ContributionSettled`
- `AcknowledgmentIssued`
- `NoncashAssetDisposed`
- `ReconciliationBreakDetected`
- `ExceptionCaseOpened` / `ExceptionCaseResolved`
- `SanctionsListUpdated`: re-screen pending intents
- `CustodianUnavailable`: queue intents and show status

## 10 AI agent responsibilities

| Agent | Category | Responsibility | Prohibited |
|---|---|---|---|
| Orphan-deposit matcher | 2 | Propose a match with evidence: amount, CUSIP, timing, sender name similarity | Posting the match |
| Complex-asset dossier agent | 2 | Request and extract documents; draft the acceptance memo with citations to clauses; list open risks | Accepting, valuing or declining |
| Document extraction agent | 2 | Appraisal form-completeness checks; extract 8283 fields | Value opinions |
| Sanctions near-match triage | 2 | Rank near-matches with reasons | Clearing a match |

## 11 Deterministic automation responsibilities

- Matching on reference.
- The acceptance-class decision.
- The completed-gift date.
- L1 valuation.
- Unit issuance.
- Acknowledgment generation, with content tests.
- §4943 aggregation arithmetic.
- 8282 deadline creation.
- Liquidation orders within policy.
- Three-way reconciliation.

## 12 Human oversight requirements

- L3 acceptance and valuation: specialist, with the gift acceptance committee above a threshold [A: e.g. $1m or any real property].
- Officer signature on the Form 8283 donee section.
- Write-off of unmatched deposits.
- Sanctions true match: sanctions officer.
- Acceptance policy changes: CFO and GC, with board approval for new asset classes.

## 13 Exception management

| Case type | Default SLA [A] | Route |
|---|---|---|
| Orphan deposit | 2 business days | Contribution operations |
| L2 risk breach | 1 business day | CRCO |
| L3 acceptance | Clock per asset type, published to donor and advisor | Specialist |
| Acknowledgment generation failure | Same day | Controller |
| Year-end in-flight intent | Escalation at T-5 business days | Controller |

## 14 Security and compliance controls

- Per-intent deposit references prevent misattribution.
- Custody accounts titled to the sponsor.
- No private keys held.
- Acknowledgment template tests in CI include the exclusive-legal-control statement.
- Acceptance decisions are recorded with the policy version.
- Segregation: the person who accepts an L3 asset above threshold cannot also approve its valuation.
- Every L3 acceptance is checked for a relationship between the buyer and the donor at exit.

## 15 Estimated staffing implications

**Drivers:**
- L3 gifts per year and the specialist-hours per gift. Assumption [A]: an L3 gift takes about 15–40 specialist hours depending on type. Fidelity handles about 500 complex contributions a year (evidence above), which bounds the scale of a large national's complex desk.
- The orphan-deposit residual rate.
- Year-end peaks in L3.

**Direction:** L1 and L2 processing staff largely disappear; L3 specialists remain and become the binding constraint, which the digital twin tests. At small scale, L3 is outsourced to an intermediary (Dechomai-type) or a non-cash processor. Numeric FTE is in [`../../09-financial-models/`](../../09-financial-models/).

## 16 Cost and performance model

**Cost drivers:** custodian and transfer fees, crypto broker spreads, chain-analytics fees, appraisal-review time, legal review for L3, and liquidation costs, passed through per policy.

**Design targets [A]:**

| Measure | Target |
|---|---|
| L1 settlement to acknowledgment | Same business day for 99% |
| Orphan residual | Under 1% of L1 receipts |
| L3 decision time | Published per type and measured. Fidelity's 65 days from acceptance to liquidity is a reference point, not a target |

## 17 Implementation dependencies

- Qualified custodian with event or file feeds (area F and the technology architecture).
- Crypto broker or custodian with screening.
- Acceptance policy approved by the board.
- Relationship graph (area B).
- Gift acceptance committee charter.
- Intermediary partner for L3 at small scale.

## 18 Measurable success criteria

1. Straight-through rate for L1 and L2.
2. Orphan residual rate and its aging.
3. Acknowledgment defects. Target: zero, verified by content tests and sampling.
4. L3 cycle time by type, and decline reasons.
5. Number of accepted assets with post-acceptance surprises (liabilities, restrictions). This measures dossier quality.
6. 8282 obligations filed on time: 100%.
