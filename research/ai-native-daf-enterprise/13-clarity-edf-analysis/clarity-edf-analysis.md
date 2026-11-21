# Clarity and EDF analysis of the AI-native DAF enterprise

**Method:** applied as pinned in [`clarity-edf-application-guide.md`](../../mission-2026-11-14/clarity-edf-application-guide.md) (Clarity at commit `8cd4801`, EDF v0.3 at `41fea6f`).

- **EDF** is used only on *observed* industry outcomes (§2).
- **Clarity alone** governs hypotheses, meaning the brief's assumptions and the workstream's own design assumptions (§1), and the prospective failure modes of a design that does not yet exist (§3).

**Claim states:** internal-demonstration, suggestive, unsupported, contradicted.
**Confidence:** Low → High, qualitative and not a probability.
**Decision posture:** impact × correctability gives Fast, Experimental, Guardrail or Strategic.
**Evidence IDs:** EV-nnn refer to [`../00-research-inventory/evidence-register.csv`](../00-research-inventory/evidence-register.csv), and CTL-nnn to [`../08-governance-and-compliance/controls.csv`](../08-governance-and-compliance/controls.csv).

**Data files:**
- [`assumption-challenges.csv`](assumption-challenges.csv): AC-01 to AC-19, with the full columns.
- [`failure-modes.csv`](failure-modes.csv): FM-01 to FM-25.

## 0. Admissibility screen applied to this workstream

Before we analyze anything, the screen from the Clarity Constitution is applied to our own outputs:

| Screen | Where this workstream is exposed | Treatment |
|---|---|---|
| False precision / tidy-but-unearned model | 09 cost ratios ("2.9× below frontier"); FTE counts to the person; twin "34 days over SLA" | 23 of 30 parameters are assumed. Every such figure is labeled **[S]** and is internal-demonstration at most. Ratios are reported as order-of-magnitude in the executive report (see §4) |
| Prescription without a signal | The Model C → D staging | Kept as a *conditional* sequence with falsifiers, not a recommendation to commit capital |
| Unbounded claims | "conventions carry no risk value"; "humans own judgment" | Bounded in AC-14 and AC-02 |
| Motivation substituted for incentives | "advisors will like APIs" | Re-expressed as incentives in AC-08 and AC-17 |
| Premature synthesis | Market scoring (10-) produced before the economics existed | The 10- matrix is revisited in §4 against 09 outputs |
| Hero narrative | "AI-native beats incumbents" | Rejected. The defensible claim is narrower (§4) |

## 1. Assumption challenges (Clarity)

Summary of [`assumption-challenges.csv`](assumption-challenges.csv):

| ID | Assumption | Claim state | Confidence | Posture | Falsifier (short) |
|---|---|---|---|---|---|
| AC-01 | More automation → better operations | contradicted (as unbounded) | Medium-High | Guardrail | Automated process with independent QA shows a higher escaped-error rate than the manual baseline |
| AC-02 | AI should replace every human activity | contradicted | High | Strategic | Regulator accepts model-made sponsor decisions |
| AC-03 | All grant decisions can be automated | contradicted (most can; all cannot) | Medium-High | Strategic | Shadow replay cannot reproduce ≥95% of routine approvals |
| AC-04 | One platform must own every financial function | contradicted | Medium-High | Strategic | Partnered custody and rails are materially worse in pilot |
| AC-05 | Lower headcount always means lower risk | contradicted | High | Guardrail | 24 months of incident data show no rise in undetected-error duration |
| AC-06 | Every existing compliance step is legally required | contradicted | Medium-High | Experimental | Counsel reclassifies a "convention" as law |
| AC-07 | Donors primarily value speed | unsupported | Low-Medium | Experimental | Conjoint or pilot data show speed dominates |
| AC-08 | Advisors will accept reduced control | contradicted | Medium | Strategic | Placement unaffected by loss of the investment role |
| AC-09 | A new sponsor is preferable to infrastructure | unsupported | Medium | Strategic | A sponsor-of-record partnership fails *and* an owned sponsor outgrows the calibrated path |
| AC-10 | DD-004 deterministic routine approval is safe | suggestive | Medium | Guardrail | Monthly QA sample of deterministic approvals exceeds tolerance |
| AC-11 | DD-006 event sourcing pays off | internal-demonstration | Low-Medium | Experimental | Versioning cost exceeds audit and export savings |
| AC-12 | ~8% exception rate; determinations reusable | suggestive | Low-Medium | Experimental | Measured rate outside 3–15% or reuse <1.5 |
| AC-13 | Inference cost is immaterial | suggestive | Medium-High | Fast | AI run cost >5% of staff cost per outcome |
| AC-14 | Conventions carry no hidden risk value | unsupported | Medium | Guardrail | Each candidate's detective role is reproduced or shown idle |
| AC-15 | The year-end surge sizes the organization | internal-demonstration (simulated) | Low-Medium | Experimental | Partner December peak <1.5× average |
| AC-16 | Model C buyers exist at ~$300 per account | unsupported | Low | Experimental | No ≥20k-account sponsor signs a paid design partnership in 12 months |
| AC-17 | Advisors prefer embedded APIs | unsupported | Low-Medium | Experimental | ≥3 wealth firms choose white-label portals instead |
| AC-18 | Absent tools prevent agent state changes | internal-demonstration | Medium | Guardrail | Reviewer override rate on agent dossiers <2% (complacency) |
| AC-19 | Smallest organization ~21 FTE at 1k, ~104 at 100k | internal-demonstration (scenario) | Low | Experimental | Measured handling times differ >2× from assumed |

### 1.1 Notes on the hardest cases

**AC-03 / AC-10: routine approval.** This mechanism *is* sound. The statutory exception for listed public charities (§4966(c)(1)) makes the routine class decidable from IRS data. Grants to revoked EINs are 0.082% of top-50 dollars (EV-082). RCF's own policy finds Charity Check adequate for more than 98% of historical grants (EV-045). Three competing risks are not addressed by grant review at all:
- **Fraud presenting as routine grants** (FM-12). This is a *payment-integrity* problem, and the payment gate, cooling-off and caps own it. Grant review does not.
- **Reputational discretion** (EV-097). This is a board-policy problem, encoded as holds (CTL-045).
- **Regulatory reinterpretation** (FM-10). This is low under current case law (EV-096), but final guidance is pending (EV-091).

The posture is therefore **Guardrail**. The design must include the monthly QA sample of deterministic approvals: the Area D falsifier for DD-004. Without it, the claim cannot be falsified, and the design should not be operated.

**AC-14: conventions with possible hidden risk value.** The activity census retired every convention. Clarity requires asking what each convention *also* did. Candidates and their replacements:

| Convention | Possible undocumented function | Replacement in design | Gap? |
|---|---|---|---|
| Two-person review of routine grants | Second pair of eyes on account-takeover patterns | Behavioral anomaly rules + new-recipient/new-device step-up (CTL-033) + caps (CTL-029) | Partial: no human sees routine flow. Add sampled human review of anomalous-but-unflagged clusters |
| Paper checks | Slows fast fraud; physical address check | Payee verification + cooling-off (CTL-004) | Covered for bank changes; not for first-time payees with fresh accounts |
| Month-end close as a project | Forced periodic human scrutiny of balances | Continuous reconciliation (CTL-015/016) | **Gap:** add a monthly controller attestation with variance review, so humans still look |
| Phone callback on charity bank changes | Out-of-band verification | CTL-004 out-of-band verification | Covered (EV-128 shows incumbents rarely publish this) |
| Welcome letter by mail | Out-of-band confirmation of donor address and identity | Notice via prior channel on changes | Minor |
| Wholesaler visits | Relationship trust signal for advisors | Partnerships team (C1.3) | Commercial, not risk |

**Result:** AC-14 is *unsupported as stated*. Two design additions are recommended:
- a monthly controller variance attestation;
- sampled human review of unflagged anomaly clusters.

**AC-09: new sponsor vs infrastructure.** The 09 model shows how this is decided. On steady-state margins, B wins: about 85% at 100k accounts [S]. On a calibrated acquisition ramp, B needs about twice C's peak capital ($12.8m vs $6.4m [S]) and is still negative at year 5. The decisive variable is asset-acquisition speed, which no repository source measures for an AI-native entrant. Claim state **unsupported**; posture **Strategic**, because the choice is costly and slow to reverse.

## 2. EDF on observed industry outcomes

Each analysis follows EDF v0.3: context → outcome → manifestations → origin network → propagation → evidence → control points (ranked) → sufficiency → next action.

### 2.1 Outcome: no sponsor documents AI in grant approval or eligibility determination (2026)

- **System context:** sponsor-side grant decisioning at the top 20 sponsors and their vendors.
- **Outcome (factual):** first-party reading of 13 of 20 entities found none documenting AI in approval, eligibility or money movement (EV-102). AI appears in 29.1% of vendor job postings against 13.3% of sponsor postings (EV-103).
- **Manifestations:**
  - The agentic products are donor-side (EV-088, EV-089).
  - Sponsors publish policy latencies, not AI claims (EV-077).
- **Origin network:**

  | Type | Origin |
  |---|---|
  | Regulatory | Personal manager liability (EV-090); pending guidance (EV-091) |
  | Organizational | Approval sits in compliance teams with low AI hiring |
  | Financial | Thin process value pool: $445k calibrated at a large national [S] (EV-107) |
  | Informational | No measured exception or QA data to justify change (EV-076) |
  | Environmental | Donor unease: 39.8% uneasy about data use (EV-114) |

- **Propagation:** organizational and financial. Vendors build donor-side features that monetize, and sponsors keep approval human.
- **Evidence:** this is an absence finding, a direct observation of public pages only. Internal use is unobserved.
- **Control points, ranked:**

  | Rank | Control point | Influence | Controllability |
  |---|---|---|---|
  | 1 | Measured QA and exception evidence | High | Medium |
  | 2 | Explicit flag-only governance that removes liability fear | Medium | High |
  | 3 | Cheaper shared infrastructure so the value pool clears at network scale | Medium | Low for any single sponsor |

- **Sufficiency:** enough to act. The next responsible action is a shadow-mode study at a design partner (GAP-034).
- **Design response:** DD-002 and DD-005 (flag-only), policy-as-code (DD-011), and Model C's network-scale economics.

### 2.2 Outcome: paper checks remain a material grant rail

- **Context:** grant disbursement at national and community sponsors.
- **Outcome:**
  - Fidelity reports 67% of grants via EFT, so about a third are not (EV-085).
  - NPT pays by PayPal or wire, not ACH (EV-031).
  - Community foundations are mixed (EV-065).
- **Manifestations:**
  - Lost or uncashed-check complaints (EV-125).
  - Nonprofit cost of $5–8 per $1,000 by check against $1–2 on EFT (EV-074).
  - Escheat handling.
- **Origin network:**

  | Type | Origin |
  |---|---|
  | Organizational | Nonprofit board policies prohibiting EFT, which Fidelity asks them to change (industry report A7) |
  | Informational | No verified recipient bank-account registry shared across sponsors |
  | Technical | Fragmented rails (EV-064) |
  | Financial | Sponsor bears little of the recipient-side cost (incentive classification "weak nonprofit leverage") |
  | Regulatory | None: no rule requires checks |

- **Classification:** historical habit amplified by informational gaps, i.e. **mixed, leaning habit** (consistent with the industry report).
- **Control points, ranked:**
  1. A verified payee-profile registry, enrolled once per recipient.
  2. Electronic-by-default policy with a check exception.
  3. Grant ID in the remittance, to remove the reason recipients ask for paper.
- **Next action:** pilot recipient enrollment with a design partner.
- **Design response:** O-15, DD-018, CTL-043, and the payment profile entity.

### 2.3 Outcome: platform migrations lose donor history

- **Context:** sponsor recordkeeping vendor changes.
- **Outcome:** AEF's migration to Ren left two years of directly accessible history (EV-037). No sponsor commits to moving grant history on transfer (EV-121).
- **Manifestations:** donors keep their own records; transfers are cash-only; DAF-to-DAF flows of $8.03bn are netted (EV-016).
- **Origin network:**

  | Type | Origin |
  |---|---|
  | Technical | CRUD schemas tied to the vendor |
  | Contractual / financial | Vendor templates allow batch export only, e.g. iPhi's 15-day window (EV-123) |
  | Organizational | Migration cost borne by the sponsor, and history is not a priced deliverable |
  | Informational | No open grant-record standard (EV-130) |

- **Control points, ranked:**
  1. Contracted data-portability clauses.
  2. An open record format (the draft standard EV-129).
  3. An event-sourced ledger that makes full export routine.
- **Sufficiency:** adequate.
- **Design response:** DD-006, CTL-035 (quarterly exit-readiness export), and the projection to `standards/daf-grant-record`.

### 2.4 Outcome: nonprofits receive thin, out-of-band remittance and donor data

- **Outcome:**
  - No readable top-10 sponsor states a grant ID in ACH addenda (EV-086).
  - Full donor contact is the documented default for only 33.2% of top-20 assets (EV-124).
  - Purpose text is 98.2% boilerplate (EV-087).
- **Origin network:**

  | Type | Origin |
  |---|---|
  | Technical | ACH addenda unused |
  | Organizational | Privacy-by-default choices |
  | Financial | Nonprofit is not the payer |
  | Regulatory | Donor anonymity rights (legitimate, so this is not a defect to remove) |

- **Control points:**
  1. Machine-readable remittance with grant ID (controllable by the sponsor).
  2. Donor-choice prompts at recommendation time (controllable).
  3. Recipient-side reconciliation APIs.
- **Design response:** CTL-043; the `Recognition` field; remittance in the PoC (`GrantIdInRemittance`, tested).

### 2.5 Outcome: challengers repriced upmarket

- **Outcome:** Charityvest moved from "zero fees" to 0.60% on the first $500k, and Daffy added a $40 tier (strategic synthesis A10). All-in cost at $250k still runs from 0.26% (Daffy) to 2.13% (EV-067).
- **Origin network:**

  | Type | Origin |
  |---|---|
  | Financial | Fixed accountability and servicing floor; small-balance accounts cannot cover it, matching the 09 finding that 1k-account operations lose money |
  | Environmental | Incumbents removed minimums (2020) |
  | Organizational | Venture or PE funding with growth targets (EV-056) |

- **Propagation:** competitive. Price convergence from both sides.
- **Control points:** cost-to-serve per account (the only durable lever); the balance mix.
- **Design implication:** the AI-native design does not escape the fixed floor at small scale. It lowers the *variable* cost per account. This supports targeting larger books or selling infrastructure, not a cheap mass-market sponsor.

## 3. Prospective failure modes of the proposed enterprise (Clarity-governed)

These are *design hypotheses about failure*, not observed outcomes, so EDF diagnosis does not apply. The structure borrows EDF's origin and control-point vocabulary under Clarity governance. Full table: [`failure-modes.csv`](failure-modes.csv) (25 modes).

**Highest residual risk:**

| ID | Failure mode | Why it ranks high | Key controls |
|---|---|---|---|
| FM-15 | Cost model wrong by 3× on exception minutes | 63% of cost is staff, and the driver is unmeasured | Measure first (Phase 1) |
| FM-04 | Reviewer automation complacency | Flag-only governance assumes alert, independent humans | Seeded-error program (to add), override telemetry |
| FM-06 / FM-16 / FM-24 | Commercial concentration and data-rights loss | Model C/D depend on a few large clients and on executed export rights (Q-N04) | Board limits, contract clauses, two sponsor-of-record partners |
| FM-05 | Specialist pool attrition | Pools of 1–3 at small scale | Bench, partnered non-cash processing |
| FM-17 | Custodian outage in surge | The twin's most dangerous stress | Seasonal buffer, second cash custodian |

**Structurally well-contained (by type-level absence plus tests):**
- FM-09: replay double effects.
- FM-13: insider with publish and deploy rights, if SoD exceptions are never granted.
- FM-23: agent permission creep.
- FM-07: model-provider lock-in, since agents are non-authoritative.

**New control additions recommended to 08** (gaps found here):
1. A reviewer seeded-error program (FM-04).
2. Expiry dates on governed parameters, with an age report in the board pack (FM-08).
3. A monthly controller variance attestation (AC-14).
4. Sampled human review of unflagged anomaly clusters (AC-14 / FM-12).
5. A cross-provider check on eligibility ingestion (FM-02).

## 4. Major conclusions for the executive report

| # | Conclusion | Evidence | Counterargument | Claim state / confidence | Falsification |
|---|---|---|---|---|---|
| MC-1 | Stage the business as infrastructure first (C), earn a partner sponsor-of-record hybrid (D), and keep owning a sponsor (B) as a later option | 10- scoring: C first in 63.4% and D in 36.5% of random weightings; A and B never first; 09 ramp peak capital C $6.4m vs B calibrated $12.8m [S]; data access closed (EV-122) | B has the best steady-state economics [S]; C depends on unproven willingness to pay (AC-16) and executed data rights (FM-16) | suggestive / Low-Medium | No paid ≥20k-account design partner within 12 months; executed contracts deny API or export |
| MC-2 | About 29% of conventional activity kinds (23 of 80) are eliminated or reduced to a residual; 51% change mechanism; 20% stay human | Activity census (tested CSV) | An enumeration of activity *kinds*, not hours; built by the design team | internal-demonstration / Low-Medium | An independent practitioner re-classification differs on >15% of rows |
| MC-3 | The smallest responsible organization is ~21 people at 1k accounts and ~104 at 100k **[S]** | 09 model; structural floor of ~8–10 for SoD and accountability | 23 of 30 parameters assumed; loaded cost swing 95% | internal-demonstration / Low | Measured handling times >2× assumed |
| MC-4 | AI-native cost per account falls below the frontier (Fidelity ~$790 all-in) somewhere between 10k and 100k accounts **[S]** | 09: $697 at 10k, $272 at 100k | Fidelity's allocation differs (affiliate-staffed, EV-023/024); assumptions dominate | internal-demonstration / Low | Shadow-mode-measured parameters put the cost at 100k above $790 |
| MC-5 | Humans own most decision *types* (33 of 81) but little decision *volume* | Decision census (tested) | Volume classes are design judgments, not measurements | suggestive / Medium | Pilot telemetry shows H decisions >10% of decision volume |
| MC-6 | Inference cost is immaterial; supervision is the AI cost | EV-106; 09 inference 0.3% of cost; ×10 swing 2.7% | Agentic multi-step costs and evaluation infrastructure | suggestive / Medium-High | AI run cost >5% of staff cost per outcome |
| MC-7 | The exception rate (and recipient-level reuse of determinations), not automation or headcount, is the economic lever | 09 sensitivity (exception rate and minutes ~27% swings each); twin: halving exceptions removes the surge breach | Exception rate is a recipient proxy (EV-079); reuse is unmeasured and its legality across sponsors unclear | suggestive / Medium | Measured reuse <1.5; exception rate insensitive to policy changes |
| MC-8 | Liquidity under a custodian outage during the year-end surge is the top operational stress | Twin: 30-day outage exhausts a 2% buffer; 5-day leaves 8.8 days | Buffer, surge and outage parameters are all assumed; real custodians have BCP | internal-demonstration (simulated) / Low-Medium | Actual buffer policy and custodian RTO make exhaustion infeasible |
| MC-9 | Preserving the advisor's role is a commercial necessity, not a courtesy | CIAP 46.9% of Fidelity assets and rising (EV-027); RCF/Ren distribution spine; adviser fee layer (EV-068) | Proposed regs may reclassify advisors (EV-092); direct-to-donor challengers grew (EV-058, vendor claim) | suggestive / Medium | Advisor pilot shows placement unaffected by loss of investment role |

### 4.1 What the executive report must soften or drop

1. **Drop precise cost ratios** ("2.9× / 3.7× below the frontier"). Report "plausibly below the frontier at ≥~100k accounts, if measured exception handling matches assumptions [S]".
2. **Present FTE counts as orders of magnitude** ("tens of people at 10k–100k accounts; a fixed floor of ~20 at any scale") with **[S]**.
3. **Do not present MC-1 as the winner.** Present it as the lowest-regret *sequence* under current evidence, with B kept as an option and the falsifiers stated.
4. **Hold the "29% eliminated" figure to activity kinds**, not effort or cost.
5. **Present the twin results as illustrations of mechanisms** (surge sizing, linear exception scaling, liquidity), not predictions.
