# 19 - Echelon Foundry implications

Status: research (2026-11-26). Echelon Foundry owns organisational methodologies and shared engineering standards. Proposals only (XRI-015..018).

## 1. Organisation

- **Echelon Foundry does not need to become a conventional DAF administrator** to enter the market ([14](14-alternative-enterprise-models.md)). The cheapest self-sustaining position is a technology licensor sold through a channel; administration is an option behind an anchor.
- **Fund evidence gates before platform capital** (DEC-008, XRI-017): G0 costs $0.15-0.35M and a partner pilot $1.0-1.5M cumulative; they decide whether the remaining capital (about $6.5M P50 in total, P90 ~$9M) is warranted. Apply the kill rule (no named partner by month 6).
- **Measure accepted-capability productivity** before relying on it (PR #87): this package's economics do not depend on agent-assisted development multiples, but capital does (build $1.1-2.4M).

## 2. Methodology

| ID | Proposal |
|---|---|
| XRI-015 | Adopt **event-level economics** (frequency × touch probability × minutes per touch × rate + failure lifecycle, with prevention and AI as separate levers) as the standard way to cost AI-native enterprise designs. It separates design effects from AI effects and exposed that ~94% of the modelled saving is not AI (CLM-011). The adversarial review also showed why the AI factor must scale AI-native minutes, never derive the no-AI case from them (CHL-100) |
| XRI-016 | Research models in F# with a `check` command that proves byte-identical reproduction, and a `validate` command for registers and links (as implemented here) |
| XRI-018 | Register DEC-001..012 as Praxis `DF-` decision records only after owner acceptance |

## 3. EDF and Clarity

- EDF applied to the observed switch record: the constraint on displacement is distribution and incentive alignment, not capability.
- Clarity: the executive decisions in [23](23-executive-decision-register.md) are mostly **not ready** (no accepted owner, date, review cadence or outcome measure). The research supplies options, evidence and falsifiers.

## 4. Shared engineering

The research reinforces existing Echelon choices (embedded libraries, deterministic pipelines, PostgreSQL) and does not require new infrastructure. It does flag one dependency risk carried from PR #87: production reliance on components under non-commercial licences (OQ-017).
