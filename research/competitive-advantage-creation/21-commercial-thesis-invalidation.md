# 21 - Commercial thesis invalidation

Status: research (2026-11-26). Track M. Agent CE. This report states the Phase III commercial thesis as precisely as reports 02-16 and the model outputs allow. It then lists the observable conditions that would invalidate the thesis or change it materially, and reconciles them with Phase II's invalidation list ([22](../competitive-displacement/22-commercial-validation-plan.md) §2). It proposes reconsideration criteria in the Clarity sense ("what would make me reconsider?"); it does not decide them. Postures and diagnoses: [17](17-clarity-and-edf-assessment.md). Register rows: [claims.csv](data/fragments/CE/claims.csv), [hypotheses.csv](data/fragments/CE/hypotheses.csv), [decisions.csv](data/fragments/CE/decisions.csv), [evidence-gaps.csv](data/fragments/CE/evidence-gaps.csv), [validation-experiments.csv](data/fragments/CE/validation-experiments.csv).

No condition below has been observed except where marked "partly observed (desk)". Every status is as of 2026-11-26, with no outreach made.

**Revision 2 (2026-11-26, model revision 2).** Round-1 review disputed the claims that A3 "passes the kill rule" and "still pays back" (P3-CHL-REV2001, REV2002, REV1046, REV2011, REV2029, REV2030). Model revision 2 withdraws both:
- No sequence pays back within 120 months in the base case.
- With the kill rule applied, every platform sequence pauses, mostly at month 24, and is worse than doing nothing on the Monte Carlo median (`sequences-ranking.md`).
- The thesis below is kept as stated and annotated. Its decisive premise is now T3: revenue per customer at a named sponsor size. TI-12(b) is restated because Nacha TPSP status is not contingent (P3-CHL-REV3019).

**Revision 3 (round 2, model revision 3, CFO-corrected basis).** The decision is unchanged. With the cost center opened at month 0, every configuration still pauses at month 24, and none beats doing nothing in the Monte Carlo. Two things are new:
- **One route pays back: partner-book licensing** (SEQ-PB, P3-SEQ-MOD012), when the sponsor performs the deep review. It reaches +$4.18M at month 120, pays back at month 76 and peaks at $2.43M; under M5 it pays back at month 80 (`bases.md`).
- **Who performs the deep review (P3-DEC-MOD005) is now a thesis premise alongside T3.** Break-even for a single sponsor is not reached if Echelon performs M1. It is 5,202 accounts if the review is risk-tiered, 3,079 accounts ($175k net) if the sponsor performs it, and 3,169 under M5 (`gate-break-even.md`).

Figures below are restated to revision 3, with earlier values kept.

## 1. The thesis

### 1.1 Statement

> **Echelon Foundry can build a commercially viable DAF technology business without outside investment, a conventional staff or a sales organization, but only as a niche, founder-led software licensor.**
>
> **The route.**
> - Complete Unbound to functional completeness (S3) before DAF commercialization becomes its own cost center.
> - Then license it through one non-exclusive channel partner (DEC-001, DEC-006), to sponsors that each pay roughly $150-600k a year net of the partner's share.
> - Bind assurance, insurance and legal only at a signed term sheet.
> - Run the business on a lean fixed cost of roughly $0.17-1.07M a year in cash (Revision 2: about $1.25M a year once TPSP obligations, control operations and the governing M1 registry are added; revision 3: about $1.03M, `response-walk-away.md`).
> - Charge implementation fees and bill in advance.
>
> **What it costs and earns, on those assumptions.**
> - Peak cash of about $547k, $8.26M or $31.49M (favourable, base, adverse; A3 uninterrupted, Echelon performing M1 on demand, model revision 3). Earlier: revision 2 gave $744k / $8.70M / $46.22M; revision 1 gave "$0.22M, $1.24M or $16.97M".
> - No base payback within 120 months; the favourable case pays back at month 25 (revision 3; month 26 in revision 2). Revision 2: previously "Base payback around month 62".
> - Under the kill rule, the base case pauses at month 24 with $1.38M of cash at risk (A3; $1.33M for A from today; revision 3; revision 2 gave $1.81M and $1.46M).
> - Niche-scale revenue; not a venture-scale outcome.
>
> **What it survives.** Moderate incumbent price responses, because of the lean cost base. Revision 2: only if customers are large enough to reach break-even at all, which on the governing M1 basis means about 10,963 accounts per customer (revision 2). Revision 3: 3,079 accounts if the sponsor performs the deep review; not reached if Echelon performs M1.
>
> **What it does not survive.** Losing its channel, a partner acquired without change-of-control protection, or customers that pay an order of magnitude less.
>
> **What the narrow components are.** Charity intelligence, Transitus, compliance evidence and the developer components are modules, acquisition cost and credibility. They are not funding sources.

### 1.2 Premises the thesis rests on

| # | Premise | Status | Basis |
|---|---|---|---|
| T1 | Unbound reaches S3 without opening the DAF cost center, at modest remaining cash | Unknown. Unbound is at S2 today | P3-CLM-EK005, P3-CLM-MOD006, P3-GAP-MOD005, P3-GAP-CE004 |
| T2 | A channel partner engages within six months of the cost-center month and accepts non-exclusive, change-of-control-protected terms | Untested | DEC-001, P3-HYP-EK006, P3-HYP-FGJ005, P3-ASM-MOD034 |
| T3 | Customers pay about $150-600k a year net of channel (ER-7 basis: ~$81 per account on 3-10k-account sponsors), about 3 a year | Untested. **Partly contradicted (desk)**: only 33 sponsors have ≥2,646 accounts | P3-ASM-AB030, P3-CLM-CE001, P3-CLM-CE003, P3-GAP-MOD003 |
| T4 | A founder-led, agent-assisted licensor can run production for ≤$0.5M a year cash before scale, and buyers accept it | Untested | P3-HYP-AB001, P3-HYP-AB003, P3-CLM-AB011 |
| T5 | The owner can fund the cash at risk before the kill rule pauses the sequence ($1.38M A3, $1.33M A, base, revision 3; revision 2: $1.81M and $1.46M) without outside equity; there is no base payback to fund towards (Revision 2: previously "the peak cash need (base $1.24M corrected)") | Unknown | P3-CLM-MOD012, P3-GAP-MOD001 |
| T6 | Incumbent response stays within what the lean cost base absorbs, and the partner is not acquired out from under the licence | Untested | P3-CLM-MOD013, P3-CLM-EK016, P3-DEC-EK002 |
| T7 | Mandatory obligations stay in the modelled ranges: SOC 2, insurance, counsel, registry run, and DEC-003 within the 180-day ceiling | Untested. Ranges are assumptions | P3-CLM-HI012, P3-GAP-AB001, P3-GAP-AB003, P3-GAP-HI003 |
| T8 | Echelon components can be licensed commercially to customers | Blocked. Terms "forthcoming" | P3-CLM-FGJ002, P3-DEC-FGJ001 |

**What the thesis is not.**
- It does not claim a durable technical moat (P3-CLM-EK006).
- It does not claim that greenfield programmes carry the licensor (P3-CLM-MOD007).
- It does not claim that partner-first lowers acquisition cost (P3-CLM-FGJ009).

## 2. Invalidation and material-change conditions

**How to read the table.**
- **Effect:**
  - **I** invalidates the thesis as stated;
  - **M** materially changes it (sequence, capital or route), but a version survives.
- **Cost to observe:** cash, plus approval where contact is needed. Outreach at any cost tier needs owner approval ([04](04-low-cost-commercial-validation.md)).
- **Timing:** months are counted from the cost-center month (CC) unless dated.

| ID | Premise | Indicator | Threshold | How and when observed | Cost to observe | Decision reopened | Effect | Status |
|---|---|---|---|---|---|---|---|---|
| TI-01 | T3 | Net annual revenue per signed or committed customer, and the size of the customer (DAF accounts) | (a) Net revenue per customer ≤$150k. At the ER-7 low, A3 does not recover fully loaded cost within 120 months: economic m120 −$534k (`tornado-sequence-a3.md`, revision 1). Revision 2: at 2,646 accounts ($150k net) A3's m120 cash is −$9.24M under M1 (revision 3: −$8.50M). Break-even needs 10,963 accounts ($622k net) under M1, or 3,949 ($224k) under M5 (revision 2). Revision 3: not reached with Echelon performing M1; 3,079 accounts ($175k net) with the sponsor performing; 3,169 under M5. Plausible sponsors: 17 at 2,646 accounts or more (`gate-break-even.md`, `platform-classes.md`). (b) Or fewer than about 10 sponsors with ≥2,646 accounts are reachable without displacing a contracted incumbent, and no partner offers its aggregated book as the customer | (a) V-2 nonbinding EOIs and V-6 term-sheet economics, from first conversations (pre-CC). (b) P3-VAL-CE001 desk classification now; confirmed in V-6 | $0 (desk); $0-1k plus approval (V-2, V-6) | DEC-006, DEC-001, P3-DEC-CD001, P3-DEC-CE002, sequence choice | **I** | **Partly observed (desk)**: 33 qualifying sponsors, 19 of them national standard and 5 donation processors (P3-CLM-CE001). Reachability untested |
| TI-02 | T2 | Named partner or design-partner customer in term-sheet talks with a pilot customer | None by CC+6 (kill rule; OD-P3-03/04) | V-6 log of partners contacted, stage and dates | $0-5k plus approval | DEC-001, DEC-008, P3-DEC-MOD001 | **I** (pauses the thesis) | Untested. No search has run (D6 in [17](17-clarity-and-edf-assessment.md)) |
| TI-03 | T2, T6 | Terms demanded by engaged partners | Every engaged partner (≥3) requires one of: exclusivity without a paid minimum; a ROFR or acquisition option; or a revenue share above 50%. At 100% share, A3 loses $7.18M (`extremes-kill-rule.md`, revision 1; Revision 2: −$1.81M under the kill rule, the same as base, because base already pauses at month 24; revision 3: −$1.38M); the thesis becomes "supplier to an acquirer" ([12](12-institutional-distribution.md) §4) | V-6 term-sheet drafts (the $25k tier) | $5-25k (term-sheet legal review) | DEC-001, P3-DEC-FGJ003, P3-DEC-EK002 | **I** (as an independent licensor); **M** if sale is accepted | Untested |
| TI-04 | T3 | Customers signed per year after the first, and partner-sourced qualified opportunities | No partner-sourced qualified opportunity within 12 months of a signed partner agreement (P3-HYP-FGJ004). Or fewer than 1 new customer a year through CC+48. At 1 a year, A3's economic m120 is −$2.85M (revision 1; Revision 2: −$19.19M uninterrupted; revision 3: −$14.37M economic, nearly the same as at 5 a year because the population cap of 4 reachable sponsors binds, `tornado-sequence-a3.md`) | CRM-style log of the partner pipeline, reviewed quarterly | $0 | DEC-001, DEC-008 | **I** | Untested |
| TI-05 | T5 | Owner's stated funding capacity and runway for DAF commercialization | Capacity below the cash at risk before the kill rule pauses the sequence ($1.38M A3, $1.33M A, base, revision 3; revision 2: $1.81M and $1.46M; `sequences-kill-rule.md`). There is no base payback, so outside capital would finance a loss (P3-CLM-MOD012). Revision 2: previously "Capacity below the base peak cash need ($1.24M corrected) ... or the sequence must be customer-funded (peak $896k)"; customer funding no longer lowers A3's peak (`sequences-funding.md`) | Owner statement, now (P3-GAP-MOD001) | $0 | DEC-008, P3-DEC-AB001 | **M** (funding route); **I** for "without outside investment" | Unknown |
| TI-06 | T1 | Ledgered cash and hours from S2 to S3 (P3-DEC-AB003); whether completion stays outside the cost center | S3 not reached inside existing operations, so the cost center opens at S2 and A3 becomes A (A is paused at month 24 in the base case, P3-CLM-MOD006; Revision 2: so is A3). Or remaining development cash above $0.25M (AB high), or hardening that proves to be a rebuild | Build ledger, monthly; owner's ruling on P3-DEC-MOD001 | $0 | P3-DEC-MOD001, P3-DEC-CE001, DEC-008 | **M** (A3 → A; the kill rule bites) | Unknown |
| TI-07 | T4 | Measured live run cost; hires forced by procurement | Run cost above $0.8M a year over the first 12 live months, or ≥2 hires forced (P3-HYP-AB001). A conventional run rate lifts A3's peak to $4.52M (`extremes-kill-rule.md`, revision 1; Revision 2: $2.48M under the kill rule; revision 3: $1.38M, the same as base, because the pause comes first) | Live accounts, monthly after go-live; partner procurement checklists earlier | $0 | P3-DEC-AB001, DEC-008 | **M** (capital); **I** with TI-05 | Untested |
| TI-08 | T6 | Acquisition of the channel partner during G1 or G2 | A target or signed partner is acquired by an incumbent or a competitor of Unbound without change-of-control continuity in the contract: revenue ends at the acquisition date (RS-5, [16](16-capital-efficient-market-entry.md) §5) | Public announcements; contract review | $0 | P3-DEC-EK002, DEC-001 | **I** (without protection); **M** (with it) | Untested. The precedent rate is high (P3-CLM-EK009) |
| TI-09 | T4 | Vendor-viability objections | ≥2 of 5 partners cite a single-founder vendor as disqualifying, even with escrow, a contracted second maintainer and insurance (P3-HYP-AB003) | V-6 conversations; diligence questionnaires | $0-1k plus approval | DEC-001, organizational design ([17](17-clarity-and-edf-assessment.md) §4.3) | **M** (hires or a co-founder change the run rate; links to TI-07) | Untested |
| TI-10 | T6 | Incumbent net-price response at contested deals; incumbent feature parity | (a) Net price offered or obtainable is below the walk-away price for the cost base actually achieved: $58.51 per account-year on Phase II MD-6, $27.86 on the lean licensor, or $30.35 with the founder at market (five years at the base acquisition rate; $21.56 at ten; `response-walk-away.md`, revision 3; revision 2 gave $31.30 and $33.78; revision 1 gave $21.51). P3-DEC-EK001's ~$73 is an MD-6 figure and should be restated once the lean run is measured (P3-GAP-CE005). (b) An incumbent ships replay and published migration outcomes before the first pilot is live | (a) Lost-deal debriefs in V-1 and V-2. (b) Public release notes, monitored monthly at $0 | $0 | DEC-006, P3-DEC-EK001, P3-DEC-EK003 | (a) **I** below walk-away; (b) **M** (differentiation, not viability) | Untested |
| TI-11 | T3 (greenfield variant) | New institutional DAF programme launches; host willingness | Fewer than ~2 new education or health programmes a year in 2021-26 (P3-HYP-CD001). Or hosts require one system for all funds (P3-HYP-CD002) | Public-record review now ($0); V-6 host conversations | $0; $0-1k plus approval | P3-DEC-CD001, P3-DEC-CE002 | **M** (removes E and G as adoption routes; they already fail as revenue routes) | Untested |
| TI-12 | T7 | Auditor and counsel positions | (a) An auditor requires full periodic human re-review instead of change-driven renewal within 180 days (V-9). The registry then trends toward the ~$767k human-review case at 20k charities, against ~$124k hybrid ([11](11-continuous-charity-intelligence.md)). Revision 2: M1 ($768k) is now the governing base and M5 is conditional on OD-CDD-02. Revision 3: under licensing that cost is the sponsor's if the sponsor performs the deep review (P3-DEC-MOD005); an Echelon-performed, demand-driven review adds about $469k a year for one sponsor at 20k charities. A favourable owner decision on OD-CDD-02 is therefore an opportunity condition, not only a risk. (b) Sponsors' auditors require SOC 1 Type 2 for the ledger: +$20-120k a year plus an observation period. The Nacha TPSP audit is not part of this trigger. Unbound is a TPSP under ratified CNV-PAY-001, so the audit belongs in the base run (Revision 2: previously "Counsel finds the licensor is a Nacha TPSP and sponsors' auditors require SOC 1: +$170k a year, A3 peak $1.49M, still pays back"; Revision 2: SOC 1 Type 2 at +$120k a year lifts A3's kill-rule peak from $1.81M to $1.87M, `extremes-kill-rule.md`; revision 3: no change from $1.38M, because the pause comes first) | Informal V-9 at $0; written positions at the $50k tier, only once a partner model is known | $0; $15-100k later | DEC-003, P3-DEC-HI002, DEC-008 | **M** | Untested |
| TI-13 | T8 | Commercial licence terms for Unbound and its Echelon dependencies | No commercial terms by the first term sheet (CNV-GOV-007) | Owner decision P3-DEC-FGJ001 | $0-7k (draft terms) | P3-DEC-FGJ001 | **I** (no sale is possible) until decided | Unresolved (owner-controlled) |
| TI-14 | T3 | V-1 decisive factors | ≥6 of 10 sponsors name product capability as decisive. That supports direct entry (OD-M-05) and reopens partner-first as the only route | V-1 interviews ($1k tier) | $0-1k plus approval | DEC-001 | **M** (route; it could strengthen the thesis) | Untested |
| TI-15 | T3 (existing-sponsor customers) | Export access | V-4 shows incumbent exports cannot be obtained or reconciled without incumbent cooperation. A3's large-sponsor customers almost all have existing books, so this blocks them; greenfield is unaffected | V-4 at the $100k tier, with a partner's pilot customer | $5-25k minimum; $40-160k full | DEC-010, DEC-007, sequence choice | **I** for large-sponsor A3; **M** otherwise | Untested |

## 3. The eight conditions to watch first

These are ranked by how decisively each would change the thesis, weighted by how cheaply and early it can be observed (Clarity: "the fastest useful path to reducing uncertainty").

1. **TI-01: revenue per customer and customer size.** It sets whether A3 has customers at all without displacement. The desk half costs $0 and is partly done. The other half folds into the V-2/V-6 conversations.
2. **TI-02: named partner by CC+6.** This is the kill rule. Its trigger claim needs stating first (P3-DEC-CE001).
3. **TI-03: partner control terms.** These decide whether Echelon is a licensor or a supplier to an acquirer.
4. **TI-05: owner funding capacity.** It costs $0 to observe today and decides the funding route.
5. **TI-06: S3 completed outside the cost center.** In revision 1 it decided whether the thesis was A3 (passing the kill rule) or A (paused in the base case). Revision 2: both pause at month 24 in the base case. Completing outside the cost center (A3X) moves build cost off the clock without saving it, and the sequence still pauses, at month 36 after $2.41M (`sequences-kill-rule.md`).
6. **TI-04: partner-sourced throughput.** Customers per year is the third-largest driver of A3's economics.
7. **TI-08: partner acquired without change-of-control protection.** No cost base survives it; it is preventable only by contract.
8. **TI-07: lean run rate falsified.** If the live run reverts to conventional cost, the base case needs outside capital.

TI-09..TI-15 matter, but each either materially changes the thesis rather than invalidating it, or comes later in the sequence.

## 4. Reconciliation with Phase II report 22 §2

Phase II's thesis was "an AI-native entrant can win institutional DAF business through a licensed platform entered via migration and eligibility-evidence wedges". Phase III's thesis has three differences:
- it is partner-first and licensing-first (DEC-001, DEC-006);
- it does not depend on migration or eligibility evidence as wedges ([06](06-customer-acquisition-without-displacement.md), [07](07-architectural-competitive-advantages.md));
- it is conditional on a completed Unbound.

Each Phase II condition is kept, revised or retired accordingly.

| Phase II item | Disposition | Reason | Phase III successor |
|---|---|---|---|
| 1. V-1 shows switching is distribution-driven only and no partner engages (V-6 fails) | **Revised** | The first half is now the premise, not a falsifier: Phase III assumes distribution is binding (D1 in [17](17-clarity-and-edf-assessment.md)). The second half is the kill rule | TI-02 |
| 2. V-2: buyers will not pay more than ~$60 per account | **Revised** | On the lean cost base the walk-away price is $27.86 at five years and $21.56 at ten; with the founder at market in cash it is $30.35. All three are below about $60 (`response-walk-away.md`, revision 3; revision 2 gave $31.30 / $23.61 / $33.78; revision 1 gave "$21.51 (five years)"). Per-account price alone no longer decides viability. Revenue per *customer*, which combines price with customer size, does, and that is the top driver (P3-CLM-MOD010) | TI-01 (revenue per customer); TI-10a (price below walk-away for the achieved cost base) |
| 3. Incumbents publish migration commitments and exit symmetry before Unbound has a reference customer | **Retired as an invalidator; kept as a differentiation signal** | Migration is no longer the entry wedge. EK021 published exit commitments are "very low" resilience ([07](07-architectural-competitive-advantages.md); [13](13-incumbent-response-model.md) §2). Matching them removes a talking point, not the business | TI-10b (M) |
| 4. V-4: exports cannot be obtained or reconciled without incumbent cooperation | **Kept, scoped** | It still blocks any customer with an existing book, and A3's qualifying sponsors almost all have one. Greenfield programmes are unaffected | TI-15 |
| 5. V-3/V-9 show change-driven re-vetting is unacceptable and exceptions exceed ~8% | **Revised** | DEC-003 now keeps the 180-day ceiling, so re-vetting is automated rather than eliminated (P3-CLM-HI002). The registry is a mid-ranked cost (`tornado-sequence-a3.md`). Auditor rejection raises cost materially but does not by itself invalidate licensing | TI-12a (M) |
| 6. Customer acquisition slower than one customer a year under every channel | **Kept, re-thresholded** | It is still decisive: at 1 a year, A3's economic m120 is −$2.85M. The lean base lowers the capital at risk; it does not create demand (P3-CLM-AB013). A leading indicator is added: no partner-sourced opportunity in 12 months | TI-04 |
| 7. Satisfied stayers rank every positioning hypothesis below "nothing" | **Kept, scoped** | It is irrelevant to greenfield programmes, but decisive for A3's large-sponsor customers. They are stayers by construction, so a "nothing" ranking leaves no reason to buy | Folded into TI-01(b) and TI-14 |
| 8. No partner engages by month 6 | **Kept, revised clock** | The clock starts at the cost-center month (OD-P3-03, OD-P3-04), not at approval. The trigger claim must be stated (P3-DEC-CE001) | TI-02 |

**New in Phase III, with no Phase II equivalent:** TI-01(b) (the size of the customer universe), TI-03, TI-05, TI-06, TI-07, TI-08, TI-09, TI-11 and TI-13. Most of them test the "without conventional capital, staffing and distribution" part of the question, which Phase II did not pose.

## 5. Monitoring plan

| When | Observe | Cost | Owner |
|---|---|---|---|
| Now (pre-CC; no contact) | TI-05 (owner statement). TI-01(b) desk classification (P3-VAL-CE001). TI-11 public-record launch count. TI-13 licence decision. TI-06 ledger started | $0 | Owner |
| On approval of the $1k tier (pre-CC) | TI-01(a), TI-09, TI-14 in V-1, V-2 and V-6 conversations; TI-03 first positions | $0-1k | Owner (founder) |
| CC+0 to CC+6 | TI-02 | $0-5k | Owner |
| Term sheet | TI-03, TI-12 (counsel scoping), TI-13 | $5-50k | Owner |
| CC+6 to CC+24 | TI-15 (V-4), TI-12 (V-9 written position) | $5-160k | Owner; Transitus owner for V-4 |
| After first go-live | TI-07, TI-04, TI-08, TI-10 | $0 | Owner |

**Re-evaluation rule (Clarity progressive commitment).** Continue at the current tier while no TI condition is met. Escalate one tier only when the next gate's trigger occurs ([04](04-low-cost-commercial-validation.md) §2). Stop or re-scope when any **I** condition is met. Record what changed and why (Clarity Loop, step 8).

## 6. Limits

- **Every threshold is conditional on the Phase III model's assumption ranges.** None is a forecast.
- **The two thresholds marked as from the tornado** (≤$150k per customer; 1 customer a year) are the ends of tested ranges, not computed break-even points.
- **The sponsor-size count uses Schedule D account counts.** It does not cover partner-aggregated books ([17](17-clarity-and-edf-assessment.md) §7).
- **Statuses reflect no outreach.** "Untested" is not evidence for or against the thesis.
