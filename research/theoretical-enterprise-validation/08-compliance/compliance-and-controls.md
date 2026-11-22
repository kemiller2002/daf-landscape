# Compliance classification and control design

**Status:** theoretical. **Not legal advice.** No statement here establishes, or claims, SOC 1 or SOC 2 compliance. Controls are *designed* only; none is operating.

## 1. Classification of requirements by authority

The baseline [regulatory map](../../ai-native-daf-enterprise/08-governance-and-compliance/regulatory-applicability-map.md) already labels its 65 REG rows: obligation type legal / risk_control / convention, and evidence [F] fetched / [S] secondary / [R] repo note / [K] unverified. This program does not re-verify them. It maps them into the directive's six classes and flags where requirements in `docs/` rely on unverified rows.

| Directive class | Baseline rows (examples) | Count (approx.) | Implication |
|---|---|---|---|
| 1. Verified legal requirement | Statute text of REG-001 (excise rates and exceptions only), 003, 004, 008, 009, 011, 013, 024, 037 (OFAC reporting) — label [F] on primary text | ~20 | Design to them now. **Review correction (A1):** REG-001's "sponsor-signed approval on every grant" is interpretation (class 2), not verified law. |
| 2. Interpretation needing professional review | REG-002 ER mechanics [K]; REG-020 ED (Notice 2006-109 UNVERIFIED); REG-042/043 money transmission [I]; REG-057 UPMIFA [S]; DD-004 delegation reading of REG-001 (TVC-003); acknowledgment timing for reversible gifts (TVC-023); recipient refund treatment (OD-09); escheat (REG-045 [K]) | ~15 | Block dependent requirements from "approved" status until reviewed |
| 3. Sponsor policy choice | Thresholds, routine class, haircut, fixing time, provisional credit limit, cooling-off length, discretionary holds (REG-055/CTL-045), over-commitment priority | — | Owner decisions ([OD register](../16-registers/owner-decisions.md)) |
| 4. Industry convention | REG-025 990 Part VI policies; REG-039/040 Treasury/FATF guidance; REG-059 COI policy; NAV-error materiality practice | ~8 | Adopt with stated rationale; not mandatory |
| 5. Proposed internal control | CTL-001..054; TVCTL-01..12 below | 66 | Need full template fields |
| 6. Unverified (labelled [K]: not fetched) | REG-015, 026, 049, 050, 058, 061, 062, 064 | 8 | **Review correction (A3):** "not fetched" does not mean "not law". §509 public support, §6001 records, breach-notification statutes and E-SIGN are real obligations whose *text* was not verified here. Treat them as **class 2 pending verification**, not as assumptions. REG-025 is a convention (class 4). |

**External fact checked in this program:** Nacha rules give most ACH returns a two-banking-day deadline. Unauthorized **consumer** debits (R10) may be returned until the banking day after the 60th calendar day after settlement. [S: nacha.org summary pages "Differentiating Unauthorized Return Reasons" and "Which 60 Days is It?", accessed 2026-11-22. **Downgraded from [V] in review:** the rule text itself was not read.] Business-account unauthorized debits use a two-day window [unverified]. A 2024 amendment on timing after the written statement was seen but not confirmed as in effect.

This applies to **contributions** (debits), not to grant payments (credits). Consequence: TVC-023 and FI-22.

**Retention:** the record retention basis is mostly unverified (REG-026 [K]; TVC-016). The review notes that REG-037 (31 CFR 501, [F] on the regulation, though the inventory pass labelled the 10-year rule itself [S]) supports a **10-year minimum for OFAC-related records**. That is the one period this program states, as a floor pending counsel. Otherwise no period is stated. Classes R-* in the [ontology](../02-ontology/enterprise-ontology.md) await counsel (OD-12). Privacy deletion (REG-048 state laws [S]) conflicts with tax, OFAC and agreement retention, so CW-35 needs a precedence rule.

## 2. Control template gaps in the baseline

[controls.csv](../../ai-native-daf-enterprise/08-governance-and-compliance/controls.csv) (54 rows) has: objective (implied), risk, owner, frequency, evidence, test method. It is **missing**:
- evidence retention;
- failure response;
- monitoring threshold or KRI;
- independent verification (who tests, how often, independence);
- exceptions and escalation;
- the REG link;
- designed-vs-operating status.

Also, TVC-015 and TVC-029: coverage is asserted as 100% while the REG→CTL mapping is open. Finding TVF-040.

**Requirement TVR-CMP-001:** every control row carries the ten fields below plus `reg_ids` and `status ∈ {designed, implemented, operating-evidenced, tested-independently}`. Coverage metrics are reported with numerator, denominator and status filter.

## 3. Proposed controls (full template)

SOC mapping is indicative only: TSC = AICPA Trust Services Criteria common-criteria families; ICFR = relevance to SOC 1 / financial-statement controls (TVC-027).

### TVCTL-01 Reservation conservation and over-commitment monitor
| Field | Value |
|---|---|
| Objective | No fund or constrained ancestor commits more than its reservable capacity; over-commitment from market moves is detected |
| Risk | Double spending; negative funds; unfunded approved grants (FI-05, FI-12) |
| Authority | Controller (A); treasury (R) |
| Trigger / frequency | Preventive at every reservation; detective after each NAV strike |
| Evidence | Reservation record with capacity snapshot; daily over-commitment report with zero-or-cases |
| Retention | R-FIN |
| Failure response | Block new reservations on the resource; open over-commitment case (OD-08 policy) |
| Monitoring | Count and value of over-committed funds; stranded reservations (must be 0) |
| Independent verification | Internal audit re-performs capacity for a sample of reservations quarterly |
| Exceptions | None for prevention; case decisions by CFO above threshold [P] |
| Mapping | ICFR; TSC processing integrity |

### TVCTL-02 Payment attempt exclusivity (double-payment)
| Field | Value |
|---|---|
| Objective | At most one live payment attempt per grant (PA-1); Unknown never retried blindly |
| Risk | Duplicate payment (TVC-024) |
| Authority | Payments ops lead (R); Controller (A) |
| Trigger | Preventive at attempt creation; detective daily scan of grants with >1 non-terminal attempt |
| Evidence | Attempt history; PA-2 decisions with approver and evidence |
| Retention | R-FIN |
| Failure response | Freeze grant; recall request; recovery case |
| Monitoring | Unknown-state age distribution; PA-2 decisions per month |
| Independent verification | Reconciler (≠ releaser) matches bank debits to attempts daily |
| Exceptions | PA-2 human decision requires two approvers (releaser excluded) |
| Mapping | ICFR; TSC processing integrity |

### TVCTL-03 Provisional contribution limit
| Field | Value |
|---|---|
| Objective | Reversible value does not fund irreversible grants beyond a set exposure |
| Risk | Sponsor loss on returned debits (TVC-023; R10 60-day window) |
| Authority | CFO (A); treasury (R) |
| Trigger | Preventive at reservation; detective weekly exposure report |
| Evidence | Capacity calculation showing provisional component; exposure report |
| Retention | R-FIN |
| Failure response | Over-limit reservation rejected; returned-debit cases tracked to recovery |
| Monitoring | Provisional exposure total; returned contribution rate |
| Independent verification | Audit sample |
| Exceptions | Credit-limit increases by CFO with donor-specific rationale [P] |
| Mapping | ICFR |

### TVCTL-04 Release-time re-check (SM-6)
| Field | Value |
|---|---|
| Objective | Authority, eligibility, sanctions, holds and data freshness re-evaluated at payment submission |
| Risk | Payment after revocation, sanctions listing or authority loss (WF-09; TVC-033) |
| Authority | CRCO (A for rule); payment gate (S) |
| Trigger | Every submission |
| Evidence | Gate decision record with list and policy versions |
| Retention | R-FIN + R-OFAC |
| Failure response | Hold; case |
| Monitoring | Gate denial rate by reason; stale-data blocks |
| Independent verification | Seeded test grants (canaries) to revoked or listed test recipients in production-like environment; result reviewed by internal audit |
| Exceptions | None |
| Mapping | TSC processing integrity; OFAC (REG-036) |

### TVCTL-05 Protective-check completion before release (resolves TVC-007)
| Field | Value |
|---|---|
| Objective | No routine grant is released while a protective screen has not completed, or its deterministic fallback has not run |
| Risk | §4967 benefit; reputational |
| Authority | CRCO |
| Trigger | Every routine grant |
| Evidence | Decision record shows agent result or fallback result |
| Failure response | Hold |
| Monitoring | Fallback rate; agent latency |
| Independent verification | QA sample of fallback-path grants |
| Exceptions | None |
| Mapping | TSC processing integrity |

### TVCTL-06 Assurance-bound auto-approval (resolves TVC-025/026)
| Field | Value |
|---|---|
| Objective | No grant is auto-approved beyond the assurance of the session or principal that requested it; new recipients from phishable or agent sessions need step-up confirmation |
| Risk | Account takeover (FM-12); prompt-injected agents |
| Authority | CRCO + security |
| Trigger | Every recommendation |
| Evidence | Session assurance, `amr`, confirmation event |
| Failure response | Route to confirmation or hold |
| Monitoring | Holds for unconfirmed new recipients; confirmed-to-requested ratio |
| Independent verification | Red-team exercise annually [P] |
| Exceptions | None |
| Mapping | TSC CC6 (logical access) |

### TVCTL-07 Reconciliation independence (resolves TVC-028)
| Field | Value |
|---|---|
| Objective | Disbursements reconciled by a role outside the payment chain |
| Risk | Concealed misdirected payments |
| Authority | Head of financial reporting or internal audit (A) — not the Controller |
| Trigger | Daily |
| Evidence | Three-way match report; break log with owner ≠ releaser |
| Failure response | Breaks aged > threshold escalate to Audit Committee |
| Monitoring | Break count and age |
| Independent verification | Internal audit (review A14: the external auditor tests controls but is not part of the control system) |
| Exceptions | At very small scale, a compensating review by an outside accountant [P]. Review B-6: a monthly compensating review leaves ~30 days of double-payment exposure, so the review must be at least weekly for payment matching. |
| Mapping | ICFR |

### TVCTL-08 NAV-error and restatement control
Objective: errors in struck NAV from custodian corrections are evaluated against materiality and corrected consistently (FI-28). Authority: Controller (R); CFO plus an independent reviewer (A). Evidence: NAV-error case with computation. Failure response: affected statements corrected. Independent verification: auditor. Mapping: ICFR.

### TVCTL-09 Policy delegation linkage (resolves TVC-003 in part)
Objective: every D approval cites a policy version that is linked to an effective board delegation. Evidence: per-decision link. Failure response: if a delegation lapses, dependent policies suspend (routine path → human). Independent verification: Audit Committee annual review. Mapping: governance; REG-001 [C].

### TVCTL-10 Authority-change propagation
Objective: authority changes reach every derived session, token, widget instance and recurring template within the stated window (AUTH-I1, TVR-WID-001/006). Evidence: propagation log with timestamps. Failure response: incident. Monitoring: p99 propagation time. Independent verification: quarterly test revocations. Mapping: TSC CC6.

### TVCTL-11 Control-evidence integrity (resolves TVF-041)
Objective: control evidence cannot be altered by the function whose controls it evidences. Authority: internal audit (A). Evidence: append-only store with hash chain; access logs. Failure response: evidence gap logged as control failure. Independent verification: auditor. Mapping: TSC CC4/CC7.

### TVCTL-13 OFAC blocking and reject reporting (rev 2; review A5)
Objective: when a payment or asset involves a blocked person, funds are **blocked** (not merely recalled to the fund) or rejected as required. Reports are filed within the regulatory deadline. Records are kept for at least 10 years (REG-037 [F]; application to DAFs [C]).

Implementation and ownership:
- Authority: sanctions officer (R), GC (A).
- Requires a `Blocked` disposition in the payment attempt and contribution models, with a blocked-property account.
- Failure response: escalate to the GC immediately.
- Independent verification: internal audit annually.

Note: TVCTL-04 is a pre-payment gate and **does not** cover REG-037 reporting (review correction).

### TVCTL-14 Disqualified-recipient and excess-benefit gate (rev 2; reviews A8, A18)
Objective: the routine path excludes recipients and payees where:
- §4966 requires expenditure responsibility, or where the grant is a taxable distribution, e.g. Type III non-functionally-integrated supporting organizations and donor-controlled supporting organizations [unverified detail, C];
- §4958(c)(2) treats any payment to a donor, advisor or related person as automatic excess benefit (REG-004 [F]).

Implementation: deterministic classification from IRS codes and the relationship graph. A match routes to a human, never to auto-approve. Independent verification: QA sample.

### TVCTL-12 Expenditure responsibility obligation tracker (fills REG-002 gap)
Objective: every ER grant has pre-grant inquiry, agreement terms, reports and Schedule D/990 reporting inputs tracked to completion. Authority: grants compliance head. Evidence: per-grant obligation record. Failure response: missing report → escalation and hold on further grants to that grantee. Independent verification: annual sample. Mapping: REG-002 [K → C].

## 4. Unmapped legal obligations

The governance inventory pass identified legal rows with no identifiable control (OUTSTANDING A1 is still open):
REG-002, 006 (ongoing), 013, 014, 015, 019 (snapshot retention), 020, 024, 026, 027–032, 035, 037 (blocking/reject reports), 041, 042/043, 046, 048, 049, 050, 054, 060, 064/065.

This program adds TVCTL-12 for REG-002, TVCTL-13 for REG-037 reporting and TVCTL-14 for REG-004/§4966 recipient classes. The rest remain gaps (TVF-045). Several are conditional on the business model (C vs D), and BSA scope changes if the provider runs custody (REG-043). Controls must therefore be **conditioned on the operating model** (TVR-CMP-003).
