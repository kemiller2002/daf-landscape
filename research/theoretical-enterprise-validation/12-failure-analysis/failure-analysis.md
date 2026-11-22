# Failure analysis

**Status:** theoretical [T]. Methods are applied only where they add information. Likelihood scores (1–5) are **assumptions** made in the absence of operating data; they rank attention, they do not estimate probabilities. Baseline failure modes FM-01..25 ([Clarity/EDF](../../ai-native-daf-enterprise/13-clarity-edf-analysis/failure-modes.csv)) are not repeated unless this analysis changes them.

## 1. FMEA: catastrophic and irreversible outcomes first

S = severity, L = likelihood assumption, D = detectability (5 = hard to detect). RPN is used only to order the table.

| ID | Failure mode | Effect | S | L | D | RPN | Controls (designed) | Residual uncertainty |
|---|---|---|---|---|---|---|---|---|
| FMEA-01 | Duplicate payment after provider timeout | Irreversible loss; recovery needs the charity's cooperation | 5 | 3 | 2 | 30 | PA-1..4, TVCTL-02 | Providers may not offer proof of non-receipt (TVC-024); ACH has no end-to-end key |
| FMEA-02 | Payment to a hijacked payee profile | Loss; reputational | 5 | 3 | 3 | 45 | WF-10, SoD-1, cooling-off, TVCTL-04 | Compromised charity mailbox defeats the prior-contact notice |
| FMEA-03 | Account takeover produces routine-looking grants to an attacker-controlled charity | Loss; §4966 exposure | 5 | 3 | 4 | 60 | TVCTL-06, velocity | Sham charity listed in Pub 78 passes eligibility (TVS-026) |
| FMEA-04 | Policy misconfiguration auto-approves ineligible class | Taxable distributions at scale | 5 | 2 | 3 | 30 | DD-011 gate, back-test, CTL-046 canaries | Back-test coverage of rare classes |
| FMEA-05 | Grant approved under lapsed delegation (board resolution not linked) | Unauthorized grants; governance failure | 4 | 2 | 5 | 40 | TVCTL-09 | Delegation records maintained outside the platform |
| FMEA-06 | Returned ACH contribution after it funded a paid grant | Sponsor loss; incorrect acknowledgment | 4 | 3 | 2 | 24 | TVCTL-03, CON-1..3 | Return rate unknown |
| FMEA-07 | NAV error from custodian correction propagates to all unit transactions | Misallocation among donors | 4 | 2 | 3 | 24 | FI-02, FI-28, TVCTL-08 | Materiality policy undecided |
| FMEA-08 | Over-commitment in drawdown leaves approved grants unfundable | Broken commitments to charities | 4 | 2 | 1 | 8 | FI-12, TVCTL-01 | Priority rule undecided (OD-08) |
| FMEA-09 | Payment released while protective AI check pending | Prohibited-benefit grant paid | 4 | 3 | 3 | 36 | TVCTL-05 | Fallback rule quality |
| FMEA-10 | Revoked advisor keeps acting through a stale widget, token or recurring template | Unauthorized recommendations | 4 | 3 | 3 | 36 | AUTH-I1, TVCTL-10, WG-1 | Partner deprovision latency (TVC-032) |
| FMEA-11 | Sanctions false negative from fuzzy-matching limits or transliteration | Strict-liability violation | 5 | 2 | 5 | 50 | CTL-012/013; B6 recall test open | Recall on transliterated names unmeasured (OUTSTANDING B6) |
| FMEA-12 | Evidence store altered or incomplete | Unsupportable audit assertions | 4 | 2 | 4 | 32 | TVCTL-11 | — |
| FMEA-13 | Status label misleads donor into duplicate recommendation | Double grant | 3 | 3 | 3 | 27 | Status vocabulary; duplicate flag | Copy not yet tested with users |
| FMEA-14 | Specialist backlog during surge delays legally sensitive decisions | SLA breach; pressure to approve hastily | 3 | 4 | 1 | 12 | Surge levers (economics §3) | Automation-bias pressure rises with backlog (FM-04) |

## 2. Fault trees (top events)

### FT-1: Money leaves the sponsor twice for one grant

```
Duplicate disbursement
├── OR: Two attempts both settle
│   ├── AND: Attempt 1 Unknown
│   │        AND new attempt created            ← blocked by PA-1
│   │        AND PA-1 bypassed (manual payment outside platform)   ← TVR-PAY-004: no off-platform payments
│   └── AND: Provider processes one request twice (provider-side bug)
│            AND provider idempotency absent    ← DD-020 selection; TVC-024
├── OR: Two grants for one intent
│   ├── Duplicate recommendation from two channels approved   ← duplicate flag (WG-5), not a block
│   └── Donor re-recommends after misleading "failed" status  ← status vocabulary
└── OR: Check cashed after void + reissue paid               ← PA-4 stop-payment
```

**Minimal cut sets of size 1** (single failures that cause the top event):
- off-platform manual payment;
- provider double-processing with no provider idempotency.

Both are outside the platform's software. Controls are contractual and procedural. Finding: **the most likely double-payment paths are organizational, not software** (TVF-076).

### FT-2: Grant paid to an ineligible or prohibited recipient

```
Ineligible payment
├── Eligibility data wrong
│   ├── Stale feed (CTL-011 blocks)
│   ├── Poisoned load (CTL-050 cross-check; E1 poisoned case not built)
│   └── Name/EIN collision (B5 open)
├── Eligibility right but changed after decision
│   ├── Before release → TVCTL-04 re-check
│   └── After release → post-payment review only
├── Recipient eligible but grant purpose prohibited
│   ├── Benefit check pending at release → TVCTL-05
│   └── Benefit check misses (P recall < 1)
└── Approval rule wrong (misconfiguration, FMEA-04)
```

### FT-3: Unauthorized person directs a grant

```
Unauthorized direction
├── Impersonation (ATO, federated IdP compromise) → TVCTL-06
├── Authority lapsed but still exercised → AUTH-I1/I2, TVCTL-10
├── Delegation exceeds delegator (AUTH-03) → chain re-walk at execution
├── Agent prompt-injected below confirm cap → TVC-026
└── Staff acting on email "instruction" (requests ≠ instructions, DD-003)
```

## 3. Threat model (STRIDE over the main trust boundaries)

| Boundary | S | T | R | I | D | E |
|---|---|---|---|---|---|---|
| Donor/advisor session | ATO → TVCTL-06 | Preview tampering → preview hash, server recompute | Disputed submission → signed receipt with session `amr` | Balance leakage on shared device → session expiry | Credential stuffing → rate limits | Delegation abuse → AUTH-03 |
| Partner host / widget | Host impersonates sponsor UI around widget (WG-3) | postMessage injection → validation (baseline) | Partner denies a launch → launch audit | Host scrapes widget? (cross-origin prevents) | Launch flooding | Partner self-service broad scopes → review gate |
| Donor agent | Stolen token → sender-constrained (CTL-053) | Injected instructions → confirmation rule | Agent attribution → actor in token exchange | Over-broad read scope | Burst recommendations → velocity | Self-escalation impossible (INV-A5) |
| Staff / insider | Shared credentials → FIDO2 | Ledger edit → append-only | Approval denial → signed approvals | Bulk export → DLP, JIT | Kill-switch misuse → two-person rule [proposed TVR-OPS-002] | **Two colluding staff** defeat pairwise SoD → reconciler independence plus anomaly analytics; residual (TVF-077) |
| Provider / custodian | Spoofed webhook → signature + two-source confirmation | Altered settlement file → hash and bank match | Provider disputes instruction → signed instructions | Provider breach exposes donor data → minimization | Outage → FM-17/18 | — |
| AI agents | — | Poisoned retrieval → snapshot citations | Unattributed draft → AgentRun records | Data sent to model APIs → vault exclusion | Model outage → AI-12 fallback | Tool scope creep → INV-A5, AgentPermissionChanged gate |

## 4. Event storming of a high-stress day (narrative check)

December 30, 100k accounts, k = 3 surge, a 4% equity drop, and the IRS publishes an auto-revocation list mid-day.
1. The revocation diff holds 140 in-flight grants (WF-09). Donors get redirect options. Contact volume spikes (GAP-006).
2. The drop puts some near-fully-reserved funds into over-commitment (FI-12). New reservations on those funds are refused. Donors see "Funding delayed" for grants approved earlier today if they were not yet funded, which depends on the alternative-1D choice.
3. A provider times out on a batch. Unknowns arise. PA-2 queue grows on the busiest day of the year, while payment-ops staff are at minimum (holiday).
4. Year-end tax-deadline pressure on donors (contributions must be received by 12/31) [I] meets ACH provisional status: contributions made today are not available for grants until after the return window under CON-1, which donors may read as "lost".

**Cross-domain weakness:** four independent subsystems degrade on the same day, and they all share the same specialist and payment-ops staff and the same contact channel. The baseline twin models the surge and a custodian outage, but not this conjunction. Requirement TVR-OPS-003: a year-end readiness plan with conjunction drills (surge + market move + provider failure + regulatory publication).

## 5. Counterfactual checks

| Question | Answer |
|---|---|
| If the AI were removed entirely, what breaks? | Nothing on the D path. Exception minutes rise (dossier preparation) and benefit-risk detection falls. TVCTL-05's fallback keeps release safe. The design degrades gracefully, which supports DD-002. |
| If the AI is wrong but confident? | It can only add flags (cost) or fail to add them (missed detection). It cannot approve. The dominant risk is reviewer automation bias (FM-04), not AI action. |
| If external systems disagree? | No source wins by default (FI-29). Breaks block resource capacity above a threshold. The disagreement is visible, not resolved silently. |
| If an irreversible action must be corrected? | A child correction record and a recovery case (SM-0). A recovery request to a charity is human-authorized. The original record is never edited. |
| What would a skeptical auditor reject? | (1) Coverage claims without denominators (TVC-015); (2) controls with no independent tester (TVF-040); (3) the Controller reconciling its own disbursements (TVC-028); (4) the evidence store administered by the CRCO (TVF-041); (5) D approvals with no cited board delegation (TVC-003). |
| What would a first-time user misunderstand? | "Available" as cash; "Accepted" as approved; a % grant estimate as a commitment; Unknown as failure; nomination as succession. |
