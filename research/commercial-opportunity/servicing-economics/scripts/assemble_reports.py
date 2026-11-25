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
2. **Re-costed through the F# model** (Model B, AI-native base; marginal contribution = fees less vendor cost, servicing hours at $65.45/h, $12k sponsor cost and onboarding over five years):
   - **292 of 1,430 sponsors cover their own incremental cost at 20 bps.** The count is 171 if handling minutes are at the high case, and 227 if only AI-enhanced (not redesigned) handling is achieved.
   - **20 sponsors could alone cover the lean organization's fixed cost** of $1.74M (Model B including the minimum second ops person); 17 at high minutes.
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
