# W3: Disbursement, remittance and recipient-side reconciliation

**Outcomes:**
- BO-30: funds arrive at the right account.
- BO-31: the recipient can identify and attribute the grant.
- BO-32: the recipient can thank the donor, per the donor's choice.
- BO-33: uncashed checks are resolved.
- BO-39: payee hijack is prevented.

**Evidence:**
- There are four rail camps (industry report §2.5).
- Fidelity pays 67% of grants by EFT, so 33% go otherwise.
- NPT pays by PayPal or wire, not ACH (EV-031).
- Chariot runs on Column N.A. (EV-052); DAFpay's default fee to nonprofits is 2.9% (EV-053).
- No readable top-10 sponsor states a grant ID in ACH addenda (EV-086).
- Processor complaints concern payout rules, check thresholds and lost checks (g1913-processor-disbursement-rules.md; gap19-complaints-with-denominators.md).
- **The cost falls largely on the nonprofit**, which is neither payer nor legal party (industry report §3).

## 1. First principles

| Element | Necessary content |
|---|---|
| **Information** | A verified endpoint for the recipient's legal entity; the grant identity and the donor-chosen recognition data; the amount |
| **Authority** | The sponsor releases funds only for an approved grant (parent payment gate); a person handles payee-change exceptions above risk thresholds |
| **Resources** | Bank or rail access from **sponsor-titled accounts** (instruction-only, DD-008) |
| **Actions** | Choose the rail; instruct; carry a shared key with the money; confirm settlement; handle returns; tell the recipient what it received and why |

**Not necessary:** paper, one payment per grant, separate letters, or each sponsor maintaining its own copy of each recipient's bank details.

## 2. Inversion findings

| Prompt | Finding |
|---|---|
| Eliminate? | Check runs and grant letters can be eliminated for enrolled recipients; their function is replaced by electronic payment with structured remittance |
| What if the recipient pulled rather than the sponsor pushed? | Recipient-pull (INN-10) removes sponsor-side payee maintenance, but adds an unclaimed backlog |
| External partner? | Rails and payee directories are already external; the risk is concentration (Chariot on one bank) |
| Begin before the request? | Recipient enrollment and verification can happen once, before any grant |

## 3. Designs

| # | Design | Mechanism | Who decides | When | Authoritative data | Human roles | Controls | Cost drivers | Experience (donor / advisor / nonprofit) | Maturity | INN |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D1 | **Conventional baseline** | Weekly or monthly batches; EFT where enrolled, checks otherwise; cover letters by mail or email; remittance out of band | Sponsor ops | Batched after approval | Sponsor's payee file | Payments staff; check printing; reissues | Positive pay; callbacks (inferred) | Per-check cost; reissues; escheat | Donor: "paid" days later. Nonprofit: matches letters to deposits by hand | Observed | — |
| D2 | **Automation-first** | Daily electronic batches; email remittance; automated check reissue | Sponsor ops | Daily | Sponsor's payee file | Fewer staff | Same | Lower | Faster; same reconciliation burden | L1 | — |
| D3 | **AI-native (parent design)** | Event-driven payment per approved grant through the internal payment gate; grant ID in CCD+/CTX addenda; donor-choice data in remittance; settlement and returns as events | Payment gate (rule); person for gate exceptions | Seconds after approval | Payment profile with verification and cooling-off | Payments specialist for exceptions | Gate (tested): verification, cooling-off, caps, dual control, idempotency | Per-payment fee; exception minutes | Real-time status; nonprofit gets a machine-readable key | L3 (parent PoC) | INN-08 |
| D4 | **Radical: recipient-owned endpoint, netted, recipient-pulled** | Three mechanism changes: (a) the **recipient owns** its payment profile in a registry and every sponsor pays to that endpoint, so changes are made once, with cooling-off and out-of-band verification; (b) all approved grants to a recipient in a day are **netted** into one payment with itemized remittance; (c) recipients not enrolled see grants in an inbox and **claim** them to a verified account instead of receiving checks | Sponsor gate releases; recipient owns endpoint facts | Enrollment before grants; daily net settlement | Recipient registry for the endpoint; sponsor for the decision | Payments ops for disputes and unclaimed grants | Registry change controls; netting itemization; unclaimed-aging → escheat path | Registry operation; far fewer payments | Nonprofit: one deposit per day with every grant itemized; donor: same status | L1 | INN-07, INN-09, INN-10 |
| D5 | **Externalized / ecosystem: multi-rail orchestration over partner networks** | Sponsor (or Model C operator) instructs through several rails (bank ACH, PayPal Grant Payments, Chariot Disbursements) chosen per recipient enrollment and cost; no funds held by the operator | Sponsor gate | Seconds after approval | Partner rail enrollment plus sponsor gate | Vendor management | Rail diversity mitigates concentration (industry report §2.7) | Partner fees; may push fees to nonprofits (DAFpay 2.9% default) | Depends on partner; risk of fees borne by nonprofits | L1 | — |
| D6 | **Recipient inbox API (extra)** | A neutral, recipient-side API aggregates grant notices and remittance from all sponsors, with donor-choice data | Each sponsor publishes; recipient reads | Event-driven | Each sponsor's grant events | None routine | Privacy filters per donor choice | Operator cost | Nonprofit: one integration for all DAF grants | L0 | INN-38 |

**Why D4 differs from D3:**
- the authoritative endpoint data moves from the sponsor to the recipient;
- the unit of payment moves from grant to recipient-day;
- for unenrolled recipients the push becomes a pull.

## 4. Constraint ledger

| Constraint | Dies | Modified | Survives |
|---|---|---|---|
| **Legal** (no rule requires checks; NACHA; escheat; money transmission if an intermediary holds funds; grant completion) | A registry or inbox that *holds* funds (D4c, D6) | D4c: unclaimed grants stay in the sponsor's account until claimed; the escheat clock applies to uncashed or unclaimed items per state law (state-escheat data); D5: operator never holds funds | D2, D3, D4 (modified), D5, D6 (notice-only) |
| **Fiduciary** | — | Netting must not delay payment beyond policy | All |
| **Accounting** | — | Netting requires itemized remittance and per-grant settlement mapping (one payment, many grant IDs) | D4 modified |
| **Privacy / security** | — | Remittance honors anonymity; the registry is a high-value target, so it needs strong change controls | D4, D6 modified |
| **Economic** | D1 at scale | D5: partner fees must not shift to nonprofits silently | D3, D4, D5 |
| **Operational** | — | A netted payment return affects many grants, so per-grant re-routing is needed | D4 modified |
| **Human acceptance** | — | Small recipients and congregations may not enroll (b4026-06: none of 14 congregation giving pages showed a DAF option), so a check or claim path is kept | D4 with fallback |

## 5. Analogies

- T1: payee directories.
- T8: consolidation.
- T11: standard remittance messaging.
- T15: claim-your-listing.

## 6. Creative competition

| Perspective | Position |
|---|---|
| **Inventor** | Eliminate *sponsor-side* payee data entirely: the recipient's verified profile is the only copy, signed by the recipient's officer |
| **Enterprise architect** | D3 already carries the grant ID. D4 netting needs a payment-to-many-grants mapping in the ledger (one `PaymentInstruction`, n grants) and per-grant return handling |
| **Economist** | Payments scale with grants in D3 and with recipient-days in D4. At about 12.5 grants per recipient per year, netting saves most where recipients get several grants a day (December). The saving is per-payment fees plus recipient reconciliation time, which is unmeasured on both sides |
| **Regulatory specialist** | Funds must stay in sponsor-titled accounts; a registry is data only. Escheat applies to unclaimed grants and needs state-by-state handling |
| **Adversarial reviewer** | Netting increases blast radius: one hijacked endpoint drains many grants. A registry is a single target for every sponsor. Recipient-pull invites phishing ("claim your grant") |
| **Customer advocate** | Nonprofits gain most from D4 and D6; donors notice little; advisors not at all. Small recipients must not be penalized by fees (D5) |
| **Commercial strategist** | D6 and the registry could be network businesses, but Chariot (DAFpay) and PayPal already occupy the nonprofit side; enter through sponsor-side orchestration (D5) with D3's remittance standard |

**Disagreements:**
- *Adversarial vs Economist* on netting: is the blast-radius risk worth the payment savings? Proposed resolution: net only for recipients with stable, long-verified profiles, capped per day.
- *Inventor vs Regulatory* on recipient-owned data: the sponsor must still be able to show the payee was verified; the recipient-signed profile plus sponsor-side verification evidence satisfies both. Agreed in principle.

**Unresolved:** recipient enrollment rates; bank handling of addenda; recipient-side reconciliation cost.

## 7. Forwarded to experiments

| Candidate | Experiment | Metric |
|---|---|---|
| D3 vs D4 netting vs D1 | **E3** synthetic payments calibrated to grant concentration | Payments per year; payment cost; recipient line-items per deposit; blast radius of one hijack; return handling |
| Crash safety of D3 and D4 | **E9** crash and replay injection | Double payments (must be 0); lost grants (must be 0) |
| Cost | **E11** | |
