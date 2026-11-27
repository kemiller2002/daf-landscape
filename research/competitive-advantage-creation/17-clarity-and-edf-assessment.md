# 17 - Clarity and EDF assessment

Status: research (2026-11-26). Track M. Agent CE. This report applies the Clarity framework and the Echelon Diagnostic Framework (EDF) to the Phase III strategic choices. It proposes; it decides nothing. All twelve Phase II decisions stay at "strategically approved" (BRIEF status ladder); nothing here moves any of them up the ladder. Register rows: [claims.csv](data/fragments/CE/claims.csv) (P3-CLM-CE001..CE009), [hypotheses.csv](data/fragments/CE/hypotheses.csv), [decisions.csv](data/fragments/CE/decisions.csv) (P3-DEC-CE001..CE003), [evidence-gaps.csv](data/fragments/CE/evidence-gaps.csv), [validation-experiments.csv](data/fragments/CE/validation-experiments.csv). Working check: [sponsor_size_check.py](data/evidence/CE/sponsor_size_check.py) and its output [sponsor-size-check.csv](data/evidence/CE/sponsor-size-check.csv). The thesis and its invalidation conditions are in [21](21-commercial-thesis-invalidation.md).

**Independence caveat.** The Phase III reports, the model and this assessment were all produced by agents from the same model family. EDF's own calibration guidance says that several lenses from one source are not independent replications (EDF `docs/edf/diagnostic-calibration.md`). Nothing below is independent validation (P3-GAP-CE003).

**Revision 2 (2026-11-26, round-1 review; resolved by model revision 2).** Round-1 review disputed four model results (P3-CHL-REV2001, REV2002, REV1046, REV2011), and agent MOD has regenerated them:
- **Kill rule.** P3-CLM-MOD006 now reads: under the cost-center clock, A, A3, E, G and H all pause at month 24 in the base case, because the pilot must be one whole live Unbound customer. A3 passes only in the favourable case. The earlier claim, "A pauses and A3 passes", is withdrawn.
- **Payback (revision 3, CFO-corrected basis).** No single-sponsor sequence pays back within 120 months in the base case. Base A3 peak cash, uninterrupted, is $8.26M with Echelon performing the M1 deep review on demand, and $2.52M under M5, which is conditional on OD-CDD-02 (`key-figures.md`). The only payback is the partner-book sequence (SEQ-PB, P3-SEQ-MOD012) when the sponsor performs the deep review: +$4.18M at month 120, payback at month 76, peak $2.43M. Under M5 it pays back at month 80 (`bases.md`). Revision 2 gave $8.70M and $3.46M.
- **Kill rule.** With the cost center opened at month 0, every configuration pauses at month 24. In the Monte Carlo (rho 0.5), 94% of A3 draws pause, and the m120 median is −$507k, worse than doing nothing (`sequences-ranking.md`). Revision 2 gave 99% and −$539k. The month-24 result is a timing knife edge: with a whole first signing and a go-live lag of 8 months or less, A3's pilot comes at month 24 or earlier (`kill-timing.md`; P3-CHL-REV4009).
- **Break-even size depends on who performs the deep review** (P3-DEC-MOD005; `gate-break-even.md`):
  - Echelon performing M1: break-even not reached;
  - M1 risk-tiered (subject to counsel and V-9): 5,202 accounts;
  - the sponsor performing it: 3,079 accounts ($175k net);
  - M5: 3,169 accounts.

  Plausible sponsors (non-captive, not donation processors): 17 have 2,646 accounts or more and 10 have 5,291 or more. A3's reachable cap is 4 (`platform-classes.md`, `cap-sensitivity.md`). Revision 2 gave 10,963 accounts ($622k) under M1 and 3,949 ($224k) under M5.

Statements below that A3 passes the kill rule or pays back at month 62 are kept as history and marked "Revision 2" or "Revision 3" where corrected. Nacha TPSP status is established, not unknown: ratified CNV-PAY-001 makes Unbound a TPSP, so the annual Rules compliance audit is a base obligation (P3-CHL-REV3019). What remains unknown is the SOC 1 requirement and counsel's view of the functions performed.

## Answer in brief

1. **No Phase III strategic choice has reached diagnostic sufficiency for a cash or contractual commitment.** Evidence is sufficient for three kinds of action only:
   - $0 desk work;
   - owner-approved founder conversations at the $0-1k tier;
   - decisions *not* to do something, such as standalone charity intelligence, component products or administration. These are cheap to reverse, so a low evidence bar is appropriate.

   Every buyer-side and partner-side premise is untested (P3-CLM-CE007).
2. **Postures, using Clarity's own definitions.**
   - The entry sequence, the partner route and the capital plan are **Experimental now** and become **Strategic at a named commitment point**: the opening of the DAF cost center, a term sheet or a permissive licence grant.
   - The boundary rules are **Guardrail**: Echelon Foundry never becomes a sponsor, AI stays advisory, no redistribution of restricted data, the 180-day validity ceiling and the walk-away partner terms.
   - Exclusion lists are **Fast**.

   No strategic choice is yet in a Strategic commitment, so the immediate risk is drifting into one without the evidence Strategic posture requires. The likeliest routes are an exclusive or acquisition-option term sheet, or a cost center opened by default.
3. **EDF applies only where there is an observed outcome.** Six observed outcomes bear on the choices (section 3). Each needs EDF-1, or EDF-0 for the modelling artefacts. The forward-looking economics are model outputs, not observations, so EDF is **not applicable** to them. This follows the repository's validated precedent: DI-003 in [decision-intelligence-results-v1.json](../../data/decision-intelligence-results-v1.json) records `edfLevel: null` when there is no outcome to diagnose.
4. **The most important finding is a contradiction inside the Phase III evidence, found by an EDF-1 pass over the model's ranking.** The economically viable customer and the non-displacing customer are different populations.
   - **What A3 assumes.** Sequence A3, the only base-case payback in revision 1 (Revision 2: no sequence pays back in the base case; [14](14-commercial-sequencing.md)), assumes Phase II ER-7 revenue of $150-600k per customer, net of channel. ER-7 states that this means 3-10k-account sponsors at about $81 per account.
   - **How many such sponsors exist.** In the corrected FY2024 DAFRC panel (SRC-013) only **33** sponsors report at least 2,646 DAF accounts, and only **25** reach the 5,291 accounts that the $300k base implies. Revision 3: after excluding donation processors and sponsors presumed to run their own platform, 17 and 10 remain (`platform-classes.md`).
     - Of the 33: 19 are national standard sponsors, 5 donation processors, 4 religious, 3 single-issue and **2 community foundations**.
     - **No** university or hospital sponsor qualifies. The 134 in the panel hold **2,882 accounts in total** (P3-CLM-CE001, P3-CLM-CE002).
   - **What that implies.** A3's base case reaches about 18 live customers by month 120 (revision 1; revision 3 caps A3 at 4 reachable plausible sponsors, with 3.8 live at month 120, `cap-sensitivity.md`). It therefore implies either winning more than half of the qualifying universe, most of which is already served, or a partner whose whole book is the "customer".
   - **Why it matters.** The first reading is displacement, which the approved strategy avoids. The second reading turns A3 into H or E economics, and those do not pay back ([14](14-commercial-sequencing.md) §2). Revision 3 models that second reading directly as partner-book licensing (SEQ-PB). It is the only sequence that pays back, at month 76, and only when the sponsor performs the deep review (P3-DEC-MOD005).

   The model is internally correct; its revenue basis and the greenfield acquisition route (P3-DEC-CD001) cannot both hold (P3-CLM-CE003). This is the first thing V-2 and V-6 must settle (P3-DEC-CE002).
5. **The kill rule is a trigger without a calibrated trigger claim.** Under the rule, the Phase III Monte Carlo pauses A3 in **94%** of draws at rho 0.5 ([19](19-sensitivity-and-stress-analysis.md); revision 3; revision 2 gave 99%, revision 1 about 75%). In revision 1 most pauses came from the named-partner test, whose timing (P3-ASM-MOD034) has no evidence. Now that the pilot must be one whole live customer, the month-24 pilot test binds for every platform sequence in the base case ([14](14-commercial-sequencing.md) §7).
   - Clarity's decision architecture requires every significant trigger to state its monitoring signal, threshold, underlying trigger claim, owner, response and reassessment condition.
   - The kill rule has a signal and a threshold. Its trigger claim (no partner by month 6 means no partner route) and its reassessment condition are unstated, and the owner's question on the 24-month clock is still open ([01](01-approved-strategic-baseline.md) §2).
   - P3-DEC-CE001 proposes completing the trigger record before the cost center opens.

## 1. What the frameworks actually say, and how they were applied

**Versions read.** Clarity at `200a9eb`, read-only:
- `decision-posture-model.md`;
- `decision-architecture.md`;
- `decision-record.md`;
- `decison-loop.md`;
- `rules.md`;
- `principles/`;
- `docs/progressive-commitment.md`, `docs/reconsideration-criteria.md`, `docs/framework-interactions.md` and `docs/templates/clarity-result-template.md`.

EDF at `710d54c`, read-only:
- `README.md`;
- `overview.md` (superseded, per its own header);
- the v0.3 specification and model;
- `complexity-levels.md`;
- `diagnostic-calibration.md`.

Phase II recorded both frameworks as SRC-061 and SRC-062.

### 1.1 Clarity

- **Posture is set by two variables: impact if wrong and correctability.** Correctability means reversibility, recovery speed, recovery cost, who bears the consequences, and the ability to mitigate.
  - **Fast:** low impact, easily reversible.
  - **Experimental:** reversible but uncertain; the goal is learning, with constrained blast radius.
  - **Guardrail:** high impact, operationally constrained, limited correctability. It covers safety boundaries, regulatory requirements and financial control policies, and needs earlier intervention triggers.
  - **Strategic:** high impact and difficult to reverse. It needs deliberate analysis, senior ownership and an explicit reassessment plan.

  "Correctability determines speed. Impact determines rigor." A posture is not a probability or a confidence rating ([decision-intelligence-architecture-2026.md](../decision-intelligence-architecture-2026.md)).
- **Proportional certainty and progressive commitment.** Start with the minimum justified commitment. Escalate only when stated reconsideration criteria are met. Avoid both excessive rigor on correctable decisions and insufficient rigor on uncorrectable ones.
- **Decision architecture.** Ownership, authority boundaries, admissible evidence, triggers and failure signals must be designed before signals arrive. A trigger is "an operational hypothesis", not a permanent truth.
- **Decision readiness** has three invariant questions: what decision must be made now, what posture it needs, and who owns it. Phase II's readiness rule adds an accepted date, review cadence and outcome measure ([23](../competitive-displacement/23-executive-decision-register.md); SRC-062).

**A framework inconsistency that affects reproducibility (P3-CLM-CE008).** Three Clarity files draw the quadrant map differently:
- `decision-posture-model.md` puts Guardrail at high impact, on the higher-correctability side of the diagram, although its text says Guardrail correctability "is limited";
- `principles/decision-map.md` puts Experimental at high impact with high correctability and Guardrail at low impact with low correctability;
- `decision-map.md` reverses the correctability axis.

This report follows the **text** of `decision-posture-model.md`, which the framework calls its core model, together with its Type 1/Type 2 mapping (low correctability leads to Guardrail or Strategic). It always states impact and correctability explicitly, so a reader can re-map them if the framework owner settles the diagram differently (P3-GAP-CE002). Clarity is read-only here; no change is proposed to it.

### 1.2 EDF

- **What EDF is.** A diagnostic grammar for explaining an observed outcome:
  - System Context (Primary System, Context, Focus);
  - Outcome, Manifestations, Origin Network and Propagation;
  - Evidence, Control Points and their ranking;
  - Confidence, Diagnostic Sufficiency, Unknowns and Next Responsible Action.
- **Levels:**
  - **EDF-0** for a simple, local, low-consequence issue;
  - **EDF-1** when several origins are plausible or the consequence is moderate;
  - **EDF-2** for interacting systems, disputed origins, distributed control or high consequence.

  "Use the smallest depth that supports the next responsible action". Do not stay at EDF-0 when a material unknown could reverse a high-consequence action.
- **Diagnostic sufficiency** is "action-relative": the diagnosis is sufficient "when additional investigation is unlikely to materially change the next responsible action." It is not a certificate of truth.
- **Evidence boundary.** EDF's own record does not establish cross-executor reproducibility or superiority to neutral structure. Its confidence labels are qualitative, so EDF confidence below is qualitative too.
- **Application rule used here.** EDF is run only on **observed outcomes**, as Phase II did (SRC-061; Phase II [14](../competitive-displacement/14-alternative-enterprise-models.md) §4). Model projections, incumbent responses that have not happened and capabilities that are not built are not outcomes. For them, EDF is recorded as **not applicable**, as DI-003 does.

### 1.3 Output format

Each assessment follows the repository's validated v1 fields (`frameworkUse.edfLevel`, `reason`, `diagnosticSufficiency` stated as "yes for X / no for Y", and `clarityPosture` qualified by the commitment it applies to). It adds the brief's distinctions: established, suggested, unknown, must be tested, reversible, and long-term commitment.

## 2. Clarity readiness of the approved baseline

**What the owner has approved (2026-11-26).** The direction of DEC-001..DEC-012, with a date, so the first invariant question is answered.

**What remains open.** For every decision, `decision-approvals.csv` records the outcome measure, review cadence and reconsideration triggers as "proposed (agent), awaiting owner acceptance". So, under the readiness rule Phase II used, the approved decisions are ready as **direction** but not yet as **commitments**. Their failure signals are agent drafts, not accepted architecture (P3-GAP-CE001).

| Readiness element (Clarity) | State today | Consequence |
|---|---|---|
| Decision defined | Yes for DEC-001..012. No for the Phase III choices: they are proposals (P3-DEC-*) | Phase III choices cannot be committed until the owner decides them |
| Posture stated | Not recorded anywhere in the decision registers | This report supplies proposed postures (section 5) |
| Owner | "Owner" for strategic items. Phase II named role owners (product owner, Transitus owner) in [23](../competitive-displacement/23-executive-decision-register.md) | Adequate for a founder-led firm. Clarity requires roles, and the roles exist |
| Admissible evidence standard | Implicit in the V-1..V-9 pass rules | The rules are admissibility standards. Their cheaper variants in [04](04-low-cost-commercial-validation.md) weaken V-2, V-7 and V-9, and say so |
| Triggers with trigger claims | Kill rule: signal and threshold only | See section 6 and P3-DEC-CE001 |
| Failure signals | Drafted per decision, not accepted | P3-DEC-CE003 |
| Review | "At each gate" | Adequate once triggers are complete |

## 3. EDF diagnoses of the observed outcomes behind the choices

Each row is a compressed EDF record. Origins are those the cited evidence supports; none is invented to fill the network.

| # | Outcome (observed) | System Context (primary / context / focus) | Origin network (supported) | Evidence | Leading control point | Level and confidence | Diagnostic sufficiency | Key unknown |
|---|---|---|---|---|---|---|---|---|
| D1 | Better DAF technology has not displaced incumbents; institution-level switches cite integration, not price or exit terms | Sponsor platform choice / institutional DAF market / reasons to switch | Distribution and incentive alignment (RCF passes ~98% of fees to Ren, CLM-017); advisor channels add providers rather than replace them (CLM-018); integration as the stated reason (CLM-016) | 44 switch events (SRC-065); Phase II EDF | Channel and incentive position, not product features | EDF-1, reused from Phase II and not re-run. Medium | **Yes** for partner-first direction (DEC-001). **No** for predicting any particular partner's behaviour | Stayers' reasons (V-1) |
| D2 | Large education and health institutions rarely run DAF programmes, and the institutional segment's share is falling (1.38% to 1.11%) | Institutional sponsors / DAF market FY2021-24 / programme adoption | Free alternative: donors' national DAFs already pay the institution. Regulatory responsibility (4966/4967). Lack of sponsor apparatus. Technology rated low (P3-CLM-CD013) | 99 of 3,056 with any signal (P3-CLM-CD005); P3-CLM-CD004; panel accounts in total: 2,882 (P3-CLM-CE002) | Demand and free-alternative economics, not operating cost | EDF-1 (several plausible origins; no interviews). Low-Medium | **Yes** to stop treating education and health programmes as a primary *revenue* route. **No** to rule out them as an adoption route (P3-HYP-CD001 untested) | Rate of new programme launches (P3-GAP-CD010) |
| D3 | Small DAF-technology firms ended acquired, not licensed or expanded into platforms | DAF technology vendors / consolidating market / exit path | Platform owners control distribution; narrow tools sit off the system-of-record path (P3-CLM-CD018); funded acquirers (P3-CLM-EK009) | Pinkaloo, Amicus, Vennfi (CLM-025); 10 acquisitions in P3-CLM-EK009 | Contract terms: change of control, non-exclusivity, data continuity (P3-DEC-EK002, P3-DEC-FGJ003) | EDF-1. Medium | **Yes** for setting walk-away partner terms (Guardrail). **No** for predicting whether Unbound would be acquired | Terms in TIFIN-SEI and similar deals (P3-GAP-EK004) |
| D4 | Phase II's capital figure ($6.5M P50) is several times Phase III's lean reconstruction ($1.0-1.5M cash base; Revision 2: the model's S3 cash to first invoice was $2.12M base under M1; revision 3 gives $1.83M) | Capital model / Phase II package / why the number is high | Conventional run rate from month 1 (P3-CLM-AB003); build-period burn counted twice (P3-CLM-AB004); channel share possibly counted twice (P3-CLM-AB005, P3-CLM-MOD003); overlapping G0-G1 and ER-7 (P3-CLM-AB006) | Exact reproduction of `Routes.fs` (P3-CLM-AB001) | Model structure (run-rate lines) | EDF-0. Origins are mechanical and reproduced. High for the mechanics | **Yes** to stop using $6.5M as the cost of commercializing a *completed* Unbound. **No** to treat $1.0-1.5M as a budget: every input is an assumption | Owner's real run rate and funding (P3-GAP-AB006, P3-GAP-MOD001) |
| D5 | Model outcome (revision 1): only A and A3 pay back. E, G and H fail even on a lean run. Revision 2: no sequence pays back within 120 months in the base case; the break-even customer is 10,963 accounts (M1) or 3,949 (M5, conditional). Revision 3: break-even depends on who performs the deep review (3,079 accounts if the sponsor does; not reached if Echelon performs M1); only partner-book licensing with sponsor-performed review pays back (month 76) | Phase III sequence model / ten-year cash / why payback differs | Revenue per customer basis: ER-7 assumes $150-600k net per customer; FGJ and CD assume $25-150k per sponsor (P3-GAP-MOD003). The A3 basis implies sponsors of 2,646-10,582 accounts, and only 33, 25 or 15 exist (P3-CLM-CE001) | `sequences-ranking.md`; `tornado-sequence-a3.md` (revenue per customer is the top driver, P3-CLM-MOD010); [sponsor-size-check.csv](data/evidence/CE/sponsor-size-check.csv) | Revenue per customer, set by customer size: a gate in V-2 and V-6 | EDF-1. Medium. The count is direct; reachability is inferred | **Yes** to require that V-2 and V-6 test revenue per customer at a named sponsor size before any sequence commitment. **No** to choose between A3 and E | How many of the 33 are reachable without displacement; whether a partner's aggregated book can be the customer (P3-HYP-CE002) |
| D6 | No design partner is available (Unbound OD-M-14), and no partner has been named | Unbound commercialization / partner-first strategy / partner availability | No outreach has been authorized: absence of search, not of interest. Vendor-viability concerns (P3-HYP-AB003) are untested | P3-CLM-AB017 | Owner approval of founder-led outreach at the $1k tier (P3-DEC-AB002) | EDF-0. The outcome is explained by no search having been made. Medium | **Yes** to treat "no partner" as uninformative until a search has run. **No** to read it as market rejection | Partner interest (V-6) |

What EDF is **not** applied to, and why:
- incumbent response scenarios ([13](13-incumbent-response-model.md)): none has happened against Unbound;
- persistence of the architectural advantages ([07](07-architectural-competitive-advantages.md)): nothing is built (P3-GAP-EK008);
- adjacent-industry potential ([08](08-adjacent-financial-industries.md)): no outcome;
- sequence economics beyond D5's revenue-basis question: these are projections.

For these, Clarity's reasoning about posture and evidence applies, and EDF does not.

## 4. Assessment by strategic domain

Abbreviations:
- **Est.** = established. A verified fact or an exact reproduction.
- **Sugg.** = suggested. Inference or a model result on assumed inputs.
- **Unk.** = unknown.
- **Test** = must be tested before commitment.
- **Rev.** = reversible, with Clarity correctability.
- **LTC** = long-term commitment created.

### 4.1 Commercial entry strategy

| Element | Assessment |
|---|---|
| Decision now | Not "which sequence to commit to", but (a) whether completing Unbound sits inside existing operations or opens the DAF cost center (P3-DEC-MOD001), and (b) whether to authorize partner discovery |
| Est. | Unbound is at S2 (requirements, an `Echelon.Execution` slice, replay tooling), not S3 (P3-CLM-EK005, P3-SRC-AB016). The kill rule pauses A, A3, E, G and H at month 24 in the base case; A3 passes only in the favourable case (P3-CLM-MOD006, Revision 2; previously "pauses A from S2 and passes A3 from S3"). Narrow-tool sequences B, C, D and F do not fund Unbound (P3-CLM-FGJ019, P3-CLM-MOD007) |
| Sugg. | Base A3 peak cash is $8.26M with no payback in 120 months (M1, Echelon performing, demand-driven), and $2.52M under M5, which is conditional on OD-CDD-02. Partner-book licensing with the sponsor performing the deep review pays back at month 76 ([16](16-capital-efficient-market-entry.md); Revision 3: revision 2 gave $8.70M and $3.46M; Revision 2: previously "A3 is the cheapest route to a base-case payback (peak $1.24M corrected, payback month 62)"). Customer funding lowers peak cash more than partner funding (P3-CLM-MOD011) |
| Unk. | Whether A3's customers exist without displacement (P3-CLM-CE003); when S3 is reached and at what cash (P3-GAP-CE004); partner timing (P3-GAP-MOD002) |
| Test | V-6 with revenue per customer at a named size; V-2; a ledger of S2 to S3 hours and cash (P3-DEC-AB003) |
| Rev. | High until the cost center opens or a term sheet is signed. Founder time spent is unrecoverable but small per month |
| LTC | Opening the cost center starts the kill clock. A term sheet binds the partner terms |
| Posture | Impact high; correctability high now and low after the term sheet. **Experimental now, Strategic at the term sheet** |
| EDF | D5, D6 (EDF-1, EDF-0). Sufficient for the $0-1k tier and for excluding B, C, D and F as funding routes. Not sufficient for choosing A3 over E or for opening the cost center |
| Reconsider if | [21](21-commercial-thesis-invalidation.md) TI-01, TI-02, TI-06 |

### 4.2 Capital allocation

| Element | Assessment |
|---|---|
| Decision now | Whether to authorize spend beyond $0, and the cap (DEC-008; P3-DEC-AB001, P3-DEC-AB002) |
| Est. | Phase II's $6.5M mixes overlapping simulations and a conventional run (D4). Modelled amounts are not approved expenditures (DEC-008 condition) |
| Sugg. | Cash to first invoice from S3 is $384k / $1.83M / $6.63M (revision 3; [16](16-capital-efficient-market-entry.md); Revision 2 gave $542k / $2.12M / $7.12M; revision 1 gave $256k / $1.05M / $4.39M). Validation for the G0 tests costs about $0-24k cash ([04](04-low-cost-commercial-validation.md); Revision 2: previously "about $1-25k") |
| Unk. | Owner funding capacity (P3-GAP-MOD001); insurance at $5M limits (P3-GAP-AB001); SOC 1 need (P3-GAP-AB005); counsel on the TPSP functions performed (P3-GAP-AB003). Revision 2: the TPSP role itself is established by CNV-PAY-001 |
| Test | Owner runway statement ($0, now); broker indications ($0) |
| Rev. | Cash spent is unrecoverable. Under the kill rule, A3's stress cases lose about $0.46-1.34M (`extremes-kill-rule.md`); a conventional run rate is the exception ($4.52M peak). Revision 3: base loses $1.38M at the month-24 pause; the stress cases range from $731k (zero customers) to $2.97M (aggressive incumbent plus partner acquired); the founder paid at market costs $1.82M |
| LTC | None below a term sheet; the binding of SOC 2 and insurance at the term sheet (P3-DEC-AB004) |
| Posture | **Fast** for the $0 tier (no cash; reversible). **Experimental** for $1k-10k (blast radius capped). **Strategic** for opening the cost center or for any spend above $25k, which assumes a term sheet. Proportional certainty: Phase II's G0 of $150-350k bought less decision value per dollar than the $10k tier ([04](04-low-cost-commercial-validation.md) §2) |
| EDF | D4 (EDF-0): sufficient to retire $6.5M for a completed Unbound; not sufficient to set a budget |
| Reconsider if | TI-05, TI-07 |

### 4.3 Organizational design

| Element | Assessment |
|---|---|
| Decision now | Founder-led, agent-assisted licensor with no hires before elimination tests (business plan §11, P3-SRC-AB009) |
| Est. | Phase II burn assumed CEO and CTO at market, sales and support from month 1 (P3-CLM-AB003). Non-negotiable obligations remain: SOC 2 at contract, a second maintainer before regulated reliance (CNV-PLT-010), insurance limits set by buyers, counsel ([02](02-existing-unbound-economics.md) §3) |
| Sugg. | Lean run of $165k / $465k / $1.07M a year (P3-HYP-AB001) |
| Unk. | Whether partners accept a single-founder vendor (P3-HYP-AB003); whether a partner carries first-line support (P3-HYP-AB002) |
| Test | V-6 conversations: vendor-viability objections; support split in the term sheet |
| Rev. | Highly correctable while no one is hired. Key-person dependence has poor correctability for the *customer* (consequences land on others), which Clarity counts against correctability |
| LTC | A second-maintainer contract and escrow, once a sponsor relies on Unbound |
| Posture | **Experimental** for the lean model. **Guardrail** for continuity controls (escrow, second maintainer, runbooks): they protect third parties and must be in place before the first live sponsor |
| EDF | Not applicable (no outcome yet). D4 diagnoses the old assumption only |
| Reconsider if | TI-07, TI-08 |

### 4.4 Product boundaries

| Element | Assessment |
|---|---|
| Decision now | What Unbound is, and what it must never be |
| Est. | Echelon Foundry must not become a sponsor (BRIEF); no proprietary payment network (DEC-009); AI is advisory (DEC-005); no non-redistributable data in shared layers (DEC-004); the 180-day validity ceiling (DEC-003); custodial administration deferred (DEC-002). Statutory sponsor eligibility: financial institutions and for-profits cannot sponsor (P3-CLM-CD001; counsel to confirm) |
| Sugg. | Adjacent modules (planned giving, fiscal sponsorship) only after a live sponsor ([08](08-adjacent-financial-industries.md); P3-SEQ-FGJ005). The registry belongs inside Unbound, not as a standalone product (P3-DEC-HI003) |
| Unk. | Whether hosted-programme role allocation works legally (P3-GAP-CD006) |
| Test | Counsel review at the $25-50k tier, only when a partner model is known |
| Rev. | The exclusions are highly correctable; they can be lifted later. Crossing a boundary is not: becoming a sponsor or administrator, or redistributing restricted data |
| LTC | Any boundary crossing |
| Posture | **Guardrail** for the boundary rules (control policies with low correctability if breached). **Fast** for exclusion lists. **Strategic** for adding an adjacent module |
| EDF | Not applicable |
| Reconsider if | A signed anchor plus licensing evidence (DEC-002 gate); counsel findings |

### 4.5 Shared infrastructure

| Element | Assessment |
|---|---|
| Decision now | The allocation rule for pooled cost across the five economic entities (P3-DEC-MOD002) |
| Est. | No other Echelon product earns revenue, so under a revenue rule Unbound bears about 98% of pooled cost (P3-CLM-MOD009). The Echelon components are PolyForm Noncommercial with commercial terms "forthcoming" (P3-CLM-FGJ002). Vigila is a task organizer, not audit logging (P3-CLM-FGJ001) |
| Sugg. | Sharing lowers engineering cost, not compliance, sales or support cost ([08](08-adjacent-financial-industries.md) §3). The S7 factor of 0.6 is one point in a rule-dependent range |
| Unk. | Whether any second product will earn revenue |
| Test | None at $0 beyond choosing the rule |
| Rev. | High. It is an accounting rule. But changing it after the kill rule has been evaluated would change whether the rule fired |
| LTC | None |
| Posture | **Fast** for choosing the rule, with one Guardrail condition: fix it **before** the cost center opens, so the viability test cannot be moved by reallocating cost afterwards (Clarity constitution: change only "to reduce ambiguity, never to admit convenience") |
| EDF | Not applicable |
| Reconsider if | A second product earns revenue |

### 4.6 Competitive advantages

| Element | Assessment |
|---|---|
| Decision now | What to build to hygiene level and what, if anything, to market as a differentiator (P3-DEC-EK003) |
| Est. | No candidate is built or measured (P3-GAP-EK008). Of 22 candidates none is a demonstrated architectural, distribution or network advantage (P3-CLM-EK006). Several capabilities claimed as distinctive are public at competitors: Chariot idempotency, Daffy and Chariot MCP, Ren automated vetting ([07](07-architectural-competitive-advantages.md) §3) |
| Sugg. | The strongest candidates (EK017 replay; EK010 reconciliation-proved migration) are copyable in about 6-30 months (P3-CLM-EK017) |
| Unk. | Willingness to pay for replay (P3-HYP-EK001); incumbent internals (P3-GAP-EK001) |
| Test | V-3 replay at $0; partner and stayer valuation in V-1 and V-6 |
| Rev. | High for building to hygiene level. Public differentiation claims are poorly correctable once made to buyers and found matched |
| LTC | None |
| Posture | **Fast** for "do not position ordinary capabilities as differentiators". **Experimental** for investing in EK017/EK010 beyond hygiene, gated on V-3 and partner valuation |
| EDF | Not applicable: no outcome (a capability that does not exist cannot be diagnosed). D1 shows the binding constraint lies elsewhere |
| Reconsider if | TI-10 (incumbent parity before the first pilot) |

### 4.7 Market selection

| Element | Assessment |
|---|---|
| Decision now | Which customer population A3's revenue depends on |
| Est. | Community foundations are not greenfield: 95% of those with $50M or more are already in the panel. Education and health institutions are greenfield by count but hold 2,882 DAF accounts in total across 134 panel sponsors (P3-CLM-CE002). Only 33 sponsors hold 2,646 accounts or more (P3-CLM-CE001) |
| Sugg. | Small programmes are viable for the programme owner when hosted, but not for the vendor except through a channel (P3-CLM-CD011, P3-CLM-CD012). E, G and H do not pay back (P3-CLM-MOD007) |
| Unk. | Reachability of the large-sponsor universe without displacement; aggregated partner books (P3-HYP-CE002) |
| Test | P3-VAL-CE001 ($0): classify the 33 by current platform and contract window using V-5 desk methods |
| Rev. | High. Targeting is a plan, not a contract |
| LTC | None until a partner or design partner is named |
| Posture | **Experimental** |
| EDF | D2 and D5 (EDF-1). Sufficient to demote education and health programmes from primary revenue route. Not sufficient to pick a segment for spend |
| Reconsider if | TI-01, TI-11 |

### 4.8 Customer acquisition

| Element | Assessment |
|---|---|
| Decision now | Whether P3-DEC-CD001 (host-sponsor programme route) is the primary acquisition route |
| Est. | Narrow DAF-tech offerings have been absorbed rather than expanded (CLM-025). Candid prices charity data from $2,750 (P3-CLM-AB020). Free migration scoping is table stakes (CLM-021) |
| Sugg. | Narrow offerings lead to the platform only if they sit on the system-of-record path and are bought by the same budget owner (P3-CLM-CD018) |
| Unk. | Host willingness (P3-HYP-CD002); programme demand (P3-HYP-CD001); partner-sourced deal rate (P3-HYP-FGJ004) |
| Test | V-6 host conversations; V-1 |
| Rev. | High |
| LTC | Programme templates only |
| Posture | **Experimental**. P3-DEC-CD001 and the model's revenue result conflict, so adopting CD001 as the *primary revenue* route is not justified yet. As an adoption and reference route it is (P3-DEC-CE002) |
| EDF | D3 and D5 (EDF-1) |
| Reconsider if | TI-04, TI-11, TI-12 |

### 4.9 Distribution

| Element | Assessment |
|---|---|
| Decision now | Minimum partner terms (P3-DEC-FGJ003, P3-DEC-EK002) before any conversation reaches a term sheet |
| Est. | Fee pass-through and acquisition precedents (CLM-017, CLM-025, P3-CLM-EK009). Channel benchmarks: billing ~3%, referral 15-20%, resale and support 20-40% ([12](12-institutional-distribution.md) §1) |
| Sugg. | Partner-first buys access, not lower CAC (P3-CLM-FGJ009). The lean licensor survives price responses but not loss of channel (P3-CLM-MOD013) |
| Unk. | Every partner term (P3-GAP-AB004, P3-GAP-FGJ001) |
| Test | V-6; P3-HYP-FGJ005, P3-HYP-EK006 |
| Rev. | High before signature; low after (exclusivity, ROFR, change of control) |
| LTC | The partner contract |
| Posture | **Experimental** for conversations. **Guardrail** for the walk-away terms (predefined boundaries, set before the signal arrives). **Strategic** at signature |
| EDF | D1 and D3 (EDF-1). Sufficient for the walk-away terms; not sufficient to forecast partner yield |
| Reconsider if | TI-02, TI-03, TI-09 |

### 4.10 Risk management

| Element | Assessment |
|---|---|
| Decision now | Is the kill rule designed as decision architecture? |
| Est. | The rule as approved: no named partner by month 6, or no referenceable live pilot by month 24 (CHL-022). Clock start: the cost-center month (OD-P3-03, OD-P3-04). Transitus is exempt (OD-P3-02) |
| Sugg. | The rule bounds the downside better than the cost structure does (P3-CLM-MOD010; [19](19-sensitivity-and-stress-analysis.md)) |
| Unk. | Calibration of the named-partner threshold (P3-ASM-MOD034, no evidence); whether OD-P3-03/04 starts the 24-month clock |
| Test | Not testable before a search runs. Its calibration is learned from the first partner search (Clarity Loop, step 8) |
| Rev. | Pausing is reversible. Restarting after a pause has some cost. A rule redefined after the clock starts loses its protective value |
| LTC | None |
| Posture | **Guardrail**: a financial control policy that must be defined before signals arrive |
| EDF | Not applicable to the rule. D6 (EDF-0) explains why "no partner" carries no information yet |
| Reconsider if | Section 6 |

### 4.11 Evidence sufficiency

| Element | Assessment |
|---|---|
| Est. | All buyer, partner and price inputs are ASSUMPTION or INFERENCE (P3-ASM-AB030, P3-ASM-FGJ001..FGJ017, P3-ASM-MOD034). No V-test has run. The model is reproducible and tested; that establishes arithmetic, not inputs ([18](18-economic-model-methodology.md)) |
| Sugg. | The highest value per dollar is in V-1 and V-6 at about $0-1k cash, which needs owner approval rather than budget ([04](04-low-cost-commercial-validation.md) §3) |
| Calibration review (Clarity result template) | Effort has run ahead of evidence in one place: ten-year sequence economics and Monte Carlo runs on a revenue basis that a $0 desk count (P3-CLM-CE001) puts in question. Effort is proportionate elsewhere: the registry and event models rest on public-data measurements (P3-CLM-HI011) |
| Posture | Diagnostic sufficiency is reached for: the $0 tier; requesting approval for outreach; exclusion decisions; walk-away terms. It is not reached for: opening the cost center; choosing a primary revenue segment; signing partner terms; spending above $10k |

### 4.12 Reversibility

| Commitment | Correctability | Why |
|---|---|---|
| $0 desk work; exclusion lists; allocation rule; postures | High | No external party relies on them |
| Founder outreach (owner-approved) | High | It creates expectations but no obligations. Reputational correctability is moderate if commitments are implied |
| Cost-center opening | Moderate | Starts the clock. Spend is unrecoverable, but capped by the rule |
| SOC 2 and insurance binding | Moderate | Recurring cost, cancellable |
| Partner term sheet with exclusivity, ROFR or acquisition option | **Low** | Binds for the contract life ([12](12-institutional-distribution.md) §4) |
| Permissive (open) licence of a component | **Very low** | Granted rights persist (P3-DEC-FGJ001) |
| Live sponsor on Unbound | **Low** | The consequences fall on the sponsor and its donors. It needs the continuity guardrails in 4.3 and P3-XRI-FGJ001 |
| **Not** archiving IRS and sanctions releases | **Very low (inaction)** | Sources overwrite history; replay evidence cannot be recreated (P3-DEC-HI004). Clarity's correctability applies to inaction too, which makes starting the archive a **Fast** decision with an irreversible downside if delayed |

### 4.13 Strategic optionality

| Element | Assessment |
|---|---|
| Est. | Transitus continues regardless of the kill rule (OD-P3-02). Echelon Foundry owns all IP (OD-P3-01), so a future servicing entity would license, not own. OD-M-05 stays as a destination (DEC-001) |
| Sugg. | A3 keeps every later sequence open and commits cash only at the term sheet ([14](14-commercial-sequencing.md) §7). Sale to an acquirer is a plausible outcome to value deliberately ([12](12-institutional-distribution.md) §4; [13](13-incumbent-response-model.md) §5) |
| Unk. | The owner's goals between independent niche and sale (P3-GAP-AB006) |
| Posture | Optionality is preserved by keeping decisions Experimental until a named counterparty exists. The options most easily destroyed are a partner's exclusivity or ROFR, a permissive licence, and opening the cost center before S3 (A's kill-rule pause) |
| EDF | Not applicable |

## 5. Decision table for the main strategic choices

Impact and correctability use the Clarity decision-record scales. "Posture now" applies to the decision that must be made now; "at commitment" applies to the later binding step.

| Choice | Options | Evidence state | Impact if wrong | Correctability now / at commitment | Posture now → at commitment | EDF level; diagnostic sufficiency | Next responsible action | Commitment point |
|---|---|---|---|---|---|---|---|---|
| Entry sequence | A3; A; E (host factory); G; H; B, C, D, F; partner book (PB, revision 3) | Est.: A, A3, E, G and H pause at month 24 in the base case; A3 passes only in the favourable case (P3-CLM-MOD006, Revision 2); B, C, D and F do not fund Unbound. Sugg.: no base-case payback within 120 months (Revision 2: previously "A pauses and A3 passes the kill rule ... A3 pays back at month 62"). Contradicted in part: A3's customer universe is 33 or fewer sponsors (P3-CLM-CE001) | High (founder decade; $1-5M) | High / Low | **Experimental → Strategic** | D5 EDF-1. **Yes** to drop B, C, D and F as funding routes and to make revenue per customer a V-2/V-6 gate. **No** for A3 versus E | P3-VAL-CE001 ($0); V-6 with a size question; ledger S2→S3 | Cost-center opening; term sheet |
| A3 versus A (timing of completion) | Complete Unbound inside existing operations, then open the cost center; or open it now | Est.: kill-sensitivity table. Unk.: S2→S3 cash and time (P3-GAP-CE004) | High | High / Moderate | **Guardrail** (trigger definition) | Not applicable (definition, not diagnosis) | Owner decides P3-DEC-MOD001 and P3-DEC-CE001 together | First DAF-specific spend |
| Licensing versus administration | License (DEC-006); custodial administration (DEC-002 deferred) | Est.: administration break-even about $1.9-2.3B; a 40% fee response erases the $11-71 advantage (P3-CLM-EK008). Unk.: V-2 prices | Critical if administration chosen wrongly | Deferral: high. Forming an administrator: very low | **Fast** to keep the deferral; **Strategic** to reopen | D1 EDF-1; **yes** for deferral | None; keep DEC-002 gates | A signed $0.5-1.0B anchor (DEC-002) |
| Partner versus direct | Partner-first (DEC-001); direct licensing (ER-4); OD-M-05 later | Est.: precedents D1, D3. Sugg.: partner buys access, not cost (P3-CLM-FGJ009). Unk.: all partner terms | High | High / Low after signature | **Experimental; Guardrail terms → Strategic** | D1, D3 EDF-1; **yes** for walk-away terms; **no** for yield | Owner approves the $1k outreach tier; adopt P3-DEC-FGJ003 and P3-DEC-EK002 as preconditions | Term sheet |
| Primary revenue customer (new) | Large sponsors at ER-7 scale; partner's aggregated book; hosted programmes | Contradiction (P3-CLM-CE003) | High | High / Moderate | **Experimental** | D2, D5 EDF-1; **yes** to require the gate; **no** to choose | P3-DEC-CE002 | Before any sequence commitment |
| Components to commercialize | Self-serve no-SLA terms for released developer tools; modules inside Unbound; do-not-commercialize list; permissive relicensing | Est.: licences are noncommercial and terms "forthcoming" (P3-CLM-FGJ002); revenue $0-50k a year (P3-CLM-FGJ019) | Low-Moderate (revenue). Moderate (focus) | High for terms and the exclusion list; **very low** for permissive grants | **Fast** (exclusion list; no-SLA terms); **Strategic** (permissive grants) | D3 EDF-1; **yes** to exclude standalone products | Decide P3-DEC-FGJ001 before the first Unbound term sheet (commercial terms are a precondition, CNV-GOV-007) | First commercial grant |
| Charity intelligence | Inside Unbound; low-price partner add-on; standalone product | Est.: Candid from $2,750 (P3-CLM-AB020). Sugg.: standalone adds about $197k of overhead (P3-CLM-HI015) | Moderate | High | **Fast** (do not pursue standalone) | Not applicable; no outcome | Start the archive now (P3-DEC-HI004) | — |
| Adjacent industries | Planned giving and fiscal sponsorship desk work; build | Sugg. only (P3-HYP-FGJ001, FGJ002) | Moderate | High (desk) / Low (build) | **Fast** (desk) → **Strategic** (build) | Not applicable | None until a live sponsor exists | A live sponsor asks |
| Kill-rule architecture (new) | Signal and threshold only (today); full trigger record | Est.: 94% of A3 draws are paused under the rule (rho 0.5; revision 3; revision 2: 99%; revision 1: about 75%, mostly at an uncalibrated named-partner month) | High (it decides whether the thesis is tested at all) | High until the clock starts; low after | **Guardrail** | Not applicable | P3-DEC-CE001 | Cost-center opening |

## 6. The kill rule as Clarity decision architecture

Clarity requires each significant trigger to state the fields below. The kill rule is the most important trigger in the package. Proposed completion (P3-DEC-CE001; owner decision required):

| Field | Named-partner test | Referenceable-pilot test |
|---|---|---|
| Monitoring signal | A named channel partner or design-partner customer in term-sheet talks, with a pilot customer identified (V-6 pass rule) | A live sponsor on Unbound that has passed a buyer security review and agrees to be referenced |
| Threshold | Cost-center month + 6 | Cost-center month + 24 (if the owner confirms OD-P3-03/04 applies; open, [01](01-approved-strategic-baseline.md) §2) |
| Underlying trigger claim (state it; it is a hypothesis) | "If no partner engages within six months of a funded search, the partner route is unavailable rather than slow" (P3-HYP-CE001) | "If no live referenceable pilot exists 24 months after the cost center opens, procurement and implementation barriers exceed what a lean licensor can overcome" |
| Owner | Owner (Echelon Foundry) | Owner |
| Operational response | Pause DAF cost-center spend; Transitus continues (OD-P3-02); keep the $0 archive running | Pause platform spend beyond Release 1; keep existing licences |
| Reassessment response | Review whether the search was actually run: number of partners contacted, conversations held, stage reached | Review whether the gap was demand or delivery |
| Trigger reassessment condition | Recalibrate the six-month threshold only on evidence from the search itself: e.g. ≥2 partners in active diligence at month 6 with a stated decision date. Never recalibrate because spend has already been made | Recalibrate only on a signed pilot with a dated go-live |
| Guard against drift | The cost-center month, the allocation rule (P3-DEC-MOD002) and the trigger fields are fixed **before** the first DAF-specific spend. Later changes only reduce ambiguity (Clarity constitution, revision ethic) | Same |

Why this matters: the model shows that a cost center opened later converts A's pause into a pass, "at the price of more cash before any test" ([14](14-commercial-sequencing.md) §6). Without a stated trigger claim, moving the clock reads as calibration when it is actually a weaker control. The owner's definition (OD-P3-04) is sound. The risk is in applying it after the fact.

## 7. Limits

- **Clarity's diagrams disagree** (section 1.1). Posture labels here rest on the core model's text.
- **EDF's performance claims are unvalidated** by EDF's own record. EDF is used here as a structure for making diagnoses explicit, not as evidence that they are right.
- **The sponsor-size check is a count, not a forecast.**
  - DAF account counts are Schedule D figures from a corrected panel (SRC-013).
  - Some large "sponsors" are donation processors whose accounts are not comparable DAFs.
  - Price per account could be higher than $81. The table shows $120 and $150; the conclusion holds.
  - A partner's aggregated book could be the paying customer. That is a different model, and it is not the ER-7 one.
- **No independent review** (P3-GAP-CE003).
