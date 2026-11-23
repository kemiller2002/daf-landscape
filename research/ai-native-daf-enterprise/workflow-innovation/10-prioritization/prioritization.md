# Prioritization

**Rule (brief §14):** rank on ten visible dimensions and keep **five separate rankings**. No single opaque score.

**Inputs:**
- the post-audit [innovation register](../02-creative-hypotheses/innovation-register.csv) (verdicts and maturity after audit);
- the [validation evidence register](../08-experiments/validation-evidence-register.csv);
- [experiments](../08-experiments/experiments.md);
- [economic validation](../09-economic-validation/economic-validation.md);
- [adversarial review](../07-adversarial-reviews/adversarial-review.md).

Ratings are H/M/L judgments with the reason shown, made **after** evidence and criteria were fixed. Where a rating rests on an assumption, the cell says [A].

## 1. Dimension table (innovations that survived the audit, plus the strongest "insufficient evidence" items)

| INN | Innovation | Magnitude | Evidence quality | Tech feasibility | Regulatory feasibility | Implementation cost | Operational risk | Reusability (functions × sponsors) | Commercial potential | Time to validation | Defensibility |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 05 | Risk-tiered policy-as-code approval | H (removes per-grant touch for most grants) | M (parent PoC L3; ranking vs manual parameter-driven, E2) | H | M (board-approved policy; regulator reading untested) | M | M (misconfiguration at scale → canaries) | H × H | H (core of Model C) | M (shadow replay, Phase 3) | M |
| 01/03/34 | Diff-driven recipient passport plus pre-verified universe plus list-change rescreen | M (latency, dated evidence) | M (E1 arithmetic; IRS cadence sourced) | H | H (Rev. Proc. 2018-32 reliance) | L | L | H × H | M (by-product; crowded: Candid, Chariot) | Short | L |
| 08 | Grant ID in remittance | M (moves ~90% of recipient matching off nonprofits [A]) | M (problem: EV-086; benefit [A]) | H | H | L | L | M × H | L (feature) | Short | L |
| 26/16 | Capped delegated principals for donor agents and advisors | M | M (INV-A6 tested; theft and expiry untested → L2) | H | H | L | M | H × H | M | Short | M |
| 18 | Always-migrated record (replay) | M (removes migration history loss, EV-037) | M (premise evidenced; prototype by construction) | M | H | M | M (schema semantics) | M × H | H (lowers switching cost into the platform) | M | M |
| 20 | Evidence by construction plus auto audit package | M | M (parent evidence records) | H | H | M | L | H × H | H (sellable to sponsors on incumbent systems) | M | M |
| 04 | Reusable determinations (ED and fiscal-sponsor review only) | M–H if reuse is high | L (reuse factor unmeasured; L1) | H | M (ER is per grant, REG-002; ED reliance needs counsel) | L | M (stale determination) | M × M | M | M (partner history) | M |
| 09 | Daily netting per recipient | L–M (−39% payments) | M (mechanistic count) | H | H | L | M (blast radius 1.63 grants per incident) | L × M | L | Short | L |
| 37 | Execution-window deferral at year-end | H on specialist FTE (−29% in model) | L (donor acceptance untested) | H | H (grant timing has no donor tax effect) | L | L | M × H | L | M (donor research) | L |
| 21 | Policy compiler with back-testing | H (makes regulatory change cheap) | L (no compiler or back-test built → L1) | M | M | M | M | H × H | H | M (needs partner decision corpus) | M |
| 22/39 | Continuous close / reconciliation by construction | M | L (hours saving = one assumption, E4) | M (needs counterparty keys) | H | M | M (masked feeds → alarms) | M × M | M | M | L |
| 15 | Advisor-embedded "invisible" DAF | H (distribution cost) | L ([I]; downgraded to L1) | M | M (proposed §4966 adviser rule; fee disclosure) | M | M | M × H | H | Long | H if embedded |
| 02 | Cross-sponsor verification network (costly determinations only) | M | M on overlap (E7 public data), L on value | M | L–M (reliance on shared diligence: counsel) | M | M (poisoned record) | H × H | M (thin on routine; viable at ≥$270 per determination [A]) | Long (cold start) | H if it exists |
| 07 | Shared payee registry | M (fraud) | L (parameter-only) | M | M (never hold funds; DD-008 and CTL-004/006 tension) | M | M (registry compromise) | M × H | M | Long | H if two-sided |
| 36 | Shared compliance policy packs | M | L | H | M (each board approves) | M | **H** (one error reaches all adopters) | H × H | M (break-even ~40–60 sponsors [A]) | M | M |
| 19 | Spend-down horizons and charitable defaults | H on philanthropic outcome (EV-015 dormancy) | L | H | H (no payout mandate; respect advisory privileges) | L | L | L × H | L–M | Long (field pilot) | L |
| 32/48 | Board assurance with expiring parameters / governance by exception | M | L | H | H | L | L | M × H | L | Short | L |
| 46 | Publish operating metrics | M (trust; competitive) | M (EV-076 shows nobody does) | H | H | L | L | L × H | M | Short | M (first mover) |
| 43 | Index-only default menu | M (donor cost) | L–M (EV-072 [I]) | H | H | L | L | L × H | M | M | L |

Rejected and excluded: INN-06 (sampling replaces review), INN-35 (pay-first), and the AI auto-clear variant.

## 2. Five rankings

### Ranking 1: highest-impact ideas (magnitude first, evidence second)

1. **INN-05 policy-as-code approval.** Removes per-grant human touch for the routine majority, with canaries required.
2. **INN-21 policy compiler with back-testing.** Turns regulatory change from a manual project into a tested release. Evidence L1.
3. **INN-15 advisor-embedded invisible DAF.** Distribution economics; evidence L1.
4. **INN-37 execution-window deferral.** The largest human-cost lever in the model; acceptance untested.
5. **INN-19 spend-down horizons.** The largest *philanthropic-outcome* lever: 22% of accounts made no grants in 2020–22.
6. **INN-04 reusable determinations.** Size depends on the reuse factor.

### Ranking 2: most feasible near-term improvements (feasibility, cost, time, regulatory)

1. **INN-08 grant ID in remittance.** Low cost, no regulatory obstacle, benefits nonprofits immediately.
2. **INN-01/03/34 diff-driven passport and rescreen.** Low cost, high regulatory feasibility.
3. **INN-26/16 capped delegations.** Already partially tested.
4. **INN-46 publish operating metrics.** Needs telemetry only.
5. **INN-09 daily netting.** Simple, but model the blast radius first.
6. **INN-32 parameter expiry.** Governance only.

### Ranking 3: most radical long-term opportunities (distance from convention, with a credible mechanism)

1. **INN-02 cross-sponsor verification network for costly determinations.** A data-network effect with a real mechanism and a quantified cold-start problem.
2. **INN-44 sponsor-owned record substrate.** Inverts vendor lock-in; L0.
3. **INN-07 / INN-38 two-sided recipient registry and inbox.** Gives nonprofits an interface.
4. **INN-15 invisible DAF.** The sponsor brand recedes into advisor platforms.
5. **INN-47 decision-rights market.** Credentialed specialists claim cases under each sponsor's delegation. L0; E6 weakens it.
6. **INN-17 ACATS-like transfer protocol.** Opposed by incumbent incentives.

### Ranking 4: most commercially valuable infrastructure capabilities (Model C/D relevance, reusability, defensibility)

1. **Policy evaluation and compiler (INN-05/21).** Sellable to sponsors that keep their recordkeeper.
2. **Evidence ledger and audit package (INN-20).** Same buyers; compliance-driven purchase.
3. **Always-migrated record (INN-18).** Lowers switching cost *into* the platform, which incumbents cannot easily match without weakening their own lock-in.
4. **Determination store (INN-04) + verification network (INN-02).** Grows with each client (the E7 mechanism), on costly work only.
5. **Embedded DAF / program-as-code (INN-15/42).** Distribution.
6. **Shared compliance policy packs (INN-36).** Plausible second product; correlated-error risk must be priced.

The audit and economics both point away from per-grant API pricing (09 §3) and away from routine eligibility as a standalone product: it is crowded and nearly free to compute.

### Ranking 5: most important experiments (value of information against cost)

| Rank | Experiment | Resolves | Needs | Why first |
|---|---|---|---|---|
| 1 | **Shadow replay of a design partner's historical grants through the policy engine**, with a timed human review sample | GAP-001, GAP-004; E2's parameter-driven ranking; the INN-05 and INN-21 back-test | One sponsor's grant history and reviewer time | Every cost and control claim depends on it |
| 2 | **Determination reuse factor on partner history** | INN-04 magnitude; the network's value premise (INN-02) | Partner exception history | Converts the largest unmeasured lever into a number |
| 3 | **Costly-work overlap**: Schedule F foreign recipients and fiscal sponsors across sponsors (public data, extending E7) | Whether costly verification recurs (INN-02 audit objection) | Further public-data harvest (feasible now) | Cheap; directly tests the network premise the audit rejected |
| 4 | **Donor acceptance of execution windows** (survey or partner A/B) | INN-37 | Partner donor base | Tests the largest human-cost lever |
| 5 | **Reconciliation break-cost study** | INN-22/39; E4's one assumption (GAP-005) | Partner reconciliation logs | Determines whether continuous close saves labor |
| 6 | **Small-sponsor Schedule I harvest** (non-top-50) | Network value for the long tail | Public data | Tests whether small sponsors gain most per member. **Done (E7c): they do not, per member; aggregate value doubles** |
| 7 | **Red-team the AI flagger** (adaptive adversary, correlated misses, automation bias) | E2 gaps; CTL-046 effectiveness | Synthetic data plus model access | Bounds the flag-only design's real downside |

## 3. Disagreements kept (from the seven-perspective passes and the audit)

- **Economist vs inventor on INN-02.** The mechanism is real, but the value is thin. The inventor holds that the costly-determination niche is enough; the economist wants experiment 3 first. *Unresolved.*
- **Regulatory specialist vs commercial strategist on INN-28/47.** Pooled specialists must act under each sponsor's delegated authority (DD-003). The strategist wants a marketplace. *Resolved toward delegation, pending counsel.*
- **Customer advocate vs economist on INN-37.** Donors may dislike execution windows. *Unresolved; experiment 4.*
- **Adversarial reviewer vs architects on E2.** The AI-native advantage is parameter-driven. *Accepted.* The claim is restated as "superior on one criterion under each sensitivity".
- **Architect vs regulatory specialist on INN-07.** A shared payee registry against DD-008 and CTL-004/006. *Resolved:* the registry supplies verified evidence; each sponsor's own payment gate and cooling-off still operate, and the registry never holds funds.
