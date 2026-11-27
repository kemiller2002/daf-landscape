# 05 — Activity elimination and automation

Each of the 180 activities was challenged with the mission's eighteen questions (why it exists; legal, contractual or control basis; whether poor upstream design causes it; whether it can be eliminated, prevented, made deterministic or AI-assisted; whether a human must decide, independently, as an Echelon employee; whether the sponsor or a shared capability owns it; batching; consequences of error and delay; how to measure it). Answers are in the `why_exists`, `legally_required` and `elimination_challenge` fields of [`operational-activities.csv`](data/registers/operational-activities.csv).

## 1. Result of the challenge

| Outcome | Activities | Comment |
|---|---:|---|
| Eliminated by design or deferral | 3 | Cards, foreign/ER grants, UBIT (deferred scope; zero frequency) |
| Fully deterministic | 22 | e.g., transaction-time charity status checks (exception rate 0.05%), CA AG/FTB status ingestion, grant intake (1%) |
| Automated with exception escalation | 54 | e.g., reconciliation breaks (2% of matches), unidentified receipts (4% of contributions), payment returns |
| AI-assisted exception handling | 18 | contacts, close preparation, audit support, fiscal-sponsor resolution, migration |
| Mandatory human judgment | 24 | death/incapacity, disputes, Tier-2 grant review, complex gifts |
| Mandatory independent human authorization | 13 | payment batch release, manual journals, bank-detail changes, break-glass, two-approver code review |
| Sponsor-owned | 19 | reserved legal control, board delegations, policy approvals, monthly sign-off |
| External provider | 7 | payment execution, custodial receipt, check printing |
| Shared Echelon | 20 | platform engineering, assurance programme, implementation |

Of the 37 activities claiming a human must decide (judgment + independent authorization), 10 are legally required, 7 contractual, 9 uncertain and 11 not legally required. The last 11 are Echelon or Unbound policy choices. They are retained because they protect donors or financial integrity, but they are candidates for redesign ([21](21-requirement-economic-impact.md)).

## 2. Where automation saves, and where it does not

Measured by the model (same inventory, CFG-5, PG-HNW, 2,000 accounts):

- **97% of events complete without a person.** The residual 3% carries all the labour.
- **Variable labour is small; fixed and floor labour dominate below ~5,000 accounts.** Vendor hours rise only from ~2,740 at 100 accounts to ~3,850 at 2,000 accounts ([`scale-grid-accounts.csv`](data/model-outputs/scale-grid-accounts.csv)). The platform's own engineering, assurance, and charity-data upkeep set the floor; automation does not remove them.
- **AI matters less than design.** The AI factor (0.85 base, field evidence) applies only to 18 AI-assisted activities. Moving it from 0.6 to 0.97 changes View 1 by about ±$25k at $500M ([`sensitivity-tornado.csv`](data/model-outputs/sensitivity-tornado.csv)). Exception rates (`exception_mult`) and handling minutes (`duration_mult`) matter 5-20× more.
- **The original model's AI oversight cost ($0.3M flat) is replaced** by an explicit activity (OA-TEC-021 AI agent configuration, evaluation and change control, 384 h/yr) plus token costs that follow exception volume (Claude Sonnet 5.5 at $2/$10 per million tokens; ~$0.026 per assisted exception).

## 3. Elimination and prevention opportunities (not yet in requirements)

| Opportunity | Activity | Mechanism | Control objective preserved |
|---|---|---|---|
| Reuse recipient-level determinations across grants, funds and sponsors | OA-GRT-005, OA-CHR-* | determination cache with provenance and expiry | Tier-2 review of genuinely risky grants |
| Calibrate Tier-2 triggers per trigger from replay false-positive rates | OA-GRT-005 | measured specificity | §4966/§4967 protection |
| Make the board delegation an activation gate | OA-GRT-006 | no "pre-delegation" mode where every grant is a human batch decision (up to 90k decisions/yr) | sponsor control |
| Notification-first contributions with unique fund references or virtual accounts | OA-CON-004 | prevents unidentified receipts | no plug postings |
| Electronic enrolment of recipients; positive pay | OA-GRT-013/016 | fewer checks, fewer uncashed items | escheat compliance |
| One error-bound sampling plan instead of three overlapping regimes | UNB-XIN-CLM-005, CNV-GRT-011, CNV-GOV-008 | single sample serves all three | decision-quality assurance |
| One independent reconciliation attestation feeding the controller's sign-off | CNV-FIN-004, CNV-GOV-003 | remove duplicated layer | independent reconciliation |
| Weekly or risk-triggered NAV sample instead of daily | CNV-FIN-005 | Unbound does not compute NAV (external manager, OD-M-07) | valuation integrity |
| Event-driven affiliation confirmation instead of annual attestation | UNB-XIN-CRM-002 | prefilled confirmation on change | prohibited-benefit screening |
| Platform default threshold for the 72-hour hold | CNV-PLT-011 | avoids December holds and contacts | fraud hold for unusual grants |
| Passkeys/TOTP instead of SMS MFA | identity | removes the largest per-account infrastructure cost at scale | strong authentication |

## 4. Uncertain cases and conservative alternatives

For the 21 `uncertain` rows the model keeps the human step (conservative) and records the alternative:

- **Board-delegated deterministic grant approval** (RCD-005; whether it satisfies "exclusive legal control" and who is a "fund manager"): kept as sponsor-owned review of triggered grants; alternative is delegation with sampled post-review.
- **Deterministic payment release as the second person** (CNV-GOV-003): kept as three-distinct-person release until auditor and board accept the design.
- **Deterministic renewal of charity eligibility without sign-off** (SPD-GRT-001): kept as hybrid vetting with human review of exceptions and high-risk tiers ([15](15-charity-vetting-alternatives.md)).
- **POA agents exercising donor privileges** (UNB-XIN-TRS-004#Q1): kept as human verification.

## 5. What cannot be automated (current evidence)

Reserved sponsor decisions (Tier-2 grants, delegations, policy approval, monthly sign-off); independent release of payments and manual journals; death and incapacity; disputes and right of response; fraud investigation; complex non-cash gifts; external audit and SOC examinations; incident command; and author-plus-two approval of control-relevant code. Agents can prepare evidence for all of these; they are not independent controls ([06](06-human-control-obligations.md)).
