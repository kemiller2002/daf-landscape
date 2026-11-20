# Audit, outcome inventory and the ten workflows to reinvent first

## 1. Audit of current research and architecture (2026-11-20)

**What is known**, validated in the repository and summarized in the parent [research inventory](../../00-research-inventory/research-inventory.md):
- **Market structure.** $327.87bn in DAF assets, $64.60bn in grants, $58.41bn net of DAF-to-DAF transfers (EV-001, EV-005, EV-016). Real advisory accounts number about 0.79m, not 3.59m (EV-008).
- **Fees.** Admin fees cluster at 0.60% on the first $500k (EV-066). Community foundations cost 1.7–4.7× more (EV-038).
- **Operating benchmarks, FY2024 Form 990s:**
  - grants per employee range from 117 to 5,670 (EV-135);
  - opex per grant runs from $61 (Fidelity) to $2,487 (SVCF) (EV-136);
  - accounts per employee run from 62.7 (NPT) to 232 (Vanguard).
- **Rails and remittance.**
  - Fidelity distributes 67% of grants by EFT.
  - NPT pays by PayPal or wire.
  - Chariot runs on Column N.A. (EV-031, EV-052).
  - No top-10 sponsor states a grant ID in ACH addenda (EV-086).
- **Exception proxies.**
  - About 4.2% like-for-like non-standard dollars at the four largest nationals (EV-080).
  - A core review-need proxy of 7.76% of lines and 11.61% of dollars across the top 50 (EV-079).
  - About 7–8.5% of grants (EV-081).
  - Revoked-EIN grants are 0.082% of dollars (strategic synthesis §0).
- **Portability.** No published outbound policy; transfers take 10 business days to 4 weeks, liquidated to cash; migrations lose history (EV-121, EV-037).
- **Contracts.** Six of the top 20 sponsors restrict automated access (EV-122).
- **AI.** No sponsor documents AI in approval (EV-089). Agentic donor products move money with no documented limits (EV-088). Inference is cheap (EV-106).
- **Concentration of grant flows.** Recipient Gini is about 0.89, and the top 1,000 recipients receive 49.1–54.3% of dollars (recipient-concentration data, PR #73). Fidelity makes about 12.5 grants per recipient (FINAL-STATUS, PR #73).

**What is designed (parent workstream):**
- outcome model and decision census;
- event catalog;
- policy-as-code decisioning;
- payment gate;
- F# journey with 59 tests;
- cost model;
- twin;
- business-model staging C→D;
- 50 controls;
- 65 regulatory requirements.

**What is assumed.** 23 of 30 cost parameters, notably exception handling minutes, complex-asset hours, contact rates, break rates and CAC.

**What is disputed or unknown:**
- the measured exception and handling-time baseline (GAP-001);
- executed contract data rights (GAP-002);
- the error baseline (GAP-004);
- break cost (GAP-005);
- money-transmission status of a non-custodial operator (GAP-012);
- willingness to pay (GAP-014);
- partner sponsor-of-record terms (GAP-027);
- **whether verification work actually recurs across sponsors.** Nothing in the repository measures cross-sponsor recipient overlap. A harvest of public Schedule I lines was started to measure it ([`../08-experiments/recipient-overlap-evidence.md`](../08-experiments/recipient-overlap-evidence.md)).

**How incumbents appear to operate.** Observed practice, kept separate from marketing and from inference:

| Organization | Verified practice | Marketing claim | Inferred internal process [I] |
|---|---|---|---|
| Fidelity Charitable | FMR provides recordkeeping and administration (EV-023); EFT for 67% of grants; ~2.66m grants CY2024 | "Digital-first" EFT transition | Large affiliate-staffed operations center; manual review of non-standard grants |
| NPT | 286 employees; 129,575 grants FY2024; PayPal or wire, no ACH; Excel donor export (EV-029, EV-031) | — | High-touch servicing for large accounts ($2.35m average) |
| DAFgiving360 (Schwab) | 1.1m grants FY2024; 194 employees, 5,670 grants per employee (EV-032) | — | Affiliate operations; highly standardized grants |
| Vanguard Charitable | 119 employees; 221,825 grants; PayPal Grant Payments; selected Give Interactive (vendor claim) | — | Ledger replatforming in progress |
| Ren / RCF | RCF paid Ren $19.23m in FY2024, 98% of its fundholder fees (EV-044); DFX portals | ">60% of DAF assets" (unsupported; confirmed floor 32.2%, EV-046) | Ren performs administration for RCF programs, not only software |
| TIFIN Give / GiveClear | GiveClear is the sponsor; Chariot disburses (EV-051) | Louise AI executes donor requests (vendor evidence only) | Advisor-led onboarding |
| Chariot | Disbursements on Column N.A.; DAFpay default fee 2.9% to nonprofits (EV-052, EV-053) | — | Payments-first infrastructure |
| Daffy | MCP server exposes `make_donation` (EV-088); $2bn reported (company) | — | Consumer-direct |

## 2. Business outcome inventory

[`outcome-inventory.csv`](outcome-inventory.csv) decomposes the parent model's 18 outcomes into **64 business outcomes**, each with:
- its basis: legal, fiduciary, risk or value;
- its beneficiary;
- the current mechanism;
- the evidence class of that description;
- its top-workflow link.

Some outcomes are **outcomes the industry rarely names** but that the evidence shows matter, for example:
- *recipient can attribute and thank the donor* (EV-086);
- *dormant capital reaches charity* (22% of accounts made no grants in 2020–22, EV-015);
- *history survives a platform or sponsor change* (EV-037).

## 3. The ten workflows to reinvent first

**Selection rule:** rank by available evidence of **cost, complexity, or structural inefficiency**. Structural inefficiency means repeated work, work borne by a party outside the transaction, or friction with no control value. The evidence strength is shown for every row, and nothing is ranked on invented numbers. Where the repository has no cost data, the row says so, and the ranking uses structural evidence only.

| Rank | Workflow | Evidence of cost, complexity or inefficiency | Evidence strength | Why structural, not incidental |
|---|---|---|---|---|
| **W1** | **Recipient verification and eligibility** (per-grant status, sanctions, identity of the legal entity) | Every grant needs it. Opex per grant varies 40× ($61–$2,487, EV-136). Fidelity's ~12.5 grants per recipient imply heavy *within*-sponsor repetition. Each sponsor verifies the same charities independently [I; cross-sponsor overlap under measurement] | Medium (within sponsor); pending (across) | Verification is a property of the *recipient*, but the industry performs it per *transaction* per *sponsor* |
| **W2** | **Non-routine grant review** (foreign, expenditure responsibility, fiscal sponsors, new organizations, benefit cases) | 4.2% like-for-like dollars at the largest nationals (EV-080); core proxy 7.76% of lines and 11.61% of dollars (EV-079). The only grant class needing legal judgment; foreign is 1.46% of dollars (NPT 4.84%) | Medium-High on volume; none on minutes (GAP-001) | Determinations (equivalency, a fiscal sponsor's charitable status) are reusable, but are redone per grant and per sponsor |
| **W3** | **Disbursement, remittance and recipient-side reconciliation** | Four rail camps; Fidelity's non-EFT share is 33%; no grant ID in addenda at any readable top-10 sponsor (EV-086); processor complaints concentrate on payout rules (strategic synthesis §0 G4); DAFpay default 2.9% fee to nonprofits (EV-053) | Medium-High | Cost lands on the nonprofit, which is neither the payer nor the legal party (industry report §3: "weak nonprofit leverage", structural) |
| **W4** | **Complex noncash contribution acceptance and liquidation** | Specialist, slow, outsourced to non-cash vendors (b40n14-03). Form 8283, 8282 and appraisal rules apply. Twin: one specialist is a concentration risk | Medium (complexity); none on volume | Bespoke diligence per asset; little reuse; legal paperwork |
| **W5** | **Donor and advisor servicing (status, how-to, documents)** | No top-20 sponsor publishes a response-time promise (EV, direction-sponsor-accessibility-service); complaints cluster on payout and timing rules (EV, gap19-complaints) | Low-Medium | Status inquiries exist because state is not shared |
| **W6** | **Sponsor-to-sponsor transfers and portability** | 10 business days to 4 weeks; liquidation to cash; no history; no published outbound policy (EV-121); DAF-to-DAF flows of $8.03bn netted FY2024 | Medium-High | Incumbent incentives (asset-based fees) oppose easy exit |
| **W7** | **Advisor-channel integration** (onboarding through advisors, delegated authority, data feeds) | Six of the top 20 restrict automated access (EV-122); public templates allow batch export only; distribution is channel-led [I] | Medium | Each sponsor–advisor pair is a bespoke integration; credential sharing is banned, so advisors re-key |
| **W8** | **System-of-record migration** (platform change) | AEF kept 2 years of history (EV-037); iPhi lost 6 of 57 sponsors; six of six DAF-tech exits went to consolidators (EV-119) | Medium | No standard record format; migration is a one-off project every time |
| **W9** | **Dormant capital and inactivity** | 22% of accounts made no grants in 2020–22; median three-year account payout 9% (EV-015); median sponsor payout 12.7% (EV-014) | Medium-High on the outcome; mechanism unknown | The industry's revenue is asset-based (incentive documented; effect unsupported) |
| **W10** | **Compliance evidence, audit, 990/Schedule D and state registration** | Annual reconstruction for auditors and filings; state registration complexity (b50-02); no sponsor publishes operating metrics (EV-076) | Low-Medium (no cost data) | Evidence is assembled after the fact instead of produced by operation |
| W11 (watch) | Reconciliation and close | No public data (GAP-005) | Low | Inferred from batch-file custody integration |
| W12 (watch) | Donor onboarding | Forms; identity; agreements. The repository has no abandonment data | Low | — |

**Selection result:** W1–W10 receive the full five-plus-design treatment, the seven-perspective competition and adversarial review. W11 and W12 and the remaining capabilities receive at least the five designs ([`../03-alternative-designs/`](../03-alternative-designs/)).
