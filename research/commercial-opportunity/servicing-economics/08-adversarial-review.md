# 08: Adversarial review

**Date:** 2026-11-25. **Pass:** ADV, an adversarial review of the model, the five research passes and the integrator's conclusions. It covers nine perspectives, the Clarity-structured challenge and the incentive and competitive reviews.

**Data:**
- [`adversarial-findings.csv`](../../../data/commercial-opportunity/servicing-economics/adversarial-findings.csv): 38 findings.
- [`assumption-challenge-adv.csv`](../../../data/commercial-opportunity/servicing-economics/assumption-challenge-adv.csv): 13 assumptions challenged with the Clarity fields.
- [`framework-procedure.jsonl`](../../../data/commercial-opportunity/servicing-economics/framework-procedure.jsonl): the Clarity and EDF procedure as the framework documents define it.

**Framework revisions:** Clarity `200a9eb`, EDF `710d54c` (v0.3).

**What is not claimed:**
- Clarity is applied as a structured challenge, not a certified review.
- EDF was not executed: it requires an observed outcome, and these are hypotheses about a company that does not exist. Each challenge row instead names an adjacent observed outcome that could be diagnosed.
- **The reviewer, the five passes and the integrator are all from the same model family. This is not independent validation (ADV-036).**

## Integrator disposition of the findings

The model was corrected and every material analysis re-run after this review (`model/out/results.md` sha256 `b25b849b…`, 28/28 tests passed). The numbers quoted in the ADV sections below are the **pre-fix** values the reviewer computed, using a Python port of the F# core.

| Finding(s) | Disposition | Effect on results |
|---|---|---|
| ADV-001, 026, 028, 029 (20 bps is not per-account parity with Ren at high balances; fee is large relative to sponsor opex) | **Accepted.** A buyer-cap scenario (lesser of 20 bps or $737 per account, as an average) was added; the cost-reflective tariff recommendation changed (reports 05, 07). | Sponsors covering fixed cost alone fall from 19 to 5 under the cap. 20 bps is credible only around $250-400k average balances. |
| ADV-002, 035 (single-sponsor sustainers overstated; captives and competitors in counts) | **Accepted.** Counts filter `captive_status`; NPT, AEF, Dechomai and the GKCCF group are excluded by name in reports 02, 05 and 10. | About 2-4 realistic decision units. |
| ADV-003 (AI-native from day one) | **Fixed.** Cash plans run AI-enhanced for 12 live months (`RedesignLagMonths`). | Anchor capital $3.40M → $3.56M (AI-native-from-go-live variant $3.35M). |
| ADV-004, 005 (build and sales uncosted) | **Fixed.** Fully loaded variant (+$1.0M build amortisation, +$0.25M sales) and an Unbound-scale $5M build plan. | Fully loaded break-even $1.83-2.29B; capital up to $8.5-11.4M with a $5M build. |
| ADV-006 (no utilisation) | **Fixed.** 90% queue utilisation. | Slightly more added staff. |
| ADV-007 (December overflow paid twice) | **Kept, documented as conservative** (about $0.1M a year high). Release authority cannot be bought from temps, so buffer capacity is retained. | None. |
| ADV-008 (compliance officer triggered by assets) | **Fixed.** Now triggered by accounts above 10,000; a test asserts costs do not fall when only assets fall. | Stress results no longer show cost relief in downturns. |
| ADV-009 (one mix, workload independent of balance) | **Fixed.** Workload scales with balance^0.34, derived from the archetypes. | High-balance sponsors are costlier per account (SVCF 158 min per account-year); SVCF's marginal break-even moves from 0.2 to 0.4 bps because its $8.5B balance dwarfs its cost. |
| ADV-010, 025 (sponsor contribution boundary) | **Fixed in part.** A per-sponsor step share (about $40k) was added and hours are valued at utilisation-adjusted cost. The double count of the minimum operations person in "covers fixed" is documented. | Positive sponsors 292 → 224 at base. |
| ADV-011 (outflow vs payout) | **Documented** as a limitation; payout-neutral pricing recommended (report 07). | None in model. |
| ADV-012 (concentration stress only on equal sponsors) | **Fixed.** Stress table for the anchor portfolio. | Losing the anchor: margin 47.9% → 2.8%. |
| ADV-013 (strategies confounded) | **Fixed.** Normalized plans ($1.5B, $250k balance). | Anchor advantage is mostly timing. |
| ADV-014 (partnership terms) | **Accepted.** Partnership-first not recommended. | None. |
| ADV-015, 016, 017 (no ramp or attrition; financing in capital; December cash timing) | **Documented** as limitations in reports 05 and 06. | Capital ±$0.1-0.4M. |
| ADV-018, 019, 024 (floor semantics, effective bps, inert minimum) | **Accepted.** Effective bps reported for every structure; floor capped at 1% of balance in the recommended tariff. | Recommended tariff changed to per-account fee + low bps. |
| ADV-020, 022 (payments and intermediary boundary) | **Fixed.** Payments pass through at cost and complex-asset intermediary fees are fund-borne in the base; servicer-pays variants retained. | +$0.1-0.2M a year in base. |
| ADV-021 (no activity fees) | **Accepted** in the recommended tariff (activity fees for complex gifts, international grants, wires). | Not modelled numerically. |
| ADV-023 (controller counted as preparer) | **Fixed.** Controller servicing share set to 0. | More added staff at small scale. |
| ADV-027 (anchor existence) | **Accepted.** Anchor-only not recommended; two or three large sponsors instead (report 07). | None. |
| ADV-030 (incentive conflicts) | **Accepted.** Safeguards adopted (report 07 §4; RC-SE-001, 002, 007). | None. |
| ADV-031 (redesign is temporary) | **Accepted** (report 07 §3). | None. |
| ADV-032 (money transmission) | **Accepted** as an activation gate (report 07 §5). | None. |
| ADV-033, 037, 038 (December roster, flat sponsor-level work, flat onboarding) | **Documented**; ranges given (onboarding $35-325k). | Sensitivity only. |
| ADV-034 (tests) | **Fixed.** 8 tests added (28 total). | n/a |
| ADV-036 (independence) | **Accepted.** Stated throughout. | n/a |

> Research-pass content below was produced by a role-separated agent pass from the same model family as the integrator. It is not independent validation. Labels: [S] sourced, [A] assumption, [D] derived, [E] estimate.

## ADV-0 Scope, method and independence

Group ADV (adversarial review), 2026-11-25. Read-only; nothing in any repository was modified. Labels: [S] sourced, [A] assumption, [D] derived, [E] estimate.

**Material reviewed (all read in full):** F# model `Domain/Economics/Parameters/Analysis/CashFlow/Strategies/Program.fs` and `Tests.fs`; `model/out/results.md` and `sponsor-model-economics.csv` (identical to the copies in `data/commercial-opportunity/servicing-economics/`); PRC, SPN, CST, ACT and ECH `report.jsonl`; ECH `framework-procedure.jsonl` and `assumption-challenge-template.csv`; the two prior memos; integrator conclusions in `servicing-economics/01-04*.md`; Unbound `05-ECONOMIC-VALIDATION.md` EV-01..EV-10.

**Method.** (1) Line-by-line code audit. (2) No .NET SDK in this session, so `scripts/port.py` is a pure-function Python port of `Economics.evaluate` and `Parameters` (Model B). It reproduces results.md exactly: Model B, 5 sponsors, $1.5B, $150k, 20 bps, AI-native = **-$559,937** (results.md: -$560k); break-even $1.97B; strategy run-rates $1.78M / $87k / $270k / -$1.07M [D, EV-ADV-001]. `scripts/checks.py` regenerates every number quoted here. (3) Perspective reviews. (4) Clarity-structured challenge of AC-01..AC-13 (`assumption-challenge-adv.csv`, all 34 template columns plus two flip columns). Per ECH's stated limits: **EDF was not executed** (it needs an observed outcome; each row names an adjacent observed outcome instead), and the Clarity rows are **structured challenge, not a certified review** (no decision-owner sign-off, no cadence).

**Independence.** This review, the five passes, the integrator and the Python port are the same model family. Agreement or disagreement between them is not independent validation (ADV-036).

## ADV-1 What flips: headline verdicts

| # | Conclusion under review | Verdict | Why (one line) | Evidence |
|---|---|---|---|---|
| 1 | '20 bps is about parity with Ren at MS GIFT; a market price for $250k+ programs' | **Flips for the actual target list** | Parity only near $400k balance; top-25 median is $2,221/account at 20 bps vs Ren $737 | EV-ADV-003 |
| 2 | '20 sponsors could alone cover fixed cost' | **Flips: 5, realistically ~2 decision units** | Cap at min(20 bps, $737/acct); NPT competitor, AEF just migrated, Greater Horizons = GKCCF group | EV-ADV-005 |
| 3 | Break-even ~$2.0B (5 sponsors, $150k) | **Understated** | Excludes platform build and sales: $2.87-3.15B with them | EV-ADV-006 |
| 4 | Capital $3.4M (anchor) | **Understated** | AI-native minutes from day one; full AI-enhanced $4.32M; +6-month delay $4.17M; build at Unbound base adds ~$4M+ [D: $5M less $0.72M] | ADV-003/004/027 |
| 5 | 'Anchor is the best entry route' | **Not shown** | Plans differ in AUA and balance; losing the anchor turns run-rate to -$0.24M | EV-ADV-011/012 |
| 6 | '$250 floor rescues small-balance books' | **Mislabelled** | That is a 30-45 bps price, and 7-18%/yr on small funds | EV-ADV-002 |
| 7 | 'CFs are attractive on balance' | **Contradicted** | 20 bps = median 11% of a top-25 sponsor's entire non-investment opex; Unbound EV-04 rejected CF entry | EV-ADV-004/015 |
| 8 | 'Redesign is the advantage' | **Temporary** | Unbound EV-02: incumbents can adopt most levers | EV-ADV-014 |

What survives: per-account cost drives viability; small-balance programs lose at any flat bps; conventional operation cannot be priced at 20 bps; captives and channels are not buyable; the prior $1,177,750 budget is a low case.

## ADV-2 Model audit: defects by file and line

Paths relative to `/home/user/daf-landscape/`. Full list with fixes in `findings.csv`. Effect sign: (+) makes the business look better than it is.

| ID | Location | Defect | Effect | Magnitude [D] | Fix |
|---|---|---|---|---|---|
| ADV-003 | Strategies.fs:70 | AI-native minutes from go-live; Unbound EV-08 says up to 8 sponsor authorisations come first | (+) | Capital anchor $3.40M -> $4.32M (all AI-enhanced); break-even $1.97B -> $6.56B | Approach ramp gated on delegation date |
| ADV-004 | Economics.fs:80-130; Strategies.fs:11-12 | Platform build: $0.72M in plans; not amortised in annual tables; Unbound base $5M ($3-15M) | (+) | Break-even -> $2.06B ($0.72M) / $2.87B ($5M) | Amortisation or internal licence line |
| ADV-005 | Parameters.fs:166; Strategies.fs:109 | No CAC: $42k sales + $20k marketing; no BD hire, RFPs, pilots | (+) | +$250k/yr -> $2.13B; with build -> $3.15B | CAC per sponsor + sales step |
| ADV-006 | Parameters.fs:128; Economics.fs:92 | 1,520 h treated as queue time; ACT uses 1,360 | (+) | -$110k/yr; $1.97B -> $2.04B | Utilisation 0.85-0.9 |
| ADV-007 | Economics.fs:95-98 | December overflow bought at loaded rate though annual FTE already include those hours; ignores 'temps cannot release', per-sponsor exclusivity and the 8x peak week | (-) $ / (+) control | $97.9k (3.3% of revenue) | Non-peak sizing + releaser bench step |
| ADV-008 | Parameters.fs:150,167 | Compliance officer triggered by AUA > $1B: market fall removes him | (+) | -$121,848 in -40/-50% stresses | Trigger on accounts or ratchet |
| ADV-009 | Parameters.fs:85-86 | One archetype mix rescaled to each sponsor's balance; workload balance-invariant | (+) high balance / (-) low | SVCF break-even 0.2 bps; $1,368 'small' funds at $75k books | Segment mixes; workload by balance band |
| ADV-010 | Economics.fs:134-139; Program.fs:131,138,154 | Sponsor contribution omits per-sponsor step costs (~$39.5k/sponsor + $7.38/acct + ops-manager uplift + peak) yet charges hours already in fixed | (+) small / (-) first | ~$40-60k (+); up to ~$214k (-) | Allocated contribution; one-sponsor P&L |
| ADV-011 | Analysis.fs:65 | Outflow stress lowers assets but not grant workload | (+) | n/q | Pair with VolumeFactor |
| ADV-012 | Analysis.fs:66 | Drop-largest only on 5 equal sponsors (20%); anchor plan = 60% | (+) | Run-rate $1.78M -> -$0.24M | Stress plans |
| ADV-013 | Strategies.fs:82-112 | Plans differ in AUA ($1.2-2.5B) and balance ($150-300k) | (+) anchor | C at $200k: $1.54M; D at $300k: $0.60M (vs $0.09M) | Normalise |
| ADV-015 | CashFlow.fs:47-49,81-90 | Full steady-state AUA at go-live; no ramp, attrition, churn, market path | (+) | ~$0.4-0.7M fees deferred on anchor [E] | Ramp + attrition |
| ADV-016 | CashFlow.fs:99,117 | 'Capital' includes 10% interest on negative cash | (-) | ~$0.2-0.3M [E] | Split |
| ADV-018 | Strategies.fs:139; Program.fs:163-178 | '$250 floor' plans are 30-45 bps prices | (+) price | 44.7 / 30.3 / 23.7 bps | Show effective bps |
| ADV-019 | Economics.fs:56 | Floor on archetype averages (Jensen) | (-) | small | Distribution |
| ADV-020 | Parameters.fs:46-78 | Rails (~$25.6/acct) and complex intermediary fees (~$10.8/acct) charged to servicer though CST/ACT say sponsor/fund-borne | (-) | ~$0.36M/yr at 10k accounts | One scope matrix for cost and comparator |
| ADV-021 | Parameters.fs:10 | No activity/exceptional fees (market charges them) | (-) | n/q | Activity fee schedule |
| ADV-022 | Economics.fs:44 | PassThrough flag drops cost unconditionally, never billed | latent | 0 now | Tie to price flag |
| ADV-023 | Parameters.fs:164 | Controller (reviewer) counted as 0.3 FTE preparer | (+) | up to 0.3 FTE | Separate queues |
| ADV-024 | Program.fs:170 | '$150k sponsor minimum' row inert at tested sizes | misleading | 0 | Drop/move |
| ADV-025 | Program.fs:131,154 | 'covers fixed alone' mixes marginal and fixed definitions | ambiguous | ~$99k | One-sponsor evaluate() |
| ADV-034 | tests/Tests.fs | No tests for monotonicity, step allocation, peak double count, effective bps, ramp | risk | - | Property tests |
| ADV-037 | Parameters.fs:96-102 | Flat 324 h/sponsor whatever size or SOC 1 scope | (+) large sponsors | n/q | Scale by accounts/feeds |
| ADV-038 | Parameters.fs:106 | Flat $105k onboarding for $20M and $1.5B sponsors | (+) anchor | up to +$220k one-time | Scale |

**Checked and found correct:** H0 reproduction and closed-form break-even; per-account floor semantics per archetype (each account pays max(fee, floor)); sponsor minimum top-up vs asset fee only; quarterly-in-arrears billing with 1-month lag; contribution in `evaluate` (revenue - external - added labour - peak - sponsor cost) is consistently defined; sponsor-retained decision minutes are excluded from servicer cost (ACT-1) and from revenue; donor-facing fees are never servicer revenue; average-asset proxy used, not EOY; `ceilSteps` started-block semantics; drop-largest by fee.

## ADV-3 Quantified re-runs (Python port of the F# core)

All [D] from `scripts/checks.py` (Model B, 20 bps, AI-native unless stated). Same-model port; reproduces the F# results first.

**Break-even AUA, 5 equal sponsors** (sustained crossing, $10M grid):

| Case | $150k avg | $250k avg | 20% margin at $150k |
|---|---:|---:|---:|
| As modelled | $1.97B | $1.50B | $3.16B |
| + build $0.72M / 5 y | $2.06B | $1.58B | $3.35B |
| + build $5M / 5 y (Unbound base) | $2.87B | $2.20B | $4.50B |
| + sales/CAC $250k/yr [A] | $2.13B | $1.64B | $3.44B |
| + build $1.0M/yr + sales $0.25M/yr | **$3.15B** | **$2.40B** | **$4.79B** |
| AI-enhanced (redesign not achieved) | $6.56B | - | - |
| Queue hours 1,360 | $2.04B | - | - |

**Single-sponsor sustainers** (active, captive_status none_found; contribution >= $1.74M Model B fixed): 20 at 20 bps; **5** if the buyer pays min(20 bps, $737/account); **2** at min(20 bps, $400). The 5: AEF (migrated to Ren 2026-04), Greater Horizons and GKCCF (one group), JCF, NPT (competitor).

**What 20 bps means to the sponsors on the target lists** (latest 990 operating cost excluding investment management, `sponsor-cost-structure.csv`):

| List | Median $/account at 20 bps | Median fee as % of sponsor's whole non-investment opex | Notable |
|---|---:|---:|---|
| SPN top-25 | $2,221 | 10.8% | GiveWell CF 85%, CF SW Washington 23%, Chattahoochee 32% |
| Self-sustaining list | $1,918 | 20.1% | JCF 71% (25 employees), Greater Horizons 90%, ICGF 77% (ratio meaningless for 0-employee captives) |

**Anchor plan anatomy:** run-rate C $1.78M; without anchor -$0.24M; anchor alone $0.74M; anchor alone AI-enhanced $0.03M; anchor alone after -30% assets -$0.16M. **Confound:** C with anchor at $200k $1.54M; D at $300k $0.60M (vs $0.09M).

**Floor:** effective 44.7 / 30.3 / 23.7 bps at $75k / $150k / $300k average balance.

## ADV-4 Perspective: incumbent competitor (Ren/Stellar, TIFIN Give, NPT/AEF private-label)

**Strongest objections**
1. *'We need not cut price where you can make money.'* Ren already earns 18.5 bps at MS GIFT (EV-PRC-003); 20 bps is not cheaper there. At USCGT matching 20 bps would cost Ren $2.2M/yr (PRC (g)), but USCGT's balances (~$107k) are exactly where 20 bps is below the entrant's cost (results.md: no break-even at $100k below 20 bps without floors).
2. *'Your levers are our policy options.'* Unbound EV-02 (EV-ADV-014): without redesign levers the entrant is about equal to an AI-enhanced incumbent; reuse, EFT default, deferral and continuous monitoring are policies anyone can adopt. Break-even gap AI-native vs AI-enhanced ($1.97B vs $6.56B) is the whole moat and it is copyable.
3. *'We own the installed base.'* Five of SPN's top-25 run Ren/Stellar iPhi (Memphis, Louisville, Minneapolis, Saint Paul, Cleveland); Ren can bundle managed services at marginal cost onto software sold at 0.5-9 bps (EV-PRC-013) and re-tier small accounts.
4. *TIFIN:* cross-subsidises service fees from management/model-sponsorship fees (ADV, PRC (g)); can drop 30 -> 10-20 bps.
5. *NPT/AEF private-label:* a client need not be a sponsor at all; a private-label DAF moves 990, audit and board burden to the national sponsor, a stronger offer for small programs than 'you keep legal ownership and reserved decisions' (integrator 02 notes NPT sells private-label/outsourced services).

**Evidence for the entrant:** documented Ren/iPhi and Blackbaud attrition (SPN 'Attractive portfolio members'); MSA friction (auto-renewal, change orders, termination fees, EV-PRC-031) is a portability wedge. **Against:** above.
**What would change their mind:** losing two or more renewals to the entrant at their own price; a SOC 1 Type 2 and a referenceable sponsor.
**Most threatened conclusion:** '20 bps is a credible competitive price' and 'redesign is the advantage'.

## ADV-5 Perspective: skeptical investor

**Strongest objections**
1. *No demand evidence.* Zero buyer conversations, LOIs or WTP data; every passes' 'same-model' caveat; AC-01/06/09 unsupported (ECH CL-3).
2. *Capital is understated by construction.* AI-native from day one, $0.72M build vs Unbound $5M, no CAC, flat onboarding: realistic capital is $4-9M+ [D: EV-ADV-006/007, results.md delayed/AI-enhanced rows], not $3.4M, before the build gap.
3. *The revenue pool is thin.* Under per-account parity only ~2 independent decision units can carry fixed cost alone; the 149-sponsor 'attractive' band has median 20 bps revenue ~$0.4M margin (SPN), so the company needs 5-15 wins, each a 12-24 month enterprise sale [A].
4. *Two-sided price trap.* Where 20 bps is profitable (high balances) it is above market per account; where it is a discount (small balances) it is below cost (PRC (e)).
5. *Concentration and market beta.* Anchor plan: -$0.24M without the anchor; anchor alone loses money after a 30% fall (EV-ADV-011).

**For:** large addressable assets ($151B average, non-captive), real incumbent friction, low AI cost, possible per-account repricing.
**Change of mind:** 3 signed design partners with per-account pricing >= $500 and delegation commitments; measured minutes at a partner within 1.5x of base.
**Most threatened:** 'minimum viable organisation and capital' (03, cash-flow table).

## ADV-6 Perspective: sponsor CFO

**Strongest objections**
1. *Price vs avoided cost.* For a $1.1B-average-balance CF, 20 bps is ~$2,200 per fund-year and a median ~11% of our whole non-investment operating budget (EV-ADV-004); I would not save that much by outsourcing DAF processing. I would ask for $/fund pricing or steep tiers.
2. *I keep the expensive part.* Reserved decisions, board delegations (up to 8 authorisations, EV-ADV-013), audit, donor relations and exceptions stay with my staff; the fee replaces only processing.
3. *Transition cost and stranded cost.* 3-5 year software contracts (SPN), parallel run, staff redeployment; onboarding $35-325k (CST) plus my staff time; savings arrive in year 2-3 at best.
4. *Fee stacking.* A servicer fee + my margin + investment fees must remain competitive with Fidelity/Schwab donor schedules (60/30/20/15 bps tiers, PRC (d)).
5. *Downside sharing.* The servicer wants minimums (AC-09) while my revenue falls with markets.

**For:** variable cost replaces fixed staff; SOC 1 evidence; no termination fee and data portability would de-risk.
**Change of mind:** a quote at or below my current DAF processing cost per fund, with a ramp and exit rights.
**Most threatened:** SPN/02 top-25 ranking and the CF-entry thesis (also Unbound EV-04).

## ADV-7 Perspective: sponsor board member

**Strongest objections**
1. *Fiduciary and vendor risk.* Outsourcing core operations to a 5-6 person startup with no SOC 1 history, no running platform (ECH-1) and $84k insurance (CST) against a $1B+ book.
2. *Delegation liability.* Redesigned economics require us to delegate routine approvals to deterministic rules (RC-ACT-007); a taxable-distribution or sanctions miss is our liability (replay: 12/100 perturbed listed names missed, ECH AC-04).
3. *Mission optics.* Asset-based servicer fees and floors on small funds (7-18%/yr on the smallest, EV-ADV-002) and December grant deferral conflict with our grantmaking mission (AC-10/11).
4. *Continuity.* Concentration: if the servicer depends on us for 60% of its revenue (anchor plan), its failure is our operational incident.

**For:** sponsor keeps legal ownership; evidence-rich controls; portability.
**Change of mind:** escrowed data and runbooks, step-in rights, insurance limits sized to AUA, independent control assurance, payout-neutral fee design.
**Most threatened:** 'an anchor can be acquired within runway' (AC-06).

## ADV-8 Perspective: controller (sponsor or servicer)

**Strongest objections**
1. *Billing base.* 'Average billable AUA' needs daily/month-end balances from custodians the servicer does not control; definitions (cash, legacy pools, >$100M accounts) are unknown (PRC (f)); avg proxy is 91.6% of EOY (SPN).
2. *Revenue recognition.* Asset-based fees are variable consideration recognised as earned; floors/minimums and implementation fees need separate performance-obligation analysis; the model treats implementation fees as cash, not deferred revenue (CashFlow.fs).
3. *SoD in the model.* Controller counted as preparer (ADV-023); only one releaser pair at Model B.
4. *SOC 1 timing.* Type 2 needs an operating period; sponsors' auditors may refuse go-live without it (CST Insurance and assurance) - a sales-cycle risk not in the plans.
5. *Boundary.* Payment rails and intermediary fees are servicer cost in the base model but sponsor/fund-borne per CST/ACT (ADV-020).

**Change of mind:** a contract template defining billable base and pass-throughs; SOC 1 Type 1 before go-live with bridge letters.
**Most threatened:** cost boundary used in every margin table.

## ADV-9 Perspective: operations manager

**Strongest objections**
1. *December is a control problem, not an hours problem.* 3.1-3.3x daily load, ~8x in peak week, ~10 ops FTE-eq at 5,000 accounts at same SLA (ACT-9); temps 'can only prepare, not release' (CST-P14); surge reviewers sponsor-exclusive (RC-ACT-002). The model buys hours at $65.45 (ADV-007).
2. *Day-one minutes.* AI-native minutes assume delegations, EFT enrolment, reuse history and clean feeds that a new client lacks (ADV-003).
3. *Utilisation.* 1,520 h are not 1,520 queue hours (ADV-006).
4. *Tails.* 20% of accounts drive ~60% of AI-native minutes (ACT-10); one complex gift is 2-30 h.
5. *Absence.* Six people, one controller; a December absence breaks dual control.

**Change of mind:** a December roster simulation with double absence that passes; a measured migration at a design partner.
**Most threatened:** staffing steps and cost per account at go-live.

## ADV-10 Perspective: compliance professional

**Strongest objections**
1. *Regulatory status unresolved* (money transmission/agent of payee, state charitable solicitation, CST-C08) - a launch gate, not a $40k line (ADV-032).
2. *Screening safety vs cost.* Deterministic clearance and reuse lower minutes but the reference matcher missed 12 of 100 perturbed listed names; IRS revocation posting lag median 89 days (ACT-11). Cost targets must not set recall thresholds.
3. *180-day re-verification redesign* depends on sponsor counsel approving automatic renewal on unchanged evidence (ACT-11 conditions); unlisted recipients (churches, some fiscal sponsors) still need humans.
4. *Data sharing.* A cross-sponsor 'evidence network' may breach sponsor confidentiality and Candid licence terms (EV-ADV-020).
5. *Incentive conflicts* (AC-11) need written policies the auditor can test.

**Change of mind:** counsel opinion; seeded recall tests at 100% on listed names; written board delegation templates.
**Most threatened:** AC-04 automation and AC-08 boundary.

## ADV-11 Perspective: customer (donor and advisor)

**Strongest objections**
1. *Fee stacking and floors.* A $250 floor on a $5,000 fund is 5%/yr before the sponsor's margin and investment fees; market minimums are $100-360 (PRC (d)).
2. *Service changes.* EFT default, structured intake and December deferral (up to 10 business days) change what donors experience; 'no December 31 deadline for grants' is true legally but not to donors' expectations.
3. *Migration risk.* Statement history, recurring grants, advisor feeds and tax receipts must survive migration.
4. *Advisor economics.* In wealth channels the advisor's 60-100 bps advisory relationship decides; a servicer that is neutral on investments adds nothing to the advisor and may threaten platform integration (PRC (g)).

**For:** better status visibility (fewer 'where is my grant' contacts), faster standard grants.
**Change of mind:** fee caps, no floor on dormant/small funds, unchanged advisor feeds.
**Most threatened:** floor-based hybrid pricing.

## ADV-12 Perspective: charitable beneficiary

**Strongest objections**
1. *Slower December money.* Deferral to January shifts cash timing for recipients whose year-end appeals fund operations (ACT-9).
2. *EFT default excludes small charities.* Open networked rails reach an estimated 15-25% of charities by count (EV-ADV-018); EFT-by-default must not mean delayed checks for the rest.
3. *False exceptions.* Most replay exceptions are recipients IRS lists do not cover (churches etc., EV-ADV-019); deterministic rules can systematically slow small, religious or new charities.
4. *Retention incentive.* Asset-based fees on both sponsor and servicer layers reward keeping money in DAFs.

**Change of mind:** published grant-latency and exception-rate metrics by charity type; a payout-neutral fee base.
**Most threatened:** cost savings from deferral and EFT default (ACT-4/9).

## ADV-13 Clarity-structured challenge of AC-01..AC-13

Rows AC-01..AC-13 in `assumption-challenge-adv.csv` fill every template column (34) and add `adv_conclusion_would_flip`, `adv_flip_condition`. EDF columns state non-applicability and an adjacent observed outcome; no EDF diagnosis was run. Not a certified Clarity review.

| ID | Assumption | Claim state | Conf. | Posture | Flips a conclusion? |
|---|---|---|---|---|---|
| AC-01 | Sponsors pay ~20 bps | unsupported | Low | Experimental | **Yes**: '$250k+ credible', '20 sustainers' |
| AC-02 | 5-person core | unsupported | Low | Guardrail | Partly (utilisation, SoD) |
| AC-03 | $75/account | unsupported | Low | Experimental | Yes for small sponsors |
| AC-04 | Automation keeps handling low | suggestive (eligibility) / unsupported | Low | Guardrail | **Yes**: capital and all break-evens if gates delay redesign |
| AC-05 | Echelon lowers cost | unsupported | Low | Strategic | **Yes** if build is attributable ($2.87B) |
| AC-06 | Anchor within runway | unsupported | Low | Strategic | **Yes**: 'anchor best route' |
| AC-07 | Balance high enough | internal-demonstration (EOY) | Low | Experimental | No (magnitude only) |
| AC-08 | Outside custody/advice regulation | suggestive (design) | Low-Med | Guardrail | Yes if licensing needed |
| AC-09 | Minimum fees | unsupported | Low | Experimental | No |
| AC-10 | Per-account floor fair | unsupported | Low | Guardrail | **Yes**: hybrid table 'floor rescues small books' |
| AC-11 | No outcome-harming incentives | unsupported | Low | Guardrail | Board acceptability |
| AC-12 | Anchor concentration acceptable | unsupported | Low | Strategic | **Yes** |
| AC-13 | '20 bps = parity with Ren' | suggestive (arithmetic) / unsupported (parity) | Med/Low | Experimental | **Yes** for CF targets |

**Cross-cutting:** the most frequent failure pattern is Confidence Debt (prices and minutes used in plans before any buyer or time-study evidence), followed by Burden Externalization (decisions to sponsors, engineering to Echelon, fees to donors, timing to charities).

## ADV-14 Incentives and charitable outcomes: safeguards and pricing by party

**Safeguards (contract and product design)**

| Safeguard | Mechanism | Cost to servicer [E] | Who benefits |
|---|---|---|---|
| Fee base excludes approved-unpaid grants and in-transit contributions | Billable AUA = balance - approved grants not yet paid | ~0.1-0.5% of revenue (approved balance x days outstanding) | Charities, donors |
| Payout-neutral component | e.g. bps on AUA + $/grant paid or bps on (AUA + trailing 12m grants); revenue does not fall when payout rises | Neutral if calibrated | Charities; aligns cost and revenue (grants drive cost, ACT-10) |
| Grant-latency SLA with December cap | Standard grants <= 5 business days; December <= 10 with published metrics | Higher December bench (ADV-007/033) | Charities |
| Complex-gift policy | Sponsor-set acceptance policy; activity fee or fund-borne intermediary charge disclosed up front; servicer cannot refuse on cost | Revenue-neutral with activity fee | Donors with illiquid assets |
| Floor cap | Per-account floor <= 1% of balance (A-ADV-006); no floor on dormant funds subject to sponsor sweep-to-charity policy | Small; floor revenue shifts to activity fees | Small donors |
| Minimum-fee caps | Sponsor minimum <= a stated share of fee at signing; downturn step-down | Lower downside protection | Sponsor |
| Transparency | Publish effective bps and $/account by band, exception rates by charity type, latency, fee waterfall to donors | Reporting only | All |
| No retention incentives | No fee share on investment products; no penalties on sponsor sweeps or spend-down funds | Forgoes upside | Charities |

**Pricing seen by each party (20 bps base)**

| Party | Gain | Loss / risk | Net view |
|---|---|---|---|
| Servicer | Revenue scales with markets and high balances | Revenue falls with payout and markets while work rises; tails unpriced | Wants per-account + activity pricing, which is also fairer |
| Sponsor | Variable cost, controls evidence | At high balances pays $1.9-2.2k/fund (EV-ADV-003); keeps decisions and transition cost | Accepts only below avoided cost: per-account or tiered |
| Donor | Possibly lower total fee if sponsor passes savings | Floors (5-18%/yr on small funds), deferral | Neutral to negative unless caps |
| Advisor | None directly | Platform change risk | Neutral/negative in wealth channels |
| Recipient charity | Faster standard grants, fewer status queries | December deferral; EFT-default exclusion; false exceptions for unlisted charities | Positive only with latency SLA and non-EFT parity |

**Reading.** The pricing that is fairest (per-account plus activity fees, payout-neutral) is also the one that best matches cost (ACT: workload follows grants and exceptions, not assets). Asset-only pricing is both the least fair and the least robust.

## ADV-15 Competitive response: durable vs temporary advantages

| Claimed advantage | Durable or temporary | Why | Incumbent response | Evidence |
|---|---|---|---|---|
| Shared charity-verification evidence network (reuse across sponsors) | **Temporary to weak** | Eligibility data is commodity (IRS BMF, OFAC); enriched data is licence-constrained (Candid); cross-sponsor sharing needs consent; incumbents at scale already have more recipient overlap (Fidelity ~13.2 grants per charity, ACT-2) | Adopt reuse policy (EV-02) | EV-ADV-014, EV-ADV-020 |
| Integrated accounting controls (ledger + SOC 1 evidence) | **Moderately durable if delivered**, but currently incumbent-favoured | Auditor trust accrues over years of clean reports; entrant has none; build cost $3-15M | Point to their SOC history; FUD on startup risk | ECH-1/3, CST assurance |
| Reusable sponsor configuration | **Temporary** | Lowers onboarding ($105k flat today) but templates are copyable; incumbents monetise change orders, so they may resist - counter-positioning lasts only while their revenue depends on it | Waive change orders for at-risk clients | EV-PRC-031 |
| Lower operational complexity (redesign: delegation, EFT default, continuous monitoring, deferral) | **Temporary** | Policy changes; EV-02 says incumbents can adopt several | Adopt same policies; re-tier | EV-ADV-014 |
| Portability (no termination fee, full export) | **Durable as positioning**, easy to match technically | Incumbent MSAs earn renewal and exit friction; matching it hurts them | Match for large clients only | EV-PRC-031 |
| Price | **Not an advantage** at high balances; unsustainable at low balances | See ADV-1 | Do nothing (MS GIFT); re-tier small accounts; bundle software at marginal cost; cross-subsidise from advisory/management fees | PRC (g) |

**Likely incumbent moves, in order of cost to them:** (1) do nothing where already at ~18 bps; (2) re-tier small-account minimums and repricing at renewal; (3) early multi-year renewals with discounts and waived change orders for clients showing attrition signals (retention incentives); (4) bundle 'managed services' onto Stellar/iPhi at marginal cost; (5) channel owners (banks, TIFIN) absorb admin cost to keep advisory assets; (6) acquire or copy. **Durable position, if any:** a per-account-priced, payout-neutral, portable offer with published control and outcome metrics - hard for incumbents whose revenue depends on bps and exit friction - plus measured (not claimed) unit cost.

## ADV-16 Conclusions most likely wrong and cheapest evidence

Ranked by (probability wrong x consequence). 'Cheapest evidence' excludes paid data; permissioned data named where needed.

| Rank | Conclusion | Why likely wrong | Cheapest evidence that settles it |
|---|---|---|---|
| 1 | Sponsors will pay 20 bps flat on high-balance books | Per-account equivalent is 2.5-3x market at target balances (EV-ADV-003) | 5-10 owner-led sponsor CFO conversations quoting both bps and $/fund; public CF board packets/RFPs (free); **permissioned:** a sponsor's current vendor invoices |
| 2 | AI-native minutes apply from go-live | Activation gates (EV-08) | One design partner: date of board delegation adoption; **permissioned:** 90-day event log (ACT-14 item 1) |
| 3 | Capital ~$3.4M | Build, CAC, gates, delays omitted (ADV-003/004/005/027) | Re-run plans with ramp + build; no new data needed |
| 4 | ~20 single-sponsor sustainers / anchor is attainable | Cap and exclusions leave ~2 (EV-ADV-005) | Public: vendor renewal dates and migration events (repo files), 990 Part VII-B vendor lines; then 15-20 interviews |
| 5 | Break-even ~$2B | Excludes build and sales ($3.15B with them) | Decide build ownership (Unbound licence vs own); no data needed |
| 6 | CFs are attractive targets | Fee vs opex (EV-ADV-004); Unbound EV-04 | Public 990 Part IX staff lines per CF; **permissioned:** CF DAF staffing and fund-type counts |
| 7 | $250 floor makes small books viable | It is a 30-45 bps price and harms small funds | **Permissioned:** one sponsor's fund balance distribution |
| 8 | Redesign is a lasting advantage | Incumbents can adopt (EV-02) | Track incumbent policy changes (public donor circulars, e.g. EFT default, SLA disclosures) |
| 9 | December handled by buying hours | Release authority not purchasable | Public: sponsor December processing disclosures; **permissioned:** December roster/backlog at a partner |
| 10 | Payment rails are servicer cost (or not) | Boundary inconsistent (ADV-020) | Counsel opinion (CST-C08) + one bank's third-party-initiation terms (public product docs) |
| 11 | 20 bps = parity with Ren | Scope and channel differ (AC-13) | Public MS GIFT circulars (scope of TPA vs MSSB); Ren product pages |
| 12 | Sponsor-level work 324 h | Flat across sizes | **Permissioned:** close/audit hours at one sponsor |

## ADV-17 Files, top findings and gaps

**Files (in `scratchpad/svc/adv/`):** `report.jsonl` (this, 18 sections), `findings.csv` (38 rows ADV-001..038), `evidence.jsonl` (23 EV-ADV), `assumptions.jsonl` (8 A-ADV), `assumption-challenge-adv.csv` (13 rows: AC-01..AC-09 plus AC-10 floor fairness, AC-11 incentive conflicts, AC-12 anchor concentration, AC-13 Ren parity; 34 template columns + 2), `scripts/port.py`, `scripts/checks.py`, `scripts/build_adv.py`, `scripts/report_text.py` (run `python3 -I -B scripts/checks.py /home/user/daf-landscape`).

**Five most consequential findings**
1. The 20 bps parity claim is balance-bound: at the actual target list it is ~$2,200/account, 3x Ren's $737; under a per-account cap, single-sponsor sustainers fall 20 -> 5 -> ~2 decision units.
2. Every cash plan uses AI-native minutes from go-live; Unbound's own EV-08 says activation gates come first. Redesign not achieved = break-even $6.56B.
3. Platform build and sales are effectively uncosted: break-even $1.97B -> $3.15B with Unbound's base build amortisation and $250k CAC.
4. Strategy ranking is confounded by AUA and balance; the anchor plan's lead partly comes from assuming a $300k-balance anchor, and losing it leaves -$0.24M/yr.
5. '20 bps + $250 floor' is a 30-45 bps price that charges small funds 7-18% a year; per-account + activity + payout-neutral pricing is both fairer and better matched to cost.

**Model defects to fix first:** approach ramp (ADV-003), build/CAC lines (ADV-004/005), asset-triggered compliance step (ADV-008), allocated sponsor contribution (ADV-010), strategy normalisation (ADV-013), effective-bps reporting (ADV-018), scope matrix (ADV-020).

**Biggest open gaps:** any buyer price evidence; sponsor balance distributions; a time study; delegation lead times; counsel opinion on payments; build ownership and cost. Same-model review: not independent validation.

## EDF/CL-0 Framework sources and revisions

| Framework | Repository @ revision | Files used |
|---|---|---|
| Clarity | /home/user/clarity-framework @ 200a9eb | rules.md (Constitution, admissibility lint, operational test); docs/assessor-guide.md; decision-posture-model.md; decision-record.md; docs/reconsideration-criteria.md; docs/progressive-commitment.md; docs/framework/concept-layers.md; docs/concepts/concept-maturity.md; docs/templates/clarity-result-template.md; docs/foundation/clarity-constitution.md; research/2026-framework-improvement/README.md and protocols/arm-D2-clarity-lean-1.1.md (experimental) |
| EDF v0.3 | /home/user/kemiller2002/echelon-diagnostic-framework @ 710d54c | docs/edf/specification.md; docs/edf/templates/edf-1-standard.md (and edf-0/edf-2); docs/edf/diagnostic-calibration.md; docs/edf/operating-cycle.md; docs/framework-engineering/claim-and-confidence-policy.md v1.0 |
| Application notes | daf-landscape @ e1a3633 | research/mission-2026-11-14/clarity-edf-application-guide.md (pinned to Clarity 8cd48019 / EDF 41fea6f); research/commercial-opportunity/clarity-edf-analysis/assumption-tests.md (Clarity 200a9eb / EDF 710d54c) |

Both local clones are shallow single-commit; the guide's older pinned commits are not present, so changes between them and the revisions used cannot be diffed here. **Rule IDs:** neither framework defines numbered rule IDs. Clarity's rules are the unnumbered 13-item admissibility list (rules.md:44-58), six commitments (rules.md:20-38) and the operational test (rules.md:86-90); 'CL-1'/'CL-1.1' are experiment-arm IDs for Clarity Lean, not rules. EDF has a nine-step required sequence and 15 required output elements. Step IDs in `framework-procedure.jsonl` (CL-xx, EDF-xx) are assigned by this group for traceability and are not framework identifiers.

## CL-1 Clarity procedure (as the documents define it)

Core questions: What is being treated as true? What currently justifies that? What would make us reconsider? (assessor-guide.md:17-21). Assessment depth: Level 0-3, smallest sufficient for the risk. Steps extracted (see `framework-procedure.jsonl` CL-01..CL-15):

| Step | Name | Required outputs |
|---|---|---|
| PRE-01 | Pin revisions and division of labour | clarity_revision, edf_revision, files_read |
| CL-01 | Admissibility screen (lint) | admissibility_result, violations_found, restated_claim |
| CL-02 | Foundational commitments check | causal_mechanism, entry_signal, incentives, bounds, tradeoffs |
| CL-03 | Operational test | operational_test_result, conditions_it_depends_on |
| CL-04 | Select assessment effort level (Progressive Commitment) | assessment_level, level_rationale |
| CL-05 | State the claim and its posture | claim, claim_posture |
| CL-06 | Evidence review | supporting_evidence, contradictory_evidence, evidence_admissibility_notes |
| CL-07 | Assumptions (explicit and shadow) | hidden_assumptions, dependencies |
| CL-08 | Confidence and proportional certainty | confidence, proportional_certainty_note |
| CL-09 | Ownership | owner |
| CL-10 | Decision posture (impact x correctability) | impact_if_wrong, correctability, decision_posture |
| CL-11 | Monitoring signals, thresholds, triggers | monitoring_signal, threshold, trigger_claim, operational_response, trigger_reassessment |
| CL-12 | Reconsideration criteria | reconsideration_criteria, falsifying_evidence |
| CL-13 | Failure detection, boundaries and commitment outcome | failure_conditions, decision_boundaries, recommended_commitment, review_trigger |
| CL-14 | Failure-pattern check | failure_pattern_risk |
| CL-15 | Result write-up | result_sections |

Concept maturity matters: Core = Claim, Evidence, Assumption, Confidence, Ownership, Reassessment, Correctability, Proportional Certainty, Confidence Debt; Candidate = Burden Externalization, Governance Debt, Resolution Debt, Trigger Claim; Research = Trigger Drift, Signal Quality, Modes of Success, Calibration (concept-maturity.md). **Limits stated by Clarity itself:** 'The goal is not to complete a worksheet' (assessor-guide.md:5,156); its own 2026 benchmark found current Clarity 'no more accurate' than the same model with no method and much less useful, with one clear strength: making assumptions explicit (research/2026-framework-improvement/README.md). Clarity Lean (CL-1.1) is EXPERIMENTAL and is used here only as the source of 'strongest rival' (alternative explanations).

## EDF-1 EDF procedure and where it does not apply

Required sequence (specification.md:39-54): System Context (Primary System, Context, Focus) -> Outcome (factual) -> Manifestations -> Origin Network (technical, human, organizational, environmental, financial, regulatory) -> Propagation (physical, informational, organizational, financial, human) -> Evaluate Evidence (observation vs inference) -> Control Points -> Rank (influence, controllability, cost, confidence) -> Diagnostic Sufficiency. Required outputs add Confidence, Unknowns, Next Responsible Action (specification.md:150-168). Claim policy: states internal-demonstration / suggestive / unsupported / contradicted / falsified / superseded / planned; confidence Low..High, qualitative (claim-and-confidence-policy.md:47-73).

**Inapplicable steps.** The nine servicing assumptions are hypotheses about a company that does not exist; EDF step 2 requires a factual outcome, so EDF steps 2-5 and 7-9 cannot be applied to them. EDF was not executed on any assumption. Each template row instead names an *adjacent observed outcome* (e.g. RCF's FY2024 payments to Ren; 12/100 sanctions misses in the public replay; cost per grant $55-$419) on which an EDF-0/EDF-1 could be run. Only the claim-state/confidence vocabulary and the evidence-separation rule (step 6) are applied to the assumptions. Diagnostic Calibration is not applicable as evidence: lenses from one model are not independent replications (diagnostic-calibration.md). EDF's own README states it does not yet establish cross-executor reproducibility or incremental value.

## CL-2 Template columns and their provenance

File `assumption-challenge-template.csv`. Columns the mission requested but the frameworks do not define are marked; they are kept because the mission asked for them, not because the frameworks require them.

| Column | Source |
|---|---|
| assumption_id | mission |
| assumption_statement | Clarity Claim (CL-05) |
| working_value | mission |
| claim_posture | Clarity Postures (CL-05) |
| assessment_level | Clarity assessor-guide levels (CL-04) |
| admissibility_result | Clarity rules.md admissibility (CL-01) |
| operational_test | Clarity rules.md operational test (CL-03) |
| supporting_evidence | Clarity Evidence (CL-06) |
| contradictory_evidence | Clarity Evidence 'challenges' (CL-06) |
| evidence_admissibility_notes | Clarity decision-record §5 relevance/incentives/proximity/verifiability (CL-06) |
| hidden_assumptions | Clarity shadow assumptions (CL-07) |
| causal_mechanism | Clarity Mechanism First (CL-02); EDF Propagation analogue |
| alternative_explanations | Clarity Lean 'strongest rival' (experimental, CL-L); not in core Clarity or EDF spec |
| incentives | Clarity Incentives Over Intent (CL-02); decision-record evidence incentives |
| feedback_loops | mission-added; no framework construct (EDF propagation is the nearest) |
| dependencies | mission-added; recorded under Clarity assumptions (CL-07) |
| failure_conditions | Clarity decision-record §8 Failure Detection (CL-13) |
| counterfactuals | mission-added; no framework construct |
| falsifying_evidence | Clarity Reconsideration Criteria (CL-12) |
| claim_state | EDF claim policy (EDF-POL) |
| confidence | EDF confidence labels (EDF-POL); Clarity Confidence (CL-08) |
| owner | Clarity Ownership (CL-09) |
| impact_if_wrong | Clarity posture (CL-10) |
| correctability | Clarity posture (CL-10) |
| decision_posture | Clarity posture (CL-10) |
| monitoring_signal | Clarity (CL-11) |
| threshold | Clarity (CL-11) |
| trigger_claim | Clarity Trigger Claim, Candidate (CL-11) |
| trigger_reassessment | Clarity (CL-11) |
| failure_pattern_risk | Clarity concept-layers failure patterns (CL-14) |
| edf_applicability | EDF-02 factual-outcome requirement |
| edf_adjacent_observed_outcome | EDF-01..09 candidate |
| recommended_commitment | Clarity decision-record §10 (CL-13) |
| evidence_paths | mission |

## CL-3 Pre-filled challenges of the nine servicing assumptions (summary)

Ordinary adversarial analysis structured by Clarity fields and labelled with EDF claim states. It is **not** a formal Clarity review (no decision owner sign-off, no review cadence) and **not** an EDF diagnosis. Full rows in the CSV.

| ID | Assumption | Claim state (EDF policy) | Confidence | Posture (Clarity) | Commitment |
|---|---|---|---|---|---|
| AC-01 | Sponsors will pay about 20 bps a year on average billable AUA for outsourced DAF administr... | unsupported (for this servicer); suggestive (that a 10-37 bps market exists) | Low-Medium | Experimental for price discovery; Strategic for the first multi-year contract | Continue Experiment |
| AC-02 | A five-person fixed core (MD/sales, technical lead, engineer, controller, grant/client ope... | unsupported | Low | Guardrail (controls) / Experimental (staff plan) | Delay (hiring plan) until time study |
| AC-03 | Incremental cost is about $75 per fund-year above the fixed budget. | unsupported | Low | Experimental | Continue Experiment |
| AC-04 | Automation (deterministic eligibility rules, determination reuse, AI flagging) keeps human... | suggestive (eligibility component, public data); unsupported (overall handling) | Medium (eligibility); Low (overall) | Guardrail | Continue Experiment |
| AC-05 | Shared Echelon infrastructure lowers the servicer's engineering, platform and administrati... | unsupported (cost reduction); suggestive (UI/print/test reuse) | Low | Strategic | Delay dependency commitment; Continue Experiment for UI/print |
| AC-06 | An anchor sponsor (~$1B AUA) can be acquired within the funding runway. | unsupported | Low | Strategic | Continue Experiment (interviews) before capital commitment |
| AC-07 | Average billable balance per account is high enough (~$200k) that bps revenue exceeds per-... | internal-demonstration (EOY figures); unsupported (average billable) | Medium (EOY); Low (billable average) | Experimental | Continue Experiment |
| AC-08 | The servicer stays outside custody, advice and fundraising regulation: sponsor keeps owner... | suggestive (design rule); unsupported (legal conclusion) | Low-Medium | Guardrail | Escalate (counsel) before contract |
| AC-09 | Sponsor contracts will carry minimum annual fees (or minimum AUA commitments) that cover f... | unsupported | Low | Experimental | Continue Experiment |

**Cross-cutting reading.** None of the nine is supported for this servicer. Four are unsupported outright (AC-02 lean staffing, AC-03 $75/account, AC-06 anchor acquisition, AC-09 minimums). Five have support only for a narrower claim: AC-01 (a 10-37 bps market exists, not that this servicer can charge 20), AC-04 (eligibility component only, measured on public recipient rows, not grants), AC-05 (UI/print/test reuse, not cost reduction), AC-07 (year-end filings, not average billable), AC-08 (a design rule, not a legal conclusion). The assumptions are coupled: the 5-FTE core (AC-02) depends on automation (AC-04) and on an unpriced platform (AC-05); revenue depends jointly on price (AC-01), balances (AC-07) and minimums (AC-09). Burden Externalization (Candidate) is the most frequent failure pattern: leanness is partly produced by moving decision cost to sponsors and engineering cost to Echelon.

## Framework revisions used

| Repository | Revision |
|---|---|
| clarity-framework | 200a9eb (200a9ebf029c051eac625bb5185929b20c8d5aed, 2026-11-16) |
| echelon-diagnostic-framework | 710d54c (710d54c20e935db8b6f75f9c60ee7217f0cb0e32, 2026-11-17) |
| Echelon-AI-Native-Enterprise-Design-Framework | 763ff8c (2026-11-20) |
| AI-Engineering | 1bc519b (2026-09-30) |
| unbound | 9b38de4 (2026-11-24) |
| daf-landscape | e1a3633 (2026-11-25) |
