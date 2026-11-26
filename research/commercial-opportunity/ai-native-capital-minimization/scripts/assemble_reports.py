#!/usr/bin/env python3
"""Assemble the pass-based capital-minimization reports from the research passes.

Each report = integrator preface (conclusions, corrections, how the pass feeds the F# model) + the pass's own
sections, with headings demoted one level. Inputs are the committed pass reports in
data/commercial-opportunity/ai-native-capital-minimization/pass-reports/. Integrator-only reports (00, 07, 11, 14, 18,
README) are written directly and are not touched. Deterministic; pure functions except main().

    python3 -I -B research/commercial-opportunity/ai-native-capital-minimization/scripts/assemble_reports.py .
"""
import csv
import json
import sys
from pathlib import Path

DATA = Path("data/commercial-opportunity/ai-native-capital-minimization")
PASSES = DATA / "pass-reports"
OUT = Path("research/commercial-opportunity/ai-native-capital-minimization")
D = "../../../data/commercial-opportunity/ai-native-capital-minimization"

NOTE = ("> The research-pass content below was produced by a role-separated agent pass from the same model family as the "
        "integrator; it is not independent validation. Labels: [S] sourced, [A] assumption, [D] derived, [E] estimate, "
        "[M] measured (the pass ran it). Figures quoted inside pass sections are the pass's own; where the integrated "
        "model differs, the preface says so and the model ([`model/out/results.md`](model/out/results.md)) governs.")


def load(root, name):
    path = root / PASSES / f"{name}-report.jsonl"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def demote(markdown):
    return "\n".join(("#" + line) if line.startswith("#") else line for line in markdown.splitlines())


def sections(rows, keep):
    return "\n\n".join(f"## {r['section']}\n\n{demote(r['markdown'])}" for r in rows if keep(r["section"]))


def starts(*prefixes):
    return lambda name: any(name.startswith(p) for p in prefixes)


def doc(title, preface, body):
    return f"# {title}\n\n{preface.strip()}\n\n{NOTE}\n\n{body}\n"


def candidates_table(root):
    rows = list(csv.DictReader((root / DATA / "requirements-candidates.csv").open(encoding="utf-8")))
    cells = lambda r: [r["candidate_id"], r["unbound_ids"], r["problem_category"], r["proposed_replacement"],
                       r["financial_control_implication"], r["acceptance_criteria"], r["legal_obligation_preserved"]]
    clean = lambda v: " ".join(str(v).split()).replace("|", "\\|")
    head = "| ID | Unbound IDs | Category | Proposed replacement | Financial-control implication | Acceptance criteria | Legal obligation preserved |\n|---|---|---|---|---|---|---|"
    return head + "\n" + "\n".join("| " + " | ".join(clean(c) for c in cells(r)) + " |" for r in rows)


PREFACES = {
    "01-conventional-assumption-register.md": ("01: Conventional assumption register", f"""
**Pass:** LYR (part 2), with OPS (overhead) and ADV2 challenges. **Data:** [`assumption-register.csv`]({D}/assumption-register.csv), 52 assumptions: previous study 28, Unbound 18, both 6.

**Integrator conclusions**
- Of 52 conventional assumptions, the pass judged 17 to have a better replacement, 32 unproven and 2 worse. The better replacements are mostly small: December deferral by sponsor policy, EFT by default, lazy charity re-verification, generated evidence.
- **The binding assumptions are not organisational habits.** They are legal and assurance obligations (sponsor reserved authority, OFAC, IRC 4966/4967, SOC 1 and SOC 2 reliance, CNV-GOV-003 three-person release before gate acceptance), the platform engineering floor, and buyer price.
- Three previous-study assumptions are **corrected** in this mission:
  - the $60k/month × 12 build (report 04);
  - ratio-based hiring triggers, which ignored December release capacity (report 06);
  - the 33.8-minute "elimination" scenario, which counted transferred work as eliminated (report 02).
- One previous-study assumption is **strengthened**: productive hours of 1,520 already deduct coordination. The integrated model counts coordination only beyond six pairs (ADV2-013).
"""),
    "02-outcome-driven-enterprise-design.md": ("02: Outcome-driven enterprise design", f"""
**Pass:** OPS (parts 1-2). **Data:**
- [`outcomes.csv`]({D}/outcomes.csv) (27 outcomes);
- [`responsibility-matrix.csv`]({D}/responsibility-matrix.csv) (83 elements, 39 needing a person);
- [`work-elimination.csv`]({D}/work-elimination.csv) (33 activities).

**Integrator conclusions**
- Designing from outcomes and applying prevent → eliminate → consolidate → simplify → automate → AI → human removes about **40%** of the previous AI-native servicer minutes: 50.7 → about 30.1 per account-year at market mix.
  - About 31 points of that is eliminated work.
  - About 10 points is **transferred** to donors, charities, intermediaries, sponsors or auditors (5.0 minutes per account and about 600 minutes per sponsor-year). Transferred work is not counted as eliminated.
- **Correction to the previous study:** its "AI-native + elimination" scenario (33.8 minutes) included transfers.
- The integrated model carries the outcome-designed variant (30.1 minutes; 12,720 sponsor-level minutes, from 19,440) **only as an unproven hypothesis**. Every minute rests on assumed exception rates; no time study exists.
- Responsibility assignments keep every legally or contractually human element human: sponsor reserved authority (SPD-ADV-001), OFAC dispositions, 4966 expenditure responsibility, release and independent review. AI is capped at recommend and prepare (report 08).
"""),
    "03-three-layer-economic-model.md": ("03: Three-layer economic model", f"""
**Pass:** LYR (part 1), integrated in model section 7. **Data:**
- [`layer-costs.csv`]({D}/layer-costs.csv) (43 lines);
- [`entity-options.csv`]({D}/entity-options.csv);
- [`layer-summary.json`]({D}/layer-summary.json).

**Integrator conclusions.** Model section 7, at $1B in 5 sponsors and 50 minutes, MSP platform base:

| Question | Answer |
|---|---|
| Incremental annual cost of servicing if Unbound exists | about **$2.0M** (F5, $1B; the pass gives $2.29M, $1.22-5.18M, at $1.5B / 10,000 accounts) |
| Incremental annual cost of Unbound if Echelon exists | about **$0.7M** with the minimum product at 1.5x; **$1.8M** on the LYR full-scope base (the pass gives $2.26M, $1.03-5.80M) |
| Servicing standalone vs incremental | standalone carries about $0.9-1.0M a year more (build amortisation, Echelon share and licence, maintenance gap) |
| Consolidated A+B+C at $1B | a loss of about $1.0M (MSP base) to $2.1M (full-scope base): the platform has one customer |

- **Shared Echelon resources are not free.** Production reliance creates about $0.27M a year of Echelon cost (second maintainer, component security review, licence programme, licensor insurance) against about $0.13M a year of verified reuse saving.
  - The integrated base charges 45% of a $300k Echelon capability plus a $60k licence.
  - The LYR base charges $0.27M plus 90%.
- **Entity structure** (research level, not legal or tax advice):
  - Run as one entity with priced internal charges now.
  - Move servicing to a subsidiary at the first live-money signing (liability ring-fence, SOC 1 boundary).
  - Separate Echelon only when it has a second commercial user.
  - Transfer prices move profit between layers and cancel on consolidation.
- **Two bases, not optimistic and conservative (ADV2-002).** "MSP base" covers the minimum servicing product with 1-2 maintaining engineers. "Full-scope base (LYR)" covers Unbound's full scope with a technical lead and three engineers. The truth for a first release lies between them and depends on scope discipline.
"""),
    "04-development-cost-reconstruction.md": ("04: Development cost reconstruction", f"""
**Pass:** DEV (sections on the $5M origin, the $60k origin, scenarios and deferrable capabilities). **Data:**
- [`dev-scenarios.csv`]({D}/dev-scenarios.csv) (6 budgets × 6 multiples);
- [`deferrable-capabilities.csv`]({D}/deferrable-capabilities.csv) (24);
- model section 8 and [`development-scenarios-model.csv`](model/out/development-scenarios-model.csv).

**Integrator conclusions**
- **Unbound's $5M build has no derivation.**
  - It is labelled `assumption` in `parameters.json:509-516`.
  - Its cited source is a peak-capital output with no build line, and it entered through one agent commit (`5aae42a`).
  - The convergence vendor P&L and the previous study inherited it.
- **The previous study's $60k/month × 12 ($0.72M) was an integrator assumption**, deliberately narrow. It is **below** any safe minimum product found here. That is a correction to the previous study's minimum capital ($2.7-3.6M), which is understated (report 11).
- **A minimum servicing product (MSP) safe with live money costs about $1.1-2.4M** [E]:
  - $2.43M at 1x, $1.94M at 1.5x (the integrated base), $1.70M at 2x, $1.45M at 3x, $1.11M at 10x.
  - Bottom-up: 132 conventional person-months after a 4 person-month Echelon reuse credit, at $120/h.
  - 30% of the effort cannot be compressed.
- **No investment below about $1.0M is safe with live money** at any multiple.
  - $1.0M works only at 5x or more.
  - $1.8M works at 1.5x or more.
  - $5M covers the full conventional scope at about 1.3x or more.
- Even a funded MSP is only "conditional". It still needs:
  - a bank or processor agreement and custodian file access;
  - a counsel opinion on money transmission;
  - a SOC observation period;
  - a second maintainer;
  - a commercial licence for the PolyForm-NC components (CNV-GOV-009).
- **Unbound defines no minimum product:** 1,185 of its 1,208 normative items (98%) are initial scope. Requirements candidate RC-AN-010 and report 17 propose a scope gate.
- **Deferral moves cost rather than removing it.** Of 24 deferrable capabilities, several push labour back to operations or sponsors while deferred: manual custodian import, scripted migration, manual SOC evidence. The integrated sequences add a deferred-scope build tranche after the second go-live (ADV2-008).
"""),
    "05-echelon-productivity-evaluation.md": ("05: Echelon productivity evaluation", f"""
**Pass:** DEV (component verification, throughput, productivity sensitivity, measurement methodology, reduce vs transfer). **Data:**
- [`component-verification.csv`]({D}/component-verification.csv) (26 repos);
- [`throughput.csv`]({D}/throughput.csv) (31);
- [`loc.json`]({D}/loc.json);
- [`build-logs/`]({D}/build-logs/).

**Revisions examined:** 26 component repositories (praxis `12bf995`, ordo `db6d39e`, dokimos `6ea8624`, aegis `711e026`, vigila `feab755`, strata `c6a384e`, limen `743cdb9`, forma `c8f40b4`, folio `56a18e1`, conditor `cadd5c7` and 16 others; see [00](00-source-baseline.md)).

**Integrator conclusions**
- **Echelon is real, healthy software but contains no DAF capability** [M].
  - All 26 repos built and about 9,768 tests passed. Every failure was environmental or timing.
  - There is no ledger, payments, grants or reconciliation code. Fides is GitHub-only identity, Arca stores records in GitHub, and no repo runs SAST or dependency scanning.
  - 21 of 26 repos are PolyForm Noncommercial and two have no licence.
- **High output is demonstrated; the cost of an accepted capability is not** [S/M].
  - About 9,045 commits and about 1.12M lines added over 105 commit days, by one human author with 46.5% of commits agent-authored.
  - The only independent end-to-end trial (Rehearsal 4) passed 1 of 108 P0 requirements and was not accepted.
  - The ordo controlled trial cost $12-27 of compute per feature mission, and both agents' self-reported test results were wrong.
  - No human time is recorded anywhere.
- **Productivity sensitivity (1.5x, 2x, 3x, 5x, 10x) is bounded by Amdahl's law.**
  - With 30% of effort incompressible and compute at 5% of replaced construction, the savings ceiling is about 66% of conventional cost.
  - A nominal 10x is about 2.7x effective.
  - Agent compute is under 5% of build cost in every scenario: the cost is human review.
- **What Echelon can reduce** [D/E]:
  - Development: $0-1.1M on an MSP (UI and print markup, schema and fault tooling, and agent-written code if measured).
  - Operating cost: nothing yet. Echelon supplies no runtime.
  - Owner and Echelon time is a transfer and must be charged.
- **The measurement protocol below is the cheapest decisive evidence in the mission.** Run it on the next 3-5 Unbound capabilities: human hours per accepted capability, compute, cycle time, defect escape, rework and review overhead.
- **Threshold to replace conventional estimates:** effective 2x or better on accepted capabilities with no worse defect escape.
- **EDF applicability:** the Echelon development history and Rehearsal 4 are observed outcomes; ADV2 applied EDF to them (report 16). EDF was **not** executed on the hypothetical company.
"""),
    "06-workload-driven-staffing.md": ("06: Workload-driven staffing and handling-time targets", f"""
**Pass:** OPS (parts 3-4), integrated in model sections 4-6. **Data:**
- [`handling-targets.csv`]({D}/handling-targets.csv);
- [`workload-tails.csv`]({D}/workload-tails.csv);
- [`staffing-capacity.csv`]({D}/staffing-capacity.csv) (11 roles).

**Integrator conclusions**
- **Handling time is a small cost.** At 50.7 minutes, labour is about $55 of $877 revenue per account-year (6%).
- **Handling-time targets:**
  - The servicer floor is about **11.7 minutes** per account-year. About 9 of those minutes are legal, independence or control work.
  - 10 minutes is infeasible without weakening control.
  - 20 is reachable only with every lever plus transfers.
  - About 30 is a plausible steady state.
  - 45-75 is realistic in each sponsor's first year, before board delegation.
  - In the model, F5 at $1B goes from 1.7% loss at 10 minutes to 17.9% loss at 50 and 43.1% loss at 100 (section 4). At $1.5B, F5 standalone break-even moves from $1.49B at 30 minutes to $1.67B at 50 (section 3).
- **December, not the annual average, sets headcount above about 5,000 accounts** [OPS].
  - Temporary staff cannot release payments.
  - The integrated model now makes year-round release-capable employees carry half the December excess (ADV2-003).
- **Ratio-based and workload-driven staffing compared (model section 6).** Workload-driven staffing does **not** save money once December release capacity is respected.
  - F5 costs $0.06M less than the previous ratio model at 2,500 accounts.
  - It costs $0.1M more at 5,000-10,000 accounts and $0.5-1.9M more at 20,000-40,000.
  - **This corrects the previous study:** its ratio triggers understated December headcount.
- **Real drivers replace the ratios:**
  - Accounting scales with sponsor books, feed sources and break rates, not accounts.
  - Integration scales with distinct counterparties and their change rate.
  - Implementation scales with new sponsors on a learning curve.
  - Compliance needs a named owner from go-live (modelled as a 0.25 FTE floor).
  - Platform change control needs three engineers able to approve (author plus two), employees or contracted (CNV-PLT-010).
- **Tails** (model section 5, $1.5B):
  - A tail-heavy book (minutes ×2) moves F5 break-even to $2.10B.
  - December plus an incident plus an absence moves it to $1.77B.
  - The severe combined stress has no break-even below $20B.
"""),
    "08-ai-native-operating-architecture.md": ("08: AI-native operating architecture", f"""
**Pass:** OPS (part 6). **Data:** [`ai-capabilities.csv`]({D}/ai-capabilities.csv) (16 capabilities).

**Integrator conclusions**
- The architecture is a **single operational model of cases, events, controls and evidence**, not departments re-implemented as agents.
- All 16 AI capabilities are capped at *recommend* and *prepare*. Every money movement, sponsor reserved decision and OFAC disposition stays with an authorised human or a deterministic rule the sponsor has adopted.
- **AI must not invent financial records, bypass sponsor authority or weaken controls.** Each capability has authority limits, evidence requirements, escalation criteria and a fail-closed behaviour.
- **This is a proposal. No runtime exists:**
  - Echelon is engineering tooling.
  - Unbound is requirements only.
  - Nothing in this report is demonstrated operation.
- Requirements candidates RC-AN-004 (case ownership), RC-AN-013 (bounded AI authority) and RC-AN-016 (transfer-not-saving reporting) carry the architecture into Unbound governance (report 17).
"""),
    "09-administrative-overhead-elimination.md": ("09: Administrative overhead elimination", f"""
**Pass:** OPS (part 5), with ADV2-013. **Data:** [`overhead.csv`]({D}/overhead.csv) (13 categories).

**Integrator conclusions**
- Conventional coordination is about 12 hours per person-week; the AI-native residual is about 4.75. The integrated design assumes:
  - a shared case/event model;
  - generated status and management reporting;
  - no ticket routing;
  - no re-keyed data;
  - no interdepartmental reconciliation.
- **The real gain is small.** The previous study's 1,520 productive hours already deducted about 6 hours a week for meetings and administration. Against that baseline the gain is about 1.25 hours per person-week, **about 3% of capacity**.
- The integrated model costs coordination only beyond six pairs (ADV2-013) and gives the outcome-designed variant +3% capacity.
- **Governance overhead remains:**
  - board and sponsor reporting;
  - change approval;
  - the independent-review sample;
  - the SOC control calendar;
  - December readiness.
- These are obligations, not habits.
- The overhead sources are broad-population surveys (Microsoft 365 telemetry; an Asana survey reported in Computerworld), not small servicers.
"""),
    "10-pricing-strategy-reassessment.md": ("10: Pricing strategy reassessment", f"""
**Pass:** COM (part 1), integrated in model section 11. **Data:**
- [`sponsor-value.csv`]({D}/sponsor-value.csv) (5 archetypes + top 30 sponsors);
- [`pricing-structures.csv`]({D}/pricing-structures.csv) (210 rows: six structures).

**Integrator conclusions**
- **20 bps remains the working objective** for:
  - small and mid-balance books;
  - books already outsourced at 25-40 bps (e.g. the U.S. Charitable Gift Trust, where Ren earns about 40 bps);
  - high-volume, small-balance books such as National Christian Foundation;
  - sponsors that commit to retiring DAF staff and systems.
- **It is not value-defensible for books averaging $1M or more per account.** There, equivalent-scope value is about 5-10 bps.
  - The median value-based maximum across 24 winnable top-30 sponsors is 7.3 bps.
  - It reaches 19.3 bps only if sponsors cut staff.
- **$737 per account (Morgan Stanley GIFT) is not a market-wide ceiling.**
  - It buys a narrow scope: a 0-employee bank-channel programme where Morgan Stanley earns separately.
  - Observed per-account prices run from $429 to $1,198.
  - At high balances, though, the value limit is real.
- **Correction to the previous study:** its recommended tariff ($150 per account + 7.5 bps) leaves only 3 of 24 winnable sponsors better off. "$350 per account + 3 bps, capped at 20 bps" leaves 16, and a 50% value share leaves 22.
- **Asset-weighted, the accepted structures earn about 6-7 bps on top-30 assets, not 20.** In the model:
  - F5 at 7 bps never breaks even below $3.8B at any balance.
  - At $250k balances, $350 + 3 bps (cap not modelled) breaks even at $1.56B.
  - A $250 per-account floor on 20 bps lowers break-even to $0.93B.
- **Efficiency does not have to be passed through** where value supports the price. Service, reliability, transparency and portability are the competitive grounds.
- **Safeguards stay in every structure:**
  - payout-neutral fee base;
  - cost-based complex-gift and foreign-grant fees;
  - floors waived in wind-down;
  - payment rails passed through at cost.
"""),
    "12-incremental-commercial-opportunities.md": ("12: Incremental commercial opportunities", f"""
**Pass:** COM (parts 2-3), integrated in sequences D and G (model section 9). **Data:** [`opportunities.csv`]({D}/opportunities.csv) (11 capabilities).

**Integrator conclusions**
- **Most standalone opportunities have potential, not demonstrated, demand.**
- Where demand is demonstrated, the products are commoditised, contested or risky as disconnected products:
  - charity verification data;
  - disbursement, which raises a money-transmission question;
  - donor portals, which would sit on incumbents' ledgers;
  - migration.
- **Two have paid precedents and are also platform components:** migration/import tooling and the eligibility (charity verification) service. Build these first.
- **Narrow entry does not reduce capital in the model.**
  - Sequence D needs a $7.0M equity need; sequence G needs $6.9M.
  - A non-custodial service still carries SOC 2, insurance, compliance consulting and support from its own launch.
  - At an assumed $40k per sponsor, six sponsors earn $240k a year against about $0.6M of fixed non-personnel cost.
  - Its value is **evidence**: price, recall of charity matching, buyer behaviour. Its value is not funding.
- **Customer-funded development is limited.**
  - Implementation fees exist (TIFIN's SEC filing, Ren's product descriptions) but amounts are not public.
  - A realistic $100-500k prepaid implementation covers onboarding, not the platform build.
  - A charitable sponsor that pays above fair value for vendor-owned IP raises a private-benefit risk.
  - No public DAF design-partner prepayment or equity deal was found.
"""),
    "13-incumbent-replication-analysis.md": ("13: Incumbent replication analysis", f"""
**Pass:** COM (part 4). **Data:** [`replication.csv`]({D}/replication.csv) (7 advantages + combination + 4 incumbent responses).

**Integrator conclusions**
- **The previous study's "easily copied" verdict is refined, not reversed.**
- **Each lever alone is copyable in about 6-24 months.** Minimum-touch operations *raise* a bps-priced incumbent's margin, so incumbents will copy them quietly without cutting price.
- **The combination is moderately durable against multi-lineage incumbents.** The combination is a single ledger with evidence-by-default controls, reusable configuration, portability and per-account pricing. An incumbent such as Ren runs an acquisition stack with separate contracts and no observed ledger unification, so transforming its installed base would take about 48-72 months.
- **It is not durable against:**
  - a funded greenfield sub-brand or an acquisition, at about 18-30 months;
  - incumbents that already transform: Vanguard spends $2-6M a year on tech services, Fidelity paid McKinsey $11.8M, and Foundant won 6 of 8 recorded community-foundation migrations.
- Replication scores are analyst judgement (same model family). No incumbent was interviewed.
"""),
    "15-failure-and-resilience-analysis.md": ("15: Failure and resilience analysis", f"""
**Pass:** LYR (part 4), with ADV2-027. Integrated in model section 10 and [`failure-costs.csv`](model/out/failure-costs.csv). **Data:** [`failure-catalogue.csv`]({D}/failure-catalogue.csv) (23 failures: consequence, detection, leading indicator, contingency, recovery cost, stop option).

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
"""),
    "16-adversarial-review.md": ("16: Adversarial review", f"""
**Pass:** ADV2, a hostile review of the model, the four passes and the integrator's conclusions. **Data:**
- [`adversarial-findings.csv`]({D}/adversarial-findings.csv) (27 model findings: 1 critical, 12 major, 14 minor);
- [`hidden-costs.csv`]({D}/hidden-costs.csv) (23);
- [`framework-procedure.jsonl`]({D}/framework-procedure.jsonl) (26: Clarity procedure and decision records; EDF records);
- [`nine-perspectives.csv`]({D}/nine-perspectives.csv);
- [`falsification.csv`]({D}/falsification.csv);
- [`adv-experiments.out`]({D}/adv-experiments.out).

**Framework revisions:** Clarity `200a9eb`; EDF `710d54c`.

**What is not claimed**
- Clarity was applied with its decision record. Ownership acceptance, decision date, review cadence and outcome could not be performed. Under Clarity's readiness rule, all five decisions are therefore **"not ready"**.
- EDF was applied only to observed outcomes: the Echelon development history, Rehearsal 4 and the ordo cost trial. It was **not** executed on the hypothetical company.
- **Reviewer, passes and integrator are the same model family. This is not independent validation.**

## Integrator disposition of the findings

The model was corrected and every analysis re-run after this review (23/23 tests). Numbers quoted in the ADV2 sections below are **pre-fix** values.

| Finding(s) | Disposition | Effect |
|---|---|---|
| ADV2-001 (critical) aggregate optimism | **Accepted.** Steady-state adjustments are an explicit switch (`withAdjustments`: sales to $250k, independent reconciler, turnover, replacement onboarding); build base 1.5x; Echelon charge raised; December carried by staff. Headline is now a range | F5 standalone break-even $1.39B → $1.67B base, $1.85B adjusted; full-scope platform $2.46-2.65B |
| ADV2-002 LYR labelled "conservative" | **Accepted.** Renamed "full-scope platform base"; integrated MSP base Echelon charge $135k + $60k licence | Both bases reported side by side |
| ADV2-003 no December capacity limit | **Accepted.** 50% of the December release excess carried by year-round release-capable employees; the rest at +50% | Workload staffing now costs more than ratios above 5,000 accounts (report 06) |
| ADV2-004 CNV-GOV-003 three-person release, reconciliation outside chain | **Accepted.** `controlCheck` requires three authorised people and an out-of-chain reconciler; F3 hires; F5/F6 carry a contracted independent reviewer | F3 admissible only with hires; minimum safe organisation is three core plus hires (report 07) |
| ADV2-005 F1/F2 admissibility | **Accepted.** Marked "NOT ADMISSIBLE with live money" in every break-even row | F1/F2 are pre-launch build organisations only |
| ADV2-006 sequences omit recurring platform cost | **Accepted.** Echelon share and licence from formation; non-production, servicing-specific platform and maintenance gap from go-live | Capital +$0.5-1.0M |
| ADV2-007 2x build base | **Accepted.** Base 1.5x; 2-3x is upside to be earned by measurement | Minimum build $1.70M → $1.94M |
| ADV2-008 deferred scope | **Accepted.** 15%-of-scope tranche over 12 months after the second go-live | Capital +$0.5M |
| ADV2-009 capital/ROIC definitions | **Accepted.** Equity need (no financing) and debt-financed trough both reported; NPV at 15% with terminal value; ROIC labelled a year-5 snapshot | Headline capital is the equity need |
| ADV2-010 combined scenario | **Accepted.** Licensees bear cost only up to net licence contribution ($300k − $250k sales − $35k SOC 2) | Combined case ≈ standalone ($1.56B) |
| ADV2-011 attribution | **Accepted.** Cost bridge leads report 14 | Most of the improvement is build and sales assumptions |
| ADV2-012 Echelon licence | **Accepted.** $60k a year base (owner-set) + LYR cost-plus failure case ($351k) + go-live gate (RC-AN-009) | — |
| ADV2-013 coordination double count | **Accepted.** Coordination costed beyond 6 pairs | Small favourable |
| ADV2-014 productivity costing bug | **Fixed.** Hires costed on paid hours | Outcome-designed variant now gains its 3% |
| ADV2-015 transfers not reported | **Accepted.** Transfer ledger in reports 02 and 14 | — |
| ADV2-016 pre-delegation per sponsor | **Fixed.** Per-sponsor early target for 12 months after each go-live | Capital up |
| ADV2-017 narrow-entry assurance | **Fixed.** CST-C04 kept | — |
| ADV2-018 code approvers | **Fixed.** Moved to Layer B (platform control) | — |
| ADV2-019 fixed layer charge | **Partly accepted.** Kept as a fixed amount for fixed lines; documented | Small |
| ADV2-020 test | **Fixed.** Asserts per design; documents that fully allocated can exceed standalone | — |
| ADV2-021 hidden contracted FTE | **Fixed.** Total FTE reported; F3 hires | — |
| ADV2-022, -023 sales and steady-state omissions | **Accepted** via `withAdjustments` | — |
| ADV2-024 price/segment condition | **Accepted.** Every break-even states 20 bps, 5 sponsors, $250k; model section 11 shows tariffs and balances | — |
| ADV2-025 pre-launch assurance timing | **Open.** Pre-launch fixed share 0.4 kept; SOC 1 observation and insurance binding timing is a limitation | Capital understated by up to about $0.1M |
| ADV2-026 sponsor-retained minutes (OPS 2.7 vs COM 7.0) | **Open.** Reported as a transferred-cost range, not carried by the model | Sponsor-side cost $0.17-1.30M a year at $1B ([`hidden-costs.csv`]({D}/hidden-costs.csv)) |
| ADV2-027 correlated failures | **Accepted.** Two joint modifiers; staged gates (report 15) | Joint failure +$2.1-4.2M |

**Does AI-native merely hide conventional costs?** Partly. At $1B, 5 sponsors and 4,000 accounts, the hidden-cost ledger finds:
- $0.75-3.06M a year not counted in the model (base $1.66M);
- $0.76M partly counted.

The largest sinks:
- **Sponsors:** oversight and appointees, migration, payment rails ($84.5k measured pass-through), the third release person, and audit evidence. Sponsor-side subset $0.17-1.30M.
- **Deferred scope.**
- **Echelon reliance**, now partly charged.

Agent compute is small. Contractors are now visible as total FTE. These costs are real even where the servicer's P&L does not carry them; a sponsor CFO will price them.
"""),
    "17-requirements-transfer-candidates.md": ("17: Requirements transfer candidates", f"""
**Pass:** LYR (part 3), with ADV2 challenges. **Data:** [`requirements-candidates.csv`]({D}/requirements-candidates.csv) (20 candidates RC-AN-001..020, each traced to Unbound clause or baseline IDs, with original purpose, problem, replacement, economic, operational, security and financial-control implications, acceptance criteria, evidence, uncertainty, and whether the legal obligation is preserved).

**Status:** proposals for Unbound governance only. **Unbound was not modified** (read-only, `9b38de4`). No candidate removes or weakens a legal obligation. Where a candidate relaxes a control, the relaxation is gated on the auditor's and the board's acceptance and on measured evidence.

**Integrator notes**
- **RC-AN-014 (replacing CNV-PLT-010's two human approvers for control-relevant code) is unproven and may be worse.** ADV2 and the integrator recommend keeping CNV-PLT-010 until an auditor accepts an alternative.
- **The candidates with the largest economic effect:**
  - RC-AN-008: assurance scope set by actual reliance;
  - RC-AN-010: no economic commitment before measurement, i.e. an MSP scope gate;
  - RC-AN-015: measure handling minutes before claims;
  - RC-AN-016: transfer-not-saving reporting;
  - RC-AN-017: plan for pre-delegation operation;
  - RC-AN-009: no production dependency on non-commercial terms.
- **Relation to the previous study's 17 candidates** (servicing-economics report 09): this set adds the outcome-design, measurement and licensing candidates. It does not withdraw any earlier candidate.

## Candidate summary

{{CANDIDATES}}
"""),
}

BODIES = {
    "01-conventional-assumption-register.md": [("lyr", starts("Part 2"))],
    "02-outcome-driven-enterprise-design.md": [("ops", starts("Summary", "Method", "Part 1", "Part 2", "Challenge"))],
    "03-three-layer-economic-model.md": [("lyr", starts("LYR summary", "Method", "Part 1"))],
    "04-development-cost-reconstruction.md": [("dev", starts("Summary", "$5M origin", "$60k origin", "Scenarios", "Deferrable"))],
    "05-echelon-productivity-evaluation.md": [("dev", starts("Component verification", "Observed throughput", "Productivity", "Measurement", "What Echelon", "Evidence gaps"))],
    "06-workload-driven-staffing.md": [("ops", starts("Part 3", "Part 4"))],
    "08-ai-native-operating-architecture.md": [("ops", starts("Part 6"))],
    "09-administrative-overhead-elimination.md": [("ops", starts("Part 5", "Limitations"))],
    "10-pricing-strategy-reassessment.md": [("com", starts("COM summary", "Part 1"))],
    "12-incremental-commercial-opportunities.md": [("com", starts("Part 2", "Part 3"))],
    "13-incumbent-replication-analysis.md": [("com", starts("Part 4", "Limitations"))],
    "15-failure-and-resilience-analysis.md": [("lyr", starts("Part 4", "Challenge", "Limitations", "Largest evidence"))],
    "16-adversarial-review.md": [("adv", lambda _: True)],
    "17-requirements-transfer-candidates.md": [("lyr", starts("Part 3"))],
}


def body(root, spec):
    return "\n\n".join(sections(load(root, group), keep) for group, keep in spec)


def main(argv):
    root = Path(argv[1] if len(argv) > 1 else ".")
    for name, (title, preface) in PREFACES.items():
        text = doc(title, preface.replace("{CANDIDATES}", candidates_table(root)), body(root, BODIES[name]))
        (root / OUT / name).write_text(text, encoding="utf-8")
        print(f"wrote {name} ({len(text):,} chars)")


if __name__ == "__main__":
    main(sys.argv)
