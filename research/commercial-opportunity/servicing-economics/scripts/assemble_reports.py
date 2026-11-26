#!/usr/bin/env python3
"""Assemble the pass-based servicing-economics reports (01-04, 08 appendix, 09) from the research passes.

Each report = integrator preface (conclusions, corrections, how the pass feeds the F# model) + the pass's own
sections, with their headings demoted one level. Inputs are the committed pass reports in
data/commercial-opportunity/servicing-economics/pass-reports/. Deterministic; pure functions except main().

    python3 -I -B research/commercial-opportunity/servicing-economics/scripts/assemble_reports.py .
"""
import json
import sys
from pathlib import Path

PASSES = Path("data/commercial-opportunity/servicing-economics/pass-reports")
OUT = Path("research/commercial-opportunity/servicing-economics")

NOTE = ("> Research-pass content below was produced by a role-separated agent pass from the same model family as the "
        "integrator. It is not independent validation. Labels: [S] sourced, [A] assumption, [D] derived, [E] estimate.")


def load(root, name):
    path = root / PASSES / f"{name}-report.jsonl"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def demote(markdown):
    return "\n".join(("#" + line) if line.startswith("#") else line for line in markdown.splitlines())


def sections(rows, keep=None):
    chosen = [r for r in rows if keep is None or keep(r["section"])]
    return "\n\n".join(f"## {r['section']}\n\n{demote(r['markdown'])}" for r in chosen)


def doc(title, preface, body):
    return f"# {title}\n\n{preface.strip()}\n\n{NOTE}\n\n{body}\n"


PREFACES = {
    "08-adversarial-review.md": ("08: Adversarial review", """
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

The model was corrected and every material analysis re-run after this review (`model/out/results.md` sha256 `b8328e3b…`, 28/28 tests passed). The numbers quoted in the ADV sections below are the **pre-fix** values the reviewer computed, using a Python port of the F# core.

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
"""),
    "01-pricing-and-scope.md": ("01: Pricing and scope", """
**Date:** 2026-11-25. **Pass:** PRC. **Data:** [`price-observations.csv`](../../../data/commercial-opportunity/servicing-economics/price-observations.csv) (59 observations); evidence EV-PRC-001..031 in the [evidence register](../../../data/commercial-opportunity/servicing-economics/evidence-register.csv).

## Integrator conclusions

1. **Comparable price band.** Fully staffed DAF administration earns about **15-40 bps of average assets, or $390-815 per account-year**. The per-account figure is more stable than the bps figure. The anchor comparable is Ren at Morgan Stanley GIFT:
   - $14.93M paid for "admin & legal" in 2024, on about $9.1B of DAF assets and 21,800 accounts;
   - that is **18.5 bps of average assets, or $737 per account-year** [D, grade A], and the rate held at 18.4-18.8 bps in 2022-2024.

   Software-only licensing sits at 0.5-9 bps ($34-611 per account), and small clients pay an apparent fixed floor of about $120-175k a year.
2. **Is 20 bps credible?** It is a market price, not a discount, for programs averaging about **$250k or more per account**. For about $100k-average books it is roughly half the incumbent rate, and it is **below this model's cost** unless paired with a per-account floor. Report 05 shows the cost side.
3. **Never compare donor fees with servicer revenue.** MS GIFT donors pay a tiered administrator fee (greater of $100 or 27 bps, stepping down to 9 bps), plus 7 bps to Morgan Stanley and up to 3 bps for the sponsor. Ren's realised 18.5 bps is below the first tier, so the donor schedule cannot be read as Ren's price.
4. **Correction to earlier repository work.** Unbound report 13 quoted "33-37 bps" for outsourced administration. That figure used year-end assets for two Ren clients and omitted MS GIFT. On average assets the same two clients come to 38-40 bps, and MS GIFT is 18.5 bps. The prior 20 bps memo is corrected accordingly: TIFIN Give's current ADV (dated 2026-09-04) lists 30 bps to $1M and 10-20 bps above as a sponsor-billed service fee, and GiveClear's 2024 990 shows $185,921 paid to Tifin Give LLC. The earlier note said no TIFIN payment had been found.
5. **What the model uses.** Price points of 5-35 bps on average billable assets, an optional per-account floor (`PerAccountMinimum`), an optional sponsor minimum (`MinimumAnnualFee`), and payments optionally passed through at cost.
"""),
    "02-sponsor-market-analysis.md": ("02: Sponsor market analysis", """
**Date:** 2026-11-25. **Pass:** SPN, with an integrator re-costing through the F# model.

**Data:**
- [`sponsor-economics.csv`](../../../data/commercial-opportunity/servicing-economics/sponsor-economics.csv): 1,597 EINs.
- [`customer-attractiveness.csv`](../../../data/commercial-opportunity/servicing-economics/customer-attractiveness.csv): 1,448 addressable sponsors.
- [`top25-hypotheses.csv`](../../../data/commercial-opportunity/servicing-economics/top25-hypotheses.csv), [`self-sustaining-candidates.csv`](../../../data/commercial-opportunity/servicing-economics/self-sustaining-candidates.csv), [`unattractive-large.csv`](../../../data/commercial-opportunity/servicing-economics/unattractive-large.csv) and [`segment-summary.csv`](../../../data/commercial-opportunity/servicing-economics/segment-summary.csv).
- [`sponsor-model-economics.csv`](../../../data/commercial-opportunity/servicing-economics/sponsor-model-economics.csv): every sponsor re-costed by the F# model.

**Regenerate:** `python3 -I -B research/commercial-opportunity/servicing-economics/scripts/sponsors/build_sponsor_economics.py`. The pass ran it three times with byte-identical output.

## Integrator conclusions

1. **Most DAF assets cannot be bought.**
   - In-house captives (Fidelity, Schwab, Vanguard) hold 43.1% of active DAF assets, and everything non-addressable holds 45.3%.
   - Wealth-firm affiliates mostly already outsource to Ren.
   - The addressable universe is **1,430 active, non-captive sponsors with about $151B of average assets** (proxy).
2. **Re-costed through the F# model** (Model B, AI-native base; marginal contribution = fees less vendor cost with payments passed through, servicing hours at $65.45/h over 90% utilisation, a per-sponsor step share, $12k sponsor cost and onboarding over five years; revised after the adversarial review):
   - **224 of 1,430 sponsors cover their own incremental cost at 20 bps.** The count is 141 if handling minutes are at the high case, 182 if only AI-enhanced handling is achieved, and 171 if buyers cap the price at Ren's $737 per account on average.
   - **By size:** no sponsor below $50M is positive (1,179 sponsors, $9B of assets); $50-100M is marginal (median +$17k); every sponsor at $100M or more is positive (156 sponsors, $135B).
   - **19 sponsors could alone cover the lean organization's fixed cost** of $1.74M (Model B including the minimum second ops person). That falls to 10 once build amortisation and sales are carried, and to 5 under the $737 per-account cap.
3. **The largest names are mostly not realistic customers.**
   - National Philanthropic Trust ($49B) is itself a competitor, selling private-label and outsourced services.
   - American Endowment Foundation migrated recently.
   - Silicon Valley Community Foundation and the Chicago Community Trust are complex community foundations with non-DAF funds.
   - Top-25 rankings are therefore **hypotheses to test, not sales leads**. The SPN ranking adds risk and switching dimensions on top of contribution.
4. **Community foundations look attractive on balance but carry hidden work.** Among the larger foundations, DAF accounts often average $0.5-2.5M (Silicon Valley Community Foundation about $8.4M), so asset fees are large per account. But they need non-DAF fund support, which the model represents only as a 1.25x handling multiplier [A], and they already run integrated CF software. Unbound's own review (report 05, EV-04) rejected CFs as the entry segment. This report keeps them in the hypothesis list but flags the integration requirement as decisive.
5. **Small-balance programs lose money at any flat bps.** Sponsors averaging under $10k per account hold 61% of reported accounts but 0.1% of assets. A per-account floor or an activity fee is required to serve them (report 05).
6. **Correction.** SPN's own cost-to-serve parameters were placeholders sized to the $75 hypothesis. The integrator re-costing above supersedes them for every economic conclusion. SPN's attractiveness scores remain as a relative ranking only.
"""),
    "03-organization-and-budget.md": ("03: Organization and budget", """
**Date:** 2026-11-25. **Passes:** CST (costs and staffing) and ECH (Echelon Foundry).

**Data:**
- [`cost-register.csv`](../../../data/commercial-opportunity/servicing-economics/cost-register.csv): 109 lines.
- [`role-compensation.csv`](../../../data/commercial-opportunity/servicing-economics/role-compensation.csv) and [`staffing-models.csv`](../../../data/commercial-opportunity/servicing-economics/staffing-models.csv).
- [`echelon-capabilities.csv`](../../../data/commercial-opportunity/servicing-economics/echelon-capabilities.csv): 22 capabilities.

## Integrator conclusions

1. **The $1,177,750 / 5-FTE budget is a low case, not a base.** Re-priced from BLS OEWS May 2025 wages (read via O*NET, grade B), BLS ECEC burden and public vendor prices, the same five roles cost **$1.66M a year (range $1.09-2.77M)**. The prior budget missed or understated:
   - market salaries for the CTO, engineer and controller;
   - security and assurance: SOC 1 and SOC 2 Type 2, penetration testing and a vCISO total about $166k, against $65k budgeted;
   - insurance: about $84k against $30k;
   - and it cannot sustain dual control.
2. **Three structures, as encoded in the model:**

   | Model | Core FTE | Fixed (economic) | Fixed (cash) | Live-operation minimum |
   |---|---:|---:|---:|---|
   | A founder-led | 3 | $1.31M | $1.12M | +2 ops staff for separation of duties (so about 5 people once live) |
   | B lean independent | 5 | $1.66M | $1.66M | +1 ops staff (second preparer/releaser) |
   | C established | 12 | $2.84M | $2.84M | none |

   Model A is a pre-launch structure. Once live it converges on Model B's headcount but keeps the founders' below-market cash pay. That is a cash, not an economic, saving of about $0.2M a year.
3. **Founder labour is not free.** Every model is shown at economic cost, with founders at market pay. Cash cost is shown separately, and the capital plans in report 06 use cash with an economic-cost variant.
4. **Echelon Foundry saves little on verified evidence.**
   - No DAF application or production infrastructure exists. Unbound is requirements only.
   - Verified reuse (framework code, design assets, the public-data replay tool, a single-VM PostgreSQL benchmark) cuts **$0-105k a year**, and it is shared cost, not eliminated cost.
   - Most of the stack is licensed PolyForm Noncommercial, so a commercial licence is a launch gate and a cost to the DAF business.
   - Engineering cost could be 33-50% lower only if agent-assisted throughput is measured at 1.5-2x and sustained for six months or more. Nothing measures that yet.
   - The prior budget also omitted the platform build itself: Unbound's own model assumes **$5M ($3-15M)**.
5. **Platform vs staffed business.** The CST cost-separation rules below are applied in the model: platform lines are in fixed cost; staffed-operations lines are in capacity and step costs; sponsor-retained decision costs ($42-43 per account) are excluded because the sponsor bears them; pass-throughs are optional.
"""),
    "04-activity-cost-and-capacity.md": ("04: Activity cost and capacity", """
**Date:** 2026-11-25. **Pass:** ACT.

**Data:**
- [`activities.csv`](../../../data/commercial-opportunity/servicing-economics/activities.csv): 33 activities.
- [`approaches.csv`](../../../data/commercial-opportunity/servicing-economics/approaches.csv), [`capacity-model.csv`](../../../data/commercial-opportunity/servicing-economics/capacity-model.csv), [`staffing-steps.csv`](../../../data/commercial-opportunity/servicing-economics/staffing-steps.csv), [`verification-180.csv`](../../../data/commercial-opportunity/servicing-economics/verification-180.csv) and [`workload-tails.csv`](../../../data/commercial-opportunity/servicing-economics/workload-tails.csv).

**Regenerate:** `python3 -I -B research/commercial-opportunity/servicing-economics/scripts/activities/act_model.py .`

## Integrator conclusions

1. **No time study exists, so every handling minute is an assumption.** The activity model, Unbound's work inventory and daf-landscape's earlier process model share assumptions, so their agreement is not independent validation.
2. **Minutes per account-year (market mix):**

   | Approach | Minutes |
   |---|---:|
   | Conventional | 260 (109-692) |
   | Conventional + AI | 124 |
   | AI-native redesign | 51 (18-169) |
   | Redesign + elimination | 34 |

   Redesign and elimination create the advantage, and AI alone roughly halves conventional handling. The main levers are:
   - board-delegated approval;
   - reuse of eligibility determinations;
   - structured intake;
   - grants paid by EFT by default;
   - continuous charity monitoring.
3. **The $40 / 48-minute allowance holds only for a redesigned operation on typical, small and inactive accounts.** At the evidence-based loaded rate of **$65.45/h** (CST), $40 buys about 37 minutes, not 48. The $75 decomposition is mis-split:

   | Line | Budget | Activity model (AI-native) |
   |---|---:|---:|
   | Payments | $10 | $26 |
   | Data and identity | $10 | $2 |
   | Total | $75 | about $89 (about $65 with elimination) |

   Conventional handling costs about $217-262 per account, which is consistent with Ren's $390-815 per account price.
4. **Capacity.**
   - Each sponsor adds about 324 hours a year of sponsor-level work under AI-native handling.
   - December daily load runs about 3.1-3.3x average.
   - The core team's single operations person and single controller cannot carry December or absences.

   The F# model applies archetype December shares and buys excess December hours at the loaded rate.
5. **180-day charity re-verification.** Continuous monitoring, determination reuse and exception-only human review cost about **$1 per account-year**, against about $69 for scheduled human review. Approval-time and release-time checks remain unchanged. Recommended as requirement transfer RC-ACT-001 in report 09.
6. **How the model uses this.** Archetype minutes, external cost, payment cost and December shares feed `Parameters.fs` (`archetypeTable`, base values). The low and high cases enter as a minutes factor (0.35x / 3.33x).
"""),
    "09-requirements-transfer-candidates.md": ("09: Requirements transfer candidates for Unbound", """
**Date:** 2026-11-25. **Status:** proposals only. Unbound is read-only during this mission (`main` @ `9b38de4`). Each candidate goes through Unbound's own governance: convergence clauses, owner ratification and the open-questions register. None removes a legally required check.

**Sources:**
- ACT candidates RC-ACT-001..009: [`requirements-candidates-act.jsonl`](../../../data/commercial-opportunity/servicing-economics/requirements-candidates-act.jsonl).
- Integrator candidates RC-SE-001..008: listed below.

## Integrator candidates

| ID | Unbound target | Issue found in this mission | Proposed change | Safety constraint |
|---|---|---|---|---|
| RC-SE-001 | UNB-SMP-ECN-004 (licence pricing) and its CNV successor | The licence and fee model has no per-account floor, so small-balance accounts lose money at any flat bps (report 05). | Add a fee component type "per-account minimum" (greater of asset fee or a floor), shown separately on invoices; floors disclosed to donors where they pass through. | Floors must never apply to accounts in wind-down after a final grant, and must not discourage grants (report 08). |
| RC-SE-002 | Fee-basis definitions (CNV-FIN-002) | Asset-based fees on balances that include approved-but-unpaid grants reward slow payment. | Exclude reserved and approved-unpaid grant amounts from billable average assets. | None weakened; strengthens charitable outcome. |
| RC-SE-003 | Payments design (CNV-PAY-*) | Payment rails are about $26 per account-year and mostly sponsor-originated. | Allow payment-rail costs to be passed through at cost, itemized. | Pass-through must be at cost with no markup, and must be disclosed. |
| RC-SE-004 | CNV-GRT-001 delegation | Without board delegation, every grant is an individual sponsor decision. The redesign levers are unavailable until delegation is in place. | Same as RC-ACT-007; make time-to-delegation an onboarding exit criterion. | Delegation by board resolution only. |
| RC-SE-005 | SPD-ADV-001 / CNV-GOV-004 | Per-sponsor exclusivity applied to surge staff turns December capacity into a per-sponsor fixed cost. | Same as RC-ACT-002: exclusivity for A3+ deciders only; pooled preparation staff allowed. | Deciders remain exclusive to one sponsor. |
| RC-SE-006 | Evidence-phase protocol (report 12) | The economics rest on unmeasured minutes. | Make the 90-day event-log study (3-5 sponsors: exception rates, minutes, contacts, December shares) a precondition for any price commitment. | n/a |
| RC-SE-007 | Complex-asset policy (OD-M-09) | Complex-asset donors cost about $700 per account-year even with redesign. | Price complex gifts as a separately billed exceptional service at cost-based rates rather than inside the asset fee, so the incentive to refuse them is removed. | Acceptance decisions stay with the sponsor; the fee must not deter acceptable gifts. |
| RC-SE-008 | Licensing gate (ECH) | PolyForm Noncommercial terms on the Echelon stack. | Record commercial-licence terms as an activation gate for any servicer use. | n/a |
"""),
}

BODIES = {
    "08-adversarial-review.md": (["adv", "ech"], lambda name: name.startswith(("ADV-", "CL-", "EDF", "Framework"))),
    "01-pricing-and-scope.md": ("prc", None),
    "02-sponsor-market-analysis.md": ("spn", None),
    "03-organization-and-budget.md": (["cst", "ech"], lambda name: not name.startswith(("CL-", "EDF", "Framework"))),
    "04-activity-cost-and-capacity.md": ("act", lambda name: not name.startswith("ACT-12")),
    "09-requirements-transfer-candidates.md": ("act", lambda name: name.startswith("ACT-12")),
}


def body(root, spec):
    names, keep = spec
    names = names if isinstance(names, list) else [names]
    return "\n\n".join(sections(load(root, n), keep) for n in names)


def main(argv):
    root = Path(argv[1]) if len(argv) > 1 else Path(".")
    for filename, (title, preface) in PREFACES.items():
        (root / OUT / filename).write_text(doc(title, preface, body(root, BODIES[filename])), encoding="utf-8")
        print("wrote", filename)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
