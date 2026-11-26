# Applying Clarity and EDF in this mission (pinned to the canonical repositories)

**Read on:** 2026-11-14, from the canonical sources, not from summaries in this repository.
- Clarity: `github.com/kemiller2002/clarity-framework` at commit `8cd48019b893a4ce42fe4c9dcc81dd81fb12d1ea`. Files read: `README.md`, `rules.md` (Clarity Constitution), `decision-posture-model.md`, `docs/progressive-commitment.md`, `docs/reconsideration-criteria.md`, `docs/templates/clarity-result-template.md`, `executive-brief.md`.
- EDF: `github.com/kemiller2002/echelon-diagnostic-framework` at commit `41fea6ffc764adc69643d5ee2940916592486f84`. Files read: `README.md`, `docs/edf/specification.md` (v0.3), `docs/framework-engineering/claim-and-confidence-policy.md` (v1.0).

This guide is an application note. It does not modify either framework. Where the earlier repository file `research/decision-intelligence-architecture-2026.md` paraphrases the frameworks, the pinned sources above take precedence.

## The division of labour (from both READMEs)

- **EDF answers "What is happening?"** EDF performs diagnosis.
- **Clarity answers "How much reasoning is currently justified, and what would make that change?"** Clarity does not perform diagnosis. Its three questions are: *What do I know? What is currently justified? What would make me reconsider?*
- Clarity is used before EDF to decide whether rapid EDF-0 is enough or whether EDF-1/EDF-2 depth is justified (Progressive Commitment). Clarity is then used after EDF to evaluate decisions.

## EDF v0.3 required sequence (used for observed industry outcomes)

1. **System Context**: primary system, context, focus.
2. **Outcome**: stated factually, not interpretively.
3. **Manifestations**: observable signals.
4. **Origin network**: technical, human, organizational, environmental, financial and regulatory origins. A single root cause is avoided.
5. **Propagation**: physical, informational, organizational, financial or human paths.
6. **Evidence**: direct observation kept separate from inference.
7. **Control points**: these may differ from origins.
8. **Control point ranking**: by influence, controllability, cost and confidence, with no false precision.
9. **Diagnostic sufficiency**: "Do we understand enough to take the next responsible action?"

Required outputs include confidence, unknowns and the next responsible action.

**Mission rule:** EDF is applied only to an *observed outcome*, for example "paper checks remain a material DAF grant-payment rail in 2026". It is not applied to a hypothesis. Where no outcome is observed, Clarity is used alone.

## Clarity elements used here

- **Constitution commitments:** mechanism first; signals before moves; incentives over intent; bounded truth (no unbounded always/never); mandatory tradeoffs; systems over heroes.
- **Admissibility screen** (from `rules.md`). The following are rejected:
  - prescription without a signal
  - motivation substituted for incentives
  - unbounded claims
  - false precision or tidy-but-unearned models
  - premature synthesis
  - hero narratives
- **Decision posture:** impact × correctability gives Fast, Experimental, Guardrail or Strategic. Required certainty is proportional to the cost of being wrong, the difficulty of correction and the cost of recovery.
- **Progressive commitment and reconsideration criteria:** each conclusion carries explicit "I will reconsider if…" conditions and a monitoring plan.
- **Operational test:** *Can this idea survive incentives, time, and pressure?*

## EDF claim and confidence policy applied to this repository's claims

- Claim states are internal-demonstration, suggestive, unsupported, contradicted, falsified, superseded and planned. "Supported" without a boundary is not used for performance claims.
- Confidence labels are Low, Low-Medium, Medium, Medium-High and High. They are qualitative, not probabilities.
- Exact percentages are published only with the raw inputs, denominator and scoring unit preserved.
- The policy separates **structural conformity, semantic agreement, factual correctness, reproducibility, incremental value and utility**. Evidence for an earlier item does not establish a later one. Two examples in this mission:
  - A vendor that *announces* an AI capability establishes at most structural presence, not utility.
  - A validator re-finding the same number establishes factual correctness, not that the interpretation is right.

## Structural constraint vs historical habit (the mission's incentives test)

A behaviour is classified as a **structural constraint** when an EDF origin network shows that it is held in place by a regulatory, legal-liability or financial origin whose control point the actor cannot change unilaterally. Examples: IRC §4966/4967 sponsor control, and asset-based fee revenue.

It is classified as a **historical habit** when the only sustaining origins are organizational or informational. Examples: legacy process, procurement inertia, and "it has always been checks". In those cases a feasible control point exists within the actor's own authority.

**Mixed** is the default when the two kinds of origin interact, for example liability aversion amplified by an absence of shared eligibility data. Each classification carries a confidence label and reconsideration criteria.
