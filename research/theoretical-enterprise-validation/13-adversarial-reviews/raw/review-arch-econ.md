# Role-separated review: architecture and economics

**Scope.** Theoretical enterprise validation artifacts under `/home/user/daf-landscape/research/theoretical-enterprise-validation/` (02, 03, 05, 06, 14, 15, 16), checked against the baseline in `/home/user/daf-landscape/research/ai-native-daf-enterprise/` (09 financial models + `outputs/parameter-register.csv`, 02 organization model, DECISION-LOG). No files under `/home/user/daf-landscape` were modified. All arithmetic is by hand and shown.

**Caveat.** This is a role-separated critique by the same model family that wrote the artifacts. It is not independent validation. Shared blind spots are likely.

Severity: 5 = would change a headline conclusion or create a control gap with money or legal exposure; 4 = materially wrong number or design defect; 3 = internal inconsistency that would mislead a reader or builder; 2 = weak support or imprecision; 1 = editorial.

---

## Part A: Enterprise architect

### A1. The SoD "graph-colouring" floor is not a derivation (03 §4, TVC-018). Severity 3
- **Claim:** a graph-colouring view of SoD-1..9 plus TVR-ORG-003 gives "at least 4 operational people", and therefore ~6–8.
- **Problem:** the constraint graph listed has these edges: profile approver–releaser, releaser–reconciler, author–publisher, raiser–decider, granter–user, write-off approver–break owner, agent owner–model-risk, sanctions officer–grant approver. Even with reconciler = break owner, this gives one path (profile approver–releaser–reconciler/break owner–write-off approver) plus disjoint edges. The graph has no odd cycle, so it is bipartite and **2 colours suffice**. The "4" does not follow from the stated constraints. The real drivers of the floor are absence cover, competence (counsel, sanctions officer), board and internal audit, and fractional roles. Those are assumptions (TVA-022), not graph theory. So the agreement with the 8–10 floor is a coincidence.
- **Correction:** drop the graph-colouring claim. State the floor as: SoD minimum of 2, plus named competence roles, plus two-deep cover, all labelled [A].

### A2. TVC-018 is a category error, not a contradiction (16, TVC-018). Severity 2
- **Claim:** "~20 at any scale" (Clarity) contradicts the "8–10" floor (org model).
- **Problem:** the baseline AI-native model outputs **21 FTE at 1k accounts** (`fte-by-role.csv`: 5+1+1+2+1+4+4+1+1+1). The "8" in Economics.fs is the **conventional comparator's** floor (scale table: "8 (floor)"). The 8–10 figure is the accountability minimum for a self-operated sponsor. The ~20 figure is the AI-native model's role floors, which include engineering (4) and agent ownership (4). The two numbers measure different things.
- **Correction:** reclassify TVC-018 as a definitional note. The real question is whether 4 engineers plus 4 agent owners are floors at 1k accounts. The baseline already concedes they are not ("At 1k, buy rather than build").

### A3. The ontology contradicts its own rule ONT-1 (02 §1 vs ONT-1). Severity 3
- **Claim:** ONT-1 says "Party ≠ relationship ≠ authority … each capacity is a separate edge".
- **Problem:** the entity catalog lists Donor, Advisor, Investment advisor, Authorized representative and Successor/beneficiary as **entities**, each with its own lifecycle and owner. Under ONT-1 they are capacities (edges) on a Party. "Successor / beneficiary" also merges persons (successor advisors) with organizations (beneficiary charities).
- **Correction:** model Party, Relationship(capacity, evidence, effective period) and AuthorityGrant as the entities. Move the role rows to a capacity table.

### A4. The "Owner (sole writer)" column is not sole (02 §1). Severity 3
- **Problem:** several rows name two writers or a non-system writer:
  - Fund: "Account service + ledger";
  - Investment advisor: "C1.2 + C2.4";
  - Reservation: "Ledger/treasury";
  - Compliance determination: "Grants compliance / sanctions officer (H) or rule", which mixes the accountable human with the system of record;
  - Holding: "Custodian (external)".
  The column then cannot support DATA-07 field-level source-of-truth rules. The org doc repeats this by assigning ADM-15 to "C2.5 + C3.3".
- **Correction:** separate three columns: system of record (one); accountable role (one); external authority (for observations).

### A5. Grant and payment-attempt machines duplicate the same facts (06 §2–3). Severity 3
- **Problem:** the grant machine has PaymentInProgress, Disbursed, Final and Returned. These mirror the attempt states (Submitted/Accepted, Settled, Returned). Two state machines record one fact, so they can diverge. That is the class of defect the program criticises elsewhere (TVC-008).
- **Problem:** returns are handled two ways depending on an internal bookkeeping step:
  - before `Reconciled`, a return is a grant transition (`Final → Returned`);
  - after `Reconciled`, it is a child record (SM-0).
- **Problem:** `Final → Reconciled` delays the three-way match until the return window has elapsed. Daily reconciliation will then show every Disbursed-not-Final grant as unmatched, or the machine is ignored in practice.
- **Correction (simpler):**
  - the grant holds decision, reservation and funding;
  - payment status is **derived** from the attempts (PA-1 already gives the rules);
  - reconciliation is a matching fact on attempts and journals, not a grant state;
  - finality is a time-derived attribute.

### A6. A definite defect in the payment-attempt machine (06 §3). Severity 3
- **Problem:** the machine has `Settled → Voided: check only, before presentment`, but PA-4 says "A check is Settled … only when presented and cleared. 'Issued' is Accepted." A check cannot be both settled and not yet presented.
- **Correction:** `Accepted → Voided` (check, before presentment). Add `Accepted → Escheated` through `CheckAged`.

### A7. The late-return example is for the wrong rail direction (06 §2). Severity 2
- **Problem:** the machine has `Final → Returned: late return (rail allows, e.g. unauthorized-debit class)`. Grant payments are ACH **credits** originated by the sponsor. Unauthorized-debit returns apply to debits, which is the contribution side (CW-27), not grants.
- **Correction:** cite a credit-side late return, or a recipient refund (CW-25) as a separate child case, or drop the example.

### A8. GR-4 contains a dead rule (06 §2). Severity 1
- **Problem:** GR-4 says a reservation is released on "`Declined` (if reserved)". No transition reaches Declined after Reserved, so the rule can never apply. Also, `Approved → Reserved` "may be atomic", but if it is atomic, two states are unnecessary.
- **Correction:** remove the dead rule, or add `Reserved → Declined` deliberately. Decide atomicity.

### A9. The contribution "state" table breaks SM-4 (06 §5). Severity 2
- **Problem:** the table mixes acceptance, receipt, finality, valuation, disposition and acknowledgment as states. These are orthogonal dimensions, which is exactly what SM-4 and the five-dimension status vocabulary argue for. Valued "may precede Final" and Acknowledged is "a separate document lifecycle". Both confirm that this is not one machine.
- **Correction:** model these as dimensions with per-asset-class allowed orders. TVC-010's resolution then follows naturally.

### A10. The state model ignores the program's own funding recommendation (06 §2 vs 14 §1). Severity 3
- **Problem:** alternatives 1D recommends a per-fund cash sleeve so that "most grants [become] cash-only transitions … fewer states". The state model still makes Reserved → Funding → Funded / FundingShortfall mandatory. The recommended hybrid (D for routine plus C above the sleeve) keeps **all** of C's states and adds sleeve replenishment and forecasting. The "fewer states" claim is false for the hybrid.
- **Correction:** either drop the sleeve, or state the hybrid's full state set honestly. **Simpler alternative:** a currency reservation (C) plus a pool-level buffer (E). Pooling grant timing across funds needs less total cash than per-fund sleeves sized at max(floor, forecast). E's outage risk is shared by D anyway, because sleeve replenishment also needs liquidation.

### A11. The cash sleeve is assigned to the wrong decision owner (14 §1). Severity 2
- **Problem:** a mandatory cash allocation in every fund changes the investment program. Under DD-007 that is an Investment Committee / IPS decision, not an operations design choice. The minority view mentions advisor-mandate conflict (DD-010) but names no authority.
- **Correction:** list it as an owner decision for the Investment Committee.

### A12. The cash sleeve gives least relief in December (14 §1). Severity 3
- **Problem:** a sleeve of 5% of AUM covers about 4.5 months of average payout. Payout is 800k × $5k ÷ $30bn = 13.3% a year, and 5 ÷ 13.3 × 12 = 4.5 months. But per-fund grants cluster in December (k = 3 implies 25% of annual grants in December). Funds that grant mostly at year-end exhaust the sleeve exactly in the surge, and fall back to the complex C path at peak load.
- **Correction:** size the sleeve seasonally, or accept that the sleeve simplifies off-peak months only. State this in the "wrong if" table.

### A13. Separating the assurer moves the independence problem rather than removing it (03 §2). Severity 3
- **Problem:**
  - Evidence ledger → "platform function": the platform sits under the CTO, who owns agents and engineering whose controls the ledger evidences. Same self-assurance, different owner.
  - Telemetry and twin → "CFO or CRCO": the CRCO owns screening, which is part of the queue being judged. The CFO/Controller already concentrates C3.4 and C4.x (TVC-028).
- **Correction:** independence comes from append-only, tamper-evident evidence plus internal-audit read access, not from who owns the ledger's infrastructure. Put telemetry with internal audit or a role with no queue stake. Do not add roles.

### A14. Organisational separations raise the floor at small scale (03 §2, 14 §4C). Severity 3
- **Problem:** the program proposes several changes together:
  - an independent reconciler (+1 FTE);
  - an analytics function separate from the COO;
  - an evidence-ledger owner separate from the CRCO;
  - a direct line from the CISO;
  - more agent owners (TVA-021).

  At 1k–10k accounts the baseline is already uneconomic (−143% margin at 1k). Model C, which the program prefers for small scale, will not carry this many separate roles.
- **Correction (simpler):** at small scale, use compensating controls instead of roles: periodic independent review by outsourced internal audit, or outsourced monthly reconciliation review. 14 §8 already concedes this. Make role separation scale-conditional.

### A15. The staff-termination rule contradicts SM-6 (03 §5.3). Severity 3
- **Problem:** "Pending approvals they made stay valid … Their **queued** approvals not yet executed are re-routed" is internally ambiguous, because a pending approval is a queued, unexecuted one. It also conflicts with SM-6. SM-6 re-checks authority at payment submission, so a releaser terminated between `Authorized` and `Submitted` fails the check.
- **Correction:** define "approval made" (decision recorded, valid, made under authority at the time) separately from "release authorization" (re-checked at execution under SM-6, re-routed if the authoriser has left).

### A16. TVC-007 is misclassified (03 §3). Severity 2
- **Problem:** the text says all three cases fail the rule-writing precondition "for the requester's identity". TVC-007 (benefit-risk timeout) is about an incomplete protective check, not identity.
- **Correction:** reword this as two failure classes.

### A17. The program over-specifies mechanism (06 SM-1/SM-2, 02, TVC-001). Severity 2
- **Problem:** TVC-001 rightly resolves event sourcing by restating it as a requirement (TVR-DATA-001). The program then prescribes mechanisms itself:
  - "expected revision" optimistic concurrency (SM-2);
  - "input snapshot hash" (SM-1);
  - "bitemporal" facts throughout;
  - fully drawn ~40-state machines.

  These are reasonable, but they are implementation choices in a requirements program.
- **Correction:** state the outcome, for example "a stale command is never applied silently" or "a past decision's inputs are reconstructible". Move mechanisms to a design note.

### A18. The workflow counts are wrong (05 §1). Severity 2
- **Claim:** "18 of 38 are missing or below 1/3 specified".
- **Problem:** using the table's own figures:
  - below 6/18: 14 rows (CW-21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 34, 35, 37, 38);
  - exactly 6/18 (= 1/3, not below): CW-02, CW-32, CW-33;
  - bold but above 1/3: CW-31 (7/18) and CW-36 (12/18). These also cite baseline material (widgets/04; MIG-01..09).
- **Correction:** "14 below one third; 18 not defined as a baseline WF". The x/18 scores are unlabelled judgments, so mark them [I].

### A19. "Giving plan is the only lever" is contradicted by the economic model (14 §2). Severity 3
- **Claim:** the giving plan is "the only lever that reduces December specialist demand without asking donors to accept deferred execution".
- **Problem:** the economic model (15 §3) lists halving *e* through determination reuse and pre-clearing, halving *m*, and seasonal specialists. None of them needs deferral. The scores "+ RD" and "+ FC" for the giving plan are unsupported.
- **Correction:** rank the levers. Reuse of recipient-level determinations has the most evidence (12.5 grants per recipient, EV-025).

### Architect: what a simpler design would look like
1. One delegation-of-authority table as data. TVC-004/005 already recommend this; keep it.
2. The grant holds decision, reservation and funding. Payment status is derived from the attempts. Reconciliation and finality are facts, not grant states.
3. One funding path: currency reservation plus a pool buffer. No per-fund sleeve.
4. Compensating controls instead of new roles below about 10k accounts.
5. Status dimensions for contributions, as already done for grants.

These achieve the same outcomes with fewer states and fewer roles.

---

## Part B: Economics reviewer

### Arithmetic re-checks (all by hand)

| Item | Recomputation | Result |
|---|---|---|
| Expected FTE_avg | 100k × 8 = 800k grants; × 8% = 64,000; × 45 min = 2.88m min = 48,000 h; ÷ 1,600 = **30.0**; × $165k = $4.95m; $49.5 per account | Correct |
| Low | 800k × 4.2% = 33,600; × 30 min = 16,800 h; ÷ 1,600 = 10.5; × $124.5k = $1.307m; $13 per account | Correct |
| High | 800k × 17% = 136,000; × 135 min = 18.36m min = 306,000 h; ÷ 1,400 = 218.6; × $250k = $54.6m; $546 per account | Correct |
| High-case total | $272 − $49.5 (baseline pool) + $546 = **$768** per account | Text says "~$500 added → roughly $790". This is 3% *below* the frontier, not above it. |
| Frontier | 24.41 bps × $66.20bn = $161.6m; ÷ 204,614 = $789.8. Average balance $66.2bn ÷ 204,614 = $323.5k, which matches the $300k case | Correct, and the balance match is fair |
| Peak/average | k=2: 500/275 = 1.818. k=3: 750/300 = 2.500. k=5: 1,250/350 = 3.571 | Correct |
| Peak FTE, expected | 30 × 1.818 = 54.5; × 2.5 = 75; × 3.571 = 107.1 | Correct |
| Peak FTE, high | 218.6 × 1.818 = 397.5; × 2.5 = **546.5**; × 3.571 = **780.7** | Table shows 548 and 782 (rounded from 219). Trivial. |
| Backlog, k=3 | base = 64,000/300 = 213.3 per day; surge 640 per day; capacity 64,000/250 = 256 per day; excess 384 × 25 = 9,600; 9,600 ÷ 256 = 37.5 days | Correct |
| Inference | 64,000 × $0.90 = $57.6k; 100k × 4 × $0.05 = $20k; total **$77.6k** | Correct |
| 1% threshold | ($272k − $20k) ÷ 64k = **$3.94** per dossier | Correct |
| Human cost per exception | $165k ÷ 1,600 = $103.1/h; × 0.75 h = $77.3 | Correct (but see B9) |
| Grant flow | 800k × $5k = $4.0bn; ÷ 250 = $16m per day; × 1% × 5 = $0.8m = 160 grants | Correct |
| Cash drag | 5% × 2% = 0.10% = 10 bps; × $300k = $300 | Correct |
| 1m reconciliation | (8m + 2m) × 0.01 = 100k breaks; × 20 min = 33,333 h; ÷ 1,600 = 20.8 | Correct; already in baseline (22 FTE at 1m) |
| Baseline | 104 × $165k = $17.16m staff; (180 − 27.2) ÷ 180 = 84.9% margin; 1k conventional 8 × $124.5k + 1,000 × $766 = $1.76m | Correct |
| Register counts (16) | Severity 5: 7; severity 4: 12 (002, 004, 005, 007, 008, 011, 015, 017, 026, 028, 030, 033); severity 3: 10; ≤2: 5; total 34 | Correct |

### B1. The flip condition in the sensitivity table is wrong (15 §8). Severity 5
- **Claim:** the frontier advantage flips when "e ≥ ~15% and m ≥ ~120 together".
- **Problem:** flipping needs added cost of at least ($790 − $272) × 100k = $51.8m. The pessimistic cost per exception-minute is $250k ÷ (1,400 × 60) = $2.976.
  - Condition: 800k × e·m × 2.976 − $4.95m ≥ $51.8m, so **e·m ≥ 23.8** (e as a fraction, m in minutes).
  - At e = 15%, m = 120: e·m = 18. Cost = 120k × 2 h ÷ 1,400 × $250k = $42.9m. Total = $272 + $379 = **$651**. No flip.
  - Even the full high case (e·m = 22.95) gives $768. No flip.
  - At base H and loaded cost ($1.719 per minute), the condition is **e·m ≥ 41**, for example 17% × 243 min.
- **Correction:** "Flips when e·m ≳ 24 (pessimistic H and cost) or ≳ 41 (base), e.g. 17% × 140 min." The headline "advantage disappears in the high case" should read "approaches parity ($768 vs $790)".

### B2. The high case applies pessimism to one pool only (15 §2). Severity 4
- **Problem:** $250k per FTE and H = 1,400 apply only to the exception pool. The other 74 FTE stay at $165k and 1,600 h. Loaded cost is the baseline's largest sensitivity (94.6% swing). Applied consistently:
  - 74 × $85k = +$6.3m;
  - complex assets: 30 × 1,600/1,400 = 34.3 FTE, so +4.3 FTE × $250k ≈ +$1.1m;
  - total ≈ $768 + $74 ≈ **$842**, which is above $790.
- **Correction:** the conclusion survives only if all parameters are made consistently pessimistic. As written, it is right for the wrong arithmetic. State which parameters are joint.

### B3. The high case stacks four extremes and two weakly sourced ranges (15 §2). Severity 4
- **e high 17%:** the broad proxy is a recipient screen that includes reputational flags. The inventory says it is "likely 28–31%". 17% is neither its centre nor its upper end; it is an arbitrary pick. The baseline's own reversal band is 3–15% (AC-12), so 17% is outside the band the baseline considers measurable.
- **m high 135:** this is FM-15's failure-mode stress (3 × 45), not a source or a "real alternative". The only evidence anchor is EV-106: **90 min for an unaided heavy review**. An AI-assisted 135 min exceeds unaided handling.
  - At e = 17%, m = 90: 204,000 h ÷ 1,400 × $250k = $36.4m. Total = $272 − $49.5 + $364 = **$587**. The advantage holds.
- **Joint extremes:** "not implausible" is asserted, not argued. All four pessimistic ends (e, m, H, cost) at once is a tail case, not a "high case".
- **Correction:** anchor m high at 90 (EV-106). Label 17% [I]. Present the joint high as a stress test, not a range end.

### B4. The low exception rate uses the wrong unit (15 §2). Severity 4
- **Problem:** "4.2% like-for-like" is a **share of dollars** (research inventory l.165, EV-080), not a share of grants. The per-grant low on the core definition is **2.8%** ("2.8–7.9% if no unitemised recipient flagged", EV-081).
- **Correction:** low e = 2.8% per grant. That gives 22,400 exceptions; × 30 min = 11,200 h = 7.0 FTE = $0.87m.

### B5. No case models determination reuse (15 §2). Severity 3
- **Problem:** the baseline calls reuse (12.5 grants per recipient) "the first parameter to measure" and says it would cut the work "well below" 8%. Every case here is per-grant with no reuse, so the expected case is biased upward and the range is asymmetric.
- **Correction:** add a reuse factor *r* (e_eff = e/r). Even r = 1.5, the AC-12 reversal threshold, cuts the expected pool from 30 to 20 FTE.

### B6. The comparison does not match grant intensity (15 §2, baseline 09 §2). Severity 3
- **Problem:** the frontier is Fidelity at 13 grants per account. AI-native is at 8. The *g* range (6.2–13) is listed but never used.
  - Per grant: Fidelity $790 ÷ 13 = $60.8; AI-native baseline $272 ÷ 8 = $34; high case $768 ÷ 8 = **$96**.
  - On a per-grant basis the high case is already worse. Parity per grant needs e·m ≥ ~11 (pessimistic) or ~19 (base). For example: 800k × e·m × 2.976 = 8 × $60.8 × 100k − $272 × 100k + $4.95m = $26.4m, so e·m = 11.1.
- **Correction:** neither per-account nor per-grant comparison is right alone, because CAC and fees are per account. Run the AI-native model at g = 13 when comparing with Fidelity. The approximate effect is +13% total cost (≈ $308), which is still advantaged in the expected case.

### B7. The surge analysis compares two extremes and omits the SLA (15 §3). Severity 4
- **Problem:** only "staff to peak with no backlog" (75) and "staff to average" (30) are shown. The decision variable is the SLA.
  - Constant staffing *c* per day keeps the end-of-surge FIFO wait at 25(640 − c)/c ≤ S.
  - S = 10 days: c ≥ 16,000/35 = 457 per day, so **53.6 FTE**.
  - S = 5 days: c ≥ 533, so **62.5 FTE**.
- **Problem:** staffing at the average means 100% annual utilisation. The off-peak slack is (256 − 213.3) × 225 = 9,600. That clears the backlog only on the last day of the year. The queue never empties, so any variance makes it unstable. Average staffing is infeasible even without a surge.
- **Correction:** add the SLA-parameterised staffing formula, with target utilisation below 1.

### B8. The surge omits the complex-asset pool (15 §3). Severity 3
- **Problem:** the complex-asset pool is 30 FTE at 100k, equal to the exception pool. Year-end appreciated-stock gifts are December-heavy, probably more so than grants [I]. TVA-004 is unsupported.
- **Correction:** apply k to both pools, or state the omission.

### B9. The twin "agreement" is circular (15 §3). Severity 2
- **Problem:** the twin uses the same k = 3 [A] (TVA-004: "Twin.fs [A]"). "34 days over SLA" and "37.5 days of capacity" are different metrics: SLA overrun versus FIFO wait. Agreement is not corroboration.
- **Problem:** E6's "35 → 25" sits in a table with 75 as if the units were comparable. They come from a different twin configuration.
- **Correction:** remove "matches". Express E6 as −29% and label it.

### B10. The AI cost denominator omits routine-grant runs (15 §4). Severity 3
- **Problem:** the baseline benefit-risk agent runs on **every** grant's purpose text (wf-contributions.md l.64). That is 800k runs, not 64k.
  - At the "single-digit dollars" per agentic run the model posits, 800k × $1–9 = $0.8m–7.2m, or 3–26% of cost.
  - The 1% threshold per routine run is $250k ÷ 800k = **$0.31**.
- **Problem:** the "$77 human cost" uses $103/h. The baseline's own EV-106 uses $55.45/h × 90 min = $83. This is rate drift (TVC-020) inside the same paragraph's reasoning.
- **Correction:** state thresholds per run type with run counts. Classify the benefit-risk screen as a single bounded call, or price it.

### B11. 1% of total cost is an arbitrary materiality line (15 §4, §8). Severity 2
- **Problem:** the relevant comparisons are the margin to the frontier and the human minutes displaced. "Flips at > ~$10 per case": $10 × 64k = $640k = 2.4% of cost. What flips is undefined.
- **Correction:** define materiality against the decision it would change.

### B12. Cash-sleeve comparisons mix payers and are wrong against custody (15 §7, 14 §1). Severity 3
- **Problem:** 14 §1 calls 10 bps "comparable to the custody and admin fees in the baseline". Custody is **0.5 bps** ($1.5m ÷ 100k = $15 per account). The drag is 20× custody. The admin fee is 60 bps ($1,800), so the drag is about 1/6 of it.
- **Problem:** 15 §7 compares donor-borne opportunity cost ($300) with sponsor operating cost ($272). These are different payers and different kinds of cost. The expected-return gap is also partly a risk premium, so the risk-adjusted cost is lower.
- **Problem:** "a 90-day sleeve lowers drag proportionally": 90 days of grants is 13.3% × 90/365 = 3.3% of AUM, so drag is 6.6 bps ≈ **$197**. That is not a large saving. A sleeve sized as max(floor, forecast) is larger still.
- **Correction:** compare against the admin fee and against the cost the sleeve avoids (per-grant liquidation trades and shortfall cases). The baseline has no estimate of that avoided cost, so record the gap.

### B13. Incident reasoning overstates the statutory penalty (15 §5). Severity 2
- **Problem:** the §4966 manager tax is 5% **capped at $10,000 per distribution** and requires knowing agreement. Who the "manager" is under policy approval is the open TVC-003 question. Only the taxable fraction of the $0.8m carries the 20% tax, so the direct tax is small. For example, 10% taxable gives $80k × 20% = $16k. Remediation and reputation dominate, but they are unquantified.
- **Problem:** the claim that scale *s* leaves detection time unchanged is asserted. More volume can shorten detection. Correlation matters to the **operator's** tail and to contagion, not to each sponsor's expected cost.
- **Correction:** state the cap, and separate sponsor exposure from operator exposure.

### B14. "Specialist pool binds across all cases" is false at small scale (15 §8). Severity 2
- **Problem:** at 1k–10k accounts the floors bind. Grants compliance is 1–3 FTE, against leadership 5–8 and engineering 4–6. In the low case at 100k (10.5 FTE), the complex-asset pool (30) is larger than the exception pool.
- **Correction:** "binds at ≥100k accounts in the expected and high cases."

### B15. Levers table formulas are vague (15 §3). Severity 1
- **Problem:** the giving-plan formula "75(1 − p) + spread" ignores the 25-FTE base-rate floor in December. Peak is about max(25 + 50(1 − p′), off-peak), where p′ is the plannable share of the December *excess*. The table is labelled "ranked" but is not ranked.

### Are low/expected/high defensible from the cited sources?
- **g:** yes, sourced (6.2–13.0). But the high value is never used.
- **e:** partly. The low uses a dollar share (B4). The high is an arbitrary point in a recipient-screen proxy, outside the baseline's 3–15% band (B3). The expected 8% is the core per-grant proxy without reuse (B5).
- **m:** no. 30 and 135 are both [A]. 135 is a failure-mode multiplier. The only evidence anchor (EV-106) suggests about 90 min unaided.
- **H, loaded cost:** [A]. Applied inconsistently across pools (B2).
- **k:** unsupported (TVA-004). The implied December share is 25% of grants at k = 3 and 36% at k = 5. Day-level sponsor data is needed.

---

## Checked and could not fault
- All closed-form arithmetic in 15 §2–7. The only issues are rounding of 548/782.
- Frontier derivation ($789.8) and the balance match (~$324k vs $300k).
- The baseline 30 FTE, 104 FTE, $27.2m, 84.9% margin, and $1.76m conventional cost at 1k.
- Contradiction-register status counts (7/12/10/5 = 34).
- The diagnosis that the baseline staffing table has no surge term (TVC-017). The distinction between per-second infrastructure peaks and daily staffing volume is correct.
- TVC-001 resolution (requirement, not mechanism), TVC-004/005 (one DoA table), TVC-025 (auto-approval ceiling ≤ session assurance), TVC-028 (pay ≠ reconcile), and PA-1/PA-2 (double-payment invariant and proof of non-receipt). All are sound.
- SM-4 (holds as orthogonal flags) and SM-0 (child records for post-terminal facts) are good principles. The defects are in how 06 applies them (A5, A9).
- The point that the cash sleeve is "not free" and is justified by simplicity rather than cost. The direction is right; the comparators are wrong (B12).
- ONT-4 (one grant, one fund) and ONT-6 (a channel is never an authority).
