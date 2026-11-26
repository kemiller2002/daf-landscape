# 15: Failure and resilience analysis

**Pass:** LYR (part 4), with ADV2-027. Integrated in model section 10 and [`failure-costs.csv`](model/out/failure-costs.csv). **Data:** [`failure-catalogue.csv`](../../../data/commercial-opportunity/ai-native-capital-minimization/failure-catalogue.csv) (23 failures: consequence, detection, leading indicator, contingency, recovery cost, stop option).

**Integrator conclusions**
- Model section 10 applies eleven failure modifiers to each sequence, including two **correlated** failures. Figures are extra debt-financed capital for sequences B-G; F is founder-led.
- **Single-failure ranges:**
  - Build at 1x instead of 1.5x: +$0.85-0.95M.
  - Development twice as long: +$4.3-6.6M, with most sequences not profitable within 60 months. Go-lives slip 12 months while burn and the build continue.
  - Sales cycles twice as long: +$1.1-3.2M.
  - Handling stays AI-enhanced (101 minutes): +$0.8-1.6M; no sequence is profitable within 60 months.
  - First customer or design partner withdraws: +$0.6-3.8M; founder-led F, with one anchor, is hit hardest.
  - Assurance +$150k a year: +$0.6-0.7M.
  - Security incident $500k: +$0.6M.
  - Echelon licence at the LYR cost-plus price ($351k a year instead of $60k): +$1.8-1.9M.
  - Customer customisation: +$0.6-1.0M.
- **Correlated failures:**
  - Build at 1x + sales 2x: +$2.1-4.1M.
  - Plus review not reduced: +$2.6-4.2M.
  - Only founder-led F still becomes profitable within 60 months, and only in the first case.
- **Staged gates are the main defence**, and every catalogued failure except a security incident or a market fall has a detection point before build spend:
  - Stop after gate 1 at about **$0.15M**: buyer price test, Echelon licence terms, payments counsel, auditor conversation.
  - Stop after gate 2 at about **$0.75M**: design partner, instrumented shadow replay, engineering spike measured with the report 05 protocol.
  - A failed go-live sinks $2-3M or more.
- **Resilience at $1.5B** (model section 5):
  - A 30% market fall moves F5 break-even to $2.11B.
  - The severe combined stress has no break-even.
  - Margin at reference scale is thin, so a staffed servicer needs to be well above break-even before it carries a downturn.

> The research-pass content below was produced by a role-separated agent pass from the same model family as the integrator; it is not independent validation. Labels: [S] sourced, [A] assumption, [D] derived, [E] estimate, [M] measured (the pass ran it). Figures quoted inside pass sections are the pass's own; where the integrated model differs, the preface says so and the model ([`model/out/results.md`](model/out/results.md)) governs.

## Part 4: failure catalogue (cost of being wrong) and staged investment

`failure-catalogue.csv`: **23 failure modes**, each with annual and capital consequence (arithmetic against the previous F# model re-run at R or its published capital plans), detection mechanism, leading indicator, contingency, recovery cost and stop option.

| Failure | Annual effect at R | Capital effect |
|---|---|---|
| Productivity gain <1.2x instead of 1.5-2x | +332,000 to +941,000 (B03 1 -> 3-5 engineers) | +1,260,000 (build x2.5) to +4,950,000 (Unbound-scale build) |
| Excessive exceptions: volume of human-handled items x1.5 | +271,250 | +0.1-0.3M (later profitability) |
| Human review cannot be reduced: auditors/boards do not accept the design; operation stays AI-enhanced | +943,516 (AI-enhanced) to +2,700,995 (conventional) | +120,000 (anchor plan) to +2,270,000 (multiple smaller sponsors) |
| Delegation unavailable for 24 months instead of 12 | +943,516 per year of delay at R (upper bound: AI-enhanced handling) | +0.1-0.9M |
| Extensive per-sponsor customisation | +165,000 to +354,000 at 5 sponsors | +1,100,000 one-off at 5 sponsors |
| Echelon not commercially ready (0.x churn, single maintainer, immature security components) | +0 to +105,000 (verified reuse share lost) + second-maintainer cost already included | +50,000-200,000 one-off replacement; +0.8-0.9M if go-live slips 6 months |
| Licence terms unfavourable or absent | each +100,000/yr fee -> +~$65M break-even AUA | launch blocked until resolved (CNV-GOV-009) |
| Design partner withdraws | -24% to -45% of revenue at R if the partner is 60% of AUA (model: lose largest sponsor at R -> profit -37,000) | +1,800,000 (plan D instead of anchor) and profitability month 30 vs 18 |
| Development takes 2x longer (24 months) | 0 at steady state | +2,300,000 to +2,500,000 |
| Acquisition takes 2x longer (first signing month 24) | 0 at steady state | +1,600,000 to +1,800,000 |
| Assurance costs higher (SOC 1 $120k + SOC 2 $70k, qualified opinion) | +115,000 (+~$75M break-even AUA) | +20,000-40,000 readiness |
| Major security incident (fraud redirection or data breach) | +500,000 to +1,000,000 in the year; plus possible sponsor loss | reserve |
| Measured minutes 2x model | +814,263 | +0.5-1.5M |
| Counsel concludes money transmission applies | unknown; licensing, bonding and compliance staff (not quantified) | unknown |
| Key-person loss (principal unavailable) | +188,958 to +222,482 replacement plus ramp-up | +0.3-0.9M delay |
| Transfer price challenged (tax) or sponsor objects to related-party pricing | unknown | unknown |
| Price falls to 15 bps | -750,000 revenue at R | n/a |
| Market -30% | -900,000 revenue; profit -817,000 | n/a |
| No external licensees for Unbound or Echelon | Group cost $4.99M vs revenue $3.0M at R; -1.99M | n/a |
| 10 sponsors instead of 5 at the same AUA | +162,619 | +0.5-1.0M |
| Duplicated corporate floors larger than planned | +60,000 to +250,000 (three-entity option) | +40,000-200,000 |
| Wages +15% | +305,608 | n/a |
| Vendor prices +50% | +409,773 | n/a |

**Staged investment (option to stop cheaply)** [E]:

| Gate | Months | Work | Cumulative spend at stop | Stops these failures before build |
|---|---|---|---|---|
| G0 | 0-3 | Owner-led buyer price tests (bps vs $/fund), Echelon licence terms decision, payments/money-transmission counsel opinion ($15-100k, CST-C08), auditor planned-approach conversation | ~$0.06-0.15M | licensing, money transmission, buyers reject tariff, auditors reject deterministic release |
| G1 | 3-9 | Design-partner contract with price collar and stop-loss; 12-month shadow replay + instrumented time study; 3-month engineering spike on ledger and payment gate with agent-throughput telemetry | ~$0.4-0.75M | AI productivity, excessive exceptions, minutes 2x, customisation, partner withdrawal, acquisition delay |
| G2 | 9-18 | Narrow release-1 build ($0.7-1.8M), SOC readiness, second maintainer | ~$2-3M | development 2x, assurance cost |
| G3 | 18+ | Go-live with delegation package | as previous study ($2.7-3.6M trough minimum) | security incident, market fall (insure/reserve; not stoppable) |

Basis: G1 = 6 months of founder-led cash personnel (Model A cash $427k/yr) + 3 months of contract engineering at $60k + counsel and replay compute; G2 = previous study build variants. **The previous plan hires the full development organisation at month 0 (~$1.05M cumulative at month 6); staging defers that until G1 evidence exists.**

## Challenge to both the previous conclusions and the new premise

- **Against the previous study:** its fully loaded case ($1.8-2.3B) still treats the platform as $1.0M/yr of build and two engineers, carries no Echelon cost, and no onboarding amortisation or servicing-specific platform work. Charging those at cost moves break-even to $2.3-2.8B base. Its AI-native minutes (~50/account-year) remain unmeasured and are the single largest operating lever (minutes x2 = +$0.81M/yr at R).
- **Against the new premise ('an entirely different company'):** the outcome-designed view removes recurring human work mainly in the servicing layer, where the previous study had already assumed most of it away. The new costs it introduces (platform ownership, foundry reliance, second maintainer, assurance of agent-authored code) are fixed and front-loaded. Lower variable cost is not permission to be optimistic: at R the group loses ~$2.0M/yr base.
- **What would make it different:** (1) measured >=2x agent throughput with escaped defects at or below baseline over six months (moves B toward ~$1.0M); (2) external licensing of Unbound to ~20k+ funds; (3) auditors and boards accepting deterministic release and generated evidence from go-live. Each is testable at G0/G1 for well under $1M.
- **Transfers are not eliminations:** complex-gift fees to funds, payment rails to sponsors, deciders to sponsor boards and recertification to advisors are all shown as transfers in the registers.

## Limitations

- Same model family produced the previous study, Unbound's economics and this analysis; nothing here is independent validation.
- No buyer conversation, signed contract, time study, auditor letter, counsel opinion or Echelon licence terms exist. Every handling minute is an assumption inherited from the previous study.
- Layer line values marked [A] (Echelon reliance costs, engineering headcount, allocation keys, usage share, markup, servicing platform features, entity admin increments) are analyst placeholders; ranges are wide on purpose.
- Measured repository facts (commit counts, authorship trailers, line counts, licences) describe activity, not productivity or quality. Line counts include tests and generated files. Commit authorship trailers may under- or over-state AI contribution.
- The F# model was re-run with an extra fixed-cost line to compute break-even; layer extras were treated as fixed, though onboarding amortisation scales with sponsors.
- Transfer pricing, entity, licensing (PolyForm NC charitable carve-out) and money-transmission points are research readings of public text, not legal or tax advice.
- AI-native results are steady-state; pre-delegation periods (Unbound EV-08) are only in the failure catalogue.

## Largest evidence gaps

1. Agent-assisted development throughput and escaped-defect rate on a regulated codebase (decides B: $1.0M vs $2.3M+ per year).
2. Echelon commercial licence terms, escrow/fork right and second-maintainer plan (decides T01 and CNV-GOV-009).
3. External auditor acceptance of deterministic release and generated evidence from go-live (CNV-GOV-001, CNV-GOV-003).
4. Sponsor board willingness and time to delegate (CNV-GRT-001) and to appoint multi-sponsor deciders (RC-AN-001).
5. Measured handling minutes, exception incidence and December arrivals (CNV-EVB-001).
6. Whether any sponsor or administrator would license Unbound externally at ~$90/fund.
7. Counsel opinion on money transmission and on PolyForm NC for nonprofit vs commercial servicers; tax view on related-party pricing.
