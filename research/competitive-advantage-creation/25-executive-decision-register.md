# 25 - Executive decision register

Status: research (2026-11-26). Reconciliation agent (RECON). This report lists every Phase III decision proposal (P3-DEC-) in [decisions.csv](data/registers/decisions.csv), after both review rounds and model revision 3. **Every P3-DEC- item is "proposed - owner decision required".** None is approved, and none authorizes expenditure, outreach, contracts or production work (BRIEF; DEC-008). The proposals are kept separate from the twelve approved Phase II decisions and from the owner's four Phase III decisions, which are listed first for reference and are not reopened here.

## Answer in brief

1. **The critical path is five decisions, all costing nothing to take.**
   - **P3-DEC-MOD005, decided first:** who performs and pays for the human deep review under licensing.
   - **P3-DEC-MOD004:** OD-CDD-02, decided alongside MOD005.
   - **P3-DEC-MOD003:** gate further DAF-specific build or spend on a named partner, a price expression and a candidate customer at the break-even size *for the chosen review allocation*.
   - **P3-DEC-CE002:** make revenue per customer at a named size an explicit gate.
   - **P3-DEC-MOD001:** define the cost-center month.

   Model revision 3 (CFO-corrected basis, after round 2) leaves the decision unchanged. With the cost center at month 0, every configuration pauses at month 24, and none beats doing nothing in the Monte Carlo (`sequences-ranking.md`).
2. **Payback exists only for partner-book licensing.** The partner licenses Unbound for its whole book (SEQ-PB, P3-SEQ-MOD012), and payback requires the sponsor to perform the deep review (month 76, +$4.18M at month 120, peak $2.43M) or M5 (month 80) (`bases.md`). Single-sponsor break-even depends on who performs the review (`gate-break-even.md`):
   - Echelon performing M1: not reached;
   - risk-tiered review: 5,202 accounts;
   - the sponsor performing it: 3,079 accounts ($175k net);
   - M5: 3,169 accounts.

   That is why P3-DEC-MOD005 now comes before the gate's size threshold.
3. **Proposals revised after review:**
   - **P3-DEC-CD001** is an adoption and reference route (round 1).
   - **P3-DEC-EK001** is a walk-away price on the achieved cost base: $27.86 on the revision-3 lean base and $58.51 on MD-6 (`response-walk-away.md`).
   - **P3-DEC-MOD003** is restated per review allocation (round 2).
4. **Twenty-three proposals in all**, grouped below by when they need deciding. Critical-path items are marked.

## 1. Already decided (reference only; not reopened)

**Approved Phase II decisions (owner, 2026-11-26), all at "strategically approved".** None is at "requirements incorporated", "evidence gate satisfied", "implementation authorized", "implemented" or "validated" ([01](01-approved-strategic-baseline.md)):

| ID | Direction |
|---|---|
| DEC-001 | Partner-first entry through a module inside an existing channel partner's offering, then licensing; OD-M-05 kept as a long-term destination |
| DEC-002 | Defer custodial administration; the $0.5-1.0B anchor condition is a planning assumption |
| DEC-003 | Change-driven charity re-vetting within the preserved 180-day validity policy |
| DEC-004 | Exclude non-redistributable data from shared or resold layers |
| DEC-005 | AI assessments are advisory only |
| DEC-006 | Licensing or subscription before asset-based fees |
| DEC-007 | Concentrate early migrations on one incumbent source where practical |
| DEC-008 | Gated capital deployment; modelled amounts are not approved expenditures |
| DEC-009 | No proprietary charity payment network |
| DEC-010 | Evidence-based process SLAs only after rehearsals and validation |
| DEC-011 | Transitus scope discipline |
| DEC-012 | Adopt the validation plan and its gates; develop lower-cost methods |

**Owner decisions in Phase III (2026-11-26, the owner's words):**

| ID | Decision | Effect |
|---|---|---|
| OD-P3-01 | "EF owns all property we make" | Unbound, Transitus, components and models are Echelon Foundry assets; commercial licence terms are an owner act |
| OD-P3-02 | "Kill rule doesn't stop Transitus" | Transitus is outside the kill rule in every sequence |
| OD-P3-03 | "No named partner rule starts when we have significant expenses" | The kill-rule clock does not start at approval |
| OD-P3-04 | "Significant is when it becomes its own cost center" | The clock starts in the month DAF commercialization becomes its own cost center |

**Open for the owner:** whether OD-P3-03 and OD-P3-04 also start the month-24 pilot clock (P3-DEC-CE001); OD-CDD-02 in Unbound (P3-DEC-MOD004); and who performs the deep review under licensing (P3-DEC-MOD005).

## 2. Proposed decisions (P3-DEC-), owner decision required

### 1. Critical path: gates before any DAF cost center or further DAF-specific spend

| ID | Proposed decision | Options | Recommendation | Reversibility | Evidence needed | Trigger (when to decide) | Revision 2 note |
|---|---|---|---|---|---|---|---|
| P3-DEC-MOD005 | Decide who performs and pays for the human deep review under licensing: the sponsor (sponsor labour in Unbound; Echelon bears monitoring only) or Echelon (as a priced service with matching revenue) | Sponsor performs (licensing; r1 sponsor policy; UNB-CDD-CIV-010) / Echelon performs as a priced service / Echelon performs unpriced (structurally loss-making) | Sponsor performs; Echelon offers review only as a separately priced service; decide alongside OD-CDD-02 | High (contract term) | Partner and sponsor interviews (V-6; V-2); counsel on reliance | **Critical path, first.** Now; decide with P3-DEC-MOD004 | Revision 3 (round 2, P3-CHL-REV4001): single-sponsor break-even is not reached if Echelon performs M1, and is 3,079 accounts ($175k net) if the sponsor performs the review. Partner-book licensing pays back (month 76) only with sponsor-performed review |
| P3-DEC-MOD003 | Gate any further DAF-specific build or spend on a named partner with a non-binding price expression and one candidate customer at or above the break-even size for the chosen review allocation (single sponsor or partner book) | Gate now / Build S3 first / Validate only ($0-25k ladder) | Gate now; restate the size threshold after P3-DEC-MOD005 (sponsor accounts and partner-book accounts in data/model-outputs/tables/gate-break-even.md); continue only $0-25k validation until the gate is met | High | V-6 named partner; V-2 price; sponsor-size evidence (P3-GAP-MOD003) | **Critical path.** Now; the size threshold is set after P3-DEC-MOD005 | Restated in revision 3: threshold in single-sponsor or partner-book accounts per review allocation (`gate-break-even.md`): 3,079 / 12,457 sponsor-performed; 3,169 / 13,335 under M5; 5,202 / 33,333 risk-tiered; not reached with Echelon-performed M1 |
| P3-DEC-CE002 | Make revenue per customer at a named customer size an explicit gate before any sequence commitment: V-2 and V-6 must establish whether paying customers are (i) large sponsors at ER-7 scale, (ii) a partner's aggregated book or (iii) hosted programmes; treat P3-DEC-CD001 (host-sponsor programme route) as an adoption and reference route, not the primary revenue route, until the gate is met | (a) adopt A3 on ER-7 revenue as modelled; (b) adopt P3-DEC-CD001 as primary route; (c) gate the choice on revenue per customer at a named size | (c) | High (planning rule; no build or contract) | P3-VAL-CE001; V-2 nonbinding EOIs with account counts; V-6 term-sheet economics | **Critical path.** Before any sequence commitment; Gate 0-2 in [23](23-commercial-validation-roadmap.md) | Revision 3: revenue per customer must be tested at the break-even size for the chosen review allocation; plausible sponsors: 17 at 2,646 accounts or more |
| P3-DEC-MOD004 | Decide OD-CDD-02 (automated 180-day renewal) before any licensing commitment | Keep M1 human review / Adopt M5 hybrid with sample audit / Defer licensing | Decide before G1; licensing economics depend on it | Medium (requirements change) | V-3; V-9 auditor walkthrough | **Critical path.** Decide with P3-DEC-MOD005, before G1 or any licensing commitment | Revision 3: A3 peak $8.26M (Echelon-performed M1, demand-driven) vs $2.52M (M5); M5 break-even 3,169 accounts |
| P3-DEC-MOD001 | Adopt an operational definition of the cost-center month for the kill rule and decide whether Unbound development counts toward it | First DAF-specific cash spend (development excluded) / First DAF-specific cash spend including development / A monthly spend threshold / Owner-declared date | First DAF-specific cash spend booked to its own budget with development excluded; record the month when it opens | High (definition can be revised before the clock starts) | Owner clarification (P3-GAP-MOD005) | **Critical path.** Before the first DAF-specific spend; the clock definition must be fixed before it starts | Revision 3: with the cost center at month 0 every configuration pauses at month 24; at month 6 or 12, and with a whole first signing, A3 passes for go-live lags up to 12 months (`kill-timing.md`) |
| P3-DEC-CE001 | Complete the kill rule as Clarity decision architecture before the DAF cost center opens: for the named-partner and referenceable-pilot tests record the monitoring signal, threshold, underlying trigger claim, owner, operational response, reassessment response and trigger reassessment condition; decide whether OD-P3-03/04 also start the month-24 pilot clock; fix the cost-center definition (P3-DEC-MOD001) and the allocation rule (P3-DEC-MOD002) before the first DAF-specific spend and change them afterwards only to reduce ambiguity | (a) keep the rule as signal and threshold only; (b) complete the trigger record as proposed; (c) complete it and also start both clocks at the cost-center month | (c) | High before the clock starts; low after (a redefinition after spend weakens the control) | Owner ruling on the month-24 clock; V-6 contact log to calibrate P3-HYP-CE001 | Before the DAF cost center opens | Pilot test binds at month 24 for every platform sequence in base |
| P3-DEC-CE003 | Accept owner outcome measures, review cadences and reconsideration triggers for DEC-001, DEC-006 and DEC-008 (now agent proposals awaiting acceptance) using the report 21 conditions TI-01..TI-08 as the reconsideration criteria, so that the approved directions become ready for commitment under the Clarity readiness rule | (a) leave measures as agent proposals; (b) accept the Phase II drafts; (c) accept the Phase III TI conditions | (c) | High (criteria can be revised to reduce ambiguity) | Owner review of report 21 | Owner review of [21](21-commercial-thesis-invalidation.md); before any decision moves past 'strategically approved' |  |

### 2. Route, partner and pricing

| ID | Proposed decision | Options | Recommendation | Reversibility | Evidence needed | Trigger (when to decide) | Revision 2 note |
|---|---|---|---|---|---|---|---|
| P3-DEC-CD001 | Treat new-programme enablement through a host sponsor (S1/S4, Sequence E variant) as an adoption and reference route, not the primary revenue route, within an owner-set loss budget, consistent with P3-DEC-CE002 (primary revenue customer decided by the revenue-per-customer gate); treat narrow component offerings as acquisition cost/credibility assets; exclude new-sponsor formation and direct bank/CU/trust sales from initial go-to-market. Revision 2 (2026-11-26, round-1 review): previously 'Prefer new-programme enablement through a host sponsor (S1/S4, Sequence E variant) as the non-displacing acquisition route'; revised because the model shows E and G never pay back (P3-CHL-REV1008, REV1012, REV1033, REV2039) | A) host-sponsor programme factory; B) direct institutional programmes only; C) narrow component products as revenue wedge; D) direct financial-institution sales | A as adoption/reference route only, with B as fallback; reject C and D for initial entry; revenue route per P3-DEC-CE002. Revision 2 (2026-11-26, round-1 review): previously 'A with B as fallback; reject C and D for initial entry' | High (no build commitment beyond configuration templates) | Host sponsor willing to license hosted programmes (V-6); programme-level WTP among education/health foundations (V-2); counsel on hosted-programme roles; institutional demand scan (P3-GAP-CD010); host accepts a second system (P3-HYP-CD002); minimum programme fee or programme count that carries the licensor; escrow, tested export and funded wind-down before any pilot (P3-CHL-REV1015); counsel on solicitation registration (P3-GAP-CD013) | Before V-6 host conversations | Revised in Revision 2 to an adoption/reference route (E and G never pay back) |
| P3-DEC-EK002 | Make partner-contract protections a precondition of the DEC-001 partner pilot: non-exclusive licence (or exclusivity only against a paid minimum), change-of-control termination with licence continuation for live sponsors, data portability and source/escrow terms | (a) accept partner's standard paper; (b) require protections; (c) require protections only for pilots above a size | (b) | Reversible before signature; hard to reverse after | V-6 partner conversations | Before the first term sheet | Partner acquisition without protection ends revenue whatever the cost base |
| P3-DEC-FGJ003 | Set minimum channel-partner contract terms that preserve Echelon strategic independence under DEC-001 (non-exclusivity or narrow time-boxed exclusivity tied to volume; capped declining revenue share; IP retention; direct-reference rights; sponsor data portability and continuity on partner exit; no ROFR/acquisition option; change-of-control termination) | Negotiate case by case / Adopt minimum terms as a walk-away floor / Accept partner paper | Adopt as a walk-away floor before V-6 term-sheet conversations; any concession recorded as a decision | Medium (once signed, terms bind for the contract life) | V-6 partner responses (P3-HYP-FGJ005); counsel review | Before V-6 term-sheet conversations |  |
| P3-DEC-EK001 | Adopt a licensing walk-away rule set on the cost base actually achieved: do not sign a partner licence whose net price to Unbound is below the walk-away price for that cost base (about $73 per account-year on the Phase II MD-6 base, vendor break-even ~43k accounts; about $27.86 (five years; $21.56 at ten) on the Phase III lean licensor base of model revision 3, $1.03M fixed including TPSP and control operations and $12.15 unmeasured variable cost, with lean break-even at $84 net of 14,305 accounts; $30.35 with the founder at market (revision 2: $31.30, 17,431 accounts, $33.78)) unless the partner commits a minimum volume that covers fixed cost. Revision 2 (2026-11-26, round-1 review): previously 'below ~$73 per account-year (vendor break-even above ~43k accounts)' as a single floor on the MD-6 base; an interim Revision 2 text cited $21.51 on the revision-1 lean base (P3-CHL-REV1004, REV3005, REV3009; P3-CLM-CE006) | (a) no floor; (b) floor at the walk-away price for the achieved cost base, or committed minimum volume; (c) fixed floor at net ~$90. Revision 2 (2026-11-26, round-1 review): option (b) previously 'floor at net ~$73 or committed minimum volume' | (b) | Reversible (pricing policy) | V-2 price test; partner volume commitments; measured live run rate and variable cost per account (P3-GAP-MOD004, P3-GAP-CE005); walk-away split infrastructure vs organization with founder at market (agent MOD) | Before pricing any partner licence | Restated: $58.51 MD-6; $27.86 lean (revision 3; $31.30 in revision 2); $30.35 founder at market; lean break-even at $84 = 14,305 accounts |
| P3-DEC-EK003 | Build ordinary capabilities (append-only history, APIs, AI-readable docs, configuration onboarding, tenancy) to hygiene level only and do not position them as differentiators; reserve differentiation claims for replayable eligibility decisions and reconciliation-proved migration until V-3/V-5 evidence exists | (a) market the full architecture; (b) market only evidence-backed differentiators | (b) | Reversible | V-3 and V-5 results | Before external positioning or marketing material | No measured advantage yet (07) |

### 3. Capital, assurance and evidence spending

| ID | Proposed decision | Options | Recommendation | Reversibility | Evidence needed | Trigger (when to decide) | Revision 2 note |
|---|---|---|---|---|---|---|---|
| P3-DEC-AB001 | Plan commercialization of a completed Unbound on a lean incremental-cash basis with an explicit pre-contract run-rate cap (proposed <=$0.15M/yr cash) and staged release at the first-invoice gate; report Phase II $6.5M only as the conventional-organization reference | (a) keep $6.5M P50 planning basis; (b) lean basis with run-rate cap; (c) lean basis without cap | (b) | reversible | Partner term sheet (V-6); insurance and SOC indications; 12-month cost ledger | When a commercialization budget is first discussed | Revision 3: the 'lean basis' now means $1.83M S3 cash to first invoice ($2.12M in revision 2), not $1.0M; a pre-contract run-rate cap remains useful |
| P3-DEC-AB002 | Adopt the $0/$1k/$10k validation ladder with pre-registered V-1..V-9 rules; treat the existing G0 budget ($150-350k) as a ceiling and spend above $10k only where a cheaper method cannot meet the rule (V-4, counsel, auditor position, SOC) | (a) existing G0 as plan; (b) ladder with G0 as ceiling; (c) $0 desk tier only | (b); founder-led outreach still needs separate owner approval | reversible | Gate outcomes at each tier | Now (approval of the $1k tier is the trigger for outreach) |  |
| P3-DEC-AB003 | Ledger actual cash and human hours per accepted Unbound capability during the build so the sunk cost and productivity are observable (replaces PR #87 M-07 spike) | (a) ledger from now; (b) estimate afterwards; (c) run M-07 spike | (a) | reversible | None beyond telemetry already captured by Praxis | Now; $0 |  |
| P3-DEC-AB004 | Defer SOC 2 Type 1 audit, insurance binding and production hardening until a partner term sheet names a pilot customer; collect automated security evidence and indications at $0 meanwhile | (a) defer to term sheet; (b) buy readiness now | (a) | reversible (adds 3-12 months to procurement if a buyer appears suddenly) | Partner procurement timeline from V-6 | At a partner term sheet naming a pilot customer | SOC 2 Type 2 observation (3-12 months) now delays the first regulated signing in the model |
| P3-DEC-MOD002 | Choose the shared-infrastructure allocation rule across products and economic entities | Equal / Usage / Revenue / Standalone cost | Usage-based allocation reported beside a revenue-based view; never combine entities without a recorded justification | High | Measured usage per product once a second product exists | When a second revenue-bearing Echelon product exists | S7 is hypothetical today |

### 4. Charity intelligence and re-vetting

| ID | Proposed decision | Options | Recommendation | Reversibility | Evidence needed | Trigger (when to decide) | Revision 2 note |
|---|---|---|---|---|---|---|---|
| P3-DEC-HI004 | Begin archiving IRS monthly charity releases and sanctions lists immediately (no cost) because sources overwrite history and replay evidence cannot be recreated later | Start now / Start at registry build | Start now | High | None | Now; $0 (sources overwrite history) |  |
| P3-DEC-HI002 | Set the DEC-003 implementation default to hybrid risk-tiered monitoring with automated 180-day renewal and a zero-acceptance attribute sample of 149 per stratum a year (95% confidence; 2% tolerable) across three strata | Periodic human review / Monitoring plus expiry / Risk-tiered / Hybrid with sample audit | Hybrid with sample audit; sponsor may tighten parameters | High (configuration) | V-9 auditor view; P3-VAL-HI003; P3-VAL-HI006; owner decision OD-CDD-02 (automated renewal counting as the deep review) and SPD-GRT-001. Revision 2: until then M1 periodic human deep review is the compliance-bound base (UNB-CDD-CIV-008; P3-CHL-REV3010, REV3020) | After OD-CDD-02 (P3-DEC-MOD004) and V-9 | Conditional: M1 governs until OD-CDD-02; who performs the review is P3-DEC-MOD005 |
| P3-DEC-HI001 | Adopt sequential-residual savings accounting with work categories (eliminated; automated; accelerated; transferred; deferred; mandatory) for all Phase III economics; never sum savings across models | Additive savings / Sequential residual with categories | Sequential residual with categories; report vendor; sponsor and system cost | High (methodology) | P3-VAL-HI007 | Before Phase III savings are reported externally |  |
| P3-DEC-HI003 | Do not pursue charity intelligence as an independent commercial product; keep it as an Unbound component and a possible low-price partner add-on until evidence shows willingness to pay above incumbent list prices | Standalone product / Component plus add-on / Open public-domain publication | Component plus add-on; consider gated open publication of source-attributed public facts for credibility | High | P3-VAL-HI008; V-8 | Revisit only if V-8 or a desk test shows willingness to pay above ~$10k | Comparator corrected to Candid Charity Check |

### 5. Components and licensing

| ID | Proposed decision | Options | Recommendation | Reversibility | Evidence needed | Trigger (when to decide) | Revision 2 note |
|---|---|---|---|---|---|---|---|
| P3-DEC-FGJ001 | Set a portfolio licensing policy for Echelon components (which stay PolyForm Noncommercial, which become permissive/open-core, which get self-serve paid commercial terms) | Keep all noncommercial until Unbound launch / Self-serve commercial terms for released developer components now / Permissive licence for selected libraries to build adoption and credibility | Decide policy now; publish self-serve commercial terms (no SLA) only for released developer components; keep DAF-specific and business-application repos closed to commercial use | High for new terms (existing grants persist) | Counsel review before publication; P3-GAP-FGJ004 | Before the first term sheet (CNV-GOV-007); owner act since Echelon Foundry owns all property (OD-P3-01) |  |
| P3-DEC-FGJ002 | Adopt an explicit "do not commercialize now" list (Vigila, Chrona, Summa, Signal, Mercatus, Fides, Arca, Tutela, Dokimos, echelon-knowledge-store, echelon-assurance and echelon-due-diligence as products; charity intelligence and Transitus as standalone products) | Adopt list / Evaluate case by case / Pursue several components in parallel | Adopt; revisit only when a named buyer brings a funded problem or Unbound reaches G2 | High | Inbound demand evidence; Unbound G2 | Revisit when a named buyer brings a funded problem or Unbound reaches G2 |  |

## 3. How the proposals fit together

- **Stop-or-continue chain.**
  1. P3-DEC-MOD003 and P3-DEC-CE002 hold spend until Gate 2 of [23](23-commercial-validation-roadmap.md).
  2. P3-DEC-MOD005 and P3-DEC-MOD004 together decide which break-even size Gate 2 must meet (revision 3, `gate-break-even.md`):
     - sponsor-performed review: 3,079 single-sponsor accounts or a 12,457-account partner book;
     - M5: 3,169 or 13,335;
     - risk-tiered attested review: 5,202 or 33,333;
     - Echelon-performed M1: not reached.
  3. P3-DEC-MOD001 and P3-DEC-CE001 decide when the clock starts and what it measures.
  4. If the gate is never met, the default is not to open a DAF cost center. Transitus continues (OD-P3-02), and so do the $0 archive (P3-DEC-HI004) and the build ledger (P3-DEC-AB003).
- **Partner protections** (P3-DEC-EK002, P3-DEC-FGJ003, P3-DEC-EK001) apply only once Gate 1 finds a partner. They are walk-away floors, and round-1 review expects partners to resist them ([12](12-institutional-distribution.md)).
- **No proposal changes an approved decision.** P3-DEC-CD001 refines DEC-001, and P3-DEC-HI002 implements DEC-003 within the 180-day ceiling, conditional on OD-CDD-02.

Decisions taken by the owner should be recorded in the organization record (P3-XRI-RECON003) and in this register's `decision_status` column, without deleting the proposal text.
