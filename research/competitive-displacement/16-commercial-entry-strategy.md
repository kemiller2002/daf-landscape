# 16 - Commercial entry strategy

Status: research recommendation (2026-11-26), **revision 2** after the adversarial review. **A proposal, not a decision**: per the Praxis authority contract (SRC-060) nothing here changes Unbound's ratified decisions; the conflict with OD-M-05 is escalated (DEC-001, XRI-001).

## 1. Is the existing Unbound commercial strategy wrong?

**As an entry strategy, the evidence says yes.** The ratified plan (OD-M-05) enters by displacing incumbents at mid-size national and single-issue sponsors (5k-50k funds) and advisor-distributed sponsors, with administration revenue around 20 bps.

| Evidence | Effect | Reference |
|---|---|---|
| 1 of 26 national/faith iPhi sponsors left Ren in 2023-26 (about 1% a year); advisor channels add rather than replace | The target segment is the **least mobile** | CLM-015, CLM-018, CLM-027 |
| Incumbent revenue is shared with sponsors-of-record and distributors (RCF ~98%; adviser compensation) | Purchase controllers are paid to stay | CLM-017 |
| No observed switch cites technology, price, exit terms or history | Product advantages are not yet purchase triggers | CLM-016 |
| AI-native administration is roughly at parity with a well-automated incumbent; AI is ~6% of the saving | No decisive cost weapon | CLM-011, CLM-013 |
| Full administration needs about $10M at market pay and rarely pays back within ten years | Highest-risk entry | CLM-030 |

The strategy is **not wrong as a destination**: the single ledger, deterministic controls, provenance-bound vetting and reconciliation-gated migration remain sound product choices. What is unsupported is **entering first as a full-service displacing administrator in the least mobile segment**.

## 2. What the adversarial review changed

Revision 1 proposed a standalone non-custodial wedge: a paid migration assessment plus a charity eligibility evidence feed sold to sponsors at contract-end windows. The reviewers showed it cannot stand alone:

- **No platform to move to at G1.** An assessment sizes either a move to a platform that does not exist yet or a move to a competitor whose team will redo the work (CHL-067).
- **No price.** Receiving vendors scope migrations free during the sales cycle, and selection consulting is a few thousand dollars (CHL-068, CHL-095). The assessment is customer-acquisition cost, not revenue.
- **Commodity evidence.** Candid Charity Check starts at $2,750 a year with most of the same public-data content; Treasury Do Not Pay is free for federal agencies (CHL-051).
- **Procurement blocks an undercapitalised vendor.** SOC 2 is expected even without SOC 1; donor PII triggers DPA, WISP and privacy duties; bank buyers review vendor financial condition (CHL-014, CHL-015, CHL-040).
- **Windows are mostly renegotiation leverage, not exits** (CHL-096). Sales cycles of 9-24 months make "two paying customers in 8 months" implausible (CHL-013).
- **The evidence base sampled only movers** (CHL-091).

## 3. Revised alternative: partner-first, licence-before-administration

| Stage | What | Capital (cumulative) | Exit criteria |
|---|---|---|---|
| **G0 Validate (0-6 months)** | Win/loss with **5 switchers and 5 stayers**; price test of licence per account and of services separately; public-data replay harness; auditor/counsel view of re-vetting policy; **channel-partner conversations** (CF-software vendor without deep DAF capability, administrator, bank/trust distributor, multi-custodian data layer); contract-end calendar with confirmed evaluations | $0.15-0.35M | **A named partner in term-sheet talks** with a pilot customer; stayers' answers do not falsify HYP-001; replay change rate ≤ ~6% |
| **G1 Partner pilot (6-24 months)** | Unbound licensed as a **DAF module inside the partner's offering** at one of the partner's re-platforming customers: canonical import and reconciliation (Transitus phase 1), eligibility evidence, DAF ledger. Partner holds the customer relationship, balance-sheet comfort and first-line support. SOC 2 Type 1 then Type 2; DPA/WISP; process-only SLAs with capped liability | $1.0-1.5M | One live pilot sponsor with full per-fund reconciliation; partner commits to a minimum volume |
| **G2 Licensed platform through the channel (24-60 months)** | MD-6/MD-7 licensing to the partner's customers | ~$6.5M P50 total (P90 ~$9M) | ~36k licensed accounts (MD-6 break-even at $81) or partner revenue covering burn |
| **G3 Administration option (60+ months)** | Full administration only if a sponsor asks, behind a signed anchor and design-partner agreement | +$1.35-2.8M incremental (PR #87) | Anchor LOI; counsel opinion; auditor acceptance |

**Kill rule (CHL-022):** no named partner by month 6, or no referenceable live pilot by month 24, pauses the thesis before platform capital beyond Release 1.

## 4. Minimum viable commercial entry point (Q9)

**A partner pilot: Unbound's DAF ledger, reconciliation-gated migration and eligibility evidence licensed as a module inside an established partner's offering, delivered to one of that partner's re-platforming customers.** The partner removes the three blockers an entrant cannot remove alone: distribution, vendor-viability objections and SOC history. Unbound contributes what partners lack and incumbents do not publish: verifiable migration with per-fund reconciliation and replayable eligibility decisions.

The free **exit-readiness assessment** (T0-T1: extraction plan, history-depth check, exit-clause review) remains a pre-sales tool and customer-acquisition cost. It is not a product. The **eligibility evidence** is a component of the module, priced against Candid's $2,750 floor, not a standalone business.

## 5. Entry points considered

| Entry point | Path to broader adoption? | Why |
|---|---|---|
| Charity intelligence | No, alone | Commodity (Candid $2,750; free public data); component only |
| Migration tooling | Only as pre-sales and inside a platform | No standalone buyer; free elsewhere |
| File ingestion / reconciliation | Inside a platform | Prevention value, not a product |
| Compliance evidence | Weak | Buyer budget unclear |
| Advisor integrations | No | Slots held; RIA segment price-compressed |
| **White-label technology through a channel** | **Yes, if a partner exists** | Cheapest self-sustaining mode; least sensitive to productivity assumptions |
| Full DAF administration | Option at G3 | Most capital; least mobile segment |

## 6. Positioning hypotheses (ranked below scope and integration; CHL-090)

The reviewers' point is accepted: from a satisfied buyer's seat none of these creates a decision to switch, and price and exit symmetry are hygiene factors that incumbents concede at renewal (CHL-098). They are tested against "nothing" with stayers in V-1:
1. "Your migration, with full history, a measured freeze and reconciliation proof."
2. "Eligibility decisions you can replay for an auditor."
3. "Your brand and your economics: a licence, not sponsor-of-record capture."

## 7. What would make this recommendation wrong

- Stayers and switchers both say national and advisor-distributed sponsors **would** switch for product reasons (falsifies HYP-001): return to OD-M-05 with confidence.
- No partner engages by month 6: the cheapest self-sustaining route disappears; direct licensing (ER-4, P50 $7.6M) or a pause.
- The partner captures most of the value (40-50% share; acquisition rather than licence; CHL-084): the business becomes a services supplier or an acquisition target.
- Incumbents publish migration commitments and exit symmetry first (HYP-013), or obstruct exports and pre-empt renewals with discounts (CHL-005): full-history migration depends on a contracted incumbent export.
- Final 4966 regulations treat personal investment advisers as donor-advisors (88 FR 77922, pending), reshaping advisor-channel economics (CHL-042).
